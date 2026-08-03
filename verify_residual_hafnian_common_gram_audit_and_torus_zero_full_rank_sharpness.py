"""Primary symbolic verifier for common-Gram full-rank sharpness."""

from functools import cache
from itertools import combinations

import sympy as sp


def hafnian(matrix: sp.Matrix, vertices: tuple[int, ...] | None = None) -> sp.Expr:
    if vertices is None:
        vertices = tuple(range(matrix.rows))

    @cache
    def rec(state: tuple[int, ...]) -> sp.Expr:
        if not state:
            return sp.Integer(1)
        first = state[0]
        total = sp.Integer(0)
        for position in range(1, len(state)):
            second = state[position]
            rest = state[1:position] + state[position + 1 :]
            total += matrix[first, second] * rec(rest)
        return sp.expand(total)

    return rec(tuple(vertices))


def permanent(matrix: sp.Matrix) -> sp.Expr:
    @cache
    def rec(row: int, columns: tuple[int, ...]) -> sp.Expr:
        if row == matrix.rows:
            return sp.Integer(1)
        total = sp.Integer(0)
        for position, column in enumerate(columns):
            rest = columns[:position] + columns[position + 1 :]
            total += matrix[row, column] * rec(row + 1, rest)
        return sp.expand(total)

    return rec(0, tuple(range(matrix.cols)))


# Generic q=4 two-port identity.
q = 4
a = sp.zeros(q)
for u, v in combinations(range(q), 2):
    a[u, v] = a[v, u] = sp.Symbol(f"a{u}{v}")
c = sp.zeros(q)
for u, v in combinations(range(q), 2):
    rest = tuple(index for index in range(q) if index not in (u, v))
    c[u, v] = c[v, u] = hafnian(a, rest)
h = hafnian(a)

left = sp.Matrix(2, q, lambda i, j: sp.Symbol(f"l{i}{j}"))
right = sp.Matrix(3, q, lambda i, j: sp.Symbol(f"r{i}{j}"))
direct = sp.Matrix(2, 3, lambda i, j: sp.Symbol(f"b{i}{j}"))
predicted = h * direct + left * c * right.T
for i in range(2):
    for j in range(3):
        full = sp.zeros(q + 2)
        full[:q, :q] = a
        for residual in range(q):
            full[residual, q] = full[q, residual] = left[i, residual]
            full[residual, q + 1] = full[q + 1, residual] = right[j, residual]
        full[q, q + 1] = full[q + 1, q] = direct[i, j]
        assert sp.expand(hafnian(full) - predicted[i, j]) == 0

# Root-permanent aggregate at r=1 on three blockers; this catches a factor two.
root = sp.Matrix([[sp.Symbol(f"g{u}") for u in range(3)]])
incidence = [sp.Matrix([[sp.Symbol(f"x{p}{u}") for u in range(3)]]) for p in range(q)]
aggregate_left = sp.Integer(0)
for u, v in combinations(range(3), 2):
    remaining = next(index for index in range(3) if index not in (u, v))
    corrected = sum(
        incidence[p][0, u] * c[p, s] * incidence[s][0, v]
        for p in range(q)
        for s in range(q)
    )
    aggregate_left += root[0, remaining] * corrected

aggregate_right = sp.Integer(0)
for p, s in combinations(range(q), 2):
    extension = root.col_join(incidence[p]).col_join(incidence[s])
    aggregate_right += c[p, s] * permanent(extension)
assert sp.expand(aggregate_left - aggregate_right) == 0

# Hadamard row expansion and Euler identity for generic q=6.
q_six = 6
a_six = sp.zeros(q_six)
for u, v in combinations(range(q_six), 2):
    a_six[u, v] = a_six[v, u] = sp.Symbol(f"s{u}{v}")
h_six = hafnian(a_six)
c_six = sp.zeros(q_six)
for u, v in combinations(range(q_six), 2):
    rest = tuple(index for index in range(q_six) if index not in (u, v))
    c_six[u, v] = c_six[v, u] = hafnian(a_six, rest)
for u in range(q_six):
    assert sp.expand(sum(a_six[u, v] * c_six[u, v] for v in range(q_six)) - h_six) == 0
euler = sum(a_six[u, v] * c_six[u, v] for u, v in combinations(range(q_six), 2))
assert sp.expand(euler - 3 * h_six) == 0


def sharp_matrix(order: int) -> sp.Matrix:
    matrix = sp.ones(order) - sp.eye(order)
    matrix[0, 1] = matrix[1, 0] = -(order - 2)
    return matrix


for order in (4, 6, 8):
    residual = sharp_matrix(order)
    assert hafnian(residual) == 0
    cofactor = sp.zeros(order)
    for u, v in combinations(range(order), 2):
        rest = tuple(index for index in range(order) if index not in (u, v))
        cofactor[u, v] = cofactor[v, u] = hafnian(residual, rest)
    alpha = sp.factorial2(order - 3)
    beta = -2 * sp.factorial2(order - 5)
    assert cofactor[0, 1] == alpha
    assert all(cofactor[0, vertex] == alpha for vertex in range(2, order))
    assert all(
        cofactor[u, v] == beta for u, v in combinations(range(2, order), 2)
    )
    assert cofactor.det() != 0
    assert cofactor.rank() == order
    stress = residual.multiply_elementwise(cofactor)
    assert stress * sp.ones(order, 1) == sp.zeros(order, 1)

    # Identity incidence maps make the common cross block equal to C itself.
    identity = sp.eye(order)
    cross_block = identity.T * cofactor * identity
    assert cross_block == cofactor
    assert cross_block.rank() == order

# q=2 is the automatic full-rank endpoint, even at h=0.
q_two_cofactor = sp.Matrix([[0, 1], [1, 0]])
assert q_two_cofactor.det() == -1

print("arbitrary-residual common Gram and aggregate normalization: PASS")
print("Hadamard-stress identities: PASS")
print("torus-zero full-cofactor-rank family q=2,4,6,8: PASS")
print("sharp common cross-block rank: PASS")
print("GLOBAL KRENN-GU STATUS: UNRESOLVED")
