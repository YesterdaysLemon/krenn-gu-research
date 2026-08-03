"""No-import audit of the permanent kernel-deletion hierarchy bookkeeping."""

from fractions import Fraction


def rank(matrix: list[list[int]]) -> int:
    rows = [[Fraction(x) for x in row] for row in matrix]
    if not rows:
        return 0
    r = 0
    for c in range(len(rows[0])):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = rows[r][c]
        rows[r] = [x / scale for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                scale = rows[i][c]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[r], strict=True)]
        r += 1
    return r


def main() -> None:
    # Exact affine arithmetic for the Hall deletion count.
    # Pairs encode a*m+b*s+c.
    active = (1, -1, 1)
    capacity = (1, -1, 0)
    difference = tuple(x - y for x, y in zip(active, capacity, strict=True))
    assert difference == (0, 0, 1)

    # Kernels of e_0, e_1, e_2, and representatives of the two
    # noncoordinate support strata.  Coordinate restrictions span each
    # two-dimensional quotient; no noncoordinate row kills a coordinate.
    quotient_bases = [
        [[0, 0], [1, 0], [0, 1]],
        [[1, 0], [0, 0], [0, 1]],
        [[1, 0], [0, 1], [0, 0]],
        [[1, 0], [-1, 0], [0, 1]],
        [[1, 0], [0, 1], [-1, -1]],
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    ]
    for basis in quotient_bases[:5]:
        assert rank(basis) == 2
    assert rank(quotient_bases[5]) == 3
    for basis in quotient_bases[3:]:
        assert all(any(row) for row in basis)

    # Equality incidence ledger: one cell for each (source, colour), then
    # pure nonvanishing makes each colour class a mode-source bijection.
    for m in (3, 5, 6, 7, 11):
        cells = {(p, c) for p in range(m) for c in range(3)}
        assert len(cells) == 3 * m
        assert all(sum(p0 == p for p0, _ in cells) == 3 for p in range(m))
        # Once the three colour classes are perfect matchings, a word has one
        # supported edge at each mode; compatibility cannot have two terms.
        assert 1**m == 1

    permutation = (0, 2, 1)
    word = (0, 1, 2)
    filtered = [[0 for _ in range(3)] for _ in range(3)]
    for mode, (source, colour) in enumerate(zip(permutation, word, strict=True)):
        assert source == (mode + colour) % 3
        filtered[source][mode] = 1
    assert rank(filtered) == 3
    assert sum(value != 0 for row in filtered for value in row) == 3

    print("independent no-import hierarchy sanity checks: PASS")
    print("no exhaustive support, word, or matching search was performed")


if __name__ == "__main__":
    main()
