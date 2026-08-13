"""Independent no-import audit of the support-two double-monomial exclusion."""

from fractions import Fraction
from itertools import permutations

Q = Fraction


def basis(index):
    return tuple(Q(int(index == j)) for j in range(3))


def zero(size):
    return tuple(Q(0) for _ in range(size))


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors))


def scale(value, vector):
    return tuple(Q(value) * entry for entry in vector)


def source(group, vector):
    values = [Q(0) for _ in range(9)]
    values[3 * group : 3 * group + 3] = vector
    return tuple(values)


def split(vector):
    return vector[:3], vector[3:6], vector[6:9]


def tensor3(x, y, z):
    return tuple(a * b * c for a in x for b in y for c in z)


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return Q(-1 if inversions % 2 else 1)


def polarized(u, v, q):
    forms = (split(u), split(v), split(q))
    result = zero(27)
    for permutation in permutations(range(3)):
        term = tensor3(
            forms[permutation[0]][0],
            forms[permutation[1]][1],
            forms[permutation[2]][2],
        )
        result = add(result, term)
    return result


def alternating(u, v, w):
    forms = (split(u), split(v), split(w))
    result = zero(27)
    for permutation in permutations(range(3)):
        term = tensor3(
            forms[permutation[0]][0],
            forms[permutation[1]][1],
            forms[permutation[2]][2],
        )
        result = add(result, scale(parity(permutation), term))
    return result


def columns_to_rows(columns):
    return [list(entries) for entries in zip(*columns)]


def matrix_rank(rows):
    work = [list(row) for row in rows if any(row)]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][j] - factor * work[pivot_row][j]
                for j in range(len(work[row]))
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def linear_rows(u, v):
    columns = []
    for index in range(9):
        column = [Q(0) for _ in range(9)]
        column[index] = Q(1)
        columns.append(polarized(u, v, tuple(column)))
    return columns_to_rows(columns)


def common_nullity(v2, *directions):
    rows = []
    for direction in directions:
        rows.extend(linear_rows(v2, direction))
    return 9 - matrix_rank(rows)


def pair(u, v):
    return tuple(a * b for a in u for b in v)


def derivative(b23, b13):
    columns = []
    for index in range(3):
        columns.append(tuple(a * b for a in basis(index) for b in b23))
    for middle in range(3):
        column = [Q(0) for _ in range(27)]
        for first in range(3):
            for third in range(3):
                column[9 * first + 3 * middle + third] = b13[3 * first + third]
        columns.append(tuple(column))
    columns.extend(zero(27) for _ in range(3))
    return columns


def matvec(columns, vector):
    return tuple(
        sum((vector[j] * columns[j][i] for j in range(len(columns))), Q(0))
        for i in range(len(columns[0]))
    )


def audit_canonical_plane():
    e0, e1, e2 = basis(0), basis(1), basis(2)
    d_columns = derivative(pair(e0, e0), pair(e1, e1))
    assert matrix_rank(columns_to_rows(d_columns)) == 6

    p0 = add(source(0, e0), source(1, zero(3)), source(2, zero(3)))
    p1 = add(source(0, zero(3)), source(1, e1), source(2, zero(3)))
    p2 = add(source(0, e2), source(1, scale(2, e2)), source(2, zero(3)))
    n0 = source(2, add(e0, scale(-1, e1)))
    n1 = source(2, e2)
    image = [p0, p1, p2, n0, n1]
    assert matrix_rank(columns_to_rows(image)) == 5

    singleton = [matvec(d_columns, column) for column in (p0, p1, p2)]
    assert matrix_rank(columns_to_rows(singleton)) == 3
    assert matrix_rank(columns_to_rows([matvec(d_columns, column) for column in image])) == 3
    print("independent canonical-plane audit: PASS (joint 5 / singleton 3)")


