"""Independent no-import audit for the GLS26 zero-anchor theorem."""

from fractions import Fraction


def vector(values):
    return tuple(Fraction(value) for value in values)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(value, item):
    return tuple(value * entry for entry in item)


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def kron(left, right):
    return tuple(a * b for a in left for b in right)


def matrix_rank(columns):
    if not columns:
        return 0
    row_count = len(columns[0])
    rows = [
        [columns[column][row] for column in range(len(columns))]
        for row in range(row_count)
    ]
    pivot_row = 0
    for pivot_column in range(len(columns)):
        selected = next(
            (row for row in range(pivot_row, row_count) if rows[row][pivot_column]),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][pivot_column]
        rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            coefficient = rows[row][pivot_column]
            if coefficient:
                rows[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(
                        rows[row], rows[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def basis(columns):
    chosen = []
    for column in columns:
        if matrix_rank([*chosen, column]) > len(chosen):
            chosen.append(column)
    return chosen


def contains(columns, item):
    return matrix_rank([*columns, item]) == matrix_rank(columns)


def nullspace(rows, width):
    work = [list(row) for row in rows]
    pivot_columns = []
    pivot_row = 0
    for column in range(width):
        selected = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break

    free_columns = [column for column in range(width) if column not in pivot_columns]
    result = []
    for free in free_columns:
        item = [Fraction(0) for _ in range(width)]
        item[free] = Fraction(1)
        for row, pivot in reversed(list(enumerate(pivot_columns))):
            item[pivot] = -sum(
                work[row][column] * item[column] for column in free_columns
            )
        result.append(tuple(item))
    return result


E = (
    vector((1, 0, 0)),
    vector((0, 1, 0)),
    vector((0, 0, 1)),
)


def tangent_space(shore0, shore1):
    return basis(
        [kron(left, right) for left in shore0 for right in E]
        + [kron(left, right) for left in E for right in shore1]
    )


def audit_fixture(name, raw0, raw1, root0, root1):
    shore0 = basis([vector(item) for item in raw0])
    shore1 = basis([vector(item) for item in raw1])
    d0 = len(shore0)
    d1 = len(shore1)
    tangent = tangent_space(shore0, shore1)
    assert len(tangent) == 3 * d0 + 3 * d1 - d0 * d1

    q = add(
        kron(vector(raw0[0]), vector(raw1[1])), kron(vector(raw0[1]), vector(raw1[0]))
    )
    epsilon = kron(vector(root0), vector(root1))
    p = dot(epsilon, q)
    assert p
    assert contains(tangent, q)

    def project(item):
        return add(scale(p, item), scale(-dot(epsilon, item), q))

    assert project(q) == vector((0,) * 9)
    test = vector((2, -1, 3, 0, 4, 1, -2, 5, 2))
    assert project(project(test)) == scale(p, project(test))
    projected_tangent = basis([project(item) for item in tangent])
    assert len(projected_tangent) == len(tangent) - 1
    assert len(projected_tangent) <= 7

    diagonal = [kron(E[colour], E[colour]) for colour in range(3)]
    delta = basis([project(item) for item in diagonal])
    q_is_diagonal = contains(diagonal, q)
    assert len(delta) == (2 if q_is_diagonal else 3)

    defect = matrix_rank([*tangent, *diagonal]) - len(tangent)
    projected_defect = matrix_rank([*projected_tangent, *delta]) - len(
        projected_tangent
    )
    assert defect == projected_defect

    coordinate_cover = all(
        contains(shore0, E[colour]) or contains(shore1, E[colour])
        for colour in range(3)
    )
    assert (defect == 0) == coordinate_cover

    annihilator0 = nullspace(shore0, 3)
    annihilator1 = nullspace(shore1, 3)
    hadamard_zero = all(
        left[colour] * right[colour] == 0
        for left in annihilator0
        for right in annihilator1
        for colour in range(3)
    )
    assert hadamard_zero == coordinate_cover

    # Re-derive the evaluated singleton matching slices using matrices not
    # shared with the primary verifier.
    port0 = (
        vector((2, 0, 1)),
        vector((1, 3, -1)),
        vector((0, 2, 4)),
    )
    port1 = (
        vector((1, 1, 0)),
        vector((0, 2, 3)),
        vector((3, -1, 2)),
    )
    singleton_checks = 0
    residual_vectors0 = [vector(item) for item in raw0]
    residual_vectors1 = [vector(item) for item in raw1]
    for residual in range(2):
        small_tangent = tangent_space(
            [residual_vectors0[residual]], [residual_vectors1[residual]]
        )
        for column in range(3):
            item = add(
                kron(residual_vectors0[residual], port1[column]),
                kron(port0[column], residual_vectors1[residual]),
            )
            assert contains(small_tangent, item)
            assert contains(tangent, item)
            assert contains(projected_tangent, project(item))
            singleton_checks += 1

    return {
        "shore_ranks": (d0, d1),
        "tangent_rank": len(tangent),
        "projected_tangent_rank": len(projected_tangent),
        "diagonal_rank": len(delta),
        "defect": defect,
        "coordinate_cover": coordinate_cover,
        "annihilator_dimensions": (len(annihilator0), len(annihilator1)),
        "singleton_checks": singleton_checks,
    }


def main():
    fixtures = (
        (
            "different generic rank-two shores",
            ((1, 2, 0), (0, 1, 3)),
            ((2, 0, 1), (1, 3, 0)),
            (2, 1, 3),
            (1, 4, 2),
        ),
        (
            "disjoint-normal coordinate cover",
            ((1, 0, 0), (0, 1, 0)),
            ((0, 1, 0), (0, 0, 1)),
            (2, 1, 3),
            (1, 4, 2),
        ),
        (
            "one-two shore cover",
            ((0, 0, 1), (0, 0, 2)),
            ((1, 0, 0), (0, 1, 0)),
            (2, 1, 3),
            (1, 4, 2),
        ),
        (
            "one-one uncovered colour",
            ((1, 0, 0), (3, 0, 0)),
            ((0, 0, 1), (0, 0, 2)),
            (2, 1, 3),
            (1, 4, 2),
        ),
    )
    results = {
        name: audit_fixture(name, shore0, shore1, root0, root1)
        for name, shore0, shore1, root0, root1 in fixtures
    }
    assert results["different generic rank-two shores"]["defect"] > 0
    assert results["disjoint-normal coordinate cover"]["defect"] == 0
    assert results["one-two shore cover"]["defect"] == 0
    assert results["one-one uncovered colour"]["defect"] > 0

    print("promoted zero-anchor residual-shore independent audit: PASS")
    for name, result in results.items():
        print(f"  {name}: {result}")
    print("  no imports from primary verifier or repository helpers")


if __name__ == "__main__":
    main()
