"""Exact primary replay for the response-map-zero support theorem."""

from itertools import combinations, product

import sympy as sp


COLORS = range(3)
EDGES = tuple(combinations(range(4), 2))
MATCHINGS = (
    (((0, 1), (2, 3))),
    (((0, 2), (1, 3))),
    (((0, 3), (1, 2))),
)
SIGMA = {0: 1, 1: 2, 2: 0}


def edge_value(blocks, edge, word):
    """Evaluate one oriented pair block on a four-port word."""

    u, v = edge
    return blocks[edge][word[u], word[v]]


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


def diagonal_blocks(prefix):
    symbols = {}
    blocks = {}
    for edge in EDGES:
        entries = sp.symbols(
            " ".join(f"{prefix}{edge[0]}{edge[1]}_{c}" for c in COLORS)
        )
        symbols[edge] = entries
        blocks[edge] = sp.diag(*entries)
    return blocks, symbols


def word_on_partition(edge, c, d):
    word = [None] * 4
    for vertex in edge:
        word[vertex] = c
    for vertex in set(range(4)) - set(edge):
        word[vertex] = d
    return tuple(word)


def check_symbolic_response_rows():
    direct, b = diagonal_blocks("b")
    channel, k = diagonal_blocks("k")
    h = sp.symbols("h")
    edge = (0, 1)
    opposite = (2, 3)
    rows = []
    for c in COLORS:
        for d in COLORS:
            if c == d:
                continue
            word = word_on_partition(edge, c, d)
            m_value = compound(direct, word)
            z_value = sp.expand(h * m_value + cross(direct, channel, word))
            assert sp.expand(m_value - b[edge][c] * b[opposite][d]) == 0
            expected_z = (
                h * b[edge][c] * b[opposite][d]
                + b[edge][c] * k[opposite][d]
                + k[edge][c] * b[opposite][d]
            )
            assert sp.expand(z_value - expected_z) == 0
            rows.append((word, m_value, z_value))
    assert len(rows) == 6
    assert len({word for word, _, _ in rows}) == 6


def all_supports(include_full=True):
    result = []
    for mask in range(8):
        support = frozenset(c for c in COLORS if mask & (1 << c))
        if include_full or len(support) <= 2:
            result.append(support)
    return result


def rows_can_vanish(be, bf, ke, kf):
    """Exact support test after the M row rules out two-term cancellation."""

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


def classified(be, bf, ke, kf):
    if be and bf:
        return len(be) == 1 and be == bf and ke <= be and kf <= be
    if be:
        if len(be) >= 2:
            return not kf
        return kf <= be
    if bf:
        if len(bf) >= 2:
            return not ke
        return ke <= bf
    return True


def check_exhaustive_support_ledger():
    b_supports = all_supports()
    k_supports = all_supports(include_full=False)
    accepted = 0
    for be, bf, ke, kf in product(b_supports, b_supports, k_supports, k_supports):
        vanishes = rows_can_vanish(be, bf, ke, kf)
        assert vanishes == classified(be, bf, ke, kf)
        if not vanishes:
            continue
        accepted += 1
        # Every selected block is supported inside B union K.  Both unions
        # cannot contain all three colours on a vanishing-row configuration.
        assert not (len(be | ke) == 3 and len(bf | kf) == 3)
    assert len(b_supports) ** 2 * len(k_supports) ** 2 == 3136
    assert accepted == 201


def selected_diagonal(b_values, k_values, alpha, beta, h):
    return tuple((alpha + h * beta) * b_values[c] + beta * k_values[c] for c in COLORS)


def five_rows(b_e, b_f, k_e, k_f, h=sp.Integer(0)):
    m_rows = []
    z_rows = []
    for c in COLORS:
        d = SIGMA[c]
        m_value = b_e[c] * b_f[d]
        m_rows.append(sp.expand(m_value))
        if c < 2:
            z_rows.append(sp.expand(h * m_value + b_e[c] * k_f[d] + k_e[c] * b_f[d]))
    return tuple(m_rows + z_rows)


def check_five_row_binary_detector():
    """Exhaust the nonzero/zero support patterns relevant to the proof."""

    supports = all_supports()
    singular = all_supports(include_full=False)
    checked = 0
    for be, bf, ke, kf in product(supports, supports, singular, singular):
        # Use value one on every supported diagonal coordinate.  The five-row
        # theorem is support-exact because each zero M row prevents a two-term
        # cancellation in its paired Z row.
        b_e = tuple(sp.Integer(c in be) for c in COLORS)
        b_f = tuple(sp.Integer(c in bf) for c in COLORS)
        k_e = tuple(sp.Integer(c in ke) for c in COLORS)
        k_f = tuple(sp.Integer(c in kf) for c in COLORS)
        if any(five_rows(b_e, b_f, k_e, k_f)):
            continue
        checked += 1
        # If a generic selected support can be full on both sides, the union
        # supports are both full.  The theorem says this never occurs.
        assert not (len(be | ke) == 3 and len(bf | kf) == 3)
    assert checked > 0


