"""Independent no-import audit of the seven-port five-helper selector."""

from fractions import Fraction
from itertools import combinations, product


PAIRS = tuple(combinations(range(7), 2))
FOURS = tuple(combinations(range(7), 4))


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def wick_rows(vectors: tuple[tuple[int, int], ...]) -> list[list[Fraction]]:
    rows = []
    for four in FOURS:
        four_set = set(four)
        row = []
        for pair in PAIRS:
            if set(pair) <= four_set:
                left, right = tuple(four_set - set(pair))
                a_i, b_i = vectors[left]
                a_j, b_j = vectors[right]
                row.append(Fraction(a_i * b_j + b_i * a_j))
            else:
                row.append(Fraction(0))
        rows.append(row)
    return rows


def selected(rows: list[list[Fraction]], pair: tuple[int, int]) -> bool:
    coordinate = [Fraction(0) for _ in PAIRS]
    coordinate[PAIRS.index(tuple(sorted(pair)))] = Fraction(1)
    return rank(rows + [coordinate]) == rank(rows)


def audit_representative_blocks() -> None:
    helpers = ((2, 5), (3, 7), (5, 11), (7, 13), (11, 17))
    full = wick_rows(((1, 0), (0, 1)) + helpers)
    assert rank(full) == 21
    assert selected(full, (0, 1))

    one = wick_rows(((0, 0), (1, 0)) + helpers)
    star_columns = [PAIRS.index((0, i)) for i in range(1, 7)]
    star_rows = [row for four, row in zip(FOURS, one, strict=True) if 0 in four]
    star = [[row[column] for column in star_columns] for row in star_rows]
    assert rank(star) == 6

    zero = wick_rows(((0, 0), (0, 0)) + helpers)
    column = PAIRS.index((0, 1))
    assert any(row[column] and sum(value != 0 for value in row) == 1 for row in zero)


def audit_tensor_cover() -> None:
    colours = tuple(
        (
            (index + 2, index + 9),
            (0, 0),
            (index + 4, 0) if index % 2 else (0, index + 6),
        )
        for index in range(7)
    )
    count = 0
    for u, v in PAIRS:
        for c_u, c_v in product(range(3), repeat=2):
            word = tuple(
                colours[port][c_u if port == u else c_v if port == v else 0]
                for port in range(7)
            )
            assert selected(wick_rows(word), (u, v))
            count += 1
    assert count == 189


def audit_boundaries() -> None:
    vectors = ((1, 1),) * 3 + ((1, -1),) * 3 + ((0, 0),)
    rows = wick_rows(vectors)
    six_rows = [row for four, row in zip(FOURS, rows, strict=True) if 6 not in four]
    six_columns = [i for i, pair in enumerate(PAIRS) if 6 not in pair]
    six = [[row[column] for column in six_columns] for row in six_rows]
    assert rank(six) == 10
    six_pairs = [PAIRS[index] for index in six_columns]
    rectangle = [Fraction(0) for _ in six_pairs]
    for pair, value in {
        (0, 3): 1,
        (0, 4): -1,
        (1, 3): -1,
        (1, 4): 1,
    }.items():
        rectangle[six_pairs.index(pair)] = Fraction(value)
    assert all(
        sum(left * right for left, right in zip(row, rectangle, strict=True)) == 0
        for row in six
    )

    union_rows = wick_rows(((1, 1),) * 5 + ((0, 0),) * 2)
    assert rank(union_rows) == 16
    kernel = [Fraction(0) for _ in PAIRS]
    for pair, value in {
        (0, 1): 1,
        (2, 3): 1,
        (0, 2): -1,
        (1, 3): -1,
    }.items():
        kernel[PAIRS.index(pair)] = Fraction(value)
    assert all(
        sum(left * right for left, right in zip(row, kernel, strict=True)) == 0
        for row in union_rows
    )


def main() -> None:
    audit_representative_blocks()
    audit_tensor_cover()
    audit_boundaries()
    print("seven-port five-helper tensor Wick independent audit: PASS")


if __name__ == "__main__":
    main()
