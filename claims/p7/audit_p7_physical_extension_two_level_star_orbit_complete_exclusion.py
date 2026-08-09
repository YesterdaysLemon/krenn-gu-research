"""Independent stdlib polynomial audit of the two-level P7 exclusion."""

from fractions import Fraction


def clean(poly):
    result = [Fraction(value) for value in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def add(left, right):
    size = max(len(left), len(right))
    return clean(
        [
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
            for i in range(size)
        ]
    )


def scale(value, poly):
    return clean([Fraction(value) * item for item in poly])


def multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return clean(result)


def power(poly, exponent):
    result = (Fraction(1),)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def determinant_fraction(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for col in range(len(work)):
        pivot = next((row for row in range(col, len(work)) if work[row][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        pivot_value = work[col][col]
        result *= pivot_value
        for row in range(col + 1, len(work)):
            factor = work[row][col] / pivot_value
            for k in range(col + 1, len(work)):
                work[row][k] -= factor * work[col][k]
    return result


def determinant_poly(matrix):
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    result = (Fraction(0),)
    for col in range(size):
        minor = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        term = multiply(matrix[0][col], determinant_poly(minor))
        result = add(result, scale((-1) ** col, term))
    return result


def resultant(left, right):
    m = len(left) - 1
    n = len(right) - 1
    left_desc = list(reversed(left))
    right_desc = list(reversed(right))
    matrix = [[Fraction(0) for _ in range(m + n)] for _ in range(m + n)]
    for row in range(n):
        matrix[row][row : row + m + 1] = left_desc
    for offset in range(m):
        row = n + offset
        matrix[row][offset : offset + n + 1] = right_desc
    return determinant_fraction(matrix)


def main():
    one = (Fraction(1),)
    zero = (Fraction(0),)
    t = (Fraction(0), Fraction(1))

    linear_21 = add(scale(2, t), one)
    quadratic_25 = add(add(power(t, 2), scale(2, t)), scale(3, one))
    std_b25 = [
        [add(scale(2, t), scale(3, one)), scale(3, t)],
        [scale(2, one), add(scale(2, t), scale(4, one))],
    ]
    trivial25 = [
        [scale(5, one), scale(10, t), zero],
        [one, add(scale(2, t), scale(8, one)), scale(4, t)],
        [zero, scale(4, one), add(scale(2, t), scale(9, one))],
    ]
    assert determinant_poly(std_b25) == scale(4, quadratic_25)
    assert determinant_poly(trivial25) == scale(360, one)
    product25 = scale(3**4 * 8, power(linear_21, 5))
    product25 = multiply(product25, power(determinant_poly(std_b25), 4))
    product25 = multiply(product25, determinant_poly(trivial25))
    expected25 = scale(5 * 2**14 * 3**6, power(linear_21, 5))
    expected25 = multiply(expected25, power(quadratic_25, 4))
    assert product25 == expected25

    quadratic_34 = add(add(scale(3, power(t, 2)), scale(2, t)), one)
    cubic = add(
        add(power(t, 3), scale(2, power(t, 2))),
        add(scale(3, t), scale(4, one)),
    )
    std_b34 = [
        [add(scale(4, t), scale(2, one)), scale(2, t)],
        [scale(3, one), add(scale(3, t), scale(2, one))],
    ]
    trivial34 = [
        [add(scale(3, t), scale(4, one)), scale(8, t), zero],
        [scale(2, one), add(scale(4, t), scale(6, one)), scale(3, t)],
        [zero, scale(6, one), add(scale(3, t), scale(6, one))],
    ]
    assert determinant_poly(std_b34) == scale(4, quadratic_34)
    assert determinant_poly(trivial34) == scale(36, cubic)
    product34 = power(add(t, scale(2, one)), 6)
    product34 = multiply(product34, power(scale(3, t), 2))
    product34 = multiply(product34, power(scale(24, one), 2))
    product34 = multiply(product34, power(determinant_poly(std_b34), 3))
    product34 = multiply(product34, determinant_poly(trivial34))
    expected34 = scale(2**14 * 3**6, power(t, 2))
    expected34 = multiply(expected34, power(add(t, scale(2, one)), 6))
    expected34 = multiply(expected34, power(quadratic_34, 3))
    expected34 = multiply(expected34, cubic)
    assert product34 == expected34

    primitive_factor_one = add(add(power(t, 2), scale(2, t)), scale(8, one))
    primitive_factor_two = add(
        add(scale(6, power(t, 3)), scale(9, power(t, 2))),
        add(scale(2, t), scale(8, one)),
    )
    assert abs(resultant(cubic, quadratic_34)) == 256
    assert abs(resultant(cubic, primitive_factor_one)) == 256
    assert abs(resultant(cubic, primitive_factor_two)) == 1280

    # Rebuild t^2 times the decisive primitive coefficient from the orbit data.
    v = scale(-1, multiply(t, add(scale(3, t), scale(4, one))))
    tw = scale(-2, primitive_factor_one)  # t*w
    cleared_primitive = scale(
        6,
        multiply(tw, add(scale(4, multiply(v, t)), tw)),
    )
    assert cleared_primitive == scale(
        24, multiply(primitive_factor_one, primitive_factor_two)
    )

    print("AUDIT PASS: exact polynomial block determinants for 2+5 and 3+4")
    print("AUDIT PASS: homogeneous degree-21 factorizations rebuilt without CAS")
    print("AUDIT PASS: cubic and non-full-support walls are pairwise disjoint")
    print("AUDIT PASS: primitive obstruction resultants are 256 and 1280")
    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 numerical_roots=0 graph_enumerations=0")
    print("SCOPE: stars with at least three values and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
