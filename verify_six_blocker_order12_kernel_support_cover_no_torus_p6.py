#!/usr/bin/env python3
"""Verify the order-twelve kernel-support no-torus obstruction."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md"
PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))
EDGES = tuple(itertools.combinations(range(6), 2))
KERNEL_MODES = (0, 1, 2)
DOUBLE_KERNEL_MODES = (0, 1)


def permanent_columns(columns):
    return sum(
        sp.prod(columns[column][permutation[column]] for column in range(4))
        for permutation in PERMUTATIONS_4
    )


def symbolic_column_linearity() -> int:
    p, q = sp.symbols("p q")
    first = sp.symbols("a0:4")
    second = sp.symbols("b0:4")
    dependent = tuple(-p * first[row] - q * second[row] for row in range(4))
    companions = tuple(sp.symbols(f"x{column}_0:4") for column in range(3))
    contraction = sp.expand(
        p * permanent_columns((first, *companions))
        + q * permanent_columns((second, *companions))
        + permanent_columns((dependent, *companions))
    )
    assert contraction == 0
    return len(PERMUTATIONS_4)


def edge_witness_ledger() -> dict[int, int]:
    ledger = {1: 0, 2: 0, 3: 0}
    kernel_set = set(KERNEL_MODES)
    for edge in EDGES:
        witnesses = kernel_set.difference(edge)
        assert witnesses
        ledger[len(witnesses)] += 1
    assert ledger == {1: 3, 2: 9, 3: 3}
    return ledger


def double_edge_ledger() -> dict[str, int]:
    kernel_set = set(DOUBLE_KERNEL_MODES)
    surviving = []
    killed = []
    for edge in EDGES:
        if kernel_set.difference(edge):
            killed.append(edge)
        else:
            surviving.append(edge)
    assert surviving == [DOUBLE_KERNEL_MODES]
    assert len(killed) == 14
    return {"killed_edges": len(killed), "surviving_edges": len(surviving)}


def permanent_four(matrix) -> int:
    return sum(
        matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
        * matrix[3][permutation[3]]
        for permutation in PERMUTATIONS_4
    )


def concrete_data():
    kernels = (
        (1, 1, 1),
        (1, 2, 3),
        (2, -1, 1),
    )
    common = (
        ((1, -1, 0), (0, 1, -1), (1, 0, -1), (2, -1, -1)),
        ((2, -1, 0), (3, 0, -1), (0, 3, -2), (1, 1, -1)),
        ((1, 2, 0), (0, 1, 1), (1, 1, -1), (2, 3, -1)),
        ((1, 0, 2), (0, 1, -1), (2, -1, 1), (1, 3, 0)),
        ((0, 2, 1), (1, -1, 2), (3, 0, -1), (2, 1, 1)),
        ((2, 1, 0), (-1, 2, 1), (1, 0, 3), (0, -2, 1)),
    )
    for mode, kernel in enumerate(kernels):
        assert all(
            sum(common[mode][row][colour] * kernel[colour] for colour in range(3)) == 0
            for row in range(4)
        )
    blocks = {
        (left, right): tuple(
            tuple(
                (left + 2) * (row + 1)
                - (right + 3) * (column + 1)
                + (left + 1) * (right + 1)
                for column in range(3)
            )
            for row in range(3)
        )
        for left, right in EDGES
    }
    return common, kernels, blocks


def cofactor(common, word, left: int, right: int) -> int:
    modes = [mode for mode in range(6) if mode not in (left, right)]
    return permanent_four(
        [[common[mode][root][word[mode]] for mode in modes] for root in range(4)]
    )


def coefficient(common, blocks, word) -> int:
    return sum(
        blocks[left, right][word[left]][word[right]]
        * cofactor(common, word, left, right)
        for left, right in EDGES
    )


def double_contraction_check() -> dict[str, object]:
    common, kernels, blocks = concrete_data()
    left, right = DOUBLE_KERNEL_MODES
    remaining = tuple(mode for mode in range(6) if mode not in DOUBLE_KERNEL_MODES)
    block_scalar = sum(
        kernels[left][left_colour]
        * blocks[left, right][left_colour][right_colour]
        * kernels[right][right_colour]
        for left_colour in range(3)
        for right_colour in range(3)
    )
    assert block_scalar != 0

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
        cofactor_matrix = [
            [common[mode][root][tail_values[mode]] for mode in remaining]
            for root in range(4)
        ]
        right_hand_side = block_scalar * permanent_four(cofactor_matrix)
        assert left_hand_side == right_hand_side
        checked += 1
    assert checked == 81
    return {
        "contracted_coefficients_checked": checked,
        "surviving_block_scalar": block_scalar,
        "kernel_support_intersection": 3,
    }


def complete_contraction_check() -> dict[str, object]:
    common, kernels, blocks = concrete_data()
    coefficients = {
        word: coefficient(common, blocks, word)
        for word in itertools.product(range(3), repeat=6)
    }
    assert any(coefficients.values())

    contractions = {}
    for tail in itertools.product(range(3), repeat=3):
        value = 0
        for head in itertools.product(range(3), repeat=3):
            weight = 1
            for mode in KERNEL_MODES:
                weight *= kernels[mode][head[mode]]
            value += weight * coefficients[(*head, *tail)]
        contractions[tail] = value
    assert contractions == {tail: 0 for tail in contractions}

    diagonal = (2, 3, 5)
    diagonal_contraction = tuple(
        diagonal[colour] * kernels[0][colour] * kernels[1][colour] * kernels[2][colour]
        for colour in range(3)
    )
    assert diagonal_contraction == (4, -6, 15)
    assert all(diagonal_contraction)
    return {
        "lambda_coefficients_checked": len(coefficients),
        "contracted_tail_coefficients_checked": len(contractions),
        "sample_diagonal_contraction": diagonal_contraction,
    }


def support_cover_ledger() -> dict[str, int]:
    colours = frozenset(range(3))
    small_zero_sets = (frozenset(),) + tuple(
        frozenset((colour,)) for colour in range(3)
    )
    four_mode_assignments = 0
    assignments_with_bad_triple = 0
    for zero_sets in itertools.product(small_zero_sets, repeat=4):
        four_mode_assignments += 1
        bad_triples = [
            triple
            for triple in itertools.combinations(range(4), 3)
            if set().union(*(zero_sets[index] for index in triple)) != colours
        ]
        assert bad_triples
        assignments_with_bad_triple += 1

    exact_three_covers = []
    for zero_sets in itertools.product(small_zero_sets, repeat=3):
        if set().union(*zero_sets) == colours:
            exact_three_covers.append(zero_sets)
            assert all(len(zero_set) == 1 for zero_set in zero_sets)
            assert len(set(zero_sets)) == 3
    assert len(exact_three_covers) == 6
    assert four_mode_assignments == assignments_with_bad_triple == 256
    return {
        "four_mode_support_assignments": four_mode_assignments,
        "assignments_with_noncovering_triple": assignments_with_bad_triple,
        "extremal_three_mode_covers": len(exact_three_covers),
    }


def zero_core_application() -> dict[str, object]:
    matrices = (
        ((-1, -2, -1), (0, -1, 1), (-1, -1, -2), (-1, -1, -2)),
        ((0, 0, 0), (0, 0, 0), (0, -1, -2), (1, 2, 2)),
        ((2, -2, 0), (0, 0, 1), (-2, 2, 1), (2, -2, 1)),
    )
    kernels = ((-3, 1, 1), (2, -2, 1), (1, 1, 0))
    for matrix, kernel in zip(matrices, kernels, strict=True):
        assert all(
            sum(row[colour] * kernel[colour] for colour in range(3)) == 0
            for row in matrix
        )
        assert sp.Matrix(matrix).rank() == 2
    product = tuple(
        kernels[0][colour] * kernels[1][colour] * kernels[2][colour]
        for colour in range(3)
    )
    assert product == (-6, -2, 0)
    assert product != (0, 0, 0)
    return {"kernel_vectors": kernels, "hadamard_product": product}


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero structural obstruction",
        "z_p hadamard z_q hadamard z_r=0",
        "two fully supported common-row kernel modes: EXCLUDED by subrank(P_4)=2",
        "four support-at-least-two common-row kernel modes: EXCLUDED",
        "z_0 hadamard z_1 hadamard z_2=(-6,-2,0)!=0",
        "effective two-row factorisation on surviving cores: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem

    symbolic_terms = symbolic_column_linearity()
    double_edges = double_edge_ledger()
    witnesses = edge_witness_ledger()
    double_contraction = double_contraction_check()
    contraction = complete_contraction_check()
    support = support_cover_ledger()
    zero_core = zero_core_application()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "symbolic_permanent_terms": symbolic_terms,
                "double_contraction_edge_ledger": double_edges,
                "edge_witness_multiplicities": witnesses,
                "double_contraction_instance": double_contraction,
                "contraction_instance": contraction,
                "support_cover_ledger": support,
                "zero_cofactor_core_application": zero_core,
                "arbitrary_blocks_excluded_on_stratum": True,
                "effective_factorisation_needed_on_stratum": False,
                "other_common_row_cores_excluded": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
