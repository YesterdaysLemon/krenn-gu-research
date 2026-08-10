#!/usr/bin/env python3
"""Verify the a=0 adjacent-boundary reduction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_A0_ADJACENT_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    b, c = sp.symbols("b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)

    u0 = sp.Matrix([0, 1, 1, 0, 0])
    u1 = sp.Matrix([b, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    h0 = sp.Matrix([0, 1, -1, 0, 0])
    h1 = sp.Matrix([b, 0, 0, -1, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    n = sp.Matrix([0, 0, 0, c, b])
    s = sp.Matrix([0, 1, 1, 0, 0])

    u0_contraction = derivative(source_permanent, variables, u0)
    expected = x0 * x3 * x4 * (x1 + x2)
    assert sp.expand(u0_contraction - expected) == 0
    support_basis = sp.Matrix.hstack(
        sp.eye(5)[:, 0],
        s,
        sp.eye(5)[:, 3],
        sp.eye(5)[:, 4],
    )
    assert support_basis.T * h0 == sp.zeros(4, 1)
    assert support_basis.rank() == 4

    common_rows = sp.Matrix.hstack(h0, h1, h2)
    opposite_rows = sp.Matrix.hstack(h0, h1, n)
    assert common_rows.rank() == 3
    assert opposite_rows.rank() == 3
    assert common_rows.T * s == sp.zeros(3, 1)
    assert opposite_rows.T * s == sp.zeros(3, 1)

    assert c * u1 == b * h2 + n
    assert b * u2 == c * h1 + n

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a=0, b*c != 0",
        "u0_contraction": str(sp.factor(u0_contraction)),
        "third_normal": str(tuple(h0)),
        "h0_modes_in_one_cross": ["C", "D"],
        "q_orientation_rigid_direction": "u1 in R_C or R_D",
        "p_orientation_rigid_direction": "u2 in R_C or R_D",
        "adjacent_a0_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_a0_adjacent_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
