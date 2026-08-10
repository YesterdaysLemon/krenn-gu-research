"""Heuristically search for a no-one-term support with no matching fork."""

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

from krenn_gu.explore_random_even_cycle_forks import Edge, cycle_edges, perfect_matchings
from explore_random_minimal_singleton_sets import (
    analyze_support,
    contiguous_cycles,
)
from search_minimal_singleton_counterexample import mutate, state_key


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("perfect matching misses a vertex")


def matching_fork_count(
    n: int,
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
) -> tuple[int, int]:
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    matchings = perfect_matchings(n, set(full_edges) | set(labels))
    singleton_sets = [
        frozenset(item for item in matching if item in labels)
        for matching in matchings
    ]
    count = 0
    for rich_id, target in enumerate(singleton_sets):
        if (
            len(target) == n // 2
            and len({labels[item] for item in target}) == 1
        ):
            continue
        for removed in target:
            sparse_target = target - {removed}
            sparse_ids = [
                matching_id
                for matching_id, singleton_set in enumerate(singleton_sets)
                if singleton_set <= sparse_target
            ]
            if not sparse_ids:
                continue
            rich_ids = [
                matching_id
                for matching_id, singleton_set in enumerate(singleton_sets)
                if singleton_set <= target
            ]
            if set(rich_ids) - set(sparse_ids) != {rich_id}:
                continue
            for changed_vertex in removed:
                partners = {
                    partner_at(matchings[item], changed_vertex)
                    for item in sparse_ids
                }
                if len(partners) != 1:
                    continue
                partner = next(iter(partners))
                common_edge = (
                    (changed_vertex, partner)
                    if changed_vertex < partner
                    else (partner, changed_vertex)
                )
                if common_edge in full_edges:
                    count += 1
    return count, len(matchings)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--initial",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_direct_free_search_p500000_multiswitch.json"
        ),
    )
    parser.add_argument("--steps", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260804)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_no_matching_fork_search.json"
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
        result = analyze_support(n, cycles, full_edges, singletons)
        one_term = int(result["one_term_minimal_sets"])
        if one_term:
            forks = None
            score = 100_000 + one_term
        else:
            forks, matching_count = matching_fork_count(
                n, full_edges, singletons
            )
            if matching_count != int(
                result["skeleton_perfect_matchings"]
            ):
                raise AssertionError("matching enumerators disagree")
            score = forks
        output = {
            **result,
            "matching_forks": forks,
            "search_score": score,
        }
        cache[key] = output
        return output

    current_result = evaluate(current)
    best = state_key(current)
    best_result = dict(current_result)
    history = [
        {
            "step": 0,
            "score": int(best_result["search_score"]),
            "one_term": int(best_result["one_term_minimal_sets"]),
            "matching_forks": best_result["matching_forks"],
        }
    ]
    started = time.perf_counter()
    for step in range(1, args.steps + 1):
        proposal = current
        for _ in range(rng.randint(1, 20)):
            changed = mutate(proposal, full_edges, rng)
            if changed is not None:
                proposal = changed
        if proposal == current:
            continue
        proposal_result = evaluate(proposal)
        current_score = int(current_result["search_score"])
        proposal_score = int(proposal_result["search_score"])
        fraction = step / args.steps
        temperature = 10.0 * (0.005**fraction)
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
                    "one_term": int(
                        best_result["one_term_minimal_sets"]
                    ),
                    "matching_forks": best_result["matching_forks"],
                }
            )
            print(
                f"best={best_result['search_score']} "
                f"one_term={best_result['one_term_minimal_sets']} "
                f"forks={best_result['matching_forks']} step={step}",
                flush=True,
            )
            if best_result["search_score"] == 0:
                break
    payload = {
        "status": (
            "no_matching_fork_candidate"
            if best_result["search_score"] == 0
            else "matching_forks_persist"
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
