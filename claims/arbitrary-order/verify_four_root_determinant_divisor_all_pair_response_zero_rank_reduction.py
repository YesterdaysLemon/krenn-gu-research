"""Focused exact replay for the four-root determinant-divisor reduction.

This primary verifier independently regenerates the labelled response and
complete-target bookkeeping and checks exact rational controls for the rank
two and rank one reductions.  It is deliberately bounded: the written
theorem supplies the arbitrary-point quotient, maximal-root, and case-cover
arguments.  Nothing here proves common-root permanent integrability, a legal
same-Q target selector, the strategic node, or the global Krenn--Gu
conjecture.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORT_VERTICES = tuple(range(6, 10))
PORTS = tuple(range(4))
OUTSIDE = (Q0, Q1) + PORT_VERTICES
ALL_VERTICES = ROOTS + OUTSIDE
OUTSIDE_PAIRS = tuple(combinations(OUTSIDE, 2))
PORT_PAIRS = tuple(combinations(PORTS, 2))
OUTSIDE_WORDS = tuple(product(COLOURS, repeat=6))
PORT_WORDS = tuple(product(COLOURS, repeat=4))

Word = tuple[int, ...]
Pair = tuple[int, int]
Companion = dict[Word, sp.Expr]


def basis(colour: int) -> sp.Matrix:
    """Return one ternary coordinate covector as a column."""

    return sp.eye(3)[:, colour]


def matrix_unit(
    row: int,
    column: int,
    coefficient: sp.Expr | int = 1,
) -> sp.Matrix:
    """Return one exact ternary matrix unit."""

    answer = sp.zeros(3)
    answer[row, column] = coefficient
    return answer


def zero_port_blocks() -> dict[int, sp.Matrix]:
    return {u: sp.zeros(3) for u in PORTS}


def zero_internal_blocks() -> dict[Pair, sp.Matrix]:
    return {pair: sp.zeros(3) for pair in PORT_PAIRS}


def response_flattening(
    h_matrix: sp.Matrix,
    a_u: sp.Matrix,
    c_u: sp.Matrix,
    a_v: sp.Matrix,
    c_v: sp.Matrix,
    b_uv: sp.Matrix,
) -> sp.Matrix:
    """Return ``Z_uv`` flattened across ``(q0,q1)|(u,v)``."""

    return sp.Matrix(
        9,
        9,
        lambda q_index, port_index: (
            h_matrix[q_index // 3, q_index % 3] * b_uv[port_index // 3, port_index % 3]
            + a_u[q_index // 3, port_index // 3] * c_v[q_index % 3, port_index % 3]
            + a_v[q_index // 3, port_index % 3] * c_u[q_index % 3, port_index // 3]
        ),
    )


def assert_all_pair_responses_zero(
    h_matrix: sp.Matrix,
    a_blocks: dict[int, sp.Matrix],
    c_blocks: dict[int, sp.Matrix],
    b_blocks: dict[Pair, sp.Matrix],
) -> None:
    """Check every coefficient of all six labelled pair responses."""

    for u, v in PORT_PAIRS:
        response = response_flattening(
            h_matrix,
            a_blocks[u],
            c_blocks[u],
            a_blocks[v],
            c_blocks[v],
            b_blocks[(u, v)],
        )
        assert all(sp.expand(entry) == 0 for entry in response)


def cross_realignment(
    a_u: sp.Matrix,
    c_v: sp.Matrix,
    a_v: sp.Matrix,
    c_u: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Realign the two cross terms across ``(q0,u)|(q1,v)``."""

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


def word_index(word: Word) -> int:
    index = 0
    for colour in word:
        index = 3 * index + colour
    return index


def pure_companion(colour: int, coefficient: sp.Expr | int = 1) -> Companion:
    return {(colour,) * 4: sp.sympify(coefficient)}


def edge_block(
    edges: dict[Pair, sp.Matrix],
    left: int,
    right: int,
) -> sp.Matrix:
    """Read an unoriented labelled edge in the requested slot order."""

    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


def contracted_pair_terms(
    edges: dict[Pair, sp.Matrix],
    companions: dict[Pair, Companion],
    word: Word,
) -> dict[Pair, sp.Expr]:
    """Generate all fifteen labelled terms of the contracted target."""

    assert len(word) == 6
    colours = dict(zip(OUTSIDE, word, strict=True))
    terms: dict[Pair, sp.Expr] = {}
    for pair in OUTSIDE_PAIRS:
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in pair)
        complement_word = tuple(colours[vertex] for vertex in complement)
        terms[pair] = sp.expand(
            edge_block(edges, *pair)[colours[pair[0]], colours[pair[1]]]
            * companions.get(pair, {}).get(complement_word, 0)
        )
    assert tuple(terms) == OUTSIDE_PAIRS
    return terms


def ghz_coefficient(word: Word, weights: tuple[int, int, int]) -> int:
    for colour, weight in enumerate(weights):
        if word == (colour,) * len(word):
            return weight
    return 0


