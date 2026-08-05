#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the triangle component.

Exact characteristic-zero verifier for
P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md: the two
weighted diagonal pencils D_01^r, D_23^r on the ninth (all-rank-one
triangle) pure-P_4 component, marked bases beta_i(t)=beta_i+t_i*alpha_i
over C(p,q,r), exact Singular marking projections with bidirectional
ideal equality, unique-kernel sheet structure, and per-sheet ternary
Fitting certificates with the line-sheet parameter kept polynomial.

Fail-closed: every Singular run is wrapped in a hard timeout; a timed
out or failed run is recorded as null in the ledger and the verifier
raises instead of claiming the step.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md"
COMPONENT_PRIMARY = (
    ROOT / "verify_p4_all_rank_one_triangle_pure_component.py"
)
H31_THEOREM = (
    ROOT
    / "P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    word for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR_TIMEOUT = 550

P, Q, R = sp.symbols("p q r")
S = sp.Symbol("s")

T0_STAR = -(Q + 1) / (P * Q + P + 1)

EXPECTED_PROJECTIONS = {
    "01": ("t1", "t2", "t3"),
    "23": ("t1", "t2", "((p*q+p+1)*t0+(q+1))*t3"),
}

# sheet name -> (diagonal, marking, killing mode, minor row sets)
SHEETS = {
    "d01_t0_line": ("01", (S, 0, 0, 0), 1, ((0, 2, 3, 7),)),
    "d23_t0_line": ("23", (S, 0, 0, 0), 1, ((0, 2, 3, 7),)),
    "d23_t3_line": (
        "23",
        (T0_STAR, 0, 0, S),
        3,
        ((0, 2, 3, 7), (0, 2, 6, 7)),
    ),
}

W_T3 = (
    P * Q * R * S + P * Q * R + P * Q * S + P * R + R * S + R + S
)
G_T3 = (
    P * Q * R**2 * S + P * Q * R**2 - P * Q * S + P * R**2
    + R**2 * S + R**2 - R - S
)

DISPLAYED_Z = {
    "d01_t0_line": (
        P * R + 1,
        P * R + 1,
        0,
        0,
        S * (P * R - 1),
        0,
        P * R - 1,
        0,
    ),
    "d23_t0_line": (
        -(R + 1) * (P * Q + 1),
        0,
        0,
        -(R + 1),
        (1 - R) * (P * Q * S + Q + S),
        R - 1,
        0,
        0,
    ),
    "d23_t3_line": (
        (R + 1) * (P * Q + 1) * (P * Q + P + 1)
        * (P * Q * R * S + P * Q * R + P * R + P * S + R * S + R),
        0,
        -S * (R + 1) * (P * Q + 1) * (P * Q + P + 1),
        (R + 1) * (P * Q + P + 1) * W_T3,
        -(R - 1) * W_T3,
        -(R - 1) * (P * Q + P + 1) * W_T3,
        0,
        S * (R + 1) * (P * Q + P + 1) * (W_T3 + P * Q + 1),
    ),
}

EXPECTED_DIAGONALS = {
    "d01_t0_line": (
        -2 * (P * R + 1),
        -2 * (R + S) * (P * R - 1),
    ),
    "d23_t0_line": (
        -2 * (R + 1) * (P * Q + 1),
        2 * (R - 1) * (P * Q * S + Q + R + S),
    ),
    "d23_t3_line": (
        2 * R * (R + 1) * (P * Q + 1) * (P * Q + P + 1) ** 2,
        -2 * (R - 1) * (P * Q + P + 1) * G_T3,
    ),
}

# rank-seven pivot witnesses (rows, columns, factored determinant)
SHEET_PIVOTS = {
    "d01_t0_line": (
        (0, 1, 3, 4, 5, 6, 7),
        (0, 1, 2, 3, 4, 5, 7),
        4 * R * (P * Q + 1) ** 2 * (P * R - 1) ** 3
        * (P * R + 1) ** 2 * (P * Q - P + 1) * (P * Q + P + 1)
        * (P * Q * R + R + 1),
    ),
    "d23_t0_line": (
        (0, 1, 2, 3, 4, 6, 7),
        (0, 1, 2, 3, 4, 6, 7),
        4 * P * R * (R - 1) ** 3 * (R + 1) ** 2
        * (P * Q + P + 1) * (P * Q + P * R + 1),
    ),
    "d23_t3_line": (
        (0, 1, 2, 3, 4, 6, 7),
        (0, 1, 2, 3, 4, 6, 7),
        4 * P * (R - 1) ** 3 * (R + 1) ** 2
        * (P * Q + P * R + 1) * W_T3,
    ),
}

# identity replays on the displayed kernel representative:
# multiplier * det P_mode[rows] == factor * B(z)
KERNEL_IDENTITIES = {
    "d01_t0_line": (
        (0, 2, 3, 7),
        1,
        -4 * P * R * (P * Q + 1) * (P * R - 1) ** 2,
    ),
    "d23_t0_line": (
        (0, 2, 3, 7),
        R - 1,
        4 * (R + 1) ** 3 * (P * Q + 1) ** 2
        * (P * Q + P * R + 1),
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def singular_command(timeout: float) -> tuple[str, ...]:
    if timeout <= 0:
        raise ValueError("Singular timeout must be positive")
    if os.name == "nt":
        return (
            "wsl.exe",
            "--exec",
            "/usr/bin/timeout",
            "--signal=KILL",
            f"{timeout:.6f}s",
            "/usr/bin/Singular",
            "-q",
        )
    return (
        "timeout",
        "--signal=KILL",
        f"{timeout:.6f}s",
        "Singular",
        "-q",
    )


def run_singular(program: str, timeout: float = SINGULAR_TIMEOUT):
    try:
        completed = subprocess.run(
            singular_command(timeout),
            input=program,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout + 10,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    if completed.returncode != 0 or completed.stderr.strip():
        return None
    return completed.stdout


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def family():
    alpha = (
        (P * Q + 1, 1, P, P * Q + 1),
        (P, 1, 0, 0),
        (1, 0, -1, 0),
        (0, 0, 1, 1),
    )
    beta = (
        (Q + 1, 0, 1, Q),
        (0, 0, 1, -1),
        (-P, 1, 0, 0),
        (1, 0, 1, 0),
    )
    return alpha, beta


def shifted_basis(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.expand(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def diagonal_row(row, extension, diagonal, slope):
    if diagonal == "01":
        return (
            slope * row[0] + row[1],
            row[2],
            row[3],
            extension,
        )
    if diagonal == "23":
        return (
            row[0],
            row[1],
            slope * row[2] + row[3],
            extension,
        )
    raise ValueError(diagonal)


def weighted_rows(diagonal, alpha, beta, extensions):
    alpha_d = tuple(
        diagonal_row(alpha[mode], extensions[mode], diagonal, R)
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(beta[mode], extensions[4 + mode], diagonal, R)
        for mode in range(4)
    )
    return alpha_d, beta_d


def weighted_coefficients(diagonal, alpha, beta, extensions):
    alpha_d, beta_d = weighted_rows(diagonal, alpha, beta, extensions)
    return {
        word: permanent(
            tuple(
                beta_d[mode] if word[mode] else alpha_d[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }


def weighted_system(diagonal, alpha, beta, extensions):
    coefficients = weighted_coefficients(
        diagonal, alpha, beta, extensions
    )
    mixed = sp.Matrix(
        [
            [
                sp.diff(coefficients[word], variable)
                for variable in extensions
            ]
            for word in MIXED_WORDS
        ]
    )
    diagonal_a = sp.Matrix(
        [
            [
                sp.diff(coefficients[(0, 0, 0, 0)], variable)
                for variable in extensions
            ]
        ]
    )
    diagonal_b = sp.Matrix(
        [
            [
                sp.diff(coefficients[(1, 1, 1, 1)], variable)
                for variable in extensions
            ]
        ]
    )
    return mixed, diagonal_a, diagonal_b


def one_marked_map(mode, alpha, beta):
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def singular_polynomial(expression) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_projection(diagonal, alpha, beta):
    extensions = sp.symbols("z0:8")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = weighted_coefficients(
        diagonal, alpha, marked_beta, extensions
    )
    equations = [coefficients[word] for word in MIXED_WORDS]
    equations.append(coefficients[(0, 0, 0, 0)] - 1)
    equations.append(
        inverse * coefficients[(1, 1, 1, 1)] - 1
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    expected = EXPECTED_PROJECTIONS[diagonal]
    lines = [
        "ring RN=(0,p,q,r),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I="
        + ",".join(map(singular_polynomial, equations))
        + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I,"
        + "*".join(map(str, eliminated))
        + ");",
        "J=std(J);",
        "ideal E=" + ",".join(expected) + ";",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        "int same=((size(JE)==0)&&(size(EJ)==0));",
        '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
        "quit;",
    ]
    stdout = run_singular("\n".join(lines))
    if stdout is None:
        return None
    results = [
        line.strip()
        for line in stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    if len(results) != 1:
        return None
    fields = results[0].split(":")
    if fields[1] != "1":
        raise AssertionError(
            ("weighted projection ideal mismatch", diagonal, stdout)
        )
    return {
        "computed_equals_expected_bidirectionally": True,
        "expected_generators": list(expected),
        "groebner_basis_size": int(fields[2]),
    }


def sheet_kernel_data(name, alpha, beta):
    diagonal, marking, mode, row_sets = SHEETS[name]
    extensions = sp.symbols("z0:8")
    marked_beta = shifted_basis(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = weighted_system(
        diagonal, alpha, marked_beta, extensions
    )
    kernel = sp.Matrix(DISPLAYED_Z[name])
    assert all(
        sp.cancel(value) == 0 for value in mixed * kernel
    ), name
    assert any(
        sp.cancel(entry) != 0 for entry in kernel
    ), name
    expected_a, expected_b = EXPECTED_DIAGONALS[name]
    diag_a = sp.factor((diagonal_a * kernel)[0])
    diag_b = sp.factor((diagonal_b * kernel)[0])
    assert sp.cancel(diag_a - expected_a) == 0, name
    assert sp.cancel(diag_b - expected_b) == 0, name
    pivot_rows, pivot_columns, pivot_value = SHEET_PIVOTS[name]
    pivot = mixed[list(pivot_rows), list(pivot_columns)].det(
        method="berkowitz"
    )
    assert sp.cancel(pivot - pivot_value) == 0, name
    return {
        "diagonal": diagonal,
        "marking": marking,
        "mode": mode,
        "row_sets": row_sets,
        "marked_beta": marked_beta,
        "kernel": kernel,
        "A": diag_a,
        "B": diag_b,
        "pivot": (pivot_rows, pivot_columns, pivot_value),
    }


def check_kernel_identity(name, data):
    if name not in KERNEL_IDENTITIES:
        return None
    rows, multiplier, factor = KERNEL_IDENTITIES[name]
    diagonal = data["diagonal"]
    marked_beta = data["marked_beta"]
    kernel = data["kernel"]
    alpha, _beta = family()
    alpha_d, beta_d = weighted_rows(
        diagonal, alpha, marked_beta, kernel
    )
    marked = one_marked_map(data["mode"], alpha_d, beta_d)
    determinant = sp.expand(
        marked[list(rows), :].det(method="berkowitz")
    )
    difference = sp.expand(
        sp.expand(multiplier * determinant)
        - sp.expand(factor * data["B"])
    )
    assert sp.cancel(difference) == 0, name
    return {
        "rows": list(rows),
        "multiplier": str(multiplier),
        "factor_times_B": str(factor),
    }


def fitting_certificate(name, data):
    diagonal = data["diagonal"]
    mode = data["mode"]
    row_sets = data["row_sets"]
    marked_beta = data["marked_beta"]
    alpha, _beta = family()
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    coefficients = weighted_coefficients(
        diagonal, alpha, marked_beta, extensions
    )
    mixed = [coefficients[word] for word in MIXED_WORDS]
    first = coefficients[(0, 0, 0, 0)]
    second = coefficients[(1, 1, 1, 1)]
    alpha_d, beta_d = weighted_rows(
        diagonal, alpha, marked_beta, extensions
    )
    marked = one_marked_map(mode, alpha_d, beta_d)
    determinants = [
        sp.expand(marked[list(rows), :].det(method="berkowitz"))
        for rows in row_sets
    ]
    equations = (
        mixed
        + determinants
        + [inverse * first * second - 1]
    )
    variables = extensions + (inverse, S)
    program = "\n".join(
        (
            "ring RN=(0,p,q,r),("
            + ",".join(map(str, variables))
            + "),dp;",
            "ideal I="
            + ",".join(map(singular_polynomial, equations))
            + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            '"CODEX_RESULT:"+string(unit)+":"+string(size(I));',
            "quit;",
        )
    )
    stdout = run_singular(program)
    if stdout is None:
        return None
    results = [
        line.strip()
        for line in stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    if results != ["CODEX_RESULT:1:1"]:
        raise AssertionError(("Fitting ideal not unit", name, stdout))
    return {
        "marked_mode": mode,
        "minor_rows": [list(rows) for rows in row_sets],
        "line_parameter_kept_polynomial": True,
        "saturated_fitting_ideal_unit": True,
    }


def main() -> None:
    alpha, beta = family()

    if COMPONENT_PRIMARY.exists():
        from verify_p4_all_rank_one_triangle_pure_component import (
            family as component_family,
        )

        planes = component_family(P, Q)
        assert all(
            tuple(plane.row(0)) == alpha[mode]
            and tuple(plane.row(1)) == beta[mode]
            for mode, plane in enumerate(planes)
        )

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == -2
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    projections = {}
    for diagonal in ("01", "23"):
        projections[diagonal] = run_projection(
            diagonal, alpha, beta
        )

    sheets = {}
    identities = {}
    certificates = {}
    for name in SHEETS:
        data = sheet_kernel_data(name, alpha, beta)
        pivot_rows, pivot_columns, pivot_value = data["pivot"]
        sheets[name] = {
            "diagonal": data["diagonal"],
            "marking": [str(entry) for entry in data["marking"]],
            "mixed_rank": 7,
            "kernel_dimension": 1,
            "rank_seven_pivot_rows": list(pivot_rows),
            "rank_seven_pivot_columns": list(pivot_columns),
            "rank_seven_pivot_determinant": str(pivot_value),
            "kernel": [str(entry) for entry in data["kernel"]],
            "A": str(data["A"]),
            "B": str(data["B"]),
        }
        identity = check_kernel_identity(name, data)
        if identity is not None:
            identities[name] = identity
        certificates[name] = fitting_certificate(name, data)

    failed = [
        diagonal
        for diagonal, value in projections.items()
        if value is None
    ] + [name for name, value in certificates.items() if value is None]
    verified = not failed

    output = {
        "verified": verified,
        "field": "C(p,q,r) (free component function field with slope)",
        "method": (
            "weighted diagonal-hyperplane pencils, exact "
            "slope-generic marked projections with bidirectional "
            "ideal equality, unique genuine kernel lines, and "
            "per-sheet ternary Fitting certificates with polynomial "
            "line-sheet parameters"
        ),
        "pure_coefficient": "-2 (word 1111 only)",
        "weighted_source_columns": {
            "01": ["r*x0+x1", "x2", "x3", "x4"],
            "23": ["x0", "x1", "r*x2+x3", "x4"],
        },
        "projections": projections,
        "marking_loci": {
            "01": "t1=t2=t3=0 (whole t0-line, slope-independent)",
            "23": (
                "t1=t2=0, ((pq+p+1)t0+(q+1))*t3=0 "
                "(t0-line union t3-line, slope-independent)"
            ),
        },
        "surviving_marking_sheets": 3,
        "sheet_kernels": sheets,
        "kernel_identities": identities,
        "fitting_certificates": certificates,
        "failed_steps_recorded_as_null": failed,
        "generic_weighted_H22_incidence_empty": verified,
        "weighted_slope_and_parameter_boundaries_closed": False,
        "known_pure_component_orbits_at_least": 13,
        "components_one_through_nine_generic_weighted_H22_excluded": (
            verified
        ),
        "components_ten_through_thirteen_H22_open": True,
        "all_pure_components_classified": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (
                COMPONENT,
                COMPONENT_PRIMARY,
                H31_THEOREM,
            )
            if path.exists()
        },
        "theorem": THEOREM.name,
        "theorem_sha256": (
            sha256(THEOREM) if THEOREM.exists() else None
        ),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / (
        "p5_h22_all_rank_one_triangle_component_generic_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))
    if not verified:
        raise AssertionError(
            ("Singular steps failed or timed out", failed)
        )


if __name__ == "__main__":
    main()
