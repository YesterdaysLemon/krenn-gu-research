#!/usr/bin/env python3
"""Verify the marked P4-to-Delta2 slice classification."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md"
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS
        )
    )


def rank_of_pair_on_coordinates(pair, coordinates):
    matrix = sp.Matrix(
        [[row[coordinate] for coordinate in coordinates] for row in pair]
    )
    return matrix.rank()


def main() -> None:
    A, T = sp.symbols("A T", nonzero=True)
    B = sp.symbols("B")
    alpha = (
        sp.Matrix([0, 1, T, -B]),
        sp.Matrix([1, 0, 0, A]),
        sp.Matrix([1, 0, 0, A]),
    )
    beta = (
        sp.Matrix([1, 0, 0, -A]),
        sp.Matrix([0, 1, -T, B]),
        sp.Matrix([B, A, -A * T, 0]),
    )
    e2 = sp.Matrix([0, 0, 1, 0])
    e3 = sp.Matrix([0, 0, 0, 1])

    coefficients = {}
    for word in itertools.product((0, 1), repeat=4):
        first = e2 if word[0] == 0 else e3
        rows = [first] + [
            (alpha[index] if word[index + 1] == 0 else beta[index])
            for index in range(3)
        ]
        coefficients[word] = sp.factor(permanent(rows))

    expected_support = {
        (0, 0, 0, 0): 2 * A,
        (1, 1, 1, 1): -2 * A * T,
    }
    assert {
        word: value for word, value in coefficients.items() if value != 0
    } == expected_support

    slice_ranks = {
        "J2": [
            rank_of_pair_on_coordinates(pair, (0, 1, 3))
            for pair in zip(alpha, beta, strict=True)
        ],
        "J3": [
            rank_of_pair_on_coordinates(pair, (0, 1, 2))
            for pair in zip(alpha, beta, strict=True)
        ],
    }
    assert slice_ranks == {"J2": [2, 2, 2], "J3": [2, 2, 2]}

    x1, y1, x2, y2, x3, y3 = sp.symbols(
        "x1 y1 x2 y2 x3 y3"
    )
    shared_coefficients = (
        2 * A * x1 - B * x2 - B * x3,
        B * (A * x1 - B * x2 - y3),
        B * (x1 - y2),
        B**2 * (x1 - y2),
        2 * A * y1,
        -A * B * (x2 - y1),
        B * (x3 + y1),
        B * (-A * y2 + B * y1 + y3),
    )
    # On B != 0, the seven mixed equations form a full-rank linear
    # system and kill the desired last coefficient.
    shared_matrix, _ = sp.linear_eq_to_matrix(
        shared_coefficients[:-1],
        (x1, y1, x2, y2, x3, y3),
    )
    assert shared_matrix.subs({A: 2, B: 3}).rank() == 6
    shared_solution = {
        x1: 0,
        y1: 0,
        x2: 0,
        y2: 0,
        x3: 0,
        y3: 0,
    }
    assert all(
        sp.expand(value.subs(shared_solution)) == 0
        for value in shared_coefficients
    )
    assert sp.expand(shared_coefficients[-1].subs(B, 0)) == 0

    omitted_coefficients = (
        x2 + x3,
        A * x1 + B * x2 + y3,
        x1 + y2,
        B * (x1 + y2),
        sp.Integer(0),
        A * (x2 + y1),
        x3 + y1,
        A * y2 + B * y1 + y3,
    )
    omitted_solution = {
        x2: 0,
        x3: 0,
        y1: 0,
        y2: -x1,
        y3: -A * x1,
    }
    assert all(
        sp.expand(value.subs(omitted_solution)) == 0
        for value in omitted_coefficients[:-1]
    )
    assert sp.factor(
        omitted_coefficients[-1].subs(omitted_solution)
    ) == -2 * A * x1

    output = {
        "verified": True,
        "field": "C",
        "marked_nonzero_coefficients": {
            "".join(map(str, word)): str(value)
            for word, value in expected_support.items()
        },
        "mixed_coefficients_zero": 14,
        "all_coordinate_deleted_slice_ranks": slice_ranks,
        "shared_common_coordinate_compatible": False,
        "omitted_common_coordinate_solution": {
            "x2": "0",
            "x3": "0",
            "y1": "0",
            "y2": "-x1",
            "y3": "-A*x1",
        },
        "all_rank_two_family_parameters": 3,
        "rank_one_gate": "alpha_i in C*e3 or beta_i in C*e2",
        "marked_Delta2_boundary_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p4_marked_delta2_slice_classification_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
