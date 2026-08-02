"""Independent no-repository-import audit of the unique-pair third shell."""

from __future__ import annotations

import json
from itertools import product

import sympy as sp

PAIR = ((3, 6, 0), (4, 5, 0))
ESCAPE = (5, 5, 2)


def permanent(rows):
    totals = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, scalar in totals.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if entry != 0 and not mask & bit:
                    updated[mask | bit] = updated.get(mask | bit, 0) + scalar * entry
        totals = updated
    return sp.expand(totals.get(127, 0))


def base_arrays():
    names = sp.symbols("a0 a3 a5 a6 b0 b1 b5 b6 X0:5 Y0:5 Z0:5")
    a0, a3, a5, a6, b0, b1, b5, b6, *roots = names
    x, y, z = roots[:5], roots[5:10], roots[10:]
    ports = [[[0] * 3 for _ in range(7)] for _ in range(2)]
    for blocker, colour, value in (
        (0, 0, a0),
        (3, 2, a3),
        (5, 1, a5),
        (6, 1, a6),
    ):
        ports[0][blocker][colour] = value
    for blocker, colour, value in (
        (0, 0, b0),
        (1, 0, b1),
        (5, 2, b5),
        (6, 1, b6),
    ):
        ports[1][blocker][colour] = value
    roots_by_blocker = [[[0] * 3 for _ in range(5)] for _ in range(7)]
    locations = (
        ((2, 0), (3, 1), (4, 2), (5, 3), (6, 4)),
        ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)),
        ((1, 0), (0, 1), (6, 2), (4, 3), (2, 4)),
    )
    for colour, (variables, places) in enumerate(zip((x, y, z), locations)):
        for value, (blocker, root) in zip(variables, places):
            roots_by_blocker[blocker][root][colour] = value
    return names, ports, roots_by_blocker


def legal_missing(ports, roots_by_blocker):
    answer = [
        (root, blocker, colour)
        for root, blocker, colour in product(range(5), range(7), range(3))
        if roots_by_blocker[blocker][root][colour] == 0
    ]
    answer += [
        (5 + port, blocker, colour)
        for port, blocker, colour in product(range(2), (1, 3, 5), range(3))
        if ports[port][blocker][colour] == 0
    ]
    return tuple(answer)


def insert(ports0, roots0, support):
    ports = [[row[:] for row in family] for family in ports0]
    roots = [[row[:] for row in block] for block in roots0]
    variables = sp.symbols(f"q0:{len(support)}")
    for value, (row, blocker, colour) in zip(variables, support):
        if row < 5:
            roots[blocker][row][colour] = value
        else:
            ports[row - 5][blocker][colour] = value
    return variables, ports, roots


def tensor_coefficient(word, ports, roots):
    rows = [[roots[blocker][root][word[blocker]] for blocker in range(7)] for root in range(5)]
    rows += [[ports[port][blocker][word[blocker]] for blocker in range(7)] for port in range(2)]
    return permanent(rows)


def quotient(numerator, denominator):
    if denominator == 0:
        return None
    symbols = sorted(numerator.free_symbols | denominator.free_symbols, key=str)
    result, remainder = sp.div(numerator, denominator, *symbols, domain=sp.QQ)
    return sp.expand(result) if sp.expand(remainder) == 0 else None


def main() -> None:
    names, ports0, roots0 = base_arrays()
    a0, _a3, _a5, a6, b0, _b1, _b5, b6, *_ = names
    endpoint = {a0: 1, a6: 1, b0: 1, b6: -1}
    universe = legal_missing(ports0, roots0)
    assert len(universe) == 104 and all(edge in universe for edge in PAIR)
    thirds = tuple(edge for edge in universe if edge not in PAIR)
    old_word = tuple(map(int, "0101122"))
    new_word = tuple(map(int, "0101112"))
    escapes = []
    old_count = 0
    for edge in thirds:
        _variables, ports, roots = insert(ports0, roots0, PAIR + (edge,))
        pure = sp.expand(
            sp.prod(tensor_coefficient((colour,) * 7, ports, roots).subs(endpoint) for colour in range(3))
        )
        mixed = sp.expand(tensor_coefficient(old_word, ports, roots).subs(endpoint))
        if quotient(pure, mixed) is None:
            escapes.append(edge)
        else:
            old_count += 1
    assert old_count == 101 and escapes == [ESCAPE]

    variables, ports, roots = insert(ports0, roots0, PAIR + (ESCAPE,))
    pure = sp.expand(
        sp.prod(tensor_coefficient((colour,) * 7, ports, roots).subs(endpoint) for colour in range(3))
    )
    mixed = sp.expand(tensor_coefficient(new_word, ports, roots).subs(endpoint))
    replacement = quotient(pure, mixed)
    assert replacement is not None and sp.expand(pure - mixed * replacement) == 0
    assert variables[2] not in pure.free_symbols | mixed.free_symbols

    print(
        json.dumps(
            {
                "status": "pass",
                "legal_universe": len(universe),
                "third_supports": len(thirds),
                "0101122_certificates": old_count,
                "unique_escape": list(ESCAPE),
                "replacement_certificate": "0101112",
                "third_shell_survivors": 0,
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
