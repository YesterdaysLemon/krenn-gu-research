#!/usr/bin/env python3
"""Independent F_5 audit of the support-three contraction formulas."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 5


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_basis(rows: object) -> tuple[tuple[int, ...], ...]:
    matrix = [
        [int(value) % PRIME for value in row]
        for row in rows
        if any(int(value) % PRIME for value in row)
    ]
    if not matrix:
        return ()
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
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(
        tuple(row) for row in matrix[:pivot_row]
    )


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    first = next(value for value in vector if value)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in vector)


def annihilator(
    kernel: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    vectors = []
    for candidate in itertools.product(range(PRIME), repeat=3):
        if all(
            sum(left * right for left, right in zip(candidate, row))
            % PRIME
            == 0
            for row in kernel
        ):
            vectors.append(candidate)
    return row_basis(vectors)


def coordinatewise_product_space(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return row_basis(
        tuple(a * b % PRIME for a, b in zip(u, v))
        for u in left
        for v in right
    )


def contains(
    space: tuple[tuple[int, ...], ...], vector: tuple[int, ...]
) -> bool:
    return len(row_basis((*space, vector))) == len(space)


def can_match_diagonal(
    left_kernel: tuple[tuple[int, ...], ...],
    right_kernel: tuple[tuple[int, ...], ...],
    diagonal: tuple[int, ...],
) -> bool:
    left_dimension = len(left_kernel)
    right_dimension = len(right_kernel)
    support = {
        index for index, value in enumerate(diagonal) if value % PRIME
    }
    left_annihilator = annihilator(left_kernel)
    right_annihilator = annihilator(right_kernel)

    if left_dimension == right_dimension == 1:
        required = row_basis(
            tuple(int(index == colour) for index in range(3))
            for colour in support
        )
        return (
            len(support) == 2
            and left_annihilator == required
            and right_annihilator == required
        )

    if left_dimension == 2 and right_dimension == 1:
        if len(support) != 1:
            return False
        colour = next(iter(support))
        coordinate = tuple(int(index == colour) for index in range(3))
        return (
            left_annihilator == (coordinate,)
            and contains(right_annihilator, coordinate)
        )
    if left_dimension == 1 and right_dimension == 2:
        return can_match_diagonal(
            right_kernel, left_kernel, diagonal
        )

    if len(support) != 1:
        return False
    colour = next(iter(support))
    coordinate = tuple(int(index == colour) for index in range(3))
    return (
        left_annihilator == (coordinate,)
        and right_annihilator == (coordinate,)
    )


def main() -> None:
    # Projective kernel lines with no full-support vector.
    kernel_lines = tuple(
        sorted(
            {
                (canonical(vector),)
                for vector in itertools.product(range(PRIME), repeat=3)
                if any(vector) and 0 in vector
            }
        )
    )
    coordinate_planes = tuple(
        row_basis(
            tuple(
                int(index == basis_coordinate)
                for index in range(3)
            )
            for basis_coordinate in range(3)
            if basis_coordinate != missing
        )
        for missing in range(3)
    )
    kernels = kernel_lines + coordinate_planes
    assert len(kernel_lines) == 15
    assert len(kernels) == 18

    rejection_counts: Counter[str] = Counter()
    survivors = []
    quadruples_checked = 0
    pair_checks = 0
    for candidate in itertools.product(kernels, repeat=4):
        quadruples_checked += 1
        rejected = False
        for first, second in itertools.combinations(range(4), 2):
            pair_checks += 1
            product_space = coordinatewise_product_space(
                candidate[first], candidate[second]
            )
            if len(product_space) > 1:
                rejection_counts["product_image_dimension_at_least_two"] += 1
                rejected = True
                break
            if not product_space:
                continue
            complement = tuple(
                mode for mode in range(4) if mode not in (first, second)
            )
            if not can_match_diagonal(
                candidate[complement[0]],
                candidate[complement[1]],
                product_space[0],
            ):
                rejection_counts["rank_or_row_space_mismatch"] += 1
                rejected = True
                break
        if not rejected:
            survivors.append(candidate)
    assert quadruples_checked == 18**4
    assert not survivors

    # Independent finite-field check of the P_3 slice obstruction.
    p3_projective_slices = set()
    p3_rank_counts: Counter[int] = Counter()
    for x, y, z in itertools.product(range(PRIME), repeat=3):
        if not (x or y or z):
            continue
        coefficients = canonical((x, y, z))
        if coefficients in p3_projective_slices:
            continue
        p3_projective_slices.add(coefficients)
        matrix = (
            (0, z, y),
            (z, 0, x),
            (y, x, 0),
        )
        p3_rank_counts[len(row_basis(matrix))] += 1
    assert p3_rank_counts.get(1, 0) == 0

    # Independently enumerate the 2^4 coordinate box.
    edges = ((0, 1, 3, 4), (1, 3, 4, 0))
    active_entries = []
    for choices in itertools.product(range(2), repeat=4):
        entry = tuple(edges[choices[mode]][mode] for mode in range(4))
        if len(set(entry)) != 4:
            continue
        missing = next(index for index in range(5) if index not in entry)
        if missing < 3:
            active_entries.append((entry, missing))
    assert active_entries == [(edges[0], 2), (edges[1], 2)]

    primary = (
        ROOT / "tmp" / "support_three_p5_contraction_subrank_verified.json"
    )
    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "projective_kernel_lines": len(kernel_lines),
        "coordinate_kernel_planes": len(coordinate_planes),
        "kernel_quadruples_checked": quadruples_checked,
        "kernel_pair_checks": pair_checks,
        "kernel_rejection_counts": dict(rejection_counts),
        "kernel_survivors": len(survivors),
        "projective_p3_slices": len(p3_projective_slices),
        "p3_slice_rank_counts": dict(sorted(p3_rank_counts.items())),
        "induced_box_active_entries": active_entries,
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "support_three_p5_contraction_subrank_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
