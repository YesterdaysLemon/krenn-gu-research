"""Independent no-import audit of the cofactor quotient-wedge invariant."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def rank(matrix: list[list[Fraction]]) -> int:
    rows = [row[:] for row in matrix]
    output = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(output, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[output], rows[pivot] = rows[pivot], rows[output]
        divisor = rows[output][column]
        rows[output] = [value / divisor for value in rows[output]]
        for i, row in enumerate(rows):
            if i == output or not row[column]:
                continue
            multiple = row[column]
            rows[i] = [
                value - multiple * base
                for value, base in zip(row, rows[output], strict=True)
            ]
        output += 1
    return output


def main() -> None:
    first = [Fraction(value) for value in (2, -3, 5, 7)]
    second = [Fraction(11) * value for value in first]
    assert all(
        first[i] * second[j] - first[j] * second[i] == 0
        for i, j in combinations(range(4), 2)
    )
    assert rank([first, second]) == 1

    nonproportional = [Fraction(value) for value in (1, 0, 0, 0)]
    assert rank([first, nonproportional]) == 2
    assert any(
        first[i] * nonproportional[j] - first[j] * nonproportional[i] != 0
        for i, j in combinations(range(4), 2)
    )

    units: list[list[Fraction]] = []
    for index in range(8):
        vector = [Fraction(0) for _ in range(8)]
        vector[index] = Fraction(1)
        units.append(vector)
        matrix = [vector[:4], vector[4:]]
        assert rank(matrix) == 1
    assert rank(units) == 8

    delta = [Fraction(0), Fraction(0), Fraction(2), Fraction(3), Fraction(5)]
    for subset in combinations(range(5), 4):
        product = Fraction(1)
        for index in subset:
            product *= delta[index]
        assert product == 0
    assert delta[2] * delta[3] * delta[4] == 30

    print("independent no-import cofactor quotient-wedge audit: PASS")


if __name__ == "__main__":
    main()
