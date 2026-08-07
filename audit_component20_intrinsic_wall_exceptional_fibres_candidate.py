#!/usr/bin/env python3
"""Independent no-import audit of component-20 exceptional wall fibres."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sympy as sp
import z3

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
SOLVER_DIR = ROOT / "tmp" / "component20_exceptional_fibres_audit_solver_inputs"
FROZEN_COMMIT = "00c3574f854e1f86cb8ec2304645204479c3f75e"
CANDIDATE_REPORT = ROOT / "COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md"
CANDIDATE_SCRIPT = (
    ROOT / "derive_component20_intrinsic_wall_exceptional_fibres_candidate.py"
)
CANDIDATE_CERTIFICATE = (
    ROOT / "component20_intrinsic_wall_exceptional_fibres_certificate.json"
)
PROOF_B_REPORT = ROOT / "P4_COMPONENT20_INTRINSIC_EXCEPTIONAL_BASE_GEOMETRY_PROOF_B.md"
PROOF_B_SCRIPT = (
    ROOT / "derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py"
)
COMPONENT_REPORT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
WALL_GEOMETRY_REPORT = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
WALL_H22_REPORT = (
    ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"
)
SUPPORT_ONE_REPORT = ROOT / "claims/p4/boundaries/pair-geometry/support-one-secant/P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md"
REPORT = ROOT / "COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_VERIFICATION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
ALPHA_WORD = WORDS[0]
BETA_WORD = WORDS[-1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=15,
    ).stdout.strip()


def add(*vectors: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(sum(vector[index] for vector in vectors)) for index in range(4)
    )


def scale(scalar: Any, vector: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def permanent(rows: tuple[tuple[Any, ...], ...]) -> sp.Expr:
    size = len(rows)
    require(all(len(row) == size for row in rows), "permanent input is not square")
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                target = mask | bit
                next_states[target] = sp.expand(
                    next_states.get(target, sp.Integer(0)) + coefficient * entry
                )
        states = next_states
    return sp.factor(states[(1 << size) - 1])


def wedge(left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(left[i] * right[j] - left[j] * right[i])
        for i, j in itertools.combinations(range(4), 2)
    )


def pair_matrix(
    left: tuple[tuple[Any, ...], ...], right: tuple[tuple[Any, ...], ...]
) -> sp.Matrix:
    pairs = tuple(itertools.combinations(range(4), 2))
    columns = []
    for left_row in left:
        for right_row in right:
            columns.append(
                sp.Matrix(
                    [
                        sp.expand(
                            left_row[i] * right_row[j] + left_row[j] * right_row[i]
                        )
                        for i, j in pairs
                    ]
                )
            )
    return sp.Matrix.hstack(*columns)


def pair_profile(
    planes: tuple[tuple[tuple[Any, ...], tuple[Any, ...]], ...],
) -> tuple[int, ...]:
    return tuple(
        pair_matrix(planes[i], planes[j]).rank()
        for i, j in itertools.combinations(range(4), 2)
    )


def graph_closure_audit() -> dict[str, Any]:
    p, q, a, b, arc_parameter = sp.symbols("p q a b arc_parameter")
    s = p - q + 1
    t = q * (q - 1)
    jacobian = sp.Matrix((s, t)).jacobian((p, q))
    points = ((sp.Integer(0), sp.Integer(1)), (-sp.Integer(1), sp.Integer(0)))
    determinants = {}
    coefficient_determinants = {}
    for p0, q0 in points:
        determinant = sp.factor(jacobian.det().subs({p: p0, q: q0}))
        require(determinant in (1, -1), "base ideal is not transverse")
        determinants[f"({p0},{q0})"] = str(determinant)
        coefficient_determinants[f"({p0},{q0})"] = str(-4 * determinant)
    require(sp.gcd(s, t) == 1, "base ideal does not have height two")
    graph_equation = sp.expand(s * b + t * a)
    require(
        all(graph_equation.subs({p: p0, q: q0}) == 0 for p0, q0 in points),
        "exceptional fibre has a residual equation",
    )
    require(sp.solve_poly_system((s, t), p, q) == [(-1, 0), (0, 1)], "base points")
    arcs = {
        "(0,1)": ((a - b) * arc_parameter / 2, 1 - b * arc_parameter / 2),
        "(-1,0)": (
            -1 + (a + b) * arc_parameter / 2,
            b * arc_parameter / 2,
        ),
    }
    for arc_p, arc_q in arcs.values():
        coefficients = (2 * (arc_p - arc_q + 1), -2 * arc_q * (arc_q - 1))
        require(
            tuple(sp.expand(item).coeff(arc_parameter, 1) for item in coefficients)
            == (a, b),
            "first-order direction arc",
        )
    return {
        "base_ideal": ["p-q+1", "q*(q-1)"],
        "base_points": [[0, 1], [-1, 0]],
        "jacobian_determinants": determinants,
        "coefficient_map_jacobian_determinants": coefficient_determinants,
        "regular_sequence": True,
        "graph_equation": "(p-q+1)*b+q*(q-1)*a",
        "direction_convention": "[a:b]=[p-q+1:-q*(q-1)]",
        "exceptional_fibre_at_each_base_point": "P1_[a:b]",
        "finite_segre_chart": "[a:b]=[1:rho]",
        "direct_segre_endpoint": "[a:b]=[0:1]",
        "all_first_order_directions_realized": True,
        "base_plane_tuples_are_zero_restrictions": True,
        "ordinary_nonzero_P4_fibres": False,
    }


def basis_at(
    point: tuple[int, int], segre_chart: str, rho: sp.Symbol
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    p0, q0 = map(sp.Integer, point)
    zero, one = sp.Integer(0), sp.Integer(1)
    e = (one, zero, zero, zero)
    r0 = (zero, -one, one, zero)
    r1 = (zero, -(p0 + q0), zero, one)
    if segre_chart == "finite":
        alpha0 = add(scale(rho, r0), scale(-one, r1))
        beta0 = r0
    elif segre_chart == "endpoint":
        alpha0 = r0
        beta0 = r1
    else:
        raise ValueError(segre_chart)
    v = (zero, p0, q0, one)
    u = (zero, p0 + one, q0 - one, one)
    alpha = (alpha0, e, e, (one, one, one, zero))
    beta = (beta0, u, v, e)
    require(
        all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4)), "basis rank"
    )
    coefficients = {
        word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS
    }
    require(
        all(value == 0 for value in coefficients.values()), "base restriction nonzero"
    )
    return alpha, beta


def base_plane_audit() -> dict[str, Any]:
    rho = sp.Symbol("rho")
    result = {}
    for point in ((0, 1), (-1, 0)):
        alpha, beta = basis_at(point, "endpoint", rho)
        planes = tuple((alpha[i], beta[i]) for i in range(4))
        profile = pair_profile(planes)
        require(profile == (3, 3, 3, 3, 3, 3), "zero-base pair profile")
        result[f"({point[0]},{point[1]})"] = {
            "planes": [
                [[str(entry) for entry in row] for row in plane] for plane in planes
            ],
            "restricted_tensor_support": {},
            "pair_profile": list(profile),
            "zero_restriction": True,
            "nonzero_P4_fibre": False,
        }
    return result


def mark_beta(
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
    markings: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(add(beta[i], scale(markings[i], alpha[i])) for i in range(4))


def h31_rows(
    distinguished: int,
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
) -> dict[str, Any]:
    retained_coordinates = tuple(i for i in range(4) if i != distinguished)
    rows = {}
    for word in WORDS:
        coefficients = []
        for mode in range(4):
            other_rows = tuple(
                tuple(
                    (beta[other] if word[other] else alpha[other])[coordinate]
                    for coordinate in retained_coordinates
                )
                for other in range(4)
                if other != mode
            )
            coefficients.append(permanent(other_rows))
        rows[word] = tuple(
            coefficients[mode] if bit == 0 else sp.Integer(0)
            for mode, bit in enumerate(word)
        ) + tuple(
            coefficients[mode] if bit == 1 else sp.Integer(0)
            for mode, bit in enumerate(word)
        )
    return {
        "mixed": tuple(rows[word] for word in MIXED_WORDS),
        "A": rows[ALPHA_WORD],
        "B": rows[BETA_WORD],
    }


def dot(row: tuple[Any, ...], vector: tuple[Any, ...]) -> sp.Expr:
    return sp.expand(sum(left * right for left, right in zip(row, vector, strict=True)))


def project_row(
    row: tuple[Any, ...],
    extension: Any,
    direction: str,
    weight_chart: str,
    lam: sp.Symbol,
) -> tuple[sp.Expr, ...]:
    if direction == "D01" and weight_chart == "finite":
        return (sp.expand(lam * row[0] + row[1]), row[2], row[3], extension)
    if direction == "D23" and weight_chart == "finite":
        return (row[0], row[1], sp.expand(lam * row[2] + row[3]), extension)
    if direction == "D01" and weight_chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and weight_chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, weight_chart))


def contraction_model(
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
    extensions: tuple[sp.Symbol, ...],
    direction: str,
    weight_chart: str,
    lam: sp.Symbol,
) -> dict[str, Any]:
    alpha_rows = tuple(
        project_row(alpha[i], extensions[i], direction, weight_chart, lam)
        for i in range(4)
    )
    beta_rows = tuple(
        project_row(beta[i], extensions[4 + i], direction, weight_chart, lam)
        for i in range(4)
    )
    coefficients = {
        word: permanent(
            tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }
    return {
        "coefficients": coefficients,
        "mixed": tuple(coefficients[word] for word in MIXED_WORDS),
        "A": coefficients[ALPHA_WORD],
        "B": coefficients[BETA_WORD],
    }


def singular_command(program_path: Path) -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q", str(program_path))
    if shutil.which("wsl.exe"):
        converted = subprocess.run(
            ("wsl.exe", "--exec", "wslpath", "-a", str(program_path)),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
            timeout=15,
        ).stdout.strip()
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q", converted)
    raise RuntimeError("Singular is required")


def singular_expression(expression: Any) -> str:
    numerator, denominator = sp.together(expression).as_numer_denom()
    require(denominator == 1, f"unexpected denominator: {denominator}")
    return str(sp.expand(numerator)).replace("**", "^")


def run_singular_file(program: str, label: str) -> str:
    SOLVER_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".sing",
        prefix="audit_",
        dir=SOLVER_DIR,
        delete=False,
    ) as handle:
        handle.write(program)
        program_path = Path(handle.name)
    try:
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        process = subprocess.Popen(
            singular_command(program_path),
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=creation_flags,
        )
        try:
            stdout, stderr = process.communicate(timeout=180)
        except subprocess.TimeoutExpired as exc:
            if os.name == "nt":
                subprocess.run(
                    ("taskkill", "/PID", str(process.pid), "/T", "/F"),
                    capture_output=True,
                    check=False,
                    timeout=15,
                )
            else:
                process.kill()
            process.communicate()
            raise AssertionError(f"{label}: Singular timeout") from exc
        require(
            process.returncode == 0 and not stderr.strip(),
            f"{label}: Singular failure: {stdout[-2000:]} {stderr[-2000:]}",
        )
        return stdout
    finally:
        program_path.unlink(missing_ok=True)


def project_ideal(
    label: str,
    equations: tuple[Any, ...],
    eliminated: tuple[sp.Symbol, ...],
    retained: tuple[sp.Symbol, ...],
) -> dict[str, Any]:
    variables = eliminated + retained
    require(len(set(variables)) == len(variables), f"{label}: repeated variable")
    lines = (
        "ring R=0,("
        + ",".join(str(variable) for variable in variables)
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_expression(item) for item in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(str(item) for item in eliminated) + "));",
        "ideal E=std(ideal(1));",
        "ideal left=simplify(reduce(J,E),2);",
        "ideal right=simplify(reduce(E,J),2);",
        "int isunit=((size(left)==0)&&(size(right)==0));",
        '"CODEX_META:"+string(isunit)+":"+string(size(J));',
        "int k;",
        'for (k=1;k<=size(J);k=k+1) { "CODEX_GEN:"+string(k)+":"+string(J[k]); }',
        "quit;",
    )
    stdout = run_singular_file("\n".join(lines), label)
    metas = [
        line.strip() for line in stdout.splitlines() if line.startswith("CODEX_META:")
    ]
    require(len(metas) == 1, f"{label}: missing metadata")
    _, unit_text, size_text = metas[0].split(":")
    generators = [
        line.strip().split(":", 2)[2]
        for line in stdout.splitlines()
        if line.startswith("CODEX_GEN:")
    ]
    require(len(generators) == int(size_text), f"{label}: generator count")
    return {
        "label": label,
        "unit_ideal": unit_text == "1",
        "standard_basis_size": int(size_text),
        "projected_standard_basis": generators,
        "retained_variables": [str(item) for item in retained],
    }


def audit_incidence() -> dict[str, Any]:
    rho, lam = sp.symbols("rho lam")
    markings = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse_first, inverse_second = sp.symbols("inverse_first inverse_second")
    results: dict[str, Any] = {}
    for point in ((0, 1), (-1, 0)):
        point_label = "p0_q1" if point == (0, 1) else "pm1_q0"
        results[point_label] = {}
        for segre_chart in ("finite", "endpoint"):
            alpha, unmarked_beta = basis_at(point, segre_chart, rho)
            beta = mark_beta(alpha, unmarked_beta, markings)
            segre_retained = (rho,) if segre_chart == "finite" else ()
            h31 = []
            for distinguished in range(4):
                model = h31_rows(distinguished, alpha, beta)
                equations = (
                    *(dot(row, extensions) for row in model["mixed"]),
                    dot(model["A"], extensions) - 1,
                    inverse_first * dot(model["B"], extensions) - 1,
                )
                projection = project_ideal(
                    f"{point_label}_{segre_chart}_H31_delete_{distinguished}",
                    equations,
                    extensions + (inverse_first,),
                    markings + segre_retained,
                )
                require(projection["unit_ideal"], projection["label"])
                h31.append(projection)

            individual_h22 = []
            shared_h22 = []
            for weight_chart in ("finite", "infinity"):
                weight_retained = (lam,) if weight_chart == "finite" else ()
                retained = markings + segre_retained + weight_retained
                models = {
                    direction: contraction_model(
                        alpha,
                        beta,
                        extensions,
                        direction,
                        weight_chart,
                        lam,
                    )
                    for direction in ("D01", "D23")
                }
                require(
                    all(
                        sp.Poly(coefficient, *extensions).total_degree() <= 1
                        and coefficient.subs(dict.fromkeys(extensions, 0)) == 0
                        for model in models.values()
                        for coefficient in model["coefficients"].values()
                    ),
                    "contraction is not extension-linear",
                )
                for direction in ("D01", "D23"):
                    model = models[direction]
                    individual_h22.append(
                        project_ideal(
                            f"{point_label}_{segre_chart}_{weight_chart}_{direction}_individual",
                            (
                                *model["mixed"],
                                model["A"] - 1,
                                inverse_first * model["B"] - 1,
                            ),
                            extensions + (inverse_first,),
                            retained,
                        )
                    )
                for direction, other_direction in (("D01", "D23"), ("D23", "D01")):
                    model = models[direction]
                    other = models[other_direction]
                    projection = project_ideal(
                        f"{point_label}_{segre_chart}_{weight_chart}_{direction}_shared_orientation",
                        (
                            *model["mixed"],
                            *other["mixed"],
                            model["A"] - 1,
                            inverse_first * model["B"] - 1,
                            inverse_second * other["B"] - 1,
                        ),
                        extensions + (inverse_first, inverse_second),
                        retained,
                    )
                    require(projection["unit_ideal"], projection["label"])
                    shared_h22.append(projection)
            results[point_label][segre_chart] = {
                "basis": {
                    "alpha": [[str(item) for item in row] for row in alpha],
                    "beta": [[str(item) for item in row] for row in unmarked_beta],
                },
                "H31": h31,
                "individual_H22": individual_h22,
                "shared_H22": shared_h22,
            }
    return results


def tensor_support(
    planes: tuple[tuple[tuple[Any, ...], tuple[Any, ...]], ...],
) -> dict[str, sp.Expr]:
    return {
        "".join(str(bit) for bit in word): permanent(
            tuple(planes[i][word[i]] for i in range(4))
        )
        for word in WORDS
        if permanent(tuple(planes[i][word[i]] for i in range(4))) != 0
    }


def proportional(left: tuple[Any, ...], right: tuple[Any, ...]) -> bool:
    pivot = next((i for i, value in enumerate(right) if value != 0), None)
    if pivot is None or left[pivot] == 0:
        return False
    ratio = sp.factor(left[pivot] / right[pivot])
    return all(sp.factor(left[i] - ratio * right[i]) == 0 for i in range(len(left)))


def diagonal_s_zero_audit() -> dict[str, Any]:
    d, x0, x1, x2 = z3.Reals("d x0 x1 x2")
    n = z3.If(x1 <= x2, x1, x2)
    w = z3.If(x1 <= x2, x2 - x1, x1 - x2)
    m = z3.If(n <= 0, n, z3.RealVal(0))
    z = z3.If(x0 <= n, x0, n)
    a0 = z3.If(
        x0 <= d,
        z3.If(x0 <= 2 * d + x2, x0, 2 * d + x2),
        z3.If(d <= 2 * d + x2, d, 2 * d + x2),
    )
    energy = d + n + w - 2 * m + z - a0
    expected_zero = z3.And(x1 == x2, x1 >= -d, x1 <= 0, x0 >= d)
    solver = z3.Solver()
    solver.add(d > 0, z3.Or(energy < 0, z3.Xor(energy == 0, expected_zero)))
    require(solver.check() == z3.unsat, "s=0 diagonal valuation cone")

    c0, c1, c2, cap_delta = sp.symbols("c0 c1 c2 Delta", nonzero=True)
    k = c0 / (4 * cap_delta)
    e = (sp.Integer(1), 0, 0, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    lower = (0, c1, -c2, 0)
    upper = (0, c1, c2, 0)
    negative_y_flags = {}
    for eps_x, eps_y in itertools.product((0, 1), repeat=2):
        free = add(
            cap_c,
            scale(-eps_x * k, e),
            scale(-sp.Rational(eps_y, 2) * cap_delta, upper),
        )
        actual = wedge(lower, free)
        expected = (
            eps_x * k * c1,
            -eps_x * k * c2,
            0,
            -eps_y * cap_delta * c1 * c2,
            c1,
            -c2,
        )
        require(actual == expected, "negative-y leading Pluecker flag")
        planes = ((lower, free), (e, lower), (e, lower), (e, upper))
        require(
            tensor_support(planes) == {"1110": -2 * c1 * c2}, "negative-y pure support"
        )
        negative_y_flags[f"{eps_x}{eps_y}"] = [str(value) for value in actual]

    y_zero_charts = {}
    for eps_x in (0, 1):
        free = add(cap_c, scale(-eps_x * k, e))
        planes = (
            (lower, free),
            (e, add(scale(sp.Rational(1, 2), lower), cap_c)),
            (e, add(scale(-sp.Rational(1, 2), lower), cap_c)),
            (e, upper),
        )
        require(tensor_support(planes) == {"1110": c1 * c2 / 2}, "y=0 pure support")
        y_zero_charts[str(eps_x)] = [str(value) for value in wedge(lower, free)]

    wall_text = " ".join(WALL_GEOMETRY_REPORT.read_text(encoding="utf-8").split())
    wall_h22_text = " ".join(WALL_H22_REPORT.read_text(encoding="utf-8").split())
    require(
        "E=0 iff x1=x2=y, -d<=y<=0, x0>=d." in wall_text,
        "frozen wall cone marker",
    )
    require("diagonal-source-torus" in wall_h22_text, "wall H22 scope marker")
    require("non-diagonal" in wall_h22_text, "wall non-diagonal exclusion")
    return {
        "exact_energy": "d+n+abs(x1-x2)-2*min(n,0)+min(x0,n)-min(x0,d,2*d+x2)",
        "zero_iff": "x1=x2=y, -d<=y<=0, x0>=d",
        "exact_real_linear_arithmetic_counterexample_query": "unsat",
        "negative_y_embedded_P3_flags": negative_y_flags,
        "y_zero_finite_k_charts": y_zero_charts,
        "matches_existing_half_centre_diagonal_atlas": True,
        "source_scope": "exact s=0 diagonal-DVR arcs only",
        "non_diagonal_or_arbitrary_source_arcs_closed": False,
    }


def half_centre_audit() -> dict[str, Any]:
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    half = sp.Rational(1, 2)
    zero_edge = (
        (e, ell),
        (e, add(cap_c, scale(half, ell))),
        (e, add(cap_c, scale(-half, ell))),
        (e, em),
    )
    require(tensor_support(zero_edge) == {}, "half-centre edge tensor")
    profile = pair_profile(zero_edge)
    require(profile == (3, 3, 2, 3, 3, 3), "half-centre edge pair profile")
    kernel_03 = pair_matrix(zero_edge[0], zero_edge[3]).nullspace()
    require(
        kernel_03 == [sp.Matrix((1, 0, 0, 0)), sp.Matrix((0, 0, 0, 1))],
        "half-centre pair-03 kernel",
    )

    p = sp.Symbol("p")
    delta = 2 * p + 1
    scaled_intrinsic_plucker = (
        p * (p + 1),
        -p * (p + 1),
        0,
        delta**2,
        -delta,
        delta,
    )
    intrinsic_limit = tuple(
        sp.factor(sp.sympify(value).subs(p, -half))
        for value in scaled_intrinsic_plucker
    )
    require(
        proportional(intrinsic_limit, wedge(*zero_edge[0])),
        "straight intrinsic plane limit",
    )

    k = sp.Symbol("k")
    finite_k = (
        (ell, add(cap_c, scale(-k, e))),
        (e, add(cap_c, scale(half, ell))),
        (e, add(cap_c, scale(-half, ell))),
        (em, e),
    )
    require(tensor_support(finite_k) == {"1111": half}, "finite-k tensor")
    require(
        all(
            pair_profile(
                tuple(
                    tuple(
                        tuple(sp.sympify(value).subs(k, sample) for value in row)
                        for row in plane
                    )
                    for plane in finite_k
                )
            )
            == (4, 4, 3, 3, 3, 3)
            for sample in (0, 1)
        ),
        "finite-k pair profile",
    )
    require(
        wedge(*finite_k[0]) == (k, -k, 0, 0, 1, -1),
        "finite-k mode-zero Pluecker vector",
    )

    tau = sp.Symbol("tau", nonzero=True)
    component15_arc = (
        (e, ell),
        (e, add(scale(tau, em), cap_c, scale(half, ell))),
        (
            add(e, scale(tau, ell)),
            add(scale(tau, em), scale(-1, cap_c), scale(half, ell)),
        ),
        (e, em),
    )
    require(
        tensor_support(component15_arc) == {"1100": -2 * tau}, "component-15 arc tensor"
    )
    arc_profile = pair_profile(component15_arc)
    require(arc_profile == (3, 4, 2, 4, 3, 4), "component-15 arc profile")
    arc_kernel_03 = pair_matrix(component15_arc[0], component15_arc[3]).nullspace()
    require(
        arc_kernel_03 == [sp.Matrix((1, 0, 0, 0)), sp.Matrix((0, 0, 0, 1))],
        "component-15 arc pair-03 kernel",
    )
    for plane, target in zip(component15_arc, zero_edge, strict=True):
        limit = tuple(sp.factor(value.subs(tau, 0)) for value in wedge(*plane))
        require(proportional(limit, wedge(*target)), "component-15 arc plane limit")

    theorem_text = " ".join(SUPPORT_ONE_REPORT.read_text(encoding="utf-8").split())
    require(
        "nonzero pure `P_4` restriction" in theorem_text,
        "support-one nonzero hypothesis",
    )
    require("exact rank-two pair" in theorem_text, "support-one rank-two hypothesis")
    require("support-one zero product" in theorem_text, "support-one kernel hypothesis")
    require("component fifteen" in theorem_text, "support-one conclusion")
    diagonal = diagonal_s_zero_audit()
    return {
        "intersection_of_intrinsic_and_p_plus_q_walls": "(p,q)=(-1/2,1/2)",
        "straight_fixed_source_U0": "span(e,A-B)",
        "restricted_tensor_support": {},
        "pair_profile": list(profile),
        "rank_two_pair_03_kernel": ["e tensor e", "(A-B) tensor (A+B)"],
        "finite_k_tensor_support": {"1111": "1/2"},
        "finite_k_pair_profile": [4, 4, 3, 3, 3, 3],
        "k_infinity_plucker_limit": [1, -1, 0, 0, 0, 0],
        "zero_restriction_k_infinity_edge": True,
        "ordinary_nonzero_P4_fibre": False,
        "component15_arc": {
            "pure_support": {"1100": "-2*tau"},
            "pair_profile": list(arc_profile),
            "exact_rank_two_pair": "03",
            "kernel": ["e tensor e", "(A-B) tensor (A+B)"],
            "all_plane_limits_match_zero_edge": True,
            "support_one_secant_theorem_hypotheses_met": True,
            "component15_closure_placement": "VERIFIED",
        },
        "diagonal_s_zero_atlas_audit": diagonal,
        "new_H31_or_H22_claim_at_zero_edge": False,
    }


def run_json_script(
    path: Path, dependencies: tuple[str, ...], timeout: int
) -> dict[str, Any]:
    command = ["uv", "run"]
    for dependency in dependencies:
        command.extend(("--with", dependency))
    command.extend(("python", path.name))
    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creation_flags,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        if os.name == "nt":
            subprocess.run(
                ("taskkill", "/PID", str(process.pid), "/T", "/F"),
                capture_output=True,
                check=False,
                timeout=15,
            )
        else:
            process.kill()
        process.communicate()
        raise AssertionError(f"bounded replay timed out: {path.name}") from exc
    require(
        process.returncode == 0,
        f"replay failed: {path.name}: {stderr[-2000:]}",
    )
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"non-JSON replay: {path.name}: {stdout[-2000:]}") from exc
    require(isinstance(payload, dict), f"non-object replay: {path.name}")
    return payload


def polynomial(text: str) -> sp.Expr:
    symbols = {str(item): item for item in sp.symbols("h0:4")}
    symbols.update({str(item): item for item in sp.symbols("rho lam")})
    return sp.expand(
        sp.sympify(text.replace("lambda", "lam").replace("^", "**"), locals=symbols)
    )


def artifact_audit(
    graph: dict[str, Any],
    incidence: dict[str, Any],
    half: dict[str, Any],
) -> dict[str, Any]:
    candidate = json.loads(CANDIDATE_CERTIFICATE.read_text(encoding="utf-8"))
    require(candidate["claim_label"] == "VERIFIED", "verified candidate label")
    require(
        candidate["discovery_claim_label"] == "CANDIDATE",
        "candidate discovery label",
    )
    require(candidate["independent_verifier_complete"] is True, "verification marker")
    require(candidate["git_commit"] == FROZEN_COMMIT, "candidate frozen commit")
    require(
        candidate["p0_and_p_minus1"]["compactified_tensor_direction_fibre"]
        == "full P1 at each base point",
        "candidate P1 claim",
    )
    require(
        candidate["p0_and_p_minus1"]["nonzero_P4_fibres"] is False,
        "candidate zero-restriction scope",
    )
    candidate_h31 = candidate["p0_and_p_minus1"]["H31"]
    candidate_h22 = candidate["p0_and_p_minus1"]["weighted_H22"]
    require(candidate_h31["projection_count"] == 16, "candidate H31 count")
    require(
        candidate_h22["complete_shared_projection_count"] == 16,
        "candidate shared-H22 count",
    )
    require("never inverted" in candidate_h31["rho_handling"], "candidate rho scope")

    charts = [chart for point in incidence.values() for chart in point.values()]
    independent_survivors = [
        item
        for chart in charts
        for item in chart["individual_H22"]
        if not item["unit_ideal"]
    ]
    candidate_survivors = candidate_h22["individual_survivors"]
    require(
        len(independent_survivors) == len(candidate_survivors) == 2, "survivor count"
    )
    survivor_pairs = (
        (
            "p0_q1_finite_finite_D01_individual",
            "p=0,q=1; finite Segre chart; finite D01 weight",
        ),
        (
            "pm1_q0_finite_finite_D01_individual",
            "p=-1,q=0; finite Segre chart; finite D01 weight",
        ),
    )
    for independent_label, candidate_label in survivor_pairs:
        independent = next(
            item for item in independent_survivors if item["label"] == independent_label
        )
        candidate_basis = candidate_survivors[candidate_label]
        require(
            len(independent["projected_standard_basis"]) == len(candidate_basis) == 3,
            "survivor basis length",
        )
        require(
            {polynomial(item) for item in independent["projected_standard_basis"]}
            == {polynomial(item) for item in candidate_basis},
            "survivor ideal mismatch",
        )

    require(
        candidate["p_minus_one_half"]["pair_profile"] == half["pair_profile"],
        "candidate half-centre profile",
    )
    require(
        candidate["p_minus_one_half"]["component15_arc"]["pure_support"]
        == {"1100": "-2*tau"},
        "candidate component-15 arc",
    )
    candidate_text = " ".join(
        CANDIDATE_REPORT.read_text(encoding="utf-8").split()
    )
    for marker in (
        "compactified Segre incidence over a zero restriction",
        "does not turn either base tuple into an actual nonzero-`P4` fibre",
        "finite-`k` or `k=0` nonzero-`P4` half-centre charts",
        "Mixed source-torus limits",
        "global Krenn--Gu conjecture remain outside scope",
    ):
        require(marker in candidate_text, f"candidate scope marker: {marker}")
    source_lines = SCRIPT.read_text(encoding="utf-8").splitlines()
    require(
        not any(
            line.strip().startswith(
                (f"import {CANDIDATE_SCRIPT.stem}", f"from {CANDIDATE_SCRIPT.stem}")
            )
            for line in source_lines
        ),
        "candidate implementation imported",
    )

    candidate_replay = run_json_script(CANDIDATE_SCRIPT, ("sympy",), 600)
    require(candidate_replay["status"] == "pass", "candidate replay")
    require(candidate_replay["claim_label"] == "VERIFIED", "candidate self-label")
    require(
        candidate_replay["discovery_claim_label"] == "CANDIDATE",
        "candidate replay discovery label",
    )
    proof_b_replay = run_json_script(PROOF_B_SCRIPT, ("sympy",), 180)
    require(proof_b_replay["status"] == "pass", "proof-B replay")
    require(proof_b_replay["claim_label"] == "VERIFIED", "proof-B self-label")
    require(
        proof_b_replay["discovery_claim_label"] == "DERIVED",
        "proof-B discovery label",
    )
    require(proof_b_replay["H31_or_H22_claim_made"] is False, "proof-B H31/H22 scope")
    require(
        proof_b_replay["half_centre_geometry"]["E_zero_iff"]
        == half["diagonal_s_zero_atlas_audit"]["zero_iff"],
        "proof-B diagonal cone",
    )
    proof_b_text = " ".join(PROOF_B_REPORT.read_text(encoding="utf-8").split())
    for marker in (
        "VERIFIED after an independent no-import reconstruction",
        "No `H31` or `H22` conclusion",
        "no arbitrary or non-diagonal source arcs",
        "no complete source-torus atlas at p=0 or p=-1",
    ):
        require(marker in proof_b_text, f"proof-B scope marker: {marker}")

    return {
        "candidate_script_imported": False,
        "candidate_replay_status": candidate_replay["status"],
        "candidate_claims_match_independent_reconstruction": True,
        "candidate_certificate_json_valid": True,
        "candidate_scope_preserves_zero_restriction_distinction": True,
        "proof_B_replay_status": proof_b_replay["status"],
        "proof_B_original_label": "DERIVED",
        "proof_B_geometry_independently_verified": True,
        "proof_B_H31_or_H22_claim": False,
        "proof_B_source_arc_limitations_preserved": True,
        "graph_equation_matches": graph["graph_equation"] == "(p-q+1)*b+q*(q-1)*a",
    }


def main() -> None:
    graph = graph_closure_audit()
    bases = base_plane_audit()
    incidence = audit_incidence()
    half = half_centre_audit()
    artifacts = artifact_audit(graph, incidence, half)
    all_segre = [chart for point in incidence.values() for chart in point.values()]
    individual = [item for chart in all_segre for item in chart["individual_H22"]]
    survivors = [item for item in individual if not item["unit_ideal"]]
    h31_count = sum(len(chart["H31"]) for chart in all_segre)
    shared_count = sum(len(chart["shared_H22"]) for chart in all_segre)
    require(h31_count == 16, "H31 projection count")
    require(shared_count == 16, "shared H22 projection count")
    require(len(individual) == 16 and len(survivors) == 2, "individual H22 count")
    input_paths = (
        CANDIDATE_REPORT,
        CANDIDATE_SCRIPT,
        CANDIDATE_CERTIFICATE,
        PROOF_B_REPORT,
        PROOF_B_SCRIPT,
        COMPONENT_REPORT,
        WALL_GEOMETRY_REPORT,
        WALL_H22_REPORT,
        SUPPORT_ONE_REPORT,
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "verifier",
                "date_utc": datetime.now(UTC)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "git_commit": git_commit(),
                "frozen_commit": FROZEN_COMMIT,
                "claim_label": "VERIFIED",
                "scope": (
                    "compactified Segre-direction marked-H31 and weighted-H22 "
                    "incidence over component-20 zero restrictions (p,q)=(0,1),"
                    "(-1,0), plus structural audit of the straight fixed-source "
                    "zero edge at (-1/2,1/2)"
                ),
                "inputs": {path.name: sha256(path) for path in input_paths},
                "method": (
                    "no-import plane/permanent reconstruction, transverse graph "
                    "calculation, exact polynomial-rho/lambda elimination with "
                    "inverse saturation, half-centre pair/arc audit, and exact "
                    "real-linear valuation-cone refutation query"
                ),
                "command": (
                    "uv run --with sympy --with z3-solver python " + SCRIPT.name
                ),
                "outputs": {
                    SCRIPT.name: sha256(SCRIPT),
                    REPORT.name: sha256(REPORT) if REPORT.exists() else "pending",
                },
                "graph_closure": graph,
                "zero_tensor_base_points": bases,
                "incidence": incidence,
                "counts": {
                    "H31_unit_projections": h31_count,
                    "individual_H22_projections": len(individual),
                    "individual_H22_survivor_projections": len(survivors),
                    "individual_H22_unit_projections": len(individual) - len(survivors),
                    "shared_H22_unit_projections": shared_count,
                },
                "individual_H22_survivor_ideals": survivors,
                "half_centre": half,
                "artifact_audit": artifacts,
                "finite_segre_rho_retained_polynomially_over_Q": True,
                "finite_weight_lambda_retained_polynomially_over_Q": True,
                "finite_weight_includes_lambda_zero": True,
                "direct_segre_and_weight_infinity_endpoints_checked": True,
                "both_shared_alpha_orientations_checked": True,
                "normalization_saturation_gap": False,
                "proof_B_geometry_claim_label_after_independent_audit": "VERIFIED",
                "proof_B_H31_or_H22_claim_promoted": False,
                "component15_placement_claim_label": "VERIFIED",
                "p_minus_one_half_new_H31_or_H22_claim": False,
                "finite_field_inference_used": False,
                "broad_search_used": False,
                "global_Krenn_Gu_resolved": False,
                "limitations": (
                    "the P1 fibres are compactified tensor-direction fibres over "
                    "zero restrictions, not ordinary nonzero-P4 fibres; the half "
                    "point audit covers the straight fixed-source zero edge and "
                    "exact s=0 diagonal-DVR arcs only; mixed/non-diagonal source "
                    "arcs, complete p=0,-1 source-torus atlases, component parameter "
                    "infinity, arbitrary GL4 degenerations, component exhaustiveness, "
                    "arbitrary-order reduction, prize graph, and global conjecture "
                    "remain outside scope"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
