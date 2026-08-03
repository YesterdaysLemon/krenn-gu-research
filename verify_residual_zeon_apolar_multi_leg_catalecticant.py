"""Verify the residual zeon-apolar multi-leg catalecticant theorem.

This is a fixed symbolic replay of arbitrary-order identities, not a search.
"""

from functools import cache
from itertools import combinations
from math import comb

import sympy as sp


def permanent(matrix: sp.Matrix):
    assert matrix.rows == matrix.cols
    size = matrix.rows
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in range(size):
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column in range(size):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                next_states[new_mask] = (
                    next_states.get(new_mask, 0)
                    + coefficient * matrix[row, column]
                )
        states = next_states
    return sp.expand(states[(1 << size) - 1])


def hafnian(matrix: sp.Matrix):
    assert matrix.rows == matrix.cols
    size = matrix.rows

    @cache
    def recurrence(vertices: tuple[int, ...]):
        if not vertices:
            return sp.Integer(1)
        if len(vertices) % 2:
            return sp.Integer(0)
        first = vertices[0]
        total = sp.Integer(0)
        for position in range(1, len(vertices)):
            second = vertices[position]
            remainder = vertices[1:position] + vertices[position + 1 :]
            total += matrix[first, second] * recurrence(remainder)
        return sp.expand(total)

    return recurrence(tuple(range(size)))


def phi_coefficient(
    residual: sp.Matrix, incidence: sp.Matrix, ports: tuple[int, ...]
):
    residual_order = residual.rows
    degree = len(ports)
    if degree % 2 or degree > residual_order:
        return sp.Integer(0)
    total = sp.Integer(0)
    for used_rows in combinations(range(residual_order), degree):
        unused_rows = tuple(
            row for row in range(residual_order) if row not in used_rows
        )
        cofactor = hafnian(residual.extract(unused_rows, unused_rows))
        compound = permanent(incidence.extract(used_rows, ports))
        total += cofactor * compound
    return sp.expand(total)


def permanental_compound(
    incidence: sp.Matrix,
    row_order: int,
    port_subsets: tuple[tuple[int, ...], ...],
):
    residual_subsets = tuple(combinations(range(incidence.rows), row_order))
    return sp.Matrix(
        [
            [permanent(incidence.extract(rows, ports)) for ports in port_subsets]
            for rows in residual_subsets
        ]
    )


def check_symbolic_q4_k2_factorization() -> None:
    residual_order = 4
    residual = sp.zeros(residual_order)
    for first, second in combinations(range(residual_order), 2):
        value = sp.symbols(f"a{first}{second}")
        residual[first, second] = residual[second, first] = value

    left = sp.Matrix(residual_order, 3, sp.symbols("l0:12"))
    right = sp.Matrix(residual_order, 3, sp.symbols("v0:12"))
    incidence = left.row_join(right)
    left_pairs = tuple(combinations(range(3), 2))
    right_columns = ((),) + tuple(combinations(range(3, 6), 2))

    catalecticant = sp.Matrix(
        [
            [phi_coefficient(residual, incidence, left_pair + right_set)
             for right_set in right_columns]
            for left_pair in left_pairs
        ]
    )

    residual_pairs = tuple(combinations(range(residual_order), 2))
    p_two = permanental_compound(incidence[:, :3], 2, left_pairs)
    middle = sp.zeros(len(residual_pairs), len(right_columns))
    for row_index, marked_rows in enumerate(residual_pairs):
        complement = tuple(
            row for row in range(residual_order) if row not in marked_rows
        )
        middle[row_index, 0] = hafnian(
            residual.extract(complement, complement)
        )
        for column_index, right_set in enumerate(right_columns[1:], start=1):
            middle[row_index, column_index] = permanent(
                incidence.extract(complement, right_set)
            )

    difference = catalecticant - p_two.T * middle
    assert all(sp.expand(entry) == 0 for entry in difference)
    assert p_two.rows == comb(residual_order, 2)


def check_symmetric_square_refinement() -> None:
    residual_order = 4
    incidence_rank = 2
    port_count = 4
    source = sp.Matrix(
        residual_order,
        incidence_rank,
        sp.symbols("u0:8"),
    )
    coordinates = sp.Matrix(
        incidence_rank,
        port_count,
        sp.symbols("c0:8"),
    )
    incidence = source * coordinates
    residual_pairs = tuple(combinations(range(residual_order), 2))
    port_pairs = tuple(combinations(range(port_count), 2))
    p_two = permanental_compound(incidence, 2, port_pairs)

    source_square = sp.zeros(len(residual_pairs), 3)
    for row_index, (first, second) in enumerate(residual_pairs):
        source_square[row_index, 0] = source[first, 0] * source[second, 0]
        source_square[row_index, 1] = (
            source[first, 0] * source[second, 1]
            + source[first, 1] * source[second, 0]
        )
        source_square[row_index, 2] = source[first, 1] * source[second, 1]

    coordinate_square = sp.zeros(3, len(port_pairs))
    for column_index, (first, second) in enumerate(port_pairs):
        coordinate_square[0, column_index] = (
            2 * coordinates[0, first] * coordinates[0, second]
        )
        coordinate_square[1, column_index] = (
            coordinates[0, first] * coordinates[1, second]
            + coordinates[1, first] * coordinates[0, second]
        )
        coordinate_square[2, column_index] = (
            2 * coordinates[1, first] * coordinates[1, second]
        )

    difference = p_two - source_square * coordinate_square
    assert all(sp.expand(entry) == 0 for entry in difference)
    assert source_square.cols == comb(incidence_rank + 1, 2)


def check_doubled_identity_sharpness() -> None:
    residual_order = 4
    identity = sp.eye(residual_order)
    incidence = identity.row_join(identity)
    for marked_order in range(residual_order + 1):
        left_sets = tuple(combinations(range(residual_order), marked_order))
        right_order = residual_order - marked_order
        right_sets_local = tuple(combinations(range(residual_order), right_order))
        top_block = sp.Matrix(
            [
                [
                    permanent(
                        incidence.extract(
                            range(residual_order),
                            left_set
                            + tuple(residual_order + index for index in right_set),
                        )
                    )
                    for right_set in right_sets_local
                ]
                for left_set in left_sets
            ]
        )
        expected = sp.zeros(comb(residual_order, marked_order))
        for row_index, left_set in enumerate(left_sets):
            complement = tuple(
                index for index in range(residual_order) if index not in left_set
            )
            expected[row_index, right_sets_local.index(complement)] = 1
        assert top_block == expected
        assert top_block.rank() == comb(residual_order, marked_order)


def main() -> None:
    check_symbolic_q4_k2_factorization()
    check_symmetric_square_refinement()
    check_doubled_identity_sharpness()
    print("PASS: symbolic q=4 k=2 all-depth catalecticant factorization")
    print("PASS: rank-two incidence factors through its three-dimensional Sym^2")
    print("PASS: doubled identity attains every q=4 binomial catalecticant bound")
    print("SCOPE: legal P5/P6/P7 synchronized deletion observability remains unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
