"""Exact audit of the two-deficient binary-localization branch.

This is a bounded primary *audit*, not a proof of the Krenn--Gu
conjecture.  It replays the finite support/status census supplied by the
arbitrary-open partial-uncontraction hierarchy and checks a few small
linear-algebra controls with exact SymPy arithmetic.  In particular, it
does not construct a source tensor, a physical deck, a response, or a
selector, and it does not promote any profile count to source integrability.

The first census treats the two deficient kernel supports as ordered
abstract supports.  The second census types those supports as the three
rank possibilities used by the branch:

* three singleton rank-two supports;
* three size-two rank-one supports, with their complementary readout;
* three size-two rank-two supports.

For each of the four remaining labels, ``-1`` means no identically zero
cross coordinate and ``0, 1, 2`` record its one allowed zero coordinate.
The finite ledger is intentionally generated directly from these choices;
the assertions do not manufacture the requested totals by orbit weighting.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product

import sympy as sp

COLOURS = (0, 1, 2)
ZERO_STATUSES = (-1, *COLOURS)
SUPPORTS = tuple(
    frozenset(pair)
    for support_size in (1, 2)
    for pair in combinations(COLOURS, support_size)
)


@dataclass(frozen=True)
class DeficientMap:
    """The support/rank typing retained by the two-deficient audit."""

    support: frozenset[int]
    kind: str
    readout: int | None = None


SupportProfile = tuple[
    frozenset[int],
    frozenset[int],
    int,
    tuple[int, ...],
]
TypedProfile = tuple[DeficientMap, DeficientMap, int, tuple[int, ...]]

RANK_TWO_SUPPORT_ONE = "rank2_support1"
RANK_ONE_SUPPORT_TWO = "rank1_support2"
RANK_TWO_SUPPORT_TWO = "rank2_support2"


def zero_counts(assignment: tuple[int, ...]) -> tuple[int, ...]:
    """Return the three disjoint ``E_c`` cardinalities."""

    return tuple(assignment.count(colour) for colour in COLOURS)


def floors_hold(
    left_support: frozenset[int],
    right_support: frozenset[int],
    counts: tuple[int, ...],
) -> bool:
    """Apply the open-set visibility floors used by the parent branch."""

    union = left_support | right_support
    intersection = left_support & right_support
    return all(counts[colour] >= 1 for colour in union) and all(
        counts[colour] >= 3 for colour in intersection
    )


def support_only_profiles() -> tuple[SupportProfile, ...]:
    """Enumerate the ordered support/status census before map typing."""

    return tuple(
        (left, right, pure_count, assignment)
        for left in SUPPORTS
        for right in SUPPORTS
        for pure_count in range(5)
        for assignment in product(ZERO_STATUSES, repeat=4 - pure_count)
    )


def check_support_only_census() -> dict[str, int]:
    """Check 12,276 ordered profiles and the 1,266 floor survivors."""

    profiles = support_only_profiles()
    expected_total = 36 * sum(4 ** (4 - pure_count) for pure_count in range(5))
    assert len(profiles) == expected_total == 12_276

    floor_survivors = tuple(
        profile
        for profile in profiles
        if floors_hold(profile[0], profile[1], zero_counts(profile[3]))
    )
    assert len(floor_survivors) == 1_266
    return {
        "support_only_ordered_total": len(profiles),
        "support_only_after_incidence_floors": len(floor_survivors),
    }


def typed_options() -> tuple[DeficientMap, ...]:
    """Return exactly the nine typed deficient-map choices."""

    singleton_rank_two = tuple(
        DeficientMap(frozenset((colour,)), RANK_TWO_SUPPORT_ONE) for colour in COLOURS
    )
    size_two_rank_one = tuple(
        DeficientMap(
            frozenset(pair),
            RANK_ONE_SUPPORT_TWO,
            next(colour for colour in COLOURS if colour not in pair),
        )
        for pair in combinations(COLOURS, 2)
    )
    size_two_rank_two = tuple(
        DeficientMap(frozenset(pair), RANK_TWO_SUPPORT_TWO)
        for pair in combinations(COLOURS, 2)
    )
    return singleton_rank_two + size_two_rank_one + size_two_rank_two


TYPED_OPTIONS = typed_options()


def typed_profiles() -> tuple[TypedProfile, ...]:
    """Enumerate typed ordered maps and the four remaining labels."""

    return tuple(
        (left, right, pure_count, assignment)
        for left in TYPED_OPTIONS
        for right in TYPED_OPTIONS
        for pure_count in range(5)
        for assignment in product(ZERO_STATUSES, repeat=4 - pure_count)
    )


def singleton_companion_rule(profile: TypedProfile) -> bool:
    """Apply the exact singleton ``E_c`` companion typing rule.

    If ``E_c`` is a singleton in the right support, the left map must be the
    rank-one size-two map whose readout is ``c``; the symmetric condition is
    imposed with left and right exchanged.
    """

    left, right, _, assignment = profile
    counts = zero_counts(assignment)

    for colour in right.support:
        if counts[colour] == 1 and not (
            left.kind == RANK_ONE_SUPPORT_TWO and left.readout == colour
        ):
            return False
    for colour in left.support:
        if counts[colour] == 1 and not (
            right.kind == RANK_ONE_SUPPORT_TWO and right.readout == colour
        ):
            return False
    return True


def check_typed_census() -> tuple[dict[str, int], tuple[TypedProfile, ...]]:
    """Check 27,621 typed profiles, then the 1,710 and 78 reductions."""

    kind_counts = Counter(option.kind for option in TYPED_OPTIONS)
    assert len(TYPED_OPTIONS) == 9
    assert kind_counts == Counter(
        {
            RANK_TWO_SUPPORT_ONE: 3,
            RANK_ONE_SUPPORT_TWO: 3,
            RANK_TWO_SUPPORT_TWO: 3,
        }
    )

    profiles = typed_profiles()
    assert len(profiles) == 9 * 9 * sum(4 ** (4 - pure) for pure in range(5))
    assert len(profiles) == 27_621

    floor_survivors = tuple(
        profile
        for profile in profiles
        if floors_hold(
            profile[0].support,
            profile[1].support,
            zero_counts(profile[3]),
        )
    )
    assert len(floor_survivors) == 1_710

    companion_survivors = tuple(
        profile for profile in floor_survivors if singleton_companion_rule(profile)
    )
    assert len(companion_survivors) == 78
    # The singleton rule has removed every rank-one/rank-two-support-two
    # typing in the residual cell; the remaining maps are pure-coordinate
    # rank-two maps with singleton support.
    assert all(
        left.kind == right.kind == RANK_TWO_SUPPORT_ONE
        for left, right, _, _ in companion_survivors
    )
    return (
        {
            "typed_options_total": len(TYPED_OPTIONS),
            "typed_profiles_total": len(profiles),
            "typed_after_incidence_floors": len(floor_survivors),
            "typed_after_singleton_companion_rule": len(companion_survivors),
        },
        companion_survivors,
    )


def check_refinement_partition(
    survivors: tuple[TypedProfile, ...],
) -> dict[str, int]:
    """Partition the 78 survivors into the requested four refinements."""

    distinct_supports = tuple(
        profile for profile in survivors if profile[0].support != profile[1].support
    )
    same_support_p1 = tuple(
        profile
        for profile in survivors
        if profile[0].support == profile[1].support and profile[2] == 1
    )
    same_support_p0_other_zero = tuple(
        profile
        for profile in survivors
        if profile[0].support == profile[1].support
        and profile[2] == 0
        and any(
            zero_counts(profile[3])[colour] == 1
            for colour in COLOURS
            if colour not in profile[0].support
        )
    )
    residual = tuple(
        profile
        for profile in survivors
        if profile not in distinct_supports
        and profile not in same_support_p1
        and profile not in same_support_p0_other_zero
    )

    assert len(distinct_supports) == 36
    assert len(same_support_p1) == 3
    assert len(same_support_p0_other_zero) == 24
    assert len(residual) == 15
    assert (
        len(distinct_supports)
        + len(same_support_p1)
        + len(same_support_p0_other_zero)
        + len(residual)
        == len(survivors)
        == 78
    )

    assert all(
        len(profile[0].support) == len(profile[1].support) == 1
        and profile[0].support.isdisjoint(profile[1].support)
        for profile in distinct_supports
    )
    assert all(profile[2] == 1 for profile in same_support_p1)
    assert all(
        profile[0].support == profile[1].support and profile[2] == 0
        for profile in same_support_p0_other_zero + residual
    )
    return {
        "refinement_distinct_supports": len(distinct_supports),
        "refinement_same_support_P1": len(same_support_p1),
        "refinement_same_support_P0_assigned_other_zero": len(
            same_support_p0_other_zero
        ),
        "refinement_final_residual": len(residual),
    }


def coordinate(dimension: int, index: int) -> sp.Matrix:
    """Return an exact coordinate column."""

    return sp.eye(dimension)[:, index]


def quotient_map(active: sp.Matrix) -> sp.Matrix:
    """Return a rank-two quotient map annihilating a nonzero active line."""

    assert active.shape == (3, 1)
    pivot = next(
        (index for index, value in enumerate(active) if value != 0),
        None,
    )
    assert pivot is not None
    rows = []
    for index in range(3):
        if index == pivot:
            continue
        row = sp.zeros(1, 3)
        row[0, index] = active[pivot]
        row[0, pivot] = -active[index]
        rows.append(row)
    result = sp.Matrix.vstack(*rows)
    assert result * active == sp.zeros(2, 1)
    assert result.rank() == 2
    return result


def check_p1_flattening() -> dict[str, int]:
    """Check exact target separation after one active-line quotient."""

    active = sp.Matrix((1, 2, 3))
    quotient = quotient_map(active)
    # In the P=1 residual, the supported zero colour (colour 0 here) is
    # killed by U=E_0.  Only the two complementary target colours remain.
    targets = sp.Matrix.hstack(
        *(
            sp.kronecker_product(
                coordinate(3, colour),
                quotient * coordinate(3, colour),
            )
            for colour in (1, 2)
        )
    )
    assert quotient * active == sp.zeros(2, 1)
    assert all(quotient * coordinate(3, colour) != sp.zeros(2, 1) for colour in COLOURS)
    # The first tensor factor is a distinct coordinate block, so the two
    # surviving target columns have flattening rank two.
    assert targets.rank() == 2
    return {"P1_flattening_target_rank": targets.rank()}


def check_two_rank2_pure_companion_no_go() -> dict[str, int]:
    """Run a fixed-plane coefficient sanity check for a pure companion.

    In a chosen two-dimensional visible-plane normal form, put the two deck
    pairs into the columns of invertible matrices ``N`` and ``M``.  Their
    companion is ``N J M.T`` with ``J`` the swap matrix, hence its determinant
    is the nonzero product ``-det(N) det(M)``.  A pure nonzero tensor has
    matrix rank one, so it cannot be this fixed-plane coefficient model.  The
    arbitrary-probe-map quotient argument belongs to the owning theorem; the
    symbolic identity and integer instance here are only local sanity checks.
    """

    a, b, c, d, u, v, w, z = sp.symbols("a b c d u v w z")
    left = sp.Matrix(((a, c), (b, d)))
    right = sp.Matrix(((u, w), (v, z)))
    swap = sp.Matrix(((0, 1), (1, 0)))
    companion = left * swap * right.T
    assert sp.factor(companion.det() + left.det() * right.det()) == 0
    assert sp.factor(companion.det()) != 0

    left_instance = sp.Matrix(((1, 2), (3, 5)))
    right_instance = sp.Matrix(((2, 1), (4, 3)))
    instance = left_instance * swap * right_instance.T
    assert left_instance.det() != 0 and right_instance.det() != 0
    assert instance.rank() == 2
    assert sp.Matrix(((1, 0), (0, 0))).rank() == 1
    return {"two_rank2_pure_companion_no_go_checks": 2}


def check_allowed_binary_diagonal() -> dict[str, int]:
    """Check the allowed opposite-orientation binary diagonal companion."""

    x, y, u, v = sp.symbols("x y u v")
    # n has p=x e_1, q=y e_2; m has p=u e_2, q=v e_1.
    p_n = x * coordinate(3, 1)
    q_n = y * coordinate(3, 2)
    p_m = u * coordinate(3, 2)
    q_m = v * coordinate(3, 1)
    companion = p_n * q_m.T + q_n * p_m.T
    expected = sp.zeros(3, 3)
    expected[1, 1] = x * v
    expected[2, 2] = y * u
    assert companion == expected
    assert sp.factor(companion[1, 1] * companion[2, 2]) == x * y * u * v
    finite = companion.subs({x: 1, y: 2, u: 3, v: 5})
    assert finite == sp.diag(0, 5, 6)
    return {"allowed_binary_diagonal_checks": 1}


def orientation_vectors(
    orientation: str,
    x_scale: int,
    y_scale: int,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return exact X/Y oriented rows in a two-dimensional visible plane."""

    e0 = coordinate(2, 0)
    e1 = coordinate(2, 1)
    if orientation == "X":
        return x_scale * e0, y_scale * e1
    if orientation == "Y":
        return x_scale * e1, y_scale * e0
    raise ValueError(f"unknown orientation: {orientation}")


