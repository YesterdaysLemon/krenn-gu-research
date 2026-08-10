#!/usr/bin/env python3
"""Verify the generic elliptic-surface obstruction on the second component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout
from verify_p5_h31_marked_basis_open_branch import mixed_matrix


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "diagonal-quadric"
    / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md")
H0_THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md"
)
PURE_DIRECTION_THEOREM = (
    ROOT
    / "P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
EXPECTED_PROJECTIONS = {coordinate: ("1",) for coordinate in range(4)}


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


def remainder_mod_quadratic(
    expression: sp.Expr,
    variable: sp.Symbol,
    relation: sp.Expr,
) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, variable),
        sp.Poly(relation, variable),
    ).as_expr()
    return sp.factor(remainder / denominator)


def elliptic_add_mod(
    left: tuple[int, int] | None,
    right: tuple[int, int] | None,
    modulus: int,
) -> tuple[int, int] | None:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % modulus == 0:
        return None
    if left == right:
        slope = (
            (3 * x1**2 + 20 * x1 - 27)
            * pow(2 * y1, -1, modulus)
        ) % modulus
    else:
        slope = (
            (y2 - y1) * pow(x2 - x1, -1, modulus)
        ) % modulus
    x3 = (slope**2 - 10 - x1 - x2) % modulus
    y3 = (-y1 + slope * (x1 - x3)) % modulus
    return x3, y3


def point_order_mod(
    point: tuple[int, int],
    modulus: int,
) -> int:
    accumulator = None
    for order in range(1, 4 * modulus + 20):
        accumulator = elliptic_add_mod(accumulator, point, modulus)
        if accumulator is None:
            return order
    raise AssertionError(("point order bound exceeded", point, modulus))


def curve_order_mod(modulus: int) -> int:
    return 1 + sum(
        1
        for x_value in range(modulus)
        for y_value in range(modulus)
        if (
            y_value**2
            - x_value**3
            - 10 * x_value**2
            + 27 * x_value
        )
        % modulus
        == 0
    )


def run_function_field_projection(
    distinguished: int,
    alpha,
    beta,
    r: sp.Symbol,
    x: sp.Symbol,
    Y: sp.Symbol,
    elliptic_relation: sp.Expr,
    timeout: float = 120,
) -> tuple[str, ...]:
    extensions = sp.symbols("a0:4") + sp.symbols("b0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("ub")
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
            inverse * (diagonal_b * extension)[0] - 1,
            elliptic_relation,
        )
    )

    eliminated = extensions + (inverse,)
    retained = shifts + (Y,)
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring R=(0,"
            + str(r)
            + ","
            + str(x)
            + "),("
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
                "Singular elliptic function-field projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    output = completed.stdout.replace("\r\n", "\n")
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def main() -> None:
    C, E, H = sp.symbols("C E H")
    U = C + H
    S = 1 + C * H
    T = H + C * E**2
    psi = (
        1
        + C * H
        - H**2
        - C**2 * E**2
        + C**2 * H**2
        - C * E**2 * H
    )
    assert sp.factor(psi - (S**2 - U * T)) == 0
    assert sp.factor(S - U - (C - 1) * (H - 1)) == 0
    assert sp.factor(S + U - (C + 1) * (H + 1)) == 0

    r, x, Y = sp.symbols("r x Y")
    denominator = x + r**2 - 1
    inverse = {
        H: (1 - x) / r,
        C: r * x / denominator,
        E: Y / (r * x),
    }
    cubic = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    elliptic_relation = Y**2 - cubic
    expected_multiplier = (
        ((x - 1) ** 2 - r**2)
        / (r**2 * x * denominator**2)
    )
    assert sp.factor(
        psi.subs(inverse) - expected_multiplier * elliptic_relation
    ) == 0

    # The odd valuation at x=0 proves that the quadratic extension is
    # nontrivial over Q(r,x).
    cubic_quotient = sp.factor(cubic / x)
    assert sp.factor(cubic_quotient.subs(x, 0) - (r**2 - 1) ** 2) == 0
    assert sp.factor(sp.discriminant(cubic, x)) == (
        r**4 * (r - 1) ** 4 * (r + 1) ** 4 * (4 * r**2 - 3)
    )
    assert elliptic_relation.subs({x: 0, Y: 0}) == 0
    assert sp.factor(elliptic_relation.subs({x: 1, Y: r**2})) == 0
    assert sp.factor(elliptic_relation.subs({x: 1, Y: -r**2})) == 0
    for sign in (1, -1):
        section = {
            symbol: sp.factor(
                inverse[symbol].subs({x: 1, Y: sign * r**2})
            )
            for symbol in (C, E, H)
        }
        assert section == {C: 1 / r, E: sign * r, H: 0}

    # Minimal Weierstrass/K3 invariants.
    a = 1 - r**2
    X, W = sp.symbols("X W")
    a2 = 3 * r**2 - 2
    a4 = a**3
    weierstrass = W**2 - X**3 - a2 * X**2 - a4 * X
    assert sp.factor(
        weierstrass.subs({X: a * x, W: a * Y})
        - a**2 * elliptic_relation
    ) == 0
    discriminant = sp.factor(16 * a4**2 * (a2**2 - 4 * a4))
    c4 = sp.factor(16 * (a2**2 - 3 * a4))
    assert discriminant == (
        16
        * r**4
        * (r - 1) ** 6
        * (r + 1) ** 6
        * (4 * r**2 - 3)
    )
    assert sp.factor(c4 - 16 * (3 * r**6 - 3 * r**2 + 1)) == 0

    s = sp.Symbol("s")
    infinity_a2 = 3 * s**2 - 2 * s**4
    infinity_a4 = s**2 * (s**2 - 1) ** 3
    infinity_discriminant = sp.factor(
        16 * infinity_a4**2 * (infinity_a2**2 - 4 * infinity_a4)
    )
    infinity_c4 = sp.factor(
        16 * (infinity_a2**2 - 3 * infinity_a4)
    )
    assert sp.factor(
        infinity_discriminant - s**24 * discriminant.subs(r, 1 / s)
    ) == 0
    assert sp.factor(infinity_discriminant / s**6).subs(s, 0) != 0
    assert sp.factor(infinity_c4 / s**2).subs(s, 0) != 0
    fibre_root_rank = 3 + 5 + 5 + 4
    fibre_euler_total = 4 + 6 + 6 + 1 + 1 + 6
    assert fibre_root_rank == 17
    assert fibre_euler_total == 24

    point_p = {X: a, W: a * r**2}
    point_2p = {
        X: a**2 / 4,
        W: -a**2 * (r**2 - 3) / 8,
    }
    assert sp.factor(weierstrass.subs(point_p)) == 0
    assert sp.factor(weierstrass.subs(point_2p)) == 0
    specialized_curve = sp.factor(weierstrass.subs(r, 2))
    assert specialized_curve == W**2 - X**3 - 10 * X**2 + 27 * X
    assert tuple(
        sp.factor(point_p[coordinate].subs(r, 2))
        for coordinate in (X, W)
    ) == (-3, -12)
    assert tuple(
        sp.factor(point_2p[coordinate].subs(r, 2))
        for coordinate in (X, W)
    ) == (sp.Rational(9, 4), sp.Rational(-9, 8))
    specialized_orders = {
        modulus: point_order_mod(
            ((-3) % modulus, (-12) % modulus),
            modulus,
        )
        for modulus in (5, 7)
    }
    assert specialized_orders == {5: 10, 7: 3}
    specialized_curve_orders = {
        modulus: curve_order_mod(modulus)
        for modulus in (5, 7, 11)
    }
    assert specialized_curve_orders == {5: 10, 7: 12, 11: 14}

    # Build the generic marked planes on the elliptic chart.
    t = sp.symbols("t0:4")
    u0 = (inverse[E], -1, -1, -inverse[E])
    u1 = (1, -1, 1, 1)
    y1 = (1, 0, 0, -1)
    y2 = (0, 1, -1, 0)
    k0 = (1, 0, 0, 1)
    k1 = (0, 1, 1, 0)
    x1 = (1, inverse[C] + 1, inverse[C] - 1, 1)
    x2 = (
        inverse[H] + inverse[E],
        1,
        1,
        inverse[H] - inverse[E],
    )
    alpha = (
        tuple(sp.factor(u0[j] + r * u1[j]) for j in range(4)),
        y1,
        y2,
        tuple(r * k0[j] - k1[j] for j in range(4)),
    )
    canonical_beta = (u1, x1, x2, k1)
    beta = tuple(
        tuple(
            sp.factor(
                canonical_beta[mode][coordinate]
                + t[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    pure_coefficients = {
        word: remainder_mod_quadratic(
            permanent(tuple(
                canonical_beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )),
            Y,
            elliptic_relation,
        )
        for word in WORDS
    }
    assert all(
        coefficient == 0
        for word, coefficient in pure_coefficients.items()
        if word != (1, 1, 1, 1)
    )
    expected_pure = sp.factor(
        -4
        * (x - 1 - r)
        * (x - 1 + r)
        / denominator
    )
    assert sp.factor(
        pure_coefficients[(1, 1, 1, 1)] - expected_pure
    ) == 0

    # Clear the rational row denominators before elimination.  These are
    # units in Q(r,x), so the marked plane bundle is unchanged after an
    # invertible reparameterization of the four marking coordinates.
    scaled_alpha = (
        tuple(sp.factor(r * x * entry) for entry in alpha[0]),
        alpha[1],
        alpha[2],
        alpha[3],
    )
    scaled_canonical_beta = (
        canonical_beta[0],
        tuple(
            sp.factor(denominator * entry)
            for entry in canonical_beta[1]
        ),
        tuple(
            sp.factor(r * x * entry)
            for entry in canonical_beta[2]
        ),
        canonical_beta[3],
    )
    scaled_beta = tuple(
        tuple(
            sp.factor(
                scaled_canonical_beta[mode][coordinate]
                + t[mode] * scaled_alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    projections = {
        distinguished: run_function_field_projection(
            distinguished,
            scaled_alpha,
            scaled_beta,
            r,
            x,
            Y,
            elliptic_relation,
        )
        for distinguished in range(4)
    }
    assert projections == EXPECTED_PROJECTIONS

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "rank-one conic bundle, elliptic function field, "
            "exact saturated binary projection"
        ),
        "normalized_chart": "A=B=F=1",
        "conic_bundle_identity": "Psi=S^2-U*T",
        "elliptic_equation": (
            "Y^2=x*((1-r^2)*x^2+(3*r^2-2)*x+(r^2-1)^2)"
        ),
        "quadratic_extension_irreducible": True,
        "finite_cubic_discriminant": (
            "r^4*(r-1)^4*(r+1)^4*(4*r^2-3)"
        ),
        "minimal_weierstrass_discriminant": (
            "16*r^4*(r-1)^6*(r+1)^6*(4*r^2-3)"
        ),
        "minimal_fibre_types": {
            "r=0": "I4",
            "r=1": "I6",
            "r=-1": "I6",
            "4*r^2=3": "I1+I1",
            "r=infinity": "I0*",
        },
        "minimal_resolution": "elliptic K3",
        "reducible_fibre_root_rank": fibre_root_rank,
        "fibre_euler_total": fibre_euler_total,
        "known_section_non_torsion": True,
        "non_torsion_good_reduction_orders": {
            str(key): value for key, value in specialized_orders.items()
        },
        "good_reduction_curve_orders": {
            str(key): value
            for key, value in specialized_curve_orders.items()
        },
        "picard_number": 20,
        "mordell_weil_rank": 1,
        "mordell_weil_torsion": "Z/2",
        "known_closed_sections": ["(1,r^2)", "(1,-r^2)"],
        "projection_plane_rows_denominator_cleared": True,
        "generic_relative_projection_ideals": {
            str(key): list(value) for key, value in projections.items()
        },
        "generic_binary_extension_exists": False,
        "generic_H31_fibre_empty": True,
        "survivor_projection_is_proper_closed_subset": True,
        "survivor_divisor_classified": False,
        "whole_second_component_closed": False,
        "all_pure_components_classified": False,
        "H31_globally_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            H0_THEOREM.name: sha256(H0_THEOREM),
            PURE_DIRECTION_THEOREM.name: sha256(PURE_DIRECTION_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_h31_diagonal_quadric_elliptic_generic_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
