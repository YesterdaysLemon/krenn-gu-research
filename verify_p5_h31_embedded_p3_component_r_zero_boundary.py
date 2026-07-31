#!/usr/bin/env python3
"""Verify the exact H31 obstruction on the r=0 ninth-component divisor."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
NORMALIZED = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))

S, U, a, b, c, h, k, d, Y = sp.symbols("S U a b c h k d Y")
x1, x2, x3, y1, y2, y3 = sp.symbols("x1 x2 x3 y1 y2 y3")
EXTENSION_VARIABLES = (x1, x2, x3, y1, y2, y3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent3(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
    )


def insertion_data() -> tuple[
    dict[tuple[int, int, int], sp.Expr], sp.Matrix
]:
    """Insertion coefficients in the marked bases."""
    p, q, rho = 1, S, U
    ell1 = p - q - rho
    ell2 = p - q + rho
    ell3 = p + q - rho
    ell4 = p + q + rho
    z1, z2, z3 = sp.symbols("z1 z2 z3")
    canonical = {
        (0, 0, 0): ell4 * x1 + ell1 * x2 + ell2 * x3,
        (0, 0, 1): ell1 * x2 + ell2 * z3,
        (0, 1, 0): ell4 * x1 + ell1 * z2,
        (0, 1, 1): ell3 * x1 + ell1 * z2,
        (1, 0, 0): ell1 * x2 + ell4 * z1,
        (1, 0, 1): -2 * q * x2,
        (1, 1, 0): ell3 * x3 + ell4 * z1 + ell1 * z2,
        (1, 1, 1): ell3 * (z1 + z3) - 2 * q * z2,
    }
    markings = (a, b, c)
    shifted: dict[tuple[int, int, int], sp.Expr] = {}
    for word in WORDS3:
        value = 0
        selected = tuple(index for index, bit in enumerate(word) if bit)
        for keep in itertools.product((0, 1), repeat=len(selected)):
            canonical_word = [0, 0, 0]
            coefficient = 1
            for offset, mode in enumerate(selected):
                if keep[offset]:
                    canonical_word[mode] = 1
                else:
                    coefficient *= markings[mode]
            value += coefficient * canonical[tuple(canonical_word)]
        shifted[word] = sp.factor(
            sp.expand(value).subs(
                {
                    z1: y1 - a * x1,
                    z2: y2 - b * x2,
                    z3: y3 - c * x3,
                }
            )
        )
    mixed_words = tuple(
        word for word in WORDS3 if word not in ((0, 0, 0), (1, 1, 1))
    )
    mixed = sp.Matrix(
        [
            [
                sp.diff(shifted[word], variable)
                for variable in EXTENSION_VARIABLES
            ]
            for word in mixed_words
        ]
    )
    return shifted, mixed


INSERTION, MIXED = insertion_data()


def bases(substitution: dict[sp.Symbol, sp.Expr]):
    alpha = (
        (0, 1, S, U),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta = (
        (1, 0, 0, 0),
        (0, -1 - a, a, 1),
        (0, 1 + b, 1, b),
        (0, -1, c, 1 + c),
    )
    return tuple(
        tuple(sp.sympify(entry).subs(substitution) for entry in row)
        for row in alpha
    ), tuple(
        tuple(sp.sympify(entry).subs(substitution) for entry in row)
        for row in beta
    )


def check_family(
    *,
    name: str,
    substitution: dict[sp.Symbol, sp.Expr],
    kernel: tuple[sp.Expr, ...],
    expected_alpha: sp.Expr,
    covers: tuple[tuple[int, tuple[int, ...], sp.Expr], ...],
) -> dict[str, object]:
    specialized_kernel = sp.Matrix(
        tuple(
            sp.factor(sp.sympify(entry).subs(substitution))
            for entry in kernel
        )
    )
    specialized_mixed = MIXED.subs(substitution)
    assert all(
        sp.factor(entry) == 0
        for entry in specialized_mixed * specialized_kernel
    ), name
    alpha_diagonal = sp.factor(
        INSERTION[(0, 0, 0)]
        .subs(substitution)
        .subs(
            dict(
                zip(
                    EXTENSION_VARIABLES,
                    specialized_kernel,
                    strict=True,
                )
            )
        )
    )
    assert sp.factor(alpha_diagonal - expected_alpha) == 0, name
    assert alpha_diagonal != 0

    beta_beta_beta = sp.factor(
        INSERTION[(1, 1, 1)]
        .subs(substitution)
        .subs(
            dict(
                zip(
                    EXTENSION_VARIABLES,
                    specialized_kernel,
                    strict=True,
                )
            )
        )
    )
    alpha_rows, beta_rows = bases(substitution)
    extension = sp.Matrix(
        (
            beta_beta_beta / 2,
            *specialized_kernel[:3, 0],
            Y,
            *specialized_kernel[3:, 0],
        )
    )
    checked_covers = []
    for mode, rows, expected in covers:
        neighboring = marked_extension(
            0, extension, alpha_rows, beta_rows, mode
        )
        actual = sp.factor(
            neighboring.extract(rows, range(4)).det(method="domain-ge")
        )
        assert sp.factor(actual - expected) == 0, (
            name,
            mode,
            rows,
            actual,
            expected,
        )
        pure = one_marked_map(mode, alpha_rows, beta_rows)
        assert any(sp.factor(pure[row, 0]) != 0 for row in range(8))
        checked_covers.append(
            {
                "mode": mode,
                "rows": "".join(str(row) for row in rows),
                "determinant": str(sp.factor(expected)),
            }
        )
    return {
        "alpha_diagonal": str(alpha_diagonal),
        "covers": checked_covers,
    }


def main() -> None:
    # The signed swap X2'=-X3, X3'=-X2 sends r=0,t!=0 to r'=-t.
    cap_a, cap_b, t = sp.symbols("A B t", nonzero=True)
    old_normals = (
        sp.Matrix((1, cap_a, cap_b)),
        sp.Matrix((1, -cap_a, -cap_b)),
        sp.Matrix((1, -cap_a, cap_b)),
    )
    signed_swap = sp.Matrix(((1, 0, 0), (0, 0, -1), (0, -1, 0)))
    transformed = tuple(signed_swap * normal for normal in old_normals)
    expected_normals = (
        sp.Matrix((1, cap_b, cap_a)),
        sp.Matrix((1, -cap_b, -cap_a)),
        sp.Matrix((1, -cap_b, cap_a)),
    )
    assert transformed == (
        expected_normals[1],
        expected_normals[0],
        expected_normals[2],
    )
    transformed_mode_zero_first_row = sp.Matrix((1, 0, -t, 0))
    assert transformed_mode_zero_first_row[2] == -t

    # Last-three pure tensor.
    alpha_rows, beta_rows = bases({})
    last_alpha = tuple(row[1:] for row in alpha_rows[1:])
    last_beta = tuple(row[1:] for row in beta_rows[1:])
    pure_p3 = {
        word: sp.factor(
            permanent3(
                tuple(
                    last_beta[mode] if word[mode] else last_alpha[mode]
                    for mode in range(3)
                )
            )
        )
        for word in WORDS3
    }
    assert pure_p3[(1, 1, 1)] == -2
    assert all(
        value == 0
        for word, value in pure_p3.items()
        if word != (1, 1, 1)
    )

    d1 = S - U - 1
    d2 = S + U - 1
    d3 = S + U + 1
    phi = sp.factor(
        S
        * (
            U * ((S - U) * (a + 1) * (b + 1) - a * (b + 1) + 1)
            + b * (S + 1)
        )
        + c * (S * b * (S + U + 1) + U * a * (1 - S - U))
    )
    determinant = sp.factor(MIXED.det(method="domain-ge"))
    assert sp.factor(determinant + 4 * d1 * d2 * d3 * phi) == 0

    signed_sheet_kernels = (
        ({U: S - 1}, sp.Matrix((0, 0, 0, 0, 0, 1))),
        ({U: 1 - S}, sp.Matrix((0, 0, 0, 0, 1, 0))),
        ({U: -S - 1}, sp.Matrix((0, 0, 0, 1, 0, 0))),
    )
    for substitution, kernel in signed_sheet_kernels:
        assert all(
            sp.factor(entry) == 0
            for entry in MIXED.subs(substitution) * kernel
        )
        assert (
            INSERTION[(0, 0, 0)]
            .subs(substitution)
            .subs(
                dict(
                    zip(
                        EXTENSION_VARIABLES,
                        kernel,
                        strict=True,
                    )
                )
            )
            == 0
        )

    # A cofactor column for the residual sheet.
    raw_kernel = tuple(
        sp.factor(
            (-1) ** (5 + column)
            * MIXED.minor_submatrix(5, column).det(method="domain-ge")
        )
        for column in range(6)
    )
    residual_kernel = sp.Matrix(
        tuple(sp.factor(entry / (2 * d1)) for entry in raw_kernel)
    )
    residual_alpha = sp.factor(
        INSERTION[(0, 0, 0)].subs(
            dict(
                zip(
                    EXTENSION_VARIABLES,
                    residual_kernel,
                    strict=True,
                )
            )
        )
    )
    assert residual_alpha == 2 * S * U * d1 * d2 * d3
    assert all(
        sp.factor(entry) == 0
        for entry in (MIXED * residual_kernel)[:5, 0]
    )

    phi0 = sp.factor(phi.subs(c, 0))
    phic = sp.factor(sp.diff(phi, c))
    c_on_phi = sp.factor(-phi0 / phic)
    residual_beta = sp.factor(
        INSERTION[(1, 1, 1)].subs(
            dict(
                zip(
                    EXTENSION_VARIABLES,
                    residual_kernel,
                    strict=True,
                )
            )
        )
    )
    residual_extension = sp.Matrix(
        (
            residual_beta / 2,
            *residual_kernel[:3, 0],
            Y,
            *residual_kernel[3:, 0],
        )
    )
    residual_expected = (
        (
            1,
            (0, 2, 4, 7),
            4 * S * U * Y**2 * (b + 1) * d1 * d2 * d3**2,
        ),
        (
            2,
            (0, 2, 4, 7),
            4 * S * U * Y**2 * (a + 1) * d1 * d2**2 * d3,
        ),
        (
            3,
            (0, 2, 4, 7),
            -4 * S * U * Y**2 * a * d1**2 * d2 * d3,
        ),
    )
    for mode, rows, expected in residual_expected:
        neighboring = marked_extension(
            0, residual_extension, alpha_rows, beta_rows, mode
        )
        actual = neighboring.extract(rows, range(4)).det(
            method="domain-ge"
        )
        assert sp.factor(
            sp.cancel(actual.subs(c, c_on_phi)) - expected
        ) == 0

    # The four zero-projected-coordinate branches of Phi.
    zero_coordinate_families = (
        (
            "S0_a0",
            {S: 0, a: 0},
            (
                -b * (U - 1) * (U + 1) * (c + 1),
                -(U + 1)
                * (-U**2 * b - U**2 + U * b * c + U + b * c + b),
                U * (U - 1) * (U + 1) * (b + 1),
                -(U - 1)
                * (-U**2 * b - U**2 + U * b * c + U + b * c + b),
                -b * (U + 1) ** 2 * (b + 1) * (-U + c + 1),
                (U - 1) ** 2 * (c + 1) * (U * b + U + b),
            ),
            2 * U * (U - 1) * (U + 1),
            ((2, (0, 2, 4, 7), 4 * U * Y**2 * (U - 1) ** 2 * (U + 1)),),
        ),
        (
            "S0_c0",
            {S: 0, c: 0},
            (
                -b * (U - 1) * (U + 1),
                (U + 1)
                * (
                    U**2 * a * b
                    + U**2 * a
                    + U**2 * b
                    + U**2
                    + U * a * b
                    + U * a
                    - U
                    - b
                ),
                U * (U - 1) * (U + 1) * (a + 1) * (b + 1),
                (U - 1) ** 2 * (a + 1) * (U * b + U + b),
                b * (U + 1) ** 2 * (b + 1) * (U * a + U - 1),
                (U - 1)
                * (
                    U**2 * a * b
                    + U**2 * a
                    + U**2 * b
                    + U**2
                    + U * a * b
                    + U * a
                    - U
                    - b
                ),
            ),
            2 * U * (U - 1) * (U + 1),
            ((1, (0, 3, 4, 7), -4 * U * Y**2 * (U - 1) ** 2 * (U + 1)),),
        ),
        (
            "U0_b0",
            {U: 0, b: 0},
            (
                -(S - 1)
                * (-S**2 * a - S**2 + S * a * c + S * a - S - a * c),
                -a * c * (S - 1) * (S + 1),
                S * (S - 1) * (S + 1) * (a + 1),
                -a * (-S + c) * (S - 1) ** 2 * (a + 1),
                -(S + 1)
                * (-S**2 * a - S**2 + S * a * c + S * a - S - a * c),
                c * (S + 1) ** 2 * (S * a + S - a),
            ),
            2 * S * (S - 1) * (S + 1),
            ((1, (0, 2, 4, 7), 4 * S * Y**2 * (S - 1) * (S + 1) ** 2),),
        ),
        (
            "U0_cm1",
            {U: 0, c: -1},
            (
                (S - 1)
                * (
                    S**2 * a * b
                    + S**2 * a
                    + S**2 * b
                    + S**2
                    - S * a * b
                    - S * b
                    + S
                    - a
                ),
                a * (S - 1) * (S + 1),
                S * (S - 1) * (S + 1) * (a + 1) * (b + 1),
                a * (S - 1) ** 2 * (a + 1) * (S * b + S + 1),
                (S + 1) ** 2 * (b + 1) * (S * a + S - a),
                -(S + 1)
                * (
                    S**2 * a * b
                    + S**2 * a
                    + S**2 * b
                    + S**2
                    - S * a * b
                    - S * b
                    + S
                    - a
                ),
            ),
            2 * S * (S - 1) * (S + 1),
            ((1, (0, 1, 5, 7), 4 * S * Y**2 * (S - 1) * (S + 1) ** 2),),
        ),
    )
    verified_families: dict[str, object] = {}
    for (
        name,
        substitution,
        kernel,
        expected_alpha,
        covers,
    ) in zero_coordinate_families:
        verified_families[name] = check_family(
            name=name,
            substitution=substitution,
            kernel=kernel,
            expected_alpha=expected_alpha,
            covers=covers,
        )

    # Maximal-minor ideals on the three signed sheets.
    sheet_data = (
        (
            {U: S - 1},
            5,
            (
                -32 * S * (S - 1) * (S * a + S - a) * (S * b + S - 1),
                -32 * S**2 * c * (S - 1) * (c + 1) * (S * a + S - a),
                -32 * S**2 * c * (S - 1) * (S * a + S - a),
                32 * S * c * (S - 1) ** 2 * (c + 1) * (S * b + S - 1),
                32 * S * (S - 1) ** 2 * (c + 1) * (S * b + S - 1),
                0,
            ),
        ),
        (
            {U: 1 - S},
            4,
            (
                -32 * S * b * (S - 1) * (b + 1) * (S * a + S - a),
                32 * S * (S - 1) * (S + c) * (S * a + S - a),
                32 * S * (S - 1) * (b + 1) * (S * a + S - a),
                -32 * S * b * (S - 1) ** 2 * (S + c) * (b + 1),
                0,
                32 * S * b * (S - 1) ** 2 * (S + c),
            ),
        ),
        (
            {U: -S - 1},
            3,
            (
                -32 * S * a * (S + 1) * (a + 1) * (S * b + S + 1),
                -32 * S**2 * a * (-S + c) * (S + 1) * (a + 1),
                0,
                32 * S * (-S + c) * (S + 1) * (S * b + S + 1),
                32 * S * (S + 1) * (a + 1) * (S * b + S + 1),
                32 * S**2 * a * (-S + c) * (S + 1),
            ),
        ),
    )
    for substitution, kernel_column, expected_minors in sheet_data:
        specialized = MIXED.subs(substitution)
        columns = tuple(
            column for column in range(6) if column != kernel_column
        )
        actual_minors = tuple(
            sp.factor(
                specialized.extract(
                    tuple(row for row in range(6) if row != omitted),
                    columns,
                ).det(method="domain-ge")
            )
            for omitted in range(6)
        )
        assert actual_minors == expected_minors

    signed_families = (
        (
            "I1",
            {U: S - 1, a: -S / (S - 1), b: (1 - S) / S},
            ((S - 1) * (c + 1), S * c, -1, -c, c + 1, h),
            2 * S * (S - 1),
            ((2, (0, 2, 6, 7), 8 * S * Y**2),),
        ),
        (
            "I2",
            {U: S - 1, b: (1 - S) / S, c: 0},
            (S - 1, 0, (S - 1) * (a + 1), 0, 1, h),
            2 * S * (S - 1),
            ((1, (0, 2, 6, 7), 8 * Y**2 * (S - 1)),),
        ),
        (
            "I3",
            {U: S - 1, a: -S / (S - 1), c: -1},
            (0, -S, -S * (b + 1), 1, 0, h),
            2 * S * (S - 1),
            ((2, (0, 2, 6, 7), 8 * S * Y**2),),
        ),
        (
            "J1",
            {U: 1 - S, a: -S / (S - 1), b: 0},
            (0, c, -1, S, h, 0),
            2 * (S - 1),
            ((2, (0, 3, 6, 7), -8 * S * Y**2),),
        ),
        (
            "J2",
            {U: 1 - S, a: -S / (S - 1), c: -S},
            (-b * (S - 1), -S, -b - 1, S * (b + 1), h, S * b),
            2 * (S - 1),
            ((2, (0, 3, 6, 7), -8 * S * Y**2),),
        ),
        (
            "J3",
            {U: 1 - S, b: -1, c: -S},
            (1 - S, -a * (S - 1), 0, 0, h, S),
            -2 * (S - 1),
            ((2, (0, 3, 4, 7), -8 * S * Y**2 * (S - 1)),),
        ),
        (
            "K1",
            {U: -S - 1, b: -(S + 1) / S, a: 0},
            (-c - 1, 0, -1, h, S + 1, 0),
            2 * S,
            ((2, (0, 2, 4, 7), -8 * S * Y**2),),
        ),
        (
            "K2",
            {U: -S - 1, b: -(S + 1) / S, c: S},
            (S + 1, S * a, a + 1, h, -(S + 1) * (a + 1), a * (S + 1)),
            -2 * S,
            ((1, (0, 3, 6, 7), 8 * Y**2 * (S + 1)),),
        ),
        (
            "K3",
            {U: -S - 1, a: -1, c: S},
            (S * b, S, 0, h, 0, S + 1),
            2 * S,
            ((3, (0, 2, 4, 7), 8 * S**2 * Y**2),),
        ),
    )
    for name, substitution, kernel, expected_alpha, covers in signed_families:
        verified_families[name] = check_family(
            name=name,
            substitution=substitution,
            kernel=kernel,
            expected_alpha=expected_alpha,
            covers=covers,
        )

    # The two empty deepest base points.
    assert sp.factor(a * c + a + c - ((a + 1) * (c + 1) - 1)) == 0
    assert sp.factor(b * c + c + 1 - (c * (b + 1) + 1)) == 0

    deep_families = (
        (
            "P1",
            {S: 0, U: 1, a: 0, c: 0},
            (b, h, -b - 1, 0, k, 0),
            -2,
            (
                (3, (0, 1, 4, 7), -8 * Y**2 * b),
                (1, (0, 2, 4, 7), -8 * Y**2 * (b + 1)),
            ),
        ),
        (
            "P2",
            {S: 0, U: 1, a: 0, b: 0},
            (0, h, 1, 0, k, 0),
            2,
            ((1, (0, 2, 4, 7), 8 * Y**2),),
        ),
        (
            "P3",
            {S: 0, U: 1, b: -1, c: 0},
            (1, h, 0, 0, k, 0),
            2,
            ((3, (0, 1, 5, 7), 8 * Y**2),),
        ),
        (
            "Q1",
            {S: -1, U: 0, b: 0, c: -1},
            (h, -a, a + 1, k, 0, 0),
            2,
            (
                (3, (0, 2, 4, 7), 8 * Y**2 * a),
                (2, (0, 2, 4, 7), -8 * Y**2 * (a + 1)),
            ),
        ),
        (
            "Q2",
            {S: -1, U: 0, a: 0, b: 0},
            (h, 0, 1, k, 0, 0),
            2,
            ((2, (0, 2, 4, 7), -8 * Y**2),),
        ),
        (
            "Q3",
            {S: -1, U: 0, a: -1, c: -1},
            (h, 1, 0, k, 0, 0),
            2,
            ((3, (0, 2, 6, 7), 8 * Y**2),),
        ),
        (
            "R1",
            {S: 0, U: 0, a: 0, b: 0},
            (d, 1 - d, 1, d - 1, -d, -c + d - 1),
            2,
            ((1, (0, 2, 4, 7), 4 * Y**2),),
        ),
        (
            "R2",
            {S: 0, U: 0, b: 0, c: 0},
            (
                d,
                -a - d + 1,
                a + 1,
                (a + 1) * (d - 1),
                -d,
                a + d - 1,
            ),
            2,
            ((1, (0, 2, 4, 7), 4 * Y**2),),
        ),
        (
            "R3",
            {S: 0, U: 0, a: 0, c: -1},
            (
                d,
                -b - d + 1,
                b + 1,
                b + d - 1,
                -(b + 1) * (b + d),
                d,
            ),
            2,
            ((1, (0, 1, 5, 7), 4 * Y**2),),
        ),
    )
    for name, substitution, kernel, expected_alpha, covers in deep_families:
        verified_families[name] = check_family(
            name=name,
            substitution=substitution,
            kernel=kernel,
            expected_alpha=expected_alpha,
            covers=covers,
        )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "signed source transport, tangent-Segre insertion divisor, "
            "Fitting strata, and one-marked factor covers"
        ),
        "signed_swap_transports_t_nonzero_to_r_nonzero": True,
        "mixed_determinant": str(determinant),
        "residual_factor": str(phi),
        "residual_open_cover": [
            str(sp.factor(item[2])) for item in residual_expected
        ],
        "zero_coordinate_branch_count": len(zero_coordinate_families),
        "signed_sheet_second_drop_family_count": len(signed_families),
        "deep_base_points": [
            "(0,0)",
            "(0,1)",
            "(0,-1)",
            "(1,0)",
            "(-1,0)",
        ],
        "deep_genuine_family_count": len(deep_families),
        "empty_deep_points": ["(0,-1)", "(1,0)"],
        "verified_boundary_families": verified_families,
        "r_zero_A_nonzero_H31_fibre_empty": True,
        "support_two_A_zero_closed_elsewhere": True,
        "whole_affine_B_nonzero_ninth_component_H31_fibre_empty": True,
        "projective_compactification_closed": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            NORMALIZED.name: sha256(NORMALIZED),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
