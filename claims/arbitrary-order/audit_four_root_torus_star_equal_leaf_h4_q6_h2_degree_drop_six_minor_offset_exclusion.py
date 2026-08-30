#!/usr/bin/env python3
"""Independent H2=0 audit of the six-minor offset membership certificate.

This file is deliberately self-contained.  It copies the ten sparse supports
used by the six GLD97 seven-minors and the written GLD88 F88 coordinate
formula; it does not import a primary verifier, GLD71, GLD88, GLD96, or the
GLD98 exploratory census.  At each root of

    H2(p) = 2*p**2 - 2*p + 1

the Q6 relation has a degree-drop component.  We work in the *separate*
quadratic quotient

    A_e = QQ(i)[q]/(k_e),
    k_e = q**2 - (1+e*i)*q + (3+e*i)/2,
    p_e = (1+e*i)/2,

which is the component retained by D(Delta); the d0 component is not
silently inverted.  Six seven-by-seven determinants are accumulated directly
as sparse B,C polynomials over A_e.  Their coefficient vectors are then
replayed independently in an exact Gaussian-rational RREF system.  The
certificate searches only multipliers of BC-degree at most one and a-degree at
most three.  The expected shape is 158 rows by 144 multiplier columns, with
rank 140 and the same rank after adjoining B or C.

The script is an exact, scoped audit of this offset-chart certificate.  It is
not a proof of the Krenn--Gu conjecture, of arbitrary H4/Q6 points, or of any
global source/graph statement.  The global status remains UNRESOLVED.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from fractions import Fraction

import sympy as sp


B, C = sp.symbols("B C")
q = sp.symbols("q")
a = sp.symbols("a", real=True)
p = sp.symbols("p")
I = sp.I


# These supports are a literal copy of the GLD71 sparse annihilator rows used
# by the six GLD97 selections.  Each item is ((root,leaf_1,leaf_2,leaf_3),c).
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


# Official six seven-by-seven selections, all zero-based in the 37-by-9
# syndrome matrix.  The first four are bordered pivot residuals; D0,D2 are
# direct rank-seven detectors.
MINORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}
PIVOT_ROWS = (0, 1, 2, 17, 25, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)


# These immutable hashes make a later run fail closed if the copied inputs or
# arithmetic path changes.
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
EXPECTED_RANK_SIGNATURE = {"rows": 158, "columns": 144, "rank": 140}


def clean(expression: sp.Expr) -> sp.Expr:
    """Canonical enough exact simplification for QQ(i)[a] coefficients."""

    # Pair arithmetic below is polynomial arithmetic in a.  Calling cancel on
    # every addition/multiplication makes the sparse determinant needlessly
    # reconstruct rational-function domains; cancellation is reserved for
    # displayed input coordinates and final hash/field conversions.
    return sp.expand(expression)


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


def q6_polynomial(p_value: sp.Expr, q_value: sp.Expr) -> sp.Expr:
    """Literal GLD96 Q6 polynomial in p,q."""

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


def h4_family(p_value: sp.Expr, q_value: sp.Expr, a_value: sp.Expr) -> dict[str, sp.Expr]:
    """Literal transcription of the written GLD88 F88 coordinates."""

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
    kernel_denominator = (p_value - q_value) * d0**3
    u_numerator = (q_value**2 - q_value + 1) * (
        2 * p_value * q_value - p_value + q_value**2 - 2 * q_value
    )
    v_numerator = -(p_value**2 - p_value + 1) * (
        p_value**2 + 2 * p_value * q_value - 2 * p_value - q_value
    )
    return {
        "s": sp.cancel((p_value + q_value - p_value * q_value) / d0),
        "b": sp.cancel(-b_numerator / ((p_value**2 - p_value + 1) * e)),
        "c": sp.cancel(-c_numerator / (d0 * e)),
        "u": sp.cancel(u_numerator / kernel_denominator),
        "v": sp.cancel(v_numerator / kernel_denominator),
        "d0": d0,
        "P": p_value**2 - p_value + 1,
        "e": e,
        "Delta": (p_value - q_value) * d0 * (p_value**2 - p_value + 1)
        * (p_value**2 + 2 * p_value * q_value - 2 * p_value - q_value)
        * (2 * p_value * q_value - p_value + q_value**2 - 2 * q_value) * e,
    }


Pair = tuple[sp.Expr, sp.Expr]


class QuadraticQuotient:
    """Exact QQ(i)[a]-coefficient quotient by the H2 quadratic k_e."""

    def __init__(self, epsilon: int) -> None:
        self.epsilon = epsilon
        self.p_value = (1 + epsilon * I) / 2
        self.k = sp.expand(
            q**2 - (1 + epsilon * I) * q + (3 + epsilon * I) / 2
        )
        # q^2 = r0 + r1*q in the monic quotient.
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
        return (clean(left[0] + right[0]), clean(left[1] + right[1]))

    def neg(self, value: Pair) -> Pair:
        return (clean(-value[0]), clean(-value[1]))

    def sub(self, left: Pair, right: Pair) -> Pair:
        return self.add(left, self.neg(right))

    def mul(self, left: Pair, right: Pair) -> Pair:
        return (
            clean(left[0] * right[0] + left[1] * right[1] * self.r0),
            clean(
                left[0] * right[1]
                + left[1] * right[0]
                + left[1] * right[1] * self.r1
            ),
        )

    def power(self, value: Pair, exponent: int) -> Pair:
        result = self.one
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exponent >>= 1
        return result

    def reduce_polynomial(self, expression: sp.Expr) -> Pair:
        polynomial = sp.Poly(sp.expand(expression), q)
        result = self.zero
        for exponent in range(int(polynomial.degree()), -1, -1):
            coefficient = polynomial.nth(exponent)
            if coefficient.has(q):
                raise AssertionError("q coefficient did not normalize")
            result = self.add(self.mul(result, self.q), (coefficient, 0))
        return result

    def inverse(self, value: Pair) -> Pair:
        # q -> r1-q is the quadratic conjugation.  The product is a scalar
        # norm, so this inversion introduces no q- or a-dependent denominator.
        conjugate = (clean(value[0] + value[1] * self.r1), clean(-value[1]))
        product = self.mul(value, conjugate)
        if clean(product[1]) != 0:
            raise AssertionError(("quadratic norm has q part", product))
        norm = clean(product[0])
        if norm == 0 or norm.has(a):
            raise AssertionError(("nonunit quotient denominator", value, norm))
        return (clean(conjugate[0] / norm), clean(conjugate[1] / norm))

    def from_expr(self, expression: sp.Expr, label: str = "") -> Pair:
        expression = sp.cancel(expression)
        numerator, denominator = expression.as_numer_denom()
        if denominator.has(B, C, a):
            raise AssertionError(("displayed-variable denominator", label, denominator))
        self.denominators.append((label, sp.factor(denominator)))
        numerator_pair = self.reduce_polynomial(numerator)
        denominator_pair = self.reduce_polynomial(denominator)
        return self.mul(numerator_pair, self.inverse(denominator_pair))

    def quotient_remainder(self, expression: sp.Expr) -> sp.Expr:
        return sp.rem(sp.Poly(sp.expand(expression), q), sp.Poly(self.k, q)).as_expr()


class BCPolynomial:
    """Sparse polynomial in B,C over a quadratic quotient."""

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


def direct_rows(
    algebra: QuadraticQuotient,
    leaf: list[list[BCPolynomial]],
    rows: tuple[int, ...],
) -> dict[int, list[BCPolynomial]]:
    """Accumulate syndrome rows directly from the copied sparse supports."""

    result: dict[int, list[BCPolynomial]] = {}
    zero = BCPolynomial(algebra)
    for relation_row in rows:
        entries: list[BCPolynomial] = []
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
                    total = total + BCPolynomial.constant(
                        algebra, algebra.from_expr(sp.Integer(coefficient), "support coefficient")
                    ) * term
                entries.append(total)
        result[relation_row] = entries
    return result


def direct_determinant(matrix: list[list[BCPolynomial]]) -> BCPolynomial:
    """Seven-by-seven determinant by exact sparse subset accumulation."""

    size = len(matrix)
    algebra = matrix[0][0].algebra
    zero = BCPolynomial(algebra)
    one = BCPolynomial.constant(algebra, algebra.one)
    states: dict[int, BCPolynomial] = {0: one}
    for _row in range(size):
        next_states: dict[int, BCPolynomial] = {}
        for mask, value in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                # Number of unchosen columns preceding the new column is the
                # Laplace sign for the row-by-row assignment.
                available_before = sum(
                    1 for previous in range(column) if not (mask & (1 << previous))
                )
                term = value * matrix[_row][column]
                if available_before & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = next_states.get(new_mask, zero) + term
        states = next_states
    return states[(1 << size) - 1]


def evaluate_bc(polynomial: BCPolynomial, b_value: int, c_value: int, a_value: int) -> Pair:
    result = polynomial.algebra.zero
    for (b_degree, c_degree), coefficient in polynomial.terms.items():
        scalar = b_value**b_degree * c_value**c_degree
        value = (
            clean(coefficient[0].subs(a, a_value) * scalar),
            clean(coefficient[1].subs(a, a_value) * scalar),
        )
        result = polynomial.algebra.add(result, value)
    return result


def bareiss_determinant(matrix: list[list[Pair]], algebra: QuadraticQuotient) -> Pair:
    """Fraction-free Bareiss replay after one exact B,C,a specialization.

    The coefficient ring A_e is a field (k_e is irreducible over QQ(i)), so
    the usual Bareiss quotient by the previous pivot is an exact unit
    division.  This is used only as a cross-check of each seven-minor; the
    symbolic determinants themselves come from the independent sparse
    accumulator above.
    """

    size = len(matrix)
    work = [[value for value in row] for row in matrix]
    sign = 1
    previous = algebra.one
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size) if not algebra.equal(work[row][pivot_index], algebra.zero)),
            None,
        )
        if pivot_row is None:
            return algebra.zero
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
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


def make_leaf(algebra: QuadraticQuotient, family: dict[str, sp.Expr]) -> list[list[BCPolynomial]]:
    one = BCPolynomial.constant(algebra, algebra.one)
    leaf = [
        [one, one, one],
        [BCPolynomial.constant(algebra, algebra.from_expr(algebra.p_value, "p")),
         BCPolynomial.constant(algebra, algebra.q),
         BCPolynomial.constant(algebra, algebra.from_expr(family["s"], "s denominator"))],
        [BCPolynomial.constant(algebra, algebra.from_expr(a, "a")), one, one],
    ]
    b88 = algebra.from_expr(1 + family["b"], "1+b88 denominator")
    c88 = algebra.from_expr(1 + family["c"], "1+c88 denominator")
    leaf[2][1] = BCPolynomial.constant(algebra, b88) + BCPolynomial.variable(algebra, (1, 0))
    leaf[2][2] = BCPolynomial.constant(algebra, c88) + BCPolynomial.variable(algebra, (0, 1))
    return leaf


def canonical_scalar(value: sp.Expr) -> list[str]:
    value = clean(value)
    real, imaginary = value.as_real_imag()
    real = sp.Rational(real)
    imaginary = sp.Rational(imaginary)
    return [str(real), str(imaginary)]


def polynomial_payload(value: sp.Expr) -> list[list[str]]:
    value = clean(value)
    if value == 0:
        return []
    polynomial = sp.Poly(sp.expand(value), a, extension=I)
    return [canonical_scalar(polynomial.nth(index)) for index in range(int(polynomial.degree()) + 1)]


def generator_payload(polynomial: BCPolynomial) -> list[list[object]]:
    payload: list[list[object]] = []
    for (b_degree, c_degree), (constant, q_coefficient) in sorted(polynomial.terms.items()):
        payload.append([
            b_degree,
            c_degree,
            polynomial_payload(constant),
            polynomial_payload(q_coefficient),
        ])
    return payload


def payload_hash(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()


def gaussian_fraction(value: sp.Expr) -> tuple[Fraction, Fraction]:
    value = clean(value)
    real, imaginary = value.as_real_imag()
    real = sp.Rational(real)
    imaginary = sp.Rational(imaginary)
    return (Fraction(int(real.p), int(real.q)), Fraction(int(imaginary.p), int(imaginary.q)))


GScalar = tuple[Fraction, Fraction]
GZERO: GScalar = (Fraction(0), Fraction(0))
GONE: GScalar = (Fraction(1), Fraction(0))


def g_add(left: GScalar, right: GScalar) -> GScalar:
    return (left[0] + right[0], left[1] + right[1])


def g_neg(value: GScalar) -> GScalar:
    return (-value[0], -value[1])


def g_sub(left: GScalar, right: GScalar) -> GScalar:
    return g_add(left, g_neg(right))


def g_mul(left: GScalar, right: GScalar) -> GScalar:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def g_inverse(value: GScalar) -> GScalar:
    norm = value[0] * value[0] + value[1] * value[1]
    if norm == 0:
        raise ZeroDivisionError("zero Gaussian-rational pivot")
    return (value[0] / norm, -value[1] / norm)


def rref(matrix: list[list[GScalar]]) -> tuple[list[list[GScalar]], tuple[int, ...]]:
    """Exact RREF over Q(i), used for both rank and explicit certificates."""

    work = [[*row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if row_count else 0
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(pivot_row, row_count) if work[index][column] != GZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = g_inverse(work[pivot_row][column])
        work[pivot_row] = [g_mul(value, inverse) for value in work[pivot_row]]
        for index in range(row_count):
            if index == pivot_row or work[index][column] == GZERO:
                continue
            multiplier = work[index][column]
            work[index] = [
                g_sub(left, g_mul(multiplier, right))
                for left, right in zip(work[index], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, tuple(pivots)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def certificate_hash(solution: list[GScalar]) -> str:
    payload = [[fraction_text(real), fraction_text(imaginary)] for real, imaginary in solution]
    return payload_hash(payload)


def conjugate_solution(solution: list[GScalar]) -> list[GScalar]:
    return [(real, -imaginary) for real, imaginary in solution]


def conjugate_payload(payload: list[list[object]]) -> list[list[object]]:
    """Conjugate a canonical generator payload without re-expanding symbols."""

    result: list[list[object]] = []
    for b_degree, c_degree, constant_payload, q_payload in payload:
        def conjugate_coefficients(coefficients: list[list[str]]) -> list[list[str]]:
            return [
                [real, str(-sp.Rational(imaginary))]
                for real, imaginary in coefficients
            ]

        result.append([
            b_degree,
            c_degree,
            conjugate_coefficients(constant_payload),
            conjugate_coefficients(q_payload),
        ])
    return result


def matrix_vector(matrix: list[list[GScalar]], vector: list[GScalar]) -> list[GScalar]:
    values: list[GScalar] = []
    for row in matrix:
        total = GZERO
        for left, right in zip(row, vector, strict=True):
            total = g_add(total, g_mul(left, right))
        values.append(total)
    return values


def build_multiplier_system(
    algebra: QuadraticQuotient,
    generators: dict[str, BCPolynomial],
) -> tuple[list[tuple[int, int, int, int]], list[list[GScalar]], dict[str, list[GScalar]]]:
    """Build 158x144 coefficient system for polynomial multipliers."""

    bc_monomials = ((0, 0), (1, 0), (0, 1))
    q_monomials = (algebra.one, algebra.q)
    columns: list[dict[tuple[int, int, int, int], sp.Expr]] = []
    for name in MINORS:
        polynomial = generators[name]
        for multiplier_b, multiplier_c in bc_monomials:
            for multiplier_a in range(4):
                for multiplier_q, q_multiplier in enumerate(q_monomials):
                    column: dict[tuple[int, int, int, int], sp.Expr] = {}
                    for (base_b, base_c), coefficient in polynomial.terms.items():
                        product = algebra.mul(coefficient, q_multiplier)
                        for q_degree, component in enumerate(product):
                            component = clean(component * a**multiplier_a)
                            if component == 0:
                                continue
                            component_poly = sp.Poly(sp.expand(component), a, extension=I)
                            for a_degree in range(int(component_poly.degree()) + 1):
                                scalar = clean(component_poly.nth(a_degree))
                                if scalar == 0:
                                    continue
                                key = (
                                    base_b + multiplier_b,
                                    base_c + multiplier_c,
                                    a_degree,
                                    q_degree,
                                )
                                column[key] = clean(column.get(key, 0) + scalar)
                    columns.append(column)
    if len(columns) != 6 * 3 * 4 * 2:
        raise AssertionError(("unexpected multiplier column count", len(columns)))
    support = sorted({key for column in columns for key, value in column.items() if value != 0})
    for target_key in ((1, 0, 0, 0), (0, 1, 0, 0)):
        if target_key not in support:
            raise AssertionError(("target coefficient row missing", target_key))
    matrix: list[list[GScalar]] = []
    for key in support:
        matrix.append([
            gaussian_fraction(column.get(key, 0)) for column in columns
        ])
    targets: dict[str, list[GScalar]] = {}
    for name, key in (("B", (1, 0, 0, 0)), ("C", (0, 1, 0, 0))):
        targets[name] = [GONE if row_key == key else GZERO for row_key in support]
    return support, matrix, targets


def membership_certificate(
    matrix: list[list[GScalar]],
    targets: dict[str, list[GScalar]],
) -> dict[str, object]:
    base_rref, base_pivots = rref(matrix)
    base_rank = len(base_pivots)
    result: dict[str, object] = {
        "rows": len(matrix),
        "columns": len(matrix[0]),
        "rank": base_rank,
        "targets": {},
        "_solutions": {},
    }
    if (len(matrix), len(matrix[0]), base_rank) != (
        EXPECTED_RANK_SIGNATURE["rows"],
        EXPECTED_RANK_SIGNATURE["columns"],
        EXPECTED_RANK_SIGNATURE["rank"],
    ):
        raise AssertionError(("unexpected base rank signature", result))
    for name, target in targets.items():
        augmented = [row + [value] for row, value in zip(matrix, target, strict=True)]
        augmented_rref, augmented_pivots = rref(augmented)
        augmented_rank = len(augmented_pivots)
        if augmented_rank != base_rank or (len(augmented_pivots) and augmented_pivots[-1] == len(matrix[0])):
            raise AssertionError(("target not in multiplier span", name, base_rank, augmented_rank))
        solution = [GZERO for _ in range(len(matrix[0]))]
        for row_index, pivot_column in enumerate(augmented_pivots):
            if pivot_column >= len(matrix[0]):
                raise AssertionError(("augmented target pivot", name, pivot_column))
            solution[pivot_column] = augmented_rref[row_index][-1]
        residual = matrix_vector(matrix, solution)
        if residual != target:
            raise AssertionError(("RREF certificate residual", name))
        result["targets"][name] = {
            "augmented_rank": augmented_rank,
            "membership": True,
            "certificate_hash": certificate_hash(solution),
            "nonzero_multiplier_coefficients": sum(value != GZERO for value in solution),
            "residual_zero": True,
        }
        result["_solutions"][name] = solution
    return result


def bareiss_2x2(left: Pair, right: Pair, lower: Pair, upper: Pair, algebra: QuadraticQuotient) -> Pair:
    """Fraction-free Bareiss base case used as an independent quotient control."""

    return algebra.sub(algebra.mul(left, right), algebra.mul(lower, upper))


def gate_report(epsilon: int, algebra: QuadraticQuotient) -> dict[str, object]:
    p_value = algebra.p_value
    d0 = p_value + q - 1
    P = p_value**2 - p_value + 1
    L1 = p_value**2 + 2 * p_value * q - 2 * p_value - q
    L2 = 2 * p_value * q - p_value + q**2 - 2 * q
    e = 2 * p_value * q**2 - 2 * p_value * q - p_value - q**2 - 2 * q + 2
    factors = {
        "p_minus_q": p_value - q,
        "d0": d0,
        "P": P,
        "L1": L1,
        "L2": L2,
        "e": e,
    }
    expected = {
        "p_minus_q": sp.Rational(3, 2),
        "d0": sp.Rational(1, 2),
        "P": sp.Rational(1, 4),
        "L1": sp.Rational(3, 4),
        "L2": sp.Integer(3),
        "e": sp.Integer(8),
    }
    resultants = {
        name: clean(sp.resultant(algebra.k, factor, q))
        for name, factor in factors.items()
    }
    if resultants != expected:
        raise AssertionError(("gate resultant mismatch", epsilon, resultants))
    inverses: dict[str, bool] = {}
    for name, factor in factors.items():
        value = algebra.from_expr(factor, f"gate {name}")
        inverse = algebra.inverse(value)
        inverses[name] = algebra.equal(algebra.mul(value, inverse), algebra.one)
        if not inverses[name]:
            raise AssertionError(("gate inverse mismatch", name))
    delta = sp.prod(factors.values())
    delta_resultant = clean(sp.resultant(algebra.k, delta, q))
    if delta_resultant != sp.Rational(27, 8):
        raise AssertionError(("Delta resultant mismatch", delta_resultant))
    if not sp.Poly(algebra.k, q, extension=I).is_irreducible:
        raise AssertionError(("H2 quadratic is not irreducible over QQ(i)", epsilon))
    q6_branch = sp.expand(q6_polynomial(p_value, q))
    if algebra.quotient_remainder(q6_branch) != 0:
        raise AssertionError(("Q6 does not vanish in k quotient", epsilon))
    return {
        "epsilon": epsilon,
        "p": str(p_value),
        "k": str(algebra.k),
        "k_discriminant": str(sp.discriminant(algebra.k, q)),
        "q6_degree_before_k_reduction": sp.Poly(q6_branch, q).degree(),
        "Delta_factors": list(factors),
        "resultants": {name: str(value) for name, value in resultants.items()},
        "Delta_resultant": str(delta_resultant),
        "all_gate_units_in_A_e": all(inverses.values()),
        "d0_component_explicitly_excluded": True,
        "detG_or_other_parameter_inverted": False,
        "H2": str(clean(2 * p_value**2 - 2 * p_value + 1)),
    }


def denominator_report(
    algebra: QuadraticQuotient,
    family: dict[str, sp.Expr],
) -> dict[str, object]:
    """Verify that every displayed input denominator is a declared gate.

    The determinant accumulator performs no division.  Its only divisions are
    the inverses used by ``from_expr`` for the three F88 coordinates and the
    copied gate checks.  This report rejects a new irreducible q-factor, any
    a/B/C denominator, and any nonunit factor modulo k.
    """

    p_value = algebra.p_value
    gate_factors = [
        p_value - q,
        p_value + q - 1,
        p_value**2 - p_value + 1,
        p_value**2 + 2 * p_value * q - 2 * p_value - q,
        2 * p_value * q - p_value + q**2 - 2 * q,
        2 * p_value * q**2 - 2 * p_value * q - p_value - q**2 - 2 * q + 2,
    ]
    expected_coordinate_denominators = {
        "s": p_value + q - 1,
        "b": (p_value**2 - p_value + 1)
        * (2 * p_value * q**2 - 2 * p_value * q - p_value - q**2 - 2 * q + 2),
        "c": (p_value + q - 1)
        * (2 * p_value * q**2 - 2 * p_value * q - p_value - q**2 - 2 * q + 2),
    }
    coordinate_checks: dict[str, bool] = {}
    for name, expected in expected_coordinate_denominators.items():
        actual = sp.cancel(family[name]).as_numer_denom()[1]
        quotient = sp.cancel(actual / expected)
        coordinate_checks[name] = quotient != 0 and not quotient.has(q, a, B, C)
        if not coordinate_checks[name]:
            raise AssertionError(("unexpected F88 denominator", name, actual, expected))

    known_gate_polynomials = [sp.Poly(sp.expand(factor), q, extension=I) for factor in gate_factors]
    unknown_factors: list[str] = []
    for label, denominator in algebra.denominators:
        if denominator.has(a, B, C):
            raise AssertionError(("displayed-variable denominator", label, denominator))
        denominator_poly = sp.Poly(sp.expand(denominator), q, extension=I)
        _unit, irreducibles = sp.factor_list(denominator_poly.as_expr(), extension=I)
        for factor, _multiplicity in irreducibles:
            factor_poly = sp.Poly(factor, q, extension=I)
            if factor_poly.degree() == 0:
                continue
            if not any(sp.gcd(factor_poly, gate).degree() > 0 for gate in known_gate_polynomials):
                unknown_factors.append(str(factor))
            common = sp.gcd(denominator_poly, sp.Poly(algebra.k, q, extension=I))
            if common.degree() != 0:
                raise AssertionError(("recorded denominator is not a k-unit", label, denominator, common))
    if unknown_factors:
        raise AssertionError(("unlisted denominator factors", sorted(set(unknown_factors))))
    return {
        "coordinate_denominators_match_F88": coordinate_checks,
        "recorded_denominators": len(algebra.denominators),
        "all_factors_in_declared_Delta": True,
        "all_recorded_denominators_k_units": True,
        "no_a_B_C_denominators": True,
    }


def common_h2_report() -> dict[str, object]:
    W = (
        2 * p**2 * q**2 - 2 * p**2 * q + p**2
        + 2 * p * q**3 - 5 * p * q**2 + 3 * p * q - p
        + 2 * q**4 - 5 * q**3 + 7 * q**2 - 4 * q + 2
    )
    d0 = p + q - 1
    K = (sp.Rational(1, 2) - p) * q**2 + (p - 1) * q + 1 - sp.Rational(3, 2) * p
    identity = clean(q6_polynomial(p, q) - d0 * K - (2 * p**2 - 2 * p + 1) * W / 2)
    if identity != 0:
        raise AssertionError(("H2 factor identity mismatch", identity))
    return {
        "H2": "2*p**2 - 2*p + 1",
        "identity": "Q6 - d0*K = H2*W/2",
        "K": str(K),
        "W": str(W),
        "branch_degree": 3,
        "d0_not_inverted_in_Q6": True,
    }


def run_branch(epsilon: int) -> dict[str, object]:
    started = time.monotonic()
    algebra = QuadraticQuotient(epsilon)
    gate = gate_report(epsilon, algebra)
    print(f"[epsilon={epsilon}] gate checks complete", file=sys.stderr, flush=True)
    family = h4_family(algebra.p_value, q, a)
    leaf = make_leaf(algebra, family)
    required_rows = tuple(sorted({row for rows, _columns in MINORS.values() for row in rows}))
    rows = direct_rows(algebra, leaf, required_rows)
    denominator = denominator_report(algebra, family)
    print(f"[epsilon={epsilon}] syndrome accumulation complete", file=sys.stderr, flush=True)
    generators: dict[str, BCPolynomial] = {}
    bareiss_controls: dict[str, bool] = {}
    for name, (selected_rows, selected_columns) in MINORS.items():
        matrix = [[rows[row][column] for column in selected_columns] for row in selected_rows]
        generators[name] = direct_determinant(matrix)
        specialized_matrix = [
            [
                evaluate_bc(matrix[row_index][column_index], 2, 3, 5)
                for column_index in range(len(selected_columns))
            ]
            for row_index in range(len(selected_rows))
        ]
        direct_value = evaluate_bc(generators[name], 2, 3, 5)
        bareiss_controls[name] = algebra.equal(
            bareiss_determinant(specialized_matrix, algebra), direct_value
        )
        if not bareiss_controls[name]:
            raise AssertionError(("Bareiss seven-minor control mismatch", epsilon, name))
        for (b_degree, c_degree), pair in generators[name].terms.items():
            for coefficient in pair:
                if sp.denom(clean(coefficient)).has(a):
                    raise AssertionError(("determinant coefficient localized in a", name, b_degree, c_degree))
                sp.Poly(sp.expand(coefficient), a, extension=I)
        print(f"[epsilon={epsilon}] {name} determinant complete", file=sys.stderr, flush=True)

    # Exact six-minor hashes are over the reduced A_e[B,C] representatives.
    generator_payloads = {
        name: generator_payload(polynomial)
        for name, polynomial in generators.items()
    }
    generator_hashes = {
        name: payload_hash(generator_payloads[name])
        for name in generators
    }
    expected_hashes = EXPECTED_GENERATOR_HASHES[epsilon]
    if any(expected_hashes[name] != value for name, value in generator_hashes.items()):
        raise AssertionError(("pinned generator hash mismatch", epsilon, generator_hashes))

    support, matrix, targets = build_multiplier_system(algebra, generators)
    print(f"[epsilon={epsilon}] multiplier matrix {len(support)}x{len(matrix[0])}", file=sys.stderr, flush=True)
    membership = membership_certificate(matrix, targets)
    print(f"[epsilon={epsilon}] RREF membership complete", file=sys.stderr, flush=True)
    certificate_solutions = membership.pop("_solutions")
    expected_certificates = EXPECTED_CERTIFICATE_HASHES[epsilon]
    for name in ("B", "C"):
        actual = membership["targets"][name]["certificate_hash"]
        if expected_certificates[name] != actual:
            raise AssertionError(("pinned certificate hash mismatch", epsilon, name, actual))

    # Small exact Bareiss base case: the same quotient multiplication used by
    # the 7x7 direct accumulator agrees with the fraction-free 2x2 identity.
    bareiss_control = bareiss_2x2(algebra.q, algebra.q, algebra.one, algebra.one, algebra)
    direct_control = BCPolynomial.constant(algebra, algebra.q) * BCPolynomial.constant(algebra, algebra.q) - (
        BCPolynomial.constant(algebra, algebra.one) * BCPolynomial.constant(algebra, algebra.one)
    )
    if not algebra.equal(bareiss_control, direct_control.terms[(0, 0)]):
        raise AssertionError(("Bareiss quotient control mismatch", epsilon))

    conjugated_denominators = [
        (label, clean(sp.conjugate(value))) for label, value in algebra.denominators
    ]
    return {
        "epsilon": epsilon,
        "p": str(algebra.p_value),
        "gate": gate,
        "denominator_audit": denominator,
        "family_denominator_count": len(algebra.denominators),
        "family_denominators_have_no_a_B_C": all(
            not value.has(a, B, C) for _label, value in algebra.denominators
        ),
        "all_recorded_q_denominators_are_units": all(
            sp.degree(sp.gcd(sp.Poly(algebra.k, q, extension=I), sp.Poly(value, q, extension=I)), q) == 0
            for _label, value in algebra.denominators
        ),
        "conjugated_denominator_count": len(conjugated_denominators),
        "minor_hashes": generator_hashes,
        "minor_support": {
            name: {
                "bc_terms": len(polynomial.terms),
                "bc_total_degree": max((sum(exponent) for exponent in polynomial.terms), default=None),
                "a_degree": max(
                    (
                        int(sp.Poly(sp.expand(component), a, extension=I).degree())
                        for pair in polynomial.terms.values()
                        for component in pair
                        if component != 0
                    ),
                    default=None,
                ),
            }
            for name, polynomial in generators.items()
        },
        "multiplier_system": {
            "rows": len(support),
            "columns": len(matrix[0]),
            "support_key_order": "sorted(B_degree,C_degree,a_degree,q_basis_degree)",
            "multiplier_bc_degree_max": 1,
            "multiplier_a_degree_max": 3,
            "q_basis_dimension": 2,
            "rank": membership["rank"],
            "targets": membership["targets"],
        },
        "bareiss_specialization_controls": bareiss_controls,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "_generator_payloads": generator_payloads,
        "_certificate_solutions": certificate_solutions,
    }


def main() -> int:
    started = time.monotonic()
    if support_digest() != EXPECTED_SUPPORT_DIGEST:
        raise SystemExit("copied sparse-support digest mismatch")
    common = common_h2_report()
    branches = [run_branch(1), run_branch(-1)]
    plus_payloads = branches[0].pop("_generator_payloads")
    minus_payloads = branches[1].pop("_generator_payloads")
    plus_certificates = branches[0].pop("_certificate_solutions")
    minus_certificates = branches[1].pop("_certificate_solutions")
    for name in MINORS:
        if minus_payloads[name] != conjugate_payload(plus_payloads[name]):
            raise AssertionError(("minus generator is not conjugate of plus generator", name))
    for name in ("B", "C"):
        if minus_certificates[name] != conjugate_solution(plus_certificates[name]):
            raise AssertionError(("minus certificate is not conjugate of plus certificate", name))
    output = {
        "status": "exact_scoped_H2_degree_drop_offset_membership_audit",
        "global_status": "UNRESOLVED",
        "scope": (
            "H2=0 degree-drop component of the normalized GLD88/F88 H4 Q6 "
            "offset chart on D(Delta), both QQ(i) quadratic branches; "
            "six GLD97 seven-minors and uniform symbolic a"
        ),
        "provenance": {
            "support_rows": list(SUPPORT_ROWS),
            "support_digest_sha256": support_digest(),
            "pivot_rows": list(PIVOT_ROWS),
            "pivot_columns": list(PIVOT_COLUMNS),
            "minor_selections": {
                name: {"rows": list(rows), "columns": list(columns)}
                for name, (rows, columns) in MINORS.items()
            },
            "construction": "literal copied supports/formulas; direct sparse determinant; local quotient and Gaussian-rational RREF",
            "forbidden_imports": ["primary verifier", "GLD71", "GLD88", "GLD96", "GLD98 exploratory census"],
        },
        "h2_factorization": common,
        "branches": branches,
        "conjugation": {
            "both_signs_computed_independently": True,
            "coefficient_field": "QQ(i)",
            "generator_payloads_conjugate": True,
            "certificate_vectors_conjugate": True,
            "note": "The minus branch is separately accumulated and RREF-checked; coefficientwise conjugation is an additional cross-check, not a substitute computation.",
        },
        "nonclaims": [
            "No arbitrary-p or arbitrary-H4/Q6 closure is claimed.",
            "No assertion is made for the d0 component of Q6; d0 is excluded by D(Delta), not inverted in QQ(i)[q]/(Q6).",
            "No E31, g0, det(G), source-integrability, graph-lift, or global Krenn--Gu conclusion is claimed.",
            "This exact computational certificate remains a scoped proof leaf pending its mathematical bridge and adversarial consolidation.",
        ],
        "runtime": {
            "seconds": round(time.monotonic() - started, 3),
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    print("H2 degree-drop six-minor membership audit: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
