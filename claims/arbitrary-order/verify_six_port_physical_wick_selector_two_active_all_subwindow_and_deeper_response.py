"""Primary exact replay for the six-port physical Wick selector theorem."""

from __future__ import annotations

from itertools import combinations, permutations, product
from math import factorial

import sympy as sp


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}

UNISOLVENT_POINTS = (
    (7, -7, 6, -4, -6, -1),
    (-5, -4, -5, -5, -3, -7),
    (-6, 3, -3, 2, -1, -6),
    (-6, 0, -7, -3, -1, -3),
    (-2, -2, 3, -2, -3, -4),
    (-2, 7, 7, -7, 4, -1),
    (7, 4, 7, 3, -5, -5),
    (1, 3, -2, 1, 0, -5),
    (6, -5, 0, -4, 5, -3),
    (-2, 6, -2, -3, -5, 5),
    (5, 1, -7, 0, 3, -2),
    (6, 4, 1, -7, -5, 4),
    (1, 5, 4, -1, 1, 1),
    (-4, -4, 6, -3, 2, 5),
    (-5, -4, 7, 2, -5, -5),
    (-1, 6, -2, -5, 4, -6),
    (0, -3, 1, 3, -4, 7),
    (-3, 4, 7, 6, 2, -2),
    (-2, 5, -7, 5, 6, -3),
    (-1, 0, 0, 0, 4, -6),
    (6, -6, -2, 5, 3, -4),
    (5, 0, 3, -7, -7, -2),
    (7, -2, 2, -5, 7, 1),
    (-5, -2, -4, -4, 2, 2),
    (-2, 3, 0, 5, 5, -3),
    (2, -3, 1, 5, 2, -7),
    (-7, -4, 4, -3, -6, 7),
    (1, 3, 3, 5, -2, -4),
    (5, -7, -7, 4, 1, 3),
    (6, 0, -2, 0, -6, 7),
    (1, 0, 6, 3, -7, -1),
    (-3, -4, 0, 1, 2, 7),
)


def complement(vertices):
    return tuple(sorted(set(VERTICES) - set(vertices)))


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
    rows = []
    for row_edge in EDGES:
        row = []
        for column_edge in EDGES:
            if set(row_edge).isdisjoint(column_edge):
                remaining = complement(row_edge + column_edge)
                row.append(pair_value[remaining])
            else:
                row.append(sp.S.Zero)
        rows.append(row)
    return sp.Matrix(rows)


def elementary(values, degree):
    return sum(
        (
            sp.prod(values[index] for index in choice)
            for choice in combinations(range(6), degree)
        ),
        sp.S.Zero,
    )


def bounded_partitions(total, maximum=5, slots=6, prefix=()):
    if total == 0:
        yield prefix
        return
    if slots == 0:
        return
    for value in range(min(maximum, total), 0, -1):
        yield from bounded_partitions(
            total - value, value, slots - 1, prefix + (value,)
        )


def monomial_symmetric_value(partition, point, modulus):
    padded = partition + (0,) * (6 - len(partition))
    total = 0
    for exponents in set(permutations(padded)):
        term = 1
        for value, exponent in zip(point, exponents, strict=True):
            term = term * pow(value % modulus, exponent, modulus) % modulus
        total = (total + term) % modulus
    return total


def determinant_mod(matrix, prime):
    work = [[value % prime for value in row] for row in matrix]
    size = len(work)
    determinant = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            scale = work[row][column] * inverse % prime
            for entry in range(column, size):
                work[row][entry] -= scale * work[column][entry]
                work[row][entry] %= prime
    return determinant % prime


