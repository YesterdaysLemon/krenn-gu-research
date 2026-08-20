"""Focused exact replay for the determinant-divisor follow-up exclusions.

The written theorem proves the arbitrary-point rank-two support cover and the
rank-one common-incidence contradiction.  This bounded primary verifier
regenerates their labelled tensor bookkeeping over ``QQ``/SymPy: all target
words, all six active-pair quotients, every Gamma/dimension profile, the
full-plane beta equations, the column splice, and the committed ``P_4``
subrank interface.  It is not an independent audit, a selector theorem, or a
global Krenn--Gu result.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
Q0, Q1, S, T, M, N = tuple(range(6))
OUTSIDE = (Q0, Q1, S, T, M, N)
ACTIVE = (Q0, Q1, S, T)
INACTIVE = (M, N)
ALL_PAIRS = tuple(combinations(OUTSIDE, 2))
ACTIVE_PAIRS = tuple(combinations(ACTIVE, 2))
WORDS_6 = tuple(product(COLOURS, repeat=6))
WORDS_4 = tuple(product(COLOURS, repeat=4))
P4_PERMUTATIONS = tuple(permutations(range(4)))

Pair = tuple[int, int]
Word = tuple[int, ...]
Companion = dict[Word, sp.Expr]


@dataclass(frozen=True)
class SupportChart:
    """One exact incident coefficient space and its quotient map."""

    dimension: int
    basis_matrix: sp.Matrix
    quotient_matrix: sp.Matrix
    gamma: frozenset[int]
    label: str


def basis(colour: int) -> sp.Matrix:
    return sp.eye(3)[:, colour]


def matrix_unit(
    row: int,
    column: int,
    coefficient: sp.Expr | int = 1,
) -> sp.Matrix:
    answer = sp.zeros(3)
    answer[row, column] = coefficient
    return answer


def word_index(word: Word) -> int:
    index = 0
    for colour in word:
        index = 3 * index + colour
    return index


def edge_block(
    edges: dict[Pair, sp.Matrix],
    left: int,
    right: int,
) -> sp.Matrix:
    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


def pure_companion(colour: int, coefficient: sp.Expr | int = 1) -> Companion:
    return {(colour,) * 4: sp.sympify(coefficient)}


def contracted_pair_terms(
    edges: dict[Pair, sp.Matrix],
    companions: dict[Pair, Companion],
    word: Word,
) -> dict[Pair, sp.Expr]:
    """Return all fifteen labelled terms of the six-slot contraction."""

    assert len(word) == 6
    colours = dict(zip(OUTSIDE, word, strict=True))
    terms: dict[Pair, sp.Expr] = {}
    for pair in ALL_PAIRS:
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in pair)
        complement_word = tuple(colours[vertex] for vertex in complement)
        terms[pair] = sp.expand(
            edge_block(edges, *pair)[colours[pair[0]], colours[pair[1]]]
            * companions.get(pair, {}).get(complement_word, 0)
        )
    assert tuple(terms) == ALL_PAIRS
    return terms


def ghz_coefficient(word: Word, weights: tuple[sp.Expr, sp.Expr, sp.Expr]) -> sp.Expr:
    for colour, weight in enumerate(weights):
        if word == (colour,) * len(word):
            return weight
    return sp.Integer(0)


def check_formal_triangle_complete_target() -> tuple[int, int, int]:
    """Reconstruct all 729 coefficients of the independent-companion control."""

    checked_words = 0
    checked_terms = 0
    checked_responses = 0
    edge_scalars = (sp.Integer(2), sp.Integer(3), sp.Integer(5))
    target_scalars = (sp.Integer(7), sp.Integer(11), sp.Integer(13))
    triangle_port = S

    for i, j, k in permutations(COLOURS):
        alpha, beta, gamma = edge_scalars
        weights = [sp.Integer(0)] * 3
        weights[i], weights[j], weights[k] = target_scalars
        edges = {
            (Q0, Q1): gamma * matrix_unit(k, k),
            (Q0, triangle_port): alpha * matrix_unit(i, i),
            (Q1, triangle_port): beta * matrix_unit(j, j),
        }
        companions = {
            (Q0, Q1): pure_companion(k, weights[k] / gamma),
            (Q0, triangle_port): pure_companion(i, weights[i] / alpha),
            (Q1, triangle_port): pure_companion(j, weights[j] / beta),
        }
        h_block = edge_block(edges, Q0, Q1)
        a_blocks = {port: edge_block(edges, Q0, port) for port in ACTIVE[2:] + INACTIVE}
        c_blocks = {port: edge_block(edges, Q1, port) for port in ACTIVE[2:] + INACTIVE}
        for left_port, right_port in combinations(ACTIVE[2:] + INACTIVE, 2):
            b_block = edge_block(edges, left_port, right_port)
            for q0_colour, q1_colour, left_colour, right_colour in product(
                COLOURS,
                repeat=4,
            ):
                response = (
                    h_block[q0_colour, q1_colour] * b_block[left_colour, right_colour]
                    + a_blocks[left_port][q0_colour, left_colour]
                    * c_blocks[right_port][q1_colour, right_colour]
                    + a_blocks[right_port][q0_colour, right_colour]
                    * c_blocks[left_port][q1_colour, left_colour]
                )
                assert sp.expand(response) == 0
                checked_responses += 1
        for word in WORDS_6:
            terms = contracted_pair_terms(edges, companions, word)
            assert len(terms) == 15
            assert sum(terms.values(), sp.Integer(0)) == ghz_coefficient(
                word,
                tuple(weights),
            )
            checked_words += 1
            checked_terms += len(terms)

    assert checked_words == 6 * 729 == 4374
    assert checked_terms == checked_words * 15 == 65610
    assert checked_responses == 6 * 6 * 81 == 2916
    return checked_words, checked_terms, checked_responses


def actual_gamma(space_basis: sp.Matrix) -> frozenset[int]:
    rank = space_basis.rank()
    return frozenset(
        colour
        for colour in COLOURS
        if space_basis.row_join(basis(colour)).rank() == rank
    )


def support_chart(dimension: int, gamma: frozenset[int]) -> SupportChart:
    """Construct exact representatives for every Gamma type used below."""

    if dimension == 1 and len(gamma) == 1:
        colour = next(iter(gamma))
        space_basis = basis(colour)
        retained = [entry for entry in COLOURS if entry != colour]
        quotient = sp.Matrix(
            2,
            3,
            lambda row, column: int(column == retained[row]),
        )
        label = f"coordinate-line-{colour}"
    elif dimension == 1 and not gamma:
        space_basis = sp.Matrix([1, 1, 1])
        quotient = sp.Matrix([[1, -1, 0], [1, 0, -1]])
        label = "noncoordinate-line"
    elif dimension == 2 and len(gamma) == 2:
        ordered = sorted(gamma)
        space_basis = sp.Matrix.hstack(*(basis(colour) for colour in ordered))
        missing = next(colour for colour in COLOURS if colour not in gamma)
        quotient = basis(missing).T
        label = f"coordinate-plane-{ordered[0]}{ordered[1]}"
    elif dimension == 2 and len(gamma) == 1:
        colour = next(iter(gamma))
        other = [entry for entry in COLOURS if entry != colour]
        space_basis = sp.Matrix.hstack(
            basis(colour),
            basis(other[0]) + basis(other[1]),
        )
        quotient = (basis(other[0]) - basis(other[1])).T
        label = f"noncoordinate-plane-with-{colour}"
    elif dimension == 2 and not gamma:
        space_basis = sp.Matrix.hstack(
            sp.Matrix([1, 0, -1]),
            sp.Matrix([0, 1, -1]),
        )
        quotient = sp.Matrix([[1, 1, 1]])
        label = "noncoordinate-plane-with-no-coordinate-axis"
    else:
        raise AssertionError(f"unsupported chart: dimension={dimension}, Gamma={gamma}")

    assert space_basis.shape == (3, dimension)
    assert space_basis.rank() == dimension
    assert quotient.shape == (3 - dimension, 3)
    assert quotient.rank() == 3 - dimension
    assert quotient * space_basis == sp.zeros(3 - dimension, dimension)
    assert actual_gamma(space_basis) == gamma
    return SupportChart(dimension, space_basis, quotient, gamma, label)


def quotient_chart_catalogue() -> tuple[SupportChart, ...]:
    charts = [support_chart(1, frozenset())]
    charts.extend(support_chart(1, frozenset({colour})) for colour in COLOURS)
    charts.append(support_chart(2, frozenset()))
    charts.extend(support_chart(2, frozenset({colour})) for colour in COLOURS)
    charts.extend(
        support_chart(2, frozenset(pair)) for pair in combinations(COLOURS, 2)
    )
    assert len(charts) == 11
    return tuple(charts)


def dense_companion(pair_index: int) -> Companion:
    return {
        word: sp.Integer(
            1
            + 7 * pair_index
            + sum((position + 2) * (colour + 1) for position, colour in enumerate(word))
        )
        for word in WORDS_4
    }


def supported_edge(
    left: SupportChart,
    right: SupportChart,
    pair_index: int,
) -> sp.Matrix:
    coupling = sp.Matrix(
        left.dimension,
        right.dimension,
        lambda row, column: sp.Integer(1 + pair_index + 2 * row - column),
    )
    return left.basis_matrix * coupling * right.basis_matrix.T


def rank_two_quotient_fixture() -> tuple[
    dict[int, SupportChart],
    dict[Pair, sp.Matrix],
    dict[Pair, Companion],
]:
    """Build one dense supported active K4 with noncoordinate support planes."""

    charts = {
        Q0: support_chart(2, frozenset({0})),
        Q1: support_chart(2, frozenset({1, 2})),
        S: support_chart(2, frozenset({0, 2})),
        T: support_chart(2, frozenset({1})),
    }
    edges = {
        pair: supported_edge(charts[pair[0]], charts[pair[1]], pair_index)
        for pair_index, pair in enumerate(ACTIVE_PAIRS)
    }
    companions = {
        pair: dense_companion(pair_index)
        for pair_index, pair in enumerate(ACTIVE_PAIRS)
    }
    return charts, edges, companions


def projected_labelled_coefficients(
    charts: dict[int, SupportChart],
    edges: dict[Pair, sp.Matrix],
    companions: dict[Pair, Companion],
    quotient_pair: Pair,
    quotient_indices: tuple[int, int],
    remaining_colours: dict[int, int],
) -> dict[Pair, sp.Expr]:
    left, right = quotient_pair
    rho_left = charts[left].quotient_matrix
    rho_right = charts[right].quotient_matrix
    totals = {pair: sp.Integer(0) for pair in ALL_PAIRS}
    for left_colour, right_colour in product(COLOURS, repeat=2):
        colours = dict(remaining_colours)
        colours[left] = left_colour
        colours[right] = right_colour
        word = tuple(colours[vertex] for vertex in OUTSIDE)
        weight = (
            rho_left[quotient_indices[0], left_colour]
            * rho_right[quotient_indices[1], right_colour]
        )
        terms = contracted_pair_terms(edges, companions, word)
        for pair, term in terms.items():
            totals[pair] += weight * term
    return {pair: sp.expand(term) for pair, term in totals.items()}


def projected_complementary_edge_coefficient(
    charts: dict[int, SupportChart],
    edges: dict[Pair, sp.Matrix],
    companions: dict[Pair, Companion],
    quotient_pair: Pair,
    quotient_indices: tuple[int, int],
    remaining_colours: dict[int, int],
) -> sp.Expr:
    complement_pair = tuple(vertex for vertex in ACTIVE if vertex not in quotient_pair)
    assert len(complement_pair) == 2
    edge_coefficient = edge_block(edges, *complement_pair)[
        remaining_colours[complement_pair[0]],
        remaining_colours[complement_pair[1]],
    ]
    complement_slots = tuple(
        vertex for vertex in OUTSIDE if vertex not in complement_pair
    )
    left, right = quotient_pair
    rho_left = charts[left].quotient_matrix
    rho_right = charts[right].quotient_matrix
    projected_companion = sp.Integer(0)
    for left_colour, right_colour in product(COLOURS, repeat=2):
        colours = dict(remaining_colours)
        colours[left] = left_colour
        colours[right] = right_colour
        companion_word = tuple(colours[vertex] for vertex in complement_slots)
        projected_companion += (
            rho_left[quotient_indices[0], left_colour]
            * rho_right[quotient_indices[1], right_colour]
            * companions[complement_pair][companion_word]
        )
    return sp.expand(edge_coefficient * projected_companion)


def check_labelled_sole_complementary_edge_survival() -> tuple[int, int]:
    """Check all words and all six exact two-slot quotient projections."""

    charts, edges, companions = rank_two_quotient_fixture()
    target_words = 0
    for word in WORDS_6:
        terms = contracted_pair_terms(edges, companions, word)
        assert all(terms[pair] == 0 for pair in ALL_PAIRS if pair not in ACTIVE_PAIRS)
        assert sum(terms.values(), sp.Integer(0)) == sum(
            (terms[pair] for pair in ACTIVE_PAIRS),
            sp.Integer(0),
        )
        target_words += 1

    quotient_coefficients = 0
    for quotient_pair in ACTIVE_PAIRS:
        remaining_vertices = tuple(
            vertex for vertex in OUTSIDE if vertex not in quotient_pair
        )
        quotient_ranges = (
            range(3 - charts[quotient_pair[0]].dimension),
            range(3 - charts[quotient_pair[1]].dimension),
        )
        for quotient_indices in product(*quotient_ranges):
            for remaining_word in WORDS_4:
                remaining_colours = dict(
                    zip(remaining_vertices, remaining_word, strict=True)
                )
                labelled_projection = projected_labelled_coefficients(
                    charts,
                    edges,
                    companions,
                    quotient_pair,
                    quotient_indices,
                    remaining_colours,
                )
                sole_edge = projected_complementary_edge_coefficient(
                    charts,
                    edges,
                    companions,
                    quotient_pair,
                    quotient_indices,
                    remaining_colours,
                )
                complement_pair = tuple(
                    vertex for vertex in ACTIVE if vertex not in quotient_pair
                )
                assert labelled_projection[complement_pair] == sole_edge
                assert all(
                    coefficient == 0
                    for pair, coefficient in labelled_projection.items()
                    if pair != complement_pair
                )
                assert (
                    sum(
                        labelled_projection.values(),
                        sp.Integer(0),
                    )
                    == sole_edge
                )
                quotient_coefficients += 1

    assert target_words == 729
    assert quotient_coefficients == 6 * 81 == 486
    return target_words, quotient_coefficients


def projected_ghz_flattening(
    left: SupportChart,
    right: SupportChart,
    weights: tuple[int, int, int] = (2, 3, 5),
) -> sp.Matrix:
    """Flatten projected GHZ across the unprojected active pair."""

    quotient_dimension = (3 - left.dimension) * (3 - right.dimension)
    answer = sp.zeros(9, quotient_dimension * 9)
    for colour, weight in enumerate(weights):
        active_vector = sp.kronecker_product(basis(colour), basis(colour))
        opposite_vector = sp.kronecker_product(
            left.quotient_matrix * basis(colour),
            right.quotient_matrix * basis(colour),
            basis(colour),
            basis(colour),
        )
        answer += weight * active_vector * opposite_vector.T
    return answer


def check_projected_rhs_rank_with_noncoordinate_charts() -> tuple[int, int]:
    """Verify rank equals N even when quotient classes are proportional."""

    charts = quotient_chart_catalogue()
    rank_checks = 0
    noncoordinate_checks = 0
    for left, right in product(charts, repeat=2):
        flattening = projected_ghz_flattening(left, right)
        surviving = set(COLOURS) - set(left.gamma | right.gamma)
        assert flattening.rank() == len(surviving)
        rank_checks += 1
        if "noncoordinate" in left.label or "noncoordinate" in right.label:
            noncoordinate_checks += 1

    assert rank_checks == 11**2 == 121
    assert noncoordinate_checks > 0
    return rank_checks, noncoordinate_checks


def gamma_subsets_for_dimension(dimension: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(subset)
        for size in range(dimension + 1)
        for subset in combinations(COLOURS, size)
    )


def profile_survivors(d_s: int, d_t: int) -> tuple[int, int]:
    """Exhaust Gamma data under precisely the six quotient rank rules."""

    q_sets = gamma_subsets_for_dimension(2)
    s_sets = gamma_subsets_for_dimension(d_s)
    t_sets = gamma_subsets_for_dimension(d_t)
    known_ranks: dict[Pair, int] = {
        (Q0, Q1): 2,
        (Q0, S): d_s,
        (Q1, S): d_s,
        (Q0, T): d_t,
        (Q1, T): d_t,
    }
    if d_s == d_t == 2:
        # This is the independently replayed full-plane beta consequence.
        known_ranks[(S, T)] = 2

    total = 0
    survivors = 0
    colour_set = set(COLOURS)
    for gamma_q0, gamma_q1, gamma_s, gamma_t in product(
        q_sets,
        q_sets,
        s_sets,
        t_sets,
    ):
        total += 1
        gamma = {
            Q0: gamma_q0,
            Q1: gamma_q1,
            S: gamma_s,
            T: gamma_t,
        }
        allowed = True
        for physical_pair, edge_rank in known_ranks.items():
            quotient_pair = tuple(
                vertex for vertex in ACTIVE if vertex not in physical_pair
            )
            surviving = colour_set - set(
                gamma[quotient_pair[0]] | gamma[quotient_pair[1]]
            )
            survivor_count = len(surviving)
            if survivor_count >= 2:
                allowed = False
                break
            if edge_rank == 2 and survivor_count != 0:
                allowed = False
                break
            if edge_rank == 1 and survivor_count == 1:
                colour = next(iter(surviving))
                # Lemma 2 makes the complementary rank-one edge the c,c
                # matrix unit, so both of its shores must contain e_c.
                if colour not in gamma[physical_pair[0]]:
                    allowed = False
                    break
                if colour not in gamma[physical_pair[1]]:
                    allowed = False
                    break
        if allowed:
            survivors += 1

    return total, survivors


def check_all_gamma_dimension_profiles() -> dict[tuple[int, int], tuple[int, int]]:
    profile_counts = {
        profile: profile_survivors(*profile)
        for profile in ((1, 1), (2, 1), (1, 2), (2, 2))
    }
    assert profile_counts == {
        (1, 1): (784, 0),
        (2, 1): (1372, 0),
        (1, 2): (1372, 0),
        (2, 2): (2401, 0),
    }
    return profile_counts


def beta_cross(
    x_vector: sp.Matrix,
    z_vector: sp.Matrix,
    y_vector: sp.Matrix,
    w_vector: sp.Matrix,
) -> sp.Matrix:
    return x_vector * w_vector.T + y_vector * z_vector.T


def core_response_flattening(
    h_matrix: sp.Matrix,
    a_s: sp.Matrix,
    c_s: sp.Matrix,
    a_t: sp.Matrix,
    c_t: sp.Matrix,
    b_st: sp.Matrix,
) -> sp.Matrix:
    """Flatten a 2 by 2 residual response against two ternary ports."""

    return sp.Matrix(
        4,
        9,
        lambda residual, local: (
            h_matrix[residual // 2, residual % 2] * b_st[local // 3, local % 3]
            + a_s[residual // 2, local // 3] * c_t[residual % 2, local % 3]
            + a_t[residual // 2, local % 3] * c_s[residual % 2, local // 3]
        ),
    )


def check_full_plane_beta_graph_and_b_rank() -> tuple[int, int, int]:
    """Solve the graph equations and replay ``B=q X_s^T J X_t``."""

    p, q, r, t_entry, a, b, c, d = sp.symbols("p q r t a b c d")
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2")
    x_vector = sp.Matrix([x1, x2])
    y_vector = sp.Matrix([y1, y2])
    mathsf_t = sp.Matrix([[p, q], [r, t_entry]])
    mathsf_s = sp.Matrix([[a, b], [c, d]])
    cross = beta_cross(
        x_vector,
        mathsf_t * x_vector,
        y_vector,
        mathsf_s * y_vector,
    )
    monomials = (x1 * y1, x1 * y2, x2 * y1, x2 * y2)
    equations = []
    for expression in (cross[0, 1], cross[1, 0], cross[0, 0] - cross[1, 1]):
        polynomial = sp.Poly(expression, x1, x2, y1, y2)
        equations.extend(polynomial.coeff_monomial(monomial) for monomial in monomials)
    solution = sp.solve(
        equations,
        (p, r, t_entry, a, b, c, d),
        dict=True,
    )
    assert solution == [
        {
            a: 0,
            b: -q,
            c: q,
            d: 0,
            p: 0,
            r: -q,
            t_entry: 0,
        }
    ]

    symplectic = sp.Matrix([[0, 1], [-1, 0]])
    solved_t = q * symplectic
    solved_s = -q * symplectic
    assert sp.expand(solved_t.det() - q**2) == 0
    solved_cross = beta_cross(
        x_vector,
        solved_t * x_vector,
        y_vector,
        solved_s * y_vector,
    )
    determinant = x1 * y2 - x2 * y1
    cross_difference = solved_cross + q * determinant * sp.eye(2)
    assert all(sp.expand(entry) == 0 for entry in cross_difference)

    xs_entries = sp.symbols("xs_0:4")
    xt_entries = sp.symbols("xt_0:4")
    x_s_square = sp.Matrix(2, 2, xs_entries)
    x_t_square = sp.Matrix(2, 2, xt_entries)
    square_b = q * x_s_square.T * symplectic * x_t_square
    assert sp.expand(square_b.det() - q**2 * x_s_square.det() * x_t_square.det()) == 0

    rational_fixtures = (
        (
            sp.Matrix([[1, 0, 0], [0, 1, 0]]),
            sp.Matrix([[1, 0, 1], [0, 1, 1]]),
            sp.Rational(2),
        ),
        (
            sp.Matrix([[1, 1, 0], [0, 1, 1]]),
            sp.Matrix([[2, -1, 0], [1, 0, 1]]),
            sp.Rational(-3, 2),
        ),
        (
            sp.Matrix([[1, 0, 2], [1, 1, 0]]),
            sp.Matrix([[0, 1, 1], [1, 0, -1]]),
            sp.Rational(5, 3),
        ),
    )
    fixture_checks = 0
    for x_s, x_t, q_value in rational_fixtures:
        assert x_s.rank() == x_t.rank() == 2
        t_matrix = q_value * symplectic
        s_matrix = -q_value * symplectic
        a_s = x_s
        c_s = t_matrix * x_s
        a_t = x_t
        c_t = s_matrix * x_t
        b_st = q_value * x_s.T * symplectic * x_t
        d_st = -q_value * x_s.T * symplectic * x_t
        assert b_st == -d_st
        response = core_response_flattening(
            sp.eye(2),
            a_s,
            c_s,
            a_t,
            c_t,
            b_st,
        )
        assert all(sp.expand(entry) == 0 for entry in response)
        assert b_st.rank() == 2
        fixture_checks += 1

    assert fixture_checks == 3
    return len(equations), fixture_checks, 2


def permanent4_columns(columns: tuple[sp.Matrix, ...]) -> sp.Expr:
    assert len(columns) == 4
    assert all(column.shape == (4, 1) for column in columns)
    return sp.expand(
        sum(
            sp.prod(columns[mode][assignment[mode]] for mode in range(4))
            for assignment in P4_PERMUTATIONS
        )
    )


def symbolic_incidence_map(prefix: str) -> sp.Matrix:
    return sp.Matrix(4, 3, sp.symbols(f"{prefix}_0:12"))


def check_common_incidence_column_splice() -> tuple[int, int]:
    """Check all 81 splice outputs and their weighted-Delta consequence."""

    l_q0 = symbolic_incidence_map("splice_q0")
    l_q1 = symbolic_incidence_map("splice_q1")
    l_t = symbolic_incidence_map("splice_t")
    tails = tuple(symbolic_incidence_map(f"splice_tail_{mode}") for mode in range(3))
    alpha, beta, gamma = (sp.Integer(2), sp.Integer(-3), sp.Integer(5))
    target_by_role = (sp.Integer(7), sp.Integer(11), sp.Integer(13))

    splice_coefficients = 0
    weighted_delta_coefficients = 0
    for i, j, k in permutations(COLOURS):
        synthetic = sp.zeros(4, 3)
        synthetic[:, i] = alpha * l_q1[:, i]
        synthetic[:, j] = beta * l_q0[:, j]
        synthetic[:, k] = gamma * l_t[:, k]
        source_map = {i: l_q1, j: l_q0, k: l_t}
        source_scalar = {i: alpha, j: beta, k: gamma}
        weights = [sp.Integer(0)] * 3
        weights[i], weights[j], weights[k] = target_by_role

        for word in WORDS_4:
            colour = word[0]
            tail_word = word[1:]
            spliced = permanent4_columns(
                (synthetic[:, colour],)
                + tuple(tails[mode][:, tail_word[mode]] for mode in range(3))
            )
            companion = permanent4_columns(
                (source_map[colour][:, colour],)
                + tuple(tails[mode][:, tail_word[mode]] for mode in range(3))
            )
            assert sp.expand(spliced - source_scalar[colour] * companion) == 0
            splice_coefficients += 1

            # Under the three multiplied pure-companion identities, the
            # preceding exact equality is the weighted diagonal coefficient.
            assumed_splice = (
                weights[colour]
                if tail_word == (colour, colour, colour)
                else sp.Integer(0)
            )
            assert assumed_splice == ghz_coefficient(word, tuple(weights))
            weighted_delta_coefficients += 1

    assert splice_coefficients == 6 * 81 == 486
    assert weighted_delta_coefficients == splice_coefficients
    return splice_coefficients, weighted_delta_coefficients


P4_PAIRS = tuple(combinations(range(4), 2))
P4_PAIR_INDEX = {pair: index for index, pair in enumerate(P4_PAIRS)}


def hyperplane_basis(normal: tuple[int, ...]) -> sp.Matrix:
    pivot = next(index for index, value in enumerate(normal) if value)
    columns = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [sp.Integer(0)] * 4
        vector[free] = 1
        vector[pivot] = -sp.Rational(normal[free], normal[pivot])
        columns.append(sp.Matrix(vector))
    return sp.Matrix.hstack(*columns)


def p4_pair_image(left: tuple[int, ...], right: tuple[int, ...]) -> sp.Matrix:
    left_basis = hyperplane_basis(left)
    right_basis = hyperplane_basis(right)
    columns = []
    for left_index, right_index in product(range(3), repeat=2):
        left_vector = left_basis[:, left_index]
        right_vector = right_basis[:, right_index]
        columns.append(
            sp.Matrix(
                [
                    left_vector[a] * right_vector[b] + left_vector[b] * right_vector[a]
                    for a, b in P4_PAIRS
                ]
            )
        )
    return sp.Matrix.hstack(*columns)


def p4_coefficient(maps: tuple[sp.Matrix, ...], word: Word) -> sp.Expr:
    return permanent4_columns(tuple(maps[mode][:, word[mode]] for mode in range(4)))


def check_p4_subrank_interface() -> tuple[int, int, int]:
    """Reconstruct the exact obstruction and explicit Delta2 lower bound."""

    equal_normal_ranks = {}
    for support in range(1, 5):
        normal = tuple([1] * support + [0] * (4 - support))
        equal_normal_ranks[support] = p4_pair_image(normal, normal).rank()
    assert equal_normal_ranks == {1: 3, 2: 4, 3: 5, 4: 6}

    independent_cases = {
        "generic": ((1, 1, 1, 1), (1, 2, 3, 4)),
        "square_proportional": ((1, 1, 1, 1), (1, -1, 1, -1)),
        "disjoint_support": ((1, 0, 0, 0), (0, 1, 0, 0)),
    }
    independent_ranks = {
        name: p4_pair_image(left, right).rank()
        for name, (left, right) in independent_cases.items()
    }
    assert independent_ranks == {
        "generic": 6,
        "square_proportional": 5,
        "disjoint_support": 6,
    }

    complement = sp.zeros(6)
    for pair, index in P4_PAIR_INDEX.items():
        other = tuple(vertex for vertex in range(4) if vertex not in pair)
        complement[index, P4_PAIR_INDEX[other]] = 1
    assert complement.det() in (1, -1)

    # The special-edge graph cover used by all three 2|2 flattenings.
    mode_partitions = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    set_partitions = 0
    for labels in product(range(4), repeat=4):
        relabel: dict[int, int] = {}
        canonical = []
        for label in labels:
            if label not in relabel:
                relabel[label] = len(relabel)
            canonical.append(relabel[label])
        if tuple(canonical) != labels:
            continue
        set_partitions += 1
        hits_all = all(
            labels[a] == labels[b] or labels[c] == labels[d]
            for (a, b), (c, d) in mode_partitions
        )
        if hits_all:
            assert max(labels.count(label) for label in set(labels)) >= 3
    assert set_partitions == 15

    ell, m_var, n_var = sp.symbols("ell m n")
    restricted = (-ell, ell, m_var, n_var)
    slices = []
    for omitted in range(4):
        remaining = [restricted[index] for index in range(4) if index != omitted]
        slices.append(sp.expand(6 * sp.prod(remaining)))
    assert slices == [
        6 * ell * m_var * n_var,
        -6 * ell * m_var * n_var,
        -6 * ell**2 * n_var,
        -6 * ell**2 * m_var,
    ]
    monomials = (ell * m_var * n_var, ell**2 * n_var, ell**2 * m_var)
    slice_matrix = sp.Matrix(
        [
            [
                sp.Poly(slice_value, ell, m_var, n_var).coeff_monomial(monomial)
                for slice_value in slices
            ]
            for monomial in monomials
        ]
    )
    assert slice_matrix.rank() == 3

    cube_a, cube_b, cube_c = sp.symbols("cube_a cube_b cube_c")
    cube = sp.Poly(
        (cube_a * ell + cube_b * m_var + cube_c * n_var) ** 3,
        ell,
        m_var,
        n_var,
    )
    forbidden = (
        cube.coeff_monomial(m_var**3),
        cube.coeff_monomial(n_var**3),
        cube.coeff_monomial(ell**3),
    )
    groebner = sp.groebner(
        forbidden,
        cube_a,
        cube_b,
        cube_c,
        order="lex",
    )
    assert list(groebner) == [cube_a**3, cube_b**3, cube_c**3]

    delta_two_maps = []
    for mode in range(4):
        local_map = sp.zeros(4, 2)
        local_map[mode, 0] = 1
        local_map[(mode + 1) % 4, 1] = 1
        delta_two_maps.append(local_map)
    delta_two_coefficients = {
        word: p4_coefficient(tuple(delta_two_maps), word)
        for word in product(range(2), repeat=4)
    }
    assert {
        word for word, coefficient in delta_two_coefficients.items() if coefficient
    } == {(0, 0, 0, 0), (1, 1, 1, 1)}
    assert delta_two_coefficients[(0, 0, 0, 0)] == 1
    assert delta_two_coefficients[(1, 1, 1, 1)] == 1

    return len(equal_normal_ranks) + len(independent_ranks), set_partitions, 2


def main() -> None:
    formal_words, formal_terms, formal_responses = (
        check_formal_triangle_complete_target()
    )
    target_words, quotient_coefficients = (
        check_labelled_sole_complementary_edge_survival()
    )
    rhs_ranks, noncoordinate_ranks = (
        check_projected_rhs_rank_with_noncoordinate_charts()
    )
    profile_counts = check_all_gamma_dimension_profiles()
    beta_equations, beta_fixtures, determinant_identities = (
        check_full_plane_beta_graph_and_b_rank()
    )
    splice_coefficients, weighted_delta = check_common_incidence_column_splice()
    p4_rank_cases, p4_partitions, p4_subrank = check_p4_subrank_interface()

    print("four-root rank-two core and singleton-triangle exact replay: PASS")
    print(
        f"  formal triangle: {formal_words} complete target words and "
        f"{formal_terms} labelled terms; {formal_responses} response coefficients"
    )
    print(
        f"  rank-two K4: {target_words} target words and "
        f"{quotient_coefficients} coefficients in six sole-edge quotients"
    )
    print(
        f"  projected GHZ rank=N on {rhs_ranks} exact chart pairs, "
        f"including {noncoordinate_ranks} noncoordinate pairs"
    )
    print(f"  Gamma profile exhaustions: {profile_counts}")
    print(
        f"  beta graph: {beta_equations} equations, {beta_fixtures} rational "
        f"fixtures, {determinant_identities} symbolic determinant identities"
    )
    print(
        f"  common-incidence splice: {splice_coefficients} coefficient identities, "
        f"{weighted_delta} weighted-Delta3 outputs"
    )
    print(
        f"  P4 interface: {p4_rank_cases} exact rank cases, "
        f"{p4_partitions} set partitions, subrank={p4_subrank}"
    )
    print("  rank-two core and rank-one singleton triangle: excluded by theorem")
    print("  rank-one Branches I, II, and two-port III remain OPEN")
    print("  no selector package or global resolution; Krenn--Gu is UNRESOLVED")
    print("  bounded replay only; arbitrary-point proofs are in the written theorem")


if __name__ == "__main__":
    main()
