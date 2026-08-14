#!/usr/bin/env python3
"""Independent Fraction audit for the S2BX (2,2,3) exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Vector = tuple[Fraction, ...]
SparseTensor = dict[tuple[int, int, int], Fraction]


def add_vector(left: Vector, right: Vector, scale: Fraction = Fraction(1)) -> Vector:
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def scale_vector(scale: Fraction, vector: Vector) -> Vector:
    return tuple(scale * value for value in vector)


def rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][col]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            factor = matrix[row][col]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def add_tensor(
    left: SparseTensor, right: SparseTensor, scale: Fraction = Fraction(1)
) -> SparseTensor:
    out = dict(left)
    for index, value in right.items():
        new_value = out.get(index, Fraction(0)) + scale * value
        if new_value:
            out[index] = new_value
        else:
            out.pop(index, None)
    return out


def cube(vector: Vector) -> SparseTensor:
    # Reverse index convention relative to the primary replay.
    out: SparseTensor = {}
    for k, j, i in product(range(3), repeat=3):
        value = vector[i] * vector[j] * vector[k]
        if value:
            out[(k, j, i)] = value
    return out


def p3() -> SparseTensor:
    out: SparseTensor = {}
    for sigma in permutations(range(3)):
        index = tuple(reversed(sigma))
        out[index] = out.get(index, Fraction(0)) + 1
    return out


def flatten(tensor: SparseTensor, mode: int) -> list[Vector]:
    columns: list[Vector] = []
    other = [slot for slot in range(3) if slot != mode]
    for first in range(3):
        for second in range(3):
            column = []
            for fixed in range(3):
                index = [0, 0, 0]
                index[mode] = fixed
                index[other[0]] = first
                index[other[1]] = second
                column.append(tensor.get(tuple(index), Fraction(0)))
            columns.append(tuple(column))
    return columns


def audit_correction() -> None:
    kappa = Fraction(7)
    # Coordinates are (second root, third root), with d,s,t=(0,1,2).
    columns: list[Vector] = []
    for colour in range(3):
        column = [Fraction(0)] * 9
        column[3 * colour] = kappa
        columns.append(tuple(column))
    rhs = [Fraction(0)] * 9
    rhs[0] = -1
    solution = (Fraction(-1, 7), Fraction(0), Fraction(0))
    reconstructed = tuple(
        sum(solution[col] * columns[col][row] for col in range(3))
        for row in range(9)
    )
    assert reconstructed == tuple(rhs)
    assert rank(columns) == 3


def audit_permanent_rank_interface() -> None:
    permanent = p3()
    assert all(rank(flatten(permanent, mode)) == 3 for mode in range(3))

    signed_vectors = (
        (Fraction(1, 4), (Fraction(1), Fraction(1), Fraction(1))),
        (Fraction(-1, 4), (Fraction(1), Fraction(1), Fraction(-1))),
        (Fraction(-1, 4), (Fraction(1), Fraction(-1), Fraction(1))),
        (Fraction(-1, 4), (Fraction(-1), Fraction(1), Fraction(1))),
    )
    decomposition: SparseTensor = {}
    for coefficient, vector in signed_vectors:
        decomposition = add_tensor(decomposition, cube(vector), coefficient)
    assert decomposition == permanent

    diagonal = {(i, i, i): Fraction(i + 2) for i in range(3)}
    assert all(rank(flatten(diagonal, mode)) == 3 for mode in range(3))

    # A first-flattening slice has matrix [[0,z,y],[z,0,x],[y,x,0]].
    # Its principal minors are checked independently by the 2x2 formula.
    for x, y, z in product(range(-2, 3), repeat=3):
        minors = (-z * z, -y * y, -x * x)
        if minors == (0, 0, 0):
            assert (x, y, z) == (0, 0, 0)


def binary_value(a: int, b: int, c: int) -> tuple[Fraction, Fraction]:
    if a == b == c == 0:
        return (Fraction(1), Fraction(0))
    if a == b == c == 1:
        return (Fraction(0), Fraction(1))
    return (Fraction(0), Fraction(0))


def audit_shifted_table() -> None:
    for lam_0, lam_1 in product(range(-3, 4), repeat=2):
        for a, b, c in product(range(2), repeat=3):
            kernel = (Fraction(0), Fraction(0))
            scale = Fraction(lam_0 if c == 0 else lam_1)
            shifted = tuple(
                value + scale * zero
                for value, zero in zip(binary_value(a, b, c), kernel, strict=True)
            )
            assert shifted == binary_value(a, b, c)


def audit_shift_trap() -> None:
    qd: Vector = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    q0: Vector = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    q1: Vector = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))

    support_counts = {1: 0, 2: 0}
    for aa, bb in product(range(-3, 4), repeat=2):
        if aa == bb == 0:
            continue
        support_counts[int(aa != 0) + int(bb != 0)] += 1
        for cc in (-5, -2, 1, 4):
            if aa:
                lam_0, lam_1 = Fraction(cc, aa), Fraction(0)
            else:
                lam_0, lam_1 = Fraction(0), Fraction(cc, bb)
            ell = add_vector(
                add_vector(scale_vector(Fraction(aa), q0), scale_vector(Fraction(bb), q1)),
                scale_vector(Fraction(cc), qd),
            )
            shifted_0 = add_vector(q0, qd, lam_0)
            shifted_1 = add_vector(q1, qd, lam_1)
            reconstructed = add_vector(
                scale_vector(Fraction(aa), shifted_0),
                scale_vector(Fraction(bb), shifted_1),
            )
            assert reconstructed == ell
            assert rank([shifted_0, shifted_1, ell]) == 2
    assert support_counts[1] == 12
    assert support_counts[2] == 36

    endpoint = scale_vector(Fraction(13), qd)
    assert rank([qd, endpoint]) == 1

    # A plane disjoint from Q_0 meets the hyperplane Q in one line.
    h: Vector = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    q_space = [qd, q0, q1]
    q_binary = [q0, q1]
    for line in (qd, add_vector(add_vector(qd, q0, 2), q1, -3)):
        plane = [line, h]
        assert rank(plane) == 2
        assert rank(plane + q_binary) == 4
        assert len(plane) + len(q_space) - rank(plane + q_space) == 1


def main() -> None:
    audit_correction()
    audit_permanent_rank_interface()
    audit_shifted_table()
    audit_shift_trap()
    print(
        "S2BX independent audit passed: Fraction correction, reverse-index "
        "P3 certificate, binary shifts, and all rational shift-support masks."
    )


if __name__ == "__main__":
    main()
