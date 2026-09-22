"""Exact k=2 rational macro array with degree <=2 and 13 crossings."""

from __future__ import annotations

from collections import Counter
from itertools import product


COLORS = range(3)
M = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def entries(include_excess):
    out = {}
    names = {}
    crossing = set()
    for base, component in ((0, "A"), (4, "B")):
        for c in COLORS:
            for x, y in M[c]:
                key = (base + x, base + y, c, c)
                out[key] = 1
                names[key] = f"P_{component}{c}:{base+x}-{base+y}"
    for a in COLORS:
        for b in COLORS:
            if a == b:
                continue
            center = (0, 4, a, b)
            leaf = (a + 1, b + 5, a, b)
            out[center] = 1
            out[leaf] = -1
            names[center] = f"C_{a}{b}:0-4"
            names[leaf] = f"L_{a}{b}:{a+1}-{b+5}"
            crossing.update((center, leaf))
    if include_excess:
        extra = (2, 5, 0, 1)
        assert extra not in out
        out[extra] = 2
        names[extra] = "E:2-5[0,1]"
        crossing.add(extra)
    return out, names, crossing


def state_degrees(crossing):
    degree = Counter()
    for u, v, a, b in crossing:
        degree[(u, a)] += 1
        degree[(v, b)] += 1
    return degree


def enumerate_words(table, names):
    matchings = tuple(perfect_matchings(range(8)))
    assert len(matchings) == 105
    result = {}
    for word in product(COLORS, repeat=8):
        terms = []
        for matching in matchings:
            weight = 1
            used = []
            for u, v in matching:
                key = (u, v, word[u], word[v])
                if key not in table:
                    break
                weight *= table[key]
                used.append(names[key])
            else:
                terms.append((weight, tuple(used)))
        result[word] = (sum(weight for weight, _ in terms), tuple(terms))
    return result


def main():
    base_table, base_names, base_crossing = entries(False)
    full_table, full_names, full_crossing = entries(True)
    assert len(base_crossing) == 12
    assert len(full_crossing) == 13
    degrees = state_degrees(full_crossing)
    assert max(degrees.values()) == 2

    base = enumerate_words(base_table, base_names)
    full = enumerate_words(full_table, full_names)
    macro = {}
    for a in COLORS:
        for b in COLORS:
            word = (a,) * 4 + (b,) * 4
            macro[(a, b)] = full[word][0]
            assert full[word][0] == (1 if a == b else 0)
            assert all("E:" not in name for _, term in full[word][1] for name in term)

    changed = [word for word in full if full[word][0] != base[word][0]]
    live = [
        (word, coefficient, terms)
        for word, (coefficient, terms) in full.items()
        if any("E:" in name for _, term in terms for name in term)
    ]
    assert changed and live

    witness = (0, 1, 0, 1, 1, 1, 0, 0)
    coefficient, terms = full[witness]
    assert coefficient != 0
    extra_terms = [(weight, term) for weight, term in terms if "E:2-5[0,1]" in term]
    assert extra_terms
    assert any(
        set(term) == {
            "C_01:0-4", "P_A1:1-3", "E:2-5[0,1]", "P_B0:6-7"
        }
        for _, term in extra_terms
    )

    print("crossing_entries", len(full_crossing))
    print("maximum_state_crossing_degree", max(degrees.values()))
    print("state_degree_histogram", dict(sorted(Counter(degrees.values()).items())))
    print("mixed_macro_coefficients", macro)
    print("words_with_extra_matching", len(live))
    print("coefficients_changed_from_12_entry_array", len(changed))
    print("witness", "0101|1100", "coefficient", coefficient)
    for weight, term in terms:
        print(" ", weight, "*", ", ".join(term))
    print("DEGREE_TWO_MACRO_EXCESS_PASS")


if __name__ == "__main__":
    main()
