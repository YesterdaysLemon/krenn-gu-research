#!/usr/bin/env python3
"""Verify the transverse mixed-chain inclusion in component eight."""

from __future__ import annotations

import itertools
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MIXED_CHAIN_TRANSVERSE_COMPONENT_INCLUSION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))
MODE_PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def tensor(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent(tuple(planes[mode].row(word[mode]) for mode in range(4)))
        for word in WORDS
    }


def squarefree_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[p] * right[q] + left[q] * right[p]) for p, q in SOURCE_PAIRS]
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            squarefree_product(left.row(i), right.row(j))
            for i, j in itertools.product(range(2), repeat=2)
        )
    )


def component_eight_family(
    a: sp.Expr,
    b: sp.Expr,
    f: sp.Expr,
    psi: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    j = f + b * psi**2
    kappa = psi * (b * f + 1)
    eta = -(b * f + 1)
    return (
        sp.Matrix(((0, 0, 1, -1), (a + b, a - b, 0, 2))),
        sp.Matrix(
            (
                (-a * f + 1, -a * f - 1, f + psi, f - psi),
                (1, 1, 0, 0),
            )
        ),
        sp.Matrix(
            (
                (
                    -a * j + eta,
                    -a * j - eta,
                    j + kappa,
                    j - kappa,
                ),
                (1, 1, 0, 0),
            )
        ),
        sp.Matrix(((1, -1, 0, 0), (0, 0, 1, 1))),
    )


def component_eight_equation(
    a: sp.Expr,
    b: sp.Expr,
    f: sp.Expr,
    psi: sp.Expr,
) -> sp.Expr:
    return sp.expand(
        a**2 * b * f * psi**2 + a**2 * f**2 - b**2 * f**2 + b**2 * psi**2 - b * f - 1
    )


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "boundary of component eight" in theorem
    assert "does not classify the vertical mixed-chain fibre" in theorem
    assert "phi=0" in theorem

    P, phi = sp.symbols("P phi", nonzero=True)
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

    # The target tensor is nonzero and pure in the displayed marking.
    target_tensor = tensor(target)
    expected_active = -4 * P * (phi - 1) * (phi + 1)
    for word in WORDS:
        expected = expected_active if word == (1, 1, 1, 1) else 0
        assert sp.factor(target_tensor[word] - expected) == 0

    # Complete relation word and exact rank witnesses.
    relation_vectors = {
        (0, 2): sp.Matrix((1, 0, 0, 0)),
        (0, 3): sp.Matrix((0, 1, 0, 0)),
        (1, 2): sp.Matrix((1, 0, 0, 0)),
        (1, 3): sp.Matrix((0, 1, 0, 0)),
        (2, 3): sp.Matrix((0, 0, 1, 0)),
    }
    matrices = {
        edge: pair_matrix(target[edge[0]], target[edge[1]]) for edge in MODE_PAIRS
    }
    for edge, relation in relation_vectors.items():
        assert matrices[edge] * relation == sp.zeros(6, 1)

    full_minor = matrices[(0, 1)].extract((0, 1, 3, 4), range(4)).det()
    assert sp.factor(full_minor) == 8 * P * phi * (phi - 1) ** 2 * (phi + 1) ** 2

    witnesses = {
        (0, 2): ((0, 1, 3), (1, 2, 3), -4 * P**2),
        (0, 3): ((0, 1, 3), (0, 2, 3), 4 * P**2),
        (1, 2): ((1, 4, 5), (1, 2, 3), -4),
        (1, 3): ((1, 2, 3), (0, 2, 3), 4 * P),
        (2, 3): ((0, 1, 2), (0, 1, 3), 4),
    }
    for edge, (rows, columns, expected) in witnesses.items():
        assert sp.factor(matrices[edge].extract(rows, columns).det()) == expected

    specialized = matrices[(0, 1)].subs(phi, 0)
    extra_relation = sp.Matrix((0, 0, 1, 0))
    assert specialized * extra_relation == sp.zeros(6, 1)
    assert specialized.rank() == 3

    # Independently reconstruct the component-eight pure identity.
    a, b, f, psi = sp.symbols("a b f psi")
    old_planes = component_eight_family(a, b, f, psi)
    hypersurface = component_eight_equation(a, b, f, psi)
    old_tensor = tensor(old_planes)
    for word in WORDS:
        expected = {
            (1, 0, 0, 1): -4 * hypersurface,
            (1, 1, 1, 1): 4,
        }.get(word, 0)
        assert sp.factor(old_tensor[word] - expected) == 0

    # The algebraic Laurent arc lies identically on Phi=0.
    t, q = sp.symbols("t q", nonzero=True)
    arc = {
        a: q / t,
        b: t**-2,
        f: 1 / P,
        psi: phi / P,
    }
    q_squared = (P * (1 - phi**2) + P**2 * t**2 + P**3 * t**4) / (phi**2 + P * t**2)
    arc_equation = sp.factor(hypersurface.subs(arc))
    assert sp.factor(arc_equation.subs(q**2, q_squared)) == 0

    arc_planes = component_eight_family(*tuple(arc[s] for s in (a, b, f, psi)))

    # V0 -> U3 after scaling its second row.
    scaled_v0 = sp.simplify(t**2 * arc_planes[0].row(1))
    expected_v0 = C + t * q * A + t**2 * (B - D)
    assert sp.simplify(scaled_v0 - expected_v0) == sp.zeros(1, 4)
    assert scaled_v0.subs(t, 0) == C

    # V1 is exactly U1 after an invertible row operation.
    corrected_v1 = sp.simplify(
        arc_planes[1].row(0) + arc[a] * arc[f] * arc_planes[1].row(1)
    )
    assert sp.simplify(corrected_v1 - w / P) == sp.zeros(1, 4)

    # V2 -> U0 after removing its A component and rescaling.
    j_arc = arc[f] + arc[b] * arc[psi] ** 2
    corrected_v2 = sp.simplify(
        arc_planes[2].row(0) + arc[a] * j_arc * arc_planes[2].row(1)
    )
    scaled_v2 = sp.simplify(P**2 * t**2 * corrected_v2)
    expected_v2 = z + t**2 * (-(P**2) * C + P * B + P * phi * D)
    assert sp.simplify(scaled_v2 - expected_v2) == sp.zeros(1, 4)
    assert sp.simplify(scaled_v2.subs(t, 0) - z) == sp.zeros(1, 4)

    # V3 is exactly U2.
    assert arc_planes[3] == target[2]

    # The projective kernel rows converge to the target marking.
    kernel_v1 = sp.simplify(t * arc_planes[1].row(0))
    assert kernel_v1.subs(t, 0) == -(q / P) * A
    kernel_v2 = sp.simplify(t**3 * arc_planes[2].row(0))
    assert kernel_v2.subs(t, 0) == -(q * phi**2 / P**2) * A

    print("verified target pure identity and complete 433333 relation word")
    print("verified component-eight pure family and exact valuative equation")
    print("verified mode order (V2,V1,V3,V0) and all marked limits")


if __name__ == "__main__":
    main()
