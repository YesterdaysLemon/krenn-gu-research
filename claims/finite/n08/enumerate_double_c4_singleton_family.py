"""Enumerate the double-C4/full-block plus singleton-factor family.

On the fixed 20-edge role-zero skeleton, the first binomial-free SAT
survivors have a common form:

* eight full blocks form a spanning 2-factor of two 4-cycles;
* the complementary cubic graph is partitioned into three perfect
  matchings;
* those matchings become diagonal singleton blocks of colours 0, 1, 2.

This script exhausts that finite macro-family and quotients it by every
skeleton automorphism and global colour permutation.  It emits one complete
DIMACS-style entry assignment per orbit for the exact factor-lattice
certifier.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np

from search_witness import EquationSystem

Edge = tuple[int, int]
Pattern = tuple[int, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def four_cycles(edges: frozenset[Edge]) -> list[frozenset[Edge]]:
    cycles: set[frozenset[Edge]] = set()
    vertices = sorted({vertex for edge in edges for vertex in edge})
    for subset in itertools.combinations(vertices, 4):
        first = subset[0]
        for tail in itertools.permutations(subset[1:]):
            order = (first, *tail)
            cycle = frozenset(
                tuple(
                    sorted(
                        (
                            order[position],
                            order[(position + 1) % 4],
                        )
                    )
                )
                for position in range(4)
            )
            if cycle <= edges:
                cycles.add(cycle)
    return sorted(cycles, key=lambda value: sorted(value))


def double_c4_factors(
    edges: frozenset[Edge],
) -> list[frozenset[Edge]]:
    factors: set[frozenset[Edge]] = set()
    for first, second in itertools.combinations(four_cycles(edges), 2):
        first_vertices = {vertex for edge in first for vertex in edge}
        second_vertices = {vertex for edge in second for vertex in edge}
        if first_vertices.isdisjoint(second_vertices):
            factors.add(first | second)
    return sorted(factors, key=lambda value: sorted(value))


def skeleton_automorphisms(
    n: int,
    edges: frozenset[Edge],
) -> list[tuple[int, ...]]:
    output: list[tuple[int, ...]] = []
    for permutation in itertools.permutations(range(n)):
        image = frozenset(
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in edges
        )
        if image == edges:
            output.append(tuple(map(int, permutation)))
    return output


def transform_pattern(
    pattern: Pattern,
    edges: list[Edge],
    edge_positions: dict[Edge, int],
    vertex_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> Pattern:
    output = [-1] * len(edges)
    for edge, label in zip(edges, pattern, strict=True):
        image = tuple(
            sorted(
                (
                    vertex_permutation[edge[0]],
                    vertex_permutation[edge[1]],
                )
            )
        )
        output[edge_positions[image]] = (
            3 if label == 3 else colour_permutation[label]
        )
    if any(label < 0 for label in output):
        raise AssertionError("pattern image missed a skeleton edge")
    return tuple(output)


def canonical_pattern(
    pattern: Pattern,
    edges: list[Edge],
    automorphisms: Iterable[tuple[int, ...]],
) -> Pattern:
    positions = {edge: index for index, edge in enumerate(edges)}
    return min(
        transform_pattern(
            pattern,
            edges,
            positions,
            automorphism,
            colour_permutation,
        )
        for automorphism in automorphisms
        for colour_permutation in itertools.permutations(range(3))
    )


def selected_entries(
    system: EquationSystem,
    edges: list[Edge],
    pattern: Pattern,
) -> set[int]:
    selected: set[int] = set()
    for edge, label in zip(edges, pattern, strict=True):
        base = 9 * system.edge_index[edge]
        if label == 3:
            selected.update(range(base, base + 9))
        else:
            selected.add(base + 4 * label)
    return selected


def activity_summary(
    system: EquationSystem,
    selected: set[int],
) -> tuple[dict[str, int], list[int]]:
    mask = np.zeros(system.variable_count, dtype=bool)
    mask[list(selected)] = True
    activity = np.all(mask[system.variable_ids], axis=2)
    counts = np.sum(activity, axis=0)
    forbidden = Counter(
        int(counts[equation])
        for equation, target in enumerate(system.target)
        if not bool(target)
    )
    required = [
        int(counts[equation])
        for equation, target in enumerate(system.target)
        if bool(target)
    ]
    return (
        {str(key): value for key, value in sorted(forbidden.items())},
        required,
    )


def write_model(path: Path, selected: set[int], variable_count: int) -> None:
    literals = [
        variable if variable - 1 in selected else -variable
        for variable in range(1, variable_count + 1)
    ]
    path.write_text(
        "s SATISFIABLE\nv "
        + " ".join(map(str, literals))
        + " 0\n",
        encoding="ascii",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--role-index", type=int, default=0)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(
        args.source_manifest.read_text(encoding="utf-8")
    )
    role = source["rows"][args.role_index]
    raw_edges = frozenset(
        tuple(map(int, edge)) for edge in role["skeleton_edges"]
    )
    if len(raw_edges) != 20:
        raise ValueError("selected role is not an exact-20-edge skeleton")
    system = EquationSystem(8, 3)
    edges = sorted(raw_edges)
    factors = double_c4_factors(raw_edges)
    matchings = [
        frozenset(tuple(map(int, edge)) for edge in matching)
        for matching in system.matchings
    ]
    patterns: set[Pattern] = set()
    for full_edges in factors:
        complement = raw_edges - full_edges
        supported_matchings = [
            matching for matching in matchings if matching <= complement
        ]
        partitions = {
            tuple(
                sorted(
                    tuple(sorted(matching))
                    for matching in triple
                )
            )
            for triple in itertools.combinations(supported_matchings, 3)
            if frozenset().union(*triple) == complement
        }
        for partition in partitions:
            labels = {edge: 3 for edge in full_edges}
            for colour, matching in enumerate(partition):
                for edge in matching:
                    labels[edge] = colour
            patterns.add(tuple(labels[edge] for edge in edges))

    automorphisms = skeleton_automorphisms(system.n, raw_edges)
    orbits: dict[Pattern, list[Pattern]] = defaultdict(list)
    for pattern in sorted(patterns):
        orbits[
            canonical_pattern(pattern, edges, automorphisms)
        ].append(pattern)

    args.output_directory.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for orbit_index, (canonical, members) in enumerate(
        sorted(orbits.items())
    ):
        selected = selected_entries(system, edges, canonical)
        forbidden_histogram, required_counts = activity_summary(
            system, selected
        )
        if "1" in forbidden_histogram or "2" in forbidden_histogram:
            raise AssertionError("enumerated macro support is not binomial-free")
        model = args.output_directory / (
            f"double_c4_singleton_orbit_{orbit_index:02d}.log"
        )
        write_model(model, selected, system.variable_count)
        rows.append(
            {
                "orbit_index": orbit_index,
                "orbit_size": len(members),
                "canonical_edge_labels": list(canonical),
                "selected_entries": len(selected),
                "selected_flat_indices": sorted(selected),
                "forbidden_activity_histogram": forbidden_histogram,
                "required_activity_counts": required_counts,
                "model": str(model),
                "model_sha256": sha256(model),
            }
        )

    payload = {
        "verified": True,
        "scope": (
            "complete double-C4 full-block plus 3-matching singleton "
            "family on one exact-20-edge skeleton"
        ),
        "claim_scope": (
            "exhausts this macro-family only; does not show that every "
            "support has this form"
        ),
        "source_manifest": str(args.source_manifest),
        "source_manifest_sha256": sha256(args.source_manifest),
        "role_index": args.role_index,
        "skeleton_edges": [list(edge) for edge in edges],
        "double_c4_factors": len(factors),
        "skeleton_automorphisms": len(automorphisms),
        "colour_unlabelled_factorizations": len(patterns),
        "labelled_supports": 6 * len(patterns),
        "support_orbits": len(rows),
        "orbits": rows,
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
                    "double_c4_factors",
                    "skeleton_automorphisms",
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
