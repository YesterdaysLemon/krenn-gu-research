#!/usr/bin/env python3
"""Verify the exact two-pair formula and repeated-resource correction.

This finite verifier exhausts the complete ``n=8`` word space.  It checks
the injective-resource formula against literal physical perfect matchings and
also confirms that the ordinary noninjective Wick expansion has genuine
extra terms.  The all-order identity rests on its counting proof.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

from verify_protected_one_pair_formula import (
    collision_count,
    edge_symbol,
    multiply_terms,
    permanent_terms,
    perfect_matchings,
    physical_terms,
    protected_partner,
)


def closure_terms(
    vertices: tuple[int, ...],
    word: tuple[int, ...],
    majority: int,
    resources: tuple[tuple[int, int], ...],
    *,
    injective: bool,
):
    """Expand the boundary hafnian, optionally forbidding resource reuse."""

    result = Counter()
    for matching in perfect_matchings(vertices):
        choices = []
        for r, s in matching:
            pair_choices = []
            direct = edge_symbol(r, s, word[r], word[s])
            if direct is not None:
                pair_choices.append((None, direct))
            for resource_index, (u, v) in enumerate(resources):
                for first, second in ((u, v), (v, u)):
                    term = multiply_terms(
                        edge_symbol(r, first, word[r], majority),
                        edge_symbol(s, second, word[s], majority),
                    )
                    if term is not None:
                        pair_choices.append((resource_index, term))
            choices.append(pair_choices)

        for selected in product(*choices):
            used = [resource for resource, _ in selected if resource is not None]
            if injective and len(used) != len(set(used)):
                continue
            term = multiply_terms(*(factor for _, factor in selected))
            assert term is not None
            result[term] += 1
    return result


def two_pair_formula_terms(
    word: tuple[int, ...], majority: int, *, injective: bool = True
):
    """Expand the exact four-root formula for ``q_majority(word)=2``."""

    minority = tuple(v for v, color in enumerate(word) if color != majority)
    complete_pairs = [
        (u, protected_partner(majority, u))
        for u in range(len(word))
        if u < protected_partner(majority, u)
        and word[u] != majority
        and word[protected_partner(majority, u)] != majority
    ]
    if len(complete_pairs) != 2:
        raise ValueError("two-pair formula requires collision count two")
    roots = {v for pair in complete_pairs for v in pair}
    independent = tuple(v for v in minority if v not in roots)
    partner_columns = tuple(protected_partner(majority, v) for v in independent)
    resources = tuple(
        (u, protected_partner(majority, u))
        for u in range(len(word))
        if u < protected_partner(majority, u)
        and word[u] == word[protected_partner(majority, u)] == majority
    )

    result = Counter()
    for deleted in combinations(minority, 4):
        rows = tuple(v for v in minority if v not in deleted)
        cofactor = permanent_terms(rows, partner_columns, word)
        boundary = closure_terms(
            tuple(deleted), word, majority, resources, injective=injective
        )
        for left, left_multiplicity in cofactor.items():
            for right, right_multiplicity in boundary.items():
                term = multiply_terms(left, right)
                assert term is not None
                result[term] += left_multiplicity * right_multiplicity
    return result


def replay() -> dict[str, object]:
    """Exhaust every applicable ``n=8`` word/majority pair exactly."""

    checked = 0
    naive_failures = 0
    first_extra = None
    for word in product(range(3), repeat=8):
        for majority in range(3):
            if collision_count(word, majority) != 2:
                continue
            exact = physical_terms(word)
            corrected = two_pair_formula_terms(word, majority, injective=True)
            assert exact == corrected, (word, majority)
            naive = two_pair_formula_terms(word, majority, injective=False)
            if naive != exact:
                naive_failures += 1
                if first_extra is None:
                    extra = naive - exact
                    first_extra = (word, majority, next(iter(extra.items())))
            checked += 1

    assert checked == 7200
    assert naive_failures == 96 and first_extra is not None
    return {
        "n8_word_majorities_exhausted": checked,
        "naive_repeated_resource_failures": naive_failures,
        "first_naive_extra": first_extra,
        "status": "EXACT_PROTECTED_TWO_PAIR_RESOURCE_CORRECTION_PASS",
    }


def main() -> None:
    receipt = replay()
    for key, value in receipt.items():
        print(key, value)


if __name__ == "__main__":
    main()
