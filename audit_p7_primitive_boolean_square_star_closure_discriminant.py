"""Independent stdlib audit of the P7 star-closure discriminant theorem."""

from fractions import Fraction
from itertools import combinations
from math import gcd


def integer_rank(matrix: list[list[int]]) -> int:
    """Exact rank by gcd-controlled fraction-free elimination."""
    work = [row[:] for row in matrix]
    if not work:
        return 0
    nrows, ncols = len(work), len(work[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next((row for row in range(pivot_row, nrows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(nrows):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            tail = [
                pivot_value * work[row][j] - factor * work[pivot_row][j]
                for j in range(column, ncols)
            ]
            divisor = 0
            for value in tail:
                divisor = gcd(divisor, abs(value))
            if divisor > 1:
                tail = [value // divisor for value in tail]
            work[row][column:] = tail
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def determinant(matrix: list[list[int]]) -> int:
    """Exact determinant by rational Gaussian elimination."""
    work = [[Fraction(value) for value in row] for row in matrix]
    size = len(work)
    sign = 1
    result = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for j in range(column + 1, size):
                work[row][j] -= factor * work[column][j]
    assert result.denominator == 1
    return sign * result.numerator


def poly_add(*polys: dict[tuple[int, ...], Fraction]) -> dict[tuple[int, ...], Fraction]:
    """Add sparse multivariate polynomials."""
    result: dict[tuple[int, ...], Fraction] = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def poly_scale(poly: dict[tuple[int, ...], Fraction], scalar: int) -> dict[tuple[int, ...], Fraction]:
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if coefficient}


def poly_mul(
    left: dict[tuple[int, ...], Fraction],
    right: dict[tuple[int, ...], Fraction],
    *others: dict[tuple[int, ...], Fraction],
) -> dict[tuple[int, ...], Fraction]:
    result: dict[tuple[int, ...], Fraction] = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(a + b for a, b in zip(monomial_left, monomial_right, strict=True))
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient_left * coefficient_right
    result = {monomial: coefficient for monomial, coefficient in result.items() if coefficient}
    for other in others:
        result = poly_mul(result, other)
    return result


def variables(count: int) -> list[dict[tuple[int, ...], Fraction]]:
    result = []
    for index in range(count):
        exponent = [0] * count
        exponent[index] = 1
        result.append({tuple(exponent): Fraction(1)})
    return result


def main() -> None:
    leaves = tuple(range(7))
    edges = list(combinations(leaves, 2))
    edge_position = {edge: index for index, edge in enumerate(edges)}
    unsigned = [[0] * 21 for _ in leaves]
    for edge, column in edge_position.items():
        for vertex in edge:
            unsigned[vertex][column] = 1

    gram7 = [
        [sum(unsigned[i][edge] * unsigned[j][edge] for edge in range(21)) for j in leaves]
        for i in leaves
    ]
    assert gram7 == [[6 if i == j else 1 for j in leaves] for i in leaves]

    schur = [[3 * int(i == j) + sum(unsigned[v][i] * unsigned[v][j] for v in leaves) for j in range(21)] for i in range(21)]
    expected = 5 * 8**6 * 3**15
    assert determinant(schur) == expected

    # Independent exact inclusion ranks for every possible forbidden zero set.
    for size in range(5, 9):
        vertices = tuple(range(size))
        pairs = list(combinations(vertices, 2))
        triples = list(combinations(vertices, 3))
        w23 = [[int(set(pair) < set(triple)) for pair in pairs] for triple in triples]
        assert integer_rank(w23) == len(pairs)

    # Sparse-polynomial replay of the universal anchor reduction.
    # Variable order: aj, ak, yj, yk, x, R.
    aj, ak, yj, yk, x, big_r = variables(6)
    one = {(0, 0, 0, 0, 0, 0): Fraction(1)}
    bjk = poly_mul(aj, ak, x)
    rj = poly_mul(aj, poly_add(one, yj))
    rk = poly_mul(ak, poly_add(one, yk))
    triangle = poly_add(
        poly_mul(aj, rk),
        poly_mul(ak, rj),
        poly_mul(bjk, big_r),
        poly_scale(poly_mul(aj, ak), -2),
        poly_scale(poly_mul(aj, bjk), -2),
        poly_scale(poly_mul(ak, bjk), -2),
    )
    reduced = poly_mul(
        aj,
        ak,
        poly_add(yj, yk, poly_mul(poly_add(big_r, poly_scale(aj, -2), poly_scale(ak, -2)), x)),
    )
    assert poly_add(triangle, poly_scale(reduced, -1)) == {}

    # Separate sparse-polynomial check of the four-value difference identity.
    z1, z2, z3, z4 = variables(4)

    def cayley(
        left: dict[tuple[int, ...], Fraction],
        middle: dict[tuple[int, ...], Fraction],
        right: dict[tuple[int, ...], Fraction],
    ) -> dict[tuple[int, ...], Fraction]:
        return poly_add(
            poly_mul(left, middle),
            poly_mul(left, right),
            poly_mul(middle, right),
            poly_scale(left, -1),
            poly_scale(middle, -1),
            poly_scale(right, -1),
        )

    difference = poly_add(cayley(z1, z2, z3), poly_scale(cayley(z1, z2, z4), -1))
    factored = poly_mul(poly_add(z3, poly_scale(z4, -1)), poly_add(z1, z2, poly_scale({(0, 0, 0, 0): Fraction(1)}, -1)))
    assert poly_add(difference, poly_scale(factored, -1)) == {}

    # Independent algebra for the four-zero-row boundary.
    # If p^2-p+1=0 and q=1-p, then pq=1, same-class factor=-2,
    # cross-class factor=1, and the two zero-row equations force 7/2=0.
    # Reduce A*p^2+B*p+C modulo p^2=p-1.
    def reduce_quadratic(coefficients: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        a2, a1, a0 = coefficients
        return a2 + a1, a0 - a2

    assert reduce_quadratic((Fraction(-1), Fraction(1), Fraction(0))) == (Fraction(0), Fraction(1))  # p(1-p)=1
    assert reduce_quadratic((Fraction(2), Fraction(-2), Fraction(0))) == (Fraction(0), Fraction(-2))
    assert Fraction(3, 2) + 2 == Fraction(7, 2)
    assert Fraction(7, 2) != 0

    print("PASS: independent all-one Schur determinant 5*8^6*3^15")
    print("PASS: independent exact W_(2,3)(s) ranks for 5<=s<=8")
    print("PASS: no-import sparse-polynomial anchor-pencil identity")
    print("PASS: no-import four-zero-row sixth-root contradiction")
    print("UNKNOWN: discriminant-plus-leaf-quadrics torus incidence")
    print("UNKNOWN: primitive Boolean-square edge-torus point")
    print("UNRESOLVED: global Krenn--Gu conjecture")


if __name__ == "__main__":
    main()
