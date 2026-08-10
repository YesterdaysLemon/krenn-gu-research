"""Focused checks for the rigid-colour three-block primitive boundary.

The arbitrary-order proof is the written cycle and bipartition argument.
This script only reconstructs representative sparse tensors, the displayed
four-vertex completion obstruction, and the one-shore saturation boundary.
"""

from __future__ import annotations


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def matching_words(
    vertices: tuple[int, ...],
    labels: dict[tuple[int, int], tuple[int, int]],
) -> list[tuple[int, ...]]:
    if not vertices:
        return [()]

    order = tuple(sorted(vertices))
    position = {vertex: index for index, vertex in enumerate(order)}

    def rec(remaining: tuple[int, ...]):
        if not remaining:
            return [((), {})]
        u = remaining[0]
        answer = []
        for index in range(1, len(remaining)):
            v = remaining[index]
            key = edge(u, v)
            if key not in labels:
                continue
            label_u, label_v = labels[key]
            rest = remaining[1:index] + remaining[index + 1 :]
            for tail, assignment in rec(rest):
                current = dict(assignment)
                current[u] = label_u
                current[v] = label_v
                answer.append(((key,) + tail, current))
        return answer

    words = []
    for _, assignment in rec(order):
        words.append(tuple(assignment[vertex] for vertex in order))
    assert len(position) == len(order)
    return words


def cycle_labels(n: int) -> dict[tuple[int, int], tuple[int, int]]:
    labels = {}
    for vertex in range(n):
        neighbour = (vertex + 1) % n
        key = edge(vertex, neighbour)
        colour = vertex % 2
        labels[key] = (colour, colour)
    return labels


def one_shore_saturation_labels(n: int) -> dict[tuple[int, int], tuple[int, int]]:
    labels = cycle_labels(n)
    odd = range(1, n, 2)
    for u in odd:
        for v in odd:
            if u < v:
                # Exercise arbitrary binary endpoint labels, including
                # off-diagonal matrix units.
                labels[(u, v)] = ((u // 2) % 2, (v // 2 + 1) % 2)
    return labels


def check_order(n: int) -> None:
    labels = cycle_labels(n)
    shore = tuple(range(0, n, 2))
    first = set(shore[:2])
    second = set(shore[2:4])
    mediator = set(range(n)) - first - second

    proper_unions = (
        first,
        second,
        mediator,
        first | second,
        first | mediator,
        second | mediator,
    )
    assert all(not matching_words(tuple(sorted(vertices)), labels) for vertices in proper_unions)

    words = matching_words(tuple(range(n)), labels)
    assert sorted(words) == [(0,) * n, (1,) * n]

    cycle_support = set(labels)
    q = {0, 1, 2, 3}
    z_support = {
        edge(u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if edge(u, v) not in cycle_support
    }
    assert edge(0, 2) in z_support and edge(1, 3) in z_support
    assert edge(0, 1) not in z_support and edge(1, 2) not in z_support

    z_haf_q = int(edge(0, 1) in z_support and edge(2, 3) in z_support)
    z_haf_q += int(edge(0, 2) in z_support and edge(1, 3) in z_support)
    z_haf_q += int(edge(0, 3) in z_support and edge(1, 2) in z_support)
    assert z_haf_q == 1

    complement = tuple(vertex for vertex in range(n) if vertex not in q)
    complement_words = matching_words(complement, labels)
    assert (0,) * len(complement) in complement_words

    saturated = one_shore_saturation_labels(n)
    assert sorted(matching_words(tuple(range(n)), saturated)) == [
        (0,) * n,
        (1,) * n,
    ]

    deleted = {0, 2}  # x_0,x_1 in the even shore
    exposed = tuple(vertex for vertex in range(n) if vertex not in deleted)
    exposed_words = matching_words(exposed, saturated)
    assert len(exposed_words) == n // 2 - 1
    assert len(set(exposed_words)) == len(exposed_words)


def main() -> None:
    for n in (8, 10, 12, 14):
        check_order(n)
    print("rigid-colour primitive sharpness focused checks: PASS")
    print("scope: representative sparse cycles; arbitrary-order proof is written")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
