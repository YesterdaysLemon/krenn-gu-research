#!/usr/bin/env python3
"""Exact independent audit of the scoped GLD100 g0 gate removal.

The audit is intentionally a single, no-import publication artifact.  The
GLD71 sparse relation supports and the written GLD88/F88 coordinates are
copied below; this file does not load a primary verifier, GLD96, GLD99, or an
exploratory run.  It uses direct sparse determinant accumulation in exact
algebraic number fields for the four residual fibres in the proposed finite
cover.  A permutation determinant at a second specialization is an
independent check of every sparse determinant replayed here.

The default run independently rebuilds the four generic residual coefficients
in Q(p,a)[q]/(Q6), computes all three pair resultants, retains the exact
q-remainder scale and p-content, and checks the full-content gcd/radical
against the named eight-factor support.  It then derives the specialized
q-gcds from those freshly recomputed raw resultants/remainders and performs
the exact algebraic fibre/minor replays below.  The pair-resultant calculation
is a necessary projection only: localization at the Q6 q-leading coefficient
H2 is recorded and its H2 locus is retained for the separate GLD99 handoff.
This is an independent computational audit of the scoped GLD100 leaf, not a
global Krenn--Gu proof; the global status remains UNRESOLVED.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
import sys
import time
from collections import OrderedDict

import sympy as sp
from sympy import QQ


p, q, a, Coff = sp.symbols("p q a C")


# ---------------------------------------------------------------------------
# Immutable copied GLD71 sparse supports and the six displayed 7-by-7 minors.
# ---------------------------------------------------------------------------

SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
PINNED_RELATIONS = {
    0: (((1, 1, 1, 1), 1),),
    1: (((0, 0, 0, 0), 1),),
    2: (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    3: (((2, 0, 2, 0), 1), ((2, 1, 2, 1), -1)),
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
    32: (
        ((0, 0, 0, 1), 1),
        ((0, 0, 0, 2), -3),
        ((0, 0, 1, 0), -2),
        ((0, 0, 1, 1), 4),
        ((0, 0, 2, 1), -6),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 1), -2),
        ((0, 1, 1, 0), 4),
        ((0, 1, 1, 1), -8),
        ((0, 1, 2, 0), -6),
        ((0, 1, 2, 1), 12),
        ((0, 2, 0, 0), -3),
        ((2, 0, 0, 0), -6),
    ),
    33: (
        ((1, 0, 0, 0), 4),
        ((1, 0, 0, 1), -8),
        ((1, 0, 1, 0), -2),
        ((1, 0, 1, 1), 1),
        ((1, 0, 1, 2), 6),
        ((1, 1, 0, 0), -2),
        ((1, 1, 0, 1), 13),
        ((1, 1, 0, 2), -6),
        ((1, 1, 1, 0), -2),
        ((1, 1, 1, 2), -6),
        ((1, 1, 2, 1), 3),
        ((1, 2, 1, 1), 3),
        ((2, 0, 0, 1), 12),
        ((2, 1, 0, 1), -12),
    ),
}

MINORS = OrderedDict(
    (
        ("T0", ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8))),
        ("T1", ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2))),
        ("T2", ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5))),
        ("T3", ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8))),
        ("D0", ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6))),
        ("D2", ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6))),
    )
)

EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
EXPECTED_COVER_RADICAL_DIGEST = (
    "dd930e75eaf842e522b08b661739c53693bb5a7de45414851651e36f291d4361"
)

# These are immutable expected summaries, not imported certificate data.  The
# generic gamma expressions, pair resultants, and gcds are recomputed from the
# copied sparse supports at every invocation and fail closed on any mismatch.
EXPECTED_GENERIC_GAMMAS = OrderedDict(
    (
        (
            "gamma0",
            {
                "a_degree": 2,
                "p_degree": 27,
                "q_degree": 3,
                "terms": 308,
                "srepr_sha256": "ecc04ca65bf325abe133e0d9dabe709f16d01cc8cb2ff4711d07c683cfc76531",
                "raw_denominator": "(p + q - 1)**2*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)",
                "quotient_scale": "4*(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
                "cleared_content": "3",
            },
        ),
        (
            "gamma1",
            {
                "a_degree": 3,
                "p_degree": 32,
                "q_degree": 3,
                "terms": 484,
                "srepr_sha256": "4db77cd0ce9882b9e2f2e7694805153b9e819a8da2e425a853ba427853c65d31",
                "raw_denominator": "(p + q - 1)*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2",
                "quotient_scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
                "cleared_content": "3",
            },
        ),
        (
            "gamma2",
            {
                "a_degree": 3,
                "p_degree": 29,
                "q_degree": 3,
                "terms": 437,
                "srepr_sha256": "b1afa68aee1f50bf708082d6a9d2f2d6552dd222e6f69a6a5473747d11291232",
                "raw_denominator": "(p + q - 1)**2*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2",
                "quotient_scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
                "cleared_content": "3",
            },
        ),
        (
            "gamma3",
            {
                "a_degree": 2,
                "p_degree": 27,
                "q_degree": 3,
                "terms": 308,
                "srepr_sha256": "c171b5d7205afb6d719fe5b3464fa6347968f41e84b0a829c0a81dddfb4bdb2b",
                "raw_denominator": "(p + q - 1)*(p**2 - p + 1)**2*(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)",
                "quotient_scale": "(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
                "cleared_content": "3",
            },
        ),
    )
)

EXPECTED_PAIR_RESULTANTS = {
    "01": {
        "resultant_a_p_degree": 135,
        "resultant_a_q_degree": 15,
        "resultant_a_terms": 2047,
        "resultant_a_sha256": "f01526b8ade89e9474e3a9425f7a87220aa8599b694f2339a64ff1c2681f94e5",
        "q6_remainder_scale": "(2*p**2 - 2*p + 1)**12",
        "q6_remainder_p_content": "p**3*(p**2 - p + 1)**10",
        "q6_remainder_p_content_srepr_sha256": "be67e76c94fec2e342b14a0c533cd6f881429c600e9696b8a324278af4eb0d8d",
        "q6_remainder_p_degree": 144,
        "q6_remainder_q_degree": 3,
        "q6_remainder_terms": 576,
        "q6_remainder_sha256": "0c0abdc92c1b9479a265aa492060965cb046fcd8d13eb2d6c32b6d77fe4149a3",
        "p_eliminant_degree": 544,
        "p_eliminant_sha256": "8f1666c2cc18c3c96b2eb2502533593ded9ef2870261c04be057b5a7d32ee32b",
        "q_resultant_rational_content": "17837583236744824004702123713604783826989481984",
    },
    "02": {
        "resultant_a_p_degree": 133,
        "resultant_a_q_degree": 15,
        "resultant_a_terms": 2074,
        "resultant_a_sha256": "a2db7ada8d86e3529cc58a617449c154f016b0b0fbaa209ae29860cd4d92a6fe",
        "q6_remainder_scale": "(2*p**2 - 2*p + 1)**12",
        "q6_remainder_p_content": "(p**2 - p + 1)**10",
        "q6_remainder_p_content_srepr_sha256": "700320feda3e3b7523253d948ff02de8c5228a2196f525645b3d8bc677ad34d0",
        "q6_remainder_p_degree": 145,
        "q6_remainder_q_degree": 3,
        "q6_remainder_terms": 580,
        "q6_remainder_sha256": "53e8eff8d4196bba8a65afa522da5410ca5f6193c99d41fb17efbb04406fe7f4",
        "p_eliminant_degree": 552,
        "p_eliminant_sha256": "13f408ae39f9df64130f4ade389f3b1835ba6863278b303d0808fdeaf54f6ef7",
        "q_resultant_rational_content": "17837583236744824004702123713604783826989481984",
    },
    "03": {
        "resultant_a_p_degree": 98,
        "resultant_a_q_degree": 12,
        "resultant_a_terms": 1219,
        "resultant_a_sha256": "b3bcbbddba13d6434a764aa7ff579fbfc075e10c523c65ae575e4b288e8d39c2",
        "q6_remainder_scale": "(2*p**2 - 2*p + 1)**9",
        "q6_remainder_p_content": "p*(p**2 - p + 1)**8",
        "q6_remainder_p_content_srepr_sha256": "811c703d9ac35298089376c661354c36b15aef36ab8202c71103242bef072524",
        "q6_remainder_p_degree": 105,
        "q6_remainder_q_degree": 3,
        "q6_remainder_terms": 418,
        "q6_remainder_sha256": "c3b126f686bd1e437710354e1134fd795ba14193df56a50ebd0eddd4c1a591c3",
        "p_eliminant_degree": 406,
        "p_eliminant_sha256": "24ea888f45f850c676c4c89e01bfa01af72ead3abe01cd2103bab9d98f47767e",
        "q_resultant_rational_content": "14836019612485612895559393214464",
    },
}

EXPECTED_COMMON_GCD = {
    "degree": 372,
    "srepr_sha256": "f2fb7f0eaaf3a9b44b4bde6c1486b0cba843141c84eddb9c891c10d5b2cd57aa",
}
EXPECTED_FULL_CONTENT_GCD = {
    "degree": 374,
    "srepr_sha256": "f8bfaa97e9d980852df37e1c98bc82769aba0ab3a762452b55bb0696697d42d2",
}


# This is the proposed finite support, not a substitute for replaying the
# three generic pair resultants.  A4/C4 names are deliberately distinct from
# the affine offset Coff.
COVER_FACTORS = OrderedDict(
    (
        ("p", p),
        ("p_minus_1", p - 1),
        ("P", p**2 - p + 1),
        ("H2", 2 * p**2 - 2 * p + 1),
        ("Q_gamma", p**2 + 1),
        ("Q_other", p**2 - 2 * p + 2),
        ("A4", 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5),
        ("C4", 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5),
    )
)

UPSTREAM_GLD99 = {
    "document_sha256_16": "f5fd49a6ff039f12",
    "used_as": "H2 fibre handoff only; no GLD99 artifact is imported",
    "claim_made_here": False,
}


def support_digest() -> str:
    encoded = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in PINNED_RELATIONS[row]],
        ]
        for row in SUPPORT_ROWS
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()


def digest(expression: sp.Expr) -> str:
    return hashlib.sha256(sp.srepr(sp.expand(expression)).encode()).hexdigest()


def q6_polynomial(p_value: sp.Expr = p, q_value: sp.Expr = q) -> sp.Expr:
    """Literal Q6 polynomial, copied without a generic q-division."""

    return (
        2 * p_value**4 * q_value**2
        - 2 * p_value**4 * q_value
        + p_value**4
        + 2 * p_value**3 * q_value**3
        - 7 * p_value**3 * q_value**2
        + 5 * p_value**3 * q_value
        - 2 * p_value**3
        + 2 * p_value**2 * q_value**4
        - 7 * p_value**2 * q_value**3
        + 12 * p_value**2 * q_value**2
        - 7 * p_value**2 * q_value
        + 2 * p_value**2
        - 2 * p_value * q_value**4
        + 5 * p_value * q_value**3
        - 7 * p_value * q_value**2
        + 2 * p_value * q_value
        + q_value**4
        - 2 * q_value**3
        + 2 * q_value**2
    )


def h4_family(
    p_value: sp.Expr = p,
    q_value: sp.Expr = q,
    a_value: sp.Expr = a,
) -> dict[str, sp.Expr]:
    """Literal transcription of the written GLD88/F88 coordinates."""

    d0 = p_value + q_value - 1
    e = (
        2 * p_value * q_value**2
        - 2 * p_value * q_value
        - p_value
        - q_value**2
        - 2 * q_value
        + 2
    )
    b_numerator = (
        -2 * a_value * p_value**2 * q_value**3
        + 3 * a_value * p_value**2 * q_value**2
        - 3 * a_value * p_value**2 * q_value
        + a_value * p_value**2
        + 2 * a_value * p_value * q_value**3
        + 2 * a_value * p_value
        + a_value * q_value**3
        - 3 * a_value * q_value**2
        + 3 * a_value * q_value
        - 2 * a_value
        + p_value**3 * q_value**2
        - p_value**3
        + p_value**2 * q_value**3
        - 3 * p_value**2 * q_value**2
        + p_value**2
        - 2 * p_value * q_value**3
        + 3 * p_value * q_value**2
        - 2 * p_value
        + q_value**2
        - 3 * q_value
        + 2
    )
    c_numerator = (
        2 * a_value * p_value * q_value**3
        - 3 * a_value * p_value * q_value**2
        + 3 * a_value * p_value * q_value
        - a_value * p_value
        - a_value * q_value**3
        + 3 * a_value * q_value**2
        - 3 * a_value * q_value
        + 2 * a_value
        + p_value**2 * q_value**2
        - 2 * p_value**2 * q_value
        - 3 * p_value * q_value**2
        + p_value * q_value
        + p_value
        - q_value**2
        + 3 * q_value
        - 2
    )
    return {
        "s": (p_value + q_value - p_value * q_value) / d0,
        "b": -b_numerator / ((p_value**2 - p_value + 1) * e),
        "c": -c_numerator / (d0 * e),
        "u": (q_value**2 - q_value + 1)
        * (2 * p_value * q_value - p_value + q_value**2 - 2 * q_value)
        / ((p_value - q_value) * d0**3),
        "v": -(p_value**2 - p_value + 1)
        * (p_value**2 + 2 * p_value * q_value - 2 * p_value - q_value)
        / ((p_value - q_value) * d0**3),
    }


def delta_polynomial(p_value: sp.Expr = p, q_value: sp.Expr = q) -> sp.Expr:
    return (
        (p_value - q_value)
        * (p_value + q_value - 1)
        * (p_value**2 - p_value + 1)
        * (p_value**2 + 2 * p_value * q_value - 2 * p_value - q_value)
        * (2 * p_value * q_value - p_value + q_value**2 - 2 * q_value)
        * (
            2 * p_value * q_value**2
            - 2 * p_value * q_value
            - p_value
            - q_value**2
            - 2 * q_value
            + 2
        )
    )


# ---------------------------------------------------------------------------
# Exact algebraic fields and direct sparse determinant machinery.
# ---------------------------------------------------------------------------


def algebraic_field(factor: sp.Expr):
    factor_poly = sp.Poly(factor, p, domain=QQ)
    if not factor_poly.is_irreducible:
        raise AssertionError(("branch factor is not irreducible over QQ", factor))
    return QQ.alg_field_from_poly(factor_poly, alias="r")


def field_value(field, expression: sp.Expr):
    """Convert an exact expression into the selected algebraic field."""

    return field.convert(sp.cancel(expression))


def branch_value(field, expression: sp.Expr, q_value: sp.Expr, a_value: sp.Expr):
    return field_value(
        field,
        expression.subs(
            {p: field.ext, q: q_value, a: a_value}, simultaneous=True
        ),
    )


def polynomial_entry(expression: sp.Expr, domain) -> sp.Poly:
    return sp.Poly(sp.cancel(expression), Coff, domain=domain)


def specialized_leaf(field, q_expression: sp.Expr, a_expression: sp.Expr, domain):
    # Keep these as SymPy expressions while substituting into F88.  The field
    # domain converts them when the resulting C-polynomials are constructed;
    # feeding its internal ANP object back to ``Expr.subs`` is not supported.
    q_value = sp.cancel(q_expression.subs(p, field.ext))
    a_value = sp.cancel(a_expression.subs(p, field.ext))
    family = h4_family(p, q, a)
    family_values = {
        name: sp.cancel(
            expression.subs(
                {p: field.ext, q: q_value, a: a_value}, simultaneous=True
            )
        )
        for name, expression in family.items()
    }
    return [
        [
            polynomial_entry(1, domain),
            polynomial_entry(1, domain),
            polynomial_entry(1, domain),
        ],
        [
            polynomial_entry(field.ext, domain),
            polynomial_entry(q_value, domain),
            polynomial_entry(family_values["s"], domain),
        ],
        [
            polynomial_entry(a_value, domain),
            polynomial_entry(1 + family_values["b"], domain),
            polynomial_entry(1 + family_values["c"] + Coff, domain),
        ],
    ]


def direct_rows(leaf, rows: tuple[int, ...]) -> dict[int, list[sp.Poly]]:
    domain = leaf[0][0].domain
    zero = sp.Poly(0, Coff, domain=domain)
    result: dict[int, list[sp.Poly]] = {}
    for relation_row in rows:
        entries: list[sp.Poly] = []
        for root in range(3):
            for component in range(3):
                total = zero
                for indices, coefficient in PINNED_RELATIONS[relation_row]:
                    if indices[0] != root:
                        continue
                    total += (
                        coefficient
                        * leaf[indices[1]][component]
                        * leaf[indices[2]][component]
                        * leaf[indices[3]][component]
                    )
                entries.append(total)
        result[relation_row] = entries
    return result


def determinant_sparse(matrix: list[list[sp.Poly]]) -> sp.Poly:
    """Exact row-by-row sparse determinant in the polynomial ring QQ(r)[C]."""

    if not matrix or len(matrix) != len(matrix[0]):
        raise AssertionError("determinant requires a nonempty square matrix")
    domain = matrix[0][0].domain
    zero = sp.Poly(0, Coff, domain=domain)
    one = sp.Poly(1, Coff, domain=domain)
    states: dict[int, sp.Poly] = {0: one}
    for _row in range(len(matrix)):
        next_states: dict[int, sp.Poly] = {}
        for mask, value in states.items():
            for column, entry in enumerate(matrix[_row]):
                if mask & (1 << column):
                    continue
                available_before = sum(
                    1 for previous in range(column) if not mask & (1 << previous)
                )
                term = value * entry
                if available_before & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = next_states.get(new_mask, zero) + term
        states = next_states
    return states[(1 << len(matrix)) - 1]


def digest_payload(payload: object) -> str:
    """Hash a JSON-shaped exact witness without importing another verifier."""

    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def polynomial_certificate(polynomial: sp.Poly) -> dict[str, object]:
    """Serialize an exact polynomial using only JSON scalar/container values."""

    payload = {
        "generators": [str(generator) for generator in polynomial.gens],
        "domain": str(polynomial.domain),
        "terms": [
            {
                "monomial": [int(exponent) for exponent in monomial],
                "coefficient": str(coefficient),
            }
            for monomial, coefficient in polynomial.terms()
        ],
        "expression": str(polynomial.as_expr()),
        "srepr_sha256": digest(polynomial.as_expr()),
    }
    return payload


def quotient_unit_certificate(
    expression: sp.Expr,
    factor: sp.Expr,
    *,
    label: str,
) -> dict[str, object]:
    """Give an exact inverse witness for a rational expression in QQ[p]/(factor)."""

    modulus = sp.Poly(factor, p, domain=QQ).monic()
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    numerator_poly = sp.Poly(numerator, p, domain=QQ).rem(modulus)
    denominator_poly = sp.Poly(denominator, p, domain=QQ).rem(modulus)
    if denominator_poly.is_zero:
        raise AssertionError((label, "zero expression denominator modulo factor", factor))
    denominator_inverse = sp.invert(denominator_poly, modulus)
    denominator_identity = (denominator_poly * denominator_inverse).rem(modulus)
    one = sp.Poly(1, p, domain=QQ)
    if denominator_identity != one:
        raise AssertionError((label, "invalid expression denominator inverse", denominator_identity))
    value = (numerator_poly * denominator_inverse).rem(modulus)
    if value.is_zero:
        raise AssertionError((label, "zero modulo factor", factor))
    inverse = sp.invert(value, modulus)
    identity = (value * inverse).rem(modulus)
    if identity != one:
        raise AssertionError((label, "invalid quotient-field inverse", identity))
    payload = {
        "schema": "gld100-quotient-unit-v1",
        "label": label,
        "modulus": polynomial_certificate(modulus),
        "numerator_remainder": polynomial_certificate(numerator_poly),
        "denominator_remainder": polynomial_certificate(denominator_poly),
        "denominator_inverse_remainder": polynomial_certificate(denominator_inverse),
        "denominator_identity_remainder": polynomial_certificate(denominator_identity),
        "value_remainder": polynomial_certificate(value),
        "inverse_remainder": polynomial_certificate(inverse),
        "identity_remainder": polynomial_certificate(identity),
        "identity_verified": True,
    }
    return {**payload, "sha256": digest_payload(payload)}


def q_relation_certificate(
    reduced: sp.Expr,
    numerator: sp.Expr,
    denominator: sp.Expr,
    factor: sp.Expr,
    *,
    label: str,
) -> dict[str, object]:
    """Certify a rational q relation and its denominator on one p-fibre."""

    modulus = sp.Poly(factor, p, domain=QQ).monic()
    reduced_poly = sp.Poly(sp.cancel(reduced), p, domain=QQ).rem(modulus)
    numerator_poly = sp.Poly(sp.cancel(numerator), p, domain=QQ).rem(modulus)
    denominator_poly = sp.Poly(sp.cancel(denominator), p, domain=QQ).rem(modulus)
    relation = (
        denominator_poly * reduced_poly - numerator_poly
    ).rem(modulus)
    if not relation.is_zero:
        raise AssertionError((label, "q relation cross-multiplication mismatch", relation))
    denominator_unit = quotient_unit_certificate(
        denominator, factor, label=f"{label}_denominator"
    )
    payload = {
        "schema": "gld100-q-relation-v1",
        "label": label,
        "modulus": polynomial_certificate(modulus),
        "reduced_representative": polynomial_certificate(reduced_poly),
        "rational_numerator": polynomial_certificate(numerator_poly),
        "rational_denominator": polynomial_certificate(denominator_poly),
        "cross_multiplication_remainder": polynomial_certificate(relation),
        "cross_multiplication_verified": True,
        "denominator_unit": denominator_unit,
    }
    return {**payload, "sha256": digest_payload(payload)}


def quotient_reduce_q6(
    expression: sp.Expr, modulus: sp.Poly, field
) -> tuple[sp.Expr, dict[str, object]]:
    """Reduce a rational q-expression in the exact field Q(p,a)[q]/(Q6)."""

    numerator, denominator = sp.cancel(expression).as_numer_denom()
    numerator_poly = sp.Poly(numerator, q, domain=field).rem(modulus)
    denominator_poly = sp.Poly(denominator, q, domain=field).rem(modulus)
    if denominator_poly.is_zero:
        raise AssertionError("q-division denominator vanished modulo Q6")
    inverse = sp.invert(denominator_poly, modulus)
    one = sp.Poly(1, q, domain=field)
    inverse_product = (denominator_poly * inverse).rem(modulus)
    if inverse_product != one:
        raise AssertionError(("invalid exact q denominator inverse", inverse_product))
    reduced = (numerator_poly * inverse).rem(modulus)
    cross_multiplication = (
        denominator_poly * reduced - numerator_poly
    ).rem(modulus)
    if not cross_multiplication.is_zero:
        raise AssertionError(
            ("invalid exact quotient reduction", cross_multiplication)
        )
    witness = {
        "schema": "gld100-q6-quotient-v1",
        "numerator_remainder": str(numerator_poly.as_expr()),
        "denominator_remainder": str(denominator_poly.as_expr()),
        "inverse_remainder": str(inverse.as_expr()),
        "inverse_product_remainder": str(inverse_product.as_expr()),
        "cross_multiplication_remainder": str(cross_multiplication.as_expr()),
        "inverse_product_verified": True,
        "cross_multiplication_verified": True,
        "numerator_remainder_sha256": digest(numerator_poly.as_expr()),
        "denominator_remainder_sha256": digest(denominator_poly.as_expr()),
        "inverse_sha256": digest(inverse.as_expr()),
        "reduced_sha256": digest(reduced.as_expr()),
        "relation_sha256": digest_payload(
            {
                "numerator": str(numerator_poly.as_expr()),
                "denominator": str(denominator_poly.as_expr()),
                "inverse": str(inverse.as_expr()),
                "reduced": str(reduced.as_expr()),
                "inverse_product": str(inverse_product.as_expr()),
                "cross_multiplication": str(cross_multiplication.as_expr()),
            }
        ),
    }
    return sp.cancel(reduced.as_expr()), witness


def primitive_clear_generic(expression: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Clear Q(p,a)-coefficient denominators and retain the exact content."""

    field = QQ.frac_field(p, a)
    polynomial = sp.Poly(sp.cancel(expression), q, domain=field)
    if polynomial.is_zero:
        raise AssertionError("generic gamma vanished before primitive clearing")
    coefficient_denominators = [
        sp.cancel(value).as_numer_denom()[1] for value in polynomial.all_coeffs()
    ]
    scale = sp.lcm(coefficient_denominators)
    if scale == 0:
        raise AssertionError("zero q-remainder denominator scale")
    cleared = sp.Poly(
        sp.cancel(scale * polynomial.as_expr()), p, q, a, domain=QQ
    )
    content, primitive = cleared.primitive()
    primitive_expression = sp.expand(primitive.as_expr())
    # This equality keeps the content/primitive split an exact checked
    # identity, rather than merely a normalization convention.
    reconstructed = sp.Poly(
        sp.expand(content.as_expr() * primitive_expression), p, q, a, domain=QQ
    )
    if reconstructed != cleared:
        raise AssertionError("primitive content reconstruction mismatch")
    return primitive_expression, sp.factor(scale), sp.expand(content.as_expr())


