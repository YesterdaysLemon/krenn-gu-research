#!/usr/bin/env python3
"""No-import audit of component 22's residual second-cofactor cover."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H0_NONZERO_"
    "RESIDUAL_SECOND_COFACTOR_COVER_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
FIRST_ROWS = (0, 1, 2, 3, 4, 5, 7, 8)
SECOND_ROWS = (0, 2, 3, 4, 5, 7, 8, 10)

A, R, D = sp.symbols("A R D")
h0, h2, rho = sp.symbols("h0 h2 rho")
x = sp.symbols("x0:8")
s = 2 * A + R


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows():
    u = (1 - D) / 2
    v = (1 + D) / 2
    g = -s / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (g, g, u, v)
    y0 = (0, D * s, -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    alpha = (y0, m, mr, c)
    canonical = (x0, a, a, d)
    marking = (h0, 0, h2, s / 2)
    beta = tuple(add(canonical[i], alpha[i], marking[i]) for i in range(4))
    assert all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4))
    return alpha, beta


def permanent3(selected):
    return sp.expand(
        sum(
            sp.prod(selected[i][permutation[i]] for i in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def mixed_matrix():
    alpha, beta = component_rows()

    def project(row, extension):
        return (row[0], row[1], rho * row[2] + row[3], extension)

    alpha_p = tuple(project(alpha[i], x[i]) for i in range(4))
    beta_p = tuple(project(beta[i], x[4 + i]) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    return sp.Matrix(
        [[sp.diff(coefficients[word], variable) for variable in x] for word in MIXED]
    )


def residual_polynomials():
    f6 = (D - 1) * rho + D + 1
    f7 = (A * D + A + R) * rho + A * D - A - R
    cap_g = (
        (
            4 * A**2 * D**2
            - 4 * A**2 * D
            + 4 * A * R * D**2
            - 4 * A * R * D
            + R**2 * D**2
            - R**2 * D
        )
        * h0
        * rho
        + (
            2 * A**3 * D**2
            + 2 * A**3 * D
            + 4 * A**2 * R * D**2
            + 2 * A**2 * R
            + A * R**2 * D**2
            + A * R**2
        )
        * h2
        * rho
        + (
            -4 * A**2 * D**2
            + 4 * A**2 * D
            - 4 * A * R * D**2
            + 4 * A * R * D
            - R**2 * D**2
            + R**2 * D
        )
        * h0
        + (
            -2 * A**3 * D**2
            + 2 * A**3 * D
            - 4 * A**2 * R * D**2
            - 2 * A**2 * R
            - A * R**2 * D**2
            - A * R**2
        )
        * h2
        + (-(A**2) * D**2 + 5 * A**2 * D - 2 * A**2 + 4 * A * R * D - A * R + R**2 * D)
        * rho
        + A**2 * D**2
        - 3 * A**2 * D
        + 2 * A**2
        - 4 * A * R * D
        + A * R
        - R**2 * D
    )
    cap_g2 = (
        (-8 * A**2 * D + A * R * D**2 - 7 * A * R * D - R**2 * D) * h0 * h2 * rho
        + (-8 * A**2 * D - A * R * D**2 - 7 * A * R * D - R**2 * D) * h0 * h2
        + (-A * D**2 - A * D - R * D) * h0 * rho
        + (2 * A**2 * D - 6 * A**2 - A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        * rho
        + (A * D**2 - A * D - R * D) * h0
        + (2 * A**2 * D - 6 * A**2 + A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        + (A * D**2 - A * D - 2 * A - R) * rho
        - A * D**2
        - A * D
        - 2 * A
        - R
    )
    return f6, f7, cap_g, cap_g2


def linear_coefficients(polynomial):
    poly = sp.Poly(polynomial, h0, h2)
    assert poly.degree(h0) <= 1 and poly.degree(h2) <= 1
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


def audit():
    matrix = mixed_matrix()
    f6, f7, cap_g, cap_g2 = residual_polynomials()
    first_minor = sp.factor(
        matrix.extract(FIRST_ROWS, range(8)).det(method="domain-ge")
    )
    known = sp.factor(
        -8 * A * D * s**4 * (D - 1) * (D + 1) * rho * (rho - 1) * (rho + 1) * f6 * f7
    )
    quotient = sp.cancel(first_minor / known)
    polynomial, denominator = sp.fraction(quotient)
    assert denominator == 1
    polynomial = sp.factor(polynomial)
    assert sp.factor(first_minor - known * polynomial) == 0

    a0, a2, ac = linear_coefficients(cap_g)
    b0, b2, bc = linear_coefficients(polynomial)
    delta = sp.expand(a0 * b2 - a2 * b0)
    n0 = sp.expand(a2 * bc - ac * b2)
    n2 = sp.expand(ac * b0 - a0 * bc)
    assert sp.factor(delta * h0 - n0 - (b2 * cap_g - a2 * polynomial)) == 0
    assert sp.factor(delta * h2 - n2 - (a0 * polynomial - b0 * cap_g)) == 0

    g2_poly = sp.Poly(cap_g2, h0, h2)
    c02 = g2_poly.coeff_monomial(h0 * h2)
    c0 = g2_poly.coeff_monomial(h0)
    c2 = g2_poly.coeff_monomial(h2)
    cc = g2_poly.coeff_monomial(1)
    numerator = sp.expand(
        c02 * n0 * n2 + c0 * n0 * delta + c2 * n2 * delta + cc * delta**2
    )
    content, primitive = sp.Poly(numerator, rho).primitive()
    assert sp.factor(content - A * D**2 * s * (D + 1)) == 0
    qbar, remainder = sp.div(primitive, sp.Poly(rho + 1, rho))
    assert remainder.is_zero and qbar.degree() == 6

    specialization = {A: 2, R: 1, D: 3}
    delta_s = sp.factor(delta.subs(specialization))
    n0_s = sp.factor(n0.subs(specialization))
    n2_s = sp.factor(n2.subs(specialization))
    assert (
        sp.expand(delta_s + 36 * (7947 * rho**3 + 24451 * rho**2 - 2443 * rho - 16419))
        == 0
    )
    assert sp.expand(n0_s - 12 * (971 * rho**3 - 2989 * rho**2 + 3829 * rho + 205)) == 0
    assert sp.expand(n2_s - 9 * (11 * rho + 7) * (277 * rho**2 + 1092 * rho - 617)) == 0
    delta_poly = sp.Poly(delta_s, rho, domain=sp.QQ)
    n0_poly = sp.Poly(n0_s, rho, domain=sp.QQ)
    delta_resultant = sp.resultant(delta_poly, n0_poly)
    assert delta_resultant == -29467769797761114707066880000000

    qbar_s = normalized_qq_poly(qbar.as_expr().subs(specialization))
    expected_qbar = (
        58411813 * rho**6
        + 86961310 * rho**5
        - 782473889 * rho**4
        - 1226471868 * rho**3
        + 1607129299 * rho**2
        + 839733022 * rho
        - 813293399
    )
    assert sp.expand(qbar_s.as_expr() - expected_qbar) == 0

    second_minor = sp.factor(
        matrix.subs(specialization)
        .extract(SECOND_ROWS, range(8))
        .det(method="domain-ge")
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

    restricted = sp.cancel(second_minor.subs({h0: n0_s / delta_s, h2: n2_s / delta_s}))
    minor_numerator, minor_denominator = sp.fraction(restricted)
    minor_numerator = normalized_qq_poly(minor_numerator)
    expected_numerator = (
        rho
        * (rho - 1)
        * (rho + 1) ** 2
        * (rho + 2)
        * (rho + 13)
        * (3 * rho + 1)
        * (43 * rho - 61)
        * (563 * rho**2 - 600 * rho - 107)
    )
    assert sp.expand(minor_numerator.as_expr() - expected_numerator) == 0
    assert (
        sp.expand(
            minor_denominator - (7947 * rho**3 + 24451 * rho**2 - 2443 * rho - 16419)
        )
        == 0
    )
    assert sp.gcd(qbar_s, delta_poly).degree() == 0
    assert sp.gcd(qbar_s, minor_numerator).degree() == 0
    second_resultant = sp.resultant(qbar_s, minor_numerator)
    resultant_hash = hashlib.sha256(str(second_resultant).encode()).hexdigest()
    assert resultant_hash == (
        "ba8be9220435ecae79090a9f35257e9a2a0f13722b63949c83cf45d278274017"
    )

    entry_degree = max(sp.Poly(entry, h0, h2).total_degree() for entry in matrix)
    assert entry_degree <= 2
    return {
        "first_minor_rows": FIRST_ROWS,
        "second_minor_rows": SECOND_ROWS,
        "Delta_degree": int(sp.degree(delta, rho)),
        "Qbar_degree": int(qbar.degree()),
        "mixed_entry_degree_bound": int(entry_degree),
        "Delta_n0_resultant": str(delta_resultant),
        "Qbar_second_minor_resultant_sha256": resultant_hash,
        "specialized_Qbar": str(qbar_s.as_expr()),
        "specialized_second_minor": str(second_minor),
    }


def main():
    theorem = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero generic-component theorem",
        "special parameter fibres remain separate",
        "No finite-field calculation is used",
        "global Krenn--Gu conjecture, which remains **UNRESOLVED**",
    ):
        assert phrase in theorem
    certificate = audit()
    print(
        json.dumps(
            {
                "status": "audit_pass",
                "field": "Q(A,R,D)",
                "repository_imports_used": False,
                "certificate": certificate,
                "remaining_displayed_residual_binary_empty": True,
                "remaining_h1_nonzero_locus_closed": False,
                "special_parameter_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
