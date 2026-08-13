"""Independent Fraction audit of the support-two (3,3) exclusion.

This file imports no repository module and no third-party package.  It uses a
separate flat-tuple representation for the graph, root table, polarized
products, transverse planes, and common-zero identities.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

Vector = tuple[F, ...]
Matrix = tuple[Vector, ...]


def unit(size: int, index: int) -> Vector:
    return tuple(F(i == index) for i in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, F(0)) for entries in zip(*vectors, strict=True))


def scale(value: F | int, vector: Vector) -> Vector:
    scalar = F(value)
    return tuple(scalar * entry for entry in vector)


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum((entry * coordinate for entry, coordinate in zip(row, vector, strict=True)), F(0))
        for row in matrix
    )


def source(group: int, local: int) -> Vector:
    return tuple(F(i == 3 * group + local) for i in range(9))


def pair(left: Vector, right: Vector) -> Vector:
    return tuple(x * y for x in left for y in right)


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


def graph_and_correction_audit() -> None:
    eta0, eta1 = F(2), F(3)
    beta, chi = F(5), F(7)
    alpha, nu, ell = F(11), F(13), F(17)
    graph: Matrix = (
        (F(0), -beta / chi, F(0)),
        (alpha, nu / chi, F(0)),
        (F(0), F(0), ell),
    )
    basis = [unit(3, i) for i in range(3)]

    def contracted(a: Vector) -> Vector:
        return add(
            scale(beta, pair(a, basis[0])),
            scale(chi, pair(basis[1], mat_vec(graph, a))),
        )

    assert contracted(basis[1]) == scale(nu, pair(basis[1], basis[1]))
    preimage_0 = add(basis[0], scale(-alpha * chi / nu, basis[1]))
    assert contracted(preimage_0) == scale(beta, pair(basis[0], basis[0]))

    corrections: Matrix = (
        (-eta0 / beta, F(0), F(0)),
        (chi * alpha * eta0 / (beta * nu), -eta1 / nu, F(0)),
        (F(0), F(0), F(0)),
    )
    for a in range(3):
        for b in range(3):
            left = (
                -eta0 * F(a == b == 0),
                -eta1 * F(a == b == 1),
                F(0),
            )
            right = scale(beta * F(b == 0), corrections[a])
            if a == 1:
                right = add(
                    right,
                    *(
                        scale(chi * graph[b][i], corrections[i])
                        for i in range(3)
                    ),
                )
            assert left == right
    assert all(row[2] == 0 for row in corrections)
    print("independent graph/correction audit: PASS (Fraction arithmetic)")


def permanent_symmetry_audit() -> None:
    beta, chi = F(5), F(7)
    alpha, nu, ell = F(11), F(13), F(17)
    l02, l12 = F(19), F(23)
    trial: Matrix = (
        (F(0), -beta / chi, l02),
        (alpha, nu / chi, l12),
        (F(0), F(0), ell),
    )
    # L E22 has only its third column.  Its (0,2) and (1,2) skew
    # entries are exactly the two provisional third-column coefficients.
    assert trial[0][2] == l02
    assert trial[1][2] == l12
    fixed: Matrix = (
        (F(0), -beta / chi, F(0)),
        (alpha, nu / chi, F(0)),
        (F(0), F(0), ell),
    )
    product = tuple(
        tuple(fixed[i][2] * F(j == 2) for j in range(3))
        for i in range(3)
    )
    assert product == tuple(
        tuple(product[j][i] for j in range(3)) for i in range(3)
    )
    assert mat_vec(fixed, unit(3, 2)) == scale(ell, unit(3, 2))
    print("independent permanent-symmetry audit: PASS (third column fixed)")


def target_plane_table_audit() -> None:
    eta0, eta1 = F(2), F(3)
    beta, chi = F(5), F(7)
    alpha, nu, ell = F(11), F(13), F(17)
    graph: Matrix = (
        (F(0), -beta / chi, F(0)),
        (alpha, nu / chi, F(0)),
        (F(0), F(0), ell),
    )
    corrections: Matrix = (
        (-eta0 / beta, F(0), F(0)),
        (chi * alpha * eta0 / (beta * nu), -eta1 / nu, F(0)),
        (F(0), F(0), F(0)),
    )
    block_b: Matrix = (
        (F(2), F(-1), F(4)),
        (F(3), F(5), F(-2)),
        (F(7), F(6), F(1)),
    )
    block_c: Matrix = (
        (F(-3), F(8), F(2)),
        (F(9), F(-4), F(5)),
        (F(6), F(1), F(-7)),
    )

    def fibre(a: int, b: int, c: int) -> Vector:
        value = (
            F(a == b == c == 0),
            F(a == b == c == 1),
            F(a == b == c == 2),
        )
        for i in range(3):
            singleton = (
                F(a == i) * block_b[b][c] + block_c[a][c] * graph[b][i]
            )
            value = add(value, scale(singleton, corrections[i]))
        return value

    for c in range(3):
        assert fibre(2, 2, c) == (F(0), F(0), F(c == 2))
        for a in (0, 1):
            assert fibre(a, 2, c)[2] == 0
        assert fibre(0, 0, c)[2] == 0
    print("independent target-plane table audit: PASS (arbitrary blocks)")


def transverse_plane_audit() -> None:
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
    assert rank(fixed_pair) == 3
    assert rank(fixed_pair + target_plane) == 5

    x = source(0, 2)
    y = source(1, 2)
    basis = [source(group, local) for group in range(3) for local in range(3)]
    for u in basis:
        for q in basis:
            value = polarized(add(x, y), u, q)
            assert rank(structural + [value]) == rank(structural)

    # In the three-source square chart every allowed Q vector has its
    # X/Y projections on the two base lines.
    for z_local in range(3):
        v = add(x, y, source(2, z_local))
        allowed_q = [x, y, *(source(2, local) for local in range(3))]
        for u in basis:
            for q in allowed_q:
                value = polarized(v, u, q)
                assert rank(structural + [value]) == rank(structural)
    print("independent transverse-plane audit: PASS (basis exhaustion)")


def atlas_and_sharpness_audit() -> None:
    x = source(0, 2)
    y = source(1, 2)
    z0 = source(2, 0)
    z1 = source(2, 1)
    t = source(2, 2)
    v = add(x, y)
    w = add(x, scale(-1, y))
    zero = tuple(F(0) for _ in range(27))

    # Fully conjugate displayed identities.
    u0 = add(scale(2, w), z0)
    u1 = add(scale(-3, w), z1)
    assert polarized(u0, v, w) == zero
    assert polarized(u1, v, w) == zero
    assert polarized(u0, v, t) == zero
    assert polarized(u1, v, t) == zero
    assert polarized(u0, u1, w) == add(
        scale(-4, tensor_basis(2, 2, 1)),
        scale(6, tensor_basis(2, 2, 0)),
    )
    assert polarized(u0, u1, t) == scale(12, tensor_basis(2, 2, 2))
    assert alternating(u0, u1, v) == add(
        scale(-4, tensor_basis(2, 2, 1)),
        scale(-6, tensor_basis(2, 2, 0)),
    )

    # Three-source nonzero scaling chart.
    v3 = add(x, y, z0)
    q0 = add(x, y, scale(-2, z0))
    s0 = add(scale(2, x), scale(3, y), scale(F(5, 2), z0))
    s1 = add(scale(-1, x), scale(4, y), scale(F(3, 2), z0))
    assert polarized(s0, v3, q0) == zero
    assert polarized(s1, v3, q0) == zero
    assert alternating(s0, s1, v3) == zero

    # Exact control outside D01: the mutual correction shares the first two
    # factor lines of T2, and the alternating tensor can remain nonzero.
    sharp_u0 = add(w, z0)
    sharp_u1 = z1
    assert rank([sharp_u0, sharp_u1, v, w, t]) == 5
    for q in (w, t):
        assert polarized(sharp_u0, v, q) == zero
        assert polarized(sharp_u1, v, q) == zero
    shared = scale(-2, tensor_basis(2, 2, 1))
    assert polarized(sharp_u0, sharp_u1, w) == shared
    assert polarized(sharp_u0, sharp_u1, t) == zero
    assert alternating(sharp_u0, sharp_u1, v) != zero
    assert rank(
        [tensor_basis(0, 0, 0), tensor_basis(1, 1, 1), shared]
    ) == 3
    print("independent atlas/sharpness audit: PASS (separate tensor route)")


def main() -> None:
    graph_and_correction_audit()
    permanent_symmetry_audit()
    target_plane_table_audit()
    transverse_plane_audit()
    atlas_and_sharpness_audit()
    print("independent support-two (3,3) exclusion: PASS")


if __name__ == "__main__":
    main()
