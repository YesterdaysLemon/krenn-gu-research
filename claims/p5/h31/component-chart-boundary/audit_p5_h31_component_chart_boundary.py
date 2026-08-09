#!/usr/bin/env python3
"""Independent finite-field audit of the H31 chart-boundary obstruction."""

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
THEOREM = HERE / "P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md"
PRIMARY = HERE / "verify_p5_h31_component_chart_boundary.py"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, -1, prime)


def permanent_dp(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    table = {0: 1}
    for row in rows:
        next_table: dict[int, int] = {}
        for mask, subtotal in table.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_table[new_mask] = (
                    next_table.get(new_mask, 0)
                    + subtotal * row[column]
                ) % prime
        table = next_table
    return table[15]


def rref_mod(
    matrix: list[list[int]],
    prime: int,
) -> tuple[list[list[int]], tuple[int, ...]]:
    result = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    pivots = []
    for column in range(len(result[0])):
        selected = next(
            (
                row
                for row in range(pivot_row, len(result))
                if result[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = (
            result[selected], result[pivot_row]
        )
        scale = inverse(result[pivot_row][column], prime)
        result[pivot_row] = [
            entry * scale % prime for entry in result[pivot_row]
        ]
        for row in range(len(result)):
            if row == pivot_row:
                continue
            multiple = result[row][column]
            if multiple:
                result[row] = [
                    (left - multiple * right) % prime
                    for left, right in zip(
                        result[row], result[pivot_row], strict=True
                    )
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(result):
            break
    return result, tuple(pivots)


def nullspace_mod(
    matrix: list[list[int]], prime: int
) -> tuple[tuple[int, ...], ...]:
    rref, pivots = rref_mod(matrix, prime)
    free = tuple(
        column
        for column in range(len(matrix[0]))
        if column not in pivots
    )
    basis = []
    for free_column in free:
        vector = [0] * len(matrix[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free_column] % prime
        basis.append(tuple(vector))
    return tuple(basis)


def dot(row: list[int], vector: tuple[int, ...], prime: int) -> int:
    return sum(
        left * right
        for left, right in zip(row, vector, strict=True)
    ) % prime


def projective_coefficients(
    dimension: int, prime: int
) -> tuple[tuple[int, ...], ...]:
    result = []
    for first_nonzero in range(dimension):
        for tail in itertools.product(
            range(prime), repeat=dimension - first_nonzero - 1
        ):
            result.append((0,) * first_nonzero + (1,) + tail)
    return tuple(result)


def linear_combination(
    basis: tuple[tuple[int, ...], ...],
    coefficients: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    return tuple(
        sum(
            coefficients[index] * basis[index][coordinate]
            for index in range(len(basis))
        ) % prime
        for coordinate in range(len(basis[0]))
    )


def boundary_rows(
    A: int, H: int, N: int, R: int, prime: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    alpha = (
        (1, 0, A, H * (A - N)),
        (0, 0, 1, H),
        (0, 1, 0, H * N * R),
        (1, 0, N, 0),
    )
    beta = (
        (0, 1, 0, -H * N * R),
        (R, 1, -R * N, -R * H * N),
        (-inverse(N, prime), 0, 1, 0),
        (0, 0, -inverse(H, prime), 1),
    )
    return (
        tuple(tuple(entry % prime for entry in row) for row in alpha),
        tuple(tuple(entry % prime for entry in row) for row in beta),
    )


def extension_system(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[list[list[int]], list[int], list[int]]:
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    coefficient_rows = {}
    for bits in BITS4:
        row = []
        for variable in range(8):
            alpha_p = tuple(
                tuple(alpha[mode][coordinate] for coordinate in common)
                + (int(variable == mode),)
                for mode in range(4)
            )
            beta_p = tuple(
                tuple(beta[mode][coordinate] for coordinate in common)
                + (int(variable == 4 + mode),)
                for mode in range(4)
            )
            row.append(
                permanent_dp(
                    tuple(
                        beta_p[mode] if bits[mode] else alpha_p[mode]
                        for mode in range(4)
                    ),
                    prime,
                )
            )
        coefficient_rows[bits] = row
    return (
        [
            coefficient_rows[bits]
            for bits in BITS4
            if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
        ],
        coefficient_rows[(0, 0, 0, 0)],
        coefficient_rows[(1, 1, 1, 1)],
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
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
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent_dp(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    ),
                    prime,
                )
            )
        rows.append(coefficient_row)
    return rows


def audit_prime(prime: int) -> dict[str, int]:
    parameter_points = 0
    binary_delta2_extensions = 0
    marked_injective_extensions = 0
    successful_third_row_lifts = 0
    for A in range(1, prime):
        for H in range(1, prime):
            for N in range(1, prime):
                for R in range(prime):
                    parameter_points += 1
                    alpha, beta = boundary_rows(A, H, N, R, prime)
                    for distinguished in range(4):
                        mixed, alpha_diagonal, beta_diagonal = (
                            extension_system(
                                distinguished, alpha, beta, prime
                            )
                        )
                        kernel = nullspace_mod(mixed, prime)
                        alpha_values = [
                            dot(alpha_diagonal, vector, prime)
                            for vector in kernel
                        ]
                        beta_values = [
                            dot(beta_diagonal, vector, prime)
                            for vector in kernel
                        ]
                        if not any(alpha_values) or not any(beta_values):
                            continue
                        for coefficients in projective_coefficients(
                            len(kernel), prime
                        ):
                            vector = linear_combination(
                                kernel, coefficients, prime
                            )
                            if not (
                                dot(alpha_diagonal, vector, prime)
                                and dot(beta_diagonal, vector, prime)
                            ):
                                continue
                            binary_delta2_extensions += 1
                            common = tuple(
                                coordinate
                                for coordinate in range(4)
                                if coordinate != distinguished
                            )
                            alpha_p = tuple(
                                tuple(
                                    alpha[mode][coordinate]
                                    for coordinate in common
                                ) + (vector[mode],)
                                for mode in range(4)
                            )
                            beta_p = tuple(
                                tuple(
                                    beta[mode][coordinate]
                                    for coordinate in common
                                ) + (vector[4 + mode],)
                                for mode in range(4)
                            )
                            marked_mode = (
                                0
                                if R and A == N
                                and distinguished in (0, 1)
                                else 2
                            )
                            marked_p = one_marked_map(
                                marked_mode, alpha_p, beta_p, prime
                            )
                            _rref, pivots = rref_mod(marked_p, prime)
                            assert len(pivots) == 4
                            pure_marked = one_marked_map(
                                marked_mode, alpha, beta, prime
                            )
                            assert any(
                                row[distinguished]
                                for row in pure_marked
                            )
                            marked_injective_extensions += 1
    assert binary_delta2_extensions == marked_injective_extensions
    return {
        "boundary_parameter_points": parameter_points,
        "binary_Delta2_projective_extensions": binary_delta2_extensions,
        "marked_injective_extensions": marked_injective_extensions,
        "successful_third_row_lifts": successful_third_row_lifts,
    }


def main() -> None:
    audits = {
        str(prime): audit_prime(prime)
        for prime in (5, 7)
    }
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": "DP permanent, modular kernels, projective extensions",
        "finite_fields": ["F_5", "F_7"],
        "audits": audits,
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "all_four_distinguished_orientations_excluded": True,
        "scope": "finite-field audit; written theorem is characteristic zero",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / "tmp" / "p5_h31_component_chart_boundary_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
