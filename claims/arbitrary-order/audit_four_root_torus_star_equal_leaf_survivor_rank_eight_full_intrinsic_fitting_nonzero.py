#!/usr/bin/env python3
"""Independent no-import audit for the GLD85 modular witness.

This audit deliberately does not import SymPy, the moving-response builder,
or the GLD85 primary verifier.  It decodes the pinned 45-by-45 matrices from
the durable certificate and redoes the Gaussian-extension determinant with a
separate standard-library implementation.  Thus it audits the exact modular
arithmetic and certificate indexing, while the primary verifier audits how
those matrices were derived from the committed response circuit.

The characteristic-zero implication is the elementary one: a zero exact
Gaussian-rational determinant reduces to zero at every prime for which all
input denominators are units.  The primary records and checks those
denominators; this audit checks the recorded denominator counts and the two
nonzero determinant residues independently.
"""

from __future__ import annotations

import base64
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_certificate.json"
)
CERTIFICATE_SHA256 = "b037dc23ceebfdbce3db3ee9a48eda1e981d627c044eef45d7d87b86414adf59"

FORMAT = "gld85-rank-eight-full-intrinsic-fitting-modular-witness-v1"
ROWS = 45
FULL_COLUMNS = 6240
EXPECTED_PIVOTS = (0, 1, 2, 3, 4, 5, 7, 8, 12, 17, 19, 26, 52)
EXPECTED_QUOTIENT = tuple(
    row for row in range(78) if row not in set(EXPECTED_PIVOTS)
)
EXPECTED_SELECTED = (
    252, 257, 259, 260, 261, 263, 264, 267, 272, 275,
    284, 285, 286, 288, 289, 431, 433, 434, 435, 437, 438,
    441, 446, 449, 458, 459, 460, 462, 703, 704, 705, 707,
    708, 711, 716, 719, 728, 729, 805, 806, 808, 809, 812,
    855, 2784,
)
EXPECTED_RESIDUES = {
    1_000_000_007: (9_639_769, 249_939_722),
    10_000_019: (1_610_829, 5_232_695),
}
EXPECTED_DENOMINATORS = 6240


def _add(a: tuple[int, int], b: tuple[int, int], p: int) -> tuple[int, int]:
    return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)


def _subtract(a: tuple[int, int], b: tuple[int, int], p: int) -> tuple[int, int]:
    return ((a[0] - b[0]) % p, (a[1] - b[1]) % p)


def _multiply(a: tuple[int, int], b: tuple[int, int], p: int) -> tuple[int, int]:
    return (
        (a[0] * b[0] - a[1] * b[1]) % p,
        (a[0] * b[1] + a[1] * b[0]) % p,
    )


def _inverse(a: tuple[int, int], p: int) -> tuple[int, int]:
    norm = (a[0] * a[0] + a[1] * a[1]) % p
    assert norm != 0
    inverse_norm = pow(norm, p - 2, p)
    return (a[0] * inverse_norm % p, -a[1] * inverse_norm % p)


def _is_zero(a: tuple[int, int], p: int) -> bool:
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


def _determinant(matrix: list[list[tuple[int, int]]], p: int) -> tuple[int, int]:
    """Bareiss-shaped elimination in F_p[i], independently written."""

    work = [list(row) for row in matrix]
    sign = (1, 0)
    for pivot_column in range(ROWS):
        pivot_row = next(
            (
                row
                for row in range(pivot_column, ROWS)
                if not _is_zero(work[row][pivot_column], p)
            ),
            None,
        )
        assert pivot_row is not None
        if pivot_row != pivot_column:
            work[pivot_column], work[pivot_row] = (
                work[pivot_row],
                work[pivot_column],
            )
            sign = _subtract((0, 0), sign, p)
        pivot = work[pivot_column][pivot_column]
        inverse = _inverse(pivot, p)
        for row in range(pivot_column + 1, ROWS):
            if _is_zero(work[row][pivot_column], p):
                continue
            multiplier = _multiply(work[row][pivot_column], inverse, p)
            for column in range(pivot_column, ROWS):
                work[row][column] = _subtract(
                    work[row][column],
                    _multiply(multiplier, work[pivot_column][column], p),
                    p,
                )
    result = sign
    for index in range(ROWS):
        result = _multiply(result, work[index][index], p)
    return result


