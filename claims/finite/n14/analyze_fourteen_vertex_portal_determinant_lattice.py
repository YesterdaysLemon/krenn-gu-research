"""Scout exact signed dependencies among adjacent-port determinant identities.

This is deliberately support-local.  It extracts one SAT singleton-factor
triple from a selected orbit of an audited order-14 rule CNF, enumerates all
positive-minimal adjacent-port circuits, instantiates every proper colouring
of the other two factors, and tests the resulting signed Laurent relations
for an exact odd integer dependency.

UNSAT-by-lattice is a rigorous obstruction for the extracted support.  A
null result means only that this determinant-relation layer did not close
that support.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_full_only_cycle_cover_cegar import (
    odd_kernel_conflict,
)


N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
SymbolicVector = tuple[tuple[str, int], ...]
SparseVector = tuple[tuple[int, int], ...]


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def contiguous_cycles(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    cycles = []
    start = 0
    for raw_length in lengths:
        length = int(raw_length)
        cycles.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise ValueError("partition does not sum to 14")
    return tuple(cycles)


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def local_feasible_mask(cycle: Sequence[int], deleted: set[int]) -> bool:
    positions = [
        index for index, vertex in enumerate(cycle) if vertex in deleted
    ]
    if not positions:
        return True
    return all(
        (
            positions[(index + 1) % len(positions)] - positions[index]
        )
        % len(cycle)
        % 2
        for index in range(len(positions))
    )


def portal_subsets(
    factor: Factor, cycles: Sequence[Sequence[int]]
) -> tuple[tuple[Edge, ...], ...]:
    """Return all proper positive-minimal adjacent-port subsets."""

    minimal_feasible: list[int] = []
    portals: list[tuple[Edge, ...]] = []
    full = (1 << len(factor)) - 1
    for subset in range(1, 1 << len(factor)):
        endpoints = {
            vertex
            for index, item in enumerate(factor)
            if subset & (1 << index)
            for vertex in item
        }
        if not all(
            local_feasible_mask(cycle, endpoints) for cycle in cycles
        ):
            continue
        if any(
            previous & subset == previous
            for previous in minimal_feasible
        ):
            continue
        minimal_feasible.append(subset)
        if subset == full:
            continue
        local_deleted = [
            tuple(vertex for vertex in cycle if vertex in endpoints)
            for cycle in cycles
        ]
        if any(not deleted for deleted in local_deleted):
            continue
        if not all(
            len(deleted) == 2
            and edge(*deleted) in cycle_edges(cycle)
            for cycle, deleted in zip(
                cycles, local_deleted, strict=True
            )
        ):
            continue
        portals.append(
            tuple(
                factor[index]
                for index in range(len(factor))
                if subset & (1 << index)
            )
        )
    return tuple(portals)


def contracted_connected_port_cycle(
    chosen: tuple[Edge, ...],
    cycles: Sequence[Sequence[int]],
    touched: Sequence[int],
) -> bool:
    """Check the loopless connected 2-regular contraction criterion."""

    if not touched:
        return False
    component_of = {
        vertex: cycle_id
        for cycle_id, cycle in enumerate(cycles)
        for vertex in cycle
    }
    touched_set = set(map(int, touched))
    degrees = {cycle_id: 0 for cycle_id in touched_set}
    adjacency = {cycle_id: set() for cycle_id in touched_set}
    for first, second in chosen:
        left = component_of[first]
        right = component_of[second]
        if left not in touched_set or right not in touched_set:
            raise AssertionError("chosen edge left its touched components")
        if left == right:
            return False
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    if any(degree != 2 for degree in degrees.values()):
        return False
    seen = set()
    stack = [next(iter(touched_set))]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(adjacency[current] - seen)
    return seen == touched_set


def proper_colourings(
    first: Factor,
    second: Factor,
    first_colour: int,
    second_colour: int,
) -> tuple[tuple[int, ...], ...]:
    adjacency: dict[int, list[int]] = defaultdict(list)
    for item in (*first, *second):
        adjacency[item[0]].append(item[1])
        adjacency[item[1]].append(item[0])
    if set(adjacency) != set(range(N)):
        raise AssertionError("factor union stopped spanning")
    if any(len(neighbours) != 2 for neighbours in adjacency.values()):
        raise AssertionError("factor union stopped being 2-regular")

    sides = [-1] * N
    components: list[tuple[int, ...]] = []
    for root in range(N):
        if sides[root] >= 0:
            continue
        sides[root] = 0
        queue = deque([root])
        component = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbour in adjacency[vertex]:
                expected = 1 - sides[vertex]
                if sides[neighbour] < 0:
                    sides[neighbour] = expected
                    queue.append(neighbour)
                elif sides[neighbour] != expected:
                    raise AssertionError("factor union stopped bipartite")
        components.append(tuple(sorted(component)))

    output = []
    colours = (int(first_colour), int(second_colour))
    for flips in itertools.product((0, 1), repeat=len(components)):
        colouring = [-1] * N
        for component, flip in zip(components, flips, strict=True):
            for vertex in component:
                colouring[vertex] = colours[sides[vertex] ^ flip]
        output.append(tuple(colouring))
    return tuple(output)


def canonical_vector(coefficients: dict[str, int]) -> SymbolicVector:
    direct = tuple(
        sorted(
            (variable, int(coefficient))
            for variable, coefficient in coefficients.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient) for variable, coefficient in direct
    )
    return min(direct, negative)


def determinant_relations(
    factors: Sequence[Factor],
    cycles: Sequence[Sequence[int]],
) -> tuple[list[SymbolicVector], list[dict[str, object]]]:
    relation_ids: dict[SymbolicVector, int] = {}
    relations: list[SymbolicVector] = []
    origins: list[dict[str, object]] = []
    for colour in range(3):
        other = [item for item in range(3) if item != colour]
        bases = proper_colourings(
            factors[other[0]],
            factors[other[1]],
            other[0],
            other[1],
        )
        for portal in portal_subsets(factors[colour], cycles):
            endpoints = {
                vertex for item in portal for vertex in item
            }
            port_edges = []
            for cycle in cycles:
                deleted = [
                    vertex for vertex in cycle if vertex in endpoints
                ]
                if len(deleted) != 2:
                    raise AssertionError("portal stopped touching twice")
                port_edge = edge(*deleted)
                if port_edge not in cycle_edges(cycle):
                    raise AssertionError("portal endpoints stopped adjacent")
                port_edges.append(port_edge)
            for base_id, base in enumerate(bases):
                coefficients: dict[str, int] = defaultdict(int)
                for first, second in port_edges:
                    coefficients[
                        (
                            f"D:{first}-{second}:c{colour}:"
                            f"a{base[first]}:b{base[second]}"
                        )
                    ] += 1
                for first, second in portal:
                    coefficients[
                        f"S:{first}-{second}:c{colour}"
                    ] -= 1
                vector = canonical_vector(coefficients)
                record = {
                    "colour": colour,
                    "portal_edges": [list(item) for item in portal],
                    "port_full_edges": [
                        list(item) for item in port_edges
                    ],
                    "base_colouring_id": base_id,
                    "base_colouring": list(base),
                }
                if vector in relation_ids:
                    origins[relation_ids[vector]][
                        "duplicate_origins"
                    ].append(record)
                    continue
                relation_ids[vector] = len(relations)
                relations.append(vector)
                origins.append(
                    {
                        **record,
                        "duplicate_origins": [],
                    }
                )
    return relations, origins


def extract_factors(
    model: Sequence[int],
    cycles: Sequence[Sequence[int]],
) -> tuple[Factor, Factor, Factor]:
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible = tuple(
        sorted(
            set(itertools.combinations(range(N), 2)) - full_edges
        )
    )
    if len(eligible) != 77:
        raise AssertionError("eligible edge count changed")
    positive = {int(literal) for literal in model if literal > 0}
    factors = []
    for colour in range(3):
        factor = tuple(
            eligible[index]
            for index in range(len(eligible))
            if colour * len(eligible) + index + 1 in positive
        )
        if len(factor) != 7:
            raise AssertionError("model role stopped being a factor")
        if len({vertex for item in factor for vertex in item}) != N:
            raise AssertionError("model role stopped being a matching")
        factors.append(factor)
    if any(
        set(factors[left]) & set(factors[right])
        for left, right in itertools.combinations(range(3), 2)
    ):
        raise AssertionError("model factors stopped being edge-disjoint")
    return tuple(factors)  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    partition = tuple(map(int, args.partition.split(",")))
    cycles = contiguous_cycles(partition)
    formula = CNF(from_file=str(args.cnf))
    selector = 232 + args.orbit
    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        sat = solver.solve(assumptions=[selector])
        model = solver.get_model() if sat else None
    if not sat or model is None:
        raise ValueError("requested selector is UNSAT in the input CNF")
    factors = extract_factors(model, cycles)
    portals = [portal_subsets(factor, cycles) for factor in factors]
    symbolic_relations, origins = determinant_relations(factors, cycles)
    variables = sorted(
        {
            variable
            for relation in symbolic_relations
            for variable, _coefficient in relation
        }
    )
    positions = {
        variable: index for index, variable in enumerate(variables)
    }
    relations: list[SparseVector] = [
        tuple(
            (positions[variable], coefficient)
            for variable, coefficient in relation
        )
        for relation in symbolic_relations
    ]
    conflict = odd_kernel_conflict(
        list(range(len(relations))),
        relations,
        len(variables),
    )
    payload = {
        "status": (
            "odd_portal_determinant_dependency"
            if conflict is not None
            else "no_odd_portal_determinant_dependency"
        ),
        "scope": (
            "one SAT singleton-factor support under one order-14 "
            "selector orbit"
        ),
        "cnf": str(args.cnf),
        "partition": list(partition),
        "orbit": args.orbit,
        "selector": selector,
        "singleton_factors": [
            [list(item) for item in factor] for factor in factors
        ],
        "portal_counts_by_colour": [len(items) for items in portals],
        "portal_subsets_by_colour": [
            [[list(item) for item in portal] for portal in items]
            for items in portals
        ],
        "distinct_relations": len(relations),
        "relation_variables": len(variables),
        "relation_vectors": [
            [[variable, coefficient] for variable, coefficient in relation]
            for relation in symbolic_relations
        ],
        "relation_origins": origins,
        "conflict": conflict,
        "support_closed": conflict is not None,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key
                not in {
                    "singleton_factors",
                    "portal_subsets_by_colour",
                    "relation_vectors",
                    "relation_origins",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
