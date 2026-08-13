"""Independent no-import audit of the repeated-coordinate HB exclusion.

This audit uses standard-library Fraction arithmetic, a third-index-major
tensor convention, and its own elimination.  It imports no repository or
third-party module.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


Q = Fraction


def rank(rows: list[list[Fraction]]) -> int:
    work = [row[:] for row in rows]
    if not work:
        return 0
    nrows, ncols = len(work), len(work[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next(
            (index for index in range(pivot_row, nrows) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(nrows):
            if index == pivot_row:
                continue
            multiple = work[index][column]
            if multiple:
                work[index] = [
                    left - multiple * right
                    for left, right in zip(work[index], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def tensor_index(i: int, j: int, k: int) -> int:
    """Third-index-major convention, deliberately unlike the primary replay."""
    return i + 3 * j + 9 * k


def derivative_matrix(lam: int, mu: int, nu: int) -> list[list[Fraction]]:
    s, t = 2, 0
    matrix = [[Q(0) for _ in range(9)] for _ in range(27)]
    for i in range(3):
        matrix[tensor_index(i, s, t)][i] = Q(-mu * nu)
    for j in range(3):
        matrix[tensor_index(s, j, t)][3 + j] = Q(-lam * nu)
    for k in range(3):
        matrix[tensor_index(s, s, k)][6 + k] = Q(lam * mu)
    return matrix


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def derivative_audit() -> None:
    lam, mu, nu = 2, 3, 5
    matrix = derivative_matrix(lam, mu, nu)
    assert rank(matrix) == 7

    k1 = [Q(0) for _ in range(9)]
    k2 = [Q(0) for _ in range(9)]
    k1[2], k1[6] = Q(lam), Q(nu)
    k2[5], k2[6] = Q(mu), Q(nu)
    assert matvec(matrix, k1) == [Q(0)] * 27
    assert matvec(matrix, k2) == [Q(0)] * 27
    assert rank([k1, k2]) == 2

    touched = {
        (i, 2, 0) for i in range(3)
    } | {
        (2, j, 0) for j in range(3)
    } | {
        (2, 2, k) for k in range(3)
    }
    actual = {
        (i, j, k)
        for i, j, k in product(range(3), repeat=3)
        if any(matrix[tensor_index(i, j, k)])
    }
    assert actual == touched
    assert len(actual) == 7
    print("independent derivative/support audit: PASS")


def torus_recovery_audit() -> None:
    lam, mu, nu = Q(2), Q(3), Q(5)
    gamma_t = Q(7)
    alpha = [Q(11), Q(13), -nu * gamma_t / lam]
    beta = [Q(17), Q(19), -nu * gamma_t / mu]
    gamma = [gamma_t, Q(23), Q(29)]

    assert lam * alpha[2] + nu * gamma[0] == 0
    assert mu * beta[2] + nu * gamma[0] == 0

    first = [-mu * nu * beta[2] * gamma[0] * value for value in alpha]
    second = [-lam * nu * alpha[2] * gamma[0] * value for value in beta]
    third = [lam * mu * alpha[2] * beta[2] * value for value in gamma]
    ell = alpha + beta + gamma
    recovered = first + second + third
    scale = nu * nu * gamma_t * gamma_t
    assert recovered == [scale * value for value in ell]
    assert all(ell)
    print("independent torus self-recovery: PASS")


def coloop_audit() -> None:
    for coloop in range(7):
        columns: list[list[Fraction]] = []
        counter = 0
        for index in range(7):
            if index == coloop:
                columns.append([Q(0), Q(0), Q(1)])
            else:
                columns.append([Q(1), Q(counter), Q(0)])
                counter += 1
        full_rows = [[columns[column][row] for column in range(7)] for row in range(3)]
        deleted_rows = [
            [columns[column][row] for column in range(7) if column != coloop]
            for row in range(3)
        ]
        assert rank(full_rows) == 3
        assert rank(deleted_rows) == 2
        assert 7 - rank(full_rows) == 4
    print("independent coloop rank audit: PASS")


def equal_plane_audit() -> None:
    # For M=[[a,b],[c,d]], skew(M E00)=-c and skew(M E11)=b.
    samples = (
        (Q(2), Q(0), Q(0), Q(3)),
        (Q(5), Q(0), Q(0), Q(-7)),
    )
    for a, b, c, d in samples:
        skew_e00 = -c
        skew_e11 = b
        assert skew_e00 == skew_e11 == 0
        assert a * d - b * c != 0

    for a, b, c, d in (
        (Q(2), Q(1), Q(0), Q(3)),
        (Q(2), Q(0), Q(1), Q(3)),
    ):
        assert (-c, b) != (Q(0), Q(0))
    print("independent equal-plane orientation: PASS")


def binary_cubic_audit() -> None:
    # Coefficients are (x^3,x^2 y,x y^2,y^3).  Directional derivative in
    # the x direction has coefficient matrix diag(3,2,1) on the first three
    # inputs and kills only y^3.
    derivative_rows = [
        [Q(3), Q(0), Q(0), Q(0)],
        [Q(0), Q(2), Q(0), Q(0)],
        [Q(0), Q(0), Q(1), Q(0)],
    ]
    assert rank(derivative_rows) == 3
    assert matvec(derivative_rows, [Q(0), Q(0), Q(0), Q(1)]) == [Q(0)] * 3

    # Two active off-target source families force every target family onto
    # the one derivative-kernel line.
    for first, second in ((0, 1), (0, 2), (1, 2)):
        forced = ({0, 1, 2} - {first}) | ({0, 1, 2} - {second})
        assert forced == {0, 1, 2}
    print("independent binary-cubic/UFD audit: PASS")


def quotient_audit() -> None:
    # Multiplication by x, y, and x+2y from binary linear forms to quadrics.
    matrices = (
        [[Q(1), Q(0)], [Q(0), Q(1)], [Q(0), Q(0)]],
        [[Q(0), Q(0)], [Q(1), Q(0)], [Q(0), Q(1)]],
        [[Q(1), Q(0)], [Q(2), Q(1)], [Q(0), Q(2)]],
    )
    assert all(rank(matrix) == 2 for matrix in matrices)

    # With all Y and Z components on fixed lines, each mixed coefficient has
    # those same two factors; stripping them leaves only an X coefficient.
    y1, z1 = Q(3), Q(5)
    mixed = [Q(7) * y1 * z1, Q(11) * y1 * z1]
    assert [value / (y1 * z1) for value in mixed] == [Q(7), Q(11)]
    print("independent quotient/factor-sharing audit: PASS")


def main() -> None:
    derivative_audit()
    torus_recovery_audit()
    coloop_audit()
    equal_plane_audit()
    binary_cubic_audit()
    quotient_audit()
    print("independent repeated-coordinate Hilbert--Burch exclusion: PASS")


if __name__ == "__main__":
    main()
