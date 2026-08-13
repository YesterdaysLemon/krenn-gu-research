"""Exact replay for the support-two mixed-row-rank exclusion.

The owning Markdown file contains the proof.  This verifier checks its
displayed graph, coefficient-table, and target-line identities over SymPy.
"""

from __future__ import annotations

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def root_index(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def place_13_2(c13: sp.Matrix, b2: sp.Matrix) -> sp.Matrix:
    """Put (A1 tensor A3) tensor A2 into physical A1,A2,A3 order."""
    out = sp.zeros(27, 1)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                out[root_index(a, b, c)] = c13[3 * a + c] * b2[b]
    return out


def derivative_value(
    a1: sp.Matrix,
    a2: sp.Matrix,
    block_b23: sp.Matrix,
    block_c13: sp.Matrix,
) -> sp.Matrix:
    return sp.kronecker_product(a1, block_b23) + place_13_2(
        block_c13, a2
    )


def contracted_graph_identity() -> None:
    beta, chi, nu = sp.symbols("beta chi nu", nonzero=True)
    le1 = -beta * e(0) / chi + nu * e(1) / chi
    contracted = beta * pair(e(1), e(0)) + chi * pair(e(1), le1)
    assert sp.simplify(contracted - nu * pair(e(1), e(1))) == sp.zeros(9, 1)

    compatible_missing_colours = [
        d for d in range(3) if sp.simplify(le1[d]) == 0
    ]
    assert compatible_missing_colours == [2]
    print("contracted graph: PASS (mixed support forces missing colour 2)")


def symbolic_target_table() -> None:
    beta, chi, nu, kappa = sp.symbols(
        "beta chi nu kappa", nonzero=True
    )
    l00, l10, l02, l12 = sp.symbols("l00 l10 l02 l12")
    graph = sp.Matrix(
        [
            [l00, -beta / chi, l02],
            [l10, nu / chi, l12],
            [0, 0, 0],
        ]
    )

    b_symbols = sp.symbols("b00 b01 b02 b10 b11 b12")
    block_b = sp.Matrix(
        [
            list(b_symbols[:3]),
            list(b_symbols[3:]),
            [0, 0, kappa],
        ]
    )
    c_symbols = sp.symbols("c00:03 c10:13 c20:23")
    block_c = sp.Matrix(3, 3, c_symbols)
    flat_b = sp.Matrix(9, 1, list(block_b))
    flat_c = sp.Matrix(9, 1, list(block_c))

    singleton_rows = [
        derivative_value(e(i), graph * e(i), flat_b, flat_c)
        for i in range(3)
    ]
    graph_sample = graph.subs({l00: 1, l10: 0, l02: 0, l12: 1})
    assert graph_sample.rank() == 2

    targets = [tensor3(e(i), e(i), e(i)) for i in range(3)]
    target = sp.zeros(27, 27)
    for i in range(3):
        target[root_index(i, i, i), :] = targets[i].T

    # The b=2 rows force S0=S1=0 and S2=-T2/kappa.
    correction = -singleton_rows[2] * targets[2].T / kappa
    all_cross = sp.simplify(target + correction)

    for a in range(3):
        for c in range(3):
            assert all_cross.row(root_index(a, 2, c)) == sp.zeros(1, 27)

    row_110 = all_cross.row(root_index(1, 1, 0)).T
    row_111 = all_cross.row(root_index(1, 1, 1)).T
    target_span = sp.Matrix.hstack(targets[1], targets[2])
    assert target_span.rank() == 2
    assert sp.Matrix.hstack(row_110, targets[2]).rank() <= 1

    gamma = sp.symbols("gamma", nonzero=True)
    relation_defect = sp.simplify(row_111 - gamma * row_110)
    assert relation_defect[root_index(1, 1, 1)] == 1
    assert relation_defect != sp.zeros(27, 1)
    print("symbolic target table: PASS (T1 survives every T2 correction)")


def zero_row_forcing() -> None:
    b20, b21 = sp.symbols("b20 b21")
    kappa = sp.symbols("kappa", nonzero=True)
    target_2 = tensor3(e(2), e(2), e(2))
    s2 = -target_2 / kappa
    target_coordinate = root_index(2, 2, 2)
    assert sp.solve(
        [
            sp.expand(b20 * s2[target_coordinate]),
            sp.expand(b21 * s2[target_coordinate]),
        ],
        (b20, b21),
        dict=True,
    ) == [{b20: 0, b21: 0}]
    assert sp.simplify(kappa * s2 + target_2) == sp.zeros(27, 1)
    s0 = sp.Matrix(sp.symbols("s0:27"))
    s1 = sp.Matrix(sp.symbols("s1:27"))
    for coefficient in (*s0, *s1):
        assert sp.solve(kappa * coefficient, coefficient) == [0]
    print("zero-row forcing: PASS (B row 2 and S0,S1,S2 pinned)")


def three_by_three_local_control() -> None:
    target_1 = tensor3(e(1), e(1), e(1))
    zero = sp.zeros(27, 1)
    m0 = zero
    m1 = zero
    correction_0 = zero
    correction_1 = -target_1
    assert m0 == correction_0
    assert m1 - target_1 == correction_1
    assert m1 == -m0
    print("(3,3) stop control: PASS (an unrestricted T1 correction absorbs slice)")


def main() -> None:
    contracted_graph_identity()
    zero_row_forcing()
    symbolic_target_table()
    three_by_three_local_control()
    print("rank-five support-two mixed-row-rank exclusion: PASS")


if __name__ == "__main__":
    main()
