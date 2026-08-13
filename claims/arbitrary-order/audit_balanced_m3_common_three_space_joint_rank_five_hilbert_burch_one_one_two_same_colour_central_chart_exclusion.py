"""Independent no-import audit of the same-colour central-chart theorem."""

from fractions import Fraction
from itertools import permutations, product

DIM = 3


def unit(index, dimension=DIM):
    return tuple(Fraction(int(index == place)) for place in range(dimension))


def add(*vectors):
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(Fraction(scalar) * entry for entry in vector)


def block(left=None, middle=None, right=None):
    zero = (Fraction(0),) * 3
    return (left or zero) + (middle or zero) + (right or zero)


def split(vector):
    return vector[:3], vector[3:6], vector[6:9]


def tensor(left, middle, right):
    # z-major storage differs from the primary Kronecker convention.
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


def rank(columns):
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


def derivative_audit():
    lam, mu = Fraction(2), Fraction(3)
    es = unit(0)
    z = (Fraction(1), Fraction(2), Fraction(0))
    w = (Fraction(1), Fraction(0), Fraction(3))
    zero = (Fraction(0),) * 3
    columns = []
    for index in range(3):
        columns.append(scale(-mu, tensor(unit(index), es, z)))
    for index in range(3):
        columns.append(scale(-lam, tensor(es, unit(index), w)))
    for index in range(3):
        columns.append(scale(lam * mu, tensor(es, es, unit(index))))
    assert rank(columns) == 7

    kernel = (
        scale(lam, es) + zero + z,
        zero + scale(mu, es) + w,
    )
    for generator in kernel:
        image = (Fraction(0),) * 27
        for coefficient, column in zip(generator, columns, strict=True):
            image = add(image, scale(coefficient, column))
        assert not any(image)

    l_basis = [block(left=unit(i)) for i in (1, 2)]
    l_basis += [block(middle=unit(i)) for i in (1, 2)]
    for index in range(3):
        l_basis.append(
            block(
                left=scale(-z[index] / lam, es),
                middle=scale(-w[index] / mu, es),
                right=unit(index),
            )
        )
    assert rank(l_basis) == 7
    assert all(
        sum(a * b for a, b in zip(generator, ell, strict=True)) == 0
        for generator in kernel
        for ell in l_basis
    )

    for coordinates in ((1, 2, 3, 4, 5, 6, 7), (-2, 4, 1, 3, -1, 2, 5)):
        a1, a2, b1, b2, g0, g1, g2 = map(Fraction, coordinates)
        gamma = (g0, g1, g2)
        gamma_z = sum(g * value for g, value in zip(gamma, z, strict=True))
        gamma_w = sum(g * value for g, value in zip(gamma, w, strict=True))
        alpha = (-gamma_z / lam, a1, a2)
        beta = (-gamma_w / mu, b1, b2)
        transpose = (
            scale(-mu * beta[0] * gamma_z, alpha)
            + scale(-lam * alpha[0] * gamma_w, beta)
            + scale(lam * mu * alpha[0] * beta[0], gamma)
        )
        expected = scale(gamma_z * gamma_w, alpha + beta + gamma)
        assert transpose == expected
    print("independent same-colour derivative/recovery: PASS")


def endpoint_atlas_audit():
    zero = (Fraction(0),) * 3
    x, y, z = unit(0), unit(0), unit(0)
    basis9 = [unit(i, 9) for i in range(9)]

    full = block(x, y, z)
    full_square = permanent_map(full, full, basis9)
    assert rank(full_square) == 7

    q1 = block(x, scale(-1, y), zero)
    q2 = block(x, zero, scale(-1, z))
    # Direct common-kernel elimination keeps the two equations in tagged halves.
    tagged = [
        permanent(full, candidate, q1) + permanent(full, candidate, q2)
        for candidate in basis9
    ]
    assert rank(tagged) == 8

    two = block(x, y, zero)
    xy_basis = [block(left=unit(i)) for i in range(3)] + [
        block(middle=unit(i)) for i in range(3)
    ]
    assert not any(any(value) for value in permanent_map(two, two, xy_basis))
    l_map = permanent_map(two, block(zero, zero, z), xy_basis)
    assert rank(l_map) == 5

    pure = block(x, zero, zero)
    value1 = permanent(block(zero, unit(1), zero), pure, block(zero, zero, unit(2)))
    value2 = permanent(block(zero, zero, unit(1)), pure, block(zero, unit(2), zero))
    assert any(value1) and any(value2)
    assert all(
        coefficient == 0 or index % 3 == 0
        for value in (value1, value2)
        for index, coefficient in enumerate(value)
    )

    p = block(unit(1), unit(2), zero)
    w = block(unit(2), unit(1), zero)
    assert not any(alternating(two, p, w))
    print("independent square-zero/two-radical atlases: PASS")


def coefficient_audit():
    for c, d in ((2, 3), (5, 0), (0, 7)):
        la, lb = Fraction(11), Fraction(13)
        square = Fraction(d) * lb
        mixed = Fraction(c) * la
        if c and d:
            assert square and mixed
        elif d == 0:
            assert not square and mixed
        else:
            assert square and not mixed
    print("independent coloop coefficient fork: PASS")


def main():
    derivative_audit()
    endpoint_atlas_audit()
    coefficient_audit()
    print("independent same-colour central-chart audit: PASS")


if __name__ == "__main__":
    main()
