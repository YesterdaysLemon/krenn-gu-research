"""Analyze any residual order-ten Kotzig/port minimum-layer binomials.

Under the corrected reciprocal-port orientation the complete order-ten
census has no residual architectures.  The code remains a fail-closed
replay of the old second stage: if a future primary census does emit
residuals, it reconstructs their binomials and maximal-support layer.

1. reconstructs that exact two-term minimum coefficient;
2. verifies that its symmetric difference is one zero-potential
   alternating D/K cycle; and
3. enlarges every diagonal block by every optional off-diagonal unit
   permitted by the balanced bridge table, then searches the resulting
   maximal support for a nonmonochromatic colouring with exactly one
   monomial made entirely from forced units.

A forced monomial that remains unique in maximal support is a valid
contradiction for every actual optional-unit subset.
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
from collections import Counter
import hashlib
import json
import time
from pathlib import Path

NormalType = tuple[int, int, int]
EntryEdge = tuple[int, int, int, int, bool, str, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def transition_potential(
    normal: NormalType, colour: int
) -> int:
    b0 = int(normal[0] == 2)
    b1 = int(normal[1] == 2)
    b2 = int(normal[2] == 1)
    return (
        1 - 2 * b2,
        2 * (b2 - b0),
        2 * (b0 + b1 - 1),
    )[colour]


def allowed_unit(
    left: NormalType,
    right: NormalType,
    row: int,
    column: int,
) -> bool:
    return all(
        (row, column) == (target, target)
        or row == left[target]
        or column == right[target]
        for target in range(3)
    )


def enumerate_coloured_matchings(
    order: int, edges: tuple[EntryEdge, ...]
) -> tuple[
    Counter[tuple[int, ...]],
    dict[tuple[int, ...], tuple[int, ...]],
    dict[tuple[int, ...], bool],
]:
    adjacency: list[list[int]] = [[] for _ in range(order)]
    for edge_id, item in enumerate(edges):
        adjacency[item[0]].append(edge_id)
        adjacency[item[1]].append(edge_id)

    counts: Counter[tuple[int, ...]] = Counter()
    first_matching: dict[tuple[int, ...], tuple[int, ...]] = {}
    first_forced: dict[tuple[int, ...], bool] = {}
    colours = [-1] * order
    chosen: list[int] = []

    def visit(remaining: int) -> None:
        if remaining == 0:
            row = tuple(colours)
            counts[row] += 1
            if counts[row] == 1:
                first_matching[row] = tuple(chosen)
                first_forced[row] = all(
                    edges[edge_id][4] for edge_id in chosen
                )
            return

        low_bit = remaining & -remaining
        left = low_bit.bit_length() - 1
        for edge_id in adjacency[left]:
            (
                u,
                v,
                left_colour,
                right_colour,
                _forced,
                _kind,
                _potential,
            ) = edges[edge_id]
            if u != left:
                u, v = v, u
                left_colour, right_colour = (
                    right_colour,
                    left_colour,
                )
            if not remaining & (1 << v):
                continue
            colours[u] = left_colour
            colours[v] = right_colour
            chosen.append(edge_id)
            visit(remaining ^ (1 << u) ^ (1 << v))
            chosen.pop()
            colours[u] = -1
            colours[v] = -1

    visit((1 << order) - 1)
    return counts, first_matching, first_forced


def main() -> None:
    parser = argparse.ArgumentParser()
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
        default=REPO_ROOT / "claims/arbitrary-order/THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_port_survivors_analyzed.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    order = 10

    source = json.loads(args.primary.read_text(encoding="utf-8"))
    records = list(source["survivor_records"])
    if (
        source.get("reciprocal_port_realizations") != 374_544
        or source.get("survivors") != len(records)
        or source.get("finite_branch_excluded") is not (not records)
        or source.get("theorem_sha256") != sha256(args.theorem)
    ):
        raise AssertionError(
            "order-ten primary survivor binding changed"
        )

    minimum_binomials = 0
    zero_potential_cycles = 0
    maximal_unique_contradictions = 0
    cycle_length_histogram: Counter[int] = Counter()
    maximal_monomial_count_histogram: Counter[int] = Counter()
    contradiction_records = []
    residual_records = []

    for survivor_index, record in enumerate(records):
        normals = tuple(
            tuple(map(int, item)) for item in record["normal_types"]
        )
        guaranteed: list[EntryEdge] = []
        maximal: list[EntryEdge] = []

        for colour, matching in enumerate(
            record["diagonal_matchings"]
        ):
            for raw_pair in matching:
                left, right = map(int, raw_pair)
                own: EntryEdge = (
                    left,
                    right,
                    colour,
                    colour,
                    True,
                    "D",
                    0,
                )
                guaranteed.append(own)
                maximal.append(own)
                optional = [
                    (row, column)
                    for row in range(3)
                    for column in range(3)
                    if (
                        row != column
                        and allowed_unit(
                            normals[left],
                            normals[right],
                            row,
                            column,
                        )
                    )
                ]
                if len(optional) > 1:
                    raise AssertionError(
                        "diagonal block lost its at-most-one optional unit"
                    )
                for row, column in optional:
                    potential = (
                        transition_potential(normals[left], row)
                        + transition_potential(
                            normals[right], column
                        )
                    )
                    if potential <= 0:
                        raise AssertionError(
                            "optional diagonal unit lost positive potential"
                        )
                    maximal.append(
                        (
                            left,
                            right,
                            row,
                            column,
                            False,
                            "D_optional",
                            potential,
                        )
                    )

        for port in record["port_edges"]:
            left, right = map(int, port["edge"])
            left_colour, right_colour = map(
                int, port["half_colours"]
            )
            potential = (
                transition_potential(
                    normals[left], left_colour
                )
                + transition_potential(
                    normals[right], right_colour
                )
            )
            if potential != int(port["potential"]):
                raise AssertionError(
                    "recorded port potential changed"
                )
            item: EntryEdge = (
                left,
                right,
                left_colour,
                right_colour,
                True,
                "K",
                potential,
            )
            guaranteed.append(item)
            maximal.append(item)

        if len(guaranteed) != 30 or not 30 <= len(maximal) <= 45:
            raise AssertionError("order-ten edge-unit census changed")

        (
            guaranteed_counts,
            guaranteed_first,
            _guaranteed_forced,
        ) = enumerate_coloured_matchings(order, tuple(guaranteed))
        mixed_guaranteed = {
            colouring: count
            for colouring, count in guaranteed_counts.items()
            if len(set(colouring)) > 1
        }
        minimum = min(
            sum(
                transition_potential(normals[vertex], colour)
                for vertex, colour in enumerate(colouring)
            )
            for colouring in mixed_guaranteed
        )
        minimum_rows = {
            colouring: count
            for colouring, count in mixed_guaranteed.items()
            if sum(
                transition_potential(normals[vertex], colour)
                for vertex, colour in enumerate(colouring)
            )
            == minimum
        }
        if (
            len(minimum_rows) != 1
            or set(minimum_rows.values()) != {2}
            or minimum
            != int(
                record["minimum_layer"]["minimum_potential"]
            )
        ):
            raise AssertionError(
                "survivor is not one exact minimum-layer binomial"
            )
        minimum_binomials += 1

        minimum_colouring = next(iter(minimum_rows))
        compatible_ids = [
            edge_id
            for edge_id, item in enumerate(guaranteed)
            if (
                minimum_colouring[item[0]] == item[2]
                and minimum_colouring[item[1]] == item[3]
            )
        ]
        compatible = tuple(guaranteed[index] for index in compatible_ids)
        compatible_counts, _compatible_first, _compatible_forced = (
            enumerate_coloured_matchings(order, compatible)
        )
        if compatible_counts.get(minimum_colouring) != 2:
            raise AssertionError(
                "minimum filtered graph lost its two matchings"
            )

        degree = [0] * order
        neighbours = [set() for _ in range(order)]
        for item in compatible:
            degree[item[0]] += 1
            degree[item[1]] += 1
            neighbours[item[0]].add(item[1])
            neighbours[item[1]].add(item[0])
        unseen = set(range(order))
        cycle_components = []
        while unseen:
            root = min(unseen)
            component = {root}
            boundary = [root]
            unseen.remove(root)
            while boundary:
                vertex = boundary.pop()
                for other in neighbours[vertex] & unseen:
                    unseen.remove(other)
                    component.add(other)
                    boundary.append(other)
            if all(degree[vertex] == 2 for vertex in component):
                cycle_components.append(component)
        if len(cycle_components) != 1:
            raise AssertionError(
                "minimum binomial does not have exactly one cycle"
            )
        cycle_vertices = cycle_components[0]
        cycle_edges = [
            item
            for item in compatible
            if item[0] in cycle_vertices
            and item[1] in cycle_vertices
        ]
        if (
            len(cycle_edges) != len(cycle_vertices)
            or any(
                sum(vertex in (item[0], item[1]) for item in cycle_edges)
                != 2
                for vertex in cycle_vertices
            )
            or {
                item[5] for item in cycle_edges
            }
            != {"D", "K"}
        ):
            raise AssertionError(
                "minimum binomial is not one alternating D/K cycle"
            )
        k_potential = sum(
            item[6] for item in cycle_edges if item[5] == "K"
        )
        if k_potential != 0:
            raise AssertionError(
                "minimum cancellation cycle lost zero potential"
            )
        zero_potential_cycles += 1
        cycle_length_histogram[len(cycle_vertices)] += 1

        maximal_counts, maximal_first, maximal_forced = (
            enumerate_coloured_matchings(order, tuple(maximal))
        )
        maximal_monomial_count_histogram[
            sum(maximal_counts.values())
        ] += 1
        witness = next(
            (
                colouring
                for colouring, count in sorted(
                    maximal_counts.items()
                )
                if (
                    count == 1
                    and len(set(colouring)) > 1
                    and maximal_forced[colouring]
                )
            ),
            None,
        )
        if witness is None:
            residual_records.append(
                {
                    "survivor_index": survivor_index,
                    "graph_index": record["graph_index"],
                    "colouring_index": record["colouring_index"],
                    "type_index": record["type_index"],
                    "minimum_potential": minimum,
                    "minimum_colouring": list(minimum_colouring),
                    "minimum_cycle_length": len(cycle_vertices),
                }
            )
            continue

        maximal_unique_contradictions += 1
        matching_ids = maximal_first[witness]
        contradiction_records.append(
            {
                "survivor_index": survivor_index,
                "graph_index": record["graph_index"],
                "colouring_index": record["colouring_index"],
                "type_index": record["type_index"],
                "minimum_potential": minimum,
                "minimum_cycle_length": len(cycle_vertices),
                "maximal_unique_colouring": list(witness),
                "maximal_unique_matching": [
                    {
                        "edge": [
                            maximal[edge_id][0],
                            maximal[edge_id][1],
                        ],
                        "half_colours": [
                            maximal[edge_id][2],
                            maximal[edge_id][3],
                        ],
                        "kind": maximal[edge_id][5],
                    }
                    for edge_id in matching_ids
                ],
            }
        )

    payload = {
        "verified": len(residual_records) == 0,
        "status": "finite_survivor_analysis",
        "scope": (
            "the non-unique minimum-potential survivors of the "
            "order-ten exact-degree-six pairwise-disjoint Kotzig/port "
            "census, followed by maximal optional-D support"
        ),
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "primary_survivors": len(records),
        "exact_minimum_binomials": minimum_binomials,
        "zero_potential_alternating_cycles": zero_potential_cycles,
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
        "contradiction_records": contradiction_records,
        "survivors": len(residual_records),
        "survivor_records": residual_records,
        "finite_branch_excluded": len(residual_records) == 0,
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
