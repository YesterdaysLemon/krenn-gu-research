#!/usr/bin/env python3
"""Verify the single-gate H31 reduction to a line arrangement."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_SINGLE_GATE_P3_REDUCTION.md"
P3_THEOREM = REPO_ROOT / "claims/p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(
                rows[row][permutation[row]]
                for row in range(size)
            )
            for permutation in itertools.permutations(range(size))
        )
    )


def main() -> None:
    A = sp.symbols("A", nonzero=True)
    B = sp.symbols("B")
    v0, v1, v2 = sp.symbols("v0 v1 v2")
    t, x1, x2, x3, y1, y2, y3 = sp.symbols(
        "t x1 x2 x3 y1 y2 y3"
    )
    variables = (t, x1, x2, x3, y1, y2, y3)

    alpha_shared = (
        (-B, 0, 1),
        (A, 1, 0),
        (A, 1, 0),
    )
    beta_shared = (
        (-A, 1, 0),
        (B, 0, 1),
        (0, B, A),
    )
    p3_coefficients = {}
    for bits in itertools.product((0, 1), repeat=3):
        rows = tuple(
            beta_shared[mode] if bits[mode] else alpha_shared[mode]
            for mode in range(3)
        )
        p3_coefficients["".join(map(str, bits))] = sp.factor(
            permanent(rows)
        )
    assert p3_coefficients == {
        "000": 2 * A,
        "001": 0,
        "010": 0,
        "011": 0,
        "100": 0,
        "101": 0,
        "110": 0,
        "111": 0,
    }

    alpha_extended = (
        alpha_shared[0] + (x1,),
        alpha_shared[1] + (x2,),
        alpha_shared[2] + (x3,),
    )
    beta_extended = (
        beta_shared[0] + (y1,),
        beta_shared[1] + (y2,),
        beta_shared[2] + (y3,),
    )
    beta_zero = (v0, v1, v2, t)
    coefficients = {}
    for bits in itertools.product((0, 1), repeat=3):
        rows = (beta_zero,) + tuple(
            beta_extended[mode] if bits[mode] else alpha_extended[mode]
            for mode in range(3)
        )
        coefficients["".join(map(str, bits))] = sp.expand(
            permanent(rows)
        )

    expected = {
        "000": (
            2 * A * t
            + A * v1 * x2
            + A * v1 * x3
            + 2 * A * v2 * x1
            - B * v2 * x2
            - B * v2 * x3
            + v0 * x2
            + v0 * x3
        ),
        "001": (
            A**2 * v1 * x1
            - A * B * v1 * x2
            + A * B * v2 * x1
            + A * v0 * x1
            + A * v1 * y3
            - B**2 * v2 * x2
            + B * v0 * x2
            - B * v2 * y3
            + v0 * y3
        ),
        "010": (
            A * v1 * x1
            + A * v1 * y2
            + B * v2 * x1
            - B * v2 * y2
            + v0 * x1
            + v0 * y2
        ),
        "011": B * (
            A * v1 * x1
            - A * v1 * y2
            + B * v2 * x1
            - B * v2 * y2
            + v0 * x1
            + v0 * y2
        ),
        "100": 2 * A * v2 * y1,
        "101": A * (
            -A * v1 * x2
            + A * v1 * y1
            - B * v2 * x2
            + B * v2 * y1
            + v0 * x2
            + v0 * y1
        ),
        "110": (
            -A * v1 * x3
            + A * v1 * y1
            + B * v2 * x3
            + B * v2 * y1
            + v0 * x3
            + v0 * y1
        ),
        "111": (
            -A**2 * v1 * y2
            + A * B * v1 * y1
            - A * B * v2 * y2
            + A * v0 * y2
            - A * v1 * y3
            + B**2 * v2 * y1
            + B * v0 * y1
            + B * v2 * y3
            + v0 * y3
        ),
    }
    assert all(
        sp.expand(coefficients[word] - value) == 0
        for word, value in expected.items()
    )

    unwanted_words = tuple(word for word in coefficients if word != "111")
    unwanted_matrix = sp.Matrix(
        [
            [
                sp.diff(coefficients[word], variable)
                for variable in variables
            ]
            for word in unwanted_words
        ]
    )
    desired_row = sp.Matrix(
        [[
            sp.diff(coefficients["111"], variable)
            for variable in variables
        ]]
    )
    determinant = sp.factor(unwanted_matrix.det())
    expected_determinant = (
        -8
        * A**4
        * B
        * v1
        * v2
        * (-A * v1 - B * v2 + v0)
        * (-A * v1 + B * v2 + v0)
        * (A * v1 - B * v2 + v0)
        * (A * v1 + B * v2 + v0)
    )
    assert sp.expand(determinant - expected_determinant) == 0

    def check_witness(
        substitutions: dict[sp.Expr, sp.Expr],
        witness: sp.Matrix,
        desired: sp.Expr,
    ) -> None:
        matrix = unwanted_matrix.subs(substitutions)
        row = desired_row.subs(substitutions)
        assert (matrix * witness).applyfunc(
            sp.factor
        ) == sp.zeros(7, 1)
        assert sp.factor(
            (row * witness)[0] - desired.subs(substitutions)
        ) == 0

    witness_B_zero = sp.Matrix(
        [v2, -1, 0, 0, 0, 1, A]
    )
    check_witness(
        {B: 0},
        witness_B_zero,
        2 * A * (v0 - A * v1),
    )

    witness_v1_zero = sp.Matrix(
        [
            v2 * (v0 - B * v2),
            B * v2 - v0,
            0,
            0,
            0,
            B * v2 + v0,
            A * (B * v2 + v0),
        ]
    )
    check_witness(
        {v1: 0},
        witness_v1_zero,
        2 * A * v0 * (B * v2 + v0),
    )

    witness_v2_zero = sp.Matrix(
        [
            (A * v1 + v0) ** 2,
            0,
            -A * (A * v1 + v0),
            -A * (A * v1 + v0),
            A * (v0 - A * v1),
            0,
            A * B * (v0 - A * v1),
        ]
    )
    check_witness(
        {v2: 0},
        witness_v2_zero,
        2 * A * B * v0 * (v0 - A * v1),
    )

    witness_signed = sp.Matrix([0, 0, 0, 0, 0, 0, 1])
    check_witness(
        {v0: -A * v1 + B * v2},
        witness_signed,
        2 * v0,
    )

    def check_row_certificate(
        substitutions: dict[sp.Expr, sp.Expr],
        multipliers: sp.Matrix,
    ) -> None:
        matrix = unwanted_matrix.subs(substitutions)
        row = desired_row.subs(substitutions)
        assert (multipliers.T * matrix - row).applyfunc(
            sp.factor
        ) == sp.zeros(1, 7)

    assert desired_row.subs({B: 0, v0: A * v1}).applyfunc(
        sp.factor
    ) == sp.zeros(1, 7)
    check_row_certificate(
        {v1: 0, v0: 0},
        sp.Matrix([0, -1, A, 0, 0, B / A, 0]),
    )
    check_row_certificate(
        {v1: 0, v0: -B * v2},
        sp.Matrix([0, 0, A, 0, 0, 0, 0]),
    )
    check_row_certificate(
        {v2: 0, v0: 0},
        sp.Matrix([0, -1, 0, A / B, 0, B / A, 0]),
    )
    check_row_certificate(
        {v2: 0, v0: A * v1},
        sp.Matrix([0, 0, 0, 0, 0, B / A, 0]),
    )
    check_row_certificate(
        {v0: 0, v1: B * v2 / A},
        sp.Matrix([0, 0, -A, A / B, B**2 / A, 0, 0]),
    )

    signed_excluded_certificates = (
        (
            {v0: A * v1 + B * v2},
            sp.Matrix(
                [
                    0,
                    B * v2 / (A * v1),
                    0,
                    -v2 / v1,
                    B * (A * v1 + B * v2) / (A * v2),
                    0,
                    0,
                ]
            ),
        ),
        (
            {v0: A * v1 - B * v2},
            sp.Matrix(
                [
                    0,
                    0,
                    -B * v2 / v1,
                    v2 / v1,
                    B * v1 / v2,
                    0,
                    0,
                ]
            ),
        ),
        (
            {v0: -A * v1 - B * v2},
            sp.Matrix(
                [
                    0,
                    A * v1 / (B * v2),
                    A * (A * v1 + B * v2) / (B * v2),
                    0,
                    0,
                    -v1 / v2,
                    0,
                ]
            ),
        ),
    )
    for substitutions, multipliers in signed_excluded_certificates:
        check_row_certificate(substitutions, multipliers)

    output = {
        "verified": True,
        "field": "C",
        "single_gate_unique": "proved in theorem",
        "marked_P3_nonzero_word": "000",
        "marked_P3_nonzero_coefficient": "2*A",
        "extension_variables": list(map(str, variables)),
        "unwanted_equations": list(unwanted_words),
        "extension_matrix_shape": list(unwanted_matrix.shape),
        "desired_functional_nonzero": desired_row != sp.zeros(1, 7),
        "determinant_factors": [
            "B",
            "v1",
            "v2",
            "-A*v1-B*v2+v0",
            "-A*v1+B*v2+v0",
            "A*v1-B*v2+v0",
            "A*v1+B*v2+v0",
        ],
        "viable_locus_components": {
            "I": "B=0 and v0-A*v1!=0",
            "II": "v1=0 and v0*(v0+B*v2)!=0",
            "III": "B!=0 and v2=0 and v0*(v0-A*v1)!=0",
            "IV": "v0=-A*v1+B*v2 and v0!=0",
        },
        "viable_locus_classified": True,
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "dependency": {
            "file": P3_THEOREM.name,
            "sha256": sha256(P3_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_h31_single_gate_p3_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
