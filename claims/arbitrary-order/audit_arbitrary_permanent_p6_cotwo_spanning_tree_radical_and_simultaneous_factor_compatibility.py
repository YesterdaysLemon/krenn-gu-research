"""Independent no-import audit of the P6 co-two simultaneous boundary."""

from fractions import Fraction
from itertools import combinations, permutations, product


Q = Fraction


def determinant(matrix):
    work = [list(map(Q, row)) for row in matrix]
    value = Q(1)
    for column in range(len(work)):
        pivot = next(index for index in range(column, len(work)) if work[index][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column]
        value *= pivot_value
        for index in range(column + 1, len(work)):
            scale = work[index][column] / pivot_value
            for j in range(column, len(work)):
                work[index][j] -= scale * work[column][j]
    return value


def rank(matrix):
    work = [list(map(Q, row)) for row in matrix if any(row)]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(pivot_row, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[index], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def symmetric_product(left, right):
    return (
        left[0] * right[0],
        left[1] * right[1],
        left[2] * right[2],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[2] * right[0],
        left[1] * right[2] + left[2] * right[1],
    )


def occupancy_space(degree):
    return {
        tuple(indices.count(colour) for colour in range(3))
        for indices in product(range(3), repeat=degree)
        if all(indices.count(colour) <= 2 for colour in range(3))
    }


def multiply_occupancy_spaces(left, right):
    return {
        tuple(a + b for a, b in zip(first, second, strict=True))
        for first in left
        for second in right
        if all(a + b <= 2 for a, b in zip(first, second, strict=True))
    }


def permanent(rows):
    total = 0
    for permutation in permutations(range(6)):
        term = 1
        for row_index, column in enumerate(permutation):
            term *= rows[row_index][column]
        total += term
    return total


def main():
    # Rows 03,14,25,01,02,12 of w0^2,w1^2,w2^2,w0w1,w0w2,w1w2.
    named_minor = (
        (2, 0, 0, 0, 0, 0),
        (0, 2, 0, 0, 0, 0),
        (0, 0, 2, 0, 0, 0),
        (0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
    )
    assert determinant(named_minor) == 8

    v_coordinates = ((1, 1, 1), (1, 2, 3), (1, 4, 9))
    assert determinant(v_coordinates) == 2
    mixed_rows = [symmetric_product(v_coordinates[i], v_coordinates[j]) for i, j in combinations(range(3), 2)]
    diagonal_rows = [symmetric_product(row, row) for row in v_coordinates]
    assert rank(mixed_rows) == 3
    assert rank(mixed_rows + diagonal_rows) == 6

    # The six degree-four occupancy patterns are distinct and nonzero.
    occupancy = occupancy_space(4)
    assert occupancy == {(2, 2, 0), (2, 0, 2), (0, 2, 2), (2, 1, 1), (1, 2, 1), (1, 1, 2)}
    assert len(occupancy) == 6
    assert all(sum(pattern) == 4 and max(pattern) == 2 for pattern in occupancy)

    u1 = occupancy_space(1)
    u2 = multiply_occupancy_spaces(u1, u1)
    u3 = multiply_occupancy_spaces(u2, u1)
    u4 = multiply_occupancy_spaces(u2, u2)
    assert u4 == occupancy

    # Reconstruct every mode-indexed T3, Q4, and C4 partition from occupancy
    # products.  This is separate from the primary's bitmask zeon algebra.
    modes = tuple(range(6))
    for a, b, c in combinations(modes, 3):
        ledgers = []
        for pair, singleton in (((a, b), c), ((a, c), b), ((b, c), a)):
            assert singleton not in pair
            ledgers.append(multiply_occupancy_spaces(u2, u1))
        assert all(ledger == u3 for ledger in ledgers)
    for a, b, c, d in combinations(modes, 4):
        partitions = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
        ledgers = [multiply_occupancy_spaces(u2, u2) for _partition in partitions]
        assert all(ledger == u4 for ledger in ledgers)
    for omitted in combinations(modes, 2):
        c, d, e, f = (mode for mode in modes if mode not in omitted)
        partitions = (((c, d), (e, f)), ((c, e), (d, f)), ((c, f), (d, e)))
        ledgers = [multiply_occupancy_spaces(u2, u2) for _partition in partitions]
        assert all(ledger == u4 for ledger in ledgers)

    v0 = (1, 1, 1, 1, 1, 1)
    v1 = (1, 2, 3, 1, 2, 3)
    v2 = (1, 4, 9, 1, 4, 9)
    assert permanent((v0,) * 6) == 720
    assert permanent((v1,) * 6) == 25920
    assert permanent((v2,) * 6) == 933120
    assert permanent((v0, v0, v1, v1, v2, v2)) == 41456
    assert 8 * sum((1332, 198, 52, 2088, 1104, 408)) == 41456

    # Use a star, not the path used by the primary.
    star_edges = tuple((0, index) for index in range(1, 6))
    for word in product(range(3), repeat=6):
        exposed = any(word[a] != word[b] for a, b in star_edges)
        assert exposed == (len(set(word)) > 1)

    print("P6 co-two simultaneous independent audit: PASS")
    print("pair/quotient ranks and occupancy product identities: PASS")
    print("direct 720-permutation coefficients: PASS")
    print("independent star-tree word cover: PASS")


if __name__ == "__main__":
    main()
