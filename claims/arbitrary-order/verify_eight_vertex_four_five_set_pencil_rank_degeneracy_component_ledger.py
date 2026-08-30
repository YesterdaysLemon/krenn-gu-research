#!/usr/bin/env python3
"""Verify the fixed-pencil q<=22 rank-degeneracy component ledger.

The plane codimensions are exact incidence counts for coordinate support
subspaces.  Every nontrivial collinearity condition on three distinct block
lines is included; when four block lines occur, the common-plane condition is
included as well.  In ``--exact-rational`` mode, every event rank is certified
by an exact rational specialization attaining an exact Segre-circuit upper
bound.  The faster default uses deterministic finite-field witnesses and is
exploratory corroboration only.  Active-active and
active-structural complementary 2+1+1 ruling circuits are recognized
explicitly and checked by hostile fixtures.  Cross-ratio closures are
deliberately pessimistic: within each equivalence class every eligible
rank-four edge is allowed to drop by one for only k-1 compatibility equations.
The verifier checks the finite ledger; the accompanying theorem document owns
the characteristic-zero circuit, irreducibility, and component arguments.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
from random import Random

import numpy as np


PRIME = 1_000_003
PAIR_ORDER = tuple(combinations(range(4), 2))
EXPECTED_INPUT_SHA256 = (
    "D5B821A47F8164F56E1254E9400FF1875BAB650CE5E64BE3A0E191129BED541A"
)
EXPECTED_Q_HISTOGRAM = {"20": 2, "21": 39, "22": 506}
EXPECTED_STRUCTURAL_PROJECTION_SHA256 = (
    "D5C0AC3C054A4B6FD6FA3CB940ECB9733A29D0AEC10D1F648F121083E01074DF"
)
STRUCTURAL_PROJECTION_KEYS = (
    "record_index",
    "generic_q",
    "selectors",
    "partitions",
    "delta_by_vertex",
    "generic_ranks",
    "option_counts",
    "crossratio_eligible_option_counts",
    "circuit_explained_rank_drop_cells",
    "complementary_ruling_rank_drop_cells",
    "best_plane_only",
    "best_screened",
    "equality_component_count",
    "equality_components",
    "threats",
)


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest().upper()


def structural_projection(results: list[dict[str, object]]):
    return [
        {key: result[key] for key in STRUCTURAL_PROJECTION_KEYS}
        for result in results
    ]


def inv(value: int) -> int:
    return pow(value % PRIME, PRIME - 2, PRIME)


def rank(rows: list[list[int]]) -> int:
    matrix = [[entry % PRIME for entry in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inv(matrix[pivot_row][column])
        matrix[pivot_row] = [(value * scale) % PRIME for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def exact_rank(rows) -> int:
    """Rank over Q, using exact fraction elimination."""

    matrix = [[Fraction(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def vector_rank(vectors: list[tuple[int, int, int]]) -> int:
    return rank([[vector[row] for vector in vectors] for row in range(3)])


def exact_vector_rank(vectors: list[tuple[int, int, int]]) -> int:
    return exact_rank([[vector[row] for vector in vectors] for row in range(3)])


def proportional(left: tuple[int, int, int], right: tuple[int, int, int]) -> bool:
    return vector_rank([left, right]) == 1


def structural_rank(masks: tuple[int, ...]) -> int:
    best = 0
    for size in range(1, min(3, len(masks)) + 1):
        for blocks in combinations(range(len(masks)), size):
            for coordinates in combinations(range(3), size):
                if any(
                    all(masks[blocks[row]] & (1 << coordinates[column]) for row, column in enumerate(permutation))
                    for permutation in permutations(range(size))
                ):
                    best = size
                    break
    return best


def null_basis(mask: int, normal: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    coordinates = [index for index in range(3) if mask & (1 << index)]
    restricted = [normal[index] % PRIME for index in coordinates]
    pivot_position = next((index for index, value in enumerate(restricted) if value), None)
    if pivot_position is None:
        return [tuple(1 if row == coordinate else 0 for row in range(3)) for coordinate in coordinates]
    pivot_coordinate = coordinates[pivot_position]
    basis = []
    for coordinate in coordinates:
        if coordinate == pivot_coordinate:
            continue
        vector = [0, 0, 0]
        vector[coordinate] = 1
        vector[pivot_coordinate] = (-normal[coordinate] * inv(normal[pivot_coordinate])) % PRIME
        basis.append(tuple(vector))
    return basis


def linear_combination(
    basis: list[tuple[int, int, int]], coefficient_seed: int
) -> tuple[int, int, int]:
    seed = coefficient_seed % PRIME
    coefficients = [1]
    if len(basis) >= 2:
        coefficients.append((seed * seed + 17 * seed + 31) % PRIME)
    if len(basis) >= 3:
        coefficients.append((seed**3 + 29 * seed * seed + 37 * seed + 41) % PRIME)
    return tuple(
        sum(coefficients[index] * basis[index][row] for index in range(len(basis))) % PRIME
        for row in range(3)
    )


def distinct(vectors: list[tuple[int, int, int]]) -> bool:
    return all(
        not proportional(vectors[left], vectors[right])
        for left, right in combinations(range(len(vectors)), 2)
    )


def generic_vectors(masks: tuple[int, ...], salt: int) -> list[tuple[int, int, int]]:
    for attempt in range(1, 30):
        vectors = []
        for block, mask in enumerate(masks):
            basis = [
                tuple(1 if row == coordinate else 0 for row in range(3))
                for coordinate in range(3)
                if mask & (1 << coordinate)
            ]
            vectors.append(linear_combination(basis, salt + 19 * block + 97 * attempt))
        if distinct(vectors) and vector_rank(vectors) == structural_rank(masks):
            return vectors
    raise AssertionError(("generic sample failed", masks, salt))


def generic_samples(
    masks: tuple[int, ...], salt: int, sample_count: int = 2
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    samples = []
    for sample in range(sample_count):
        vectors = tuple(generic_vectors(masks, salt + 104729 * sample))
        if vectors not in samples:
            samples.append(vectors)
    return tuple(samples)


def exact_distinct(vectors: list[tuple[int, int, int]]) -> bool:
    return all(
        exact_vector_rank([vectors[left], vectors[right]]) == 2
        for left, right in combinations(range(len(vectors)), 2)
    )


def exact_generic_vectors(
    masks: tuple[int, ...], salt: int
) -> tuple[tuple[int, int, int], ...]:
    generator = Random(salt)
    vectors = []
    for mask in masks:
        vector = tuple(
            generator.randrange(1, 10_000)
            if mask & (1 << coordinate)
            else 0
            for coordinate in range(3)
        )
        vectors.append(vector)
    return tuple(vectors)


def exact_generic_samples(
    masks: tuple[int, ...], salt: int, sample_count: int = 4
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    samples = []
    for attempt in range(1, 200):
        vectors = exact_generic_vectors(masks, salt + 37 * attempt)
        if not exact_distinct(list(vectors)):
            continue
        if exact_vector_rank(list(vectors)) != structural_rank(masks):
            continue
        if vectors not in samples:
            samples.append(vectors)
        if len(samples) == sample_count:
            return tuple(samples)
    raise AssertionError(("failed to construct exact generic samples", masks, salt))


def normal_vector(normal_mask: int, seed: int) -> tuple[int, int, int]:
    values = []
    for coordinate in range(3):
        if not normal_mask & (1 << coordinate):
            values.append(0)
            continue
        value = (
            seed ** (coordinate + 1)
            + (17 + 12 * coordinate) * seed
            + 31
            + 10 * coordinate
        ) % PRIME
        values.append(value or coordinate + 2)
    return tuple(values)


def incidence_codimension(
    masks: tuple[int, ...], selected_blocks: tuple[int, ...], normal_mask: int
) -> int | None:
    base_dimension = sum(mask.bit_count() - 1 for mask in masks)
    selected = set(selected_blocks)
    incidence_dimension = normal_mask.bit_count() - 1
    for block, mask in enumerate(masks):
        if block not in selected:
            incidence_dimension += mask.bit_count() - 1
            continue
        intersection_dimension = mask.bit_count() - int(bool(mask & normal_mask))
        if intersection_dimension <= 0:
            return None
        incidence_dimension += intersection_dimension - 1
    codimension = base_dimension - incidence_dimension
    return codimension if codimension >= 0 else None


def forced_projective_point_code(
    mask: int, normal_mask: int, selected: bool
) -> int | None:
    """Encode a point forced by one-dimensional coordinate incidence.

    ``None`` means that the point still moves in a projective space of positive
    dimension.  For a selected two-coordinate block meeting the normal in both
    coordinates, the mask itself identifies its unique kernel line because the
    same exact normal is shared by all selected blocks.
    """

    vector_dimension = mask.bit_count() - int(selected and bool(mask & normal_mask))
    if vector_dimension != 1:
        return None
    if not selected or not (mask & normal_mask) or mask.bit_count() == 1:
        return mask
    normal_intersection = mask & normal_mask
    if normal_intersection.bit_count() == 1:
        return mask ^ normal_intersection
    assert mask.bit_count() == 2 and normal_intersection == mask
    return mask


def incidence_distinct_locus_nonempty(
    masks: tuple[int, ...], selected_blocks: tuple[int, ...], normal_mask: int
) -> bool:
    """Decide nonemptiness of the exact-partition open in one incidence cell.

    A collision is forced exactly when two blocks have the same
    one-dimensional allowed vector space.  Every other block moves in a
    positive-dimensional projective space and can avoid finitely many points
    over characteristic zero.
    """

    selected = set(selected_blocks)
    fixed_points = []
    for block, mask in enumerate(masks):
        intersection_dimension = mask.bit_count() - int(
            block in selected and bool(mask & normal_mask)
        )
        if intersection_dimension <= 0:
            return False
        code = forced_projective_point_code(
            mask, normal_mask, block in selected
        )
        if code is not None:
            fixed_points.append(code)
    return len(fixed_points) == len(set(fixed_points))


def incidence_samples(
    masks: tuple[int, ...],
    selected_blocks: tuple[int, ...],
    normal_mask: int,
    salt: int,
    sample_count: int = 2,
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    selected = set(selected_blocks)
    candidates = []
    for attempt in range(1, 100):
        normal = normal_vector(normal_mask, salt + 193 * attempt)
        bases = []
        for block, mask in enumerate(masks):
            if block in selected:
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
        vectors = tuple(
            linear_combination(basis, salt + 307 * block + 1009 * attempt)
            for block, basis in enumerate(bases)
        )
        if not distinct(list(vectors)):
            continue
        selected_vectors = [vectors[block] for block in selected_blocks]
        if vector_rank(selected_vectors) != 2:
            continue
        if vectors not in candidates:
            candidates.append(vectors)
        if len(candidates) == sample_count:
            return tuple(candidates)
    return tuple(candidates)


def exact_normal_vector(normal_mask: int, seed: int) -> tuple[int, int, int]:
    generator = Random(seed)
    return tuple(
        generator.randrange(1, 1_000)
        if normal_mask & (1 << coordinate)
        else 0
        for coordinate in range(3)
    )


def exact_null_basis(
    mask: int, normal: tuple[int, int, int]
) -> list[tuple[int, int, int]]:
    coordinates = [coordinate for coordinate in range(3) if mask & (1 << coordinate)]
    pivot = next((coordinate for coordinate in coordinates if normal[coordinate]), None)
    if pivot is None:
        return [
            tuple(1 if row == coordinate else 0 for row in range(3))
            for coordinate in coordinates
        ]
    basis = []
    for coordinate in coordinates:
        if coordinate == pivot:
            continue
        vector = [0, 0, 0]
        vector[coordinate] = normal[pivot]
        vector[pivot] = -normal[coordinate]
        basis.append(tuple(vector))
    return basis


def exact_linear_combination(
    basis: list[tuple[int, int, int]], seed: int
) -> tuple[int, int, int]:
    generator = Random(seed)
    coefficients = [generator.randrange(1, 1_000) for _ in basis]
    return tuple(
        sum(coefficient * vector[row] for coefficient, vector in zip(coefficients, basis))
        for row in range(3)
    )


def exact_incidence_samples(
    masks: tuple[int, ...],
    selected_blocks: tuple[int, ...],
    normal_mask: int,
    salt: int,
    sample_count: int = 4,
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    selected = set(selected_blocks)
    candidates = []
    for attempt in range(1, 300):
        normal = exact_normal_vector(normal_mask, salt + 131 * attempt)
        bases = []
        for block, mask in enumerate(masks):
            if block in selected:
                bases.append(exact_null_basis(mask, normal))
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
        vectors = tuple(
            exact_linear_combination(
                basis, salt + 211 * block + 1009 * attempt
            )
            for block, basis in enumerate(bases)
        )
        if not exact_distinct(list(vectors)):
            continue
        if exact_vector_rank([vectors[block] for block in selected_blocks]) != 2:
            continue
        if vectors not in candidates:
            candidates.append(vectors)
        if len(candidates) == sample_count:
            return tuple(candidates)
    raise AssertionError(
        ("failed to construct exact incidence samples", masks, selected_blocks, normal_mask, salt)
    )


def plane_options(
    masks: tuple[int, ...], salt: int, exact_rational: bool = False
):
    options = [
        {
            "selected_blocks": (),
            "normal_mask": 0,
            "codimension": 0,
            "samples": () if exact_rational else generic_samples(masks, salt),
        }
    ]
    block_count = len(masks)
    selected_sets = list(combinations(range(block_count), 3))
    if block_count == 4:
        selected_sets.append(tuple(range(4)))
    for selected_index, selected_blocks in enumerate(selected_sets):
        selected_masks = tuple(masks[block] for block in selected_blocks)
        if structural_rank(selected_masks) <= 2:
            continue
        for normal_mask in range(1, 8):
            codimension = incidence_codimension(masks, selected_blocks, normal_mask)
            if codimension is None:
                continue
            if not incidence_distinct_locus_nonempty(
                masks, selected_blocks, normal_mask
            ):
                continue
            samples = (
                ()
                if exact_rational
                else incidence_samples(
                    masks,
                    selected_blocks,
                    normal_mask,
                    salt + 100003 * selected_index + 1009 * normal_mask,
                )
            )
            if not exact_rational and not samples:
                raise AssertionError(
                    (
                        "finite-field sampler missed a combinatorially feasible "
                        "incidence cell",
                        masks,
                        selected_blocks,
                        normal_mask,
                    )
                )
            options.append(
                {
                    "selected_blocks": selected_blocks,
                    "normal_mask": normal_mask,
                    "codimension": codimension,
                    "samples": samples,
                }
            )
    return options


def chart_vectors(
    partition: tuple[int, int, int, int], block_vectors: list[tuple[int, int, int]]
) -> tuple[tuple[int, int, int], ...]:
    return tuple(block_vectors[partition[chart]] for chart in range(4))


def edge_rank(
    left: tuple[tuple[int, int, int], ...],
    right: tuple[tuple[int, int, int], ...],
) -> int:
    vectors = [
        tuple(left[chart][row] * right[chart][column] % PRIME for row in range(3) for column in range(3))
        for chart in range(4)
    ]
    return rank(vectors)


def exact_edge_rank(
    left: tuple[tuple[int, int, int], ...],
    right: tuple[tuple[int, int, int], ...],
) -> int:
    vectors = [
        tuple(
            left[chart][row] * right[chart][column]
            for row in range(3)
            for column in range(3)
        )
        for chart in range(4)
    ]
    return exact_rank(vectors)


def prepare_options(
    masks: tuple[int, ...],
    partition: tuple[int, int, int, int],
    salt: int,
    exact_rational: bool = False,
):
    options = plane_options(masks, salt, exact_rational=exact_rational)
    for option in options:
        option["masks"] = masks
        option["partition"] = partition
        charts = tuple(
            chart_vectors(partition, sample) for sample in option["samples"]
        )
        option["charts"] = charts
        if option["selected_blocks"]:
            exact_samples = exact_incidence_samples(
                masks,
                option["selected_blocks"],
                option["normal_mask"],
                salt + 300007 * option["normal_mask"] + 1709 * sum(option["selected_blocks"]),
            )
        else:
            exact_samples = exact_generic_samples(masks, salt + 700001)
        exact_charts = tuple(
            chart_vectors(partition, sample) for sample in exact_samples
        )
        option["exact_samples"] = exact_samples
        option["exact_charts"] = exact_charts
        option["crossratio_eligible"] = (
            len(set(partition)) == 4
            and forced_collinear(option, tuple(range(len(masks))))
        )
        if option["crossratio_eligible"]:
            assert all(
                exact_vector_rank(list(chart)) == 2 for chart in exact_charts
            )
    return options


def forced_collinear(option, blocks: tuple[int, ...]) -> bool:
    """Return whether an option forces distinct block points onto one P1."""
    unique_blocks = tuple(sorted(set(blocks)))
    if len(unique_blocks) < 3:
        return False
    masks = tuple(option["masks"][block] for block in unique_blocks)
    if structural_rank(masks) <= 2:
        return True
    selected = set(option["selected_blocks"])
    if not selected:
        return False
    normal_mask = option["normal_mask"]
    forced_into_event_line = selected | {
        block
        for block, mask in enumerate(option["masks"])
        if mask & normal_mask == 0
    }
    return set(unique_blocks).issubset(forced_into_event_line)


def forced_factor_rank_upper(option, blocks: tuple[int, ...]) -> int:
    unique_blocks = tuple(sorted(set(blocks)))
    upper = structural_rank(tuple(option["masks"][block] for block in unique_blocks))
    if forced_collinear(option, unique_blocks):
        upper = min(upper, 2)
    return upper


def repeated_chart_pair(partition: tuple[int, int, int, int]):
    """Return the repeated chart pair of a 2+1+1 partition, if present."""

    if len(set(partition)) != 3:
        return None
    repeated = tuple(
        pair
        for pair in combinations(range(4), 2)
        if partition[pair[0]] == partition[pair[1]]
    )
    assert len(repeated) == 1
    return repeated[0]


def forced_complementary_ruling_circuit(left_option, right_option) -> bool:
    """Detect a forced reducible (1,0)+(0,1) plane circuit."""

    left_pair = repeated_chart_pair(left_option["partition"])
    right_pair = repeated_chart_pair(right_option["partition"])
    if left_pair is None or right_pair is None:
        return False
    if set(left_pair) & set(right_pair) or set(left_pair) | set(right_pair) != set(range(4)):
        return False
    left_blocks = tuple(sorted(set(left_option["partition"])))
    right_blocks = tuple(sorted(set(right_option["partition"])))
    return forced_collinear(left_option, left_blocks) and forced_collinear(
        right_option, right_blocks
    )


def forced_edge_rank_upper(left_option, right_option, generic_rank: int):
    """Upper-bound an event-edge rank using only forced Segre circuits."""
    left_partition = left_option["partition"]
    right_partition = right_option["partition"]
    edge_pairs = tuple(sorted(set(zip(left_partition, right_partition, strict=True))))
    upper = min(generic_rank, len(edge_pairs))
    mechanisms = []

    left_blocks = tuple(pair[0] for pair in edge_pairs)
    right_blocks = tuple(pair[1] for pair in edge_pairs)
    if len(set(left_blocks)) == 1:
        factor_upper = forced_factor_rank_upper(right_option, right_blocks)
        if factor_upper < upper:
            upper = factor_upper
            mechanisms.append("fixed-left-factor span bound")
    if len(set(right_blocks)) == 1:
        factor_upper = forced_factor_rank_upper(left_option, left_blocks)
        if factor_upper < upper:
            upper = factor_upper
            mechanisms.append("fixed-right-factor span bound")

    if generic_rank == 4 and forced_complementary_ruling_circuit(
        left_option, right_option
    ):
        upper = min(upper, 3)
        mechanisms.append("complementary-ruling four-point Segre circuit")

    forced_circuits = []
    for indices in combinations(range(len(edge_pairs)), 3):
        triple_left = tuple(edge_pairs[index][0] for index in indices)
        triple_right = tuple(edge_pairs[index][1] for index in indices)
        if len(set(triple_left)) == 1 and forced_collinear(right_option, triple_right):
            forced_circuits.append(indices)
        if len(set(triple_right)) == 1 and forced_collinear(left_option, triple_left):
            forced_circuits.append(indices)
    if forced_circuits:
        upper = min(upper, len(edge_pairs) - 1)
        mechanisms.append("fixed-factor three-point Segre circuit")
    if len(set(forced_circuits)) >= 2:
        upper = min(upper, 2)
        mechanisms.append("two overlapping three-point circuits")
    return upper, tuple(mechanisms)


def assert_complementary_ruling_detector():
    """Replay active-active and active-structural ruling countermodels."""

    masks = (7, 7, 7)
    left_options = prepare_options(masks, (0, 0, 1, 2), 880301)
    right_options = prepare_options(masks, (0, 1, 2, 2), 880907)
    left_generic = left_options[0]
    right_generic = right_options[0]
    left_line = next(
        option
        for option in left_options
        if option["selected_blocks"] == (0, 1, 2)
        and option["normal_mask"] == 7
        and option["codimension"] == 1
    )
    right_line = next(
        option
        for option in right_options
        if option["selected_blocks"] == (0, 1, 2)
        and option["normal_mask"] == 7
        and option["codimension"] == 1
    )
    generic_rank = int(edge_rank_matrix([left_generic], [right_generic])[0, 0])
    event_rank = int(edge_rank_matrix([left_line], [right_line])[0, 0])
    exact_generic_rank_value = int(
        exact_edge_rank_matrix([left_generic], [right_generic])[0, 0]
    )
    exact_event_rank_value = int(
        exact_edge_rank_matrix([left_line], [right_line])[0, 0]
    )
    upper, mechanisms = forced_edge_rank_upper(left_line, right_line, generic_rank)
    assert generic_rank == 4
    assert event_rank == upper == 3
    assert exact_generic_rank_value == 4
    assert exact_event_rank_value == 3
    assert "complementary-ruling four-point Segre circuit" in mechanisms
    structural_options = prepare_options((3, 3, 3), (0, 1, 2, 2), 881917)
    structural_baseline = structural_options[0]
    assert structural_baseline["selected_blocks"] == ()
    assert forced_collinear(structural_baseline, (0, 1, 2))
    assert structural_rank(structural_baseline["masks"]) == 2
    mixed_generic_rank = int(
        edge_rank_matrix([left_generic], [structural_baseline])[0, 0]
    )
    mixed_event_rank = int(
        edge_rank_matrix([left_line], [structural_baseline])[0, 0]
    )
    mixed_exact_generic_rank = int(
        exact_edge_rank_matrix([left_generic], [structural_baseline])[0, 0]
    )
    mixed_exact_event_rank = int(
        exact_edge_rank_matrix([left_line], [structural_baseline])[0, 0]
    )
    mixed_upper, mixed_mechanisms = forced_edge_rank_upper(
        left_line, structural_baseline, mixed_generic_rank
    )
    assert mixed_generic_rank == 4
    assert mixed_event_rank == mixed_upper == 3
    assert mixed_exact_generic_rank == 4
    assert mixed_exact_event_rank == 3
    assert "complementary-ruling four-point Segre circuit" in mixed_mechanisms
    return {
        "active_active": {
            "partitions": [[0, 0, 1, 2], [0, 1, 2, 2]],
            "generic_rank": generic_rank,
            "event_rank": event_rank,
            "exact_rational_generic_rank": exact_generic_rank_value,
            "exact_rational_event_rank": exact_event_rank_value,
            "forced_upper": upper,
            "mechanisms": list(mechanisms),
        },
        "active_structural": {
            "partitions": [[0, 0, 1, 2], [0, 1, 2, 2]],
            "active_masks": [7, 7, 7],
            "structural_masks": [3, 3, 3],
            "structural_rank": 2,
            "generic_rank": mixed_generic_rank,
            "event_rank": mixed_event_rank,
            "exact_rational_generic_rank": mixed_exact_generic_rank,
            "exact_rational_event_rank": mixed_exact_event_rank,
            "forced_upper": mixed_upper,
            "mechanisms": list(mixed_mechanisms),
        },
    }


def edge_rank_matrix(left_options, right_options) -> np.ndarray:
    matrix = np.zeros((len(left_options), len(right_options)), dtype=np.int8)
    for left_index, left_option in enumerate(left_options):
        for right_index, right_option in enumerate(right_options):
            matrix[left_index, right_index] = max(
                edge_rank(left_chart, right_chart)
                for left_chart, right_chart in product(
                    left_option["charts"], right_option["charts"]
                )
            )
    return matrix


def exact_edge_rank_matrix(left_options, right_options) -> np.ndarray:
    matrix = np.zeros((len(left_options), len(right_options)), dtype=np.int8)
    for left_index, left_option in enumerate(left_options):
        for right_index, right_option in enumerate(right_options):
            matrix[left_index, right_index] = max(
                exact_edge_rank(left_chart, right_chart)
                for left_chart, right_chart in product(
                    left_option["exact_charts"], right_option["exact_charts"]
                )
            )
    return matrix


def stable_state_salt(
    masks: tuple[int, ...], partition: tuple[int, int, int, int]
) -> int:
    """Return a platform-independent salt for one support/partition state."""

    payload = bytes((*masks, 255, *partition))
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


@lru_cache(maxsize=None)
def cached_prepared_options(
    state: tuple[tuple[int, ...], tuple[int, int, int, int]],
    exact_rational: bool,
):
    masks, partition = state
    return tuple(
        prepare_options(
            masks,
            partition,
            stable_state_salt(masks, partition),
            exact_rational=exact_rational,
        )
    )


@lru_cache(maxsize=None)
def cached_edge_rank_matrix(
    left_state: tuple[tuple[int, ...], tuple[int, int, int, int]],
    right_state: tuple[tuple[int, ...], tuple[int, int, int, int]],
    exact_rational: bool,
) -> np.ndarray:
    left_options = cached_prepared_options(left_state, exact_rational)
    right_options = cached_prepared_options(right_state, exact_rational)
    matrix_function = exact_edge_rank_matrix if exact_rational else edge_rank_matrix
    return matrix_function(left_options, right_options)


def broadcast_vector(vector: np.ndarray, vertex: int, shape: tuple[int, ...]):
    dimensions = [1] * len(shape)
    dimensions[vertex] = len(vector)
    return vector.reshape(dimensions)


def broadcast_matrix(
    matrix: np.ndarray, left: int, right: int, shape: tuple[int, ...]
):
    dimensions = [1] * len(shape)
    dimensions[left] = matrix.shape[0]
    dimensions[right] = matrix.shape[1]
    return matrix.reshape(dimensions)


def crossratio_mod(chart: tuple[tuple[int, int, int], ...]) -> int:
    def bracket(
        left: tuple[int, int, int], right: tuple[int, int, int]
    ) -> int:
        cross = (
            left[1] * right[2] - left[2] * right[1],
            left[2] * right[0] - left[0] * right[2],
            left[0] * right[1] - left[1] * right[0],
        )
        return next(value % PRIME for value in cross if value % PRIME)

    numerator = bracket(chart[0], chart[2]) * bracket(chart[1], chart[3])
    denominator = bracket(chart[0], chart[3]) * bracket(chart[1], chart[2])
    return numerator % PRIME * inv(denominator) % PRIME


def assert_universal_crossratio_dominance() -> int:
    """Give two distinct cross-ratio witnesses for every coordinate event type."""
    checked = 0
    for masks in product(range(1, 8), repeat=4):
        singleton_masks = [mask for mask in masks if mask.bit_count() == 1]
        if len(singleton_masks) != len(set(singleton_masks)):
            continue
        salt = sum((index + 1) * mask * 137 for index, mask in enumerate(masks))
        for option in prepare_options(masks, (0, 1, 2, 3), salt):
            if not option["crossratio_eligible"]:
                continue
            values = {crossratio_mod(chart) for chart in option["charts"]}
            if len(values) != 2:
                raise AssertionError(
                    (
                        "cross-ratio dominance witness failed",
                        masks,
                        option["selected_blocks"],
                        option["normal_mask"],
                        option["codimension"],
                        values,
                    )
                )
            checked += 1
    assert checked == 3052
    return checked


def set_partitions(values: tuple[int, ...]):
    if not values:
        yield ()
        return
    first, *rest = values
    for partition in set_partitions(tuple(rest)):
        yield ((first,),) + partition
        for index in range(len(partition)):
            yield partition[:index] + ((first,) + partition[index],) + partition[index + 1 :]


def unique_partitions(values: tuple[int, ...]):
    seen = set()
    for partition in set_partitions(values):
        canonical = tuple(sorted((tuple(sorted(block)) for block in partition), key=lambda block: block[0]))
        if canonical not in seen:
            seen.add(canonical)
            yield canonical


def screen_record(
    record: dict[str, object], record_index: int, exact_rational: bool = False
):
    partitions = tuple(tuple(value) for value in record["partitions"])
    masks_by_vertex = tuple(tuple(value) for value in record["support_masks_by_vertex_block"])
    delta = sum(record["delta_by_vertex"])
    generic_q = int(record["q"])
    option_lists = []
    state_keys = []
    for vertex in range(4):
        masks = masks_by_vertex[vertex]
        state = (masks, partitions[vertex])
        state_keys.append(state)
        option_lists.append(cached_prepared_options(state, exact_rational))

    shape = tuple(len(options) for options in option_lists)
    pair_matrices = {
        (left, right): cached_edge_rank_matrix(
            state_keys[left], state_keys[right], exact_rational
        )
        for left, right in PAIR_ORDER
    }
    generic_ranks = tuple(
        int(pair_matrices[pair][0, 0]) for pair in PAIR_ORDER
    )
    expected_generic_ranks = tuple(record["ranks_01_02_03_12_13_23"])
    if generic_ranks != expected_generic_ranks:
        raise AssertionError(
            (
                (
                    "exact-rational base samples missed generic rank"
                    if exact_rational
                    else "finite-field base sample missed generic rank"
                ),
                record_index,
                generic_ranks,
                expected_generic_ranks,
            )
        )
    circuit_explanation_count = 0
    ruling_explanation_count = 0
    for pair_index, pair in enumerate(PAIR_ORDER):
        generic_rank = expected_generic_ranks[pair_index]
        matrix = pair_matrices[pair]
        for left_index, left_option in enumerate(option_lists[pair[0]]):
            for right_index, right_option in enumerate(option_lists[pair[1]]):
                upper, mechanisms = forced_edge_rank_upper(
                    left_option, right_option, generic_rank
                )
                sampled_rank = int(matrix[left_index, right_index])
                if sampled_rank != upper:
                    raise AssertionError(
                        (
                            "unexplained or accidentally deficient event rank",
                            record_index,
                            pair,
                            left_index,
                            right_index,
                            generic_rank,
                            sampled_rank,
                            upper,
                            mechanisms,
                        )
                    )
                if sampled_rank < generic_rank:
                    assert mechanisms
                    circuit_explanation_count += 1
                    if "complementary-ruling four-point Segre circuit" in mechanisms:
                        ruling_explanation_count += 1

    costs = np.full(shape, delta, dtype=np.int16)
    for vertex, options in enumerate(option_lists):
        codimensions = np.asarray(
            [option["codimension"] for option in options], dtype=np.int16
        )
        costs += broadcast_vector(codimensions, vertex, shape)
    for pair, matrix in pair_matrices.items():
        costs += broadcast_matrix(matrix, pair[0], pair[1], shape)

    def describe(
        indices: tuple[int, int, int, int],
        compensated_q: int,
        equivalence: tuple[tuple[int, ...], ...] | None = None,
    ):
        selected_options = tuple(
            option_lists[vertex][indices[vertex]] for vertex in range(4)
        )
        ranks = tuple(
            int(pair_matrices[pair][indices[pair[0]], indices[pair[1]]])
            for pair in PAIR_ORDER
        )
        descriptor = {
            "option_indices": list(indices),
            "plane_options": [
                {
                    "selected_blocks": list(option["selected_blocks"]),
                    "normal_mask": option["normal_mask"],
                    "codimension": option["codimension"],
                }
                for option in selected_options
            ],
            "plane_codimension": sum(
                option["codimension"] for option in selected_options
            ),
            "ranks": list(ranks),
            "compensated_q": int(compensated_q),
        }
        if equivalence is not None:
            nontrivial = tuple(block for block in equivalence if len(block) > 1)
            cross_cost = sum(len(block) - 1 for block in nontrivial)
            cross_drop = sum(
                ranks[PAIR_ORDER.index(tuple(sorted((left, right))))] == 4
                for block in nontrivial
                for left, right in combinations(block, 2)
            )
            descriptor.update(
                {
                    "crossratio_classes": [list(block) for block in nontrivial],
                    "crossratio_cost": cross_cost,
                    "crossratio_drop": cross_drop,
                }
            )
        return descriptor

    plane_flat_index = int(np.argmin(costs))
    plane_indices = tuple(
        int(value) for value in np.unravel_index(plane_flat_index, shape)
    )
    plane_minimum = int(costs[plane_indices])
    best = describe(plane_indices, plane_minimum)
    best_type = "subset-plane"
    equality_components = [
        {
            "type": "subset-plane",
            **describe(tuple(int(value) for value in indices), 20),
        }
        for indices in np.argwhere(costs == 20)
    ]

    all_indices = tuple(np.arange(length) for length in shape)
    eligible_indices = tuple(
        np.asarray(
            [
                index
                for index, option in enumerate(options)
                if option["crossratio_eligible"]
            ],
            dtype=int,
        )
        for options in option_lists
    )
    for equivalence in unique_partitions((0, 1, 2, 3)):
        nontrivial = tuple(block for block in equivalence if len(block) > 1)
        if not nontrivial:
            continue
        involved = {vertex for block in nontrivial for vertex in block}
        if any(len(eligible_indices[vertex]) == 0 for vertex in involved):
            continue
        indices_by_vertex = tuple(
            eligible_indices[vertex] if vertex in involved else all_indices[vertex]
            for vertex in range(4)
        )
        candidate = costs[np.ix_(*indices_by_vertex)].copy()
        cross_cost = sum(len(block) - 1 for block in nontrivial)
        candidate += cross_cost
        candidate_shape = tuple(len(indices) for indices in indices_by_vertex)
        for block in nontrivial:
            for left, right in combinations(block, 2):
                pair = tuple(sorted((left, right)))
                restricted = pair_matrices[pair][
                    np.ix_(indices_by_vertex[left], indices_by_vertex[right])
                ]
                candidate -= broadcast_matrix(
                    (restricted == 4).astype(np.int16),
                    left,
                    right,
                    candidate_shape,
                )
        local_flat_index = int(np.argmin(candidate))
        local_indices = tuple(
            int(value)
            for value in np.unravel_index(local_flat_index, candidate_shape)
        )
        global_indices = tuple(
            int(indices_by_vertex[vertex][local_indices[vertex]])
            for vertex in range(4)
        )
        value = int(candidate[local_indices])
        if value < best["compensated_q"]:
            best = describe(global_indices, value, equivalence)
            best_type = "subset-plane+crossratio"
        for equality_indices in np.argwhere(candidate == 20):
            equality_global_indices = tuple(
                int(indices_by_vertex[vertex][int(equality_indices[vertex])])
                for vertex in range(4)
            )
            equality_components.append(
                {
                    "type": "subset-plane+crossratio",
                    **describe(equality_global_indices, 20, equivalence),
                }
            )

    threats = []
    if best["compensated_q"] < 20:
        threats.append({"type": best_type, **best})
    return {
        "record_index": record_index,
        "rank_certificate_mode": (
            "exact_rational_specialization_plus_exact_circuit_upper"
            if exact_rational
            else "finite_field_specialization_plus_exact_circuit_upper"
        ),
        "generic_q": generic_q,
        "selectors": record["selectors"],
        "partitions": record["partitions"],
        "delta_by_vertex": record["delta_by_vertex"],
        "generic_ranks": record["ranks_01_02_03_12_13_23"],
        "option_counts": list(shape),
        "crossratio_eligible_option_counts": [
            len(indices) for indices in eligible_indices
        ],
        "circuit_explained_rank_drop_cells": circuit_explanation_count,
        "complementary_ruling_rank_drop_cells": ruling_explanation_count,
        "best_plane_only": describe(plane_indices, plane_minimum),
        "best_screened": best,
        "equality_component_count": len(equality_components),
        "equality_components": equality_components,
        "threats": threats,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name(
            "balanced_m3_full_sensor_q22_near_frontier_input_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--exact-rational",
        action="store_true",
        help=(
            "certify every event rank with an exact Q-specialization plus the "
            "exact circuit upper, rather than the faster finite-field witness"
        ),
    )
    parser.add_argument(
        "--record-limit",
        type=int,
        help="optional prefix length for development smoke tests",
    )
    parser.add_argument(
        "--check-universal-crossratio-dominance",
        action="store_true",
        help="also certify two cross-ratio values on all 3052 coordinate event types",
    )
    args = parser.parse_args()
    input_bytes = args.input.read_bytes()
    input_sha256 = hashlib.sha256(input_bytes).hexdigest().upper()
    data = json.loads(input_bytes)
    complementary_ruling_detector_self_test = assert_complementary_ruling_detector()
    input_records = data["records"]
    full_replay = args.record_limit is None
    if full_replay:
        assert input_sha256 == EXPECTED_INPUT_SHA256
        assert len(input_records) == 547
        assert {
            str(q): sum(int(record["q"]) == q for record in input_records)
            for q in (20, 21, 22)
        } == EXPECTED_Q_HISTOGRAM
    if args.record_limit is not None:
        assert args.record_limit > 0
        input_records = input_records[: args.record_limit]
    results = [
        screen_record(record, index, exact_rational=args.exact_rational)
        for index, record in enumerate(input_records)
    ]
    threats = [result for result in results if result["threats"]]
    minimum = min(result["best_screened"]["compensated_q"] for result in results)
    projection_sha256 = canonical_sha256(structural_projection(results))
    summary = {
        "status": (
            "exact_q22_rank_degeneracy_component_ledger"
            if args.exact_rational
            else "exploratory_finite_field_rank_degeneracy_screen"
        ),
        "global_conjecture": "UNRESOLVED",
        "input_sha256": input_sha256,
        "structural_projection_sha256": projection_sha256,
        "rank_certificate_mode": (
            "exact_rational_specialization_plus_exact_circuit_upper"
            if args.exact_rational
            else "finite_field_specialization_plus_exact_circuit_upper"
        ),
        "complementary_ruling_detector_self_test": complementary_ruling_detector_self_test,
        "records": len(results),
        "minimum_screened_compensated_q": minimum,
        "threat_record_count": len(threats),
        "complementary_ruling_rank_drop_cells": sum(
            result["complementary_ruling_rank_drop_cells"] for result in results
        ),
        "complementary_ruling_record_count": sum(
            result["complementary_ruling_rank_drop_cells"] > 0 for result in results
        ),
        "circuit_explained_rank_drop_cells": sum(
            result["circuit_explained_rank_drop_cells"] for result in results
        ),
        "equality_component_count": sum(
            result["equality_component_count"] for result in results
        ),
        "equality_record_indices": [
            result["record_index"]
            for result in results
            if result["equality_component_count"]
        ],
        "best_histogram": {
            str(value): sum(
                result["best_screened"]["compensated_q"] == value for result in results
            )
            for value in sorted(
                {result["best_screened"]["compensated_q"] for result in results}
            )
        },
        "threats": threats,
        "results": results,
        "scope_limit": (
            "screens deterministic generic points of every normal-support "
            "incidence stratum for three-block collinearity and four-block "
            "planarity, active-active and active-structural complementary "
            "ruling circuits, and k-1-cost cross-ratio compatibility; "
            "the exact irreducible/scheme component proof, cross-ratio image "
            "dimensions, and componentwise B_all properness remain open"
        ),
    }
    if full_replay:
        assert projection_sha256 == EXPECTED_STRUCTURAL_PROJECTION_SHA256
        assert summary["minimum_screened_compensated_q"] == 20
        assert summary["threat_record_count"] == 0
        assert summary["complementary_ruling_rank_drop_cells"] == 0
        assert summary["complementary_ruling_record_count"] == 0
        assert summary["circuit_explained_rank_drop_cells"] == 6429
        assert summary["equality_component_count"] == 9
        assert summary["equality_record_indices"] == [8, 36, 50, 142, 431]
        assert summary["best_histogram"] == {"20": 5, "21": 73, "22": 469}
    if args.check_universal_crossratio_dominance:
        summary["universal_crossratio_dominance_options"] = (
            assert_universal_crossratio_dominance()
        )
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {key: summary[key] for key in (
                "status",
                "rank_certificate_mode",
                "records",
                "minimum_screened_compensated_q",
                "threat_record_count",
                "complementary_ruling_rank_drop_cells",
                "complementary_ruling_record_count",
                "circuit_explained_rank_drop_cells",
                "equality_component_count",
                "equality_record_indices",
                "best_histogram",
                "input_sha256",
                "structural_projection_sha256",
                "global_conjecture",
            )},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
