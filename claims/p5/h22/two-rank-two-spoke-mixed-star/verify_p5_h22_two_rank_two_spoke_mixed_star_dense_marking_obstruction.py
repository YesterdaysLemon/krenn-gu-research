#!/usr/bin/env python3
"""Verify the dense-marking H22 obstruction on the tenth component."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md"
)
COMPONENT = REPO_ROOT / "claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md"
H31 = REPO_ROOT / "claims/p5/h31/two-rank-two-spoke-mixed-star/P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def cayley_rows(u: sp.Expr, v: sp.Expr):
    # Coordinates are coefficients of (a,a_bar,b,b_bar).  The row scalings
    # clear the Cayley denominators in s,t,d.
    alpha = (
        (1, 0, 1, 0),
        (1 - u, -1 - u, 1 - u, -1 + u),
        (1 - v, -1 - v, 1 - v, 1 - v),
        (0, 0, 0, 1 - u * v),
    )
    beta = (
        (0, 0, 1, 0),
        (0, -1 - u, 1 - u, 0),
        (0, -1 - v, 1 - v, 0),
        (1 - u * v, -1 - u * v, -1 + u * v, 0),
    )
    return alpha, beta


def standard_row(row):
    a, a_bar, b, b_bar = row
    return (a + a_bar, a - a_bar, b + b_bar, b - b_bar)


def weighted_row(row, extension, direction: str, rho):
    a, a_bar, b, b_bar = row
    if direction == "01":
        return (
            a + rho * a_bar,
            b + b_bar,
            b - b_bar,
            extension,
        )
    if direction == "23":
        return (
            a + a_bar,
            a - a_bar,
            b + rho * b_bar,
            extension,
        )
    raise ValueError(direction)


def mixed_matrix(alpha, beta, shifts, direction: str, rho):
    extension = sp.symbols("x0:4") + sp.symbols("y0:4")
    marked_beta = tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    alpha_weighted = tuple(
        weighted_row(alpha[mode], extension[mode], direction, rho)
        for mode in range(4)
    )
    beta_weighted = tuple(
        weighted_row(marked_beta[mode], extension[4 + mode], direction, rho)
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
    return sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in extension]
            for word in MIXED_WORDS
        ]
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def specialized_free_module_test(matrix: sp.Matrix, label: str) -> int:
    generators = ",".join(
        "[" + ",".join(singular(matrix[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    program = "\n".join(
        (
            "ring R=(0,rho),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "int full=(size(M)==8);",
            '"CODEX_RESULT:"+string(full)+":"+string(size(M));',
            "M;",
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
        raise AssertionError(
            (label, completed.returncode, completed.stdout, completed.stderr)
        )
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert results == ["CODEX_RESULT:1:8"], (label, completed.stdout)
    expected = {f"M[{index}]=gen({index})" for index in range(1, 9)}
    observed = {
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("M[")
    }
    assert observed == expected, (label, observed)
    return 8


def main() -> None:
    u, v, rho = sp.symbols("u v rho")
    shifts = sp.symbols("h0:4")
    alpha, beta = cayley_rows(u, v)

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    standard_row(beta[mode] if word[mode] else alpha[mode])
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    expected_pure = 4 * (u - 1) * (v - 1) * (u * v - 1)
    assert sp.expand(pure[(1, 1, 1, 1)] - expected_pure) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    matrices = {
        direction: mixed_matrix(alpha, beta, shifts, direction, rho)
        for direction in ("01", "23")
    }
    canonical = {
        direction: matrix.subs(dict.fromkeys(shifts, 0))
        for direction, matrix in matrices.items()
    }
    rows = tuple(range(8))
    minors = {
        direction: sp.factor(
            matrix.extract(rows, range(8)).det(method="domain-ge")
        )
        for direction, matrix in canonical.items()
    }
    expected_01 = (
        -2048
        * rho**2
        * (rho - 1)
        * (rho + 1)
        * (u - 1) ** 3
        * (u - v)
        * (v - 1) ** 3
        * (u * v - 1) ** 4
        * (2 * rho * u * v - 2 * rho + u * v - u - v + 1)
        * (
            -2 * rho * u**2 * v**2
            + 2 * rho * u**2 * v
            + 2 * rho * u * v**2
            - 2 * rho * u * v
            + u**3 * v**2
            + u**2 * v**3
            - 4 * u**2 * v**2
            + 4 * u * v
            - u
            - v
        )
    )
    expected_23 = (
        4096
        * rho**3
        * u
        * v
        * (rho - 1)
        * (rho + 1)
        * (u - 1) ** 2
        * (u + 1) ** 3
        * (u + v)
        * (v - 1) ** 2
        * (v + 1) ** 3
        * (u * v - 1) ** 4
    )
    assert sp.expand(minors["01"] - expected_01) == 0
    assert sp.expand(minors["23"] - expected_23) == 0

    sample = {u: sp.Rational(1, 3), v: sp.Rational(1, 2)}
    sample_module_sizes = {
        direction: specialized_free_module_test(matrix.subs(sample), direction)
        for direction, matrix in matrices.items()
    }

    result = {
        "canonical_marking_minors": {
            direction: str(value) for direction, value in minors.items()
        },
        "canonical_rows": list(rows),
        "cayley_parameters": {
            "u": "(s-1)/(s+1)",
            "v": "(t-1)/(t+1)",
            "d": "(1+u*v)/(1-u*v)",
            "rho": "(r-1)/(r+1)",
        },
        "dense_total_marking_open_binary_empty": True,
        "generic_component_complete_marking_fibre_closed": False,
        "generic_weighted_H22_fibre_closed": False,
        "method": "Cayley-toric gauge, two symbolic minors, and exact sample modules",
        "pure_coefficient": str(expected_pure),
        "sample_component_point": {"s": 2, "t": 3},
        "sample_complete_marking_fibres_empty": True,
        "sample_module_basis_sizes": sample_module_sizes,
        "search_used": False,
        "theorem": THEOREM.name,
        "verified": True,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            H31.name: sha256(H31),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
