"""Symbolic all-81 proof of the C8+split local boundary tensor."""

from __future__ import annotations

from collections import defaultdict
from itertools import product


A, B, C = 0, 1, 2
MATCHINGS = {
    A: ((0, 1), (2, 3)),
    B: ((0, 2), (1, 3)),
    C: ((0, 3), (1, 2)),
}
E = MATCHINGS[B]


def matching_partner(color, u):
    for x, y in MATCHINGS[color]:
        if u == x:
            return y
        if u == y:
            return x
    raise AssertionError


def add_poly(target, source, sign=1, exponent_shift=0):
    for exponent, coefficient in source.items():
        target[exponent + exponent_shift] += sign * coefficient


def boundary_polynomial(word):
    """Return Laurent polynomial after x0=t, x1=-t^-1, y0=y1=-1."""

    def rec(unmatched):
        if not unmatched:
            return {0: 1}
        u = min(unmatched)
        out = defaultdict(int)

        # Protected edge of the selected color at u.
        v = matching_partner(word[u], u)
        if v in unmatched and word[v] == word[u]:
            add_poly(out, rec(unmatched - {u, v}))

        # A full external two-lane resource can consume E_i only when its two
        # source endpoints have the same foreground color a or b.  If P_i=Q_i,
        # relative anti-alignment kills mixed a/b use by target collision.  If
        # P_i and Q_i are distinct, mixed use leaves two partial resources.
        for i, edge in enumerate(E):
            if u not in edge:
                continue
            v = edge[0] if edge[1] == u else edge[1]
            if v not in unmatched or word[v] != word[u]:
                continue
            tail = rec(unmatched - {u, v})
            if word[u] == A:
                # x0=t and x1=-t^-1 encode only x0*x1=-1.
                add_poly(out, tail, sign=(1 if i == 0 else -1),
                         exponent_shift=(1 if i == 0 else -1))
            elif word[u] == B:
                add_poly(out, tail, sign=-1)

        return {e: c for e, c in out.items() if c}

    return rec(frozenset(range(4)))


def main():
    nonzero = {}
    for word in product((A, B, C), repeat=4):
        polynomial = boundary_polynomial(word)
        expected = {0: 1} if word == (C, C, C, C) else {}
        assert polynomial == expected, (word, polynomial)
        if polynomial:
            nonzero[word] = polynomial
    assert nonzero == {(C, C, C, C): {0: 1}}
    print("local_words_checked", 81)
    print("surviving_boundary_words", {"cccc": {0: 1}})
    print("relations_used", "x0*x1=-1, y0=y1=-1, mixed caps forbidden")
    print("SYMBOLIC_C8_SPLIT_DELTA_PASS")


if __name__ == "__main__":
    main()
