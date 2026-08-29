#!/usr/bin/env python3
"""Exploratory fibre census for the GLD97 six-minor offset ideal.

This file is deliberately an exploratory instrument, not a theorem or an
exhaustive computation.  It fixes rational ``(p,a)`` values over ``QQ`` or
finite-field values ``(characteristic,p,a)`` and measures the ideal generated
by ``Q6`` and the six GLD97 seven-minors in the two offset variables ``B,C``.
The generic ``QQ(p,a)`` Groebner computation is intentionally absent: each
sample is a small fixed-fibre calculation in ``B,C,q``.

The sparse relation supports below are copied verbatim from the committed
GLD71 verifier
``verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py``
(rows used by the GLD97 six minors).  The H4/F88 rational coordinates are a
local transcription of the committed GLD88 verifier, and ``Q6`` plus the
six row/column selections are transcribed from the committed GLD97 theorem
and verifier.  These provenance links are inputs to this census; this script
does not import any verifier, builder, GLD97 audit, or exploratory script.

Every output is marked ``exploratory`` and ``UNRESOLVED``.  A regular sample
means only that the displayed finite-fibre algebra calculation found the
reported membership; it is not evidence for arbitrary ``p``, arbitrary
characteristic, a chart cover, or the global Krenn--Gu conjecture.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ


B, C, q = sp.symbols("B C q")
VARIABLES = (B, C, q)
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)


# These are the exact GLD71 sparse annihilator supports used by the six
# GLD97 seven-minors.  They are copied rather than imported so the census is
# reproducible without loading a primary verifier.  Each support item is
# ((root, leaf_1, leaf_2, leaf_3), coefficient).
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


# GLD97's four bordered minors and two direct rank-seven detectors.  All
# indices are zero-based in the 37-by-9 GLD71 syndrome matrix.
MINORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}
# The committed GLD97 raw-support ledger bounds every one of these six
# determinants by total degree 3 in the two offsets (B,C).  A fixed fibre may
# cancel a leading term or make a determinant zero; outputs therefore report
# both this declared support degree and the actual specialized degree.
DECLARED_RAW_BC_DEGREE = {name: 3 for name in MINORS}
PIVOT_ROWS = (0, 1, 2, 17, 25, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)

EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)


# The default census intentionally mixes regular and boundary/control
# samples.  ``Q_p0_a0`` and ``Q_p1_a0`` expose Q6/Delta overlaps; the F7
# sample exposes a characteristic gate failure.  More samples can be passed
# with ``--sample rational:p:a`` or ``--sample finite:ell:p:a``.
DEFAULT_SAMPLES = (
    {"id": "Q_p0_a0", "kind": "rational", "p": "0", "a": "0"},
    {"id": "Q_p1_a0", "kind": "rational", "p": "1", "a": "0"},
    {"id": "Q_p2_a0", "kind": "rational", "p": "2", "a": "0"},
    {"id": "Q_p3_a1", "kind": "rational", "p": "3", "a": "1"},
    {"id": "F11_p2_a0", "kind": "finite_field", "characteristic": 11, "p": 2, "a": 0},
    {"id": "F7_p3_a2", "kind": "finite_field", "characteristic": 7, "p": 3, "a": 2},
)


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


def h4_family(p: sp.Expr, q_value: sp.Expr, a_value: sp.Expr) -> dict[str, sp.Expr]:
    """Local transcription of the committed GLD88 F88 coordinates."""

    d0 = p + q_value - 1
    e = 2 * p * q_value**2 - 2 * p * q_value - p - q_value**2 - 2 * q_value + 2
    nb = (
        -2 * a_value * p**2 * q_value**3
        + 3 * a_value * p**2 * q_value**2
        - 3 * a_value * p**2 * q_value
        + a_value * p**2
        + 2 * a_value * p * q_value**3
        + 2 * a_value * p
        + a_value * q_value**3
        - 3 * a_value * q_value**2
        + 3 * a_value * q_value
        - 2 * a_value
        + p**3 * q_value**2
        - p**3
        + p**2 * q_value**3
        - 3 * p**2 * q_value**2
        + p**2
        - 2 * p * q_value**3
        + 3 * p * q_value**2
        - 2 * p
        + q_value**2
        - 3 * q_value
        + 2
    )
    nc = (
        2 * a_value * p * q_value**3
        - 3 * a_value * p * q_value**2
        + 3 * a_value * p * q_value
        - a_value * p
        - a_value * q_value**3
        + 3 * a_value * q_value**2
        - 3 * a_value * q_value
        + 2 * a_value
        + p**2 * q_value**2
        - 2 * p**2 * q_value
        - 3 * p * q_value**2
        + p * q_value
        + p
        - q_value**2
        + 3 * q_value
        - 2
    )
    return {
        "s": sp.cancel((p + q_value - p * q_value) / d0),
        "b": sp.cancel(-nb / ((p**2 - p + 1) * e)),
        "c": sp.cancel(-nc / (d0 * e)),
        "d0": d0,
        "P": p**2 - p + 1,
        "e": e,
    }


def q6_polynomial(p: sp.Expr, q_value: sp.Expr) -> sp.Expr:
    """The committed GLD96/GLD97 Q6 formula."""

    return (
        2 * p**4 * q_value**2
        - 2 * p**4 * q_value
        + p**4
        + 2 * p**3 * q_value**3
        - 7 * p**3 * q_value**2
        + 5 * p**3 * q_value
        - 2 * p**3
        + 2 * p**2 * q_value**4
        - 7 * p**2 * q_value**3
        + 12 * p**2 * q_value**2
        - 7 * p**2 * q_value
        + 2 * p**2
        - 2 * p * q_value**4
        + 5 * p * q_value**3
        - 7 * p * q_value**2
        + 2 * p * q_value
        + q_value**4
        - 2 * q_value**3
        + 2 * q_value**2
    )


def chart_factors(p: sp.Expr) -> dict[str, sp.Expr]:
    """Return the GLD88/GLD95 chart factors used by the Delta gate."""

    d0 = p + q - 1
    P = p**2 - p + 1
    L1 = p**2 + 2 * p * q - 2 * p - q
    L2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    return {
        "p_minus_q": p - q,
        "d0": d0,
        "P": P,
        "L1": L1,
        "L2": L2,
        "e": e,
    }


class QuotientAlgebra:
    """Small exact model of K[q]/(Q6), with K=QQ or GF(ell)."""

    def __init__(self, q6_expression: sp.Expr, characteristic: int | None) -> None:
        self.characteristic = characteristic
        self.q6_poly = q_poly(q6_expression, characteristic)
        if self.q6_poly.is_zero:
            raise ValueError("Q6 is zero in the selected coefficient field")
        self.degree = int(self.q6_poly.degree())
        if self.degree == 0:
            raise ValueError("Q6 is a unit in the selected coefficient field")
        self.zero = tuple(self._coefficient(0) for _ in range(self.degree))
        self.one = tuple(
            [self._coefficient(1)]
            + [self._coefficient(0) for _ in range(self.degree - 1)]
        )
        leading = self._coefficient(self.q6_poly.LC())
        inverse_leading = self._inverse_scalar(leading)
        self.relation = tuple(
            self._neg(self._mul_scalar(self._coefficient(self.q6_poly.nth(i)), inverse_leading))
            for i in range(self.degree)
        )

    def _coefficient(self, value: sp.Expr | int) -> sp.Expr | int:
        if self.characteristic is None:
            return sp.Rational(value)
        rational = sp.Rational(value)
        numerator = int(rational.p) % self.characteristic
        denominator = int(rational.q) % self.characteristic
        return numerator * pow(denominator, -1, self.characteristic) % self.characteristic

    def _add_scalar(self, left: sp.Expr | int, right: sp.Expr | int) -> sp.Expr | int:
        value = left + right
        return self._coefficient(value)

    def _neg(self, value: sp.Expr | int) -> sp.Expr | int:
        return self._coefficient(-value)

    def _mul_scalar(self, left: sp.Expr | int, right: sp.Expr | int) -> sp.Expr | int:
        return self._coefficient(left * right)

    def _inverse_scalar(self, value: sp.Expr | int) -> sp.Expr | int:
        if self.characteristic is None:
            return sp.Rational(1, 1) / value
        return pow(int(value) % self.characteristic, -1, self.characteristic)

    def add(self, left: tuple, right: tuple) -> tuple:
        return tuple(self._add_scalar(a, b) for a, b in zip(left, right, strict=True))

    def neg(self, value: tuple) -> tuple:
        return tuple(self._neg(item) for item in value)

    def sub(self, left: tuple, right: tuple) -> tuple:
        return self.add(left, self.neg(right))

    def mul(self, left: tuple, right: tuple) -> tuple:
        raw = [self._coefficient(0) for _ in range(2 * self.degree - 1)]
        for left_index, left_value in enumerate(left):
            for right_index, right_value in enumerate(right):
                raw[left_index + right_index] = self._add_scalar(
                    raw[left_index + right_index],
                    self._mul_scalar(left_value, right_value),
                )
        for index in range(2 * self.degree - 2, self.degree - 1, -1):
            coefficient = raw[index]
            if coefficient == 0:
                continue
            for relation_index, relation_value in enumerate(self.relation):
                raw[index - self.degree + relation_index] = self._add_scalar(
                    raw[index - self.degree + relation_index],
                    self._mul_scalar(coefficient, relation_value),
                )
        return tuple(raw[: self.degree])

    def from_expr(self, expression: sp.Expr) -> tuple:
        polynomial = q_poly(expression, self.characteristic)
        remainder = polynomial.rem(self.q6_poly)
        return tuple(self._coefficient(remainder.nth(index)) for index in range(self.degree))

    def to_expr(self, value: tuple) -> sp.Expr:
        return sp.expand(sum(coefficient * q**index for index, coefficient in enumerate(value)))

    def inverse(self, value: tuple) -> tuple:
        expression = self.to_expr(value)
        polynomial = q_poly(expression, self.characteristic)
        inverse = sp.invert(polynomial, self.q6_poly)
        return self.from_expr(inverse.as_expr())

    def rational(self, expression: sp.Expr) -> tuple:
        numerator, denominator = sp.cancel(expression).as_numer_denom()
        return self.mul(self.from_expr(numerator), self.inverse(self.from_expr(denominator)))


class BCPolynomial:
    """Sparse polynomial in B,C with coefficients in QuotientAlgebra."""

    def __init__(self, algebra: QuotientAlgebra, terms: dict[tuple[int, int], tuple] | None = None) -> None:
        self.algebra = algebra
        self.terms: dict[tuple[int, int], tuple] = {}
        for exponent, coefficient in (terms or {}).items():
            if coefficient != algebra.zero:
                self.terms[exponent] = coefficient

    @classmethod
    def constant(cls, algebra: QuotientAlgebra, expression: sp.Expr | tuple) -> "BCPolynomial":
        value = expression if isinstance(expression, tuple) else algebra.from_expr(expression)
        return cls(algebra, {(0, 0): value})

    @classmethod
    def variable(cls, algebra: QuotientAlgebra, exponent: tuple[int, int]) -> "BCPolynomial":
        return cls(algebra, {exponent: algebra.one})

    def __add__(self, other: "BCPolynomial") -> "BCPolynomial":
        terms = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            terms[exponent] = self.algebra.add(terms.get(exponent, self.algebra.zero), coefficient)
            if terms[exponent] == self.algebra.zero:
                terms.pop(exponent)
        return BCPolynomial(self.algebra, terms)

    def __neg__(self) -> "BCPolynomial":
        return BCPolynomial(self.algebra, {
            exponent: self.algebra.neg(coefficient)
            for exponent, coefficient in self.terms.items()
        })

    def __sub__(self, other: "BCPolynomial") -> "BCPolynomial":
        return self + (-other)

    def __mul__(self, other: "BCPolynomial") -> "BCPolynomial":
        terms: dict[tuple[int, int], tuple] = {}
        for (left_b, left_c), left_value in self.terms.items():
            for (right_b, right_c), right_value in other.terms.items():
                exponent = (left_b + right_b, left_c + right_c)
                product = self.algebra.mul(left_value, right_value)
                terms[exponent] = self.algebra.add(
                    terms.get(exponent, self.algebra.zero), product
                )
        return BCPolynomial(self.algebra, terms)

    def to_expr(self) -> sp.Expr:
        expression = 0
        for (b_degree, c_degree), coefficient in sorted(self.terms.items()):
            expression += self.algebra.to_expr(coefficient) * B**b_degree * C**c_degree
        return sp.expand(expression)


def bc_polynomial_stats(polynomial: BCPolynomial) -> dict[str, object]:
    """Describe the specialized total degree/support in B,C over A."""

    if not polynomial.terms:
        return {
            "zero": True,
            "bc_total_degree": None,
            "bc_degrees": {"B": None, "C": None},
            "bc_support_terms": 0,
            "q_coefficient_support_terms": 0,
        }
    return {
        "zero": False,
        "bc_total_degree": max(sum(exponent) for exponent in polynomial.terms),
        "bc_degrees": {
            "B": max(exponent[0] for exponent in polynomial.terms),
            "C": max(exponent[1] for exponent in polynomial.terms),
        },
        "bc_support_terms": len(polynomial.terms),
        "q_coefficient_support_terms": sum(
            sum(value != polynomial.algebra.zero[0] for value in coefficient)
            for coefficient in polynomial.terms.values()
        ),
    }


def direct_rows_in_algebra(
    leaf: list[list[BCPolynomial]],
    rows: tuple[int, ...],
    algebra: QuotientAlgebra,
) -> dict[int, list[BCPolynomial]]:
    """Accumulate selected rows while reducing q modulo Q6 after each product."""

    zero = BCPolynomial.constant(algebra, algebra.zero)
    result: dict[int, list[BCPolynomial]] = {}
    for relation_row in rows:
        entries = []
        for root in range(3):
            for component in range(3):
                total = zero
                for indices, coefficient in PINNED_RELATIONS[relation_row]:
                    if indices[0] != root:
                        continue
                    term = (
                        leaf[indices[1]][component]
                        * leaf[indices[2]][component]
                        * leaf[indices[3]][component]
                    )
                    total = total + BCPolynomial.constant(algebra, algebra.from_expr(coefficient)) * term
                entries.append(total)
        result[relation_row] = entries
    return result


def determinant_in_algebra(matrix: list[list[BCPolynomial]]) -> BCPolynomial:
    """Compute a small determinant by subset dynamic programming."""

    size = len(matrix)
    algebra = matrix[0][0].algebra
    zero = BCPolynomial.constant(algebra, algebra.zero)
    one = BCPolynomial.constant(algebra, algebra.one)
    states: dict[int, BCPolynomial] = {0: one}
    for row_index in range(size):
        next_states: dict[int, BCPolynomial] = {}
        for mask, value in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                available_before = sum(
                    1 for previous in range(column) if not (mask & (1 << previous))
                )
                term = value * matrix[row_index][column]
                if available_before % 2:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = next_states.get(new_mask, zero) + term
        states = next_states
    return states.get((1 << size) - 1, zero)


def leaf_in_algebra(
    p: sp.Expr,
    a_value: sp.Expr,
    family: dict[str, sp.Expr],
    algebra: QuotientAlgebra,
) -> list[list[BCPolynomial]]:
    one = BCPolynomial.constant(algebra, 1)
    leaf = [
        [one, one, one],
        [BCPolynomial.constant(algebra, p), BCPolynomial.variable(algebra, (0, 0)), one],
        [BCPolynomial.constant(algebra, a_value), one, one],
    ]
    leaf[1][1] = BCPolynomial.constant(algebra, q)
    leaf[1][2] = BCPolynomial.constant(algebra, algebra.rational(family["s"]))
    b_value = BCPolynomial.constant(
        algebra, algebra.add(algebra.one, algebra.rational(family["b"]))
    )
    c_value = BCPolynomial.constant(
        algebra, algebra.add(algebra.one, algebra.rational(family["c"]))
    )
    leaf[2][1] = b_value + BCPolynomial.variable(algebra, (1, 0))
    leaf[2][2] = c_value + BCPolynomial.variable(algebra, (0, 1))
    return leaf


def parse_rational(text: str) -> sp.Rational:
    value = sp.Rational(text)
    if not value.is_Rational:
        raise ValueError(f"not rational: {text}")
    return value


def parse_sample_spec(spec: str) -> dict[str, object]:
    pieces = spec.split(":")
    if pieces[0] == "rational" and len(pieces) == 3:
        parse_rational(pieces[1])
        parse_rational(pieces[2])
        return {"id": f"Q_p{pieces[1]}_a{pieces[2]}", "kind": "rational", "p": pieces[1], "a": pieces[2]}
    if pieces[0] == "finite" and len(pieces) == 4:
        characteristic = int(pieces[1])
        p_value = int(pieces[2])
        a_value = int(pieces[3])
        if characteristic <= 1 or not sp.isprime(characteristic):
            raise ValueError(f"finite sample characteristic must be prime: {characteristic}")
        return {
            "id": f"F{characteristic}_p{p_value % characteristic}_a{a_value % characteristic}",
            "kind": "finite_field",
            "characteristic": characteristic,
            "p": p_value % characteristic,
            "a": a_value % characteristic,
        }
    raise ValueError(f"sample must be rational:p:a or finite:ell:p:a, got {spec!r}")


def sample_values(sample: dict[str, object]) -> tuple[sp.Expr, sp.Expr, int | None]:
    if sample["kind"] == "rational":
        return parse_rational(str(sample["p"])), parse_rational(str(sample["a"])), None
    characteristic = int(sample["characteristic"])
    return sp.Integer(int(sample["p"]) % characteristic), sp.Integer(int(sample["a"]) % characteristic), characteristic


def field_poly(expression: sp.Expr, variables: tuple[sp.Symbol, ...], characteristic: int | None) -> sp.Poly:
    if characteristic is None:
        return sp.Poly(expression, *variables, domain=QQ)
    # Poly(..., modulus=ell) performs the coefficient reduction and rejects a
    # rational coefficient whose denominator is zero in the selected field.
    return sp.Poly(expression, *variables, modulus=characteristic)


def q_poly(expression: sp.Expr, characteristic: int | None) -> sp.Poly:
    return field_poly(expression, (q,), characteristic)


def polynomial_stats(expression: sp.Expr, characteristic: int | None) -> dict[str, object]:
    polynomial = field_poly(expression, VARIABLES, characteristic)
    if polynomial.is_zero:
        return {"zero": True, "total_degree": None, "degrees": {}, "support_terms": 0}
    return {
        "zero": False,
        "total_degree": int(polynomial.total_degree()),
        "degrees": {
            variable.name: int(polynomial.degree(variable)) for variable in VARIABLES
        },
        "support_terms": len(polynomial.terms()),
    }


def univariate_stats(expression: sp.Expr, characteristic: int | None) -> dict[str, object]:
    polynomial = q_poly(expression, characteristic)
    if polynomial.is_zero:
        return {"zero": True, "degree": None, "support_terms": 0, "leading_coefficient": "0"}
    return {
        "zero": False,
        "degree": int(polynomial.degree()),
        "support_terms": len(polynomial.terms()),
        "leading_coefficient": str(polynomial.LC()),
    }


def factor_gate_report(
    p: sp.Expr,
    q6_expression: sp.Expr,
    denominator_bounds: dict[str, sp.Expr],
    characteristic: int | None,
) -> dict[str, object]:
    """Check chart factors and declared determinant denominator bounds."""

    q6_poly = q_poly(q6_expression, characteristic)
    q6_zero = q6_poly.is_zero
    q6_degree = None if q6_zero else int(q6_poly.degree())
    factor_data: dict[str, object] = {}
    denominator_data: dict[str, object] = {}
    hard_failures: list[str] = []
    soft_failures: list[str] = []

    for name, factor in chart_factors(p).items():
        factor_poly = q_poly(factor, characteristic)
        zero = factor_poly.is_zero
        gcd_expression = "0" if q6_zero else str(sp.factor(sp.gcd(q6_poly, factor_poly).as_expr()))
        overlap = False if q6_zero or zero else sp.gcd(q6_poly, factor_poly).degree() > 0
        factor_data[name] = {
            "expression": str(sp.factor(factor)),
            "reduced_expression": str(factor_poly.as_expr()),
            "zero_polynomial": zero,
            "gcd_with_Q6": gcd_expression,
            "Q6_overlap": bool(overlap),
        }
        if zero:
            hard_failures.append(f"chart_factor_zero:{name}")
        elif overlap:
            soft_failures.append(f"Q6_overlaps_chart_factor:{name}:{gcd_expression}")

    for name, denominator in denominator_bounds.items():
        if denominator.free_symbols - {q}:
            hard_failures.append(f"denominator_has_displayed_variable:{name}")
        denominator_poly = q_poly(denominator, characteristic)
        zero = denominator_poly.is_zero
        gcd_expression = "0" if q6_zero else str(sp.factor(sp.gcd(q6_poly, denominator_poly).as_expr()))
        overlap = False if q6_zero or zero else sp.gcd(q6_poly, denominator_poly).degree() > 0
        denominator_data[name] = {
            "expression": str(sp.factor(denominator)),
            "reduced_expression": str(denominator_poly.as_expr()),
            "zero_polynomial": zero,
            "gcd_with_Q6": gcd_expression,
            "Q6_overlap": bool(overlap),
        }
        if zero:
            hard_failures.append(f"denominator_bound_zero:{name}")
        elif overlap:
            soft_failures.append(f"Q6_overlaps_denominator_bound:{name}:{gcd_expression}")

    if q6_zero:
        hard_failures.append("Q6_zero_polynomial")
    elif characteristic is not None and q6_degree != 4:
        soft_failures.append(f"Q6_degree_drop:{q6_degree}")

    delta_expression = sp.prod(chart_factors(p).values())
    delta_poly = q_poly(delta_expression, characteristic)
    if not q6_zero and q6_degree and q6_degree > 0:
        delta_remainder = delta_poly.rem(q6_poly)
    else:
        delta_remainder = delta_poly
    return {
        "Q6": univariate_stats(q6_expression, characteristic),
        "Q6_algebra_dimension": q6_degree,
        "Q6_algebra": (
            ("GF(%d)[q]/(Q6)" % characteristic)
            if characteristic is not None
            else "QQ[q]/(Q6)"
        ),
        "Delta_expression": str(sp.factor(delta_expression)),
        "Delta_remainder_mod_Q6": str(delta_remainder.as_expr()),
        "chart_factors": factor_data,
        "denominator_bounds": denominator_data,
        "hard_failures": hard_failures,
        "soft_failures": soft_failures,
        "regular_chart_gate": not hard_failures and not soft_failures,
    }


def rank_mod(rows: list[list[int]], characteristic: int) -> int:
    """Small exact row rank over GF(characteristic)."""

    if not rows:
        return 0
    matrix = [[int(value) % characteristic for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if matrix[row][column] % characteristic),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % characteristic, -1, characteristic)
        matrix[rank] = [value * inverse % characteristic for value in matrix[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            multiple = matrix[row][column] % characteristic
            if multiple:
                matrix[row] = [
                    (left - multiple * right) % characteristic
                    for left, right in zip(matrix[row], matrix[rank], strict=True)
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def field_rank(rows: list[list[sp.Expr | int]], characteristic: int | None) -> int:
    if characteristic is None:
        return rank_qq(rows)
    return rank_mod([[int(value) for value in row] for row in rows], characteristic)


def rank_qq(rows: list[list[sp.Expr | int]]) -> int:
    """Small exact rational row rank without SymPy's expression-level rref."""

    if not rows:
        return 0
    matrix = []
    for row in rows:
        converted = []
        for value in row:
            rational = sp.Rational(value)
            converted.append(Fraction(int(rational.p), int(rational.q)))
        matrix.append(converted)
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for row in range(rank + 1, row_count):
            value = matrix[row][column]
            if not value:
                continue
            multiplier = value / pivot_value
            for index in range(column, column_count):
                matrix[row][index] -= multiplier * matrix[rank][index]
        rank += 1
        if rank == row_count:
            break
    return rank


