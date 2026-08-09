#!/usr/bin/env python3
"""Independent no-import audit of the kernel-support contraction theorem."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md"
EDGES = tuple(itertools.combinations(range(6), 2))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
KERNEL_MODES = (1, 3, 5)
DOUBLE_KERNEL_MODES = (1, 3)


def permanent(matrix) -> int:
    return sum(
        matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
        * matrix[3][permutation[3]]
        for permutation in PERMUTATIONS
    )


def annihilator_rows(kernel):
    a, b, c = kernel
    assert a
    first = (b, -a, 0)
    second = (c, 0, -a)
    return (
        first,
        second,
        tuple(first[index] + second[index] for index in range(3)),
        tuple(2 * first[index] - second[index] for index in range(3)),
    )


def audit_data():
    kernels = {
        1: (1, -2, 3),
        3: (2, 1, -1),
        5: (3, -1, 2),
    }
    common = [
        ((1, 2, -1), (0, 1, 3), (2, -1, 1), (1, 0, 2)),
        None,
        ((2, 0, 1), (-1, 3, 2), (1, 1, -2), (0, 2, 3)),
        None,
        ((1, -2, 0), (3, 1, 2), (-1, 0, 1), (2, 2, -3)),
        None,
    ]
    for mode, kernel in kernels.items():
        common[mode] = annihilator_rows(kernel)
        assert all(
            sum(row[colour] * kernel[colour] for colour in range(3)) == 0
            for row in common[mode]
        )
    blocks = {
        (left, right): tuple(
            tuple(
                (left + 1) * (right + 2) + (row + 2) * (column + 1) - 3 * left * column
                for column in range(3)
            )
            for row in range(3)
        )
        for left, right in EDGES
    }
    return tuple(common), kernels, blocks


def cofactor(common, word, left: int, right: int) -> int:
    modes = tuple(mode for mode in range(6) if mode not in (left, right))
    matrix = tuple(
        tuple(common[mode][root][word[mode]] for mode in modes) for root in range(4)
    )
    return permanent(matrix)


def coefficient(common, blocks, word) -> int:
    return sum(
        blocks[left, right][word[left]][word[right]]
        * cofactor(common, word, left, right)
        for left, right in EDGES
    )


def double_contraction_audit(common, kernels, blocks) -> dict[str, int]:
    left, right = DOUBLE_KERNEL_MODES
    remaining = tuple(mode for mode in range(6) if mode not in DOUBLE_KERNEL_MODES)
    block_scalar = sum(
        kernels[left][left_colour]
        * blocks[left, right][left_colour][right_colour]
        * kernels[right][right_colour]
        for left_colour in range(3)
        for right_colour in range(3)
    )
    checked = 0
    for tail in itertools.product(range(3), repeat=4):
        tail_values = dict(zip(remaining, tail, strict=True))
        left_hand_side = 0
        for left_colour, right_colour in itertools.product(range(3), repeat=2):
            word = [None] * 6
            word[left] = left_colour
            word[right] = right_colour
            for mode, colour in tail_values.items():
                word[mode] = colour
            left_hand_side += (
                kernels[left][left_colour]
                * kernels[right][right_colour]
                * coefficient(common, blocks, tuple(word))
            )
        cofactor_matrix = tuple(
            tuple(common[mode][root][tail_values[mode]] for mode in remaining)
            for root in range(4)
        )
        assert left_hand_side == block_scalar * permanent(cofactor_matrix)
        checked += 1
    assert checked == 81
    return {
        "contracted_coefficients": checked,
        "surviving_block_scalar": block_scalar,
    }


def double_contraction_pair_audits() -> dict[str, dict[str, int]]:
    common, kernels, blocks = audit_data()
    nonzero_scalar = double_contraction_audit(common, kernels, blocks)
    assert nonzero_scalar["surviving_block_scalar"] != 0

    zero_blocks = dict(blocks)
    zero_blocks[DOUBLE_KERNEL_MODES] = ((1, -2, 0), (0, 0, 0), (0, 0, 0))
    zero_scalar = double_contraction_audit(common, kernels, zero_blocks)
    assert zero_scalar["surviving_block_scalar"] == 0
    return {"nonzero_scalar": nonzero_scalar, "zero_scalar": zero_scalar}


def full_tensor_contraction_audit() -> dict[str, int]:
    common, kernels, blocks = audit_data()
    words = tuple(itertools.product(range(3), repeat=6))
    coefficients = {word: coefficient(common, blocks, word) for word in words}
    assert any(coefficients.values())

    remaining = tuple(mode for mode in range(6) if mode not in KERNEL_MODES)
    contracted = {}
    for tail in itertools.product(range(3), repeat=3):
        tail_values = dict(zip(remaining, tail, strict=True))
        value = 0
        for head in itertools.product(range(3), repeat=3):
            word = [None] * 6
            weight = 1
            for index, mode in enumerate(KERNEL_MODES):
                word[mode] = head[index]
                weight *= kernels[mode][head[index]]
            for mode, colour in tail_values.items():
                word[mode] = colour
            value += weight * coefficients[tuple(word)]
        contracted[tail] = value
    assert contracted == {word: 0 for word in contracted}
    return {
        "lambda_coefficients": len(coefficients),
        "contracted_coefficients": len(contracted),
        "nonzero_uncontracted_coefficients": sum(
            bool(x) for x in coefficients.values()
        ),
    }


def independent_support_audit() -> dict[str, int]:
    colours = {0, 1, 2}
    choices = (set(), {0}, {1}, {2})
    checked = 0
    for zero_sets in itertools.product(choices, repeat=4):
        checked += 1
        assert any(
            set().union(*(zero_sets[index] for index in triple)) != colours
            for triple in itertools.combinations(range(4), 3)
        )

    three_mode_covers = 0
    for zero_sets in itertools.product(choices, repeat=3):
        if set().union(*zero_sets) == colours:
            three_mode_covers += 1
            assert sorted(next(iter(entry)) for entry in zero_sets) == [0, 1, 2]
    assert checked == 256
    assert three_mode_covers == 6
    return {
        "four_mode_assignments": checked,
        "three_mode_extremal_covers": three_mode_covers,
    }


def zero_core_kernel_audit() -> tuple[int, int, int]:
    matrices = (
        ((-1, -2, -1), (0, -1, 1), (-1, -1, -2), (-1, -1, -2)),
        ((0, 0, 0), (0, 0, 0), (0, -1, -2), (1, 2, 2)),
        ((2, -2, 0), (0, 0, 1), (-2, 2, 1), (2, -2, 1)),
    )
    kernels = ((-3, 1, 1), (2, -2, 1), (1, 1, 0))
    for matrix, kernel in zip(matrices, kernels, strict=True):
        assert [
            sum(a * b for a, b in zip(row, kernel, strict=True)) for row in matrix
        ] == [
            0,
            0,
            0,
            0,
        ]
    product = tuple(
        kernels[0][colour] * kernels[1][colour] * kernels[2][colour]
        for colour in range(3)
    )
    assert product == (-6, -2, 0)
    return product


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "No finite-field inference is used" in " ".join(theorem.split())
    assert "cores satisfying the support-cover condition: UNKNOWN" in theorem
    assert "two fully supported common-row kernel modes: EXCLUDED" in theorem
    double_contractions = double_contraction_pair_audits()
    contraction = full_tensor_contraction_audit()
    support = independent_support_audit()
    zero_core_product = zero_core_kernel_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent integer contraction and support enumeration",
                "field": "rational characteristic zero",
                "double_contraction": double_contractions,
                "contraction": contraction,
                "support_cover": support,
                "zero_cofactor_core_kernel_product": zero_core_product,
                "finite_field_used": False,
                "other_common_row_cores_excluded": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
