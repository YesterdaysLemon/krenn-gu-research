#!/usr/bin/env python3
"""Independent no-import audit for the S2BV nonaligned pair-pole exclusion."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations, product

WIDTH = 3
D_COLOUR, S_COLOUR, T_COLOUR = range(WIDTH)


def unit(length: int, index: int) -> tuple[F, ...]:
    return tuple(F(i == index) for i in range(length))


def basis(block: int, coordinate: int) -> tuple[F, ...]:
    return unit(3 * WIDTH, WIDTH * block + coordinate)


def add(*vectors: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(value[i] for value in vectors) for i in range(len(vectors[0])))


def scale(scalar: F, vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(scalar * value for value in vector)


def split(v: tuple[F, ...], width: int = WIDTH) -> tuple[tuple[F, ...], ...]:
    return tuple(v[i * width : (i + 1) * width] for i in range(3))


def tensor(
    a: tuple[F, ...], b: tuple[F, ...], c: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    width = len(a)
    return {
        (i, j, k): value
        for i, j, k in product(range(width), repeat=3)
        if (value := a[i] * b[j] * c[k])
    }


def tensor_add(
    *values: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int, int], F]:
    keys = set().union(*(value.keys() for value in values))
    return {
        key: total
        for key in keys
        if (total := sum(value.get(key, F(0)) for value in values))
    }


def tensor_scale(
    scalar: F, value: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int, int], F]:
    return {key: scalar * item for key, item in value.items() if scalar * item}


def permanent(
    u: tuple[F, ...], v: tuple[F, ...], z: tuple[F, ...]
) -> dict[tuple[int, int, int], F]:
    roots = [split(value) for value in (u, v, z)]
    return tensor_add(
        *(
            tensor(
                roots[sigma[0]][0], roots[sigma[1]][1], roots[sigma[2]][2]
            )
            for sigma in permutations(range(3))
        )
    )


def rank(rows: list[list[F]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for col in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][col]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][col]:
                continue
            multiple = matrix[row][col]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def column_rank(columns: list[list[F]]) -> int:
    return rank([list(row) for row in zip(*columns, strict=True)])


def audit_source_forks() -> None:
    x, y, z = basis(0, T_COLOUR), basis(1, T_COLOUR), basis(2, T_COLOUR)
    alpha, beta = F(2), F(-3)
    shear = -alpha - beta
    v = add(x, y)
    u = add(scale(alpha, x), scale(beta, y), z)
    h = add(u, scale(shear, v))
    q = scale(F(5), add(x, scale(-F(1), y)))
    assert permanent(h, u, v) == {}
    assert permanent(q, v, v) == {}
    assert permanent(h, q, v) == {}

    v3 = add(x, y, z)
    pure = basis(0, T_COLOUR)
    q3 = add(y, scale(-F(1), z))
    r3 = basis(0, D_COLOUR)
    assert permanent(q3, v3, v3) == {}
    assert permanent(pure, q3, v3) == {}
    assert permanent(v3, pure, r3) == {}
    assert permanent(pure, q3, r3) == {}


def canonical_rows() -> tuple[list[tuple[F, ...]], dict[str, tuple[F, ...] | F]]:
    x = basis(0, T_COLOUR)
    y = basis(1, T_COLOUR)
    zd, zs, zt = (basis(2, colour) for colour in range(WIDTH))
    b, mu = F(3), F(2)
    c = add(zd, scale(F(2), zs), scale(F(3), zt))
    r = add(scale(F(2), zd), scale(-F(1), zs), zt)
    u = scale(F(1, 2), zt)
    q = scale(mu, add(x, scale(-F(1), y)))
    v = add(x, y, c)
    return [u, r, add(scale(b, u), scale(-F(1), q)), v], {
        "x": x,
        "y": y,
        "zt": zt,
        "b": b,
        "mu": mu,
        "c": c,
        "r": r,
        "q": q,
    }


def audit_exact_control() -> None:
    rows, data = canonical_rows()
    g0, g1, g2, g3 = rows
    b = data["b"]
    assert isinstance(b, F)
    q = data["q"]
    assert isinstance(q, tuple)
    assert column_rank([list(value) for value in rows]) == 4

    r_s, r_t = g0, g3
    p_s, p_t = add(scale(b, g0), scale(-F(1), g2)), g0
    q_d, q_t = g1, g3
    assert p_s == q
    coefficients = {
        (S_COLOUR, S_COLOUR, D_COLOUR): permanent(r_s, p_s, q_d),
        (S_COLOUR, T_COLOUR, D_COLOUR): permanent(r_s, p_t, q_d),
        (T_COLOUR, S_COLOUR, D_COLOUR): permanent(r_t, p_s, q_d),
        (T_COLOUR, T_COLOUR, D_COLOUR): permanent(r_t, p_t, q_d),
        (S_COLOUR, S_COLOUR, T_COLOUR): permanent(r_s, p_s, q_t),
        (S_COLOUR, T_COLOUR, T_COLOUR): permanent(r_s, p_t, q_t),
        (T_COLOUR, S_COLOUR, T_COLOUR): permanent(r_t, p_s, q_t),
        (T_COLOUR, T_COLOUR, T_COLOUR): permanent(r_t, p_t, q_t),
    }
    target_t = tensor(
        unit(WIDTH, T_COLOUR), unit(WIDTH, T_COLOUR), unit(WIDTH, T_COLOUR)
    )
    for root, value in coefficients.items():
        assert value == (target_t if root == (T_COLOUR,) * 3 else {})


MONOMIAL_WIDTH = 9
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, F]


def poly_var(index: int) -> Polynomial:
    exponent = [0] * MONOMIAL_WIDTH
    exponent[index] = 1
    return {tuple(exponent): F(1)}


def poly_add(*values: Polynomial) -> Polynomial:
    keys = set().union(*(value.keys() for value in values))
    return {
        key: total
        for key in keys
        if (total := sum(value.get(key, F(0)) for value in values))
    }


def poly_scale(scalar: F, value: Polynomial) -> Polynomial:
    return {key: scalar * item for key, item in value.items() if scalar * item}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for first, a in left.items():
        for second, b in right.items():
            key = tuple(x + y for x, y in zip(first, second, strict=True))
            out[key] = out.get(key, F(0)) + a * b
    return {key: value for key, value in out.items() if value}


def audit_pair_residues() -> None:
    xd, xs, xt, yd, ys, yt, zd, zs, zt = (poly_var(i) for i in range(9))
    b, mu = F(3), F(2)
    c = poly_add(zd, poly_scale(F(2), zs), poly_scale(F(3), zt))
    r = poly_add(poly_scale(F(2), zd), poly_scale(-F(1), zs), zt)
    ell = poly_scale(b * F(1, 2), zt)
    target_d = poly_mul(poly_mul(xd, yd), zd)
    target_s = poly_mul(poly_mul(xs, ys), zs)

    numerator_x = poly_add(
        poly_scale(-F(1), poly_mul(r, target_s)),
        poly_mul(poly_add(ell, poly_scale(-mu, c)), target_d),
    )
    numerator_y = poly_add(
        poly_mul(r, target_s),
        poly_scale(-F(1), poly_mul(poly_add(ell, poly_scale(mu, c)), target_d)),
    )
    assert all(exponent[2] == 0 for exponent in numerator_x)
    assert all(exponent[5] == 0 for exponent in numerator_y)
    assert poly_add(numerator_x, numerator_y) == poly_scale(
        -2 * mu, poly_mul(c, target_d)
    )

    zero_c_x = poly_add(
        poly_scale(-F(1), poly_mul(r, target_s)), poly_mul(ell, target_d)
    )
    assert zero_c_x
    assert any(exponent[1] and exponent[4] for exponent in zero_c_x)
    assert any(exponent[0] and exponent[3] for exponent in zero_c_x)

    determinant = poly_scale(-2 * mu, poly_mul(poly_mul(xt, yt), r))
    assert determinant

    # Cross-multiplied verification of the two nontrivial singleton equations.
    assert poly_add(
        poly_scale(-F(1), numerator_x),
        numerator_y,
        poly_scale(F(2), poly_mul(ell, target_d)),
        poly_scale(-F(2), poly_mul(r, target_s)),
    ) == {}
    assert poly_add(
        numerator_x,
        numerator_y,
        poly_scale(2 * mu, poly_mul(c, target_d)),
    ) == {}


def main() -> None:
    audit_source_forks()
    audit_exact_control()
    audit_pair_residues()
    print(
        "S2BV independent audit passed: source forks, reverse-indexed exact "
        "control, sparse-polynomial pair lift, and incompatible divisor residues."
    )


if __name__ == "__main__":
    main()
