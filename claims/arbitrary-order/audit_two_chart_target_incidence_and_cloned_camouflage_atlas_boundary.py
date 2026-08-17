"""Independent no-import audit for the two-chart/cloned-atlas theorem.

This script uses only the Python standard library.  It does not import the
primary verifier or SymPy.  Its physical replay enumerates perfect matchings
directly rather than using the corrected-compound formula.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

COLORS = range(3)


def matrix_rank(rows: list[list[Fraction]]) -> int:
    work = [row[:] for row in rows]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def transpose(rows: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*rows, strict=True)]


def verify_affine_control_independently() -> None:
    injective_sensor = [[Fraction(1)], [Fraction(1)]]
    nonincident_target = [[Fraction(1), Fraction(0)], [Fraction(1), Fraction(-1)]]
    assert matrix_rank(injective_sensor) == 1
    assert matrix_rank(nonincident_target) == 2

    for mixed_size in range(2, 9):
        dim_f = mixed_size + 1
        column_count = 1 + 2 * mixed_size
        row_count = 2 * dim_f
        sensor = [[Fraction(0) for _ in range(column_count)] for _ in range(row_count)]

        # Common A column.
        sensor[0][0] = 1
        sensor[dim_f][0] = 1

        # B0 has the mixed coordinate columns x_i.
        for index in range(mixed_size):
            sensor[1 + index][1 + index] = 1

        # B1 has columns d+x_i.
        for index in range(mixed_size):
            column = 1 + mixed_size + index
            sensor[dim_f][column] = 1
            sensor[dim_f + 1 + index][column] = 1

        tau = [Fraction(0) for _ in range(row_count)]
        tau[0] = 1
        augmented = [row + [tau[index]] for index, row in enumerate(sensor)]
        assert matrix_rank(sensor) == 2 * mixed_size + 1
        assert matrix_rank(augmented) == 2 * mixed_size + 2

        # ell=(phi0,-phi1), with phi1=d*-sum x_i*.
        ell = [Fraction(0) for _ in range(row_count)]
        ell[0] = 1
        ell[dim_f] = -1
        for index in range(mixed_size):
            ell[dim_f + 1 + index] = 1
        for column in transpose(sensor):
            assert sum(x * y for x, y in zip(ell, column, strict=True)) == 0
        assert sum(x * y for x, y in zip(ell, tau, strict=True)) == 1

        aggregate = [ell[i] + ell[dim_f + i] for i in range(dim_f)]
        assert aggregate == [Fraction(0)] + [Fraction(1)] * mixed_size

        # One common tensor can avoid each named mixed coordinate.
        for omitted in range(mixed_size):
            active = (omitted + 1) % mixed_size
            coefficients = [Fraction(1)] + [Fraction(0)] * mixed_size
            coefficients[1 + active] = -1
            assert coefficients[0] == 1
            assert coefficients[1 + omitted] == 0
            assert sum(coefficients[1:]) == -1


def frame(port: int, sign: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if port in (0, 1):
        a, b = (1, 0, 0), (0, 1, 0)
    else:
        a, b = (0, 1, 0), (1, 0, 0)
    return a, tuple(sign * value for value in b)


def k_entry(i: int, j: int, ci: int, cj: int, sign: int) -> Fraction:
    ai, bi = frame(i, sign)
    aj, bj = frame(j, sign)
    return Fraction(ai[ci] * bj[cj] + bi[ci] * aj[cj])


def diagonal_weights(i: int, j: int) -> tuple[Fraction, Fraction, Fraction]:
    if i > j:
        i, j = j, i
    if (i, j) == (0, 1) or (i == 2 and j >= 3):
        return Fraction(0), Fraction(0), Fraction(1)
    if (i, j) == (0, 2):
        return Fraction(1), Fraction(1), Fraction(0)
    if (i, j) == (1, 2):
        return Fraction(3), Fraction(2), Fraction(0)
    if i == 0 and j >= 3:
        return Fraction(1), Fraction(2, 3), Fraction(0)
    if i == 1 and j >= 3:
        return Fraction(2), Fraction(2), Fraction(0)
    return Fraction(0), Fraction(0), Fraction(0)


def d_entry(i: int, j: int, ci: int, cj: int) -> Fraction:
    if ci != cj:
        return Fraction(0)
    return diagonal_weights(i, j)[ci]


def direct_entry(i: int, j: int, ci: int, cj: int, sign: int) -> Fraction:
    return d_entry(i, j, ci, cj) - k_entry(i, j, ci, cj, sign)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for offset in range(1, len(vertices)):
        second = vertices[offset]
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS_6 = tuple(perfect_matchings(tuple(range(6))))


def graph_edge(
    left: int,
    right: int,
    colors: tuple[int, ...],
    window: tuple[int, ...],
    sign: int,
) -> Fraction:
    if left > right:
        return graph_edge(right, left, colors, window, sign)
    if (left, right) == (0, 1):
        return Fraction(1)
    if left in (0, 1) and right >= 2:
        port = window[right - 2]
        a, b = frame(port, sign)
        row = a if left == 0 else b
        return Fraction(row[colors[right]])
    port_left = window[left - 2]
    port_right = window[right - 2]
    return direct_entry(
        port_left,
        port_right,
        colors[left],
        colors[right],
        sign,
    )


def response_word(
    window: tuple[int, ...], word: tuple[int, ...], sign: int
) -> Fraction:
    colors = (0, 0) + word
    return sum(
        product_value(
            graph_edge(left, right, colors, window, sign) for left, right in matching
        )
        for matching in MATCHINGS_6
    )


def product_value(values) -> Fraction:
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def active_colors(window: tuple[int, ...], port: int) -> set[int]:
    answer: set[int] = set()
    for color in COLORS:
        for partner in window:
            if partner == port or not diagonal_weights(port, partner)[color]:
                continue
            remaining = tuple(v for v in window if v not in (port, partner))
            if any(
                other != color and diagonal_weights(remaining[0], remaining[1])[other]
                for other in COLORS
            ):
                answer.add(color)
    return answer


def verify_physical_atlas_independently() -> None:
    assert len(MATCHINGS_6) == 15
    clones = (3, 4, 5, 6)
    windows = tuple((0, 1, 2, clone) for clone in clones)
    expected_pure = (Fraction(3), Fraction(4, 3), Fraction(1))

    for window in windows:
        for sign in (1, -1):
            response = {
                word: response_word(window, word, sign)
                for word in product(COLORS, repeat=4)
            }
            assert tuple(response[(c, c, c, c)] for c in COLORS) == expected_pure
            assert all(
                value == 0 for word, value in response.items() if len(set(word)) > 1
            )

            for i, j in combinations(window, 2):
                for ci, cj in product(COLORS, repeat=2):
                    pair = direct_entry(i, j, ci, cj, sign) + k_entry(
                        i, j, ci, cj, sign
                    )
                    assert pair == d_entry(i, j, ci, cj)
            for port in window:
                assert active_colors(window, port) == {0, 1}

    # The selected atlas is identical under the two physical channel signs.
    for window in windows:
        for word in product(COLORS, repeat=4):
            assert response_word(window, word, 1) == response_word(window, word, -1)
    assert k_entry(0, 1, 0, 1, 1) == 1
    assert k_entry(0, 1, 0, 1, -1) == -1

    for left, right in combinations(windows, 2):
        assert set(left) & set(right) == {0, 1, 2}


def main() -> None:
    verify_affine_control_independently()
    verify_physical_atlas_independently()
    print("independent two-chart target-incidence/cloned-atlas audit: PASS")


if __name__ == "__main__":
    main()
