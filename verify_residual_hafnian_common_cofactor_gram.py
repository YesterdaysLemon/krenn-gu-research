"""Primary verifier for the common residual-hafnian cofactor Gram theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def hafnian(matrix, vertices=None):
    if vertices is None:
        vertices = tuple(range(matrix.rows))
    vertices = tuple(vertices)
    if not vertices:
        return sp.Integer(1)
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first, second] * hafnian(matrix, rest)
    return sp.expand(total)


def check_generic_four_residual_formula():
    residual_count = 4
    port_dimension = 3
    residual = sp.zeros(residual_count)
    for edge_number, (i, j) in enumerate(combinations(range(residual_count), 2)):
        symbol = sp.Symbol(f"a{edge_number}")
        residual[i, j] = residual[j, i] = symbol

    left = sp.Matrix(port_dimension, residual_count, lambda i, j: sp.Symbol(f"r{i}{j}"))
    right = sp.Matrix(
        port_dimension, residual_count, lambda i, j: sp.Symbol(f"s{i}{j}")
    )
    direct = sp.Matrix(
        port_dimension, port_dimension, lambda i, j: sp.Symbol(f"b{i}{j}")
    )

    cofactor = sp.zeros(residual_count)
    for p, q in combinations(range(residual_count), 2):
        rest = tuple(index for index in range(residual_count) if index not in (p, q))
        cofactor[p, q] = cofactor[q, p] = hafnian(residual, rest)

    predicted = sp.expand(hafnian(residual)) * direct + left * cofactor * right.T

    for i in range(port_dimension):
        for j in range(port_dimension):
            full = sp.zeros(residual_count + 2)
            full[:residual_count, :residual_count] = residual
            for p in range(residual_count):
                full[p, residual_count] = full[residual_count, p] = left[i, p]
                full[p, residual_count + 1] = full[residual_count + 1, p] = right[j, p]
            full[residual_count, residual_count + 1] = direct[i, j]
            full[residual_count + 1, residual_count] = direct[i, j]
            assert sp.expand(hafnian(full) - predicted[i, j]) == 0


def check_two_residual_recovery():
    c = sp.Matrix([[0, 1], [1, 0]])
    a0, b0, a1, b1 = sp.symbols("a0 b0 a1 b1")
    left = sp.Matrix([[a0, b0]])
    right = sp.Matrix([[a1, b1]])
    assert sp.expand((left * c * right.T)[0] - (a0 * b1 + b0 * a1)) == 0


def check_common_completion():
    residual_count = 4
    port_count = 3
    port_dimension = 2
    c = sp.Matrix(
        residual_count,
        residual_count,
        lambda i, j: 0 if i == j else 1 + i + j,
    )
    maps = [
        sp.Matrix(
            residual_count,
            port_dimension,
            lambda i, j, port=port: 1 + 7 * port + 3 * i - 2 * j,
        )
        for port in range(port_count)
    ]
    joined = sp.Matrix.hstack(*maps)
    completion = joined.T * c * joined
    for u in range(port_count):
        for v in range(port_count):
            row = slice(u * port_dimension, (u + 1) * port_dimension)
            column = slice(v * port_dimension, (v + 1) * port_dimension)
            assert completion[row, column] == maps[u].T * c * maps[v]
    assert completion.rank() <= residual_count


def check_schur_defect():
    cofactor = sp.Matrix(
        [
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ]
    )
    maps = [
        sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]]),
        sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]]),
        sp.Matrix([[0, 0], [0, 0], [1, 0], [0, 1]]),
        sp.Matrix([[1, 0], [0, 1], [1, 0], [0, 1]]),
        sp.Matrix([[1, 0], [0, 1], [0, 1], [1, 0]]),
        sp.Matrix([[1, 0], [1, 1], [1, 1], [0, 1]]),
    ]

    def gram(left, right):
        return left.T * cofactor * right

    anchor = gram(maps[1], maps[0])
    assert anchor.det() != 0
    test_left = sp.Matrix.hstack(maps[2], maps[3])
    test_right = sp.Matrix.hstack(maps[4], maps[5])
    schur = gram(test_left, test_right) - gram(
        test_left, maps[0]
    ) * anchor.inv() * gram(maps[1], test_right)
    assert cofactor.rank() == 4
    assert schur.rank() <= cofactor.rank() - 2


if __name__ == "__main__":
    check_generic_four_residual_formula()
    check_two_residual_recovery()
    check_common_completion()
    check_schur_defect()
    print("residual-hafnian common cofactor Gram primary verifier: PASS")
