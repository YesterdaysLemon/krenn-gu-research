"""Primary exact replay for the post-GLD20 dead-colour companion gate."""

from itertools import combinations, product

import sympy as sp


PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
EDGE_NUMBER = {edge: number for number, edge in enumerate(EDGES)}
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
Q0, Q1 = 4, 5
OUTSIDE = PORTS + (Q0, Q1)
Q_LABEL = frozenset((Q0, Q1))


def pairing(left, right):
    return sp.expand(left[0] * right[1] + left[1] * right[0])


def clique(vertices):
    return frozenset(combinations(sorted(vertices), 2))


def targeted_channels():
    vertex_sets = tuple(
        frozenset(port for port in PORTS if mask & (1 << port))
        for mask in range(16)
        if mask.bit_count() >= 2
    )
    channels = set()
    for first, second in combinations(COLORS, 2):
        for first_vertices, second_vertices in product(vertex_sets, repeat=2):
            if len(first_vertices) < 4 and len(second_vertices) < 4:
                continue
            first_graph = clique(first_vertices)
            second_graph = clique(second_vertices)
            channels.add(
                tuple(
                    ((1 << first) if edge in first_graph else 0)
                    | ((1 << second) if edge in second_graph else 0)
                    for edge in EDGES
                )
            )
    return channels


def valid_complementary_pair(be, bf, ke, kf):
    if be and bf:
        return be.bit_count() == 1 and be == bf and not (ke & ~be) and not (kf & ~be)
    if be:
        return not kf if be.bit_count() >= 2 else not (kf & ~be)
    if bf:
        return not ke if bf.bit_count() >= 2 else not (ke & ~bf)
    return True


def active_mask(channel):
    answer = 0
    for mask in channel:
        answer |= mask
    return answer


def check_support_ledger():
    channels = targeted_channels()
    assert len(channels) == 3 * (11 + 11 - 1) == 63

    raw_count = 0
    dense_count = 0
    nondense_count = 0
    for channel in channels:
        active = active_mask(channel)
        assert active.bit_count() == 2
        missing = next(color for color in COLORS if not active & (1 << color))
        local_choices = []
        for edge, opposite in MATCHINGS:
            edge_number = EDGE_NUMBER[edge]
            opposite_number = EDGE_NUMBER[opposite]
            choices = []
            for be, bf in product(range(8), repeat=2):
                if valid_complementary_pair(
                    be,
                    bf,
                    channel[edge_number],
                    channel[opposite_number],
                ):
                    choices.append((be, bf))
            local_choices.append(tuple(choices))

        dense = all(mask == active for mask in channel)
        dominant = active if dense else channel[0]
        for mask in channel[1:]:
            dominant &= mask
        assert dominant.bit_count() == (2 if dense else 1)
        channel_count = 0
        for choices in product(*local_choices):
            direct = [0] * len(EDGES)
            for (edge, opposite), (be, bf) in zip(MATCHINGS, choices, strict=True):
                direct[EDGE_NUMBER[edge]] = be
                direct[EDGE_NUMBER[opposite]] = bf
            assert all(not (mask & (1 << missing)) for mask in direct)
            assert all(not (mask & ~dominant) for mask in direct)
            assert all((be | ke) != 0b111 for be, ke in zip(direct, channel))
            if dense:
                assert direct == [0] * len(EDGES)
            channel_count += 1

        raw_count += channel_count
        if dense:
            dense_count += channel_count
        else:
            nondense_count += channel_count

    assert dense_count == 3
    assert nondense_count == 6 * (6 * 32 + 4 * 8) == 1344
    assert raw_count == 1347
    return channels


def physical_channel(shores):
    blocks = {}
    for u, v in EDGES:
        blocks[(u, v)] = sp.ImmutableMatrix(
            3,
            3,
            lambda row, column: pairing(
                shores.get((u, row), (0, 0)),
                shores.get((v, column), (0, 0)),
            ),
        )
    return blocks


