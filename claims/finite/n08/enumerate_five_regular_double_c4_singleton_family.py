"""Enumerate the double-C4/singleton family on every 5-regular K8 graph.

The complement of a 5-regular graph on eight vertices is 2-regular, so up
to isomorphism it is one of C8, C5+C3, or C4+C4.  For each type this script
enumerates every spanning C4+C4 full-block factor and every
one-factorization of its cubic complement.  It quotients the resulting
supports by skeleton automorphisms and global colour permutations and emits
one complete entry assignment per orbit for the factor-lattice certifier.
"""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import itertools
import json
from pathlib import Path

from enumerate_double_c4_singleton_family import (
    activity_summary,
    canonical_pattern,
    double_c4_factors,
    selected_entries,
    sha256,
    skeleton_automorphisms,
    write_model,
)
from krenn_gu.search_witness import EquationSystem

Edge = tuple[int, int]
Pattern = tuple[int, ...]


def cycle_edges(vertices: tuple[int, ...]) -> frozenset[Edge]:
    return frozenset(
        tuple(
            sorted(
                (
                    vertices[index],
                    vertices[(index + 1) % len(vertices)],
                )
            )
        )
        for index in range(len(vertices))
    )


def five_regular_skeletons(
    reference_c4_c4_edges: frozenset[Edge],
) -> list[tuple[str, frozenset[Edge]]]:
    complete = frozenset(itertools.combinations(range(8), 2))
    missing_by_type = {
        "c8": cycle_edges(tuple(range(8))),
        "c5_c3": (
            cycle_edges((0, 1, 2, 3, 4))
            | cycle_edges((5, 6, 7))
        ),
    }
    return [
        ("c8", complete - missing_by_type["c8"]),
        ("c5_c3", complete - missing_by_type["c5_c3"]),
        ("c4_c4", reference_c4_c4_edges),
    ]


def enumerate_patterns(
    system: EquationSystem,
    skeleton: frozenset[Edge],
) -> tuple[list[frozenset[Edge]], set[Pattern]]:
    matchings = [
        frozenset(tuple(map(int, edge)) for edge in matching)
        for matching in system.matchings
    ]
    edges = sorted(skeleton)
    factors = double_c4_factors(skeleton)
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
    return factors, patterns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-c4-c4-manifest",
        type=Path,
        required=True,
        help=(
            "verified family producer whose fixed C4+C4-complement "
            "skeleton is reused so its existing orbit audits remain bound"
        ),
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
    for type_name, skeleton in five_regular_skeletons(reference_edges):
        degrees = {
            vertex: sum(vertex in edge for edge in skeleton)
            for vertex in range(8)
        }
        if set(degrees.values()) != {5}:
            raise AssertionError(f"{type_name} skeleton is not 5-regular")
        edges = sorted(skeleton)
        factors, patterns = enumerate_patterns(system, skeleton)
        automorphisms = skeleton_automorphisms(system.n, skeleton)
        orbits: dict[Pattern, list[Pattern]] = {}
        for pattern in sorted(patterns):
            representative = canonical_pattern(
                pattern,
                edges,
                automorphisms,
            )
            orbits.setdefault(representative, []).append(pattern)

        orbit_rows: list[dict[str, object]] = []
        for local_index, (canonical, members) in enumerate(
            sorted(orbits.items())
        ):
            selected = selected_entries(system, edges, canonical)
            forbidden_histogram, required_counts = activity_summary(
                system,
                selected,
            )
            if "1" in forbidden_histogram or "2" in forbidden_histogram:
                raise AssertionError(
                    f"{type_name} orbit {local_index} is not binomial-free"
                )
            model = args.output_directory / (
                f"{type_name}_orbit_{local_index:02d}.log"
            )
            write_model(model, selected, system.variable_count)
            orbit_rows.append(
                {
                    "global_orbit_index": global_orbit_index,
                    "local_orbit_index": local_index,
                    "orbit_size_colour_unlabelled": len(members),
                    "canonical_edge_labels": list(canonical),
                    "selected_entries": len(selected),
                    "selected_flat_indices": sorted(selected),
                    "forbidden_activity_histogram": forbidden_histogram,
                    "required_activity_counts": required_counts,
                    "model": str(model),
                    "model_sha256": sha256(model),
                }
            )
            global_orbit_index += 1

        type_rows.append(
            {
                "skeleton_type": type_name,
                "skeleton_edges": [list(edge) for edge in edges],
                "double_c4_factors": len(factors),
                "skeleton_automorphisms": len(automorphisms),
                "colour_unlabelled_factorizations": len(patterns),
                "labelled_supports": 6 * len(patterns),
                "support_orbits": len(orbit_rows),
                "orbits": orbit_rows,
            }
        )

    payload = {
        "verified": True,
        "scope": (
            "complete double-C4 full-block plus three-matching singleton "
            "family on all 5-regular eight-vertex skeletons"
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
        "double_c4_factors": sum(
            int(row["double_c4_factors"]) for row in type_rows
        ),
        "colour_unlabelled_factorizations": sum(
            int(row["colour_unlabelled_factorizations"])
            for row in type_rows
        ),
        "labelled_supports": sum(
            int(row["labelled_supports"]) for row in type_rows
        ),
        "support_orbits": sum(
            int(row["support_orbits"]) for row in type_rows
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
                    "double_c4_factors",
                    "colour_unlabelled_factorizations",
                    "labelled_supports",
                    "support_orbits",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
