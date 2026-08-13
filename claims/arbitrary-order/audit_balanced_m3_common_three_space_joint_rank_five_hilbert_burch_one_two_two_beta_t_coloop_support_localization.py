"""Independent rational audit of the (1,2,2) beta_t-coloop localization."""

from __future__ import annotations

from fractions import Fraction

Vector = list[Fraction]


def basis(i: int, n: int = 3) -> Vector:
    return [Fraction(int(i == j)) for j in range(n)]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction())


def cross(left: Vector, right: Vector) -> Vector:
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def kron(*vectors: Vector) -> Vector:
    out = [Fraction(1)]
    for vector in vectors:
        out = [a * b for a in out for b in vector]
    return out


def matrix_rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][col]
        matrix[rank] = [entry / value for entry in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][col]:
                continue
            value = matrix[row][col]
            matrix[row] = [
                a - value * b
                for a, b in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def derivative_columns(
    y: Vector, z: Vector, w: Vector, s: int, t: int, lam: Fraction, mu: Fraction
) -> list[Vector]:
    et = basis(t)
    es = basis(s)
    block = [a - mu * b for a, b in zip(kron(y, w), kron(et, z), strict=True)]
    columns = [kron(basis(i), block) for i in range(3)]
    columns += [[-lam * value for value in kron(es, basis(j), w)] for j in range(3)]
    columns += [
        [lam * mu * value for value in kron(es, et, basis(k))] for k in range(3)
    ]
    return columns


def transpose_apply(columns: list[Vector], product: Vector) -> Vector:
    return [dot(column, product) for column in columns]


def target_coefficients(alpha: Vector, beta: Vector, gamma: Vector) -> Vector:
    return [alpha[i] * beta[i] * gamma[i] for i in range(3)]


def audit_complete_face() -> None:
    s, t = 0, 2
    lam, mu = Fraction(2), Fraction(3)
    y = [Fraction(1), Fraction(4), Fraction(0)]
    z = [Fraction(2), Fraction(-1), Fraction(5)]
    w = [Fraction(3), Fraction(2), Fraction(7)]
    columns = derivative_columns(y, z, w, s, t, lam, mu)
    gamma_rows = [
        [Fraction(1), Fraction(0), Fraction(-3, 7)],
        [Fraction(0), Fraction(1), Fraction(-2, 7)],
    ]
    assert matrix_rank(gamma_rows) == 2
    for alpha in (basis(0), basis(1), basis(2)):
        for beta in (basis(0), basis(1)):
            for gamma in gamma_rows:
                assert beta[t] == 0 and dot(gamma, w) == 0
                assert transpose_apply(columns, kron(alpha, beta, gamma)) == [
                    Fraction()
                ] * 9
    print("independent beta_t face: PASS")


def audit_two_tables() -> None:
    generic_w = [Fraction(3), Fraction(2), Fraction(7)]
    generic_gamma = [
        [Fraction(1), Fraction(0), Fraction(-3, 7)],
        [Fraction(0), Fraction(1), Fraction(-2, 7)],
    ]
    assert all(dot(gamma, generic_w) == 0 for gamma in generic_gamma)
    for i in (0, 1):
        for j in (0, 1):
            for k, gamma in enumerate(generic_gamma):
                expected = [Fraction()] * 3
                if i == j == k:
                    expected[i] = Fraction(1)
                assert target_coefficients(basis(i), basis(j), gamma) == expected

    boundary_w = [Fraction(3), Fraction(2), Fraction(0)]
    n = [Fraction(2), Fraction(-3), Fraction(0)]
    et = basis(2)
    assert dot(n, boundary_w) == dot(et, boundary_w) == 0
    assert matrix_rank([n, et]) == 2
    for i in (0, 1):
        for j in (0, 1):
            expected = [Fraction()] * 3
            if i == j:
                expected[i] = n[i]
            assert target_coefficients(basis(i), basis(j), n) == expected
            assert target_coefficients(basis(i), basis(j), et) == [Fraction()] * 3
    print("independent beta_t binary tables: PASS")


def audit_ranks_and_auxiliary_faces() -> None:
    s = t = 2
    y = [Fraction(2), Fraction(3), Fraction(0)]
    z = [Fraction(1), Fraction(4), Fraction(5)]
    w = [Fraction(3), Fraction(-2), Fraction(7)]
    u = [y[1], -y[0], Fraction(0)]
    v = cross(z, w)
    assert dot(u, y) == dot(u, basis(t)) == 0
    assert dot(v, z) == dot(v, w) == 0
    assert matrix_rank([y, basis(t), u]) == 3
    assert matrix_rank([z, w, v]) == 3

    columns = derivative_columns(y, z, w, s, t, Fraction(2), Fraction(3))
    for i in (0, 1):
        for gamma in (basis(0), basis(1), basis(2)):
            assert transpose_apply(columns, kron(basis(i), u, gamma)) == [
                Fraction()
            ] * 9
        for beta in (basis(0), basis(1), basis(2)):
            assert transpose_apply(columns, kron(basis(i), beta, v)) == [
                Fraction()
            ] * 9
    assert u[0] * u[1] != 0 and v[0] * v[1] != 0
    for i in range(3):
        assert dot(v, basis(i)) == v[i]

    r0, r1, avec = basis(0), basis(1), basis(2)
    p0 = [Fraction(2), Fraction(-1), Fraction(5)]
    p1 = [Fraction(1), Fraction(3), Fraction(-2)]
    q0 = [Fraction(-1), Fraction(4), Fraction(7)]
    q1 = [Fraction(5), Fraction(1), Fraction(-3)]
    assert matrix_rank([r0, r1, avec, p0, p1, q0, q1]) == 3
    print("independent beta_t ranks/faces: PASS")


def main() -> None:
    audit_complete_face()
    audit_ranks_and_auxiliary_faces()
    audit_two_tables()
    print("independent beta_t-coloop support audit: PASS")


if __name__ == "__main__":
    main()
