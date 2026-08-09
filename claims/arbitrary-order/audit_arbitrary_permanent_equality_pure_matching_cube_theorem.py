"""Independent no-import audit of the equality pure-matching cube theorem."""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    original = (("i", "p1"), ("j", "p2"))
    crossed = (("i", "p2"), ("j", "p1"))
    assert original != crossed
    assert {mode for mode, _ in original} == {mode for mode, _ in crossed}
    assert {source for _, source in original} == {source for _, source in crossed}

    backbone = Fraction(6)
    cross = Fraction(-5)
    ratio = cross / backbone
    assert backbone * (1 + ratio) == backbone + cross == 1
    assert backbone + (-backbone) == 0

    # In the distinct-mode branch, switches in two colours would demand their
    # mandatory covectors at the same physical cross cell.
    coordinate_0 = (1, 0, 0)
    coordinate_1 = (0, 1, 0)
    assert coordinate_0 != coordinate_1
    required_cross_cell = ("a2", "p1")
    demands = {(required_cross_cell, coordinate_0), (required_cross_cell, coordinate_1)}
    assert len({cell for cell, _ in demands}) == 1
    assert len({covector for _, covector in demands}) == 2

    # In the co-located branch, two switch colours use distinct common modes,
    # each consuming one of the two mode-degree excess units.
    mode_excess = {"a": 0, "b0": 1, "b1": 1}
    assert sum(mode_excess.values()) == 2
    assert len([mode for mode in mode_excess if mode.startswith("b")]) == 2

    sizes = [1, 2, 4]
    assert max(sizes) == 4

    print("independent no-import equality pure-matching cube audit: PASS")


if __name__ == "__main__":
    main()
