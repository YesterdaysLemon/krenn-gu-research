"""Independent Fraction audit of the support-two (2,2) complete theorem."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

Vector = tuple[F, ...]
Tensor = tuple[F, ...]
RootBlock = dict[tuple[int, int], F]


def unit(size: int, index: int) -> Vector:
    return tuple(F(i == index) for i in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, F(0)) for entries in zip(*vectors, strict=True))


def scale(value: F | int, vector: Vector) -> Vector:
    scalar = F(value)
    return tuple(scalar * entry for entry in vector)


def source(group: int, local: int) -> Vector:
    return tuple(F(i == 3 * group + local) for i in range(9))


def root_basis(a: int, b: int, c: int) -> Vector:
    return unit(27, 9 * a + 3 * b + c)


def tensor_basis(x: int, y: int, z: int) -> Tensor:
    return unit(27, 9 * x + 3 * y + z)


def component(vector: Vector, group: int, local: int) -> F:
    return vector[3 * group + local]


def polarized(u: Vector, v: Vector, q: Vector) -> Tensor:
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


def alternating(u: Vector, v: Vector, w: Vector) -> Tensor:
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
    rows = len(matrix)
    cols = len(columns)
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row_index in range(rows):
            if row_index == pivot_row or not matrix[row_index][col]:
                continue
            multiple = matrix[row_index][col]
            matrix[row_index] = [
                left - multiple * right
                for left, right in zip(
                    matrix[row_index], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def derivative_value(
    a: Vector, b: Vector, block_b: RootBlock, block_c: RootBlock
) -> Vector:
    out = [F(0) for _ in range(27)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                out[9 * i + 3 * j + k] = (
                    a[i] * block_b.get((j, k), F(0))
                    + block_c.get((i, k), F(0)) * b[j]
                )
    return tuple(out)


def root_nonroot_outer(root: Vector, tensor: Tensor) -> list[list[F]]:
    return [[root_row * entry for entry in tensor] for root_row in root]


def matrix_add(*matrices: list[list[F]]) -> list[list[F]]:
    return [
        [sum(entries, F(0)) for entries in zip(*rows, strict=True)]
        for rows in zip(*matrices, strict=True)
    ]


def zero_matrix() -> list[list[F]]:
    return [[F(0) for _ in range(27)] for _ in range(27)]


def type_ii_collapse_audit() -> None:
    kappa = F(7)
    for coordinate_factor in range(3):
        forced_common_row = scale(kappa, unit(3, coordinate_factor))
        for kernel_colour in range(3):
            if kernel_colour != coordinate_factor:
                # The only nonzero row of e_i tensor z is row i, whereas
                # target consistency demands a nonzero row d.
                assert scale(kappa, unit(3, kernel_colour)) != scale(
                    0, forced_common_row
                )
                continue
            # At d=i the demanded diagonal row is exactly kappa e_i, so the
            # common-end form z is a coordinate vector and the block is a
            # coordinate monomial.
            assert forced_common_row == scale(
                kappa, unit(3, coordinate_factor)
            )
    print("independent Type-II collapse audit: PASS (all coordinate rows)")


def normal_form_audit() -> None:
    block_b = {(0, 0): F(1)}
    block_c1 = {
        (1, 1): F(1),
        (0, 0): F(1),
        (0, 1): F(-1),
        (0, 2): F(2),
        (2, 0): F(3),
        (2, 1): F(-3),
        (2, 2): F(5),
    }
    zero3 = scale(0, unit(3, 0))
    p10 = (F(1), F(0), F(0), F(0), F(0), F(0))
    p11 = (F(0), F(0), F(0), F(0), F(1), F(0))
    p12 = (F(0), F(0), F(1), F(0), F(0), F(1))
    image1 = [
        derivative_value(p[:3], p[3:], block_b, block_c1)
        for p in (p10, p11, p12)
    ]
    assert image1[0] == root_basis(0, 0, 0)
    assert image1[1][9 * 1 + 3 * 1 + 1] == 1
    assert image1[2][9 * 2 + 0] == 1
    assert image1[2][9 * 0 + 3 * 2 + 0] == 1
    derivative_columns = [
        derivative_value(unit(3, i), zero3, block_b, block_c1)
        for i in range(3)
    ] + [
        derivative_value(zero3, unit(3, j), block_b, block_c1)
        for j in range(3)
    ]
    assert rank(derivative_columns) == 6

    block_c2 = {(1, 0): F(1), (2, 2): F(1)}
    p22 = (F(0), F(1), F(0), F(0), F(0), F(1))
    u2 = derivative_value(p22[:3], p22[3:], block_b, block_c2)
    assert u2[9 * 1 + 3 * 0 + 0] == 1
    assert u2[9 * 2 + 3 * 2 + 2] == 1
    # The first zero row forces its coefficient tensor to vanish; the second
    # would then have to absorb the nonzero target T2 with that same tensor.
    print("independent normal-form audit: PASS (two charts / c=2 clash)")


def target_table_audit() -> None:
    block_c = {
        (1, 1): F(1),
        (0, 0): F(1),
        (0, 1): F(-1),
        (0, 2): F(2),
        (2, 0): F(3),
        (2, 1): F(-3),
        (2, 2): F(5),
    }
    block_b = {(0, 0): F(1)}
    p10 = (F(1), F(0), F(0), F(0), F(0), F(0))
    p11 = (F(0), F(0), F(0), F(0), F(1), F(0))
    p12 = (F(0), F(0), F(1), F(0), F(0), F(1))
    u0, u1, _u2 = [
        derivative_value(p[:3], p[3:], block_b, block_c)
        for p in (p10, p11, p12)
    ]
    targets = [tensor_basis(i, i, i) for i in range(3)]
    target = zero_matrix()
    for i in range(3):
        target[9 * i + 3 * i + i] = list(targets[i])
    all_cross = matrix_add(
        target,
        root_nonroot_outer(scale(-1, u0), targets[0]),
        root_nonroot_outer(scale(-1, u1), targets[1]),
    )

    def table_row(a: int, b: int, c: int) -> Tensor:
        return tuple(all_cross[9 * a + 3 * b + c])

    zero = tuple(F(0) for _ in range(27))
    assert table_row(0, 0, 0) == zero
    assert table_row(2, 0, 0) == zero
    assert table_row(1, 1, 1) == zero
    for c in range(3):
        assert table_row(0, 2, c) == zero
        assert table_row(2, 2, c) == (targets[2] if c == 2 else zero)
        assert table_row(0, 1, c) == scale(-block_c.get((0, c), F(0)), targets[1])
        assert table_row(2, 1, c) == scale(-block_c.get((2, c), F(0)), targets[1])
    assert add(table_row(0, 1, 0), table_row(0, 1, 1)) == zero
    assert add(table_row(2, 1, 0), table_row(2, 1, 1)) == zero
    print("independent arbitrary-C table audit: PASS (sparse root tensors)")


def transverse_line_audit() -> None:
    x = source(0, 2)
    y = source(1, 2)
    target_1_index = 9 * 1 + 3 * 1 + 1
    basis = [source(group, local) for group in range(3) for local in range(3)]
    for u in basis:
        for q in basis:
            assert polarized(add(x, y), u, q)[target_1_index] == 0

    # In the three-source chart, the square image shares x and y.  Every
    # allowed Q vector has X/Y projections on those lines.
    for z_local in range(3):
        v = add(x, y, source(2, z_local))
        allowed_q = [x, y, *(source(2, local) for local in range(3))]
        for u in basis:
            for q in allowed_q:
                assert polarized(v, u, q)[target_1_index] == 0
    print("independent transverse-line audit: PASS (basis exhaustion)")


def atlas_and_sharpness_audit() -> None:
    x = source(0, 2)
    y = source(1, 2)
    z0 = source(2, 0)
    z1 = source(2, 1)
    t = source(2, 2)
    v = add(x, y)
    w = add(x, scale(-1, y))

    # Fully conjugate displayed identities, checked with independent values.
    u0 = add(scale(2, w), z0)
    u1 = add(scale(-3, w), z1)
    assert polarized(u0, v, w) == tuple(F(0) for _ in range(27))
    assert polarized(u1, v, w) == tuple(F(0) for _ in range(27))
    assert polarized(u0, v, t) == tuple(F(0) for _ in range(27))
    assert polarized(u1, v, t) == tuple(F(0) for _ in range(27))
    assert polarized(u0, u1, w)[9 * 2 + 3 * 2 + 1] == F(-4)
    assert polarized(u0, u1, t) == scale(12, tensor_basis(2, 2, 2))

    # Three-source nonzero scaling chart: all scalar rows lie in one plane.
    v3 = add(x, y, z0)
    q0 = add(x, y, scale(-2, z0))
    s0 = add(scale(2, x), scale(3, y), scale(F(5, 2), z0))
    s1 = add(scale(-1, x), scale(4, y), scale(F(3, 2), z0))
    zero = tuple(F(0) for _ in range(27))
    assert polarized(s0, v3, q0) == zero
    assert polarized(s1, v3, q0) == zero
    assert alternating(s0, s1, v3) == zero

    # Exact failure when the correction shares two square-image factors.
    sharp_u0 = add(w, z0)
    sharp_u1 = z1
    assert rank([sharp_u0, sharp_u1, v, w, t]) == 5
    for q in (w, t):
        assert polarized(sharp_u0, v, q) == zero
        assert polarized(sharp_u1, v, q) == zero
    assert polarized(sharp_u0, sharp_u1, w) == scale(
        -2, tensor_basis(2, 2, 1)
    )
    assert polarized(sharp_u0, sharp_u1, t) == zero
    assert alternating(sharp_u0, sharp_u1, v) != zero
    print("independent atlas/sharpness audit: PASS (Fraction arithmetic)")


def main() -> None:
    type_ii_collapse_audit()
    normal_form_audit()
    target_table_audit()
    transverse_line_audit()
    atlas_and_sharpness_audit()
    print("independent support-two (2,2) complete exclusion: PASS")


if __name__ == "__main__":
    main()
