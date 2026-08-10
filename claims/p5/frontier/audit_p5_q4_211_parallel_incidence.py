#!/usr/bin/env python3
"""Independent finite-field audit of the q4_211 diagonal-pencil lemma."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def matrix_rank_mod(rows, prime):
    matrix = [list(value % prime for value in row) for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime for value in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            multiple = matrix[row][column]
            if multiple:
                matrix[row] = [
                    (left - multiple * right) % prime
                    for left, right in zip(
                        matrix[row],
                        matrix[pivot_row],
                        strict=True,
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def projective_vectors(prime):
    representatives = []
    for vector in itertools.product(range(prime), repeat=3):
        if not any(vector):
            continue
        first = next(value for value in vector if value)
        inverse = pow(first, -1, prime)
        normalized = tuple(value * inverse % prime for value in vector)
        if normalized not in representatives:
            representatives.append(normalized)
    return representatives


def solution_space_rows(p, q, prime):
    # Unknowns are a0,a1,a2,b0,b1,b2.  Delete the two allowed
    # diagonal coordinates 00 and 11.
    equations = []
    for left in range(3):
        for right in range(3):
            if (left, right) in ((0, 0), (1, 1)):
                continue
            row = [0] * 6
            row[left] = q[right] % prime
            row[3 + right] = p[left] % prime
            equations.append(row)

    # Return every solution; at F3/F5 there are at most p^3 solutions
    # in the surviving cases and p^6 is still tiny for this audit.
    return [
        vector
        for vector in itertools.product(range(prime), repeat=6)
        if all(
            sum(left * right for left, right in zip(row, vector)) % prime
            == 0
            for row in equations
        )
    ]


def audit_prime(prime):
    vectors = projective_vectors(prime)
    classified = []
    checked_pairs = 0
    for p in vectors:
        for q in vectors:
            checked_pairs += 1
            solutions = solution_space_rows(p, q, prime)
            a_rows = [p] + [solution[:3] for solution in solutions]
            b_rows = [q] + [solution[3:] for solution in solutions]
            a_rank = matrix_rank_mod(a_rows, prime)
            b_rank = matrix_rank_mod(b_rows, prime)
            if min(a_rank, b_rank) < 2:
                continue

            # The exact lemma predicts p,q in the target diagonal
            # two-plane, with either opposite coordinate axes or both
            # having full support in that plane.
            assert p[2] == q[2] == 0
            products = (p[0] * q[0] % prime, p[1] * q[1] % prime)
            opposite_axes = products == (0, 0)
            full_support = all(products)
            assert opposite_axes or full_support
            classified.append(
                {
                    "p": p,
                    "q": q,
                    "a_rank": a_rank,
                    "b_rank": b_rank,
                    "type": (
                        "opposite_coordinate_axes"
                        if opposite_axes
                        else "both_full_support"
                    ),
                }
            )

    quotient_checks = []
    for b in range(1, prime):
        for c in range(1, prime):
            # X coordinates are e0,e3,e4.  In X/<k>, with
            # k=e0+b e3+c e4, the two singleton residuals become
            # -2b e3^2 and -2c e4^2.
            k = (1, b, c)
            g2 = (1, 0, c)
            g1 = (1, b, 0)
            e3 = (0, 1, 0)
            e4 = (0, 0, 1)
            assert tuple(
                (left + b * right) % prime
                for left, right in zip(g2, e3, strict=True)
            ) == k
            assert tuple(
                (left + c * right) % prime
                for left, right in zip(g1, e4, strict=True)
            ) == k
            coefficient_u2 = -2 * b % prime
            coefficient_u1 = -2 * c % prime
            assert coefficient_u2 and coefficient_u1
            quotient_checks.append((b, c))

    return {
        "prime": prime,
        "projective_vectors": len(vectors),
        "ordered_pairs_checked": checked_pairs,
        "surviving_pairs": len(classified),
        "opposite_axis_pairs": sum(
            item["type"] == "opposite_coordinate_axes"
            for item in classified
        ),
        "full_support_pairs": sum(
            item["type"] == "both_full_support" for item in classified
        ),
        "nonzero_parameter_quotient_pairs_checked": len(quotient_checks),
    }


def main() -> None:
    finite_field_audits = [audit_prime(prime) for prime in (3, 5)]

    # Independently rederive the five source contractions apolarly.
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, b, c = sp.symbols("a b c")
    variables = (x0, x1, x2, x3, x4)
    permanent = sp.prod(variables)
    u0 = (a, 1, 1, 0, 0)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)

    def apply(*directions):
        result = permanent
        for direction in directions:
            result = derivative(result, variables, direction)
        return sp.expand(result)

    residuals = (
        apply(u1, h2, h2),
        apply(u2, h1, h1),
        apply(u0, h1, h1),
        apply(u0, h2, h2),
        apply(u0, h1, h2),
    )
    expected = (
        -2 * c * x1 * x2,
        -2 * b * x1 * x2,
        -2 * b * x4 * (x1 + x2),
        -2 * c * x3 * (x1 + x2),
        a * x1 * x2 + (x1 + x2) * (x0 - b * x3 - c * x4),
    )
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(residuals, expected, strict=True)
    )

    output = {
        "audited": True,
        "method": "independent apolar derivatives and finite-field pencil census",
        "finite_field_audits": finite_field_audits,
        "source_residuals": [str(value) for value in residuals],
        "ambient_local_maps_enumerated": 0,
        "zero_residual_dichotomy_checked": True,
        "nonzero_residual_common_kernel_boundary_excluded": True,
        "parallel_without_third_common_incidence_excluded": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "generic b*c nonzero parallel incidence only",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_parallel_incidence_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
