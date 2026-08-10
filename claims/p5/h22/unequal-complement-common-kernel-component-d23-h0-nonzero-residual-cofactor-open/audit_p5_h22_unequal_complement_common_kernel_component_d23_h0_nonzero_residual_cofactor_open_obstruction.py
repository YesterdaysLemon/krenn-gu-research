#!/usr/bin/env python3
"""No-import audit of component 22's h0-nonzero D23 cofactor open."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / (
    "verify_p5_h22_unequal_complement_common_kernel_component_"
    "d23_h0_nonzero_residual_cofactor_open_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))

A, R, D = sp.symbols("A R D")
h0, h2, rho = sp.symbols("h0 h2 rho")
x = sp.symbols("x0:8")
s = 2 * A + R
ROWS = (0, 1, 2, 3, 4, 5, 7, 8)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def rows():
    u = (1 - D) / 2
    v = (1 + D) / 2
    g = -s / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (g, g, u, v)
    y0 = (0, D * s, -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    alpha = (y0, m, mr, c)
    canonical = (x0, a, a, d)
    marking = (h0, 0, h2, s / 2)
    beta = tuple(add(canonical[i], alpha[i], marking[i]) for i in range(4))
    assert all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4))
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
    beta_p = tuple(project(beta[i], x[4 + i]) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    return sp.Matrix(
        [[sp.diff(coefficients[word], variable) for variable in x] for word in MIXED]
    )


def residual_polynomials():
    f2 = s * h2 + 1
    f6 = (D - 1) * rho + D + 1
    f7 = (A * D + A + R) * rho + A * D - A - R
    f8 = (A * D + A + R * D) * rho + A * D - A + R * D
    L = (A * D + A + R * D) * h0 * rho + (A * D - A + R * D) * h0 + R * rho + s
    T = (
        (A**2 * D - 3 * A**2 - 3 * A * R - R**2) * rho
        + A**2 * D
        + 3 * A**2
        + 3 * A * R
        + R**2
    )
    G = (
        (
            4 * A**2 * D**2
            - 4 * A**2 * D
            + 4 * A * R * D**2
            - 4 * A * R * D
            + R**2 * D**2
            - R**2 * D
        )
        * h0
        * rho
        + (
            2 * A**3 * D**2
            + 2 * A**3 * D
            + 4 * A**2 * R * D**2
            + 2 * A**2 * R
            + A * R**2 * D**2
            + A * R**2
        )
        * h2
        * rho
        + (
            -4 * A**2 * D**2
            + 4 * A**2 * D
            - 4 * A * R * D**2
            + 4 * A * R * D
            - R**2 * D**2
            + R**2 * D
        )
        * h0
        + (
            -2 * A**3 * D**2
            + 2 * A**3 * D
            - 4 * A**2 * R * D**2
            - 2 * A**2 * R
            - A * R**2 * D**2
            - A * R**2
        )
        * h2
        + (-(A**2) * D**2 + 5 * A**2 * D - 2 * A**2 + 4 * A * R * D - A * R + R**2 * D)
        * rho
        + A**2 * D**2
        - 3 * A**2 * D
        + 2 * A**2
        - 4 * A * R * D
        + A * R
        - R**2 * D
    )
    G2 = (
        (-8 * A**2 * D + A * R * D**2 - 7 * A * R * D - R**2 * D) * h0 * h2 * rho
        + (-8 * A**2 * D - A * R * D**2 - 7 * A * R * D - R**2 * D) * h0 * h2
        + (-A * D**2 - A * D - R * D) * h0 * rho
        + (2 * A**2 * D - 6 * A**2 - A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        * rho
        + (A * D**2 - A * D - R * D) * h0
        + (2 * A**2 * D - 6 * A**2 + A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        + (A * D**2 - A * D - 2 * A - R) * rho
        - A * D**2
        - A * D
        - 2 * A
        - R
    )
    return f2, f6, f7, f8, L, T, G, G2


def cofactor_audit():
    f2, f6, f7, f8, L, T, G, G2 = residual_polynomials()
    matrix = mixed_matrix()
    determinant = sp.factor(matrix.extract(ROWS, range(8)).det(method="domain-ge"))
    known = sp.factor(
        -8 * A * D * s**4 * (D - 1) * (D + 1) * rho * (rho - 1) * (rho + 1) * f6 * f7
    )
    quotient = sp.cancel(determinant / known)
    numerator, denominator = sp.fraction(quotient)
    assert denominator == 1
    polynomial = sp.factor(numerator)
    assert sp.factor(determinant - known * polynomial) == 0
    assert polynomial.free_symbols <= {A, R, D, h0, h2, rho}

    radical = sp.sqrt(29665)
    point = {
        A: 2,
        R: 1,
        D: 3,
        rho: 2,
        h0: (-35 + radical) / 540,
        h2: (-199 - radical) / 1656,
    }
    assert sp.simplify(G.subs(point)) == 0
    assert sp.simplify(G2.subs(point)) == 0
    factors = (
        h0,
        h2,
        f2,
        rho,
        rho - 1,
        rho + 1,
        f6,
        f7,
        f8,
        L,
        T,
        R * h2 - 1,
    )
    values = tuple(sp.factor(value.subs(point)) for value in factors)
    assert all(value != 0 for value in values)
    expected_p = (-169645 + 5603 * radical) / 276
    assert sp.simplify(polynomial.subs(point) - expected_p) == 0
    assert 169645**2 - 5603**2 * 29665 != 0
    expected_minor = -sp.Rational(20160000, 23) * (-169645 + 5603 * radical)
    assert sp.simplify(determinant.subs(point) - expected_minor) == 0
    return {
        "rows": ROWS,
        "P_total_degree": sp.Poly(polynomial, h0, h2, rho).total_degree(),
        "P_term_count": len(sp.Poly(polynomial, h0, h2, rho).terms()),
        "point_factor_values": tuple(map(str, values)),
        "P_value": str(sp.factor(expected_p)),
        "minor_value": str(sp.factor(expected_minor)),
    }


def main():
    certificate = cofactor_audit()
    replay = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert replay.returncode == 0, (replay.stdout, replay.stderr)
    assert json.loads(replay.stdout)["status"] == "pass"
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "repository_imports_used": False,
                "certificate": certificate,
                "primary_replay": "pass",
                "P_nonzero_residual_binary_empty": True,
                "remaining_residual": "h0!=0, P=0",
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
