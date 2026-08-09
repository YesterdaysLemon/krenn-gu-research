"""Independent replay of the order-ten Kotzig/port minimum-layer census.

This program intentionally does not import either exploration program.
It uses a separate graph6 decoder, enumerates perfect one-factorizations
from direct perfect-matching lists, reconstructs normal types from
balanced five-subset masks, pairs reciprocal coloured tasks, and
recomputes minimum-potential colouring multiplicities.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import time
from pathlib import Path

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
NormalType = tuple[int, int, int]
ColouredEdge = tuple[int, int, int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def graph6_small(text: str) -> set[Edge]:
    values = [ord(character) - 63 for character in text.strip()]
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    answer: set[Edge] = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                answer.add((left, right))
            cursor += 1
    return answer


def degree_sequence(order: int, edges: set[Edge]) -> tuple[int, ...]:
    result = [0] * order
    for left, right in edges:
        result[left] += 1
        result[right] += 1
    return tuple(result)


def connected(order: int, edges: set[Edge]) -> bool:
    neighbours = [set() for _ in range(order)]
    for left, right in edges:
        neighbours[left].add(right)
        neighbours[right].add(left)
    seen = {0}
    boundary = [0]
    while boundary:
        vertex = boundary.pop()
        for other in neighbours[vertex] - seen:
            seen.add(other)
            boundary.append(other)
    return len(seen) == order


def perfect_matchings(
    order: int, allowed: set[Edge]
) -> list[Matching]:
    def extend(unused: tuple[int, ...]) -> list[Matching]:
        if not unused:
            return [()]
        root = unused[0]
        output: list[Matching] = []
        for offset, mate in enumerate(unused[1:], start=1):
            pair = (root, mate)
            if pair not in allowed:
                continue
            remainder = unused[1:offset] + unused[offset + 1 :]
            for tail in extend(remainder):
                output.append((pair, *tail))
        return output

    return sorted(set(extend(tuple(range(order)))))


def is_hamiltonian_cycle(order: int, edges: set[Edge]) -> bool:
    return (
        len(edges) == order
        and degree_sequence(order, edges) == (2,) * order
        and connected(order, edges)
    )


def kotzig_partitions(
    order: int, diagonal: set[Edge]
) -> list[tuple[Matching, Matching, Matching]]:
    matchings = perfect_matchings(order, diagonal)
    output: set[tuple[Matching, Matching, Matching]] = set()
    for first in matchings:
        first_set = set(first)
        for second in matchings:
            second_set = set(second)
            if first_set & second_set:
                continue
            third_set = diagonal - first_set - second_set
            if degree_sequence(order, third_set) != (1,) * order:
                continue
            third = tuple(sorted(third_set))
            factors = (first, second, third)
            if all(
                is_hamiltonian_cycle(
                    order, set(factors[a]) | set(factors[b])
                )
                for a, b in ((0, 1), (0, 2), (1, 2))
            ):
                output.add(factors)
    return sorted(output)


def balanced_normal_assignments(
    order: int,
    factors: tuple[Matching, Matching, Matching],
) -> list[tuple[NormalType, ...]]:
    balanced = tuple(
        frozenset(selection)
        for selection in itertools.combinations(
            range(order), order // 2
        )
    )
    bit_masks: list[list[frozenset[int]]] = []
    for bit in range(3):
        flip_edges = set().union(
            *(
                set(factors[colour])
                for colour in range(3)
                if colour != bit
            )
        )
        bit_masks.append(
            [
                mask
                for mask in balanced
                if all(
                    (left in mask) != (right in mask)
                    for left, right in flip_edges
                )
            ]
        )

    output = []
    for mask0, mask1, mask2 in itertools.product(*bit_masks):
        output.append(
            tuple(
                (
                    2 if vertex in mask0 else 1,
                    2 if vertex in mask1 else 0,
                    1 if vertex in mask2 else 0,
                )
                for vertex in range(order)
            )
        )
    return output


def independent_potential(
    normal: NormalType, colour: int
) -> int:
    first = int(normal[0] == 2)
    second = int(normal[1] == 2)
    third = int(normal[2] == 1)
    values = (
        1 - 2 * third,
        2 * third - 2 * first,
        2 * first + 2 * second - 2,
    )
    return values[colour]


def independently_allowed_unit(
    left: NormalType,
    right: NormalType,
    row: int,
    column: int,
) -> bool:
    for target in range(3):
        if (
            (row, column) != (target, target)
            and row != left[target]
            and column != right[target]
        ):
            return False
    return True


def minimum_multiplicities(
    order: int, edges: tuple[ColouredEdge, ...]
) -> dict[str, object]:
    incident: list[list[int]] = [[] for _ in range(order)]
    for edge_id, (left, right, _a, _b, _weight) in enumerate(edges):
        incident[left].append(edge_id)
        incident[right].append(edge_id)

    best: int | None = None
    counts: Counter[tuple[int, ...]] = Counter()
    all_matchings = 0
    mixed_matchings = 0
    colouring = [-1] * order

    def search(unused: frozenset[int], value: int) -> None:
        nonlocal best
        nonlocal all_matchings
        nonlocal mixed_matchings
        if not unused:
            all_matchings += 1
            row = tuple(colouring)
            if len(set(row)) == 1:
                return
            mixed_matchings += 1
            if best is None or value < best:
                best = value
                counts.clear()
            if value == best:
                counts[row] += 1
            return

        root = min(unused)
        for edge_id in incident[root]:
            left, right, first_colour, second_colour, weight = edges[
                edge_id
            ]
            if right == root:
                left, right = right, left
                first_colour, second_colour = (
                    second_colour,
                    first_colour,
                )
            if right not in unused:
                continue
            colouring[left] = first_colour
            colouring[right] = second_colour
            search(unused - {left, right}, value + weight)
            colouring[left] = -1
            colouring[right] = -1

    search(frozenset(range(order)), 0)
    if best is None or best > 0:
        raise AssertionError("independent minimum layer changed")
    histogram = Counter(counts.values())
    return {
        "perfect_matchings": all_matchings,
        "nonmonochromatic_matchings": mixed_matchings,
        "minimum_potential": best,
        "multiplicity_signature": tuple(sorted(histogram.items())),
        "has_unique_minimum": histogram.get(1, 0) > 0,
        "minimum_rows": dict(counts),
    }


def maximal_forced_singleton(
    order: int,
    edges: tuple[tuple[int, int, int, int, bool], ...],
) -> tuple[tuple[int, ...] | None, int]:
    incident: list[list[int]] = [[] for _ in range(order)]
    for edge_id, item in enumerate(edges):
        incident[item[0]].append(edge_id)
        incident[item[1]].append(edge_id)
    counts: Counter[tuple[int, ...]] = Counter()
    first_is_forced: dict[tuple[int, ...], bool] = {}
    colours = [-1] * order
    chosen: list[int] = []

    def search(unused: frozenset[int]) -> None:
        if not unused:
            row = tuple(colours)
            counts[row] += 1
            if counts[row] == 1:
                first_is_forced[row] = all(
                    edges[edge_id][4] for edge_id in chosen
                )
            return
        root = min(unused)
        for edge_id in incident[root]:
            left, right, first_colour, second_colour, _forced = (
                edges[edge_id]
            )
            if right == root:
                left, right = right, left
                first_colour, second_colour = (
                    second_colour,
                    first_colour,
                )
            if right not in unused:
                continue
            colours[left] = first_colour
            colours[right] = second_colour
            chosen.append(edge_id)
            search(unused - {left, right})
            chosen.pop()
            colours[left] = -1
            colours[right] = -1

    search(frozenset(range(order)))
    witness = next(
        (
            row
            for row, count in sorted(counts.items())
            if (
                count == 1
                and len(set(row)) > 1
                and first_is_forced[row]
            )
        ),
        None,
    )
    return witness, sum(counts.values())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=Path("tmp", "cub10.g6"),
    )
    parser.add_argument(
        "--primary",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_ports_explored.json",
        ),
    )
    parser.add_argument(
        "--theorem",
        type=Path,
        default=Path(
            "claims",
            "arbitrary-order",
            "THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md"
        ),
    )
    parser.add_argument(
        "--survivor-analysis",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_port_survivors_analyzed.json",
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_ports_audited.json",
        ),
    )
    parser.add_argument("--progress-every", type=int, default=25_000)
    args = parser.parse_args()
    started = time.perf_counter()
    order = 10

    rows = tuple(
        row.strip()
        for row in args.catalogue.read_text(
            encoding="ascii"
        ).splitlines()
        if row.strip()
    )
    graphs = tuple(graph6_small(row) for row in rows)
    if (
        len(graphs) != 19
        or len(set(rows)) != 19
        or any(
            degree_sequence(order, graph) != (3,) * order
            or not connected(order, graph)
            for graph in graphs
        )
    ):
        raise AssertionError(
            "order-ten connected cubic catalogue changed"
        )

    colouring_count = 0
    type_count = 0
    port_count = 0
    contradiction_count = 0
    guaranteed_matchings = 0
    mixed_guaranteed_matchings = 0
    potential_histogram: Counter[int] = Counter()
    multiplicity_histogram: Counter[
        tuple[tuple[int, int], ...]
    ] = Counter()
    graph_records = []
    survivors = []
    exact_minimum_binomials = 0
    zero_potential_cycles = 0
    cycle_length_histogram: Counter[int] = Counter()
    maximal_unique_contradictions = 0
    maximal_monomial_count_histogram: Counter[int] = Counter()
    maximal_residuals = []

    for graph_index, diagonal in enumerate(graphs):
        colourings = kotzig_partitions(order, diagonal)
        colouring_count += len(colourings)
        graph_ports = 0
        graph_contradictions = 0

        for colouring_index, factors in enumerate(colourings):
            assignments = balanced_normal_assignments(
                order, factors
            )
            if len(assignments) != 8:
                raise AssertionError(
                    "independent type-assignment count changed"
                )
            type_count += len(assignments)
            diagonal_edges = tuple(
                (
                    left,
                    right,
                    colour,
                    colour,
                    0,
                )
                for colour, matching in enumerate(factors)
                for left, right in matching
            )

            for type_index, normals in enumerate(assignments):
                unused_tasks = {
                    (vertex, colour)
                    for vertex in range(order)
                    for colour in range(3)
                }
                used_pairs: set[Edge] = set()
                chosen: list[ColouredEdge] = []

                def pair_tasks() -> None:
                    nonlocal port_count
                    nonlocal graph_ports
                    nonlocal contradiction_count
                    nonlocal graph_contradictions
                    nonlocal guaranteed_matchings
                    nonlocal mixed_guaranteed_matchings
                    nonlocal exact_minimum_binomials
                    nonlocal zero_potential_cycles
                    nonlocal maximal_unique_contradictions

                    if not unused_tasks:
                        port_count += 1
                        graph_ports += 1
                        layer = minimum_multiplicities(
                            order,
                            diagonal_edges + tuple(chosen),
                        )
                        guaranteed_matchings += int(
                            layer["perfect_matchings"]
                        )
                        mixed_guaranteed_matchings += int(
                            layer["nonmonochromatic_matchings"]
                        )
                        potential_histogram[
                            int(layer["minimum_potential"])
                        ] += 1
                        signature = tuple(
                            layer["multiplicity_signature"]
                        )
                        multiplicity_histogram[signature] += 1
                        if bool(layer["has_unique_minimum"]):
                            contradiction_count += 1
                            graph_contradictions += 1
                        else:
                            minimum_rows = dict(
                                layer["minimum_rows"]
                            )
                            if (
                                len(minimum_rows) != 1
                                or set(minimum_rows.values()) != {2}
                            ):
                                raise AssertionError(
                                    "independent survivor is not one binomial"
                                )
                            exact_minimum_binomials += 1
                            minimum_colouring = next(
                                iter(minimum_rows)
                            )
                            tagged_guaranteed = [
                                (*item, "D")
                                for item in diagonal_edges
                            ] + [
                                (*item, "K") for item in chosen
                            ]
                            compatible = [
                                item
                                for item in tagged_guaranteed
                                if (
                                    minimum_colouring[item[0]]
                                    == item[2]
                                    and minimum_colouring[item[1]]
                                    == item[3]
                                )
                            ]
                            degree = [0] * order
                            neighbours = [set() for _ in range(order)]
                            for item in compatible:
                                degree[item[0]] += 1
                                degree[item[1]] += 1
                                neighbours[item[0]].add(item[1])
                                neighbours[item[1]].add(item[0])
                            unseen = set(range(order))
                            cycles = []
                            while unseen:
                                root = min(unseen)
                                component = {root}
                                boundary = [root]
                                unseen.remove(root)
                                while boundary:
                                    vertex = boundary.pop()
                                    for other in (
                                        neighbours[vertex] & unseen
                                    ):
                                        unseen.remove(other)
                                        component.add(other)
                                        boundary.append(other)
                                if all(
                                    degree[vertex] == 2
                                    for vertex in component
                                ):
                                    cycles.append(component)
                            if len(cycles) != 1:
                                raise AssertionError(
                                    "independent minimum cycle count changed"
                                )
                            cycle = cycles[0]
                            cycle_edges = [
                                item
                                for item in compatible
                                if (
                                    item[0] in cycle
                                    and item[1] in cycle
                                )
                            ]
                            if (
                                len(cycle_edges) != len(cycle)
                                or {item[5] for item in cycle_edges}
                                != {"D", "K"}
                                or sum(
                                    item[4]
                                    for item in cycle_edges
                                    if item[5] == "K"
                                )
                                != 0
                            ):
                                raise AssertionError(
                                    "independent minimum cycle changed"
                                )
                            zero_potential_cycles += 1
                            cycle_length_histogram[len(cycle)] += 1

                            maximal_entries = [
                                (
                                    item[0],
                                    item[1],
                                    item[2],
                                    item[3],
                                    True,
                                )
                                for item in diagonal_edges
                            ]
                            for colour, matching in enumerate(
                                factors
                            ):
                                for left, right in matching:
                                    optional = [
                                        (row, column)
                                        for row in range(3)
                                        for column in range(3)
                                        if (
                                            row != column
                                            and independently_allowed_unit(
                                                normals[left],
                                                normals[right],
                                                row,
                                                column,
                                            )
                                        )
                                    ]
                                    if len(optional) > 1:
                                        raise AssertionError(
                                            "independent optional block changed"
                                        )
                                    maximal_entries.extend(
                                        (
                                            left,
                                            right,
                                            row,
                                            column,
                                            False,
                                        )
                                        for row, column in optional
                                    )
                            maximal_entries.extend(
                                (
                                    item[0],
                                    item[1],
                                    item[2],
                                    item[3],
                                    True,
                                )
                                for item in chosen
                            )
                            witness, monomial_count = (
                                maximal_forced_singleton(
                                    order,
                                    tuple(maximal_entries),
                                )
                            )
                            maximal_monomial_count_histogram[
                                monomial_count
                            ] += 1
                            if witness is None:
                                maximal_residuals.append(
                                    [
                                        graph_index,
                                        colouring_index,
                                        type_index,
                                    ]
                                )
                            else:
                                maximal_unique_contradictions += 1
                            survivors.append(
                                [
                                    graph_index,
                                    colouring_index,
                                    type_index,
                                    [
                                        [
                                            item[0],
                                            item[1],
                                            item[2],
                                            item[3],
                                        ]
                                        for item in chosen
                                    ],
                                ]
                            )
                        if (
                            args.progress_every > 0
                            and port_count % args.progress_every == 0
                        ):
                            print(
                                "ports",
                                port_count,
                                "survivors",
                                len(survivors),
                                "elapsed",
                                round(time.perf_counter() - started, 1),
                                flush=True,
                            )
                        return

                    vertex, colour = min(unused_tasks)
                    partner_colour = normals[vertex][colour]
                    for partner in range(order):
                        reciprocal = (partner, partner_colour)
                        pair = tuple(sorted((vertex, partner)))
                        if (
                            partner == vertex
                            or pair in diagonal
                            or pair in used_pairs
                            or reciprocal not in unused_tasks
                            or normals[partner][partner_colour]
                            != colour
                        ):
                            continue
                        if pair[0] == vertex:
                            target_colours = (
                                colour,
                                partner_colour,
                            )
                        else:
                            target_colours = (
                                partner_colour,
                                colour,
                            )
                        half_colours = (
                            target_colours[1],
                            target_colours[0],
                        )
                        if not independently_allowed_unit(
                            normals[pair[0]],
                            normals[pair[1]],
                            half_colours[0],
                            half_colours[1],
                        ):
                            continue
                        weight = (
                            independent_potential(
                                normals[pair[0]],
                                half_colours[0],
                            )
                            + independent_potential(
                                normals[pair[1]],
                                half_colours[1],
                            )
                        )
                        unused_tasks.remove((vertex, colour))
                        unused_tasks.remove(reciprocal)
                        used_pairs.add(pair)
                        chosen.append(
                            (
                                pair[0],
                                pair[1],
                                half_colours[0],
                                half_colours[1],
                                weight,
                            )
                        )
                        pair_tasks()
                        chosen.pop()
                        used_pairs.remove(pair)
                        unused_tasks.add(reciprocal)
                        unused_tasks.add((vertex, colour))

                pair_tasks()

        graph_records.append(
            {
                "graph_index": graph_index,
                "graph6": rows[graph_index],
                "kotzig_colourings": len(colourings),
                "reciprocal_port_realizations": graph_ports,
                "unique_minimum_contradictions": (
                    graph_contradictions
                ),
            }
        )

    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    observed = {
        "graph6_rows": len(graphs),
        "graphs": graph_records,
        "labelled_kotzig_colourings": colouring_count,
        "normal_type_assignments": type_count,
        "reciprocal_port_realizations": port_count,
        "unique_minimum_contradictions": contradiction_count,
        "total_guaranteed_matchings": guaranteed_matchings,
        "total_nonmonochromatic_guaranteed_matchings": (
            mixed_guaranteed_matchings
        ),
        "minimum_potential_histogram": {
            str(key): value
            for key, value in sorted(potential_histogram.items())
        },
        "minimum_colouring_multiplicity_histogram": [
            {
                "multiplicities": {
                    str(key): value for key, value in signature
                },
                "realizations": count,
            }
            for signature, count in sorted(
                multiplicity_histogram.items()
            )
        ],
        "survivors": len(survivors),
    }
    if primary.get("graph6_sha256") != sha256(args.catalogue):
        raise AssertionError("primary catalogue binding changed")
    if primary.get("theorem_sha256") != sha256(args.theorem):
        raise AssertionError("primary theorem binding changed")
    if any(primary.get(key) != value for key, value in observed.items()):
        raise AssertionError(
            "primary and independent order-ten censuses disagree"
        )
    if len(survivors) != primary.get("survivors"):
        raise AssertionError(
            "independent survivor count changed"
        )

    analysis = json.loads(
        args.survivor_analysis.read_text(encoding="utf-8")
    )
    analysis_observed = {
        "primary_survivors": len(survivors),
        "exact_minimum_binomials": exact_minimum_binomials,
        "zero_potential_alternating_cycles": (
            zero_potential_cycles
        ),
        "minimum_cycle_length_histogram": {
            str(key): value
            for key, value in sorted(
                cycle_length_histogram.items()
            )
        },
        "maximal_support_monomial_count_histogram": {
            str(key): value
            for key, value in sorted(
                maximal_monomial_count_histogram.items()
            )
        },
        "maximal_support_unique_forced_contradictions": (
            maximal_unique_contradictions
        ),
        "survivors": len(maximal_residuals),
    }
    if analysis.get("primary_sha256") != sha256(args.primary):
        raise AssertionError(
            "survivor analysis primary binding changed"
        )
    if analysis.get("theorem_sha256") != sha256(args.theorem):
        raise AssertionError(
            "survivor analysis theorem binding changed"
        )
    if any(
        analysis.get(key) != value
        for key, value in analysis_observed.items()
    ):
        raise AssertionError(
            "primary and independent survivor analyses disagree"
        )
    if maximal_residuals:
        raise AssertionError(
            "an order-ten maximal-support realization survived"
        )

    payload = {
        "verified": True,
        "status": "independent_finite_combinatorial_audit",
        "scope": (
            "order-ten connected cubic catalogue, direct Kotzig "
            "partitions, balanced masks, reciprocal task pairings, "
            "and minimum-potential guaranteed-colouring multiplicities"
        ),
        "catalogue_provenance": "nauty geng -cq -d3 -D3 10",
        "catalogue": str(args.catalogue),
        "catalogue_sha256": sha256(args.catalogue),
        **observed,
        **analysis_observed,
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "survivor_analysis": str(args.survivor_analysis),
        "survivor_analysis_sha256": sha256(
            args.survivor_analysis
        ),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "finite_branch_excluded": True,
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
