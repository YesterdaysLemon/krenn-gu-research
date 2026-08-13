"""Independent no-import audit of the joint-rank-five localization."""

from fractions import Fraction
from itertools import product

Q = Fraction


def basis(i):
    return tuple(Q(int(j == i)) for j in range(3))


def zero(n):
    return tuple(Q(0) for _ in range(n))


def add(u, v):
    return tuple(a + b for a, b in zip(u, v))


def sub(u, v):
    return tuple(a - b for a, b in zip(u, v))


def kron(u, v):
    return tuple(a * b for a in u for b in v)


def outer(u, v):
    return kron(u, v)


def columns_to_rows(columns):
    return [[column[i] for column in columns] for i in range(len(columns[0]))]


def matrix_rank(rows):
    work = [list(row) for row in rows]
    if not work:
        return 0
    nrows = len(work)
    ncols = len(work[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for r in range(nrows):
            if r == pivot_row or not work[r][column]:
                continue
            factor = work[r][column]
            work[r] = [
                work[r][c] - factor * work[pivot_row][c] for c in range(ncols)
            ]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def matvec(rows, vector):
    return tuple(sum(entry * value for entry, value in zip(row, vector)) for row in rows)


def derivative(b23, b13, b12):
    columns = []
    for i in range(3):
        columns.append(kron(basis(i), b23))
    for j in range(3):
        column = [Q(0) for _ in range(27)]
        for i in range(3):
            for k in range(3):
                column[9 * i + 3 * j + k] = b13[3 * i + k]
        columns.append(tuple(column))
    for k in range(3):
        columns.append(kron(b12, basis(k)))
    return columns_to_rows(columns)


def hb_blocks(x, y, z, b, c, w):
    return (
        sub(outer(y, w), outer(c, z)),
        sub(outer(b, z), outer(x, w)),
        sub(outer(x, c), outer(b, y)),
    )


def vstack(*vectors):
    return tuple(value for vector in vectors for value in vector)


def audit_derivative_profiles():
    e0, e1 = basis(0), basis(1)
    shared = derivative(outer(e0, e0), outer(e0, e0), zero(9))
    transverse = derivative(outer(e0, e0), outer(e0, e1), zero(9))
    assert matrix_rank(shared) == 5
    assert matrix_rank(transverse) == 6

    profiles = {
        "222": (e0, e0, e0, e1, e1, e1, (2, 2, 2)),
        "122": (e0, e0, e0, zero(3), e1, e1, (1, 2, 2)),
        "112": (e0, zero(3), e0, zero(3), e0, e1, (1, 1, 2)),
        "111": (e0, zero(3), e0, zero(3), e0, e0, (1, 1, 1)),
    }
    for x, y, z, b, c, w, expected in profiles.values():
        blocks = hb_blocks(x, y, z, b, c, w)
        dmat = derivative(*blocks)
        n1 = vstack(x, y, z)
        n2 = vstack(b, c, w)
        assert matrix_rank(dmat) == 7
        assert matvec(dmat, n1) == zero(27)
        assert matvec(dmat, n2) == zero(27)
        got = (
            matrix_rank(columns_to_rows([x, b])),
            matrix_rank(columns_to_rows([y, c])),
            matrix_rank(columns_to_rows([z, w])),
        )
        assert got == expected
    print("independent derivative census: PASS (5 / 6 / Hilbert-Burch 7)")


def audit_transverse_rows():
    e0, e1, e2 = basis(0), basis(1), basis(2)
    b23 = outer(e0, e0)
    b13 = outer(e0, e1)
    dmat = derivative(b23, b13, zero(9))
    p0 = vstack(e0, zero(3), zero(3))
    p1 = vstack(zero(3), e1, zero(3))
    p2 = vstack(e2, e2, zero(3))
    n0 = vstack(zero(3), zero(3), e0)
    n1 = vstack(zero(3), zero(3), e1)

    direct_columns = [p0, p1, p2, n0, n1]
    direct_rows = columns_to_rows(direct_columns)
    assert matrix_rank(direct_rows) == 5
    assert matrix_rank([matvec(dmat, column) for column in direct_columns]) == 3
    involved = direct_rows[:6]
    third = direct_rows[6:]
    assert matrix_rank(involved) == 3
    assert matrix_rank(third) == 2

    extension = vstack(zero(3), zero(3), e2)
    extended_columns = [add(p0, extension), p1, p2, n0, n1]
    extended_rows = columns_to_rows(extended_columns)
    involved = extended_rows[:6]
    third = extended_rows[6:]
    assert matrix_rank(extended_rows) == 5
    assert matrix_rank(involved) == 3
    assert matrix_rank(third) == 3
    assert matrix_rank(involved) + matrix_rank(third) - matrix_rank(extended_rows) == 1
    print("independent transverse-row audit: PASS (rank-two boundary isolated)")


def audit_beta_components():
    # Evaluate each ideal on separate integer samples from every asserted
    # component.  This is deliberately row-oriented and does not use SymPy.
    samples_122 = [
        # a=0 and B,C proportional
        (Q(0), (Q(2), Q(3)), (Q(4), Q(6))),
        # B_2=C_2=0
        (Q(5), (Q(2), Q(0)), (Q(7), Q(0))),
    ]
    for a, b, c in samples_122:
        assert b[0] * c[1] - b[1] * c[0] == 0
        assert a * c[1] == 0
        assert a * b[1] == 0

    samples_112 = [
        (Q(0), Q(0), Q(3), Q(5)),
        (Q(0), Q(7), Q(0), Q(5)),
        (Q(11), Q(0), Q(3), Q(0)),
    ]
    for a, b, g, h in samples_112:
        assert b * g == 0 and a * h == 0 and a * b == 0

    samples_111 = [
        (Q(0), Q(0), Q(3)),
        (Q(0), Q(5), Q(0)),
        (Q(7), Q(0), Q(0)),
    ]
    for a, b, g in samples_111:
        assert b * g == 0 and a * g == 0 and a * b == 0

    # Independent truth-table reconstruction of the coordinate clauses.
    minimal_112 = set()
    for x_coord, y_coord, z_coord, w_coord in product([False, True], repeat=4):
        clauses = (
            (x_coord or y_coord)
            and (x_coord or z_coord)
            and (y_coord or w_coord)
        )
        if clauses and sum((x_coord, y_coord, z_coord, w_coord)) == 2:
            minimal_112.add((x_coord, y_coord, z_coord, w_coord))
        clauses_111 = (
            (x_coord or y_coord)
            and (x_coord or z_coord)
            and (y_coord or z_coord)
        )
        if clauses_111:
            assert sum((x_coord, y_coord, z_coord)) >= 2
    assert minimal_112 == {
        (True, True, False, False),
        (True, False, False, True),
        (False, True, True, False),
    }
    print("independent beta-zero audit: PASS (component ideals and boundary clauses)")


def audit_support_bound():
    e0, e1, e2 = basis(0), basis(1), basis(2)
    spanning = [outer(ei, e0) for ei in (e0, e1, e2)]
    spanning += [outer(e1, ej) for ej in (e0, e1, e2)]
    rows = columns_to_rows(spanning)
    rank = matrix_rank(rows)
    assert rank == 5
    for index, expected in enumerate((True, True, False)):
        diagonal = outer(basis(index), basis(index))
        enlarged = columns_to_rows(spanning + [diagonal])
        assert (matrix_rank(enlarged) == rank) is expected
    print("independent support audit: PASS (at most two target diagonals)")


def main():
    audit_derivative_profiles()
    audit_transverse_rows()
    audit_beta_components()
    audit_support_bound()
    print("independent joint-rank-five derivative/torus localization: PASS")


if __name__ == "__main__":
    main()
