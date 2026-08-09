#!/usr/bin/env python3
"""Independent audit of the embedded-P3 generic H31 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

THEOREM = (
    HERE / "P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
)
PRIMARY = (
    HERE / "verify_p5_h31_embedded_p3_component_generic_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=3))
ALPHA = (
    (-1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
)
BETA = (
    (-1, 0, 1),
    (1, 1, 0),
    (-1, 0, 1),
)
SIGMA = {
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 0),
    (0, 1, -1),
    (1, 0, -1),
    (0, 1, 1),
    (1, -1, 0),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_top(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    """Coefficient of X_1 X_2 X_3 by subset dynamic programming."""
    coefficients = {0: 1}
    for row in rows:
        updated: dict[int, int] = {}
        for support, coefficient in coefficients.items():
            for coordinate, entry in enumerate(row):
                bit = 1 << coordinate
                if support & bit:
                    continue
                target = support | bit
                updated[target] = (
                    updated.get(target, 0) + coefficient * entry
                ) % prime
        coefficients = updated
    return coefficients.get(7, 0)


def insertion_matrix(
    point: tuple[int, int, int], prime: int
) -> list[list[int]]:
    rows = []
    for word in WORDS[:-1]:
        selected = tuple(
            BETA[mode] if word[mode] else ALPHA[mode]
            for mode in range(3)
        )
        coefficients = [0] * 6
        for mode in range(3):
            other = tuple(
                selected[index]
                for index in range(3)
                if index != mode
            )
            column = mode if word[mode] == 0 else 3 + mode
            coefficients[column] = squarefree_top(
                (point,) + other, prime
            )
        rows.append([entry % prime for entry in coefficients])
    return rows


def rref_mod(
    matrix: list[list[int]], prime: int
) -> tuple[list[list[int]], list[int]]:
    result = [row[:] for row in matrix]
    row_count = len(result)
    column_count = len(result[0]) if result else 0
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if result[row][column] % prime
            ),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = (
            result[selected],
            result[pivot_row],
        )
        inverse = pow(result[pivot_row][column] % prime, -1, prime)
        result[pivot_row] = [
            entry * inverse % prime for entry in result[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            multiplier = result[row][column] % prime
            if multiplier:
                result[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(
                        result[row], result[pivot_row], strict=True
                    )
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return result, pivots


def nullspace_mod(
    matrix: list[list[int]], prime: int
) -> list[list[int]]:
    reduced, pivots = rref_mod(matrix, prime)
    free = [
        column
        for column in range(len(matrix[0]))
        if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [0] * len(matrix[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % prime
        basis.append(vector)
    return basis


def projective_points(prime: int):
    for second in range(prime):
        for third in range(prime):
            yield (1, second, third)
    for third in range(prime):
        yield (0, 1, third)
    yield (0, 0, 1)


def normalize_projective(
    point: tuple[int, int, int], prime: int
) -> tuple[int, int, int]:
    first = next(entry for entry in point if entry % prime)
    inverse = pow(first % prime, -1, prime)
    return tuple(entry * inverse % prime for entry in point)


def in_expected_locus(
    point: tuple[int, int, int], prime: int
) -> bool:
    p, q, rho = point
    line_values = (
        p - q - rho,
        p - q + rho,
        p + q + rho,
    )
    coordinate_point = sum(entry % prime != 0 for entry in point) == 1
    return coordinate_point or any(value % prime == 0 for value in line_values)


def audit_prime(prime: int) -> dict[str, int]:
    rank_drop_count = 0
    expected_count = 0
    for point in projective_points(prime):
        matrix = insertion_matrix(point, prime)
        _, pivots = rref_mod(matrix, prime)
        drops = len(pivots) < 6
        expected = in_expected_locus(point, prime)
        assert drops == expected
        rank_drop_count += int(drops)
        expected_count += int(expected)

    sigma_mod = {
        normalize_projective(
            tuple(entry % prime for entry in point), prime
        )
        for point in SIGMA
    }
    source_alpha = (1, 2, 4)
    source_beta = (0, 1, 3)
    source_points = [
        tuple(
            (source_beta[index] + parameter * source_alpha[index])
            % prime
            for index in range(3)
        )
        for parameter in range(prime)
    ] + [source_alpha]
    normalized_source = {
        normalize_projective(point, prime) for point in source_points
    }
    assert len(normalized_source) == prime + 1
    assert normalized_source.isdisjoint(sigma_mod)

    source_rank_drops = 0
    for point in normalized_source:
        matrix = insertion_matrix(point, prime)
        kernel = nullspace_mod(matrix, prime)
        if kernel:
            source_rank_drops += 1
            assert len(kernel) == 1
            assert kernel[0][:3] == [0, 0, 0]
    assert source_rank_drops == 3

    return {
        "projective_points": prime * prime + prime + 1,
        "rank_drop_points": rank_drop_count,
        "expected_rank_drop_points": expected_count,
        "source_line_points": prime + 1,
        "source_line_rank_drops": source_rank_drops,
    }


def main() -> None:
    for word in WORDS:
        rows = tuple(
            BETA[mode] if word[mode] else ALPHA[mode]
            for mode in range(3)
        )
        value = squarefree_top(rows, 1_000_003)
        expected = 1_000_001 if word == (1, 1, 1) else 0
        assert value == expected

    audits = {str(prime): audit_prime(prime) for prime in (101, 103)}
    output = {
        "verified": True,
        "method": (
            "independent squarefree subset multiplication and "
            "projective finite-field rank audit"
        ),
        "primes": audits,
        "pure_P3_nonzero_word": "111",
        "pure_P3_nonzero_coefficient": "-2",
        "rank_drop_locus_matches_three_lines_plus_three_points": True,
        "sample_projected_line_avoids_nine_exceptional_points": True,
        "sample_projected_line_rank_jumps": 3,
        "all_sample_rank_jump_kernels_kill_alpha_diagonal": True,
        "generic_marked_H31_fibre_empty": True,
        "finite_field_audit_is_theorem": False,
        "global_problem_resolved": False,
        "dependencies": {
            THEOREM.name: sha256(THEOREM),
            PRIMARY.name: sha256(PRIMARY),
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
