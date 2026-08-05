#!/usr/bin/env python3
"""Verify the second-cofactor cover of component 22's h0-nonzero residual."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_cofactor_open_obstruction import (
    A,
    D,
    R,
    cofactor_certificate,
    h0,
    h1,
    h2,
    h3,
    mixed_matrix,
    rho,
    s,
)

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H0_NONZERO_"
    "RESIDUAL_SECOND_COFACTOR_COVER_OBSTRUCTION.md"
)
SECOND_ROWS = (0, 2, 3, 4, 5, 7, 8, 10)
SPECIALIZATION = {A: 2, R: 1, D: 3}


def linear_coefficients(polynomial):
    poly = sp.Poly(polynomial, h0, h2)
    assert poly.degree(h0) <= 1
    assert poly.degree(h2) <= 1
    assert poly.coeff_monomial(h0 * h2) == 0
    return (
        poly.coeff_monomial(h0),
        poly.coeff_monomial(h2),
        poly.coeff_monomial(1),
    )


def normalized_qq_poly(expression):
    poly = sp.Poly(expression, rho, domain=sp.QQ)
    _denominator, integral = poly.clear_denoms(convert=True)
    _content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def cramer_certificate(polynomial, residual):
    *_open_factors, cap_g, cap_g2 = residual
    a0, a2, ac = linear_coefficients(cap_g)
    b0, b2, bc = linear_coefficients(polynomial)
    delta = sp.expand(a0 * b2 - a2 * b0)
    n0 = sp.expand(a2 * bc - ac * b2)
    n2 = sp.expand(ac * b0 - a0 * bc)

    assert sp.factor(delta * h0 - n0 - (b2 * cap_g - a2 * polynomial)) == 0
    assert sp.factor(delta * h2 - n2 - (a0 * polynomial - b0 * cap_g)) == 0

    g2_poly = sp.Poly(cap_g2, h0, h2)
    assert g2_poly.degree(h0) <= 1
    assert g2_poly.degree(h2) <= 1
    c02 = g2_poly.coeff_monomial(h0 * h2)
    c0 = g2_poly.coeff_monomial(h0)
    c2 = g2_poly.coeff_monomial(h2)
    cc = g2_poly.coeff_monomial(1)
    numerator = sp.expand(
        c02 * n0 * n2 + c0 * n0 * delta + c2 * n2 * delta + cc * delta**2
    )
    content, primitive = sp.Poly(numerator, rho).primitive()
    assert sp.factor(content - A * D**2 * s * (D + 1)) == 0
    quotient, remainder = sp.div(primitive, sp.Poly(rho + 1, rho))
    assert remainder.is_zero
    assert quotient.degree() == 6
    assert sp.factor(numerator - content * (rho + 1) * quotient.as_expr()) == 0
    return delta, n0, n2, quotient


def specialization_certificate(delta, n0, n2, qbar, matrix):
    delta_s = sp.factor(delta.subs(SPECIALIZATION))
    n0_s = sp.factor(n0.subs(SPECIALIZATION))
    n2_s = sp.factor(n2.subs(SPECIALIZATION))
    assert (
        sp.expand(delta_s + 36 * (7947 * rho**3 + 24451 * rho**2 - 2443 * rho - 16419))
        == 0
    )
    assert sp.expand(n0_s - 12 * (971 * rho**3 - 2989 * rho**2 + 3829 * rho + 205)) == 0
    assert sp.expand(n2_s - 9 * (11 * rho + 7) * (277 * rho**2 + 1092 * rho - 617)) == 0

    delta_poly = sp.Poly(delta_s, rho, domain=sp.QQ)
    n0_poly = sp.Poly(n0_s, rho, domain=sp.QQ)
    assert sp.gcd(delta_poly, n0_poly).degree() == 0
    delta_resultant = sp.resultant(delta_poly, n0_poly)
    assert delta_resultant == -29467769797761114707066880000000

    qbar_s = normalized_qq_poly(qbar.as_expr().subs(SPECIALIZATION))
    expected_qbar = sp.Poly(
        58411813 * rho**6
        + 86961310 * rho**5
        - 782473889 * rho**4
        - 1226471868 * rho**3
        + 1607129299 * rho**2
        + 839733022 * rho
        - 813293399,
        rho,
        domain=sp.QQ,
    )
    assert sp.expand(qbar_s.as_expr() - expected_qbar.as_expr()) == 0

    matrix_s = matrix.subs(SPECIALIZATION)
    second_minor = sp.factor(
        matrix_s.extract(SECOND_ROWS, range(8)).det(method="domain-ge")
    )
    expected_minor = sp.factor(
        5760000
        * rho
        * (rho - 1)
        * (rho + 1)
        * (rho + 2)
        * (3 * rho + 1)
        * (
            1679 * h0 * rho**2
            - 1470 * h0 * rho
            - 3341 * h0
            + 109 * rho**2
            - 138 * rho
            - 55
        )
    )
    assert sp.factor(second_minor - expected_minor) == 0

    restricted_minor = sp.cancel(
        second_minor.subs({h0: n0_s / delta_s, h2: n2_s / delta_s})
    )
    minor_numerator, minor_denominator = sp.fraction(restricted_minor)
    minor_numerator = normalized_qq_poly(minor_numerator)
    expected_minor_numerator = sp.Poly(
        rho
        * (rho - 1)
        * (rho + 1) ** 2
        * (rho + 2)
        * (rho + 13)
        * (3 * rho + 1)
        * (43 * rho - 61)
        * (563 * rho**2 - 600 * rho - 107),
        rho,
        domain=sp.QQ,
    )
    assert (
        sp.expand(minor_numerator.as_expr() - expected_minor_numerator.as_expr()) == 0
    )
    assert (
        sp.expand(
            minor_denominator - (7947 * rho**3 + 24451 * rho**2 - 2443 * rho - 16419)
        )
        == 0
    )
    assert sp.gcd(qbar_s, delta_poly).degree() == 0
    assert sp.gcd(qbar_s, minor_numerator).degree() == 0

    second_resultant = sp.resultant(qbar_s, minor_numerator)
    assert second_resultant != 0
    resultant_hash = hashlib.sha256(str(second_resultant).encode()).hexdigest()
    assert resultant_hash == (
        "ba8be9220435ecae79090a9f35257e9a2a0f13722b63949c83cf45d278274017"
    )
    return {
        "specialization": {str(key): value for key, value in SPECIALIZATION.items()},
        "Delta": str(delta_s),
        "n0": str(n0_s),
        "n2": str(n2_s),
        "Delta_n0_resultant": str(delta_resultant),
        "Qbar": str(qbar_s.as_expr()),
        "second_minor_rows": SECOND_ROWS,
        "second_minor_factorization": str(second_minor),
        "restricted_minor_numerator": str(minor_numerator.as_expr()),
        "Qbar_minor_resultant_sha256": resultant_hash,
    }


def main():
    theorem = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero generic-component theorem",
        "closes the entire",
        "special parameter fibres remain separate",
        "global Krenn--Gu conjecture, which remains **UNRESOLVED**",
    ):
        assert phrase in theorem

    polynomial, _first_minor, residual = cofactor_certificate()
    delta, n0, n2, qbar = cramer_certificate(polynomial, residual)
    matrix = mixed_matrix().subs({h1: 0, h3: s / 2}, simultaneous=True)
    entry_degrees = tuple(sp.Poly(entry, h0, h2).total_degree() for entry in matrix)
    assert max(entry_degrees) <= 2
    specialization = specialization_certificate(delta, n0, n2, qbar, matrix)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23",
                "residual": "h1=0, 2*h3=2*A+R, G=G2=P=0",
                "Delta_rho_degree": int(sp.degree(delta, rho)),
                "Qbar_rho_degree": int(qbar.degree()),
                "mixed_entry_h0_h2_degree_bound": int(max(entry_degrees)),
                "clearing_power_for_second_minor": 16,
                "exact_nonzero_resultant_specialization": specialization,
                "remaining_displayed_residual_binary_empty": True,
                "remaining_h1_nonzero_locus_closed": False,
                "special_parameter_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