def check_labelled_equation_generation() -> tuple[int, int, int]:
    """Regenerate the six responses and the complete 15-term target."""

    response_coefficients = 0
    for u, v in PORT_PAIRS:
        h_matrix = sp.Matrix(3, 3, sp.symbols(f"h_{u}{v}_0:9"))
        a_u = sp.Matrix(3, 3, sp.symbols(f"au_{u}{v}_0:9"))
        a_v = sp.Matrix(3, 3, sp.symbols(f"av_{u}{v}_0:9"))
        c_u = sp.Matrix(3, 3, sp.symbols(f"cu_{u}{v}_0:9"))
        c_v = sp.Matrix(3, 3, sp.symbols(f"cv_{u}{v}_0:9"))
        b_uv = sp.Matrix(3, 3, sp.symbols(f"b_{u}{v}_0:9"))
        flattened = response_flattening(h_matrix, a_u, c_u, a_v, c_v, b_uv)
        for q0_colour, q1_colour, u_colour, v_colour in product(
            COLOURS,
            repeat=4,
        ):
            expected = (
                h_matrix[q0_colour, q1_colour] * b_uv[u_colour, v_colour]
                + a_u[q0_colour, u_colour] * c_v[q1_colour, v_colour]
                + a_v[q0_colour, v_colour] * c_u[q1_colour, u_colour]
            )
            assert (
                flattened[
                    3 * q0_colour + q1_colour,
                    3 * u_colour + v_colour,
                ]
                == expected
            )
            response_coefficients += 1

    # One coordinate-monomial triangle supplies all three pure target terms.
    # Checking every permutation and active port exercises all labels rather
    # than only one displayed pure coefficient.
    complete_target_words = 0
    complete_target_terms = 0
    for i, j, k in permutations(COLOURS):
        for active_port in PORTS:
            active_vertex = PORT_VERTICES[active_port]
            edges = {
                (Q0, Q1): matrix_unit(k, k),
                tuple(sorted((Q0, active_vertex))): matrix_unit(i, i),
                tuple(sorted((Q1, active_vertex))): matrix_unit(j, j),
            }
            companions = {
                (Q0, Q1): pure_companion(k),
                tuple(sorted((Q0, active_vertex))): pure_companion(i),
                tuple(sorted((Q1, active_vertex))): pure_companion(j),
            }
            for word in OUTSIDE_WORDS:
                terms = contracted_pair_terms(edges, companions, word)
                assert len(terms) == 15
                assert sum(terms.values(), sp.Integer(0)) == ghz_coefficient(
                    word,
                    (1, 1, 1),
                )
                complete_target_words += 1
                complete_target_terms += len(terms)

    assert response_coefficients == 6 * 81 == 486
    assert complete_target_words == 6 * 4 * 729 == 17496
    assert complete_target_terms == complete_target_words * 15 == 262440
    return response_coefficients, complete_target_words, complete_target_terms


def check_quotient_cross_and_rank_controls() -> tuple[int, int, int]:
    """Check realignment ranks, support signs, and exact quotient fixtures."""

    realignment_ranks = 0
    for rank_a, rank_c in product(range(4), repeat=2):
        a_v = sp.diag(*([1] * rank_a + [0] * (3 - rank_a)))
        c_u = sp.diag(*([1] * rank_c + [0] * (3 - rank_c)))
        first, second = cross_realignment(sp.eye(3), sp.eye(3), a_v, c_u)
        assert first.rank() == 1
        assert second.rank() == rank_a * rank_c
        realignment_ranks += 1

    # The denominator-free characteristic-zero certificate for three active
    # quotient blocks.  It avoids choosing any ratio until an active chart is
    # declared.
    s0, s1, s2, t0, t1, t2 = sp.symbols("s0 s1 s2 t0 t1 t2")
    equation_01 = s0 * t1 + s1 * t0
    equation_02 = s0 * t2 + s2 * t0
    equation_12 = s1 * t2 + s2 * t1
    certificate = s2 * equation_01 + s1 * equation_02 - s0 * equation_12
    assert sp.expand(certificate - 2 * s1 * s2 * t0) == 0

    h_rank_two = sp.diag(1, 1, 0)
    pi = sp.Matrix([[0, 0, 1]])
    alpha_s = sp.Matrix([1, 2, -1])
    alpha_t = sp.Matrix([2, -1, 3])
    a_blocks = zero_port_blocks()
    c_blocks = zero_port_blocks()
    b_blocks = zero_internal_blocks()
    a_blocks[0] = basis(2) * alpha_s.T
    a_blocks[1] = basis(2) * alpha_t.T
    c_blocks[0] = 3 * basis(2) * alpha_s.T
    c_blocks[1] = -3 * basis(2) * alpha_t.T
    assert_all_pair_responses_zero(h_rank_two, a_blocks, c_blocks, b_blocks)
    assert pi * a_blocks[0] == alpha_s.T
    assert pi * a_blocks[1] == alpha_t.T
    assert pi * c_blocks[0] == 3 * alpha_s.T
    assert pi * c_blocks[1] == -3 * alpha_t.T

    # Enumerate every labelled support allowed by the sign equations.  A
    # singleton has no active-pair rank conclusion; a two-port support has
    # the opposite-sign normal form; support three or four is excluded by
    # the certificate above in characteristic zero.
    quotient_supports = tuple(
        subset for size in (1, 2) for subset in combinations(PORTS, size)
    )
    assert len(quotient_supports) == 10
    support_checks = 0
    for support in quotient_supports:
        rational_a = zero_port_blocks()
        rational_c = zero_port_blocks()
        if len(support) == 1:
            rational_a[support[0]] = matrix_unit(2, 0)
            rational_c[support[0]] = matrix_unit(2, 1)
        else:
            left, right = support
            rational_a[left] = matrix_unit(2, 0)
            rational_a[right] = matrix_unit(2, 1)
            rational_c[left] = 2 * matrix_unit(2, 0)
            rational_c[right] = -2 * matrix_unit(2, 1)
        assert_all_pair_responses_zero(
            h_rank_two,
            rational_a,
            rational_c,
            zero_internal_blocks(),
        )
        support_checks += 1

    assert realignment_ranks == 16
    assert support_checks == 10
    return realignment_ranks, support_checks, 1


def projection_killing(colour: int) -> sp.Matrix:
    retained = [entry for entry in COLOURS if entry != colour]
    return sp.Matrix(
        2,
        3,
        lambda row, column: int(column == retained[row]),
    )


def projected_ghz_flattening(
    killed_left: int,
    killed_right: int,
    weights: tuple[int, int, int] = (2, 3, 5),
) -> sp.Matrix:
    rho_left = projection_killing(killed_left)
    rho_right = projection_killing(killed_right)
    answer = sp.zeros(4, 81)
    for colour, weight in enumerate(weights):
        q_vector = sp.kronecker_product(
            rho_left * basis(colour),
            rho_right * basis(colour),
        )
        port_vector = sp.zeros(81, 1)
        port_vector[word_index((colour,) * 4)] = 1
        answer += weight * q_vector * port_vector.T
    return answer


def rank_two_with_avoided_lines(i: int, j: int) -> sp.Matrix:
    rows = [colour for colour in COLOURS if colour != i]
    columns = [colour for colour in COLOURS if colour != j]
    return sum(
        (
            basis(row) * basis(column).T
            for row, column in zip(rows, columns, strict=True)
        ),
        sp.zeros(3),
    )


