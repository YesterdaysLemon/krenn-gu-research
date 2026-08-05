"""Independent no-import audit of the five-port two-residual pentad."""

from __future__ import annotations

from itertools import combinations

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, int]
Edge = tuple[int, int]


def clean(polynomial: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def scale(polynomial: Polynomial, scalar: int) -> Polynomial:
    return clean({monomial: scalar * coefficient for monomial, coefficient in polynomial.items()})


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                first + second
                for first, second in zip(monomial_left, monomial_right, strict=True)
            )
            result[monomial] = result.get(monomial, 0) + coefficient_left * coefficient_right
    return clean(result)


def variable(index: int, variable_count: int) -> Polynomial:
    exponent = [0] * variable_count
    exponent[index] = 1
    return {tuple(exponent): 1}


def product(factors: tuple[Polynomial, ...], variable_count: int) -> Polynomial:
    result: Polynomial = {(0,) * variable_count: 1}
    for factor in factors:
        result = multiply(result, factor)
    return result


PENTAD_TERMS: tuple[tuple[int, tuple[Edge, ...]], ...] = (
    (1, ((1, 2), (1, 3), (2, 4), (3, 5), (4, 5))),
    (-1, ((1, 2), (1, 3), (2, 5), (3, 4), (4, 5))),
    (-1, ((1, 2), (1, 4), (2, 3), (3, 5), (4, 5))),
    (1, ((1, 2), (1, 4), (2, 5), (3, 4), (3, 5))),
    (1, ((1, 2), (1, 5), (2, 3), (3, 4), (4, 5))),
    (-1, ((1, 2), (1, 5), (2, 4), (3, 4), (3, 5))),
    (1, ((1, 3), (1, 4), (2, 3), (2, 5), (4, 5))),
    (-1, ((1, 3), (1, 4), (2, 4), (2, 5), (3, 5))),
    (-1, ((1, 3), (1, 5), (2, 3), (2, 4), (4, 5))),
    (1, ((1, 3), (1, 5), (2, 4), (2, 5), (3, 4))),
    (-1, ((1, 4), (1, 5), (2, 3), (2, 5), (3, 4))),
    (1, ((1, 4), (1, 5), (2, 3), (2, 4), (3, 5))),
)


def symbolic_pentad() -> None:
    edges = tuple(combinations(range(1, 6), 2))
    edge_index = {pair: index for index, pair in enumerate(edges)}
    y = {pair: variable(index, len(edges)) for pair, index in edge_index.items()}

    named: Polynomial = {}
    for sign, term_edges in PENTAD_TERMS:
        term = product(tuple(y[pair] for pair in term_edges), len(edges))
        named = add(named, scale(term, sign))
    assert len(named) == 12

    parameter_count = 10
    a = [variable(index, parameter_count) for index in range(5)]
    b = [variable(index + 5, parameter_count) for index in range(5)]
    gram: dict[Edge, Polynomial] = {}
    for i, j in combinations(range(5), 2):
        gram[(i + 1, j + 1)] = add(multiply(a[i], b[j]), multiply(b[i], a[j]))

    substituted: Polynomial = {}
    for sign, term_edges in PENTAD_TERMS:
        term = product(tuple(gram[pair] for pair in term_edges), parameter_count)
        substituted = add(substituted, scale(term, sign))
    assert substituted == {}

    assignment = {pair: index + 1 for index, pair in enumerate(edges)}
    value = 0
    for sign, term_edges in PENTAD_TERMS:
        term_value = sign
        for pair in term_edges:
            term_value *= assignment[pair]
        value += term_value
    assert value == -6


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    denominator = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                row
                for row in range(pivot_index + 1, size)
                if work[row][pivot_index] != 0
            )
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = work[row][column] * pivot - work[row][pivot_index] * work[pivot_index][column]
                assert numerator % denominator == 0
                work[row][column] = numerator // denominator
        denominator = pivot
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
    return sign * work[-1][-1]


def response_jacobian(
    port_count: int,
    a: tuple[int, ...],
    b: tuple[int, ...],
) -> list[list[int]]:
    rows: list[list[int]] = []
    for i, j in combinations(range(port_count), 2):
        row = [0] * (2 * port_count)
        row[i] = b[j]
        row[j] = b[i]
        row[port_count + i] = a[j]
        row[port_count + j] = a[i]
        rows.append(row)
    return rows


def determinant_certificates() -> None:
    a5 = (1, 2, 3, 4, 5)
    b5 = (2, 5, 10, 17, 26)
    jacobian5 = response_jacobian(5, a5, b5)
    minor5 = [row[:9] for row in jacobian5[:9]]
    assert bareiss_determinant(minor5) == -39520

    certificate5 = (
        -4
        * b5[4]
        * (a5[0] * b5[1] - a5[1] * b5[0])
        * (a5[0] * b5[2] - a5[2] * b5[0])
        * (a5[1] * b5[2] - a5[2] * b5[1])
        * (a5[3] * b5[4] - a5[4] * b5[3])
    )
    assert certificate5 == -39520

    a4 = a5[:4]
    b4 = b5[:4]
    jacobian4 = response_jacobian(4, a4, b4)
    minor4 = [row[:6] for row in jacobian4]
    assert bareiss_determinant(minor4) == 13640

    certificate4 = 2 * (a4[2] * b4[3] - a4[3] * b4[2]) * (
        a4[0] * b4[1] * b4[2] * b4[3]
        + a4[1] * b4[0] * b4[2] * b4[3]
        - a4[2] * b4[0] * b4[1] * b4[3]
        - a4[3] * b4[0] * b4[1] * b4[2]
    )
    assert certificate4 == 13640

    a5_second = (2, -1, 3, 5, 7)
    b5_second = (1, 4, -2, 6, 9)
    jacobian_second = response_jacobian(5, a5_second, b5_second)
    determinant_second = bareiss_determinant([row[:9] for row in jacobian_second[:9]])
    certificate_second = (
        -4
        * b5_second[4]
        * (a5_second[0] * b5_second[1] - a5_second[1] * b5_second[0])
        * (a5_second[0] * b5_second[2] - a5_second[2] * b5_second[0])
        * (a5_second[1] * b5_second[2] - a5_second[2] * b5_second[1])
        * (a5_second[3] * b5_second[4] - a5_second[4] * b5_second[3])
    )
    assert determinant_second == certificate_second != 0


def main() -> None:
    symbolic_pentad()
    determinant_certificates()
    print("residual two-port factor-analysis/pentad independent audit: PASS")
    print("dictionary_substitution_terms: 0")
    print("first_five_port_minor: -39520")
    print("four_port_minor: 13640")
    print("global_krenn_gu_resolved: false")


if __name__ == "__main__":
    main()
