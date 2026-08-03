"""Primary exact checks for the switched-circulant primitive-square no-go."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(7))
DEGREE_TWO_MONOMIALS = ((2, 0, 0), (1, 1, 0), (1, 0, 1), (0, 2, 0), (0, 1, 1), (0, 0, 2))
DEGREE_FOUR_MONOMIALS = tuple(
    (first, second, 4 - first - second)
    for first in range(4, -1, -1)
    for second in range(4 - first, -1, -1)
)
SELECTED_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15)


def cyclic_distance(left: int, right: int) -> int:
    difference = (left - right) % 7
    return min(difference, 7 - difference)


def edge_weight(left: int, right: int, values: tuple[sp.Expr, ...]) -> sp.Expr:
    return values[cyclic_distance(left, right) - 1]


def four_hafnian(vertices: tuple[int, ...], values: tuple[sp.Expr, ...]) -> sp.Expr:
    first, second, third, fourth = sorted(vertices)
    return sp.expand(
        edge_weight(first, second, values) * edge_weight(third, fourth, values)
        + edge_weight(first, third, values) * edge_weight(second, fourth, values)
        + edge_weight(first, fourth, values) * edge_weight(second, third, values)
    )


def character_quadrics(
    values: tuple[sp.Expr, ...], character: sp.Expr
) -> tuple[sp.Expr, ...]:
    equations = []
    for distance in (1, 2, 3):
        five_set = tuple(vertex for vertex in VERTICES if vertex not in (0, distance))
        equation = sum(
            four_hafnian(
                tuple(item for item in five_set if item != omitted), values
            )
            * character**omitted
            for omitted in five_set
        )
        equations.append(sp.expand(equation))
    return tuple(equations)


def displayed_symbol_check() -> tuple[tuple[sp.Expr, ...], sp.Symbol]:
    a, b, c, t = sp.symbols("a b c t")
    equations = character_quadrics((a, b, c), t)
    first = a**2 + a * c + b**2
    second = a * b + a * c + b * c
    third = a**2 + b * c + c**2
    fourth = a * b + b**2 + c**2
    expected = (
        first * (t**2 + t**6) + second * (t**3 + t**5) + third * t**4,
        first * t + second * (t**3 + t**6) + fourth * (t**4 + t**5),
        second * (t + t**2) + third * (t**4 + t**6) + fourth * t**5,
    )
    assert all(
        sp.expand(actual - target) == 0
        for actual, target in zip(equations, expected, strict=True)
    )
    print("three exact C7 Fourier-symbol quadrics: PASS")
    return equations, t


def macaulay_matrix(equations: tuple[sp.Expr, ...]) -> sp.Matrix:
    a, b, c = sp.symbols("a b c")
    variables = (a, b, c)
    degree_two = tuple(a**i * b**j * c**k for i, j, k in DEGREE_TWO_MONOMIALS)
    degree_four = tuple(a**i * b**j * c**k for i, j, k in DEGREE_FOUR_MONOMIALS)
    rows = []
    for equation in equations:
        for multiplier in degree_two:
            polynomial = sp.Poly(sp.expand(equation * multiplier), *variables)
            rows.append(
                [polynomial.coeff_monomial(monomial) for monomial in degree_four]
            )
    return sp.Matrix(rows)


def macaulay_certificate_check(equations: tuple[sp.Expr, ...], t: sp.Symbol) -> None:
    matrix = macaulay_matrix(equations)
    assert matrix.shape == (18, 15)
    selected = matrix[list(SELECTED_ROWS), :]

    trivial_determinant = selected.subs(t, 1).det(method="domain-ge")
    assert trivial_determinant == -3_149_280
    assert sp.factorint(abs(trivial_determinant)) == {2: 5, 3: 9, 5: 1}

    determinant = sp.Poly(selected.det(method="domain-ge"), t)
    cyclotomic = sp.Poly(sum(t**power for power in range(7)), t)
    remainder = determinant.rem(cyclotomic).as_expr()
    expected_remainder = -73_728 * t**3 * (t + 1)
    assert sp.expand(remainder - expected_remainder) == 0
    assert sp.factorint(73_728) == {2: 13, 3: 2}
    print("degree-four Macaulay minor at t=1 and modulo Phi_7: PASS")


def switching_reduction_check() -> None:
    a, b, c = sp.symbols("a b c")
    values = (a, b, c)
    switches = sp.symbols("s0:7", nonzero=True)
    base_four = {
        subset: four_hafnian(subset, values)
        for subset in combinations(VERTICES, 4)
    }
    for missing_edge in combinations(VERTICES, 2):
        five_set = tuple(vertex for vertex in VERTICES if vertex not in missing_edge)
        switched_sum = sp.Integer(0)
        reduced_sum = sp.Integer(0)
        common_switch = sp.prod(switches[vertex] for vertex in five_set)
        for omitted in five_set:
            four_set = tuple(vertex for vertex in five_set if vertex != omitted)
            switched_sum += (
                sp.prod(switches[vertex] for vertex in four_set)
                * base_four[four_set]
            )
            reduced_sum += base_four[four_set] / switches[omitted]
        assert sp.cancel(switched_sum - common_switch * reduced_sum) == 0
    print("vertex switching reduces primitivity to a C7-equivariant linear kernel: PASS")


def main() -> None:
    equations, character = displayed_symbol_check()
    macaulay_certificate_check(equations, character)
    switching_reduction_check()
    print("seven-leaf switched-circulant primitive-square primary: PASS")
    print("searches=0 parameter_enumerations=0 finite_fields=0 numerics=0")


if __name__ == "__main__":
    main()
