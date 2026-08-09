"""Verify the complete 5-regular full-2-factor/singleton family on K8."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

from search_witness import EquationSystem
from verify_double_c4_singleton_family import (
    activity_summary,
    canonical,
    check_factor_audit,
    checked_path,
    component_sizes,
    one_factorizations,
    parse_model,
    selected_entries,
    sha256,
    skeleton_automorphisms,
)
from verify_five_regular_double_c4_singleton_family import (
    complement_component_sizes,
)

Edge = tuple[int, int]
Pattern = tuple[int, ...]


def all_two_factors(
    skeleton: frozenset[Edge],
    n: int,
) -> dict[tuple[int, ...], list[frozenset[Edge]]]:
    output: dict[tuple[int, ...], list[frozenset[Edge]]] = defaultdict(list)
    for raw_edges in itertools.combinations(sorted(skeleton), n):
        factor = frozenset(raw_edges)
        degrees = Counter(vertex for edge in factor for vertex in edge)
        if all(degrees[vertex] == 2 for vertex in range(n)):
            output[tuple(component_sizes(factor, n))].append(factor)
    return dict(output)


def reconstruct_factor_type(
    system: EquationSystem,
    skeleton: frozenset[Edge],
    edges: list[Edge],
    automorphisms: list[tuple[int, ...]],
    factors: list[frozenset[Edge]],
    producer: dict[str, object],
) -> list[dict[str, object]]:
    patterns: set[Pattern] = set()
    for factor in factors:
        for factorization in one_factorizations(
            skeleton - factor,
            system.n,
        ):
            labels = {edge: 3 for edge in factor}
            for colour, matching in enumerate(factorization):
                for edge in matching:
                    labels[edge] = colour
            patterns.add(tuple(labels[edge] for edge in edges))

    orbits: dict[Pattern, list[Pattern]] = defaultdict(list)
    for pattern in patterns:
        orbits[canonical(pattern, edges, automorphisms)].append(pattern)
    reconstructed = sorted(orbits.items())
    counts = {
        "spanning_two_factors": len(factors),
        "colour_unlabelled_factorizations": len(patterns),
        "labelled_supports": 6 * len(patterns),
        "support_orbits": len(reconstructed),
    }
    for key, expected in counts.items():
        if producer.get(key) != expected:
            raise AssertionError(
                f"factor-type {producer['full_factor_cycle_type']}: "
                f"{key} mismatch {producer.get(key)} != {expected}"
            )

    producer_rows = producer["orbits"]
    if len(producer_rows) != len(reconstructed):
        raise AssertionError("factor-type orbit count mismatch")
    binomial_free_unlabelled = 0
    for local_index, ((pattern, members), row) in enumerate(
        zip(reconstructed, producer_rows, strict=True)
    ):
        if row["local_orbit_index"] != local_index:
            raise AssertionError("local orbit indices changed")
        if tuple(row["canonical_edge_labels"]) != pattern:
            raise AssertionError("canonical factor pattern changed")
        if row["orbit_size_colour_unlabelled"] != len(members):
            raise AssertionError("factor orbit size changed")
        selected = selected_entries(pattern, edges)
        if len(selected) != 84:
            raise AssertionError("factor support is not 84-entry")
        if row["selected_flat_indices"] != sorted(selected):
            raise AssertionError("factor selected support changed")
        model = checked_path(str(row["model"]), str(row["model_sha256"]))
        if parse_model(model, system.variable_count) != selected:
            raise AssertionError("factor model assignment changed")
        forbidden, required = activity_summary(system, selected)
        if forbidden != row["forbidden_activity_histogram"]:
            raise AssertionError("factor activity histogram changed")
        if required != row["required_activity_counts"]:
            raise AssertionError("factor required activity changed")
        binomial_free = "1" not in forbidden and "2" not in forbidden
        if row["binomial_free"] is not binomial_free:
            raise AssertionError("binomial-free classification changed")
        if binomial_free:
            binomial_free_unlabelled += len(members)

    if producer["binomial_free_colour_unlabelled"] != (
        binomial_free_unlabelled
    ):
        raise AssertionError("binomial-free factorization count changed")
    if producer["binomial_free_labelled_supports"] != (
        6 * binomial_free_unlabelled
    ):
        raise AssertionError("binomial-free labelled count changed")
    return producer_rows


def default_audits(family: dict[str, object]) -> list[Path]:
    output: list[Path] = []
    for type_row in family["types"]:
        skeleton_type = str(type_row["skeleton_type"])
        for factor_row in type_row["factor_types"]:
            cycle_type = "_".join(
                map(str, factor_row["full_factor_cycle_type"])
            )
            for orbit in factor_row["orbits"]:
                local_index = int(orbit["local_orbit_index"])
                if not bool(orbit["binomial_free"]):
                    output.append(
                        Path(
                            "tmp/"
                            "eight_vertex_five_regular_full_singleton_"
                            f"factor_{skeleton_type}_{cycle_type}_"
                            f"{local_index:02d}_verified.json"
                        )
                    )
                elif skeleton_type == "c4_c4":
                    output.append(
                        Path(
                            "tmp/eight_vertex_double_c4_singleton_"
                            f"factor_{local_index:02d}_verified.json"
                        )
                    )
                else:
                    output.append(
                        Path(
                            "tmp/"
                            "eight_vertex_five_regular_double_c4_singleton_"
                            f"factor_{skeleton_type}_{local_index:02d}_"
                            "verified.json"
                        )
                    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family-manifest",
        type=Path,
        default=Path(
            "tmp/eight_vertex_five_regular_full_singleton_family.json"
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
            "eight_vertex_five_regular_full_singleton_family_verified.json"
        ),
    )
    args = parser.parse_args()

    family = json.loads(
        args.family_manifest.read_text(encoding="utf-8")
    )
    if family.get("verified") is not True:
        raise AssertionError("family producer output is not verified")
    checked_path(
        str(family["reference_c4_c4_manifest"]),
        str(family["reference_c4_c4_manifest_sha256"]),
    )
    if args.factor_audit is None:
        args.factor_audit = default_audits(family)

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
        raise AssertionError("2-regular graph classification changed")

    system = EquationSystem(8, 3)
    expected_complements = {
        "c8": [8],
        "c5_c3": [5, 3],
        "c4_c4": [4, 4],
    }
    all_rows: list[dict[str, object]] = []
    aggregate: Counter[str] = Counter()
    expected_global_index = 0
    for type_row in family["types"]:
        type_name = str(type_row["skeleton_type"])
        skeleton = frozenset(
            tuple(map(int, edge)) for edge in type_row["skeleton_edges"]
        )
        if complement_component_sizes(skeleton, 8) != (
            expected_complements[type_name]
        ):
            raise AssertionError(f"{type_name}: complement type changed")
        edges = sorted(skeleton)
        automorphisms = skeleton_automorphisms(skeleton, 8)
        if type_row["skeleton_automorphisms"] != len(automorphisms):
            raise AssertionError(f"{type_name}: automorphism count changed")
        factor_groups = all_two_factors(skeleton, 8)
        producer_groups = {
            tuple(map(int, row["full_factor_cycle_type"])): row
            for row in type_row["factor_types"]
        }
        if set(factor_groups) != set(producer_groups):
            raise AssertionError(f"{type_name}: factor types changed")
        for factor_type in sorted(factor_groups):
            producer = producer_groups[factor_type]
            rows = reconstruct_factor_type(
                system,
                skeleton,
                edges,
                automorphisms,
                factor_groups[factor_type],
                producer,
            )
            for key in (
                "spanning_two_factors",
                "colour_unlabelled_factorizations",
                "labelled_supports",
                "binomial_free_colour_unlabelled",
                "binomial_free_labelled_supports",
                "support_orbits",
            ):
                aggregate[key] += int(producer[key])
            for row in rows:
                if row["global_orbit_index"] != expected_global_index:
                    raise AssertionError("global orbit order changed")
                expected_global_index += 1
                all_rows.append(row)

    expected_counts = {
        "spanning_two_factors": 753,
        "colour_unlabelled_factorizations": 1323,
        "labelled_supports": 7938,
        "binomial_free_colour_unlabelled": 181,
        "binomial_free_labelled_supports": 1086,
        "support_orbits": 86,
    }
    for key, expected in expected_counts.items():
        if aggregate[key] != expected or family.get(key) != expected:
            raise AssertionError(
                f"aggregate {key} changed: "
                f"{aggregate[key]}, {family.get(key)}, expected {expected}"
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
            "all 7938 labelled full-spanning-2-factor plus "
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
        **expected_counts,
        "binomial_bearing_labelled_supports": 6852,
        "certified_impossible_labelled_supports": 7938,
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
