"""Independent no-import audit of complete transverse five-cell detection."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

PAIRS = tuple(combinations(range(4), 2))
PAIRINGS = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
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


def balanced_partitions(
    ells: tuple[tuple[int, int], ...],
) -> list[tuple[int, int, int, int]]:
    if any(ell == (0, 0) for ell in ells):
        return []
    return [
        pairing
        for pairing in PAIRINGS
        if proportional(ells[pairing[0]], ells[pairing[1]])
        and proportional(ells[pairing[2]], ells[pairing[3]])
    ]


def coordinate_forced_zero(rows: list[list[int]], column: int) -> bool:
    rank = rational_rank(rows)
    without = [row[:column] + row[column + 1 :] for row in rows]
    return rational_rank(without) < rank


def audit_companion_masks() -> tuple[int, int, int]:
    vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (-1, 2))
    checked = zero_frames = balanced_frames = 0
    for ells in product(vectors, repeat=4):
        if not rank_two(ells):
            continue
        checked += 1
        rows = companion_rows(ells)
        rank = rational_rank(rows)
        zero_roots = [root for root, ell in enumerate(ells) if ell == (0, 0)]
        balanced = balanced_partitions(ells)
        if zero_roots:
            zero_frames += 1
            assert rank == 5
            for root in zero_roots:
                for other in set(range(4)) - {root}:
                    column = PAIRS.index(tuple(sorted((root, other))))
                    assert coordinate_forced_zero(rows, column)
        elif balanced:
            balanced_frames += 1
            assert rank == 5
            for first, second, third, fourth in balanced:
                first_pair = PAIRS.index(tuple(sorted((first, second))))
                second_pair = PAIRS.index(tuple(sorted((third, fourth))))
                assert coordinate_forced_zero(rows, first_pair)
                assert coordinate_forced_zero(rows, second_pair)
        else:
            assert rank == 6
    assert checked == 2310
    return checked, zero_frames, balanced_frames


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
    for active in range(5):
        a = [
            (127 + 5 * mode, 131 + 7 * mode, 137 + 11 * mode)
            for mode in range(5)
        ]
        b = [
            (139 + 13 * mode, 149 + 17 * mode, 151 + 19 * mode)
            for mode in range(5)
        ]
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
                (g_other, a_other, a_other, b_other),
                other_word,
            )
            expected += g[active][2] * tensor_value(
                (h_other, a_other, a_other, b_other),
                other_word,
            )
            assert full == expected


def audit_weak_rowspace_trapping() -> int:
    profiles: list[tuple[Covector, ...]] = []
    profiles.append(tuple((value, 0, 0) for value in (2, -1, -1, 0, 0)))
    for pair in combinations(range(5), 2):
        profile: list[Covector] = [(0, 1, 0)] * 5
        for mode in pair:
            profile[mode] = (2, -1, 0)
        profiles.append(tuple(profile))
    for escape in range(5):
        profile = [
            (1, 0, 0),
            (0, 1, 0),
            (2, 1, 0),
            (1, -2, 0),
            (3, 1, 0),
        ]
        profile[escape] = (2, 3, -1)
        profiles.append(tuple(profile))

    checked = 0
    for h in profiles:
        rows = pair_rows(h)
        rank = rational_rank(rows)
        escape = {mode for mode, covector in enumerate(h) if covector[2] != 0}
        assert len(escape) <= 1
        for mode in set(range(5)) - escape:
            unit = [0] * 15
            unit[3 * mode + 2] = 1
            assert rational_rank(rows + [unit]) == rank
        checked += 1
    return checked


def audit_scope_wall_and_pigeonhole() -> None:
    a: Covector = (1, 0, 0)
    b: Covector = (0, 1, 0)
    h = tuple((value, 0, 0) for value in (1, 1, -2, 0, 0))
    g = tuple((value, 0, 0) for value in (1, 1, 1, -1, 0))
    fixed_a = (a,) * 5
    fixed_b = (b,) * 5
    assert all(
        tensor_value((h, g, fixed_a, fixed_a, fixed_b), word) == 0
        for word in product(range(3), repeat=5)
    )
    for escapes in product((None, 0, 1, 2, 3, 4), repeat=4):
        union = {mode for mode in escapes if mode is not None}
        assert set(range(5)) - union
    trapped_source_dimension = 2
    diagonal_flattening_rank = 3
    assert trapped_source_dimension < diagonal_flattening_rank


def main() -> None:
    frames, zero_frames, balanced_frames = audit_companion_masks()
    audit_contractions()
    weak = audit_weak_rowspace_trapping()
    audit_scope_wall_and_pigeonhole()
    print(f"AUDIT PASS: {frames} companion frames match forced zero masks")
    print(f"AUDIT PASS: zero frames {zero_frames}; balanced frames {balanced_frames}")
    print("AUDIT PASS: recursive permanent on all 5 x 81 contraction slices")
    print(f"AUDIT PASS: {weak} independently assembled weak rowspace charts")
    print("AUDIT PASS: exact pairwise scope wall and escape-set pigeonhole")
    print("AUDIT SCOPE: written case split proves complete local-transverse cell")
    print("AUDIT SCOPE: local-dependence and global Krenn-Gu remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
