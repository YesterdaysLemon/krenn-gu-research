"""Independent no-import audit of the bosonic defect boundary."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations


@dataclass(frozen=True)
class Quad:
    """The exact number rational + radical*sqrt(2)."""

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
    total = ZERO
    for permutation in permutations(range(len(matrix))):
        term = ONE
        for row, column in enumerate(permutation):
            term = term * matrix[row][column]
        total = total + term
    return total


def minor(matrix: list[list[Quad]], deleted_row: int, deleted_column: int) -> list[list[Quad]]:
    return [
        [entry for column, entry in enumerate(row) if column != deleted_column]
        for row_index, row in enumerate(matrix)
        if row_index != deleted_row
    ]


def main() -> None:
    bypass = [
        [Quad(1), Quad(1), Quad(1, -1)],
        [Quad(-1), Quad(1), Quad(1)],
        [Quad(1, 1), Quad(-1), Quad(1)],
    ]
    assert permanent(bypass) == ZERO
    diagonal_minors = [permanent(minor(bypass, index, index)) for index in range(3)]
    assert diagonal_minors == [ZERO, ZERO, ZERO]
    assert permanent(minor(bypass, 0, 1)) == Quad(0, 1)
    assert permanent(minor(bypass, 1, 0)) == Quad(0, 1)
    defect = Quad(2) * bypass[0][2] * bypass[1][2] * bypass[2][0] * bypass[2][1]
    assert defect == Quad(2)

    modes = {f"a{i}" for i in range(3)} | {f"b{i}" for i in range(3)}
    sources = {f"p{i}" for i in range(3)} | {f"q{i}" for i in range(3)}
    support = {(f"a{i}", f"p{j}") for i in range(3) for j in range(3)}
    support |= {(f"a{i}", f"q{i}") for i in range(3)}
    support |= {(f"b{i}", f"p{i}") for i in range(3)}
    support |= {(f"b{i}", f"q{i}") for i in range(3)}
    support |= {(f"b{i}", f"q{(i + 1) % 3}") for i in range(3)}
    assert len(modes) == len(sources) == 6
    assert len(support) == 21

    for c in range(3):
        pure = {
            (f"a{(c - 1) % 3}", f"q{(c - 1) % 3}"),
            (f"b{(c - 2) % 3}", f"q{(c - 2) % 3}"),
            (f"b{(c - 1) % 3}", f"q{c}"),
            (f"b{c}", f"p{c}"),
            (f"a{c}", f"p{(c - 1) % 3}"),
            (f"a{(c + 1) % 3}", f"p{(c + 1) % 3}"),
        }
        assert {left for left, _ in pure} == modes
        assert {right for _, right in pure} == sources

    theta = {
        ("a0", "p0"), ("a0", "p1"), ("a1", "p1"), ("a1", "p0"),
        ("a0", "p2"), ("a2", "p2"), ("a2", "p0"),
    }
    chords = {("a1", "p2"), ("a2", "p1")}
    assert len(theta) == 7 and theta | chords <= support
    assert {(f"b{i}", f"q{i}") for i in range(3)} <= support

    replay_modes = {f"a{i}": 1 for i in range(3)}
    replay_sources = {f"p{i}": 1 for i in range(3)}
    assert sum(replay_modes.values()) == sum(replay_sources.values()) == 3

    print("independent no-import bosonic Plucker defect audit: PASS")


if __name__ == "__main__":
    main()
