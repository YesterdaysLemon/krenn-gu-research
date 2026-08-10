"""Focused exact checks for the rigid-colour cancellation boundary.

The arbitrary-order theorem is the written matching bijection.  This script
checks endpoint conventions and the displayed six-vertex countermechanism.
"""

from collections import defaultdict
from itertools import product

VERTICES = tuple(range(6))


def edge_data():
    edges = {}
    for i in range(3):
        for j in range(3):
            d = (j - i) % 3
            edges[(i, 3 + j)] = (d, d, 1)
    edges.update(
        {
            (0, 1): (1, 2, 1),
            (1, 2): (1, 2, 1),
            (0, 2): (2, 1, 1),
            (3, 4): (2, 1, -1),
            (4, 5): (2, 1, -1),
            (3, 5): (1, 2, -1),
        }
    )
    return edges


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            out.append(((first, second),) + tail)
    return out


def matching_word_and_weight(matching, edges):
    word = [None] * len(VERTICES)
    weight = 1
    for u, v in matching:
        labels = edges[(u, v)]
        word[u], word[v] = labels[0], labels[1]
        weight *= labels[2]
    return tuple(word), weight


def coefficient(vertices, word, edges):
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            label_u, label_v, weight = edges[(u, v)]
            if word[u] != label_u or word[v] != label_v:
                term = 0
                break
            term *= weight
        total += term
    return total


def pure_hafnian(vertices, colour, edges):
    word = {vertex: colour for vertex in vertices}
    return coefficient(tuple(vertices), word, edges)


def oriented_edge(vertex, other, edges):
    u, v = sorted((vertex, other))
    label_u, label_v, weight = edges[(u, v)]
    if vertex == u:
        return label_u, label_v, weight
    return label_v, label_u, weight


def check_rigidity(colour, edges):
    for vertex in VERTICES:
        for other in VERTICES:
            if vertex == other:
                continue
            u, v = sorted((vertex, other))
            label_u, label_v, _ = edges[(u, v)]
            local = label_u if vertex == u else label_v
            remote = label_v if vertex == u else label_u
            if remote == colour:
                assert local == colour


def main():
    edges = edge_data()
    assert len(edges) == 15
    assert all(weight != 0 for _, _, weight in edges.values())

    matchings = perfect_matchings(VERTICES)
    assert len(matchings) == 15

    contributions = defaultdict(list)
    for matching in matchings:
        word, weight = matching_word_and_weight(matching, edges)
        contributions[word].append((matching, weight))

    pure = {(0,) * 6, (1,) * 6, (2,) * 6}
    cancelled = {
        (0, 1, 2, 0, 2, 1),
        (1, 2, 0, 2, 1, 0),
        (2, 0, 1, 1, 0, 2),
    }
    residual = {
        (1, 1, 2, 1, 1, 2),
        (1, 2, 1, 1, 2, 1),
        (1, 2, 2, 1, 2, 2),
        (2, 1, 1, 2, 1, 1),
        (2, 1, 2, 2, 1, 2),
        (2, 2, 1, 2, 2, 1),
    }
    assert set(contributions) == pure | cancelled | residual
    for word in pure:
        assert [weight for _, weight in contributions[word]] == [1]
    for word in cancelled:
        assert sorted(weight for _, weight in contributions[word]) == [-1, 1]
    for word in residual:
        assert [weight for _, weight in contributions[word]] == [-1]

    expected = {word: 1 for word in pure}
    expected.update({word: -1 for word in residual})
    for word in product(range(3), repeat=6):
        actual = sum(weight for _, weight in contributions.get(word, ()))
        assert actual == expected.get(word, 0)

    check_rigidity(0, edges)

    # Near-monochromatic deck identity for the exact colour-0 slice.
    for vertex in VERTICES:
        for local_colour in range(3):
            deck_sum = 0
            for other in VERTICES:
                if other == vertex:
                    continue
                local, remote, weight = oriented_edge(vertex, other, edges)
                if local == local_colour and remote == 0:
                    complement = tuple(
                        v for v in VERTICES if v not in (vertex, other)
                    )
                    deck_sum += weight * pure_hafnian(complement, 0, edges)
            assert deck_sum == (1 if local_colour == 0 else 0)

    # Two-point cofactor/cross-correction identity on every pure colour-0 edge.
    for (p, q), (label_p, label_q, edge_weight) in edges.items():
        if (label_p, label_q) != (0, 0):
            continue
        outside = tuple(v for v in VERTICES if v not in (p, q))
        for other_colour in (1, 2):
            word = {v: other_colour for v in VERTICES}
            word[p] = word[q] = 0
            expansion = edge_weight * pure_hafnian(outside, other_colour, edges)
            for index, u in enumerate(outside):
                for v in outside[index + 1 :]:
                    p_u = oriented_edge(p, u, edges)
                    p_v = oriented_edge(p, v, edges)
                    q_u = oriented_edge(q, u, edges)
                    q_v = oriented_edge(q, v, edges)
                    x_pu = p_u[2] if p_u[:2] == (0, other_colour) else 0
                    x_pv = p_v[2] if p_v[:2] == (0, other_colour) else 0
                    x_qu = q_u[2] if q_u[:2] == (0, other_colour) else 0
                    x_qv = q_v[2] if q_v[:2] == (0, other_colour) else 0
                    remaining = tuple(w for w in outside if w not in (u, v))
                    expansion += (x_pu * x_qv + x_pv * x_qu) * pure_hafnian(
                        remaining, other_colour, edges
                    )
            assert coefficient(VERTICES, word, edges) == expansion == 0

    # Audit the global rigid-colour factorization on every word of the gadget.
    for word_tuple in product(range(3), repeat=6):
        word = dict(enumerate(word_tuple))
        colour_vertices = tuple(v for v in VERTICES if word[v] == 0)
        other_vertices = tuple(v for v in VERTICES if word[v] != 0)
        left = coefficient(VERTICES, word, edges)
        right = pure_hafnian(colour_vertices, 0, edges) * coefficient(
            other_vertices, word, edges
        )
        assert left == right

    # Every target coefficient involving colour zero is correct.
    for word_tuple in product(range(3), repeat=6):
        if 0 not in word_tuple:
            continue
        target = 1 if len(set(word_tuple)) == 1 else 0
        assert coefficient(VERTICES, dict(enumerate(word_tuple)), edges) == target

    print("rigid-colour focused verification: PASS")
    print("15 exact perfect matchings and all 3^6 coefficient words checked")
    print("global colour-0 factorization checked on the displayed gadget")
    print("displayed graph is a Krenn-Gu witness: false")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
