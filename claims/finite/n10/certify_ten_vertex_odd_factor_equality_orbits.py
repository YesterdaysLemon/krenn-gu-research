"""Find a forbidden one-term amplitude in every odd-factor equality orbit."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

from explore_random_even_cycle_forks import colouring_table, perfect_matchings

Edge = tuple[int, int]


def one_term_certificate(
    full_edges: set[Edge],
    singleton_matchings: list[list[Edge]],
    colourings: np.ndarray,
) -> dict[str, object]:
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    if len(labels) != 15:
        raise AssertionError("singleton matchings overlap")
    skeleton = full_edges | set(labels)
    matchings = perfect_matchings(10, skeleton)
    counts = np.zeros(len(colourings), dtype=np.int16)
    last = np.full(len(colourings), -1, dtype=np.int16)
    for matching_id, matching in enumerate(matchings):
        requirements: dict[int, int] = {}
        viable = True
        for item in matching:
            if item not in labels:
                continue
            colour = labels[item]
            for vertex in item:
                if (
                    vertex in requirements
                    and requirements[vertex] != colour
                ):
                    viable = False
                    break
                requirements[vertex] = colour
            if not viable:
                break
        if not viable:
            continue
        mask = np.ones(len(colourings), dtype=bool)
        for vertex, colour in requirements.items():
            mask &= colourings[:, vertex] == colour
        counts += mask
        last[mask] = matching_id
    monochromatic = np.all(
        colourings == colourings[:, :1], axis=1
    )
    candidates = np.flatnonzero((counts == 1) & ~monochromatic)
    if not len(candidates):
        raise AssertionError("support has no forbidden one-term amplitude")
    equation = int(candidates[0])
    matching_id = int(last[equation])
    if matching_id < 0:
        raise AssertionError("one-term activity lost its matching")
    return {
        "skeleton_perfect_matchings": len(matchings),
        "one_term_forbidden_colourings": len(candidates),
        "equation_index": equation,
        "colouring": list(map(int, colourings[equation])),
        "unique_matching_index": matching_id,
        "unique_matching": [
            list(item) for item in matchings[matching_id]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.orbits.read_text(encoding="utf-8"))
    if source.get("status") != "complete":
        raise AssertionError("orbit catalogue is incomplete")
    cycle_type = list(map(int, source["full_cycle_type"]))
    if all(length % 2 == 0 for length in cycle_type):
        raise AssertionError("factor type has no odd cycle")
    full_edges = {
        tuple(map(int, item)) for item in source["full_edges"]
    }
    colourings = colouring_table(10)
    rows: list[dict[str, object]] = []
    started = time.perf_counter()
    for index, orbit in enumerate(source["rows"]):
        singleton_matchings = [
            [tuple(map(int, item)) for item in matching]
            for matching in orbit["singleton_matchings"]
        ]
        certificate = one_term_certificate(
            full_edges, singleton_matchings, colourings
        )
        rows.append(
            {
                "orbit_index": index,
                "orbit_size_uncoloured": int(
                    orbit["orbit_size_uncoloured"]
                ),
                "singleton_matchings": orbit["singleton_matchings"],
                **certificate,
            }
        )
        if (index + 1) % 25 == 0 or index + 1 == len(source["rows"]):
            print(
                f"orbit={index + 1}/{len(source['rows'])} "
                f"one_terms={certificate['one_term_forbidden_colourings']}",
                flush=True,
            )
    payload = {
        "status": "all_one_term",
        "scope": (
            "all n=10,d=3 equality supports with full-factor type "
            f"{cycle_type}, modulo vertex and global-colour symmetry"
        ),
        "necessary_conditions_only": False,
        "orbit_catalogue": str(args.orbits),
        "full_cycle_type": cycle_type,
        "raw_uncoloured_factorizations": int(
            source["raw_uncoloured_factorizations"]
        ),
        "support_orbits": len(rows),
        "certified_orbits": len(rows),
        "minimum_one_term_colourings": min(
            int(row["one_term_forbidden_colourings"]) for row in rows
        ),
        "maximum_one_term_colourings": max(
            int(row["one_term_forbidden_colourings"]) for row in rows
        ),
        "rows": rows,
        "solve_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
