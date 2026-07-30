#!/usr/bin/env python3
"""Verify the adjacent one-cross two-gate reduction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md"


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


def repeated_derivative(polynomial, variables, directions):
    result = polynomial
    for direction in directions:
        result = derivative(result, variables, direction)
    return sp.factor(result)


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    b, c = sp.symbols("b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)
    h1 = sp.Matrix([b, 0, 0, -1, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    n = sp.Matrix([0, 0, 0, c, b])
    u1 = sp.Matrix([b, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    m = c * u1 - b * u2

    triple_h1 = repeated_derivative(
        source_permanent,
        variables,
        (h1, h1, h1),
    )
    triple_h2 = repeated_derivative(
        source_permanent,
        variables,
        (h2, h2, h2),
    )
    assert triple_h1 == 0
    assert triple_h2 == 0

    assert m == b * h2 - c * h1
    assert b * u2 == c * h1 + n
    assert c * u1 == b * h2 + n
    assert sp.Matrix.hstack(h1, h2, n).rank() == 3
    assert sp.Matrix.hstack(u1, u2).rank() == 2
    assert sp.Matrix.hstack(u1, m).rank() == 2
    assert sp.Matrix.hstack(u2, m).rank() == 2

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a*b*c != 0",
        "triple_h1_contraction": str(triple_h1),
        "triple_h2_contraction": str(triple_h2),
        "second_common_mode_excluded": True,
        "double_normal_gate_absorbed": True,
        "remaining_adjacent_gates": [
            "span(u1,u2) contained in a remaining row space",
            "L_A(e1+e2)=0 or L_Y(e1+e2)=0",
        ],
        "adjacent_one_cross_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_two_gate_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
