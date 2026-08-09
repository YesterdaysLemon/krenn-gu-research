#!/usr/bin/env python3
"""Independent audit of the P_6 kernel and natural-lift obstructions."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "tmp" / "p6_kernel_natural_lift_verified.json"
TARGET4 = tuple(itertools.product(range(3), repeat=4))
PERM6 = tuple(itertools.permutations(range(6)))

MAPS = (
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


def injective_sum(
    available_sources: tuple[int, ...], colours: tuple[int, ...]
) -> int:
    """Subset-DP sum, independent of the primary permutation expansion."""

    assert len(available_sources) == 4
    values = {0: 1}
    for mode in range(4):
        next_values: dict[int, int] = {}
        for mask, subtotal in values.items():
            for local_index, source in enumerate(available_sources):
                bit = 1 << local_index
                if mask & bit:
                    continue
                if source == 5:
                    entry = 0
                else:
                    entry = MAPS[mode][source][colours[mode]]
                next_mask = mask | bit
                next_values[next_mask] = (
                    next_values.get(next_mask, 0) + subtotal * entry
                )
        values = next_values
    return values[(1 << 4) - 1]


def p5_row(colours: tuple[int, ...]) -> list[int]:
    return [
        injective_sum(
            tuple(source for source in range(5) if source != missing),
            colours,
        )
        for missing in range(5)
    ]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    rows = [[value % prime for value in row] for row in matrix]
    pivot_row = 0
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
        scale = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * scale % prime for value in rows[pivot_row]]
        for row in range(pivot_row + 1, len(rows)):
            factor = rows[row][column]
            if factor:
                rows[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(rows[row], rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def alternating_components(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[frozenset[int], ...]:
    """Left-vertex sets of components in two bipartite matchings."""

    right_to_left_first = {right: left for left, right in enumerate(first)}
    unseen = set(range(6))
    components = []
    while unseen:
        start = min(unseen)
        component = set()
        current = start
        while current not in component:
            component.add(current)
            unseen.remove(current)
            current = right_to_left_first[second[current]]
        assert current == start
        components.append(frozenset(component))
    return tuple(components)


def main() -> None:
    rows = [p5_row(colours) for colours in TARGET4]
    off_rows = [
        row
        for colours, row in zip(TARGET4, rows)
        if len(set(colours)) > 1
    ]
    generator = (1, 1, 1, 1, 0)
    assert all(
        sum(entry * value for entry, value in zip(row, generator)) == 0
        for row in off_rows
    )
    diagonal_image = []
    for colour in range(3):
        row = rows[TARGET4.index((colour,) * 4)]
        diagonal_image.append(
            sum(entry * value for entry, value in zip(row, generator))
        )
    assert diagonal_image == [12, 12, 12]

    finite_field_ranks = {}
    for prime in (5, 7):
        rank = rank_mod(off_rows, prime)
        assert rank == 4
        finite_field_ranks[f"F_{prime}"] = rank

    # Rebuild all coordinate double contractions via subset DP.  The result is
    # nonzero only when the two singled-out modes consume source 5 and one
    # source in 0,...,4 in either order.
    double_contraction_checks = 0
    for first_source in range(6):
        for fifth_source in range(6):
            available = tuple(
                source
                for source in range(6)
                if source not in (first_source, fifth_source)
            )
            for index, colours in enumerate(TARGET4):
                actual = (
                    0
                    if first_source == fifth_source
                    else injective_sum(available, colours)
                )
                expected = 0
                if first_source < 5 and fifth_source == 5:
                    expected = rows[index][first_source]
                elif first_source == 5 and fifth_source < 5:
                    expected = rows[index][fifth_source]
                assert actual == expected
                double_contraction_checks += 1

    identity = tuple(range(6))
    hamiltonian_partners = []
    cycle_switch_checks = 0
    component_histogram: dict[int, int] = {}
    for permutation in PERM6:
        components = alternating_components(identity, permutation)
        component_histogram[len(components)] = (
            component_histogram.get(len(components), 0) + 1
        )
        if len(components) == 1:
            assert len(components[0]) == 6
            hamiltonian_partners.append(permutation)
            continue
        switched = components[0]
        assert 0 < len(switched) < 6
        mixed_matching = tuple(
            permutation[mode] if mode in switched else identity[mode]
            for mode in range(6)
        )
        assert sorted(mixed_matching) == list(range(6))
        cycle_switch_checks += 1

    assert len(hamiltonian_partners) == 120
    pairwise_hamiltonian_checks = 0
    pairwise_hamiltonian_survivors = 0
    for first in hamiltonian_partners:
        for second in hamiltonian_partners:
            pairwise_hamiltonian_checks += 1
            if len(alternating_components(first, second)) == 1:
                pairwise_hamiltonian_survivors += 1
    assert pairwise_hamiltonian_checks == 14_400
    assert pairwise_hamiltonian_survivors == 0
    assert cycle_switch_checks == 600

    # Independent profile census: assign one of the seven proper missing
    # masks to each mode, then require that each colour is missing at most
    # once.  This starts from blocker modes rather than colour choices.
    profile_counts: Counter[tuple[int, ...]] = Counter()
    labelled_missing_patterns = 0
    for masks in itertools.product(range(0b111), repeat=6):
        if any(
            sum(bool(mask & (1 << colour)) for mask in masks) > 1
            for colour in range(3)
        ):
            continue
        profile = tuple(
            sorted(
                (mask.bit_count() for mask in masks if mask),
                reverse=True,
            )
        )
        profile_counts[profile] += 1
        labelled_missing_patterns += 1
    expected_profiles = {
        (): 1,
        (1,): 18,
        (1, 1): 90,
        (1, 1, 1): 120,
        (2,): 18,
        (2, 1): 90,
    }
    assert dict(profile_counts) == expected_profiles
    assert labelled_missing_patterns == 337

    # Use different support-two generators from the primary verifier and
    # check the local rank/incidence/port assertions over two finite fields.
    local_model_checks = 0
    for mask in range(0b111):
        support = [colour for colour in range(3) if mask & (1 << colour)]
        if not support:
            kernel = [0, 0, 0]
            roots = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            port = [1, 1, 1]
        elif len(support) == 1:
            kernel = [int(colour == support[0]) for colour in range(3)]
            roots = [
                [int(colour == blocked) for colour in range(3)]
                for blocked in range(3)
                if blocked != support[0]
            ]
            port = kernel[:]
        else:
            first, second = support
            blocked = next(
                colour for colour in range(3) if colour not in support
            )
            kernel = [0, 0, 0]
            kernel[first] = 1
            kernel[second] = 2
            blocked_row = [int(colour == blocked) for colour in range(3)]
            relation_row = [0, 0, 0]
            relation_row[first] = 2
            relation_row[second] = -1
            roots = [blocked_row, relation_row]
            port = [int(colour == first) for colour in range(3)]
        roots += [[0, 0, 0]] * (5 - len(roots))
        for prime in (5, 7):
            root_rank = rank_mod(roots, prime)
            full_rank = rank_mod(roots + [port], prime)
            assert root_rank == (3 if mask == 0 else 2)
            assert full_rank == 3
            for colour in range(3):
                coordinate = [int(index == colour) for index in range(3)]
                blocked = rank_mod(roots + [coordinate], prime) == root_rank
                assert blocked == (not bool(mask & (1 << colour)))
            if mask:
                assert all(
                    sum(row[colour] * kernel[colour] for colour in range(3))
                    % prime
                    == 0
                    for row in roots
                )
                assert (
                    sum(
                        port[colour] * kernel[colour] for colour in range(3)
                    )
                    % prime
                )
            local_model_checks += 1

    primary_data = json.loads(PRIMARY.read_text(encoding="utf-8"))
    assert primary_data["verified"] is True
    assert primary_data["p5_off_diagonal_rank"] == 4
    assert primary_data["surviving_pairwise_six_cycle_triples"] == 0
    assert primary_data["labelled_common_port_missing_patterns"] == 337

    output = {
        "verified": True,
        "method": "subset DP, modular row reduction, bipartite graph walks",
        "finite_field_off_diagonal_ranks": finite_field_ranks,
        "p5_kernel_generator": list(generator),
        "p5_kernel_diagonal_image": diagonal_image,
        "double_contraction_coefficients_checked": double_contraction_checks,
        "s6_cycle_component_histogram": {
            str(key): value for key, value in sorted(component_histogram.items())
        },
        "proper_cycle_switches_checked_after_normalization": (
            cycle_switch_checks
        ),
        "pairwise_hamiltonian_partner_pairs_checked": (
            pairwise_hamiltonian_checks
        ),
        "pairwise_hamiltonian_survivors": pairwise_hamiltonian_survivors,
        "labelled_common_port_missing_patterns": labelled_missing_patterns,
        "common_port_profile_counts": {
            "+".join(map(str, profile)) if profile else "empty": count
            for profile, count in profile_counts.items()
        },
        "finite_field_common_port_local_model_checks": local_model_checks,
        "primary_artifact": PRIMARY.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
        "unrestricted_p6_resolved": False,
    }
    output_path = ROOT / "tmp" / "p6_kernel_natural_lift_audited.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
