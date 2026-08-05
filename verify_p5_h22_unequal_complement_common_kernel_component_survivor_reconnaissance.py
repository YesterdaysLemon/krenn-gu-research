#!/usr/bin/env python3
"""Verify two exact false-positive H22 survivors on component twenty-two."""

from __future__ import annotations

import itertools
import json

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
    project,
)
from verify_p5_h31_marked_basis_open_branch import one_marked_map
from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)


def product(left, right):
    return sp.Matrix(
        [
            left[i] * right[j] + left[j] * right[i]
            for i, j in itertools.combinations(range(len(left)), 2)
        ]
    )


def pair_profile(alpha, beta):
    return tuple(
        sp.Matrix.hstack(
            product(alpha[i], alpha[j]),
            product(alpha[i], beta[j]),
            product(beta[i], alpha[j]),
            product(beta[i], beta[j]),
        ).rank()
        for i, j in itertools.combinations(range(4), 2)
    )


def check_point(rho, shifts, extension, expected_diagonals, expected_minors):
    alpha, canonical = component_rows(sp.Integer(1), sp.Integer(1), sp.Integer(2))
    beta = shifted(canonical, alpha, shifts)
    model = build_model(alpha, beta, extension, "D01", "finite", rho)
    assert all(sp.factor(value) == 0 for value in model["mixed"])
    assert (sp.factor(model["A"]), sp.factor(model["B"])) == expected_diagonals

    projected_alpha = tuple(
        project(alpha[i], extension[i], "D01", "finite", rho)
        for i in range(4)
    )
    projected_beta = tuple(
        project(beta[i], extension[4 + i], "D01", "finite", rho)
        for i in range(4)
    )
    lifted_alpha = tuple(tuple(alpha[i]) + (extension[i],) for i in range(4))
    lifted_beta = tuple(tuple(beta[i]) + (extension[4 + i],) for i in range(4))
    assert pair_profile(lifted_alpha, lifted_beta) == (4, 4, 4, 4, 4, 4)
    assert pair_profile(projected_alpha, projected_beta) == (4, 4, 4, 3, 3, 3)

    minors = tuple(
        sp.factor(
            one_marked_map(mode, projected_alpha, projected_beta)
            .extract((0, 1, 3, 7), range(4))
            .det()
        )
        for mode in range(4)
    )
    assert minors == expected_minors
    assert all(value != 0 for value in minors)
    return {
        "rho": str(rho),
        "marking": list(map(str, shifts)),
        "extension": list(map(str, extension)),
        "pure_diagonals": list(map(str, expected_diagonals)),
        "lifted_pair_profile": [4, 4, 4, 4, 4, 4],
        "projected_pair_profile": [4, 4, 4, 3, 3, 3],
        "one_marked_ranks": [4, 4, 4, 4],
        "row_0137_minors": list(map(str, minors)),
    }


def main():
    first = check_point(
        sp.Integer(-2),
        (1, 0, 0, -1),
        (
            sp.Rational(8, 5),
            sp.Rational(4, 5),
            sp.Rational(2, 25),
            sp.Rational(-18, 25),
            sp.Rational(3, 25),
            sp.Rational(6, 25),
            sp.Rational(6, 25),
            sp.Integer(1),
        ),
        (sp.Rational(-192, 25), sp.Rational(-18, 25)),
        (
            sp.Rational(27648, 3125),
            sp.Rational(-31104, 3125),
            sp.Rational(-31104, 3125),
            sp.Rational(-27648, 15625),
        ),
    )
    second = check_point(
        sp.Integer(3),
        (0, 0, 0, 1),
        (-3, 5, 6, 1, sp.Rational(-15, 2), -2, -2, 1),
        (sp.Integer(72), sp.Integer(-24)),
        (sp.Integer(73728), sp.Integer(15552), sp.Integer(15552), sp.Integer(110592)),
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 22,
                "direction": "finite D01",
                "points": [first, second],
                "binary_survivors_are_H22_lifts": False,
                "generic_weighted_H22_fibre_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