def check_physical_shores():
    p, r = (1, 1), (1, -1)
    for secondary_vertices in (
        frozenset((0, 1)),
        frozenset((0, 1, 2)),
        frozenset(PORTS),
    ):
        shores = {(port, 0): p for port in PORTS}
        shores.update({(port, 1): r for port in secondary_vertices})
        blocks = physical_channel(shores)
        for edge, block in blocks.items():
            expected_second = -2 if edge in clique(secondary_vertices) else 0
            assert block == sp.diag(2, expected_second, 0)
        assert all(shores.get((port, 2), (0, 0)) == (0, 0) for port in PORTS)


def edge_value(left, right, word, direct, shores, h):
    if {left, right} == {Q0, Q1}:
        return h
    if left in (Q0, Q1) and right in PORTS:
        return shores[(left, right, word[right])]
    if right in (Q0, Q1) and left in PORTS:
        return shores[(right, left, word[left])]
    edge = tuple(sorted((left, right)))
    if word[left] != word[right]:
        return sp.Integer(0)
    return direct[(edge, word[left])]


def hafnian(vertices, word, direct, shores, h):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return sp.Integer(1)
    first = vertices[0]
    answer = 0
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        answer += edge_value(first, second, word, direct, shores, h) * hafnian(
            remainder, word, direct, shores, h
        )
    return sp.expand(answer)


def even_labels():
    return tuple(
        frozenset(label) for size in (2, 4, 6) for label in combinations(OUTSIDE, size)
    )


def coordinate_key(label, word):
    return label, tuple((port, word[port]) for port in PORTS if port in label)


def nonzero_label_coordinates(word, direct, shores, h):
    answer = {}
    for label in even_labels():
        value = hafnian(label, word, direct, shores, h)
        if value != 0:
            answer[coordinate_key(label, word)] = value
    return answer


def symbolic_graph_data(dense=False):
    h = sp.Symbol("h", nonzero=True)
    direct = {}
    for edge in EDGES:
        for color in COLORS:
            if dense or color != 0:
                direct[(edge, color)] = sp.Integer(0)
            else:
                direct[(edge, color)] = sp.Symbol(f"b{edge[0]}{edge[1]}_{color}")
    shores = {}
    for port in PORTS:
        first_scale = sp.Symbol(f"s{port}_0")
        second_scale = sp.Symbol(f"s{port}_1")
        shores[(Q0, port, 0)] = first_scale
        shores[(Q1, port, 0)] = first_scale
        shores[(Q0, port, 1)] = second_scale
        shores[(Q1, port, 1)] = -second_scale
        shores[(Q0, port, 2)] = sp.Integer(0)
        shores[(Q1, port, 2)] = sp.Integer(0)
    return direct, shores, h


def check_dead_colour_label_ledger():
    direct, shores, h = symbolic_graph_data()
    pure_missing = {port: 2 for port in PORTS}
    pure_values = nonzero_label_coordinates(pure_missing, direct, shores, h)
    assert pure_values == {(Q_LABEL, ()): h}

    for port in PORTS:
        for active in (0, 1):
            word = {item: 2 for item in PORTS}
            word[port] = active
            values = nonzero_label_coordinates(word, direct, shores, h)
            expected = {
                (Q_LABEL, ()),
                (frozenset((Q0, port)), ((port, active),)),
                (frozenset((Q1, port)), ((port, active),)),
            }
            assert set(values) == expected

    # Outside a proper secondary clique, the secondary shore is zero.  The
    # corresponding Hamming-one word therefore leaves only the Q label.
    shores[(Q0, 3, 1)] = sp.Integer(0)
    shores[(Q1, 3, 1)] = sp.Integer(0)
    outside_word = {port: 2 for port in PORTS}
    outside_word[3] = 1
    outside_values = nonzero_label_coordinates(outside_word, direct, shores, h)
    assert outside_values == {(Q_LABEL, ()): h}


