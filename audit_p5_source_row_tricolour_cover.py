#!/usr/bin/env python3
"""Independent F_3 audit of the source-row tricolour cover."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_SOURCE_ROW_TRICOLOUR_COVER.md"
PRIME = 3
ZERO = (0, 0, 0)
COORDINATES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    if not any(vector):
        return ZERO
    pivot = next(value for value in vector if value)
    inverse = pow(pivot, -1, PRIME)
    return tuple((value * inverse) % PRIME for value in vector)


def rank_mod(vectors: list[tuple[int, ...]]) -> int:
    if not vectors:
        return 0
    matrix = [list(vector) for vector in vectors]
    row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (
                index
                for index in range(row, len(matrix))
                if matrix[index][column] % PRIME
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column] % PRIME, -1, PRIME)
        matrix[row] = [
            value * inverse % PRIME for value in matrix[row]
        ]
        for index in range(len(matrix)):
            if index == row:
                continue
            factor = matrix[index][column] % PRIME
            if factor:
                matrix[index] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(matrix[index], matrix[row])
                ]
        row += 1
    return row


def kernel_basis(covector: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    candidates = [
        vector
        for vector in itertools.product(range(PRIME), repeat=3)
        if any(vector)
        and sum(a * b for a, b in zip(covector, vector)) % PRIME == 0
    ]
    dimension = 3 if covector == ZERO else 2
    basis: list[tuple[int, ...]] = []
    for vector in candidates:
        if rank_mod(basis + [vector]) > len(basis):
            basis.append(vector)
        if len(basis) == dimension:
            break
    assert len(basis) == dimension
    return tuple(basis)


def restricted_colour(
    basis: tuple[tuple[int, ...], ...], colour: int
) -> np.ndarray:
    return np.asarray(
        [vector[colour] for vector in basis], dtype=np.int64
    )


def tensor_product(factors: list[np.ndarray]) -> np.ndarray:
    result = np.asarray([1], dtype=np.int64)
    for factor in factors:
        result = np.kron(result, factor) % PRIME
    return result


def main() -> None:
    projective = sorted(
        {
            canonical(vector)
            for vector in itertools.product(range(PRIME), repeat=3)
            if any(vector)
        }
    )
    covectors = (ZERO,) + tuple(projective)
    assert len(projective) == 13
    bases = {covector: kernel_basis(covector) for covector in covectors}

    multisets_checked = 0
    coefficient_ratios_checked = 0
    vanishing_cases = 0
    violations = []
    for rows in itertools.combinations_with_replacement(covectors, 5):
        multisets_checked += 1
        terms = []
        for colour in range(3):
            terms.append(
                tensor_product(
                    [
                        restricted_colour(bases[row], colour)
                        for row in rows
                    ]
                )
            )
        coordinate_set = set(rows) & set(COORDINATES)
        for lambda_one, lambda_two in itertools.product((1, 2), repeat=2):
            coefficient_ratios_checked += 1
            value = (
                terms[0]
                + lambda_one * terms[1]
                + lambda_two * terms[2]
            ) % PRIME
            if np.any(value):
                continue
            vanishing_cases += 1
            if coordinate_set != set(COORDINATES):
                violations.append(
                    {
                        "rows": rows,
                        "lambdas": (1, lambda_one, lambda_two),
                    }
                )

    assert multisets_checked == 8568
    assert coefficient_ratios_checked == 34272
    assert vanishing_cases == 420
    assert not violations

    output = {
        "audited": True,
        "field": "F_3",
        "projective_nonzero_covectors": len(projective),
        "zero_or_projective_covectors": len(covectors),
        "five_covector_multisets_checked": multisets_checked,
        "nonzero_coefficient_ratios_checked": coefficient_ratios_checked,
        "vanishing_restricted_tensors": vanishing_cases,
        "vanishing_cases_missing_a_coordinate_covector": len(violations),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_source_row_tricolour_cover_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
