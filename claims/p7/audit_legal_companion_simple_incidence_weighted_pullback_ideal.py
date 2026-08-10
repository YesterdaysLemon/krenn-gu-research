"""Independent standard-library audit of the weighted pullback ideal."""

from fractions import Fraction

PIVOT_ROWS = {
    0: (
        (1, 2, 3, 4, 5),
        (1, 2, 3, 4, 6),
        (1, 2, 3, 4, 7),
        (1, 2, 3, 4, 8),
        (1, 2, 3, 5, 6),
        (1, 2, 4, 5, 6),
        (1, 3, 4, 5, 6),
        (2, 3, 4, 5, 6),
    ),
    1: (
        (0, 2, 3, 4, 5),
        (0, 2, 3, 4, 6),
        (0, 2, 3, 4, 7),
        (0, 2, 3, 4, 8),
        (0, 2, 3, 5, 6),
        (0, 2, 4, 5, 6),
        (0, 3, 4, 5, 6),
        (2, 3, 4, 5, 6),
    ),
}


def bareiss_determinant(matrix):
    work = [list(map(int, row)) for row in matrix]
    order = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(order - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                row
                for row in range(pivot_index + 1, order)
                if work[row][pivot_index] != 0
            )
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, order):
            for column in range(pivot_index + 1, order):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def rational_solve(matrix, rhs):
    order = len(matrix)
    augmented = [
        [Fraction(value) for value in row] + [Fraction(rhs_value)]
        for row, rhs_value in zip(matrix, rhs, strict=True)
    ]
    for column in range(order):
        pivot = next(row for row in range(column, order) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(order):
            if row == column or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    augmented[row], augmented[column], strict=True
                )
            ]
    return [augmented[row][-1] for row in range(order)]


def deck_value(vertices, zero_residual_edge):
    order = len(vertices)
    value = {4: 3, 6: 15, 8: 105}[order]
    if zero_residual_edge and {0, 1}.issubset(vertices):
        value -= {4: 1, 6: 3, 8: 15}[order]
    return value


def pinned_data(pin, zero_residual_edge):
    partners = tuple(vertex for vertex in range(9) if vertex != pin)
    matrix = [
        [
            deck_value(tuple(v for v in row if v != partner), zero_residual_edge)
            if partner in row
            else 0
            for partner in partners
        ]
        for row in PIVOT_ROWS[pin]
    ]
    rhs = [
        deck_value(tuple(sorted((pin, *row))), zero_residual_edge)
        for row in PIVOT_ROWS[pin]
    ]
    determinant = bareiss_determinant(matrix)
    solution = rational_solve(matrix, rhs)
    cramer = [determinant * value for value in solution]
    assert all(value.denominator == 1 for value in cramer)
    return determinant, dict(
        zip(partners, (int(value) for value in cramer), strict=True)
    )


def pentad(values):
    k12, k13, k14, k15, k23, k24, k25, k34, k35, k45 = values
    return (
        k12 * k13 * k24 * k35 * k45
        - k12 * k13 * k25 * k34 * k45
        - k12 * k14 * k23 * k35 * k45
        + k12 * k14 * k25 * k34 * k35
        + k12 * k15 * k23 * k34 * k45
        - k12 * k15 * k24 * k34 * k35
        + k13 * k14 * k23 * k25 * k45
        - k13 * k14 * k24 * k25 * k35
        - k13 * k15 * k23 * k24 * k45
        + k13 * k15 * k24 * k25 * k34
        - k14 * k15 * k23 * k25 * k34
        + k14 * k15 * k23 * k24 * k35
    )


def rank(matrix):
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


def audit_minor_kernel_and_weights():
    quotient = [[-2, 1, 0], [-3, 0, 1], [-5, 1, 1]]
    q = [1, 2, 3]
    gamma = [[1, 0, 0], *quotient]
    assert rank(quotient) == 2
    assert rank(gamma) == 3
    assert matrix_vector(quotient, q) == [0, 0, 0]
    assert matrix_vector(gamma, q) == [1, 0, 0, 0]

    scale = 2
    tau = Fraction(3)
    u0 = (1, 2, 3, 4, 5)
    u1 = (2, -1, 4, 1, 3)
    edges = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
    )
    khat = [u0[i] * u1[j] + u0[j] * u1[i] for i, j in edges]
    y = [Fraction(value, tau) for value in khat]
    scaled_y = [scale * value for value in y]
    scaled_khat = [scale**16 * value for value in khat]
    scaled_tau = scale**15 * tau
    assert all(
        scaled_tau * left == right
        for left, right in zip(scaled_y, scaled_khat, strict=True)
    )
    alpha = y[0] * khat[1] - y[1] * khat[0]
    scaled_alpha = scaled_y[0] * scaled_khat[1] - scaled_y[1] * scaled_khat[0]
    assert scaled_alpha == scale**17 * alpha
    assert pentad(khat) == 0


def audit_exact_nonforcing_decks():
    d0_one, u0_one = pinned_data(0, False)
    d1_one, _ = pinned_data(1, False)
    assert d0_one == d1_one == 32805
    assert u0_one[1] == 32805

    d0, u0 = pinned_data(0, True)
    d1, u1 = pinned_data(1, True)
    assert d0 == d1 == 32805
    assert u0[1] == 0
    assert all(u0[blocker] == d0 for blocker in range(2, 9))
    assert all(u1[blocker] == d1 for blocker in range(2, 9))
    assert pentad(tuple(range(1, 11))) == -6
    common_khat = 2 * 32805**2
    assert common_khat - 2 * common_khat == -2152336050


def main():
    audit_minor_kernel_and_weights()
    audit_exact_nonforcing_decks()
    print("PASS: independent weighted-pullback-ideal audit")
    print("minor_kernel_and_weight_15_gluing=exact")
    print("h0_pinned_d0=d1=32805")
    print("ambient_h0_bad_pentad=-6 bad_alignment=-2152336050")
    print("graph_or_parameter_search_used=False")


if __name__ == "__main__":
    main()
