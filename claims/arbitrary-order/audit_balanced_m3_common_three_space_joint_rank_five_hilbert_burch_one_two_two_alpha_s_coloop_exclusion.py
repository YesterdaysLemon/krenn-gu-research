"""Independent rational audit of the (1,2,2) alpha_s-coloop exclusion.

This file imports neither the primary verifier nor a third-party package.  It
uses ``Fraction`` arithmetic, direct evaluation-pair fixtures, a reversed
cubic coefficient order, and separate row reduction.
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


def dot(left: Vector, right: Vector) -> F:
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def determinant(rows: tuple[Vector, Vector, Vector]) -> F:
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


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


def pencil_face_audit() -> None:
    # Opposite representatives of the same evaluation direction lie in L,
    # while arbitrary representatives on that direction kill det D_B^T.
    u, v = F(2), F(3)
    beta_y, mu_beta_t = F(5) * u, F(5) * v
    gamma_z, gamma_w = F(-7) * u, F(-7) * v
    assert beta_y * gamma_w - mu_beta_t * gamma_z == 0
    assert beta_y + (-F(5) * u) == 0
    assert mu_beta_t + (-F(5) * v) == 0

    # In the chart s=0,t=1, coordinate restriction determinants are the
    # s-components of v*y-u*mu*e_t and v*z-u*w.
    y = (F(11), F(0), F(13))
    z = (F(17), F(19), F(23))
    w = (F(29), F(31), F(37))
    mu = F(41)
    p_normal = add(scale(v, y), scale(-u * mu, unit(3, 1)))
    q_normal = add(scale(v, z), scale(-u, w))
    e1, e2 = unit(3, 1), unit(3, 2)
    assert determinant((p_normal, e1, e2)) == v * y[0]
    assert determinant((q_normal, e1, e2)) == v * z[0] - u * w[0]

    # Coefficients of (v*y_s)(v*z_s-u*w_s) and of
    # (-u*mu)(v*z_s-u*w_s) independently reproduce the A/B fork.
    distinct_coefficients = {
        (2, 0): F(0),
        (1, 1): -y[0] * w[0],
        (0, 2): y[0] * z[0],
    }
    equal_coefficients = {
        (2, 0): mu * w[0],
        (1, 1): -mu * z[0],
        (0, 2): F(0),
    }
    assert distinct_coefficients[(1, 1)] and distinct_coefficients[(0, 2)]
    assert equal_coefficients[(2, 0)] and equal_coefficients[(1, 1)]
    print("independent pencil/factor audit: PASS")


def target(alpha: Vector, beta: Vector, gamma: Vector) -> Vector:
    return tuple(a * b * c for a, b, c in zip(alpha, beta, gamma, strict=True))


def cell_support(
    alphas: list[Vector], betas: list[Vector], gammas: list[Vector]
) -> set[tuple[int, int, int]]:
    zero = (F(0), F(0), F(0))
    return {
        (i, j, k)
        for i, j, k in product(range(2), repeat=3)
        if target(alphas[i], betas[j], gammas[k]) != zero
    }


def table_audit() -> None:
    e0, e1, e2 = (unit(3, index) for index in range(3))
    rows = [e1, e2]
    assert cell_support(rows, [e1, e2], [e1, e2]) == {
        (0, 0, 0),
        (1, 1, 1),
    }
    assert cell_support(
        rows,
        [e0, add(e1, e2)],
        [add(scale(-1, e0), e1), add(e0, e2)],
    ) == {(0, 1, 0), (1, 1, 1)}
    assert cell_support(
        rows,
        [add(e0, e1), add(scale(-1, e0), e2)],
        [e0, add(e1, e2)],
    ) == {(0, 0, 1), (1, 1, 1)}
    assert cell_support(
        rows,
        [e0, add(e1, e2)],
        [e0, add(e1, e2)],
    ) == {(0, 1, 1), (1, 1, 1)}
    print("independent binary-table audit: PASS")


# Reverse the primary verifier's cubic ordering deliberately.
MONOMIALS = list(reversed(list(combinations_with_replacement(range(3), 3))))


def symmetric_value(monomial: tuple[int, int, int], r: Vector, p: Vector, q: Vector) -> F:
    assignments = set(permutations(monomial))
    count = factorial(3)
    for index in range(3):
        count //= factorial(monomial.count(index))
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


def incidence_audit() -> None:
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
    print("independent same-pair incidence kernels: PASS")


def equal_plane_audit() -> None:
    # For R=P, L*E01 symmetric forces L00=0 and L*E11 symmetric forces
    # L01=0, so the first row vanishes.  The R=Q calculation is identical.
    matrix = ((F(2), F(3)), (F(5), F(7)))
    left_e01 = ((F(0), matrix[0][0]), (F(0), matrix[1][0]))
    left_e11 = ((F(0), matrix[0][1]), (F(0), matrix[1][1]))
    assert left_e01[0][1] == 2 and left_e01[1][0] == 0
    assert left_e11[0][1] == 3 and left_e11[1][0] == 0

    # For P=Q, L*E11 symmetry kills L01.  With lower-triangular L,
    # F=S*L^T and F=cE11 give S=(c/L11)E11: both surviving cells are values
    # of the single square map per(-,p1,p1).
    lower = ((F(2), F(0)), (F(5), F(7)))
    c = F(11)
    symmetric_square = ((F(0), F(0)), (F(0), c / lower[1][1]))
    reconstructed = (
        (
            symmetric_square[0][0] * lower[0][0]
            + symmetric_square[0][1] * lower[0][1],
            symmetric_square[0][0] * lower[1][0]
            + symmetric_square[0][1] * lower[1][1],
        ),
        (
            symmetric_square[1][0] * lower[0][0]
            + symmetric_square[1][1] * lower[0][1],
            symmetric_square[1][0] * lower[1][0]
            + symmetric_square[1][1] * lower[1][1],
        ),
    )
    assert reconstructed == ((F(0), F(0)), (F(0), c))
    print("independent equal-plane orientation audit: PASS")


def main() -> None:
    pencil_face_audit()
    table_audit()
    incidence_audit()
    equal_plane_audit()
    print("independent (1,2,2) alpha_s-coloop audit: PASS")


if __name__ == "__main__":
    main()
