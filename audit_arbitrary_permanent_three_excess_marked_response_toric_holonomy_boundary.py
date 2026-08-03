"""Independent no-import audit of marked-response holonomy boundary."""

from collections import Counter, defaultdict


def dot(vector, mark):
    return sum(value * direction for value, direction in zip(vector, mark, strict=True))


def reaches_all(adjacency, start, vertices):
    seen = {start}
    frontier = [start]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return seen == set(vertices)


def main():
    # Independent integer instance of the abstract response family.
    s, t = 2, 3
    omega_abstract = ((1, s), (t, 1))
    determinant = (
        omega_abstract[0][0] * omega_abstract[1][1]
        - omega_abstract[0][1] * omega_abstract[1][0]
    )
    assert determinant == 1 - s * t == -5
    assert 1 + s * t == 7

    modes = ("a0", "a1", "a2", "r1", "r2")
    sources = ("p0", "p1", "p2", "q1", "q2")
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    cells = {
        ("a0", "p0"): (1, 1, 1),
        ("a0", "p1"): (1, 2, 1),
        ("a0", "p2"): (1, 1, -2),
        ("a1", "p0"): e0,
        ("a1", "p1"): e0,
        ("a2", "p0"): e1,
        ("a2", "p2"): e1,
        ("a1", "q1"): e1,
        ("a1", "q2"): e2,
        ("a2", "q1"): e2,
        ("a2", "q2"): (2, 0, 0),
        ("r1", "q1"): e0,
        ("r2", "q2"): e1,
        ("r1", "p0"): e2,
        ("r1", "p1"): e1,
        ("r1", "p2"): e2,
        ("r2", "p1"): e2,
        ("r2", "p2"): e0,
    }
    assert len(cells) == 18
    assert tuple(Counter(row for row, _ in cells)[row] for row in modes) == (
        3,
        4,
        4,
        4,
        3,
    )
    assert tuple(Counter(column for _, column in cells)[column] for column in sources) == (
        4,
        4,
        4,
        3,
        3,
    )

    pure = (
        {("r1", "q1"), ("a2", "q2"), ("a0", "p0"), ("a1", "p1"), ("r2", "p2")},
        {("a1", "q1"), ("r2", "q2"), ("a0", "p0"), ("a2", "p2"), ("r1", "p1")},
        {("a2", "q1"), ("a1", "q2"), ("a0", "p0"), ("r1", "p2"), ("r2", "p1")},
    )
    for color, matching in enumerate(pure):
        assert {row for row, _ in matching} == set(modes)
        assert {column for _, column in matching} == set(sources)
        assert all(cells[edge][color] for edge in matching)
    assert (4, 2, -1) == (
        2 * (cells[("a0", "p0")][0] + cells[("a0", "p1")][0]),
        cells[("a0", "p0")][1] + cells[("a0", "p2")][1],
        cells[("a0", "p0")][2] + cells[("a0", "p2")][2],
    )

    f_matching = {
        ("a0", "p0"),
        ("a1", "p1"),
        ("a2", "p2"),
        ("r1", "q1"),
        ("r2", "q2"),
    }
    word = {"a0": 2, "a1": 0, "a2": 1, "r1": 0, "r2": 1}
    eligible = {edge for edge, vector in cells.items() if vector[word[edge[0]]]}
    assert len(eligible) == 9
    assert eligible - {edge for edge in eligible if edge[0].startswith("a")} == {
        ("r1", "q1"),
        ("r2", "q2"),
    }
    assert sum(cells[("a0", source)][2] for source in ("p0", "p1", "p2")) == 0

    # Rebuild the alternating digraph independently.
    source_owner = {source: row for row, source in f_matching}
    adjacency = defaultdict(set)
    for row in modes:
        adjacency[row]
    for edge in cells:
        if edge not in f_matching:
            row, source = edge
            adjacency[row].add(source_owner[source])
    assert all(reaches_all(adjacency, row, modes) for row in modes)

    def color(vector):
        support = [index for index, value in enumerate(vector) if value]
        return support[0] if len(support) == 1 else None

    aq = Counter(
        color(vector)
        for (row, source), vector in cells.items()
        if row.startswith("a") and source.startswith("q")
    )
    rp = Counter(
        color(vector)
        for (row, source), vector in cells.items()
        if row.startswith("r") and source.startswith("p")
    )
    assert aq == Counter({0: 1, 1: 1, 2: 2})
    assert rp == Counter({0: 1, 1: 1, 2: 3})
    assert rp - aq == Counter({2: 1})

    # Independent transverse response calculation, using exit columns p0,p2.
    entrance_marks = {"a1": (0, 1, 1), "a2": (1, 0, 1)}
    exit_marks = {"r1": e2, "r2": e0}
    y = tuple(
        tuple(dot(cells[(row, source)], entrance_marks[row]) for source in ("q1", "q2"))
        for row in ("a1", "a2")
    )
    z = tuple(
        tuple(dot(cells.get((row, source), (0, 0, 0)), exit_marks[row]) for source in ("p0", "p2"))
        for row in ("r1", "r2")
    )
    assert y == ((1, 1), (1, 2))
    assert z == ((1, 1), (0, 1))
    omega = tuple(
        tuple(sum(y[i][k] * z[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )
    assert omega == ((1, 2), (1, 3))
    assert omega[0][0] * omega[1][1] - omega[0][1] * omega[1][0] == 1

    residue = tuple(
        sum(cells[("a0", source)][color_index] for source in ("p0", "p1", "p2"))
        for color_index in range(3)
    )
    assert residue == (3, 4, 0)

    # Any two-row by two-column one-channel response is an outer product.
    y0, y1, z0, z1 = 2, 5, 7, 11
    omega_one = ((y0 * z0, y0 * z1), (y1 * z0, y1 * z1))
    assert omega_one[0][0] * omega_one[1][1] == omega_one[0][1] * omega_one[1][0]

    print("independent no-import marked-response boundary audit: PASS")
    print("tight aligned support does not force transverse toric holonomy")


if __name__ == "__main__":
    main()
