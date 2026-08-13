"""Independent no-import audit of the double-repeated intersection theorem."""

from fractions import Fraction
from itertools import permutations, product

DIM = 3


def unit(index, dimension=DIM):
    return tuple(Fraction(int(position == index)) for position in range(dimension))


def add(*vectors):
    return tuple(sum(values, Fraction(0)) for values in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(Fraction(scalar) * value for value in vector)


def block(left=None, middle=None, right=None):
    zero = (Fraction(0),) * DIM
    return (left or zero) + (middle or zero) + (right or zero)


def split(vector):
    return vector[:3], vector[3:6], vector[6:9]


def tensor(left, middle, right):
    # Reverse-flat storage is intentionally different from the primary replay.
    answer = [Fraction(0)] * 27
    for i, j, k in product(range(3), repeat=3):
        answer[k * 9 + j * 3 + i] += left[i] * middle[j] * right[k]
    return tuple(answer)


def permanent(left, middle, right):
    rows = (split(left), split(middle), split(right))
    answer = (Fraction(0),) * 27
    for order in permutations(range(3)):
        answer = add(
            answer,
            tensor(rows[order[0]][0], rows[order[1]][1], rows[order[2]][2]),
        )
    return answer


def alternating(first, second, third):
    rows = (split(first), split(second), split(third))
    answer = (Fraction(0),) * 27
    for order in permutations(range(3)):
        inversions = sum(
            order[i] > order[j] for i in range(3) for j in range(i + 1, 3)
        )
        term = tensor(rows[order[0]][0], rows[order[1]][1], rows[order[2]][2])
        answer = add(answer, scale((-1) ** inversions, term))
    return answer


def matrix_rank_from_columns(columns):
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [entry / divisor for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(
                    rows[row], rows[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def permanent_map(left, middle, basis):
    return [permanent(left, middle, vector) for vector in basis]


def root_tensor(left, middle, right):
    return tensor(left, middle, right)


def derivative_audit():
    lam, mu, nu, xi = map(Fraction, (2, 3, 5, 7))
    es, et = unit(0), unit(1)
    zero = (Fraction(0),) * 3
    columns = []
    for index in range(3):
        columns.append(scale(-mu * nu, root_tensor(unit(index), et, et)))
    for index in range(3):
        columns.append(scale(-lam * xi, root_tensor(es, unit(index), es)))
    for index in range(3):
        columns.append(scale(lam * mu, root_tensor(es, et, unit(index))))
    assert matrix_rank_from_columns(columns) == 7

    kernel = (
        scale(lam, es) + zero + scale(nu, et),
        zero + scale(mu, et) + scale(xi, es),
    )
    for generator in kernel:
        image = (Fraction(0),) * 27
        for coefficient, column in zip(generator, columns, strict=True):
            image = add(image, scale(coefficient, column))
        assert not any(image)

    l_basis = []
    for index in (1, 2):
        l_basis.append(block(left=unit(index)))
    for index in (0, 2):
        l_basis.append(block(middle=unit(index)))
    for index in range(3):
        l_basis.append(
            block(
                left=scale(-nu / lam if index == 1 else 0, es),
                middle=scale(-xi / mu if index == 0 else 0, et),
                right=unit(index),
            )
        )
    assert matrix_rank_from_columns(l_basis) == 7
    assert all(
        sum(a * b for a, b in zip(k, ell, strict=True)) == 0
        for k in kernel
        for ell in l_basis
    )

    samples = (
        (1, 2, 3, 4, 5, 6, 7),
        (-2, 5, 1, -3, 4, -1, 2),
        (7, -1, 6, 2, -5, 3, 1),
    )
    for a1, a2, b0, b2, g0, g1, g2 in samples:
        alpha = (-(nu / lam) * g1, Fraction(a1), Fraction(a2))
        beta = (Fraction(b0), -(xi / mu) * g0, Fraction(b2))
        gamma = tuple(map(Fraction, (g0, g1, g2)))
        transpose = (
            scale(-mu * nu * beta[1] * gamma[1], alpha)
            + scale(-lam * xi * alpha[0] * gamma[0], beta)
            + scale(lam * mu * alpha[0] * beta[1], gamma)
        )
        expected = scale(nu * xi * gamma[0] * gamma[1], alpha + beta + gamma)
        assert transpose == expected
    print("independent derivative/recovery: PASS")


def correction_audit():
    lam, mu, nu, xi = map(Fraction, (2, 3, 5, 7))
    a1, a2, b0, b2, g0, g1, g2 = map(Fraction, (2, -1, 3, 4, -2, 5, 7))
    pr1, pr2, pp0, pp2, ph0, ph1, ph2 = map(
        Fraction, (11, 13, 17, 19, 23, 29, 31)
    )
    alpha0 = -nu * g1 / lam
    beta1 = -xi * g0 / mu
    contraction = (
        a1 * beta1 * g1 * (-mu * nu * pr1)
        + a2 * beta1 * g1 * (-mu * nu * pr2)
        + alpha0 * b0 * g0 * (-lam * xi * pp0)
        + alpha0 * b2 * g0 * (-lam * xi * pp2)
        + alpha0 * beta1 * g0 * (lam * mu * ph0)
        + alpha0 * beta1 * g1 * (lam * mu * ph1)
        + alpha0 * beta1 * g2 * (lam * mu * ph2)
    )
    phi = (
        a1 * pr1
        + a2 * pr2
        + b0 * pp0
        + b2 * pp2
        + g0 * ph0
        + g1 * ph1
        + g2 * ph2
    )
    assert contraction == nu * xi * g0 * g1 * phi
    print("independent coefficient pullback: PASS")


def source_atlas_audit():
    zero = (Fraction(0),) * 3
    x, y, z = unit(0), unit(0), unit(0)
    whole_basis = [unit(i, 9) for i in range(9)]

    full = block(x, y, z)
    assert matrix_rank_from_columns(permanent_map(full, full, whole_basis)) == 7

    two = block(x, y, zero)
    xy_basis = [block(left=unit(i)) for i in range(3)] + [
        block(middle=unit(i)) for i in range(3)
    ]
    assert not any(
        any(column) for column in permanent_map(two, two, xy_basis)
    )
    mixed = permanent_map(two, block(zero, zero, z), xy_basis)
    assert matrix_rank_from_columns(mixed) == 5

    pure = block(x, zero, zero)
    d = block(unit(1), y, z)
    radical = [block(left=unit(i)) for i in range(3)] + [
        block(zero, y, scale(-1, z))
    ]
    assert not any(any(column) for column in permanent_map(pure, d, radical))
    assert matrix_rank_from_columns(permanent_map(d, d, radical)) == 3

    common_p = block(unit(1), y, scale(-1, z))
    common_s = [pure, block(zero, y, z)]
    assert any(alternating(common_s[0], common_s[1], common_p))
    assert not any(
        any(column)
        for column in permanent_map(common_s[1], common_p, radical)
    )
    common_core = permanent_map(common_s[0], common_p, radical)
    assert matrix_rank_from_columns(common_core) == 1
    union_rank = matrix_rank_from_columns(common_s + radical)
    intersection_dimension = 2 + 4 - union_rank
    assert intersection_dimension == 1
    assert not any(permanent(common_s[0], common_p, common_s[0]))
    print("independent square/common-radical atlases: PASS")


def zero_rectangle_audit():
    zero = (Fraction(0),) * 3
    x, y = unit(0), unit(0)
    k = block(x, scale(-1, y), zero)
    external = block(x, y, zero)
    zs = [block(zero, zero, unit(i)) for i in range(3)]
    e_basis = [k, *zs]
    a = zs[2]
    b = add(k, zs[0])
    q_basis = [zs[0], zs[1], add(k, zs[2])]

    assert any(alternating(a, b, external))
    for s in (a, b):
        assert not any(
            any(column) for column in permanent_map(external, s, q_basis)
        )
    assert not any(any(column) for column in permanent_map(a, a, q_basis))
    core = permanent_map(b, a, q_basis)
    assert matrix_rank_from_columns(core) == 1
    assert not any(core[0]) and not any(core[1]) and any(core[2])

    allowed_indices = {k_index * 9 for k_index in range(3)}
    for left, middle, right in product(e_basis, repeat=3):
        value = permanent(left, middle, right)
        assert all(
            coefficient == 0 or index in allowed_indices
            for index, coefficient in enumerate(value)
        )

    # Independent checks of the two possible kernels in the scalar-Z formula.
    identity_columns = [unit(i) for i in range(3)]
    identity_columns.append(unit(2))
    assert matrix_rank_from_columns(identity_columns) == 3
    rank_one_columns = [
        (Fraction(0),) * 3,
        (Fraction(0),) * 3,
        (Fraction(0),) * 3,
        unit(2),
    ]
    assert matrix_rank_from_columns(rank_one_columns) == 1
    print("independent zero-rectangle/correction factor audit: PASS")


def main():
    derivative_audit()
    correction_audit()
    source_atlas_audit()
    zero_rectangle_audit()
    print("independent double-repeated intersection audit: PASS")


if __name__ == "__main__":
    main()