def check_rank_two_escape_exclusions() -> tuple[int, int, int]:
    """Replay both projected-target contradictions and the singleton rank."""

    two_sided_projections = 0
    for i, j in product(COLOURS, repeat=2):
        h_matrix = rank_two_with_avoided_lines(i, j)
        rho_i = projection_killing(i)
        rho_j = projection_killing(j)
        projected_h = rho_i * h_matrix * rho_j.T
        target = projected_ghz_flattening(i, j)
        assert h_matrix.rank() == 2
        assert projected_h.rank() == 2
        if i == j:
            # H' tensor Pi_Q has Q|U flattening rank one, while the two
            # surviving GHZ colours have flattening rank two.
            assert target.rank() == 2
        else:
            # Only the third colour remains, whose Q factor has matrix rank
            # one; equality would make the rank-two H' proportional to it.
            assert target.rank() == 1
            surviving = next(colour for colour in COLOURS if colour not in (i, j))
            q_factor = sp.kronecker_product(
                rho_i * basis(surviving),
                rho_j * basis(surviving),
            ).reshape(2, 2)
            assert q_factor.rank() == 1
            assert projected_h.rank() != q_factor.rank()
        two_sided_projections += 1

    # On a singleton one-sided chart, realignment gives rank 2*rank(B) on
    # the H term and rank at most one on the cross term.  The exact rational
    # matrices below exercise every possible rank of B.
    singleton_realignments = 0
    h_rank_two = sp.diag(1, 1, 0)
    a_t = matrix_unit(0, 0)
    c_v = matrix_unit(0, 1)
    for rank_b in range(4):
        b_uv = sp.diag(*([1] * rank_b + [0] * (3 - rank_b)))
        h_term = sp.kronecker_product(h_rank_two, b_uv)
        cross, _ = cross_realignment(a_t, c_v, sp.zeros(3), sp.zeros(3))
        assert h_term.rank() == 2 * rank_b
        assert cross.rank() == 1
        if rank_b:
            assert h_term.rank() != cross.rank()
        singleton_realignments += 1

    regular_left = sp.Matrix([1, 1, 1])
    regular_right = sp.Matrix([1, -1, 1])
    assert (regular_left.T * h_rank_two * regular_right)[0] == 0
    assert all(entry != 0 for entry in (*regular_left, *regular_right))

    # In the two-port one-sided chart, pure i and pure j force the two local
    # coordinate labels to be i,j.  The all-k slice then asks a rank-two H to
    # equal a rank-one coordinate matrix.
    one_sided_slices = 0
    for i, j, k in permutations(COLOURS):
        h_matrix = basis(i) * basis(i).T + basis(k) * basis(k).T
        rho_i = projection_killing(i)
        rho_j = projection_killing(j)
        projected_h = rho_i * h_matrix * rho_j.T
        assert h_matrix.rank() == 2
        assert projected_h.rank() == 1
        assert projected_ghz_flattening(i, j).rank() == 1

        admissible_local_labels = {
            labels
            for labels in product(COLOURS, repeat=2)
            if i in labels and j in labels
        }
        assert admissible_local_labels == {(i, j), (j, i)}
        target_k_matrix = basis(k) * basis(k).T
        assert h_matrix.rank() == 2
        assert target_k_matrix.rank() == 1
        assert h_matrix != target_k_matrix
        one_sided_slices += 1

    assert two_sided_projections == 9
    assert singleton_realignments == 4
    assert one_sided_slices == 6
    return two_sided_projections, singleton_realignments, one_sided_slices


def rank_two_core_blocks() -> tuple[
    sp.Matrix,
    dict[int, sp.Matrix],
    dict[int, sp.Matrix],
    dict[Pair, sp.Matrix],
]:
    """Return the exact rank-two conformal-core sharp control."""

    h_matrix = sp.diag(1, 1, 0)
    a_blocks = zero_port_blocks()
    c_blocks = zero_port_blocks()
    b_blocks = zero_internal_blocks()
    a_blocks[0] = matrix_unit(0, 0)
    c_blocks[0] = matrix_unit(1, 0)
    a_blocks[1] = matrix_unit(1, 1)
    c_blocks[1] = matrix_unit(0, 1)
    b_blocks[(0, 1)] = -matrix_unit(0, 1)
    return h_matrix, a_blocks, c_blocks, b_blocks


