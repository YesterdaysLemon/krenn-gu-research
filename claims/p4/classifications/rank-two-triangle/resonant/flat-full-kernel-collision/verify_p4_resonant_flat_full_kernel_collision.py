#!/usr/bin/env python3
"""Exact replay of the full-kernel collision classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def product2(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def cross(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.simplify(
        product2(left[:4, 0], right[4:, 0])
        - product2(left[4:, 0], right[:4, 0])
    )


def product3(*rows: sp.Matrix) -> sp.Matrix:
    values = []
    for omitted in range(4):
        columns = [index for index in range(4) if index != omitted]
        values.append(
            sp.expand(
                sum(
                    sp.prod(rows[index][columns[permutation[index]]] for index in range(3))
                    for permutation in itertools.permutations(range(3))
                )
            )
        )
    return sp.Matrix(values)


def coefficient_matrix(
    y: sp.Matrix,
    x: sp.Matrix,
    y2: sp.Matrix,
    x2: sp.Matrix,
    y3: sp.Matrix,
    x3: sp.Matrix,
) -> sp.Matrix:
    return sp.Matrix.hstack(
        product3(y, y2, y3),
        product3(x, y2, y3),
        product3(y, x2, x3),
        product3(x, x2, x3),
    )


def pair_matrix(
    y2: sp.Matrix, x2: sp.Matrix, y3: sp.Matrix, x3: sp.Matrix
) -> sp.Matrix:
    return sp.Matrix.hstack(
        product2(y2, y3),
        product2(y2, x3),
        product2(x2, y3),
        product2(x2, x3),
    )


def minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def synchronizer_matrix(y: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    variables = sp.symbols("a0:4 b0:4")
    candidate_y = sp.Matrix(variables[:4])
    candidate_x = sp.Matrix(variables[4:])
    matrix, _ = sp.linear_eq_to_matrix(
        list(product2(y, candidate_x) - product2(x, candidate_y)), variables
    )
    return matrix


def main() -> None:
    ell, r, s, t, u = sp.symbols("ell r s t u")
    y = sp.ones(4, 1)

    # Multiplicity 2+1+1.  The synchronizer is a line whose point at
    # infinity has local rank one.  Every valid partner has active row x,
    # and x^3=0 because x has support two.
    x211 = sp.Matrix((0, 0, 1, ell))
    z211 = sp.Matrix((0, 0, -1, ell))
    A211 = sp.Matrix.vstack(y, x211)
    B211 = sp.Matrix.vstack(z211, sp.zeros(4, 1))
    sync211 = synchronizer_matrix(y, x211)
    basis211 = sp.Matrix.hstack(A211, B211)
    assert sync211.rank() == 6
    assert sync211 * basis211 == sp.zeros(6, 2)
    assert basis211.rank() == 2
    assert sp.Matrix.vstack(z211.T, sp.zeros(1, 4)).rank() == 1
    assert product3(x211, x211, x211) == sp.zeros(4, 1)

    # Multiplicity 3+1 has the identical mechanism with support-one x.
    x31 = sp.Matrix((0, 0, 0, 1))
    z31 = sp.Matrix((0, 0, 0, 1))
    A31 = sp.Matrix.vstack(y, x31)
    B31 = sp.Matrix.vstack(z31, sp.zeros(4, 1))
    sync31 = synchronizer_matrix(y, x31)
    basis31 = sp.Matrix.hstack(A31, B31)
    assert sync31.rank() == 6
    assert sync31 * basis31 == sp.zeros(6, 2)
    assert basis31.rank() == 2
    assert product3(x31, x31, x31) == sp.zeros(4, 1)

    # Multiplicity 2+2.  Its synchronizer is a projective plane with a
    # one-dimensional radical for the induced alternating product form.
    x22 = sp.Matrix((0, 0, 1, 1))
    A = sp.Matrix.vstack(y, x22)
    B0 = sp.Matrix.vstack(sp.Matrix((0, 0, -1, 1)), sp.zeros(4, 1))
    B1 = sp.Matrix.vstack(sp.Matrix((-1, 1, 0, 0)), sp.Matrix((-1, 1, 0, 0)))
    sync22 = synchronizer_matrix(y, x22)
    basis22 = sp.Matrix.hstack(A, B0, B1)
    assert sync22.rank() == 5
    assert sync22 * basis22 == sp.zeros(6, 3)
    assert basis22.rank() == 3
    omega = sp.Matrix((0, 1, -1, -1, 1, 0))
    assert cross(A, B0) == cross(A, B1) == sp.zeros(6, 1)
    assert cross(B0, B1) == omega

    D = r * B0 + s * B1
    dy, dx = D[:4, 0], D[4:, 0]
    y2, x2 = y + t * dy, x22 + t * dx
    y3, x3 = y + u * dy, x22 + u * dx
    assert cross(sp.Matrix.vstack(y2, x2), sp.Matrix.vstack(y3, x3)) == sp.zeros(6, 1)

    C = coefficient_matrix(y, x22, y2, x2, y3, x3)
    triples4 = tuple(itertools.combinations(range(4), 3))
    compression = [sp.factor(C.extract(rows, (0, 1, 2)).det()) for rows in triples4]
    expected_compression = [
        -16 * s * (t + u) * (r * t + 1) * (r * u + 1),
        -16 * s * (t + u) * (r * t - 1) * (r * u - 1),
        16 * r * (t + u) * (s * t + 1) * (s * u + 1),
        16 * r * (t + u) * (s * t - 1) * (s * u - 1),
    ]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(compression, expected_compression)
    )
    assert sp.factor(C.det()) == -64 * r * s * (t + u) ** 2

    # Every full cofactor is divisible by t+u.  On r*s!=0 compression
    # therefore forces t+u=0; otherwise the first two factors would force
    # {rt,ru}={-1,+1}, which itself gives t+u=0.
    full_three = minors(C, 3)
    assert all(
        sp.div(sp.Poly(value, t, u, r, s), sp.Poly(t + u, t, u, r, s))[1].is_zero
        for value in full_three
    )

    opposite = sp.simplify(C.subs(u, -t))
    opposite_first_two = minors(opposite[:, :3], 2)
    seam_minors = (
        4 * (s * t - 1) * (s * t + 1),
        4 * (r**2 * s**2 * t**4 + 2 * s**2 * t**2 - 3),
    )
    assert all(sp.factor(value) in opposite_first_two for value in seam_minors)

    # If r=0, compression again gives u=-t, but the two displayed minors
    # below demand (st)^2=1 and (st)^2=3/2 simultaneously.
    rzero_first_two = minors(C.subs({r: 0, u: -t})[:, :3], 2)
    rzero_incompatible = (
        -4 * (1 - s**2 * t**2),
        -4 * (3 - 2 * s**2 * t**2),
    )
    assert all(sp.factor(value) in rzero_first_two for value in rzero_incompatible)
    # If s=0, the escaping coefficient is identically zero.
    assert C[:, 3].subs(s, 0) == sp.zeros(4, 1)

    # The only finite pure seam after scaling D has rt,st in {+/-1}.
    # It is genuinely pure, but its two noncentral planes have pair rank 2.
    pure_points = {}
    expected_C = sp.Matrix(((8, 4, 2, 0), (8, 4, 2, 0), (8, 4, 2, 2), (8, 4, 2, 2)))
    for epsilon in (-1, 1):
        for eta in (-1, 1):
            substitution = {r: epsilon, s: eta, t: 1, u: -1}
            specialized_C = C.subs(substitution)
            assert specialized_C == expected_C
            specialized_pair = pair_matrix(
                y2.subs(substitution),
                x2.subs(substitution),
                y3.subs(substitution),
                x3.subs(substitution),
            )
            assert all(value == 0 for value in minors(specialized_pair, 3))
            assert any(value != 0 for value in minors(specialized_pair, 2))
            pure_points[f"({epsilon},{eta})"] = {
                "compressed_rank": 1,
                "full_rank": 2,
                "noncentral_pair_rank": 2,
            }

    # Projective endpoint D is a valid plane only for r*s!=0.  With one
    # endpoint, full rank is <=2 but the compressed span cannot be a line;
    # with two endpoints the same failure is immediate.
    C_infinity = coefficient_matrix(y, x22, dy, dx, y + u * dy, x22 + u * dx)
    assert all(value == 0 for value in minors(C_infinity, 3))
    infinity_first_two = minors(C_infinity[:, :3], 2)
    infinity_incompatible = (8 * r**2 * s * u, 4 * r * s * (r * s * u**2 - 1))
    assert all(sp.factor(value) in infinity_first_two for value in infinity_incompatible)

    C_double = coefficient_matrix(y, x22, dy, dx, dy, dx)
    assert all(value == 0 for value in minors(C_double, 3))
    assert 4 * r**2 * s**2 in minors(C_double[:, :3], 2)

    result = {
        "full_kernel_collision_types": ["2+1+1", "3+1", "2+2"],
        "2+1+1_and_3+1": "projective synchronizer point has local rank one; finite active cube is zero",
        "2+2_geometry": "projective synchronizer plane with radical A; flat triples are lines through A",
        "2+2_finite_pure_seam": pure_points,
        "2+2_projective_endpoints": "empty",
        "triangle_conclusion": "every finite pure seam has a rank-two noncentral pair",
        "combined_conclusion": "with the distinct-ratio theorems, the full-kernel-support flat rank-three triangle is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
