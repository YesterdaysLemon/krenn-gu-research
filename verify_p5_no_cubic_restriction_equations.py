"""Verify that the P5 restriction image has no cubic equations."""

from __future__ import annotations

import itertools
import json
import math
import random
from collections import Counter

import numpy as np


PRIME = 5
MODES = 5
PARTITIONS = ("T", "A", "V")
S3 = tuple(itertools.permutations(range(3)))
SEED = 20_260_727


def compose(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(3))


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * 3
    for old, new in enumerate(permutation):
        output[new] = old
    return tuple(output)


def sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    remaining = set(range(3))
    lengths = []
    while remaining:
        start = min(remaining)
        current = start
        length = 0
        while current in remaining:
            remaining.remove(current)
            current = permutation[current]
            length += 1
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def standard_representation(
    permutation: tuple[int, ...],
) -> np.ndarray:
    basis = (
        np.array((1, -1, 0), dtype=np.int64),
        np.array((0, 1, -1), dtype=np.int64),
    )
    matrix = np.zeros((2, 2), dtype=np.int64)
    for column, vector in enumerate(basis):
        image = np.zeros(3, dtype=np.int64)
        for old, new in enumerate(permutation):
            image[new] = vector[old]
        matrix[0, column] = image[0]
        matrix[1, column] = -image[2]
    return matrix % PRIME


REPRESENTATIONS = {
    "T": {
        permutation: np.ones((1, 1), dtype=np.int64)
        for permutation in S3
    },
    "A": {
        permutation: np.array(
            ((sign(permutation) % PRIME,),), dtype=np.int64
        )
        for permutation in S3
    },
    "V": {
        permutation: standard_representation(permutation)
        for permutation in S3
    },
}


def check_representations() -> None:
    expected_characters = {
        "T": {(1, 1, 1): 1, (2, 1): 1, (3,): 1},
        "A": {(1, 1, 1): 1, (2, 1): -1, (3,): 1},
        "V": {(1, 1, 1): 2, (2, 1): 0, (3,): -1},
    }
    for kind, matrices in REPRESENTATIONS.items():
        identity = np.eye(matrices[S3[0]].shape[0], dtype=np.int64)
        if not np.array_equal(matrices[S3[0]] % PRIME, identity):
            raise AssertionError(f"{kind} identity matrix failed")
        for permutation in S3:
            observed_character = (
                int(np.trace(matrices[permutation])) % PRIME
            )
            expected_character = (
                expected_characters[kind][cycle_type(permutation)]
                % PRIME
            )
            if observed_character != expected_character:
                raise AssertionError(
                    f"{kind} character table mismatch"
                )
        for left in S3:
            for right in S3:
                product = (
                    matrices[left] @ matrices[right] % PRIME
                )
                expected = matrices[compose(left, right)] % PRIME
                if not np.array_equal(product, expected):
                    raise AssertionError(
                        f"{kind} representation multiplication failed"
                    )
        degree = identity.shape[0]
        inverse_order = pow(len(S3), -1, PRIME)
        for row in range(degree):
            for column in range(degree):
                matrix_unit = np.zeros_like(identity)
                for permutation in S3:
                    coefficient = (
                        degree
                        * inverse_order
                        * int(
                            matrices[inverse(permutation)][
                                column, row
                            ]
                        )
                    ) % PRIME
                    matrix_unit += (
                        coefficient * matrices[permutation]
                    )
                expected = np.zeros_like(identity)
                expected[row, column] = 1
                if not np.array_equal(
                    matrix_unit % PRIME, expected
                ):
                    raise AssertionError(
                        f"{kind} matrix-unit orthogonality failed"
                    )


def permute_covector(
    covector: np.ndarray,
    permutation: tuple[int, ...],
) -> np.ndarray:
    result = np.zeros_like(covector)
    inverse_permutation = inverse(permutation)
    for indices in itertools.product(
        range(covector.shape[0]), repeat=3
    ):
        source = tuple(
            indices[inverse_permutation[position]]
            for position in range(3)
        )
        result[indices] = covector[source]
    return result


def check_permutation_action() -> None:
    covector = np.arange(27, dtype=np.int64).reshape((3,) * 3)
    for left in S3:
        for right in S3:
            observed = permute_covector(
                permute_covector(covector, left), right
            )
            expected = permute_covector(
                covector, compose(left, right)
            )
            if not np.array_equal(observed, expected):
                raise AssertionError(
                    "copy-permutation action multiplication failed"
                )