def check_compression_and_discriminant():
    t = sp.symbols("t0:6")
    pair_value = {edge: t[edge[0]] + t[edge[1]] for edge in EDGES}
    d_matrix = wick_matrix(pair_value)

    incidence = sp.zeros(6, 15)
    for column, edge in enumerate(EDGES):
        for vertex in edge:
            incidence[vertex, column] = 1
    edge_one = sp.ones(15, 1)
    j_matrix = (
        sp.eye(15)
        - sp.Rational(1, 2) * incidence.T * incidence
        + sp.Rational(1, 3) * edge_one * edge_one.T
    )
    total = sum(t)
    delta = sp.diag(*(total - 2 * (t[i] + t[j]) for i, j in EDGES))
    p_matrix = sp.zeros(15, 6)
    for row, (i, j) in enumerate(EDGES):
        p_matrix[row, i] = t[j]
        p_matrix[row, j] = t[i]
    l_matrix = delta + p_matrix * incidence

    assert j_matrix * d_matrix == l_matrix
    assert j_matrix * j_matrix == sp.eye(15)
    assert j_matrix.det() == -1

    e = {degree: elementary(t, degree) for degree in range(1, 7)}
    expected = -9216 * (
        12 * e[5] ** 3
        - 4 * e[1] * e[4] * e[5] ** 2
        + e[1] ** 2 * e[3] * e[5] ** 2
        - 4 * e[1] ** 2 * e[2] * e[5] * e[6]
        + 12 * e[1] ** 3 * e[6] ** 2
    )

    # Both determinant polynomials are symmetric, homogeneous of degree 15,
    # and have individual degree at most five (proved in the theorem).  The
    # resulting monomial-symmetric space has the following 32-partition basis.
    partitions = tuple(bounded_partitions(15))
    assert len(partitions) == 32
    prime = 1_000_003
    evaluation_matrix = [
        [monomial_symmetric_value(partition, point, prime) for partition in partitions]
        for point in UNISOLVENT_POINTS
    ]
    assert determinant_mod(evaluation_matrix, prime) == 188237
    for values in UNISOLVENT_POINTS:
        substitution = dict(zip(t, values, strict=True))
        direct = wick_matrix(
            {edge: values[edge[0]] + values[edge[1]] for edge in EDGES}
        ).det()
        assert direct == expected.subs(substitution)

    general_controls = (
        ((1, 1, 1, 1, 1, 1), (1, 2, 3, 4, 5, 6)),
        ((2, 3, 5, 7, 11, 13), (-1, 0, 2, -3, 5, 8)),
        ((0, 1, 2, 3, 4, 5), (1, -2, 3, -4, 5, -6)),
        ((1, 0, 2, 0, 3, 4), (0, 5, -1, 7, 2, -3)),
        ((-2, -1, 1, 2, 3, 5), (7, 0, -4, 6, -8, 9)),
        ((0, 0, 1, 1, 2, 3), (1, 2, 0, -1, 4, -5)),
    )
    for a_values, b_values in general_controls:
        pair_values = {
            (i, j): a_values[i] * b_values[j] + b_values[i] * a_values[j]
            for i, j in EDGES
        }
        capital_a = sp.prod(a_values)
        s = {
            degree: sum(
                (
                    sp.prod(
                        b_values[index] if index in choice else a_values[index]
                        for index in range(6)
                    )
                    for choice in combinations(range(6), degree)
                ),
                sp.S.Zero,
            )
            for degree in range(1, 7)
        }
        homogeneous = -9216 * (
            12 * capital_a**2 * s[5] ** 3
            - 4 * capital_a * s[1] * s[4] * s[5] ** 2
            + s[1] ** 2 * s[3] * s[5] ** 2
            - 4 * s[1] ** 2 * s[2] * s[5] * s[6]
            + 12 * s[1] ** 3 * s[6] ** 2
        )
        assert wick_matrix(pair_values).det() == homogeneous
    print("32-point unisolvent physical discriminant certificate: PASS")


def shore_matrix(colours, alpha=sp.Integer(2), beta=sp.Integer(3)):
    pair_value = {}
    for i, j in EDGES:
        if colours[i] != colours[j]:
            pair_value[(i, j)] = sp.S.Zero
        elif colours[i] == 0:
            pair_value[(i, j)] = alpha
        else:
            pair_value[(i, j)] = beta
    return wick_matrix(pair_value)


