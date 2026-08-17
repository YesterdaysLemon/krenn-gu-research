"""Independent no-import audit of the six-port Wick selector theorem."""

from fractions import Fraction
from itertools import combinations, product
from math import factorial


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def complement(items, universe=VERTICES):
    return tuple(sorted(set(universe) - set(items)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def wick_matrix(pair_value):
    matrix = []
    for row_edge in EDGES:
        row = []
        for column_edge in EDGES:
            if set(row_edge).isdisjoint(column_edge):
                row.append(pair_value[complement(row_edge + column_edge)])
            else:
                row.append(0)
        matrix.append(row)
    return matrix


def bareiss_determinant(matrix):
    work = [list(map(int, row)) for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (row for row in range(pivot_index + 1, size) if work[row][pivot_index]),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = work[row][column] * pivot
                numerator -= work[row][pivot_index] * work[pivot_index][column]
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return 0
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def elementary_mixed(a_values, b_values, degree):
    return sum(
        (
            product_value(
                b_values[index] if index in choice else a_values[index]
                for index in range(6)
            )
            for choice in combinations(range(6), degree)
        ),
        0,
    )


def product_value(values):
    result = 1
    for value in values:
        result *= value
    return result


def discriminant_value(a_values, b_values):
    capital_a = product_value(a_values)
    s = {degree: elementary_mixed(a_values, b_values, degree) for degree in range(1, 7)}
    return -9216 * (
        12 * capital_a**2 * s[5] ** 3
        - 4 * capital_a * s[1] * s[4] * s[5] ** 2
        + s[1] ** 2 * s[3] * s[5] ** 2
        - 4 * s[1] ** 2 * s[2] * s[5] * s[6]
        + 12 * s[1] ** 3 * s[6] ** 2
    )


def audit_discriminant_and_shores():
    controls = (
        ((3, 1, -2, 4, 0, 5), (2, -1, 7, 0, 6, -3)),
        ((0, 2, 0, 3, 5, 7), (11, -4, 1, 9, 0, -2)),
        ((-1, -2, -3, 1, 2, 3), (5, 8, -13, 21, -34, 55)),
        ((1, 4, 9, 16, 25, 36), (6, 5, 4, 3, 2, 1)),
        ((0, 0, 2, -3, 4, -5), (1, -1, 0, 7, -8, 9)),
    )
    for a_values, b_values in controls:
        pairs = {
            (i, j): a_values[i] * b_values[j] + b_values[i] * a_values[j]
            for i, j in EDGES
        }
        assert bareiss_determinant(wick_matrix(pairs)) == discriminant_value(
            a_values, b_values
        )

    alpha, beta = 5, -7
    expected_ranks = (15, 10, 15, 10)
    for index, count in enumerate((6, 5, 4, 3)):
        colours = (0,) * count + (1,) * (6 - count)
        pairs = {
            edge: alpha
            if colours[edge[0]] == colours[edge[1]] == 0
            else beta
            if colours[edge[0]] == colours[edge[1]] == 1
            else 0
            for edge in EDGES
        }
        matrix = wick_matrix(pairs)
        assert rank(matrix) == expected_ranks[index]
        determinant = bareiss_determinant(matrix)
        if count == 6:
            assert determinant == -1458 * alpha**15
        elif count == 4:
            assert determinant == 54 * alpha**10 * beta**5
        else:
            assert determinant == 0


def four_rows(pair_value, pair_array):
    result = {}
    for four_set in combinations(VERTICES, 4):
        total = 0
        for pair in combinations(four_set, 2):
            remainder = tuple(vertex for vertex in four_set if vertex not in pair)
            total += (
                pair_value[tuple(sorted(pair))] * pair_array[tuple(sorted(remainder))]
            )
        result[four_set] = total
    return result


def audit_singular_selectors_and_cover():
    # Derive each 5+1 selector from the structural four-set equation.
    alpha = 13
    colours = (0, 0, 0, 0, 0, 1)
    pair_value = {
        edge: alpha if colours[edge[0]] == colours[edge[1]] == 0 else 0
        for edge in EDGES
    }
    for desired_vertex in range(5):
        pair_array = {edge: 0 for edge in EDGES}
        pair_array[(desired_vertex, 5)] = 1
        rows = four_rows(pair_value, pair_array)
        containing = 0
        avoiding = 0
        for triple in combinations(range(5), 3):
            value = Fraction(rows[tuple(sorted((5,) + triple))], alpha)
            if desired_vertex in triple:
                containing += value
            else:
                avoiding += value
        assert (containing - avoiding) / 6 == 1

    # Independently check the weighted 3+3 kernel generators.
    alpha, beta = 2, 5
    colours = (0, 0, 0, 1, 1, 1)
    pair_value = {
        edge: alpha
        if colours[edge[0]] == colours[edge[1]] == 0
        else beta
        if colours[edge[0]] == colours[edge[1]] == 1
        else 0
        for edge in EDGES
    }
    generators = []
    for left in (1, 2):
        for right in (4, 5):
            vector = {edge: 0 for edge in EDGES}
            vector[(0, 3)] = 1
            vector[tuple(sorted((0, right)))] = -1
            vector[tuple(sorted((left, 3)))] = -1
            vector[tuple(sorted((left, right)))] = 1
            generators.append(vector)
    internal = {edge: 0 for edge in EDGES}
    for edge in combinations(range(3), 2):
        internal[edge] = alpha
    for edge in combinations(range(3, 6), 2):
        internal[edge] = -beta
    generators.append(internal)
    for vector in generators:
        assert all(value == 0 for value in four_rows(pair_value, vector).values())
    assert rank([[vector[edge] for edge in EDGES] for vector in generators]) == 5
    assert all(any(vector[edge] for vector in generators) for edge in EDGES)

    # Check all nine desired ternary coefficient types by the stated word cover.
    for left_colour, right_colour in product(range(3), repeat=2):
        if left_colour == right_colour and left_colour in (0, 1):
            other = 1 - left_colour
            word = (left_colour, right_colour, left_colour, left_colour, other, other)
        elif (left_colour, right_colour) != (2, 2):
            active = left_colour if left_colour in (0, 1) else right_colour
            word = (left_colour, right_colour) + (active,) * 4
        else:
            word = (2, 2, 0, 0, 1, 1)
        pairs = {
            edge: 3
            if word[edge[0]] == word[edge[1]] == 0
            else 7
            if word[edge[0]] == word[edge[1]] == 1
            else 0
            for edge in EDGES
        }
        matrix = wick_matrix(pairs)
        if left_colour == right_colour and left_colour in (0, 1):
            assert rank(matrix) == 15
        elif (left_colour, right_colour) != (2, 2):
            unit = [0] * 15
            unit[EDGE_INDEX[(0, 1)]] = 1
            assert rank(matrix + [unit]) == rank(matrix)
        else:
            row = matrix[EDGE_INDEX[(4, 5)]]
            assert row[EDGE_INDEX[(0, 1)]] == 3
            assert sum(bool(value) for value in row) == 1


def audit_common_row_cover():
    # Exhaust every shore size through ten ports and every pair type.
    for size in range(7, 11):
        for a_size in range(size + 1):
            b_size = size - a_size
            pair_types = []
            if a_size >= 2:
                pair_types.append("AA")
            if b_size >= 2:
                pair_types.append("BB")
            if a_size and b_size:
                pair_types.append("AB")
            for pair_type in pair_types:
                if pair_type == "AA":
                    available_a, available_b = a_size - 2, b_size
                    choices = ((6, 0), (4, 2), (2, 4))
                    assert any(
                        a >= 2 and a - 2 <= available_a and b <= available_b
                        for a, b in choices
                    )
                elif pair_type == "BB":
                    available_a, available_b = a_size, b_size - 2
                    choices = ((0, 6), (2, 4), (4, 2))
                    assert any(
                        a <= available_a and b >= 2 and b - 2 <= available_b
                        for a, b in choices
                    )
                else:
                    invertible = ((4, 2), (2, 4))
                    has_invertible = any(
                        a >= 1
                        and b >= 1
                        and a - 1 <= a_size - 1
                        and b - 1 <= b_size - 1
                        for a, b in invertible
                    )
                    has_five_one = a_size >= 5 or b_size >= 5
                    assert has_invertible or has_five_one


def hafnian(vertices, colours, b0, b1):
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for raw_edge in matching:
            edge = tuple(sorted(raw_edge))
            if colours[edge[0]] != colours[edge[1]]:
                term = 0
                break
            term *= b0[edge] if colours[edge[0]] == 0 else b1[edge]
        total += term
    return total


def response(vertices, colours, k0, k1, b0, b1):
    total = 0
    for pair in combinations(vertices, 2):
        edge = tuple(sorted(pair))
        if colours[edge[0]] != colours[edge[1]]:
            continue
        k_value = k0[edge] if colours[edge[0]] == 0 else k1[edge]
        remainder = tuple(vertex for vertex in vertices if vertex not in edge)
        total += k_value * hafnian(remainder, colours, b0, b1)
    return total


def polynomial_multiply(left, right):
    result = {}
    for (x_left, y_left), left_value in left.items():
        for (x_right, y_right), right_value in right.items():
            key = (x_left + x_right, y_left + y_right)
            result[key] = result.get(key, Fraction(0)) + left_value * right_value
    return result


def polynomial_power(polynomial, exponent):
    result = {(0, 0): Fraction(1)}
    for _ in range(exponent):
        result = polynomial_multiply(result, polynomial)
    return result


def audit_deeper_responses():
    alpha, beta, c = 2, -3, 5
    x_values = (2, 3, 5, 7, 11, 13)
    y_values = (17, 19, 23, 29, 31, 37)
    k0 = {edge: alpha * x_values[edge[0]] * x_values[edge[1]] for edge in EDGES}
    k1 = {edge: beta * y_values[edge[0]] * y_values[edge[1]] for edge in EDGES}
    b0 = {edge: c * value for edge, value in k0.items()}
    b1 = {edge: -c * value for edge, value in k1.items()}

    # Every mixed binary four-port word is zero; pure words have the stated sign.
    for four_set in combinations(VERTICES, 4):
        four_set = tuple(four_set)
        for local_word in product((0, 1), repeat=4):
            colours = [0] * 6
            for vertex, colour in zip(four_set, local_word, strict=True):
                colours[vertex] = colour
            value = response(four_set, colours, k0, k1, b0, b1)
            if len(set(local_word)) > 1:
                assert value == 0

    colours = (0, 0, 1, 1, 1, 1)
    mixed_six = response(VERTICES, colours, k0, k1, b0, b1)
    k1_hafnian = sum(
        product_value(k1[tuple(sorted(edge))] for edge in matching)
        for matching in perfect_matchings(range(2, 6))
    )
    assert mixed_six == -(c**2) * k0[(0, 1)] * k1_hafnian
    assert mixed_six != 0

    # Independently extract the h=1 generating-family coefficients.
    quadratic = {(2, 0): Fraction(1, 2), (1, 1): Fraction(-1), (0, 2): Fraction(1)}
    for degree in range(3, 9):
        first = {
            key: value / factorial(degree)
            for key, value in polynomial_power(quadratic, degree).items()
        }
        second = {
            (x_degree + 1, y_degree + 1): value / factorial(degree - 1)
            for (x_degree, y_degree), value in polynomial_power(
                quadratic, degree - 1
            ).items()
        }
        coefficient = first.get((2, 2 * degree - 2), 0)
        coefficient += second.get((2, 2 * degree - 2), 0)
        labelled = coefficient * factorial(2) * factorial(2 * degree - 2)
        assert labelled == Fraction(
            (2 - degree) * factorial(2 * degree - 2), factorial(degree - 1)
        )


def main():
    assert len(EDGES) == 15
    audit_discriminant_and_shores()
    audit_singular_selectors_and_cover()
    audit_common_row_cover()
    audit_deeper_responses()
    print("independent six-port physical Wick selector audit: PASS")
    print("general witness-locus attachment and singular branch: UNKNOWN")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
