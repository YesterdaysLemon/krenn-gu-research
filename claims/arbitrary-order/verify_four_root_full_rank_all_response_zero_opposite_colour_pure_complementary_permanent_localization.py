"""Focused exact replay for the four-root full-rank response-zero theorem.

This is a bounded verifier, not the proof of the arbitrary-point theorem.  It
checks the tensor identities used by the written proof, exact sharpness
controls, and the complete ten-vertex boundary fixture over ``QQ``.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
OUTSIDE = (Q0, Q1) + PORTS
ALL_VERTICES = ROOTS + OUTSIDE


def matrix_unit(row: int, column: int, coefficient: sp.Expr | int = 1):
    """Return one exact ternary matrix unit."""

    answer = sp.zeros(3)
    answer[row, column] = coefficient
    return answer


def response_flattening(
    h_matrix: sp.Matrix,
    a_u: sp.Matrix,
    c_u: sp.Matrix,
    a_v: sp.Matrix,
    c_v: sp.Matrix,
    b_uv: sp.Matrix,
) -> sp.Matrix:
    """Return Z_uv flattened across (q0,q1)|(u,v)."""

    return sp.Matrix(
        9,
        9,
        lambda q_index, port_index: (
            h_matrix[q_index // 3, q_index % 3] * b_uv[port_index // 3, port_index % 3]
            + a_u[q_index // 3, port_index // 3] * c_v[q_index % 3, port_index % 3]
            + a_v[q_index // 3, port_index % 3] * c_u[q_index % 3, port_index // 3]
        ),
    )


def cross_realignment(
    a_u: sp.Matrix,
    c_v: sp.Matrix,
    a_v: sp.Matrix,
    c_u: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Flatten the two cross products across (q0,u)|(q1,v)."""

    first = sp.Matrix(
        9,
        9,
        lambda row, column: a_u[row // 3, row % 3] * c_v[column // 3, column % 3],
    )
    second = sp.Matrix(
        9,
        9,
        lambda row, column: a_v[row // 3, column % 3] * c_u[column // 3, row % 3],
    )
    return first, second


def check_rank_three_and_realignment_identities() -> None:
    """Replay the two load-bearing exact rank identities."""

    h_entries = sp.symbols("h_0:9")
    h_matrix = sp.Matrix(3, 3, h_entries)
    scalar = sp.symbols("b")
    x = sp.Matrix(sp.symbols("x_0:3"))
    y = sp.Matrix(sp.symbols("y_0:3"))
    p = sp.Matrix(sp.symbols("p_0:3"))
    q = sp.Matrix(sp.symbols("q_0:3"))

    # A sum of two outer products has determinant zero.  Thus a zero response
    # slice gives b^3 det(H)=0, and det(H) != 0 forces b=0 without dividing by
    # a response coordinate.
    rank_two_sum = x * y.T + p * q.T
    assert sp.expand(rank_two_sum.det()) == 0
    assert sp.expand((scalar * h_matrix).det() - scalar**3 * h_matrix.det()) == 0

    a_u = sp.Matrix(3, 3, sp.symbols("au_0:9"))
    c_u = sp.Matrix(3, 3, sp.symbols("cu_0:9"))
    a_v = sp.Matrix(3, 3, sp.symbols("av_0:9"))
    c_v = sp.Matrix(3, 3, sp.symbols("cv_0:9"))
    b_uv = sp.Matrix(3, 3, sp.symbols("buv_0:9"))
    response = response_flattening(h_matrix, a_u, c_u, a_v, c_v, b_uv)
    for s, t in product(COLOURS, repeat=2):
        q_slice = sp.Matrix(
            [[response[3 * a + b, 3 * s + t] for b in COLOURS] for a in COLOURS]
        )
        expected = (
            b_uv[s, t] * h_matrix + a_u[:, s] * c_v[:, t].T + a_v[:, t] * c_u[:, s].T
        )
        assert q_slice == expected

    # Lemma 3 uses a different realignment.  The first cross term is an
    # outer product; the second is a column-permuted Kronecker product.
    first, second = cross_realignment(a_u, c_v, a_v, c_u)
    vec_a_u = sp.Matrix([a_u[a, s] for a in COLOURS for s in COLOURS])
    vec_c_v = sp.Matrix([c_v[b, t] for b in COLOURS for t in COLOURS])
    assert first == vec_a_u * vec_c_v.T
    kron = sp.kronecker_product(a_v, c_u.T)
    column_permutation = [3 * t + b for b in COLOURS for t in COLOURS]
    assert second == kron[:, column_permutation]

    for rank_a, rank_c in product(range(4), repeat=2):
        diagonal_a = sp.diag(*([1] * rank_a + [0] * (3 - rank_a)))
        diagonal_c = sp.diag(*([1] * rank_c + [0] * (3 - rank_c)))
        _, exact_second = cross_realignment(
            sp.eye(3), sp.eye(3), diagonal_a, diagonal_c
        )
        assert exact_second.rank() == rank_a * rank_c


def zero_block_family() -> dict[tuple[int, int], sp.Matrix]:
    return {pair: sp.zeros(3) for pair in combinations(range(4), 2)}


def assert_all_pair_responses_zero(
    h_matrix: sp.Matrix,
    a_blocks: dict[int, sp.Matrix],
    c_blocks: dict[int, sp.Matrix],
    b_blocks: dict[tuple[int, int], sp.Matrix],
) -> None:
    for u, v in combinations(range(4), 2):
        response = response_flattening(
            h_matrix,
            a_blocks[u],
            c_blocks[u],
            a_blocks[v],
            c_blocks[v],
            b_blocks[(u, v)],
        )
        assert all(sp.expand(entry) == 0 for entry in response)


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate labelled perfect matchings recursively."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def check_top_response_is_derived() -> None:
    """Every six-vertex matching contains a direct port edge."""

    local_q0, local_q1 = 4, 5
    local_ports = tuple(range(4))
    vertices = local_ports + (local_q0, local_q1)
    matchings = tuple(perfect_matchings(vertices))
    assert len(matchings) == 15
    for matching in matchings:
        assert any(
            left in local_ports and right in local_ports for left, right in matching
        )


def check_support_and_sign_normal_forms() -> None:
    """Replay the singleton, two-port, and characteristic-zero sign forms."""

    h_matrix = sp.eye(3)
    b_blocks = zero_block_family()

    # Singleton support: all residual and local coordinate choices work.
    singleton_controls = 0
    for i, j, a, b in product(COLOURS, repeat=4):
        a_blocks = {u: sp.zeros(3) for u in range(4)}
        c_blocks = {u: sp.zeros(3) for u in range(4)}
        a_blocks[0] = matrix_unit(i, a)
        c_blocks[0] = matrix_unit(j, b)
        assert_all_pair_responses_zero(h_matrix, a_blocks, c_blocks, b_blocks)
        singleton_controls += 1
    assert singleton_controls == 81

    # Two active ports: the opposite sign cancels as a polynomial identity
    # for arbitrary nonzero port covectors.
    alpha_s = sp.Matrix(sp.symbols("alpha_s_0:3"))
    alpha_t = sp.Matrix(sp.symbols("alpha_t_0:3"))
    tau = sp.symbols("tau", nonzero=True)
    for i, j in product(COLOURS, repeat=2):
        e_i = sp.eye(3)[:, i]
        e_j = sp.eye(3)[:, j]
        a_blocks = {u: sp.zeros(3) for u in range(4)}
        c_blocks = {u: sp.zeros(3) for u in range(4)}
        a_blocks[0] = e_i * alpha_s.T
        c_blocks[0] = tau * e_j * alpha_s.T
        a_blocks[1] = e_i * alpha_t.T
        c_blocks[1] = -tau * e_j * alpha_t.T
        assert_all_pair_responses_zero(h_matrix, a_blocks, c_blocks, b_blocks)

    # This denominator-free syzygy is the saturated three-support
    # contradiction.  On a selected active chart, s1*s2*t0 and 2 are units.
    s0, s1, s2, t0, t1, t2 = sp.symbols("s0 s1 s2 t0 t1 t2")
    equation_01 = s0 * t1 + s1 * t0
    equation_02 = s0 * t2 + s2 * t0
    equation_12 = s1 * t2 + s2 * t1
    certificate = s2 * equation_01 + s1 * equation_02 - s0 * equation_12
    assert sp.expand(certificate - 2 * s1 * s2 * t0) == 0

    # A coordinate choice realizes the maximum-root local blocking asserted
    # by the sharpness controls.
    e0, e1 = sp.eye(3)[:, 0], sp.eye(3)[:, 1]
    assert len([entry for entry in e0 if entry != 0]) == 1
    assert len([entry for entry in e1 if entry != 0]) == 1


def check_determinant_and_characteristic_controls() -> None:
    """Replay the determinant-divisor and characteristic-two controls."""

    e0 = sp.eye(3)[:, 0]
    h_divisor = e0 * e0.T
    assert h_divisor.det() == 0
    alpha = [sp.Matrix(sp.symbols(f"ad_{u}_0:3")) for u in range(4)]
    beta = [sp.Matrix(sp.symbols(f"bd_{u}_0:3")) for u in range(4)]
    a_blocks = {u: e0 * alpha[u].T for u in range(4)}
    c_blocks = {u: e0 * beta[u].T for u in range(4)}
    b_blocks = {
        (u, v): -(alpha[u] * beta[v].T + beta[u] * alpha[v].T)
        for u, v in combinations(range(4), 2)
    }
    assert_all_pair_responses_zero(h_divisor, a_blocks, c_blocks, b_blocks)
    divisor_sample = b_blocks[(0, 1)].subs(
        {
            **{symbol: value for symbol, value in zip(alpha[0], (1, 0, 0))},
            **{symbol: value for symbol, value in zip(beta[0], (0, 1, 0))},
            **{symbol: value for symbol, value in zip(alpha[1], (0, 0, 1))},
            **{symbol: value for symbol, value in zip(beta[1], (1, 0, 0))},
        }
    )
    assert divisor_sample != sp.zeros(3)

    # Over ZZ the four-active-port response is nonzero but every coefficient
    # is even; reducing exactly modulo two makes all six responses zero.
    e1 = sp.eye(3)[:, 1]
    port_lines = [sp.eye(3)[:, index] for index in (0, 1, 2, 0)]
    a_char_two = {u: e0 * port_lines[u].T for u in range(4)}
    c_char_two = {u: e1 * port_lines[u].T for u in range(4)}
    b_zero = zero_block_family()
    for u, v in combinations(range(4), 2):
        response = response_flattening(
            sp.eye(3),
            a_char_two[u],
            c_char_two[u],
            a_char_two[v],
            c_char_two[v],
            b_zero[(u, v)],
        )
        coefficients = [int(entry) for entry in response]
        assert any(coefficient != 0 for coefficient in coefficients)
        assert all(coefficient % 2 == 0 for coefficient in coefficients)


def projection_matrix(killed_colour: int) -> sp.Matrix:
    retained = [colour for colour in COLOURS if colour != killed_colour]
    return sp.Matrix(
        2,
        3,
        lambda row, column: int(column == retained[row]),
    )


def pure_port_vector(colour: int) -> sp.Matrix:
    answer = sp.zeros(3**4, 1)
    index = 0
    for entry in (colour,) * 4:
        index = 3 * index + entry
    answer[index] = 1
    return answer


def projected_ghz_flattening(i: int, j: int, weights: tuple[int, int, int]):
    rho_i = projection_matrix(i)
    rho_j = projection_matrix(j)
    answer = sp.zeros(4, 3**4)
    for colour, weight in enumerate(weights):
        basis = sp.eye(3)[:, colour]
        q_vector = sp.kronecker_product(rho_i * basis, rho_j * basis)
        answer += weight * q_vector * pure_port_vector(colour).T
    return answer


def check_complete_target_projection() -> None:
    """Check H' nonvanishing, projection ranks, and factor localization."""

    weights = (2, 3, 5)
    for i, j in product(COLOURS, repeat=2):
        projected_target = projected_ghz_flattening(i, j, weights)
        assert projected_target.rank() == (2 if i == j else 1)

        # If H' vanished, H would be supported in row i union column j.  Its
        # generic such matrix has determinant zero, exactly replaying (37).
        symbols = iter(sp.symbols(f"hp_{i}_{j}_0:9"))
        supported_h = sp.zeros(3)
        for row, column in product(COLOURS, repeat=2):
            if row == i or column == j:
                supported_h[row, column] = next(symbols)
        assert sp.expand(supported_h.det()) == 0

    # A nonzero outer product has singleton support only when both factor
    # supports are singleton.  A five-coordinate second factor is enough to
    # replay the dimension-free Cartesian-support argument.
    subsets_left = [
        frozenset(subset)
        for size in range(1, 5)
        for subset in combinations(range(4), size)
    ]
    subsets_right = [
        frozenset(subset)
        for size in range(1, 6)
        for subset in combinations(range(5), size)
    ]
    singleton_product_supports = []
    for left_support in subsets_left:
        for right_support in subsets_right:
            cartesian = {
                (left, right) for left in left_support for right in right_support
            }
            if cartesian == {(3, 4)}:
                singleton_product_supports.append((left_support, right_support))
    assert singleton_product_supports == [(frozenset({3}), frozenset({4}))]


def fixture_edges() -> dict[tuple[int, int], sp.Matrix]:
    """Build the exact ten-vertex rational fixture from Section 9.5."""

    edges: dict[tuple[int, int], sp.Matrix] = {}

    def add(left: int, right: int, block: sp.Matrix) -> None:
        assert left < right
        assert (left, right) not in edges
        edges[(left, right)] = block

    root_port_entries = (
        (0, 0, 2),
        (1, 0, 0),
        (2, 0, 1),
        (1, 1, 2),
        (2, 1, 0),
        (3, 1, 1),
        (2, 2, 2),
        (3, 2, 0),
        (3, 3, 2),
    )
    for root, port, port_colour in root_port_entries:
        add(root, PORTS[port], matrix_unit(0, port_colour))

    root_q_entries = (
        (0, Q0, 0),
        (1, Q0, 1),
        (2, Q1, 0),
        (0, Q1, 1),
    )
    for root, q_vertex, q_colour in root_q_entries:
        add(root, q_vertex, matrix_unit(0, q_colour))

    add(Q0, Q1, sp.eye(3))
    add(Q0, PORTS[0], matrix_unit(0, 0))
    add(Q1, PORTS[0], matrix_unit(1, 0))
    add(Q0, PORTS[1], matrix_unit(0, 1))
    add(Q1, PORTS[1], matrix_unit(1, 1, sp.Integer(-1)))
    return edges


def edge_block(
    edges: dict[tuple[int, int], sp.Matrix], left: int, right: int
) -> sp.Matrix:
    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


def root_incidence_matrix(
    edges: dict[tuple[int, int], sp.Matrix], outside_vertex: int
) -> sp.Matrix:
    root_vector = sp.ones(3, 1)
    return sp.Matrix(
        4,
        3,
        lambda root, colour: (root_vector.T * edge_block(edges, root, outside_vertex))[
            0, colour
        ],
    )


def permanent_coefficient(
    incidence: dict[int, sp.Matrix],
    outside_vertices: tuple[int, ...],
    colours: dict[int, int],
) -> sp.Expr:
    answer = sp.Integer(0)
    for assigned_vertices in permutations(outside_vertices):
        term = sp.Integer(1)
        for root, vertex in enumerate(assigned_vertices):
            term *= incidence[vertex][root, colours[vertex]]
        answer += term
    return sp.expand(answer)


def complementary_permanent(
    incidence: dict[int, sp.Matrix], outside_vertices: tuple[int, ...]
) -> Counter[tuple[int, ...]]:
    answer: Counter[tuple[int, ...]] = Counter()
    for word in product(COLOURS, repeat=4):
        colours = dict(zip(outside_vertices, word))
        coefficient = permanent_coefficient(incidence, outside_vertices, colours)
        if coefficient:
            answer[word] = coefficient
    return answer


def matching_coefficient(
    edges: dict[tuple[int, int], sp.Matrix], word: tuple[int, ...]
) -> tuple[sp.Expr, list[tuple[tuple[tuple[int, int], ...], sp.Expr]]]:
    nonzero_terms = []
    total = sp.Integer(0)
    for matching in perfect_matchings(ALL_VERTICES):
        term = sp.Integer(1)
        for left, right in matching:
            term *= edge_block(edges, left, right)[word[left], word[right]]
        if term:
            nonzero_terms.append((matching, term))
            total += term
    return sp.expand(total), nonzero_terms


def check_fixture_maximum_root(
    edges: dict[tuple[int, int], sp.Matrix],
) -> None:
    root_vector = sp.ones(3, 1)
    assert all(entry != 0 for entry in root_vector)
    for left, right in combinations(ROOTS, 2):
        assert (root_vector.T * edge_block(edges, left, right) * root_vector)[0] == 0

    cliques = (
        (2, PORTS[2]),
        (3, PORTS[3]),
        (0, Q1, PORTS[0]),
        (1, Q0, PORTS[1]),
    )
    for clique in cliques:
        for left, right in combinations(clique, 2):
            block = edge_block(edges, left, right)
            assert sum(entry != 0 for entry in block) == 1

    monomial_edges = {
        (left, right)
        for left, right in combinations(ALL_VERTICES, 2)
        if sum(entry != 0 for entry in edge_block(edges, left, right)) == 1
    }
    independent_sets = []
    for mask in range(1 << len(ALL_VERTICES)):
        subset = tuple(
            vertex for index, vertex in enumerate(ALL_VERTICES) if mask & (1 << index)
        )
        if all(pair not in monomial_edges for pair in combinations(subset, 2)):
            independent_sets.append(subset)
    maximum_size = max(map(len, independent_sets))
    assert maximum_size == 4
    assert ROOTS in independent_sets


def check_fixture_incidence_and_responses(
    edges: dict[tuple[int, int], sp.Matrix],
) -> tuple[dict[int, sp.Matrix], Counter[tuple[int, ...]]]:
    incidence = {
        outside_vertex: root_incidence_matrix(edges, outside_vertex)
        for outside_vertex in OUTSIDE
    }
    f0, f1, f2, f3 = (sp.eye(4)[:, index] for index in range(4))
    expected = {
        PORTS[0]: sp.Matrix.hstack(f1, f2, f0),
        PORTS[1]: sp.Matrix.hstack(f2, f3, f1),
        PORTS[2]: sp.Matrix.hstack(f3, sp.zeros(4, 1), f2),
        PORTS[3]: sp.Matrix.hstack(sp.zeros(4, 1), sp.zeros(4, 1), f3),
        Q0: sp.Matrix.hstack(f0, f1, sp.zeros(4, 1)),
        Q1: sp.Matrix.hstack(f2, f0, sp.zeros(4, 1)),
    }
    assert incidence == expected
    ranks = tuple(incidence[vertex].rank() for vertex in PORTS + (Q0, Q1))
    assert ranks == (3, 3, 2, 1, 2, 2)
    assert sum(3 - rank for rank in ranks) == 5

    pi_q = complementary_permanent(incidence, PORTS)
    assert pi_q == Counter({(2, 2, 2, 2): 1})

    z_q0 = sp.Matrix(sp.symbols("zq0_0:3"))
    z_q1 = sp.Matrix(sp.symbols("zq1_0:3"))
    x_root = sp.ones(3, 1)

    def evaluated_root_q(root: int, q_vertex: int, z_q: sp.Matrix) -> sp.Expr:
        return (x_root.T * edge_block(edges, root, q_vertex) * z_q)[0]

    raw_p = sp.expand(
        evaluated_root_q(1, Q0, z_q0) * evaluated_root_q(2, Q1, z_q1)
        + evaluated_root_q(1, Q1, z_q1) * evaluated_root_q(2, Q0, z_q0)
    )
    assert raw_p == z_q0[1] * z_q1[0]
    h_polynomial = (z_q0.T * edge_block(edges, Q0, Q1) * z_q1)[0]
    ones_substitution = {symbol: 1 for symbol in (*z_q0, *z_q1)}
    assert raw_p.subs(ones_substitution) == 1
    assert h_polynomial.subs(ones_substitution) == 3

    h_matrix = edge_block(edges, Q0, Q1)
    a_blocks = {u: edge_block(edges, Q0, PORTS[u]) for u in range(4)}
    c_blocks = {u: edge_block(edges, Q1, PORTS[u]) for u in range(4)}
    b_blocks = {
        (u, v): edge_block(edges, PORTS[u], PORTS[v])
        for u, v in combinations(range(4), 2)
    }
    assert h_matrix == sp.eye(3)
    assert h_matrix.det() == 1
    assert_all_pair_responses_zero(h_matrix, a_blocks, c_blocks, b_blocks)

    q_u_vertices = (Q0, Q1) + PORTS
    for word in product(COLOURS, repeat=6):
        coefficient = sp.Integer(0)
        for matching in perfect_matchings(q_u_vertices):
            term = sp.Integer(1)
            for left, right in matching:
                term *= edge_block(edges, left, right)[
                    word[q_u_vertices.index(left)],
                    word[q_u_vertices.index(right)],
                ]
            coefficient += term
        assert coefficient == 0

    rho_0 = projection_matrix(0)
    rho_1 = projection_matrix(1)
    projected_h = rho_0 * h_matrix * rho_1.T
    expected_projected_h = sp.zeros(2)
    expected_projected_h[1, 1] = 1
    assert projected_h == expected_projected_h
    projected_lhs = (
        sp.Matrix(projected_h).reshape(4, 1)
        * sp.Matrix([pi_q.get(word, 0) for word in product(COLOURS, repeat=4)]).T
    )
    projected_rhs = projected_ghz_flattening(0, 1, (1, 1, 1))
    assert projected_lhs == projected_rhs
    return incidence, pi_q


def check_fixture_mixed_coefficient(
    edges: dict[tuple[int, int], sp.Matrix],
    incidence: dict[int, sp.Matrix],
    pi_q: Counter[tuple[int, ...]],
) -> None:
    outside_word = {
        Q0: 0,
        Q1: 0,
        PORTS[0]: 2,
        PORTS[1]: 2,
        PORTS[2]: 2,
        PORTS[3]: 2,
    }
    assert edge_block(edges, Q0, Q1)[0, 0] * pi_q[(2, 2, 2, 2)] == 1

    contracted_terms = {}
    for pair in combinations(OUTSIDE, 2):
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in pair)
        edge_coefficient = edge_block(edges, *pair)[
            outside_word[pair[0]], outside_word[pair[1]]
        ]
        pi_coefficient = permanent_coefficient(
            incidence,
            complement,
            {vertex: outside_word[vertex] for vertex in complement},
        )
        contracted_terms[pair] = sp.expand(edge_coefficient * pi_coefficient)
    assert contracted_terms[(Q0, Q1)] == 1
    assert all(
        coefficient == 0
        for pair, coefficient in contracted_terms.items()
        if pair != (Q0, Q1)
    )
    assert sum(contracted_terms.values(), sp.Integer(0)) == 1

    full_word = tuple(
        0 if vertex in ROOTS else outside_word[vertex] for vertex in ALL_VERTICES
    )
    graph_coefficient, nonzero_matchings = matching_coefficient(edges, full_word)
    assert len(tuple(perfect_matchings(ALL_VERTICES))) == 945
    assert graph_coefficient == 1
    assert len(nonzero_matchings) == 1
    matching, coefficient = nonzero_matchings[0]
    assert coefficient == 1
    assert (Q0, Q1) in matching
    assert set(matching) == {
        (0, PORTS[0]),
        (1, PORTS[1]),
        (2, PORTS[2]),
        (3, PORTS[3]),
        (Q0, Q1),
    }


def main() -> None:
    check_rank_three_and_realignment_identities()
    check_support_and_sign_normal_forms()
    check_top_response_is_derived()
    check_determinant_and_characteristic_controls()
    check_complete_target_projection()

    edges = fixture_edges()
    check_fixture_maximum_root(edges)
    incidence, pi_q = check_fixture_incidence_and_responses(edges)
    check_fixture_mixed_coefficient(edges, incidence, pi_q)

    print("four-root full-rank response-zero exact replay: PASS")
    print("  9 response slices and 16 Kronecker-rank controls checked")
    print("  81 singleton and 9 two-port sign normal forms checked")
    print("  determinant-divisor and characteristic-two controls checked")
    print("  all 9 same/opposite-colour target projections checked")
    print("  ten-vertex maximum-root boundary fixture checked over QQ")
    print("  Pi_Q=e_2^4, raw p=1, h=3, mixed coefficient=1")
    print("  bounded replay only; the written theorem is the general proof")


if __name__ == "__main__":
    main()
