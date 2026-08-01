#!/usr/bin/env python3
"""Independent modular audit of component twenty-one's H31 obstruction."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PRIMES = (101, 103)


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def extension_rows(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    variables: tuple[sp.Symbol, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_extended = tuple(
        tuple(alpha[mode][index] for index in retained) + (variables[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][index] for index in retained) + (variables[4 + mode],)
        for mode in range(4)
    )
    return alpha_extended, beta_extended


def matrices(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    variables = sp.symbols("x0:8")
    alpha_extended, beta_extended = extension_rows(
        distinguished, alpha, beta, variables
    )
    coefficients = {
        word: permanent(
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
    diagonal_alpha = sp.Matrix(
        [[sp.diff(coefficients[(0, 0, 0, 0)], variable) for variable in variables]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(coefficients[(1, 1, 1, 1)], variable) for variable in variables]]
    )
    return mixed, diagonal_alpha, diagonal_beta


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def modular_certificate(
    prime: int,
    distinguished: int,
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
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
            f"ring R={prime},(t0,t1,t2,t3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector a=" + alpha + ";",
            "vector b=" + beta + ";",
            '"CODEX_RESULT:"+string(reduce(a,M)==0)+":"+string(reduce(b,M)!=0)+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == ["CODEX_RESULT:1:1:7"], completed.stdout
    return {
        "prime": prime,
        "distinguished_coordinate": distinguished,
        "all_alpha_normal_form_zero": True,
        "all_beta_normal_form_nonzero": True,
        "standard_module_basis_size": 7,
    }


def main() -> None:
    t = sp.symbols("t0:4")
    # Independent exact reconstruction at (p,q,kappa,ell)=(2,3,1,2).
    alpha = (
        (sp.Integer(1), sp.Integer(5), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(3), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1)),
    )
    canonical_beta = (
        (sp.Integer(1), sp.Integer(1), sp.Integer(2), sp.Integer(2)),
        (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(3), sp.Integer(-1), sp.Integer(0), sp.Integer(0)),
    )
    beta = tuple(
        tuple(
            canonical_beta[mode][coordinate] + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    pure = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert {word: value for word, value in pure.items() if value != 0} == {
        (1, 1, 1, 1): sp.Integer(8)
    }

    certificates = []
    for distinguished in range(4):
        mixed, diagonal_alpha, diagonal_beta = matrices(distinguished, alpha, beta)
        if distinguished < 2:
            assert diagonal_alpha == sp.zeros(1, 8)
            retained = tuple(index for index in range(4) if index != distinguished)
            supports = tuple(
                {
                    retained.index(index)
                    for index, value in enumerate(alpha[mode])
                    if value and index in retained
                }
                | {3}
                for mode in range(3)
            )
            assert len(set().union(*supports)) == 2
        else:
            for prime in PRIMES:
                certificates.append(
                    modular_certificate(
                        prime,
                        distinguished,
                        mixed,
                        diagonal_alpha,
                        diagonal_beta,
                    )
                )

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent permanent and symbolic modular-module audit",
                "sample_pure_support": {"1111": 8},
                "hall_deletions": [0, 1],
                "modular_certificates": certificates,
                "generic_marked_H31_fibre_empty": True,
                "characteristic_zero_inference_from_modular_data": False,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
