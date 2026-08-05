#!/usr/bin/env python3
"""Primary exact verifier for the P_6 kernel and natural-lift note."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md"
TARGET4 = tuple(itertools.product(range(3), repeat=4))
PERM6 = tuple(itertools.permutations(range(6)))

INTEGER_MAPS = (
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0),
        (-1, -1, 0),
        (0, 0, -1),
    ),
    (
        (1, 1, -2),
        (-2, 1, 1),
        (1, -2, 1),
        (1, 1, 1),
        (1, 1, 1),
    ),
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0),
        (0, -1, -1),
        (-1, 0, 0),
    ),
    (
        (-1, -1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, 1, -1),
        (0, -2, 0),
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contraction_row(colours: tuple[int, ...]) -> list[int]:
    """Five coefficients R(e_s) at one four-mode target word."""

    row = []
    for missing in range(5):
        total = 0
        remaining = tuple(value for value in range(5) if value != missing)
        for source_tuple in itertools.permutations(remaining):
            term = 1
            for mode in range(4):
                term *= INTEGER_MAPS[mode][source_tuple[mode]][colours[mode]]
            total += term
        row.append(total)
    return row


def rref(
    matrix: list[list[int | Fraction]],
) -> tuple[list[list[Fraction]], list[int]]:
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return [], []
    pivot_row = 0
    pivots = []
    for column in range(len(rows[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [
                left - factor * right
                for left, right in zip(rows[row], rows[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows[:pivot_row], pivots


def nullspace(matrix: list[list[int]], columns: int) -> list[list[Fraction]]:
    reduced, pivots = rref(matrix)
    free_columns = [column for column in range(columns) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(vector)
    return basis


def double_contraction_coefficient(
    contracted_source: int,
    fifth_map_source: int,
    colours: tuple[int, ...],
) -> int:
    """Coefficient after two coordinate contractions of zero-extended P_6."""

    if contracted_source == fifth_map_source:
        return 0
    remaining = tuple(
        value
        for value in range(6)
        if value not in (contracted_source, fifth_map_source)
    )
    total = 0
    for source_tuple in itertools.permutations(remaining):
        term = 1
        for mode in range(4):
            source = source_tuple[mode]
            if source == 5:
                term = 0
                break
            term *= INTEGER_MAPS[mode][source][colours[mode]]
        total += term
    return total


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def relative_cycles(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    """Cycles of first^{-1} second on the mode vertices."""

    first_inverse = inverse(first)
    relative = tuple(first_inverse[second[mode]] for mode in range(6))
    unseen = set(range(6))
    cycles = []
    while unseen:
        start = min(unseen)
        cycle = []
        current = start
        while current in unseen:
            unseen.remove(current)
            cycle.append(current)
            current = relative[current]
        assert current == start
        cycles.append(tuple(cycle))
    return tuple(cycles)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(6)
        for right in range(left + 1, 6)
    )
    return -1 if inversions % 2 else 1


def missing_profile(masks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (mask.bit_count() for mask in masks if mask),
            reverse=True,
        )
    )


def canonical_root_rows(mask: int) -> tuple[list[list[int]], list[int]]:
    """A rank-sharp local model for one missing-colour support."""

    if mask == 0:
        return (
            [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]],
            [1, 1, 1],
        )
    support = [colour for colour in range(3) if mask & (1 << colour)]
    assert 1 <= len(support) <= 2
    if len(support) == 1:
        missing = support[0]
        blocked = [colour for colour in range(3) if colour != missing]
        roots = [
            [int(colour == blocked[0]) for colour in range(3)],
            [int(colour == blocked[1]) for colour in range(3)],
        ]
        port = [int(colour == missing) for colour in range(3)]
    else:
        first, second = support
        blocked = next(colour for colour in range(3) if colour not in support)
        roots = [
            [int(colour == blocked) for colour in range(3)],
            [
                int(colour == first) - int(colour == second)
                for colour in range(3)
            ],
        ]
        port = [int(colour == first) for colour in range(3)]
    return roots + [[0, 0, 0]] * (5 - len(roots)), port


def main() -> None:
    contraction_rows = [contraction_row(colours) for colours in TARGET4]
    off_rows = [
        row
        for colours, row in zip(TARGET4, contraction_rows)
        if len(set(colours)) > 1
    ]
    diagonal_rows = [
        contraction_rows[TARGET4.index((colour,) * 4)]
        for colour in range(3)
    ]
    _, pivots = rref(off_rows)
    kernel = nullspace(off_rows, 5)
    expected_kernel = [
        [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(0)]
    ]
    assert len(pivots) == 4
    assert kernel == expected_kernel
    kernel_generator = [1, 1, 1, 1, 0]
    diagonal_image = [
        sum(left * right for left, right in zip(row, kernel_generator))
        for row in diagonal_rows
    ]
    assert diagonal_image == [12, 12, 12]

    # Check every matrix-unit choice for the arbitrary fifth map.  Linearity
    # then proves Phi(z)=R(z) tensor L(e_5) on E.
    zero_row_basis_checks = 0
    for contracted_source in range(6):
        for fifth_map_source in range(6):
            for fifth_target_colour in range(3):
                for target_colour in range(3):
                    for index, colours in enumerate(TARGET4):
                        actual = (
                            double_contraction_coefficient(
                                contracted_source,
                                fifth_map_source,
                                colours,
                            )
                            if target_colour == fifth_target_colour
                            else 0
                        )
                        expected = 0
                        if target_colour == fifth_target_colour:
                            if contracted_source < 5 and fifth_map_source == 5:
                                expected = contraction_rows[index][contracted_source]
                            elif contracted_source == 5 and fifth_map_source < 5:
                                expected = contraction_rows[index][fifth_map_source]
                        assert actual == expected
                        zero_row_basis_checks += 1

    # Every non-Hamiltonian relative permutation supplies a proper alternating
    # cycle switch and therefore a forbidden mixed coordinate coefficient.
    cycle_switch_checks = 0
    single_cycle_pairs = 0
    for first in PERM6:
        for second in PERM6:
            cycles = relative_cycles(first, second)
            if len(cycles) == 1:
                assert len(cycles[0]) == 6
                single_cycle_pairs += 1
                continue
            switched_modes = set(cycles[0])
            assert switched_modes
            assert len(switched_modes) < 6
            selected_sources = tuple(
                second[mode] if mode in switched_modes else first[mode]
                for mode in range(6)
            )
            assert sorted(selected_sources) == list(range(6))
            cycle_switch_checks += 1

    identity = tuple(range(6))
    six_cycles = tuple(
        permutation
        for permutation in PERM6
        if len(relative_cycles(identity, permutation)) == 1
    )
    assert len(six_cycles) == 120
    assert all(permutation_sign(permutation) == -1 for permutation in six_cycles)

    candidate_triples = 0
    surviving_triples = 0
    for first_relative in six_cycles:
        first_inverse = inverse(first_relative)
        for second_relative in six_cycles:
            candidate_triples += 1
            last_relative = tuple(
                first_inverse[second_relative[mode]] for mode in range(6)
            )
            assert permutation_sign(last_relative) == 1
            if len(relative_cycles(identity, last_relative)) == 1:
                surviving_triples += 1
    assert candidate_triples == 14_400
    assert surviving_triples == 0
    assert single_cycle_pairs == 720 * 120
    assert cycle_switch_checks == 720 * 600

    # Each colour chooses either no missing blocker or one of six.  Exclude a
    # mode missing all three colours, since every mode lies in the blocker
    # union.  This reconstructs the complete common-port profile census.
    profile_counts: Counter[tuple[int, ...]] = Counter()
    labelled_missing_patterns = 0
    for missing_modes in itertools.product(range(-1, 6), repeat=3):
        masks = [0] * 6
        for colour, mode in enumerate(missing_modes):
            if mode >= 0:
                masks[mode] |= 1 << colour
        if any(mask == 0b111 for mask in masks):
            continue
        assert sum(mask.bit_count() for mask in masks) <= 3
        nonempty_masks = [mask for mask in masks if mask]
        assert all(
            left & right == 0
            for index, left in enumerate(nonempty_masks)
            for right in nonempty_masks[index + 1 :]
        )
        profile_counts[missing_profile(tuple(masks))] += 1
        labelled_missing_patterns += 1

    expected_profile_counts = {
        (): 1,
        (1,): 18,
        (1, 1): 90,
        (1, 1, 1): 120,
        (2,): 18,
        (2, 1): 90,
    }
    assert dict(profile_counts) == expected_profile_counts
    assert labelled_missing_patterns == 337

    # Canonical row-space models audit the rank/kernel claims for every local
    # missing mask.  They show that incidence alone does not remove any of the
    # six global profiles.
    local_models = {}
    for mask in range(0b111):
        root_rows, port_row = canonical_root_rows(mask)
        root_rank = len(rref(root_rows)[1])
        full_rank = len(rref(root_rows + [port_row])[1])
        expected_root_rank = 3 if mask == 0 else 2
        assert root_rank == expected_root_rank
        assert full_rank == 3
        root_kernel = nullspace(root_rows, 3)
        if mask == 0:
            assert root_kernel == []
            kernel_support: list[int] = []
        else:
            assert len(root_kernel) == 1
            kernel_vector = root_kernel[0]
            kernel_support = [
                colour for colour, value in enumerate(kernel_vector) if value
            ]
            expected_support = [
                colour for colour in range(3) if mask & (1 << colour)
            ]
            assert kernel_support == expected_support
            assert sum(
                Fraction(entry) * value
                for entry, value in zip(port_row, kernel_vector)
            )
        local_models[str(mask)] = {
            "missing_colours": [
                colour for colour in range(3) if mask & (1 << colour)
            ],
            "root_rank": root_rank,
            "full_rank": full_rank,
            "kernel_support": kernel_support,
        }

    output = {
        "verified": True,
        "field": "C",
        "p5_contraction_target_words": len(TARGET4),
        "p5_off_diagonal_rows": len(off_rows),
        "p5_off_diagonal_rank": len(pivots),
        "p5_off_diagonal_kernel": kernel_generator,
        "p5_kernel_diagonal_image": diagonal_image,
        "zero_row_basis_coefficients_checked": zero_row_basis_checks,
        "s6_permutations": len(PERM6),
        "ordered_relative_single_cycle_pairs": single_cycle_pairs,
        "proper_cycle_switches_checked": cycle_switch_checks,
        "six_cycles": len(six_cycles),
        "candidate_pairwise_six_cycle_triples_after_normalization": (
            candidate_triples
        ),
        "surviving_pairwise_six_cycle_triples": surviving_triples,
        "labelled_common_port_missing_patterns": labelled_missing_patterns,
        "common_port_profile_counts": {
            "+".join(map(str, profile)) if profile else "empty": count
            for profile, count in profile_counts.items()
        },
        "canonical_common_port_local_models": local_models,
        "unrestricted_p6_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
    }
    output_path = ROOT / "tmp" / "p6_kernel_natural_lift_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
