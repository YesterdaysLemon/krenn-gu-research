"""Independent no-import audit of the (1,1,2) central-colour coloop exclusion.

The audit uses standard-library Fraction arithmetic, separate elimination,
a third-index-major tensor layout, and independently constructed kernel and
annihilator models.  It imports no repository or third-party module.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction


def rank(rows: list[list[Fraction]]) -> int:
    work = [row[:] for row in rows]
    if not work:
        return 0
    nrows, ncols = len(work), len(work[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next(
            (row for row in range(pivot_row, nrows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(nrows):
            if row == pivot_row:
                continue
            multiple = work[row][column]
            if multiple:
                work[row] = [
                    left - multiple * right
                    for left, right in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def columns_to_rows(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*columns, strict=True)]


def matvec(rows: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in rows]


def tensor_index(i: int, j: int, k: int, dimension: int) -> int:
    """Third-index-major storage, unlike the primary SymPy replay."""
    return i + dimension * j + dimension * dimension * k


def tensor3(
    x: list[Fraction], y: list[Fraction], z: list[Fraction]
) -> list[Fraction]:
    dimension = len(x)
    answer = [Q(0)] * (dimension**3)
    for i, j, k in product(range(dimension), repeat=3):
        answer[tensor_index(i, j, k, dimension)] = x[i] * y[j] * z[k]
    return answer


BlockVector = tuple[list[Fraction], list[Fraction], list[Fraction]]


def permanent(
    left: BlockVector, middle: BlockVector, right: BlockVector
) -> list[Fraction]:
    arguments = (left, middle, right)
    dimension = len(left[0])
    answer = [Q(0)] * (dimension**3)
    for assignment in permutations(range(3)):
        term = tensor3(
            arguments[assignment[0]][0],
            arguments[assignment[1]][1],
            arguments[assignment[2]][2],
        )
        answer = [a + b for a, b in zip(answer, term, strict=True)]
    return answer


def basis_vector(index: int, dimension: int) -> list[Fraction]:
    return [Q(int(position == index)) for position in range(dimension)]


def block_basis(index: int, dimension: int) -> BlockVector:
    blocks = [[Q(0)] * dimension for _ in range(3)]
    blocks[index // dimension][index % dimension] = Q(1)
    return blocks[0], blocks[1], blocks[2]


def flatten(vector: BlockVector) -> list[Fraction]:
    return vector[0] + vector[1] + vector[2]


def scaled(scalar: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [scalar * value for value in vector]


def added(*vectors: list[Fraction]) -> list[Fraction]:
    return [sum(values) for values in zip(*vectors, strict=True)]


def map_rows(first: BlockVector, second: BlockVector) -> list[list[Fraction]]:
    dimension = len(first[0])
    images = [
        permanent(first, second, block_basis(index, dimension))
        for index in range(3 * dimension)
    ]
    return columns_to_rows(images)


def common_rows(first: BlockVector, plane: list[BlockVector]) -> list[list[Fraction]]:
    return [row for vector in plane for row in map_rows(first, vector)]


def geometry_and_theta_audit() -> None:
    columns = [
        [Q(0), Q(0), Q(1)],
        [Q(1), Q(1), Q(0)],
        [Q(1), Q(0), Q(0)],
        [Q(0), Q(1), Q(0)],
        [Q(2), Q(1), Q(0)],
        [Q(-1), Q(3), Q(0)],
        [Q(5), Q(-2), Q(0)],
    ]
    full = columns_to_rows(columns)
    other = columns_to_rows(columns[1:])
    assert rank(full) == 3
    assert rank(other) == 2
    assert columns[0][2] == 1 and all(column[2] == 0 for column in columns[1:])
    assert 7 - rank(full) == 4

    cells = [
        (i, j, k)
        for i, j, k in product((1, 2), (0, 2), range(3))
        if i == j == k
    ]
    assert cells == [(2, 2, 2)]

    z = [Q(1), Q(1), Q(0)]
    w = [Q(0), Q(1), Q(1)]
    n = [Q(1), Q(-1), Q(1)]
    q_columns = [
        [Q(1), Q(0), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(0), Q(1), Q(1)],
        [Q(0), Q(0), Q(0), Q(0), Q(1)],
    ]
    q_rows = columns_to_rows(q_columns)
    assert q_rows[3:5] == [z, w]
    assert rank(q_rows[3:5]) == 2
    assert rank(q_rows) == 3
    assert matvec(q_rows, n) == [Q(1), Q(0), Q(0), Q(0), Q(0)]
    print("independent central-coloop/theta audit: PASS")


def square_and_small_support_audit() -> None:
    zero = [Q(0), Q(0)]
    base = [Q(1), Q(0)]

    # One source: the square is pure, while conjugate S/Q rows land in the
    # union of the two fixed-factor subspaces.
    pure: BlockVector = (base[:], zero[:], zero[:])
    square_row: BlockVector = ([Q(2), Q(3)], base[:], base[:])
    expected_square = [2 * value for value in tensor3(base, base, base)]
    assert permanent(square_row, square_row, pure) == expected_square
    for a, b in product((Q(0), Q(1)), repeat=2):
        p: BlockVector = ([Q(2), Q(3)], scaled(a, base), scaled(-a, base))
        q: BlockVector = ([Q(5), Q(7)], scaled(b, base), scaled(b, base))
        for c_index in range(6):
            value = permanent(block_basis(c_index, 2), p, q)
            assert value[tensor_index(0, 1, 1, 2)] == 0
            assert value[tensor_index(1, 1, 1, 2)] == 0

    x_only_0: BlockVector = (base[:], zero[:], zero[:])
    x_only_1: BlockVector = ([Q(0), Q(1)], zero[:], zero[:])
    assert permanent(x_only_0, x_only_1, square_row) == [Q(0)] * 8

    # Two sources: M(v)=(L(v),v_Z) has rank five and one-dimensional
    # kernel, so a fibre through the square vector has dimension two.
    two: BlockVector = (base[:], base[:], zero[:])

    def tangent(vector: BlockVector) -> list[Fraction]:
        answer = [Q(0)] * 4
        for i, j in product(range(2), repeat=2):
            answer[i + 2 * j] = base[i] * vector[1][j] + vector[0][i] * base[j]
        return answer

    m_images = []
    for index in range(6):
        vector = block_basis(index, 2)
        m_images.append(tangent(vector) + vector[2])
    m_rows = columns_to_rows(m_images)
    kernel = [Q(1), Q(0), Q(-1), Q(0), Q(0), Q(0)]
    assert rank(m_rows) == 5
    assert matvec(m_rows, kernel) == [Q(0)] * 6
    q_two: BlockVector = ([Q(0), Q(1)], zero[:], base[:])
    assert permanent(q_two, q_two, two) == [
        2 * value for value in tensor3(q_two[0], base, base)
    ]
    assert rank([flatten(q_two), kernel]) == 2
    print("independent one-/two-source audit: PASS")


def two_supported_full_row_audit() -> None:
    dimension = 3
    zero = [Q(0)] * dimension
    x = y = zeta = basis_vector(0, dimension)
    q: BlockVector = (x[:], y[:], zero[:])

    # D!=0: explicit kernel rows and their common annihilator.
    for r in (
        (basis_vector(1, 3), basis_vector(1, 3), zeta[:]),
        (x[:], y[:], zeta[:]),
    ):
        k0: BlockVector = (
            scaled(-1, r[0]),
            scaled(-1, r[1]),
            zeta[:],
        )
        k1: BlockVector = (x[:], scaled(-1, y), zero[:])
        kernel_rows = map_rows(r, q)
        assert rank(kernel_rows) == 7
        assert matvec(kernel_rows, flatten(k0)) == [Q(0)] * 27
        assert matvec(kernel_rows, flatten(k1)) == [Q(0)] * 27
        annihilator = common_rows(r, [k0, k1])
        assert rank(annihilator) == 8
        assert matvec(annihilator, flatten(q)) == [Q(0)] * 54

    # D=0: K=<x,-y,0>+Z.  Test both the zero-core plane and a mixed plane.
    cancelling_r: BlockVector = (x[:], scaled(-1, y), zeta[:])
    cancelling_rows = map_rows(cancelling_r, q)
    assert rank(cancelling_rows) == 5
    kernel_line: BlockVector = (x[:], scaled(-1, y), zero[:])
    assert matvec(cancelling_rows, flatten(kernel_line)) == [Q(0)] * 27
    for index in range(3):
        z_row: BlockVector = (zero[:], zero[:], basis_vector(index, 3))
        assert matvec(cancelling_rows, flatten(z_row)) == [Q(0)] * 27

    z0: BlockVector = (zero[:], zero[:], basis_vector(1, 3))
    z1: BlockVector = (zero[:], zero[:], basis_vector(2, 3))
    assert permanent(z0, z1, block_basis(0, 3)) == [Q(0)] * 27
    mixed: BlockVector = (
        kernel_line[0],
        kernel_line[1],
        basis_vector(2, 3),
    )
    mixed_annihilator = common_rows(cancelling_r, [z0, mixed])
    assert rank(mixed_annihilator) == 8
    assert matvec(mixed_annihilator, flatten(q)) == [Q(0)] * 54
    print("independent full-row/two-supported-square audit: PASS")


def full_supported_moving_audit() -> None:
    dimension = 3
    zero = [Q(0)] * dimension
    x = y = zeta = basis_vector(0, dimension)
    a = basis_vector(1, dimension)
    r: BlockVector = (x[:], y[:], zeta[:])

    for b, c in ((Q(2), Q(3)), (Q(1), Q(2))):
        q: BlockVector = (a[:], scaled(b, y), scaled(c, zeta))
        square_x = added(scaled(b * c, x), scaled(b + c, a))
        expected = [2 * value for value in tensor3(square_x, y, zeta)]
        assert permanent(q, q, r) == expected

        s_alpha: BlockVector = (
            scaled(Q(-1, b + c), added(a, scaled(c, x))),
            y[:],
            zero[:],
        )
        s_beta: BlockVector = (
            scaled(Q(-1, b + c), added(a, scaled(b, x))),
            zero[:],
            zeta[:],
        )
        kernel_rows = map_rows(r, q)
        assert rank(kernel_rows) == 7
        assert matvec(kernel_rows, flatten(s_alpha)) == [Q(0)] * 27
        assert matvec(kernel_rows, flatten(s_beta)) == [Q(0)] * 27
        annihilator = common_rows(r, [s_alpha, s_beta])
        assert rank(annihilator) == 8
        assert matvec(annihilator, flatten(q)) == [Q(0)] * 54

    opposite: BlockVector = (a[:], scaled(2, y), scaled(-2, zeta))
    opposite_rows = map_rows(r, opposite)
    assert rank(opposite_rows) == 6
    for index in range(3):
        x_row: BlockVector = (basis_vector(index, 3), zero[:], zero[:])
        assert matvec(opposite_rows, flatten(x_row)) == [Q(0)] * 27
    assert permanent(
        (basis_vector(0, 3), zero[:], zero[:]),
        (basis_vector(1, 3), zero[:], zero[:]),
        block_basis(5, 3),
    ) == [Q(0)] * 27
    print("independent full-square/moving-factor audit: PASS")


def full_supported_aligned_audit() -> None:
    dimension = 3
    zero = [Q(0)] * dimension
    x = y = zeta = basis_vector(0, dimension)
    r: BlockVector = (x[:], y[:], zeta[:])

    # No pair coefficient vanishes.
    regular: BlockVector = (x[:], y[:], zeta[:])
    regular_plane = [
        (x[:], scaled(-1, y), zero[:]),
        (x[:], zero[:], scaled(-1, zeta)),
    ]
    regular_rows = map_rows(r, regular)
    assert rank(regular_rows) == 7
    for vector in regular_plane:
        assert matvec(regular_rows, flatten(vector)) == [Q(0)] * 27
    for left, right, third in product(regular_plane, regular_plane, range(9)):
        value = permanent(left, right, block_basis(third, 3))
        assert all(
            value[tensor_index(i, j, k, 3)] == 0
            for i, j, k in product(range(3), repeat=3)
            if sum(index != 0 for index in (i, j, k)) >= 2
        )

    # One pair coefficient vanishes: K=X + <(0,-3y,zeta)>.
    one: BlockVector = (scaled(2, x), y[:], scaled(-1, zeta))
    one_rows = map_rows(r, one)
    one_kernel = [
        (basis_vector(index, 3), zero[:], zero[:]) for index in range(3)
    ] + [(zero[:], scaled(-3, y), zeta[:])]
    assert rank(one_rows) == 5
    assert all(matvec(one_rows, flatten(vector)) == [Q(0)] * 27 for vector in one_kernel)
    for left, right, third in product(one_kernel, one_kernel, range(9)):
        value = permanent(left, right, block_basis(third, 3))
        assert all(
            value[tensor_index(i, j, k, 3)] == 0
            for i, j, k in product(range(3), repeat=3)
            if j != 0 and k != 0
        )

    # Two pair coefficients vanish: K=X+Y, and the quotient-Z coefficient
    # is the rank-five tangent map L(p).
    two: BlockVector = (x[:], y[:], scaled(-1, zeta))
    two_rows = map_rows(r, two)
    xy_basis = [
        block_basis(index, 3) for index in range(6)
    ]
    assert rank(two_rows) == 3
    assert all(matvec(two_rows, flatten(vector)) == [Q(0)] * 27 for vector in xy_basis)

    tangent_images = []
    for vector in xy_basis:
        answer = [Q(0)] * 9
        for i, j in product(range(3), repeat=2):
            answer[i + 3 * j] = x[i] * vector[1][j] + vector[0][i] * y[j]
        tangent_images.append(answer)
    assert rank(columns_to_rows(tangent_images)) == 5
    print("independent full-square/aligned-factor audit: PASS")


def main() -> None:
    geometry_and_theta_audit()
    square_and_small_support_audit()
    two_supported_full_row_audit()
    full_supported_moving_audit()
    full_supported_aligned_audit()
    print("independent (1,1,2) central-colour coloop exclusion: PASS")


if __name__ == "__main__":
    main()
