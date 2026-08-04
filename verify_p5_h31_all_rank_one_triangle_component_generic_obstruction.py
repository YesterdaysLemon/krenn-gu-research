#!/usr/bin/env python3
"""Verify the generic H31 obstruction on the all-rank-one triangle component.

Exact characteristic-zero theorem verifier for
P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md, in the
established generic marked-H31 pattern (marked bases
beta_i(t)=beta_i+t_i*alpha_i over the free component function field
C(p,q), four distinguished source coordinates, exact Singular marking
projections with bidirectional ideal equality, and per-sheet Fitting
certificates in which line-sheet parameters stay polynomial ring
variables).

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
    / "P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md"
COMPONENT_PRIMARY = (
    ROOT / "verify_p4_all_rank_one_triangle_pure_component.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    word for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR_TIMEOUT = 550

P, Q = sp.symbols("p q")
S = sp.Symbol("s")
K, L = sp.symbols("k l")

EXPECTED_PROJECTIONS = {
    0: ("t3", "t2", "t1"),
    1: ("1",),
    2: ("t3", "t1", "t0*t2"),
    3: (
        "(p*q+1)*t3+(p*q+p+1)",
        "t2",
        "t1",
        "(p*q+p+1)*t0+(q+1)",
    ),
}

# sheet name -> (distinguished, marking, killing mode, minor row sets)
SHEETS = {
    "q0_t0_line": (0, (S, 0, 0, 0), 1, ((0, 2, 3, 7), (0, 3, 6, 7))),
    "q2_t0_line": (2, (S, 0, 0, 0), 3, ((0, 2, 3, 7), (0, 2, 6, 7))),
    "q2_t2_line": (2, (0, 0, S, 0), 3, ((0, 2, 4, 7), (0, 2, 6, 7))),
    "q3_point": (
        3,
        (
            -(Q + 1) / (P * Q + P + 1),
            0,
            0,
            -(P * Q + P + 1) / (P * Q + 1),
        ),
        1,
        ((0, 1, 4, 7),),
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
    """Run Singular fail-closed; return stdout or None on any failure."""
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


def extension_coefficients(distinguished, alpha, beta, extension):
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_extended = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (extension[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        word: permanent(
            tuple(
                beta_extended[mode] if word[mode]
                else alpha_extended[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }


def mixed_system(distinguished, alpha, beta, extensions):
    coefficients = extension_coefficients(
        distinguished, alpha, beta, sp.Matrix(extensions)
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


def marked_extension(distinguished, extension, alpha, beta, mode):
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_extended = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row],)
        for row in range(4)
    )
    beta_extended = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_extended, beta_extended)


def singular_polynomial(expression) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def reconstruction_direction(distinguished, alpha, marked_beta):
    return sp.Matrix(
        [alpha[mode][distinguished] for mode in range(4)]
        + [marked_beta[mode][distinguished] for mode in range(4)]
    )


def check_reconstruction_kernel(alpha, beta):
    """The marked tensor is the single word -2 for every marking, so
    restoring the deleted coordinate is a kernel direction of every
    mixed system, with diagonals (0, -2)."""
    shifts = sp.symbols("t0:4")
    marked_beta = shifted_basis(alpha, beta, shifts)
    extensions = sp.symbols("z0:8")
    for distinguished in range(4):
        mixed, diagonal_a, diagonal_b = mixed_system(
            distinguished, alpha, marked_beta, extensions
        )
        direction = reconstruction_direction(
            distinguished, alpha, marked_beta
        )
        assert all(
            sp.expand(value) == 0 for value in mixed * direction
        ), distinguished
        assert sp.expand((diagonal_a * direction)[0]) == 0, distinguished
        assert (
            sp.expand((diagonal_b * direction)[0] + 2) == 0
        ), distinguished


def run_projection(distinguished, alpha, beta):
    extensions = sp.symbols("z0:8")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_system(
        distinguished, alpha, marked_beta, extensions
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.append((diagonal_a * extension)[0] - 1)
    equations.append(inverse * (diagonal_b * extension)[0] - 1)
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    expected = EXPECTED_PROJECTIONS[distinguished]
    lines = [
        "ring R=(0,p,q),("
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
            ("projection ideal mismatch", distinguished, stdout)
        )
    return {
        "computed_equals_expected_bidirectionally": True,
        "expected_generators": list(expected),
        "groebner_basis_size": int(fields[2]),
    }


def clear_vector(vector):
    vector = sp.Matrix([sp.cancel(entry) for entry in vector])
    lcm = sp.lcm([sp.denom(entry) for entry in vector])
    vector = sp.Matrix(
        [sp.expand(sp.cancel(entry * lcm)) for entry in vector]
    )
    divisor = sp.gcd(list(vector))
    if divisor not in (0, 1):
        vector = sp.Matrix(
            [sp.cancel(entry / divisor) for entry in vector]
        )
    return vector


# Displayed genuine kernel generators per sheet (cleared entries).
DISPLAYED_Z_GEN = {
    "q0_t0_line": (-1, -1, 0, 0, S, 0, 1, 0),
    "q2_t0_line": (
        P * Q + 1, 0, 0, 1, -(S * (P * Q + 1) + Q), 1, 0, 0,
    ),
    "q2_t2_line": (
        -P * (P * Q + 1),
        -S * (P * Q + 1),
        0,
        S - P,
        Q * (P - S),
        S - P,
        S * (P * Q + 1),
        0,
    ),
    "q3_point": (
        -P**2 * (P * Q + P + 1),
        0,
        (P * Q + P + 1) ** 2,
        -(P * Q + 1) * (P * Q + P + 1),
        P * Q + 1,
        (P * Q + 1) * (P * Q + P + 1),
        0,
        0,
    ),
}

# Rank-six pivot witnesses (rows, columns, factored determinant).
SHEET_PIVOTS = {
    "q0_t0_line": (
        (0, 1, 3, 5, 6, 7),
        (0, 1, 2, 3, 4, 5),
        2 * (P * Q + 1) ** 2 * (P * Q + P + 1),
    ),
    "q2_t0_line": (
        (0, 1, 2, 3, 6, 7),
        (0, 1, 2, 3, 4, 6),
        2 * P * (P * Q + 1) ** 2,
    ),
    "q2_t2_line": (
        (0, 1, 2, 3, 6, 7),
        (1, 2, 3, 4, 5, 6),
        -2 * P * (P * Q + 1) ** 3,
    ),
    "q3_point": (
        (0, 1, 2, 3, 4, 7),
        (0, 1, 2, 3, 4, 6),
        2 * P**2 * (P * Q + P + 1) / (P * Q + 1),
    ),
}


def sheet_kernel_data(name, alpha, beta):
    distinguished, marking, mode, row_sets = SHEETS[name]
    extensions = sp.symbols("z0:8")
    marked_beta = shifted_basis(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_system(
        distinguished, alpha, marked_beta, extensions
    )
    z_rec = reconstruction_direction(
        distinguished, alpha, marked_beta
    )
    z_gen = sp.Matrix(DISPLAYED_Z_GEN[name])
    # both displayed vectors are in the kernel
    assert all(
        sp.cancel(value) == 0 for value in mixed * z_rec
    ), name
    assert all(
        sp.cancel(value) == 0 for value in mixed * z_gen
    ), name
    # they are independent
    independent = any(
        sp.cancel(
            z_rec[left] * z_gen[right] - z_rec[right] * z_gen[left]
        )
        != 0
        for left, right in itertools.combinations(range(8), 2)
    )
    assert independent, name
    # the mixed matrix has rank six: one nonzero six-by-six pivot,
    # with a line-parameter-free determinant on the line sheets
    pivot_rows, pivot_columns, pivot_value = SHEET_PIVOTS[name]
    pivot = mixed[list(pivot_rows), list(pivot_columns)].det(
        method="berkowitz"
    )
    assert sp.cancel(pivot - pivot_value) == 0, name
    diag_a_gen = sp.factor((diagonal_a * z_gen)[0])
    diag_b_gen = sp.factor((diagonal_b * z_gen)[0])
    return {
        "distinguished": distinguished,
        "marking": marking,
        "mode": mode,
        "row_sets": row_sets,
        "marked_beta": marked_beta,
        "z_rec": z_rec,
        "z_gen": z_gen,
        "A_gen": diag_a_gen,
        "B_gen": diag_b_gen,
        "diagonal_a": diagonal_a,
        "diagonal_b": diagonal_b,
        "pivot": (pivot_rows, pivot_columns, pivot_value),
    }


EXPECTED_SHEET_DIAGONALS = {
    "q0_t0_line": (
        sp.Integer(2),
        -2 * S,
    ),
    "q2_t0_line": (
        2 * (P * Q + 1),
        2 * (S * (P * Q + 1) + Q),
    ),
    "q2_t2_line": (
        -2 * P * (P * Q + 1),
        -2 * Q * (P - S),
    ),
    "q3_point": (
        2 * (P * Q + 1) * (P * Q + P + 1) ** 2,
        -2 * (P - 1) * (P * Q + P + 1),
    ),
}

# Certificate-minor identities on z = k*z_gen + l*z_rec_cleared,
# written as denominator*det = numerator * A(z)^a * B(z)^b.
EXPECTED_MINOR_IDENTITIES = {
    "q0_t0_line": (
        ((0, 2, 3, 7), 1, 1, -2 * L * P * (P * Q + 1), 1),
        ((0, 3, 6, 7), 1, 1, 2 * S * (L * P - K) * (P * Q + 1), 1),
    ),
    "q2_t0_line": (
        ((0, 2, 3, 7), 1, 1,
         -2 * L * (P * Q + 1) * (P * Q - P + 1), 1),
        ((0, 2, 6, 7), 1, 1,
         2 * (K * (S * (P * Q + 1) + Q) + L * Q), 1),
    ),
    "q2_t2_line": (
        ((0, 2, 4, 7), 1, 1, 2 * L * Q * (P * Q - P + 1), 1),
        ((0, 2, 6, 7), 1, 1, -2 * Q * (K * (P - S) - L), 1),
    ),
    "q3_point": (
        (
            (0, 1, 4, 7),
            2,
            1,
            -(Q + 1),
            (P * Q + 1) * (P * Q + P + 1),
        ),
    ),
}


def check_minor_identities(name, data):
    """Exact all-extension identities on the two-dimensional kernel."""
    distinguished = data["distinguished"]
    marked_beta = data["marked_beta"]
    z_rec = clear_vector(data["z_rec"])
    z_gen = data["z_gen"]
    z_general = sp.Matrix(
        [
            sp.expand(K * generic + L * reconstruction)
            for generic, reconstruction in zip(z_gen, z_rec)
        ]
    )
    diag_a = sp.expand((data["diagonal_a"] * z_general)[0])
    diag_b = sp.expand((data["diagonal_b"] * z_general)[0])
    alpha, _beta = family()
    marked = marked_extension(
        distinguished, z_general, alpha, marked_beta, data["mode"]
    )
    identities = []
    for rows, a_power, b_power, numerator, denominator in (
        EXPECTED_MINOR_IDENTITIES[name]
    ):
        determinant = sp.expand(
            marked[list(rows), :].det(method="berkowitz")
        )
        difference = sp.expand(
            sp.expand(denominator * determinant)
            - sp.expand(
                numerator * diag_a**a_power * diag_b**b_power
            )
        )
        if difference != 0:
            coefficients = sp.Poly(difference, K, L).coeffs()
            assert all(
                sp.cancel(coefficient) == 0
                for coefficient in coefficients
            ), (name, rows)
        identities.append(
            {
                "rows": list(rows),
                "A_power": a_power,
                "B_power": b_power,
                "residual_factor": str(
                    sp.cancel(numerator / denominator)
                ),
            }
        )
    return identities


def fitting_certificate(name, data):
    distinguished = data["distinguished"]
    marking = data["marking"]
    mode = data["mode"]
    row_sets = data["row_sets"]
    alpha, beta = family()
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    marked_beta = data["marked_beta"]
    mixed, diagonal_a, diagonal_b = mixed_system(
        distinguished, alpha, marked_beta, extensions
    )
    extension = sp.Matrix(extensions)
    marked = marked_extension(
        distinguished, extension, alpha, marked_beta, mode
    )
    determinants = [
        sp.expand(marked[list(rows), :].det(method="berkowitz"))
        for rows in row_sets
    ]
    first = (diagonal_a * extension)[0]
    second = (diagonal_b * extension)[0]
    equations = (
        list(mixed * extension)
        + determinants
        + [inverse * first * second - 1]
    )
    line_variables = tuple(
        symbol
        for entry in marking
        for symbol in sp.sympify(entry).free_symbols
        if symbol not in (P, Q)
    )
    variables = extensions + (inverse,) + tuple(set(line_variables))
    program = "\n".join(
        (
            "ring R=(0,p,q),("
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
        "line_parameter_kept_polynomial": bool(line_variables),
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

    shifts = sp.symbols("t0:4")
    marked = shifted_basis(alpha, beta, shifts)
    marked_pure = {
        word: sp.factor(
            permanent(
                tuple(
                    marked[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert marked_pure == pure

    check_reconstruction_kernel(alpha, beta)

    projections = {}
    for distinguished in range(4):
        projections[str(distinguished)] = run_projection(
            distinguished, alpha, beta
        )

    sheets = {}
    identities = {}
    certificates = {}
    for name in SHEETS:
        data = sheet_kernel_data(name, alpha, beta)
        expected_a, expected_b = EXPECTED_SHEET_DIAGONALS[name]
        assert sp.cancel(data["A_gen"] - expected_a) == 0, name
        assert sp.cancel(data["B_gen"] - expected_b) == 0, name
        pivot_rows, pivot_columns, pivot_value = data["pivot"]
        sheets[name] = {
            "distinguished": data["distinguished"],
            "marking": [str(entry) for entry in data["marking"]],
            "mixed_rank": 6,
            "kernel_dimension": 2,
            "rank_six_pivot_rows": list(pivot_rows),
            "rank_six_pivot_columns": list(pivot_columns),
            "rank_six_pivot_determinant": str(pivot_value),
            "z_gen": [str(entry) for entry in data["z_gen"]],
            "A_gen": str(data["A_gen"]),
            "B_gen": str(data["B_gen"]),
        }
        identities[name] = check_minor_identities(name, data)
        certificates[name] = fitting_certificate(name, data)

    failed = [
        str(distinguished)
        for distinguished, value in projections.items()
        if value is None
    ] + [name for name, value in certificates.items() if value is None]
    verified = not failed

    output = {
        "verified": verified,
        "field": "C(p,q) (free rational component function field)",
        "method": (
            "single-word reconstruction kernel, exact function-field "
            "marked projections with bidirectional ideal equality, "
            "and per-sheet Fitting certificates with polynomial "
            "line-sheet parameters"
        ),
        "pure_coefficient": "-2 (word 1111 only, all markings)",
        "marked_tensor_invariant": True,
        "reconstruction_kernel_all_coordinates": True,
        "reconstruction_diagonals": ["0", "-2"],
        "projections": projections,
        "marking_loci": {
            "0": "t1=t2=t3=0 (whole t0-line)",
            "1": "empty (unit ideal)",
            "2": "t1=t3=0, t0*t2=0 (t0-line union t2-line)",
            "3": (
                "t1=t2=0, t0=-(q+1)/(pq+p+1), "
                "t3=-(pq+p+1)/(pq+1) (one point)"
            ),
        },
        "surviving_marking_sheets": 4,
        "sheet_kernels": sheets,
        "minor_identities": identities,
        "fitting_certificates": certificates,
        "failed_steps_recorded_as_null": failed,
        "generic_marked_fibre_excluded": verified,
        "complete_boundary_marked_fibre_excluded": False,
        "known_pure_component_orbits_at_least": 13,
        "components_one_through_nine_generic_marked_fibres_excluded": (
            verified
        ),
        "components_ten_through_thirteen_H31_open": True,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "weighted_H22_excluded_on_component": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (COMPONENT, COMPONENT_PRIMARY)
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
        "p5_h31_all_rank_one_triangle_component_generic_verified.json"
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
