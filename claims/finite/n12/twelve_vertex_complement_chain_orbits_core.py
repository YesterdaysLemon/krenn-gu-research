"""Pure orbit machinery for the hard twelve-vertex complement profile."""

from __future__ import annotations

import itertools

N = 12
SIDE = N // 2
FULL = (1 << N) - 1
LEFT = (1 << SIDE) - 1


def balanced(mask: int) -> bool:
    return (
        mask != 0
        and mask.bit_count() % 2 == 0
        and (mask & LEFT).bit_count()
        == (mask >> SIDE).bit_count()
    )


def membership_variables():
    variable = {}
    next_variable = 1
    for colour in range(3):
        for mask in range(1, FULL + 1):
            if balanced(mask):
                variable[colour, mask] = next_variable
                next_variable += 1
    return variable


def partner_orbits(values, group):
    remaining = set(values)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = sorted(
            {permutation[representative] for permutation in group}
        )
        if not set(orbit) <= remaining:
            raise AssertionError(
                "stabilizer did not preserve remaining columns"
            )
        orbits.append(orbit)
        remaining.difference_update(orbit)
    return orbits


def canonical_leaves():
    initial_group = [
        permutation
        for permutation in itertools.permutations(range(SIDE))
        if permutation[0] == 0 and permutation[1] == 1
    ]
    leaves = []

    def recurse(pairs, used_rows, used_columns, group, orbit_weight):
        if len(pairs) == SIDE:
            leaves.append(
                {
                    "pairs": tuple(pairs),
                    "partner_permutation": tuple(
                        column for _row, column in pairs
                    ),
                    "orbit_weight": orbit_weight,
                }
            )
            return

        row = min(set(range(SIDE)) - set(used_rows))
        row_stabilizer = [
            permutation
            for permutation in group
            if permutation[row] == row
        ]
        available_columns = sorted(
            set(range(SIDE)) - set(used_columns)
        )
        for orbit in partner_orbits(available_columns, row_stabilizer):
            column = orbit[0]
            next_group = [
                permutation
                for permutation in row_stabilizer
                if permutation[column] == column
            ]
            recurse(
                pairs + [(row, column)],
                used_rows + [row],
                used_columns + [column],
                next_group,
                orbit_weight * len(orbit),
            )

    recurse([(0, 1)], [0], [1], initial_group, 1)
    if len(leaves) != 16:
        raise AssertionError(f"expected 16 leaves, got {len(leaves)}")
    if sum(leaf["orbit_weight"] for leaf in leaves) != 120:
        raise AssertionError("canonical leaves do not cover all 5! chains")
    if len({leaf["partner_permutation"] for leaf in leaves}) != len(leaves):
        raise AssertionError("duplicate canonical leaves")
    return leaves


def chain_assumptions(variable, pairs):
    remainder = FULL
    assumptions = []
    pair_masks = []
    suffix_masks = []
    for row, column in pairs:
        pair = (1 << row) | (1 << (column + SIDE))
        if pair & remainder != pair:
            raise AssertionError("matching chain reused a vertex")
        pair_masks.append(pair)
        assumptions.append(variable[1, pair])
        remainder ^= pair
        if remainder:
            suffix_masks.append(remainder)
            assumptions.append(variable[1, remainder])
    if remainder:
        raise AssertionError("matching chain did not cover the profile")
    return assumptions, pair_masks, suffix_masks


__all__ = [
    "FULL",
    "SIDE",
    "canonical_leaves",
    "chain_assumptions",
    "membership_variables",
]
