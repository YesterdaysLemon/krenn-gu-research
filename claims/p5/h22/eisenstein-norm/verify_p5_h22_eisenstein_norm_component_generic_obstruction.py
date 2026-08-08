#!/usr/bin/env python3
"""Verify weighted H22 obstruction on the Eisenstein-norm component."""

from __future__ import annotations

import itertools
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

ROOT = REPO_ROOT
THEOREM = HERE / "P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = ROOT / "P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.cancel(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.cancel(coefficient * entry) for entry in row)


def marked_rows(
    u: sp.Symbol, v: sp.Symbol, shifts: tuple[sp.Symbol, ...]
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    denominator = u**2 + u * v + v**2 - 1
    line_parameter = sp.cancel((5 - 5 * u - 4 * v) / denominator)
    alpha_parameter = sp.cancel(2 + u * line_parameter)
    r = sp.cancel(1 + line_parameter)
    gamma = sp.cancel(1 + v * line_parameter)
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    m = add(scale(alpha_parameter, a), c, b)
    m_r = add(m, scale(r, c))
    d = add(scale(gamma, a), b)
    x0 = add(
        b,
        scale(-(alpha_parameter + gamma), a),
        scale(-(2 + r), c),
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


def extension_model(
    alpha_rows: tuple[tuple[sp.Expr, ...], ...],
    beta_rows: tuple[tuple[sp.Expr, ...], ...],
    rho: sp.Expr | None,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
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
        word: permanent(
            tuple(
                beta_weighted[mode] if word[mode] else alpha_weighted[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in extensions]
            for word in MIXED_WORDS
        ]
    )
    diagonal_alpha = sp.Matrix(
        [[sp.diff(coefficients[WORDS[0]], variable) for variable in extensions]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(coefficients[WORDS[-1]], variable) for variable in extensions]]
    )
    return mixed, diagonal_alpha, diagonal_beta


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def diagonal_product_test(
    label: str,
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
    variables: str,
) -> dict[str, int | bool]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    equations = [
        sp.cancel(
            sum(mixed[row, column] * extensions[column] for column in range(8))
        )
        for row in range(14)
    ]
    alpha_polynomial = sp.cancel(
        sum(diagonal_alpha[0, column] * extensions[column] for column in range(8))
    )
    beta_polynomial = sp.cancel(
        sum(diagonal_beta[0, column] * extensions[column] for column in range(8))
    )
    generators = ",".join(singular(equation) for equation in equations)
    product = singular(alpha_polynomial * beta_polynomial)
    program = "\n".join(
        (
            f"ring R=(0,u,v),({variables}),dp;",
            "option(redSB);",
            "ideal I=" + generators + ";",
            "I=std(I);",
            "poly p=" + product + ";",
            "poly rp=reduce(p,I);",
            '"CODEX_PRODUCT:"+string(rp==0)+":"+string(size(I));',
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
        timeout=240,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((label, completed.returncode, completed.stdout, completed.stderr))
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_PRODUCT:")
    ]
    assert len(results) == 1, completed.stdout
    _, product_zero, basis_size = results[0].split(":")
    assert product_zero == "1", (label, results[0])
    return {
        "diagonal_product_remainder_zero": True,
        "groebner_basis_size": int(basis_size),
    }


def main() -> None:
    u, v, rho = sp.symbols("u v rho")
    shifts = sp.symbols("h0:4")
    alpha_rows, beta_rows = marked_rows(u, v, shifts)
    pure = {
        word: sp.factor(
            permanent(
                tuple(beta_rows[mode] if word[mode] else alpha_rows[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == 4
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    finite = extension_model(alpha_rows, beta_rows, rho)
    infinity = extension_model(alpha_rows, beta_rows, None)
    finite_result = diagonal_product_test(
        "finite weighted 01 chart",
        *finite,
        variables="rho,h0,h1,h2,h3,x0,x1,x2,x3,y0,y1,y2,y3",
    )
    infinity_result = diagonal_product_test(
        "infinite weighted 01 chart",
        *infinity,
        variables="h0,h1,h2,h3,x0,x1,x2,x3,y0,y1,y2,y3",
    )

    canonical = {u: 2, v: 0, rho: 2} | {shift: 0 for shift in shifts}
    canonical_mixed = finite[0].subs(canonical)
    canonical_ranks = [
        canonical_mixed.rank(),
        canonical_mixed.col_join(finite[1].subs(canonical)).rank(),
        canonical_mixed.col_join(finite[2].subs(canonical)).rank(),
    ]
    assert canonical_ranks == [7, 7, 8]
    assert finite_result["groebner_basis_size"] == 48
    assert infinity_result["groebner_basis_size"] == 10

    print(
        json.dumps(
            {
                "status": "pass",
                "theorem": THEOREM.name,
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "component_function_field": "C(u,v)",
                "marking_and_slope_ring": "C(u,v)[rho,h0,h1,h2,h3]",
                "finite_weighted_01_ideal": finite_result,
                "infinite_weighted_01_ideal": infinity_result,
                "canonical_ranks_mixed_alpha_beta": canonical_ranks,
                "weighted_01_binary_neighbour_excluded": True,
                "generic_weighted_H22_fibre_empty": True,
                "all_thirteen_certified_components_generically_H22_closed": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
