"""Independent stdlib audit of the two-source exceptional-row obstruction."""

from __future__ import annotations

from itertools import product


def rank_mod_two(rows: list[list[int]]) -> int:
    work = [[entry % 2 for entry in row] for row in rows]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (i for i in range(pivot_row, len(work)) if work[i][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        for i, row in enumerate(work):
            if i == pivot_row or not row[column]:
                continue
            work[i] = [
                (left + right) % 2
                for left, right in zip(row, work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def product_map(q: tuple[int, ...]) -> list[list[int]]:
    left = q[:6]
    right = q[6:]
    columns: list[list[int]] = []
    for basis in range(9):
        s = [0] * 6
        z = [0] * 3
        if basis < 6:
            s[basis] = 1
        else:
            z[basis - 6] = 1
        columns.append(
            [
                (s[i] * right[j] + left[i] * z[j]) % 2
                for i, j in product(range(6), range(3))
            ]
        )
    return [[columns[j][i] for j in range(9)] for i in range(18)]


def audit_nine_space_census() -> None:
    counts: dict[tuple[str, int], int] = {}
    for q in product(range(2), repeat=9):
        if not any(q):
            continue
        left_nonzero = any(q[:6])
        right_nonzero = any(q[6:])
        kind = "mixed" if left_nonzero and right_nonzero else "pure"
        nullity = 9 - rank_mod_two(product_map(q))
        key = (kind, nullity)
        counts[key] = counts.get(key, 0) + 1
    assert counts == {("pure", 6): 63, ("pure", 3): 7, ("mixed", 1): 441}
    print("independent F_2 (6+3)-space census: PASS (63 / 7 / 441)")


def rref_three_planes() -> list[list[list[int]]]:
    planes: list[list[list[int]]] = []
    for p0 in range(4):
        for p1 in range(p0 + 1, 5):
            for p2 in range(p1 + 1, 6):
                pivots = (p0, p1, p2)
                free = [
                    (row, column)
                    for row, pivot in enumerate(pivots)
                    for column in range(pivot + 1, 6)
                    if column not in pivots
                ]
                for bits in product((0, 1), repeat=len(free)):
                    matrix = [[0] * 6 for _ in range(3)]
                    for row, pivot in enumerate(pivots):
                        matrix[row][pivot] = 1
                    for (row, column), bit in zip(free, bits, strict=True):
                        matrix[row][column] = bit
                    planes.append(matrix)
    return planes


def splitting_map(rows: list[list[int]]) -> list[list[int]]:
    output: list[list[int]] = []
    for row in rows:
        x, y = row[:3], row[3:]
        for i, j in product(range(3), repeat=2):
            equation = [0] * 6
            equation[j] = x[i]
            equation[3 + i] = y[j]
            output.append(equation)
    return output


def audit_every_binary_three_plane() -> None:
    planes = rref_three_planes()
    assert len(planes) == 1395
    ranks: dict[int, int] = {}
    for plane in planes:
        value = rank_mod_two(splitting_map(plane))
        ranks[value] = ranks.get(value, 0) + 1
    assert ranks == {3: 2, 6: 1393}
    print("independent F_2 three-plane splitting census: PASS (2 aligned; 1393 injective)")


def audit_purity_pigeonhole() -> None:
    for labels in product((0, 1), repeat=3):
        majority = 0 if labels.count(0) >= 2 else 1
        if labels.count(majority) == 3:
            assert len(set(labels)) == 1
        else:
            minority_index = next(i for i, label in enumerate(labels) if label != majority)
            forced_zero = {i for i in range(3) if i != minority_index}
            assert len(forced_zero) == 2
    print("independent pure-grid pigeonhole: PASS (8 assignments)")


def main() -> None:
    audit_nine_space_census()
    audit_every_binary_three_plane()
    audit_purity_pigeonhole()
    print("independent two-source exceptional-root-row audit: PASS")


if __name__ == "__main__":
    main()
