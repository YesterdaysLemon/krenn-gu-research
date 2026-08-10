"""Independent no-import audit of the rigid-colour boundary gadget."""

from collections import defaultdict
from itertools import product

MATCHINGS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 1), (2, 4), (3, 5)),
    ((0, 1), (2, 5), (3, 4)),
    ((0, 2), (1, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    ((0, 3), (1, 2), (4, 5)),
    ((0, 3), (1, 4), (2, 5)),
    ((0, 3), (1, 5), (2, 4)),
    ((0, 4), (1, 2), (3, 5)),
    ((0, 4), (1, 3), (2, 5)),
    ((0, 4), (1, 5), (2, 3)),
    ((0, 5), (1, 2), (3, 4)),
    ((0, 5), (1, 3), (2, 4)),
    ((0, 5), (1, 4), (2, 3)),
)

EDGES = {
    (0, 1): (1, 2, 1),
    (0, 2): (2, 1, 1),
    (0, 3): (0, 0, 1),
    (0, 4): (1, 1, 1),
    (0, 5): (2, 2, 1),
    (1, 2): (1, 2, 1),
    (1, 3): (2, 2, 1),
    (1, 4): (0, 0, 1),
    (1, 5): (1, 1, 1),
    (2, 3): (1, 1, 1),
    (2, 4): (2, 2, 1),
    (2, 5): (0, 0, 1),
    (3, 4): (2, 1, -1),
    (3, 5): (1, 2, -1),
    (4, 5): (2, 1, -1),
}


def term(matching):
    labels = [None] * 6
    value = 1
    for edge in matching:
        left, right, weight = EDGES[edge]
        labels[edge[0]], labels[edge[1]] = left, right
        value *= weight
    return tuple(labels), value


def compatible_sum(vertices, word):
    vertex_set = set(vertices)
    total = 0
    for matching in MATCHINGS:
        used = {v for edge in matching for v in edge}
        if used != vertex_set:
            continue
        labels, weight = term(matching)
        if all(labels[v] == word[v] for v in vertices):
            total += weight
    if not vertices:
        return 1
    if len(vertices) < 6:
        # The fixed full ledger cannot list smaller matchings.  Reconstruct
        # them directly by filtering all pair partitions of the subset.
        vertices = tuple(sorted(vertices))

        def recurse(items):
            if not items:
                return [()]
            first = items[0]
            return [
                ((first, items[j]),) + tail
                for j in range(1, len(items))
                for tail in recurse(items[1:j] + items[j + 1 :])
            ]

        total = 0
        for matching in recurse(vertices):
            value = 1
            for edge in matching:
                left, right, weight = EDGES[edge]
                if left != word[edge[0]] or right != word[edge[1]]:
                    value = 0
                    break
                value *= weight
            total += value
    return total


def oriented(vertex, other):
    edge = tuple(sorted((vertex, other)))
    left, right, weight = EDGES[edge]
    if vertex == edge[0]:
        return left, right, weight
    return right, left, weight


def main():
    assert len(MATCHINGS) == 15
    assert len(set(MATCHINGS)) == 15
    assert len(EDGES) == 15

    ledger = defaultdict(list)
    for matching in MATCHINGS:
        word, value = term(matching)
        ledger[word].append(value)

    exact = {
        (0, 0, 0, 0, 0, 0): [1],
        (1, 1, 1, 1, 1, 1): [1],
        (2, 2, 2, 2, 2, 2): [1],
        (0, 1, 2, 0, 2, 1): [1, -1],
        (1, 2, 0, 2, 1, 0): [1, -1],
        (2, 0, 1, 1, 0, 2): [1, -1],
        (1, 1, 2, 1, 1, 2): [-1],
        (1, 2, 1, 1, 2, 1): [-1],
        (1, 2, 2, 1, 2, 2): [-1],
        (2, 1, 1, 2, 1, 1): [-1],
        (2, 1, 2, 2, 1, 2): [-1],
        (2, 2, 1, 2, 2, 1): [-1],
    }
    assert set(ledger) == set(exact)
    for word, values in exact.items():
        assert sorted(ledger[word]) == sorted(values)

    # Directly reconstruct the rigid-colour product, independently of the
    # primary script's recursive matching representation.
    for word_tuple in product((0, 1, 2), repeat=6):
        word = dict(enumerate(word_tuple))
        zeros = tuple(v for v in range(6) if word[v] == 0)
        nonzeros = tuple(v for v in range(6) if word[v] != 0)
        full = compatible_sum(tuple(range(6)), word)
        zero_word = {v: 0 for v in zeros}
        product_value = compatible_sum(zeros, zero_word) * compatible_sum(
            nonzeros, word
        )
        assert full == product_value

    # Independent one-open-vertex ledger for base colour zero.
    for vertex in range(6):
        for local_colour in range(3):
            total = 0
            for other in range(6):
                if other == vertex:
                    continue
                local, remote, weight = oriented(vertex, other)
                if (local, remote) != (local_colour, 0):
                    continue
                complement = tuple(v for v in range(6) if v not in (vertex, other))
                total += weight * compatible_sum(
                    complement, {v: 0 for v in complement}
                )
            assert total == (1 if local_colour == 0 else 0)

    assert all(
        sum(values) == (1 if len(set(word)) == 1 else 0)
        for word, values in ledger.items()
        if 0 in word
    )

    print("independent rigid-colour boundary audit: PASS")
    print("explicit 15-matching ledger; no import from primary verifier")
    print("six residual no-colour-0 words remain with coefficient -1")
    print("displayed graph is a Krenn-Gu witness: false")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
