#!/usr/bin/env python3
"""Verify the complete mixed-endpoint star-(1,1,1) classification."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MIXED_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md"
OVERLAPPING = ROOT / "P4_OVERLAPPING_MIXED_ORIENTATION_PROJECTIVE_EXHAUSTION.md"
DISJOINT = ROOT / "P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md"
CYCLIC_SINGLETON = ROOT / "P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_ONE_BOUNDARY.md"
ONE_KERNEL_TRIANGLE = ROOT / "P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
QUADRATIC_WORDS = tuple(itertools.combinations(range(4), 2))


def permanent(vectors: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(vectors[mode][permutation[mode]] for mode in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent(tuple(planes[mode].row(word[mode]).T for mode in range(4)))
        for word in WORDS
    }


def product_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            u = left.row(left_row)
            v = right.row(right_row)
            columns.append(
                sp.Matrix(
                    [sp.expand(u[i] * v[j] + u[j] * v[i]) for i, j in QUADRATIC_WORDS]
                )
            )
    return sp.Matrix.hstack(*columns)


def pair_profile(planes: tuple[sp.Matrix, ...]) -> tuple[int, ...]:
    return tuple(product_matrix(planes[i], planes[j]).rank() for i, j in PAIRS)


def normal_form(
    a: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
    d: sp.Expr,
    f: sp.Expr,
    g: sp.Expr,
    h: sp.Expr,
    j: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    A = sp.Matrix([1, 1, 0, 0])
    C = sp.Matrix([1, -1, 0, 0])
    E2 = sp.Matrix([0, 0, 1, 0])
    E3 = sp.Matrix([0, 0, 0, 1])
    return (
        sp.Matrix.vstack(E2.T, (a * A + b * C + E3).T),
        sp.Matrix.vstack((c * C + f * E2 + g * E3).T, A.T),
        sp.Matrix.vstack((d * C + h * E2 + j * E3).T, A.T),
        sp.Matrix.vstack(C.T, E2.T),
    )


def squarefree_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in QUADRATIC_WORDS]
    )


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "endpoint-indegree signature `(2,1,0,0)`" in theorem
    assert "UNRESOLVED" in theorem
    assert "complete" in OVERLAPPING.read_text(encoding="utf-8").lower()
    assert "Every nonzero pure" in DISJOINT.read_text(encoding="utf-8")
    assert "components 16 and 17" in CYCLIC_SINGLETON.read_text(encoding="utf-8")
    one_kernel_text = " ".join(ONE_KERNEL_TRIANGLE.read_text(encoding="utf-8").split())
    assert "exactly-one-kernel stratum is now exhausted" in one_kernel_text

    a, b, c, d, f, g, h, j = sp.symbols("a b c d f g h j")
    planes = normal_form(a, b, c, d, f, g, h, j)
    tensor = coefficients(planes)
    expected = {
        (0, 0, 0, 0): -2 * (c * j + d * g),
        (1, 0, 0, 0): -2 * (b * f * j + b * g * h + c * h + d * f),
        (1, 0, 0, 1): -2 * (b * c * j + b * d * g + c * d),
        (1, 0, 1, 1): 2 * a * g,
        (1, 1, 0, 1): 2 * a * j,
        (1, 1, 1, 1): sp.Integer(2),
    }
    assert all(sp.expand(tensor[word] - expected.get(word, 0)) == 0 for word in WORDS)

    # The a != 0 survivor and the asymmetric c=0,d!=0 branch are lower-pair.
    a_branch = normal_form(1, b, 0, 0, f, 0, h, 0)
    assert product_matrix(a_branch[1], a_branch[3]).rank() == 2
    asymmetric = normal_form(0, b, 0, -b * j, f, 0, h, j)
    assert product_matrix(asymmetric[1], asymmetric[3]).rank() == 2

    # On b=0, modes (0,1,3) form the support-one cyclic triangle.
    loop_branch = normal_form(0, 0, 0, 0, f, g, h, j)
    E2 = sp.Matrix([0, 0, 1, 0])
    E3 = sp.Matrix([0, 0, 0, 1])
    A = sp.Matrix([1, 1, 0, 0])
    C = sp.Matrix([1, -1, 0, 0])
    assert squarefree_product(E2, E2) == sp.zeros(6, 1)
    assert squarefree_product(g * E3 - f * E2, f * E2 + g * E3) == sp.zeros(6, 1)
    assert squarefree_product(A, C) == sp.zeros(6, 1)
    loop_sample = tuple(plane.subs({f: 1, g: 2, h: 3, j: 4}) for plane in loop_branch)
    assert pair_profile(loop_sample) == (3, 3, 3, 4, 3, 3)

    # On b != 0, fj+gh=0 gives the exactly-one-kernel triangle on (1,2,3).
    polar_branch = normal_form(0, b, 0, 0, f, g, -f * j / g, j)
    assert squarefree_product(
        polar_branch[1].row(0).T, polar_branch[2].row(0).T
    ) == sp.zeros(6, 1)
    assert squarefree_product(
        polar_branch[1].row(1).T, polar_branch[3].row(0).T
    ) == sp.zeros(6, 1)
    assert squarefree_product(
        polar_branch[2].row(1).T, polar_branch[3].row(0).T
    ) == sp.zeros(6, 1)
    polar_sample = tuple(plane.subs({b: 2, f: 1, g: 2, j: 3}) for plane in polar_branch)
    assert pair_profile(polar_sample) == (4, 4, 3, 3, 3, 3)
    for left, right in ((1, 2), (1, 3), (2, 3)):
        matrix = product_matrix(polar_sample[left], polar_sample[right])
        assert matrix.rank() == 3
        relation = sp.Matrix(2, 2, tuple(matrix.nullspace()[0]))
        assert relation.rank() == 1

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation": "mixed endpoint star-(1,1,1)",
                "endpoint_indegree_signature": [2, 1, 0, 0],
                "singleton_branch_profiles": {
                    "cyclic_support_one": pair_profile(loop_sample),
                    "one_kernel_triangle": pair_profile(polar_sample),
                },
                "orientation_complete": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