def bc_exponents(max_degree: int) -> list[tuple[int, int]]:
    return [
        (b_degree, total_degree - b_degree)
        for total_degree in range(max_degree + 1)
        for b_degree in range(total_degree + 1)
    ]


def expression_to_bc(
    expression: sp.Expr,
    algebra: QuotientAlgebra,
    characteristic: int | None,
) -> BCPolynomial:
    """Parse an already q-reduced expression as a B,C polynomial over A."""

    polynomial = field_poly(expression, VARIABLES, characteristic)
    terms: dict[tuple[int, int], tuple] = {}
    for (b_degree, c_degree, q_degree), coefficient in polynomial.terms():
        if q_degree >= algebra.degree:
            raise AssertionError("expression was not reduced in q")
        vector = list(algebra.zero)
        vector[q_degree] = algebra._coefficient(coefficient)
        exponent = (b_degree, c_degree)
        terms[exponent] = algebra.add(
            terms.get(exponent, algebra.zero), tuple(vector)
        )
    return BCPolynomial(algebra, terms)


def shift_bc(polynomial: BCPolynomial, multiplier: tuple[int, int]) -> BCPolynomial:
    b_shift, c_shift = multiplier
    return BCPolynomial(
        polynomial.algebra,
        {
            (b_degree + b_shift, c_degree + c_shift): coefficient
            for (b_degree, c_degree), coefficient in polynomial.terms.items()
        },
    )


