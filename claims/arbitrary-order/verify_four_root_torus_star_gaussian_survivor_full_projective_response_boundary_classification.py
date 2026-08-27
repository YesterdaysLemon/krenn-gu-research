#!/usr/bin/env python3
"""Verify the complete GLD72 projective rank-one response boundary.

The calculation is exact over Q(i).  It decomposes the complete 35-dimensional
raw kernel under the actual leaf S3 action, proves that the trivial and
standard blocks have no point in the first proportional-column chart, proves
that K0 is injective (so the other two projective charts are empty), and
replays the GLD77 three-point sign boundary.

This is a fixed-Gaussian projective-boundary classification.  The accompanying
theorem supplies the direct-isotypic-sum argument.  No moving-survivor or
global Krenn--Gu conclusion is asserted here.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import permutations
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[2]
GLD74 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py"
)
S3_REDUCTION = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_response_s3_representation_reduction.py"
)
GLD77 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_response_sign_boundary_trichotomy.py"
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_rank(matrix: sp.Matrix) -> int:
    return int(DomainMatrix.from_Matrix(matrix).rank())


def monic_gcd(polynomials: list[sp.Expr], variable: sp.Symbol) -> sp.Expr:
    result = sp.Poly(polynomials[0], variable, extension=sp.I)
    for polynomial in polynomials[1:]:
        result = sp.gcd(result, sp.Poly(polynomial, variable, extension=sp.I))
    return sp.expand(result.monic().as_expr())


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def check() -> dict[str, object]:
    gld74 = load("gld74_full_boundary", GLD74)
    s3 = load("gld76_s3_full_boundary", S3_REDUCTION)
    gld77 = load("gld77_full_boundary", GLD77)
    s3_result = s3.check()
    assert s3_result["complete_q0_response_covariance_verified"] is True
    assert s3_result["raw_kernel"][
        "isotypic_dimensions_trivial_sign_standard"
    ] == [8, 3, 24]

    gld73, _xi, eta, transformed_ports, columns, target = gld74.transformed_map()
    _particular, raw_kernel, _pivots, free = gld74.affine_fibre(
        gld73, columns, target
    )
    raw_kernel = raw_kernel.applyfunc(sp.expand)
    assert raw_kernel.shape == (79, 35)

    quotient = gld74.quotient_forms()
    response = [
        sp.Matrix(
            [quotient["coefficient_rows"][row][root][:35] for row in range(65)]
        )
        for root in range(3)
    ]

    descriptors = s3.raw_descriptors()
    group = tuple(permutations((1, 2, 3)))
    raw_actions = tuple(
        s3.permutation_matrix(descriptors, (0, *sigma)) for sigma in group
    )

    # GLD74 works after the equal-leaf frame change sending the Gaussian
    # survivor to literal Delta_4.  Verify covariance again in those actual
    # transformed coordinates, rather than importing only the canonical
    # GLD76 character calculation.
    gld75 = s3.load_gld75()
    survivor = gld73.load_gld72()
    parent = survivor.load_gate().load_parent()
    words = parent.LOCAL_INDICES
    mixed_rows = tuple(
        row for row, word in enumerate(words) if len(set(word)) != 1
    )
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    raw_response_maps = gld74.q0_response_context(
        gld73, eta, transformed_ports
    )
    constant_columns = [columns[0], *columns[13:25]]
    constant_mixed = sp.Matrix(
        [
            [column[row] for column in constant_columns]
            for row in mixed_rows
        ]
    )
    pivot_rows = tuple(constant_mixed.T.rref()[1])
    quotient_rows = tuple(
        row for row in range(78) if row not in set(pivot_rows)
    )
    correction = (
        constant_mixed[list(quotient_rows), :]
        * constant_mixed[list(pivot_rows), :].inv()
    )
    quotient_projection = sp.zeros(65, 78)
    for output_row, mixed_row in enumerate(quotient_rows):
        quotient_projection[output_row, mixed_row] = 1
        for pivot_column, pivot_row in enumerate(pivot_rows):
            quotient_projection[output_row, pivot_row] -= correction[
                output_row, pivot_column
            ]
    assert quotient_projection[:, list(quotient_rows)] == sp.eye(65)

    transformed_covariance = []
    for sigma, raw_action in zip(group, raw_actions, strict=True):
        mode_permutation = (0, *sigma)
        tensor_action = sp.Matrix.hstack(
            *(
                gld75.permute_tensor_modes(
                    parent, sp.eye(81)[:, column], mode_permutation
                )
                for column in range(81)
            )
        )
        mixed_action = tensor_action[list(mixed_rows), list(mixed_rows)]
        assert (
            nuisance * raw_action - tensor_action * nuisance
        ).applyfunc(sp.expand) == sp.zeros(81, 79)
        assert all(
            (
                raw_response * raw_action - mixed_action * raw_response
            ).applyfunc(sp.expand)
            == sp.zeros(78, 79)
            for raw_response in raw_response_maps
        )
        assert constant_mixed.row_join(
            mixed_action * constant_mixed
        ).rank() == 13

        transported_kernel = (raw_action * raw_kernel).applyfunc(sp.expand)
        kernel_action = transported_kernel[list(free), :]
        assert (
            raw_kernel * kernel_action - transported_kernel
        ).applyfunc(sp.expand) == sp.zeros(79, 35)
        quotient_action = (
            quotient_projection * mixed_action
        )[:, list(quotient_rows)]
        assert (
            quotient_action * quotient_projection
            - quotient_projection * mixed_action
        ).applyfunc(sp.expand) == sp.zeros(65, 78)
        assert all(
            (
                quotient_action * matrix - matrix * kernel_action
            ).applyfunc(sp.expand)
            == sp.zeros(65, 35)
            for matrix in response
        )
        transformed_covariance.append(True)
    assert all(transformed_covariance)

    trivial_projector = sum(raw_actions, sp.zeros(79, 79))
    sign_projector = sum(
        (
            permutation_sign(sigma) * action
            for sigma, action in zip(group, raw_actions, strict=True)
        ),
        sp.zeros(79, 79),
    )
    standard_projector = 6 * sp.eye(79) - trivial_projector - sign_projector
    transposition = raw_actions[group.index((1, 3, 2))]
    standard_plus_projector = (sp.eye(79) + transposition) * standard_projector

    def fibre_basis(
        projector: sp.Matrix, expected_pivots: tuple[int, ...] | None
    ):
        candidates = projector * raw_kernel
        pivots = tuple(candidates.rref()[1])
        if expected_pivots is not None:
            assert pivots == expected_pivots
        actual = candidates[:, list(pivots)]
        fibre = actual[list(free), :]
        assert raw_kernel * fibre == actual
        return fibre

    trivial = fibre_basis(
        trivial_projector, (0, 7, 8, 9, 10, 12, 13, 16)
    )
    sign = fibre_basis(sign_projector, (9, 10, 13))
    standard_plus = fibre_basis(
        standard_plus_projector,
        None,
    )
    assert (trivial.cols, sign.cols, standard_plus.cols) == (8, 3, 12)

    trivial_maps = [matrix * trivial for matrix in response]
    sign_maps = [matrix * sign for matrix in response]
    standard_maps = [matrix * standard_plus for matrix in response]

    # K0 is injective on every isotypic multiplicity block.  Since a
    # transposition has a one-dimensional + eigenspace in the standard irrep,
    # the 12-column standard check is equivalent to the full 24-dimensional
    # standard-isotypic injectivity statement.
    k0_profiles = (
        (
            "trivial",
            trivial_maps[0],
            (2, 3, 6, 14, 15, 16, 18, 19),
            -5328 + 5328 * sp.I,
        ),
        (
            "sign",
            sign_maps[0],
            (0, 19, 44),
            sp.Rational(-1, 6) + sp.Rational(1, 6) * sp.I,
        ),
        (
            "standard_multiplicity",
            standard_maps[0],
            (1, 2, 3, 6, 7, 18, 19, 23, 25, 27, 30, 43),
            21275136 - 7091712 * sp.I,
        ),
    )
    k0_output = []
    for name, matrix, rows, expected in k0_profiles:
        determinant = sp.factor(matrix[list(rows), :].det())
        assert determinant == expected != 0, (name, determinant, expected)
        assert exact_rank(matrix) == matrix.cols
        k0_output.append(
            {"block": name, "rows": list(rows), "determinant": str(determinant)}
        )
    assert exact_rank(response[0]) == 35

    a, b = sp.symbols("a b")

    # Trivial block: two first-equation minors leave only a=-1.  The remaining
    # one-dimensional kernel then fails the second proportionality equation
    # for every b.
    trivial_first = a * trivial_maps[0] - trivial_maps[1]
    trivial_rows = (
        (2, 3, 6, 14, 16, 18, 19, 41),
        (2, 3, 6, 14, 16, 18, 19, 43),
    )
    trivial_minors = [
        sp.factor(trivial_first[list(rows), :].det(), extension=sp.I)
        for rows in trivial_rows
    ]
    assert monic_gcd(trivial_minors, a) == a + 1
    trivial_at_minus = trivial_first.subs(a, -1).applyfunc(sp.expand)
    assert exact_rank(trivial_at_minus) == 7
    trivial_null = trivial_at_minus.nullspace()
    assert len(trivial_null) == 1
    normalized_trivial_null = sp.simplify(
        trivial_null[0] / trivial_null[0][-1]
    )
    expected_trivial_null = sp.Matrix(
        [
            -sp.Rational(2, 3) * sp.I,
            (1 - sp.I) / 18,
            -2 * sp.I,
            2 * sp.I,
            0,
            2 - sp.I,
            -3 - sp.I,
            1,
        ]
    )
    assert normalized_trivial_null == expected_trivial_null
    trivial_second = (b * trivial_maps[0] - trivial_maps[2]) * normalized_trivial_null
    trivial_residual_rows = (2, 14)
    trivial_residuals = [
        sp.factor(trivial_second[row], extension=sp.I)
        for row in trivial_residual_rows
    ]
    assert monic_gcd(trivial_residuals, b) == 1

    # Standard block: Schur reduction to the transposition + eigenspace.
    # Three exact maximal minors of the first pencil have gcd (a+1)^4.
    # Hence a common projective kernel could only occur on a=-1.  There the
    # first pencil has a four-dimensional kernel; two 4 x 4 minors of the
    # second pencil restricted to that kernel have unit gcd in Q(i)[b].
    standard_first = a * standard_maps[0] - standard_maps[1]
    standard_rows = (
        (1, 2, 3, 6, 7, 16, 18, 19, 23, 25, 27, 43),
        (1, 2, 3, 6, 7, 16, 18, 19, 22, 23, 25, 43),
        (1, 2, 3, 6, 7, 16, 18, 19, 22, 23, 25, 44),
    )
    standard_minors = [
        sp.factor(
            standard_first[list(rows), :].det(method="domain-ge"),
            extension=sp.I,
        )
        for rows in standard_rows
    ]
    standard_first_gcd = monic_gcd(standard_minors, a)
    assert sp.expand(standard_first_gcd - (a + 1) ** 4) == 0

    standard_minus = standard_first.subs(a, -1).applyfunc(sp.expand)
    assert exact_rank(standard_minus) == 8
    standard_nullspace = sp.Matrix.hstack(*standard_minus.nullspace())
    assert standard_nullspace.shape == (12, 4)
    standard_second = (
        (b * standard_maps[0] - standard_maps[2]) * standard_nullspace
    ).applyfunc(sp.expand)
    standard_residual_rows = (
        (1, 2, 3, 6),
        (1, 2, 3, 7),
    )
    standard_residuals = [
        sp.factor(
            standard_second[list(rows), :].det(method="domain-ge"),
            extension=sp.I,
        )
        for rows in standard_residual_rows
    ]
    assert monic_gcd(standard_residuals, b) == 1

    sign_result = gld77.check()
    assert sign_result["reduced_projective_point_count"] == 3
    assert sign_result["boundary_outside_sign_plane_classified"] is False

    return {
        "status": "exact_fixed_gaussian_full_projective_response_boundary_classification",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_then_C",
        "raw_kernel_isotypic_dimensions": [8, 3, 24],
        "standard_multiplicity_dimension": 12,
        "complete_q0_response_covariance_verified": True,
        "transformed_gld74_quotient_covariance_verified": True,
        "k0_injective_block_minors": k0_output,
        "other_projective_charts_empty": True,
        "trivial_first_minor_rows": [list(rows) for rows in trivial_rows],
        "trivial_first_minor_gcd": str(monic_gcd(trivial_minors, a)),
        "trivial_residual_rows": list(trivial_residual_rows),
        "trivial_residual_gcd": str(monic_gcd(trivial_residuals, b)),
        "trivial_boundary_empty": True,
        "standard_boundary_minor_rows": [list(rows) for rows in standard_rows],
        "standard_first_minor_gcd": str(standard_first_gcd),
        "standard_residual_rows": [list(rows) for rows in standard_residual_rows],
        "standard_residual_gcd": str(monic_gcd(standard_residuals, b)),
        "standard_boundary_empty": True,
        "mixed_isotypic_boundary_new_points": False,
        "full_projective_boundary_point_count": 3,
        "full_projective_boundary_is_exactly_gld77_sign_points": True,
        "moving_survivor_open_exclusion_proved": False,
        "graph_witness_proved": False,
    }


def main():
    result = check()
    print("four-root Gaussian full projective response boundary: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
