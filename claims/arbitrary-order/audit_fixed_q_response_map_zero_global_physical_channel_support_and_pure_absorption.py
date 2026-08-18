"""Independent stdlib audit of the post-GLD19 global support theorem."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
EDGE_NUMBER = {edge: number for number, edge in enumerate(EDGES)}
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
ZERO = Fraction(0)


def pairing(left, right):
    return Fraction(left[0]) * Fraction(right[1]) + Fraction(left[1]) * Fraction(
        right[0]
    )


def connected(edge_set):
    if not edge_set:
        return False
    seen = {next(iter(edge_set))[0]}
    changed = True
    while changed:
        changed = False
        for u, v in edge_set:
            if u in seen and v not in seen:
                seen.add(v)
                changed = True
            if v in seen and u not in seen:
                seen.add(u)
                changed = True
    return len(seen) == 4


def path_four(edge_set):
    degrees = sorted(sum(port in edge for edge in edge_set) for port in PORTS)
    return len(edge_set) == 3 and degrees == [1, 1, 2, 2] and connected(edge_set)


def vertices(mask):
    return frozenset(port for port in PORTS if mask & (1 << port))


def clique(vertex_set):
    return frozenset(combinations(sorted(vertex_set), 2))


def channel_atlas():
    answer = {(0,) * len(EDGES)}
    for color in COLORS:
        for graph_mask in range(1, 1 << len(EDGES)):
            graph = frozenset(
                edge for number, edge in enumerate(EDGES) if graph_mask & (1 << number)
            )
            if path_four(graph):
                continue
            answer.add(tuple((1 << color) if edge in graph else 0 for edge in EDGES))
    nontrivial_vertex_sets = tuple(
        vertices(mask) for mask in range(16) if mask.bit_count() >= 2
    )
    for colors in combinations(COLORS, 2):
        for first_set, second_set in product(nontrivial_vertex_sets, repeat=2):
            first_clique = clique(first_set)
            second_clique = clique(second_set)
            answer.add(
                tuple(
                    ((1 << colors[0]) if edge in first_clique else 0)
                    | ((1 << colors[1]) if edge in second_clique else 0)
                    for edge in EDGES
                )
            )
    return answer


def shores_to_support(shores):
    answer = []
    for u, v in EDGES:
        mask = 0
        for color in COLORS:
            if pairing(shores.get((u, color), (0, 0)), shores.get((v, color), (0, 0))):
                mask |= 1 << color
        for first, second in product(COLORS, repeat=2):
            if first != second:
                assert not pairing(
                    shores.get((u, first), (0, 0)),
                    shores.get((v, second), (0, 0)),
                )
        answer.append(mask)
    return tuple(answer)


def audit_channel_atlas():
    atlas = channel_atlas()
    assert len(atlas) == 517
    assert Counter(
        (
            atlas_item[0]
            | atlas_item[1]
            | atlas_item[2]
            | atlas_item[3]
            | atlas_item[4]
            | atlas_item[5]
        ).bit_count()
        for atlas_item in atlas
    ) == Counter({0: 1, 1: 153, 2: 363})

    # Independently recover every allowed labelled one-colour graph from a
    # small rational shore alphabet.
    alphabet = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1))
    realized = set()
    for assignment in product(alphabet, repeat=4):
        realized.add(
            frozenset(
                edge
                for edge in EDGES
                if pairing(assignment[edge[0]], assignment[edge[1]])
            )
        )
    allowed = set()
    for graph_mask in range(64):
        graph = frozenset(
            edge for number, edge in enumerate(EDGES) if graph_mask & (1 << number)
        )
        if not path_four(graph):
            allowed.add(graph)
    assert realized == allowed

    p, r = (1, 1), (1, -1)
    vertex_sets = tuple(vertices(mask) for mask in range(16) if mask.bit_count() >= 2)
    for first_set, second_set in product(vertex_sets, repeat=2):
        shores = {(port, 0): p for port in first_set}
        shores.update({(port, 2): r for port in second_set})
        expected = tuple(
            ((1 << 0) if edge in clique(first_set) else 0)
            | ((1 << 2) if edge in clique(second_set) else 0)
            for edge in EDGES
        )
        assert shores_to_support(shores) == expected
    return atlas


def allowed_pair(be, bf, ke, kf):
    if be and bf:
        singleton = be.bit_count() == 1 and be == bf
        return singleton and ke | be == be and kf | be == be
    if be:
        return kf == 0 if be.bit_count() > 1 else kf | be == be
    if bf:
        return ke == 0 if bf.bit_count() > 1 else ke | bf == bf
    return True


def family_shape(mask):
    chosen = tuple(edge for number, edge in enumerate(EDGES) if mask & (1 << number))
    if len(chosen) == 0:
        return "empty"
    if len(chosen) == 1:
        return "single"
    if len(chosen) == 2:
        assert set(chosen[0]) & set(chosen[1])
        return "adjacent"
    degrees = sorted(sum(port in edge for edge in chosen) for port in PORTS)
    if degrees == [1, 1, 1, 3]:
        return "star"
    assert degrees == [0, 2, 2, 2]
    return "triangle"


def audit_raw_ledger(atlas):
    counts = Counter()
    for channel in atlas:
        union = 0
        for edge_mask in channel:
            union |= edge_mask
        local_choices = []
        for edge, opposite in MATCHINGS:
            edge_number = EDGE_NUMBER[edge]
            opposite_number = EDGE_NUMBER[opposite]
            choices = []
            for be, bf in product(range(8), repeat=2):
                if not allowed_pair(
                    be, bf, channel[edge_number], channel[opposite_number]
                ):
                    continue
                family = 0
                if be | channel[edge_number] == 7:
                    family |= 1 << edge_number
                if bf | channel[opposite_number] == 7:
                    family |= 1 << opposite_number
                assert family.bit_count() < 2
                choices.append(family)
            local_choices.append(tuple(choices))
        for first, second, third in product(*local_choices):
            family = first | second | third
            counts[(union.bit_count(), family_shape(family))] += 1

    expected_rows = (
        (0, 4096, 1536, 192, 4, 4),
        (1, 109248, 58464, 10512, 312, 312),
        (2, 141651, 110736, 27864, 432, 2352),
    )
    shapes = ("empty", "single", "adjacent", "star", "triangle")
    for colors, *values in expected_rows:
        assert tuple(counts[(colors, shape)] for shape in shapes) == tuple(values)
    assert sum(counts.values()) == 467715
    assert sum(counts[(colors, "empty")] for colors in COLORS) == 254995


def diagonal(values):
    data = [ZERO] * 9
    for color, value in enumerate(values):
        data[3 * color + color] = Fraction(value)
    return tuple(data)


def entry(matrix, row, column):
    return matrix[3 * row + column]


def physical_channel(shores):
    answer = {}
    for u, v in EDGES:
        answer[(u, v)] = tuple(
            pairing(shores.get((u, row), (0, 0)), shores.get((v, column), (0, 0)))
            for row in COLORS
            for column in COLORS
        )
    return answer


def empty_blocks():
    return {edge: diagonal((0, 0, 0)) for edge in EDGES}


def pair_value(blocks, edge, word):
    return entry(blocks[edge], word[edge[0]], word[edge[1]])


def m4(blocks, word):
    return sum(
        pair_value(blocks, e, word) * pair_value(blocks, f, word) for e, f in MATCHINGS
    )


def x4(direct, channel, word):
    return sum(
        pair_value(direct, e, word) * pair_value(channel, f, word)
        + pair_value(channel, e, word) * pair_value(direct, f, word)
        for e, f in MATCHINGS
    )


def assert_zero_maps(direct, channel):
    for matrix in tuple(direct.values()) + tuple(channel.values()):
        assert all(
            not entry(matrix, row, column)
            for row, column in product(COLORS, repeat=2)
            if row != column
        )
    for word in product(COLORS, repeat=4):
        if len(set(word)) > 1:
            assert m4(direct, word) == 0
            assert x4(direct, channel, word) == 0


def full_family(direct, channel):
    answer = set()
    for edge in EDGES:
        support = {
            color
            for color in COLORS
            if entry(direct[edge], color, color) or entry(channel[edge], color, color)
        }
        if support == set(COLORS):
            answer.add(edge)
    return frozenset(answer)


def audit_controls():
    identity = diagonal((1, 1, 1))
    zero = diagonal((0, 0, 0))
    for family in (
        {(0, 1), (0, 2), (0, 3)},
        {(0, 1), (0, 2), (1, 2)},
    ):
        direct = {edge: identity if edge in family else zero for edge in EDGES}
        channel = empty_blocks()
        assert_zero_maps(direct, channel)
        assert full_family(direct, channel) == family

    direct = empty_blocks()
    for color, matching in enumerate(MATCHINGS):
        for edge in matching:
            direct[edge] = diagonal(tuple(int(value == color) for value in COLORS))
    assert_zero_maps(direct, empty_blocks())
    assert tuple(m4(direct, (color,) * 4) for color in COLORS) == (1, 1, 1)
    assert not full_family(direct, empty_blocks())

    dense_shores = {(port, 0): (1, 1) for port in PORTS} | {
        (port, 1): (1, -1) for port in PORTS
    }
    dense = physical_channel(dense_shores)
    assert all(matrix == diagonal((2, -2, 0)) for matrix in dense.values())
    assert_zero_maps(empty_blocks(), dense)

    triangle = {(0, 1), (0, 2), (1, 2)}
    triangle_shores = {(port, 0): (1, 1) for port in (0, 1, 2)} | {
        (port, 1): (1, -1) for port in (0, 1, 2)
    }
    triangle_channel = physical_channel(triangle_shores)
    triangle_direct = {
        edge: diagonal((0, 0, 1)) if edge in triangle else zero for edge in EDGES
    }
    assert_zero_maps(triangle_direct, triangle_channel)
    assert full_family(triangle_direct, triangle_channel) == triangle

    star = {(0, 1), (0, 2), (0, 3)}
    star_shores = {
        (0, 0): (1, 1),
        (1, 0): (1, 1),
        (0, 1): (1, -1),
        (2, 1): (1, -1),
    }
    star_channel = physical_channel(star_shores)
    star_direct = empty_blocks()
    star_direct[(0, 1)] = diagonal((0, 1, 1))
    star_direct[(0, 2)] = diagonal((1, 0, 1))
    star_direct[(0, 3)] = identity
    assert_zero_maps(star_direct, star_channel)
    assert full_family(star_direct, star_channel) == star

    formal_path = {(0, 1), (1, 2), (2, 3)}
    assert path_four(frozenset(formal_path))
    formal_channel = {
        edge: diagonal((int(edge in formal_path), 0, 0)) for edge in EDGES
    }
    assert_zero_maps(empty_blocks(), formal_channel)


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
    return pivot_row


def audit_pure_absorption():
    # Nonzero contraction coefficients times three independent port words.
    coefficient_rows = ((2, 0, 0), (0, 3, 0), (0, 0, 5))
    assert rational_rank(coefficient_rows) == 3
    assert rational_rank(coefficient_rows + ((0, 0, 0),)) == 3


def main():
    atlas = audit_channel_atlas()
    audit_raw_ledger(atlas)
    audit_controls()
    audit_pure_absorption()
    print("response-map-zero global physical support independent audit: PASS")


if __name__ == "__main__":
    main()
