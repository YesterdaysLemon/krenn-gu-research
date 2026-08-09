"""Independently replay one partial-circuit binomial-closure branch."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_portal_determinant_lattice import (
    contiguous_cycles,
    cycle_edges,
    edge,
)
from integer_signed_lattice import IntegerSignedLattice


N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def feasible_on_cycle(
    cycle: Sequence[int], deleted: set[int]
) -> bool:
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


def feasible(
    chosen: Sequence[Edge], cycles: Sequence[Sequence[int]]
) -> bool:
    endpoints = {vertex for item in chosen for vertex in item}
    return all(
        feasible_on_cycle(cycle, endpoints & set(cycle))
        for cycle in cycles
    )


def positive_minimal_subsets(
    factor: Factor, cycles: Sequence[Sequence[int]]
) -> list[Factor]:
    output = []
    for size in range(1, len(factor)):
        for chosen in itertools.combinations(factor, size):
            if not feasible(chosen, cycles):
                continue
            if any(
                feasible(smaller, cycles)
                for smaller_size in range(1, size)
                for smaller in itertools.combinations(
                    chosen, smaller_size
                )
            ):
                continue
            output.append(tuple(chosen))
    return output


def port_exception(
    chosen: Sequence[Edge],
    cycles: Sequence[Sequence[int]],
    touched: Sequence[int],
) -> bool:
    endpoints = {vertex for item in chosen for vertex in item}
    component = {
        vertex: cycle_id
        for cycle_id, cycle in enumerate(cycles)
        for vertex in cycle
    }
    for cycle_id in touched:
        cycle = tuple(cycles[cycle_id])
        local = [vertex for vertex in cycle if vertex in endpoints]
        if len(local) != 2:
            return False
        positions = sorted(cycle.index(vertex) for vertex in local)
        if (positions[1] - positions[0]) % len(cycle) not in {
            1,
            len(cycle) - 1,
        }:
            return False
    touched_set = set(map(int, touched))
    adjacency = {cycle_id: set() for cycle_id in touched_set}
    degrees = {cycle_id: 0 for cycle_id in touched_set}
    for first, second in chosen:
        left = component[first]
        right = component[second]
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
    stack = [int(touched[0])]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(adjacency[current] - seen)
    return seen == touched_set


def proper_colourings(
    first: Factor, second: Factor, colours: tuple[int, int]
) -> list[tuple[int, ...]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for factor in (first, second):
        for left, right in factor:
            adjacency[left].add(right)
            adjacency[right].add(left)
    side = [-1] * N
    components = []
    for start in range(N):
        if side[start] >= 0:
            continue
        side[start] = 0
        component = []
        stack = [start]
        while stack:
            current = stack.pop()
            component.append(current)
            for other in adjacency[current]:
                expected = 1 - side[current]
                if side[other] < 0:
                    side[other] = expected
                    stack.append(other)
                elif side[other] != expected:
                    raise AssertionError("base factors stopped bipartite")
        components.append(component)
    output = []
    for flips in itertools.product((0, 1), repeat=len(components)):
        colouring = [-1] * N
        for component_id, component in enumerate(components):
            for vertex in component:
                colouring[vertex] = colours[
                    side[vertex] ^ flips[component_id]
                ]
        output.append(tuple(colouring))
    return output


def monomial_vector(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
    variable_positions: dict[int, int],
) -> tuple[int, ...]:
    vector = [0] * len(variable_positions)
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        variable = (
            9 * engine.EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
        )
        vector[variable_positions[variable]] += 1
    return tuple(vector)


def full_relation(
    cycle: Sequence[int],
    colouring: Sequence[int],
    variable_positions: dict[int, int],
) -> tuple[int, ...]:
    edges = tuple(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )
    row = [0] * len(variable_positions)
    for sign, indices in ((1, range(0, len(edges), 2)), (-1, range(1, len(edges), 2))):
        for index in indices:
            item = edges[index]
            variable = (
                9 * engine.EDGE_INDEX[item]
                + 3 * int(colouring[item[0]])
                + int(colouring[item[1]])
            )
            row[variable_positions[variable]] += sign
    direct = tuple(row)
    negative = tuple(-value for value in row)
    return min(direct, negative)


def active_ids(
    matchings: Sequence[Factor],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item in full_edges
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        )
    )


def hamming_distance(
    first: Sequence[int], second: Sequence[int]
) -> int:
    return sum(left != right for left, right in zip(first, second))


def hamming_ball(
    centres: Sequence[Sequence[int]], radius: int
) -> set[tuple[int, ...]]:
    output = set()
    for raw_centre in centres:
        centre = tuple(map(int, raw_centre))
        output.add(centre)
        for distance in range(1, radius + 1):
            for vertices in itertools.combinations(range(N), distance):
                for replacements in itertools.product(
                    (0, 1), repeat=distance
                ):
                    candidate = list(centre)
                    for vertex, choice in zip(
                        vertices, replacements, strict=True
                    ):
                        alternatives = [
                            colour
                            for colour in range(3)
                            if colour != centre[vertex]
                        ]
                        candidate[vertex] = alternatives[choice]
                    output.add(tuple(candidate))
    return output


def sparse_to_row(
    raw: Sequence[Sequence[int]], width: int
) -> tuple[int, ...]:
    row = [0] * width
    for position, coefficient in raw:
        row[int(position)] = int(coefficient)
    return tuple(row)


def compact_lattice(
    rows: Sequence[Sequence[int]], bits: Sequence[int]
) -> tuple[IntegerSignedLattice, tuple[int, ...], set[int]]:
    positions = tuple(
        position
        for position in range(len(rows[0]))
        if any(row[position] for row in rows)
    )
    return (
        IntegerSignedLattice(
            [[row[position] for position in positions] for row in rows],
            bits,
        ),
        positions,
        set(positions),
    )


def reduce_amplitude(
    activity: Sequence[int],
    colouring: Sequence[int],
    matchings: Sequence[Factor],
    full_edges: set[Edge],
    labels: dict[Edge, int],
    variable_positions: dict[int, int],
    lattice: IntegerSignedLattice,
    positions: Sequence[int],
    position_set: set[int],
) -> list[dict[str, object]]:
    groups = []
    for matching_id in activity:
        vector = monomial_vector(
            matchings[matching_id],
            colouring,
            full_edges,
            labels,
            variable_positions,
        )
        for group in groups:
            difference = [
                left - right
                for left, right in zip(
                    vector, group["representative"], strict=True
                )
            ]
            if any(
                value
                for position, value in enumerate(difference)
                if position not in position_set
            ):
                continue
            compact = [difference[position] for position in positions]
            coordinates = lattice.coordinates(compact)
            if coordinates is None:
                continue
            sign = lattice.transported_sign(compact)
            group["coefficient"] += sign
            group["members"].append(
                {
                    "matching_id": int(matching_id),
                    "sign": sign,
                    "coordinates": coordinates,
                }
            )
            break
        else:
            groups.append(
                {
                    "representative": list(vector),
                    "coefficient": 1,
                    "members": [
                        {
                            "matching_id": int(matching_id),
                            "sign": 1,
                            "coordinates": [0] * lattice.generators,
                        }
                    ],
                }
            )
    return [group for group in groups if group["coefficient"]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    if analysis["status"] not in {
        "contradiction",
        "relation_selection_branch_contradiction",
        "binomial_closure_survivor",
    }:
        raise AssertionError("unsupported binomial-closure status")
    survivor_mode = analysis["status"] == "binomial_closure_survivor"
    support_mode = analysis["status"] == "contradiction"
    mandatory_core_survivor_mode = (
        survivor_mode
        and analysis.get("selected_mandatory_unit_core") is True
    )
    if support_mode:
        if (
            not analysis.get("support_closed")
            or not analysis.get("selected_mandatory_unit_core")
        ):
            raise AssertionError(
                "unconditional contradiction lacks a mandatory unit core"
            )
    elif analysis.get("support_closed"):
        raise AssertionError("conditional branch was mislabeled as support")
    if not survivor_mode and not analysis.get(
        "relation_selection_branch_closed"
    ):
        raise AssertionError("branch closure flag changed")
    if survivor_mode and analysis.get("relation_selection_branch_closed"):
        raise AssertionError("survivor was mislabeled as branch closure")

    partial = json.loads(
        Path(analysis["partial_analysis"]).read_text(encoding="utf-8")
    )
    partition = tuple(map(int, partial["partition"]))
    cycles = contiguous_cycles(partition)
    factors = tuple(
        tuple(edge(*map(int, item)) for item in factor)
        for factor in partial["singleton_factors"]
    )
    full_edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = frozenset(full_edges)
    matchings = engine.perfect_matchings(full_edges | set(labels))
    if len(matchings) != int(analysis["skeleton_perfect_matchings"]):
        raise AssertionError("perfect-matching census changed")
    support_variables = sorted(
        {
            9 * engine.EDGE_INDEX[item] + 3 * left + right
            for item in full_edges
            for left in range(3)
            for right in range(3)
        }
        | {
            9 * engine.EDGE_INDEX[item] + 4 * colour
            for item, colour in labels.items()
        }
    )
    variable_positions = {
        variable: position
        for position, variable in enumerate(support_variables)
    }
    width = len(support_variables)
    reported_rows = [
        sparse_to_row(raw, width)
        for raw in analysis["relation_vectors"]
    ]
    bits = list(map(int, analysis["final_sign_bits"]))
    initial_count = int(analysis["initial_relations"])
    selected_ids = list(
        map(int, analysis["selected_initial_relation_ids"])
    )
    if initial_count != len(selected_ids):
        raise AssertionError("selected initial relation count changed")

    reconstructed_relations = set()
    clauses = set()
    relation_index = {}
    relation_rows = []
    relation_centres: list[set[tuple[int, ...]]] = []
    for colour in range(3):
        other = [item for item in range(3) if item != colour]
        bases = proper_colourings(
            factors[other[0]],
            factors[other[1]],
            (other[0], other[1]),
        )
        for chosen in positive_minimal_subsets(
            factors[colour], cycles
        ):
            endpoints = {vertex for item in chosen for vertex in item}
            touched = tuple(
                cycle_id
                for cycle_id, cycle in enumerate(cycles)
                if endpoints & set(cycle)
            )
            untouched = tuple(
                cycle_id
                for cycle_id in range(len(cycles))
                if cycle_id not in touched
            )
            if not untouched or port_exception(chosen, cycles, touched):
                continue
            for base in bases:
                target = list(base)
                for vertex in endpoints:
                    target[vertex] = colour
                ids = []
                for cycle_id in untouched:
                    row = full_relation(
                        cycles[cycle_id],
                        target,
                        variable_positions,
                    )
                    reconstructed_relations.add(row)
                    if row not in relation_index:
                        relation_index[row] = len(relation_rows)
                        relation_rows.append(row)
                        relation_centres.append(set())
                    relation_id = relation_index[row]
                    relation_centres[relation_id].add(tuple(target))
                    ids.append(relation_id)
                clauses.add(tuple(sorted(set(ids))))
    expected_relation_count = 1 + max(
        relation_id for clause in clauses for relation_id in clause
    )
    if len(reconstructed_relations) != expected_relation_count:
        raise AssertionError("relation reconstruction count changed")
    try:
        reconstructed_selected_ids = [
            relation_index[row] for row in reported_rows[:initial_count]
        ]
    except KeyError as error:
        raise AssertionError(
            "selected initial relation row was not reconstructed"
        ) from error
    if len(set(reconstructed_selected_ids)) != initial_count:
        raise AssertionError("selected initial relation rows are not distinct")
    selected_set = set(reconstructed_selected_ids)
    if support_mode or mandatory_core_survivor_mode:
        unit_relation_ids = {
            clause[0] for clause in clauses if len(clause) == 1
        }
        if (
            selected_set != unit_relation_ids
            or not unit_relation_ids
        ):
            raise AssertionError(
                "reported support core is not exactly the mandatory units"
            )
    elif any(not set(clause) & selected_set for clause in clauses):
        raise AssertionError("selected branch violates a relation clause")
    centres = set().union(
        *(
            relation_centres[relation_id]
            for relation_id in reconstructed_selected_ids
        )
    )

    lattice_by_round: dict[
        int, tuple[IntegerSignedLattice, tuple[int, ...], set[int]]
    ] = {}
    derived_checked = 0
    for relation_id in range(initial_count, len(reported_rows)):
        source = analysis["relation_sources"][relation_id]
        source_mode = source["mode"]
        if source_mode not in {
            "derived_forbidden_binomial_amplitude",
            "derived_required_unit_amplitude",
        }:
            raise AssertionError("unexpected derived relation source")
        source_round = int(source["round"])
        if source_round not in lattice_by_round:
            prefix_count = next(
                (
                    index
                    for index in range(
                        initial_count, len(reported_rows)
                    )
                    if int(
                        analysis["relation_sources"][index]["round"]
                    )
                    >= source_round
                ),
                len(reported_rows),
            )
            lattice_by_round[source_round] = compact_lattice(
                reported_rows[:prefix_count], bits[:prefix_count]
            )
        source_lattice, source_positions, source_position_set = (
            lattice_by_round[source_round]
        )
        if source_lattice.has_inconsistent_kernel:
            raise AssertionError(
                "source lattice has a prior signed-kernel conflict"
            )
        colouring = tuple(map(int, source["target_colouring"]))
        if source_mode == "derived_forbidden_binomial_amplitude":
            if min(
                hamming_distance(colouring, centre)
                for centre in centres
            ) > int(analysis["hamming_radius"]):
                raise AssertionError(
                    "derived source left the Hamming census"
                )
        elif len(set(colouring)) != 1:
            raise AssertionError(
                "required unit source stopped being monochromatic"
            )
        activity = active_ids(
            matchings, colouring, full_edges, labels
        )
        if list(activity) != list(source["target_matching_ids"]):
            raise AssertionError("derived source activity changed")
        groups = reduce_amplitude(
            activity,
            colouring,
            matchings,
            full_edges,
            labels,
            variable_positions,
            source_lattice,
            source_positions,
            source_position_set,
        )
        if source_mode == "derived_forbidden_binomial_amplitude":
            if (
                len(groups) != 2
                or abs(groups[0]["coefficient"])
                != abs(groups[1]["coefficient"])
            ):
                raise AssertionError(
                    "derived source stopped being binomial"
                )
            if [group["coefficient"] for group in groups] != list(
                source["group_coefficients"]
            ):
                raise AssertionError(
                    "derived group coefficients changed"
                )
            row = tuple(
                left - right
                for left, right in zip(
                    groups[0]["representative"],
                    groups[1]["representative"],
                    strict=True,
                )
            )
            bit = int(
                -groups[1]["coefficient"]
                // groups[0]["coefficient"]
                == -1
            )
        else:
            if (
                len(groups) != 1
                or abs(int(groups[0]["coefficient"])) != 1
            ):
                raise AssertionError(
                    "required source stopped being a unit amplitude"
                )
            if int(groups[0]["coefficient"]) != int(
                source["group_coefficient"]
            ):
                raise AssertionError(
                    "required unit coefficient changed"
                )
            row = tuple(groups[0]["representative"])
            bit = int(int(groups[0]["coefficient"]) == -1)
        row = min(row, tuple(-value for value in row))
        if row != reported_rows[relation_id] or bit != bits[relation_id]:
            raise AssertionError("derived signed relation changed")
        derived_checked += 1

    final_lattice, final_positions, final_position_set = compact_lattice(
        reported_rows, bits
    )
    if final_lattice.has_inconsistent_kernel:
        raise AssertionError("final relations have a prior kernel conflict")
    if survivor_mode:
        monochromatic = {
            tuple([colour] * N) for colour in range(3)
        }
        candidates = sorted(
            hamming_ball(
                centres, int(analysis["hamming_radius"])
            )
            | monochromatic
        )
        amplitudes_tested = 0
        maximum_activity = 0
        two_class_amplitudes = 0
        two_class_equal_magnitude_amplitudes = 0
        required_unit_anchors = 0

        def require_final_implication(
            raw_row: Sequence[int],
            expected_sign: int,
            label: str,
        ) -> None:
            row = min(
                tuple(map(int, raw_row)),
                tuple(-int(value) for value in raw_row),
            )
            if any(
                value
                for position, value in enumerate(row)
                if position not in final_position_set
            ):
                raise AssertionError(f"{label} was not derived")
            compact = [
                row[position] for position in final_positions
            ]
            coordinates = final_lattice.coordinates(compact)
            if coordinates is None:
                raise AssertionError(f"{label} was not derived")
            if final_lattice.transported_sign(compact) != expected_sign:
                raise AssertionError(f"{label} has the wrong sign")

        for target in candidates:
            activity = active_ids(
                matchings, target, full_edges, labels
            )
            required = target in monochromatic
            if not activity and not required:
                continue
            amplitudes_tested += 1
            maximum_activity = max(maximum_activity, len(activity))
            groups = reduce_amplitude(
                activity,
                target,
                matchings,
                full_edges,
                labels,
                variable_positions,
                final_lattice,
                final_positions,
                final_position_set,
            )
            if not required and len(groups) == 1:
                raise AssertionError(
                    "survivor census has an isolated forbidden class"
                )
            if (
                not required
                and len(groups) == 2
            ):
                two_class_amplitudes += 1
                if (
                    abs(groups[0]["coefficient"])
                    == abs(groups[1]["coefficient"])
                ):
                    two_class_equal_magnitude_amplitudes += 1
                    row = [
                        left - right
                        for left, right in zip(
                            groups[0]["representative"],
                            groups[1]["representative"],
                            strict=True,
                        )
                    ]
                    expected_sign = (
                        -groups[1]["coefficient"]
                        // groups[0]["coefficient"]
                    )
                    require_final_implication(
                        row,
                        int(expected_sign),
                        "survivor forbidden binomial",
                    )
            if required and not groups:
                raise AssertionError(
                    "survivor census annihilates a required amplitude"
                )
            if (
                required
                and len(groups) == 1
                and abs(groups[0]["coefficient"]) == 1
            ):
                required_unit_anchors += 1
                require_final_implication(
                    groups[0]["representative"],
                    int(groups[0]["coefficient"]),
                    "survivor required unit anchor",
                )
        if not analysis["rounds"]:
            raise AssertionError("survivor has no closure round")
        for round_record in analysis["rounds"]:
            round_id = int(round_record["round"])
            before = initial_count + sum(
                int(source.get("round", 0)) < round_id
                for source in analysis["relation_sources"][
                    initial_count:
                ]
            )
            added = sum(
                int(source.get("round", 0)) == round_id
                for source in analysis["relation_sources"][
                    initial_count:
                ]
            )
            if (
                int(round_record["relation_count_before"]) != before
                or int(round_record["new_relations"]) != added
                or int(round_record["relation_count_after"])
                != before + added
            ):
                raise AssertionError(
                    "survivor round relation counts changed"
                )
        round_record = analysis["rounds"][-1]
        expected = {
            "candidate_colourings": len(candidates),
            "amplitudes_tested": amplitudes_tested,
            "maximum_activity": maximum_activity,
            "one_class_forbidden_amplitudes": 0,
            "two_class_amplitudes": two_class_amplitudes,
            "two_class_equal_magnitude_amplitudes": (
                two_class_equal_magnitude_amplitudes
            ),
            "required_unit_anchors": required_unit_anchors,
            "new_relations": 0,
        }
        for key, value in expected.items():
            if int(round_record[key]) != value:
                raise AssertionError(
                    f"survivor metric changed: {key}"
                )
        payload = {
            "verified": True,
            "status": (
                "partial_circuit_mandatory_core_survivor_verified"
                if mandatory_core_survivor_mode
                else "partial_circuit_binomial_survivor_verified"
            ),
            "scope": (
                (
                    "independent relation clauses, exact mandatory-unit "
                    "core, every derived two-coset or required-unit "
                    "amplitude, Smith lattice, full Hamming candidate "
                    "census, activity, signed cosets, and absence of "
                    "every supported closure or contradiction trigger"
                )
                if mandatory_core_survivor_mode
                else (
                    "independent relation clauses, selected mandatory "
                    "relations, Smith lattice, full Hamming candidate "
                    "census, activity, signed cosets, and absence of "
                    "every supported closure or contradiction trigger"
                )
            ),
            "analysis": str(args.analysis),
            "partition": list(partition),
            "orbit": int(analysis["orbit"]),
            "relation_clauses": len(clauses),
            "selected_initial_relations": initial_count,
            "derived_relations_checked": derived_checked,
            "candidate_colourings": len(candidates),
            "amplitudes_tested": amplitudes_tested,
            "maximum_activity": maximum_activity,
            "relation_selection_branch_closed": False,
            "support_closed": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": time.perf_counter() - started,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(payload, indent=2))
        return

    contradiction = analysis["contradiction"]
    if contradiction["mode"] != "isolated_nonzero_lattice_class":
        raise AssertionError("unsupported contradiction mode")
    target = tuple(map(int, contradiction["target_colouring"]))
    if len(set(target)) == 1:
        raise AssertionError("contradiction target became monochromatic")
    if min(hamming_distance(target, centre) for centre in centres) > int(
        analysis["hamming_radius"]
    ):
        raise AssertionError("contradiction target left Hamming census")
    activity = active_ids(matchings, target, full_edges, labels)
    if list(activity) != list(contradiction["target_matching_ids"]):
        raise AssertionError("contradiction activity changed")
    groups = reduce_amplitude(
        activity,
        target,
        matchings,
        full_edges,
        labels,
        variable_positions,
        final_lattice,
        final_positions,
        final_position_set,
    )
    if len(groups) != 1 or groups[0]["coefficient"] == 0:
        raise AssertionError("target stopped having one nonzero class")
    if groups[0] != contradiction["surviving_group"]:
        raise AssertionError("reported surviving class changed")

    payload = {
        "verified": True,
        "status": (
            "partial_circuit_binomial_support_verified"
            if support_mode
            else "partial_circuit_binomial_branch_verified"
        ),
        "scope": (
            (
                "independent minimal-circuit relation clauses, selected "
                "initial branch, every derived two-coset or required-unit "
                "amplitude, final Smith lattice, target activity, and "
                "isolated signed class"
            )
            if any(
                source.get("mode")
                == "derived_required_unit_amplitude"
                for source in analysis["relation_sources"][
                    initial_count:
                ]
            )
            else (
                "independent minimal-circuit relation clauses, selected "
                "initial branch, every derived two-coset amplitude, final "
                "Smith lattice, target activity, and isolated signed class"
            )
        ),
        "analysis": str(args.analysis),
        "partition": list(partition),
        "orbit": int(analysis["orbit"]),
        "relation_clauses": len(clauses),
        "unit_relation_clauses": sum(
            len(clause) == 1 for clause in clauses
        ),
        "binary_relation_clauses": sum(
            len(clause) == 2 for clause in clauses
        ),
        "selected_initial_relations": initial_count,
        "derived_relations_checked": derived_checked,
        "final_relations": len(reported_rows),
        "final_lattice_rank": final_lattice.rank,
        "target_active_matchings": len(activity),
        "target_nonzero_signed_classes": len(groups),
        "relation_selection_branch_closed": True,
        "support_closed": support_mode,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    if support_mode:
        payload["analysis_sha256"] = sha256(args.analysis)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
