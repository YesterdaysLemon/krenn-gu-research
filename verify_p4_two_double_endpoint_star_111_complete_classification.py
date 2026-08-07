#!/usr/bin/env python3
"""Verify the complete two-double-endpoint star-(1,1,1) classification."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
COMP18 = ROOT / "P4_COMMON_SINGLETON_COMPONENT.md"
COMP21 = ROOT / "P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md"
MIXED_CHAIN = ROOT / "P4_MIXED_CHAIN_TRANSVERSE_COMPONENT_INCLUSION.md"
TRIPLE_KERNEL = ROOT / "claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def tensor(y, x):
    return {
        bits: sp.factor(permanent(tuple(x[i] if bits[i] else y[i] for i in range(4))))
        for bits in WORDS
    }


def product(left, right):
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in SOURCE_PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(
            product(left.row(i), right.row(j))
            for i, j in itertools.product(range(2), repeat=2)
        )
    )


def profile(planes):
    return tuple(pair_matrix(planes[i], planes[j]).rank() for i, j in PAIRS)


def plucker(plane):
    return sp.Matrix([plane[:, pair].det() for pair in SOURCE_PAIRS])


def proportional(left, right):
    return sp.Matrix.hstack(left, right).rank() == 1


def support(t):
    return {bits: value for bits, value in t.items() if value != 0}


def main():
    assert "eighteenth pure" in COMP18.read_text(encoding="utf-8")
    assert "component twenty-one" in COMP21.read_text(encoding="utf-8")
    assert "boundary of component eight" in MIXED_CHAIN.read_text(encoding="utf-8")
    assert "components sixteen or eighteen" in TRIPLE_KERNEL.read_text(encoding="utf-8")

    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    e0 = sp.Matrix((1, 0, 0, 0))
    e1 = sp.Matrix((0, 1, 0, 0))
    e2 = sp.Matrix((0, 0, 1, 0))
    e3 = sp.Matrix((0, 0, 0, 1))
    zero6 = sp.zeros(6, 1)
    assert product(A, C) == zero6 and product(B, D) == zero6

    # I, singleton: the coefficient ledger is exactly the component-18
    # ternary orthogonality system.
    av = sp.symbols("a1:4")
    bv = sp.symbols("b1:4")
    cv = sp.symbols("c1:4")
    q0, q1, q2, q3 = sp.symbols("q0:4")
    xs = (sp.Matrix((0, *av)), sp.Matrix((0, *bv)), sp.Matrix((0, *cv)), e0)
    ys = (e0, e0, e0, sp.Matrix((q0, q1, q2, q3)))
    singleton_center = tensor(ys, xs)
    singleton_support = support(singleton_center)
    assert set(singleton_support) == {
        (0, 1, 1, 0),
        (1, 0, 1, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 0),
        (1, 1, 1, 1),
    }
    assert (
        sp.factor(singleton_center[(1, 1, 1, 0)] - q0 * singleton_center[(1, 1, 1, 1)])
        == 0
    )

    # I, binary: reconstruct equations (6)--(8), then the component-21
    # projective placement.
    a0, b0, d0, a1, b1, d1, a2, b2, d2, p, c, q, r = sp.symbols(
        "a0 b0 d0 a1 b1 d1 a2 b2 d2 p c q r"
    )
    y = (A, C, C, p * A + c * C + q * B + r * D)
    x = (
        a0 * C + b0 * B + d0 * D,
        a1 * A + b1 * B + d1 * D,
        a2 * A + b2 * B + d2 * D,
        C,
    )
    center_binary = tensor(y, x)
    expected_center = {
        (0, 1, 1, 0): 4
        * (
            a1 * b2 * q
            - a1 * d2 * r
            + a2 * b1 * q
            - a2 * d1 * r
            + (b1 * b2 - d1 * d2) * p
        ),
        (1, 0, 0, 0): -4 * (b0 * q - d0 * r),
        (1, 0, 1, 0): -4 * (a0 * (b2 * q - d2 * r) + c * (b0 * b2 - d0 * d2)),
        (1, 0, 1, 1): -4 * (b0 * b2 - d0 * d2),
        (1, 1, 0, 0): -4 * (a0 * (b1 * q - d1 * r) + c * (b0 * b1 - d0 * d1)),
        (1, 1, 0, 1): -4 * (b0 * b1 - d0 * d1),
        (1, 1, 1, 0): 4
        * (
            -a0 * c * (b1 * b2 - d1 * d2)
            + a1 * a2 * (b0 * q - d0 * r)
            + p * (a1 * (b0 * b2 - d0 * d2) + a2 * (b0 * b1 - d0 * d1))
        ),
        (1, 1, 1, 1): -4 * a0 * (b1 * b2 - d1 * d2),
    }
    assert set(support(center_binary)) == set(expected_center)
    assert all(
        sp.factor(center_binary[word] - value) == 0
        for word, value in expected_center.items()
    )

    k1, k2 = sp.symbols("k1 k2")
    normalized21 = (
        sp.Matrix.vstack(A.T, C.T),
        sp.Matrix.vstack(C.T, (B + k1 * A).T),
        sp.Matrix.vstack(C.T, (B + k2 * A).T),
        sp.Matrix.vstack(D.T, C.T),
    )
    component21 = (
        sp.Matrix.vstack((A + B / k2).T, C.T),
        sp.Matrix.vstack(A.T, C.T),
        sp.Matrix.vstack(C.T, (B + k1 * A).T),
        sp.Matrix.vstack(C.T, D.T),
    )
    for left, right in zip(
        normalized21, (component21[1], component21[2], component21[0], component21[3])
    ):
        assert proportional(plucker(left), plucker(right))
    t = sp.symbols("t", nonzero=True)
    endpoint_arc = sp.Matrix((1, 0, -1 / t))  # (A^C,A^B,C^B) for p=1/t,q=0
    assert sp.simplify(t * endpoint_arc).subs(t, 0) == sp.Matrix((0, 0, -1))

    # II, equal binary support: active coefficient is a forbidden multiple.
    a1, b1, d1, a2, b2, d2, a3, b3, d3 = sp.symbols("a1 b1 d1 a2 b2 d2 a3 b3 d3")
    same = tensor(
        (A, C, C, A),
        (
            C,
            a1 * A + b1 * B + d1 * D,
            a2 * A + b2 * B + d2 * D,
            a3 * C + b3 * B + d3 * D,
        ),
    )
    assert sp.factor(same[(1, 1, 1, 1)] + a3 * same[(0, 1, 1, 0)]) == 0

    # II, adjacent binary support.  Verify the exact case-split identities.
    E02 = sp.Matrix((1, 0, 1, 0))
    F02 = sp.Matrix((1, 0, -1, 0))
    alpha, beta, delta = sp.symbols("alpha beta delta")
    adjacent = tensor(
        (A, C, C, F02),
        (
            E02,
            a1 * A + b1 * B + d1 * D,
            a2 * A + b2 * B + d2 * D,
            alpha * E02 + beta * e1 + delta * e3,
        ),
    )
    X = a1 * (b2 - d2) + a2 * (b1 - d1)
    E = b1 * b2 - d1 * d2
    reduced_anchor = sp.factor(adjacent[(1, 1, 1, 1)].subs(delta, 0))
    assert sp.factor(adjacent[(0, 1, 1, 0)] + 2 * (X - E)) == 0
    assert adjacent[(1, 0, 0, 1)] == -2 * delta
    assert (
        sp.factor(
            adjacent[(1, 0, 1, 1)].subs(delta, 0) - (b2 - d2) * (beta - 2 * alpha)
        )
        == 0
    )
    assert (
        sp.factor(
            adjacent[(1, 1, 0, 1)].subs(delta, 0) - (b1 - d1) * (beta - 2 * alpha)
        )
        == 0
    )
    assert sp.factor(reduced_anchor - ((2 * alpha + beta) * X + 2 * beta * E)) == 0

    # II, singleton on and off the original binary label.
    u1, v1, w1, u2, v2, w2, c1, c2, c3 = sp.symbols("u1 v1 w1 u2 v2 w2 c1 c2 c3")
    inside = tensor(
        (A, C, C, e0),
        (
            e0,
            u1 * A + v1 * B + w1 * D,
            u2 * A + v2 * B + w2 * D,
            sp.Matrix((0, c1, c2, c3)),
        ),
    )
    Ein = v1 * v2 - w1 * w2
    assert sp.factor(inside[(0, 1, 1, 0)] - 2 * Ein) == 0
    assert sp.factor(inside[(1, 1, 1, 1)] - inside[(0, 1, 1, 1)] / 2 - c1 * Ein) == 0
    outside = tensor(
        (A, C, C, e2),
        (
            e2,
            u1 * A + v1 * B + w1 * D,
            u2 * A + v2 * B + w2 * D,
            sp.Matrix((c1, c2, 0, c3)),
        ),
    )
    Xout = u1 * (v2 - w2) + u2 * (v1 - w1)
    assert outside[(1, 0, 0, 1)] == -2 * c3
    assert sp.factor(outside[(0, 1, 1, 0)] - 2 * Xout) == 0
    assert sp.factor(outside[(1, 1, 1, 1)].subs(c3, 0) - (c1 + c2) * Xout) == 0

    # II, disjoint binary support: exact survivor equations and mixed-chain
    # triangle.  Its generic sample has the 333433 profile (unique full edge
    # 12), and the projective nontransverse endpoint is lower-pair.
    alpha3, gamma3, epsilon3 = sp.symbols("alpha3 gamma3 epsilon3")
    disjoint = tensor(
        (A, C, C, D),
        (
            B,
            a1 * A + b1 * B + d1 * D,
            a2 * A + b2 * B + d2 * D,
            alpha3 * A + gamma3 * C + epsilon3 * B,
        ),
    )
    assert disjoint[(1, 0, 0, 1)] == -4 * epsilon3
    assert sp.factor(disjoint[(1, 0, 1, 1)].subs(epsilon3, 0) + 4 * b2 * gamma3) == 0
    assert sp.factor(disjoint[(1, 1, 0, 1)].subs(epsilon3, 0) + 4 * b1 * gamma3) == 0
    assert sp.factor(disjoint[(0, 1, 1, 0)] + 4 * (a1 * d2 + a2 * d1)) == 0
    assert (
        sp.factor(
            disjoint[(0, 1, 1, 1)].subs({epsilon3: 0, gamma3: 0})
            - 4 * alpha3 * (b1 * b2 - d1 * d2)
        )
        == 0
    )
    assert (
        sp.factor(
            disjoint[(1, 1, 1, 1)].subs({epsilon3: 0, gamma3: 0})
            - 4 * alpha3 * (a1 * b2 + a2 * b1)
        )
        == 0
    )

    disjoint_sample = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack(C.T, (A + 2 * B + D).T),
        sp.Matrix.vstack(C.T, (A - sp.Rational(1, 2) * B - D).T),
        sp.Matrix.vstack(D.T, A.T),
    )
    assert profile(disjoint_sample) == (3, 3, 3, 4, 3, 3)
    for edge, relation in {
        (0, 1): (1, 0, 0, 0),
        (0, 2): (1, 0, 0, 0),
        (0, 3): (0, 0, 1, 0),
        (1, 3): (0, 1, 0, 0),
        (2, 3): (0, 1, 0, 0),
    }.items():
        assert (
            pair_matrix(disjoint_sample[edge[0]], disjoint_sample[edge[1]])
            * sp.Matrix(relation)
            == zero6
        )
    lower_endpoint = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack(C.T, A.T),
        sp.Matrix.vstack(C.T, B.T),
        sp.Matrix.vstack(D.T, A.T),
    )
    assert profile(lower_endpoint)[-1] == 2

    # Singleton double support, reverse singleton and incident-binary supports.
    aa1, bb1, cc1, aa2, bb2, cc2 = sp.symbols("aa1 bb1 cc1 aa2 bb2 cc2")
    qx, qz, qw = sp.symbols("qx qz qw")
    rev_singleton = tensor(
        (e0, e0, e0, e1),
        (
            e1,
            sp.Matrix((0, aa1, bb1, cc1)),
            sp.Matrix((0, aa2, bb2, cc2)),
            sp.Matrix((qx, 0, qz, qw)),
        ),
    )
    assert (
        sp.factor(rev_singleton[(1, 1, 1, 1)] - qx * rev_singleton[(0, 1, 1, 0)]) == 0
    )
    rev_incident = tensor(
        (e0, e0, e0, C),
        (
            A,
            sp.Matrix((0, aa1, bb1, cc1)),
            sp.Matrix((0, aa2, bb2, cc2)),
            qx * A + qz * e2 + qw * e3,
        ),
    )
    assert (
        sp.factor(
            rev_incident[(1, 1, 1, 1)]
            - rev_incident[(0, 1, 1, 1)]
            + qx * rev_incident[(0, 1, 1, 0)]
        )
        == 0
    )

    # Singleton double support with disjoint binary reverse pair.  Verify the
    # coefficient reduction and both triple-kernel placements.
    E12 = e1 + e2
    F12 = e1 - e2
    alpha, gamma, qzero = sp.symbols("alpha gamma qzero")
    singleton_disjoint = tensor(
        (e0, e0, e0, F12),
        (
            E12,
            sp.Matrix((0, aa1, bb1, cc1)),
            sp.Matrix((0, aa2, bb2, cc2)),
            qzero * e0 + alpha * E12 + gamma * e3,
        ),
    )
    H = (aa1 + bb1) * cc2 + (aa2 + bb2) * cc1
    assert sp.factor(singleton_disjoint[(1, 1, 1, 1)] - qzero * H) == 0
    assert (
        sp.factor(
            singleton_disjoint[(1, 0, 1, 1)] - ((aa2 + bb2) * gamma + 2 * alpha * cc2)
        )
        == 0
    )
    assert (
        sp.factor(
            singleton_disjoint[(1, 1, 0, 1)] - ((aa1 + bb1) * gamma + 2 * alpha * cc1)
        )
        == 0
    )
    component16_sample = (
        sp.Matrix.vstack(e0.T, E12.T),
        sp.Matrix.vstack(e0.T, (e2 - e3).T),
        sp.Matrix.vstack(e0.T, (e1 - e3).T),
        sp.Matrix.vstack(F12.T, (e0 + E12 + 2 * e3).T),
    )
    assert profile(component16_sample) == (3, 3, 3, 3, 4, 4)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        matrix = pair_matrix(component16_sample[i], component16_sample[j])
        assert matrix.rank() == 3 and matrix * sp.Matrix((1, 0, 0, 0)) == zero6

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation": "star-(1,1,1) with exactly two kernel-kernel spokes",
                "placements": {
                    "center_singleton": 18,
                    "center_binary": 21,
                    "reverse_disjoint_binary": 8,
                    "reverse_singleton_double_disjoint_third": [16, 18],
                },
                "empty_reverse_supports": [
                    "equal binary",
                    "adjacent binary",
                    "singleton on binary label",
                    "singleton outside binary label",
                    "singleton third over singleton double support",
                    "incident binary third over singleton double support",
                ],
                "orientation_complete": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
