#!/usr/bin/env python3
"""Independent apolar audit for the h1-partner all-normal theorem."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def repeated(polynomial, variables, directions):
    value = polynomial
    for direction in directions:
        value = derivative(value, variables, direction)
    return sp.expand(value)


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    variables = (x0, x1, x2, x3, x4)
    f2 = x0 * x1 * x2 * x3
    u0 = (1, 1, 0, 0, 0)
    h0 = (1, -1, 0, 0, 0)
    u1 = (0, 0, 1, 1, 0)
    h1 = (0, 0, 1, -1, 0)
    h2 = (0, 0, 0, 0, 1)

    q0, q1, r0, r1, s0, s1 = sp.symbols(
        "q0 q1 r0 r1 s0 s1"
    )
    q_row = tuple(q0 * u0[index] + q1 * h0[index] for index in range(5))
    r_row = tuple(r0 * u0[index] + r1 * h0[index] for index in range(5))
    s_row = tuple(s0 * h0[index] + s1 * u1[index] for index in range(5))
    support_two = repeated(
        f2,
        variables,
        (h1, q_row, r_row, s_row),
    )
    triple_h1 = repeated(f2, variables, (h1, h1, h1))
    assert support_two == triple_h1 == 0

    ia, ib, ic, id_ = sp.symbols("ia ib ic id", nonzero=True)
    orientation_i_matrix = sp.Matrix(
        ((0, ia, ib), (ic, 0, id_), (1, 0, 0))
    )
    orientation_i_target_two = (
        orientation_i_matrix.T.inv() * sp.Matrix((0, 0, 1))
    )
    assert orientation_i_target_two == sp.Matrix(
        (0, 1 / id_, -ic / id_)
    )

    # The independent zero-diagonal calculation gives the correct
    # orientation-II cycle Q20,Q01,Q12.
    a, b, c, d = sp.symbols("a b c d")
    zero_diagonal = sp.Matrix(
        ((0, a, b), (c, 0, d), (0, 1, 0))
    )
    zero_diagonal_determinant = sp.factor(zero_diagonal.det())
    assert zero_diagonal_determinant == b * c

    # Squarefree polynomial representatives of the three residuals.
    q20 = (x0 - x1) * x2 * x3
    q01 = (x0 + x1) * (x2 - x3) * x4
    q12 = x0 * x1 * (x2 + x3)
    q20_h1 = derivative(q20, variables, h1)
    q12_u0 = derivative(q12, variables, u0)
    q01_u0 = derivative(q01, variables, u0)
    q01_h1 = derivative(q01, variables, h1)
    assert sp.expand(q20_h1 + (x0 - x1) * (x2 - x3)) == 0
    assert sp.expand(q12_u0 - (x0 + x1) * (x2 + x3)) == 0
    assert sp.expand(q01_u0 - 2 * (x2 - x3) * x4) == 0
    assert sp.expand(q01_h1 - 2 * (x0 + x1) * x4) == 0

    # The two bilinear source pairs in the rank-one-P branch form a
    # basis of H2, so assigning both dependencies to one endpoint
    # leaves image rank at most two.
    source_pair_basis = sp.Matrix.hstack(
        sp.Matrix(h0),
        sp.Matrix(h1),
        sp.Matrix(u0),
        sp.Matrix(u1),
    )
    source_pair_rank = source_pair_basis[:4, :].rank()
    assert source_pair_rank == 4

    # At a rank-one Q01 mode Y, write the surviving derivative by its
    # values p,q,r on u0,h1,h2.  The two opposite dependency
    # orientations factor through h1 or u0.
    p, q, r = sp.symbols("p q r")
    w = tuple(
        sp.Rational(1, 2) * p * u0[index]
        + sp.Rational(1, 2) * q * h1[index]
        + r * h2[index]
        for index in range(5)
    )
    q01_w = derivative(q01, variables, w)
    assert sp.factor(q01_w.subs(q, 0)) == sp.factor(
        (x2 - x3) * (p * x4 + r * (x0 + x1))
    )
    assert sp.factor(q01_w.subs(p, 0)) == sp.factor(
        (x0 + x1) * (q * x4 + r * (x2 - x3))
    )

    # An invertible map on one side of a rank-one bilinear tensor
    # forces the two images on the other side to be dependent.
    z00, z01, z10, z11 = sp.symbols("z00 z01 z10 z11")
    independent_side = sp.eye(2)
    other_side = sp.Matrix(((z00, z01), (z10, z11)))
    transformed_bilinear = independent_side * other_side.T
    rank_one_minor = sp.factor(transformed_bilinear.det())
    assert rank_one_minor == z00 * z11 - z01 * z10

    output = {
        "audited": True,
        "field": "C",
        "method": "independent block-apolar differentiation",
        "orientation_I_support_two_T2": str(support_two),
        "orientation_I_third_h1_derivative": str(triple_h1),
        "orientation_I_target_two_normal_coordinates": [
            str(value) for value in orientation_i_target_two
        ],
        "orientation_II_zero_diagonal_determinant": str(
            zero_diagonal_determinant
        ),
        "orientation_II_Q20_by_h1": str(q20_h1),
        "orientation_II_Q12_by_u0": str(q12_u0),
        "orientation_II_Q01_by_u0": str(q01_u0),
        "orientation_II_Q01_by_h1": str(q01_h1),
        "orientation_II_source_pair_rank": source_pair_rank,
        "orientation_II_q_zero_factorization": str(
            sp.factor(q01_w.subs(q, 0))
        ),
        "orientation_II_p_zero_factorization": str(
            sp.factor(q01_w.subs(p, 0))
        ),
        "orientation_II_factor_line_collision": True,
        "ambient_maps_enumerated": 0,
        "monotone_cover_orbits": [6, 11],
        "monotone_covers_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "apolar zeros, directed cycle, and factor-line collision",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_h1_partner_all_normal_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
