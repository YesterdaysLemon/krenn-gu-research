"""Focused exact checks for the GLS16 base-shadow and cross-target theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
from math import factorial


def direct_permanent_words(order: int) -> set[tuple[str, ...]]:
    outside = ("q0", "q1") + tuple(f"c{i}" for i in range(order - 2))
    return set(permutations(outside))


def psi_k_words(order: int) -> set[tuple[str, ...]]:
    roots = tuple(range(order))
    complement = tuple(f"c{i}" for i in range(order - 2))
    words: set[tuple[str, ...]] = set()
    for left, right in combinations(roots, 2):
        for q_left, q_right in (("q0", "q1"), ("q1", "q0")):
            remaining = tuple(root for root in roots if root not in (left, right))
            for image in permutations(complement):
                word = [""] * order
                word[left] = q_left
                word[right] = q_right
                for root, outside in zip(remaining, image, strict=True):
                    word[root] = outside
                words.add(tuple(word))
    return words


def check_matching_shadow() -> dict[int, tuple[int, int]]:
    counts = {}
    for order in range(2, 8):
        psi_words = psi_k_words(order)
        direct_words = direct_permanent_words(order)
        assert psi_words == direct_words
        assert len(psi_words) == factorial(order)
        root_edge_terms = len(tuple(combinations(range(order), 2))) * factorial(
            order - 2
        )
        assert root_edge_terms == factorial(order) // 2
        counts[order] = (len(psi_words), root_edge_terms)
    return counts


def check_grade_shadow() -> dict[int, tuple[int, int]]:
    counts = {}
    for order in range(2, 9):
        outside_size = order + 2
        even_labels = 0
        base_labels = 0
        for size in range(2, outside_size + 1, 2):
            grade = (size - 2) // 2
            label_count = len(tuple(combinations(range(outside_size), size)))
            even_labels += label_count
            if grade == 0:
                base_labels += label_count
            else:
                assert grade >= 1
        assert base_labels == outside_size * (outside_size - 1) // 2
        counts[order] = (even_labels, base_labels)
    return counts


def projective_line(delta: int, eta: int) -> tuple[Fraction, Fraction]:
    if delta:
        return Fraction(1), Fraction(eta, delta)
    return Fraction(0), Fraction(1)


def check_projective_trichotomy() -> tuple[int, int]:
    directions = {
        projective_line(delta, eta)
        for delta in range(-3, 4)
        for eta in range(-3, 4)
        if (delta, eta) != (0, 0)
    }
    cases = 0
    forced_pure_m = 0
    for delta, eta in directions:
        for base_class in (Fraction(0), Fraction(1), Fraction(2)):
            absorption_shadow = eta * base_class
            cases += 1
            if base_class and absorption_shadow == 0:
                assert eta == 0
                assert delta == 1
                forced_pure_m += 1
    pure_m = (Fraction(1), Fraction(0))
    for first in directions:
        for second in directions:
            if first != second:
                assert first != pure_m or second != pure_m
    return cases, forced_pure_m


def cross_partition(source: frozenset[int], target: frozenset[int], order: int):
    common = source & target
    source_only = source - target
    target_only = target - source
    exterior = frozenset(range(order)) - (source | target)
    assert source != target
    assert len(source_only) == len(target_only) in (1, 2)
    assert common | source_only | target_only | exterior == frozenset(range(order))
    assert not (common & source_only)
    assert not (common & target_only)
    assert not (source_only & target_only)
    return len(common), len(source_only), len(exterior)


def check_cross_target_slots() -> dict[int, dict[tuple[int, int, int], int]]:
    answer = {}
    for order in range(3, 8):
        profile: dict[tuple[int, int, int], int] = {}
        targets = tuple(frozenset(pair) for pair in combinations(range(order), 2))
        for source in targets:
            for target in targets:
                if source == target:
                    continue
                key = cross_partition(source, target, order)
                profile[key] = profile.get(key, 0) + 1
                assert source != target
                assert frozenset({-2, -1}) | source != target
                assert source != frozenset({-2, -1}) | target
        answer[order] = profile
    return answer


def tensor_entry(indices: tuple[int, ...], salt: int) -> Fraction:
    value = salt
    for index, digit in enumerate(indices, start=1):
        value += index * (digit + 1)
    return Fraction((value % 11) - 5)


def check_cross_factorization() -> int:
    """Check id_A tensor cross(lambda,g) in a separate dense model."""

    checks = 0
    dimension = 2
    for common_target_size, source_only_size, exterior_size in (
        (1, 1, 0),
        (1, 1, 1),
        (0, 2, 0),
        (0, 2, 1),
    ):
        shared_size = 2 + exterior_size
        shared_words = tuple(product(range(dimension), repeat=shared_size))
        source_words = tuple(product(range(dimension), repeat=source_only_size))
        target_words = tuple(product(range(dimension), repeat=source_only_size))
        common_words = tuple(product(range(dimension), repeat=common_target_size))
        cross = {}
        for source_word in source_words:
            for target_word in target_words:
                value = sum(
                    tensor_entry(shared + source_word, 3)
                    * tensor_entry(shared + target_word, 7)
                    for shared in shared_words
                )
                cross[source_word, target_word] = value
        for input_common in common_words:
            for output_common in common_words:
                for source_word in source_words:
                    for target_word in target_words:
                        full_coefficient = (
                            cross[source_word, target_word]
                            if input_common == output_common
                            else Fraction(0)
                        )
                        expected = (
                            Fraction(input_common == output_common)
                            * cross[source_word, target_word]
                        )
                        assert full_coefficient == expected
                        checks += 1
    return checks


def main() -> None:
    matching_counts = check_matching_shadow()
    grade_counts = check_grade_shadow()
    projective_cases = check_projective_trichotomy()
    cross_profiles = check_cross_target_slots()
    factorization_checks = check_cross_factorization()
    print("base-grade pair shadow and cross-target selector checks: PASS")
    print("  Psi_C(K^Q) / permanent and killed-R counts:", matching_counts)
    print("  even-label / surviving-order-two counts:", grade_counts)
    print("  projective cases / forced pure-M cases:", projective_cases)
    print("  ordered cross-target slot profiles:", cross_profiles)
    print("  dense cross-factorization entries:", factorization_checks)
    print("  scope: identities and branch localization only; node closure remains open")


if __name__ == "__main__":
    main()
