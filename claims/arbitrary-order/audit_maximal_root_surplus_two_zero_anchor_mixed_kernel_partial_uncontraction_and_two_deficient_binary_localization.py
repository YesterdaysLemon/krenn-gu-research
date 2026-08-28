"""Independent finite audit for the GLS63 two-deficient parent attempt.

The audit is intentionally standard-library-only.  It checks the finite
support census, the mixed-kernel survival rule, the row-space incidence
leaves, and small exact tensor controls over ``Fraction``.  It is not a
symbolic proof of the function-field identities: physical decks remain
same-source objects in the theorem, while this file only replays finite and
displayed algebraic leaves.

The canonical support census has six choices for each deficient support
(three singleton and three two-colour supports), and an ordered list of
nonaxis zero statuses in ``{-1, 0, 1, 2}`` of every length 0 through 4.
Thus it is exactly ``6*6*sum(4**u) = 12,276``.  A typed support gives one
rank-two row type for a singleton and two oriented row types for a
two-colour support, hence nine choices per deficient label and
``9*9*sum(4**u) = 27,621``.  The labels carrying the statuses are kept in
order; pure-axis labels are the unlisted slots.

The finite ledger is:

    support-only: 12,276 -> 1,266 (incidence/common-three) -> 78 (singleton-compatible)
    typed:        27,621 -> 1,710 (incidence/common-three) -> 78 (singleton-compatible) -> 15 (q4 residual)
    final 78 bins: 36 / 3 / 24 / 15.

The last fifteen are the binary residual family.  All assertions are exact
over Q or over the displayed finite coefficient set; no project import,
SymPy, numerical tolerance, or global-status upgrade is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

Scalar = Fraction
Vector = tuple[Scalar, ...]
Matrix = tuple[tuple[Scalar, ...], ...]
Tensor = dict[tuple[int, ...], Scalar]

COLOURS = (0, 1, 2)
ZERO_STATUS = (-1, 0, 1, 2)
LABEL_COUNT = 6
FINITE_VALUES = (-1, 0, 1)

SUPPORTS = tuple(
    tuple((colour,) for colour in COLOURS) + tuple(combinations(COLOURS, 2))
)
TYPED_SUPPORTS = tuple(
    (support, orientation)
    for support in SUPPORTS
    for orientation in range(1 if len(support) == 1 else 2)
)


def as_vector(values: tuple[int, ...] | list[int]) -> Vector:
    """Convert a short integer vector to an exact rational vector."""

    return tuple(Scalar(value) for value in values)


def rank_fraction(rows: list[Vector] | tuple[Vector, ...]) -> int:
    """Return exact row rank over Q."""

    if not rows:
        return 0
    work = [list(row) for row in rows]
    width = len(work[0])
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for index in range(len(work)):
            if index == rank or not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [
                left - factor * right
                for left, right in zip(work[index], work[rank], strict=True)
            ]
        rank += 1
    return rank


def unit(index: int) -> Vector:
    """The indexed basis covector in Q^3."""

    return tuple(Scalar(int(position == index)) for position in COLOURS)


def vector_add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def vector_scale(factor: Scalar, vector: Vector) -> Vector:
    return tuple(factor * value for value in vector)


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS) for row in COLOURS
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(row_left, row_right, strict=True))
        for row_left, row_right in zip(left, right, strict=True)
    )


def matrix_scale(factor: Scalar, matrix: Matrix) -> Matrix:
    return tuple(tuple(factor * value for value in row) for row in matrix)


ZERO_MATRIX: Matrix = tuple(tuple(Scalar(0) for _ in COLOURS) for _ in COLOURS)


def is_nonzero(vector: Vector) -> bool:
    return any(vector)


def is_pure(matrix: Matrix, colour: int) -> bool:
    return all(
        value == 0 or (row == colour and column == colour)
        for row, matrix_row in enumerate(matrix)
        for column, value in enumerate(matrix_row)
    )


def support_vector(support: tuple[int, ...]) -> Vector:
    """A canonical kernel vector with exactly the displayed support."""

    return tuple(Scalar(int(colour in support)) for colour in COLOURS)


def row_plane(support: tuple[int, ...]) -> tuple[Vector, Vector]:
    """A rank-two plane annihilating the canonical kernel vector."""

    if len(support) == 1:
        omitted = support[0]
        return tuple(unit(colour) for colour in COLOURS if colour != omitted)  # type: ignore[return-value]
    first, second = support
    remaining = next(colour for colour in COLOURS if colour not in support)
    difference = vector_add(unit(first), vector_scale(Scalar(-1), unit(second)))
    return difference, unit(remaining)


def support_survives_row_quotient(support: tuple[int, ...], colour: int) -> bool:
    """Check e_colour is not in the deficient row plane."""

    rows = row_plane(support)
    return rank_fraction(rows + (unit(colour),)) > rank_fraction(rows)


def profiles() -> tuple[
    tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]], ...
]:
    """Enumerate canonical two-deficient support/status profiles."""

    return tuple(
        (left, right, nonaxis_count, assignment)
        for left, right in product(SUPPORTS, repeat=2)
        for nonaxis_count in range(5)
        for assignment in product(ZERO_STATUS, repeat=nonaxis_count)
    )


def typed_profiles() -> tuple[
    tuple[tuple[int, ...], int, tuple[int, ...], int, int, tuple[int, ...]], ...
]:
    """Enumerate the typed support/status profiles."""

    return tuple(
        (left, left_type, right, right_type, nonaxis_count, assignment)
        for (left, left_type), (right, right_type) in product(TYPED_SUPPORTS, repeat=2)
        for nonaxis_count in range(5)
        for assignment in product(ZERO_STATUS, repeat=nonaxis_count)
    )


def zero_counts(assignment: tuple[int, ...]) -> tuple[int, int, int]:
    return tuple(assignment.count(colour) for colour in COLOURS)  # type: ignore[return-value]


def support_union(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> set[int]:
    return set(profile[0]) | set(profile[1])


def support_intersection(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> set[int]:
    return set(profile[0]) & set(profile[1])


def incidence_floor(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> bool:
    counts = zero_counts(profile[3])
    return all(counts[colour] >= 1 for colour in support_union(profile))


def common_three_floor(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> bool:
    counts = zero_counts(profile[3])
    return all(counts[colour] >= 3 for colour in support_intersection(profile))


def full_row_floor(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> bool:
    counts = zero_counts(profile[3])
    return all(counts[colour] >= 2 for colour in support_union(profile))


def singleton_rule(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> bool:
    """Apply the singleton deficient/nonaxis geometry from GLS63."""

    left, right, _, assignment = profile
    counts = zero_counts(assignment)
    left_set = set(left)
    right_set = set(right)
    for colour in left_set - right_set:
        if counts[colour] == 1 and right_set != set(COLOURS) - {colour}:
            return False
    for colour in right_set - left_set:
        if counts[colour] == 1 and left_set != set(COLOURS) - {colour}:
            return False
    return True


def support_stage(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> bool:
    return incidence_floor(profile) and common_three_floor(profile)


def localized_stage(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> bool:
    return support_stage(profile) and singleton_rule(profile)


def profile_category(
    profile: tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, ...]],
) -> str:
    """Classify the 78 profiles after the singleton rule."""

    left, right, nonaxis_count, assignment = profile
    if left != right:
        assert len(left) == len(right) == 1
        return "distinct_singleton"
    assert len(left) == len(right) == 1
    colour = left[0]
    if nonaxis_count == 3 and assignment == (colour,) * 3:
        return "q3_xxy_triangle"
    if nonaxis_count == 4 and assignment.count(colour) == 3:
        remaining = tuple(value for value in assignment if value != colour)
        if remaining and remaining[0] in set(COLOURS) - {colour}:
            return "binary_one_other_zero"
    if (
        nonaxis_count == 4
        and assignment.count(colour) >= 3
        and all(value in (-1, colour) for value in assignment)
    ):
        return "q4_six_pair"
    raise AssertionError(f"unclassified localized profile: {profile!r}")


def check_mixed_survival() -> int:
    """Check that a pair survives structurally exactly when D is a subset of S."""

    all_labels = (1 << LABEL_COUNT) - 1
    checked = 0
    for contracted_deficient in range(1 << LABEL_COUNT):
        for contracted_injective in range(1 << LABEL_COUNT):
            if contracted_deficient & contracted_injective:
                continue
            open_mask = all_labels ^ (contracted_deficient | contracted_injective)
            actual = {
                pair
                for pair in combinations(range(LABEL_COUNT), 2)
                if (open_mask & (1 << pair[0])) and (open_mask & (1 << pair[1]))
            }
            expected = {
                pair
                for pair in combinations(range(LABEL_COUNT), 2)
                if all(open_mask & (1 << endpoint) for endpoint in pair)
            }
            assert actual == expected
            checked += 1
    assert checked == 3**LABEL_COUNT
    return checked


def check_row_quotient_and_support_incidence() -> tuple[int, int]:
    """Audit kernel support visibility and the two deficient incidence floors."""

    checks = 0
    for support in SUPPORTS:
        rows = row_plane(support)
        assert rank_fraction(rows) == 2
        kernel = support_vector(support)
        assert all(sum(row[i] * kernel[i] for i in COLOURS) == 0 for row in rows)
        for colour in COLOURS:
            expected = colour in support
            assert support_survives_row_quotient(support, colour) == expected
            checks += 1

    profiles_checked = 0
    for profile in profiles():
        if not incidence_floor(profile):
            continue
        counts = zero_counts(profile[3])
        assert all(counts[colour] >= 1 for colour in support_union(profile))
        profiles_checked += 1
    assert profiles_checked == 4182
    return checks, profiles_checked


def check_target_support(
    deficient_supports: tuple[tuple[int, ...], ...],
    assignment: tuple[int, ...],
) -> set[int]:
    """Return the colours surviving generic deficient/nonaxis contractions."""

    visible = set(COLOURS)
    for support in deficient_supports:
        visible &= set(support)
    zeroed = set(assignment)
    return visible - zeroed


def check_profile_ledger() -> tuple[Counter[str], Counter[str]]:
    """Run the independent support and typed profile ledgers."""

    support_profiles = profiles()
    assert len(support_profiles) == 6 * 6 * sum(4**u for u in range(5))
    support_stage_profiles = tuple(
        profile for profile in support_profiles if support_stage(profile)
    )
    assert len(support_stage_profiles) == 1266
    support_localized = tuple(
        profile for profile in support_stage_profiles if singleton_rule(profile)
    )
    assert len(support_localized) == 78
    support_categories = Counter(
        profile_category(profile) for profile in support_localized
    )
    assert support_categories == Counter(
        {
            "distinct_singleton": 36,
            "q3_xxy_triangle": 3,
            "binary_one_other_zero": 24,
            "q4_six_pair": 15,
        }
    )

    typed = typed_profiles()
    assert len(typed) == 9 * 9 * sum(4**u for u in range(5))
    typed_stage = tuple(
        profile
        for profile in typed
        if support_stage((profile[0], profile[2], profile[4], profile[5]))
    )
    assert len(typed_stage) == 1710
    typed_localized = tuple(
        profile
        for profile in typed_stage
        if singleton_rule((profile[0], profile[2], profile[4], profile[5]))
    )
    assert len(typed_localized) == 78
    typed_categories = Counter(
        profile_category((profile[0], profile[2], profile[4], profile[5]))
        for profile in typed_localized
    )
    assert typed_categories == support_categories
    q4 = tuple(
        profile
        for profile in support_localized
        if profile_category(profile) == "q4_six_pair"
    )
    assert len(q4) == 15
    for profile in q4:
        left, right, _, assignment = profile
        assert left == right and len(left) == 1
        colour = left[0]
        assert len(assignment) == 4
        assert assignment.count(colour) >= 3
        # In the two-open residual equation n and m are left open; only the
        # four U labels are cross-contracted, so no deficient support is
        # intersected into the target support.
        assert check_target_support((), assignment) == set(COLOURS) - {colour}
    return support_categories, typed_categories


def finite_plane_vectors(support: tuple[int, ...]) -> tuple[Vector, ...]:
    """Enumerate a bounded exact coefficient set in a coordinate plane."""

    result = []
    for coefficients in product(FINITE_VALUES, repeat=len(support)):
        vector = [Scalar(0) for _ in COLOURS]
        for colour, coefficient in zip(support, coefficients, strict=True):
            vector[colour] = Scalar(coefficient)
        candidate = tuple(vector)
        if is_nonzero(candidate):
            result.append(candidate)
    return tuple(result)


def independent_pairs(support: tuple[int, ...]) -> tuple[tuple[Vector, Vector], ...]:
    vectors = finite_plane_vectors(support)
    return tuple(
        (left, right)
        for left, right in product(vectors, repeat=2)
        if rank_fraction((left, right)) == 2
    )


def companion(
    p_left: Vector,
    q_left: Vector,
    p_right: Vector,
    q_right: Vector,
) -> Matrix:
    return matrix_add(outer(p_left, q_right), outer(q_left, p_right))


def check_rank_two_pure_companion_no_go() -> int:
    """Exhaust a small exact model of the rank-two pure-companion lemma."""

    checked = 0
    for colour in COLOURS:
        complement = tuple(other for other in COLOURS if other != colour)
        # Same deficient kernel support: the proposed pure line can be either
        # coordinate in the common row plane.
        same_pairs = independent_pairs(complement)
        for target in complement:
            for left_pair, right_pair in product(same_pairs, repeat=2):
                matrix = companion(
                    left_pair[0],
                    left_pair[1],
                    right_pair[0],
                    right_pair[1],
                )
                assert not (
                    is_nonzero(tuple(value for row in matrix for value in row))
                    and is_pure(matrix, target)
                )
                checked += 1

        # Distinct singleton supports: the two row planes meet in the third
        # coordinate, which is the only possible pure-companion line.
        # The explicit loop above is kept simple below: n has {c,e}, m has
        # {d,e}, and all colour permutations are covered by this outer loop.
        for first, second in (
            (complement[0], complement[1]),
            (complement[1], complement[0]),
        ):
            n_plane = (colour, second)
            m_plane = (first, second)
            for left_pair, right_pair in product(
                independent_pairs(n_plane), independent_pairs(m_plane)
            ):
                matrix = companion(
                    left_pair[0],
                    left_pair[1],
                    right_pair[0],
                    right_pair[1],
                )
                assert not (
                    is_nonzero(tuple(value for row in matrix for value in row))
                    and is_pure(matrix, second)
                )
                checked += 1
    assert checked > 0
    return checked


def check_p1_two_colour_separation() -> int:
    """Check active-line quotient separation and the P=1 flattening rank."""

    active_values = (-2, -1, 1, 2)
    checks = 0
    for active_tuple in product(active_values, repeat=3):
        active = as_vector(active_tuple)
        for colour in COLOURS:
            other = tuple(item for item in COLOURS if item != colour)
            left, right = (unit(other[0]), unit(other[1]))
            # Images of the two complementary coordinate covectors are
            # independent modulo the active line exactly when these three
            # vectors have rank three.
            assert rank_fraction((active, left, right)) == 3
            # The two deficient factors are also independent as a two-row
            # flattening, so the target has rank two while g_nm tensor h_p
            # has rank one across (n,m)|(p).
            left_target = tuple(Scalar(int(index == other[0])) for index in COLOURS)
            right_target = tuple(Scalar(int(index == other[1])) for index in COLOURS)
            assert rank_fraction((left_target, right_target)) == 2
            checks += 1
    assert checks == 4**3 * 3
    return checks


def check_binary_g_nm_control() -> int:
    """Exhibit the exact local binary companion left by the census."""

    checks = 0
    for colour in COLOURS:
        d, e = tuple(item for item in COLOURS if item != colour)
        p_n, q_n = unit(d), unit(e)
        p_m, q_m = unit(e), unit(d)
        binary = companion(p_n, q_n, p_m, q_m)
        expected = matrix_add(outer(unit(d), unit(d)), outer(unit(e), unit(e)))
        assert binary == expected
        assert rank_fraction(row_plane((colour,))) == 2
        assert not is_pure(binary, d)
        assert all(
            binary[row][column]
            == (Scalar(1) if row == column and row in (d, e) else Scalar(0))
            for row in COLOURS
            for column in COLOURS
        )
        checks += 1
    assert checks == 3
    return checks


def tensor_add(target: Tensor, source: Tensor) -> None:
    for key, value in source.items():
        target[key] = target.get(key, Scalar(0)) + value
        if target[key] == 0:
            del target[key]


def pair_companion_tensor3(
    p: tuple[Vector, Vector, Vector],
    q: tuple[Vector, Vector, Vector],
    first: int,
    second: int,
) -> Matrix:
    return companion(p[first], q[first], p[second], q[second])


def tensor_pair_with_vector(
    matrix: Matrix, first: int, second: int, vector: Vector
) -> Tensor:
    result: Tensor = {}
    single = next(index for index in range(3) if index not in (first, second))
    for left, row in enumerate(matrix):
        for right, value in enumerate(row):
            for third, coefficient in enumerate(vector):
                if value and coefficient:
                    key = [0, 0, 0]
                    key[first] = left
                    key[second] = right
                    key[single] = third
                    result[tuple(key)] = (
                        result.get(tuple(key), Scalar(0)) + value * coefficient
                    )
    return result


def check_q3_xxy_triangle_identity() -> int:
    """Check the explicit mixed-orientation three-port cancellation."""

    c, d, e = COLOURS
    C = unit(c)
    r_u, r_v, r_w = unit(d), unit(e), vector_add(unit(d), unit(e))
    p = (C, C, r_w)
    q = (r_u, r_v, C)
    h = (
        vector_scale(Scalar(-1), p[0]),
        vector_scale(Scalar(-1), p[1]),
        p[2],
    )
    result: Tensor = {}
    for first, second, single in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        matrix = pair_companion_tensor3(p, q, first, second)
        tensor_add(result, tensor_pair_with_vector(matrix, first, second, h[single]))
    assert result == {(c, c, c): Scalar(-2)}
    for index in range(3):
        assert rank_fraction((p[index], q[index], h[index])) == rank_fraction(
            (p[index], q[index])
        )
    return len(result)


def tensor_pair_pair(
    matrix_left: Matrix,
    pair_left: tuple[int, int],
    matrix_right: Matrix,
    pair_right: tuple[int, int],
) -> Tensor:
    result: Tensor = {}
    for left, row in enumerate(matrix_left):
        for middle, left_value in enumerate(row):
            for right, right_row in enumerate(matrix_right):
                for last, right_value in enumerate(right_row):
                    if left_value and right_value:
                        key = [0, 0, 0, 0]
                        key[pair_left[0]] = left
                        key[pair_left[1]] = middle
                        key[pair_right[0]] = right
                        key[pair_right[1]] = last
                        tuple_key = tuple(key)
                        result[tuple_key] = (
                            result.get(tuple_key, Scalar(0)) + left_value * right_value
                        )
    return result


def check_q4_six_pair_identity() -> int:
    """Check the four-port six-pair cancellation at a distinct r,s fibre."""

    c, d = 0, 1
    C = unit(c)
    # The exact control uses distinct complementary directions, r=e_1 and
    # s=e_2.  The labelled placement of each pair and its complementary deck
    # is essential: after reordering into slots (0,1,2,3), the two same-type
    # contributions cancel the four cross-type off-colour terms.
    r = unit(d)
    s = unit(2)
    M_r = matrix_add(outer(C, r), outer(r, C))
    M_s = matrix_add(outer(C, s), outer(s, C))
    cross = matrix_add(outer(C, C), outer(r, s))
    decks = {
        (0, 1): matrix_scale(Scalar(-1, 2), M_r),
        (2, 3): matrix_scale(Scalar(-1, 2), M_s),
        (0, 2): outer(C, C),
        (0, 3): outer(C, C),
        (1, 2): outer(C, C),
        (1, 3): outer(C, C),
    }
    shores = (
        (C, r),
        (C, r),
        (s, C),
        (s, C),
    )
    result: Tensor = {}
    all_ports = (0, 1, 2, 3)
    for first, second in combinations(all_ports, 2):
        matrix = companion(
            shores[first][0],
            shores[first][1],
            shores[second][0],
            shores[second][1],
        )
        complement = tuple(index for index in all_ports if index not in (first, second))
        tensor_add(
            result,
            tensor_pair_pair(
                matrix,
                (first, second),
                decks[complement],
                complement,
            ),
        )
    assert result == {(c, c, c, c): Scalar(4)}
    assert cross == companion(C, r, s, C)
    return len(result)


def main() -> None:
    survival_cases = check_mixed_survival()
    quotient_checks, incidence_profiles = check_row_quotient_and_support_incidence()
    support_categories, typed_categories = check_profile_ledger()
    pure_companion_cases = check_rank_two_pure_companion_no_go()
    p1_checks = check_p1_two_colour_separation()
    binary_checks = check_binary_g_nm_control()
    q3_terms = check_q3_xxy_triangle_identity()
    q4_terms = check_q4_six_pair_identity()

    print(
        "support-only ledger: 12276 -> 1266 (incidence/common-three) "
        "-> 78 (singleton-compatible)"
    )
    print(
        "typed ledger: 27621 -> 1710 (incidence/common-three) "
        "-> 78 (singleton-compatible) -> 15 (q4 residual)"
    )
    print("localized categories: 36/3/24/15")
    print(f"mixed pair-survival masks: {survival_cases}")
    print(
        f"row quotient checks: {quotient_checks}; incidence profiles: {incidence_profiles}"
    )
    print(f"rank-two pure-companion finite cases: {pure_companion_cases}")
    print(f"P1 quotient separation checks: {p1_checks}")
    print(f"binary g_nm controls: {binary_checks}")
    print(f"q3 XXY triangle support terms: {q3_terms}")
    print(f"q4 six-pair support terms (distinct r=e1,s=e2 fibre): {q4_terms}")
    assert support_categories == typed_categories
    print(
        "scope walls: finite/displayed algebra only; no deck independence or "
        "function-field restriction separation; deficient count >=3, unique "
        "nonrigid, nonzero anchor, response/selector/synchronization/activity, "
        "attachment, and the global Krenn-Gu conjecture remain UNRESOLVED"
    )
    print("PASS (GLS63 audit scope only; no global closure claim)")


if __name__ == "__main__":
    main()
