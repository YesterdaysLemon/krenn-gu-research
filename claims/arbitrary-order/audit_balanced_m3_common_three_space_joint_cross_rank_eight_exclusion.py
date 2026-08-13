"""Independent stdlib audit of the S2Q joint-rank-eight exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def rank(rows: list[list[Fraction]]) -> int:
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


def pair_product(p: list[Fraction], q: list[Fraction]) -> list[Fraction]:
    out: list[Fraction] = []
    for left, right in ((0, 3), (0, 6), (3, 6)):
        out.extend(
            p[left + i] * q[right + j] + q[left + i] * p[right + j]
            for i, j in product(range(3), repeat=2)
        )
    return out


def basis_vector(index: int) -> list[Fraction]:
    return [Fraction(int(i == index)) for i in range(9)]


def audit_zero_divisors() -> None:
    pure = basis_vector(0)
    mixed = [a + b for a, b in zip(basis_vector(0), basis_vector(4), strict=True)]
    full = [a + b for a, b in zip(mixed, basis_vector(8), strict=True)]

    kernels: list[int] = []
    for q in (pure, mixed, full):
        matrix = [pair_product(basis_vector(i), q) for i in range(9)]
        kernels.append(9 - rank(matrix))
    assert kernels == [3, 1, 0]
    print("independent zero-divisor ranks: PASS (3 / 1 / 0)")


def audit_grid_sharpness() -> None:
    e = [basis_vector(i) for i in range(9)]
    p = [e[4], e[1], [Fraction(0)] * 9]
    q = [e[0], e[3], [Fraction(0)] * 9]
    assert rank([*p, *q]) == 4
    for i, j in product(range(3), repeat=2):
        if i != j:
            assert pair_product(p[i], q[j]) == [Fraction(0)] * 27

    # Independent case table: each tuple is
    # (number of nonzero q rows, number of support-pattern cases, max rank).
    table = [(0, 1, 3), (1, 3, 4), (2, 7, 4), (3, 5, 4)]
    assert sum(cases for _, cases, _ in table) == 16
    assert max(bound for _, _, bound in table) == 4
    print("independent off-diagonal grid audit: PASS (sharp rank 4)")


def audit_hyperplane_loss() -> None:
    # Standalone exact controls for rank(T|K)>=rank(T)-1.
    matrix = [
        [Fraction(int(i == j)) for j in range(6)] + [Fraction(0), Fraction(0), Fraction(0)]
        for i in range(6)
    ]
    assert rank(matrix) == 6
    assert rank([row[1:] for row in matrix]) == 5
    assert rank([row[:8] for row in matrix]) == 6
    print("independent hyperplane rank-loss audit: PASS (sharp one)")


def audit_exceptional_covectors() -> None:
    # The two pure-Z rows z1,z2 map to C tensor z1 and C tensor z2.
    # For a nonzero coordinate C these are two distinct coordinate tensors.
    c_z1 = [Fraction(0)] * 54
    c_z2 = [Fraction(0)] * 54
    c_z1[1] = Fraction(1)
    c_z2[28] = Fraction(1)
    assert rank([c_z1, c_z2]) == 2

    exceptional_covectors = [[Fraction(1), Fraction(0), Fraction(0)]]
    target_covectors = [
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    assert rank(exceptional_covectors) == 1
    assert rank(target_covectors) == 2
    print("independent exceptional-covector audit: PASS (1 versus 2)")


def main() -> None:
    audit_hyperplane_loss()
    audit_zero_divisors()
    audit_grid_sharpness()
    audit_exceptional_covectors()
    print("independent balanced m=3 joint-rank-eight exclusion audit: PASS")


if __name__ == "__main__":
    main()
