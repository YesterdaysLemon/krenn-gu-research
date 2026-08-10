#!/usr/bin/env python3
"""Verify the exact-star obstruction in normalized q5_221."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_STAR_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_coefficient(maps, target_index) -> sp.Expr:
    order = len(maps)
    value = sp.Integer(0)
    for permutation in itertools.permutations(range(order)):
        term = sp.Integer(1)
        for mode, source_index in enumerate(permutation):
            term *= maps[mode][target_index[mode], source_index]
        value += term
    return sp.factor(value)


def nonzero_tensor_coefficients(maps):
    return {
        target_index: coefficient
        for target_index in itertools.product(
            range(3),
            repeat=len(maps),
        )
        if (
            coefficient := permanent_coefficient(maps, target_index)
        ) != 0
    }


def main() -> None:
    q10, q20, q01, q21, q02, q12 = sp.symbols(
        "q10 q20 q01 q21 q02 q12",
    )
    cross_matrix = sp.Matrix(
        (
            (0, q10, q20),
            (q01, 0, q21),
            (q02, q12, 0),
        )
    )
    determinant = sp.factor(cross_matrix.det())
    expected_determinant = q10 * q21 * q02 + q20 * q01 * q12
    assert sp.expand(determinant - expected_determinant) == 0

    # Q_12 in the cycle C_+ has normal pattern (u0,h0,h0).
    # In the factor basis (e0,e1,u1), these representative row maps
    # retain only the target-colour-one pure coefficient.
    zero3 = sp.zeros(1, 3)
    u0_3 = sp.Matrix(((1, 1, 0),))
    h0_3 = sp.Matrix(((1, -1, 0),))
    u1_factor = sp.Matrix(((0, 0, 1),))
    q12_maps = (
        sp.Matrix.vstack(zero3, u1_factor, h0_3),
        sp.Matrix.vstack(u1_factor, u0_3, u1_factor),
        sp.Matrix.vstack(zero3, u0_3, u1_factor),
    )
    q12_coefficients = nonzero_tensor_coefficients(q12_maps)
    assert q12_coefficients == {(1, 1, 1): 2}

    # The rank-one Q_20 gate at V2 contracts by a functional with no
    # h0 coordinate.  The remaining V1 plane is span(h1,u1), and the
    # bilinear factor at V0 is h0.  The representative maps make the
    # resulting target direction explicit.
    ell, plane_a, plane_b = sp.symbols("ell plane_a plane_b")
    h0_20 = sp.Matrix(((1, 0, 0),))
    u1_20 = sp.Matrix(((0, 1, 1),))
    h1_20 = sp.Matrix(((0, 1, -1),))
    q20_maps = (
        sp.Matrix.vstack(h1_20, u1_20, h0_20),
        sp.Matrix.vstack(
            h1_20 + ell * u1_20,
            zero3,
            plane_a * h1_20 + plane_b * u1_20,
        ),
        sp.Matrix.vstack(
            zero3,
            zero3,
            u1_20 + ell * h1_20,
        ),
    )
    q20_coefficients = nonzero_tensor_coefficients(q20_maps)
    assert q20_coefficients == {
        (2, 2, 2): sp.factor(
            -2 * (plane_a * ell - plane_b)
        )
    }

    contraction_coordinates = (0, 1 + ell, 1 - ell)
    contraction_matrix = sp.Matrix(
        (
            (0, contraction_coordinates[2], contraction_coordinates[1]),
            (contraction_coordinates[2], 0, 0),
            (contraction_coordinates[1], 0, 0),
        )
    )
    rank_two_minors = (
        sp.factor(
            contraction_matrix.extract((0, 1), (0, 1)).det()
        ),
        sp.factor(
            contraction_matrix.extract((0, 2), (0, 2)).det()
        ),
    )
    assert rank_two_minors == (
        -(ell - 1) ** 2,
        -(ell + 1) ** 2,
    )
    assert sp.gcd(*rank_two_minors) == 1

    # In cycle C_+, q20*q01*q12 is nonzero.  The h1 coefficient of
    # L_O^* epsilon_0 is the (0,1) entry of M^{-1}.
    central_h1_coefficient = sp.factor(cross_matrix.inv()[0, 1])
    assert central_h1_coefficient == sp.factor(
        q20 * q12 / determinant
    )

    # Restrict T2=Sym(e0,e1,e2,e3) to the mixed target colouring
    # (V0,V1,V2,O)=(0,1,1,0).  Only the four selected rows matter.
    h0_4 = sp.Matrix(((1, -1, 0, 0),))
    u0_4 = sp.Matrix(((1, 1, 0, 0),))
    u1_4 = sp.Matrix(((0, 0, 1, 1),))
    h1_4 = sp.Matrix(((0, 0, 1, -1),))
    shear_h1, shear_u1, shear_scale = sp.symbols(
        "shear_h1 shear_u1 shear_scale",
    )
    leaf1_row = (
        u0_4
        + shear_scale * (shear_h1 * h1_4 + shear_u1 * u1_4)
    )
    central_h0_coefficient = sp.factor(cross_matrix.inv()[0, 0])
    selected_maps = (
        h1_4,
        leaf1_row,
        u0_4,
        central_h0_coefficient * h0_4
        + central_h1_coefficient * h1_4,
    )
    forbidden_coefficient = sp.Integer(0)
    for permutation in itertools.permutations(range(4)):
        term = sp.Integer(1)
        for mode, source_index in enumerate(permutation):
            term *= selected_maps[mode][0, source_index]
        forbidden_coefficient += term
    forbidden_coefficient = sp.factor(forbidden_coefficient)
    assert forbidden_coefficient == sp.factor(
        -4 * q20 * q12 / determinant
    )

    output = {
        "verified": True,
        "field": "C",
        "central_zero_diagonal_determinant": str(determinant),
        "forced_cross_cycles": [
            ["Q20", "Q01", "Q12"],
            ["Q10", "Q21", "Q02"],
        ],
        "Q12_nonzero_coefficients": {
            str(key): str(value)
            for key, value in q12_coefficients.items()
        },
        "Q20_nonzero_coefficients": {
            str(key): str(value)
            for key, value in q20_coefficients.items()
        },
        "rank_one_contraction_rank_two_minors": [
            str(value) for value in rank_two_minors
        ],
        "central_h1_coefficient": str(central_h1_coefficient),
        "leaf1_shear_cancels": not forbidden_coefficient.has(
            shear_scale,
            shear_h1,
            shear_u1,
        ),
        "forced_forbidden_T2_coefficient": str(
            forbidden_coefficient
        ),
        "exact_star_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_star_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
