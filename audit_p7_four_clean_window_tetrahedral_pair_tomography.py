"""Independent no-import audit of four-window pair tomography."""

from fractions import Fraction
from itertools import combinations

PORTS = tuple(range(1, 7))
EDGES = tuple(combinations(PORTS, 2))
WINDOWS = (
    frozenset((1, 2, 3, 4)),
    frozenset((1, 2, 5, 6)),
    frozenset((1, 3, 5, 6)),
    frozenset((1, 4, 5, 6)),
)
TARGET = frozenset((1, 2, 3, 4))


def rank(rows: list[list[Fraction]]) -> int:
    work = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    left - coefficient * right
                    for left, right in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def observations(values: dict[tuple[int, int], Fraction]):
    def star(window: frozenset[int], vertex: int) -> Fraction:
        return sum(
            values[tuple(sorted((vertex, other)))]
            for other in window
            if other != vertex
        )

    result = {
        (window, vertex): star(window, vertex)
        for window in WINDOWS
        for vertex in window
    }
    return result


def reconstruct(data):
    def shore(a: int, b: int) -> Fraction:
        window = frozenset((a, b, 5, 6))
        return (
            data[(window, a)]
            + data[(window, b)]
            - data[(window, 5)]
            - data[(window, 6)]
        ) / 2

    target = WINDOWS[0]
    p = shore(1, 2) - shore(1, 3)
    q = shore(1, 2) - shore(1, 4)
    answer = {}
    answer[(1, 2)] = (data[(target, 1)] + p + q) / 3
    answer[(1, 3)] = answer[(1, 2)] - p
    answer[(1, 4)] = answer[(1, 2)] - q
    a_value = data[(target, 2)] - answer[(1, 2)]
    b_value = data[(target, 3)] - answer[(1, 3)]
    c_value = data[(target, 4)] - answer[(1, 4)]
    answer[(2, 3)] = (a_value + b_value - c_value) / 2
    answer[(2, 4)] = (a_value + c_value - b_value) / 2
    answer[(3, 4)] = (b_value + c_value - a_value) / 2
    return answer


def main() -> None:
    matrix = [
        [
            Fraction(int(vertex in pair and set(pair) <= window))
            for pair in EDGES
        ]
        for window in WINDOWS
        for vertex in sorted(window)
    ]
    nuisance_columns = [
        index for index, pair in enumerate(EDGES) if not set(pair) <= TARGET
    ]
    nuisance = [[row[index] for index in nuisance_columns] for row in matrix]
    assert rank(matrix) == 14
    assert rank(nuisance) == 8

    for selected in EDGES:
        values = {
            pair: Fraction(int(pair == selected))
            for pair in EDGES
        }
        recovered = reconstruct(observations(values))
        for pair in combinations((1, 2, 3, 4), 2):
            assert recovered[pair] == values[pair]

    print("independent rational ranks: 14 and 8")
    print("fifteen coordinate-basis responses reconstruct target exactly")
    print("nuisance cancellation and six-dimensional recovery: AUDITED")


if __name__ == "__main__":
    main()
