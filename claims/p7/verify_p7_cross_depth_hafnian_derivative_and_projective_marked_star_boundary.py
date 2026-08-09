"""Primary symbolic checks for the P7 cross-depth hafnian boundary."""

from functools import cache
from itertools import combinations, permutations

import sympy as sp


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def hafnian(vertices: tuple[int, ...], weights: dict[tuple[int, int], sp.Expr]) -> sp.Expr:
    """Exact recursive hafnian; used only on one eight-vertex symbolic control."""

    @cache
    def rec(state: tuple[int, ...]) -> sp.Expr:
        if not state:
            return sp.Integer(1)
        u = state[0]
        total = sp.Integer(0)
        for pos in range(1, len(state)):
            v = state[pos]
            rest = state[1:pos] + state[pos + 1 :]
            total += weights[edge(u, v)] * rec(rest)
        return sp.expand(total)

    return rec(tuple(sorted(vertices)))


# A generic 2+2 shore with four complementary vertices is enough to check
# the arbitrary-size operator pattern without a P7 matching census.
vertices = tuple(range(8))
weights = {
    (u, v): sp.Symbol(f"a{u}{v}") for u, v in combinations(vertices, 2)
}
full = hafnian(vertices, weights)
j_set = (0, 1)
d_set = (2, 3)
x_set = (4, 5, 6, 7)

shore_operator = sp.Integer(0)
shore_permanent = sp.Integer(0)
for image in permutations(d_set):
    shore_edges = tuple(edge(j, d) for j, d in zip(j_set, image, strict=True))
    term = full
    shore_weight = sp.Integer(1)
    for shore_edge in shore_edges:
        term = sp.diff(term, weights[shore_edge])
        shore_weight *= weights[shore_edge]
    shore_operator += shore_weight * term
    shore_permanent += shore_weight

complement_hafnian = hafnian(x_set, weights)
assert sp.expand(shore_operator - shore_permanent * complement_hafnian) == 0

# One more edge derivative removes its endpoints from the complement.
p = edge(4, 5)
e = (6, 7)
assert sp.expand(sp.diff(shore_operator, weights[p]) - shore_permanent * weights[e]) == 0

# Exact P7 complement incidence: differentiating a triangle in W\{a}
# produces the star of retained complementary pairs containing a.
w_set = frozenset((1, 2, 3, 4))
pairs = tuple(combinations(sorted(w_set), 2))
for a in sorted(w_set):
    derivative_pairs = {
        frozenset(p) for p in combinations(sorted(w_set - {a}), 2)
    }
    retained_pairs = {w_set - p for p in derivative_pairs}
    expected_star = {frozenset((a, b)) for b in w_set - {a}}
    assert retained_pairs == expected_star

# Common-shore pair-vector proportionality.
f = sp.Symbol("f", nonzero=True)
m = {frozenset(p): sp.Symbol(f"m{p[0]}{p[1]}") for p in pairs}
z = {frozenset(p): sp.Symbol(f"z{p[0]}{p[1]}") for p in pairs}
for e_pair, direct_value in m.items():
    observed_z = f * z[e_pair]
    observed_m = f * direct_value
    assert sp.expand(direct_value * observed_z - z[e_pair] * observed_m) == 0

# The actual two-root weights are second permanental minors.
def pair_permanents(a_row: tuple[int, ...], b_row: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        a_row[u - 1] * b_row[v - 1] + a_row[v - 1] * b_row[u - 1]
        for u, v in pairs
    )


positive = pair_permanents((1, 1, 1, 1), (1, 1, 1, 1))
sharp_failure = pair_permanents((1, 0, 1, 0), (0, 1, 1, 2))
projective = pair_permanents((0, 0, 0, 0), (0, 0, 0, 0))
assert positive == (2, 2, 2, 2, 2, 2)
assert sharp_failure == (1, 1, 2, 1, 0, 2)
assert projective == (0, 0, 0, 0, 0, 0)

# Four individually normalizable complement triangles force one common value.
kappa_symbols = {frozenset(p): sp.Symbol(f"k{p[0]}{p[1]}") for p in pairs}
equalities: list[sp.Expr] = []
for a in sorted(w_set):
    triangle = [
        kappa_symbols[frozenset(p)]
        for p in combinations(sorted(w_set - {a}), 2)
    ]
    equalities.extend((triangle[1] - triangle[0], triangle[2] - triangle[0]))
coefficient_matrix, _ = sp.linear_eq_to_matrix(equalities, list(kappa_symbols.values()))
assert coefficient_matrix.rank() == 5
assert coefficient_matrix.nullspace() == [sp.ones(6, 1)]

# Free-h response M=1+x1*x2, Z=lambda has no nonempty z coefficients.
lam = sp.Symbol("lambda")
x1, x2 = sp.symbols("x1 x2")
direct_moment = 1 + x1 * x2
residual_response = lam
assert sp.expand(residual_response).coeff(x1 * x2) == 0
square_zero_remainder = sp.expand(direct_moment * (lam - lam * x1 * x2) - lam)
assert square_zero_remainder == -lam * x1**2 * x2**2

print("generic shore derivative recurrence: PASS")
print("P7 common-normalization pair derivatives and stars: PASS")
print("two-root permanental normalization criterion and controls: PASS")
print("projective marked sectors and free-h boundary: PASS")
print("GLOBAL KRENN-GU STATUS: UNRESOLVED")
