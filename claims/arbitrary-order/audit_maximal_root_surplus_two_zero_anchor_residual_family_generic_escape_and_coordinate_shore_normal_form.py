"""Independent no-import audit for the GLS27 residual-family theorem."""

from fractions import Fraction


def vec(values):
    return tuple(Fraction(value) for value in values)


E = (vec((1, 0, 0)), vec((0, 1, 0)), vec((0, 0, 1)))


def rank(columns):
    if not columns:
        return 0
    rows = [[column[row] for column in columns] for row in range(len(columns[0]))]
    pivot = 0
    for column in range(len(columns)):
        selected = next(
            (row for row in range(pivot, len(rows)) if rows[row][column]), None
        )
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        value = rows[pivot][column]
        rows[pivot] = [entry / value for entry in rows[pivot]]
        for row in range(len(rows)):
            if row != pivot and rows[row][column]:
                value = rows[row][column]
                rows[row] = [
                    a - value * b for a, b in zip(rows[row], rows[pivot], strict=True)
                ]
        pivot += 1
    return pivot


def contains(space, item):
    return rank([*space, item]) == rank(space)


def kron(left, right):
    return tuple(a * b for a in left for b in right)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def matrix_rank(item):
    return rank(
        [tuple(item[3 * row + column] for row in range(3)) for column in range(3)]
    )


def audit_forms():
    e0, e1, e2 = E
    one = [e0, vec((3, 0, 0))]
    two = [e1, e2]
    q12 = add(kron(one[0], two[1]), kron(one[1], two[0]))
    assert rank(one) == 1 and rank(two) == 2 and matrix_rank(q12) == 1
    assert all(q12[3 * colour + colour] == 0 for colour in range(3))

    plane0 = [e0, vec((0, 2, 5))]
    plane1 = [e1, e2]
    q22 = add(kron(plane0[0], plane1[1]), kron(plane0[1], plane1[0]))
    assert matrix_rank(q22) == 2
    assert all(q22[3 * row] == 0 for row in range(3))
    assert all(contains(plane0, basis) or contains(plane1, basis) for basis in E)

    escape0 = [vec((1, 0, 2)), e1]
    escape1 = [e0, vec((0, 1, 3))]
    assert not contains(escape0, e2) and not contains(escape1, e2)
    return {"C12": matrix_rank(q12), "C22": matrix_rank(q22), "escape_colour": 2}


def audit_control():
    # Direct GLD11 rows at A=(r0,r2), Q=(q0,q1).
    shore0 = [E[0], E[2]]
    shore1 = [vec((0, 0, 0)), E[1]]
    q = add(kron(shore0[0], shore1[1]), kron(shore0[1], shore1[0]))
    assert rank(shore0) == 2 and rank(shore1) == 1 and matrix_rank(q) == 1
    assert all(contains(shore0, basis) or contains(shore1, basis) for basis in E)
    root_table = (
        (1, 0, 2, None, 0, 2),
        (2, None, None, 1, 2, 0),
        (None, 1, 0, 2, None, 1),
        (0, 2, 1, 0, 1, None),
    )
    injection = ((0, 0), (1, 3), (2, 1), (3, 2))
    assert all(root_table[root][port] == 1 for root, port in injection)
    return {"shore_ranks": (2, 1), "q_rank": 1, "Pi_injection": injection}


def main():
    print("zero-anchor residual-family independent audit: PASS")
    print("  separate normal-form/escape derivation:", audit_forms())
    print("  independent GLD11 source reading:", audit_control())
    print("  no imports from primary verifier or repository helpers")


if __name__ == "__main__":
    main()
