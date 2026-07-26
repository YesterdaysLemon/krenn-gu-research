"""Heuristic search for a mixed-factor failure of the one-term criterion.

Mutate the three singleton perfect matchings by two-edge switches and
minimize the number of inclusion-minimal feasible singleton sets that touch
every full-factor cycle.  Reaching zero would be a counterexample to the
candidate extension of the all-odd theorem (not a Krenn--Gu witness).
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path
from typing import Sequence

from explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    edge,
    random_singletons,
)
from explore_random_minimal_singleton_sets import (
    analyze_support,
    contiguous_cycles,
)


def state_key(
    singletons: Sequence[Sequence[Edge]],
) -> tuple[tuple[Edge, ...], ...]:
    return tuple(tuple(sorted(matching)) for matching in singletons)


def mutate(
    singletons: Sequence[Sequence[Edge]],
    full_edges: frozenset[Edge],
    rng: random.Random,
) -> tuple[tuple[Edge, ...], ...] | None:
    colour = rng.randrange(3)
    matching = list(singletons[colour])
    other_edges = {
        item
        for other_colour, other in enumerate(singletons)
        if other_colour != colour
        for item in other
    }
    for _attempt in range(30):
        first_index, second_index = rng.sample(range(len(matching)), 2)
        a, b = matching[first_index]
        c, d = matching[second_index]
        alternatives = [
            (edge(a, c), edge(b, d)),
            (edge(a, d), edge(b, c)),
        ]
        rng.shuffle(alternatives)
        for replacement in alternatives:
            if any(
                item in full_edges or item in other_edges
                for item in replacement
            ):
                continue
            changed = list(matching)
            changed[first_index], changed[second_index] = replacement
            output = [tuple(items) for items in singletons]
            output[colour] = tuple(sorted(changed))
            return tuple(output)
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", default="3+4+7")
    parser.add_argument("--steps", type=int, default=5_000)
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/minimal_singleton_counterexample_search.json"
        ),
    )
    args = parser.parse_args()
    lengths = tuple(map(int, args.partition.split("+")))
    n = sum(lengths)
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    rng = random.Random(args.seed)
    cache: dict[
        tuple[tuple[Edge, ...], ...], dict[str, object]
    ] = {}

    def evaluate(
        singletons: Sequence[Sequence[Edge]],
    ) -> dict[str, object]:
        key = state_key(singletons)
        if key not in cache:
            cache[key] = analyze_support(
                n, cycles, full_edges, singletons
            )
        return cache[key]

    best_state: tuple[tuple[Edge, ...], ...] | None = None
    best_result: dict[str, object] | None = None
    started = time.perf_counter()
    history: list[dict[str, int]] = []
    for restart in range(args.restarts):
        current = random_singletons(n, full_edges, rng)
        current_result = evaluate(current)
        for step in range(args.steps):
            proposal = mutate(current, full_edges, rng)
            if proposal is None:
                continue
            proposal_result = evaluate(proposal)
            current_score = int(
                current_result["one_term_minimal_sets"]
            )
            proposal_score = int(
                proposal_result["one_term_minimal_sets"]
            )
            fraction = step / max(1, args.steps - 1)
            temperature = 5.0 * (0.02**fraction)
            if (
                proposal_score <= current_score
                or rng.random()
                < math.exp(
                    -(proposal_score - current_score) / temperature
                )
            ):
                current = proposal
                current_result = proposal_result
            if best_result is None or int(
                current_result["one_term_minimal_sets"]
            ) < int(best_result["one_term_minimal_sets"]):
                best_state = state_key(current)
                best_result = dict(current_result)
                history.append(
                    {
                        "restart": restart,
                        "step": step,
                        "one_term_minimal_sets": int(
                            best_result["one_term_minimal_sets"]
                        ),
                    }
                )
                print(
                    f"best={best_result['one_term_minimal_sets']} "
                    f"restart={restart} step={step}",
                    flush=True,
                )
                if best_result["one_term_minimal_sets"] == 0:
                    break
        if (
            best_result is not None
            and best_result["one_term_minimal_sets"] == 0
        ):
            break
    if best_state is None or best_result is None:
        raise AssertionError("search did not evaluate a state")
    payload = {
        "status": (
            "counterexample_candidate"
            if best_result["one_term_minimal_sets"] == 0
            else "exploratory_no_counterexample"
        ),
        "necessary_conditions_only": True,
        "full_cycle_type": list(lengths),
        "steps_per_restart": args.steps,
        "restarts": args.restarts,
        "states_evaluated": len(cache),
        "elapsed_seconds": time.perf_counter() - started,
        "best_result": best_result,
        "best_singleton_matchings": [
            [list(item) for item in matching]
            for matching in best_state
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