def check_rank_two_conformal_core_and_q4() -> tuple[int, int, int]:
    """Check conformal recovery and both forms of the Q4 projection."""

    h_matrix, a_blocks, c_blocks, b_blocks = rank_two_core_blocks()
    assert_all_pair_responses_zero(h_matrix, a_blocks, c_blocks, b_blocks)
    assert h_matrix.rank() == 2
    assert any(block != sp.zeros(3) for block in a_blocks.values())
    assert any(block != sp.zeros(3) for block in c_blocks.values())

    conformal_cells = 0
    for u, v in PORT_PAIRS:
        for colour_u, colour_v in product(COLOURS, repeat=2):
            cross = (
                a_blocks[u][:, colour_u] * c_blocks[v][:, colour_v].T
                + a_blocks[v][:, colour_v] * c_blocks[u][:, colour_u].T
            )
            # theta_H reads the (0,0) coefficient and satisfies theta_H(H)=1.
            scalar = cross[0, 0]
            assert cross == scalar * h_matrix
            assert b_blocks[(u, v)][colour_u, colour_v] == -scalar
            conformal_cells += 1

    # Dense exact companions check that double projection of the full
    # fifteen-term contraction retains precisely the six physical U-U terms.
    edges: dict[Pair, sp.Matrix] = {(Q0, Q1): h_matrix}
    for u in PORTS:
        edges[(Q0, PORT_VERTICES[u])] = a_blocks[u]
        edges[(Q1, PORT_VERTICES[u])] = c_blocks[u]
    for (u, v), block in b_blocks.items():
        edges[(PORT_VERTICES[u], PORT_VERTICES[v])] = block

    companions: dict[Pair, Companion] = {}
    for pair_index, pair in enumerate(OUTSIDE_PAIRS):
        companions[pair] = {
            word: sp.Integer(
                1
                + pair_index
                + sum(
                    (position + 2) * (colour + 1)
                    for position, colour in enumerate(word)
                )
            )
            for word in PORT_WORDS
        }

    q4_dense_words = 0
    for port_word in PORT_WORDS:
        outside_word = (2, 2) + port_word
        full_terms = contracted_pair_terms(edges, companions, outside_word)
        internal_terms = sum(
            (full_terms[(PORT_VERTICES[u], PORT_VERTICES[v])] for u, v in PORT_PAIRS),
            sp.Integer(0),
        )
        assert sum(full_terms.values(), sp.Integer(0)) == internal_terms
        q4_dense_words += 1

    # A separate formal Q4 control realizes the nonzero projected colour-2
    # target with one U-U edge.  It is a quotient identity, not a response
    # point or a common-root permanent realization.
    q4_edges = {(PORT_VERTICES[0], PORT_VERTICES[1]): 7 * matrix_unit(2, 2)}
    q4_companions = {
        (PORT_VERTICES[0], PORT_VERTICES[1]): pure_companion(2),
    }
    q4_target_words = 0
    for port_word in PORT_WORDS:
        word = (2, 2) + port_word
        coefficient = sum(
            contracted_pair_terms(q4_edges, q4_companions, word).values(),
            sp.Integer(0),
        )
        assert coefficient == (7 if port_word == (2, 2, 2, 2) else 0)
        q4_target_words += 1

    assert conformal_cells == 6 * 9 == 54
    assert q4_dense_words == 81
    assert q4_target_words == 81
    return conformal_cells, q4_dense_words, q4_target_words


def beta_cross(
    a_vector: sp.Matrix,
    c_vector: sp.Matrix,
    other_a: sp.Matrix,
    other_c: sp.Matrix,
) -> sp.Matrix:
    """Return the rank-two conformal cross before quotienting by ``K H``."""

    return a_vector * other_c.T + other_a * c_vector.T


def scalar_mod_identity(matrix: sp.Matrix) -> bool:
    """Decide exact membership in the line spanned by the 2 by 2 identity."""

    return matrix[0, 1] == matrix[1, 0] == 0 and matrix[0, 0] == matrix[1, 1]


def check_mixed_vector_kernel_and_combined_support() -> tuple[int, int, int]:
    """Replay the beta-kernel charts and the exact two-support core control."""

    c1, c2, x, y, cap_x, cap_y = sp.symbols("c1 c2 x y X Y")
    first_a = sp.Matrix([1, 0])
    first_c = sp.Matrix([c1, c2])

    # On the c1-nonzero chart the kernel is one mixed line.  Its generator
    # is beta-orthogonal to w, while its self-cross cannot lie in K I_2
    # because its diagonal difference has the nonzero factor 2*c1.
    line_a = sp.Matrix([1, 0])
    line_c = sp.Matrix([-c1, -c2])
    assert beta_cross(first_a, first_c, line_a, line_c) == sp.zeros(2)
    self_cross = beta_cross(line_a, line_c, line_a, line_c)
    assert sp.expand(self_cross[0, 0] - self_cross[1, 1]) == -2 * c1
    assert self_cross[1, 0] == 0

    # On the c1=0 chart the full kernel has the displayed two-parameter
    # form.  Two kernel vectors are mutually beta-orthogonal precisely only
    # if the three characteristic-zero equations below hold.
    chart_c = sp.Matrix([0, c2])
    kernel_a = sp.Matrix([x, y])
    kernel_c = c2 * sp.Matrix([y, -x])
    assert scalar_mod_identity(beta_cross(first_a, chart_c, kernel_a, kernel_c))
    other_a = sp.Matrix([cap_x, cap_y])
    other_c = c2 * sp.Matrix([cap_y, -cap_x])
    mutual = beta_cross(kernel_a, kernel_c, other_a, other_c)
    assert sp.expand(mutual[0, 1]) == -2 * c2 * x * cap_x
    assert sp.expand(mutual[1, 0]) == 2 * c2 * y * cap_y
    assert (
        sp.expand(mutual[0, 0] - mutual[1, 1] - 2 * c2 * (x * cap_y + cap_x * y)) == 0
    )

    rational_kernel_pairs = 0
    nonzero_parameters = tuple(
        (left, right)
        for left, right in product(range(-2, 3), repeat=2)
        if (left, right) != (0, 0)
    )
    for left, right in product(nonzero_parameters, repeat=2):
        local_a = sp.Matrix(left)
        local_c = sp.Matrix([left[1], -left[0]])
        remote_a = sp.Matrix(right)
        remote_c = sp.Matrix([right[1], -right[0]])
        assert not scalar_mod_identity(beta_cross(local_a, local_c, remote_a, remote_c))
        rational_kernel_pairs += 1

    # The physical conformal-core fixture realizes exactly two nonzero W_u.
    # Each W_u is the column image of z -> (A_u(-,z),C_u(-,z)).
    _, a_blocks, c_blocks, _ = rank_two_core_blocks()
    combined_ranks = []
    left_projection_ranks = []
    right_projection_ranks = []
    combined_maps = []
    for u in PORTS:
        left_map = a_blocks[u][:2, :]
        right_map = c_blocks[u][:2, :]
        combined = sp.Matrix.vstack(left_map, right_map)
        combined_maps.append(combined)
        combined_ranks.append(combined.rank())
        left_projection_ranks.append(left_map.rank())
        right_projection_ranks.append(right_map.rank())
    assert combined_ranks == [1, 1, 0, 0]
    assert left_projection_ranks == combined_ranks
    assert right_projection_ranks == combined_ranks

    # Corollary 7.1 is sharp on the same control: each active combined map
    # has torus-free kernel and a fixed coordinate row in im(Phi_u^*), while
    # each inactive map has the whole local torus in its kernel.
    assert [kernel_torus_search(combined) for combined in combined_maps] == [
        False,
        False,
        True,
        True,
    ]
    assert [row_span_contains_coordinate(combined) for combined in combined_maps] == [
        True,
        True,
        False,
        False,
    ]

    assert rational_kernel_pairs == 24**2 == 576
    return rational_kernel_pairs, sum(rank != 0 for rank in combined_ranks), 2


