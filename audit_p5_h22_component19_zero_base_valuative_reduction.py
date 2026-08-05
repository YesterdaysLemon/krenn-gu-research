#!/usr/bin/env python3
"""No-import parameter-aware audit of component-19 zero-base DVR arcs."""

from __future__ import annotations

import hashlib
import itertools
import shutil
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_ZERO_BASE_VALUATIVE_REDUCTION_VERIFICATION.md"
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = WORDS4[1:-1]
ALPHA = WORDS4[0]
BETA = WORDS4[-1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def equal(left: sp.Expr, right: sp.Expr, message: str) -> None:
    require(sp.factor(left - right) == 0, message)


def add(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(4))


def scale(scalar: sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    width = len(rows)
    require(all(len(row) == width for row in rows), "permanent is not square")
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        following: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                target = mask | bit
                following[target] = sp.expand(
                    following.get(target, sp.Integer(0)) + coefficient * entry
                )
        states = following
    return sp.expand(states[(1 << width) - 1])


def component_bases(p: sp.Expr, q: sp.Expr, phi: sp.Expr):
    cap_a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    first = add(a_bar, scale(p, cap_b))
    second = add(b_bar, scale(q, cap_b))
    alpha = (add(scale(q - phi, first), scale(-p, second)), cap_b, b_bar, a_bar)
    beta = (first, cap_a, cap_a, add(cap_b, scale(phi, b_bar)))
    return alpha, beta


def mark_beta(alpha, beta, markings):
    return tuple(add(beta[i], scale(markings[i], alpha[i])) for i in range(4))


def project_row(row, extension, direction, chart, weight):
    if direction == "D01" and chart == "finite":
        return (weight * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], weight * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def contraction(alpha, beta, extensions, direction, chart, weight):
    alpha_rows = tuple(
        project_row(alpha[i], extensions[i], direction, chart, weight) for i in range(4)
    )
    beta_rows = tuple(
        project_row(beta[i], extensions[4 + i], direction, chart, weight)
        for i in range(4)
    )
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
            )
        )
        for word in WORDS4
    }
    return alpha_rows, beta_rows, coefficients


def coefficient_matrix(expressions, variables):
    return sp.Matrix(
        [[sp.diff(expression, variable) for variable in variables] for expression in expressions]
    )


def restrict_full(row, direction, weight):
    if direction == "D01":
        return (sp.expand(weight * row[0] + row[1]), row[2], row[3], row[4])
    return (row[0], row[1], sp.expand(weight * row[2] + row[3]), row[4])