def check_shore_table_and_singular_structure():
    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    six = shore_matrix((0, 0, 0, 0, 0, 0), alpha, beta)
    four_two = shore_matrix((0, 0, 0, 0, 1, 1), alpha, beta)
    assert sp.factor(six.det()) == -1458 * alpha**15
    assert sp.factor(four_two.det()) == 54 * alpha**10 * beta**5

    ranks = []
    for count in (6, 5, 4, 3):
        matrix = shore_matrix((0,) * count + (1,) * (6 - count))
        ranks.append(matrix.rank())
    assert ranks == [15, 10, 15, 10]

    # In a 5+1 word, recover every singleton pair by the ten triple rows.
    colours = (0, 0, 0, 0, 0, 1)
    matrix = shore_matrix(colours, alpha=sp.Integer(7), beta=sp.Integer(11))
    singleton = 5
    majority = range(5)
    for vertex in majority:
        selector = sp.zeros(1, 15)
        for triple in combinations(majority, 3):
            four_set = tuple(sorted((singleton,) + triple))
            row_edge = complement(four_set)
            sign = 1 if vertex in triple else -1
            selector[0, EDGE_INDEX[row_edge]] += sp.Rational(sign, 6 * 7)
        selected = selector * matrix
        expected = sp.zeros(1, 15)
        expected[0, EDGE_INDEX[tuple(sorted((vertex, singleton)))]] = 1
        assert selected == expected

    # In a 3+3 word, check the four rectangle cycles and weighted internal line.
    colours = (0, 0, 0, 1, 1, 1)
    alpha_value, beta_value = sp.Integer(2), sp.Integer(3)
    matrix = shore_matrix(colours, alpha_value, beta_value)
    kernel_vectors = []
    for left in (1, 2):
        for right in (4, 5):
            vector = sp.zeros(15, 1)
            for edge, value in (
                ((0, 3), 1),
                ((0, right), -1),
                ((left, 3), -1),
                ((left, right), 1),
            ):
                vector[EDGE_INDEX[tuple(sorted(edge))], 0] = value
            kernel_vectors.append(vector)
    internal = sp.zeros(15, 1)
    for edge in combinations(range(3), 2):
        internal[EDGE_INDEX[edge], 0] = alpha_value
    for edge in combinations(range(3, 6), 2):
        internal[EDGE_INDEX[edge], 0] = -beta_value
    kernel_vectors.append(internal)
    kernel_basis = sp.Matrix.hstack(*kernel_vectors)
    assert kernel_basis.rank() == 5
    assert matrix * kernel_basis == sp.zeros(15, 5)
    assert matrix.rank() == 10
    assert all(
        any(vector[index, 0] != 0 for vector in kernel_vectors) for index in range(15)
    )


def row_selects(matrix, column):
    unit = sp.zeros(15, 1)
    unit[column, 0] = 1
    return matrix.T.rank() == matrix.T.row_join(unit).rank()


def check_tensor_polarization_cover():
    for left_colour, right_colour in product(range(3), repeat=2):
        if left_colour == right_colour and left_colour in (0, 1):
            other = 1 - left_colour
            word = (left_colour, right_colour, left_colour, left_colour, other, other)
            matrix = shore_matrix(
                tuple(0 if colour == left_colour else 1 for colour in word)
            )
            assert matrix.det() != 0
        elif (
            2 not in (left_colour, right_colour)
            or (left_colour, right_colour).count(2) == 1
        ):
            active = left_colour if left_colour in (0, 1) else right_colour
            word = (left_colour, right_colour) + (active,) * 4
            normalized = tuple(0 if colour == active else 1 for colour in word)
            matrix = shore_matrix(normalized)
            assert row_selects(matrix, EDGE_INDEX[(0, 1)])
        else:
            word = (2, 2, 0, 0, 1, 1)
            pair_value = {
                edge: sp.Integer(5)
                if word[edge[0]] == word[edge[1]] == 0
                else sp.Integer(7)
                if word[edge[0]] == word[edge[1]] == 1
                else sp.S.Zero
                for edge in EDGES
            }
            matrix = wick_matrix(pair_value)
            row_edge = (4, 5)  # complement of inactive pair plus the 0,0 pair
            row = matrix[EDGE_INDEX[row_edge], :]
            assert row[EDGE_INDEX[(0, 1)]] == 5
            assert sum(int(value != 0) for value in row) == 1