def generic_leaf():
    """Build the copied F88 family over Q(p,q,a), with C as the offset."""

    coefficient_field = QQ.frac_field(p, q, a)
    family = h4_family(p, q, a)
    return [
        [
            polynomial_entry(1, coefficient_field),
            polynomial_entry(1, coefficient_field),
            polynomial_entry(1, coefficient_field),
        ],
        [
            polynomial_entry(p, coefficient_field),
            polynomial_entry(q, coefficient_field),
            polynomial_entry(family["s"], coefficient_field),
        ],
        [
            polynomial_entry(a, coefficient_field),
            polynomial_entry(1 + family["b"], coefficient_field),
            polynomial_entry(1 + family["c"] + Coff, coefficient_field),
        ],
    ]


def generic_gamma_atlas() -> tuple[dict[str, object], dict[str, sp.Expr]]:
    """Reconstruct all four generic gamma_i from the copied sparse rows."""

    print("[gld100-audit] generic gamma atlas", file=sys.stderr, flush=True)
    field = QQ.frac_field(p, a)
    modulus = sp.Poly(q6_polynomial(), q, domain=field).monic()
    leaf = generic_leaf()
    target_rows = tuple(
        sorted({row for minor_rows, _ in MINORS.values() for row in minor_rows if row in (0, 1, 2, 17, 25, 28, 31, 32, 33)})
    )
    rows = direct_rows(leaf, target_rows)
    records: dict[str, object] = {}
    gammas: dict[str, sp.Expr] = {}
    for index in range(4):
        name = f"gamma{index}"
        selected_rows, selected_columns = MINORS[f"T{index}"]
        matrix = [[rows[row][column] for column in selected_columns] for row in selected_rows]
        residual = determinant_sparse(matrix)
        if not residual.is_zero and residual.degree() > 1:
            raise AssertionError((name, "raw residual degree exceeds one", residual.degree()))
        if residual.eval(0) != field.zero:
            raise AssertionError((name, "nonzero generic F88 constant residual"))
        raw_gamma = sp.cancel(residual.coeff_monomial(Coff))
        if raw_gamma == 0:
            raise AssertionError((name, "raw gamma vanished"))
        reduced, quotient_witness = quotient_reduce_q6(raw_gamma, modulus, field)
        primitive, quotient_scale, content = primitive_clear_generic(reduced)
        primitive_q = sp.Poly(primitive, q, domain=field)
        if primitive_q.rem(modulus).is_zero:
            raise AssertionError((name, "primitive gamma vanished modulo Q6"))
        primitive_pqa = sp.Poly(primitive, p, q, a, domain=QQ)
        expected = EXPECTED_GENERIC_GAMMAS[name]
        observed = {
            "raw_residual_degree_C": None if residual.is_zero else int(residual.degree()),
            "raw_denominator": str(sp.factor(raw_gamma.as_numer_denom()[1])),
            "quotient_scale": str(sp.factor(quotient_scale)),
            "cleared_content": str(content),
            "a_degree": int(primitive_pqa.degree(a)),
            "p_degree": int(primitive_pqa.degree(p)),
            "q_degree": int(primitive_pqa.degree(q)),
            "terms": len(primitive_pqa.terms()),
            "srepr_sha256": digest(primitive),
            "q6_division_uses_monic_modulus": True,
            "q6_literal_q_leading_coefficient": str(COVER_FACTORS["H2"]),
            "q_leading_coefficient_srepr_sha256": digest(primitive_q.LC()),
            "H2_localization_locus_retained": True,
            "quotient_witness": quotient_witness,
        }
        for key in expected:
            if observed[key] != expected[key]:
                raise AssertionError(
                    (name, "generic gamma metadata mismatch", key, observed[key], expected[key])
                )
        records[name] = observed
        gammas[name] = primitive
    # The atlas is an exact Q(p,a)[q]/(Q6) reconstruction, not four
    # unrelated displayed polynomials: check the common quotient modulus too.
    common = modulus
    for expression in gammas.values():
        common = sp.gcd(common, sp.Poly(expression, q, domain=field))
    if common.degree() != 0:
        raise AssertionError(("generic gamma/Q6 gcd is nontrivial", common.as_expr()))
    return {
        "field": "QQ(p,a)",
        "quotient_modulus": "Q6, monic for q-division",
        "q6_literal_q_leading_coefficient": str(COVER_FACTORS["H2"]),
        "q6_q_leading_coefficient_nonzero_assumed_in_field": True,
        "gamma_count": len(gammas),
        "generic_q_gcd": "1",
        "generic_q_gcd_is_one": True,
        "residuals": records,
        "status": "exact_generic_gamma_reconstruction",
    }, gammas


