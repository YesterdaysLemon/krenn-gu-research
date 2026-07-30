#!/usr/bin/env python3
"""Verify the exact marked-end path obstruction in normalized q5_221."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_vector(left, right):
    return sp.Matrix(
        tuple(
            left[i] * right[j] + left[j] * right[i]
            for i, j in itertools.combinations(range(4), 2)
        )
    )


def pair_image_rank(left_basis, right_basis) -> int:
    vectors = tuple(
        pair_vector(left, right)
        for left in left_basis
        for right in right_basis
    )
    return int(sp.Matrix.hstack(*vectors).rank())


def tensor_coefficient(rows, factors):
    value = sp.Integer(0)
    for permutation in itertools.permutations(range(len(rows))):
        term = sp.Integer(1)
        for mode, factor_index in enumerate(permutation):
            term *= sp.Matrix(rows[mode]).dot(sp.Matrix(factors[factor_index]))
        value += term
    return sp.factor(value)


def main() -> None:
    e5 = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = tuple(e5[0][i] + e5[1][i] for i in range(5))
    h0 = tuple(e5[0][i] - e5[1][i] for i in range(5))
    u1 = tuple(e5[2][i] + e5[3][i] for i in range(5))
    h1 = tuple(e5[2][i] - e5[3][i] for i in range(5))
    h2 = e5[4]
    e4 = tuple(vector[:4] for vector in e5[:4])
    u0_4, h0_4, u1_4, h1_4 = (
        vector[:4] for vector in (u0, h0, u1, h1)
    )

    # Pair-image lemma.  T_u1 has kernel C h1.  If a plane U avoiding
    # h1 had total pair image with span(h0,u1) of dimension at most two,
    # T_h0(U) would lie in T_u1(U).  The coordinate comparison in the
    # theorem then collapses U to C u0.
    t_u1 = sp.Matrix.hstack(
        *(pair_vector(vector, u1_4) for vector in e4)
    )
    t_h0 = sp.Matrix.hstack(
        *(pair_vector(vector, h0_4) for vector in e4)
    )
    nullspace_u1 = t_u1.nullspace()
    assert len(nullspace_u1) == 1
    assert sp.Matrix.hstack(nullspace_u1[0], sp.Matrix(h1_4)).rank() == 1
    a, c, d, p, r, s = sp.symbols("a c d p r s")
    source = sp.Matrix((a, a, c, d))
    target = sp.Matrix((p, p, r, s))
    difference = sp.expand(t_h0 * source - t_u1 * target)
    equations = tuple(sp.expand(value) for value in difference)
    groebner = sp.groebner(equations, p, c, d, r, s, order="lex")
    assert groebner.reduce(c)[1] == 0
    assert groebner.reduce(d)[1] == 0
    assert pair_image_rank((u0_4, u1_4), (h0_4, u1_4)) == 3

    # The low-support hyperplane normal at D lies in span(u0,u1).
    # Support at most two leaves only the two coordinate-pair lines.
    x, y = sp.symbols("x y")
    d_normal = tuple(
        x * u0_4[index] + y * u1_4[index] for index in range(4)
    )
    assert d_normal == (x, x, y, y)
    assert tuple(value.subs({x: 1, y: 0}) for value in d_normal) == u0_4
    assert tuple(value.subs({x: 0, y: 1}) for value in d_normal) == u1_4

    # Q02 support-two normal chart (h1,u1,u1).  In factor coordinates
    # (u0,e2,e3), representative plane-row maps give a pure tensor whose
    # occupied row directions correspond to (u0,h1,h1).
    q02_factors = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    q02_rows = (
        ((1, 0, 0), (0, 1, 1)),
        ((1, 0, 0), (0, 1, -1)),
        ((1, 0, 0), (0, 1, -1)),
    )
    q02_nonzero = {}
    for target in itertools.product(range(2), repeat=3):
        selected = tuple(q02_rows[mode][target[mode]] for mode in range(3))
        coefficient = tensor_coefficient(selected, q02_factors)
        if coefficient:
            q02_nonzero[target] = coefficient
    assert q02_nonzero == {(0, 1, 1): -2}

    # Nonzero-Q02 branch.  The required T1 coefficient and forbidden T2
    # coefficient share the same gamma times the B,D two-row permanent,
    # with independent nonzero A-row scales.
    a1_scale, a2_scale, beta, gamma, delta = sp.symbols(
        "a1_scale a2_scale beta gamma delta",
        nonzero=True,
    )
    b_u, b_h, d_u, d_h = sp.symbols("b_u b_h d_u d_h")
    c_u, c_h = sp.symbols("c_u c_h")
    a1_row = tuple(a1_scale * value for value in h2)
    a2_row = tuple(
        a2_scale * (u1[i] + beta * h0[i]) for i in range(5)
    )
    b1_row = tuple(b_u * u0[i] + b_h * h0[i] for i in range(5))
    d1_row = tuple(d_u * u0[i] + d_h * h0[i] for i in range(5))
    c1_row = tuple(
        gamma * u1[i]
        + delta * h1[i]
        + c_u * u0[i]
        + c_h * h0[i]
        for i in range(5)
    )
    t1_factors = (e5[0], e5[1], u1, h2)
    t2_factors = e5[:4]
    required_q02 = tensor_coefficient(
        (a1_row, b1_row, c1_row, d1_row),
        t1_factors,
    )
    forbidden_q02 = tensor_coefficient(
        (a2_row, b1_row, c1_row, d1_row),
        t2_factors,
    )
    pair_permanent = 2 * (b_u * d_u - b_h * d_h)
    assert required_q02 == sp.factor(
        2 * a1_scale * gamma * pair_permanent
    )
    assert forbidden_q02 == sp.factor(
        2 * a2_scale * gamma * pair_permanent
    )

    # Remaining Q20 rank-one branch: C1 must take h2, B1 must take u1,
    # and the A1,D1 block is per(u0,h0)=0.
    aa, ab, dh, du, bh0, bh1, bu0, bu1, bh2 = sp.symbols(
        "aa ab dh du bh0 bh1 bu0 bu1 bh2"
    )
    rank_one_a1 = tuple(aa * u0[i] + ab * h2[i] for i in range(5))
    rank_one_b1 = tuple(
        bh0 * h0[i]
        + bh1 * h1[i]
        + bu0 * u0[i]
        + bu1 * u1[i]
        + bh2 * h2[i]
        for i in range(5)
    )
    pinned_c1 = h2
    rank_one_d1 = tuple(dh * h0[i] + du * h1[i] for i in range(5))
    rank_one_required = tensor_coefficient(
        (rank_one_a1, rank_one_b1, pinned_c1, rank_one_d1),
        t1_factors,
    )
    assert rank_one_required == 0

    # Remaining Q20 rank-two branch.
    rr, ss, bb, kk, sigma, cc, cap_c, dd, cap_a = sp.symbols(
        "rr ss bb kk sigma cc cap_c dd cap_a"
    )
    rank_two_a1 = tuple(
        rr * h2[i] + ss * (u1[i] + bb * u0[i])
        for i in range(5)
    )
    rank_two_b0 = u0
    rank_two_b1 = tuple(
        h0[i] + kk * h2[i] + sigma * u0[i]
        for i in range(5)
    )
    rank_two_c1 = tuple(cc * h2[i] for i in range(5))
    rank_two_d0 = tuple(
        cap_c * (u0[i] + dd * h2[i]) + cap_a * h0[i]
        for i in range(5)
    )
    rank_two_d1 = h0
    rank_two_required = tensor_coefficient(
        (rank_two_a1, rank_two_b1, rank_two_c1, rank_two_d1),
        t1_factors,
    )
    rank_two_forbidden = tensor_coefficient(
        (rank_two_a1, rank_two_b0, rank_two_c1, rank_two_d0),
        t1_factors,
    )
    assert rank_two_required == -4 * cc * ss
    assert rank_two_forbidden == 4 * cap_c * cc * ss

    output = {
        "verified": True,
        "field": "C",
        "pair_image_lemma_minimum": 3,
        "Q02_nonzero_chart": {
            str(key): str(value) for key, value in q02_nonzero.items()
        },
        "Q02_required_T1_coefficient": str(required_q02),
        "Q02_forbidden_T2_coefficient": str(forbidden_q02),
        "Q20_rank_one_required_T1_coefficient": str(rank_one_required),
        "Q20_rank_two_required_T1_coefficient": str(rank_two_required),
        "Q20_rank_two_forbidden_T1_coefficient": str(rank_two_forbidden),
        "exact_marked_end_path_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_marked_end_path_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