def audit_two_source_atlas():
    x = source(0, basis(1))
    y = source(1, basis(2))
    t = source(2, basis(1))
    v2 = add(x, y)
    w = add(x, scale(-1, y))

    nonconjugate = source(1, basis(0))
    assert common_nullity(v2, nonconjugate, t) == 1

    tangent = source(1, basis(0))
    q1 = add(tangent, t)
    assert common_nullity(v2, w, q1) == 2

    z0 = source(2, basis(0))
    z1 = source(2, basis(2))
    u0 = add(scale(2, w), z0)
    u1 = add(scale(3, w), z1)
    first = polarized(u0, u1, w)
    expected = scale(
        -2,
        tensor3(
            basis(1),
            basis(2),
            add(scale(2, basis(2)), scale(3, basis(0))),
        ),
    )
    assert first == expected
    assert polarized(u0, u1, t) == scale(
        -12, tensor3(basis(1), basis(2), basis(1))
    )
    expected_alt = scale(
        2,
        tensor3(
            basis(1),
            basis(2),
            add(scale(3, basis(0)), scale(-2, basis(2))),
        ),
    )
    assert alternating(u0, u1, v2) == expected_alt
    print("independent two-source audit: PASS (three zero-divisor cases)")


def audit_three_source_atlas():
    x = source(0, basis(2))
    y = source(1, basis(0))
    z = source(2, basis(1))
    v2 = add(x, y, z)

    q_all = add(x, scale(2, y), scale(-3, z))
    u0 = add(scale(2, x), scale(-1, y))
    u1 = add(scale(3, x), z)
    assert polarized(u0, v2, q_all) == zero(27)
    assert polarized(u1, v2, q_all) == zero(27)
    assert alternating(u0, u1, v2) == zero(27)

    q_zero = add(y, scale(-1, z))
    independent_target = source(2, basis(2))
    assert common_nullity(v2, q_zero, independent_target) == 1

    proportional_target = add(x, scale(-1, y), z)
    assert common_nullity(v2, q_zero, proportional_target) == 3
    assert alternating(source(0, basis(0)), source(0, basis(1)), v2) == zero(27)
    print("independent three-source audit: PASS (scaling / independent / pure)")


def audit_sharp_fixture():
    x0 = source(0, basis(0))
    y0 = source(1, basis(0))
    z0 = source(2, basis(0))
    v0 = source(2, basis(2))
    v1 = source(2, basis(1))
    v2 = add(x0, y0)
    q0 = add(x0, scale(-1, y0))
    q1 = scale(Q(1, 2), z0)
    forms = [v0, v1, v2, q0, q1]
    assert matrix_rank(columns_to_rows(forms)) == 5

    for left, right in ((v0, v1), (v0, v2), (v1, v2)):
        assert polarized(left, right, q0) == zero(27)
        assert polarized(left, right, q1) == zero(27)
    assert polarized(v2, v2, q0) == zero(27)
    assert polarized(v2, v2, q1) == tensor3(basis(0), basis(0), basis(0))
    assert alternating(v0, v1, v2) == zero(27)

    # Use the colour-permuted canonical physical rows.  The empty permanent
    # is exactly the missing-colour target coefficient; the other two target
    # coefficients are the two monomial singleton-span basis vectors.
    root_1 = [v2, v0, zero(9)]
    root_2 = [v2, zero(9), v1]
    root_3 = [q1, q0, scale(-1, q0)]
    empty = [
        polarized(root_1[a], root_2[b], root_3[c])
        for a in range(3)
        for b in range(3)
        for c in range(3)
    ]
    assert [index for index, value in enumerate(empty) if value != zero(27)] == [0]
    assert empty[0] == tensor3(basis(0), basis(0), basis(0))
    print("independent sharpness audit: PASS (rank five without singleton determinant)")


def main():
    audit_canonical_plane()
    audit_two_source_atlas()
    audit_three_source_atlas()
    audit_sharp_fixture()
    print("independent support-two double-monomial exclusion: PASS")


if __name__ == "__main__":
    main()
