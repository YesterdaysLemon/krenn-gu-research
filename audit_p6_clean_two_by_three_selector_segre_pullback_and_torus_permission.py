"""Independent no-import audit of the clean P6 Segre-pullback theorem."""

from itertools import combinations, permutations

Monomial = tuple[int, int, int, int]
Polynomial = dict[Monomial, int]


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_monomial[index] + right_monomial[index] for index in range(4)
            )
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return clean(result)


def scale(poly: Polynomial, scalar: int) -> Polynomial:
    return clean({monomial: scalar * coefficient for monomial, coefficient in poly.items()})


def variable_power(index: int, power: int) -> Polynomial:
    monomial = [0, 0, 0, 0]
    monomial[index] = power
    return {tuple(monomial): 1}


def monomial(exponents: tuple[int, int, int, int]) -> Polynomial:
    return {exponents: 1}


def permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def symbolic_fan_matrix() -> list[list[Polynomial]]:
    columns: list[list[Polynomial]] = []
    for i, j in combinations(range(4), 2):
        exponents_ij_2 = [0, 0, 0, 0]
        exponents_ij_2[i] = 1
        exponents_ij_2[j] = 2
        exponents_ji_2 = [0, 0, 0, 0]
        exponents_ji_2[i] = 2
        exponents_ji_2[j] = 1
        exponents_ij_3 = [0, 0, 0, 0]
        exponents_ij_3[i] = 1
        exponents_ij_3[j] = 3
        exponents_ji_3 = [0, 0, 0, 0]
        exponents_ji_3[i] = 3
        exponents_ji_3[j] = 1
        columns.append(
            [
                {(0, 0, 0, 0): 2},
                add(variable_power(i, 2), variable_power(j, 2)),
                add(variable_power(i, 3), variable_power(j, 3)),
                add(variable_power(i, 1), variable_power(j, 1)),
                add(monomial(tuple(exponents_ij_2)), monomial(tuple(exponents_ji_2))),
                add(monomial(tuple(exponents_ij_3)), monomial(tuple(exponents_ji_3))),
            ]
        )
    return [[columns[column][row] for column in range(6)] for row in range(6)]


def polynomial_determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    result: Polynomial = {}
    for column_order in permutations(range(6)):
        term: Polynomial = {(0, 0, 0, 0): permutation_sign(column_order)}
        for row, column in enumerate(column_order):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return result


def expected_determinant() -> Polynomial:
    result: Polynomial = {(0, 0, 0, 0): -2}
    for i, j in combinations(range(4), 2):
        difference = add(variable_power(i, 1), scale(variable_power(j, 1), -1))
        result = multiply(result, multiply(difference, difference))
    parameter_sum: Polynomial = {}
    for index in range(4):
        parameter_sum = add(parameter_sum, variable_power(index, 1))
    return multiply(result, parameter_sum)


def symbolic_determinant_audit() -> None:
    actual = polynomial_determinant(symbolic_fan_matrix())
    expected = expected_determinant()
    assert actual == expected
    assert max(sum(monomial_value) for monomial_value in actual) == 13
    print("independent sparse-polynomial Vandermonde-square identity: PASS")


def integer_fan(parameters: tuple[int, int, int, int]) -> list[list[int]]:
    columns: list[list[int]] = []
    for left, right in combinations(parameters, 2):
        columns.append(
            [
                2,
                left**2 + right**2,
                left**3 + right**3,
                left + right,
                left * right**2 + right * left**2,
                left * right**3 + right * left**3,
            ]
        )
    return [[columns[column][row] for column in range(6)] for row in range(6)]


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(len(work) - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                row
                for row in range(pivot_index + 1, len(work))
                if work[row][pivot_index] != 0
            )
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, len(work)):
            for column in range(pivot_index + 1, len(work)):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


def matrix_vector(matrix: list[list[int]], vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(entry * value for entry, value in zip(row, vector, strict=True)) for row in matrix)


def kronecker(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left_value * right_value for left_value in left for right_value in right)


def fixed_certificate_audit() -> None:
    matrix = integer_fan((1, 2, 3, 4))
    assert bareiss_determinant(matrix) == -2880

    left_factors = ((1, 1), (1, 1), (1, 2))
    right_factors = ((1, 1, 1), (1, 2, 3), (1, 4, 9))
    face_columns = (
        (14, -24, 20, 15, -29, 9),
        (10, -33, 36, 30, -58, 18),
        (2, 38, -45, -30, 73, -23),
    )
    scales = (10, 6, 30)
    for left, right, faces, factor in zip(
        left_factors, right_factors, face_columns, scales, strict=True
    ):
        expected = tuple(factor * value for value in kronecker(left, right))
        observed = matrix_vector(matrix, faces)
        assert observed == expected
        assert all(faces)
        for first, second in combinations(range(3), 2):
            assert (
                observed[first] * observed[3 + second]
                - observed[second] * observed[3 + first]
                == 0
            )

    left_rank_minor = left_factors[0][0] * left_factors[2][1] - left_factors[2][0] * left_factors[0][1]
    assert left_rank_minor == 1
    right_matrix = [[right_factors[column][row] for column in range(3)] for row in range(3)]
    assert bareiss_determinant(right_matrix) == 2
    print("independent integer fan and three-colour torus certificate: PASS")


def bilinear(matrix: tuple[tuple[int, ...], ...], left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row in range(3)
        for column in range(3)
    )


def shore_audit() -> None:
    shore = ((-1, 1, 0), (0, 0, 0), (0, 0, 0))
    common = (1, 1, 1)
    selected = (1, 2, 3)
    assert bilinear(shore, common, common) == 0
    assert bilinear(shore, common, selected) == 1
    assert tuple(
        target * left * right
        for target, left, right in zip((10, 3, 10), common, selected, strict=True)
    ) == (10, 6, 30)
    assert all(
        coordinate
        for parameter in (1, 2, 3, 4)
        for coordinate in (1, parameter, parameter**2, parameter**3)
    )
    print("independent zero-coupled nonzero-shore audit: PASS")


def main() -> None:
    symbolic_determinant_audit()
    fixed_certificate_audit()
    shore_audit()
    print("P6 clean 2x3 Segre-pullback independent audit: PASS")


if __name__ == "__main__":
    main()
