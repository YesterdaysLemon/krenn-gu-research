#!/usr/bin/env python3
"""Independent exact audit of the thirteenth component's H31 theorem."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def subset_permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    table: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        nxt: dict[int, sp.Expr] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = sp.expand(nxt.get(target, 0) + coefficient * entry)
        table = nxt
    return sp.expand(table[15])


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(coefficient * entry) for entry in row)


def specialized_rows(
    point: tuple[sp.Rational, sp.Rational, sp.Rational, sp.Rational],
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha_parameter, beta_parameter, r, gamma = point
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    m = add(scale(alpha_parameter, a), scale(beta_parameter, c), b)
    m_r = add(m, scale(r, c))
    d = add(scale(gamma, a), b)
    x0 = add(
        b,
        scale(-(alpha_parameter + gamma), a),
        scale(-(2 * beta_parameter + r), c),
    )
    alpha_rows = (b_bar, m, m_r, c)
    canonical_beta = (x0, a, a, d)
    beta_rows = tuple(
        add(canonical_beta[mode], scale(shifts[mode], alpha_rows[mode]))
        for mode in range(4)
    )
    return alpha_rows, beta_rows


def extension_rows(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    variables = sp.symbols("x0:4") + sp.symbols("y0:4")
    common = tuple(index for index in range(4) if index != distinguished)
    alpha_extended = tuple(
        tuple(alpha[mode][index] for index in common) + (variables[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][index] for index in common) + (variables[4 + mode],)
        for mode in range(4)
    )
    coefficients = {
        word: subset_permanent(
            tuple(
                beta_extended[mode] if word[mode] else alpha_extended[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in variables]
            for word in WORDS
            if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
        ]
    )
    diagonals = tuple(
        sp.Matrix(
            [[sp.diff(coefficients[word], variable) for variable in variables]]
        )
        for word in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, *diagonals


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def module_check(
    mixed: sp.Matrix, diagonal_alpha: sp.Matrix, diagonal_beta: sp.Matrix
) -> dict[str, int | bool]:
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(singular(diagonal_alpha[0, column]) for column in range(8)) + "]"
    beta_vector = "[" + ",".join(singular(diagonal_beta[0, column]) for column in range(8)) + "]"
    program = "\n".join(
        (
            "ring R=0,(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector a=" + alpha_vector + ";",
            "vector b=" + beta_vector + ";",
            "vector ra=reduce(a,M);",
            "vector rb=reduce(b,M);",
            '"AUDIT:"+string(ra==0)+":"+string(rb!=0)+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        SINGULAR,
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    result = [line for line in completed.stdout.splitlines() if line.startswith("AUDIT:")]
    assert len(result) == 1, completed.stdout
    _, alpha_zero, beta_nonzero, size = result[0].split(":")
    assert alpha_zero == "1" and beta_nonzero == "1" and int(size) == 10
    return {
        "all_alpha_remainder_zero": True,
        "all_beta_remainder_nonzero": True,
        "basis_size": 10,
    }


def main() -> None:
    shifts = sp.symbols("h0:4")
    points = (
        (sp.Rational(-4, 3), sp.Rational(1), sp.Rational(-2, 3), sp.Rational(1)),
        (sp.Rational(2), sp.Rational(1), sp.Rational(-4), sp.Rational(1)),
    )
    point_results = []
    for point in points:
        alpha_parameter, beta_parameter, r, gamma = point
        assert (
            alpha_parameter**2
            + alpha_parameter * gamma
            + gamma**2
            - 3 * beta_parameter**2
            - 3 * beta_parameter * r
            - r**2
        ) == 0
        alpha_rows, beta_rows = specialized_rows(point, shifts)
        pure = {
            word: sp.factor(
                subset_permanent(
                    tuple(
                        beta_rows[mode] if word[mode] else alpha_rows[mode]
                        for mode in range(4)
                    )
                )
            )
            for word in WORDS
        }
        assert pure[(1, 1, 1, 1)] == 4
        assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))
        modules = []
        for distinguished in range(4):
            mixed, diagonal_alpha, diagonal_beta = extension_rows(
                distinguished, alpha_rows, beta_rows
            )
            modules.append(module_check(mixed, diagonal_alpha, diagonal_beta))
        point_results.append(
            {
                "point": [str(value) for value in point],
                "module_results": modules,
            }
        )

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP extension constructor",
                "all_markings": True,
                "points": point_results,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
