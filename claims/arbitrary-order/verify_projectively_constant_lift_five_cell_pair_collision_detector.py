"""Verify the five-cell pair-collision and all-companion detector."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

PAIRS = tuple(combinations(range(4), 2))


def permanent(matrix: list[list[int]]) -> int:
    size = len(matrix)
    return sum(
        sp.prod(matrix[row][assignment[row]] for row in range(size))
        for assignment in permutations(range(size))
    )


def tensor_value(rows: tuple[tuple[tuple[int, int, int], ...], ...], word: tuple[int, ...]) -> int:
    return permanent(
        [
            [row[mode][word[mode]] for mode in range(len(word))]
            for row in rows
        ]
    )


def collision_matrix_four() -> sp.Matrix:
    words = tuple(product(range(3), repeat=4))
    columns = []
    for active in range(4):
        for component in range(3):
            column = []
            for word in words:
                value = 0
                for b_mode in range(4):
                    if b_mode == active:
                        continue
                    term = 2 * int(word[active] == component)
                    term *= int(word[b_mode] == 1)
                    term *= sp.prod(
                        int(word[mode] == 0)
                        for mode in range(4)
                        if mode not in (active, b_mode)
                    )
                    value += term
                column.append(value)
            columns.append(sp.Matrix(column))
    return sp.Matrix.hstack(*columns)


def pair_collision_matrix(h: tuple[tuple[int, int, int], ...]) -> sp.Matrix:
    """Return g -> P5(h,g,a,a,b) for normalized a=e0, b=e1."""
    words = tuple(product(range(3), repeat=5))
    word_index = {word: index for index, word in enumerate(words)}
    matrix = sp.zeros(243, 15)
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
                        matrix[word_index[tuple(word)], column] += 2 * h_value
    return matrix


def check_common_kernel_contractions() -> None:
    e0, e1 = (1, 0, 0), (0, 1, 0)
    h = tuple(
        tuple(5 * mode + 2 * component + 1 for component in range(3))
        for mode in range(5)
    )
    g = tuple(
        tuple(7 * mode + 3 * component + 2 for component in range(3))
        for mode in range(5)
    )
    for active in range(5):
        a = [tuple(11 * mode + component + 3 for component in range(3)) for mode in range(5)]
        b = [tuple(13 * mode + 2 * component + 5 for component in range(3)) for mode in range(5)]
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
            g_collision = tensor_value((g_other, a_other, a_other, b_other), other_word)
            h_collision = tensor_value((h_other, a_other, a_other, b_other), other_word)
            expected = h[active][2] * g_collision + g[active][2] * h_collision
            assert full == expected


def check_injectivity_charts() -> None:
    chart_vectors = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1))
    checked = 0
    for first, second in combinations(range(5), 2):
        for third in set(range(5)) - {first, second}:
            for vector in chart_vectors:
                h = [(0, 0, 0)] * 5
                h[first] = (2, 3, 1)
                h[second] = (5, 7, -1)
                h[third] = vector
                assert pair_collision_matrix(tuple(h)).rank() == 15
                checked += 1
    assert checked == 120


def companion_matrix(ells: tuple[tuple[int, int], ...]) -> sp.Matrix:
    matrix = sp.zeros(8, 6)
    roots = set(range(4))
    for opened in range(4):
        for companion in range(4):
            if companion == opened:
                continue
            complement = tuple(sorted(roots - {opened, companion}))
            column = PAIRS.index(complement)
            matrix[2 * opened, column] += ells[companion][0]
            matrix[2 * opened + 1, column] += ells[companion][1]
    return matrix


def check_companion_zero_edge() -> tuple[int, int]:
    vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1))
    checked = 0
    singular = 0
    for ells in product(vectors, repeat=4):
        if sp.Matrix(ells).rank() != 2:
            continue
        checked += 1
        kernel = companion_matrix(ells).nullspace()
        assert len(kernel) <= 1
        if kernel:
            singular += 1
            assert any(entry == 0 for entry in kernel[0])
    assert checked == 1220
    assert singular > 0
    return checked, singular


def pair_tensor(
    h: tuple[tuple[int, int, int], ...],
    g: tuple[tuple[int, int, int], ...],
) -> tuple[int, ...]:
    a = ((1, 0, 0),) * 5
    b = ((0, 1, 0),) * 5
    return tuple(
        tensor_value((h, g, a, a, b), word)
        for word in product(range(3), repeat=5)
    )


def check_sharpness_kernel() -> None:
    a, b = (1, 0, 0), (0, 1, 0)
    h = (b, b, b, (1, -1, 0), (1, -1, 0))
    g = ((0, 0, 0), (0, 0, 0), (0, 0, 0), (-1, 0, 0), a)
    assert any(component for covector in g for component in covector)
    assert pair_tensor(h, g) == (0,) * 243


def check_end_to_end_exceptional_frames() -> None:
    roots = (
        ((0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 1, 0), (1, 1, 0)),
        ((1, 0, 0), (0, 0, 1), (1, 1, 1), (0, 1, 0), (1, -1, 0)),
        ((1, 1, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1), (0, 1, 0)),
        ((0, 1, 0), (1, -1, 0), (1, 0, 0), (0, 0, 1), (1, 1, 1)),
    )
    pair_tensors = {pair: pair_tensor(roots[pair[0]], roots[pair[1]]) for pair in PAIRS}
    assert all(any(value != 0 for value in tensor) for tensor in pair_tensors.values())

    frames = (
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((1, 0), (2, 0), (0, 1), (0, -3)),
    )
    root_set = set(range(4))
    for ells in frames:
        detected = False
        for opened in range(4):
            for coordinate in range(2):
                coefficient = [0] * 243
                for companion in root_set - {opened}:
                    complement = tuple(sorted(root_set - {opened, companion}))
                    scalar = ells[companion][coordinate]
                    coefficient = [
                        left + scalar * right
                        for left, right in zip(
                            coefficient,
                            pair_tensors[complement],
                            strict=True,
                        )
                    ]
                detected |= any(value != 0 for value in coefficient)
        assert detected


def main() -> None:
    collision = collision_matrix_four()
    assert collision.shape == (81, 12)
    assert collision.rank() == 12
    check_common_kernel_contractions()
    check_injectivity_charts()
    checked, singular = check_companion_zero_edge()
    check_sharpness_kernel()
    check_end_to_end_exceptional_frames()
    print("PASS: exact four-mode collision rank 12")
    print("PASS: all 5 x 81 common-kernel contraction slices")
    print("PASS: 120 double-transverse five-mode injectivity charts")
    print(f"PASS: {checked} rank-two companion frames; {singular} singular zero-edge frames")
    print("PASS: exact weak-root pair-collision kernel preserves the scope wall")
    print("PASS: end-to-end zero-companion and balanced-2+2 detector models")
    print("SCOPE: at most one non-doubly-transverse root; no witness exclusion")
    print("SCOPE: full q=0 r=5 and global Krenn-Gu remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