def matrix_unit_covectors(
    dimension: int,
    kind: str,
    rng: random.Random,
) -> np.ndarray:
    representation = REPRESENTATIONS[kind]
    degree = representation[S3[0]].shape[0]
    seed = np.fromiter(
        (
            rng.randrange(PRIME)
            for _ in range(dimension**3)
        ),
        dtype=np.int64,
        count=dimension**3,
    ).reshape((dimension,) * 3)
    output = np.zeros((degree,) + seed.shape, dtype=np.int64)
    fixed_row = 0
    inverse_order = pow(len(S3), -1, PRIME)
    for column in range(degree):
        for permutation in S3:
            coefficient = (
                degree
                * inverse_order
                * int(
                    representation[inverse(permutation)][
                        column, fixed_row
                    ]
                )
            ) % PRIME
            output[column] += (
                coefficient
                * permute_covector(seed, permutation)
            )
    return output % PRIME


def permanent_copy_contraction(
    local_covectors: list[np.ndarray],
) -> np.ndarray:
    states = {
        (0, 0, 0): np.array(1, dtype=np.int64)
    }
    full_mask = (1 << 5) - 1
    for local in local_covectors:
        next_states: dict[tuple[int, int, int], np.ndarray] = {}
        for masks, value in states.items():
            unused = [
                [
                    source
                    for source in range(5)
                    if not mask & (1 << source)
                ]
                for mask in masks
            ]
            for sources in itertools.product(*unused):
                new_masks = tuple(
                    mask | (1 << source)
                    for mask, source in zip(
                        masks, sources, strict=True
                    )
                )
                term = (
                    np.multiply.outer(
                        value,
                        local[(slice(None), *sources)],
                    )
                    % PRIME
                )
                if new_masks in next_states:
                    next_states[new_masks] = (
                        next_states[new_masks] + term
                    ) % PRIME
                else:
                    next_states[new_masks] = term
        states = next_states
    if set(states) != {(full_mask, full_mask, full_mask)}:
        raise AssertionError("permanent-copy DP did not close")
    return states[(full_mask, full_mask, full_mask)].reshape(-1)


def check_permanent_copy_dp() -> None:
    permutations = (
        tuple(range(5)),
        (1, 2, 3, 4, 0),
        (4, 3, 2, 1, 0),
    )
    local_covectors = []
    for mode in range(MODES):
        local = np.zeros((1, 5, 5, 5), dtype=np.int64)
        local[
            0,
            permutations[0][mode],
            permutations[1][mode],
            permutations[2][mode],
        ] = 1
        local_covectors.append(local)
    observed = permanent_copy_contraction(local_covectors)
    if observed.tolist() != [1]:
        raise AssertionError("permanent-copy DP isolated witness failed")


def pivot_columns_mod(
    matrix: np.ndarray,
) -> tuple[int, list[int]]:
    reduced = matrix.copy() % PRIME
    rank = 0
    pivots = []
    for column in range(reduced.shape[1]):
        pivot = next(
            (
                row
                for row in range(rank, reduced.shape[0])
                if reduced[row, column]
            ),
            None,
        )
        if pivot is None:
            continue
        reduced[[rank, pivot]] = reduced[[pivot, rank]]
        inverse_pivot = pow(
            int(reduced[rank, column]), -1, PRIME
        )
        reduced[rank] = (
            reduced[rank] * inverse_pivot % PRIME
        )
        for row in range(reduced.shape[0]):
            if row != rank and reduced[row, column]:
                reduced[row] = (
                    reduced[row]
                    - reduced[row, column] * reduced[rank]
                ) % PRIME
        pivots.append(column)
        rank += 1
        if rank == reduced.shape[0]:
            break
    return rank, pivots


