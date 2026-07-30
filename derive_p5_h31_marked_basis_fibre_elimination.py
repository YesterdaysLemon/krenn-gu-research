#!/usr/bin/env python3
"""Emit exact Singular projections for the H31 marked-basis fibre.

The proof uses two weighted source normalizations:

* ``--absolute --normalize-l`` is the complete L!=0 chart;
* ``--absolute --normalize-c-l0`` is the complete L=0,D!=0 chart.

The other stratum switches are retained as compact independent
cross-checks of the constructible case split.
"""

from __future__ import annotations

import argparse
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verify_p5_h31_marked_basis_open_branch import mixed_matrix


def singular(expression: sp.Expr) -> str:
    text = str(sp.expand(expression)).replace("**", "^")
    return (
        text.replace("L", "ll")
        .replace("Q", "qq")
        .replace("C", "cc")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("distinguished", type=int, choices=range(4))
    parser.add_argument(
        "--stratum",
        choices=(
            "generic",
            "Q0",
            "A0",
            "B0",
            "AB0",
            "L0",
            "C0",
            "Q0C0",
            "LQ0",
            "L0B0",
        ),
        default="generic",
    )
    parser.add_argument("--absolute", action="store_true")
    parser.add_argument(
        "--variable-q",
        action="store_true",
        help=(
            "treat Q as an elimination-ring variable over Q(L,C); "
            "this is a smaller generic projection than --absolute"
        ),
    )
    parser.add_argument(
        "--normalize-l",
        action="store_true",
        help=(
            "with --absolute, set L=1 and retain Q,C as ring variables; "
            "this represents the L!=0 weighted-torus chart"
        ),
    )
    parser.add_argument(
        "--normalize-c-l0",
        action="store_true",
        help=(
            "with --absolute, set L=0,C=1 and retain Q as a ring "
            "variable; this represents the L=0,D!=0 chart"
        ),
    )
    parser.add_argument("--direct-normalization", action="store_true")
    parser.add_argument("--fast-groebner", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.output is not None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            emit(
                arguments.distinguished,
                arguments.stratum,
                arguments.absolute,
                arguments.variable_q,
                arguments.normalize_l,
                arguments.normalize_c_l0,
                arguments.direct_normalization,
                arguments.fast_groebner,
            )
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(buffer.getvalue(), encoding="utf-8")
        return

    emit(
        arguments.distinguished,
        arguments.stratum,
        arguments.absolute,
        arguments.variable_q,
        arguments.normalize_l,
        arguments.normalize_c_l0,
        arguments.direct_normalization,
        arguments.fast_groebner,
    )


def emit(
    distinguished: int,
    stratum: str,
    absolute: bool,
    variable_q: bool,
    normalize_l: bool,
    normalize_c_l0: bool,
    direct_normalization: bool,
    fast_groebner: bool,
) -> None:

    ll, qq, cc = sp.symbols("L Q C")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    d_value = cc + ll
    a_value = 1 + ll * qq
    alpha = (
        (1, qq, 0, -a_value),
        (ll, 1, -ll, -ll),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    canonical_beta = (
        (0, 1, d_value, cc),
        (0, 0, 1, 1),
        (0, 1, 0, ll),
        (1, 0, 1, 0),
    )
    beta = tuple(
        tuple(
            canonical_beta[mode][coordinate]
            + shifts[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    substitutions: dict[sp.Symbol, sp.Expr]
    parameters: tuple[str, ...]
    if absolute:
        if normalize_l and normalize_c_l0:
            raise ValueError(
                "--normalize-l and --normalize-c-l0 are mutually exclusive"
            )
        substitutions = (
            {ll: 1}
            if normalize_l
            else ({ll: 0, cc: 1} if normalize_c_l0 else {})
        )
        parameters = ()
    elif variable_q:
        if stratum != "generic":
            raise ValueError("--variable-q is supported only on the generic stratum")
        substitutions = {}
        parameters = ("ll", "cc")
    elif stratum == "generic":
        substitutions = {}
        parameters = ("ll", "qq", "cc")
    elif stratum == "Q0":
        substitutions = {qq: 0}
        parameters = ("ll", "cc")
    elif stratum == "A0":
        substitutions = {qq: -1 / ll}
        parameters = ("ll", "cc")
    elif stratum == "B0":
        substitutions = {qq: -1 / (cc + ll)}
        parameters = ("ll", "cc")
    elif stratum == "AB0":
        substitutions = {qq: -1 / ll, cc: 0}
        parameters = ("ll",)
    elif stratum == "L0":
        substitutions = {ll: 0}
        parameters = ("qq", "cc")
    elif stratum == "C0":
        substitutions = {cc: 0}
        parameters = ("ll", "qq")
    elif stratum == "Q0C0":
        substitutions = {qq: 0, cc: 0}
        parameters = ("ll",)
    elif stratum == "LQ0":
        substitutions = {ll: 0, qq: 0}
        parameters = ("cc",)
    else:
        substitutions = {ll: 0, qq: -1 / cc}
        parameters = ("cc",)
    mixed = mixed.subs(substitutions)
    diagonal_a = diagonal_a.subs(substitutions)
    diagonal_b = diagonal_b.subs(substitutions)
    equations = list(mixed * sp.Matrix(extensions))
    if direct_normalization:
        equations.extend((
            (diagonal_a * sp.Matrix(extensions))[0] - 1,
            sp.Symbol("ub") * (diagonal_b * sp.Matrix(extensions))[0] - 1,
        ))
        diagonal_inverses = (sp.Symbol("ub"),)
    else:
        equations.extend((
            sp.Symbol("ua") * (diagonal_a * sp.Matrix(extensions))[0] - 1,
            sp.Symbol("ub") * (diagonal_b * sp.Matrix(extensions))[0] - 1,
        ))
        diagonal_inverses = (sp.Symbol("ua"), sp.Symbol("ub"))
    if absolute:
        inverse_d = sp.Symbol("ud")
        equations.append(inverse_d * (cc + ll).subs(substitutions) - 1)
        absolute_parameters = (
            (sp.Symbol("qq"), sp.Symbol("cc"))
            if normalize_l
            else (
                (sp.Symbol("qq"),)
                if normalize_c_l0
                else (sp.Symbol("ll"), sp.Symbol("qq"), sp.Symbol("cc"))
            )
        )
        variables = (
            extensions
            + diagonal_inverses
            + (inverse_d,)
            + shifts
            + absolute_parameters
        )
        eliminated = (
            extensions
            + diagonal_inverses
            + (inverse_d,)
        )
        eliminated_count = len(eliminated)
        print(
            "ring r=0,("
            + ",".join(map(str, variables))
            + f"),(dp({eliminated_count}),dp({len(shifts) + len(absolute_parameters)}));"
        )
    else:
        retained_parameters = (
            (sp.Symbol("qq"),)
            if variable_q
            else ()
        )
        variables = (
            extensions
            + diagonal_inverses
            + shifts
            + retained_parameters
        )
        eliminated = extensions + diagonal_inverses
        eliminated_count = len(eliminated)
        print(
            "ring r=(0," + ",".join(parameters) + "),("
            + ",".join(map(str, variables))
            + f"),(dp({eliminated_count}),dp({len(shifts) + len(retained_parameters)}));"
        )
    if not fast_groebner:
        print("option(redSB);")
    print("ideal incidence=" + ",".join(map(singular, equations)) + ";")
    print(
        "ideal basis="
        + ("slimgb(incidence);" if fast_groebner else "std(incidence);")
    )
    print(
        "ideal marking=eliminate(basis,"
        + "*".join(map(str, eliminated))
        + ");"
    )
    print(
        "marking="
        + ("slimgb(marking);" if fast_groebner else "std(marking);")
    )
    print(
        '"STRATUM=' + ("absolute" if absolute else stratum)
        + '_DISTINGUISHED=' + str(distinguished) + '";'
    )
    print('"BASIS_SIZE"; size(basis);')
    print('"MARKING_SIZE"; size(marking);')
    print("marking;")
    print("quit;")


if __name__ == "__main__":
    main()
