"""No-import audit for the P7 deletion-cube observability boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def permanent_dp(matrix: list[list[int]]) -> int:
    """Independent integer subset recurrence."""
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    states = {0: 1}
    for row in matrix:
        nxt: dict[int, int] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    new_mask = mask | (1 << column)
                    nxt[new_mask] = nxt.get(new_mask, 0) + value * entry
        states = nxt
    return states[(1 << size) - 1]


def submatrix(
    matrix: list[list[int]], rows: tuple[int, ...], cols: tuple[int, ...]
) -> list[list[int]]:
    return [[matrix[row][column] for column in cols] for row in rows]


def audit_marked_laplace() -> None:
    matrix = [
        [2, -1, 3, 0, 4],
        [1, 5, -2, 2, 3],
        [0, 2, 1, -3, 5],
        [4, 1, 0, 2, -1],
        [-2, 3, 4, 1, 2],
    ]
    full = permanent_dp(matrix)
    total = 0
    universe = tuple(range(5))
    for rows in combinations(universe, 3):
        other_rows = tuple(row for row in universe if row not in rows)
        for cols in combinations(universe, 3):
            if 0 not in cols:
                continue
            other_cols = tuple(column for column in universe if column not in cols)
            total += permanent_dp(submatrix(matrix, rows, cols)) * permanent_dp(
                submatrix(matrix, other_rows, other_cols)
            )
    assert full != 0
    assert total == 6 * full


def multiply_square_zero(
    left: dict[int, Fraction], right: dict[int, Fraction]
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            out[mask] = out.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in out.items() if value}


def audit_top_face_fibre() -> None:
    top_data = set()
    lower_data = set()
    for a in (Fraction(1), Fraction(2), Fraction(-3), Fraction(5, 2)):
        moment = {0: Fraction(1), 0b1100: a}
        relative = {0b0011: 1 / a}
        response = multiply_square_zero(moment, relative)
        top_data.add((moment.get(0b1111, Fraction(0)), response[0b1111]))
        lower_data.add((moment[0b1100], response[0b0011]))
    assert top_data == {(Fraction(0), Fraction(1))}
    assert len(lower_data) == 4


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    row_count = len(work)
    col_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(col_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    work[row][j] - scale * work[pivot_row][j]
                    for j in range(col_count)
                ]
        pivot_row += 1
    return pivot_row


def audit_observation_deficit() -> None:
    mu = Fraction(7, 3)
    one_channel = [[Fraction(1), mu]]
    invisible = [mu, Fraction(-1)]
    assert sum(one_channel[0][i] * invisible[i] for i in range(2)) == 0
    assert rank(one_channel) == 1
    assert rank([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]) == 2

    overlay = [
        [1, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1],
    ]
    assert rank([[Fraction(entry) for entry in row] for row in overlay]) == 4
    for s, t in ((1, 0), (0, 1), (2, -5)):
        hidden = [-s - t, s, t, t, s, -s - t]
        assert all(
            sum(row[column] * hidden[column] for column in range(6)) == 0
            for row in overlay
        )


def audit_label_gap() -> None:
    roots = set(range(5))
    blockers = set(range(5, 12))
    residuals = {12, 13}
    four_ports = {5, 6, 7, 8}
    six_ports = blockers - {11}
    four_label = roots | (blockers - four_ports)
    six_label = roots | (blockers - six_ports)
    lower_frame = [{0, 1}, {0, 1} | residuals]
    assert len(four_label & blockers) == 3
    assert len(six_label & blockers) == 1
    assert all(not (label & blockers) for label in lower_frame)


def main() -> None:
    audit_marked_laplace()
    audit_top_face_fibre()
    audit_observation_deficit()
    audit_label_gap()
    print("PASS: independent integer marked-Laplace audit")
    print("PASS: independent rational top-face noninjectivity audit")
    print("PASS: independent observation-kernel and deletion-label audit")
    print("SCOPE: bounded audits only; P7 and global conjecture remain UNRESOLVED")


if __name__ == "__main__":
    main()
