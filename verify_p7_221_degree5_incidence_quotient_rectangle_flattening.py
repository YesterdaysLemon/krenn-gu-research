"""Verify the incidence-quotient degree-five rectangle theorem.

This is exact symbolic replay only: it reconstructs one formal Wick rectangle,
checks its quotient flattening ranks, and checks the sharp sparse countermodel.
It performs no graph, support, alignment, or mixed-word search.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

import verify_p7_221_common_terminal_block_scalar_hafnian_realizability as scalar

P = scalar.P
RHO = scalar.RHO
RECTANGLE = {
    frozenset("125ab"): sp.Integer(1),
    frozenset("145ab"): sp.Integer(-1),
    frozenset("235ab"): sp.Integer(-1),
    frozenset("345ab"): sp.Integer(1),
}


def hafnian_evaluator(matrix: dict[frozenset[str], sp.Expr]):
    @cache
    def hafnian(vertices: tuple[str, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        if len(vertices) % 2:
            return sp.Integer(0)
        first = vertices[0]
        total = sp.Integer(0)
        for position, second in enumerate(vertices[1:], 1):
            rest = vertices[1:position] + vertices[position + 1 :]
            total += matrix.get(frozenset((first, second)), 0) * hafnian(rest)
        return sp.expand(total)

    return lambda vertices: hafnian(tuple(sorted(vertices)))


def formal_wick_value(colour: int, face: frozenset[str]) -> sp.Expr:
    ledger, _ = scalar.formal_ledger()
    minus_terminal_block = {
        edge: -weight for edge, weight in scalar.common_terminal_block().items()
    }
    hafnian = hafnian_evaluator(minus_terminal_block)
    total = sp.Integer(0)
    ordered_face = tuple(terminal for terminal in P if terminal in face)
    for even_size in (0, 2, 4):
        for edge_set_tuple in combinations(ordered_face, even_size):
            edge_set = frozenset(edge_set_tuple)
            surviving = face - edge_set
            deletion = frozenset(P) - surviving
            total += hafnian(edge_set) * ledger[colour][deletion]
    return sp.simplify(total)


def permanent_evaluator(matrix: sp.Matrix):
    @cache
    def permanent(rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Expr:
        if not rows:
            return sp.Integer(1)
        first = rows[0]
        return sp.expand(
            sum(
                matrix[first, column]
                * permanent(rows[1:], columns[:position] + columns[position + 1 :])
                for position, column in enumerate(columns)
            )
        )

    return permanent


def flattening_columns(left_vectors: tuple[sp.Matrix, ...], coefficients: tuple[sp.Expr, ...]):
    return sp.Matrix.hstack(
        *(coefficient * vector for coefficient, vector in zip(coefficients, left_vectors, strict=True))
    )


def main() -> None:
    assert sp.simplify(RHO**2 - 21) == 0

    expected = {
        frozenset("125ab"): (RHO - 2, 0, (1 + RHO) / 7),
        frozenset("145ab"): (0, 0, (1 + RHO) / 7),
        frozenset("235ab"): (0, 0, (1 + RHO) / 7),
        frozenset("345ab"): (0, RHO - 2, (1 + RHO) / 7),
    }
    wick_values: dict[frozenset[str], tuple[sp.Expr, ...]] = {}
    for face in RECTANGLE:
        actual = tuple(formal_wick_value(colour, face) for colour in range(3))
        assert all(sp.simplify(left - right) == 0 for left, right in zip(actual, expected[face], strict=True))
        wick_values[face] = actual
    rectangle_value = tuple(
        sp.simplify(sum(RECTANGLE[face] * wick_values[face][colour] for face in RECTANGLE))
        for colour in range(3)
    )
    assert rectangle_value == (RHO - 2, RHO - 2, 0)

    # In a nondegenerate quotient choose a0,a1 as independent left vectors.
    # The corresponding pure right tensors b0,b1 are independent as well, so
    # this two-column matrix is the relevant flattening core.
    a0 = sp.Matrix((1, 0))
    a1 = sp.Matrix((0, 1))
    formal_nondegenerate = flattening_columns((a0, a1), (RHO - 2, RHO - 2))
    assert formal_nondegenerate.rank() == 2
    assert sp.simplify(formal_nondegenerate.det() - (RHO - 2) ** 2) == 0

    # Lemma 1 says every physical projection is an outer product.  Check its
    # 2x2 minors identically for generic entries.
    x0, x1, y0, y1 = sp.symbols("x0 x1 y0 y1")
    physical = sp.Matrix((x0, x1)) * sp.Matrix((y0, y1)).T
    assert sp.expand(physical.det()) == 0

    # Sharp failure: quotient pi_i kills colour 0 but retains colour 1.
    quotient_i = sp.Matrix(((0, 1, 0), (0, 0, 1)))
    quotient_j = sp.eye(3)
    e0 = sp.Matrix((1, 0, 0))
    e1 = sp.Matrix((0, 1, 0))
    counter_a0 = sp.kronecker_product(quotient_i * e0, quotient_j * e0)
    counter_a1 = sp.kronecker_product(quotient_i * e1, quotient_j * e1)
    assert counter_a0 == sp.zeros(6, 1)
    assert counter_a1 != sp.zeros(6, 1)
    counter_formal = flattening_columns((counter_a0, counter_a1), (RHO - 2, RHO - 2))
    assert counter_formal.rank() == 1

    # Five remaining core modes select 1,2,5,a,b.  The sparse permanent is
    # rho-2 on 125ab and zero on the other three rectangle faces.
    incidence = sp.zeros(5, 7)
    selected = ((0, "1", RHO - 2), (1, "2", 1), (2, "5", 1), (3, "a", 1), (4, "b", 1))
    for row, terminal, value in selected:
        incidence[row, P.index(terminal)] = value
    permanent = permanent_evaluator(incidence)
    physical_permanents = {
        face: sp.simplify(permanent(tuple(range(5)), tuple(P.index(p) for p in P if p in face)))
        for face in RECTANGLE
    }
    assert physical_permanents == {
        frozenset("125ab"): RHO - 2,
        frozenset("145ab"): 0,
        frozenset("235ab"): 0,
        frozenset("345ab"): 0,
    }
    physical_rectangle_scalar = sp.simplify(
        sum(RECTANGLE[face] * physical_permanents[face] for face in RECTANGLE)
    )
    assert physical_rectangle_scalar == RHO - 2
    assert physical_rectangle_scalar * counter_a1 == counter_formal[:, 1]

    print("degree-five incidence-quotient rectangle theorem: VERIFIED")
    print("formal_rectangle=(rho-2)(D0+D1)")
    print("physical_pair_quotient_flattening_rank<=1: SYMBOLIC")
    print("formal_rank_under_independence=2")
    print("degenerate_quotient_countermodel_rank=1: VERIFIED")
    print("common_terminal_block=fixed; core_A_and_R=arbitrary")
    print("graph_search=0 support_search=0 mixed_word_enumeration=0")
    print("global_status=CONDITIONAL_OBSTRUCTION")


if __name__ == "__main__":
    main()
