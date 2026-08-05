"""Independent no-import dual-number audit of the dominance certificate."""


EXPECTED_DETERMINANT = 10622643353619573315207168
SELECTED_PARAMETERS = tuple(range(17)) + (18, 19, 20)
SUBSETS = {
    0: ((),),
    1: ((0,), (1,), (2,)),
    2: ((0, 1), (0, 2), (1, 2)),
    3: ((0, 1, 2),),
}


class Dual:
    def __init__(self, value, gradient):
        self.value = value
        self.gradient = tuple(gradient)

    @staticmethod
    def constant(value):
        return Dual(value, (0,) * 20)

    @staticmethod
    def parameter(value, derivative_index):
        gradient = [0] * 20
        if derivative_index is not None:
            gradient[derivative_index] = 1
        return Dual(value, gradient)

    def __add__(self, other):
        if not isinstance(other, Dual):
            other = Dual.constant(other)
        return Dual(
            self.value + other.value,
            (
                left + right
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if not isinstance(other, Dual):
            other = Dual.constant(other)
        return Dual(
            self.value * other.value,
            (
                left * other.value + self.value * right
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    def __rmul__(self, other):
        return self * other


def permutations(values):
    if not values:
        return [()]
    answer = []
    for index, value in enumerate(values):
        remainder = values[:index] + values[index + 1 :]
        for tail in permutations(remainder):
            answer.append((value,) + tail)
    return answer


def permanent(matrix):
    if not matrix:
        return Dual.constant(1)
    answer = Dual.constant(0)
    for permutation in permutations(tuple(range(len(matrix)))):
        term = Dual.constant(1)
        for row in range(len(matrix)):
            term = term * matrix[row][permutation[row]]
        answer = answer + term
    return answer


def submatrix(matrix, rows, columns):
    return [[matrix[row][column] for column in columns] for row in rows]


def complement(subset):
    return tuple(index for index in range(3) if index not in subset)


def bareiss_determinant(matrix):
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
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % denominator == 0
                work[row][column] = numerator // denominator
        denominator = pivot
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
    return sign * work[-1][-1]


def main():
    values = (
        1, 2, 0,
        0, 1, 3,
        2, 0, 1,
        1, 0, 2,
        3, 1, 0,
        0, 2, 1,
        2, 1, 0,
        1, 3, 2,
        0, 1, 4,
    )
    derivative_positions = {
        parameter: index for index, parameter in enumerate(SELECTED_PARAMETERS)
    }
    parameters = [
        Dual.parameter(value, derivative_positions.get(index))
        for index, value in enumerate(values)
    ]
    y = [parameters[row * 3 : row * 3 + 3] for row in range(3)]
    z = [parameters[9 + row * 3 : 9 + row * 3 + 3] for row in range(3)]
    w = [parameters[18 + row * 3 : 18 + row * 3 + 3] for row in range(3)]

    coordinates = []
    for degree in range(4):
        subsets = SUBSETS[degree]
        for core_modes in subsets:
            for core_sources in subsets:
                response = Dual.constant(0)
                for exterior_rows in subsets:
                    for exterior_columns in subsets:
                        response += (
                            permanent(submatrix(y, core_modes, exterior_columns))
                            * permanent(submatrix(z, exterior_rows, core_sources))
                            * permanent(
                                submatrix(
                                    w,
                                    complement(exterior_rows),
                                    complement(exterior_columns),
                                )
                            )
                        )
                coordinates.append(response)

    assert len(coordinates) == 20
    jacobian_minor = [list(coordinate.gradient) for coordinate in coordinates]
    determinant = bareiss_determinant(jacobian_minor)
    assert determinant == EXPECTED_DETERMINANT

    print("independent no-import boundary-jet dominance audit: PASS")
    print(f"dual-number Bareiss determinant = {determinant}")
    print("fixed 20-coordinate characteristic-zero certificate; no family census")


if __name__ == "__main__":
    main()
