"""Independent no-import audit for the P7 selector-matroid boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def permanent_dp(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    states = {0: Fraction(1)}
    for row in matrix:
        nxt: dict[int, Fraction] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    new_mask = mask | (1 << column)
                    nxt[new_mask] = nxt.get(new_mask, Fraction(0)) + value * entry
        states = nxt
    return states[(1 << size) - 1]


def submatrix(
    matrix: list[list[Fraction]], rows: tuple[int, ...], cols: tuple[int, ...]
) -> list[list[Fraction]]:
    return [[matrix[row][column] for column in cols] for row in rows]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    work[row][j] - scale * work[pivot_row][j] for j in range(cols)
                ]
        pivot_row += 1
    return pivot_row


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((row[i] * vector[i] for i in range(len(vector))), Fraction(0)) for row in matrix]


def audit_selector_kernel() -> None:
    incidence = [
        [1, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1],
    ]
    matrix = [[Fraction(entry) for entry in row] for row in incidence]
    assert rank(matrix) == 4
    for s, t in ((1, 0), (0, 1), (3, -2)):
        vector = [Fraction(x) for x in (-s - t, s, t, t, s, -s - t)]
        assert mat_vec(matrix, vector) == [Fraction(0)] * 4

    for lam in (Fraction(1), Fraction(-2), Fraction(5, 3)):
        response = [Fraction(x) * lam for x in (0, 1, -1, -1, 1, 0)]
        assert mat_vec(matrix, response) == [Fraction(0)] * 4

    for port_count in (5, 6):
        pairs = list(combinations(range(port_count), 2))
        rows = []
        for window in combinations(range(port_count), 4):
            window_set = set(window)
            for vertex in window:
                rows.append(
                    [
                        Fraction(int(vertex in edge and set(edge).issubset(window_set)))
                        for edge in pairs
                    ]
                )
        assert rank(rows) == len(pairs)


def canonical_matrices() -> list[list[list[Fraction]]]:
    raw = [
        [
            [-1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [-1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0],
        ],
        [
            [0, 1, 0, 0, 0],
            [-1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [-1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
        ],
        [
            [-1, 1, 0, 0, 0],
            [-1, 0, 1, 0, 0],
            [-1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 0],
        ],
    ]
    return [[[Fraction(entry) for entry in row] for row in matrix] for matrix in raw]


def shore_products(
    matrix: list[list[Fraction]], pair: tuple[int, int]
) -> list[Fraction]:
    universe = tuple(range(5))
    other_rows = tuple(row for row in universe if row not in pair)
    products = []
    for shore in combinations(universe, 3):
        if 0 not in shore:
            continue
        other_cols = tuple(column for column in universe if column not in shore)
        products.append(
            permanent_dp(submatrix(matrix, other_rows, shore))
            * permanent_dp(submatrix(matrix, pair, other_cols))
        )
    return products


def audit_canonical_countermodel() -> None:
    for matrix in canonical_matrices():
        assert permanent_dp(matrix) == -1
        pure_p7 = [row + [Fraction(0), Fraction(0)] for row in matrix]
        pure_p7.extend(
            [
                [Fraction(0)] * 5 + [Fraction(1), Fraction(0)],
                [Fraction(0)] * 5 + [Fraction(0), Fraction(1)],
            ]
        )
        assert permanent_dp(pure_p7) == -1
        assert shore_products(matrix, (0, 1)) == [Fraction(0)] * 6
        assert shore_products(matrix, (2, 3)) == [Fraction(0)] * 6
        assert any(
            value
            for pair in combinations(range(5), 2)
            if pair not in {(0, 1), (2, 3)}
            for value in shore_products(matrix, pair)
        )


def solve_three_by_three(
    matrix: list[list[Fraction]], rhs: list[Fraction]
) -> list[Fraction]:
    augmented = [matrix[row][:] + [rhs[row]] for row in range(3)]
    for column in range(3):
        pivot = next(row for row in range(column, 3) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(3):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                augmented[row][j] - scale * augmented[column][j] for j in range(4)
            ]
    return [augmented[row][3] for row in range(3)]


def audit_dominance_samples() -> None:
    targets = [
        (Fraction(2), [1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]),
        (Fraction(-3), [2, -1, 5, 3, -4, 7], [1, 6, -2, 8, 9, -5]),
        (Fraction(5, 2), [3, 4, -2, 9, 1, -6], [5, -3, 7, 2, 8, 4]),
    ]
    pairs = list(combinations(range(3, 7), 2))
    for gamma, m_values, nu_values in targets:
        m = dict(zip(pairs, (Fraction(value) for value in m_values), strict=True))
        nu = dict(zip(pairs, (Fraction(value) for value in nu_values), strict=True))
        assert m[(3, 4)] * m[(3, 5)] * m[(3, 6)]
        u = {3: Fraction(1)}
        v = {3: Fraction(0), 4: m[(3, 4)], 5: m[(3, 5)], 6: m[(3, 6)]}
        system = [[v[5], v[4], 0], [v[6], 0, v[4]], [0, v[6], v[5]]]
        solution = solve_three_by_three(
            [[Fraction(entry) for entry in row] for row in system],
            [m[(4, 5)], m[(4, 6)], m[(5, 6)]],
        )
        u.update({4: solution[0], 5: solution[1], 6: solution[2]})
        for pair in pairs:
            direct_top = u[pair[0]] * v[pair[1]] + u[pair[1]] * v[pair[0]]
            assert direct_top == m[pair]
            tail = (nu[pair] - m[pair]) / gamma
            assert direct_top + gamma * tail == nu[pair]


def audit_balanced_count() -> None:
    cycle = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
    for marked_root in range(5):
        coefficient = sum(1 for pair in cycle if marked_root not in pair)
        assert coefficient == 3


def main() -> None:
    audit_selector_kernel()
    audit_canonical_countermodel()
    audit_dominance_samples()
    audit_balanced_count()
    print("PASS: independent selector-kernel and legal-response audit")
    print("PASS: independent canonical rank-cooccurrence countermodel audit")
    print("PASS: independent rational six-window dominance samples")
    print("PASS: independent balanced marked-matching coefficient count")
    print("SCOPE: mixed-colour P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
