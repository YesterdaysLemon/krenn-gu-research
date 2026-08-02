#!/usr/bin/env python3
"""Independent exact-Q audit of component 22's finite-D23 rho=-1 slice."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMS4 = tuple(itertools.permutations(range(4)))
x = sp.symbols("x0:8")
h0, h1, h2, h3, tau, w = sp.symbols("h0 h1 h2 h3 tau w")
ROWS = (
    (0, 1, 2, 3, 4, 5, 8),
    (0, 1, 3, 4, 5, 6, 8),
    (0, 1, 3, 4, 5, 7, 8),
    (0, 1, 3, 4, 5, 8, 10),
    (0, 1, 3, 4, 5, 8, 12),
)
COLUMNS = (0, 1, 2, 3, 4, 5, 6)


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
    alpha_p = tuple(
        (row[0], row[1], -row[2] + row[3], x[i]) for i, row in enumerate(alpha)
    )
    beta_p = tuple(
        (row[0], row[1], -row[2] + row[3], x[4 + i]) for i, row in enumerate(beta)
    )
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
    return str(sp.factor(sp.fraction(sp.together(expression))[0])).replace("**", "^")


def run_unit_case(label, substitutions):
    alpha, beta = projected_rows((h0, h1, h2, h3))
    values = coefficients(alpha, beta)
    matrices = (
        one_marked_map(0, alpha, beta).extract((0, 1, 3, 7), range(4)),
        one_marked_map(1, alpha, beta).extract((0, 1, 2, 7), range(4)),
        one_marked_map(1, alpha, beta).extract((0, 1, 4, 7), range(4)),
    )
    equations = [values[bits].subs(substitutions) for bits in BITS4[1:-1]]
    equations.extend(
        (
            values[BITS4[0]].subs(substitutions) - 1,
            w * values[BITS4[-1]].subs(substitutions) - 1,
        )
    )
    declarations = []
    for index, matrix in enumerate(matrices):
        specialized = matrix.subs(substitutions)
        entries = [
            sg(specialized[row, column]) for row in range(4) for column in range(4)
        ]
        declarations.append(f"matrix N{index}[4][4]=" + ",".join(entries) + ";")
    program = "\n".join(
        (
            "ring Q=0,(" + ",".join(map(str, (*x, w))) + "),dp;",
            "option(redSB);",
            *declarations,
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
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:1"], (label, completed.stdout)
    return label


def main():
    alpha, beta = projected_rows((h0, h1, h2, h3))
    values = coefficients(alpha, beta)
    mixed = sp.Matrix(
        [[sp.diff(values[bits], variable) for variable in x] for bits in BITS4[1:-1]]
    )
    kernel = sp.Matrix((-sp.Rational(1, 3), 0, 0, 0, (1 - h0) / 3, 0, 0, 1))
    assert all(sp.expand(entry) == 0 for entry in mixed * kernel)
    extension = {x[index]: tau * kernel[index] for index in range(8)}
    assert sp.expand(values[BITS4[0]].subs(extension)) == 0
    assert sp.expand(values[BITS4[-1]].subs(extension)) == 0

    determinants = []
    seven_columns = mixed.extract(range(14), COLUMNS)
    for row_indices in ROWS:
        determinant = seven_columns.extract(row_indices, range(7)).det(
            method="domain-ge"
        )
        determinants.append(
            sp.Poly(determinant, h0, h1, h2, h3).primitive()[1].as_expr()
        )
    expected = (
        h2 - 1,
        64 * h1 - 6 * h3 - 49,
        h0 - 1,
        (2 * h3 - 5) * (6 * h3 + 65),
    )
    determinant_basis = sp.groebner(determinants, h3, h2, h1, h0, order="grevlex")
    expected_basis = sp.groebner(expected, h3, h2, h1, h0, order="grevlex")
    assert all(determinant_basis.reduce(value)[1] == 0 for value in expected)
    assert all(expected_basis.reduce(value)[1] == 0 for value in determinants)

    q3 = {h0: 1, h1: 1, h2: 1, h3: sp.Rational(5, 2)}
    q4 = {h0: 1, h1: -sp.Rational(1, 4), h2: 1, h3: -sp.Rational(65, 6)}
    for point in (q3, q4):
        assert all(sp.cancel(value.subs(point)) == 0 for value in expected)
    closed = (
        run_unit_case("rho_minus_one_Q3_at_A2_R1_D3", q3),
        run_unit_case("rho_minus_one_Q4_at_A2_R1_D3", q4),
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"A": 2, "R": 1, "D": 3},
                "independent_no_repository_imports": True,
                "universal_kernel_verified": True,
                "A_on_kernel": "0",
                "B_on_kernel": "0",
                "rank_drop_ideal": [str(value) for value in expected],
                "rank_drop_points": {
                    "Q3": {str(key): str(value) for key, value in q3.items()},
                    "Q4": {str(key): str(value) for key, value in q4.items()},
                },
                "closed_exact_points": closed,
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
