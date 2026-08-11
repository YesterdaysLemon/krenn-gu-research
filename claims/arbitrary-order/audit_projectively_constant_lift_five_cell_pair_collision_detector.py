"""Independent no-import audit of the five-cell pair-collision detector."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

PAIRS = tuple(combinations(range(4), 2))
Covector = tuple[int, int, int]


def rational_rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows if any(row)]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(pivot_row + 1, len(matrix)):
            if not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def permanent_recursive(matrix: tuple[tuple[int, ...], ...]) -> int:
    if not matrix:
        return 1
    total = 0
    for column, value in enumerate(matrix[0]):
        if not value:
            continue
        minor = tuple(row[:column] + row[column + 1 :] for row in matrix[1:])
        total += value * permanent_recursive(minor)
    return total


def tensor_value(rows: tuple[tuple[Covector, ...], ...], word: tuple[int, ...]) -> int:
    matrix = tuple(
        tuple(row[mode][word[mode]] for mode in range(len(word))) for row in rows
    )
    return permanent_recursive(matrix)


def pair_rows(h: tuple[Covector, ...]) -> list[list[int]]:
    words = tuple(product(range(3), repeat=5))
    word_index = {word: index for index, word in enumerate(words)}
    rows = [[0] * 15 for _ in range(243)]
    for g_mode in range(5):
        for g_component in range(3):
            column = 3 * g_mode + g_component
            for h_mode in range(5):
                if h_mode == g_mode:
                    continue
                for h_component, h_value in enumerate(h[h_mode]):
                    if not h_value:
                        continue
                    for b_mode in range(5):
                        if b_mode in (h_mode, g_mode):
                            continue
                        word = [0] * 5
                        word[h_mode] = h_component
                        word[g_mode] = g_component
                        word[b_mode] = 1
                        rows[word_index[tuple(word)]][column] += 2 * h_value
    return rows


def collision_rows_four() -> list[list[int]]:
    words = tuple(product(range(3), repeat=4))
    rows = [[0] * 12 for _ in range(81)]
    for active in range(4):
        for component in range(3):
            column = 3 * active + component
            for word_index, word in enumerate(words):
                for b_mode in range(4):
                    if b_mode == active:
                        continue
                    value = 2 * int(word[active] == component)
                    value *= int(word[b_mode] == 1)
                    value *= all(
                        word[mode] == 0
                        for mode in range(4)
                        if mode not in (active, b_mode)
                    )
                    rows[word_index][column] += value
    return rows


def audit_contractions() -> None:
    e0, e1 = (1, 0, 0), (0, 1, 0)
    h: tuple[Covector, ...] = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
        (41, 43, 47),
    )
    g: tuple[Covector, ...] = (
        (53, 59, 61),
        (67, 71, 73),
        (79, 83, 89),
        (97, 101, 103),
        (107, 109, 113),
    )
    a_base: tuple[Covector, ...] = (
        (127, 131, 137),
        (139, 149, 151),
        (157, 163, 167),
        (173, 179, 181),
        (191, 193, 197),
    )
    b_base: tuple[Covector, ...] = (
        (199, 211, 223),
        (227, 229, 233),
        (239, 241, 251),
        (257, 263, 269),
        (271, 277, 281),
    )
    for active in range(5):
        a = list(a_base)
        b = list(b_base)
        a[active] = e0
        b[active] = e1
        others = tuple(mode for mode in range(5) if mode != active)
        h_other = tuple(h[mode] for mode in others)
        g_other = tuple(g[mode] for mode in others)
        a_other = tuple(a[mode] for mode in others)
        b_other = tuple(b[mode] for mode in others)
        for other_word in product(range(3), repeat=4):
            word = [0] * 5
            word[active] = 2
            for mode, colour in zip(others, other_word, strict=True):
                word[mode] = colour
            full = tensor_value((h, g, tuple(a), tuple(a), tuple(b)), tuple(word))
            expected = h[active][2] * tensor_value(
                (g_other, a_other, a_other, b_other), other_word
            )
            expected += g[active][2] * tensor_value(
                (h_other, a_other, a_other, b_other), other_word
            )
            assert full == expected


def companion_rows(ells: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[0] * 6 for _ in range(8)]
    roots = set(range(4))
    for opened in range(4):
        for companion in range(4):
            if companion == opened:
                continue
            complement = tuple(sorted(roots - {opened, companion}))
            column = PAIRS.index(complement)
            rows[2 * opened][column] += ells[companion][0]
            rows[2 * opened + 1][column] += ells[companion][1]
    return rows


def proportional(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] * right[1] == left[1] * right[0]


def rank_two(ells: tuple[tuple[int, int], ...]) -> bool:
    return any(not proportional(ells[p], ells[q]) for p, q in PAIRS)


def audit_companion_zero_edges() -> tuple[int, int]:
    vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (-1, 2))
    checked = 0
    singular = 0
    for ells in product(vectors, repeat=4):
        if not rank_two(ells):
            continue
        checked += 1
        rows = companion_rows(ells)
        rank = rational_rank(rows)
        assert rank in (5, 6)
        if rank == 5:
            singular += 1
            assert any(
                rational_rank([row[:column] + row[column + 1 :] for row in rows]) < 5
                for column in range(6)
            )
    assert checked == 2310
    assert singular > 0
    return checked, singular


def audit_injectivity_charts() -> int:
    vectors: tuple[Covector, ...] = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 2, 3),
        (2, -1, 1),
    )
    checked = 0
    for first, second in combinations(range(5), 2):
        for third in set(range(5)) - {first, second}:
            for vector in vectors:
                h: list[Covector] = [(0, 0, 0)] * 5
                h[first] = (3, 5, 1)
                h[second] = (7, 11, -2)
                h[third] = vector
                assert rational_rank(pair_rows(tuple(h))) == 15
                checked += 1
    assert checked == 150
    return checked


def audit_sharpness_kernel() -> None:
    a: Covector = (1, 0, 0)
    b: Covector = (0, 1, 0)
    h: tuple[Covector, ...] = (b, b, b, (1, -1, 0), (1, -1, 0))
    g: tuple[Covector, ...] = (
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (-1, 0, 0),
        a,
    )
    fixed_a = (a,) * 5
    fixed_b = (b,) * 5
    assert all(
        tensor_value((h, g, fixed_a, fixed_a, fixed_b), word) == 0
        for word in product(range(3), repeat=5)
    )


def main() -> None:
    assert rational_rank(collision_rows_four()) == 12
    audit_contractions()
    charts = audit_injectivity_charts()
    frames, singular = audit_companion_zero_edges()
    audit_sharpness_kernel()
    print("AUDIT PASS: independent rational four-mode collision rank 12")
    print("AUDIT PASS: recursive permanent on all 5 x 81 contraction slices")
    print(f"AUDIT PASS: {charts} separately assembled pair-injectivity charts")
    print(f"AUDIT PASS: {frames} companion frames; {singular} singular zero-edge frames")
    print("AUDIT PASS: recursive replay of the weak-root collision kernel")
    print("AUDIT SCOPE: written contraction and bipartite-support proofs are arbitrary-field")
    print("AUDIT SCOPE: at least two weak roots and full q=0 r=5 remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
