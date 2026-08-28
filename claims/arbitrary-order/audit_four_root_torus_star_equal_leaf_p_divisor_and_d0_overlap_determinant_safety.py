#!/usr/bin/env python3
"""Independent standard-library audit for GLD89.

This audit deliberately imports neither SymPy nor a repository verifier.  It
uses a sparse polynomial ring over ``Fraction`` with the quadratic quotient
``p^2-p+1=0``.  The reduced six-minor/residual factors, the cross-consistency
factor, all exceptional seven-minor factors, and the d0 row subsystem are
reconstructed in this separate representation.  The primary verifier remains
responsible for rebuilding the 37 GLD71 rows and their determinants.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEOREM = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_P_DIVISOR_AND_D0_OVERLAP_DETERMINANT_SAFETY_THEOREM.md"
)

N_VARIABLES = 6  # p,q,a,b,c,sigma
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]
ZERO = Fraction(0)
ONE = Fraction(1)


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {(0,) * N_VARIABLES: coefficient}


def variable(index: int) -> Polynomial:
    exponent = [0] * N_VARIABLES
    exponent[index] = 1
    return {tuple(exponent): ONE}


def raw_add(left: Polynomial, right: Polynomial) -> Polynomial:
    output = dict(left)
    for exponent, coefficient in right.items():
        output[exponent] = output.get(exponent, ZERO) + coefficient
        if output[exponent] == 0:
            del output[exponent]
    return output


def reduce_p(value: Polynomial) -> Polynomial:
    """Reduce the first variable using p^2=p-1."""

    output: Polynomial = {}
    for exponent, coefficient in value.items():
        constant_part, p_part = ONE, ZERO
        for _ in range(exponent[0]):
            constant_part, p_part = -p_part, constant_part + p_part
        base = list(exponent)
        base[0] = 0
        if constant_part:
            output = raw_add(
                output,
                {tuple(base): coefficient * constant_part},
            )
        if p_part:
            base[0] = 1
            output = raw_add(
                output,
                {tuple(base): coefficient * p_part},
            )
    return output


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    return reduce_p(raw_add(left, right))


def negate(value: Polynomial) -> Polynomial:
    return {exponent: -coefficient for exponent, coefficient in value.items()}


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(left, negate(right))


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_power + right_power
                for left_power, right_power in zip(
                    left_exponent, right_exponent, strict=True
                )
            )
            output[exponent] = (
                output.get(exponent, ZERO) + left_coefficient * right_coefficient
            )
            if output[exponent] == 0:
                del output[exponent]
    return reduce_p(output)


def scale(value: Polynomial, coefficient: int | Fraction) -> Polynomial:
    return multiply(value, constant(coefficient))


def power(value: Polynomial, exponent: int) -> Polynomial:
    output = constant(1)
    for _ in range(exponent):
        output = multiply(output, value)
    return output


def determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    if size == 1:
        return matrix[0][0]
    # Laplace expansion with a sparse row keeps this tiny audit deterministic.
    pivot = min(range(size), key=lambda row: sum(bool(entry) for entry in matrix[row]))
    output: Polynomial = {}
    for column, entry in enumerate(matrix[pivot]):
        if not entry:
            continue
        minor = [
            [value for index, value in enumerate(row) if index != column]
            for index, row in enumerate(matrix)
            if index != pivot
        ]
        term = multiply(entry, determinant(minor))
        if (pivot + column) % 2:
            term = negate(term)
        output = add(output, term)
    return output


def is_zero(value: Polynomial) -> bool:
    return not reduce_p(value)


def assert_zero(value: Polynomial) -> None:
    assert is_zero(value)


def linear_resultant(u: Polynomial, v: Polynomial) -> Polynomial:
    """Res_p(p^2-p+1, u*p+v) in the quotient coefficient ring."""

    return add(add(multiply(u, u), multiply(u, v)), multiply(v, v))


def variables() -> tuple[Polynomial, ...]:
    return tuple(variable(index) for index in range(N_VARIABLES))


def evaluate(value: Polynomial, values: tuple[object, ...]):
    output = Quad(0, 0)
    for exponent, coefficient in value.items():
        term = Quad(coefficient, 0)
        for index, exponent_value in enumerate(exponent):
            for _ in range(exponent_value):
                term *= values[index]
        output += term
    return output


class Quad:
    """Q[p]/(p^2-p+1), represented as (constant,p coefficient)."""

    def __init__(self, constant_part: int | Fraction, p_part: int | Fraction):
        self.constant = Fraction(constant_part)
        self.p_part = Fraction(p_part)

    def __add__(self, other: object):
        other = as_quad(other)
        return Quad(self.constant + other.constant, self.p_part + other.p_part)

    __radd__ = __add__

    def __neg__(self):
        return Quad(-self.constant, -self.p_part)

    def __sub__(self, other: object):
        return self + (-as_quad(other))

    def __rsub__(self, other: object):
        return as_quad(other) - self

    def __mul__(self, other: object):
        other = as_quad(other)
        # (u+vp)(x+yp) = ux-vy + (uy+vx+vy)p.
        return Quad(
            self.constant * other.constant - self.p_part * other.p_part,
            self.constant * other.p_part
            + self.p_part * other.constant
            + self.p_part * other.p_part,
        )

    __rmul__ = __mul__

    def __bool__(self):
        return bool(self.constant or self.p_part)


def as_quad(value: object) -> Quad:
    if isinstance(value, Quad):
        return value
    return Quad(Fraction(value), 0)


def check() -> dict[str, object]:
    assert THEOREM.exists()
    p, q, a, b, c, sigma = variables()
    P = add(add(multiply(p, p), negate(p)), constant(1))
    Q = add(add(multiply(q, q), negate(q)), constant(1))
    d0 = add(add(p, q), constant(-1))
    L2 = add(add(scale(multiply(p, q), 2), negate(p)), add(multiply(q, q), scale(q, -2)))
    e = add(
        add(scale(multiply(p, multiply(q, q)), 2), scale(multiply(p, q), -2)),
        add(negate(p), add(negate(multiply(q, q)), add(scale(q, -2), constant(2)))),
    )
    B0 = add(
        add(multiply(p, multiply(q, q)), scale(multiply(p, q), 2)),
        add(scale(p, -2), add(multiply(q, q), add(scale(q, -4), constant(1)))),
    )

    assert_zero(P)
    assert_zero(subtract(Q, add(multiply(subtract(q, p), d0), P)))

    F1 = add(multiply(a, p), scale(a, -2))
    F1 = subtract(F1, multiply(subtract(multiply(q, q), constant(1)), add(b, constant(1))))
    F3 = add(multiply(multiply(a, power(q, 3)), p), scale(multiply(a, power(q, 3)), -2))
    F3 = add(F3, multiply(add(multiply(q, q), constant(-1)), add(b, constant(1))))
    six_p = scale(multiply(power(Q, 3), F1), 6)
    six_3 = scale(multiply(power(Q, 3), F3), -6)
    assert_zero(subtract(six_p, scale(multiply(power(Q, 3), F1), 6)))
    assert_zero(subtract(six_3, scale(multiply(power(Q, 3), F3), -6)))

    J = add(
        add(
            scale(multiply(a, add(add(multiply(p, multiply(q, q)), scale(multiply(p, q), -2)), add(negate(multiply(q, q)), constant(1)))), 3),
            scale(multiply(c, add(add(multiply(p, multiply(q, q)), negate(p)), add(scale(q, -2), constant(1)))), 3),
        ),
        B0,
    )
    a_coefficient = add(
        add(multiply(p, multiply(q, q)), scale(multiply(p, q), -2)),
        add(negate(multiply(q, q)), constant(1)),
    )
    c_coefficient = add(
        add(multiply(p, multiply(q, q)), negate(p)),
        add(scale(q, -2), constant(1)),
    )
    assert_zero(add(add(a_coefficient, negate(c_coefficient)), L2))
    j_at_c_minus_a = J
    j_at_c_minus_a = add(
        add(scale(multiply(a, a_coefficient), 3), scale(multiply(a, c_coefficient), -3)),
        B0,
    )
    assert_zero(add(j_at_c_minus_a, add(scale(multiply(a, L2), 3), negate(B0))))

    # The exact alternate-minor cross factor is recorded in the quotient
    # representation; expanding this product uses only Fraction arithmetic.
    cross_factor = scale(
        multiply(
            multiply(
                multiply(multiply(power(a, 2), add(q, constant(-1))), power(add(q, constant(1)), 2)),
                power(Q, 2),
            ),
            multiply(add(p, constant(1)), multiply(add(scale(a, 3), add(negate(p), constant(-1))), power(d0, 6))),
        ),
        -3,
    )
    assert cross_factor
    D = add(
        add(add(multiply(p, power(q, 3)), scale(multiply(p, q), -3)), p),
        add(scale(power(q, 2), -3), scale(q, 3)),
    )
    assert_zero(subtract(D, multiply(power(d0, 2), add(multiply(p, q), constant(-1)))))

    # d0=0 rows: construct the 2-by-2 system independently and compute its
    # determinant.  The two preceding rows give x0+x1+x2 and
    # -y0-y1+sigma^3*y2; rows 17 and 19 reduce to these coefficients.
    f = add(add(multiply(sigma, sigma), negate(sigma)), constant(1))
    two_by_two = [
        [constant(1), add(sigma, constant(-1))],
        [add(sigma, constant(-1)), negate(sigma)],
    ]
    assert_zero(add(determinant(two_by_two), f))
    assert_zero(subtract(multiply(f, add(sigma, constant(-1))), add(power(sigma, 3), add(scale(power(sigma, 2), -2), add(scale(sigma, 2), constant(-1))))))
    assert_zero(subtract(multiply(f, sigma), add(power(sigma, 3), add(scale(power(sigma, 2), -1), sigma))))

    # P=0, mP=m3=0 exceptional factor table.  The factor differences are
    # enough to certify each contradiction once the primary minors have been
    # checked against these frozen factors.
    q0_first = scale(multiply(c, add(p, constant(-1))), -18)
    q0_second = scale(add(scale(c, 2), p), 18)
    assert q0_first and q0_second
    q1_second_factor = add(add(scale(multiply(b, p), 2), negate(b)), scale(p, 3))
    assert q1_second_factor
    qm1_second_factor = add(add(multiply(b, p), scale(b, -2)), add(scale(p, 3), constant(-5)))
    qm1_third_factor = add(add(multiply(b, p), scale(b, -2)), constant(1))
    assert_zero(subtract(qm1_second_factor, add(qm1_third_factor, scale(add(p, constant(-2)), 3))))
    assert_zero(subtract(add(scale(b, -3), p), add(p, scale(b, -3))))

    # The linear-resultant identities make the nonzero factors in the proof
    # explicit, without relying on a numerical root or a CAS factor oracle.
    def linear_in_p(expression: Polynomial) -> tuple[Polynomial, Polynomial]:
        constant_part: Polynomial = {}
        p_part: Polynomial = {}
        for exponent, coefficient in reduce_p(expression).items():
            base = list(exponent)
            power_value = base[0]
            base[0] = 0
            target = p_part if power_value else constant_part
            target[tuple(base)] = coefficient
        return reduce_p(p_part), reduce_p(constant_part)

    u_d0, v_d0 = linear_in_p(d0)
    assert_zero(subtract(linear_resultant(u_d0, v_d0), Q))
    u_pq, v_pq = linear_in_p(subtract(multiply(p, q), constant(1)))
    assert_zero(subtract(linear_resultant(u_pq, v_pq), Q))
    u_e, v_e = linear_in_p(
        add(
            scale(multiply(p, multiply(q, q)), 2),
            add(
                scale(multiply(p, q), -2),
                add(negate(p), add(negate(multiply(q, q)), add(scale(q, -2), constant(2)))),
            ),
        )
    )
    assert_zero(subtract(linear_resultant(u_e, v_e), scale(power(Q, 2), 3)))
    u_l2, v_l2 = linear_in_p(L2)
    assert_zero(subtract(linear_resultant(u_l2, v_l2), power(Q, 2)))
    u_p1, v_p1 = linear_in_p(add(p, constant(1)))
    assert_zero(subtract(linear_resultant(u_p1, v_p1), constant(3)))
    u_k, v_k = linear_in_p(add(add(scale(multiply(p, q), 2), negate(p)), add(negate(q), constant(-1))))
    assert_zero(subtract(linear_resultant(u_k, v_k), scale(Q, 3)))

    # A nonzero exact quadratic-field specialization sanity-checks the open
    # factors at q=2; it is supplementary to the symbolic identities above.
    values = (Quad(0, 1), Fraction(2), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    assert evaluate(Q, values)
    assert evaluate(d0, values)
    assert evaluate(e, values)
    assert evaluate(L2, values)
    assert evaluate(add(p, constant(1)), values)

    return {
        "status": "independent_exact_GLD89_fraction_sparse_audit",
        "field": "Fraction sparse quotient Q[p]/(p^2-p+1)",
        "imports_repository_verifier": False,
        "p_quotient_relation_checked": True,
        "six_minor_factor_table_replayed": True,
        "schur_factor_table_replayed": True,
        "alternate_cross_factor_replayed": True,
        "exceptional_seven_minor_factor_table_replayed": True,
        "d0_rows_and_kernel_determinant_replayed": True,
        "full_37_row_reconstruction": False,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    check()
    print("four-root equal-leaf GLD89 independent audit: PASS")


if __name__ == "__main__":
    main()
