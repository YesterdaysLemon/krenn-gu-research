"""Independently audit a mixed reciprocal 84-entry support."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

from eight_vertex_sparse_exact import positive_model_literals
from search_witness import EquationSystem
from support_toric_degeneration import (
    verify_balanced_certificate,
    verify_degeneration_certificate,
)

Edge = tuple[int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def blocks(
    selected: set[int],
    system: EquationSystem,
) -> dict[Edge, set[int]]:
    output: dict[Edge, set[int]] = {}
    for flat in selected:
        edge_index, position = divmod(flat, system.d**2)
        output.setdefault(system.edges[edge_index], set()).add(position)
    return output


def degrees(edges: set[Edge], n: int) -> list[int]:
    return [
        sum(vertex in edge for edge in edges)
        for vertex in range(n)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.manifest.read_text(encoding="utf-8"))
    if source["status"] != "MIXED_NO_BINOMIAL_SUPPORT_FOUND":
        raise AssertionError("discovery manifest has no mixed survivor")
    model = Path(source["model"])
    if sha256(model) != source["model_sha256"]:
        raise AssertionError("support model hash changed")
    support = {
        literal - 1
        for literal in positive_model_literals(model)
        if 1 <= literal <= 252
    }
    recorded = set(
        map(int, source["witness"]["selected_flat_indices"])
    )
    if support != recorded:
        raise AssertionError("model and recorded support differ")

    system = EquationSystem(8, 3)
    block_map = blocks(support, system)
    size_histogram = Counter(map(len, block_map.values()))
    if size_histogram != {1: 12, 9: 8}:
        raise AssertionError("support is not 12-singleton/8-full")
    full_edges = {
        edge for edge, entries in block_map.items() if len(entries) == 9
    }
    singleton_edges = {
        edge for edge, entries in block_map.items() if len(entries) == 1
    }
    if degrees(full_edges, system.n) != [2] * system.n:
        raise AssertionError("full blocks do not form a spanning 2-factor")
    if degrees(singleton_edges, system.n) != [3] * system.n:
        raise AssertionError("singleton blocks do not form a cubic graph")

    incidence_colours: dict[tuple[int, Edge], int] = {}
    monochromatic_edges: set[Edge] = set()
    monochromatic = 0
    bichromatic = 0
    for edge in sorted(singleton_edges):
        position = next(iter(block_map[edge]))
        first_colour, second_colour = divmod(position, system.d)
        incidence_colours[(edge[0], edge)] = first_colour
        incidence_colours[(edge[1], edge)] = second_colour
        if first_colour == second_colour:
            monochromatic += 1
            monochromatic_edges.add(edge)
        else:
            bichromatic += 1
    if not bichromatic:
        raise AssertionError("support has no bichromatic singleton")
    if {
        vertex
        for edge in monochromatic_edges
        for vertex in edge
    } != set(range(system.n)):
        raise AssertionError(
            "monochromatic singleton edges do not cover every vertex"
        )
    for vertex in range(system.n):
        observed: list[int] = []
        for edge in singleton_edges:
            if vertex not in edge:
                continue
            opposite = edge[1] if vertex == edge[0] else edge[0]
            observed.append(incidence_colours[(opposite, edge)])
        observed.sort()
        if observed != list(range(system.d)):
            raise AssertionError(
                f"vertex {vertex} does not send each killer colour once"
            )

    mask = np.zeros(system.variable_count, dtype=bool)
    mask[list(support)] = True
    activity = np.all(mask[system.variable_ids], axis=2)
    counts = np.sum(activity, axis=0)
    forbidden_histogram = Counter(
        int(counts[index])
        for index, required in enumerate(system.target)
        if not bool(required)
    )
    required_counts = [
        int(counts[index])
        for index, required in enumerate(system.target)
        if bool(required)
    ]
    recorded_histogram = {
        int(key): int(value)
        for key, value in source["witness"][
            "forbidden_activity_histogram"
        ].items()
    }
    if dict(sorted(forbidden_histogram.items())) != recorded_histogram:
        raise AssertionError("forbidden activity histogram changed")
    if required_counts != list(
        map(int, source["witness"]["required_activity_counts"])
    ):
        raise AssertionError("required activity counts changed")
    if 1 in forbidden_histogram or 2 in forbidden_histogram:
        raise AssertionError("support contains a forbidden mono/binomial")
    if min(required_counts) <= 0:
        raise AssertionError("a required amplitude has empty support")

    toric_certificate = source["toric_certificate"]
    if toric_certificate["mode"] == "balanced_support":
        toric_audit = verify_balanced_certificate(
            system,
            support,
            toric_certificate,
        )
    elif toric_certificate["mode"] == "support_degeneration":
        toric_audit = verify_degeneration_certificate(
            system,
            support,
            toric_certificate,
        )
    else:
        raise AssertionError("unknown toric-certificate mode")

    payload = {
        "verified": True,
        "scope": source["scope"],
        "necessary_conditions_only": True,
        "selected_entries": len(support),
        "nonzero_blocks": len(block_map),
        "block_size_histogram": {
            str(key): value
            for key, value in sorted(size_histogram.items())
        },
        "full_factor_degrees": degrees(full_edges, system.n),
        "singleton_degrees": degrees(singleton_edges, system.n),
        "monochromatic_singletons": monochromatic,
        "bichromatic_singletons": bichromatic,
        "forbidden_activity_histogram": {
            str(key): value
            for key, value in sorted(forbidden_histogram.items())
        },
        "required_activity_counts": required_counts,
        "toric_certificate": toric_audit,
        "model_sha256": sha256(model),
        "manifest_sha256": sha256(args.manifest),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
