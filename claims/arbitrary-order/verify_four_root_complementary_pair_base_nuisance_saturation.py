"""Exact replay for four-root complementary-pair base-nuisance saturation."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

PORTS = frozenset(range(4))
PAIRS = tuple(frozenset(pair) for pair in combinations(PORTS, 2))


def matrix_rank(rows: list[list[Fraction]]) -> int:
    if not rows:
        return 0
    matrix = [row[:] for row in rows]
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def check_slot_orientations() -> int:
    checks = 0
    for target in PAIRS:
        complement = PORTS - target
        assert complement in PAIRS
        assert target != complement
        assert not target & complement
        assert target | complement == PORTS

        # For target S and nuisance label I=T=U-S, the label deck has T slots,
        # while its evaluated companion Pi_T has U-T=S slots.
        label_slots = complement
        companion_slots = PORTS - complement
        receiver_slots = PORTS - target
        target_slots = target
        assert label_slots == receiver_slots
        assert companion_slots == target_slots
        checks += 1
    return checks


def slice_matrix(
    dimension: int, companion: tuple[Fraction, ...]
) -> list[list[Fraction]]:
    """Rows span all eta(Pi) H coefficient slices for basis eta and H."""

    receiver_dimension = dimension**2
    assert len(companion) == receiver_dimension
    rows: list[list[Fraction]] = []
    for coefficient in companion:
        for basis_index in range(receiver_dimension):
            row = [Fraction(0)] * receiver_dimension
            row[basis_index] = coefficient
            rows.append(row)
    return rows


def check_slice_saturation() -> tuple[int, int]:
    profiles = 0
    full_rank_profiles = 0
    for dimension in range(1, 5):
        size = dimension**2
        companions = [
            tuple(Fraction(index == selected) for index in range(size))
            for selected in range(size)
        ]
        companions.append(tuple(Fraction(index + 1) for index in range(size)))
        companions.append(tuple(Fraction(0) for _ in range(size)))
        for companion in companions:
            rank = matrix_rank(slice_matrix(dimension, companion))
            expected = size if any(companion) else 0
            assert rank == expected
            profiles += 1
            full_rank_profiles += int(rank == size)
    return profiles, full_rank_profiles


def is_star(family: frozenset[frozenset[int]]) -> bool:
    return any(all(vertex in edge for edge in family) for vertex in PORTS)


def is_triangle(family: frozenset[frozenset[int]]) -> bool:
    return any(all(vertex not in edge for edge in family) for vertex in PORTS)


def check_survivor_atlas() -> tuple[int, int, int, int]:
    admissible = []
    for mask in product((False, True), repeat=len(PAIRS)):
        family = frozenset(
            pair for pair, survives in zip(PAIRS, mask, strict=True) if survives
        )
        if all(not ({pair, PORTS - pair} <= family) for pair in PAIRS):
            admissible.append(family)
            assert len(family) <= 3
    maximal = [family for family in admissible if len(family) == 3]
    stars = [family for family in maximal if is_star(family)]
    triangles = [family for family in maximal if is_triangle(family)]
    assert len(admissible) == 27
    assert len(maximal) == 8
    assert len(stars) == 4
    assert len(triangles) == 4
    assert set(stars).isdisjoint(triangles)
    return len(admissible), len(maximal), len(stars), len(triangles)


def check_zero_nonzero_logic() -> int:
    """Exhaust raw Pi and quotient-class booleans for all six targets."""

    checks = 0
    for raw_mask in product((False, True), repeat=len(PAIRS)):
        raw = dict(zip(PAIRS, raw_mask, strict=True))
        for survivor_mask in product((False, True), repeat=len(PAIRS)):
            survivor = dict(zip(PAIRS, survivor_mask, strict=True))
            if any(survivor[pair] and not raw[pair] for pair in PAIRS):
                continue
            if any(raw[PORTS - pair] and survivor[pair] for pair in PAIRS):
                continue
            for pair in PAIRS:
                if survivor[pair]:
                    assert not survivor[PORTS - pair]
            assert sum(survivor.values()) <= 3
            checks += 1
    return checks


def main() -> None:
    slot_checks = check_slot_orientations()
    slice_profiles = check_slice_saturation()
    survivor_atlas = check_survivor_atlas()
    logical_profiles = check_zero_nonzero_logic()
    print("four-root complementary-pair base-nuisance saturation: PASS")
    print("  ordered complementary slot checks:", slot_checks)
    print("  exact slice profiles / full-rank profiles:", slice_profiles)
    print("  admissible / maximal / star / triangle masks:", survivor_atlas)
    print("  consistent raw/quotient Boolean profiles:", logical_profiles)
    print("  scope: base shadows only; non-leading legal rows remain open")


if __name__ == "__main__":
    main()
