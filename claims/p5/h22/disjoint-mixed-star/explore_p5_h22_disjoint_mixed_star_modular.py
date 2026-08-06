#!/usr/bin/env python3
"""Exploratory modular diagnostic for weighted H22 on the eighth component.

This is finite-field evidence only.  It is deliberately not named or used as
a characteristic-zero theorem verifier.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
sys.path.insert(0, str(REPO_ROOT))

import audit_p5_h31_disjoint_mixed_star_component_generic_obstruction as A
from audit_p5_h31_marked_basis_open_branch import rank_mod


ROWS4 = tuple(itertools.combinations(range(8), 4))


def weighted(row, extension, direction, slope, modulus):
    if direction == "01":
        return (
            (slope * row[0] + row[1]) % modulus,
            row[2],
            row[3],
            extension,
        )
    if direction == "23":
        return (
            row[0],
            row[1],
            (slope * row[2] + row[3]) % modulus,
            extension,
        )
    raise ValueError(direction)


def coefficients(alpha, beta, direction, slope, extension, modulus):
    alpha_d = tuple(
        weighted(
            alpha[mode], extension[mode], direction, slope, modulus
        )
        for mode in range(4)
    )
    beta_d = tuple(
        weighted(
            beta[mode], extension[4 + mode], direction, slope, modulus
        )
        for mode in range(4)
    )
    return {
        bits: A.permanent(
            tuple(
                beta_d[mode] if bits[mode] else alpha_d[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in A.BITS4
    }, alpha_d, beta_d


def matrices(alpha, beta, direction, slope, modulus):
    columns = []
    for coordinate in range(8):
        extension = [0] * 8
        extension[coordinate] = 1
        values, _alpha_d, _beta_d = coefficients(
            alpha, beta, direction, slope, extension, modulus
        )
        columns.append(values)
    mixed_bits = tuple(
        bits
        for bits in A.BITS4
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


def main() -> None:
    modulus = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    sample = {
        11: (1, 2, 7, 3),
        13: (1, 3, 5, 10),
    }[modulus]
    slope = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    A.SAMPLES[modulus] = sample
    _parameters, alpha, canonical_beta = A.component_basis(modulus)
    for direction in ("01", "23"):
        survivors = []
        common_minors = {mode: set(ROWS4) for mode in range(4)}
        minimum_ranks = {mode: 4 for mode in range(4)}
        genuine_count = 0
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
            mixed, first, second = matrices(
                alpha, beta, direction, slope, modulus
            )
            rank, kernel = A.rref_nullspace(mixed, modulus)
            if not any(A.dot(first, vector, modulus) for vector in kernel):
                continue
            if not any(A.dot(second, vector, modulus) for vector in kernel):
                continue
            local_genuine = []
            for projective in A.projective_directions(
                len(kernel), modulus
            ):
                extension = A.combine(projective, kernel, modulus)
                if (
                    A.dot(first, extension, modulus)
                    and A.dot(second, extension, modulus)
                ):
                    local_genuine.append(extension)
            assert local_genuine
            survivors.append((shifts, rank, len(local_genuine)))
            for extension in local_genuine:
                _values, alpha_d, beta_d = coefficients(
                    alpha,
                    beta,
                    direction,
                    slope,
                    extension,
                    modulus,
                )
                for mode in range(4):
                    marked = A.one_marked_map(
                        mode, alpha_d, beta_d, modulus
                    )
                    observed_rank = rank_mod(marked, modulus)
                    minimum_ranks[mode] = min(
                        minimum_ranks[mode], observed_rank
                    )
                    nonzero = {
                        rows
                        for rows in ROWS4
                        if A.determinant_mod(
                            [
                                [
                                    marked[row][column]
                                    for column in range(4)
                                ]
                                for row in rows
                            ],
                            modulus,
                        )
                    }
                    common_minors[mode] &= nonzero
                genuine_count += 1
        print(
            direction,
            "survivors",
            len(survivors),
            "genuine directions",
            genuine_count,
        )
        if direction == "01":
            assert all(
                shifts[1] * shifts[2] % modulus == 0
                for shifts, _rank, _count in survivors
            )
        else:
            assert all(
                shifts[1] == shifts[2] == shifts[3] == 0
                for shifts, _rank, _count in survivors
            )
        assert all(rank == 7 for _shifts, rank, _count in survivors)
        assert minimum_ranks[0] == 4
        print("first survivors", survivors[:30])
        print("minimum marked ranks", minimum_ranks)
        print(
            "common nonzero minors",
            {
                mode: sorted(values)[:20]
                for mode, values in common_minors.items()
            },
        )


if __name__ == "__main__":
    main()
