"""Enumerate every 5-regular full-2-factor/singleton support on K8.

Eight full blocks form an arbitrary spanning 2-factor.  The complementary
cubic graph is one-factorized, with one diagonal singleton perfect matching
per colour.  This strictly contains the earlier double-C4 family and
includes full factors of types C8 and C5+C3.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from enumerate_double_c4_singleton_family import (
    activity_summary,
    canonical_pattern,
    selected_entries,
    sha256,
    skeleton_automorphisms,
    write_model,
)
from enumerate_five_regular_double_c4_singleton_family import (
    five_regular_skeletons,
)
from search_witness import EquationSystem
from verify_double_c4_singleton_family import component_sizes

Edge = tuple[int, int]
Pattern = tuple[int, ...]


def spanning_two_factors(
    skeleton: frozenset[Edge],
    n: int,
) -> dict[tuple[int, ...], list[frozenset[Edge]]]:
    output: dict[tuple[int, ...], list[frozenset[Edge]]] = {}
    for raw_edges in itertools.combinations(sorted(skeleton), n):
        factor = frozenset(raw_edges)
        degrees = Counter(vertex for edge in factor for vertex in edge)
        if any(degrees[vertex] != 2 for vertex in range(n)):
            continue
        factor_type = tuple(component_sizes(factor, n))
        output.setdefault(factor_type, []).append(factor)
    return output


def enumerate_patterns(
    system: EquationSystem,
    skeleton: frozenset[Edge],
    factors: list[frozenset[Edge]],
) -> set[Pattern]:
    edges = sorted(skeleton)
    matchings = [
        frozenset(tuple(map(int, edge)) for edge in matching)
        for matching in system.matchings
    ]
    patterns: set[Pattern] = set()
    for full_edges in factors:
        complement = skeleton - full_edges
        supported = [
            matching for matching in matchings
            if matching <= complement
        ]
        partitions = {
            tuple(
                sorted(
                    tuple(sorted(matching))
                    for matching in triple
                )
            )
            for triple in itertools.combinations(supported, 3)
            if frozenset().union(*triple) == complement
        }
        for partition in partitions:
            labels = {edge: 3 for edge in full_edges}
            for colour, matching in enumerate(partition):
                for edge in matching:
                    labels[edge] = colour
            patterns.add(tuple(labels[edge] for edge in edges))
    return patterns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-c4-c4-manifest",
        type=Path,
        required=True,
    )
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    reference = json.loads(
        args.reference_c4_c4_manifest.read_text(encoding="utf-8")
    )
    reference_edges = frozenset(
        tuple(map(int, edge)) for edge in reference["skeleton_edges"]
    )
    system = EquationSystem(8, 3)
    args.output_directory.mkdir(parents=True, exist_ok=True)

    type_rows: list[dict[str, object]] = []
    global_orbit_index = 0
    for skeleton_name, skeleton in five_regular_skeletons(reference_edges):
        edges = sorted(skeleton)
        automorphisms = skeleton_automorphisms(system.n, skeleton)
        factor_groups = spanning_two_factors(skeleton, system.n)
        factor_type_rows: list[dict[str, object]] = []
        for factor_type, factors in sorted(factor_groups.items()):
            patterns = enumerate_patterns(system, skeleton, factors)
            orbit_members: dict[Pattern, list[Pattern]] = {}
            for pattern in sorted(patterns):
                representative = canonical_pattern(
                    pattern,
                    edges,
                    automorphisms,
                )
                orbit_members.setdefault(representative, []).append(
                    pattern
                )

            orbit_rows: list[dict[str, object]] = []
            binomial_free_unlabelled = 0
            for local_index, (canonical, members) in enumerate(
                sorted(orbit_members.items())
            ):
                selected = selected_entries(system, edges, canonical)
                forbidden_histogram, required_counts = activity_summary(
                    system,
                    selected,
                )
                binomial_free = (
                    "1" not in forbidden_histogram
                    and "2" not in forbidden_histogram
                )
                if binomial_free:
                    binomial_free_unlabelled += len(members)
                factor_label = "_".join(map(str, factor_type))
                model = args.output_directory / (
                    f"{skeleton_name}_factor_{factor_label}_"
                    f"orbit_{local_index:02d}.log"
                )
                write_model(model, selected, system.variable_count)
                orbit_rows.append(
                    {
                        "global_orbit_index": global_orbit_index,
                        "local_orbit_index": local_index,
                        "orbit_size_colour_unlabelled": len(members),
                        "full_factor_cycle_type": list(factor_type),
                        "binomial_free": binomial_free,
                        "canonical_edge_labels": list(canonical),
                        "selected_entries": len(selected),
                        "selected_flat_indices": sorted(selected),
                        "forbidden_activity_histogram": (
                            forbidden_histogram
                        ),
                        "required_activity_counts": required_counts,
                        "model": str(model),
                        "model_sha256": sha256(model),
                    }
                )
                global_orbit_index += 1

            factor_type_rows.append(
                {
                    "full_factor_cycle_type": list(factor_type),
                    "spanning_two_factors": len(factors),
                    "colour_unlabelled_factorizations": len(patterns),
                    "labelled_supports": 6 * len(patterns),
                    "binomial_free_colour_unlabelled": (
                        binomial_free_unlabelled
                    ),
                    "binomial_free_labelled_supports": (
                        6 * binomial_free_unlabelled
                    ),
                    "support_orbits": len(orbit_rows),
                    "orbits": orbit_rows,
                }
            )

        type_rows.append(
            {
                "skeleton_type": skeleton_name,
                "skeleton_edges": [list(edge) for edge in edges],
                "skeleton_automorphisms": len(automorphisms),
                "factor_types": factor_type_rows,
            }
        )

    all_factor_rows = [
        factor_row
        for type_row in type_rows
        for factor_row in type_row["factor_types"]
    ]
    payload = {
        "verified": True,
        "scope": (
            "complete full-spanning-2-factor plus three-matching "
            "singleton family on all 5-regular eight-vertex skeletons"
        ),
        "claim_scope": (
            "exhausts this macro-family only; does not show that every "
            "exact-20 support has this form"
        ),
        "reference_c4_c4_manifest": str(
            args.reference_c4_c4_manifest
        ),
        "reference_c4_c4_manifest_sha256": sha256(
            args.reference_c4_c4_manifest
        ),
        "skeleton_types": len(type_rows),
        "spanning_two_factors": sum(
            int(row["spanning_two_factors"])
            for row in all_factor_rows
        ),
        "colour_unlabelled_factorizations": sum(
            int(row["colour_unlabelled_factorizations"])
            for row in all_factor_rows
        ),
        "labelled_supports": sum(
            int(row["labelled_supports"]) for row in all_factor_rows
        ),
        "binomial_free_colour_unlabelled": sum(
            int(row["binomial_free_colour_unlabelled"])
            for row in all_factor_rows
        ),
        "binomial_free_labelled_supports": sum(
            int(row["binomial_free_labelled_supports"])
            for row in all_factor_rows
        ),
        "support_orbits": sum(
            int(row["support_orbits"]) for row in all_factor_rows
        ),
        "types": type_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "skeleton_types",
                    "spanning_two_factors",
                    "colour_unlabelled_factorizations",
                    "labelled_supports",
                    "binomial_free_colour_unlabelled",
                    "binomial_free_labelled_supports",
                    "support_orbits",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
