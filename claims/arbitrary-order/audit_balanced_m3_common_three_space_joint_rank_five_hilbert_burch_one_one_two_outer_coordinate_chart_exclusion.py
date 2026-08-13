"""Independent no-import audit of the (1,1,2) outer-chart theorem."""

from __future__ import annotations

from fractions import Fraction as Q


def basis(i: int, n: int = 3) -> tuple[Q, ...]:
    return tuple(Q(int(j == i)) for j in range(n))


def zero(n: int) -> tuple[Q, ...]:
    return (Q(0),) * n


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(c: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(c * value for value in vector)


def inner(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def kron3(
    left: tuple[Q, ...], middle: tuple[Q, ...], right: tuple[Q, ...]
) -> tuple[Q, ...]:
    return tuple(a * b * c for a in left for b in middle for c in right)


def stack(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(value for vector in vectors for value in vector)


def rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(row, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        divisor = matrix[row][column]
        matrix[row] = [value / divisor for value in matrix[row]]
        for i in range(len(matrix)):
            if i == row or matrix[i][column] == 0:
                continue
            factor = matrix[i][column]
            matrix[i] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[i], matrix[row], strict=True)
            ]
        row += 1
        if row == len(matrix):
            break
    return row


def matvec(columns: list[tuple[Q, ...]], vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(
        sum((columns[j][i] * vector[j] for j in range(len(columns))), Q(0))
        for i in range(len(columns[0]))
    )


def transpose_matvec(
    columns: list[tuple[Q, ...]], vector: tuple[Q, ...]
) -> tuple[Q, ...]:
    return tuple(inner(column, vector) for column in columns)


def derivative_columns(
    y: tuple[Q, ...], z: tuple[Q, ...], s: int, t: int, lam: Q, nu: Q
) -> list[tuple[Q, ...]]:
    es, et = basis(s), basis(t)
    columns = [scale(-1, kron3(basis(i), y, z)) for i in range(3)]
    columns += [scale(-lam * nu, kron3(es, basis(j), et)) for j in range(3)]
    columns += [scale(lam, kron3(es, y, basis(k))) for k in range(3)]
    return columns


def audit_derivative() -> None:
    y = (Q(1), Q(2), Q(3))
    z = (Q(2), Q(4), Q(1))
    s, t, lam, nu = 0, 1, Q(2), Q(3)
    columns = derivative_columns(y, z, s, t, lam, nu)
    assert rank([[column[i] for column in columns] for i in range(27)]) == 7
    k1 = stack(scale(lam, basis(s)), zero(3), z)
    k2 = stack(zero(3), y, scale(nu, basis(t)))
    assert matvec(columns, k1) == zero(27)
    assert matvec(columns, k2) == zero(27)

    for gamma, alpha_tail, beta_tail in (
        ((Q(1), Q(2), Q(5)), (Q(3), Q(7)), (Q(4), Q(6))),
        ((Q(2), Q(-1), Q(3)), (Q(5), Q(-2)), (Q(8), Q(1))),
        ((Q(-3), Q(4), Q(1)), (Q(2), Q(9)), (Q(-5), Q(7))),
    ):
        alpha = (-inner(gamma, z) / lam, *alpha_tail)
        beta0 = (-nu * gamma[t] - y[1] * beta_tail[0] - y[2] * beta_tail[1]) / y[0]
        beta = (beta0, *beta_tail)
        ell = stack(alpha, beta, gamma)
        got = transpose_matvec(columns, kron3(alpha, beta, gamma))
        expected = scale(nu * inner(gamma, z) * gamma[t], ell)
        assert got == expected

    alpha = (Q(0), Q(2), Q(-1))
    beta = (Q(-2), Q(1), Q(0))
    gamma = (Q(3), Q(5), Q(7))
    assert inner(beta, y) == 0
    assert transpose_matvec(columns, kron3(alpha, beta, gamma)) == zero(9)
    print("independent derivative/recovery: PASS")


def cross(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def audit_torus_and_support() -> None:
    for y, z, s, t in (
        ((Q(1), Q(2), Q(3)), (Q(2), Q(4), Q(1)), 0, 1),
        ((Q(0), Q(2), Q(3)), (Q(3), Q(1), Q(4)), 0, 2),
        ((Q(0), Q(2), Q(3)), (Q(1), Q(5), Q(2)), 0, 0),
    ):
        k1 = list(stack(scale(Q(2), basis(s)), zero(3), z))
        k2 = list(stack(zero(3), y, scale(Q(3), basis(t))))
        assert rank([k1, k2]) == 2
        for coordinate in range(9):
            row = [Q(0)] * 9
            row[coordinate] = Q(1)
            assert rank([k1, k2, row]) == 3
        assert rank([list(z), list(basis(t))]) == 2

        a, b = (i for i in range(3) if i != s)
        kinds = []
        for j in range(3):
            beta = cross(y, basis(j))
            assert beta != zero(3)
            kinds.append((beta[a] != 0, beta[b] != 0))
        if y[s] == 0:
            assert set(kinds) == {(True, True), (False, False)}
        else:
            assert (False, False) not in kinds
    print("independent torus/support atlas: PASS")


def pair_add(left: tuple[Q, Q], right: tuple[Q, Q]) -> tuple[Q, Q]:
    return (left[0] + right[0], left[1] + right[1])


def pair_scale(c: Q, pair: tuple[Q, Q]) -> tuple[Q, Q]:
    return (c * pair[0], c * pair[1])


def audit_coefficient_forks() -> None:
    target_a, target_b = (Q(5), Q(0)), (Q(0), Q(7))
    for c, d in ((Q(2), Q(3)), (Q(0), Q(3)), (Q(2), Q(0))):
        square_equal = pair_add(pair_scale(c, target_a), pair_scale(d, target_b))
        assert square_equal == (Q(5) * c, Q(7) * d)

        square_first = pair_scale(d, target_b)
        mixed_first = pair_scale(c, target_a)
        assert square_first == (Q(0), Q(7) * d)
        assert mixed_first == (Q(5) * c, Q(0))

        square_second = pair_scale(c, target_a)
        mixed_second = pair_scale(d, target_b)
        assert square_second == (Q(5) * c, Q(0))
        assert mixed_second == (Q(0), Q(7) * d)
    print("independent coloop coefficient audit: PASS")


def tensor2(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a * b for a in left for b in right)


def audit_endpoint_atlases() -> None:
    x = (Q(1), Q(0))
    y = (Q(0), Q(1))
    c = Q(3)

    plus = pair_add_tensor(tensor2(x, scale(-c, y)), tensor2(scale(c, x), y))
    minus = pair_sub_tensor(tensor2(x, scale(-c, y)), tensor2(scale(c, x), y))
    assert plus == zero(4)
    assert minus == scale(-2 * c, tensor2(x, y))

    # The two-source mixed map has one kernel line.  In coordinates
    # (q_X0,q_X1,q_Y0,q_Y1), its four outputs have rank three.
    # The image is spanned by q_Y0+q_X0, q_Y1, q_X1.
    l_reduced = [
        [Q(1), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(0), Q(1)],
        [Q(0), Q(1), Q(0), Q(0)],
    ]
    assert rank(l_reduced) == 3
    assert matvec([tuple(row[i] for row in l_reduced) for i in range(4)], (Q(1), Q(0), Q(-1), Q(0))) == zero(3)

    # In the pure radical atlas, plus zero forces the alternating tensor
    # onto the single product of the two base lines.
    d_y, d_z = x, y
    p_y, p_z = scale(c, d_y), scale(-c, d_z)
    tangent = pair_add_tensor(tensor2(d_y, p_z), tensor2(p_y, d_z))
    alternating = pair_sub_tensor(tensor2(d_y, p_z), tensor2(p_y, d_z))
    assert tangent == zero(4)
    assert alternating == scale(-2 * c, tensor2(d_y, d_z))
    print("independent endpoint source audit: PASS")


def pair_add_tensor(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return add(left, right)


def pair_sub_tensor(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return add(left, scale(Q(-1), right))


def audit_outer_pair_symmetry() -> None:
    x = (Q(1), Q(2), Q(0))
    y = basis(0)
    z = basis(2)
    w = (Q(2), Q(1), Q(3))
    first = (x, zero(3), z)
    second = (zero(3), y, w)
    swapped_first = (second[1], zero(3), second[2])
    swapped_second = (zero(3), first[0], first[2])
    assert swapped_first == (y, zero(3), w)
    assert swapped_second == (zero(3), x, z)
    assert swapped_first[0] == y and swapped_second[2] == z
    print("independent outer-pair symmetry: PASS")


def main() -> None:
    audit_derivative()
    audit_torus_and_support()
    audit_coefficient_forks()
    audit_endpoint_atlases()
    audit_outer_pair_symmetry()
    print("independent outer-coordinate-chart audit: PASS")


if __name__ == "__main__":
    main()
