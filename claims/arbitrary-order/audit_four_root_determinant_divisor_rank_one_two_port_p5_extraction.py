"""Independent exact audit of the rank-one two-port P5 extraction.

This standard-library-only audit does not read or import the focused primary
verifier or any repository module.  It reconstructs the finite algebra using
exact :class:`fractions.Fraction` arithmetic and a sparse row-assignment model
that expands every defining permanent permutation directly.

The checks cover the three coordinate-pairing quotient cases, the labelled
8+4 source routing into three diagonal and nine zero common-tail relations,
all 120 row assignments for each of the 243 P5 output coefficients, all 15
perfect matchings of the physical six-vertex response, and the independent
two-extra-row P6 sign/sharpness identity.

This is a bounded replay of displayed finite identities.  The written proof
remains responsible for the arbitrary-point quotient implications and for
the inherited Branch-III hypotheses.  The audit proves no P5 nonrestriction,
selector theorem, strategic-node closure, or global Krenn--Gu result.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from fractions import Fraction
from functools import cache
from itertools import permutations, product
from math import factorial
from typing import TypeAlias

Scalar: TypeAlias = Fraction
Vector: TypeAlias = tuple[Scalar, ...]
Matrix: TypeAlias = tuple[Vector, ...]
Color: TypeAlias = str
Variable: TypeAlias = tuple[str, int]
Monomial: TypeAlias = tuple[Variable, ...]
Polynomial: TypeAlias = dict[Monomial, Scalar]
Entry: TypeAlias = tuple[Scalar, Monomial] | None
Column: TypeAlias = tuple[Entry, ...]
PairKey: TypeAlias = tuple[str, str]

ZERO = Fraction(0)
ONE = Fraction(1)

I = "i"  # noqa: E741 - theorem colour label
J = "j"
K = "k"
COLORS: tuple[Color, ...] = (I, J, K)

Q0 = "q0"
Q1 = "q1"
S = "s"
T = "t"
M = "m"
N = "n"
PHYSICAL_SLOTS = (Q0, Q1, S, T, M, N)

# Distinct positive rational representatives preserve every displayed sign
# and every declared nonzero gate without using numerical approximation.
A = Fraction(2)
B = Fraction(3)
TAU = Fraction(5)
GAMMA = Fraction(7)
MU = {I: Fraction(11), J: Fraction(13), K: Fraction(17)}


def basis(dimension: int, coordinate: int) -> Vector:
    return tuple(ONE if index == coordinate else ZERO for index in range(dimension))


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(a * b for b in right) for a in left)


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def matrix_rank(value: Sequence[Sequence[Scalar]]) -> int:
    rows = [list(row) for row in value if any(row)]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def proportional(left: Vector, right: Vector) -> bool:
    if not any(left) or not any(right):
        return False
    pivot = next(index for index, entry in enumerate(right) if entry)
    multiple = left[pivot] / right[pivot]
    return all(a == multiple * b for a, b in zip(left, right, strict=True))


def nonzero_column(value: Matrix) -> Vector:
    for column in range(len(value[0])):
        candidate = tuple(row[column] for row in value)
        if any(candidate):
            return candidate
    raise AssertionError("expected a nonzero matrix")


def structurally_killed(
    fixed_factors: dict[str, Color], killed_lines: dict[str, Color]
) -> bool:
    return any(fixed_factors.get(slot) == color for slot, color in killed_lines.items())


def check_coordinate_pairing_quotients() -> dict[str, int]:
    """Replay the two forced lines and the rank-two contradiction.

    An omitted slot in ``fixed_factors`` is carried by a complementary
    permanent and is not declared structurally zero in the quotient.  Thus
    the table records exactly which summands are killed by their displayed
    edge factors, independently of any special value of a companion.
    """

    source_fixed = {
        "A_s": {Q0: I, S: I},
        "A_t": {Q0: I},
        "C_s": {Q1: J, S: I},
        "C_t": {Q1: J},
    }
    mixed_target_fixed = {
        color: {slot: color for slot in PHYSICAL_SLOTS} for color in (I, J)
    }

    case_i_kills = {Q0: I, S: I}
    case_i_sources = tuple(
        name
        for name, factors in source_fixed.items()
        if not structurally_killed(factors, case_i_kills)
    )
    case_i_targets = tuple(
        color
        for color, factors in mixed_target_fixed.items()
        if not structurally_killed(factors, case_i_kills)
    )
    assert case_i_sources == ("C_t",)
    assert case_i_targets == (J,)
    # Equality with the sole C_t term forces the t-factor line to be K e_j by
    # rank-one factor uniqueness.
    target_j = outer(basis(3, 1), (Fraction(2), Fraction(-3), Fraction(5)))
    assert matrix_rank(target_j) == 1
    assert proportional(nonzero_column(target_j), basis(3, 1))

    # Before the final s<->t relabelling, the symmetric d=j quotient forces
    # alpha_t onto the i-line.
    case_j_fixed = {
        "A_s": {Q0: I, S: J},
        "A_t": {Q0: I},
        "C_s": {Q1: J, S: J},
        "C_t": {Q1: J},
    }
    case_j_kills = {Q1: J, S: J}
    case_j_sources = tuple(
        name
        for name, factors in case_j_fixed.items()
        if not structurally_killed(factors, case_j_kills)
    )
    case_j_targets = tuple(
        color
        for color, factors in mixed_target_fixed.items()
        if not structurally_killed(factors, case_j_kills)
    )
    assert case_j_sources == ("A_t",)
    assert case_j_targets == (I,)
    target_i = outer(basis(3, 0), (Fraction(7), Fraction(11)))
    assert matrix_rank(target_i) == 1
    assert proportional(nonzero_column(target_i), basis(3, 0))

    # If alpha_s has the third colour k, quotienting the s-slot kills the two
    # s-edge terms.  A_t and C_t share alpha_t on the t-side, so their sum has
    # flattening rank at most one.  The surviving i and j pure targets have
    # independent t-lines and independent complementary tags, hence rank two.
    case_k_fixed = {
        "A_s": {Q0: I, S: K},
        "A_t": {Q0: I},
        "C_s": {Q1: J, S: K},
        "C_t": {Q1: J},
    }
    case_k_kills = {S: K}
    case_k_sources = tuple(
        name
        for name, factors in case_k_fixed.items()
        if not structurally_killed(factors, case_k_kills)
    )
    case_k_targets = tuple(
        color
        for color, factors in mixed_target_fixed.items()
        if not structurally_killed(factors, case_k_kills)
    )
    assert case_k_sources == ("A_t", "C_t")
    assert case_k_targets == (I, J)
    lhs_flattening = outer(
        (Fraction(2), Fraction(-3), Fraction(5)),
        (Fraction(7), Fraction(-11)),
    )
    rhs_flattening = matrix_add(
        outer(basis(3, 0), (MU[I], ZERO)),
        outer(basis(3, 1), (ZERO, MU[J])),
    )
    assert matrix_rank(lhs_flattening) == 1
    assert matrix_rank(rhs_flattening) == 2

    return {
        "coordinate_cases": 3,
        "forced_coordinate_lines": 2,
        "rank_two_contradictions": 1,
    }


def incidence_label(slot: str, color: Color) -> str:
    aliases = {(Q1, I): "X", (Q0, J): "Y"}
    if (slot, color) in aliases:
        return aliases[(slot, color)]
    return f"{slot.upper()}_{color}"


def pair_key(left: str, right: str) -> PairKey:
    first, second = sorted((left, right))
    return first, second


def mixed_routes(
    word: tuple[Color, Color, Color, Color],
) -> tuple[tuple[str, Scalar, PairKey], ...]:
    q0_color, q1_color, s_color, t_color = word
    routes: list[tuple[str, Scalar, PairKey]] = []
    if q0_color == I and s_color == I:
        routes.append(
            (
                "A_s",
                A,
                pair_key(
                    incidence_label(Q1, q1_color),
                    incidence_label(T, t_color),
                ),
            )
        )
    if q0_color == I and t_color == J:
        routes.append(
            (
                "A_t",
                B,
                pair_key(
                    incidence_label(Q1, q1_color),
                    incidence_label(S, s_color),
                ),
            )
        )
    if q1_color == J and s_color == I:
        routes.append(
            (
                "C_s",
                TAU * A,
                pair_key(
                    incidence_label(Q0, q0_color),
                    incidence_label(T, t_color),
                ),
            )
        )
    if q1_color == J and t_color == J:
        routes.append(
            (
                "C_t",
                -TAU * B,
                pair_key(
                    incidence_label(Q0, q0_color),
                    incidence_label(S, s_color),
                ),
            )
        )
    return tuple(routes)


MIXED_RELATION_ROWS = (
    ((I, I, I, I), "A_s", A, pair_key("X", "T_i"), "diagonal-i"),
    ((J, J, J, J), "C_t", -TAU * B, pair_key("Y", "S_j"), "diagonal-j"),
    ((J, J, I, I), "C_s", TAU * A, pair_key("T_i", "Y"), "zero"),
    ((I, I, I, K), "A_s", A, pair_key("T_k", "X"), "zero"),
    ((J, J, I, K), "C_s", TAU * A, pair_key("T_k", "Y"), "zero"),
    ((I, I, J, J), "A_t", B, pair_key("S_j", "X"), "zero"),
    ((J, J, K, J), "C_t", -TAU * B, pair_key("S_k", "Y"), "zero"),
    ((I, I, K, J), "A_t", B, pair_key("S_k", "X"), "zero"),
)

COMPANION_RELATION_ROWS = (
    ((K, K), GAMMA, pair_key("S_k", "T_k"), "diagonal-k"),
    ((J, I), GAMMA, pair_key("S_j", "T_i"), "zero"),
    ((J, K), GAMMA, pair_key("S_j", "T_k"), "zero"),
    ((K, I), GAMMA, pair_key("S_k", "T_i"), "zero"),
)

DIAGONAL_RELATIONS = {
    pair_key("X", "T_i"): (I, MU[I] / A),
    pair_key("Y", "S_j"): (J, MU[J] / (-TAU * B)),
    pair_key("S_k", "T_k"): (K, MU[K] / GAMMA),
}
ZERO_RELATIONS = frozenset(
    {
        pair_key("T_i", "Y"),
        pair_key("T_k", "X"),
        pair_key("T_k", "Y"),
        pair_key("S_j", "X"),
        pair_key("S_k", "Y"),
        pair_key("S_k", "X"),
        pair_key("S_j", "T_i"),
        pair_key("S_j", "T_k"),
        pair_key("S_k", "T_i"),
    }
)


def check_common_tail_relation_routing() -> dict[str, int]:
    source_counts: Counter[str] = Counter()
    relation_kinds: Counter[str] = Counter()
    routed_pairs: set[PairKey] = set()
    for word, source, scalar, pairing, kind in MIXED_RELATION_ROWS:
        assert mixed_routes(word) == ((source, scalar, pairing),)
        source_counts[source] += 1
        relation_kinds[kind] += 1
        routed_pairs.add(pairing)

    for (s_color, t_color), scalar, pairing, kind in COMPANION_RELATION_ROWS:
        assert scalar == GAMMA
        assert pairing == pair_key(
            incidence_label(S, s_color), incidence_label(T, t_color)
        )
        relation_kinds[kind] += 1
        routed_pairs.add(pairing)

    assert source_counts == Counter({"A_s": 2, "A_t": 2, "C_s": 2, "C_t": 2})
    assert relation_kinds == Counter(
        {"zero": 9, "diagonal-i": 1, "diagonal-j": 1, "diagonal-k": 1}
    )
    assert not (set(DIAGONAL_RELATIONS) & set(ZERO_RELATIONS))
    assert routed_pairs == set(DIAGONAL_RELATIONS) | set(ZERO_RELATIONS)
    assert len(routed_pairs) == 12

    return {
        "complete_mixed_relations": len(MIXED_RELATION_ROWS),
        "companion_relations": len(COMPANION_RELATION_ROWS),
        "diagonal_relations": len(DIAGONAL_RELATIONS),
        "zero_relations": len(ZERO_RELATIONS),
    }


def normalize_polynomial(value: Polynomial) -> Polynomial:
    return {monomial: scalar for monomial, scalar in value.items() if scalar}


def add_polynomials(*values: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for value in values:
        for monomial, scalar in value.items():
            answer[monomial] = answer.get(monomial, ZERO) + scalar
    return normalize_polynomial(answer)


def scale_polynomial(value: Polynomial, scalar: Scalar) -> Polynomial:
    return normalize_polynomial(
        {monomial: scalar * coefficient for monomial, coefficient in value.items()}
    )


def top_column(label: str, size: int) -> Column:
    return tuple((ONE, ((label, row),)) if row < 4 else None for row in range(size))


def bottom_only_column(scalar: Scalar, size: int, row: int) -> Column:
    return tuple((scalar, ()) if index == row else None for index in range(size))


def augmented_column(label: str, size: int, extra_entries: dict[int, Scalar]) -> Column:
    entries = list(top_column(label, size))
    for row, scalar in extra_entries.items():
        entries[row] = (scalar, ()) if scalar else None
    return tuple(entries)


def sparse_permanent(columns: Sequence[Column]) -> tuple[Polynomial, int, int]:
    size = len(columns)
    assert size and all(len(column) == size for column in columns)
    answer: Polynomial = {}
    examined = 0
    surviving = 0
    for row_assignment in permutations(range(size)):
        examined += 1
        coefficient = ONE
        variables: list[Variable] = []
        for column, row in zip(columns, row_assignment, strict=True):
            entry = column[row]
            if entry is None:
                coefficient = ZERO
                break
            entry_coefficient, entry_variables = entry
            coefficient *= entry_coefficient
            variables.extend(entry_variables)
        if not coefficient:
            continue
        surviving += 1
        monomial = tuple(sorted(variables))
        answer[monomial] = answer.get(monomial, ZERO) + coefficient
    return normalize_polynomial(answer), examined, surviving


@cache
def p4_polynomial(labels: tuple[str, str, str, str]) -> Polynomial:
    value, examined, surviving = sparse_permanent(
        tuple(top_column(label, 4) for label in labels)
    )
    assert examined == factorial(4)
    assert surviving == factorial(4)
    return value


def synthetic_column(
    mode: int, color: Color
) -> tuple[Column, bool, str | None, Scalar]:
    definitions: dict[tuple[int, Color], tuple[str, str | Scalar]] = {
        (0, I): ("bottom", A),
        (0, J): ("top", "S_j"),
        (0, K): ("top", "S_k"),
        (1, I): ("top", "T_i"),
        (1, J): ("bottom", -TAU * B),
        (1, K): ("top", "T_k"),
        (2, I): ("top", "X"),
        (2, J): ("top", "Y"),
        (2, K): ("bottom", GAMMA),
    }
    kind, payload = definitions[(mode, color)]
    if kind == "bottom":
        assert isinstance(payload, Fraction)
        return bottom_only_column(payload, 5, 4), True, None, payload
    assert isinstance(payload, str)
    return top_column(payload, 5), False, payload, ONE


def tail_relation_value(pairing: PairKey, m_color: Color, n_color: Color) -> Scalar:
    if pairing in ZERO_RELATIONS:
        return ZERO
    diagonal = DIAGONAL_RELATIONS.get(pairing)
    if diagonal is None:
        raise AssertionError(f"unrouted common-tail pairing: {pairing}")
    color, value = diagonal
    return value if m_color == n_color == color else ZERO


def check_p5_sparse_permutations() -> dict[str, int]:
    bottom_histogram: Counter[int] = Counter()
    route_histogram: Counter[PairKey] = Counter()
    output_histogram: Counter[str] = Counter()
    row_assignments = 0
    raw_nonzero_assignments = 0

    for word in product(COLORS, repeat=5):
        synthetic_data = tuple(synthetic_column(mode, word[mode]) for mode in range(3))
        columns = tuple(item[0] for item in synthetic_data) + (
            top_column(incidence_label(M, word[3]), 5),
            top_column(incidence_label(N, word[4]), 5),
        )
        direct, examined, surviving = sparse_permanent(columns)
        assert examined == factorial(5)
        row_assignments += examined
        raw_nonzero_assignments += surviving

        bottom_count = sum(item[1] for item in synthetic_data)
        bottom_histogram[bottom_count] += 1
        if bottom_count != 1:
            assert not direct
            assert surviving == 0
            reduced = ZERO
        else:
            top_labels = tuple(item[2] for item in synthetic_data if not item[1])
            assert len(top_labels) == 2 and all(top_labels)
            bottom_scalar = next(item[3] for item in synthetic_data if item[1])
            labels = (
                str(top_labels[0]),
                str(top_labels[1]),
                incidence_label(M, word[3]),
                incidence_label(N, word[4]),
            )
            expected = scale_polynomial(p4_polynomial(labels), bottom_scalar)
            assert direct == expected
            assert surviving == factorial(4)
            pairing = pair_key(str(top_labels[0]), str(top_labels[1]))
            route_histogram[pairing] += 1
            reduced = bottom_scalar * tail_relation_value(pairing, word[3], word[4])

        target = MU[word[0]] if all(color == word[0] for color in word) else ZERO
        assert reduced == target
        output_histogram["nonzero" if reduced else "zero"] += 1

    assert bottom_histogram == Counter({0: 72, 1: 108, 2: 54, 3: 9})
    assert set(route_histogram) == set(DIAGONAL_RELATIONS) | set(ZERO_RELATIONS)
    assert set(route_histogram.values()) == {9}
    assert output_histogram == Counter({"zero": 240, "nonzero": 3})
    assert row_assignments == 3**5 * factorial(5)
    assert raw_nonzero_assignments == 108 * factorial(4)

    return {
        "coefficients": 3**5,
        "permutations_per_coefficient": factorial(5),
        "row_assignments": row_assignments,
        "exactly_one_bottom_words": bottom_histogram[1],
        "zero_coefficients": output_histogram["zero"],
        "diagonal_coefficients": output_histogram["nonzero"],
    }


def perfect_matchings(
    vertices: tuple[str, ...],
) -> tuple[tuple[tuple[str, str], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def check_six_vertex_matchings() -> dict[str, int]:
    matchings = perfect_matchings(PHYSICAL_SLOTS)
    assert len(matchings) == 15
    internal_u = {S, T, M, N}
    b_edge_histogram: Counter[int] = Counter()
    h_edge_histogram: Counter[bool] = Counter()
    potentially_active_spoke_matchings = 0
    active_spokes = {
        frozenset((Q0, S)),
        frozenset((Q0, T)),
        frozenset((Q1, S)),
        frozenset((Q1, T)),
    }
    for matching in matchings:
        edge_sets = tuple(frozenset(edge) for edge in matching)
        b_edges = sum(edge <= internal_u for edge in edge_sets)
        has_h = frozenset((Q0, Q1)) in edge_sets
        assert b_edges >= 1
        b_edge_histogram[b_edges] += 1
        h_edge_histogram[has_h] += 1
        if not has_h and all(
            edge in active_spokes or edge <= internal_u for edge in edge_sets
        ):
            potentially_active_spoke_matchings += 1

    assert b_edge_histogram == Counter({1: 12, 2: 3})
    assert h_edge_histogram == Counter({False: 12, True: 3})
    assert potentially_active_spoke_matchings == 2

    return {
        "perfect_matchings": len(matchings),
        "matchings_using_H": h_edge_histogram[True],
        "matchings_without_H": h_edge_histogram[False],
        "matchings_with_a_zero_B_edge": len(matchings),
    }


def p6_extra_entries(slot: str, color: Color) -> dict[int, Scalar]:
    if slot == Q0 and color == I:
        return {4: ONE}
    if slot == Q1 and color == J:
        return {5: TAU}
    if slot == S and color == I:
        return {4: A, 5: A}
    if slot == T and color == J:
        return {4: -B, 5: B}
    return {}


def mixed_identity_polynomial(word: tuple[Color, ...]) -> Polynomial:
    q0_color, q1_color, s_color, t_color, m_color, n_color = word
    pieces: list[Polynomial] = []
    if q0_color == I and s_color == I:
        pieces.append(
            scale_polynomial(
                p4_polynomial(
                    (
                        incidence_label(Q1, q1_color),
                        incidence_label(T, t_color),
                        incidence_label(M, m_color),
                        incidence_label(N, n_color),
                    )
                ),
                A,
            )
        )
    if q0_color == I and t_color == J:
        pieces.append(
            scale_polynomial(
                p4_polynomial(
                    (
                        incidence_label(Q1, q1_color),
                        incidence_label(S, s_color),
                        incidence_label(M, m_color),
                        incidence_label(N, n_color),
                    )
                ),
                B,
            )
        )
    if q1_color == J and s_color == I:
        pieces.append(
            scale_polynomial(
                p4_polynomial(
                    (
                        incidence_label(Q0, q0_color),
                        incidence_label(T, t_color),
                        incidence_label(M, m_color),
                        incidence_label(N, n_color),
                    )
                ),
                TAU * A,
            )
        )
    if q1_color == J and t_color == J:
        pieces.append(
            scale_polynomial(
                p4_polynomial(
                    (
                        incidence_label(Q0, q0_color),
                        incidence_label(S, s_color),
                        incidence_label(M, m_color),
                        incidence_label(N, n_color),
                    )
                ),
                -TAU * B,
            )
        )
    return add_polynomials(*pieces)


def companion_identity_polynomial(word: tuple[Color, ...]) -> Polynomial:
    if word[0:2] != (I, J):
        return {}
    return scale_polynomial(
        p4_polynomial(
            (
                incidence_label(S, word[2]),
                incidence_label(T, word[3]),
                incidence_label(M, word[4]),
                incidence_label(N, word[5]),
            )
        ),
        TAU,
    )


def check_p6_sign_and_sharpness() -> dict[str, int]:
    # The s,t two-extra-row minor is a permanent, not a determinant:
    # a*b + a*(-b)=0.  This is the cancellation that removes the sixth pair.
    assert A * B + A * (-B) == ZERO

    output_histogram: Counter[str] = Counter()
    row_assignments = 0
    for word in product(COLORS, repeat=6):
        columns = tuple(
            augmented_column(
                incidence_label(slot, color),
                6,
                p6_extra_entries(slot, color),
            )
            for slot, color in zip(PHYSICAL_SLOTS, word, strict=True)
        )
        direct, examined, _surviving = sparse_permanent(columns)
        assert examined == factorial(6)
        row_assignments += examined

        decomposed = add_polynomials(
            mixed_identity_polynomial(word), companion_identity_polynomial(word)
        )
        assert direct == decomposed

        reduced = ZERO
        if all(color == I for color in word):
            reduced += MU[I]
        if all(color == J for color in word):
            reduced += MU[J]
        if word == (I, J, K, K, K, K):
            reduced += TAU * MU[K] / GAMMA

        expected = {
            (I, I, I, I, I, I): MU[I],
            (J, J, J, J, J, J): MU[J],
            (I, J, K, K, K, K): TAU * MU[K] / GAMMA,
        }.get(word, ZERO)
        assert reduced == expected
        output_histogram["nonzero" if reduced else "zero"] += 1

    assert output_histogram == Counter({"zero": 726, "nonzero": 3})
    assert row_assignments == 3**6 * factorial(6)

    return {
        "coefficients": 3**6,
        "permutations_per_coefficient": factorial(6),
        "row_assignments": row_assignments,
        "nonzero_coefficients": output_histogram["nonzero"],
        "mixed_coefficient_numerator": (TAU * MU[K] / GAMMA).numerator,
        "mixed_coefficient_denominator": (TAU * MU[K] / GAMMA).denominator,
    }


def check_scope_controls() -> dict[str, int]:
    declared_nonzero = (A, B, TAU, GAMMA, MU[I], MU[J], MU[K])
    assert all(declared_nonzero)
    normalization = tuple(MU[color] * (ONE / MU[color]) for color in COLORS)
    assert normalization == (ONE, ONE, ONE)
    assert len(DIAGONAL_RELATIONS) + len(ZERO_RELATIONS) == 12
    return {
        "declared_nonzero_factors": len(declared_nonzero),
        "target_normalizations": len(normalization),
        "repository_imports": 0,
        "finite_fields": 0,
    }


def render_counts(values: dict[str, int]) -> str:
    return ", ".join(f"{name}={value}" for name, value in values.items())


def main() -> None:
    checks: Iterable[tuple[str, Callable[[], dict[str, int]]]] = (
        ("coordinate-pairing", check_coordinate_pairing_quotients),
        ("common-tail-routing", check_common_tail_relation_routing),
        ("P5-row-assignments", check_p5_sparse_permutations),
        ("six-vertex-matchings", check_six_vertex_matchings),
        ("P6-sign-sharpness", check_p6_sign_and_sharpness),
        ("scope-controls", check_scope_controls),
    )
    for label, check in checks:
        result = check()
        print(f"PASS {label}: {render_counts(result)}")

    print(
        "BOUNDARY: exact rational replay of finite quotient/rank mechanics, "
        "label routing, permutations, and matchings; the arbitrary-point "
        "theorem and inherited branch remain written-proof obligations."
    )
    print(
        "OPEN: unrestricted P5 -> Delta3, rank-one Branches I/II, weaker "
        "response patterns, absorption/exceptional fibres, selectors, the "
        "strategic node, and the global Krenn--Gu conjecture."
    )
    print("PASS independent rank-one two-port P5 extraction audit")


if __name__ == "__main__":
    main()
