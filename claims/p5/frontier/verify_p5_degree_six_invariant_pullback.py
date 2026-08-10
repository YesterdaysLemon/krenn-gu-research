#!/usr/bin/env python3
"""Verify that degree-six scalar invariants do not separate P5 from Delta3.

The calculation is exact modulo five.  A nonzero evaluation determinant
modulo five proves the corresponding integer determinant is nonzero over
the rationals.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import string
from collections import Counter

import numpy as np

import sys
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

import analyze_p5_degree_six_invariant_space as SPACE


PRIME = 5
SEED = 20_260_729
PATTERNS = (
    (0, 3, 5, 3, 3),
    (0, 4, 8, 0, 0),
    (0, 5, 5, 5, 9),
    (0, 0, 3, 4, 0),
    (0, 2, 5, 0, 1),
    (0, 0, 2, 8, 1),
    (0, 2, 0, 5, 6),
    (0, 6, 9, 2, 9),
    (0, 3, 2, 8, 0),
    (0, 4, 7, 8, 8),
    (0, 5, 9, 6, 8),
)
# Explicit contraction paths avoid trusting a tensor-network optimizer.
CONTRACTION_PATHS = (
    ((4, 13), (0, 7), (2, 5), (0, 3), (1, 4), (0, 2), (3, 4),
     (7, 8), (1, 3), (0, 5), (1, 5), (1, 3), (0, 3), (0, 2),
     (0, 1)),
    ((0, 8), (4, 11), (1, 8), (0, 8), (1, 4), (2, 7), (8, 9),
     (4, 8), (0, 7), (1, 6), (2, 5), (1, 3), (1, 3), (1, 2),
     (0, 1)),
    ((3, 11), (4, 6), (3, 10), (0, 7), (1, 2), (0, 5), (1, 5),
     (3, 8), (2, 7), (5, 6), (4, 5), (1, 3), (2, 3), (1, 2),
     (0, 1)),
    ((4, 15), (4, 12), (0, 11), (2, 8), (1, 4), (0, 4), (3, 8),
     (5, 8), (2, 5), (0, 5), (3, 5), (1, 3), (0, 3), (0, 2),
     (0, 1)),
    ((0, 14), (4, 10), (3, 11), (0, 8), (1, 7), (0, 5), (3, 5),
     (6, 8), (1, 7), (3, 6), (4, 5), (0, 3), (1, 3), (1, 2),
     (0, 1)),
    ((5, 7), (1, 6), (2, 8), (0, 8), (1, 7), (0, 5), (1, 6),
     (3, 8), (0, 4), (1, 5), (2, 5), (1, 3), (0, 3), (0, 2),
     (0, 1)),
    ((1, 8), (2, 6), (1, 8), (1, 9), (1, 5), (0, 1), (0, 8),
     (4, 8), (1, 7), (4, 6), (2, 5), (0, 3), (1, 3), (0, 1),
     (0, 1)),
    ((5, 7), (1, 7), (1, 7), (0, 8), (0, 7), (0, 3), (3, 8),
     (5, 8), (1, 3), (2, 5), (0, 5), (3, 4), (1, 3), (1, 2),
     (0, 1)),
    ((3, 11), (4, 10), (0, 10), (2, 6), (1, 6), (0, 3), (1, 5),
     (3, 8), (2, 7), (3, 6), (3, 5), (0, 2), (2, 3), (1, 2),
     (0, 1)),
    ((0, 8), (2, 12), (3, 5), (1, 9), (0, 2), (0, 1), (0, 5),
     (3, 8), (1, 7), (2, 6), (4, 5), (1, 4), (1, 3), (1, 2),
     (0, 1)),
    ((4, 15), (3, 10), (0, 9), (1, 5), (1, 5), (0, 4), (0, 6),
     (5, 8), (1, 4), (4, 6), (1, 3), (2, 4), (2, 3), (1, 2),
     (0, 1)),
)


def invariant_dimension() -> int:
    tableaux = SPACE.standard_tableaux()
    adjacent = SPACE.adjacent_matrices(tableaux)
    rows = [
        (
            SPACE.class_size(cycle_type),
            SPACE.character(cycle_type, adjacent),
        )
        for cycle_type in SPACE.partitions(SPACE.DEGREE)
    ]
    if sum(size for size, _character in rows) != math.factorial(6):
        raise AssertionError("S6 class sizes changed")
    if (
        sum(size * character**2 for size, character in rows)
        != math.factorial(6)
    ):
        raise AssertionError("Specht character orthogonality failed")
    numerator = sum(
        size * character**SPACE.MODES
        for size, character in rows
    )
    if numerator % math.factorial(6):
        raise AssertionError("invariant multiplicity is not integral")
    return numerator // math.factorial(6)


def local_partitions():
    copies = set(range(6))
    return tuple(
        (
            (0, *pair),
            tuple(sorted(copies - {0, *pair})),
        )
        for pair in itertools.combinations(range(1, 6), 2)
    )


def epsilon_tensor() -> np.ndarray:
    epsilon = np.zeros((3, 3, 3), dtype=np.int64)
    for permutation in itertools.permutations(range(3)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        epsilon[permutation] = (-1) ** inversions
    return epsilon


def expression(pattern: tuple[int, ...]) -> str:
    labels = list(string.ascii_letters[:30])

    def label(copy: int, mode: int) -> str:
        return labels[5 * copy + mode]

    subscripts = [
        "".join(label(copy, mode) for mode in range(5))
        for copy in range(6)
    ]
    partitions = local_partitions()
    for mode, partition_index in enumerate(pattern):
        for block in partitions[partition_index]:
            subscripts.append(
                "".join(label(copy, mode) for copy in block)
            )
    return ",".join(subscripts) + "->"


def evaluate(tensor: np.ndarray) -> np.ndarray:
    epsilon = epsilon_tensor()
    operands = [tensor] * 6 + [epsilon] * 10
    return np.array(
        [
            int(
                np.einsum(
                    expression(pattern),
                    *operands,
                    optimize=["einsum_path", *path],
                )
            )
            % PRIME
            for pattern, path in zip(
                PATTERNS, CONTRACTION_PATHS, strict=True
            )
        ],
        dtype=np.int64,
    )


def random_array(
    rng: random.Random,
    shape: tuple[int, ...],
) -> np.ndarray:
    count = math.prod(shape)
    return np.fromiter(
        (rng.randrange(PRIME) for _ in range(count)),
        dtype=np.int64,
        count=count,
    ).reshape(shape)


def permanent_restriction(maps: list[np.ndarray]) -> np.ndarray:
    output = np.zeros((3,) * 5, dtype=np.int64)
    for permutation in itertools.permutations(range(5)):
        term = maps[0][:, permutation[0]]
        for mode in range(1, 5):
            term = np.multiply.outer(
                term, maps[mode][:, permutation[mode]]
            )
        output += term
    return output % PRIME


def rref_mod(
    matrix: np.ndarray,
) -> tuple[int, list[int], np.ndarray]:
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
        inverse = pow(
            int(reduced[rank, column]), -1, PRIME
        )
        reduced[rank] = reduced[rank] * inverse % PRIME
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
    return rank, pivots, reduced


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
        inverse = pow(pivot_value, -1, PRIME)
        for row in range(column + 1, work.shape[0]):
            multiplier = work[row, column] * inverse % PRIME
            work[row] = (
                work[row] - multiplier * work[column]
            ) % PRIME
    return determinant % PRIME


def full_rank_witness(
    matrix: np.ndarray,
) -> tuple[list[int], int]:
    rank, row_indices, _reduced = rref_mod(matrix.T)
    if rank != len(PATTERNS):
        raise AssertionError(f"evaluation rank is only {rank}")
    square = matrix[row_indices]
    determinant = determinant_mod(square)
    if determinant == 0:
        raise AssertionError("selected evaluation minor vanished")
    return row_indices, determinant


def main() -> None:
    if invariant_dimension() != 11 or len(PATTERNS) != 11:
        raise AssertionError("degree-six invariant dimension changed")
    worst_case_integer = 3**30 * (PRIME - 1) ** 6
    if worst_case_integer >= np.iinfo(np.int64).max:
        raise AssertionError("int64 contraction bound is unsafe")

    rng = random.Random(SEED)
    generic = np.vstack(
        [
            evaluate(random_array(rng, (3,) * 5))
            for _sample in range(32)
        ]
    )
    generic_rows, generic_determinant = full_rank_witness(generic)

    restriction_maps = [
        [
            random_array(rng, (3, 5))
            for _mode in range(5)
        ]
        for _sample in range(48)
    ]
    restrictions = np.vstack(
        [
            evaluate(permanent_restriction(maps))
            for maps in restriction_maps
        ]
    )
    restriction_rows, restriction_determinant = full_rank_witness(
        restrictions
    )

    delta = np.zeros((3,) * 5, dtype=np.int64)
    for colour in range(3):
        delta[(colour,) * 5] = 1

    print(
        json.dumps(
            {
                "verified": True,
                "field_for_independence_witness": "F_5",
                "degree": 6,
                "local_group": "SL(3)^5",
                "invariant_space_dimension_over_Q": len(PATTERNS),
                "basis_patterns": PATTERNS,
                "generic_evaluation_samples": len(generic),
                "generic_full_rank_row_indices": generic_rows,
                "generic_minor_determinant_mod_5": generic_determinant,
                "p5_restriction_samples": len(restrictions),
                "p5_full_rank_row_indices": restriction_rows,
                "p5_minor_determinant_mod_5": (
                    restriction_determinant
                ),
                "delta_basis_values_mod_5": evaluate(delta).tolist(),
                "degree_six_invariant_pullback_injective": True,
                "degree_six_scalar_invariant_separator_exists": False,
                "scope": (
                    "homogeneous degree-six SL(3)^5 scalar invariants"
                ),
                "higher_degree_or_noninvariant_separator_excluded": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
