#!/usr/bin/env python3
"""Verify the q5_221 embedded-P4 hyperplane-incidence reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md"
PERMUTATIONS_FOUR = tuple(itertools.permutations(range(4)))
# Only the two multiplicity-two colours may be swapped.  Colour two is
# the distinguished singleton colour in normalized q5_221.
ROW_PERMUTATIONS = ((0, 1, 2), (1, 0, 2))
COLUMN_PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contracted_p5(
    covector: tuple[int, ...],
) -> dict[tuple[int, ...], int]:
    result = {}
    for indices in itertools.product(range(5), repeat=4):
        if len(set(indices)) != 4:
            result[indices] = 0
            continue
        missing = next(index for index in range(5) if index not in indices)
        result[indices] = covector[missing]
    return result


def symmetrized_product(
    factors: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], int]:
    result = {}
    for indices in itertools.product(range(5), repeat=4):
        result[indices] = sum(
            math.prod(
                factors[factor][indices[permutation[factor]]]
                for factor in range(4)
            )
            for permutation in PERMUTATIONS_FOUR
        )
    return result


def contracted_p5_twice(
    first_covector: tuple[int, ...],
    second_covector: tuple[int, ...],
) -> dict[tuple[int, ...], int]:
    result = {}
    for indices in itertools.product(range(5), repeat=3):
        if len(set(indices)) != 3:
            result[indices] = 0
            continue
        complement = tuple(
            index for index in range(5) if index not in indices
        )
        first, second = complement
        result[indices] = (
            first_covector[first] * second_covector[second]
            + first_covector[second] * second_covector[first]
        )
    return result


def symmetrized_product_three(
    factors: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], int]:
    result = {}
    for indices in itertools.product(range(5), repeat=3):
        result[indices] = sum(
            math.prod(
                factors[factor][indices[permutation[factor]]]
                for factor in range(3)
            )
            for permutation in itertools.permutations(range(3))
        )
    return result


def proportional_nonzero(
    left: dict[tuple[int, ...], int],
    right: dict[tuple[int, ...], int],
) -> bool:
    ratio = None
    for key in left:
        if not right[key]:
            if left[key]:
                return False
            continue
        candidate = Fraction(left[key], right[key])
        if ratio is None:
            ratio = candidate
        elif candidate != ratio:
            return False
    return ratio not in (None, 0)


def canonical_incidence(bits: tuple[int, ...]) -> str:
    candidates = []
    for rows in ROW_PERMUTATIONS:
        for columns in COLUMN_PERMUTATIONS:
            candidates.append(
                "".join(
                    str(bits[4 * rows[row] + columns[column]])
                    for row in range(3)
                    for column in range(4)
                )
            )
    return min(candidates)


def matrix_rank(rows: tuple[tuple[int, ...], ...]) -> int:
    matrix = [
        [Fraction(value) for value in row]
        for row in rows
    ]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [
            value / pivot_value for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right
                for left, right in zip(
                    matrix[row],
                    matrix[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def main() -> None:
    standard = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    covectors = (
        (1, 1, 0, 0, 0),
        (0, 0, 1, 1, 0),
        (0, 0, 0, 0, 1),
    )
    factor_sets = (
        (
            (1, 1, 0, 0, 0),
            standard[2],
            standard[3],
            standard[4],
        ),
        (
            standard[0],
            standard[1],
            (0, 0, 1, 1, 0),
            standard[4],
        ),
        (
            standard[0],
            standard[1],
            standard[2],
            standard[3],
        ),
    )
    for covector, factors in zip(covectors, factor_sets, strict=True):
        assert contracted_p5(covector) == symmetrized_product(factors)

    normals = (
        (1, -1, 0, 0, 0),
        (0, 0, 1, -1, 0),
        (0, 0, 0, 0, 1),
    )
    for normal, factors in zip(normals, factor_sets, strict=True):
        assert all(
            sum(
                first * second
                for first, second in zip(normal, factor, strict=True)
            )
            == 0
            for factor in factors
        )
    assert len(
        {
            tuple(normal)
            for normal in normals
        }
    ) == 3
    assert matrix_rank(normals) == 3

    h0_basis = factor_sets[0]
    containing_rows = (
        normals[0],
        standard[2],
        standard[3],
    )
    avoiding_rows = (
        standard[0],
        standard[2],
        standard[3],
    )
    containing_restriction = tuple(
        tuple(
            sum(
                first * second
                for first, second in zip(row, basis, strict=True)
            )
            for basis in h0_basis
        )
        for row in containing_rows
    )
    avoiding_restriction = tuple(
        tuple(
            sum(
                first * second
                for first, second in zip(row, basis, strict=True)
            )
            for basis in h0_basis
        )
        for row in avoiding_rows
    )
    assert matrix_rank(containing_restriction) == 2
    assert matrix_rank(avoiding_restriction) == 3

    orbit_counts = {}
    for bits in itertools.product((0, 1), repeat=12):
        if any(
            sum(bits[4 * row : 4 * row + 4]) != 2
            for row in range(3)
        ):
            continue
        key = canonical_incidence(bits)
        orbit_counts[key] = orbit_counts.get(key, 0) + 1
    representative_rows = (
        ("0011", "0011", "0011"),
        ("0011", "0011", "0101"),
        ("0011", "0101", "0011"),
        ("0011", "0011", "1100"),
        ("0011", "1100", "0011"),
        ("0011", "0101", "0110"),
        ("0011", "0101", "1001"),
        ("0011", "0101", "1010"),
        ("0101", "1010", "0011"),
    )
    expected_keys = {
        canonical_incidence(
            tuple(int(bit) for row in rows for bit in row)
        )
        for rows in representative_rows
    }
    assert len(expected_keys) == 9
    assert set(orbit_counts) == expected_keys

    x_plus = (1, 1, 0, 0, 0)
    x_minus = (1, -1, 0, 0, 0)
    y_plus = (0, 0, 1, 1, 0)
    y_minus = (0, 0, 1, -1, 0)
    z = standard[4]
    residual_factor_sets = {
        "01": (x_plus, y_minus, z),
        "10": (x_minus, y_plus, z),
        "02": (x_plus, standard[2], standard[3]),
        "20": (x_minus, standard[2], standard[3]),
        "12": (standard[0], standard[1], y_plus),
        "21": (standard[0], standard[1], y_minus),
    }
    residual_annihilators = {
        "01": (x_minus, y_plus),
        "10": (x_plus, y_minus),
        "02": (x_minus, z),
        "20": (x_plus, z),
        "12": (y_minus, z),
        "21": (y_plus, z),
    }
    u_vectors = (x_plus, y_plus, z)
    h_vectors = (x_minus, y_minus, z)
    for key, factors in residual_factor_sets.items():
        first, second = (int(character) for character in key)
        assert proportional_nonzero(
            contracted_p5_twice(
                u_vectors[first],
                h_vectors[second],
            ),
            symmetrized_product_three(factors),
        )
        annihilators = residual_annihilators[key]
        assert matrix_rank(factors) == 3
        assert matrix_rank(annihilators) == 2
        assert all(
            sum(
                first * second
                for first, second in zip(
                    annihilator,
                    factor,
                    strict=True,
                )
            )
            == 0
            for annihilator in annihilators
            for factor in factors
        )

    output = {
        "verified": True,
        "field": "C",
        "embedded_P4_contractions_checked": 3,
        "hyperplane_normals": normals,
        "hyperplane_normal_rank": 3,
        "representative_containing_restriction_rank": (
            matrix_rank(containing_restriction)
        ),
        "representative_avoiding_restriction_rank": (
            matrix_rank(avoiding_restriction)
        ),
        "rank_drop_incidence_lower_bounds": [2, 2, 2],
        "minimal_incidence_matrices_checked": sum(orbit_counts.values()),
        "minimal_marked_incidence_orbits": len(orbit_counts),
        "underlying_uncoloured_incidence_orbits": 6,
        "canonical_incidence_orbits": sorted(orbit_counts),
        "orbit_labelled_counts": dict(sorted(orbit_counts.items())),
        "cross_contraction_residuals_checked": sorted(
            residual_factor_sets
        ),
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_hyperplane_incidence_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
