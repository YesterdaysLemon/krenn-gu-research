#!/usr/bin/env python3
"""Independently replay the exact GLD92 Q6-boundary minor calculation.

This audit intentionally does not import the GLD71 builder, GLD88 family
builder, or the primary verifier.  It evaluates the seven sparse relation
supports needed by the two displayed minors directly and repeats the exact
determinants, Q6 divisions, and a-resultant test.  The fixed sparse supports
and the rational H4 family are shared mathematical input, so this is an
independent determinant/evaluation route, not an independent proof of the
upstream incidence bridge.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
MINOR_ROWS = {
    "M_28": (0, 1, 2, 17, 25, 28),
    "M_31": (0, 1, 2, 17, 25, 31),
}

# These are the seven immutable GLD71 sparse supports used by the two
# six-minors.  Keeping them here rather than importing the relation builder
# makes the audit's coefficient-evaluation path genuinely separate.
AUDIT_RELATIONS = {
    0: (((1, 1, 1, 1), 1),),
    1: (((0, 0, 0, 0), 1),),
    2: (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    17: (
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 0), -1),
        ((1, 0, 0, 0), -1),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
    ),
    25: (
        ((1, 1, 0, 0), 1),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 2, 0, 0), -1),
        ((1, 2, 0, 1), 1),
        ((1, 2, 1, 0), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 1), 1),
        ((2, 1, 1, 0), 1),
        ((2, 2, 0, 0), 1),
        ((2, 2, 0, 1), -1),
        ((2, 2, 1, 0), -1),
    ),
    28: (
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 2), -1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 2), -1),
        ((0, 1, 1, 0), -1),
        ((0, 1, 1, 2), 1),
        ((2, 0, 1, 0), -1),
        ((2, 0, 1, 2), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 2), 1),
        ((2, 1, 1, 0), 1),
        ((2, 1, 1, 2), -1),
    ),
    31: (
        ((1, 0, 0, 0), 8),
        ((1, 0, 0, 1), -4),
        ((1, 0, 1, 0), -4),
        ((1, 0, 1, 1), 2),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 1, 1, 2), 3),
        ((1, 1, 2, 1), 3),
        ((1, 2, 0, 0), -12),
        ((1, 2, 0, 1), 6),
        ((1, 2, 1, 0), 6),
        ((2, 1, 1, 1), 6),
    ),
}

EXPECTED_NUMERATOR_SREPR_SHA256 = {
    "M_28": "55bfba7b569752acb072ad0922d273e55d70651782e93394a14f9c23098727b8",
    "M_31": "352948a2c113f32f10b90520592cb266cb455853297a664964478fdd7369b18f",
}
EXPECTED_Q6_REMAINDER_SREPR_SHA256 = {
    "M_28": "8efab099320d2e498167c86999ac90adfeb85f2d80d3bd1f4b4e7539577298ef",
    "M_31": "b05d58c3177d7d0c8ea1b54cf7931f0a8e73b314518c748031f9be847d331912",
}
EXPECTED_RESULTANT_SREPR_SHA256 = (
    "fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d"
)
EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256 = (
    "0057c78ceea5241553d856ce437f0fb4fd77571c8205eaa96c7c13dce54cec42"
)
EXPECTED_SUPPORT_DIGEST_SHA256 = (
    "9bea8532ac1a79352508e04db8eca836402a9153edb18fa45e94a012d63162f8"
)


def canonical_polynomial_digest(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> tuple[str, int]:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=sp.QQ)
    encoded = [
        [list(monomial), int(coefficient.p), int(coefficient.q)]
        for monomial, coefficient in polynomial.terms()
    ]
    payload = json.dumps(encoded, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), len(encoded)


def support_digest() -> str:
    encoded = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in support],
        ]
        for row, support in sorted(AUDIT_RELATIONS.items())
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()


def q6_polynomial(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2
        - 2 * p**4 * q
        + p**4
        + 2 * p**3 * q**3
        - 7 * p**3 * q**2
        + 5 * p**3 * q
        - 2 * p**3
        + 2 * p**2 * q**4
        - 7 * p**2 * q**3
        + 12 * p**2 * q**2
        - 7 * p**2 * q
        + 2 * p**2
        - 2 * p * q**4
        + 5 * p * q**3
        - 7 * p * q**2
        + 2 * p * q
        + q**4
        - 2 * q**3
        + 2 * q**2
    )


def h4_family(p: sp.Symbol, q: sp.Symbol, a: sp.Symbol) -> dict[str, sp.Expr]:
    d0 = p + q - 1
    rank_denominator = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    b_numerator = (
        -2 * a * p**2 * q**3
        + 3 * a * p**2 * q**2
        - 3 * a * p**2 * q
        + a * p**2
        + 2 * a * p * q**3
        + 2 * a * p
        + a * q**3
        - 3 * a * q**2
        + 3 * a * q
        - 2 * a
        + p**3 * q**2
        - p**3
        + p**2 * q**3
        - 3 * p**2 * q**2
        + p**2
        - 2 * p * q**3
        + 3 * p * q**2
        - 2 * p
        + q**2
        - 3 * q
        + 2
    )
    c_numerator = (
        2 * a * p * q**3
        - 3 * a * p * q**2
        + 3 * a * p * q
        - a * p
        - a * q**3
        + 3 * a * q**2
        - 3 * a * q
        + 2 * a
        + p**2 * q**2
        - 2 * p**2 * q
        - 3 * p * q**2
        + p * q
        + p
        - q**2
        + 3 * q
        - 2
    )
    kernel_denominator = (p - q) * d0**3
    return {
        "s": sp.factor((p + q - p * q) / d0),
        "b": sp.factor(-b_numerator / ((p**2 - p + 1) * rank_denominator)),
        "c": sp.factor(-c_numerator / (d0 * rank_denominator)),
        "u": sp.factor(
            (q**2 - q + 1) * (2 * p * q - p + q**2 - 2 * q)
            / kernel_denominator
        ),
        "v": sp.factor(
            -(p**2 - p + 1) * (p**2 + 2 * p * q - 2 * p - q)
            / kernel_denominator
        ),
    }


def direct_syndrome_rows(
    leaf: sp.Matrix, rows: tuple[int, ...]
) -> sp.Matrix:
    output = []
    for row_index in rows:
        support = AUDIT_RELATIONS[row_index]
        output.append(
            [
                sp.expand(
                    sum(
                        coefficient
                        * leaf[indices[1], component]
                        * leaf[indices[2], component]
                        * leaf[indices[3], component]
                        for indices, coefficient in support
                        if indices[0] == root
                    )
                )
                for root in range(3)
                for component in range(3)
            ]
        )
    return sp.Matrix(output)


def check() -> dict[str, object]:
    assert set(AUDIT_RELATIONS) == {0, 1, 2, 17, 25, 28, 31}
    assert support_digest() == EXPECTED_SUPPORT_DIGEST_SHA256
    p, q, a = sp.symbols("p q a")
    family = h4_family(p, q, a)
    leaf = sp.Matrix(
        [
            [1, 1, 1],
            [p, q, family["s"]],
            [a, 1 + family["b"], 1 + family["c"]],
        ]
    )
    q6 = q6_polynomial(p, q)
    pnorm = p**2 - p + 1
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    expected_denominator = pnorm**2 * e**2
    minor_data: dict[str, dict[str, object]] = {}
    for key, rows in MINOR_ROWS.items():
        matrix = direct_syndrome_rows(leaf, rows)
        determinant = sp.cancel(matrix[:, PIVOT_COLUMNS].det(method="domain-ge"))
        numerator, denominator = determinant.as_numer_denom()
        numerator = sp.expand(numerator)
        denominator = sp.factor(denominator)
        assert sp.cancel(denominator - expected_denominator) == 0
        numerator_digest = hashlib.sha256(
            sp.srepr(numerator).encode()
        ).hexdigest()
        assert numerator_digest == EXPECTED_NUMERATOR_SREPR_SHA256[key]
        numerator_in_q = sp.Poly(
            numerator, q, domain=sp.QQ.frac_field(p, a)
        )
        q6_in_q = sp.Poly(q6, q, domain=sp.QQ.frac_field(p, a))
        _quotient, remainder = sp.div(numerator_in_q, q6_in_q)
        remainder_expr = sp.expand(remainder.as_expr())
        remainder_digest = hashlib.sha256(
            sp.srepr(remainder_expr).encode()
        ).hexdigest()
        assert remainder_digest == EXPECTED_Q6_REMAINDER_SREPR_SHA256[key]
        assert not remainder.is_zero
        factors = sp.factor_list(numerator)[1]
        minor_data[key] = {
            "rows": list(rows),
            "denominator": str(denominator),
            "numerator_total_degree": sp.Poly(
                numerator, p, q, a
            ).total_degree(),
            "numerator_degree_a": sp.Poly(numerator, a).degree(),
            "numerator_degree_q": sp.Poly(numerator, q).degree(),
            "numerator_terms": len(sp.Poly(numerator, p, q, a).terms()),
            "numerator_srepr_sha256": numerator_digest,
            "numerator_canonical_sha256": canonical_polynomial_digest(
                numerator, (p, q, a)
            )[0],
            "factor_degrees": [
                sp.Poly(factor, p, q, a).total_degree()
                for factor, _exponent in factors
            ],
            "factor_exponents": [
                exponent for _factor, exponent in factors
            ],
            "q6_remainder_degree_q": sp.Poly(remainder_expr, q).degree(),
            "q6_remainder_srepr_sha256": remainder_digest,
            "q6_divides_numerator": False,
        }

    assert minor_data["M_28"]["factor_degrees"] == [1, 20]
    assert minor_data["M_28"]["factor_exponents"] == [3, 1]
    assert minor_data["M_31"]["factor_degrees"] == [1, 1, 18]
    assert minor_data["M_31"]["factor_exponents"] == [1, 3, 1]

    n28_matrix = direct_syndrome_rows(leaf, MINOR_ROWS["M_28"])
    n31_matrix = direct_syndrome_rows(leaf, MINOR_ROWS["M_31"])
    n28 = sp.cancel(
        n28_matrix[:, PIVOT_COLUMNS].det(method="domain-ge")
    ).as_numer_denom()[0]
    n31 = sp.cancel(
        n31_matrix[:, PIVOT_COLUMNS].det(method="domain-ge")
    ).as_numer_denom()[0]
    f28 = sp.cancel(n28 / (p - q) ** 3)
    f31 = sp.cancel(n31 / ((p + q - 1) * (p - q) ** 3))
    f28_factors = sp.factor_list(f28)[1]
    f31_factors = sp.factor_list(f31)[1]
    assert len(f28_factors) == len(f31_factors) == 1
    assert f28_factors[0][1] == f31_factors[0][1] == 1
    assert sp.Poly(f28_factors[0][0], p, q, a).total_degree() == 20
    assert sp.Poly(f31_factors[0][0], p, q, a).total_degree() == 18

    # Check that the common zero set has no hidden a-line on the declared
    # Delta-open.  The coefficient ideal is computed from the directly
    # evaluated F-polynomials, not from the primary's matrix object.
    vertical_equations = [q6]
    for expression in (f28, f31):
        vertical_equations.extend(sp.Poly(expression, a).all_coeffs())
    vertical_basis = sp.groebner(
        vertical_equations, p, q, order="lex"
    )
    vertical_eliminant = sp.factor(vertical_basis.polys[-1].as_expr())
    assert vertical_basis.is_zero_dimensional
    assert vertical_eliminant == q**6 * (q**2 - q + 1) ** 4
    assert vertical_basis.reduce(((p - q) * (p**2 - p + 1)) ** 6)[1] == 0

    q6_factors = sp.factor_list(q6, p, q)[1]
    assert len(q6_factors) == 1
    assert q6_factors[0][1] == 1
    q6_plane_poly = sp.Poly(q6, p, q, domain=sp.QQ)
    for open_factor in (
        p - q,
        p + q - 1,
        p**2 - p + 1,
        p**2 + 2 * p * q - 2 * p - q,
        2 * p * q - p + q**2 - 2 * q,
        2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2,
    ):
        assert sp.gcd(
            q6_plane_poly, sp.Poly(open_factor, p, q, domain=sp.QQ)
        ).total_degree() == 0
    resultant = sp.resultant(f28, f31, a)
    resultant_digest = hashlib.sha256(
        sp.srepr(resultant).encode()
    ).hexdigest()
    assert resultant_digest == EXPECTED_RESULTANT_SREPR_SHA256
    resultant_poly = sp.Poly(resultant, p, q, domain=sp.QQ)
    gcd = sp.gcd(resultant_poly, sp.Poly(q6, p, q, domain=sp.QQ))
    assert gcd.total_degree() == 0
    assert sp.factor(gcd.as_expr()) in (1, -1)
    resultant_in_q = sp.Poly(
        resultant, q, domain=sp.QQ.frac_field(p)
    )
    q6_in_q = sp.Poly(q6, q, domain=sp.QQ.frac_field(p))
    _quotient, remainder = sp.div(resultant_in_q, q6_in_q)
    remainder_digest = hashlib.sha256(
        sp.srepr(remainder.as_expr()).encode()
    ).hexdigest()
    assert remainder_digest == EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256
    assert not remainder.is_zero

    return {
        "status": "independent_sparse_support_exact_replay",
        "gld_identifier": "GLD92",
        "global_conjecture": "UNRESOLVED",
        "imports_primary_verifier": False,
        "imports_GLD71_builder": False,
        "imports_GLD88_family_builder": False,
        "audit_route": "direct seven-support sparse evaluation plus exact SymPy determinants",
        "support_rows": sorted(AUDIT_RELATIONS),
        "support_digest_sha256": support_digest(),
        "minor_data": minor_data,
        "q6": {
            "total_degree": 6,
            "irreducible_over_Q": True,
            "factor_degrees": [
                sp.Poly(factor, p, q).total_degree()
                for factor, _exponent in q6_factors
            ],
            "factor_exponents": [
                exponent for _factor, exponent in q6_factors
            ],
            "Delta_factor_gcds_are_one": True,
        },
        "stripped_minor_degrees": {
            "F28_total_degree": sp.Poly(f28, p, q, a).total_degree(),
            "F28_degree_a": sp.Poly(f28, a).degree(),
            "F31_total_degree": sp.Poly(f31, p, q, a).total_degree(),
            "F31_degree_a": sp.Poly(f31, a).degree(),
        },
        "vertical_fibre_certificate": {
            "coefficient_equation_count": len(vertical_equations),
            "zero_dimensional_base_ideal": True,
            "q_eliminant": str(vertical_eliminant),
            "delta_product": "(p-q)*(p**2-p+1)",
            "delta_product_power_in_ideal": 6,
            "conclusion": "all vertical common-minor fibres lie outside D(Delta)",
        },
        "resultant": {
            "eliminated_variable": "a",
            "total_degree": resultant_poly.total_degree(),
            "degree_q": resultant_in_q.degree(),
            "srepr_sha256": resultant_digest,
            "gcd_with_Q6": str(gcd.as_expr()),
            "q6_divides_resultant": False,
            "q6_remainder_degree_q": remainder.degree(),
            "q6_remainder_srepr_sha256": remainder_digest,
        },
        "independence_boundary": (
            "The audit shares the seven fixed supports and rational family "
            "with the primary; it independently evaluates/determinates them "
            "and does not reprove the GLD75/GLD88 bridge."
        ),
        "finite_common_locus_residual": (
            "V(Q6,F28,F31) intersect D(Omega*Delta), retained rather than "
            "enumerated or excluded"
        ),
    }


def main() -> None:
    result = check()
    print("GLD92 independent sparse-support audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
