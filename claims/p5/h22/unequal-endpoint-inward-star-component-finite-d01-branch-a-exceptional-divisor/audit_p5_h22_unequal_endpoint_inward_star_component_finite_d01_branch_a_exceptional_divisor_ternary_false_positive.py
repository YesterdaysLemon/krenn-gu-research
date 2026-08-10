#!/usr/bin/env python3
"""No-import audit of the component-25 ternary false-positive certificate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import time

import sympy as sp

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def permanent(square):
    return sp.expand(
        sum(
            sp.prod(square[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def add(*rows):
    return tuple(sum(row[index] for row in rows) for index in range(4))


def scale(coefficient, row):
    return tuple(coefficient * value for value in row)


def bases(e, j, k, s):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    pivot = e * j + k**2
    cross = e + j
    alpha = (
        add(scale(cross, cap_a), scale(-pivot, cap_b)),
        add(
            scale(cross, add(cap_a, scale(k, cap_d))),
            scale(-pivot, add(cap_b, scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(cap_a, scale(e, cap_b), scale(-k, cap_d)),
        add(cap_a, scale(-s * j, cap_c), scale(j, cap_b)),
    )
    return alpha, beta


def project(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    raise ValueError(direction)


def projected_marked(alpha, beta, extension, marking, direction, slope):
    alpha_p = tuple(
        project(alpha[index], extension[index], direction, slope) for index in range(4)
    )
    beta_c = tuple(
        project(beta[index], extension[4 + index], direction, slope)
        for index in range(4)
    )
    beta_p = tuple(
        add(beta_c[index], scale(marking[index], alpha_p[index])) for index in range(4)
    )
    return alpha_p, beta_p


def coefficient_tensor(alpha, beta):
    return {
        bits: permanent(
            tuple(beta[index] if bits[index] else alpha[index] for index in range(4))
        )
        for bits in BITS4
    }


def one_marked(mode, alpha, beta):
    rows = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(row)
    return sp.Matrix(rows)


def main():
    started = time.perf_counter()
    e, j, k, s = map(sp.Rational, (-5, 2, 3, -1))
    slope = sp.Rational(1, 3)
    extension = (
        sp.Rational(13, 448),
        sp.Rational(-33, 56),
        sp.Rational(-1, 56),
        sp.Rational(-3, 64),
        sp.Rational(-1, 28),
        sp.Rational(79, 448),
        sp.Rational(1, 28),
        sp.Rational(5, 32),
    )
    alpha, beta = bases(e, j, k, s)
    canonical_alpha = tuple(
        project(alpha[index], extension[index], "D01", slope) for index in range(4)
    )
    canonical_beta = tuple(
        project(beta[index], extension[4 + index], "D01", slope) for index in range(4)
    )
    canonical = coefficient_tensor(canonical_alpha, canonical_beta)
    assert canonical[BITS4[0]] == 1
    marking = tuple(
        -canonical[tuple(int(index == mode) for index in range(4))] for mode in range(4)
    )
    assert marking == (0, sp.Rational(5, 16), 2, sp.Rational(-38, 21))

    ranks = {}
    row_0123 = {}
    matrices = {}
    for direction in ("D01", "D23"):
        alpha_p, beta_p = projected_marked(
            alpha, beta, extension, marking, direction, slope
        )
        matrices[direction] = tuple(
            one_marked(mode, alpha_p, beta_p) for mode in range(4)
        )
        ranks[direction] = tuple(matrix.rank() for matrix in matrices[direction])
        row_0123[direction] = tuple(
            matrix.extract((0, 1, 2, 3), range(4)).det()
            for matrix in matrices[direction]
        )
        if direction == "D01":
            marked_tensor = coefficient_tensor(alpha_p, beta_p)
            assert marked_tensor[BITS4[0]] == 1
            assert marked_tensor[BITS4[-1]] == 0
            assert all(marked_tensor[bits] == 0 for bits in BITS4[1:-1])

    assert ranks == {"D01": (3, 3, 3, 3), "D23": (4, 4, 4, 4)}
    assert row_0123["D01"] == (0, 0, 0, 0)
    assert row_0123["D23"] == (
        sp.Rational(-380369, 9261),
        sp.Rational(-97669, 903168),
        sp.Rational(-505, 451584),
        sp.Rational(-6829, 8232),
    )
    fixed = matrices["D23"][1].extract((0, 4, 5, 6), range(4))
    assert fixed.det() == sp.Rational(-1, 28224)

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_false_positive_excluded",
                "role": "independent no-import exact-Q permanent audit",
                "unique_affine_marking": ["0", "5/16", "2", "-38/21"],
                "D01_one_marked_ranks": [3, 3, 3, 3],
                "D01_marked_all_beta_diagonal": "0",
                "D23_one_marked_ranks": [4, 4, 4, 4],
                "fixed_D23_mode1_rows0456_minor": "-1/28224",
                "entire_exceptional_divisor_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
