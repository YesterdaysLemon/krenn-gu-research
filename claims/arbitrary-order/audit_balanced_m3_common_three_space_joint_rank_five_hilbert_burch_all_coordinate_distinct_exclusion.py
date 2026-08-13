"""Independent no-import audit of the all-coordinate-distinct HB exclusion.

This audit uses only standard-library Fraction arithmetic, a deliberately
third-index-major tensor convention, and its own row reduction and permanent
implementation.  It imports no repository or third-party module.
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


def tensor_index(i: int, j: int, k: int) -> int:
    """Third-index-major convention, unlike the primary replay."""
    return i + 3 * j + 9 * k


def derivative_matrix(lam: int, mu: int, nu: int) -> list[list[Fraction]]:
    matrix = [[Q(0) for _ in range(9)] for _ in range(27)]
    for i in range(3):
        matrix[tensor_index(i, 1, 2)][i] = Q(-mu * nu)
    for j in range(3):
        matrix[tensor_index(0, j, 2)][3 + j] = Q(-lam * nu)
    for k in range(3):
        matrix[tensor_index(0, 1, k)][6 + k] = Q(lam * mu)
    return matrix


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right, strict=True))


def derivative_annihilator_audit() -> None:
    lam, mu, nu = 2, 3, 5
    matrix = derivative_matrix(lam, mu, nu)
    assert rank(matrix) == 7

    k1 = [Q(lam), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0), Q(nu)]
    k2 = [Q(0), Q(0), Q(0), Q(0), Q(mu), Q(0), Q(0), Q(0), Q(nu)]
    assert matvec(matrix, k1) == [Q(0)] * 27
    assert matvec(matrix, k2) == [Q(0)] * 27
    assert rank([k1, k2]) == 2

    basis = []
    for position in (1, 2, 3, 5, 6, 7):
        vector = [Q(0)] * 9
        vector[position] = Q(1)
        basis.append(vector)
    h = [Q(0)] * 9
    h[0], h[4], h[8] = Q(nu, lam), Q(nu, mu), Q(-1)
    basis.append(h)
    assert rank(basis) == 7
    assert all(dot(kernel, vector) == 0 for kernel in (k1, k2) for vector in basis)
    print("independent derivative/annihilator audit: PASS")


def torus_audit() -> None:
    lam, mu, nu, g = Q(2), Q(3), Q(5), Q(7)
    alpha = [nu * g / lam, Q(11), Q(13)]
    beta = [Q(17), nu * g / mu, Q(19)]
    gamma = [Q(23), Q(29), -g]
    ell = alpha + beta + gamma
    assert all(ell)
    assert lam * alpha[0] + nu * gamma[2] == 0
    assert mu * beta[1] + nu * gamma[2] == 0

    recovered = (
        [-mu * nu * beta[1] * gamma[2] * value for value in alpha]
        + [-lam * nu * alpha[0] * gamma[2] * value for value in beta]
        + [lam * mu * alpha[0] * beta[1] * value for value in gamma]
    )
    scale = nu * nu * gamma[2] * gamma[2]
    assert recovered == [scale * value for value in ell]
    print("independent torus self-recovery: PASS")


def target(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(int(i == j == k == colour) for colour in range(3))


def support_and_faces_audit() -> None:
    matrix = derivative_matrix(2, 3, 5)
    touched = {
        (i, j, k)
        for i, j, k in product(range(3), repeat=3)
        if any(matrix[tensor_index(i, j, k)])
    }
    expected = (
        {(i, 1, 2) for i in range(3)}
        | {(0, j, 2) for j in range(3)}
        | {(0, 1, k) for k in range(3)}
    )
    assert touched == expected
    assert len(touched) == 7

    core = list(product((1, 2), (0, 2), (0, 1)))
    assert len(core) == 8
    assert all(cell not in touched and target(*cell) == (0, 0, 0) for cell in core)

    face_a = {(j, k): target(0, j, k) for j, k in product((0, 2), (0, 1))}
    face_b = {(i, k): target(i, 1, k) for i, k in product((1, 2), (0, 1))}
    face_q2 = {(i, j): target(i, j, 2) for i, j in product((1, 2), (0, 2))}
    assert [key for key, value in face_a.items() if any(value)] == [(0, 0)]
    assert [key for key, value in face_b.items() if any(value)] == [(1, 1)]
    assert [key for key, value in face_q2.items() if any(value)] == [(2, 2)]
    assert face_a[(0, 0)] == (1, 0, 0)
    assert face_b[(1, 1)] == (0, 1, 0)
    assert face_q2[(2, 2)] == (0, 0, 1)
    print("independent support/target-face audit: PASS")


def coloop_and_symmetry_audit() -> None:
    for coloop in range(7):
        columns = []
        counter = 0
        for index in range(7):
            if index == coloop:
                columns.append([Q(0), Q(0), Q(1)])
            else:
                columns.append([Q(1), Q(counter), Q(0)])
                counter += 1
        full = [[columns[column][row] for column in range(7)] for row in range(3)]
        deleted = [
            [columns[column][row] for column in range(7) if column != coloop]
            for row in range(3)
        ]
        assert rank(full) == 3
        assert rank(deleted) == 2
        assert 7 - rank(full) == 4

    labels = {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)}
    orbit = {(sigma[2], sigma[0]) for sigma in permutations(range(3))}
    assert orbit == labels
    print("independent coloop/orbit audit: PASS")


Vector = tuple[list[Fraction], list[Fraction], list[Fraction]]


def permanent(left: Vector, middle: Vector, right: Vector) -> list[Fraction]:
    arguments = (left, middle, right)
    answer = [Q(0)] * 27
    for assignment in permutations(range(3)):
        x_part = arguments[assignment[0]][0]
        y_part = arguments[assignment[1]][1]
        z_part = arguments[assignment[2]][2]
        for i, j, k in product(range(3), repeat=3):
            answer[tensor_index(i, j, k)] += x_part[i] * y_part[j] * z_part[k]
    return answer


def two_plane_lemma_audit() -> None:
    # Directional derivative on (x^3,x^2y,xy^2,y^3) kills exactly y^3.
    derivative = [
        [Q(3), Q(0), Q(0), Q(0)],
        [Q(0), Q(2), Q(0), Q(0)],
        [Q(0), Q(0), Q(1), Q(0)],
    ]
    assert rank(derivative) == 3
    assert matvec(derivative, [Q(0), Q(0), Q(0), Q(1)]) == [Q(0)] * 3

    # A direct permanent replay in the missing-Z normal form.  Every mixed
    # value has the identical Z factor a_Z, independently of v or w.
    zero = [Q(0)] * 3
    s0: Vector = ([Q(1), Q(2), Q(0)], [Q(3), Q(5), Q(0)], zero[:])
    s1: Vector = ([Q(7), Q(11), Q(0)], [Q(13), Q(17), Q(0)], zero[:])
    a: Vector = ([Q(19), Q(0), Q(0)], [Q(23), Q(0), Q(0)], [Q(29), Q(31), Q(0)])
    assert permanent(s0, s0, s1) == [Q(0)] * 27
    assert permanent(s1, s0, s1) == [Q(0)] * 27

    for annihilator in (s0, s1):
        for test in (s0, s1):
            actual = permanent(a, annihilator, test)
            expected = [Q(0)] * 27
            for i, j, k in product(range(3), repeat=3):
                xy = (
                    annihilator[0][i] * test[1][j]
                    + test[0][i] * annihilator[1][j]
                )
                expected[tensor_index(i, j, k)] = xy * a[2][k]
            assert actual == expected
    print("independent binary-kernel/fixed-factor audit: PASS")


def ordinary_coloop_face_audit() -> None:
    lam, mu, nu = Q(2), Q(3), Q(5)
    zero = (Q(0), Q(0), Q(0))
    t0, t1 = (Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0))

    q0_table = []
    for j in (0, 2):
        a_face = tuple(nu / lam * value for value in (t0 if j == 0 else zero))
        q0_table.append(tuple(a_face[index] + zero[index] - zero[index] for index in range(3)))
    q1_table = []
    for i in (1, 2):
        b_face = tuple(nu / mu * value for value in (t1 if i == 1 else zero))
        q1_table.append(tuple(zero[index] + b_face[index] - zero[index] for index in range(3)))
    assert q0_table == [(nu / lam, Q(0), Q(0)), zero]
    assert q1_table == [(Q(0), nu / mu, Q(0)), zero]
    assert all(a != b for a, b in zip(t0, t1, strict=True) if a or b)
    print("independent ordinary-coloop face audit: PASS")


def main() -> None:
    derivative_annihilator_audit()
    torus_audit()
    support_and_faces_audit()
    coloop_and_symmetry_audit()
    two_plane_lemma_audit()
    ordinary_coloop_face_audit()
    print("independent all-coordinate-distinct Hilbert--Burch exclusion: PASS")


if __name__ == "__main__":
    main()
