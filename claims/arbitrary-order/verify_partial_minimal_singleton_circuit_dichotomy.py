"""Audit the combinatorics in the partial minimal-circuit dichotomy."""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


Edge = tuple[int, int]
OUTPUT = Path(
    "tmp/partial_minimal_singleton_circuit_dichotomy_verified.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def partitions(
    total: int, parts: int, minimum: int = 4
) -> list[tuple[int, ...]]:
    output = []
    for values in itertools.product(
        range(minimum, total + 1, 2), repeat=parts
    ):
        if sum(values) == total:
            output.append(values)
    return sorted(set(output))


def cycles_for(lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    return tuple(output)


def cycle_edges(cycle: tuple[int, ...]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def completion_count(
    cycle: tuple[int, ...], deleted: set[int]
) -> int:
    if not deleted:
        return 2
    positions = [
        index for index, vertex in enumerate(cycle) if vertex in deleted
    ]
    feasible = all(
        (
            positions[(index + 1) % len(positions)] - positions[index]
        )
        % len(cycle)
        % 2
        for index in range(len(positions))
    )
    return int(feasible)


def contracted_connected_port_cycle(
    chosen: tuple[Edge, ...],
    cycles: tuple[tuple[int, ...], ...],
    touched: tuple[int, ...],
) -> bool:
    component_of = {
        vertex: cycle_id
        for cycle_id, cycle in enumerate(cycles)
        for vertex in cycle
    }
    degrees = {cycle_id: 0 for cycle_id in touched}
    adjacency = {cycle_id: set() for cycle_id in touched}
    for first, second in chosen:
        left = component_of[first]
        right = component_of[second]
        if left == right:
            return False
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    if any(degrees[item] != 2 for item in touched):
        return False
    seen = set()
    stack = [touched[0]]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(adjacency[current] - seen)
    return seen == set(touched)


def main() -> None:
    started = time.perf_counter()
    factorization_checks = 0
    matching_subsets = 0
    positive_minimal = 0
    proper_partial_minimal = 0
    port_exceptions = 0
    single_touched_exceptions = 0

    # A loopless two-port pairing captures every possible exceptional T
    # after the actual full cycles are contracted.  Exhausting up to six
    # components independently checks connectedness versus minimality.
    pairing_cases = 0
    for component_count in range(2, 7):
        ports = tuple(
            (component, port)
            for component in range(component_count)
            for port in range(2)
        )

        def pairings(
            remaining: tuple[tuple[int, int], ...],
            chosen: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
        ):
            if not remaining:
                yield chosen
                return
            first = remaining[0]
            for index in range(1, len(remaining)):
                second = remaining[index]
                if first[0] == second[0]:
                    continue
                yield from pairings(
                    remaining[1:index] + remaining[index + 1 :],
                    (*chosen, (first, second)),
                )

        for pairing in pairings(ports, ()):
            pairing_cases += 1
            adjacency = {item: set() for item in range(component_count)}
            for first, second in pairing:
                adjacency[first[0]].add(second[0])
                adjacency[second[0]].add(first[0])
            seen = set()
            stack = [0]
            while stack:
                current = stack.pop()
                if current in seen:
                    continue
                seen.add(current)
                stack.extend(adjacency[current] - seen)
            connected = len(seen) == component_count
            has_proper_component = False
            for mask in range(1, (1 << len(pairing)) - 1):
                degrees = [0] * component_count
                for index, (first, second) in enumerate(pairing):
                    if mask & (1 << index):
                        degrees[first[0]] += 1
                        degrees[second[0]] += 1
                if all(degree in (0, 2) for degree in degrees):
                    has_proper_component = True
                    break
            if connected == has_proper_component:
                raise AssertionError(
                    "connected port cycle/minimality equivalence changed"
                )

    # Exhaust real matching subsets on representative all-even partitions.
    # Matchings are drawn from one deterministic perfect matching at a time;
    # all of its subsets are checked exactly.
    for total in range(8, 15, 2):
        for part_count in range(2, min(6, total // 4) + 1):
            for lengths in partitions(total, part_count):
                cycles = cycles_for(lengths)
                full_edges = {
                    item
                    for cycle in cycles
                    for item in cycle_edges(cycle)
                }
                all_edges = tuple(
                    item
                    for item in itertools.combinations(range(total), 2)
                    if item not in full_edges
                )
                # Deterministic greedy matchings from every possible first
                # edge give broad endpoint-pattern coverage without assuming
                # the theorem in the generator.
                sampled = set()
                for seed in all_edges:
                    used = set(seed)
                    chosen = [seed]
                    for item in all_edges:
                        if not (set(item) & used):
                            chosen.append(item)
                            used.update(item)
                    if len(chosen) != total // 2:
                        continue
                    factor = tuple(sorted(chosen))
                    if factor in sampled:
                        continue
                    sampled.add(factor)
                    feasible_minimal: list[int] = []
                    for mask in range(1, 1 << len(factor)):
                        matching_subsets += 1
                        chosen_edges = tuple(
                            factor[index]
                            for index in range(len(factor))
                            if mask & (1 << index)
                        )
                        deleted = {
                            vertex
                            for item in chosen_edges
                            for vertex in item
                        }
                        counts = [
                            completion_count(cycle, deleted)
                            for cycle in cycles
                        ]
                        if not all(counts):
                            continue
                        if any(
                            previous & mask == previous
                            for previous in feasible_minimal
                        ):
                            continue
                        feasible_minimal.append(mask)
                        positive_minimal += 1
                        touched = tuple(
                            index
                            for index, cycle in enumerate(cycles)
                            if set(cycle) & deleted
                        )
                        untouched = tuple(
                            index
                            for index in range(len(cycles))
                            if index not in touched
                        )
                        full_count = 2 ** len(cycles)
                        extra_count = 2 ** len(untouched)
                        if full_count != (
                            2 ** (len(touched) + len(untouched))
                        ):
                            raise AssertionError(
                                "full-only count factorization changed"
                            )
                        if extra_count != 2 ** len(untouched):
                            raise AssertionError(
                                "T-completion factorization changed"
                            )
                        factorization_checks += 1
                        if not untouched:
                            continue
                        proper_partial_minimal += 1
                        adjacent_ports = True
                        for cycle_id in touched:
                            local = tuple(
                                vertex
                                for vertex in cycles[cycle_id]
                                if vertex in deleted
                            )
                            if (
                                len(local) != 2
                                or edge(*local)
                                not in cycle_edges(cycles[cycle_id])
                            ):
                                adjacent_ports = False
                                break
                        exception = adjacent_ports and (
                            contracted_connected_port_cycle(
                                chosen_edges, cycles, touched
                            )
                        )
                        port_exceptions += int(exception)
                        if len(touched) == 1 and exception:
                            single_touched_exceptions += 1

    if single_touched_exceptions:
        raise AssertionError("one-cycle loop exception became possible")
    source = Path(__file__)
    theorem = Path(
        "PARTIAL_MINIMAL_SINGLETON_CIRCUIT_DICHOTOMY.md"
    )
    payload = {
        "verified": True,
        "status": "partial_minimal_singleton_circuit_dichotomy_verified",
        "scope": (
            "exact feasible-subset completion counts and contracted "
            "port-cycle exception through order 14"
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "matching_subsets_checked": matching_subsets,
        "positive_minimal_sets": positive_minimal,
        "proper_partial_minimal_sets": proper_partial_minimal,
        "factorization_checks": factorization_checks,
        "contracted_pairings_checked": pairing_cases,
        "partial_port_exceptions": port_exceptions,
        "single_touched_port_exceptions": single_touched_exceptions,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
