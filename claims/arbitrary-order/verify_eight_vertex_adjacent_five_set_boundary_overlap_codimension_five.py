"""Primary exact audit for adjacent five-set boundary overlap at eight vertices."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from math import comb

import sympy as sp

COMMON = tuple(range(4))
LEFT_VERTICES = COMMON + (4,)
RIGHT_VERTICES = COMMON + (5,)
COLOURS = tuple(range(3))

Selector = tuple[int, int, int]


def nonconstant_selectors(vertices: tuple[int, ...]) -> tuple[Selector, ...]:
    """Return the nonempty three-colour coordinate-boundary selectors."""
    return tuple(
        selector
        for selector in product(vertices, repeat=3)
        if len(set(selector)) > 1
    )


def zero_colours(selector: Selector, vertex: int) -> frozenset[int]:
    """Return the target coordinates forced to vanish at one root."""
    return frozenset(
        colour for colour, selected in enumerate(selector) if selected == vertex
    )


def coordinate_basis(zeros: frozenset[int]) -> sp.Matrix:
    """Return a basis matrix for the coordinate subspace with ``zeros`` killed."""
    identity = sp.eye(3)
    return sp.Matrix.hstack(
        *(identity[:, colour] for colour in COLOURS if colour not in zeros)
    )


def intersection_vector_dimension(left: sp.Matrix, right: sp.Matrix) -> int:
    """Compute an exact coordinate-subspace intersection dimension."""
    joined = sp.Matrix.hstack(left, right)
    return left.cols + right.cols - joined.rank()


def check_selector_geometry() -> dict[str, object]:
    """Enumerate every selector pair and exact common-root sync stratum."""
    left_selectors = nonconstant_selectors(LEFT_VERTICES)
    right_selectors = nonconstant_selectors(RIGHT_VERTICES)
    assert len(left_selectors) == len(right_selectors) == 120

    codimension_histogram: Counter[int] = Counter()
    sync_count_histogram: Counter[int] = Counter()
    equality_cases: list[tuple[Selector, Selector, int]] = []
    feasible_strata = 0

    common_edges = tuple(combinations(COMMON, 2))
    assert len(common_edges) == 6

    for left_selector in left_selectors:
        left_zeros = {
            vertex: zero_colours(left_selector, vertex)
            for vertex in LEFT_VERTICES
        }
        assert sum(2 - len(left_zeros[vertex]) for vertex in LEFT_VERTICES) == 7

        for right_selector in right_selectors:
            right_zeros = {
                vertex: zero_colours(right_selector, vertex)
                for vertex in RIGHT_VERTICES
            }
            assert sum(2 - len(right_zeros[vertex]) for vertex in RIGHT_VERTICES) == 7

            local_data: dict[int, tuple[int, int, bool]] = {}
            for vertex in COMMON:
                left_basis = coordinate_basis(left_zeros[vertex])
                right_basis = coordinate_basis(right_zeros[vertex])
                left_projective_dimension = left_basis.cols - 1
                right_projective_dimension = right_basis.cols - 1
                product_dimension = (
                    left_projective_dimension + right_projective_dimension
                )
                intersection_dimension = intersection_vector_dimension(
                    left_basis, right_basis
                )
                sync_dimension = intersection_dimension - 1
                sync_feasible = intersection_dimension > 0
                sync_cost = (
                    product_dimension - sync_dimension if sync_feasible else -1
                )
                if sync_feasible:
                    expected_cost = 2 - len(
                        left_zeros[vertex] & right_zeros[vertex]
                    )
                    assert sync_cost == expected_cost
                nonsync_feasible = (
                    not sync_feasible or sync_dimension < product_dimension
                )
                local_data[vertex] = (
                    sync_cost,
                    sync_dimension,
                    nonsync_feasible,
                )

            for sync_mask in range(1 << len(COMMON)):
                exact_sync = {
                    vertex
                    for vertex in COMMON
                    if sync_mask & (1 << vertex)
                }
                sync_cost = 0
                feasible = True
                common_assignments = 0
                for vertex in COMMON:
                    local_cost, sync_dimension, nonsync_feasible = local_data[vertex]
                    if vertex in exact_sync:
                        if sync_dimension < 0:
                            feasible = False
                            break
                        sync_cost += local_cost
                        common_assignments += len(
                            left_zeros[vertex] & right_zeros[vertex]
                        )
                    elif not nonsync_feasible:
                        feasible = False
                        break
                if not feasible:
                    continue

                feasible_strata += 1
                sync_count = len(exact_sync)
                assert sync_cost == 2 * sync_count - common_assignments

                common_constraint_rank = sum(
                    1 if left in exact_sync and right in exact_sync else 2
                    for left, right in common_edges
                )
                total_constraint_rank = 8 + common_constraint_rank
                assert total_constraint_rank == 20 - comb(sync_count, 2)

                root_stratum_dimension = 14 - sync_cost
                coefficient_fibre_dimension = 112 - total_constraint_rank
                incidence_dimension = (
                    root_stratum_dimension + coefficient_fibre_dimension
                )
                codimension = 112 - incidence_dimension
                formula_codimension = (
                    6
                    - comb(sync_count, 2)
                    + 2 * sync_count
                    - common_assignments
                )
                assert codimension == formula_codimension
                assert codimension >= 5

                codimension_histogram[codimension] += 1
                sync_count_histogram[sync_count] += 1
                if codimension == 5:
                    equality_cases.append(
                        (left_selector, right_selector, sync_mask)
                    )

    assert feasible_strata == 213_648
    assert codimension_histogram == Counter(
        {9: 96_480, 8: 87_576, 6: 15_444, 7: 14_088, 5: 60}
    )
    assert len(equality_cases) == 60
    for left_selector, right_selector, sync_mask in equality_cases:
        assert sync_mask == 0b1111
        assert left_selector == right_selector
        assert set(left_selector) <= set(COMMON)
        assert len(set(left_selector)) > 1

    return {
        "selectors_per_five_set": len(left_selectors),
        "selector_pairs": len(left_selectors) * len(right_selectors),
        "feasible_exact_sync_strata": feasible_strata,
        "codimension_histogram": dict(sorted(codimension_histogram.items())),
        "sync_count_histogram": dict(sorted(sync_count_histogram.items())),
        "minimum_codimension": min(codimension_histogram),
        "minimum_source_strata": len(equality_cases),
    }


def check_ambient_dimensions() -> dict[str, int]:
    """Check projective, affine, and full-graph dimension arithmetic."""
    projective_ambient = 14 * 8
    projective_incidence_maximum = projective_ambient - 5
    projectivization_fibre = 14

    affine_ambient = 14 * 9
    affine_nonzero_envelope = projective_incidence_maximum + projectivization_fibre
    affine_zero_block = affine_ambient - 9

    full_graph_ambient = 28 * 9
    omitted_block_dimension = full_graph_ambient - affine_ambient
    full_graph_pullback = affine_nonzero_envelope + omitted_block_dimension

    adjacent_pairs = comb(8, 5) * (5 * 3) // 2

    assert projective_ambient == 112
    assert projective_incidence_maximum == 107
    assert affine_ambient == 126
    assert affine_nonzero_envelope == 121
    assert affine_zero_block == 117
    assert affine_ambient - max(affine_nonzero_envelope, affine_zero_block) == 5
    assert full_graph_ambient == 252
    assert full_graph_pullback == 247
    assert full_graph_ambient - full_graph_pullback == 5
    assert adjacent_pairs == 420

    return {
        "projective_ambient": projective_ambient,
        "projective_incidence_at_most": projective_incidence_maximum,
        "affine_ambient": affine_ambient,
        "affine_nonzero_envelope_at_most": affine_nonzero_envelope,
        "affine_zero_block_dimension": affine_zero_block,
        "full_graph_ambient": full_graph_ambient,
        "full_graph_pullback_at_most": full_graph_pullback,
        "adjacent_five_set_pairs": adjacent_pairs,
    }


def main() -> None:
    selector_geometry = check_selector_geometry()
    ambient_dimensions = check_ambient_dimensions()
    print("eight-vertex adjacent five-set overlap primary audit: PASS")
    print(f"  selector geometry: {selector_geometry}")
    print(f"  ambient dimensions: {ambient_dimensions}")


if __name__ == "__main__":
    main()