def bc_row(
    polynomial: BCPolynomial,
    degree: int,
    algebra: QuotientAlgebra,
) -> list[sp.Expr | int]:
    columns = [(b, c, q_degree) for b, c in bc_exponents(degree) for q_degree in range(algebra.degree)]
    positions = {column: index for index, column in enumerate(columns)}
    row: list[sp.Expr | int] = [0] * len(columns)
    for (b_degree, c_degree), coefficient in polynomial.terms.items():
        for q_degree, scalar in enumerate(coefficient):
            row[positions[(b_degree, c_degree, q_degree)]] = scalar
    return row


def target_bc_row(
    target: sp.Symbol,
    degree: int,
    algebra: QuotientAlgebra,
) -> list[int]:
    columns = [(b, c, q_degree) for b, c in bc_exponents(degree) for q_degree in range(algebra.degree)]
    positions = {column: index for index, column in enumerate(columns)}
    row = [0] * len(columns)
    target_exponent = (1, 0) if target == B else (0, 1)
    row[positions[(target_exponent[0], target_exponent[1], 0)]] = 1
    return row


def macaulay_membership_in_algebra(
    generators: list[sp.Expr],
    algebra: QuotientAlgebra,
    characteristic: int | None,
    max_degree: int,
) -> dict[str, object]:
    """Find B,C membership using K-linear Macaulay rows over A=K[q]/(Q6)."""

    bc_generators = [
        expression_to_bc(expression, algebra, characteristic)
        for expression in generators[1:]
    ]
    specialized_generator_degrees = {
        name: (
            max(sum(exponent) for exponent in polynomial.terms)
            if polynomial.terms
            else None
        )
        for name, polynomial in zip(MINORS, bc_generators, strict=True)
    }
    nonzero = [polynomial for polynomial in bc_generators if polynomial.terms]
    q_powers = [algebra.from_expr(q**index) for index in range(algebra.degree)]
    signatures = []
    minimal_degree = None
    for degree in range(1, max_degree + 1):
        rows: list[list[sp.Expr | int]] = []
        for generator in nonzero:
            generator_degree = max(sum(exponent) for exponent in generator.terms)
            if generator_degree > degree:
                continue
            for multiplier in bc_exponents(degree - generator_degree):
                shifted = shift_bc(generator, multiplier)
                for q_power in q_powers:
                    scaled = shifted * BCPolynomial.constant(algebra, q_power)
                    rows.append(bc_row(scaled, degree, algebra))
        base_rank = field_rank(rows, characteristic)
        b_rank = field_rank(
            rows + [target_bc_row(B, degree, algebra)], characteristic
        )
        c_rank = field_rank(
            rows + [target_bc_row(C, degree, algebra)], characteristic
        )
        signature = {
            "degree_BC": degree,
            "rows": len(rows),
            "columns": len(bc_exponents(degree)) * algebra.degree,
            "nonconstant_target_columns": (
                (len(bc_exponents(degree)) - 1) * algebra.degree
            ),
            "rank": base_rank,
            "rank_with_B": b_rank,
            "rank_with_C": c_rank,
            "B_in_span": b_rank == base_rank,
            "C_in_span": c_rank == base_rank,
        }
        signature["nonconstant_target_deficiency"] = (
            signature["nonconstant_target_columns"] - base_rank
        )
        signature["nonconstant_target_surjective"] = (
            signature["nonconstant_target_deficiency"] == 0
        )
        signatures.append(signature)
        if (
            minimal_degree is None
            and signature["B_in_span"]
            and signature["C_in_span"]
        ):
            minimal_degree = degree
    return {
        "status": "found" if minimal_degree is not None else "not_found_within_cap",
        "minimal_degree_BC": minimal_degree,
        "tested_to": max_degree,
        "coefficient_algebra_dimension": algebra.degree,
        "declared_raw_support_bc_total_degrees": dict(DECLARED_RAW_BC_DEGREE),
        "specialized_generator_bc_degrees": specialized_generator_degrees,
        "rank_signature": signatures,
    }


