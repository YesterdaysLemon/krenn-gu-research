#!/usr/bin/env python3
"""Independent finite-field audit of the six-dimensional component H31 fibre."""

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
    HERE / "P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md"
)
PRIMARY = (
    HERE
    / "verify_p5_h31_six_dimensional_component_generic_obstruction.py"
)
SAMPLES = {
    5: (3, 4, 3, 2),
    7: (3, 5, 5, 2),
}
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
FITTING_ROWS = {
    0: ((0, 1, 2, 7), (0, 1, 3, 7), (0, 1, 4, 7)),
    2: ((0, 2, 6, 7), (0, 3, 6, 7), (0, 4, 6, 7)),
    3: ((0, 1, 2, 7), (0, 1, 3, 7), (0, 1, 4, 7)),
}


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


def extension_coefficients(
    distinguished: int, alpha, beta, extension, modulus: int
):
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (extension[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        bits: permanent(
            tuple(
                beta_p[mode] if bits[mode] else alpha_p[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in BITS4
    }


def extension_matrices(distinguished: int, alpha, beta, modulus: int):
    columns = []
    for coordinate in range(8):
        extension = [0] * 8
        extension[coordinate] = 1
        coefficients = extension_coefficients(
            distinguished, alpha, beta, extension, modulus
        )
        columns.append(coefficients)
    mixed_bits = tuple(
        bits
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    mixed = [
        [columns[column][bits] for column in range(8)]
        for bits in mixed_bits
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
                        work[row], work[pivot_row], strict=True
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
                    work[row][offset] - scale * work[column][offset]
                ) % modulus
    return result % modulus


def one_marked_map(mode: int, alpha, beta, modulus: int):
    rows = []
    for bits in BITS3:
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
            basis = tuple(int(index == coordinate) for index in range(4))
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


def marked_extension(
    distinguished: int,
    extension,
    alpha,
    beta,
    mode: int,
    modulus: int,
):
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row],)
        for row in range(4)
    )
    beta_p = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_p, beta_p, modulus)


def projective_directions(dimension: int, modulus: int):
    for pivot in range(dimension):
        for tail in itertools.product(
            range(modulus), repeat=dimension - pivot - 1
        ):
            yield (0,) * pivot + (1,) + tail


def expected_markings(parameters, modulus: int):
    s, _d, u, v = parameters
    inverse = pow((u - v) % modulus, -1, modulus)
    common_t1 = (1 - u) * inverse % modulus
    common_t2 = s * v * inverse % modulus
    return {
        0: {(1, common_t1, common_t2, 0)},
        1: set(),
        2: {(0, common_t1, common_t2, 1)},
        3: {(0, common_t1, common_t2, 0)},
    }


def audit_modulus(modulus: int):
    parameters, alpha, canonical_beta = canonical_basis(modulus)
    s, _d, u, _v = parameters
    pure = {
        bits: permanent(
            tuple(
                canonical_beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in BITS4
    }
    assert pure[(1, 1, 1, 1)] == 2 * s * u % modulus
    assert all(
        value == 0
        for bits, value in pure.items()
        if bits != (1, 1, 1, 1)
    )

    expected = expected_markings(parameters, modulus)
    observed = {distinguished: set() for distinguished in range(4)}
    extension_checks = 0
    reconstruction_checks = 0
    for distinguished in range(4):
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
                distinguished, alpha, beta, modulus
            )
            _rank, kernel = rref_nullspace(mixed, modulus)

            if distinguished == 1:
                reconstruction = tuple(
                    alpha[mode][1] for mode in range(4)
                ) + tuple(beta[mode][1] for mode in range(4))
                assert all(
                    dot(row, reconstruction, modulus) == 0
                    for row in mixed
                )
                assert dot(diagonal_a, reconstruction, modulus) == 0
                assert dot(
                    diagonal_b, reconstruction, modulus
                ) == 2 * s * u % modulus
                reconstruction_checks += 1

            first_nonzero = any(
                dot(diagonal_a, vector, modulus) for vector in kernel
            )
            second_nonzero = any(
                dot(diagonal_b, vector, modulus) for vector in kernel
            )
            if not (first_nonzero and second_nonzero):
                continue
            observed[distinguished].add(shifts)
            assert distinguished in FITTING_ROWS
            for direction in projective_directions(len(kernel), modulus):
                extension = tuple(
                    sum(
                        direction[index] * kernel[index][coordinate]
                        for index in range(len(kernel))
                    )
                    % modulus
                    for coordinate in range(8)
                )
                first = dot(diagonal_a, extension, modulus)
                second = dot(diagonal_b, extension, modulus)
                if first == 0 or second == 0:
                    continue
                marked = marked_extension(
                    distinguished,
                    extension,
                    alpha,
                    beta,
                    0,
                    modulus,
                )
                determinants = tuple(
                    determinant_mod(
                        [
                            [marked[row][column] for column in range(4)]
                            for row in rows
                        ],
                        modulus,
                    )
                    for rows in FITTING_ROWS[distinguished]
                )
                assert any(determinants)
                extension_checks += 1
    assert observed == expected, (observed, expected)
    return {
        "modulus": modulus,
        "sample_s_d_u_v": list(parameters),
        "marked_bases_tested": 4 * modulus**4,
        "surviving_markings": sum(len(value) for value in observed.values()),
        "projected_markings": {
            str(key): [list(value) for value in sorted(values)]
            for key, values in observed.items()
        },
        "genuine_projective_extension_directions_checked": extension_checks,
        "reconstruction_kernel_checks": reconstruction_checks,
    }


def main() -> None:
    audits = [
        audit_modulus(modulus) for modulus in sorted(SAMPLES)
    ]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "finite-field marked-basis census, DP permanent, modular "
            "kernel computation, and exhaustive three-minor replay"
        ),
        "moduli": sorted(SAMPLES),
        "audits": audits,
        "generic_marked_fibre_excluded_modularly": True,
        "finite_field_results_are_corroboration_only": True,
        "known_pure_component_orbits_at_least": 7,
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
        / "p5_h31_six_dimensional_component_generic_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
