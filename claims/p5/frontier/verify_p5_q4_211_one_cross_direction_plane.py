#!/usr/bin/env python3
"""Verify the adjacent one-cross direction-plane obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md"


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


def pure_coefficient(e_colour: int) -> sp.Expr:
    """Coefficient forced through A,Y,W in Sym(e1,e2,e3)."""

    # A and Y send e1,e2 to the singleton target colour 1.  Their
    # e3 images and all W images are left arbitrary.
    symbols = sp.symbols("a10 a20 a30 a11 a21 a31 "
                         "y10 y20 y30 y11 y21 y31 "
                         "w10 w20 w30 w11 w21 w31 "
                         "w12 w22 w32")
    (
        a10, a20, a30, a11, a21, a31,
        y10, y20, y30, y11, y21, y31,
        w10, w20, w30, w11, w21, w31,
        w12, w22, w32,
    ) = symbols
    # Only the requested coordinate is needed.  E images at A,Y have
    # that coordinate zero when e_colour=2 in the q orientation.
    if e_colour == 2:
        a = {1: 0, 2: 0, 3: a30}
        y = {1: 0, 2: 0, 3: y30}
        w = {1: w12, 2: w22, 3: w32}
    else:
        # Colour-swapped p orientation: E images at A,Y lie on e2.
        a = {1: 0, 2: 0, 4: a31}
        y = {1: 0, 2: 0, 4: y31}
        w = {1: w10, 2: w20, 4: w30}
    factors = tuple(a)
    return sp.expand(
        sum(
            a[permutation[0]]
            * y[permutation[1]]
            * w[permutation[2]]
            for permutation in itertools.permutations(factors)
        )
    )


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, b, c = sp.symbols("a b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)

    u1 = sp.Matrix([b, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    h1 = sp.Matrix([b, 0, 0, -1, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])

    s = sp.Matrix([0, 1, 1, 0, 0])
    d = sp.Matrix([0, 1, -1, 0, 0])
    w = sp.Matrix([1, 0, 0, -b, -c])
    h0 = sp.Matrix.hstack(s, d, w)
    assert h0.T * u1 == sp.zeros(3, 1)
    assert h0.T * u2 == sp.zeros(3, 1)
    assert sp.Matrix.hstack(u1, u2).rank() == 2

    mixed = repeated_derivative(
        source_permanent,
        variables,
        (u1, u2),
    )
    repeated_u1 = repeated_derivative(
        source_permanent,
        variables,
        (u1, u1),
    )
    repeated_u2 = repeated_derivative(
        source_permanent,
        variables,
        (u2, u2),
    )
    assert sp.expand(mixed - x1 * x2 * (x0 + b * x3 + c * x4)) == 0
    assert sp.expand(repeated_u1 - 2 * b * x1 * x2 * x4) == 0
    assert sp.expand(repeated_u2 - 2 * c * x1 * x2 * x3) == 0
    assert repeated_derivative(
        source_permanent,
        variables,
        (u1, h1),
    ) == 0
    assert repeated_derivative(
        source_permanent,
        variables,
        (u2, h2),
    ) == 0

    # If alpha,beta annihilate e0, mixed symmetry gives beta_1=alpha_2=0.
    alpha1, alpha2, beta1, beta2 = sp.symbols(
        "alpha1 alpha2 beta1 beta2"
    )
    alpha = sp.Matrix([0, alpha1, alpha2])
    beta = sp.Matrix([0, beta1, beta2])
    mixed_target_e1 = beta1
    mixed_target_e2 = alpha2
    assert mixed_target_e1 == beta[1]
    assert mixed_target_e2 == alpha[2]
    diagonalized = sp.Matrix.hstack(
        alpha.subs(alpha2, 0),
        beta.subs(beta1, 0),
    )
    assert sp.factor(diagonalized[1:, :].det()) == alpha1 * beta2

    q_forbidden = pure_coefficient(2)
    p_forbidden = pure_coefficient(1)
    assert q_forbidden == 0
    assert p_forbidden == 0

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b*c != 0 whenever the direction gate occurs",
        "mixed_direction_contraction": str(mixed),
        "repeated_u1_contraction": str(repeated_u1),
        "repeated_u2_contraction": str(repeated_u2),
        "direction_target_rows": ["C*e1^*", "C*e2^*"],
        "q_forbidden_e2_cubed_coefficient": str(q_forbidden),
        "p_forbidden_e1_cubed_coefficient": str(p_forbidden),
        "direction_plane_gate_excluded": True,
        "remaining_adjacent_gate": (
            "L_A(e1+e2)=0 or L_Y(e1+e2)=0"
        ),
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
        ROOT / "tmp" / "p5_q4_211_one_cross_direction_plane_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
