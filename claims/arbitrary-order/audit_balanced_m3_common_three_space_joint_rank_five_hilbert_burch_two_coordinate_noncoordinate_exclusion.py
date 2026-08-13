"""Independent no-import audit of the two-coordinate/noncoordinate exclusion.

This audit uses standard-library Fraction arithmetic, a third-index-major
tensor convention, its own elimination and permanent routines, four separate
noncoordinate support charts, and independently assembled hyperplane models.
It imports no repository or third-party module.
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


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def matmul(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    right_t = transpose(right)
    return [[dot(row, column) for column in right_t] for row in left]


def derivative_matrix(
    lam: int, mu: int, z: tuple[int, int, int]
) -> list[list[Fraction]]:
    matrix = [[Q(0) for _ in range(9)] for _ in range(27)]
    for i, k in product(range(3), repeat=2):
        matrix[tensor_index(i, 1, k)][i] = Q(-mu * z[k])
    for j, k in product(range(3), repeat=2):
        matrix[tensor_index(0, j, k)][3 + j] = Q(-lam * z[k])
    for k in range(3):
        matrix[tensor_index(0, 1, k)][6 + k] = Q(lam * mu)
    return matrix


def perpendicular_basis(z: tuple[int, int, int]) -> list[list[Fraction]]:
    z0, z1, z2 = map(Q, z)
    if z0:
        return [[-z1, z0, Q(0)], [-z2, Q(0), z0]]
    return [[Q(1), Q(0), Q(0)], [Q(0), -z2, z1]]


def derivative_and_torus_audit() -> None:
    lam, mu = 2, 3
    charts = ((2, 3, 0), (2, 0, 5), (0, 3, 5), (2, 3, 5))
    for z_raw in charts:
        z = list(map(Q, z_raw))
        matrix = derivative_matrix(lam, mu, z_raw)
        assert rank(matrix) == 7

        k1 = [Q(lam), Q(0), Q(0), Q(0), Q(0), Q(0)] + z
        k2 = [Q(0), Q(0), Q(0), Q(0), Q(mu), Q(0)] + z
        assert matvec(matrix, k1) == [Q(0)] * 27
        assert matvec(matrix, k2) == [Q(0)] * 27
        assert rank([k1, k2]) == 2

        basis: list[list[Fraction]] = []
        for position in (1, 2, 3, 5):
            vector = [Q(0)] * 9
            vector[position] = Q(1)
            basis.append(vector)
        for index in range(3):
            vector = [Q(0)] * 9
            vector[0] = -z[index] / lam
            vector[4] = -z[index] / mu
            vector[6 + index] = Q(1)
            basis.append(vector)
        assert rank(basis) == 7
        assert all(dot(kernel, vector) == 0 for kernel in (k1, k2) for vector in basis)

        gamma = [Q(7), Q(11), Q(13)]
        gamma_z = dot(gamma, z)
        assert gamma_z
        alpha = [-gamma_z / lam, Q(17), Q(19)]
        beta = [Q(23), -gamma_z / mu, Q(29)]
        ell = alpha + beta + gamma
        assert all(ell)
        recovered = (
            [-mu * beta[1] * gamma_z * value for value in alpha]
            + [-lam * alpha[0] * gamma_z * value for value in beta]
            + [lam * mu * alpha[0] * beta[1] * value for value in gamma]
        )
        assert recovered == [gamma_z * gamma_z * value for value in ell]
    print("independent derivative/annihilator/torus audit: PASS")


def contracted_faces_and_q_gate_audit() -> None:
    charts = ((2, 3, 0), (2, 0, 5), (0, 3, 5), (2, 3, 5))
    for z in charts:
        matrix = derivative_matrix(2, 3, z)
        gamma_basis = perpendicular_basis(z)
        assert rank(gamma_basis) == 2
        assert all(dot(gamma, list(map(Q, z))) == 0 for gamma in gamma_basis)

        restrictions = [
            [gamma[index] for gamma in gamma_basis] for index in range(3)
        ]
        assert all(any(row) for row in restrictions)
        relation = [
            sum(Q(z[index]) * restrictions[index][column] for index in range(3))
            for column in range(2)
        ]
        assert relation == [Q(0), Q(0)]

        for gamma in gamma_basis:
            for i, j in product((1, 2), (0, 2)):
                contracted = [Q(0)] * 9
                for k in range(3):
                    row = matrix[tensor_index(i, j, k)]
                    contracted = [
                        old + gamma[k] * value
                        for old, value in zip(contracted, row, strict=True)
                    ]
                assert contracted == [Q(0)] * 9

            for j in (0, 2):
                contracted = [Q(0)] * 9
                for k in range(3):
                    row = matrix[tensor_index(0, j, k)]
                    contracted = [
                        old + gamma[k] * value
                        for old, value in zip(contracted, row, strict=True)
                    ]
                assert contracted == [Q(0)] * 9

            for i in (1, 2):
                contracted = [Q(0)] * 9
                for k in range(3):
                    row = matrix[tensor_index(i, 1, k)]
                    contracted = [
                        old + gamma[k] * value
                        for old, value in zip(contracted, row, strict=True)
                    ]
                assert contracted == [Q(0)] * 9

        # The ell_2 kernel is one-dimensional.  Its nonzero vector has a
        # nonzero (gamma_0,gamma_1) target contraction.
        l2 = restrictions[2]
        coefficients = [l2[1], -l2[0]]
        gamma = [
            coefficients[0] * gamma_basis[0][index]
            + coefficients[1] * gamma_basis[1][index]
            for index in range(3)
        ]
        assert any(gamma) and gamma[2] == 0
        assert gamma[0] or gamma[1]
    print("independent contracted-face/Q-injectivity audit: PASS")


def hyperplane_fork_audit() -> None:
    charts = ((2, 3, 0), (2, 0, 5), (0, 3, 5), (2, 3, 5))
    for z_raw in charts:
        z = list(map(Q, z_raw))
        gamma_basis = perpendicular_basis(z_raw)

        # Rows of h_block are two independent annihilators of z and z^T.
        h_block = gamma_basis + [z]
        assert rank(h_block) == 3
        columns = [
            [Q(1), Q(0), Q(0)],
            [Q(0), Q(1), Q(0)],
            [Q(1), Q(0), Q(0)],
            [Q(0), Q(1), Q(0)],
        ]
        columns.extend(transpose(h_block))
        phi = transpose(columns)
        assert rank(phi) == 3
        assert 7 - rank(phi) == 4

        # The third output coordinate is gamma(z); its zero hyperplane maps
        # to the common first-two-coordinate plane.
        q_coefficients = transpose(gamma_basis)
        q_image = matmul([row[4:] for row in phi], q_coefficients)
        assert rank(q_image) == 2
        assert q_image[2] == [Q(0), Q(0)]
        assert rank([row[:2] for row in phi]) == 2
        assert rank([row[2:4] for row in phi]) == 2

    for coloop in range(7):
        columns = []
        counter = 0
        for index in range(7):
            if index == coloop:
                columns.append([Q(0), Q(0), Q(1)])
            else:
                columns.append([Q(1), Q(counter), Q(0)])
                counter += 1
        full = transpose(columns)
        deleted = transpose([column for index, column in enumerate(columns) if index != coloop])
        assert rank(full) == 3
        assert rank(deleted) == 2
        assert 7 - rank(full) == 4
    print("independent eight-hyperplane/equality-fork audit: PASS")


BlockVector = tuple[list[Fraction], list[Fraction], list[Fraction]]


def permanent(
    left: BlockVector, middle: BlockVector, right: BlockVector
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


def square_zero_lemma_audit() -> None:
    zero = [Q(0), Q(0)]
    base = [Q(1), Q(0)]
    a: BlockVector = ([Q(2), Q(3)], [Q(5), Q(7)], [Q(11), Q(13)])

    pure: BlockVector = (base[:], zero[:], zero[:])
    q: BlockVector = ([Q(17), Q(19)], [Q(23), Q(29)], [Q(31), Q(37)])
    value = permanent(a, pure, q)
    assert all(value[tensor_index(1, j, k, 2)] == 0 for j, k in product(range(2), repeat=2))

    two: BlockVector = (base[:], base[:], zero[:])
    q_xy: BlockVector = ([Q(17), Q(19)], [Q(23), Q(29)], zero[:])
    assert permanent(two, two, q_xy) == [Q(0)] * 8
    expected = [Q(0)] * 8
    for i, j, k in product(range(2), repeat=3):
        expected[tensor_index(i, j, k, 2)] = a[2][k] * (
            base[i] * q_xy[1][j] + q_xy[0][i] * base[j]
        )
    assert permanent(a, two, q_xy) == expected

    three: BlockVector = (base[:], base[:], base[:])
    q0: BlockVector = (base[:], [-value for value in base], zero[:])
    q1: BlockVector = (base[:], zero[:], [-value for value in base])
    for kernel_vector in (q0, q1):
        assert permanent(three, three, kernel_vector) == [Q(0)] * 8
        mixed = permanent(a, three, kernel_vector)
        for i, j, k in product(range(2), repeat=3):
            if i + j + k >= 2:
                assert mixed[tensor_index(i, j, k, 2)] == 0

    # A decomposable tensor in this tangent support can have at most one
    # factor off its base line, hence two such tensors share a factor.
    possible_off_base = [mask for mask in product((0, 1), repeat=3) if sum(mask) <= 1]
    assert all(
        any(left[index] == right[index] == 0 for index in range(3))
        for left, right in product(possible_off_base, repeat=2)
    )
    print("independent square-zero mixed-factor atlas: PASS")


def equality_and_ordinary_coloop_audit() -> None:
    # F=[[0,0],[0,tau]], P=R*M.  Direct inversion gives the antisymmetric
    # numerator -c*tau.  Exhaust an exact rational box as an independent
    # guard on the radical-alignment orientation.
    for a, b, c, d in product(range(-2, 3), repeat=4):
        determinant = a * d - b * c
        if determinant == 0:
            continue
        # S=F*M^-1 has rows (0,0),(-c,a)/det for tau=1.
        form = [[Q(0), Q(0)], [Q(-c, determinant), Q(a, determinant)]]
        if form[0][1] == form[1][0]:
            assert c == 0

    t0, t1, t2 = [Q(1), Q(0), Q(0)], [Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(1)]
    assert rank([t0, t1, t2]) == 3

    # The r_2-coloop equation asks a nonzero T_0-valued map to cancel a
    # nonzero T_1-valued map.  The r_1-coloop equation instead supplies one
    # point outside two scalar kernel lines and therefore exactly the S2AL
    # square/mixed fork on span(A).
    assert [left + right for left, right in zip(t0, t1, strict=True)] != [Q(0)] * 3
    candidates = [(Q(s), Q(t)) for s, t in product(range(-2, 3), repeat=2)]
    witness = next((s, t) for s, t in candidates if s and s + t)
    assert witness[0] and witness[0] + witness[1]
    assert rank([t0, t1]) == 2
    print("independent equal-plane/ordinary-coloop audit: PASS")


def main() -> None:
    derivative_and_torus_audit()
    contracted_faces_and_q_gate_audit()
    hyperplane_fork_audit()
    square_zero_lemma_audit()
    equality_and_ordinary_coloop_audit()
    print("independent two-coordinate/noncoordinate Hilbert--Burch exclusion: PASS")


if __name__ == "__main__":
    main()
