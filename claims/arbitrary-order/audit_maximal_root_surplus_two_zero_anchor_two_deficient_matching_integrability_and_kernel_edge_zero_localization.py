"""Independent standard-library audit for GLS64 displayed finite algebra."""

from collections import Counter
from itertools import combinations

PORTS = tuple(range(4))


def edge(i: int, j: int) -> tuple[int, int]:
    return tuple(sorted((i, j)))


def complement(i: int, j: int) -> tuple[int, int]:
    return tuple(k for k in PORTS if k not in (i, j))


def monomial(*factors: str) -> tuple[str, ...]:
    return tuple(sorted(factors))


lhs_a: Counter[tuple[str, ...]] = Counter()
lhs_b: Counter[tuple[str, ...]] = Counter()
rhs: Counter[tuple[str, ...]] = Counter()

matchings = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
for first, second in matchings:
    term = monomial("eta", f"w{first[0]}{first[1]}", f"w{second[0]}{second[1]}")
    lhs_a[term] += 2
    lhs_b[term] += 2

for u in PORTS:
    rest = tuple(i for i in PORTS if i != u)
    for i in rest:
        j, k = tuple(v for v in rest if v != i)
        lhs_a[monomial(f"B{u}", f"A{i}", f"w{edge(j, k)[0]}{edge(j, k)[1]}")] += 1
        lhs_b[monomial(f"A{u}", f"B{i}", f"w{edge(j, k)[0]}{edge(j, k)[1]}")] += 1

for i, j in combinations(PORTS, 2):
    k, ell = complement(i, j)
    wij = f"w{i}{j}"
    rhs[monomial(wij, "eta", f"w{k}{ell}")] += 1
    rhs[monomial(wij, f"A{k}", f"B{ell}")] += 1
    rhs[monomial(wij, f"B{k}", f"A{ell}")] += 1

assert lhs_a == rhs
assert lhs_b == rhs

pattern_count = 0
pair_checks = 0
cofactor_checks = 0
for size in (3, 4):
    for zero_tuple in combinations(PORTS, size):
        zero_set = set(zero_tuple)
        pattern_count += 1
        for pair in combinations(PORTS, 2):
            assert not set(pair).isdisjoint(zero_set)
            pair_checks += 1
        for u in PORTS:
            assert not (set(PORTS) - {u}).isdisjoint(zero_set)
            cofactor_checks += 1

print(f"labelled polynomial monomials: {len(rhs)}")
print(f"zero-coordinate patterns: {pattern_count}")
print(f"pair-incidence checks: {pair_checks}")
print(f"one-kernel-incidence checks: {cofactor_checks}")
print("A/B complementary-edge identities: exact")
print(
    "PASS (GLS64 finite/displayed audit only; eta=0 residual and global "
    "Krenn-Gu conjecture remain unresolved)"
)
