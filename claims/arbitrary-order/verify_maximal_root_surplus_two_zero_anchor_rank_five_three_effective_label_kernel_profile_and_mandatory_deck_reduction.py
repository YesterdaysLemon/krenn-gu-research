"""Focused exact replay for GLS50.

This script checks the finite coordinate, rank, and profile claims used by
the theorem.  The prose proof supplies the arbitrary-field bridge.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def diagonal_basis() -> sp.Matrix:
    """Columns are r_0,r_1,r_2 in the row-major basis of K^3 tensor K^3."""

    out = sp.zeros(9, 3)
    for c in range(3):
        out[3 * c + c, c] = 1
    return out


def target_slice_map(extra_pure_factors: int) -> sp.Matrix:
    """Map k to sum_c k_c r_c tensor e_c^(tensor extra_pure_factors)."""

    rows = 9 * 3**extra_pure_factors
    out = sp.zeros(rows, 3)
    for c in range(3):
        pure_index = 0
        for _ in range(extra_pure_factors):
            pure_index = 3 * pure_index + c
        out[(3 * c + c) * 3**extra_pure_factors + pure_index, c] = 1
    return out


def two_form_cover_obstruction() -> int:
    """A line can cover one coordinate covector; two lines cannot cover three."""

    assignments = list(product(range(2), repeat=3))
    admissible = 0
    for assignment in assignments:
        loads = [assignment.count(shore) for shore in range(2)]
        if max(loads) <= 1:
            admissible += 1
    assert admissible == 0
    return len(assignments)


def three_line_coordinate_cover() -> int:
    """Three line slots cover three coordinate lines only by a permutation."""

    assignments = list(product(range(3), repeat=3))
    permutations = []
    for assignment in assignments:
        loads = [assignment.count(slot) for slot in range(3)]
        if loads == [1, 1, 1]:
            permutations.append(assignment)
    assert len(permutations) == 6
    return len(permutations)


def profile_replay() -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Enumerate the exact effective-dimension consequences of kernel flags."""

    one_residual = []
    for ku_line, kv_line in product((0, 1), repeat=2):
        if ku_line and kv_line:
            # Both opposite maps become diagonal; nonzero gamma makes the
            # third map diagonal, contradicting rank B=5.
            continue
        one_residual.append(tuple(sorted((1, 3 - ku_line, 3 - kv_line))))
    one_residual = sorted(set(one_residual))
    assert one_residual == [(1, 2, 3), (1, 3, 3)]

    three_port = []
    for flags in product((0, 1), repeat=3):
        if all(flags):
            # Every opposite pair map becomes diagonal.
            continue
        three_port.append(tuple(sorted(3 - flag for flag in flags)))
    three_port = sorted(set(three_port))
    assert three_port == [(2, 2, 3), (2, 3, 3), (3, 3, 3)]
    return one_residual, three_port


def main() -> None:
    delta = diagonal_basis()
    assert delta.rank() == 3

    # The target slice k -> sum k_c r_c e_c... is injective with one or two
    # surviving opposite promoted ports.  Hence a deck form cannot vanish on
    # a nonzero joint-kernel vector.
    one_opposite = target_slice_map(1)
    two_opposite = target_slice_map(2)
    assert one_opposite.shape == (27, 3)
    assert two_opposite.shape == (81, 3)
    assert one_opposite.rank() == two_opposite.rank() == 3

    gamma_assignments = two_form_cover_obstruction()
    coordinate_permutations = three_line_coordinate_cover()
    one_residual, three_port = profile_replay()

    # If every rank-five source coefficient lies in Delta, its combined image
    # has rank at most three, the terminal contradiction in both profile cuts.
    assert delta.row_join(delta).rank() == 3 < 5

    print("GLS50 focused exact verifier: PASS")
    print(f"two-form hostile colour assignments: {gamma_assignments}, none cover")
    print(f"three-deck coordinate permutations: {coordinate_permutations}")
    print(f"injective diagonal target-slice ranks: {one_opposite.rank()}, {two_opposite.rank()}")
    print(f"one-residual profiles: {one_residual}")
    print(f"three-port profiles: {three_port}")


if __name__ == "__main__":
    main()
