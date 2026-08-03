"""Independent standard-library audit of the P7 support-six exclusion."""

from collections import defaultdict
from itertools import combinations

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]


def add(*polynomials: Polynomial) -> Polynomial:
    out: defaultdict[Monomial, int] = defaultdict(int)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def scale(polynomial: Polynomial, scalar: int) -> Polynomial:
    return {monomial: scalar * coefficient for monomial, coefficient in polynomial.items() if scalar * coefficient}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    out: defaultdict[Monomial, int] = defaultdict(int)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            out[tuple(sorted(left_monomial + right_monomial))] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def variable(name: str) -> Polynomial:
    return {(name,): 1}


ONE: Polynomial = {(): 1}


def haf4(vertices: tuple[int, int, int, int], edge: dict[tuple[int, int], Polynomial]) -> Polynomial:
    a, b, c, d = vertices

    def e(i: int, j: int) -> Polynomial:
        return edge[tuple(sorted((i, j)))]

    return add(
        multiply(e(a, b), e(c, d)),
        multiply(e(a, c), e(b, d)),
        multiply(e(a, d), e(b, c)),
    )


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        value = work[column][column]
        for row in range(column + 1, size):
            for other_column in range(column + 1, size):
                numerator = work[row][other_column] * value - work[row][column] * work[column][other_column]
                assert numerator % previous == 0
                work[row][other_column] = numerator // previous
        previous = value
    return sign * work[-1][-1]


def rational_rank(matrix: list[list[int]]) -> int:
    from fractions import Fraction

    work = [[Fraction(value) for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [entry - value * pivot_entry for entry, pivot_entry in zip(work[index], work[row])]
        row += 1
    return row


def main() -> None:
    support = tuple(range(6))
    c1, c2 = 6, 7
    u = [variable(f"u{i}") for i in support]
    v = [variable(f"v{i}") for i in support]
    d = {(i, j): variable(f"d{i}{j}") for i, j in combinations(support, 2)}

    raw_edge: dict[tuple[int, int], Polynomial] = {(c1, c2): ONE}
    for i in support:
        raw_edge[tuple(sorted((i, c1)))] = u[i]
        raw_edge[tuple(sorted((i, c2)))] = v[i]
    raw_edge.update(d)

    triple = (0, 1, 2)
    row_three = add(
        *(
            haf4(tuple(sorted((set(triple) - {removed}) | {c1, c2})), raw_edge)
            for removed in triple
        )
    )
    target_three = add(
        *(
            add(d[(i, j)], multiply(u[i], v[j]), multiply(v[i], u[j]))
            for i, j in combinations(triple, 2)
        )
    )
    assert row_three == target_three

    recovered_edge = dict(raw_edge)
    for i, j in combinations(support, 2):
        recovered_edge[(i, j)] = scale(add(multiply(u[i], v[j]), multiply(v[i], u[j])), -1)

    quad = (0, 1, 2, 3)
    row_four = add(
        *(
            haf4(tuple(sorted((set(quad) - {removed}) | {c1})), recovered_edge)
            for removed in quad
        )
    )
    mixed = add(
        *(
            add(
                multiply(multiply(v[i], u[j]), u[k]),
                multiply(multiply(u[i], v[j]), u[k]),
                multiply(multiply(u[i], u[j]), v[k]),
            )
            for i, j, k in combinations(quad, 3)
        )
    )
    assert add(row_four, scale(mixed, 2)) == {}

    edges = list(combinations(support, 2))
    triples = list(combinations(support, 3))
    quads = list(combinations(support, 4))
    w23 = [[int(set(edge) <= set(triple_set)) for edge in edges] for triple_set in triples]
    w24 = [[int(set(edge) <= set(quad_set)) for edge in edges] for quad_set in quads]
    assert rational_rank(w23) == 15
    assert bareiss_determinant(w24) == 1458
    assert bareiss_determinant([[1, 1, 0], [1, 0, 1], [0, 1, 1]]) == -2

    print("PASS: independent P7 support-six exclusion audit")
    print("fixed exact inclusion invariants: rank 15, determinant 1458")
    print("scope: sparse universal identities and integer elimination only")


if __name__ == "__main__":
    main()
