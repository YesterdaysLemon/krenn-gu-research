"""Independent no-import audit of the residual-hafnian Gram theorem."""

from fractions import Fraction
from itertools import combinations


def hafnian(matrix, vertices=None):
    if vertices is None:
        vertices = tuple(range(len(matrix)))
    vertices = tuple(vertices)
    if not vertices:
        return 1
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first][second] * hafnian(matrix, rest)
    return total


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t] for row in left
    ]


def rank(matrix):
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
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def audit():
    residual_count = 6
    port_count = 4
    port_dimension = 2
    residual = [[0 for _ in range(residual_count)] for _ in range(residual_count)]
    for edge_number, (i, j) in enumerate(combinations(range(residual_count), 2)):
        residual[i][j] = residual[j][i] = 2 + 3 * edge_number

    h = hafnian(residual)
    cofactor = [[0 for _ in range(residual_count)] for _ in range(residual_count)]
    for p, q in combinations(range(residual_count), 2):
        rest = tuple(index for index in range(residual_count) if index not in (p, q))
        cofactor[p][q] = cofactor[q][p] = hafnian(residual, rest)

    maps = []
    for port in range(port_count):
        maps.append(
            [
                [
                    1 + 13 * port + 5 * residual_vertex - 3 * coordinate
                    for coordinate in range(port_dimension)
                ]
                for residual_vertex in range(residual_count)
            ]
        )

    direct_blocks = {}
    corrected_blocks = {}
    for u, v in combinations(range(port_count), 2):
        direct = [
            [7 + 11 * u - 2 * v + 3 * i + j for j in range(port_dimension)]
            for i in range(port_dimension)
        ]
        direct_blocks[u, v] = direct
        corrected = multiply(multiply(transpose(maps[u]), cofactor), maps[v])
        corrected_blocks[u, v] = corrected

        for i in range(port_dimension):
            for j in range(port_dimension):
                size = residual_count + 2
                full = [[0 for _ in range(size)] for _ in range(size)]
                for p in range(residual_count):
                    for q in range(residual_count):
                        full[p][q] = residual[p][q]
                    full[p][residual_count] = full[residual_count][p] = maps[u][p][i]
                    full[p][residual_count + 1] = full[residual_count + 1][p] = maps[v][
                        p
                    ][j]
                full[residual_count][residual_count + 1] = direct[i][j]
                full[residual_count + 1][residual_count] = direct[i][j]
                assert hafnian(full) == h * direct[i][j] + corrected[i][j]

    joined = [
        [value for port in range(port_count) for value in maps[port][row]]
        for row in range(residual_count)
    ]
    completion = multiply(multiply(transpose(joined), cofactor), joined)
    assert rank(completion) <= residual_count

    for u in range(port_count):
        for v in range(port_count):
            block = [
                row[v * port_dimension : (v + 1) * port_dimension]
                for row in completion[u * port_dimension : (u + 1) * port_dimension]
            ]
            expected = multiply(multiply(transpose(maps[u]), cofactor), maps[v])
            assert block == expected


if __name__ == "__main__":
    audit()
    print("residual-hafnian common cofactor Gram independent audit: PASS")
