"""All-row recursive-permanent replay of the GLD55 colour-exchange transfer."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V, W = sp.symbols("u v w")
OUT_STAR = ((0, 1), (0, 2), (0, 3))
IN_STAR = ((1, 0), (2, 0), (3, 0))
PARAMETER_EXCHANGE = {U: U / (U - 1), V: V / (V - 1), W: W / (W - 1)}


def swap_colour(colour):
    return 1 - colour if colour in (0, 1) else colour


def swap_word(value):
    return tuple(swap_colour(colour) for colour in value)


def p_index(which, root, colour):
    return 12 * which + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def mapped_index(index):
    if index < 24:
        block, offset = divmod(index, 12)
        root, colour = divmod(offset, 3)
        return 12 * block + 3 * root + swap_colour(colour)
    if index < 78:
        offset = index - 24
        edge, colours = divmod(offset, 9)
        left, right = divmod(colours, 3)
        return 24 + 9 * edge + 3 * swap_colour(left) + swap_colour(right)
    return 78 + swap_colour(index - 78)


def coordinate_sign(index):
    return -1 if index < 12 or 24 <= index < 78 else 1


def cross_value(colour, root, port, support):
    if root == port:
        return sp.Integer(1)
    for edge, value in zip(support, (U, V, W), strict=True):
        if colour == 0 and (root, port) == edge:
            return value
        if colour == 1 and (port, root) == edge:
            return value / (value - 1)
    return sp.Integer(0)


def permanent(rows, ports, root_word, port_word, support):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        entry = cross_value(port_word[port], first, port, support)
        if entry:
            total += entry * permanent(
                rows[1:], ports[:index] + ports[index + 1 :],
                root_word, port_word, support,
            )
    return sp.expand(total)


def add_entry(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
    else:
        row.pop(index, None)


def equation(port_word, root_word, support):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word, support)
    for omitted_port in ROOTS:
        ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(roots, ports, root_word, port_word, support)
            colour = port_word[omitted_port]
            add_entry(row, p_index(0, missing_root, root_word[missing_root]), y[colour] * minor)
            add_entry(row, p_index(1, missing_root, root_word[missing_root]), x[colour] * minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc] * y[rc] + y[lc] * x[rc]
        ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(roots, ports, root_word, port_word, support)
            add_entry(row, w_index(left_root, right_root, root_word[left_root], root_word[right_root]), corrected * minor)
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def main():
    for value in (U, V, W):
        exchanged = value / (value - 1)
        assert sp.cancel(exchanged / (exchanged - 1) - value) == 0
    assert len({mapped_index(index) for index in range(81)}) == 81
    assert all(mapped_index(mapped_index(index)) == index for index in range(81))

    words = tuple(product(range(3), repeat=4))
    for port_word, root_word in product(words, repeat=2):
        out_row, out_rhs = equation(port_word, root_word, OUT_STAR)
        in_row, in_rhs = equation(swap_word(port_word), swap_word(root_word), IN_STAR)
        in_row = {
            index: sp.cancel(value.xreplace(PARAMETER_EXCHANGE))
            for index, value in in_row.items()
        }
        in_rhs = sp.cancel(in_rhs.xreplace(PARAMETER_EXCHANGE))
        assert sp.cancel(in_rhs - out_rhs) == 0, (port_word, root_word, "rhs")
        for index in range(81):
            actual = in_row.get(mapped_index(index), 0)
            expected = coordinate_sign(index) * out_row.get(index, 0)
            assert sp.cancel(actual - expected) == 0, (port_word, root_word, index)
    print("PASS: all 6561 complete rows obey the GLD55 in-star/out-star covariance")


if __name__ == "__main__":
    main()
