#!/usr/bin/env python3
"""Independent no-import audit of the projective common-kernel YY theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md"
PRIMARY = HERE / "verify_p4_common_kernel_yy_211_triangle_projective_classification.py"
COMPONENT13 = REPO_ROOT / "claims/p4/classifications/P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md"
DENSE = REPO_ROOT / "claims/p4/boundaries/P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))
MASKS3 = (14, 13, 11, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mul(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    out: dict[int, sp.Expr] = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            if lm & rm:
                continue
            out[lm | rm] = sp.expand(out.get(lm | rm, 0) + lv * rv)
    return out


def form(row: tuple[sp.Expr, ...]) -> dict[int, sp.Expr]:
    return {1 << i: value for i, value in enumerate(row) if value != 0}


def cubic(*rows: tuple[sp.Expr, ...]) -> sp.Matrix:
    value: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        value = mul(value, form(row))
    return sp.Matrix([sp.factor(value.get(mask, 0)) for mask in MASKS3])


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def wedge(plane: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.factor(plane[0][i] * plane[1][j] - plane[0][j] * plane[1][i])
            for i, j in PAIRS
        ]
    )


def reduce_zeta(value: sp.Expr, zeta: sp.Symbol) -> sp.Expr:
    numerator, denominator = sp.together(value).as_numer_denom()
    remainder = sp.rem(
        sp.Poly(numerator, zeta), sp.Poly(zeta**2 + zeta + 1, zeta)
    ).as_expr()
    return sp.factor(remainder / denominator)


def main() -> None:
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    beta, r, epsilon, zeta = sp.symbols("beta r epsilon zeta")
    m = add(scale(beta, c), b)
    mr = add(m, scale(r, c))

    C0 = cubic(a, a, a)
    C1 = cubic(a, m, a)
    C2 = cubic(m, mr, c)
    X = cubic(m, mr, a)
    W = sp.Matrix.hstack(C0, C1, C2)
    assert C0 == sp.zeros(4, 1)
    assert sp.factor(W.extract((0, 2), (1, 2)).det()) == 4
    assert sp.Matrix(a).T * W == sp.zeros(1, 3)
    assert sp.Matrix(b_bar).T * W == sp.zeros(1, 3)
    assert sp.factor((sp.Matrix(a).T * X)[0]) == 4
    assert (sp.Matrix(b_bar).T * X)[0] == 0

    # Rebuild the norm arc independently and compare leading wedges.
    K = 3 * beta**2 + 3 * beta * r + r**2
    V0 = zeta - zeta**2
    U = epsilon**2 * K / V0
    gamma = (V0 - U) / V0
    alpha = U + zeta * gamma
    norm = alpha**2 + alpha * gamma + gamma**2 - epsilon**2 * K
    assert reduce_zeta(norm, zeta) == 0

    arc = (
        (
            scale(epsilon, b_bar),
            add(
                scale(epsilon, b),
                scale(-(alpha + gamma), a),
                scale(-epsilon * (2 * beta + r), c),
            ),
        ),
        (add(scale(alpha, a), scale(epsilon * beta, c), scale(epsilon, b)), a),
        (
            add(
                scale(alpha, a),
                scale(epsilon * (beta + r), c),
                scale(epsilon, b),
            ),
            a,
        ),
        (c, add(scale(gamma, a), scale(epsilon, b))),
    )
    target = ((b_bar, a), (m, a), (mr, a), (c, a))
    proportionalities = []
    for index, (arc_plane, target_plane) in enumerate(zip(arc, target, strict=True)):
        divisor = epsilon if index < 3 else 1
        leading = (wedge(arc_plane) / divisor).applyfunc(
            lambda value: reduce_zeta(value.subs(epsilon, 0), zeta)
        )
        target_wedge = wedge(target_plane)
        minors = [
            reduce_zeta(
                leading[i] * target_wedge[j] - leading[j] * target_wedge[i], zeta
            )
            for i, j in PAIRS
        ]
        assert all(value == 0 for value in minors)
        assert any(value != 0 for value in leading)
        proportionalities.append(True)

    theorem = THEOREM.read_text(encoding="utf-8")
    component13 = COMPONENT13.read_text(encoding="utf-8")
    dense = DENSE.read_text(encoding="utf-8")
    for marker in (
        "full `YY` flag orbit produces no new component",
        "There is no rank-one-`W` vertical fibre",
        "component-thirteen Eisenstein norm quadric",
        "global conjecture remains **UNRESOLVED**",
    ):
        assert marker in theorem
    assert "F=alpha^2+alpha*gamma+gamma^2" in component13
    assert "X=m(m+r c)d" in dense

    print(
        json.dumps(
            {
                "status": "verified",
                "role": "independent no-import audit",
                "claim_label": "VERIFIED",
                "scope": "complete projective common-kernel YY triangle-(2,1,1) orientation",
                "t_zero_W_rank": 2,
                "t_zero_unique_annihilator": ["a", "b_bar"],
                "component13_norm_arc": True,
                "grassmann_limits": proportionalities,
                "primary_imported": False,
                "inputs": {
                    path.name: sha256(path)
                    for path in (THEOREM, PRIMARY, COMPONENT13, DENSE)
                },
                "finite_field_inference_used": False,
                "broad_search_used": False,
                "triangle_211_cell_exhausted": False,
                "global_Krenn_Gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
