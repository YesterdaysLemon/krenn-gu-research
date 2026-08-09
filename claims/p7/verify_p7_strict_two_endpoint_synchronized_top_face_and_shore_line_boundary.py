"""Verify the strict two-endpoint synchronized-top boundary.

This script checks fixed symbolic identities only.  It performs no support,
colour-word, graph-family, or matching-family search.
"""

from __future__ import annotations

import sympy as sp


def verify_endpoint_transfer_rank() -> None:
    """The two endpoint bases transfer through the exchange form."""

    p00, p01, p10, p11 = sp.symbols("p00 p01 p10 p11")
    q00, q01, q10, q11 = sp.symbols("q00 q01 q10 q11")
    left = sp.Matrix(((p00, p01), (p10, p11)))
    right = sp.Matrix(((q00, q01), (q10, q11)))
    exchange = sp.Matrix(((0, 1), (1, 0)))
    response = left * exchange * right.T

    expected = -left.det() * right.det()
    assert sp.expand(response.det() - expected) == 0

    # In endpoint-form bases the response is exactly the exchange matrix and
    # has bilinear rank two.
    assert exchange.det() == -1
    assert exchange.rank() == 2

    # Equal-axis GHZ pair forms span two root directions; an unlike-axis
    # common-colour product has bilinear rank one.
    same_axis_forms = (
        sp.Matrix(((1, 0), (0, 0))),
        sp.Matrix(((0, 0), (0, 1))),
    )
    assert sp.Matrix.hstack(
        *[form.reshape(4, 1) for form in same_axis_forms]
    ).rank() == 2
    unlike_axis_form = sp.Matrix(((1, 0), (0, 0)))
    assert unlike_axis_form.rank() == 1
    assert exchange.rank() != unlike_axis_form.rank()


def verify_dual_companion_selectors() -> None:
    """Independent companion forms have exact dual selector rows."""

    a, b, c, d = sp.symbols("a b c d")
    observation_columns = sp.Matrix(((a, c), (b, d)))
    determinant = observation_columns.det()
    adjugate_selectors = observation_columns.adjugate()

    assert sp.expand(
        adjugate_selectors * observation_columns
        - determinant * sp.eye(2)
    ) == sp.zeros(2)


def verify_shore_line_kernel() -> None:
    """Restriction of a 3 by 3 block to two lines has kernel dimension eight."""

    entries = sp.symbols("x0:9")
    block = sp.Matrix(3, 3, entries)
    left_line = sp.Matrix((1, 0, 0))
    right_line = sp.Matrix((1, 0, 0))
    observed = sp.expand((left_line.T * block * right_line)[0])

    observation_row = sp.Matrix(
        [[sp.diff(observed, entry) for entry in entries]]
    )
    assert observation_row.rank() == 1
    assert len(observation_row.nullspace()) == 8

    invisible = sp.Matrix(((0, 1, 0), (0, 0, 0), (0, 0, 0)))
    assert (left_line.T * invisible * right_line)[0] == 0


def verify_response_fibre() -> None:
    """Check M_a, Phi_a, and Z_a coefficient by coefficient."""

    a, h = sp.symbols("a h", nonzero=True)
    x1, x2, x3, x4 = sp.symbols("x1 x2 x3 x4")
    direct = 1 + a * x3 * x4
    relative = h + a**-1 * x1 * x2
    residual_present = sp.expand(direct * relative)
    expected = h + h * a * x3 * x4 + a**-1 * x1 * x2 + x1 * x2 * x3 * x4

    assert sp.expand(residual_present - expected) == 0
    polynomial_m = sp.Poly(direct, x1, x2, x3, x4)
    polynomial_z = sp.Poly(residual_present, x1, x2, x3, x4)

    assert polynomial_m.coeff_monomial(1) == 1
    assert polynomial_z.coeff_monomial(1) == h
    assert polynomial_m.coeff_monomial(x1 * x2 * x3 * x4) == 0
    assert polynomial_z.coeff_monomial(x1 * x2 * x3 * x4) == 1
    assert polynomial_m.coeff_monomial(x3 * x4) == a
    assert polynomial_z.coeff_monomial(x1 * x2) == a**-1

    corrected_top = (
        polynomial_z.coeff_monomial(x1 * x2 * x3 * x4)
        - h * polynomial_m.coeff_monomial(x1 * x2 * x3 * x4)
    )
    corrected_pair = (
        polynomial_z.coeff_monomial(x1 * x2)
        - h * polynomial_m.coeff_monomial(x1 * x2)
    )
    assert corrected_top == 1
    assert corrected_pair == a**-1
    assert sp.simplify(
        polynomial_m.coeff_monomial(x3 * x4) * corrected_pair
    ) == 1


def main() -> None:
    verify_endpoint_transfer_rank()
    verify_dual_companion_selectors()
    verify_shore_line_kernel()
    verify_response_fibre()
    print(
        {
            "status": "pass",
            "scope": "strict two-endpoint synchronized top face only",
            "endpoint_transfer_rank": 2,
            "companion_selectors": 2,
            "shore_line_observation_rank": 1,
            "shore_line_kernel_dimension": 8,
            "response_fibre_parameter": "a",
            "support_searches": 0,
            "determinant_activated": False,
            "unconditional_p7_exclusion": False,
        }
    )


if __name__ == "__main__":
    main()
