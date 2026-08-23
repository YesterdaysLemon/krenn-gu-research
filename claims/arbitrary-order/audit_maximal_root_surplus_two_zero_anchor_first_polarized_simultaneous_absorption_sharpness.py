"""Independent Fraction audit of the first-polarized sharpness control.

This script imports neither SymPy nor any repository verifier.  It rebuilds
the rational graph, uses its own recursive matching expansion and sparse
column reduction, and literally assembles the labelled GLS23 nuisance and
the three normal-pencil coefficient equations.
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
E = (
    (F(1), F(0), F(0)),
    (F(0), F(1), F(0)),
    (F(0), F(0), F(1)),
)


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
    e00, e11, e22 = unit(0, 0), unit(1, 1), unit(2, 2)
    w = (F(0), F(1), F(1))
    j = outer(w, w)

    put(edges, A0, Q0, e11)
    put(edges, A0, Q1, e22)
    put(edges, A1, Q0, e22)
    put(edges, A1, Q1, e11)
    put(edges, Q0, Q1, e00)

    put(edges, A0, K, outer((1, 0, -1), E[0]))
    put(edges, A1, K, outer((1, 1, -2), E[0]))
    for root in (A0, A1):
        for port in (U1, U2, U3):
            put(edges, root, port, e00)

    port_weights = {K: F(1), U1: F(1), U2: F(1), U3: F(1, 12)}
    for port, value in port_weights.items():
        put(edges, Q0, port, scale(value, outer(E[0], w)))
        put(edges, Q1, port, scale(-value, outer(E[0], w)))

    response_scalars = {
        (K, U1): F(1),
        (K, U2): F(1),
        (K, U3): F(-3, 2),
        (U1, U2): F(1),
        (U1, U3): F(1),
        (U2, U3): F(-2),
    }
    for pair, value in response_scalars.items():
        left, right = pair
        correction = scale(2 * port_weights[left] * port_weights[right], j)
        put(edges, left, right, add(scale(value, e00), correction))
    return edges, port_weights, response_scalars


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
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


def tensor_index(values):
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
    for colour_a0, colour_a1 in product(range(3), repeat=2):
        for kept_values in product(range(3), repeat=len(promoted)):
            kept = dict(zip(promoted, kept_values, strict=True))
            total = F(0)
            for residual_values in product(range(3), repeat=len(residual)):
                colours = {
                    A0: colour_a0,
                    A1: colour_a1,
                    **kept,
                    **dict(zip(residual, residual_values, strict=True)),
                }
                for matching in local_matchings:
                    term = F(1)
                    for left, right in matching:
                        term *= edge(edges, left, right)[colours[left]][colours[right]]
                    total += term
            answer[3 * colour_a0 + colour_a1][tensor_index(kept_values)] = total
    return promoted, answer


def projector(edges):
    _, q = companion(edges, Q)
    p = sum(row[0] for row in q)
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
            basis[pivot] = {row: value / lead for row, value in vector.items()}
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


def inserted_columns(target, promoted, companion_matrix):
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
                    vector[9 * root + tensor_index(c_values)] = companion_matrix[root][
                        tensor_index(d_values)
                    ]
            answer.append(vector)
    return answer


def flatten(companion_matrix):
    return [companion_matrix[root][port] for root in range(9) for port in range(9)]


def response(edges, pair):
    left, right = pair
    answer = zero_matrix()
    local_matchings = tuple(matchings((Q0, Q1, left, right)))
    for colour_left, colour_right in product(range(3), repeat=2):
        total = F(0)
        for colour_q0, colour_q1 in product(range(3), repeat=2):
            colours = {
                Q0: colour_q0,
                Q1: colour_q1,
                left: colour_left,
                right: colour_right,
            }
            for matching in local_matchings:
                term = F(1)
                for first, second in matching:
                    term *= edge(edges, first, second)[colours[first]][colours[second]]
                total += term
        answer[colour_left][colour_right] = total
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


def bilinear(left, matrix, right):
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row, column in product(range(3), repeat=2)
    )


def one_q_deck(edges, removed_residual, removed_port):
    vertices = tuple(
        vertex for vertex in B_HAT if vertex not in (removed_residual, removed_port)
    )
    residual = next(vertex for vertex in vertices if vertex in Q)
    promoted = tuple(vertex for vertex in vertices if vertex in PORTS)
    answer = [F(0)] * 27
    local_matchings = tuple(matchings(vertices))
    for promoted_values in product(range(3), repeat=3):
        colours = dict(zip(promoted, promoted_values, strict=True))
        for residual_colour in range(3):
            colours[residual] = residual_colour
            for matching in local_matchings:
                term = F(1)
                for left, right in matching:
                    term *= edge(edges, left, right)[colours[left]][colours[right]]
                answer[tensor_index(promoted_values)] += term
    return promoted, answer


def external_pair(left, left_ports, right, right_ports):
    answer = [F(0)] * 81
    left_indices = [PORTS.index(port) for port in left_ports]
    right_indices = [PORTS.index(port) for port in right_ports]
    for word in product(range(3), repeat=4):
        answer[tensor_index(word)] = (
            left[word[left_indices[0]]][word[left_indices[1]]]
            * right[word[right_indices[0]]][word[right_indices[1]]]
        )
    return answer


def external_single(single, port, deck, deck_ports):
    answer = [F(0)] * 81
    port_index = PORTS.index(port)
    deck_indices = [PORTS.index(deck_port) for deck_port in deck_ports]
    for word in product(range(3), repeat=4):
        deck_values = tuple(word[position] for position in deck_indices)
        answer[tensor_index(word)] = (
            single[word[port_index]] * deck[tensor_index(deck_values)]
        )
    return answer


def vector_add_in_place(left, right, scale_factor=F(1)):
    for position, value in enumerate(right):
        left[position] += scale_factor * value


def check_maximum_root_and_incidence(edges, port_weights, response_scalars):
    root_values = (
        bilinear(ONE, edge(edges, A0, A1), ONE),
        bilinear(ONE, edge(edges, A0, K), ONE),
        bilinear(ONE, edge(edges, A1, K), ONE),
    )
    assert root_values == (F(0), F(0), F(0))

    # Any root containing A_i contains no Q_s or u_j, by the displayed
    # matrix-unit edges, so it has size at most three.  Without A, a Q_s
    # forces w(z_u)=0 at every accompanying promoted port; two such ports
    # then contradict their nonzero response scalar.  With only the four
    # promoted ports, the six edge equations would force the following
    # three complementary products to agree.
    for root in (A0, A1):
        for vertex in (*Q, U1, U2, U3):
            assert (
                sum(value != 0 for row in edge(edges, root, vertex) for value in row)
                == 1
            )
    assert all(port_weights[port] for port in PORTS)
    assert all(response_scalars[pair] for pair in PORT_PAIRS)
    cross_products = (
        response_scalars[K, U1] * response_scalars[U2, U3],
        response_scalars[K, U2] * response_scalars[U1, U3],
        response_scalars[K, U3] * response_scalars[U1, U2],
    )
    assert cross_products == (F(-2), F(1), F(-3, 2))
    assert len(set(cross_products)) == 3

    incidence_ranks = []
    for vertex in (Q0, Q1, U1, U2, U3):
        rows = [row_times(edge(edges, root, vertex), ONE) for root in ROOTS]
        columns = [list(column) for column in zip(*rows, strict=True)]
        incidence_ranks.append(rank(columns)[0])
    assert incidence_ranks == [3, 3, 2, 2, 2]
    assert sum(3 - value for value in incidence_ranks) == 3
    return root_values, cross_products, incidence_ranks


def check_modules(edges):
    q, p, projection = projector(edges)
    assert p == 2
    assert [q[row][0] for row in range(9)] == [0, 0, 0, 0, 1, 0, 0, 0, 1]
    assert rank(matrix_columns(projection))[0] == 8

    projected = {}
    for label in LABELS:
        promoted, raw = companion(edges, label)
        projected[label] = promoted, matmul(projection, raw)

    pair_records = []
    for target in PORT_PAIRS:
        nuisance_columns = []
        for label, (promoted, companion_matrix) in projected.items():
            if label != target:
                nuisance_columns.extend(
                    inserted_columns(target, promoted, companion_matrix)
                )
        nuisance_rank, nuisance_basis = rank(nuisance_columns)
        desired_matrix = projected[target][1]
        desired_slice_rank = rank(matrix_columns(desired_matrix))[0]
        absorbed = not reduce_column(
            sparse(flatten(desired_matrix)), dict(nuisance_basis)
        )
        pair_records.append((target, desired_slice_rank, nuisance_rank, absorbed))
    assert [record[1] for record in pair_records] == [1] * 6
    assert [record[2] for record in pair_records] == [36, 36, 36, 50, 50, 50]
    assert all(record[3] for record in pair_records)

    top_columns = []
    for _, companion_matrix in projected.values():
        top_columns.extend(matrix_columns(companion_matrix))
    top_rank, top_basis = rank(top_columns)
    diagonal_columns = []
    for colour in range(3):
        diagonal_columns.append(
            [projection[row][3 * colour + colour] for row in range(9)]
        )
    diagonal_rank = rank(diagonal_columns)[0]
    assert top_rank == 6
    assert diagonal_rank == 2
    for column in diagonal_columns:
        assert not reduce_column(sparse(column), dict(top_basis))
    assert rank(top_columns + diagonal_columns)[0] == 6
    return pair_records, top_rank, diagonal_rank


def check_contraction_profiles(edges, response_scalars):
    normal = E[0]
    a = {port: row_times(edge(edges, A0, port), ONE) for port in PORTS}
    x = {port: row_times(edge(edges, A0, port), normal) for port in PORTS}
    b = {port: row_times(edge(edges, A1, port), ONE) for port in PORTS}
    y = {port: row_times(edge(edges, A1, port), normal) for port in PORTS}
    assert a[K] == b[K] == [F(0), F(0), F(0)]
    assert all(a[port] == b[port] == [F(1), F(0), F(0)] for port in PORTS[1:])
    assert all(x[port] == y[port] == [F(1), F(0), F(0)] for port in PORTS)

    responses = {pair: response(edges, pair) for pair in PORT_PAIRS}
    assert all(
        responses[pair] == scale(response_scalars[pair], unit(0, 0))
        for pair in PORT_PAIRS
    )
    assert all(response_scalars[pair] for pair in PORT_PAIRS)

    suppliers_11 = {
        pair: add(
            outer(x[pair[0]], y[pair[1]]),
            outer(y[pair[0]], x[pair[1]]),
        )
        for pair in PORT_PAIRS
    }
    assert all(matrix == scale(2, unit(0, 0)) for matrix in suppliers_11.values())
    assert all(
        suppliers_11[tuple(port for port in PORTS if port not in target)]
        for target in PORT_PAIRS
    )

    # The two individual one-Q decks are retained and nontrivial, but their
    # exact weighted sum cancels at every removed promoted port.
    one_q_nonzero_entries = 0
    one_q_cancellations = 0
    for port in PORTS:
        kept0, deck0 = one_q_deck(edges, Q0, port)
        kept1, deck1 = one_q_deck(edges, Q1, port)
        assert kept0 == kept1
        one_q_nonzero_entries += sum(value != 0 for value in deck0)
        one_q_nonzero_entries += sum(value != 0 for value in deck1)
        assert all(left + right == 0 for left, right in zip(deck0, deck1, strict=True))
        one_q_cancellations += 1
    assert one_q_nonzero_entries > 0
    assert one_q_cancellations == 4

    weights_0 = {}
    weights_1 = {}
    for residual in Q:
        xi0 = matrix_times_column(edge(edges, A0, residual), ONE)
        xi1 = matrix_times_column(edge(edges, A1, residual), ONE)
        weights_0[residual] = sum(xi0)
        weights_1[residual] = sum(xi1)
    assert tuple(weights_0.values()) == (F(1), F(1))
    assert tuple(weights_1.values()) == (F(1), F(1))

    def assemble(kind):
        total = [F(0)] * 81
        for supplier_pair in PORT_PAIRS:
            left, right = supplier_pair
            response_pair = tuple(port for port in PORTS if port not in supplier_pair)
            if kind == "10":
                supplier = add(outer(x[left], b[right]), outer(b[left], x[right]))
            elif kind == "01":
                supplier = add(outer(a[left], y[right]), outer(y[left], a[right]))
            else:
                supplier = suppliers_11[supplier_pair]
            vector_add_in_place(
                total,
                external_pair(
                    supplier,
                    supplier_pair,
                    responses[response_pair],
                    response_pair,
                ),
            )

        if kind in ("10", "01"):
            for residual in Q:
                weight = weights_1[residual] if kind == "10" else weights_0[residual]
                for port in PORTS:
                    deck_ports, deck = one_q_deck(edges, residual, port)
                    single = x[port] if kind == "10" else y[port]
                    vector_add_in_place(
                        total,
                        external_single(single, port, deck, deck_ports),
                        weight,
                    )
        return total

    target = [F(0)] * 81
    target[0] = F(1)
    residual_counts = {}
    for kind in ("10", "01", "11"):
        observed = assemble(kind)
        residual_counts[kind] = sum(
            left != right for left, right in zip(observed, target, strict=True)
        )
    assert residual_counts == {"10": 0, "01": 0, "11": 0}

    # The scalar arithmetic behind the three equations is independently
    # visible: the normal sum is 2 sum(lambda)=1, while each first-polar sum
    # is twice the three responses incident with k; the other three sum zero.
    incident = sum(response_scalars[pair] for pair in PORT_PAIRS if K in pair)
    nonincident = sum(response_scalars[pair] for pair in PORT_PAIRS if K not in pair)
    assert (2 * sum(response_scalars.values()), 2 * incident, nonincident) == (
        F(1),
        F(1),
        F(0),
    )
    return responses, residual_counts, one_q_nonzero_entries


def check_coefficients(edges):
    pure = tuple(coefficient(edges, (colour,) * 8) for colour in range(3))
    assert pure == (F(1), F(1), F(1))
    failures = []
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        value = coefficient(edges, word)
        if value:
            failures.append((word, value))
    hamming_one = ((1, 1, 1, 1, 1, 1, 1, 2), F(1))
    assert len(failures) == 316
    assert hamming_one in failures
    return pure, len(failures), hamming_one


def check():
    edges, port_weights, response_scalars = build_control()
    root = check_maximum_root_and_incidence(edges, port_weights, response_scalars)
    modules = check_modules(edges)
    profiles = check_contraction_profiles(edges, response_scalars)
    coefficients = check_coefficients(edges)
    return {
        "root_cross_products_incidence": root,
        "pair_top_modules": modules,
        "response_scalars": tuple(profiles[0][pair][0][0] for pair in PORT_PAIRS),
        "profile_residuals": profiles[1],
        "retained_one_q_entries": profiles[2],
        "pure_mixed_hamming_one": coefficients,
    }


def main():
    result = check()
    print("first-polarized simultaneous-absorption Fraction audit: PASS")
    print("  exact replay:", result)
    print("  no SymPy/primary/GLS31 imports; witness/node/global closure OPEN")


if __name__ == "__main__":
    main()
