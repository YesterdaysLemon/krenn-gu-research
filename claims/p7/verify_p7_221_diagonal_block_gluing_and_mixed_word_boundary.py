"""Verify diagonal block gluing of the exact 2+2+1 scalar charts.

The three common-terminal scalar graphs are embedded in one honest bilinear
block graph.  All 186 pure coordinates are checked, together with one exact
nonzero mixed-word witness.  There is no support or parameter search.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp

import verify_p7_221_common_terminal_block_scalar_hafnian_realizability as scalar

Z = tuple(f"z{index}" for index in range(7))
VERTICES = Z + scalar.P
VERTEX_INDEX = {vertex: index for index, vertex in enumerate(VERTICES)}
TERMINAL_VECTOR = sp.Matrix((1, 0, 0))


def ordered(left: str, right: str) -> tuple[str, str]:
    return (left, right) if VERTEX_INDEX[left] < VERTEX_INDEX[right] else (right, left)


def canonical_scalar_graph(builder):
    graph, old_core = builder()
    rename = dict(zip(old_core, Z, strict=True))
    result: dict[frozenset[str], sp.Expr] = {}
    for edge, weight in graph.items():
        left, right = tuple(edge)
        left = rename.get(left, left)
        right = rename.get(right, right)
        scalar.add_edge(result, left, right, weight)
    return result


def scalar_charts():
    return tuple(
        canonical_scalar_graph(builder)
        for builder in (scalar.build_colour_zero, scalar.build_colour_one, scalar.build_colour_two)
    )


def scalar_weight(graph, left: str, right: str) -> sp.Expr:
    return graph.get(frozenset((left, right)), sp.Integer(0))


def build_physical_blocks(charts):
    """Build oriented 3x3 blocks; reverse orientations are transposes."""

    blocks: dict[tuple[str, str], sp.Matrix] = {}
    for left, right in combinations(VERTICES, 2):
        if left in Z and right in Z:
            block = sp.diag(*(scalar_weight(chart, left, right) for chart in charts))
        elif left in Z and right in scalar.P:
            block = sp.zeros(3)
            for colour, chart in enumerate(charts):
                block[colour, 0] = scalar_weight(chart, left, right)
        else:
            assert left in scalar.P and right in scalar.P
            weights = [scalar_weight(chart, left, right) for chart in charts]
            assert all(sp.simplify(weight - weights[0]) == 0 for weight in weights)
            block = sp.zeros(3)
            block[0, 0] = weights[0]
        blocks[left, right] = block
        blocks[right, left] = block.T
    return blocks


def local_vector(vertex: str, core_colours: dict[str, int]) -> sp.Matrix:
    if vertex in scalar.P:
        return TERMINAL_VECTOR
    vector = sp.zeros(3, 1)
    vector[core_colours[vertex]] = 1
    return vector


def evaluate_block(
    blocks: dict[tuple[str, str], sp.Matrix],
    left: str,
    right: str,
    core_colours: dict[str, int],
) -> sp.Expr:
    return sp.simplify(
        (local_vector(left, core_colours).T * blocks[left, right] * local_vector(right, core_colours))[
            0
        ]
    )


def induced_scalar_graph(blocks, core_colours: dict[str, int]):
    graph: dict[frozenset[str], sp.Expr] = {}
    for left, right in combinations(VERTICES, 2):
        weight = evaluate_block(blocks, left, right, core_colours)
        if weight != 0:
            scalar.add_edge(graph, left, right, weight)
    return graph


def cofactor(
    graph: dict[frozenset[str], sp.Expr],
    deletion: frozenset[str],
) -> sp.Expr:
    hafnian = scalar.hafnian_evaluator(graph)
    survivors = tuple(terminal for terminal in scalar.P if terminal not in deletion)
    return hafnian(Z + survivors)


def check_abstract_edge_interpolation() -> None:
    """Check the rank-one extension formula with generic chart scalars."""

    a = sp.symbols("a0:3")
    r = sp.symbols("r0:3")
    m = sp.symbols("m")
    core_core = sp.diag(*a)
    core_terminal = sp.zeros(3)
    for colour in range(3):
        core_terminal[colour, 0] = r[colour]
    terminal_terminal = sp.zeros(3)
    terminal_terminal[0, 0] = m

    for colour in range(3):
        e = sp.eye(3).col(colour)
        assert (e.T * core_core * e)[0] == a[colour]
        assert (e.T * core_terminal * TERMINAL_VECTOR)[0] == r[colour]
    assert (TERMINAL_VECTOR.T * terminal_terminal * TERMINAL_VECTOR)[0] == m


def main() -> None:
    check_abstract_edge_interpolation()
    charts = scalar_charts()
    blocks = build_physical_blocks(charts)

    for left, right in combinations(VERTICES, 2):
        assert blocks[right, left] == blocks[left, right].T

    ledger, prescribed_per_colour = scalar.formal_ledger()
    assert prescribed_per_colour == 62
    expected_free = (
        (sp.Integer(0), 155 + 110 * scalar.RHO / 7),
        (sp.Integer(0), 155 + 110 * scalar.RHO / 7),
        (sp.Rational(103, 147), sp.Rational(103, 147) + 36 * scalar.RHO),
    )

    checked = 0
    for colour in range(3):
        pure_assignment = {vertex: colour for vertex in Z}
        induced = induced_scalar_graph(blocks, pure_assignment)
        for left, right in combinations(VERTICES, 2):
            assert sp.simplify(
                scalar_weight(induced, left, right) - scalar_weight(charts[colour], left, right)
            ) == 0
        for deletion, expected in ledger[colour].items():
            assert sp.simplify(cofactor(induced, deletion) - expected) == 0
            checked += 1
        free_q, free_empty = expected_free[colour]
        assert sp.simplify(cofactor(induced, scalar.Q) - free_q) == 0
        assert sp.simplify(cofactor(induced, frozenset()) - free_empty) == 0
    assert checked == 186

    # This mixed assignment uses c2 on z0,z1,z2 and c0 on z3,...,z6.
    # At D=1234ab only terminal 5 survives.  The unique nonzero factorization
    # is (z0,5)_(c2) * (z1,z2)_(c2) * haf(A0[z3,z4,z5,z6]) = 1/7.
    mixed_assignment = {
        Z[0]: 2,
        Z[1]: 2,
        Z[2]: 2,
        Z[3]: 0,
        Z[4]: 0,
        Z[5]: 0,
        Z[6]: 0,
    }
    mixed_graph = induced_scalar_graph(blocks, mixed_assignment)
    mixed_deletion = frozenset("1234ab")
    mixed_value = cofactor(mixed_graph, mixed_deletion)
    assert sp.simplify(mixed_value - sp.Rational(1, 7)) == 0

    print("diagonal block gluing of the three pure scalar charts: VERIFIED")
    print("physical_blocks=91 symmetric_or_transpose-compatible")
    print("prescribed_pure_values_checked=186")
    print("free_pure_values_checked=6")
    print("mixed witness: D=1234ab, colours=(2,2,2,0,0,0,0), value=1/7")
    print("candidate_searches=0")
    print("off_diagonal_extension_cancellation=UNRESOLVED")


if __name__ == "__main__":
    main()
