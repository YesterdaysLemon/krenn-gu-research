#!/usr/bin/env python3
"""Probe degree-six scalar invariants on generic P5 restrictions.

This is numerical discovery only.  It identifies an invariant basis and
estimates the rank of its pullback to random local restrictions of P5.
"""

from __future__ import annotations

import argparse
import itertools
import json
import string
from pathlib import Path

import numpy as np
import opt_einsum as oe
from scipy.linalg import qr


MODES = 5
COPIES = 6
EXPECTED_INVARIANT_DIMENSION = 11


def epsilon_tensor() -> np.ndarray:
    epsilon = np.zeros((3, 3, 3), dtype=np.float64)
    for permutation in itertools.permutations(range(3)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        epsilon[permutation] = (-1) ** inversions
    return epsilon


def local_partitions() -> tuple[
    tuple[tuple[int, ...], tuple[int, ...]], ...
]:
    output = []
    copies = set(range(COPIES))
    for pair in itertools.combinations(range(1, COPIES), 2):
        first = (0, *pair)
        second = tuple(sorted(copies - set(first)))
        output.append((first, second))
    if len(output) != 10:
        raise AssertionError("six-copy triple partitions changed")
    return tuple(output)


def contraction_expression(
    pattern: tuple[int, ...],
    partitions: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
):
    labels = list(string.ascii_letters[: MODES * COPIES])

    def label(copy: int, mode: int) -> str:
        return labels[MODES * copy + mode]

    subscripts = []
    shapes = []
    for copy in range(COPIES):
        subscripts.append(
            "".join(label(copy, mode) for mode in range(MODES))
        )
        shapes.append((3,) * MODES)
    for mode, partition_index in enumerate(pattern):
        for block in partitions[partition_index]:
            subscripts.append(
                "".join(label(copy, mode) for copy in block)
            )
            shapes.append((3, 3, 3))
    expression = ",".join(subscripts) + "->"
    return oe.contract_expression(
        expression,
        *shapes,
        optimize="random-greedy-128",
    )


def permanent_tensor() -> np.ndarray:
    tensor = np.zeros((5,) * MODES, dtype=np.float64)
    for permutation in itertools.permutations(range(5)):
        tensor[permutation] = 1.0
    return tensor


def restriction_expression():
    return oe.contract_expression(
        "ai,bj,ck,dl,em,ijklm->abcde",
        *((3, 5),) * MODES,
        (5,) * MODES,
        optimize="optimal",
    )


def normalize(tensor: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(tensor)
    if norm == 0:
        raise AssertionError("sampled zero tensor")
    return tensor / norm


def numerical_rank(matrix: np.ndarray) -> tuple[int, list[float]]:
    singular_values = np.linalg.svd(
        matrix, compute_uv=False, full_matrices=False
    )
    tolerance = (
        1_000
        * np.finfo(np.float64).eps
        * max(matrix.shape)
        * singular_values[0]
    )
    rank = int(np.count_nonzero(singular_values > tolerance))
    return rank, singular_values.tolist()


def evaluate(
    tensor: np.ndarray,
    expressions: list,
    epsilon: np.ndarray,
) -> np.ndarray:
    operands = [tensor] * COPIES + [
        epsilon for _mode in range(MODES) for _block in range(2)
    ]
    return np.array(
        [expression(*operands) for expression in expressions],
        dtype=np.float64,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--candidate-patterns", type=int, default=64)
    parser.add_argument("--generic-samples", type=int, default=24)
    parser.add_argument("--restriction-samples", type=int, default=32)
    args = parser.parse_args()
    if args.candidate_patterns < EXPECTED_INVARIANT_DIMENSION:
        raise ValueError("too few candidate patterns")

    rng = np.random.default_rng(args.seed)
    partitions = local_partitions()
    possible = [
        (0, *tail)
        for tail in itertools.product(
            range(len(partitions)), repeat=MODES - 1
        )
    ]
    rng.shuffle(possible)
    patterns = possible[: args.candidate_patterns]
    expressions = [
        contraction_expression(pattern, partitions)
        for pattern in patterns
    ]
    epsilon = epsilon_tensor()

    generic_matrix = np.vstack(
        [
            evaluate(
                normalize(rng.normal(size=(3,) * MODES)),
                expressions,
                epsilon,
            )
            for _sample in range(args.generic_samples)
        ]
    )
    generic_rank, generic_singular_values = numerical_rank(
        generic_matrix
    )
    if generic_rank != EXPECTED_INVARIANT_DIMENSION:
        raise AssertionError(
            "candidate contractions did not span the verified "
            f"{EXPECTED_INVARIANT_DIMENSION}-dimensional space: "
            f"rank {generic_rank}"
        )

    _q, _r, pivots = qr(
        generic_matrix, mode="economic", pivoting=True
    )
    selected = list(
        map(int, pivots[:EXPECTED_INVARIANT_DIMENSION])
    )
    selected_rank, _selected_singular_values = numerical_rank(
        generic_matrix[:, selected]
    )
    if selected_rank != EXPECTED_INVARIANT_DIMENSION:
        raise AssertionError("pivoted invariant basis extraction failed")
    basis_patterns = [patterns[index] for index in selected]
    basis_expressions = [expressions[index] for index in selected]

    source = permanent_tensor()
    restrict = restriction_expression()
    restriction_matrix = []
    for _sample in range(args.restriction_samples):
        maps = [
            rng.normal(size=(3, 5)) for _mode in range(MODES)
        ]
        tensor = normalize(restrict(*maps, source))
        restriction_matrix.append(
            evaluate(tensor, basis_expressions, epsilon)
        )
    restriction_matrix_array = np.vstack(restriction_matrix)
    restriction_rank, restriction_singular_values = numerical_rank(
        restriction_matrix_array
    )

    delta = np.zeros((3,) * MODES, dtype=np.float64)
    for colour in range(3):
        delta[(colour,) * MODES] = 1.0
    delta_values = evaluate(
        normalize(delta), basis_expressions, epsilon
    )

    payload = {
        "status": "EXPLORATORY_NUMERICAL_INVARIANT_PULLBACK",
        "seed": args.seed,
        "candidate_patterns": len(patterns),
        "generic_samples": args.generic_samples,
        "verified_invariant_space_dimension": (
            EXPECTED_INVARIANT_DIMENSION
        ),
        "observed_generic_rank": generic_rank,
        "generic_singular_values": generic_singular_values,
        "basis_patterns": basis_patterns,
        "restriction_samples": args.restriction_samples,
        "observed_p5_pullback_rank": restriction_rank,
        "p5_pullback_singular_values": restriction_singular_values,
        "sampled_linear_pullback_kernel_dimension": (
            EXPECTED_INVARIANT_DIMENSION - restriction_rank
        ),
        "delta_basis_values": delta_values.tolist(),
        "degree_six_linear_separator_found": False,
        "exact_certificate": False,
        "global_conjecture_resolved": False,
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
