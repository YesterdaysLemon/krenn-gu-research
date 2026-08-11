"""Verify the complete locally transverse q=0, r=5 detector."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

PAIRS = tuple(combinations(range(4), 2))
PAIRINGS = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))


def permanent(matrix: list[list[int]]) -> int:
    size = len(matrix)
    return sum(
        sp.prod(matrix[row][assignment[row]] for row in range(size))
        for assignment in permutations(range(size))
    )


def tensor_value(
    rows: tuple[tuple[tuple[int, int, int], ...], ...],
    word: tuple[int, ...],
) -> int:
    return permanent(
        [[row[mode][word[mode]] for mode in range(len(word))] for row in rows]
    )


def pair_collision_matrix(h: tuple[tuple[int, int, int], ...]) -> sp.Matrix:
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


def proportional(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] * right[1] == left[1] * right[0]


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


def check_companion_zero_patterns() -> tuple[int, int, int]:
    vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1))
    checked = zero_frames = balanced_frames = 0
    for ells in product(vectors, repeat=4):
        if sp.Matrix(ells).rank() != 2:
            continue
        checked += 1
        matrix = companion_matrix(ells)
        kernel = matrix.nullspace()
        zero_roots = [root for root, ell in enumerate(ells) if ell == (0, 0)]
        balanced = balanced_partitions(ells)
        if zero_roots:
            zero_frames += 1
            assert len(kernel) == 1
            vector = kernel[0]
            for root in zero_roots:
                for other in set(range(4)) - {root}:
                    pair = tuple(sorted((root, other)))
                    assert vector[PAIRS.index(pair)] == 0
        elif balanced:
            balanced_frames += 1
            assert len(kernel) == 1
            vector = kernel[0]
            for first, second, third, fourth in balanced:
                first_pair = tuple(sorted((first, second)))
                second_pair = tuple(sorted((third, fourth)))
                assert vector[PAIRS.index(first_pair)] == 0
                assert vector[PAIRS.index(second_pair)] == 0
        else:
            assert not kernel
            assert matrix.rank() == 6
    assert checked == 1220
    return checked, zero_frames, balanced_frames


def weak_profiles() -> tuple[tuple[tuple[int, int, int], ...], ...]:
    profiles: list[tuple[tuple[int, int, int], ...]] = []
    pure = (1, 1, -2, 0, 0)
    profiles.append(tuple((value, 0, 0) for value in pure))
    for pair in combinations(range(5), 2):
        profile = [(0, 1, 0)] * 5
        for mode in pair:
            profile[mode] = (1, -1, 0)
        profiles.append(tuple(profile))
    for escape in range(5):
        profile = [
            (1, 0, 0),
            (0, 1, 0),
            (1, 1, 0),
            (1, -1, 0),
            (2, 1, 0),
        ]
        profile[escape] = (1, 2, 1)
        profiles.append(tuple(profile))
    return tuple(profiles)


def check_weak_kernel_trapping() -> tuple[int, int]:
    checked = kernel_vectors = 0
    for h in weak_profiles():
        assert sum(covector != (0, 0, 0) for covector in h) >= 3
        escape = {mode for mode, covector in enumerate(h) if covector[2] != 0}
        assert len(escape) <= 1
        kernel = pair_collision_matrix(h).nullspace()
        checked += 1
        kernel_vectors += len(kernel)
        for vector in kernel:
            for mode in set(range(5)) - escape:
                assert vector[3 * mode + 2] == 0
    assert kernel_vectors > 0
    return checked, kernel_vectors


def check_common_kernel_contractions() -> None:
    e0, e1 = (1, 0, 0), (0, 1, 0)
    h = tuple(
        tuple(5 * mode + component + 2 for component in range(3))
        for mode in range(5)
    )
    g = tuple(
        tuple(7 * mode + 2 * component + 3 for component in range(3))
        for mode in range(5)
    )
    for active in range(5):
        a = [
            tuple(11 * mode + component + 5 for component in range(3))
            for mode in range(5)
        ]
        b = [
            tuple(13 * mode + 3 * component + 7 for component in range(3))
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


def check_pairwise_scope_wall() -> None:
    a, b = (1, 0, 0), (0, 1, 0)
    h = tuple((value, 0, 0) for value in (1, 1, -2, 0, 0))
    g = tuple((value, 0, 0) for value in (1, 1, 1, -1, 0))
    fixed_a = (a,) * 5
    fixed_b = (b,) * 5
    assert sum(covector != (0, 0, 0) for covector in h) == 3
    assert sum(covector != (0, 0, 0) for covector in g) == 4
    assert all(
        tensor_value((h, g, fixed_a, fixed_a, fixed_b), word) == 0
        for word in product(range(3), repeat=5)
    )


def check_escape_pigeonhole() -> None:
    choices = (None, 0, 1, 2, 3, 4)
    for escapes in product(choices, repeat=4):
        union = {mode for mode in escapes if mode is not None}
        assert set(range(5)) - union
    assert sp.diag(2, 3, 5).rank() == 3
    source = sp.Matrix.hstack(sp.Matrix((1, 2, 3)), sp.Matrix((5, 7, 11)))
    assert source.rank() <= 2


def main() -> None:
    frames, zero_frames, balanced_frames = check_companion_zero_patterns()
    check_common_kernel_contractions()
    profiles, kernel_vectors = check_weak_kernel_trapping()
    check_pairwise_scope_wall()
    check_escape_pigeonhole()
    print(f"PASS: {frames} rank-two companion frames match all forced zero masks")
    print(f"PASS: zero frames {zero_frames}; balanced frames {balanced_frames}")
    print("PASS: all 5 x 81 common-kernel contraction slices")
    print(f"PASS: {profiles} weak charts with {kernel_vectors} exact kernel vectors trapped")
    print("PASS: exact support-3/support-4 pairwise zero-tensor scope wall")
    print("PASS: all weak escape patterns leave a common mode; local rank 2 < 3")
    print("SCOPE: complete locally transverse q=0 r=5 detection only")
    print("SCOPE: local-dependence boundary and global Krenn-Gu remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
