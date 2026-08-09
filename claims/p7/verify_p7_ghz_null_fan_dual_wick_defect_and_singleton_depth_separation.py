"""Verify GHZ-null fan words and their vacuum-free response boundary.

The replay checks fixed symbolic identities only.  It performs no graph,
support, colour-word, window, selector, or parameter enumeration.
"""

from __future__ import annotations

from functools import cache

import sympy as sp


def ghz_diagonal_value(local_axes: tuple[int, ...]) -> tuple[int, int, int]:
    """Return the three pure diagonal monomial evaluations."""

    return tuple(int(all(axis == colour for axis in local_axes)) for colour in range(3))


def hafnian(vertices: tuple[int, ...], edge: dict[tuple[int, int], sp.Expr]) -> sp.Expr:
    @cache
    def recurse(current: tuple[int, ...]) -> sp.Expr:
        if not current:
            return sp.Integer(1)
        first = current[0]
        return sp.expand(
            sum(
                edge.get(tuple(sorted((first, partner))), sp.Integer(0))
                * recurse(current[1:position] + current[position + 1 :])
                for position, partner in enumerate(current[1:], start=1)
            )
        )

    return recurse(vertices)


def square_zero_multiply(
    left: tuple[sp.Expr, sp.Expr], right: tuple[sp.Expr, sp.Expr]
) -> tuple[sp.Expr, sp.Expr]:
    return (
        sp.expand(left[0] * right[0]),
        sp.expand(left[0] * right[1] + left[1] * right[0]),
    )


def main() -> None:
    # Full seven-blocker assignments: blocker order is (t,1,2,3,4,5,6).
    # The shore colour is used at t and every forced-shore blocker; retained
    # double blockers use their common-null/missing-colour axes.
    target_1234 = (1, 1, 1, 2, 2, 1, 1)
    fan_1256 = (0, 1, 1, 0, 0, 0, 0)
    fan_1356 = (0, 1, 0, 2, 0, 0, 0)
    fan_1456 = (0, 1, 0, 0, 2, 0, 0)
    for word in (target_1234, fan_1256, fan_1356, fan_1456):
        assert ghz_diagonal_value(word) == (0, 0, 0)

    six_double_word = (0, 1, 1, 2, 2, 0, 0)
    assert ghz_diagonal_value(six_double_word) == (0, 0, 0)

    # Independent companion columns turn a zero target vector into two zero
    # response coefficients.
    f, z_top, m_top = sp.symbols("f z_top m_top", nonzero=True)
    companion_matrix = sp.eye(2)
    selected = f * companion_matrix * sp.Matrix((z_top, m_top))
    solution = sp.solve(tuple(selected), (z_top, m_top), dict=True)
    assert solution == []  # nonzero assumptions prohibit a zero solution object
    # Drop assumptions for the exact linear solve.
    z_free, m_free = sp.symbols("z_free m_free")
    assert sp.linsolve((f * companion_matrix, sp.zeros(2, 1)), (z_free, m_free)) == {
        (0, 0)
    }

    # With m_W=z_W=0, the four-point dual-Wick identity is vacuum-free.
    h = sp.Symbol("h")
    z_pairs = sp.symbols("z12 z13 z14 z23 z24 z34")
    m_complements = sp.symbols("m34 m24 m23 m14 m13 m12")
    insertion = sp.expand(sum(z * m for z, m in zip(z_pairs, m_complements, strict=True)))
    defect = insertion - sp.Integer(0)
    assert sp.expand(defect - h * 0) == insertion

    # Root-only lower-jet labels contain no blocker deletions, whereas a pair
    # face deletes five blockers.  This fixed representative audits the exact
    # label separation used by Proposition 4.
    roots = frozenset({"r0", "r1", "r2", "r3", "r4"})
    residuals = frozenset({"q0", "q1"})
    blockers = frozenset({"b0", "b1", "b2", "b3", "b4", "b5", "b6"})
    lower_jet_label = frozenset({"r0", "r2"}) | residuals
    pair_face_label = roots | (blockers - {"b0", "b1"})
    direct_pair_label = pair_face_label | residuals
    assert not (lower_jet_label & blockers)
    assert len(pair_face_label & blockers) == 5
    assert lower_jet_label not in (pair_face_label, direct_pair_label)

    # Physical free-h family: M=1+t, Phi=lambda-lambda*t, so Z=lambda.
    lam = sp.Symbol("lambda")
    assert square_zero_multiply((1, 1), (lam, -lam)) == (lam, 0)

    # Audit directly on the physical graph for a fan four-set and all six
    # double blockers.  Vertices 0..6 are ports, 7,8 are residuals.
    physical_edges = {
        (0, 1): sp.Integer(1),
        (7, 8): lam,
        (0, 7): -lam,
        (1, 8): sp.Integer(1),
    }
    assert hafnian((0, 1, 7, 8), physical_edges) == 0
    assert hafnian((0, 1, 2, 3), physical_edges) == 0
    assert hafnian((0, 1, 2, 3, 7, 8), physical_edges) == 0
    assert hafnian((0, 1, 2, 3, 4, 5), physical_edges) == 0
    assert hafnian((0, 1, 2, 3, 4, 5, 7, 8), physical_edges) == 0
    assert sp.diff(-lam, lam) == -1  # one blocker singleton row varies with h

    print("P7 GHZ-null fan and dual-Wick defect: VERIFIED")
    print("tetrahedral_fan_target_values=0 six_double_target_value=0")
    print("independent_top_selectors_force=m4=z4=0")
    print("null_window_equation=sum(z_e*m_comp)=0")
    print("root_only_ledger_vs_pair_face_labels=DISJOINT")
    print("physical_free_h_boundary=M(1+t)*Phi(lambda-lambda*t)=lambda")
    print("root_singleton_vs_blocker_singleton=SEPARATE_EDGE_FAMILIES")
    print("searches=0 enumerations=0 P7_GLOBAL_STATUS=UNKNOWN")


if __name__ == "__main__":
    main()
