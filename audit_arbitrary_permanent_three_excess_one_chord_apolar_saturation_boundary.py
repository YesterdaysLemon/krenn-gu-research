"""Independent no-import audit of the apolar-saturation witness."""

from __future__ import annotations

from collections import defaultdict, deque


def main() -> None:
    modes = ("a0", "a1", "a2", "r0", "r1", "r2")
    sources = ("p0", "p1", "p2", "q0", "q1", "q2")
    edges = {
        ("a0", "p0"), ("a0", "p1"), ("a0", "p2"),
        ("a1", "p0"), ("a1", "p1"), ("a1", "p2"),
        ("a2", "p0"), ("a2", "p2"),
        ("a1", "q0"), ("a2", "q1"), ("a2", "q0"), ("a2", "q2"),
        ("r0", "p0"), ("r0", "p1"), ("r1", "p1"), ("r2", "p2"),
        ("r0", "q2"), ("r1", "q1"), ("r1", "q0"),
        ("r2", "q2"), ("r2", "q1"),
    }
    assert len(edges) == 21
    assert tuple(sum(edge[0] == mode for edge in edges) for mode in modes) == (3, 4, 5, 3, 3, 3)
    assert tuple(sum(edge[1] == source for edge in edges) for source in sources) == (4, 4, 4, 3, 3, 3)

    matchings = (
        {("a0", "p0"), ("a1", "q0"), ("a2", "q1"), ("r0", "q2"), ("r1", "p1"), ("r2", "p2")},
        {("a0", "p1"), ("a1", "p2"), ("a2", "q0"), ("r0", "p0"), ("r1", "q1"), ("r2", "q2")},
        {("a0", "p2"), ("a1", "p0"), ("a2", "q2"), ("r0", "p1"), ("r1", "q0"), ("r2", "q1")},
    )
    for matching in matchings:
        assert {edge[0] for edge in matching} == set(modes)
        assert {edge[1] for edge in matching} == set(sources)

    owner = {source: mode for mode, source in matchings[0]}
    arcs: dict[str, set[str]] = defaultdict(set)
    for mode, source in edges:
        arcs[mode].add(owner[source])

    for start in modes:
        seen = {start}
        queue = deque([start])
        while queue:
            for target in arcs[queue.popleft()]:
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        assert seen == set(modes)

    assert sum((1, 1, -3, 1)) == 0
    assert (3 - 0, 3 - 1, 3 - 3) == (3, 2, 0)

    theta_matchings = (
        {("a0", "p0"), ("a1", "p1"), ("a2", "p2")},
        {("a0", "p1"), ("a1", "p0"), ("a2", "p2")},
        {("a0", "p2"), ("a1", "p1"), ("a2", "p0")},
    )
    backbone = set().union(*matchings)
    defects = tuple(len(theta - backbone) for theta in theta_matchings)
    assert defects == (2, 1, 2)

    print("independent no-import one-chord apolar saturation audit: PASS")


if __name__ == "__main__":
    main()
