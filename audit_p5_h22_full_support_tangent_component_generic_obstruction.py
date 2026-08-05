#!/usr/bin/env python3
"""Independent F_7 audit of the component-fourteen H22 obstruction."""

from __future__ import annotations

import itertools
import json

from audit_p5_h22_directed_zero_divisor_triangle_components_generic_obstruction import (
    PRIME,
    SLOPES,
    dot,
    genuine_data,
    linear_combination,
    marked_map,
    projective_vectors,
    rank,
    shifted,
)


PARAMETERS = (3, 6)


def normalized_bases():
    p, q = PARAMETERS
    e = (1, 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, p, q)
    s1 = (1 - p, 1 + q, -p - q, 0)
    s2 = (1 - q, 1 + p, 0, -p - q)
    cap_s = p + q + 1
    alpha = (
        e,
        e,
        tuple(cap_s * e[index] - u[index] for index in range(4)),
        tuple(
            (q - 1) * s1[index] - (p - 1) * s2[index]
            for index in range(4)
        ),
    )
    beta = (w, w, e, s1)
    return (
        tuple(tuple(entry % PRIME for entry in row) for row in alpha),
        tuple(tuple(entry % PRIME for entry in row) for row in beta),
    )


def marking_union(alpha, canonical_beta, direction):
    points = set()
    counts = {}
    for slope in SLOPES:
        slope_points = set()
        for shifts in itertools.product(range(PRIME), repeat=4):
            beta = shifted(alpha, canonical_beta, shifts)
            genuine, _, _, _ = genuine_data(alpha, beta, direction, slope)
            if genuine:
                slope_points.add(shifts)
        counts[str(slope)] = len(slope_points)
        points.update(slope_points)
    return points, counts


def main():
    alpha, canonical_beta = normalized_bases()
    d01_points, d01_counts = marking_union(alpha, canonical_beta, "01")
    d23_points, d23_counts = marking_union(alpha, canonical_beta, "23")
    common = d01_points & d23_points

    p, q = PARAMETERS
    cap_p = (p + q) % PRIME
    cap_s = (cap_p + 1) % PRIME
    k = (
        q
        * pow(((p - q) * (cap_p - 1)) % PRIME, -1, PRIME)
        % PRIME
    )
    expected_common = {
        (h, 0, 0, k) for h in range(PRIME)
    } | {
        (0, h, 0, k) for h in range(PRIME)
    }
    assert common <= expected_common

    genuine_d01_marking_slopes = 0
    genuine_extensions = 0
    infinity_extensions = 0
    for shifts in common:
        beta = shifted(alpha, canonical_beta, shifts)
        for slope in SLOPES:
            genuine, kernel, diagonal_a, diagonal_b = genuine_data(
                alpha, beta, "01", slope
            )
            if not genuine:
                continue
            genuine_d01_marking_slopes += 1
            for projective in projective_vectors(len(kernel)):
                extension = linear_combination(projective, kernel)
                if not dot(diagonal_a, extension) or not dot(diagonal_b, extension):
                    continue
                genuine_extensions += 1
                if slope == "inf":
                    infinity_extensions += 1
                ranks = tuple(
                    rank(
                        marked_map(
                            alpha,
                            beta,
                            "01",
                            slope,
                            extension,
                            marked_mode,
                        )
                    )
                    for marked_mode in range(4)
                )
                assert max(ranks) == 4

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "F_7",
                "component_parameters": {"p": p, "q": q},
                "projective_slopes": [str(slope) for slope in SLOPES],
                "D01_marking_counts": d01_counts,
                "D23_marking_counts": d23_counts,
                "common_markings": len(common),
                "common_marking_closure_size": 2 * PRIME - 1,
                "genuine_D01_marking_slope_pairs": genuine_d01_marking_slopes,
                "genuine_projective_extensions": genuine_extensions,
                "infinity_projective_extensions": infinity_extensions,
                "every_extension_has_a_rank_four_marked_map": True,
                "role": "independent corroboration, not the characteristic-zero proof",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
