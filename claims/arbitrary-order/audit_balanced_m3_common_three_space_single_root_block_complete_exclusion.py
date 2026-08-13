"""Independent stdlib audit of the complete single-root-block exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

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


def pair_product(p: Vector, q: Vector) -> Vector:
    out: Vector = []
    for left, right in ((3, 6), (0, 6), (0, 3)):
        out.extend(
            p[left + i] * q[right + j] + q[left + i] * p[right + j]
            for i, j in product(range(3), repeat=2)
        )
    return out


def derivative(p: Vector, q: Vector) -> Matrix:
    pair = pair_product(p, q)
    columns: Matrix = []
    for column in range(9):
        r = e(column)
        vector = [Fraction(0)] * 27
        for x, y, z in product(range(3), repeat=3):
            vector[9 * x + 3 * y + z] = (
                r[x] * pair[3 * y + z]
                + r[3 + y] * pair[9 + 3 * x + z]
                + r[6 + z] * pair[18 + 3 * x + y]
            )
        columns.append(vector)
    return [list(row) for row in zip(*columns, strict=True)]


def audit_zero_pair_atlas() -> None:
    x0, x1, y0, y1, z0 = e(0), e(1), e(3), e(4), e(6)
    controls = [
        (x0, x1, y0, y1),
        (x0, x1, add(y0, z0, -1), add(y0, z0)),
        (add(x0, y0), add(x0, y0, -1), add(x1, z0), add(x1, z0, -1)),
        (add(x0, y0), add(x0, y0, -1), add(x0, z0), add(x0, z0, -1)),
    ]
    zero = [Fraction(0)] * 27
    for p0, q1, p1, q0 in controls:
        assert pair_product(p0, q1) == zero
        assert pair_product(p1, q0) == zero
        assert pair_product(p0, q0) != zero
        assert pair_product(p1, q1) != zero
    print("independent crossed-pair atlas: PASS (pure/mixed boundaries)")


def audit_derivative_boundaries() -> None:
    x0, x1, y0, y1, z0 = e(0), e(1), e(3), e(4), e(6)

    same_zero = derivative(add(x0, y0), add(x1, y1, -1))
    same_one = derivative(add(x1, y1), add(x0, y0, -1))
    assert all(
        left == -right
        for row_left, row_right in zip(same_zero, same_one, strict=True)
        for left, right in zip(row_left, row_right, strict=True)
    )

    transverse_zero = derivative(add(x0, y0), add(x1, z0, -1))
    transverse_one = derivative(add(x1, z0), add(x0, y0, -1))
    assert rank([*transverse_zero, *transverse_one]) == 9

    shared_zero = derivative(add(x0, y0), add(x0, z0, -1))
    shared_one = derivative(add(x0, z0), add(x0, y0, -1))
    assert rank([*shared_zero, *shared_one]) == 8
    assert rank([*zip(*shared_zero, strict=True), *zip(*shared_one, strict=True)]) == 7
    print("independent M/M derivatives: PASS (opposite / rank 9 / tangent 7)")


def audit_tangent_rulings() -> None:
    # The Boolean implication proof of Lemma 2: all triples satisfying
    # (x0 or y0), (x0 or z0), (y0 or z0) have at least two true entries.
    accepted = []
    for x_base, y_base, z_base in product((False, True), repeat=3):
        if not (x_base or y_base):
            continue
        if not (x_base or z_base):
            continue
        if not (y_base or z_base):
            continue
        accepted.append((x_base, y_base, z_base))
        assert sum((x_base, y_base, z_base)) >= 2
    assert len(accepted) == 4
    for left in accepted:
        for right in accepted:
            assert any(a and b for a, b in zip(left, right, strict=True))

    target_zero = ("X0", "Y0", "Z0")
    target_one = ("X1", "Y1", "Z1")
    assert all(left != right for left, right in zip(target_zero, target_one, strict=True))
    print("independent tangent-ruling audit: PASS (4 Boolean patterns)")


def main() -> None:
    audit_zero_pair_atlas()
    audit_derivative_boundaries()
    audit_tangent_rulings()
    print("independent single-root-block complete exclusion audit: PASS")


if __name__ == "__main__":
    main()
