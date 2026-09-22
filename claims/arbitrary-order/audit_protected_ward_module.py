"""Independent exact audit of the unrestricted Ward-module boundary.

The audit uses a two-vertex, two-color square-zero algebra and standard-library
rational linear algebra.  It verifies the ordinary support-module formula,
its conjugated Ward form, and the distinction between a raw top term and the
transformed physical top response.  It is a finite semantic control, not a
proof of the arbitrary-order module theorem or of elimination.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
import json


COLORS = 2
BASIS = tuple(product(range(-1, COLORS), repeat=2))
INDEX = {word: i for i, word in enumerate(BASIS)}
DIM = len(BASIS)


def zero_matrix():
    return [[Fraction(0) for _ in range(DIM)] for _ in range(DIM)]


def identity_matrix():
    matrix = zero_matrix()
    for i in range(DIM):
        matrix[i][i] = 1
    return matrix


def matrix_add(left, right, right_scale=1):
    scale = Fraction(right_scale)
    return [
        [left[i][j] + scale * right[i][j] for j in range(DIM)]
        for i in range(DIM)
    ]


def matrix_mul(left, right):
    answer = zero_matrix()
    for i in range(DIM):
        for k in range(DIM):
            if not left[i][k]:
                continue
            for j in range(DIM):
                answer[i][j] += left[i][k] * right[k][j]
    return answer


def matrix_vector(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(DIM)), Fraction(0))
        for i in range(DIM)
    ]


def rank(vectors):
    """Column rank over Q by exact row reduction."""
    if not vectors:
        return 0
    matrix = [[Fraction(vector[row]) for vector in vectors] for row in range(DIM)]
    rows, cols = len(matrix), len(vectors)
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            value = matrix[row][col]
            matrix[row] = [
                matrix[row][j] - value * matrix[pivot_row][j]
                for j in range(cols)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def closure(generators, operators):
    vectors = [list(map(Fraction, vector)) for vector in generators]
    current_rank = rank(vectors)
    changed = True
    while changed:
        changed = False
        for vector in tuple(vectors):
            for operator in operators:
                candidate = matrix_vector(operator, vector)
                new_rank = rank([*vectors, candidate])
                if new_rank > current_rank:
                    vectors.append(candidate)
                    current_rank = new_rank
                    changed = True
    return vectors


def support(word):
    return tuple(i for i, color in enumerate(word) if color >= 0)


def local_unit(vertex, out_color, in_color):
    matrix = zero_matrix()
    for column, word in enumerate(BASIS):
        if word[vertex] == in_color:
            image = list(word)
            image[vertex] = out_color
            matrix[INDEX[tuple(image)]][column] = 1
    return matrix


def multiplication_by_monomial(monomial):
    matrix = zero_matrix()
    for column, word in enumerate(BASIS):
        image = list(word)
        for vertex, color in enumerate(monomial):
            if color < 0:
                continue
            if image[vertex] >= 0:
                break
            image[vertex] = color
        else:
            matrix[INDEX[tuple(image)]][column] = 1
    return matrix


def verify():
    units = tuple(
        local_unit(vertex, a, b)
        for vertex in range(2)
        for a in range(COLORS)
        for b in range(COLORS)
    )

    # The generator has nonzero components exactly on supports {0} and {0,1}.
    ordinary = [Fraction(0)] * DIM
    ordinary[INDEX[(0, -1)]] = 1
    ordinary[INDEX[(1, -1)]] = 2
    ordinary[INDEX[(0, 0)]] = 3
    ordinary[INDEX[(1, 1)]] = -1
    ordinary_module = closure([ordinary], units)
    assert rank(ordinary_module) == COLORS + COLORS**2 == 6
    occupied = {
        support(BASIS[row])
        for vector in ordinary_module
        for row in range(DIM)
        if vector[row]
    }
    assert occupied == {(0,), (0, 1)}

    # Q=x_(0,0)x_(1,1), so exp(+-Q)=I+-M_Q and M_Q^2=0.
    multiply_q = multiplication_by_monomial((0, 1))
    identity = identity_matrix()
    exp_q = matrix_add(identity, multiply_q)
    exp_minus_q = matrix_add(identity, multiply_q, -1)
    assert matrix_mul(exp_q, exp_minus_q) == identity

    # A transformed residual with no top component can acquire a raw top term
    # after exp(-Q); reconjugation removes it from the physical top response.
    transformed = [Fraction(0)] * DIM
    transformed[INDEX[(-1, -1)]] = 1
    transformed[INDEX[(1, -1)]] = 2
    residual = matrix_vector(exp_minus_q, transformed)
    assert residual[INDEX[(0, 1)]] == -1
    response = matrix_vector(exp_q, residual)
    assert all(
        response[row] == 0
        for row, word in enumerate(BASIS)
        if support(word) == (0, 1)
    )

    ward_operators = tuple(
        matrix_mul(matrix_mul(exp_minus_q, operator), exp_q)
        for operator in units
    )
    ward_module = closure([residual], ward_operators)
    transformed_module = closure([transformed], units)
    predicted = [matrix_vector(exp_minus_q, vector) for vector in transformed_module]
    assert rank(ward_module) == rank(predicted) == 1 + COLORS == 3
    assert rank([*ward_module, *predicted]) == 3

    return {
        "schema": "protected-ward-module-audit-v1",
        "status": "verified_exact_finite_semantic_control",
        "vertices": 2,
        "colors": COLORS,
        "ordinary_support_module_dimension": rank(ordinary_module),
        "conjugated_ward_module_dimension": rank(ward_module),
        "raw_top_term": str(residual[INDEX[(0, 1)]]),
        "transformed_top_response_zero": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
