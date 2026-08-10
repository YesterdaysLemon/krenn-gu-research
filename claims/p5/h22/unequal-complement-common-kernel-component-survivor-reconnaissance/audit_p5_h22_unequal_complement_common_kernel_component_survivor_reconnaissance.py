#!/usr/bin/env python3
"""Independent exact audit of component-22 H22 survivor reconnaissance."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_SURVIVOR_RECONNAISSANCE.md"
PRIMARY = ROOT / "verify_p5_h22_unequal_complement_common_kernel_component_survivor_reconnaissance.py"
BITS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left, right):
    return sp.Matrix(
        [
            left[i] * right[j] + left[j] * right[i]
            for i, j in itertools.combinations(range(len(left)), 2)
        ]
    )


def pair_profile(alpha, beta):
    return tuple(
        sp.Matrix.hstack(
            product(alpha[i], alpha[j]),
            product(alpha[i], beta[j]),
            product(beta[i], alpha[j]),
            product(beta[i], beta[j]),
        ).rank()
        for i, j in itertools.combinations(range(4), 2)
    )


def component_rows():
    A = R = 1
    D = 2
    u = sp.Rational(1 - D, 2)
    v = sp.Rational(1 + D, 2)
    G = sp.Rational(-(2 * A + R), 2)
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2, 0, 1, 1)
    mr = tuple(m[i] + R * c[i] for i in range(4))
    d = (G, G, u, v)
    y0 = (0, D * (2 * A + R), -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    return (y0, m, mr, c), (x0, a, a, d)


def marked_rows(canonical, alpha, shifts):
    return tuple(
        tuple(canonical[i][j] + shifts[i] * alpha[i][j] for j in range(4))
        for i in range(4)
    )


def projected(rows, extensions, rho):
    return tuple(
        (
            rho * rows[i][0] + rows[i][1],
            rows[i][2],
            rows[i][3],
            extensions[i],
        )
        for i in range(4)
    )


def one_marked(mode, alpha, beta):
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def audit_point(rho, shifts, extension, diagonals, minors):
    alpha, canonical = component_rows()
    beta = marked_rows(canonical, alpha, shifts)
    alpha_p = projected(alpha, extension[:4], rho)
    beta_p = projected(beta, extension[4:], rho)
    coefficients = {
        bits: permanent(
            tuple(beta_p[i] if bits[i] else alpha_p[i] for i in range(4))
        )
        for bits in BITS
    }
    assert all(
        value == 0 for bits, value in coefficients.items() if bits not in (BITS[0], BITS[-1])
    )
    assert (coefficients[BITS[0]], coefficients[BITS[-1]]) == diagonals
    alpha5 = tuple(tuple(alpha[i]) + (extension[i],) for i in range(4))
    beta5 = tuple(tuple(beta[i]) + (extension[4 + i],) for i in range(4))
    assert pair_profile(alpha5, beta5) == (4, 4, 4, 4, 4, 4)
    assert pair_profile(alpha_p, beta_p) == (4, 4, 4, 3, 3, 3)
    observed = tuple(
        one_marked(mode, alpha_p, beta_p).extract((0, 1, 3, 7), range(4)).det()
        for mode in range(4)
    )
    assert observed == minors
    return list(map(str, observed))


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in (
        "generic fibre still UNKNOWN",
        "neither is a counterexample",
        "No finite-field computation is used",
    ):
        assert phrase in theorem
    assert '"generic_weighted_H22_fibre_closed": False' in primary
    first = audit_point(
        -2,
        (1, 0, 0, -1),
        (
            sp.Rational(8, 5),
            sp.Rational(4, 5),
            sp.Rational(2, 25),
            sp.Rational(-18, 25),
            sp.Rational(3, 25),
            sp.Rational(6, 25),
            sp.Rational(6, 25),
            1,
        ),
        (sp.Rational(-192, 25), sp.Rational(-18, 25)),
        (
            sp.Rational(27648, 3125),
            sp.Rational(-31104, 3125),
            sp.Rational(-31104, 3125),
            sp.Rational(-27648, 15625),
        ),
    )
    second = audit_point(
        3,
        (0, 0, 0, 1),
        (-3, 5, 6, 1, sp.Rational(-15, 2), -2, -2, 1),
        (72, -24),
        (73728, 15552, 15552, 110592),
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import audit",
                "field": "Q",
                "row_0137_minors": [first, second],
                "binary_survivors_are_H22_lifts": False,
                "generic_weighted_H22_fibre_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
