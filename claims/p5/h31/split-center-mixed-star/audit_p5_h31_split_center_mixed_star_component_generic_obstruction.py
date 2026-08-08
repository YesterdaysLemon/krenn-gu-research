#!/usr/bin/env python3
"""Independent rational audit of the component-24 generic H31 proof."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS
        )
    )


def extension_coefficients(q, alpha, beta, extension):
    common = tuple(index for index in range(4) if index != q)
    alpha_p = tuple(tuple(row[index] for index in common) + (extension[mode],) for mode, row in enumerate(alpha))
    beta_p = tuple(tuple(row[index] for index in common) + (extension[4 + mode],) for mode, row in enumerate(beta))
    return {
        bits: permanent(tuple(beta_p[mode] if bits[mode] else alpha_p[mode] for mode in range(4)))
        for bits in BITS4
    }


def mixed_matrix(q, alpha, beta):
    variables = sp.symbols("x0:8")
    coefficients = extension_coefficients(q, alpha, beta, sp.Matrix(variables))
    mixed = sp.Matrix(
        [[sp.diff(coefficients[bits], variable) for variable in variables] for bits in BITS4 if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    )
    diagonals = tuple(
        sp.Matrix([[sp.diff(coefficients[bits], variable) for variable in variables]])
        for bits in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, *diagonals


def one_marked_map(mode, alpha, beta):
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
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent(tuple(basis if other == mode else selected[other] for other in range(4)))
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def marked_extension(q, extension, alpha, beta):
    common = tuple(index for index in range(4) if index != q)
    alpha_p = tuple(tuple(row[index] for index in common) + (extension[mode],) for mode, row in enumerate(alpha))
    beta_p = tuple(tuple(row[index] for index in common) + (extension[4 + mode],) for mode, row in enumerate(beta))
    return one_marked_map(0, alpha_p, beta_p)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(coefficient * entry for entry in row)


def component_rows(k, s, t):
    A, C, B, D = (1, 1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (0, 0, 1, -1)
    c = (t - k * s) / (1 - k * s * t)
    alpha = (A, add(A, scale(k, D)), add(A, scale(c, C), scale(k, B), scale(-k, D)), D)
    beta = (B, add(B, scale(s, C)), C, add(scale(t, A), C, scale(-k * t, B)))
    return alpha, beta


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    numerator = sp.fraction(sp.together(expression))[0]
    return str(sp.expand(numerator)).replace("**", "^")


def run(program):
    completed = subprocess.run(singular_command(), input=program, text=True, capture_output=True, timeout=120, check=False)
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers, completed.stdout
    return markers


def audit_point(k, s, t):
    alpha, beta = component_rows(k, s, t)
    extension = sp.symbols("x0:8")
    inverse = sp.Symbol("u")
    h = sp.symbols("h0:4")
    projected_sizes = []
    for q in (0, 1, 3):
        marked = tuple(add(beta[index], scale(h[index], alpha[index])) for index in range(4))
        mixed, d0, d1 = mixed_matrix(q, alpha, marked)
        vector = sp.Matrix(extension)
        equations = (*tuple(mixed * vector), (d0 * vector)[0] - 1, inverse * (d1 * vector)[0] - 1)
        variables = extension + (inverse,) + h
        expected = {
            0: (h[3] - k * t, h[2], k * (t + 1) * h[1] - 2 * k * s * t - t + 1, h[0]),
            1: (h[3] - k * t, h[2], k * (t - 1) * h[1] + 2 * k * s * t - t - 1, h[0]),
            3: (
                h[3] - k * t,
                k * (k * s * t - 1) * h[1] + 2 * t * (k**2 * s**2 - 1) * h[2] + k * s * t - 1,
                h[0],
                2 * t * (k**2 * s**2 - 1) * h[2] ** 2 + (k**2 * s**2 * t**2 - 1) * h[2],
            ),
        }[q]
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
                "ideal I=" + ",".join(map(sg, equations)) + "; I=slimgb(I);",
                "ideal J=std(eliminate(I," + "*".join(map(str, extension + (inverse,))) + "));",
                "ideal E=" + ",".join(map(sg, expected)) + "; E=std(E);",
                "ideal A=simplify(reduce(J,E),2); ideal B=simplify(reduce(E,J),2);",
                '"RESULT:"+string(size(J))+":"+string(size(A))+":"+string(size(B));',
                "quit;",
            )
        )
        expected_size = 4
        assert run(program) == [f"RESULT:{expected_size}:0:0"]
        projected_sizes.append(expected_size)

    h2b = -(k**2 * s**2 * t**2 - 1) / (2 * t * (k**2 * s**2 - 1))
    branches = (
        (0, (0, (2 * k * s * t + t - 1) / (k * (t + 1)), 0, k * t)),
        (1, (0, (t + 1 - 2 * k * s * t) / (k * (t - 1)), 0, k * t)),
        (3, (0, -1 / k, 0, k * t)),
        (3, (0, s * t, h2b, k * t)),
    )
    unit_count = 0
    for q, marking in branches:
        marked = tuple(add(beta[index], scale(marking[index], alpha[index])) for index in range(4))
        mixed, d0, d1 = mixed_matrix(q, alpha, marked)
        vector = sp.Matrix(extension)
        minor = marked_extension(q, vector, alpha, marked).extract((0, 1, 3, 7), range(4)).det(method="domain-ge")
        equations = (*tuple(mixed * vector), (d0 * vector)[0] - 1, inverse * (d1 * vector)[0] - 1, minor)
        variables = extension + (inverse,)
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
                "ideal I=" + ",".join(map(sg, equations)) + "; I=slimgb(I);",
                '"RESULT:"+string(size(std(I)))+":"+string(reduce(1,std(I))==0);',
                "quit;",
            )
        )
        markers = run(program)
        assert markers == ["RESULT:1:1"], (q, marking, markers)
        unit_count += 1
    return {"point": [str(k), str(s), str(t)], "projection_sizes": projected_sizes, "branch_unit_ideals": unit_count}


def main():
    points = [audit_point(*point) for point in ((sp.Rational(2), sp.Rational(3), sp.Rational(2)), (sp.Rational(3), sp.Rational(2), sp.Rational(4)))]
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import rational audit",
                "field": "Q",
                "points": points,
                "generic_characteristic_zero_proof_replaced": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
