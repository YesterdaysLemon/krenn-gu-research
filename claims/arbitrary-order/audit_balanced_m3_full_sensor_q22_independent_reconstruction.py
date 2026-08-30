#!/usr/bin/env python3
"""Fresh finite-field reconstruction of the pinned q<=22 near-frontier ledger.

This audit intentionally imports no census, Kestrel, or repository research
module.  It rebuilds support options, exact finite-field ranks, one-step
loss events, complementary-ruling tests, and the min-plus screen from the
JSON input beside this file.  The input is a pinned data ledger, not a
derived output.  The audit is evidence for the finite screen only: it does
not prove the analytic bridge to the Krenn--Gu problem and does not promote
any theorem or global status.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


PRIME = 1_000_033
VERTICES = tuple(range(4))
PAIRS = tuple(itertools.combinations(VERTICES, 2))
DEFAULT_INPUT = Path(__file__).with_name(
    "balanced_m3_full_sensor_q22_near_frontier_input_v1.json"
)
EXPECTED_INPUT_SHA256 = (
    "d5b821a47f8164f56e1254e9400ff1875bab650ce5e64be3a0e191129bed541a"
)
EXPECTED_RECORDS_SHA256 = (
    "650e8ed6e2165a3066fc9ba1cda30709b9f6e24fe599a6860afb2b1deb471550"
)
EXPECTED_Q_HISTOGRAM = {20: 2, 21: 39, 22: 506}
EXPECTED_EXPLAINED_CELLS = 6_429
EXPECTED_MIN_BEST_HISTOGRAM = {20: 5, 21: 73, 22: 469}
EXPECTED_MIN_INDICES = (8, 36, 50, 142, 431)
EXPECTED_LINE_OPTION_TOTAL = 19_662
EXPECTED_LINE_OPTIONS_BY_KIND = {"triple": 15_913, "four": 3_749}
EXPECTED_NORMAL_TOTAL = {
    1: 2_779,
    2: 2_813,
    3: 2_773,
    4: 2_999,
    5: 2_771,
    6: 2_756,
    7: 2_771,
}
EXPECTED_PRODUCT_SUM = 1_994_316
EXPECTED_Q20_INDICES = (50, 142)
EXPECTED_EQUALITY_SIGNATURES = (
    (8, 9, 2, "subset-plane", (1, 1, 2, 1, 2, 2), ()),
    (36, 9, 2, "subset-plane", (1, 2, 1, 2, 1, 2), ()),
    (50, 3, 0, "subset-plane", (1, 3, 3, 3, 3, 4), ()),
    (50, 3, 2, "subset-plane", (1, 2, 3, 2, 3, 4), ()),
    (50, 3, 2, "subset-plane", (1, 3, 2, 3, 2, 4), ()),
    (50, 3, 4, "subset-plane", (1, 2, 2, 2, 2, 4), ()),
    (50, 3, 5, "subset-plane+crossratio", (1, 2, 2, 2, 2, 3), ((2, 3),)),
    (142, 0, 0, "subset-plane", (2, 3, 3, 4, 4, 4), ()),
    (431, 9, 2, "subset-plane", (1, 1, 2, 1, 2, 2), ()),
)


def finite_inverse(value: int) -> int:
    """Invert a nonzero residue in the independently chosen prime field."""

    return pow(int(value) % PRIME, PRIME - 2, PRIME)


def finite_rank(rows: list[list[int]] | list[tuple[int, ...]]) -> int:
    """Hand-written exact row reduction over F_PRIME."""

    if not rows:
        return 0
    matrix = [[int(value) % PRIME for value in row] for row in rows]
    row_count, column_count, pivot_row = len(matrix), len(matrix[0]), 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        scale = finite_inverse(matrix[pivot_row][column])
        matrix[pivot_row] = [value * scale % PRIME for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (left - scale * right) % PRIME
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def vector_rank(vectors: tuple[tuple[int, ...], ...] | list[tuple[int, ...]]) -> int:
    """Rank of a finite list of column vectors."""

    return finite_rank([list(row) for row in zip(*vectors)]) if vectors else 0


def structural_rank(masks: tuple[int, ...]) -> int:
    """Maximum matching size between blocks and allowed coordinates."""

    best = 0
    for size in range(1, min(3, len(masks)) + 1):
        found = False
        for blocks in itertools.combinations(range(len(masks)), size):
            for coordinates in itertools.combinations(range(3), size):
                for permutation in itertools.permutations(range(size)):
                    if all(
                        masks[blocks[index]]
                        & (1 << coordinates[permutation[index]])
                        for index in range(size)
                    ):
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if found:
            best = size
    return best


def probe_value(seed: int, coordinate: int) -> int:
    """Deterministic polynomial probe, independent of the source screen."""

    value = (
        pow(seed % PRIME, coordinate + 1, PRIME)
        + (7919 + 104729 * coordinate) * seed
        + 313 * coordinate
        + 97
    ) % PRIME
    return value or coordinate + 1


def proportional(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return vector_rank((left, right)) <= 1


def generic_vectors(masks: tuple[int, ...], seed: int) -> tuple[tuple[int, ...], ...]:
    """Find a deterministic generic point on the indicated support product."""

    for attempt in range(1, 80):
        vectors = []
        for block, mask in enumerate(masks):
            coordinates = [c for c in range(3) if mask & (1 << c)]
            values = [
                probe_value(seed + 1009 * attempt + 313 * block, coordinate)
                for coordinate in coordinates
            ]
            vector = [0, 0, 0]
            for coordinate, value in zip(coordinates, values, strict=True):
                vector[coordinate] = value
            vectors.append(tuple(vector))
        if (
            len(set(vectors)) == len(vectors)
            and all(not proportional(left, right) for left, right in itertools.combinations(vectors, 2))
            and vector_rank(vectors) == structural_rank(masks)
        ):
            return tuple(vectors)
    raise AssertionError(("generic sample failed", masks, seed))


def generic_samples(
    masks: tuple[int, ...], seed: int, count: int = 3
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    return tuple(
        generic_vectors(masks, seed + 99_991 * index) for index in range(count)
    )


def normal_vector(mask: int, seed: int) -> tuple[int, ...]:
    return tuple(
        0
        if not (mask & (1 << coordinate))
        else (
            pow(seed % PRIME, coordinate + 1, PRIME)
            + 17 * seed
            + 1009 * coordinate
            + 313
        )
        % PRIME
        or coordinate + 2
        for coordinate in range(3)
    )


def null_basis(mask: int, normal: tuple[int, ...]) -> list[tuple[int, ...]]:
    coordinates = [c for c in range(3) if mask & (1 << c)]
    restricted = [normal[c] % PRIME for c in coordinates]
    pivot = next((index for index, value in enumerate(restricted) if value), None)
    if pivot is None:
        return [
            tuple(1 if row == coordinate else 0 for row in range(3))
            for coordinate in coordinates
        ]
    pivot_coordinate = coordinates[pivot]
    basis = []
    for coordinate in coordinates:
        if coordinate == pivot_coordinate:
            continue
        vector = [0, 0, 0]
        vector[coordinate] = 1
        vector[pivot_coordinate] = (
            -normal[coordinate] * finite_inverse(normal[pivot_coordinate])
        ) % PRIME
        basis.append(tuple(vector))
    return basis


def incidence_vectors(
    masks: tuple[int, ...],
    selected: tuple[int, ...],
    normal_mask: int,
    seed: int,
):
    selected_set = set(selected)
    for attempt in range(1, 160):
        normal = normal_vector(normal_mask, seed + 811 * attempt)
        bases = []
        for block, mask in enumerate(masks):
            if block in selected_set:
                bases.append(null_basis(mask, normal))
            else:
                bases.append(
                    [
                        tuple(1 if row == coordinate else 0 for row in range(3))
                        for coordinate in range(3)
                        if mask & (1 << coordinate)
                    ]
                )
        if any(not basis for basis in bases):
            continue
        vectors = []
        for block, basis in enumerate(bases):
            values = [
                probe_value(seed + 313 * attempt + 577 * block, index)
                for index in range(len(basis))
            ]
            vectors.append(
                tuple(
                    sum(values[index] * basis[index][row] for index in range(len(basis)))
                    % PRIME
                    for row in range(3)
                )
            )
        if any(proportional(left, right) for left, right in itertools.combinations(vectors, 2)):
            continue
        if vector_rank(tuple(vectors[index] for index in selected)) != 2:
            continue
        yield tuple(vectors)


def incidence_codimension(
    masks: tuple[int, ...], selected: tuple[int, ...], normal_mask: int
) -> int | None:
    base = sum(mask.bit_count() - 1 for mask in masks)
    selected_set = set(selected)
    dimension = normal_mask.bit_count() - 1
    for block, mask in enumerate(masks):
        if block not in selected_set:
            dimension += mask.bit_count() - 1
        else:
            intersection = mask.bit_count() - int(bool(mask & normal_mask))
            if intersection <= 0:
                return None
            dimension += intersection - 1
    value = base - dimension
    return value if value >= 0 else None


def options(
    masks: tuple[int, ...], partition: tuple[int, ...], seed: int
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = [
        {"selected": (), "normal": 0, "codim": 0, "samples": generic_samples(masks, seed)}
    ]
    selected_sets = list(itertools.combinations(range(len(masks)), 3))
    if len(masks) == 4:
        selected_sets.append(tuple(range(4)))
    for selected_index, selected in enumerate(selected_sets):
        if structural_rank(tuple(masks[index] for index in selected)) <= 2:
            continue
        for normal_mask in range(1, 8):
            codim = incidence_codimension(masks, selected, normal_mask)
            if codim is None:
                continue
            samples = tuple(
                itertools.islice(
                    incidence_vectors(
                        masks,
                        selected,
                        normal_mask,
                        seed + 10_007 * selected_index + 1009 * normal_mask,
                    ),
                    3,
                )
            )
            if samples:
                result.append(
                    {
                        "selected": selected,
                        "normal": normal_mask,
                        "codim": codim,
                        "samples": samples,
                    }
                )
    for option in result:
        option["masks"] = masks
        option["partition"] = partition
        option["charts"] = tuple(
            tuple(sample[partition[coordinate]] for coordinate in range(4))
            for sample in option["samples"]
        )
        option["crossratio"] = (
            len(set(partition)) == 4
            and any(vector_rank(chart) == 2 for chart in option["charts"])
        )
    return result


def edge_rank(
    left: tuple[tuple[int, ...], ...], right: tuple[tuple[int, ...], ...]
) -> int:
    rows = [
        tuple(
            left[chart][coordinate] * right[chart][index] % PRIME
            for coordinate in range(3)
            for index in range(3)
        )
        for chart in VERTICES
    ]
    return vector_rank(tuple(rows))


def edge_matrix(
    left_options: list[dict[str, object]], right_options: list[dict[str, object]]
) -> np.ndarray:
    return np.array(
        [
            [
                max(
                    edge_rank(left, right)
                    for left, right in itertools.product(
                        left_option["charts"], right_option["charts"]
                    )
                )
                for right_option in right_options
            ]
            for left_option in left_options
        ],
        dtype=np.int8,
    )


def forced_collinear(option: dict[str, object], blocks: tuple[int, ...]) -> bool:
    blocks = tuple(sorted(set(blocks)))
    if len(blocks) < 3:
        return False
    masks = option["masks"]
    if structural_rank(tuple(masks[index] for index in blocks)) <= 2:
        return True
    if not option["selected"]:
        return False
    forced = set(option["selected"]) | {
        index
        for index, mask in enumerate(masks)
        if mask & int(option["normal"]) == 0
    }
    return set(blocks) <= forced


def repeated_pair(partition: tuple[int, ...]) -> tuple[int, int] | None:
    if len(set(partition)) != 3:
        return None
    pairs = [
        pair
        for pair in itertools.combinations(range(4), 2)
        if partition[pair[0]] == partition[pair[1]]
    ]
    assert len(pairs) == 1
    return pairs[0]


def complementary_ruling(
    left: dict[str, object], right: dict[str, object]
) -> bool:
    left_pair = repeated_pair(left["partition"])
    right_pair = repeated_pair(right["partition"])
    if (
        left_pair is None
        or right_pair is None
        or set(left_pair) & set(right_pair)
        or set(left_pair) | set(right_pair) != set(range(4))
    ):
        return False
    return forced_collinear(left, left["partition"]) and forced_collinear(
        right, right["partition"]
    )


def event_upper(
    left: dict[str, object], right: dict[str, object], generic_rank: int
) -> tuple[int, tuple[str, ...]]:
    edges = tuple(sorted(set(zip(left["partition"], right["partition"]))))
    upper = min(generic_rank, len(edges))
    mechanisms: list[str] = []
    left_blocks = tuple(edge[0] for edge in edges)
    right_blocks = tuple(edge[1] for edge in edges)
    if len(set(left_blocks)) == 1:
        value = structural_rank(tuple(right["masks"][index] for index in right_blocks))
        if forced_collinear(right, right_blocks):
            value = min(value, 2)
        if value < upper:
            upper, mechanisms = value, mechanisms + ["fixed-left"]
    if len(set(right_blocks)) == 1:
        value = structural_rank(tuple(left["masks"][index] for index in left_blocks))
        if forced_collinear(left, left_blocks):
            value = min(value, 2)
        if value < upper:
            upper, mechanisms = value, mechanisms + ["fixed-right"]
    if generic_rank == 4 and complementary_ruling(left, right):
        upper = min(upper, 3)
        mechanisms.append("complementary-ruling")
    circuits = []
    for indices in itertools.combinations(range(len(edges)), 3):
        lefts = tuple(edges[index][0] for index in indices)
        rights = tuple(edges[index][1] for index in indices)
        if len(set(lefts)) == 1 and forced_collinear(right, rights):
            circuits.append(indices)
        if len(set(rights)) == 1 and forced_collinear(left, lefts):
            circuits.append(indices)
    if circuits:
        upper = min(upper, len(edges) - 1)
        mechanisms.append("three-point")
    if len(set(circuits)) >= 2:
        upper = min(upper, 2)
        mechanisms.append("two-three")
    return upper, tuple(mechanisms)


def all_set_partitions(values: tuple[int, ...]):
    if not values:
        yield ()
        return
    first, *rest = values
    for partition in all_set_partitions(tuple(rest)):
        yield ((first,),) + partition
        for index in range(len(partition)):
            yield (
                partition[:index]
                + (((first,) + partition[index]),)
                + partition[index + 1 :]
            )


def unique_set_partitions(values: tuple[int, ...]):
    seen = set()
    for partition in all_set_partitions(values):
        canonical = tuple(
            sorted(
                (tuple(sorted(block)) for block in partition),
                key=lambda block: block[0],
            )
        )
        if canonical not in seen:
            seen.add(canonical)
            yield canonical


def crossratio_candidate_cost(
    cost: np.ndarray,
    matrices: dict[tuple[int, int], np.ndarray],
    options_by_vertex: list[list[dict[str, object]]],
) -> int:
    all_indices = tuple(np.arange(size) for size in cost.shape)
    eligible = tuple(
        np.array(
            [index for index, option in enumerate(options_by_vertex[vertex]) if option["crossratio"]],
            dtype=int,
        )
        for vertex in VERTICES
    )
    best = int(cost.min())
    for equivalence in unique_set_partitions(VERTICES):
        nontrivial = tuple(block for block in equivalence if len(block) > 1)
        if not nontrivial:
            continue
        involved = {vertex for block in nontrivial for vertex in block}
        if any(len(eligible[vertex]) == 0 for vertex in involved):
            continue
        indices = tuple(
            eligible[vertex] if vertex in involved else all_indices[vertex]
            for vertex in VERTICES
        )
        candidate = cost[np.ix_(*indices)].astype(np.int16, copy=True)
        candidate += sum(len(block) - 1 for block in nontrivial)
        for block in nontrivial:
            for left, right in itertools.combinations(block, 2):
                pair = tuple(sorted((left, right)))
                restricted = matrices[pair][np.ix_(indices[left], indices[right])]
                candidate -= (restricted == 4).astype(np.int16).reshape(
                    tuple(
                        restricted.shape[0]
                        if coordinate == pair[0]
                        else restricted.shape[1]
                        if coordinate == pair[1]
                        else 1
                        for coordinate in VERTICES
                    )
                )
        best = min(best, int(candidate.min()))
    return best


def equality_descriptors(
    record: dict[str, object], record_index: int
) -> list[dict[str, object]]:
    """Independently reconstruct every value-20 event stratum in one record."""

    partitions = tuple(tuple(values) for values in record["partitions"])
    masks = tuple(tuple(values) for values in record["support_masks_by_vertex_block"])
    options_by_vertex = [
        options(
            masks[vertex],
            partitions[vertex],
            1009 * (record_index + 1) + 113 * vertex,
        )
        for vertex in VERTICES
    ]
    shape = tuple(len(values) for values in options_by_vertex)
    matrices = {
        pair: edge_matrix(options_by_vertex[pair[0]], options_by_vertex[pair[1]])
        for pair in PAIRS
    }
    delta = sum(record["delta_by_vertex"])
    cost = np.full(shape, delta, dtype=np.int16)
    for vertex in VERTICES:
        cost += np.array(
            [option["codim"] for option in options_by_vertex[vertex]],
            dtype=np.int16,
        ).reshape(
            tuple(
                len(options_by_vertex[vertex]) if coordinate == vertex else 1
                for coordinate in VERTICES
            )
        )
    for (left, right), matrix in matrices.items():
        cost += matrix.reshape(
            tuple(
                matrix.shape[0]
                if coordinate == left
                else matrix.shape[1]
                if coordinate == right
                else 1
                for coordinate in VERTICES
            )
        )

    def describe(
        indices: tuple[int, int, int, int],
        kind: str,
        cross_classes: tuple[tuple[int, ...], ...] = (),
    ) -> dict[str, object]:
        selected_options = tuple(
            options_by_vertex[vertex][indices[vertex]] for vertex in VERTICES
        )
        ranks = [
            int(matrices[pair][indices[pair[0]], indices[pair[1]]])
            for pair in PAIRS
        ]
        cross_cost = sum(len(block) - 1 for block in cross_classes)
        for block in cross_classes:
            for left, right in itertools.combinations(block, 2):
                pair_index = PAIRS.index(tuple(sorted((left, right))))
                if ranks[pair_index] == 4:
                    ranks[pair_index] -= 1
        plane_codimension = sum(int(option["codim"]) for option in selected_options)
        c_rank = plane_codimension + cross_cost
        assert delta + c_rank + sum(ranks) == 20
        return {
            "record_index": record_index,
            "type": kind,
            "Delta": delta,
            "c_rank": c_rank,
            "effective_ranks_01_02_03_12_13_23": tuple(ranks),
            "crossratio_classes": cross_classes,
            "line_vertices": tuple(
                vertex
                for vertex, option in enumerate(selected_options)
                if option["selected"]
            ),
            "option_indices": indices,
        }

    descriptors = [
        describe(tuple(int(value) for value in indices), "subset-plane")
        for indices in np.argwhere(cost == 20)
    ]
    all_indices = tuple(np.arange(size) for size in shape)
    eligible = tuple(
        np.array(
            [
                index
                for index, option in enumerate(options_by_vertex[vertex])
                if option["crossratio"]
            ],
            dtype=int,
        )
        for vertex in VERTICES
    )
    for equivalence in unique_set_partitions(VERTICES):
        nontrivial = tuple(block for block in equivalence if len(block) > 1)
        if not nontrivial:
            continue
        involved = {vertex for block in nontrivial for vertex in block}
        if any(len(eligible[vertex]) == 0 for vertex in involved):
            continue
        indices_by_vertex = tuple(
            eligible[vertex] if vertex in involved else all_indices[vertex]
            for vertex in VERTICES
        )
        candidate = cost[np.ix_(*indices_by_vertex)].astype(np.int16, copy=True)
        candidate += sum(len(block) - 1 for block in nontrivial)
        candidate_shape = tuple(len(indices) for indices in indices_by_vertex)
        for block in nontrivial:
            for left, right in itertools.combinations(block, 2):
                pair = tuple(sorted((left, right)))
                restricted = matrices[pair][
                    np.ix_(indices_by_vertex[left], indices_by_vertex[right])
                ]
                candidate -= (restricted == 4).astype(np.int16).reshape(
                    tuple(
                        restricted.shape[0]
                        if coordinate == pair[0]
                        else restricted.shape[1]
                        if coordinate == pair[1]
                        else 1
                        for coordinate in VERTICES
                    )
                )
        for local in np.argwhere(candidate == 20):
            local_indices = tuple(int(value) for value in local)
            global_indices = tuple(
                int(indices_by_vertex[vertex][local_indices[vertex]])
                for vertex in VERTICES
            )
            assert len(global_indices) == len(candidate_shape)
            descriptors.append(
                describe(
                    global_indices,
                    "subset-plane+crossratio",
                    nontrivial,
                )
            )
    return sorted(
        descriptors,
        key=lambda item: (
            item["record_index"],
            item["c_rank"],
            item["type"],
            item["effective_ranks_01_02_03_12_13_23"],
            item["crossratio_classes"],
        ),
    )


def equality_signature(descriptor: dict[str, object]):
    return (
        descriptor["record_index"],
        descriptor["Delta"],
        descriptor["c_rank"],
        descriptor["type"],
        descriptor["effective_ranks_01_02_03_12_13_23"],
        descriptor["crossratio_classes"],
    )


def permute_vertex_record(
    record: dict[str, object], new_to_old: tuple[int, int, int, int]
) -> dict[str, object]:
    """Relabel common vertices while leaving the four chart labels fixed."""

    old_to_new = {old: new for new, old in enumerate(new_to_old)}
    old_ranks = {
        pair: int(rank)
        for pair, rank in zip(
            PAIRS, record["ranks_01_02_03_12_13_23"], strict=True
        )
    }
    return {
        "selectors": [
            [old_to_new[int(value)] for value in selector]
            for selector in record["selectors"]
        ],
        "partitions": [record["partitions"][old] for old in new_to_old],
        "support_masks_by_vertex_block": [
            record["support_masks_by_vertex_block"][old] for old in new_to_old
        ],
        "delta_by_vertex": [record["delta_by_vertex"][old] for old in new_to_old],
        "ranks_01_02_03_12_13_23": [
            old_ranks[tuple(sorted((new_to_old[left], new_to_old[right])))]
            for left, right in PAIRS
        ],
    }


def vertex_record_projection(record: dict[str, object]) -> dict[str, object]:
    return {
        key: record[key]
        for key in (
            "selectors",
            "partitions",
            "support_masks_by_vertex_block",
            "delta_by_vertex",
            "ranks_01_02_03_12_13_23",
        )
    }


def audit_declared_equality_symmetries(
    data: dict[str, object], descriptors: list[dict[str, object]]
) -> dict[str, object]:
    swap_two_three = (0, 1, 3, 2)
    records = data["records"]
    assert permute_vertex_record(records[8], swap_two_three) == vertex_record_projection(
        records[36]
    )
    assert permute_vertex_record(records[50], swap_two_three) == vertex_record_projection(
        records[50]
    )
    record_8_line = next(
        item["line_vertices"] for item in descriptors if item["record_index"] == 8
    )
    record_36_line = next(
        item["line_vertices"] for item in descriptors if item["record_index"] == 36
    )
    assert record_8_line == (3,) and record_36_line == (2,)
    record_50_one_lines = {
        item["line_vertices"]
        for item in descriptors
        if item["record_index"] == 50 and item["c_rank"] == 2
    }
    assert record_50_one_lines == {(2,), (3,)}
    declared_orbit_count = len(descriptors) - 2
    assert len(descriptors) == 9 and declared_orbit_count == 7
    return {
        "record_8_to_36_vertex_permutation": swap_two_three,
        "record_50_one_line_vertex_permutation": swap_two_three,
        "equality_strata": len(descriptors),
        "declared_orbits": declared_orbit_count,
    }


def screen_record(
    record: dict[str, object], index: int
) -> tuple[tuple[int, ...], int, int, int, list[list[dict[str, object]]]]:
    partitions = tuple(tuple(values) for values in record["partitions"])
    masks = tuple(tuple(values) for values in record["support_masks_by_vertex_block"])
    options_by_vertex = [
        options(masks[vertex], partitions[vertex], 1009 * (index + 1) + 113 * vertex)
        for vertex in VERTICES
    ]
    shape = tuple(len(values) for values in options_by_vertex)
    matrices = {
        pair: edge_matrix(options_by_vertex[pair[0]], options_by_vertex[pair[1]])
        for pair in PAIRS
    }
    expected = tuple(record["ranks_01_02_03_12_13_23"])
    got = tuple(int(matrices[pair][0, 0]) for pair in PAIRS)
    assert got == expected, ("base rank mismatch", index, got, expected)
    explained = ruling = 0
    for pair_index, pair in enumerate(PAIRS):
        for left_index, left in enumerate(options_by_vertex[pair[0]]):
            for right_index, right in enumerate(options_by_vertex[pair[1]]):
                upper, why = event_upper(left, right, expected[pair_index])
                sampled = int(matrices[pair][left_index, right_index])
                assert sampled == upper, (
                    "unexplained event",
                    index,
                    pair,
                    left_index,
                    right_index,
                    sampled,
                    upper,
                    why,
                )
                if sampled < expected[pair_index]:
                    explained += 1
                    if "complementary-ruling" in why:
                        ruling += 1
    delta = sum(record["delta_by_vertex"])
    cost = np.full(shape, delta, dtype=np.int16)
    for vertex in VERTICES:
        cost += np.array(
            [option["codim"] for option in options_by_vertex[vertex]], dtype=np.int16
        ).reshape(
            tuple(
                len(options_by_vertex[vertex]) if coordinate == vertex else 1
                for coordinate in VERTICES
            )
        )
    for (left, right), matrix in matrices.items():
        cost += matrix.reshape(
            tuple(
                matrix.shape[0]
                if coordinate == left
                else matrix.shape[1]
                if coordinate == right
                else 1
                for coordinate in VERTICES
            )
        )
    best = int(cost.min())
    best = crossratio_candidate_cost(cost, matrices, options_by_vertex)
    return shape, explained, ruling, best, options_by_vertex


def update_option_census(
    census: dict[str, object], record: dict[str, object], options_by_vertex: list[list[dict[str, object]]]
) -> None:
    q = int(record["q"])
    by_kind: Counter[str] = census["line_options_by_kind"]
    by_kind_q: dict[int, Counter[str]] = census["line_options_by_q"]
    normal_total: Counter[int] = census["normal_total"]
    normal_by_q: dict[int, Counter[int]] = census["normal_by_q"]
    eligible: Counter[str] = census["crossratio_eligible_options"]
    eligible_by_q: dict[int, Counter[str]] = census["crossratio_eligible_by_q"]
    for vertex_options in options_by_vertex:
        for option in vertex_options[1:]:
            kind = "four" if len(option["selected"]) == 4 else "triple"
            by_kind[kind] += 1
            by_kind_q[q][kind] += 1
            normal = int(option["normal"])
            normal_total[normal] += 1
            normal_by_q[q][normal] += 1
            eligible["crossratio"] += int(bool(option["crossratio"]))
            eligible_by_q[q]["crossratio"] += int(bool(option["crossratio"]))
        eligible["options"] += sum(int(bool(option["crossratio"])) for option in vertex_options)
        eligible_by_q[q]["options"] += sum(
            int(bool(option["crossratio"])) for option in vertex_options
        )
    shape = tuple(len(values) for values in options_by_vertex)
    census["state_shape_hist"][shape] += 1
    census["vertex_product_sum"] += math.prod(shape)
    census["vertex_product_hist"][math.prod(shape)] += 1


def serialise_counter(counter: Counter) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def load_input(path: Path) -> tuple[dict[str, object], str, str]:
    raw = path.read_bytes()
    raw_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw.decode("utf-8"))
    records_sha = hashlib.sha256(
        json.dumps(data["records"], sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    assert raw_sha == EXPECTED_INPUT_SHA256, (raw_sha, EXPECTED_INPUT_SHA256)
    assert records_sha == EXPECTED_RECORDS_SHA256, (records_sha, EXPECTED_RECORDS_SHA256)
    assert len(data["records"]) == 547
    assert data["near_frontier_count"] == 547
    assert data["near_frontier_histogram"] == {"20": 2, "21": 39, "22": 506}
    return data, raw_sha, records_sha


def run(path: Path, progress: bool) -> dict[str, object]:
    data, input_sha, records_sha = load_input(path)
    shape_hist: Counter[tuple[int, ...]] = Counter()
    explained = ruling = ruling_records = 0
    best_hist: Counter[int] = Counter()
    best_records = []
    q20_records = []
    equality_components = []
    census: dict[str, object] = {
        "line_options_by_kind": Counter(),
        "line_options_by_q": defaultdict(Counter),
        "normal_total": Counter(),
        "normal_by_q": defaultdict(Counter),
        "crossratio_eligible_options": Counter(),
        "crossratio_eligible_by_q": defaultdict(Counter),
        "state_shape_hist": Counter(),
        "vertex_product_sum": 0,
        "vertex_product_hist": Counter(),
    }
    started = time.time()
    for index, record in enumerate(data["records"]):
        shape, cells, ruling_cells, best, options_by_vertex = screen_record(record, index)
        shape_hist[shape] += 1
        explained += cells
        ruling += ruling_cells
        ruling_records += int(ruling_cells > 0)
        best_hist[best] += 1
        update_option_census(census, record, options_by_vertex)
        if best == 20:
            equality_components.extend(equality_descriptors(record, index))
            best_records.append(
                {
                    "index": index,
                    "q": int(record["q"]),
                    "partitions": record["partitions"],
                    "delta": record["delta_by_vertex"],
                    "ranks": record["ranks_01_02_03_12_13_23"],
                    "shape": shape,
                    "cells": int(cells),
                    "ruling": int(ruling_cells),
                }
            )
        if int(record["q"]) == 20:
            q20_records.append(
                {
                    "index": index,
                    "partitions": record["partitions"],
                    "delta": record["delta_by_vertex"],
                    "ranks": record["ranks_01_02_03_12_13_23"],
                    "shape": shape,
                    "cells": int(cells),
                    "ruling": int(ruling_cells),
                }
            )
        if progress and (index + 1) % 25 == 0:
            print(
                "progress",
                index + 1,
                round(time.time() - started, 1),
                "explained",
                explained,
                "ruling",
                ruling,
                "best",
                dict(sorted(best_hist.items())),
                flush=True,
            )
    q_hist = dict(sorted(Counter(int(record["q"]) for record in data["records"]).items()))
    assert q_hist == EXPECTED_Q_HISTOGRAM
    assert explained == EXPECTED_EXPLAINED_CELLS
    assert ruling == ruling_records == 0
    assert dict(sorted(best_hist.items())) == EXPECTED_MIN_BEST_HISTOGRAM
    assert tuple(item["index"] for item in best_records) == EXPECTED_MIN_INDICES
    assert tuple(item["index"] for item in q20_records) == EXPECTED_Q20_INDICES
    assert sum(census["line_options_by_kind"].values()) == EXPECTED_LINE_OPTION_TOTAL
    assert dict(census["line_options_by_kind"]) == EXPECTED_LINE_OPTIONS_BY_KIND
    assert dict(census["normal_total"]) == EXPECTED_NORMAL_TOTAL
    assert census["vertex_product_sum"] == EXPECTED_PRODUCT_SUM
    equality_signatures = tuple(
        equality_signature(descriptor) for descriptor in equality_components
    )
    assert equality_signatures == EXPECTED_EQUALITY_SIGNATURES
    equality_symmetry_audit = audit_declared_equality_symmetries(
        data, equality_components
    )
    return {
        "status": "independent_finite_field_q22_reconstruction",
        "global_conjecture": "UNRESOLVED",
        "input": {
            "path": path.relative_to(Path(__file__).parents[2]).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": input_sha,
            "records_sha256": records_sha,
        },
        "records": len(data["records"]),
        "q_hist": q_hist,
        "explained_cells": explained,
        "ruling_cells": ruling,
        "ruling_records": ruling_records,
        "best_hist": dict(sorted(best_hist.items())),
        "best_min_records": best_records,
        "q20_records": q20_records,
        "equality_components": equality_components,
        "equality_symmetry_audit": equality_symmetry_audit,
        "option_census": {
            "line_options_total": int(sum(census["line_options_by_kind"].values())),
            "line_options_by_kind": dict(sorted(census["line_options_by_kind"].items())),
            "line_options_by_q": {
                str(q): dict(sorted(values.items()))
                for q, values in sorted(census["line_options_by_q"].items())
            },
            "normal_total": serialise_counter(census["normal_total"]),
            "normal_by_q": {
                str(q): serialise_counter(values)
                for q, values in sorted(census["normal_by_q"].items())
            },
            "crossratio_eligible_options": dict(sorted(census["crossratio_eligible_options"].items())),
            "crossratio_eligible_by_q": {
                str(q): dict(sorted(values.items()))
                for q, values in sorted(census["crossratio_eligible_by_q"].items())
            },
            "state_shape_hist": serialise_counter(census["state_shape_hist"]),
            "vertex_product_sum": int(census["vertex_product_sum"]),
            "vertex_product_hist": serialise_counter(census["vertex_product_hist"]),
        },
        "scope_limit": (
            "q<=22 canonical near-frontier input only; finite-field exact screen, "
            "not a proof of B_all, target consistency, scheme completeness, or "
            "the Krenn-Gu conjecture"
        ),
        "seconds": round(time.time() - started, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    result = run(args.input.resolve(), args.progress)
    print("balanced m=3 full-sensor q<=22 independent reconstruction: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
