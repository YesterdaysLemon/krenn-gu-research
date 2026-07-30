#!/usr/bin/env python3
"""Verify the one-cross normal-pencil saturation reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


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
    h1 = sp.Matrix([b, 0, 0, -1, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    n = sp.Matrix([0, 0, 0, c, b])
    u1 = sp.Matrix([b, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    m = c * u1 - b * u2
    w_plus = sp.Matrix([1, 0, 0, b, -c])
    w_minus = sp.Matrix([1, 0, 0, -b, c])
    e1 = sp.Matrix([0, 1, 0, 0, 0])
    e2 = sp.Matrix([0, 0, 1, 0, 0])

    q_residual = derivative(
        derivative(source_permanent, variables, u2),
        variables,
        h1,
    )
    p_residual = derivative(
        derivative(source_permanent, variables, u1),
        variables,
        h2,
    )
    assert sp.expand(
        q_residual + x1 * x2 * (x0 - b * x3 + c * x4)
    ) == 0
    assert sp.expand(
        p_residual + x1 * x2 * (x0 + b * x3 - c * x4)
    ) == 0
    assert derivative(
        derivative(source_permanent, variables, m),
        variables,
        n,
    ) == 0

    j_minus = sp.Matrix.hstack(e1, e2, w_minus)
    j_plus = sp.Matrix.hstack(e1, e2, w_plus)
    assert j_minus.T * h2 == sp.zeros(3, 1)
    assert j_minus.T * n == sp.zeros(3, 1)
    assert sp.Matrix.hstack(h2, n).rank() == 2
    assert j_plus.T * h1 == sp.zeros(3, 1)
    assert j_plus.T * n == sp.zeros(3, 1)
    assert sp.Matrix.hstack(h1, n).rank() == 2

    A, B = sp.symbols("A B")
    # Coordinates 0,3,4 support the pencil permanents.
    h2_small = sp.Matrix([c, 0, -1])
    h1_small = sp.Matrix([b, -1, 0])
    n_small = sp.Matrix([0, c, b])
    minus_line = A * h2_small + B * n_small
    plus_line = A * h1_small + B * n_small
    minus_cubic = sp.factor(
        permanent([minus_line, minus_line, minus_line])
    )
    plus_cubic = sp.factor(
        permanent([plus_line, plus_line, plus_line])
    )
    assert sp.expand(
        minus_cubic - 6 * A * B * c**2 * (-A + b * B)
    ) == 0
    assert sp.expand(
        plus_cubic - 6 * A * B * b**2 * (-A + c * B)
    ) == 0

    minus_polarized = sp.factor(
        permanent([h2_small, n_small, minus_line])
    )
    plus_polarized = sp.factor(
        permanent([h1_small, n_small, plus_line])
    )
    assert sp.expand(
        minus_polarized - 2 * c**2 * (-A + b * B)
    ) == 0
    assert sp.expand(
        plus_polarized - 2 * b**2 * (-A + c * B)
    ) == 0

    assert b * h2 + n == c * u1
    assert c * h1 + n == b * u2

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b*c != 0",
        "q_residual": str(sp.factor(q_residual)),
        "p_residual": str(sp.factor(p_residual)),
        "q_normal_pencil": "span(h2,n)",
        "p_normal_pencil": "span(h1,n)",
        "q_binary_cubic": str(minus_cubic),
        "p_binary_cubic": str(plus_cubic),
        "q_forced_third_line": "C*u1",
        "p_forced_third_line": "C*u2",
        "fourth_normal_target_covector": "C*e0*",
        "q_mandatory_opposite_pencil": "span(h1,n)",
        "p_mandatory_opposite_pencil": "span(h2,n)",
        "one_cross_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_pencil_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
