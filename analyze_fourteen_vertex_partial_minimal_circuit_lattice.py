"""Scout mandatory Laurent relations from partial minimal circuits."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_full_only_cycle_cover_cegar import (
    odd_kernel_conflict,
)
from analyze_fourteen_vertex_portal_determinant_lattice import (
    Edge,
    Factor,
    canonical_vector,
    contiguous_cycles,
    contracted_connected_port_cycle,
    cycle_edges,
    edge,
    extract_factors,
    local_feasible_mask,
    proper_colourings,
)


SymbolicVector = tuple[tuple[str, int], ...]
SparseVector = tuple[tuple[int, int], ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def minimal_feasible_subsets(
    factor: Factor, cycles: Sequence[Sequence[int]]
) -> tuple[tuple[Edge, ...], ...]:
    output = []
    minimal = []
    for mask in range(1, (1 << len(factor)) - 1):
        endpoints = {
            vertex
            for index, item in enumerate(factor)
            if mask & (1 << index)
            for vertex in item
        }
        if not all(
            local_feasible_mask(cycle, endpoints) for cycle in cycles
        ):
            continue
        if any(previous & mask == previous for previous in minimal):
            continue
        minimal.append(mask)
        output.append(
            tuple(
                factor[index]
                for index in range(len(factor))
                if mask & (1 << index)
            )
        )
    return tuple(output)


def is_port_exception(
    chosen: tuple[Edge, ...],
    cycles: Sequence[Sequence[int]],
    touched: tuple[int, ...],
) -> bool:
    endpoints = {vertex for item in chosen for vertex in item}
    for cycle_id in touched:
        deleted = tuple(
            vertex for vertex in cycles[cycle_id] if vertex in endpoints
        )
        if (
            len(deleted) != 2
            or edge(*deleted) not in cycle_edges(cycles[cycle_id])
        ):
            return False
    return contracted_connected_port_cycle(chosen, cycles, touched)


def full_cycle_relation(
    cycle: Sequence[int], colouring: Sequence[int]
) -> SymbolicVector:
    edges = tuple(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )
    coefficients: Counter[str] = Counter()
    for sign, matching in (
        (1, edges[0::2]),
        (-1, edges[1::2]),
    ):
        for first, second in matching:
            coefficients[
                (
                    f"W:{first}-{second}:"
                    f"a{colouring[first]}:b{colouring[second]}"
                )
            ] += sign
    return canonical_vector(dict(coefficients))


def forced_relations(
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
        for chosen in minimal_feasible_subsets(
            factors[colour], cycles
        ):
            endpoints = {vertex for item in chosen for vertex in item}
            touched = tuple(
                cycle_id
                for cycle_id, cycle in enumerate(cycles)
                if set(cycle) & endpoints
            )
            untouched = tuple(
                cycle_id
                for cycle_id in range(len(cycles))
                if cycle_id not in touched
            )
            if len(untouched) != 1:
                continue
            if is_port_exception(chosen, cycles, touched):
                continue
            forced_cycle = untouched[0]
            for base_id, base in enumerate(bases):
                target = list(base)
                for vertex in endpoints:
                    target[vertex] = colour
                vector = full_cycle_relation(
                    cycles[forced_cycle], target
                )
                record = {
                    "colour": colour,
                    "minimal_subset": [list(item) for item in chosen],
                    "touched_cycles": list(touched),
                    "forced_cycle": forced_cycle,
                    "base_colouring_id": base_id,
                    "base_colouring": list(base),
                    "target_colouring": target,
                }
                if vector in relation_ids:
                    origins[relation_ids[vector]][
                        "duplicate_origins"
                    ].append(record)
                    continue
                relation_ids[vector] = len(relations)
                relations.append(vector)
                origins.append({**record, "duplicate_origins": []})
    return relations, origins


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument(
        "--model-json",
        type=Path,
        help=(
            "optional SAT-model record produced by an incremental "
            "orchestrator; skips reparsing and resolving the CNF"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    partition = tuple(map(int, args.partition.split(",")))
    cycles = contiguous_cycles(partition)
    selector = 232 + args.orbit
    model_source = "fresh_cnf_solve"
    model_record_sha256 = None
    if args.model_json is None:
        formula = CNF(from_file=str(args.cnf))
        with Solver(
            name="cadical195", bootstrap_with=formula.clauses
        ) as solver:
            sat = solver.solve(assumptions=[selector])
            model = solver.get_model() if sat else None
    else:
        if not args.model_json.is_file():
            raise FileNotFoundError(args.model_json)
        model_payload = json.loads(
            args.model_json.read_text(encoding="utf-8")
        )
        if model_payload.get("status") != "incremental_sat_model":
            raise ValueError("unrecognized incremental SAT-model record")
        if int(model_payload.get("selector", 0)) != selector:
            raise ValueError("SAT-model selector does not match the orbit")
        if str(model_payload.get("cnf")) != str(args.cnf):
            raise ValueError("SAT-model CNF does not match --cnf")
        if str(model_payload.get("cnf_sha256")) != sha256(args.cnf):
            raise ValueError("SAT-model CNF hash does not match --cnf")
        model = list(map(int, model_payload["model"]))
        sat = selector in {literal for literal in model if literal > 0}
        model_source = "incremental_solver_record"
        model_record_sha256 = sha256(args.model_json)
    if not sat or model is None:
        raise ValueError("requested selector is UNSAT in the input CNF")
    factors = extract_factors(model, cycles)
    symbolic, origins = forced_relations(factors, cycles)
    variables = sorted(
        {
            variable
            for relation in symbolic
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
        for relation in symbolic
    ]
    conflict = odd_kernel_conflict(
        list(range(len(relations))),
        relations,
        len(variables),
    )
    minimal_counts = [
        len(minimal_feasible_subsets(factor, cycles))
        for factor in factors
    ]
    payload = {
        "status": (
            "odd_partial_circuit_relation_dependency"
            if conflict is not None
            else "no_odd_partial_circuit_relation_dependency"
        ),
        "scope": (
            "one SAT singleton-factor support under one order-14 "
            "selector orbit"
        ),
        "cnf": str(args.cnf),
        "partition": list(partition),
        "orbit": args.orbit,
        "selector": selector,
        "model_source": model_source,
        "model_record": (
            str(args.model_json) if args.model_json is not None else None
        ),
        "model_record_sha256": model_record_sha256,
        "singleton_factors": [
            [list(item) for item in factor] for factor in factors
        ],
        "proper_minimal_subset_counts": minimal_counts,
        "distinct_forced_relations": len(relations),
        "relation_variables": len(variables),
        "relation_vectors": [
            [[variable, coefficient] for variable, coefficient in relation]
            for relation in symbolic
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
                    "relation_vectors",
                    "relation_origins",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
