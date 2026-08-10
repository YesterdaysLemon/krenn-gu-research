"""Enumerate killer-label orbits on a fixed six-vertex union skeleton."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import argparse
import itertools
import json
from pathlib import Path

from krenn_gu.enumerate_cubic_rankone import (
    graph_automorphisms,
    nested_pattern,
    transform_pattern,
)

Edge = tuple[int, int]
Pattern = tuple[int, ...]


def parse_edges(text: str) -> frozenset[Edge]:
    return frozenset(
        tuple(sorted((int(token[0]), int(token[1]))))
        for token in text.split(",")
        if token
    )


def union_from_missing(missing: frozenset[Edge]) -> frozenset[Edge]:
    return frozenset(
        (first, second)
        for first in range(6)
        for second in range(first + 1, 6)
        if (first, second) not in missing
    )


def pattern_union(pattern: Pattern) -> frozenset[Edge]:
    return frozenset(
        tuple(sorted((vertex, pattern[3 * vertex + colour])))
        for vertex in range(6)
        for colour in range(3)
    )


def raw_patterns(edges: frozenset[Edge]) -> set[Pattern]:
    choices = []
    for vertex in range(6):
        neighbours = sorted(
            other
            for edge in edges
            if vertex in edge
            for other in edge
            if other != vertex
        )
        choices.append(tuple(itertools.permutations(neighbours, 3)))
    return {
        tuple(value for row in rows for value in row)
        for rows in itertools.product(*choices)
        if pattern_union(
            tuple(value for row in rows for value in row)
        )
        == edges
    }


def orbit_representatives(edges: frozenset[Edge]) -> list[Pattern]:
    automorphisms = graph_automorphisms(edges)
    colour_permutations = tuple(itertools.permutations(range(3)))
    unseen = raw_patterns(edges)
    representatives: list[Pattern] = []
    for seed in sorted(unseen):
        if seed not in unseen:
            continue
        orbit = {
            transform_pattern(seed, vertices, colours)
            for vertices in automorphisms
            for colours in colour_permutations
        }
        representatives.append(min(orbit))
        unseen -= orbit
    if unseen:
        raise AssertionError("orbit traversal did not exhaust the patterns")
    return sorted(representatives)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--missing-edges",
        required=True,
        help="comma-separated complement edges, for example 01,12,23,30,45",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    missing = parse_edges(args.missing_edges)
    edges = union_from_missing(missing)
    representatives = orbit_representatives(edges)
    payload = {
        "missing_edges": [list(edge) for edge in sorted(missing)],
        "union_edges": len(edges),
        "automorphisms": len(graph_automorphisms(edges)),
        "orbits": len(representatives),
        "representatives": [
            nested_pattern(pattern) for pattern in representatives
        ],
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: raw={len(raw_patterns(edges))} "
            f"orbits={len(representatives)}"
        )
    else:
        print(text)


if __name__ == "__main__":
    main()
