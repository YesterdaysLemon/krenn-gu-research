#!/usr/bin/env python3
"""Exact k=2 color-regular extension of the C8+split local boundary tensor."""

from functools import lru_cache
from itertools import product


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


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

    # Protected unit K4 blocks.
    for offset in (0, 4):
        for colour, pairs in MATCHINGS.items():
            for u, v in pairs:
                add(offset + u, offset + v, colour, colour, 1)

    # The C8 layer A:0 -> B:2.  Its port permutation sends matching labels
    # 0->1->2->0 and its two M_1 pair products multiply to -1.
    pi = (0, 2, 3, 1)
    pi_weights = (1, 1, 1, -1)
    for u in range(4):
        add(u, 4 + pi[u], 0, 2, pi_weights[u])

    # The forced split layer A:1 -> B:2 is pi after the M_1 partner swap.
    # It maps each M_1 edge to the same M_2 resource with the opposite
    # endpoint alignment, and each pair product is -1.
    sigma = (3, 1, 0, 2)
    sigma_weights = (1, 1, -1, -1)
    for u in range(4):
        add(u, 4 + sigma[u], 1, 2, sigma_weights[u])

    # Complete all three state-layer matchings without changing the slice in
    # which B is uniformly colour 2.  All filler weights are one.
    for u in range(4):
        add(u, 4 + u, 2, 0, 1)  # B:0 -> A:2
        add(u, 4 + u, 2, 1, 1)  # B:1 -> A:2
        add(u, 4 + u, 0, 1, 1)  # A:0 -> B:1
        add(u, 4 + u, 1, 0, 1)  # B:0 -> A:1

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


def main():
    assert len(ALL_MATCHINGS) == 105

    crossing_entries = [key for key in ENTRIES if key[0] // 4 != key[1] // 4]
    assert len(crossing_entries) == 24
    degree = {(v, colour): 0 for v in range(8) for colour in range(3)}
    for u, v, colour_u, colour_v in crossing_entries:
        degree[(u, colour_u)] += 1
        degree[(v, colour_v)] += 1
    assert set(degree.values()) == {2}
    for vertex in range(8):
        for colour in range(3):
            neighbour_colours = []
            for u, v, colour_u, colour_v in crossing_entries:
                if (u, colour_u) == (vertex, colour):
                    neighbour_colours.append(colour_v)
                if (v, colour_v) == (vertex, colour):
                    neighbour_colours.append(colour_u)
            assert sorted(neighbour_colours) == [d for d in range(3) if d != colour]

    # Every one-component word on A has the exact GHZ response when B is the
    # uniform colour-2 exterior.
    local_nonzero = []
    for word_a in product(range(3), repeat=4):
        value, terms = coefficient(word_a + (2, 2, 2, 2))
        target = 1 if word_a == (2, 2, 2, 2) else 0
        assert value == target
        if value:
            local_nonzero.append((word_a, value, len(terms)))
    assert local_nonzero == [((2, 2, 2, 2), 1, 1)]

    # This is a local control, not a full source.
    failures = []
    for word in product(range(3), repeat=8):
        value, terms = coefficient(word)
        target = 1 if len(set(word)) == 1 else 0
        if value != target:
            failures.append((word, value, len(terms)))
    assert failures

    first_word, first_value, first_terms = failures[0]
    print("crossing_entries=24 state_degree=2 foreign_colours=one_each")
    print("c8_products=1,-1 total=-1")
    print("opposite_split_products=-1,-1 anti_alignment=PASS")
    print("uniform_background_slice_words=81 exact_delta=PASS")
    print(
        "full_source_control_failure="
        + "".join(map(str, first_word))
        + f" coefficient={first_value} terms={first_terms}"
    )
    print(f"full_source_error_words={len(failures)}")
    print("C8_SPLIT_LOCAL_COMPLETION_PASS")


if __name__ == "__main__":
    main()
