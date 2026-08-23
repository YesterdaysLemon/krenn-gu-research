"""Independent no-import audit for the GLS34 finite algebra.

This program deliberately uses only the Python standard library.  It rebuilds
the displayed tangent-root certificate, its Fitting ranks, the six universal
blind columns, representative Segre-silence cases, and the exact rational
two-active physical channel control from the stated matrices.

The finite calculations audit the certificate and sharpness control.  The
universal tensor-annihilator and Segre-line assertions still rest on the
written mathematical proof; finite examples cannot prove those assertions.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations, product

PRIME = 1_000_033
COLOURS = range(3)
PORTS = tuple(range(4))
PAIRS = tuple(combinations(PORTS, 2))


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in right_t]
        for row in left
    ]


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def pivot_columns_mod(matrix: list[list[int]], prime: int) -> list[int]:
    rows = [[value % prime for value in row] for row in matrix]
    if not rows:
        return []
    pivot_row = 0
    pivots: list[int] = []
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [(value * inverse) % prime for value in rows[pivot_row]]
        for row in range(pivot_row + 1, len(rows)):
            factor = rows[row][column]
            if factor:
                rows[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(rows[row], rows[pivot_row], strict=True)
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivots


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    rows = [[value % prime for value in row] for row in matrix]
    size = len(rows)
    assert all(len(row) == size for row in rows)
    determinant = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if rows[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant
        pivot_value = rows[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            factor = rows[row][column] * inverse % prime
            if factor:
                rows[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(rows[row], rows[column], strict=True)
                ]
    return determinant % prime


def modular_minor_certificate(
    matrix: list[list[int]], expected_rank: int
) -> tuple[list[int], list[int], int]:
    columns = pivot_columns_mod(matrix, PRIME)
    selected = [[row[column] for column in columns] for row in matrix]
    rows = pivot_columns_mod(transpose(selected), PRIME)
    assert len(columns) == len(rows) == expected_rank
    minor = [[matrix[row][column] for column in columns] for row in rows]
    determinant = determinant_mod(minor, PRIME)
    assert determinant
    return rows, columns, determinant


def cross(left: list[int], right: list[int]) -> list[int]:
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def column(matrix: list[list[int]], index: int) -> list[int]:
    return [row[index] for row in matrix]


def exponent(*indices: int) -> tuple[int, int, int]:
    output = [0, 0, 0]
    for index in indices:
        output[index] += 1
    return tuple(output)


def normal_polynomials(
    first: list[list[int]], second: list[list[int]]
) -> list[dict[tuple[int, int], int]]:
    """Coefficients of (first*z0) cross (second*z1), by component."""
    output: list[dict[tuple[int, int], int]] = [{}, {}, {}]
    for i, j in product(COLOURS, repeat=2):
        value = cross(column(first, i), column(second, j))
        for component in COLOURS:
            if value[component]:
                output[component][i, j] = value[component]
    return output


def domain_index(a: int, b: int, c: int, d: int) -> int:
    return ((a * 3 + b) * 3 + c) * 3 + d


def observation_matrix(
    normal0: list[dict[tuple[int, int], int]],
    normal1: list[dict[tuple[int, int], int]],
) -> list[list[int]]:
    """Build 00/10/01/11 coefficient rows in a fixed lexicographic order."""
    exp1 = sorted({exponent(i) for i in COLOURS})
    exp2 = sorted({exponent(i, j) for i, j in product(COLOURS, repeat=2)})
    exp3 = sorted({exponent(i, j, k) for i, j, k in product(COLOURS, repeat=3)})
    keys = (
        [("00", left, right) for left in exp1 for right in exp1]
        + [("10", left, right) for left in exp2 for right in exp2]
        + [("01", left, right) for left in exp2 for right in exp2]
        + [("11", left, right) for left in exp3 for right in exp3]
    )
    row_index = {key: index for index, key in enumerate(keys)}
    matrix = [[0] * 81 for _ in keys]
    for a, b, c, d in product(COLOURS, repeat=4):
        source = domain_index(a, b, c, d)
        if a == b == 0:
            matrix[row_index["00", exponent(c), exponent(d)]][source] += 1
        if b == 0:
            for (i, j), value in normal0[a].items():
                matrix[row_index["10", exponent(i, c), exponent(j, d)]][source] += value
        if a == 0:
            for (i, j), value in normal1[b].items():
                matrix[row_index["01", exponent(i, c), exponent(j, d)]][source] += value
        for (i, j), value0 in normal0[a].items():
            for (k, ell), value1 in normal1[b].items():
                matrix[row_index["11", exponent(i, k, c), exponent(j, ell, d)]][
                    source
                ] += value0 * value1
    assert len(matrix) == 181
    return matrix


def kappa_matrix(normal: list[dict[tuple[int, int], int]]) -> list[list[int]]:
    exp2 = sorted({exponent(i, j) for i, j in product(COLOURS, repeat=2)})
    keys = [(left, right) for left in exp2 for right in exp2]
    row_index = {key: index for index, key in enumerate(keys)}
    matrix = [[0] * 18 for _ in keys]
    for block in range(2):
        for c, d in product(COLOURS, repeat=2):
            source = block * 9 + c * 3 + d
            for (i, j), value in normal[block + 1].items():
                matrix[row_index[exponent(i, c), exponent(j, d)]][source] += value
    return matrix


def mu_matrix(
    normal0: list[dict[tuple[int, int], int]],
    normal1: list[dict[tuple[int, int], int]],
) -> list[list[int]]:
    exp3 = sorted({exponent(i, j, k) for i, j, k in product(COLOURS, repeat=3)})
    keys = [(left, right) for left in exp3 for right in exp3]
    row_index = {key: index for index, key in enumerate(keys)}
    matrix = [[0] * 36 for _ in keys]
    for a, b, c, d in product(range(2), range(2), COLOURS, COLOURS):
        source = (a * 2 + b) * 9 + c * 3 + d
        for (i, j), value0 in normal0[a + 1].items():
            for (k, ell), value1 in normal1[b + 1].items():
                matrix[row_index[exponent(i, k, c), exponent(j, ell, d)]][source] += (
                    value0 * value1
                )
    return matrix


def polynomial_vector(
    polynomial: dict[tuple[int, int], int], sign: int = 1
) -> list[int]:
    return [sign * polynomial.get((c, d), 0) for c, d in product(COLOURS, repeat=2)]


def kappa_syzygy(normal: list[dict[tuple[int, int], int]]) -> list[int]:
    return polynomial_vector(normal[2]) + polynomial_vector(normal[1], -1)


def mu_syzygies(
    normal0: list[dict[tuple[int, int], int]],
    normal1: list[dict[tuple[int, int], int]],
) -> list[list[int]]:
    output: list[list[int]] = []
    for fixed_b in range(2):
        vector = [0] * 36
        for c, d in product(COLOURS, repeat=2):
            vector[(0 * 2 + fixed_b) * 9 + c * 3 + d] = normal0[2].get((c, d), 0)
            vector[(1 * 2 + fixed_b) * 9 + c * 3 + d] = -normal0[1].get((c, d), 0)
        output.append(vector)
    for fixed_a in range(2):
        vector = [0] * 36
        for c, d in product(COLOURS, repeat=2):
            vector[(fixed_a * 2 + 0) * 9 + c * 3 + d] = normal1[2].get((c, d), 0)
            vector[(fixed_a * 2 + 1) * 9 + c * 3 + d] = -normal1[1].get((c, d), 0)
        output.append(vector)
    return output


def blind_columns(
    left00: list[list[int]],
    left01: list[list[int]],
    left10: list[list[int]],
    left11: list[list[int]],
) -> list[list[int]]:
    """The three r0 tensor A1 and three A0 tensor r1 coefficient columns."""
    columns: list[list[int]] = []
    for free_b in COLOURS:
        vector = [0] * 81
        for a, c, d in product(COLOURS, repeat=3):
            vector[domain_index(a, free_b, c, d)] = (
                left01[0][d] * left00[a][c] - left00[0][c] * left01[a][d]
            )
        columns.append(vector)
    for free_a in COLOURS:
        vector = [0] * 81
        for b, c, d in product(COLOURS, repeat=3):
            vector[domain_index(free_a, b, c, d)] = (
                left11[0][d] * left10[b][c] - left10[0][c] * left11[b][d]
            )
        columns.append(vector)
    return transpose(columns)


def fitting_certificate_audit() -> dict[str, object]:
    left00 = [[1, 1, -1], [2, -1, 1], [-2, -1, 0]]
    left01 = [[-1, -1, 1], [2, 1, 2], [-1, 0, -1]]
    left10 = [[-2, 2, -2], [0, -2, -1], [-1, -2, 1]]
    left11 = [[2, 1, 0], [-1, 1, 1], [2, 1, -1]]
    normal0 = normal_polynomials(left00, left01)
    normal1 = normal_polynomials(left10, left11)

    kappa0 = kappa_matrix(normal0)
    kappa1 = kappa_matrix(normal1)
    mu = mu_matrix(normal0, normal1)
    observation = observation_matrix(normal0, normal1)
    blind = blind_columns(left00, left01, left10, left11)

    assert matvec(kappa0, kappa_syzygy(normal0)) == [0] * 36
    assert matvec(kappa1, kappa_syzygy(normal1)) == [0] * 36
    mu_kernel = mu_syzygies(normal0, normal1)
    assert all(matvec(mu, vector) == [0] * 100 for vector in mu_kernel)
    assert len(pivot_columns_mod(transpose(mu_kernel), PRIME)) == 4

    # These are polynomial identities over Z, not merely modular checks.
    observation_blind = matmul(observation, blind)
    assert observation_blind == [[0] * 6 for _ in range(181)]

    certificates = {
        "kappa0": modular_minor_certificate(kappa0, 17),
        "kappa1": modular_minor_certificate(kappa1, 17),
        "mu": modular_minor_certificate(mu, 32),
        "blind": modular_minor_certificate(blind, 6),
        "observation": modular_minor_certificate(observation, 75),
    }
    return {
        "prime": PRIME,
        "ranks": {
            name: len(rows) for name, (rows, _columns, _det) in certificates.items()
        },
        "minor_determinants_mod_prime": {
            name: determinant
            for name, (_rows, _columns, determinant) in certificates.items()
        },
        "exact_kappa_kernel_dimensions_at_least": (1, 1),
        "exact_mu_kernel_dimension_at_least": 4,
        "six_blind_columns_exactly_killed": True,
    }


def tensor_product(factors: list[list[Fraction]]) -> list[Fraction]:
    output = [Fraction(1)]
    for factor in factors:
        output = [left * right for left in output for right in factor]
    return output


def tensor_sum(
    coefficients: list[Fraction], tensors: list[list[Fraction]]
) -> list[Fraction]:
    return [
        sum(
            coefficient * tensor[index]
            for coefficient, tensor in zip(coefficients, tensors, strict=True)
        )
        for index in range(len(tensors[0]))
    ]


def segre_examples_audit() -> dict[str, bool]:
    support_one_killed = tensor_product([[Fraction(1)], [Fraction(0)], [Fraction(2)]])
    support_one_survives = tensor_product([[Fraction(1)], [Fraction(3)], [Fraction(2)]])
    assert support_one_killed == [0]
    assert support_one_survives != [0]

    bases = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(-1)],
        [Fraction(1), Fraction(1)],
        [Fraction(3), Fraction(2)],
    ]
    lambdas = [Fraction(2), Fraction(3), Fraction(5), Fraction(7)]
    first = tensor_product(bases)
    second = tensor_product(
        [
            [scalar * value for value in basis]
            for scalar, basis in zip(lambdas, bases, strict=True)
        ]
    )
    aligned_two = tensor_sum([Fraction(1), -Fraction(1, 210)], [first, second])
    assert not any(aligned_two)

    misaligned_first = tensor_product(
        [[Fraction(1), 0], [Fraction(1), 0], [Fraction(1)]]
    )
    misaligned_second = tensor_product(
        [[0, Fraction(1)], [Fraction(1), 0], [Fraction(1)]]
    )
    assert any(
        tensor_sum([Fraction(1), Fraction(1)], [misaligned_first, misaligned_second])
    )

    exceptional_factors = [
        [[Fraction(1), 0], [Fraction(1)], [Fraction(1)]],
        [[0, Fraction(1)], [Fraction(1)], [Fraction(1)]],
        [[Fraction(1), Fraction(1)], [Fraction(1)], [Fraction(1)]],
    ]
    exceptional_tensors = [tensor_product(factors) for factors in exceptional_factors]
    assert not any(
        tensor_sum([Fraction(1), Fraction(1), Fraction(-1)], exceptional_tensors)
    )

    two_exception_factors = [
        [[Fraction(1), 0], [Fraction(1), 0]],
        [[0, Fraction(1)], [0, Fraction(1)]],
        [
            [Fraction(1), Fraction(1)],
            [Fraction(1), Fraction(2)],
        ],
    ]
    two_exception_tensors = [
        tensor_product(factors) for factors in two_exception_factors
    ]
    assert any(
        tensor_sum([Fraction(1), Fraction(1), Fraction(-1)], two_exception_tensors)
    )
    return {
        "support_zero_automatic_silence": True,
        "support_one_kill_and_survival": True,
        "support_two_aligned_silence_and_misaligned_survival": True,
        "support_three_one_exception_silence": True,
        "support_three_two_exception_survival": True,
    }


Vector = list[Fraction]
Matrix = list[list[Fraction]]


def vector(*values: int | Fraction) -> Vector:
    return [Fraction(value) for value in values]


def outer(left: Vector, right: Vector) -> Matrix:
    return [[a * b for b in right] for a in left]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [a + b for a, b in zip(left_row, right_row, strict=True)]
        for left_row, right_row in zip(left, right, strict=True)
    ]


def matrix_scale(scalar: Fraction, matrix: Matrix) -> Matrix:
    return [[scalar * value for value in row] for row in matrix]


def matrix_transpose(matrix: Matrix) -> Matrix:
    return [list(column_values) for column_values in zip(*matrix, strict=True)]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def left_contract(weight: Vector, matrix: Matrix) -> Vector:
    return [
        dot(weight, list(column_values)) for column_values in zip(*matrix, strict=True)
    ]


def bilinear(left: Vector, matrix: Matrix, right: Vector) -> Fraction:
    return dot(left_contract(left, matrix), right)


def zero_matrix() -> Matrix:
    return [[Fraction(0) for _ in COLOURS] for _ in COLOURS]


def put_edge(
    edges: dict[tuple[int, int], Matrix], left: int, right: int, matrix: Matrix
) -> None:
    if left < right:
        edges[left, right] = matrix
    else:
        edges[right, left] = matrix_transpose(matrix)


def edge_block(edges: dict[tuple[int, int], Matrix], left: int, right: int) -> Matrix:
    if left < right:
        return edges.get((left, right), zero_matrix())
    return matrix_transpose(edges.get((right, left), zero_matrix()))


@cache
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[tuple[tuple[int, int], ...]] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


def matching_contraction(
    vertices: tuple[int, ...],
    fixed: dict[int, int],
    weights: dict[int, Vector],
    edges: dict[tuple[int, int], Matrix],
) -> Fraction:
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for left, right in matching:
            matrix = edge_block(edges, left, right)
            if left in fixed and right in fixed:
                factor = matrix[fixed[left]][fixed[right]]
            elif left in fixed:
                factor = dot(matrix[fixed[left]], weights[right])
            elif right in fixed:
                factor = dot(weights[left], [row[fixed[right]] for row in matrix])
            else:
                factor = bilinear(weights[left], matrix, weights[right])
            term *= factor
        total += term
    return total


def graph_coefficient(
    word: tuple[int, ...], edges: dict[tuple[int, int], Matrix]
) -> Fraction:
    return matching_contraction(
        tuple(range(len(word))),
        {vertex: colour for vertex, colour in enumerate(word)},
        {},
        edges,
    )


def complement(pair: tuple[int, int]) -> tuple[int, int]:
    return tuple(port for port in PORTS if port not in pair)  # type: ignore[return-value]


def build_physical_control() -> tuple[
    dict[tuple[int, int], Matrix],
    tuple[Vector, ...],
    tuple[Vector, ...],
    tuple[Vector, ...],
    tuple[Vector, ...],
    dict[tuple[int, int], Matrix],
    Vector,
    Vector,
]:
    e0, e1, e2 = vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1)
    n0, n1 = vector(1, 1, 0), vector(1, 2, 1)
    xi00, xi01 = e2, vector(1, -1, 1)
    xi10, xi11 = vector(0, 1, -2), vector(1, 1, -3)
    x = (e0, e0, e1, e1)
    y = x
    a = (e1, e2, e0, e2)
    b = (e2, e1, e2, e0)
    r0, t0 = e2, vector(Fraction(1, 2), Fraction(1, 2), -1)
    r1, t1 = vector(1, -1, 1), vector(0, 1, -1)

    responses = {
        (0, 1): outer(e1, e1),
        (2, 3): matrix_scale(Fraction(1, 2), outer(e0, e0)),
        (0, 2): outer(e0, e1),
        (0, 3): outer(e0, e1),
        (1, 2): outer(e0, e1),
        (1, 3): matrix_scale(Fraction(-3), outer(e0, e1)),
    }
    edges: dict[tuple[int, int], Matrix] = {}
    put_edge(edges, 0, 2, outer(xi00, e0))
    put_edge(edges, 0, 3, outer(xi01, e0))
    put_edge(edges, 1, 2, outer(xi10, e0))
    put_edge(edges, 1, 3, outer(xi11, e0))
    for port in PORTS:
        put_edge(
            edges,
            0,
            4 + port,
            matrix_add(outer(r0, a[port]), outer(t0, x[port])),
        )
        put_edge(
            edges,
            1,
            4 + port,
            matrix_add(outer(r1, b[port]), outer(t1, y[port])),
        )
    put_edge(edges, 2, 3, outer(e0, e0))
    for pair, response in responses.items():
        put_edge(edges, 4 + pair[0], 4 + pair[1], response)
    return edges, a, b, x, y, responses, n0, n1


def physical_control_audit() -> dict[str, object]:
    edges, a, b, x, y, responses, n0, n1 = build_physical_control()
    e0, e1, e2 = vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1)
    ones = vector(1, 1, 1)
    kernels00 = (e0, e0, e1, e1)
    kernels10 = (e1, e2, e0, e2)
    kernels01 = (e2, e1, e2, e0)

    for port in PORTS:
        assert left_contract(ones, edge_block(edges, 0, 4 + port)) == a[port]
        assert left_contract(ones, edge_block(edges, 1, 4 + port)) == b[port]
        assert left_contract(n0, edge_block(edges, 0, 4 + port)) == x[port]
        assert left_contract(n1, edge_block(edges, 1, 4 + port)) == y[port]
        assert dot(a[port], kernels00[port]) == 0
        assert dot(b[port], kernels00[port]) == 0
        assert dot(x[port], kernels10[port]) == 0
        assert dot(b[port], kernels10[port]) == 0
        assert dot(a[port], kernels01[port]) == 0
        assert dot(y[port], kernels01[port]) == 0

    for family in (kernels10, kernels01):
        for omitted in PORTS:
            value = vector(1, 1, 1)
            for port in PORTS:
                if port != omitted:
                    value = [
                        left * right
                        for left, right in zip(value, family[port], strict=True)
                    ]
            assert value == vector(0, 0, 0)

    all_port_product = vector(1, 1, 1)
    for kernel in kernels00:
        all_port_product = [
            left * right for left, right in zip(all_port_product, kernel, strict=True)
        ]
    assert all_port_product == vector(0, 0, 0)

    constant_deck_value = matching_contraction(
        tuple(range(4, 8)),
        {},
        {4 + port: kernels00[port] for port in PORTS},
        edges,
    )
    constant_deck_left = Fraction(-2) * constant_deck_value
    assert constant_deck_value == Fraction(-2)
    assert constant_deck_left == Fraction(4)

    normal_tensor: dict[tuple[int, int, int, int], Fraction] = {}
    for word in product(COLOURS, repeat=4):
        value = Fraction(0)
        for pair in PAIRS:
            other = complement(pair)
            supplier = matrix_add(
                outer(x[pair[0]], y[pair[1]]),
                outer(y[pair[0]], x[pair[1]]),
            )
            value += (
                supplier[word[pair[0]]][word[pair[1]]]
                * responses[other][word[other[0]]][word[other[1]]]
            )
        normal_tensor[word] = value
        expected = Fraction(
            1 if word == (0, 0, 0, 0) else 2 if word == (1, 1, 1, 1) else 0
        )
        assert value == expected

    for pair, response in responses.items():
        assert any(value for row in response for value in row)
        vertices = (2, 3, 4 + pair[0], 4 + pair[1])
        for left_colour, right_colour in product(COLOURS, repeat=2):
            observed = matching_contraction(
                vertices,
                {4 + pair[0]: left_colour, 4 + pair[1]: right_colour},
                {2: ones, 3: ones},
                edges,
            )
            assert observed == response[left_colour][right_colour]

    q = matrix_add(
        outer(vector(0, 0, 1), vector(1, 1, -3)),
        outer(vector(1, -1, 1), vector(0, 1, -2)),
    )
    assert bilinear(ones, q, ones) == -2

    profiles = {
        "00": (ones, ones, 15),
        "10": (n0, ones, 10),
        "01": (ones, n1, 11),
        "11": (n0, n1, 0),
    }
    failure_counts: dict[str, int] = {}
    failure_maps: dict[str, dict[tuple[int, ...], Fraction]] = {}
    for label, (left, right, expected_count) in profiles.items():
        failures: list[tuple[tuple[int, ...], Fraction]] = []
        weights = {0: left, 1: right, 2: ones, 3: ones}
        for word in product(COLOURS, repeat=4):
            observed = matching_contraction(
                tuple(range(8)),
                {4 + port: word[port] for port in PORTS},
                weights,
                edges,
            )
            expected = (
                left[word[0]] * right[word[0]] if len(set(word)) == 1 else Fraction(0)
            )
            if observed != expected:
                failures.append((word, observed - expected))
        assert len(failures) == expected_count
        if label != "11":
            assert failures[0] == ((0, 0, 0, 0), Fraction(-1))
        failure_counts[label] = len(failures)
        failure_maps[label] = dict(failures)

    singleton_defect_slices = 0
    for label, kernels in (("10", kernels10), ("01", kernels01)):
        for free_port in PORTS:
            complement_ports = tuple(port for port in PORTS if port != free_port)
            for free_colour in COLOURS:
                contracted_defect = Fraction(0)
                for complement_word in product(COLOURS, repeat=3):
                    word = [0, 0, 0, 0]
                    word[free_port] = free_colour
                    for port, colour in zip(
                        complement_ports, complement_word, strict=True
                    ):
                        word[port] = colour
                    factor = Fraction(1)
                    for port in complement_ports:
                        factor *= kernels[port][word[port]]
                    contracted_defect += (
                        failure_maps[label].get(tuple(word), Fraction(0)) * factor
                    )
                assert contracted_defect == 0
                singleton_defect_slices += 1
    assert singleton_defect_slices == 24

    pure_coefficients = tuple(
        graph_coefficient((colour,) * 8, edges) for colour in COLOURS
    )
    assert pure_coefficients == (Fraction(0), Fraction(0), Fraction(0))
    original_failures = 0
    for word in product(COLOURS, repeat=8):
        expected = Fraction(1 if len(set(word)) == 1 else 0)
        if graph_coefficient(word, edges) != expected:
            original_failures += 1
    assert original_failures == 147
    return {
        "p": -2,
        "gamma": (1, 2, 0),
        "six_nonzero_responses": True,
        "normal_tensor_identity": "diag(1,2,0)",
        "constant_diagonal_restriction": "zero",
        "constant_kernel_values": (constant_deck_left, Fraction(0)),
        "constant_kernel_defect": constant_deck_left,
        "fixed_failure_counts": failure_counts,
        "zero_singleton_defect_slices": singleton_defect_slices,
        "pure_coefficients": tuple(int(value) for value in pure_coefficients),
        "original_failure_count": original_failures,
    }


def main() -> None:
    assert is_prime(PRIME)
    fitting = fitting_certificate_audit()
    segre = segre_examples_audit()
    physical = physical_control_audit()
    print("GLS34 independent no-import audit: PASS")
    print("  tangent-root/Fitting certificate:", fitting)
    print("  representative Segre cases:", segre)
    print("  exact diagonal-silent physical control:", physical)
    print(
        "  scope: finite certificate/control algebra audited independently; "
        "universal theorems rely on the written proof; strategic/global closure OPEN"
    )


if __name__ == "__main__":
    main()
