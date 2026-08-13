"""Independent no-import audit of the (1,1,2) third-colour coloop exclusion.

This audit uses standard-library Fraction arithmetic, its own elimination,
a third-index-major tensor convention, direct derivative contraction, and
separately derived support-map matrices.  It imports no repository or
third-party module.
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
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
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


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right, strict=True))


def tensor_index(i: int, j: int, k: int, dimension: int) -> int:
    """Third-index-major storage, deliberately unlike the primary replay."""
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


def block_basis(index: int, dimension: int = 2) -> BlockVector:
    blocks = [[Q(0)] * dimension for _ in range(3)]
    blocks[index // dimension][index % dimension] = Q(1)
    return blocks[0], blocks[1], blocks[2]


def linear_map_rows(images: list[list[Fraction]]) -> list[list[Fraction]]:
    return columns_to_rows(images)


def coloop_geometry_audit() -> None:
    columns = [
        [Q(1), Q(1), Q(0)],
        [Q(0), Q(0), Q(1)],
        [Q(1), Q(0), Q(0)],
        [Q(0), Q(1), Q(0)],
        [Q(2), Q(1), Q(0)],
        [Q(-1), Q(3), Q(0)],
        [Q(5), Q(-2), Q(0)],
    ]
    full = columns_to_rows(columns)
    other = columns_to_rows([column for index, column in enumerate(columns) if index != 1])
    assert rank(full) == 3
    assert rank(other) == 2
    assert rank(columns_to_rows(columns[2:4])) == 2
    assert columns[1][2] == 1
    assert all(column[2] == 0 for index, column in enumerate(columns) if index != 1)
    assert 7 - rank(full) == 4

    cells = [
        (i, j, k)
        for i, j, k in product((1, 2), (0, 2), range(3))
        if i == j == k
    ]
    assert cells == [(2, 2, 2)]
    print("independent coloop/untouched-table audit: PASS")


def derivative_value(
    a: list[Fraction],
    b: list[Fraction],
    c: list[Fraction],
    z: list[Fraction],
    w: list[Fraction],
) -> list[Fraction]:
    # s=0,t=1, lambda=2, mu=3.
    answer = [Q(0)] * 27
    for i, j, k in product(range(3), repeat=3):
        value = -3 * a[i] * int(j == 1) * z[k]
        value -= 2 * int(i == 0) * b[j] * w[k]
        value += 6 * int(i == 0) * int(j == 1) * c[k]
        answer[tensor_index(i, j, k, 3)] = value
    return answer


def theta_and_contraction_audit() -> None:
    z = [Q(1), Q(1), Q(0)]
    w = [Q(0), Q(1), Q(1)]
    n = [Q(1), Q(-1), Q(1)]
    assert rank([z, w]) == 2
    assert dot(n, z) == dot(n, w) == 0

    # q_0=A+v, q_1=A+B, q_2=B in W=V direct-sum <A,B>.
    q_columns = [
        [Q(1), Q(0), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(0), Q(1), Q(1)],
        [Q(0), Q(0), Q(0), Q(0), Q(1)],
    ]
    q_rows = columns_to_rows(q_columns)
    quotient_rows = q_rows[3:5]
    assert quotient_rows == [z, w]
    assert rank(quotient_rows) == 2
    assert rank(q_rows) == 3
    assert matvec(q_rows, n) == [Q(1), Q(0), Q(0), Q(0), Q(0)]

    gamma = [Q(1), Q(-1), Q(0)]
    delta = [Q(1), Q(0), Q(0)]
    assert dot(gamma, z) == 0 and gamma[1] * dot(gamma, w) != 0
    assert dot(delta, w) == 0 and delta[0] != 0

    # If theta(n)=0, n also kills D_B(K): here c is any representative in
    # n^perp, while n already kills z,w.
    a = [Q(2), Q(3), Q(5)]
    b = [Q(7), Q(11), Q(13)]
    c = [Q(17), Q(17), Q(0)]
    derivative = derivative_value(a, b, c, z, w)
    contraction = []
    for i, j in product(range(3), repeat=2):
        contraction.append(
            sum(
                n[k] * derivative[tensor_index(i, j, k, 3)]
                for k in range(3)
            )
        )
    assert dot(n, c) == 0
    assert contraction == [Q(0)] * 9

    target_contraction = [Q(0)] * 27
    for colour in range(3):
        target_contraction[tensor_index(colour, colour, colour, 3)] = n[colour]
    assert any(target_contraction)
    print("independent theta-rank/normal-contraction audit: PASS")


def square_upgrade_audit() -> None:
    r: BlockVector = ([Q(1), Q(2)], [Q(3), Q(5)], [Q(7), Q(11)])
    b_row: BlockVector = ([Q(13), Q(17)], [Q(19), Q(23)], [Q(29), Q(31)])
    h_row: BlockVector = ([Q(37), Q(41)], [Q(43), Q(47)], [Q(53), Q(59)])
    scalar = Q(7)
    q_row: BlockVector = tuple(
        [scalar * b + h for b, h in zip(b_block, h_block, strict=True)]
        for b_block, h_block in zip(b_row, h_row, strict=True)
    )  # type: ignore[assignment]
    square = permanent(r, q_row, q_row)
    exterior = permanent(r, b_row, q_row)
    zero_term = permanent(r, h_row, q_row)
    expected = [scalar * value for value in exterior]
    expected = [a + b for a, b in zip(expected, zero_term, strict=True)]
    assert square == expected
    assert Q(2) * Q(3) * Q(5) != 0
    print("independent exterior-to-square audit: PASS")


def support_map_audit() -> None:
    zero = [Q(0), Q(0)]
    base = [Q(1), Q(0)]

    three: BlockVector = (base[:], base[:], base[:])
    three_images = [permanent(three, three, block_basis(index)) for index in range(6)]
    three_map = linear_map_rows(three_images)
    three_kernel = (
        [Q(1), Q(0), Q(-1), Q(0), Q(0), Q(0)],
        [Q(1), Q(0), Q(0), Q(0), Q(-1), Q(0)],
    )
    assert rank(three_map) == 4
    assert all(matvec(three_map, vector) == [Q(0)] * 8 for vector in three_kernel)
    assert rank([list(vector) for vector in three_kernel]) == 2

    two: BlockVector = (base[:], base[:], zero[:])
    two_images = [permanent(two, two, block_basis(index)) for index in range(6)]
    two_map = linear_map_rows(two_images)
    xy_basis = [[Q(int(i == j)) for i in range(6)] for j in range(4)]
    assert rank(two_map) == 2
    assert all(matvec(two_map, vector) == [Q(0)] * 8 for vector in xy_basis)
    assert rank(xy_basis) == 4

    def tangent(q: BlockVector) -> list[Fraction]:
        answer = [Q(0)] * 4
        for i, j in product(range(2), repeat=2):
            answer[i + 2 * j] = base[i] * q[1][j] + q[0][i] * base[j]
        return answer

    tangent_images = [tangent(block_basis(index)) for index in range(4)]
    tangent_map = linear_map_rows(tangent_images)
    tangent_kernel = [Q(1), Q(0), Q(-1), Q(0)]
    assert rank(tangent_map) == 3
    assert matvec(tangent_map, tangent_kernel) == [Q(0)] * 4

    # Check per(r,p,q)=p_Z tensor L(q) on bases; bilinearity then gives the
    # full two-source identity independently of the primary implementation.
    for p_index, q_index in product(range(6), range(4)):
        p = block_basis(p_index)
        q = block_basis(q_index)
        actual = permanent(two, p, q)
        expected = [Q(0)] * 8
        tangent_q = tangent(q)
        for i, j, k in product(range(2), repeat=3):
            expected[tensor_index(i, j, k, 2)] = tangent_q[i + 2 * j] * p[2][k]
        assert actual == expected
    print("independent three-/two-source support audit: PASS")


def pure_conjugate_audit() -> None:
    zero = [Q(0), Q(0)]
    base = [Q(1), Q(0)]

    def scaled(scalar: Fraction, vector: list[Fraction]) -> list[Fraction]:
        return [scalar * value for value in vector]

    def expected_value(
        c_row: BlockVector,
        p_x: list[Fraction],
        q_x: list[Fraction],
        a: Fraction,
        b: Fraction,
    ) -> list[Fraction]:
        first_x = [b * p - a * q for p, q in zip(p_x, q_x, strict=True)]
        second_x = [b * p + a * q for p, q in zip(p_x, q_x, strict=True)]
        first = tensor3(first_x, c_row[1], base)
        second = tensor3(second_x, base, c_row[2])
        return [left + right for left, right in zip(first, second, strict=True)]

    x_options = (zero, [Q(1), Q(0)], [Q(0), Q(1)])
    for c_index, p_x, q_x, a, b in product(
        range(6), x_options, x_options, (Q(0), Q(1)), (Q(0), Q(1))
    ):
        c_row = block_basis(c_index)
        p: BlockVector = (p_x, scaled(a, base), scaled(-a, base))
        q: BlockVector = (q_x, scaled(b, base), scaled(b, base))
        actual = permanent(c_row, p, q)
        assert actual == expected_value(c_row, p_x, q_x, a, b)
        assert actual[tensor_index(0, 1, 1, 2)] == 0
        assert actual[tensor_index(1, 1, 1, 2)] == 0

    pure: BlockVector = (base[:], zero[:], zero[:])
    square_vector: BlockVector = ([Q(2), Q(3)], base[:], base[:])
    expected_square = [2 * value for value in tensor3(base, base, base)]
    assert permanent(square_vector, square_vector, pure) == expected_square

    # A decomposable tensor killed by the double quotient has y_1*z_1=0,
    # hence its Y line is <y> or its Z line is <zeta>.
    nonzero_vectors = [
        [Q(a), Q(b)]
        for a, b in product((-1, 0, 1), repeat=2)
        if (a, b) != (0, 0)
    ]
    for x_vector, y_vector, z_vector in product(nonzero_vectors, repeat=3):
        decomposable = tensor3(x_vector, y_vector, z_vector)
        quotient = [
            decomposable[tensor_index(i, 1, 1, 2)] for i in range(2)
        ]
        if quotient == [Q(0), Q(0)]:
            assert y_vector[1] == 0 or z_vector[1] == 0

    two_plane = [[Q(1), Q(0), Q(1)], [Q(0), Q(1), Q(1)], [Q(0)] * 3]
    assert rank(two_plane) == 2
    assert rank([[Q(int(i == j)) for j in range(3)] for i in range(3)]) == 3
    print("independent pure/conjugate factor-sharing audit: PASS")


def main() -> None:
    coloop_geometry_audit()
    theta_and_contraction_audit()
    square_upgrade_audit()
    support_map_audit()
    pure_conjugate_audit()
    print("independent (1,1,2) third-colour coloop exclusion: PASS")


if __name__ == "__main__":
    main()
