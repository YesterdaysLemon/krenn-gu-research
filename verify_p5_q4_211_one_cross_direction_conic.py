#!/usr/bin/env python3
"""Verify the one-cross direction-conic reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(3))
            for permutation in itertools.permutations(range(3))
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
    a, b, c = sp.symbols("a b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)
    u0 = sp.Matrix([a, 1, 1, 0, 0])
    u1 = sp.Matrix([b, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    h1 = sp.Matrix([b, 0, 0, -1, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    n = sp.Matrix([0, 0, 0, c, b])
    m = c * u1 - b * u2

    s = sp.Matrix([0, 1, 1, 0, 0])
    d = sp.Matrix([0, 1, -1, 0, 0])
    w = sp.Matrix([1, 0, 0, -b, -c])
    h0_basis = sp.Matrix.hstack(s, d, w)
    assert h0_basis.T * u1 == sp.zeros(3, 1)
    assert h0_basis.T * u2 == sp.zeros(3, 1)
    assert sp.Matrix.hstack(u1, u2).rank() == 2

    q_form_h2 = derivative(
        derivative(
            derivative(source_permanent, variables, u0),
            variables,
            h2,
        ),
        variables,
        n,
    )
    q_form_h1 = derivative(
        derivative(
            derivative(source_permanent, variables, u0),
            variables,
            h1,
        ),
        variables,
        n,
    )
    common_quadratic = (
        a * x1 * x2
        - b * x1 * x3
        - b * x2 * x3
        - c * x1 * x4
        - c * x2 * x4
        + x0 * x1
        + x0 * x2
    )
    assert sp.expand(q_form_h2 + c * common_quadratic) == 0
    assert sp.expand(q_form_h1 + b * common_quadratic) == 0

    matrix = sp.Matrix(
        [
            [a / 2, 0, 1],
            [0, -a / 2, 0],
            [1, 0, 0],
        ]
    )
    inverse = sp.Matrix(
        [
            [0, 0, 1],
            [0, -2 / a, 0],
            [1, 0, -a / 2],
        ]
    )
    assert sp.factor(matrix.det()) == a / 2
    assert sp.simplify(matrix * inverse) == sp.eye(3)

    A, B, C, D = sp.symbols("A B C D")
    ell_p = A * u1 + B * u2
    ell_q = C * u1 + D * u2
    support = (0, 3, 4)

    def restrict(row):
        return sp.Matrix([row[index] for index in support])

    q_h2 = sp.factor(
        permanent([restrict(h2), restrict(ell_p), restrict(ell_q)])
    )
    q_n = sp.factor(
        permanent([restrict(n), restrict(ell_p), restrict(ell_q)])
    )
    q_h1 = sp.factor(
        permanent([restrict(h1), restrict(ell_p), restrict(ell_q)])
    )
    assert sp.expand(q_h2 + 2 * b * A * C) == 0
    assert sp.expand(
        q_n - 2 * (A * b + B * c) * (C * b + D * c)
    ) == 0
    assert sp.expand(q_h1 + 2 * c * B * D) == 0
    assert m == sp.Matrix([0, 0, 0, b * 0 + c, -b])
    assert m == b * h2 - c * h1
    assert sp.Matrix.hstack(u1, m).rank() == 2
    assert sp.Matrix.hstack(u2, m).rank() == 2

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a*b*c != 0",
        "common_quadratic": str(sp.factor(common_quadratic)),
        "conic_determinant": str(sp.factor(matrix.det())),
        "inverse_conic": str(inverse),
        "q_direction_lines": ["C*u2", "C*(c*u1-b*u2)"],
        "p_direction_lines": ["C*u1", "C*(c*u1-b*u2)"],
        "free_polar_core_retained": False,
        "remaining_gate_count": 4,
        "polarization_h2": str(q_h2),
        "polarization_n": str(q_n),
        "polarization_h1": str(q_h1),
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
        ROOT / "tmp" / "p5_q4_211_one_cross_direction_conic_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