def factor_records(polynomial: sp.Poly) -> list[dict[str, object]]:
    """Factor a p-polynomial and hash every exact factor representation."""

    _unit, factors = sp.factor_list(polynomial.as_expr(), p)
    return [
        {
            "degree": int(sp.Poly(factor, p, domain=QQ).degree()),
            "multiplicity": int(multiplicity),
            "expression": str(factor),
            "srepr_sha256": digest(factor),
        }
        for factor, multiplicity in factors
    ]


def pair_resultant(
    name: str,
    left: sp.Expr,
    right: sp.Expr,
) -> tuple[sp.Poly, sp.Poly, dict[str, object]]:
    """Recompute one a-resultant, Q6 remainder, and q-resultant exactly."""

    print(f"[gld100-audit] pair resultant {name}", file=sys.stderr, flush=True)
    resultant_a = sp.expand(sp.resultant(left, right, a))
    resultant_a_poly = sp.Poly(resultant_a, p, q, domain=QQ)
    if resultant_a_poly.is_zero:
        raise AssertionError((name, "a-resultant vanished identically"))
    field = QQ.frac_field(p)
    modulus = sp.Poly(q6_polynomial(), q, domain=field).monic()
    remainder = sp.Poly(resultant_a, q, domain=field).rem(modulus)
    if remainder.is_zero:
        raise AssertionError((name, "Q6 remainder vanished identically"))
    coefficients = remainder.all_coeffs()
    coefficient_denominators = [
        sp.cancel(value).as_numer_denom()[1] for value in coefficients
    ]
    scale = sp.factor(sp.lcm(coefficient_denominators))
    cleared = sp.Poly(
        sp.cancel(scale * remainder.as_expr()), q, domain=QQ.poly_ring(p)
    )
    p_content, primitive_q = cleared.primitive()
    p_content_poly = sp.Poly(p_content.as_expr(), p, domain=QQ)
    primitive_expression = sp.expand(primitive_q.as_expr())
    # Verify both exact identities in QQ[p,q]: scaled remainder = cleared and
    # cleared = p-content * primitive q-remainder.
    if sp.Poly(
        sp.cancel(scale * remainder.as_expr()), q, domain=QQ.poly_ring(p)
    ) != cleared:
        raise AssertionError((name, "q-remainder scale identity mismatch"))
    reconstructed = sp.Poly(
        sp.expand(p_content_poly.as_expr() * primitive_expression),
        q,
        domain=QQ.poly_ring(p),
    )
    if reconstructed != cleared:
        raise AssertionError((name, "q-remainder content identity mismatch"))
    primitive_pq = sp.Poly(primitive_expression, p, q, domain=QQ)
    q_resultant_raw = sp.Poly(
        sp.expand(sp.resultant(q6_polynomial(), primitive_expression, q)),
        p,
        domain=QQ,
    )
    if q_resultant_raw.is_zero:
        raise AssertionError((name, "q-resultant vanished identically"))
    rational_content, eliminant = q_resultant_raw.primitive()
    expected = EXPECTED_PAIR_RESULTANTS[name]
    observed = {
        "resultant_a_p_degree": int(resultant_a_poly.degree(p)),
        "resultant_a_q_degree": int(resultant_a_poly.degree(q)),
        "resultant_a_terms": len(resultant_a_poly.terms()),
        "resultant_a_sha256": digest(resultant_a),
        "q6_remainder_scale": str(scale),
        "q6_remainder_p_content": str(sp.factor(p_content_poly.as_expr())),
        "q6_remainder_p_content_srepr_sha256": digest(p_content_poly.as_expr()),
        "q6_remainder_p_degree": int(primitive_pq.degree(p)),
        "q6_remainder_q_degree": int(primitive_pq.degree(q)),
        "q6_remainder_terms": len(primitive_pq.terms()),
        "q6_remainder_sha256": digest(primitive_expression),
        "q_resultant_literal_q6": True,
        "q_resultant_rational_content": str(rational_content),
        "p_eliminant_degree": int(eliminant.degree()),
        "p_eliminant_sha256": digest(eliminant.as_expr()),
        "q6_literal_q_leading_coefficient": str(COVER_FACTORS["H2"]),
        "q6_division_uses_monic_modulus": True,
        "H2_localization_locus_retained": True,
        "p_content_included_in_full_conditions": True,
    }
    for key in expected:
        if observed[key] != expected[key]:
            raise AssertionError(
                (name, "pair resultant metadata mismatch", key, observed[key], expected[key])
            )
    record = {
        **observed,
        "p_eliminant_factors": factor_records(eliminant),
        "q_remainder_exact_identity": True,
        "q_remainder_p_content_exact_identity": True,
    }
    # Keep the freshly recomputed source expressions available to the
    # specialized-fibre audit.  They are consumed before the public report is
    # serialized, so no SymPy object escapes the JSON-shaped audit result.
    source_artifact = {
        "raw_resultant_a": resultant_a,
        "primitive_q_remainder": primitive_expression,
        "p_content": p_content_poly,
        "scale": scale,
    }
    return eliminant, p_content_poly, record, source_artifact


