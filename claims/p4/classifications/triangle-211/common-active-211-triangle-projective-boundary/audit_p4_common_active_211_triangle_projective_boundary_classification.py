#!/usr/bin/env python3
"""Independent no-import audit of the common-active projective boundary theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md"
PRIMARY = ROOT / "verify_p4_common_active_211_triangle_projective_boundary_classification.py"
COMPONENT11 = ROOT / "P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md"
COMPONENT12 = ROOT / "P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md"
MASKS3 = (14, 13, 11, 7)
PAIRS = tuple(itertools.combinations(range(4), 2))


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


def pair_product(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_map(
    left: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
    right: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(pair_product(lrow, rrow) for lrow in left for rrow in right)
    )


def wedge(plane: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.factor(plane[0][i] * plane[1][j] - plane[0][j] * plane[1][i])
            for i, j in PAIRS
        ]
    )


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def data(
    beta: sp.Expr,
    rho: sp.Expr,
    gamma: sp.Expr,
    delta: sp.Expr,
    s: tuple[sp.Expr, ...],
    t: tuple[sp.Expr, ...],
) -> tuple[sp.Matrix, sp.Matrix]:
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = add(scale(beta, c), s)
    mr = add(m, scale(rho, c))
    d = add(scale(gamma, a), scale(delta, c), t)
    return (
        sp.Matrix.hstack(cubic(a, a, d), cubic(a, m, d), cubic(m, mr, d)),
        cubic(m, mr, c),
    )


def main() -> None:
    beta, rho, gamma, delta, k, epsilon = sp.symbols(
        "beta rho gamma delta k epsilon", nonzero=True
    )
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    s_full = (0, 0, 1, k)
    s_bar = (0, 0, 1, -k)
    s_coordinate = (0, 0, 1, 0)
    zero_row = (0, 0, 0, 0)
    b0 = 2 * beta + rho

    # Independent reconstruction of the three boundary mechanisms.
    W_same, X_same = data(beta, rho, gamma, delta, s_coordinate, s_coordinate)
    assert all(sp.factor(value) == 0 for value in X_same + b0 * W_same[:, 0])

    t_generic = (0, 0, 1, k)
    W_coordinate, X_coordinate = data(
        beta, rho, gamma, delta, s_coordinate, t_generic
    )
    assert sp.factor(W_coordinate.extract((0, 1, 2), range(3)).det()) == 4 * k**3 * b0
    assert X_coordinate.subs(rho, -2 * beta) == sp.zeros(4, 1)

    W_t0, X_t0 = data(beta, rho, 1, 0, s_full, zero_row)
    assert sp.factor(W_t0.extract((0, 2), (1, 2)).det()) == -4 * k**2
    assert (sp.Matrix(c).T * W_t0) == sp.zeros(1, 3)
    assert (sp.Matrix(s_bar).T * W_t0) == sp.zeros(1, 3)
    assert sp.factor((sp.Matrix(c).T * X_t0)[0]) == -4 * k
    assert (sp.Matrix(s_bar).T * X_t0)[0] == 0

    # The component-eleven arc is checked only through Pluecker coordinates.
    zeta = sp.symbols("zeta")
    target = (
        (a, c),
        (a, add(scale(beta, c), s_full)),
        (a, add(scale(beta + rho, c), s_full)),
        (s_bar, c),
    )
    arc = (
        (a, c),
        (a, add(scale(zeta, c), s_full)),
        (a, add(scale(zeta + rho, c), s_full)),
        (s_bar, c),
    )
    assert all(sp.factor(value) == 0 for value in wedge(arc[1]).subs(zeta, beta) - wedge(target[1]))
    assert all(sp.factor(value) == 0 for value in wedge(arc[2]).subs(zeta, beta) - wedge(target[2]))
    assert all(sp.factor(value) == 0 for value in wedge(arc[1]).subs(zeta, 0) - wedge((a, s_full)))
    assert all(
        sp.factor(value) == 0
        for value in wedge(arc[2]).subs(zeta, 0)
        - wedge((a, add(scale(rho, c), s_full)))
    )

    # Coordinate t: derive the two factors without importing the primary code.
    W_boundary, _ = data(beta, rho, gamma, delta, s_full, s_coordinate)
    minors = tuple(
        sp.factor(W_boundary.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    )
    assert minors[0] == 0
    assert minors[1] == 4 * k**2 * (b0 + 2 * delta)
    reduced = tuple(sp.factor(value.subs(delta, -b0 / 2)) for value in minors[2:])
    assert reduced == (
        2 * k**2 * (b0 - 2 * gamma) * (b0 + 2 * gamma),
        2 * k**2 * (b0 - 2 * gamma) * (b0 + 2 * gamma),
    )

    arc_checks = {}
    for sign in (1, -1):
        delta_eps = -b0 * (k + epsilon) / (2 * k)
        gamma_eps = sign * delta_eps
        W_eps, _ = data(
            beta,
            rho,
            gamma_eps,
            delta_eps,
            s_full,
            (0, 0, 1, epsilon),
        )
        assert all(
            sp.factor(W_eps.extract(rows, range(3)).det()) == 0
            for rows in itertools.combinations(range(4), 3)
        )
        limit = W_eps.subs(epsilon, 0)
        assert sp.factor(limit.extract((0, 3), (0, 1)).det()) == -2 * k
        arc_checks[str(sign)] = "dense polarity sheet with regular rank-two limit"

    # A rational all-pair sample of the component-eleven boundary.
    sample = {beta: 2, rho: 3, k: 5}
    sample_planes = (
        (s_bar, c),
        (a, add(scale(beta, c), s_full)),
        (a, add(scale(beta + rho, c), s_full)),
        (a, c),
    )
    profile = [
        pair_map(sample_planes[i], sample_planes[j]).subs(sample).rank()
        for i, j in PAIRS
    ]
    assert profile == [3, 3, 3, 3, 3, 3]

    theorem = THEOREM.read_text(encoding="utf-8")
    component11 = COMPONENT11.read_text(encoding="utf-8")
    component12 = COMPONENT12.read_text(encoding="utf-8")
    for marker in (
        "complete common-active, genuine-support-two orientation",
        "component-eleven closure",
        "component-twelve polarity sheets",
        "remains **UNKNOWN**",
    ):
        assert marker in theorem
    assert "U_0=span(a+p b" in component11
    assert "gamma^2=delta^2" in component12

    print(
        json.dumps(
            {
                "status": "verified",
                "role": "independent no-import audit",
                "claim_label": "VERIFIED",
                "scope": "projective common-active triangle-(2,1,1) boundary",
                "component11_boundary_profile": profile,
                "component12_arc_checks": arc_checks,
                "primary_imported": False,
                "inputs": {
                    path.name: sha256(path)
                    for path in (THEOREM, PRIMARY, COMPONENT11, COMPONENT12)
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
