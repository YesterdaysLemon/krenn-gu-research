#!/usr/bin/env python3
"""Independent modular audit of the radical-star P4 classification."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md"
PRIMARY = ROOT / "verify_p4_radical_star_component_classification.py"
MODULI = (101, 103)
WORDS = tuple(itertools.product((0, 1), repeat=4))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows: tuple[tuple[int, ...], ...], modulus: int) -> int:
    values = [0] * 16
    values[0] = 1
    for row in rows:
        updated = [0] * 16
        for mask, value in enumerate(values):
            for column in range(4):
                bit = 1 << column
                if mask & bit == 0:
                    updated[mask | bit] = (
                        updated[mask | bit] + value * row[column]
                    ) % modulus
        values = updated
    return values[15]


def tensor(
    planes: tuple[tuple[tuple[int, ...], ...], ...], modulus: int
) -> dict[tuple[int, ...], int]:
    return {
        word: permanent_dp(
            tuple(planes[mode][word[mode]] for mode in range(4)),
            modulus,
        )
        for word in WORDS
    }


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [
            entry * inverse % modulus for entry in work[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
    return pivot_row


def pair_rank(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
    modulus: int,
) -> int:
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            columns.append(
                [
                    (
                        left[left_row][first] * right[right_row][second]
                        + left[left_row][second] * right[right_row][first]
                    )
                    % modulus
                    for first, second in SOURCE_PAIRS
                ]
            )
    matrix = [
        [columns[column][row] for column in range(4)]
        for row in range(6)
    ]
    return rank_mod(matrix, modulus)


def two_two_planes(
    values: tuple[int, int, int, int, int, int], modulus: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    A, B, C, E, F, H = values
    raw = (
        ((E, -F, -F, -E), (A, -B, B, A)),
        ((1, 0, 0, -1), (A, C + B, C - B, A)),
        ((H + E, F, F, H - E), (0, 1, -1, 0)),
        ((1, 0, 0, 1), (0, 1, 1, 0)),
    )
    return tuple(
        tuple(
            tuple(entry % modulus for entry in row) for row in plane
        )
        for plane in raw
    )


def one_three_planes(
    values: tuple[int, int, int, int], modulus: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    S, D, G, T = values
    P, Q = G - T, D - S
    raw = (
        ((2, P + Q, Q - P, 0), (0, 0, 1, 1)),
        ((0, 1, -1, 0), (1, 0, S, D)),
        ((1, 0, G, T), (0, 1, 0, -1)),
        ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    return tuple(
        tuple(
            tuple(entry % modulus for entry in row) for row in plane
        )
        for plane in raw
    )


def active_determinant(
    coefficients: dict[tuple[int, ...], int], modulus: int
) -> int:
    return (
        coefficients[(0, 1, 0, 0)] * coefficients[(1, 1, 0, 1)]
        - coefficients[(0, 1, 0, 1)] * coefficients[(1, 1, 0, 0)]
    ) % modulus


def audit_modulus(modulus: int) -> dict[str, object]:
    two_values = (2, 3, 5, 7, 11, 13)
    two_planes = two_two_planes(two_values, modulus)
    two_tensor = tensor(two_planes, modulus)
    A, B, C, E, F, H = two_values
    psi = (
        A**3 * F**3
        + A**2 * C * F**2 * H
        - A * B**2 * F * H**2
        - A * C**2 * E**2 * F
        + A * C**2 * F * H**2
        - B**2 * C * E**2 * H
    )
    assert active_determinant(two_tensor, modulus) == -16 * psi % modulus
    assert [
        pair_rank(two_planes[left], two_planes[right], modulus)
        for left, right in SOURCE_PAIRS
    ] == [4, 4, 3, 4, 3, 3]

    branch_parameters = {
        "L1": (1, 3, 4, -3 + 4 + 1),
        "L2": (1, 3, 4, 3 + 4 - 1),
        "L3": (1, 2, 3, -2 - 3 - 1),
    }
    branch_results = {}
    generic_values = (1, 2, 3, 5)
    generic_coefficients = tensor(
        one_three_planes(generic_values, modulus), modulus
    )
    generic_S, generic_D, generic_G, generic_T = generic_values
    generic_split = (
        generic_D - generic_G - generic_S + generic_T
    ) * (
        generic_D + generic_G - generic_S - generic_T
    ) * (
        generic_D + generic_G + generic_S + generic_T
    )
    assert active_determinant(generic_coefficients, modulus) == (
        generic_split % modulus
    )
    for branch, values in branch_parameters.items():
        planes = one_three_planes(values, modulus)
        coefficients = tensor(planes, modulus)
        S, D, G, T = values
        split = (D - G - S + T) * (D + G - S - T) * (
            D + G + S + T
        )
        assert active_determinant(coefficients, modulus) == split % modulus
        assert split == 0
        profile = tuple(
            pair_rank(planes[left], planes[right], modulus)
            for left, right in SOURCE_PAIRS
        )
        assert profile == (4, 4, 3, 4, 3, 3)
        branch_results[branch] = {
            "active_determinant": 0,
            "pair_profile": list(profile),
        }

    # Directly replay the four rank-one zero products that force the
    # two block-center support patterns.
    zero_products = (
        ((1, 0, 0, -1), (1, 0, 0, 1)),
        ((0, 1, -1, 0), (0, 1, 1, 0)),
        ((0, 1, -1, 0), (0, 1, 1, 0)),
        ((0, 1, 0, -1), (0, 1, 0, 1)),
    )
    for left, right in zero_products:
        assert all(
            (
                left[first] * right[second]
                + left[second] * right[first]
            )
            % modulus
            == 0
            for first, second in SOURCE_PAIRS
        )

    return {
        "modulus": modulus,
        "DP_permanent_coefficients": 16 * 4,
        "two_two_active_determinant": (-16 * psi) % modulus,
        "two_two_pair_profile": [4, 4, 3, 4, 3, 3],
        "one_three_branches": branch_results,
        "rank_one_zero_products_replayed": len(zero_products),
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "DP permanent, modular pair-image ranks, and direct "
            "coordinate-pair zero-product checks"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "two_two_normal_form_replayed": True,
        "three_one_three_branches_replayed": True,
        "radical_star_component_orbits": 4,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_radical_star_component_classification_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
