"""Focused exact checks for cross parity and the rigid-head Wick tower.

The arbitrary-order proofs are written in the owning theorem note.  This
script checks bounded endpoint, matching-partition, and sparse-family
conventions only; it does not search graph families or prove exhaustiveness.
"""

from __future__ import annotations

from itertools import combinations, permutations

Edge = tuple[int, int]
Unit = tuple[int, int, int]


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def oriented_unit(edges: dict[Edge, Unit], u: int, v: int) -> Unit:
    a, b, weight = edges[edge(u, v)]
    return (a, b, weight) if u < v else (b, a, weight)


def perfect_matchings(vertices: tuple[int, ...], edges: dict[Edge, Unit]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        key = edge(u, v)
        if key not in edges:
            continue
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest, edges):
            yield (key,) + tail


def matching_term(matching: tuple[Edge, ...], edges: dict[Edge, Unit], n: int):
    word = [-1] * n
    weight = 1
    for u, v in matching:
        a, b, value = edges[(u, v)]
        word[u], word[v] = a, b
        weight *= value
    return tuple(word), weight


def tensor(edges: dict[Edge, Unit], vertices: tuple[int, ...]):
    order = tuple(sorted(vertices))
    position = {vertex: index for index, vertex in enumerate(order)}
    result: dict[tuple[int, ...], int] = {}
    for matching in perfect_matchings(order, edges):
        word = [-1] * len(order)
        weight = 1
        for u, v in matching:
            a, b, value = edges[(u, v)]
            word[position[u]], word[position[v]] = a, b
            weight *= value
        key = tuple(word)
        result[key] = result.get(key, 0) + weight
    return {word: value for word, value in result.items() if value}


def haf_colour(
    edges: dict[Edge, Unit], vertices: tuple[int, ...], colour: int
) -> int:
    if not vertices:
        return 1
    u = vertices[0]
    total = 0
    for index in range(1, len(vertices)):
        v = vertices[index]
        key = edge(u, v)
        if key not in edges:
            continue
        a, b, weight = oriented_unit(edges, u, v)
        if a != colour or b != colour:
            continue
        rest = vertices[1:index] + vertices[index + 1 :]
        total += weight * haf_colour(edges, rest, colour)
    return total


def direct_word_coefficient(
    edges: dict[Edge, Unit], assignment: dict[int, int], n: int
) -> int:
    total = 0
    for matching in perfect_matchings(tuple(range(n)), edges):
        word, weight = matching_term(matching, edges, n)
        if all(word[v] == assignment[v] for v in range(n)):
            total += weight
    return total


def check_cross_parity() -> None:
    n = 8
    edges: dict[Edge, Unit] = {}
    for u in range(n):
        for v in range(u + 1, n):
            edges[(u, v)] = ((u + 2 * v) % 3, (2 * u + v + 1) % 3, (-1) ** (u + v))

    for colour in range(3):
        tails = {
            u
            for u in range(n)
            if any(
                oriented_unit(edges, u, v)[0] != colour
                and oriented_unit(edges, u, v)[1] == colour
                for v in range(n)
                if v != u
            )
        }
        for matching in perfect_matchings(tuple(range(n)), edges):
            word, _ = matching_term(matching, edges, n)
            cross = []
            cross_tails = []
            for u, v in matching:
                a, b, _ = edges[(u, v)]
                if (a == colour) != (b == colour):
                    cross.append((u, v))
                    cross_tails.append(v if a == colour else u)
            assert len(cross) <= len(tails)
            assert len(cross_tails) == len(set(cross_tails))
            assert set(cross_tails) <= tails
            assert word.count(colour) % 2 == len(cross) % 2


def rigid_fixture() -> tuple[dict[Edge, Unit], set[int], set[int]]:
    n = 8
    shore = {0, 1, 2}
    rigid = set(range(3, n))
    edges: dict[Edge, Unit] = {}
    for u in range(n):
        for v in range(u + 1, n):
            if u in shore and v in rigid:
                edges[(u, v)] = (1, 0, 1 + ((u + v) % 3))
            elif u in rigid and v in rigid:
                colour = 0 if (u + v) % 2 else 1
                edges[(u, v)] = (colour, colour, 1 + ((u * v) % 2))
            else:
                edges[(u, v)] = (1, 1, 1 + ((u + v) % 2))
    return edges, shore, rigid


