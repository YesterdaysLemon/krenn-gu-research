"""Primary exact replay for the post-GLD19 global support theorem."""

from collections import Counter
from itertools import combinations, product

import sympy as sp


PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def q(left: tuple[int, int], right: tuple[int, int]) -> int:
    return left[0] * right[1] + left[1] * right[0]


def is_p4(edge_set: frozenset[tuple[int, int]]) -> bool:
    if len(edge_set) != 3:
        return False
    degrees = [sum(port in edge for edge in edge_set) for port in PORTS]
    if sorted(degrees) != [1, 1, 2, 2]:
        return False
    seen = {0}
    frontier = [0]
    while frontier:
        port = frontier.pop()
        for edge in edge_set:
            if port not in edge:
                continue
            other = edge[0] if edge[1] == port else edge[1]
            if other not in seen:
                seen.add(other)
                frontier.append(other)
    return len(seen) == 4


def clique_edges(vertices: frozenset[int]) -> frozenset[tuple[int, int]]:
    return frozenset(combinations(sorted(vertices), 2))


def classified_channel_supports() -> set[tuple[int, ...]]:
    supports = {(0,) * len(EDGES)}
    for color in COLORS:
        for graph_bits in range(1, 1 << len(EDGES)):
            graph = frozenset(
                edge for index, edge in enumerate(EDGES) if graph_bits & (1 << index)
            )
            if is_p4(graph):
                continue
            supports.add(tuple((1 << color) if edge in graph else 0 for edge in EDGES))
    vertex_sets = tuple(
        frozenset(port for port in PORTS if mask & (1 << port))
        for mask in range(1 << len(PORTS))
        if mask.bit_count() >= 2
    )
    for first_color, second_color in combinations(COLORS, 2):
        for first_vertices, second_vertices in product(vertex_sets, repeat=2):
            first_graph = clique_edges(first_vertices)
            second_graph = clique_edges(second_vertices)
            supports.add(
                tuple(
                    ((1 << first_color) if edge in first_graph else 0)
                    | ((1 << second_color) if edge in second_graph else 0)
                    for edge in EDGES
                )
            )
    return supports


def support_from_shores(
    shores: dict[tuple[int, int], tuple[int, int]],
) -> tuple[int, ...]:
    support = []
    for edge in EDGES:
        u, v = edge
        mask = 0
        for color in COLORS:
            if q(shores.get((u, color), (0, 0)), shores.get((v, color), (0, 0))):
                mask |= 1 << color
        for first_color, second_color in product(COLORS, repeat=2):
            if first_color == second_color:
                continue
            assert (
                q(
                    shores.get((u, first_color), (0, 0)),
                    shores.get((v, second_color), (0, 0)),
                )
                == 0
            )
        support.append(mask)
    return tuple(support)


def check_channel_atlas() -> set[tuple[int, ...]]:
    supports = classified_channel_supports()
    assert len(supports) == 1 + 3 * 51 + 3 * 11**2 == 517
    assert all(mask != 0b111 for item in supports for mask in item)
    assert all(any(item) for item in supports if item != (0,) * len(EDGES))
    assert all(
        (
            0
            if not any(item)
            else (item[0] | item[1] | item[2] | item[3] | item[4] | item[5]).bit_count()
        )
        <= 2
        for item in supports
    )

    zero, x, y, p, r = (0, 0), (1, 0), (0, 1), (1, 1), (1, -1)
    vectors = (zero, x, y, p, r)
    realized_graphs = set()
    for assignment in product(vectors, repeat=4):
        realized_graphs.add(
            frozenset(
                edge for edge in EDGES if q(assignment[edge[0]], assignment[edge[1]])
            )
        )
    expected_graphs = {
        frozenset(edge for index, edge in enumerate(EDGES) if bits & (1 << index))
        for bits in range(1 << len(EDGES))
        if not is_p4(
            frozenset(edge for index, edge in enumerate(EDGES) if bits & (1 << index))
        )
    }
    assert realized_graphs == expected_graphs
    assert (
        sum(
            is_p4(graph)
            for graph in (
                frozenset(
                    edge for index, edge in enumerate(EDGES) if bits & (1 << index)
                )
                for bits in range(1 << len(EDGES))
            )
        )
        == 12
    )

    vertex_sets = tuple(
        frozenset(port for port in PORTS if mask & (1 << port))
        for mask in range(1 << len(PORTS))
        if mask.bit_count() >= 2
    )
    for first_vertices, second_vertices in product(vertex_sets, repeat=2):
        shores = {}
        for port in first_vertices:
            shores[(port, 0)] = p
        for port in second_vertices:
            shores[(port, 1)] = r
        expected = tuple(
            ((1 << 0) if edge in clique_edges(first_vertices) else 0)
            | ((1 << 1) if edge in clique_edges(second_vertices) else 0)
            for edge in EDGES
        )
        assert support_from_shores(shores) == expected
    return supports


