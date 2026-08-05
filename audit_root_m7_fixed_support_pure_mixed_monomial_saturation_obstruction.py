"""Independent no-import audit of the fixed-support monomial obstruction."""

from __future__ import annotations

from collections import Counter
from functools import cache

ROWS = ("r0", "r1", "r2", "r3", "r4", "a", "b")


def data():
    ports = {
        ("a", 0, 0): "alpha0",
        ("a", 3, 2): "alpha3",
        ("a", 5, 1): "alpha5",
        ("a", 6, 1): "alpha6",
        ("b", 0, 0): "beta0",
        ("b", 1, 0): "beta1",
        ("b", 5, 2): "beta5",
        ("b", 6, 1): "beta6",
    }
    roots = {
        ("r0", 2, 0): "X0", ("r1", 3, 0): "X1", ("r2", 4, 0): "X2",
        ("r3", 5, 0): "X3", ("r4", 6, 0): "X4",
        ("r0", 0, 1): "Y0", ("r1", 1, 1): "Y1", ("r2", 2, 1): "Y2",
        ("r3", 3, 1): "Y3", ("r4", 4, 1): "Y4",
        ("r0", 1, 2): "Z0", ("r1", 0, 2): "Z1", ("r2", 6, 2): "Z2",
        ("r3", 4, 2): "Z3", ("r4", 2, 2): "Z4",
    }
    return ports | roots


def monomials(word, entries):
    choices = {
        row: tuple((u, name) for (rr, u, colour), name in entries.items() if rr == row and colour == word[u])
        for row in ROWS
    }

    @cache
    def recurse(index, used):
        if index == len(ROWS):
            return ((),)
        answer = []
        for column, variable in choices[ROWS[index]]:
            bit = 1 << column
            if not used & bit:
                for tail in recurse(index + 1, used | bit):
                    answer.append((variable,) + tail)
        return tuple(answer)

    return tuple(Counter(term) for term in recurse(0, 0))


def multiply(*monomials_to_multiply):
    answer = Counter()
    for monomial in monomials_to_multiply:
        answer.update(monomial)
    return answer


def main() -> None:
    entries = data()
    words = ((0,) * 7, (1,) * 7, (2,) * 7, (0, 0, 0, 0, 1, 0, 2))
    results = [monomials(word, entries) for word in words]
    assert [len(result) for result in results] == [1, 1, 1, 1]
    c0, c1, c2, cw = (result[0] for result in results)

    expected_cw = Counter({
        "alpha0": 1, "beta1": 1, "X0": 1, "X1": 1,
        "X3": 1, "Y4": 1, "Z2": 1,
    })
    assert cw == expected_cw

    pure_product = multiply(c0, c1, c2)
    quotient = pure_product - cw
    assert not +(cw - pure_product)
    assert multiply(cw, quotient) == pure_product

    support = {(row, u) for (row, u, colour) in entries if colour == words[3][u]}
    new_single_edges = []
    for row in ROWS:
        for column in range(7):
            if (row, column) in support:
                continue
            augmented = dict(entries)
            augmented[(row, column, words[3][column])] = "new"
            if len(monomials(words[3], augmented)) > 1:
                new_single_edges.append((row, column))
    assert new_single_edges == [("a", 1)]

    print("PASS: independent fixed-support pure--mixed monomial audit")
    print("pure matching counts: 1,1,1")
    print("mixed word 0000102 matching count: 1")
    print("identity: C0*C1*C2 = Cw*Q")
    print("saturation <Cw>:(C0*C1*C2)^infinity: unit ideal")
    print("single-edge alternatives: a_(1,0) only; no root edge")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
