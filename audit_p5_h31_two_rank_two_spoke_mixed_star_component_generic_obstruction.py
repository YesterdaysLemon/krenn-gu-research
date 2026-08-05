#!/usr/bin/env python3
"""Independent audit of the tenth-component generic H31 obstruction."""

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
    / "P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_top(rows) -> sp.Expr:
    """Coefficient of X_0 X_1 X_2 X_3 by subset dynamic programming."""
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


def planes(s: sp.Expr, t: sp.Expr):
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)

    def add(*rows):
        return tuple(sum(row[j] for row in rows) for j in range(4))

    def scale(value, row):
        return tuple(value * entry for entry in row)

    total = s + t
    return (
        (add(a, b), b),
        (add(a, b, scale(-1, b_bar), scale(-s, a_bar)), add(b, scale(-s, a_bar))),
        (add(a, b, b_bar, scale(-t, a_bar)), add(b, scale(-t, a_bar))),
        (
            b_bar,
            (total - 1 - s * t, total + 1 + s * t, -total, -total),
        ),
    )


def extension_rows(
    distinguished: int,
    alpha,
    beta,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    extension = sp.symbols("z0:8")
    common = tuple(j for j in range(4) if j != distinguished)
    alpha_extended = tuple(
        tuple(alpha[mode][j] for j in common) + (extension[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][j] for j in common) + (extension[4 + mode],)
        for mode in range(4)
    )
    coefficients = {
        word: squarefree_top(
            tuple(
                beta_extended[mode] if word[mode] else alpha_extended[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    rows = {
        word: [sp.diff(coefficients[word], variable) for variable in extension]
        for word in WORDS
    }
    mixed = sp.Matrix(
        [
            rows[word]
            for word in WORDS
            if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
        ]
    )
    return (
        mixed,
        sp.Matrix([rows[(0, 0, 0, 0)]]),
        sp.Matrix([rows[(1, 1, 1, 1)]]),
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def specialized_module_audit(
    s_value: int,
    t_value: int,
    distinguished: int,
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
) -> int:
    substitution = {sp.Symbol("s"): s_value, sp.Symbol("t"): t_value}
    mixed = mixed.subs(substitution)
    diagonal_alpha = diagonal_alpha.subs(substitution)
    diagonal_beta = diagonal_beta.subs(substitution)
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(
        singular(diagonal_alpha[0, column]) for column in range(8)
    ) + "]"
    beta_vector = "[" + ",".join(
        singular(diagonal_beta[0, column]) for column in range(8)
    ) + "]"
    program = "\n".join(
        (
            "ring R=0,(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module N=" + generators + ";",
            "N=std(N);",
            "vector a=" + alpha_vector + ";",
            "vector b=" + beta_vector + ";",
            "vector ra=reduce(a,N);",
            "vector rb=reduce(b,N);",
            "int good=((ra==0)&&(rb!=0));",
            '"CODEX_RESULT:"+string(good)+":"+string(size(N));',
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
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    _, good, basis_size = results[0].split(":")
    assert good == "1"
    return int(basis_size)


def main() -> None:
    s, t = sp.symbols("s t")
    shifts = sp.symbols("h0:4")
    component_planes = planes(s, t)
    alpha = tuple(rows[0] for rows in component_planes)
    beta = tuple(
        tuple(
            sp.expand(component_planes[mode][1][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    pure = {
        word: sp.factor(
            squarefree_top(
                tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] + 4 * (s + t)) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    kernels = (
        (-1, s - 1, t - 1, 0, -shifts[0], shifts[1] * (s - 1) + s, shifts[2] * (t - 1) + t, (s - 1) * (t - 1)),
        (-1, -s - 1, -t - 1, 0, -shifts[0], -shifts[1] * (s + 1) - s, -shifts[2] * (t + 1) - t, -(s + 1) * (t + 1)),
        (-1, 0, -2, -1, -shifts[0] - 1, -1, -2 * shifts[2] - 1, -shifts[3] + s + t),
        (1, 2, 0, -1, shifts[0] + 1, 2 * shifts[1] + 1, 1, -shifts[3] - s - t),
    )
    expected = (4 * (s + t), 4 * (s + t), 4 * (s + t), -4 * (s + t))
    sample_sizes: dict[str, list[int]] = {"2,3": [], "3,5": []}
    for distinguished in range(4):
        mixed, diagonal_alpha, diagonal_beta = extension_rows(
            distinguished, alpha, beta
        )
        kernel = sp.Matrix(kernels[distinguished])
        assert all(sp.factor(entry) == 0 for entry in mixed * kernel)
        assert sp.factor((diagonal_alpha * kernel)[0]) == 0
        assert sp.factor((diagonal_beta * kernel)[0] - expected[distinguished]) == 0
        for sample in ((2, 3), (3, 5)):
            sample_sizes[f"{sample[0]},{sample[1]}"].append(
                specialized_module_audit(
                    *sample,
                    distinguished,
                    mixed,
                    diagonal_alpha,
                    diagonal_beta,
                )
            )

    result = {
        "audit_method": "independent subset-DP reconstruction and exact all-marking module tests",
        "global_kernel_identities": True,
        "independent_of_primary_implementation": True,
        "sample_component_points": [[2, 3], [3, 5]],
        "sample_module_basis_sizes": sample_sizes,
        "theorem_sha256": sha256(THEOREM),
        "primary_sha256": sha256(PRIMARY),
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
