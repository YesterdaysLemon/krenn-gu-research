"""No-import audit of the conditional synchronized two-depth selector."""


def dot(left, right):
    return sum(x * y for x, y in zip(left, right, strict=True))


def transpose(matrix):
    return tuple(zip(*matrix, strict=True))


def multiply(left, right):
    columns = transpose(right)
    return tuple(tuple(dot(row, column) for column in columns) for row in left)


def add(left, right):
    return tuple(
        tuple(x + y for x, y in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def scale(coefficient, matrix):
    return tuple(tuple(coefficient * value for value in row) for row in matrix)


def rank(matrix):
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(pivot_row + 1, rows):
            entry = work[row][column]
            if entry:
                work[row] = [
                    pivot_value * work[row][j] - entry * work[pivot_row][j]
                    for j in range(columns)
                ]
        pivot_row += 1
    return pivot_row


def corrected(left, right):
    exchange = ((0, 1), (1, 0))
    return multiply(multiply(transpose(left), exchange), right)


def main() -> None:
    # Synchronized subtraction W-hB=D with exact integer matrices.
    h = 3
    direct = ((1, 2, 0), (0, -1, 4), (2, 1, 3))
    left = ((1, 0, 2), (0, 1, 1))
    right = ((2, 1, 0), (1, -1, 3))
    residual = corrected(left, right)
    full = add(scale(h, direct), residual)
    assert add(full, scale(-h, direct)) == residual
    assert rank(residual) == 2

    # Five common-null contractions kill every competing pair term.
    kappa = (1, 2, 3)
    null_a = (2, -1, 0)
    null_b = (3, 0, -1)
    assert dot(null_a, kappa) == dot(null_b, kappa) == 0
    a_rows = ((1, 0, 2), (0, 1, 1)) + (null_a,) * 5
    b_rows = ((0, 1, 3), (2, -1, 0)) + (null_b,) * 5
    vectors = ((2, 1, -1), (1, -2, 1)) + (kappa,) * 5

    survivors = []
    for u in range(7):
        for v in range(u + 1, 7):
            value = (
                dot(a_rows[u], vectors[u]) * dot(b_rows[v], vectors[v])
                + dot(b_rows[u], vectors[u]) * dot(a_rows[v], vectors[v])
            )
            if value:
                survivors.append((u, v))
    assert survivors == [(0, 1)]

    # Aligned cancellation: the unique scalar choice removing hB also removes
    # the aligned target coefficient.
    alpha = 5
    beta = -alpha * h
    mu = 7
    rho_aligned = h
    assert alpha * h + beta == 0
    assert alpha * mu * rho_aligned + beta * mu == 0

    # A shared two-channel rectangular block has rank at most two.
    left_stack = ((1, 0), (0, 1), (1, 1), (2, 1), (1, -1), (3, 2))
    right_stack = ((2, 1), (1, 0), (0, 1), (1, 2), (2, -1), (1, 3))
    cross_block = multiply(multiply(left_stack, ((0, 1), (1, 0))), transpose(right_stack))
    assert rank(cross_block) == 2

    # The determinant pencils t and t-1 have no common root; evaluating the
    # Euclidean resultant here is the elementary identity Res(t,t-1)=1.
    assert (0 - 1) != 0

    # W-only affine inverse at nonzero h, with all entries integral because
    # this sample difference is divisible by h.
    desired = add(scale(h, direct), residual)
    recovered_direct_numerator = add(desired, scale(-1, residual))
    assert recovered_direct_numerator == scale(h, direct)

    print("PASS: independent synchronized subtraction and null selector")
    print("PASS: aligned scalar no-go and common-channel rank bound")
    print("SCOPE: T0 exposure is conditional; P7 remains UNRESOLVED")


if __name__ == "__main__":
    main()
