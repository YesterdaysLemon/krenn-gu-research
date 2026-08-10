"""Census matching-theoretic motifs in dense rectangle certificates.

Each completed native-Kissat SAT log records one full support model.  This
script reconstructs *all* two-monomial rectangle certificates in each model,
then summarizes features that might admit an arbitrary-order proof:

* whether the shared perfect matchings differ on one alternating cycle;
* the length of that cycle;
* where the two changed vertices lie in the symmetric difference; and
* how the isolated matching meets the two shared matchings.

The output is exploratory.  A universal feature in a finite log census is
not promoted to a theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

from cancellation_transport import (
    _rectangle_certificates_on_decided_equations,
)
from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from eight_vertex_sparse_exact import positive_model_literals
from search_witness import EquationSystem


LOG_PATTERN = re.compile(r"role_(\d{4})_run_(\d{3})\.log")
Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def symmetric_difference_components(
    first: Matching,
    second: Matching,
) -> list[set[int]]:
    """Return nontrivial alternating-cycle vertex sets for two matchings."""
    difference = set(first) ^ set(second)
    adjacency: dict[int, set[int]] = {}
    for left, right in difference:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    components: list[set[int]] = []
    unseen = set(adjacency)
    while unseen:
        root = min(unseen)
        stack = [root]
        component: set[int] = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        components.append(component)
    return sorted(components, key=lambda component: (len(component), min(component)))


def matching_feature(
    system: EquationSystem,
    certificate: dict[str, object],
    selected_entries: set[int],
) -> dict[str, object]:
    shared_indices = list(map(int, certificate["matching_indices"]))
    first = system.matchings[shared_indices[0]]
    second = system.matchings[shared_indices[1]]
    components = symmetric_difference_components(first, second)
    changed = set(map(int, certificate["changed_vertices"]))
    component_hits = sorted(len(changed & component) for component in components)
    feature: dict[str, object] = {
        "certificate_mode": certificate["certificate_mode"],
        "shared_common_edges": len(set(first) & set(second)),
        "shared_cycle_lengths": sorted(map(len, components)),
        "changed_vertices_in_shared_difference": len(
            changed & set().union(*components)
        )
        if components
        else 0,
        "changed_vertices_on_same_shared_cycle": any(
            changed <= component for component in components
        ),
        "changed_vertices_per_shared_cycle": component_hits,
    }
    source_colouring = certificate.get(
        "source_colouring",
        certificate.get("target_colouring"),
    )
    if source_colouring is not None:
        colouring = list(map(int, source_colouring))
        multiplicities = Counter(colouring)
        feature["source_nonmajority_vertices"] = (
            len(colouring) - max(multiplicities.values())
        )
        feature["source_distinct_colours"] = len(multiplicities)
    isolated_index = certificate.get("isolated_matching_index")
    if isolated_index is not None:
        isolated = system.matchings[int(isolated_index)]
        changed_edge = tuple(sorted(changed))
        changed_left, changed_right = changed_edge
        block_offset = system.edge_index[changed_edge] * system.d * system.d
        block_support = {
            entry - block_offset
            for entry in selected_entries
            if block_offset
            <= entry
            < block_offset + system.d * system.d
        }
        source_row = int(source_colouring[changed_left])
        source_column = int(source_colouring[changed_right])
        source_local_entry = source_row * system.d + source_column
        isolated_singleton_colours: list[int] = []
        for edge in isolated:
            edge_offset = (
                system.edge_index[edge] * system.d * system.d
            )
            edge_support = {
                entry - edge_offset
                for entry in selected_entries
                if edge_offset
                <= entry
                < edge_offset + system.d * system.d
            }
            singleton_colour = next(
                (
                    colour
                    for colour in range(system.d)
                    if edge_support
                    == {colour * system.d + colour}
                ),
                None,
            )
            if singleton_colour is not None:
                isolated_singleton_colours.append(singleton_colour)
        first_components = symmetric_difference_components(first, isolated)
        second_components = symmetric_difference_components(second, isolated)
        isolated_four_cycles = [
            component
            for component_collection in (
                first_components,
                second_components,
            )
            for component in component_collection
            if len(component_collection) == 1 and len(component) == 4
        ]
        feature.update(
            {
                "isolated_common_edges_with_shared": sorted(
                    [
                        len(set(first) & set(isolated)),
                        len(set(second) & set(isolated)),
                    ]
                ),
                "isolated_cycle_lengths_with_shared": sorted(
                    [
                        sorted(map(len, first_components)),
                        sorted(map(len, second_components)),
                    ]
                ),
                "isolated_has_four_cycle_to_shared": any(
                    len(components_to_one) == 1
                    and len(components_to_one[0]) == 4
                    for components_to_one in (
                        first_components,
                        second_components,
                    )
                ),
                "isolated_four_cycle_to_shared_count": len(
                    isolated_four_cycles
                ),
                "isolated_contains_changed_edge": (
                    changed_edge in isolated
                ),
                "changed_edge_support_size": len(block_support),
                "changed_edge_source_entry_selected": (
                    source_local_entry in block_support
                ),
                "changed_edge_is_singleton": len(block_support) == 1,
                "changed_edge_is_monochromatic_singleton": (
                    block_support == {source_local_entry}
                    and source_row == source_column
                ),
                "changed_edge_source_colours_equal": (
                    source_row == source_column
                ),
                "isolated_singleton_edge_count": len(
                    isolated_singleton_colours
                ),
                "isolated_is_singleton_perfect_matching": (
                    len(isolated_singleton_colours) == system.n // 2
                ),
                "isolated_singleton_distinct_colours": len(
                    set(isolated_singleton_colours)
                ),
                "changed_vertices_in_isolated_four_cycle": max(
                    (
                        len(changed & component)
                        for component in isolated_four_cycles
                    ),
                    default=0,
                ),
                "changed_vertices_on_same_isolated_four_cycle": any(
                    changed <= component
                    for component in isolated_four_cycles
                ),
            }
        )
    return feature


def feature_key(feature: dict[str, object]) -> str:
    return json.dumps(feature, sort_keys=True, separators=(",", ":"))


def completed_logs(work_dir: Path) -> list[Path]:
    paths: list[tuple[int, int, Path]] = []
    for path in work_dir.glob("role_*_run_*.log"):
        match = LOG_PATTERN.fullmatch(path.name)
        if match is None:
            continue
        text = path.read_text(encoding="ascii")
        if "s SATISFIABLE" in text:
            paths.append(
                (int(match.group(1)), int(match.group(2)), path)
            )
    return [path for _role, _run, path in sorted(paths)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--work-dir",
        action="append",
        type=Path,
        required=True,
        help="native-Kissat work directory; may be repeated",
    )
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=1,
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    equation_indices = list(range(len(system.colourings)))
    rows: list[dict[str, object]] = []
    feature_counter: Counter[str] = Counter()
    for work_dir in args.work_dir:
        for log in completed_logs(work_dir):
            model = sorted(positive_model_literals(log))
            selected = local_positive_to_flat(
                system,
                model,
                args.center_degree,
            )
            selected_mask = np.zeros(system.variable_count, dtype=bool)
            selected_mask[list(selected)] = True
            active_matrix = np.all(
                selected_mask[system.variable_ids],
                axis=2,
            )
            activities = [
                set(
                    map(
                        int,
                        np.flatnonzero(
                            active_matrix[:, equation_index]
                        ),
                    )
                )
                for equation_index in equation_indices
            ]
            certificates = _rectangle_certificates_on_decided_equations(
                system,
                equation_indices,
                activities,
            )
            features = [
                matching_feature(system, certificate, selected)
                for certificate in certificates
            ]
            model_feature_counter = Counter(
                feature_key(feature) for feature in features
            )
            feature_counter.update(model_feature_counter)
            singleton_edges: dict[Edge, int] = {}
            for edge in system.edges:
                edge_offset = (
                    system.edge_index[edge] * system.d * system.d
                )
                edge_support = {
                    entry - edge_offset
                    for entry in selected
                    if edge_offset
                    <= entry
                    < edge_offset + system.d * system.d
                }
                for colour in range(system.d):
                    if edge_support == {
                        colour * system.d + colour
                    }:
                        singleton_edges[edge] = colour
                        break
            singleton_matchings = [
                matching
                for matching in system.matchings
                if all(edge in singleton_edges for edge in matching)
            ]
            mixed_singleton_matchings = [
                matching
                for matching in singleton_matchings
                if len(
                    {
                        singleton_edges[edge]
                        for edge in matching
                    }
                )
                > 1
            ]
            existence = {
                "has_rectangle": bool(features),
                "has_nonzero_target": any(
                    feature["certificate_mode"] == "nonzero_target"
                    for feature in features
                ),
                "has_isolated_forbidden": any(
                    feature["certificate_mode"] == "isolated_forbidden"
                    for feature in features
                ),
                "has_single_shared_cycle": any(
                    len(feature["shared_cycle_lengths"]) == 1
                    for feature in features
                ),
                "has_shared_four_cycle": any(
                    feature["shared_cycle_lengths"] == [4]
                    for feature in features
                ),
                "has_changed_vertices_on_same_shared_cycle": any(
                    feature["changed_vertices_on_same_shared_cycle"]
                    for feature in features
                ),
                "has_isolated_four_cycle_to_shared": any(
                    bool(
                        feature.get(
                            "isolated_has_four_cycle_to_shared",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_single_shared_cycle_and_isolated_four_cycle": any(
                    len(feature["shared_cycle_lengths"]) == 1
                    and bool(
                        feature.get(
                            "isolated_has_four_cycle_to_shared",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_shared_four_cycle_and_isolated_four_cycle": any(
                    feature["shared_cycle_lengths"] == [4]
                    and bool(
                        feature.get(
                            "isolated_has_four_cycle_to_shared",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_changed_vertices_on_isolated_four_cycle": any(
                    bool(
                        feature.get(
                            "changed_vertices_on_same_isolated_four_cycle",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_isolated_changed_edge_four_cycle": any(
                    bool(
                        feature.get(
                            "isolated_contains_changed_edge",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_vertices_on_same_isolated_four_cycle",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_singleton_changed_edge_exchange": any(
                    bool(
                        feature.get(
                            "isolated_contains_changed_edge",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_vertices_on_same_isolated_four_cycle",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_edge_is_singleton",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_monochromatic_singleton_changed_edge_exchange": any(
                    bool(
                        feature.get(
                            "isolated_contains_changed_edge",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_vertices_on_same_isolated_four_cycle",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_edge_is_monochromatic_singleton",
                            False,
                        )
                    )
                    for feature in features
                ),
                "has_full_singleton_exchange_motif": any(
                    feature["certificate_mode"] == "isolated_forbidden"
                    and bool(
                        feature.get(
                            "isolated_contains_changed_edge",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_vertices_on_same_isolated_four_cycle",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "changed_edge_is_monochromatic_singleton",
                            False,
                        )
                    )
                    and len(feature["shared_cycle_lengths"]) == 1
                    for feature in features
                ),
                "has_full_singleton_Q_exchange": any(
                    feature["certificate_mode"] == "isolated_forbidden"
                    and bool(
                        feature.get(
                            "changed_edge_is_monochromatic_singleton",
                            False,
                        )
                    )
                    and bool(
                        feature.get(
                            "isolated_is_singleton_perfect_matching",
                            False,
                        )
                    )
                    and int(
                        feature.get(
                            "isolated_singleton_distinct_colours",
                            0,
                        )
                    )
                    > 1
                    for feature in features
                ),
            }
            rows.append(
                {
                    "work_dir": str(work_dir),
                    "source_log": str(log),
                    "source_log_sha256": sha256(log),
                    "rectangle_certificates": len(certificates),
                    "monochromatic_singleton_edges": len(
                        singleton_edges
                    ),
                    "singleton_perfect_matchings": len(
                        singleton_matchings
                    ),
                    "mixed_singleton_perfect_matchings": len(
                        mixed_singleton_matchings
                    ),
                    "distinct_feature_types": len(
                        model_feature_counter
                    ),
                    "existence": existence,
                    "feature_histogram": [
                        {
                            "count": count,
                            "feature": json.loads(key),
                        }
                        for key, count in model_feature_counter.most_common()
                    ],
                }
            )

    universal_existence = {
        key: sum(bool(row["existence"][key]) for row in rows)
        for key in rows[0]["existence"]
    } if rows else {}
    payload = {
        "scope": (
            "exploratory census of all rectangle certificates in "
            "completed dense support logs"
        ),
        "support_models": len(rows),
        "total_rectangle_certificates": sum(
            int(row["rectangle_certificates"]) for row in rows
        ),
        "universal_existence_counts": universal_existence,
        "distinct_feature_types": len(feature_counter),
        "feature_histogram": [
            {
                "count": count,
                "feature": json.loads(key),
            }
            for key, count in feature_counter.most_common()
        ],
        "models": rows,
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "support_models",
                    "total_rectangle_certificates",
                    "universal_existence_counts",
                    "distinct_feature_types",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
