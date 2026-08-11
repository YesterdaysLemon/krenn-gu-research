"""Verify the q=0, r=5 collective companion and activity detector."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def companion_matrix(ells: tuple[tuple[int, int], ...]) -> sp.Matrix:
    """Return the 8x6 scalar matrix for the collective companion map."""
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
    return left[0] * right[1] - left[1] * right[0] == 0


def exceptional(ells: tuple[tuple[int, int], ...]) -> bool:
    """Return the exact zero-companion or balanced-2+2 condition."""
    if any(ell == (0, 0) for ell in ells):
        return True
    pairings = (
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 3, 1, 2),
    )
    return any(
        proportional(ells[a], ells[b]) and proportional(ells[c], ells[d])
        for a, b, c, d in pairings
    )


def check_companion_classification() -> None:
    vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1))
    checked = 0
    for ells in product(vectors, repeat=4):
        if sp.Matrix(ells).rank() != 2:
            continue
        checked += 1
        rank = companion_matrix(ells).rank()
        assert (rank < 6) == exceptional(ells)
        assert rank in (5, 6)
    assert checked == 1220


def check_explicit_exceptional_kernels() -> None:
    cases = (
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((0, 0), (0, 0), (1, 0), (0, 1)),
        ((1, 0), (1, 0), (0, 1), (0, 1)),
    )
    for ells in cases:
        matrix = companion_matrix(ells)
        kernel = matrix.nullspace()
        assert matrix.rank() == 5
        assert len(kernel) == 1
        assert kernel[0] != sp.zeros(6, 1)


def permanent(matrix: list[list[int]]) -> int:
    size = len(matrix)
    return sum(
        sp.prod(matrix[row][assignment[row]] for row in range(size))
        for assignment in permutations(range(size))
    )


def check_pair_quotient() -> None:
    """Check all 5x81 quotient slices with a labelled permanent."""
    e0, e1 = (1, 0, 0), (0, 1, 0)
    for active in range(5):
        a = [tuple(3 * mode + colour + 2 for colour in range(3)) for mode in range(5)]
        b = [tuple(5 * mode + 2 * colour + 7 for colour in range(3)) for mode in range(5)]
        hp = [tuple(7 * mode + 3 * colour + 11 for colour in range(3)) for mode in range(5)]
        hq = [tuple(11 * mode + 5 * colour + 13 for colour in range(3)) for mode in range(5)]
        a[active] = e0
        b[active] = e1
        others = tuple(mode for mode in range(5) if mode != active)

        for other_word in product(range(3), repeat=4):
            word = [0, 0, 0, 0, 0]
            word[active] = 2
            for mode, colour in zip(others, other_word, strict=True):
                word[mode] = colour
            full = permanent(
                [
                    [row[mode][word[mode]] for mode in range(5)]
                    for row in (hp, hq, a, a, b)
                ]
            )
            rp = permanent(
                [
                    [row[mode][word[mode]] for mode in others]
                    for row in (hp, a, a, b)
                ]
            )
            rq = permanent(
                [
                    [row[mode][word[mode]] for mode in others]
                    for row in (hq, a, a, b)
                ]
            )
            expected = hp[active][2] * rq + hq[active][2] * rp
            assert full == expected


def check_activity_algebra() -> None:
    """Exhaust a small scalar model of v_p r_q+v_q r_p=0."""
    values = (-1, 0, 1)
    checked = 0
    for v_values in product(values, repeat=4):
        for r_values in product(values, repeat=4):
            if sum(value != 0 for value in r_values) < 3:
                continue
            if not all(
                v_values[p] * r_values[q] + v_values[q] * r_values[p] == 0
                for p, q in PAIRS
            ):
                continue
            checked += 1
            assert v_values == (0, 0, 0, 0)
    assert checked > 0


def check_transverse_four_mode_rank() -> None:
    """Check the normalized collision operator used in the corollary."""
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
    matrix = sp.Matrix.hstack(*columns)
    assert matrix.shape == (81, 12)
    assert matrix.rank() == 12


def check_local_concision() -> None:
    assert sp.diag(2, 3, 5).rank() == 3
    assert sp.Matrix.hstack(sp.Matrix((7, 11, 13)), sp.Matrix((2, 5, 17))).rank() <= 2


def main() -> None:
    check_companion_classification()
    check_explicit_exceptional_kernels()
    check_pair_quotient()
    check_activity_algebra()
    check_transverse_four_mode_rank()
    check_local_concision()
    print("PASS: 1220 exact rank-two companion frames match the classification")
    print("PASS: explicit zero and balanced-2+2 companion kernels")
    print("PASS: all 5 x 81 pair-collision quotient slices")
    print("PASS: exhaustive small scalar model of three-activity equations")
    print("PASS: normalized transverse four-mode collision rank 12")
    print("PASS: local source span at most 2 versus diagonal rank 3")
    print("SCOPE: collective q=0 r=5 detector under good companions and activity")
    print("SCOPE: exceptional companions, activity failure, and global remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
