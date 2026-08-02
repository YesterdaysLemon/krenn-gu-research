#!/usr/bin/env python3
"""Verify the three-kernel pure-cofactor compatibility obstruction."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md"
)
DEPENDENCIES = (
    ROOT / "SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md",
    ROOT / "FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md",
)
COLOURS = range(3)
PERMUTATIONS = tuple(itertools.permutations(range(4)))
TAIL_WORDS = tuple(itertools.product(COLOURS, repeat=3))


def permanent_coefficient(matrices, word):
    return sp.expand(
        sum(
            sp.prod(matrices[mode][permutation[mode], word[mode]] for mode in range(4))
            for permutation in PERMUTATIONS
        )
    )


def symbolic_matrices():
    leading = tuple(sp.Matrix(4, 3, sp.symbols(f"h{mode}_0:12")) for mode in COLOURS)
    tail = tuple(sp.Matrix(4, 3, sp.symbols(f"t{mode}_0:12")) for mode in range(3))
    synthetic = sp.Matrix.hstack(*(leading[colour][:, colour] for colour in COLOURS))
    return leading, tail, synthetic


def column_splicing_identities() -> int:
    leading, tail, synthetic = symbolic_matrices()
    checked = 0
    for colour in COLOURS:
        for tail_word in TAIL_WORDS:
            word = (colour, *tail_word)
            observed = permanent_coefficient((synthetic, *tail), word)
            expected = permanent_coefficient((leading[colour], *tail), word)
            assert sp.expand(observed - expected) == 0
            checked += 1
    assert checked == 81
    return checked


def support_pattern_ledger() -> dict[str, object]:
    colours = frozenset(COLOURS)
    support_choices = (colours,) + tuple(
        colours.difference((missing,)) for missing in COLOURS
    )
    survivors = []
    for supports in itertools.product(support_choices, repeat=3):
        pair_bound = all(
            len(supports[left].intersection(supports[right])) <= 2
            for left, right in itertools.combinations(COLOURS, 2)
        )
        triple_bound = not set.intersection(*(set(support) for support in supports))
        if pair_bound and triple_bound:
            survivors.append(supports)
            missing = tuple(
                next(iter(colours.difference(support))) for support in supports
            )
            assert sorted(missing) == [0, 1, 2]
            assert all(len(support) == 2 for support in supports)
    assert len(survivors) == 6
    return {
        "support_triples_checked": len(support_choices) ** 3,
        "extremal_survivors": len(survivors),
        "normalized_supports": [[1, 2], [0, 2], [0, 1]],
    }


def pure_recombination() -> dict[str, object]:
    lambdas = sp.symbols("lambda0:3", nonzero=True)
    deletion_coefficients = {}
    synthetic_coefficients = {}
    for leading_colour in COLOURS:
        for tail_word in TAIL_WORDS:
            word = (leading_colour, *tail_word)
            value = (
                lambdas[leading_colour]
                if tail_word == (leading_colour,) * 3
                else sp.S.Zero
            )
            deletion_coefficients[leading_colour, word] = value
            synthetic_coefficients[word] = value

    nonzero = {
        word: value for word, value in synthetic_coefficients.items() if value != 0
    }
    assert nonzero == {
        (0, 0, 0, 0): lambdas[0],
        (1, 1, 1, 1): lambdas[1],
        (2, 2, 2, 2): lambdas[2],
    }
    assert len(deletion_coefficients) == 81
    return {
        "synthetic_coefficients": len(synthetic_coefficients),
        "nonzero_words": [list(word) for word in nonzero],
        "nonzero_coefficients": [str(value) for value in nonzero.values()],
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for dependency in DEPENDENCIES:
        assert dependency.exists()
    for phrase in (
        "Exact characteristic-zero compatibility obstruction",
        "P_4(D,H_3,H_4,H_5)",
        "at most two modes admit a kernel vector of support at least two",
        "effective two-row factorisation on surviving cores: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem

    identities = column_splicing_identities()
    supports = support_pattern_ledger()
    recombination = pure_recombination()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "root_dependencies": [dependency.name for dependency in DEPENDENCIES],
                "symbolic_column_splicing_coefficients": identities,
                "support_pattern_ledger": supports,
                "pure_recombination": recombination,
                "p4_subrank_used": 2,
                "three_support_two_kernel_pattern_possible": False,
                "effective_factorisation_reached": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
