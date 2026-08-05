"""No-import sanity checks for the arbitrary 3m+2 support theorem."""


def check_counts(m: int) -> None:
    assert 4 + 3 * (m - 1) == 3 * m + 1
    assert sum((m, m, m + 1)) == 3 * m + 1
    assert sum(edge_count - m for edge_count in (m, m, m + 1)) == 1


def check_repair(m: int) -> None:
    before = [0, 2] + [1] * (m - 2)
    assert sum(before) == m
    after = before.copy()
    after[0] += 1
    after[1] -= 1
    assert after == [1] * m

    # ell and the omitted coordinate cell have different mode endpoints but
    # the same source endpoint, so no matching uses both.
    ell = (0, 0)
    omitted = (1, 0)
    assert ell[0] != omitted[0]
    assert ell[1] == omitted[1]


def check_alternating_cycles() -> None:
    for cycle_length in range(4, 20, 2):
        new_edges = cycle_length // 2
        assert new_edges >= 2
    assert tuple(1 - bit for bit in (0, 1)) == (1, 0)


def main() -> None:
    for m in (3, 4, 5, 7, 12):
        check_counts(m)
        check_repair(m)
    check_alternating_cycles()
    print("independent no-import 3m+2 support sanity checks: PASS")
    print("no support, word, or matching enumeration was performed")


if __name__ == "__main__":
    main()
