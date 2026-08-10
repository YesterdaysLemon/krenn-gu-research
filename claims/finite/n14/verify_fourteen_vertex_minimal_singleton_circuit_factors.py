"""Independently replay a singleton-circuit factor census."""

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
import hashlib
import json
import time
from functools import lru_cache
from pathlib import Path


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def enumerate_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for suffix in enumerate_matchings(remaining):
            yield (edge(first, second), *suffix)


def factor_digest(factors) -> str:
    digest = hashlib.sha256()
    for factor in factors:
        digest.update(
            (";".join(f"{a}-{b}" for a, b in factor) + "\n").encode()
        )
    return digest.hexdigest()


def cycle_completion_table(cycle):
    length = len(cycle)
    cycle_edge_set = {
        edge(cycle[index], cycle[(index + 1) % length])
        for index in range(length)
    }

    @lru_cache(maxsize=None)
    def count(remaining: frozenset[int]) -> int:
        if not remaining:
            return 1
        first = min(remaining)
        total = 0
        for second in remaining:
            if second != first and edge(first, second) in cycle_edge_set:
                total += count(remaining - {first, second})
        return total

    table = {}
    for deleted_mask in range(1 << length):
        remaining = frozenset(
            vertex
            for position, vertex in enumerate(cycle)
            if not (deleted_mask & (1 << position))
        )
        table[deleted_mask] = count(remaining)
    return table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    stored = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, stored["partition"]))
    cycles = []
    start = 0
    for length in lengths:
        cycles.append(tuple(range(start, start + length)))
        start += length
    full_edges = {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for cycle in cycles
        for index in range(len(cycle))
    }
    if [list(item) for item in sorted(full_edges)] != stored["full_edges"]:
        raise AssertionError("stored full edges changed")

    all_matchings = list(enumerate_matchings(tuple(range(14))))
    factors = [
        factor
        for factor in all_matchings
        if not (set(factor) & full_edges)
    ]
    if len(all_matchings) != int(stored["all_k14_perfect_matchings"]):
        raise AssertionError("K14 perfect-matching count changed")
    if len(factors) != int(stored["eligible_singleton_factors"]):
        raise AssertionError("eligible factor count changed")
    if factor_digest(factors) != stored["eligible_factor_sha256"]:
        raise AssertionError("eligible factor enumeration changed")

    completion_tables = [
        cycle_completion_table(cycle) for cycle in cycles
    ]
    adjacent_masks = []
    for cycle in cycles:
        adjacent_masks.append(
            {
                (1 << index) | (1 << ((index + 1) % len(cycle)))
                for index in range(len(cycle))
            }
        )
    positions = [
        {vertex: index for index, vertex in enumerate(cycle)}
        for cycle in cycles
    ]

    reproduced = []
    safe_indices = []
    rectangle_sets = 0
    portal_sets = 0
    full_sets = 0
    factors_with_portals = 0
    for factor_index, factor in enumerate(factors):
        endpoint_masks = [
            (1 << first) | (1 << second) for first, second in factor
        ]
        global_deleted = [0] * 128
        minimal = []
        first_record = None
        factor_portals = 0
        for subset in range(1, 128):
            bit = subset & -subset
            edge_id = bit.bit_length() - 1
            global_deleted[subset] = (
                global_deleted[subset ^ bit] | endpoint_masks[edge_id]
            )
            local = []
            for position, table in zip(
                positions, completion_tables, strict=True
            ):
                mask = 0
                for vertex, local_id in position.items():
                    if global_deleted[subset] & (1 << vertex):
                        mask |= 1 << local_id
                if table[mask] == 0:
                    break
                local.append(mask)
            else:
                if any((old & subset) == old for old in minimal):
                    continue
                minimal.append(subset)
                if any(mask == 0 for mask in local):
                    continue
                if subset == 127:
                    full_sets += 1
                    continue
                exceptional = all(
                    mask.bit_count() == 2
                    and mask in adjacent
                    for mask, adjacent in zip(
                        local, adjacent_masks, strict=True
                    )
                )
                if exceptional:
                    portal_sets += 1
                    factor_portals += 1
                    continue
                rectangle_sets += 1
                if first_record is None:
                    witness_cycle = next(
                        index
                        for index, (mask, adjacent) in enumerate(
                            zip(local, adjacent_masks, strict=True)
                        )
                        if not (
                            mask.bit_count() == 2
                            and mask in adjacent
                        )
                    )
                    first_record = {
                        "factor_index": factor_index,
                        "subset_mask": subset,
                        "witness_cycle": witness_cycle,
                        "witness_deleted_mask": local[witness_cycle],
                    }
        factors_with_portals += bool(factor_portals)
        if first_record is None:
            safe_indices.append(factor_index)
        else:
            reproduced.append(first_record)

    if reproduced != stored["obstructed_factor_records"]:
        raise AssertionError("obstructed factor records changed")
    if safe_indices != stored["safe_factor_indices"]:
        raise AssertionError("safe factor index list changed")
    expected_counts = {
        "rectangle_obstructed_factors": len(reproduced),
        "rectangle_safe_factors": len(safe_indices),
        "factors_with_adjacent_port_circuits": factors_with_portals,
        "rectangle_minimal_sets": rectangle_sets,
        "adjacent_port_minimal_sets": portal_sets,
        "full_factor_minimal_sets_ignored": full_sets,
    }
    for key, value in expected_counts.items():
        if int(stored[key]) != value:
            raise AssertionError(f"{key} changed")

    payload = {
        "verified": True,
        "status": (
            "fourteen_vertex_minimal_singleton_circuit_factor_census_"
            "verified"
        ),
        "scope": (
            "independent K14 perfect-matching recursion, brute cycle "
            "completion tables, every factor subset, and exact catalogue"
        ),
        "census": str(args.census),
        "census_sha256": hashlib.sha256(
            args.census.read_bytes()
        ).hexdigest(),
        "partition": list(lengths),
        "eligible_singleton_factors": len(factors),
        **expected_counts,
        "elapsed_seconds": time.perf_counter() - started,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
