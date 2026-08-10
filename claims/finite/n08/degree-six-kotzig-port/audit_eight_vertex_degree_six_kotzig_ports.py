"""Independent replay of the order-eight Kotzig/port exclusion.

This program intentionally does not import
``explore_eight_vertex_degree_six_kotzig_ports``.  It uses a second graph6
decoder, validates the connected catalogue against the six-class nauty
catalogue, enumerates balanced type assignments by four-subset masks, pairs
reciprocal port tasks directly, and checks mixed amplitudes from scratch.
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
from pathlib import Path

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
NormalType = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def small_graph6(text: str) -> set[Edge]:
    values = [ord(character) - 63 for character in text.strip()]
    order = values.pop(0)
    bits = [
        (value >> shift) & 1
        for value in values
        for shift in range(5, -1, -1)
    ]
    result: set[Edge] = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                result.add((left, right))
            cursor += 1
    return result


def degrees(order: int, edges: set[Edge]) -> tuple[int, ...]:
    output = [0] * order
    for left, right in edges:
        output[left] += 1
        output[right] += 1
    return tuple(output)


def is_connected(order: int, edges: set[Edge]) -> bool:
    neighbours = [set() for _ in range(order)]
    for left, right in edges:
        neighbours[left].add(right)
        neighbours[right].add(left)
    found = {0}
    boundary = [0]
    while boundary:
        vertex = boundary.pop()
        for other in neighbours[vertex] - found:
            found.add(other)
            boundary.append(other)
    return len(found) == order


def isomorphic(first: set[Edge], second: set[Edge], order: int) -> bool:
    for permutation in itertools.permutations(range(order)):
        image = {
            tuple(sorted((permutation[left], permutation[right])))
            for left, right in first
        }
        if image == second:
            return True
    return False


def matching_list(order: int, allowed: set[Edge]) -> list[Matching]:
    def extend(unused: tuple[int, ...]) -> list[Matching]:
        if not unused:
            return [()]
        root = unused[0]
        answers = []
        for mate in unused[1:]:
            pair = tuple(sorted((root, mate)))
            if pair not in allowed:
                continue
            tail_vertices = tuple(
                vertex for vertex in unused if vertex not in (root, mate)
            )
            for tail in extend(tail_vertices):
                answers.append(tuple(sorted((pair, *tail))))
        return answers

    return sorted(set(extend(tuple(range(order)))))


def hamiltonian(order: int, edges: set[Edge]) -> bool:
    return len(edges) == order and degrees(order, edges) == (2,) * order and is_connected(
        order, edges
    )


def coloured_kotzig_partitions(
    order: int, diagonal: set[Edge]
) -> list[tuple[Matching, Matching, Matching]]:
    factors = matching_list(order, diagonal)
    answers = set()
    for red in factors:
        red_set = set(red)
        for green in factors:
            green_set = set(green)
            if red_set & green_set:
                continue
            blue_set = diagonal - red_set - green_set
            if degrees(order, blue_set) != (1,) * order:
                continue
            blue = tuple(sorted(blue_set))
            triple = (red, green, blue)
            if all(
                hamiltonian(order, set(triple[a]) | set(triple[b]))
                for a, b in ((0, 1), (0, 2), (1, 2))
            ):
                answers.add(triple)
    return sorted(answers)


def types_from_balanced_masks(
    order: int, factors: tuple[Matching, Matching, Matching]
) -> list[tuple[NormalType, ...]]:
    balanced_masks = [
        frozenset(vertices)
        for vertices in itertools.combinations(range(order), order // 2)
    ]
    choices: list[list[frozenset[int]]] = []
    for bit in range(3):
        flip_edges = set().union(
            *(set(factors[colour]) for colour in range(3) if colour != bit)
        )
        choices.append(
            [
                mask
                for mask in balanced_masks
                if all((left in mask) != (right in mask) for left, right in flip_edges)
            ]
        )
    answers = []
    for bit0, bit1, bit2 in itertools.product(*choices):
        row = []
        for vertex in range(order):
            row.append(
                (
                    2 if vertex in bit0 else 1,
                    2 if vertex in bit1 else 0,
                    1 if vertex in bit2 else 0,
                )
            )
        answers.append(tuple(row))
    return answers


def reciprocal_port_labelings(
    order: int, port_edges: set[Edge], types: tuple[NormalType, ...]
) -> list[dict[Edge, tuple[int, int]]]:
    neighbours = [set() for _ in range(order)]
    for left, right in port_edges:
        neighbours[left].add(right)
        neighbours[right].add(left)

    unused_tasks = {(vertex, colour) for vertex in range(order) for colour in range(3)}
    unused_edges = set(port_edges)
    chosen: dict[Edge, tuple[int, int]] = {}
    answers: list[dict[Edge, tuple[int, int]]] = []

    def search() -> None:
        if not unused_tasks:
            if not unused_edges:
                answers.append(dict(sorted(chosen.items())))
            return
        vertex, target = min(unused_tasks)
        partner_target = types[vertex][target]
        for partner in sorted(neighbours[vertex]):
            pair = tuple(sorted((vertex, partner)))
            reciprocal_task = (partner, partner_target)
            if (
                pair not in unused_edges
                or reciprocal_task not in unused_tasks
                or types[partner][partner_target] != target
            ):
                continue
            unused_tasks.remove((vertex, target))
            unused_tasks.remove(reciprocal_task)
            unused_edges.remove(pair)
            oriented_targets = (
                (target, partner_target)
                if pair[0] == vertex
                else (partner_target, target)
            )
            physical_unit = (
                oriented_targets[1],
                oriented_targets[0],
            )
            if physical_unit not in allowed_bridge_units(
                types[pair[0]], types[pair[1]]
            ):
                unused_edges.add(pair)
                unused_tasks.add(reciprocal_task)
                unused_tasks.add((vertex, target))
                continue
            chosen[pair] = physical_unit
            search()
            del chosen[pair]
            unused_edges.add(pair)
            unused_tasks.add(reciprocal_task)
            unused_tasks.add((vertex, target))

    search()
    canonical = {
        tuple((pair, targets) for pair, targets in sorted(answer.items())): answer
        for answer in answers
    }
    return list(canonical.values())


def allowed_bridge_units(left: NormalType, right: NormalType) -> set[tuple[int, int]]:
    answers = set()
    for row in range(3):
        for column in range(3):
            valid = True
            for target in range(3):
                valid &= (
                    (row == target and column == target)
                    or row == left[target]
                    or column == right[target]
                )
            if valid:
                answers.add((row, column))
    return answers


def unique_guaranteed_mixed_row(
    order: int,
    all_matchings: list[Matching],
    factors: tuple[Matching, Matching, Matching],
    types: tuple[NormalType, ...],
    ports: dict[Edge, tuple[int, int]],
) -> tuple[tuple[int, ...], Matching] | None:
    possible: dict[Edge, set[tuple[int, int]]] = {}
    forced: dict[Edge, set[tuple[int, int]]] = {}
    for colour, factor in enumerate(factors):
        for pair in factor:
            left, right = pair
            own = {(colour, colour)}
            possible[pair] = own | {
                unit
                for unit in allowed_bridge_units(types[left], types[right])
                if unit[0] != unit[1]
            }
            forced[pair] = own
    for pair, unit in ports.items():
        possible[pair] = {unit}
        forced[pair] = {unit}

    for row in itertools.product(range(3), repeat=order):
        if len(set(row)) == 1:
            continue
        active = []
        for factor in all_matchings:
            if all(
                (row[left], row[right]) in possible.get(pair, set())
                for pair in factor
                for left, right in (pair,)
            ):
                active.append(factor)
        if len(active) == 1 and all(
            (row[left], row[right]) in forced.get(pair, set())
            for pair in active[0]
            for left, right in (pair,)
        ):
            return tuple(row), active[0]
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connected-catalogue", type=Path, default=Path("tmp", "cub08.g6")
    )
    parser.add_argument(
        "--all-catalogue",
        type=Path,
        default=Path("tmp", "cub08_all_nauty.g6"),
    )
    parser.add_argument(
        "--primary",
        type=Path,
        default=Path("tmp", "eight_vertex_degree_six_kotzig_ports_explored.json"),
    )
    parser.add_argument(
        "--theorem",
        type=Path,
        default=HERE / "EIGHT_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp", "eight_vertex_degree_six_kotzig_ports_audited.json"),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    order = 8

    all_rows = [
        row.strip()
        for row in args.all_catalogue.read_text(encoding="ascii").splitlines()
        if row.strip()
    ]
    all_graphs = [small_graph6(row) for row in all_rows]
    if len(all_graphs) != 6 or any(
        degrees(order, graph) != (3,) * order for graph in all_graphs
    ):
        raise AssertionError("all-cubic nauty catalogue changed")
    if any(
        isomorphic(all_graphs[first], all_graphs[second], order)
        for first in range(len(all_graphs))
        for second in range(first)
    ):
        raise AssertionError("duplicate isomorphism class in all catalogue")

    connected_rows = [
        row.strip()
        for row in args.connected_catalogue.read_text(encoding="ascii").splitlines()
        if row.strip()
    ]
    connected_graphs = [small_graph6(row) for row in connected_rows]
    connected_from_all = [
        graph for graph in all_graphs if is_connected(order, graph)
    ]
    if len(connected_graphs) != 5 or len(connected_from_all) != 5:
        raise AssertionError("connected cubic class count changed")
    for graph in connected_graphs:
        if sum(isomorphic(graph, other, order) for other in connected_from_all) != 1:
            raise AssertionError("connected catalogues do not agree")

    complete = {(left, right) for left in range(order) for right in range(left + 1, order)}
    all_matchings = matching_list(order, complete)
    if len(all_matchings) != 105:
        raise AssertionError("perfect-matching census changed")

    colouring_count = 0
    type_count = 0
    unused_tests = 0
    port_tests = 0
    port_labelings = 0
    contradictions = 0
    missing_contradictions = []
    graph_colour_counts = []

    for graph_index, diagonal in enumerate(connected_graphs):
        colourings = coloured_kotzig_partitions(order, diagonal)
        graph_colour_counts.append(len(colourings))
        colouring_count += len(colourings)
        complement = complete - diagonal
        unused_matchings = matching_list(order, complement)
        for colouring_index, colouring in enumerate(colourings):
            assignments = types_from_balanced_masks(order, colouring)
            type_count += len(assignments)
            for type_index, types in enumerate(assignments):
                for unused_index, unused in enumerate(unused_matchings):
                    unused_tests += 1
                    port_graph = complement - set(unused)
                    port_tests += 1
                    labelings = reciprocal_port_labelings(order, port_graph, types)
                    port_labelings += len(labelings)
                    for labeling_index, labeling in enumerate(labelings):
                        witness = unique_guaranteed_mixed_row(
                            order, all_matchings, colouring, types, labeling
                        )
                        if witness is None:
                            missing_contradictions.append(
                                [
                                    graph_index,
                                    colouring_index,
                                    type_index,
                                    unused_index,
                                    labeling_index,
                                ]
                            )
                        else:
                            contradictions += 1

    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    if primary.get("theorem_sha256") != sha256(args.theorem):
        raise AssertionError("primary theorem binding changed")
    observed = {
        "graph6_rows": len(connected_graphs),
        "labelled_kotzig_colourings": colouring_count,
        "normal_type_assignments": type_count,
        "unused_matching_tests": unused_tests,
        "reciprocal_port_tests": port_tests,
        "reciprocal_port_realizations": port_labelings,
        "maximal_support_unique_mixed_contradictions": contradictions,
        "survivors": len(missing_contradictions),
    }
    if any(primary.get(key) != value for key, value in observed.items()):
        raise AssertionError("primary and independent census disagree")
    if missing_contradictions:
        raise AssertionError("a reciprocal-port realization survived")

    payload = {
        "verified": True,
        "status": "independent_finite_combinatorial_audit",
        "scope": (
            "independent order-eight connected cubic catalogue, Kotzig "
            "colourings, balanced masks, reciprocal task pairings, maximal "
            "bridge support, and unique guaranteed mixed monomials"
        ),
        "connected_catalogue": str(args.connected_catalogue),
        "connected_catalogue_sha256": sha256(args.connected_catalogue),
        "all_cubic_catalogue": str(args.all_catalogue),
        "all_cubic_catalogue_sha256": sha256(args.all_catalogue),
        "all_cubic_isomorphism_classes": len(all_graphs),
        "connected_cubic_isomorphism_classes": len(connected_graphs),
        "graph_kotzig_colouring_counts": graph_colour_counts,
        **observed,
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    payload["output"] = str(args.output)
    payload["output_sha256"] = sha256(args.output)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
