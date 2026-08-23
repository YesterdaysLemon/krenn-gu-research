"""Focused exact checks for the GLS31 simultaneous-absorption sharpness theorem."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


A0, A1, Q0, Q1, K, U1, U2, U3 = range(8)
VERTICES = tuple(range(8))
ROOTS = (A0, A1, K)
Q = (Q0, Q1)
PORTS = (K, U1, U2, U3)
B_HAT = Q + PORTS
PORT_PAIRS = tuple(combinations(PORTS, 2))
LABELS = tuple(combinations(B_HAT, 2))
ONE = sp.ones(3, 1)
EYE = sp.eye(3)
E = tuple(EYE[:, index] for index in range(3))


def outer(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(left) * sp.Matrix(right).T


def put_edge(
    edges: dict[tuple[int, int], sp.Matrix],
    left: int,
    right: int,
    matrix: sp.MatrixBase,
) -> None:
    if left < right:
        edges[left, right] = sp.Matrix(matrix)
    else:
        edges[right, left] = sp.Matrix(matrix).T


def edge_block(
    edges: dict[tuple[int, int], sp.Matrix], left: int, right: int
) -> sp.Matrix:
    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


def build_control() -> dict[tuple[int, int], sp.Matrix]:
    edges: dict[tuple[int, int], sp.Matrix] = {}
    e00 = outer(E[0], E[0])
    e11 = outer(E[1], E[1])
    e22 = outer(E[2], E[2])
    j = outer(E[1] + E[2], E[1] + E[2])

    put_edge(edges, A0, Q0, e11)
    put_edge(edges, A0, Q1, e22)
    put_edge(edges, A1, Q0, e22)
    put_edge(edges, A1, Q1, e11)
    put_edge(edges, Q0, Q1, e00)

    put_edge(edges, A0, K, outer(E[0] - E[2], E[0]))
    put_edge(edges, A1, K, outer(E[0] + E[1] - 2 * E[2], E[0]))
    for root in (A0, A1):
        for port in (U1, U2, U3):
            put_edge(edges, root, port, e00)

    put_edge(edges, Q0, K, e11 + e22)
    put_edge(edges, Q0, U1, e11 + e22)
    put_edge(edges, Q1, U2, e11 + e22)
    put_edge(edges, Q1, U3, sp.Rational(1, 2) * (e11 + e22))

    put_edge(edges, K, U1, e00)
    put_edge(edges, K, U2, e00 - j)
    put_edge(edges, K, U3, e00 - sp.Rational(1, 2) * j)
    put_edge(edges, U1, U2, e00 - j)
    put_edge(edges, U1, U3, e00 - sp.Rational(1, 2) * j)
    put_edge(edges, U2, U3, sp.Rational(-9, 2) * e00)
    return edges


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((left, right),) + tail


MATCHINGS_8 = tuple(perfect_matchings(VERTICES))


def graph_coefficient(
    edges: dict[tuple[int, int], sp.Matrix], word: tuple[int, ...]
) -> sp.Expr:
    total = 0
    for matching in MATCHINGS_8:
        term = 1
        for left, right in matching:
            term *= edge_block(edges, left, right)[word[left], word[right]]
        total += term
    return sp.factor(total)


def tensor_index(values: tuple[int, ...]) -> int:
    answer = 0
    for value in values:
        answer = 3 * answer + value
    return answer


def residual_companion(
    edges: dict[tuple[int, int], sp.Matrix], label: tuple[int, int]
) -> tuple[tuple[int, ...], sp.Matrix]:
    """Evaluate residual label ports at ONE and retain promoted label ports."""

    promoted = tuple(port for port in PORTS if port in label)
    residual = tuple(vertex for vertex in Q if vertex in label)
    columns = 3 ** len(promoted)
    answer = sp.zeros(9, columns)
    four_vertices = (A0, A1, *label)
    four_matchings = tuple(perfect_matchings(four_vertices))
    for a0_colour, a1_colour in product(range(3), repeat=2):
        for promoted_values in product(range(3), repeat=len(promoted)):
            kept = dict(zip(promoted, promoted_values, strict=True))
            total = 0
            for residual_values in product(range(3), repeat=len(residual)):
                colours = {
                    A0: a0_colour,
                    A1: a1_colour,
                    **kept,
                    **dict(zip(residual, residual_values, strict=True)),
                }
                for matching in four_matchings:
                    term = 1
                    for left, right in matching:
                        term *= edge_block(edges, left, right)[
                            colours[left], colours[right]
                        ]
                    total += term
            answer[3 * a0_colour + a1_colour, tensor_index(promoted_values)] = total
    return promoted, answer


def residual_projector(
    edges: dict[tuple[int, int], sp.Matrix],
) -> tuple[sp.Matrix, sp.Expr, sp.Matrix]:
    _, q = residual_companion(edges, Q)
    epsilon = sp.kronecker_product(ONE.T, ONE.T)
    p = (epsilon * q)[0]
    projector = p * sp.eye(9) - q * epsilon
    assert p == 2
    assert projector.rank() == 8
    assert projector * q == sp.zeros(9, 1)
    return q, p, projector


def response_matrix(
    edges: dict[tuple[int, int], sp.Matrix], pair: tuple[int, int]
) -> sp.Matrix:
    left, right = pair
    answer = sp.zeros(3)
    matchings = tuple(perfect_matchings((Q0, Q1, left, right)))
    for left_colour, right_colour in product(range(3), repeat=2):
        total = 0
        for q0_colour, q1_colour in product(range(3), repeat=2):
            colours = {
                Q0: q0_colour,
                Q1: q1_colour,
                left: left_colour,
                right: right_colour,
            }
            for matching in matchings:
                term = 1
                for first, second in matching:
                    term *= edge_block(edges, first, second)[
                        colours[first], colours[second]
                    ]
                total += term
        answer[left_colour, right_colour] = total
    return answer


def inserted_slices(
    target: tuple[int, int],
    promoted: tuple[int, ...],
    coefficient: sp.Matrix,
) -> sp.Matrix:
    x_vertices = tuple(vertex for vertex in target if vertex in promoted)
    y_vertices = tuple(vertex for vertex in promoted if vertex not in target)
    z_vertices = tuple(vertex for vertex in target if vertex not in promoted)
    columns: list[sp.Matrix] = []
    for y_values in product(range(3), repeat=len(y_vertices)):
        y_map = dict(zip(y_vertices, y_values, strict=True))
        for z_values in product(range(3), repeat=len(z_vertices)):
            z_map = dict(zip(z_vertices, z_values, strict=True))
            vector = sp.zeros(81, 1)
            for root_index in range(9):
                for x_values in product(range(3), repeat=len(x_vertices)):
                    x_map = dict(zip(x_vertices, x_values, strict=True))
                    promoted_values = tuple(
                        {**x_map, **y_map}[vertex] for vertex in promoted
                    )
                    target_values = tuple(
                        {**x_map, **z_map}[vertex] for vertex in target
                    )
                    row = 9 * root_index + tensor_index(target_values)
                    vector[row] = coefficient[root_index, tensor_index(promoted_values)]
            columns.append(vector)
    return sp.Matrix.hstack(*columns)


def flatten_pair_tensor(coefficient: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [coefficient[root, port] for root in range(9) for port in range(9)]
    )


def check_maximum_root_and_incidence(
    edges: dict[tuple[int, int], sp.Matrix],
) -> dict[str, object]:
    assert edge_block(edges, A0, A1) == sp.zeros(3)
    for root in (A0, A1):
        assert (ONE.T * edge_block(edges, root, K) * ONE)[0] == 0

    monomial_edges = {
        pair
        for pair in combinations(VERTICES, 2)
        if sum(entry != 0 for entry in edge_block(edges, *pair)) == 1
    }
    independent_number = max(
        len(subset)
        for size in range(9)
        for subset in combinations(VERTICES, size)
        if all(pair not in monomial_edges for pair in combinations(subset, 2))
    )
    assert independent_number == 3

    outside = (Q0, Q1, U1, U2, U3)
    incidence = {
        vertex: sp.Matrix.vstack(
            *(ONE.T * edge_block(edges, root, vertex) for root in ROOTS)
        )
        for vertex in outside
    }
    ranks = tuple(incidence[vertex].rank() for vertex in outside)
    assert ranks == (2, 2, 1, 2, 2)
    assert sum(3 - rank for rank in ranks) == 6
    return {
        "monomial_independence_number": independent_number,
        "incidence_ranks": ranks,
        "incidence_defect": 6,
    }


def check_transverse_modules(
    edges: dict[tuple[int, int], sp.Matrix],
) -> dict[str, object]:
    q, p, projector = residual_projector(edges)
    expected_q = sp.zeros(9, 1)
    expected_q[4] = expected_q[8] = 1
    assert q == expected_q

    projected: dict[tuple[int, int], tuple[tuple[int, ...], sp.Matrix]] = {}
    for label in LABELS:
        promoted, coefficient = residual_companion(edges, label)
        projected[label] = promoted, projector * coefficient
    assert projected[Q][1] == sp.zeros(9, 1)

    top_columns = [coefficient for _, coefficient in projected.values()]
    top_nuisance = sp.Matrix.hstack(*top_columns)
    assert top_nuisance.rank() == 6
    diagonal = sp.Matrix.hstack(
        *(projector * sp.eye(9)[:, 3 * colour + colour] for colour in range(3))
    )
    assert diagonal.rank() == 2
    assert top_nuisance.row_join(diagonal).rank() == top_nuisance.rank()

    target_records = []
    for target in PORT_PAIRS:
        nuisance_columns = []
        for label, (promoted, coefficient) in projected.items():
            if label == target:
                continue
            nuisance_columns.append(inserted_slices(target, promoted, coefficient))
        nuisance = sp.Matrix.hstack(*nuisance_columns)
        desired = flatten_pair_tensor(projected[target][1])
        nuisance_rank = nuisance.rank()
        augmented_rank = nuisance.row_join(desired).rank()
        assert augmented_rank == nuisance_rank
        target_records.append(
            (target, projected[target][1].rank(), nuisance_rank, augmented_rank)
        )
    assert tuple(record[1] for record in target_records) == (1,) * 6
    assert tuple(record[2] for record in target_records) == (36, 36, 36, 50, 50, 50)
    return {
        "p": p,
        "top_nuisance_rank": top_nuisance.rank(),
        "diagonal_rank": diagonal.rank(),
        "pair_records": tuple(target_records),
    }


def tensor4_from_pair_terms(
    suppliers: dict[tuple[int, int], sp.Matrix],
    responses: dict[tuple[int, int], sp.Matrix],
) -> dict[tuple[int, int, int, int], sp.Expr]:
    answer: dict[tuple[int, int, int, int], sp.Expr] = {}
    for word in product(range(3), repeat=4):
        total = 0
        for pair in combinations(range(4), 2):
            complement = tuple(index for index in range(4) if index not in pair)
            physical_pair = tuple(PORTS[index] for index in pair)
            physical_complement = tuple(PORTS[index] for index in complement)
            total += (
                suppliers[physical_pair][word[pair[0]], word[pair[1]]]
                * responses[physical_complement][
                    word[complement[0]], word[complement[1]]
                ]
            )
        answer[word] = sp.factor(total)
    return answer


def check_normal_and_full_coefficients(
    edges: dict[tuple[int, int], sp.Matrix],
) -> dict[str, object]:
    e00 = outer(E[0], E[0])
    normal = E[0]
    x = {port: (normal.T * edge_block(edges, A0, port)).T for port in PORTS}
    y = {port: (normal.T * edge_block(edges, A1, port)).T for port in PORTS}
    assert all(vector == E[0] for vector in (*x.values(), *y.values()))
    suppliers = {
        pair: outer(x[pair[0]], y[pair[1]]) + outer(y[pair[0]], x[pair[1]])
        for pair in PORT_PAIRS
    }
    assert all(supplier == 2 * e00 for supplier in suppliers.values())
    responses = {pair: response_matrix(edges, pair) for pair in PORT_PAIRS}
    scalars = tuple(response[0, 0] for response in responses.values())
    assert scalars == (1, 1, 1, 1, 1, sp.Rational(-9, 2))
    assert all(
        response == scalar * e00
        for scalar, response in zip(scalars, responses.values(), strict=True)
    )
    normal_tensor = tensor4_from_pair_terms(suppliers, responses)
    assert normal_tensor[(0, 0, 0, 0)] == 1
    assert all(
        value == 0 for word, value in normal_tensor.items() if word != (0, 0, 0, 0)
    )

    pure = tuple(graph_coefficient(edges, (colour,) * 8) for colour in range(3))
    assert pure == (1, 1, 1)
    mixed_failures = []
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        value = graph_coefficient(edges, word)
        if value != 0:
            mixed_failures.append((word, value))
    assert len(mixed_failures) == 313
    assert ((0, 0, 0, 0, 0, 1, 0, 1), -1) in mixed_failures
    return {
        "responses": scalars,
        "normal_tensor_support": ((0, 0, 0, 0),),
        "pure_coefficients": pure,
        "mixed_failures": len(mixed_failures),
        "first_failure": mixed_failures[0],
    }


def evaluate_root_tensor(
    tensor: sp.Matrix,
    left: sp.MatrixBase,
    right: sp.MatrixBase,
) -> sp.Matrix:
    answer = sp.zeros(3)
    for left_port, right_port in product(range(3), repeat=2):
        column = 3 * left_port + right_port
        answer[left_port, right_port] = sum(
            left[a0] * right[a1] * tensor[3 * a0 + a1, column]
            for a0, a1 in product(range(3), repeat=2)
        )
    return answer


def evaluate_root_one_port(
    tensor: sp.Matrix,
    left: sp.MatrixBase,
    right: sp.MatrixBase,
) -> sp.Matrix:
    answer = sp.zeros(3, 1)
    for port_colour in range(3):
        answer[port_colour] = sum(
            left[a0] * right[a1] * tensor[3 * a0 + a1, port_colour]
            for a0, a1 in product(range(3), repeat=2)
        )
    return answer


def check_tangent_pencil(edges: dict[tuple[int, int], sp.Matrix]) -> dict[str, object]:
    q, p, projector = residual_projector(edges)
    n0 = n1 = E[0]
    t, u = sp.symbols("t u")
    s0 = s1 = ONE
    left_pencil = s0 + t * n0
    right_pencil = s1 + u * n1
    q_matrix = sp.Matrix(3, 3, list(q))
    assert (left_pencil.T * q_matrix * right_pencil)[0] == p

    checked = 0
    for pair in PORT_PAIRS:
        first, second = pair
        _, raw = residual_companion(edges, pair)
        projected = projector * raw
        a_first = (s0.T * edge_block(edges, A0, first)).T
        x_first = (n0.T * edge_block(edges, A0, first)).T
        b_first = (s1.T * edge_block(edges, A1, first)).T
        y_first = (n1.T * edge_block(edges, A1, first)).T
        a_second = (s0.T * edge_block(edges, A0, second)).T
        x_second = (n0.T * edge_block(edges, A0, second)).T
        b_second = (s1.T * edge_block(edges, A1, second)).T
        y_second = (n1.T * edge_block(edges, A1, second)).T
        k10 = outer(x_first, b_second) + outer(b_first, x_second)
        k01 = outer(a_first, y_second) + outer(y_first, a_second)
        k11 = outer(x_first, y_second) + outer(y_first, x_second)
        expected = p * (t * k10 + u * k01 + t * u * k11)
        assert sp.simplify(
            evaluate_root_tensor(projected, left_pencil, right_pencil) - expected
        ) == sp.zeros(3)
        checked += 1

    one_q_checked = 0
    for residual in Q:
        xi0 = edge_block(edges, A0, residual) * ONE
        xi1 = edge_block(edges, A1, residual) * ONE
        lambda0 = (ONE.T * xi0)[0]
        lambda1 = (ONE.T * xi1)[0]
        for port in PORTS:
            _, raw = residual_companion(edges, (residual, port))
            projected = projector * raw
            x_port = (n0.T * edge_block(edges, A0, port)).T
            y_port = (n1.T * edge_block(edges, A1, port)).T
            expected = p * (t * lambda1 * x_port + u * lambda0 * y_port)
            assert sp.simplify(
                evaluate_root_one_port(projected, left_pencil, right_pencil) - expected
            ) == sp.zeros(3, 1)
            one_q_checked += 1
    assert projector * residual_companion(edges, Q)[1] == sp.zeros(9, 1)
    assert edge_block(edges, A0, A1) == sp.zeros(3)

    diagonal_checks = 0
    for colour in range(3):
        delta = projector * sp.eye(9)[:, 3 * colour + colour]
        observed = sum(
            left_pencil[a0] * right_pencil[a1] * delta[3 * a0 + a1]
            for a0, a1 in product(range(3), repeat=2)
        )
        expected = p * (
            t * n0[colour] * s1[colour]
            + u * s0[colour] * n1[colour]
            + t * u * n0[colour] * n1[colour]
        )
        assert sp.expand(observed - expected) == 0
        diagonal_checks += 1

    # Exact retained-root quotient diagram for X0=X1=<e1,e2>.
    tangent_columns = []
    for x0 in (E[1], E[2]):
        for basis in E:
            tangent_columns.append(sp.kronecker_product(x0, basis))
    for basis in E:
        for x1 in (E[1], E[2]):
            tangent_columns.append(sp.kronecker_product(basis, x1))
    tangent = projector * sp.Matrix.hstack(*tangent_columns)
    c0 = sp.zeros(3, 9)
    for first, second in product(range(3), repeat=2):
        c0[second, 3 * first + second] = n0[first]
    assert tangent.rank() == 7
    assert (c0 * projector).rank() == 3
    assert (c0 * tangent).rank() == 2
    diagonal = sp.Matrix.hstack(
        *(projector * sp.eye(9)[:, 3 * colour + colour] for colour in range(3))
    )
    assert tangent.row_join(diagonal).rank() == 8
    return {
        "pencil_pairs": checked,
        "one_q_labels": one_q_checked,
        "diagonal_rows": diagonal_checks,
        "transverse_rank": projector.rank(),
        "tangent_rank": tangent.rank(),
        "retained_quotient_dimension": 1,
        "diagonal_mod_tangent_rank": 1,
    }


def main() -> None:
    edges = build_control()
    root = check_maximum_root_and_incidence(edges)
    modules = check_transverse_modules(edges)
    coefficients = check_normal_and_full_coefficients(edges)
    tangent = check_tangent_pencil(edges)
    print("GLS31 simultaneous absorption and tangent-pencil primary checks: PASS")
    print("  maximum-root/incidence:", root)
    print("  complete GLS23/GLS26 modules:", modules)
    print("  normal/pure/mixed coefficients:", coefficients)
    print("  tangent pencil and quotient diagram:", tangent)
    print("  scope: exact sharpness plus identities; witness/node/global closure OPEN")


if __name__ == "__main__":
    main()
