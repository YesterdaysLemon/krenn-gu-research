"""Exact finite and linear-algebra checks for the GLS62 branch.

The owning GLS62 document proves the following scoped implication.  At root
order three, with zero anchor and all six auxiliary joint maps torus-rigid,
an exactly-one-deficient map cannot occur.  This replay checks the finite
support ledger used by that proof and the small quotient calculations used in
its load-bearing steps.

There are two deliberately different counts below.  ``RAW_PROFILES`` is the
complete labelled abstract profile census: the deficient label is fixed, its
kernel support has size one or two, and each of the five injective labels is
either a pure axis or has at most one zero cross-product colour.  The direct
``NORMALIZED_PROFILES`` census fixes ``A=range(s)`` and remembers only the
pure-axis count P, as in the proof's colour/label normalization.  It has
exactly

    2 * sum(P=0..5) 4**(5-P) = 2,730

tuples.  The six requested ledger bins are a disjoint partition of this
normalized enumeration; no unrelated slices are multiplied by orbit factors.

No source tensor, physical deck, response, selector, or synchronization is
constructed here.  The exact algebra is only an audit of the finite/support
and displayed quotient leaves; the same-source tensor argument and its scope
remain in the theorem document, and the global conjecture remains unresolved.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

LABELS = tuple(range(5))
COLOURS = tuple(range(3))
ZERO_CHOICES = (-1, *COLOURS)


Profile = tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]
NormalizedProfile = tuple[int, int, tuple[int, ...]]


def make_profile(
    support: tuple[int, ...],
    pure: tuple[int, ...],
    assignment: tuple[int, ...],
) -> Profile:
    """Make one profile, with the assignment aligned with its nonaxis U."""

    nonaxis = tuple(label for label in LABELS if label not in pure)
    assert len(nonaxis) == len(assignment)
    assert all(value in ZERO_CHOICES for value in assignment)
    assert support in tuple(combinations(COLOURS, len(support)))
    return support, pure, nonaxis, assignment


def profiles() -> tuple[Profile, ...]:
    """Enumerate every labelled abstract exactly-one-deficient profile."""

    result: list[Profile] = []
    for support_size in (1, 2):
        for support in combinations(COLOURS, support_size):
            for pure_count in range(len(LABELS) + 1):
                for pure in combinations(LABELS, pure_count):
                    nonaxis = tuple(label for label in LABELS if label not in pure)
                    for assignment in product(ZERO_CHOICES, repeat=len(nonaxis)):
                        result.append(make_profile(support, pure, assignment))
    return tuple(result)


RAW_PROFILES = profiles()


def nonaxis_zero_sets(profile: Profile) -> tuple[frozenset[int], ...]:
    """Return the GLS61 E_c sets for the five non-deficient labels."""

    _, _, nonaxis, assignment = profile
    return tuple(
        frozenset(
            label
            for label, value in zip(nonaxis, assignment, strict=True)
            if value == colour
        )
        for colour in COLOURS
    )


def nonaxis_zero_counts(profile: Profile) -> tuple[int, ...]:
    return tuple(len(zero_set) for zero_set in nonaxis_zero_sets(profile))


def normalized_profiles() -> tuple[NormalizedProfile, ...]:
    """Enumerate the direct proof-normalized support/profile census.

    ``support_size`` chooses the canonical kernel support A=range(s), and P
    is only a count.  The remaining 5-P abstract nonaxis labels each receive
    one status in {-1,0,1,2}; this is precisely the GLS61 fact that one
    injective nonaxis label has at most one identically zero cross coordinate.
    """

    result: list[NormalizedProfile] = []
    for support_size in (1, 2):
        for pure_count in range(len(LABELS) + 1):
            for assignment in product(ZERO_CHOICES, repeat=len(LABELS) - pure_count):
                result.append((support_size, pure_count, assignment))
    return tuple(result)


NORMALIZED_PROFILES = normalized_profiles()


def normalized_zero_counts(profile: NormalizedProfile) -> tuple[int, ...]:
    """Return |E_c| for a normalized profile."""

    _, _, assignment = profile
    return tuple(assignment.count(colour) for colour in COLOURS)


def check_raw_profile_census() -> dict[str, int]:
    """Check the complete 6 * 5^5 labelled abstract profile census."""

    assert len(RAW_PROFILES) == 6 * 5**5 == 18_750
    by_support_size = {
        size: sum(len(profile[0]) == size for profile in RAW_PROFILES)
        for size in (1, 2)
    }
    assert by_support_size == {1: 9_375, 2: 9_375}

    by_pure_count = {
        pure_count: sum(len(profile[1]) == pure_count for profile in RAW_PROFILES)
        for pure_count in range(6)
    }
    # There are six possible A's.  For P pure labels, choose the P labels and
    # give each of the remaining 5-P labels one of -1,0,1,2 statuses.
    assert by_pure_count == {
        pure_count: 6 * sp.binomial(5, pure_count) * 4 ** (5 - pure_count)
        for pure_count in range(6)
    }

    for profile in RAW_PROFILES:
        zero_sets = nonaxis_zero_sets(profile)
        assert all(
            zero_sets[left].isdisjoint(zero_sets[right])
            for left, right in combinations(COLOURS, 2)
        )

    return {
        "raw_profiles": len(RAW_PROFILES),
        "raw_support_size_one": by_support_size[1],
        "raw_support_size_two": by_support_size[2],
    }


def check_raw_floor_partition() -> dict[str, int]:
    """Check the exhaustive E-floor partition before symmetry normalization."""

    floor_lt_two = sum(
        any(nonaxis_zero_counts(profile)[colour] < 2 for colour in profile[0])
        for profile in RAW_PROFILES
    )
    floor_eq_two = sum(
        all(nonaxis_zero_counts(profile)[colour] >= 2 for colour in profile[0])
        and any(nonaxis_zero_counts(profile)[colour] == 2 for colour in profile[0])
        for profile in RAW_PROFILES
    )
    floor_ge_three = sum(
        all(nonaxis_zero_counts(profile)[colour] >= 3 for colour in profile[0])
        for profile in RAW_PROFILES
    )
    assert (floor_lt_two, floor_eq_two, floor_ge_three) == (
        15_957,
        2_250,
        543,
    )
    assert floor_lt_two + floor_eq_two + floor_ge_three == len(RAW_PROFILES)

    # The E_c are disjoint and there are only five nonaxis labels.  Therefore
    # the final cell has |A|=1, P<=2; its labelled multiplicities are exactly
    # 3*106, 3*5*13, and 3*C(5,2)*1.
    final_profiles = tuple(
        profile
        for profile in RAW_PROFILES
        if all(nonaxis_zero_counts(profile)[colour] >= 3 for colour in profile[0])
    )
    assert len(final_profiles) == 543
    assert all(
        len(profile[0]) == 1 and len(profile[1]) <= 2 for profile in final_profiles
    )
    return {
        "raw_supported_E_floor_lt_2": floor_lt_two,
        "raw_supported_E_exactly_2": floor_eq_two,
        "raw_supported_E_floor_ge_3": floor_ge_three,
    }


def check_proof_case_ledger() -> dict[str, int]:
    """Re-derive the requested direct 2,730-case proof partition."""

    assert len(NORMALIZED_PROFILES) == 2 * sum(4 ** (5 - pure) for pure in range(6))
    assert len(NORMALIZED_PROFILES) == 2_730

    # The first two bins are the supported-E floor alternatives.  A normalized
    # profile has A=range(s), so no colour or pure-label orbit factors occur.
    supported_floor_lt_two = tuple(
        profile
        for profile in NORMALIZED_PROFILES
        if min(normalized_zero_counts(profile)[colour] for colour in range(profile[0]))
        < 2
    )
    supported_exact_two = tuple(
        profile
        for profile in NORMALIZED_PROFILES
        if min(normalized_zero_counts(profile)[colour] for colour in range(profile[0]))
        == 2
    )
    residual = tuple(
        profile
        for profile in NORMALIZED_PROFILES
        if min(normalized_zero_counts(profile)[colour] for colour in range(profile[0]))
        >= 3
    )
    assert len(supported_floor_lt_two) == 2_190
    assert len(supported_exact_two) == 420
    assert len(residual) == 120
    assert len(supported_floor_lt_two) + len(supported_exact_two) + len(
        residual
    ) == len(NORMALIZED_PROFILES)

    # The residual automatically has singleton A and P<=2: two disjoint
    # supported E-sets of size at least three cannot fit into five U labels.
    assert all(profile[0] == 1 for profile in residual)
    assert all(profile[1] <= 2 for profile in residual)

    p0_residual = tuple(profile for profile in residual if profile[1] == 0)
    p0_ordinary = tuple(
        profile
        for profile in p0_residual
        if any(normalized_zero_counts(profile)[colour] == 0 for colour in (1, 2))
    )
    p0_singleton_pair = tuple(
        profile
        for profile in p0_residual
        if all(normalized_zero_counts(profile)[colour] == 1 for colour in (1, 2))
    )
    assert len(p0_residual) == 106
    assert len(p0_ordinary) == 86
    assert len(p0_singleton_pair) == 20
    assert len(p0_ordinary) + len(p0_singleton_pair) == len(p0_residual)

    p1_residual = tuple(profile for profile in residual if profile[1] == 1)
    p2_residual = tuple(profile for profile in residual if profile[1] == 2)
    p3_residual = tuple(profile for profile in residual if profile[1] >= 3)
    assert len(p1_residual) == 13
    assert len(p2_residual) == 1
    assert not p3_residual
    assert all(
        any(normalized_zero_counts(profile)[colour] == 0 for colour in (1, 2))
        for profile in p1_residual
    )
    assert all(normalized_zero_counts(profile)[1:] == (0, 0) for profile in p2_residual)

    ledger = {
        "supported_E_floor_lt_2": len(supported_floor_lt_two),
        "supported_E_exactly_2_obstruction": len(supported_exact_two),
        "P0_ordinary_one_open_failures": len(p0_ordinary),
        "P0_singleton_nonsupport_pair_contradiction": len(p0_singleton_pair),
        "P1_active_line_contradiction": len(p1_residual),
        "P2_active_line_contradiction": len(p2_residual),
    }
    assert sum(ledger.values()) == 2_730
    assert ledger == {
        "supported_E_floor_lt_2": 2_190,
        "supported_E_exactly_2_obstruction": 420,
        "P0_ordinary_one_open_failures": 86,
        "P0_singleton_nonsupport_pair_contradiction": 20,
        "P1_active_line_contradiction": 13,
        "P2_active_line_contradiction": 1,
    }
    return {**ledger, "proof_case_total": sum(ledger.values()), "survivors": 0}


def quotient_map(active: sp.Matrix) -> sp.Matrix:
    """An exact matrix for V*/(F active), with kernel F*active."""

    assert active.shape == (3, 1)
    pivot = next((index for index, value in enumerate(active) if value != 0), None)
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


def coordinate(colour: int) -> sp.Matrix:
    return sp.eye(3)[:, colour]


def check_row_quotient_visibility() -> dict[str, int]:
    """Check rho_n(e_a) != 0 exactly for a in the selected kernel support."""

    cases = 0
    support_cells = tuple(
        support
        for support_size in (1, 2)
        for support in combinations(COLOURS, support_size)
    )
    for support in support_cells:
        row_space = sp.Matrix.vstack(
            *(coordinate(colour).T for colour in COLOURS if colour not in support)
        )
        assert row_space.rank() == 3 - len(support)
        for colour in COLOURS:
            # A quotient representative can be taken as the coordinates in A.
            quotient = sp.Matrix.vstack(*(coordinate(index).T for index in support))
            visible = quotient * coordinate(colour)
            assert (visible != sp.zeros(len(support), 1)) == (colour in support)
            assert row_space.col_join(coordinate(colour).T).rank() == (
                3 - len(support) + int(colour in support)
            )
            cases += 1

    # The actual rank-two pure-coordinate deficient map used after the floor
    # is K=F e_0, row J_n=span(e_1,e_2).
    deficient_rows = sp.Matrix(((0, 1, 0), (0, 0, 1)))
    rho = sp.Matrix(((1, 0, 0),))
    assert deficient_rows.rank() == 2
    assert rho * deficient_rows.T == sp.zeros(1, 2)
    assert rho * coordinate(0) != sp.zeros(1, 1)
    assert all(rho * coordinate(colour) == sp.zeros(1, 1) for colour in (1, 2))
    return {"row_quotient_visibility_cases": cases, "rank_two_model": 1}


def shore_vectors(colour: int, orientation: str) -> tuple[sp.Matrix, sp.Matrix]:
    """Exact representatives of the two GLS61 zero-coordinate orientations."""

    others = tuple(index for index in COLOURS if index != colour)
    if orientation == "X":
        # p is on the colour axis; q has a nonzero complementary projection.
        return coordinate(colour), coordinate(others[0]) + 2 * coordinate(others[1])
    if orientation == "Y":
        # q is on the colour axis; p has a nonzero complementary projection.
        return coordinate(others[0]) + 2 * coordinate(others[1]), coordinate(colour)
    raise ValueError(orientation)


def check_four_pair_orientations() -> dict[str, int]:
    """Check all XX, XY, YX, YY same-colour companion obstructions."""

    checked = 0
    for colour in COLOURS:
        for left, right in product(("X", "Y"), repeat=2):
            p_left, q_left = shore_vectors(colour, left)
            p_right, q_right = shore_vectors(colour, right)
            companion = p_left * q_right.T + q_left * p_right.T
            off_pure = [
                companion[row, column]
                for row in COLOURS
                for column in COLOURS
                if (row, column) != (colour, colour)
            ]
            assert any(value != 0 for value in off_pure)
            checked += 1
    assert checked == 12
    return {"GLS61_pair_orientation_cases": checked}


def check_rank_two_pure_companion_obstruction() -> dict[str, int]:
    """Replay the rank-two deficient versus nonaxis pure-companion lemma."""

    c, d, e = 0, 1, 2
    deficient_row_space = sp.Matrix(((0, 1, 0), (0, 0, 1)))
    off_d = (c, e)

    # X-oriented u: p_u=e_d and pi_d(q_u) is nonzero.  Purity of
    # p_n tensor q_u + q_n tensor p_u therefore forces p_n=0; the remaining
    # Y_n row space would have to be both rank two and contained in e_d.
    p_u_x, q_u_x = coordinate(d), coordinate(c) + coordinate(e)
    p_n = sp.Matrix(sp.symbols("p_n0:3"))
    q_n = sp.Matrix(sp.symbols("q_n0:3"))
    g_x = p_n * q_u_x.T + q_n * p_u_x.T
    assert g_x[:, off_d] == p_n * sp.Matrix([[1, 1]])
    assert sp.solve(list(g_x[:, off_d]), list(p_n)) == {
        p_n[0]: 0,
        p_n[1]: 0,
        p_n[2]: 0,
    }
    # Once p_n=0, purity would require every row of row(Y_n) to lie on e_d.
    # The rank-two deficient row model has a visible e_e direction.
    assert deficient_row_space[:, off_d].rank() == 1
    assert deficient_row_space[:, (d,)].rank() == 1
    assert deficient_row_space[:, off_d] != sp.zeros(2, 2)
    assert q_n.shape == (3, 1)

    # Y-oriented u is the exact transpose of the preceding argument.
    p_u_y, q_u_y = coordinate(c) + coordinate(e), coordinate(d)
    g_y = p_n * q_u_y.T + q_n * p_u_y.T
    assert g_y[:, off_d] == q_n * sp.Matrix([[1, 1]])
    assert sp.solve(list(g_y[:, off_d]), list(q_n)) == {
        q_n[0]: 0,
        q_n[1]: 0,
        q_n[2]: 0,
    }
    assert deficient_row_space[:, off_d].rank() == 1
    return {"rank_two_pure_companion_orientation_cases": 2}


def check_active_line_target_separation() -> dict[str, int]:
    """Check the P=1 and P=2 target separations over exact quotients."""

    active_p = sp.Matrix((1, 2, 3))
    active_q = sp.Matrix((2, 3, 5))
    quotient_p = quotient_map(active_p)
    quotient_q = quotient_map(active_q)

    # Every coordinate target survives an active full-row quotient when the
    # active row is genuinely non-coordinate; the untouched n coordinate then
    # separates all colours, even if the quotient itself is only two-dimensional.
    p1_targets = sp.Matrix.hstack(
        *(
            sp.kronecker_product(coordinate(colour), quotient_p * coordinate(colour))
            for colour in COLOURS
        )
    )
    assert quotient_p.rank() == 2
    assert all(quotient_p * coordinate(colour) != sp.zeros(2, 1) for colour in COLOURS)
    assert p1_targets.rank() == 3

    # With two pure axes, the two nonsupported colours d,e remain independent
    # at the untouched deficient slot and both active quotients.
    p2_targets = sp.Matrix.hstack(
        *(
            sp.kronecker_product(
                coordinate(colour),
                quotient_p * coordinate(colour),
                quotient_q * coordinate(colour),
            )
            for colour in (1, 2)
        )
    )
    assert p2_targets.rank() == 2
    assert all(
        quotient_p * coordinate(colour) != sp.zeros(2, 1)
        and quotient_q * coordinate(colour) != sp.zeros(2, 1)
        for colour in (1, 2)
    )

    # Any pair meeting a pure slot carries its active line and is killed;
    # this is the exact source-side quotient used in both P cases.
    assert quotient_p * active_p == sp.zeros(2, 1)
    assert quotient_q * active_q == sp.zeros(2, 1)
    return {
        "P1_target_separation_rank": p1_targets.rank(),
        "P2_target_separation_rank": p2_targets.rank(),
        "active_line_kill_checks": 2,
    }


def main() -> None:
    summary: dict[str, int] = {}
    summary.update(check_raw_profile_census())
    summary.update(check_raw_floor_partition())
    summary.update(check_proof_case_ledger())
    summary.update(check_row_quotient_visibility())
    summary.update(check_four_pair_orientations())
    summary.update(check_rank_two_pure_companion_obstruction())
    summary.update(check_active_line_target_separation())

    for key in sorted(summary):
        print(f"{key}: {summary[key]}")
    print(
        "PASS: GLS62 exactly-one-deficient profile census, row quotients, "
        "four orientations, pure-companion obstruction, and active-line "
        "target separation"
    )


if __name__ == "__main__":
    main()
