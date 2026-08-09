"""Independent no-import audit for the root m=7 boundary theorems."""

from fractions import Fraction
from functools import cache


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a, strict=True)]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    bt = transpose(b)
    return [
        [sum(x * y for x, y in zip(row, col, strict=True)) for col in bt] for row in a
    ]


def rank(matrix: list[list[int | Fraction]]) -> int:
    rows = [[Fraction(x) for x in row] for row in matrix]
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


def check_gram() -> None:
    jform = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    cols = []
    a = {(0, 0): 1, (3, 2): 1, (5, 1): 1, (6, 1): 1}
    b = {(0, 0): 1, (1, 0): 1, (5, 2): 1, (6, 1): -1}
    for u in range(7):
        for c in range(3):
            cols.append([Fraction(a.get((u, c), 0)), Fraction(b.get((u, c), 0))])
    rmat = transpose(cols)
    gram = matmul(matmul(transpose(rmat), jform), rmat)
    assert rank(rmat) == rank(gram) == 2


def check_cyclic_support() -> None:
    coloured_edges = {(p, (p + 2 * c) % 7): c for p in range(7) for c in range(3)}
    assert len(coloured_edges) == 21
    assert all(sum(p0 == p for p0, _ in coloured_edges) == 3 for p in range(7))
    assert all(sum(b0 == b for _, b0 in coloured_edges) == 3 for b in range(7))
    ledger = [
        "".join(str(c) for c in range(3) if (blocker - 2 * c) % 7 < 5)
        for blocker in range(7)
    ]
    assert ledger == ["02", "02", "01", "01", "012", "12", "12"]

    chosen = [(0, 0), (1, 1), (2, 4), (3, 5), (4, 6), (5, 2), (6, 3)]
    assert len({b for _, b in chosen}) == 7
    word = [None] * 7
    for edge in chosen:
        word[edge[1]] = coloured_edges[edge]
    assert word == [0, 0, 2, 2, 1, 1, 1]


def check_overlay() -> None:
    incidence = [
        [1, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1],
    ]
    assert rank(incidence) == 4
    # Columns of a right inverse, obtained from the displayed formulas.
    right_inverse = [
        [0, 1, 0, 0],
        [Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2)],
        [Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2), Fraction(1, 2)],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [Fraction(-1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)],
    ]
    assert matmul([[Fraction(x) for x in row] for row in incidence], right_inverse) == [
        [Fraction(i == j) for j in range(4)] for i in range(4)
    ]


def bit_subsets(items: tuple[int, ...], size: int) -> list[int]:
    if size == 0:
        return [0]
    if len(items) < size:
        return []
    head, *tail = items
    tail_tuple = tuple(tail)
    return bit_subsets(tail_tuple, size) + [
        (1 << head) | rest for rest in bit_subsets(tail_tuple, size - 1)
    ]


def even_subsets(mask: int) -> set[int]:
    current = mask
    result = set()
    while True:
        if current.bit_count() % 2 == 0:
            result.add(current)
        if current == 0:
            return result
        current = (current - 1) & mask


def check_frame_assignments_and_no_cube() -> None:
    roots = tuple(range(5))
    rmask = (1 << 5) - 1
    qmask = (1 << 5) | (1 << 6)
    support = {0, rmask | (1 << 5), rmask | (1 << 6)}
    for imask in bit_subsets(roots, 2):
        support.update((imask, imask | qmask))
    assert len(support) == 23

    assignments = 0
    for size in range(2, 6):
        for imask in bit_subsets(roots, size):
            allowed = (rmask ^ imask) | qmask
            choices = (
                (0, qmask)
                if size == 2
                else tuple((rmask ^ imask) | (1 << q) for q in (5, 6))
            )
            for amask in choices:
                assert not amask & ~allowed
                assert amask.bit_count() <= size
                assert amask.bit_count() % 2 == size % 2
                assert imask | amask in support
            assignments += 1
    assert assignments == 26

    universe = (1 << 7) - 1
    for size in (4, 6):
        for umask in bit_subsets(tuple(range(7)), size):
            cube = even_subsets(umask)
            complement = universe ^ umask
            base = complement
            while True:
                assert not {base ^ item for item in cube} <= support
                if base == 0:
                    break
                base = (base - 1) & complement


@cache
def hafnian_count(n: int) -> int:
    if n == 0:
        return 1
    return (n - 1) * hafnian_count(n - 2)


def main() -> None:
    check_gram()
    check_cyclic_support()
    check_overlay()
    check_frame_assignments_and_no_cube()
    assert [hafnian_count(n) for n in (2, 4, 6)] == [1, 3, 15]
    assert 15 - 9 - 9 - 9 == -12
    assert 15 - 9 + 9 - 9 == 6
    for r in range(1, 7):
        for k0 in range(8 - r):
            k2 = k0 + r
            assert k2 >= r
    print("independent root m=7 route-boundary audit: PASS")
    print("no exhaustive support, word, or matching search was performed")


if __name__ == "__main__":
    main()
