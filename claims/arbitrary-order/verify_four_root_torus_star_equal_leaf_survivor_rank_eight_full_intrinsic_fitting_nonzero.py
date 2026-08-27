#!/usr/bin/env python3
"""Verify the scoped GLD85 rank-eight intrinsic-Fitting point.

GLD84 reduces the equal-leaf survivor locus to six leaf variables and two
Schur residual equations on each named rank-eight chart.  This verifier fixes
one such chart (rows 0--7), reconstructs one exact characteristic-zero point,
and evaluates the full intrinsic bordered-Pluecker coefficient map there.

The construction is exact over ``Q(i)``.  The final 45-by-45 determinant is
certified nonzero by reduction to two split-safe primes.  Every rational
denominator in the exact transported constant/response data is checked to be
invertible before reduction.  The pinned modular witnesses are kept in the
companion JSON certificate and are independently replayed by the no-import
audit; this file remains the derivation-side verifier.

This is a properness/nonzero result on one named rank-eight chart.  It does
not empty the intrinsic residual, and it makes no claim about other charts,
centre ranks, survivor components, source branches, or the global conjecture.
"""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import struct
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

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
    / "four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_certificate.json"
)
CERTIFICATE_SHA256 = "b037dc23ceebfdbce3db3ee9a48eda1e981d627c044eef45d7d87b86414adf59"

