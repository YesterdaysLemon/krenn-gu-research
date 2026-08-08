#!/usr/bin/env python3
"""Verify generic marked-H31 exclusion on pure-P4 component twenty-one."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
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

from verify_p5_h31_marked_basis_open_branch import mixed_matrix

ROOT = REPO_ROOT
THEOREM = (
    HERE / "P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


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


def pure_bases(
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    ell: sp.Symbol,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    row_00 = add(a, scale(p, b))
    row_01 = add(c, scale(q, b))
    alpha = (
        add(scale(q, row_00), scale(-p, row_01)),
        add(scale(ell, a), c),
        c,
        d,
    )
    beta = (
        row_00,
        a,
        add(b, scale(kappa, a)),
        add(a, scale(ell, c)),
    )
    return alpha, beta


def shifted(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact row-module replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.factor(expression)).replace("**", "^")


def module_certificate(
    distinguished: int,
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
    expected_size: int,
) -> dict[str, object]:
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha = (
        "[" + ",".join(singular(diagonal_alpha[0, column]) for column in range(8)) + "]"
    )
    beta = (
        "[" + ",".join(singular(diagonal_beta[0, column]) for column in range(8)) + "]"
    )
    program = "\n".join(
        (
            "ring R=(0,p,q,kappa,ell),(t0,t1,t2,t3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector a=" + alpha + ";",
            "vector b=" + beta + ";",
            "vector ra=reduce(a,M);",
            "vector rb=reduce(b,M);",
            '"CODEX_RESULT:"+string(ra==0)+":"+string(rb!=0)+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((distinguished, completed.stdout, completed.stderr))
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, alpha_zero, beta_nonzero, size = markers[0].split(":")
    assert alpha_zero == "1"
    assert beta_nonzero == "1"
    assert int(size) == expected_size
    return {
        "distinguished_coordinate": distinguished,
        "all_alpha_normal_form_zero": True,
        "all_beta_normal_form_nonzero": True,
        "standard_module_basis_size": int(size),
    }


def main() -> None:
    p, q, kappa, ell = sp.symbols("p q kappa ell")
    shifts = sp.symbols("t0:4")
    alpha, canonical_beta = pure_bases(p, q, kappa, ell)
    beta = shifted(alpha, canonical_beta, shifts)

    pure = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] - 4 * p) == 0
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    sample = {p: 2, q: 3, kappa: 1, ell: 2} | {shift: 0 for shift in shifts}
    expected_sizes = (2, 2, 7, 7)
    mixed_ranks: list[int] = []
    stacked_alpha_ranks: list[int] = []
    stacked_beta_ranks: list[int] = []
    certificates = []
    for distinguished, expected_size in enumerate(expected_sizes):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
        if distinguished < 2:
            assert diagonal_alpha == sp.zeros(1, 8)
        certificates.append(
            module_certificate(
                distinguished,
                mixed,
                diagonal_alpha,
                diagonal_beta,
                expected_size,
            )
        )
        specialized = mixed.subs(sample)
        mixed_ranks.append(specialized.rank())
        stacked_alpha_ranks.append(
            specialized.col_join(diagonal_alpha.subs(sample)).rank()
        )
        stacked_beta_ranks.append(
            specialized.col_join(diagonal_beta.subs(sample)).rank()
        )

    assert mixed_ranks == [2, 2, 7, 7]
    assert stacked_alpha_ranks == mixed_ranks
    assert stacked_beta_ranks == [3, 3, 8, 8]

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(p,q,kappa,ell)",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "pure_support": {"1111": "4*p"},
                "all_affine_markings": True,
                "module_certificates": certificates,
                "sample_mixed_ranks": mixed_ranks,
                "sample_stacked_alpha_ranks": stacked_alpha_ranks,
                "sample_stacked_beta_ranks": stacked_beta_ranks,
                "generic_marked_H31_fibre_empty": True,
                "weighted_H22_closed": False,
                "component_boundaries_closed": False,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
