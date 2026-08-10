#!/usr/bin/env python3
"""Verify the adjacent one-cross common-kernel obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md"


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


def outer3(left, middle, right):
    return sp.MutableDenseNDimArray(
        [
            left[i] * middle[j] * right[k]
            for i in range(3)
            for j in range(3)
            for k in range(3)
        ],
        (3, 3, 3),
    )


def add_arrays(*arrays):
    result = sp.MutableDenseNDimArray.zeros(3, 3, 3)
    for array in arrays:
        for i, j, k in itertools.product(range(3), repeat=3):
            result[i, j, k] += array[i, j, k]
    return result


def scale_array(scalar, array):
    return sp.MutableDenseNDimArray(
        [scalar * value for value in array],
        (3, 3, 3),
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
    s = sp.Matrix([0, 1, 1, 0, 0])
    d = sp.Matrix([0, 1, -1, 0, 0])
    w_minus = sp.Matrix([1, 0, 0, -b, c])
    w_plus = sp.Matrix([1, 0, 0, b, -c])

    contractions = {
        "u1_h2_h2": repeated_derivative(
            source_permanent, variables, (u1, h2, h2)
        ),
        "u2_h1_h1": repeated_derivative(
            source_permanent, variables, (u2, h1, h1)
        ),
        "u0_h1_h2_n": repeated_derivative(
            source_permanent, variables, (u0, h1, h2, n)
        ),
        "u0_h2_h2_n": repeated_derivative(
            source_permanent, variables, (u0, h2, h2, n)
        ),
        "u2_h1": repeated_derivative(
            source_permanent, variables, (u2, h1)
        ),
        "u1_h2": repeated_derivative(
            source_permanent, variables, (u1, h2)
        ),
    }
    assert contractions["u1_h2_h2"] == -2 * c * x1 * x2
    assert contractions["u2_h1_h1"] == -2 * b * x1 * x2
    assert contractions["u0_h1_h2_n"] == -2 * b * c * (x1 + x2)
    assert contractions["u0_h2_h2_n"] == -2 * c**2 * (x1 + x2)
    assert contractions["u2_h1"] == -x1 * x2 * (
        x0 - b * x3 + c * x4
    )
    assert contractions["u1_h2"] == -x1 * x2 * (
        x0 + b * x3 - c * x4
    )

    # Binary polarity after D(s)=0.
    y1, y2, d1, d2 = sp.symbols("y1 y2 d1 d2")
    polar = y1 * d2 + y2 * d1
    assert sp.expand(polar.subs({d1: 1, d2: -1})) == -y1 + y2
    assert sp.Matrix.hstack(s, w_minus, w_plus).rank() == 3

    # The normalized e0^4 coefficient is divisible by rho_C(s).
    A0, A3, A4 = sp.symbols("A0 A3 A4")
    Y0, Y3, Y4 = sp.symbols("Y0 Y3 Y4")
    D0, D3, D4 = sp.symbols("D0 D3 D4")
    C0, C1, C2, C3, C4 = sp.symbols("C0 C1 C2 C3 C4")
    e0_rows = [
        (a, 1, 1, 0, 0),
        (A0, 0, 0, A3, A4),
        (Y0, 0, 0, Y3, Y4),
        (C0, C1, C2, C3, C4),
        (D0, 0, 0, D3, D4),
    ]
    e0_coefficient = sp.factor(permanent(e0_rows))
    x_permanent = (
        A0 * D3 * Y4
        + A0 * D4 * Y3
        + A3 * D0 * Y4
        + A3 * D4 * Y0
        + A4 * D0 * Y3
        + A4 * D3 * Y0
    )
    assert e0_coefficient == (C1 + C2) * x_permanent

    # Check the six-term P3 cancellation identity (21).
    y = sp.symbols("y", nonzero=True)
    delta = sp.symbols("delta", nonzero=True)
    gamma = sp.symbols("gamma", nonzero=True)
    cs0, cs2 = sp.symbols("cs0 cs2")
    yw0, yw1, yw2 = sp.symbols("yw0 yw1 yw2")
    cw0, cw1, cw2 = sp.symbols("cw0 cw1 cw2")
    dw0, dw1, dw2 = sp.symbols("dw0 dw1 dw2")
    e1_target = sp.Matrix([0, 1, 0])
    e2_target = sp.Matrix([0, 0, 1])
    v_y = y * e1_target
    v_d = delta * e2_target
    c_d = gamma * e2_target
    c_s = sp.Matrix([cs0, 0, cs2])
    y_w = sp.Matrix([yw0, yw1, yw2])
    c_w = sp.Matrix([cw0, cw1, cw2])
    d_w = sp.Matrix([dw0, dw1, dw2])
    c_e1 = (c_s + c_d) / 2
    c_e2 = (c_s - c_d) / 2

    six_terms = add_arrays(
        outer3(v_y, c_e2, d_w),
        outer3(v_y, c_w, -v_d),
        outer3(v_y, c_e1, d_w),
        outer3(v_y, c_w, v_d),
        outer3(y_w, c_e1, -v_d),
        outer3(y_w, c_e2, v_d),
    )
    reduced = add_arrays(
        scale_array(-1, outer3(y_w, c_d, v_d)),
        outer3(v_y, c_s, d_w),
    )
    for index in itertools.product(range(3), repeat=3):
        assert sp.expand(six_terms[index] - reduced[index]) == 0

    forbidden_coefficients = [
        sp.factor(reduced[1, 0, index])
        for index in range(3)
    ]
    assert forbidden_coefficients == [
        cs0 * dw0 * y,
        cs0 * dw1 * y,
        cs0 * dw2 * y,
    ]

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b*c != 0 whenever the common-kernel gate occurs",
        "contractions": {
            name: str(value) for name, value in contractions.items()
        },
        "binary_polar_after_D_s_zero": str(
            sp.expand(polar.subs({d1: 1, d2: -1}))
        ),
        "e0_coefficient_factor": str(e0_coefficient),
        "p3_reduced_identity": (
            "-Y(w) tensor C(d) tensor D(e1) + "
            "Y(e1) tensor C(s) tensor D(w)"
        ),
        "forbidden_coefficients": [
            str(value) for value in forbidden_coefficients
        ],
        "common_kernel_gate_excluded": True,
        "adjacent_one_cross_excluded": True,
        "generic_q4_211_incidence_excluded": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_common_kernel_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
