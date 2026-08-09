#!/usr/bin/env python3
"""Verify complete normalized-chart H31 exclusion on embedded P3."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
)
GENERIC = (
    ROOT / "P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
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


def check_binary_family(
    alpha,
    beta,
    shifts,
    extension,
    expected_alpha,
    expected_beta,
) -> tuple:
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
        0, alpha, marked_beta
    )
    assert all(
        sp.factor(entry) == 0 for entry in mixed * extension
    )
    assert sp.factor(
        (diagonal_alpha * extension)[0] - expected_alpha
    ) == 0
    assert sp.factor(
        (diagonal_beta * extension)[0] - expected_beta
    ) == 0
    return marked_beta


def minor(matrix, rows) -> sp.Expr:
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


def main() -> None:
    p, q, rho = sp.symbols("p q rho")
    x1, x2, x3, z1, z2, z3 = sp.symbols(
        "x1 x2 x3 z1 z2 z3"
    )
    variables = (x1, x2, x3, z1, z2, z3)
    ell1 = p - q - rho
    ell2 = p - q + rho
    ell3 = p + q - rho
    ell4 = p + q + rho
    insertion = (
        ell4 * x1 + ell1 * x2 + ell2 * x3,
        ell1 * x2 + ell2 * z3,
        ell4 * x1 + ell1 * z2,
        ell3 * x1 + ell1 * z2,
        ell1 * x2 + ell4 * z1,
        -2 * q * x2,
        ell3 * x3 + ell4 * z1 + ell1 * z2,
    )
    matrix = sp.Matrix(
        [
            [sp.diff(entry, variable) for variable in variables]
            for entry in insertion
        ]
    )
    point_kernels = {
        (1, 0, 0): ((1, -1, 0, 1, -1, 1),),
        (0, 1, 0): ((1, 0, 1, 0, 1, 0),),
        (0, 0, 1): ((0, 1, 1, 1, 0, 1),),
        (1, 0, 1): (
            (0, 1, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 0),
        ),
        (1, 1, 0): (
            (0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 1),
        ),
        (0, 1, -1): (
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 1, 0),
        ),
        (1, 0, -1): (
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 0, 1),
        ),
        (0, 1, 1): (
            (0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 1),
        ),
        (1, -1, 0): (
            (1, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0),
        ),
    }
    kernel_dimensions = {}
    for point, expected_basis in point_kernels.items():
        specialized = matrix.subs(dict(zip((p, q, rho), point)))
        expected = tuple(sp.Matrix(vector) for vector in expected_basis)
        assert all(
            specialized * vector == sp.zeros(7, 1)
            for vector in expected
        )
        assert len(specialized.nullspace()) == len(expected)
        kernel_dimensions[str(point)] = len(expected)

    cap_p, cap_q, cap_r = sp.symbols("P Q R")
    insertion_full = {
        "000": ell4 * x1 + ell1 * x2 + ell2 * x3,
        "001": ell1 * x2 + ell2 * z3,
        "010": ell4 * x1 + ell1 * z2,
        "011": ell3 * x1 + ell1 * z2,
        "100": ell1 * x2 + ell4 * z1,
        "101": -2 * q * x2,
        "110": ell3 * x3 + ell4 * z1 + ell1 * z2,
        "111": ell3 * (z1 + z3) - 2 * q * z2,
    }
    coordinate_relations = {}
    for name, point, kernel, expected_factor in (
        (
            "e_p",
            (1, 0, 0),
            point_kernels[(1, 0, 0)][0],
            4 * (cap_q - cap_r) * (cap_q + cap_r),
        ),
        (
            "e_q",
            (0, 1, 0),
            point_kernels[(0, 1, 0)][0],
            4 * (cap_p - cap_r) * (cap_p + cap_r),
        ),
        (
            "e_r",
            (0, 0, 1),
            point_kernels[(0, 0, 1)][0],
            4 * (cap_p - cap_q) * (cap_p + cap_q),
        ),
    ):
        substitution = {
            p: cap_p,
            q: cap_q,
            rho: cap_r,
            **dict(zip(variables, kernel, strict=True)),
        }
        values = {
            word: sp.factor(expression.subs(substitution))
            for word, expression in insertion_full.items()
        }
        anchor = values["000"]
        relations = (
            sp.factor(anchor * values["110"] - values["100"] * values["010"]),
            sp.factor(anchor * values["101"] - values["100"] * values["001"]),
            sp.factor(anchor * values["011"] - values["010"] * values["001"]),
        )
        nonzero = tuple(value for value in relations if value != 0)
        assert nonzero
        assert all(
            sp.expand(value - expected_factor) == 0
            or sp.expand(value + expected_factor) == 0
            for value in nonzero
        )
        coordinate_relations[name] = str(sp.factor(expected_factor))

    cap_s, h, y = sp.symbols("S h y")
    base_beta = (
        (1, 0, 1, 1),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    alpha_l3 = (
        (0, 1, cap_s, cap_s + 1),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    l3_cases = (
        {
            "name": "101",
            "shifts": (-1 / cap_s, -1, -h, -1),
            "extension": sp.Matrix((0, 0, 1, 0, y, 0, 0, 0)),
            "diagonals": (-2 * cap_s, -2 * y),
            "minors": (
                (1, (0, 5, 6, 7), 8 * y * (h - 1) / cap_s),
                (3, (0, 1, 2, 7), -8 * cap_s * h * y),
            ),
            "pure_entries": ((1, 4, -2 / cap_s), (3, 0, 2)),
        },
        {
            "name": "011",
            "shifts": (0, 0, 0, -h),
            "extension": sp.Matrix((0, 0, 0, 1, y, 0, 0, 0)),
            "diagonals": (2, -2 * y),
            "minors": (
                (2, (0, 2, 4, 7), 8 * cap_s * y**2),
            ),
            "pure_entries": ((2, 4, -2),),
        },
        {
            "name": "1m10",
            "shifts": (-1 / (cap_s + 1), -h, -1, 0),
            "extension": sp.Matrix((0, 1, 0, 0, y, 0, 0, 0)),
            "diagonals": (2 * (cap_s + 1), -2 * y),
            "minors": (
                (
                    2,
                    (0, 1, 4, 7),
                    8 * cap_s * y**2 * (cap_s + 1),
                ),
            ),
            "pure_entries": ((2, 4, -2 / (cap_s + 1)),),
        },
    )
    l3_results = {}
    for case in l3_cases:
        marked_beta = check_binary_family(
            alpha_l3,
            base_beta,
            case["shifts"],
            case["extension"],
            *case["diagonals"],
        )
        for mode, rows, expected in case["minors"]:
            actual = minor(
                marked_extension(
                    0,
                    case["extension"],
                    alpha_l3,
                    marked_beta,
                    mode,
                ),
                rows,
            )
            assert sp.factor(actual - expected) == 0
        for mode, row, expected in case["pure_entries"]:
            actual = one_marked_map(
                mode, alpha_l3, marked_beta
            )[row, 0]
            assert sp.factor(actual - expected) == 0
        l3_results[case["name"]] = True

    # Endpoint S=0 covers for the second and third L3 markings.
    for case, minor_data in (
        (
            l3_cases[1],
            (
                (1, (0, 4, 5, 7), 8 * h * y),
                (2, (0, 5, 6, 7), -8 * y * (h - 1)),
            ),
        ),
        (
            l3_cases[2],
            (
                (3, (0, 1, 2, 7), 8 * h * y),
                (2, (0, 4, 6, 7), 8 * y * (h - 1)),
            ),
        ),
    ):
        alpha_zero = tuple(
            tuple(sp.sympify(entry).subs({cap_s: 0}) for entry in row)
            for row in alpha_l3
        )
        shifts_zero = tuple(
            sp.sympify(entry).subs({cap_s: 0})
            for entry in case["shifts"]
        )
        marked_zero = shifted_basis(
            alpha_zero, base_beta, shifts_zero
        )
        extension_zero = case["extension"].subs({cap_s: 0})
        for mode, rows, expected in minor_data:
            actual = minor(
                marked_extension(
                    0,
                    extension_zero,
                    alpha_zero,
                    marked_zero,
                    mode,
                ),
                rows,
            )
            assert sp.factor(actual - expected) == 0

    alpha_e1 = (
        (0, 1, cap_s, cap_s),
        *alpha_l3[1:],
    )
    shifts_e1 = (-1 / cap_s, -1, -1, -sp.Rational(1, 2))
    extension_e1 = sp.Matrix((1, 1, -1, 0, y, 0, 0, 1))
    marked_e1 = check_binary_family(
        alpha_e1,
        base_beta,
        shifts_e1,
        extension_e1,
        4 * cap_s,
        -2 * (cap_s * y + 1) / cap_s,
    )
    e1_minor = minor(
        marked_extension(
            0, extension_e1, alpha_e1, marked_e1, 1
        ),
        (0, 1, 3, 7),
    )
    assert sp.factor(e1_minor + 16 * cap_s * (cap_s * y + 1)) == 0
    assert one_marked_map(1, alpha_e1, marked_e1)[3, 0] == 1

    alpha_e2 = (
        (0, 1, cap_s, 1),
        *alpha_l3[1:],
    )
    beta_e2 = (
        (1, 0, 1, 0),
        *base_beta[1:],
    )
    shifts_e2 = (0, 0, -sp.Rational(1, 2), 0)
    extension_e2 = sp.Matrix((-cap_s, 1, 0, 1, y, 0, 1, 0))
    marked_e2 = check_binary_family(
        alpha_e2,
        beta_e2,
        shifts_e2,
        extension_e2,
        4,
        -2 * (y + 1),
    )
    neighbouring_e2 = marked_extension(
        0, extension_e2, alpha_e2, marked_e2, 1
    )
    assert sp.factor(
        minor(neighbouring_e2, (0, 2, 3, 7))
        + 16 * cap_s * (y + 1)
    ) == 0
    e2_zero = neighbouring_e2.subs({cap_s: 0})
    assert sp.factor(
        minor(e2_zero, (0, 2, 4, 7))
        - 8 * (y - 1) * (y + 1)
    ) == 0
    assert one_marked_map(1, alpha_e2, marked_e2)[4, 0] == 1

    deepest_alpha = tuple(
        tuple(
            sp.sympify(entry).subs({cap_s: 0})
            for entry in row
        )
        + (extension_e2[index].subs({cap_s: 0, y: 1}),)
        for index, row in enumerate(alpha_e2)
    )
    deepest_beta = tuple(
        tuple(
            sp.sympify(entry).subs({cap_s: 0})
            for entry in row
        )
        + (extension_e2[4 + index].subs({y: 1}),)
        for index, row in enumerate(marked_e2)
    )
    source_basis = tuple(
        tuple(int(left == right) for right in range(5))
        for left in range(5)
    )
    stacked = full_one_marked(
        1, source_basis[0], deepest_alpha, deepest_beta
    ).col_join(
        full_one_marked(
            1, source_basis[4], deepest_alpha, deepest_beta
        )
    )
    deepest_rows = (0, 2, 7, 10, 14)
    deepest_determinant = sp.factor(
        stacked.extract(deepest_rows, range(5)).det()
    )
    assert deepest_determinant == 8

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "nine-point insertion kernels, truncated Segre "
            "classification, and one-marked covers"
        ),
        "exceptional_kernel_dimensions": kernel_dimensions,
        "coordinate_truncated_Segre_factors": coordinate_relations,
        "binary_survivor_plane_strata": [
            "T=1,U=S+1",
            "T=1,U=S",
            "T=0,U=1",
        ],
        "binary_survivor_marked_families": 5,
        "L3_family_certificates": l3_results,
        "coordinate_e1_one_marked_minor": str(e1_minor),
        "coordinate_e2_dense_one_marked_minor": str(
            minor(neighbouring_e2, (0, 2, 3, 7))
        ),
        "coordinate_e2_S0_one_marked_minor": str(
            minor(e2_zero, (0, 2, 4, 7))
        ),
        "deepest_stacked_rows": list(deepest_rows),
        "deepest_stacked_determinant": str(deepest_determinant),
        "complete_normalized_chart_marked_H31_fibre_empty": True,
        "normalization_projective_boundary_closed": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            GENERIC.name: sha256(GENERIC),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
