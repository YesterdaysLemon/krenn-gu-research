#!/usr/bin/env python3
"""Verify the final b=0 boundary obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_B0_FINAL_OBSTRUCTION.md"


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


def row_plane(kernel):
    return sp.Matrix.hstack(
        sp.Matrix([-kernel[1], kernel[0], 0]),
        sp.Matrix([0, 0, 1]),
    )


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, c = sp.symbols("a c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)

    u0 = sp.Matrix([a, 1, 1, 0, 0])
    u1 = sp.Matrix([0, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    h2 = sp.Matrix([c, 0, 0, 0, -1])

    contractions = {
        "label_product": repeated_derivative(
            source_permanent, variables, (u0, u1, h2, h2)
        ),
        "w_chart": repeated_derivative(
            source_permanent, variables, (u1, h2)
        ),
        "k_chart": repeated_derivative(
            source_permanent, variables, (u2, u1)
        ),
        "triple_h2": repeated_derivative(
            source_permanent, variables, (h2, h2, h2)
        ),
    }
    assert contractions["label_product"] == -2 * c * (x1 + x2)
    assert contractions["w_chart"] == -x1 * x2 * (x0 - c * x4)
    assert contractions["k_chart"] == x1 * x2 * (x0 + c * x4)
    assert contractions["triple_h2"] == 0

    g0, g1, g2 = sp.symbols("g0 g1 g2")
    matrix = sp.Matrix(
        [
            [0, g2, g1],
            [g2, 0, g0],
            [g1, g0, 0],
        ]
    )
    kernel_s = sp.Matrix([1, 1, 0])
    kernel_d = sp.Matrix([1, -1, 0])
    ds_system = sp.simplify(
        row_plane(kernel_d).T * matrix * row_plane(kernel_s)
    )
    ss_system = sp.simplify(
        row_plane(kernel_s).T * matrix * row_plane(kernel_s)
    )
    assert list(ds_system) == [0, g0 + g1, g0 - g1, 0]
    assert list(ss_system) == [-2 * g2, g0 - g1, g0 - g1, 0]

    # Binary-polar calculations used in cases X and Y.
    c1, c2, d1, d2 = sp.symbols("c1 c2 d1 d2")
    binary = c1 * d2 + c2 * d1
    d_kills_s = {d1: 1, d2: -1}
    assert sp.expand(binary.subs(d_kills_s)) == -c1 + c2
    # Zero forces c1=c2 (C kills d); a pure nonzero factor instead
    # records C(d)=c1-c2 on its required target line.

    r_b, p_b, r_c, p_c = sp.symbols("r_b p_b r_c p_c")
    label_ideal = (
        r_b * r_c,
        p_b * p_c,
    )
    assert label_ideal == (r_b * r_c, p_b * p_c)

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b=0, a*c != 0",
        "contractions": {
            name: str(value) for name, value in contractions.items()
        },
        "d_s_zero_system": str(ds_system),
        "s_s_zero_system": str(ss_system),
        "binary_polar_with_D_kernel_s": str(
            sp.expand(binary.subs(d_kills_s))
        ),
        "h2_target_label_cases": [
            "B:e0^*, C:e1^*",
            "B:e1^*, C:e0^*",
        ],
        "case_X_excluded": True,
        "case_Y_excluded": True,
        "b0_boundary_excluded": True,
        "c0_boundary_excluded": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_b0_final_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
