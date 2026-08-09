#!/usr/bin/env python3
"""Verify the support-two A=0 boundary obstruction for H31."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

from verify_p5_h31_embedded_p3_component_normalized_boundary import (
    full_one_marked,
    permanent5,
)
from verify_p5_h31_marked_basis_open_branch import one_marked_map


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md"
)
NORMALIZED = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent4(rows):
    size = len(rows)
    return sp.factor(
        sum(
            sp.prod(
                rows[row][permutation[row]] for row in range(size)
            )
            for permutation in itertools.permutations(range(size))
        )
    )


def insertion_tensor(point, alpha, beta, variables):
    result = {}
    for word in WORDS3:
        selected = tuple(
            beta[mode] if word[mode] else alpha[mode]
            for mode in range(3)
        )
        value = 0
        for mode in range(3):
            extension = (
                variables[3 + mode] if word[mode] else variables[mode]
            )
            other = tuple(
                selected[index]
                for index in range(3)
                if index != mode
            )
            value += extension * permanent4((point,) + other)
        result[word] = sp.factor(value)
    return result


def main() -> None:
    cap_c, p, q, rho = sp.symbols("C p q rho", nonzero=True)
    x1, x2, x3, z1, z2, z3 = sp.symbols(
        "x1 x2 x3 z1 z2 z3"
    )
    variables = (x1, x2, x3, z1, z2, z3)
    alpha_shared = (
        (0, 1, 0),
        (1, 0, cap_c),
        (0, 1, 0),
    )
    beta_shared = (
        (1, 0, -cap_c),
        (0, 1, 0),
        (1, 0, -cap_c),
    )
    insertion_values = insertion_tensor(
        (p, q, rho), alpha_shared, beta_shared, variables
    )
    unwanted_words = WORDS3[:-1]
    insertion = sp.Matrix(
        [
            [
                sp.diff(insertion_values[word], variable)
                for variable in variables
            ]
            for word in unwanted_words
        ]
    )
    expected_insertion = sp.Matrix(
        (
            (
                cap_c * p + rho,
                0,
                cap_c * p + rho,
                0,
                0,
                0,
            ),
            (
                0,
                -cap_c * p + rho,
                0,
                0,
                0,
                cap_c * p + rho,
            ),
            (0, 0, 0, 0, 0, 0),
            (
                -cap_c * p + rho,
                0,
                0,
                0,
                -cap_c * p + rho,
                0,
            ),
            (
                0,
                -cap_c * p + rho,
                0,
                cap_c * p + rho,
                0,
                0,
            ),
            (0, -2 * cap_c * q, 0, 0, 0, 0),
            (
                0,
                0,
                -cap_c * p + rho,
                0,
                -cap_c * p + rho,
                0,
            ),
        )
    )
    assert all(
        sp.factor(entry) == 0
        for entry in insertion - expected_insertion
    ), insertion - expected_insertion
    maximal_minor = sp.factor(
        insertion.extract((0, 1, 3, 4, 5, 6), range(6)).det()
    )
    assert maximal_minor == (
        4
        * cap_c
        * q
        * (cap_c * p - rho) ** 2
        * (cap_c * p + rho) ** 3
    )

    cap_p, cap_q, cap_r = sp.symbols("P Q R")
    alpha_diagonal = sp.factor(
        insertion_values[(0, 0, 0)].subs(
            {p: cap_p, q: cap_q, rho: cap_r}
        )
    )
    assert alpha_diagonal == (
        cap_c * cap_p + cap_r
    ) * (x1 + x3)

    # Generic point rho=-Cp, p!=0.
    h, t1, t2, t3, y0 = sp.symbols("h t1 t2 t3 y0")
    generic_substitution = {
        rho: -cap_c * p,
        x1: -h,
        x2: 0,
        x3: -h,
        z2: h,
    }
    specialized_insertion = insertion.subs(generic_substitution)
    generic_vector = sp.Matrix((-h, 0, -h, z1, h, z3))
    assert specialized_insertion * generic_vector == sp.zeros(7, 1)

    marked_alpha = (
        (cap_p, cap_q, cap_r, sp.Symbol("x0")),
        (0, 1, 0, -h),
        (1, 0, cap_c, 0),
        (0, 1, 0, -h),
    )
    marked_beta = (
        (p, q, -cap_c * p, y0),
        (1, t1, -cap_c, z1 - h * t1),
        (t2, 1, cap_c * t2, h),
        (1, t3, -cap_c, z3 - h * t3),
    )
    alpha_slice = {
        word: permanent4(
            (marked_alpha[0],)
            + tuple(
                marked_beta[mode + 1]
                if word[mode]
                else marked_alpha[mode + 1]
                for mode in range(3)
            )
        )
        for word in WORDS3
    }
    expected_mixed = {
        (0, 0, 1): (cap_c * cap_p + cap_r) * (z3 - 2 * h * t3),
        (0, 1, 0): -2 * h * t2 * (cap_c * cap_p + cap_r),
        (0, 1, 1): t2 * (cap_c * cap_p + cap_r) * (z3 - 2 * h * t3),
        (1, 0, 0): (cap_c * cap_p + cap_r) * (z1 - 2 * h * t1),
        (1, 0, 1): (
            (cap_c * cap_p + cap_r)
            * (-2 * h * t1 * t3 + t1 * z3 + t3 * z1)
        ),
        (1, 1, 0): t2 * (cap_c * cap_p + cap_r) * (z1 - 2 * h * t1),
    }
    assert all(
        sp.factor(alpha_slice[word] - expected) == 0
        for word, expected in expected_mixed.items()
    ), {
        word: sp.factor(alpha_slice[word] - expected)
        for word, expected in expected_mixed.items()
    }

    generic_family_substitution = {
        t2: 0,
        z1: 2 * h * t1,
        z3: 2 * h * t3,
    }
    assert sp.factor(
        alpha_slice[(1, 0, 1)].subs(generic_family_substitution)
        - 2 * h * t1 * t3 * (cap_c * cap_p + cap_r)
    ) == 0

    generic_beta = tuple(
        tuple(
            sp.factor(
                sp.sympify(entry).subs(generic_family_substitution)
            )
            for entry in row
        )
        for row in marked_beta
    )
    generic_alpha = marked_alpha
    neighbor_mode_two = one_marked_map(
        2, generic_alpha, generic_beta
    )
    generic_d = h * q + 2 * h * p * (t1 + t3) + y0
    generic_minor = sp.factor(
        neighbor_mode_two.extract((0, 4, 5, 7), range(4)).det()
    )
    expected_generic_minor = (
        16
        * cap_c**2
        * h**2
        * p**2
        * (cap_c * cap_p + cap_r)
        * generic_d
    )
    assert sp.factor(
        generic_minor - expected_generic_minor
    ) == 0, (generic_minor, expected_generic_minor)
    pure_alpha = (
        (0, cap_p, cap_q, cap_r),
        (0, 0, 1, 0),
        (0, 1, 0, cap_c),
        (0, 0, 1, 0),
    )
    pure_beta = (
        (1, p, q, -cap_c * p),
        (0, 1, t1, -cap_c),
        (0, 0, 1, 0),
        (0, 1, t3, -cap_c),
    )
    transverse = (
        one_marked_map(2, pure_alpha, pure_beta)
        * sp.Matrix((1, 0, 0, 0))
    )
    assert transverse[5] == -2 * cap_c * p

    # Coordinate endpoint and the C=-1 resonance.
    root = (0, 1, 1, 1, 0)
    coordinate_x1, coordinate_x3 = sp.symbols("u1 u3")
    coordinate_mixed = permanent5(
        (
            root,
            (1, 0, 1, 0, y0),
            (0, 0, 1, 0, coordinate_x1),
            (0, 1, 0, cap_c, 0),
            (0, 0, 1, 0, coordinate_x3),
        )
    )
    assert sp.factor(
        coordinate_mixed
        - (cap_c + 1) * (coordinate_x1 + coordinate_x3)
    ) == 0

    # Resonant transverse subcase P+R!=0.
    k, y = sp.symbols("k y")
    resonant_alpha = (
        (
            cap_p,
            cap_q,
            cap_r,
            h * (cap_p * k + cap_q + cap_r * k),
        ),
        (0, 1, 0, h),
        (1, 0, -1, 0),
        (0, 1, 0, h),
    )
    resonant_beta = (
        (0, 1, 0, y),
        (1, 0, 1, 0),
        (0, 1, 0, -h),
        (1, k, 1, -h * k),
    )
    resonant_maps = tuple(
        one_marked_map(mode, resonant_alpha, resonant_beta)
        for mode in range(4)
    )
    cover_values = (
        sp.factor(
            resonant_maps[3].extract((0, 3, 4, 7), range(4)).det()
        ),
        sp.factor(
            resonant_maps[1].extract((0, 1, 5, 7), range(4)).det()
        ),
        sp.factor(
            resonant_maps[2].extract((0, 1, 3, 7), range(4)).det()
        ),
    )
    assert cover_values == (
        -4
        * h
        * (cap_p - cap_r)
        * (cap_p + cap_r)
        * (y - h)
        * (y + h),
        4 * h * k**2 * (cap_p - cap_r) ** 2 * (y - h) ** 2,
        -16
        * cap_q
        * h**2
        * (cap_p - cap_r)
        * (y - h)
        * (cap_p * k + cap_q + cap_r * k),
    )
    resonant_pure_alpha = (
        (0, cap_p, cap_q, cap_r),
        (0, 0, 1, 0),
        (0, 1, 0, -1),
        (0, 0, 1, 0),
    )
    resonant_pure_beta = (
        (1, 0, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 0),
        (0, 1, k, 1),
    )
    assert (
        one_marked_map(
            3, resonant_pure_alpha, resonant_pure_beta
        )
        * sp.Matrix((1, 0, 0, 0))
    )[0] == -cap_p + cap_r
    assert (
        one_marked_map(
            2, resonant_pure_alpha, resonant_pure_beta
        )
        * sp.Matrix((1, 0, 0, 0))
    )[7] == 2

    deepest_alpha = (
        (0, cap_p, 0, cap_r, 0),
        (0, 0, 1, 0, h),
        (0, 1, 0, -1, 0),
        (0, 0, 1, 0, h),
    )
    deepest_beta = (
        (1, 0, 1, 0, -h),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, -h),
        (0, 1, 0, 1, 0),
    )
    deepest_stack = full_one_marked(
        1, (1, 0, 0, 0, 0), deepest_alpha, deepest_beta
    ).col_join(
        full_one_marked(
            1,
            (0, 0, 0, 0, 1),
            deepest_alpha,
            deepest_beta,
        )
    )
    deepest_rows = (0, 3, 7, 8, 12)
    deepest_determinant = sp.factor(
        deepest_stack.extract(deepest_rows, range(5)).det()
    )
    assert deepest_determinant == (
        -8 * h**2 * (cap_p - cap_r) ** 2 * (cap_p + cap_r)
    )

    # Resonant antipodal subcase P+R=0.
    antipodal_x, antipodal_d = sp.symbols("x d")
    antipodal_alpha = (
        (0, -cap_p, cap_q, cap_p, -cap_q * antipodal_d),
        (0, 0, 1, 0, antipodal_x),
        (0, 1, 0, -1, 0),
        (0, 0, 1, 0, 1 - antipodal_x),
    )
    antipodal_beta = (
        (1, 0, 1, 0, y),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, antipodal_d),
        (0, 1, k, 1, -k * antipodal_x),
    )
    antipodal_binary = {
        word: permanent5(
            (root,)
            + tuple(
                antipodal_beta[mode]
                if word[mode]
                else antipodal_alpha[mode]
                for mode in range(4)
            )
        )
        for word in itertools.product((0, 1), repeat=4)
    }
    assert antipodal_binary[(1, 0, 1, 1)] == 2 * (
        antipodal_d + antipodal_x
    )
    assert antipodal_binary[(1, 1, 1, 0)] == -2 * (
        -antipodal_d + antipodal_x - 1
    )

    half = sp.Rational(1, 2)
    antipodal_specialization = {
        antipodal_x: half,
        antipodal_d: -half,
    }
    antipodal_neighbor_alpha = tuple(
        tuple(entry for entry in row[1:])
        for row in tuple(
            tuple(
                sp.sympify(entry).subs(antipodal_specialization)
                for entry in row
            )
            for row in antipodal_alpha
        )
    )
    antipodal_neighbor_beta = tuple(
        tuple(entry for entry in row[1:])
        for row in tuple(
            tuple(
                sp.sympify(entry).subs(antipodal_specialization)
                for entry in row
            )
            for row in antipodal_beta
        )
    )
    antipodal_mode_one = one_marked_map(
        1, antipodal_neighbor_alpha, antipodal_neighbor_beta
    )
    antipodal_mode_two = one_marked_map(
        2, antipodal_neighbor_alpha, antipodal_neighbor_beta
    )
    assert sp.factor(
        antipodal_mode_one.extract((0, 1, 3, 7), range(4)).det()
        - 4 * cap_p**3 * k**2 * (2 * y - 1)
    ) == 0
    assert sp.factor(
        antipodal_mode_two.extract((0, 1, 3, 7), range(4)).det()
        - 4 * cap_p * cap_q**2 * (2 * y - 1)
    ) == 0

    antipodal_deep_alpha = (
        (0, -cap_p, 0, cap_p, 0),
        (0, 0, 1, 0, half),
        (0, 1, 0, -1, 0),
        (0, 0, 1, 0, half),
    )
    antipodal_deep_beta = (
        (1, 0, 1, 0, y),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, -half),
        (0, 1, 0, 1, 0),
    )
    antipodal_stack_mode_three = full_one_marked(
        3,
        (1, 0, 0, 0, 0),
        antipodal_deep_alpha,
        antipodal_deep_beta,
    ).col_join(
        full_one_marked(
            3,
            (0, 0, 0, 0, 1),
            antipodal_deep_alpha,
            antipodal_deep_beta,
        )
    )
    expected_kernel = sp.Matrix((0, 0, -2, 0, 1))
    assert (
        antipodal_stack_mode_three * expected_kernel
        == sp.zeros(16, 1)
    )
    assert len(antipodal_stack_mode_three.nullspace()) == 1

    gamma_rows = (
        (0, 0, 0, 0, 1),
        (0, 0, -2, 0, 1),
        (1, 0, -1, 0, y),
        tuple(expected_kernel),
    )
    fixed_third_coefficient = permanent5(
        (
            root,
            antipodal_deep_beta[0],
            antipodal_deep_beta[1],
            antipodal_deep_beta[2],
            gamma_rows[3],
        )
    )
    assert fixed_third_coefficient == 4

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "support-two insertion pencil, exceptional-line "
            "factor covers, and third-contraction resonance"
        ),
        "support_two_parameter": "C=1/B !=0",
        "insertion_maximal_minor": str(maximal_minor),
        "genuine_binary_forces": "rho=-C*p",
        "generic_exceptional_line_minor": str(generic_minor),
        "coordinate_nonresonant_third_coefficient": str(
            coordinate_mixed
        ),
        "coordinate_resonance": "C=-1",
        "resonant_cover_minors": [
            str(value) for value in cover_values
        ],
        "resonant_deepest_stacked_determinant": str(
            deepest_determinant
        ),
        "antipodal_binary_ratios": ["x=1/2", "d=-1/2"],
        "antipodal_fixed_third_coefficient": str(
            fixed_third_coefficient
        ),
        "support_two_A_zero_boundary_H31_fibre_empty": True,
        "remaining_mode_zero_plane_and_projective_boundary_closed": False,
        "global_problem_resolved": False,
        "dependencies": {
            NORMALIZED.name: sha256(NORMALIZED),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
