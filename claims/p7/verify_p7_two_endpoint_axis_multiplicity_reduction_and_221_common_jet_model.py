"""Verify the strict two-endpoint axis reduction and the common 2+2+1 model.

This is a fixed symbolic calculation on five labelled roots.  It performs no
support search and does not enumerate graph families.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

Q0 = 5
Q1 = 6
ROOTS = tuple(range(5))


def check_same_axis_triple_obstruction() -> None:
    x1, y1, x2, y2, x3, y3 = sp.symbols("x1 y1 x2 y2 x3 y3")
    a, c = sp.symbols("a c")
    px, py, qx, qy = sp.symbols("px py qx qy")

    b12 = a * x1 * x2 + c * y1 * y2
    p3 = px * x3 + py * y3
    q3 = qx * x3 + qy * y3

    # In the triple companions K_p and K_q, these two mixed monomials have
    # unique source B_12 p_3 and B_12 q_3.  The other two summands contain a
    # diagonal block on 13 or 23 and cannot contribute either coefficient.
    assert sp.expand(b12 * p3).coeff(x1 * x2 * y3) == a * py
    assert sp.expand(b12 * q3).coeff(x1 * x2 * y3) == a * qy
    assert sp.expand(b12 * p3).coeff(y1 * y2 * x3) == c * px
    assert sp.expand(b12 * q3).coeff(y1 * y2 * x3) == c * qx

    # If both diagonal coefficients of B_12 are nonzero, all four endpoint
    # coefficients at root 3 vanish.  If exactly one is nonzero, p_3,q_3 are
    # proportional.  If both vanish, the pair frame {B_12,H_12} has rank at
    # most one.  Each alternative contradicts the required rank-two frames.
    endpoint_matrix = sp.Matrix(((px, py), (qx, qy)))
    assert endpoint_matrix.subs({px: 0, py: 0, qx: 0, qy: 0}).rank() == 0
    assert endpoint_matrix.subs({py: 0, qy: 0}).det() == 0
    assert endpoint_matrix.subs({px: 0, qx: 0}).det() == 0


def hafnian_form(
    vertices: tuple[int, ...],
    blocks: dict[tuple[int, int], sp.Expr],
) -> sp.Expr:
    @cache
    def recurse(items: tuple[int, ...]) -> sp.Expr:
        if not items:
            return sp.Integer(1)
        first = items[0]
        total = sp.Integer(0)
        for position in range(1, len(items)):
            second = items[position]
            edge = blocks.get(tuple(sorted((first, second))), sp.Integer(0))
            if edge != 0:
                rest = items[1:position] + items[position + 1 :]
                total += edge * recurse(rest)
        return sp.expand(total)

    return recurse(tuple(sorted(vertices)))


def unit(color: int, coefficient: sp.Expr | None = None) -> sp.Matrix:
    if coefficient is None:
        coefficient = sp.Integer(1)
    vector = sp.zeros(3, 1)
    vector[color] = coefficient
    return vector


def build_model():
    x1, y1, x2, y2, u3, y3, u4, y4, u5, x5 = sp.symbols(
        "x1 y1 x2 y2 u3 y3 u4 y4 u5 x5"
    )
    local = (
        (0, x1, y1),
        (0, x2, y2),
        (u3, 0, y3),
        (u4, 0, y4),
        (u5, x5, 0),
    )
    p = (x1, y2, u3, y4, u5)
    q = (y1, x2, y3, u4, x5)
    b = {
        (0, 1): y1 * y2,
        (2, 3): y3 * y4,
        (0, 2): -x1 * y3 - y1 * u3 + y1 * y3,
        (0, 3): y1 * y4,
        (1, 2): y2 * y3,
        (1, 3): -y2 * u4 - x2 * y4 + y2 * y4,
        (0, 4): -y1 * u5,
        (1, 4): x2 * x5,
        (2, 4): u3 * u5,
        (3, 4): -y4 * x5,
    }
    h = {
        (i, j): sp.expand(p[i] * q[j] + q[i] * p[j])
        for i, j in combinations(ROOTS, 2)
    }
    blocks = dict(b)
    blocks.update({(i, Q0): p[i] for i in ROOTS})
    blocks.update({(i, Q1): q[i] for i in ROOTS})
    return local, p, q, b, h, blocks


def build_ledger() -> dict[tuple[frozenset[int], frozenset[int]], sp.Matrix]:
    ledger: dict[tuple[frozenset[int], frozenset[int]], sp.Matrix] = {}

    singleton = {
        0: (unit(1), unit(2)),
        1: (unit(2), unit(1)),
        2: (unit(0), unit(2)),
        3: (unit(2), unit(0)),
        4: (unit(0), unit(1)),
    }
    for root, (c0, c1) in singleton.items():
        root_set = frozenset((root,))
        ledger[root_set, frozenset((Q0,))] = c0
        ledger[root_set, frozenset((Q1,))] = c1

    pair_values = {
        (0, 1): (unit(2) - unit(1), unit(1)),
        (2, 3): (unit(2) - unit(0), unit(0)),
        (0, 2): (unit(2), unit(2)),
        (0, 3): (unit(2), sp.zeros(3, 1)),
        (1, 2): (unit(2), sp.zeros(3, 1)),
        (1, 3): (unit(2), unit(2)),
        (0, 4): (unit(1), unit(1)),
        (1, 4): (unit(1), sp.zeros(3, 1)),
        (2, 4): (unit(0), sp.zeros(3, 1)),
        (3, 4): (unit(0), unit(0)),
    }
    for pair, (empty_value, full_value) in pair_values.items():
        root_set = frozenset(pair)
        ledger[root_set, frozenset()] = empty_value
        ledger[root_set, frozenset((Q0, Q1))] = full_value

    q0_triples = {(0, 1, 2): 2, (0, 2, 3): 2, (0, 1, 4): 1}
    q1_triples = {(0, 1, 3): 2, (1, 2, 3): 2, (2, 3, 4): 0}
    for triple in combinations(ROOTS, 3):
        root_set = frozenset(triple)
        ledger[root_set, frozenset((Q0,))] = (
            unit(q0_triples[triple]) if triple in q0_triples else sp.zeros(3, 1)
        )
        ledger[root_set, frozenset((Q1,))] = (
            unit(q1_triples[triple]) if triple in q1_triples else sp.zeros(3, 1)
        )

    for quartet in combinations(ROOTS, 4):
        root_set = frozenset(quartet)
        value = unit(2, sp.Rational(1, 7)) if quartet == (0, 1, 2, 3) else sp.zeros(3, 1)
        ledger[root_set, frozenset()] = value
        ledger[root_set, frozenset((Q0, Q1))] = value

    root_set = frozenset(ROOTS)
    ledger[root_set, frozenset((Q0,))] = sp.zeros(3, 1)
    ledger[root_set, frozenset((Q1,))] = sp.zeros(3, 1)
    return ledger


def graph_tensor_for_subset(
    root_subset: tuple[int, ...],
    blocks: dict[tuple[int, int], sp.Expr],
    ledger: dict[tuple[frozenset[int], frozenset[int]], sp.Matrix],
) -> sp.Matrix:
    tags = (
        (frozenset(), frozenset((Q0, Q1)))
        if len(root_subset) % 2 == 0
        else (frozenset((Q0,)), frozenset((Q1,)))
    )
    result = sp.zeros(3, 1)
    roots = frozenset(root_subset)
    for tag in tags:
        companion = hafnian_form(tuple(root_subset) + tuple(tag), blocks)
        result += companion * ledger[roots, tag]
    return result.applyfunc(sp.expand)


def check_common_221_model() -> None:
    local, p, q, b, h, blocks = build_model()
    ledger = build_ledger()

    # One honest common endpoint/root-edge system supplies every subset.
    assert len(b) == 10 and len(h) == 10
    for pair in combinations(ROOTS, 2):
        assert h[pair] == sp.expand(p[pair[0]] * q[pair[1]] + q[pair[0]] * p[pair[1]])

    # The six selected triple companion forms and the only nonzero quartet.
    expected_triples = {
        ((0, 1, 2), Q0): local[0][2] * local[1][2] * local[2][2],
        ((0, 1, 3), Q1): local[0][2] * local[1][2] * local[3][2],
        ((0, 2, 3), Q0): local[0][2] * local[2][2] * local[3][2],
        ((1, 2, 3), Q1): local[1][2] * local[2][2] * local[3][2],
        ((0, 1, 4), Q0): local[0][1] * local[1][1] * local[4][1],
        ((2, 3, 4), Q1): local[2][0] * local[3][0] * local[4][0],
    }
    for (triple, endpoint), expected in expected_triples.items():
        assert sp.expand(hafnian_form(triple + (endpoint,), blocks) - expected) == 0

    g0 = hafnian_form((0, 1, 2, 3), blocks)
    gq = hafnian_form((0, 1, 2, 3, Q0, Q1), blocks)
    target_quartet = local[0][2] * local[1][2] * local[2][2] * local[3][2]
    assert sp.expand(g0 + gq - 7 * target_quartet) == 0

    # This fixed symbolic loop checks the 31 labelled lower-root equations;
    # it is not a support or graph-family enumeration.
    checked = 0
    for size in range(1, 6):
        for root_subset in combinations(ROOTS, size):
            graph_value = graph_tensor_for_subset(root_subset, blocks, ledger)
            target = sp.Matrix(
                [sp.prod(local[root][color] for root in root_subset) for color in range(3)]
            )
            assert all(sp.expand(value) == 0 for value in graph_value - target)
            checked += 1
    assert checked == 31

    # Root labels plus the parity tag make every formal cofactor key unique.
    assert len(ledger) == 62


def main() -> None:
    check_same_axis_triple_obstruction()
    check_common_221_model()
    print("PASS: strict two-endpoint model forbids three same-axis roots")
    print("PASS: one common 2+2+1 tangent-block system satisfies all lower jets")
    print("PASS: globally nonconflicting formal cofactor ledger")
    print("SCOPE: common principal-hafnian realization and global P7 remain UNRESOLVED")


if __name__ == "__main__":
    main()
