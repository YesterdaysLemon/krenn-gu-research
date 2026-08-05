"""Independent no-repository-import audit of the complete legal triple shell."""

from __future__ import annotations

import json
from itertools import combinations, product

import sympy as sp

OLD_LABELS = ("0000102", "1112101", "1112220", "0101010", "1010220", "0101122")
OLD_WORDS = tuple(tuple(map(int, word)) for word in OLD_LABELS)
FINAL_WORD = tuple(map(int, "2002000"))
EXPECTED_SURVIVORS = (
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


def permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for used, scalar in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if entry != 0 and used & bit == 0:
                    target = used | bit
                    next_states[target] = next_states.get(target, 0) + scalar * entry
        states = next_states
    return sp.expand(states.get(127, 0))


def fixed_model():
    symbols = sp.symbols("aa0 aa3 aa5 aa6 bb0 bb1 bb5 bb6 xx0:5 yy0:5 zz0:5")
    aa0, aa3, aa5, aa6, bb0, bb1, bb5, bb6, *root_weights = symbols
    xx, yy, zz = root_weights[:5], root_weights[5:10], root_weights[10:]
    ports = [[[0] * 3 for _ in range(7)] for _ in range(2)]
    for blocker, colour, value in ((0, 0, aa0), (3, 2, aa3), (5, 1, aa5), (6, 1, aa6)):
        ports[0][blocker][colour] = value
    for blocker, colour, value in ((0, 0, bb0), (1, 0, bb1), (5, 2, bb5), (6, 1, bb6)):
        ports[1][blocker][colour] = value
    roots = [[[0] * 3 for _ in range(5)] for _ in range(7)]
    placements = (
        ((2, 0), (3, 1), (4, 2), (5, 3), (6, 4)),
        ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)),
        ((1, 0), (0, 1), (6, 2), (4, 3), (2, 4)),
    )
    for colour, (weights, locations) in enumerate(zip((xx, yy, zz), placements)):
        for value, (blocker, root) in zip(weights, locations):
            roots[blocker][root][colour] = value
    endpoint = {aa0: 1, aa6: 1, bb0: 1, bb6: -1}
    return ports, roots, endpoint


def legal_universe(ports, roots):
    root_edges = [
        (root, blocker, colour)
        for root, blocker, colour in product(range(5), range(7), range(3))
        if roots[blocker][root][colour] == 0
    ]
    port_edges = [
        (5 + port, blocker, colour)
        for port, blocker, colour in product(range(2), (1, 3, 5), range(3))
        if ports[port][blocker][colour] == 0
    ]
    return tuple(root_edges + port_edges)


def extend(ports0, roots0, support):
    ports = [[row[:] for row in family] for family in ports0]
    roots = [[row[:] for row in block] for block in roots0]
    weights = sp.symbols("u0:3")
    for weight, (row, blocker, colour) in zip(weights, support):
        if row < 5:
            roots[blocker][row][colour] = weight
        else:
            ports[row - 5][blocker][colour] = weight
    return ports, roots


def coefficient(word, ports, roots):
    rows = [[roots[blocker][root][word[blocker]] for blocker in range(7)] for root in range(5)]
    rows.extend([[ports[port][blocker][word[blocker]] for blocker in range(7)] for port in range(2)])
    return permanent(rows)


def divides(numerator, denominator):
    if denominator == 0:
        return False
    variables = sorted(numerator.free_symbols | denominator.free_symbols, key=str)
    _quotient, remainder = sp.div(numerator, denominator, *variables, domain=sp.QQ)
    return sp.expand(remainder) == 0


def main() -> None:
    ports0, roots0, endpoint = fixed_model()
    universe = legal_universe(ports0, roots0)
    assert len(universe) == 104
    first_counts = [0] * len(OLD_WORDS)
    survivors = []
    checked = 0
    for support in combinations(universe, 3):
        checked += 1
        ports, roots = extend(ports0, roots0, support)
        pure_product = sp.expand(
            sp.prod(coefficient((colour,) * 7, ports, roots).subs(endpoint) for colour in range(3))
        )
        for index, word in enumerate(OLD_WORDS):
            mixed = sp.expand(coefficient(word, ports, roots).subs(endpoint))
            if divides(pure_product, mixed):
                first_counts[index] += 1
                break
        else:
            survivors.append(support)
    assert checked == 182_104
    assert first_counts == [179_884, 1_768, 326, 5, 0, 112]
    assert tuple(survivors) == EXPECTED_SURVIVORS

    for support in survivors:
        ports, roots = extend(ports0, roots0, support)
        pure_product = sp.expand(
            sp.prod(coefficient((colour,) * 7, ports, roots).subs(endpoint) for colour in range(3))
        )
        final_mixed = sp.expand(coefficient(FINAL_WORD, ports, roots).subs(endpoint))
        assert divides(pure_product, final_mixed)

    print(
        json.dumps(
            {
                "status": "pass",
                "legal_universe": len(universe),
                "triple_supports": checked,
                "first_certificate_counts": dict(zip(OLD_LABELS, first_counts)),
                "relative_survivors": len(survivors),
                "final_certificate": "2002000",
                "final_certificate_supports": len(survivors),
                "triple_shell_survivors": 0,
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
