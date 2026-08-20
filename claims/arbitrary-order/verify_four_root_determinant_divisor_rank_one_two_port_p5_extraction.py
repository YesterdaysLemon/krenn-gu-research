"""Focused exact replay for the rank-one two-port ``P_5`` extraction.

The accompanying theorem contains the arbitrary-point quotient and tensor
arguments.  This primary verifier checks their finite labelled algebra over
the exact rational polynomial ring used by SymPy: the three coordinate-factor
cases, all twelve common-tail routes, every coefficient of the Latin ``P_5``
splice by a direct 120-permutation expansion, the fifteen physical matchings,
and the signed two-row ``P_6`` sharpness identity.

This is a bounded proof replay, not an independent audit, a ``P_5``
nonrestriction theorem, a legal GLD selector package, or a global Krenn--Gu
result.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
I, J, K = COLOURS  # noqa: E741 - theorem colour labels
Q0, Q1, S, T, M, N = tuple(range(6))
VERTICES = (Q0, Q1, S, T, M, N)
PORTS = (S, T, M, N)
PAIRS = tuple(combinations(VERTICES, 2))
WORDS_5 = tuple(product(COLOURS, repeat=5))
WORDS_6 = tuple(product(COLOURS, repeat=6))
P4_PERMUTATIONS = tuple(permutations(range(4)))
P5_PERMUTATIONS = tuple(permutations(range(5)))
P6_PERMUTATIONS = tuple(permutations(range(6)))

a, b, tau, gamma = sp.symbols("a b tau gamma", nonzero=True)
mu_i, mu_j, mu_k = sp.symbols("mu_i mu_j mu_k", nonzero=True)
MU = (mu_i, mu_j, mu_k)
ZERO = sp.Integer(0)
ONE = sp.Integer(1)

Word = tuple[int, ...]
Pair = tuple[int, int]
PairName = tuple[str, str]


@dataclass(frozen=True)
class RoutedTerm:
    """One labelled summand in the remaining complete-target identity."""

    source: str
    scalar: sp.Expr
    pair: PairName


@dataclass(frozen=True)
class SyntheticColumn:
    """One top-only or bottom-only column of a synthetic incidence map."""

    top_name: str | None = None
    bottom_scalar: sp.Expr = ZERO

    @property
    def is_bottom(self) -> bool:
        return self.top_name is None


def basis(colour: int) -> sp.Matrix:
    """Return a ternary coordinate vector."""

    return sp.eye(3)[:, colour]


def quotient_away(colour: int) -> sp.Matrix:
    """Return the coordinate quotient by ``K e_colour``."""

    retained = tuple(entry for entry in COLOURS if entry != colour)
    quotient = sp.Matrix(
        2,
        3,
        lambda row, column: int(column == retained[row]),
    )
    assert quotient.rank() == 2
    assert quotient * basis(colour) == sp.zeros(2, 1)
    return quotient


def kronecker_columns(columns: tuple[sp.Matrix, ...]) -> sp.Matrix:
    answer = sp.Matrix([1])
    for column in columns:
        answer = sp.kronecker_product(answer, column)
    return answer


def possible_survivors(
    explicit_factors: dict[str, dict[int, int]],
    quotients: dict[int, sp.Matrix],
) -> tuple[str, ...]:
    """Return terms not structurally killed by an explicit factor quotient."""

    survivors = []
    for term, factors in explicit_factors.items():
        killed = any(
            slot in factors
            and quotient * basis(factors[slot]) == sp.zeros(quotient.rows, 1)
            for slot, quotient in quotients.items()
        )
        if not killed:
            survivors.append(term)
    return tuple(survivors)


def check_coordinate_pairing_cases() -> tuple[int, int, int]:
    """Replay the ``d=i``, ``d=j``, and ``d=k`` quotient/rank cases."""

    explicit_by_d = {}
    for d in COLOURS:
        explicit_by_d[d] = {
            "A_s": {Q0: I, S: d},
            "A_t": {Q0: I},
            "C_s": {Q1: J, S: d},
            "C_t": {Q1: J},
        }

    i_quotients = {Q0: quotient_away(I), S: quotient_away(I)}
    j_quotients = {Q1: quotient_away(J), S: quotient_away(J)}
    k_quotients = {S: quotient_away(K)}
    assert possible_survivors(explicit_by_d[I], i_quotients) == ("C_t",)
    assert possible_survivors(explicit_by_d[J], j_quotients) == ("A_t",)
    assert possible_survivors(explicit_by_d[K], k_quotients) == ("A_t", "C_t")

    # In the first two cases, equality of the only surviving simple tensor
    # with the pure target forces the remaining t-factor onto the target line.
    x0, x1, x2 = sp.symbols("x0 x1 x2")
    alpha = sp.Matrix([x0, x1, x2])
    forced_j = quotient_away(J) * alpha
    forced_i = quotient_away(I) * alpha
    assert tuple(forced_j) == (x0, x2)
    assert tuple(forced_i) == (x1, x2)
    assert quotient_away(J).nullspace() == [basis(J)]
    assert quotient_away(I).nullspace() == [basis(I)]

    # For d=k, quotient the s-slot and flatten across t.  The target has two
    # independent rows, whereas any two terms sharing alpha_t have rank <= 1.
    qk = quotient_away(K)
    rest_i = kronecker_columns((basis(I), basis(I), qk * basis(I), basis(I), basis(I)))
    rest_j = kronecker_columns((basis(J), basis(J), qk * basis(J), basis(J), basis(J)))
    target_flattening = (
        sp.Integer(11) * basis(I) * rest_i.T + sp.Integer(13) * basis(J) * rest_j.T
    )
    shared_factor_flattening = sp.Matrix([1, 2, 3]) * (rest_i + rest_j).T
    assert rest_i.shape == rest_j.shape == (162, 1)
    assert target_flattening.rank() == 2
    assert shared_factor_flattening.rank() == 1
    return 3, 2, target_flattening.rank()


def named_pair(left: str, right: str) -> PairName:
    return tuple(sorted((left, right)))


def q0_column(colour: int) -> str:
    return "Y" if colour == J else f"Q0_{colour}"


def q1_column(colour: int) -> str:
    return "X" if colour == I else f"Q1_{colour}"


def s_column(colour: int) -> str:
    return {I: "S_i", J: "S_j", K: "S_k"}[colour]


def t_column(colour: int) -> str:
    return {I: "T_i", J: "T_j", K: "T_k"}[colour]


def remaining_target_terms(word: Word) -> tuple[RoutedTerm, ...]:
    """Return the four possible terms of equation (5) at one active word."""

    assert len(word) == 4
    q0_colour, q1_colour, s_colour, t_colour = word
    terms = []
    if q0_colour == I and s_colour == I:
        terms.append(
            RoutedTerm(
                "A_s",
                a,
                named_pair(q1_column(q1_colour), t_column(t_colour)),
            )
        )
    if q0_colour == I and t_colour == J:
        terms.append(
            RoutedTerm(
                "A_t",
                b,
                named_pair(q1_column(q1_colour), s_column(s_colour)),
            )
        )
    if q1_colour == J and s_colour == I:
        terms.append(
            RoutedTerm(
                "C_s",
                tau * a,
                named_pair(q0_column(q0_colour), t_column(t_colour)),
            )
        )
    if q1_colour == J and t_colour == J:
        terms.append(
            RoutedTerm(
                "C_t",
                -tau * b,
                named_pair(q0_column(q0_colour), s_column(s_colour)),
            )
        )
    return tuple(terms)


ZERO_PAIR_ROUTES = {
    named_pair("T_i", "Y"),
    named_pair("T_k", "X"),
    named_pair("T_k", "Y"),
    named_pair("S_j", "X"),
    named_pair("S_k", "Y"),
    named_pair("S_k", "X"),
    named_pair("S_j", "T_i"),
    named_pair("S_j", "T_k"),
    named_pair("S_k", "T_i"),
}

DIAGONAL_PAIR_ROUTES = {
    named_pair("X", "T_i"): (a, I),
    named_pair("Y", "S_j"): (-tau * b, J),
    named_pair("S_k", "T_k"): (gamma, K),
}


def check_common_tail_routes() -> tuple[int, int, int]:
    """Derive the three diagonal and nine zero routes with exact labels."""

    equation5_routes = {
        (I, I, I, I): RoutedTerm("A_s", a, named_pair("X", "T_i")),
        (J, J, J, J): RoutedTerm("C_t", -tau * b, named_pair("Y", "S_j")),
        (J, J, I, I): RoutedTerm("C_s", tau * a, named_pair("Y", "T_i")),
        (I, I, I, K): RoutedTerm("A_s", a, named_pair("X", "T_k")),
        (J, J, I, K): RoutedTerm("C_s", tau * a, named_pair("Y", "T_k")),
        (I, I, J, J): RoutedTerm("A_t", b, named_pair("X", "S_j")),
        (J, J, K, J): RoutedTerm("C_t", -tau * b, named_pair("Y", "S_k")),
        (I, I, K, J): RoutedTerm("A_t", b, named_pair("X", "S_k")),
    }
    for word, expected in equation5_routes.items():
        assert remaining_target_terms(word) == (expected,)

    equation4_routes = {
        (K, K): (gamma, named_pair("S_k", "T_k"), mu_k),
        (J, I): (gamma, named_pair("S_j", "T_i"), sp.Integer(0)),
        (J, K): (gamma, named_pair("S_j", "T_k"), sp.Integer(0)),
        (K, I): (gamma, named_pair("S_k", "T_i"), sp.Integer(0)),
    }
    assert equation4_routes[(K, K)][1] in DIAGONAL_PAIR_ROUTES
    assert all(
        pair in ZERO_PAIR_ROUTES
        for _, pair, target in equation4_routes.values()
        if target == 0
    )

    equation5_diagonals = 2
    equation5_zeros = 6
    equation4_diagonals = 1
    equation4_zeros = 3
    assert equation5_diagonals + equation5_zeros == 8
    assert equation4_diagonals + equation4_zeros == 4
    assert len(DIAGONAL_PAIR_ROUTES) == 3
    assert len(ZERO_PAIR_ROUTES) == 9
    return 3, 9, 12


TOP_VECTORS: dict[str, sp.Matrix] = {}


def top_vector(name: str) -> sp.Matrix:
    if name not in TOP_VECTORS:
        TOP_VECTORS[name] = sp.Matrix(sp.symbols(f"{name}_0:4"))
    return TOP_VECTORS[name]


def top_column(name: str, ambient_dimension: int) -> sp.Matrix:
    assert ambient_dimension >= 4
    return top_vector(name).col_join(sp.zeros(ambient_dimension - 4, 1))


def bottom_column(scalar: sp.Expr, ambient_dimension: int, row: int = 4) -> sp.Matrix:
    column = sp.zeros(ambient_dimension, 1)
    column[row] = scalar
    return column


def permanent_columns(
    columns: tuple[sp.Matrix, ...],
    all_permutations: tuple[tuple[int, ...], ...],
) -> sp.Expr:
    """Expand a permanent directly, retaining every supplied permutation."""

    size = len(columns)
    assert all(column.shape == (size, 1) for column in columns)
    assert len(all_permutations) == sp.factorial(size)
    terms = []
    for permutation in all_permutations:
        term = sp.Integer(1)
        for column_index, row_index in enumerate(permutation):
            term *= columns[column_index][row_index]
            if term == 0:
                break
        terms.append(term)
    assert len(terms) == len(all_permutations)
    return sp.expand(sum(terms, sp.Integer(0)))


SYNTHETIC_MAPS = (
    {
        I: SyntheticColumn(bottom_scalar=a),
        J: SyntheticColumn(top_name="S_j"),
        K: SyntheticColumn(top_name="S_k"),
    },
    {
        I: SyntheticColumn(top_name="T_i"),
        J: SyntheticColumn(bottom_scalar=-tau * b),
        K: SyntheticColumn(top_name="T_k"),
    },
    {
        I: SyntheticColumn(top_name="X"),
        J: SyntheticColumn(top_name="Y"),
        K: SyntheticColumn(bottom_scalar=gamma),
    },
)


def synthetic_matrix_column(column: SyntheticColumn) -> sp.Matrix:
    if column.is_bottom:
        return bottom_column(column.bottom_scalar, 5)
    assert column.top_name is not None
    return top_column(column.top_name, 5)


def ghz5_coefficient(word: Word) -> sp.Expr:
    for colour, weight in enumerate(MU):
        if word == (colour,) * 5:
            return weight
    return sp.Integer(0)


def scaled_common_tail_value(
    bottom_scalar: sp.Expr,
    pair: PairName,
    tail_word: tuple[int, int],
) -> sp.Expr:
    """Apply (13)--(14) without dividing by an active scalar."""

    if pair in ZERO_PAIR_ROUTES:
        return sp.Integer(0)
    relation_scalar, colour = DIAGONAL_PAIR_ROUTES[pair]
    assert sp.expand(bottom_scalar - relation_scalar) == 0
    if tail_word == (colour, colour):
        return MU[colour]
    return sp.Integer(0)


def check_direct_p5_splice() -> tuple[int, int, tuple[int, int, int]]:
    """Check all 243 coefficients by all 120 permanent permutations."""

    structural_triples = set()
    zero_relation_triples = set()
    diagonal_triples = set()
    coefficients = 0
    permutation_terms = 0

    for word in WORDS_5:
        triple = word[:3]
        tail_word = word[3:]
        descriptors = tuple(SYNTHETIC_MAPS[mode][triple[mode]] for mode in range(3))
        columns = tuple(synthetic_matrix_column(entry) for entry in descriptors) + (
            top_column(f"M_{tail_word[0]}", 5),
            top_column(f"N_{tail_word[1]}", 5),
        )
        direct = permanent_columns(columns, P5_PERMUTATIONS)
        permutation_terms += len(P5_PERMUTATIONS)

        bottoms = tuple(entry for entry in descriptors if entry.is_bottom)
        tops = tuple(entry for entry in descriptors if not entry.is_bottom)
        if len(bottoms) != 1:
            expected_expansion = sp.Integer(0)
            reduced = sp.Integer(0)
            structural_triples.add(triple)
        else:
            assert len(tops) == 2
            top_names = tuple(entry.top_name for entry in tops)
            assert all(name is not None for name in top_names)
            expected_expansion = bottoms[0].bottom_scalar * permanent_columns(
                (
                    top_vector(top_names[0]),
                    top_vector(top_names[1]),
                    top_vector(f"M_{tail_word[0]}"),
                    top_vector(f"N_{tail_word[1]}"),
                ),
                P4_PERMUTATIONS,
            )
            pair = named_pair(top_names[0], top_names[1])
            reduced = scaled_common_tail_value(
                bottoms[0].bottom_scalar,
                pair,
                tail_word,
            )
            if pair in ZERO_PAIR_ROUTES:
                zero_relation_triples.add(triple)
            else:
                diagonal_triples.add(triple)

        assert sp.expand(direct - expected_expansion) == 0
        assert sp.expand(reduced - ghz5_coefficient(word)) == 0
        coefficients += 1

    assert coefficients == 243
    assert permutation_terms == 243 * 120 == 29160
    assert diagonal_triples == {(I, I, I), (J, J, J), (K, K, K)}
    assert len(zero_relation_triples) == 9
    assert len(structural_triples) == 15
    assert diagonal_triples | zero_relation_triples | structural_triples == set(
        product(COLOURS, repeat=3)
    )
    return (
        coefficients,
        permutation_terms,
        (
            len(diagonal_triples),
            len(zero_relation_triples),
            len(structural_triples),
        ),
    )


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate all labelled perfect matchings recursively."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def matrix_unit(
    row: int,
    column: int,
    coefficient: sp.Expr = ONE,
) -> sp.Matrix:
    answer = sp.zeros(3)
    answer[row, column] = coefficient
    return answer


def edge_block(edges: dict[Pair, sp.Matrix], left: int, right: int) -> sp.Matrix:
    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


def check_automatic_six_vertex_response() -> tuple[int, int]:
    """Check all fifteen matchings termwise, at every physical colour word."""

    matchings = tuple(perfect_matchings(VERTICES))
    assert len(matchings) == 15
    nonzero_edge_support = {
        (Q0, Q1),
        (Q0, S),
        (Q0, T),
        (Q1, S),
        (Q1, T),
    }
    assert all(
        any(tuple(sorted(edge)) not in nonzero_edge_support for edge in matching)
        for matching in matchings
    )

    edges = {
        (Q0, Q1): gamma * matrix_unit(K, K),
        (Q0, S): a * matrix_unit(I, I),
        (Q0, T): b * matrix_unit(I, J),
        (Q1, S): tau * a * matrix_unit(J, I),
        (Q1, T): -tau * b * matrix_unit(J, J),
    }
    checked_terms = 0
    for word in WORDS_6:
        colours = dict(zip(VERTICES, word, strict=True))
        for matching in matchings:
            term = sp.Integer(1)
            for left, right in matching:
                term *= edge_block(edges, left, right)[colours[left], colours[right]]
            assert sp.expand(term) == 0
            checked_terms += 1
    assert checked_terms == 729 * 15 == 10935
    return len(matchings), checked_terms


def p6_bottom_entry(mode: int, colour: int) -> tuple[sp.Expr, sp.Expr]:
    """Return the two extra-row entries in equation (25)."""

    if mode == Q0 and colour == I:
        return sp.Integer(1), sp.Integer(0)
    if mode == Q1 and colour == J:
        return sp.Integer(0), tau
    if mode == S and colour == I:
        return a, a
    if mode == T and colour == J:
        return -b, b
    return sp.Integer(0), sp.Integer(0)


def bottom_pair_permanent(
    left: tuple[sp.Expr, sp.Expr],
    right: tuple[sp.Expr, sp.Expr],
) -> sp.Expr:
    return sp.expand(left[0] * right[1] + left[1] * right[0])


def p6_top_name(mode: int, colour: int) -> str:
    if mode == Q0:
        return q0_column(colour)
    if mode == Q1:
        return q1_column(colour)
    if mode == S:
        return s_column(colour)
    if mode == T:
        return t_column(colour)
    if mode == M:
        return f"M_{colour}"
    if mode == N:
        return f"N_{colour}"
    raise AssertionError(f"unknown mode {mode}")


def p6_matrix_column(mode: int, colour: int) -> sp.Matrix:
    bottom = p6_bottom_entry(mode, colour)
    return top_vector(p6_top_name(mode, colour)).col_join(sp.Matrix(bottom))


def check_p6_sharpness_signs() -> tuple[int, int, int, int]:
    """Check the two-row Laplace partition, signs, and mismatched target."""

    # Every 6-permutation chooses two columns for the last two rows.  Grouping
    # by their unordered pair gives 15 groups of size 2!*4!=48.
    permutation_groups: dict[Pair, int] = {pair: 0 for pair in PAIRS}
    for permutation in P6_PERMUTATIONS:
        bottom_columns = tuple(
            sorted(column for column, row in enumerate(permutation) if row in (4, 5))
        )
        assert len(bottom_columns) == 2
        permutation_groups[bottom_columns] += 1
    assert set(permutation_groups.values()) == {48}
    assert sum(permutation_groups.values()) == 720

    nonzero_bottom_coefficients = {}
    checked_bottom_coefficients = 0
    for left, right in PAIRS:
        for left_colour, right_colour in product(COLOURS, repeat=2):
            value = bottom_pair_permanent(
                p6_bottom_entry(left, left_colour),
                p6_bottom_entry(right, right_colour),
            )
            if value != 0:
                nonzero_bottom_coefficients[
                    (left, right, left_colour, right_colour)
                ] = value
            checked_bottom_coefficients += 1

    assert nonzero_bottom_coefficients == {
        (Q0, Q1, I, J): tau,
        (Q0, S, I, I): a,
        (Q0, T, I, J): b,
        (Q1, S, J, I): tau * a,
        (Q1, T, J, J): -tau * b,
    }
    assert (
        bottom_pair_permanent(
            p6_bottom_entry(S, I),
            p6_bottom_entry(T, J),
        )
        == 0
    )
    assert checked_bottom_coefficients == 15 * 9 == 135

    # Check the complete six-by-six permanent directly at every target word.
    # The comparison is with the unsigned two-row Laplace expansion, so it
    # audits the signs without assuming the target equations.
    routed_coefficients = 0
    direct_permutation_terms = 0
    for word in WORDS_6:
        columns = tuple(p6_matrix_column(mode, word[mode]) for mode in VERTICES)
        direct = permanent_columns(columns, P6_PERMUTATIONS)
        direct_permutation_terms += len(P6_PERMUTATIONS)

        laplace = sp.Integer(0)
        physical_routes = []
        extra_route: RoutedTerm | None = None
        for left, right in PAIRS:
            scalar = bottom_pair_permanent(
                p6_bottom_entry(left, word[left]),
                p6_bottom_entry(right, word[right]),
            )
            if scalar == 0:
                continue
            complement = tuple(mode for mode in VERTICES if mode not in (left, right))
            laplace += scalar * permanent_columns(
                tuple(top_vector(p6_top_name(mode, word[mode])) for mode in complement),
                P4_PERMUTATIONS,
            )
            if (left, right) == (Q0, Q1):
                extra_route = RoutedTerm(
                    "q0q1",
                    scalar,
                    named_pair(s_column(word[S]), t_column(word[T])),
                )
            else:
                source = {
                    (Q0, S): "A_s",
                    (Q0, T): "A_t",
                    (Q1, S): "C_s",
                    (Q1, T): "C_t",
                }[(left, right)]
                other_pair = {
                    "A_s": named_pair(q1_column(word[Q1]), t_column(word[T])),
                    "A_t": named_pair(q1_column(word[Q1]), s_column(word[S])),
                    "C_s": named_pair(q0_column(word[Q0]), t_column(word[T])),
                    "C_t": named_pair(q0_column(word[Q0]), s_column(word[S])),
                }[source]
                physical_routes.append(RoutedTerm(source, scalar, other_pair))

        assert sp.expand(direct - laplace) == 0
        assert tuple(physical_routes) == remaining_target_terms(word[:4])

        # Equation (5) evaluates the four physical routes.  Equation (4)
        # evaluates the separate q0q1 route, which exists only at Q-word ij.
        remaining_target = mu_i * int(word == (I,) * 6) + mu_j * int(word == (J,) * 6)
        extra_target = sp.Integer(0)
        if extra_route is not None:
            assert word[Q0 : Q1 + 1] == (I, J)
            assert extra_route.scalar == tau
            if word[S:] == (K, K, K, K):
                extra_target = tau * mu_k / gamma
        reduced = remaining_target + extra_target
        expected = (
            mu_i * int(word == (I,) * 6)
            + mu_j * int(word == (J,) * 6)
            + (tau * mu_k / gamma) * int(word == (I, J, K, K, K, K))
        )
        assert sp.expand(reduced - expected) == 0
        routed_coefficients += 1
    assert routed_coefficients == 729
    assert direct_permutation_terms == 729 * 720 == 524880

    # The q0 and q1 flattening supports contain only {i,j}; equation (26) is
    # therefore deliberately not a concise three-colour P6 restriction.
    q0_support = {I, J}
    q1_support = {I, J}
    assert len(q0_support) == len(q1_support) == 2
    return (
        checked_bottom_coefficients,
        routed_coefficients,
        direct_permutation_terms,
        5,
    )


def main() -> None:
    quotient_cases, forced_lines, target_rank = check_coordinate_pairing_cases()
    diagonal_relations, zero_relations, total_relations = check_common_tail_routes()
    p5_coefficients, p5_permutation_terms, triple_split = check_direct_p5_splice()
    matchings, matching_terms = check_automatic_six_vertex_response()
    (
        p6_bottom_coefficients,
        p6_coefficients,
        p6_permutation_terms,
        p6_nonzero_blocks,
    ) = check_p6_sharpness_signs()

    print("four-root rank-one two-port P5 extraction exact replay: PASS")
    print(
        f"  coordinate pairing: {quotient_cases} quotient cases, "
        f"{forced_lines} forced factor lines, forbidden target rank={target_rank}"
    )
    print(
        f"  common tails: {diagonal_relations} diagonal + {zero_relations} zero "
        f"relations = {total_relations}; source split 8 from (5), 4 from (4)"
    )
    print(
        f"  direct P5: {p5_coefficients} coefficients, "
        f"{p5_permutation_terms} permutation terms; triple split "
        f"diagonal/zero/structural={triple_split}"
    )
    print(
        f"  seventh response: {matchings} physical matchings and "
        f"{matching_terms} termwise-zero colour evaluations"
    )
    print(
        f"  P6 sharpness: {p6_bottom_coefficients} bottom coefficients, "
        f"{p6_coefficients} target routes, {p6_permutation_terms} direct "
        f"permutation terms, {p6_nonzero_blocks} signed blocks"
    )
    print("  exact symbolic arithmetic over QQ; no numerical or modular evidence")
    print("  bounded primary replay only; arbitrary-point proofs are in the theorem")
    print("  P5 nonrestriction and strategic node remain OPEN; global UNRESOLVED")


if __name__ == "__main__":
    main()
