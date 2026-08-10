#!/usr/bin/env python3
"""Verify the generic H31 obstruction on the eleventh pure-P4 component."""

from __future__ import annotations

import hashlib
import itertools
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


ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


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
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(coefficient * entry) for entry in row)


def marked_rows(
    p: sp.Symbol, q: sp.Symbol, r: sp.Symbol, shifts: tuple[sp.Symbol, ...]
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    radius = r + 1
    u = add(a, scale(p, b))
    v = add(a_bar, scale(q, b))
    alpha_0 = add(scale(1 + q * radius, u), scale(-p * radius, v))
    alpha = (alpha_0, a, a, b_bar)
    canonical_beta = (
        u,
        add(a_bar, b),
        add(scale(r, a_bar), b),
        a_bar,
    )
    beta = tuple(
        tuple(
            sp.expand(canonical_beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def row_module_test(
    distinguished: int,
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
    expected_size: int,
) -> dict[str, int | bool]:
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(singular(diagonal_alpha[0, column]) for column in range(8)) + "]"
    beta_vector = "[" + ",".join(singular(diagonal_beta[0, column]) for column in range(8)) + "]"
    program = "\n".join(
        (
            "ring R=(0,p,q,r),(h0,h1,h2,h3),dp;",
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
        timeout=60,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((distinguished, completed.returncode, completed.stdout, completed.stderr))
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    _, alpha_zero, beta_nonzero, basis_size = results[0].split(":")
    assert alpha_zero == "1"
    assert beta_nonzero == "1"
    assert int(basis_size) == expected_size
    return {
        "all_alpha_remainder_zero": True,
        "all_beta_remainder_nonzero": True,
        "reduced_module_basis_size": int(basis_size),
    }


def main() -> None:
    p, q, r = sp.symbols("p q r", nonzero=True)
    shifts = sp.symbols("h0:4")
    alpha, beta = marked_rows(p, q, r, shifts)

    pure = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] + 4 * p * (r + 1)) == 0
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    expected_sizes = (4, 4, 8, 8)
    module_results = []
    canonical_ranks = []
    stacked_alpha_ranks = []
    stacked_beta_ranks = []
    canonical_substitution = {p: 1, q: 2, r: 2} | {shift: 0 for shift in shifts}
    for distinguished, expected_size in enumerate(expected_sizes):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
        if distinguished < 2:
            assert diagonal_alpha == sp.zeros(1, 8)
        else:
            radius = r + 1
            Q = 1 + q * radius
            expected = (
                (-2, -2 * Q, -2 * Q, 2 * p, 0, 0, 0, 0)
                if distinguished == 2
                else (2, 2 * Q, 2 * Q, 2 * p, 0, 0, 0, 0)
            )
            assert all(
                sp.factor(diagonal_alpha[0, index] - expected[index]) == 0
                for index in range(8)
            )
        module_results.append(
            row_module_test(
                distinguished,
                mixed,
                diagonal_alpha,
                diagonal_beta,
                expected_size,
            )
        )
        canonical = mixed.subs(canonical_substitution)
        canonical_ranks.append(canonical.rank())
        stacked_alpha_ranks.append(canonical.col_join(diagonal_alpha.subs(canonical_substitution)).rank())
        stacked_beta_ranks.append(canonical.col_join(diagonal_beta.subs(canonical_substitution)).rank())

    assert canonical_ranks == [4, 4, 7, 7]
    assert stacked_alpha_ranks == [4, 4, 7, 7]
    assert stacked_beta_ranks == [5, 5, 8, 8]

    print(
        json.dumps(
            {
                "status": "pass",
                "theorem": THEOREM.name,
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "component_function_field": "C(p,q,r)",
                "marking_ring": "C(p,q,r)[h0,h1,h2,h3]",
                "module_results": module_results,
                "canonical_mixed_ranks": canonical_ranks,
                "canonical_stacked_alpha_ranks": stacked_alpha_ranks,
                "canonical_stacked_beta_ranks": stacked_beta_ranks,
                "binary_neighbour_excluded": True,
                "all_eleven_certified_components_generically_H31_closed": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
