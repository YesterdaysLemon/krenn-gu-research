"""Independent no-import audit of the residual-relative response theorem."""

from fractions import Fraction
from functools import cache
from itertools import combinations


def multiply(left, right):
    product = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            product[mask] = product.get(mask, 0) + left_value * right_value
    return product


def wick_exponential(edges):
    result = {0: 1}
    for (first, second), weight in edges.items():
        edge_mask = (1 << first) | (1 << second)
        result = multiply(result, {0: 1, edge_mask: weight})
    return result


def response_with_residuals(moments, port_count, residual_count):
    residual_mask = ((1 << residual_count) - 1) << port_count
    return {
        port_mask: moments.get(port_mask | residual_mask, 0)
        for port_mask in range(1 << port_count)
    }


def hafnian_from_edges(vertices, edge_value):
    vertices = tuple(vertices)

    @cache
    def recurrence(remaining):
        if not remaining:
            return 1
        if len(remaining) % 2:
            return 0
        first = remaining[0]
        total = 0
        for position in range(1, len(remaining)):
            second = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += edge_value(first, second) * recurrence(rest)
        return total

    return recurrence(vertices)


def permanent_from_rows(rows, columns, entry):
    rows = tuple(rows)
    columns = tuple(columns)
    if len(rows) != len(columns):
        return 0

    @cache
    def recurrence(row_index, remaining_columns):
        if row_index == len(rows):
            return 1
        total = 0
        for position, column in enumerate(remaining_columns):
            rest = remaining_columns[:position] + remaining_columns[position + 1 :]
            total += entry(rows[row_index], column) * recurrence(row_index + 1, rest)
        return total

    return recurrence(0, columns)


def matrix_rank(matrix):
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
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
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
        if pivot_row == rows:
            break
    return pivot_row


def matrix_multiply(left, right):
    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def transpose(matrix):
    return [list(column) for column in zip(*matrix, strict=True)]


def main():
    port_count = 6
    residual_count = 4

    def port_weight(first, second):
        return 2 + 3 * first + 5 * second

    def residual_weight(first, second):
        return 1 + 2 * first + 7 * second

    def incidence_weight(residual, port):
        return 1 + residual + 2 * port + residual * port

    port_edges = {
        (first, second): port_weight(first, second)
        for first in range(port_count)
        for second in range(first + 1, port_count)
    }
    full_edges = dict(port_edges)
    for first in range(residual_count):
        for second in range(first + 1, residual_count):
            full_edges[(port_count + first, port_count + second)] = residual_weight(
                first, second
            )
    for residual in range(residual_count):
        for port in range(port_count):
            full_edges[(port, port_count + residual)] = incidence_weight(residual, port)

    base = wick_exponential(port_edges)
    response = response_with_residuals(
        wick_exponential(full_edges), port_count, residual_count
    )

    relative = {}
    residual_vertices = tuple(range(residual_count))
    for size in (0, 2, 4):
        for ports in combinations(range(port_count), size):
            value = 0
            for used_residuals in combinations(residual_vertices, size):
                unused = tuple(
                    vertex
                    for vertex in residual_vertices
                    if vertex not in used_residuals
                )
                residual_hafnian = hafnian_from_edges(unused, residual_weight)
                incidence_permanent = permanent_from_rows(
                    used_residuals, ports, incidence_weight
                )
                value += residual_hafnian * incidence_permanent
            mask = sum(1 << port for port in ports)
            relative[mask] = value

    reconstructed = multiply(base, relative)
    for mask in range(1 << port_count):
        assert response[mask] == reconstructed.get(mask, 0)
    assert all(mask.bit_count() <= residual_count for mask in relative)

    # Independent q=2 four- and six-point insertion recurrence.
    six_ports = 6
    base_edges = {
        (first, second): 1 + first + 4 * second
        for first in range(six_ports)
        for second in range(first + 1, six_ports)
    }
    base_six = wick_exponential(base_edges)
    a = tuple(2 + index for index in range(six_ports))
    b = tuple(3 + 2 * index for index in range(six_ports))
    pair = {
        (first, second): a[first] * b[second] + b[first] * a[second]
        for first in range(six_ports)
        for second in range(first + 1, six_ports)
    }
    quadratic = {
        (1 << first) | (1 << second): value
        for (first, second), value in pair.items()
    }
    tangent = multiply(base_six, quadratic)
    for size in (4, 6):
        for ports in combinations(range(six_ports), size):
            mask = sum(1 << port for port in ports)
            expected = 0
            for first, second in combinations(ports, 2):
                complement = mask ^ (1 << first) ^ (1 << second)
                expected += pair[(first, second)] * base_six.get(complement, 0)
            assert tangent.get(mask, 0) == expected

    # Cross-depth q=4 rank on disjoint port charts.  The left and right
    # incidence matrices are Vandermonde charts of ranks four.
    left_count = 5
    right_count = 4
    residual_order = 4
    left_incidence = [
        [(column + 1) ** row for column in range(left_count)]
        for row in range(residual_order)
    ]
    right_incidence = [
        [(column + 2) ** row for column in range(right_count)]
        for row in range(residual_order)
    ]
    cofactor = []
    for first in range(residual_order):
        row = []
        for second in range(residual_order):
            if first == second:
                row.append(0)
                continue
            remaining = [
                index
                for index in range(residual_order)
                if index not in (first, second)
            ]
            row.append(residual_weight(remaining[0], remaining[1]))
        cofactor.append(row)

    degree_two = matrix_multiply(
        matrix_multiply(transpose(left_incidence), cofactor), right_incidence
    )
    degree_four_middle = []
    for omitted in range(residual_order):
        rows = tuple(row for row in range(residual_order) if row != omitted)
        degree_four_middle.append(
            [
                permanent_from_rows(
                    rows,
                    columns,
                    lambda row, column: right_incidence[row][column],
                )
                for columns in combinations(range(right_count), 3)
            ]
        )
    degree_four = matrix_multiply(
        transpose(left_incidence), degree_four_middle
    )
    combined = [
        degree_two[row] + degree_four[row] for row in range(left_count)
    ]
    assert matrix_rank(degree_two) == residual_order
    assert matrix_rank(combined) == residual_order

    print("independent residual-relative response audit: PASS")
    print("integer square-zero products, subset recurrences, and cross-depth rank")


if __name__ == "__main__":
    main()
