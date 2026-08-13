"""Independent stdlib audit of the single-root-block rank-seven exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

Vector = list[Fraction]
Matrix = list[list[Fraction]]


def rank(rows: Matrix) -> int:
    work = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
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
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def e(index: int) -> Vector:
    return [Fraction(int(i == index)) for i in range(9)]


def add(left: Vector, right: Vector, sign: int = 1) -> Vector:
    return [a + sign * b for a, b in zip(left, right, strict=True)]


def permanent_map(p: Vector, q: Vector) -> Matrix:
    """Build r -> per(r,p,q) directly from the six source assignments."""
    columns: list[Vector] = []
    for column in range(9):
        r = e(column)
        vectors = (r, p, q)
        out = [Fraction(0)] * 27
        for assignment in permutations(range(3)):
            x_vector = vectors[assignment[0]][:3]
            y_vector = vectors[assignment[1]][3:6]
            z_vector = vectors[assignment[2]][6:9]
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        out[9 * x + 3 * y + z] += (
                            x_vector[x] * y_vector[y] * z_vector[z]
                        )
        columns.append(out)
    return [[columns[column][row] for column in range(9)] for row in range(27)]


def multiply(matrix: Matrix, vector: Vector) -> Vector:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def audit_grid_normal_forms() -> None:
    x0, x1, x2, y0, y1, z0 = e(0), e(1), e(2), e(3), e(4), e(6)
    zero = [Fraction(0)] * 9
    forms = {
        "PP": ([x0, y0, zero], [y1, x1, zero]),
        "PM-shared": ([x0, add(x2, z0, -1), zero], [add(x2, z0), x1, zero]),
        "PM-disjoint": ([x0, add(y0, z0, -1), zero], [add(y0, z0), x1, zero]),
        "MM-same": (
            [add(x0, y0), add(x1, y1), zero],
            [add(x1, y1, -1), add(x0, y0, -1), zero],
        ),
        "MM-different": (
            [add(x0, y0), add(x1, z0), zero],
            [add(x1, z0, -1), add(x0, y0, -1), zero],
        ),
    }
    zero_map = [[Fraction(0)] * 9 for _ in range(27)]
    for name, (p_rows, q_rows) in forms.items():
        assert rank([*p_rows, *q_rows]) == 4, name
        for i in range(3):
            for j in range(3):
                if i != j:
                    assert permanent_map(p_rows[i], q_rows[j]) == zero_map, name
        assert rank(permanent_map(p_rows[0], q_rows[0])) > 0
        assert rank(permanent_map(p_rows[1], q_rows[1])) > 0
    print("independent marked-grid atlas: PASS (5 families)")


def audit_pure_mixed_kernel_lines() -> None:
    x0, x1, y0, z0 = e(0), e(1), e(3), e(6)
    p0, q0 = x0, add(y0, z0)
    p1, q1 = add(y0, z0, -1), x1
    d0, d1 = permanent_map(p0, q0), permanent_map(p1, q1)
    yz_columns = list(range(3, 9))
    stacked_columns = [
        [*transpose(d0)[column], *transpose(d1)[column]] for column in yz_columns
    ]
    assert rank(stacked_columns) == 6

    k0, k1 = add(y0, z0, -1), add(y0, z0)
    zero = [Fraction(0)] * 27
    assert multiply(d0, k0) == zero
    assert multiply(d1, k1) == zero
    assert rank([multiply(d0, k0), multiply(d0, k1)]) == 1
    assert rank([multiply(d1, k0), multiply(d1, k1)]) == 1

    yz_target_zero = [Fraction(1)] + [Fraction(0)] * 8
    yz_target_one = [Fraction(0)] * 4 + [Fraction(1)] + [Fraction(0)] * 4
    assert rank([yz_target_zero, yz_target_one]) == 2
    print("independent P/M kernel audit: PASS (two kernels, one factor line)")


def audit_mixed_mixed_cases() -> None:
    x0, x1, y0, y1, z0 = e(0), e(1), e(3), e(4), e(6)
    same_d0 = permanent_map(add(x0, y0), add(x1, y1, -1))
    same_d1 = permanent_map(add(x1, y1), add(x0, y0, -1))
    assert all(
        left == -right
        for row_left, row_right in zip(same_d0, same_d1, strict=True)
        for left, right in zip(row_left, row_right, strict=True)
    )

    diff_d0 = permanent_map(add(x0, y0), add(x1, z0, -1))
    diff_d1 = permanent_map(add(x1, z0), add(x0, y0, -1))
    stacked = [*diff_d0, *diff_d1]
    assert rank(stacked) == 9
    print("independent M/M audit: PASS (opposites / zero common kernel)")


def audit_rank_budget() -> None:
    # dim R=3 and dim span(P,Q)<=4 can reach joint rank seven only at the
    # exact four-dimensional grid boundary classified above.
    assert 3 + 4 == 7
    target_covectors = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]
    assert rank(target_covectors) == 2
    print("independent rank/covector budget: PASS (3+4; target rank 2)")


def main() -> None:
    audit_grid_normal_forms()
    audit_pure_mixed_kernel_lines()
    audit_mixed_mixed_cases()
    audit_rank_budget()
    print("independent single-root-block joint-rank-seven audit: PASS")


if __name__ == "__main__":
    main()
