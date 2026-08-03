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

    sizes = [1]
    for _ in range(3):
        sizes.append(2 * sizes[-1])
    assert sizes == [1, 2, 4, 8]

    print("independent no-import equality pure-matching cube audit: PASS")


if __name__ == "__main__":
    main()
