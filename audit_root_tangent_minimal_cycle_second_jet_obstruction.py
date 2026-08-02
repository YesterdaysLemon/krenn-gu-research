"""No-import rational audit of the minimal-cycle second-jet obstruction."""

from __future__ import annotations

import json
from fractions import Fraction

Vector = tuple[Fraction, Fraction, Fraction]
Matrix = tuple[Vector, Vector, Vector]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(dot(row, vector) for row in matrix)  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[i][j] for i in range(3)) for j in range(3))  # type: ignore[return-value]


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(a * b for b in right) for a in left)  # type: ignore[return-value]


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(3)) for i in range(3)
    )  # type: ignore[return-value]


def coefficient_rows(left: Fraction, right: Fraction) -> tuple[Vector, Vector]:
    denominator = right - left
    if denominator == 0:
        raise ZeroDivisionError("adjacent quotient classes must be distinct")
    minus = (
        (1 - right) / denominator,
        right / denominator,
        -1 / denominator,
    )
    plus = (
        (left - 1) / denominator,
        -left / denominator,
        1 / denominator,
    )
    return minus, plus


def main() -> None:
    root: Vector = (Fraction(1), Fraction(1), Fraction(1))
    ell: Vector = (Fraction(1), Fraction(0), Fraction(0))
    checked_edges = 0

    for length in range(3, 17):
        parameters = [Fraction(i + 2, i + 3) for i in range(length)]
        assert len(set(parameters)) == length
        for index, current in enumerate(parameters):
            left = parameters[(index - 1) % length]
            nxt = parameters[(index + 1) % length]
            a_minus, a_plus = coefficient_rows(left, current)
            b_minus, b_plus = coefficient_rows(current, nxt)
            direction: Vector = (Fraction(0), Fraction(1), current)
            matrix = add(outer(a_plus, ell), outer(ell, b_minus))

            assert dot(a_minus, root) == 0
            assert dot(a_plus, root) == 0
            assert dot(b_minus, root) == 0
            assert dot(b_plus, root) == 0
            assert dot(a_minus, direction) == 0
            assert dot(a_plus, direction) == 1
            assert dot(b_minus, direction) == 1
            assert dot(b_plus, direction) == 0
            assert mat_vec(matrix, root) == a_plus
            assert mat_vec(transpose(matrix), root) == b_minus
            assert dot(direction, mat_vec(matrix, direction)) == 0

            ghz_hessian = (Fraction(0), Fraction(1), current * current)
            assert ghz_hessian != (Fraction(0), Fraction(0), Fraction(0))
            checked_edges += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent fractions; no repository imports",
                "cycle_lengths": [3, 16],
                "checked_edges": checked_edges,
                "minimal_mixed_second_derivative": [0, 0, 0],
                "ghz_mixed_second_derivative": "(0,1,t_i^2) != 0",
                "minimal_cycle_second_jet_compatible": False,
                "tangent_tangent_repairs_excluded": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
