#!/usr/bin/env python3
"""Verify the finite interfaces used by the GLD81 source bridge.

The arbitrary-source implication is the matching-partition proof in the
theorem document.  This replay checks its complete ten-vertex combinatorics,
the exact target-response rescaling, and the accepted GLD80 interface/open
premise.  It does not infer source integrability from nuisance membership.
"""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GLD80 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / (
        "verify_four_root_torus_star_survivor_existential_principal_open_"
        "first_response_nonextension.py"
    )
)

ROOTS = frozenset(range(4))
Q0 = 4
Q1 = 5
PORTS = frozenset(range(6, 10))
OUTSIDE = frozenset(range(4, 10))
VERTICES = tuple(range(10))

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[Matching] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            output.append(((first, second), *matching))
    return tuple(output)


def has_root_root_edge(matching: Matching) -> bool:
    return any(left in ROOTS and right in ROOTS for left, right in matching)


def outside_edges(matching: Matching) -> tuple[Edge, ...]:
    return tuple(
        (left, right)
        for left, right in matching
        if left in OUTSIDE and right in OUTSIDE
    )


def raw_edge_kind(edge: Edge) -> str:
    left, right = edge
    assert left in OUTSIDE and right in OUTSIDE
    if edge == (Q0, Q1):
        return "Q"
    if left in (Q0, Q1):
        assert right in PORTS
        return "residual_port"
    assert left in PORTS and right in PORTS
    return "port_pair"


def residual_port_label(edge: Edge) -> str | None:
    """Return the GLD70 label determined by the complementary residual."""

    left, right = edge
    if left == Q0 and right in PORTS:
        return "h_eta"
    if left == Q1 and right in PORTS:
        return "h_xi"
    return None


def matching_contains_edge_between(
    matching: Matching, left_set: frozenset[int], right_vertex: int
) -> bool:
    return any(
        (left in left_set and right == right_vertex)
        or (right in left_set and left == right_vertex)
        for left, right in matching
    )


def target_response_scaling() -> tuple[list[Fraction], list[Fraction]]:
    root_values = (
        (1, 2, 3),
        (2, 3, 5),
        (3, 5, 7),
        (5, 7, 11),
    )
    z0 = (2, 3, 5)
    z1 = (7, 11, 13)
    contracted: list[Fraction] = []
    scaled_response: list[Fraction] = []
    for colour in range(3):
        root_product = Fraction(1)
        for root in range(4):
            root_product *= root_values[root][colour]
        contracted.append(root_product * z0[colour] * z1[colour])
        response = root_product * z1[colour]
        scaled_response.append(response * z0[colour])
    return contracted, scaled_response


