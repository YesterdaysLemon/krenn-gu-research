#!/usr/bin/env python3
"""Verify the exact disjoint q4_211 exclusion theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md"


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


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def repeated_derivative(polynomial, variables, directions):
    result = polynomial
    for direction in directions:
        result = derivative(result, variables, direction)
    return sp.factor(result)


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, b, c = sp.symbols("a b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)
    u0 = (a, 1, 1, 0, 0)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)
    n = sp.Matrix([0, 0, 0, c, b])
    s = sp.Matrix([0, 1, 1, 0, 0])
    d = sp.Matrix([0, 1, -1, 0, 0])
    w_minus = sp.Matrix([1, 0, 0, -b, c])

    identities = {
        "u1_h2_h2": repeated_derivative(
            source_permanent, variables, (u1, h2, h2)
        ),
        "u0_h2_h2": repeated_derivative(
            source_permanent, variables, (u0, h2, h2)
        ),
        "u0_h1_h1_h2": repeated_derivative(
            source_permanent, variables, (u0, h1, h1, h2)
        ),
        "u2_h1_h1": repeated_derivative(
            source_permanent, variables, (u2, h1, h1)
        ),
        "u2_h1": repeated_derivative(
            source_permanent, variables, (u2, h1)
        ),
    }
    assert sp.expand(identities["u1_h2_h2"] + 2 * c * x1 * x2) == 0
    assert sp.expand(
        identities["u0_h2_h2"] + 2 * c * x3 * (x1 + x2)
    ) == 0
    assert sp.expand(
        identities["u0_h1_h1_h2"] - 2 * b * (x1 + x2)
    ) == 0
    assert sp.expand(identities["u2_h1_h1"] + 2 * b * x1 * x2) == 0
    assert sp.expand(
        identities["u2_h1"]
        + x1 * x2 * (x0 - b * x3 + c * x4)
    ) == 0

    # Abstract coefficient of Sym(e1,e2,w-) under kernel pattern
    # B(s)=D(s)=0 and C(d)=0.
    vb, vc, vd = sp.symbols("vb vc vd")
    zb, zc, zd = sp.symbols("zb zc zd")
    pattern_matrix = [
        [vb, -vb, zb],
        [vc, vc, zc],
        [vd, -vd, zd],
    ]
    pattern_coefficient = sp.factor(permanent(pattern_matrix))
    assert pattern_coefficient == -2 * vb * vd * zc

    assert d.dot(n) == 0
    assert w_minus.dot(n) == 0
    assert sp.Matrix.hstack(d, w_minus).rank() == 2

    # In the all-s quotient, every e0 target row kills d.  Therefore
    # the e0^4 coefficient of Sym(d,d,e3,e4) is identically zero.
    g0, g1, g2, g3 = sp.symbols("g0 g1 g2 g3")
    e3_values = sp.symbols("r0:4")
    e4_values = sp.symbols("t0:4")
    all_s_e0_matrix = [
        [0, 0, e3_values[index], e4_values[index]]
        for index in range(4)
    ]
    all_s_e0_coefficient = permanent(all_s_e0_matrix)
    assert all_s_e0_coefficient == 0

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a*b*c != 0",
        "propagated_kernel": "L_D(e1+e2)=0",
        "kernel_architectures_before_exclusion": [
            "s,s,s,s",
            "s,s,d,s",
        ],
        "three_s_one_d_cancellation": str(pattern_coefficient),
        "new_normal_from_kernel": str(n.T),
        "all_s_colour_zero_coefficient": str(all_s_e0_coefficient),
        "exact_disjoint_incidence_excluded": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_disjoint_exclusion_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
