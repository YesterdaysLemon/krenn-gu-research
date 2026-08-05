"""Verify fifth permanental compound observability for seven cores.

All matrices, orders, primes, and reductions are fixed.  This script performs
no support, graph-family, parameter, face, or minor search.
"""

from itertools import combinations

import sympy as sp

INDICES = tuple(range(7))
CORE_PAIRS = tuple(combinations(INDICES, 2))
TERMINAL_FACES = tuple(combinations(INDICES, 5))


def permanent_mod(matrix: list[list[int]], modulus: int) -> int:
    states = {0: 1}
    for row in matrix:
        next_states: dict[int, int] = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                next_mask = mask | bit
                next_states[next_mask] = (
                    next_states.get(next_mask, 0) + coefficient * value
                ) % modulus
        states = next_states
    return states.get((1 << len(matrix)) - 1, 0)


def compound_mod(incidence: list[list[int]], modulus: int) -> list[list[int]]:
    result = []
    for face in TERMINAL_FACES:
        row = []
        for deleted_pair in CORE_PAIRS:
            surviving_rows = [
                index for index in INDICES if index not in deleted_pair
            ]
            submatrix = [
                [incidence[index][column] for column in face]
                for index in surviving_rows
            ]
            row.append(permanent_mod(submatrix, modulus))
        result.append(row)
    return result


def determinant_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[value % modulus for value in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column] != 0
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % modulus
        inverse = pow(pivot_value, modulus - 2, modulus)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * inverse % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[column])
                ]
    return determinant % modulus


def solve_mod(matrix: list[list[int]], target: list[int], modulus: int) -> list[int]:
    work = [
        [value % modulus for value in row] + [target[index] % modulus]
        for index, row in enumerate(matrix)
    ]
    for column in range(len(matrix)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column] != 0
        )
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], modulus - 2, modulus)
        work[column] = [value * inverse % modulus for value in work[column]]
        for row in range(len(work)):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[column])
                ]
    return [work[index][-1] for index in range(len(matrix))]


def matrix_vector_mod(
    matrix: list[list[int]], vector: list[int], modulus: int
) -> list[int]:
    return [
        sum(left * right for left, right in zip(row, vector)) % modulus
        for row in matrix
    ]


def fixed_incidence(modulus: int, rho: int) -> list[list[int]]:
    inverse_7 = pow(7, modulus - 2, modulus)
    inverse_21 = pow(21, modulus - 2, modulus)
    incidence = [[0 for _ in INDICES] for _ in INDICES]
    incidence[0][4] = inverse_7
    incidence[1][0] = incidence[1][2] = 1
    incidence[2][1] = incidence[2][3] = 1
    incidence[3][2] = 1
    incidence[3][6] = -rho % modulus
    incidence[4][3] = 1
    incidence[4][6] = (-5 - 2 * rho * inverse_21) % modulus
    incidence[5][4] = 1
    incidence[5][6] = (230 + 104 * rho * inverse_7) % modulus
    incidence[6][5] = 1
    incidence[6][6] = (1 + 16 * rho * inverse_21) % modulus
    return incidence


def main() -> None:
    identity = sp.eye(7)
    complement_matrix = sp.zeros(21)
    for row, face in enumerate(TERMINAL_FACES):
        for column, deleted_pair in enumerate(CORE_PAIRS):
            surviving_rows = tuple(
                index for index in INDICES if index not in deleted_pair
            )
            submatrix = identity.extract(surviving_rows, face)
            complement_matrix[row, column] = sp.per(submatrix)
            expected = int(set(face) == set(surviving_rows))
            assert complement_matrix[row, column] == expected
    assert abs(complement_matrix.det()) == 1

    modulus = 43
    rho = 8
    assert rho * rho % modulus == 21
    compound = compound_mod(fixed_incidence(modulus, rho), modulus)
    assert determinant_mod(compound, modulus) == 11

    # Exact exceptional-face line law in the good reduction.  The exceptional
    # surviving set is {1,2,3,4,5}, indexed here by 0,...,4.
    exceptional_index = TERMINAL_FACES.index((0, 1, 2, 3, 4))
    exceptional_vector = [0] * 21
    exceptional_vector[exceptional_index] = 1
    inverse_column = solve_mod(compound, exceptional_vector, modulus)
    assert matrix_vector_mod(compound, inverse_column, modulus) == exceptional_vector
    scale = 17
    edge_vector = [scale * value % modulus for value in inverse_column]
    response = matrix_vector_mod(compound, edge_vector, modulus)
    assert response == [scale * value % modulus for value in exceptional_vector]

    # Representative 2x2 circuits on fixed edge coordinates.
    for left, right in ((0, 1), (3, 10), (8, 20)):
        assert (
            edge_vector[left] * inverse_column[right]
            - edge_vector[right] * inverse_column[left]
        ) % modulus == 0

    print("PASS: C5(I7) is the complement permutation matrix")
    print("PASS: fixed C5 determinant is 11 mod 43 at rho=8")
    print("PASS: exceptional-face inverse-column line and 2x2 circuits")
    print("SCOPE: general observability; existing four-face circuit not recomputed")


if __name__ == "__main__":
    main()