def named_factor_names(polynomial: sp.Poly) -> tuple[list[str], list[dict[str, object]]]:
    records = factor_records(polynomial)
    names: list[str] = []
    for record in records:
        factor = sp.sympify(record["expression"], locals={"p": p})
        matches = [
            factor_name
            for factor_name, expression in COVER_FACTORS.items()
            if sp.Poly(factor, p, domain=QQ).monic()
            == sp.Poly(expression, p, domain=QQ).monic()
        ]
        if len(matches) != 1:
            raise AssertionError(("unexpected p-support factor", factor, matches))
        names.append(matches[0])
        record["name"] = matches[0]
    return names, records


SPECIALIZED_Q_FIBRES = OrderedDict(
    (
        (
            "p_zero",
            {
                "factor": p,
                "q_expected": q**2,
                # The p-content of two pair remainders vanishes at p=0.  The
                # raw a-resultants must therefore be specialized here rather
                # than silently discarding those factors.
                "source_mode": "raw_resultant",
            },
        ),
        (
            "p_one",
            {
                "factor": p - 1,
                "q_expected": (q - 1) ** 2,
                "source_mode": "primitive_q_remainder",
            },
        ),
        (
            "Q_other",
            {
                "factor": p**2 - 2 * p + 2,
                "q_expected": q + p - 2,
                "source_mode": "primitive_q_remainder",
            },
        ),
        (
            "Q_gamma",
            {
                "factor": p**2 + 1,
                "q_expected": q + p,
                "source_mode": "primitive_q_remainder",
            },
        ),
        (
            "A4",
            {
                "factor": 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
                "q_expected": q
                - (
                    sp.Rational(2, 3)
                    - sp.Rational(6, 5) * p
                    + sp.Rational(2, 5) * p**2
                    - sp.Rational(1, 3) * p**3
                ),
                "source_mode": "primitive_q_remainder",
            },
        ),
        (
            "C4",
            {
                "factor": 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
                "q_expected": q
                - (
                    sp.Rational(2, 3)
                    - p
                    + 2 * p**2
                    - sp.Rational(4, 3) * p**3
                ),
                "source_mode": "primitive_q_remainder",
            },
        ),
    )
)


