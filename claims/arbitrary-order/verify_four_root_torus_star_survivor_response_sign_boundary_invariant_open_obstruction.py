#!/usr/bin/env python3
"""Verify the invariant principal-open obstruction at all GLD77 sign points.

The calculation is exact over Q(i).  It averages one GLD74 raw section over
the actual leaf S3 action, restricts each proportionality operator to the
eight-dimensional invariant raw-kernel block, and checks a named nonzero
9-by-9 augmented minor at every reduced GLD77 sign-plane boundary point.

The accompanying theorem supplies the equivariant local-algebra argument.
This verifier does not classify projective boundary outside the sign plane.
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
UNIVERSAL = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_response_universal_module_reduction.py"
)

POINTS = (
    (
        "v_minus",
        -1,
        1,
        {13: -1, 15: 1, 22: 1, 24: -1, 31: -1, 33: 1},
        (2, 3, 6, 14, 15, 16, 18, 19, 67),
        sp.Rational(6574160, 27) + sp.Rational(1735448, 9) * sp.I,
    ),
    (
        "v_plus",
        1,
        -1,
        {
            9: -sp.I,
            10: -1,
            11: sp.I,
            14: 1,
            18: sp.I,
            19: 1,
            20: -sp.I,
            23: -1,
            27: -sp.I,
            28: -1,
            29: sp.I,
            32: 1,
        },
        (2, 3, 6, 14, 15, 16, 18, 19, 22),
        sp.Rational(153664, 9) + sp.Rational(44480, 3) * sp.I,
    ),
    (
        "v_third",
        -1,
        -1,
        {
            9: 1,
            10: -1,
            11: -1,
            14: 1,
            18: -1,
            19: 1,
            20: 1,
            23: -1,
            27: 1,
            28: -1,
            29: -1,
            32: 1,
        },
        (2, 3, 6, 14, 15, 16, 18, 19, 67),
        -sp.Rational(29451260, 81) + sp.Rational(3419540, 81) * sp.I,
    ),
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_rank(matrix: sp.Matrix) -> int:
    return int(DomainMatrix.from_Matrix(matrix).rank())


def check():
    gld74 = load("gld74_full_fibre", GLD74)
    s3 = load("gld76_s3_reduction", S3_REDUCTION)
    universal = load("gld76_universal_module", UNIVERSAL)
    gld73, _xi, eta, ports, columns, target = gld74.transformed_map()
    particular, raw_kernel, _pivots, free = gld74.affine_fibre(
        gld73, columns, target
    )
    assert raw_kernel.shape == (79, 35)

    data = gld74.quotient_forms()
    root_maps = [
        sp.Matrix(
            [data["coefficient_rows"][row][root][:35] for row in range(65)]
        )
        for root in range(3)
    ]
    affine = [
        sp.Matrix(
            [data["coefficient_rows"][row][root][35] for row in range(65)]
        )
        for root in range(3)
    ]

    parent = gld73.load_gld72().load_gate().load_parent()
    descriptors = s3.raw_descriptors()
    group = tuple(permutations((1, 2, 3)))
    raw_actions = tuple(
        s3.permutation_matrix(descriptors, (0, *sigma)) for sigma in group
    )

    # Check covariance of the actual transformed interface and all full legal
    # root-response maps.  This prevents an abstract tensor-orbit symmetry
    # from being substituted for graph/source response semantics.
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    response_maps = universal.q0_response_maps(
        gld73, eta, ports, parent.LOCAL_INDICES
    )
    for sigma, raw_action in zip(group, raw_actions, strict=True):
        inverse = [0] * 4
        for source, destination in enumerate((0, *sigma)):
            inverse[destination] = source
        tensor_action = sp.zeros(81, 81)
        for output, word in enumerate(parent.LOCAL_INDICES):
            source_word = tuple(word[inverse[mode]] for mode in range(4))
            tensor_action[output, parent.LOCAL_INDEX[source_word]] = 1
        assert all(
            sp.expand(value) == 0
            for value in nuisance * raw_action - tensor_action * nuisance
        )
        assert tensor_action * target == target
        assert all(
            all(
                sp.expand(value) == 0
                for value in tensor_action * response - response * raw_action
            )
            for response in response_maps
        )

    # The selected GLD74 mixed quotient is regular after inverting this fixed
    # 13-by-13 response pivot.  It is named separately from the obstruction
    # minors so no quotient denominator is discarded silently.
    mixed_rows = tuple(
        row for row, word in enumerate(parent.LOCAL_INDICES) if len(set(word)) != 1
    )
    constant_columns = [columns[0], *columns[13:25]]
    constant_mixed = sp.Matrix(
        [[column[row] for column in constant_columns] for row in mixed_rows]
    )
    quotient_pivot_rows = tuple(constant_mixed.T.rref()[1])
    quotient_pivot = sp.factor(
        constant_mixed[list(quotient_pivot_rows), :].det()
    )
    assert quotient_pivot == sp.Rational(8, 27) * (1 + sp.I)

    # Reynolds-average the complete kernel and select a deterministic basis
    # of its invariant image.  Dividing by 6 is a unit in characteristic zero.
    reynolds_kernel = sum(
        (raw_action * raw_kernel for raw_action in raw_actions),
        sp.zeros(79, 35),
    )
    invariant_pivots = tuple(reynolds_kernel.rref()[1])
    assert invariant_pivots == (0, 7, 8, 9, 10, 12, 13, 16)
    invariant_raw = reynolds_kernel[:, list(invariant_pivots)]
    invariant_fibre = invariant_raw[list(free), :]
    assert invariant_fibre.shape == (35, 8)
    assert exact_rank(invariant_fibre) == 8
    invariant_basis_rows = tuple(invariant_fibre.T.rref()[1])
    invariant_basis_pivot = sp.factor(
        invariant_fibre[list(invariant_basis_rows), :].det()
    )
    assert invariant_basis_pivot == 1008 * sp.I

    averaged_particular = sum(
        (raw_action * particular for raw_action in raw_actions),
        sp.zeros(79, 1),
    ) / 6
    section_shift = (averaged_particular - particular)[list(free), :]
    assert raw_kernel * section_shift == averaged_particular - particular
    averaged_affine = [
        affine[root] + root_maps[root] * section_shift for root in range(3)
    ]

    profiles = []
    for name, a, b, sparse_vector, selected_rows, expected_determinant in POINTS:
        boundary_vector = sp.zeros(35, 1)
        for index, value in sparse_vector.items():
            boundary_vector[index] = value
        z0, z1, z2 = (matrix * boundary_vector for matrix in root_maps)
        assert z0 != sp.zeros(65, 1)
        assert all(sp.expand(value) == 0 for value in z1 - a * z0)
        assert all(sp.expand(value) == 0 for value in z2 - b * z0)

        proportionality = (a * root_maps[0] - root_maps[1]).col_join(
            b * root_maps[0] - root_maps[2]
        )
        invariant_operator = proportionality * invariant_fibre
        invariant_affine = (a * averaged_affine[0] - averaged_affine[1]).col_join(
            b * averaged_affine[0] - averaged_affine[2]
        )
        augmented = invariant_operator.row_join(invariant_affine)
        selected = augmented[list(selected_rows), :]
        determinant = sp.factor(selected.det())
        assert exact_rank(invariant_operator) == 8
        assert exact_rank(augmented) == 9
        assert exact_rank(selected[:, :8]) == 8
        assert determinant == expected_determinant != 0
        profiles.append(
            {
                "name": name,
                "chart_slopes": [a, b],
                "operator_augmented_ranks": [8, 9],
                "selected_rows": list(selected_rows),
                "obstruction_minor_at_gld72": str(determinant),
            }
        )

    return {
        "status": "exact_sign_boundary_invariant_principal_open_obstruction",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_characteristic_zero_then_C",
        "quotient_pivot_rows": list(quotient_pivot_rows),
        "quotient_pivot_at_gld72": str(quotient_pivot),
        "raw_invariant_dimension": invariant_fibre.cols,
        "invariant_basis_kernel_columns": list(invariant_pivots),
        "invariant_basis_fibre_rows": list(invariant_basis_rows),
        "invariant_basis_pivot_at_gld72": str(invariant_basis_pivot),
        "points": profiles,
        "sign_plane_boundary_branches_excluded_on_named_principal_opens": True,
        "boundary_outside_sign_plane_classified": False,
        "full_survivor_open_exclusion_proved": False,
        "affine_response_lift_constructed": False,
    }


def main():
    print("four-root survivor sign-boundary invariant open obstruction: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
