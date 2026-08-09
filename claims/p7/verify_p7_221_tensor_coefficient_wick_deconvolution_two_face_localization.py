"""Verify tensor-coefficient Wick localization for the formal 2+2+1 ledger.

This is a fixed seven-terminal squarefree-algebra check.  It performs no
support search, graph-family enumeration, or parameter sweep.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

TERMINALS = ("1", "2", "3", "4", "5", "a", "b")
FULL = (1 << len(TERMINALS)) - 1
Q = (1 << TERMINALS.index("a")) | (1 << TERMINALS.index("b"))
P_MINUS_Q = FULL ^ Q
Polynomial = dict[int, sp.Expr]


def add(*polynomials: Polynomial) -> Polynomial:
    """Add squarefree subset polynomials."""

    answer: Polynomial = {}
    for polynomial in polynomials:
        for subset, value in polynomial.items():
            answer[subset] = sp.expand(answer.get(subset, 0) + value)
    return {subset: value for subset, value in answer.items() if value != 0}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in K[x_i]/(x_i^2)."""

    answer: Polynomial = {}
    for left_subset, left_value in left.items():
        for right_subset, right_value in right.items():
            if left_subset & right_subset:
                continue
            subset = left_subset | right_subset
            answer[subset] = sp.expand(
                answer.get(subset, 0) + left_value * right_value
            )
    return {subset: value for subset, value in answer.items() if value != 0}


def terminal_matrix(prefix: str) -> sp.Matrix:
    """Return one generic hollow symmetric seven-terminal matrix."""

    matrix = sp.zeros(len(TERMINALS))
    for left, right in combinations(range(len(TERMINALS)), 2):
        value = sp.Symbol(f"{prefix}_{TERMINALS[left]}{TERMINALS[right]}")
        matrix[left, right] = matrix[right, left] = value
    return matrix


def wick_moment(matrix: sp.Matrix) -> Polynomial:
    """Return all even principal hafnians as a squarefree polynomial."""

    @cache
    def hafnian(subset: int) -> sp.Expr:
        if subset == 0:
            return sp.Integer(1)
        if subset.bit_count() % 2:
            return sp.Integer(0)
        first = (subset & -subset).bit_length() - 1
        rest = subset ^ (1 << first)
        total = sp.Integer(0)
        remaining = rest
        while remaining:
            right_bit = remaining & -remaining
            right = right_bit.bit_length() - 1
            total += matrix[first, right] * hafnian(rest ^ right_bit)
            remaining ^= right_bit
        return sp.expand(total)

    return {
        subset: hafnian(subset)
        for subset in range(1 << len(TERMINALS))
        if subset.bit_count() % 2 == 0
    }


def verify_face_count() -> None:
    """Check the exact prescribed/free deletion partition."""

    prescribed = {
        sum(1 << index for index in deletion)
        for size in (2, 4, 6)
        for deletion in combinations(range(len(TERMINALS)), size)
        if sum(1 << index for index in deletion) != Q
    }
    assert len(prescribed) == 62
    assert Q not in prescribed
    assert 0 not in prescribed

    surviving_degrees = {
        (FULL ^ deletion).bit_count() for deletion in prescribed
    }
    assert surviving_degrees == {1, 3, 5}
    degree_five = [
        deletion for deletion in prescribed if (FULL ^ deletion).bit_count() == 5
    ]
    assert len(degree_five) == 20


def verify_two_face_formula() -> None:
    """Check E_-M F and the sign of the unique ab shear."""

    alpha, beta = sp.symbols("alpha beta")
    matrix = terminal_matrix("m")
    inverse_wick = wick_moment(-matrix)
    mixed_boundary = {P_MINUS_Q: alpha, FULL: beta}
    quotient = multiply(inverse_wick, mixed_boundary)

    m_ab = matrix[TERMINALS.index("a"), TERMINALS.index("b")]
    expected = {
        P_MINUS_Q: alpha,
        FULL: sp.expand(beta - m_ab * alpha),
    }
    assert quotient == expected

    rho = sp.Symbol("rho")
    common_terminal_top = sp.expand(
        expected[FULL].subs(m_ab, 1 - rho)
    )
    assert common_terminal_top == sp.expand(beta + (rho - 1) * alpha)


def verify_wick_inverse() -> None:
    """Check E_M E_-M=1 for the generic scalar terminal block."""

    matrix = terminal_matrix("w")
    forward = wick_moment(matrix)
    backward = wick_moment(-matrix)
    assert multiply(forward, backward) == {0: sp.Integer(1)}


def main() -> None:
    verify_face_count()
    verify_two_face_formula()
    verify_wick_inverse()
    print(
        {
            "status": "pass",
            "coefficient_space": "seven-blocker tensor",
            "scalar_terminal_vertices": 7,
            "prescribed_mixed_zero_faces": 62,
            "surviving_mixed_core_faces": 2,
            "unique_shear_edge": "ab",
            "shear_sign": "-M_ab",
            "support_searches": 0,
            "common_core_realized": False,
            "global_conjecture_resolved": False,
        }
    )


if __name__ == "__main__":
    main()
