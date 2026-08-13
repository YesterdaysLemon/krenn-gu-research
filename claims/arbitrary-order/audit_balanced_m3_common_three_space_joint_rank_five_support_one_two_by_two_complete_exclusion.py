"""Independent no-import audit of the support-one (2,2) exclusion.

This file imports no repository module and no third-party package.  It uses
standard-library Fraction arithmetic, flat sparse tensors, numeric arbitrary
blocks, and a coordinate convention separate from the SymPy verifier.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

Vector = tuple[F, ...]


def unit(size: int, index: int) -> Vector:
    return tuple(F(position == index) for position in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, F(0)) for entries in zip(*vectors, strict=True))


def scale(value: F | int, vector: Vector) -> Vector:
    scalar = F(value)
    return tuple(scalar * entry for entry in vector)


def join(left: Vector, right: Vector) -> Vector:
    return (*left, *right)


def source(group: int, local: int) -> Vector:
    return unit(9, 3 * group + local)


def tensor_basis(x: int, y: int, z: int) -> Vector:
    return unit(27, 9 * x + 3 * y + z)


def component(vector: Vector, group: int, local: int) -> F:
    return vector[3 * group + local]


def polarized(u: Vector, v: Vector, q: Vector) -> Vector:
    forms = (u, v, q)
    out = [F(0) for _ in range(27)]
    for sigma in permutations(range(3)):
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    out[9 * x + 3 * y + z] += (
                        component(forms[sigma[0]], 0, x)
                        * component(forms[sigma[1]], 1, y)
                        * component(forms[sigma[2]], 2, z)
                    )
    return tuple(out)


def alternating(u: Vector, v: Vector, w: Vector) -> Vector:
    forms = (u, v, w)
    out = [F(0) for _ in range(27)]
    for sigma in permutations(range(3)):
        inversions = sum(
            sigma[i] > sigma[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        sign = F(-1 if inversions % 2 else 1)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    out[9 * x + 3 * y + z] += sign * (
                        component(forms[sigma[0]], 0, x)
                        * component(forms[sigma[1]], 1, y)
                        * component(forms[sigma[2]], 2, z)
                    )
    return tuple(out)


def rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    row_count = len(matrix)
    column_count = len(columns)
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def target_fibre(
    a: int,
    shore_b: int,
    k: int,
    c: int,
    d: int,
    block_b: list[list[F]],
    block_c: list[list[F]],
    kappa: F,
    kappa_prime: F,
) -> Vector:
    value = (
        unit(3, k)
        if a == shore_b == k
        else scale(0, unit(3, 0))
    )
    if a == d:
        value = add(
            value,
            scale(-block_b[shore_b][k] / kappa, unit(3, d)),
        )
    if shore_b == c:
        value = add(
            value,
            scale(-block_c[a][k] / kappa_prime, unit(3, c)),
        )
    return value


def zero_row_normal_form_audit() -> None:
    kappa, kappa_prime, tau = F(5), F(7), F(11)
    zero = unit(3, 0)
    zero = scale(0, zero)

    for c in range(3):
        forbidden = scale(-1 / kappa, unit(3, c))
        assert forbidden[c] != 0

    for c in range(3):
        for d in range(3):
            if c == d:
                continue
            j = next(index for index in range(3) if index not in (c, d))
            plane = [
                join(unit(3, d), zero),
                join(zero, unit(3, c)),
                join(unit(3, j), scale(tau, unit(3, j))),
            ]
            assert rank(plane) == 3
            assert rank([vector[:3] for vector in plane]) == 2
            assert rank([vector[3:] for vector in plane]) == 2
            assert all(vector[c] == 0 for vector in plane)
            assert all(vector[3 + d] == 0 for vector in plane)

            corrections = {
                target: join(
                    (
                        scale(-1 / kappa, unit(3, d))
                        if target == d
                        else zero
                    ),
                    (
                        scale(-1 / kappa_prime, unit(3, c))
                        if target == c
                        else zero
                    ),
                )
                for target in range(3)
            }
            assert rank(plane + [corrections[d]]) == 3
            assert rank(plane + [corrections[c]]) == 3
            assert corrections[j] == join(zero, zero)

            # Root-row coefficient triples are evaluations on plane columns.
            rows_r = [tuple(column[a] for column in plane) for a in range(3)]
            rows_p = [
                tuple(column[3 + b] for column in plane) for b in range(3)
            ]
            assert rows_r[d] == (F(1), F(0), F(0))
            assert rows_r[c] == (F(0), F(0), F(0))
            assert rows_r[j] == (F(0), F(0), F(1))
            assert rows_p[d] == (F(0), F(0), F(0))
            assert rows_p[c] == (F(0), F(1), F(0))
            assert rows_p[j] == (F(0), F(0), tau)

    print("independent zero-row normal form: PASS (Fraction / all colours)")


def support_and_target_table_audit() -> None:
    kappa, kappa_prime = F(5), F(7)
    survivors = {
        (c, d)
        for c in range(3)
        for d in range(3)
        if c != d and 2 in (c, d)
    }
    assert survivors == {(0, 2), (1, 2), (2, 0), (2, 1)}

    base_b = (
        (F(2), F(-1), F(4)),
        (F(3), F(6), F(-2)),
        (F(8), F(9), F(10)),
    )
    base_c = (
        (F(-3), F(8), F(2)),
        (F(9), F(-4), F(6)),
        (F(1), F(5), F(-7)),
    )

    for c in (0, 1):
        d = 2
        j = 1 - c
        block_b = [list(row) for row in base_b]
        block_c = [list(row) for row in base_c]
        block_b[d] = [kappa * F(k == d) for k in range(3)]
        block_c[c] = [kappa_prime * F(k == c) for k in range(3)]

        for k in range(3):
            square = target_fibre(
                j, j, k, c, d, block_b, block_c, kappa, kappa_prime
            )
            mixed_dj = target_fibre(
                d, j, k, c, d, block_b, block_c, kappa, kappa_prime
            )
            mixed_jc = target_fibre(
                j, c, k, c, d, block_b, block_c, kappa, kappa_prime
            )
            mixed_dc = target_fibre(
                d, c, k, c, d, block_b, block_c, kappa, kappa_prime
            )
            assert square == (
                unit(3, j) if k == j else scale(0, unit(3, 0))
            )
            assert mixed_dj == scale(
                -block_b[j][k] / kappa, unit(3, d)
            )
            assert mixed_jc == scale(
                -block_c[j][k] / kappa_prime, unit(3, c)
            )
            assert mixed_dc == add(
                scale(-block_b[c][k] / kappa, unit(3, d)),
                scale(-block_c[d][k] / kappa_prime, unit(3, c)),
            )
            for mixed in (mixed_dj, mixed_jc, mixed_dc):
                assert mixed[j] == 0

    print("independent support/target table: PASS (numeric arbitrary blocks)")


def diagonal_plane_and_atlas_audit() -> None:
    target_plane = [
        tensor_basis(0, 0, 0),
        tensor_basis(1, 1, 1),
    ]
    structural = [
        tensor_basis(2, y, z) for y in range(3) for z in range(3)
    ] + [tensor_basis(x, 2, z) for x in range(3) for z in range(3)]
    fixed_pair = [tensor_basis(2, 2, z) for z in range(3)]
    assert rank(structural) == 15
    assert rank(structural + target_plane) == 17
    assert rank(fixed_pair + target_plane) == 5

    x = source(0, 2)
    y = source(1, 2)
    z0 = source(2, 0)
    z1 = source(2, 1)
    t = source(2, 2)
    v = add(x, y)
    w = add(x, scale(-1, y))
    zero = scale(0, tensor_basis(0, 0, 0))

    # Fully conjugate two-source chart, through a separate numeric fixture.
    u0 = add(scale(2, w), z0)
    u1 = add(scale(-3, w), z1)
    for q in (w, t):
        assert polarized(u0, v, q) == zero
        assert polarized(u1, v, q) == zero
    assert polarized(u0, u1, w) == add(
        scale(-4, tensor_basis(2, 2, 1)),
        scale(6, tensor_basis(2, 2, 0)),
    )
    assert polarized(u0, u1, t) == scale(12, tensor_basis(2, 2, 2))
    assert alternating(u0, u1, v) == add(
        scale(-4, tensor_basis(2, 2, 1)),
        scale(-6, tensor_basis(2, 2, 0)),
    )

    # Nonzero three-source scaling chart has zero alternating determinant.
    v3 = add(x, y, z0)
    q0 = add(x, y, scale(-2, z0))
    s0 = add(scale(2, x), scale(3, y), scale(F(5, 2), z0))
    s1 = add(scale(-1, x), scale(4, y), scale(F(3, 2), z0))
    assert polarized(s0, v3, q0) == zero
    assert polarized(s1, v3, q0) == zero
    assert alternating(s0, s1, v3) == zero

    # The row-basis alternating tensor itself has nonzero scale.
    basis_alt = alternating(source(0, 0), source(1, 1), source(2, 2))
    assert basis_alt == tensor_basis(0, 1, 2)
    print("independent diagonal-plane atlas: PASS (sparse tensor route)")


def main() -> None:
    zero_row_normal_form_audit()
    support_and_target_table_audit()
    diagonal_plane_and_atlas_audit()
    print("independent support-one (2,2) complete exclusion: PASS")


if __name__ == "__main__":
    main()
