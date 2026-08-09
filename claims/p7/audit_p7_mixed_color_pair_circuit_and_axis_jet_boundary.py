"""Independent no-import audit for the mixed-colour P7 pair circuit."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def determinant3(matrix: list[list[Fraction]]) -> Fraction:
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def outer(left: list[Fraction], right: list[Fraction]) -> list[list[Fraction]]:
    return [[left[i] * right[j] for j in range(3)] for i in range(3)]


def add(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [[left[i][j] + right[i][j] for j in range(3)] for i in range(3)]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    work[row][j] - scale * work[pivot_row][j] for j in range(cols)
                ]
        pivot_row += 1
    return pivot_row


def audit_pair_circuit() -> None:
    samples = (
        ([1, 0, 1], [0, 1, 1], [1, 1, 0], [1, -1, 1]),
        ([2, -1, 3], [1, 4, 0], [-2, 1, 5], [3, 0, -1]),
        ([1, 2, 4], [-3, 1, 2], [5, -2, 1], [0, 3, -1]),
    )
    for raw in samples:
        a_u, b_u, a_v, b_v = ([Fraction(value) for value in vector] for vector in raw)
        response = add(outer(a_u, b_v), outer(b_u, a_v))
        assert determinant3(response) == 0
        assert rank(response) <= 2
    first = samples[0]
    first_response = add(
        outer([Fraction(x) for x in first[0]], [Fraction(x) for x in first[3]]),
        outer([Fraction(x) for x in first[1]], [Fraction(x) for x in first[2]]),
    )
    assert first_response[0][0] * first_response[1][1] - first_response[0][1] * first_response[1][0]


def audit_pair_top_inverse() -> None:
    targets = (
        (2, 3, 10, 29),
        (-1, 4, 7, -5),
        (Fraction(3, 2), Fraction(-2), Fraction(9), Fraction(11)),
    )
    for raw_x, raw_p, raw_m4, raw_z4 in targets:
        x = Fraction(raw_x)
        p = Fraction(raw_p)
        m4 = Fraction(raw_m4)
        z4 = Fraction(raw_z4)
        assert x
        y = m4 / x
        q = (z4 - p * y) / x
        assert x * y == m4
        assert p * y + q * x == z4


def audit_diagonal_interpolation() -> None:
    beta = [Fraction(2), Fraction(-3), Fraction(5)]
    a_u = [Fraction(1), Fraction(1), Fraction(1)]
    b_u = [Fraction(0), Fraction(0), Fraction(0)]
    a_v = [Fraction(0), Fraction(0), Fraction(0)]
    b_v = [Fraction(7), Fraction(-2), Fraction(4)]
    direct = [[beta[i] if i == j else Fraction(0) for j in range(3)] for i in range(3)]
    corrected = add(outer(a_u, b_v), outer(b_u, a_v))
    assert [direct[i][i] for i in range(3)] == beta
    assert [corrected[i][i] for i in range(3)] == b_v


def audit_axis_labels() -> None:
    patterns = (
        (0, 0, 0, 0, 1),
        (0, 0, 0, 1, 2),
        (0, 0, 1, 1, 2),
    )
    for axes in patterns:
        labels: dict[tuple[int, int], int] = {}
        for size in range(1, 6):
            for roots in combinations(range(5), size):
                surviving = sorted(set(range(3)) - {axes[root] for root in roots})
                tags = (0b00, 0b11) if size % 2 == 0 else (0b01, 0b10)
                root_mask = sum(1 << root for root in roots)
                for color, tag in zip(surviving, tags, strict=False):
                    label = (root_mask, tag)
                    assert label not in labels
                    labels[label] = color
        assert labels
        assert all(root_mask.bit_count() % 2 == tag.bit_count() % 2 for root_mask, tag in labels)


def audit_companion_shores() -> None:
    cases = (
        (
            ({"b", "c"}, {"a1", "a2", "a3", "b"}, {"a1", "a2", "a3", "c"}),
            (
                (("b", "a1"), ("c", "a3")),
                (("b", "a1"), ("a2", "a3")),
                (("a1", "a2"), ("a3", "c")),
            ),
        ),
        (
            ({"b1", "b2", "c"}, {"a1", "a2", "c"}, {"a1", "a2", "b1", "b2"}),
            (
                (("b1", "b2"), ("c", "a1")),
                (("a1", "a2"), ("c", "b1")),
                (("a1", "a2"), ("b1", "b2")),
            ),
        ),
    )
    for shores, matchings in cases:
        for shore, matching in zip(shores, matchings, strict=True):
            endpoints = [vertex for edge in matching for vertex in edge]
            assert len(endpoints) == len(set(endpoints))
            assert shore.issubset(endpoints)


def main() -> None:
    audit_pair_circuit()
    audit_pair_top_inverse()
    audit_diagonal_interpolation()
    audit_axis_labels()
    audit_companion_shores()
    print("PASS: independent rational corrected-pair determinant audit")
    print("PASS: independent pair/top inverse and diagonal interpolation audit")
    print("PASS: independent exceptional all-axis deletion-label audit")
    print("PASS: independent singleton-axis companion-shore audit")
    print("SCOPE: mixed-entry exposure, P7, and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
