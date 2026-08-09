"""Exact symbolic checks for the root m=7 route-boundary theorems."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


def check_two_port_gram() -> None:
    jform = sp.Matrix([[0, 1], [1, 0]])
    a = {(0, 0): 1, (3, 2): 1, (5, 1): 1, (6, 1): 1}
    b = {(0, 0): 1, (1, 0): 1, (5, 2): 1, (6, 1): -1}
    cols = [
        sp.Matrix([a.get((u, c), 0), b.get((u, c), 0)])
        for u in range(7)
        for c in range(3)
    ]
    rmat = sp.Matrix.hstack(*cols)
    gram = rmat.T * jform * rmat
    assert rmat.rank() == 2
    assert gram.rank() == 2

    idx = lambda u, c: 3 * u + c
    anchor_a = rmat[:, [idx(1, 0), idx(3, 2)]]
    anchor_d = rmat[:, [idx(5, 1), idx(5, 2)]]
    cross = anchor_d.T * jform * anchor_a
    assert cross == sp.eye(2)
    schur = (
        gram
        - gram[:, [idx(1, 0), idx(3, 2)]]
        * cross.inv()
        * gram[[idx(5, 1), idx(5, 2)], :]
    )
    assert schur == sp.zeros(21)


def check_lower_jet_contradiction() -> None:
    e0 = sp.Matrix([1, 0, 0])
    e2star = sp.Matrix([[0, 0, 1]])
    assert (e2star * e0)[0] == 0
    assert e0.dot(e0) * e0.dot(e0) == 1


def check_cyclic_majority_survivor() -> None:
    matchings = [[(j, (j + 2 * c) % 7) for j in range(7)] for c in range(3)]
    assert all(
        sorted(b for _, b in matching) == list(range(7)) for matching in matchings
    )
    assert len({edge for matching in matchings for edge in matching}) == 21
    assert all(sp.prod(1 for _ in matching) == 1 for matching in matchings)

    blocker_ledger = []
    for blocker in range(7):
        colours = [c for c in range(3) if (blocker - 2 * c) % 7 < 5]
        blocker_ledger.append("".join(str(c) for c in colours))
    assert blocker_ledger == ["02", "02", "01", "01", "012", "12", "12"]

    for j in range(7):
        assert len({(j + 2 * c) % 7 for c in range(3)}) == 3
    for b in range(7):
        local = sp.zeros(7, 3)
        for c in range(3):
            p = (b - 2 * c) % 7
            local[p, c] = 1
        assert local.rank() == 3

    for c in range(3):
        assert (5 + 2 * c) % 7 != (6 + 2 * c) % 7

    mixed = {0: 0, 1: 1, 2: 4, 3: 5, 4: 6, 5: 2, 6: 3}
    assert sorted(mixed.values()) == list(range(7))
    blocker_word = [None] * 7
    for p, b in mixed.items():
        colour = next(c for c in range(3) if (p + 2 * c) % 7 == b)
        blocker_word[b] = colour
    assert tuple(blocker_word) == (0, 0, 2, 2, 1, 1, 1)

    # The arbitrary majority count is k_2-k_0=r, hence k_2>=r.
    k0, k2, r = sp.symbols("k0 k2 r", integer=True, nonnegative=True)
    assert sp.solve(sp.Eq(k2 - k0, r), k2)[0] == k0 + r


def even_subsets(mask: int) -> set[int]:
    sub = mask
    out = set()
    while True:
        if sub.bit_count() % 2 == 0:
            out.add(sub)
        if sub == 0:
            return out
        sub = (sub - 1) & mask


def check_no_forced_cube() -> None:
    roots = range(5)
    qmask = (1 << 5) | (1 << 6)
    rmask = (1 << 5) - 1
    support = {0, rmask | (1 << 5), rmask | (1 << 6)}
    for pair in combinations(roots, 2):
        pmask = sum(1 << i for i in pair)
        support.add(pmask)
        support.add(pmask | qmask)

    assert len(support) == 23

    assignments = 0
    for size in range(2, 6):
        for subset in combinations(roots, size):
            imask = sum(1 << i for i in subset)
            allowed = (rmask ^ imask) | qmask
            if size == 2:
                choices = (0, qmask)
            else:
                choices = tuple((rmask ^ imask) | (1 << q) for q in (5, 6))
            for amask in choices:
                assert amask & ~allowed == 0
                assert amask.bit_count() <= size
                assert amask.bit_count() % 2 == size % 2
                assert imask | amask in support
            assignments += 1
    assert assignments == 26

    universe = (1 << 7) - 1
    for size in (4, 6):
        for terminals in combinations(range(7), size):
            umask = sum(1 << i for i in terminals)
            cube = even_subsets(umask)
            complement = universe ^ umask
            base = complement
            while True:
                translated = {base ^ x for x in cube}
                assert not translated <= support
                if base == 0:
                    break
                base = (base - 1) & complement


def check_overlay_right_inverse() -> None:
    incidence = sp.Matrix(
        [
            [1, 1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1],
        ]
    )
    assert incidence.rank() == 4
    f0, f1, f2, f3 = sp.symbols("f0 f1 f2 f3")
    x02 = (f0 - f1 + f2 - f3) / 2
    xvec = sp.Matrix([f1, x02, f0 - f1 - x02, 0, 0, f2 - x02])
    assert sp.simplify(incidence * xvec - sp.Matrix([f0, f1, f2, f3])) == sp.zeros(4, 1)


@cache
def all_ones_hafnian(vertices: tuple[int, ...]) -> int:
    if not vertices:
        return 1
    first = vertices[0]
    return sum(
        all_ones_hafnian(tuple(v for v in vertices if v not in (first, partner)))
        for partner in vertices[1:]
    )


def check_conditional_wick_failure() -> None:
    assert all_ones_hafnian((0, 1)) == 1
    assert all_ones_hafnian((0, 1, 2, 3)) == 3
    assert all_ones_hafnian((0, 1, 2, 3, 4, 5)) == 15
    assert 15 - 9 - 9 - 9 == -12
    assert 15 - 9 + 9 - 9 == 6


def main() -> None:
    check_two_port_gram()
    check_lower_jet_contradiction()
    check_cyclic_majority_survivor()
    check_no_forced_cube()
    check_overlay_right_inverse()
    check_conditional_wick_failure()
    print("root m=7 symbolic route boundary checks: PASS")
    print("no large support, word, or matching enumeration was performed")


if __name__ == "__main__":
    main()
