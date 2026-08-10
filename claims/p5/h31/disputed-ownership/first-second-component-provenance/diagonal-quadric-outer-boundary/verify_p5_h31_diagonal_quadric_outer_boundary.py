#!/usr/bin/env python3
"""Verify the complete H31 obstruction on the second-component boundary."""

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
from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = (
    REPO_ROOT / 'claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md')
NORMALIZED = (
    REPO_ROOT / 'claims/p5/h31/diagonal-quadric-normalization-boundary/P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md'
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SOURCE_INVOLUTION = (1, 0, 3, 2)
MODE_INVOLUTION = (0, 2, 1, 3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.together(sp.expand(expression))).replace("**", "^")


def normal_form(A, B, C, E, F, H) -> tuple[sp.Matrix, ...]:
    return (
        sp.Matrix(((E, -F, -F, -E), (A, -B, B, A))),
        sp.Matrix(((1, 0, 0, -1), (A, C + B, C - B, A))),
        sp.Matrix(((H + E, F, F, H - E), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )


def pluecker(plane: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.factor(plane[:, (left, right)].det())
        for left, right in itertools.combinations(range(4), 2)
    )


def proportional(left, right) -> bool:
    return all(
        sp.factor(left[i] * right[j] - left[j] * right[i]) == 0
        for i in range(6)
        for j in range(i + 1, 6)
    ) and any(entry != 0 for entry in left) and any(
        entry != 0 for entry in right
    )


def marked_rows(
    A,
    B,
    C,
    E,
    F,
    H,
    pivot: tuple[int, int],
    *,
    scale_alpha3=sp.Integer(1),
) -> tuple[tuple[tuple[sp.Expr, ...], ...], ...]:
    u0 = (E, -F, -F, -E)
    u1 = (A, -B, B, A)
    y1 = (1, 0, 0, -1)
    x1 = (A, C + B, C - B, A)
    x2 = (H + E, F, F, H - E)
    y2 = (0, 1, -1, 0)
    k0 = (1, 0, 0, 1)
    k1 = (0, 1, 1, 0)
    active = sp.Matrix(
        (
            (
                -4 * F * (A * F + C * H),
                -4 * (A * F * H + C * E**2),
            ),
            (
                4 * (A * C * F + B**2 * H),
                4 * A * (A * F + C * H),
            ),
        )
    )
    row0 = (u0, u1)
    row3 = (k0, k1)
    i, j = pivot
    other_i, other_j = 1 - i, 1 - j
    pivot_value = active[i, j]
    assert pivot_value != 0
    beta0 = row0[i]
    beta3 = row3[j]
    alpha0 = tuple(
        sp.factor(
            row0[other_i][coordinate]
            - active[other_i, j] * beta0[coordinate] / pivot_value
        )
        for coordinate in range(4)
    )
    alpha3 = tuple(
        sp.factor(
            scale_alpha3
            * (
                row3[other_j][coordinate]
                - active[i, other_j]
                * beta3[coordinate]
                / pivot_value
            )
        )
        for coordinate in range(4)
    )
    alpha = (alpha0, y1, y2, alpha3)
    canonical = (beta0, x1, x2, beta3)
    return alpha, canonical


def shifted_rows(alpha, canonical):
    t = sp.symbols("t0:4")
    beta = tuple(
        tuple(
            sp.factor(
                canonical[mode][coordinate]
                + t[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return t, beta


def check_pure(alpha, canonical, expected: sp.Expr) -> None:
    coefficients = {
        word: permanent(
            tuple(
                canonical[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert sp.factor(coefficients[(1, 1, 1, 1)] - expected) == 0
    assert all(
        sp.factor(value) == 0
        for word, value in coefficients.items()
        if word != (1, 1, 1, 1)
    )


def run_relative_projection(
    label: str,
    distinguished: int,
    alpha,
    beta,
    parameter: sp.Symbol | None,
    *,
    base_nonzero: tuple[sp.Expr, ...] = (),
    timeout: float = 300,
) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse_binary = sp.Symbol("ub")
    base_inverses = sp.symbols(f"w0:{len(base_nonzero)}")
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.extend(
        (
            (diagonal_a * extension)[0] - 1,
            inverse_binary * (diagonal_b * extension)[0] - 1,
        )
    )
    equations.extend(
        inverse * factor - 1
        for inverse, factor in zip(
            base_inverses,
            base_nonzero,
            strict=True,
        )
    )
    eliminated = extensions + (inverse_binary,) + tuple(base_inverses)
    retained = shifts + (() if parameter is None else (parameter,))
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring r=0,("
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
                "Singular outer-boundary projection failure",
                label,
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def specialize_beta(beta, shifts) -> tuple[tuple[sp.Expr, ...], ...]:
    t = sp.symbols("t0:4")
    substitutions = dict(zip(t, shifts, strict=True))
    return tuple(
        tuple(
            sp.factor(sp.sympify(entry).subs(substitutions))
            for entry in row
        )
        for row in beta
    )


def verify_kernel_case(
    *,
    label: str,
    distinguished: int,
    alpha,
    beta,
    shifts,
    kernel: tuple[sp.Matrix, sp.Matrix],
    expected_diagonals: tuple[sp.Expr, sp.Expr],
    marked_mode: int,
    marked_rows: list[int],
    expected_minor: sp.Expr,
) -> dict:
    u, v = sp.symbols("u v")
    marked_beta = specialize_beta(beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        marked_beta,
    )
    assert all(
        all(sp.factor(entry) == 0 for entry in mixed * vector)
        for vector in kernel
    )
    assert sp.Matrix.hstack(*kernel).rank() == 2
    extension = u * kernel[0] + v * kernel[1]
    actual_diagonals = (
        sp.factor((diagonal_a * extension)[0]),
        sp.factor((diagonal_b * extension)[0]),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(
            actual_diagonals,
            expected_diagonals,
            strict=True,
        )
    )
    marked = marked_extension(
        distinguished,
        extension,
        alpha,
        marked_beta,
        marked_mode,
    )
    actual_minor = sp.factor(marked[marked_rows, :].det())
    assert sp.factor(actual_minor - expected_minor) == 0
    pure_column = one_marked_map(
        marked_mode,
        alpha,
        marked_beta,
    )[:, distinguished]
    assert any(sp.factor(entry) != 0 for entry in pure_column)
    return {
        "label": label,
        "distinguished_coordinate": distinguished,
        "marking": [str(entry) for entry in shifts],
        "binary_diagonals": [str(entry) for entry in actual_diagonals],
        "marked_mode": marked_mode,
        "marked_rows": marked_rows,
        "marked_minor": str(actual_minor),
    }


def stacked_marked_map(
    distinguished: int,
    mode: int,
    extension: sp.Matrix,
    alpha,
    beta,
) -> sp.Matrix:
    common = [
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    ]
    alpha_extended = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row],)
        for row in range(4)
    )
    beta_extended = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row],)
        for row in range(4)
    )
    pure = one_marked_map(mode, alpha, beta)
    neighbour = one_marked_map(mode, alpha_extended, beta_extended)
    pure_embedded = pure.row_join(sp.zeros(8, 1))
    neighbour_embedded = sp.zeros(8, 5)
    for local, global_coordinate in enumerate(common):
        neighbour_embedded[:, global_coordinate] = neighbour[:, local]
    neighbour_embedded[:, 4] = neighbour[:, 3]
    return pure_embedded.col_join(neighbour_embedded)


def main() -> None:
    A, B, C, E, F, H = sp.symbols("A B C E F H")
    psi = sp.expand(
        A**3 * F**3
        + A**2 * C * F**2 * H
        - A * B**2 * F * H**2
        - A * C**2 * E**2 * F
        + A * C**2 * F * H**2
        - B**2 * C * E**2 * H
    )
    K = sp.expand(
        A**2 * F**2
        + A * C * F * H
        - C**2 * E**2
        + C**2 * H**2
    )
    assert sp.factor(psi.subs(A, 0)) == -B**2 * C * E**2 * H
    assert sp.factor(psi.subs(F, 0)) == -B**2 * C * E**2 * H
    assert sp.factor(psi.subs(B, 0) - A * F * K) == 0

    # The one-dimensional diagonal source torus preserving the normal form.
    a, b = sp.symbols("a b", nonzero=True)
    source_torus = sp.diag(a, b, b, a)
    transformed_parameters = (a * A, b * B, b * C, a * E, b * F, a * H)
    original_planes = normal_form(A, B, C, E, F, H)
    transformed_planes = normal_form(*transformed_parameters)
    assert all(
        proportional(
            pluecker(original_planes[mode] * source_torus),
            pluecker(transformed_planes[mode]),
        )
        for mode in range(4)
    )

    # A source involution plus the mode swap 1<->2 pairs the six
    # coordinate surfaces and the two exceptional toric edges.
    p = sp.Symbol("p")
    symmetry_pairs = (
        ((0, 1, 0, p, 1, 1), (1, p, 1, 1, 0, 0), "AC_to_FH"),
        ((0, 1, p, 0, 1, 1), (1, 0, 1, 1, 0, p), "AE_to_FB"),
        ((0, 1, p, 1, 1, 0), (1, 1, 0, 1, 0, p), "AH_to_FC"),
        ((0, 1, p, 1, 0, 0), (0, 1, 0, 1, 0, p), "edge_pair"),
    )
    for source_parameters, target_parameters, _ in symmetry_pairs:
        source_planes = normal_form(*source_parameters)
        target_planes = normal_form(*target_parameters)
        permuted = tuple(
            plane[:, SOURCE_INVOLUTION] for plane in source_planes
        )
        assert all(
            proportional(
                pluecker(permuted[MODE_INVOLUTION[mode]]),
                pluecker(target_planes[mode]),
            )
            for mode in range(4)
        )

    # Representative marked curves.
    ac_alpha, ac_canonical = marked_rows(0, 1, 0, p, 1, 1, (1, 0))
    ae_alpha, ae_canonical = marked_rows(0, 1, p, 0, 1, 1, (1, 0))
    ah_alpha, ah_canonical = marked_rows(0, 1, p, 1, 1, 0, (0, 1))
    edge_alpha, edge_canonical = marked_rows(
        0, 1, p, 1, 0, 0, (0, 1)
    )
    ac_t, ac_beta = shifted_rows(ac_alpha, ac_canonical)
    ae_t, ae_beta = shifted_rows(ae_alpha, ae_canonical)
    ah_t, ah_beta = shifted_rows(ah_alpha, ah_canonical)
    edge_t, edge_beta = shifted_rows(edge_alpha, edge_canonical)
    assert ac_t == ae_t == ah_t == edge_t == sp.symbols("t0:4")
    check_pure(ac_alpha, ac_canonical, 4)
    check_pure(ae_alpha, ae_canonical, 4)
    check_pure(ah_alpha, ah_canonical, -4 * p)
    check_pure(edge_alpha, edge_canonical, -4 * p)

    expected_ac = {
        0: ("1",),
        1: ("t1", "t0", "t2*t3-t3"),
        2: ("t1", "t0", "t2*t3+t3"),
        3: ("1",),
    }
    expected_ae = {
        0: (
            "t3",
            "t1",
            "t0*t2*p-t0",
            "t0*t2^2-t0*p^2-t2*p^2+t2",
            "t2*p^3-t2*p-p^2+1",
            "t0*p^3-t0*t2+p^2-1",
        ),
        1: ("1",),
        2: ("1",),
        3: (
            "t3",
            "t1",
            "t0*t2*p-t0",
            "t0*t2^2-t0*p^2-t2*p^2+t2",
            "t2*p^3-t2*p-p^2+1",
            "t0*p^3-t0*t2+p^2-1",
        ),
    }
    expected_ah = {coordinate: ("1",) for coordinate in range(4)}
    expected_edge = {
        0: ("t2", "t0", "t1*t3"),
        1: ("1",),
        2: ("1",),
        3: ("t2", "t0", "t1*t3"),
    }
    relative_projections = {
        "AC": {
            q: run_relative_projection(
                "AC", q, ac_alpha, ac_beta, p
            )
            for q in range(4)
        },
        "AE": {
            q: run_relative_projection(
                "AE", q, ae_alpha, ae_beta, p
            )
            for q in range(4)
        },
        "AH": {
            q: run_relative_projection(
                "AH",
                q,
                ah_alpha,
                ah_beta,
                p,
                base_nonzero=(p,),
            )
            for q in range(4)
        },
        "edge": {
            q: run_relative_projection(
                "edge",
                q,
                edge_alpha,
                edge_beta,
                p,
                base_nonzero=(p,),
            )
            for q in range(4)
        },
    }
    assert relative_projections["AC"] == expected_ac
    assert relative_projections["AE"] == expected_ae
    assert relative_projections["AH"] == expected_ah
    assert relative_projections["edge"] == expected_edge

    u, v, s = sp.symbols("u v s")
    verified_cases: list[dict] = []

    # AC: t3=0 components.
    for q, second_kernel, second_diagonal in (
        (
            1,
            sp.Matrix((-1, 0, 0, 1, -1, 1, s + 1, 0)),
            4 * v,
        ),
        (
            2,
            sp.Matrix((1, 0, 0, -1, -1, 1, s - 1, 0)),
            -4 * v,
        ),
    ):
        verified_cases.append(
            verify_kernel_case(
                label=f"AC_q{q}_t3_zero",
                distinguished=q,
                alpha=ac_alpha,
                beta=ac_beta,
                shifts=(0, 0, s, 0),
                kernel=(
                    sp.Matrix((0, 0, 1, 0, 0, 0, 0, 0)),
                    second_kernel,
                ),
                expected_diagonals=(-2 * p * (u - v), second_diagonal),
                marked_mode=1,
                marked_rows=[0, 1, 3, 7],
                expected_minor=16 * p * v * (u - v) ** 2,
            )
        )

    # AC: t2=+/-1, generic s chart.
    D = p**2 * s + 1
    ac_fixed_data = {
        1: (
            1,
            sp.Matrix(
                (
                    -sp.Rational(1, 2),
                    -p * s / (2 * D),
                    0,
                    1 / (2 * D),
                    -1 / (2 * D),
                    1 / (2 * D),
                    1,
                    0,
                )
            ),
            sp.Matrix(
                (
                    0,
                    p / D,
                    1 / s,
                    p**2 / D,
                    -p**2 / D,
                    p**2 / D,
                    0,
                    1,
                )
            ),
            p * (s * u - 2 * v) / (s * D),
            -2
            * p**2
            * (2 * p**2 * v + u)
            * (s * u - 2 * v) ** 2
            / D**3,
        ),
        2: (
            -1,
            sp.Matrix(
                (
                    -sp.Rational(1, 2),
                    -p * s / (2 * D),
                    0,
                    1 / (2 * D),
                    1 / (2 * D),
                    -1 / (2 * D),
                    1,
                    0,
                )
            ),
            sp.Matrix(
                (
                    0,
                    p / D,
                    -1 / s,
                    p**2 / D,
                    p**2 / D,
                    -p**2 / D,
                    0,
                    1,
                )
            ),
            -p * (s * u - 2 * v) / (s * D),
            2
            * p**2
            * (2 * p**2 * v + u)
            * (s * u - 2 * v) ** 2
            / D**3,
        ),
    }
    for q, (t2_value, k0, k1, diagonal_a, minor) in ac_fixed_data.items():
        verified_cases.append(
            verify_kernel_case(
                label=f"AC_q{q}_fixed_t2_generic",
                distinguished=q,
                alpha=ac_alpha,
                beta=ac_beta,
                shifts=(0, 0, t2_value, s),
                kernel=(k0, k1),
                expected_diagonals=(
                    diagonal_a,
                    2 * (2 * p**2 * v + u) / D,
                ),
                marked_mode=0,
                marked_rows=[0, 1, 3, 7],
                expected_minor=minor,
            )
        )

    # AC: alternate bases on p^2 s+1=0.
    exceptional_s = -1 / p**2
    for q, t2_value, k0, k1, da, db, minor in (
        (
            1,
            1,
            sp.Matrix((0, 1 / p, 0, 1, -1, 1, 0, 0)),
            sp.Matrix((p**2, p, -p**2, 0, 0, 0, -2 * p**2, 1)),
            2 * p * (p**2 * v + u),
            4 * u,
            16 * u * (p**2 * v + u) ** 2,
        ),
        (
            2,
            -1,
            sp.Matrix((0, -1 / p, 0, -1, -1, 1, 0, 0)),
            sp.Matrix((p**2, p, p**2, 0, 0, 0, -2 * p**2, 1)),
            2 * p * (-p**2 * v + u),
            -4 * u,
            16 * u * (-p**2 * v + u) ** 2,
        ),
    ):
        verified_cases.append(
            verify_kernel_case(
                label=f"AC_q{q}_fixed_t2_exceptional",
                distinguished=q,
                alpha=ac_alpha,
                beta=ac_beta,
                shifts=(0, 0, t2_value, exceptional_s),
                kernel=(k0, k1),
                expected_diagonals=(da, db),
                marked_mode=0,
                marked_rows=[0, 1, 2, 7],
                expected_minor=minor,
            )
        )

    # AC: p=0 points in the projection are closure artifacts.
    ac_alpha_zero = tuple(
        tuple(sp.factor(sp.sympify(entry).subs(p, 0)) for entry in row)
        for row in ac_alpha
    )
    ac_beta_zero = tuple(
        tuple(sp.factor(sp.sympify(entry).subs(p, 0)) for entry in row)
        for row in ac_beta
    )
    artifact_checks = 0
    for q, shifts in (
        (1, (0, 0, s, 0)),
        (1, (0, 0, 1, s)),
        (2, (0, 0, s, 0)),
        (2, (0, 0, -1, s)),
    ):
        marked_beta = specialize_beta(ac_beta_zero, shifts)
        mixed, diagonal_a, _ = mixed_matrix(
            q, ac_alpha_zero, marked_beta
        )
        kernel = mixed.nullspace()
        assert kernel
        assert all(
            sp.factor((diagonal_a * vector)[0]) == 0
            for vector in kernel
        )
        artifact_checks += 1

    # AE: generic graph.
    generic_shifts = (-p / (p**2 + 1), 0, 1 / p, 0)
    for q, sign in ((0, 1), (3, -1)):
        L = p**2 * u + 2 * p * v - u
        verified_cases.append(
            verify_kernel_case(
                label=f"AE_q{q}_generic_graph",
                distinguished=q,
                alpha=ae_alpha,
                beta=ae_beta,
                shifts=generic_shifts,
                kernel=(
                    sp.Matrix((0, 0, 1, -p, 1, 0, 0, 0)),
                    sp.Matrix((0, sign, 0, 0, 0, 0, 1, 1)),
                ),
                expected_diagonals=(
                    sign * 2 * u * (p**2 + 1),
                    2 * L / p,
                ),
                marked_mode=0,
                marked_rows=[0, 4, 5, 7],
                expected_minor=(
                    sign * 16 * u**2 * (p**2 + 1) * L
                ),
            )
        )

    # AE: the two complete special fibres p=+/-1.
    for epsilon in (1, -1):
        ae_alpha_special = tuple(
            tuple(
                sp.factor(sp.sympify(entry).subs(p, epsilon))
                for entry in row
            )
            for row in ae_alpha
        )
        ae_beta_special = tuple(
            tuple(
                sp.factor(sp.sympify(entry).subs(p, epsilon))
                for entry in row
            )
            for row in ae_beta
        )
        special_linear = (
            (s + epsilon) * u - (s - epsilon) * v
        )
        for q, sign in ((0, 1), (3, -1)):
            verified_cases.append(
                verify_kernel_case(
                    label=f"AE_p{epsilon}_q{q}_t0_zero",
                    distinguished=q,
                    alpha=ae_alpha_special,
                    beta=ae_beta_special,
                    shifts=(0, 0, s, 0),
                    kernel=(
                        sp.Matrix(
                            (1, 0, -epsilon, 0, 0, epsilon, 1, 0)
                        ),
                        sp.Matrix(
                            (
                                -1,
                                sign,
                                epsilon,
                                0,
                                0,
                                -epsilon,
                                0,
                                1,
                            )
                        ),
                    ),
                    expected_diagonals=(
                        -sign * 2 * epsilon * (u - v),
                        2 * epsilon * special_linear,
                    ),
                    marked_mode=0,
                    marked_rows=[0, 4, 5, 7],
                    expected_minor=(
                        sign
                        * 8
                        * (u - v) ** 2
                        * special_linear
                    ),
                )
            )
            special_denominator = 2 * s + epsilon
            verified_cases.append(
                verify_kernel_case(
                    label=f"AE_p{epsilon}_q{q}_t2_fixed",
                    distinguished=q,
                    alpha=ae_alpha_special,
                    beta=ae_beta_special,
                    shifts=(s, 0, epsilon, 0),
                    kernel=(
                        sp.Matrix(
                            (
                                1,
                                0,
                                -epsilon
                                * (s + epsilon)
                                / special_denominator,
                                -s / special_denominator,
                                2
                                * s
                                * (s + epsilon)
                                / special_denominator,
                                epsilon,
                                1,
                                0,
                            )
                        ),
                        sp.Matrix(
                            (
                                -1,
                                sign,
                                epsilon
                                * (s + epsilon)
                                / special_denominator,
                                s / special_denominator,
                                -2
                                * s
                                * (s + epsilon)
                                / special_denominator,
                                -epsilon,
                                0,
                                1,
                            )
                        ),
                    ),
                    expected_diagonals=(
                        -sign
                        * 2
                        * (u - v)
                        / special_denominator,
                        4 * u,
                    ),
                    marked_mode=0,
                    marked_rows=[0, 4, 5, 7],
                    expected_minor=(
                        sign
                        * epsilon
                        * 16
                        * u
                        * (u - v) ** 2
                        / special_denominator**2
                    ),
                )
            )

    # Edge: the two components away from their intersection.
    for q, sign in ((0, 1), (3, -1)):
        verified_cases.append(
            verify_kernel_case(
                label=f"edge_q{q}_t3_zero_nonzero_t1",
                distinguished=q,
                alpha=edge_alpha,
                beta=edge_beta,
                shifts=(0, s, 0, 0),
                kernel=(
                    sp.Matrix((0, 1, 0, 0, 0, 0, 0, 0)),
                    sp.Matrix((0, 0, 0, sign, 1, s, 1, 0)),
                ),
                expected_diagonals=(
                    2 * (u - v),
                    -sign * 4 * p * v,
                ),
                marked_mode=3,
                marked_rows=[0, 2, 6, 7],
                expected_minor=(
                    sign * 32 * p * s**2 * v**2 * (u - v)
                ),
            )
        )
        first_kernel = (
            sp.Matrix((s / p, 0, -s / p, 1, 1, 2 * s / p, 1, 0))
            if q == 0
            else sp.Matrix(
                (-s / p, 0, s / p, -1, 1, -2 * s / p, 1, 0)
            )
        )
        second_kernel = (
            sp.Matrix((-1 / p, 1 / s, 1 / p, 0, 0, -2 / p, 0, 1))
            if q == 0
            else sp.Matrix(
                (-1 / p, -1 / s, 1 / p, 0, 0, -2 / p, 0, 1)
            )
        )
        edge_linear = s * u - sign * v
        verified_cases.append(
            verify_kernel_case(
                label=f"edge_q{q}_t1_zero_nonzero_t3",
                distinguished=q,
                alpha=edge_alpha,
                beta=edge_beta,
                shifts=(0, 0, 0, s),
                kernel=(first_kernel, second_kernel),
                expected_diagonals=(
                    -2 * edge_linear / s,
                    -sign * 4 * p * u,
                ),
                marked_mode=0,
                marked_rows=[0, 1, 5, 7],
                expected_minor=16 * u * edge_linear**2,
            )
        )

    # Edge intersection: one ordinary minor and one stacked exception.
    stacked_cases = []
    edge_canonical_beta = edge_canonical
    for q, sign in ((0, 1), (3, -1)):
        edge_k0 = sp.Matrix((0, 1, 0, 0, 0, 0, 0, 0))
        edge_k1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        verified_cases.append(
            verify_kernel_case(
                label=f"edge_q{q}_intersection_generic_direction",
                distinguished=q,
                alpha=edge_alpha,
                beta=edge_beta,
                shifts=(0, 0, 0, 0),
                kernel=(edge_k0, edge_k1),
                expected_diagonals=(
                    2 * (u - v),
                    -sign * 4 * p * v,
                ),
                marked_mode=0,
                marked_rows=[0, 3, 4, 7],
                expected_minor=(
                    sign * 16 * p * v * (u - v) * (u + v)
                ),
            )
        )
        exceptional_extension = -edge_k0 + edge_k1
        stacked = stacked_marked_map(
            q,
            0,
            exceptional_extension,
            edge_alpha,
            edge_canonical_beta,
        )
        stacked_rows = [3, 4, 7, 8, 12]
        stacked_minor = sp.factor(stacked[stacked_rows, :].det())
        assert stacked_minor == 128 * p
        stacked_cases.append(
            {
                "label": f"edge_q{q}_u_plus_v_zero",
                "stacked_mode": 0,
                "stacked_rows": stacked_rows,
                "stacked_minor": str(stacked_minor),
            }
        )

    # The B=0 conic.  The affine parameterization is homogeneous in
    # (E,F,H), and p^2-1 is inverted on this chart.
    conic_H = 1 - 2 * p
    conic_E = -(p**2 - p + 1)
    conic_F = p**2 - 1
    assert sp.factor(
        conic_E**2
        - conic_F**2
        - conic_F * conic_H
        - conic_H**2
    ) == 0
    conic_alpha, conic_canonical = marked_rows(
        1,
        0,
        1,
        conic_E,
        conic_F,
        conic_H,
        (1, 0),
        scale_alpha3=conic_F,
    )
    _, conic_beta = shifted_rows(conic_alpha, conic_canonical)
    check_pure(conic_alpha, conic_canonical, 4 * conic_F)
    expected_conic = {
        0: ("1",),
        1: (
            "2*p-1",
            "3*t3+4",
            "t1-1",
            "9*t0+16*t2",
            "4*t2^2+3*t2",
        ),
        2: (
            "2*p-1",
            "3*t3+4",
            "t1-1",
            "9*t0-16*t2",
            "4*t2^2-3*t2",
        ),
        3: ("1",),
    }
    conic_projection = {
        q: run_relative_projection(
            "conic_affine",
            q,
            conic_alpha,
            conic_beta,
            p,
            base_nonzero=(conic_F,),
        )
        for q in range(4)
    }
    assert conic_projection == expected_conic

    conic_plus_alpha = tuple(
        tuple(
            sp.factor(
                sp.sympify(entry).subs(p, sp.Rational(1, 2))
            )
            for entry in row
        )
        for row in conic_alpha
    )
    conic_plus_beta = tuple(
        tuple(
            sp.factor(
                sp.sympify(entry).subs(p, sp.Rational(1, 2))
            )
            for entry in row
        )
        for row in conic_beta
    )
    for q, q_sign in ((1, 1), (2, -1)):
        first_kernel = (
            sp.Matrix((-1, 0, 0, 1, 0, -sp.Rational(4, 3), 1, 0)),
            sp.Matrix((0, 0, q_sign, 0, 0, 0, 0, 1)),
        )
        first_rows = [0, 3, 6, 7] if q == 1 else [0, 2, 3, 7]
        first_denominator = 64 if q == 1 else 128
        plus = 4 * u + 3 * v
        minus = 4 * u - 3 * v
        verified_cases.append(
            verify_kernel_case(
                label=f"conic_plus_q{q}_first",
                distinguished=q,
                alpha=conic_plus_alpha,
                beta=conic_plus_beta,
                shifts=(0, 1, 0, -sp.Rational(4, 3)),
                kernel=first_kernel,
                expected_diagonals=(
                    -q_sign * 3 * plus / 8,
                    minus / 2,
                ),
                marked_mode=0,
                marked_rows=first_rows,
                expected_minor=9 * minus * plus**2 / first_denominator,
            )
        )
        second_kernel = (
            sp.Matrix((0, sp.Rational(4, 3), 0, 0, 0, 0, 1, 0)),
            sp.Matrix(
                (
                    sp.Rational(3, 4),
                    2,
                    q_sign,
                    -sp.Rational(3, 4),
                    1,
                    1,
                    0,
                    1,
                )
            ),
        )
        verified_cases.append(
            verify_kernel_case(
                label=f"conic_plus_q{q}_second",
                distinguished=q,
                alpha=conic_plus_alpha,
                beta=conic_plus_beta,
                shifts=(
                    sp.Rational(4, 3),
                    1,
                    -q_sign * sp.Rational(3, 4),
                    -sp.Rational(4, 3),
                ),
                kernel=second_kernel,
                expected_diagonals=(
                    q_sign * 3 * (2 * u + 3 * v) / 4,
                    2 * u,
                ),
                marked_mode=2,
                marked_rows=[0, 1, 5, 7],
                expected_minor=2 * u * (2 * u + 3 * v) ** 2,
            )
        )

    # The missing point u=0 of the conic parameterization.
    infinity_alpha, infinity_canonical = marked_rows(
        1, 0, 1, -1, 1, 0, (1, 0)
    )
    _, infinity_beta = shifted_rows(infinity_alpha, infinity_canonical)
    check_pure(infinity_alpha, infinity_canonical, 4)
    expected_infinity = {
        0: ("1",),
        1: ("t3-1", "t1+1", "t0+t2", "t2^2-t2"),
        2: ("t3-1", "t1+1", "t0-t2", "t2^2+t2"),
        3: ("1",),
    }
    infinity_projection = {
        q: run_relative_projection(
            "conic_infinity",
            q,
            infinity_alpha,
            infinity_beta,
            None,
        )
        for q in range(4)
    }
    assert infinity_projection == expected_infinity
    for q, q_sign in ((1, 1), (2, -1)):
        first_kernel = (
            sp.Matrix((-1, 0, 0, 1, 0, 1, 1, 0)),
            sp.Matrix((0, 0, q_sign, 0, 0, 0, 0, 1)),
        )
        verified_cases.append(
            verify_kernel_case(
                label=f"conic_infinity_q{q}_first",
                distinguished=q,
                alpha=infinity_alpha,
                beta=infinity_beta,
                shifts=(0, -1, 0, 1),
                kernel=first_kernel,
                expected_diagonals=(
                    -q_sign * 2 * (u - v),
                    2 * (u + v),
                ),
                marked_mode=1,
                marked_rows=[0, 4, 6, 7],
                expected_minor=8 * (u - v) * (u + v) ** 2,
            )
        )
        second_kernel = (
            sp.Matrix((0, 1, 0, 0, 0, 0, 1, 0)),
            sp.Matrix((-1, -2, q_sign, 1, 1, 1, 0, 1)),
        )
        verified_cases.append(
            verify_kernel_case(
                label=f"conic_infinity_q{q}_second",
                distinguished=q,
                alpha=infinity_alpha,
                beta=infinity_beta,
                shifts=(-1, -1, q_sign, 1),
                kernel=second_kernel,
                expected_diagonals=(
                    q_sign * 2 * (u - 2 * v),
                    2 * u,
                ),
                marked_mode=2,
                marked_rows=[0, 1, 5, 7],
                expected_minor=8 * u * (u - 2 * v) ** 2,
            )
        )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "toric boundary stratification, relative saturated binary "
            "projection, all-extension marked minors, and a stacked "
            "five-dimensional Fitting certificate"
        ),
        "outer_boundary": "Psi=0 and A*B*F=0",
        "all_rank_conditions": ["(A,B)!=(0,0)", "(E,F)!=(0,0)"],
        "coordinate_curve_representatives": ["AC", "AE", "AH", "edge"],
        "source_mode_symmetry_pairs": [
            label for _, _, label in symmetry_pairs
        ],
        "relative_projection_ideals": {
            family: {
                str(q): list(ideal) for q, ideal in projections.items()
            }
            for family, projections in relative_projections.items()
        },
        "ac_projection_closure_artifact_checks": artifact_checks,
        "conic_equation": "E^2=F^2+F*H+H^2",
        "conic_parameterization": {
            "H": "u*(u-2*v)",
            "E": "-(v^2-u*v+u^2)",
            "F": "v^2-u^2",
        },
        "conic_affine_projection_ideals": {
            str(q): list(ideal) for q, ideal in conic_projection.items()
        },
        "conic_infinity_projection_ideals": {
            str(q): list(ideal)
            for q, ideal in infinity_projection.items()
        },
        "verified_kernel_minor_cases": verified_cases,
        "stacked_exception_cases": stacked_cases,
        "stacked_exception_minor": "128*p",
        "all_outer_binary_survivors_classified": True,
        "all_outer_genuine_extensions_ternarily_excluded": True,
        "outer_boundary_H31_fibre_empty": True,
        "normalized_affine_slice_H31_fibre_empty": True,
        "second_component_complete_marked_fibre_empty": True,
        "all_pure_components_classified": False,
        "H31_globally_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "remaining_geometry": [
            "possible further all-rank-two pure-P4 components",
            "H22",
        ],
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            NORMALIZED.name: sha256(NORMALIZED),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_diagonal_quadric_outer_boundary_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
