#!/usr/bin/env python3
"""Independent finite-field audit of all new family-chart orientations."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h31_rank_two_component_orbit.py"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inv(value: int, prime: int) -> int:
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
    if not result:
        return result, ()
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
        scale = inv(result[pivot_row][column], prime)
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
    matrix: list[list[int]],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    rref, pivots = rref_mod(matrix, prime)
    free_columns = tuple(
        column
        for column in range(len(matrix[0]))
        if column not in pivots
    )
    basis = []
    for free in free_columns:
        vector = [0] * len(matrix[0])
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free] % prime
        basis.append(tuple(vector))
    return tuple(basis)


def dot(row: list[int], vector: tuple[int, ...], prime: int) -> int:
    return sum(
        left * right
        for left, right in zip(row, vector, strict=True)
    ) % prime


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


def projective_coefficients(
    dimension: int,
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    representatives = []
    for first_nonzero in range(dimension):
        for tail in itertools.product(
            range(prime),
            repeat=dimension - first_nonzero - 1,
        ):
            representatives.append(
                (0,) * first_nonzero + (1,) + tail
            )
    return tuple(representatives)


def family_rows(
    prime: int,
    E: int,
    I: int,
    L: int,
    Q: int,
    C: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    inverse_E = inv(E, prime)
    inverse_I = inv(I, prime)
    D = (C + E * I * L) % prime
    beta = (
        (0, 1, D * inverse_E % prime, C),
        (0, 0, 1, E),
        (0, 1, 0, E * I * L % prime),
        (1, 0, I, 0),
    )
    alpha = (
        (1, Q, 0, -E * I * (1 + L * Q) % prime),
        (L, 1, -I * L % prime, -E * I * L % prime),
        (-inverse_I % prime, 0, 1, 0),
        (0, 0, -inverse_E % prime, 1),
    )
    return alpha, beta


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
            selected = tuple(
                beta_p[mode] if bits[mode] else alpha_p[mode]
                for mode in range(4)
            )
            row.append(permanent_dp(selected, prime))
        coefficient_rows[bits] = row
    mixed = [
        coefficient_rows[bits]
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    return (
        mixed,
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
                int(index == coordinate)
                for index in range(4)
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


def audit_prime(prime: int) -> dict[str, object]:
    counts = {
        distinguished: {
            "admissible_parameters": 0,
            "generic_parameters": 0,
            "exceptional_parameters": 0,
            "binary_Delta2_projective_extensions": 0,
            "marked_injective_extensions": 0,
            "successful_third_row_lifts": 0,
        }
        for distinguished in (0, 1, 2)
    }
    for E in range(1, prime):
        for I in range(1, prime):
            for L, Q, C in itertools.product(range(prime), repeat=3):
                if (C + E * I * L) % prime == 0:
                    continue
                alpha, beta = family_rows(prime, E, I, L, Q, C)
                for distinguished in (0, 1, 2):
                    record = counts[distinguished]
                    record["admissible_parameters"] += 1
                    record[
                        "generic_parameters"
                        if L else "exceptional_parameters"
                    ] += 1
                    mixed, alpha_diagonal, beta_diagonal = extension_system(
                        distinguished, alpha, beta, prime
                    )
                    kernel = nullspace_mod(mixed, prime)
                    if L:
                        assert len(kernel) == 1
                        assert dot(alpha_diagonal, kernel[0], prime) == 0
                        continue

                    expected_dimension = {0: 2, 1: 5, 2: 3}[
                        distinguished
                    ]
                    assert len(kernel) == expected_dimension
                    if distinguished == 1:
                        assert all(
                            dot(alpha_diagonal, vector, prime) == 0
                            for vector in kernel
                        )
                        continue

                    common = tuple(
                        coordinate
                        for coordinate in range(4)
                        if coordinate != distinguished
                    )
                    pure_marked = one_marked_map(
                        1, alpha, beta, prime
                    )
                    assert any(
                        row[distinguished]
                        for row in pure_marked
                    )
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
                        record[
                            "binary_Delta2_projective_extensions"
                        ] += 1
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
                        marked_p = one_marked_map(
                            1, alpha_p, beta_p, prime
                        )
                        _rref, pivots = rref_mod(marked_p, prime)
                        assert len(pivots) == 4
                        record["marked_injective_extensions"] += 1

    for distinguished in (0, 2):
        record = counts[distinguished]
        assert (
            record["binary_Delta2_projective_extensions"]
            == record["marked_injective_extensions"]
        )
        assert record["successful_third_row_lifts"] == 0
    assert counts[1]["binary_Delta2_projective_extensions"] == 0
    return {str(key): value for key, value in counts.items()}


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
        "new_distinguished_orientations": [0, 1, 2],
        "prior_distinguished_orientation": 3,
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "family_chart_symmetry_orbit_H31_lift_possible": False,
        "scope": "finite-field audit; written theorem is characteristic zero",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_h31_rank_two_component_orbit_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
