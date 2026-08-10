#!/usr/bin/env python3
"""Independent finite-field audit of the second-component H31 point."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h31_diagonal_quadric_component_point.py"
MODULI = (5, 7)
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
ALPHA = (
    (3, -2, 0, -1),
    (1, 0, 0, -1),
    (0, 1, -1, 0),
    (1, -1, -1, 1),
)
CANONICAL_BETA = (
    (1, -1, 1, 1),
    (1, 1, -1, 1),
    (3, 1, 1, -1),
    (0, 1, 1, 0),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows: list[list[int]], modulus: int) -> int:
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
                ) % modulus
        table = next_table
    return table[15]


def matrix_rank_mod(matrix: list[list[int]], modulus: int) -> int:
    if not matrix:
        return 0
    work = [[entry % modulus for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, modulus)
        work[rank] = [
            entry * inverse % modulus for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def nullspace_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    work = [[entry % modulus for entry in row] for row in matrix]
    row = 0
    pivots: list[int] = []
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], -1, modulus)
        work[row] = [entry * inverse % modulus for entry in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            scale = work[other][column]
            if scale:
                work[other] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(
                        work[other], work[row], strict=True
                    )
                ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    free = [
        column for column in range(len(work[0])) if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [0] * len(work[0])
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[pivot_row][free_column] % modulus
        basis.append(vector)
    return basis


def shifted_beta(
    shifts: tuple[int, ...], modulus: int
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            (
                CANONICAL_BETA[mode][coordinate]
                + shifts[mode] * ALPHA[mode][coordinate]
            )
            % modulus
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def extension_coefficients(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    extension: list[int],
    modulus: int,
) -> dict[tuple[int, ...], int]:
    common = [
        coordinate for coordinate in range(4) if coordinate != distinguished
    ]
    alpha_extended = tuple(
        [alpha[mode][coordinate] for coordinate in common]
        + [extension[mode] % modulus]
        for mode in range(4)
    )
    beta_extended = tuple(
        [beta[mode][coordinate] for coordinate in common]
        + [extension[4 + mode] % modulus]
        for mode in range(4)
    )
    return {
        word: permanent_dp(
            [
                list(
                    beta_extended[mode]
                    if word[mode]
                    else alpha_extended[mode]
                )
                for mode in range(4)
            ],
            modulus,
        )
        for word in WORDS4
    }


def extension_system(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    modulus: int,
) -> tuple[list[list[int]], list[int], list[int]]:
    columns = []
    for column in range(8):
        extension = [0] * 8
        extension[column] = 1
        columns.append(
            extension_coefficients(
                distinguished,
                alpha,
                beta,
                extension,
                modulus,
            )
        )
    mixed_words = [
        word for word in WORDS4 if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    mixed = [
        [columns[column][word] for column in range(8)]
        for word in mixed_words
    ]
    diagonal_a = [
        columns[column][(0, 0, 0, 0)] for column in range(8)
    ]
    diagonal_b = [
        columns[column][(1, 1, 1, 1)] for column in range(8)
    ]
    return mixed, diagonal_a, diagonal_b


def dot(left: list[int], right: list[int], modulus: int) -> int:
    return sum(
        first * second
        for first, second in zip(left, right, strict=True)
    ) % modulus


def combine(
    coefficients: tuple[int, ...],
    basis: list[list[int]],
    modulus: int,
) -> list[int]:
    return [
        sum(
            coefficients[index] * basis[index][coordinate]
            for index in range(len(basis))
        )
        % modulus
        for coordinate in range(len(basis[0]))
    ]


def projective_vectors(dimension: int, modulus: int):
    for pivot in range(dimension):
        suffix_length = dimension - pivot - 1
        for suffix in itertools.product(range(modulus), repeat=suffix_length):
            yield (0,) * pivot + (1,) + suffix


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    modulus: int,
) -> list[list[int]]:
    rows = []
    for bits in WORDS3:
        selected: list[tuple[int, ...] | None] = []
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
                permanent_dp(
                    [
                        list(basis if other == mode else selected[other])
                        for other in range(4)
                    ],
                    modulus,
                )
            )
        rows.append(coefficient_row)
    return rows


def marked_extension(
    distinguished: int,
    extension: list[int],
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    mode: int,
    modulus: int,
) -> list[list[int]]:
    common = [
        coordinate for coordinate in range(4) if coordinate != distinguished
    ]
    alpha_extended = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row] % modulus,)
        for row in range(4)
    )
    beta_extended = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row] % modulus,)
        for row in range(4)
    )
    return one_marked_map(
        mode,
        alpha_extended,
        beta_extended,
        modulus,
    )


def audit_modulus(modulus: int) -> dict:
    alpha = tuple(
        tuple(entry % modulus for entry in row) for row in ALPHA
    )
    survivor_markings: dict[int, list[tuple[int, ...]]] = {}
    marking_points = 0
    for distinguished in range(4):
        survivors = []
        for shifts in itertools.product(range(modulus), repeat=4):
            marking_points += 1
            beta = shifted_beta(shifts, modulus)
            mixed, diagonal_a, diagonal_b = extension_system(
                distinguished,
                alpha,
                beta,
                modulus,
            )
            kernel = nullspace_mod(mixed, modulus)
            if not kernel:
                continue
            first_nonzero = any(
                dot(diagonal_a, vector, modulus) for vector in kernel
            )
            second_nonzero = any(
                dot(diagonal_b, vector, modulus) for vector in kernel
            )
            if first_nonzero and second_nonzero:
                survivors.append(shifts)
        survivor_markings[distinguished] = survivors

    assert survivor_markings == {
        0: [(0, 1, 1, 1)],
        1: [],
        2: [],
        3: [(0, -1 % modulus, 1, 1)],
    }

    extension_directions = 0
    genuine_extensions = 0
    marked_rank_tests = 0
    for distinguished in (0, 3):
        shifts = survivor_markings[distinguished][0]
        beta = shifted_beta(shifts, modulus)
        mixed, diagonal_a, diagonal_b = extension_system(
            distinguished,
            alpha,
            beta,
            modulus,
        )
        assert matrix_rank_mod(mixed, modulus) == 6
        kernel = nullspace_mod(mixed, modulus)
        assert len(kernel) == 2
        pure_map = one_marked_map(1, alpha, beta, modulus)
        assert any(row[distinguished] for row in pure_map)
        for coefficients in projective_vectors(len(kernel), modulus):
            extension_directions += 1
            extension = combine(coefficients, kernel, modulus)
            first = dot(diagonal_a, extension, modulus)
            second = dot(diagonal_b, extension, modulus)
            if not first or not second:
                continue
            genuine_extensions += 1
            marked = marked_extension(
                distinguished,
                extension,
                alpha,
                beta,
                1,
                modulus,
            )
            assert matrix_rank_mod(marked, modulus) == 4
            marked_rank_tests += 1

    assert extension_directions == 2 * (modulus + 1)
    assert genuine_extensions == 2 * (modulus - 1)
    assert marked_rank_tests == genuine_extensions
    return {
        "modulus": modulus,
        "marking_points": marking_points,
        "survivor_markings": {
            str(key): [list(marking) for marking in value]
            for key, value in survivor_markings.items()
        },
        "survivor_kernel_dimension": 2,
        "projective_extension_directions": extension_directions,
        "genuine_binary_extensions": genuine_extensions,
        "injective_marked_map_tests": marked_rank_tests,
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "fixed-fibre marking enumeration, DP permanent, "
            "projective kernel directions, and marked-map ranks"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "total_marking_points": sum(
            audit["marking_points"] for audit in audits
        ),
        "total_projective_extension_directions": sum(
            audit["projective_extension_directions"] for audit in audits
        ),
        "total_genuine_binary_extensions": sum(
            audit["genuine_binary_extensions"] for audit in audits
        ),
        "all_genuine_extensions_ternarily_excluded": True,
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
        / "p5_h31_diagonal_quadric_component_point_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
