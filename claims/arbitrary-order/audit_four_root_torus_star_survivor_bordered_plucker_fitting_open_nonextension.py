#!/usr/bin/env python3
"""Independent no-import audit of the GLD83 bordered-Pluecker reduction.

This standard-library audit imports no repository Python module.  It replays
the pinned Gaussian determinant over Q(i), checks the gamma-free scaling and
finite exterior indexing, and tests the bordered block identity on exact
nonsingular, singular-pivot, and constant-rank-drop controls.  The universal
polynomial identity and Fitting-open implication remain the written proof.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_invariant_quadratic_macaulay_certificate.json"
)
THEOREM = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_THEOREM.md"
)
EXPECTED_SHA256 = "4cdaf08a5f5dc40abc845d4dc1e6046ce3b259b2c751dfd3ec2955e5b94e65e0"

Gaussian = tuple[Fraction, Fraction]
ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def subtract(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def power(value: Gaussian, exponent: int) -> Gaussian:
    assert exponent >= 0
    result = ONE
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        remaining >>= 1
    return result


def divide(left: Gaussian, right: Gaussian) -> Gaussian:
    norm = right[0] * right[0] + right[1] * right[1]
    assert norm != 0
    return (
        (left[0] * right[0] + left[1] * right[1]) / norm,
        (left[1] * right[0] - left[0] * right[1]) / norm,
    )


def decode(raw: list[int]) -> Gaussian:
    assert len(raw) == 4
    return (Fraction(raw[0], raw[1]), Fraction(raw[2], raw[3]))


def integer(value: int) -> Gaussian:
    return (Fraction(value), Fraction(0))


def determinant(matrix: list[list[Gaussian]]) -> Gaussian:
    size = len(matrix)
    assert size > 0 and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    output = ONE
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            return ZERO
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            output = (-output[0], -output[1])
        pivot_value = work[column][column]
        output = multiply(output, pivot_value)
        for row in range(column + 1, size):
            if work[row][column] == ZERO:
                continue
            factor = divide(work[row][column], pivot_value)
            for index in range(column, size):
                work[row][index] = subtract(
                    work[row][index], multiply(factor, work[column][index])
                )
    return output


def rows_from_columns(columns: list[list[Gaussian]]) -> list[list[Gaussian]]:
    height = len(columns[0])
    assert all(len(column) == height for column in columns)
    return [[column[row] for column in columns] for row in range(height)]


def bordered_control(
    constant_columns: list[list[Gaussian]],
    left: list[Gaussian],
    right: list[Gaussian],
) -> tuple[Gaussian, Gaussian, Gaussian]:
    assert len(constant_columns) == 2
    assert all(len(column) == 4 for column in [*constant_columns, left, right])
    constant = rows_from_columns(constant_columns)
    pivot = [row[:2] for row in constant[:2]]
    gamma = determinant(pivot)
    # adj([[a,b],[c,d]])
    adjugate = [
        [pivot[1][1], (-pivot[0][1][0], -pivot[0][1][1])],
        [(-pivot[1][0][0], -pivot[1][0][1]), pivot[0][0]],
    ]

    def qnum(vector: list[Gaussian]) -> list[Gaussian]:
        result = []
        for row in range(2, 4):
            correction = ZERO
            for middle in range(2):
                adj_times_pivot = ZERO
                for column in range(2):
                    adj_times_pivot = add(
                        adj_times_pivot,
                        multiply(adjugate[middle][column], vector[column]),
                    )
                correction = add(
                    correction,
                    multiply(constant[row][middle], adj_times_pivot),
                )
            result.append(subtract(multiply(gamma, vector[row]), correction))
        return result

    projected_minor = determinant(rows_from_columns([qnum(left), qnum(right)]))
    bordered = determinant(rows_from_columns([*constant_columns, left, right]))
    assert projected_minor == multiply(gamma, bordered)
    return gamma, bordered, projected_minor


def audit_certificate_and_scaling() -> None:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    data = json.loads(raw)
    assert data["format"] == "gaussian-quadratic-macaulay-Qi-v1"
    assert data["field"] == "Q(i)"
    assert len(data["minor_descriptors"]) == 45

    columns = [
        [decode(coefficient) for coefficient in column] for column in data["columns"]
    ]
    normalized = determinant(rows_from_columns(columns))
    assert normalized == decode(data["determinant"]) != ZERO

    d_value: Gaussian = (Fraction(24), Fraction(-24))
    gamma_value: Gaussian = (
        Fraction(-692533995824480256),
        Fraction(-692533995824480256),
    )
    pluecker_scalar = multiply(power(d_value, 2), gamma_value)
    pluecker_determinant = multiply(power(pluecker_scalar, 45), normalized)
    fraction_free_determinant = multiply(
        power(multiply(d_value, gamma_value), 90), normalized
    )
    assert pluecker_determinant != ZERO
    assert fraction_free_determinant == multiply(
        power(gamma_value, 45), pluecker_determinant
    )


def audit_bordered_controls() -> None:
    # Nonsingular selected pivot.
    nonsingular = bordered_control(
        [
            [integer(1), ZERO, integer(1), integer(2)],
            [ZERO, integer(1), integer(3), integer(5)],
        ],
        [integer(2), integer(1), integer(0), integer(1)],
        [integer(1), integer(4), integer(1), integer(0)],
    )
    assert nonsingular[0] != ZERO

    # The selected 2-row pivot is singular, while the full constant block has
    # rank two and the bordered determinant is nonzero.  This is an algebraic
    # chart control, not an asserted survivor point.
    singular_pivot = bordered_control(
        [[integer(1), integer(2), ZERO, ZERO], [ZERO, ZERO, integer(1), ZERO]],
        [ZERO, integer(1), ZERO, ZERO],
        [ZERO, ZERO, ZERO, integer(1)],
    )
    assert singular_pivot[0] == ZERO
    assert singular_pivot[1] != ZERO
    assert singular_pivot[2] == ZERO

    # Rank drop below the number of constant columns kills every bordered
    # determinant, whatever the two response columns.
    constant_rank_drop = bordered_control(
        [
            [integer(1), integer(2), integer(3), integer(4)],
            [integer(2), integer(4), integer(6), integer(8)],
        ],
        [integer(0), integer(1), integer(0), integer(1)],
        [integer(1), integer(0), integer(1), integer(0)],
    )
    assert constant_rank_drop[1] == ZERO


def audit_dimensions_and_scope() -> None:
    assert math.comb(9 + 1, 2) == 45
    assert math.comb(78, 15) == 4367914309753280
    assert 3 * math.comb(78, 15) == 13103742929259840

    text = THEOREM.read_text(encoding="utf-8")
    required = (
        "Delta_83(F)=Omega(F) det M_Pl(F)",
        "M_ff=gamma_num M_Pl",
        "Delta_82=gamma_num^46 Delta_83",
        "I_Pl=I_45(A_Pl)=Fitt_0(coker A_Pl)",
        "The full Fitting open is an exact finite union",
        "not a practical enumeration",
        "global Krenn--Gu conjecture remain",
        "**UNRESOLVED**",
    )
    for phrase in required:
        assert phrase in text


def main() -> None:
    audit_certificate_and_scaling()
    print("independent Q(i) gamma-free Gaussian scaling replay: PASS")
    audit_bordered_controls()
    print("bordered determinant pivot and rank-drop controls: PASS")
    audit_dimensions_and_scope()
    print("full exterior/Fitting dimensions and scope fences: PASS")
    print(
        "scope: GLD83 bordered principal and Fitting opens; intrinsic rank-drop "
        "locus, other branches, and global Krenn-Gu remain open"
    )


if __name__ == "__main__":
    main()