def rational_projective_lines() -> tuple[sp.Matrix, ...]:
    """Return all projective lines represented over ``{-1,0,1}``."""

    representatives: list[sp.Matrix] = [sp.zeros(3, 1)]
    for entries in product((-1, 0, 1), repeat=3):
        if entries == (0, 0, 0):
            continue
        first_nonzero = next(entry for entry in entries if entry)
        if first_nonzero != 1:
            continue
        representatives.append(sp.Matrix(entries))
    assert len(representatives) == 14
    return tuple(representatives)


def row_span_contains_coordinate(rows: sp.Matrix) -> bool:
    rank = rows.rank()
    return any(rows.col_join(basis(colour).T).rank() == rank for colour in COLOURS)


def kernel_torus_search(rows: sp.Matrix) -> bool:
    """Find a torus vector using four exact coefficients per kernel basis."""

    kernel = rows.nullspace()
    if not kernel:
        return False
    for coefficients in product(range(4), repeat=len(kernel)):
        vector = sum(
            (
                coefficient * kernel_vector
                for coefficient, kernel_vector in zip(
                    coefficients,
                    kernel,
                    strict=True,
                )
            ),
            sp.zeros(3, 1),
        )
        if all(entry != 0 for entry in vector):
            return True
    return False


def check_moving_blocker_controls() -> tuple[int, int, int]:
    """Check the local torus criterion and sharp two-open-port fixture."""

    local_subspaces = 0
    lines = rational_projective_lines()
    for first, second in product(lines, repeat=2):
        rows = sp.Matrix.vstack(first.T, second.T)
        has_torus = kernel_torus_search(rows)
        contains_coordinate = row_span_contains_coordinate(rows)
        assert has_torus == (not contains_coordinate)
        local_subspaces += 1

    h_matrix, a_blocks, c_blocks, _ = rank_two_core_blocks()
    z0 = sp.Matrix([1, 1, 1])
    z1 = sp.Matrix([1, -1, 1])
    assert (z0.T * h_matrix * z1)[0] == 0
    assert (z0.T * h_matrix) != sp.zeros(1, 3)
    assert (z1.T * h_matrix.T) != sp.zeros(1, 3)
    open_ports = []
    for u in PORTS:
        a_u = a_blocks[u].T * z0
        c_u = c_blocks[u].T * z1
        rows = sp.Matrix.vstack(a_u.T, c_u.T)
        if kernel_torus_search(rows):
            open_ports.append(u)
    assert open_ports == [2, 3]

    # Three hypothetical open ports at one regular zero make all evaluated
    # residual factors collinear.  Their cross sum has rank one and cannot
    # be a nonzero scalar multiple of rank-two H.
    p_line = sp.Matrix([1, -1, 0])
    q_line = sp.Matrix([1, 1, 0])
    assert (z0.T * p_line)[0] == 0
    assert (z1.T * q_line)[0] == 0
    cross = p_line * q_line.T + p_line * q_line.T
    assert cross.rank() == 1
    blocker_scalar = sp.Symbol("blocker_scalar")
    equations = list(blocker_scalar * h_matrix + cross)
    assert sp.solve(equations, blocker_scalar, dict=True) == []

    assert local_subspaces == 14**2 == 196
    return local_subspaces, len(open_ports), cross.rank()


def wick_b_blocks(
    a_vectors: dict[int, sp.Matrix],
    c_vectors: dict[int, sp.Matrix],
) -> dict[Pair, sp.Matrix]:
    return {
        (u, v): -(a_vectors[u] * c_vectors[v].T + c_vectors[u] * a_vectors[v].T)
        for u, v in PORT_PAIRS
    }


def transpose_rank_one_data(
    a_blocks: dict[int, sp.Matrix],
    c_blocks: dict[int, sp.Matrix],
) -> tuple[dict[int, sp.Matrix], dict[int, sp.Matrix]]:
    return c_blocks, a_blocks


