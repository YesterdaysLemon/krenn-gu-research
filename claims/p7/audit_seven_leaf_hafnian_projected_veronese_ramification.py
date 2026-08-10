"""Independent no-import audit of projected-Veronese ramification."""

from fractions import Fraction
from itertools import combinations, combinations_with_replacement

VERTICES = tuple(range(7))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FOUR_SETS = tuple(combinations(VERTICES, 4))
FIVE_SETS = tuple(combinations(VERTICES, 5))
SYMMETRIC_PAIRS = tuple(combinations_with_replacement(range(len(EDGES)), 2))


def rational_rank(matrix):
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
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(row_count):
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
        if pivot_row == row_count:
            break
    return pivot_row


def multiplication_projection():
    rows = []
    for four_set in FOUR_SETS:
        support = set(four_set)
        row = []
        for left_index, right_index in SYMMETRIC_PAIRS:
            left = set(EDGES[left_index])
            right = set(EDGES[right_index])
            row.append(
                int(
                    left_index != right_index
                    and not left.intersection(right)
                    and left.union(right) == support
                )
            )
        rows.append(row)
    return rows


def all_one_jacobian():
    return [
        [int(set(edge).issubset(four_set)) for edge in EDGES]
        for four_set in FOUR_SETS
    ]


def lefschetz_matrix():
    return [
        [int(set(four_set).issubset(five_set)) for four_set in FOUR_SETS]
        for five_set in FIVE_SETS
    ]


def audit_bilinear_coefficients():
    # Both constructions must give coefficient one for each ordered pair
    # (f_e, k_g) of disjoint edges whose union is the output four-set.
    for four_set in FOUR_SETS:
        support = set(four_set)
        projected = set()
        for left_index, right_index in SYMMETRIC_PAIRS:
            left = set(EDGES[left_index])
            right = set(EDGES[right_index])
            if (
                left_index != right_index
                and not left.intersection(right)
                and left.union(right) == support
            ):
                projected.add((left_index, right_index))
                projected.add((right_index, left_index))

        differentiated = set()
        for direction_index, edge in enumerate(EDGES):
            if not set(edge).issubset(support):
                continue
            complement = tuple(sorted(support.difference(edge)))
            differentiated.add((EDGE_INDEX[complement], direction_index))
        assert projected == differentiated
        assert len(projected) == 6


def main():
    projection = multiplication_projection()
    assert len(projection) == 35 and len(projection[0]) == 231
    assert rational_rank(projection) == 35
    print("AUDIT PASS: multiplication projection has rank 35 and kernel 196")

    audit_bilinear_coefficients()
    print("AUDIT PASS: tangent projection equals the hafnian differential formally")

    assert rational_rank(all_one_jacobian()) == 21
    print("AUDIT PASS: all-one four-hafnian Jacobian has rank 21")

    assert rational_rank(lefschetz_matrix()) == 21
    print("AUDIT PASS: primitive four-form target has dimension 14")

    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 graph_enumerations=0 numerics=0")
    print("SCOPE: physical primitive ramification torus remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