def valid_complementary_supports(be: int, bf: int, ke: int, kf: int) -> bool:
    if be and bf:
        return be.bit_count() == 1 and be == bf and not (ke & ~be) and not (kf & ~be)
    if be:
        return (not kf) if be.bit_count() >= 2 else not (kf & ~be)
    if bf:
        return (not ke) if bf.bit_count() >= 2 else not (ke & ~bf)
    return True


def f_shape(f_edges: int) -> str:
    selected = [edge for index, edge in enumerate(EDGES) if f_edges & (1 << index)]
    if not selected:
        return "empty"
    if len(selected) == 1:
        return "single"
    if len(selected) == 2:
        assert set(selected[0]) & set(selected[1])
        return "adjacent"
    assert len(selected) == 3
    degrees = sorted(sum(port in edge for edge in selected) for port in PORTS)
    if degrees == [1, 1, 1, 3]:
        return "star"
    assert degrees == [0, 2, 2, 2]
    return "triangle"


def check_raw_support_ledger(channel_supports: set[tuple[int, ...]]) -> None:
    table: Counter[tuple[int, str]] = Counter()
    for channel in channel_supports:
        active_colors = 0
        for mask in channel:
            active_colors |= mask
        local_distributions = []
        for edge, opposite in MATCHINGS:
            edge_number = EDGE_INDEX[edge]
            opposite_number = EDGE_INDEX[opposite]
            local = Counter()
            for be, bf in product(range(8), repeat=2):
                if not valid_complementary_supports(
                    be, bf, channel[edge_number], channel[opposite_number]
                ):
                    continue
                f_mask = 0
                if (be | channel[edge_number]) == 0b111:
                    f_mask |= 1 << edge_number
                if (bf | channel[opposite_number]) == 0b111:
                    f_mask |= 1 << opposite_number
                assert f_mask.bit_count() <= 1
                local[f_mask] += 1
            local_distributions.append(local)

        distribution = Counter({0: 1})
        for local in local_distributions:
            updated = Counter()
            for first_mask, first_count in distribution.items():
                for second_mask, second_count in local.items():
                    updated[first_mask | second_mask] += first_count * second_count
            distribution = updated
        for f_mask, count in distribution.items():
            table[(active_colors.bit_count(), f_shape(f_mask))] += count

    expected = {
        (0, "empty"): 4096,
        (0, "single"): 1536,
        (0, "adjacent"): 192,
        (0, "star"): 4,
        (0, "triangle"): 4,
        (1, "empty"): 109248,
        (1, "single"): 58464,
        (1, "adjacent"): 10512,
        (1, "star"): 312,
        (1, "triangle"): 312,
        (2, "empty"): 141651,
        (2, "single"): 110736,
        (2, "adjacent"): 27864,
        (2, "star"): 432,
        (2, "triangle"): 2352,
    }
    assert table == Counter(expected)
    assert sum(table.values()) == 467715
    assert (
        sum(count for (colors, shape), count in table.items() if shape == "empty")
        == 254995
    )

    zero_channel = (0,) * len(EDGES)
    matching_counts = []
    for edge, opposite in MATCHINGS:
        matching_counts.append(
            sum(
                valid_complementary_supports(be, bf, 0, 0)
                for be, bf in product(range(8), repeat=2)
            )
        )
    assert matching_counts == [18, 18, 18]
    assert 18**3 == 5832
    assert zero_channel in channel_supports