def specialize_q_expression(
    expression: sp.Expr, factor: sp.Expr, field
) -> sp.Poly:
    """Specialize an audit-local p,q expression into QQ<root>[q]."""

    root = field.ext
    coefficient_domain = QQ.poly_ring(q)
    reduced = sp.Poly(
        sp.expand(expression), p, domain=coefficient_domain
    ).rem(sp.Poly(factor, p, domain=coefficient_domain))
    return sp.Poly(sp.cancel(reduced.as_expr().subs(p, root)), q, domain=field)


def q_bezout_gcd(
    polynomials: list[sp.Poly], *, label: str
) -> tuple[sp.Poly, dict[str, object]]:
    """Compute and certify an exact q-gcd with a displayed Bezout identity."""

    if not polynomials:
        raise AssertionError((label, "empty q-gcd family"))
    variable = polynomials[0].gens[0]
    domain = polynomials[0].domain
    gcd_value = polynomials[0]
    coefficients = [sp.Poly(1, variable, domain=domain)]
    for value in polynomials[1:]:
        if value.is_zero:
            coefficients.append(sp.Poly(0, variable, domain=domain))
            continue
        left, right, next_gcd = sp.gcdex(gcd_value, value)
        coefficients = [coefficient * left for coefficient in coefficients]
        coefficients.append(right)
        gcd_value = next_gcd
    if gcd_value.is_zero:
        raise AssertionError((label, "all q-gcd sources vanished"))
    normalized = gcd_value.monic()
    # SymPy's field gcdex is monic in this setting.  Refuse to manufacture a
    # certificate if that contract changes instead of reporting a bare gcd.
    if normalized != gcd_value:
        raise AssertionError((label, "gcdex did not return monic gcd", gcd_value))
    total = sp.Poly(0, variable, domain=domain)
    for coefficient, value in zip(coefficients, polynomials, strict=True):
        total += coefficient * value
    if total != gcd_value:
        raise AssertionError((label, "q Bezout identity mismatch", total, gcd_value))
    payload = {
        "schema": "gld100-q-bezout-v1",
        "label": label,
        "variable": str(variable),
        "domain": str(domain),
        "sources": [polynomial_certificate(value) for value in polynomials],
        "coefficients": [
            polynomial_certificate(coefficient) for coefficient in coefficients
        ],
        "gcd": polynomial_certificate(gcd_value),
        "identity": polynomial_certificate(total),
        "identity_verified": True,
    }
    return gcd_value, {**payload, "sha256": digest_payload(payload)}


def specialized_q_fibre_report(
    pair_artifacts: dict[str, object],
) -> dict[str, object]:
    """Derive every retained q-gcd from this audit's pair-resultant outputs."""

    reports: dict[str, object] = {}
    for name, definition in SPECIALIZED_Q_FIBRES.items():
        factor = definition["factor"]
        field = algebraic_field(factor)
        root = field.ext
        modulus = specialize_q_expression(q6_polynomial(), factor, field)
        if modulus.is_zero:
            raise AssertionError((name, "specialized Q6 vanished"))
        q6_specialized = modulus.monic()
        source_polynomials: list[sp.Poly] = []
        unit_gates: dict[str, object] = {}
        source_mode = definition["source_mode"]
        p_content_remainders: dict[str, dict[str, object]] = {}
        for pair_name in ("03", "01", "02"):
            artifact = pair_artifacts[pair_name]
            content = artifact["p_content"]
            scale = artifact["scale"]
            # This is a scalar in QQ<root>.  Reduce it directly in that field;
            # wrapping an expression containing the algebraic alias ``r`` as
            # a polynomial in the unrelated source symbol ``p`` is invalid.
            content_remainder = content.rem(sp.Poly(factor, p, domain=QQ))
            content_scalar = field.convert(
                sp.cancel(content_remainder.as_expr().subs(p, root))
            )
            p_content_remainders[pair_name] = {
                "expression": str(content_scalar),
                "is_zero": bool(content_scalar == field.zero),
            }
            if source_mode == "raw_resultant":
                expression = artifact["raw_resultant_a"]
            else:
                expression = artifact["primitive_q_remainder"]
                unit_gates[pair_name] = {
                    "p_content": quotient_unit_certificate(
                        content.as_expr(),
                        factor,
                        label=f"{name}_{pair_name}_p_content",
                    ),
                    "clearing_scale": quotient_unit_certificate(
                        scale,
                        factor,
                        label=f"{name}_{pair_name}_clearing_scale",
                    ),
                }
            source_polynomial = specialize_q_expression(expression, factor, field)
            source_polynomials.append(source_polynomial)
        if source_mode == "raw_resultant":
            # The raw route is admitted only because at least one removed
            # p-content actually vanishes; all clearing scales remain units.
            if not any(
                gate["is_zero"] for gate in p_content_remainders.values()
            ):
                raise AssertionError((name, "raw route lacks vanishing p-content"))
            scale_units = {
                pair_name: quotient_unit_certificate(
                    pair_artifacts[pair_name]["scale"],
                    factor,
                    label=f"{name}_{pair_name}_clearing_scale_raw",
                )
                for pair_name in ("03", "01", "02")
            }
            unit_gates = {
                "mode": "raw_resultant_preserves_zero_p_content",
                "p_content_remainders": p_content_remainders,
                "clearing_scale_units": scale_units,
            }
        q_gcd, bezout = q_bezout_gcd(
            [q6_specialized, *source_polynomials], label=f"{name}_q_gcd"
        )
        expected = sp.Poly(
            sp.cancel(definition["q_expected"].subs(p, root)),
            q,
            domain=field,
        ).monic()
        if q_gcd != expected:
            raise AssertionError((name, "derived q-gcd mismatch", q_gcd, expected))
        reports[name] = {
            "factor": str(factor),
            "field": str(field),
            "source_mode": source_mode,
            "q6_specialized": polynomial_certificate(q6_specialized),
            "sources": [
                polynomial_certificate(source) for source in source_polynomials
            ],
            "specialization_unit_gates": unit_gates,
            "q_gcd": polynomial_certificate(q_gcd),
            "q_gcd_degree": int(q_gcd.degree()),
            "expected_q_gcd": polynomial_certificate(expected),
            "q_gcd_derived_from_pair_outputs": True,
            "bezout_certificate": bezout,
            "status": "independent_exact_specialized_q_gcd",
        }
    return reports


