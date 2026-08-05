"""Independent no-project-import audit of cross-root coordinate charts."""

from fractions import Fraction


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def multiply(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def inverse(matrix):
    order = len(matrix)
    augmented = [
        [Fraction(value) for value in row]
        + [Fraction(int(i == j)) for j in range(order)]
        for i, row in enumerate(matrix)
    ]
    for column in range(order):
        pivot = next(row for row in range(column, order) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        augmented[column] = [entry / value for entry in augmented[column]]
        for row in range(order):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(augmented[row], augmented[column])
            ]
    return [row[order:] for row in augmented]


coordinates = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
v = (1, 1, 1)
planes = (
    ((1, 1), (1, 0), (1, 0)),
    ((1, 0), (1, 0), (1, 1)),
    ((1, 0), (1, 1), (1, 0)),
)
normals = ((0, 1, -1), (1, -1, 0), (1, 0, -1))

# Plane equations and coordinate identifications.
for label in range(3):
    plane = planes[label]
    normal = [list(normals[label])]
    assert multiply(normal, plane) == [[0, 0]]
    base_coordinate = multiply([list(coordinates[0])], plane)
    label_coordinate = multiply([list(coordinates[label])], plane)
    assert base_coordinate == label_coordinate

edge = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
for left_label in range(3):
    for right_label in range(3):
        restricted = multiply(multiply(transpose(planes[left_label]), edge), planes[right_label])
        left_coordinate = multiply([list(coordinates[left_label])], planes[left_label])[0]
        right_coordinate = multiply([list(coordinates[right_label])], planes[right_label])[0]
        expected = [[a * b for b in right_coordinate] for a in left_coordinate]
        assert restricted == expected

# Pairwise plane intersections have rank-two normals and contain the torus line.
for first, second in ((0, 1), (0, 2), (1, 2)):
    pair = [list(normals[first]), list(normals[second])]
    assert rank(pair) == 2
    assert multiply(pair, [[entry] for entry in v]) == [[0], [0]]

# Independent gate check with fully supported on/off root vectors.
omega = (1, -1, 0)
x_off = (1, 1, 1)
x_on = (2, 1, 1)
assert sum(a * b for a, b in zip(omega, x_off)) == 0
assert sum(a * b for a, b in zip(omega, x_on)) == 1
blocker_endpoint = (0, 0, 1)
assert sum(a * b for a, b in zip(blocker_endpoint, x_off)) == 1
assert sum(a * b for a, b in zip(blocker_endpoint, x_on)) == 1
for active in range(3):
    incidence = []
    for root in range(3):
        vector = x_on if root == active else x_off
        scalar = sum(a * b for a, b in zip(omega, vector))
        incidence.append([scalar * entry for entry in normals[root]])
    assert rank(incidence) == 1
    assert multiply(incidence, planes[active]) == [[0, 0], [0, 0], [0, 0]]

# Nine independent torus evaluation tensors.
x_rows = [[1, t, t * t] for t in (1, 2, 3)]
y_rows = [[1, t, t * t] for t in (4, 5, 6)]
evaluation = []
for x in x_rows:
    for y in y_rows:
        evaluation.append([a * b for a in x for b in y])
assert rank(evaluation) == 9

# Arbitrary rational value interpolation through B=X^-1 H Y^-T.
values = [[2, -3, 5], [7, 11, -13], [17, -19, 23]]
x_inverse = inverse(x_rows)
y_inverse = inverse(y_rows)
interpolated = multiply(multiply(x_inverse, values), transpose(y_inverse))
assert multiply(multiply(x_rows, interpolated), transpose(y_rows)) == values

# Every coordinate label is valid on every torus line by scalar renormalization.
for i in range(3):
    for j in range(3):
        for left_label in range(3):
            for right_label in range(3):
                denominator = x_rows[i][left_label] * y_rows[j][right_label]
                assert denominator != 0
                scalar = Fraction(values[i][j], denominator)
                assert scalar * denominator == values[i][j]

print("independent plane-overlap and coordinate-label audit: PASS")
print("independent gated root-kernel audit: PASS")
print("independent nine-evaluation rank audit: PASS")
print("independent arbitrary-value interpolation: PASS")
print("GLOBAL KRENN-GU STATUS: UNRESOLVED")
