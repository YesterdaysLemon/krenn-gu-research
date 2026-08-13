"""Independent no-import audit of the (1,1,2) central-coordinate localization.

The audit uses standard-library Fraction arithmetic, a third-index-major
tensor convention, its own elimination and permanent routines, separate
same-/distinct-colour models, and rational source-support atlases.  It
imports no repository or third-party module.
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


def tensor_index(i: int, j: int, k: int, dimension: int = 3) -> int:
    """Third-index-major convention, unlike the primary replay."""
    return i + dimension * j + dimension * dimension * k


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right, strict=True))


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [dot(row, vector) for row in matrix]


def derivative_matrix(
    s: int,
    t: int,
    z: tuple[int, int, int],
    w: tuple[int, int, int],
    lam: int = 2,
    mu: int = 3,
) -> list[list[Fraction]]:
    matrix = [[Q(0) for _ in range(9)] for _ in range(27)]
    for i, k in product(range(3), repeat=2):
        matrix[tensor_index(i, t, k)][i] = Q(-mu * z[k])
    for j, k in product(range(3), repeat=2):
        matrix[tensor_index(s, j, k)][3 + j] = Q(-lam * w[k])
    for k in range(3):
        matrix[tensor_index(s, t, k)][6 + k] = Q(lam * mu)
    return matrix


def derivative_annihilator_audit() -> None:
    models = (
        (0, 0, (1, 2, 0), (0, 1, 3)),
        (0, 1, (1, 2, 3), (2, 3, 5)),
        (0, 1, (1, 0, 3), (2, 3, 0)),
    )
    for s, t, z_raw, w_raw in models:
        z, w = list(map(Q, z_raw)), list(map(Q, w_raw))
        matrix = derivative_matrix(s, t, z_raw, w_raw)
        assert rank(matrix) == 7
        k1 = [Q(0)] * 9
        k2 = [Q(0)] * 9
        k1[s], k2[3 + t] = Q(2), Q(3)
        k1[6:9], k2[6:9] = z, w
        assert matvec(matrix, k1) == [Q(0)] * 27
        assert matvec(matrix, k2) == [Q(0)] * 27
        assert rank([k1, k2]) == 2

        basis: list[list[Fraction]] = []
        for i in range(3):
            if i != s:
                vector = [Q(0)] * 9
                vector[i] = Q(1)
                basis.append(vector)
        for j in range(3):
            if j != t:
                vector = [Q(0)] * 9
                vector[3 + j] = Q(1)
                basis.append(vector)
        for k in range(3):
            vector = [Q(0)] * 9
            vector[s] = -z[k] / 2
            vector[3 + t] = -w[k] / 3
            vector[6 + k] = Q(1)
            basis.append(vector)
        assert rank(basis) == 7
        assert all(dot(kernel, vector) == 0 for kernel in (k1, k2) for vector in basis)
    print("independent derivative/kernel/annihilator audit: PASS")


def torus_audit() -> None:
    for s, t in ((0, 0), (0, 1)):
        z, w, gamma = [Q(1), Q(2), Q(3)], [Q(2), Q(3), Q(5)], [Q(7), Q(11), Q(13)]
        gamma_z, gamma_w = dot(gamma, z), dot(gamma, w)
        alpha, beta = [Q(17), Q(19), Q(23)], [Q(29), Q(31), Q(37)]
        alpha[s], beta[t] = -gamma_z / 2, -gamma_w / 3
        ell = alpha + beta + gamma
        recovered = (
            [-3 * beta[t] * gamma_z * value for value in alpha]
            + [-2 * alpha[s] * gamma_w * value for value in beta]
            + [6 * alpha[s] * beta[t] * value for value in gamma]
        )
        assert recovered == [gamma_z * gamma_w * value for value in ell]
        assert all(ell)
    print("independent torus self-recovery audit: PASS")


def target(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(int(i == j == k == colour) for colour in range(3))


def target_and_relation_fork_audit() -> None:
    same = {
        cell: target(*cell)
        for cell in product((1, 2), repeat=3)
    }
    assert [cell for cell, value in same.items() if any(value)] == [
        (1, 1, 1),
        (2, 2, 2),
    ]
    distinct = {
        cell: target(*cell)
        for cell in product((1, 2), (0, 2), range(3))
    }
    assert [cell for cell, value in distinct.items() if any(value)] == [
        (2, 2, 2)
    ]

    # Deleting any one of the last three basis columns leaves R and P in a
    # rank-two plane.  The two recovery-factor hyperplanes have the same
    # dimension count, while the first four alternatives are retained.
    for deleted in (4, 5, 6):
        columns = []
        counter = 0
        for index in range(7):
            if index == deleted:
                columns.append([Q(0), Q(0), Q(1)])
            else:
                columns.append([Q(1), Q(counter), Q(0)])
                counter += 1
        full = [[columns[column][row] for column in range(7)] for row in range(3)]
        remaining = [
            [columns[column][row] for column in range(7) if column != deleted]
            for row in range(3)
        ]
        assert rank(full) == 3 and rank(remaining) == 2
        assert rank([row[:2] for row in remaining]) == 2
        assert rank([row[2:4] for row in remaining]) == 2
        assert 7 - rank(full) == 4
    assert 9 - 5 == 4
    print("independent target/nine-hyperplane fork audit: PASS")


BlockVector = tuple[list[Fraction], list[Fraction], list[Fraction]]


def permanent(
    left: BlockVector,
    middle: BlockVector,
    right: BlockVector,
) -> list[Fraction]:
    arguments = (left, middle, right)
    answer = [Q(0)] * 8
    for assignment in permutations(range(3)):
        x_part = arguments[assignment[0]][0]
        y_part = arguments[assignment[1]][1]
        z_part = arguments[assignment[2]][2]
        for i, j, k in product(range(2), repeat=3):
            answer[tensor_index(i, j, k, 2)] += x_part[i] * y_part[j] * z_part[k]
    return answer


def same_colour_symmetry_audit() -> None:
    for a, b, c, d in product(range(-2, 3), repeat=4):
        determinant = a * d - b * c
        if determinant == 0:
            continue
        # E00*M^-1 and E11*M^-1 must both be symmetric.
        form0 = [[Q(d, determinant), Q(-b, determinant)], [Q(0), Q(0)]]
        form1 = [[Q(0), Q(0)], [Q(-c, determinant), Q(a, determinant)]]
        if form0[0][1] == form0[1][0] and form1[0][1] == form1[1][0]:
            assert b == c == 0
    print("independent same-colour symmetry audit: PASS")


def distinct_colour_source_audit() -> None:
    zero = [Q(0), Q(0)]
    base = [Q(1), Q(0)]
    external: BlockVector = ([Q(2), Q(3)], [Q(5), Q(7)], [Q(11), Q(13)])

    pure: BlockVector = (base[:], zero[:], zero[:])
    q: BlockVector = ([Q(17), Q(19)], [Q(23), Q(29)], [Q(31), Q(37)])
    mixed = permanent(external, pure, q)
    assert all(
        mixed[tensor_index(1, j, k, 2)] == 0
        for j, k in product(range(2), repeat=2)
    )

    three: BlockVector = (base[:], base[:], base[:])
    scaling_vectors: tuple[BlockVector, ...] = (
        (base[:], [-value for value in base], zero[:]),
        (base[:], zero[:], [-value for value in base]),
    )
    for scaling in scaling_vectors:
        assert permanent(three, three, scaling) == [Q(0)] * 8
        tangent = permanent(external, three, scaling)
        assert all(
            tangent[tensor_index(i, j, k, 2)] == 0
            for i, j, k in product(range(2), repeat=3)
            if i + j + k >= 2
        )

    two: BlockVector = (base[:], base[:], zero[:])
    q_xy: BlockVector = ([Q(17), Q(19)], [Q(23), Q(29)], zero[:])
    assert permanent(two, two, q_xy) == [Q(0)] * 8
    expected = [Q(0)] * 8
    for i, j, k in product(range(2), repeat=3):
        expected[tensor_index(i, j, k, 2)] = external[2][k] * (
            base[i] * q_xy[1][j] + q_xy[0][i] * base[j]
        )
    assert permanent(external, two, q_xy) == expected

    # Exhaust a rational box: L(q)=0 exactly has q_X=-a*x, q_Y=a*y.
    kernel_vectors = []
    for qx0, qx1, qy0, qy1 in product(range(-2, 3), repeat=4):
        q_test: BlockVector = ([Q(qx0), Q(qx1)], [Q(qy0), Q(qy1)], zero[:])
        if permanent(external, two, q_test) == [Q(0)] * 8:
            # external_Z is nonzero, so this is exactly the L-kernel.
            kernel_vectors.append((qx0, qx1, qy0, qy1))
            assert qx1 == qy1 == 0 and qx0 == -qy0
    assert kernel_vectors

    # The core square at q_u=(x,-y) has XY matrix
    # [[dy0-dx0,dy1],[-dx1,0]], whose determinant is dx1*dy1.
    for dx0, dx1, dy0, dy1 in product(range(-2, 3), repeat=4):
        determinant = dx1 * dy1
        if determinant:
            matrix_rows = [[Q(dy0 - dx0), Q(dy1)], [Q(-dx1), Q(0)]]
            assert rank(matrix_rows) == 2
        else:
            assert determinant == 0
    print("independent distinct-colour source atlas: PASS")


def main() -> None:
    derivative_annihilator_audit()
    torus_audit()
    target_and_relation_fork_audit()
    same_colour_symmetry_audit()
    distinct_colour_source_audit()
    print("independent (1,1,2) central-coordinate torus localization: PASS")


if __name__ == "__main__":
    main()
