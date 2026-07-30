#!/usr/bin/env python3
"""Generate the full marked-fibre incidence on the chart boundary."""

from __future__ import annotations

import argparse
import subprocess

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import (
    singular_command_with_timeout,
)
from verify_p5_h31_marked_basis_open_branch import mixed_matrix


def rows() -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
]:
    """Return the H=N=1 normalized boundary and all row shifts."""
    A, R = sp.symbols("A R")
    t = sp.symbols("t0:4")
    canonical_alpha = (
        (1, 0, A, A - 1),
        (0, 0, 1, 1),
        (0, 1, 0, R),
        (1, 0, 1, 0),
    )
    beta = (
        (0, 1, 0, -R),
        (R, 1, -R, -R),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    alpha = tuple(
        tuple(
            canonical_alpha[mode][coordinate]
            + t[mode] * beta[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def singular_program(distinguished: int) -> str:
    A, R = sp.symbols("A R")
    t = sp.symbols("t0:4")
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    inverse_a, inverse_b = sp.symbols("ua ub")
    extension = sp.Matrix(x + y)
    alpha, beta = rows()
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    equations = list(mixed * extension)
    equations.extend((
        (diagonal_a * extension)[0] - 1,
        inverse_b * (diagonal_b * extension)[0] - 1,
        inverse_a * A - 1,
    ))
    eliminated = x + y + (inverse_a, inverse_b)
    retained = (A, R) + t
    variables = eliminated + retained
    return "\n".join((
        "ring B=0,("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal incidence=" + ",".join(map(singular, equations)) + ";",
        "ideal basis=slimgb(incidence);",
        "ideal marking=eliminate(basis,"
        + "*".join(map(str, eliminated))
        + ");",
        "marking=slimgb(marking);",
        f'"Q={distinguished}_ABSOLUTE";',
        '"BASIS_SIZE"; size(basis);',
        '"MARKING_SIZE"; size(marking);',
        "marking;",
        "quit;",
        "",
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=range(4))
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--timeout", type=float, default=120)
    arguments = parser.parse_args()
    program = singular_program(arguments.q)
    if not arguments.run:
        print(program, end="")
        return
    completed = subprocess.run(
        singular_command_with_timeout(arguments.timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=arguments.timeout + 5,
        check=False,
    )
    print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
