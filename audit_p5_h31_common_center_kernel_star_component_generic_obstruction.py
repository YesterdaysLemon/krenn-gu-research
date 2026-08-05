#!/usr/bin/env python3
"""Independent rational audit of component-23 generic H31 obstruction."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def add(left, right, coefficient=1):
    return tuple(left[i] + coefficient * right[i] for i in range(4))


def component_rows(r, t):
    k = sp.Rational(1 - r * t, t - r)
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    alpha = (
        A,
        add(A, D, k),
        add(add(add(A, C, -1), B), D, r),
        add(add(add(tuple(-entry for entry in A), C, -1), B), D, t),
    )
    beta = (B, add(B, C), C, C)
    return alpha, beta


def projected_rows(q, extension, alpha, beta):
    common = tuple(index for index in range(4) if index != q)
    alpha_p = tuple(
        tuple(alpha[i][coordinate] for coordinate in common) + (extension[i],)
        for i in range(4)
    )
    beta_p = tuple(
        tuple(beta[i][coordinate] for coordinate in common) + (extension[4 + i],)
        for i in range(4)
    )
    return alpha_p, beta_p


def coefficient_tensor(alpha, beta):
    return {
        bits: permanent(tuple(beta[i] if bits[i] else alpha[i] for i in range(4)))
        for bits in BITS4
    }


def one_marked(mode, alpha, beta):
    rows = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(
                permanent(
                    tuple(basis if other == mode else selected[other] for other in range(4))
                )
            )
        rows.append(row)
    return sp.Matrix(rows)


def check_branch(r, t, q, h1, e0, e1, expected_d0, expected_d1, factor, pure):
    p, w = sp.symbols("p w")
    alpha, canonical = component_rows(r, t)
    beta = tuple(
        add(canonical[i], alpha[i], h1 if i == 1 else 0) for i in range(4)
    )
    z = sp.Matrix(e0) * p + sp.Matrix(e1) * w
    alpha_p, beta_p = projected_rows(q, z, alpha, beta)
    tensor = coefficient_tensor(alpha_p, beta_p)
    assert all(value == 0 for bits, value in tensor.items() if bits not in (BITS4[0], BITS4[-1]))
    d0 = sp.factor(tensor[BITS4[0]])
    d1 = sp.factor(tensor[BITS4[-1]])
    assert sp.factor(d0 - expected_d0) == 0
    assert sp.factor(d1 - expected_d1) == 0
    marked = one_marked(0, alpha_p, beta_p)
    determinant = sp.factor(marked.extract((0, 3, 4, 7), range(4)).det())
    assert sp.factor(determinant - factor * d0 * d1**2) == 0
    pure_map = one_marked(0, alpha, beta)
    assert pure_map[1, q] == pure
    return {
        "point": [r, t],
        "distinguished": q,
        "marking_h1": str(h1),
        "diagonals": [str(d0), str(d1)],
        "minor_factor": str(factor),
        "pure_transverse": str(pure),
    }


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in ("generic marked-`H31` fibre", "bidirectional", "UNRESOLVED"):
        assert phrase in theorem
    assert '"generic_H31_fibre_empty": True' in primary
    cases = []
    for r, t, data in (
        (
            2,
            3,
            (
                (2, sp.Rational(-1, 3), (0, -5, sp.Rational(1, 3), sp.Rational(4, 3), 1, 0, 0, 0), 2 * (8 * sp.Symbol("p") - 3 * sp.Symbol("w")), sp.Rational(2, 3) * (2 * sp.Symbol("p") - 3 * sp.Symbol("w")), sp.Rational(20, 3), 10),
                (3, sp.Rational(-1, 7), (0, 5, sp.Rational(-9, 7), sp.Rational(-16, 7), 1, 0, 0, 0), 2 * (-2 * sp.Symbol("p") + 7 * sp.Symbol("w")), -2 * (sp.Rational(12, 7) * sp.Symbol("p") + sp.Symbol("w")), sp.Rational(120, 7), -10),
            ),
        ),
        (
            2,
            4,
            (
                (2, sp.Rational(-1, 2), (0, sp.Rational(-7, 2), sp.Rational(1, 4), sp.Rational(9, 4), 1, 0, 0, 0), 2 * (11 * sp.Symbol("p") - 4 * sp.Symbol("w")), 2 * (sp.Rational(3, 4) * sp.Symbol("p") - sp.Symbol("w")), sp.Rational(21, 4), 7),
                (3, sp.Rational(-1, 4), (0, sp.Rational(7, 2), sp.Rational(-9, 8), sp.Rational(-25, 8), 1, 0, 0, 0), 2 * (-sp.Symbol("p") + 8 * sp.Symbol("w")), -2 * (sp.Rational(15, 8) * sp.Symbol("p") + sp.Symbol("w")), sp.Rational(105, 8), -7),
            ),
        ),
    ):
        for q, h1, e0, d0, d1, factor, pure in data:
            cases.append(
                check_branch(r, t, q, h1, e0, (0, 0, 1, 1, 0, 1, 0, 0), d0, d1, factor, pure)
            )
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import audit",
                "field": "Q",
                "cases": cases,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
