#!/usr/bin/env python3
"""Verify the GLD82 invariant quadratic Macaulay determinant.

The calculation is exact over Q(i).  It reconstructs the GLD74 literal-Delta
quotient, Reynolds-averages the physical raw fibre, selects the moving
eight-dimensional invariant kernel block, and checks that 45 named intrinsic
rank-one minors span every quadric in eight invariant raw coordinates and one
homogenizing coordinate at the Gaussian survivor.

The theorem document defines the same 45-by-45 coefficient determinant over
the localized moving survivor base.  This replay proves its nonzero Gaussian
specialization; it does not expand the universal four-parameter polynomial.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from itertools import permutations
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
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_invariant_quadratic_macaulay_certificate.json"
)
CERTIFICATE_SHA256 = "4cdaf08a5f5dc40abc845d4dc1e6046ce3b259b2c751dfd3ec2955e5b94e65e0"

MINOR_DESCRIPTORS = (
    (2, 3, 0, 1),
    (2, 3, 0, 2),
    (2, 3, 1, 2),
    (2, 6, 0, 1),
    (2, 6, 0, 2),
    (2, 6, 1, 2),
    (2, 14, 0, 1),
    (2, 14, 0, 2),
    (2, 14, 1, 2),
    (2, 15, 0, 1),
    (2, 15, 0, 2),
    (2, 16, 0, 1),
    (2, 16, 0, 2),
    (2, 16, 1, 2),
    (2, 18, 0, 1),
    (2, 18, 0, 2),
    (2, 18, 1, 2),
    (2, 19, 0, 1),
    (2, 19, 0, 2),
    (2, 19, 1, 2),
    (2, 22, 0, 1),
    (2, 27, 0, 1),
    (2, 27, 0, 2),
    (2, 27, 1, 2),
    (3, 6, 0, 1),
    (3, 6, 0, 2),
    (3, 6, 1, 2),
    (3, 14, 0, 1),
    (3, 14, 0, 2),
    (3, 14, 1, 2),
    (3, 15, 0, 1),
    (3, 15, 0, 2),
    (3, 16, 0, 1),
    (3, 16, 0, 2),
    (3, 16, 1, 2),
    (3, 18, 0, 1),
    (3, 18, 0, 2),
    (3, 18, 1, 2),
    (3, 19, 0, 1),
    (6, 14, 0, 1),
    (6, 14, 0, 2),
    (6, 14, 1, 2),
    (6, 16, 0, 1),
    (6, 16, 1, 2),
    (16, 18, 0, 1),
)
DEGREE_TWO_PAIRS = tuple((left, right) for left in range(9) for right in range(left, 9))
EXPECTED_DETERMINANT = (
    -sp.Rational(
        378089878893442723106646837537745718758189247729870198909680050358976512,
        205891132094649,
    )
    + sp.Rational(
        25931419533924809154531852205198475327334321064667678574124775287933632512,
        1853020188851841,
    )
    * sp.I
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def product_coefficient(
    left: int,
    right: int,
    first: tuple[sp.Expr, ...],
    second: tuple[sp.Expr, ...],
) -> sp.Expr:
    if left == right:
        return first[left] * second[right]
    return first[left] * second[right] + first[right] * second[left]


def encode_gaussian(value: sp.Expr) -> list[int]:
    real, imaginary = sp.expand(value).as_real_imag()
    real = sp.Rational(real)
    imaginary = sp.Rational(imaginary)
    return [real.p, real.q, imaginary.p, imaginary.q]


def construct() -> dict[str, object]:
    gld74 = load("gld74_gld82", GLD74)
    s3 = load("s3_gld82", S3_REDUCTION)

    gld73, _xi, _eta, _ports, columns, target = gld74.transformed_map()
    particular, raw_kernel, _pivots, free = gld74.affine_fibre(gld73, columns, target)
    quotient = gld74.quotient_forms()
    root_maps = [
        sp.Matrix([quotient["coefficient_rows"][row][root][:35] for row in range(65)])
        for root in range(3)
    ]
    affine_columns = [
        sp.Matrix([quotient["coefficient_rows"][row][root][35] for row in range(65)])
        for root in range(3)
    ]

    descriptors = s3.raw_descriptors()
    group = tuple(permutations((1, 2, 3)))
    raw_actions = tuple(
        s3.permutation_matrix(descriptors, (0, *sigma)) for sigma in group
    )
    reynolds_kernel = sum(
        (raw_action * raw_kernel for raw_action in raw_actions),
        sp.zeros(79, 35),
    )
    invariant_pivots = tuple(reynolds_kernel.rref()[1])
    assert invariant_pivots == (0, 7, 8, 9, 10, 12, 13, 16)
    invariant_raw = reynolds_kernel[:, list(invariant_pivots)]
    invariant_fibre = invariant_raw[list(free), :]
    assert invariant_fibre.shape == (35, 8) and invariant_fibre.rank() == 8

    averaged_particular = (
        sum(
            (raw_action * particular for raw_action in raw_actions),
            sp.zeros(79, 1),
        )
        / 6
    )
    section_shift = (averaged_particular - particular)[list(free), :]
    assert raw_kernel * section_shift == averaged_particular - particular
    averaged_affine = [
        affine_columns[root] + root_maps[root] * section_shift for root in range(3)
    ]
    invariant_maps = [matrix * invariant_fibre for matrix in root_maps]

    # Each entry is the coefficient row of a moving quotient column in
    # homogeneous coordinates (u_0,...,u_7,s).
    linear_forms = [
        [
            tuple(sp.expand(invariant_maps[root][row, column]) for column in range(8))
            + (sp.expand(averaged_affine[root][row]),)
            for row in range(65)
        ]
        for root in range(3)
    ]

    selected_columns = []
    for left_row, right_row, left_column, right_column in MINOR_DESCRIPTORS:
        first = linear_forms[left_column][left_row]
        second = linear_forms[right_column][right_row]
        third = linear_forms[right_column][left_row]
        fourth = linear_forms[left_column][right_row]
        selected_columns.append(
            sp.Matrix(
                [
                    sp.expand(
                        product_coefficient(left, right, first, second)
                        - product_coefficient(left, right, third, fourth)
                    )
                    for left, right in DEGREE_TWO_PAIRS
                ]
            )
        )

    coefficient_matrix = sp.Matrix.hstack(*selected_columns)
    assert coefficient_matrix.shape == (45, 45)
    determinant = sp.factor(coefficient_matrix.det())
    assert determinant == EXPECTED_DETERMINANT != 0

    return {
        "invariant_pivots": invariant_pivots,
        "invariant_fibre_rank": invariant_fibre.rank(),
        "coefficient_matrix": coefficient_matrix,
        "determinant": determinant,
        "quotient_fingerprint": gld74.coefficient_fingerprint(
            quotient["coefficient_rows"]
        ),
    }


def canonical_certificate_bytes(result: dict[str, object]) -> bytes:
    matrix = result["coefficient_matrix"]
    assert isinstance(matrix, sp.MatrixBase)
    payload = {
        "format": "gaussian-quadratic-macaulay-Qi-v1",
        "field": "Q(i)",
        "variable_order": [*[f"u{index}" for index in range(8)], "s"],
        "degree_two_monomial_order": [list(pair) for pair in DEGREE_TWO_PAIRS],
        "minor_descriptors": [list(value) for value in MINOR_DESCRIPTORS],
        "columns": [
            [encode_gaussian(matrix[row, column]) for row in range(45)]
            for column in range(45)
        ],
        "determinant": encode_gaussian(result["determinant"]),
        "gld74_quotient_fingerprint": result["quotient_fingerprint"],
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def check() -> dict[str, object]:
    result = construct()
    canonical = canonical_certificate_bytes(result)
    stored = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in stored
    assert stored == canonical
    assert hashlib.sha256(stored).hexdigest() == CERTIFICATE_SHA256

    return {
        "status": "exact_fraction_free_quadratic_coefficient_principal_open",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_characteristic_zero_then_C",
        "invariant_raw_kernel_rank": result["invariant_fibre_rank"],
        "homogeneous_coordinate_count": 9,
        "degree_two_monomial_count": len(DEGREE_TWO_PAIRS),
        "selected_intrinsic_minor_count": len(MINOR_DESCRIPTORS),
        "quadratic_coefficient_shape_rank": [45, 45, 45],
        "normalized_determinant_at_gld72": str(result["determinant"]),
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_bytes": len(stored),
        "gld74_quotient_fingerprint": result["quotient_fingerprint"],
        "fraction_free_moving_circuit_supplied": True,
        "moving_delta_fully_expanded": False,
        "principal_open_contains_gld72": True,
        "named_source_branch_excluded_via_gld81": True,
        "exceptional_divisor_covered": False,
        "global_conjecture_resolved": False,
    }


def main() -> None:
    print("four-root fraction-free quadratic principal open: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
