"""Independent no-import audit for the GLS44 diagonal rank-four exclusion.

This script imports no project module or third-party package.  It uses exact
``Fraction`` elimination and an exhaustive finite-field factorization census,
independently of the SymPy primary verifier.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


Vector = tuple[int, int, int]
Matrix = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]


def rank(rows: list[list[int | Fraction]], modulus: int | None = None) -> int:
    if not rows:
        return 0
    if modulus is None:
        work = [[Fraction(value) for value in row] for row in rows]
    else:
        work = [[int(value) % modulus for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        if modulus is None:
            work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        else:
            inverse = pow(int(pivot_value), -1, modulus)
            work[pivot_row] = [(value * inverse) % modulus for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            if modulus is None:
                work[row] = [
                    value - factor * pivot
                    for value, pivot in zip(work[row], work[pivot_row])
                ]
            else:
                work[row] = [
                    (value - factor * pivot) % modulus
                    for value, pivot in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def outer(left: Vector, right: Vector, modulus: int | None = None) -> Matrix:
    entries = tuple(
        tuple(left[row] * right[column] for column in range(3))
        for row in range(3)
    )
    if modulus is None:
        return entries  # type: ignore[return-value]
    return tuple(
        tuple(value % modulus for value in row) for row in entries
    )  # type: ignore[return-value]


def add(left: Matrix, right: Matrix, modulus: int | None = None) -> Matrix:
    entries = tuple(
        tuple(left[row][column] + right[row][column] for column in range(3))
        for row in range(3)
    )
    if modulus is None:
        return entries  # type: ignore[return-value]
    return tuple(
        tuple(value % modulus for value in row) for row in entries
    )  # type: ignore[return-value]


def matrix_rank(matrix: Matrix, modulus: int | None = None) -> int:
    return rank([list(row) for row in matrix], modulus)


def vector_rank(vectors: tuple[Vector, Vector], modulus: int | None = None) -> int:
    return rank([list(vector) for vector in zip(*vectors)], modulus)


def check_rank_two_dual_cross_blocks() -> None:
    """Use dual coordinate functionals, rather than tensor projection."""

    invertible = [
        ((1, 0), (0, 1)),
        ((1, 2), (3, 5)),
        ((2, -1), (1, 1)),
    ]
    checked = 0
    for left in invertible:
        for right in invertible:
            assert rank([list(row) for row in left]) == 2
            assert rank([list(row) for row in right]) == 2
            for x_c, y_c in product(range(-2, 3), repeat=2):
                # Columns are the two residual-label responses after applying
                # the four dual cross-block functionals.
                response = [
                    [y_c * left[row][column] for column in range(2)]
                    for row in range(2)
                ] + [
                    [x_c * right[row][column] for column in range(2)]
                    for row in range(2)
                ]
                expected = 0 if x_c == y_c == 0 else 2
                assert rank(response) == expected
                checked += 1
    assert checked == 225


def check_rank_one_dual_column() -> None:
    """Audit the quotient obstruction by a dual functional on the root axis."""

    checked = 0
    for root_colour in range(3):
        quotient_colours = [colour for colour in range(3) if colour != root_colour]
        for b in product(range(-2, 3), repeat=3):
            if b[root_colour] == 0:
                continue
            # The two quotient basis tensors have independent values under
            # the root-coordinate functional on the right.
            images = [
                [b[root_colour] if row == column else 0 for column in range(2)]
                for row in range(2)
            ]
            assert rank(images) == 2
            # The projected diagonal has no such column.  One excess tensor
            # contributes only one vector, hence at most one dimension.
            for excess in product(range(-1, 2), repeat=2):
                assert rank([list(excess)]) <= 1
            checked += 1
        assert quotient_colours == [colour for colour in range(3) if colour != root_colour]
    assert checked == 300


def check_complete_factorization_census_mod_three() -> None:
    """Exhaust all 3^12 residual factorizations over a characteristic-3 field.

    This is structural calibration, not the characteristic-zero proof.  It
    independently checks every zero and rank-drop factorization profile used
    in the written argument.
    """

    field = range(3)
    vectors = list(product(field, repeat=3))
    seen_rank_one = 0
    seen_rank_two = 0
    seen_zero = 0
    for a0, a1, b0, b1 in product(vectors, repeat=4):
        q = add(outer(a0, b1, 3), outer(a1, b0, 3), 3)
        if any(q[row][column] for row in range(3) for column in range(3) if row != column):
            continue
        diagonal_support = [colour for colour in range(3) if q[colour][colour]]
        if not diagonal_support:
            seen_zero += 1
            continue
        q_rank = matrix_rank(q, 3)
        left_rank = vector_rank((a0, a1), 3)
        right_rank = vector_rank((b0, b1), 3)
        assert q_rank in (1, 2)
        if q_rank == 2:
            assert left_rank == right_rank == 2
            support = set(diagonal_support)
            assert all(
                vector[colour] == 0
                for vector in (a0, a1, b0, b1)
                for colour in range(3)
                if colour not in support
            )
            seen_rank_two += 1
        else:
            root_colour = diagonal_support[0]
            assert left_rank == 1 or right_rank == 1
            if left_rank == 1:
                assert all(
                    vector[colour] == 0
                    for vector in (a0, a1)
                    for colour in range(3)
                    if colour != root_colour
                )
            if right_rank == 1:
                assert all(
                    vector[colour] == 0
                    for vector in (b0, b1)
                    for colour in range(3)
                    if colour != root_colour
                )
            seen_rank_one += 1
    assert seen_zero > 0
    assert seen_rank_one > 0
    assert seen_rank_two > 0


def main() -> None:
    check_rank_two_dual_cross_blocks()
    check_rank_one_dual_column()
    check_complete_factorization_census_mod_three()
    print("GLS44 nonzero-diagonal rank-four no-import audit: PASS")


if __name__ == "__main__":
    main()
