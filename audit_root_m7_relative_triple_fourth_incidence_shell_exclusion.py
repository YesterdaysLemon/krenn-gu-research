"""Independent no-repository-import audit of the relative fourth shell."""

from __future__ import annotations

import json
from itertools import product

import sympy as sp

TRIPLES = (
    ((0, 3, 1), (3, 4, 1), (4, 0, 1)),
    ((0, 4, 1), (3, 0, 1), (4, 3, 1)),
    ((0, 5, 0), (3, 6, 0), (4, 2, 0)),
    ((0, 6, 0), (3, 2, 0), (4, 5, 0)),
    ((1, 4, 1), (4, 5, 1), (5, 1, 1)),
    ((1, 4, 1), (4, 5, 1), (6, 1, 1)),
    ((2, 3, 1), (3, 4, 1), (4, 2, 1)),
    ((2, 4, 1), (3, 2, 1), (4, 3, 1)),
    ((3, 6, 0), (4, 5, 0), (5, 5, 2)),
)
EXPECTED_ESCAPES = (
    ((0, 3, 1), (3, 4, 1), (4, 0, 1), (5, 1, 0)),
    ((0, 4, 1), (3, 0, 1), (4, 3, 1), (5, 1, 0)),
    ((0, 5, 0), (3, 6, 0), (4, 2, 0), (5, 1, 0)),
    ((0, 6, 0), (3, 2, 0), (4, 5, 0), (5, 1, 0)),
    ((1, 4, 1), (4, 5, 1), (5, 1, 0), (5, 1, 1)),
    ((1, 4, 1), (4, 5, 1), (5, 1, 0), (6, 1, 1)),
    ((2, 3, 1), (3, 4, 1), (4, 2, 1), (5, 1, 0)),
    ((2, 4, 1), (3, 2, 1), (4, 3, 1), (5, 1, 0)),
    ((3, 6, 0), (4, 5, 0), (5, 1, 0), (5, 5, 2)),
    ((3, 6, 0), (4, 5, 0), (5, 5, 2), (6, 3, 2)),
)


def permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, scalar in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if entry != 0 and not mask & bit:
                    target = mask | bit
                    updated[target] = updated.get(target, 0) + scalar * entry
        states = updated
    return sp.expand(states.get(127, 0))


def base_model():
    names = sp.symbols("a0 a3 a5 a6 b0 b1 b5 b6 X0:5 Y0:5 Z0:5")
    a0, a3, a5, a6, b0, b1, b5, b6, *weights = names
    x, y, z = weights[:5], weights[5:10], weights[10:]
    ports = [[[0] * 3 for _ in range(7)] for _ in range(2)]
    for u, c, value in ((0, 0, a0), (3, 2, a3), (5, 1, a5), (6, 1, a6)):
        ports[0][u][c] = value
    for u, c, value in ((0, 0, b0), (1, 0, b1), (5, 2, b5), (6, 1, b6)):
        ports[1][u][c] = value
    roots = [[[0] * 3 for _ in range(5)] for _ in range(7)]
    locations = (
        ((2, 0), (3, 1), (4, 2), (5, 3), (6, 4)),
        ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)),
        ((1, 0), (0, 1), (6, 2), (4, 3), (2, 4)),
    )
    for colour, (values, places) in enumerate(zip((x, y, z), locations)):
        for value, (u, root) in zip(values, places):
            roots[u][root][colour] = value
    return ports, roots, {a0: 1, a6: 1, b0: 1, b6: -1}


def universe(ports, roots):
    answer = [
        (root, u, colour)
        for root, u, colour in product(range(5), range(7), range(3))
        if roots[u][root][colour] == 0
    ]
    answer += [
        (5 + port, u, colour)
        for port, u, colour in product(range(2), (1, 3, 5), range(3))
        if ports[port][u][colour] == 0
    ]
    return tuple(answer)


def extend(ports0, roots0, support):
    ports = [[row[:] for row in family] for family in ports0]
    roots = [[row[:] for row in block] for block in roots0]
    for value, (row, u, colour) in zip(sp.symbols("t0:4"), support):
        if row < 5:
            roots[u][row][colour] = value
        else:
            ports[row - 5][u][colour] = value
    return ports, roots


def coefficient(word, ports, roots):
    rows = [[roots[u][root][word[u]] for u in range(7)] for root in range(5)]
    rows += [[ports[port][u][word[u]] for u in range(7)] for port in range(2)]
    return permanent(rows)


def divides(numerator, denominator):
    if denominator == 0:
        return False
    variables = sorted(numerator.free_symbols | denominator.free_symbols, key=str)
    _quotient, remainder = sp.div(numerator, denominator, *variables, domain=sp.QQ)
    return sp.expand(remainder) == 0


def main() -> None:
    ports0, roots0, endpoint = base_model()
    legal = universe(ports0, roots0)
    candidates = tuple(
        sorted({tuple(sorted(triple + (edge,))) for triple in TRIPLES for edge in legal if edge not in triple})
    )
    assert len(legal) == 104 and len(candidates) == 908
    old_word = tuple(map(int, "2002000"))
    new_words = tuple(tuple(map(int, word)) for word in ("0220212", "0210220"))
    escapes = []
    for support in candidates:
        ports, roots = extend(ports0, roots0, support)
        pure = sp.expand(
            sp.prod(coefficient((colour,) * 7, ports, roots).subs(endpoint) for colour in range(3))
        )
        mixed = sp.expand(coefficient(old_word, ports, roots).subs(endpoint))
        if not divides(pure, mixed):
            escapes.append(support)
    assert len(candidates) - len(escapes) == 898
    assert tuple(escapes) == EXPECTED_ESCAPES

    replacement_counts = [0] * len(new_words)
    for support in escapes:
        ports, roots = extend(ports0, roots0, support)
        pure = sp.expand(
            sp.prod(coefficient((colour,) * 7, ports, roots).subs(endpoint) for colour in range(3))
        )
        for index, word in enumerate(new_words):
            mixed = sp.expand(coefficient(word, ports, roots).subs(endpoint))
            if divides(pure, mixed):
                replacement_counts[index] += 1
                break
        else:
            raise AssertionError(f"replacement certificate missing for {support}")
    assert replacement_counts == [8, 2]

    print(
        json.dumps(
            {
                "status": "pass",
                "legal_universe": len(legal),
                "relative_triples": len(TRIPLES),
                "distinct_four_supports": len(candidates),
                "retained_2002000": len(candidates) - len(escapes),
                "relative_escapes": len(escapes),
                "replacement_certificates": {"0220212": 8, "0210220": 2},
                "relative_fourth_shell_survivors": 0,
                "repository_imports": 0,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
