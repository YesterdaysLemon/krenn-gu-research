"""Independent Fraction audit for the GLS24 one-probe marginal reduction.

This file imports neither the primary verifier nor repository mathematics code.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


Q = Fraction


def rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                entry - factor * base
                for entry, base in zip(matrix[index], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*matrix)]


def multiply(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def outer(left: list[Fraction], right: list[Fraction]) -> list[list[Fraction]]:
    return [[a * b for b in right] for a in left]


def flatten(matrix: list[list[Fraction]]) -> list[Fraction]:
    return [entry for row in matrix for entry in row]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right))


def evaluation(x0: list[Fraction], x1: list[Fraction]) -> list[Fraction]:
    return [a * b for a in x0 for b in x1]


def transverse_basis(
    x0: list[Fraction], x1: list[Fraction]
) -> list[list[Fraction]]:
    epsilon = evaluation(x0, x1)
    pivot = epsilon[0]
    assert pivot
    columns = []
    for index in range(1, 9):
        vector = [Q(0) for _ in range(9)]
        vector[index] = Q(1)
        vector[0] = -epsilon[index] / pivot
        assert dot(epsilon, vector) == 0
        columns.append(vector)
    return columns


def rho0(x0: list[Fraction], tensor: list[Fraction]) -> list[Fraction]:
    return [
        sum(x0[a] * tensor[3 * a + b] for a in range(3))
        for b in range(3)
    ]


def rho1(x1: list[Fraction], tensor: list[Fraction]) -> list[Fraction]:
    return [
        sum(tensor[3 * a + b] * x1[b] for b in range(3))
        for a in range(3)
    ]


def wedge(u: list[Fraction], v: list[Fraction]) -> list[Fraction]:
    return [
        u[0] * v[1] - u[1] * v[0],
        u[0] * v[2] - u[2] * v[0],
        u[1] * v[2] - u[2] * v[1],
    ]


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    return rank(matrix)


def check_sequences_and_trichotomy() -> dict[str, int]:
    x0 = [Q(1), Q(1), Q(1)]
    x1 = [Q(1), Q(2), Q(3)]
    basis = transverse_basis(x0, x1)
    assert rank(basis) == 8

    marginal0 = [rho0(x0, column) for column in basis]
    marginal1 = [rho1(x1, column) for column in basis]
    assert rank(marginal0) == rank(marginal1) == 2
    assert all(dot(x1, value) == 0 for value in marginal0)
    assert all(dot(x0, value) == 0 for value in marginal1)

    raw = [
        [Q(1), Q(0), Q(2)],
        [Q(2), Q(-1), Q(1)],
        [Q(0), Q(3), Q(1)],
    ]
    value = sum(x0[a] * raw[a][b] * x1[b] for a in range(3) for b in range(3))
    raw[0][0] -= value
    omega = flatten(raw)
    assert dot(evaluation(x0, x1), omega) == 0
    u0 = rho0(x0, omega)
    u1 = rho1(x1, omega)
    assert any(u0) or any(u1)
    mu_columns = [wedge(u0, value) for value in marginal0]
    assert rank(mu_columns) == 1
    assert not any(wedge(u0, u0))

    l0 = [[Q(-1), Q(1), Q(0)], [Q(-1), Q(0), Q(1)]]
    l1 = [[Q(-2), Q(1), Q(0)], [Q(-3), Q(0), Q(1)]]
    rank_one = outer(l0[0], l1[0])
    rank_two = [
        [rank_one[a][b] + l0[1][a] * l1[1][b] for b in range(3)]
        for a in range(3)
    ]
    for matrix, expected in ((rank_one, 1), (rank_two, 2)):
        assert matrix_rank(matrix) == expected
        vector = flatten(matrix)
        assert not any(rho0(x0, vector))
        assert not any(rho1(x1, vector))

    return {
        "transverse_columns": len(basis),
        "rho_rank": rank(marginal0),
        "rho_kernel": len(basis) - rank(marginal0),
        "wedge_rank": rank(mu_columns),
        "wedge_kernel": len(basis) - rank(mu_columns),
        "double_core_rank_one": matrix_rank(rank_one),
        "double_core_rank_two": matrix_rank(rank_two),
    }


def check_slice_and_aggregate() -> dict[str, int]:
    x0 = [Q(1), Q(1), Q(1)]
    x1 = [Q(1), Q(2), Q(3)]
    basis = transverse_basis(x0, x1)

    omega_matrix = [
        [Q(-15), Q(0), Q(2)],
        [Q(2), Q(-1), Q(1)],
        [Q(0), Q(3), Q(1)],
    ]
    omega = flatten(omega_matrix)
    correction = dot(evaluation(x0, x1), omega)
    omega[0] -= correction
    assert dot(evaluation(x0, x1), omega) == 0
    u = rho0(x0, omega)
    assert any(u)

    def mu(vector: list[Fraction]) -> list[Fraction]:
        return wedge(u, rho0(x0, vector))

    assert not any(mu(omega))
    mapped_basis = [mu(column) for column in basis]
    assert rank(mapped_basis) == 1

    labelled = []
    for first in range(2):
        row = []
        for second in range(2):
            coefficients = [
                Q(first + 1),
                Q(second + 2),
                Q(first - second),
                Q(1),
                Q(0),
                Q(-1),
                Q(2),
                Q(1),
            ]
            vector = [Q(0) for _ in range(9)]
            for scalar, column in zip(coefficients, basis):
                vector = [a + scalar * b for a, b in zip(vector, column)]
            row.append(vector)
        labelled.append(row)
    eta = [Q(3), Q(-2)]
    for first in range(2):
        sliced = [
            sum(eta[second] * labelled[first][second][entry] for second in range(2))
            for entry in range(9)
        ]
        image_first = mu(sliced)
        image_second = [
            sum(eta[second] * mu(labelled[first][second])[entry] for second in range(2))
            for entry in range(3)
        ]
        assert image_first == image_second

    synchronized = [omega, [Q(2) * value for value in omega]]
    assert all(not any(mu(column)) for column in synchronized)
    escape = next(column for column in basis if any(mu(column)))
    nonsynchronized = synchronized + [escape]
    assert any(any(mu(column)) for column in nonsynchronized)

    return {
        "labelled_slice_tensors": 4,
        "root_image_rank": rank(mapped_basis),
        "pair_image_rows": rank(mapped_basis) * 9,
        "synchronized_columns": len(synchronized),
        "escape_columns": len(nonsynchronized),
    }


def check_rank_rise_states() -> dict[str, int]:
    states = 0
    rises = 0
    for nuisance_mask in product((0, 1), repeat=3):
        nuisance_columns = [
            [Q(1 if row == column else 0) for row in range(3)]
            for column, active in enumerate(nuisance_mask)
            if active
        ]
        nuisance_rank = rank(nuisance_columns)
        for desired in range(3):
            column = [Q(1 if row == desired else 0) for row in range(3)]
            augmented_rank = rank(nuisance_columns + [column])
            expected = nuisance_mask[desired] == 0
            assert (augmented_rank > nuisance_rank) == expected
            states += 1
            rises += int(expected)
    return {"exact_states": states, "rank_rises": rises}


def check_r3_window() -> dict[str, int]:
    ports = frozenset(range(4))
    complements = [frozenset(pair) for pair in combinations(ports, 2)]
    responses = {ports - complement for complement in complements}
    assert len(complements) == len(responses) == 6
    assert all(len(response) == 2 for response in responses)
    return {
        "pair_complements": len(complements),
        "distinct_pair_responses": len(responses),
        "top_response": 1,
        "nine_row_pair_modules": 6,
    }


def main() -> None:
    sequences = check_sequences_and_trichotomy()
    slicing = check_slice_and_aggregate()
    ranks = check_rank_rise_states()
    window = check_r3_window()
    print("promoted one-probe anchor-marginal independent audit: PASS")
    print(f"  independently derived exact sequences/trichotomy: {sequences}")
    print(f"  direct slice and aggregate checks: {slicing}")
    print(f"  exhaustive small rank-rise states: {ranks}")
    print(f"  independent root-order-three window count: {window}")
    print("  no imports from primary verifier or repository mathematics code")
    print("  scope: marginal route only; survival, activity, and closure open")


if __name__ == "__main__":
    main()
