"""Independently verify a minimized even-cycle activation certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.examples.hitman import Hitman
from pysat.solvers import Solver

N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]


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


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def parse_factor(raw: list[list[int]]) -> Factor:
    return tuple(sorted(edge(*item) for item in raw))


def cycles_for(lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise AssertionError("partition changed")
    return tuple(output)


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def colouring_index(colouring: tuple[int, ...]) -> int:
    return sum(
        int(colour) * (3**vertex)
        for vertex, colour in enumerate(colouring)
    )


def transform_factor(
    factor: Factor, action: tuple[int, ...]
) -> Factor:
    return tuple(
        sorted(edge(action[first], action[second]) for first, second in factor)
    )


def transform_colouring(
    colouring: tuple[int, ...],
    action: tuple[int, ...],
    role_permutation: tuple[int, int, int],
) -> tuple[int, ...]:
    output = [0] * N
    for old_vertex, old_colour in enumerate(colouring):
        output[action[old_vertex]] = role_permutation[old_colour]
    return tuple(output)


def enumerate_matchings(allowed: set[Edge]) -> list[Factor]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output = []

    def visit(remaining: int, chosen: Factor) -> None:
        if not remaining:
            output.append(tuple(sorted(chosen)))
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << N) - 1, ())
    return sorted(set(output))


def edge_variable(role: int, edge_id: int, edge_count: int) -> int:
    return 1 + role * edge_count + edge_id


def connected(
    edges: set[Edge], deleted: frozenset[int] = frozenset()
) -> bool:
    adjacency = {
        vertex: set()
        for vertex in range(N)
        if vertex not in deleted
    }
    for first, second in edges:
        if first in deleted or second in deleted:
            continue
        adjacency[first].add(second)
        adjacency[second].add(first)
    root = min(adjacency)
    seen = {root}
    frontier = [root]
    while frontier:
        vertex = frontier.pop()
        for neighbour in adjacency[vertex] - seen:
            seen.add(neighbour)
            frontier.append(neighbour)
    return len(seen) == N - len(deleted)


def three_connected(edges: set[Edge]) -> bool:
    return all(
        connected(edges, frozenset(deleted))
        for size in range(3)
        for deleted in itertools.combinations(range(N), size)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    certificate = json.loads(
        args.certificate.read_text(encoding="utf-8")
    )
    if certificate.get("status") not in {
        "two_even_cycle_minimum_activity_certificate",
        "fourteen_vertex_minimum_activity_certificate",
    }:
        raise AssertionError("minimum certificate status changed")
    samples_path = Path(certificate["samples"])
    analysis_path = Path(certificate["analysis"])
    if sha256(analysis_path) != certificate["analysis_sha256"]:
        raise AssertionError("minimum certificate provenance changed")
    manifest = json.loads(samples_path.read_text(encoding="utf-8"))
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    survivor_index = int(certificate["survivor_index"])
    survivor = manifest["survivors"][survivor_index]
    if (
        canonical_sha256(survivor)
        != certificate["survivor_canonical_sha256"]
    ):
        raise AssertionError("minimum certificate survivor changed")
    lengths = tuple(map(int, manifest["partition"]))
    if (
        tuple(map(int, certificate["partition"])) != lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("minimum certificate partition changed")
    cycles = cycles_for(lengths)
    full_edges = {
        edge(cycle[position], cycle[(position + 1) % len(cycle)])
        for cycle in cycles
        for position in range(len(cycle))
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    eligible_edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    source_factors = tuple(
        parse_factor(survivor[key])
        for key in ("first", "second", "third")
    )
    if analysis.get("status") == "two_even_cycle_factor_fork":
        from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
            validate_simple_certificate as validate_two_cycle,
        )

        validated_factors, validated_colourings = validate_two_cycle(
            analysis, survivor, cycles, full_edges
        )
    elif (
        analysis.get("status") == "even_cycle_factor_fork"
        and lengths == (4, 4, 6)
    ):
        from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
            validate_simple_certificate as validate_c4_c4_c6,
        )

        validated_factors, validated_colourings = validate_c4_c4_c6(
            analysis
        )
    elif analysis.get("status") == "one_extra_cycle_core":
        if tuple(map(int, analysis["full_cycle_type"])) != lengths:
            raise AssertionError("one-extra core partition changed")
        validated_factors = tuple(
            parse_factor(analysis["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        core = analysis["certificate"]
        source_equations = [
            int(core["full_only_equation_index"]),
            *[
                int(row["one_extra_equation_index"])
                for row in core["cycle_rows"]
            ],
        ]
        source_equations = list(dict.fromkeys(source_equations))
        validated_colourings = tuple(
            map(indexed_colouring, source_equations)
        )
        core_audit_path = analysis_path.with_name(
            f"{analysis_path.stem}_verified.json"
        )
        core_audit = json.loads(
            core_audit_path.read_text(encoding="utf-8")
        )
        if (
            core_audit.get("verified") is not True
            or core_audit.get("status")
            != "one_extra_cycle_core_verified"
            or core_audit.get("certificate_sha256")
            != sha256(analysis_path)
        ):
            raise AssertionError(
                "one-extra source core is not independently verified"
            )
    else:
        raise AssertionError("unsupported source factor-fork status")
    if tuple(validated_factors) != source_factors:
        raise AssertionError(
            "independently validated singleton factors changed"
        )
    if analysis.get("status") != "one_extra_cycle_core":
        source_equations = [
            int(analysis["certificate"]["base_equation_index"]),
            *[
                int(row["target_equation_index"])
                for row in analysis["certificate"]["alternatives"]
            ],
        ]
    if list(
        map(
            int,
            certificate.get("source_equations", source_equations),
        )
    ) != source_equations:
        raise AssertionError("minimum certificate source equations changed")
    source_colourings = tuple(map(indexed_colouring, source_equations))
    if tuple(map(tuple, validated_colourings)) != source_colourings:
        raise AssertionError(
            "independently validated source colourings changed"
        )
    transformation = certificate.get("source_transform")
    if transformation is None:
        factors = source_factors
        colourings = source_colourings
    else:
        pinned_source_role = int(
            transformation["pinned_source_role"]
        )
        role_permutation = tuple(
            map(int, transformation["role_permutation"])
        )
        action = tuple(map(int, transformation["vertex_action"]))
        if (
            pinned_source_role not in (1, 2)
            or sorted(role_permutation) != [0, 1, 2]
            or role_permutation[pinned_source_role] != 0
            or len(action) != N
            or sorted(action) != list(range(N))
        ):
            raise AssertionError("source re-orientation changed")
        transformed_full_edges = {
            edge(action[first], action[second])
            for first, second in full_edges
        }
        if transformed_full_edges != full_edges:
            raise AssertionError(
                "source vertex action is not a full-factor automorphism"
            )
        reordered: list[Factor | None] = [None, None, None]
        for old_role, factor in enumerate(source_factors):
            reordered[role_permutation[old_role]] = transform_factor(
                factor, action
            )
        if any(factor is None for factor in reordered):
            raise AssertionError("source factor re-orientation failed")
        factors = tuple(
            factor for factor in reordered if factor is not None
        )
        colourings = tuple(
            transform_colouring(
                colouring,
                action,
                role_permutation,
            )
            for colouring in source_colourings
        )
        census_path = Path(transformation["census"])
        if sha256(census_path) != transformation["census_sha256"]:
            raise AssertionError("re-orientation census changed")
        census = json.loads(census_path.read_text(encoding="utf-8"))
        if (
            tuple(map(int, census["partition"])) != lengths
            or factors[0]
            not in {
                parse_factor(row["representative"])
                for row in census["factor_orbits"]
            }
        ):
            raise AssertionError(
                "re-oriented first factor is not a census representative"
            )
    stored_factors = tuple(
        parse_factor(certificate["singleton_matchings"][key])
        for key in ("first", "second", "third")
    )
    if stored_factors != factors:
        raise AssertionError("minimum certificate factors changed")
    equations = list(map(colouring_index, colourings))
    if list(map(int, certificate["equations"])) != equations:
        raise AssertionError("minimum certificate equations changed")
    source_edges = set().union(*map(set, factors))
    source_matchings = enumerate_matchings(full_edges | source_edges)

    conditions = {
        int(variable): bool(value)
        for variable, value in certificate["activation_conditions"]
    }
    if len(conditions) != int(certificate["activation_constraint_score"]):
        raise AssertionError("minimum condition count changed")
    decoded: dict[tuple[int, Edge], bool] = {}
    for variable, value in conditions.items():
        zero = variable - 1
        role, item_id = divmod(zero, len(eligible_edges))
        if role not in (1, 2) or item_id >= len(eligible_edges):
            raise AssertionError("minimum condition variable changed")
        item = eligible_edges[item_id]
        if (item in factors[role]) != value:
            raise AssertionError("minimum condition contradicts source")
        decoded[(role, item)] = value

    required_true: set[int] = set()
    unwanted_rows: list[
        tuple[int, tuple[int, ...], tuple[int, ...]]
    ] = []
    activity_rows = []
    for equation_id, colouring in enumerate(colourings):
        def source_active(matching: Factor) -> bool:
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

        desired = {
            matching
            for matching in source_matchings
            if source_active(matching)
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
        role_zero = {
            item
            for item in factors[0]
            if colouring[item[0]]
            == colouring[item[1]]
            == 0
        }
        possible = enumerate_matchings(
            full_edges | role_zero | set(possible_role)
        )
        for matching in desired:
            for item in matching:
                role = possible_role.get(item)
                if role is None:
                    continue
                required_true.add(
                    edge_variable(
                        role,
                        eligible_edge_id[item],
                        len(eligible_edges),
                    )
                )
        unwanted = 0
        for matching in possible:
            if matching in desired:
                continue
            blockers = tuple(
                sorted(
                    edge_variable(
                        role,
                        eligible_edge_id[item],
                        len(eligible_edges),
                    )
                    for item in matching
                    for role in [possible_role.get(item)]
                    if role is not None and item not in factors[role]
                )
            )
            active_role_variables = tuple(
                sorted(
                    edge_variable(
                        role,
                        eligible_edge_id[item],
                        len(eligible_edges),
                    )
                    for item in matching
                    for role in [possible_role.get(item)]
                    if role is not None
                )
            )
            if not blockers:
                raise AssertionError("unwanted matching has no blocker")
            unwanted_rows.append(
                (equation_id, blockers, active_role_variables)
            )
            unwanted += 1
        activity_rows.append(
            {
                "desired_matchings": len(desired),
                "potential_matchings": len(possible),
                "unwanted_matchings": unwanted,
            }
        )

    activity_scope = certificate.get(
        "activity_scope", "unconditional_edge_assignment"
    )
    if activity_scope in {
        "perfect_matching_edge_disjoint",
        "connected_perfect_matching_edge_disjoint",
        "three_connected_perfect_matching_edge_disjoint",
    }:
        require_connected = activity_scope in {
            "connected_perfect_matching_edge_disjoint",
            "three_connected_perfect_matching_edge_disjoint",
        }
        require_three_connected = (
            activity_scope
            == "three_connected_perfect_matching_edge_disjoint"
        )
        def role_mask(variables: set[int] | tuple[int, ...], role: int) -> int:
            mask = 0
            for variable in variables:
                zero = int(variable) - 1
                variable_role, item_id = divmod(
                    zero, len(eligible_edges)
                )
                if variable_role == role:
                    mask |= 1 << item_id
            return mask

        fixed_masks = {
            role: role_mask(required_true, role) for role in (1, 2)
        }
        retained_rows = []
        feasible_by_equation = [0] * len(colourings)
        if not require_connected:
            structural_clauses: list[list[int]] = []
            for role in (1, 2):
                for vertex in range(N):
                    incident = [
                        edge_variable(
                            role,
                            eligible_edge_id[item],
                            len(eligible_edges),
                        )
                        for item in eligible_edges
                        if vertex in item
                    ]
                    structural_clauses.append(incident)
                    structural_clauses.extend(
                        [-first, -second]
                        for first, second in itertools.combinations(
                            incident, 2
                        )
                    )
                structural_clauses.extend(
                    [
                        -edge_variable(
                            role,
                            eligible_edge_id[item],
                            len(eligible_edges),
                        )
                    ]
                    for item in factors[0]
                )
            structural_clauses.extend(
                [
                    -edge_variable(1, item_id, len(eligible_edges)),
                    -edge_variable(2, item_id, len(eligible_edges)),
                ]
                for item_id in range(len(eligible_edges))
            )
            with Solver(
                name="cadical195",
                bootstrap_with=structural_clauses,
            ) as solver:
                if not solver.solve(
                    assumptions=sorted(required_true)
                ):
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
        else:
            allowed_factor_edges = set(eligible_edges) - set(factors[0])
            candidate_factors = enumerate_matchings(
                allowed_factor_edges
            )
            candidate_masks = []
            for factor in candidate_factors:
                mask = 0
                for item in factor:
                    mask |= 1 << eligible_edge_id[item]
                candidate_masks.append((mask, factor))
            for equation_id, blockers, active in unwanted_rows:
                required_masks = {
                    role: fixed_masks[role] | role_mask(active, role)
                    for role in (1, 2)
                }
                role_candidates = {
                    role: [
                        (mask, factor)
                        for mask, factor in candidate_masks
                        if mask & required_masks[role]
                        == required_masks[role]
                    ]
                    for role in (1, 2)
                }
                feasible = any(
                    not first_mask & second_mask
                    and (
                        three_connected(
                            full_edges
                            | set(factors[0])
                            | set(first_factor)
                            | set(second_factor)
                        )
                        if require_three_connected
                        else connected(
                            full_edges
                            | set(factors[0])
                            | set(first_factor)
                            | set(second_factor)
                        )
                    )
                    for first_mask, first_factor in role_candidates[1]
                    for second_mask, second_factor in role_candidates[2]
                )
                if feasible:
                    retained_rows.append(
                        (equation_id, blockers, active)
                    )
                    feasible_by_equation[equation_id] += 1
        unwanted_rows = retained_rows
        for equation_id, count in enumerate(feasible_by_equation):
            activity_rows[equation_id][
                "structurally_feasible_unwanted_matchings"
            ] = count
    elif activity_scope != "unconditional_edge_assignment":
        raise AssertionError("minimum activity scope changed")

    blocking_sets = [row[1] for row in unwanted_rows]
    for blockers in blocking_sets:
        if not any(
            conditions.get(variable) is False
            for variable in blockers
        ):
            raise AssertionError(
                "minimum conditions allow a feasible unwanted matching"
            )
    stored_rows = certificate["equation_activity"]
    if activity_rows != stored_rows:
        raise AssertionError("minimum activity census changed")
    stored_true = {
        variable for variable, value in conditions.items() if value
    }
    if stored_true != required_true:
        raise AssertionError("minimum certificate true premises changed")
    unique_blocks = sorted(set(blocking_sets))
    with Hitman(
        bootstrap_with=[list(row) for row in unique_blocks],
        htype="sorted",
    ) as hitman:
        optimum = hitman.get() or []
    stored_false = {
        variable for variable, value in conditions.items() if not value
    }
    if len(stored_false) != len(optimum):
        raise AssertionError("false-premise hitting set is not minimum")
    payload = {
        "verified": True,
        "status": "fourteen_vertex_minimum_activity_certificate_verified",
        "scope": (
            "source factor-fork semantics and provenance, all desired and "
            "potentially active matchings, premise truth values, hitting "
            "coverage, and exact minimum false-premise cardinality"
        ),
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "partition": list(lengths),
        "equations": equations,
        "desired_true_premises": len(required_true),
        "unwanted_matching_constraints": len(unique_blocks),
        "minimum_false_premises": len(stored_false),
        "activation_constraint_score": len(conditions),
        "activity_scope": activity_scope,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
