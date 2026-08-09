#!/usr/bin/env python3
"""Verify the support-one boundary of cyclic rank-one P4 triangles."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PERMUTATIONS = tuple(itertools.permutations(range(4)))
SOURCE_PERMUTATIONS = PERMUTATIONS
PAIRS = tuple(itertools.combinations(range(4), 2))
SOURCE_LABELS = tuple((i,) for i in range(4)) + PAIRS


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def cubic(rows):
    identity = sp.eye(4)
    return sp.Matrix(
        [[permanent((identity.row(coordinate), *rows)) for coordinate in range(4)]]
    )


def factors(label, gain):
    identity = sp.eye(4)
    if len(label) == 1:
        row = identity.row(label[0])
        return row, row
    left, right = label
    return identity.row(left) + gain * identity.row(right), identity.row(left) - gain * identity.row(right)


def leaves(ordered_labels, gains):
    (u1, v1), (u2, v2), (u3, v3) = (
        factors(label, gain) for label, gain in zip(ordered_labels, gains, strict=True)
    )
    return (
        sp.Matrix.vstack(u1, u3),
        sp.Matrix.vstack(u2, v1),
        sp.Matrix.vstack(v3, v2),
    ), cubic((u1, u2, v3)), cubic((u3, v1, v2))


def canonical_support_multiset(labels):
    representatives = []
    for permutation in SOURCE_PERMUTATIONS:
        image = [tuple(sorted(permutation[index] for index in label)) for label in labels]
        representatives.append(tuple(sorted(image)))
    return min(representatives)


def pluecker(plane):
    return sp.Matrix([plane[:, pair].det() for pair in PAIRS])


def source_degrees(labels):
    degrees = [0, 0, 0, 0]
    for left, right in labels:
        degrees[left] += 1
        degrees[right] += 1
    return tuple(sorted(degrees, reverse=True))


def main() -> None:
    gains = sp.symbols("lambda1 lambda2 lambda3", nonzero=True)
    support_orbits = sorted(
        {
            canonical_support_multiset(labels)
            for labels in itertools.combinations_with_replacement(SOURCE_LABELS, 3)
            if any(len(label) == 1 for label in labels)
        },
        key=str,
    )
    assert len(support_orbits) == 14

    surviving_orbits = set()
    survivor_order_counts = {}
    for support_orbit in support_orbits:
        viable_orders = 0
        for ordered_labels in set(itertools.permutations(support_orbit)):
            planes, kernel_cubic, active_cubic = leaves(ordered_labels, gains)
            if any(plane.rank() < 2 for plane in planes):
                continue
            pair_ranks = tuple(
                pair_matrix(planes[left], planes[right]).rank()
                for left, right in ((0, 1), (0, 2), (1, 2))
            )
            if min(pair_ranks) < 3:
                continue
            wedges = tuple(
                sp.expand(
                    kernel_cubic[0, left] * active_cubic[0, right]
                    - kernel_cubic[0, right] * active_cubic[0, left]
                )
                for left, right in PAIRS
            )
            if any(active_cubic) and any(wedge != 0 for wedge in wedges):
                viable_orders += 1
        if viable_orders:
            surviving_orbits.add(support_orbit)
            survivor_order_counts[str(support_orbit)] = viable_orders

    expected_orbits = {
        ((0,), (0, 1), (2, 3)),
        ((0,), (1, 2), (1, 3)),
        ((0,), (1,), (2, 3)),
    }
    assert surviving_orbits == expected_orbits
    assert set(survivor_order_counts.values()) == {6}

    lambda_1, lambda_2, lambda_3 = gains
    expected_cubics = {
        ((0,), (0, 1), (2, 3)): (
            sp.Matrix([[0, 0, -lambda_2 * lambda_3, lambda_2]]),
            sp.Matrix([[0, 0, -lambda_2 * lambda_3, -lambda_2]]),
        ),
        ((0,), (1, 2), (1, 3)): (
            sp.Matrix([[0, -lambda_2 * lambda_3, -lambda_3, lambda_2]]),
            sp.Matrix([[0, -lambda_2 * lambda_3, lambda_3, -lambda_2]]),
        ),
        ((0,), (1,), (2, 3)): (
            sp.Matrix([[0, 0, -lambda_3, 1]]),
            sp.Matrix([[0, 0, lambda_3, 1]]),
        ),
    }
    for labels, expected in expected_cubics.items():
        planes, kernel_cubic, active_cubic = leaves(labels, gains)
        assert (kernel_cubic, active_cubic) == expected
        assert tuple(
            pair_matrix(planes[left], planes[right]).rank()
            for left, right in ((0, 1), (0, 2), (1, 2))
        ) == (3, 3, 3)

    # Lift the singleton labels to genuine binary edges.  For epsilon != 0
    # the three support graphs are respectively path, star, path.
    epsilon, kappa, eta = sp.symbols("epsilon kappa eta", nonzero=True)
    arcs = (
        (
            ((0, 2), (0, 1), (2, 3)),
            (epsilon * kappa, lambda_2, lambda_3),
            ((0,), (0, 1), (2, 3)),
            (lambda_1, lambda_2, lambda_3),
            (2, 2, 1, 1),
            17,
        ),
        (
            ((0, 1), (1, 2), (1, 3)),
            (epsilon * kappa, lambda_2, lambda_3),
            ((0,), (1, 2), (1, 3)),
            (lambda_1, lambda_2, lambda_3),
            (3, 1, 1, 1),
            16,
        ),
        (
            ((0, 2), (1, 3), (2, 3)),
            (epsilon * kappa, epsilon * eta, lambda_3),
            ((0,), (1,), (2, 3)),
            (lambda_1, lambda_2, lambda_3),
            (2, 2, 1, 1),
            17,
        ),
    )
    containing_components = []
    for lifted_labels, lifted_gains, target_labels, target_gains, degrees, component in arcs:
        lifted_planes, lifted_kernel, lifted_active = leaves(lifted_labels, lifted_gains)
        target_planes, target_kernel, target_active = leaves(target_labels, target_gains)
        assert source_degrees(lifted_labels) == degrees
        assert all(
            pluecker(lifted).subs(epsilon, 0) == pluecker(target)
            for lifted, target in zip(lifted_planes, target_planes, strict=True)
        )
        assert lifted_kernel.subs(epsilon, 0) == target_kernel
        assert lifted_active.subs(epsilon, 0) == target_active
        containing_components.append(component)

    # Exact apolar lifting lemma.  If w is in ker(C(0)), correcting it in a
    # pivot direction produces w(epsilon) in ker(C(epsilon)) with the same
    # limit.  This lifts every target opposite plane, not only one sample.
    c0, c1, c2, c3, t = sp.symbols("c0 c1 c2 c3 t", nonzero=True)
    moving_covector = sp.Matrix([[c0 + epsilon * t, c1, c2, c3]])
    w1, w2, w3 = sp.symbols("w1 w2 w3")
    target_row = sp.Matrix([[-(c1 * w1 + c2 * w2 + c3 * w3) / c0, w1, w2, w3]])
    correction = (moving_covector * target_row.T)[0] / moving_covector[0, 0]
    lifted_row = target_row - correction * sp.Matrix([[1, 0, 0, 0]])
    assert sp.simplify((moving_covector * lifted_row.T)[0]) == 0
    assert sp.simplify(lifted_row.subs(epsilon, 0) - target_row) == sp.zeros(1, 4)

    print(
        json.dumps(
            {
                "status": "pass",
                "support_orbits_with_a_singleton": len(support_orbits),
                "nonzero_rank_three_orbits": [str(orbit) for orbit in sorted(surviving_orbits, key=str)],
                "punctured_support_types": ["path", "star", "path"],
                "containing_components": containing_components,
                "apolar_plane_lift": "symbolic pivot correction",
                "parameter_search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