def hafnian_coefficient(vertices, colours, b0, b1):
    total = sp.S.Zero
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.S.One
        for edge in matching:
            edge = tuple(sorted(edge))
            left, right = edge
            if colours[left] != colours[right]:
                term = sp.S.Zero
                break
            term *= b0[edge] if colours[left] == 0 else b1[edge]
        total += term
    return sp.expand(total)


def response_coefficient(vertices, colours, k0, k1, b0, b1):
    total = sp.S.Zero
    vertices = tuple(vertices)
    for pair in combinations(vertices, 2):
        if colours[pair[0]] != colours[pair[1]]:
            continue
        edge = tuple(sorted(pair))
        k_value = k0[edge] if colours[pair[0]] == 0 else k1[edge]
        total += k_value * hafnian_coefficient(
            tuple(vertex for vertex in vertices if vertex not in pair),
            colours,
            b0,
            b1,
        )
    return sp.expand(total)


def check_deeper_detector_and_control():
    k0_symbols = sp.symbols("k0_0:15")
    k1_symbols = sp.symbols("k1_0:15")
    k0 = {edge: k0_symbols[index] for index, edge in enumerate(EDGES)}
    k1 = {edge: k1_symbols[index] for index, edge in enumerate(EDGES)}
    c = sp.symbols("c")
    b0 = {edge: c * value for edge, value in k0.items()}
    b1 = {edge: -c * value for edge, value in k1.items()}

    mixed_four_colours = (0, 0, 1, 1, 0, 0)
    assert response_coefficient(range(4), mixed_four_colours, k0, k1, b0, b1) == 0

    pure_one_colours = (1,) * 6
    pure_four = response_coefficient(range(4), pure_one_colours, k0, k1, b0, b1)
    c_k1 = sum(
        (
            sp.prod(k1[tuple(sorted(edge))] for edge in matching)
            for matching in perfect_matchings(range(4))
        ),
        sp.S.Zero,
    )
    assert sp.expand(pure_four + 2 * c * c_k1) == 0

    six_colours = (0, 0, 1, 1, 1, 1)
    mixed_six = response_coefficient(VERTICES, six_colours, k0, k1, b0, b1)
    c_k1_rest = sum(
        (
            sp.prod(k1[tuple(sorted(edge))] for edge in matching)
            for matching in perfect_matchings(range(2, 6))
        ),
        sp.S.Zero,
    )
    expected = -(c**2) * k0[(0, 1)] * c_k1_rest
    assert sp.expand(mixed_six - expected) == 0

    # The ratio graph is the connected bipartite double cover of KG(6,2).
    adjacency = {side_edge: set() for side_edge in product((0, 1), EDGES)}
    for edge, other in product(EDGES, repeat=2):
        if set(edge).isdisjoint(other):
            adjacency[(0, edge)].add((1, other))
            adjacency[(1, other)].add((0, edge))
    reached = {(0, EDGES[0])}
    frontier = list(reached)
    while frontier:
        current = frontier.pop()
        for neighbour in adjacency[current] - reached:
            reached.add(neighbour)
            frontier.append(neighbour)
    assert len(reached) == 30

    x, y = sp.symbols("x y")
    quadratic = x**2 / 2 - x * y + y**2
    for degree in range(3, 8):
        homogeneous = quadratic**degree / factorial(degree)
        homogeneous += x * y * quadratic ** (degree - 1) / factorial(degree - 1)
        coefficient = sp.expand(homogeneous).coeff(x, 2).coeff(y, 2 * degree - 2)
        labelled = sp.factor(coefficient * factorial(2) * factorial(2 * degree - 2))
        expected_labelled = (
            (2 - degree) * factorial(2 * degree - 2) // factorial(degree - 1)
        )
        assert labelled == expected_labelled


def main():
    assert len(EDGES) == 15
    check_compression_and_discriminant()
    check_shore_table_and_singular_structure()
    check_tensor_polarization_cover()
    check_deeper_detector_and_control()
    print("six-port physical Wick selector verification: PASS")
    print("constant z2/z4/z6 target attachment: ASSUMED, not proved")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
