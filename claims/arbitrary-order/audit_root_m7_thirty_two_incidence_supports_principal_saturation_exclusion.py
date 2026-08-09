"""Independent matching-polynomial audit of the thirty support exclusions."""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import combinations, permutations, product

ROWS = ("r0", "r1", "r2", "r3", "r4", "a", "b")
W = (0, 0, 0, 0, 1, 0, 2)


def base_entries():
    data = {
        ("a", 0, 0): "a0", ("a", 1, 0): "g", ("a", 3, 2): "a3",
        ("a", 5, 1): "a5", ("a", 6, 1): "a6", ("b", 0, 0): "b0",
        ("b", 1, 0): "b1", ("b", 5, 2): "b5", ("b", 6, 1): "b6",
    }
    for root, u in enumerate((2, 3, 4, 5, 6)):
        data[(f"r{root}", u, 0)] = f"X{root}"
    for root, u in enumerate((0, 1, 2, 3, 4)):
        data[(f"r{root}", u, 1)] = f"Y{root}"
    for root, u in enumerate((1, 0, 6, 4, 2)):
        data[(f"r{root}", u, 2)] = f"Z{root}"
    return data


def polynomial(word, data):
    choices = {row: tuple((u, name) for (rr, u, c), name in data.items() if rr == row and c == word[u]) for row in ROWS}

    @cache
    def recurse(index, used):
        if index == 7:
            return ((),)
        answer = []
        for column, name in choices[ROWS[index]]:
            if not used & (1 << column):
                for tail in recurse(index + 1, used | (1 << column)):
                    answer.append((name,) + tail)
        return tuple(answer)

    return tuple(Counter(term) for term in recurse(0, 0))


def gcd_monomial(poly):
    common = poly[0].copy()
    for term in poly[1:]:
        common &= term
    return common


def stabilizer_size():
    edges = {(u, u + 1): 1 if u % 2 == 0 else 0 for u in range(6)}
    ports = {0: {0: {0, 1}, 1: {5, 6}, 2: {3}}, 1: {0: {0, 1}, 1: {6}, 2: {5}}}
    total = 0
    for rev, colours, swap in product((0, 1), permutations(range(3)), (0, 1)):
        phi = (lambda u: 6 - u) if rev else (lambda u: u)
        changed_edges = {tuple(sorted((phi(u), phi(v)))): colours[c] for (u, v), c in edges.items()}
        changed_ports = {0: {c: set() for c in range(3)}, 1: {c: set() for c in range(3)}}
        for p in range(2):
            for c, vertices in ports[p].items():
                changed_ports[1 - p if swap else p][colours[c]].update(phi(u) for u in vertices)
        total += changed_edges == edges and changed_ports == ports
    return total


def main() -> None:
    base = base_entries()
    base_support = {(row, u) for row, u, colour in base if colour == W[u]}

    def count(edges):
        data = {(row, u, W[u]): "q" for row, u in edges}
        return len(polynomial(W, data))

    missing = sorted(set(product(ROWS, range(7))) - base_support)
    pairs = [pair for pair in combinations(missing, 2) if count(base_support | set(pair)) > 2]
    assert len(pairs) == 30 and stabilizer_size() == 1

    words = {"w": W, "p": (1, 1, 1, 2, 1, 0, 1), "q": (1, 1, 1, 2, 2, 2, 0)}
    classes = Counter()
    legal = 0
    for index, pair in enumerate(pairs):
        data = dict(base)
        for j, (row, u) in enumerate(pair):
            data[(row, u, W[u])] = f"n{index}_{j}"
        c0, c1, c2 = (polynomial((colour,) * 7, data) for colour in range(3))
        pure_gcd = gcd_monomial(c0) + c1[0] + c2[0]
        selected = None
        for label in ("w", "p", "q"):
            mixed = polynomial(words[label], data)
            if label == "w":
                # The nonmonomial residual matching polynomial must agree
                # between C0 and Cw after removing their monomial gcds.
                g0, gw = gcd_monomial(c0), gcd_monomial(mixed)
                residual0 = sorted(tuple(sorted((term - g0).elements())) for term in c0)
                residualw = sorted(tuple(sorted((term - gw).elements())) for term in mixed)
                if residual0 == residualw and not +(gw - pure_gcd):
                    selected = label
                    break
            elif len(mixed) == 1 and not +(mixed[0] - pure_gcd):
                selected = label
                break
        assert selected is not None
        classes[selected] += 1
        legal += not any(row in ("a", "b") and u in (2, 4, 6) for row, u in pair)

    assert classes == Counter({"w": 15, "p": 14, "q": 1})
    assert legal == 18
    print("PASS: independent thirty-support principal-saturation audit")
    print("stabilizer/orbits: 1 / 30")
    print("certificates: 0000102=15, 1112101=14, 1112220=1")
    print("survivors: 0")
    print("endpoint legal/illegal: 18/12")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
