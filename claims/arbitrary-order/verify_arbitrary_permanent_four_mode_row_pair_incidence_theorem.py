"""Verify the four-mode row-pair incidence theorem's symbolic core."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # Equality at three forces null axes e0,e1,e2.  Selecting the modes with
    # null axes e1,e2 leaves e0 and torus nulls in the contracted complement,
    # so the concise target contraction has only its color-zero entry.
    t1, t2, t3, t4 = sp.symbols("t1:5", nonzero=True)
    e0 = sp.Matrix((1, 0, 0))
    torus = (
        sp.Matrix((t1, 1, 1)),
        sp.Matrix((1, t2, 1)),
        sp.Matrix((1, 1, t3)),
        sp.Matrix((t4, 1, 1)),
    )
    target_weights = sp.symbols("lambda0:3", nonzero=True)
    diagonal = []
    for color in range(3):
        diagonal.append(
            target_weights[color]
            * e0[color]
            * sp.prod(vector[color] for vector in torus)
        )
    assert diagonal[0] != 0
    assert diagonal[1:] == [0, 0]

    # Local two-row columns.  At the e1-null mode, columns 0 and 2 form a
    # basis; at the e2-null mode, columns 0 and 1 form a basis.
    a, b, g, h = sp.symbols("a b g h")
    i, j, k, ell = sp.symbols("i j k ell")
    r1 = sp.Matrix.hstack(sp.Matrix((a, b)), sp.zeros(2, 1), sp.Matrix((g, h)))
    r2 = sp.Matrix.hstack(sp.Matrix((i, j)), sp.Matrix((k, ell)), sp.zeros(2, 1))
    j_form = sp.Matrix(((0, 1), (1, 0)))
    response = sp.expand(r1.T * j_form * r2)

    # A rank-one color-zero target forces the color-2 column at the first
    # mode to annihilate both basis columns at the second mode.
    equation_20 = response[2, 0]
    equation_21 = response[2, 1]
    assert equation_20 == g * j + h * i
    assert equation_21 == ell * g + h * k

    coefficient_matrix = sp.Matrix(((j, i), (ell, k)))
    second_basis = sp.Matrix(((i, k), (j, ell)))
    assert sp.expand(coefficient_matrix.det() + second_basis.det()) == 0

    # Cramer's eliminations: if both response entries vanish and the second
    # local pair is a basis, then g=h=0, contradicting the first basis.
    elimination_g = sp.expand(k * equation_20 - i * equation_21)
    elimination_h = sp.expand(ell * equation_20 - j * equation_21)
    assert sp.expand(elimination_g + g * second_basis.det()) == 0
    assert sp.expand(elimination_h - h * second_basis.det()) == 0

    first_basis = sp.Matrix(((a, g), (b, h)))
    assert first_basis.det() == a * h - b * g
    assert first_basis.det().subs({g: 0, h: 0}) == 0

    # Representative full-rank endpoint frames give a rank-two corrected
    # block, as the injective-invertible-surjective proof requires.
    sample = response.subs({a: 1, b: 0, g: 0, h: 1, i: 1, j: 0, k: 0, ell: 1})
    assert r1.subs({a: 1, b: 0, g: 0, h: 1}).rank() == 2
    assert r2.subs({i: 1, j: 0, k: 0, ell: 1}).rank() == 2
    assert sample.rank() == 2

    # Incidence equality bookkeeping: six required colour incidences across
    # exactly three two-planes gives the triangle 01,02,12.
    coordinate_planes = ({0, 1}, {0, 2}, {1, 2})
    assert all(sum(color in plane for plane in coordinate_planes) == 2 for color in range(3))
    assert sum(len(plane) for plane in coordinate_planes) == 6

    print("PASS: equality-at-three coordinate-plane normal form")
    print("PASS: partially polarized target has rank one")
    print("PASS: nondegenerate two-row pairing contradiction")
    print("SCOPE: at least four incidence modes; P7 and Krenn--Gu unresolved")


if __name__ == "__main__":
    main()