def diagonal(values: tuple[int, int, int]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix.diag(*values)


def zero_blocks() -> dict[tuple[int, int], sp.ImmutableMatrix]:
    return {edge: diagonal((0, 0, 0)) for edge in EDGES}


def physical_blocks(
    shores: dict[tuple[int, int], tuple[int, int]],
) -> dict[tuple[int, int], sp.ImmutableMatrix]:
    blocks = {}
    for edge in EDGES:
        u, v = edge
        blocks[edge] = sp.ImmutableMatrix(
            3,
            3,
            lambda first, second: q(
                shores.get((u, first), (0, 0)),
                shores.get((v, second), (0, 0)),
            ),
        )
    return blocks


def edge_value(blocks, edge, word):
    return blocks[edge][word[edge[0]], word[edge[1]]]


def compound(blocks, word):
    return sp.expand(
        sum(
            edge_value(blocks, e, word) * edge_value(blocks, f, word)
            for e, f in MATCHINGS
        )
    )


def cross(first, second, word):
    return sp.expand(
        sum(
            edge_value(first, e, word) * edge_value(second, f, word)
            + edge_value(second, e, word) * edge_value(first, f, word)
            for e, f in MATCHINGS
        )
    )


def assert_response_map_zero(direct, channel) -> None:
    assert all(block == sp.diag(*block.diagonal()) for block in direct.values())
    assert all(block == sp.diag(*block.diagonal()) for block in channel.values())
    for word in product(COLORS, repeat=4):
        if len(set(word)) == 1:
            continue
        assert compound(direct, word) == 0
        assert cross(direct, channel, word) == 0


def full_capable_edges(direct, channel) -> frozenset[tuple[int, int]]:
    result = set()
    for edge in EDGES:
        support = 0
        for color in COLORS:
            if direct[edge][color, color] or channel[edge][color, color]:
                support |= 1 << color
        if support == 0b111:
            result.add(edge)
    return frozenset(result)


def check_response_controls() -> None:
    identity = diagonal((1, 1, 1))
    zero = diagonal((0, 0, 0))

    for full_family in (
        {(0, 1), (0, 2), (0, 3)},
        {(0, 1), (0, 2), (1, 2)},
    ):
        direct = {edge: identity if edge in full_family else zero for edge in EDGES}
        channel = zero_blocks()
        assert_response_map_zero(direct, channel)
        assert full_capable_edges(direct, channel) == full_family

    direct = zero_blocks()
    for color, matching in enumerate(MATCHINGS):
        for edge in matching:
            direct[edge] = diagonal(tuple(int(index == color) for index in COLORS))
    assert_response_map_zero(direct, zero_blocks())
    assert full_capable_edges(direct, zero_blocks()) == frozenset()
    assert tuple(compound(direct, (color,) * 4) for color in COLORS) == (1, 1, 1)

    common_shores = {(port, 0): (1, 1) for port in PORTS} | {
        (port, 1): (1, -1) for port in PORTS
    }
    dense_channel = physical_blocks(common_shores)
    assert all(block == diagonal((2, -2, 0)) for block in dense_channel.values())
    assert_response_map_zero(zero_blocks(), dense_channel)
    assert full_capable_edges(zero_blocks(), dense_channel) == frozenset()

    triangle = {(0, 1), (0, 2), (1, 2)}
    triangle_shores = {(port, 0): (1, 1) for port in (0, 1, 2)} | {
        (port, 1): (1, -1) for port in (0, 1, 2)
    }
    triangle_channel = physical_blocks(triangle_shores)
    triangle_direct = {
        edge: diagonal((0, 0, 1)) if edge in triangle else zero for edge in EDGES
    }
    assert_response_map_zero(triangle_direct, triangle_channel)
    assert full_capable_edges(triangle_direct, triangle_channel) == triangle
    assert sorted(
        sum(bool(triangle_channel[edge][color, color]) for color in COLORS)
        for edge in triangle
    ) == [2, 2, 2]

    star = {(0, 1), (0, 2), (0, 3)}
    star_shores = {
        (0, 0): (1, 1),
        (1, 0): (1, 1),
        (0, 1): (1, -1),
        (2, 1): (1, -1),
    }
    star_channel = physical_blocks(star_shores)
    star_direct = zero_blocks()
    star_direct[(0, 1)] = diagonal((0, 1, 1))
    star_direct[(0, 2)] = diagonal((1, 0, 1))
    star_direct[(0, 3)] = identity
    assert_response_map_zero(star_direct, star_channel)
    assert full_capable_edges(star_direct, star_channel) == star
    assert sorted(
        sum(bool(star_channel[edge][color, color]) for color in COLORS) for edge in star
    ) == [0, 1, 1]

    # Edgewise diagonal/rank controls that fail the common-shore theorem.
    p4 = {(0, 1), (1, 2), (2, 3)}
    assert is_p4(frozenset(p4))
    formal_p4 = {edge: diagonal((int(edge in p4), 0, 0)) for edge in EDGES}
    assert_response_map_zero(zero_blocks(), formal_p4)
    rainbow_star = zero_blocks()
    rainbow_star[(0, 1)] = diagonal((1, 0, 0))
    rainbow_star[(0, 2)] = diagonal((0, 1, 0))
    rainbow_star[(0, 3)] = diagonal((0, 0, 1))
    assert_response_map_zero(zero_blocks(), rainbow_star)
    assert all(block.rank() <= 2 for block in rainbow_star.values())


def check_pure_absorption_linear_algebra() -> None:
    alpha = sp.diag(2, 3, 5)
    pure_classes = sp.Matrix(3, 4, sp.symbols("d0:12"))
    port_words = sp.eye(3)
    left = pure_classes.T * alpha * port_words
    equations = list(left)
    solution = sp.solve(equations, list(pure_classes), dict=True)
    assert solution == [{entry: 0 for entry in pure_classes}]


def main() -> None:
    channel_supports = check_channel_atlas()
    check_raw_support_ledger(channel_supports)
    check_response_controls()
    check_pure_absorption_linear_algebra()
    print("response-map-zero global physical support primary replay: PASS")


if __name__ == "__main__":
    main()
