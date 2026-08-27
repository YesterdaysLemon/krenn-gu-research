#!/usr/bin/env python3
"""No-import audit of the GLD82 Gaussian quadratic-span certificate.

This standard-library script imports neither the primary verifier nor any
repository Python module.  It independently parses Q(i), computes the exact
45-by-45 determinant by fraction Gaussian elimination, and checks the
projective-empty and scope semantics attached to full quadratic span.
"""

from __future__ import annotations

import hashlib
import json
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
    / "FOUR_ROOT_TORUS_STAR_SURVIVOR_INVARIANT_QUADRATIC_MACAULAY_PRINCIPAL_OPEN_NONEXTENSION_THEOREM.md"
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
        assert pivot is not None
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


def audit_certificate() -> None:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    data = json.loads(raw)
    assert data["format"] == "gaussian-quadratic-macaulay-Qi-v1"
    assert data["field"] == "Q(i)"
    assert data["variable_order"] == [
        "u0",
        "u1",
        "u2",
        "u3",
        "u4",
        "u5",
        "u6",
        "u7",
        "s",
    ]
    assert data["degree_two_monomial_order"] == [
        [left, right] for left in range(9) for right in range(left, 9)
    ]
    assert (
        len(data["minor_descriptors"])
        == len({tuple(value) for value in data["minor_descriptors"]})
        == 45
    )

    # The certificate is stored column-major.  Transpose it for elimination.
    columns = [
        [decode(coefficient) for coefficient in column] for column in data["columns"]
    ]
    assert len(columns) == 45 and all(len(column) == 45 for column in columns)
    matrix = [[columns[column][row] for column in range(45)] for row in range(45)]
    computed = determinant(matrix)
    assert computed == decode(data["determinant"]) != ZERO


def audit_scope() -> None:
    text = THEOREM.read_text(encoding="utf-8")
    required = (
        "Delta_82(F)=Omega(F) gamma_num(F) det M_ff(F)",
        "unspecified denominator-clearing exponents",
        "Only the proved necessary rank-one consequence is compressed",
        "global Krenn--Gu",
        "conjecture remain **UNRESOLVED**",
        "selected quadrics form a basis",
        "not divisor coverage or global resolution",
    )
    for phrase in required:
        assert phrase in text


def main() -> None:
    audit_certificate()
    print("independent Q(i) 45-by-45 quadratic determinant replay: PASS")
    print("full quadratic span forces projective invariant incidence empty: PASS")
    audit_scope()
    print("principal-open, source-branch, divisor, and global scope fences: PASS")
    print(
        "scope: explicit GLD82 survivor open and GLD81 named source branch; "
        "the exceptional divisor and global Krenn-Gu remain open"
    )


if __name__ == "__main__":
    main()
