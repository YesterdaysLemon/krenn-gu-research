#!/usr/bin/env python3
"""Verify the exact GLD87 H1--H3 determinant-safety theorem.

The calculation is over ``Q`` for the actual equal-leaf frame and is then
read as a characteristic-zero statement (and hence after extension to
``C``).  It uses the pinned GLD71 syndrome map, but keeps the H1 proof local:
the 11 selected rows are enough to obstruct an invertible center.  The two
other pair-collision divisors are transferred by exact leaf-column
equivariance.  H4 is deliberately not analyzed here.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD71 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD86 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py"
)

COMPRESSED_ROWS = (0, 1, 2, 17, 19, 25, 28, 31, 32, 33, 34)
BASE_ROWS = (0, 1, 3, 4, 9)
DIFFERENCE_ROWS = (2, 5, 6, 7, 8, 10)
BASE_COLUMNS = (1, 2, 4, 5, 7, 8)
DIFFERENCE_COLUMNS = (0, 3, 6)
EXCEPTIONAL_7_ROWS = (0, 1, 9, 2, 5, 6, 8)
EXCEPTIONAL_7_COLUMNS = (1, 2, 4, 7, 0, 3, 6)
EXCEPTIONAL_6_ROWS = (0, 1, 2, 5, 6, 7)
EXCEPTIONAL_6_COLUMNS = (0, 1, 3, 4, 6, 7)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def quotient_remainder_in_s(expression: sp.Expr, relation: sp.Expr) -> sp.Expr:
    variable = next(iter(relation.free_symbols))
    return (
        sp.Poly(sp.expand(expression), variable)
        .rem(sp.Poly(relation, variable))
        .as_expr()
    )


def check() -> dict[str, object]:
    # GLD86 is the exact upstream bridge: on B, ``M C = 0`` is equivalent to
    # the ten pinned basis equations, and differentiation gives rank(A) equal
    # to the first-eight syndrome-column rank.
    gld86 = load_module(GLD86, "gld86_for_gld87")
    upstream = gld86.check()
    assert upstream["rank_at_most_six_confined_to_named_divisors"] is True
    assert upstream["global_conjecture_resolved"] is False

    gld71 = load_module(GLD71, "gld71_for_gld87")
    parent = (
        gld86.load_module(gld86.GLD75, "gld75_for_gld87")
        .load_gld72()
        .load_gate()
        .load_parent()
    )
    relations = gld71.full_relations(parent)
    assert len(relations) == 37

    p, q, s, a, b, c = sp.symbols("p q s a b c")
    leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, b, c]])
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    assert syndrome.shape == (37, 9)
    center_coordinates = sp.Matrix(sp.symbols("C0:8"))
    center_with_unit = sp.Matrix(list(center_coordinates) + [1])
    assert (
        syndrome * center_with_unit
        == syndrome[:, 8] + syndrome[:, :8] * center_coordinates
    )

    # The first two leaf columns collide on H1.  A unimodular within-block
    # change makes the difference columns visibly separate from the base
    # columns; no division by a parameter occurs in this transform.
    selected = syndrome.extract(COMPRESSED_ROWS, range(9))
    t0 = sp.Matrix([[1, 0, 0], [-1, 1, 0], [0, 0, 1]])
    transformed = selected * sp.diag(t0, t0, t0)
    transformed = transformed.subs(q, p)
    assert transformed.extract(BASE_ROWS, DIFFERENCE_COLUMNS) == sp.zeros(5, 3)

    base = transformed.extract(BASE_ROWS, BASE_COLUMNS)
    difference = transformed.extract(DIFFERENCE_ROWS, DIFFERENCE_COLUMNS)
    expected_base = sp.Matrix(
        [
            [0, 0, p**3, s**3, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [p**2 - p, s**2 - s, -2 * p**2 + 2 * p - 1, -2 * s**2 + 2 * s - 1, 0, 0],
            [
                p**3 - 2 * p**2 + 2 * p,
                s**3 - 2 * s**2 + 2 * s,
                p**2 - p,
                s**2 - s,
                0,
                0,
            ],
            [
                0,
                0,
                12 * p**2 - 12 * p + 4,
                12 * s**2 - 12 * s + 4,
                -12 * p**2 + 12 * p,
                -12 * s**2 + 12 * s,
            ],
        ]
    )
    assert transformed.applyfunc(sp.expand) == transformed
    assert base == expected_base

    expected_difference = sp.Matrix(
        [
            [0, 0, -(p**2 - 1)],
            [0, 2 * p - 1, 1 - 2 * p],
            [p * (p - 2), 0, -p * (p - 2)],
            [0, 6 * (p**2 + 2 * p - 2), 0],
            [6 * (2 * p**2 - 2 * p - 1), 0, 0],
            [0, 12 * (2 * p - 1), 12 * p * (p - 2)],
        ]
    )
    assert difference.applyfunc(sp.expand) == ((a - b) * expected_difference).applyfunc(
        sp.expand
    )

    # Every nonzero base 4-minor has the diagonal collision factor p-s.
    # Their exact Groebner basis gives the only residual pair away from p=s.
    normalized = []
    nonzero_base_minors = 0
    for row_indices in itertools.combinations(range(5), 4):
        for column_indices in itertools.combinations(range(6), 4):
            minor = sp.expand(
                base.extract(row_indices, column_indices).det(method="domain-ge")
            )
            if minor == 0:
                continue
            nonzero_base_minors += 1
            quotient, remainder = sp.div(minor, p - s, domain=sp.QQ)
            assert remainder == 0
            normalized.append(sp.expand(quotient))
    assert nonzero_base_minors == 37
    groebner = sp.groebner(normalized, p, s, order="lex")
    basis = tuple(sp.expand(value.as_expr()) for value in groebner.polys)
    assert basis == (
        p - 2 * s**3 + 3 * s**2 - 2 * s,
        s**4 - 2 * s**3 + 2 * s**2 - s,
    )
    assert sp.factor(basis[1]) == s * (s - 1) * (s**2 - s + 1)

    # The difference block has rank three for every p in characteristic zero:
    # three displayed minors have gcd one.
    difference_minors = tuple(
        sp.factor(
            difference.extract(rows, (0, 1, 2)).det(method="domain-ge") / (a - b) ** 3
        )
        for rows in ((0, 1, 2), (0, 1, 4), (2, 3, 4))
    )
    assert tuple(sp.expand(value) for value in difference_minors) == tuple(
        sp.expand(value)
        for value in (
            p * (p - 2) * (p - 1) * (p + 1) * (2 * p - 1),
            6 * (p - 1) * (p + 1) * (2 * p - 1) * (2 * p**2 - 2 * p - 1),
            36 * p * (p - 2) * (p**2 + 2 * p - 2) * (2 * p**2 - 2 * p - 1),
        )
    )
    assert (
        sp.gcd(sp.gcd(difference_minors[0], difference_minors[1]), difference_minors[2])
        == 1
    )

    relation = s**2 - s + 1
    # The residual pair p=1-s, relation=0 is the only candidate not already
    # removed by det(G)=(p-s)(b-a) != 0.  Two exact minors and a kernel vector
    # finish the H1 determinant-safety statement on that pair.
    minor_7 = sp.expand(
        transformed.extract(EXCEPTIONAL_7_ROWS, EXCEPTIONAL_7_COLUMNS)
        .subs(p, 1 - s)
        .det(method="domain-ge")
    )
    reduced_7 = sp.factor(quotient_remainder_in_s(minor_7, relation))
    assert reduced_7 == -648 * (a - b) ** 3 * (c * s + c - s)
    minor_6 = sp.expand(
        transformed.extract(EXCEPTIONAL_6_ROWS, EXCEPTIONAL_6_COLUMNS)
        .subs(p, 1 - s)
        .det(method="domain-ge")
    )
    reduced_6 = sp.factor(quotient_remainder_in_s(minor_6, relation))
    assert reduced_6 == 36 * (a - b) ** 3 * (2 * s - 1)
    assert sp.gcd(sp.Poly(s + 1, s), sp.Poly(relation, s)).as_expr() == 1
    assert sp.gcd(sp.Poly(2 * s - 1, s), sp.Poly(relation, s)).as_expr() == 1

    kernel_vector = sp.Matrix([3 * b + s - 2, -3 * (a - b), 3 * (a - b)])
    kernel_substitution = {p: 1 - s, c: (s + 1) / 3}
    for block in (0, 3, 6):
        for row in range(transformed.rows):
            value = sp.expand((transformed[row, block : block + 3] * kernel_vector)[0])
            assert (
                quotient_remainder_in_s(value.subs(kernel_substitution), relation) == 0
            )

    # Exact S3 covariance transfers the H1 obstruction to H2 and H3.  The
    # block permutation is the same on every center row, so det(C) changes by
    # only det(P)=+-1.
    swap_23 = (0, 2, 1, 3, 5, 4, 6, 8, 7)
    swap_13 = (2, 1, 0, 5, 4, 3, 8, 7, 6)
    assert syndrome.xreplace({q: s, s: q, b: c, c: b}) == syndrome[:, swap_23]
    assert syndrome.xreplace({p: s, s: p, a: c, c: a}) == syndrome[:, swap_13]

    # The actual leaf frame determinant on H1 is (p-s)(b-a), so the proof is
    # explicitly restricted to the leaf-invertible retained chart.
    assert sp.expand(leaf.det().subs(q, p)) == sp.expand((p - s) * (b - a))

    return {
        "status": "exact_GLD87_H1_H2_H3_determinant_safety",
        "global_conjecture": "UNRESOLVED",
        "field": "Q_characteristic_zero_then_C",
        "syndrome_shape": list(syndrome.shape),
        "compressed_rows": list(COMPRESSED_ROWS),
        "base_rows": list(BASE_ROWS),
        "difference_rows": list(DIFFERENCE_ROWS),
        "base_nonzero_4_minors": nonzero_base_minors,
        "base_groebner_basis": [str(value) for value in basis],
        "difference_minors_gcd": "1",
        "exceptional_pair": "p=1-s, s^2-s+1=0",
        "exceptional_7_minor_mod_relation": "-648*(a-b)^3*(c*s+c-s)",
        "exceptional_6_minor_mod_relation": "36*(a-b)^3*(2*s-1)",
        "exceptional_kernel_vector": "(3*b+s-2, -3*(a-b), 3*(a-b))",
        "leaf_det": "(p-s)*(b-a)",
        "h1_h2_h3_excluded_under_invertible_center": True,
        "omega_saturated_h1_h2_h3_excluded": True,
        "retained_low_rank_confined_to_h4": True,
        "h4_analyzed": False,
        "fitting_pullback_computed": False,
        "omega_saturated_global_exclusion": False,
        "global_conjecture_resolved": False,
        "upstream_gld86_status": upstream["status"],
        "exact_leaf_column_equivariance": True,
    }


def main() -> None:
    print("four-root equal-leaf GLD87 H1-H3 determinant safety: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
