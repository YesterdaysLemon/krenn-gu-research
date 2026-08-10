#!/usr/bin/env python3
"""Independent finite-field audit of the adjacent P4 pencil reduction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md"


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


def rank_mod(rows, prime):
    matrix = [[value % prime for value in row] for row in rows]
    pivot = 0
    for column in range(len(matrix[0])):
        row = next(
            (
                index
                for index in range(pivot, len(matrix))
                if matrix[index][column]
            ),
            None,
        )
        if row is None:
            continue
        matrix[pivot], matrix[row] = matrix[row], matrix[pivot]
        inverse = pow(matrix[pivot][column], -1, prime)
        matrix[pivot] = [
            value * inverse % prime for value in matrix[pivot]
        ]
        for index in range(len(matrix)):
            if index == pivot:
                continue
            multiple = matrix[index][column]
            if multiple:
                matrix[index] = [
                    (left - multiple * right) % prime
                    for left, right in zip(
                        matrix[index],
                        matrix[pivot],
                        strict=True,
                    )
                ]
        pivot += 1
    return pivot


def audit_prime(prime):
    parameter_pairs = 0
    scalar_cases = {"one_nonzero": 0, "two_nonzero": 0}
    for b in range(1, prime):
        for c in range(1, prime):
            parameter_pairs += 1
            kernel = (1, b, c)
            w_plus = (1, b, -c % prime)
            w_minus = (1, -b % prime, c)
            assert rank_mod([kernel, w_plus, w_minus], prime) == 3

            # Use the quotient basis (w+,w-).  One scalar gives one
            # simple summand; two nonzero scalars give flattening rank 2.
            for p in range(prime):
                for q in range(prime):
                    if not p and not q:
                        continue
                    matrix = [[0, q], [p, 0]]
                    rank = rank_mod(matrix, prime)
                    if bool(p) ^ bool(q):
                        assert rank == 1
                        scalar_cases["one_nonzero"] += 1
                    else:
                        assert rank == 2
                        scalar_cases["two_nonzero"] += 1
    return {
        "prime": prime,
        "nonzero_parameter_pairs": parameter_pairs,
        "cross_scalar_cases": scalar_cases,
        "quotient_plane_always_rank_two": True,
    }


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    b, c = sp.symbols("b c")
    variables = (x0, x1, x2, x3, x4)
    permanent = sp.prod(variables)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)
    residuals = []
    for first, second in ((u1, h2), (u2, h1)):
        residual = derivative(permanent, variables, first)
        residuals.append(derivative(residual, variables, second))
    expected = (
        -x1 * x2 * (x0 + b * x3 - c * x4),
        -x1 * x2 * (x0 - b * x3 + c * x4),
    )
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(residuals, expected, strict=True)
    )

    output = {
        "audited": True,
        "method": "independent apolar derivatives and quotient-rank census",
        "source_residuals": [str(sp.factor(value)) for value in residuals],
        "finite_field_audits": [audit_prime(prime) for prime in (3, 5)],
        "ambient_local_maps_enumerated": 0,
        "one_scalar_boundary_retained": True,
        "marked_Delta2_boundary_retained": True,
        "adjacent_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "generic common-mode adjacent reduction",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_adjacent_p4_pencil_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