def injection_rhs(
    edges: dict[Edge, Unit],
    shore: set[int],
    rigid: set[int],
    heads: set[int],
    c: int,
    d: int,
) -> int:
    total = 0
    ordered_heads = tuple(sorted(heads))
    for size in range(len(ordered_heads) + 1):
        for exposed in combinations(ordered_heads, size):
            exposed_set = set(exposed)
            internal = tuple(sorted(heads - exposed_set))
            if len(internal) % 2:
                continue
            zc = haf_colour(edges, internal, c)
            if not zc:
                continue
            for images in permutations(sorted(shore), size):
                flag_product = 1
                for r, s in zip(exposed, images, strict=True):
                    a, b, weight = oriented_unit(edges, s, r)
                    if a != d or b != c:
                        flag_product = 0
                        break
                    flag_product *= weight
                if not flag_product:
                    continue
                residue = tuple(sorted(set(range(8)) - heads - set(images)))
                total += zc * flag_product * haf_colour(edges, residue, d)
    return total


def check_rigid_head_tower() -> None:
    edges, shore, rigid = rigid_fixture()
    for size in range(1, len(rigid) + 1):
        for heads_tuple in combinations(sorted(rigid), size):
            heads = set(heads_tuple)
            assignment = {v: (0 if v in heads else 1) for v in range(8)}
            direct = direct_word_coefficient(edges, assignment, 8)
            assert direct == injection_rhs(edges, shore, rigid, heads, 0, 1)

    # Anchored cut factorization: c on S union T, d on R-T.
    for size in range(len(rigid)):
        for chosen in combinations(sorted(rigid), size):
            left = shore | set(chosen)
            right = rigid - set(chosen)
            assignment = {v: (0 if v in left else 1) for v in range(8)}
            direct = direct_word_coefficient(edges, assignment, 8)
            product = haf_colour(edges, tuple(sorted(left)), 0) * haf_colour(
                edges, tuple(sorted(right)), 1
            )
            assert direct == product


def check_killer_planes_and_bridges() -> None:
    c, killer_p, killer_q = 0, 1, 2
    for a in range(3):
        for b in range(3):
            survives = a != killer_p and b != killer_q
            coordinate_bridge = survives and a == c and b == c
            assert coordinate_bridge == ((a, b) == (c, c))

    square_original = (0, 1, 0, 1)
    square_promoted = (1, 0, 1, 0)
    assert sorted(square_original) == sorted(square_promoted)

    hex_original = (0, 1, 0, 2, 1, 2)
    hex_promoted = (1, 2, 0, 2, 0, 1)
    assert sorted(hex_original) == sorted(hex_promoted) == [0, 0, 1, 1, 2, 2]


def shift_edges(m: int, include_chord: bool = True) -> dict[Edge, Unit]:
    edges: dict[Edge, Unit] = {}
    for colour in range(3):
        for i in range(m):
            u, v = i, m + ((i + colour) % m)
            edges[edge(u, v)] = (colour, colour, 1)
    if include_chord:
        edges[(0, 1)] = (1, 0, 7)
    return edges


def check_sparse_shifts() -> None:
    for m in (3, 5, 7):
        n = 2 * m
        with_chord = shift_edges(m, True)
        without_chord = shift_edges(m, False)
        assert tensor(with_chord, tuple(range(n))) == tensor(without_chord, tuple(range(n)))

        for a, b in combinations(range(3), 2):
            pair_edges = {
                key: unit
                for key, unit in without_chord.items()
                if unit[0] == unit[1] and unit[0] in {a, b}
            }
            pair_tensor = tensor(pair_edges, tuple(range(n)))
            assert pair_tensor == {(a,) * n: 1, (b,) * n: 1}

        mixed = [(0, m)]
        mixed.extend((i, m + i + 1) for i in range(1, m - 1))
        mixed.append((m - 1, m + 1))
        assert len({vertex for pair in mixed for vertex in pair}) == n
        word, weight = matching_term(tuple(edge(*pair) for pair in mixed), without_chord, n)
        assert weight == 1 and len(set(word)) == 3

        tails = {0: set(), 1: set(), 2: set()}
        for u, v in with_chord:
            a, b, _ = with_chord[(u, v)]
            if a != b:
                tails[b].add(u)
                tails[a].add(v)
        assert tails == {0: {0}, 1: {1}, 2: set()}


def main() -> None:
    check_cross_parity()
    check_rigid_head_tower()
    check_killer_planes_and_bridges()
    check_sparse_shifts()
    print("matrix-unit cross-parity and rigid-head Wick checks: PASS")
    print("scope: bounded convention checks; arbitrary-order proof is written")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