def basis_summary(
    generators: list[sp.Expr],
    algebra: QuotientAlgebra,
    characteristic: int | None,
    macaulay_max_degree: int,
) -> dict[str, object]:
    """Report a certificate-backed [Q6,B,C] candidate without Groebner blowup."""

    nonzero = [
        field_poly(expression, VARIABLES, characteristic)
        for expression in generators
        if not field_poly(expression, VARIABLES, characteristic).is_zero
    ]
    macaulay = macaulay_membership_in_algebra(
        generators, algebra, characteristic, macaulay_max_degree
    )
    b_member = macaulay["status"] == "found" and all(
        signature["B_in_span"] for signature in macaulay["rank_signature"][-1:]
    )
    c_member = macaulay["status"] == "found" and all(
        signature["C_in_span"] for signature in macaulay["rank_signature"][-1:]
    )
    constant_terms = {}
    constants_zero = True
    generator_bc_stats = {}
    for index, expression in enumerate(generators[1:]):
        polynomial = expression_to_bc(expression, algebra, characteristic)
        name = tuple(MINORS)[index]
        generator_bc_stats[name] = {
            **bc_polynomial_stats(polynomial),
            "declared_raw_support_bc_total_degree": DECLARED_RAW_BC_DEGREE[name],
        }
        constant = polynomial.terms.get((0, 0), algebra.zero)
        zero = constant == algebra.zero
        constant_terms[f"minor_{index}"] = {
            "zero_in_A": zero,
            "expression": str(algebra.to_expr(constant)),
        }
        constants_zero = constants_zero and zero

    basis = []
    basis_status = "not_certified"
    if b_member and c_member and constants_zero:
        q6_monic = algebra.q6_poly.monic().as_expr()
        basis = [
            {
                "polynomial": str(q6_monic),
                "leading_monomial": [0, 0, algebra.degree],
                "total_degree": algebra.degree,
                "support_terms": len(algebra.q6_poly.monic().terms()),
            },
            {"polynomial": "B", "leading_monomial": [1, 0, 0], "total_degree": 1, "support_terms": 1},
            {"polynomial": "C", "leading_monomial": [0, 1, 0], "total_degree": 1, "support_terms": 1},
        ]
        basis_status = "exact_fixed_fibre_equality_from_A_membership_and_zero_constants"
    return {
        "input_nonzero_count": len(nonzero),
        "basis": basis,
        "basis_size": len(basis),
        "basis_status": basis_status,
        "B_membership": bool(b_member),
        "C_membership": bool(c_member),
        "B_remainder": "0 (A-Macaulay membership)" if b_member else "not certified",
        "C_remainder": "0 (A-Macaulay membership)" if c_member else "not certified",
        "generator_constant_terms": constant_terms,
        "generator_bc_stats": generator_bc_stats,
        "unit_ideal": False,
        "macaulay": macaulay,
    }


