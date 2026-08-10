"""Test full-only cycle cancellations on a fixed order-14 equality support.

For a colouring that activates no singleton edge, the active perfect
matchings are exactly the Cartesian product of the two alternating
matchings on every even full-factor cycle.  Its forbidden amplitude
therefore factors as one nonzero-monomial binomial per cycle.  At least one
cycle binomial must vanish.

This script builds 3^7 guaranteed no-singleton colourings from one
singleton factor.  A Boolean variable says that one distinct local cycle
binomial has ratio -1.  Every colouring contributes a clause saying that
at least one of its cycle relations is selected.  Exact Smith-normal-form
checks reject selections whose signed Laurent relations contain an
integer dependency with odd coefficient sum.

UNSAT is a support-local obstruction.  SAT only means that this particular
full-only relation calculus did not close the support.
"""

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
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

from pysat.solvers import Solver
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
SparseVector = tuple[tuple[int, int], ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def cycle_edges(cycle: Sequence[int]) -> tuple[Edge, ...]:
    return tuple(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def contiguous_cycles(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + int(length))))
        start += int(length)
    if start != N:
        raise ValueError("partition does not sum to 14")
    return tuple(output)


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*item) for item in raw))


def proper_two_colourings(
    factors: Sequence[Factor], colour_pair: tuple[int, int]
) -> tuple[tuple[int, ...], ...]:
    adjacency = {vertex: set() for vertex in range(N)}
    for factor in factors:
        for first, second in factor:
            adjacency[first].add(second)
            adjacency[second].add(first)
    sides = [-1] * N
    components: list[list[int]] = []
    for start in range(N):
        if sides[start] >= 0:
            continue
        sides[start] = 0
        stack = [start]
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for other in adjacency[current]:
                expected = 1 - sides[current]
                if sides[other] < 0:
                    sides[other] = expected
                    stack.append(other)
                elif sides[other] != expected:
                    raise AssertionError(
                        "two singleton factors are not bipartite"
                    )
        components.append(component)

    output = []
    for flips in itertools.product(range(2), repeat=len(components)):
        colours = [-1] * N
        for component_id, component in enumerate(components):
            flip = flips[component_id]
            for vertex in component:
                colours[vertex] = colour_pair[sides[vertex] ^ flip]
        output.append(tuple(colours))
    return tuple(output)


def active_singletons(
    colouring: Sequence[int], factors: Sequence[Factor]
) -> set[Edge]:
    return {
        item
        for colour, factor in enumerate(factors)
        for item in factor
        if colouring[item[0]] == colouring[item[1]] == colour
    }


def relation_vector(
    cycle: Sequence[int], colouring: Sequence[int]
) -> SparseVector:
    edges = cycle_edges(cycle)
    alternating = (edges[0::2], edges[1::2])

    def monomial(matching: Sequence[Edge]) -> Counter[int]:
        output: Counter[int] = Counter()
        for item in matching:
            first, second = item
            local_edge = edges.index(item)
            variable = (
                9 * local_edge
                + 3 * int(colouring[first])
                + int(colouring[second])
            )
            output[variable] += 1
        return output

    difference = monomial(alternating[0])
    difference.subtract(monomial(alternating[1]))
    direct = tuple(
        sorted(
            (int(variable), int(coefficient))
            for variable, coefficient in difference.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient) for variable, coefficient in direct
    )
    return min(direct, negative)


def dense(vector: SparseVector, width: int) -> list[int]:
    output = [0] * width
    for variable, coefficient in vector:
        output[variable] = coefficient
    return output


