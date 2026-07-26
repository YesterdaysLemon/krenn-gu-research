#!/usr/bin/env python3
"""Independent finite-field audit of the P_4 subrank formulas."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 5
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rank_mod(rows: list[list[int]]) -> int:
    matrix = [[value % PRIME for value in row] for row in rows]
    if not matrix:
        return 0
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
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, PRIME)
        matrix[pivot_row] = [
            value * inverse % PRIME for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    first = next(value for value in vector if value)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in vector)


def normals() -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                canonical(vector)
                for vector in itertools.product(range(PRIME), repeat=4)
                if any(vector)
            }
        )
    )


def basis(normal: tuple[int, ...]) -> list[list[int]]:
    pivot = next(index for index, value in enumerate(normal) if value)
    vectors = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [0] * 4
        vector[free] = 1
        vector[pivot] = (
            -normal[free] * pow(normal[pivot], -1, PRIME)
        ) % PRIME
        vectors.append(vector)
    return vectors


def pair_image_rank(
    left_normal: tuple[int, ...], right_normal: tuple[int, ...]
) -> int:
    image_vectors = []
    for left in basis(left_normal):
        for right in basis(right_normal):
            image_vectors.append(
                [
                    (
                        left[first] * right[second]
                        + left[second] * right[first]
                    )
                    % PRIME
                    for first, second in PAIRS
                ]
            )
    return rank_mod(image_vectors)


def proportional(
    left: tuple[int, ...], right: tuple[int, ...]
) -> bool:
    # Projective normals are canonical already.
    return left == right


def main() -> None:
    projective_normals = normals()
    rank_counts: Counter[int] = Counter()
    equal_support_counts: Counter[tuple[int, int]] = Counter()
    independent_exceptional = 0
    ordered_pairs_checked = 0

    for left in projective_normals:
        for right in projective_normals:
            ordered_pairs_checked += 1
            actual = pair_image_rank(left, right)
            rank_counts[actual] += 1
            if proportional(left, right):
                support = sum(value != 0 for value in left)
                expected = support + 2
                equal_support_counts[(support, actual)] += 1
            else:
                left_squares = tuple(value * value % PRIME for value in left)
                right_squares = tuple(value * value % PRIME for value in right)
                square_proportional = canonical(left_squares) == canonical(
                    right_squares
                )
                expected = 5 if square_proportional else 6
                if square_proportional:
                    independent_exceptional += 1
            assert actual == expected

    # Independent reconstruction of the special-edge covering fact.
    perfect_matchings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    equivalence_patterns_checked = 0
    covering_patterns = 0
    for labels in itertools.product(range(4), repeat=4):
        mapping = {}
        canonical_labels = []
        for label in labels:
            mapping.setdefault(label, len(mapping))
            canonical_labels.append(mapping[label])
        if tuple(canonical_labels) != labels:
            continue
        equivalence_patterns_checked += 1
        covers = all(
            labels[a] == labels[b] or labels[c] == labels[d]
            for (a, b), (c, d) in perfect_matchings
        )
        if covers:
            covering_patterns += 1
            assert max(labels.count(label) for label in set(labels)) >= 3

    # Exhaust all finite-field cubes and compare coefficient support with
    # l*span(mn,ln,lm).  Cubes use characteristic five, so polarization
    # has no characteristic-two or characteristic-three collapse.
    allowed_exponents = {(1, 1, 1), (2, 0, 1), (2, 1, 0)}
    nonzero_cubes_in_slice_space = 0
    nonzero_linear_forms = 0
    for alpha, beta, gamma in itertools.product(range(PRIME), repeat=3):
        if not (alpha or beta or gamma):
            continue
        nonzero_linear_forms += 1
        coefficients = {}
        for i in range(4):
            for j in range(4 - i):
                k = 3 - i - j
                # Direct expansion coefficient 3!/(i!j!k!).
                denominator = 1
                for value in (i, j, k):
                    for factor in range(2, value + 1):
                        denominator = denominator * factor % PRIME
                multinomial = 6 * pow(denominator, -1, PRIME) % PRIME
                coefficient = (
                    multinomial
                    * pow(alpha, i, PRIME)
                    * pow(beta, j, PRIME)
                    * pow(gamma, k, PRIME)
                ) % PRIME
                coefficients[(i, j, k)] = coefficient
        if all(
            coefficient == 0 or exponent in allowed_exponents
            for exponent, coefficient in coefficients.items()
        ):
            nonzero_cubes_in_slice_space += 1
    assert nonzero_cubes_in_slice_space == 0

    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "projective_normals": len(projective_normals),
        "ordered_normal_pairs_checked": ordered_pairs_checked,
        "pair_image_rank_counts": dict(sorted(rank_counts.items())),
        "equal_normal_support_rank_counts": {
            f"support_{support}_rank_{rank}": count
            for (support, rank), count in sorted(equal_support_counts.items())
        },
        "independent_square_proportional_pairs": independent_exceptional,
        "equivalence_patterns_checked": equivalence_patterns_checked,
        "covering_equivalence_patterns": covering_patterns,
        "nonzero_linear_forms_checked": nonzero_linear_forms,
        "nonzero_cubes_in_support_two_slice_space": (
            nonzero_cubes_in_slice_space
        ),
        "primary_artifact": (
            ROOT / "tmp" / "fourth_order_permanent_subrank_verified.json"
        ).relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(
            ROOT / "tmp" / "fourth_order_permanent_subrank_verified.json"
        ),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "fourth_order_permanent_subrank_audited.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
