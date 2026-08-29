"""Independent finite audit for the one-deficient GLS61 exclusion.

This file deliberately imports only the Python standard library.  The
written argument is characteristic-zero and polynomial; the finite checks
below audit its support, quotient, and orientation boundaries over Q and F_3.
The profile census fixes the visible kernel-colour set to (0,) or (0, 1).
The other labelled choices are colour relabelings, so the requested canonical
census is 2 * sum(P=0..5) 4**(5-P) = 2730.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from fractions import Fraction
from itertools import combinations, product

Vector = tuple[int, ...]
Subspace = frozenset[Vector]
COLORS = (0, 1, 2)
PROFILE_VALUES = (-1, 0, 1, 2)
PRIME = 3


def rank_fraction(rows: Iterable[Sequence[int | Fraction]]) -> int:
    """Return the exact row rank over Q."""

    work = [list(map(Fraction, row)) for row in rows]
    if not work:
        return 0
    width = len(work[0])
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
    return rank


def rank_mod(rows: Iterable[Sequence[int]], prime: int = PRIME) -> int:
    """Return row rank over F_prime."""

    work = [[value % prime for value in row] for row in rows]
    if not work:
        return 0
    width = len(work[0])
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(value * inverse) % prime for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
    return rank


def unit(index: int, dimension: int = 3) -> Vector:
    return tuple(int(position == index) for position in range(dimension))


def span(basis: Sequence[Vector], prime: int = PRIME) -> Subspace:
    """Enumerate the finite span of a vector list."""

    if not basis:
        return frozenset({(0,) * 3})
    return frozenset(
        tuple(
            sum(coeff * vector[index] for coeff, vector in zip(coeffs, basis)) % prime
            for index in range(len(basis[0]))
        )
        for coeffs in product(range(prime), repeat=len(basis))
    )


def all_subspaces(dimension: int, prime: int = PRIME) -> tuple[Subspace, ...]:
    """Enumerate every subspace of F_prime^dimension."""

    vectors = tuple(product(range(prime), repeat=dimension))
    nonzero = tuple(vector for vector in vectors if any(vector))
    found: set[Subspace] = {frozenset({(0,) * dimension})}
    for size in range(1, dimension + 1):
        for basis in combinations(nonzero, size):
            if rank_mod(basis, prime) == size:
                found.add(span(basis, prime))
    return tuple(
        sorted(found, key=lambda subspace: (len(subspace), tuple(sorted(subspace))))
    )


def subspace_sum(left: Subspace, right: Subspace, prime: int = PRIME) -> Subspace:
    # Sum the already-enumerated finite subspaces directly.  Passing all
    # elements as a spanning list would ask span() to iterate 3**26
    # coefficients for a full plane.
    return frozenset(
        tuple((left_value[index] + right_value[index]) % prime for index in range(3))
        for left_value in left
        for right_value in right
    )


def projection(vector: Vector, omitted: int) -> Vector:
    return tuple(value for index, value in enumerate(vector) if index != omitted)


def projected_rank(subspace: Subspace, omitted: int, prime: int = PRIME) -> int:
    return rank_mod(tuple(projection(vector, omitted) for vector in subspace), prime)


def coordinate_line(index: int, prime: int = PRIME) -> Subspace:
    return span((unit(index),), prime)


def quotient_rows(active: Vector, prime: int = PRIME) -> tuple[Vector, Vector]:
    """Return two independent covectors annihilating the active line."""

    candidates = tuple(
        vector
        for vector in product(range(prime), repeat=3)
        if sum(left * right for left, right in zip(vector, active)) % prime == 0
    )
    first = next(vector for vector in candidates if any(vector))
    second = next(
        vector for vector in candidates if rank_mod((first, vector), prime) == 2
    )
    return first, second


def quotient_column(rows: Sequence[Vector], colour: int, prime: int = PRIME) -> Vector:
    return tuple(row[colour] % prime for row in rows)


def outer(
    left: Vector, right: Vector, prime: int = PRIME
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((left[row] * right[column]) % prime for column in range(3))
        for row in range(3)
    )


def add_matrices(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
    prime: int = PRIME,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((left[row][column] + right[row][column]) % prime for column in range(3))
        for row in range(3)
    )


def off_diagonal_nonzero(matrix: tuple[tuple[int, ...], ...], colour: int) -> bool:
    return any(
        matrix[row][column]
        for row in COLORS
        for column in COLORS
        if (row, column) != (colour, colour)
    )


def profile_census() -> dict[str, int]:
    """Audit the complete P/U case cover using canonical A supports."""

    categories = {
        "row_quotient_floor": 0,
        "same_colour_pair": 0,
        "p0_missing_other_colour": 0,
        "p0_rank2_companion": 0,
        "p1_all_colour_diagonal": 0,
        "p2_two_colour_diagonal": 0,
        "zero_survivors": 0,
    }
    full_axis_quotient = 0
    per_support: dict[int, list[tuple[int, int, int, int, int]]] = {1: [], 2: []}
    total = 0
    for support_size in (1, 2):
        visible = tuple(range(support_size))
        for pure_count in range(6):
            nonaxis_count = 5 - pure_count
            row_floor = pair_case = post = 0
            for assignment in product(PROFILE_VALUES, repeat=nonaxis_count):
                total += 1
                if pure_count == 5:
                    # The all-axis profile is discharged by the same
                    # row/active quotient floor.  Keep a subcounter, but put
                    # these two profiles in the six-bin partition.
                    categories["row_quotient_floor"] += 1
                    full_axis_quotient += 1
                    row_floor += 1
                    continue
                zero_counts = tuple(assignment.count(colour) for colour in COLORS)
                if any(zero_counts[colour] < 2 for colour in visible):
                    categories["row_quotient_floor"] += 1
                    row_floor += 1
                    continue
                if any(zero_counts[colour] == 2 for colour in visible):
                    categories["same_colour_pair"] += 1
                    pair_case += 1
                    continue
                post += 1
                if support_size == 2:
                    raise AssertionError(
                        "two visible colours cannot each have three disjoint zeros"
                    )
                # Visible colour is 0 by canonical relabeling.
                if pure_count == 0:
                    if zero_counts[1] == 0 or zero_counts[2] == 0:
                        categories["p0_missing_other_colour"] += 1
                    else:
                        assert zero_counts == (3, 1, 1)
                        categories["p0_rank2_companion"] += 1
                elif pure_count == 1:
                    categories["p1_all_colour_diagonal"] += 1
                elif pure_count == 2:
                    assert nonaxis_count == 3 and zero_counts[0] == 3
                    assert zero_counts[1] == zero_counts[2] == 0
                    categories["p2_two_colour_diagonal"] += 1
                else:
                    raise AssertionError("post-floor profile has too many pure axes")
            per_support[support_size].append(
                (pure_count, nonaxis_count, 4**nonaxis_count, row_floor, pair_case)
            )

    canonical_total = sum(4 ** (5 - pure_count) for pure_count in range(6)) * 2
    assert total == canonical_total == 2730
    assert categories["row_quotient_floor"] == 2190
    assert categories["same_colour_pair"] == 420
    assert categories["p0_missing_other_colour"] == 86
    assert categories["p0_rank2_companion"] == 20
    assert categories["p1_all_colour_diagonal"] == 13
    assert categories["p2_two_colour_diagonal"] == 1
    assert full_axis_quotient == 2
    assert (
        sum(categories[name] for name in categories if name != "zero_survivors")
        == total
    )
    assert categories["zero_survivors"] == 0

    print(f"canonical_profile_total: {total}")
    print(f"labelled_colour_copy_total: {3 * total}")
    for support_size in (1, 2):
        print(
            f"support_size_{support_size}_total: {sum(row[2] for row in per_support[support_size])}"
        )
        for pure_count, nonaxis_count, count, row_floor, pair_case in per_support[
            support_size
        ]:
            print(
                f"  A_size={support_size} P={pure_count} U={nonaxis_count} "
                f"total={count} row_floor={row_floor} pair={pair_case}"
            )
    for name, value in categories.items():
        print(f"{name}: {value}")
    print(f"full_axis_quotient_subcounter: {full_axis_quotient}")
    return categories


def check_active_quotients() -> tuple[int, int]:
    """Exhaust active-line coordinate survival and diagonal separation over F_3."""

    active_vectors = tuple(
        vector
        for vector in product(range(PRIME), repeat=3)
        if all(value for value in vector)
    )
    coordinate_cases = 0
    for active in active_vectors:
        rows = quotient_rows(active)
        assert rank_mod(rows) == 2
        for colour in COLORS:
            assert any(quotient_column(rows, colour))
            coordinate_cases += 1

    diagonal_cases = 0
    supports = tuple(
        support for size in range(1, 4) for support in combinations(COLORS, size)
    )
    nonzero_weights = (1, 2)
    # For p >= 2, every extra pure slot contributes a nonzero coordinate
    # factor.  Thus exhaustive coordinate survival in each slot reduces the
    # cancellation check to the two-slot (P=2) representatives below.
    for pure_count in (2,):
        for active_tuple in product(active_vectors, repeat=pure_count):
            quotients = tuple(quotient_rows(active) for active in active_tuple)
            for support in supports:
                for weights in product(nonzero_weights, repeat=len(support)):
                    image = {}
                    for colour, weight in zip(support, weights, strict=True):
                        for output in product(range(2), repeat=pure_count):
                            factor = weight
                            for slot, index in enumerate(output):
                                factor *= quotients[slot][index][colour]
                            image[output] = (image.get(output, 0) + factor) % PRIME
                    assert any(image.values())
                    diagonal_cases += 1
    assert coordinate_cases == 24
    print(f"active_line_coordinate_cases: {coordinate_cases}")
    print(f"active_line_two_slot_diagonal_cases: {diagonal_cases}")
    return coordinate_cases, diagonal_cases


def check_row_quotient_support() -> int:
    """Check rank-one planes and rank-two kernel lines over exact Q."""

    cases = 0
    for missing in COLORS:
        plane_rows = [unit(missing)]
        support = tuple(
            colour
            for colour in COLORS
            if rank_fraction(plane_rows + [unit(colour)]) > rank_fraction(plane_rows)
        )
        assert support == tuple(colour for colour in COLORS if colour != missing)
        assert rank_fraction(plane_rows + [unit(colour) for colour in support]) == 3
        cases += 1

        line_support = (missing,)
        row_basis = [unit(colour) for colour in COLORS if colour != missing]
        visible = tuple(
            colour
            for colour in COLORS
            if rank_fraction(row_basis + [unit(colour)]) > rank_fraction(row_basis)
        )
        assert visible == line_support
        cases += 1

        other = next(colour for colour in COLORS if colour != missing)
        relation = [
            tuple(
                1 if index == missing else -1 if index == other else 0
                for index in COLORS
            ),
            unit(next(colour for colour in COLORS if colour not in (missing, other))),
        ]
        visible = tuple(
            colour
            for colour in COLORS
            if rank_fraction(relation + [unit(colour)]) > rank_fraction(relation)
        )
        assert set(visible) == {missing, other}
        assert (
            rank_fraction(relation + [unit(missing), unit(other)])
            - rank_fraction(relation)
            == 1
        )
        cases += 1
    assert cases == 9
    print(f"row_quotient_support_cases: {cases}")
    return cases


def check_pair_orientation_obstruction() -> int:
    """Check all four same-colour orientation pairs and three colours over F_3."""

    cases = 0
    for colour in COLORS:
        others = tuple(index for index in COLORS if index != colour)
        pure = unit(colour)
        off0, off1 = unit(others[0]), unit(others[1])
        # Representative coefficient rows for XX, YY, XY, and YX.
        representatives = (
            (pure, off0, pure, off1),
            (off0, pure, off1, pure),
            (pure, off0, off1, pure),
            (off0, pure, pure, off1),
        )
        for p_s, q_s, p_u, q_u in representatives:
            companion = add_matrices(outer(p_s, q_u), outer(q_s, p_u))
            assert off_diagonal_nonzero(companion, colour)
            cases += 1

        # The projected proof is exhaustive for all finite boundary vectors.
        nonzero_pure = tuple(scalar * pure for scalar in (1, 2))
        all_vectors = tuple(product(range(PRIME), repeat=3))
        for p_s in nonzero_pure:
            for p_u in nonzero_pure:
                for q_s in all_vectors:
                    for q_u in all_vectors:
                        if any(projection(q_u, colour)):
                            projected = outer(p_s, q_u)
                            assert any(
                                projected[row][column]
                                for row in COLORS
                                for column in others
                            )
                        if any(projection(q_s, colour)):
                            projected = outer(q_s, p_u)
                            assert any(
                                projected[row][column]
                                for row in others
                                for column in COLORS
                            )
    assert cases == 12
    print(f"same_colour_orientation_cases: {cases}")
    return cases


def check_rank_two_companion_obstruction() -> tuple[int, int]:
    """Enumerate n rowspaces and oriented u rowspaces over F_3."""

    subspaces = all_subspaces(3)
    zero = frozenset({(0, 0, 0)})
    rank_two_n_cases = 0
    oriented_u_cases = 0
    impossible_pure_companions = 0
    for missing in COLORS:
        plane = frozenset(
            vector for vector in product(range(PRIME), repeat=3) if vector[missing] == 0
        )
        for target in COLORS:
            if target == missing:
                continue
            target_line = coordinate_line(target)
            n_pairs = tuple(
                (left, right)
                for left in subspaces
                for right in subspaces
                if left <= plane
                and right <= plane
                and subspace_sum(left, right) == plane
            )
            for n_x, n_y in n_pairs:
                rank_two_n_cases += 1
                # X-oriented u: X is the target line; Y projects onto its
                # two-space and the joint map is injective/nonaxis.
                for orientation in ("X", "Y"):
                    u_x_candidates = subspaces if orientation == "Y" else (target_line,)
                    u_y_candidates = (target_line,) if orientation == "Y" else subspaces
                    for u_x in u_x_candidates:
                        for u_y in u_y_candidates:
                            pure_rows, transverse_rows = (
                                (u_y, u_x) if orientation == "Y" else (u_x, u_y)
                            )
                            if not pure_rows <= target_line:
                                continue
                            if (
                                pure_rows == zero
                                or projected_rank(transverse_rows, target) != 2
                            ):
                                continue
                            if subspace_sum(u_x, u_y) != frozenset(
                                product(range(PRIME), repeat=3)
                            ):
                                continue
                            oriented_u_cases += 1
                            if orientation == "X":
                                pure_possible = n_x == zero and n_y <= target_line
                            else:
                                pure_possible = n_y == zero and n_x <= target_line
                            if pure_possible:
                                impossible_pure_companions += 1
    assert impossible_pure_companions == 0
    assert rank_two_n_cases > 0 and oriented_u_cases > 0
    print(f"rank_two_n_rowspace_cases: {rank_two_n_cases}")
    print(f"oriented_nonaxis_rowspace_cases: {oriented_u_cases}")
    print(f"rank_two_pure_companion_survivors: {impossible_pure_companions}")
    return rank_two_n_cases, oriented_u_cases


def main() -> None:
    profile_census()
    check_active_quotients()
    check_row_quotient_support()
    check_pair_orientation_obstruction()
    check_rank_two_companion_obstruction()
    print("scope: exact characteristic-zero source identity assumed")
    print("scope: r=3, zero anchor, all-six-rigid, exactly one deficient label")
    print(
        "scope walls: two-deficient, unique-nonrigid, nonzero-anchor, attachment, global conjecture remain open"
    )
    print("PASS: independent exactly-one-deficient row-quotient exclusion audit")


if __name__ == "__main__":
    main()