def _unpack(payload: str, p: int) -> tuple[list[list[tuple[int, int]]], bytes]:
    raw = base64.b64decode(payload, validate=True)
    assert len(raw) == ROWS * ROWS * 8
    matrix = []
    cursor = 0
    for _row in range(ROWS):
        current = []
        for _column in range(ROWS):
            real, imaginary = struct.unpack(">II", raw[cursor:cursor + 8])
            cursor += 8
            assert real < p and imaginary < p
            current.append((real, imaginary))
        matrix.append(current)
    assert cursor == len(raw)
    return matrix, raw


def _check_point_metadata(payload: dict[str, object]) -> None:
    assert payload["field"] == "Q(i)"
    assert payload["rank_eight_rows"] == list(range(8))
    assert payload["centre"] == [
        [4, 5, -8, 5],
        [2, 5, -4, 5],
        [-6, 5, 12, 5],
        [-12, 5, -36, 5],
        [-12, 5, -6, 5],
        [6, 5, -12, 5],
        [-6, 5, -18, 5],
        [-2, 1, 4, 1],
    ]
    assert payload["leaf"] == [
        [1, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [-2, 3, 0, 1],
        [0, 1, 0, 1],
    ]
    assert payload["x8"] == [0, 1, 0, 1]
    assert payload["mu"] == [-140, 9, -20, 9]
    assert payload["leaf_determinant"] == [-1, 1, -1, 3]
    assert payload["centre_determinant"] == [1584, 25, 3312, 25]
    assert payload["frame_denominator"] == [256, 3, -448, 3]


def check() -> dict[str, object]:
    raw_certificate = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw_certificate
    assert hashlib.sha256(raw_certificate).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw_certificate)
    assert payload["format"] == FORMAT
    _check_point_metadata(payload)
    assert tuple(payload["selected_columns"]) == EXPECTED_SELECTED
    assert len(EXPECTED_SELECTED) == ROWS
    assert len(set(EXPECTED_SELECTED)) == ROWS
    assert all(0 <= value < FULL_COLUMNS for value in EXPECTED_SELECTED)
    assert tuple(payload["old_selected_pivot_rows"]) == (
        0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 17, 27, 53
    )
    assert payload["quotient_dimension"] == 65
    assert payload["full_quotient_column_count"] == FULL_COLUMNS

    prime_records = {int(item["prime"]): item for item in payload["primes"]}
    assert set(prime_records) == set(EXPECTED_RESIDUES)
    results = {}
    for prime, expected in EXPECTED_RESIDUES.items():
        assert _is_prime(prime) and prime % 4 == 3
        record = prime_records[prime]
        assert tuple(record["pivot_rows"]) == EXPECTED_PIVOTS
        assert tuple(record["quotient_rows"]) == EXPECTED_QUOTIENT
        assert record["denominator_count"] == EXPECTED_DENOMINATORS
        assert record["denominator_nonzero_count"] == EXPECTED_DENOMINATORS
        matrix, raw_matrix = _unpack(record["selected_matrix_u32_be_base64"], prime)
        digest = hashlib.sha256(raw_matrix).hexdigest()
        assert record["selected_matrix_sha256"] == digest
        residue = _determinant(matrix, prime)
        assert residue == expected
        assert residue != (0, 0)
        assert tuple(record["selected_minor_residue"]) == expected
        results[str(prime)] = {
            "determinant_residue": list(residue),
            "matrix_sha256": digest,
            "denominators_checked": EXPECTED_DENOMINATORS,
        }

    # These are explicit scope fences, not conclusions inferred from a
    # nonzero modular minor.
    assert payload["old_selected_M_Pl_can_vanish"] is True
    assert payload["residual_V_I_Pl_empty_or_excluded"] is False
    assert payload["other_rank_eight_charts_checked"] is False
    assert payload["rank_seven_or_lower_checked"] is False
    assert payload["global_conjecture_resolved"] is False
    return {
        "status": "independent_no_import_modular_witness_audit_pass",
        "theorem_id": "GLD85",
        "field": "F_p[i] with p == 3 mod 4",
        "modular_witnesses": results,
        "characteristic_zero_implication": "nonzero reduction with every exact input denominator a unit implies the Q(i) determinant is nonzero",
        "full_intrinsic_fitting_map": [45, FULL_COLUMNS],
        "old_selected_M_Pl_can_vanish": True,
        "intrinsic_residual_empty_or_excluded": False,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    print("four-root rank-eight full intrinsic Fitting independent audit: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
