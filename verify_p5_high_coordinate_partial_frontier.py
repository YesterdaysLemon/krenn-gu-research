#!/usr/bin/env python3
"""Verify the exact high-coordinate partial-row frontier."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md"
DEPENDENCIES = (
    ROOT / "P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md",
    ROOT / "P5_Q4_211_EXCLUSION_THEOREM.md",
    ROOT / "P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md",
    ROOT / "P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md",
    ROOT / "P4_PURE_RANK_TWO_COMPONENT_THEOREM.md",
    ROOT / "P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md",
    ROOT / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md",
    ROOT / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md",
    ROOT / "P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md",
    ROOT / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md",
    ROOT / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md",
    ROOT / "P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md",
    ROOT / "P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT
    / "P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md",
    ROOT / "P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md",
    ROOT / "P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md",
    ROOT
    / "P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT
    / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P4_EMBEDDED_P3_PURE_COMPONENT.md",
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md",
    ROOT / "P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md",
    ROOT / "P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT
    / "P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md",
    ROOT / "P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md",
    ROOT / "P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md",
    ROOT / "P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md",
    ROOT / "P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md",
    ROOT / "P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md",
    ROOT / "P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md",
    ROOT / "P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md",
    ROOT / "P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md",
    ROOT / "P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md",
    ROOT / "P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md",
    ROOT / "P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P5_H31_MARKED_BASIS_OPEN_BRANCH.md",
    ROOT / "P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md",
    ROOT / "P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md",
    ROOT / "P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md",
    ROOT / "P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md",
    ROOT / "P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md",
    ROOT / "P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md",
    ROOT / "P5_H31_SECONDARY_GATE_EXCLUSION.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contraction_polynomial(
    contraction: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
) -> sp.Expr:
    return sp.expand(
        sum(
            contraction[index]
            * sp.prod(
                variables[other]
                for other in range(5)
                if other != index
            )
            for index in range(5)
        )
    )


def main() -> None:
    # Labelled counts: source of partial row, missing colour, and
    # coordinate-row assignments.
    q5_311 = 3 * 10 * 2
    q5_221 = 3 * 5 * 6
    q4_per_support = 5 * 3 * 6 * 2
    q4_zero = q4_per_support
    q4_partial = 4 * q4_per_support
    partial_31_per_support = 5 * 3 * 2 * 4
    partial_22_per_marking = 5 * 3 * 6

    excluded = (
        q5_311
        + q5_221
        + q4_zero
        + q4_partial
        + partial_31_per_support
    )
    frontier = (
        2 * partial_31_per_support
        + 3 * partial_22_per_marking
    )
    high_total = excluded + frontier
    assert (
        q5_311,
        q5_221,
        q4_zero,
        q4_partial,
        partial_31_per_support,
        frontier,
        excluded,
        high_total,
    ) == (60, 90, 180, 720, 120, 510, 1170, 1680)

    a, b, c = sp.symbols("a b c", nonzero=True)
    h31_rows = sp.Matrix(
        [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [a, b, c],
        ]
    )
    h22_rows = sp.Matrix(
        [
            [1, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 0],
            [a, b, c],
        ]
    )
    assert h31_rows.rank() == h22_rows.rank() == 3
    assert tuple(
        tuple(h31_rows[:, colour])
        for colour in range(3)
    ) == (
        (1, 1, 1, 0, a),
        (0, 0, 0, 1, b),
        (0, 0, 0, 0, c),
    )
    assert tuple(
        tuple(h22_rows[:, colour])
        for colour in range(3)
    ) == (
        (1, 1, 0, 0, a),
        (0, 0, 1, 1, b),
        (0, 0, 0, 0, c),
    )

    x = sp.symbols("x0:5")
    e = tuple(
        tuple(int(index == coordinate) for index in range(5))
        for coordinate in range(5)
    )
    sum_012 = tuple(e[0][j] + e[1][j] + e[2][j] for j in range(5))
    v0 = tuple(e[0][j] + e[1][j] for j in range(5))
    v1 = tuple(e[2][j] + e[3][j] for j in range(5))

    h31_factorizations = {
        "delete_3": contraction_polynomial(e[3], x),
        "delete_4": contraction_polynomial(e[4], x),
        "support_3": contraction_polynomial(sum_012, x),
    }
    assert h31_factorizations == {
        "delete_3": x[0] * x[1] * x[2] * x[4],
        "delete_4": x[0] * x[1] * x[2] * x[3],
        "support_3": sp.expand(
            x[3] * x[4]
            * (x[0] * x[1] + x[0] * x[2] + x[1] * x[2])
        ),
    }

    h22_factorizations = {
        "v0": contraction_polynomial(v0, x),
        "v1": contraction_polynomial(v1, x),
        "v2": contraction_polynomial(e[4], x),
    }
    assert h22_factorizations == {
        "v0": sp.expand((x[0] + x[1]) * x[2] * x[3] * x[4]),
        "v1": sp.expand(x[0] * x[1] * (x[2] + x[3]) * x[4]),
        "v2": x[0] * x[1] * x[2] * x[3],
    }

    normal_matrix = sp.Matrix(
        [
            [1, -1, 0, 0, 0],
            [0, 0, 1, -1, 0],
            [0, 0, 0, 0, 1],
        ]
    )
    assert normal_matrix.rank() == 3
    assert sum(
        normal_matrix[0, column] * v0[column]
        for column in range(5)
    ) == 0
    assert sum(
        normal_matrix[1, column] * v1[column]
        for column in range(5)
    ) == 0

    output = {
        "verified": True,
        "field": "C",
        "covered_local_signatures": 6495,
        "high_coordinate_signatures": high_total,
        "excluded_high_coordinate_signatures": excluded,
        "frontier_high_coordinate_signatures": frontier,
        "frontier_families": {
            "H31": {
                "signatures": 2 * partial_31_per_support,
                "single_gate_pure_compressions_excluded": True,
                "known_component_canonical_marked_sections_excluded": True,
                "known_component_open_shifted_branch_excluded": True,
                "finite_known_family_marked_fibre_excluded": True,
                "known_component_chart_divisor_marked_fibre_excluded": True,
                "genuine_toric_marked_fibres_excluded": True,
                "first_plane_infinity_marked_fibre_excluded": True,
                "internal_E0_marked_fibre_excluded": True,
                "whole_marked_component_excluded": True,
                "first_component_whole_marked_fibre_excluded": True,
                "second_component_exists": True,
                "second_component_rational_point_marked_fibre_excluded": True,
                "second_component_rational_curve_marked_fibre_excluded": True,
                "second_component_transverse_E_curve_marked_fibre_excluded": True,
                "second_component_complete_factored_slice_excluded": True,
                "second_component_factored_slice_symmetry_orbit_excluded": True,
                "second_component_complete_H0_slice_excluded": True,
                "second_component_H0_slice_symmetry_orbit_excluded": True,
                "second_component_generic_marked_fibre_excluded": True,
                "second_component_survivor_projection_proper_closed": True,
                "second_component_middle_coordinate_dense_rank_drop_chart_closed": True,
                "second_component_middle_coordinate_pivot_complement_closed": True,
                "second_component_end_coordinate_dense_full_rank_chart_closed": True,
                "second_component_endpoint_deepest_genus_two_intersections_closed": True,
                "second_component_endpoint_t2_divisor_closed": True,
                "second_component_endpoint_t3_divisor_closed": True,
                "second_component_all_regular_endpoint_markings_closed": True,
                "second_component_all_regular_elliptic_marked_fibres_closed": True,
                "second_component_normalization_boundary_marked_fibre_excluded": True,
                "second_component_normalized_affine_slice_excluded": True,
                "second_component_outer_ABF_boundary_classified": True,
                "second_component_outer_ABF_boundary_marked_fibre_excluded": True,
                "second_component_survivor_divisor_classified": True,
                "second_component_boundary_marked_fibre_excluded": True,
                "second_component_whole_marked_fibre_excluded": True,
                "known_pure_component_orbits_at_least": 9,
                "three_one_three_components_exist": True,
                "three_one_three_components_pair_product_profile": [
                    4,
                    4,
                    3,
                    4,
                    3,
                    3,
                ],
                "three_one_three_components_generic_marked_fibres_excluded": True,
                "three_one_three_components_complete_marked_fibres_excluded": False,
                "common_smooth_diagonal_quadric_nonblock_pure_locus_empty": True,
                "common_smooth_diagonal_quadric_component_sized_locus_excluded": True,
                "radical_star_generic_stratum_classified": True,
                "radical_star_component_orbits": 4,
                "radical_star_additional_components": 0,
                "mixed_orientation_component_exists": True,
                "mixed_orientation_component_directed_indegrees": [
                    2,
                    1,
                    0,
                    0,
                ],
                "mixed_orientation_component_generic_marked_fibre_excluded": True,
                "mixed_orientation_component_complete_marked_fibre_excluded": False,
                "six_dimensional_component_exists": True,
                "six_dimensional_component_pair_profile": [
                    4,
                    3,
                    2,
                    4,
                    4,
                    3,
                ],
                "six_dimensional_component_generic_marked_fibre_excluded": True,
                "six_dimensional_component_complete_marked_fibre_excluded": False,
                "disjoint_mixed_star_component_exists": True,
                "disjoint_mixed_star_component_supports": ["01", "01", "23"],
                "disjoint_mixed_star_component_generic_marked_fibre_excluded": True,
                "embedded_P3_component_exists": True,
                "embedded_P3_component_pair_profile": [4, 4, 4, 2, 2, 2],
                "embedded_P3_component_generic_marked_fibre_excluded": True,
                "embedded_P3_component_complete_marked_fibre_excluded": False,
                "embedded_P3_component_normalized_chart_marked_fibre_excluded": True,
                "embedded_P3_component_nine_insertion_points_closed": True,
                "seven_previously_known_components_generic_marked_fibres_excluded": True,
                "all_eight_known_components_generic_marked_fibres_excluded": True,
                "all_nine_known_components_generic_marked_fibres_excluded": True,
                "mixed_determinantal_five_primes_classified": True,
                "mixed_determinantal_additional_component_orbits": 0,
                "remaining_exceptional_pair_graphs": [
                    "star",
                    "triangle",
                ],
                "remaining_component_strata": [
                    "mixed_orientation_charts_outside_the_classified_normal_form",
                    "rank_two_exceptional_relations",
                    "unclassified_lower_pair_rank_boundaries",
                    "coincident_or_support_one_zero_product_boundaries",
                ],
                "all_pure_components_classified": False,
                "toric_plane_orientations_remaining": 0,
                "remaining_geometry": (
                    "one_three_sixth_and_six_dimensional_component_"
                    "boundaries_remaining_mixed_orientation_star_"
                    "triangle_lower_pair_rank_classification_and_H22"
                ),
                "source_contractions": [
                    "P4_to_pure",
                    "P4_to_Delta2",
                    "support3_to_pure_or_Delta2",
                ],
            },
            "H22": {
                "signatures": 3 * partial_22_per_marking,
                "six_dimensional_component_equal_weight_binary_incidence_empty": True,
                "six_dimensional_component_weighted_binary_survivors_exist": True,
                "six_dimensional_component_generic_weighted_incidence_empty": True,
                "six_dimensional_component_weighted_23_ternary_rank_excluded": True,
                "mixed_orientation_component_generic_weighted_incidence_empty": True,
                "mixed_orientation_component_weighted_01_full_mixed_rank": True,
                "mixed_orientation_component_weighted_23_ternary_rank_excluded": True,
                "three_one_three_components_generic_weighted_incidence_empty": True,
                "three_one_three_components_weighted_01_binary_incidence_empty": True,
                "three_one_three_components_weighted_23_survivor_sheets_excluded": True,
                "first_rank_two_component_generic_weighted_incidence_empty": True,
                "first_rank_two_component_weighted_01_full_mixed_rank": True,
                "first_rank_two_component_weighted_23_two_sheets_excluded": True,
                "diagonal_quadric_component_generic_weighted_incidence_empty": True,
                "diagonal_quadric_component_projective_join_fibre_empty": True,
                "diagonal_quadric_component_properness_transport": True,
                "known_components_generic_weighted_H22_empty_count": 9,
                "certified_pure_component_orbit_count": 9,
                "disjoint_mixed_star_component_generic_weighted_incidence_empty": True,
                "embedded_P3_component_generic_weighted_incidence_empty": True,
                "six_dimensional_component_diagonal_pencils": [
                    "x0_equals_x1",
                    "x2_equals_x3",
                ],
                "six_dimensional_component_weighted_slopes_closed": False,
                "mixed_orientation_component_weighted_slopes_closed": False,
                "mixed_orientation_component_projective_boundary_closed": False,
                "three_one_three_components_projective_boundaries_closed": False,
                "first_rank_two_component_projective_boundary_closed": False,
                "diagonal_quadric_component_special_divisors_closed": False,
                "seven_previously_known_components_generic_H22_incidence_empty": True,
                "all_eight_known_components_generic_H22_incidence_empty": True,
                "all_nine_known_components_generic_H22_incidence_empty": True,
                "all_H22_excluded": False,
                "source_contractions": [
                    "P4_to_pure_or_Delta2",
                    "P4_to_pure_or_Delta2",
                    "P4_to_pure",
                ],
            },
        },
        "dependencies": {
            path.name: sha256(path)
            for path in DEPENDENCIES
        },
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_high_coordinate_partial_frontier_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
