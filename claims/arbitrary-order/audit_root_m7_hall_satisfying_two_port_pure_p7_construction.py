"""Independent no-import audit of the Hall-satisfying pure-P7 construction."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import product


def rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix if any(row)]
    pivot_row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                left - scale * right
                for left, right in zip(work[index], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def permanent(matrix: list[list[int]]) -> int:
    @cache
    def recurse(row: int, used: int) -> int:
        if row == len(matrix):
            return 1
        total = 0
        for column, value in enumerate(matrix[row]):
            bit = 1 << column
            if value and not used & bit:
                total += value * recurse(row + 1, used | bit)
        return total

    return recurse(0, 0)


def build_data():
    a = [[0, 0, 0] for _ in range(7)]
    b = [[0, 0, 0] for _ in range(7)]
    a[0][0] = a[3][2] = a[5][1] = a[6][1] = 1
    b[0][0] = b[1][0] = b[5][2] = 1
    b[6][1] = -1

    h = [[[0, 0, 0] for _ in range(5)] for _ in range(7)]
    entries = {
        0: ((2, 1),),
        1: ((1, 1), (2, 0)),
        2: ((0, 0), (1, 2), (2, 4)),
        3: ((0, 1), (1, 3)),
        4: ((0, 2), (1, 4), (2, 3)),
        5: ((0, 3),),
        6: ((0, 4), (2, 2)),
    }
    # Pairs are (target colour, root basis row).  The single negative entry
    # H_0[:,1]=-f_0 is encoded separately.
    for blocker, pairs in entries.items():
        for colour, root in pairs:
            h[blocker][root][colour] = 1
    h[0][0][1] = -1
    return a, b, h


def coefficient(word, a, b, h) -> int:
    matrix = [[h[u][root][word[u]] for u in range(7)] for root in range(5)]
    matrix.append([a[u][word[u]] for u in range(7)])
    matrix.append([b[u][word[u]] for u in range(7)])
    return permanent(matrix)


def principal_path_counts() -> dict[int, Counter[tuple[int, ...]]]:
    edges = {(index, index + 1): 1 if index % 2 == 0 else 0 for index in range(6)}
    answer = {}
    for deleted in range(7):
        vertices = tuple(vertex for vertex in range(7) if vertex != deleted)

        @cache
        def recurse(remaining: tuple[int, ...]):
            if not remaining:
                return ((),)
            first = remaining[0]
            rows = []
            for position in range(1, len(remaining)):
                edge = (first, remaining[position])
                if edge not in edges:
                    continue
                rest = remaining[1:position] + remaining[position + 1 :]
                for tail in recurse(rest):
                    rows.append((edge,) + tail)
            return tuple(rows)

        positions = {vertex: index for index, vertex in enumerate(vertices)}
        signatures: Counter[tuple[int, ...]] = Counter()
        for matching in recurse(vertices):
            word = [-1] * 6
            for edge in matching:
                colour = edges[edge]
                word[positions[edge[0]]] = word[positions[edge[1]]] = colour
            signatures[tuple(word)] += 1
        answer[deleted] = signatures
    return answer


def main() -> None:
    a, b, h = build_data()
    if rank(a) != 3 or rank(b) != 3:
        raise AssertionError("port rank")
    for root in range(5):
        if rank([h[u][root] for u in range(7)]) != 3:
            raise AssertionError(("root", root))
    for u in range(7):
        local = [h[u][root] for root in range(5)] + [a[u], b[u]]
        if rank(local) != 3:
            raise AssertionError(("local", u))

    principals = principal_path_counts()
    if [len(principals[index]) for index in range(7)] != [1, 0, 1, 0, 1, 0, 1]:
        raise AssertionError(principals)

    coefficients = {
        word: coefficient(word, a, b, h) for word in product(range(3), repeat=7)
    }
    histogram = Counter(coefficients.values())
    if histogram != Counter({0: 2151, 1: 24, -1: 12}):
        raise AssertionError(histogram)
    pure = [coefficients[(colour,) * 7] for colour in range(3)]
    if pure != [1, 1, 1]:
        raise AssertionError(pure)
    mixed = [(word, value) for word, value in coefficients.items() if value and len(set(word)) > 1]
    if mixed[0] != ((0, 0, 0, 0, 1, 0, 2), 1) or len(mixed) != 33:
        raise AssertionError(mixed[:2])

    print("PASS: independent Hall-satisfying binary-cofactor/pure-P7 audit")
    print("port ranks: 3,3")
    print("root-row spans: 3,3,3,3,3")
    print("local map ranks: 3,3,3,3,3,3,3")
    print("pure P7 coefficients: 1,1,1")
    print("nonzero mixed coefficients: 33")
    print("first mixed failure: 0000102 -> 1")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
