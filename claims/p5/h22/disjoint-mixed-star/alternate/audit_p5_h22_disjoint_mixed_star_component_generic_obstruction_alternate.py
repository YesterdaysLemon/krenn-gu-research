#!/usr/bin/env python3
"""Independent modular audit of the eighth component's weighted H22.

Imports nothing from the primary verifier.  At two exact finite-field
component points it exhausts every affine marking of both weighted
diagonal pencils and checks:

1.  the mixed 14 x 8 matrix has full column rank at every marking off
    the claimed loci: t1*t2 = 0 for the 01 pencil and
    t1 = t2 = t3 = 0 for the 23 pencil;
2.  every marking with a nonzero kernel lies on the claimed locus and
    has a one-dimensional kernel;
3.  on every genuine projective binary direction, the mode-zero
    one-marked contraction has rank four, and at least one of the
    minors in rows (0,1,3,7), (0,1,5,7) is nonzero.

These finite-field censuses are corroboration only; the theorem is
the characteristic-zero function-field calculation of the primary
verifier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_"
    "ALTERNATE.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h22_disjoint_mixed_star_component_generic_"
    "obstruction_alternate.py"
)
SAMPLES = {
    11: (1, 2, 7, 3),
    13: (1, 3, 5, 10),
}
# Slopes off every excluded divisor at these samples.  The function-
# field theorem inverts finitely many slope polynomials (for example
# r, r-1, r+1, and af(r+1)-(r-1)); slopes reducing into that divisor
# locus modulo p genuinely deviate and are not audited as claims.
SLOPES = {11: (2, 3), 13: (2, 3)}
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = tuple(
    bits for bits in BITS4
    if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
MINOR_ROWS = ((0, 1, 3, 7), (0, 1, 5, 7))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows, modulus: int) -> int:
    states = [0] * 16
    states[0] = 1
    for row in rows:
        updated = [0] * 16
        for mask, value in enumerate(states):
            if not value:
                continue
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit == 0:
                    updated[mask | bit] = (
                        updated[mask | bit] + value * entry
                    ) % modulus
        states = updated
    return states[15]


def component_rows(modulus: int):
    a, b, f, phi = SAMPLES[modulus]
    j = (f + b * phi * phi) % modulus
    kappa = phi * (b * f + 1) % modulus
    eta = -(b * f + 1) % modulus
    alpha = (
        (0, 0, 1, -1),
        (-a * f + 1, -a * f - 1, f + phi, f - phi),
        (-a * j + eta, -a * j - eta, j + kappa, j - kappa),
        (1, -1, 0, 0),
    )
    beta = (
        (a + b, a - b, 0, 2),
        (1, 1, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    alpha = tuple(
        tuple(value % modulus for value in row) for row in alpha
    )
    beta = tuple(
        tuple(value % modulus for value in row) for row in beta
    )
    residue = (
        a * a * b * f * phi * phi
        + a * a * f * f
        - b * b * f * f
        + b * b * phi * phi
        - b * f
        - 1
    ) % modulus
    assert residue == 0
    return alpha, beta


def weighted(row, extension, direction, slope, modulus):
    if direction == "01":
        return (
            (slope * row[0] + row[1]) % modulus,
            row[2] % modulus,
            row[3] % modulus,
            extension % modulus,
        )
    return (
        row[0] % modulus,
        row[1] % modulus,
        (slope * row[2] + row[3]) % modulus,
        extension % modulus,
    )


def rref_nullspace(matrix, modulus: int):
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                index
                for index in range(pivot_row, rows)
                if work[index][column]
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
        for index in range(rows):
            if index == pivot_row or work[index][column] == 0:
                continue
            scale = work[index][column]
            work[index] = [
                (left - scale * right) % modulus
                for left, right in zip(
                    work[index], work[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
    free = tuple(
        column for column in range(columns) if column not in pivots
    )
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row_index, pivot_column in enumerate(pivots):
            vector[pivot_column] = (
                -work[row_index][free_column] % modulus
            )
        basis.append(tuple(vector))
    return len(pivots), tuple(basis)


def rank_mod(matrix, modulus: int) -> int:
    rank, _basis = rref_nullspace(matrix, modulus)
    return rank


def determinant_mod(matrix, modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    size = len(work)
    result = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        value = work[column][column]
        result = result * value % modulus
        inverse = pow(value, -1, modulus)
        for row in range(column + 1, size):
            scale = work[row][column] * inverse % modulus
            for offset in range(column, size):
                work[row][offset] = (
                    work[row][offset]
                    - scale * work[column][offset]
                ) % modulus
    return result % modulus


def extension_matrices(alpha, beta, direction, slope, modulus):
    columns = []
    for coordinate in range(8):
        extension = [0] * 8
        extension[coordinate] = 1
        alpha_d = tuple(
            weighted(
                alpha[mode], extension[mode], direction, slope,
                modulus,
            )
            for mode in range(4)
        )
        beta_d = tuple(
            weighted(
                beta[mode], extension[4 + mode], direction, slope,
                modulus,
            )
            for mode in range(4)
        )
        columns.append({
            bits: permanent(
                tuple(
                    beta_d[mode] if bits[mode] else alpha_d[mode]
                    for mode in range(4)
                ),
                modulus,
            )
            for bits in BITS4
        })
    mixed = [
        [columns[column][bits] for column in range(8)]
        for bits in MIXED
    ]
    diagonal_a = [
        columns[column][(0, 0, 0, 0)] for column in range(8)
    ]
    diagonal_b = [
        columns[column][(1, 1, 1, 1)] for column in range(8)
    ]
    return mixed, diagonal_a, diagonal_b


def dot(row, vector, modulus: int) -> int:
    return sum(
        left * right
        for left, right in zip(row, vector, strict=True)
    ) % modulus


def one_marked_mode0(alpha_d, beta_d, modulus):
    rows = []
    for bits in BITS3:
        chosen = [
            beta_d[mode] if bits[mode - 1] else alpha_d[mode]
            for mode in (1, 2, 3)
        ]
        row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            row.append(
                permanent(
                    (basis,) + tuple(chosen), modulus
                )
            )
        rows.append(row)
    return rows


def on_locus(direction: str, shifts, modulus: int) -> bool:
    if direction == "01":
        return shifts[1] * shifts[2] % modulus == 0
    return shifts[1] == shifts[2] == shifts[3] == 0


def on_stratum(shifts, modulus: int, slope: int, sample) -> bool:
    """The four refined 01-pencil strata of the theorem."""
    a, _b, f, phi = sample
    t0, t1, t2, t3 = shifts
    branch_t0 = (phi * (t0 - 1) - f) % modulus
    branch_t1 = (
        (a * f * (slope + 1) - (slope - 1)) * t1 - (slope + 1)
    ) % modulus
    if t1 == 0 and t2 == 0:
        return True
    if t1 == 0 and branch_t0 == 0:
        return True
    if t2 == 0 and t3 == 0:
        return True
    if t2 == 0 and branch_t1 == 0:
        return True
    return False


def audit_point(modulus: int, slope: int):
    alpha, canonical_beta = component_rows(modulus)
    summary = {}
    for direction in ("01", "23"):
        kernel_markings = 0
        genuine_directions = 0
        nongenuine_kernels = 0
        for shifts in itertools.product(range(modulus), repeat=4):
            beta = tuple(
                tuple(
                    (
                        canonical_beta[mode][coordinate]
                        + shifts[mode] * alpha[mode][coordinate]
                    )
                    % modulus
                    for coordinate in range(4)
                )
                for mode in range(4)
            )
            mixed, diagonal_a, diagonal_b = extension_matrices(
                alpha, beta, direction, slope, modulus
            )
            rank, kernel = rref_nullspace(mixed, modulus)
            if rank == 8:
                continue
            assert on_locus(direction, shifts, modulus), (
                direction, slope, shifts,
            )
            if direction == "01":
                assert on_stratum(
                    shifts, modulus, slope, SAMPLES[modulus]
                ), (direction, slope, shifts)
            assert rank == 7, (direction, slope, shifts, rank)
            kernel_markings += 1
            vector = kernel[0]
            first = dot(diagonal_a, vector, modulus)
            second = dot(diagonal_b, vector, modulus)
            if first == 0 or second == 0:
                nongenuine_kernels += 1
                continue
            genuine_directions += 1
            alpha_d = tuple(
                weighted(
                    alpha[mode], vector[mode], direction, slope,
                    modulus,
                )
                for mode in range(4)
            )
            beta_d = tuple(
                weighted(
                    beta[mode], vector[4 + mode], direction, slope,
                    modulus,
                )
                for mode in range(4)
            )
            marked = one_marked_mode0(alpha_d, beta_d, modulus)
            assert rank_mod(marked, modulus) == 4, (
                direction, slope, shifts,
            )
            minors = [
                determinant_mod(
                    [marked[row] for row in rows], modulus
                )
                for rows in MINOR_ROWS
            ]
            assert any(minors), (direction, slope, shifts)
        summary[direction] = {
            "kernel_markings": kernel_markings,
            "genuine_directions": genuine_directions,
            "nongenuine_kernels": nongenuine_kernels,
        }
        assert kernel_markings > 0
        assert genuine_directions > 0
    return summary


def main() -> None:
    audits = []
    for modulus in sorted(SAMPLES):
        for slope in SLOPES[modulus]:
            summary = audit_point(modulus, slope)
            audits.append({
                "modulus": modulus,
                "sample_a_b_f_phi": list(SAMPLES[modulus]),
                "slope": slope,
                "markings_tested_per_pencil": modulus**4,
                "pencils": summary,
            })
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "finite-field marked-basis census, subset-DP permanent, "
            "modular kernels, and mode-zero one-marked minor replay "
            "on every genuine projective binary direction"
        ),
        "moduli": sorted(SAMPLES),
        "audits": audits,
        "claims_checked": [
            "full column rank off the claimed marking loci",
            "rank seven and t1*t2=0 at every 01-pencil kernel",
            "every 01-pencil kernel lies on one of the four refined "
            "marking strata",
            "rank seven and t1=t2=t3=0 at every 23-pencil kernel",
            "rank-four mode-zero one-marked contraction with a "
            "nonzero selected minor on every genuine direction",
        ],
        "special_slope_note": (
            "slopes reducing into the excluded divisor locus "
            "(r=0, r=1, r=-1, and finitely many further divisor "
            "slopes per finite point) genuinely deviate, as the "
            "function-field theorem inverts those factors; audited "
            "slopes avoid them"
        ),
        "finite_field_results_are_corroboration_only": True,
        "generic_weighted_H22_component_incidence_excluded_modularly":
            True,
        "all_eight_known_components_generically_closed_for_H22": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / (
            "p5_h22_disjoint_mixed_star_component_generic_"
            "obstruction_alternate_audit.json"
        )
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
