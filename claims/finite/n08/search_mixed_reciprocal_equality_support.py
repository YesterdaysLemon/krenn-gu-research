"""Search the 84-entry reciprocal-killer equality stratum.

Eight blocks are fixed full and the complementary cubic graph consists of
one-entry reciprocal killers.  A killer chosen at a vertex constrains the
colour at the *opposite* endpoint, so those three opposite-end colours must
be a permutation of the three killer colours.  This search deliberately
requires at least one bichromatic singleton and lazily adds exact
no-binomial activity constraints.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from augment_no_binomial_amplitudes import no_binomial_extension
from enumerate_double_c4_singleton_family import (
    activity_summary,
    write_model,
)
from search_witness import EquationSystem

Edge = tuple[int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def block_support(
    selected: set[int],
    system: EquationSystem,
) -> dict[Edge, set[int]]:
    output: dict[Edge, set[int]] = {}
    for edge in system.edges:
        base = system.d**2 * system.edge_index[edge]
        local = {
            flat - base
            for flat in selected
            if base <= flat < base + system.d**2
        }
        if local:
            output[edge] = local
    return output


class EqualitySearch:
    def __init__(
        self,
        system: EquationSystem,
        full_edges: frozenset[Edge],
    ) -> None:
        self.system = system
        self.full_edges = full_edges
        self.skeleton = frozenset(
            edge
            for edge in system.edges
            if edge in full_edges
        )
        self.singleton_edges: frozenset[Edge] = frozenset()
        self.top_id = 0
        self.incidence_variable: dict[tuple[int, Edge, int], int] = {}
        self.activity_variable: dict[tuple[int, int], int] = {}
        self.encoded_colourings: set[int] = set()

    def initialize(
        self,
        singleton_edges: frozenset[Edge],
    ) -> list[list[int]]:
        self.singleton_edges = singleton_edges
        self.skeleton = self.full_edges | singleton_edges
        clauses: list[list[int]] = []
        incident: dict[int, list[Edge]] = {
            vertex: sorted(
                edge
                for edge in singleton_edges
                if vertex in edge
            )
            for vertex in range(self.system.n)
        }
        if any(len(edges) != self.system.d for edges in incident.values()):
            raise ValueError("singleton graph is not cubic")

        for vertex in range(self.system.n):
            for edge in incident[vertex]:
                for colour in range(self.system.d):
                    self.top_id += 1
                    self.incidence_variable[
                        (vertex, edge, colour)
                    ] = self.top_id

        for vertex in range(self.system.n):
            for edge in incident[vertex]:
                variables = [
                    self.incidence_variable[(vertex, edge, colour)]
                    for colour in range(self.system.d)
                ]
                clauses.append(variables)
                clauses.extend(
                    [-first, -second]
                    for index, first in enumerate(variables)
                    for second in variables[index + 1 :]
                )
            for colour in range(self.system.d):
                variables = [
                    self.incidence_variable[
                        (
                            (
                                edge[1]
                                if vertex == edge[0]
                                else edge[0]
                            ),
                            edge,
                            colour,
                        )
                    ]
                    for edge in incident[vertex]
                ]
                clauses.append(variables)
                clauses.extend(
                    [-first, -second]
                    for index, first in enumerate(variables)
                    for second in variables[index + 1 :]
                )

        # Remove the global colour action.
        for colour, edge in enumerate(incident[0]):
            opposite = edge[1] if edge[0] == 0 else edge[0]
            clauses.append(
                [
                    self.incidence_variable[
                        (opposite, edge, colour)
                    ]
                ]
            )

        # Require at least one singleton edge whose endpoint colours differ.
        same_variables: list[int] = []
        same_by_edge: dict[Edge, int] = {}
        for edge in sorted(singleton_edges):
            first, second = edge
            equal_colour_variables: list[int] = []
            for colour in range(self.system.d):
                self.top_id += 1
                both = self.top_id
                equal_colour_variables.append(both)
                left = self.incidence_variable[(first, edge, colour)]
                right = self.incidence_variable[(second, edge, colour)]
                clauses.extend(
                    (
                        [-both, left],
                        [-both, right],
                        [both, -left, -right],
                    )
                )
            self.top_id += 1
            same = self.top_id
            same_variables.append(same)
            same_by_edge[edge] = same
            clauses.append([-same, *equal_colour_variables])
            clauses.extend(
                [-both, same] for both in equal_colour_variables
            )
        clauses.append([-same for same in same_variables])
        # The degree-five singleton theorem forces the monochromatic
        # singleton subgraph to cover every vertex.
        for vertex in range(self.system.n):
            clauses.append(
                [
                    same_by_edge[edge]
                    for edge in singleton_edges
                    if vertex in edge
                ]
            )

        # Required monochromatic amplitudes must be nonzero structurally.
        for colouring_index, required in enumerate(self.system.target):
            if not bool(required):
                continue
            variables = [
                self.ensure_activity(
                    clauses,
                    colouring_index,
                    matching_index,
                )
                for matching_index in range(len(self.system.matchings))
            ]
            clauses.append(variables)
        return clauses

    def required_literals(
        self,
        colouring_index: int,
        matching_index: int,
    ) -> list[int]:
        colouring = self.system.colourings[colouring_index]
        literals: list[int] = []
        for edge in self.system.matchings[matching_index]:
            canonical = tuple(map(int, edge))
            if canonical in self.full_edges:
                continue
            if canonical not in self.singleton_edges:
                # A matching using a structural-zero block is inactive.
                return [0]
            for vertex in canonical:
                literals.append(
                    self.incidence_variable[
                        (
                            vertex,
                            canonical,
                            int(colouring[vertex]),
                        )
                    ]
                )
        return literals

    def ensure_activity(
        self,
        clauses: list[list[int]],
        colouring_index: int,
        matching_index: int,
    ) -> int:
        key = (colouring_index, matching_index)
        existing = self.activity_variable.get(key)
        if existing is not None:
            return existing
        self.top_id += 1
        variable = self.top_id
        self.activity_variable[key] = variable
        required = self.required_literals(
            colouring_index,
            matching_index,
        )
        if required == [0]:
            clauses.append([-variable])
        elif not required:
            clauses.append([variable])
        else:
            clauses.extend([-variable, literal] for literal in required)
            clauses.append([variable, *(-literal for literal in required)])
        return variable

    def encode_no_binomial_colouring(
        self,
        colouring_index: int,
    ) -> list[list[int]]:
        if colouring_index in self.encoded_colourings:
            return []
        clauses: list[list[int]] = []
        variables = [
            self.ensure_activity(
                clauses,
                colouring_index,
                matching_index,
            )
            for matching_index in range(len(self.system.matchings))
        ]
        extension, next_top, _selector = no_binomial_extension(
            variables,
            self.top_id,
        )
        self.top_id = next_top
        clauses.extend(extension)
        self.encoded_colourings.add(colouring_index)
        return clauses

    def selected_entries(self, model: set[int]) -> set[int]:
        selected: set[int] = set()
        for edge in self.full_edges:
            base = self.system.d**2 * self.system.edge_index[edge]
            selected.update(range(base, base + self.system.d**2))
        for edge in self.singleton_edges:
            first, second = edge
            first_colour = next(
                colour
                for colour in range(self.system.d)
                if self.incidence_variable[
                    (first, edge, colour)
                ] in model
            )
            second_colour = next(
                colour
                for colour in range(self.system.d)
                if self.incidence_variable[
                    (second, edge, colour)
                ] in model
            )
            base = self.system.d**2 * self.system.edge_index[edge]
            selected.add(
                base + self.system.d * first_colour + second_colour
            )
        return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-support", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-output", type=Path)
    parser.add_argument("--max-models", type=int, default=0)
    args = parser.parse_args()

    started = time.perf_counter()
    system = EquationSystem(8, 3)
    source = json.loads(
        args.source_support.read_text(encoding="utf-8")
    )
    selected = set(map(int, source["selected_flat_indices"]))
    blocks = block_support(selected, system)
    if len(blocks) != 20:
        raise ValueError("source does not have exactly 20 nonzero blocks")
    full_edges = frozenset(
        edge for edge, entries in blocks.items() if len(entries) == 9
    )
    singleton_edges = frozenset(
        edge for edge, entries in blocks.items() if len(entries) == 1
    )
    if len(full_edges) != 8 or len(singleton_edges) != 12:
        raise ValueError("source is not in the 8-full/12-singleton stratum")

    search = EqualitySearch(system, full_edges)
    clauses = search.initialize(singleton_edges)
    models = 0
    learned_colourings = 0
    status = "UNKNOWN"
    witness: dict[str, object] | None = None
    witness_support: set[int] | None = None
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        while solver.solve():
            models += 1
            positive = {
                literal
                for literal in solver.get_model() or []
                if literal > 0
            }
            support = search.selected_entries(positive)
            forbidden_histogram, required_counts = activity_summary(
                system,
                support,
            )
            mask = np.zeros(system.variable_count, dtype=bool)
            mask[list(support)] = True
            activity = np.all(mask[system.variable_ids], axis=2)
            counts = np.sum(activity, axis=0)
            bad_colourings = [
                index
                for index, required in enumerate(system.target)
                if not bool(required) and int(counts[index]) in (1, 2)
            ]
            violated = [
                index
                for index in bad_colourings
                if index not in search.encoded_colourings
            ]
            if bad_colourings and not violated:
                raise AssertionError(
                    "an encoded no-binomial colouring was violated"
                )
            print(
                f"model={models} violated={len(violated)} "
                f"encoded={len(search.encoded_colourings)} "
                f"variables={search.top_id}",
                flush=True,
            )
            if not bad_colourings:
                status = "MIXED_NO_BINOMIAL_SUPPORT_FOUND"
                witness = {
                    "selected_entries": len(support),
                    "selected_flat_indices": sorted(support),
                    "forbidden_activity_histogram": forbidden_histogram,
                    "required_activity_counts": required_counts,
                }
                witness_support = support
                break
            additions: list[list[int]] = []
            for colouring_index in violated:
                additions.extend(
                    search.encode_no_binomial_colouring(colouring_index)
                )
            learned_colourings += len(violated)
            for clause in additions:
                solver.add_clause(clause)
            if args.max_models and models >= args.max_models:
                status = "MODEL_LIMIT"
                break
        else:
            status = "UNSAT"

    model_output = args.model_output or args.output.with_suffix(
        ".model.log"
    )
    model_path: str | None = None
    model_hash: str | None = None
    toric_certificate: dict[str, object] | None = None
    if witness_support is not None:
        model_output.parent.mkdir(parents=True, exist_ok=True)
        write_model(
            model_output,
            witness_support,
            system.variable_count,
        )
        model_path = str(model_output)
        model_hash = sha256(model_output)
        from analyze_support_toric_census import discover_certificate

        toric_certificate = discover_certificate(
            system,
            sorted(witness_support),
        )

    payload = {
        "status": status,
        "scope": (
            "fixed full factor with bijective opposite-end reciprocal "
            "killer colours and at least one bichromatic singleton"
        ),
        "necessary_conditions_only": True,
        "stronger_than_prize_hypothesis": True,
        "source_support": str(args.source_support),
        "source_support_sha256": sha256(args.source_support),
        "full_edges": [list(edge) for edge in sorted(full_edges)],
        "singleton_edges": [
            list(edge) for edge in sorted(singleton_edges)
        ],
        "initial_clauses": len(clauses),
        "models": models,
        "encoded_forbidden_colourings": learned_colourings,
        "variables": search.top_id,
        "model": model_path,
        "model_sha256": model_hash,
        "toric_certificate": toric_certificate,
        "witness": witness,
        "solve_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
