"""Primary exact checks for GLS64 (audit only; not the written proof)."""

from itertools import combinations

import sympy as sp

PORTS = tuple(range(4))


def edge(i: int, j: int) -> tuple[int, int]:
    return tuple(sorted((i, j)))


def complement(i: int, j: int) -> tuple[int, int]:
    return tuple(k for k in PORTS if k not in (i, j))


eta = sp.Symbol("eta")
A = sp.symbols("A0:4")
B = sp.symbols("B0:4")
w = {ij: sp.Symbol(f"w{ij[0]}{ij[1]}") for ij in combinations(PORTS, 2)}


def W(i: int, j: int) -> sp.Symbol:
    return w[edge(i, j)]


delta = {
    (i, j): eta * W(i, j) + A[i] * B[j] + B[i] * A[j] for i, j in combinations(PORTS, 2)
}

C_A = {}
C_B = {}
for u in PORTS:
    rest = tuple(i for i in PORTS if i != u)
    C_A[u] = sum(A[i] * W(*tuple(j for j in rest if j != i)) for i in rest)
    C_B[u] = sum(B[i] * W(*tuple(j for j in rest if j != i)) for i in rest)

H = W(0, 1) * W(2, 3) + W(0, 2) * W(1, 3) + W(0, 3) * W(1, 2)
rhs = sum(W(i, j) * delta[complement(i, j)] for i, j in combinations(PORTS, 2))
lhs_a = 2 * eta * H + sum(B[u] * C_A[u] for u in PORTS)
lhs_b = 2 * eta * H + sum(A[u] * C_B[u] for u in PORTS)

assert sp.expand(lhs_a - rhs) == 0
assert sp.expand(lhs_b - rhs) == 0

zero_patterns = 0
pair_target_kills = 0
one_kernel_target_kills = 0
for size in (3, 4):
    for zero_tuple in combinations(PORTS, size):
        zero_set = set(zero_tuple)
        zero_patterns += 1
        for pair in combinations(PORTS, 2):
            assert zero_set.intersection(pair)
            pair_target_kills += 1
        for u in PORTS:
            contracted = set(PORTS) - {u}
            assert zero_set.intersection(contracted)
            one_kernel_target_kills += 1

scalar_control = {
    eta: 0,
    **{symbol: 1 for symbol in A},
    **{symbol: 0 for symbol in B},
    W(0, 1): 1,
    W(2, 3): 1,
    W(0, 2): 0,
    W(1, 3): 0,
    W(0, 3): -1,
    W(1, 2): -1,
}
assert H.subs(scalar_control) == 2
assert all(value.subs(scalar_control) == 0 for value in delta.values())
assert all(value.subs(scalar_control) == 0 for value in C_A.values())
assert all(value.subs(scalar_control) == 0 for value in C_B.values())

print(f"complementary_edge_terms: {len(delta)}")
print("perfect_matching_products: 3")
print("matching_product_multiplicity: 2")
print(f"zero_patterns_checked: {zero_patterns}")
print(f"pair_target_kills_checked: {pair_target_kills}")
print(f"one_kernel_target_kills_checked: {one_kernel_target_kills}")
print("integrability_identity_A_residual: 0")
print("integrability_identity_B_residual: 0")
print("eta_zero_scalar_boundary_H: 2")
print(
    "PASS: GLS64 matching-integrability identity and eta-zero localization "
    "checks (audit only; global Krenn-Gu conjecture remains unresolved)"
)