def orientation_companion(
    left_orientation: str,
    right_orientation: str,
    left_index: int,
    right_index: int,
) -> sp.Matrix:
    """Build one exact two-label orientation companion."""

    x_scales = (1, 1, 1)
    y_scales = (1, 2, 3)
    p_left, q_left = orientation_vectors(
        left_orientation, x_scales[left_index], y_scales[left_index]
    )
    p_right, q_right = orientation_vectors(
        right_orientation, x_scales[right_index], y_scales[right_index]
    )
    return sp.kronecker_product(p_left, q_right) + sp.kronecker_product(q_left, p_right)


def in_column_span(columns: sp.Matrix, target: sp.Matrix) -> bool:
    """Check exact column-span membership without numerical tolerances."""

    return columns.row_join(target).rank() == columns.rank()


def check_q3_orientation_system() -> dict[str, int]:
    """Check XXX/YYY failure and the six mixed q=3 orientations."""

    pure_targets = (coordinate(4, 0), coordinate(4, 3))
    outcomes: dict[str, bool] = {}
    ranks: dict[str, int] = {}
    for pattern in ("XXX", "XXY", "XYX", "XYY", "YXX", "YXY", "YYX", "YYY"):
        companions = sp.Matrix.hstack(
            *(
                orientation_companion(pattern[left], pattern[right], left, right)
                for left, right in ((0, 1), (0, 2), (1, 2))
            )
        )
        ranks[pattern] = companions.rank()
        outcomes[pattern] = any(
            in_column_span(companions, target) for target in pure_targets
        )

    assert outcomes["XXX"] is False
    assert outcomes["YYY"] is False
    assert all(
        outcomes[pattern] for pattern in ("XXY", "XYX", "XYY", "YXX", "YXY", "YYX")
    )
    assert ranks["XXX"] == ranks["YYY"] == 2
    assert all(
        ranks[pattern] == 3 for pattern in ("XXY", "XYX", "XYY", "YXX", "YXY", "YYX")
    )

    # The labelled three-port XXY identity is checked in the full visible
    # space.  For u,v of type X and w of type Y, choose h_u=-p_u,
    # h_v=-p_v, h_w=p_w.  Reordering every pair term into (u,v,w) gives
    # exactly -2*p_u tensor p_v tensor q_w, a nonzero pure c tensor.
    e_c = coordinate(3, 0)
    p_u = e_c
    q_u = coordinate(3, 1) + 2 * coordinate(3, 2)
    p_v = e_c
    q_v = 2 * coordinate(3, 1) - coordinate(3, 2)
    p_w = 3 * coordinate(3, 1) + coordinate(3, 2)
    q_w = e_c
    h_u, h_v, h_w = -p_u, -p_v, p_w
    triangle = (
        sp.kronecker_product(p_u, q_v, h_w)
        + sp.kronecker_product(q_u, p_v, h_w)
        + sp.kronecker_product(p_u, h_v, q_w)
        + sp.kronecker_product(q_u, h_v, p_w)
        + sp.kronecker_product(h_u, p_v, q_w)
        + sp.kronecker_product(h_u, q_v, p_w)
    )
    pure_identity = -2 * sp.kronecker_product(p_u, p_v, q_w)
    assert triangle == pure_identity
    assert pure_identity != sp.zeros(27, 1)
    return {
        "q3_orientation_patterns": len(outcomes),
        "q3_homogeneous_failures": 2,
        "q3_mixed_patterns_allow": 6,
        "q3_XXY_minus_2_pure_identity": 1,
    }


