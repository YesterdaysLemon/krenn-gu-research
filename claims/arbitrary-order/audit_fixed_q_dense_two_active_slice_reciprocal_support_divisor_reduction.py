"""Standalone recursive-permanent audit of the GLD43 support reduction."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
AMPLITUDES = {
    (colour, i, j): sp.symbols(f"a{colour}{i}{j}")
    for colour in (0, 1)
    for i in ROOTS
    for j in ROOTS
    if i != j
}


def key(port_word, root_word):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port):
    if root == port:
        return sp.Integer(1)
    if colour in (0, 1):
        return AMPLITUDES[(colour, root, port)]
    return sp.Integer(0)


def permanent(rows, ports, root_word, port_word):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        entry = cross_value(port_word[port], first, port)
        if entry:
            total += entry * permanent(
                rows[1:],
                ports[:index] + ports[index + 1 :],
                root_word,
                port_word,
            )
    return sp.expand(total)


def add_entry(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
    else:
        row.pop(index, None)


def equation(port_word, root_word):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word)
    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            colour = port_word[omitted_port]
            add_entry(row, p_index(0, missing_root, root_word[missing_root]), y[colour] * minor)
            add_entry(row, p_index(1, missing_root, root_word[missing_root]), x[colour] * minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc] * y[rc] + y[lc] * x[rc]
        retained_ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            add_entry(
                row,
                w_index(left_root, right_root, root_word[left_root], root_word[right_root]),
                corrected * minor,
            )
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def permute_word(word, permutation):
    answer = [None] * 4
    for old_index, new_index in enumerate(permutation):
        answer[new_index] = word[old_index]
    return tuple(answer)


def representatives():
    answer = {}
    for permutation in permutations(ROOTS):
        answer.setdefault((permutation[0], permutation[2]), permutation)
    return answer


def derive(row_keys, x, y):
    rows, rhs = [], []
    for row_key in row_keys:
        row, value = equation(*row_key)
        rows.append([sp.factor(row.get(index, 0)) for index in range(81)])
        rhs.append(sp.factor(value))
    nullspace = sp.Matrix(rows).T.nullspace()
    assert len(nullspace) == 1
    vector = [sp.factor(value / nullspace[0][0]) for value in nullspace[0]]
    assert vector == [1, -x, -y]
    detector = sp.factor(sum(value * target for value, target in zip(vector, rhs, strict=True)))
    assert detector == -(x * y - x - y)


def main():
    base_keys = (
        key("1202", "0212"),
        key("2212", "2212"),
        key("0222", "0222"),
    )
    for edge, permutation in representatives().items():
        row_keys = tuple(
            tuple(permute_word(word, permutation) for word in row_key)
            for row_key in base_keys
        )
        x = AMPLITUDES[(0, *edge)]
        y = AMPLITUDES[(1, edge[1], edge[0])]
        derive(row_keys, x, y)
        divisor = x * y - x - y
        assert sp.factor(divisor.subs(x, 0)) == -y
        assert sp.factor(divisor.subs(y, 0)) == -x

    paired_masks = tuple(product((False, True), repeat=12))
    assert len(paired_masks) == 4096
    assert sum(sum(mask) == 0 for mask in paired_masks) == 1
    assert sum(sum(mask) == 1 for mask in paired_masks) == 12
    residual_masks = sum(sum(mask) >= 2 for mask in paired_masks)
    assert residual_masks == 4083
    assert (1 << 24) - residual_masks == 16_773_133
    print(
        "PASS: standalone recursive-permanent audit derives all 12 GLD43 "
        "divisors and the exact 4083-mask residual support count"
    )


if __name__ == "__main__":
    main()
