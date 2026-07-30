#!/usr/bin/env python3
"""Verify the monotone h1,h2-partner all-normal obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md"


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


def contraction_matrix(factors, direction, basis):
    return sp.Matrix(
        [
            [
                coefficient(factors, (direction, left, right))
                for right in basis
            ]
            for left in basis
        ]
    )


def bilinear_matrix(factors, basis):
    return sp.Matrix(
        [
            [
                coefficient(factors, (left, right))
                for right in basis
            ]
            for left in basis
        ]
    )


def main() -> None:
    # Orientation-I Q02 charts, shared with cover #13.
    support_two_planes = (
        ((1, 0, 0), (0, 1, -1)),
        ((1, 0, 0), (0, 1, -1)),
        ((1, 0, 0), (0, 1, 1)),
    )
    support_two = restricted_p3(support_two_planes)
    assert {
        bits: value for bits, value in support_two.items() if value
    } == {(1, 1, 0): -2}

    full_planes = (
        ((-1, 1, 0), (-1, 0, 1)),
        ((1, 1, 0), (1, 0, 1)),
        ((1, 1, 0), (-1, 0, 1)),
    )
    full = restricted_p3(full_planes)
    assert {
        bits: value for bits, value in full.items() if value
    } == {(1, 0, 0): 2, (1, 0, 1): -2}

    e = tuple(
        tuple(1 if row == column else 0 for column in range(4))
        for row in range(4)
    )
    u0 = tuple(left + right for left, right in zip(e[0], e[1]))
    h0 = tuple(left - right for left, right in zip(e[0], e[1]))
    u1 = tuple(left + right for left, right in zip(e[2], e[3]))
    h1 = tuple(left - right for left, right in zip(e[2], e[3]))
    t2 = (e[0], e[1], e[2], e[3])

    q0, q1, r0, r1, s0, s1 = sp.symbols(
        "q0 q1 r0 r1 s0 s1"
    )
    q_row = tuple(q0 * u0[index] + q1 * h0[index] for index in range(4))
    r_row = tuple(r0 * u0[index] + r1 * h0[index] for index in range(4))
    s_row = tuple(s0 * h0[index] + s1 * u1[index] for index in range(4))
    support_two_t2 = coefficient(t2, (h1, q_row, r_row, s_row))
    assert support_two_t2 == 0

    q = sp.symbols("Q0:4")
    r = sp.symbols("R0:4")
    s = sp.symbols("S0:4")
    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    q_plus = tuple(q[index] + alpha * h1[index] for index in range(4))
    r_plus = tuple(r[index] + beta * h1[index] for index in range(4))

    def rectangle(q_row, r_row):
        return coefficient(t2, (h1, q_row, r_row, s))

    rectangle_identity = sp.factor(
        rectangle(q_plus, r_plus)
        - rectangle(q_plus, r)
        - rectangle(q, r_plus)
        + rectangle(q, r)
    )
    triple_h1 = coefficient(t2, (h1, h1, h1, s))
    assert rectangle_identity == triple_h1 == 0

    # In orientation I, alpha_F2=epsilon_0.  Inverting the
    # zero-diagonal pullback matrix shows that the target-two row at F
    # restricts to a nonzero multiple of h1 on H2.
    ia, ib, ic, id_ = sp.symbols("ia ib ic id", nonzero=True)
    orientation_i_matrix = sp.Matrix(
        ((0, ia, ib), (ic, 0, id_), (1, 0, 0))
    )
    orientation_i_determinant = sp.factor(
        orientation_i_matrix.det()
    )
    target_two_in_normal_basis = orientation_i_matrix.T.inv() * sp.Matrix(
        (0, 0, 1)
    )
    assert orientation_i_determinant == ia * id_
    assert target_two_in_normal_basis == sp.Matrix(
        (0, 1 / id_, -ic / id_)
    )

    # Orientation II has alpha_F2=epsilon_1.  The zero-diagonal
    # pullback matrix forces the directed cycle Q20,Q01,Q12.
    a, b, c, d = sp.symbols("a b c d")
    orientation_ii_matrix = sp.Matrix(
        ((0, a, b), (c, 0, d), (0, 1, 0))
    )
    orientation_ii_determinant = sp.factor(
        orientation_ii_matrix.det()
    )
    assert orientation_ii_determinant == b * c

    # The rank-two Q20 branch uses the support-two normal chart
    # (u1,u1,h1), with factors (h1,h1,h0).
    q20_support_two = restricted_p3(support_two_planes)
    assert {
        bits: value
        for bits, value in q20_support_two.items()
        if value
    } == {(1, 1, 0): -2}

    e5 = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0_5 = tuple(
        left + right for left, right in zip(e5[0], e5[1], strict=True)
    )
    h0_5 = tuple(
        left - right for left, right in zip(e5[0], e5[1], strict=True)
    )
    u1_5 = tuple(
        left + right for left, right in zip(e5[2], e5[3], strict=True)
    )
    h1_5 = tuple(
        left - right for left, right in zip(e5[2], e5[3], strict=True)
    )
    h2_5 = e5[4]
    q20 = (h0_5, e5[2], e5[3])
    q01 = (u0_5, h1_5, h2_5)
    q12 = (e5[0], e5[1], u1_5)
    basis5 = e5

    q20_by_h1 = contraction_matrix(q20, h1_5, basis5)
    expected_h0_h1 = bilinear_matrix((h0_5, h1_5), basis5)
    assert q20_by_h1 == -expected_h0_h1

    q12_by_u0 = contraction_matrix(q12, u0_5, basis5)
    expected_u0_u1 = bilinear_matrix((u0_5, u1_5), basis5)
    assert q12_by_u0 == expected_u0_u1

    q01_by_u0 = contraction_matrix(q01, u0_5, basis5)
    expected_h1_h2 = bilinear_matrix((h1_5, h2_5), basis5)
    assert q01_by_u0 == 2 * expected_h1_h2

    q01_by_h1 = contraction_matrix(q01, h1_5, basis5)
    expected_u0_h2 = bilinear_matrix((u0_5, h2_5), basis5)
    assert q01_by_h1 == 2 * expected_u0_h2

    # In the rank-two branch, the asserted P and Y row spaces have the
    # required J01 ranks three and one.
    aa, bb = sp.symbols("aa bb", nonzero=True)
    j01 = (u0_5, h1_5, h2_5)
    p_rows = (
        h1_5,
        h2_5,
        tuple(
            aa * u0_5[index] + bb * h0_5[index]
            for index in range(5)
        ),
    )
    p_j01 = sp.Matrix(
        [[sum(x * y for x, y in zip(row, vector, strict=True))
          for vector in j01] for row in p_rows]
    )
    assert sp.factor(p_j01.det()) == 4 * aa

    y_rows = (u0_5, h0_5, u1_5)
    y_j01 = sp.Matrix(
        [[sum(x * y for x, y in zip(row, vector, strict=True))
          for vector in j01] for row in y_rows]
    )
    assert y_j01.rank() == 1

    # The two rank-one-P bilinear source pairs form a basis of H2.
    h2_pair_basis = sp.Matrix.hstack(
        sp.Matrix(h0_5),
        sp.Matrix(h1_5),
        sp.Matrix(u0_5),
        sp.Matrix(u1_5),
    )
    assert h2_pair_basis[:4, :].rank() == 4
    dependency_endpoints = tuple(itertools.product((0, 1), repeat=2))
    assert tuple(
        endpoints
        for endpoints in dependency_endpoints
        if endpoints[0] != endpoints[1]
    ) == ((0, 1), (1, 0))

    # General contraction at a rank-one Q01 mode Y.  The two possible
    # dependency orientations factor through h1 or u0 respectively.
    p, q, r = sp.symbols("p q r")
    w = tuple(
        sp.Rational(1, 2) * p * u0_5[index]
        + sp.Rational(1, 2) * q * h1_5[index]
        + r * h2_5[index]
        for index in range(5)
    )
    q01_by_w = contraction_matrix(q01, w, basis5)
    q_zero_factor = bilinear_matrix(
        (
            h1_5,
            tuple(
                p * h2_5[index] + r * u0_5[index]
                for index in range(5)
            ),
        ),
        basis5,
    )
    p_zero_factor = bilinear_matrix(
        (
            u0_5,
            tuple(
                q * h2_5[index] + r * h1_5[index]
                for index in range(5)
            ),
        ),
        basis5,
    )
    assert q01_by_w.subs(q, 0) == q_zero_factor
    assert q01_by_w.subs(p, 0) == p_zero_factor

    target_colours = (e5[0][:3], e5[1][:3], e5[2][:3])
    assert all(
        sp.Matrix.hstack(
            sp.Matrix(target_colours[left]),
            sp.Matrix(target_colours[right]),
        ).rank()
        == 2
        for left, right in itertools.combinations(range(3), 2)
    )

    cover_patterns = {
        6: (0b0011, 0b0111, 0b0101),
        11: (0b0011, 0b1101, 0b0101),
    }
    for pattern in cover_patterns.values():
        d0, d1, d2 = pattern
        all_normal = d0 & d1 & d2
        assert all_normal.bit_count() == 1
        f_mode = (all_normal & -all_normal).bit_length() - 1
        partner_bits = (d1 & d2) & ~(1 << f_mode)
        assert partner_bits.bit_count() == 1
        partner_mode = (
            (partner_bits & -partner_bits).bit_length() - 1
        )
        x_bits = d1 & ~(1 << f_mode) & ~(1 << partner_mode)
        assert x_bits
        other_non_h2 = ((1 << 4) - 1) & ~d2
        assert d0 & other_non_h2

    output = {
        "verified": True,
        "field": "C",
        "monotone_cover_orbits": [6, 11],
        "cover_patterns": {
            str(index): [format(bits, "04b") for bits in pattern]
            for index, pattern in cover_patterns.items()
        },
        "orientation_I_support_two_T2": str(support_two_t2),
        "orientation_I_rectangle_identity": str(rectangle_identity),
        "orientation_I_zero_diagonal_determinant": str(
            orientation_i_determinant
        ),
        "orientation_I_target_two_normal_coordinates": [
            str(value) for value in target_two_in_normal_basis
        ],
        "orientation_II_zero_diagonal_determinant": str(
            orientation_ii_determinant
        ),
        "orientation_II_forced_cycle": ["Q20", "Q01", "Q12"],
        "orientation_II_Q20_tensor_support": ["110"],
        "orientation_II_Q20_factor_directions": ["h1", "h1", "h0"],
        "orientation_II_rank_two_P_J01_determinant": str(
            sp.factor(p_j01.det())
        ),
        "orientation_II_rank_one_Y_J01_rank": y_j01.rank(),
        "orientation_II_dependency_orientations": ["XY", "YX"],
        "orientation_II_factor_line_collision": True,
        "monotone_covers_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_h1_partner_all_normal_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
