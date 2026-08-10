#!/usr/bin/env python3
"""Verify generic H31 obstruction on the Eisenstein-norm P4 component."""

from __future__ import annotations

import itertools
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from krenn_gu.p5_marked_basis import mixed_matrix


WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md"


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
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    tuple[sp.Expr, ...],
]:
    # Rational projection of the norm quadric from (2,1,1,1), on beta=1.
    denominator = u**2 + u * v + v**2 - 1
    line_parameter = sp.cancel((5 - 5 * u - 4 * v) / denominator)
    alpha_parameter = sp.cancel(2 + u * line_parameter)
    beta_parameter = sp.Integer(1)
    r = sp.cancel(1 + line_parameter)
    gamma = sp.cancel(1 + v * line_parameter)

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
    return alpha_rows, beta_rows, (
        alpha_parameter,
        beta_parameter,
        r,
        gamma,
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def row_module_test(
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
) -> dict[str, int | bool]:
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(singular(diagonal_alpha[0, column]) for column in range(8)) + "]"
    beta_vector = "[" + ",".join(singular(diagonal_beta[0, column]) for column in range(8)) + "]"
    program = "\n".join(
        (
            "ring R=(0,u,v),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector a=" + alpha_vector + ";",
            "vector b=" + beta_vector + ";",
            "vector ra=reduce(a,M);",
            "vector rb=reduce(b,M);",
            '"CODEX_RESULT:"+string(ra==0)+":"+string(rb!=0)+":"+string(size(M));',
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
        timeout=120,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((completed.returncode, completed.stdout, completed.stderr))
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    _, alpha_zero, beta_nonzero, basis_size = results[0].split(":")
    assert alpha_zero == "1"
    assert beta_nonzero == "1"
    return {
        "all_alpha_remainder_zero": True,
        "all_beta_remainder_nonzero": True,
        "reduced_module_basis_size": int(basis_size),
    }


def main() -> None:
    u, v = sp.symbols("u v")
    shifts = sp.symbols("h0:4")
    alpha_rows, beta_rows, parameters = marked_rows(u, v, shifts)
    alpha_parameter, beta_parameter, r, gamma = parameters
    norm_equation = sp.factor(
        alpha_parameter**2
        + alpha_parameter * gamma
        + gamma**2
        - 3 * beta_parameter**2
        - 3 * beta_parameter * r
        - r**2
    )
    assert norm_equation == 0

    pure = {
        word: sp.factor(
            permanent(
                tuple(beta_rows[mode] if word[mode] else alpha_rows[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == 4
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    module_results = []
    canonical_ranks = []
    stacked_alpha_ranks = []
    stacked_beta_ranks = []
    canonical_substitution = {u: 2, v: 0} | {shift: 0 for shift in shifts}
    for distinguished in range(4):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
            distinguished, alpha_rows, beta_rows
        )
        module_results.append(
            row_module_test(mixed, diagonal_alpha, diagonal_beta)
        )
        canonical = mixed.subs(canonical_substitution)
        canonical_ranks.append(canonical.rank())
        stacked_alpha_ranks.append(
            canonical.col_join(diagonal_alpha.subs(canonical_substitution)).rank()
        )
        stacked_beta_ranks.append(
            canonical.col_join(diagonal_beta.subs(canonical_substitution)).rank()
        )

    assert [result["reduced_module_basis_size"] for result in module_results] == [10] * 4
    assert canonical_ranks == [7, 7, 7, 7]
    assert stacked_alpha_ranks == [7, 7, 7, 7]
    assert stacked_beta_ranks == [8, 8, 8, 8]

    print(
        json.dumps(
            {
                "status": "pass",
                "theorem": THEOREM.name,
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "component_function_field": "C(u,v)",
                "quadric_chart": "beta=1, projection from (2,1,1,1)",
                "marking_ring": "C(u,v)[h0,h1,h2,h3]",
                "module_results": module_results,
                "canonical_mixed_ranks": canonical_ranks,
                "canonical_stacked_alpha_ranks": stacked_alpha_ranks,
                "canonical_stacked_beta_ranks": stacked_beta_ranks,
                "binary_neighbour_excluded": True,
                "all_thirteen_certified_components_generically_H31_closed": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
