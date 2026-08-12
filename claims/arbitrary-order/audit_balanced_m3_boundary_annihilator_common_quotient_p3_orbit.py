"""Independent stdlib audit of the m=3 common-quotient P3 orbit theorem."""

from fractions import Fraction
from itertools import permutations, product


def matrix_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [value - scale * pivot_value for value, pivot_value in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def permanent_value(vectors):
    return sum(
        vectors[0][sigma[0]] * vectors[1][sigma[1]] * vectors[2][sigma[2]]
        for sigma in permutations(range(3))
    )


def quotient_tensor(a, b):
    basis = ((-Fraction(a), Fraction(1), Fraction(0)), (-Fraction(b), Fraction(0), Fraction(1)))
    return {
        index: permanent_value(tuple(basis[position] for position in index))
        for index in product(range(2), repeat=3)
    }


def hyperdet(tensor):
    x = [tensor[index] for index in product(range(2), repeat=3)]
    x0, x1, x2, x3, x4, x5, x6, x7 = x
    return (
        x0 * x0 * x7 * x7
        + x1 * x1 * x6 * x6
        + x2 * x2 * x5 * x5
        + x4 * x4 * x3 * x3
        - 2
        * (
            x0 * x7 * (x1 * x6 + x2 * x5 + x4 * x3)
            + x1 * x6 * x2 * x5
            + x1 * x6 * x4 * x3
            + x2 * x5 * x4 * x3
        )
        + 4 * (x0 * x3 * x5 * x6 + x7 * x4 * x2 * x1)
    )


def flatten(tensor, mode):
    other = [position for position in range(3) if position != mode]
    rows = [[Fraction(0) for _ in range(4)] for _ in range(2)]
    for first in range(2):
        for column, pair in enumerate(product(range(2), repeat=2)):
            index = [0, 0, 0]
            index[mode] = first
            index[other[0]], index[other[1]] = pair
            rows[first][column] = tensor[tuple(index)]
    return rows


def dot(left, right):
    return sum(Fraction(x) * Fraction(y) for x, y in zip(left, right))


def quadratic_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def quadratic_mul(left, right):
    """Multiply in Q[omega]/(omega^2+omega+1)."""
    ac = left[0] * right[0]
    omega_coefficient = left[0] * right[1] + left[1] * right[0]
    bd = left[1] * right[1]
    return (ac - bd, omega_coefficient - bd)


def quadratic_scale(value, scalar):
    return (value[0] * Fraction(scalar), value[1] * Fraction(scalar))


def quadratic_sum(values):
    total = (Fraction(0), Fraction(0))
    for value in values:
        total = quadratic_add(total, value)
    return total


def quadratic_permanent(vectors):
    return quadratic_sum(
        quadratic_mul(
            quadratic_mul(vectors[0][sigma[0]], vectors[1][sigma[1]]),
            vectors[2][sigma[2]],
        )
        for sigma in permutations(range(3))
    )


def check_singleton_factorization():
    a = ((1, 2, -1), (3, -2, 4), (2, 5, 1))
    b01 = ((1, 0, 2), (-1, 3, 1), (4, 2, -2))
    b02 = ((0, 2, 1), (3, -1, 4), (2, 1, 5))
    b12 = ((2, 1, -1), (0, 3, 2), (4, -2, 1))
    h = ((2, -1, 3), (1, 4, -2), (5, 0, 1))

    beta = (
        sum(a[1][j] * b12[j][k] * a[2][k] for j, k in product(range(3), repeat=2)),
        sum(a[0][i] * b02[i][k] * a[2][k] for i, k in product(range(3), repeat=2)),
        sum(a[0][i] * b01[i][j] * a[1][j] for i, j in product(range(3), repeat=2)),
    )
    direct = sum(
        a[0][i]
        * a[1][j]
        * a[2][k]
        * (h[0][i] * b12[j][k] + b02[i][k] * h[1][j] + b01[i][j] * h[2][k])
        for i, j, k in product(range(3), repeat=3)
    )
    factored = sum(beta[mode] * dot(a[mode], h[mode]) for mode in range(3))
    assert direct == factored
    print("independent singleton factorization: PASS")


def check_support_orbits():
    zero = quotient_tensor(0, 0)
    w_tensor = quotient_tensor(2, 0)
    ghz_tensor = quotient_tensor(2, 3)
    assert all(value == 0 for value in zero.values())
    assert sum(value != 0 for value in w_tensor.values()) == 3
    assert all(matrix_rank(flatten(w_tensor, mode)) == 2 for mode in range(3))
    assert hyperdet(w_tensor) == 0
    assert all(matrix_rank(flatten(ghz_tensor, mode)) == 2 for mode in range(3))
    assert hyperdet(ghz_tensor) == -48 * Fraction(2) ** 2 * Fraction(3) ** 2
    print("independent quotient support census: PASS (zero / W / GHZ)")


def apply_map(linear_map, vector):
    return tuple(dot(row, vector) for row in linear_map)


def check_common_quotient_route():
    beta = (1, 2, 3)
    quotient_rows = ((-2, 1, 0), (-3, 0, 1))
    bars = (
        ((1, 2), (3, 5), (7, 11)),
        ((2, 1), (5, 3), (11, 7)),
        ((1, 4), (2, 9), (3, 16)),
    )
    maps = tuple(
        tuple(tuple(sum(row[p] * quotient_rows[p][j] for p in range(2)) for j in range(3)) for row in bar)
        for bar in bars
    )
    assert all(apply_map(linear_map, beta) == (0, 0, 0) for linear_map in maps)

    q_tensor = quotient_tensor(2, 3)
    for output in product(range(3), repeat=3):
        direct = sum(
            maps[0][output[0]][sigma[0]]
            * maps[1][output[1]][sigma[1]]
            * maps[2][output[2]][sigma[2]]
            for sigma in permutations(range(3))
        )
        factored = sum(
            bars[0][output[0]][i]
            * bars[1][output[1]][j]
            * bars[2][output[2]][k]
            * q_tensor[(i, j, k)]
            for i, j, k in product(range(2), repeat=3)
        )
        assert direct == factored
    print("independent common-quotient contraction: PASS (27 coefficients)")


def check_diagonal_lines_over_quadratic_field():
    a = Fraction(2)
    b = Fraction(3)
    one = (Fraction(1), Fraction(0))
    omega = (Fraction(0), Fraction(1))
    omega_squared = quadratic_mul(omega, omega)
    assert omega_squared == (Fraction(-1), Fraction(-1))
    zero = (Fraction(0), Fraction(0))

    binary_lines = (
        (one, quadratic_scale(omega, a / b)),
        (one, quadratic_scale(omega_squared, a / b)),
    )
    plane_columns = ((-a, -b), (1, 0), (0, 1))
    root_lines = []
    for line in binary_lines:
        root_lines.append(
            tuple(
                quadratic_add(quadratic_scale(line[0], row[0]), quadratic_scale(line[1], row[1]))
                for row in plane_columns
            )
        )
    beta_contractions = [
        quadratic_sum(quadratic_scale(line[index], beta) for index, beta in enumerate((1, a, b)))
        for line in root_lines
    ]
    assert beta_contractions == [zero, zero]
    assert all(all(entry != zero for entry in line) for line in root_lines)

    mixed_a = quadratic_permanent((root_lines[0], root_lines[0], root_lines[1]))
    mixed_b = quadratic_permanent((root_lines[0], root_lines[1], root_lines[1]))
    pure = (
        quadratic_permanent((root_lines[0], root_lines[0], root_lines[0])),
        quadratic_permanent((root_lines[1], root_lines[1], root_lines[1])),
    )
    assert mixed_a == zero and mixed_b == zero
    assert all(value != zero for value in pure)

    for line, scales in zip(root_lines, ((1, 2, 3), (5, 7, 11))):
        matrix = [[quadratic_scale(line[row], scales[column]) for column in range(3)] for row in range(3)]
        assert all(entry != zero for row in matrix for entry in row)
        for row in range(3):
            for column in range(3):
                assert quadratic_mul(matrix[row][column], matrix[0][0]) == quadratic_mul(
                    matrix[row][0], matrix[0][column]
                )
        permanent = quadratic_sum(
            quadratic_mul(quadratic_mul(matrix[0][sigma[0]], matrix[1][sigma[1]]), matrix[2][sigma[2]])
            for sigma in permutations(range(3))
        )
        assert permanent != zero
    print("independent quadratic-field diagonal-line audit: PASS")


def main():
    check_singleton_factorization()
    check_support_orbits()
    check_common_quotient_route()
    check_diagonal_lines_over_quadratic_field()
    print("independent m=3 common-quotient orbit audit: PASS")


if __name__ == "__main__":
    main()
