#!/usr/bin/env python3
"""Verify the finite support-Segre rank census for the four-K5 pencil.

This is an exact finite computation at the *generic point of every exact
root-partition stratum*.  It is deliberately narrower than a theorem about
the full witness locus: rank-degeneracy subvarieties, the ``B_all``
intersection, compatibility of the seventy pencils, and the target equations
are not part of this verifier.

The old pencil probe used the number of distinct partition-block pairs as the
rank of four decomposable evaluations.  That surrogate is false.  For a
local signature ``(A, B, E)`` this verifier computes the generic rank of the
support-Segre matrix

    M[(a,b),(p,q)] = X[a,p] * Y[b,q]

over ``Q(X,Y)``.  A deterministic finite-field full-rank specialization is a
certificate that the corresponding polynomial minor is nonzero.  Only cases
where that specialization is deficient are replayed by exact determinant
polynomials.  Monomials are encoded by *adding* base-5 digit weights, which
records exponent vectors; multiplying the weights would incorrectly identify
different variables.

The complete run takes a few minutes and uses NumPy for the final integer
min-plus table.  No generated output is required for correctness: the
expected counts, hashes, and equality records below are asserted after the
enumeration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import (
    combinations,
    combinations_with_replacement,
    permutations,
    product,
)

import numpy as np

PRIME = 1_000_003
SHIFT = 7
COMMON_VERTICES = tuple(range(4))
PAIR_ORDER = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))

EXPECTED_SELECTOR_MULTISETS = 9_078_630  # binomial(120 + 4 - 1, 4)
EXPECTED_SELECTOR_ORBITS = 65_966
EXPECTED_PAIR_INSTANCES = 74_083_334
EXPECTED_RAW_SIGNATURES = 1_026_928
EXPECTED_FULL_PARTITION_SYSTEMS = 2_269_536_547
EXPECTED_MODULARLY_DEFICIENT = 24_765

EXPECTED_SELECTOR_HASH = (
    "e27c85bda3fc01904ad977c003eee1d235a12677186b84a9790d20a234c1e35f"
)
EXPECTED_RANK_HASH = (
    "b4610a69106b5fa342f7d5e386ba28761523b3976fea29657d7a348d7351d00f"
)
EXPECTED_Q_HASH = (
    "1af40871b003b0bbbdcb23aa46de728ff950b9edae489f65a2b504a8808bcb6a"
)

EXPECTED_RANK_HISTOGRAM = {
    (1, 1): 49,
    (2, 2): 2_755,
    (3, 2): 541,
    (3, 3): 92_401,
    (4, 2): 209,
    (4, 3): 22_060,
    (4, 4): 908_913,
}

EXPECTED_Q_HISTOGRAM = {
    20: 2,
    21: 39,
    22: 506,
    23: 8_882,
    24: 150_155,
    25: 804_555,
    26: 5_147_814,
    27: 18_813_205,
    28: 65_063_565,
    29: 162_773_111,
    30: 322_044_201,
    31: 496_230_100,
    32: 535_661_624,
    33: 394_624_590,
    34: 194_788_958,
    35: 55_870_011,
    36: 13_169_086,
    37: 3_943_026,
    38: 443_117,
}

EXPECTED_EQUALITIES = {
    (
        (0, 0, 0, 0),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
        (2, 3, 3, 4, 4, 4),
        (0, 0, 0, 0),
    ),
    (
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
        (1, 3, 3, 3, 3, 4),
        (0, 3, 0, 0),
    ),
}


def progress(enabled: bool, *parts: object) -> None:
    """Write progress without contaminating the JSON result on stdout."""

    if enabled:
        print(*parts, file=sys.stderr, flush=True)


def selector_maps() -> list[tuple[int, int, int]]:
    """Return the 120 nonconstant maps from colours to five K5 vertices."""

    return [m for m in product(range(5), repeat=3) if len(set(m)) > 1]


def encode_selector_quadruple(quadruple: tuple[int, int, int, int]) -> int:
    return (((quadruple[0] << SHIFT) | quadruple[1]) << SHIFT | quadruple[2]) << SHIFT | quadruple[3]


def decode_selector_quadruple(value: int) -> tuple[int, int, int, int]:
    return (
        (value >> (3 * SHIFT)) & 127,
        (value >> (2 * SHIFT)) & 127,
        (value >> SHIFT) & 127,
        value & 127,
    )


def selector_orbits(
    maps: list[tuple[int, int, int]], progress_enabled: bool
) -> tuple[list[tuple[int, int, int, int]], str]:
    """Enumerate chart-sorted selector tuples modulo safe S4 x S3 actions."""

    map_id = {m: index for index, m in enumerate(maps)}
    transforms: list[list[int]] = []
    for vertex_permutation in permutations(range(4)):
        for colour_permutation in permutations(range(3)):
            transforms.append(
                [
                    map_id[
                        tuple(
                            (
                                vertex_permutation[m[colour_permutation[colour]]]
                                if m[colour_permutation[colour]] < 4
                                else 4
                            )
                            for colour in range(3)
                        )
                    ]
                    for m in maps
                ]
            )

    unseen = {
        encode_selector_quadruple(quadruple)
        for quadruple in combinations_with_replacement(range(len(maps)), 4)
    }
    assert len(unseen) == EXPECTED_SELECTOR_MULTISETS

    representatives: list[tuple[int, int, int, int]] = []
    while unseen:
        quadruple = decode_selector_quadruple(unseen.pop())
        representatives.append(quadruple)
        orbit = {
            encode_selector_quadruple(
                tuple(sorted(transform[index] for index in quadruple))
            )
            for transform in transforms
        }
        unseen.difference_update(orbit)
        if len(representatives) % 20_000 == 0:
            progress(progress_enabled, "selector orbits", len(representatives))

    assert len(representatives) == EXPECTED_SELECTOR_ORBITS
    representatives.sort()
    selector_blob = b"".join(bytes(quadruple) for quadruple in representatives)
    selector_hash = hashlib.sha256(selector_blob).hexdigest()
    assert selector_hash == EXPECTED_SELECTOR_HASH
    return representatives, selector_hash


def restricted_growth_partitions() -> list[tuple[int, int, int, int]]:
    partitions: list[tuple[int, int, int, int]] = []

    def extend(prefix: list[int]) -> None:
        if len(prefix) == 4:
            partitions.append(tuple(prefix))
            return
        for label in range(max(prefix) + 2):
            extend(prefix + [label])

    extend([0])
    result = sorted(set(partitions))
    assert len(result) == 15
    return result


def support_masks(maps: list[tuple[int, int, int]]) -> list[tuple[int, ...]]:
    """Allowed-coordinate masks for each selector and each K5 vertex."""

    return [
        tuple(
            sum(1 << colour for colour in range(3) if selector[colour] != vertex)
            for vertex in range(5)
        )
        for selector in maps
    ]


State = tuple[tuple[int, int, int, int], tuple[int, ...], int]
Signature = tuple[tuple[int, ...], tuple[int, ...], tuple[tuple[int, int], ...]]


def state_cache_for_supports(
    partition_list: list[tuple[int, int, int, int]],
    cache: dict[tuple[int, int, int, int], list[State]],
    supports: tuple[int, int, int, int],
) -> list[State]:
    """Return feasible exact partition states for one common vertex."""

    if supports in cache:
        return cache[supports]

    independent_dimension = sum(mask.bit_count() - 1 for mask in supports)
    result: list[State] = []
    for partition in partition_list:
        block_masks = [7] * (max(partition) + 1)
        for chart, block in enumerate(partition):
            block_masks[block] &= supports[chart]
        if any(mask == 0 for mask in block_masks):
            continue
        one_dimensional = [mask for mask in block_masks if mask.bit_count() == 1]
        # Two distinct exact blocks with the same one-dimensional coordinate
        # support are necessarily proportional and are not a valid stratum.
        if len(one_dimensional) != len(set(one_dimensional)):
            continue
        stratum_dimension = sum(mask.bit_count() - 1 for mask in block_masks)
        result.append(
            (partition, tuple(block_masks), independent_dimension - stratum_dimension)
        )
    cache[supports] = result
    return result


def collect_signatures(
    representatives: list[tuple[int, int, int, int]],
    map_supports: list[tuple[int, ...]],
    partition_list: list[tuple[int, int, int, int]],
    progress_enabled: bool,
) -> tuple[set[Signature], dict[tuple[int, int, int, int], list[State]], int]:
    cache: dict[tuple[int, int, int, int], list[State]] = {}
    signatures: set[Signature] = set()
    pair_instances = 0
    for rep_index, quadruple in enumerate(representatives, start=1):
        states = [
            state_cache_for_supports(
                partition_list,
                cache,
                tuple(map_supports[quadruple[chart]][vertex] for chart in range(4)),
            )
            for vertex in COMMON_VERTICES
        ]
        for left, right in PAIR_ORDER:
            for left_partition, left_masks, _ in states[left]:
                for right_partition, right_masks, _ in states[right]:
                    edge_set = tuple(
                        sorted(
                            {
                                (left_partition[chart], right_partition[chart])
                                for chart in range(4)
                            }
                        )
                    )
                    signatures.add((left_masks, right_masks, edge_set))
                    pair_instances += 1
        if rep_index % 20_000 == 0:
            progress(
                progress_enabled,
                "signature collection",
                rep_index,
                len(signatures),
                pair_instances,
            )
    assert pair_instances == EXPECTED_PAIR_INSTANCES
    assert len(signatures) == EXPECTED_RAW_SIGNATURES
    return signatures, cache, pair_instances


COORDINATES = tuple((p, q) for p in range(3) for q in range(3))
PERMUTATION_SIGNS: dict[int, list[tuple[tuple[int, ...], int]]] = {}
for size in range(1, 5):
    signed: list[tuple[tuple[int, ...], int]] = []
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        signed.append((permutation, -1 if inversions % 2 else 1))
    PERMUTATION_SIGNS[size] = signed

# Base-5 digit weights encode exponent vectors.  A determinant of size at
# most four has exponent at most four in any variable, so no base-5 carry is
# possible.
BASE5_DIGIT_WEIGHTS = [5**index for index in range(24)]


def modular_rank(
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    edge_set: tuple[tuple[int, int], ...],
) -> int:
    """Rank at one deterministic specialization over F_PRIME."""

    left_values = [
        [(17 + 101 * block + 13 * coordinate + 3 * len(left_masks)) % PRIME or 1
         for coordinate in range(3)]
        for block in range(len(left_masks))
    ]
    right_values = [
        [(31 + 97 * block + 11 * coordinate + 3 * len(right_masks)) % PRIME or 1
         for coordinate in range(3)]
        for block in range(len(right_masks))
    ]
    matrix = [
        [
            (left_values[left][p] * right_values[right][q]) % PRIME
            if (left_masks[left] >> p) & 1 and (right_masks[right] >> q) & 1
            else 0
            for p, q in COORDINATES
        ]
        for left, right in edge_set
    ]
    rank = 0
    pivot_row = 0
    for column in range(9):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], PRIME - 2, PRIME)
        matrix[pivot_row] = [
            value * inverse % PRIME for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (old - factor * new) % PRIME
                for old, new in zip(matrix[row], matrix[pivot_row])
            ]
        rank += 1
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return rank


def determinant_polynomial_is_nonzero(
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    edge_set: tuple[tuple[int, int], ...],
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> bool:
    """Check a minor exactly by collecting exponent-vector monomials."""

    coefficients: dict[int, int] = {}
    for permutation, sign in PERMUTATION_SIGNS[len(rows)]:
        monomial_code = 0
        valid = True
        for row_index, column_index in enumerate(permutation):
            left, right = edge_set[rows[row_index]]
            p, q = COORDINATES[columns[column_index]]
            if not (
                (left_masks[left] >> p) & 1
                and (right_masks[right] >> q) & 1
            ):
                valid = False
                break
            # Multiplication of matrix entries adds variable exponents.
            monomial_code += (
                BASE5_DIGIT_WEIGHTS[3 * left + p]
                + BASE5_DIGIT_WEIGHTS[12 + 3 * right + q]
            )
        if valid:
            coefficients[monomial_code] = coefficients.get(monomial_code, 0) + sign
    return any(coefficient != 0 for coefficient in coefficients.values())


def exact_generic_rank(
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    edge_set: tuple[tuple[int, int], ...],
) -> int:
    """Return rank over Q(X,Y) by exact nonzero-minor search."""

    for size in range(len(edge_set), 0, -1):
        for rows in combinations(range(len(edge_set)), size):
            for columns in combinations(range(9), size):
                if determinant_polynomial_is_nonzero(
                    left_masks, right_masks, edge_set, rows, columns
                ):
                    return size
    return 0


def rank_cache(
    signatures: set[Signature], progress_enabled: bool
) -> tuple[dict[Signature, int], Counter[tuple[int, int]], int]:
    cache: dict[Signature, int] = {}
    histogram: Counter[tuple[int, int]] = Counter()
    modularly_deficient = 0
    for index, signature in enumerate(signatures, start=1):
        left_masks, right_masks, edge_set = signature
        cardinality = len(edge_set)
        modular = modular_rank(left_masks, right_masks, edge_set)
        if modular == cardinality:
            rank = cardinality
        else:
            modularly_deficient += 1
            rank = exact_generic_rank(left_masks, right_masks, edge_set)
        cache[signature] = rank
        histogram[(cardinality, rank)] += 1
        if index % 200_000 == 0:
            progress(progress_enabled, "rank cache", index, modularly_deficient)
    assert modularly_deficient == EXPECTED_MODULARLY_DEFICIENT
    assert dict(histogram) == EXPECTED_RANK_HISTOGRAM
    rank_hash = hashlib.sha256(repr(sorted(histogram.items())).encode()).hexdigest()
    assert rank_hash == EXPECTED_RANK_HASH
    return cache, histogram, modularly_deficient


def q_frontier(
    representatives: list[tuple[int, int, int, int]],
    map_supports: list[tuple[int, ...]],
    partition_list: list[tuple[int, int, int, int]],
    state_cache: dict[tuple[int, int, int, int], list[State]],
    ranks: dict[Signature, int],
    progress_enabled: bool,
) -> tuple[Counter[int], int, set[tuple[object, ...]], int]:
    """Enumerate all exact partition systems using NumPy min-plus tables."""

    histogram: Counter[int] = Counter()
    equality_records: set[tuple[object, ...]] = set()
    full_systems = 0
    minimum = 10**9

    for rep_index, quadruple in enumerate(representatives, start=1):
        states = [
            state_cache_for_supports(
                partition_list,
                state_cache,
                tuple(map_supports[quadruple[chart]][vertex] for chart in range(4)),
            )
            for vertex in COMMON_VERTICES
        ]
        pair_matrices: dict[tuple[int, int], np.ndarray] = {}
        pair_keys: dict[tuple[int, int], list[list[Signature]]] = {}
        for left, right in PAIR_ORDER:
            matrix = np.empty((len(states[left]), len(states[right])), dtype=np.int8)
            keys: list[list[Signature]] = [
                [None] * len(states[right]) for _ in states[left]  # type: ignore[list-item]
            ]
            for left_index, left_state in enumerate(states[left]):
                for right_index, right_state in enumerate(states[right]):
                    left_partition, left_masks, _ = left_state
                    right_partition, right_masks, _ = right_state
                    edge_set = tuple(
                        sorted(
                            {
                                (left_partition[chart], right_partition[chart])
                                for chart in range(4)
                            }
                        )
                    )
                    signature = (left_masks, right_masks, edge_set)
                    matrix[left_index, right_index] = ranks[signature]
                    keys[left_index][right_index] = signature
            pair_matrices[(left, right)] = matrix
            pair_keys[(left, right)] = keys

        delta = [
            np.array([state[2] for state in vertex_states], dtype=np.int16)
            for vertex_states in states
        ]
        values = (
            delta[0][:, None, None, None]
            + delta[1][None, :, None, None]
            + delta[2][None, None, :, None]
            + delta[3][None, None, None, :]
        )
        values = values + (
            pair_matrices[(0, 1)][:, :, None, None]
            + pair_matrices[(0, 2)][:, None, :, None]
            + pair_matrices[(0, 3)][:, None, None, :]
            + pair_matrices[(1, 2)][None, :, :, None]
            + pair_matrices[(1, 3)][None, :, None, :]
            + pair_matrices[(2, 3)][None, None, :, :]
        )
        expected_shape = tuple(len(vertex_states) for vertex_states in states)
        assert values.shape == expected_shape
        values_array = np.asarray(values)
        local_values, local_counts = np.unique(values_array, return_counts=True)
        histogram.update(
            {int(value): int(count) for value, count in zip(local_values, local_counts)}
        )
        full_systems += values_array.size
        local_minimum = int(values_array.min())
        if local_minimum < minimum:
            minimum = local_minimum
            equality_records.clear()
        if local_minimum == minimum:
            for position in np.argwhere(values_array == minimum):
                index = tuple(int(value) for value in position)
                selected = tuple(states[vertex][index[vertex]] for vertex in range(4))
                six_ranks = tuple(
                    int(pair_matrices[pair][left_index, right_index])
                    for pair, (left_index, right_index) in zip(
                        PAIR_ORDER,
                        (
                            (index[0], index[1]),
                            (index[0], index[2]),
                            (index[0], index[3]),
                            (index[1], index[2]),
                            (index[1], index[3]),
                            (index[2], index[3]),
                        ),
                    )
                )
                record = (
                    quadruple,
                    tuple(state[0] for state in selected),
                    six_ranks,
                    tuple(state[2] for state in selected),
                )
                equality_records.add(record)
        if rep_index % 5_000 == 0:
            progress(
                progress_enabled,
                "q frontier",
                rep_index,
                full_systems,
                minimum,
            )

    assert full_systems == EXPECTED_FULL_PARTITION_SYSTEMS
    assert dict(histogram) == EXPECTED_Q_HISTOGRAM
    assert minimum == 20
    # Convert the records to the stable six-tuple form used by the published
    # equality statement.
    equality_summary = {
        (
            record[1][0],
            record[1][1],
            record[1][2],
            record[1][3],
            record[2],
            record[3],
        )
        for record in equality_records
    }
    assert equality_summary == EXPECTED_EQUALITIES
    q_hash = hashlib.sha256(repr(sorted(histogram.items())).encode()).hexdigest()
    assert q_hash == EXPECTED_Q_HASH
    return histogram, minimum, equality_records, full_systems


def run(progress_enabled: bool) -> dict[str, object]:
    maps = selector_maps()
    assert len(maps) == 120
    map_supports = support_masks(maps)
    representatives, selector_hash = selector_orbits(maps, progress_enabled)
    partition_list = restricted_growth_partitions()
    signatures, state_cache, pair_instances = collect_signatures(
        representatives, map_supports, partition_list, progress_enabled
    )
    ranks, rank_histogram, modularly_deficient = rank_cache(
        signatures, progress_enabled
    )
    # The set is only needed for the rank phase; dropping it keeps the q phase
    # below the memory ceiling on ordinary CI workers.
    del signatures
    q_histogram, minimum, equality_records, full_systems = q_frontier(
        representatives,
        map_supports,
        partition_list,
        state_cache,
        ranks,
        progress_enabled,
    )
    return {
        "status": "verified_finite_support_segre_generic_rank_census",
        "field": "characteristic_zero_generic_partition_strata",
        "global_conjecture": "UNRESOLVED",
        "selector_maps": len(maps),
        "selector_multisets": EXPECTED_SELECTOR_MULTISETS,
        "selector_orbits": len(representatives),
        "selector_representative_sha256": selector_hash,
        "partition_types": len(partition_list),
        "pair_instances": pair_instances,
        "raw_support_labelled_signatures": EXPECTED_RAW_SIGNATURES,
        "legacy_packed_signature_count": 677_260,
        "legacy_packed_signature_scope": (
            "historical packed/quotiented key; not used by this verifier"
        ),
        "modular_prime": PRIME,
        "modularly_deficient_signatures": modularly_deficient,
        "rank_histogram_c_by_r": {
            f"{cardinality},{rank}": count
            for (cardinality, rank), count in sorted(rank_histogram.items())
        },
        "rank_histogram_sha256": EXPECTED_RANK_HASH,
        "full_partition_systems": full_systems,
        "q_histogram": {str(value): count for value, count in sorted(q_histogram.items())},
        "q_histogram_sha256": EXPECTED_Q_HASH,
        "q_minimum": minimum,
        "q_equalities": [
            {
                "selector_ids": list(record[0]),
                "partitions": [list(partition) for partition in record[1]],
                "ranks_01_02_03_12_13_23": list(record[2]),
                "delta_by_vertex": list(record[3]),
            }
            for record in sorted(equality_records, key=repr)
        ],
        "rank_degeneracy_components": "not classified",
        "b_all_and_seventy_pencil_gluing": "open",
        "is_global_krenn_gu_proof": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress progress; the JSON result is still printed",
    )
    args = parser.parse_args()
    result = run(not args.quiet)
    print("four-K5 support-Segre generic-rank census: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