def run_sample(
    sample: dict[str, object], macaulay_max_degree: int, progress: bool = False
) -> dict[str, object]:
    started = time.monotonic()
    if progress:
        print(f"[{sample['id']}] start", file=sys.stderr, flush=True)
    p, a_value, characteristic = sample_values(sample)
    q6_expression = sp.expand(q6_polynomial(p, q))
    family = h4_family(p, q, a_value)
    leaf_denominator = sp.cancel(family["d0"] * family["P"] * family["e"])
    if leaf_denominator == 0:
        raise AssertionError("zero common F88 leaf denominator")
    # Each syndrome entry is a product of three leaf coordinates and each
    # displayed determinant has seven entries per term.  This is a declared
    # denominator bound, not a claim that it is the reduced raw denominator.
    determinant_denominator_bound = sp.cancel(leaf_denominator**21)
    denominator_bounds = {name: determinant_denominator_bound for name in MINORS}
    gate = factor_gate_report(
        p, q6_expression, denominator_bounds, characteristic
    )
    hard_gate = list(gate["hard_failures"])
    soft_gate = list(gate["soft_failures"])
    result: dict[str, object] = {
        "id": sample["id"],
        "kind": sample["kind"],
        "p": str(p),
        "a": str(a_value),
        "characteristic": characteristic,
        "Q6": univariate_stats(q6_expression, characteristic),
        "chart": {
            "F88_denominators": {
                "s": str(sp.factor(family["d0"])),
                "b88": str(sp.factor(family["P"] * family["e"])),
                "c88": str(sp.factor(family["d0"] * family["e"])),
            },
            "determinant_denominator_bound": str(
                sp.factor(determinant_denominator_bound)
            ),
        },
        "provenance": {
            "support_rows": list(SUPPORT_ROWS),
            "support_digest_sha256": support_digest(),
            "minor_selections": {
                name: {"rows": list(rows), "columns": list(columns)}
                for name, (rows, columns) in MINORS.items()
            },
        },
    }

    # Detect characteristic-zero denominators that become zero modulo the
    # selected finite field before constructing a meaningless localized leaf.
    # A quotient-algebra determinant requires all chart factors to be units.
    # Overlap samples remain scientifically useful as controls, but are
    # reported and skipped rather than inverted through a non-unit.
    if hard_gate or soft_gate:
        result["gate"] = gate
        result["status"] = (
            "exceptional_gate_failure" if hard_gate else "exceptional_gate_overlap"
        )
        result["exceptional_reasons"] = hard_gate + soft_gate
        result["computation"] = "skipped_before_quotient_algebra"
        result["seconds"] = round(time.monotonic() - started, 3)
        return result

    required_rows = tuple(
        sorted({row for rows, _columns in MINORS.values() for row in rows} | set(PIVOT_ROWS))
    )
    algebra = QuotientAlgebra(q6_expression, characteristic)
    if progress:
        print(f"[{sample['id']}] quotient algebra ready", file=sys.stderr, flush=True)
    algebra_leaf = leaf_in_algebra(p, a_value, family, algebra)
    row_map = direct_rows_in_algebra(algebra_leaf, required_rows, algebra)
    if progress:
        print(f"[{sample['id']}] syndrome rows ready", file=sys.stderr, flush=True)
    reduced_minors: list[sp.Expr] = []
    minor_data: dict[str, object] = {}
    determinant_seconds: dict[str, float] = {}
    pivot_reduced = None
    pivot_reduced_in_algebra = None
    for name, (rows, columns) in [
        ("PIVOT", (PIVOT_ROWS, PIVOT_COLUMNS)),
        *MINORS.items(),
    ]:
        determinant_started = time.monotonic()
        matrix = [
            [row_map[row][column] for column in columns]
            for row in rows
        ]
        reduced_in_algebra = determinant_in_algebra(matrix)
        reduced = reduced_in_algebra.to_expr()
        determinant_seconds[name] = round(time.monotonic() - determinant_started, 3)
        if progress:
            print(
                f"[{sample['id']}] {name} determinant {determinant_seconds[name]}s",
                file=sys.stderr,
                flush=True,
            )
        if name == "PIVOT":
            pivot_reduced_in_algebra = reduced_in_algebra
            pivot_reduced = reduced
        else:
            reduced_minors.append(reduced)
            minor_data[name] = {
                "reduced_in_A": polynomial_stats(reduced, characteristic),
                "bc_support": bc_polynomial_stats(reduced_in_algebra),
                "declared_raw_support_bc_total_degree": DECLARED_RAW_BC_DEGREE[name],
                "reduction_status": "direct_quotient_algebra_determinant",
            }

    result["gate"] = gate
    result["determinant_seconds"] = determinant_seconds
    result["minor_polynomials"] = minor_data
    result["pivot_signature"] = {
        "rows": list(PIVOT_ROWS),
        "columns": list(PIVOT_COLUMNS),
        "reduced_in_A": polynomial_stats(pivot_reduced, characteristic),
        "bc_support": bc_polynomial_stats(pivot_reduced_in_algebra),
        "reduction_status": "direct_quotient_algebra_determinant",
    }

    generators = [q6_expression, *reduced_minors]
    if progress:
        print(f"[{sample['id']}] determinants ready; quotient membership", file=sys.stderr, flush=True)
    ideal = basis_summary(
        generators, algebra, characteristic, macaulay_max_degree
    )
    if progress:
        print(f"[{sample['id']}] quotient Macaulay rank ready", file=sys.stderr, flush=True)
    result["ideal"] = ideal
    exceptional_reasons = list(gate["hard_failures"]) + list(gate["soft_failures"])
    if characteristic is not None and result["Q6"]["degree"] != 4:
        exceptional_reasons.append(f"Q6_degree_not_four:{result['Q6']['degree']}")
    if not ideal["B_membership"]:
        exceptional_reasons.append("B_not_in_basis_ideal")
    if not ideal["C_membership"]:
        exceptional_reasons.append("C_not_in_basis_ideal")
    if ideal["macaulay"]["minimal_degree_BC"] is None:
        exceptional_reasons.append("B_C_Macaulay_degree_above_cap")
    result["status"] = "regular_membership" if not exceptional_reasons else "exceptional_or_gate_overlap"
    result["exceptional_reasons"] = exceptional_reasons
    result["computation"] = "exact_fixed_fibre_quotient_algebra_determinants_and_Macaulay_rank"
    result["seconds"] = round(time.monotonic() - started, 3)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample",
        action="append",
        help="sample spec rational:p:a or finite:ell:p:a (repeatable; replaces defaults)",
    )
    parser.add_argument("--max-samples", type=int, default=6)
    # D=4 is the first exact membership degree on the regular pilot fibres;
    # callers can raise the cap explicitly for a diagnostic non-membership run.
    parser.add_argument("--macaulay-max-degree", type=int, default=4)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args(argv)
    if support_digest() != EXPECTED_SUPPORT_DIGEST:
        raise SystemExit("pinned GLD71 support digest mismatch")
    if args.max_samples <= 0 or args.macaulay_max_degree <= 0:
        raise SystemExit("max-samples and macaulay-max-degree must be positive")

    samples = (
        [parse_sample_spec(spec) for spec in args.sample]
        if args.sample
        else list(DEFAULT_SAMPLES)
    )[: args.max_samples]
    started = time.monotonic()
    results = []
    for sample in samples:
        try:
            results.append(run_sample(sample, args.macaulay_max_degree, args.progress))
        except Exception as exc:  # exploratory census retains failed samples
            results.append(
                {
                    "id": sample["id"],
                    "kind": sample["kind"],
                    "p": str(sample["p"]),
                    "a": str(sample["a"]),
                    "characteristic": sample.get("characteristic"),
                    "status": "computation_error",
                    "exception_type": type(exc).__name__,
                    "exception": str(exc),
                    "seconds": round(time.monotonic() - started, 3),
                }
            )
    exceptional = [
        item["id"]
        for item in results
        if item.get("status") != "regular_membership"
    ]
    payload = {
        "status": "exploratory",
        "global_status": "UNRESOLVED",
        "experiment_id": "GLD98-membership-pilot",
        "scope": (
            "selected fixed rational or finite-field (p,a) fibres; six GLD97 "
            "seven-minors plus Q6, with explicit Delta/denominator diagnostics"
        ),
        "generic_QQ_p_a_Groebner": "not_attempted",
        "construction": "copied GLD71 supports; local GLD88 F88 and GLD96 Q6 formulas; direct sparse quotient-algebra determinants",
        "determinant_algorithm": "7x7 subset dynamic programming over K[q]/(Q6); no symbolic QQ(p,a) Groebner",
        "support_digest_sha256": support_digest(),
        "samples_requested": len(samples),
        "samples_completed": len(results),
        "exceptional_samples": exceptional,
        "samples": results,
        "runtime_seconds": round(time.monotonic() - started, 3),
        "runtime_environment": {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
            "script": str(Path(__file__).resolve()),
        },
        "nonclaims": [
            "This is not a theorem, proof, exhaustive p/a cover, or counterexample.",
            "Finite-field gate failures and Q6/Delta overlaps are reported, not silently localized away.",
            "A basis containing B,C is only a fixed-fibre algebra observation and does not globalize in p or characteristic.",
            "The script does not reprove the GLD75/GLD86 bridge, F88 endpoint, or any physical Omega gate.",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
