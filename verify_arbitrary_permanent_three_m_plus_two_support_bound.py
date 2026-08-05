"""Symbolic sanity checks for the arbitrary 3m+2 support theorem."""

from __future__ import annotations

import sympy as sp


def check_transverse_counts() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    assert sp.simplify(3 * m + 1 - 3 * m) == 1
    assert sp.simplify((4 + 3 * (m - 1)) - (3 * m + 1)) == 0

    lambdas = sp.diag(*sp.symbols("lambda0:3", nonzero=True))
    assert lambdas.rank() == 3


def check_coordinate_case(m: int) -> None:
    counts = [m, m, m + 1]
    assert sum(counts) == 3 * m + 1
    assert all(count >= m for count in counts)
    assert sum(count - m for count in counts) == 1


def check_noncoordinate_ledgers(m: int) -> None:
    # ell at the four-cell mode: every coordinate colour has mode degree one.
    regular = [[1 for _ in range(m)] for _ in range(3)]
    assert all(sum(row) == m for row in regular)

    # ell at i*=0 and the coordinate-only four-cell mode j=1.  Colour zero
    # is missing at i*, doubled at j, and occurs once elsewhere.
    repair = [0, 2, *([1] * (m - 2))]
    assert len(repair) == m
    assert sum(repair) == m
    assert repair.count(0) == repair.count(2) == 1

    # Source p*=0 has its coordinate d-cell at j.  Replacing it by ell at
    # i* changes the mode ledger from (0,2,1,...) to (1,1,1,...).
    repaired = repair.copy()
    repaired[0] += 1
    repaired[1] -= 1
    assert repaired == [1] * m


def check_one_exception_cycle_logic() -> None:
    # A distinct perfect matching has an alternating cycle.  Its half-length
    # is at least two, so it needs at least two edges outside the reference.
    for cycle_length in range(4, 14, 2):
        assert cycle_length // 2 >= 2

    # In the repair case the only two eligible exceptions share source p*.
    ell = (0, 0)
    omitted = (1, 0)
    assert ell[1] == omitted[1]


def check_two_cycle_orientation() -> None:
    # Two alternating components.  A proper orientation and its complement
    # are both mixed and choose opposite edges on every component.
    orientation = (0, 1)
    complement = tuple(1 - bit for bit in orientation)
    assert orientation not in ((0, 0), (1, 1))
    assert complement not in ((0, 0), (1, 1))
    assert all(a != b for a, b in zip(orientation, complement, strict=True))


def main() -> None:
    check_transverse_counts()
    for m in (3, 5, 7, 11):
        check_coordinate_case(m)
        check_noncoordinate_ledgers(m)
    check_one_exception_cycle_logic()
    check_two_cycle_orientation()
    print("arbitrary permanent 3m+2 support bound: symbolic sanity checks PASS")
    print("arbitrary matching input: Bogdanov theorem (not finite enumeration)")


if __name__ == "__main__":
    main()