def check_rank_one_normal_forms() -> tuple[int, int]:
    """Check all 31 labelled response branches in the rank-one cover."""

    x = basis(0)
    y = basis(0)
    d = basis(1)
    escaping_left = basis(1)
    escaping_right = basis(2)
    h_matrix = x * y.T
    rational_lines = (
        sp.Matrix([1, 2, -1]),
        sp.Matrix([2, -1, 1]),
        sp.Matrix([-1, 1, 2]),
        sp.Matrix([1, -2, 2]),
    )

    branch_checks = 0
    response_coefficients = 0

    # Branch I: the double-contained Wick core.
    a_vectors = {u: rational_lines[u] for u in PORTS}
    c_vectors = {u: rational_lines[(u + 1) % 4] for u in PORTS}
    a_blocks = {u: x * a_vectors[u].T for u in PORTS}
    c_blocks = {u: y * c_vectors[u].T for u in PORTS}
    assert_all_pair_responses_zero(
        h_matrix,
        a_blocks,
        c_blocks,
        wick_b_blocks(a_vectors, c_vectors),
    )
    branch_checks += 1
    response_coefficients += 6 * 81

    # Branch IIa: every singleton one-sided support, and its transpose.
    for active in PORTS:
        local_a = {u: sp.zeros(3, 1) for u in PORTS}
        local_c = {u: rational_lines[(u + 1) % 4] for u in PORTS}
        local_a[active] = rational_lines[active]
        contained_a = {u: x * local_a[u].T for u in PORTS}
        escaping_c = {u: y * local_c[u].T for u in PORTS}
        escaping_c[active] += d * rational_lines[(active + 2) % 4].T
        b_blocks = wick_b_blocks(local_a, local_c)
        for left_blocks, right_blocks in (
            (contained_a, escaping_c),
            transpose_rank_one_data(contained_a, escaping_c),
        ):
            assert_all_pair_responses_zero(
                h_matrix,
                left_blocks,
                right_blocks,
                b_blocks,
            )
            branch_checks += 1
            response_coefficients += 6 * 81

    # Branch IIb: every two-port one-sided support, and its transpose.
    for left, right in PORT_PAIRS:
        local_a = {u: sp.zeros(3, 1) for u in PORTS}
        local_c = {u: rational_lines[(u + 1) % 4] for u in PORTS}
        local_a[left] = rational_lines[left]
        local_a[right] = rational_lines[right]
        contained_a = {u: x * local_a[u].T for u in PORTS}
        escaping_c = {u: y * local_c[u].T for u in PORTS}
        escaping_c[left] += d * local_a[left].T
        escaping_c[right] -= d * local_a[right].T
        b_blocks = wick_b_blocks(local_a, local_c)
        for left_blocks, right_blocks in (
            (contained_a, escaping_c),
            transpose_rank_one_data(contained_a, escaping_c),
        ):
            assert_all_pair_responses_zero(
                h_matrix,
                left_blocks,
                right_blocks,
                b_blocks,
            )
            branch_checks += 1
            response_coefficients += 6 * 81

    # Branch IIIa: every two-sided singleton support.
    for active in PORTS:
        left_blocks = zero_port_blocks()
        right_blocks = zero_port_blocks()
        left_blocks[active] = escaping_left * rational_lines[active].T
        right_blocks[active] = escaping_right * rational_lines[(active + 1) % 4].T
        assert_all_pair_responses_zero(
            h_matrix,
            left_blocks,
            right_blocks,
            zero_internal_blocks(),
        )
        branch_checks += 1
        response_coefficients += 6 * 81

    # Branch IIIb: every two-sided two-port support and opposite sign.
    for left, right in PORT_PAIRS:
        alpha_left = rational_lines[left]
        alpha_right = rational_lines[right]
        left_blocks = zero_port_blocks()
        right_blocks = zero_port_blocks()
        left_blocks[left] = escaping_left * alpha_left.T
        left_blocks[right] = escaping_left * alpha_right.T
        right_blocks[left] = 3 * escaping_right * alpha_left.T
        right_blocks[right] = -3 * escaping_right * alpha_right.T
        assert_all_pair_responses_zero(
            h_matrix,
            left_blocks,
            right_blocks,
            zero_internal_blocks(),
        )
        branch_checks += 1
        response_coefficients += 6 * 81

    assert branch_checks == 1 + 2 * 4 + 2 * 6 + 4 + 6 == 31
    assert response_coefficients == branch_checks * 6 * 81 == 15066
    return branch_checks, response_coefficients


def seventh_response_scalar_identity() -> sp.Expr:
    """Return the reduced denominator-free seventh-response difference."""

    h = sp.Symbol("h")
    a = sp.symbols("a0:4")
    c = sp.symbols("c0:4")
    response = {(u, v): -(a[u] * c[v] + a[v] * c[u]) for u, v in PORT_PAIRS}

    port_partitions = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    reduced_h_times_t = sum(
        (response[first] * response[second] for first, second in port_partitions),
        sp.Integer(0),
    )
    for u in PORTS:
        for v in PORTS:
            if u == v:
                continue
            complement = tuple(port for port in PORTS if port not in (u, v))
            pair = tuple(sorted(complement))
            reduced_h_times_t += a[u] * c[v] * response[pair]

    wick_sum = sum(
        (
            sp.prod(a[u] for u in subset)
            * sp.prod(c[v] for v in PORTS if v not in subset)
            for subset in combinations(PORTS, 2)
        ),
        sp.Integer(0),
    )
    difference = sp.expand(reduced_h_times_t + 2 * wick_sum)
    assert difference == 0

    # The unreduced matching expression really has 3+12=15 labelled terms.
    b_symbols = {pair: sp.Symbol(f"b{pair[0]}{pair[1]}") for pair in PORT_PAIRS}
    t_expression = h * sum(
        (b_symbols[first] * b_symbols[second] for first, second in port_partitions),
        sp.Integer(0),
    )
    t_expression += sum(
        (
            a[u]
            * c[v]
            * b_symbols[tuple(sorted(port for port in PORTS if port not in (u, v)))]
            for u in PORTS
            for v in PORTS
            if u != v
        ),
        sp.Integer(0),
    )
    assert len(sp.Add.make_args(sp.expand(t_expression))) == 15
    return difference


def matching_tensor_coefficient(
    h_matrix: sp.Matrix,
    a_blocks: dict[int, sp.Matrix],
    c_blocks: dict[int, sp.Matrix],
    b_blocks: dict[Pair, sp.Matrix],
    word: Word,
) -> sp.Expr:
    """Evaluate the 15 six-vertex perfect matchings exactly."""

    assert len(word) == 6
    local_edges: dict[Pair, sp.Matrix] = {(0, 1): h_matrix}
    for u in PORTS:
        local_edges[(0, u + 2)] = a_blocks[u]
        local_edges[(1, u + 2)] = c_blocks[u]
    for (u, v), block in b_blocks.items():
        local_edges[(u + 2, v + 2)] = block

    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(range(6))):
        term = sp.Integer(1)
        for left, right in matching:
            term *= local_edges.get((left, right), sp.zeros(3))[
                word[left],
                word[right],
            ]
        total += term
    return sp.expand(total)


def check_seventh_response_identity_and_independence() -> tuple[int, int]:
    """Check the polynomial identity and a nonzero rank-one top response."""

    seventh_response_scalar_identity()

    h_matrix = matrix_unit(0, 0)
    a_vectors = {u: basis(0) for u in PORTS}
    c_vectors = {u: basis(1) for u in PORTS}
    a_blocks = {u: basis(0) * a_vectors[u].T for u in PORTS}
    c_blocks = {u: basis(0) * c_vectors[u].T for u in PORTS}
    b_blocks = wick_b_blocks(a_vectors, c_vectors)
    assert_all_pair_responses_zero(h_matrix, a_blocks, c_blocks, b_blocks)

    top_coefficients = {}
    for subset in combinations(PORTS, 2):
        port_word = tuple(0 if u in subset else 1 for u in PORTS)
        word = (0, 0) + port_word
        top_coefficients[subset] = matching_tensor_coefficient(
            h_matrix,
            a_blocks,
            c_blocks,
            b_blocks,
            word,
        )
    assert set(top_coefficients.values()) == {-2}
    return 1, len(top_coefficients)


