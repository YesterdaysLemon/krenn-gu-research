#!/usr/bin/env python3
"""Exact k=4 reciprocal control: all uniform-background tensors at A.

Every one of the six ordered foreground/background incidences at A is a
partial pair plus two orphan endpoints.  The array is globally hollow and
color regular, but it is not a full source.
"""

from itertools import product


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
VECTORS = {0: 1, 1: 2, 2: 3}

# Canonical c=2 partial-pair tensor.  Entries are (target component, port).
FIRST = ((1, 0), (1, 3), (1, 1), (2, 0))
SECOND = ((1, 1), (1, 0), (1, 2), (2, 0))


def port_change(first_colour, second_colour, background):
    image = {
        0: 0,
        VECTORS[first_colour]: 1,
        VECTORS[second_colour]: 2,
        VECTORS[background]: 3,
    }
    return tuple(image[u] for u in range(4))


def outgoing_from_A(source_colour, background):
    first_colour = (background + 1) % 3
    second_colour = (background + 2) % 3
    change = port_change(first_colour, second_colour, background)
    inverse = [0] * 4
    for u, v in enumerate(change):
        inverse[v] = u
    template = FIRST if source_colour == first_colour else SECOND
    assert source_colour in (first_colour, second_colour)
    answer = []
    for actual_port in range(4):
        component, canonical_port = template[change[actual_port]]
        answer.append(4 * component + inverse[canonical_port])
    return tuple(answer)


def complete_layer(first_colour, second_colour):
    """Complete the two prescribed A shores to a hollow permutation."""
    size = 16
    mapping = [None] * size
    forward = outgoing_from_A(first_colour, second_colour)
    reverse = outgoing_from_A(second_colour, first_colour)
    for u, v in enumerate(forward):
        mapping[u] = v
    for target_A, source_exterior in enumerate(reverse):
        assert mapping[source_exterior] is None
        mapping[source_exterior] = target_A

    used = {v for v in mapping if v is not None}
    sources = [u for u, v in enumerate(mapping) if v is None]
    targets = [v for v in range(size) if v not in used]

    def extend(index):
        if index == len(sources):
            return True
        u = sources[index]
        for slot, v in enumerate(targets):
            if v is None or u // 4 == v // 4:
                continue
            targets[slot] = None
            mapping[u] = v
            if extend(index + 1):
                return True
            mapping[u] = None
            targets[slot] = v
        return False

    assert extend(0)
    assert set(mapping) == set(range(size))
    assert all(u // 4 != v // 4 for u, v in enumerate(mapping))
    return tuple(mapping)


def resource_index(vertex, colour):
    component, port = divmod(vertex, 4)
    for index, edge in enumerate(MATCHINGS[colour]):
        if port in edge:
            return component, index
    raise AssertionError


def paired_source_edge(mapping, source_component, source_colour, target_colour):
    found = []
    for edge in MATCHINGS[source_colour]:
        u, v = (4 * source_component + port for port in edge)
        if resource_index(mapping[u], target_colour) == resource_index(mapping[v], target_colour):
            found.append((u, v))
    assert len(found) == 1
    return found[0]


def add(entries, u, v, cu, cv, weight, name):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    assert key not in entries
    entries[key] = (weight, name)


def build_entries():
    entries = {}
    for base in range(0, 16, 4):
        for colour, pairs in MATCHINGS.items():
            for u, v in pairs:
                add(entries, base + u, base + v, colour, colour, 1,
                    f"P{colour}:{base+u}-{base+v}")

    layers = {}
    for first, second in ((0, 1), (0, 2), (1, 2)):
        mapping = complete_layer(first, second)
        layers[(first, second)] = mapping
        weights = [1] * 16

        # Forward incidence at A.
        u, v = paired_source_edge(mapping, 0, first, second)
        weights[u], weights[v] = 1, -1

        # Reverse incidence at A, expressed on the first-colour shore.
        inverse = [0] * 16
        for x, y in enumerate(mapping):
            inverse[y] = x
        r, s = paired_source_edge(tuple(inverse), 0, second, first)
        x, y = inverse[r], inverse[s]
        assert x not in (u, v) and y not in (u, v)
        weights[x], weights[y] = 1, -1

        for x, (y, weight) in enumerate(zip(mapping, weights)):
            add(entries, x, y, first, second, weight,
                f"X{first}{second}:{x}-{y}")
    return entries, layers


def terms_for(word, entries):
    adjacency = {u: [] for u in range(16)}
    for (u, v, cu, cv), (weight, name) in entries.items():
        if word[u] == cu and word[v] == cv:
            adjacency[u].append((v, weight, name))
            adjacency[v].append((u, weight, name))

    def rec(unmatched):
        if not unmatched:
            return [(1, ())]
        u = min(unmatched, key=lambda x: sum(v in unmatched for v, _, _ in adjacency[x]))
        answer = []
        for v, weight, name in adjacency[u]:
            if v not in unmatched:
                continue
            for tail_weight, tail in rec(unmatched - {u, v}):
                answer.append((weight * tail_weight, (name,) + tail))
        return answer

    return rec(frozenset(range(16)))


def main():
    entries, layers = build_entries()
    crossings = [key for key in entries if key[0] // 4 != key[1] // 4]
    assert len(crossings) == 48
    degree = {(u, c): [] for u in range(16) for c in range(3)}
    for u, v, cu, cv in crossings:
        degree[(u, cu)].append(cv)
        degree[(v, cv)].append(cu)
    for (u, colour), neighbours in degree.items():
        assert sorted(neighbours) == [c for c in range(3) if c != colour]

    rows = 0
    for background in range(3):
        supported = {}
        for local in product(range(3), repeat=4):
            word = local + (background,) * 12
            terms = terms_for(word, entries)
            value = sum(weight for weight, _ in terms)
            target = int(local == (background,) * 4)
            assert value == target, (background, local, value, terms)
            if terms:
                supported[local] = tuple(weight for weight, _ in terms)
            rows += 1
        assert supported == {
            (0, 0, 0, 0): (1,) if background == 0 else (1, -1),
            (1, 1, 1, 1): (1,) if background == 1 else (1, -1),
            (2, 2, 2, 2): (1,) if background == 2 else (1, -1),
        }
    assert rows == 243

    # A row nonuniform on B keeps the global boundary explicit.
    failure = (0,) * 4 + (1, 2, 0, 0) + (0,) * 8
    terms = terms_for(failure, entries)
    value = sum(weight for weight, _ in terms)
    assert value != 0

    print("crossing_entries=48 color_regular=PASS")
    print("six_A_incidents=partial_pair_plus_two_orphans")
    print("A_all_three_backgrounds=3*81=243 exact_delta=PASS")
    print(f"outside_failure=0000|1200|0000|0000 coefficient={value} terms={len(terms)}")
    print("PARTIAL_ORPHAN_ALL_BACKGROUND_COMPONENT_PASS")


if __name__ == "__main__":
    main()
