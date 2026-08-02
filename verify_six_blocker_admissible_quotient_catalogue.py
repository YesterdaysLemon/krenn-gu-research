#!/usr/bin/env python3
"""Exact catalogue of first-surplus blocker profiles and two-copy quotients.

For one fully supported pairwise-zero five-root configuration, every colour
has at least five blockers.  This verifier classifies the possible colour
membership profiles when the blocker union has size six.  It then enumerates
admissible identifications between two such local configurations, retaining
relative colour orientation and forbidding identifications inside either
distinguished local copy.

The result is a combinatorial skeleton only.  It does not assert that any
catalogued quotient is realized by compatible covectors or graph blocks.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter

COLOURS = (0, 1, 2)
PROFILES = tuple(range(1, 8))
COLOUR_PERMUTATIONS = tuple(itertools.permutations(COLOURS))
EXPECTED_CATALOGUE_SHA256 = (
    "c346ca7ce741623d50351a945fddda15bba2d0fff154b4666d78168d6f3ccc58"
)


def permute_profile(profile: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for old_colour in COLOURS:
        if profile & (1 << old_colour):
            result |= 1 << permutation[old_colour]
    return result


def canonical_local(profiles: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted(permute_profile(profile, permutation) for profile in profiles))
        for permutation in COLOUR_PERMUTATIONS
    )


def colour_counts(profiles: tuple[int, ...]) -> tuple[int, int, int]:
    return tuple(
        sum(bool(profile & (1 << colour)) for profile in profiles)
        for colour in COLOURS
    )


def classify_local_orbits() -> tuple[tuple[int, ...], ...]:
    survivors = set()
    for profiles in itertools.combinations_with_replacement(PROFILES, 6):
        if min(colour_counts(profiles)) >= 5:
            survivors.add(canonical_local(profiles))

    candidates = (
        (7, 7, 7, 7, 7, 7),
        (3, 7, 7, 7, 7, 7),
        (1, 7, 7, 7, 7, 7),
        (3, 5, 7, 7, 7, 7),
        (1, 6, 7, 7, 7, 7),
        (3, 5, 6, 7, 7, 7),
    )
    expected = {canonical_local(candidate) for candidate in candidates}
    assert survivors == expected
    assert len(survivors) == 6
    return tuple(sorted(survivors))


def local_name(profiles: tuple[int, ...]) -> str:
    missing_sets = [
        tuple(colour for colour in COLOURS if not profile & (1 << colour))
        for profile in profiles
        if profile != 7
    ]
    missing_sizes = tuple(sorted(map(len, missing_sets)))
    names = {
        (): "all_full",
        (1,): "one_missing_one",
        (2,): "one_missing_two",
        (1, 1): "two_missing_singletons",
        (1, 2): "missing_one_plus_missing_two",
        (1, 1, 1): "three_missing_singletons",
    }
    assert all(size in (1, 2) for size in missing_sizes)
    return names[missing_sizes]


def partial_matchings(size: int) -> tuple[tuple[int, ...], ...]:
    """All partial injections from the left size-set to the right size-set."""

    result = []

    def visit(left: int, used_right: int, assignment: list[int]) -> None:
        if left == size:
            result.append(tuple(assignment))
            return
        assignment.append(-1)
        visit(left + 1, used_right, assignment)
        assignment.pop()
        for right in range(size):
            if used_right & (1 << right):
                continue
            assignment.append(right)
            visit(left + 1, used_right | (1 << right), assignment)
            assignment.pop()

    visit(0, 0, [])
    return tuple(result)


def incidence_matrix(
    left_profiles: tuple[int, ...],
    right_profiles: tuple[int, ...],
    matching: tuple[int, ...],
) -> tuple[int, ...]:
    counts = Counter(
        (left_profiles[left], right_profiles[right])
        for left, right in enumerate(matching)
        if right >= 0
    )
    return tuple(counts[(left, right)] for left in PROFILES for right in PROFILES)


def transform_matrix(
    matrix: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    transformed = Counter()
    for left in PROFILES:
        for right in PROFILES:
            count = matrix[(left - 1) * 7 + right - 1]
            if count:
                transformed[
                    (
                        permute_profile(left, permutation),
                        permute_profile(right, permutation),
                    )
                ] += count
    return tuple(
        transformed[(left, right)] for left in PROFILES for right in PROFILES
    )


def transpose_matrix(matrix: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        matrix[(right - 1) * 7 + left - 1]
        for left in PROFILES
        for right in PROFILES
    )


def canonical_pair_signature(
    left_profiles: tuple[int, ...],
    right_profiles: tuple[int, ...],
    matrix: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    candidates = []
    for permutation in COLOUR_PERMUTATIONS:
        left = tuple(
            sorted(permute_profile(profile, permutation) for profile in left_profiles)
        )
        right = tuple(
            sorted(permute_profile(profile, permutation) for profile in right_profiles)
        )
        transformed = transform_matrix(matrix, permutation)
        candidates.append((left, right, transformed))
        candidates.append((right, left, transpose_matrix(transformed)))
    return min(candidates)


def oriented_profiles(profiles: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                tuple(
                    sorted(
                        permute_profile(profile, permutation)
                        for profile in profiles
                    )
                )
                for permutation in COLOUR_PERMUTATIONS
            }
        )
    )


def pair_catalogue(
    left_profiles: tuple[int, ...],
    right_profiles: tuple[int, ...],
    matchings: tuple[tuple[int, ...], ...],
) -> set[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]]:
    signatures = set()
    for oriented_right in oriented_profiles(right_profiles):
        # Many of the 13,327 labelled partial matchings differ only by
        # permuting blockers with the same local profile.  Collapse those
        # labelled matchings before the more expensive colour/swap orbit step.
        raw_matrices = {
            incidence_matrix(left_profiles, oriented_right, matching)
            for matching in matchings
        }
        for matrix in raw_matrices:
            signatures.add(
                canonical_pair_signature(left_profiles, oriented_right, matrix)
            )
    return signatures


def main() -> None:
    local_orbits = classify_local_orbits()
    names = {profiles: local_name(profiles) for profiles in local_orbits}
    matchings = partial_matchings(6)
    assert len(matchings) == 13327

    pair_summaries = []
    digest_lines = []
    blocker_quotient_orbits = 0
    fully_disjoint_orbits = 0
    for left_index, left_profiles in enumerate(local_orbits):
        for right_profiles in local_orbits[left_index:]:
            signatures = pair_catalogue(left_profiles, right_profiles, matchings)
            histogram = Counter(sum(signature[2]) for signature in signatures)
            left_name = names[left_profiles]
            right_name = names[right_profiles]
            histogram_text = ",".join(
                f"{shared}:{histogram[shared]}" for shared in sorted(histogram)
            )
            digest_lines.append(
                f"{left_name}|{right_name}|{len(signatures)}|{histogram_text}"
            )
            pair_summaries.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "blocker_quotient_orbits": len(signatures),
                    "shared_blocker_histogram": dict(sorted(histogram.items())),
                }
            )
            blocker_quotient_orbits += len(signatures)
            fully_disjoint_orbits += histogram[0]

    digest = hashlib.sha256("\n".join(sorted(digest_lines)).encode()).hexdigest()
    if EXPECTED_CATALOGUE_SHA256:
        assert digest == EXPECTED_CATALOGUE_SHA256

    root_overlap_orbits = 6  # intersection size 0, 1, ..., 5
    decorated_orbits = root_overlap_orbits * blocker_quotient_orbits
    # A fully disjoint template has root-overlap zero and blocker-overlap zero.
    # Relative global colour orientations can leave more than one such orbit
    # for a fixed pair of non-rigid local profile types.
    non_disjoint_orbits = decorated_orbits - fully_disjoint_orbits

    print(
        json.dumps(
            {
                "status": "verified",
                "local_six_blocker_orbits": [
                    {
                        "name": names[profiles],
                        "profiles": profiles,
                        "colour_degrees": colour_counts(profiles),
                    }
                    for profiles in local_orbits
                ],
                "partial_matchings_per_oriented_pair": len(matchings),
                "relative_colour_orientations_retained": True,
                "pair_summaries": pair_summaries,
                "blocker_quotient_orbits": blocker_quotient_orbits,
                "root_overlap_orbits": root_overlap_orbits,
                "decorated_two_copy_orbits": decorated_orbits,
                "fully_disjoint_decorated_orbits": fully_disjoint_orbits,
                "non_disjoint_decorated_orbits": non_disjoint_orbits,
                "catalogue_sha256": digest,
                "scope": "combinatorial incidence skeleton",
                "covector_realizability_checked": False,
                "global_krenn_gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
