#!/usr/bin/env python3
"""Replay the isolated protected-seam factorization on two unit K4s.

The verifier checks all 192 color/component/seam/root choices with complete
formal monomial enumeration.  This is an exact finite replay of the local
identity, not a macro-supply or all-order exclusion theorem.
"""

from __future__ import annotations

from collections import Counter

from verify_protected_one_pair_formula import (
    edge_symbol,
    multiply_terms,
    permanent_terms,
    physical_terms,
    protected_partner,
)


def protected_edges(component: int, color: int) -> tuple[tuple[int, int], ...]:
    """Return the two edges of ``M_color`` in one protected component."""

    vertices = tuple(range(4 * component, 4 * component + 4))
    return tuple(
        (u, protected_partner(color, u))
        for u in vertices
        if u < protected_partner(color, u)
    )


def seam_closure_terms(
    pair: tuple[int, int],
    word: tuple[int, ...],
    majority: int,
    resources: tuple[tuple[int, int], ...],
):
    """Return the direct/resource closure factor for one protected seam."""

    r, s = pair
    result = Counter()
    direct = edge_symbol(r, s, word[r], word[s])
    if direct is not None:
        result[direct] += 1
    for u, v in resources:
        for first, second in ((u, v), (v, u)):
            term = multiply_terms(
                edge_symbol(r, first, word[r], majority),
                edge_symbol(s, second, word[s], majority),
            )
            if term is not None:
                result[term] += 1
    return result


def convolve(left, right):
    """Multiply two formal monomial polynomials."""

    result = Counter()
    for first, first_count in left.items():
        for second, second_count in right.items():
            term = multiply_terms(first, second)
            assert term is not None
            result[term] += first_count * second_count
    return result


def replay() -> dict[str, int | str]:
    """Exhaust the two-component protected-seam parameter choices."""

    checked = 0
    for majority in range(3):
        for seam_color in range(3):
            if seam_color == majority:
                continue
            for seam_component, root_component in ((0, 1), (1, 0)):
                for seam in protected_edges(seam_component, seam_color):
                    for root_pair in protected_edges(root_component, majority):
                        other_resources = tuple(
                            edge
                            for edge in protected_edges(root_component, majority)
                            if edge != root_pair
                        )
                        for root_color_x in range(3):
                            if root_color_x == majority:
                                continue
                            for root_color_y in range(3):
                                if root_color_y == majority:
                                    continue
                                word = [majority] * 8
                                r, s = seam
                                x, y = root_pair
                                word[r] = word[s] = seam_color
                                word[x], word[y] = root_color_x, root_color_y
                                frozen_word = tuple(word)

                                columns = (
                                    protected_partner(majority, r),
                                    protected_partner(majority, s),
                                )
                                supplier = permanent_terms(
                                    root_pair, columns, frozen_word
                                )
                                closure = seam_closure_terms(
                                    seam, frozen_word, majority, other_resources
                                )
                                assert physical_terms(frozen_word) == convolve(
                                    supplier, closure
                                )
                                assert len(supplier) == 2
                                assert len(closure) == 3
                                checked += 1

    assert checked == 192
    return {
        "protected_seam_words_exhausted": checked,
        "generic_supplier_terms": 2,
        "generic_closure_terms": 3,
        "status": "EXACT_PROTECTED_SEAM_FACTOR_PASS",
    }


def main() -> None:
    receipt = replay()
    for key, value in receipt.items():
        print(key, value)


if __name__ == "__main__":
    main()
