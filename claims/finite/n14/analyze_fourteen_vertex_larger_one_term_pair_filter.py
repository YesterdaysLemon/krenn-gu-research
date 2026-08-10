"""Filter factor pairs by larger one-term matching-set catalogues."""

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
import itertools
import json
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    completion_tables,
    contiguous_cycles,
    factor_safe,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges, perfect_matchings

Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument("one_term_catalogue", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_larger_one_term_pair_filter.json"
        ),
    )
    args = parser.parse_args()
    census = json.loads(args.census.read_text(encoding="utf-8"))
    catalogue = json.loads(
        args.one_term_catalogue.read_text(encoding="utf-8")
    )
    lengths = tuple(map(int, census["partition"]))
    if tuple(map(int, catalogue["partition"])) != lengths:
        raise ValueError("catalogue partition mismatch")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    if tuple(
        tuple(map(int, item)) for item in catalogue["eligible_edges"]
    ) != eligible_edges:
        raise ValueError("catalogue edge order mismatch")
    edge_id = {
        item: position for position, item in enumerate(eligible_edges)
    }
    vertex_component = {
        vertex: component
        for component, cycle in enumerate(cycles)
        for vertex in cycle
    }
    tables = completion_tables(cycles)
    factors = perfect_matchings(N, set(eligible_edges))
    safe_factors = [
        factor
        for factor in factors
        if factor_safe(
            factor, cycles, vertex_component, tables
        )
    ]

    def mask(items: Factor | tuple[Edge, ...] | set[Edge]) -> int:
        return sum(1 << edge_id[item] for item in items)

    one_terms = {
        int(size): set(map(int, masks))
        for size, masks in catalogue["one_term_masks_by_size"].items()
    }
    size_three = one_terms.get(3, set())
    pair_completions: dict[tuple[int, int], int] = {}
    for target_mask in size_three:
        item_ids = tuple(
            position
            for position in range(len(eligible_edges))
            if target_mask & (1 << position)
        )
        for first, second in itertools.combinations(item_ids, 2):
            third = next(
                item
                for item in item_ids
                if item not in {first, second}
            )
            pair_completions[(first, second)] = (
                pair_completions.get((first, second), 0)
                | (1 << third)
            )

    def completion(items: Factor) -> int:
        item_ids = sorted(edge_id[item] for item in items)
        output = 0
        for first, second in itertools.combinations(item_ids, 2):
            output |= pair_completions.get((first, second), 0)
        return output

    rows = [
        (mask(factor), completion(factor), factor)
        for factor in safe_factors
    ]
    rows = [
        row for row in rows if not row[0] & row[1]
    ]

    def contains_larger(selected: int) -> tuple[int, int] | None:
        item_ids = [
            position
            for position in range(len(eligible_edges))
            if selected & (1 << position)
        ]
        for size in sorted(size for size in one_terms if size >= 4):
            targets = one_terms[size]
            for subset in itertools.combinations(item_ids, size):
                target = sum(1 << item for item in subset)
                if target in targets:
                    return size, target
        return None

    orbit_rows = []
    pair_survivors = []
    for orbit_id, orbit in enumerate(census["factor_orbits"]):
        first = tuple(
            tuple(map(int, item)) for item in orbit["representative"]
        )
        first_edges = mask(first)
        first_completion = completion(first)
        compatible = 0
        larger_free = 0
        for second_edges, second_completion, second in rows:
            if first_edges & second_edges:
                continue
            if first_completion & second_edges:
                continue
            if second_completion & first_edges:
                continue
            compatible += 1
            witness = contains_larger(first_edges | second_edges)
            if witness is not None:
                continue
            larger_free += 1
            pair_survivors.append(
                {
                    "orbit_id": orbit_id,
                    "first": [list(item) for item in first],
                    "second": [list(item) for item in second],
                }
            )
        orbit_rows.append(
            {
                "orbit_id": orbit_id,
                "orbit_size": int(orbit["orbit_size"]),
                "size3_compatible_seconds": compatible,
                "larger_one_term_free_seconds": larger_free,
            }
        )
        print(
            f"orbit={orbit_id} seconds={compatible} "
            f"larger_free={larger_free}",
            flush=True,
        )

    payload = {
        "status": "larger_one_term_pair_filter_complete",
        "necessary_conditions_only": True,
        "partition": list(lengths),
        "safe_factors": len(safe_factors),
        "size3_free_factors": len(rows),
        "size3_compatible_seconds": sum(
            row["size3_compatible_seconds"] for row in orbit_rows
        ),
        "larger_one_term_free_seconds": len(pair_survivors),
        "orbit_rows": orbit_rows,
        "pair_survivors": pair_survivors,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key not in {"orbit_rows", "pair_survivors"}
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
