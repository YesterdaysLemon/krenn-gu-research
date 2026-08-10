"""Independent no-import audit of the switched-circulant no-go."""

VERTICES = tuple(range(7))
DEGREE_TWO = ((2, 0, 0), (1, 1, 0), (1, 0, 1), (0, 2, 0), (0, 1, 1), (0, 0, 2))
DEGREE_FOUR = tuple(
    (first, second, 4 - first - second)
    for first in range(4, -1, -1)
    for second in range(4 - first, -1, -1)
)
SELECTED_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15)
ZERO = ()
ONE = (1,)


def trim(polynomial):
    values = list(polynomial)
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(left, right):
    size = max(len(left), len(right))
    return trim(
        tuple(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        )
    )


def negate(polynomial):
    return tuple(-value for value in polynomial)


def subtract(left, right):
    return add(left, negate(right))


def multiply(left, right):
    if not left or not right:
        return ZERO
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            result[left_degree + right_degree] += left_value * right_value
    return trim(tuple(result))


def exact_divide(numerator, denominator):
    assert denominator
    if not numerator:
        return ZERO
    remainder = list(numerator)
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    denominator_degree = len(denominator) - 1
    denominator_lead = denominator[-1]
    while len(trim(tuple(remainder))) - 1 >= denominator_degree:
        remainder = list(trim(tuple(remainder)))
        shift = len(remainder) - len(denominator)
        value, residue = divmod(remainder[-1], denominator_lead)
        assert residue == 0
        quotient[shift] += value
        for degree, coefficient in enumerate(denominator):
            remainder[degree + shift] -= value * coefficient
    assert not trim(tuple(remainder))
    return trim(tuple(quotient))


def remainder(numerator, denominator):
    work = list(numerator)
    denominator_degree = len(denominator) - 1
    denominator_lead = denominator[-1]
    while len(trim(tuple(work))) - 1 >= denominator_degree:
        work = list(trim(tuple(work)))
        shift = len(work) - len(denominator)
        value, residue = divmod(work[-1], denominator_lead)
        assert residue == 0
        for degree, coefficient in enumerate(denominator):
            work[degree + shift] -= value * coefficient
    return trim(tuple(work))


def bareiss_determinant(matrix):
    work = [[tuple(entry) for entry in row] for row in matrix]
    size = len(work)
    sign = 1
    previous = ONE
    for column in range(size - 1):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        assert pivot is not None
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for inner in range(column + 1, size):
                numerator = subtract(
                    multiply(work[row][inner], pivot_value),
                    multiply(work[row][column], work[column][inner]),
                )
                work[row][inner] = exact_divide(numerator, previous)
            work[row][column] = ZERO
        previous = pivot_value
    determinant = work[-1][-1]
    return negate(determinant) if sign < 0 else determinant


def distance(left, right):
    difference = (left - right) % 7
    return min(difference, 7 - difference)


def edge_monomial(left, right):
    exponent = [0, 0, 0]
    exponent[distance(left, right) - 1] = 1
    return tuple(exponent)


def add_exponents(left, right):
    return tuple(first + second for first, second in zip(left, right, strict=True))


def four_hafnian(vertices):
    first, second, third, fourth = sorted(vertices)
    result = {}
    for left, right in (
        (((first, second), (third, fourth))),
        (((first, third), (second, fourth))),
        (((first, fourth), (second, third))),
    ):
        exponent = add_exponents(edge_monomial(*left), edge_monomial(*right))
        result[exponent] = result.get(exponent, 0) + 1
    return result


def character_quadrics():
    equations = []
    for excluded_distance in (1, 2, 3):
        five_set = tuple(
            vertex for vertex in VERTICES if vertex not in (0, excluded_distance)
        )
        equation = {}
        for omitted in five_set:
            four_set = tuple(vertex for vertex in five_set if vertex != omitted)
            for exponent, coefficient in four_hafnian(four_set).items():
                term = (0,) * omitted + (coefficient,)
                equation[exponent] = add(equation.get(exponent, ZERO), term)
        equations.append(equation)
    return equations


def macaulay_matrix(equations):
    rows = []
    for equation in equations:
        for multiplier in DEGREE_TWO:
            coefficients = {
                add_exponents(exponent, multiplier): value
                for exponent, value in equation.items()
            }
            rows.append([coefficients.get(monomial, ZERO) for monomial in DEGREE_FOUR])
    return rows


def main():
    equations = character_quadrics()
    matrix = macaulay_matrix(equations)
    selected = [matrix[index] for index in SELECTED_ROWS]
    determinant = bareiss_determinant(selected)
    assert sum(determinant) == -3_149_280
    cyclotomic = (1, 1, 1, 1, 1, 1, 1)
    assert remainder(determinant, cyclotomic) == (0, 0, 0, -73_728, -73_728)
    print("AUDIT PASS: independent C7 symbol and degree-four Macaulay matrix")
    print("AUDIT PASS: determinant at 1 = -2^5*3^9*5")
    print("AUDIT PASS: determinant mod Phi_7 = -2^13*3^2*t^3*(t+1)")
    print("searches=0 parameter_enumerations=0 finite_fields=0 numerics=0")


if __name__ == "__main__":
    main()
