"""Primary exact checks for the residual two-port pentad theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

Edge = tuple[int, int]


def edge(i: int, j: int) -> Edge:
    return (i, j) if i < j else (j, i)


def pentad(values: dict[Edge, sp.Expr]) -> sp.Expr:
    """Return the named five-port pentad."""

    def x(i: int, j: int) -> sp.Expr:
        return values[edge(i, j)]

    return sp.expand(
        x(1, 2) * x(1, 3) * x(2, 4) * x(3, 5) * x(4, 5)
        - x(1, 2) * x(1, 3) * x(2, 5) * x(3, 4) * x(4, 5)
        - x(1, 2) * x(1, 4) * x(2, 3) * x(3, 5) * x(4, 5)
        + x(1, 2) * x(1, 4) * x(2, 5) * x(3, 4) * x(3, 5)
        + x(1, 2) * x(1, 5) * x(2, 3) * x(3, 4) * x(4, 5)
        - x(1, 2) * x(1, 5) * x(2, 4) * x(3, 4) * x(3, 5)
        + x(1, 3) * x(1, 4) * x(2, 3) * x(2, 5) * x(4, 5)
        - x(1, 3) * x(1, 4) * x(2, 4) * x(2, 5) * x(3, 5)
        - x(1, 3) * x(1, 5) * x(2, 3) * x(2, 4) * x(4, 5)
        + x(1, 3) * x(1, 5) * x(2, 4) * x(2, 5) * x(3, 4)
        - x(1, 4) * x(1, 5) * x(2, 3) * x(2, 5) * x(3, 4)
        + x(1, 4) * x(1, 5) * x(2, 3) * x(2, 4) * x(3, 5)
    )


def pentad_and_irreducibility_checks() -> None:
    edges = tuple(combinations(range(1, 6), 2))
    y = {pair: sp.Symbol(f"k{pair[0]}{pair[1]}") for pair in edges}
    polynomial = pentad(y)
    assert len(sp.Poly(polynomial, *y.values()).terms()) == 12
    assert polynomial.coeff(y[(1, 2)] * y[(1, 3)] * y[(2, 4)] * y[(3, 5)] * y[(4, 5)]) == 1

    a = sp.symbols("a1:6")
    b = sp.symbols("b1:6")
    gram = {
        (i + 1, j + 1): a[i] * b[j] + b[i] * a[j]
        for i, j in combinations(range(5), 2)
    }
    assert sp.expand(pentad(gram)) == 0

    poly_in_k45 = sp.Poly(polynomial, y[(4, 5)])
    coefficient = poly_in_k45.coeff_monomial(y[(4, 5)])
    constant = poly_in_k45.coeff_monomial(1)

    coefficient_in_k23 = sp.Poly(coefficient, y[(2, 3)])
    coefficient_constant = coefficient_in_k23.coeff_monomial(1)
    coefficient_linear = coefficient_in_k23.coeff_monomial(y[(2, 3)])
    expected_constant = y[(1, 2)] * y[(1, 3)] * (
        y[(2, 4)] * y[(3, 5)] - y[(2, 5)] * y[(3, 4)]
    )
    assert sp.expand(coefficient_constant - expected_constant) == 0
    assert coefficient_linear.subs(y[(1, 2)], 0) != 0
    assert coefficient_linear.subs(y[(1, 3)], 0) != 0

    determinant_zero_point = {
        y[(1, 2)]: 1,
        y[(1, 3)]: 1,
        y[(1, 4)]: 0,
        y[(1, 5)]: 1,
        y[(2, 4)]: 1,
        y[(2, 5)]: 0,
        y[(3, 4)]: 0,
        y[(3, 5)]: 0,
    }
    assert expected_constant.subs(determinant_zero_point) == 0
    assert coefficient_linear.subs(determinant_zero_point) == -1

    coprime_point = {
        y[(1, 2)]: 0,
        y[(1, 3)]: 0,
        y[(1, 4)]: 1,
        y[(1, 5)]: 1,
        y[(2, 3)]: 1,
        y[(2, 4)]: 0,
        y[(2, 5)]: 1,
        y[(3, 4)]: 1,
        y[(3, 5)]: 0,
    }
    assert coefficient.subs(coprime_point) == 0
    assert constant.subs(coprime_point) == -1


def jacobian_checks() -> None:
    a = sp.symbols("a1:6")
    b = sp.symbols("b1:6")
    variables = (*a, *b)
    edges = tuple(combinations(range(5), 2))
    responses = tuple(a[i] * b[j] + b[i] * a[j] for i, j in edges)
    jacobian = sp.Matrix(responses).jacobian(variables)

    minor5 = sp.expand(jacobian[:9, :9].det())
    expected5 = sp.expand(
        -4
        * b[4]
        * (a[0] * b[1] - a[1] * b[0])
        * (a[0] * b[2] - a[2] * b[0])
        * (a[1] * b[2] - a[2] * b[1])
        * (a[3] * b[4] - a[4] * b[3])
    )
    assert sp.expand(minor5 - expected5) == 0

    point = {a[i]: i + 1 for i in range(5)}
    point.update({b[i]: (i + 1) ** 2 + 1 for i in range(5)})
    assert minor5.subs(point) == -39520
    assert jacobian.subs(point).rank() == 9

    responses4 = tuple(
        a[i] * b[j] + b[i] * a[j] for i, j in combinations(range(4), 2)
    )
    jacobian4 = sp.Matrix(responses4).jacobian((*a[:4], *b[:4]))
    minor4 = sp.expand(jacobian4[:, :6].det())
    expected4 = sp.expand(
        2
        * (a[2] * b[3] - a[3] * b[2])
        * (
            a[0] * b[1] * b[2] * b[3]
            + a[1] * b[0] * b[2] * b[3]
            - a[2] * b[0] * b[1] * b[3]
            - a[3] * b[0] * b[1] * b[2]
        )
    )
    assert sp.expand(minor4 - expected4) == 0
    assert minor4.subs(point) == 13640
    assert jacobian4.subs(point).rank() == 6


def relative_invariant_checks() -> None:
    edges = tuple(combinations(range(1, 6), 2))
    y = {pair: sp.Symbol(f"k{pair[0]}{pair[1]}") for pair in edges}
    polynomial = pentad(y)

    t = sp.symbols("t1:6")
    scaled = {
        (i, j): t[i - 1] * t[j - 1] * y[(i, j)]
        for i, j in edges
    }
    assert sp.expand(pentad(scaled) - sp.prod(value**2 for value in t) * polynomial) == 0

    for left in range(1, 5):
        permutation = list(range(1, 6))
        permutation[left - 1], permutation[left] = (
            permutation[left],
            permutation[left - 1],
        )
        relabeled = {
            (i, j): y[edge(permutation[i - 1], permutation[j - 1])]
            for i, j in edges
        }
        assert sp.expand(pentad(relabeled) + polynomial) == 0


def main() -> None:
    pentad_and_irreducibility_checks()
    jacobian_checks()
    relative_invariant_checks()
    print("residual two-port factor-analysis/pentad primary: PASS")
    print("pentad_terms: 12")
    print("five_port_jacobian_rank: 9")
    print("four_port_jacobian_rank: 6")
    print("global_krenn_gu_resolved: false")


if __name__ == "__main__":
    main()
