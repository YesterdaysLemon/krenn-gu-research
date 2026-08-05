"""Independent no-import audit of the P7 h=0 pair-projection theorem."""

from fractions import Fraction
from itertools import combinations

EDGES = tuple(combinations(range(5), 2))
N_VARIABLES = 10


def polynomial_add(left, right, sign=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        value = result.get(monomial, 0) + sign * coefficient
        if value:
            result[monomial] = value
        elif monomial in result:
            del result[monomial]
    return result


def polynomial_multiply(left, right):
    result = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                a + b for a, b in zip(monomial_left, monomial_right, strict=True)
            )
            coefficient = coefficient_left * coefficient_right
            result[monomial] = result.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def variable(index):
    exponent = [0] * N_VARIABLES
    exponent[index] = 1
    return {tuple(exponent): 1}


def pentad_terms():
    # Each item is (sign, five edge labels), independently transcribed from (6).
    return (
        (1, ((0, 1), (0, 2), (1, 3), (2, 4), (3, 4))),
        (-1, ((0, 1), (0, 2), (1, 4), (2, 3), (3, 4))),
        (-1, ((0, 1), (0, 3), (1, 2), (2, 4), (3, 4))),
        (1, ((0, 1), (0, 3), (1, 4), (2, 3), (2, 4))),
        (1, ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4))),
        (-1, ((0, 1), (0, 4), (1, 3), (2, 3), (2, 4))),
        (1, ((0, 2), (0, 3), (1, 2), (1, 4), (3, 4))),
        (-1, ((0, 2), (0, 3), (1, 3), (1, 4), (2, 4))),
        (-1, ((0, 2), (0, 4), (1, 2), (1, 3), (3, 4))),
        (1, ((0, 2), (0, 4), (1, 3), (1, 4), (2, 3))),
        (-1, ((0, 3), (0, 4), (1, 2), (1, 4), (2, 3))),
        (1, ((0, 3), (0, 4), (1, 2), (1, 3), (2, 4))),
    )


def evaluate_pentad(values):
    total = 0
    for sign, factors in pentad_terms():
        product = sign
        for edge in factors:
            product *= values[edge]
        total += product
    return total


def audit_sparse_hyperbolic_identity():
    a = [variable(i) for i in range(5)]
    b = [variable(i + 5) for i in range(5)]
    gram = {}
    for i, j in EDGES:
        gram[(i, j)] = polynomial_add(
            polynomial_multiply(a[i], b[j]), polynomial_multiply(b[i], a[j])
        )

    total = {}
    one = {(0,) * N_VARIABLES: 1}
    for sign, factors in pentad_terms():
        product = one
        for edge in factors:
            product = polynomial_multiply(product, gram[edge])
        total = polynomial_add(total, product, sign)
    assert total == {}


def rational_rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def matrix_vector(matrix, vector):
    return [
        sum(Fraction(value) * Fraction(coordinate) for value, coordinate in zip(row, vector, strict=True))
        for row in matrix
    ]


def audit_simple_incidence_boundary():
    w = list(range(1, 13))
    gamma = [[0] * 12 for _ in range(14)]
    gamma[0][0] = 1
    for j in range(1, 12):
        gamma[j + 2][0] = -w[j]
        gamma[j + 2][j] = 1
    quotient = gamma[3:]
    assert rational_rank(gamma) == 12
    assert rational_rank(quotient) == 11
    assert matrix_vector(quotient, w) == [0] * 11
    assert matrix_vector(gamma, w) == [1] + [0] * 13
    assert evaluate_pentad(dict(zip(EDGES, w[:10], strict=True))) == -6


def audit_projective_alignment():
    u0 = (1, 2, 3, 4, 5)
    u1 = (2, -1, 4, 1, 3)
    khat = {
        (i, j): u0[i] * u1[j] + u0[j] * u1[i]
        for i, j in EDGES
    }
    assert evaluate_pentad(khat) == 0

    tau = Fraction(3)
    y = {edge: Fraction(value, 3) for edge, value in khat.items()}
    assert all(
        y[e] * khat[f] - y[f] * khat[e] == 0
        for e, f in combinations(EDGES, 2)
    )
    assert all(tau * y[edge] == khat[edge] for edge in EDGES)

    perturbed = dict(y)
    perturbed[EDGES[0]] += 1
    assert any(
        perturbed[e] * khat[f] - perturbed[f] * khat[e] != 0
        for e, f in combinations(EDGES, 2)
    )


def main():
    audit_sparse_hyperbolic_identity()
    audit_simple_incidence_boundary()
    audit_projective_alignment()
    print("PASS: independent P7 h=0 pair-projection audit")
    print("sparse_hyperbolic_pentad=0")
    print("ambient_simple_incidence_bad_pentad=-6")
    print("projective_pair_alignment=exact")
    print("graph_or_parameter_search_used=False")


if __name__ == "__main__":
    main()
