#!/usr/bin/env python3
"""Verify weighted H22 rank-two projected-line boundary exclusion."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

from verify_p5_h22_embedded_p3_component_generic_obstruction import (
    weighted_coefficients,
    weighted_row,
)
from verify_p5_h31_marked_basis_open_branch import one_marked_map


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
)
GENERIC = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
H31_BOUNDARY = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS5 = tuple(itertools.permutations(range(5)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shifted_basis(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.factor(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def neighbor_bases(alpha, beta, extension, slope):
    return (
        tuple(
            weighted_row(
                alpha[mode], extension[mode], "01", slope
            )
            for mode in range(4)
        ),
        tuple(
            weighted_row(
                beta[mode], extension[4 + mode], "01", slope
            )
            for mode in range(4)
        ),
    )


def check_binary(
    alpha,
    beta,
    shifts,
    extension,
    slope,
    expected_alpha,
    expected_beta,
):
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = weighted_coefficients(
        alpha, marked_beta, extension, "01", slope
    )
    assert all(
        sp.factor(value) == 0
        for word, value in coefficients.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    assert sp.factor(
        coefficients[(0, 0, 0, 0)] - expected_alpha
    ) == 0
    assert sp.factor(
        coefficients[(1, 1, 1, 1)] - expected_beta
    ) == 0
    return marked_beta, neighbor_bases(
        alpha, marked_beta, extension, slope
    )


def determinant(matrix, rows) -> sp.Expr:
    return sp.factor(matrix.extract(rows, range(4)).det())


def permanent5(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(5))
            for permutation in PERMUTATIONS5
        )
    )


def full_one_marked(mode, contraction, alpha, beta) -> sp.Matrix:
    source_basis = tuple(
        tuple(int(left == right) for right in range(5))
        for left in range(5)
    )
    rows = []
    for word in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if word[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        rows.append(
            [
                permanent5(
                    tuple(
                        source_basis[coordinate]
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                    + (contraction,)
                )
                for coordinate in range(5)
            ]
        )
    return sp.Matrix(rows)


def transverse_entry(mode, row, alpha, beta, slope) -> sp.Expr:
    kernel = sp.Matrix((1, -slope, 0, 0))
    return sp.factor(
        (one_marked_map(mode, alpha, beta) * kernel)[row]
    )


def main() -> None:
    cap_s, slope, h, y = sp.symbols("S r h y")
    cap_k = slope * cap_s - 1
    alpha_l3 = (
        (0, 1, cap_s, cap_s + 1),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta_l3 = (
        (1, 0, 1, slope + 1),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    l3_cases = (
        {
            "name": "101",
            "shifts": (-1 / cap_s, -1, -h, -1),
            "extension": sp.Matrix((0, 0, 1, 0, y, 0, 0, 0)),
            "diagonals": (-2 * cap_s, -2 * y),
            "minors": (
                (
                    1,
                    (0, 5, 6, 7),
                    8 * y * (h - 1) * cap_k**2 / cap_s,
                ),
                (3, (0, 1, 2, 7), -8 * cap_s * h * y),
            ),
            "transverse": ((1, 4, -2 / cap_s), (3, 0, 2)),
        },
        {
            "name": "011",
            "shifts": (-slope, 0, 0, -h),
            "extension": sp.Matrix((0, 0, 0, 1, y, 0, 0, 0)),
            "diagonals": (2, -2 * y),
            "minors": (
                (2, (0, 2, 4, 7), 8 * cap_s * y**2),
            ),
            "transverse": ((2, 0, -2 * cap_s),),
        },
        {
            "name": "1m10",
            "shifts": (
                -(slope + 1) / (cap_s + 1),
                -h,
                -1,
                0,
            ),
            "extension": sp.Matrix((0, 1, 0, 0, y, 0, 0, 0)),
            "diagonals": (2 * (cap_s + 1), -2 * y),
            "minors": (
                (
                    2,
                    (0, 1, 4, 7),
                    8 * cap_s * y**2 * (cap_s + 1),
                ),
            ),
            "transverse": ((2, 0, -2 * cap_s),),
        },
    )
    l3_certificates = {}
    for case in l3_cases:
        marked, (neighbor_alpha, neighbor_beta) = check_binary(
            alpha_l3,
            beta_l3,
            case["shifts"],
            case["extension"],
            slope,
            *case["diagonals"],
        )
        for mode, rows, expected in case["minors"]:
            actual = determinant(
                one_marked_map(
                    mode, neighbor_alpha, neighbor_beta
                ),
                rows,
            )
            assert sp.factor(actual - expected) == 0
        for mode, row, expected in case["transverse"]:
            actual = transverse_entry(
                mode, row, alpha_l3, marked, slope
            )
            assert sp.factor(actual - expected) == 0
        l3_certificates[case["name"]] = True

    # Endpoint S=0 factor covers for the second and third markings.
    endpoint_data = (
        (
            l3_cases[1],
            (
                (1, (0, 4, 5, 7), 8 * h * y * cap_k**2),
                (
                    2,
                    (0, 5, 6, 7),
                    -8 * y * (h - 1) * cap_k**2,
                ),
            ),
        ),
        (
            l3_cases[2],
            (
                (3, (0, 1, 2, 7), 8 * h * y),
                (
                    2,
                    (0, 4, 6, 7),
                    8 * y * (h - 1) * cap_k**2,
                ),
            ),
        ),
    )
    for case, certificates in endpoint_data:
        alpha_zero = tuple(
            tuple(sp.sympify(entry).subs({cap_s: 0}) for entry in row)
            for row in alpha_l3
        )
        beta_zero = tuple(
            tuple(sp.sympify(entry).subs({cap_s: 0}) for entry in row)
            for row in beta_l3
        )
        shifts_zero = tuple(
            sp.sympify(entry).subs({cap_s: 0})
            for entry in case["shifts"]
        )
        extension_zero = case["extension"].subs({cap_s: 0})
        marked_zero, (neighbor_alpha, neighbor_beta) = check_binary(
            alpha_zero,
            beta_zero,
            shifts_zero,
            extension_zero,
            slope,
            sp.sympify(case["diagonals"][0]).subs({cap_s: 0}),
            -2 * y,
        )
        for mode, rows, expected in certificates:
            actual = determinant(
                one_marked_map(
                    mode, neighbor_alpha, neighbor_beta
                ),
                rows,
            )
            assert sp.factor(
                actual - sp.sympify(expected).subs({cap_s: 0})
            ) == 0
        # Branchwise transverse constants.
        assert transverse_entry(
            1, 0, alpha_zero, marked_zero, slope
        ) == 2
        if case["name"] == "011":
            assert sp.factor(
                transverse_entry(
                    2, 7, alpha_zero, marked_zero, slope
                ).subs({h: 0})
                + 2
            ) == 0
        else:
            assert transverse_entry(
                3, 0, alpha_zero, marked_zero, slope
            ) == 2
            assert sp.factor(
                transverse_entry(
                    2, 7, alpha_zero, marked_zero, slope
                ).subs({h: 0})
                + 2
            ) == 0

    # Coordinate point e_p: U=S,T=1.
    alpha_e1 = (
        (0, 1, cap_s, cap_s),
        *alpha_l3[1:],
    )
    beta_e1 = (
        (1, 0, 1, 1),
        *beta_l3[1:],
    )
    extension_e1 = sp.Matrix((1, 1, -1, 0, y, 0, 0, 1))
    shifts_e1 = (-1 / cap_s, -1, -1, -sp.Rational(1, 2))
    factor_e1 = -slope * cap_s + cap_s * y + 1
    marked_e1, (neighbor_alpha, neighbor_beta) = check_binary(
        alpha_e1,
        beta_e1,
        shifts_e1,
        extension_e1,
        slope,
        4 * cap_s,
        -2 * factor_e1 / cap_s,
    )
    e1_minor = determinant(
        one_marked_map(1, neighbor_alpha, neighbor_beta),
        (0, 1, 3, 7),
    )
    assert sp.factor(e1_minor + 16 * cap_s * factor_e1) == 0
    assert transverse_entry(
        1, 3, alpha_e1, marked_e1, slope
    ) == 1

    # Coordinate point e_q: U=1,T=r.
    alpha_e2 = (
        (0, 1, cap_s, 1),
        *alpha_l3[1:],
    )
    beta_e2 = (
        (1, 0, 1, slope),
        *beta_l3[1:],
    )
    extension_e2 = sp.Matrix((-cap_s, 1, 0, 1, y, 0, 1, 0))
    shifts_e2 = (-slope, 0, -sp.Rational(1, 2), 0)
    factor_e2 = -slope * cap_s + y + 1
    marked_e2, (neighbor_alpha, neighbor_beta) = check_binary(
        alpha_e2,
        beta_e2,
        shifts_e2,
        extension_e2,
        slope,
        4,
        -2 * factor_e2,
    )
    neighboring_e2 = one_marked_map(
        1, neighbor_alpha, neighbor_beta
    )
    e2_dense = determinant(neighboring_e2, (0, 2, 3, 7))
    assert sp.factor(e2_dense + 16 * cap_s * factor_e2) == 0
    e2_zero = neighboring_e2.subs({cap_s: 0})
    e2_endpoint = determinant(e2_zero, (0, 2, 4, 7))
    assert sp.factor(e2_endpoint - 8 * (y - 1) * (y + 1)) == 0
    assert sp.factor(
        transverse_entry(1, 3, alpha_e2, marked_e2, slope) - cap_s
    ) == 0
    assert sp.factor(
        transverse_entry(1, 0, alpha_e2, marked_e2, slope).subs({cap_s: 0})
        - 2
    ) == 0

    deepest_alpha_e2 = tuple(
        tuple(sp.sympify(entry).subs({cap_s: 0}) for entry in row)
        + (extension_e2[index].subs({cap_s: 0, y: 1}),)
        for index, row in enumerate(alpha_e2)
    )
    deepest_beta_e2 = tuple(
        tuple(sp.sympify(entry).subs({cap_s: 0}) for entry in row)
        + (extension_e2[4 + index].subs({y: 1}),)
        for index, row in enumerate(marked_e2)
    )
    contraction_e2 = (1, slope, 0, 0, 0)
    pure_contraction = (0, 0, 0, 0, 1)
    stacked_e2 = full_one_marked(
        1, contraction_e2, deepest_alpha_e2, deepest_beta_e2
    ).col_join(
        full_one_marked(
            1,
            pure_contraction,
            deepest_alpha_e2,
            deepest_beta_e2,
        )
    )
    rows_e2 = (0, 2, 7, 10, 14)
    determinant_e2 = sp.factor(
        stacked_e2.extract(rows_e2, range(5)).det()
    )
    assert determinant_e2 == 8

    # Coordinate point e_r: S=r=-1.
    cap_t, cap_u = sp.symbols("T U")
    slope_e3 = -1
    alpha_e3 = (
        (0, 1, -1, cap_u),
        *alpha_l3[1:],
    )
    beta_e3 = (
        (1, 0, 1, cap_t),
        *beta_l3[1:],
    )
    shifts_e3 = (1, -sp.Rational(1, 2), 0, -1)
    extension_e3 = sp.Matrix((-cap_u, 0, 1, 1, y, 1, 0, 0))
    factor_e3 = cap_t + cap_u + y
    marked_e3, (neighbor_alpha, neighbor_beta) = check_binary(
        alpha_e3,
        beta_e3,
        shifts_e3,
        extension_e3,
        slope_e3,
        4,
        -2 * factor_e3,
    )
    neighboring_e3 = one_marked_map(
        2, neighbor_alpha, neighbor_beta
    )
    e3_dense = determinant(neighboring_e3, (0, 2, 3, 7))
    assert sp.factor(e3_dense + 16 * cap_u * factor_e3) == 0
    e3_zero = neighboring_e3.subs({cap_u: 0})
    e3_endpoint = determinant(e3_zero, (0, 2, 4, 7))
    assert sp.factor(
        e3_endpoint + 8 * (y - cap_t) * (y + cap_t)
    ) == 0
    assert transverse_entry(
        2, 3, alpha_e3, marked_e3, slope_e3
    ) == cap_u
    assert transverse_entry(
        2, 0, alpha_e3, marked_e3, slope_e3
    ) == 2 - cap_u

    deepest_alpha_e3 = tuple(
        tuple(sp.sympify(entry).subs({cap_u: 0}) for entry in row)
        + (extension_e3[index].subs({cap_u: 0, y: cap_t}),)
        for index, row in enumerate(alpha_e3)
    )
    deepest_beta_e3 = tuple(
        tuple(sp.sympify(entry).subs({cap_u: 0}) for entry in row)
        + (
            extension_e3[4 + index].subs(
                {cap_u: 0, y: cap_t}
            ),
        )
        for index, row in enumerate(marked_e3)
    )
    stacked_e3 = full_one_marked(
        2,
        (1, -1, 0, 0, 0),
        deepest_alpha_e3,
        deepest_beta_e3,
    ).col_join(
        full_one_marked(
            2,
            pure_contraction,
            deepest_alpha_e3,
            deepest_beta_e3,
        )
    )
    rows_e3 = (0, 2, 8, 14, 15)
    determinant_e3 = sp.factor(
        stacked_e3.extract(rows_e3, range(5)).det()
    )
    assert determinant_e3 == -8

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "weighted six-stratum insertion boundary and "
            "one-marked factor covers"
        ),
        "rank_two_projected_line_strata": [
            "U=S+1,T=r+1",
            "U=S,T=1",
            "U=1,T=r",
            "S=-1,r=-1",
        ],
        "binary_survivor_marked_families": 6,
        "L3_certificates": l3_certificates,
        "coordinate_e1_minor": str(e1_minor),
        "coordinate_e2_dense_minor": str(e2_dense),
        "coordinate_e2_endpoint_minor": str(e2_endpoint),
        "coordinate_e2_stacked_determinant": str(determinant_e2),
        "coordinate_e3_dense_minor": str(e3_dense),
        "coordinate_e3_endpoint_minor": str(e3_endpoint),
        "coordinate_e3_stacked_determinant": str(determinant_e3),
        "rank_two_projected_line_weighted_H22_fibre_empty": True,
        "rank_one_projection_collapse_closed": False,
        "normalization_projective_boundary_closed": False,
        "global_problem_resolved": False,
        "dependencies": {
            GENERIC.name: sha256(GENERIC),
            H31_BOUNDARY.name: sha256(H31_BOUNDARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
