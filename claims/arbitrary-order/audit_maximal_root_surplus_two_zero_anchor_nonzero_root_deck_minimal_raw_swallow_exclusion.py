"""Independent support-census audit for GLS38.

This audit imports neither the primary verifier nor any third-party package.
It replaces coefficient charts and row reduction by exact bitmask support
logic for the rank-one diagonal, missing-row, transpose, and generator-support
leaves of the proof.
"""

from __future__ import annotations

from itertools import product


COLORS = tuple(range(3))
DIAGONAL = frozenset((color, color) for color in COLORS)


def vector_support(mask: int) -> frozenset[int]:
    return frozenset(color for color in COLORS if mask & (1 << color))


def outer_support(
    left: frozenset[int], right: frozenset[int]
) -> frozenset[tuple[int, int]]:
    return frozenset(product(left, right))


def rank_one_diagonal_census() -> dict[str, int]:
    """A nonzero decomposable diagonal support fixes one common colour."""

    examined = 0
    coordinate = 0
    for left_mask, right_mask in product(range(1, 8), repeat=2):
        examined += 1
        left = vector_support(left_mask)
        right = vector_support(right_mask)
        tensor = outer_support(left, right)
        if tensor <= DIAGONAL:
            assert left == right
            assert len(left) == 1
            coordinate += 1
    assert examined == 49
    assert coordinate == 3
    return {"examined": examined, "coordinate": coordinate}


def missing_row_census() -> dict[str, int]:
    """Audit the left-shore missing-row contradiction by support masks."""

    examined = 0
    forced = 0
    contradictions = 0
    for color in COLORS:
        axis = frozenset({color})
        for row in COLORS:
            if row == color:
                continue
            row_axis = frozenset({row})
            for b_0_mask, b_1_mask in product(range(8), repeat=2):
                examined += 1
                b_0 = vector_support(b_0_mask)
                b_1 = vector_support(b_1_mask)

                # If X(row) is nonzero, the a_s tensor Y term has no row
                # contribution because a_s is supported on color != row.
                diagonal_in_row = all(
                    not {(row, column) for column in shore if column != row}
                    for shore in (b_0, b_1)
                )
                assert diagonal_in_row == (b_0 <= row_axis and b_1 <= row_axis)
                if not diagonal_in_row:
                    continue
                forced += 1

                # Every linear combination d=lambda_0 b_1+lambda_1 b_0 has
                # support contained in the union.  It therefore cannot have
                # the nonzero support {color} pinned by q=a tensor d.
                combination_upper_bound = b_0 | b_1
                possible_pinned_support = any(
                    vector_support(d_mask) == axis
                    and vector_support(d_mask) <= combination_upper_bound
                    for d_mask in range(8)
                )
                assert not possible_pinned_support
                contradictions += 1
    assert examined == 384
    assert forced == contradictions == 24
    return {
        "examined": examined,
        "forced": forced,
        "contradictions": contradictions,
    }


def missing_column_census() -> dict[str, int]:
    """Audit the transposed right-shore missing-column contradiction."""

    examined = 0
    forced = 0
    contradictions = 0
    for color in COLORS:
        axis = frozenset({color})
        for column in COLORS:
            if column == color:
                continue
            column_axis = frozenset({column})
            for a_0_mask, a_1_mask in product(range(8), repeat=2):
                examined += 1
                a_0 = vector_support(a_0_mask)
                a_1 = vector_support(a_1_mask)
                diagonal_in_column = all(
                    not {(row, column) for row in shore if row != column}
                    for shore in (a_0, a_1)
                )
                assert diagonal_in_column == (
                    a_0 <= column_axis and a_1 <= column_axis
                )
                if not diagonal_in_column:
                    continue
                forced += 1
                combination_upper_bound = a_0 | a_1
                possible_pinned_support = any(
                    vector_support(d_mask) == axis
                    and vector_support(d_mask) <= combination_upper_bound
                    for d_mask in range(8)
                )
                assert not possible_pinned_support
                contradictions += 1
    assert examined == 384
    assert forced == contradictions == 24
    return {
        "examined": examined,
        "forced": forced,
        "contradictions": contradictions,
    }


def left_generator_support_census() -> dict[str, int]:
    """Once every X is on one row, diagonal generators lie in one line."""

    one_q = 0
    pair = 0
    for color in COLORS:
        axis = frozenset({color})
        pure = frozenset({(color, color)})
        supported_or_zero = (frozenset(), axis)
        all_supports = tuple(vector_support(mask) for mask in range(8))

        for a_s, x, y, b_s in product(
            supported_or_zero, supported_or_zero, all_supports, all_supports
        ):
            upper_bound = outer_support(a_s, y) | outer_support(x, b_s)
            assert upper_bound & DIAGONAL <= pure
            one_q += 1

        for x, y_prime, x_prime, y in product(
            supported_or_zero, all_supports, supported_or_zero, all_supports
        ):
            upper_bound = outer_support(x, y_prime) | outer_support(x_prime, y)
            assert upper_bound & DIAGONAL <= pure
            pair += 1

    assert one_q == pair == 768
    return {"one_q": one_q, "pair": pair}


def right_generator_support_census() -> dict[str, int]:
    """Transpose the support collapse: one column gives one diagonal line."""

    one_q = 0
    pair = 0
    for color in COLORS:
        axis = frozenset({color})
        pure = frozenset({(color, color)})
        supported_or_zero = (frozenset(), axis)
        all_supports = tuple(vector_support(mask) for mask in range(8))

        for a_s, x, y, b_s in product(
            all_supports, all_supports, supported_or_zero, supported_or_zero
        ):
            upper_bound = outer_support(a_s, y) | outer_support(x, b_s)
            assert upper_bound & DIAGONAL <= pure
            one_q += 1

        for x, y_prime, x_prime, y in product(
            all_supports, supported_or_zero, all_supports, supported_or_zero
        ):
            upper_bound = outer_support(x, y_prime) | outer_support(x_prime, y)
            assert upper_bound & DIAGONAL <= pure
            pair += 1

    assert one_q == pair == 768
    return {"one_q": one_q, "pair": pair}


def shore_profile_census() -> dict[str, int]:
    """Exhaust the discrete residual-shore ranks after q is nonzero."""

    profiles = tuple(product(range(3), repeat=2))
    zero_shore = tuple(profile for profile in profiles if 0 in profile)
    positive_low = tuple(
        profile
        for profile in profiles
        if 0 not in profile and min(profile) == 1
    )
    two_two = tuple(profile for profile in profiles if profile == (2, 2))
    assert len(profiles) == 9
    assert len(zero_shore) == 5
    assert len(positive_low) == 3
    assert len(two_two) == 1
    assert len(zero_shore) + len(positive_low) + len(two_two) == len(profiles)
    return {
        "total": len(profiles),
        "zero": len(zero_shore),
        "positive_low": len(positive_low),
        "two_two": len(two_two),
        "covered": len(profiles),
    }


def main() -> None:
    diagonal = rank_one_diagonal_census()
    left_missing = missing_row_census()
    right_missing = missing_column_census()
    left_generators = left_generator_support_census()
    right_generators = right_generator_support_census()
    profiles = shore_profile_census()
    print("GLS38 independent no-import support audit: PASS")
    print("  rank-one diagonal support:", diagonal)
    print("  left missing row:", left_missing)
    print("  right missing column:", right_missing)
    print("  left generator support:", left_generators)
    print("  right generator support:", right_generators)
    print("  shore profiles:", profiles)
    print("  nonzero-q rank-three full swallow: EMPTY (GLS37 supplies (2,2))")


if __name__ == "__main__":
    main()
