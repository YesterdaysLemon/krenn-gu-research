"""Independent no-project-import audit of the zeon catalecticant theorem."""

from fractions import Fraction
from functools import cache
from itertools import combinations
from math import comb


def permanent(matrix):
    size = len(matrix)
    states = {0: Fraction(1)}
    for row in range(size):
        next_states = {}
        for mask, coefficient in states.items():
            for column in range(size):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                next_states[new_mask] = next_states.get(
                    new_mask, Fraction(0)
                ) + coefficient * matrix[row][column]
        states = next_states
    return states[(1 << size) - 1]


def hafnian(matrix):
    @cache
    def recurrence(vertices):
        if not vertices:
            return Fraction(1)
        if len(vertices) % 2:
            return Fraction(0)
        first = vertices[0]
        total = Fraction(0)
        for position in range(1, len(vertices)):
            second = vertices[position]
            remainder = vertices[1:position] + vertices[position + 1 :]
            total += matrix[first][second] * recurrence(remainder)
        return total

    return recurrence(tuple(range(len(matrix))))


def submatrix(matrix, rows, columns):
    return [[matrix[row][column] for column in columns] for row in rows]


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def multiply(left, right):
    return [
        [
            sum(
                (left[row][middle] * right[middle][column]
                 for middle in range(len(right))),
                Fraction(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def transpose(matrix):
    return [list(column) for column in zip(*matrix, strict=True)]


def phi_coefficient(residual, incidence, ports):
    residual_order = len(residual)
    degree = len(ports)
    if degree % 2 or degree > residual_order:
        return Fraction(0)
    total = Fraction(0)
    for used_rows in combinations(range(residual_order), degree):
        unused = tuple(row for row in range(residual_order) if row not in used_rows)
        total += hafnian(submatrix(residual, unused, unused)) * permanent(
            submatrix(incidence, used_rows, ports)
        )
    return total


def audit_all_depth_factorization() -> None:
    residual_order = 4
    residual = [
        [Fraction(0), Fraction(2), Fraction(3), Fraction(5)],
        [Fraction(2), Fraction(0), Fraction(7), Fraction(11)],
        [Fraction(3), Fraction(7), Fraction(0), Fraction(13)],
        [Fraction(5), Fraction(11), Fraction(13), Fraction(0)],
    ]
    left_count = 5
    right_count = 4
    parameters = tuple(range(1, left_count + right_count + 1))
    incidence = [
        [Fraction(parameter**row) for parameter in parameters]
        for row in range(residual_order)
    ]
    left_pairs = tuple(combinations(range(left_count), 2))
    right_columns = ((),) + tuple(
        combinations(range(left_count, left_count + right_count), 2)
    )
    catalecticant = [
        [
            phi_coefficient(residual, incidence, left_pair + right_set)
            for right_set in right_columns
        ]
        for left_pair in left_pairs
    ]

    residual_pairs = tuple(combinations(range(residual_order), 2))
    p_two = [
        [permanent(submatrix(incidence, rows, ports)) for ports in left_pairs]
        for rows in residual_pairs
    ]
    middle = []
    for marked_rows in residual_pairs:
        complement = tuple(
            row for row in range(residual_order) if row not in marked_rows
        )
        row = [hafnian(submatrix(residual, complement, complement))]
        row.extend(
            permanent(submatrix(incidence, complement, right_set))
            for right_set in right_columns[1:]
        )
        middle.append(row)

    assert catalecticant == multiply(transpose(p_two), middle)
    assert rank(catalecticant) == comb(residual_order, 2) == 6
    assert len(catalecticant) == comb(left_count, 2)
    assert len(catalecticant[0]) == 1 + comb(right_count, 2)


def audit_symmetric_square_refinement() -> None:
    residual_order = 4
    source = [
        [Fraction(1), Fraction(2)],
        [Fraction(3), Fraction(5)],
        [Fraction(7), Fraction(11)],
        [Fraction(13), Fraction(17)],
    ]
    coordinates = [
        [Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5)],
        [Fraction(2), Fraction(3), Fraction(5), Fraction(7), Fraction(11)],
    ]
    incidence = multiply(source, coordinates)
    row_pairs = tuple(combinations(range(residual_order), 2))
    port_pairs = tuple(combinations(range(len(coordinates[0])), 2))
    p_two = [
        [permanent(submatrix(incidence, rows, ports)) for ports in port_pairs]
        for rows in row_pairs
    ]
    source_square = []
    for first, second in row_pairs:
        source_square.append(
            [
                source[first][0] * source[second][0],
                source[first][0] * source[second][1]
                + source[first][1] * source[second][0],
                source[first][1] * source[second][1],
            ]
        )
    coordinate_square = [[], [], []]
    for first, second in port_pairs:
        coordinate_square[0].append(
            2 * coordinates[0][first] * coordinates[0][second]
        )
        coordinate_square[1].append(
            coordinates[0][first] * coordinates[1][second]
            + coordinates[1][first] * coordinates[0][second]
        )
        coordinate_square[2].append(
            2 * coordinates[1][first] * coordinates[1][second]
        )
    assert p_two == multiply(source_square, coordinate_square)
    assert rank(p_two) == comb(2 + 1, 2) == 3


def audit_q6_middle_sharpness() -> None:
    residual_order = 6
    marked_order = 3
    marked_sets = tuple(combinations(range(residual_order), marked_order))
    complement_sets = tuple(
        combinations(range(residual_order), residual_order - marked_order)
    )
    block = []
    for marked in marked_sets:
        row = []
        for other in complement_sets:
            selected = marked + other
            identity_columns = [
                [Fraction(int(row_index == column_index)) for column_index in selected]
                for row_index in range(residual_order)
            ]
            row.append(permanent(identity_columns))
        block.append(row)
    assert rank(block) == comb(residual_order, marked_order) == 20


def main() -> None:
    audit_all_depth_factorization()
    audit_symmetric_square_refinement()
    audit_q6_middle_sharpness()
    print("AUDIT PASS: q=4 k=2 all-depth factorization has sharp rank six")
    print("AUDIT PASS: rank-two incidence factors through three symmetric squares")
    print("AUDIT PASS: q=6 k=3 doubled identity has complement rank twenty")
    print("AUDIT SCOPE: legal synchronized GHZ deletion charts remain unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
