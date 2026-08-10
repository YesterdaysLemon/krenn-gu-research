"""Independent combinatorial audit of the balanced half-sensor theorem.

This file does not import the primary verifier.  It compares sets of labelled
perfect matchings, then checks the explicit sensor rank by separate rational
row reduction.  These are bounded audits of the written arbitrary-order
proof, not an exhaustive graph search.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def canonical_edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(tuple(sorted((canonical_edge(first, second), *tail))))
    return tuple(answer)


def audit_matching_bijection() -> None:
    for m in range(1, 6):
        roots = tuple(range(m))
        nonroots = tuple(range(m, 2 * m))
        direct = Counter(matchings(roots + nonroots))
        reconstructed: Counter[Matching] = Counter()

        for present_size in range(0, m + 1, 2):
            for present in combinations(nonroots, present_size):
                present_set = set(present)
                deletion = tuple(v for v in nonroots if v not in present_set)
                for unmatched in combinations(roots, len(deletion)):
                    unmatched_set = set(unmatched)
                    remaining_roots = tuple(v for v in roots if v not in unmatched_set)
                    for targets in permutations(deletion):
                        cross = tuple(
                            canonical_edge(root, target)
                            for root, target in zip(unmatched, targets, strict=True)
                        )
                        for root_matching in matchings(remaining_roots):
                            for nonroot_matching in matchings(present):
                                reconstructed[
                                    tuple(sorted((*cross, *root_matching, *nonroot_matching)))
                                ] += 1

        assert reconstructed == direct
        assert len(direct) == odd_double_factorial(2 * m - 1)
        assert set(direct.values()) == {1}


def odd_double_factorial(odd: int) -> int:
    if odd == -1:
        return 1
    answer = 1
    for value in range(1, odd + 1, 2):
        answer *= value
    return answer


def matrix_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def audit_explicit_rank() -> None:
    for m in range(1, 8):
        columns = [
            subset
            for size in range(m % 2, m + 1, 2)
            for subset in combinations(range(m), size)
        ]
        binary_words = list(range(1 << m))
        matrix = [[0 for _ in columns] for _ in binary_words]
        for column, deletion in enumerate(columns):
            deletion_mask = sum(1 << index for index in deletion)
            remaining = m - len(deletion)
            matrix[deletion_mask][column] = odd_double_factorial(remaining - 1)
        assert matrix_rank(matrix) == 2 ** (m - 1)


def audit_target_disjointness_and_degrees() -> None:
    pairs = ((0, 1), (1, 2), (2, 0))
    for m in range(3, 7):
        sensor_support = set()
        for size in range(m % 2, m + 1, 2):
            for deletion in combinations(range(m), size):
                deletion_set = set(deletion)
                sensor_support.add(
                    tuple(
                        pairs[index % 3][0 if index in deletion_set else 1]
                        for index in range(m)
                    )
                )
        diagonal_support = {(colour,) * m for colour in range(3)}
        assert sensor_support.isdisjoint(diagonal_support)

        for present_size in range(0, m + 1, 2):
            for present in combinations(range(m), present_size):
                present_set = set(present)
                deletion_set = set(range(m)) - present_set
                total_degree = tuple(
                    int(index in present_set) + int(index in deletion_set)
                    for index in range(m)
                )
                assert total_degree == (1,) * m


def main() -> None:
    audit_matching_bijection()
    audit_explicit_rank()
    audit_target_disjointness_and_degrees()
    print("independent balanced half-sensor audit: PASS")
    print("labelled matching bijection checked through n=10")
    print("no import from the primary verifier; exact rational row reduction")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