def odd_kernel_conflict(
    relation_ids: Sequence[int],
    relation_vectors: Sequence[SparseVector],
    width: int,
) -> dict[str, object] | None:
    """Return one exact odd signed dependency among selected rows."""

    if not relation_ids:
        return None
    rows = [
        dense(relation_vectors[relation_id], width)
        for relation_id in relation_ids
    ]
    # Columns of V beyond rank form a Z-basis for ker(A), where
    # S = U*A*V and A is the transpose of the selected relation matrix.
    transposed = [list(column) for column in zip(*rows, strict=True)]
    matrix = DomainMatrix.from_list_sympy(
        width, len(rows), transposed
    ).convert_to(ZZ)
    smith, _left, right = smith_normal_decomp(matrix)
    smith_matrix = smith.to_Matrix()
    rank = sum(
        smith_matrix[index, index] != 0
        for index in range(min(smith.shape))
    )
    right_matrix = right.to_Matrix()
    for column in range(rank, len(rows)):
        coefficients = [
            int(right_matrix[row, column])
            for row in range(len(rows))
        ]
        if sum(coefficients) % 2 == 0:
            continue
        support = [
            int(relation_ids[index])
            for index, coefficient in enumerate(coefficients)
            if coefficient
        ]
        if not support:
            raise AssertionError("odd kernel vector has empty support")
        # Replay the exact dependency before returning it.
        reconstructed = [0] * width
        for coefficient, row in zip(coefficients, rows, strict=True):
            for position, value in enumerate(row):
                reconstructed[position] += coefficient * value
        if any(reconstructed):
            raise AssertionError("Smith kernel vector did not replay")
        return {
            "selected_relation_ids": list(map(int, relation_ids)),
            "dependency_coefficients": coefficients,
            "conflict_relation_ids": support,
            "coefficient_sum": int(sum(coefficients)),
        }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--max-rounds", type=int, default=1000)
    parser.add_argument(
        "--anchor-role",
        type=int,
        action="append",
        choices=(0, 1, 2),
        help="singleton colour used for the 3-state cube; defaults to all",
    )
    parser.add_argument(
        "--cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_full_only_cycle_cover_cegar.cnf"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_full_only_cycle_cover_cegar.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    source = json.loads(args.samples.read_text(encoding="utf-8"))
    lengths = tuple(map(int, source["partition"]))
    if (
        sum(lengths) != N
        or not lengths
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("full factor is not an all-even order-14 type")
    survivors = source["survivors"]
    if not 0 <= args.survivor_index < len(survivors):
        raise IndexError("survivor index out of range")
    survivor = survivors[args.survivor_index]
    factors = tuple(
        parse_factor(survivor[key])
        for key in ("first", "second", "third")
    )
    if any(len(factor) != N // 2 for factor in factors):
        raise AssertionError("singleton factor is not perfect")
    if len(set().union(*map(set, factors))) != 3 * (N // 2):
        raise AssertionError("singleton factors are not edge-disjoint")

    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    if set().union(*map(set, factors)) & full_edges:
        raise AssertionError("singleton factor meets the full factor")

    relation_maps: list[dict[SparseVector, int]] = [
        {} for _cycle in cycles
    ]
    relation_vectors_by_cycle: list[list[SparseVector]] = [
        [] for _cycle in cycles
    ]
    relation_origins: list[list[dict[str, object]]] = [
        [] for _cycle in cycles
    ]
    clause_keys: set[tuple[tuple[int, int], ...]] = set()
    anchor_roles = sorted(set(args.anchor_role or (0, 1, 2)))
    base_records = []
    cube_colourings = 0

    for anchor_role in anchor_roles:
        other_roles = tuple(
            role for role in range(3) if role != anchor_role
        )
        bases = proper_two_colourings(
            [factors[role] for role in other_roles],
            other_roles,
        )
        for base_id, base in enumerate(bases):
            base_records.append(
                {
                    "anchor_role": anchor_role,
                    "base_id": base_id,
                    "base_colouring": list(base),
                }
            )
            for state in itertools.product(range(3), repeat=N // 2):
                cube_colourings += 1
                colouring = list(base)
                for choice, item in zip(
                    state, factors[anchor_role], strict=True
                ):
                    if choice:
                        colouring[item[choice - 1]] = anchor_role
                colouring_tuple = tuple(colouring)
                if active_singletons(colouring_tuple, factors):
                    raise AssertionError(
                        "constructed cube colouring activates a singleton"
                    )
                local_keys = []
                for cycle_id, cycle in enumerate(cycles):
                    vector = relation_vector(cycle, colouring_tuple)
                    relation_map = relation_maps[cycle_id]
                    if vector not in relation_map:
                        relation_map[vector] = len(
                            relation_vectors_by_cycle[cycle_id]
                        )
                        relation_vectors_by_cycle[cycle_id].append(vector)
                        relation_origins[cycle_id].append(
                            {
                                "anchor_role": anchor_role,
                                "base_id": base_id,
                                "local_colouring": [
                                    int(colouring_tuple[vertex])
                                    for vertex in cycle
                                ],
                                "example_state": list(map(int, state)),
                            }
                        )
                    local_keys.append(
                        (cycle_id, relation_map[vector])
                    )
                clause_keys.add(tuple(local_keys))

    offsets = []
    next_variable = 1
    for vectors in relation_vectors_by_cycle:
        offsets.append(next_variable)
        next_variable += len(vectors)
    clauses = [
        tuple(
            offsets[cycle_id] + relation_id
            for cycle_id, relation_id in clause
        )
        for clause in sorted(clause_keys)
    ]
    conflicts = []
    status = "round_limit"
    final_selected: list[list[int]] | None = None

    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        solver.set_phases(
            [-variable for variable in range(1, next_variable)]
        )
        for round_id in range(args.max_rounds):
            if not solver.solve():
                status = "UNSAT"
                break
            model = solver.get_model()
            if model is None:
                raise AssertionError("SAT solver returned no model")
            positive = {literal for literal in model if literal > 0}
            selected_by_cycle = [
                [
                    relation_id
                    for relation_id in range(len(vectors))
                    if offsets[cycle_id] + relation_id in positive
                ]
                for cycle_id, vectors in enumerate(
                    relation_vectors_by_cycle
                )
            ]
            conflict = None
            for cycle_id, selected in enumerate(selected_by_cycle):
                conflict = odd_kernel_conflict(
                    selected,
                    relation_vectors_by_cycle[cycle_id],
                    9 * lengths[cycle_id],
                )
                if conflict is None:
                    continue
                conflict["cycle_id"] = cycle_id
                blocking = [
                    -(offsets[cycle_id] + relation_id)
                    for relation_id in conflict["conflict_relation_ids"]
                ]
                solver.add_clause(blocking)
                clauses.append(tuple(blocking))
                conflict["blocking_clause"] = blocking
                conflict["round"] = round_id
                conflicts.append(conflict)
                break
            if conflict is None:
                status = "SAT"
                final_selected = selected_by_cycle
                break

    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.cnf.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {next_variable - 1} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")

    payload = {
        "status": status,
        "scope": (
            "full-only factorized amplitudes on the 3^7 no-singleton "
            "colouring cube of one fixed equality support"
        ),
        "samples": str(args.samples),
        "samples_sha256": sha256(args.samples),
        "survivor_index": args.survivor_index,
        "partition": list(lengths),
        "singleton_factors": [
            [list(item) for item in factor] for factor in factors
        ],
        "anchor_roles": anchor_roles,
        "base_colourings": base_records,
        "cube_instances": len(base_records),
        "cube_colourings": cube_colourings,
        "distinct_cover_clauses": len(clause_keys),
        "relation_counts_by_cycle": [
            len(vectors) for vectors in relation_vectors_by_cycle
        ],
        "relation_vectors_by_cycle": [
            [
                [list(item) for item in vector]
                for vector in vectors
            ]
            for vectors in relation_vectors_by_cycle
        ],
        "relation_origins_by_cycle": relation_origins,
        "variable_offsets": offsets,
        "lattice_conflicts": conflicts,
        "lattice_conflict_count": len(conflicts),
        "final_selected_relation_ids_by_cycle": final_selected,
        "cnf": str(args.cnf),
        "cnf_sha256": sha256(args.cnf),
        "cnf_variables": next_variable - 1,
        "cnf_clauses": len(clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": True,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
