#!/usr/bin/env python3
"""Verify the middle-coordinate rank-drop chart on the elliptic component."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import mixed_matrix


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md"
GENERIC = ROOT / "P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md"
H0_THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md"
)
PURE_DIRECTION = (
    ROOT
    / "P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
PIVOT_ROWS = (1, 2, 3, 8, 9, 11)
PIVOT_COLUMNS = (0, 2, 3, 4, 5, 6)
REMAINING_COLUMN = 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remainder_mod_elliptic(
    expression: sp.Expr,
    Y: sp.Symbol,
    relation: sp.Expr,
) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, Y),
        sp.Poly(relation, Y),
    ).as_expr()
    return sp.factor(remainder / denominator)


def bordered_minor(
    matrix: sp.Matrix,
    row: int,
    Y: sp.Symbol,
    relation: sp.Expr,
) -> sp.Expr:
    return remainder_mod_elliptic(
        matrix.extract(
            PIVOT_ROWS + (row,),
            PIVOT_COLUMNS + (REMAINING_COLUMN,),
        ).det(method="domain-ge"),
        Y,
        relation,
    )


def unique_dependent_factor(
    expression: sp.Expr,
    variable: sp.Symbol,
) -> sp.Expr:
    numerator = sp.factor(sp.fraction(sp.cancel(expression))[0])
    dependent = [
        factor
        for factor, multiplicity in sp.factor_list(numerator)[1]
        if factor.has(variable)
        for _ in range(multiplicity)
    ]
    assert len(dependent) == 1
    return dependent[0]


def same_divisor(left: sp.Expr, right: sp.Expr) -> None:
    ratio = sp.factor(left / right)
    assert ratio != 0
    assert not ratio.free_symbols


def main() -> None:
    r, x, Y = sp.symbols("r x Y")
    t = sp.symbols("t0:4")
    t0, t1, t2, t3 = t
    D = x + r**2 - 1
    f = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    elliptic_relation = Y**2 - f
    Q = (
        -r**4
        + r**2 * x**2
        - 3 * r**2 * x
        + 2 * r**2
        - x**2
        + 2 * x
        - 1
    )
    assert sp.factor(Q + f / x) == 0

    alpha = (
        (
            Y + r**2 * x,
            -r * x - r**2 * x,
            -r * x + r**2 * x,
            -Y + r**2 * x,
        ),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (r, -1, -1, r),
    )
    canonical_beta = (
        (1, -1, 1, 1),
        (D, r * x + D, r * x - D, D),
        (x * (1 - x) + Y, r * x, r * x, x * (1 - x) - Y),
        (0, 1, 1, 0),
    )
    beta = tuple(
        tuple(
            canonical_beta[mode][coordinate]
            + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    expected_pivot = (
        -64
        * r**2
        * t0
        * x**2
        * (t3 - 1)
        * (r**2 * x - t2)
        * D
        * Q**2
    )
    cases = {}

    for distinguished, sigma in ((1, -1), (2, 1)):
        mixed, diagonal_a, diagonal_b = mixed_matrix(
            distinguished,
            alpha,
            beta,
        )
        if distinguished == 1:
            kernel_zero = (
                -r * x * (r + 1),
                0,
                1,
                -1,
                -1,
                (r + 1) * (r + x - 1),
                r * x,
                1,
            )
        else:
            kernel_zero = (
                r * x * (r - 1),
                0,
                -1,
                -1,
                1,
                (r - 1) * (-r + x - 1),
                r * x,
                1,
            )
        marked_kernel = sp.Matrix(
            kernel_zero[:4]
            + tuple(
                kernel_zero[4 + mode] + t[mode] * kernel_zero[mode]
                for mode in range(4)
            )
        )
        assert all(
            remainder_mod_elliptic(entry, Y, elliptic_relation) == 0
            for entry in mixed * marked_kernel
        )
        assert remainder_mod_elliptic(
            (diagonal_a * marked_kernel)[0],
            Y,
            elliptic_relation,
        ) == 0
        assert remainder_mod_elliptic(
            (diagonal_b * marked_kernel)[0],
            Y,
            elliptic_relation,
        ) == -4 * r * x * (x - 1 - r) * (x - 1 + r)

        # The a2 entry of the universal kernel is +/-1, so deleting that
        # column gives a quotient test for an additional kernel vector.
        quotient = mixed[:, [0, 1, 3, 4, 5, 6, 7]]
        pivot = remainder_mod_elliptic(
            quotient.extract(PIVOT_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            ),
            Y,
            elliptic_relation,
        )
        assert sp.factor(pivot - expected_pivot) == 0

        border_zero = bordered_minor(
            quotient,
            0,
            Y,
            elliptic_relation,
        )
        expected_border_zero = (
            128
            * sigma
            * r**3
            * t3
            * x**2
            * (t3 - 1)
            * (r**2 * x - t2)
            * D
            * Q**2
        )
        assert sp.factor(border_zero - expected_border_zero) == 0

        quotient_t3_zero = quotient.subs(t3, 0)
        border_ten = bordered_minor(
            quotient_t3_zero,
            10,
            Y,
            elliptic_relation,
        )
        expected_border_ten = (
            -128
            * r**3
            * t0
            * x**2
            * (r * x + sigma * t2)
            * D
            * (t2 + x**2 - x)
            * Q**2
        )
        # sigma=-1 gives rx-t2; sigma=+1 gives rx+t2.
        assert sp.factor(border_ten - expected_border_ten) == 0

        border_seven = bordered_minor(
            quotient_t3_zero,
            7,
            Y,
            elliptic_relation,
        )
        short_seven = (
            r**4 * t0 * x**2
            + sigma * r**3 * t0 * x**2
            + r**2 * t0 * x**3
            - r**2 * t0 * x**2
            + r**2 * x
            + sigma * r * t0 * x**3
            - sigma * r * t0 * x**2
            - t2
        )
        expected_border_seven = (
            128
            * sigma
            * r**3
            * t0
            * x**2
            * D
            * Q**2
            * short_seven
        )
        assert sp.factor(border_seven - expected_border_seven) == 0

        branch_one = {
            t3: 0,
            t2: -sigma * r * x,
            t0: -1 / (x * D),
        }
        branch_two = {
            t3: 0,
            t2: x * (1 - x),
            t0: -1 / (r * (r + sigma) * x),
        }
        assert sp.factor(short_seven.subs(branch_one)) == 0
        assert sp.factor(short_seven.subs(branch_two)) == 0

        branch_factors = {}
        for name, substitution in (
            ("I", branch_one),
            ("II", branch_two),
        ):
            specialized = quotient.subs(substitution)
            dependent = {
                row: unique_dependent_factor(
                    bordered_minor(
                        specialized,
                        row,
                        Y,
                        elliptic_relation,
                    ),
                    t1,
                )
                for row in (5, 6, 13)
            }

            def compatibility(left_row: int, right_row: int) -> sp.Expr:
                left = dependent[left_row]
                right = dependent[right_row]
                return remainder_mod_elliptic(
                    sp.diff(left, t1) * right.subs(t1, 0)
                    - sp.diff(right, t1) * left.subs(t1, 0),
                    Y,
                    elliptic_relation,
                )

            compatibility_6_13 = compatibility(6, 13)
            if name == "I":
                expected = (
                    sigma
                    * Y
                    * (r + sigma)
                    * (x - 1)
                    * (x - 1 + sigma * r) ** 2
                    * D
                    * Q
                )
                same_divisor(compatibility_6_13, expected)
                at_h0 = sp.factor(dependent[13].subs(x, 1))
                assert sp.factor(at_h0 - r**4 * (Y - t1)) == 0
                branch_factors[name] = {
                    "compatibility_6_13": sp.factor(expected),
                    "H0_t1_factor": at_h0,
                }
            else:
                expected_6_13 = (
                    sigma
                    * Y
                    * r
                    * (x - 1 + sigma * r)
                    * D
                    * Q
                )
                same_divisor(compatibility_6_13, expected_6_13)
                compatibility_5_6 = compatibility(5, 6)
                expected_5_6 = (
                    2
                    * Y
                    * r**2
                    * (x - 1)
                    * (x + 1 - sigma * r)
                    * D**2
                    * Q
                )
                same_divisor(compatibility_5_6, expected_5_6)
                # Substituting x=1-sigma*r into the second condition
                # leaves only r=0 or r=sigma on this branch.
                assert sp.factor(
                    ((x - 1) * (x + 1 - sigma * r)).subs(
                        x,
                        1 - sigma * r,
                    )
                ) == 2 * r * (r - sigma)
                branch_factors[name] = {
                    "compatibility_6_13": sp.factor(expected_6_13),
                    "compatibility_5_6": sp.factor(expected_5_6),
                }

        cases[str(distinguished)] = {
            "universal_kernel": [str(entry) for entry in marked_kernel],
            "pivot": str(pivot),
            "branch_factors": {
                name: {
                    key: str(value)
                    for key, value in values.items()
                }
                for name, values in branch_factors.items()
            },
        }

    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinates": [1, 2],
        "universal_mixed_kernel_verified": True,
        "dense_pivot_rank_drop_support": [
            "H0 ruling x=1",
            "already-closed pure-direction curves",
            "already-closed singular base fibres",
        ],
        "new_survivor_curve_on_pivot_chart": False,
        "full_survivor_divisor_classified": False,
        "cases": cases,
        "dependencies": {
            path.name: sha256(path)
            for path in (GENERIC, H0_THEOREM, PURE_DIRECTION)
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp"
        / "p5_h31_elliptic_middle_coordinate_rank_drop_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
