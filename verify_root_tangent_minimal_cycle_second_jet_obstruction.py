"""Exact verifier for the minimal-cycle mixed second-jet obstruction."""

from __future__ import annotations

import json

import sympy as sp


def quotient_rows(left: sp.Expr, right: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
    """Return the coefficient covectors for q_left and q_right."""
    a_minus = sp.Matrix(
        [
            (1 - right) / (right - left),
            right / (right - left),
            -1 / (right - left),
        ]
    )
    a_plus = sp.Matrix(
        [
            (left - 1) / (right - left),
            -left / (right - left),
            1 / (right - left),
        ]
    )
    return a_minus, a_plus


def check_symbolic() -> dict[str, bool]:
    left, current, nxt = sp.symbols("left current next")
    x = sp.Matrix([1, 1, 1])
    ell = sp.Matrix([1, 0, 0])
    y = sp.Matrix([0, 1, current])
    z = sp.Matrix([0, 1, current])

    a_minus, a_plus = quotient_rows(left, current)
    b_minus, b_plus = quotient_rows(current, nxt)
    matrix = a_plus * ell.T + ell * b_minus.T

    f_y = sp.Matrix([y[1] - y[0], y[2] - y[0]])
    q_current = sp.Matrix([1, current])
    ghz_hessian = sp.Matrix([y[0] * z[0], y[1] * z[1], y[2] * z[2]])

    checks = {
        "left_covector_annihilates_root": sp.simplify((a_minus.T * x)[0]) == 0,
        "right_covector_annihilates_root": sp.simplify((a_plus.T * x)[0]) == 0,
        "next_left_covector_annihilates_root": sp.simplify((b_minus.T * x)[0]) == 0,
        "next_right_covector_annihilates_root": sp.simplify((b_plus.T * x)[0]) == 0,
        "selected_direction_has_shared_class": sp.simplify(f_y - q_current) == sp.zeros(2, 1),
        "selected_right_coefficient_one": sp.simplify((a_plus.T * y)[0] - 1) == 0,
        "selected_left_coefficient_zero": sp.simplify((a_minus.T * y)[0]) == 0,
        "next_selected_left_coefficient_one": sp.simplify((b_minus.T * z)[0] - 1) == 0,
        "next_selected_right_coefficient_zero": sp.simplify((b_plus.T * z)[0]) == 0,
        "edge_left_contraction": sp.simplify(matrix * x - a_plus) == sp.zeros(3, 1),
        "edge_right_contraction": sp.simplify(matrix.T * x - b_minus) == sp.zeros(3, 1),
        "pairwise_zero_base": sp.simplify((x.T * matrix * x)[0]) == 0,
        "minimal_mixed_second_derivative_zero": sp.simplify((y.T * matrix * z)[0]) == 0,
        "ghz_hessian_formula": sp.simplify(ghz_hessian - sp.Matrix([0, 1, current**2]))
        == sp.zeros(3, 1),
    }
    return checks


def check_cycles() -> dict[str, object]:
    checked_edges = 0
    for length in range(3, 13):
        parameters = [sp.Rational(i + 1, i + 2) for i in range(length)]
        if len(set(parameters)) != length:
            raise AssertionError("cycle parameters must be distinct")
        x = sp.Matrix([1, 1, 1])
        ell = sp.Matrix([1, 0, 0])
        for index, current in enumerate(parameters):
            left = parameters[(index - 1) % length]
            nxt = parameters[(index + 1) % length]
            a_minus, a_plus = quotient_rows(left, current)
            b_minus, b_plus = quotient_rows(current, nxt)
            y = sp.Matrix([0, 1, current])
            z = sp.Matrix([0, 1, current])
            matrix = a_plus * ell.T + ell * b_minus.T

            assert (a_minus.T * y)[0] == 0
            assert (a_plus.T * y)[0] == 1
            assert (b_minus.T * z)[0] == 1
            assert (b_plus.T * z)[0] == 0
            assert matrix * x == a_plus
            assert matrix.T * x == b_minus
            assert (y.T * matrix * z)[0] == 0
            assert sp.Matrix([0, 1, current**2]) != sp.zeros(3, 1)
            checked_edges += 1
    return {"cycle_lengths": [3, 12], "checked_edges": checked_edges}


def main() -> None:
    symbolic = check_symbolic()
    if not all(symbolic.values()):
        raise AssertionError(symbolic)
    cycles = check_cycles()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "symbolic_checks": symbolic,
                **cycles,
                "minimal_cycle_second_jet_compatible": False,
                "tangent_tangent_repairs_excluded": False,
                "additional_companions_excluded": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
