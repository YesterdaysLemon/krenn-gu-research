"""Independent no-project-import audit of residual Gram sharpness."""

from fractions import Fraction


def hafnian(matrix, vertices=None):
    if vertices is None:
        vertices = tuple(range(len(matrix)))
    if not vertices:
        return 1
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first][partner] * hafnian(matrix, rest)
    return total


def permanent(matrix):
    if not matrix:
        return 1
    total = 0
    first = matrix[0]
    for column, value in enumerate(first):
        remainder = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        total += value * permanent(remainder)
    return total


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def multiply(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def cofactor_matrix(matrix):
    order = len(matrix)
    result = [[0 for _ in range(order)] for _ in range(order)]
    for u in range(order):
        for v in range(u + 1, order):
            rest = tuple(index for index in range(order) if index not in (u, v))
            value = hafnian(matrix, rest)
            result[u][v] = result[v][u] = value
    return result


def sharp_matrix(order):
    result = [[0 if u == v else 1 for v in range(order)] for u in range(order)]
    result[0][1] = result[1][0] = -(order - 2)
    return result


# Fixed q=6 numerical two-port check, written independently of both primaries.
order = 6
residual = [[0 for _ in range(order)] for _ in range(order)]
edge_number = 1
for u in range(order):
    for v in range(u + 1, order):
        residual[u][v] = residual[v][u] = 2 * edge_number - 5
        edge_number += 1
h = hafnian(residual)
cofactor = cofactor_matrix(residual)
left = [[2 + 3 * u - coordinate for coordinate in range(2)] for u in range(order)]
right = [[-1 + 2 * u + 2 * coordinate for coordinate in range(3)] for u in range(order)]
corrected = multiply(multiply(transpose(left), cofactor), right)
direct = [[7 + 3 * u - 2 * v for v in range(3)] for u in range(2)]
for i in range(2):
    for j in range(3):
        full_order = order + 2
        full = [[0 for _ in range(full_order)] for _ in range(full_order)]
        for u in range(order):
            for v in range(order):
                full[u][v] = residual[u][v]
            full[u][order] = full[order][u] = left[u][i]
            full[u][order + 1] = full[order + 1][u] = right[u][j]
        full[order][order + 1] = full[order + 1][order] = direct[i][j]
        assert hafnian(full) == h * direct[i][j] + corrected[i][j]

# Row expansion of the hafnian gives the common Hadamard stress.
for u in range(order):
    assert sum(residual[u][v] * cofactor[u][v] for v in range(order)) == h

# Independent r=2, four-blocker aggregate normalization check.
root_rows = [[1, 2, -1, 3], [0, 1, 4, -2]]
residual_rows = [
    [1 + 2 * p - blocker for blocker in range(4)] for p in range(order)
]
aggregate_left = 0
for u in range(4):
    for v in range(u + 1, 4):
        remaining = [column for column in range(4) if column not in (u, v)]
        root_minor = [[row[column] for column in remaining] for row in root_rows]
        corrected_pair = sum(
            residual_rows[p][u] * cofactor[p][q] * residual_rows[q][v]
            for p in range(order)
            for q in range(order)
        )
        aggregate_left += permanent(root_minor) * corrected_pair

aggregate_right = 0
for p in range(order):
    for q in range(p + 1, order):
        extension = root_rows + [residual_rows[p], residual_rows[q]]
        aggregate_right += cofactor[p][q] * permanent(extension)
assert aggregate_left == aggregate_right

# Exact full-rank zero-hafnian controls, including complete support at q>=4.
for sharp_order in (4, 6, 8):
    sharp = sharp_matrix(sharp_order)
    assert hafnian(sharp) == 0
    assert all(sharp[u][v] != 0 for u in range(sharp_order) for v in range(u + 1, sharp_order))
    sharp_cofactor = cofactor_matrix(sharp)
    assert matrix_rank(sharp_cofactor) == sharp_order
    for u in range(sharp_order):
        stress_row = sum(
            sharp[u][v] * sharp_cofactor[u][v] for v in range(sharp_order)
        )
        assert stress_row == 0

assert matrix_rank([[0, 1], [1, 0]]) == 2

print("independent arbitrary-residual two-port factorization: PASS")
print("independent root-permanent aggregate normalization: PASS")
print("independent Hadamard-stress audit: PASS")
print("independent torus-zero full-rank controls: PASS")
print("GLOBAL KRENN-GU STATUS: UNRESOLVED")
