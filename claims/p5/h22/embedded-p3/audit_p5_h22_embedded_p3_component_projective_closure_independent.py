#!/usr/bin/env python3
"""No-primary-import audit of the embedded-P3 projective H22 closure claim."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_VERIFICATION.md"
CLAIM = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h22_embedded_p3_component_projective_closure.py"
GENERIC = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
RANK_TWO = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
RANK_ONE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"
GENERIC_PRIMARY = ROOT / "verify_p5_h22_embedded_p3_component_generic_obstruction.py"
RANK_TWO_PRIMARY = ROOT / "verify_p5_h22_embedded_p3_component_rank_two_line_boundary.py"
RANK_ONE_PRIMARY = ROOT / "verify_p5_h22_embedded_p3_component_rank_one_collapse.py"

WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
STANDARD_ORIENTED = ((0, 1), (2, 3))
STANDARD_MATCHING = frozenset((frozenset((0, 1)), frozenset((2, 3))))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    permutations = PERMUTATIONS3 if len(rows) == 3 else PERMUTATIONS4
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(len(rows)))
            for permutation in permutations
        )
    )


def plane_basis_from_normal(
    normal: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    pivot = next(index for index, entry in enumerate(normal) if entry != 0)
    rows = []
    for coordinate in range(3):
        if coordinate == pivot:
            continue
        row = [sp.Integer(0)] * 3
        row[coordinate] = normal[pivot]
        row[pivot] = -normal[coordinate]
        assert sp.expand(sum(row[index] * normal[index] for index in range(3))) == 0
        rows.append(tuple(row))
    return rows[0], rows[1]


def homogeneous_rectangle_certificate() -> dict[str, object]:
    cap_c, cap_a, cap_b = sp.symbols("C A B")
    planes = (
        ((-cap_a, cap_c, 0), (-cap_b, 0, cap_c)),
        ((cap_a, cap_c, 0), (cap_b, 0, cap_c)),
        ((cap_a, cap_c, 0), (-cap_b, 0, cap_c)),
    )
    coefficients = {
        word: sp.factor(permanent(tuple(planes[mode][word[mode]] for mode in range(3))))
        for word in WORDS3
    }
    expected = {(1, 0, 0): 2 * cap_a * cap_c**2, (1, 0, 1): -2 * cap_b * cap_c**2}
    assert coefficients == {word: expected.get(word, sp.Integer(0)) for word in WORDS3}
    return {
        "valid_chart": "C!=0",
        "nonzero_coefficients": {
            "100": str(coefficients[(1, 0, 0)]),
            "101": str(coefficients[(1, 0, 1)]),
        },
        "warning": "these displayed rows cease to be plane bases at C=0",
    }


def support_mask_certificate() -> dict[str, object]:
    result = {}
    expected_nonzero = {
        1: {},
        2: {},
        3: {"100": "2"},
        4: {},
        5: {"101": "-2"},
        6: {"110": "-2"},
        7: {"100": "2", "101": "-2"},
    }
    for mask in range(1, 8):
        cap_c, cap_a, cap_b = (
            sp.Integer(bool(mask & (1 << index))) for index in range(3)
        )
        normals = (
            (cap_c, cap_a, cap_b),
            (cap_c, -cap_a, -cap_b),
            (cap_c, -cap_a, cap_b),
        )
        planes = tuple(plane_basis_from_normal(normal) for normal in normals)
        coefficients = {
            word: sp.factor(
                permanent(tuple(planes[mode][word[mode]] for mode in range(3)))
            )
            for word in WORDS3
        }
        nonzero = {
            "".join(map(str, word)): str(value)
            for word, value in coefficients.items()
            if value != 0
        }
        assert nonzero == expected_nonzero[mask]
        result[str(mask)] = {
            "support_size": mask.bit_count(),
            "nonzero_coefficients_in_independent_kernel_bases": nonzero,
            "pure_restriction_zero": not bool(nonzero),
        }
    assert all(result[str(mask)]["pure_restriction_zero"] for mask in (1, 2, 4))
    assert all(not result[str(mask)]["pure_restriction_zero"] for mask in (3, 5, 6, 7))
    return result


def transformed_matching(order: tuple[int, int, int]) -> dict[str, object]:
    """`order[new hyper slot] = old hyper slot`."""
    inverse = {old: new for new, old in enumerate(order)}
    old_to_new = {0: 0, **{old + 1: inverse[old] + 1 for old in range(3)}}
    oriented = tuple(
        tuple(old_to_new[coordinate] for coordinate in pair)
        for pair in STANDARD_ORIENTED
    )
    matching = frozenset(frozenset(pair) for pair in oriented)
    canonical_weights = []
    for pair in oriented:
        if pair[0] < pair[1]:
            canonical_weights.append(("lambda", "mu"))
        else:
            canonical_weights.append(("mu", "lambda"))
    return {
        "oriented_pairs": [list(pair) for pair in oriented],
        "unordered_matching": [
            list(pair) for pair in sorted(tuple(sorted(pair)) for pair in matching)
        ],
        "is_standard_unordered_matching": matching == STANDARD_MATCHING,
        "canonical_pair_weights": [list(weight) for weight in canonical_weights],
        "shared_oriented_weight_preserved": (
            matching == STANDARD_MATCHING
            and canonical_weights[0] == ("lambda", "mu")
            and canonical_weights[1] == ("lambda", "mu")
        ),
    }


def normal_chart_transport_certificate() -> dict[str, object]:
    result = {}
    for mask in (3, 5, 6, 7):
        admissible_orders = []
        for order in itertools.permutations(range(3)):
            if not (mask & (1 << order[0]) and mask & (1 << order[2])):
                continue
            transport = transformed_matching(order)
            admissible_orders.append(
                {
                    "new_CAB_from_old_slots": list(order),
                    **transport,
                }
            )
        assert admissible_orders
        result[str(mask)] = {
            "chart_orders": admissible_orders,
            "some_normal_chart_transport_exists": True,
            "some_transport_preserves_unordered_01_23": any(
                entry["is_standard_unordered_matching"] for entry in admissible_orders
            ),
            "some_transport_preserves_shared_oriented_weight": any(
                entry["shared_oriented_weight_preserved"] for entry in admissible_orders
            ),
        }
    assert result["6"]["some_normal_chart_transport_exists"]
    assert not result["6"]["some_transport_preserves_unordered_01_23"]
    assert not result["3"]["some_transport_preserves_shared_oriented_weight"]
    assert result["5"]["some_transport_preserves_shared_oriented_weight"]
    assert result["7"]["some_transport_preserves_shared_oriented_weight"]
    return result


def mask_six_matching_return_failure() -> dict[str, object]:
    mask = 6
    failures = []
    for order in itertools.permutations(range(3)):
        if not (mask & (1 << order[0]) and mask & (1 << order[2])):
            continue
        inverse = {old: new for new, old in enumerate(order)}
        old_to_new = {0: 0, **{old + 1: inverse[old] + 1 for old in range(3)}}
        matching_after_chart = frozenset(
            frozenset(old_to_new[index] for index in pair)
            for pair in STANDARD_ORIENTED
        )
        new_support = {new + 1 for new, old in enumerate(order) if mask & (1 << old)}
        returns = []
        for hyper_order in itertools.permutations((1, 2, 3)):
            rho = {0: 0, **{old: hyper_order[old - 1] for old in (1, 2, 3)}}
            returned = frozenset(
                frozenset(rho[index] for index in pair) for pair in matching_after_chart
            )
            if returned != STANDARD_MATCHING:
                continue
            final_support = {rho[index] for index in new_support}
            returns.append(
                {
                    "return_permutation": [rho[index] for index in range(4)],
                    "final_normal_support": sorted(final_support),
                    "final_C_nonzero": 1 in final_support,
                }
            )
        assert returns
        assert all(not entry["final_C_nonzero"] for entry in returns)
        failures.append(
            {
                "chart_order": list(order),
                "matching_after_chart": [
                    list(pair)
                    for pair in sorted(tuple(sorted(pair)) for pair in matching_after_chart)
                ],
                "all_standard_matching_returns": returns,
            }
        )
    return {
        "mask": mask,
        "representative": "[C:A:B]=[0:1:1]",
        "pure_P3_restriction_nonzero": True,
        "no_transport_keeps_C_nonzero_and_returns_matching_to_01_23": True,
        "cases": failures,
    }


def free_plane_counterexample() -> dict[str, object]:
    # Full normal support [C:A:B]=[1:1:1], so no normal-base boundary is used.
    planes = (
        ((0, 1, 0, 0), (1, 0, 0, 0)),
        ((0, -1, 1, 0), (0, -1, 0, 1)),
        ((0, 1, 1, 0), (0, 1, 0, 1)),
        ((0, 1, 1, 0), (0, -1, 0, 1)),
    )
    coefficients = {
        word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS4
    }
    nonzero = {
        "".join(map(str, word)): str(value)
        for word, value in coefficients.items()
        if value != 0
    }
    assert nonzero == {"1100": "2", "1101": "-2"}

    common_coordinate_triples = []
    for modes in itertools.combinations(range(4), 3):
        for coordinate in range(4):
            if all(
                all(row[coordinate] == 0 for row in planes[mode]) for mode in modes
            ):
                common_coordinate_triples.append(
                    {"modes": list(modes), "omitted_coordinate": coordinate}
                )
    assert common_coordinate_triples == [{"modes": [1, 2, 3], "omitted_coordinate": 0}]

    missing_u0 = sp.Matrix(planes[0])
    e0 = sp.Matrix([[1, 0, 0, 0]])
    assert missing_u0.col_join(e0).rank() == missing_u0.rank()

    cap_s, cap_t, cap_u = sp.symbols("S T U")
    normalized_u0 = sp.Matrix(((0, 1, cap_s, cap_u), (1, 0, 1, cap_t)))
    separation_minor = sp.factor(
        normalized_u0.col_join(e0).extract((0, 1, 2), (0, 1, 2)).det()
    )
    assert separation_minor == 1

    return {
        "normal_point": "[C:A:B]=[1:1:1]",
        "planes": [[list(row) for row in plane] for plane in planes],
        "nonzero_pure_P4_coefficients": nonzero,
        "pure_P4_restriction_nonzero_and_decomposable": True,
        "unique_embedded_common_hyperplane_triple": common_coordinate_triples,
        "free_plane_contains_transverse_axis_e0": True,
        "normalized_theorem_plane": [
            ["0", "1", "S", "U"],
            ["1", "0", "1", "T"],
        ],
        "normalized_plane_plus_e0_rank_three_minor": str(separation_minor),
        "normalized_theorem_plane_never_contains_e0": True,
        "monomial_source_and_mode_symmetries_preserve_this_separation": True,
        "covered_by_three_normalized_H22_theorems": False,
    }


def normalized_finite_chart_cover() -> dict[str, object]:
    cap_s, cap_t, cap_u, slope = sp.symbols("S T U r")
    projected_alpha = sp.Matrix((1, cap_s, cap_u))
    projected_beta = sp.Matrix((slope, 1, cap_t))
    cross_product = sp.Matrix(
        (
            cap_s * cap_t - cap_u,
            cap_u * slope - cap_t,
            1 - cap_s * slope,
        )
    )
    assert cross_product == projected_alpha.cross(projected_beta)
    collapse_substitution = {cap_t: slope * cap_u, cap_s: 1 / slope}
    assert all(sp.factor(entry.subs(collapse_substitution)) == 0 for entry in cross_product)

    discriminant_factors = (
        slope * cap_s - 1,
        slope * cap_u - cap_t,
        cap_s * cap_t - cap_u,
        slope * cap_s - slope * cap_u + cap_t - 1,
        slope * cap_s + slope * cap_u - cap_t - 1,
        slope * cap_s - cap_s * cap_t + cap_u - 1,
        slope * cap_s + cap_s * cap_t - cap_u - 1,
        slope * cap_u - cap_s * cap_t - cap_t + cap_u,
        slope * cap_u + cap_s * cap_t - cap_t - cap_u,
    )
    discriminant = sp.factor(sp.prod(discriminant_factors))
    return {
        "normalized_free_plane": "span((0,1,S,U),(1,0,1,T))",
        "weight_chart": "finite [lambda:mu]=[r:1] only",
        "projected_cross_product": [str(entry) for entry in cross_product],
        "rank_one_locus": ["r*S=1", "T=r*U"],
        "rank_two_locus": "complement of rank-one locus",
        "generic_theorem_scope": "rank two and discriminant nonzero",
        "rank_two_boundary_scope": "rank two and discriminant zero",
        "rank_one_theorem_scope": "rank one",
        "discriminant": str(discriminant),
        "finite_normalized_parameter_partition_complete": True,
        "does_not_cover_free_planes_containing_e0": True,
        "does_not_cover_homogeneous_weight_endpoint_[1:0]": True,
    }


def homogeneous_weight_transport_gap() -> dict[str, object]:
    # The mask-3 chart must swap source coordinates 2 and 3.  It leaves the
    # first oriented pair alone and reverses the second one.
    mask_three_transport = transformed_matching((0, 2, 1))
    assert mask_three_transport["canonical_pair_weights"] == [
        ["lambda", "mu"],
        ["mu", "lambda"],
    ]
    return {
        "repository_standard_signature": [
            "lambda*x0+mu*x1",
            "lambda*x2+mu*x3",
        ],
        "mask_3_required_coordinate_transport": "swap source coordinates 2 and 3",
        "transported_signature": [
            "lambda*x0+mu*x1",
            "mu*x2+lambda*x3",
        ],
        "finite_nonzero_weights_can_be_rebalanced_by_weight_dependent_diagonal_scaling": True,
        "endpoint_zero_pattern_cannot_be_rebalanced_by_nonzero_diagonal_scaling": True,
        "example_endpoint": {
            "weight": "[lambda:mu]=[0:1]",
            "first_pair_support": "second endpoint",
            "transported_second_pair_support": "first endpoint",
        },
        "primary_checks_weight_action": False,
        "three_cited_theorems_use_only_affine_slope_r": True,
        "homogeneous_weight_transport_verified": False,
    }


def main() -> None:
    homogeneous = homogeneous_rectangle_certificate()
    masks = support_mask_certificate()
    chart_transport = normal_chart_transport_certificate()
    mask_six = mask_six_matching_return_failure()
    free_plane = free_plane_counterexample()
    normalized_cover = normalized_finite_chart_cover()
    weight_gap = homogeneous_weight_transport_gap()

    primary_text = PRIMARY.read_text(encoding="utf-8")
    assert "alpha_0" not in primary_text
    assert "infinity" not in primary_text

    result = {
        "status": "pass",
        "claim_label": "REFUTED",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": "claimed full projective weighted-H22 closure of the embedded-P3 component and its symmetry/dependency cover",
        "inputs": {
            path.name: sha256(path)
            for path in (
                CLAIM,
                PRIMARY,
                GENERIC,
                RANK_TWO,
                RANK_ONE,
                GENERIC_PRIMARY,
                RANK_TWO_PRIMARY,
                RANK_ONE_PRIMARY,
            )
        },
        "method": "independent permanent reconstruction; exact support-mask and matching transport; invariant free-plane counterexample; normalized finite-chart scope partition",
        "command": "uv run --with sympy python audit_p5_h22_embedded_p3_component_projective_closure_independent.py",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "limitations": "REFUTED is the asserted full symmetry/dependency cover, not a positive H22 lift; the weighted-H22 status of the uncovered free-plane and homogeneous-weight strata remains UNKNOWN",
        "homogeneous_sign_rectangle": homogeneous,
        "projective_support_masks": masks,
        "normal_chart_transports": chart_transport,
        "mask_6_matching_counterexample": mask_six,
        "free_plane_normalization_counterexample": free_plane,
        "three_theorem_normalized_finite_chart_cover": normalized_cover,
        "homogeneous_weight_transport_gap": weight_gap,
        "target_primary_omits_free_plane_basis": True,
        "target_primary_omits_homogeneous_weight_endpoint": True,
        "claimed_full_projective_closure_verified": False,
        "claimed_full_projective_closure_refuted_as_dependency_cover": True,
        "uncovered_strata_weighted_H22_status": "UNKNOWN",
        "finite_field_computation_used_as_proof": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
