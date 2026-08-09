#!/usr/bin/env python3
"""Independent contingency-matrix audit of the six-blocker catalogue.

The primary verifier starts from labelled partial matchings.  This audit
instead derives the six local types from missing-colour assignments and
enumerates every feasible profile-by-profile contingency matrix directly.
It imports no code or data from the primary verifier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter

BITS = (0, 1, 2)
MASKS = tuple(range(1, 8))
PERMS = tuple(itertools.permutations(BITS))
PINNED_DIGEST = "c346ca7ce741623d50351a945fddda15bba2d0fff154b4666d78168d6f3ccc58"


def move_mask(mask: int, permutation: tuple[int, ...]) -> int:
    image = 0
    for source in BITS:
        if mask & (1 << source):
            image |= 1 << permutation[source]
    return image


def normalize_single(profile_multiset: tuple[int, ...]) -> tuple[int, ...]:
    images = []
    for permutation in PERMS:
        images.append(
            tuple(sorted(move_mask(mask, permutation) for mask in profile_multiset))
        )
    return min(images)


def derive_local_types_from_missing_owners() -> tuple[tuple[int, ...], ...]:
    """Assign each colour to at most one blocker at which it is missing."""

    types = set()
    # Owner -1 means that the colour is present at all six blockers.
    for owners in itertools.product(range(-1, 6), repeat=3):
        profiles = [7] * 6
        for colour, owner in enumerate(owners):
            if owner >= 0:
                profiles[owner] &= ~(1 << colour)
        if 0 in profiles:
            continue
        types.add(normalize_single(tuple(sorted(profiles))))
    assert len(types) == 6
    return tuple(sorted(types))


def type_name(profiles: tuple[int, ...]) -> str:
    defects = sorted(3 - mask.bit_count() for mask in profiles if mask != 7)
    return {
        (): "all_full",
        (1,): "one_missing_one",
        (2,): "one_missing_two",
        (1, 1): "two_missing_singletons",
        (1, 2): "missing_one_plus_missing_two",
        (1, 1, 1): "three_missing_singletons",
    }[tuple(defects)]


def relative_orientations(profiles: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                tuple(sorted(move_mask(mask, permutation) for mask in profiles))
                for permutation in PERMS
            }
        )
    )


def row_choices(limit: int, column_caps: tuple[int, ...]):
    allocation = [0] * len(column_caps)

    def visit(column: int, used: int):
        if column == len(column_caps):
            yield tuple(allocation)
            return
        maximum = min(column_caps[column], limit - used)
        for value in range(maximum + 1):
            allocation[column] = value
            yield from visit(column + 1, used + value)
        allocation[column] = 0

    yield from visit(0, 0)


def feasible_matrices(
    left_profiles: tuple[int, ...], right_profiles: tuple[int, ...]
) -> set[tuple[int, ...]]:
    left_counts = Counter(left_profiles)
    right_counts = Counter(right_profiles)
    left_masks = tuple(sorted(left_counts))
    right_masks = tuple(sorted(right_counts))
    result = set()
    entries = [[0] * 7 for _ in range(7)]

    def visit(row_index: int, remaining_columns: tuple[int, ...]) -> None:
        if row_index == len(left_masks):
            result.add(tuple(entry for row in entries for entry in row))
            return
        left_mask = left_masks[row_index]
        for allocation in row_choices(left_counts[left_mask], remaining_columns):
            for position, right_mask in enumerate(right_masks):
                entries[left_mask - 1][right_mask - 1] = allocation[position]
            visit(
                row_index + 1,
                tuple(
                    cap - used
                    for cap, used in zip(
                        remaining_columns, allocation, strict=True
                    )
                ),
            )
            for right_mask in right_masks:
                entries[left_mask - 1][right_mask - 1] = 0

    visit(0, tuple(right_counts[mask] for mask in right_masks))
    return result


def recolour_matrix(
    matrix: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    result = [[0] * 7 for _ in range(7)]
    for left in MASKS:
        for right in MASKS:
            value = matrix[(left - 1) * 7 + right - 1]
            if value:
                new_left = move_mask(left, permutation)
                new_right = move_mask(right, permutation)
                result[new_left - 1][new_right - 1] += value
    return tuple(entry for row in result for entry in row)


def matrix_transpose(matrix: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        matrix[(right - 1) * 7 + left - 1]
        for left in MASKS
        for right in MASKS
    )


def normalize_pair(
    left_profiles: tuple[int, ...],
    right_profiles: tuple[int, ...],
    matrix: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    orbit = []
    for permutation in PERMS:
        left = tuple(sorted(move_mask(mask, permutation) for mask in left_profiles))
        right = tuple(sorted(move_mask(mask, permutation) for mask in right_profiles))
        moved = recolour_matrix(matrix, permutation)
        orbit.append((left, right, moved))
        orbit.append((right, left, matrix_transpose(moved)))
    return min(orbit)


def main() -> None:
    local_types = derive_local_types_from_missing_owners()
    labels = {profiles: type_name(profiles) for profiles in local_types}
    summaries = []
    digest_lines = []
    total = 0
    fully_disjoint = 0
    for left_index, left_profiles in enumerate(local_types):
        for right_profiles in local_types[left_index:]:
            normalized = set()
            for oriented_right in relative_orientations(right_profiles):
                for matrix in feasible_matrices(left_profiles, oriented_right):
                    normalized.add(
                        normalize_pair(left_profiles, oriented_right, matrix)
                    )
            histogram = Counter(sum(signature[2]) for signature in normalized)
            left_name = labels[left_profiles]
            right_name = labels[right_profiles]
            histogram_text = ",".join(
                f"{shared}:{histogram[shared]}" for shared in sorted(histogram)
            )
            digest_lines.append(
                f"{left_name}|{right_name}|{len(normalized)}|{histogram_text}"
            )
            summaries.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "quotient_orbits": len(normalized),
                    "shared_histogram": dict(sorted(histogram.items())),
                }
            )
            total += len(normalized)
            fully_disjoint += histogram[0]

    digest = hashlib.sha256("\n".join(sorted(digest_lines)).encode()).hexdigest()
    assert digest == PINNED_DIGEST
    assert total == 1791
    assert fully_disjoint == 31

    print(
        json.dumps(
            {
                "status": "verified",
                "method": "independent missing-owner and contingency-matrix audit",
                "local_types": [labels[profiles] for profiles in local_types],
                "blocker_quotient_orbits": total,
                "root_overlap_orbits": 6,
                "decorated_two_copy_orbits": 6 * total,
                "fully_disjoint_decorated_orbits": fully_disjoint,
                "non_disjoint_decorated_orbits": 6 * total - fully_disjoint,
                "catalogue_sha256": digest,
                "pair_summaries": summaries,
                "covector_realizability_checked": False,
                "global_krenn_gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
