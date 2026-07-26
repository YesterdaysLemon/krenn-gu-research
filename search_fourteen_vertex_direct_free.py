"""Heuristically remove both one-term and direct binomial/trinomial motifs."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

import numpy as np

from explore_random_even_cycle_forks import Edge, cycle_edges
from explore_random_minimal_singleton_sets import (
    analyze_support,
    contiguous_cycles,
)
from search_minimal_singleton_counterexample import mutate, state_key
from verify_fourteen_vertex_no_one_term_support import perfect_matchings


def indexed_colouring(index: int, n: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(n))


def direct_hits(
    n: int,
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
    prefix: int,
) -> tuple[int, int, int]:
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    matchings = perfect_matchings(set(full_edges) | set(labels))
    all_edges = tuple(itertools.combinations(range(n), 2))
    edge_index = {item: index for index, item in enumerate(all_edges)}

    def activity(colouring: Sequence[int]) -> tuple[int, ...]:
        return tuple(
            matching_id
            for matching_id, matching in enumerate(matchings)
            if all(
                item in full_edges
                or (
                    colouring[item[0]]
                    == colouring[item[1]]
                    == labels[item]
                )
                for item in matching
            )
        )

    def signature(
        first: Sequence[Edge],
        second: Sequence[Edge],
        colouring: Sequence[int],
    ) -> tuple[tuple[int, int], ...]:
        def variables(matching: Sequence[Edge]) -> list[int]:
            output = []
            for item in matching:
                if item in full_edges:
                    first_colour = int(colouring[item[0]])
                    second_colour = int(colouring[item[1]])
                else:
                    first_colour = second_colour = labels[item]
                output.append(
                    9 * edge_index[item]
                    + 3 * first_colour
                    + second_colour
                )
            return output

        vector: Counter[int] = Counter(variables(first))
        vector.subtract(variables(second))
        direct = tuple(
            sorted(
                (entry, coefficient)
                for entry, coefficient in vector.items()
                if coefficient
            )
        )
        negative = tuple(
            (entry, -coefficient) for entry, coefficient in direct
        )
        return min(direct, negative)

    indices = np.arange(prefix, dtype=np.int64)
    colourings = np.empty((prefix, n), dtype=np.int8)
    for vertex in range(n):
        colourings[:, vertex] = (
            indices // (3**vertex)
        ) % 3
    counts = np.zeros(prefix, dtype=np.int16)
    first_id = np.full(prefix, -1, dtype=np.int16)
    second_id = np.full(prefix, -1, dtype=np.int16)
    third_id = np.full(prefix, -1, dtype=np.int16)
    for matching_id, matching in enumerate(matchings):
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        mask = np.ones(prefix, dtype=bool)
        for vertex, colour in requirements.items():
            mask &= colourings[:, vertex] == colour
        first_id[mask & (counts == 0)] = matching_id
        second_id[mask & (counts == 1)] = matching_id
        third_id[mask & (counts == 2)] = matching_id
        counts += mask
    def relevant_vertices(
        first: Sequence[Edge],
        second: Sequence[Edge],
    ) -> tuple[int, ...]:
        return tuple(
            sorted(
                {
                    vertex
                    for item in itertools.chain(first, second)
                    if item in full_edges
                    for vertex in item
                }
            )
        )

    def codes_for(
        equation_indices: np.ndarray,
        vertices: Sequence[int],
    ) -> np.ndarray:
        codes = np.zeros(len(equation_indices), dtype=np.int64)
        for position, vertex in enumerate(vertices):
            codes += (
                (equation_indices // (3**vertex)) % 3
            ) * (3**position)
        return codes

    binomial = np.flatnonzero(counts == 2)
    binomial_keys = (
        first_id[binomial].astype(np.int32) * len(matchings)
        + second_id[binomial].astype(np.int32)
    )
    relations: set[tuple[tuple[int, int], ...]] = set()
    for pair_key in np.unique(binomial_keys):
        pair_indices = binomial[binomial_keys == pair_key]
        first = int(pair_key // len(matchings))
        second = int(pair_key % len(matchings))
        vertices = relevant_vertices(
            matchings[first], matchings[second]
        )
        _, positions = np.unique(
            codes_for(pair_indices, vertices), return_index=True
        )
        for position in positions:
            equation = int(pair_indices[position])
            relations.add(
                signature(
                    matchings[first],
                    matchings[second],
                    colourings[equation],
                )
            )
    hit_signatures: set[tuple[tuple[int, int], ...]] = set()
    trinomial = np.flatnonzero(counts == 3)
    id_arrays = (first_id, second_id, third_id)
    for left_position, right_position in ((0, 1), (0, 2), (1, 2)):
        left = id_arrays[left_position][trinomial]
        right = id_arrays[right_position][trinomial]
        target_keys = (
            left.astype(np.int32) * len(matchings)
            + right.astype(np.int32)
        )
        for pair_key in np.unique(target_keys):
            pair_indices = trinomial[target_keys == pair_key]
            first = int(pair_key // len(matchings))
            second = int(pair_key % len(matchings))
            vertices = relevant_vertices(
                matchings[first], matchings[second]
            )
            _, positions = np.unique(
                codes_for(pair_indices, vertices), return_index=True
            )
            for position in positions:
                equation = int(pair_indices[position])
                target_signature = signature(
                    matchings[first],
                    matchings[second],
                    colourings[equation],
                )
                if target_signature in relations:
                    hit_signatures.add(target_signature)
    return len(hit_signatures), len(relations), len(matchings)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--initial",
        type=Path,
        default=Path(
            "tmp/minimal_singleton_counterexample_search_small.json"
        ),
    )
    parser.add_argument("--steps", type=int, default=2_000)
    parser.add_argument("--prefix", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_direct_free_search.json"
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
        result = analyze_support(
            n, cycles, full_edges, singletons
        )
        one_term = int(result["one_term_minimal_sets"])
        if one_term:
            result["direct_relation_hits_in_prefix"] = None
            result["distinct_binomial_relations_in_prefix"] = None
            result["screening_prefixes"] = []
            result["search_score"] = 1_000_000 + one_term
        else:
            prefixes = sorted(
                {
                    min(args.prefix, 100_000),
                    min(args.prefix, 200_000),
                    args.prefix,
                }
            )
            screening = []
            for stage, prefix in enumerate(prefixes):
                hits, relations, matching_count = direct_hits(
                    n, full_edges, singletons, prefix
                )
                if matching_count != int(
                    result["skeleton_perfect_matchings"]
                ):
                    raise AssertionError("matching enumerators disagree")
                screening.append(
                    {
                        "prefix": prefix,
                        "direct_relation_hits": hits,
                        "distinct_binomial_relations": relations,
                    }
                )
                if hits:
                    remaining_stages = len(prefixes) - stage - 1
                    result["direct_relation_hits_in_prefix"] = hits
                    result[
                        "distinct_binomial_relations_in_prefix"
                    ] = relations
                    result["screening_prefixes"] = screening
                    result["search_score"] = (
                        10_000 * remaining_stages + hits
                    )
                    break
            else:
                result["direct_relation_hits_in_prefix"] = 0
                result[
                    "distinct_binomial_relations_in_prefix"
                ] = screening[-1]["distinct_binomial_relations"]
                result["screening_prefixes"] = screening
                result["search_score"] = 0
        cache[key] = result
        return result

    current_result = evaluate(current)
    best = current
    best_result = dict(current_result)
    history = [
        {
            "step": 0,
            "search_score": int(best_result["search_score"]),
            "one_term_minimal_sets": int(
                best_result["one_term_minimal_sets"]
            ),
            "direct_relation_hits_in_prefix": best_result[
                "direct_relation_hits_in_prefix"
            ],
        }
    ]
    started = time.perf_counter()
    for step in range(1, args.steps + 1):
        proposal = current
        for _ in range(rng.randint(1, 20)):
            changed = mutate(proposal, full_edges, rng)
            if changed is None:
                continue
            proposal = changed
        if proposal == current:
            continue
        proposal_result = evaluate(proposal)
        current_score = int(current_result["search_score"])
        proposal_score = int(proposal_result["search_score"])
        fraction = step / args.steps
        temperature = 8.0 * (0.01**fraction)
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
                    "search_score": int(
                        best_result["search_score"]
                    ),
                    "one_term_minimal_sets": int(
                        best_result["one_term_minimal_sets"]
                    ),
                    "direct_relation_hits_in_prefix": best_result[
                        "direct_relation_hits_in_prefix"
                    ],
                }
            )
            print(
                f"best_score={best_result['search_score']} "
                f"one_term={best_result['one_term_minimal_sets']} "
                f"direct={best_result['direct_relation_hits_in_prefix']} "
                f"step={step}",
                flush=True,
            )
            if best_result["search_score"] == 0:
                break
    payload = {
        "status": (
            "prefix_direct_free_candidate"
            if best_result["search_score"] == 0
            else "exploratory_no_prefix_direct_free_support"
        ),
        "necessary_conditions_only": True,
        "full_cycle_type": list(lengths),
        "search_prefix": args.prefix,
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
