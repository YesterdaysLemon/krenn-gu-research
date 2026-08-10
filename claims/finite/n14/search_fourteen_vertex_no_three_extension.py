"""Search for a no-one-term support without a canonical three-PM extension."""

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
import json
import math
import random
import time
from pathlib import Path
from typing import Sequence

from krenn_gu.explore_random_even_cycle_forks import Edge, cycle_edges
from explore_random_minimal_singleton_sets import (
    analyze_support,
    contiguous_cycles,
)
from search_minimal_singleton_counterexample import mutate, state_key

from verify_fourteen_vertex_no_one_term_support import perfect_matchings


def extension_count(
    cycles: Sequence[Sequence[int]],
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
) -> tuple[int, list[dict[str, object]]]:
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    matchings = perfect_matchings(set(full_edges) | set(labels))
    representatives: dict[
        frozenset[Edge], tuple[Edge, ...]
    ] = {}
    matching_groups: dict[
        frozenset[Edge], list[tuple[Edge, ...]]
    ] = {}
    for matching in matchings:
        target = frozenset(set(matching) & set(labels))
        representatives.setdefault(target, matching)
        matching_groups.setdefault(target, []).append(matching)
    feasible = set(representatives)
    minimal = [
        target
        for target in feasible
        if not any(other < target for other in feasible)
    ]
    even_vertices = {
        vertex
        for cycle in cycles
        if len(cycle) % 2 == 0
        for vertex in cycle
    }
    certificates: dict[
        frozenset[Edge], dict[str, object]
    ] = {}
    for target in minimal:
        if len(target) != 1:
            continue
        singleton = next(iter(target))
        colour = labels[singleton]
        for base in matching_groups[target]:
            symmetric = set(base) ^ set(singletons[colour])
            adjacency: dict[int, list[tuple[int, Edge]]] = {
                vertex: [] for item in symmetric for vertex in item
            }
            for first, second in symmetric:
                adjacency[first].append((second, (first, second)))
                adjacency[second].append((first, (first, second)))
            unseen = set(adjacency)
            while unseen:
                start = min(unseen)
                vertices: set[int] = set()
                edges: set[Edge] = set()
                stack = [start]
                while stack:
                    vertex = stack.pop()
                    if vertex in vertices:
                        continue
                    vertices.add(vertex)
                    unseen.discard(vertex)
                    for other, item in adjacency[vertex]:
                        edges.add(item)
                        stack.append(other)
                if not (vertices & even_vertices):
                    continue
                extension = frozenset(
                    {singleton}
                    | (edges & set(singletons[colour]))
                )
                active_graph = set(full_edges) | set(extension)
                active_matchings = perfect_matchings(active_graph)
                if len(active_matchings) != 3:
                    continue
                certificates.setdefault(
                    extension,
                    {
                        "minimal_singleton_edge": list(singleton),
                        "colour": colour,
                        "extension_singleton_edges": [
                            list(item) for item in sorted(extension)
                        ],
                        "alternating_component_vertices": sorted(vertices),
                    },
                )
    return len(certificates), list(certificates.values())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--initial",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_direct_free_search_p200000.json"
        ),
    )
    parser.add_argument("--steps", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_no_three_extension_search.json"
        ),
    )
    args = parser.parse_args()
    initial = json.loads(args.initial.read_text(encoding="utf-8"))
    lengths = tuple(map(int, initial["full_cycle_type"]))
    n = sum(lengths)
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    current = tuple(
        tuple(tuple(map(int, item)) for item in matching)
        for matching in initial["best_singleton_matchings"]
    )
    rng = random.Random(args.seed)
    cache: dict[
        tuple[tuple[Edge, ...], ...], dict[str, object]
    ] = {}

    def evaluate(
        singletons: Sequence[Sequence[Edge]],
    ) -> dict[str, object]:
        key = state_key(singletons)
        if key in cache:
            return cache[key]
        poset = analyze_support(
            n, cycles, full_edges, singletons
        )
        one_term = int(poset["one_term_minimal_sets"])
        if one_term:
            count = None
            certificates = []
            score = 100_000 + one_term
        else:
            count, certificates = extension_count(
                cycles, full_edges, singletons
            )
            score = count
        result = {
            **poset,
            "three_matching_extensions": count,
            "extension_certificates": certificates,
            "search_score": score,
        }
        cache[key] = result
        return result

    current_result = evaluate(current)
    best = state_key(current)
    best_result = dict(current_result)
    history = [
        {
            "step": 0,
            "score": int(best_result["search_score"]),
            "extensions": best_result["three_matching_extensions"],
        }
    ]
    started = time.perf_counter()
    for step in range(1, args.steps + 1):
        proposal = current
        for _ in range(rng.randint(1, 4)):
            changed = mutate(proposal, full_edges, rng)
            if changed is not None:
                proposal = changed
        if proposal == current:
            continue
        proposal_result = evaluate(proposal)
        current_score = int(current_result["search_score"])
        proposal_score = int(proposal_result["search_score"])
        fraction = step / args.steps
        temperature = 4.0 * (0.005**fraction)
        if (
            proposal_score <= current_score
            or rng.random()
            < math.exp(
                -(proposal_score - current_score) / temperature
            )
        ):
            current = proposal
            current_result = proposal_result
        if int(current_result["search_score"]) < int(
            best_result["search_score"]
        ):
            best = state_key(current)
            best_result = dict(current_result)
            history.append(
                {
                    "step": step,
                    "score": int(best_result["search_score"]),
                    "extensions": best_result[
                        "three_matching_extensions"
                    ],
                }
            )
            print(
                f"best={best_result['search_score']} step={step}",
                flush=True,
            )
            if best_result["search_score"] == 0:
                break
    payload = {
        "status": (
            "no_canonical_three_extension_candidate"
            if best_result["search_score"] == 0
            else "exploratory_extensions_persist"
        ),
        "necessary_conditions_only": True,
        "full_cycle_type": list(lengths),
        "steps": args.steps,
        "states_evaluated": len(cache),
        "elapsed_seconds": time.perf_counter() - started,
        "best_result": best_result,
        "best_singleton_matchings": [
            [list(item) for item in matching]
            for matching in best
        ],
        "history": history,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "history"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