def check_dense_mixed_ledger():
    direct, shores, h = symbolic_graph_data(dense=True)
    package_count = 0
    for edge in EDGES:
        complement = tuple(port for port in PORTS if port not in edge)
        desired = frozenset((Q0, Q1, *edge))
        for repeated in (0, 1):
            other = 1 - repeated
            nuisance_coordinates = set()
            for orientation in ((other, 2), (2, other)):
                word = {edge[0]: repeated, edge[1]: repeated}
                word[complement[0]], word[complement[1]] = orientation
                values = nonzero_label_coordinates(word, direct, shores, h)
                assert coordinate_key(desired, word) in values
                nuisance_coordinates.update(key for key in values if key[0] != desired)
                active_complement = (
                    complement[0] if orientation[0] == other else complement[1]
                )
                expected_labels = {Q_LABEL, desired}
                expected_labels.update(
                    frozenset((qvertex, port))
                    for qvertex in (Q0, Q1)
                    for port in (*edge, active_complement)
                )
                assert {label for label, _ in values} == expected_labels
            assert len(nuisance_coordinates) == 9
            assert sum(key[0] == Q_LABEL for key in nuisance_coordinates) == 1
            package_count += 1
    assert package_count == 12


def check_h_gate_and_hamming_solve():
    root_words = tuple(product(COLORS, repeat=4))
    target_index = root_words.index((2, 2, 2, 2))
    alpha = sp.Rational(5)
    target = sp.zeros(len(root_words), 1)
    target[target_index] = alpha
    assert target.rank() == 1

    h = sp.Rational(2)
    companion_slice = target / h
    assert h * companion_slice == target
    assert companion_slice[target_index] == sp.Rational(5, 2)
    assert sum(value != 0 for value in companion_slice) == 1
    assert sp.zeros(len(root_words), 1) != target

    shore_matrix = sp.Matrix(((1, 1), (1, -1)))
    assert shore_matrix.det() == -2
    hamming_gu = sp.Matrix((5, 7))
    solved = -sp.Rational(3) * shore_matrix.inv() * hamming_gu
    assert shore_matrix * solved + 3 * hamming_gu == sp.zeros(2, 1)


def check_dense_absorption_rank_gate():
    nuisance = sp.zeros(162, 9)
    for index in range(9):
        nuisance[index, index] = 1
    detected = sp.zeros(162, 1)
    detected[9] = 1
    absorbed = nuisance[:, 0]
    assert nuisance.rank() == 9
    assert nuisance.row_join(detected).rank() == 10
    assert nuisance.row_join(absorbed).rank() == 9

    # Abstract one-row positive and swallowed controls for the rank semantics.
    for tau, increment in ((sp.Integer(1), 1), (sp.Integer(0), 0)):
        clean_nuisance = sp.zeros(1, 9)
        clean_desired = sp.Matrix((tau,))
        assert clean_nuisance.row_join(clean_desired).rank() == increment


def check_dense_response_window():
    shores = {(port, 0): (1, 1) for port in PORTS}
    shores.update({(port, 1): (1, -1) for port in PORTS})
    blocks = physical_channel(shores)
    assert all(block == sp.diag(2, -2, 0) for block in blocks.values())
    assert all(block.rank() == 2 for block in blocks.values())
    direct = {edge: sp.zeros(3, 3) for edge in EDGES}
    for word in product(COLORS, repeat=4):
        if len(set(word)) == 1:
            continue
        for edge, opposite in MATCHINGS:
            assert direct[edge][word[edge[0]], word[edge[1]]] == 0
            assert direct[opposite][word[opposite[0]], word[opposite[1]]] == 0


def main():
    check_support_ledger()
    check_physical_shores()
    check_dead_colour_label_ledger()
    check_dense_mixed_ledger()
    check_h_gate_and_hamming_solve()
    check_dense_absorption_rank_gate()
    check_dense_response_window()
    print("response-map-zero dead-colour companion-gate primary replay: PASS")


if __name__ == "__main__":
    main()
