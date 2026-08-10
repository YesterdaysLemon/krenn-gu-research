#!/usr/bin/env python3
"""No-import audit of component 22's h1-nonzero second-cofactor cover."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
s = 2 * A + R
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
SECOND_ROWS = (1, 2, 3, 5, 6, 7, 9, 12)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def rows():
    u = (1 - D) / 2
    v = (1 + D) / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    alpha = (
        (0, D * s, -u, v),
        m,
        add(m, c, R),
        c,
    )
    canonical = (
        (-A * v, A * (u + 1) + R, 1, 0),
        a,
        a,
        (-s / 2, -s / 2, u, v),
    )
    marking = (h0, h1, h2, h3)
    beta = tuple(add(canonical[i], alpha[i], marking[i]) for i in range(4))
    return alpha, beta


def permanent3(selected):
    return sp.expand(
        sum(
            sp.prod(selected[i][permutation[i]] for i in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def mixed_matrix():
    alpha, beta = rows()

    def project(row, extension):
        return (row[0], row[1], rho * row[2] + row[3], extension)

    alpha_p = tuple(project(alpha[i], x[i]) for i in range(4))
    beta_p = tuple(project(beta[i], x[i + 4]) for i in range(4))
    equations = []
    for word in WORDS[1:-1]:
        selected = tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
        equations.append(
            sp.expand(
                sum(
                    selected[i][3]
                    * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                    for i in range(4)
                )
            )
        )
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in equations]
    )


def associate(matrix, clearing_factor, expected):
    cleared = matrix.applyfunc(lambda entry: sp.expand(clearing_factor * entry))
    assert all(sp.denom(entry) == 1 for entry in cleared)
    determinant = DomainMatrix.from_Matrix(cleared).det().as_expr()
    quotient = sp.cancel(determinant / expected)
    assert quotient != 0 and quotient.free_symbols <= {A, R, D}
    assert sp.factor(determinant - quotient * expected) == 0
    return sp.factor(quotient)


def main():
    matrix = mixed_matrix()
    f2 = s * h2 + 1
    f6 = (D - 1) * rho + D + 1
    f7 = (A * D + A + R) * rho + A * D - A - R
    f8 = (A * D + A + R * D) * rho + A * D - A + R * D
    cap_u = 2 * h0 * f6 + (3 - D) * rho - (D + 1)
    cap_v = (
        (
            2 * A**2 * D**2
            + 2 * A**2 * D
            + 5 * A * R * D**2
            - 2 * A * R * D
            - A * R
            + D**2 * R**2
            - R**2
        )
        * h2
        * rho
        + (
            -2 * A**2 * D**2
            + 2 * A**2 * D
            - 5 * A * R * D**2
            - 2 * A * R * D
            + A * R
            - D**2 * R**2
            + R**2
        )
        * h2
        + (A * D + A + D**2 * R - D * R + R) * rho
        + A * D
        - A
        - D**2 * R
        - D * R
        - R
    )
    second_expected = h2 * f2 * rho * (rho + 1) ** 2 * f7 * f8 * cap_u * cap_v
    second = associate(
        matrix.extract(SECOND_ROWS, range(8)).subs(h1, -1 / (2 * A), simultaneous=True),
        16 * A,
        second_expected,
    )
    assert second == -(2**33) * A**8 * D * s**3 * (D + 1)
    print(
        json.dumps(
            {
                "status": "audit_pass",
                "field": "Q(A,R,D)",
                "repository_imports_used": False,
                "context_first_minor_replayed_here": False,
                "second_minor_quotient": str(second),
                "rank_drop_cover_verified": True,
                "displayed_residual_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
