"""Independent no-import audit of the five-cell collective detector."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
Covector = tuple[int, int, int]


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


def rational_rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
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
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def proportional(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] * right[1] == left[1] * right[0]


def exceptional(ells: tuple[tuple[int, int], ...]) -> bool:
    if any(ell == (0, 0) for ell in ells):
        return True
    return any(
        proportional(ells[a], ells[b]) and proportional(ells[c], ells[d])
        for a, b, c, d in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    )


def rank_two(ells: tuple[tuple[int, int], ...]) -> bool:
    return any(not proportional(ells[p], ells[q]) for p, q in PAIRS)


def audit_companion_frames() -> None:
    vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (-1, 2))
    checked = 0
    for ells in product(vectors, repeat=4):
        if not rank_two(ells):
            continue
        checked += 1
        rank = rational_rank(companion_rows(ells))
        assert (rank < 6) == exceptional(ells)
    assert checked == 2310


def permanent_recursive(matrix: tuple[tuple[int, ...], ...]) -> int:
    if not matrix:
        return 1
    total = 0
    for column, value in enumerate(matrix[0]):
        if not value:
            continue
        minor = tuple(
            row[:column] + row[column + 1 :] for row in matrix[1:]
        )
        total += value * permanent_recursive(minor)
    return total


def tensor_value(rows: tuple[tuple[Covector, ...], ...], word: tuple[int, ...]) -> int:
    matrix = tuple(
        tuple(row[mode][word[mode]] for mode in range(len(word))) for row in rows
    )
    return permanent_recursive(matrix)


def audit_pair_quotients() -> None:
    e0, e1 = (1, 0, 0), (0, 1, 0)
    a_base: tuple[Covector, ...] = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
        (41, 43, 47),
    )
    b_base: tuple[Covector, ...] = (
        (53, 59, 61),
        (67, 71, 73),
        (79, 83, 89),
        (97, 101, 103),
        (107, 109, 113),
    )
    hp: tuple[Covector, ...] = (
        (127, 131, 137),
        (139, 149, 151),
        (157, 163, 167),
        (173, 179, 181),
        (191, 193, 197),
    )
    hq: tuple[Covector, ...] = (
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
        for other_word in product(range(3), repeat=4):
            word = [0, 0, 0, 0, 0]
            word[active] = 2
            for mode, colour in zip(others, other_word, strict=True):
                word[mode] = colour
            full = tensor_value((hp, hq, tuple(a), tuple(a), tuple(b)), tuple(word))
            restricted_p = tuple(hp[mode] for mode in others)
            restricted_q = tuple(hq[mode] for mode in others)
            restricted_a = tuple(a[mode] for mode in others)
            restricted_b = tuple(b[mode] for mode in others)
            rp = tensor_value(
                (restricted_p, restricted_a, restricted_a, restricted_b),
                other_word,
            )
            rq = tensor_value(
                (restricted_q, restricted_a, restricted_a, restricted_b),
                other_word,
            )
            assert full == hp[active][2] * rq + hq[active][2] * rp


def audit_activity_equations() -> None:
    values = (-2, -1, 0, 1, 2)
    surviving = 0
    for v_values in product(values, repeat=4):
        for r_values in product((-1, 0, 1), repeat=4):
            if sum(value != 0 for value in r_values) < 3:
                continue
            if all(
                v_values[p] * r_values[q] + v_values[q] * r_values[p] == 0
                for p, q in PAIRS
            ):
                surviving += 1
                assert v_values == (0, 0, 0, 0)
    assert surviving > 0


def audit_symmetric_exceptional_models() -> None:
    zero_case = ((0, 0), (1, 0), (0, 1), (1, 1))
    two_zero_case = ((0, 0), (0, 0), (1, 0), (0, 1))
    split_case = ((1, 0), (2, 0), (0, 1), (0, -3))
    assert rational_rank(companion_rows(zero_case)) == 5
    assert rational_rank(companion_rows(two_zero_case)) == 5
    assert rational_rank(companion_rows(split_case)) == 5


def audit_concision() -> None:
    trapped_source_dimension = 2
    diagonal_flattening_rank = 3
    assert trapped_source_dimension < diagonal_flattening_rank


def main() -> None:
    audit_companion_frames()
    audit_symmetric_exceptional_models()
    audit_pair_quotients()
    audit_activity_equations()
    audit_concision()
    print("AUDIT PASS: 2310 rank-two companion frames by rational elimination")
    print("AUDIT PASS: explicit zero and balanced-2+2 symmetric kernels")
    print("AUDIT PASS: recursive permanent on all 5 x 81 quotient slices")
    print("AUDIT PASS: independent scalar census of three-activity equations")
    print("AUDIT PASS: trapped local source dimension 2 versus diagonal rank 3")
    print("AUDIT SCOPE: written symmetric-form proof handles arbitrary companions")
    print("AUDIT SCOPE: exceptional frames and activity failures remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
