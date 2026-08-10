#!/usr/bin/env python3
"""Independent exact-Q audit of the rho=0 component-22 D23 supplement.

No repository construction or verifier module is imported.  This rebuilds
the rows, projection, permanents, mixed matrix, and one-marked maps locally.
The fixed specialization is an audit only, not the generic proof.
"""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMS4 = tuple(itertools.permutations(range(4)))
x = sp.symbols("x0:8")
h0, h1, h2, h3, t, w, v = sp.symbols("h0 h1 h2 h3 t w v")


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows():
    A, R, D = sp.Integer(2), sp.Integer(1), sp.Integer(3)
    u, z = (1 - D) / 2, (1 + D) / 2
    G = -(2 * A + R) / 2
    a, c = (1, 1, 0, 0), (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (G, G, u, z)
    y0 = (0, D * (2 * A + R), -u, z)
    x0 = (-A * z, A * (u + 1) + R, 1, 0)
    return (y0, m, mr, c), (x0, a, a, d)


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMS4
        )
    )


def projected_rows(shifts):
    alpha, beta = component_rows()
    beta = tuple(add(beta[i], alpha[i], shifts[i]) for i in range(4))
    alpha_p = tuple((row[0], row[1], row[3], x[i]) for i, row in enumerate(alpha))
    beta_p = tuple((row[0], row[1], row[3], x[4 + i]) for i, row in enumerate(beta))
    return alpha_p, beta_p


def coefficients(alpha, beta):
    return {
        bits: permanent(tuple(beta[i] if bits[i] else alpha[i] for i in range(4)))
        for bits in BITS4
    }


def one_marked_map(mode, alpha, beta):
    rows = []
    for bits in BITS3:
        selected, cursor = [], 0
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


def sg(expression):
    return str(sp.fraction(sp.together(expression))[0]).replace("**", "^")


def matrix_declaration(name, matrix):
    return (
        f"matrix {name}[4][4]="
        + ",".join(sg(matrix[row, column]) for row in range(4) for column in range(4))
        + ";"
    )


def h2_zero_unit_case(alpha, beta, values):
    matrices = (
        one_marked_map(0, alpha, beta).extract((0, 1, 3, 7), range(4)),
        one_marked_map(1, alpha, beta).extract((0, 1, 2, 7), range(4)),
        one_marked_map(1, alpha, beta).extract((0, 1, 4, 7), range(4)),
    )
    equations = [values[bits] for bits in BITS4[1:-1]]
    equations.extend((values[BITS4[0]] - 1, w * values[BITS4[-1]] - 1, v * h1 - 1))
    program = "\n".join(
        (
            "ring Q=0,(" + ",".join(map(str, (*x, h0, h1, h3, w, v))) + "),dp;",
            "option(redSB);",
            *[matrix_declaration(f"N{i}", matrix) for i, matrix in enumerate(matrices)],
            "ideal I=" + ",".join(map(sg, equations)) + ",det(N0),det(N1),det(N2);",
            "I=slimgb(I); ideal J=std(I);",
            '"RESULT:"+string(size(J))+":"+string(reduce(1,J)==0);',
            "quit;",
        )
    )
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=90,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:1"], completed.stdout
    return "rho_zero_h2_zero_h1_nonzero_at_A2_R1_D3"


def main():
    alpha, beta = projected_rows((h0, h1, h2, h3))
    values = coefficients(alpha, beta)
    mixed = sp.Matrix(
        [[sp.diff(values[bits], variable) for variable in x] for bits in BITS4[1:-1]]
    )
    kernel = sp.Matrix((2, 2, 2, 0, 2 * h0 + 2, 2 * h1, 2 * h2, -2))
    assert all(sp.expand(entry) == 0 for entry in mixed * kernel)

    substitution = {x[index]: t * kernel[index] for index in range(8)}
    assert sp.expand(values[BITS4[0]].subs(substitution)) == 0
    assert sp.expand(values[BITS4[-1]].subs(substitution) - 8 * t) == 0

    cofactor = mixed.extract((0, 1, 3, 4, 5, 7, 9), (1, 2, 3, 4, 5, 6, 7)).det()
    assert sp.factor(cofactor) == 2184000 * h2 * (7 * h0 + 34 * h1 + 5)

    alpha0, beta0 = projected_rows((h0, h1, 0, h3))
    values0 = coefficients(alpha0, beta0)
    unit = h2_zero_unit_case(alpha0, beta0, values0)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"A": 2, "R": 1, "D": 3},
                "independent_no_repository_imports": True,
                "kernel_annihilation": True,
                "A_on_kernel": "0",
                "B_on_kernel": "8*t",
                "selected_cofactor": "2184000*h2*(7*h0+34*h1+5)",
                "exact_unit_case": unit,
                "audit_only_not_generic_proof": True,
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