def fixture_root_edges() -> dict[Pair, sp.Matrix]:
    """Build the ten-vertex root incidence shared by both physical controls."""

    edges: dict[Pair, sp.Matrix] = {}

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
        add(root, PORT_VERTICES[port], matrix_unit(0, port_colour))

    root_q_entries = (
        (0, Q0, 0),
        (1, Q0, 1),
        (2, Q1, 0),
        (0, Q1, 1),
    )
    for root, q_vertex, q_colour in root_q_entries:
        add(root, q_vertex, matrix_unit(0, q_colour))
    return edges


def physical_control_edges(rank: int) -> dict[Pair, sp.Matrix]:
    edges = fixture_root_edges()
    if rank == 2:
        h_matrix, a_blocks, c_blocks, b_blocks = rank_two_core_blocks()
    elif rank == 1:
        h_matrix = matrix_unit(0, 0)
        a_blocks = zero_port_blocks()
        c_blocks = zero_port_blocks()
        a_blocks[0] = matrix_unit(0, 0)
        c_blocks[0] = matrix_unit(0, 1)
        a_blocks[1] = matrix_unit(0, 1)
        c_blocks[1] = matrix_unit(0, 0)
        b_blocks = zero_internal_blocks()
        b_blocks[(0, 1)] = -(matrix_unit(0, 0) + matrix_unit(1, 1))
    else:
        raise AssertionError(f"unsupported control rank: {rank}")

    edges[(Q0, Q1)] = h_matrix
    for u in PORTS:
        if a_blocks[u] != sp.zeros(3):
            edges[(Q0, PORT_VERTICES[u])] = a_blocks[u]
        if c_blocks[u] != sp.zeros(3):
            edges[(Q1, PORT_VERTICES[u])] = c_blocks[u]
    for (u, v), block in b_blocks.items():
        if block != sp.zeros(3):
            edges[(PORT_VERTICES[u], PORT_VERTICES[v])] = block
    return edges


def root_incidence_matrix(
    edges: dict[Pair, sp.Matrix],
    outside_vertex: int,
) -> sp.Matrix:
    root_vector = sp.ones(3, 1)
    return sp.Matrix(
        4,
        3,
        lambda root, colour: (root_vector.T * edge_block(edges, root, outside_vertex))[
            0, colour
        ],
    )


def permanent4(columns: tuple[tuple[int, ...], ...]) -> int:
    return sum(
        columns[0][assignment[0]]
        * columns[1][assignment[1]]
        * columns[2][assignment[2]]
        * columns[3][assignment[3]]
        for assignment in permutations(ROOTS)
    )


def complementary_permanent(
    incidence: dict[int, sp.Matrix],
    complement: tuple[int, ...],
) -> Companion:
    answer: Companion = {}
    for word in PORT_WORDS:
        columns = tuple(
            tuple(int(entry) for entry in incidence[vertex][:, colour])
            for vertex, colour in zip(complement, word, strict=True)
        )
        coefficient = permanent4(columns)
        if coefficient:
            answer[word] = sp.Integer(coefficient)
    return answer


def fixture_companions(
    incidence: dict[int, sp.Matrix],
) -> dict[Pair, Companion]:
    return {
        pair: complementary_permanent(
            incidence,
            tuple(vertex for vertex in OUTSIDE if vertex not in pair),
        )
        for pair in OUTSIDE_PAIRS
    }


def fixture_maximum_root(edges: dict[Pair, sp.Matrix]) -> int:
    """Replay the coordinate-monomial independent-set bound."""

    monomial_edges = {
        pair
        for pair in combinations(ALL_VERTICES, 2)
        if sum(entry != 0 for entry in edge_block(edges, *pair)) == 1
    }
    maximum_size = 0
    for mask in range(1 << len(ALL_VERTICES)):
        subset = tuple(
            vertex for index, vertex in enumerate(ALL_VERTICES) if mask & (1 << index)
        )
        if all(pair not in monomial_edges for pair in combinations(subset, 2)):
            maximum_size = max(maximum_size, len(subset))
    assert maximum_size == 4
    return maximum_size


def raw_incidence_value(edges: dict[Pair, sp.Matrix]) -> sp.Expr:
    z_q0 = sp.Matrix(sp.symbols("z_q0_0:3"))
    z_q1 = sp.Matrix(sp.symbols("z_q1_0:3"))
    root_vector = sp.ones(3, 1)

    def evaluated(root: int, q_vertex: int, vector: sp.Matrix) -> sp.Expr:
        return (root_vector.T * edge_block(edges, root, q_vertex) * vector)[0]

    raw = sp.expand(
        evaluated(1, Q0, z_q0) * evaluated(2, Q1, z_q1)
        + evaluated(1, Q1, z_q1) * evaluated(2, Q0, z_q0)
    )
    return raw.subs({symbol: 1 for symbol in (*z_q0, *z_q1)})


def full_matching_coefficient(
    edges: dict[Pair, sp.Matrix],
    word: Word,
    matchings: tuple[tuple[Pair, ...], ...],
) -> sp.Expr:
    total = sp.Integer(0)
    for matching in matchings:
        term = sp.Integer(1)
        for left, right in matching:
            coefficient = edge_block(edges, left, right)[word[left], word[right]]
            if coefficient == 0:
                term = sp.Integer(0)
                break
            term *= coefficient
        total += term
    return sp.expand(total)


