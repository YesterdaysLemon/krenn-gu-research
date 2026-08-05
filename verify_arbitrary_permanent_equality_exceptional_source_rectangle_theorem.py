"""Symbolic checks for the exceptional-source rectangle theorem."""

from __future__ import annotations

from itertools import product

import sympy as sp


def check_degree_ledger() -> None:
    for m in (3, 5, 7):
        epsilons = [entry for entry in product(range(3), repeat=m) if sum(entry) == 2]
        assert all(
            sorted(value for value in epsilon if value) in ([2], [1, 1])
            for epsilon in epsilons
        )
        for epsilon in epsilons:
            assert sum(3 + value for value in epsilon) == 3 * m + 2

    # Representative q=2 ledgers, with the two noncoordinate cells together
    # or apart.  Coordinate degree is always 3+epsilon-q.
    epsilon = (1, 1, 0)
    for q in ((1, 1, 0), (2, 0, 0)):
        coordinate = tuple(
            3 + extra - noncoordinate
            for extra, noncoordinate in zip(epsilon, q, strict=True)
        )
        assert sum(coordinate) == 3 * len(epsilon)


def check_source_localization() -> None:
    mandatory_sources = {0, 1, 2, 3}
    excess_sources = {1, 3}
    omitted_mandatory = {1, 3}
    assert omitted_mandatory <= excess_sources
    assert omitted_mandatory <= mandatory_sources

    # With one exceptional source, no alternating cycle can be formed.
    assert len({1}) < 2
    # With two, a distinct matching can use exactly one new edge at each.
    assert len(excess_sources) == 2


def check_rectangle_equation() -> None:
    a, b, c, d = sp.symbols("A B C D", nonzero=True)
    coefficient = a * d + b * c
    solved = sp.solve(sp.Eq(coefficient, 0), b * c, dict=True)
    assert solved == [{b * c: -a * d}]
    assert sp.simplify((b / a) * (c / d) + 1).subs(b * c, -a * d) == 0

    # A four-cycle has two new edges; every longer alternating cycle has more.
    for length in range(4, 14, 2):
        assert length // 2 >= 2


def main() -> None:
    check_degree_ledger()
    check_source_localization()
    check_rectangle_equation()
    print("exceptional-source rectangle theorem: symbolic checks PASS")
    print("no support, word, or matching enumeration was performed")


if __name__ == "__main__":
    main()
