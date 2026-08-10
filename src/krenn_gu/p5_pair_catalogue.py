"""Deterministic P5 pair-signature catalogue construction.

The construction is shared below the claim verifier and the Boolean support
semantics.  It preserves the exact F5 enumeration order and counts; it does
not by itself assert the characteristic-zero coverage theorem.
"""

from __future__ import annotations

import itertools

from krenn_gu import five_row_f5 as f5


SOURCES = tuple(range(5))
COLOURS = tuple(range(3))


def support(row: tuple[int, ...]) -> int:
    return sum(
        (value != 0) << index for index, value in enumerate(row)
    )


def coordinate_mask(rows: tuple[tuple[int, ...], ...]) -> int:
    rank = f5.rank_mod(rows)
    return sum(
        (f5.rank_mod(rows + (coordinate,)) == rank) << colour
        for colour, coordinate in enumerate(f5.COORDINATES)
    )


def base_signature(rows: tuple[tuple[int, ...], ...]) -> tuple:
    supports = tuple(support(row) for row in rows)
    subsets = tuple(
        subset
        for size in (2, 3, 4)
        for subset in itertools.combinations(SOURCES, size)
    )
    incidences = tuple(
        coordinate_mask(tuple(rows[index] for index in subset))
        for subset in subsets
    )
    return supports, incidences


def permute_signature(
    signature: tuple, permutation: tuple[int, ...]
) -> tuple:
    subsets = tuple(
        subset
        for size in (2, 3, 4)
        for subset in itertools.combinations(SOURCES, size)
    )
    subset_index = {subset: index for index, subset in enumerate(subsets)}
    supports, incidences = signature
    new_supports = tuple(
        supports[permutation[index]] for index in SOURCES
    )
    new_incidences = []
    for subset in subsets:
        old_subset = tuple(sorted(permutation[index] for index in subset))
        new_incidences.append(incidences[subset_index[old_subset]])
    return new_supports, tuple(new_incidences)


def finite_field_local_signatures() -> tuple[tuple, ...]:
    points = (f5.ZERO,) + tuple(
        sorted(
            {
                f5.canonical(vector)
                for vector in itertools.product(range(f5.PRIME), repeat=3)
                if any(vector)
            }
        )
    )
    pair_condition = tuple(
        tuple(
            f5.pair_contains_coordinate(left, right)
            for right in points
        )
        for left in points
    )
    result = set()
    retained = 0
    for indices in itertools.combinations_with_replacement(
        range(len(points)), 5
    ):
        if any(
            not pair_condition[indices[first]][indices[second]]
            for first, second in itertools.combinations(range(5), 2)
        ):
            continue
        rows = tuple(points[index] for index in indices)
        if f5.rank_mod(rows) != 3:
            continue
        retained += 1
        base = base_signature(rows)
        for permutation in itertools.permutations(SOURCES):
            result.add(permute_signature(base, permutation))
    if retained != 2556:
        raise AssertionError("finite-field retained count changed")
    catalogue = tuple(sorted(result))
    if len(catalogue) != 6495:
        raise AssertionError("pair-signature catalogue count changed")
    return catalogue


__all__ = ["finite_field_local_signatures"]