def generic_pair_resultant_bridge(
    gamma_atlas: tuple[dict[str, object], dict[str, sp.Expr]] | None = None,
) -> dict[str, object]:
    """Run the exact generic pair-resultant projection and support audit."""

    if gamma_atlas is None:
        gamma_report, gammas = generic_gamma_atlas()
    else:
        gamma_report, gammas = gamma_atlas
    eliminants: dict[str, sp.Poly] = {}
    contents: dict[str, sp.Poly] = {}
    pair_reports: dict[str, object] = {}
    pair_artifacts: dict[str, object] = {}
    for right_index in (1, 2, 3):
        name = f"0{right_index}"
        eliminant, content, report, source_artifact = pair_resultant(
            name, gammas["gamma0"], gammas[f"gamma{right_index}"]
        )
        eliminants[name] = eliminant
        contents[name] = content
        pair_reports[name] = report
        pair_artifacts[name] = source_artifact

    common_01 = sp.gcd(eliminants["01"], eliminants["02"]).monic()
    common_gcd = sp.gcd(common_01, eliminants["03"]).monic()
    common_radical = common_gcd.sqf_part().monic()
    full_conditions = {
        name: (eliminants[name] * contents[name].sqf_part()).monic()
        for name in eliminants
    }
    full_01 = sp.gcd(full_conditions["01"], full_conditions["02"]).monic()
    full_gcd = sp.gcd(full_01, full_conditions["03"]).monic()
    full_radical = full_gcd.sqf_part().monic()
    common_gcd_names, common_gcd_factor_report = named_factor_names(common_gcd)
    full_gcd_names, full_gcd_factor_report = named_factor_names(full_gcd)
    common_names, common_factor_report = named_factor_names(common_radical)
    full_names, full_factor_report = named_factor_names(full_radical)
    expected_names = set(COVER_FACTORS)
    if (
        set(common_gcd_names) != expected_names
        or set(full_gcd_names) != expected_names
        or set(common_names) != expected_names
        or set(full_names) != expected_names
    ):
        raise AssertionError(
            (
                "pair-resultant radical support mismatch",
                common_gcd_names,
                full_gcd_names,
                common_names,
                full_names,
            )
        )
    if common_radical.degree() != 18 or full_radical.degree() != 18:
        raise AssertionError(("pair-resultant radical degree mismatch", common_radical.degree(), full_radical.degree()))
    if digest(common_radical.as_expr()) != EXPECTED_COVER_RADICAL_DIGEST:
        raise AssertionError(("common pair radical digest mismatch", digest(common_radical.as_expr())))
    if digest(full_radical.as_expr()) != EXPECTED_COVER_RADICAL_DIGEST:
        raise AssertionError(("full-content pair radical digest mismatch", digest(full_radical.as_expr())))
    if common_gcd.degree() != EXPECTED_COMMON_GCD["degree"] or digest(common_gcd.as_expr()) != EXPECTED_COMMON_GCD["srepr_sha256"]:
        raise AssertionError(("common pair gcd mismatch", common_gcd.degree(), digest(common_gcd.as_expr())))
    if full_gcd.degree() != EXPECTED_FULL_CONTENT_GCD["degree"] or digest(full_gcd.as_expr()) != EXPECTED_FULL_CONTENT_GCD["srepr_sha256"]:
        raise AssertionError(("full-content pair gcd mismatch", full_gcd.degree(), digest(full_gcd.as_expr())))
    full_content_names, full_content_factor_report = named_factor_names(full_gcd.sqf_part().monic())
    if set(full_content_names) != expected_names:
        raise AssertionError(("full-content gcd radical support mismatch", full_content_names))
    specialized_q_fibres = specialized_q_fibre_report(pair_artifacts)
    return {
        "status": "exact_generic_pair_resultant_bridge",
        "logical_scope": (
            "A common Q6 root of gamma0,gamma1,gamma2,gamma3 must lie over a p root common to all three pair eliminants; this is a necessary projection only."
        ),
        "gamma_atlas": gamma_report,
        "pairs": pair_reports,
        "common_pair_gcd": {
            "degree": int(common_gcd.degree()),
            "srepr_sha256": digest(common_gcd.as_expr()),
            "factors": common_gcd_factor_report,
            "radical_degree": int(common_radical.degree()),
            "radical_srepr_sha256": digest(common_radical.as_expr()),
            "radical_factor_names": common_names,
            "radical_factors": common_factor_report,
            "p_content_included": False,
        },
        "full_content_gcd": {
            "degree": int(full_gcd.degree()),
            "srepr_sha256": digest(full_gcd.as_expr()),
            "factors": full_gcd_factor_report,
            "radical_degree": int(full_radical.degree()),
            "radical_srepr_sha256": digest(full_radical.as_expr()),
            "radical_factor_names": full_names,
            "radical_factors": full_factor_report,
            "full_gcd_radical_factors": full_content_factor_report,
            "p_content_included": True,
        },
        "specialized_q_fibres": specialized_q_fibres,
        "q6_leading_coefficient_caveat": {
            "literal_q_leading_coefficient": str(COVER_FACTORS["H2"]),
            "q_division_modulus_is_monic": True,
            "localizes_at_H2": True,
            "H2_locus_retained_in_support": True,
            "degree_drop_roots_not_discarded": True,
            "q_resultants_use_literal_Q6_after_remainder_primitive_clear": True,
        },
        "factor_support_exact": True,
        "radical_degree": 18,
        "radical_srepr_sha256": EXPECTED_COVER_RADICAL_DIGEST,
    }


def permutation_determinant(matrix):
    """Independent dense determinant replay after C specialization."""

    size = len(matrix)
    total = matrix[0][0] * 0
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = matrix[0][0] * 0 + 1
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total = total - term if inversions & 1 else total + term
    return total


def polynomial_equal(left: sp.Poly, right_expression: sp.Expr) -> bool:
    right = sp.Poly(right_expression, Coff, domain=left.domain)
    return left == right


def polynomial_record(polynomial: sp.Poly) -> dict[str, object]:
    return {
        "degree_C": None if polynomial.is_zero else int(polynomial.degree()),
        "terms": len(polynomial.terms()),
        "srepr_sha256": digest(polynomial.as_expr()),
        "expression": str(polynomial.as_expr()),
    }


def verify_dense_control(
    field,
    polynomial: sp.Poly,
    matrix: list[list[sp.Poly]],
    values: tuple[int, ...] = (0, 1, 2),
) -> list[int]:
    """Cross-check sparse and dense determinants at three exact C values."""

    if not polynomial.is_zero and polynomial.degree() > 2:
        raise AssertionError(("direct determinant degree exceeds two", polynomial.degree()))
    checked: list[int] = []
    for value in values:
        sparse_value = field.convert(polynomial.eval(value))
        dense_matrix = [[entry.eval(value) for entry in row] for row in matrix]
        dense_value = field.convert(permutation_determinant(dense_matrix))
        if sparse_value != dense_value:
            raise AssertionError(("sparse/dense determinant mismatch", value))
        checked.append(value)
    return checked


# ---------------------------------------------------------------------------
# Named-support checks and exact branch replays.
# ---------------------------------------------------------------------------


