#!/usr/bin/env python3
"""No-import audit of three pure-cofactor column compatibility."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md"
)
PERMUTATIONS = tuple(itertools.permutations(range(4)))
COLOURS = (0, 1, 2)


def permanent(matrices, word) -> int:
    total = 0
    for permutation in PERMUTATIONS:
        product = 1
        for mode in range(4):
            product *= matrices[mode][permutation[mode]][word[mode]]
        total += product
    return total


def integer_data():
    leading = (
        ((1, 2, -1), (0, 1, 3), (2, -1, 1), (1, 0, 2)),
        ((2, 0, 1), (-1, 3, 2), (1, 1, -2), (0, 2, 3)),
        ((1, -2, 0), (3, 1, 2), (-1, 0, 1), (2, 2, -3)),
    )
    tail = (
        ((2, 1, -1), (1, -2, 0), (0, 3, 2), (-1, 1, 1)),
        ((1, 0, 2), (-2, 1, 3), (3, -1, 0), (1, 2, -2)),
        ((0, 2, 1), (2, -1, -2), (1, 3, 0), (-1, 0, 2)),
    )
    synthetic = tuple(
        tuple(leading[colour][row][colour] for colour in COLOURS) for row in range(4)
    )
    return leading, tail, synthetic


def integer_splicing_audit() -> dict[str, int]:
    leading, tail, synthetic = integer_data()
    checked = 0
    nonzero_observed = 0
    for colour in COLOURS:
        for tail_word in itertools.product(COLOURS, repeat=3):
            word = (colour, *tail_word)
            observed = permanent((synthetic, *tail), word)
            expected = permanent((leading[colour], *tail), word)
            assert observed == expected
            nonzero_observed += observed != 0
            checked += 1
    assert checked == 81
    assert nonzero_observed > 0
    return {
        "coefficients_checked": checked,
        "nonzero_sample_coefficients": nonzero_observed,
    }


def pure_table_audit() -> dict[str, object]:
    lambdas = (2, -3, 5)
    synthetic = {}
    for colour in COLOURS:
        for tail_word in itertools.product(COLOURS, repeat=3):
            synthetic[colour, *tail_word] = (
                lambdas[colour] if tail_word == (colour,) * 3 else 0
            )
    nonzero = {word: value for word, value in synthetic.items() if value}
    assert nonzero == {
        (0, 0, 0, 0): 2,
        (1, 1, 1, 1): -3,
        (2, 2, 2, 2): 5,
    }
    return {
        "coefficients": len(synthetic),
        "nonzero_coefficients": {
            "".join(map(str, word)): value for word, value in nonzero.items()
        },
    }


def support_audit() -> dict[str, int]:
    colours = frozenset(COLOURS)
    choices = (colours,) + tuple(colours.difference((colour,)) for colour in COLOURS)
    checked = 0
    survivors = 0
    for supports in itertools.product(choices, repeat=3):
        checked += 1
        if any(
            len(supports[left].intersection(supports[right])) == 3
            for left, right in itertools.combinations(COLOURS, 2)
        ):
            continue
        if set.intersection(*(set(support) for support in supports)):
            continue
        missing = [colours.difference(support) for support in supports]
        assert all(len(item) == 1 for item in missing)
        assert set().union(*missing) == set(COLOURS)
        survivors += 1
    assert checked == 64
    assert survivors == 6
    return {"patterns_checked": checked, "extremal_patterns": survivors}


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    normalized = " ".join(theorem.split())
    assert "No finite-field inference is used" in normalized
    assert "torus J_H with at most two such modes: UNKNOWN" in theorem

    splicing = integer_splicing_audit()
    pure = pure_table_audit()
    supports = support_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent integer column-splicing reconstruction",
                "field": "rational characteristic zero",
                "column_splicing": splicing,
                "pure_recombination": pure,
                "support_ledger": supports,
                "finite_field_used": False,
                "effective_factorisation_reached": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
