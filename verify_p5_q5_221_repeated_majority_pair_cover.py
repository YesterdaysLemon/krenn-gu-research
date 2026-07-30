#!/usr/bin/env python3
"""Verify the exact repeated-majority-pair cover obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(*vectors):
    return tuple(
        sum(vector[index] for vector in vectors)
        for index in range(len(vectors[0]))
    )


def scale(value, vector):
    return tuple(value * coordinate for coordinate in vector)


def dot(first, second):
    return sum(
        left * right
        for left, right in zip(first, second, strict=True)
    )


def restrict(rows, basis):
    return tuple(
        tuple(dot(row, vector) for vector in basis)
        for row in rows
    )


def permanent(matrix):
    return sp.factor(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def tensor_coefficient(source_factors, rows, target_index):
    matrix = tuple(
        tuple(
            dot(rows[mode][target_index[mode]], source_factor)
            for source_factor in source_factors
        )
        for mode in range(4)
    )
    return permanent(matrix)


def main() -> None:
    e5 = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = add(e5[0], e5[1])
    h0 = add(e5[0], scale(-1, e5[1]))
    u1 = add(e5[2], e5[3])
    h1 = add(e5[2], scale(-1, e5[3]))
    h2 = e5[4]
    j01 = (u0, h1, h2)
    j10 = (h0, u1, h2)
    j12 = (e5[0], e5[1], u1)

    # The residual gates force these three row spaces.
    up = (h0, h1, u1)
    ur = (h1, h2, u0)
    assert sp.Matrix(restrict(up, j01)).rank() == 1
    assert sp.Matrix(restrict(up, j10)).rank() == 2
    assert sp.Matrix(restrict(ur, j10)).rank() == 1
    assert sp.Matrix(restrict(up, j12)).rank() == 2
    assert all(
        dot(row, (1, 1, 0)) == 0
        for row in restrict(up, j12)
    )

    # The two-summand Segre identity.  Every 2 x 2 minor of
    # a*z'^T+z*a'^T is a product of one wedge on each side.
    a0, a1, z0, z1, ap0, ap1, zp0, zp1 = sp.symbols(
        "a0 a1 z0 z1 ap0 ap1 zp0 zp1"
    )
    bilinear = sp.Matrix((a0, a1)) * sp.Matrix((zp0, zp1)).T
    bilinear += sp.Matrix((z0, z1)) * sp.Matrix((ap0, ap1)).T
    segre_minor = sp.factor(bilinear.det())
    expected_segre_minor = sp.factor(
        -(a0 * z1 - a1 * z0) * (ap0 * zp1 - ap1 * zp0)
    )
    assert segre_minor == expected_segre_minor

    p0, p1, p2, q0, q1, q2 = sp.symbols(
        "p0 p1 p2 q0 q1 q2"
    )
    a, b, c, d, ee, f = sp.symbols("a b c d e f")
    cap_a, cap_b, cap_c, alpha, beta = sp.symbols(
        "A B C alpha beta"
    )
    rows_p = (
        add(h1, scale(p0, u1)),
        add(h0, scale(p1, u1)),
        scale(p2, u1),
    )
    rows_q = (
        add(h1, scale(q0, u1)),
        add(h0, scale(q1, u1)),
        scale(q2, u1),
    )
    rows_r = (
        add(scale(a, h1), scale(b, u0)),
        add(h2, scale(c, h1), scale(d, u0)),
        add(scale(ee, h1), scale(f, u0)),
    )
    r0 = add(u0, scale(alpha, h1))
    r1 = add(u1, scale(beta, h1))
    rows_s = (
        add(h2, scale(cap_a, r0)),
        add(r1, scale(cap_b, r0)),
        scale(cap_c, r0),
    )
    rows = (rows_p, rows_q, rows_r, rows_s)

    # Incidences and the Q12 sign chart encoded by the normal form.
    assert all(
        sp.Matrix(mode_rows).rank() == 3
        for mode_rows in rows
    )
    assert sp.Matrix(restrict(rows_p, j01)).rank() == 1
    assert sp.Matrix(restrict(rows_q, j01)).rank() == 1
    assert sp.Matrix(restrict(rows_r, j10)).rank() == 1
    s12 = restrict(rows_s, j12)
    assert sp.Matrix(s12).rank() == 2
    assert all(dot(row, (1, -1, 0)) == 0 for row in s12)
    assert tuple(dot(row, h1) for row in rows_p) == (2, 0, 0)
    assert tuple(dot(row, h0) for row in rows_p) == (0, 2, 0)
    assert tuple(dot(row, h2) for row in rows_r) == (0, 1, 0)
    assert tuple(dot(row, u1) for row in rows_r) == (0, 0, 0)
    assert tuple(dot(row, h2) for row in rows_s) == (1, 0, 0)
    assert tuple(dot(row, u1) for row in rows_s) == (0, 2, 0)

    t0 = (u0, e5[2], e5[3], h2)
    t2 = (e5[0], e5[1], e5[2], e5[3])
    required_t0 = tensor_coefficient(t0, rows, (0, 0, 0, 0))
    forbidden_t0 = tensor_coefficient(t0, rows, (0, 0, 2, 0))
    required_t2 = tensor_coefficient(t2, rows, (2, 2, 2, 2))
    assert required_t0 == 4 * b * (p0 * q0 - 1)
    assert forbidden_t0 == 4 * f * (p0 * q0 - 1)
    assert required_t2 == 4 * cap_c * f * p2 * q2

    output = {
        "verified": True,
        "field": "C",
        "cover_orbit": 8,
        "exact_distinguished_normal_degrees": [2, 2, 2, 1],
        "residual_rank_one_gates": {
            "Q01": ["P", "Q"],
            "Q10": ["R"],
        },
        "Q12_plane_normals": ["u0", "u0", "h0"],
        "two_summand_segre_minor": str(segre_minor),
        "required_T0_0000": str(required_t0),
        "forbidden_T0_0020": str(forbidden_t0),
        "required_T2_2222": str(required_t2),
        "decisive_forced_zero": "f",
        "exact_cover_excluded": True,
        "monotone_cover_excluded": False,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_repeated_majority_pair_cover_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
