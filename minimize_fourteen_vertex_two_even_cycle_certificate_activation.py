"""Minimize the activation premises of a two-cycle factor-fork proof.

For each equation used by the proof, the source certificate records its
entire active perfect-matching set.  To preserve that set under transport it
is enough to:

* require every role-1/role-2 edge used by a desired active matching; and
* choose a hitting set of source-absent role-1/role-2 edges that meets every
  other potentially active perfect matching.

By default the resulting partial assignment is exact even before imposing
the global support constraints.  An optional structural mode first discards
unwanted matchings that cannot occur when roles 1 and 2 are perfect
matchings edge-disjoint from each other and from the pinned role-0 factor.
A stronger optional scope additionally imposes the globally required
connectedness of the union with the fixed full factor.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.examples.hitman import Hitman
from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    Factor,
    edge_variable,
    parse_factor,
    validate_simple_certificate,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
    transform as transform_factor_by_action,
)
from explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(item: object) -> str:
    return hashlib.sha256(
        json.dumps(
            item, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def colouring_index(colouring: tuple[int, ...]) -> int:
    return sum(
        int(colour) * (3**vertex)
        for vertex, colour in enumerate(colouring)
    )


def transform_colouring(
    colouring: tuple[int, ...],
    action: dict[int, int],
    colour_permutation: tuple[int, int, int],
) -> tuple[int, ...]:
    output = [0] * N
    for old_vertex, old_colour in enumerate(colouring):
        output[action[old_vertex]] = colour_permutation[old_colour]
    return tuple(output)


def matching_activity(
    matching: Factor,
    full_edges: set[Edge],
    factors: tuple[Factor, Factor, Factor],
    colouring: tuple[int, ...],
) -> bool:
    labels = {
        item: role
        for role, factor in enumerate(factors)
        for item in factor
    }
    return all(
        item in full_edges
        or (
            item in labels
            and colouring[item[0]]
            == colouring[item[1]]
            == labels[item]
        )
        for item in matching
    )


def minimize_conditions(
    factors: tuple[Factor, Factor, Factor],
    colourings: tuple[tuple[int, ...], ...],
    full_edges: set[Edge],
    eligible_edges: tuple[Edge, ...],
    structural_feasibility: bool = False,
    connected_structural_feasibility: bool = False,
    three_connected_structural_feasibility: bool = False,
) -> tuple[dict[int, bool], list[dict[str, int]]]:
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    source_union = set().union(*map(set, factors))
    source_matchings = perfect_matchings(
        N, full_edges | source_union
    )
    required_true: set[int] = set()
    unwanted_rows: list[tuple[int, list[int], list[int]]] = []
    equation_rows = []

    for equation_id, colouring in enumerate(colourings):
        desired = {
            matching
            for matching in source_matchings
            if matching_activity(
                matching, full_edges, factors, colouring
            )
        }
        possible_role: dict[Edge, int] = {}
        for role in (1, 2):
            for item in eligible_edges:
                if (
                    colouring[item[0]]
                    == colouring[item[1]]
                    == role
                ):
                    possible_role[item] = role
        role_zero_edges = {
            item
            for item in factors[0]
            if colouring[item[0]]
            == colouring[item[1]]
            == 0
        }
        possible = perfect_matchings(
            N,
            full_edges
            | role_zero_edges
            | set(possible_role),
        )
        for matching in desired:
            for item in matching:
                role = possible_role.get(item)
                if role is None:
                    continue
                if item not in factors[role]:
                    raise AssertionError(
                        "desired matching uses a source-absent edge"
                    )
                required_true.add(
                    edge_variable(
                        role, edge_id[item], len(eligible_edges)
                    )
                )
        unwanted = 0
        for matching in possible:
            if matching in desired:
                continue
            candidates = []
            active_role_variables = []
            for item in matching:
                role = possible_role.get(item)
                if role is None:
                    continue
                variable = edge_variable(
                    role, edge_id[item], len(eligible_edges)
                )
                active_role_variables.append(variable)
                if item not in factors[role]:
                    candidates.append(variable)
            if not candidates:
                raise AssertionError(
                    "unwanted matching has no source-false blocker"
                )
            unwanted_rows.append(
                (
                    equation_id,
                    sorted(set(candidates)),
                    sorted(set(active_role_variables)),
                )
            )
            unwanted += 1
        equation_rows.append(
            {
                "desired_matchings": len(desired),
                "potential_matchings": len(possible),
                "unwanted_matchings": unwanted,
            }
        )

    if (
        connected_structural_feasibility
        or three_connected_structural_feasibility
    ):
        structural_feasibility = True

    if structural_feasibility:
        structural = CNF()
        for role in (1, 2):
            for vertex in range(N):
                incident = [
                    edge_variable(
                        role, edge_id[item], len(eligible_edges)
                    )
                    for item in eligible_edges
                    if vertex in item
                ]
                structural.append(incident)
                for first, second in itertools.combinations(incident, 2):
                    structural.append([-first, -second])
            for item in factors[0]:
                structural.append(
                    [
                        -edge_variable(
                            role,
                            edge_id[item],
                            len(eligible_edges),
                        )
                    ]
                )
        for item_id in range(len(eligible_edges)):
            structural.append(
                [
                    -edge_variable(
                        1, item_id, len(eligible_edges)
                    ),
                    -edge_variable(
                        2, item_id, len(eligible_edges)
                    ),
                ]
            )
        if (
            connected_structural_feasibility
            or three_connected_structural_feasibility
        ):
            fixed_edges = full_edges | set(factors[0])
            deletion_sizes = (
                range(3)
                if three_connected_structural_feasibility
                else range(1)
            )
            for deletion_size in deletion_sizes:
                for raw_deleted in itertools.combinations(
                    range(N), deletion_size
                ):
                    deleted = set(raw_deleted)
                    adjacency = {
                        vertex: set()
                        for vertex in range(N)
                        if vertex not in deleted
                    }
                    for first, second in fixed_edges:
                        if first in deleted or second in deleted:
                            continue
                        adjacency[first].add(second)
                        adjacency[second].add(first)
                    components = []
                    unseen = set(adjacency)
                    while unseen:
                        root = min(unseen)
                        component = {root}
                        frontier = [root]
                        unseen.remove(root)
                        while frontier:
                            vertex = frontier.pop()
                            for neighbour in adjacency[vertex] & unseen:
                                unseen.remove(neighbour)
                                component.add(neighbour)
                                frontier.append(neighbour)
                        components.append(component)
                    components.sort(
                        key=lambda row: (
                            min(row),
                            len(row),
                            tuple(sorted(row)),
                        )
                    )
                    for tail_mask in range(
                        (1 << (len(components) - 1)) - 1
                    ):
                        side = set(components[0])
                        for component_id in range(
                            1, len(components)
                        ):
                            if tail_mask & (1 << (component_id - 1)):
                                side.update(components[component_id])
                        crossing = [
                            edge_variable(
                                role,
                                edge_id[item],
                                len(eligible_edges),
                            )
                            for role in (1, 2)
                            for item in eligible_edges
                            if item not in factors[0]
                            and item[0] not in deleted
                            and item[1] not in deleted
                            and (
                                (item[0] in side)
                                != (item[1] in side)
                            )
                        ]
                        if not crossing:
                            raise AssertionError(
                                "fixed quotient has an unbridgeable cut"
                            )
                        structural.append(crossing)
        retained_rows = []
        feasible_by_equation = [0] * len(colourings)
        with Solver(
            name="cadical195", bootstrap_with=structural.clauses
        ) as solver:
            if not solver.solve(assumptions=sorted(required_true)):
                raise AssertionError(
                    "source-required premises violate support structure"
                )
            for equation_id, blockers, active in unwanted_rows:
                if solver.solve(
                    assumptions=sorted(
                        required_true.union(active)
                    )
                ):
                    retained_rows.append(
                        (equation_id, blockers, active)
                    )
                    feasible_by_equation[equation_id] += 1
        unwanted_rows = retained_rows
        for equation_id, count in enumerate(feasible_by_equation):
            equation_rows[equation_id][
                "structurally_feasible_unwanted_matchings"
            ] = count

    blocking_sets = [row[1] for row in unwanted_rows]
    unique_blocking_sets = sorted(set(map(tuple, blocking_sets)))
    with Hitman(
        bootstrap_with=[list(row) for row in unique_blocking_sets],
        htype="sorted",
    ) as hitman:
        required_false = set(map(int, hitman.get() or []))
    if required_true & required_false:
        raise AssertionError("minimum activation assignment conflicts")
    if any(
        not required_false.intersection(blocking)
        for blocking in unique_blocking_sets
    ):
        raise AssertionError("minimum hitting set misses a matching")
    conditions = {
        **{variable: True for variable in required_true},
        **{variable: False for variable in required_false},
    }
    return conditions, equation_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", type=Path)
    parser.add_argument("analysis", type=Path)
    parser.add_argument("--survivor-index", type=int, required=True)
    parser.add_argument(
        "--structural-feasibility",
        action="store_true",
        help=(
            "discard unwanted activity that cannot extend to the two "
            "variable singleton perfect matchings"
        ),
    )
    parser.add_argument(
        "--connected-structural-feasibility",
        action="store_true",
        help=(
            "also require the full-factor and singleton-factor union to "
            "be connected"
        ),
    )
    parser.add_argument(
        "--three-connected-structural-feasibility",
        action="store_true",
        help=(
            "require the completed support to remain connected after "
            "deleting any set of at most two vertices"
        ),
    )
    parser.add_argument(
        "--pin-source-role",
        type=int,
        choices=(0, 1, 2),
        default=0,
        help=(
            "re-orient the colour-symmetric proof so this source "
            "singleton role becomes the pinned first factor"
        ),
    )
    parser.add_argument(
        "--census",
        type=Path,
        help=(
            "first-factor orbit census used to canonicalize a re-oriented "
            "pinned factor; required when --pin-source-role is nonzero"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest = json.loads(args.samples.read_text(encoding="utf-8"))
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    lengths = tuple(map(int, manifest["partition"]))
    if any(length % 2 for length in lengths) or sum(lengths) != N:
        raise AssertionError("manifest is not an even-cycle factor")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    survivor = manifest["survivors"][args.survivor_index]
    if analysis.get("status") == "two_even_cycle_factor_fork":
        factors, colourings = validate_simple_certificate(
            analysis, survivor, cycles, full_edges
        )
    elif (
        analysis.get("status") == "even_cycle_factor_fork"
        and lengths == (4, 4, 6)
    ):
        from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
            validate_simple_certificate as validate_c4_c4_c6,
        )

        factors, colourings = validate_c4_c4_c6(analysis)
        survivor_factors = tuple(
            parse_factor(survivor[key])
            for key in ("first", "second", "third")
        )
        if survivor_factors != factors:
            raise AssertionError(
                "analysis and survivor singleton factors differ"
            )
    elif analysis.get("status") == "one_extra_cycle_core":
        if tuple(map(int, analysis["full_cycle_type"])) != lengths:
            raise AssertionError("one-extra core partition changed")
        factors = tuple(
            parse_factor(analysis["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        survivor_factors = tuple(
            parse_factor(survivor[key])
            for key in ("first", "second", "third")
        )
        if survivor_factors != factors:
            raise AssertionError(
                "one-extra core and survivor singleton factors differ"
            )
        core_certificate = analysis["certificate"]
        source_equations = [
            int(core_certificate["full_only_equation_index"]),
            *[
                int(row["one_extra_equation_index"])
                for row in core_certificate["cycle_rows"]
            ],
        ]
        source_equations = list(dict.fromkeys(source_equations))
        colourings = tuple(
            tuple(
                (equation // (3**vertex)) % 3
                for vertex in range(N)
            )
            for equation in source_equations
        )
    else:
        raise AssertionError("unsupported simple factor-fork status")
    source_factors = factors
    source_colourings = colourings
    if analysis.get("status") != "one_extra_cycle_core":
        source_equations = [
            int(analysis["certificate"]["base_equation_index"]),
            *[
                int(row["target_equation_index"])
                for row in analysis["certificate"]["alternatives"]
            ],
        ]
    source_transform = None
    if args.pin_source_role:
        if args.census is None:
            raise ValueError(
                "--census is required when --pin-source-role is nonzero"
            )
        census = json.loads(args.census.read_text(encoding="utf-8"))
        if tuple(map(int, census["partition"])) != lengths:
            raise AssertionError("canonicalization census changed")
        representatives = {
            parse_factor(row["representative"])
            for row in census["factor_orbits"]
        }
        if args.pin_source_role == 1:
            role_permutation = (1, 0, 2)
        else:
            role_permutation = (1, 2, 0)
        reordered: list[Factor | None] = [None, None, None]
        for old_role, factor in enumerate(source_factors):
            reordered[role_permutation[old_role]] = factor
        if any(factor is None for factor in reordered):
            raise AssertionError("source role permutation failed")
        permuted_factors = tuple(
            factor for factor in reordered if factor is not None
        )
        action = next(
            (
                candidate
                for candidate in full_automorphisms(cycles)
                if transform_factor_by_action(
                    permuted_factors[0], candidate
                )
                in representatives
            ),
            None,
        )
        if action is None:
            raise AssertionError(
                "re-oriented first factor has no census representative"
            )
        factors = tuple(
            transform_factor_by_action(factor, action)
            for factor in permuted_factors
        )
        colourings = tuple(
            transform_colouring(
                colouring,
                action,
                role_permutation,
            )
            for colouring in source_colourings
        )
        source_transform = {
            "pinned_source_role": args.pin_source_role,
            "role_permutation": list(role_permutation),
            "vertex_action": [
                int(action[vertex]) for vertex in range(N)
            ],
            "census": str(args.census),
            "census_sha256": sha256(args.census),
        }
    conditions, equation_rows = minimize_conditions(
        factors,
        colourings,
        full_edges,
        eligible_edges,
        structural_feasibility=args.structural_feasibility,
        connected_structural_feasibility=(
            args.connected_structural_feasibility
        ),
        three_connected_structural_feasibility=(
            args.three_connected_structural_feasibility
        ),
    )
    payload = {
        "status": "fourteen_vertex_minimum_activity_certificate",
        "partition": list(lengths),
        "samples": str(args.samples),
        "samples_sha256": sha256(args.samples),
        "survivor_canonical_sha256": canonical_sha256(survivor),
        "analysis": str(args.analysis),
        "analysis_sha256": sha256(args.analysis),
        "survivor_index": args.survivor_index,
        "singleton_matchings": {
            key: [list(item) for item in factor]
            for key, factor in zip(
                ("first", "second", "third"),
                factors,
                strict=True,
            )
        },
        "source_equations": source_equations,
        "source_transform": source_transform,
        "equations": list(map(colouring_index, colourings)),
        "equation_activity": equation_rows,
        "activity_scope": (
            "three_connected_perfect_matching_edge_disjoint"
            if args.three_connected_structural_feasibility
            else (
                "connected_perfect_matching_edge_disjoint"
                if args.connected_structural_feasibility
                else (
                    "perfect_matching_edge_disjoint"
                    if args.structural_feasibility
                    else "unconditional_edge_assignment"
                )
            )
        ),
        "activation_conditions": [
            [variable, value]
            for variable, value in sorted(conditions.items())
        ],
        "activation_constraint_score": len(conditions),
        "source_full_mask_score": sum(
            1
            for role in (1, 2)
            for colouring in colourings
            for item in eligible_edges
            if colouring[item[0]]
            == colouring[item[1]]
            == role
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_replayed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
