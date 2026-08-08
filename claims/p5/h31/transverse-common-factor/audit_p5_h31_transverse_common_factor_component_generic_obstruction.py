#!/usr/bin/env python3
"""Independent exact audit of the twelfth component's generic H31 theorem."""

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
    r: int, k: int, shifts: tuple[sp.Symbol, ...]
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    m = add(b, c)
    m_r = add(b, scale(1 + r, c))
    d = (0, (r + 2) * (k + 1), 1, k)
    n = (-(k - 1) * (r + 2), 0, -1, k)
    alpha = (n, a, a, d)
    canonical = (c, m, m_r, c)
    beta = tuple(
        add(canonical[mode], scale(shifts[mode], alpha[mode]))
        for mode in range(4)
    )
    return alpha, beta


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
        sp.Matrix([[sp.diff(coefficients[word], variable) for variable in variables]])
        for word in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, *diagonals


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def module_check(
    mixed: sp.Matrix, alpha: sp.Matrix, beta: sp.Matrix, expected_size: int
) -> tuple[bool, bool, int]:
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(singular(alpha[0, column]) for column in range(8)) + "]"
    beta_vector = "[" + ",".join(singular(beta[0, column]) for column in range(8)) + "]"
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
    assert alpha_zero == "1" and beta_nonzero == "1" and int(size) == expected_size
    return True, True, int(size)


def main() -> None:
    shifts = sp.symbols("h0:4")
    points = ((1, 2), (2, 3))
    expected_sizes = (7, 7, 8, 8)
    point_results = []
    for point in points:
        alpha, beta = specialized_rows(*point, shifts)
        pure = {
            word: sp.factor(
                subset_permanent(
                    tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
                )
            )
            for word in WORDS
        }
        assert pure[(1, 1, 1, 1)] == -4
        assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))
        modules = []
        for distinguished, expected_size in enumerate(expected_sizes):
            mixed, diagonal_alpha, diagonal_beta = extension_rows(distinguished, alpha, beta)
            modules.append(module_check(mixed, diagonal_alpha, diagonal_beta, expected_size))
        point_results.append(
            {
                "point": list(point),
                "pure_coefficient": str(pure[(1, 1, 1, 1)]),
                "module_results": [
                    {
                        "all_alpha_remainder_zero": result[0],
                        "all_beta_remainder_nonzero": result[1],
                        "basis_size": result[2],
                    }
                    for result in modules
                ],
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
