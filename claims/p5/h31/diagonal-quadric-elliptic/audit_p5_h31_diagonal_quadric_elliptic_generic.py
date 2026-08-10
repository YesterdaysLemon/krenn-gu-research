#!/usr/bin/env python3
"""Independent exact audit of the generic elliptic-surface obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.singular_runtime import singular_command_with_timeout


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md"
)
PRIMARY = ROOT / "verify_p5_h31_diagonal_quadric_elliptic_generic.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
EXPECTED_PROJECTIONS = {coordinate: ("1",) for coordinate in range(4)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    next_states.get(new_mask, sp.Integer(0))
                    + coefficient * entry
                )
        states = next_states
    return sp.expand(states[15])


def remainder_mod_quadratic(
    expression: sp.Expr,
    variable: sp.Symbol,
    relation: sp.Expr,
) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, variable),
        sp.Poly(relation, variable),
    ).as_expr()
    return sp.factor(remainder / denominator)


def extension_system(
    distinguished: int,
    alpha,
    beta,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    extensions = sp.symbols("a0:4") + sp.symbols("b0:4")
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    extended_alpha = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extensions[mode],)
        for mode, row in enumerate(alpha)
    )
    extended_beta = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extensions[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent_dp(tuple(
            extended_beta[mode] if word[mode] else extended_alpha[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], variable) for variable in extensions]
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    diagonal_a = sp.Matrix([[
        sp.diff(coefficients[(0, 0, 0, 0)], variable)
        for variable in extensions
    ]])
    diagonal_b = sp.Matrix([[
        sp.diff(coefficients[(1, 1, 1, 1)], variable)
        for variable in extensions
    ]])
    return mixed, diagonal_a, diagonal_b


def singular(expression: sp.Expr) -> str:
    return str(sp.together(sp.expand(expression))).replace("**", "^")


def run_projection(
    distinguished: int,
    alpha,
    beta,
    r: sp.Symbol,
    x: sp.Symbol,
    Y: sp.Symbol,
    elliptic_relation: sp.Expr,
    timeout: float = 120,
) -> tuple[str, ...]:
    extensions = sp.symbols("a0:4") + sp.symbols("b0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("ua")
    mixed, diagonal_a, diagonal_b = extension_system(
        distinguished,
        alpha,
        beta,
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.extend(
        (
            (diagonal_a * extension)[0] - 1,
            inverse * (diagonal_b * extension)[0] - 1,
            elliptic_relation,
        )
    )
    eliminated = extensions + (inverse,)
    retained = shifts + (Y,)
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring R=(0,"
            + str(r)
            + ","
            + str(x)
            + "),("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));",
            "option(redSB);",
            "ideal incidence=" + ",".join(map(singular, equations)) + ";",
            "ideal basis=std(incidence);",
            "ideal marking=eliminate(basis,"
            + "*".join(map(str, eliminated))
            + ");",
            "marking=std(marking);",
            '"MARKING";',
            "marking;",
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 5,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "independent elliptic projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    output = completed.stdout.replace("\r\n", "\n")
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def main() -> None:
    r, x, Y = sp.symbols("r x Y")
    t = sp.symbols("t0:4")
    denominator = x + r**2 - 1
    cubic = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    elliptic_relation = Y**2 - cubic

    # Clear every rational-row denominator.  These factors are units in
    # Q(r,x), so the resulting rows give the same generic plane tuple.
    alpha0 = (
        Y + r**2 * x,
        -r * x - r**2 * x,
        -r * x + r**2 * x,
        -Y + r**2 * x,
    )
    alpha = (
        alpha0,
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (r, -1, -1, r),
    )
    canonical_beta = (
        (1, -1, 1, 1),
        (
            denominator,
            r * x + denominator,
            r * x - denominator,
            denominator,
        ),
        (
            x * (1 - x) + Y,
            r * x,
            r * x,
            x * (1 - x) - Y,
        ),
        (0, 1, 1, 0),
    )
    beta = tuple(
        tuple(
            sp.expand(
                canonical_beta[mode][coordinate]
                + t[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    pure = {
        word: remainder_mod_quadratic(
            permanent_dp(tuple(
                canonical_beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )),
            Y,
            elliptic_relation,
        )
        for word in WORDS
    }
    assert all(
        coefficient == 0
        for word, coefficient in pure.items()
        if word != (1, 1, 1, 1)
    )
    assert sp.factor(
        pure[(1, 1, 1, 1)]
        + 4 * r * x * (x - 1 - r) * (x - 1 + r)
    ) == 0

    projections = {
        distinguished: run_projection(
            distinguished,
            alpha,
            beta,
            r,
            x,
            Y,
            elliptic_relation,
        )
        for distinguished in range(4)
    }
    assert projections == EXPECTED_PROJECTIONS

    output = {
        "audited": True,
        "field": "C",
        "method": (
            "independent dynamic-programming permanent, denominator-cleared "
            "plane rows, exact function-field projection"
        ),
        "coefficient_field": "Q(r,x)",
        "retained_algebraic_coordinate": "Y",
        "all_row_denominators_cleared": True,
        "relative_projection_ideals": {
            str(key): list(value) for key, value in projections.items()
        },
        "generic_binary_extension_exists": False,
        "generic_H31_fibre_empty": True,
        "whole_second_component_closed": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_diagonal_quadric_elliptic_generic_audited.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
