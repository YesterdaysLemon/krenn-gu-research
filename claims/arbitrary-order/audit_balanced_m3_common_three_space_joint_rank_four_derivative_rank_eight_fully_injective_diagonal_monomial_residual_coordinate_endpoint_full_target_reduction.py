#!/usr/bin/env python3
"""Independent no-import Fraction audit of the diagonal endpoint reduction."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction


def unit(size: int, index: int) -> tuple[Q, ...]:
    return tuple(Q(int(i == index)) for i in range(size))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(scalar: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(scalar * value for value in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def cross(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def outer(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(a * b for b in right) for a in left)


def matrix_subtract(
    left: tuple[tuple[Q, ...], ...],
    right: tuple[tuple[Q, ...], ...],
) -> tuple[tuple[Q, ...], ...]:
    return tuple(
        tuple(a - b for a, b in zip(row_a, row_b, strict=True))
        for row_a, row_b in zip(left, right, strict=True)
    )


def deterministic_vector(seed: int, offset: int) -> tuple[Q, ...]:
    return tuple(Q((seed + 2) * (i + 1) + offset, i + 2) for i in range(6))


def vector_rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
    matrix = [list(row) for row in zip(*vectors, strict=True)]
    rows = len(matrix)
    columns = len(vectors)
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                matrix[row][j] - factor * matrix[rank][j]
                for j in range(columns)
            ]
        rank += 1
    return rank


def check_numeric_full_identity() -> None:
    targets = tuple(unit(6, i) for i in range(3))
    sources = tuple(unit(6, 3 + i) for i in range(3))
    zero = tuple(Q(0) for _ in range(6))

    for seed in range(1, 6):
        lam = Q(seed + 2, seed + 1)
        x = (Q(seed), Q(seed + 1), Q(2 - seed))
        y = (Q(seed + 2), Q(1 - seed), Q(seed + 3))
        a = tuple(
            tuple(Q((c + 1) * (i + 2) + seed, c + i + 2) for i in range(3))
            for c in range(3)
        )
        b = tuple(
            tuple(Q((c + 2) * (i + 1) - seed, c + i + 3) for i in range(3))
            for c in range(3)
        )
        h = tuple(matrix_subtract(outer(a[c], y), outer(x, b[c])) for c in range(3))

        shifted_h = []
        for c in range(3):
            t = Q(seed + c + 1, c + 2)
            shifted_a = add(a[c], scale(t, x))
            shifted_b = add(b[c], scale(t, y))
            shifted_h.append(matrix_subtract(outer(shifted_a, y), outer(x, shifted_b)))
        assert tuple(shifted_h) == h

        p = [[[zero for _ in range(3)] for _ in range(3)] for _ in range(3)]
        for i, j, k in product(range(3), repeat=3):
            pieces = []
            if i == j == k:
                pieces.append(targets[i])
            if k == 0:
                pieces.extend(scale(h[c][i][j], sources[c]) for c in range(3))
            if i == 2 and j == 2:
                pieces.append(scale(lam, sources[k]))
            p[i][j][k] = add(*pieces) if pieces else zero

            direct = []
            if i == j == k:
                direct.append(targets[i])
            for c in range(3):
                coefficient = Q(int(k == 0)) * (
                    a[c][i] * y[j] - x[i] * b[c][j]
                )
                coefficient += lam * Q(int(i == 2 and j == 2 and k == c))
                direct.append(scale(coefficient, sources[c]))
            assert p[i][j][k] == add(*direct)

        recovered_1 = scale(1 / lam, p[2][2][1])
        recovered_2 = scale(1 / lam, add(p[2][2][2], scale(-1, targets[2])))
        assert recovered_1 == sources[1]
        assert recovered_2 == sources[2]

        c_matrix = tuple(
            tuple(lam if i == j == 2 else Q(0) for j in range(3))
            for i in range(3)
        )
        kappa = tuple(
            tuple(c_matrix[i][j] + h[0][i][j] for j in range(3))
            for i in range(3)
        )
        residual = [[zero for _ in range(3)] for _ in range(3)]
        for i, j in product(range(3), repeat=2):
            value = p[i][j][0]
            if i == j == 0:
                value = add(value, scale(-1, targets[0]))
            value = add(
                value,
                scale(-h[1][i][j], recovered_1),
                scale(-h[2][i][j], recovered_2),
            )
            residual[i][j] = value
            assert value == scale(kappa[i][j], sources[0])

        for i, j, m, n in product(range(3), repeat=4):
            minor = add(
                scale(kappa[m][n], residual[i][j]),
                scale(-kappa[i][j], residual[m][n]),
            )
            assert minor == zero


def check_retained_faces_and_omission_control() -> None:
    targets = tuple(unit(6, i) for i in range(3))
    sources = tuple(unit(6, 3 + i) for i in range(3))
    zero = tuple(Q(0) for _ in range(6))
    lam = Q(5, 2)
    faces = {
        1: [[zero for _j in range(3)] for _i in range(3)],
        2: [[zero for _j in range(3)] for _i in range(3)],
    }
    faces[1][1][1] = targets[1]
    faces[1][2][2] = scale(lam, sources[1])
    faces[2][2][2] = add(targets[2], scale(lam, sources[2]))

    recovered_1 = scale(1 / lam, faces[1][2][2])
    recovered_2 = scale(
        1 / lam,
        add(faces[2][2][2], scale(-1, targets[2])),
    )
    assert recovered_1 == sources[1]
    assert recovered_2 == sources[2]

    retained = 0
    for k in reversed((1, 2)):
        for j, i in product(reversed(range(3)), repeat=2):
            if (i, j) == (2, 2):
                continue
            expected = targets[k] if i == j == k else zero
            assert faces[k][i][j] == expected
            retained += 1
    assert retained == 16

    perturbation = sources[0]
    perturbed = {
        k: [[faces[k][i][j] for j in range(3)] for i in range(3)]
        for k in (1, 2)
    }
    perturbed[1][1][1] = add(perturbed[1][1][1], perturbation)
    assert scale(1 / lam, perturbed[1][2][2]) == recovered_1
    perpendicular = (unit(3, 2), unit(3, 0))
    for beta, alpha in product(perpendicular, repeat=2):
        delta = zero
        for j, i in product(reversed(range(3)), repeat=2):
            delta = add(
                delta,
                scale(
                    alpha[i] * beta[j],
                    add(
                        perturbed[1][i][j],
                        scale(-1, faces[1][i][j]),
                    ),
                ),
            )
        assert delta == zero
    assert add(perturbed[1][1][1], scale(-1, targets[1])) == perturbation


def check_reversed_contractions() -> None:
    targets = tuple(unit(6, i) for i in range(3))
    sources = tuple(unit(6, 3 + i) for i in range(3))
    zero = tuple(Q(0) for _ in range(6))
    lam = Q(7, 3)

    for seed in range(1, 8):
        x = (Q(seed), Q(seed + 1), Q(seed + 2))
        y = (Q(seed + 3), Q(2 * seed + 1), Q(1 - seed))
        alpha = cross(x, (Q(1), Q(seed), Q(seed + 4)))
        beta = cross(y, (Q(seed + 2), Q(3), Q(1)))
        assert dot(alpha, x) == 0
        assert dot(beta, y) == 0

        a = tuple(
            tuple(Q(seed + c + i + 1, i + 2) for i in range(3))
            for c in range(3)
        )
        b = tuple(
            tuple(Q(2 * seed - c + i, c + 2) for i in range(3))
            for c in range(3)
        )
        h = tuple(matrix_subtract(outer(a[c], y), outer(x, b[c])) for c in range(3))

        for k in reversed(range(3)):
            contracted = zero
            for i, j in product(reversed(range(3)), repeat=2):
                pieces = []
                if i == j == k:
                    pieces.append(targets[k])
                if k == 0:
                    pieces.extend(scale(h[c][i][j], sources[c]) for c in range(3))
                if i == 2 and j == 2:
                    pieces.append(scale(lam, sources[k]))
                value = add(*pieces) if pieces else zero
                contracted = add(contracted, scale(alpha[i] * beta[j], value))
            expected = add(
                scale(alpha[k] * beta[k], targets[k]),
                scale(lam * alpha[2] * beta[2], sources[k]),
            )
            assert contracted == expected


def perpendicular_basis(vector: tuple[Q, ...]) -> tuple[tuple[Q, ...], ...]:
    first = (vector[1], -vector[0], Q(0))
    pivot = 0 if vector[0] else 1
    second = [Q(0), Q(0), Q(1)]
    second[pivot] = -vector[2] / vector[pivot]
    result = first, tuple(second)
    assert first != (Q(0), Q(0), Q(0))
    assert all(dot(row, vector) == 0 for row in result)
    return result


def is_coordinate(vector: tuple[Q, ...], coordinate: int) -> bool:
    return all(vector[i] == 0 for i in range(3) if i != coordinate)


def check_support_census() -> None:
    representatives = []
    for mask in range(1, 8):
        vector = tuple(Q(int(bool(mask & (1 << i)))) for i in range(3))
        if vector != (Q(0), Q(0), Q(1)):
            representatives.append(vector)
    assert len(representatives) == 6

    for y, x in product(reversed(representatives), repeat=2):
        alpha = perpendicular_basis(x)
        beta = perpendicular_basis(y)
        actual = []
        for k in reversed(range(3)):
            values = (
                alpha[0][k] * beta[0][k],
                alpha[0][k] * beta[1][k],
                alpha[1][k] * beta[0][k],
            )
            actual.append(any(value for value in values))
        actual.reverse()
        expected = [
            not is_coordinate(x, 0)
            and not is_coordinate(y, 0)
            and bool(x[1] or y[1]),
            not is_coordinate(x, 1)
            and not is_coordinate(y, 1)
            and bool(x[0] or y[0]),
            False,
        ]
        assert actual == expected


def check_two_radical_interface() -> None:
    def quadratic(vector: tuple[Q, Q, Q]) -> Q:
        s, t, u = vector
        return s * t + s * u + t * u

    for seed in range(1, 9):
        left = (Q(seed), Q(seed + 1), Q(-2 * seed - 1))
        right = (Q(2 - seed), Q(seed + 3), Q(-5))
        assert sum(left, Q(0)) == 0
        assert sum(right, Q(0)) == 0
        polar = (
            left[0] * right[1]
            + left[0] * right[2]
            + right[0] * left[1]
            + left[1] * right[2]
            + right[0] * left[2]
            + right[1] * left[2]
        )
        summed = tuple(left[i] + right[i] for i in range(3))
        assert polar == quadratic(summed) - quadratic(left) - quadratic(right)

    gram = ((Q(-2), Q(-1)), (Q(-1), Q(-2)))
    assert gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0] == 3

    for x0, x1, y0, y1 in product((Q(1), Q(2)), repeat=4):
        alpha_zero = (x1, -x0, Q(0))
        beta_zero = (y1, -y0, Q(0))
        assert alpha_zero[0] * beta_zero[0] == x1 * y1
        assert alpha_zero[1] * beta_zero[1] == x0 * y0
        assert alpha_zero[2] * beta_zero[2] == 0

    pure_x, pure_y = unit(9, 0), unit(9, 3)
    support_two = add(pure_x, pure_y)
    row_a = tuple(Q(i + 1, i + 2) for i in range(9))
    row_b = tuple(Q(2 * i + 3, i + 4) for i in range(9))

    expected_two = tuple(Q(0) for _ in range(27))
    for k in range(3):
        expected_two = add(
            expected_two,
            scale(2 * row_a[6 + k], source_tensor(0, 0, k)),
        )
    assert polarized_product(support_two, row_a, support_two) == expected_two

    expected_square = tuple(Q(0) for _ in range(27))
    expected_cross = tuple(Q(0) for _ in range(27))
    for j, k in product(range(3), repeat=2):
        expected_square = add(
            expected_square,
            scale(
                2 * row_a[3 + j] * row_a[6 + k],
                source_tensor(0, j, k),
            ),
        )
        expected_cross = add(
            expected_cross,
            scale(
                row_a[3 + j] * row_b[6 + k]
                + row_b[3 + j] * row_a[6 + k],
                source_tensor(0, j, k),
            ),
        )
    assert polarized_product(pure_x, row_a, row_a) == expected_square
    assert polarized_product(pure_x, row_a, row_b) == expected_cross

    for x0, x1, y0, y1 in product((Q(1), Q(3)), repeat=4):
        alpha_zero = (x1, -x0, Q(0))
        beta_zero = (y1, -y0, Q(0))
        alpha_one = beta_one = (Q(0), Q(0), Q(1))
        for k in reversed(range(3)):
            assert alpha_zero[k] * beta_one[k] == 0
            assert alpha_one[k] * beta_zero[k] == 0
        assert alpha_zero[0] * beta_zero[0] == x1 * y1
        assert alpha_zero[1] * beta_zero[1] == x0 * y0


def source_tensor(left: int, middle: int, right: int) -> tuple[Q, ...]:
    return unit(27, 9 * left + 3 * middle + right)


def polarized_product(
    first: tuple[Q, ...],
    second: tuple[Q, ...],
    third: tuple[Q, ...],
) -> tuple[Q, ...]:
    rows = (first, second, third)
    result = tuple(Q(0) for _ in range(27))
    for sigma in reversed(tuple(permutations(range(3)))):
        x = rows[sigma[0]][:3]
        y = rows[sigma[1]][3:6]
        z = rows[sigma[2]][6:9]
        term = tuple(Q(0) for _ in range(27))
        for i, j, k in product(range(3), repeat=3):
            coefficient = x[i] * y[j] * z[k]
            if coefficient:
                term = add(term, scale(coefficient, source_tensor(i, j, k)))
        result = add(result, term)
    return result


def check_sharp_control() -> None:
    x0, y0, z0 = unit(9, 0), unit(9, 3), unit(9, 6)
    rows_r = y0, z0
    rows_p = z0, y0
    rows_q = x0, y0, z0
    targets = tuple(source_tensor(i, i, i) for i in range(3))
    zero = tuple(Q(0) for _ in range(27))
    lam = Q(5, 2)
    sources = scale(1 / lam, targets[0]), zero, scale(-1 / lam, targets[2])
    coefficients = ((Q(1), Q(0)), (Q(0), Q(0)), (Q(0), Q(1)))
    nonzero = []

    for k, b, a in product(reversed(range(3)), reversed(range(2)), reversed(range(2))):
        got = polarized_product(rows_r[a], rows_p[b], rows_q[k])
        expected = scale(coefficients[k][a] * coefficients[k][b], targets[k])
        if a == b == 1:
            expected = add(expected, scale(lam, sources[k]))
        assert got == expected
        if got != zero:
            nonzero.append((a, b, k))
    assert sorted(nonzero) == [(0, 0, 0), (1, 1, 0)]
    assert vector_rank(rows_q) == 3
    assert vector_rank(rows_r) == 2
    assert vector_rank(rows_p) == 2


def check_flattening_converse() -> None:
    zero = tuple(Q(0) for _ in range(6))
    for pivot in reversed(range(9)):
        kappa = [Q(i + 2, i + 3) for i in range(9)]
        kappa[pivot] = Q(1)
        residual = [
            deterministic_vector(pivot + i + 2, i + 3)
            for i in range(9)
        ]
        recovered = scale(1 / kappa[pivot], residual[pivot])
        for index in reversed(range(9)):
            minor = add(
                scale(kappa[pivot], residual[index]),
                scale(-kappa[index], residual[pivot]),
            )
            scaled_error = scale(
                kappa[pivot],
                add(residual[index], scale(-kappa[index], recovered)),
            )
            assert scaled_error == minor

        source = deterministic_vector(pivot + 11, 5)
        factorized = [scale(entry, source) for entry in kappa]
        for left, right in product(range(9), repeat=2):
            assert add(
                scale(kappa[right], factorized[left]),
                scale(-kappa[left], factorized[right]),
            ) == zero


def main() -> None:
    check_numeric_full_identity()
    check_retained_faces_and_omission_control()
    check_reversed_contractions()
    check_support_census()
    check_two_radical_interface()
    check_sharp_control()
    check_flattening_converse()
    print("independent sparse/Fraction coefficient audit: PASS")
    print("independent retained-face and omission audit: PASS")
    print("reversed contraction and support audit: PASS")
    print("independent two-radical support audit: PASS")
    print("independent flattening converse and sharpness controls: PASS")


if __name__ == "__main__":
    main()
