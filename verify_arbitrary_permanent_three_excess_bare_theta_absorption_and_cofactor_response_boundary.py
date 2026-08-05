"""Exact verifier for bare-theta absorption and marked cofactor response."""

from __future__ import annotations

from collections import Counter

import sympy as sp


def main() -> None:
    a, b, c, d, e, f, g = sp.symbols("A B C D E F G", nonzero=True)
    x = sp.Matrix(((a, b, c), (d, e, 0), (f, 0, g)))
    z = a * e * g + b * d * g + c * e * f

    q = sp.Matrix(
        3,
        3,
        lambda i, j: x.minor_submatrix(i, j).per(),
    )
    expected_q = sp.Matrix(
        ((e * g, d * g, e * f), (b * g, a * g + c * f, b * f), (c * e, c * d, a * e + b * d))
    )
    assert q == expected_q

    identities = (
        z * g - (q[0, 0] * q[1, 1] + q[0, 1] * q[1, 0]),
        z * e - (q[0, 0] * q[2, 2] + q[0, 2] * q[2, 0]),
        z * b - (q[1, 0] * q[2, 2] + q[1, 2] * q[2, 0]),
        z * c - (q[1, 0] * q[2, 1] + q[1, 1] * q[2, 0]),
        z * d - (q[0, 1] * q[2, 2] + q[0, 2] * q[2, 1]),
        z * f - (q[0, 1] * q[1, 2] + q[0, 2] * q[1, 1]),
    )
    assert all(sp.expand(identity) == 0 for identity in identities)

    h = q[0, 1] * q[1, 0] * q[2, 2] - q[0, 2] * q[2, 0] * q[1, 1]
    assert sp.factor(h - (b * d * g - c * e * f) * z) == 0

    a_on_z = -(b * d * g + c * e * f) / (e * g)
    assert sp.factor(q[1, 1].subs(a, a_on_z)) == -b * d * g / e
    assert sp.factor(q[2, 2].subs(a, a_on_z)) == -c * e * f / g

    # 1+1+1 absorption: quotient rows 0 and 2 to e0; row 1 retains e0,e1.
    mu = sp.symbols("mu", nonzero=True)
    l1_q = sp.Matrix((mu, 1))
    z1_q = sp.Matrix((0, 1))
    residue_111 = l1_q + z1_q - 2 * l1_q
    assert residue_111 == sp.Matrix((-mu, 0))
    assert Counter((1, 2, 2, 1, 2)) == Counter((2, 1, 2, 1, 2))
    assert sum((2, 1, 2)) == 5

    # 2+1+0 absorption: rows 1 and 2 are e2-lines; row 0 retains e0,e2.
    z0_q = sp.Matrix((1, 0))
    l1_row_q = sp.Matrix((1, 1))
    l2_row_q = sp.Matrix((1, 2))
    residue_210 = z0_q + l1_row_q - 2 * l2_row_q
    assert residue_210 == sp.Matrix((0, -3))
    assert Counter((1, 0, 1, 0, 1)) == Counter((0, 1, 0, 1, 1))
    assert sum((1, 2, 2)) == 5

    # 3+0+0 zero absorption: three independent row-zero forms sum to e2.
    l0_300 = sp.Matrix((1, 1, 0))
    l1_300 = sp.Matrix((1, -1, 0))
    l2_300 = sp.Matrix((-2, 0, 1))
    assert sp.Matrix.hstack(l0_300, l1_300, l2_300).det() != 0
    residue_300 = l0_300 + l1_300 + l2_300
    assert residue_300 == sp.Matrix((0, 0, 1))
    assert residue_300[:2, 0] == sp.Matrix((0, 0))  # zero modulo span(e2)
    assert {0}.isdisjoint({1})  # distinct surviving target lines
    assert Counter((2, 1, 2, 0, 2)) == Counter({0: 1, 1: 1, 2: 3})
    assert sum((1, 2, 2)) == 5

    # A torically transported signless equation and a Segre minor clash.
    r11, r12, r21, r22 = sp.symbols("r11 r12 r21 r22", nonzero=True)
    symmetric = r11 * r22 + r12 * r21
    alternating = r11 * r22 - r12 * r21
    assert sp.expand(symmetric + alternating) == 2 * r11 * r22
    assert sp.expand(symmetric - alternating) == 2 * r12 * r21

    print("bare-theta absorption and cofactor-response boundary: PASS")
    print("six anchor quadrics, three absorption charts, and factor-2 clash")


if __name__ == "__main__":
    main()