RANK_EIGHT_ROWS = tuple(range(8))
LEAF_COLUMNS = tuple(range(9, 15))
CENTRE_COLUMNS = tuple(range(8))
MIXED_ROWS = 78
CONSTANT_COLUMNS = 13
QUOTIENT_ROWS = 65
HOMOGENEOUS_COORDINATES = 9
QUADRATIC_ROWS = 45
FULL_QUOTIENT_COLUMNS = 3 * (QUOTIENT_ROWS * (QUOTIENT_ROWS - 1) // 2)

# GLD83's bordered rows: the old selected quotient chart is retained only as
# a control.  At this point every selected 15-row constant block has rank
# below 13, so its old selected M_Pl vanishes identically.
OLD_SELECTED_PIVOT_ROWS = (0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 17, 27, 53)
OLD_SELECTED_DESCRIPTORS = (
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

# Exact c and z values, encoded as (real numerator, real denominator,
# imaginary numerator, imaginary denominator).  x8 is fixed to zero.
POINT_CENTRE = (
    (4, 5, -8, 5),
    (2, 5, -4, 5),
    (-6, 5, 12, 5),
    (-12, 5, -36, 5),
    (-12, 5, -6, 5),
    (6, 5, -12, 5),
    (-6, 5, -18, 5),
    (-2, 1, 4, 1),
)
POINT_LEAF = (
    (1, 1, 0, 1),
    (0, 1, 0, 1),
    (0, 1, 0, 1),
    (0, 1, 0, 1),
    (-2, 3, 0, 1),
    (0, 1, 0, 1),
)

EXPECTED_MU = (-140, 9, -20, 9)
EXPECTED_LEAF_DET = (-1, 1, -1, 3)
EXPECTED_CENTRE_DET = (1584, 25, 3312, 25)
EXPECTED_FRAME_DENOMINATOR = (256, 3, -448, 3)
EXPECTED_OLD_GAMMA = (0, 1, 0, 1)

PRIMES = (1_000_000_007, 10_000_019)


def _load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("gld85_moving_builder", BUILDER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.build_moving_response_builder()


def _decode_gaussian(raw: Iterable[int]) -> sp.Expr:
    values = tuple(int(value) for value in raw)
    assert len(values) == 4 and values[1] and values[3]
    return sp.Rational(values[0], values[1]) + sp.I * sp.Rational(
        values[2], values[3]
    )


def _encode_gaussian(value: sp.Expr) -> list[int]:
    real, imaginary = sp.expand(value).as_real_imag()
    assert real.is_Rational and imaginary.is_Rational
    return [int(real.p), int(real.q), int(imaginary.p), int(imaginary.q)]


def _point(builder: Any) -> dict[sp.Symbol, sp.Expr]:
    shifts = builder.chart.shifts
    values = [_decode_gaussian(item) for item in POINT_CENTRE]
    values.append(sp.Integer(0))
    values.extend(_decode_gaussian(item) for item in POINT_LEAF)
    assert len(values) == 15
    return dict(zip(shifts, values, strict=True))


def _exact_rank_eight_data(builder: Any, substitutions: dict[sp.Symbol, sp.Expr]):
    """Return A,q,mu,rho and exact frames at the pinned point."""

    shifts = builder.chart.shifts
    generators = tuple(
        sp.expand(value.subs(shifts[8], 0))
        for value in builder.chart.survivor_generators
    )
    centre = sp.Matrix(shifts[:8])
    coefficient = sp.Matrix(generators).jacobian(centre)
    inhomogeneous = sp.Matrix(generators).subs({value: 0 for value in centre})
    leaf_substitutions = {
        shifts[index]: substitutions[shifts[index]] for index in LEAF_COLUMNS
    }
    A = coefficient.subs(leaf_substitutions).applyfunc(sp.expand)
    q = inhomogeneous.subs(leaf_substitutions).applyfunc(sp.expand)
    A_R = A.extract(RANK_EIGHT_ROWS, CENTRE_COLUMNS)
    q_R = q[list(RANK_EIGHT_ROWS), :]
    mu = sp.factor(A_R.det())
    adj = A_R.adjugate()
    residuals = tuple(
        sp.expand(mu * q[row, 0] - (A[row, :] * adj * q_R)[0, 0])
        for row in range(8, 10)
    )
    frames = tuple(
        frame.subs(substitutions).applyfunc(sp.expand)
        for frame in builder.chart.frames
    )
    return A, q, mu, residuals, frames


def _exact_transport_data(builder: Any, substitutions: dict[sp.Symbol, sp.Expr]):
    """Specialize U_num(C_F) and U_num(W) using the committed circuit."""

    target = builder.chart.target(builder.modules.parent).subs(substitutions)
    alpha = (
        builder.interface.reynolds_average(
            builder.interface.solve_target(target)
        )
        + builder.invariant.section_shift
    ).applyfunc(sp.expand)
    invariant_basis = builder.invariant.invariant_basis
    adjugates = tuple(
        frame.subs(substitutions).applyfunc(sp.expand).adjugate()
        for frame in builder.chart.frames
    )
    U_num = sp.kronecker_product(*adjugates)
    mixed = builder.interface.mixed_rows
    constant = (U_num * builder.interface.constant).extract(
        mixed, range(CONSTANT_COLUMNS)
    )
    response_blocks = []
    for response in builder.interface.response_maps[:3]:
        output = U_num * response
        basis_output = output * invariant_basis
        affine_output = output * alpha
        basis_mixed = basis_output.extract(mixed, range(8))
        affine_mixed = affine_output.extract(mixed, range(1))
        response_blocks.append(basis_mixed.row_join(affine_mixed).applyfunc(sp.expand))
    assert constant.shape == (MIXED_ROWS, CONSTANT_COLUMNS)
    assert all(block.shape == (MIXED_ROWS, HOMOGENEOUS_COORDINATES) for block in response_blocks)
    return constant.applyfunc(sp.expand), tuple(response_blocks)


def _old_selected_constant_rank_defects(constant: sp.Matrix, builder: Any) -> int:
    """Count old GLD83 descriptor row sets whose C_F rank is below 13."""

    quotient_rows = tuple(
        row for row in range(MIXED_ROWS) if row not in OLD_SELECTED_PIVOT_ROWS
    )
    descriptors = tuple(builder.quadratic_circuit.descriptors)
    assert descriptors == OLD_SELECTED_DESCRIPTORS
    defects = 0
    for left_row, right_row, _left_colour, _right_colour in descriptors:
        rows = OLD_SELECTED_PIVOT_ROWS + (
            quotient_rows[left_row],
            quotient_rows[right_row],
        )
        if constant.extract(rows, range(CONSTANT_COLUMNS)).rank() < CONSTANT_COLUMNS:
            defects += 1
    return defects


def _schur_response(
    response: sp.Matrix,
    *,
    rows: tuple[int, ...],
    leftovers: tuple[int, ...],
    complement_block: sp.Matrix,
    pivot_inverse: sp.Matrix,
    pivots: tuple[int, ...],
) -> sp.Matrix:
    """Take the exact two-row Schur complement for one response block."""

    values = response.extract(rows, range(HOMOGENEOUS_COORDINATES))
    return (
        values.extract(leftovers, range(HOMOGENEOUS_COORDINATES))
        - complement_block
        * pivot_inverse
        * values.extract(pivots, range(HOMOGENEOUS_COORDINATES))
    ).applyfunc(sp.expand)


def _old_selected_matrix(
    constant: sp.Matrix,
    responses: tuple[sp.Matrix, ...],
    builder: Any,
) -> sp.Matrix:
    """Evaluate GLD83's 45 selected bordered quadrics at this point.

    Each descriptor uses its own exact 13-row C_F pivot inside the named
    15-row set.  A rank-deficient set contributes a zero bordered determinant;
    otherwise the two-row Schur complement gives all 45 quadratic
    coefficients without expanding 15-by-15 determinants one monomial at a
    time.
    """

    quotient_rows = tuple(
        row for row in range(MIXED_ROWS) if row not in OLD_SELECTED_PIVOT_ROWS
    )
    descriptors = tuple(builder.quadratic_circuit.descriptors)
    columns = []
    monomials = tuple(
        (left, right)
        for left in range(HOMOGENEOUS_COORDINATES)
        for right in range(left, HOMOGENEOUS_COORDINATES)
    )
    for left_row, right_row, left_response, right_response in descriptors:
        rows = OLD_SELECTED_PIVOT_ROWS + (
            quotient_rows[left_row],
            quotient_rows[right_row],
        )
        block = constant.extract(rows, range(CONSTANT_COLUMNS))
        if block.rank() < CONSTANT_COLUMNS:
            columns.append(sp.zeros(QUADRATIC_ROWS, 1))
            continue
        pivots = tuple(block.T.rref()[1])
        assert len(pivots) == CONSTANT_COLUMNS
        leftovers = tuple(row for row in range(15) if row not in set(pivots))
        pivot_block = block.extract(pivots, range(CONSTANT_COLUMNS))
        complement_block = block.extract(leftovers, range(CONSTANT_COLUMNS))
        pivot_inverse = pivot_block.inv()

        first = _schur_response(
            responses[left_response],
            rows=rows,
            leftovers=leftovers,
            complement_block=complement_block,
            pivot_inverse=pivot_inverse,
            pivots=pivots,
        )
        second = _schur_response(
            responses[right_response],
            rows=rows,
            leftovers=leftovers,
            complement_block=complement_block,
            pivot_inverse=pivot_inverse,
            pivots=pivots,
        )
        pivot_determinant = sp.expand(pivot_block.det())
        values = []
        for left_degree, right_degree in monomials:
            value = (
                first[0, left_degree] * second[1, right_degree]
                - first[1, left_degree] * second[0, right_degree]
            )
            if left_degree != right_degree:
                value += (
                    first[0, right_degree] * second[1, left_degree]
                    - first[1, right_degree] * second[0, left_degree]
                )
            values.append(sp.expand(pivot_determinant * value))
        columns.append(sp.Matrix(values))
    result = sp.Matrix.hstack(*columns)
    assert result.shape == (QUADRATIC_ROWS, QUADRATIC_ROWS)
    return result


def _gadd(a: tuple[int, int], b: tuple[int, int], p: int) -> tuple[int, int]:
    return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)


def _gsub(a: tuple[int, int], b: tuple[int, int], p: int) -> tuple[int, int]:
    return ((a[0] - b[0]) % p, (a[1] - b[1]) % p)


def _gmul(a: tuple[int, int], b: tuple[int, int], p: int) -> tuple[int, int]:
    return (
        (a[0] * b[0] - a[1] * b[1]) % p,
        (a[0] * b[1] + a[1] * b[0]) % p,
    )


def _ginv(a: tuple[int, int], p: int) -> tuple[int, int]:
    norm = (a[0] * a[0] + a[1] * a[1]) % p
    assert norm != 0
    inverse = pow(norm, p - 2, p)
    return (a[0] * inverse % p, -a[1] * inverse % p)


def _gzero(a: tuple[int, int], p: int) -> bool:
    return a[0] % p == 0 and a[1] % p == 0


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor = 3 if divisor == 2 else divisor + 2
    return True


def _mod_exact(value: sp.Expr, p: int, denominators: list[int]) -> tuple[int, int]:
    real, imaginary = sp.expand(value).as_real_imag()
    assert real.is_Rational and imaginary.is_Rational
    for part in (real, imaginary):
        denominator = int(part.q)
        denominators.append(denominator)
        assert denominator % p != 0, (p, denominator)
    return (
        int(real.p) * pow(int(real.q), p - 2, p) % p,
        int(imaginary.p) * pow(int(imaginary.q), p - 2, p) % p,
    )


def _invert_matrix(matrix, p: int):
    n = len(matrix)
    augmented = [
        list(row) + [(1, 0) if row_index == col else (0, 0) for col in range(n)]
        for row_index, row in enumerate(matrix)
    ]
    for col in range(n):
        pivot = next(
            (row for row in range(col, n) if not _gzero(augmented[row][col], p)),
            None,
        )
        assert pivot is not None
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = _ginv(augmented[col][col], p)
        augmented[col] = [_gmul(scale, value, p) for value in augmented[col]]
        for row in range(n):
            if row == col or _gzero(augmented[row][col], p):
                continue
            factor = augmented[row][col]
            augmented[row] = [
                _gsub(left, _gmul(factor, right, p), p)
                for left, right in zip(augmented[row], augmented[col], strict=True)
            ]
    return [row[n:] for row in augmented]


def _determinant(matrix, p: int) -> tuple[int, int]:
    n = len(matrix)
    work = [list(row) for row in matrix]
    result = (1, 0)
    for col in range(n):
        pivot = next(
            (row for row in range(col, n) if not _gzero(work[row][col], p)),
            None,
        )
        if pivot is None:
            return (0, 0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = _gsub((0, 0), result, p)
        pivot_value = work[col][col]
        result = _gmul(result, pivot_value, p)
        inverse = _ginv(pivot_value, p)
        for row in range(col + 1, n):
            if _gzero(work[row][col], p):
                continue
            factor = _gmul(work[row][col], inverse, p)
            for index in range(col, n):
                work[row][index] = _gsub(
                    work[row][index], _gmul(factor, work[col][index], p), p
                )
    return result


def _quotient_rows_and_response_maps(C, W, p: int):
    """Return the exact pinned row RREF and quotient response maps modulo p."""

    work = [[C[row][col] for row in range(MIXED_ROWS)] for col in range(CONSTANT_COLUMNS)]
    pivots = []
    row = 0
    for col in range(MIXED_ROWS):
        pivot = next(
            (candidate for candidate in range(row, CONSTANT_COLUMNS)
             if not _gzero(work[candidate][col], p)),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = _ginv(work[row][col], p)
        work[row] = [_gmul(scale, value, p) for value in work[row]]
        for candidate in range(CONSTANT_COLUMNS):
            if candidate == row or _gzero(work[candidate][col], p):
                continue
            factor = work[candidate][col]
            work[candidate] = [
                _gsub(left, _gmul(factor, right, p), p)
                for left, right in zip(work[candidate], work[row], strict=True)
            ]
        pivots.append(col)
        row += 1
        if row == CONSTANT_COLUMNS:
            break
    assert tuple(pivots) == RANK_EIGHT_ROWS or len(pivots) == CONSTANT_COLUMNS
    pivot_rows = tuple(pivots)
    quotient_rows = tuple(
        row for row in range(MIXED_ROWS) if row not in set(pivot_rows)
    )
    pivot_matrix = [[C[row][col] for col in range(CONSTANT_COLUMNS)] for row in pivot_rows]
    pivot_inverse = _invert_matrix(pivot_matrix, p)
    eliminator = []
    for row in quotient_rows:
        values = []
        for col in range(CONSTANT_COLUMNS):
            value = (0, 0)
            for index in range(CONSTANT_COLUMNS):
                value = _gadd(
                    value,
                    _gmul(C[row][index], pivot_inverse[index][col], p),
                    p,
                )
            values.append(value)
        eliminator.append(values)
    quotient_maps = []
    for response in W:
        result = []
        for local_row, original_row in enumerate(quotient_rows):
            output = []
            for col in range(HOMOGENEOUS_COORDINATES):
                value = response[original_row][col]
                for pivot_index in range(CONSTANT_COLUMNS):
                    value = _gsub(
                        value,
                        _gmul(
                            eliminator[local_row][pivot_index],
                            response[pivot_rows[pivot_index]][col],
                            p,
                        ),
                        p,
                    )
                output.append(value)
            result.append(output)
        quotient_maps.append(result)
    return pivot_rows, quotient_rows, quotient_maps


def _all_quadratic_columns(quotient_maps, p: int):
    columns = []
    for left_response in range(3):
        for right_response in range(left_response + 1, 3):
            left = quotient_maps[left_response]
            right = quotient_maps[right_response]
            for row_a in range(QUOTIENT_ROWS):
                for row_b in range(row_a + 1, QUOTIENT_ROWS):
                    column = []
                    for degree_left in range(HOMOGENEOUS_COORDINATES):
                        for degree_right in range(degree_left, HOMOGENEOUS_COORDINATES):
                            value = _gsub(
                                _gmul(left[row_a][degree_left], right[row_b][degree_right], p),
                                _gmul(left[row_b][degree_left], right[row_a][degree_right], p),
                                p,
                            )
                            if degree_left != degree_right:
                                value = _gadd(
                                    value,
                                    _gsub(
                                        _gmul(left[row_a][degree_right], right[row_b][degree_left], p),
                                        _gmul(left[row_b][degree_right], right[row_a][degree_left], p),
                                        p,
                                    ),
                                    p,
                                )
                            column.append(value)
                    assert len(column) == QUADRATIC_ROWS
                    columns.append(column)
    assert len(columns) == FULL_QUOTIENT_COLUMNS
    return columns


def _pack_matrix(matrix: list[list[tuple[int, int]]]) -> str:
    raw = b"".join(
        struct.pack(">II", int(real), int(imaginary))
        for row in matrix
        for real, imaginary in row
    )
    return base64.b64encode(raw).decode("ascii")


def _matrix_digest(matrix: list[list[tuple[int, int]]]) -> str:
    raw = b"".join(
        struct.pack(">II", int(real), int(imaginary))
        for row in matrix
        for real, imaginary in row
    )
    return hashlib.sha256(raw).hexdigest()


def _modular_witness(constant: sp.Matrix, responses: tuple[sp.Matrix, ...], p: int):
    assert _is_prime(p) and p % 4 == 3
    denominators: list[int] = []
    C = [
        [_mod_exact(constant[row, col], p, denominators) for col in range(CONSTANT_COLUMNS)]
        for row in range(MIXED_ROWS)
    ]
    W = [
        [
            [_mod_exact(response[row, col], p, denominators)
             for col in range(HOMOGENEOUS_COORDINATES)]
            for row in range(MIXED_ROWS)
        ]
        for response in responses
    ]
    pivot_rows, quotient_rows, quotient_maps = _quotient_rows_and_response_maps(C, W, p)
    assert len(pivot_rows) == CONSTANT_COLUMNS
    assert len(quotient_rows) == QUOTIENT_ROWS
    columns = _all_quadratic_columns(quotient_maps, p)
    selected = _certificate_selected_columns()
    selected_matrix = [
        [columns[index][row] for index in selected] for row in range(QUADRATIC_ROWS)
    ]
    residue = _determinant(selected_matrix, p)
    return {
        "prime": p,
        "pivot_rows": list(pivot_rows),
        "quotient_rows": list(quotient_rows),
        "selected_matrix": selected_matrix,
        "selected_minor_residue": list(residue),
        "denominator_count": len(denominators),
        "denominator_nonzero_count": sum(
            denominator % p != 0 for denominator in denominators
        ),
        "selected_matrix_sha256": _matrix_digest(selected_matrix),
    }


def _certificate_selected_columns() -> list[int]:
    return [
        252, 257, 259, 260, 261, 263, 264, 267, 272, 275,
        284, 285, 286, 288, 289, 431, 433, 434, 435, 437, 438,
        441, 446, 449, 458, 459, 460, 462, 703, 704, 705, 707,
        708, 711, 716, 719, 728, 729, 805, 806, 808, 809, 812,
        855, 2784,
    ]


def _emit_certificate(builder: Any, substitutions: dict[sp.Symbol, sp.Expr]) -> None:
    constant, responses = _exact_transport_data(builder, substitutions)
    witness = [_modular_witness(constant, responses, prime) for prime in PRIMES]
    payload = {
        "format": "gld85-rank-eight-full-intrinsic-fitting-modular-witness-v1",
        "field": "Q(i)",
        "characteristic_zero_source": "exact SymPy Q(i) reconstruction from committed GLD75--GLD76 circuit",
        "rank_eight_rows": list(RANK_EIGHT_ROWS),
        "centre": [list(value) for value in POINT_CENTRE],
        "leaf": [list(value) for value in POINT_LEAF],
        "x8": [0, 1, 0, 1],
        "mu": list(EXPECTED_MU),
        "leaf_determinant": list(EXPECTED_LEAF_DET),
        "centre_determinant": list(EXPECTED_CENTRE_DET),
        "frame_denominator": list(EXPECTED_FRAME_DENOMINATOR),
        "old_selected_pivot_rows": list(OLD_SELECTED_PIVOT_ROWS),
        "old_selected_gamma": list(EXPECTED_OLD_GAMMA),
        "old_selected_M_Pl_can_vanish": True,
        "residual_V_I_Pl_empty_or_excluded": False,
        "other_rank_eight_charts_checked": False,
        "rank_seven_or_lower_checked": False,
        "global_conjecture_resolved": False,
        "quotient_dimension": QUOTIENT_ROWS,
        "full_quotient_column_count": FULL_QUOTIENT_COLUMNS,
        "selected_columns": _certificate_selected_columns(),
        "column_order": "response pairs (0,1),(0,2),(1,2), then quotient row pairs (a,b), 0<=a<b<65, lexicographic",
        "primes": [],
    }
    for item in witness:
        encoded = _pack_matrix(item.pop("selected_matrix"))
        item["selected_matrix_u32_be_base64"] = encoded
        payload["primes"].append(item)
    print(json.dumps(payload, indent=2, sort_keys=True))


def _read_certificate() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "gld85-rank-eight-full-intrinsic-fitting-modular-witness-v1"
    assert payload["field"] == "Q(i)"
    assert tuple(payload["rank_eight_rows"]) == RANK_EIGHT_ROWS
    assert tuple(tuple(item) for item in payload["centre"]) == POINT_CENTRE
    assert tuple(tuple(item) for item in payload["leaf"]) == POINT_LEAF
    assert payload["old_selected_gamma"] == list(EXPECTED_OLD_GAMMA)
    assert payload["old_selected_M_Pl_can_vanish"] is True
    assert payload["selected_columns"] == _certificate_selected_columns()
    assert len(payload["selected_columns"]) == QUADRATIC_ROWS
    assert len(set(payload["selected_columns"])) == QUADRATIC_ROWS
    assert all(0 <= value < FULL_QUOTIENT_COLUMNS for value in payload["selected_columns"])
    return payload


def _check_certificate_witness(
    witness: dict[str, Any],
    computed: dict[str, Any],
) -> None:
    assert int(witness["prime"]) == computed["prime"]
    assert tuple(witness["pivot_rows"]) == tuple(computed["pivot_rows"])
    assert tuple(witness["quotient_rows"]) == tuple(computed["quotient_rows"])
    assert int(witness["denominator_count"]) == computed["denominator_count"]
    assert int(witness["denominator_nonzero_count"]) == computed["denominator_nonzero_count"]
    assert computed["denominator_count"] == computed["denominator_nonzero_count"]
    encoded = base64.b64decode(witness["selected_matrix_u32_be_base64"], validate=True)
    assert len(encoded) == QUADRATIC_ROWS * QUADRATIC_ROWS * 8
    stored = [
        [tuple(struct.unpack(">II", encoded[offset:offset + 8]))
         for offset in range(row * QUADRATIC_ROWS * 8, (row + 1) * QUADRATIC_ROWS * 8, 8)]
        for row in range(QUADRATIC_ROWS)
    ]
    assert stored == computed["selected_matrix"]
    assert witness["selected_matrix_sha256"] == computed["selected_matrix_sha256"]
    assert tuple(witness["selected_minor_residue"]) == tuple(computed["selected_minor_residue"])
    assert tuple(computed["selected_minor_residue"]) != (0, 0)


def check(builder: Any | None = None) -> dict[str, object]:
    payload = _read_certificate()
    builder = builder or _load_builder()
    substitutions = _point(builder)

    A, q, mu, residuals, frames = _exact_rank_eight_data(builder, substitutions)
    assert A.shape == (10, 8) and q.shape == (10, 1)
    assert mu == _decode_gaussian(EXPECTED_MU)
    assert residuals == (sp.Integer(0), sp.Integer(0))
    assert all(
        sp.simplify(entry.subs(substitutions)) == 0
        for entry in builder.chart.survivor_generators
    )

    leaf_det = sp.factor(frames[1].det())
    centre_det = sp.factor(frames[0].det())
    frame_denominator = sp.factor(sp.prod(frame.det() for frame in frames))
    assert sp.simplify(leaf_det - _decode_gaussian(EXPECTED_LEAF_DET)) == 0
    assert sp.simplify(centre_det - _decode_gaussian(EXPECTED_CENTRE_DET)) == 0
    assert (
        sp.simplify(
            frame_denominator - _decode_gaussian(EXPECTED_FRAME_DENOMINATOR)
        )
        == 0
    )

    constant, responses = _exact_transport_data(builder, substitutions)
    assert constant.rank() == CONSTANT_COLUMNS
    old_gamma = sp.factor(
        constant.extract(OLD_SELECTED_PIVOT_ROWS, range(CONSTANT_COLUMNS)).det()
    )
    assert sp.simplify(old_gamma - _decode_gaussian(EXPECTED_OLD_GAMMA)) == 0
    old_defects = _old_selected_constant_rank_defects(constant, builder)
    old_selected_matrix = _old_selected_matrix(constant, responses, builder)
    assert old_selected_matrix == sp.zeros(QUADRATIC_ROWS, QUADRATIC_ROWS)

    computed_witnesses = [
        _modular_witness(constant, responses, prime) for prime in PRIMES
    ]
    stored_witnesses = {int(item["prime"]): item for item in payload["primes"]}
    assert set(stored_witnesses) == set(PRIMES)
    for computed in computed_witnesses:
        _check_certificate_witness(stored_witnesses[computed["prime"]], computed)

    return {
        "status": "exact_rank_eight_full_intrinsic_fitting_nonzero_point",
        "theorem_id": "GLD85",
        "field": "Q(i)_characteristic_zero_with_two_exact_modular_reductions",
        "global_conjecture": "UNRESOLVED",
        "chart": "GLD84 named rank-eight Schur chart: rows 0..7, six leaf variables x9..x14, residuals rho_8=rho_9=0",
        "point_centre": [list(value) for value in POINT_CENTRE],
        "point_leaf": [list(value) for value in POINT_LEAF],
        "rank_eight_schur_mu": list(EXPECTED_MU),
        "rank_eight_residuals": ["0", "0"],
        "frame_open_values": {
            "det_leaf": list(EXPECTED_LEAF_DET),
            "det_centre": list(EXPECTED_CENTRE_DET),
            "frame_denominator": list(EXPECTED_FRAME_DENOMINATOR),
            "gauge_factor": "1",
        },
        "full_constant_block_shape_rank": [MIXED_ROWS, CONSTANT_COLUMNS, CONSTANT_COLUMNS],
        "full_intrinsic_fitting_map_shape": [QUADRATIC_ROWS, FULL_QUOTIENT_COLUMNS],
        "quotient_pivot_rows": list(computed_witnesses[0]["pivot_rows"]),
        "quotient_rows": list(computed_witnesses[0]["quotient_rows"]),
        "selected_columns": _certificate_selected_columns(),
        "selected_column_count": QUADRATIC_ROWS,
        "modular_primes": list(PRIMES),
        "modular_minor_residues": {
            str(item["prime"]): list(item["selected_minor_residue"])
            for item in computed_witnesses
        },
        "denominator_checks": {
            str(item["prime"]): {
                "checked": item["denominator_count"],
                "invertible": item["denominator_nonzero_count"],
            }
            for item in computed_witnesses
        },
        "full_intrinsic_fitting_ideal_nonzero_at_point": True,
        "full_intrinsic_fitting_open_proper_on_named_chart": True,
        "old_selected_M_Pl_can_vanish": True,
        "old_selected_M_Pl_control": {
            "pivot_rows": list(OLD_SELECTED_PIVOT_ROWS),
            "gamma": list(EXPECTED_OLD_GAMMA),
            "descriptor_count": len(OLD_SELECTED_DESCRIPTORS),
            "selected_constant_row_sets_rank_below_13": old_defects,
            "all_selected_constant_row_sets_rank_below_13": old_defects
            == len(OLD_SELECTED_DESCRIPTORS),
            "old_selected_matrix_is_zero_at_point": True,
        },
        "residual_V_I_Pl_empty_or_excluded": False,
        "other_rank_eight_charts_checked": False,
        "rank_seven_or_lower_checked": False,
        "other_survivor_components_or_gauges_checked": False,
        "global_conjecture_resolved": False,
        "certificate_format": payload["format"],
    }


def main() -> None:
    builder = _load_builder()
    substitutions = _point(builder)
    if "--emit-certificate" in sys.argv[1:]:
        _emit_certificate(builder, substitutions)
        return
    result = check(builder)
    print("four-root rank-eight full intrinsic Fitting point: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
