"""Independent k=2 exhaustion of the all-split switched-cycle formula."""

from __future__ import annotations

from itertools import product


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
RESOURCES = {
    "A": ((0, 1), (4, 5), (2, 3), (6, 7)),
    "B": ((4, 6), (0, 2), (5, 7), (1, 3)),
    "C": ((0, 3), (4, 7), (1, 2), (5, 6)),
}
COLORS = {"A": 0, "B": 1, "C": 2}
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


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


ALL_MATCHINGS = tuple(perfect_matchings(range(8)))


def add(entries, u, v, cu, cv, weight, name):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    assert key not in entries, (key, entries.get(key), name)
    entries[key] = (weight, name)


def f_edges():
    edges = []
    for i in range(4):
        edges.append((f"A{i}", f"B{i}"))
        edges.append((f"B{i}", f"C{i}"))
        edges.append((f"C{i}", f"A{(i + 1) % 4}"))
    return tuple(edges)


F_EDGES = f_edges()


def resource(label):
    return RESOURCES[label[0]][int(label[1:])]


def build(bitmask):
    entries = {}
    maps = {}
    for base in (0, 4):
        for color, pairs in MATCHINGS.items():
            for x, y in pairs:
                add(entries, base + x, base + y, color, color, 1,
                    f"P{color}:{base+x}-{base+y}")

    for edge_index, (left, right) in enumerate(F_EDGES):
        left_resource = resource(left)
        right_resource = resource(right)
        right_order = right_resource[::-1] if (bitmask >> edge_index) & 1 else right_resource
        prime = PRIMES[edge_index]
        lane_map = {}
        for lane, (u, v) in enumerate(zip(left_resource, right_order)):
            weight = 1 if lane == 0 else prime
            add(entries, u, v, COLORS[left[0]], COLORS[right[0]], weight,
                f"F{edge_index}:{left}-{right}:{u}-{v}")
            lane_map[u] = v
            lane_map[v] = u
        maps[frozenset((left, right))] = lane_map
    return entries, maps


def mate_a(u):
    for edge in RESOURCES["A"]:
        if u == edge[0]:
            return edge[1]
        if u == edge[1]:
            return edge[0]
    raise AssertionError


def a_index(u):
    for i, edge in enumerate(RESOURCES["A"]):
        if u in edge:
            return i
    raise AssertionError


def functional_map(labels, maps):
    out = {}
    incoming_color = {}
    for u in range(8):
        i = a_index(u)
        if labels[i] == "B":
            target_label = f"B{i}"
        else:
            target_label = f"C{(i - 1) % 4}"
        edge_map = maps[frozenset((f"A{i}", target_label))]
        out[u] = edge_map[mate_a(u)]
        incoming_color[(u, out[u])] = COLORS[labels[i]]
    return out, incoming_color


def directed_cycles(out):
    cycles = []
    globally_seen = set()
    for start in out:
        if start in globally_seen:
            continue
        path = []
        at = start
        index = {}
        while at not in index and at not in globally_seen:
            index[at] = len(path)
            path.append(at)
            at = out[at]
        globally_seen.update(path)
        if at in index:
            cycles.append(tuple(path[index[at] :]))
    return cycles


def terms(word, entries):
    out = []
    for matching in ALL_MATCHINGS:
        weight = 1
        names = []
        for u, v in matching:
            key = (u, v, word[u], word[v])
            if key not in entries:
                break
            factor, name = entries[key]
            weight *= factor
            names.append(name)
        else:
            out.append((weight, tuple(names)))
    return out


def main():
    assert len(ALL_MATCHINGS) == 105
    checked_words = 0
    checked_saturated = 0
    checked_unsaturated = 0

    # Exhaust every straight/swapped endpoint bijection on the C12 resource
    # cycle, every nonconstant switch word, and every functional cycle.
    for bitmask in range(1 << len(F_EDGES)):
        entries, maps = build(bitmask)
        for labels in product(("B", "C"), repeat=4):
            if len(set(labels)) == 1:
                continue
            out, incoming_color = functional_map(labels, maps)
            for cycle in directed_cycles(out):
                word = [0] * 8
                for u in cycle:
                    word[out[u]] = incoming_color[(u, out[u])]
                actual = terms(tuple(word), entries)

                transitions = []
                cycle_set = set(cycle)
                for i in range(4):
                    if labels[i] == "B" and labels[(i + 1) % 4] == "C":
                        saturated = (
                            set(RESOURCES["A"][i]) <= cycle_set
                            and set(RESOURCES["A"][(i + 1) % 4]) <= cycle_set
                        )
                        if saturated:
                            edge_index = F_EDGES.index((f"B{i}", f"C{i}"))
                            transitions.append(PRIMES[edge_index])

                # There is exactly one term using no B--C resource edge.
                bc_prefixes = {
                    f"F{idx}:" for idx, (left, right) in enumerate(F_EDGES)
                    if left.startswith("B") and right.startswith("C")
                }
                baseline = [
                    weight
                    for weight, names in actual
                    if not any(any(name.startswith(prefix) for prefix in bc_prefixes)
                               for name in names)
                ]
                assert len(baseline) == 1, (bitmask, labels, cycle, word, actual)
                expected = [baseline[0]]
                for signature in transitions:
                    expected += [weight * signature for weight in expected]
                assert sorted(weight for weight, _ in actual) == sorted(expected), (
                    bitmask, labels, cycle, word, transitions, actual, expected
                )
                checked_words += 1
                checked_saturated += len(transitions)
                checked_unsaturated += sum(
                    labels[i] == "B" and labels[(i + 1) % 4] == "C"
                    for i in range(4)
                ) - len(transitions)

    print("endpoint_bijection_patterns", 1 << len(F_EDGES))
    print("switched_cycle_words_checked", checked_words)
    print("saturated_transition_occurrences", checked_saturated)
    print("unsaturated_transition_occurrences", checked_unsaturated)
    print("K2_ALL_SPLIT_FACTORIZATION_PASS")


if __name__ == "__main__":
    main()
