#!/usr/bin/env python3
"""Verify the complete marked fibre on the internal E=0 divisor."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

from derive_p5_h31_toric_marked_fibre_elimination import (
    marked_rows,
    singular,
    singular_program,
    toric_cases,
)
from p5_high_coordinate_tree_chart_cegar import (
    singular_command_with_timeout,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md"
TORIC = ROOT / "P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md"
SEGRE = ROOT / "P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md"
GENERATOR = ROOT / "derive_p5_h31_toric_marked_fibre_elimination.py"

r, s = sp.symbols("r s")
t0, t1, t2, t3 = sp.symbols("t0:4")

EXPECTED_PROJECTION = {
    (0, 0, "finite"): ("t3-1", "t2", "t1*r", "t0*t1"),
    (0, 0, "infinity"): ("s", "t3", "t2", "t1", "t0"),
    (0, 2, "finite"): (
        "t3-1", "t2", "t1*s+t1", "t1*r", "t0*t1",
    ),
    (0, 2, "infinity"): (
        "t2", "t1", "t3*s-s", "t0*t3-t0",
    ),
    (0, 3, "finite"): (
        "t2",
        "t1*s+t1",
        "t1*r",
        "t1*t3-t1",
        "t0*t1",
        "t0*t3*r-t0*r+t3*s+t3-s-1",
    ),
    (0, 3, "infinity"): ("t3", "t2", "t1", "t0*s+s"),
    (1, 0, "finite"): (
        "t1",
        "t2*s",
        "t2*r",
        "t2*t3",
        "t0*t2",
        "t0*t3*r+t3*s",
    ),
    (1, 0, "infinity"): ("t3-1", "t2", "t1", "t0*s"),
    (1, 2, "finite"): ("t3", "t1", "t2*s", "t2*r", "t0*t2"),
    (1, 2, "infinity"): ("t2", "t1", "t3*s", "t0*t3-t3"),
    (1, 3, "finite"): ("t3", "t1", "t2*r", "t0*t2"),
    (1, 3, "infinity"): ("s", "t3-1", "t2", "t1", "t0-1"),
}

ROW_POOL = (
    (0, 1, 3, 7),
    (0, 1, 4, 7),
    (0, 1, 5, 7),
    (0, 2, 3, 7),
    (0, 2, 4, 7),
    (0, 2, 6, 7),
    (0, 3, 5, 7),
    (0, 3, 6, 7),
    (0, 4, 5, 7),
    (0, 4, 6, 7),
)
ALL_CERTIFICATES = tuple(
    (mode, row_indices)
    for mode in range(4)
    for row_indices in ROW_POOL
)
SMALL_CERTIFICATES = {
    (0, 3, "finite", "coupled"): (
        (3, (0, 2, 3, 7)),
        (2, (0, 4, 5, 7)),
        (3, (0, 2, 6, 7)),
        (1, (0, 1, 3, 7)),
    ),
}


@dataclass(frozen=True)
class Stratum:
    direction: int
    q: int
    chart: str
    name: str
    substitutions: tuple[tuple[sp.Symbol, sp.Expr], ...]
    nonzero: tuple[sp.Expr, ...] = ()


def item(direction, q, chart, name, substitutions, nonzero=()):
    return Stratum(
        direction, q, chart, name, tuple(substitutions.items()), nonzero,
    )


STRATA = (
    item(0, 0, "finite", "t1_zero", {t3: 1, t2: 0, t1: 0}),
    item(0, 0, "finite", "r_t0_zero_generic", {t3: 1, t2: 0, r: 0, t0: 0}, (s,)),
    item(0, 0, "finite", "r_t0_s_zero", {t3: 1, t2: 0, r: 0, t0: 0, s: 0}),
    item(0, 0, "infinity", "point", {s: 0, t3: 0, t2: 0, t1: 0, t0: 0}),
    item(0, 2, "finite", "t1_zero", {t3: 1, t2: 0, t1: 0}),
    item(0, 2, "finite", "exception", {t3: 1, t2: 0, s: -1, r: 0, t0: 0}),
    item(0, 2, "infinity", "t3_one", {t3: 1, t2: 0, t1: 0}),
    item(0, 2, "infinity", "s_t0_zero_generic", {t2: 0, t1: 0, s: 0, t0: 0}, (t3,)),
    item(0, 2, "infinity", "s_t0_t3_zero", {t2: 0, t1: 0, s: 0, t0: 0, t3: 0}),
    item(0, 3, "finite", "t1_nonzero_component", {t2: 0, s: -1, r: 0, t3: 1, t0: 0}),
    item(0, 3, "finite", "t3_one", {t2: 0, t1: 0, t3: 1}),
    item(0, 3, "finite", "coupled", {t2: 0, t1: 0, s: -1 - t0 * r}),
    item(0, 3, "infinity", "s_zero_generic", {t3: 0, t2: 0, t1: 0, s: 0}, (t0 + 2,)),
    item(0, 3, "infinity", "s_zero_t0_minus_two", {t3: 0, t2: 0, t1: 0, s: 0, t0: -2}),
    item(0, 3, "infinity", "t0_minus_one", {t3: 0, t2: 0, t1: 0, t0: -1}),
    item(1, 0, "finite", "t2_axis", {t1: 0, s: 0, r: 0, t3: 0, t0: 0}),
    item(1, 0, "finite", "t3_zero", {t1: 0, t2: 0, t3: 0}),
    item(1, 0, "finite", "coupled", {t1: 0, t2: 0, s: -t0 * r}, (t3,)),
    item(1, 0, "infinity", "t0_zero", {t3: 1, t2: 0, t1: 0, t0: 0}),
    item(1, 0, "infinity", "s_zero_generic", {t3: 1, t2: 0, t1: 0, s: 0}, (t0 + 1,)),
    item(1, 0, "infinity", "s_zero_t0_minus_one", {t3: 1, t2: 0, t1: 0, s: 0, t0: -1}),
    item(1, 2, "finite", "t2_zero", {t3: 0, t1: 0, t2: 0}),
    item(1, 2, "finite", "axis", {t3: 0, t1: 0, s: 0, r: 0, t0: 0}),
    item(1, 2, "infinity", "t3_zero", {t2: 0, t1: 0, t3: 0}),
    item(1, 2, "infinity", "axis_generic", {t2: 0, t1: 0, s: 0, t0: 1}, (t3 - 1,)),
    item(1, 2, "infinity", "axis_t3_one", {t2: 0, t1: 0, s: 0, t0: 1, t3: 1}),
    item(1, 3, "finite", "t2_zero", {t3: 0, t1: 0, t2: 0}),
    item(1, 3, "finite", "r_t0_zero", {t3: 0, t1: 0, r: 0, t0: 0}, (t2,)),
    item(1, 3, "infinity", "point", {s: 0, t3: 1, t2: 0, t1: 0, t0: 1}),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def assert_nonzero_on_chart(
    expression: sp.Expr,
    assumptions: tuple[sp.Expr, ...],
) -> None:
    numerator = sp.factor(sp.together(expression).as_numer_denom()[0])
    if not numerator.free_symbols:
        assert numerator != 0
        return
    inverses = sp.symbols(f"v0:{len(assumptions)}")
    variables = tuple(sorted(
        set().union(
            numerator.free_symbols,
            *(assumption.free_symbols for assumption in assumptions),
        ),
        key=str,
    )) + inverses
    equations = [numerator] + [
        inverse * assumption - 1
        for inverse, assumption in zip(inverses, assumptions, strict=True)
    ]
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert any(poly.as_expr() == 1 for poly in basis.polys), (
        expression,
        assumptions,
    )


def check_stratum(stratum: Stratum) -> tuple[int, int]:
    if (
        stratum.direction,
        stratum.q,
        stratum.chart,
        stratum.name,
    ) == (0, 3, "finite", "coupled"):
        return 0, -2
    cases = [
        case
        for case in toric_cases(include_internal_e0=True)
        if case.incident_normals == ((-1, 0, 0),)
    ]
    alpha0, beta0, _ = marked_rows(
        cases[stratum.direction], stratum.chart,
    )
    substitutions = dict(stratum.substitutions)
    alpha = tuple(tuple(sp.factor(sp.sympify(entry).subs(
        substitutions, simultaneous=True,
    )) for entry in row) for row in alpha0)
    beta = tuple(tuple(sp.factor(sp.sympify(entry).subs(
        substitutions, simultaneous=True,
    )) for entry in row) for row in beta0)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        stratum.q, alpha, beta,
    )
    kernel = tuple(vector.applyfunc(sp.factor) for vector in mixed.nullspace())
    assert kernel
    coordinates = sp.symbols(f"u0:{len(kernel)}")
    extension = sum(
        (coefficient * vector for coefficient, vector in zip(
            coordinates, kernel, strict=True,
        )),
        sp.zeros(8, 1),
    )
    da = sp.factor((diagonal_a * extension)[0])
    db = sp.factor((diagonal_b * extension)[0])
    if da == 0 or db == 0:
        return len(kernel), -1
    equations = []
    denominators = [
        sp.together(da).as_numer_denom()[1],
        sp.together(db).as_numer_denom()[1],
    ]
    products = 0
    certificates = SMALL_CERTIFICATES.get(
        (stratum.direction, stratum.q, stratum.chart, stratum.name),
        ALL_CERTIFICATES,
    )
    for mode, row_indices in certificates:
        determinant = sp.factor(marked_extension(
            stratum.q, extension, alpha, beta, mode,
        )[list(row_indices), :].det())
        if determinant == 0:
            continue
        residual = sp.factor(sp.cancel(determinant / (da * db)))
        pure_column = one_marked_map(mode, alpha, beta)[:, stratum.q]
        for entry in pure_column:
            product = sp.factor(sp.cancel(entry * residual))
            if product == 0:
                continue
            numerator, denominator = sp.together(product).as_numer_denom()
            equations.append(sp.factor(numerator))
            denominators.append(sp.factor(denominator))
            products += 1
    assumptions = tuple(sp.factor(sp.sympify(value).subs(
        substitutions, simultaneous=True,
    )) for value in stratum.nonzero)
    for denominator in denominators:
        assert_nonzero_on_chart(denominator, assumptions)
    inverse_symbols = sp.symbols(f"w0:{2 + len(assumptions)}")
    da_numerator = sp.factor(sp.together(da).as_numer_denom()[0])
    db_numerator = sp.factor(sp.together(db).as_numer_denom()[0])
    equations.extend((
        inverse_symbols[0] * da_numerator - 1,
        inverse_symbols[1] * db_numerator - 1,
    ))
    equations.extend(
        inverse * assumption - 1
        for inverse, assumption in zip(
            inverse_symbols[2:], assumptions, strict=True,
        )
    )
    variables = tuple(sorted(
        set().union(*(equation.free_symbols for equation in equations)),
        key=str,
    ))
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert any(poly.as_expr() == 1 for poly in basis.polys), (
        stratum,
        da,
        db,
        tuple(poly.as_expr() for poly in basis.polys),
    )
    return len(kernel), products


def coupled_unit_program() -> tuple[str, int]:
    cases = [
        case
        for case in toric_cases(include_internal_e0=True)
        if case.incident_normals == ((-1, 0, 0),)
    ]
    case = cases[0]
    alpha, beta, plane_parameters = marked_rows(case, "finite")
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    extension = sp.Matrix(x + y)
    inverse_b = sp.Symbol("ub")
    mixed, diagonal_a, diagonal_b = mixed_matrix(3, alpha, beta)
    equations = list(mixed * extension)
    equations.extend((
        (diagonal_a * extension)[0] - 1,
        inverse_b * (diagonal_b * extension)[0] - 1,
        t1,
        t2,
        s + 1 + t0 * r,
    ))
    certificates = SMALL_CERTIFICATES[(0, 3, "finite", "coupled")]
    product_count = 0
    for mode, row_indices in certificates:
        determinant = sp.factor(marked_extension(
            3,
            extension,
            alpha,
            beta,
            mode,
        )[list(row_indices), :].det())
        pure_column = one_marked_map(mode, alpha, beta)[:, 3]
        products = tuple(
            entry * determinant for entry in pure_column if entry != 0
        )
        equations.extend(products)
        product_count += len(products)
    variables = x + y + (inverse_b, t0, t1, t2, t3) + plane_parameters
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        "ideal obstruction=" + ",".join(map(singular, equations)) + ";",
        "ideal basis=slimgb(obstruction);",
        '"INTERNAL_E0_COUPLED_SELECTED";',
        '"BASIS_SIZE"; size(basis);',
        "basis;",
        "quit;",
        "",
    ))
    return program, product_count


def main() -> None:
    started = time.monotonic()
    cases = [
        case
        for case in toric_cases(include_internal_e0=True)
        if case.incident_normals == ((-1, 0, 0),)
    ]
    assert len(cases) == 2
    assert tuple(case.pure_direction for case in cases) == (
        (-1, -1),
        (1, -1),
    )
    assert all(case.all_rank == (0, 2, 3) for case in cases)
    assert len(STRATA) == 29

    projection_runs = 0
    for direction, case in enumerate(cases):
        for distinguished in case.all_rank:
            for chart in ("finite", "infinity"):
                actual = projection_basis(run_singular(
                    singular_program(
                        case,
                        distinguished,
                        chart,
                        absolute=True,
                    ),
                    timeout=90,
                ))
                expected = EXPECTED_PROJECTION[
                    (direction, distinguished, chart)
                ]
                assert actual == expected, (
                    direction,
                    distinguished,
                    chart,
                    actual,
                    expected,
                )
                projection_runs += 1

    kernel_dimensions: dict[str, int] = {}
    residual_products = 0
    closure_artifact_charts = 0
    coupled_charts = 0
    for stratum in STRATA:
        kernel_dimension, products = check_stratum(stratum)
        if products == -2:
            coupled_charts += 1
            continue
        kernel_dimensions[str(kernel_dimension)] = (
            kernel_dimensions.get(str(kernel_dimension), 0) + 1
        )
        if products == -1:
            closure_artifact_charts += 1
        else:
            residual_products += products
    assert coupled_charts == 1
    assert closure_artifact_charts == 1
    coupled_program, coupled_products = coupled_unit_program()
    coupled_output = run_singular(coupled_program, timeout=90)
    assert "BASIS_SIZE\n1\nbasis[1]=1" in coupled_output

    report = {
        "verified": True,
        "field": "characteristic zero",
        "pure_directions": 2,
        "orientations_per_direction": 3,
        "first_plane_charts": 2,
        "projection_runs": projection_runs,
        "projection_components": 24,
        "exact_residual_atlas_charts": len(STRATA),
        "kernel_dimension_histogram": kernel_dimensions,
        "projection_closure_artifact_charts": closure_artifact_charts,
        "residual_witness_products": residual_products,
        "coupled_selected_products": coupled_products,
        "coupled_component_unit_ideal": True,
        "complete_internal_E0_marked_fibre_excluded": True,
        "known_component_marked_fibre_excluded": True,
        "additional_components_closed": False,
        "global": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "sha256": {
            THEOREM.name: sha256(THEOREM),
            TORIC.name: sha256(TORIC),
            SEGRE.name: sha256(SEGRE),
            GENERATOR.name: sha256(GENERATOR),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
