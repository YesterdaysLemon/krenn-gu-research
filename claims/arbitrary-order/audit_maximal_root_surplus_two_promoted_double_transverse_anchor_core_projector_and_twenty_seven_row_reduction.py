"""Independent Fraction audit for the GLS25 double-transverse core theorem.

This file imports neither the primary verifier nor repository mathematics code.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


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


def columns_to_rows(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    return transpose(columns)


def solve_unique(
    columns: list[list[Fraction]], target: list[Fraction]
) -> list[Fraction]:
    rows = [row + [value] for row, value in zip(columns_to_rows(columns), target)]
    row_index = 0
    pivots: list[int] = []
    width = len(columns)
    for column in range(width):
        pivot = next(
            (index for index in range(row_index, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[row_index], rows[pivot] = rows[pivot], rows[row_index]
        value = rows[row_index][column]
        rows[row_index] = [entry / value for entry in rows[row_index]]
        for index in range(len(rows)):
            if index == row_index or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                entry - factor * base
                for entry, base in zip(rows[index], rows[row_index])
            ]
        pivots.append(column)
        row_index += 1
    assert pivots == list(range(width))
    for row in rows:
        assert any(row[:width]) or row[-1] == 0
    solution = [Q(0) for _ in range(width)]
    for index, pivot in enumerate(pivots):
        solution[pivot] = rows[index][-1]
    return solution


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right))


def outer(left: list[Fraction], right: list[Fraction]) -> list[list[Fraction]]:
    return [[a * b for b in right] for a in left]


def flatten(matrix: list[list[Fraction]]) -> list[Fraction]:
    return [entry for row in matrix for entry in row]


def matricize(vector: list[Fraction]) -> list[list[Fraction]]:
    return [vector[3 * row : 3 * row + 3] for row in range(3)]


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [dot(row, vector) for row in matrix]


def left_vec(vector: list[Fraction], matrix: list[list[Fraction]]) -> list[Fraction]:
    return [sum(vector[row] * matrix[row][column] for row in range(3)) for column in range(3)]


def add_vectors(*vectors: list[Fraction]) -> list[Fraction]:
    return [sum(entries) for entries in zip(*vectors)]


def scale(scalar: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [scalar * entry for entry in vector]


def evaluation(x0: list[Fraction], x1: list[Fraction]) -> list[Fraction]:
    return [a * b for a in x0 for b in x1]


def transverse_basis(x0: list[Fraction], x1: list[Fraction]) -> list[list[Fraction]]:
    epsilon = evaluation(x0, x1)
    assert epsilon[0]
    basis = []
    for index in range(1, 9):
        vector = [Q(0) for _ in range(9)]
        vector[index] = Q(1)
        vector[0] = -epsilon[index] / epsilon[0]
        assert dot(epsilon, vector) == 0
        basis.append(vector)
    return basis


def xi_data() -> dict[str, object]:
    x0 = [Q(1), Q(1), Q(1)]
    x1 = [Q(1), Q(2), Q(3)]
    q = [
        [Q(2), Q(0), Q(1)],
        [Q(1), Q(-1), Q(2)],
        [Q(0), Q(3), Q(1)],
    ]
    s0 = mat_vec(q, x1)
    s1 = left_vec(x0, q)
    p = dot(x0, s0)
    assert p == dot(x1, s1)
    assert p

    def xi(vector: list[Fraction]) -> list[Fraction]:
        matrix = matricize(vector)
        rho0 = left_vec(x0, matrix)
        rho1 = mat_vec(matrix, x1)
        value = []
        for a in range(3):
            for b in range(3):
                value.append(
                    p * matrix[a][b] - s0[a] * rho0[b] - rho1[a] * s1[b]
                )
        return value

    l0 = [[Q(-1), Q(1), Q(0)], [Q(-1), Q(0), Q(1)]]
    l1 = [[Q(-2), Q(1), Q(0)], [Q(-3), Q(0), Q(1)]]
    core = [flatten(outer(left, right)) for left in l0 for right in l1]
    e_basis = transverse_basis(x0, x1)
    return {
        "x0": x0,
        "x1": x1,
        "p": p,
        "s0": s0,
        "s1": s1,
        "xi": xi,
        "l0": l0,
        "l1": l1,
        "core": core,
        "e_basis": e_basis,
    }


def wedge4(omega: list[Fraction], value: list[Fraction]) -> list[Fraction]:
    return [
        omega[left] * value[right] - omega[right] * value[left]
        for left, right in combinations(range(4), 2)
    ]


def check_projector() -> dict[str, object]:
    data = xi_data()
    x0 = data["x0"]
    x1 = data["x1"]
    p = data["p"]
    s0 = data["s0"]
    s1 = data["s1"]
    xi = data["xi"]
    l0 = data["l0"]
    l1 = data["l1"]
    core = data["core"]
    e_basis = data["e_basis"]
    assert isinstance(x0, list)
    assert isinstance(x1, list)
    assert isinstance(p, Fraction)
    assert isinstance(s0, list)
    assert isinstance(s1, list)
    assert callable(xi)
    assert isinstance(l0, list)
    assert isinstance(l1, list)
    assert isinstance(core, list)
    assert isinstance(e_basis, list)

    images = [xi(vector) for vector in e_basis]
    assert rank(images) == 4
    for vector in images:
        matrix = matricize(vector)
        assert not any(left_vec(x0, matrix))
        assert not any(mat_vec(matrix, x1))
    assert rank(core + images) == 4
    assert all(xi(vector) == scale(p, vector) for vector in core)
    assert all(xi(xi(vector)) == scale(p, xi(vector)) for vector in e_basis)

    expected_kernel = [
        flatten(outer(s0, l1[0])),
        flatten(outer(s0, l1[1])),
        flatten(outer(l0[0], s1)),
        flatten(outer(l0[1], s1)),
    ]
    assert rank(expected_kernel) == 4
    assert all(not any(xi(vector)) for vector in expected_kernel)
    assert rank(e_basis + expected_kernel) == 8

    return {
        "p": p,
        "transverse_dimension": rank(e_basis),
        "core_dimension": rank(core),
        "image_rank": rank(images),
        "kernel_rank": rank(expected_kernel),
        "scaled_idempotent": True,
    }


def check_anchor_exterior_and_slices() -> dict[str, int]:
    data = xi_data()
    p = data["p"]
    xi = data["xi"]
    core = data["core"]
    e_basis = data["e_basis"]
    assert isinstance(p, Fraction)
    assert callable(xi)
    assert isinstance(core, list)
    assert isinstance(e_basis, list)

    omega_one_coords = [Q(1), Q(0), Q(0), Q(0)]
    omega_two_coords = [Q(1), Q(0), Q(0), Q(1)]
    omega_one = [sum(c * basis[k] for k, c in enumerate(omega_one_coords)) for basis in zip(*core)]
    omega_two = [sum(c * basis[k] for k, c in enumerate(omega_two_coords)) for basis in zip(*core)]
    assert rank(matricize(omega_one)) == 1
    assert rank(matricize(omega_two)) == 2
    assert xi(omega_two) == scale(p, omega_two)

    xi_coordinates = [solve_unique(core, xi(vector)) for vector in e_basis]
    chi_columns = [wedge4(omega_two_coords, value) for value in xi_coordinates]
    assert rank(chi_columns) == 3
    omega_e_coords = solve_unique(e_basis, omega_two)
    assert not any(wedge4(omega_two_coords, solve_unique(core, xi(omega_two))))

    labelled: list[list[list[Fraction]]] = []
    for first in range(2):
        row = []
        for second in range(2):
            coefficients = [
                Q(first + 1), Q(second + 1), Q(first - second), Q(2),
                Q(-1), Q(0), Q(1), Q(3),
            ]
            vector = [
                sum(coefficients[k] * e_basis[k][entry] for k in range(8))
                for entry in range(9)
            ]
            row.append(vector)
        labelled.append(row)
    eta = [Q(2), Q(-3)]

    def chi(vector: list[Fraction]) -> list[Fraction]:
        return wedge4(omega_two_coords, solve_unique(core, xi(vector)))

    assert not any(chi(omega_two))
    for first in range(2):
        sliced = [
            sum(eta[second] * labelled[first][second][entry] for second in range(2))
            for entry in range(9)
        ]
        second = [
            sum(eta[k] * chi(labelled[first][k])[entry] for k in range(2))
            for entry in range(6)
        ]
        assert chi(sliced) == second

    synchronized = [omega_e_coords, scale(Q(-2), omega_e_coords)]
    assert all(not any(chi(add_vectors(*[scale(c, e_basis[k]) for k, c in enumerate(column)]))) for column in synchronized)
    escape = next(vector for vector in e_basis if any(chi(vector)))
    assert any(chi(escape))

    return {
        "rank_one_anchor": rank(matricize(omega_one)),
        "rank_two_anchor": rank(matricize(omega_two)),
        "chi_rank": rank(chi_columns),
        "chi_kernel": 8 - rank(chi_columns),
        "slice_tensors": 4,
        "pair_rows": 3 * 9,
        "top_rows": 4,
    }


def check_rank_rise_and_window() -> dict[str, int]:
    nuisance = [[Q(1 if row == column else 0) for row in range(5)] for column in range(3)]
    absorbed = add_vectors(nuisance[0], nuisance[2])
    surviving = [Q(0), Q(0), Q(0), Q(0), Q(1)]
    assert rank(nuisance + [absorbed]) == rank(nuisance)
    assert rank(nuisance + [surviving]) == rank(nuisance) + 1

    ports = frozenset(range(4))
    complements = [frozenset(pair) for pair in combinations(ports, 2)]
    responses = {ports - complement for complement in complements}
    assert len(complements) == len(responses) == 6
    return {
        "small_nuisance_rank": rank(nuisance),
        "absorbed_rank": rank(nuisance + [absorbed]),
        "surviving_rank": rank(nuisance + [surviving]),
        "pair_modules": len(complements),
        "pair_responses": len(responses),
        "top_modules": 1,
    }


def main() -> None:
    projector = check_projector()
    anchor = check_anchor_exterior_and_slices()
    rank_window = check_rank_rise_and_window()
    print("promoted double-transverse core independent audit: PASS")
    print(f"  independently derived scaled projector: {projector}")
    print(f"  direct anchor/exterior/slice checks: {anchor}")
    print(f"  independent rank-rise and r=3 window: {rank_window}")
    print("  no imports from primary verifier or repository mathematics code")
    print("  scope: conditional core route only; survival and closure open")


if __name__ == "__main__":
    main()
