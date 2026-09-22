#!/usr/bin/env python3
"""Exact k=2 control: reciprocal C8+split repairs for all backgrounds."""

from functools import lru_cache
from itertools import product


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
PORT_CYCLE = (0, 2, 3, 1)  # induces M_0 -> M_1 -> M_2 -> M_0


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


ALL_MATCHINGS = perfect_matchings(tuple(range(8)))


def build_entries():
    entries = {}

    def add(u, v, colour_u, colour_v, weight):
        if u > v:
            u, v = v, u
            colour_u, colour_v = colour_v, colour_u
        key = (u, v, colour_u, colour_v)
        assert key not in entries
        entries[key] = weight

    for offset in (0, 4):
        for colour, pairs in MATCHINGS.items():
            for u, v in pairs:
                add(offset + u, offset + v, colour, colour, 1)

    # For each target/background colour e, source d=e+1 is a C8 and source
    # f=e-1 is its forced split repair.  The same affine port cycle in all
    # three columns is exactly what makes the reverse-shore repairs compatible.
    for target in range(3):
        c8_source = (target + 1) % 3
        split_source = (target - 1) % 3

        for u, weight in enumerate((1, 1, 1, -1)):
            add(u, 4 + PORT_CYCLE[u], c8_source, target, weight)

        partner = {
            u: v
            for x, y in MATCHINGS[split_source]
            for u, v in ((x, y), (y, x))
        }
        split_map = tuple(PORT_CYCLE[partner[u]] for u in range(4))
        split_weights = [0] * 4
        for x, y in MATCHINGS[split_source]:
            split_weights[x] = 1
            split_weights[y] = -1
        for u in range(4):
            add(u, 4 + split_map[u], split_source, target, split_weights[u])

    return entries


ENTRIES = build_entries()


def coefficient(word):
    value = 0
    terms = []
    for matching in ALL_MATCHINGS:
        weight = 1
        for u, v in matching:
            key = (u, v, word[u], word[v])
            if key not in ENTRIES:
                break
            weight *= ENTRIES[key]
        else:
            value += weight
            terms.append((matching, weight))
    return value, terms


def paired_depth(word, colour):
    return sum(
        word[offset + u] != colour and word[offset + v] != colour
        for offset in (0, 4)
        for u, v in MATCHINGS[colour]
    )


def main():
    crossing_entries = [key for key in ENTRIES if key[0] // 4 != key[1] // 4]
    assert len(crossing_entries) == 24
    degree = {(v, colour): 0 for v in range(8) for colour in range(3)}
    foreign = {(v, colour): [] for v in range(8) for colour in range(3)}
    for u, v, colour_u, colour_v in crossing_entries:
        degree[(u, colour_u)] += 1
        degree[(v, colour_v)] += 1
        foreign[(u, colour_u)].append(colour_v)
        foreign[(v, colour_v)].append(colour_u)
    assert set(degree.values()) == {2}
    for state, neighbours in foreign.items():
        assert sorted(neighbours) == [c for c in range(3) if c != state[1]]

    local_rows = 0
    for nonuniform_side in (0, 1):
        for background in range(3):
            for local_word in product(range(3), repeat=4):
                word = (
                    local_word + (background,) * 4
                    if nonuniform_side == 0
                    else (background,) * 4 + local_word
                )
                value, _ = coefficient(word)
                target = 1 if local_word == (background,) * 4 else 0
                assert value == target
                local_rows += 1
    assert local_rows == 486

    failures = []
    low_depth_failures = []
    for word in product(range(3), repeat=8):
        value, terms = coefficient(word)
        target = 1 if len(set(word)) == 1 else 0
        if value != target:
            depths = tuple(paired_depth(word, colour) for colour in range(3))
            failure = (word, value, len(terms), depths, terms)
            failures.append(failure)
            if min(depths) <= 1:
                low_depth_failures.append(failure)

    assert len(failures) == 195
    assert len(low_depth_failures) == 171
    first_word, first_value, term_count, depths, terms = low_depth_failures[0]
    assert first_word == tuple(map(int, "00010022"))
    assert (first_value, term_count, depths) == (-1, 1, (1, 3, 2))

    print("crossing_entries=24 state_degree=2 foreign_colours=one_each")
    print("reciprocal_background_slices=2*3*81=486 exact_delta=PASS")
    print("mixed_macro_rows=6 exact_zero=PASS")
    print("full_source_error_words=195")
    print("low_paired_depth_error_words=171")
    print("first_q1_failure=0001|0022 coefficient=-1 terms=1 q=(1,3,2)")
    print("first_q1_matching=" + repr(terms[0][0]))
    print("RECIPROCAL_ALL_BACKGROUND_C8_CONTROL_PASS")


if __name__ == "__main__":
    main()
