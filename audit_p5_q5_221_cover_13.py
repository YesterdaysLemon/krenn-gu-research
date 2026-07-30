#!/usr/bin/env python3
"""Independent apolar audit for the exact q5_221 cover-13 theorem."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_COVER_13_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def directional_derivative(polynomial, variables, direction):
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
    value = polynomial
    for direction in directions:
        value = directional_derivative(value, variables, direction)
    return sp.expand(value)


def main() -> None:
    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
    variables = (x0, x1, x2, x3)
    f2 = x0 * x1 * x2 * x3
    u0 = (1, 1, 0, 0)
    h0 = (1, -1, 0, 0)
    u1 = (0, 0, 1, 1)
    h1 = (0, 0, 1, -1)

    q0, q1, r0, r1, s0, s1 = sp.symbols(
        "q0 q1 r0 r1 s0 s1"
    )
    q_row = tuple(q0 * u0[index] + q1 * h0[index] for index in range(4))
    r_row = tuple(r0 * u0[index] + r1 * h0[index] for index in range(4))
    s_row = tuple(s0 * h0[index] + s1 * u1[index] for index in range(4))
    support_two_value = repeated_derivative(
        f2,
        variables,
        (h1, q_row, r_row, s_row),
    )
    assert support_two_value == 0

    # The full-support rectangle is the third finite difference in the
    # h1 direction; it vanishes because f2 has y-block degree two.
    triple_h1 = repeated_derivative(
        f2,
        variables,
        (h1, h1, h1),
    )
    assert triple_h1 == 0

    output = {
        "audited": True,
        "field": "C",
        "method": "independent squarefree apolar differentiation",
        "support_two_required_T2_2222": str(support_two_value),
        "third_h1_derivative_T2": str(triple_h1),
        "ambient_row_spaces_enumerated": 0,
        "exact_cover_excluded": True,
        "monotone_cover_excluded": False,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "support-two block and full-support rectangle identities",
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_cover_13_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
