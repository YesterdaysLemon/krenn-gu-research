from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import product

M = {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)), 2: ((0, 3), (1, 2))}


def q(w, c):
    return sum(
        w[4 * k + u] != c and w[4 * k + v] != c for k in range(2) for u, v in M[c]
    )


def maps(r, s):
    return ({r[0]: s[0], r[1]: s[1]}, {r[0]: s[1], r[1]: s[0]})


def aligned(rp1, rp2, rq0, rq1):
    ans = []
    for f10, f20, f21 in product(maps(rp1, rq0), maps(rp2, rq0), maps(rp2, rq1)):
        # hidden Q0: unshared P ports from rp1,rp2 hit same Q0 port
        sp = next(iter(set(rp1) & set(rp2)))
        up1 = next(iter(set(rp1) - {sp}))
        up2 = next(iter(set(rp2) - {sp}))
        if f10[up1] != f20[up2]:
            continue
        # hidden P2: unshared Q ports from rq0,rq1 pull back to same P2 port
        sq = next(iter(set(rq0) & set(rq1)))
        uq0 = next(iter(set(rq0) - {sq}))
        uq1 = next(iter(set(rq1) - {sq}))
        inv20 = {v: u for u, v in f20.items()}
        inv21 = {v: u for u, v in f21.items()}
        if inv20[uq0] != inv21[uq1]:
            continue
        ans.append((f10, f20, f21))
    return ans


def terms_for(rp1, rp2, rq0, rq1, fs):
    edges = []
    for k in range(2):
        for c in range(3):
            for u, v in M[c]:
                edges.append((4 * k + u, 4 * k + v, c, c, f"P{k}{u}{v}[{c}]"))
    for a, b, r, s, f, name in (
        (1, 0, rp1, rq0, fs[0], "10"),
        (2, 0, rp2, rq0, fs[1], "20"),
        (2, 1, rp2, rq1, fs[2], "21"),
    ):
        for u in r:
            edges.append((u, 4 + f[u], a, b, f"X{name}:{u}-{f[u]}"))
    by = defaultdict(list)
    for e in edges:
        by[e[0]].append(e)
        by[e[1]].append(e)

    @lru_cache(None)
    def rec(mask):
        if mask == (1 << 8) - 1:
            return [((), ())]
        u = next(i for i in range(8) if not (mask >> i) & 1)
        out = []
        for x, y, a, b, n in by[u]:
            v = y if x == u else x
            if (mask >> v) & 1:
                continue
            cu, cv = (a, b) if x == u else (b, a)
            for ass, names in rec(mask | (1 << u) | (1 << v)):
                out.append((((u, cu), (v, cv)) + ass, (n,) + names))
        return out

    d = defaultdict(list)
    for ass, names in rec(0):
        w = [None] * 8
        for u, c in ass:
            w[u] = c
        d[tuple(w)].append(names)
    return d


if __name__ == "__main__":
    hist = defaultdict(int)
    examples = {}
    for ip1, ip2, iq0, iq1 in product(range(2), repeat=4):
        rp1, rp2, rq0, rq1 = M[1][ip1], M[2][ip2], M[0][iq0], M[1][iq1]
        for fi, fs in enumerate(aligned(rp1, rp2, rq0, rq1)):
            d = terms_for(rp1, rp2, rq0, rq1, fs)
            low = [
                (w, ts)
                for w, ts in d.items()
                if min(q(w, c) for c in range(3)) <= 1 and not all(x == w[0] for x in w)
            ]
            unique = [(w, ts[0]) for w, ts in low if len(ts) == 1]
            hist[(len(low), len(unique))] += 1
            examples.setdefault(
                (len(low), len(unique)), (ip1, ip2, iq0, iq1, fi, unique[:5])
            )
    assert hist == {(2, 2): 16, (1, 1): 16}, hist
    print("hist", dict(hist))
    for k, v in sorted(examples.items()):
        print(k, v[:5])
        for w, t in v[5]:
            print(
                " ",
                "".join(map(str, w[:4])) + "|" + "".join(map(str, w[4:])),
                [q(w, c) for c in range(3)],
                t,
            )
