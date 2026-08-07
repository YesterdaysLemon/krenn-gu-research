#!/usr/bin/env python3
"""Verify the support classification of cyclic rank-one P4 triangles."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))
SIGNS = tuple(itertools.product((1, -1), repeat=3))


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def root(edge, sign) -> sp.Matrix:
    vector = [0, 0, 0, 0]
    vector[edge[0]] = 1
    vector[edge[1]] = sign
    return sp.Matrix([vector])


def directed_triangle(labels, signs):
    positive = tuple(root(edge, sign) for edge, sign in zip(labels, signs, strict=True))
    negative = tuple(root(edge, -sign) for edge, sign in zip(labels, signs, strict=True))
    # Label order is 12, 13, 23.  Row order is (kernel, active).
    return (
        sp.Matrix.vstack(positive[0], positive[1]),
        sp.Matrix.vstack(positive[2], negative[0]),
        sp.Matrix.vstack(negative[1], negative[2]),
    )


def triple_covectors(planes):
    identity = sp.eye(4)
    return {
        bits: sp.Matrix(
            [[
                permanent(
                    (
                        identity.row(coordinate),
                        planes[0].row(bits[0]),
                        planes[1].row(bits[1]),
                        planes[2].row(bits[2]),
                    )
                )
                for coordinate in range(4)
            ]]
        )
        for bits in itertools.product((0, 1), repeat=3)
    }


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def relation_data(planes):
    result = []
    for left, right in ((0, 1), (0, 2), (1, 2)):
        matrix = pair_matrix(planes[left], planes[right])
        result.append(
            (
                matrix.rank(),
                tuple(sp.Matrix(2, 2, tuple(vector)).rank() for vector in matrix.nullspace()),
            )
        )
    return tuple(result)


def covector_span_rank(covectors):
    return sp.Matrix.vstack(*covectors).rank()


def support_degrees(labels):
    degrees = [0, 0, 0, 0]
    for left, right in labels:
        degrees[left] += 1
        degrees[right] += 1
    return tuple(sorted(degrees, reverse=True))


def switched_signs(labels, signs, vertex_signs):
    return tuple(
        sign * vertex_signs[right] * vertex_signs[left]
        for (left, right), sign in zip(labels, signs, strict=True)
    )


def gauge_representative_exists(labels, signs, target):
    return any(
        switched_signs(labels, signs, vertex_signs) == target
        for vertex_signs in itertools.product((1, -1), repeat=4)
    )


def main() -> None:
    support_types = {
        "star": ((0, 1), (0, 2), (0, 3)),
        "path": ((0, 1), (1, 2), (2, 3)),
        "triangle": ((0, 1), (1, 2), (0, 2)),
    }
    assert support_degrees(support_types["star"]) == (3, 1, 1, 1)
    assert support_degrees(support_types["path"]) == (2, 2, 1, 1)
    assert support_degrees(support_types["triangle"]) == (2, 2, 2, 0)

    summaries = {}
    for name, labels in support_types.items():
        data = []
        for signs in SIGNS:
            planes = directed_triangle(labels, signs)
            assert all(plane.rank() == 2 for plane in planes)
            relations = relation_data(planes)
            covectors = triple_covectors(planes)
            mixed = tuple(
                covectors[bits]
                for bits in itertools.product((0, 1), repeat=3)
                if bits not in ((0, 0, 0), (1, 1, 1))
            )
            assert all(covector == sp.zeros(1, 4) for covector in mixed)
            kernel = covectors[(0, 0, 0)]
            active = covectors[(1, 1, 1)]
            data.append(
                {
                    "signs": signs,
                    "relations": relations,
                    "kernel": tuple(kernel),
                    "active": tuple(active),
                    "covector_span_rank": covector_span_rank((kernel, active)),
                }
            )

        if name in ("star", "path"):
            assert all(
                item["relations"] == ((3, (1,)), (3, (1,)), (3, (1,)))
                for item in data
            )
            assert all(item["covector_span_rank"] == 2 for item in data)
            assert all(
                gauge_representative_exists(labels, signs, (1, 1, 1))
                for signs in SIGNS
            )
        else:
            assert all(
                item["relations"] == ((2, (1, 1)), (2, (1, 1)), (2, (1, 1)))
                for item in data
            )
            assert all(item["covector_span_rank"] == 1 for item in data)
            for item in data:
                kernel_zero = item["kernel"] == (0, 0, 0, 0)
                active_zero = item["active"] == (0, 0, 0, 0)
                assert kernel_zero != active_zero
                nonzero = item["active"] if kernel_zero else item["kernel"]
                assert nonzero[:3] == (0, 0, 0)
                assert nonzero[3] in (2, -2)
            for signs in SIGNS:
                holonomy = signs[0] * signs[1] * signs[2]
                assert gauge_representative_exists(labels, signs, (1, 1, holonomy))

        summaries[name] = {
            "support_degrees": support_degrees(labels),
            "sign_sheets_checked": len(data),
            "generic_pair_ranks": tuple(item[0] for item in data[0]["relations"]),
            "covector_span_rank": data[0]["covector_span_rank"],
        }

    # Weighted support triangles carry a multiplicative cycle holonomy.
    # Purity forces nu=lambda*mu; on that divisor every pair rank is two.
    lam, mu, nu = sp.symbols("lambda mu nu", nonzero=True)
    weighted_triangle = (
        sp.Matrix(((1, lam, 0, 0), (0, 1, mu, 0))),
        sp.Matrix(((1, 0, nu, 0), (1, -lam, 0, 0))),
        sp.Matrix(((0, 1, -mu, 0), (1, 0, -nu, 0))),
    )
    weighted_covectors = triple_covectors(weighted_triangle)
    assert weighted_covectors[(0, 0, 0)] == sp.Matrix([[0, 0, 0, nu - lam * mu]])
    assert weighted_covectors[(1, 1, 1)] == sp.Matrix([[0, 0, 0, -nu - lam * mu]])
    resonant_triangle = tuple(plane.subs(nu, lam * mu) for plane in weighted_triangle)
    assert tuple(item[0] for item in relation_data(resonant_triangle)) == (2, 2, 2)

    # If exactly two labels agree, a continuous ratio remains.  Adjacent
    # third support makes the kernel and escape cubics equal, so nonzero
    # purity is impossible.  A disjoint third support gives a component-eight
    # boundary and admits the explicit pure opening below.
    adjacent_repeated = (
        sp.Matrix(((1, lam, 0, 0), (1, mu, 0, 0))),
        sp.Matrix(((1, 0, nu, 0), (1, -lam, 0, 0))),
        sp.Matrix(((1, -mu, 0, 0), (1, 0, -nu, 0))),
    )
    adjacent_covectors = triple_covectors(adjacent_repeated)
    expected_adjacent = sp.Matrix([[0, 0, 0, nu * (lam - mu)]])
    assert sp.simplify(adjacent_covectors[(0, 0, 0)] - expected_adjacent) == sp.zeros(1, 4)
    assert sp.simplify(adjacent_covectors[(1, 1, 1)] - expected_adjacent) == sp.zeros(1, 4)

    disjoint_repeated = (
        sp.Matrix(((1, lam, 0, 0), (1, mu, 0, 0))),
        sp.Matrix(((0, 0, 1, nu), (1, -lam, 0, 0))),
        sp.Matrix(((1, -mu, 0, 0), (0, 0, 1, -nu))),
    )
    disjoint_covectors = triple_covectors(disjoint_repeated)
    assert sp.simplify(
        disjoint_covectors[(0, 0, 0)]
        - sp.Matrix([[0, 0, nu * (lam - mu), lam - mu]])
    ) == sp.zeros(1, 4)
    assert sp.simplify(
        disjoint_covectors[(1, 1, 1)]
        - sp.Matrix([[0, 0, nu * (lam - mu), -lam + mu]])
    ) == sp.zeros(1, 4)

    p, q, r, k = sp.symbols("p q r k")
    component_eight_opening = (
        sp.Matrix(((1, 0, p, -p), (0, 1, q, -q))),
        sp.Matrix(((1, 1, 0, 0), (1, r, 0, 0))),
        sp.Matrix(((0, 0, 1, 1), (1, -1, 0, 0))),
        sp.Matrix(((1, -r, 0, 0), (0, k, 1, -1))),
    )
    opening_tensor = {
        word: sp.factor(
            permanent(
                tuple(component_eight_opening[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in itertools.product((0, 1), repeat=4)
    }
    assert {
        word: value for word, value in opening_tensor.items() if value != 0
    } == {
        (0, 1, 1, 1): -2 * p * (r - 1),
        (1, 1, 1, 1): -2 * q * (r - 1),
    }
    boundary_sample = tuple(
        plane.subs({p: 2, q: 3, r: 2, k: 0}) for plane in component_eight_opening
    )
    open_sample = tuple(
        plane.subs({p: 2, q: 3, r: 2, k: 5}) for plane in component_eight_opening
    )
    assert tuple(
        pair_matrix(boundary_sample[left], boundary_sample[right]).rank()
        for left, right in PAIRS
    ) == (3, 4, 4, 3, 3, 3)
    assert tuple(
        pair_matrix(open_sample[left], open_sample[right]).rank()
        for left, right in PAIRS
    ) == (3, 4, 4, 3, 3, 4)

    # If all three labels agree, nondegenerate planes are the same binary
    # coordinate plane and every pair image has rank one.
    repeated_label = (0, 1)
    for sign in (1, -1):
        planes = directed_triangle(
            (repeated_label, repeated_label, repeated_label),
            (sign, -sign, sign),
        )
        assert all(plane.rank() == 2 for plane in planes)
        assert tuple(item[0] for item in relation_data(planes)) == (1, 1, 1)

    print(
        json.dumps(
            {
                "status": "pass",
                "distinct_support_types": summaries,
                "weighted_triangle_holonomy": "nu=lambda*mu forces pair profile (2,2,2)",
                "repeated_adjacent_support": "zero or degenerate",
                "repeated_disjoint_support": "component-eight boundary",
                "all_rank_three_survivors": (
                    "support star",
                    "support path",
                    "repeated-disjoint component-eight boundary",
                ),
                "containing_components": (8, 16, 17),
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
