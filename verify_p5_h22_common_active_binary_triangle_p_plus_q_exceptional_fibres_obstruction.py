#!/usr/bin/env python3
"""Build the verified weighted-H22 obstruction on exceptional p+q fibres."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

from audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial import (
    MIXED_WORDS,
    WORDS,
    chart_planes,
    contract,
    marked_matrix,
    permanent3,
    permanent4,
    reconstruct_model,
)

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_OBSTRUCTION.md"
)
P4_BOUNDARY = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H31_EXCEPTIONAL = (
    ROOT
    / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md"
)
H22_PARTIAL = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
INDEPENDENT_AUDIT = (
    ROOT
    / "audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_independent.py"
)


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
    ).stdout.strip()


def add(left, right):
    return tuple(sp.expand(a + b) for a, b in zip(left, right))


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def shift(alpha, beta, marking):
    return tuple(add(beta[i], scale(marking[i], alpha[i])) for i in range(4))


def wedge(left, right):
    return tuple(
        sp.factor(left[i] * right[j] - left[j] * right[i])
        for i, j in itertools.combinations(range(4), 2)
    )


def lower_bases(x, y, gamma=None):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    w = add(scale(x, ell), scale(y, em))
    alpha = (e, em, e, add(cap_c, scale(-1, w)))
    beta = (ell, e, add(cap_c, w), ell if gamma is None else add(ell, scale(gamma, e)))
    return alpha, beta


def pure_coefficients(alpha, beta):
    return {
        word: sp.factor(
            permanent4(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        )
        for word in WORDS
    }


def lower_model(alpha, beta, direction, slope, marking):
    beta = shift(alpha, beta, marking)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_rows = tuple(
        contract(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    mixed = sp.Matrix(
        [
            [coefficients[word].coeff(variable) for variable in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "extensions": extensions,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "diagonal_alpha": coefficients[WORDS[0]],
        "diagonal_beta": coefficients[WORDS[-1]],
    }


def geometry_certificate():
    x, y, gamma, lam = sp.symbols("x y gamma lambda", nonzero=True)
    direct = {}
    for a in (0, -1):
        direct[a] = {}
        for chart in ("B_full", "B_drop"):
            alpha, beta = chart_planes(chart, sp.Integer(a), lam, (0, 0, 0, 0))
            coefficients = pure_coefficients(alpha, beta)
            expected = (-2 * lam if chart == "B_full" else -2) * (1 if a == 0 else -1)
            assert sp.factor(coefficients[WORDS[-1]] - expected) == 0
            assert all(
                value == 0 for word, value in coefficients.items() if word != WORDS[-1]
            )
            direct[a][chart] = str(expected)
    lower = {}
    for name, parameter in (("baseline", None), ("wall", gamma)):
        alpha, beta = lower_bases(x, y, parameter)
        coefficients = pure_coefficients(alpha, beta)
        assert coefficients[WORDS[-1]] == -2
        assert all(
            value == 0 for word, value in coefficients.items() if word != WORDS[-1]
        )
        lower[name] = "-2"
    baseline_alpha, baseline_beta = lower_bases(x, y)
    wall_alpha, wall_beta = lower_bases(x, y, gamma)
    assert wedge(baseline_beta[3], baseline_alpha[3]) == (0, 0, 0, -2 * y, 1, -1)
    assert wedge(wall_beta[3], wall_alpha[3]) == (
        -gamma * (x + y),
        gamma * (x - y),
        gamma,
        -2 * y,
        1,
        -1,
    )
    return {
        "direct_sole_pure_coefficients": direct,
        "lower_sole_pure_coefficients": lower,
        "baseline_mode_zero_pluecker": ["0", "0", "0", "-2*y", "1", "-1"],
        "wall_mode_zero_pluecker": [
            "-gamma*(x+y)",
            "gamma*(x-y)",
            "gamma",
            "-2*y",
            "1",
            "-1",
        ],
        "a_minus_one_symmetry": "swap lower modes and apply e -> -e",
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(value):
    return str(sp.cancel(value)).replace("**", "^")


def projection_certificate(
    label, model, expected, extra_parameters=(), inversions=(), finite=False
):
    extensions = model["extensions"]
    mixed = model["mixed"]
    diagonal_a = model["diagonal_alpha"]
    diagonal_b = model["diagonal_beta"]
    inverse = sp.Symbol("winv")
    equations = [
        *tuple(mixed * sp.Matrix(extensions)),
        diagonal_a - 1,
        inverse * diagonal_b - 1,
    ]
    eliminated = extensions + (inverse,)
    if finite:
        slope = sp.Symbol("r")
        eliminated += (slope,)
    for parameter, inverse_name in inversions:
        parameter_inverse = sp.Symbol(inverse_name)
        equations.append(parameter_inverse * parameter - 1)
        eliminated += (parameter_inverse,)
    markings = sp.symbols("h0:4")
    variables = eliminated + markings + tuple(extra_parameters)
    blocks = f"(dp({len(eliminated)}),dp(4)"
    if extra_parameters:
        blocks += f",dp({len(extra_parameters)})"
    blocks += ")"
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + ")," + blocks + ";",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal L=simplify(reduce(J,E),2);",
            "ideal RJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(L)==0)&&(size(RJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label,
        completed.stdout,
    )
    return {
        "label": label,
        "projected_ideal": [singular(value) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
        "normalization": "A=1, winv*B=1",
    }


def projection_certificates():
    h0, h1, h2, h3 = sp.symbols("h0:4")
    lam, slope = sp.symbols("lambda r")
    results = []
    for a in (0, -1):
        expected = (h3, h2, h0) if a == 0 else (h3, h1, h0)
        marking = (h0, h1, h2, h3)
        for chart in ("B_full", "B_drop"):
            for direction in ("D01_finite", "D01_infinity"):
                model = reconstruct_model(
                    chart, direction, sp.Integer(a), lam, slope, marking
                )
                parameters = (lam,) if chart == "B_full" else ()
                inversions = ((lam, "linv"),) if chart == "B_full" else ()
                results.append(
                    projection_certificate(
                        f"a={a}:{chart}:{direction}",
                        model,
                        expected,
                        parameters,
                        inversions,
                        direction.endswith("finite"),
                    )
                )
    x, y, gamma = sp.symbols("x y gamma")
    marking = (h0, h1, h2, h3)
    lower_expected = {
        ("baseline", "D01_finite"): (h3, h2, h1),
        ("baseline", "D01_infinity"): (h3, h2, h1),
        ("wall", "D01_finite"): (h3, h2, h1),
        ("wall", "D01_infinity"): (h3, h2, h1, h0),
    }
    for family in ("baseline", "wall"):
        alpha, beta = lower_bases(x, y, None if family == "baseline" else gamma)
        for direction in ("D01_finite", "D01_infinity"):
            model = lower_model(alpha, beta, direction, slope, marking)
            parameters = (x, y) if family == "baseline" else (x, y, gamma)
            inversions = () if family == "baseline" else ((gamma, "ginv"),)
            results.append(
                projection_certificate(
                    f"lower:{family}:{direction}",
                    model,
                    lower_expected[(family, direction)],
                    parameters,
                    inversions,
                    direction.endswith("finite"),
                )
            )
    return results


def rank_witness(mixed):
    rank = mixed.rank()
    columns = mixed.rref()[1][:rank]
    rows = mixed.T.rref()[1][:rank]
    determinant = sp.factor(mixed.extract(rows, columns).det())
    assert determinant != 0
    return list(rows), list(columns), determinant


def kernel_certificate(
    label, model, rank, marked_mode, rows, expected_a, expected_b, expected_minor
):
    mixed = model["mixed"]
    assert mixed.rank() == rank, (label, mixed.rank())
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - rank
    frame = sp.Matrix.hstack(*kernel)
    assert frame.rank() == len(kernel)
    coefficients = sp.symbols(f"X0:{len(kernel)}")
    extension = frame * sp.Matrix(coefficients)
    substitution = dict(zip(model["extensions"], extension))
    actual_a = sp.factor(model["diagonal_alpha"].subs(substitution))
    actual_b = sp.factor(model["diagonal_beta"].subs(substitution))
    minor = sp.factor(
        marked_matrix(model, marked_mode)
        .subs(substitution)
        .extract(rows, range(4))
        .det()
    )
    assert sp.factor(actual_a - expected_a(*coefficients)) == 0, (label, actual_a)
    assert sp.factor(actual_b - expected_b(*coefficients)) == 0, (label, actual_b)
    assert sp.factor(minor - expected_minor(*coefficients)) == 0, (label, minor)
    witness_rows, witness_columns, witness = rank_witness(mixed)
    return {
        "label": label,
        "mixed_rank": rank,
        "kernel_dimension": len(kernel),
        "complete_kernel_frame": [
            [str(sp.factor(value)) for value in vector] for vector in kernel
        ],
        "rank_witness_rows": witness_rows,
        "rank_witness_columns": witness_columns,
        "rank_witness": str(witness),
        "A": str(actual_a),
        "B": str(actual_b),
        "marked_mode": marked_mode,
        "minor_rows": list(rows),
        "minor": str(minor),
        "genuine_open_forces_minor_nonzero": True,
    }


def no_genuine(label, model, diagonal, expected_rank):
    mixed = model["mixed"]
    assert mixed.rank() == expected_rank, (label, mixed.rank())
    kernel = mixed.nullspace()
    expression = model["diagonal_alpha"] if diagonal == "A" else model["diagonal_beta"]
    assert all(
        sp.factor(expression.subs(dict(zip(model["extensions"], vector)))) == 0
        for vector in kernel
    )
    return {
        "label": label,
        "mixed_rank": expected_rank,
        "kernel_dimension": len(kernel),
        f"{diagonal}_on_complete_kernel": "zero",
        "genuine_binary_neighbour_exists": False,
    }


def direct_kernel_certificates():
    lam, r, t = sp.symbols("lambda r t", nonzero=True)
    results = []
    specifications = [
        (
            0,
            "B_full",
            "D01_finite",
            (0, t, 0, 0),
            6,
            (0, 2, 4, 7),
            lambda X, Y: -2 * Y * r,
            lambda X, Y: -2 * (lam + r) * (X * r + Y * (r * t + 1)),
            lambda X, Y: -8 * Y**2 * lam * r**2 * (lam + r) * (X * r + Y * (r * t + 1)),
        ),
        (
            0,
            "B_full",
            "D01_infinity",
            (0, t, 0, 0),
            6,
            (0, 2, 4, 7),
            lambda X, Y: -2 * Y,
            lambda X, Y: -2 * (X * lam + Y),
            lambda X, Y: -8 * Y**2 * lam * (X * lam + Y),
        ),
        (
            0,
            "B_drop",
            "D01_finite",
            (0, t, 0, 0),
            6,
            (0, 2, 4, 7),
            lambda X, Y: -2 * Y * r,
            lambda X, Y: -2 * (X * r + Y * (r * t + 1)),
            lambda X, Y: -8 * Y**2 * r**2 * (X * r + Y * (r * t + 1)),
        ),
        (
            0,
            "B_drop",
            "D01_infinity",
            (0, t, 0, 0),
            5,
            (0, 2, 4, 7),
            lambda X, Y, Z: -2 * Z,
            lambda X, Y, Z: -2 * X,
            lambda X, Y, Z: -8 * X * Z**2,
        ),
        (
            -1,
            "B_full",
            "D01_finite",
            (0, 0, t, 0),
            6,
            (0, 1, 4, 7),
            lambda X, Y: 2 * Y * r,
            lambda X, Y: -2 * (X * lam * r - Y * (lam + r)),
            lambda X, Y: 8 * Y**2 * lam * r**2 * (X * lam * r - Y * (lam + r)),
        ),
        (
            -1,
            "B_full",
            "D01_infinity",
            (0, 0, t, 0),
            6,
            (0, 1, 4, 7),
            lambda X, Y: 2 * Y,
            lambda X, Y: -2 * (X * lam - Y),
            lambda X, Y: 8 * Y**2 * lam * (X * lam - Y),
        ),
        (
            -1,
            "B_drop",
            "D01_finite",
            (0, 0, t, 0),
            6,
            (0, 1, 4, 7),
            lambda X, Y: 2 * Y * r,
            lambda X, Y: -2 * (X * r - Y),
            lambda X, Y: 8 * Y**2 * r**2 * (X * r - Y),
        ),
        (
            -1,
            "B_drop",
            "D01_infinity",
            (0, 0, t, 0),
            5,
            (0, 1, 4, 7),
            lambda X, Y, Z: 2 * Z,
            lambda X, Y, Z: -2 * Y,
            lambda X, Y, Z: 8 * Y * Z**2,
        ),
    ]
    for a, chart, direction, marking, rank, rows, ea, eb, em in specifications:
        model = reconstruct_model(chart, direction, sp.Integer(a), lam, r, marking)
        results.append(
            kernel_certificate(
                f"a={a}:{chart}:{direction}",
                model,
                rank,
                3,
                rows,
                ea,
                eb,
                em,
            )
        )
    # Every direct finite-slope branch has A=0 at r=0.
    for a in (0, -1):
        marking = (0, t, 0, 0) if a == 0 else (0, 0, t, 0)
        for chart in ("B_full", "B_drop"):
            model = reconstruct_model(
                chart, "D01_finite", sp.Integer(a), lam, sp.Integer(0), marking
            )
            results.append(no_genuine(f"a={a}:{chart}:r=0", model, "A", 1))
    # The only singular generic frame, lambda+r=0 at a=-1,B_full.
    model = reconstruct_model(
        "B_full", "D01_finite", sp.Integer(-1), lam, -lam, (0, 0, t, 0)
    )
    results.append(no_genuine("a=-1:B_full:r=-lambda", model, "B", 6))
    return results


def lower_kernel_certificates():
    x, y, gamma, r, t = sp.symbols("x y gamma r t", nonzero=True)
    baseline_alpha, baseline_beta = lower_bases(x, y)
    wall_alpha, wall_beta = lower_bases(x, y, gamma)
    results = []
    model = lower_model(baseline_alpha, baseline_beta, "D01_finite", r, (t, 0, 0, 0))
    results.append(
        kernel_certificate(
            "lower:baseline:finite",
            model,
            6,
            1,
            (0, 1, 3, 7),
            lambda X, Y: -2 * X * r,
            lambda X, Y: -2 * X * (r * t + 1),
            lambda X, Y: 8 * X**3 * r**2 * (r * t + 1),
        )
    )
    model = lower_model(baseline_alpha, baseline_beta, "D01_infinity", r, (t, 0, 0, 0))
    results.append(
        kernel_certificate(
            "lower:baseline:infinity",
            model,
            5,
            1,
            (0, 1, 3, 7),
            lambda X, Y, Z: -2 * X,
            lambda X, Y, Z: -2 * (X * t + Z),
            lambda X, Y, Z: 8 * X**2 * (X * t + Z),
        )
    )
    model = lower_model(wall_alpha, wall_beta, "D01_finite", r, (t, 0, 0, 0))
    results.append(
        kernel_certificate(
            "lower:wall:finite:generic",
            model,
            6,
            1,
            (0, 1, 3, 7),
            lambda X, Y: -2 * Y * r / (gamma * (r * t + 1)),
            lambda X, Y: -2 * Y * (gamma * r + 1) / gamma,
            lambda X, Y: (
                8 * Y**3 * r**2 * (gamma * r + 1) / (gamma**3 * (r * t + 1) ** 2)
            ),
        )
    )
    model = lower_model(wall_alpha, wall_beta, "D01_infinity", r, (0, 0, 0, 0))
    results.append(
        kernel_certificate(
            "lower:wall:infinity",
            model,
            5,
            1,
            (0, 1, 3, 7),
            lambda X, Y, Z: -2 * X,
            lambda X, Y, Z: -2 * Z,
            lambda X, Y, Z: 8 * X**2 * Z,
        )
    )
    # Singular finite wall parameters are direct no-neighbour fibres.
    model = lower_model(
        wall_alpha, wall_beta, "D01_finite", sp.Integer(0), (t, 0, 0, 0)
    )
    results.append(no_genuine("lower:wall:r=0", model, "A", 1))
    model = lower_model(wall_alpha, wall_beta, "D01_finite", r, (-1 / r, 0, 0, 0))
    results.append(no_genuine("lower:wall:r*t+1=0", model, "B", 6))
    return results


def main():
    geometry = geometry_certificate()
    projections = projection_certificates()
    direct = direct_kernel_certificates()
    lower = lower_kernel_certificates()
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "proof_b",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "claim_label": "VERIFIED",
                "scope": "direct weighted-H22 obstruction on all a=0,-1 p+q exceptional finite fibres",
                "inputs": {
                    P4_BOUNDARY.name: sha256(P4_BOUNDARY),
                    H31_EXCEPTIONAL.name: sha256(H31_EXCEPTIONAL),
                    H22_PARTIAL.name: sha256(H22_PARTIAL),
                    INDEPENDENT_AUDIT.name: sha256(INDEPENDENT_AUDIT),
                },
                "method": "exact direct orientations, saturated D01 projections, complete symbolic kernels, and fixed marked minors",
                "command": "uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py",
                "outputs": {THEOREM.name: sha256(THEOREM)},
                "limitations": "verified diagonal-DVR a=0,-1 H22 fibres only; no other centres, non-diagonal closure, gluing, or global claim",
                "geometry": geometry,
                "projection_certificates": projections,
                "direct_chart_certificates": direct,
                "lower_pair_certificates": lower,
                "finite_field_computation_used": False,
                "broad_minor_scan_used": False,
                "generic_1_over_a_formulas_used": False,
                "generic_1_over_a_plus_1_formulas_used": False,
                "exceptional_a0_a_minus1_weighted_H22_empty": "VERIFIED",
                "fresh_independent_verifier_complete": True,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
