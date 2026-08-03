"""Independent no-import audit of the Hamming-face pinch ledger."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations


@dataclass(frozen=True)
class Quad:
    rational: int
    radical: int = 0

    def __add__(self, other: Quad) -> Quad:
        return Quad(self.rational + other.rational, self.radical + other.radical)

    def __mul__(self, other: Quad) -> Quad:
        return Quad(
            self.rational * other.rational + 2 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )


ZERO = Quad(0)
ONE = Quad(1)


def permanent(matrix: list[list[Quad]]) -> Quad:
    if not matrix:
        return ONE
    total = ZERO
    for permutation in permutations(range(len(matrix))):
        term = ONE
        for row, column in enumerate(permutation):
            term = term * matrix[row][column]
        total = total + term
    return total


def complement(matrix: list[list[Quad]], selected: set[int]) -> list[list[Quad]]:
    return [
        [entry for column, entry in enumerate(row) if column not in selected]
        for row_index, row in enumerate(matrix)
        if row_index not in selected
    ]


def main() -> None:
    bypass = [
        [Quad(1), Quad(1), Quad(1, -1)],
        [Quad(-1), Quad(1), Quad(1)],
        [Quad(1, 1), Quad(-1), Quad(1)],
    ]
    assert permanent(bypass) == ZERO
    assert [permanent(complement(bypass, {index})) for index in range(3)] == [ZERO, ZERO, ZERO]

    z = [Quad(2), Quad(3), Quad(5)]
    for first, second, remaining in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        coefficient = z[first] * z[second] * bypass[remaining][remaining]
        assert coefficient != ZERO
        replaced = [row[:] for row in bypass]
        for index in (first, second):
            replaced[index] = [ZERO, ZERO, ZERO]
            replaced[index][index] = z[index]
        assert permanent(replaced) == coefficient

    fully_replaced = [[ZERO, ZERO, ZERO] for _ in range(3)]
    for index in range(3):
        fully_replaced[index][index] = z[index]
    assert permanent(fully_replaced) == z[0] * z[1] * z[2] != ZERO

    print("independent no-import Hamming-face pinch audit: PASS")


if __name__ == "__main__":
    main()