def check_q4_six_pair_cancellation() -> dict[str, int]:
    """Check an exact six-pair cancellation identity for q=4.

    Take two X ports and two Y ports at one exact fibre.  With ``c=0``,
    ``r=e_1``, and ``s=e_2``, the X/X and Y/Y companions are respectively

        M_r=e_c tensor r+r tensor e_c,
        M_s=e_c tensor s+s tensor e_c,

    while each cross companion is ``e_c tensor e_c+r tensor s``.  Assigning
    the complementary two-port decks ``-M_r/2``, ``-M_s/2``, and four copies
    of ``e_c tensor e_c`` gives the six-pair identity

        sum g_ij tensor D_(complement(ij))
            = 4 e_c tensor e_c tensor e_c tensor e_c.

    The explicit reindexing below is important: each pair/deck product is
    written in its labelled factor order before it is compared in the common
    order ``(0,1,2,3)``.  This is a fibre-level cancellation control, not a
    claim that the displayed repeated rows form a complete witness.
    """

    e_c = coordinate(3, 0)
    r = coordinate(3, 1)
    s = coordinate(3, 2)
    p_rows = (e_c, e_c, s, s)
    q_rows = (r, r, e_c, e_c)
    edges = tuple(combinations(range(4), 2))
    companions = {
        edge: p_rows[edge[0]] * q_rows[edge[1]].T + q_rows[edge[0]] * p_rows[edge[1]].T
        for edge in edges
    }
    M_r = e_c * r.T + r * e_c.T
    M_s = e_c * s.T + s * e_c.T
    e_cc = e_c * e_c.T
    decks = {
        (0, 1): -M_r / 2,
        (2, 3): -M_s / 2,
        (0, 2): e_cc,
        (0, 3): e_cc,
        (1, 2): e_cc,
        (1, 3): e_cc,
    }
    assert companions[(0, 1)] == M_r
    assert companions[(2, 3)] == M_s
    assert all(
        companions[edge] == e_cc + r * s.T for edge in ((0, 2), (0, 3), (1, 2), (1, 3))
    )

    def flatten_four(indices: tuple[int, ...]) -> int:
        result = 0
        for index in indices:
            result = 3 * result + index
        return result

    def labelled_product(
        pair_tensor: sp.Matrix,
        deck_tensor: sp.Matrix,
        pair: tuple[int, int],
        complement: tuple[int, int],
    ) -> sp.Matrix:
        """Place a pair/deck product into canonical labelled order."""

        result = sp.zeros(81, 1)
        for first, second, third, fourth in product(range(3), repeat=4):
            coefficient = pair_tensor[first, second] * deck_tensor[third, fourth]
            if coefficient == 0:
                continue
            canonical = [0, 0, 0, 0]
            canonical[pair[0]] = first
            canonical[pair[1]] = second
            canonical[complement[0]] = third
            canonical[complement[1]] = fourth
            result[flatten_four(tuple(canonical))] += coefficient
        return result

    cancellation = sp.zeros(81, 1)
    for edge in edges:
        complement = tuple(index for index in range(4) if index not in edge)
        cancellation += labelled_product(
            companions[edge], decks[complement], edge, complement
        )
    target = 4 * sp.kronecker_product(e_c, e_c, e_c, e_c)
    assert cancellation == target
    return {"q4_six_pair_cancellation_checks": 1}


def main() -> None:
    """Run every bounded exact audit and print its evidence ledger."""

    summary: dict[str, int] = {}
    summary.update(check_support_only_census())
    typed_summary, survivors = check_typed_census()
    summary.update(typed_summary)
    summary.update(check_refinement_partition(survivors))
    summary.update(check_p1_flattening())
    summary.update(check_two_rank2_pure_companion_no_go())
    summary.update(check_allowed_binary_diagonal())
    summary.update(check_q3_orientation_system())
    summary.update(check_q4_six_pair_cancellation())

    for key in sorted(summary):
        print(f"{key}: {summary[key]}")
    print(
        "PASS: exact two-deficient profile audit and local binary/orientation "
        "controls (audit only; global Krenn-Gu conjecture remains unresolved)"
    )


if __name__ == "__main__":
    main()
