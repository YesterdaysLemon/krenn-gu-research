#!/usr/bin/env python3
"""Independent modular audit of the generic weighted H22 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT / "verify_p5_h22_six_dimensional_component_generic_obstruction.py"
)
SAMPLES = {
    7: (3, 5, 5, 2, 2),
    11: (3, 5, 5, 2, 3),
}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    bits
    for bits in WORDS
    if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
FITTING_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows, modulus: int) -> int:
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


def canonical_basis(modulus: int):
    s, d, u, v, slope = SAMPLES[modulus]
    h = (s - d) % modulus
    planes = (
        ((1, 0, 0, -1), (0, 0, 1, 1)),
        (
            (s, 1 - u, 0, d + u * h),
            (0, 1 - v, s, d + v * h),
        ),
        ((1, 0, -1, 0), (0, 1, -s, -d)),
        ((1, 0, 0, 1), (0, 0, 1, -1)),
    )
    planes = tuple(
        tuple(
            tuple(entry % modulus for entry in row)
            for row in plane
        )
        for plane in planes
    )
    alpha = (
        planes[0][0],
        tuple(
            (
                v * planes[1][0][coordinate]
                - u * planes[1][1][coordinate]
            )
            % modulus
            for coordinate in range(4)
        ),
        planes[2][0],
        planes[3][1],
    )
    beta = (
        planes[0][1],
        planes[1][0],
        planes[2][1],
        planes[3][0],
    )
    return (s, d, u, v, slope), alpha, beta


def diagonal_row(row, extension, diagonal: str, slope, modulus: int):
    if diagonal == "01":
        return (
            (slope * row[0] + row[1]) % modulus,
            row[2],
            row[3],
            extension,
        )
    if diagonal == "23":
        return (
            row[0],
            row[1],
            (slope * row[2] + row[3]) % modulus,
            extension,
        )
    raise ValueError(diagonal)


def extension_matrices(
    alpha,
    beta,
    diagonal: str,
    slope,
    modulus: int,
):
    columns = []
    for extension_coordinate in range(8):
        extension = [0] * 8
        extension[extension_coordinate] = 1
        alpha_d = tuple(
            diagonal_row(
                alpha[mode],
                extension[mode],
                diagonal,
                slope,
                modulus,
            )
            for mode in range(4)
        )
        beta_d = tuple(
            diagonal_row(
                beta[mode],
                extension[4 + mode],
                diagonal,
                slope,
                modulus,
            )
            for mode in range(4)
        )
        columns.append(
            {
                bits: permanent(
                    tuple(
                        beta_d[mode] if bits[mode] else alpha_d[mode]
                        for mode in range(4)
                    ),
                    modulus,
                )
                for bits in WORDS
            }
        )
    mixed = [
        [columns[column][bits] for column in range(8)]
        for bits in MIXED_WORDS
    ]
    diagonals = tuple(
        [columns[column][bits] for column in range(8)]
        for bits in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, *diagonals


def rref_nullspace(matrix, modulus: int):
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [
            value * inverse % modulus for value in work[pivot_row]
        ]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(
                        work[row],
                        work[pivot_row],
                        strict=True,
                    )
                ]
        pivots.append(column)
        pivot_row += 1
    free = tuple(column for column in range(columns) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column] % modulus
        basis.append(tuple(vector))
    return len(pivots), tuple(basis)


def dot(row, vector, modulus: int) -> int:
    return sum(
        left * right for left, right in zip(row, vector, strict=True)
    ) % modulus


def determinant_mod(matrix, modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % modulus
            for offset in range(column, len(work)):
                work[row][offset] = (
                    work[row][offset]
                    - scale * work[column][offset]
                ) % modulus
    return result % modulus


def one_marked_map(mode: int, alpha, beta, modulus: int):
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    ),
                    modulus,
                )
            )
        rows.append(coefficient_row)
    return rows


def projective_kernel_directions(kernel, modulus: int):
    if len(kernel) == 1:
        return (kernel[0],)
    assert len(kernel) == 2
    first, second = kernel
    affine = tuple(
        tuple(
            (left + scalar * right) % modulus
            for left, right in zip(first, second, strict=True)
        )
        for scalar in range(modulus)
    )
    return affine + (second,)


def marked_minor_check(
    alpha,
    beta,
    extension,
    slope,
    modulus: int,
):
    alpha_d = tuple(
        diagonal_row(
            alpha[mode],
            extension[mode],
            "23",
            slope,
            modulus,
        )
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(
            beta[mode],
            extension[4 + mode],
            "23",
            slope,
            modulus,
        )
        for mode in range(4)
    )
    marked = one_marked_map(0, alpha_d, beta_d, modulus)
    determinants = tuple(
        determinant_mod(
            [[marked[row][column] for column in range(4)] for row in rows],
            modulus,
        )
        for rows in FITTING_ROWS
    )
    marked_rank, _ = rref_nullspace(marked, modulus)
    assert marked_rank == 4
    return determinants, marked_rank


def audit_sample(modulus: int):
    sample, alpha, beta = canonical_basis(modulus)
    s, d, u, v, slope = sample
    expected_t1 = (1 - u) * pow(u - v, -1, modulus) % modulus
    expected_t2 = s * v * pow(u - v, -1, modulus) % modulus
    summary = {}
    for diagonal in ("01", "23"):
        survivors = []
        extension_checks = 0
        selected_pair_zero_checks = 0
        minor_patterns = set()
        for shifts in itertools.product(range(modulus), repeat=4):
            marked_beta = tuple(
                tuple(
                    (
                        beta[mode][coordinate]
                        + shifts[mode] * alpha[mode][coordinate]
                    )
                    % modulus
                    for coordinate in range(4)
                )
                for mode in range(4)
            )
            mixed, first, second = extension_matrices(
                alpha,
                marked_beta,
                diagonal,
                slope,
                modulus,
            )
            rank, kernel = rref_nullspace(mixed, modulus)
            first_nonzero = any(
                dot(first, vector, modulus) for vector in kernel
            )
            second_nonzero = any(
                dot(second, vector, modulus) for vector in kernel
            )
            if not (first_nonzero and second_nonzero):
                continue
            survivors.append(
                {
                    "shifts": list(shifts),
                    "mixed_rank": rank,
                    "kernel_dimension": len(kernel),
                }
            )
            assert diagonal == "23"
            assert shifts[:3] == (0, expected_t1, expected_t2)
            for direction in projective_kernel_directions(kernel, modulus):
                if not (
                    dot(first, direction, modulus)
                    and dot(second, direction, modulus)
                ):
                    continue
                determinants, marked_rank = marked_minor_check(
                    alpha,
                    marked_beta,
                    direction,
                    slope,
                    modulus,
                )
                assert marked_rank == 4
                extension_checks += 1
                if not any(determinants):
                    selected_pair_zero_checks += 1
                minor_patterns.add(determinants)
        if diagonal == "01":
            assert not survivors
        else:
            assert survivors
            assert all(
                survivor["kernel_dimension"] == 2
                for survivor in survivors
            )
        summary[diagonal] = {
            "markings_tested": modulus**4,
            "viable_binary_markings": len(survivors),
            "survivors": survivors,
            "genuine_projective_extensions_checked": extension_checks,
            "full_marked_rank_four_checks": extension_checks,
            "selected_pair_zero_specializations": selected_pair_zero_checks,
            "nonzero_minor_patterns": [
                list(pattern) for pattern in sorted(minor_patterns)
            ],
        }
    return {
        "modulus": modulus,
        "sample_s_d_u_v_slope": list(sample),
        "expected_weighted_23_marking_prefix": [
            0,
            expected_t1,
            expected_t2,
        ],
        "diagonals": summary,
    }


def main() -> None:
    audits = []
    for modulus in SAMPLES:
        sample, alpha, beta = canonical_basis(modulus)
        pure = {
            bits: permanent(
                tuple(
                    beta[mode] if bits[mode] else alpha[mode]
                    for mode in range(4)
                ),
                modulus,
            )
            for bits in WORDS
        }
        expected = 2 * sample[0] * sample[2] % modulus
        assert pure[(1, 1, 1, 1)] == expected != 0
        assert all(
            value == 0
            for bits, value in pure.items()
            if bits != (1, 1, 1, 1)
        )
        audits.append(audit_sample(modulus))

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "finite-field weighted marked-basis census, DP permanent, "
            "modular nullspaces, and exhaustive projective kernel replay"
        ),
        "moduli": list(SAMPLES),
        "audits": audits,
        "weighted_01_generic_binary_fibre_empty_modularly": True,
        "weighted_23_marking_sheet_and_full_rank_obstruction_replayed": True,
        "finite_field_results_are_corroboration_only": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output = (
        ROOT
        / "tmp"
        / "p5_h22_six_dimensional_component_generic_audit.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
