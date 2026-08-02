"""Independent exact audit of the endpoint-legal hitting classification."""

from __future__ import annotations

import json
from itertools import combinations, product

import sympy as sp

ROWS = 7


def permanent(matrix):
    totals = {0: sp.Integer(1)}
    for row in matrix:
        updated = {}
        for mask, coeff in totals.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if value != 0 and not mask & bit:
                    updated[mask | bit] = updated.get(mask | bit, 0) + coeff * value
        totals = updated
    return sp.expand(totals.get(127, 0))


def base_data():
    names = sp.symbols("a0 a3 a5 a6 b0 b1 b5 b6 X0:5 Y0:5 Z0:5")
    a0, a3, a5, a6, b0, b1, b5, b6, *roots = names
    x, y, z = roots[:5], roots[5:10], roots[10:]
    a = [[0] * 3 for _ in range(7)]
    b = [[0] * 3 for _ in range(7)]
    for u, c, value in ((0, 0, a0), (3, 2, a3), (5, 1, a5), (6, 1, a6)):
        a[u][c] = value
    for u, c, value in ((0, 0, b0), (1, 0, b1), (5, 2, b5), (6, 1, b6)):
        b[u][c] = value
    h = [[[0] * 3 for _ in range(5)] for _ in range(7)]
    for variables, locations, c in (
        (x, ((2, 0), (3, 1), (4, 2), (5, 3), (6, 4)), 0),
        (y, ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)), 1),
        (z, ((1, 0), (0, 1), (6, 2), (4, 3), (2, 4)), 2),
    ):
        for value, (u, r) in zip(variables, locations):
            h[u][r][c] = value
    return names, a, b, h


def coefficient(word, a, b, h):
    matrix = [[h[u][r][word[u]] for u in range(7)] for r in range(5)]
    matrix += [[a[u][word[u]] for u in range(7)], [b[u][word[u]] for u in range(7)]]
    return permanent(matrix)


def add(a0, b0, h0, support):
    a, b, h = [r[:] for r in a0], [r[:] for r in b0], [[r[:] for r in block] for block in h0]
    ts = sp.symbols(f"t0:{len(support)}")
    for value, (row, u, c) in zip(ts, support):
        if row < 5:
            h[u][row][c] = value
        elif row == 5:
            a[u][c] = value
        else:
            b[u][c] = value
    return ts, a, b, h


def main() -> None:
    names, a0, b0, h0 = base_data()
    a0s, _, _, a6, b0s, _, _, b6, *_ = names
    universe = [(r, u, c) for r, u, c in product(range(5), range(7), range(3)) if h0[u][r][c] == 0]
    universe += [(r, u, c) for r, ports in ((5, a0), (6, b0)) for u, c in product((1, 3, 5), range(3)) if ports[u][c] == 0]
    assert len(universe) == 104
    endpoint = {a0s: 1, a6: 1, b0s: 1, b6: -1}
    words = [tuple(map(int, q)) for q in ("0000102", "1112101", "1112220", "0101010", "1010220")]

    def persists(support):
        ts, a, b, h = add(a0, b0, h0, support)
        pure = sp.expand(sp.prod(coefficient((c,) * 7, a, b, h).subs(endpoint) for c in range(3)))
        symbols = sorted(pure.free_symbols | set(ts), key=str)
        return any((f := sp.expand(coefficient(w, a, b, h).subs(endpoint))) != 0 and sp.cancel(pure / f).is_polynomial(*symbols) for w in words)

    assert all(persists((edge,)) for edge in universe)
    survivors = [pair for pair in combinations(universe, 2) if not persists(pair)]
    assert survivors == [((3, 6, 0), (4, 5, 0))]
    _ts, a, b, h = add(a0, b0, h0, survivors[0])
    pure = sp.expand(sp.prod(coefficient((c,) * 7, a, b, h) for c in range(3)))
    mixed = coefficient(tuple(map(int, "0101122")), a, b, h)
    quotient = sp.cancel(pure / mixed)
    assert quotient.is_polynomial(*sorted(pure.free_symbols, key=str))
    assert sp.expand(pure - mixed * quotient) == 0
    print(json.dumps({
        "status": "pass", "legal_universe": 104, "singletons": 104,
        "pairs": 5356, "minimal_transversals": 1,
        "unique_pair": [[3, 6, 0], [4, 5, 0]],
        "full_ideal_certificate": "0101122", "full_ideal_survivors": 0,
        "finite_field_proof_used": False, "global_conjecture_resolved": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
