"""Independent no-import audit of the support-one higher-row exclusion.

This script uses only standard-library Fraction arithmetic.  It does not
import the primary verifier or any repository module, and it stores tensors
as sparse coordinate dictionaries rather than SymPy column matrices.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product

Vector = tuple[F, ...]
Tensor = dict[tuple[int, int, int], F]


def basis(size: int, index: int) -> Vector:
    return tuple(F(int(i == index)) for i in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(values, F(0)) for values in zip(*vectors, strict=True))


def scale(value: F | int, vector: Vector) -> Vector:
    return tuple(F(value) * entry for entry in vector)


def split(vector: Vector) -> tuple[Vector, Vector, Vector]:
    return vector[:3], vector[3:6], vector[6:9]


def polarized(u: Vector, v: Vector, q: Vector) -> Tensor:
    ux, uy, uz = split(u)
    vx, vy, vz = split(v)
    qx, qy, qz = split(q)
    out: Tensor = {}
    for x, y, z in product(range(3), repeat=3):
        value = (
            ux[x] * vy[y] * qz[z]
            + ux[x] * qy[y] * vz[z]
            + vx[x] * uy[y] * qz[z]
            + vx[x] * qy[y] * uz[z]
            + qx[x] * uy[y] * vz[z]
            + qx[x] * vy[y] * uz[z]
        )
        if value:
            out[(x, y, z)] = value
    return out


def tensor_add(left: Tensor, right: Tensor) -> Tensor:
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, F(0)) + value
        if not out[key]:
            del out[key]
    return out


def tensor_scale(value: F | int, tensor: Tensor) -> Tensor:
    return {key: F(value) * entry for key, entry in tensor.items() if entry}


def rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows = len(matrix)
    cols = len(columns)
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][col]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            multiple = matrix[row][col]
            matrix[row] = [
                matrix[row][j] - multiple * matrix[pivot_row][j]
                for j in range(cols)
            ]
        pivot_row += 1
    return pivot_row


def pair(left: Vector, right: Vector) -> Vector:
    return tuple(left[i] * right[j] for i in range(3) for j in range(3))


def graph_contraction_audit() -> None:
    e0, e1, e2 = (basis(3, i) for i in range(3))
    beta = F(5)
    c = scale(F(-1, 4), e2)
    graph_columns = [scale(2, e0), scale(3, e1), scale(4, e2)]
    phi = [
        add(
            scale(beta, pair(a, e2)),
            pair(c, graph_columns[index]),
        )
        for index, a in enumerate((e0, e1, e2))
    ]
    assert rank(phi) == 3
    target = pair(e2, e2)
    assert scale(F(1, 4), phi[2]) == target
    assert graph_columns[2] != scale(-beta / c[2], e2)
    print("independent graph contraction audit: PASS")


def zero_row_audit() -> None:
    targets = [{(i, i, i): F(1)} for i in range(3)]
    kappa = F(7)
    for missing in range(3):
        corrections = [{}, {}, {}]
        corrections[missing] = tensor_scale(-F(1, 7), targets[missing])
        for first in range(3):
            for third in range(3):
                left = (
                    tensor_scale(-1, targets[missing])
                    if first == third == missing
                    else {}
                )
                right = (
                    tensor_scale(kappa, corrections[first])
                    if third == missing
                    else {}
                )
                assert left == right
        assert ((2, 2, 2) in corrections[missing]) == (missing == 2)
    print("independent zero-row audit: PASS")


def two_source_atlas_audit() -> None:
    x0, x1 = basis(9, 0), basis(9, 1)
    y0 = basis(9, 3)
    z0, z1 = basis(9, 6), basis(9, 7)
    u = add(x0, y0)

    # Nonconjugate line: the common zero is y-x and its square keeps x,y.
    q0, q1 = x1, z0
    v = add(y0, scale(-1, x0))
    assert polarized(u, v, q0) == polarized(u, v, q1) == {}
    assert polarized(v, v, q1) == {(0, 0, 0): F(-2)}

    # Conjugate line: lambda(y-x)+z' stays a common zero; all square values
    # retain the x,y factor lines or the active z0 line.
    q0 = add(x0, scale(-1, y0))
    v = add(y0, scale(-1, x0), z1)
    assert polarized(u, v, q0) == polarized(u, v, z0) == {}
    square_kernel = polarized(v, v, q0)
    square_active = polarized(v, v, z0)
    assert set(square_kernel) <= {(0, 0, 1)}
    assert set(square_active) <= {(0, 0, 0), (0, 0, 1)}
    print("independent two-source pencil audit: PASS")


def three_source_atlas_audit() -> None:
    x0, x1 = basis(9, 0), basis(9, 1)
    y0 = basis(9, 3)
    z0 = basis(9, 6)
    u = add(x0, y0, z0)

    scaling = add(x0, y0, scale(-2, z0))
    v = add(scale(3, x0), scale(-1, y0), z0)
    assert polarized(u, v, scaling) == polarized(u, v, x1) == {}
    assert set(polarized(v, v, scaling)) <= {(0, 0, 0)}
    assert set(polarized(v, v, x1)) <= {(1, 0, 0)}

    boundary = add(y0, scale(-1, z0))
    pure = add(x0, scale(2, x1))
    assert polarized(u, pure, boundary) == polarized(u, pure, x1) == {}
    assert polarized(pure, pure, boundary) == polarized(pure, pure, x1) == {}
    print("independent three-source pencil audit: PASS")


def row_profile_audit() -> None:
    # Matrices are stored by columns.  These separately replay the invertible,
    # equal-kernel, and unequal-kernel profiles used in the proof.
    full = (
        (F(2), F(0), F(0)),
        (F(0), F(3), F(0)),
        (F(5), F(7), F(11)),
    )
    same = (
        (F(2), F(0), F(0)),
        (F(0), F(3), F(0)),
        (F(0), F(0), F(0)),
    )
    different = (
        (F(0), F(0), F(0)),
        (F(0), F(3), F(0)),
        (F(5), F(7), F(0)),
    )
    assert rank(list(full)) == 3
    assert rank(list(same)) == rank(list(different)) == 2
    assert same[2] == (F(0), F(0), F(0))
    assert different[0] == (F(0), F(0), F(0))
    assert different[2][0] and different[2][1]
    print("independent graph-profile audit: PASS")


def binary_boundary_audit() -> None:
    x0, x1 = basis(9, 0), basis(9, 1)
    y0 = basis(9, 3)
    z0 = basis(9, 6)
    full = add(x0, y0, z0)
    q_a = add(x0, scale(-1, y0))
    q_b = add(x0, scale(-1, z0))
    assert polarized(full, full, q_a) == polarized(full, full, q_b) == {}

    pure = x0
    mixed = add(y0, z0)
    q_plane = (x1, add(y0, scale(-1, z0)))
    assert all(polarized(pure, mixed, q) == {} for q in q_plane)
    square = [polarized(mixed, mixed, q) for q in q_plane]
    assert square[0] == {(1, 0, 0): F(2)}
    assert square[1] == {}
    print("independent binary five-product audit: PASS")


def main() -> None:
    graph_contraction_audit()
    zero_row_audit()
    row_profile_audit()
    two_source_atlas_audit()
    three_source_atlas_audit()
    binary_boundary_audit()
    print("independent support-one higher-row-rank exclusion: PASS")


if __name__ == "__main__":
    main()
