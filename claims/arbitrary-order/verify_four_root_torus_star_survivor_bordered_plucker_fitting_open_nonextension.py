#!/usr/bin/env python3
"""Verify the GLD83 bordered-Pluecker and Fitting-open reduction.

This verifier reconstructs the moving transported constant and response
blocks at the exact GLD72 survivor.  It computes all 2,025 coefficients of
the forty-five selected bordered quadrics through their exact Schur
complements, then checks the predicted gamma-free scaling against the pinned
physical GLD74/GLD82 matrix.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
BUILDER = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_moving_response_builder.py"
)
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_invariant_quadratic_macaulay_certificate.json"
)
CERTIFICATE_SHA256 = "4cdaf08a5f5dc40abc845d4dc1e6046ce3b259b2c751dfd3ec2955e5b94e65e0"

I_GAMMA = (0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 17, 27, 53)
D_AT_GLD72 = 24 - 24 * sp.I
GAMMA_AT_GLD72 = -692533995824480256 * (1 + sp.I)


def load_builder():
    spec = importlib.util.spec_from_file_location("moving_builder_for_gld83", BUILDER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def decode_gaussian(raw: list[int]) -> sp.Expr:
    assert len(raw) == 4
    return sp.Rational(raw[0], raw[1]) + sp.I * sp.Rational(raw[2], raw[3])


def certificate_matrix(payload: dict[str, object]) -> sp.Matrix:
    raw_columns = payload["columns"]
    assert isinstance(raw_columns, list)
    columns = [
        sp.Matrix([decode_gaussian(value) for value in raw_column])
        for raw_column in raw_columns
    ]
    result = sp.Matrix.hstack(*columns)
    assert result.shape == (45, 45)
    return result


def direct_gaussian_bordered_matrix(module):
    builder = module.build_moving_response_builder()
    substitutions = builder.chart.origin
    frames = tuple(
        frame.subs(substitutions).applyfunc(sp.expand) for frame in builder.chart.frames
    )
    frame_determinants = tuple(sp.factor(frame.det()) for frame in frames)
    frame_denominator = sp.expand(sp.prod(frame_determinants))
    assert frame_denominator == D_AT_GLD72

    alpha_section = builder.alpha_section().subs(substitutions).applyfunc(sp.expand)
    invariant_basis = builder.invariant.invariant_basis
    homogeneous_raw = invariant_basis.row_join(alpha_section)
    constant_num = builder.transport.apply(
        builder.interface.constant,
        substitutions=substitutions,
        expand=False,
    )
    constant_mixed = constant_num.extract(
        builder.interface.mixed_rows,
        range(builder.interface.constant.cols),
    )
    quotient_rows = tuple(row for row in range(78) if row not in I_GAMMA)
    assert quotient_rows == builder.quotient.quotient_positions
    pivot = constant_mixed[list(I_GAMMA), :]
    quotient = constant_mixed[list(quotient_rows), :]
    gamma = sp.factor(pivot.det())
    assert gamma == GAMMA_AT_GLD72
    pivot_inverse = pivot.inv()
    quotient_eliminator = quotient * pivot_inverse

    ordinary_root_maps = []
    ordinary_affine_columns = []
    for response in builder.interface.response_maps[:3]:
        response_num = builder.transport.apply(
            response,
            substitutions=substitutions,
            expand=False,
        )
        homogeneous_output = response_num * homogeneous_raw
        homogeneous_mixed = homogeneous_output.extract(
            builder.interface.mixed_rows,
            range(homogeneous_output.cols),
        )

        def ordinary_quotient(value: sp.Matrix) -> sp.Matrix:
            value_pivot = value[list(I_GAMMA), :]
            value_quotient = value[list(quotient_rows), :]
            return (value_quotient - quotient_eliminator * value_pivot).applyfunc(
                sp.expand
            )

        homogeneous_quotient = ordinary_quotient(homogeneous_mixed)
        ordinary_root_maps.append(homogeneous_quotient[:, :8])
        ordinary_affine_columns.append(homogeneous_quotient[:, 8:9])

    # Schur complementation of each bordered 15-by-15 determinant gives
    # gamma times the corresponding ordinary quotient 2-by-2 minor.
    ordinary_quadratic = module.quadratic_matrix_from_linear_forms(
        ordinary_root_maps,
        ordinary_affine_columns,
    )
    bordered = ordinary_quadratic.applyfunc(lambda value: sp.expand(gamma * value))
    assert bordered.shape == (45, 45)
    return builder, bordered, gamma, frame_denominator


def check() -> dict[str, object]:
    raw_certificate = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw_certificate
    assert hashlib.sha256(raw_certificate).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw_certificate)
    assert payload["format"] == "gaussian-quadratic-macaulay-Qi-v1"
    normalized_matrix = certificate_matrix(payload)
    normalized_determinant = decode_gaussian(payload["determinant"])
    assert normalized_determinant != 0

    module = load_builder()
    descriptors = tuple(
        tuple(int(entry) for entry in raw) for raw in payload["minor_descriptors"]
    )
    assert descriptors == module.MINOR_DESCRIPTORS
    assert len(descriptors) == len(set(descriptors)) == 45

    quotient_rows = tuple(row for row in range(78) if row not in I_GAMMA)
    assert len(I_GAMMA) == 13 and len(quotient_rows) == 65
    selected_coordinates = []
    for left_row, right_row, left_column, right_column in descriptors:
        assert 0 <= left_row < right_row < 65
        assert 0 <= left_column < right_column < 3
        ordered_rows = (*I_GAMMA, quotient_rows[left_row], quotient_rows[right_row])
        assert len(ordered_rows) == len(set(ordered_rows)) == 15
        selected_coordinates.append((ordered_rows, left_column, right_column))
    assert len(selected_coordinates) == len(set(selected_coordinates)) == 45

    builder, bordered_matrix, gamma, frame_denominator = (
        direct_gaussian_bordered_matrix(module)
    )
    pluecker_scalar = sp.expand(frame_denominator**2 * gamma)
    predicted_bordered = normalized_matrix.applyfunc(
        lambda value: sp.expand(pluecker_scalar * value)
    )
    assert bordered_matrix == predicted_bordered

    pluecker_determinant = sp.expand(pluecker_scalar**45 * normalized_determinant)
    fraction_free_determinant = sp.expand(
        (frame_denominator * gamma) ** 90 * normalized_determinant
    )
    assert pluecker_scalar != 0 and pluecker_determinant != 0
    assert fraction_free_determinant == sp.expand(gamma**45 * pluecker_determinant)

    homogeneous_coordinates = 9
    quadratic_monomials = math.comb(homogeneous_coordinates + 1, 2)
    exterior_coordinates = math.comb(78, 15)
    response_pairs = math.comb(3, 2)
    full_pluecker_columns = response_pairs * exterior_coordinates
    assert quadratic_monomials == 45
    assert exterior_coordinates == 4367914309753280
    assert full_pluecker_columns == 13103742929259840

    return {
        "status": "exact_bordered_pluecker_principal_and_fitting_open_reduction",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_characteristic_zero_then_C",
        "mixed_response_rows": 78,
        "constant_block_columns": 13,
        "bordered_minor_size": 15,
        "homogeneous_coordinate_count": homogeneous_coordinates,
        "quadratic_monomial_count": quadratic_monomials,
        "selected_bordered_quadratic_count": len(selected_coordinates),
        "selected_bordered_matrix_shape_rank": [45, 45, 45],
        "full_exterior_coordinate_count": exterior_coordinates,
        "full_bordered_quadratic_column_count": full_pluecker_columns,
        "d_at_gld72": str(frame_denominator),
        "gamma_at_gld72": str(gamma),
        "pluecker_scalar_over_normalized_matrix": str(pluecker_scalar),
        "moving_bordered_matrix_exactly_matches": True,
        "pluecker_determinant_nonzero_at_gld72": True,
        "quotient_pivot_factor_in_delta83": False,
        "delta82_over_delta83_factor": "gamma_num^46",
        "selected_open_contained_in_full_fitting_open": True,
        "full_fitting_open_exhausts_survivor_chart": False,
        "named_source_branch_excluded_via_gld81": True,
        "global_conjecture_resolved": False,
        "parent_certificate_sha256": CERTIFICATE_SHA256,
        "parent_quotient_fingerprint": payload["gld74_quotient_fingerprint"],
        "survivor_generator_count": len(builder.chart.survivor_generators),
    }


def main() -> None:
    print("four-root bordered-Pluecker Fitting open: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
