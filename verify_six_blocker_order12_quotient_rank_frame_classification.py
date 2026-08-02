#!/usr/bin/env python3
"""Verify the order-twelve quotient-rank and frame classification."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_QUOTIENT_RANK_FRAME_CLASSIFICATION.md"


def hadamard(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[index] * right[index] for index in range(3)])


def quotient_and_conic_normal_forms() -> None:
    beta, delta = sp.symbols("beta delta", nonzero=True)
    q = sp.Matrix([[beta, 0, 0, delta]])
    assert q.rank() == 1
    kernel_basis = sp.Matrix(
        [
            [0, 0, delta],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, -beta],
        ]
    )
    assert kernel_basis.rank() == 3
    assert q * kernel_basis == sp.zeros(1, 3)

    # A nonzero cofactor class makes bar(Pi) a nonzero scalar multiple of q.
    cofactor_class = sp.symbols("cbar", nonzero=True)
    quotient_map = -cofactor_class * q
    assert quotient_map.rank() == 1
    assert quotient_map.nullspace() == q.nullspace()

    # In projective ker(q), substitute x00=-(delta/beta)x11 into the Segre
    # equation x00*x11-x01*x10=0.  The resulting ternary quadric is smooth
    # exactly when delta is nonzero.
    x01, x10, x11 = sp.symbols("x01 x10 x11")
    conic = -delta * x11**2 - beta * x01 * x10
    gradient = tuple(sp.diff(conic, variable) for variable in (x01, x10, x11))
    assert gradient == (-beta * x10, -beta * x01, -2 * delta * x11)
    assert sp.solve((*gradient, conic), (x01, x10, x11), dict=True) == [
        {x01: 0, x10: 0, x11: 0}
    ]

    # The delta=0 boundary factors into the two Segre rulings.
    assert sp.factor(conic.subs(delta, 0)) == -beta * x01 * x10


def symbolic_frame_identity() -> None:
    beta, delta = sp.symbols("beta delta", nonzero=True)
    xa = sp.Matrix(sp.symbols("xa0:3", nonzero=True))
    za = sp.Matrix(sp.symbols("za0:3", nonzero=True))
    xb = sp.Matrix(sp.symbols("xb0:3", nonzero=True))
    zb = sp.Matrix(sp.symbols("zb0:3", nonzero=True))
    v01 = hadamard(xa, zb)
    v10 = hadamard(za, xb)
    middle = delta * hadamard(xa, xb) - beta * hadamard(za, zb)
    frame = sp.Matrix.hstack(v01, v10, middle)

    ratios = sp.Matrix(
        3,
        3,
        lambda colour, column: (
            sp.S.One
            if column == 0
            else (za[colour] / xa[colour]) * (xb[colour] / zb[colour])
            if column == 1
            else delta * (xb[colour] / zb[colour]) - beta * (za[colour] / xa[colour])
        ),
    )
    scale = sp.prod(xa[colour] * zb[colour] for colour in range(3))
    assert sp.factor(frame.det() - scale * ratios.det()) == 0


def universal_rank_boundary_checks() -> None:
    beta, delta, a_value, r = sp.symbols("beta delta A r", nonzero=True)
    b_value = sp.symbols("B")
    r0, r1 = sp.symbols("r0 r1", nonzero=True)

    # On delta=0, equality of two normalized ratio points forces equality of
    # their r-coordinates.  Hence rank one would make za proportional to xa.
    delta_zero_minor = sp.Matrix([[1, -beta * r0], [1, -beta * r1]]).det()
    assert sp.factor(delta_zero_minor - beta * (r0 - r1)) == 0

    # For delta nonzero, rank one gives rs=A and delta*s-beta*r=B.
    # Eliminating s yields the same quadratic for every colour.  Its constant
    # term is nonzero even when B=0, because delta*A is nonzero.
    eliminated = sp.together((delta * a_value / r - beta * r - b_value) * r)
    quadratic = beta * r**2 + b_value * r - delta * a_value
    assert sp.expand(eliminated + quadratic) == 0
    assert sp.Poly(quadratic, r).TC() == -delta * a_value

    # B need not be nonzero: this exact rank-one frame has B=0 and two ratio
    # roots, while both exchanged planes remain two-dimensional.
    one = sp.Matrix([1, 1, 1])
    signed = sp.Matrix([1, 1, -1])
    b_zero_frame = sp.Matrix.hstack(
        one,
        hadamard(signed, signed),
        signed - signed,
    )
    assert sp.Matrix.hstack(one, signed).rank() == 2
    assert b_zero_frame.rank() == 1
    assert {
        (signed[index] ** 2, signed[index] - signed[index]) for index in range(3)
    } == {(1, 0)}


def frame_examples() -> dict[str, object]:
    one = sp.Matrix([1, 1, 1])

    # Full frame: beta=1, delta=2.
    xa = one
    za = sp.Matrix([1, 2, 3])
    xb = sp.Matrix([2, 3, 5])
    zb = sp.Matrix([3, 5, 7])
    full = sp.Matrix.hstack(
        hadamard(xa, zb),
        hadamard(za, xb),
        2 * hadamard(xa, xb) - hadamard(za, zb),
    )
    assert full.rank() == 3
    assert full.det() == 69

    # Rank two on delta=0; rank one is impossible there when Xa is a plane.
    za_two = sp.Matrix([1, 1, 2])
    zb_two = sp.Matrix([1, 1, 2])
    rank_two_delta_zero = sp.Matrix.hstack(
        hadamard(one, zb_two),
        hadamard(za_two, one),
        -hadamard(za_two, zb_two),
    )
    assert sp.Matrix.hstack(one, za_two).rank() == 2
    assert sp.Matrix.hstack(one, zb_two).rank() == 2
    assert rank_two_delta_zero.rank() == 2

    # Rank one with beta=delta=1.  The ratio pairs are
    # (r,s)=(1,-2),(1,-2),(2,-1), a genuine 2+1 collision.
    za_one = sp.Matrix([1, 1, 2])
    xb_one = sp.Matrix([-2, -2, -1])
    rank_one = sp.Matrix.hstack(
        hadamard(one, one),
        hadamard(za_one, xb_one),
        hadamard(one, xb_one) - hadamard(za_one, one),
    )
    assert sp.Matrix.hstack(one, za_one).rank() == 2
    assert sp.Matrix.hstack(xb_one, one).rank() == 2
    assert rank_one.rank() == 1
    ratio_pairs = tuple((za_one[index], xb_one[index]) for index in range(3))
    assert ratio_pairs == ((1, -2), (1, -2), (2, -1))
    assert {(r * s, s - r) for r, s in ratio_pairs} == {(-2, -3)}
    quadratic = sp.Poly(sp.Symbol("r") ** 2 - 3 * sp.Symbol("r") + 2)
    assert quadratic.all_roots() == [1, 2]

    # The target coefficient polynomial is common to all three colours and
    # has two complementary-support base points.
    t = sp.symbols("t")
    coefficient_polynomials = tuple(
        sp.expand((1 + t * za_one[index]) * (t * xb_one[index] - 1))
        for index in range(3)
    )
    assert len(set(coefficient_polynomials)) == 1
    assert coefficient_polynomials[0] == -2 * t**2 - 3 * t - 1
    assert sp.solve(coefficient_polynomials[0], t) == [
        sp.Rational(-1),
        sp.Rational(-1, 2),
    ]
    boundary_supports = []
    for parameter in (sp.Rational(-1), sp.Rational(-1, 2)):
        y_a = one + parameter * za_one
        y_b = parameter * xb_one - one
        assert hadamard(y_a, y_b) == sp.zeros(3, 1)
        support_a = tuple(index for index in range(3) if y_a[index] != 0)
        support_b = tuple(index for index in range(3) if y_b[index] != 0)
        assert set(support_a).isdisjoint(support_b)
        assert set(support_a) | set(support_b) == set(range(3))
        assert sorted((len(support_a), len(support_b))) == [1, 2]
        boundary_supports.append((support_a, support_b))

    # Rank two with delta nonzero and three distinct collinear ratio points.
    za_divisor = sp.Matrix([2, 3, 4])
    xb_divisor = sp.Matrix([sp.Rational(-2), sp.Rational(-3, 2), sp.Rational(-4, 3)])
    rank_two_nonzero = sp.Matrix.hstack(
        one,
        hadamard(za_divisor, xb_divisor),
        xb_divisor - za_divisor,
    )
    assert rank_two_nonzero.rank() == 2
    divisor_points = tuple(
        (
            za_divisor[index] * xb_divisor[index],
            xb_divisor[index] - za_divisor[index],
        )
        for index in range(3)
    )
    assert len(set(divisor_points)) == 3
    assert all(left == right for left, right in divisor_points)

    return {
        "full_frame_rank": full.rank(),
        "full_frame_determinant": int(full.det()),
        "delta_zero_divisor_rank": rank_two_delta_zero.rank(),
        "nonzero_delta_divisor_rank": rank_two_nonzero.rank(),
        "rank_one_ratio_pairs": [
            [int(first), int(second)] for first, second in ratio_pairs
        ],
        "rank_one_base_parameters": ["-1", "-1/2"],
        "rank_one_base_supports": [
            [list(support_a), list(support_b)]
            for support_a, support_b in boundary_supports
        ],
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero structural classification",
        "Quotient-zero surface",
        "Quotient-rank-one conic or rulings",
        "rank frame=1  <=> P_0=P_1=P_2",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "SIX_BLOCKER_ORDER12_ISOTROPIC_P6_CURVE.md",
        "SIX_BLOCKER_MAXIMAL_OVERLAP_GHZ_HYPERCUBE.md",
    ):
        assert (ROOT / dependency).exists()

    quotient_and_conic_normal_forms()
    symbolic_frame_identity()
    universal_rank_boundary_checks()
    examples = frame_examples()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "quotient_rank_possibilities": [0, 1],
                "rank_one_diagonal_locus": "cross-form isotropic hyperplane",
                "frame_examples": examples,
                "delta_zero_frame_rank_one_possible": False,
                "nonzero_delta_frame_rank_one_type": "2+1 ratio-pair collision",
                "rank_one_linear_coefficient_B_may_vanish": True,
                "arbitrary_ambient_order_claimed": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
