#!/usr/bin/env python3
"""Verify the complete marked fibre on the component-chart divisor."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

from derive_p5_h31_chart_boundary_marked_fibre_elimination import (
    rows,
    singular,
    singular_program,
)
from p5_high_coordinate_tree_chart_cegar import (
    singular_command_with_timeout,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md"
)
PLANE = ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
CANONICAL = (
    ROOT
    / "claims/p5/h31/component-chart-boundary/P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md"
)
GENERATOR = (
    ROOT / "derive_p5_h31_chart_boundary_marked_fibre_elimination.py"
)

EXPECTED_PROJECTION = {
    0: (
        "t3",
        "t2",
        "t0*t1",
        "R^2*t1+A*R-R",
        "A*R*t0-R*t0",
    ),
    1: (
        "t3",
        "t2",
        "t1",
        "2*R*t0-A+1",
        "A*t0+t0",
        "A^2-1",
    ),
    2: ("t3", "t2", "t1", "A*R*t0-R*t0"),
    3: (
        "t2",
        "t1",
        "A*t3-t3^2+t3",
        "R*t0*t3+t3",
        "A*R*t0+R*t0+t3",
    ),
}

CERTIFICATES = {
    0: (
        (2, (0, 2, 3, 7)),
        (2, (0, 3, 6, 7)),
        (2, (0, 2, 6, 7)),
        (0, (0, 4, 5, 7)),
    ),
    1: (
        (0, (0, 3, 5, 7)),
        (0, (0, 4, 5, 7)),
    ),
    2: (
        (2, (0, 2, 3, 7)),
        (2, (0, 3, 6, 7)),
        (2, (0, 2, 6, 7)),
    ),
    3: (
        (2, (0, 2, 3, 7)),
        (2, (0, 3, 6, 7)),
        (0, (0, 4, 5, 7)),
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(expression)) == 0


def run_singular(program: str, timeout: float = 90) -> str:
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
                "Singular failure",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return completed.stdout.replace("\r\n", "\n")


def projection_basis(output: str) -> tuple[str, ...]:
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def check_normalization() -> None:
    A0, H, N, R = sp.symbols("A0 H N R", nonzero=True)
    shifts = sp.symbols("s0:4")
    original_alpha = (
        (1, 0, A0, H * (A0 - N)),
        (0, 0, 1, H),
        (0, 1, 0, H * N * R),
        (1, 0, N, 0),
    )
    original_beta = (
        (0, 1, 0, -H * N * R),
        (R, 1, -R * N, -R * H * N),
        (-1 / N, 0, 1, 0),
        (0, 0, -1 / H, 1),
    )
    source = sp.diag(N, N, 1, 1 / H)
    alpha_scales = (1 / N, 1, 1 / N, 1 / N)
    beta_scales = (1 / N, 1 / N, 1, H)
    shift_image = (
        shifts[0],
        N * shifts[1],
        shifts[2] / N,
        shifts[3] / (H * N),
    )
    normalized_alpha, normalized_beta = rows()
    t_symbols = sp.symbols("t0:4")
    substitution = {sp.Symbol("A"): A0 / N, sp.Symbol("R"): R}
    expected_canonical_alpha = tuple(
        tuple(
            sp.sympify(entry)
            .subs(substitution)
            .subs({
                t_symbols[index]: 0 for index in range(4)
            })
            for entry in row
        )
        for row in normalized_alpha
    )
    expected_beta = tuple(
        tuple(
            sp.sympify(normalized_beta[mode][coordinate])
            .subs(substitution)
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    for mode in range(4):
        transformed_alpha = (
            alpha_scales[mode]
            * sp.Matrix([original_alpha[mode]])
            * source
        )
        assert all(
            zero(
                transformed_alpha[coordinate]
                - expected_canonical_alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        transformed_marked = (
            alpha_scales[mode]
            * (
                sp.Matrix([original_alpha[mode]])
                + shifts[mode] * sp.Matrix([original_beta[mode]])
            )
            * source
        )
        assert all(
            zero(
                transformed_marked[coordinate]
                - expected_canonical_alpha[mode][coordinate]
                - shift_image[mode] * expected_beta[mode][coordinate]
            )
            for coordinate in range(4)
        )
    assert (
        sp.factor(sp.prod(shift_image) / sp.prod(shifts))
        == 1 / (H * N)
    )


@dataclass(frozen=True)
class Stratum:
    distinguished: int
    name: str
    substitutions: tuple[tuple[sp.Symbol, sp.Expr], ...]
    mode: int
    rows: tuple[int, int, int, int]
    diagonal: str
    factor: sp.Expr
    pure_witness: sp.Expr
    nonzero: tuple[sp.Expr, ...]


def certificate_strata() -> tuple[Stratum, ...]:
    A, R = sp.symbols("A R")
    t0, t1, t2, t3 = sp.symbols("t0:4")

    def item(
        distinguished: int,
        name: str,
        substitutions: dict[sp.Symbol, sp.Expr],
        mode: int,
        row_indices: tuple[int, int, int, int],
        diagonal: str,
        factor: sp.Expr,
        pure_witness: sp.Expr = sp.Integer(1),
        nonzero: tuple[sp.Expr, ...] = (),
    ) -> Stratum:
        return Stratum(
            distinguished,
            name,
            tuple(substitutions.items()),
            mode,
            row_indices,
            diagonal,
            factor,
            pure_witness,
            nonzero,
        )

    return (
        item(
            0,
            "R0_t1_axis",
            {R: 0, t0: 0, t2: 0, t3: 0},
            2,
            (0, 2, 3, 7),
            "a",
            1,
            nonzero=(A, t1, A - 1),
        ),
        item(
            0,
            "R0_t0_axis",
            {R: 0, t1: 0, t2: 0, t3: 0},
            2,
            (0, 3, 6, 7),
            "b",
            -1,
            nonzero=(A,),
        ),
        item(
            0,
            "R_nonzero_A_nonone",
            {
                t0: 0,
                t1: (1 - A) / R,
                t2: 0,
                t3: 0,
            },
            2,
            (0, 2, 3, 7),
            "a",
            1,
            nonzero=(A, R, A - 1),
        ),
        item(
            0,
            "A1_axis_generic",
            {A: 1, t1: 0, t2: 0, t3: 0},
            2,
            (0, 2, 6, 7),
            "a",
            -2 * R,
            nonzero=(R, R * t0 + 1),
        ),
        item(
            0,
            "A1_axis_exception",
            {A: 1, t0: -1 / R, t1: 0, t2: 0, t3: 0},
            0,
            (0, 4, 5, 7),
            "b",
            R,
            nonzero=(R,),
        ),
        item(
            1,
            "A1",
            {A: 1, t0: 0, t1: 0, t2: 0, t3: 0},
            0,
            (0, 3, 5, 7),
            "b",
            -1 / R,
            pure_witness=R,
            nonzero=(R,),
        ),
        item(
            1,
            "Aminus1",
            {A: -1, t0: -1 / R, t1: 0, t2: 0, t3: 0},
            0,
            (0, 4, 5, 7),
            "b",
            R,
            pure_witness=R,
            nonzero=(R,),
        ),
        item(
            2,
            "t0_zero",
            {t0: 0, t1: 0, t2: 0, t3: 0},
            2,
            (0, 2, 3, 7),
            "a",
            1,
            nonzero=(A, R),
        ),
        item(
            2,
            "R0_axis",
            {R: 0, t1: 0, t2: 0, t3: 0},
            2,
            (0, 3, 6, 7),
            "b",
            1,
            nonzero=(A,),
        ),
        item(
            2,
            "A1_axis_generic",
            {A: 1, t1: 0, t2: 0, t3: 0},
            2,
            (0, 2, 6, 7),
            "a",
            -2 * R,
            nonzero=(R, R * t0 - 1),
        ),
        item(
            2,
            "A1_axis_exception",
            {A: 1, t0: 1 / R, t1: 0, t2: 0, t3: 0},
            2,
            (0, 2, 6, 7),
            "a",
            -2 * R,
            nonzero=(R,),
        ),
        item(
            3,
            "t0_zero",
            {t0: 0, t1: 0, t2: 0, t3: 0},
            2,
            (0, 2, 3, 7),
            "a",
            -1,
            nonzero=(A,),
        ),
        item(
            3,
            "R0_axis",
            {R: 0, t1: 0, t2: 0, t3: 0},
            2,
            (0, 3, 6, 7),
            "b",
            1,
            nonzero=(A,),
        ),
        item(
            3,
            "Aminus1_axis_generic",
            {A: -1, t1: 0, t2: 0, t3: 0},
            0,
            (0, 4, 5, 7),
            "b",
            -R**2 * t0,
            nonzero=(R, t0, R * t0 + 1),
        ),
        item(
            3,
            "Aminus1_axis_exception",
            {A: -1, t0: -1 / R, t1: 0, t2: 0, t3: 0},
            0,
            (0, 4, 5, 7),
            "b",
            R,
            nonzero=(R,),
        ),
        item(
            3,
            "nonzero_t3",
            {t0: -1 / R, t1: 0, t2: 0, t3: A + 1},
            0,
            (0, 4, 5, 7),
            "b",
            R,
            nonzero=(A, R, A + 1),
        ),
    )


def assert_factor_nonzero(
    factor: sp.Expr,
    assumptions: tuple[sp.Expr, ...],
) -> None:
    numerator = sp.together(factor).as_numer_denom()[0]
    if not numerator.free_symbols:
        assert numerator != 0
        return
    inverses = sp.symbols(f"w0:{len(assumptions)}")
    variables = tuple(sorted(
        set().union(
            numerator.free_symbols,
            *(assumption.free_symbols for assumption in assumptions),
        ),
        key=str,
    )) + inverses
    equations = [numerator] + [
        inverse * assumption - 1
        for inverse, assumption in zip(
            inverses,
            assumptions,
            strict=True,
        )
    ]
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert any(poly.as_expr() == 1 for poly in basis.polys), (
        factor,
        assumptions,
        tuple(poly.as_expr() for poly in basis.polys),
    )


def check_factor_strata() -> int:
    alpha0, beta0 = rows()
    checked = 0
    for stratum in certificate_strata():
        substitutions = dict(stratum.substitutions)
        alpha = tuple(
            tuple(
                sp.factor(
                    sp.sympify(entry).subs(
                        substitutions,
                        simultaneous=True,
                    )
                )
                for entry in row
            )
            for row in alpha0
        )
        beta = tuple(
            tuple(
                sp.factor(
                    sp.sympify(entry).subs(
                        substitutions,
                        simultaneous=True,
                    )
                )
                for entry in row
            )
            for row in beta0
        )
        mixed, diagonal_a, diagonal_b = mixed_matrix(
            stratum.distinguished,
            alpha,
            beta,
        )
        basis = tuple(
            vector.applyfunc(sp.factor)
            for vector in mixed.nullspace()
        )
        assert basis
        coordinates = sp.symbols(f"u0:{len(basis)}")
        extension = sum(
            (
                coefficient * vector
                for coefficient, vector in zip(
                    coordinates,
                    basis,
                    strict=True,
                )
            ),
            sp.zeros(8, 1),
        )
        da = sp.factor((diagonal_a * extension)[0])
        db = sp.factor((diagonal_b * extension)[0])
        assert da != 0 and db != 0
        determinant = sp.factor(
            marked_extension(
                stratum.distinguished,
                extension,
                alpha,
                beta,
                stratum.mode,
            )[list(stratum.rows), :].det()
        )
        residual = sp.factor(sp.cancel(determinant / (da * db)))
        factor = sp.factor(
            sp.sympify(stratum.factor).subs(
                substitutions,
                simultaneous=True,
            )
        )
        expected = factor * (da if stratum.diagonal == "a" else db)
        assert zero(residual - expected), (
            stratum,
            residual,
            expected,
        )
        pure_column = one_marked_map(
            stratum.mode,
            alpha,
            beta,
        )[:, stratum.distinguished]
        witness = sp.factor(
            sp.sympify(stratum.pure_witness).subs(
                substitutions,
                simultaneous=True,
            )
        )
        assert any(zero(entry - witness) for entry in pure_column), (
            stratum,
            tuple(map(sp.factor, pure_column)),
            witness,
        )
        assumptions = tuple(
            sp.factor(
                sp.sympify(assumption).subs(
                    substitutions,
                    simultaneous=True,
                )
            )
            for assumption in stratum.nonzero
        )
        assert_factor_nonzero(factor * witness, assumptions)
        checked += 1
    return checked


def selected_program(distinguished: int) -> tuple[str, int]:
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
    product_count = 0
    for mode, row_indices in CERTIFICATES[distinguished]:
        determinant = sp.factor(
            marked_extension(
                distinguished,
                extension,
                alpha,
                beta,
                mode,
            )[list(row_indices), :].det()
        )
        assert determinant != 0
        pure_column = one_marked_map(mode, alpha, beta)[:, distinguished]
        products = tuple(
            entry * determinant
            for entry in pure_column
            if entry != 0
        )
        equations.extend(products)
        product_count += len(products)
    variables = x + y + (inverse_a, inverse_b, A, R) + t
    program = "\n".join((
        "ring B=0,(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        "ideal obstruction=" + ",".join(map(singular, equations)) + ";",
        "ideal basis=slimgb(obstruction);",
        f'"Q={distinguished}_SELECTED";',
        '"BASIS_SIZE"; size(basis);',
        "basis;",
        "quit;",
        "",
    ))
    return program, product_count


def main() -> None:
    started = time.monotonic()
    check_normalization()
    alpha, beta = rows()
    coefficients = tuple(
        permanent(tuple(
            beta[mode] if bits & (1 << (3 - mode)) else alpha[mode]
            for mode in range(4)
        ))
        for bits in range(16)
    )
    A = sp.Symbol("A")
    assert zero(coefficients[0] - 2 * A)
    assert all(zero(value) for value in coefficients[1:])

    projection_runs = 0
    for distinguished in range(4):
        projection = projection_basis(
            run_singular(singular_program(distinguished), timeout=90)
        )
        assert projection == EXPECTED_PROJECTION[distinguished], (
            distinguished,
            projection,
            EXPECTED_PROJECTION[distinguished],
        )
        projection_runs += 1
    factor_strata = check_factor_strata()
    assert factor_strata == 16

    report = {
        "verified": True,
        "field": "characteristic zero",
        "normalization": "H=N=1 with bijective shift action",
        "projection_unit_or_ledger_runs": projection_runs,
        "exact_factor_certificate_strata": factor_strata,
        "all_extension_residual_covers": True,
        "complete_chart_boundary_marked_fibre_excluded": True,
        "projective_first_plane_boundary_closed": False,
        "internal_E0_marked_fibre_closed": False,
        "additional_components_closed": False,
        "global": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "sha256": {
            THEOREM.name: sha256(THEOREM),
            PLANE.name: sha256(PLANE),
            CANONICAL.name: sha256(CANONICAL),
            GENERATOR.name: sha256(GENERATOR),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
