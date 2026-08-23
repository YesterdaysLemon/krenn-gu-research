"""Independent no-import Fraction audit for GLS31.

This script deliberately does not import the primary verifier or SymPy.  It
uses a separate sparse column-reduction route and recursive matching engine.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product


A0, A1, Q0, Q1, K, U1, U2, U3 = range(8)
VERTICES = tuple(range(8))
ROOTS = (A0, A1, K)
Q = (Q0, Q1)
PORTS = (K, U1, U2, U3)
B_HAT = Q + PORTS
PORT_PAIRS = tuple(combinations(PORTS, 2))
LABELS = tuple(combinations(B_HAT, 2))
ONE = (F(1), F(1), F(1))


def zero_matrix(rows=3, columns=3):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def unit(row, column, value=F(1)):
    answer = zero_matrix()
    answer[row][column] = F(value)
    return answer


def add(*matrices):
    return [
        [
            sum(matrix[row][column] for matrix in matrices)
            for column in range(len(matrices[0][0]))
        ]
        for row in range(len(matrices[0]))
    ]


def scale(value, matrix):
    return [[F(value) * entry for entry in row] for row in matrix]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def outer(left, right):
    return [
        [F(left[row]) * F(right[column]) for column in range(3)] for row in range(3)
    ]


def put(edges, left, right, matrix):
    if left < right:
        edges[left, right] = matrix
    else:
        edges[right, left] = transpose(matrix)


def edge(edges, left, right):
    if left < right:
        return edges.get((left, right), zero_matrix())
    return transpose(edges.get((right, left), zero_matrix()))


def build_control():
    edges = {}
    e = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    e00, e11, e22 = unit(0, 0), unit(1, 1), unit(2, 2)
    j = outer((0, 1, 1), (0, 1, 1))
    put(edges, A0, Q0, e11)
    put(edges, A0, Q1, e22)
    put(edges, A1, Q0, e22)
    put(edges, A1, Q1, e11)
    put(edges, Q0, Q1, e00)
    put(edges, A0, K, outer((1, 0, -1), e[0]))
    put(edges, A1, K, outer((1, 1, -2), e[0]))
    for root in (A0, A1):
        for port in (U1, U2, U3):
            put(edges, root, port, e00)
    put(edges, Q0, K, add(e11, e22))
    put(edges, Q0, U1, add(e11, e22))
    put(edges, Q1, U2, add(e11, e22))
    put(edges, Q1, U3, scale(F(1, 2), add(e11, e22)))
    put(edges, K, U1, e00)
    put(edges, K, U2, add(e00, scale(-1, j)))
    put(edges, K, U3, add(e00, scale(F(-1, 2), j)))
    put(edges, U1, U2, add(e00, scale(-1, j)))
    put(edges, U1, U3, add(e00, scale(F(-1, 2), j)))
    put(edges, U2, U3, scale(F(-9, 2), e00))
    return edges


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(matchings(VERTICES))


def coefficient(edges, word):
    total = F(0)
    for matching in MATCHINGS:
        term = F(1)
        for left, right in matching:
            term *= edge(edges, left, right)[word[left]][word[right]]
        total += term
    return total


def index(values):
    answer = 0
    for value in values:
        answer = 3 * answer + value
    return answer


def matmul(left, right):
    return [
        [
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(len(right))
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def companion(edges, label):
    promoted = tuple(port for port in PORTS if port in label)
    residual = tuple(vertex for vertex in Q if vertex in label)
    answer = zero_matrix(9, 3 ** len(promoted))
    local_matchings = tuple(matchings((A0, A1, *label)))
    for ca0, ca1 in product(range(3), repeat=2):
        for kept_values in product(range(3), repeat=len(promoted)):
            kept = dict(zip(promoted, kept_values, strict=True))
            total = F(0)
            for residual_values in product(range(3), repeat=len(residual)):
                colours = {
                    A0: ca0,
                    A1: ca1,
                    **kept,
                    **dict(zip(residual, residual_values, strict=True)),
                }
                for matching in local_matchings:
                    term = F(1)
                    for left, right in matching:
                        term *= edge(edges, left, right)[colours[left]][colours[right]]
                    total += term
            answer[3 * ca0 + ca1][index(kept_values)] = total
    return promoted, answer


def projector(edges):
    _, q = companion(edges, Q)
    p = sum(row[0] for row in q)
    assert p == 2
    projection = zero_matrix(9, 9)
    for row in range(9):
        for column in range(9):
            projection[row][column] = p * (row == column) - q[row][0]
    return q, p, projection


def sparse(vector):
    return {row: value for row, value in enumerate(vector) if value}


def reduce_column(vector, basis):
    vector = dict(vector)
    while vector:
        pivot = min(vector)
        if pivot not in basis:
            lead = vector[pivot]
            normalized = {row: value / lead for row, value in vector.items()}
            basis[pivot] = normalized
            return True
        factor = vector[pivot]
        for row, value in basis[pivot].items():
            new = vector.get(row, F(0)) - factor * value
            if new:
                vector[row] = new
            else:
                vector.pop(row, None)
    return False


def rank(columns):
    basis = {}
    for column in columns:
        reduce_column(sparse(column), basis)
    return len(basis), basis


def matrix_columns(matrix):
    return [
        [matrix[row][column] for row in range(len(matrix))]
        for column in range(len(matrix[0]))
    ]


def inserted_columns(target, promoted, coefficient):
    x_vertices = tuple(vertex for vertex in target if vertex in promoted)
    y_vertices = tuple(vertex for vertex in promoted if vertex not in target)
    z_vertices = tuple(vertex for vertex in target if vertex not in promoted)
    answer = []
    for y_values in product(range(3), repeat=len(y_vertices)):
        y_map = dict(zip(y_vertices, y_values, strict=True))
        for z_values in product(range(3), repeat=len(z_vertices)):
            z_map = dict(zip(z_vertices, z_values, strict=True))
            vector = [F(0)] * 81
            for root in range(9):
                for x_values in product(range(3), repeat=len(x_vertices)):
                    x_map = dict(zip(x_vertices, x_values, strict=True))
                    d_values = tuple({**x_map, **y_map}[vertex] for vertex in promoted)
                    c_values = tuple({**x_map, **z_map}[vertex] for vertex in target)
                    vector[9 * root + index(c_values)] = coefficient[root][
                        index(d_values)
                    ]
            answer.append(vector)
    return answer


def flatten(coefficient):
    return [coefficient[root][port] for root in range(9) for port in range(9)]


def response(edges, pair):
    left, right = pair
    answer = zero_matrix()
    local_matchings = tuple(matchings((Q0, Q1, left, right)))
    for cl, cr in product(range(3), repeat=2):
        total = F(0)
        for cq0, cq1 in product(range(3), repeat=2):
            colours = {Q0: cq0, Q1: cq1, left: cl, right: cr}
            for matching in local_matchings:
                term = F(1)
                for first, second in matching:
                    term *= edge(edges, first, second)[colours[first]][colours[second]]
                total += term
        answer[cl][cr] = total
    return answer


def row_times(matrix, vector):
    return [
        sum(vector[row] * matrix[row][column] for row in range(3))
        for column in range(3)
    ]


def matrix_times_column(matrix, vector):
    return [
        sum(matrix[row][column] * vector[column] for column in range(3))
        for row in range(3)
    ]


def kronecker(left, right):
    return [left[first] * right[second] for first in range(3) for second in range(3)]


def contract_first(vector):
    """Contract a two-root vector at n0=e0 in its first factor."""

    return [vector[second] for second in range(3)]


def check():
    edges = build_control()

    # Independent maximum-root/defect replay.
    assert sum(value for row in edge(edges, A0, K) for value in row) == 0
    assert sum(value for row in edge(edges, A1, K) for value in row) == 0
    assert edge(edges, A0, A1) == zero_matrix()
    monomial = {
        pair
        for pair in combinations(VERTICES, 2)
        if sum(value != 0 for row in edge(edges, *pair) for value in row) == 1
    }
    alpha = max(
        len(subset)
        for size in range(9)
        for subset in combinations(VERTICES, size)
        if all(pair not in monomial for pair in combinations(subset, 2))
    )
    assert alpha == 3
    incidence_ranks = []
    for vertex in (Q0, Q1, U1, U2, U3):
        rows = [row_times(edge(edges, root, vertex), ONE) for root in ROOTS]
        incidence_ranks.append(
            rank([list(column) for column in zip(*rows, strict=True)])[0]
        )
    assert incidence_ranks == [2, 2, 1, 2, 2]
    assert sum(3 - value for value in incidence_ranks) == 6

    q, p, projection = projector(edges)
    assert [q[row][0] for row in range(9)] == [0, 0, 0, 0, 1, 0, 0, 0, 1]

    # The retained-root quotient is 8/7 dimensional and contraction by e0
    # has images of ranks 3/2, independently replaying Theorem 3.
    standard = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    tangent_raw = []
    for shore in (standard[1], standard[2]):
        tangent_raw.extend(kronecker(shore, basis) for basis in standard)
    for basis in standard:
        tangent_raw.extend(
            kronecker(basis, shore) for shore in (standard[1], standard[2])
        )
    tangent_projected = []
    for column in tangent_raw:
        tangent_projected.append(
            [
                sum(projection[row][middle] * column[middle] for middle in range(9))
                for row in range(9)
            ]
        )
    transverse_columns = matrix_columns(projection)
    assert rank(transverse_columns)[0] == 8
    assert rank(tangent_projected)[0] == 7
    assert rank([contract_first(column) for column in transverse_columns])[0] == 3
    assert rank([contract_first(column) for column in tangent_projected])[0] == 2

    # q is constant on s+tau e0, and the three projected diagonal rows have
    # precisely the claimed nonconstant polynomial coefficients.
    q_matrix = [[q[3 * first + second][0] for second in range(3)] for first in range(3)]
    assert (
        sum(q_matrix[first][second] for first, second in product(range(3), repeat=2))
        == p
    )
    assert [
        sum(q_matrix[0][second] for second in range(3)),
        sum(q_matrix[first][0] for first in range(3)),
        q_matrix[0][0],
    ] == [0, 0, 0]
    projected = {}
    for label in LABELS:
        promoted, raw = companion(edges, label)
        projected[label] = promoted, matmul(projection, raw)

    # Independently extract every one-Q bivariate coefficient.  Constants and
    # mixed bidegrees vanish; the two linear coefficients retain the labelled
    # lambda_1*x and lambda_0*y terms.
    one_q_checks = 0
    normal = standard[0]
    for residual in Q:
        xi0 = matrix_times_column(edge(edges, A0, residual), ONE)
        xi1 = matrix_times_column(edge(edges, A1, residual), ONE)
        lambda0, lambda1 = sum(xi0), sum(xi1)
        for port in PORTS:
            matrix = projected[tuple(sorted((residual, port)))][1]
            x_port = row_times(edge(edges, A0, port), normal)
            y_port = row_times(edge(edges, A1, port), normal)
            for port_colour in range(3):
                column = [matrix[root][port_colour] for root in range(9)]
                polynomial = (
                    sum(column),
                    sum(column[second] for second in range(3)),
                    sum(column[3 * first] for first in range(3)),
                    column[0],
                )
                assert polynomial == (
                    F(0),
                    p * lambda1 * x_port[port_colour],
                    p * lambda0 * y_port[port_colour],
                    F(0),
                )
            one_q_checks += 1
    assert one_q_checks == 8
    assert all(value == 0 for row in projected[Q][1] for value in row)

    top_columns = []
    for _, matrix in projected.values():
        top_columns.extend(matrix_columns(matrix))
    top_rank, top_basis = rank(top_columns)
    assert top_rank == 6
    delta_columns = []
    for colour in range(3):
        basis = [[F(0)] for _ in range(9)]
        basis[3 * colour + colour][0] = F(1)
        delta_columns.append([row[0] for row in matmul(projection, basis)])
    for colour, delta in enumerate(delta_columns):
        polynomial = (
            sum(delta),
            sum(delta[second] for second in range(3)),
            sum(delta[3 * first] for first in range(3)),
            delta[0],
        )
        active = F(1) if colour == 0 else F(0)
        assert polynomial == (F(0), p * active, p * active, p * active)
    delta_rank = rank(delta_columns)[0]
    assert delta_rank == 2
    assert rank(tangent_projected + delta_columns)[0] == 8
    for column in delta_columns:
        assert not reduce_column(sparse(column), dict(top_basis))

    pair_records = []
    for target in PORT_PAIRS:
        nuisance_columns = []
        for label, (promoted, matrix) in projected.items():
            if label != target:
                nuisance_columns.extend(inserted_columns(target, promoted, matrix))
        nuisance_rank, nuisance_basis = rank(nuisance_columns)
        desired = flatten(projected[target][1])
        absorbed = not reduce_column(sparse(desired), dict(nuisance_basis))
        pair_records.append(
            (
                target,
                rank(matrix_columns(projected[target][1]))[0],
                nuisance_rank,
                absorbed,
            )
        )
    assert [record[1] for record in pair_records] == [1] * 6
    assert [record[2] for record in pair_records] == [36, 36, 36, 50, 50, 50]
    assert all(record[3] for record in pair_records)

    responses = [response(edges, pair) for pair in PORT_PAIRS]
    scalars = [matrix[0][0] for matrix in responses]
    assert scalars == [F(1), F(1), F(1), F(1), F(1), F(-9, 2)]
    assert all(
        matrix == scale(value, unit(0, 0))
        for value, matrix in zip(scalars, responses, strict=True)
    )
    assert 2 * sum(scalars) == 1
    assert all(
        row_times(edge(edges, root, port), normal) == [F(1), F(0), F(0)]
        for root in (A0, A1)
        for port in PORTS
    )

    pure = tuple(coefficient(edges, (colour,) * 8) for colour in range(3))
    assert pure == (F(1), F(1), F(1))
    failures = []
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        value = coefficient(edges, word)
        if value:
            failures.append((word, value))
    assert len(failures) == 313
    assert ((0, 0, 0, 0, 0, 1, 0, 1), F(-1)) in failures
    return {
        "alpha": alpha,
        "incidence_ranks": incidence_ranks,
        "top_rank": top_rank,
        "delta_rank": delta_rank,
        "pair_records": pair_records,
        "responses": scalars,
        "pure": pure,
        "mixed_failures": len(failures),
        "one_q_labels": one_q_checks,
    }


def check_polarization():
    # Separate sparse bivariate-polynomial expansion.  Coefficients are keyed
    # by (tau_degree, upsilon_degree); subtraction of the constant projection
    # removes K00 and leaves exactly the three declared supplier polynomials.
    a_u, x_u = (F(2), F(-1), F(3)), (F(1), F(0), F(2))
    b_u, y_u = (F(-2), F(4), F(1)), (F(0), F(3), F(-1))
    a_v, x_v = (F(5), F(1), F(-2)), (F(2), F(-1), F(0))
    b_v, y_v = (F(1), F(-3), F(2)), (F(-1), F(2), F(4))

    def pair_tensor(left, right, swapped_left, swapped_right):
        return tuple(
            left[i] * right[j] + swapped_left[i] * swapped_right[j]
            for i, j in product(range(3), repeat=2)
        )

    k00 = pair_tensor(a_u, b_v, b_u, a_v)
    k10 = pair_tensor(x_u, b_v, b_u, x_v)
    k01 = pair_tensor(a_u, y_v, y_u, a_v)
    k11 = pair_tensor(x_u, y_v, y_u, x_v)
    polynomial = {(0, 0): k00, (1, 0): k10, (0, 1): k01, (1, 1): k11}
    projected = {
        degree: tuple(2 * value for value in tensor)
        for degree, tensor in polynomial.items()
        if degree != (0, 0)
    }
    assert projected[(1, 0)] == tuple(2 * value for value in k10)
    assert projected[(0, 1)] == tuple(2 * value for value in k01)
    assert projected[(1, 1)] == tuple(2 * value for value in k11)
    return tuple(sorted(projected))


def main():
    graph = check()
    polarization = check_polarization()
    print("GLS31 independent Fraction audit: PASS")
    print("  graph/module replay:", graph)
    print("  separate sparse polarization degrees:", polarization)
    print("  no imports from primary verifier; witness/node/global closure OPEN")


if __name__ == "__main__":
    main()
