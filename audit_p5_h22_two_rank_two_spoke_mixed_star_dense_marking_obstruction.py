#!/usr/bin/env python3
"""Independent audit of the tenth-component dense-marking H22 result."""

from __future__ import annotations

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
PRIMARY = (
    ROOT
    / "verify_p5_h22_two_rank_two_spoke_mixed_star_dense_marking_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_top(rows) -> sp.Expr:
    coefficients = {0: sp.Integer(1)}
    for row in rows:
        updated: dict[int, sp.Expr] = {}
        for support, coefficient in coefficients.items():
            for coordinate, entry in enumerate(row):
                bit = 1 << coordinate
                if support & bit:
                    continue
                target = support | bit
                updated[target] = sp.expand(
                    updated.get(target, 0) + coefficient * entry
                )
        coefficients = updated
    return sp.expand(coefficients.get(15, 0))


def rows(u, v):
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


def standard(row):
    a, a_bar, b, b_bar = row
    return (a + a_bar, a - a_bar, b + b_bar, b - b_bar)


def project(row, extension, direction, rho):
    a, a_bar, b, b_bar = row
    if direction == "01":
        return (a + rho * a_bar, b + b_bar, b - b_bar, extension)
    return (a + a_bar, a - a_bar, b + rho * b_bar, extension)


def extension_matrix(alpha, beta, shifts, direction, rho):
    extension = sp.symbols("z0:8")
    marked = tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    alpha_projected = tuple(
        project(alpha[mode], extension[mode], direction, rho)
        for mode in range(4)
    )
    beta_projected = tuple(
        project(marked[mode], extension[4 + mode], direction, rho)
        for mode in range(4)
    )
    coefficients = {
        word: squarefree_top(
            tuple(
                beta_projected[mode]
                if word[mode]
                else alpha_projected[mode]
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


def module_audit(matrix: sp.Matrix) -> int:
    generators = ",".join(
        "[" + ",".join(singular(matrix[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    program = "\n".join(
        (
            "ring R=(0,rho),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module N=" + generators + ";",
            "N=std(N);",
            "int full=(size(N)==8);",
            '"CODEX_RESULT:"+string(full)+":"+string(size(N));',
            "N;",
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
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    assert "CODEX_RESULT:1:8" in completed.stdout, completed.stdout
    expected = {f"N[{index}]=gen({index})" for index in range(1, 9)}
    observed = {
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("N[")
    }
    assert observed == expected
    return 8


def main() -> None:
    u, v, rho = sp.symbols("u v rho")
    shifts = sp.symbols("h0:4")
    alpha, beta = rows(u, v)

    pure = {
        word: sp.factor(
            squarefree_top(
                tuple(
                    standard(beta[mode] if word[mode] else alpha[mode])
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert sp.expand(
        pure[(1, 1, 1, 1)] - 4 * (u - 1) * (v - 1) * (u * v - 1)
    ) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    matrices = {
        direction: extension_matrix(alpha, beta, shifts, direction, rho)
        for direction in ("01", "23")
    }
    sample_points = {
        "s3_t5": {u: sp.Rational(1, 2), v: sp.Rational(2, 3)},
        "s5_t7": {u: sp.Rational(2, 3), v: sp.Rational(3, 4)},
    }
    module_sizes = {
        label: {
            direction: module_audit(matrix.subs(sample))
            for direction, matrix in matrices.items()
        }
        for label, sample in sample_points.items()
    }

    canonical_rows = tuple(range(8))
    sample = {u: sp.Rational(1, 3), v: sp.Rational(1, 2), rho: sp.Rational(2, 3)}
    canonical_ranks = {}
    canonical_determinants = {}
    for direction, matrix in matrices.items():
        canonical = matrix.subs(dict.fromkeys(shifts, 0))
        determinant = sp.factor(
            canonical.extract(canonical_rows, range(8)).det(method="domain-ge")
        )
        canonical_determinants[direction] = sp.factor(determinant.subs(sample))
        canonical_ranks[direction] = canonical.subs(sample).rank()
        assert canonical_determinants[direction] != 0
        assert canonical_ranks[direction] == 8

    result = {
        "audit_method": "independent subset-DP permanent and exact sample modules",
        "canonical_determinants_at_s2_t3_r5": {
            direction: str(value)
            for direction, value in canonical_determinants.items()
        },
        "canonical_ranks": canonical_ranks,
        "independent_of_primary_implementation": True,
        "sample_complete_marking_module_sizes": module_sizes,
        "primary_sha256": sha256(PRIMARY),
        "theorem_sha256": sha256(THEOREM),
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
