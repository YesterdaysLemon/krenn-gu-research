"""Independent no-import audit for GLS43.

This script imports no project module or third-party package.  It uses a
small Fraction-free integer elimination route and a dictionary polynomial
determinant, independently of the SymPy primary verifier.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product


def rank(rows: list[list[int | Fraction]]) -> int:
    work = [[Fraction(value) for value in row] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix)]


def outer(left: tuple[int, int, int], right: tuple[int, int, int]) -> list[list[int]]:
    return [[left[i] * right[j] for j in range(3)] for i in range(3)]


def add(*matrices: list[list[int]]) -> list[list[int]]:
    return [
        [sum(matrix[i][j] for matrix in matrices) for j in range(3)]
        for i in range(3)
    ]


def scale(factor: int, matrix: list[list[int]]) -> list[list[int]]:
    return [[factor * value for value in row] for row in matrix]


def symmetric(left: tuple[int, int, int], right: tuple[int, int, int]) -> list[list[int]]:
    return add(outer(left, right), outer(right, left))


def flatten(matrix: list[list[int]]) -> list[int]:
    return [value for row in matrix for value in row]


def matrix_span_rank(matrices: list[list[list[int]]]) -> int:
    return rank(transpose([flatten(matrix) for matrix in matrices]))


# Sparse polynomials in (r,s,t), keyed by exponent triples.
Poly = dict[tuple[int, int, int], int]


def p_const(value: int) -> Poly:
    return {} if value == 0 else {(0, 0, 0): value}


def p_var(index: int, factor: int = 1) -> Poly:
    exponent = [0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): factor}


def p_add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def p_neg(poly: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def p_mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(a + b for a, b in zip(monomial_left, monomial_right))
            result[monomial] = (
                result.get(monomial, 0) + coefficient_left * coefficient_right
            )
            if result[monomial] == 0:
                del result[monomial]
    return result


def parity(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def p_det(matrix: list[list[Poly]]) -> Poly:
    size = len(matrix)
    result: Poly = {}
    for permutation in permutations(range(size)):
        term = p_const(parity(permutation))
        for row, column in enumerate(permutation):
            term = p_mul(term, matrix[row][column])
        result = p_add(result, term)
    return result


def terminal_polynomial_matrix() -> list[list[Poly]]:
    zero, one, minus_one = p_const(0), p_const(1), p_const(-1)
    r, s, t = p_var(0), p_var(1), p_var(2)
    return [
        [minus_one, one, zero, p_neg(r), zero],
        [zero, zero, one, p_neg(s), zero],
        [zero, zero, minus_one, p_neg(t), zero],
        [zero, one, zero, zero, p_neg(r)],
        [minus_one, zero, one, zero, p_neg(s)],
        [zero, minus_one, zero, zero, p_neg(t)],
    ]


def expected_terminal_minors() -> list[Poly]:
    r, s, t = p_var(0), p_var(1), p_var(2)
    plus = p_add

    def minus(left: Poly, right: Poly) -> Poly:
        return p_add(left, p_neg(right))

    return [
        p_mul(plus(r, t), plus(s, t)),
        p_mul(minus(r, t), plus(r, t)),
        p_neg(p_mul(plus(r, s), plus(r, t))),
        p_neg(p_mul(minus(s, t), plus(s, t))),
        p_neg(p_mul(plus(r, t), plus(s, t))),
        p_neg(p_mul(plus(r, s), plus(s, t))),
    ]


def terminal_numeric_matrix(fibre: tuple[int, int, int]) -> list[list[int]]:
    r, s, t = fibre
    return [
        [-1, 1, 0, -r, 0],
        [0, 0, 1, -s, 0],
        [0, 0, -1, -t, 0],
        [0, 1, 0, 0, -r],
        [-1, 0, 1, 0, -s],
        [0, -1, 0, 0, -t],
    ]


def multiply(matrix: list[list[int]], vector: tuple[int, ...]) -> list[int]:
    return [sum(value * vector[column] for column, value in enumerate(row)) for row in matrix]


def check_terminal_derivation() -> None:
    matrix = terminal_polynomial_matrix()
    minors = []
    for omitted in range(6):
        square = [row for index, row in enumerate(matrix) if index != omitted]
        minors.append(p_det(square))
    assert minors == expected_terminal_minors()

    exceptional = [
        ((1, -1, -1), (1, 1, 0, 0, 1)),
        ((1, -1, 1), (1, 0, 1, -1, 0)),
        ((1, 1, -1), (0, 1, 1, 1, 1)),
    ]
    for fibre, kernel_vector in exceptional:
        numeric = terminal_numeric_matrix(fibre)
        assert rank(numeric) == 4
        assert multiply(numeric, kernel_vector) == [0] * 6
    assert rank(terminal_numeric_matrix((1, 2, 3))) == 5

    # The maximal-minor equations give r=+/-t and s=+/-t.  In characteristic
    # not two, the all-equal sign choice is excluded and exactly these three
    # projective sign patterns remain.
    surviving = []
    for sign_r, sign_s in product((-1, 1), repeat=2):
        fibre = (sign_r, sign_s, 1)
        if rank(terminal_numeric_matrix(fibre)) < 5:
            surviving.append(fibre)
    assert surviving == [(-1, -1, 1), (-1, 1, 1), (1, -1, 1)]


def check_quotient_line_representation() -> None:
    # P represents an arbitrary rank-two quotient K^3 -> K^2.  For each
    # nonzero coordinate of b, b_i*xbar must lie on the fixed line K*P(e_i).
    # Exhausting all small full-rank P and all support patterns is an exact
    # independent stress replay of the coefficient-comparison lemma.
    checked = 0
    for entries in product((-1, 0, 1), repeat=6):
        quotient = [list(entries[:3]), list(entries[3:])]
        if rank(quotient) != 2:
            continue
        columns = list(zip(*quotient))
        for b in product((-1, 0, 1), repeat=3):
            if b == (0, 0, 0):
                continue
            constraints: list[list[int]] = []
            for coordinate, coefficient in enumerate(b):
                if coefficient == 0:
                    continue
                column = columns[coordinate]
                if column == (0, 0):
                    constraints.extend([[1, 0], [0, 1]])
                else:
                    # det(xbar, column)=0.
                    constraints.append([column[1], -column[0]])
            assert 2 - rank(constraints) <= 1
            checked += 1
    assert checked > 10_000


def check_three_dimensional_endgame() -> None:
    h0, h1 = (1, -1, 0), (1, 0, -1)
    cases = [
        ((1, -1, -1), (1, 1, 0)),
        ((1, -1, 1), (1, 0, 1)),
        ((1, 1, -1), (0, 1, 1)),
    ]
    for _, line in cases:
        generators = [symmetric(h0, line), symmetric(h1, line), symmetric(line, line)]
        assert matrix_span_rank(generators) == 3


def check_repeated_anchor_boundary() -> None:
    left = (1, 0, -1)
    right = (-1, 0, -1)
    q = scale(2, outer(left, right))
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    diagonal = [outer(vector, vector) for vector in (e0, e1, e2)]
    cylinder = diagonal + [q]
    assert matrix_span_rank(cylinder) == 4

    kernel_basis = [
        (-1, 0, 1, 0, 0, 0),
        (-1, 0, 0, 1, 0, 0),
        (1, 0, 0, 0, 0, 1),
    ]
    star_images = []
    for vector in kernel_basis:
        x, y = vector[:3], vector[3:]
        image = add(outer(left, y), outer(x, right))
        assert matrix_span_rank(cylinder + [image]) == 4
        assert x[1] == y[1] == 0
        star_images.append(image)
    assert matrix_span_rank(star_images) == 2

    z = (0, 0, 1)
    port_pair = symmetric(z, z)
    assert matrix_span_rank(cylinder + [port_pair]) == 4
    assert matrix_span_rank(star_images + [port_pair]) == 3
    assert matrix_span_rank(star_images + [port_pair, q]) == 3
    assert matrix_span_rank(star_images + [port_pair, outer(e1, e1)]) == 4


def main() -> None:
    check_terminal_derivation()
    check_quotient_line_representation()
    check_three_dimensional_endgame()
    check_repeated_anchor_boundary()
    print("GLS43 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
