#!/usr/bin/env python3
"""Independent modular audit of the mixed-orientation H22 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

ROOT = REPO_ROOT
THEOREM = (
    HERE
    / "P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md"
)
PRIMARY = (
    HERE
    / "verify_p5_h22_mixed_orientation_component_generic_obstruction.py"
)
SAMPLES = {
    5: (1, 2, 1, 2),
    7: (2, 1, 1, 2),
}
EXPECTED_D23_SURVIVORS = {5: 7, 7: 6}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    bits
    for bits in WORDS
    if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
FITTING_ROWS = ((0, 2, 6, 7), (0, 4, 6, 7))


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
    d, p, q, slope = SAMPLES[modulus]
    n = q * (d + p + q) % modulus
    planes = (
        (
            (-d * p, d + q, n, 0),
            (d * p, -d - q, 0, n),
        ),
        ((0, 0, 1, 1), (-d, 1, -p - q, d)),
        ((p, 1, 0, q), (-1, 0, 1, 0)),
        ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    alpha = tuple(
        tuple(entry % modulus for entry in plane[1])
        for plane in planes
    )
    beta = tuple(
        tuple(entry % modulus for entry in plane[0])
        for plane in planes
    )
    return (d, p, q, slope), alpha, beta


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


def low_marking_values(shifts, d, p, q, modulus: int):
    t0, t1, t2, t3 = shifts
    return (
        t1 * t3,
        (t0 - 1) * t3,
        t1 * ((d + q) * t2 - p * q),
        (t0 - 1) * (t2 + d - p),
        (t0 - 1) * t1,
    )


def closure_membership(shifts, d, p, q, modulus: int):
    t0, t1, t2, t3 = shifts
    return {
        "A": (t0 - 1) % modulus == 0 and t1 == 0,
        "B": (
            (t0 - 1) % modulus == 0
            and t3 == 0
            and ((d + q) * t2 - p * q) % modulus == 0
        ),
        "C": (
            t1 == 0
            and t3 == 0
            and (t2 + d - p) % modulus == 0
        ),
    }


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
    marked = one_marked_map(3, alpha_d, beta_d, modulus)
    rank, _ = rref_nullspace(marked, modulus)
    determinants = tuple(
        determinant_mod(
            [[marked[row][column] for column in range(4)] for row in rows],
            modulus,
        )
        for rows in FITTING_ROWS
    )
    return rank, determinants


def audit_sample(modulus: int):
    sample, alpha, beta = canonical_basis(modulus)
    d, p, q, slope = sample
    d01_ranks = {}
    d23_survivors = []
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
        mixed01, _first01, _second01 = extension_matrices(
            alpha,
            marked_beta,
            "01",
            slope,
            modulus,
        )
        rank01, kernel01 = rref_nullspace(mixed01, modulus)
        assert rank01 == 8
        assert not kernel01
        d01_ranks[rank01] = d01_ranks.get(rank01, 0) + 1

        mixed23, first23, second23 = extension_matrices(
            alpha,
            marked_beta,
            "23",
            slope,
            modulus,
        )
        rank23, kernel23 = rref_nullspace(mixed23, modulus)
        if not kernel23:
            continue
        assert len(kernel23) == 1
        direction = kernel23[0]
        if not (
            dot(first23, direction, modulus)
            and dot(second23, direction, modulus)
        ):
            continue
        assert rank23 == 7
        assert all(
            value % modulus == 0
            for value in low_marking_values(shifts, d, p, q, modulus)
        )
        closures = closure_membership(shifts, d, p, q, modulus)
        assert any(closures.values())
        marked_rank, determinants = marked_minor_check(
            alpha,
            marked_beta,
            direction,
            slope,
            modulus,
        )
        assert marked_rank == 4
        assert all(determinants)
        d23_survivors.append(
            {
                "shifts": list(shifts),
                "mixed_rank": rank23,
                "kernel_dimension": 1,
                "covering_closures": [
                    branch
                    for branch, contains in closures.items()
                    if contains
                ],
                "selected_mode3_minors": list(determinants),
                "mode3_marked_rank": marked_rank,
            }
        )

    assert len(d23_survivors) == EXPECTED_D23_SURVIVORS[modulus]
    return {
        "modulus": modulus,
        "sample_d_p_q_slope": list(sample),
        "D01": {
            "markings_tested": modulus**4,
            "mixed_rank_distribution": {
                str(rank): count for rank, count in sorted(d01_ranks.items())
            },
            "all_mixed_ranks_eight": True,
        },
        "D23": {
            "markings_tested": modulus**4,
            "genuine_survivor_count": len(d23_survivors),
            "all_survivors_on_three_closure_cover": True,
            "all_survivor_kernels_one_dimensional": True,
            "both_selected_minors_nonzero_on_every_survivor": True,
            "survivors": d23_survivors,
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
        d, p, q, _slope = sample
        expected = 2 * q * (d + p + q) % modulus
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
            "finite-field marked-basis census, DP permanent, modular "
            "nullspaces, closure-cover replay, and selected minors"
        ),
        "moduli": list(SAMPLES),
        "audits": audits,
        "D01_full_rank_replayed_modularly": True,
        "D23_closure_cover_and_rank_four_obstruction_replayed": True,
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
        / "p5_h22_mixed_orientation_component_generic_audit.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
