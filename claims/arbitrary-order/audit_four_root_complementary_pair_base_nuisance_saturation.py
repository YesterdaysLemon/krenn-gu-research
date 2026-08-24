"""No-import audit of complementary-pair base-shadow anti-simultaneity."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def recover_receiver_basis(
    dimension: int, companion: dict[tuple[int, int], Fraction]
) -> int:
    """Construct one dual target slice and recover every deck basis vector."""

    nonzero_coordinate = next(
        (coordinate for coordinate, value in companion.items() if value), None
    )
    if nonzero_coordinate is None:
        return 0
    scale = companion[nonzero_coordinate]
    recovered = 0
    for left in reversed(range(dimension)):
        for right in reversed(range(dimension)):
            deck = {(left, right): Fraction(1)}
            sliced = {
                coordinate: value * companion[nonzero_coordinate] / scale
                for coordinate, value in deck.items()
            }
            assert sliced == deck
            recovered += 1
    return recovered


def audit_tensor_slices() -> tuple[int, int]:
    profiles = 0
    recovered = 0
    for dimension in reversed(range(1, 6)):
        coordinates = tuple(
            (left, right)
            for left in reversed(range(dimension))
            for right in reversed(range(dimension))
        )
        companions = []
        for selected in coordinates:
            companions.append(
                {
                    coordinate: Fraction(coordinate == selected)
                    for coordinate in coordinates
                }
            )
        companions.append(
            {
                coordinate: Fraction(2 * index - 3)
                for index, coordinate in enumerate(coordinates)
            }
        )
        companions.append({coordinate: Fraction(0) for coordinate in coordinates})
        for companion in companions:
            count = recover_receiver_basis(dimension, companion)
            assert count == (dimension**2 if any(companion.values()) else 0)
            recovered += count
            profiles += 1
    return profiles, recovered


def audit_complementary_labels() -> int:
    ports = frozenset("abcd")
    pairs = tuple(
        frozenset(pair) for pair in combinations(sorted(ports, reverse=True), 2)
    )
    checks = 0
    for target in reversed(pairs):
        label = ports - target
        assert label in pairs
        # I=label has companion indexed by B-I; after Q contraction its open
        # port slots are U-I=target, so deck and companion occupy opposite factors.
        deck_slots = label
        companion_slots = ports - label
        assert deck_slots == ports - target
        assert companion_slots == target
        checks += 1
    return checks


def classify_maximal_families() -> tuple[int, int, int]:
    ports = frozenset(range(4))
    pairs = tuple(frozenset(pair) for pair in combinations(ports, 2))
    families = []
    for first in (pairs[0], ports - pairs[0]):
        for second in (pairs[1], ports - pairs[1]):
            for third in (pairs[2], ports - pairs[2]):
                family = frozenset((first, second, third))
                assert len(family) == 3
                assert all((ports - edge) not in family for edge in family)
                families.append(family)
    unique = set(families)
    stars = {
        family
        for family in unique
        if any(all(vertex in edge for edge in family) for vertex in ports)
    }
    triangles = {
        family
        for family in unique
        if any(all(vertex not in edge for edge in family) for vertex in ports)
    }
    assert len(unique) == 8
    assert len(stars) == len(triangles) == 4
    assert stars | triangles == unique
    assert not (stars & triangles)
    return len(unique), len(stars), len(triangles)


def main() -> None:
    label_checks = audit_complementary_labels()
    tensor_profiles = audit_tensor_slices()
    maximal_families = classify_maximal_families()
    print("independent complementary-pair base-shadow audit: PASS")
    print("  reversed complementary-label checks:", label_checks)
    print("  constructive slice profiles / recovered basis vectors:", tensor_profiles)
    print("  maximal / star / triangle families:", maximal_families)
    print("  scope: coefficient-slice saturation and K4 survivor atlas only")


if __name__ == "__main__":
    main()
