"""Exact k=3 signed-shift classification of minimum-density literal graphs."""

from __future__ import annotations

from itertools import permutations, product


PAIRS = ((0, 1), (0, 2), (1, 2))
M = {
    0: {(0, 1), (2, 3)},
    1: {(0, 2), (1, 3)},
    2: {(0, 3), (1, 2)},
}


def node(A, a):
    return 3 * A + a


def edges(signs):
    result = set()
    for (a, b), shift in zip(PAIRS, signs):
        for A in range(3):
            result.add(tuple(sorted((node(A, a), node((A + shift) % 3, b)))))
    assert len(result) == 9
    return result


def component_sizes(edge_set):
    neighbors = {t: set() for t in range(9)}
    for t, u in edge_set:
        neighbors[t].add(u)
        neighbors[u].add(t)
    assert {len(ns) for ns in neighbors.values()} == {2}
    unseen = set(neighbors)
    sizes = []
    while unseen:
        start = unseen.pop()
        stack = [start]
        seen = {start}
        while stack:
            t = stack.pop()
            for u in neighbors[t]:
                if u not in seen:
                    seen.add(u)
                    unseen.remove(u)
                    stack.append(u)
        sizes.append(len(seen))
    return sorted(sizes)


def independent_transversals(edge_set):
    out = []
    for colors in product(range(3), repeat=3):
        selected = {node(A, colors[A]) for A in range(3)}
        if not any(t in selected and u in selected for t, u in edge_set):
            out.append(colors)
    return out


def transform_signs(signs, color_map, reflection):
    # color_map sends old colors to new colors; reflection is +/-1 on Z3.
    inverse = {color_map[a]: a for a in range(3)}
    out = []
    for i, j in PAIRS:
        a, b = inverse[i], inverse[j]
        if a < b:
            shift = signs[PAIRS.index((a, b))]
        else:
            shift = -signs[PAIRS.index((b, a))]
        out.append(reflection * shift)
    return tuple(out)


def induced_color_map(port_map):
    transformed = {}
    for c, matching in M.items():
        image = {
            tuple(sorted((port_map[x], port_map[y])))
            for x, y in matching
        }
        transformed[c] = next(d for d, target in M.items() if image == target)
    return tuple(transformed[c] for c in range(3))


def main():
    target = (-1, -1, -1)
    cases = {
        (1, 1, 1): ((0, 1, 2), -1, (0, 1, 2, 3)),
        (1, 1, -1): ((0, 2, 1), -1, (0, 1, 3, 2)),
        (1, -1, -1): ((1, 2, 0), -1, (0, 2, 3, 1)),
    }
    constants = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
    for signs, (color_map, reflection, port_tuple) in cases.items():
        edge_set = edges(signs)
        assert component_sizes(edge_set) == [9]
        assert independent_transversals(edge_set) == constants
        assert transform_signs(signs, color_map, reflection) == target
        port_map = dict(enumerate(port_tuple))
        assert induced_color_map(port_map) == color_map
        print("C9", signs, "color_map", color_map,
              "component_reflection", reflection, "port_map", port_tuple)

    triangle = (1, -1, 1)
    triangle_edges = edges(triangle)
    avoiding = independent_transversals(triangle_edges)
    assert component_sizes(triangle_edges) == [3, 3, 3]
    assert (0, 2, 1) in avoiding and (0, 2, 1) not in constants
    assert len(avoiding) > 3
    print("TRIANGLES", triangle, "components", component_sizes(triangle_edges),
          "extra_independent", (0, 2, 1), "independent_count", len(avoiding))

    # Exhaust the simultaneous component/color isomorphisms: precisely the
    # three nontriangle normalized patterns reach the chosen C9 target.
    normalized = [(1, x, y) for x in (1, -1) for y in (1, -1)]
    reaches_target = []
    for signs in normalized:
        if any(transform_signs(signs, pi, r) == target
               for pi in permutations(range(3)) for r in (1, -1)):
            reaches_target.append(signs)
    assert set(reaches_target) == set(cases)
    print("K3_LITERAL_TOPOLOGY_CLASSIFICATION_PASS")


if __name__ == "__main__":
    main()