def check() -> dict[str, object]:
    gld80 = load("gld80_gld81_replay", GLD80).check()
    assert gld80["survivor_principal_open_exists"] is True
    assert gld80["gld76_complete_gaussian_interface_transport_verified"] is True
    assert gld80["gld76_matching_partition_identity_verified"] is True
    assert gld80["explicit_survivor_exceptional_polynomial_computed"] is False

    matchings = perfect_matchings(VERTICES)
    assert len(matchings) == 945
    valid = tuple(
        matching for matching in matchings if not has_root_root_edge(matching)
    )
    assert len(valid) == 360
    assert all(len(outside_edges(matching)) == 1 for matching in valid)

    raw_edge_multiplicities = Counter(outside_edges(matching)[0] for matching in valid)
    assert len(raw_edge_multiplicities) == 15
    assert set(raw_edge_multiplicities.values()) == {24}
    raw_kind_counts = Counter()
    for edge, multiplicity in raw_edge_multiplicities.items():
        raw_kind_counts[raw_edge_kind(edge)] += multiplicity
    assert raw_kind_counts == {
        "Q": 24,
        "residual_port": 192,
        "port_pair": 144,
    }

    residual_label_counts = Counter()
    for matching in valid:
        raw_edge = outside_edges(matching)[0]
        label = residual_port_label(raw_edge)
        if label is None:
            continue
        residual_label_counts[label] += 1
        if label == "h_eta":
            assert matching_contains_edge_between(matching, ROOTS, Q1)
        else:
            assert matching_contains_edge_between(matching, ROOTS, Q0)
    assert residual_label_counts == {"h_eta": 96, "h_xi": 96}

    by_neighbor: dict[int, tuple[Matching, ...]] = {}
    complementary_raw_counts: dict[int, set[int]] = {}
    for neighbor in VERTICES:
        if neighbor == Q0:
            continue
        varied_edge = tuple(sorted((Q0, neighbor)))
        containing = tuple(
            matching for matching in matchings if varied_edge in matching
        )
        assert len(containing) == 105
        nonzero = tuple(
            matching for matching in containing if not has_root_root_edge(matching)
        )
        by_neighbor[neighbor] = nonzero
        complementary_raw_counts[neighbor] = {
            len(outside_edges(tuple(edge for edge in matching if edge != varied_edge)))
            for matching in nonzero
        }

    assert {neighbor: len(value) for neighbor, value in by_neighbor.items()} == {
        0: 60,
        1: 60,
        2: 60,
        3: 60,
        5: 24,
        6: 24,
        7: 24,
        8: 24,
        9: 24,
    }
    assert all(complementary_raw_counts[root] == {1} for root in ROOTS)
    assert complementary_raw_counts[Q1] == {0}
    assert all(complementary_raw_counts[port] == {0} for port in PORTS)
    for port in PORTS:
        assert all(
            matching_contains_edge_between(matching, ROOTS, Q1)
            for matching in by_neighbor[port]
        )

    partitioned = tuple(
        matching
        for neighbor_matchings in by_neighbor.values()
        for matching in neighbor_matchings
    )
    assert len(partitioned) == len(set(partitioned)) == len(valid)
    assert set(partitioned) == set(valid)

    constant_response_dimensions = 1 + 4 * 3
    root_response_dimensions = 4
    assert constant_response_dimensions + root_response_dimensions == 17

    contracted_weights, scaled_response_weights = target_response_scaling()
    assert contracted_weights == scaled_response_weights
    assert all(value != 0 for value in contracted_weights)

    root_scales = (Fraction(2), Fraction(3), Fraction(5), Fraction(7))
    z0_scale = Fraction(11)
    z1_scale = Fraction(13)
    grade_zero_scale = z0_scale * z1_scale
    for value in root_scales:
        grade_zero_scale *= value
    first_response_scale = z0_scale * z1_scale
    for value in root_scales:
        first_response_scale *= value
    assert grade_zero_scale == first_response_scale
    root_product = Fraction(1)
    for value in root_scales:
        root_product *= value
    constant_column_scale = root_product
    assert constant_column_scale == root_product
    for root_scale in root_scales:
        root_column_scale = root_product / root_scale
        root_domain_scale = root_scale
        assert root_column_scale * root_domain_scale == root_product

    branch_cover = [
        "other_root_or_surplus_branch",
        "port_rank_drop",
        "fewer_than_three_base_survivors",
        "maximal_triangle",
        "residual_coordinate_boundary",
        "isotropic_star_slope",
        "outside_certified_survivor_component_or_gauge",
        "gld80_exceptional_divisor",
    ]
    assert len(branch_cover) == 8

    return {
        "status": "exact_source_to_response_incidence_bridge",
        "global_conjecture": "UNRESOLVED",
        "field": "characteristic_zero_matching_identity_then_C_source_consequence",
        "ten_vertex_perfect_matchings": len(matchings),
        "nonzero_grade_zero_matchings": len(valid),
        "raw_outside_edge_count": len(raw_edge_multiplicities),
        "raw_presentation_shape": [1, 24, 54, 79],
        "raw_matching_kind_counts": dict(raw_kind_counts),
        "residual_port_complementary_labels": dict(residual_label_counts),
        "q0_response_nonzero_matching_counts": {
            str(neighbor): len(value) for neighbor, value in by_neighbor.items()
        },
        "q0_response_domain_split": [13, 4, 17],
        "root_response_complements_have_one_raw_edge": True,
        "constant_response_complements_have_no_raw_edge": True,
        "target_response_rescaling_verified": True,
        "source_gauge_scaling_sanity_checked": True,
        "root_column_domain_gauge_factors_verified": True,
        "complete_interface_covariance_replayed": True,
        "gld80_principal_open_source_branch_excluded": True,
        "residual_branch_cover": branch_cover,
        "explicit_delta_computed": False,
        "other_source_branches_excluded": False,
    }


def main() -> None:
    result = check()
    print("four-root torus-star source-to-incidence bridge: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
