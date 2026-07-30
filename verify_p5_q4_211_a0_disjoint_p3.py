#!/usr/bin/env python3
"""Verify the ternary-Segre obstruction on the a=0 disjoint boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md"
P3_THEOREM = ROOT / "P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md"
P3_VERIFIER = ROOT / "verify_p3_decomposable_restriction_classification.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    order = len(rows)
    matrix = sp.Matrix.vstack(*(row.T for row in rows))
    return sp.expand(
        sum(
            sp.prod(matrix[index, permutation[index]] for index in range(order))
            for permutation in itertools.permutations(range(order))
        )
    )


def main() -> None:
    f = sp.Matrix([1, 0, -1, 0])
    h = sp.Matrix([1, 0, 0, -1])
    assert permanent((f, f, h, h)) == 0

    z_e, z_s, z_p, z_q = sp.symbols("z_E z_S z_P z_Q")
    z = sp.Matrix([z_e, z_s, z_p, z_q])
    zero_slice_witnesses = (
        permanent((f, f, h, z)),
        permanent((f, h, f, z)),
        permanent((f, z, h, h)),
    )
    assert zero_slice_witnesses == (2 * z_s,) * 3

    # Once the last three rows have zero S coordinate, the P4 permanent
    # separates as the S coordinate in the first mode times P3(E,P,Q).
    r_e, r_s, r_p, r_q = sp.symbols("r_E r_S r_P r_Q")
    b_e, b_p, b_q = sp.symbols("b_E b_P b_Q")
    c_e, c_p, c_q = sp.symbols("c_E c_P c_Q")
    d_e, d_p, d_q = sp.symbols("d_E d_P d_Q")
    row_r = sp.Matrix([r_e, r_s, r_p, r_q])
    row_b = sp.Matrix([b_e, 0, b_p, b_q])
    row_c = sp.Matrix([c_e, 0, c_p, c_q])
    row_d = sp.Matrix([d_e, 0, d_p, d_q])
    ternary_b = sp.Matrix([b_e, b_p, b_q])
    ternary_c = sp.Matrix([c_e, c_p, c_q])
    ternary_d = sp.Matrix([d_e, d_p, d_q])
    factorization = sp.factor(
        permanent((row_r, row_b, row_c, row_d))
        - r_s * permanent((ternary_b, ternary_c, ternary_d))
    )
    assert factorization == 0

    b_p, b_q, c_p, c_q, d_p, d_q = sp.symbols(
        "b_P b_Q c_P c_Q d_P d_Q"
    )
    f3 = sp.Matrix([1, -1, 0])
    h3 = sp.Matrix([1, 0, -1])
    moving_b = sp.Matrix([0, b_p, b_q])
    moving_c = sp.Matrix([0, c_p, c_q])
    moving_d = sp.Matrix([0, d_p, d_q])
    planes = (
        (f3, moving_b),
        (h3, moving_c),
        (h3, moving_d),
    )
    coefficients = {
        bits: sp.factor(
            permanent(
                tuple(planes[mode][bits[mode]] for mode in range(3))
            )
        )
        for bits in itertools.product((0, 1), repeat=3)
    }
    expected = {
        (0, 0, 0): 2,
        (0, 0, 1): -d_p - d_q,
        (0, 1, 0): -c_p - c_q,
        (0, 1, 1): c_p * d_q + c_q * d_p,
        (1, 0, 0): -2 * b_p,
        (1, 0, 1): b_p * d_q + b_q * d_p,
        (1, 1, 0): b_p * c_q + b_q * c_p,
        (1, 1, 1): 0,
    }
    assert coefficients == expected

    # The exact absence conditions are precisely the three displayed
    # sums: adding the other marked row raises each plane to rank three.
    assert sp.factor(
        sp.Matrix.hstack(f3, moving_b, h3).det()
    ) == -b_p - b_q
    assert sp.factor(
        sp.Matrix.hstack(h3, moving_c, f3).det()
    ) == c_p + c_q
    assert sp.factor(
        sp.Matrix.hstack(h3, moving_d, f3).det()
    ) == d_p + d_q

    # If the upper B factor vanishes, its three nontrivial coefficients
    # force b_P=c_P=d_P=0 under b_Q != 0.
    b_upper_zero = {
        b_p: 0,
        c_p: 0,
        d_p: 0,
    }
    b_lower_matrix = sp.Matrix(
        [
            [coefficients[(0, 0, 0)], coefficients[(0, 0, 1)]],
            [coefficients[(0, 1, 0)], coefficients[(0, 1, 1)]],
        ]
    )
    final_determinant = sp.factor(
        b_lower_matrix.subs(b_upper_zero).det()
    )
    assert final_determinant == -c_q * d_q

    # The other two upper-factor branches immediately violate exact
    # noncontainment.
    assert coefficients[(0, 1, 0)] == -(c_p + c_q)
    assert coefficients[(0, 0, 1)] == -(d_p + d_q)

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a=0, b*c != 0",
        "incidence_type": "exact disjoint h1:{A,B}, h2:{C,D}",
        "marked_corner": str(permanent((f, f, h, h))),
        "zero_slice_witnesses": [
            str(value) for value in zero_slice_witnesses
        ],
        "P4_to_P3_factorization": True,
        "ternary_coefficients": {
            "".join(str(bit) for bit in bits): str(value)
            for bits, value in coefficients.items()
        },
        "exact_absence_factors": [
            str(b_p + b_q),
            str(c_p + c_q),
            str(d_p + d_q),
        ],
        "final_matrix_determinant": str(final_determinant),
        "P3_predecessor_theorem": P3_THEOREM.name,
        "P3_predecessor_theorem_sha256": sha256(P3_THEOREM),
        "P3_predecessor_verifier": P3_VERIFIER.name,
        "P3_predecessor_verifier_sha256": sha256(P3_VERIFIER),
        "exact_disjoint_a0_excluded": True,
        "a0_boundary_excluded_with_adjacent_theorem": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_a0_disjoint_p3_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
