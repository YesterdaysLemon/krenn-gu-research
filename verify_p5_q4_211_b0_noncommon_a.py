#!/usr/bin/env python3
"""Verify the b=0 noncommon-A obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_B0_NONCOMMON_A_OBSTRUCTION.md"


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


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(5))
            for permutation in itertools.permutations(range(5))
        )
    )


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, c = sp.symbols("a c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)

    u0 = sp.Matrix([a, 1, 1, 0, 0])
    u1 = sp.Matrix([0, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    h0 = sp.Matrix([0, 1, -1, 0, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    s = sp.Matrix([0, 1, 1, 0, 0])
    d = sp.Matrix([0, 1, -1, 0, 0])
    w = sp.Matrix([1, 0, 0, 0, -c])

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

    def row_plane(kernel):
        return sp.Matrix.hstack(
            sp.Matrix([-kernel[1], kernel[0], 0]),
            sp.Matrix([0, 0, 1]),
        )

    zero_systems = {}
    for left_name, left in (("s", kernel_s), ("d", kernel_d)):
        for right_name, right in (("s", kernel_s), ("d", kernel_d)):
            restricted = sp.simplify(
                row_plane(left).T * matrix * row_plane(right)
            )
            zero_systems[f"{left_name}{right_name}"] = restricted

    assert list(zero_systems["dd"]) == [
        2 * g2, g0 + g1, g0 + g1, 0
    ]
    assert list(zero_systems["sd"]) == [
        0, g0 - g1, g0 + g1, 0
    ]
    assert list(zero_systems["ds"]) == [
        0, g0 + g1, g0 - g1, 0
    ]

    contractions = {
        "kernel_propagation": repeated_derivative(
            source_permanent, variables, (u0, u1, h2, h2)
        ),
        "zero_w_chart": repeated_derivative(
            source_permanent, variables, (u1, h2)
        ),
        "h0_chart": repeated_derivative(
            source_permanent, variables, (u1, h0)
        ),
        "pure_colour_zero_chart": repeated_derivative(
            source_permanent, variables, (u0, h2)
        ),
    }
    assert contractions["kernel_propagation"] == -2 * c * (x1 + x2)
    assert contractions["zero_w_chart"] == -x1 * x2 * (x0 - c * x4)
    assert contractions["h0_chart"] == -x0 * x4 * (x1 - x2)
    assert contractions["pure_colour_zero_chart"] == -x3 * (
        a * x1 * x2
        - c * x1 * x4
        - c * x2 * x4
        + x0 * x1
        + x0 * x2
    )

    kernel_basis = sp.Matrix.hstack(s, w)
    assert kernel_basis.rank() == 2
    assert kernel_basis.T * h0 == sp.zeros(2, 1)
    assert kernel_basis.T * u2 == sp.zeros(2, 1)

    # In the reduced image (26), C(e1) is colour two, D(e1) is
    # colour two, and D(w) is colour one.  The (C colour 2,
    # D colour 1) coefficient is therefore exactly the middle term.
    c_e1_colour2, d_w_colour1 = sp.symbols(
        "c_e1_colour2 d_w_colour1",
        nonzero=True,
    )
    forbidden_mixed_coefficient = c_e1_colour2 * d_w_colour1
    assert forbidden_mixed_coefficient != 0
    c0, c3, c4, d3, d4 = sp.symbols("c0 c3 c4 d3 d4")
    d_e1_colour1 = sp.symbols("d_e1_colour1")
    target_rows = [
        tuple(u0),
        tuple(h2),
        (0, 0, 0, 1, 0),
        (c0, c_e1_colour2, c_e1_colour2, c3, c4),
        (
            d_w_colour1 + c * d4,
            d_e1_colour1,
            -d_e1_colour1,
            d3,
            d4,
        ),
    ]
    exact_forbidden_coefficient = sp.factor(permanent(target_rows))
    assert exact_forbidden_coefficient == (
        -2 * c_e1_colour2 * d_w_colour1
    )

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b=0, a*c != 0",
        "zero_chart_systems": {
            name: str(value) for name, value in zero_systems.items()
        },
        "contractions": {
            name: str(value) for name, value in contractions.items()
        },
        "forbidden_mixed_coefficient": str(forbidden_mixed_coefficient),
        "exact_forbidden_mixed_coefficient": str(
            exact_forbidden_coefficient
        ),
        "noncommon_A_excluded": True,
        "forced_h2_modes": ["A", "B", "C"],
        "forced_remaining_kernel": "L_D(e1+e2)=0",
        "b0_boundary_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_b0_noncommon_a_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
