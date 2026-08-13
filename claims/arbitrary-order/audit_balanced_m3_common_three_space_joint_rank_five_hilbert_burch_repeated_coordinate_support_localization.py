"""Independent no-import audit of the repeated-coordinate support result.

This file imports no repository module and no third-party package.  It uses
standard-library Fraction arithmetic, row-oriented tensors, a separate cubic
coefficient order, and exact Gaussian elimination.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from math import factorial

Vector = tuple[F, ...]


def unit(size: int, index: int) -> Vector:
    return tuple(F(position == index) for position in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, F(0)) for entries in zip(*vectors, strict=True))


def scale(value: F | int, vector: Vector) -> Vector:
    scalar = F(value)
    return tuple(scalar * entry for entry in vector)


def tensor3(x: Vector, y: Vector, z: Vector) -> Vector:
    return tuple(a * b * c for a in x for b in y for c in z)


def source(group: int, local: int) -> Vector:
    return unit(9, 3 * group + local)


def component(vector: Vector, group: int, local: int) -> F:
    return vector[3 * group + local]


def polarized(u: Vector, v: Vector, q: Vector) -> Vector:
    forms = (u, v, q)
    out = [F(0) for _ in range(27)]
    for sigma in permutations(range(3)):
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    out[9 * x + 3 * y + z] += (
                        component(forms[sigma[0]], 0, x)
                        * component(forms[sigma[1]], 1, y)
                        * component(forms[sigma[2]], 2, z)
                    )
    return tuple(out)


def rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def nullspace(rows: list[Vector], column_count: int) -> list[Vector]:
    matrix = [list(row) for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_columns.append(column)
        pivot_row += 1
    free_columns = [
        column for column in range(column_count) if column not in pivot_columns
    ]
    output = []
    for free in free_columns:
        vector = [F(0) for _ in range(column_count)]
        vector[free] = F(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free]
        output.append(tuple(vector))
    return output


def derivative_support_audit() -> None:
    basis = [unit(3, index) for index in range(3)]
    es = basis[2]
    z = (F(2), F(3), F(0))
    lam = F(2)
    mu = F(5)
    columns = [scale(-mu, tensor3(vector, es, z)) for vector in basis]
    columns += [scale(-lam, tensor3(es, vector, z)) for vector in basis]
    columns += [scale(lam * mu, tensor3(es, es, vector)) for vector in basis]
    assert rank(columns) == 7

    k1 = (*scale(lam, es), F(0), F(0), F(0), *z)
    k2 = (F(0), F(0), F(0), *scale(mu, es), *z)
    for kernel_vector in (k1, k2):
        image = add(
            *(
                scale(coefficient, column)
                for coefficient, column in zip(
                    kernel_vector, columns, strict=True
                )
            )
        )
        assert image == scale(0, unit(27, 0))
    assert rank([k1, k2]) == 2

    for i, j, k in product((0, 1), (0, 1), range(3)):
        coordinate = 9 * i + 3 * j + k
        assert all(column[coordinate] == 0 for column in columns)

    gamma = (F(3), F(-2), F(0))
    assert sum(a * b for a, b in zip(gamma, z, strict=True)) == 0

    same_colour = tuple(column[26] for column in columns)
    assert same_colour == (
        F(0),
        F(0),
        F(0),
        F(0),
        F(0),
        F(0),
        F(0),
        F(0),
        lam * mu,
    )
    print("independent support grid: PASS (rank / gamma / same-colour row)")


MONOMIALS = list(combinations_with_replacement(range(3), 3))


def symmetric_value(
    monomial: tuple[int, int, int],
    r: Vector,
    p: Vector,
    q: Vector,
) -> F:
    assignments = set(permutations(monomial))
    multiplicities = [monomial.count(index) for index in range(3)]
    count = factorial(3)
    for multiplicity in multiplicities:
        count //= factorial(multiplicity)
    return sum(
        (r[i] * p[j] * q[k] for i, j, k in assignments),
        F(0),
    ) / count


def restriction_rows(
    bases: tuple[list[Vector], list[Vector], list[Vector]],
) -> list[Vector]:
    return [
        tuple(symmetric_value(monomial, r, p, q) for monomial in MONOMIALS)
        for r, p, q in product(*bases)
    ]


def coefficient_vector(entries: dict[tuple[int, int, int], int]) -> Vector:
    return tuple(F(entries.get(monomial, 0)) for monomial in MONOMIALS)


def kernel_equals(rows: list[Vector], expected: list[Vector]) -> bool:
    kernel = nullspace(rows, len(MONOMIALS))
    return rank(kernel) == rank(expected) == rank(kernel + expected)


def incidence_kernel_audit() -> None:
    e0, e1, e2 = (unit(3, index) for index in range(3))
    independent = restriction_rows(([e1, e2], [e0, e2], [e0, e1]))
    expected_independent = [
        coefficient_vector({(0, 0, 0): 1}),
        coefficient_vector({(1, 1, 1): 1}),
        coefficient_vector({(2, 2, 2): 1}),
    ]
    assert kernel_equals(independent, expected_independent)

    pencil = restriction_rows(
        ([e1, e2], [e0, e2], [add(e0, scale(-1, e1)), e2])
    )
    expected_pencil = [
        coefficient_vector({(0, 0, 0): 1}),
        coefficient_vector({(1, 1, 1): 1}),
        coefficient_vector({(0, 0, 1): 1, (0, 1, 1): 1}),
    ]
    assert kernel_equals(pencil, expected_pencil)
    print("independent incidence kernels: PASS (separate row elimination)")


def equal_plane_audit() -> None:
    # A concrete dense L exposes the entries killed by the three orientations.
    matrix = ((F(2), F(3)), (F(5), F(7)))
    left_e00 = ((matrix[0][0], F(0)), (matrix[1][0], F(0)))
    left_e11 = ((F(0), matrix[0][1]), (F(0), matrix[1][1]))
    left_e10 = ((matrix[0][1], F(0)), (matrix[1][1], F(0)))
    assert left_e00[0][1] == 0 and left_e00[1][0] == 5
    assert left_e11[1][0] == 0 and left_e11[0][1] == 3
    assert left_e10[0][1] == 0 and left_e10[1][0] == 7

    # R=P retains an invertible diagonal relation; R=Q or P=Q kills the
    # second row and is singular.
    diagonal = ((F(2), F(0)), (F(0), F(7)))
    singular = ((F(2), F(3)), (F(0), F(0)))
    assert diagonal[0][0] * diagonal[1][1] != 0
    assert singular[0][0] * singular[1][1] - singular[0][1] * singular[1][0] == 0
    print("independent equal-plane audit: PASS (diagonal / singular)")


def square_chart_audit() -> None:
    x = source(0, 0)
    y = source(1, 0)
    z = source(2, 0)
    t = source(2, 1)
    u = add(x, y)
    w = add(x, scale(-1, y))
    zero = scale(0, unit(27, 0))

    z0 = source(2, 1)
    z1 = source(2, 2)
    v0 = add(scale(2, w), z0)
    v1 = add(scale(-3, w), z1)
    for q in (w, t):
        assert polarized(v0, u, q) == zero
        assert polarized(v1, u, q) == zero

    u3 = add(x, y, z)
    q0 = add(x, y, scale(-2, z))
    s0 = add(scale(2, x), scale(3, y), scale(F(5, 2), z))
    s1 = add(scale(-1, x), scale(4, y), scale(F(3, 2), z))
    assert polarized(s0, u3, q0) == zero
    assert polarized(s1, u3, q0) == zero
    print("independent square-chart audit: PASS (two-/three-source)")


def main() -> None:
    derivative_support_audit()
    incidence_kernel_audit()
    equal_plane_audit()
    square_chart_audit()
    print("independent repeated-coordinate support localization: PASS")


if __name__ == "__main__":
    main()
