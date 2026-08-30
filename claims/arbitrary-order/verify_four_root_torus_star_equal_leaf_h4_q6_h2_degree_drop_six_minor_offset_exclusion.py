#!/usr/bin/env python3
"""Exact H2=0 six-minor offset replay for the normalized H4/Q6 chart.

This is a primary, characteristic-zero replay of the scoped GLD99 claim.  It
loads the committed GLD71 syndrome and GLD88 F88 family builders, splits
``H2=2*p**2-2*p+1`` over ``Q(i)``, and works in each surviving quadratic
quotient ``Q(i)[q]/(Q_+/-)``.  The six selected seven-minors are accumulated
exactly as sparse polynomials in the GLD88 offsets ``B,C``.  A 158 by 144
Macaulay coefficient system then supplies polynomial-in-``a`` certificates
for both ``B`` and ``C``.

The result is only the denominator-safe normalized offset-chart implication.
It is not a proof of arbitrary H4/Q6 coverage, the GLD83 Fitting pullback, or
the global Krenn--Gu conjecture.  All metadata therefore retain strict
``UNRESOLVED`` status.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import QQ_I
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)

p, q, a, b, c, B, C = sp.symbols("p q a b c B C", real=True)
I = sp.I
P_PLUS = (1 + I) / 2
P_MINUS = (1 - I) / 2

PIVOT_ROWS = (0, 1, 2, 17, 25, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
TARGETS = ((28, 8), (32, 2), (32, 5), (33, 8))
MINORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)

# These are hashes of the exact coefficient payloads in A_e[B,C], where the
# q-coordinate is stored in the ordered basis (1,q).  Plus and minus are
# intentionally pinned separately; a hash is never compared to its conjugate
# hash as though the strings themselves should agree.
EXPECTED_GENERATOR_HASHES: dict[int, dict[str, str]] = {
    1: {
        "T0": "c66046efa2e34a5cff341e5edb6deccc0fab008fd5fe4ff89f458abf5ebc2e4e",
        "T1": "106ebfdaf5c6aea5f4f5d844ad170d3be4be45dcb10a73cedd57721c1754d83f",
        "T2": "7e562e95ae2a740d76469338204cf942903d025c264c81987d5a7cc687c52adb",
        "T3": "f5576f4d76055fe5cea933ca4bd2fa9b2a4279a0f92155b8b5143fd60938019f",
        "D0": "463c8a46c7583204a8cbefa5fb0dae6c46af86105d45a5f2d27658e183ed9ace",
        "D2": "e311a0588bc91f96530de1799ee05a829fce5999ed246a3cfc3cea926ee9e936",
    },
    -1: {
        "T0": "aab9bf74f768c5e8aabadf988e7a795556a432a2c7b3b808eb4c08c71f6d8aa7",
        "T1": "8c3b58a67a46f3159c64fe42e2902a8eb973db07a869dc41a37136dbf5db935b",
        "T2": "68c0a116dfc57bbb4ac72c5750f3d821977cbd78b168ce27de2a116d1f43c06d",
        "T3": "0fd46d37b59d76b6a3224a1a15006a80fbc2e862e634ae6d8b7be29ea7229bbf",
        "D0": "af0791f41ea378e8045902b90ced9167af1551633cfe94fe8e62f50bc5c3b3f3",
        "D2": "856831444749d5b033247401445313384fc4789ab9184c97e19b13f130324445",
    },
}
EXPECTED_CERTIFICATE_HASHES: dict[int, dict[str, str]] = {
    1: {
        "B": "da5154181e031400a933d6ecb2e4b82dbaf6c3d9b7c11dc557cf20740546b9e3",
        "C": "e52ba0af1cc4c2b65a9849bebe6c8414f75eb64dbb42ae4879464d3ee3213e35",
    },
    -1: {
        "B": "837adda0446d760cc959890eef072b600fc93dc9ca3f2a837bbd256a8be82cf0",
        "C": "7143e9974307c5855ebe438433ffe0776cc187b05883f0453ae5672efd94774a",
    },
}
EXPECTED_FACTORISATION_HASH = (
    "72c0f82d284e3fdbf977e20827a5a21ec811f1ddb4b8826d369b35bd149ac86b"
)
EXPECTED_GATE_RESULTANTS = {
    "p_minus_q": "3/2",
    "d0": "1/2",
    "P": "1/4",
    "L1": "3/4",
    "L2": "3",
    "e": "8",
    "Delta": "27/8",
    "s_denominator": "1/2",
    "b88_denominator": "2",
    "c88_denominator": "4",
    "kernel_uv_denominator": "3/16",
}
EXPECTED_MINOR_SHAPES = {
    "T0": {"bc_total_degree": 3, "c_degree": 1, "q_degree": 1, "a_degree": 2},
    "T1": {"bc_total_degree": 3, "c_degree": 1, "q_degree": 1, "a_degree": 3},
    "T2": {"bc_total_degree": 3, "c_degree": 1, "q_degree": 1, "a_degree": 3},
    "T3": {"bc_total_degree": 3, "c_degree": 1, "q_degree": 1, "a_degree": 2},
    "D0": {"bc_total_degree": 3, "c_degree": 2, "q_degree": 1, "a_degree": 2},
    "D2": {"bc_total_degree": 3, "c_degree": 2, "q_degree": 1, "a_degree": 2},
}
EXPECTED_MULTIPLIER_SIGNATURE = {"rows": 158, "columns": 144, "rank": 140}
EXPECTED_AUGMENTED_RANK = {"B": 140, "C": 140}


Pair = tuple[sp.Expr, sp.Expr]
GScalar = tuple[Fraction, Fraction]
GZERO: GScalar = (Fraction(0), Fraction(0))
GONE: GScalar = (Fraction(1), Fraction(0))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(("cannot load canonical builder", path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def clean(expression: sp.Expr) -> sp.Expr:
    return sp.expand(expression)


def q6_polynomial(p_value: sp.Expr, q_value: sp.Expr) -> sp.Expr:
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


def support_digest(gld71) -> str:
    supports = tuple(gld71.SPARSE_RELATIONS[index] for index in SUPPORT_ROWS)
    encoded = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in support],
        ]
        for row, support in zip(SUPPORT_ROWS, supports, strict=True)
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()


def h2_factorization() -> dict[str, object]:
    h2 = 2 * p**2 - 2 * p + 1
    q6 = q6_polynomial(p, q)
    resultant = sp.factor(sp.resultant(h2, q6, p))
    expected_resultant = (2 * q**2 - 2 * q + 1) * (
        2 * q**4 - 4 * q**3 + 10 * q**2 - 8 * q + 5
    )
    if sp.expand(resultant - expected_resultant) != 0:
        raise AssertionError(("H2/Q6 resultant", resultant))
    d0_plus = sp.expand(P_PLUS + q - 1)
    d0_minus = sp.expand(P_MINUS + q - 1)
    q_plus = q**2 - (1 + I) * q + (3 + I) / 2
    q_minus = q**2 - (1 - I) * q + (3 - I) / 2
    plus_value = sp.expand(q6.subs(p, P_PLUS))
    minus_value = sp.expand(q6.subs(p, P_MINUS))
    if sp.expand(plus_value + I * d0_plus * q_plus / 2) != 0:
        raise AssertionError("plus H2/Q6 factorization mismatch")
    if sp.expand(minus_value - I * d0_minus * q_minus / 2) != 0:
        raise AssertionError("minus H2/Q6 factorization mismatch")
    if sp.expand(q_minus - sp.conjugate(q_plus)) != 0:
        raise AssertionError("minus quadratic is not the conjugate branch")
    payload = {
        "H2": str(sp.expand(h2)),
        "resultant_p": str(resultant),
        "p_plus": str(P_PLUS),
        "p_minus": str(P_MINUS),
        "Q_plus": str(sp.expand(q_plus)),
        "Q_minus": str(sp.expand(q_minus)),
        "Q6_at_p_plus": str(plus_value),
        "Q6_at_p_minus": str(minus_value),
        "d0_at_p_plus": str(d0_plus),
        "d0_at_p_minus": str(d0_minus),
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if digest != EXPECTED_FACTORISATION_HASH:
        raise AssertionError(("factorization hash", digest, EXPECTED_FACTORISATION_HASH))
    plus_poly = sp.Poly(q_plus, q, domain=QQ_I)
    minus_poly = sp.Poly(q_minus, q, domain=QQ_I)
    if sp.discriminant(plus_poly.as_expr(), q) != -6:
        raise AssertionError("Q+ discriminant")
    if not plus_poly.is_irreducible or not minus_poly.is_irreducible:
        raise AssertionError("Q+/- irreducibility")
    return {
        **payload,
        "factorization_sha256": digest,
        "Q_plus_discriminant": str(sp.discriminant(plus_poly.as_expr(), q)),
        "Q_minus_discriminant": str(sp.discriminant(minus_poly.as_expr(), q)),
        "Q_plus_irreducible_over_QI": True,
        "Q_minus_irreducible_over_QI": True,
        "d0_component_removed_by_Delta": True,
    }


def chart_factors(p_value: sp.Expr) -> dict[str, sp.Expr]:
    d0 = p_value + q - 1
    P = p_value**2 - p_value + 1
    L1 = p_value**2 + 2 * p_value * q - 2 * p_value - q
    L2 = 2 * p_value * q - p_value + q**2 - 2 * q
    e = 2 * p_value * q**2 - 2 * p_value * q - p_value - q**2 - 2 * q + 2
    return {
        "p_minus_q": p_value - q,
        "d0": d0,
        "P": P,
        "L1": L1,
        "L2": L2,
        "e": e,
        "Delta": sp.expand((p_value - q) * d0 * P * L1 * L2 * e),
    }


def denominator_factors(p_value: sp.Expr) -> dict[str, sp.Expr]:
    factors = chart_factors(p_value)
    return {
        "s_denominator": factors["d0"],
        "b88_denominator": factors["P"] * factors["e"],
        "c88_denominator": factors["d0"] * factors["e"],
        "kernel_uv_denominator": factors["p_minus_q"] * factors["d0"] ** 3,
    }


def gate_report(qmod: sp.Poly, p_value: sp.Expr) -> dict[str, object]:
    gates = {**chart_factors(p_value), **denominator_factors(p_value)}
    q_poly = sp.Poly(qmod.as_expr(), q, domain=QQ_I)
    resultants: dict[str, str] = {}
    gcds: dict[str, str] = {}
    for name, value in gates.items():
        value_poly = sp.Poly(sp.expand(value), q, domain=QQ_I)
        gcd = sp.gcd(q_poly, value_poly)
        resultant = sp.expand(sp.resultant(q_poly.as_expr(), value_poly.as_expr(), q))
        if gcd.degree() != 0 or resultant == 0:
            raise AssertionError(("nonunit chart gate", name, gcd, resultant))
        gcds[name] = str(gcd.as_expr())
        resultants[name] = str(resultant)
    if resultants != EXPECTED_GATE_RESULTANTS:
        raise AssertionError(("gate resultants", resultants, EXPECTED_GATE_RESULTANTS))
    if not q_poly.is_irreducible:
        raise AssertionError("quadratic branch is reducible")
    q6_remainder = sp.rem(
        sp.Poly(q6_polynomial(p_value, q), q, domain=QQ_I), q_poly
    ).as_expr()
    if q6_remainder != 0:
        raise AssertionError(("Q6 branch remainder", q6_remainder))
    return {
        "p": str(p_value),
        "gcds_with_Q_branch": gcds,
        "resultants_with_Q_branch": resultants,
        "all_units_on_Delta": True,
        "d0_component_removed_by_Delta": True,
        "Q6_remainder_zero": True,
    }


def branch_family(family: dict[str, sp.Expr], p_value: sp.Expr) -> dict[str, sp.Expr]:
    return {name: sp.cancel(value.subs(p, p_value)) for name, value in family.items()}


def family_denominator_report(family: dict[str, sp.Expr]) -> dict[str, object]:
    d0 = p + q - 1
    P = p**2 - p + 1
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    expected = {
        "s": d0,
        "b": P * e,
        "c": d0 * e,
        "u": (p - q) * d0**3,
        "v": (p - q) * d0**3,
    }
    checks: dict[str, bool] = {}
    for name, denominator in expected.items():
        actual = sp.cancel(family[name]).as_numer_denom()[1]
        ratio = sp.cancel(actual / denominator)
        checks[name] = ratio != 0 and not ratio.has(p, q, a, B, C)
        if not checks[name]:
            raise AssertionError(("unexpected canonical F88 denominator", name, actual, denominator))
    return {
        "coordinate_denominators_match_F88": checks,
        "no_displayed_variable_denominator": True,
        "declared_denominators": {name: str(value) for name, value in expected.items()},
    }


class QuadraticQuotient:
    """Exact QQ(i)[a]-coefficient quotient by Q_e(q)."""

    def __init__(self, epsilon: int) -> None:
        self.epsilon = epsilon
        self.p_value = (1 + epsilon * I) / 2
        self.k = sp.expand(q**2 - (1 + epsilon * I) * q + (3 + epsilon * I) / 2)
        self.r0 = -(3 + epsilon * I) / 2
        self.r1 = 1 + epsilon * I
        self.zero: Pair = (sp.Integer(0), sp.Integer(0))
        self.one: Pair = (sp.Integer(1), sp.Integer(0))
        self.q: Pair = (sp.Integer(0), sp.Integer(1))
        self.denominators: list[tuple[str, sp.Expr]] = []

    @staticmethod
    def equal(left: Pair, right: Pair) -> bool:
        return clean(left[0] - right[0]) == 0 and clean(left[1] - right[1]) == 0

    def add(self, left: Pair, right: Pair) -> Pair:
        return clean(left[0] + right[0]), clean(left[1] + right[1])

    def neg(self, value: Pair) -> Pair:
        return clean(-value[0]), clean(-value[1])

    def sub(self, left: Pair, right: Pair) -> Pair:
        return self.add(left, self.neg(right))

    def mul(self, left: Pair, right: Pair) -> Pair:
        return (
            clean(left[0] * right[0] + left[1] * right[1] * self.r0),
            clean(left[0] * right[1] + left[1] * right[0] + left[1] * right[1] * self.r1),
        )

    def reduce_polynomial(self, expression: sp.Expr) -> Pair:
        polynomial = sp.Poly(sp.expand(expression), q)
        result = self.zero
        for exponent in range(int(polynomial.degree()), -1, -1):
            coefficient = polynomial.nth(exponent)
            if coefficient.has(q):
                raise AssertionError("q coefficient did not normalize")
            result = self.add(self.mul(result, self.q), (coefficient, sp.Integer(0)))
        return result

    def inverse(self, value: Pair) -> Pair:
        conjugate = clean(value[0] + value[1] * self.r1), clean(-value[1])
        product = self.mul(value, conjugate)
        if product[1] != 0:
            raise AssertionError(("quadratic norm has q part", product))
        norm = clean(product[0])
        if norm == 0 or norm.has(a, B, C):
            raise AssertionError(("nonunit quotient denominator", value, norm))
        return clean(conjugate[0] / norm), clean(conjugate[1] / norm)

    def from_expr(self, expression: sp.Expr, label: str = "") -> Pair:
        expression = sp.cancel(expression)
        numerator, denominator = expression.as_numer_denom()
        if denominator.has(a, B, C):
            raise AssertionError(("displayed-variable denominator", label, denominator))
        self.denominators.append((label, sp.factor(denominator)))
        return self.mul(
            self.reduce_polynomial(numerator),
            self.inverse(self.reduce_polynomial(denominator)),
        )

    def quotient_remainder(self, expression: sp.Expr) -> sp.Expr:
        return sp.rem(sp.Poly(sp.expand(expression), q), sp.Poly(self.k, q)).as_expr()


class BCPolynomial:
    """Sparse B,C polynomial over one exact quadratic quotient."""

    def __init__(self, algebra: QuadraticQuotient, terms: dict[tuple[int, int], Pair] | None = None) -> None:
        self.algebra = algebra
        self.terms: dict[tuple[int, int], Pair] = {}
        for exponent, coefficient in (terms or {}).items():
            if not algebra.equal(coefficient, algebra.zero):
                self.terms[exponent] = coefficient

    @classmethod
    def constant(cls, algebra: QuadraticQuotient, value: Pair) -> "BCPolynomial":
        return cls(algebra, {(0, 0): value})

    @classmethod
    def variable(cls, algebra: QuadraticQuotient, exponent: tuple[int, int]) -> "BCPolynomial":
        return cls(algebra, {exponent: algebra.one})

    def __add__(self, other: "BCPolynomial") -> "BCPolynomial":
        terms = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            old = terms.get(exponent, self.algebra.zero)
            value = self.algebra.add(old, coefficient)
            if self.algebra.equal(value, self.algebra.zero):
                terms.pop(exponent, None)
            else:
                terms[exponent] = value
        return BCPolynomial(self.algebra, terms)

    def __neg__(self) -> "BCPolynomial":
        return BCPolynomial(
            self.algebra,
            {exponent: self.algebra.neg(value) for exponent, value in self.terms.items()},
        )

    def __sub__(self, other: "BCPolynomial") -> "BCPolynomial":
        return self + (-other)

    def __mul__(self, other: "BCPolynomial") -> "BCPolynomial":
        terms: dict[tuple[int, int], Pair] = {}
        for (left_b, left_c), left_value in self.terms.items():
            for (right_b, right_c), right_value in other.terms.items():
                exponent = (left_b + right_b, left_c + right_c)
                product = self.algebra.mul(left_value, right_value)
                old = terms.get(exponent, self.algebra.zero)
                terms[exponent] = self.algebra.add(old, product)
        return BCPolynomial(self.algebra, terms)


def direct_rows(gld71, algebra: QuadraticQuotient, leaf: list[list[BCPolynomial]], rows: tuple[int, ...]):
    result: dict[int, list[BCPolynomial]] = {}
    zero = BCPolynomial(algebra)
    for relation_row in rows:
        entries: list[BCPolynomial] = []
        for root in range(3):
            for component in range(3):
                total = zero
                for indices, coefficient in gld71.SPARSE_RELATIONS[relation_row]:
                    if indices[0] != root:
                        continue
                    term = leaf[indices[1]][component] * leaf[indices[2]][component] * leaf[indices[3]][component]
                    total = total + BCPolynomial.constant(
                        algebra, (sp.Integer(coefficient), sp.Integer(0))
                    ) * term
                entries.append(total)
        result[relation_row] = entries
    return result


def direct_determinant(matrix: list[list[BCPolynomial]]) -> BCPolynomial:
    algebra = matrix[0][0].algebra
    zero = BCPolynomial(algebra)
    one = BCPolynomial.constant(algebra, algebra.one)
    states: dict[int, BCPolynomial] = {0: one}
    for _row in range(len(matrix)):
        next_states: dict[int, BCPolynomial] = {}
        for mask, value in states.items():
            for column in range(len(matrix)):
                if mask & (1 << column):
                    continue
                available_before = sum(
                    1 for previous in range(column) if not (mask & (1 << previous))
                )
                term = value * matrix[_row][column]
                if available_before & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = next_states.get(new_mask, zero) + term
        states = next_states
    return states[(1 << len(matrix)) - 1]


def make_leaf(
    algebra: QuadraticQuotient,
    family: dict[str, sp.Expr],
    *,
    include_offsets: bool = True,
) -> list[list[BCPolynomial]]:
    one = BCPolynomial.constant(algebra, algebra.one)
    b_coordinate = BCPolynomial.constant(algebra, algebra.from_expr(1 + family["b"], "1+b"))
    c_coordinate = BCPolynomial.constant(algebra, algebra.from_expr(1 + family["c"], "1+c"))
    if include_offsets:
        b_coordinate = b_coordinate + BCPolynomial.variable(algebra, (1, 0))
        c_coordinate = c_coordinate + BCPolynomial.variable(algebra, (0, 1))
    leaf = [
        [one, one, one],
        [
            BCPolynomial.constant(algebra, algebra.from_expr(algebra.p_value, "p")),
            BCPolynomial.constant(algebra, algebra.q),
            BCPolynomial.constant(algebra, algebra.from_expr(family["s"], "s")),
        ],
        [
            BCPolynomial.constant(algebra, algebra.from_expr(a, "a")),
            b_coordinate,
            c_coordinate,
        ],
    ]
    return leaf


def evaluate_bc(polynomial: BCPolynomial, b_value: int, c_value: int, a_value: int) -> Pair:
    result = polynomial.algebra.zero
    for (b_degree, c_degree), coefficient in polynomial.terms.items():
        scalar = b_value**b_degree * c_value**c_degree
        result = polynomial.algebra.add(
            result,
            (
                clean(coefficient[0].subs(a, a_value) * scalar),
                clean(coefficient[1].subs(a, a_value) * scalar),
            ),
        )
    return result


def bareiss_determinant(matrix: list[list[Pair]], algebra: QuadraticQuotient) -> Pair:
    work = [[value for value in row] for row in matrix]
    sign = 1
    previous = algebra.one
    for pivot_index in range(len(matrix) - 1):
        pivot_row = next(
            (row for row in range(pivot_index, len(matrix)) if not algebra.equal(work[row][pivot_index], algebra.zero)),
            None,
        )
        if pivot_row is None:
            return algebra.zero
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, len(matrix)):
            for column in range(pivot_index + 1, len(matrix)):
                numerator = algebra.sub(
                    algebra.mul(pivot, work[row][column]),
                    algebra.mul(work[row][pivot_index], work[pivot_index][column]),
                )
                if pivot_index:
                    numerator = algebra.mul(numerator, algebra.inverse(previous))
                work[row][column] = numerator
            work[row][pivot_index] = algebra.zero
        previous = pivot
    result = work[-1][-1]
    return result if sign == 1 else algebra.neg(result)


def polynomial_payload(value: sp.Expr) -> list[list[str]]:
    value = clean(value)
    if value == 0:
        return []
    polynomial = sp.Poly(sp.expand(value), a, extension=I)
    result = []
    for index in range(int(polynomial.degree()) + 1):
        coefficient = polynomial.nth(index)
        real, imaginary = coefficient.as_real_imag()
        result.append([str(sp.Rational(real)), str(sp.Rational(imaginary))])
    return result


def generator_payload(polynomial: BCPolynomial) -> list[list[object]]:
    return [
        [b_degree, c_degree, polynomial_payload(pair[0]), polynomial_payload(pair[1])]
        for (b_degree, c_degree), pair in sorted(polynomial.terms.items())
    ]


def payload_hash(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def canonical_builder_probe(gld71, parent, relations, gld88, family) -> dict[str, object]:
    """Exercise both canonical builders before the custom quotient replay."""

    if len(relations) != 37 or support_digest(gld71) != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError("canonical GLD71 relation surface changed")
    probe_substitution = {p: 0, q: 3, a: 0}
    if sp.cancel(family["s"].subs(probe_substitution) - sp.Rational(3, 2)) != 0:
        raise AssertionError("canonical GLD88 family probe")
    probe_leaf = sp.Matrix([[1, 1, 1], [0, 3, sp.Rational(3, 2)], [0, 3, 4]])
    syndrome = gld71.coefficient_matrix(parent, relations, (probe_leaf, probe_leaf, probe_leaf))
    if syndrome.shape != (37, 9):
        raise AssertionError(("canonical syndrome shape", syndrome.shape))
    checks = 0
    for row, support in enumerate(gld71.SPARSE_RELATIONS):
        for root in range(3):
            for component in range(3):
                expected = sum(
                    coefficient
                    * probe_leaf[indices[1], component]
                    * probe_leaf[indices[2], component]
                    * probe_leaf[indices[3], component]
                    for indices, coefficient in support
                    if indices[0] == root
                )
                if sp.expand(syndrome[row, 3 * root + component] - expected) != 0:
                    raise AssertionError(("canonical syndrome entry", row, root, component))
                checks += 1
    if checks != 333:
        raise AssertionError(("canonical builder check count", checks))
    return {"syndrome_shape": [37, 9], "entry_checks": checks, "verified": True}


def check_f88_kernel(gld71, algebra: QuadraticQuotient, family: dict[str, sp.Expr]) -> dict[str, object]:
    branch = branch_family(family, algebra.p_value)
    leaf = make_leaf(algebra, branch, include_offsets=False)
    rows = direct_rows(gld71, algebra, leaf, tuple(range(37)))
    kernel = (
        algebra.from_expr(branch["u"], "u kernel"),
        algebra.from_expr(branch["v"], "v kernel"),
        algebra.one,
    )
    checks = 0
    for relation_row in range(37):
        for block in range(3):
            entries = rows[relation_row][3 * block : 3 * block + 3]
            total = algebra.zero
            for entry, coordinate in zip(entries, kernel, strict=True):
                pair = entry.terms.get((0, 0), algebra.zero)
                total = algebra.add(total, algebra.mul(pair, coordinate))
            if not algebra.equal(total, algebra.zero):
                raise AssertionError(("F88 kernel identity", algebra.epsilon, relation_row, block, total))
            checks += 1
    if checks != 111:
        raise AssertionError(("kernel check count", checks))
    return {
        "identity_count": checks,
        "kernel": [str(branch["u"]), str(branch["v"]), "1"],
        "verified": True,
    }


def denominator_report(algebra: QuadraticQuotient, family: dict[str, sp.Expr]) -> dict[str, object]:
    gate_values = list(chart_factors(algebra.p_value).values())
    gate_polynomials = [sp.Poly(sp.expand(value), q, extension=I) for value in gate_values]
    unknown: list[str] = []
    for label, denominator in algebra.denominators:
        if denominator.has(a, B, C):
            raise AssertionError(("displayed-variable denominator", label, denominator))
        denominator_poly = sp.Poly(sp.expand(denominator), q, extension=I)
        common = sp.gcd(denominator_poly, sp.Poly(algebra.k, q, extension=I))
        if common.degree() != 0:
            raise AssertionError(("recorded denominator is not a branch unit", label, denominator, common))
        _unit, factors = sp.factor_list(denominator_poly.as_expr(), extension=I)
        for factor, _multiplicity in factors:
            factor_poly = sp.Poly(factor, q, extension=I)
            if factor_poly.degree() != 0 and not any(
                sp.gcd(factor_poly, gate).degree() > 0 for gate in gate_polynomials
            ):
                unknown.append(str(factor))
    if unknown:
        raise AssertionError(("unlisted denominator factors", sorted(set(unknown))))
    return {
        "recorded_denominators": len(algebra.denominators),
        "all_recorded_denominators_branch_units": True,
        "all_recorded_factors_in_Delta": True,
        "no_a_B_C_denominators": True,
        "family_coordinate_denominators": family_denominator_report(family),
    }


def minor_shape(polynomial: BCPolynomial) -> dict[str, int]:
    bc_total_degree = max((sum(exponent) for exponent in polynomial.terms), default=0)
    c_degree = max((exponent[1] for exponent in polynomial.terms), default=0)
    q_degree = max(
        (index for pair in polynomial.terms.values() for index, component in enumerate(pair) if component != 0),
        default=0,
    )
    a_degree = max(
        int(sp.Poly(component, a, extension=I).degree())
        for pair in polynomial.terms.values()
        for component in pair
        if component != 0
    )
    return {
        "bc_total_degree": bc_total_degree,
        "c_degree": c_degree,
        "q_degree": q_degree,
        "a_degree": a_degree,
    }


def g_add(left: GScalar, right: GScalar) -> GScalar:
    return left[0] + right[0], left[1] + right[1]


def g_neg(value: GScalar) -> GScalar:
    return -value[0], -value[1]


def g_sub(left: GScalar, right: GScalar) -> GScalar:
    return g_add(left, g_neg(right))


def g_mul(left: GScalar, right: GScalar) -> GScalar:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_to_sympy(value: GScalar) -> sp.Expr:
    return sp.Rational(value[0].numerator, value[0].denominator) + I * sp.Rational(
        value[1].numerator, value[1].denominator
    )


def gaussian_fraction(value: sp.Expr) -> GScalar:
    real, imaginary = sp.expand(value).as_real_imag()
    real = sp.Rational(real)
    imaginary = sp.Rational(imaginary)
    return (
        Fraction(int(real.p), int(real.q)),
        Fraction(int(imaginary.p), int(imaginary.q)),
    )


def exact_domain_matrix(matrix: list[list[GScalar]]) -> DomainMatrix:
    return DomainMatrix.from_Matrix(
        sp.Matrix([[gaussian_to_sympy(value) for value in row] for row in matrix])
    ).convert_to(QQ_I)


def matrix_vector(matrix: list[list[GScalar]], vector: list[GScalar]) -> list[GScalar]:
    result: list[GScalar] = []
    for row in matrix:
        total = GZERO
        for left, right in zip(row, vector, strict=True):
            total = g_add(total, g_mul(left, right))
        result.append(total)
    return result


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def certificate_hash(solution: list[GScalar]) -> str:
    payload = [[fraction_text(real), fraction_text(imaginary)] for real, imaginary in solution]
    return payload_hash(payload)


def domain_hash(matrix: DomainMatrix) -> str:
    encoded = [
        [[str(value.x), str(value.y)] for value in row]
        for row in matrix.to_list()
    ]
    return payload_hash(encoded)


def build_multiplier_system(
    algebra: QuadraticQuotient,
    generators: dict[str, BCPolynomial],
) -> tuple[list[tuple[str, tuple[int, int], int, int]], list[tuple[int, int, int, int]], list[list[GScalar]], dict[str, list[GScalar]]]:
    """Build the exact 158x144 coefficient system.

    The descriptor order is immutable: minor name, BC multiplier, a degree,
    then the quotient multiplier 1 or q.  Every coefficient key is a tuple
    ``(B_degree,C_degree,a_degree,q_basis_degree)``.
    """

    bc_monomials = ((0, 0), (1, 0), (0, 1))
    q_monomials = (algebra.one, algebra.q)
    descriptors: list[tuple[str, tuple[int, int], int, int]] = []
    columns: list[dict[tuple[int, int, int, int], sp.Expr]] = []
    for name in MINORS:
        for multiplier_bc in bc_monomials:
            for multiplier_a in range(4):
                for multiplier_q, q_multiplier in enumerate(q_monomials):
                    descriptors.append((name, multiplier_bc, multiplier_a, multiplier_q))
                    column: dict[tuple[int, int, int, int], sp.Expr] = {}
                    for (base_b, base_c), coefficient in generators[name].terms.items():
                        product = algebra.mul(coefficient, q_multiplier)
                        for q_degree, component in enumerate(product):
                            if component == 0:
                                continue
                            component_poly = sp.Poly(sp.expand(component), a, extension=I)
                            for a_degree in range(int(component_poly.degree()) + 1):
                                scalar = clean(component_poly.nth(a_degree))
                                if scalar == 0:
                                    continue
                                key = (
                                    base_b + multiplier_bc[0],
                                    base_c + multiplier_bc[1],
                                    a_degree + multiplier_a,
                                    q_degree,
                                )
                                column[key] = clean(column.get(key, 0) + scalar)
                    columns.append(column)
    if len(descriptors) != 6 * 3 * 4 * 2:
        raise AssertionError(("multiplier descriptor count", len(descriptors)))
    row_keys: list[tuple[int, int, int, int]] = sorted(
        {key for column in columns for key, value in column.items() if value != 0}
        | {(1, 0, 0, 0), (0, 1, 0, 0)}
    )
    if len(row_keys) != EXPECTED_MULTIPLIER_SIGNATURE["rows"]:
        raise AssertionError(("multiplier row count", len(row_keys)))
    matrix = [
        [gaussian_fraction(column.get(key, 0)) for column in columns]
        for key in row_keys
    ]
    targets = {
        name: [GONE if row_key == key else GZERO for row_key in row_keys]
        for name, key in (("B", (1, 0, 0, 0)), ("C", (0, 1, 0, 0)))
    }
    if any(not isinstance(key, tuple) or len(key) != 4 for key in row_keys):
        raise AssertionError("Macaulay row key is not a four-tuple")
    if len(matrix) != 158 or len(matrix[0]) != 144:
        raise AssertionError(("multiplier matrix shape", len(matrix), len(matrix[0])))
    return descriptors, row_keys, matrix, targets


def macaulay_certificate(
    epsilon: int,
    descriptors: list[tuple[str, tuple[int, int], int, int]],
    row_keys: list[tuple[int, int, int, int]],
    matrix: list[list[GScalar]],
    targets: dict[str, list[GScalar]],
) -> tuple[dict[str, object], dict[str, list[GScalar]]]:
    if len(descriptors) != 144 or len(row_keys) != 158:
        raise AssertionError("unexpected Macaulay input shape")
    base = exact_domain_matrix(matrix)
    base_rref, base_pivots = base.rref()
    if base.shape != (158, 144) or len(base_pivots) != 140:
        raise AssertionError(("Macaulay rank signature", base.shape, len(base_pivots)))
    result: dict[str, object] = {
        "rows": 158,
        "columns": 144,
        "rank": len(base_pivots),
        "pivot_columns": list(base_pivots),
        "base_rref_sha256": domain_hash(base_rref),
        "multiplier_bc_degree_max": 1,
        "multiplier_a_degree_max": 3,
        "q_basis": ["1", "q"],
        "targets": {},
    }
    solutions: dict[str, list[GScalar]] = {}
    for target_name in ("B", "C"):
        augmented = [row + [value] for row, value in zip(matrix, targets[target_name], strict=True)]
        augmented_dm = exact_domain_matrix(augmented)
        augmented_rref, augmented_pivots = augmented_dm.rref()
        if len(augmented_pivots) != EXPECTED_AUGMENTED_RANK[target_name]:
            raise AssertionError(("augmented rank", target_name, augmented_pivots))
        target_column = 144
        if target_column in augmented_pivots:
            raise AssertionError(("target became a pivot", target_name))
        solution = [GZERO for _ in descriptors]
        augmented_list = augmented_rref.to_Matrix().tolist()
        for row_index, pivot_column in enumerate(augmented_pivots):
            if pivot_column < target_column:
                solution[pivot_column] = gaussian_fraction(augmented_list[row_index][target_column])
        residual = matrix_vector(matrix, solution)
        if residual != targets[target_name]:
            raise AssertionError(("certificate residual", target_name))
        actual_hash = certificate_hash(solution)
        expected_hash = EXPECTED_CERTIFICATE_HASHES[epsilon][target_name]
        if actual_hash != expected_hash:
            raise AssertionError(("certificate hash", target_name, actual_hash, expected_hash))
        result["targets"][target_name] = {
            "augmented_shape": [158, 145],
            "rank_with_target": len(augmented_pivots),
            "pivot_columns": list(augmented_pivots),
            "target_column_is_not_pivot": True,
            "rref_sha256": domain_hash(augmented_rref),
            "solution_sha256": actual_hash,
            "nonzero_multiplier_coefficients": sum(value != GZERO for value in solution),
            "exact_identity_verified": True,
        }
        solutions[target_name] = solution
    return result, solutions


def run_branch(gld71, family: dict[str, sp.Expr], epsilon: int) -> dict[str, object]:
    started = time.monotonic()
    algebra = QuadraticQuotient(epsilon)
    qmod = sp.Poly(algebra.k, q, domain=QQ_I)
    gates = gate_report(qmod, algebra.p_value)
    branch = branch_family(family, algebra.p_value)
    leaf = make_leaf(algebra, branch)
    rows = direct_rows(gld71, algebra, leaf, tuple(range(37)))
    kernel = check_f88_kernel(gld71, algebra, family)
    denominators = denominator_report(algebra, family)
    generators: dict[str, BCPolynomial] = {}
    minor_records: dict[str, object] = {}
    generator_payloads: dict[str, list[list[object]]] = {}
    generator_hashes: dict[str, str] = {}
    constant_checks: dict[str, bool] = {}
    shapes: dict[str, dict[str, int]] = {}
    bareiss_controls: dict[str, bool] = {}
    for name, (selected_rows, selected_columns) in MINORS.items():
        if name.startswith("T"):
            target_row, target_column = TARGETS[int(name[1:])]
            if selected_rows != (*PIVOT_ROWS, target_row) or selected_columns != (*PIVOT_COLUMNS, target_column):
                raise AssertionError(("T selection drift", name))
        matrix = [[rows[row][column] for column in selected_columns] for row in selected_rows]
        print(f"[gld99] epsilon={epsilon} {name} determinant", file=sys.stderr, flush=True)
        generator = direct_determinant(matrix)
        generators[name] = generator
        payload = generator_payload(generator)
        generator_payloads[name] = payload
        digest = payload_hash(payload)
        generator_hashes[name] = digest
        if digest != EXPECTED_GENERATOR_HASHES[epsilon][name]:
            raise AssertionError(("minor payload hash", epsilon, name, digest))
        constant = generator.terms.get((0, 0), algebra.zero)
        constant_checks[name] = algebra.equal(constant, algebra.zero)
        if not constant_checks[name]:
            raise AssertionError(("nonzero B=C=0 constant", epsilon, name, constant))
        shape = minor_shape(generator)
        shapes[name] = shape
        if shape != EXPECTED_MINOR_SHAPES[name]:
            raise AssertionError(("minor support shape", epsilon, name, shape, EXPECTED_MINOR_SHAPES[name]))
        specialized_matrix = [
            [evaluate_bc(matrix[row_index][column_index], 2, 3, 5) for column_index in range(7)]
            for row_index in range(7)
        ]
        bareiss_controls[name] = algebra.equal(
            bareiss_determinant(specialized_matrix, algebra),
            evaluate_bc(generator, 2, 3, 5),
        )
        if not bareiss_controls[name]:
            raise AssertionError(("Bareiss determinant control", epsilon, name))
        minor_records[name] = {
            "rows": list(selected_rows),
            "columns": list(selected_columns),
            "representation": "exact A_e[B,C] sparse determinant",
            "payload_sha256": digest,
            "support_shape": shape,
            "constant_term_zero": constant_checks[name],
            "bareiss_specialization_control": True,
        }
    descriptors, row_keys, multiplier_matrix, targets = build_multiplier_system(algebra, generators)
    print(f"[gld99] epsilon={epsilon} Macaulay {len(row_keys)}x{len(descriptors)}", file=sys.stderr, flush=True)
    # The certificate hashes are branch-specific.  The matrix/rank shape is
    # branch-invariant, while the actual Gaussian coefficients are conjugate.
    macaulay, solutions = macaulay_certificate(
        epsilon, descriptors, row_keys, multiplier_matrix, targets
    )
    public = {
        "epsilon": epsilon,
        "p": str(algebra.p_value),
        "Q_branch": str(algebra.k),
        "gates": gates,
        "F88_kernel": kernel,
        "denominator_audit": denominators,
        "minor_records": minor_records,
        "minor_hashes": generator_hashes,
        "constant_terms_zero": constant_checks,
        "bareiss_specialization_controls": bareiss_controls,
        "macaulay": macaulay,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    return {
        **public,
        "_generator_payloads": generator_payloads,
        "_certificate_solutions": solutions,
    }


def conjugate_payload(payload: list[list[object]]) -> list[list[object]]:
    result = []
    for b_degree, c_degree, constant_payload, q_payload in payload:
        def conjugate_coefficients(coefficients: list[list[str]]) -> list[list[str]]:
            return [[real, str(-sp.Rational(imaginary))] for real, imaginary in coefficients]
        result.append([
            b_degree,
            c_degree,
            conjugate_coefficients(constant_payload),
            conjugate_coefficients(q_payload),
        ])
    return result


def conjugate_solution(solution: list[GScalar]) -> list[GScalar]:
    return [(real, -imaginary) for real, imaginary in solution]


def main() -> int:
    started = time.monotonic()
    print("[gld99] H2 factorization", file=sys.stderr, flush=True)
    factorization = h2_factorization()
    print("[gld99] canonical builders", file=sys.stderr, flush=True)
    gld71 = load_module(GLD71, "gld71_for_gld99_h2_primary")
    gld88 = load_module(GLD88, "gld88_for_gld99_h2_primary")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    family = gld88.h4_family(p, q, a)
    canonical = canonical_builder_probe(gld71, parent, relations, gld88, family)
    branches = [run_branch(gld71, family, 1), run_branch(gld71, family, -1)]
    plus_payloads = branches[0].pop("_generator_payloads")
    minus_payloads = branches[1].pop("_generator_payloads")
    plus_solutions = branches[0].pop("_certificate_solutions")
    minus_solutions = branches[1].pop("_certificate_solutions")
    for name in MINORS:
        if minus_payloads[name] != conjugate_payload(plus_payloads[name]):
            raise AssertionError(("minus determinant is not coefficientwise conjugate", name))
    for name in ("B", "C"):
        if minus_solutions[name] != conjugate_solution(plus_solutions[name]):
            raise AssertionError(("minus certificate is not coefficientwise conjugate", name))
    if branches[0]["minor_hashes"] == branches[1]["minor_hashes"]:
        raise AssertionError("plus/minus hashes unexpectedly compared as identical")
    output = {
        "status": "exact_scoped_H2_degree_drop_six_minor_offset_exclusion",
        "gld_identifier": "GLD99",
        "field": "Q_characteristic_zero_then_Q(i)",
        "global_conjecture": "UNRESOLVED",
        "runtime_environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "scope": (
            "normalized equal-leaf H4 GLD88/F88 offset chart on H2=Q6=0 and D(Delta), "
            "both Q(i) quadratic branches, symbolic a"
        ),
        "constructors": {
            "GLD71": GLD71.relative_to(ROOT).as_posix(),
            "GLD88": GLD88.relative_to(ROOT).as_posix(),
            "imports_exploratory_files": False,
            "support_rows": list(SUPPORT_ROWS),
            "support_digest_sha256": EXPECTED_SUPPORT_DIGEST,
            "canonical_builder_probe": canonical,
        },
        "h2_factorization": factorization,
        "pivot_rows": list(PIVOT_ROWS),
        "pivot_columns": list(PIVOT_COLUMNS),
        "targets": [list(target) for target in TARGETS],
        "branches": branches,
        "conjugation": {
            "both_branches_recomputed": True,
            "coefficient_field": "Q(i)",
            "determinant_payloads_conjugate": True,
            "certificate_vectors_conjugate": True,
            "branch_hashes_checked_separately": True,
        },
        "implication": (
            "Full syndrome rank at most six implies vanishing of these six selected "
            "seven-minors; the exact polynomial certificates then force B=C=0 "
            "on the declared normalized D(Delta) chart."
        ),
        "localization_fences": {
            "R31": "not included or inverted",
            "E31": "not used or inverted",
            "g0": "not used or inverted",
            "a": "polynomial variable; no a localization",
            "d0": "excluded by the Delta gate, not silently inverted in Q6",
        },
        "nonclaims": [
            "The six displayed minors are not claimed equivalent to the full rank ideal.",
            "No arbitrary-p, other-chart, Delta=0, or outside-F88 closure is claimed.",
            "No GLD83 Fitting pullback or GLD95 downstream exclusion is replayed here.",
            "No global Krenn-Gu resolution is claimed; global status remains UNRESOLVED.",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    print("H2 degree-drop six-minor offset verifier: PASS")
    print(json.dumps(output, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
