#!/usr/bin/env python3
"""Independent modular audit of the equal-weight six-dimensional H22 chart."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = REPO_ROOT
THEOREM = (
    HERE
    / "P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md"
)
PRIMARY = (
    HERE
    / "verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py"
)
SAMPLES = {
    5: (3, 4, 3, 2),
    7: (3, 5, 5, 2),
}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    bits
    for bits in WORDS
    if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)


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
    s, d, u, v = SAMPLES[modulus]
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
    return (s, d, u, v), alpha, beta


def diagonal_row(row, extension: int, diagonal: str, modulus: int):
    if diagonal == "01":
        return (
            (row[0] + row[1]) % modulus,
            row[2],
            row[3],
            extension,
        )
    if diagonal == "23":
        return (
            row[0],
            row[1],
            (row[2] + row[3]) % modulus,
            extension,
        )
    raise ValueError(diagonal)


def extension_matrices(alpha, beta, diagonal: str, modulus: int):
    columns = []
    for extension_coordinate in range(8):
        extension = [0] * 8
        extension[extension_coordinate] = 1
        alpha_d = tuple(
            diagonal_row(
                alpha[mode],
                extension[mode],
                diagonal,
                modulus,
            )
            for mode in range(4)
        )
        beta_d = tuple(
            diagonal_row(
                beta[mode],
                extension[4 + mode],
                diagonal,
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


def audit_diagonal(alpha, beta, diagonal: str, modulus: int):
    profile = Counter()
    survivors = []
    row_identity_checks = 0
    s, _, u, v = SAMPLES[modulus]
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
            modulus,
        )
        if diagonal == "23":
            row_1000 = mixed[MIXED_WORDS.index((1, 0, 0, 0))]
            row_1110 = mixed[MIXED_WORDS.index((1, 1, 1, 0))]
            assert all(
                (
                    left
                    - (shifts[0] - 1) * right
                )
                % modulus
                == 0
                for left, right in zip(
                    row_1000,
                    first,
                    strict=True,
                )
            )
            obstruction_factor = (
                s * shifts[0] * shifts[1] * v
                - s * shifts[0] * u
                + s * shifts[0]
                - s * shifts[1] * v
                - s
                - shifts[0] * shifts[1] * shifts[2] * u
                + shifts[0] * shifts[1] * shifts[2] * v
                - shifts[0] * shifts[2] * u
                + shifts[0] * shifts[2]
                + shifts[1] * shifts[2] * u
                - shifts[1] * shifts[2] * v
                + shifts[2] * u
                - shifts[2]
            )
            assert all(
                (
                    (u - v) * left
                    + obstruction_factor * right
                )
                % modulus
                == 0
                for left, right in zip(
                    row_1110,
                    first,
                    strict=True,
                )
            )
            if shifts[0] == 1:
                assert (obstruction_factor + s * u) % modulus == 0
            row_identity_checks += 1
        rank, kernel = rref_nullspace(mixed, modulus)
        first_nonzero = any(
            dot(first, vector, modulus) for vector in kernel
        )
        second_nonzero = any(
            dot(second, vector, modulus) for vector in kernel
        )
        profile[(len(kernel), first_nonzero, second_nonzero)] += 1
        if first_nonzero and second_nonzero:
            survivors.append(shifts)
    assert not survivors
    return {
        "markings_tested": modulus**4,
        "viable_binary_Delta2_markings": 0,
        "two_row_identity_checks": row_identity_checks,
        "kernel_functional_profile": {
            (
                f"dim_{dimension}:"
                f"first_{int(first_nonzero)}:"
                f"second_{int(second_nonzero)}"
            ): count
            for (
                dimension,
                first_nonzero,
                second_nonzero,
            ), count in sorted(profile.items())
        },
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
        audits.append(
            {
                "modulus": modulus,
                "sample_s_d_u_v": list(sample),
                "pure_coefficient": expected,
                "diagonals": {
                    diagonal: audit_diagonal(
                        alpha,
                        beta,
                        diagonal,
                        modulus,
                    )
                    for diagonal in ("01", "23")
                },
            }
        )

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "finite-field marked-basis census, DP permanent, and "
            "independent modular nullspace computation"
        ),
        "moduli": list(SAMPLES),
        "audits": audits,
        "both_diagonal_binary_incidence_fibres_empty_modularly": True,
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
        / "p5_h22_six_dimensional_equal_weight_binary_audit.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