def matrix_from_diagonal(values):
    return sp.diag(*map(sp.Integer, values))


def zero_blocks():
    return {edge: sp.zeros(3, 3) for edge in EDGES}


def all_word_coefficients(direct, channel, h=sp.Integer(0)):
    m_values = {}
    z_values = {}
    for word in product(COLORS, repeat=4):
        m_value = compound(direct, word)
        m_values[word] = m_value
        z_values[word] = sp.expand(h * m_value + cross(direct, channel, word))
    return m_values, z_values


def is_pure_word(word):
    return len(set(word)) == 1


def check_controls():
    # Pure normalized response-map-zero control on the three matchings.
    direct = zero_blocks()
    channel = zero_blocks()
    for color, (edge, opposite) in enumerate(MATCHINGS):
        direct[edge][color, color] = 1
        direct[opposite][color, color] = 1
    m_values, z_values = all_word_coefficients(direct, channel)
    assert {word: value for word, value in m_values.items() if value} == {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
    }
    assert not any(z_values.values())
    assert [
        direct[(0, 1)][0, 0] * direct[(2, 3)][0, 0],
        direct[(0, 2)][1, 1] * direct[(1, 3)][1, 1],
        direct[(0, 3)][2, 2] * direct[(1, 2)][2, 2],
    ] == [1, 1, 1]

    # The annihilation conclusion is attained physically.
    x = {
        0: sp.Matrix((1, 1, 0)),
        1: sp.Matrix((1, 1, 0)),
        2: sp.zeros(3, 1),
        3: sp.zeros(3, 1),
    }
    y = {
        0: sp.Matrix((1, -1, 0)),
        1: sp.Matrix((1, -1, 0)),
        2: sp.zeros(3, 1),
        3: sp.zeros(3, 1),
    }
    physical = {
        edge: x[edge[0]] * y[edge[1]].T + y[edge[0]] * x[edge[1]].T for edge in EDGES
    }
    direct = zero_blocks()
    direct[(0, 1)][2, 2] = 1
    assert physical[(0, 1)] == sp.diag(2, -2, 0)
    assert direct[(0, 1)] + physical[(0, 1)] == sp.diag(2, -2, 1)
    assert physical[(2, 3)] == sp.zeros(3, 3)
    m_values, z_values = all_word_coefficients(direct, physical)
    assert not any(m_values.values())
    assert not any(z_values.values())

    # Dropping M_U purity.
    direct = {edge: sp.eye(3) for edge in EDGES}
    channel = zero_blocks()
    m_values, z_values = all_word_coefficients(direct, channel)
    assert not any(z_values.values())
    assert m_values[(0, 0, 1, 1)] == 1

    # Dropping Z_U purity while retaining physical rank two and pure M_U.
    x_common = sp.Matrix((1, 1, 0))
    y_common = sp.Matrix((1, -1, 0))
    channel = {edge: x_common * y_common.T + y_common * x_common.T for edge in EDGES}
    direct = zero_blocks()
    direct[(0, 3)][2, 2] = 1
    direct[(1, 2)][2, 2] = 1
    m_values, z_values = all_word_coefficients(direct, channel)
    assert all(not value for word, value in m_values.items() if not is_pure_word(word))
    assert z_values[(2, 0, 0, 2)] == 2
    assert direct[(0, 3)] + channel[(0, 3)] == sp.diag(2, -2, 1)
    assert direct[(1, 2)] + channel[(1, 2)] == sp.diag(2, -2, 1)

    # Formal rank-three boundary.
    b_zero = (0, 0, 0)
    k_full = (1, 1, 1)
    assert not any(five_rows(b_zero, b_zero, k_full, k_full))
    assert selected_diagonal(b_zero, k_full, 0, 1, 0) == (1, 1, 1)

    # A pure selected axis need not make the realized response map zero.
    # Here R(a,b)=a, so its kernel is exactly the pure-Z line K(0,1).
    mixed_response_map = sp.Matrix([[1, 0]])
    pure_z_line = sp.Matrix([0, 1])
    assert mixed_response_map.rank() == 1
    assert mixed_response_map * pure_z_line == sp.zeros(1, 1)
    assert mixed_response_map.nullspace() == [pure_z_line]


def main():
    check_symbolic_response_rows()
    check_exhaustive_support_ledger()
    check_five_row_binary_detector()
    check_controls()
    print("fully response-map-zero support primary replay: PASS")


if __name__ == "__main__":
    main()