def determinant_mod(matrix: np.ndarray) -> int:
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("determinant requires a square matrix")
    work = matrix.copy() % PRIME
    determinant = 1
    for column in range(work.shape[1]):
        pivot = next(
            (
                row
                for row in range(column, work.shape[0])
                if work[row, column]
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[[column, pivot]] = work[[pivot, column]]
            determinant = -determinant
        pivot_value = int(work[column, column])
        determinant = determinant * pivot_value % PRIME
        inverse_pivot = pow(pivot_value, -1, PRIME)
        for row in range(column + 1, work.shape[0]):
            multiplier = work[row, column] * inverse_pivot % PRIME
            work[row] = (
                work[row] - multiplier * work[column]
            ) % PRIME
    return determinant % PRIME


def full_rank_witness(
    matrix: np.ndarray,
    expected_rank: int,
) -> tuple[list[int], list[int], int]:
    rank, columns = pivot_columns_mod(matrix)
    if rank != expected_rank:
        raise AssertionError(
            f"multiplicity rank {rank} != {expected_rank}"
        )
    restricted = matrix[:, columns]
    row_rank, rows = pivot_columns_mod(restricted.T)
    if row_rank != expected_rank:
        raise AssertionError("independent-row extraction failed")
    determinant = determinant_mod(matrix[np.ix_(rows, columns)])
    if determinant == 0:
        raise AssertionError("recorded full-rank minor vanished")
    return rows, columns, determinant


def diagonal_action(
    types: tuple[str, ...],
    permutation: tuple[int, ...],
) -> np.ndarray:
    output = np.ones((1, 1), dtype=np.int64)
    for kind in types:
        output = np.kron(
            output, REPRESENTATIONS[kind][permutation]
        ) % PRIME
    return output


def require_invariant(
    types: tuple[str, ...],
    vector: np.ndarray,
) -> None:
    for permutation in S3:
        image = diagonal_action(types, permutation) @ vector % PRIME
        if not np.array_equal(image, vector % PRIME):
            raise AssertionError(
                "sampled multiplicity vector is not S3-invariant"
            )


def invariant_multiplicity(types: tuple[str, ...]) -> int:
    character = {
        "T": (1, 1, 1),
        "A": (1, -1, 1),
        "V": (2, 0, -1),
    }
    class_sizes = (1, 3, 2)
    numerator = sum(
        class_size
        * math_product(
            character[kind][class_index] for kind in types
        )
        for class_index, class_size in enumerate(class_sizes)
    )
    if numerator % 6:
        raise AssertionError("nonintegral S3 invariant multiplicity")
    return numerator // 6


def math_product(values) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def type_representatives() -> tuple[tuple[str, ...], ...]:
    output = []
    for v_count in range(6):
        for a_count in range(6 - v_count):
            t_count = 5 - v_count - a_count
            types = (
                ("V",) * v_count
                + ("A",) * a_count
                + ("T",) * t_count
            )
            if invariant_multiplicity(types):
                output.append(types)
    return tuple(output)


def module_tuple_orbit_size(types: tuple[str, ...]) -> int:
    denominator = math_product(
        math.factorial(multiplicity)
        for multiplicity in Counter(types).values()
    )
    return math.factorial(MODES) // denominator


def main() -> None:
    check_representations()
    check_permutation_action()
    check_permanent_copy_dp()
    all_module_tuples = tuple(
        types
        for types in itertools.product(PARTITIONS, repeat=MODES)
        if invariant_multiplicity(types)
    )
    if len(all_module_tuples) != 147:
        raise AssertionError("cubic module-tuple count changed")
    schur_dimensions = {"T": 10, "A": 1, "V": 8}
    decomposed_dimension = sum(
        invariant_multiplicity(types)
        * math_product(schur_dimensions[kind] for kind in types)
        for types in all_module_tuples
    )
    tensor_dimension = 3**MODES
    cubic_dimension = math.comb(tensor_dimension + 2, 3)
    if decomposed_dimension != cubic_dimension:
        raise AssertionError("cubic Schur-Weyl decomposition is incomplete")

    rng = random.Random(SEED)
    records = []
    for types in type_representatives():
        multiplicity = invariant_multiplicity(types)
        samples = multiplicity + 3
        permanent_rows = []
        for _sample in range(samples):
            permanent_covectors = [
                matrix_unit_covectors(5, kind, rng)
                for kind in types
            ]
            vector = permanent_copy_contraction(
                permanent_covectors
            )
            require_invariant(types, vector)
            permanent_rows.append(vector)
        permanent_matrix = np.vstack(permanent_rows)
        rows, columns, determinant = full_rank_witness(
            permanent_matrix, multiplicity
        )
        records.append(
            {
                "types": types,
                "module_tuple_orbit_size": (
                    module_tuple_orbit_size(types)
                ),
                "invariant_multiplicity": multiplicity,
                "ambient_specht_tensor_dimension": (
                    permanent_matrix.shape[1]
                ),
                "samples": samples,
                "p5_multiplicity_rank": multiplicity,
                "full_rank_row_indices": rows,
                "full_rank_column_indices": columns,
                "minor_determinant_mod_5": determinant,
            }
        )
        print(json.dumps(records[-1]), flush=True)
    if (
        sum(record["module_tuple_orbit_size"] for record in records)
        != len(all_module_tuples)
    ):
        raise AssertionError("type representatives do not cover modules")
    print(
        json.dumps(
            {
                "verified": True,
                "field_for_rank_witnesses": "F_5",
                "degree": 3,
                "target_tensor_space_dimension": tensor_dimension,
                "cubic_polynomial_space_dimension": cubic_dimension,
                "nonzero_irreducible_module_tuples": len(
                    all_module_tuples
                ),
                "representative_module_types": len(records),
                "records": records,
                "all_p5_multiplicity_ranks_full": True,
                "cubic_pullback_injective_over_Q": True,
                "nonzero_cubic_restriction_equations": 0,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
