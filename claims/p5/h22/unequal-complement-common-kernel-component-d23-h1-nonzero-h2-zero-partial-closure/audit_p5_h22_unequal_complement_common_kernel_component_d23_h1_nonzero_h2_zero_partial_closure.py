#!/usr/bin/env python3
"""Independent audit of component 22's H=h2=0 three-divisor closure."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)

started = time.perf_counter()
root = Path(__file__).resolve().parent
note = root / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_"
    "H2_ZERO_PARTIAL_CLOSURE.md"
)

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
s = 2 * A + R

alpha, canonical = component_rows(A, R, D)
marked = shifted(canonical, alpha, (h0, h1, h2, h3))
model = build_model(alpha, marked, x, "D23", "finite", rho)
mixed_matrix = sp.Matrix(
    [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
)


def gaussian_determinant(rows, field):
    """Determinant by explicit field Gaussian elimination with row swaps."""
    matrix = [list(row) for row in rows]
    sign = field.one
    size = len(matrix)
    for column in range(size):
        pivot_row = next(
            (row for row in range(column, size) if matrix[row][column]), None
        )
        if pivot_row is None:
            return field.zero
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]
            sign = -sign
        pivot = matrix[column][column]
        for row in range(column + 1, size):
            if not matrix[row][column]:
                continue
            multiplier = matrix[row][column] / pivot
            matrix[row][column] = field.zero
            for index in range(column + 1, size):
                matrix[row][index] -= multiplier * matrix[column][index]
    determinant = sign
    for index in range(size):
        determinant *= matrix[index][index]
    return determinant


def verify_determinant(row_indices, substitutions, clearing_factor, expected):
    matrix = mixed_matrix.extract(row_indices, range(8)).subs(
        substitutions, simultaneous=True
    )
    symbols = sorted(
        set().union(
            *(entry.free_symbols for entry in matrix),
            clearing_factor.free_symbols,
            expected.free_symbols,
        ),
        key=str,
    )
    field = sp.QQ.frac_field(*symbols)
    rows = [
        [field.from_sympy(matrix[row, column]) for column in range(8)]
        for row in range(8)
    ]
    actual = gaussian_determinant(rows, field) * field.from_sympy(
        clearing_factor
    ) ** 8
    assert actual == field.from_sympy(expected)


base_substitutions = {h1: -1 / (2 * A), h2: 0}

q1 = D * h0 + 1
verify_determinant(
    (1, 2, 3, 5, 6, 7, 10, 11),
    {**base_substitutions, rho: 1},
    2 * A,
    2**16 * A**9 * D**4 * (A + R) ** 2 * s**2 * (D + 1) * q1,
)
verify_determinant(
    (2, 3, 5, 6, 10, 11, 12, 13),
    {**base_substitutions, rho: 1, h0: -1 / D},
    2 * A,
    2**12 * A**7 * D**3 * (A - R) * (A + R) * s**3 * (D + 1) ** 3,
)

rho6 = -(D + 1) / (D - 1)
q6 = D * s * h0 + A - D * (A + R)
h0_6 = (D * (A + R) - A) / (D * s)
p6 = (
    6 * A**2 * D**2
    - 2 * A**2
    + A * D**4 * R
    + 5 * A * D**2 * R
    + 2 * A * D**2 * h3
    - 2 * A * R
    - 6 * A * h3
    + 2 * D**2 * R**2
    + 2 * D**2 * R * h3
    - R**2
    - 4 * R * h3
)
e6 = (A + R) * D**2 - 3 * A - 2 * R
h3_6 = -sp.Poly(p6, h3).nth(0) / (2 * e6)
verify_determinant(
    (0, 1, 2, 3, 6, 7, 9, 11),
    {**base_substitutions, rho: rho6},
    2 * A * (D - 1),
    2**17 * A**9 * D**4 * s**5 * (D - 1) ** 2 * (D + 1) ** 3 * q6,
)
verify_determinant(
    (0, 1, 2, 3, 6, 7, 9, 10),
    {**base_substitutions, rho: rho6, h0: h0_6},
    2 * A * (D - 1),
    -(2**16) * A**10 * D**4 * s**4 * (D - 1) * (D + 1) ** 3 * p6,
)
verify_determinant(
    (0, 1, 2, 3, 6, 7, 9, 12),
    {**base_substitutions, rho: rho6, h0: h0_6, h3: h3_6},
    2 * A * (D - 1) * e6,
    -(2**15)
    * A**9
    * D**4
    * s**6
    * (D - 1) ** 2
    * (D + 1) ** 4
    * (A * D**2 - 5 * A - 2 * R)
    * e6**7
    * (A * D**2 + A + 2 * D**2 * R - R),
)

n8 = A * D - A + R * D
d8 = A * D + A + R * D
rho8 = -n8 / d8
q8 = D * R * s * h0 - A**2 * (D + 1) - D * R * s
h0_8 = (A**2 * (D + 1) + D * R * s) / (D * R * s)
p8 = A**2 * D**2 + 5 * A**2 + A * D**2 * R + 4 * A * R + 2 * A * h3 + R**2 + 2 * R * h3
h3_8 = -sp.Poly(p8, h3).nth(0) / (2 * (A + R))
c81 = A**2 * D**2 - A**2 + A * D**2 * R - 5 * A * R - 2 * R**2
c82 = A**2 * D**2 - A**2 + 3 * A * D**2 * R + A * R + 2 * D**2 * R**2
verify_determinant(
    (0, 1, 2, 3, 6, 7, 9, 11),
    {**base_substitutions, rho: rho8},
    d8,
    -(2**10) * A**4 * D**4 * (A + R) ** 2 * s**5 * (D - 1) * (D + 1) ** 2 * n8 * d8 * q8,
)
verify_determinant(
    (0, 1, 2, 3, 6, 7, 9, 10),
    {**base_substitutions, rho: rho8, h0: h0_8},
    R * d8,
    2**9 * A**5 * D**4 * R**9 * (A + R) ** 2 * s**4 * (D - 1) * (D + 1) ** 3 * n8 * d8 * p8,
)
verify_determinant(
    (0, 1, 2, 3, 6, 7, 9, 12),
    {**base_substitutions, rho: rho8, h0: h0_8, h3: h3_8},
    R * (A + R) * d8,
    2**8 * A**4 * D**4 * R**8 * (A + R) ** 8 * s**6 * (D + 1) ** 2 * n8 * d8 * c81 * c82,
)

print(
    json.dumps(
        {
            "status": "PASS",
            "component": 22,
            "slice": "H=0, h2=0, rho*(rho+1)!=0",
            "closed_divisors": ["rho=1", "f6=0", "f8=0"],
            "matrix_reconstruction": "independent low-level model build",
            "determinant_algorithm": "explicit Gaussian elimination over rational function fields",
            "determinants_checked": 8,
            "other_h2_zero_cases_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
            "theorem_sha256": hashlib.sha256(note.read_bytes()).hexdigest(),
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
