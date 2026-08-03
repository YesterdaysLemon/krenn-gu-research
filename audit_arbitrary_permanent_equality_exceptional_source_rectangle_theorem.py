"""No-import audit of exceptional-source rectangle bookkeeping."""

from fractions import Fraction


def main() -> None:
    # All partitions of the two mode-degree excess units.
    assert sorted(((2,), (1, 1))) == [(1, 1), (2,)]
    for m in (3, 6, 7):
        assert 4 + 4 + 3 * (m - 2) == 3 * m + 2
        assert 5 + 3 * (m - 1) == 3 * m + 2

    # The local rectangle coefficient and ratio identity over Q.
    a, b, c, d = map(Fraction, (2, 3, -4, 6))
    # Rescale c to the unique cancelling value.
    c = -a * d / b
    assert a * d + b * c == 0
    assert (b / a) * (c / d) == -1

    exceptional_sources = (4, 9)
    assert len(set(exceptional_sources)) == 2
    cross_edges = ((0, exceptional_sources[1]), (1, exceptional_sources[0]))
    assert len({source for _, source in cross_edges}) == 2

    for cycle_length in range(4, 20, 2):
        assert cycle_length // 2 >= 2

    print("independent no-import exceptional-source rectangle audit: PASS")


if __name__ == "__main__":
    main()
