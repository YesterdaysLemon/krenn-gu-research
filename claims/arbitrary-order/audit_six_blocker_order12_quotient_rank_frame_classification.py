#!/usr/bin/env python3
"""Independent no-import audit of the quotient-rank frame classification."""

from __future__ import annotations

import json
from fractions import Fraction

import sympy as sp

Vector = tuple[Fraction, Fraction, Fraction]


def vector(*entries: int | Fraction) -> Vector:
    return tuple(Fraction(entry) for entry in entries)  # type: ignore[return-value]


def product(left: Vector, right: Vector) -> Vector:
    return tuple(a * b for a, b in zip(left, right))  # type: ignore[return-value]


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right))  # type: ignore[return-value]


def scale(value: Fraction, row: Vector) -> Vector:
    return tuple(value * entry for entry in row)  # type: ignore[return-value]


def determinant(columns: tuple[Vector, Vector, Vector]) -> Fraction:
    matrix = tuple(zip(*columns))
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def rational_rank(columns: tuple[Vector, ...]) -> int:
    return int(sp.Matrix(tuple(zip(*columns))).rank())


def audit_frame(
    xa: Vector,
    za: Vector,
    xb: Vector,
    zb: Vector,
    beta: Fraction,
    delta: Fraction,
) -> dict[str, object]:
    v01 = product(xa, zb)
    v10 = product(za, xb)
    middle = subtract(scale(delta, product(xa, xb)), scale(beta, product(za, zb)))
    columns = (v01, v10, middle)
    theta = determinant(columns)
    rank = rational_rank(columns)

    ratio_points = []
    normalized_rows = []
    p_product = Fraction(1)
    for colour in range(3):
        r = za[colour] / xa[colour]
        s = xb[colour] / zb[colour]
        point = (r * s, delta * s - beta * r)
        ratio_points.append(point)
        normalized_rows.append((Fraction(1), *point))
        p_product *= xa[colour] * zb[colour]
    normalized_det = determinant(tuple(zip(*normalized_rows)))  # type: ignore[arg-type]
    assert theta == p_product * normalized_det
    assert rank == rational_rank(tuple(zip(*normalized_rows)))  # type: ignore[arg-type]
    return {
        "rank": rank,
        "theta": str(theta),
        "ratio_points": [[str(item) for item in point] for point in ratio_points],
    }


def quotient_kernel_audit() -> None:
    beta, delta = Fraction(5), Fraction(7)
    q = sp.Matrix([[beta, 0, 0, delta]])
    kernel = sp.Matrix(
        [
            [0, 0, delta],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, -beta],
        ]
    )
    assert q.rank() == 1
    assert kernel.rank() == 3
    assert q * kernel == sp.zeros(1, 3)

    # A nonzero quotient cofactor multiplies q and has the same kernel; a
    # zero quotient cofactor gives the zero map on all four dimensions.
    nonzero_map = Fraction(-11) * q
    zero_map = sp.zeros(1, 4)
    assert nonzero_map.rank() == 1
    assert nonzero_map.nullspace() == q.nullspace()
    assert zero_map.rank() == 0
    assert len(zero_map.nullspace()) == 4


def universal_boundary_audit() -> None:
    beta, delta, a_value, b_value, r = sp.symbols("beta delta A B r")
    r0, r1 = sp.symbols("r0 r1")
    delta_zero_minor = sp.Matrix([[1, -beta * r0], [1, -beta * r1]]).det()
    assert sp.expand(delta_zero_minor - beta * (r0 - r1)) == 0
    eliminated = sp.together((delta * a_value / r - beta * r - b_value) * r)
    assert sp.expand(eliminated + beta * r**2 + b_value * r - delta * a_value) == 0

    # Independent exact B=0 rank-one realization with two ratio values.
    b_zero = audit_frame(
        vector(1, 1, 1),
        vector(1, 1, -1),
        vector(1, 1, -1),
        vector(1, 1, 1),
        Fraction(1),
        Fraction(1),
    )
    assert b_zero["rank"] == 1
    assert b_zero["ratio_points"] == [["1", "0"]] * 3


def main() -> None:
    quotient_kernel_audit()
    universal_boundary_audit()
    one = vector(1, 1, 1)
    full = audit_frame(
        one,
        vector(1, 2, 3),
        vector(2, 3, 5),
        vector(3, 5, 7),
        Fraction(1),
        Fraction(2),
    )
    assert full["rank"] == 3 and full["theta"] == "69"

    delta_zero = audit_frame(
        one,
        vector(1, 1, 2),
        one,
        vector(1, 1, 2),
        Fraction(1),
        Fraction(0),
    )
    assert delta_zero["rank"] == 2

    rank_one = audit_frame(
        one,
        vector(1, 1, 2),
        vector(-2, -2, -1),
        one,
        Fraction(1),
        Fraction(1),
    )
    assert rank_one["rank"] == 1
    assert rank_one["ratio_points"] == [["-2", "-3"]] * 3

    # Independently reconstruct the two common-quadratic base points.
    rank_one_r = vector(1, 1, 2)
    rank_one_s = vector(-2, -2, -1)
    common_quadratics = []
    for r, s in zip(rank_one_r, rank_one_s):
        # Coefficients of (1+r*t)(s*t-1), low degree first.
        common_quadratics.append((Fraction(-1), s - r, r * s))
    assert len(set(common_quadratics)) == 1
    assert common_quadratics[0] == (Fraction(-1), Fraction(-3), Fraction(-2))
    for parameter in (Fraction(-1), Fraction(-1, 2)):
        first = tuple(Fraction(1) + parameter * r for r in rank_one_r)
        second = tuple(parameter * s - Fraction(1) for s in rank_one_s)
        assert product(first, second) == vector(0, 0, 0)
        supports = (
            {index for index, value in enumerate(first) if value},
            {index for index, value in enumerate(second) if value},
        )
        assert supports[0].isdisjoint(supports[1])
        assert supports[0] | supports[1] == set(range(3))
        assert sorted(map(len, supports)) == [1, 2]

    rank_two = audit_frame(
        one,
        vector(2, 3, 4),
        vector(Fraction(-2), Fraction(-3, 2), Fraction(-4, 3)),
        one,
        Fraction(1),
        Fraction(1),
    )
    assert rank_two["rank"] == 2
    assert len({tuple(point) for point in rank_two["ratio_points"]}) == 3

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "no-import rational quotient and ratio geometry",
                "field": "rational characteristic zero",
                "full_frame": full,
                "delta_zero_divisor": delta_zero,
                "rank_one_collision": rank_one,
                "rank_two_collinear": rank_two,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
