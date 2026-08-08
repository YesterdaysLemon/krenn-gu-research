#!/usr/bin/env python3
"""Exploratory modular H31 diagnostic for the ninth (triangle) component.

This is finite-field evidence only.  It is deliberately not named or
used as a characteristic-zero theorem verifier.  Following the
disjoint mixed-star exploration pattern: marked bases
beta_i + t_i alpha_i, binary extension kernels of the 14x8 mixed
system for each distinguished source coordinate, survivor marking
loci, and one-marked-map ranks on the genuine directions.

Usage: python explore_p5_h31_all_rank_one_triangle_modular.py [prime]
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path


BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = tuple(
    bits for bits in BITS4 if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
ROWS4 = tuple(itertools.combinations(range(8), 4))
PERMS4 = tuple(itertools.permutations(range(4)))
SAMPLE_P = 2
SAMPLE_Q = 3


def family_rows(p, q, modulus):
    alpha = (
        (p * q + 1, 1, p, p * q + 1),
        (p, 1, 0, 0),
        (1, 0, -1, 0),
        (0, 0, 1, 1),
    )
    beta = (
        (q + 1, 0, 1, q),
        (0, 0, 1, -1),
        (-p, 1, 0, 0),
        (1, 0, 1, 0),
    )
    reduce_row = lambda row: tuple(value % modulus for value in row)
    return tuple(map(reduce_row, alpha)), tuple(map(reduce_row, beta))


def permanent4(rows, modulus):
    return sum(
        rows[0][pi[0]] * rows[1][pi[1]] * rows[2][pi[2]] * rows[3][pi[3]]
        for pi in PERMS4
    ) % modulus


def perm3(r0, r1, r2, modulus):
    return (
        r0[0] * (r1[1] * r2[2] + r1[2] * r2[1])
        + r0[1] * (r1[0] * r2[2] + r1[2] * r2[0])
        + r0[2] * (r1[0] * r2[1] + r1[1] * r2[0])
    ) % modulus


def rref_nullspace(matrix, modulus):
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
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
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                (left - scale * right) % modulus
                for left, right in zip(work[row], work[pivot_row])
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
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column] % modulus
        basis.append(tuple(vector))
    return len(pivots), tuple(basis)


def projective_directions(dimension, modulus):
    for pivot in range(dimension):
        for tail in itertools.product(
            range(modulus), repeat=dimension - pivot - 1
        ):
            yield (0,) * pivot + (1,) + tail


def determinant_mod(matrix, modulus):
    work = [[entry % modulus for entry in row] for row in matrix]
    size = len(work)
    result = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
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
                    work[row][offset] - scale * work[column][offset]
                ) % modulus
    return result % modulus


def rank_mod(matrix, modulus):
    rank, _basis = rref_nullspace(matrix, modulus)
    return rank


def one_marked_map(mode, alpha_ext, beta_ext, modulus):
    rows = []
    for bits in BITS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta_ext[other] if bits[bit_index] else alpha_ext[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent4(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    ),
                    modulus,
                )
            )
        rows.append(coefficient_row)
    return rows


def explore(modulus):
    alpha, beta0 = family_rows(SAMPLE_P, SAMPLE_Q, modulus)
    # pure sanity: single word -2
    pure = {
        bits: permanent4(
            tuple(
                beta0[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in BITS4
    }
    assert pure[(1, 1, 1, 1)] == (-2) % modulus
    assert all(
        value == 0 for bits, value in pure.items() if bits != (1, 1, 1, 1)
    )

    report = {}
    for distinguished in range(4):
        common = tuple(
            coordinate
            for coordinate in range(4)
            if coordinate != distinguished
        )
        alpha_common = tuple(
            tuple(alpha[mode][coordinate] for coordinate in common)
            for mode in range(4)
        )
        beta0_common = tuple(
            tuple(beta0[mode][coordinate] for coordinate in common)
            for mode in range(4)
        )
        survivors = []
        rank_histogram = {}
        genuine_count = 0
        minimum_ranks = {mode: 4 for mode in range(4)}
        common_minors = {mode: set(ROWS4) for mode in range(4)}
        for shifts in itertools.product(range(modulus), repeat=4):
            beta_common = tuple(
                tuple(
                    (b + shifts[mode] * a) % modulus
                    for b, a in zip(beta0_common[mode], alpha_common[mode])
                )
                for mode in range(4)
            )
            mixed_rows = []
            for word in MIXED:
                selected = tuple(
                    beta_common[mode] if word[mode] else alpha_common[mode]
                    for mode in range(4)
                )
                row = [0] * 8
                for mode in range(4):
                    others = tuple(
                        selected[other]
                        for other in range(4)
                        if other != mode
                    )
                    slot = mode + (4 if word[mode] else 0)
                    row[slot] = perm3(*others, modulus)
                mixed_rows.append(row)
            first = [0] * 8
            second = [0] * 8
            for mode in range(4):
                others_alpha = tuple(
                    alpha_common[other]
                    for other in range(4)
                    if other != mode
                )
                others_beta = tuple(
                    beta_common[other]
                    for other in range(4)
                    if other != mode
                )
                first[mode] = perm3(*others_alpha, modulus)
                second[4 + mode] = perm3(*others_beta, modulus)
            rank, kernel = rref_nullspace(mixed_rows, modulus)
            rank_histogram[rank] = rank_histogram.get(rank, 0) + 1
            if not kernel:
                continue

            def dot(row, vector):
                return sum(
                    left * right for left, right in zip(row, vector)
                ) % modulus

            if not any(dot(first, vector) for vector in kernel):
                continue
            if not any(dot(second, vector) for vector in kernel):
                continue
            genuine = []
            for direction in projective_directions(len(kernel), modulus):
                extension = tuple(
                    sum(
                        direction[index] * kernel[index][coordinate]
                        for index in range(len(kernel))
                    )
                    % modulus
                    for coordinate in range(8)
                )
                if dot(first, extension) and dot(second, extension):
                    genuine.append(extension)
            if not genuine:
                continue
            survivors.append((shifts, rank, len(genuine)))
            for extension in genuine:
                genuine_count += 1
                alpha_ext = tuple(
                    alpha_common[mode] + (extension[mode],)
                    for mode in range(4)
                )
                beta_ext = tuple(
                    beta_common[mode] + (extension[4 + mode],)
                    for mode in range(4)
                )
                for mode in range(4):
                    marked = one_marked_map(
                        mode, alpha_ext, beta_ext, modulus
                    )
                    observed = rank_mod(marked, modulus)
                    minimum_ranks[mode] = min(
                        minimum_ranks[mode], observed
                    )
                    nonzero = {
                        rows
                        for rows in ROWS4
                        if determinant_mod(
                            [marked[row] for row in rows], modulus
                        )
                    }
                    common_minors[mode] &= nonzero
        zero_coordinates = [
            coordinate
            for coordinate in range(4)
            if all(shifts[coordinate] == 0 for shifts, _r, _g in survivors)
        ] if survivors else []
        report[distinguished] = {
            "survivors": len(survivors),
            "genuine_directions": genuine_count,
            "mixed_rank_histogram": {
                str(rank): count
                for rank, count in sorted(rank_histogram.items())
            },
            "survivor_shifts_first_30": [
                list(shifts) for shifts, _rank, _count in survivors[:30]
            ],
            "survivor_mixed_ranks": sorted(
                {rank for _shifts, rank, _count in survivors}
            ),
            "forced_zero_shift_coordinates": zero_coordinates,
            "minimum_marked_ranks": {
                str(mode): rank for mode, rank in minimum_ranks.items()
            },
            "common_nonzero_minor_counts": {
                str(mode): len(values)
                for mode, values in common_minors.items()
            },
        }
        print(
            "distinguished",
            distinguished,
            "survivors",
            len(survivors),
            "genuine directions",
            genuine_count,
            "ranks",
            report[distinguished]["survivor_mixed_ranks"],
        )
        if survivors:
            print("  first survivors", [
                list(shifts) for shifts, _r, _g in survivors[:10]
            ])
            print(
                "  minimum marked ranks",
                report[distinguished]["minimum_marked_ranks"],
            )
    return report


def main() -> None:
    modulus = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    report = explore(modulus)
    output = {
        "exploratory_only": True,
        "finite_field_evidence_not_a_theorem": True,
        "component": "P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT",
        "modulus": modulus,
        "sample_p_q": [SAMPLE_P, SAMPLE_Q],
        "marked_bases_per_distinguished": modulus**4,
        "distinguished_reports": {
            str(key): value for key, value in report.items()
        },
    }
    output_path = Path(__file__).resolve().parent / "tmp" / (
        f"p5_h31_all_rank_one_triangle_modular_p{modulus}.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
