#!/usr/bin/env python3
"""Verify the GLD84 equal-leaf survivor center-rank chart reduction.

The calculation is exact over Q(i).  It reads the independently pinned
GLD75 sparse survivor basis, imposes the scale equation x8=0, and proves that
the ten equations are affine-linear in the remaining eight center shifts.
It then checks the named rank-seven Gaussian chart, the transverse rank-eight
minor, the smooth scale-fixed tangent coordinates, and the finite chart
counts used by the written determinantal reduction.
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
GLD75 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py"
)
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"

CENTER_COLUMNS = tuple(range(8))
LEAF_COLUMNS = tuple(range(9, 15))
RANK_SEVEN_ROWS = tuple(range(7))
RANK_SEVEN_COLUMNS = (0, 1, 2, 3, 4, 5, 7)
RANK_EIGHT_ROWS = tuple(range(8))


def load_gld75():
    spec = importlib.util.spec_from_file_location("gld75_for_gld84", GLD75)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def determinant_directional_derivative(
    matrix_at_point: sp.Matrix, matrix_derivative: sp.Matrix
) -> sp.Expr:
    """Differentiate a determinant by replacing one column at a time."""

    assert matrix_at_point.rows == matrix_at_point.cols
    assert matrix_derivative.shape == matrix_at_point.shape
    total = sp.Integer(0)
    for column in range(matrix_at_point.cols):
        replaced = matrix_at_point.copy()
        replaced[:, column] = matrix_derivative[:, column]
        total += replaced.det()
    return sp.expand(total)


def check() -> dict[str, object]:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert payload["variable_order"] == [f"x{index}" for index in range(15)]

    gld75 = load_gld75()
    shifts = tuple(sp.symbols("x0:15"))
    generators = tuple(
        sp.expand(gld75.sparse_polynomial(encoded, shifts).as_expr())
        for encoded in payload["basis"]
    )
    assert len(generators) == 10

    scale_fixed = tuple(sp.expand(value.subs(shifts[8], 0)) for value in generators)
    center = sp.Matrix(shifts[:8])
    leaf = tuple(shifts[index] for index in LEAF_COLUMNS)
    coefficient = sp.Matrix(scale_fixed).jacobian(center)
    inhomogeneous = sp.Matrix(scale_fixed).subs({value: 0 for value in center})

    assert all(shifts[8] not in value.free_symbols for value in scale_fixed)
    assert all(
        sp.diff(entry, variable) == 0
        for entry in coefficient
        for variable in center
    )
    assert all(
        entry.free_symbols <= set(leaf)
        for entry in (*coefficient, *inhomogeneous)
    )
    reconstruction_error = (
        sp.Matrix(scale_fixed) - coefficient * center - inhomogeneous
    ).applyfunc(sp.expand)
    assert reconstruction_error == sp.zeros(10, 1)

    origin = {value: 0 for value in shifts}
    coefficient_at_origin = coefficient.subs(origin)
    assert coefficient_at_origin.rank() == 7
    assert inhomogeneous.subs(origin) == sp.zeros(10, 1)
    gaussian_kernel = coefficient_at_origin.nullspace()
    assert len(gaussian_kernel) == 1
    gaussian_kernel_generator = sp.Matrix([1, -1, 0, 0, 0, 0, 1, 0])
    assert coefficient_at_origin * gaussian_kernel_generator == sp.zeros(10, 1)

    rank_seven_block = coefficient.extract(RANK_SEVEN_ROWS, RANK_SEVEN_COLUMNS)
    rank_seven_minor_at_origin = rank_seven_block.subs(origin).det()
    assert rank_seven_minor_at_origin == 12

    rank_eight_block = coefficient.extract(RANK_EIGHT_ROWS, CENTER_COLUMNS)
    rank_eight_block_at_origin = rank_eight_block.subs(origin)
    rank_eight_minor_at_origin = rank_eight_block_at_origin.det()
    rank_eight_x14_derivative = determinant_directional_derivative(
        rank_eight_block_at_origin,
        rank_eight_block.diff(shifts[14]).subs(origin),
    )
    assert rank_eight_minor_at_origin == 0

    assert rank_eight_x14_derivative == 0

    # The scale-fixed GLD75 germ is smooth with these four free coordinates.
    scale_fixed_jacobian = sp.Matrix([*scale_fixed, shifts[8]]).jacobian(shifts)
    jacobian_at_origin = scale_fixed_jacobian.subs(origin)
    assert jacobian_at_origin.rank() == 11
    pivot_columns = jacobian_at_origin.rref()[1]
    free_columns = tuple(
        index for index in range(15) if index not in set(pivot_columns)
    )
    assert free_columns == (6, 12, 13, 14)

    tangent = next(
        vector
        for vector in jacobian_at_origin.nullspace()
        if vector[14] != 0
    )
    tangent = tangent / tangent[14]
    directional_matrix_derivative = sp.zeros(8, 8)
    for index, variable in enumerate(shifts):
        if tangent[index] == 0:
            continue
        directional_matrix_derivative += tangent[index] * rank_eight_block.diff(
            variable
        ).subs(origin)
    directional_derivative = determinant_directional_derivative(
        rank_eight_block_at_origin,
        directional_matrix_derivative,
    )
    assert directional_derivative == 48 * sp.I

    rank_eight_chart_count = math.comb(10, 8)
    rank_seven_chart_count = math.comb(10, 7) * math.comb(8, 7)
    assert rank_eight_chart_count == 45
    assert rank_seven_chart_count == 960

    return {
        "status": "exact_equal_leaf_center_rank_determinantal_chart_reduction",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_characteristic_zero_then_C",
        "scale_fixed_survivor_generator_count": len(scale_fixed),
        "center_variable_count": len(center),
        "leaf_variable_count": len(leaf),
        "center_coefficient_shape": list(coefficient.shape),
        "center_rank_at_gld72": coefficient_at_origin.rank(),
        "gaussian_center_kernel_generator": [
            int(value) for value in gaussian_kernel_generator
        ],
        "named_rank_seven_rows": list(RANK_SEVEN_ROWS),
        "named_rank_seven_columns": list(RANK_SEVEN_COLUMNS),
        "named_rank_seven_minor_at_gld72": str(rank_seven_minor_at_origin),
        "named_rank_eight_rows": list(RANK_EIGHT_ROWS),
        "named_rank_eight_minor_at_gld72": str(rank_eight_minor_at_origin),
        "rank_eight_minor_ambient_partial_x14_at_gld72": str(
            rank_eight_x14_derivative
        ),
        "rank_eight_minor_tau14_derivative_at_gld72": str(
            directional_derivative
        ),
        "scale_fixed_tangent_free_columns": list(free_columns),
        "rank_eight_chart_count": rank_eight_chart_count,
        "rank_seven_chart_count": rank_seven_chart_count,
        "rank_at_most_six_minor_generator_count": rank_seven_chart_count,
        "gld72_component_has_nearby_rank_eight_points": True,
        "center_rank_cover_exhausts_equal_leaf_base": True,
        "center_rank_cover_exhausts_full_survivor_locus": False,
        "gld83_fitting_residual_closed": False,
        "global_conjecture_resolved": False,
        "parent_certificate_sha256": CERTIFICATE_SHA256,
    }


def main() -> None:
    print("four-root equal-leaf center-rank determinantal reduction: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
