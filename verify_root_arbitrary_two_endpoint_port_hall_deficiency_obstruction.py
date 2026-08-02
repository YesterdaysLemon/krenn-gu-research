"""Verify the exact two-port Hall deficiency of the odd-blocker gadget."""

from __future__ import annotations

import json
from itertools import combinations

import sympy as sp


def port_rows(blocker_count: int) -> tuple[list[list[int]], list[list[int]]]:
    a = [[0, 0, 0] for _ in range(blocker_count)]
    b = [[0, 0, 0] for _ in range(blocker_count)]
    a[0], a[1], a[-1] = [1, 0, 0], [0, 0, 1], [0, 1, 0]
    b[0], b[1], b[-1] = [1, 0, 0], [0, 0, 1], [0, -1, 0]
    return a, b


def permanent(matrix: list[list[int]]) -> int:
    size = len(matrix)
    totals = {0: 1}
    for row in matrix:
        updated: dict[int, int] = {}
        for mask, coefficient in totals.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if value and not mask & bit:
                    new_mask = mask | bit
                    updated[new_mask] = updated.get(new_mask, 0) + coefficient * value
        totals = updated
    return totals.get((1 << size) - 1, 0)


def deterministic_root_rows(blocker_count: int, word: tuple[int, ...]) -> list[list[int]]:
    root_count = blocker_count - 2
    rows = [[0 for _ in range(blocker_count)] for _ in range(root_count)]
    # The root rows use the final m-2 blocker columns as an identity.  This is
    # a legal specialization of the arbitrary H entries for the selected word.
    for row in range(root_count):
        rows[row][row + 2] = 1 + ((row + word[row + 2]) % 3)
    return rows


def coefficient_matrix(blocker_count: int, word: tuple[int, ...]) -> list[list[int]]:
    a, b = port_rows(blocker_count)
    roots = deterministic_root_rows(blocker_count, word)
    return roots + [
        [a[column][word[column]] for column in range(blocker_count)],
        [b[column][word[column]] for column in range(blocker_count)],
    ]


def symbolic_seven_blocker_check() -> dict[str, object]:
    blocker_count = 7
    a, b = port_rows(blocker_count)
    cofactor_symbols = {
        (u, v, colour): sp.Symbol(f"R{u}{v}_{colour}")
        for u, v in combinations(range(blocker_count), 2)
        for colour in range(3)
    }
    expressions = []
    support_pairs = []
    for colour in range(3):
        terms = []
        nonzero_pairs = []
        for u, v in combinations(range(blocker_count), 2):
            port_minor = a[u][colour] * b[v][colour] + b[u][colour] * a[v][colour]
            terms.append(port_minor * cofactor_symbols[u, v, colour])
            if port_minor:
                nonzero_pairs.append((u, v))
        expression = sp.expand(sum(terms))
        assert expression == 0
        expressions.append(expression)
        support_pairs.append(nonzero_pairs)
    assert support_pairs == [[], [], []]
    return {
        "blockers": blocker_count,
        "symbolic_root_cofactors": len(cofactor_symbols),
        "pure_expressions": [str(expression) for expression in expressions],
        "nonzero_port_pairs": support_pairs,
    }


def bounded_permanent_checks() -> list[dict[str, int]]:
    rows = []
    for blocker_count in range(5, 16, 2):
        pure_values = []
        for colour in range(3):
            word = (colour,) * blocker_count
            value = permanent(coefficient_matrix(blocker_count, word))
            assert value == 0
            pure_values.append(value)

        # A mixed control assigns the two ports to columns 0 and 1, while the
        # deterministic root identity uses columns 2,...,m-1.
        mixed_word = (0, 2) + (0,) * (blocker_count - 2)
        mixed_value = permanent(coefficient_matrix(blocker_count, mixed_word))
        expected = 2
        for row in range(blocker_count - 2):
            expected *= 1 + ((row + mixed_word[row + 2]) % 3)
        assert mixed_value == expected != 0
        rows.append(
            {
                "blockers": blocker_count,
                "pure_0": pure_values[0],
                "pure_1": pure_values[1],
                "pure_2": pure_values[2],
                "mixed_control": mixed_value,
            }
        )
    return rows


def hall_support_check(blocker_count: int) -> dict[str, object]:
    a, b = port_rows(blocker_count)
    supports = []
    for colour in range(3):
        support_a = [u for u in range(blocker_count) if a[u][colour]]
        support_b = [u for u in range(blocker_count) if b[u][colour]]
        assert support_a == support_b and len(support_a) == 1
        supports.append({"colour": colour, "a": support_a, "b": support_b})
    return {"blockers": blocker_count, "supports": supports}


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "symbolic_m7": symbolic_seven_blocker_check(),
                "hall_support": [hall_support_check(m) for m in range(5, 16, 2)],
                "bounded_permanents": bounded_permanent_checks(),
                "all_pure_coefficients_zero": True,
                "mixed_permanent_map_identically_zero": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
