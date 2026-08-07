#!/usr/bin/env python3
"""Verify the complete marked fibre on first-plane infinity."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

from derive_p5_h31_fibre_infinity_marked_fibre_elimination import (
    rows,
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
    ROOT / "P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md"
)
CANONICAL = ROOT / "P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md"
PLANE = ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
GENERATOR = (
    ROOT / "derive_p5_h31_fibre_infinity_marked_fibre_elimination.py"
)

A, D, E = sp.symbols("A D E")
t0, t1, t2, t3 = sp.symbols("t0:4")

EXPECTED_PROJECTION = {
    0: (
        "E-t2",
        "t3^2-t3",
        "t1*t3",
        "A*t3",
        "t0*t1",
        "t0*t2*t3-t0*t2",
        "D*t0*t3+t3",
        "t1*t2^2+t2*t3-t2",
        "A*t2^2+D*t2*t3-D*t2",
        "D*t1*t2-A*t2",
        "A*t1*t2-D*t1",
        "D*t0*t2+t2*t3",
        "A*t0*t2",
        "D^2*t1-A^2*t2",
    ),
    1: (
        "t3",
        "t0*t2",
        "E*t2-t2^2",
        "2*E*t1-t1*t2-1",
        "t1*t2^2-t2",
        "A*t2^2-D*t2",
        "D*t1*t2-A*t2",
        "A^2*t2-A*D",
        "4*D*t0*t1-4*t1^2*t2-A*t0+4*t1",
        "A*E*t0-2*D*t0+2*t1*t2-2",
        "D^2*t0-A*t2+D",
        "A*D*t0",
        "A*D*E-A*D*t2",
        "4*A*t1^2*t2+A^2*t0-4*A*t1",
        "A*D^2*t1-A^2*D",
        "A^2*t0^2-4*A*t0*t1",
        "A^3*t0+4*A*D*t1^2-4*A^2*t1",
    ),
    2: (
        "t1*t3",
        "E*t3-t2*t3",
        "A*t3",
        "t0*t1",
        "E*t0-t0*t2",
        "D*t0*t3+t3",
        "A*t1*t2+D*t1",
        "A*t0*t2^2",
        "D*E^2*t1-A*E*t2-D*E+D*t2",
        "A^2*E*t2^2+2*A*D*E*t2-A*D*t2^2+D^2*E-D^2*t2",
        "E^2*t1^2*t2+t1*t2^2",
    ),
    3: (
        "t0*t1",
        "E*t0-t0*t2",
        "t2*t3^2-t2*t3",
        "t1*t3^2",
        "t1*t2*t3",
        "t0*t2*t3-t0*t2",
        "t1^2*t3",
        "E*t1*t3",
        "D*t1*t3",
        "A*t0*t3-t1*t3",
        "E*t1*t2+t2*t3-t2",
        "A*t1*t2+D*t1",
        "A*t0*t2",
        "D*E*t1-A*t2*t3+A*t2",
        "t0*t3^3-t0*t3^2",
        "t0^2*t3^2-t0^2*t3",
        "D*t0*t3^2-D*t0*t3",
        "D*E*t3^2-D*E*t3",
        "A*t2^2*t3-A*t2^2+D*t2*t3-D*t2",
        "A*E*t2*t3+D*E*t3-D*t2*t3",
        "A*E*t2^2-D*t2^2*t3+D*E*t2",
    ),
}

EXPECTED_COMPONENTS = {
    0: (
        ("D*t0+1", "t3-1", "t1", "E-t2", "A"),
        ("t3", "t2", "t1", "E-t2"),
        ("t1*t2-1", "t3", "t0", "E-t2", "-D*t1+A"),
        ("t3", "t2", "t0", "E-t2", "D"),
    ),
    1: (
        ("2*E*t1-1", "A*t0-4*t1", "t3", "t2", "D"),
        ("2*E*t1-1", "D*t0+1", "t3", "t2", "A"),
        ("t1*t2-1", "t3", "t0", "E-t2", "-D*t1+A"),
    ),
    2: (
        ("t3", "t2", "t1", "E"),
        ("t3", "t1", "E-t2", "A"),
        ("A*E*t2+D*E-D*t2", "t3", "t1", "t0"),
        ("E^2*t1+t2", "A*t2+D", "t3", "t0"),
        ("t3", "t2", "t0", "D"),
        ("D*t0+1", "t1", "E-t2", "A"),
    ),
    3: (
        ("t3-1", "t1", "E-t2", "A"),
        ("t3", "t2", "t1", "E"),
        ("t2", "t1", "t0", "E"),
        ("A*E*t2+D*E-D*t2", "t3-1", "t1", "t0"),
        ("t3", "t2", "t1", "t0"),
        ("t2", "t1", "t0", "D"),
        ("E*t1-1", "A*t2+D", "t3", "t0"),
        ("t3", "t2", "t0", "D"),
    ),
}


@dataclass(frozen=True)
class Stratum:
    q: int
    component: int
    name: str
    substitutions: tuple[tuple[sp.Symbol, sp.Expr], ...]
    certificates: tuple[tuple[int, tuple[int, int, int, int]], ...]
    nonzero: tuple[sp.Expr, ...] = ()


def item(
    q: int,
    component: int,
    name: str,
    substitutions: dict[sp.Symbol, sp.Expr],
    certificates: tuple[
        tuple[int, tuple[int, int, int, int]], ...
    ],
    nonzero: tuple[sp.Expr, ...] = (),
) -> Stratum:
    return Stratum(
        q,
        component,
        name,
        tuple(substitutions.items()),
        certificates,
        nonzero,
    )


STRATA = (
    item(0, 1, "A0_t3_1", {A: 0, E: t2, t3: 1, t1: 0, t0: -1 / D},
         ((1, (0, 1, 5, 7)),), (D,)),
    item(0, 2, "central", {E: 0, t1: 0, t2: 0, t3: 0},
         ((2, (0, 4, 6, 7)), (3, (0, 1, 3, 7)), (2, (0, 2, 3, 7)))),
    item(0, 3, "coupled", {t0: 0, t3: 0, E: t2, t1: 1 / t2, A: D / t2},
         ((0, (0, 1, 3, 7)),), (D, t2)),
    item(0, 4, "D0_t1_free", {D: 0, E: 0, t0: 0, t2: 0, t3: 0},
         ((2, (0, 2, 6, 7)),), (A,)),
    item(1, 1, "D0", {D: 0, t2: 0, t3: 0, t1: 1 / (2 * E), t0: 2 / (A * E)},
         ((0, (0, 1, 3, 7)),), (A, E)),
    item(1, 2, "A0", {A: 0, t2: 0, t3: 0, t1: 1 / (2 * E), t0: -1 / D},
         ((0, (0, 1, 3, 7)),), (D, E)),
    item(1, 3, "coupled", {t0: 0, t3: 0, E: t2, t1: 1 / t2, A: D / t2},
         ((0, (0, 1, 3, 7)),), (D, t2)),
    item(2, 1, "central", {E: 0, t1: 0, t2: 0, t3: 0},
         ((3, (0, 1, 5, 7)), (1, (0, 1, 5, 7)), (3, (0, 1, 4, 7)))),
    item(2, 2, "A0_plane", {A: 0, E: t2, t1: 0, t3: 0},
         ((1, (0, 4, 5, 7)),), (D,)),
    item(2, 3, "relation_generic",
         {D: A * E * t2 / (t2 - E), t0: 0, t1: 0, t3: 0},
         ((3, (0, 1, 3, 7)),), (A, t2 - E)),
    item(2, 4, "quadric_generic",
         {D: A * E**2 * t1, t2: -E**2 * t1, t0: 0, t3: 0},
         ((3, (0, 1, 3, 7)),), (A, E * t1 + 1)),
    item(2, 4, "quadric_Et1_minus_1",
         {t1: -1 / E, D: -A * E, t2: E, t0: 0, t3: 0},
         ((0, (0, 1, 3, 7)),), (A, E)),
    item(2, 5, "D0_plane", {D: 0, t0: 0, t2: 0, t3: 0},
         ((0, (0, 1, 5, 7)), (2, (0, 2, 6, 7))), (A,)),
    item(2, 6, "A0_t3_generic",
         {A: 0, E: t2, t1: 0, t0: -1 / D},
         ((1, (0, 1, 5, 7)),), (D, t3 + 1)),
    item(2, 6, "A0_t3_minus_1",
         {A: 0, E: t2, t1: 0, t0: -1 / D, t3: -1},
         ((1, (0, 1, 5, 7)),), (D,)),
    item(3, 1, "A0_t3_1_generic",
         {A: 0, E: t2, t3: 1, t1: 0},
         ((0, (0, 2, 6, 7)), (3, (0, 1, 3, 7))), (D, D * t0 + 1)),
    item(3, 1, "A0_t3_1_Dt0_minus_1",
         {A: 0, E: t2, t3: 1, t1: 0, t0: -1 / D},
         ((1, (0, 1, 5, 7)),), (D,)),
    item(3, 2, "central_t0", {E: 0, t1: 0, t2: 0, t3: 0},
         ((3, (0, 1, 5, 7)),)),
    item(3, 3, "central_t3_generic",
         {E: 0, t0: 0, t1: 0, t2: 0},
         ((3, (0, 1, 3, 7)),), (t3,)),
    item(3, 4, "relation_t3_1",
         {D: A * E * t2 / (t2 - E), t0: 0, t1: 0, t3: 1},
         ((3, (0, 1, 3, 7)),), (A, t2 - E)),
    item(3, 5, "origin_shifts", {t0: 0, t1: 0, t2: 0, t3: 0},
         ((3, (0, 1, 3, 7)),)),
    item(3, 6, "D0_t3_generic", {D: 0, t0: 0, t1: 0, t2: 0},
         ((3, (0, 1, 3, 7)),), (A, t3)),
    item(3, 7, "hyperbola_generic",
         {D: -A * t2, t1: 1 / E, t0: 0, t3: 0},
         ((3, (0, 1, 3, 7)),), (A, E, t2 - E)),
    item(3, 7, "hyperbola_t2_E",
         {D: -A * E, t2: E, t1: 1 / E, t0: 0, t3: 0},
         ((3, (0, 1, 3, 7)),), (A, E)),
    item(3, 8, "D0_t1_plane", {D: 0, t0: 0, t2: 0, t3: 0},
         ((3, (0, 1, 3, 7)),), (A,)),
)

COMPONENT_EQUATIONS = {
    q: tuple(
        tuple(
            sp.sympify(
                generator.replace("^", "**"),
                locals={"A": A, "D": D, "E": E,
                        "t0": t0, "t1": t1, "t2": t2, "t3": t3},
            )
            for generator in component
        )
        for component in components
    )
    for q, components in EXPECTED_COMPONENTS.items()
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_singular(program: str, timeout: float = 120) -> str:
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


def projection_and_components_program(distinguished: int) -> str:
    return singular_program(distinguished).replace(
        "quit;\n",
        "\n".join((
            'LIB "primdec.lib";',
            "list components=minAssGTZ(marking);",
            '"COMPONENT_COUNT"; size(components);',
            "components;",
            "quit;",
            "",
        )),
    )


def projection_basis(output: str) -> tuple[str, ...]:
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def component_bases(
    output: str,
) -> tuple[tuple[str, ...], ...]:
    components: list[list[str]] = []
    current: list[str] | None = None
    for line in output.splitlines():
        if re.fullmatch(r"\[\d+\]:", line):
            current = []
            components.append(current)
        elif current is not None and re.match(r"\s+_\[\d+\]=", line):
            current.append(line.split("=", 1)[1].replace(" ", ""))
    return tuple(tuple(component) for component in components)


def check_normalization() -> None:
    A0, D0, E0 = sp.symbols("A0 D0 E0")
    H, N = sp.symbols("H N", nonzero=True)
    shifts = sp.symbols("s0:4")
    original_alpha = (
        (0, 0, 1, H),
        (0, 0, 1, H),
        (0, 1, 0, H * N * E0),
        (1, 0, N, 0),
    )
    original_beta = (
        (-D0 / H, A0, 0, N * (D0 - A0 * E0 * H)),
        (E0, 1, -E0 * N, -E0 * H * N),
        (-1 / N, 0, 1, 0),
        (0, 0, -1 / H, 1),
    )
    source = sp.diag(N, N, 1, 1 / H)
    alpha_scales = (1, 1, 1 / N, 1 / N)
    beta_scales = (H / N, 1 / N, 1, H)
    shift_image = (
        N * shifts[0] / H,
        N * shifts[1],
        shifts[2] / N,
        shifts[3] / (H * N),
    )
    normalized_alpha, normalized_beta = rows()
    normalized_parameters = {A: A0 * H, D: D0, E: E0}
    t_symbols = sp.symbols("t0:4")
    expected_alpha = tuple(
        tuple(
            sp.sympify(entry)
            .subs(normalized_parameters)
            .subs({symbol: 0 for symbol in t_symbols})
            for entry in row
        )
        for row in normalized_alpha
    )
    expected_beta = tuple(
        tuple(
            sp.sympify(entry).subs(normalized_parameters)
            for entry in row
        )
        for row in normalized_beta
    )
    for mode in range(4):
        transformed_alpha = (
            alpha_scales[mode]
            * sp.Matrix([original_alpha[mode]])
            * source
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
                transformed_alpha[coordinate]
                - expected_alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        assert all(
            zero(
                transformed_marked[coordinate]
                - expected_alpha[mode][coordinate]
                - shift_image[mode] * expected_beta[mode][coordinate]
            )
            for coordinate in range(4)
        )
        assert beta_scales[mode] != 0
    assert zero(sp.prod(shift_image) / sp.prod(shifts) - 1 / H**2)


def check_pure_deletion() -> None:
    alpha, beta = rows()
    coefficients = tuple(
        permanent(tuple(
            beta[mode] if bits & (1 << (3 - mode)) else alpha[mode]
            for mode in range(4)
        ))
        for bits in range(16)
    )
    assert zero(coefficients[0] - 2)
    assert all(zero(coefficient) for coefficient in coefficients[1:])


def check_atlas() -> None:
    assert len(STRATA) == 25
    assert {(stratum.q, stratum.component) for stratum in STRATA} == {
        (q, component)
        for q, components in EXPECTED_COMPONENTS.items()
        for component in range(1, len(components) + 1)
    }
    for stratum in STRATA:
        substitutions = dict(stratum.substitutions)
        component = COMPONENT_EQUATIONS[stratum.q][
            stratum.component - 1
        ]
        assert all(
            zero(
                equation.subs(
                    substitutions,
                    simultaneous=True,
                )
            )
            for equation in component
        ), stratum

    relation = A * E * t2 + D * E - D * t2
    assert zero(relation.subs(E, t2) - A * t2**2)
    quadric = (E**2 * t1 + t2, A * t2 + D)
    assert all(
        zero(expression.subs({
            D: A * E**2 * t1,
            t2: -E**2 * t1,
        }, simultaneous=True))
        for expression in quadric
    )
    hyperbola = (E * t1 - 1, A * t2 + D)
    assert all(
        zero(expression.subs({
            D: -A * t2,
            t1: 1 / E,
        }, simultaneous=True))
        for expression in hyperbola
    )


def zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(expression)) == 0


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
        tuple(poly.as_expr() for poly in basis.polys),
    )


def check_stratum(stratum: Stratum) -> tuple[int, int]:
    substitutions = dict(stratum.substitutions)
    alpha0, beta0 = rows()
    alpha = tuple(tuple(sp.factor(sp.sympify(entry).subs(
        substitutions, simultaneous=True,
    )) for entry in row) for row in alpha0)
    beta = tuple(tuple(sp.factor(sp.sympify(entry).subs(
        substitutions, simultaneous=True,
    )) for entry in row) for row in beta0)
    mixed, diagonal_a, diagonal_b = mixed_matrix(stratum.q, alpha, beta)
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
    assert da != 0 and db != 0
    witness_equations: list[sp.Expr] = []
    denominators = [sp.together(da).as_numer_denom()[1],
                    sp.together(db).as_numer_denom()[1]]
    product_count = 0
    for mode, row_indices in stratum.certificates:
        determinant = sp.factor(marked_extension(
            stratum.q, extension, alpha, beta, mode,
        )[list(row_indices), :].det())
        assert determinant != 0
        residual = sp.factor(sp.cancel(determinant / (da * db)))
        pure_column = one_marked_map(mode, alpha, beta)[:, stratum.q]
        for entry in pure_column:
            product = sp.factor(sp.cancel(entry * residual))
            if product == 0:
                continue
            numerator, denominator = sp.together(product).as_numer_denom()
            witness_equations.append(sp.factor(numerator))
            denominators.append(sp.factor(denominator))
            product_count += 1
    assert witness_equations
    assumptions = tuple(sp.factor(sp.sympify(value).subs(
        substitutions, simultaneous=True,
    )) for value in stratum.nonzero)
    for denominator in denominators:
        assert_nonzero_on_chart(denominator, assumptions)
    da_numerator = sp.factor(sp.together(da).as_numer_denom()[0])
    db_numerator = sp.factor(sp.together(db).as_numer_denom()[0])
    inverse_symbols = sp.symbols(f"w0:{2 + len(assumptions)}")
    equations = witness_equations + [
        inverse_symbols[0] * da_numerator - 1,
        inverse_symbols[1] * db_numerator - 1,
    ] + [
        inverse * assumption - 1
        for inverse, assumption in zip(
            inverse_symbols[2:], assumptions, strict=True,
        )
    ]
    variables = tuple(sorted(
        set().union(*(equation.free_symbols for equation in equations)),
        key=str,
    ))
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert any(poly.as_expr() == 1 for poly in basis.polys), (
        stratum,
        da,
        db,
        witness_equations,
        tuple(poly.as_expr() for poly in basis.polys),
    )
    return len(kernel), product_count


def main() -> None:
    started = time.monotonic()
    check_normalization()
    check_pure_deletion()
    check_atlas()

    for distinguished in range(4):
        output = run_singular(
            projection_and_components_program(distinguished),
            timeout=120,
        )
        assert projection_basis(output) == EXPECTED_PROJECTION[
            distinguished
        ], distinguished
        assert component_bases(output) == EXPECTED_COMPONENTS[
            distinguished
        ], distinguished

    kernel_dimensions: dict[str, int] = {}
    residual_products = 0
    for stratum in STRATA:
        kernel_dimension, products = check_stratum(stratum)
        kernel_dimensions[str(kernel_dimension)] = (
            kernel_dimensions.get(str(kernel_dimension), 0) + 1
        )
        residual_products += products

    report = {
        "verified": True,
        "field": "characteristic zero",
        "normalization": (
            "H=N=1 with A->A*H and bijective row-shift action"
        ),
        "projection_runs": 4,
        "minimal_projection_components": sum(
            len(components)
            for components in EXPECTED_COMPONENTS.values()
        ),
        "exact_residual_cover_strata": len(STRATA),
        "kernel_dimension_histogram": kernel_dimensions,
        "selected_nonzero_residual_products": residual_products,
        "all_binary_extensions_ternarily_excluded": True,
        "complete_first_plane_infinity_marked_fibre_excluded": True,
        "internal_E0_marked_fibre_closed": False,
        "additional_components_closed": False,
        "global": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "sha256": {
            THEOREM.name: sha256(THEOREM),
            CANONICAL.name: sha256(CANONICAL),
            PLANE.name: sha256(PLANE),
            GENERATOR.name: sha256(GENERATOR),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
