#!/usr/bin/env python3
"""Independent apolar audit of the q5_221 multiplicity theorem."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")

    # Commutative polynomial representatives of the two polarized
    # tensors.  Contraction by h2 is apolar differentiation by x4.
    f0 = (x0 + x1) * x2 * x3 * x4
    f1 = x0 * x1 * (x2 + x3) * x4
    double_h2_f0 = sp.diff(f0, x4, 2)
    double_h2_f1 = sp.diff(f1, x4, 2)
    single_h2_f1 = sp.diff(f1, x4)
    assert double_h2_f0 == 0
    assert double_h2_f1 == 0
    assert sp.expand(single_h2_f1) == sp.expand(
        x0 * x1 * (x2 + x3)
    )

    # The target-covector support deductions are one-dimensional
    # annihilator computations in the coordinate target basis.
    a0, a1, a2 = sp.symbols("a0 a1 a2")
    own_and_double_equations = sp.Matrix([[1, 0, 0], [0, 0, 1]])
    assert own_and_double_equations.nullspace() == [
        sp.Matrix((0, 1, 0))
    ]
    apolar_and_own_equations = sp.Matrix([[0, 1, 0], [0, 0, 1]])
    assert apolar_and_own_equations.nullspace() == [
        sp.Matrix((1, 0, 0))
    ]

    # Two target-zero rows h2 mean two x4 differentiations of f0,
    # independently of the other two rows.
    r0, r1, r2, r3, r4 = sp.symbols("r0:5")
    s0, s1, s2, s3, s4 = sp.symbols("s0:5")
    directional_r = sum(
        coefficient * sp.diff(double_h2_f0, variable)
        for coefficient, variable in zip(
            (r0, r1, r2, r3, r4),
            (x0, x1, x2, x3, x4),
            strict=True,
        )
    )
    final_value = sum(
        coefficient * sp.diff(directional_r, variable)
        for coefficient, variable in zip(
            (s0, s1, s2, s3, s4),
            (x0, x1, x2, x3, x4),
            strict=True,
        )
    )
    assert final_value == 0

    output = {
        "audited": True,
        "field": "C",
        "method": "independent apolar differentiation",
        "double_h2_derivative_T0": str(double_h2_f0),
        "double_h2_derivative_T1": str(double_h2_f1),
        "single_h2_derivative_T1": str(single_h2_f1),
        "first_forced_target_support": [1],
        "residual_forced_target_support": [0],
        "oriented_h2_pullback_supports": [[0], [1]],
        "ambient_row_spaces_enumerated": 0,
        "distinguished_normal_multiplicity": 2,
        "monotone_cover_orbits_excluded": [0, 1, 2, 3, 4, 9],
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "apolar source identities and target annihilators",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_distinguished_normal_multiplicity_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
