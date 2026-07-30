#!/usr/bin/env python3
"""Verify the remaining fixed-kernel q5_221 obstructions."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(matrix):
    order = len(matrix)
    return sp.factor(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(order))
            for permutation in itertools.permutations(range(order))
        )
    )


def coefficient(factors, rows):
    return permanent(
        [
            [
                sum(
                    left * right
                    for left, right in zip(row, factor, strict=True)
                )
                for factor in factors
            ]
            for row in rows
        ]
    )


def restricted_p3(planes):
    factors = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    return {
        bits: coefficient(
            factors,
            tuple(planes[mode][bits[mode]] for mode in range(3)),
        )
        for bits in itertools.product((0, 1), repeat=3)
    }


def pairing_matrix(rows, basis):
    return sp.Matrix(
        [
            [
                sum(
                    left * right
                    for left, right in zip(row, vector, strict=True)
                )
                for vector in basis
            ]
            for row in rows
        ]
    )


def main() -> None:
    # The two orientations of the all-normal zero-diagonal matrix.
    a, b, c, d = sp.symbols("a b c d")
    c_plus_matrix = sp.Matrix(((0, a, b), (c, 0, d), (0, 1, 0)))
    c_minus_matrix = sp.Matrix(((0, a, b), (c, 0, d), (1, 0, 0)))
    c_plus_determinant = sp.factor(c_plus_matrix.det())
    c_minus_determinant = sp.factor(c_minus_matrix.det())
    assert c_plus_determinant == b * c
    assert c_minus_determinant == a * d

    # Every nonzero derivative of a squarefree cubic has rank >= 2.
    da, db, dc = sp.symbols("da db dc")
    derivative_matrix = sp.Matrix(
        ((0, dc, db), (dc, 0, da), (db, da, 0))
    )
    principal_minors = (
        sp.factor(derivative_matrix.extract((0, 1), (0, 1)).det()),
        sp.factor(derivative_matrix.extract((0, 2), (0, 2)).det()),
        sp.factor(derivative_matrix.extract((1, 2), (1, 2)).det()),
    )
    assert principal_minors == (-dc**2, -db**2, -da**2)

    # Concrete support-two P3 charts used in the two proofs.
    # Cover #7, Q12: normals (u0,h0,h0), factors (u1,u0,u0).
    cover7_q12_planes = (
        ((1, -1, 0), (0, 0, 1)),
        ((1, 1, 0), (0, 0, 1)),
        ((1, 1, 0), (0, 0, 1)),
    )
    cover7_q12 = restricted_p3(cover7_q12_planes)
    cover7_q12_support = {
        bits: value for bits, value in cover7_q12.items() if value
    }
    assert cover7_q12_support == {(1, 0, 0): 2}

    # Cover #10, Q20: normals (h1,u1,u1), factors (h0,h1,h1).
    cover10_q20_planes = (
        ((1, 0, 0), (0, 1, 1)),
        ((1, 0, 0), (0, 1, -1)),
        ((1, 0, 0), (0, 1, -1)),
    )
    cover10_q20 = restricted_p3(cover10_q20_planes)
    cover10_q20_support = {
        bits: value for bits, value in cover10_q20.items() if value
    }
    assert cover10_q20_support == {(0, 1, 1): -2}

    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = tuple(left + right for left, right in zip(e[0], e[1], strict=True))
    h0 = tuple(left - right for left, right in zip(e[0], e[1], strict=True))
    u1 = tuple(left + right for left, right in zip(e[2], e[3], strict=True))
    h1 = tuple(left - right for left, right in zip(e[2], e[3], strict=True))
    h2 = e[4]
    j01 = (u0, h1, h2)
    j12 = (e[0], e[1], u1)

    # Cover #7: the false rank-two Q20 branch gives a support-one
    # Q12 normal at H.
    cover7_false_h_rows = (h0, h1, u0)
    cover7_false_h_j12 = pairing_matrix(cover7_false_h_rows, j12)
    assert cover7_false_h_j12.rank() == 2
    nonzero_rows = tuple(
        tuple(cover7_false_h_j12[row, column] for column in range(3))
        for row in (0, 2)
    )
    support_one_normal = sp.Matrix(nonzero_rows).nullspace()[0]
    assert support_one_normal == sp.Matrix((0, 0, 1))

    # General Q12 normal at H has equal first two coordinates, and
    # support one occurs exactly when its u1 coefficient vanishes.
    aa, bb, cc = sp.symbols("aa bb cc")
    general_h_row = tuple(
        aa * u0[index] + bb * u1[index] + cc * h2[index]
        for index in range(5)
    )
    general_h_j12 = pairing_matrix((h0, general_h_row), j12)
    general_h_normal = sp.Matrix(general_h_j12).nullspace()[0]
    assert sp.factor(general_h_normal[0] - general_h_normal[1]) == 0
    assert sp.factor(general_h_normal[0]) == -bb / aa

    # In the C- proof for cover #7, the two Q21 intersections vanish.
    ka, kb, kc = sp.symbols("ka kb kc", nonzero=True)
    q02_row = tuple(
        kb * u0[index] - ka * u1[index] + kc * h2[index]
        for index in range(5)
    )
    intersection_matrix = sp.Matrix(
        (h0, h1, q02_row, u1, h2)
    )
    intersection_determinant = sp.factor(intersection_matrix.det())
    assert intersection_determinant == -4 * kb

    # Cover #10: the rank-one Q20 branch gives a support-one Q01
    # normal at P.
    cover10_rank_one_rows = (h0, u0, h2)
    cover10_rank_one_j01 = pairing_matrix(
        cover10_rank_one_rows, j01
    )
    assert cover10_rank_one_j01.rank() == 2
    p_nonzero_rows = tuple(
        tuple(cover10_rank_one_j01[row, column] for column in range(3))
        for row in (1, 2)
    )
    cover10_support_one = sp.Matrix(p_nonzero_rows).nullspace()[0]
    assert cover10_support_one == sp.Matrix((0, 1, 0))

    # In the rank-two branch, the X,Y Q01 maps are invertible.
    az = sp.symbols("az", nonzero=True)
    lifted_h0 = tuple(
        h0[index] + az * h2[index] for index in range(5)
    )
    z_j01 = pairing_matrix((u0, h1, lifted_h0), j01)
    z_j01_determinant = sp.factor(z_j01.det())
    assert z_j01_determinant == 4 * az

    # A valid full-support sign rectangle has only two vertices whose
    # last two coordinates agree; a support-two edge has only one.
    sign_rectangle = (
        (1, 1, 1),
        (1, -1, -1),
        (1, -1, 1),
        (1, 1, -1),
    )
    equality_vertices = tuple(
        normal for normal in sign_rectangle if normal[1] == normal[2]
    )
    support_two_variants = ((0, 1, 1), (0, 1, -1))
    equality_support_two = tuple(
        normal
        for normal in support_two_variants
        if normal[1] == normal[2]
    )
    assert len(equality_vertices) == 2
    assert len(equality_support_two) == 1

    # The cover-#7 factor collision uses Q01/h1=2 Sym(u0,h2).
    q01 = (u0, h1, h2)
    q01_h1_matrix = sp.Matrix(
        [
            [
                coefficient(q01, (h1, left, right))
                for right in e
            ]
            for left in e
        ]
    )
    expected_u0_h2 = sp.Matrix(
        [
            [
                2 * coefficient((u0, h2), (left, right))
                for right in e
            ]
            for left in e
        ]
    )
    assert q01_h1_matrix == expected_u0_h2

    cover_patterns = {
        7: (0b0011, 0b0111, 0b1001),
        10: (0b0011, 0b1101, 0b0011),
    }

    output = {
        "verified": True,
        "field": "C",
        "monotone_cover_orbits": [7, 10],
        "cover_patterns": {
            str(index): [format(bits, "04b") for bits in pattern]
            for index, pattern in cover_patterns.items()
        },
        "C_plus_determinant": str(c_plus_determinant),
        "C_minus_determinant": str(c_minus_determinant),
        "derivative_principal_minors": [
            str(value) for value in principal_minors
        ],
        "cover7_Q12_tensor_support": ["100"],
        "cover7_Q12_factor_directions": ["u1", "u0", "u0"],
        "cover7_Q21_intersection_determinant": str(
            intersection_determinant
        ),
        "cover10_Q20_tensor_support": ["011"],
        "cover10_Q20_factor_directions": ["h0", "h1", "h1"],
        "cover10_Q01_invertibility_determinant": str(
            z_j01_determinant
        ),
        "all_equal_coordinate_P3_triples": 0,
        "factor_line_collision": True,
        "monotone_covers_excluded": True,
        "remaining_monotone_cover_orbits": [8, 12, 13],
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_remaining_fixed_kernel_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
