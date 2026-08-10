#!/usr/bin/env python3
"""Verify the complete marked fibre on the component-chart divisor."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from derive_p5_h31_chart_boundary_marked_fibre_elimination import (  # noqa: E402
    rows,
    singular,
    singular_program,
)
from krenn_gu.singular_runtime import (  # noqa: E402
    singular_command_with_timeout,
)
from krenn_gu.p5_marked_basis import (  # noqa: E402
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)


THEOREM = (
    HERE / "P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md"
)
PLANE = REPO_ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
CANONICAL = (
    REPO_ROOT
    / "claims/p5/h31/component-chart-boundary/P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md"
)
GENERATOR = (
    HERE / "derive_p5_h31_chart_boundary_marked_fibre_elimination.py"
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
class CertificateRecord:
    distinguished: int
    name: str
    substitutions: tuple[tuple[sp.Symbol, sp.Expr], ...]
    mode: int
    rows: tuple[int, int, int, int]
    diagonal: str
    factor: sp.Expr
    pure_witness: sp.Expr
    nonzero: tuple[sp.Expr, ...]


def certificate_records() -> tuple[CertificateRecord, ...]:
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
    ) -> CertificateRecord:
        return CertificateRecord(
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
            # Assign the t0=0 intersection to the preceding t0_zero
            # record, so the sixteen records form a disjoint locally
            # closed cover rather than an overlapping cover.
            nonzero=(R, t0, R * t0 - 1),
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
            # Assign the R=0 intersection to the following R0_axis
            # record, making the locally closed record cover disjoint.
            nonzero=(A, R),
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


def check_factor_records() -> int:
    alpha0, beta0 = rows()
    checked = 0
    for record in certificate_records():
        substitutions = dict(record.substitutions)
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
            record.distinguished,
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
                record.distinguished,
                extension,
                alpha,
                beta,
                record.mode,
            )[list(record.rows), :].det()
        )
        residual = sp.factor(sp.cancel(determinant / (da * db)))
        factor = sp.factor(
            sp.sympify(record.factor).subs(
                substitutions,
                simultaneous=True,
            )
        )
        expected = factor * (da if record.diagonal == "a" else db)
        assert zero(residual - expected), (
            record,
            residual,
            expected,
        )
        pure_column = one_marked_map(
            record.mode,
            alpha,
            beta,
        )[:, record.distinguished]
        witness = sp.factor(
            sp.sympify(record.pure_witness).subs(
                substitutions,
                simultaneous=True,
            )
        )
        assert any(zero(entry - witness) for entry in pure_column), (
            record,
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
            for assumption in record.nonzero
        )
        assert_factor_nonzero(factor * witness, assumptions)
        checked += 1
    return checked


def projection_components() -> dict[int, tuple[tuple[sp.Expr, ...], ...]]:
    """Return the thirteen irreducible components of equation (9).

    These are projection-closure components.  Certificate records below
    further refine three components at rational-basis exceptional values;
    component, locally closed record, and exceptional basis are deliberately
    kept as different notions.
    """
    A, R = sp.symbols("A R")
    t0, t1, t2, t3 = sp.symbols("t0:4")
    return {
        0: (
            (R, t1, t2, t3),
            (A - 1, t1, t2, t3),
            (t0, t2, t3, R * t1 + A - 1),
            (R, t0, t2, t3),
        ),
        1: (
            (A + 1, R * t0 + 1, t1, t2, t3),
            (A - 1, t0, t1, t2, t3),
        ),
        2: (
            (t0, t1, t2, t3),
            (R, t1, t2, t3),
            (A - 1, t1, t2, t3),
        ),
        3: (
            (R * t0 + 1, t3 - A - 1, t1, t2),
            (t0, t3, t1, t2),
            (R, t3, t1, t2),
            (A + 1, t3, t1, t2),
        ),
    }


# The thirteen generic records are in bijection with the thirteen
# projection components.  The remaining three records replace a rational
# kernel basis at an exceptional value on the named component.
RECORD_COMPONENT = {
    (0, "R0_t1_axis"): (0, 3),
    (0, "R0_t0_axis"): (0, 0),
    (0, "R_nonzero_A_nonone"): (0, 2),
    (0, "A1_axis_generic"): (0, 1),
    (0, "A1_axis_exception"): (0, 1),
    (1, "A1"): (1, 1),
    (1, "Aminus1"): (1, 0),
    (2, "t0_zero"): (2, 0),
    (2, "R0_axis"): (2, 1),
    (2, "A1_axis_generic"): (2, 2),
    (2, "A1_axis_exception"): (2, 2),
    (3, "t0_zero"): (3, 1),
    (3, "R0_axis"): (3, 2),
    (3, "Aminus1_axis_generic"): (3, 3),
    (3, "Aminus1_axis_exception"): (3, 3),
    (3, "nonzero_t3"): (3, 0),
}
EXCEPTIONAL_BASIS_RECORDS = {
    (0, "A1_axis_exception"),
    (2, "A1_axis_exception"),
    (3, "Aminus1_axis_exception"),
}


def _ideal_intersection(
    left: tuple[sp.Expr, ...],
    right: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
) -> tuple[sp.Expr, ...]:
    auxiliary = sp.Dummy("intersection")
    basis = sp.groebner(
        [auxiliary * expression for expression in left]
        + [(1 - auxiliary) * expression for expression in right],
        auxiliary,
        *variables,
        order="lex",
    )
    return tuple(
        polynomial.as_expr()
        for polynomial in basis.polys
        if not polynomial.as_expr().has(auxiliary)
    )


def _ideals_equal(
    left: tuple[sp.Expr, ...],
    right: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
) -> bool:
    left_basis = sp.groebner(left, *variables, order="grevlex")
    right_basis = sp.groebner(right, *variables, order="grevlex")
    return (
        all(left_basis.reduce(expression)[1] == 0 for expression in right)
        and all(
            right_basis.reduce(expression)[1] == 0
            for expression in left
        )
    )


def check_projection_reconciliation() -> dict[str, int]:
    """Check the component/record reconciliation and closure artifacts.

    Mechanical exhaustiveness is supplied separately by the four selected
    saturated unit-ideal computations.  This bounded check verifies the
    thirteen-component decomposition, every record's assigned component,
    the record census/refinements, and the two closure-only identities.
    """
    A, R = sp.symbols("A R")
    t0, t1, t2, t3 = sp.symbols("t0:4")
    variables = (A, R, t0, t1, t2, t3)
    expected = {
        0: (
            t3,
            t2,
            t0 * t1,
            R * (R * t1 + A - 1),
            R * t0 * (A - 1),
        ),
        1: (
            t3,
            t2,
            t1,
            2 * R * t0 - A + 1,
            (A + 1) * t0,
            A**2 - 1,
        ),
        2: (t3, t2, t1, R * t0 * (A - 1)),
        3: (
            t2,
            t1,
            t3 * (A - t3 + 1),
            t3 * (R * t0 + 1),
            R * t0 * (A + 1) + t3,
        ),
    }
    components = projection_components()
    for distinguished, component_ideals in components.items():
        intersection = component_ideals[0]
        for component in component_ideals[1:]:
            intersection = _ideal_intersection(
                intersection,
                component,
                variables,
            )
        assert _ideals_equal(
            intersection,
            expected[distinguished],
            variables,
        ), (distinguished, intersection, expected[distinguished])

    records = certificate_records()
    record_keys = {(record.distinguished, record.name) for record in records}
    assert record_keys == set(RECORD_COMPONENT)
    assert sum(len(items) for items in components.values()) == 13
    assert len(records) == 16
    assert len(EXCEPTIONAL_BASIS_RECORDS) == 3
    generic_records = record_keys - EXCEPTIONAL_BASIS_RECORDS
    assert len(generic_records) == 13
    assert {
        RECORD_COMPONENT[key] for key in generic_records
    } == {
        (distinguished, index)
        for distinguished, items in components.items()
        for index in range(len(items))
    }

    by_key = {
        (record.distinguished, record.name): record
        for record in records
    }
    for key, record in by_key.items():
        component_q, component_index = RECORD_COMPONENT[key]
        assert component_q == record.distinguished
        substitutions = dict(record.substitutions)
        assert all(
            zero(
                expression.subs(
                    substitutions,
                    simultaneous=True,
                )
            )
            for expression in components[component_q][component_index]
        ), (key, components[component_q][component_index])
    # These two nonzero refinements assign the only overlapping loci to a
    # single record and make the sixteen-piece locally closed cover disjoint.
    assert t0 in by_key[(2, "A1_axis_generic")].nonzero
    assert R in by_key[(3, "t0_zero")].nonzero

    # Equation (9) has two closure-only loci not owned by a certificate
    # record.  Exact row identities show that neither meets the saturated
    # binary incidence d_a*d_b != 0.
    alpha, beta = rows()
    mixed0, _diagonal_a0, diagonal_b0 = mixed_matrix(0, alpha, beta)
    q0 = {A: 1, R: 0, t0: 0, t2: 0, t3: 0}
    q0_identity = (
        t1 * diagonal_b0
        + mixed0[0, :]
        - t1 * mixed0[4, :]
        - mixed0[10, :]
    ).subs(q0, simultaneous=True)
    assert all(zero(entry) for entry in q0_identity)

    _mixed1, _diagonal_a1, diagonal_b1 = mixed_matrix(1, alpha, beta)
    q1 = {A: 1, R: 0, t0: 0, t1: 0, t2: 0, t3: 0}
    assert all(
        zero(entry.subs(q1, simultaneous=True))
        for entry in diagonal_b1
    )
    return {
        "irreducible_projection_components": 13,
        "generic_rational_basis_records": 13,
        "exceptional_basis_records": 3,
        "locally_closed_certificate_records": 16,
        "projection_closure_artifact_loci": 2,
    }


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


def check_selected_unit_ideals(timeout: float) -> tuple[dict[str, object], ...]:
    """Run the four exact characteristic-zero saturated cover checks.

    These comparatively expensive computations are the direct mechanical
    exhaustiveness check.  They run by default; the bounded local-check mode
    must opt out explicitly and reports that exhaustiveness was not confirmed.
    """
    results: list[dict[str, object]] = []
    for distinguished in range(4):
        program, product_count = selected_program(distinguished)
        output = run_singular(program, timeout=timeout)
        lines = tuple(
            line.strip()
            for line in output.splitlines()
            if line.strip()
        )
        assert f"Q={distinguished}_SELECTED" in lines, lines
        marker = lines.index("BASIS_SIZE")
        assert lines[marker + 1] == "1", lines
        assert "basis[1]=1" in lines, lines
        results.append({
            "distinguished": distinguished,
            "unit_ideal": True,
            "product_count": product_count,
            "program_bytes": len(program.encode("utf-8")),
            "program_sha256": hashlib.sha256(
                program.encode("utf-8")
            ).hexdigest(),
            "stdout_sha256": hashlib.sha256(
                output.encode("utf-8")
            ).hexdigest(),
        })
    return tuple(results)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the characteristic-zero H31 chart-boundary marked-fibre "
            "cover and its sixteen exact factor-certificate records."
        )
    )
    parser.add_argument(
        "--selected-unit-ideals",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "run the four expensive saturated unit-ideal computations "
            "generated by selected_program() (default: enabled; use "
            "--no-selected-unit-ideals for the bounded local replay only)"
        ),
    )
    parser.add_argument(
        "--selected-timeout",
        type=float,
        default=900.0,
        help="per-Singular-run timeout in seconds (default: 900)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
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
    reconciliation = check_projection_reconciliation()
    factor_records = check_factor_records()
    assert factor_records == 16
    selected_runs = (
        check_selected_unit_ideals(args.selected_timeout)
        if args.selected_unit_ideals
        else ()
    )

    report = {
        "bounded_obstruction_replay_passed": True,
        "field": "characteristic zero",
        "normalization": "H=N=1 with bijective shift action",
        "projection_elimination_runs": projection_runs,
        **reconciliation,
        "exact_factor_certificate_records": factor_records,
        "component_record_reconciliation_checked": True,
        "selected_saturation_unit_ideal_runs": {
            "requested": args.selected_unit_ideals,
            "completed": len(selected_runs),
            "records": selected_runs,
        },
        "selected_saturation_exhaustiveness_confirmed": (
            len(selected_runs) == 4
        ),
        "exact_factor_record_checks_passed": factor_records == 16,
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
