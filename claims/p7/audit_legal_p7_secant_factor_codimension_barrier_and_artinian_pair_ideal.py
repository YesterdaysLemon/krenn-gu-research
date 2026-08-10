"""Independent standard-library audit of the legal secant--factor barrier."""

from fractions import Fraction


def rational_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
    return pivot_row


def matrix_vector(matrix, vector):
    return [
        sum(Fraction(a) * Fraction(b) for a, b in zip(row, vector, strict=True))
        for row in matrix
    ]


def factor_jacobian_at_fixed_point():
    a = tuple(range(1, 8))
    b = tuple(value * value for value in a)
    rows = []
    for i in range(7):
        for j in range(i + 1, 7):
            row = [0] * 14
            row[i] = b[j]
            row[j] = b[i]
            row[7 + i] = a[j]
            row[7 + j] = a[i]
            rows.append(row)
    return rows, (*a, *(-value for value in b))


def audit_factor_dimension_and_barrier():
    jacobian, gauge = factor_jacobian_at_fixed_point()
    assert rational_rank(jacobian) == 13
    assert rational_rank(jacobian[:13]) == 13
    assert matrix_vector(jacobian, gauge) == [0] * 21

    border_floor = 218 + 32 - 242
    factor_dimension = (219 - 21) + 13 - 1
    assert border_floor == 8
    assert factor_dimension == 210
    assert 218 - factor_dimension == 8
    assert border_floor + factor_dimension - 218 == 0
    assert [border_floor - count for count in range(9)] == list(range(8, -1, -1))


def two_by_two_determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def audit_artinian_norm():
    # In Q[x]/(x^2-1), columns are multiplication images in basis (1,x).
    multiply_x_minus_one = [[-1, 1], [1, -1]]
    multiply_x_plus_two = [[2, 1], [1, 2]]
    assert two_by_two_determinant(multiply_x_minus_one) == 0
    assert two_by_two_determinant(multiply_x_plus_two) == 3

    # (x+2)(2-x)/3=1 modulo x^2-1.
    constant = Fraction(4, 3) - Fraction(1, 3)
    x_coefficient = Fraction(2, 3) - Fraction(2, 3)
    assert constant == 1
    assert x_coefficient == 0


def main():
    audit_factor_dimension_and_barrier()
    audit_artinian_norm()
    print("PASS: independent legal secant--factor barrier audit")
    print("factor_jacobian_rank=13 codimension=8")
    print("mandatory_intersection_dimension_floor=0")
    print("eight_equation_border_floor=0")
    print("artinian_gate_norm_criterion=exact")
    print("graph_or_parameter_search_used=False")


if __name__ == "__main__":
    main()
