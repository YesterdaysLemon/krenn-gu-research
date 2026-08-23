"""Independent no-import audit for GLS51.

Only the Python standard library is used.  The determinant is expanded with
custom sparse polynomials, the zero relation and crossed square are censused
projectively over F_3, and the sharpness control is replayed with Fraction.
"""

from fractions import Fraction
from itertools import permutations, product


NVAR = 22
ZERO_MONOMIAL = (0,) * NVAR


def poly_add(*values):
    result = {}
    for value in values:
        for monomial, coefficient in value.items():
            result[monomial] = result.get(monomial, 0) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def poly_scale(value, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in value.items()
        if scalar * coefficient
    }


def poly_mul(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_monomial[index] + right_monomial[index]
                for index in range(NVAR)
            )
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def poly_product(*values):
    result = {ZERO_MONOMIAL: 1}
    for value in values:
        result = poly_mul(result, value)
    return result


def variable(index):
    monomial = [0] * NVAR
    monomial[index] = 1
    return {tuple(monomial): 1}


def permutation_sign(value):
    inversions = sum(
        value[left] > value[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def test_custom_determinant() -> None:
    gamma = variable(0)
    alpha = [variable(1 + index) for index in range(3)]
    a = [variable(4 + index) for index in range(3)]
    b = [variable(7 + index) for index in range(3)]
    z = [variable(10 + index) for index in range(3)]
    w = [variable(13 + index) for index in range(3)]
    lu = [variable(16 + index) for index in range(3)]
    lv = [variable(19 + index) for index in range(3)]
    lambda_u = poly_add(*(poly_mul(lu[index], z[index]) for index in range(3)))
    lambda_v = poly_add(*(poly_mul(lv[index], w[index]) for index in range(3)))

    matrix = []
    for row in range(3):
        matrix_row = []
        for column in range(3):
            value = poly_scale(
                poly_product(lambda_u, lambda_v, a[row], b[column]), 2
            )
            if row == column:
                value = poly_add(
                    value, poly_product(gamma, alpha[row], z[row], w[row])
                )
            matrix_row.append(value)
        matrix.append(matrix_row)

    determinant = {}
    for permutation in permutations(range(3)):
        term = poly_product(
            *(matrix[row][permutation[row]] for row in range(3))
        )
        determinant = poly_add(
            determinant, poly_scale(term, permutation_sign(permutation))
        )

    leading = poly_product(
        gamma, gamma, gamma, *alpha, *z, *w
    )
    corrections = []
    for index in range(3):
        others = [value for value in range(3) if value != index]
        corrections.append(
            poly_product(
                a[index],
                b[index],
                alpha[others[0]],
                alpha[others[1]],
                z[others[0]],
                z[others[1]],
                w[others[0]],
                w[others[1]],
            )
        )
    expected = poly_add(
        leading,
        poly_scale(
            poly_product(
                gamma,
                gamma,
                lambda_u,
                lambda_v,
                poly_add(*corrections),
            ),
            2,
        ),
    )
    assert determinant == expected


PRIME = 3


def inverse(value):
    return pow(value, PRIME - 2, PRIME)


def canonical(vector):
    for entry in vector:
        if entry % PRIME:
            scale = inverse(entry % PRIME)
            return tuple((scale * item) % PRIME for item in vector)
    raise ValueError("zero vector has no projective class")


def projective_vectors():
    return sorted(
        {
            canonical(vector)
            for vector in product(range(PRIME), repeat=6)
            if any(vector)
        }
    )


def mu_mod(left, right):
    x, y = left[:3], left[3:]
    xp, yp = right[:3], right[3:]
    return tuple(
        (x[row] * yp[column] + xp[row] * y[column]) % PRIME
        for row in range(3)
        for column in range(3)
    )


def broad_type(vector):
    x_nonzero = any(vector[:3])
    y_nonzero = any(vector[3:])
    if x_nonzero and not y_nonzero:
        return "X"
    if y_nonzero and not x_nonzero:
        return "Y"
    if x_nonzero and y_nonzero:
        return "T"
    raise AssertionError("projective zero")


def pure_diagonal(matrix, color):
    expected_position = 3 * color + color
    return matrix[expected_position] != 0 and all(
        entry == 0
        for position, entry in enumerate(matrix)
        if position != expected_position
    )


def test_projective_zero_and_crossed_square() -> None:
    vectors = projective_vectors()
    assert len(vectors) == 364
    zero_neighbors = [[] for _ in vectors]
    matched = [[[] for _ in vectors] for _ in range(2)]
    zero_counts = {"X": 0, "Y": 0, "T": 0}

    for left_index, left in enumerate(vectors):
        for right_index, right in enumerate(vectors):
            matrix = mu_mod(left, right)
            if not any(matrix):
                zero_neighbors[left_index].append(right_index)
                left_type = broad_type(left)
                right_type = broad_type(right)
                assert left_type == right_type
                if left_type == "T":
                    expected = canonical(left[:3] + tuple(-entry % PRIME for entry in left[3:]))
                    assert right == expected
                zero_counts[left_type] += 1
            for color in range(2):
                if pure_diagonal(matrix, color):
                    matched[color][left_index].append(right_index)

    assert all(zero_counts[value] > 0 for value in zero_counts)
    assert all(
        len(zero_neighbors[index]) == 1
        for index, vector in enumerate(vectors)
        if broad_type(vector) == "T"
    )

    crossed_types = set()
    solution_count = 0
    for ui in range(len(vectors)):
        for vi in matched[0][ui]:
            for uj in zero_neighbors[vi]:
                for vj in matched[1][uj]:
                    if vj in zero_neighbors[ui]:
                        solution_count += 1
                        crossed_types.add(
                            (broad_type(vectors[ui]), broad_type(vectors[uj]))
                        )
    assert solution_count > 0
    assert crossed_types == {("X", "Y"), ("Y", "X")}


def vec_scale(value, scalar):
    return tuple(scalar * entry for entry in value)


def outer_q(left, right):
    return tuple(left[row] * right[column] for row in range(3) for column in range(3))


def mat_add(*values):
    return tuple(sum(value[index] for value in values) for index in range(9))


def matrix_unit(row, column):
    return tuple(Fraction(int(index == 3 * row + column)) for index in range(9))


def rational_rank(columns):
    matrix = [list(column) for column in zip(*columns)]
    row = 0
    for column in range(len(columns)):
        pivot = next(
            (index for index in range(row, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][column]
        matrix[row] = [entry / scale for entry in matrix[row]]
        for index in range(len(matrix)):
            if index == row or not matrix[index][column]:
                continue
            scale = matrix[index][column]
            matrix[index] = [
                matrix[index][position] - scale * matrix[row][position]
                for position in range(len(columns))
            ]
        row += 1
        if row == len(matrix):
            break
    return row


def test_fraction_sharpness_and_hyperplanes() -> None:
    zero = (Fraction(0),) * 3
    e = [
        tuple(Fraction(int(index == color)) for index in range(3))
        for color in range(3)
    ]
    a = e[0]
    b = vec_scale(e[0], Fraction(-1, 2))
    xu = [vec_scale(e[0], -1), zero, e[2]]
    yu = [vec_scale(e[0], Fraction(1, 2)), e[1], zero]
    xv = [vec_scale(e[0], -1), e[1], zero]
    yv = [vec_scale(e[0], Fraction(1, 2)), zero, e[2]]
    gu = [mat_add(outer_q(a, yu[d]), outer_q(xu[d], b)) for d in range(3)]
    gv = [mat_add(outer_q(a, yv[d]), outer_q(xv[d], b)) for d in range(3)]
    muv = [
        [mat_add(outer_q(xu[i], yv[j]), outer_q(xv[j], yu[i])) for j in range(3)]
        for i in range(3)
    ]
    for i, j in product(range(3), repeat=2):
        terms = [muv[i][j]]
        if j == 0:
            terms.append(gu[i])
        if i == 0:
            terms.append(gv[j])
        expected = matrix_unit(i, i) if i == j else (Fraction(0),) * 9
        assert mat_add(*terms) == expected

    joint_u = [xu[d] + yu[d] for d in range(3)]
    joint_v = [xv[d] + yv[d] for d in range(3)]
    assert rational_rank(joint_u) == rational_rank(joint_v) == 3
    pair_columns = gu + gv + [muv[i][j] for i, j in product(range(3), repeat=2)]
    assert rational_rank(pair_columns) == 7

    deck_color = {"u": 0, "v": 1, "w": 2}
    survivors = []
    for left, right, opposite in (("u", "v", "w"), ("u", "w", "v"), ("v", "w", "u")):
        colors = set(range(3)) - {deck_color[left], deck_color[right]}
        colors &= {deck_color[opposite]}
        assert len(colors) == 1
        survivors.extend(colors)
    assert set(survivors) == {0, 1, 2}
    assert rational_rank([matrix_unit(color, color) for color in survivors]) == 3


def main() -> None:
    test_custom_determinant()
    test_projective_zero_and_crossed_square()
    test_fraction_sharpness_and_hyperplanes()
    print("GLS51 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
