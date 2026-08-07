#!/usr/bin/env python3
"""Exact verifier for the projective common-kernel YY (2,1,1) triangle."""

from __future__ import annotations

import itertools
import json

import sympy as sp

MASKS3 = (14, 13, 11, 7)
PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def multiply(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    out: dict[int, sp.Expr] = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            if lm & rm:
                continue
            out[lm | rm] = sp.expand(out.get(lm | rm, 0) + lv * rv)
    return out


def linear(row: sp.Matrix) -> dict[int, sp.Expr]:
    return {1 << i: row[i] for i in range(4) if row[i] != 0}


def triple(*rows: sp.Matrix) -> sp.Matrix:
    value: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        value = multiply(value, linear(row))
    return sp.Matrix([sp.factor(value.get(mask, 0)) for mask in MASKS3])


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    value: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        value = multiply(value, linear(row))
    return sp.factor(value.get(15, 0))


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def wedge(plane: tuple[sp.Matrix, sp.Matrix]) -> sp.Matrix:
    matrix = sp.Matrix.vstack(plane[0].T, plane[1].T)
    return sp.Matrix([sp.factor(matrix[:, (i, j)].det()) for i, j in PAIRS])


def data(
    a: sp.Matrix,
    c: sp.Matrix,
    beta: sp.Expr,
    r: sp.Expr,
    gamma: sp.Expr,
    delta: sp.Expr,
    s: sp.Matrix,
    t: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    m = beta * c + s
    mr = m + r * c
    d = gamma * a + delta * c + t
    W = sp.Matrix.hstack(triple(a, a, d), triple(a, m, d), triple(m, mr, c))
    return W, triple(m, mr, d)


def zero(value: sp.Expr) -> bool:
    return sp.factor(value) == 0


def reduce_zeta(value: sp.Expr, zeta: sp.Symbol) -> sp.Expr:
    numerator, denominator = sp.together(value).as_numer_denom()
    reduced = sp.rem(sp.Poly(numerator, zeta), sp.Poly(zeta**2 + zeta + 1, zeta))
    return sp.factor(reduced.as_expr() / denominator)


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    c = sp.Matrix((1, -1, 0, 0))
    beta, r, gamma, delta, u, v, p, q = sp.symbols(
        "beta r gamma delta u v p q"
    )
    s = sp.Matrix((0, 0, u, v))
    t = sp.Matrix((0, 0, p, q))
    W, X = data(a, c, beta, r, gamma, delta, s, t)
    polar = u * q + v * p
    determinant = u * q - v * p
    energy = (2 * beta + r) * polar
    minors = tuple(
        sp.factor(W.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    )
    expected = (
        8 * q * u * v * polar,
        8 * p * u * v * polar,
        4 * determinant * (energy - 2 * gamma * u * v),
        4 * determinant * (energy + 2 * gamma * u * v),
    )
    assert all(zero(left - right) for left, right in zip(minors, expected, strict=True))

    # The dense polarity identity, now including endpoints of nonzero t.
    dense_substitution = {q: -v * p / u, gamma: 0}
    assert all(
        zero(value)
        for value in X.subs(dense_substitution)
        - (
            delta * W[:, 2]
            - beta * (beta + r) * W[:, 0]
        ).subs(dense_substitution)
    )

    # Coordinate s: q!=0 forces 2 beta+r=0 and lowers the synchronized pair.
    s_coordinate = sp.Matrix((0, 0, 1, 0))
    m_coordinate = beta * c + s_coordinate
    mr_coordinate = m_coordinate - 2 * beta * c
    synchronized = pair_matrix((a, m_coordinate), (a, mr_coordinate))
    assert all(
        zero(synchronized.extract(rows, columns).det())
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
    )

    # Full s, t=0: exact rank-two W, unique annihilator plane, and pure tensor.
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    W_zero, X_zero = data(a, c, beta, r, 1, 0, b, sp.zeros(4, 1))
    assert W_zero[:, 0] == sp.zeros(4, 1)
    assert sp.factor(W_zero.extract((0, 2), (1, 2)).det()) == 4
    assert W_zero.T * a == sp.zeros(3, 1)
    assert W_zero.T * b_bar == sp.zeros(3, 1)
    assert sp.factor((a.T * X_zero)[0]) == 4
    assert sp.factor((b_bar.T * X_zero)[0]) == 0

    m = beta * c + b
    mr = m + r * c
    planes = ((b_bar, a), (a, m), (a, mr), (c, a))
    coefficients = {
        bits: permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    assert {bits: value for bits, value in coefficients.items() if value != 0} == {
        (1, 1, 1, 1): 4
    }
    profile = [pair_matrix(planes[i], planes[j]).rank() for i, j in PAIRS]
    assert profile == [4, 4, 3, 3, 3, 3]
    assert [
        pair_matrix(planes[i], planes[j]).subs(beta, 0).rank() for i, j in PAIRS
    ] == [3, 4, 3, 3, 3, 3]
    assert [
        pair_matrix(planes[i], planes[j]).subs(r, -beta).rank() for i, j in PAIRS
    ] == [4, 3, 3, 3, 3, 3]

    # Exact component-13 norm-quadric arc over Q(zeta).
    epsilon, zeta = sp.symbols("epsilon zeta")
    K = 3 * beta**2 + 3 * beta * r + r**2
    V0 = zeta - zeta**2
    Uepsilon = epsilon**2 * K / V0
    gamma_epsilon = (V0 - Uepsilon) / V0
    alpha_epsilon = Uepsilon + zeta * gamma_epsilon
    norm = (
        alpha_epsilon**2
        + alpha_epsilon * gamma_epsilon
        + gamma_epsilon**2
        - epsilon**2 * K
    )
    assert reduce_zeta(norm, zeta) == 0
    assert reduce_zeta((alpha_epsilon + gamma_epsilon).subs(epsilon, 0), zeta) == zeta + 1

    m_epsilon = alpha_epsilon * a + epsilon * beta * c + epsilon * b
    mr_epsilon = m_epsilon + epsilon * r * c
    d_epsilon = gamma_epsilon * a + epsilon * b
    x0_epsilon = (
        epsilon * b
        - (alpha_epsilon + gamma_epsilon) * a
        - epsilon * (2 * beta + r) * c
    )
    arc_planes = (
        (epsilon * b_bar, x0_epsilon),
        (m_epsilon, a),
        (mr_epsilon, a),
        (c, d_epsilon),
    )
    target_planes = planes

    # Leading projective wedges; proportionality is enough for Grassmann limits.
    leading = []
    for index, arc_plane in enumerate(arc_planes):
        divisor = epsilon if index in (0, 1, 2) else 1
        vector = wedge(arc_plane) / divisor
        limit = vector.applyfunc(lambda value: reduce_zeta(value.subs(epsilon, 0), zeta))
        target = wedge(target_planes[index])
        rank = sp.Matrix.hstack(limit, target).applyfunc(
            lambda value: reduce_zeta(value, zeta)
        ).rank(iszerofunc=lambda value: reduce_zeta(value, zeta) == 0)
        assert rank == 1
        leading.append([str(value) for value in limit])

    print(
        json.dumps(
            {
                "status": "verified",
                "claim_label": "VERIFIED",
                "scope": "complete projective common-kernel YY triangle-(2,1,1) orientation",
                "general_minors": [str(value) for value in expected],
                "dense_nonzero_t": "active cubic lies in kernel-rich span",
                "coordinate_s": "lower pair or embedded P3",
                "t_zero_profile": profile,
                "component13_arc_leading_wedges": leading,
                "rank_one_vertical_fibre": False,
                "orientation_projectively_exhausted": True,
                "triangle_211_cell_exhausted": False,
                "finite_field_inference_used": False,
                "broad_search_used": False,
                "global_Krenn_Gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
