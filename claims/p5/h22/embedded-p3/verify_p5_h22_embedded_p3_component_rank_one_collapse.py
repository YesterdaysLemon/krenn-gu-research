#!/usr/bin/env python3
"""Verify the weighted H22 rank-one projected-image obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
from verify_p5_h22_embedded_p3_component_generic_obstruction import (
    weighted_coefficients,
)



import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp



ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"
)
RANK_TWO = (
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


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


def main() -> None:
    cap_s, cap_u = sp.symbols("S U", nonzero=True)
    slope = 1 / cap_s
    cap_t = cap_u / cap_s
    t0, t1, t2, t3 = sp.symbols("t0:4")
    shifts = (t0, t1, t2, t3)
    x0, x1, x2, x3 = sp.symbols("x0:4")
    y0, y1, y2, y3 = sp.symbols("y0:4")
    extensions = (x0, x1, x2, x3, y0, y1, y2, y3)
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
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients_01 = weighted_coefficients(
        alpha, marked_beta, extensions, "01", slope
    )
    diagonal_01 = sp.factor(coefficients_01[(0, 0, 0, 0)])
    assert diagonal_01 == sp.factor(
        (1 + cap_s + cap_u) * x1
        + (1 - cap_s - cap_u) * x2
        + (1 - cap_s + cap_u) * x3
    )
    assert sp.factor(
        coefficients_01[(1, 0, 0, 0)]
        - (slope + t0) * diagonal_01
    ) == 0

    forced_shifts = (-slope, t1, t2, t3)
    forced_beta = shifted_basis(alpha, beta, forced_shifts)
    forced_01 = weighted_coefficients(
        alpha, forced_beta, extensions, "01", slope
    )
    assert forced_01[(1, 1, 1, 1)] == -2 * y0

    forced_23 = weighted_coefficients(
        alpha, forced_beta, extensions, "23", slope
    )
    assert all(
        forced_23[(0,) + word] == 0 for word in WORDS3
    )

    # Undo the three harmless upper-triangular marked-basis shears.
    z1, z2, z3 = sp.symbols("z1:4")
    shear_substitution = {
        y1: z1 + t1 * x1,
        y2: z2 + t2 * x2,
        y3: z3 + t3 * x3,
    }
    unmarked_beta = shifted_basis(
        alpha, beta, (-slope, 0, 0, 0)
    )
    unmarked_extensions = (
        x0,
        x1,
        x2,
        x3,
        y0,
        z1,
        z2,
        z3,
    )
    unmarked_23 = weighted_coefficients(
        alpha,
        unmarked_beta,
        unmarked_extensions,
        "23",
        slope,
    )
    for word in WORDS3:
        marked_word = (1,) + word
        expected = 0
        for lower_word in WORDS3:
            if any(
                lower_word[index] > word[index]
                for index in range(3)
            ):
                continue
            coefficient = sp.prod(
                (t1, t2, t3)[index]
                for index in range(3)
                if word[index] and not lower_word[index]
            )
            expected += coefficient * unmarked_23[
                (1,) + lower_word
            ]
        actual = forced_23[marked_word].subs(shear_substitution)
        assert sp.factor(actual - expected) == 0

    variables = (x1, x2, x3, z1, z2, z3)
    unwanted_words = tuple(
        (1,) + word
        for word in WORDS3
        if word != (1, 1, 1)
    )
    insertion = sp.Matrix(
        [
            [
                sp.diff(unmarked_23[word], variable)
                for variable in variables
            ]
            for word in unwanted_words
        ]
    )
    expected_insertion = sp.Matrix(
        (
            (
                (cap_s + 1) / cap_s,
                -(cap_s + 1) / cap_s,
                (1 - cap_s) / cap_s,
                0,
                0,
                0,
            ),
            (
                0,
                -(cap_s + 1) / cap_s,
                0,
                0,
                0,
                (1 - cap_s) / cap_s,
            ),
            (
                (cap_s + 1) / cap_s,
                0,
                0,
                0,
                -(cap_s + 1) / cap_s,
                0,
            ),
            (
                (cap_s - 1) / cap_s,
                0,
                0,
                0,
                -(cap_s + 1) / cap_s,
                0,
            ),
            (
                0,
                -(cap_s + 1) / cap_s,
                0,
                (cap_s + 1) / cap_s,
                0,
                0,
            ),
            (0, -2, 0, 0, 0, 0),
            (
                0,
                0,
                (cap_s - 1) / cap_s,
                (cap_s + 1) / cap_s,
                -(cap_s + 1) / cap_s,
                0,
            ),
        )
    )
    assert all(
        sp.factor(entry) == 0
        for entry in insertion - expected_insertion
    )

    common_factor = (
        4 * (cap_s - 1) ** 2 * (cap_s + 1) ** 2
        / cap_s**5
    )
    expected_signs = (-1, 0, 1, 0, 1, 0, -1)
    maximal_minors = []
    for omitted, expected_sign in enumerate(expected_signs):
        rows = tuple(
            row for row in range(7) if row != omitted
        )
        determinant = sp.factor(
            insertion.extract(rows, range(6)).det()
        )
        assert sp.factor(
            determinant - expected_sign * common_factor
        ) == 0
        maximal_minors.append(determinant)

    special_kernels = {}
    for value, expected_basis in (
        (
            1,
            (
                (0, 0, 1, 0, 0, 0),
                (0, 0, 0, 0, 0, 1),
            ),
        ),
        (
            -1,
            (
                (0, 0, 0, 1, 0, 0),
                (0, 0, 0, 0, 1, 0),
            ),
        ),
    ):
        specialized = insertion.subs({cap_s: value})
        expected_vectors = tuple(
            sp.Matrix(vector) for vector in expected_basis
        )
        assert all(
            specialized * vector == sp.zeros(7, 1)
            for vector in expected_vectors
        )
        assert len(specialized.nullspace()) == 2
        special_kernels[str(value)] = [
            list(vector) for vector in expected_basis
        ]

    desired_23 = sp.factor(unmarked_23[(1, 1, 1, 1)])
    expected_desired_23 = sp.factor(
        (
            (cap_s - 1) * z1
            - 2 * cap_s * z2
            + (cap_s - 1) * z3
        )
        / cap_s
    )
    assert desired_23 == expected_desired_23
    kernel_plus = special_kernels["1"]
    assert all(
        desired_23.subs(
            {
                cap_s: 1,
                **dict(zip(variables, vector, strict=True)),
            }
        )
        == 0
        for vector in kernel_plus
    )
    kernel_minus = special_kernels["-1"]
    assert all(
        diagonal_01.subs(
            {
                cap_s: -1,
                **dict(zip(variables, vector, strict=True)),
            }
        )
        == 0
        for vector in kernel_minus
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "collapse marking identity, complementary insertion "
            "pencil, and two exceptional-kernel covectors"
        ),
        "collapse_equations": ["r*S=1", "T=r*U"],
        "forced_mode_zero_marking": "t0=-r",
        "complementary_insertion_maximal_minors": [
            str(value) for value in maximal_minors
        ],
        "complementary_insertion_exceptional_parameters": [
            "S=1",
            "S=-1",
        ],
        "S_equals_1_kernel_kills_D23_pure_diagonal": True,
        "S_equals_minus_1_kernel_kills_D01_alpha_diagonal": True,
        "rank_one_projection_collapse_weighted_H22_fibre_empty": True,
        "complete_normalized_chart_weighted_H22_fibre_empty": True,
        "normalization_projective_boundary_closed": False,
        "global_problem_resolved": False,
        "dependencies": {
            RANK_TWO.name: sha256(RANK_TWO),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
