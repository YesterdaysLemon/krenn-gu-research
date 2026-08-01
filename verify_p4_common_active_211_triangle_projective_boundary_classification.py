#!/usr/bin/env python3
"""Exact verifier for the projective common-active (2,1,1) triangle boundary."""

from __future__ import annotations

import itertools
import json

import sympy as sp

MASKS3 = (14, 13, 11, 7)
PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def multiply(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            if lm & rm:
                continue
            result[lm | rm] = sp.expand(result.get(lm | rm, 0) + lv * rv)
    return result


def linear(row: sp.Matrix) -> dict[int, sp.Expr]:
    return {1 << i: sp.sympify(row[i]) for i in range(4) if row[i] != 0}


def triple(*rows: sp.Matrix) -> sp.Matrix:
    value: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        value = multiply(value, linear(row))
    return sp.Matrix([sp.expand(value.get(mask, 0)) for mask in MASKS3])


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


def plucker(plane: tuple[sp.Matrix, sp.Matrix]) -> sp.Matrix:
    matrix = sp.Matrix.vstack(plane[0].T, plane[1].T)
    return sp.Matrix(
        [sp.factor(matrix[:, (i, j)].det()) for i, j in PAIRS]
    )


def cubic_data(
    a: sp.Matrix,
    c: sp.Matrix,
    beta: sp.Expr,
    rho: sp.Expr,
    gamma: sp.Expr,
    delta: sp.Expr,
    s: sp.Matrix,
    t: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    m = beta * c + s
    mr = m + rho * c
    d = gamma * a + delta * c + t
    return (
        sp.Matrix.hstack(triple(a, a, d), triple(a, m, d), triple(m, mr, d)),
        triple(m, mr, c),
    )


def zero(expr: sp.Expr) -> bool:
    return sp.factor(expr) == 0


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    c = sp.Matrix((1, -1, 0, 0))
    assert product(a, c) == sp.zeros(6, 1)

    beta, rho, u, v, p, q, gamma, delta = sp.symbols(
        "beta rho u v p q gamma delta"
    )
    s = sp.Matrix((0, 0, u, v))
    t = sp.Matrix((0, 0, p, q))
    W, _X = cubic_data(a, c, beta, rho, gamma, delta, s, t)
    polar = u * q + v * p
    determinant = u * q - v * p
    energy = (2 * beta + rho) * polar
    minors = tuple(
        sp.factor(W.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    )
    expected = (
        4 * q * polar * (energy + 2 * delta * u * v),
        4 * p * polar * (energy + 2 * delta * u * v),
        -4 * (gamma - delta) * determinant * (energy - 2 * gamma * u * v),
        4 * (gamma + delta) * determinant * (energy + 2 * gamma * u * v),
    )
    assert all(zero(left - right) for left, right in zip(minors, expected, strict=True))

    # s=0 collapses the synchronized pair image to dimension at most one.
    m0 = beta * c
    mr0 = (beta + rho) * c
    collapsed_pair = pair_matrix((a, m0), (a, mr0))
    assert all(
        zero(collapsed_pair.extract(rows, columns).det())
        for rows in itertools.combinations(range(6), 2)
        for columns in itertools.combinations(range(4), 2)
    )

    k = sp.symbols("k", nonzero=True)
    s_full = sp.Matrix((0, 0, 1, k))
    s_bar = sp.Matrix((0, 0, 1, -k))
    z = sp.symbols("z")

    # t=0.  Coordinate s has no escape; full s has the unique component-11 plane.
    s_coordinate = sp.Matrix((0, 0, 1, 0))
    W_t0_coord, X_t0_coord = cubic_data(
        a, c, beta, rho, 1, 0, s_coordinate, sp.zeros(4, 1)
    )
    assert X_t0_coord == -(2 * beta + rho) * W_t0_coord[:, 1]

    W_t0, X_t0 = cubic_data(a, c, beta, rho, 1, 0, s_full, sp.zeros(4, 1))
    assert sp.factor(W_t0.extract((0, 2), (1, 2)).det()) == -4 * k**2
    assert W_t0.T * c == sp.zeros(3, 1)
    assert W_t0.T * s_bar == sp.zeros(3, 1)
    assert sp.factor((c.T * X_t0)[0]) == -4 * k
    assert sp.factor((s_bar.T * X_t0)[0]) == 0

    mode_swap_target = (
        (a, c),
        (a, beta * c + s_full),
        (a, (beta + rho) * c + s_full),
        (s_bar, c),
    )
    component11_arc = (
        (a, c),
        (a, z * c + s_full),
        (a, (z + rho) * c + s_full),
        (s_bar, c),
    )
    for target_plane, arc_plane in zip(mode_swap_target, component11_arc, strict=True):
        assert all(
            zero(value)
            for value in plucker(arc_plane).subs(z, beta) - plucker(target_plane)
        )
    limit_arc = tuple(
        tuple(row.subs(z, 0) for row in plane) for plane in component11_arc
    )
    beta_zero_target = (
        (a, c),
        (a, s_full),
        (a, rho * c + s_full),
        (s_bar, c),
    )
    assert all(
        all(zero(value) for value in plucker(left) - plucker(right))
        for left, right in zip(limit_arc, beta_zero_target, strict=True)
    )

    pure_planes = ((s_bar, c), mode_swap_target[1], mode_swap_target[2], (a, c))
    coefficients = {
        bits: permanent(tuple(pure_planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    assert {bits: value for bits, value in coefficients.items() if value != 0} == {
        (1, 1, 1, 1): -4 * k
    }
    assert [
        pair_matrix(pure_planes[i], pure_planes[j]).rank() for i, j in PAIRS
    ] == [3, 3, 3, 3, 3, 3]

    # s coordinate, t nonzero: same-support gives X in W; otherwise rank forces X=0.
    t_same = sp.Matrix((0, 0, 1, 0))
    W_same, X_same = cubic_data(a, c, beta, rho, gamma, delta, s_coordinate, t_same)
    assert X_same == -(2 * beta + rho) * W_same[:, 0]

    t_moving = sp.Matrix((0, 0, 1, k))
    W_moving, X_moving = cubic_data(
        a, c, beta, rho, gamma, delta, s_coordinate, t_moving
    )
    assert sp.factor(W_moving.extract((0, 1, 2), range(3)).det()) == 4 * k**3 * (
        2 * beta + rho
    )
    assert X_moving.subs(rho, -2 * beta) == sp.zeros(4, 1)

    t_opposite = sp.Matrix((0, 0, 0, 1))
    W_opposite, X_opposite = cubic_data(
        a, c, beta, rho, gamma, delta, s_coordinate, t_opposite
    )
    assert zero(
        W_opposite.extract((0, 1, 2), range(3)).det()
        - 4 * (2 * beta + rho)
    )
    assert X_opposite.subs(rho, -2 * beta) == sp.zeros(4, 1)

    # s full, t coordinate: exactly the two limits gamma=+/-delta.
    t_coordinate = sp.Matrix((0, 0, 1, 0))
    W_boundary, _ = cubic_data(
        a, c, beta, rho, gamma, delta, s_full, t_coordinate
    )
    boundary_minors = tuple(
        sp.factor(W_boundary.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    )
    b0 = 2 * beta + rho
    assert boundary_minors == (
        0,
        4 * k**2 * (b0 + 2 * delta),
        -4 * k**2 * (delta - gamma) * (b0 - 2 * gamma),
        -4 * k**2 * (delta + gamma) * (b0 + 2 * gamma),
    )
    epsilon = sp.symbols("epsilon")
    t_epsilon = sp.Matrix((0, 0, 1, epsilon))
    arc_results = {}
    for sign in (1, -1):
        delta_epsilon = -b0 * (k + epsilon) / (2 * k)
        gamma_epsilon = sign * delta_epsilon
        W_arc, _ = cubic_data(
            a,
            c,
            beta,
            rho,
            gamma_epsilon,
            delta_epsilon,
            s_full,
            t_epsilon,
        )
        assert all(
            zero(W_arc.extract(rows, range(3)).det())
            for rows in itertools.combinations(range(4), 3)
        )
        W_limit = W_arc.subs(epsilon, 0)
        boundary_substitution = {
            delta: -b0 / 2,
            gamma: sign * (-b0 / 2),
        }
        assert all(
            zero(value)
            for value in W_limit - W_boundary.subs(boundary_substitution)
        )
        assert zero(W_limit.extract((0, 3), (0, 1)).det() + 2 * k)
        arc_results[str(sign)] = {
            "delta_epsilon": str(delta_epsilon),
            "gamma_epsilon": str(gamma_epsilon),
            "rank_two_witness": str(
                sp.factor(W_limit.extract((0, 3), (0, 1)).det())
            ),
        }

    print(
        json.dumps(
            {
                "status": "verified",
                "claim_label": "VERIFIED",
                "scope": "projective boundary of the common-active genuine-support-two triangle-(2,1,1) orientation",
                "general_polarity_minors": [str(value) for value in expected],
                "s_zero": "pair rank at most one",
                "t_zero": "component 11 closure or zero",
                "s_coordinate": "no nonzero pure escape",
                "t_coordinate_arcs": arc_results,
                "dense_orientation_now_projectively_exhausted": True,
                "triangle_211_cell_exhausted": False,
                "global_Krenn_Gu_resolved": False,
                "finite_field_inference_used": False,
                "broad_search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