def check_physical_sharpness_controls() -> tuple[int, int, int]:
    """Check both exact maximum-root controls and their target defect."""

    control_count = 0
    complete_decompositions = 0
    mixed_defects = 0
    matchings = tuple(perfect_matchings(ALL_VERTICES))
    assert len(matchings) == 945

    for rank in (2, 1):
        edges = physical_control_edges(rank)
        assert fixture_maximum_root(edges) == 4
        incidence = {vertex: root_incidence_matrix(edges, vertex) for vertex in OUTSIDE}
        assert tuple(
            incidence[vertex].rank() for vertex in PORT_VERTICES + (Q0, Q1)
        ) == (
            3,
            3,
            2,
            1,
            2,
            2,
        )
        assert sum(3 - incidence[vertex].rank() for vertex in OUTSIDE) == 5
        companions = fixture_companions(incidence)
        assert companions[(Q0, Q1)] == {(2, 2, 2, 2): 1}
        assert raw_incidence_value(edges) == 1

        h_matrix = edge_block(edges, Q0, Q1)
        a_blocks = {u: edge_block(edges, Q0, PORT_VERTICES[u]) for u in PORTS}
        c_blocks = {u: edge_block(edges, Q1, PORT_VERTICES[u]) for u in PORTS}
        b_blocks = {
            (u, v): edge_block(edges, PORT_VERTICES[u], PORT_VERTICES[v])
            for u, v in PORT_PAIRS
        }
        assert h_matrix.rank() == rank
        assert_all_pair_responses_zero(h_matrix, a_blocks, c_blocks, b_blocks)
        assert (sp.ones(1, 3) * h_matrix * sp.ones(3, 1))[0] == rank

        # The contracted 15-term identity is independently matched against
        # all 945 ten-vertex matchings at every one of the 729 outside words.
        for outside_word in OUTSIDE_WORDS:
            contracted = sum(
                contracted_pair_terms(edges, companions, outside_word).values(),
                sp.Integer(0),
            )
            full_word = (0, 0, 0, 0) + outside_word
            assert contracted == full_matching_coefficient(edges, full_word, matchings)
            complete_decompositions += 1

        mixed_word = (0, 0, 2, 2, 2, 2)
        mixed_terms = contracted_pair_terms(edges, companions, mixed_word)
        assert mixed_terms[(Q0, Q1)] == 1
        assert all(
            coefficient == 0
            for pair, coefficient in mixed_terms.items()
            if pair != (Q0, Q1)
        )
        assert sum(mixed_terms.values(), sp.Integer(0)) == 1
        assert ghz_coefficient(mixed_word, (1, 1, 1)) == 0
        mixed_defects += 1
        control_count += 1

    assert control_count == 2
    assert complete_decompositions == 2 * 729 == 1458
    assert mixed_defects == 2
    return control_count, complete_decompositions, mixed_defects


def check_rank_zero_and_saturation_controls() -> tuple[int, int]:
    """Record the selected-pair and denominator-free proof boundaries."""

    h_zero = sp.zeros(3)
    h_rank_one = matrix_unit(0, 0)
    h_rank_two = sp.diag(1, 1, 0)
    assert h_zero.rank() == 0
    assert h_rank_one.rank() == 1
    assert h_rank_two.rank() == 2
    assert h_rank_one.det() == h_rank_two.det() == 0
    assert h_rank_one != sp.zeros(3) and h_rank_two != sp.zeros(3)

    # Rank zero is excluded only by GLS4 activity for the same selected pair:
    # H tensor Pi is nonzero exactly when both factors are nonzero over QQ.
    nonzero_pi = sp.zeros(81, 1)
    nonzero_pi[word_index((2, 2, 2, 2))] = 1
    assert sp.kronecker_product(h_zero, nonzero_pi) == sp.zeros(243, 3)
    assert sp.kronecker_product(h_rank_one, nonzero_pi) != sp.zeros(243, 3)

    # No response contraction h, raw p, selector, nuisance, or target-module
    # denominator is inverted anywhere in this replay.
    return 3, 0


def main() -> None:
    response_coefficients, target_words, target_terms = (
        check_labelled_equation_generation()
    )
    realignment_ranks, quotient_supports, sign_certificates = (
        check_quotient_cross_and_rank_controls()
    )
    two_sided, singleton, one_sided = check_rank_two_escape_exclusions()
    conformal_cells, q4_dense, q4_target = check_rank_two_conformal_core_and_q4()
    beta_pairs, combined_supports, beta_charts = (
        check_mixed_vector_kernel_and_combined_support()
    )
    blocker_subspaces, open_ports, blocker_rank = check_moving_blocker_controls()
    rank_one_branches, rank_one_coefficients = check_rank_one_normal_forms()
    seventh_identities, seventh_coefficients = (
        check_seventh_response_identity_and_independence()
    )
    physical_controls, decompositions, defects = check_physical_sharpness_controls()
    rank_strata, divisions = check_rank_zero_and_saturation_controls()

    print("four-root determinant-divisor exact replay: PASS")
    print(
        f"  {response_coefficients} labelled response coefficients; "
        f"{target_words} complete-target words and {target_terms} terms checked"
    )
    print(
        f"  {realignment_ranks} realignment ranks, {quotient_supports} "
        f"quotient supports, {sign_certificates} characteristic-zero sign certificate"
    )
    print(
        f"  rank-two escapes: {two_sided} two-sided projections, "
        f"{singleton} singleton ranks, {one_sided} one-sided target slices"
    )
    print(f"  {conformal_cells} conformal cells; Q4 words {q4_dense}+{q4_target}")
    print(
        f"  {beta_pairs} exact beta-kernel pairs, {beta_charts} symbolic charts, "
        f"combined nonzero supports={combined_supports}"
    )
    print(
        f"  {blocker_subspaces} exact local subspaces; sharp open ports={open_ports}; "
        f"three-open cross rank={blocker_rank}"
    )
    print(
        f"  {rank_one_branches} exhaustive labelled rank-one branches and "
        f"{rank_one_coefficients} response coefficients checked"
    )
    print(
        f"  {seventh_identities} denominator-free seventh identity; "
        f"{seventh_coefficients} nonzero Wick coefficients"
    )
    print(
        f"  {physical_controls} physical controls, {decompositions} full matching "
        f"decompositions, {defects} exact mixed-target defects"
    )
    print(f"  {rank_strata} determinant strata; silent divisions={divisions}")
    print("  formal monomial triangles satisfy all 729 target coefficients")
    print("  bounded replay only; arbitrary-point conclusions are in the theorem")
    print("  strategic node and global Krenn--Gu conjecture remain OPEN/UNRESOLVED")


if __name__ == "__main__":
    main()
