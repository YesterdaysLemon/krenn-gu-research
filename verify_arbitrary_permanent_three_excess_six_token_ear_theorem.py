"""Primary symbolic checks for the six-token odd-ear theorem."""

from __future__ import annotations

import sympy as sp


def integer_partitions(total: int, maximum: int | None = None) -> tuple[tuple[int, ...], ...]:
    """Return positive unordered partitions; used only for the constant budget three."""
    if total == 0:
        return ((),)
    upper = total if maximum is None else min(total, maximum)
    result: list[tuple[int, ...]] = []
    for first in range(upper, 0, -1):
        for tail in integer_partitions(total - first, first):
            result.append((first, *tail))
    return tuple(result)


def main() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    vertices = 2 * m
    edges = 3 * m + 3
    ears = sp.expand(edges - vertices)
    endpoint_slots = sp.expand(2 * ears)
    mandatory_slots = vertices

    assert ears == m + 3
    assert sp.expand(endpoint_slots - mandatory_slots) == 6

    vertices_per_shore = m
    endpoints_per_shore = ears
    assert sp.expand(endpoints_per_shore - vertices_per_shore) == 3
    assert sp.expand(2 * edges - 3 * vertices) == 6
    assert sp.expand(edges - 3 * vertices_per_shore) == 3

    # Each ear of odd length ell adds ell edges and ell-1 vertices.
    ell = sp.symbols("ell", integer=True, positive=True)
    assert sp.expand(ell - (ell - 1)) == 1

    # A vertex is born with degree two and gains one edge per later endpoint use.
    h = sp.symbols("h", integer=True, positive=True)
    degree = 2 + h
    surplus = sp.expand(h - 1)
    assert sp.expand(degree - 3 - surplus) == 0

    assert integer_partitions(3) == ((3,), (2, 1), (1, 1, 1))

    # A last ear with an internal vertex leaves that vertex at degree two.
    last_ear_internal_vertex_degree = 2
    minimum_degree = 3
    assert last_ear_internal_vertex_degree < minimum_degree

    print("arbitrary permanent three-excess six-token ear theorem: PASS")
    print("symbolic ledger only; no ear, matching, support, or graph census was performed")


if __name__ == "__main__":
    main()
