"""Independent stdlib audit of the complete S2U full-rank exclusion."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product


def rref(rows: list[list[Fraction]], columns: int) -> tuple[list[list[Fraction]], list[int]]:
    work = [[Fraction(entry) for entry in row] for row in rows]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        pivot = next(
            (i for i in range(pivot_row, len(work)) if work[i][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for i, row in enumerate(work):
            if i == pivot_row or not row[column]:
                continue
            multiple = row[column]
            work[i] = [
                left - multiple * right
                for left, right in zip(row, work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivots


def row_rank(rows: list[list[Fraction]], columns: int | None = None) -> int:
    if columns is None:
        columns = len(rows[0]) if rows else 0
    return len(rref(rows, columns)[1])


def nullspace(rows: list[list[Fraction]], columns: int) -> list[list[Fraction]]:
    reduced, pivots = rref(rows, columns)
    free = [column for column in range(columns) if column not in pivots]
    basis: list[list[Fraction]] = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(vector)
    return basis


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def matmul(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    columns = list(zip(*right, strict=True))
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in columns]
        for row in left
    ]


def projection_from_kernel(kernel: list[list[int]]) -> list[list[Fraction]]:
    basis = nullspace([[Fraction(x) for x in row] for row in kernel], 3)
    out = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for column, vector in enumerate(basis):
        for row in range(3):
            out[row][column] = vector[row]
    return out


KERNEL_ATLAS = [
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], [[0, 1, 0], [1, 0, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 1]], [[1, 1, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], [[1, 1, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], [[0, 1, 0]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 1]], []],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], []],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], [[1, 1, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], [[1, 1, 0]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], [[1, 0, 0]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 0]], [[1, 0, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], []],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 0]], []],
    [[[0, 1, 1], [1, 0, 1]], [], []],
    [[[1, 1, 1]], [[1, 1, 1]], [[1, 1, 0]]],
    [[[1, 1, 1]], [[1, 1, 0]], [[1, 0, 1]]],
    [[[1, 1, 1]], [[1, 1, 0]], [[0, 0, 1]]],
    [[[1, 1, 1]], [[1, 1, 1]], []],
    [[[1, 1, 1]], [[1, 1, 0]], []],
    [[[1, 1, 1]], [], []],
    [[], [], []],
]


def restriction_rows(r_space: list[list[Fraction]]) -> list[list[Fraction]]:
    out: list[list[Fraction]] = []
    for root_row, x, y, z in product(range(3), repeat=4):
        row = [Fraction(0) for _ in range(27)]
        row[3 * y + z] = r_space[root_row][x]
        row[9 + 3 * x + z] = r_space[root_row][3 + y]
        row[18 + 3 * x + y] = r_space[root_row][6 + z]
        out.append(row)
    return out


def audit_derivative_atlas() -> None:
    ranks: Counter[int] = Counter()
    profiles: list[tuple[int, int, int]] = []
    for kernels in KERNEL_ATLAS:
        projections = [projection_from_kernel(kernel) for kernel in kernels]
        r_space = [
            [entry for projection in projections for entry in projection[row]]
            for row in range(3)
        ]
        assert row_rank(r_space, 9) == 3
        value = row_rank(restriction_rows(r_space), 27)
        ranks[value] += 1
        if value < 27:
            profiles.append(tuple(3 - len(kernel) for kernel in kernels))
    assert ranks == Counter({27: 18, 24: 2})
    assert profiles == [(1, 1, 2), (1, 1, 3)]
    print("independent rational derivative atlas: PASS (18 injective; 2 exceptional)")


def outer(left: list[int], right: list[int]) -> list[list[Fraction]]:
    return [[Fraction(a * b) for b in right] for a in left]


def add_matrices(*matrices: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(matrix[i][j] for matrix in matrices) for j in range(3)]
        for i in range(3)
    ]


def scale_matrix(matrix: list[list[Fraction]], scale: int) -> list[list[Fraction]]:
    return [[scale * entry for entry in row] for row in matrix]


def derivative_rows(
    a_tensor: list[list[Fraction]],
    b_tensor: list[list[Fraction]],
    c_tensor: list[list[Fraction]],
) -> list[list[Fraction]]:
    out: list[list[Fraction]] = []
    for x, y, z in product(range(3), repeat=3):
        row = [Fraction(0) for _ in range(9)]
        row[x] = a_tensor[y][z]
        row[3 + y] = b_tensor[x][z]
        row[6 + z] = c_tensor[x][y]
        out.append(row)
    return out


def audit_hilbert_burch_boundary() -> None:
    e0, e1 = [1, 0, 0], [0, 1, 0]
    a_tensor = scale_matrix(add_matrices(outer(e0, e1), outer(e1, e0)), -1)
    b_tensor = add_matrices(outer(e0, e1), outer(e1, e0))
    c_tensor = add_matrices(outer(e0, e1), scale_matrix(outer(e1, e0), -1))
    matrix = derivative_rows(a_tensor, b_tensor, c_tensor)
    first = [*e0, *e0, *e0]
    second = [*e1, *e1, 0, -1, 0]
    assert matvec(matrix, [Fraction(x) for x in first]) == [0] * 27
    assert matvec(matrix, [Fraction(x) for x in second]) == [0] * 27
    assert row_rank(matrix, 9) == 7
    print("independent Hilbert-Burch sharp boundary: PASS (rank 7)")


def pair_rows(q: list[int]) -> list[list[Fraction]]:
    qx, qy, qz = q[:3], q[3:6], q[6:9]
    out = [[Fraction(0) for _ in range(9)] for _ in range(27)]
    for i, j in product(range(3), repeat=2):
        out[3 * i + j][3 + i] = qz[j]
        out[3 * i + j][6 + j] = qy[i]
        out[9 + 3 * i + j][i] = qz[j]
        out[9 + 3 * i + j][6 + j] = qx[i]
        out[18 + 3 * i + j][i] = qy[j]
        out[18 + 3 * i + j][3 + j] = qx[i]
    return out


def exceptional_space(epsilon: int) -> list[list[Fraction]]:
    out = [[Fraction(0) for _ in range(9)] for _ in range(3)]
    out[0][0] = out[0][3] = Fraction(1)
    out[0][6] = Fraction(epsilon)
    out[1][7] = out[2][8] = Fraction(1)
    return out


def audit_pair_products() -> None:
    support_ranks: Counter[tuple[int, int]] = Counter()
    for mask in range(1, 8):
        q = [0] * 9
        size = 0
        for source in range(3):
            if mask & (1 << source):
                q[3 * source] = 1
                size += 1
        support_ranks[(size, row_rank(pair_rows(q), 9))] += 1
    assert support_ranks == Counter({(1, 6): 3, (2, 8): 3, (3, 9): 1})

    delta = restriction_rows(exceptional_space(1))
    basis = [[int(i == j) for i in range(9)] for j in range(9)]
    ex, ey, ez = basis[0], basis[3], basis[6]
    ell_minus = [a - b for a, b in zip(ex, ey, strict=True)]
    ell_plus = [a + b for a, b in zip(ex, ey, strict=True)]
    cases = [
        (ex, 6, basis[:3]),
        (basis[1], 6, basis[:3]),
        (ey, 6, basis[3:6]),
        (basis[4], 6, basis[3:6]),
        (ez, 5, [*basis[6:9], ell_minus]),
        (ell_minus, 5, [*basis[6:9], ell_plus]),
        ([a + b for a, b in zip(ell_minus, ez, strict=True)], 6, basis[6:9]),
    ]
    for q, expected_rank, expected_kernel in cases:
        matrix = matmul(delta, pair_rows(q))
        assert row_rank(matrix, 9) == expected_rank
        assert all(matvec(matrix, vector) == [0] * 81 for vector in expected_kernel)
        assert row_rank(expected_kernel, 9) == 9 - expected_rank
    print("independent pair-product ranks: PASS (7 regular + 7 exceptional orbits)")


def audit_grid_categories() -> None:
    regular = Counter(
        "six-in-three" if len(set(labels)) == 1 else "zero-intersection"
        for labels in product("XYZ", repeat=3)
    )
    exceptional = Counter()
    for labels in product(("X", "Y", "L"), repeat=3):
        if set(labels) == {"L"}:
            exceptional["nine-in-five"] += 1
        elif len(set(labels)) == 1:
            exceptional["six-in-three"] += 1
        else:
            exceptional["zero-intersection"] += 1
    assert regular == Counter({"zero-intersection": 24, "six-in-three": 3})
    assert exceptional == Counter(
        {"zero-intersection": 24, "six-in-three": 2, "nine-in-five": 1}
    )
    print("independent zero-grid category audit: PASS (54/54 assignments)")


def main() -> None:
    audit_derivative_atlas()
    audit_hilbert_burch_boundary()
    audit_pair_products()
    audit_grid_categories()
    print("independent balanced m=3 full-joint-rank exclusion audit: PASS")


if __name__ == "__main__":
    main()
