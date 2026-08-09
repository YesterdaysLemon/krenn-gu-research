"""Independent audit of the a_(1,0) shared-factor obstruction."""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import combinations, product

ROWS = ("r0", "r1", "r2", "r3", "r4", "a", "b")


def entries():
    return {
        ("a", 0, 0): "alpha0", ("a", 1, 0): "gamma", ("a", 3, 2): "alpha3",
        ("a", 5, 1): "alpha5", ("a", 6, 1): "alpha6",
        ("b", 0, 0): "beta0", ("b", 1, 0): "beta1", ("b", 5, 2): "beta5",
        ("b", 6, 1): "beta6",
        ("r0", 2, 0): "X0", ("r1", 3, 0): "X1", ("r2", 4, 0): "X2",
        ("r3", 5, 0): "X3", ("r4", 6, 0): "X4",
        ("r0", 0, 1): "Y0", ("r1", 1, 1): "Y1", ("r2", 2, 1): "Y2",
        ("r3", 3, 1): "Y3", ("r4", 4, 1): "Y4",
        ("r0", 1, 2): "Z0", ("r1", 0, 2): "Z1", ("r2", 6, 2): "Z2",
        ("r3", 4, 2): "Z3", ("r4", 2, 2): "Z4",
    }


def monomials(word, data):
    choices = {row: tuple((u, name) for (rr, u, c), name in data.items() if rr == row and c == word[u]) for row in ROWS}

    @cache
    def recurse(index, used):
        if index == 7:
            return ((),)
        answer = []
        for column, variable in choices[ROWS[index]]:
            if not used & (1 << column):
                for tail in recurse(index + 1, used | (1 << column)):
                    answer.append((variable,) + tail)
        return tuple(answer)

    return tuple(Counter(term) for term in recurse(0, 0))


def matching_count_from_edges(edges):
    choices = {row: tuple(column for rr, column in edges if rr == row) for row in ROWS}

    @cache
    def recurse(index, used):
        if index == 7:
            return 1
        return sum(recurse(index + 1, used | (1 << column)) for column in choices[ROWS[index]] if not used & (1 << column))

    return recurse(0, 0)


def main() -> None:
    data = entries()
    pure0 = monomials((0,) * 7, data)
    word = (0, 0, 0, 0, 1, 0, 2)
    mixed = monomials(word, data)
    assert len(pure0) == len(mixed) == 2
    pure_port_parts = {tuple(sorted(v for v in term if v in {"alpha0", "beta0", "beta1", "gamma"})) for term in pure0}
    mixed_port_parts = {tuple(sorted(v for v in term if v in {"alpha0", "beta0", "beta1", "gamma"})) for term in mixed}
    assert pure_port_parts == mixed_port_parts == {("alpha0", "beta1"), ("beta0", "gamma")}

    # Each mixed monomial divides the corresponding pure-product monomial
    # after multiplying by the colour-one and colour-two pure monomials.
    pure1 = monomials((1,) * 7, data)[0]
    pure2 = monomials((2,) * 7, data)[0]
    for pure_term, mixed_term in zip(pure0, mixed):
        full = pure_term + pure1 + pure2
        assert not +(mixed_term - full)

    edges = {(row, column) for row, column, colour in data if colour == word[column]}
    assert matching_count_from_edges(edges) == 2
    missing = sorted(set(product(ROWS, range(7))) - edges)
    assert not [edge for edge in missing if matching_count_from_edges(edges | {edge}) > 2]
    pairs = [pair for pair in combinations(missing, 2) if matching_count_from_edges(edges | set(pair)) > 2]
    root_swaps = [pair for pair in pairs if all(row.startswith("r") for row, _ in pair)]
    assert (len(pairs), len(root_swaps), len(pairs) - len(root_swaps)) == (30, 10, 20)

    print("PASS: independent a_(1,0) shared pure/mixed factor audit")
    print("pure 0^7 and mixed 0000102 matching counts: 2,2")
    print("shared port factor: alpha0*beta1 + beta0*gamma")
    print("certificate: C0*C1*C2 lies in <C_0000102>")
    print("further one-edge escapes: 0")
    print("minimal two-edge pairs: 30 = 10 root swaps + 20 root-port exchanges")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