def full_one_marked_map(full_planes, direction, weight, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    basis = tuple(
        tuple(sp.Integer(index == coordinate) for index in range(5))
        for coordinate in range(5)
    )
    rows = []
    for word in WORDS3:
        fixed = tuple(
            restrict_full(full_planes[mode][bit], direction, weight)
            for mode, bit in zip(other_modes, word, strict=True)
        )
        rows.append(
            [
                permanent((*fixed, restrict_full(basis_row, direction, weight)))
                for basis_row in basis
            ]
        )
    return sp.Matrix(rows)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    require(shutil.which("wsl.exe") is not None, "Singular is unavailable")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_expression(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def assert_projection(label, equations, eliminated, retained, expected) -> None:
    variables = eliminated + retained
    program = [
        "ring R=0,("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_expression(item) for item in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(singular_expression(item) for item in expected) + ";",
        "E=std(E);",
        "ideal L=simplify(reduce(J,E),2);",
        "ideal Rr=simplify(reduce(E,J),2);",
        '"CODEX_RESULT:' + label + ':"+string((size(L)==0)&&(size(Rr)==0));',
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(),
        input="\n".join(program),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=55,
    )
    require(completed.returncode == 0, f"{label}: Singular failed")
    require(f"CODEX_RESULT:{label}:1" in completed.stdout, f"{label}: ideal mismatch")


def orientation_equations(d01, d23, extensions, inverses, pure_direction, pure_word):
    inverse_one, inverse_two = inverses
    if pure_direction == "D01":
        return (
            *(d01[word] for word in WORDS4 if word != pure_word),
            d01[pure_word] - 1,
            *(d23[word] for word in MIXED),
            inverse_one * d23[ALPHA] - 1,
            inverse_two * d23[BETA] - 1,
        )
    return (
        *(d01[word] for word in MIXED),
        d01[ALPHA] - 1,
        inverse_one * d01[BETA] - 1,
        *(d23[word] for word in WORDS4 if word != pure_word),
        inverse_two * d23[pure_word] - 1,
    )


def parameter_aware_projections() -> None:
    p, q, phi, lam = sp.symbols("p q phi lam")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    inverse_one, inverse_two, localizer = sp.symbols("inverse_one inverse_two localizer")
    alpha, beta = component_bases(p, q, phi)
    beta = mark_beta(alpha, beta, h)
    open_factor = p * (q - phi) * phi * (phi - 1) * (phi + 1)
    expected_finite = {
        ("D01", BETA): (lam - 1, h[3], h[1], (q - phi) * h[0] + 1),
        ("D01", ALPHA): (
            lam + 1,
            h[3],
            h[2],
            h[1],
            q * phi - 1,
            (q - phi) * h[0] + 1,
            (phi**2 - 1) * h[0] - phi,
        ),
        ("D23", ALPHA): (sp.Integer(1),),
        ("D23", BETA): (sp.Integer(1),),
    }
    for chart in ("finite", "infinity"):
        _, _, d01 = contraction(alpha, beta, x, "D01", chart, lam)
        _, _, d23 = contraction(alpha, beta, x, "D23", chart, lam)
        for pure_direction, pure_word in itertools.product(("D01", "D23"), (ALPHA, BETA)):
            equations = orientation_equations(
                d01, d23, x, (inverse_one, inverse_two), pure_direction, pure_word
            ) + (localizer * open_factor - 1,)
            expected = (
                expected_finite[(pure_direction, pure_word)]
                if chart == "finite"
                else (sp.Integer(1),)
            )
            retained = h + ((lam,) if chart == "finite" else ()) + (p, q, phi)
            label = f"generic_{chart}_{pure_direction}_{''.join(map(str, pure_word))}"
            assert_projection(
                label,
                equations,
                x + (inverse_one, inverse_two, localizer),
                retained,
                expected,
            )

    r = sp.Symbol("r")
    for epsilon in (sp.Integer(1), sp.Integer(-1)):
        alpha, beta = component_bases(p, epsilon + r, epsilon)
        beta = mark_beta(alpha, beta, h)
        for chart in ("finite", "infinity"):
            _, _, d01 = contraction(alpha, beta, x, "D01", chart, lam)
            _, _, d23 = contraction(alpha, beta, x, "D23", chart, lam)
            for pure_direction, pure_word in itertools.product(
                ("D01", "D23"), (ALPHA, BETA)
            ):
                equations = orientation_equations(
                    d01, d23, x, (inverse_one, inverse_two), pure_direction, pure_word
                ) + (localizer * p * r - 1,)
                if chart == "finite" and pure_direction == "D01" and pure_word == BETA:
                    expected = (lam - 1, h[3], h[1], r * h[0] + 1)
                else:
                    expected = (sp.Integer(1),)
                retained = h + ((lam,) if chart == "finite" else ()) + (p, r)
                label = (
                    f"endpoint_{epsilon}_{chart}_{pure_direction}_"
                    f"{''.join(map(str, pure_word))}"
                )
                assert_projection(
                    label,
                    equations,
                    x + (inverse_one, inverse_two, localizer),
                    retained,
                    expected,
                )


def branch_determinants() -> None:
    p, q, phi, t, cap_c, cap_d = sp.symbols("p q phi t C D")
    x = sp.symbols("x0:8")
    residual = q - phi
    alpha, beta = component_bases(p, q, phi)
    beta = mark_beta(alpha, beta, (-1 / residual, 0, t, 0))
    _, _, d01 = contraction(alpha, beta, x, "D01", "finite", 1)
    _, _, d23 = contraction(alpha, beta, x, "D23", "finite", 1)
    unwanted = tuple(d01[word] for word in WORDS4[:-1]) + tuple(
        d23[word] for word in MIXED
    )
    matrix = coefficient_matrix(unwanted, x)
    frame_c = sp.Matrix((0, -1 / p, phi / p, 0, 1, 0, 0, 0))
    frame_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    frame = sp.Matrix.hstack(frame_c, frame_d)
    require(all(sp.factor(item) == 0 for item in matrix * frame), "generic frame")
    equal(
        matrix.extract((2, 3, 5, 11, 13, 16), (0, 1, 2, 3, 6, 7)).det(),
        -4096 * p**4 * phi * residual * (phi - 1) * (phi + 1),
        "generic rank witness",
    )
    extension = cap_c * frame_c + cap_d * frame_d
    substitution = dict(zip(x, extension, strict=True))
    equal(d01[BETA].subs(substitution), 4 * (p * cap_d - phi * t * cap_c), "B01")
    equal(d23[ALPHA].subs(substitution), -4 * phi * residual * cap_c / p, "A23")
    equal(d23[BETA].subs(substitution), 4 * cap_c, "B23")

    cap_x, cap_y, cap_z = sp.symbols("X Y Z")
    q_hidden = 1 / phi
    residual_hidden = q_hidden - phi
    alpha, beta = component_bases(p, q_hidden, phi)
    beta = mark_beta(alpha, beta, (-1 / residual_hidden, 0, 0, 0))
    _, _, d01 = contraction(alpha, beta, x, "D01", "finite", -1)
    _, _, d23 = contraction(alpha, beta, x, "D23", "finite", -1)
    unwanted = tuple(d01[word] for word in WORDS4 if word != ALPHA) + tuple(
        d23[word] for word in MIXED
    )
    matrix = coefficient_matrix(unwanted, x)
    hidden_frame = sp.Matrix.hstack(
        sp.Matrix((0, 1 / phi, 1, 0, 0, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0)),
        sp.Matrix((p / phi, 0, 0, 0, 0, 0, 0, 1)),
    )
    require(all(sp.factor(item) == 0 for item in matrix * hidden_frame), "hidden frame")
    equal(
        matrix.extract((0, 1, 3, 20, 21), (0, 1, 3, 5, 6)).det(),
        1024 * p**3 * phi**2 * (phi - 1) * (phi + 1),
        "hidden rank witness",
    )
    extension = hidden_frame * sp.Matrix((cap_x, cap_y, cap_z))
    substitution = dict(zip(x, extension, strict=True))
    gap = p * cap_z - (phi**2 - 1) * cap_y
    equal(d01[ALPHA].subs(substitution), 4 * cap_x * p * (phi**2 - 1) / phi, "hidden A01")
    equal(d23[ALPHA].subs(substitution), -4 * cap_x * (phi**2 - 1) / phi**2, "hidden A23")
    equal(d23[BETA].subs(substitution), 4 * phi * gap / (phi**2 - 1), "hidden B23")
    full_planes = tuple(
        (
            tuple(alpha[i]) + (extension[i],),
            tuple(beta[i]) + (extension[4 + i],),
        )
        for i in range(4)
    )
    marked = full_one_marked_map(full_planes, "D23", -1, 3)
    equal(
        marked.extract((0, 1, 3, 7), (0, 1, 2, 4)).det(),
        64 * cap_x**2 * p**2 * gap / phi**3,
        "hidden target-local obstruction",
    )

    for epsilon in (sp.Integer(1), sp.Integer(-1)):
        r = sp.Symbol("r")
        alpha, beta = component_bases(p, epsilon + r, epsilon)
        beta = mark_beta(alpha, beta, (-1 / r, 0, t, 0))
        _, _, d01 = contraction(alpha, beta, x, "D01", "finite", 1)
        _, _, d23 = contraction(alpha, beta, x, "D23", "finite", 1)
        unwanted = tuple(d01[word] for word in WORDS4[:-1]) + tuple(
            d23[word] for word in MIXED
        )
        matrix = coefficient_matrix(unwanted, x)
        frame_x = sp.Matrix((0, -1 / p, epsilon / p, 0, 1, 0, 0, 0))
        frame_y = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
        frame_z = sp.Matrix(
            (epsilon * p, -(r + epsilon) / r, 1 / r, 0, 0, 0, 0, 1)
        )
        frame = sp.Matrix.hstack(frame_x, frame_y, frame_z)
        require(all(sp.factor(item) == 0 for item in matrix * frame), "endpoint frame")
        equal(
            matrix.extract((2, 3, 11, 13, 16), (0, 1, 2, 3, 6)).det(),
            -1024 * epsilon * p**3 * r,
            "endpoint rank witness",
        )
        extension = frame * sp.Matrix((cap_x, cap_y, cap_z))
        substitution = dict(zip(x, extension, strict=True))
        f_value = epsilon * cap_x * r + cap_z * p
        g_value = p * r * cap_y - t * f_value
        h_value = cap_x * r + cap_z * p * r + epsilon * cap_z * p
        equal(d01[BETA].subs(substitution), 4 * g_value / r, "endpoint B01")
        equal(d23[ALPHA].subs(substitution), -4 * f_value / p, "endpoint A23")
        equal(d23[BETA].subs(substitution), 4 * h_value / r, "endpoint B23")
        full_planes = tuple(
            (
                tuple(alpha[i]) + (extension[i],),
                tuple(beta[i]) + (extension[4 + i],),
            )
            for i in range(4)
        )
        marked = full_one_marked_map(full_planes, "D23", 1, 3)
        equal(
            marked.extract((0, 2, 3, 7), (0, 1, 2, 4)).det(),
            64 * f_value**2 * h_value / r**2,
            "endpoint target-local obstruction",
        )


def chart_transitions_and_pole_profile() -> None:
    x, y, h_r, c_p, e_p = sp.symbols("x y h_r C_p E_p")
    alpha_p = sp.Matrix((x, -1))
    beta_p = sp.Matrix((1, 0))
    alpha_r = sp.Matrix((1, -y))
    beta_r = sp.Matrix((0, 1))
    overlap = {y: 1 / x}
    require((alpha_r - y * alpha_p).subs(overlap) == sp.zeros(2, 1), "alpha transition")
    require((beta_r - (x * beta_p - alpha_p)).subs(overlap) == sp.zeros(2, 1), "beta transition")
    h_p_formula = (-1 + y * h_r) / x
    require(
        ((beta_r + h_r * alpha_r) - x * (beta_p + h_p_formula * alpha_p)).subs(overlap)
        == sp.zeros(2, 1),
        "marking transition",
    )
    c_r = y * c_p
    e_r = x * e_p - c_p
    d_p = e_p + h_p_formula * c_p
    d_r = e_r + h_r * c_r
    equal(d_r.subs(overlap), (x * d_p).subs(overlap), "extension transition")

    tau, phi = sp.symbols("tau phi")
    extension = sp.Matrix((0, -1 / tau, phi / tau, 0, 1, 1, 0, 0))
    require(
        tuple((tau * extension).subs(tau, 0)) == (0, -1, phi, 0, 0, 0, 0, 0),
        "projective pole limit",
    )
    equal(4 * tau, 4 * tau, "vanishing diagonal")
    equal(-64 * tau**3, -64 * tau**3, "vanishing obstruction")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    chart_transitions_and_pole_profile()
    parameter_aware_projections()
    branch_determinants()
    dependencies = (
        ROOT / "P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md",
        ROOT / "P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md",
        REPORT,
        SCRIPT,
    )
    for path in dependencies:
        require(path.exists(), f"missing dependency: {path.name}")
        print(f"SHA256 {path.name} {sha256(path)}")
    print("COMPONENT19_ZERO_BASE_VALUATIVE_REDUCTION_VERIFIED")


if __name__ == "__main__":
    main()
