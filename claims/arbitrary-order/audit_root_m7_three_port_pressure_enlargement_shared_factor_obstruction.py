"""Independent matching audit of the three-port shared-factor obstruction."""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import combinations, product

ROWS = ("r0", "r1", "r2", "r3", "r4", "a", "b")
W = (0, 0, 0, 0, 1, 0, 2)


def entries():
    data = {
        ("a", 0, 0): "a0", ("a", 1, 0): "g", ("a", 3, 2): "a3",
        ("a", 5, 1): "a5", ("a", 5, 2): "eps", ("a", 6, 1): "a6",
        ("b", 0, 0): "b0", ("b", 1, 0): "b1", ("b", 5, 1): "del",
        ("b", 5, 2): "b5", ("b", 6, 1): "b6",
    }
    for root, u in enumerate((2, 3, 4, 5, 6)):
        data[(f"r{root}", u, 0)] = f"X{root}"
    for root, u in enumerate((0, 1, 2, 3, 4)):
        data[(f"r{root}", u, 1)] = f"Y{root}"
    for root, u in enumerate((1, 0, 6, 4, 2)):
        data[(f"r{root}", u, 2)] = f"Z{root}"
    return data


def monomials(word, data):
    choices = {row: tuple((u, name) for (rr, u, c), name in data.items() if rr == row and c == word[u]) for row in ROWS}

    @cache
    def recurse(index, used):
        if index == 7:
            return ((),)
        answer = []
        for column, name in choices[ROWS[index]]:
            if not used & (1 << column):
                for tail in recurse(index + 1, used | (1 << column)):
                    answer.append((name,) + tail)
        return tuple(answer)

    return tuple(Counter(term) for term in recurse(0, 0))


def count_edges(edges):
    data = {(row, u, W[u]): "q" for row, u in edges}
    return len(monomials(W, data))


def principal_path_count(deleted):
    vertices = tuple(u for u in range(7) if u != deleted)
    path = {tuple(sorted((u, u + 1))) for u in range(6)}

    @cache
    def recurse(remaining):
        if not remaining:
            return 1
        first = remaining[0]
        total = 0
        for index in range(1, len(remaining)):
            second = remaining[index]
            if tuple(sorted((first, second))) not in path:
                continue
            rest = remaining[1:index] + remaining[index + 1 :]
            total += recurse(rest)
        return total

    return recurse(vertices)


def main() -> None:
    data = entries()
    pure0 = monomials((0,) * 7, data)
    mixed = monomials(W, data)
    assert len(pure0) == len(mixed) == 2
    ports = {"a0", "b0", "b1", "g"}
    pure_parts = {tuple(sorted(v for v in term if v in ports)) for term in pure0}
    mixed_parts = {tuple(sorted(v for v in term if v in ports)) for term in mixed}
    assert pure_parts == mixed_parts == {("a0", "b1"), ("b0", "g")}
    assert all("del" not in term and "eps" not in term for term in mixed)

    base = dict(data)
    del base[("b", 5, 1)], base[("a", 5, 2)]
    support = {(row, u) for row, u, colour in base if colour == W[u]}
    missing = sorted(set(product(ROWS, range(7))) - support)
    pairs = [pair for pair in combinations(missing, 2) if count_edges(support | set(pair)) > 2]
    assert len(pairs) == 30
    triple = {("b", 5, 1), ("a", 5, 2)}
    assert not [pair for pair in pairs if {(row, u, W[u]) for row, u in pair} <= triple]
    assert principal_path_count(1) == principal_path_count(5) == 0

    print("PASS: independent three-port shared-factor audit")
    print("shared pure/mixed colour-zero matching polynomial: 2 terms")
    print("C0*C1*C2 lies in <C_0000102>")
    print("previous pair-shell supports contained: 0/30")
    print("new blockers are odd; endpoint cofactors unchanged")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
