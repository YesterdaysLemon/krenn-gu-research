#!/usr/bin/env python3
"""Verify the complete marked-basis fibre obstruction on the known chart."""

from __future__ import annotations

import hashlib
import json
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

from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md"
FAMILY = REPO_ROOT / 'claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md'
COMPONENT = REPO_ROOT / 'claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md'
OPEN_BRANCH = REPO_ROOT / 'claims/p5/h31/marked-basis-open-branch/P5_H31_MARKED_BASIS_OPEN_BRANCH.md'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(expression)) == 0


def rows(
    L: sp.Expr,
    Q: sp.Expr,
    C: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
]:
    D = C + L
    A = 1 + L * Q
    alpha = (
        (1, Q, 0, -A),
        (L, 1, -L, -L),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    canonical = (
        (0, 1, D, C),
        (0, 0, 1, 1),
        (0, 1, 0, L),
        (1, 0, 1, 0),
    )
    beta = tuple(
        tuple(
            sp.factor(
                canonical[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def assert_matrix_zero(matrix: sp.Matrix) -> None:
    assert all(zero(entry) for entry in matrix)


def assert_rank_minor(
    matrix: sp.Matrix,
    row_indices: tuple[int, ...],
    column_indices: tuple[int, ...],
    expected: sp.Expr,
) -> None:
    actual = sp.factor(
        matrix[list(row_indices), list(column_indices)].det()
    )
    assert zero(actual - expected), (actual, expected)


def assert_marked_factor(
    distinguished: int,
    mode: int,
    row_indices: tuple[int, ...],
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    expected: sp.Expr,
) -> None:
    matrix = marked_extension(
        distinguished,
        extension,
        alpha,
        beta,
        mode,
    )
    actual = sp.factor(matrix[list(row_indices), :].det())
    assert zero(actual - expected), (actual, expected)


def assert_pure_entry(
    distinguished: int,
    mode: int,
    expected: sp.Expr,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> None:
    column = one_marked_map(mode, alpha, beta)[:, distinguished]
    assert any(zero(entry - expected) for entry in column), (
        distinguished,
        mode,
        expected,
        tuple(map(sp.factor, column)),
    )


def assert_kernel(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    basis: tuple[sp.Matrix, ...],
    basis_rows: tuple[int, ...],
    basis_minor: sp.Expr,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    for vector in basis:
        assert_matrix_zero(mixed * vector)
    basis_matrix = sp.Matrix.hstack(*basis)
    actual_basis_minor = sp.factor(
        basis_matrix[list(basis_rows), :].det()
    )
    assert zero(actual_basis_minor - basis_minor), (
        actual_basis_minor,
        basis_minor,
    )
    return mixed, diagonal_a, diagonal_b


def assert_unit_cover(
    residuals: tuple[sp.Expr, ...],
    coordinates: tuple[sp.Symbol, ...],
    parameters: tuple[sp.Symbol, ...] = (),
    nonzero_parameters: tuple[sp.Expr, ...] = (),
) -> None:
    """Check that the residual forms have no common nonzero vector.

    The coordinate normalization sum(h_i*z_i)-1 projectivizes the
    extension direction.  Parameter inverses encode only the explicitly
    stated nonvanishing assumptions.
    """

    h = sp.symbols(f"h0:{len(coordinates)}")
    inverses = sp.symbols(f"w0:{len(nonzero_parameters)}")
    equations = [
        sp.together(residual).as_numer_denom()[0]
        for residual in residuals
    ]
    equations.append(
        sum(left * right for left, right in zip(h, coordinates, strict=True))
        - 1
    )
    equations.extend(
        inverse * parameter - 1
        for inverse, parameter in zip(
            inverses,
            nonzero_parameters,
            strict=True,
        )
    )
    variables = coordinates + parameters + h + inverses
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert basis.is_zero_dimensional or basis.polys
    assert any(poly.as_expr() == 1 for poly in basis.polys), tuple(
        poly.as_expr() for poly in basis.polys
    )


def check_normalizations() -> None:
    E, I, L, Q, C = sp.symbols("E I L Q C", nonzero=True)
    D = C + E * I * L
    source = sp.diag(E * I, E * I, E, 1)
    original_alpha = (
        (1, Q, 0, -E * I * (1 + L * Q)),
        (L, 1, -I * L, -E * I * L),
        (-1 / I, 0, 1, 0),
        (0, 0, -1 / E, 1),
    )
    original_beta = (
        (0, 1, D / E, C),
        (0, 0, 1, E),
        (0, 1, 0, E * I * L),
        (1, 0, I, 0),
    )
    alpha_scales = (1 / (E * I), 1 / (E * I), 1 / E, 1)
    beta_scales = (1 / (E * I), 1 / E, 1 / (E * I), 1 / (E * I))
    normalized_alpha, normalized_beta = rows(
        L,
        Q,
        C / (E * I),
        (0, 0, 0, 0),
    )
    for mode in range(4):
        transformed_alpha = (
            sp.Matrix([original_alpha[mode]]) * source
            * alpha_scales[mode]
        )
        transformed_beta = (
            sp.Matrix([original_beta[mode]]) * source
            * beta_scales[mode]
        )
        assert_matrix_zero(
            transformed_alpha - sp.Matrix([normalized_alpha[mode]])
        )
        assert_matrix_zero(
            transformed_beta - sp.Matrix([normalized_beta[mode]])
        )

    # The different alpha/beta row scalings induce the stated bijection
    # on the four Borel shift coordinates.
    shift_multipliers = tuple(
        sp.factor(beta_scales[mode] / alpha_scales[mode])
        for mode in range(4)
    )
    assert shift_multipliers == (1, I, 1 / I, 1 / (E * I))

    # L!=0 weighted source normalization.
    l, q, c = sp.symbols("l q c", nonzero=True)
    source_l = sp.diag(1, l, 1, 1)
    alpha_l, beta_l = rows(l, q, c, (0, 0, 0, 0))
    alpha_one, beta_one = rows(1, l * q, c / l, (0, 0, 0, 0))
    one = sp.Integer(1)
    alpha_l_scales = (one, one / l, one, one)
    beta_l_scales = (one / l, one, one / l, one)
    for mode in range(4):
        assert_matrix_zero(
            sp.Matrix([alpha_l[mode]])
            * source_l
            * alpha_l_scales[mode]
            - sp.Matrix([alpha_one[mode]])
        )
        assert_matrix_zero(
            sp.Matrix([beta_l[mode]])
            * source_l
            * beta_l_scales[mode]
            - sp.Matrix([beta_one[mode]])
        )
    assert tuple(
        sp.factor(beta_l_scales[mode] / alpha_l_scales[mode])
        for mode in range(4)
    ) == (1 / l, l, 1 / l, 1)

    # L=0,C!=0 weighted source normalization.
    source_c = sp.diag(1, c, 1, 1)
    alpha_c, beta_c = rows(0, q, c, (0, 0, 0, 0))
    alpha_c_one, beta_c_one = rows(0, c * q, 1, (0, 0, 0, 0))
    alpha_c_scales = (one, one / c, one, one)
    beta_c_scales = (one / c, one, one / c, one)
    for mode in range(4):
        assert_matrix_zero(
            sp.Matrix([alpha_c[mode]])
            * source_c
            * alpha_c_scales[mode]
            - sp.Matrix([alpha_c_one[mode]])
        )
        assert_matrix_zero(
            sp.Matrix([beta_c[mode]])
            * source_c
            * beta_c_scales[mode]
            - sp.Matrix([beta_c_one[mode]])
        )


def projection_bases() -> dict[int, tuple[sp.Expr, ...]]:
    c, q = sp.symbols("c q")
    s0, s1, s2, s3 = sp.symbols("s0:4")
    return {
        0: (
            s3,
            s2 * c + q * c - s1 + q + 1,
            s1 * c - s2 * c + s1,
            s0 * c - s2 * c + q * c + q + c + 2,
            s2 * q + s2,
            s1 * q + s1,
            s0 * q + s0 - s1 + 1,
            s1 * s2 - s2,
            s0 * s2 - s2,
            s1**2 - s1,
            s0 * s1 - s1,
            (q + 1) * ((c + 1) * q + 1),
        ),
        1: (
            q * c + s0 + q - c,
            (2 * c + 1) * s3,
            (2 * c + 1) * s2,
            (2 * c + 1) * s1 + 5 * c * s2
            + 2 * s2 + s3 - c - 1,
            (2 * c + 1) * s0 - 2 * c**2 - 3 * c - 1,
            s3 * q - 6 * c * s1 - 9 * c * s2
            + 2 * s0 - 3 * s1 - 4 * s2 + c + 1,
            s2 * q - 2 * s3 * q + 4 * c * s1
            + 4 * c * s2 - 2 * s0 + 2 * s1
            + 3 * s2 - 2 * s3,
            3 * s1 * q + 3 * s2 * q - 6 * c * s1
            - 3 * c * s2 - 10 * c * s3 + 6 * s0
            + 3 * s1 + s3 - 3 * c - 6,
            s0 * q + 2 * c * s1 + 2 * c * s2 + c * s3
            + s0 + s1 + s2 + s3 - 2 * c - 1,
            s3**2 - s3,
            s2 * s3 - s3,
            s1 * s3,
            2 * s0 * s3 - 2 * s0 + s2 - 2 * s3
            + 2 * c + 2,
            s2**2 + 2 * c * s2 + 2 * s2 - 2 * s3,
            s1 * s2 - s2 + s3,
            2 * s0 * s2 - 2 * s0 + s2 - 2 * s3
            + 2 * c + 2,
            4 * s0 * s1 - 2 * s1 - 3 * s2 + 4 * s3
            - 2 * c - 2,
            4 * s0**2 - 4 * c**2 - s2 + s3 - 8 * c - 4,
        ),
        2: (
            s3,
            s1,
            s2 * q + s2 - 1,
            s0 * s2 * c + s0 * q * c + s0 * q - s0 * c
            - s2 * c + c + 1,
            (s0 * q + 1) * ((c + 1) * q + 1),
        ),
        3: (
            s1,
            s2 * c - s3 * c - s3,
            s3 * q,
            s2 * q,
            s0 * q - s3 + 1,
            s3**2 - s3,
            s2 * s3 - s2,
            s0 * s3 + s3,
            s0 * s2 + s2,
        ),
    }


def check_projection_case_splits() -> None:
    c, q = sp.symbols("c q")
    s0, s1, s2, s3 = sp.symbols("s0:4")
    bases = projection_bases()

    def vanishes(
        distinguished: int,
        substitutions: dict[sp.Symbol, sp.Expr],
    ) -> None:
        assert all(
            zero(generator.subs(substitutions, simultaneous=True))
            for generator in bases[distinguished]
        )

    # q=0: the A=0 and B=0 branches, with their intersection empty.
    vanishes(
        0,
        {
            q: -1,
            s0: 1,
            s1: 1,
            s2: (c + 1) / c,
            s3: 0,
        },
    )
    vanishes(
        0,
        {
            q: -1 / (c + 1),
            s0: -(c + 1) / c,
            s1: 0,
            s2: 0,
            s3: 0,
        },
    )
    assert zero(
        bases[0][3].subs(
            {c: 0, q: -1, s0: 0, s1: 0, s2: 0, s3: 0}
        )
        - 1
    )

    # q=1: the B=0 curve away from 2c+1=0.
    vanishes(
        1,
        {
            q: -1 / (c + 1),
            s0: c + 1,
            s1: (c + 1) / (2 * c + 1),
            s2: 0,
            s3: 0,
        },
    )
    specialized = tuple(
        sp.factor(generator.subs(c, -sp.Rational(1, 2)))
        for generator in bases[1]
    )
    triangular = (
        2 * s0 + q + 1,
        s1 + q**2 + 2 * q,
        s2 - 2 * q**2 - 4 * q - 1,
        s3 - q**2 - 2 * q - 1,
        q * (q + 1) * (q + 2),
    )
    triangular_basis = sp.groebner(
        triangular,
        s0,
        s1,
        s2,
        s3,
        q,
        order="lex",
        domain=sp.QQ,
    )
    assert all(
        zero(triangular_basis.reduce(generator)[1])
        for generator in specialized
    )
    specialized_basis = sp.groebner(
        specialized,
        s0,
        s1,
        s2,
        s3,
        q,
        order="lex",
        domain=sp.QQ,
    )
    assert all(
        zero(specialized_basis.reduce(generator)[1])
        for generator in triangular
    )
    for q_value, shift in (
        (-2, (sp.Rational(1, 2), 0, 1, 1)),
        (-1, (0, 1, -1, 0)),
        (0, (-sp.Rational(1, 2), 0, 1, 1)),
    ):
        vanishes(
            1,
            {
                c: -sp.Rational(1, 2),
                q: q_value,
                s0: shift[0],
                s1: shift[1],
                s2: shift[2],
                s3: shift[3],
            },
        )

    # q=2: generic unique point or the free B=0 line.
    vanishes(
        2,
        {
            s0: -1 / q,
            s1: 0,
            s2: 1 / (q + 1),
            s3: 0,
        },
    )
    vanishes(
        2,
        {
            q: -1 / (c + 1),
            s1: 0,
            s2: (c + 1) / c,
            s3: 0,
        },
    )
    assert zero(
        sp.factor(
            bases[2][4]
            - (s0 * q + 1) * ((c + 1) * q + 1)
        )
    )

    # q=3: t3=0 gives q*s0+1=0; t3=1 gives q=0.
    vanishes(
        3,
        {s0: -1 / q, s1: 0, s2: 0, s3: 0},
    )
    vanishes(
        3,
        {
            q: 0,
            s0: -1,
            s1: 0,
            s2: (c + 1) / c,
            s3: 1,
        },
    )


def check_q0() -> int:
    L, Q, C, T = sp.symbols("L Q C T", nonzero=True)
    D = C + L
    R = 2 * C + L
    u, v = sp.symbols("u v")
    checked = 0

    # A=0, away from R=0.
    alpha, beta = rows(L, -1 / L, C, (L, 1 / L, L * D / C, 0))
    basis = (
        sp.Matrix((1, 0, 0, -L / R, C * L / R, 1, 0, 0)),
        sp.Matrix((0, L, -1, L / R, L * D / R, 0, -L * D / C, 1)),
    )
    mixed, da, db = assert_kernel(
        0, alpha, beta, basis, (0, 1), L
    )
    assert_rank_minor(
        mixed,
        (0, 1, 2, 3, 7, 9),
        (0, 1, 2, 3, 4, 6),
        2 * L * R / C,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * C * (u - v) / R)
    assert zero(d1 - 2 * D * (C * u + D * v) / R)
    assert_marked_factor(
        0, 0, (0, 4, 6, 7), extension, alpha, beta,
        d0 * d1 * (-2 * (u - v) / R),
    )
    assert_pure_entry(0, 0, 1, alpha, beta)
    checked += 1

    # The R=0 specialization needs a different, non-collapsing basis.
    alpha, beta = rows(
        L, -1 / L, -L / 2, (L, 1 / L, -L, 0)
    )
    basis = (
        sp.Matrix((0, 0, 0, 2 / L, 1, 0, 0, 0)),
        sp.Matrix((1, L, -1, -2, 0, 1, L, 1)),
    )
    mixed, da, db = assert_kernel(
        0, alpha, beta, basis, (0, 3), -2 / L
    )
    assert_rank_minor(
        mixed,
        (0, 1, 2, 3, 7, 9),
        (0, 1, 2, 3, 5, 6),
        -2 * L**2,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * (u - L * v) / L)
    assert zero(d1 - u)
    assert_marked_factor(
        0, 1, (0, 2, 3, 7), extension, alpha, beta,
        d0 * d1 * (-2 * u / L),
    )
    assert_pure_entry(0, 1, -1, alpha, beta)
    checked += 1

    # B=0.
    alpha, beta = rows(
        L, -1 / D, C, (-L * D / C, 0, 0, 0)
    )
    basis = (
        sp.Matrix((
            1, L - C, 0, 0,
            (C - L) * D / C, 0, D, 0,
        )),
        sp.Matrix((1, L, -1, 0, -L * D / C, 0, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        0, alpha, beta, basis, (0, 2), -1
    )
    assert_rank_minor(
        mixed,
        (1, 2, 3, 4, 5, 7),
        (0, 1, 2, 3, 4, 5),
        2 * L / D**2,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * C * u / D)
    assert zero(d1 - 2 * D * (u + v))
    assert_marked_factor(
        0, 0, (0, 2, 3, 7), extension, alpha, beta,
        d0 * d1 * (-2 * L**2 * u),
    )
    assert_pure_entry(0, 0, 1, alpha, beta)
    checked += 1

    # L=0,Q!=0, with arbitrary T.
    alpha, beta = rows(0, Q, C, (T, 0, 0, 0))
    basis = (
        sp.Matrix((
            1, 1 / Q, 0, 0,
            -(Q * T + 1) / Q, 0, -1 / Q, 0,
        )),
        sp.Matrix((1, 0, -1, 0, T, 0, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        0, alpha, beta, basis, (1, 2), -1 / Q
    )
    assert_rank_minor(
        mixed,
        (0, 1, 3, 5, 6, 7),
        (0, 1, 2, 3, 4, 5),
        -2 * Q,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    H = C * Q * v - (Q * T + 1) * u
    assert zero(d0 - 2 * u)
    assert zero(d1 - 2 * H / Q)
    residuals = (
        -2 * Q * (u + v),
        -2 * T * u,
        -2 * v * (Q * T + 1),
    )
    for mode, indices, residual in (
        (2, (0, 1, 3, 7), residuals[0]),
        (2, (0, 1, 4, 7), residuals[1]),
        (1, (0, 2, 4, 7), residuals[2]),
    ):
        assert_marked_factor(
            0, mode, indices, extension, alpha, beta,
            d0 * d1 * residual,
        )
        assert_pure_entry(0, mode, 1, alpha, beta)
    assert_unit_cover(
        residuals,
        (u, v),
        parameters=(Q, T),
        nonzero_parameters=(Q,),
    )
    checked += 1

    # At L=Q=0 the first diagonal is identically zero.
    alpha, beta = rows(0, 0, C, (T, 0, 0, 0))
    mixed, da, _ = mixed_matrix(0, alpha, beta)
    assert mixed.rank() == 6
    for vector in mixed.nullspace():
        assert zero((da * vector)[0])
    return checked


def check_q1() -> int:
    L, C = sp.symbols("L C", nonzero=True)
    D = C + L
    R = L + 2 * C
    u, v = sp.symbols("u v")
    checked = 0

    # B=0 with C,R nonzero.
    alpha, beta = rows(
        L,
        -1 / D,
        C,
        (D, D / (L * R), 0, 0),
    )
    basis = (
        sp.Matrix((1, 0, 0, -1, 0, -1, 0, 0)),
        sp.Matrix((
            1, L * D * R / C**2, 0, -D**2 / C**2,
            0, 0, L * D * R / C**2, 0,
        )),
    )
    mixed, da, db = assert_kernel(
        1,
        alpha,
        beta,
        basis,
        (1, 3),
        L * D * R / C**2,
    )
    assert_rank_minor(
        mixed,
        (0, 1, 2, 3, 4, 7),
        (0, 1, 2, 3, 4, 7),
        2 * C**2 * L**6 / D**3,
    )
    extension = u * basis[0] + v * basis[1]
    F = C**2 * u + D**2 * v
    G = C * u - D * v
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * L * R * F / (C**2 * D))
    assert zero(d1 + 2 * L * D * G / C)
    residual = -2 * L**2 * F / (C**2 * R)
    assert_marked_factor(
        1, 0, (0, 2, 4, 7), extension, alpha, beta,
        d0 * d1 * residual,
    )
    assert_pure_entry(1, 0, L, alpha, beta)
    checked += 1

    # C=0 (the A=B=0 intersection) remains on the B=0 curve.
    alpha, beta = rows(L, -1 / L, 0, (L, 1 / L, 0, 0))
    basis = (
        sp.Matrix((1, 0, 0, -1, 0, -1, 0, 0)),
        sp.Matrix((0, 1, 0, -1 / L, 0, 0, 1, 0)),
    )
    mixed, da, db = assert_kernel(
        1, alpha, beta, basis, (0, 1), 1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 2, 3, 7, 8),
        (0, 1, 2, 3, 4, 7),
        -2 * L**7,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * (L * u + v))
    assert zero(d1 + 2 * L**2 * u)
    assert_marked_factor(
        1, 0, (0, 2, 4, 7), extension, alpha, beta,
        d0 * d1 * (-2 * (L * u + v)),
    )
    assert_pure_entry(1, 0, 1, alpha, beta)
    checked += 1

    special_cases = (
        (
            "qbar=-2",
            -2 / L,
            (L / 2, 0, L, 1),
            (
                sp.Matrix((-2 / L, 1, 0, 0, 0, 0, 1, 0)),
                sp.Matrix((-1, 0, 0, 0, 0, 0, 0, 1)),
            ),
            (0, 1),
            1,
            (0, 1, 3, 7),
            0,
            -4 * L**2 * v,
            -L * v,
            L * (L * v + 2 * u) / 2,
            L,
            (
                (0, 1, 3, 4, 5, 7),
                (0, 1, 2, 3, 4, 5),
                -4 * L**4,
            ),
        ),
        (
            "qbar=-1",
            -1 / L,
            (0, 1 / L, -L, 0),
            (
                sp.Matrix((0, 0, 0, 2 / L, 1, 0, 0, 0)),
                sp.Matrix((-1 / L, 1, 0, -2 / L, 0, 1 / L, 1, 0)),
            ),
            (0, 4),
            1 / L,
            (0, 2, 4, 7),
            1,
            2 * u,
            -2 * (u - v),
            L * u,
            1,
            (
                (0, 1, 2, 3, 7, 9),
                (0, 1, 2, 3, 5, 7),
                -2 * L**9,
            ),
        ),
        (
            "qbar=0",
            0,
            (-L / 2, 0, L, 1),
            (
                sp.Matrix((0, 0, -2 / L, 0, 1, 0, 0, 0)),
                sp.Matrix((0, 1, 2 / L, 0, 0, 0, 1, 0)),
            ),
            (1, 2),
            2 / L,
            (0, 4, 6, 7),
            1,
            L * u,
            -2 * (u - v),
            L * u,
            -L,
            (
                (0, 1, 2, 3, 5, 7),
                (0, 1, 2, 3, 5, 7),
                4 * L**7,
            ),
        ),
    )
    for (
        _,
        q_value,
        shifts,
        basis,
        basis_rows,
        basis_minor,
        marked_rows,
        marked_mode,
        residual,
        expected_d0,
        expected_d1,
        pure_entry,
        rank_certificate,
    ) in special_cases:
        alpha, beta = rows(L, q_value, -L / 2, shifts)
        mixed, da, db = assert_kernel(
            1,
            alpha,
            beta,
            basis,
            basis_rows,
            basis_minor,
        )
        assert_rank_minor(mixed, *rank_certificate)
        extension = u * basis[0] + v * basis[1]
        d0 = sp.factor((da * extension)[0])
        d1 = sp.factor((db * extension)[0])
        assert zero(d0 - expected_d0)
        assert zero(d1 - expected_d1)
        assert_marked_factor(
            1,
            marked_mode,
            marked_rows,
            extension,
            alpha,
            beta,
            d0 * d1 * residual,
        )
        assert_pure_entry(
            1, marked_mode, pure_entry, alpha, beta
        )
        checked += 1

    # L=0: d0 is identically zero for every marking.
    Q, C0 = sp.symbols("Q C0")
    t = sp.symbols("t0:4")
    alpha, beta = rows(0, Q, C0, t)
    _, da, _ = mixed_matrix(1, alpha, beta)
    assert_matrix_zero(da)
    return checked


def check_q2() -> int:
    L, Q, C, T = sp.symbols("L Q C T", nonzero=True)
    D = C + L
    A = 1 + L * Q
    B = 1 + D * Q
    u, v, w = sp.symbols("u v w")
    checked = 0

    # Generic branch.
    alpha, beta = rows(L, Q, C, (-1 / Q, 0, L / A, 0))
    basis = (
        sp.Matrix((1, 0, 0, -1, B / Q, 1, 0, 0)),
        sp.Matrix((1, L, -1, 0, 1 / Q, 0, -L / A, -1)),
    )
    mixed, da, db = assert_kernel(
        2, alpha, beta, basis, (2, 3), -1
    )
    assert_rank_minor(
        mixed,
        (1, 2, 3, 4, 7, 9),
        (0, 1, 2, 3, 4, 6),
        2 * L**3 * Q**3 / A,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 + 2 * A * (u + v))
    assert zero(d1 - 2 * (B * u + v) / Q)
    residuals = (
        -2 * Q * A * u,
        -2 * (A * u + v) / A,
    )
    assert_marked_factor(
        2, 2, (0, 1, 3, 7), extension, alpha, beta,
        d0 * d1 * residuals[0],
    )
    assert_marked_factor(
        2, 1, (0, 2, 3, 7), extension, alpha, beta,
        d0 * d1 * residuals[1],
    )
    assert_pure_entry(2, 2, A, alpha, beta)
    assert_pure_entry(2, 1, -1, alpha, beta)
    assert_unit_cover(
        residuals,
        (u, v),
        parameters=(L, Q),
        nonzero_parameters=(L, Q, A),
    )
    checked += 1

    # B=0 free line, away from T=D.
    A_b = C / D
    alpha, beta = rows(L, -1 / D, C, (T, 0, L / A_b, 0))
    P = C * D + L * T
    basis = (
        sp.Matrix((
            D**2, -L * (C - L) * (D - T), 0, -P,
            D * (C - L) * (D - T), P, L * D * (D - T), 0,
        )),
        sp.Matrix((
            D**2, L**2 * (D - T), -C * (D - T), -T * D,
            -L * D * (D - T), T * D, 0, -C * (D - T),
        )),
    )
    mixed, da, db = assert_kernel(
        2,
        alpha,
        beta,
        basis,
        (2, 6),
        C * L * D * (D - T) ** 2,
    )
    assert_rank_minor(
        mixed,
        (1, 2, 3, 4, 7, 9),
        (0, 1, 2, 3, 4, 5),
        2 * L**4 * (D - T) / (C * D**3),
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 + 2 * C * D * (u + v))
    assert zero(d1 - 2 * C * D * u * (D - T))
    residual = 2 * L**4 * (u + v) * (D - T) / C
    assert_marked_factor(
        2, 0, (0, 2, 3, 7), extension, alpha, beta,
        d0 * d1 * residual,
    )
    assert_pure_entry(2, 0, 1, alpha, beta)
    checked += 1

    # The point T=D on the free line.
    alpha, beta = rows(L, -1 / D, C, (D, 0, L / A_b, 0))
    basis = (
        sp.Matrix((1, 0, 0, -1, 0, 1, 0, 0)),
        sp.Matrix((1, L, -1, 0, -D, 0, -L * D / C, -1)),
    )
    mixed, da, db = assert_kernel(
        2, alpha, beta, basis, (2, 3), -1
    )
    assert_rank_minor(
        mixed,
        (1, 2, 3, 4, 7, 9),
        (0, 1, 2, 3, 4, 6),
        -2 * L**3 / (C * D**2),
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 + 2 * C * (u + v) / D)
    assert zero(d1 + 2 * D * v)
    residuals = (2 * C * u / D**2, -2 * (C * u + D * v) / C)
    assert_marked_factor(
        2, 2, (0, 1, 3, 7), extension, alpha, beta,
        d0 * d1 * residuals[0],
    )
    assert_marked_factor(
        2, 1, (0, 2, 3, 7), extension, alpha, beta,
        d0 * d1 * residuals[1],
    )
    assert_pure_entry(2, 2, C / D, alpha, beta)
    assert_pure_entry(2, 1, -1, alpha, beta)
    assert_unit_cover(
        residuals,
        (u, v),
        parameters=(C, L),
        nonzero_parameters=(C, D),
    )
    checked += 1

    # L=0, Q!=0.
    alpha, beta = rows(0, Q, C, (T, 0, 0, 0))
    basis = (
        sp.Matrix((1, 0, 0, -1, C - T, 1, 0, 0)),
        sp.Matrix((-Q, -1, 0, 0, Q * T + 1, 0, 1, 0)),
        sp.Matrix((-1, 0, 1, 0, T, 0, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        2, alpha, beta, basis, (1, 2, 3), 1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 3, 6, 7),
        (0, 1, 2, 3, 4),
        -Q,
    )
    extension = u * basis[0] + v * basis[1] + w * basis[2]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 + 2 * (u - Q * v - w))
    assert zero(
        d1 - 2 * ((C - T) * u + (Q * T + 1) * v + T * w)
    )
    residuals = (
        -2 * (u - w),
        -2 * Q * (u - Q * v),
        2 * (Q * v + w),
    )
    for mode, indices, residual in (
        (1, (0, 2, 3, 7), residuals[0]),
        (2, (0, 1, 3, 7), residuals[1]),
        (3, (0, 2, 3, 7), residuals[2]),
    ):
        assert_marked_factor(
            2, mode, indices, extension, alpha, beta,
            d0 * d1 * residual,
        )
        assert_pure_entry(2, mode, 1, alpha, beta)
    assert_unit_cover(
        residuals,
        (u, v, w),
        parameters=(Q,),
        nonzero_parameters=(Q,),
    )
    checked += 1

    # L=Q=0.
    alpha, beta = rows(0, 0, C, (T, 0, 0, 0))
    basis = (
        sp.Matrix((1, 0, 0, -1, C - T, 1, 0, 0)),
        sp.Matrix((0, -1, 0, 0, 1, 0, 1, 0)),
        sp.Matrix((-1, 0, 1, 0, T, 0, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        2, alpha, beta, basis, (1, 2, 3), 1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 5, 6, 7),
        (0, 1, 2, 3, 4),
        1,
    )
    extension = u * basis[0] + v * basis[1] + w * basis[2]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    residuals = (-2 * u, 2 * w, 2 * v)
    for indices, residual in (
        ((0, 2, 4, 7), residuals[0]),
        ((0, 3, 4, 7), residuals[1]),
        ((0, 3, 6, 7), residuals[2]),
    ):
        assert_marked_factor(
            2, 1, indices, extension, alpha, beta,
            d0 * d1 * residual,
        )
    assert_pure_entry(2, 1, 1, alpha, beta)
    assert_unit_cover(residuals, (u, v, w))
    checked += 1
    return checked


def check_q3() -> int:
    L, Q, C, T, S = sp.symbols("L Q C T S", nonzero=True)
    D = C + L
    B = 1 + D * Q
    u, v, w = sp.symbols("u v w")
    checked = 0

    # L,Q nonzero.
    alpha, beta = rows(L, Q, C, (-1 / Q, 0, 0, 0))
    basis = (
        sp.Matrix((1, 0, 0, -1, -B / Q, -1, 0, 0)),
        sp.Matrix((1, 1 / Q, 0, 0, 0, 0, -1 / Q, 0)),
    )
    mixed, da, db = assert_kernel(
        3, alpha, beta, basis, (1, 3), 1 / Q
    )
    assert_rank_minor(
        mixed,
        (0, 1, 2, 3, 4, 7),
        (0, 1, 2, 3, 4, 7),
        2 * L * Q**2 * (1 + L * Q),
    )
    assert_rank_minor(
        mixed,
        (0, 1, 2, 3, 7, 8),
        (0, 1, 2, 3, 4, 7),
        -2 * L * Q * (C * (1 + L * Q) + L**2 * Q),
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 + 2 * (L * Q * u - v))
    assert zero(d1 + 2 * D * u)
    residuals = (-2 * Q * (u + v), -2 * v / Q)
    assert_marked_factor(
        3, 2, (0, 1, 3, 7), extension, alpha, beta,
        d0 * d1 * residuals[0],
    )
    assert_marked_factor(
        3, 2, (0, 1, 4, 7), extension, alpha, beta,
        d0 * d1 * residuals[1],
    )
    assert_pure_entry(3, 2, 1, alpha, beta)
    assert_unit_cover(
        residuals,
        (u, v),
        parameters=(Q,),
        nonzero_parameters=(Q,),
    )
    checked += 1

    # Q=0,L,C nonzero.
    alpha, beta = rows(0 + L, 0, C, (-L, 0, L * D / C, 1))
    basis = (
        sp.Matrix((
            0, -C / D, -C / (L * D), C / (L * D),
            C / L, C / (L * D), 1, 0,
        )),
        sp.Matrix((
            -1, -L**2 / D, C / D, L / D,
            L, L / D, 0, 1,
        )),
    )
    mixed, da, db = assert_kernel(
        3, alpha, beta, basis, (0, 6), 1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 5, 7, 8, 9),
        (0, 1, 2, 3, 4, 5),
        -2 * L**2 * D,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * C * (u - L * v) / (L * D))
    assert zero(d1 - 2 * D * u / L)
    residual = -2 * L * (u - L * v) / D
    assert_marked_factor(
        3, 0, (0, 1, 3, 7), extension, alpha, beta,
        d0 * d1 * residual,
    )
    assert_pure_entry(3, 0, 1, alpha, beta)
    checked += 1

    # L=0,Q!=0, t0-axis.
    alpha, beta = rows(0, Q, C, (T, 0, 0, 0))
    basis = (
        sp.Matrix((-1, 0, 0, 1, C - T, 1, 0, 0)),
        sp.Matrix((-Q, -1, 0, 0, Q * T + 1, 0, 1, 0)),
    )
    mixed, da, db = assert_kernel(
        3, alpha, beta, basis, (0, 1), 1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 3, 4, 6, 7),
        (0, 1, 2, 3, 4, 7),
        -2 * Q**2,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 + 2 * Q * v)
    assert zero(d1 - 2 * (C * u + (Q * T + 1) * v))
    residuals = (
        2 * Q * (u + Q * v),
        -2 * Q * T * v,
        -2 * (Q * T + 1) * v,
    )
    for mode, indices, residual in (
        (2, (0, 1, 3, 7), residuals[0]),
        (2, (0, 1, 4, 7), residuals[1]),
        (1, (0, 2, 6, 7), residuals[2]),
    ):
        assert_marked_factor(
            3, mode, indices, extension, alpha, beta,
            d0 * d1 * residual,
        )
        assert_pure_entry(3, mode, 1, alpha, beta)
    assert_unit_cover(
        residuals,
        (u, v),
        parameters=(Q, T),
        nonzero_parameters=(Q,),
    )
    checked += 1

    # L=0,Q!=0, t3-axis away from S=0,1.
    alpha, beta = rows(0, Q, C, (0, 0, 0, S))
    basis = (
        sp.Matrix((
            0, -1, -Q * S / (S - 1), Q / (S - 1),
            (C * Q + S - 1) / (S - 1),
            Q / (S - 1), 1, 0,
        )),
        sp.Matrix((-1 / S, 0, 0, 1 / S, C / S, 1 / S, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        3, alpha, beta, basis, (1, 7), -1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 3, 4, 6, 7),
        (0, 1, 2, 3, 4, 5),
        -2 * Q**2 * S * (S - 1),
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert_marked_factor(
        3, 1, (0, 2, 6, 7), extension, alpha, beta,
        d0 * d1 * (-2 * u),
    )
    assert_pure_entry(3, 1, 1, alpha, beta)
    checked += 1

    # S=1,Q!=0.
    alpha, beta = rows(0, Q, C, (0, 0, 0, 1))
    basis = (
        sp.Matrix((0, 0, -1, 1, C, 1, 0, 0)),
        sp.Matrix((-1, 0, 1, 0, 0, 0, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        3, alpha, beta, basis, (2, 4), -C
    )
    assert_rank_minor(
        mixed,
        (0, 1, 3, 4, 6, 7),
        (0, 1, 2, 3, 4, 6),
        2 * Q**3,
    )
    extension = u * basis[0] + v * basis[1]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    assert zero(d0 - 2 * (u - v))
    assert zero(d1 - 2 * C * u)
    assert_marked_factor(
        3, 1, (0, 2, 4, 7), extension, alpha, beta,
        d0 * d1 * (2 * u),
    )
    assert_pure_entry(3, 1, 1, alpha, beta)
    checked += 1

    # Q=0 has the unique marking t3=1 and a three-dimensional kernel.
    alpha, beta = rows(0, 0, C, (0, 0, 0, 1))
    basis = (
        sp.Matrix((0, 0, -1, 1, C, 1, 0, 0)),
        sp.Matrix((0, -1, 0, 0, 1, 0, 1, 0)),
        sp.Matrix((-1, 0, 1, 0, 0, 0, 0, 1)),
    )
    mixed, da, db = assert_kernel(
        3, alpha, beta, basis, (0, 1, 2), 1
    )
    assert_rank_minor(
        mixed,
        (0, 1, 5, 7, 8),
        (0, 1, 2, 3, 4),
        -C,
    )
    extension = u * basis[0] + v * basis[1] + w * basis[2]
    d0 = sp.factor((da * extension)[0])
    d1 = sp.factor((db * extension)[0])
    residuals = (2 * u, 2 * w, -2 * v)
    for indices, residual in (
        ((0, 2, 4, 7), residuals[0]),
        ((0, 2, 5, 7), residuals[1]),
        ((0, 2, 6, 7), residuals[2]),
    ):
        assert_marked_factor(
            3, 1, indices, extension, alpha, beta,
            d0 * d1 * residual,
        )
    assert_pure_entry(3, 1, 1, alpha, beta)
    assert_unit_cover(residuals, (u, v, w))
    checked += 1
    return checked


def main() -> None:
    check_normalizations()
    check_projection_case_splits()
    branch_counts = {
        "q0": check_q0(),
        "q1": check_q1(),
        "q2": check_q2(),
        "q3": check_q3(),
    }
    output = {
        "verified": True,
        "field": "C",
        "method": (
            "determinantal marked-basis incidence, exact projection "
            "case splits, kernel-rank certificates, and all-extension "
            "marked-minor covers"
        ),
        "normalization_actions_checked": 3,
        "projection_orientations_checked": 4,
        "certificate_strata_checked": branch_counts,
        "all_binary_extensions_ternarily_excluded": True,
        "finite_known_family_marked_fibre_closed": True,
        "projective_component_boundary_closed": False,
        "additional_plane_components_closed": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            FAMILY.name: sha256(FAMILY),
            COMPONENT.name: sha256(COMPONENT),
            OPEN_BRANCH.name: sha256(OPEN_BRANCH),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_marked_basis_fibre_classification_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
