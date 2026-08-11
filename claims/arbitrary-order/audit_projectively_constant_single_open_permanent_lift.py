"""Independent no-import audit of the single-open permanent lift."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import permutations
from math import factorial


def permanent(matrix: list[list[int]]) -> int:
    """Use a permutation ledger independent of the primary checker."""
    size = len(matrix)
    total = 0
    for assignment in permutations(range(size)):
        term = 1
        for row, column in enumerate(assignment):
            term *= matrix[row][column]
        total += term
    return total


def matching_total(
    vertices: tuple[int, ...], edge: dict[tuple[int, int], int]
) -> int:
    """Use a first-vertex perfect-matching recursion."""

    @cache
    def recurse(remaining: tuple[int, ...]) -> int:
        if not remaining:
            return 1
        first = remaining[0]
        total = 0
        for offset in range(1, len(remaining)):
            second = remaining[offset]
            rest = remaining[1:offset] + remaining[offset + 1 :]
            total += edge[tuple(sorted((first, second)))] * recurse(rest)
        return total

    return recurse(vertices)


def signed(seed: int, first: int, second: int, shift: int) -> int:
    magnitude = seed + 2 * first + 3 * second + shift
    return -magnitude if (seed + first + second + shift) % 2 else magnitude


def numeric_case(r: int, q: int, seed: int) -> None:
    """Compare two separately constructed exact integer ledgers."""
    m = r + 2 * q
    roots = tuple(range(r))
    pinned = roots[1:]
    outside = tuple(range(r, r + m))
    vertices = roots + outside

    eta = signed(seed, 0, 0, 1)
    ell = {root: signed(seed, root, 0, 2) for root in pinned}
    a = {mode: signed(seed, mode - r, 0, 3) for mode in outside}
    b = {mode: signed(seed, mode - r, 1, 4) for mode in outside}
    h = {
        (root, mode): signed(seed, root, mode - r, 5)
        for root in pinned
        for mode in outside
    }

    edge: dict[tuple[int, int], int] = {}
    for first in vertices:
        for second in vertices:
            if first >= second:
                continue
            pair = (first, second)
            if first == 0 and second in pinned:
                edge[pair] = ell[second]
            elif first == 0 and second in outside:
                edge[pair] = eta * b[second]
            elif first in pinned and second in pinned:
                edge[pair] = 0
            elif first in pinned and second in outside:
                edge[pair] = h[(first, second)]
            else:
                edge[pair] = a[first] * b[second] + b[first] * a[second]

    graph = matching_total(vertices, edge)
    lifted_rows: list[list[int]] = []
    for root in pinned:
        lifted_rows.append([ell[root], *(h[(root, mode)] for mode in outside)])
    for _ in range(q + 1):
        lifted_rows.append([eta, *(a[mode] for mode in outside)])
    for _ in range(q + 1):
        lifted_rows.append([0, *(b[mode] for mode in outside)])
    assert len(lifted_rows) == m + 1
    assert permanent(lifted_rows) == factorial(q + 1) * graph

    fixed_rows: list[list[int]] = []
    fixed_rows.extend(
        [[h[(root, mode)] for mode in outside] for root in pinned]
    )
    fixed_rows.extend([[a[mode] for mode in outside] for _ in range(q)])
    fixed_rows.extend([[b[mode] for mode in outside] for _ in range(q + 1)])
    fixed = permanent(fixed_rows)

    sectors = {partner: 0 for partner in vertices[1:]}
    for partner in vertices[1:]:
        rest = tuple(vertex for vertex in vertices if vertex not in (0, partner))
        sectors[partner] = edge[(0, partner)] * matching_total(rest, edge)

    outside_value = sum(sectors[partner] for partner in outside)
    assert factorial(q) * outside_value == eta * fixed

    for root in pinned:
        rows: list[list[int]] = []
        rows.extend(
            [
                [h[(other, mode)] for mode in outside]
                for other in pinned
                if other != root
            ]
        )
        rows.extend([[a[mode] for mode in outside] for _ in range(q + 1)])
        rows.extend([[b[mode] for mode in outside] for _ in range(q + 1)])
        assert factorial(q + 1) * sectors[root] == ell[root] * permanent(rows)

    contracted_rows: list[list[int]] = []
    contracted_rows.extend(
        [[0, *(h[(root, mode)] for mode in outside)] for root in pinned]
    )
    contracted_rows.extend(
        [[1, *(a[mode] for mode in outside)] for _ in range(q + 1)]
    )
    contracted_rows.extend(
        [[0, *(b[mode] for mode in outside)] for _ in range(q + 1)]
    )
    assert permanent(contracted_rows) == (q + 1) * fixed


def rank(matrix: list[list[int | Fraction]]) -> int:
    """Exact rational row rank by a standalone Gauss-Jordan routine."""
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
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def matmul(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    return [
        [
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(len(right))
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def add(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [a + b for a, b in zip(left_row, right_row, strict=True)]
        for left_row, right_row in zip(left, right, strict=True)
    ]


def audit_frame() -> None:
    """Rebuild the companion quotient frame without computer algebra."""
    root = [[1], [2], [3]]
    eta = [[1, 0, 0]]
    companions = [[-2, 1, 0], [-3, 0, 1]]
    diagonal = [[2, 0, 0], [0, 3, 0], [0, 0, 5]]
    fixed = matmul(diagonal, root)
    cofactor_columns = [[0, 0], [3, 0], [0, 5]]

    assert matmul(eta, root) == [[1]]
    assert matmul(companions, root) == [[0], [0]]
    assert rank(companions) == 2
    fixed_eta = matmul(fixed, eta)
    cofactor_companions = matmul(cofactor_columns, companions)
    assert add(fixed_eta, cofactor_companions) == diagonal

    kernel_eta = [[0, 0], [1, 0], [0, 1]]
    effective = matmul(companions, kernel_eta)
    assert effective == [[1, 0], [0, 1]]
    assert rank(cofactor_columns) == 2
    assert rank(
        [
            [cofactor_columns[row][0], cofactor_columns[row][1], fixed[row][0]]
            for row in range(3)
        ]
    ) == 3


def audit_support() -> None:
    for r in range(2, 15):
        for q in range(8):
            m = r + 2 * q
            order = m + 1
            row_types = ["h"] * (r - 1)
            row_types += ["a"] * (q + 1)
            row_types += ["b"] * (q + 1)
            assert len(row_types) == order
            assert (3 * (q + 1) <= m) == (r >= q + 3)
            assert factorial(q + 1) == (q + 1) * factorial(q)


def main() -> None:
    cases = ((2, 0), (3, 0), (2, 1), (3, 1), (2, 2), (4, 1))
    for r, q in cases:
        for seed in (1, 4, 7):
            numeric_case(r, q, seed)
        print(f"AUDIT PASS: independent integer lift ledger r={r} q={q}")

    audit_frame()
    audit_support()
    print("AUDIT PASS: outside, companion, and contraction sectors agree exactly")
    print("AUDIT PASS: rational companion plane and diagonal quotient rank two")
    print("AUDIT PASS: factorial, row-count, and Hall arithmetic")
    print("AUDIT SCOPE: cross-depth detector transport and P_M exclusion unproved")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
