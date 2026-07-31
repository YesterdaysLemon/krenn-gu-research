#!/usr/bin/env python3
"""Independent exact audit of the Eisenstein component's H22 theorem."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
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


def weighted_row(
    row: tuple[sp.Expr, ...], extension: sp.Expr, rho: sp.Expr | None
) -> tuple[sp.Expr, ...]:
    merged = row[0] if rho is None else sp.expand(rho * row[0] + row[1])
    return (merged, row[2], row[3], extension)


def coefficient_model(
    alpha_rows: tuple[tuple[sp.Expr, ...], ...],
    beta_rows: tuple[tuple[sp.Expr, ...], ...],
    rho: sp.Expr | None,
) -> tuple[list[sp.Expr], sp.Expr, sp.Expr]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    alpha_weighted = tuple(
        weighted_row(alpha_rows[mode], extensions[mode], rho)
        for mode in range(4)
    )
    beta_weighted = tuple(
        weighted_row(beta_rows[mode], extensions[4 + mode], rho)
        for mode in range(4)
    )
    coefficients = {
        word: subset_permanent(
            tuple(
                beta_weighted[mode] if word[mode] else alpha_weighted[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    return (
        [coefficients[word] for word in MIXED_WORDS],
        coefficients[WORDS[0]],
        coefficients[WORDS[-1]],
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def ideal_check(
    label: str,
    equations: list[sp.Expr],
    diagonal_alpha: sp.Expr,
    diagonal_beta: sp.Expr,
    variables: str,
) -> dict[str, int | bool]:
    program = "\n".join(
        (
            f"ring R=0,({variables}),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(singular(equation) for equation in equations) + ";",
            "I=std(I);",
            "poly p=" + singular(diagonal_alpha * diagonal_beta) + ";",
            "poly rp=reduce(p,I);",
            '"AUDIT_PRODUCT:"+string(rp==0)+":"+string(size(I));',
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
        timeout=180,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((label, completed.returncode, completed.stdout, completed.stderr))
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("AUDIT_PRODUCT:")
    ]
    assert len(results) == 1, completed.stdout
    _, product_zero, basis_size = results[0].split(":")
    assert product_zero == "1", (label, results[0])
    return {
        "diagonal_product_remainder_zero": True,
        "groebner_basis_size": int(basis_size),
    }


def main() -> None:
    shifts = sp.symbols("h0:4")
    rho = sp.symbols("rho")
    points = (
        (sp.Rational(-4, 3), sp.Rational(1), sp.Rational(-2, 3), sp.Rational(1)),
        (sp.Rational(2), sp.Rational(1), sp.Rational(-4), sp.Rational(1)),
    )
    results = []
    for point in points:
        alpha_rows, beta_rows = specialized_rows(point, shifts)
        finite = coefficient_model(alpha_rows, beta_rows, rho)
        infinity = coefficient_model(alpha_rows, beta_rows, None)
        finite_result = ideal_check(
            "finite",
            *finite,
            variables="rho,h0,h1,h2,h3,x0,x1,x2,x3,y0,y1,y2,y3",
        )
        infinity_result = ideal_check(
            "infinity",
            *infinity,
            variables="h0,h1,h2,h3,x0,x1,x2,x3,y0,y1,y2,y3",
        )
        results.append(
            {
                "point": [str(value) for value in point],
                "finite_chart": finite_result,
                "infinite_chart": infinity_result,
            }
        )

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP diagonal-product ideals",
                "points": results,
                "all_markings": True,
                "all_projective_slopes": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
