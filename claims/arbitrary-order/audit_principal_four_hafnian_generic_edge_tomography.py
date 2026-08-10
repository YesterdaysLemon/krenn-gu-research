"""Independent stdlib audit of principal four-hafnian edge tomography."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                work[row][entry] - factor * work[pivot_row][entry]
                for entry in range(cols)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def inclusion_matrix(n: int) -> list[list[int]]:
    edge_list = list(combinations(range(n), 2))
    return [
        [int(edge[0] in four and edge[1] in four) for edge in edge_list]
        for four in combinations(range(n), 4)
    ]


def audit_kernel_difference_argument(n: int) -> None:
    edge_list = list(combinations(range(n), 2))
    # A deliberately nonconstant exact vector must be detected by some four-set.
    values = {edge: Fraction((edge[0] + 1) * (edge[1] + 2) - 3) for edge in edge_list}
    four_sums = [
        sum(values[edge] for edge in combinations(four, 2))
        for four in combinations(range(n), 4)
    ]
    assert any(value != 0 for value in four_sums)

    # Directly audit the subtraction identity used in the proof.
    a, b = 0, 1
    for triple in combinations(range(2, n), 3):
        left = sum(values[tuple(sorted((a, t)))] for t in triple)
        left += sum(values[edge] for edge in combinations(triple, 2))
        right = sum(values[tuple(sorted((b, t)))] for t in triple)
        right += sum(values[edge] for edge in combinations(triple, 2))
        difference = sum(
            values[tuple(sorted((a, t)))] - values[tuple(sorted((b, t)))]
            for t in triple
        )
        assert left - right == difference


def four_hafnian(weights: dict[tuple[int, int], Fraction], four: tuple[int, ...]) -> Fraction:
    i, j, k, ell = four
    edge = lambda u, v: weights.get(tuple(sorted((u, v))), Fraction(0))
    return edge(i, j) * edge(k, ell) + edge(i, k) * edge(j, ell) + edge(i, ell) * edge(j, k)


def audit_symmetries_and_singular_line() -> None:
    base = {
        edge: Fraction((edge[0] + 2) * (edge[1] + 3))
        for edge in combinations(range(6), 2)
    }
    negated = {edge: -value for edge, value in base.items()}
    for four in combinations(range(6), 4):
        assert four_hafnian(base, four) == four_hafnian(negated, four)

    for parameter in (Fraction(-7), Fraction(0), Fraction(11, 3)):
        one_edge = {(0, 1): parameter}
        assert all(
            four_hafnian(one_edge, four) == 0 for four in combinations(range(6), 4)
        )


def main() -> None:
    assert rational_rank(inclusion_matrix(6)) == 15
    print("AUDIT PASS: independent W_(2,4)(6) rational rank 15")
    assert rational_rank(inclusion_matrix(9)) == 36
    print("AUDIT PASS: independent P7 nine-nonroot rational rank 36")
    audit_kernel_difference_argument(6)
    audit_kernel_difference_argument(9)
    print("AUDIT PASS: exact four-set subtraction identity")
    audit_symmetries_and_singular_line()
    print("AUDIT PASS: sign involution and positive-dimensional singular fibre")
    assert 2**5 < 126 <= 3**5
    print("AUDIT PASS: exact P7 shallow-deck label capacity boundary")
    print("AUDIT SCOPE: generic finiteness is not global uniqueness")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
