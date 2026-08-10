"""Verify the double-C4/singleton family on all 5-regular K8 skeletons.

This is the aggregate, producer-independent audit for the three possible
unlabelled skeleton types.  It regenerates the macro supports, their
symmetry orbits and activity data, then requires a semantic
factor-lattice/DRAT audit for every orbit representative.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.search_witness import EquationSystem
from verify_double_c4_singleton_family import (
    activity_summary,
    canonical,
    check_factor_audit,
    checked_path,
    double_c4_factors,
    one_factorizations,
    parse_model,
    selected_entries,
    sha256,
    skeleton_automorphisms,
)

Edge = tuple[int, int]
Pattern = tuple[int, ...]


def complement_component_sizes(
    skeleton: frozenset[Edge],
    n: int,
) -> list[int]:
    complete = frozenset(itertools.combinations(range(n), 2))
    complement = complete - skeleton
    adjacency = [set() for _ in range(n)]
    for first, second in complement:
        adjacency[first].add(second)
        adjacency[second].add(first)
    if any(len(adjacency[vertex]) != 2 for vertex in range(n)):
        raise AssertionError("complement is not 2-regular")
    unseen = set(range(n))
    sizes: list[int] = []
    while unseen:
        root = min(unseen)
        stack = [root]
        unseen.remove(root)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def reconstruct_type(
    system: EquationSystem,
    type_row: dict[str, object],
) -> tuple[dict[str, int], list[tuple[Pattern, list[Pattern]]]]:
    type_name = str(type_row["skeleton_type"])
    expected_components = {
        "c8": [8],
        "c5_c3": [5, 3],
        "c4_c4": [4, 4],
    }
    skeleton = frozenset(
        tuple(map(int, edge)) for edge in type_row["skeleton_edges"]
    )
    if len(skeleton) != 20:
        raise AssertionError(f"{type_name}: skeleton does not have 20 edges")
    degrees = Counter(vertex for edge in skeleton for vertex in edge)
    if any(degrees[vertex] != 5 for vertex in range(system.n)):
        raise AssertionError(f"{type_name}: skeleton is not 5-regular")
    if complement_component_sizes(skeleton, system.n) != (
        expected_components[type_name]
    ):
        raise AssertionError(f"{type_name}: complement type mismatch")

    edges = sorted(skeleton)
    factors = double_c4_factors(skeleton, system.n)
    patterns: set[Pattern] = set()
    for factor in factors:
        complement = skeleton - factor
        for factorization in one_factorizations(
            complement,
            system.n,
        ):
            labels = {edge: 3 for edge in factor}
            for colour, matching in enumerate(factorization):
                for edge in matching:
                    labels[edge] = colour
            patterns.add(tuple(labels[edge] for edge in edges))

    automorphisms = skeleton_automorphisms(skeleton, system.n)
    orbits: dict[Pattern, list[Pattern]] = defaultdict(list)
    for pattern in patterns:
        orbits[canonical(pattern, edges, automorphisms)].append(pattern)
    reconstructed = sorted(orbits.items())
    counts = {
        "double_c4_factors": len(factors),
        "skeleton_automorphisms": len(automorphisms),
        "colour_unlabelled_factorizations": len(patterns),
        "labelled_supports": 6 * len(patterns),
        "support_orbits": len(reconstructed),
    }
    for key, expected in counts.items():
        if type_row.get(key) != expected:
            raise AssertionError(
                f"{type_name}: {key} mismatch "
                f"{type_row.get(key)} != {expected}"
            )

    producer_rows = type_row["orbits"]
    if len(producer_rows) != len(reconstructed):
        raise AssertionError(f"{type_name}: orbit-row count mismatch")
    for local_index, ((pattern, members), row) in enumerate(
        zip(reconstructed, producer_rows, strict=True)
    ):
        if row["local_orbit_index"] != local_index:
            raise AssertionError(f"{type_name}: local orbit order mismatch")
        if tuple(row["canonical_edge_labels"]) != pattern:
            raise AssertionError(f"{type_name}: canonical pattern mismatch")
        if row["orbit_size_colour_unlabelled"] != len(members):
            raise AssertionError(f"{type_name}: orbit size mismatch")
        selected = selected_entries(pattern, edges)
        if len(selected) != 84:
            raise AssertionError(f"{type_name}: support is not 84-entry")
        if row["selected_flat_indices"] != sorted(selected):
            raise AssertionError(f"{type_name}: selected support mismatch")
        model = checked_path(str(row["model"]), str(row["model_sha256"]))
        if parse_model(model, system.variable_count) != selected:
            raise AssertionError(f"{type_name}: model assignment mismatch")
        forbidden, required = activity_summary(system, selected)
        if forbidden != row["forbidden_activity_histogram"]:
            raise AssertionError(f"{type_name}: activity histogram mismatch")
        if required != row["required_activity_counts"]:
            raise AssertionError(f"{type_name}: required activity mismatch")
        if "1" in forbidden or "2" in forbidden:
            raise AssertionError(f"{type_name}: support is not binomial-free")
    return counts, reconstructed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family-manifest",
        type=Path,
        default=Path(
            "tmp/eight_vertex_five_regular_double_c4_singleton_family.json"
        ),
    )
    parser.add_argument(
        "--factor-audit",
        action="append",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/"
            "eight_vertex_five_regular_double_c4_singleton_family_verified.json"
        ),
    )
    args = parser.parse_args()
    if args.factor_audit is None:
        args.factor_audit = [
            *(
                Path(
                    "tmp/"
                    "eight_vertex_five_regular_double_c4_singleton_"
                    f"factor_c8_{index:02d}_verified.json"
                )
                for index in range(12)
            ),
            Path(
                "tmp/"
                "eight_vertex_five_regular_double_c4_singleton_"
                "factor_c5_c3_00_verified.json"
            ),
            *(
                Path(
                    "tmp/eight_vertex_double_c4_singleton_"
                    f"factor_{index:02d}_verified.json"
                )
                for index in range(10)
            ),
        ]

    family = json.loads(
        args.family_manifest.read_text(encoding="utf-8")
    )
    if family.get("verified") is not True:
        raise AssertionError("family producer did not mark output verified")
    checked_path(
        str(family["reference_c4_c4_manifest"]),
        str(family["reference_c4_c4_manifest_sha256"]),
    )
    if family.get("skeleton_types") != 3:
        raise AssertionError("producer does not contain three skeleton types")
    type_names = [row["skeleton_type"] for row in family["types"]]
    if type_names != ["c8", "c5_c3", "c4_c4"]:
        raise AssertionError(f"unexpected skeleton type order: {type_names}")

    # Every simple 2-regular graph on eight vertices is a disjoint union of
    # cycles of length at least three.  The only partitions of eight into
    # such parts are 8, 5+3 and 4+4, so these rows exhaust all unlabelled
    # 5-regular eight-vertex skeletons.
    partitions = [
        parts
        for length in range(1, 4)
        for parts in itertools.combinations_with_replacement(
            range(3, 9),
            length,
        )
        if sum(parts) == 8
    ]
    if sorted(partitions) != [(3, 5), (4, 4), (8,)]:
        raise AssertionError("2-regular complement classification changed")

    system = EquationSystem(8, 3)
    aggregate_counts: Counter[str] = Counter()
    all_rows: list[dict[str, object]] = []
    expected_global_index = 0
    for type_row in family["types"]:
        counts, _reconstructed = reconstruct_type(system, type_row)
        aggregate_counts.update(counts)
        for row in type_row["orbits"]:
            if row["global_orbit_index"] != expected_global_index:
                raise AssertionError("global orbit indices are not consecutive")
            expected_global_index += 1
            all_rows.append(row)

    expected_aggregate = {
        "double_c4_factors": 72,
        "colour_unlabelled_factorizations": 181,
        "labelled_supports": 1086,
        "support_orbits": 23,
    }
    for key, expected in expected_aggregate.items():
        if aggregate_counts[key] != expected:
            raise AssertionError(
                f"reconstructed aggregate {key}: "
                f"{aggregate_counts[key]} != {expected}"
            )
        if family.get(key) != expected:
            raise AssertionError(
                f"producer aggregate {key}: {family.get(key)} != {expected}"
            )

    audit_by_model_hash: dict[str, Path] = {}
    for audit_path in args.factor_audit:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        model_hash = str(audit["source_model_sha256"])
        if model_hash in audit_by_model_hash:
            raise AssertionError(f"duplicate audit for model {model_hash}")
        audit_by_model_hash[model_hash] = audit_path
    expected_hashes = {str(row["model_sha256"]) for row in all_rows}
    if set(audit_by_model_hash) != expected_hashes:
        missing = expected_hashes - set(audit_by_model_hash)
        extra = set(audit_by_model_hash) - expected_hashes
        raise AssertionError(f"audit coverage mismatch: {missing=}, {extra=}")

    audit_rows = [
        check_factor_audit(
            audit_by_model_hash[str(row["model_sha256"])],
            row,
        )
        for row in all_rows
    ]
    payload = {
        "verified": True,
        "scope": (
            "all 1086 labelled double-C4/full-block plus "
            "three-matching singleton supports on every 5-regular "
            "eight-vertex skeleton"
        ),
        "claim_scope": (
            "proves this finite macro-family impossible only; does not "
            "show that every exact-20 support has this form and is not "
            "the global Krenn-Gu conjecture"
        ),
        "family_manifest": str(args.family_manifest),
        "family_manifest_sha256": sha256(args.family_manifest),
        "skeleton_types": 3,
        **expected_aggregate,
        "selected_entries_per_support": 84,
        "binomial_free_labelled_supports": 1086,
        "certified_impossible_labelled_supports": 1086,
        "orbit_audits": audit_rows,
        "total_factor_relations": sum(
            int(row["factor_relations"]) for row in audit_rows
        ),
        "total_factor_clauses": sum(
            int(row["factor_clauses"]) for row in audit_rows
        ),
        "total_lattice_branches": sum(
            int(row["lattice_branches"]) for row in audit_rows
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
