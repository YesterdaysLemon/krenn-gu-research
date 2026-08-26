#!/usr/bin/env python3
"""Verify the exhaustive GLD74 projective boundary inside the sign plane.

This is an exact calculation over Q(i).  It restricts the homogeneous linear
part of the GLD74 mixed response quotient to the three-dimensional sign
isotypic block of the raw fibre, identifies the resulting 3 by 3 matrix of
linear forms, and proves that its projective rank-one locus consists of three
reduced points.  It does not classify boundary points outside the sign block
and does not construct an affine response lift.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations, permutations
from pathlib import Path

import sympy as sp

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
GLD76_ESCAPE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_response_projective_escape_boundary.py"
)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def check():
    gld74 = load(GLD74, "gld74_full_fibre")
    s3_reduction = load(S3_REDUCTION, "gld76_s3_reduction")
    escape = load(GLD76_ESCAPE, "gld76_projective_escape")
    data = gld74.quotient_forms()
    coefficient_matrices = [
        sp.Matrix(
            [data["coefficient_rows"][row][column][:35] for row in range(65)]
        )
        for column in range(3)
    ]

    gld73 = gld74.load_gld73()
    transformed = gld74.transformed_map()
    _particular, raw_kernel, _pivots, _free = gld74.affine_fibre(
        transformed[0], transformed[4], transformed[5]
    )
    assert raw_kernel.shape == (79, 35)

    descriptors = s3_reduction.raw_descriptors()
    sign_projector = sp.zeros(79, 79)
    actions = []
    for sigma in permutations((1, 2, 3)):
        action = s3_reduction.permutation_matrix(descriptors, (0, *sigma))
        actions.append((sigma, action))
        sign_projector += permutation_sign(sigma) * action
    sign_projector /= 6
    assert sign_projector * sign_projector == sign_projector

    projected_kernel = sign_projector * raw_kernel
    sign_pivots = projected_kernel.rref()[1]
    raw_sign_basis = projected_kernel[:, list(sign_pivots)]
    assert raw_sign_basis.shape == (79, 3) and raw_sign_basis.rank() == 3
    for sigma, action in actions:
        assert action * raw_sign_basis == permutation_sign(sigma) * raw_sign_basis

    kernel_rows = raw_kernel.T.rref()[1]
    fibre_sign_basis = (
        raw_kernel[list(kernel_rows), :].inv()
        * raw_sign_basis[list(kernel_rows), :]
    )
    assert raw_kernel * fibre_sign_basis == raw_sign_basis
    expected_fibre_sign_basis = sp.zeros(35, 3)
    for row, column, value in (
        (9, 0, 1),
        (11, 0, -1),
        (18, 0, -1),
        (20, 0, 1),
        (27, 0, 1),
        (29, 0, -1),
        (10, 1, 1),
        (14, 1, -1),
        (19, 1, -1),
        (23, 1, 1),
        (28, 1, 1),
        (32, 1, -1),
        (13, 2, 1),
        (15, 2, -1),
        (22, 2, -1),
        (24, 2, 1),
        (31, 2, 1),
        (33, 2, -1),
    ):
        expected_fibre_sign_basis[row, column] = sp.Rational(value, 6)
    assert fibre_sign_basis == expected_fibre_sign_basis

    output = sp.Matrix.hstack(
        *(matrix * fibre_sign_basis for matrix in coefficient_matrices)
    )
    assert output.rank() == 3
    output_columns = output.rref()[1]
    output_basis = output[:, list(output_columns)]
    output_rows = output_basis.T.rref()[1]
    output_inverse = output_basis[list(output_rows), :].inv()
    coordinate_matrices = [
        (
            output_inverse
            * (matrix * fibre_sign_basis)[list(output_rows), :]
        ).applyfunc(sp.simplify)
        for matrix in coefficient_matrices
    ]
    expected_coordinate_matrices = (
        sp.eye(3),
        sp.Matrix(((sp.I, 1 + sp.I, 0), (1 - sp.I, -sp.I, 0), (0, 0, -1))),
        sp.diag(-1, -1, 1),
    )
    assert tuple(coordinate_matrices) == expected_coordinate_matrices
    assert all(
        all(sp.expand(value) == 0 for value in output_basis * coordinates - matrix * fibre_sign_basis)
        for coordinates, matrix in zip(
            coordinate_matrices, coefficient_matrices, strict=True
        )
    )

    u, v, w = sp.symbols("u v w")
    vector = sp.Matrix((u, v, w))
    sign_response = sp.Matrix.hstack(
        *(coordinates * vector for coordinates in coordinate_matrices)
    )
    expected_sign_response = sp.Matrix(
        (
            (u, sp.I * u + (1 + sp.I) * v, -u),
            (v, (1 - sp.I) * u - sp.I * v, -v),
            (w, -w, w),
        )
    )
    assert sign_response == expected_sign_response

    minors = [
        sp.factor(sign_response.extract(rows, columns).det())
        for rows in combinations(range(3), 2)
        for columns in combinations(range(3), 2)
    ]
    nonzero_minors = tuple(sorted(set(value for value in minors if value != 0), key=str))
    generators = (
        sp.expand((u + v) * (u - sp.I * v)),
        u * w,
        v * w,
    )
    ideal = sp.groebner(nonzero_minors, u, v, w, order="grevlex", domain=sp.QQ_I)
    expected_ideal = sp.groebner(generators, u, v, w, order="grevlex", domain=sp.QQ_I)
    assert ideal == expected_ideal
    assert tuple(sp.factor(poly.as_expr()) for poly in ideal.polys) == tuple(
        sp.factor(value) for value in generators
    )

    # The ideal is the reduced union of the three displayed homogeneous
    # maximal ideals.  Indeed, w != 0 forces u=v=0; on w=0 the two distinct
    # factors u+v and u-i*v give the other two points.
    projective_points = (
        ("v_minus", sp.Matrix((0, 0, -6)), -1, 1),
        ("v_plus", sp.Matrix((-6 * sp.I, -6, 0)), 1, -1),
        ("v_third", sp.Matrix((6, -6, 0)), -1, -1),
    )
    profiles = []
    for name, coordinates, a, b in projective_points:
        fibre_vector = fibre_sign_basis * coordinates
        z0, z1, z2 = (matrix * fibre_vector for matrix in coefficient_matrices)
        assert z0 != sp.zeros(65, 1)
        assert all(sp.expand(value) == 0 for value in z1 - a * z0)
        assert all(sp.expand(value) == 0 for value in z2 - b * z0)
        assert sp.Matrix.hstack(z0, z1, z2).rank() == 1
        proportionality = (a * coefficient_matrices[0] - coefficient_matrices[1]).col_join(
            b * coefficient_matrices[0] - coefficient_matrices[2]
        )
        proportionality_pivots, proportionality_free, _proportionality_kernel = (
            escape.gaussian_nullspace(gld73, proportionality)
        )
        assert len(proportionality_pivots) == 34
        assert len(proportionality_free) == 1
        assert all(sp.expand(value) == 0 for value in proportionality * fibre_vector)
        raw_direction = raw_kernel * fibre_vector
        for sigma, action in actions:
            assert action * raw_direction == permutation_sign(sigma) * raw_direction
        profiles.append(
            {
                "name": name,
                "sign_coordinates": [str(value) for value in coordinates],
                "column_ratios_z1_z2_over_z0": [a, b],
                "fibre_support": {
                    str(index): str(sp.expand(value))
                    for index, value in enumerate(fibre_vector)
                    if value != 0
                },
                "proportionality_rank_nullity": [34, 1],
            }
        )

    return {
        "status": "exact_sign_plane_projective_boundary_trichotomy_not_full_boundary",
        "global_conjecture": "UNRESOLVED",
        "raw_fibre_sign_dimension": raw_sign_basis.cols,
        "sign_response_matrix": [
            [str(sp.expand(value)) for value in row]
            for row in sign_response.tolist()
        ],
        "rank_one_ideal_groebner_basis": [str(value) for value in generators],
        "reduced_projective_point_count": len(projective_points),
        "projective_points": profiles,
        "boundary_outside_sign_plane_classified": False,
        "affine_response_lift_constructed": False,
        "survivor_open_exclusion_proved": False,
    }


def main():
    print("four-root survivor sign-boundary trichotomy: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
