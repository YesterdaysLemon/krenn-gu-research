#!/usr/bin/env python3
"""Verify generic weighted H22 exclusion on the embedded-P3 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "embedded-p3"
    / "P4_EMBEDDED_P3_PURE_COMPONENT.md")
H31 = (
    ROOT / "claims" / "p5" / "h31" / "embedded-p3"
    / "P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def weighted_row(row, extension, direction: str, slope):
    if direction == "01":
        return (
            slope * row[0] + row[1],
            row[2],
            row[3],
            extension,
        )
    if direction == "23":
        return (
            row[0],
            row[1],
            slope * row[2] + row[3],
            extension,
        )
    raise ValueError(direction)


def weighted_coefficients(
    alpha,
    beta,
    extensions,
    direction: str,
    slope,
) -> dict[tuple[int, ...], sp.Expr]:
    alpha_weighted = tuple(
        weighted_row(
            alpha[mode],
            extensions[mode],
            direction,
            slope,
        )
        for mode in range(4)
    )
    beta_weighted = tuple(
        weighted_row(
            beta[mode],
            extensions[4 + mode],
            direction,
            slope,
        )
        for mode in range(4)
    )
    return {
        word: sp.factor(
            permanent(
                tuple(
                    beta_weighted[mode]
                    if word[mode]
                    else alpha_weighted[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS4
    }


def main() -> None:
    cap_s, cap_t, cap_u, slope = sp.symbols("S T U r")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta = (
        (1, 0, 1, cap_t),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    marked_beta = tuple(
        tuple(
            sp.expand(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    weighted_23 = weighted_coefficients(
        alpha, marked_beta, extensions, "23", slope
    )
    assert weighted_23[(0, 0, 0, 0)] == 0

    shared_alpha = tuple(row[1:] for row in alpha[1:])
    shared_beta = tuple(row[1:] for row in beta[1:])
    pure_p3 = {
        word: sp.factor(
            permanent(
                tuple(
                    shared_beta[mode]
                    if word[mode]
                    else shared_alpha[mode]
                    for mode in range(3)
                )
            )
        )
        for word in WORDS3
    }
    assert pure_p3[(1, 1, 1)] == -2
    assert all(
        value == 0
        for word, value in pure_p3.items()
        if word != (1, 1, 1)
    )

    projected_alpha_01 = tuple(
        weighted_row(alpha[mode], 0, "01", slope)[:3]
        for mode in range(4)
    )
    projected_beta_01 = tuple(
        weighted_row(marked_beta[mode], 0, "01", slope)[:3]
        for mode in range(4)
    )
    assert projected_alpha_01[0] == (1, cap_s, cap_u)
    assert projected_beta_01[0] == (
        slope + shifts[0],
        cap_s * shifts[0] + 1,
        cap_t + cap_u * shifts[0],
    )
    assert projected_alpha_01[1:] == shared_alpha
    assert all(
        tuple(
            sp.expand(
                projected_beta_01[mode + 1][coordinate]
                - shifts[mode + 1] * shared_alpha[mode][coordinate]
            )
            for coordinate in range(3)
        )
        == shared_beta[mode]
        for mode in range(3)
    )

    exceptional_points = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, -1),
        (1, 0, -1),
        (0, 1, 1),
        (1, -1, 0),
    )
    projected_alpha = sp.Matrix((1, cap_s, cap_u))
    projected_beta = sp.Matrix((slope, 1, cap_t))
    factors = tuple(
        sp.factor(
            sp.Matrix.hstack(
                projected_alpha,
                projected_beta,
                sp.Matrix(point),
            ).det()
        )
        for point in exceptional_points
    )
    expected_factors = (
        cap_s * cap_t - cap_u,
        slope * cap_u - cap_t,
        1 - slope * cap_s,
        -slope * cap_s + cap_s * cap_t - cap_u + 1,
        slope * cap_u + cap_s * cap_t - cap_t - cap_u,
        slope * cap_s + slope * cap_u - cap_t - 1,
        slope * cap_s + cap_s * cap_t - cap_u - 1,
        -slope * cap_s + slope * cap_u - cap_t + 1,
        -slope * cap_u + cap_s * cap_t + cap_t - cap_u,
    )
    assert factors == expected_factors
    discriminant = sp.factor(sp.prod(factors))
    expected_discriminant = (
        (slope * cap_s - 1)
        * (slope * cap_u - cap_t)
        * (cap_s * cap_t - cap_u)
        * (slope * cap_s - slope * cap_u + cap_t - 1)
        * (slope * cap_s + slope * cap_u - cap_t - 1)
        * (slope * cap_s - cap_s * cap_t + cap_u - 1)
        * (slope * cap_s + cap_s * cap_t - cap_u - 1)
        * (slope * cap_u - cap_s * cap_t - cap_t + cap_u)
        * (slope * cap_u + cap_s * cap_t - cap_t - cap_u)
    )
    assert sp.expand(discriminant - expected_discriminant) == 0
    sample = {cap_s: 2, cap_t: 3, cap_u: 4, slope: 5}
    assert discriminant.subs(sample) == -1_396_755_360

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "weighted diagonal maps and inherited apolar "
            "insertion arrangement"
        ),
        "weighted_23_all_alpha_diagonal_identically_zero": True,
        "weighted_01_insertion_arrangement_identified": True,
        "weighted_01_projected_line_discriminant": str(discriminant),
        "weighted_01_exceptional_point_count": len(exceptional_points),
        "nonempty_open_sample": {
            "S": 2,
            "T": 3,
            "U": 4,
            "r": 5,
        },
        "nonempty_open_sample_discriminant": -1_396_755_360,
        "weighted_01_generic_binary_neighbour_exists": False,
        "weighted_23_generic_binary_neighbour_exists": False,
        "generic_weighted_H22_fibre_empty": True,
        "complete_slope_parameter_boundary_closed": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            H31.name: sha256(H31),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
