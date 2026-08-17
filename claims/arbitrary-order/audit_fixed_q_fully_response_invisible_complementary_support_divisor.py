"""Independent stdlib audit for the response-map-zero support theorem."""

from fractions import Fraction
from itertools import combinations, product


COLORS = tuple(range(3))
VERTICES = tuple(range(4))
EDGES = tuple(combinations(VERTICES, 2))
SIGMA = (1, 2, 0)
ZERO = Fraction(0)
ONE = Fraction(1)


def canonical_edge(u, v):
    return (u, v) if u < v else (v, u)


def zero_matrix():
    return tuple(ZERO for _ in range(9))


def diagonal_matrix(values):
    data = [ZERO] * 9
    for color, value in enumerate(values):
        data[3 * color + color] = Fraction(value)
    return tuple(data)


def matrix_entry(matrix, row, column):
    return matrix[3 * row + column]


def matrix_add(first, second):
    return tuple(a + b for a, b in zip(first, second, strict=True))


def outer(first, second):
    return tuple(
        Fraction(first[i]) * Fraction(second[j]) for i in COLORS for j in COLORS
    )


def physical_block(x_u, y_u, x_v, y_v):
    return matrix_add(outer(x_u, y_v), outer(y_u, x_v))


def pairings(vertices):
    """Independent deletion recursion for perfect matchings."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in pairings(remainder):
            yield ((canonical_edge(first, second)),) + tail


PAIRINGS = tuple(pairings(VERTICES))
assert len(PAIRINGS) == 3


def pair_value(blocks, edge, word):
    u, v = edge
    return matrix_entry(blocks[edge], word[u], word[v])


def m4_value(direct, word):
    total = ZERO
    for matching in PAIRINGS:
        value = ONE
        for edge in matching:
            value *= pair_value(direct, edge, word)
        total += value
    return total


def x4_value(direct, channel, word):
    total = ZERO
    for matching in PAIRINGS:
        first, second = matching
        total += pair_value(direct, first, word) * pair_value(channel, second, word)
        total += pair_value(channel, first, word) * pair_value(direct, second, word)
    return total


def z4_value(direct, channel, word, h=ZERO):
    return h * m4_value(direct, word) + x4_value(direct, channel, word)


def word_on(edge, first_color, second_color):
    result = [None] * 4
    for vertex in edge:
        result[vertex] = first_color
    for vertex in set(VERTICES) - set(edge):
        result[vertex] = second_color
    return tuple(result)


def blocks_from_diagonals(diagonals):
    return {edge: diagonal_matrix(diagonals.get(edge, (0, 0, 0))) for edge in EDGES}


def check_unique_matching_rows():
    edge = (0, 1)
    opposite = (2, 3)
    for values in (
        ((2, 3, 5), (7, 11, 13), (17, 19, 23), (29, 31, 37)),
        ((1, 0, -2), (0, 3, 0), (5, 0, 7), (0, -11, 13)),
    ):
        be, bf, ke, kf = (tuple(map(Fraction, row)) for row in values)
        direct = blocks_from_diagonals({edge: be, opposite: bf})
        channel = blocks_from_diagonals({edge: ke, opposite: kf})
        h = Fraction(41, 17)
        for c in COLORS:
            for d in COLORS:
                if c == d:
                    continue
                word = word_on(edge, c, d)
                assert m4_value(direct, word) == be[c] * bf[d]
                assert z4_value(direct, channel, word, h) == (
                    h * be[c] * bf[d] + be[c] * kf[d] + ke[c] * bf[d]
                )


def mask_support(mask):
    return frozenset(c for c in COLORS if mask & (1 << c))


def row_zero_support(be, bf, ke, kf):
    for c in COLORS:
        for d in COLORS:
            if c == d:
                continue
            if c in be and d in bf:
                return False
            if c in be and d in kf:
                return False
            if c in ke and d in bf:
                return False
    return True


def expected_class(be, bf, ke, kf):
    if be and bf:
        return len(be) == 1 and be == bf and ke <= be and kf <= be
    if be:
        return (not kf) if len(be) >= 2 else kf <= be
    if bf:
        return (not ke) if len(bf) >= 2 else ke <= bf
    return True


def check_support_classification():
    b_masks = tuple(mask_support(mask) for mask in range(8))
    k_masks = tuple(mask_support(mask) for mask in range(8) if mask != 7)
    allowed = []
    for be, bf, ke, kf in product(b_masks, b_masks, k_masks, k_masks):
        row_zero = row_zero_support(be, bf, ke, kf)
        assert row_zero == expected_class(be, bf, ke, kf)
        if row_zero:
            allowed.append((be, bf, ke, kf))
            assert not (len(be | ke) == 3 and len(bf | kf) == 3)
    assert len(allowed) == 201


def five_row_values(be, bf, ke, kf, h=ZERO):
    rows = []
    for c in COLORS:
        d = SIGMA[c]
        rows.append(be[c] * bf[d])
    for c in (0, 1):
        d = SIGMA[c]
        m_value = be[c] * bf[d]
        rows.append(h * m_value + be[c] * kf[d] + ke[c] * bf[d])
    return tuple(rows)


def vector_from_mask(mask):
    return tuple(ONE if mask & (1 << c) else ZERO for c in COLORS)


def check_five_row_detector():
    singular_masks = tuple(mask for mask in range(8) if mask != 7)
    zero_five = 0
    for be_mask, bf_mask, ke_mask, kf_mask in product(
        range(8), range(8), singular_masks, singular_masks
    ):
        be = vector_from_mask(be_mask)
        bf = vector_from_mask(bf_mask)
        ke = vector_from_mask(ke_mask)
        kf = vector_from_mask(kf_mask)
        if any(five_row_values(be, bf, ke, kf)):
            continue
        zero_five += 1
        assert (be_mask | ke_mask) != 7 or (bf_mask | kf_mask) != 7
    assert zero_five > 0


def all_responses(direct, channel, h=ZERO):
    m_values = {}
    z_values = {}
    for word in product(COLORS, repeat=4):
        m_values[word] = m4_value(direct, word)
        z_values[word] = z4_value(direct, channel, word, h)
    return m_values, z_values


def check_controls():
    # Pure normalized response-map-zero fixture.
    direct_diagonals = {
        (0, 1): (1, 0, 0),
        (2, 3): (1, 0, 0),
        (0, 2): (0, 1, 0),
        (1, 3): (0, 1, 0),
        (0, 3): (0, 0, 1),
        (1, 2): (0, 0, 1),
    }
    direct = blocks_from_diagonals(direct_diagonals)
    channel = blocks_from_diagonals({})
    m_values, z_values = all_responses(direct, channel)
    assert {word: value for word, value in m_values.items() if value} == {
        (0, 0, 0, 0): ONE,
        (1, 1, 1, 1): ONE,
        (2, 2, 2, 2): ONE,
    }
    assert not any(z_values.values())

    # Raw opposite annihilation from endpoint vectors.
    x = {
        0: (1, 1, 0),
        1: (1, 1, 0),
        2: (0, 0, 0),
        3: (0, 0, 0),
    }
    y = {
        0: (1, -1, 0),
        1: (1, -1, 0),
        2: (0, 0, 0),
        3: (0, 0, 0),
    }
    channel = {
        edge: physical_block(x[edge[0]], y[edge[0]], x[edge[1]], y[edge[1]])
        for edge in EDGES
    }
    direct = blocks_from_diagonals({(0, 1): (0, 0, 1)})
    assert channel[(0, 1)] == diagonal_matrix((2, -2, 0))
    assert channel[(2, 3)] == zero_matrix()
    assert matrix_add(direct[(0, 1)], channel[(0, 1)]) == diagonal_matrix((2, -2, 1))
    m_values, z_values = all_responses(direct, channel)
    assert not any(m_values.values())
    assert not any(z_values.values())

    # M_U-purity boundary.
    direct = {edge: diagonal_matrix((1, 1, 1)) for edge in EDGES}
    channel = blocks_from_diagonals({})
    m_values, z_values = all_responses(direct, channel)
    assert m_values[(0, 0, 1, 1)] == ONE
    assert not any(z_values.values())

    # Z_U-purity boundary, derived from physical endpoint vectors again.
    common_x = (1, 1, 0)
    common_y = (1, -1, 0)
    channel = {
        edge: physical_block(common_x, common_y, common_x, common_y) for edge in EDGES
    }
    direct = blocks_from_diagonals({(0, 3): (0, 0, 1), (1, 2): (0, 0, 1)})
    m_values, z_values = all_responses(direct, channel)
    assert all(value == 0 for word, value in m_values.items() if len(set(word)) > 1)
    assert z_values[(2, 0, 0, 2)] == 2

    # Formal rank-three boundary.
    full = (ONE, ONE, ONE)
    zero = (ZERO, ZERO, ZERO)
    assert not any(five_row_values(zero, zero, full, full))

    # Independently replay the formal pure-Z-axis boundary: R(a,b)=a has
    # nonzero rank and kernel exactly K(0,1), although that selected line is
    # pure.
    response_row = (ONE, ZERO)
    pure_z_line = (ZERO, ONE)
    assert response_row != (ZERO, ZERO)
    assert sum(entry * value for entry, value in zip(response_row, pure_z_line)) == ZERO
    assert all(
        sum(entry * value for entry, value in zip(response_row, vector)) != ZERO
        for vector in ((ONE, ZERO), (ONE, ONE))
    )


def main():
    check_unique_matching_rows()
    check_support_classification()
    check_five_row_detector()
    check_controls()
    print("fully response-map-zero support independent audit: PASS")


if __name__ == "__main__":
    main()
