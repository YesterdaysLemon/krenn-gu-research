#!/usr/bin/env python3
"""Verify that the P5 restriction image has no quadratic equations."""

from __future__ import annotations

import itertools
import json
import math


MODES = tuple(range(5))
SOURCES = tuple(range(5))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))


def witness_permutation(
    exterior_modes: tuple[int, ...],
) -> tuple[int, ...]:
    permutation = list(SOURCES)
    if len(exterior_modes) == 2:
        left, right = exterior_modes
        permutation[left], permutation[right] = (
            permutation[right],
            permutation[left],
        )
    elif len(exterior_modes) == 4:
        for left, right in zip(
            exterior_modes,
            exterior_modes[1:] + exterior_modes[:1],
            strict=True,
        ):
            permutation[left] = right
    elif exterior_modes:
        raise ValueError("only even exterior subsets occur")
    return tuple(permutation)


def local_factor(
    observed: tuple[int, int],
    target: tuple[int, int],
    exterior: bool,
) -> int:
    if exterior:
        if observed == target:
            return 1
        if observed == tuple(reversed(target)):
            return -1
        return 0
    return int(tuple(sorted(observed)) == target)


def projection_coefficient(
    exterior_modes: tuple[int, ...],
) -> tuple[int, tuple[int, ...]]:
    identity = tuple(SOURCES)
    witness = witness_permutation(exterior_modes)
    exterior = set(exterior_modes)
    target = tuple(
        (
            (identity[mode], witness[mode])
            if mode in exterior
            else tuple(sorted((identity[mode], witness[mode])))
        )
        for mode in MODES
    )
    coefficient = 0
    contributing_pairs = []
    for left in PERMUTATIONS:
        for right in PERMUTATIONS:
            value = 1
            for mode in MODES:
                value *= local_factor(
                    (left[mode], right[mode]),
                    target[mode],
                    mode in exterior,
                )
                if value == 0:
                    break
            if value:
                coefficient += value
                contributing_pairs.append(
                    PERMUTATIONS.index(left) * len(PERMUTATIONS)
                    + PERMUTATIONS.index(right)
                )
    return coefficient, tuple(contributing_pairs)


def main() -> None:
    module_dimensions = {}
    total_dimension = 0
    records = []
    for exterior_count in (0, 2, 4):
        for exterior_modes in itertools.combinations(
            MODES, exterior_count
        ):
            dimension = 3**exterior_count * 6 ** (
                len(MODES) - exterior_count
            )
            module_dimensions[exterior_modes] = dimension
            total_dimension += dimension
            coefficient, contributing_pairs = (
                projection_coefficient(exterior_modes)
            )
            expected_coefficient = 1 if not exterior_modes else 2
            expected_pairs = 1 if not exterior_modes else 2
            if coefficient != expected_coefficient:
                raise AssertionError(
                    f"projection vanished for {exterior_modes}: "
                    f"{coefficient}"
                )
            if len(contributing_pairs) != expected_pairs:
                raise AssertionError(
                    "witness coefficient was not isolated"
                )
            records.append(
                {
                    "exterior_modes": exterior_modes,
                    "symmetric_modes": tuple(
                        mode
                        for mode in MODES
                        if mode not in exterior_modes
                    ),
                    "irreducible_module_dimension": dimension,
                    "witness_permutation": witness_permutation(
                        exterior_modes
                    ),
                    "nonzero_projection_coefficient": coefficient,
                    "contributing_ordered_permutation_pairs": (
                        len(contributing_pairs)
                    ),
                }
            )

    tensor_dimension = 3**5
    expected_quadratic_dimension = (
        tensor_dimension * (tensor_dimension + 1) // 2
    )
    if total_dimension != expected_quadratic_dimension:
        raise AssertionError("quadratic Cauchy decomposition is incomplete")
    if len(records) != 16:
        raise AssertionError("quadratic decomposition is not multiplicity-free")
    if sum(math.comb(5, count) for count in (0, 2, 4)) != 16:
        raise AssertionError("even-parity module count changed")

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "homogeneous quadratic equations on the full local "
                    "restriction image of the order-five permanent tensor"
                ),
                "target_tensor_space_dimension": tensor_dimension,
                "quadratic_polynomial_space_dimension": (
                    expected_quadratic_dimension
                ),
                "multiplicity_free_irreducible_modules": len(records),
                "all_module_pullbacks_nonzero": True,
                "quadratic_pullback_injective": True,
                "nonzero_quadratic_restriction_equations": 0,
                "records": records,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
