#!/usr/bin/env python3
"""Independent exact audit of the transverse mixed-chain boundary."""

from __future__ import annotations

import itertools
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MIXED_CHAIN_TRANSVERSE_COMPONENT_INCLUSION.md"
PRIMARY = ROOT / "verify_p4_mixed_chain_transverse_component_inclusion.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent_dp(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        updated: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                updated[new_mask] = sp.expand(updated.get(new_mask, 0) + value * entry)
        states = updated
    return states[15]


def restriction(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent_dp(tuple(planes[mode].row(word[mode]) for mode in range(4)))
        for word in WORDS
    }


def pair_product_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    rows = []
    for left_row, right_row in itertools.product(range(2), repeat=2):
        u = left.row(left_row)
        v = right.row(right_row)
        rows.append([sp.expand(u[p] * v[q] + u[q] * v[p]) for p, q in SOURCE_PAIRS])
    return sp.Matrix(rows).T


def pluecker(plane: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(plane[0, p] * plane[1, q] - plane[0, q] * plane[1, p])
            for p, q in SOURCE_PAIRS
        ]
    )


def limit_at_zero(vector: sp.Matrix, t: sp.Symbol) -> sp.Matrix:
    return vector.applyfunc(lambda entry: sp.cancel(entry).subs(t, 0))


def main() -> None:
    assert THEOREM.exists() and PRIMARY.exists()
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "(V_2,V_1,V_3,V_0)" in theorem
    assert "not part of the" in theorem
    assert "`433333` cell" in theorem

    # A rational generic target point, chosen independently of the primary.
    P = sp.Integer(2)
    phi = sp.Integer(2)
    A = sp.Matrix([[1, 1, 0, 0]])
    C = sp.Matrix([[1, -1, 0, 0]])
    B = sp.Matrix([[0, 0, 1, 1]])
    D = sp.Matrix([[0, 0, 1, -1]])
    w = P * C + B + phi * D
    z = -P * C + phi * D + phi**2 * B
    target = (
        sp.Matrix.vstack(A, z),
        sp.Matrix.vstack(A, w),
        sp.Matrix.vstack(C, B),
        sp.Matrix.vstack(D, C),
    )

    target_tensor = restriction(target)
    assert target_tensor[(1, 1, 1, 1)] == -24
    assert all(
        value == 0 for word, value in target_tensor.items() if word != (1, 1, 1, 1)
    )

    expected_relations = {
        (0, 2): sp.Matrix((1, 0, 0, 0)),
        (0, 3): sp.Matrix((0, 1, 0, 0)),
        (1, 2): sp.Matrix((1, 0, 0, 0)),
        (1, 3): sp.Matrix((0, 1, 0, 0)),
        (2, 3): sp.Matrix((0, 0, 1, 0)),
    }
    profile = []
    for edge in itertools.combinations(range(4), 2):
        matrix = pair_product_matrix(target[edge[0]], target[edge[1]])
        profile.append(matrix.rank())
        if edge == (0, 1):
            assert matrix.nullspace() == []
            continue
        kernel = matrix.nullspace()
        assert len(kernel) == 1
        relation = kernel[0]
        expected = expected_relations[edge]
        pivot = next(index for index, entry in enumerate(expected) if entry)
        assert relation * expected[pivot] == expected * relation[pivot]
        assert sp.Matrix(2, 2, relation).rank() == 1
    assert tuple(profile) == (4, 3, 3, 3, 3, 3)

    # Rebuild the component-eight family without importing the primary.
    t, q = sp.symbols("t q", nonzero=True)
    b = t**-2
    f = sp.Rational(1, 2)
    psi = sp.Integer(1)
    a = q / t
    j = f + b * psi**2
    kappa = psi * (b * f + 1)
    eta = -(b * f + 1)
    old = (
        sp.Matrix.vstack(D, a * A + b * C + B - D),
        sp.Matrix.vstack(C - a * f * A + f * B + psi * D, A),
        sp.Matrix.vstack(-a * j * A + eta * C + j * B + kappa * D, A),
        sp.Matrix.vstack(C, B),
    )

    phi_equation = sp.expand(
        a**2 * b * f * psi**2 + a**2 * f**2 - b**2 * f**2 + b**2 * psi**2 - b * f - 1
    )
    q_squared = (-6 + 4 * t**2 + 8 * t**4) / (4 + 2 * t**2)
    assert sp.factor(phi_equation.subs(q**2, q_squared)) == 0
    assert q_squared.subs(t, 0) == sp.Rational(-3, 2)

    old_tensor = restriction(old)
    for word, value in old_tensor.items():
        expected = 4 if word == (1, 1, 1, 1) else 0
        assert sp.factor((value - expected).subs(q**2, q_squared)) == 0

    # Independent Pluecker-coordinate replay of the four Grassmann limits.
    v0_limit = limit_at_zero(t**2 * pluecker(old[0]), t)
    assert v0_limit == pluecker(sp.Matrix.vstack(D, C))

    v1_pluecker = pluecker(old[1])
    assert sp.simplify(v1_pluecker + pluecker(target[1]) / P) == sp.zeros(6, 1)

    v2_limit = limit_at_zero(P**2 * t**2 * pluecker(old[2]), t)
    assert v2_limit == -pluecker(target[0])

    assert pluecker(old[3]) == pluecker(target[2])

    # The projective kernel lines converge in the permuted mode order.
    kernel_v1 = limit_at_zero(t * old[1].row(0), t)
    kernel_v2 = limit_at_zero(t**3 * old[2].row(0), t)
    assert kernel_v1 == -(q / P) * A
    assert kernel_v2 == -q * A
    assert old[3].row(0) == C
    assert old[0].row(0) == D

    print("audit target profile:", tuple(profile))
    print("audit algebraic arc: Phi=0, q(0)^2=-3/2")
    print("audit Pluecker mode order: (V2,V1,V3,V0)")
    print("audit marked kernel limit: (A,A,C,D)")


if __name__ == "__main__":
    main()
