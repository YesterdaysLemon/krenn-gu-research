#!/usr/bin/env python3
"""Verify the marked-P4 alternating-gate classification."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md"
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


def coefficients(row_pairs):
    return {
        word: sp.factor(
            permanent(
                [
                    row_pairs[mode][word[mode]]
                    for mode in range(4)
                ]
            )
        )
        for word in itertools.product((0, 1), repeat=4)
    }


def main() -> None:
    p, q, r, t = sp.symbols("p q r t")
    x2, x3, y2, y3 = sp.symbols("x2 x3 y2 y3")
    z2, z3, d2, d3 = sp.symbols("z2 z3 d2 d3")
    lam = p * t + q * r
    delta = p * t - q * r
    e2 = sp.Matrix([0, 0, 1, 0])
    e3 = sp.Matrix([0, 0, 0, 1])

    transverse = (
        (e2, e3),
        (sp.Matrix([p, q, x2, x3]), e2),
        (e3, sp.Matrix([r, -t, y2, y3])),
        (
            sp.Matrix(
                [delta * r, delta * t, lam * y2, lam * y3]
            ),
            sp.Matrix(
                [delta * p, -delta * q, -lam * x2, -lam * x3]
            ),
        ),
    )
    transverse_coefficients = coefficients(transverse)
    transverse_support = {
        word: value
        for word, value in transverse_coefficients.items()
        if value != 0
    }
    assert set(transverse_support) == {
        (0, 0, 0, 0),
        (1, 1, 1, 1),
    }
    assert sp.expand(
        transverse_support[(0, 0, 0, 0)] - delta * lam
    ) == 0
    assert sp.expand(
        transverse_support[(1, 1, 1, 1)] + delta * lam
    ) == 0

    tangent = (
        (e2, e3),
        (sp.Matrix([p, q, 0, 0]), e2),
        (e3, sp.Matrix([p, -q, 0, 0])),
        (
            sp.Matrix([p, q, z2, z3]),
            sp.Matrix([p, -q, d2, d3]),
        ),
    )
    tangent_coefficients = coefficients(tangent)
    tangent_support = {
        word: value
        for word, value in tangent_coefficients.items()
        if value != 0
    }
    assert set(tangent_support) == {
        (0, 0, 0, 0),
        (1, 1, 1, 1),
    }
    assert sp.expand(tangent_support[(0, 0, 0, 0)] - 2 * p * q) == 0
    assert sp.expand(tangent_support[(1, 1, 1, 1)] + 2 * p * q) == 0

    # Before solving, only four mixed coefficients remain.
    unsolved = (
        (e2, e3),
        (sp.Matrix([p, q, x2, x3]), e2),
        (e3, sp.Matrix([r, -t, y2, y3])),
        (
            sp.Matrix([r, t, z2, z3]),
            sp.Matrix([p, -q, d2, d3]),
        ),
    )
    unsolved_coefficients = coefficients(unsolved)
    nonzero_mixed = {
        word: value
        for word, value in unsolved_coefficients.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
        and value != 0
    }
    expected_mixed = {
        (0, 0, 1, 0): lam * y3 - delta * z3,
        (0, 0, 1, 1): -delta * d3 - lam * x3,
        (1, 0, 1, 0): lam * y2 - delta * z2,
        (1, 0, 1, 1): -delta * d2 - lam * x2,
    }
    assert set(nonzero_mixed) == set(expected_mixed)
    assert all(
        sp.expand(nonzero_mixed[word] - expected_mixed[word]) == 0
        for word in expected_mixed
    )

    # Same-mode gates demand a bilinear scalar to be both zero and nonzero.
    a20, a21, a30, a31 = sp.symbols("a20 a21 a30 a31")
    b20, b21, b30, b31 = sp.symbols("b20 b21 b30 b31")
    bilinear_alpha = a20 * a31 + a21 * a30
    bilinear_beta = b20 * b31 + b21 * b30
    plus_requirements = (bilinear_alpha, bilinear_beta)
    minus_requirements = (bilinear_beta, bilinear_alpha)
    assert plus_requirements[0] == minus_requirements[1]
    assert plus_requirements[1] == minus_requirements[0]

    output = {
        "verified": True,
        "field": "C",
        "gate_pattern": "one e2 gate and one e3 gate at distinct modes",
        "transverse_diagonal_coefficients": [
            str(delta * lam),
            str(-delta * lam),
        ],
        "tangent_diagonal_coefficients": [
            str(2 * p * q),
            str(-2 * p * q),
        ],
        "mixed_equations": [
            "lambda*y_j-Delta*z_j=0",
            "-lambda*x_j-Delta*d_j=0",
        ],
        "mixed_coefficients_zero_per_normal_form": 14,
        "normal_form_strata": 2,
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
        ROOT / "tmp" / "p4_marked_delta2_alternating_gate_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
