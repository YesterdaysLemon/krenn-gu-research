"""Independent no-import audit of adjacent five-set boundary overlap."""

from __future__ import annotations

from collections import Counter
from math import comb

COMMON = (0, 1, 2, 3)
LEFT_VERTICES = (0, 1, 2, 3, 4)
RIGHT_VERTICES = (0, 1, 2, 3, 5)

Selector = tuple[int, int, int]


def selector_words(vertices: tuple[int, ...]) -> tuple[Selector, ...]:
    """Decode all nonconstant selectors from base-five integers."""
    words: list[Selector] = []
    base = len(vertices)
    for code in range(base**3):
        value = code
        digits: list[int] = []
        for _ in range(3):
            digits.append(vertices[value % base])
            value //= base
        word = tuple(digits)
        if not (word[0] == word[1] == word[2]):
            words.append(word)
    return tuple(words)


def colour_masks(selector: Selector, vertices: tuple[int, ...]) -> dict[int, int]:
    """Encode coordinate-zero sets as three-bit integers."""
    masks = {vertex: 0 for vertex in vertices}
    for colour, vertex in enumerate(selector):
        masks[vertex] |= 1 << colour
    return masks


def exact_stratum_states(
    left_masks: dict[int, int], right_masks: dict[int, int]
) -> Counter[tuple[int, int]]:
    """Dynamic-program exact sync choices, tracking count and total codimension cost."""
    states: Counter[tuple[int, int]] = Counter({(0, 0): 1})
    for vertex in COMMON:
        left = left_masks[vertex]
        right = right_masks[vertex]
        intersection_size = (left & right).bit_count()
        union_size = (left | right).bit_count()

        sync_feasible = union_size <= 2
        sync_cost = 2 - intersection_size
        nonsync_forced_empty = left == right and left.bit_count() == 2

        options: list[tuple[int, int]] = []
        if not nonsync_forced_empty:
            options.append((0, 0))
        if sync_feasible:
            options.append((1, sync_cost))
        assert options

        updated: Counter[tuple[int, int]] = Counter()
        for (sync_count, cost), multiplicity in states.items():
            for sync_increment, cost_increment in options:
                updated[
                    (sync_count + sync_increment, cost + cost_increment)
                ] += multiplicity
        states = updated
    return states


def audit_selector_strata() -> dict[str, object]:
    """Audit the finite stratification by a dynamic programme."""
    left_words = selector_words(LEFT_VERTICES)
    right_words = selector_words(RIGHT_VERTICES)
    assert len(left_words) == len(right_words) == 120

    codimensions: Counter[int] = Counter()
    state_types: Counter[tuple[int, int]] = Counter()
    feasible_strata = 0
    minimum_pairs = 0

    for left_word in left_words:
        left_masks = colour_masks(left_word, LEFT_VERTICES)
        assert sum(2 - mask.bit_count() for mask in left_masks.values()) == 7
        for right_word in right_words:
            right_masks = colour_masks(right_word, RIGHT_VERTICES)
            assert sum(2 - mask.bit_count() for mask in right_masks.values()) == 7

            pair_minimum_contribution = 0
            for (sync_count, sync_cost), multiplicity in exact_stratum_states(
                left_masks, right_masks
            ).items():
                common_edge_rank = 12 - comb(sync_count, 2)
                total_equation_rank = 8 + common_edge_rank
                coefficient_fibre = 112 - total_equation_rank
                root_stratum = 14 - sync_cost
                incidence_dimension = root_stratum + coefficient_fibre
                codimension = 112 - incidence_dimension

                assert codimension == 6 - comb(sync_count, 2) + sync_cost
                assert codimension >= 5

                feasible_strata += multiplicity
                codimensions[codimension] += multiplicity
                state_types[(sync_count, sync_cost)] += multiplicity
                if codimension == 5:
                    pair_minimum_contribution += multiplicity

            if pair_minimum_contribution:
                assert pair_minimum_contribution == 1
                assert left_word == right_word
                assert set(left_word) <= set(COMMON)
                minimum_pairs += 1

    assert feasible_strata == 213_648
    assert codimensions == Counter(
        {9: 96_480, 8: 87_576, 6: 15_444, 7: 14_088, 5: 60}
    )
    assert minimum_pairs == 60

    return {
        "selector_pairs": len(left_words) * len(right_words),
        "feasible_exact_strata": feasible_strata,
        "state_type_count": len(state_types),
        "codimension_histogram": dict(sorted(codimensions.items())),
        "minimum_codimension": min(codimensions),
        "minimum_selector_pairs": minimum_pairs,
    }


def audit_global_arithmetic() -> dict[str, int]:
    """Audit affine closure, zero-block, pullback, and adjacent-pair counts."""
    projective_blocks = 14
    projective_dimension = projective_blocks * 8
    projective_envelope = projective_dimension - 5

    affine_dimension = projective_blocks * 9
    affine_torus_lift = projective_envelope + projective_blocks
    whole_zero_block = affine_dimension - 9
    affine_envelope = max(affine_torus_lift, whole_zero_block)

    all_blocks = comb(8, 2)
    full_dimension = all_blocks * 9
    pullback_dimension = affine_envelope + (all_blocks - projective_blocks) * 9

    five_sets = comb(8, 5)
    neighbours_per_five_set = 5 * 3
    adjacent_pairs = five_sets * neighbours_per_five_set // 2

    assert (projective_dimension, projective_envelope) == (112, 107)
    assert (affine_dimension, affine_torus_lift, whole_zero_block) == (
        126,
        121,
        117,
    )
    assert affine_dimension - affine_envelope == 5
    assert (full_dimension, pullback_dimension) == (252, 247)
    assert full_dimension - pullback_dimension == 5
    assert (five_sets, adjacent_pairs) == (56, 420)

    return {
        "projective_dimensions": (projective_dimension, projective_envelope),
        "affine_dimensions": (
            affine_dimension,
            affine_torus_lift,
            whole_zero_block,
        ),
        "full_graph_dimensions": (full_dimension, pullback_dimension),
        "five_sets": five_sets,
        "adjacent_pairs": adjacent_pairs,
    }


def main() -> None:
    strata = audit_selector_strata()
    arithmetic = audit_global_arithmetic()
    print("eight-vertex adjacent five-set overlap independent audit: PASS")
    print(f"  dynamic selector strata: {strata}")
    print(f"  global dimension arithmetic: {arithmetic}")


if __name__ == "__main__":
    main()
