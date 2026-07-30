#!/usr/bin/env python3
"""Verify the exact-triangle obstruction in q5_221."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_TRIANGLE_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(rows) -> int:
    if not rows:
        return 0
    return int(sp.Matrix(rows).rank())


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


def add(*vectors):
    return tuple(
        sum(vector[index] for vector in vectors)
        for index in range(len(vectors[0]))
    )


def scale(value, vector):
    return tuple(value * coordinate for coordinate in vector)


def main() -> None:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = add(e[0], e[1])
    h0 = add(e[0], scale(-1, e[1]))
    u1 = add(e[2], e[3])
    h1 = add(e[2], scale(-1, e[3]))
    h2 = e[4]

    j02 = (u0, e[2], e[3])
    j12 = (e[0], e[1], u1)
    j01 = (u0, h1, h2)
    j10 = (h0, u1, h2)

    a, b, p, r, s, v = sp.symbols(
        "a b p r s v",
        nonzero=True,
    )
    c, q, t = sp.symbols("c q t")
    ua = (h0, h1, add(scale(a, u0), scale(b, u1), scale(c, h2)))
    uc = (h1, h2, add(scale(p, u0), scale(q, h0), scale(r, u1)))
    ub = (h0, h2, add(scale(s, u0), scale(t, h1), scale(v, u1)))

    ua02 = restrict(ua, j02)
    ua12 = restrict(ua, j12)
    uc02 = restrict(uc, j02)
    ub12 = restrict(ub, j12)
    assert rank(ua02) == rank(ua12) == 2
    assert rank(uc02) == rank(ub12) == 2

    expected_normals = {
        "A02": (b, -a, -a),
        "A12": (b, b, -a),
        "C02": (r, -p, -p),
        "B12": (v, v, -s),
    }
    restricted_rows = {
        "A02": ua02,
        "A12": ua12,
        "C02": uc02,
        "B12": ub12,
    }
    for name, normal in expected_normals.items():
        assert all(dot(row, normal) == 0 for row in restricted_rows[name])
        assert all(coordinate != 0 for coordinate in normal)

    b01 = restrict(ub, j01)
    c01 = restrict(uc, j01)
    b10 = restrict(ub, j10)
    c10 = restrict(uc, j10)
    assert rank(b01) == 2
    assert rank(c01) == 3
    assert rank(b10) == 3
    assert rank(c10) == 2
    c01_determinant = sp.factor(sp.Matrix(c01).det())
    b10_determinant = sp.factor(sp.Matrix(b10).det())
    assert c01_determinant != 0
    assert b10_determinant != 0

    assert all(dot(vector, h0) == 0 for vector in j01)
    assert all(dot(vector, u1) == 0 for vector in j01)
    assert all(dot(vector, u0) == 0 for vector in j10)
    assert all(dot(vector, h1) == 0 for vector in j10)
    assert rank((h0, u1)) == rank((u0, h1)) == 2
    # Optional h2 at mode D meets each direct-residual annihilator in
    # one line.  Rank one would additionally force h0 or h1, which the
    # strengthened incidence statement excludes.
    assert rank((h2, h0)) == rank((h2, h1)) == 2
    assert rank((h0, u1, h2)) == rank((u0, h1, h2)) == 3

    # Majority-singleton extension.  At the new rank-one Q01 gate,
    # U_D=span(h0,u1,aD*u0+bD*h1+cD*h2).  Its Q02 normal is
    # (bD,-aD,aD), while its J12 determinant is nonzero exactly when
    # aD is nonzero.
    a_d, b_d, c_d = sp.symbols("a_d b_d c_d")
    r_d = add(scale(a_d, u0), scale(b_d, h1), scale(c_d, h2))
    u_d = (h0, u1, r_d)
    d02 = restrict(u_d, j02)
    d12 = restrict(u_d, j12)
    d02_normal = (b_d, -a_d, a_d)
    assert all(dot(row, d02_normal) == 0 for row in d02)
    d12_determinant = sp.factor(sp.Matrix(d12).det())
    assert d12_determinant == -4 * a_d
    d02_a_zero = tuple(
        tuple(sp.sympify(value).subs(a_d, 0) for value in row)
        for row in d02
    )
    assert rank(d02_a_zero) == 2
    assert all(dot(row, (1, 0, 0)) == 0 for row in d02_a_zero)

    # Chirality II has no chirality-I support assumptions.  Give it
    # independent unrestricted parameters, then isolate each boundary
    # by its exact vanishing conditions.
    p2, q2, r2, s2, t2, v2 = sp.symbols(
        "p2 q2 r2 s2 t2 v2",
    )
    ub_target = (
        add(scale(s2, u0), scale(t2, h1), scale(v2, u1)),
        h2,
        h0,
    )
    uc_target = (
        h2,
        add(scale(p2, u0), scale(q2, h0), scale(r2, u1)),
        h1,
    )
    b01_exception = restrict(
        tuple(
            tuple(
                sp.sympify(entry).subs({s2: 0, t2: 0})
                for entry in row
            )
            for row in ub_target
        ),
        j01,
    )
    c10_exception = restrict(
        tuple(
            tuple(
                sp.sympify(entry).subs({q2: 0, r2: 0})
                for entry in row
            )
            for row in uc_target
        ),
        j10,
    )
    assert rank(b01_exception) == rank(c10_exception) == 1
    assert b01_exception[0] == (0, 0, 0)
    assert b01_exception[2] == (0, 0, 0)
    assert c10_exception[1] == (0, 0, 0)
    assert c10_exception[2] == (0, 0, 0)
    assert b01_exception[1] != (0, 0, 0)
    assert c10_exception[0] != (0, 0, 0)

    c01_rank_three_minor = sp.factor(sp.Matrix(restrict(uc_target, j01)).det())
    b10_rank_three_minor = sp.factor(sp.Matrix(restrict(ub_target, j10)).det())
    assert c01_rank_three_minor != 0
    assert b10_rank_three_minor != 0

    c01_p_zero = restrict(
        tuple(
            tuple(sp.sympify(entry).subs({p2: 0}) for entry in row)
            for row in uc_target
        ),
        j01,
    )
    b10_v_zero = restrict(
        tuple(
            tuple(sp.sympify(entry).subs({v2: 0}) for entry in row)
            for row in ub_target
        ),
        j10,
    )
    assert rank(c01_p_zero) == rank(b10_v_zero) == 2
    assert all(dot(row, (1, 0, 0)) == 0 for row in c01_p_zero)
    assert all(dot(row, (0, 1, 0)) == 0 for row in b10_v_zero)

    cross_zero_covectors = ((0, 0, 1), (0, 0, 2))
    assert rank(cross_zero_covectors) == 1
    assert rank((h0, h1)) == 2

    output = {
        "verified": True,
        "field": "C",
        "residual_spaces_checked": ["J02", "J12", "J01", "J10"],
        "full_support_normals_checked": list(expected_normals),
        "Q01_rank_profile_if_nonzero": [2, 3, "at_least_2"],
        "Q10_rank_profile_if_nonzero": [3, 2, "at_least_2"],
        "C_J01_rank_minor": str(c01_determinant),
        "B_J10_rank_minor": str(b10_determinant),
        "cross_scalar_zero_covector_rank": 1,
        "chirality_II_B_rank_one_target_row": 1,
        "chirality_II_C_rank_one_target_row": 0,
        "chirality_II_rank_one_conditions": ["s2=t2=0", "q2=r2=0"],
        "chirality_II_C_J01_rank_minor": str(c01_rank_three_minor),
        "chirality_II_B_J10_rank_minor": str(b10_rank_three_minor),
        "chirality_II_support_one_normals": ["u0", "u1"],
        "exact_triangle_excluded": True,
        "distinguished_singleton_triangle_cover_excluded": True,
        "majority_singleton_triangle_cover_excluded": True,
        "optional_D_h2_direct_residual_ranks": [2, 2],
        "optional_D_h2_cross_residual_minimum_rank": 2,
        "majority_singleton_Q02_normal": [
            str(value) for value in d02_normal
        ],
        "majority_singleton_J12_rank_minor": str(d12_determinant),
        "majority_singleton_a_zero_Q02_support": [0],
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_triangle_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
