#!/usr/bin/env python3
"""Independent F_7 audit of the component-fifteen H22 obstruction."""

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


PARAMETERS = (2, 2, 3)


def normalized_bases():
    p, q, rho = PARAMETERS
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    ell = tuple(a[index] + b_bar[index] for index in range(4))
    ell_bar = tuple(a[index] - b_bar[index] for index in range(4))
    k = tuple(a_bar[index] + p * b[index] for index in range(4))
    k_bar = tuple(b[index] + q * a_bar[index] for index in range(4))
    other = tuple(ell_bar[index] + rho * a_bar[index] for index in range(4))
    alpha_3 = tuple(
        p * rho * k_bar[index] - (p * q + 1) * other[index]
        for index in range(4)
    )
    alpha = (a, b_bar, ell, alpha_3)
    beta = (b, a_bar, k, k_bar)
    return (
        tuple(tuple(entry % PRIME for entry in row) for row in alpha),
        tuple(tuple(entry % PRIME for entry in row) for row in beta),
    )


def main():
    alpha, canonical_beta = normalized_bases()
    p, q, rho = PARAMETERS
    expected_point = (
        0,
        0,
        (p * q + 1) * pow(rho, -1, PRIME) % PRIME,
        0,
    )
    observed = {}
    marking_slope_pairs = []
    extension_count = 0
    infinity_extensions = 0
    rank_profiles = set()
    for slope in SLOPES:
        observed[slope] = set()
        for shifts in itertools.product(range(PRIME), repeat=4):
            beta = shifted(alpha, canonical_beta, shifts)
            genuine, _, _, _ = genuine_data(alpha, beta, "01", slope)
            if genuine:
                observed[slope].add(shifts)
        expected = set() if slope in (-1 % PRIME, 1) else {expected_point}
        assert observed[slope] == expected
        for shifts in observed[slope]:
            marking_slope_pairs.append((slope, shifts))
            beta = shifted(alpha, canonical_beta, shifts)
            genuine, kernel, diagonal_a, diagonal_b = genuine_data(
                alpha, beta, "01", slope
            )
            assert genuine
            assert len(kernel) == 2
            for projective in projective_vectors(2):
                extension = linear_combination(projective, kernel)
                if not dot(diagonal_a, extension) or not dot(diagonal_b, extension):
                    continue
                extension_count += 1
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
                rank_profiles.add(ranks)
                assert max(ranks) == 4

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "F_7",
                "component_parameters": {"p": p, "q": q, "rho": rho},
                "projective_slopes": [str(slope) for slope in SLOPES],
                "D01_marking_counts": {
                    str(slope): len(points) for slope, points in observed.items()
                },
                "common_marking_point": list(expected_point),
                "genuine_marking_slope_pairs": len(marking_slope_pairs),
                "genuine_projective_extensions": extension_count,
                "infinity_projective_extensions": infinity_extensions,
                "observed_marked_rank_profiles": [
                    list(profile) for profile in sorted(rank_profiles)
                ],
                "every_extension_has_a_rank_four_marked_map": True,
                "role": "independent corroboration, not the characteristic-zero proof",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
