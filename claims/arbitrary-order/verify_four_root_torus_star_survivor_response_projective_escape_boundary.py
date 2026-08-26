#!/usr/bin/env python3
"""Verify exact raw-fibre directions on the GLD74 projective boundary.

The two sparse vectors below are durable witnesses.  The verifier rebuilds
the GLD74 quotient, checks the full proportionality matrices have rank 34,
and replays the vectors as rank-one directions at infinity.  They are not
affine response lifts.
"""

from __future__ import annotations

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

ESCAPE_WITNESSES = (
    (
        -1,
        1,
        {
            13: -1,
            15: 1,
            22: 1,
            24: -1,
            31: -1,
            33: 1,
        },
    ),
    (
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
    ),
)


def load_gld74():
    spec = importlib.util.spec_from_file_location("gld74_full_fibre", GLD74)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_s3_reduction():
    spec = importlib.util.spec_from_file_location("gld76_s3_reduction", S3_REDUCTION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gaussian_nullspace(gld73, matrix: sp.Matrix):
    work = [
        [gld73.gaussian(sp.expand(matrix[row, column])) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]
    pivot_row = 0
    pivots = []
    for column in range(matrix.cols):
        pivot = next(
            (
                row
                for row in range(pivot_row, matrix.rows)
                if work[row][column] != gld73.GZERO
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gld73.gdiv(value, scale) for value in work[pivot_row]]
        for row in range(matrix.rows):
            if row == pivot_row or work[row][column] == gld73.GZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gld73.gsub(value, gld73.gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
    free = tuple(column for column in range(matrix.cols) if column not in set(pivots))
    vectors = []
    for free_column in free:
        vector = [gld73.GZERO] * matrix.cols
        vector[free_column] = gld73.GONE
        for row, pivot in enumerate(pivots):
            vector[pivot] = gld73.gsub(gld73.GZERO, work[row][free_column])
        vectors.append(vector)
    return tuple(pivots), free, vectors


def sympy_gaussian(value):
    real, imaginary = value
    return sp.Rational(real.numerator, real.denominator) + sp.I * sp.Rational(
        imaginary.numerator, imaginary.denominator
    )


def check():
    gld74 = load_gld74()
    s3_reduction = load_s3_reduction()
    gld73 = gld74.load_gld73()
    data = gld74.quotient_forms()
    matrices = [
        sp.Matrix(
            [data["coefficient_rows"][row][column][:35] for row in range(65)]
        )
        for column in range(3)
    ]
    k0, k1, k2 = matrices
    transformed = gld74.transformed_map()
    _particular, raw_kernel, _pivots, _free = gld74.affine_fibre(
        transformed[0], transformed[4], transformed[5]
    )
    descriptors = s3_reduction.raw_descriptors()
    witnesses = []
    for a, b, sparse_vector in ESCAPE_WITNESSES:
        proportionality = (a * k0 - k1).col_join(b * k0 - k2)
        pivots, free, kernel = gaussian_nullspace(gld73, proportionality)
        assert len(pivots) == 34 and len(free) == len(kernel) == 1
        vector = sp.zeros(35, 1)
        for index, value in sparse_vector.items():
            vector[index] = value
        computed = sp.Matrix([sympy_gaussian(value) for value in kernel[0]])
        assert computed == vector
        assert all(sp.expand(value) == 0 for value in proportionality * vector)
        z0, z1, z2 = (matrix * vector for matrix in matrices)
        assert z0 != sp.zeros(65, 1)
        assert all(sp.expand(value) == 0 for value in z1 - a * z0)
        assert all(sp.expand(value) == 0 for value in z2 - b * z0)
        assert sp.Matrix.hstack(z0, z1, z2).rank() == 1
        raw_direction = raw_kernel * vector
        for sigma in permutations((1, 2, 3)):
            inversions = sum(
                sigma[left] > sigma[right]
                for left in range(3)
                for right in range(left + 1, 3)
            )
            sign = -1 if inversions % 2 else 1
            raw_action = s3_reduction.permutation_matrix(descriptors, (0, *sigma))
            assert raw_action * raw_direction == sign * raw_direction
        witnesses.append(
            {
                "a": a,
                "b": b,
                "free_coordinate": free[0],
                "support_size": len(sparse_vector),
                "leaf_s3_type": "sign",
                "t": [str(sp.expand(value)) for value in vector],
                "nonzero_z0_coordinate": next(
                    index for index, value in enumerate(z0) if value != 0
                ),
            }
        )
    return {
        "status": "exact_projective_escape_witnesses_not_affine_response_lifts",
        "global_conjecture": "UNRESOLVED",
        "quotient_linear_shape": [65, 3, 35],
        "witnesses": witnesses,
        "affine_response_lift_constructed": False,
        "whole_survivor_locus_response_excluded": False,
    }


def main():
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