def cover_report(pair_bridge_verified: bool = False) -> dict[str, object]:
    factor_polys = [sp.Poly(value, p, domain=QQ) for value in COVER_FACTORS.values()]
    product = sp.Poly(sp.prod(factor_polys), p, domain=QQ)
    squarefree = product.sqf_part().monic()
    factorization = sp.factor_list(squarefree.as_expr(), p)[1]
    names = []
    for factor, multiplicity in factorization:
        if multiplicity != 1:
            raise AssertionError(("named support is not squarefree", factor, multiplicity))
        matched = [name for name, expression in COVER_FACTORS.items()
                   if sp.Poly(expression, p, domain=QQ).monic() == sp.Poly(factor, p, domain=QQ).monic()]
        if len(matched) != 1:
            raise AssertionError(("unexpected named support factor", factor, matched))
        names.append(matched[0])
    if set(names) != set(COVER_FACTORS):
        raise AssertionError(("named support factor set changed", names))
    radical_digest = digest(squarefree.as_expr())
    if radical_digest != EXPECTED_COVER_RADICAL_DIGEST:
        raise AssertionError(("named support radical digest", radical_digest))
    q6_leading = sp.Poly(q6_polynomial(), q, domain=QQ.poly_ring(p)).LC()
    if sp.expand(q6_leading - COVER_FACTORS["H2"]) != 0:
        raise AssertionError(("H2 is not Q6 q-leading coefficient", q6_leading))
    # The first two survivor assertions are pointwise boundary checks.  The
    # specialized q-gcd derivation is performed separately from the freshly
    # recomputed pair-resultant sources.
    delta_p0 = sp.expand(delta_polynomial().subs({p: 0, q: 0}))
    delta_p1 = sp.expand(delta_polynomial().subs({p: 1, q: 1}))
    q6_p0 = sp.expand(q6_polynomial().subs({p: 0, q: 0}))
    q6_p1 = sp.expand(q6_polynomial().subs({p: 1, q: 1}))
    if delta_p0 != 0 or delta_p1 != 0 or q6_p0 != 0 or q6_p1 != 0:
        raise AssertionError(
            ("p/p-1 survivor check", delta_p0, delta_p1, q6_p0, q6_p1)
        )
    delta_in_p = sp.Poly(delta_polynomial(), p, domain=QQ.frac_field(q))
    P_in_p = sp.Poly(COVER_FACTORS["P"], p, domain=QQ)
    if not delta_in_p.rem(P_in_p).is_zero:
        raise AssertionError("P factor was not found in Delta")
    return {
        "named_factor_names": names,
        "named_radical_degree": squarefree.degree(),
        "named_radical_srepr_sha256": radical_digest,
        "q6_q_leading_coefficient": str(q6_leading),
        "p_survivor": {"q": "0", "delta": "0"},
        "p_minus_1_survivor": {"q": "1", "delta": "0"},
        "p_survivor_Q6_zero": True,
        "p_minus_1_survivor_Q6_zero": True,
        "P_excluded_by_Delta": True,
        "H2_reserved_for_GLD99_handoff": True,
        "pair_resultant_identity_replayed": bool(pair_bridge_verified),
        "status": (
            "exact_named_support_product_after_generic_pair_replay"
            if pair_bridge_verified
            else "named_support_product_without_pair_replay"
        ),
    }


BRANCHES = OrderedDict(
    (
        (
            "Q_gamma",
            {
                "factor": p**2 + 1,
                "q": -p,
                "q_numerator": -p,
                "q_denominator": sp.Integer(1),
                "a": sp.Integer(0),
                "identity_minor": "D0",
                "identity": 192 * (1 - p),
                "expected_gamma_gcd": a,
            },
        ),
        (
            "Q_other",
            {
                "factor": p**2 - 2 * p + 2,
                "q": 2 - p,
                "q_numerator": 2 - p,
                "q_denominator": sp.Integer(1),
                "a": a,
                "identity_minor": None,
                "identity": None,
                "expected_gamma_gcd": sp.Integer(1),
            },
        ),
        (
            "A4",
            {
                "factor": 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
                "q": sp.Rational(2, 3) - 6 * p / 5 - p**3 / 3 + 2 * p**2 / 5,
                "q_numerator": 2 * p - 1,
                "q_denominator": p - 2,
                "a": sp.Integer(0),
                "identity_minor": "D0",
                "identity": -sp.Rational(7776, 3125)
                * (p + 1)
                * (8171 * p**2 - 5068 * p + 1965),
                "expected_gamma_gcd": a,
            },
        ),
        (
            "C4",
            {
                "factor": 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
                "q": sp.Rational(2, 3) - 4 * p**3 / 3 - p + 2 * p**2,
                "q_numerator": p + 1,
                "q_denominator": 2 * p - 1,
                "a": p,
                "identity_minor": "D2",
                "identity": sp.Rational(243, 128)
                * (p - 1)
                * (52 * p**2 + 2 * p + 25),
                "expected_gamma_gcd": a - p,
            },
        ),
    )
)


def branch_q_consistency_report() -> dict[str, object]:
    """Link the derived q-gcd representatives to the branch replays."""

    reports: dict[str, object] = {}
    for name in ("Q_gamma", "Q_other", "A4", "C4"):
        factor = BRANCHES[name]["factor"]
        expected_from_projection = SPECIALIZED_Q_FIBRES[name]["q_expected"]
        expected_from_branch = q - BRANCHES[name]["q"]
        coefficient_domain = QQ.poly_ring(q)
        remainder = sp.Poly(
            sp.expand(expected_from_projection - expected_from_branch),
            p,
            domain=coefficient_domain,
        ).rem(sp.Poly(factor, p, domain=coefficient_domain))
        if not remainder.is_zero:
            raise AssertionError((name, "projection/branch q mismatch", remainder))
        reports[name] = {
            "factor": str(factor),
            "projection_q_polynomial": str(expected_from_projection),
            "branch_q_polynomial": str(expected_from_branch),
            "remainder_mod_factor": "0",
            "consistent": True,
        }
    return reports


def verify_branch_geometry(name: str, record: dict[str, object], field):
    factor = record["factor"]
    q_expression = record["q"]
    root = field.ext
    q_expression_value = sp.cancel(q_expression.subs(p, root))
    q_value = field_value(field, q_expression_value)
    q6_value = field_value(
        field,
        q6_polynomial(p, q).subs(
            {p: root, q: q_expression_value}, simultaneous=True
        ),
    )
    if q6_value != field.zero:
        raise AssertionError((name, "Q6 does not vanish on supplied q branch", q6_value))
    q_relation = q_relation_certificate(
        q_expression,
        record["q_numerator"],
        record["q_denominator"],
        factor,
        label=f"{name}_q",
    )
    delta_value = field_value(
        field,
        delta_polynomial(p, q).subs(
            {p: root, q: q_expression_value}, simultaneous=True
        ),
    )
    if delta_value == field.zero:
        raise AssertionError((name, "branch lies on Delta"))
    delta_expression = sp.cancel(
        delta_polynomial(p, q).subs(q, q_expression)
    )
    delta_unit = quotient_unit_certificate(
        delta_expression, factor, label=f"{name}_Delta"
    )
    coefficient = (
        record["identity"] if record["identity"] is not None else sp.Integer(1)
    )
    coefficient_gcd = sp.gcd(
        sp.Poly(factor, p, domain=QQ),
        sp.Poly(coefficient, p, domain=QQ),
    )
    coefficient_gcd_degree = coefficient_gcd.degree()
    if record["identity"] is not None and coefficient_gcd_degree != 0:
        raise AssertionError((name, "claimed lambda is not a field unit", coefficient_gcd))
    lambda_unit = None
    if record["identity"] is not None:
        lambda_unit = quotient_unit_certificate(
            record["identity"], factor, label=f"{name}_lambda"
        )
    return {
        "factor": str(factor),
        "factor_degree": sp.Poly(factor, p, domain=QQ).degree(),
        "factor_irreducible_Q": sp.Poly(factor, p, domain=QQ).is_irreducible,
        "abstract_root": str(root),
        "q": str(q_value),
        "Q6_zero": True,
        "Delta_nonzero": True,
        "Delta_unit": delta_unit,
        "q_relation_certificate": q_relation,
        "lambda_factor_gcd_degree": coefficient_gcd_degree,
        "lambda_unit": lambda_unit,
    }, q_value


def clear_a_polynomial(expression: sp.Expr, field) -> sp.Poly:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    denominator_poly = sp.Poly(denominator, a, domain=field)
    if denominator_poly.degree() > 0:
        raise AssertionError(("gamma has an a-dependent denominator", denominator))
    return sp.Poly(numerator, a, domain=field)


