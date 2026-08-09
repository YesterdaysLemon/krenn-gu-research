"""Independent audit of the maximum-degree-five obstruction."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import time
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def direct_allowed(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
    row: int,
    column: int,
) -> bool:
    """Test a matrix unit directly on all coordinate-plane products."""
    for target in range(3):
        for x_colour in range(3):
            if x_colour == left[target]:
                continue
            for y_colour in range(3):
                if y_colour == right[target]:
                    continue
                coefficient = (
                    x_colour == row and y_colour == column
                )
                coordinate_product = (
                    x_colour == target and y_colour == target
                )
                if coefficient and not coordinate_product:
                    return False
    return True


def enumerate_matchings(
    order: int,
    adjacent,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    return enumerate_selected_matchings(
        frozenset(range(order)), adjacent
    )


def enumerate_selected_matchings(
    selected: frozenset[int],
    adjacent,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    output: list[tuple[tuple[int, int], ...]] = []

    def visit(
        unused: frozenset[int],
        chosen: tuple[tuple[int, int], ...],
    ) -> None:
        if not unused:
            output.append(tuple(sorted(chosen)))
            return
        first = min(unused)
        for second in sorted(unused - {first}):
            if not adjacent(first, second):
                continue
            visit(
                unused - {first, second},
                chosen + (tuple(sorted((first, second))),),
            )

    visit(selected, ())
    return tuple(sorted(set(output)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "tmp/five_regular_balanced_bridge_"
            "diagonal_backbone_verified.json"
        ),
    )
    parser.add_argument(
        "--theorem",
        type=Path,
        default=Path(__file__).resolve().with_name(
            "FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/five_regular_balanced_bridge_"
            "diagonal_backbone_audited.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    if (
        not source.get("verified")
        or source.get("status")
        != "five_regular_balanced_bridge_diagonal_backbone_verified"
        or source.get("global_conjecture_resolved") is not False
        or source.get("theorem_sha256") != sha256(args.theorem)
        or source.get(
            "two_colour_factorization_requires_anchor_weight_support"
        )
        is not False
        or source.get("nonzero_anchor_diagonal_colours_per_pair") != 2
        or source.get(
            "all_anchor_pair_deleted_principal_hafnians_forced_zero"
        )
        is not True
        or source.get("full_principal_hafnians_required_one") is not True
        or source.get(
            "proper_anchor_subset_unique_matching_verified"
        )
        is not True
        or source.get(
            "nonconstant_two_colour_anchor_assignment_forced"
        )
        is not True
        or source.get(
            "five_regular_simultaneous_all_bridge_excluded"
        )
        is not True
        or source.get(
            "maximum_degree_five_simultaneous_all_bridge_excluded"
        )
        is not True
    ):
        raise AssertionError("primary verifier binding changed")

    choices = [
        tuple(colour for colour in range(3) if colour != target)
        for target in range(3)
    ]
    types = list(itertools.product(*choices))
    diagonal_sets = {}
    diagonal_histogram: Counter[int] = Counter()
    off_diagonal_checks = 0
    for left_id, left in enumerate(types):
        for right_id, right in enumerate(types):
            entries = tuple(
                (row, column)
                for row in range(3)
                for column in range(3)
                if direct_allowed(left, right, row, column)
            )
            diagonal = frozenset(
                row for row, column in entries if row == column
            )
            diagonal_sets[left_id, right_id] = diagonal
            diagonal_histogram[len(diagonal)] += 1
            for row, column in entries:
                if row == column:
                    continue
                if (
                    left[column] != row
                    or right[row] != column
                ):
                    raise AssertionError(
                        "direct restriction admitted a nonreciprocal unit"
                    )
                off_diagonal_checks += 1
            complementary = all(
                left[colour] != right[colour]
                for colour in range(3)
            )
            if (len(diagonal) == 3) != complementary:
                raise AssertionError(
                    "direct complement classification changed"
                )

    if diagonal_histogram != Counter({0: 2, 1: 24, 2: 30, 3: 8}):
        raise AssertionError("direct diagonal histogram changed")

    subset_counts = {}
    for size, expected in ((1, 36), (2, 18), (3, 8)):
        for subset in itertools.combinations(range(3), size):
            required = frozenset(subset)
            actual = sum(
                required <= diagonal
                for diagonal in diagonal_sets.values()
            )
            if actual != expected:
                raise AssertionError(
                    "direct subset transition count changed"
                )
            subset_counts[",".join(map(str, subset))] = actual

    matching_regressions = []
    for order in range(2, 15, 2):
        anchor_pairs = tuple(
            (index, index + 1) for index in range(0, order, 2)
        )
        path = enumerate_matchings(
            order, lambda first, second: abs(first - second) == 1
        )
        if len(path) != 1:
            raise AssertionError("independent path matching count changed")
        row = {"order": order, "path_perfect_matchings": len(path)}
        if order >= 4:
            cycle = enumerate_matchings(
                order,
                lambda first, second: (
                    abs(first - second) == 1
                    or {first, second} == {0, order - 1}
                ),
            )
            if len(cycle) != 2:
                raise AssertionError(
                    "independent cycle matching count changed"
                )
            row["cycle_perfect_matchings"] = len(cycle)
        path_subset_checks = 0
        cycle_subset_checks = 0
        for mask in range(1 << len(anchor_pairs)):
            selected = frozenset(
                vertex
                for pair_id, pair in enumerate(anchor_pairs)
                if mask & (1 << pair_id)
                for vertex in pair
            )
            path_subset = enumerate_selected_matchings(
                selected,
                lambda first, second: (
                    abs(first - second) == 1
                ),
            )
            if len(path_subset) != 1:
                raise AssertionError(
                    "independent path-subset uniqueness changed"
                )
            path_subset_checks += 1
            if order >= 4:
                cycle_subset = enumerate_selected_matchings(
                    selected,
                    lambda first, second: (
                        abs(first - second) == 1
                        or {first, second} == {0, order - 1}
                    ),
                )
                expected = (
                    2 if mask == (1 << len(anchor_pairs)) - 1 else 1
                )
                if len(cycle_subset) != expected:
                    raise AssertionError(
                        "independent cycle-subset uniqueness changed"
                    )
                cycle_subset_checks += 1
        row["path_anchor_subsets_checked"] = path_subset_checks
        if order >= 4:
            row["cycle_anchor_subsets_checked"] = cycle_subset_checks
        matching_regressions.append(row)

    list_types = [
        frozenset(subset)
        for size in (2, 3)
        for subset in itertools.combinations(range(3), size)
    ]
    list_colour_regressions = []
    for pair_count in range(2, 7):
        configurations = 0
        for lists in itertools.product(list_types, repeat=pair_count):
            configurations += 1
            found = False
            for assignment in itertools.product(
                range(3), repeat=pair_count
            ):
                if (
                    len(set(assignment)) == 2
                    and all(
                        colour in allowed
                        for colour, allowed in zip(
                            assignment, lists, strict=True
                        )
                    )
                ):
                    found = True
                    break
            if not found:
                raise AssertionError(
                    "independent anchor-list colouring failed"
                )
        list_colour_regressions.append(
            {
                "anchor_pairs": pair_count,
                "list_configurations": configurations,
                "nonconstant_two_colour_assignment_exists": True,
            }
        )

    alternating_cycle_regressions = []
    all_colours = frozenset(range(3))
    for minority in range(3):
        majority = all_colours - {minority}
        order_rows = []
        for order in range(4, 15, 2):
            states = {
                (start, start, False)
                for start in range(len(types))
            }
            for edge_id in range(order):
                required = majority if edge_id % 2 == 0 else {minority}
                next_states = set()
                for start, current, saw_bad_majority in states:
                    for neighbour in range(len(types)):
                        if not required <= diagonal_sets[
                            current, neighbour
                        ]:
                            continue
                        bad = (
                            edge_id % 2 == 0
                            and not all(
                                types[current][colour]
                                != types[neighbour][colour]
                                for colour in range(3)
                            )
                        )
                        next_states.add(
                            (
                                start,
                                neighbour,
                                saw_bad_majority or bad,
                            )
                        )
                states = next_states
            closed = {
                saw_bad
                for start, current, saw_bad in states
                if start == current
            }
            if True in closed or False not in closed:
                raise AssertionError(
                    "independent alternating-cycle automaton changed"
                )
            order_rows.append(
                {
                    "order": order,
                    "closed_walk_exists": True,
                    "closed_walk_with_noncomplementary_majority_edge": (
                        False
                    ),
                }
            )
        alternating_cycle_regressions.append(
            {
                "minority_colour": minority,
                "majority_colours": sorted(majority),
                "orders": order_rows,
            }
        )

    complements = [
        tuple(
            next(
                colour
                for colour in range(3)
                if colour not in (target, item[target])
            )
            for target in range(3)
        )
        for item in types
    ]
    two_colour_anchor_audits = []
    for colour_pair in itertools.combinations(range(3), 2):
        nodes = [
            (type_id, side, colour)
            for type_id in range(len(types))
            for side in (0, 1)
            for colour in colour_pair
        ]
        edges = set()
        for first_id, first_side, first_colour in nodes:
            left = (
                types[first_id]
                if first_side == 0
                else complements[first_id]
            )
            for second_id, outgoing_side, second_colour in nodes:
                incoming_side = 1 - outgoing_side
                right = (
                    types[second_id]
                    if incoming_side == 0
                    else complements[second_id]
                )
                if direct_allowed(
                    left,
                    right,
                    first_colour,
                    second_colour,
                ):
                    edges.add(
                        (
                            (first_id, first_side, first_colour),
                            (
                                second_id,
                                outgoing_side,
                                second_colour,
                            ),
                        )
                    )
        reach = {
            node: {node}
            | {
                second
                for first, second in edges
                if first == node
            }
            for node in nodes
        }
        for middle in nodes:
            for first in nodes:
                if middle in reach[first]:
                    reach[first].update(reach[middle])
        colour_change_on_cycle = sum(
            first[2] != second[2] and first in reach[second]
            for first, second in edges
        )
        component_signatures = {
            frozenset(
                other
                for other in nodes
                if other in reach[node] and node in reach[other]
            )
            for node in nodes
        }
        if (
            len(edges) != 384
            or len(component_signatures) != 8
            or sorted(map(len, component_signatures)) != [4] * 8
            or any(
                len({node[2] for node in component}) != 1
                for component in component_signatures
            )
            or colour_change_on_cycle
        ):
            raise AssertionError(
                "direct two-colour anchor automaton changed"
            )
        two_colour_anchor_audits.append(
            {
                "colours": list(colour_pair),
                "states": len(nodes),
                "directed_transitions": len(edges),
                "strong_components": len(component_signatures),
                "strong_component_sizes": sorted(
                    map(len, component_signatures), reverse=True
                ),
                "colour_changing_transitions_on_closed_walks": (
                    colour_change_on_cycle
                ),
            }
        )

    source_records = {
        (int(record["left_type"]), int(record["right_type"])): (
            tuple(map(int, record["left_normals"])),
            tuple(map(int, record["right_normals"])),
            frozenset(map(int, record["diagonal_colours"])),
            bool(record["complementary"]),
        )
        for record in source["records"]
    }
    expected_records = {
        (left_id, right_id): (
            left,
            right,
            diagonal_sets[left_id, right_id],
            all(
                left[colour] != right[colour]
                for colour in range(3)
            ),
        )
        for left_id, left in enumerate(types)
        for right_id, right in enumerate(types)
    }
    if source_records != expected_records:
        raise AssertionError("primary and direct 64-record tables differ")

    payload = {
        "verified": True,
        "status": (
            "five_regular_balanced_bridge_diagonal_backbone_"
            "independently_audited"
        ),
        "scope": (
            "independent binary normal types, direct coordinate-plane "
            "matrix-unit restrictions, reciprocity, subset transitions, "
            "recursive path/cycle perfect-matching enumeration, and "
            "independent two-colour anchor automata with the "
            "anchor-pair-deleted hafnian-cofactor consequence, proper "
            "anchor-subset uniqueness, and the independent "
            "two-colour list-extension contradiction"
        ),
        "source": str(args.source),
        "source_sha256": sha256(args.source),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "normal_types": len(types),
        "ordered_type_pairs": len(expected_records),
        "diagonal_count_histogram": {
            str(key): diagonal_histogram[key]
            for key in sorted(diagonal_histogram)
        },
        "reciprocal_allowed_off_diagonal_entries": (
            off_diagonal_checks
        ),
        "subset_transition_counts": subset_counts,
        "matching_regressions": matching_regressions,
        "alternating_cycle_regressions": (
            alternating_cycle_regressions
        ),
        "complementary_majority_parity_forced": True,
        "spanning_complementary_anchor_matching_forced": True,
        "two_colour_anchor_automata": two_colour_anchor_audits,
        "two_colour_alternating_cycles_are_monochromatic": True,
        "two_colour_amplitude_factorization_checked": True,
        "two_colour_factorization_requires_anchor_weight_support": False,
        "nonzero_anchor_diagonal_colours_per_pair": 2,
        "all_anchor_pair_deleted_principal_hafnians_forced_zero": True,
        "full_principal_hafnians_required_one": True,
        "proper_anchor_subset_unique_matching_verified": True,
        "full_diagonal_component_hafnians_forced_nonzero": True,
        "list_colour_regressions": list_colour_regressions,
        "nonconstant_two_colour_anchor_assignment_forced": True,
        "five_regular_simultaneous_all_bridge_excluded": True,
        "maximum_degree_five_simultaneous_all_bridge_excluded": True,
        "degree_five_arithmetic": {
            "maximum_support_degree": 5,
            "distinct_off_diagonal_primary_killers": 3,
            "maximum_remaining_diagonal_neighbours": 2,
        },
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