def gamma_branch(name: str, record: dict[str, object]) -> dict[str, object]:
    """Replay all four B=0 residual C coefficients over an exact field."""

    field = algebraic_field(record["factor"])
    domain = field.frac_field(a)
    leaf = specialized_leaf(field, record["q"], a, domain)
    rows = direct_rows(leaf, tuple(sorted({row for rows, _ in MINORS.values() for row in rows})))
    gammas: list[sp.Poly] = []
    records: dict[str, object] = {}
    for name_index in range(4):
        minor_name = f"T{name_index}"
        selected_rows, selected_columns = MINORS[minor_name]
        matrix = [[rows[row][column] for column in selected_columns] for row in selected_rows]
        polynomial = determinant_sparse(matrix)
        # The exact route requires the four residuals to be affine in C.
        if not polynomial.is_zero and polynomial.degree() > 1:
            raise AssertionError((name, minor_name, "residual degree exceeds one", polynomial.degree()))
        if polynomial.eval(0) != domain.zero:
            raise AssertionError((name, minor_name, "nonzero F88 constant residual"))
        gamma = polynomial.coeff_monomial(Coff)
        gamma_poly = clear_a_polynomial(gamma, field)
        gammas.append(gamma_poly)
        records[minor_name] = {
            "degree_C": None if polynomial.is_zero else int(polynomial.degree()),
            "gamma_a_degree": None if gamma_poly.is_zero else int(gamma_poly.degree()),
            "gamma_srepr_sha256": digest(gamma_poly.as_expr()),
        }
    common = sp.Poly(0, a, domain=field)
    for gamma in gammas:
        common = sp.gcd(common, gamma)
    if not common.is_zero:
        common = common.monic()
    expected = sp.Poly(
        record["expected_gamma_gcd"].subs(p, field.ext), a, domain=field
    )
    expected = expected.monic() if not expected.is_zero else expected
    if common != expected:
        raise AssertionError((name, "gamma gcd mismatch", common.as_expr(), expected.as_expr()))
    return {
        "field": str(field),
        "q": str(field_value(field, record["q"].subs(p, field.ext))),
        "gamma_gcd": str(common.as_expr()),
        "gamma_gcd_degree": None if common.is_zero else int(common.degree()),
        "expected_gamma_gcd": str(expected.as_expr()),
        "common_affine_gamma_zero_empty": common.degree() == 0,
        "residuals": records,
        "status": "exact_gamma_gcd_replay",
    }


def direct_branch(name: str, record: dict[str, object]) -> dict[str, object]:
    """Replay all six minors and compare D0/D2 with the declared identity."""

    field = algebraic_field(record["factor"])
    domain = field
    q_expression = record["q"]
    a_expression = record["a"]
    leaf = specialized_leaf(field, q_expression, a_expression, domain)
    all_rows = tuple(sorted({row for rows, _ in MINORS.values() for row in rows}))
    rows = direct_rows(leaf, all_rows)
    geometry, q_value = verify_branch_geometry(name, record, field)
    minors: dict[str, sp.Poly] = {}
    records: dict[str, object] = {}
    dense_checks: dict[str, list[int]] = {}
    for minor_name, (selected_rows, selected_columns) in MINORS.items():
        matrix = [[rows[row][column] for column in selected_columns] for row in selected_rows]
        polynomial = determinant_sparse(matrix)
        dense_checks[minor_name] = verify_dense_control(
            field, polynomial, matrix, (0, 1, 2)
        )
        minors[minor_name] = polynomial
        records[minor_name] = polynomial_record(polynomial)
    identity_minor = record["identity_minor"]
    if identity_minor is not None:
        identity_value = sp.cancel(record["identity"].subs(p, field.ext))
        expected = sp.Poly(identity_value * Coff**2, Coff, domain=field)
        if minors[identity_minor] != expected:
            raise AssertionError(
                (name, identity_minor, "direct C^2 identity mismatch", minors[identity_minor].as_expr(), expected.as_expr())
            )
        other = "D2" if identity_minor == "D0" else "D0"
        if not minors[other].is_zero:
            raise AssertionError((name, other, "companion detector is not zero"))
        identity_check = {
            "minor": identity_minor,
            "exact_identity": str(expected.as_expr()),
            "coefficient_unit": True,
            "forces_C_zero_when_B_zero": True,
        }
    else:
        identity_check = {
            "minor": None,
            "exact_identity": None,
            "coefficient_unit": None,
            "forces_C_zero_when_B_zero": None,
        }
    return {
        "geometry": geometry,
        "q": str(q_value),
        "a": str(a_expression.subs(p, field.ext)),
        "minors": records,
        "direct_detector_identity": identity_check,
        "sparse_vs_permutation_at_C_values": dense_checks,
        "sparse_vs_permutation_at_three_exact_C_values": True,
        "status": "exact_sparse_fibre_replay",
    }


def main() -> int:
    started = time.monotonic()
    if support_digest() != EXPECTED_SUPPORT_DIGEST:
        raise SystemExit("copied GLD71 support digest mismatch")
    # This is deliberately part of the default path.  Any changed sparse
    # relation, quotient normalization, resultant, content, or factor support
    # raises before a PASS line can be emitted.
    branch_q_consistency = branch_q_consistency_report()
    pair_bridge = generic_pair_resultant_bridge()
    cover = cover_report(pair_bridge_verified=True)
    branch_reports: dict[str, object] = {}
    gaps: list[str] = [
        "The exact pair-resultant bridge is a necessary projection and does not by itself prove the finite cover or the GLD100 theorem; its H2 localization requires the separate GLD99 handoff.",
        "The GLD75/GLD86 incidence bridge, GLD96 E31 B=0 implication, and GLD95 F88 endpoint are mathematical upstream dependencies.",
    ]
    for name, record in BRANCHES.items():
        print(f"[gld100-audit] {name} direct geometry", file=sys.stderr, flush=True)
        # Every retained branch gets the common-a gamma replay on the default
        # and only successful path.  Q_other has no fixed-a direct detector;
        # its independently derived q-gcd plus the gamma gcd is the exact
        # emptiness check retained for that branch.
        gamma_report = gamma_branch(name, record)
        if name == "Q_other":
            branch_reports[name] = {"gamma": gamma_report}
        else:
            branch_reports[name] = {
                "direct": direct_branch(name, record),
                "gamma": gamma_report,
            }
    output = {
        "status": "independent_exact_scoped_fibre_audit",
        "gld_identifier": "GLD100",
        "global_conjecture": "UNRESOLVED",
        "scope": (
            "normalized GLD88/F88 H4 Q6 offset chart at B=0, with exact "
            "number-field checks on Q_gamma, Q_other, A4, and C4 fibres"
        ),
        "physical_open": "Omega is retained; this audit does not remove the physical incidence gate.",
        "provenance": {
            "support_rows": list(SUPPORT_ROWS),
            "support_digest_sha256": support_digest(),
            "minor_selections": {
                name: {"rows": list(rows), "columns": list(columns)}
                for name, (rows, columns) in MINORS.items()
            },
            "construction": (
                "copied GLD71 supports and GLD88/F88 formulas; generic sparse "
                "determinants over QQ(p,q,a), exact Q(p,a)[q]/(Q6) reduction, "
                "three a-resultants and literal-Q6 q-resultants; direct sparse "
                "determinants over QQ<r>; dense permutation cross-check at the "
                "three exact values C=0,1,2"
            ),
            "forbidden_imports": ["primary verifier", "GLD96", "GLD99", "exploratory runs"],
        },
        "pair_resultant_cover": cover,
        "generic_pair_resultant_bridge": pair_bridge,
        "projection_to_branch_q_consistency": branch_q_consistency,
        "upstream_GLD99": UPSTREAM_GLD99,
        "branches": branch_reports,
        "gaps": gaps,
        "nonclaims": [
            "No GLD100 theorem or global Krenn--Gu conclusion is claimed.",
            "No GLD99 result is reproduced or claimed; its owner hash is recorded only as the H2 handoff identifier.",
            "The exact pair-resultant/content/radical computation is a necessary projection and finite-support certificate only; it is not by itself the mathematical finite-cover implication or a GLD100 proof.",
            "Q6 reduction uses the monic localization at H2 and explicitly retains H2 and degree-drop loci; no leading-coefficient root is silently discarded.",
            "The direct D0/D2 identities are necessary rank-minor equations on the exact B=0 fibres; they do not prove B=0 or generate the full rank ideal.",
            "No statement is made for E31=0, Delta=0, other H4 charts, arbitrary H4 points outside F88, Omega removal, source integrability, or global gluing.",
        ],
        "runtime": {
            "seconds": round(time.monotonic() - started, 3),
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True, default=str))
    print(
        "GLD100 independent exact audit: PASS (scoped leaf computational audit; global Krenn--Gu remains UNRESOLVED and no global proof is claimed)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
