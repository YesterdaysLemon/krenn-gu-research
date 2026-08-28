#!/usr/bin/env python3
"""Verify the scoped GLD92 dense exclusion on the H4/Q6 boundary.

The verifier reconstructs the fixed 37-row GLD71 syndrome on the GLD88
equal-leaf H4 family, evaluates two alternative six-row minors exactly over
Q, and proves that their nonzero principal opens cover the Q6 divisor away
from a finite common-minor residual.  It deliberately does not enumerate or
exclude that residual, and it does not address the other H4 boundaries or
the global Krenn--Gu obligation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
MINOR_ROWS = {
    "M_28": (0, 1, 2, 17, 25, 28),
    "M_31": (0, 1, 2, 17, 25, 31),
}
EXPECTED_NUMERATOR_SREPR_SHA256 = {
    "M_28": "55bfba7b569752acb072ad0922d273e55d70651782e93394a14f9c23098727b8",
    "M_31": "352948a2c113f32f10b90520592cb266cb455853297a664964478fdd7369b18f",
}
EXPECTED_Q6_REMAINDER_SREPR_SHA256 = {
    "M_28": "8efab099320d2e498167c86999ac90adfeb85f2d80d3bd1f4b4e7539577298ef",
    "M_31": "b05d58c3177d7d0c8ea1b54cf7931f0a8e73b314518c748031f9be847d331912",
}
EXPECTED_RESULTANT_SREPR_SHA256 = (
    "fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d"
)
EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256 = (
    "0057c78ceea5241553d856ce437f0fb4fd77571c8205eaa96c7c13dce54cec42"
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_polynomial_digest(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> tuple[str, int]:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=sp.QQ)
    encoded = [
        [list(monomial), int(coefficient.p), int(coefficient.q)]
        for monomial, coefficient in polynomial.terms()
    ]
    payload = json.dumps(encoded, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), len(encoded)


def q6_polynomial(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2
        - 2 * p**4 * q
        + p**4
        + 2 * p**3 * q**3
        - 7 * p**3 * q**2
        + 5 * p**3 * q
        - 2 * p**3
        + 2 * p**2 * q**4
        - 7 * p**2 * q**3
        + 12 * p**2 * q**2
        - 7 * p**2 * q
        + 2 * p**2
        - 2 * p * q**4
        + 5 * p * q**3
        - 7 * p * q**2
        + 2 * p * q
        + q**4
        - 2 * q**3
        + 2 * q**2
    )


def exact_minor(
    syndrome: sp.Matrix,
    rows: tuple[int, ...],
    p: sp.Symbol,
    q: sp.Symbol,
    a: sp.Symbol,
    q6: sp.Expr,
) -> dict[str, object]:
    determinant = sp.cancel(
        syndrome.extract(rows, PIVOT_COLUMNS).det(method="domain-ge")
    )
    numerator, denominator = determinant.as_numer_denom()
    numerator = sp.expand(numerator)
    denominator = sp.factor(denominator)
    numerator_poly = sp.Poly(numerator, p, q, a, domain=sp.QQ)
    q6_poly = sp.Poly(q6, q, domain=sp.QQ.frac_field(p, a))
    numerator_in_q = sp.Poly(
        numerator, q, domain=sp.QQ.frac_field(p, a)
    )
    _quotient, remainder = sp.div(numerator_in_q, q6_poly)
    remainder_expr = sp.expand(remainder.as_expr())
    factors = sp.factor_list(numerator)[1]
    numerator_digest = hashlib.sha256(
        sp.srepr(numerator).encode()
    ).hexdigest()
    assert numerator_digest == EXPECTED_NUMERATOR_SREPR_SHA256[
        "M_28" if rows == MINOR_ROWS["M_28"] else "M_31"
    ]
    remainder_digest = hashlib.sha256(
        sp.srepr(remainder_expr).encode()
    ).hexdigest()
    key = "M_28" if rows == MINOR_ROWS["M_28"] else "M_31"
    assert remainder_digest == EXPECTED_Q6_REMAINDER_SREPR_SHA256[key]
    return {
        "rows": list(rows),
        "numerator": numerator,
        "denominator": denominator,
        "numerator_total_degree": numerator_poly.total_degree(),
        "numerator_degree_a": sp.Poly(numerator, a).degree(),
        "numerator_degree_q": sp.Poly(numerator, q).degree(),
        "numerator_srepr_sha256": numerator_digest,
        "numerator_canonical_sha256": canonical_polynomial_digest(
            numerator, (p, q, a)
        )[0],
        "numerator_terms": len(numerator_poly.terms()),
        "factor_degrees": [
            sp.Poly(factor, p, q, a).total_degree()
            for factor, _exponent in factors
        ],
        "factor_exponents": [
            exponent for _factor, exponent in factors
        ],
        "q6_remainder": remainder_expr,
        "q6_remainder_degree_q": sp.Poly(remainder_expr, q).degree(),
        "q6_remainder_srepr_sha256": remainder_digest,
        "q6_divides_numerator": remainder.is_zero,
    }


def check() -> dict[str, object]:
    gld71 = load_module(GLD71, "gld71_for_gld92_primary")
    gld88 = load_module(GLD88, "gld88_for_gld92_primary")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37

    p, q, a = sp.symbols("p q a")
    family = gld88.h4_family(p, q, a)
    leaf = sp.Matrix(
        [
            [1, 1, 1],
            [p, q, family["s"]],
            [a, 1 + family["b"], 1 + family["c"]],
        ]
    )
    syndrome = gld71.coefficient_matrix(
        parent, relations, (leaf, leaf, leaf)
    )
    assert syndrome.shape == (37, 9)

    d0 = p + q - 1
    pnorm = p**2 - p + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    delta = (p - q) * d0 * pnorm * l1 * l2 * e
    omega_leaf_factor = -3 * a + p + 1
    q6 = q6_polynomial(p, q)

    # GLD88's common block-kernel formula is checked on the reconstructed
    # matrix.  This gives rank <= 6 before either alternative six-minor is
    # invoked, and records the exact bridge used by the theorem.
    kernel = sp.Matrix([family["u"], family["v"], 1])
    block_kernel_identity_count = 0
    for block_index in range(3):
        block = syndrome[:, 3 * block_index : 3 * block_index + 3]
        for value in block * kernel:
            assert sp.cancel(value) == 0
            block_kernel_identity_count += 1

    minor_data = {
        key: exact_minor(syndrome, rows, p, q, a, q6)
        for key, rows in MINOR_ROWS.items()
    }
    assert minor_data["M_28"]["factor_degrees"] == [1, 20]
    assert minor_data["M_28"]["factor_exponents"] == [3, 1]
    assert minor_data["M_31"]["factor_degrees"] == [1, 1, 18]
    assert minor_data["M_31"]["factor_exponents"] == [1, 3, 1]
    expected_denominator = pnorm**2 * e**2
    for data in minor_data.values():
        assert sp.cancel(data["denominator"] - expected_denominator) == 0
        assert data["q6_divides_numerator"] is False

    n28 = minor_data["M_28"]["numerator"]
    n31 = minor_data["M_31"]["numerator"]
    assert sp.rem(
        sp.Poly(n28, p, q, a), sp.Poly((p - q) ** 3, p, q, a)
    ).is_zero
    assert sp.rem(
        sp.Poly(n31, p, q, a),
        sp.Poly((p + q - 1) * (p - q) ** 3, p, q, a),
    ).is_zero
    f28 = sp.cancel(n28 / (p - q) ** 3)
    f31 = sp.cancel(n31 / ((p + q - 1) * (p - q) ** 3))
    f28_factors = sp.factor_list(f28)[1]
    f31_factors = sp.factor_list(f31)[1]
    assert len(f28_factors) == 1
    assert len(f31_factors) == 1
    assert f28_factors[0][1] == 1
    assert f31_factors[0][1] == 1
    assert sp.Poly(f28_factors[0][0], p, q, a).total_degree() == 20
    assert sp.Poly(f31_factors[0][0], p, q, a).total_degree() == 18

    q6_factors = sp.factor_list(q6, p, q)[1]
    assert len(q6_factors) == 1
    assert q6_factors[0][1] == 1
    assert sp.Poly(q6_factors[0][0], p, q).total_degree() == 6
    q6_plane_poly = sp.Poly(q6, p, q, domain=sp.QQ)
    for open_factor in (p - q, d0, pnorm, l1, l2, e):
        assert sp.gcd(
            q6_plane_poly, sp.Poly(open_factor, p, q, domain=sp.QQ)
        ).total_degree() == 0

    # First rule out a hidden vertical a-line in the common residual.  Such a
    # line would make every coefficient of both F-polynomials vanish at one
    # (p,q).  The exact lex certificate below is small: the base ideal is
    # zero-dimensional, its q eliminant is q^6*(q^2-q+1)^4, and the sixth
    # power of (p-q)*P lies in that ideal.  Hence every vertical base point
    # is already outside D(Delta).
    vertical_equations = [q6]
    for expression in (f28, f31):
        vertical_equations.extend(sp.Poly(expression, a).all_coeffs())
    vertical_basis = sp.groebner(
        vertical_equations, p, q, order="lex"
    )
    vertical_eliminant = sp.factor(vertical_basis.polys[-1].as_expr())
    assert vertical_basis.is_zero_dimensional
    assert vertical_eliminant == q**6 * (q**2 - q + 1) ** 4
    vertical_product = (p - q) * pnorm
    assert vertical_basis.reduce(vertical_product**6)[1] == 0

    # The resultant is computed before any specialization.  Its coprimality
    # with the irreducible Q6 certifies that F28 and F31 have no common
    # component dominating the Q6 curve.  Together with the vertical-fibre
    # certificate, it makes the residual finite on D(Delta).  It intentionally
    # does not claim that this finite intersection is empty.
    resultant = sp.resultant(f28, f31, a)
    resultant_poly = sp.Poly(resultant, p, q, domain=sp.QQ)
    resultant_digest = hashlib.sha256(
        sp.srepr(resultant).encode()
    ).hexdigest()
    assert resultant_digest == EXPECTED_RESULTANT_SREPR_SHA256
    q6_as_poly = sp.Poly(q6, p, q, domain=sp.QQ)
    resultant_gcd = sp.gcd(resultant_poly, q6_as_poly)
    assert resultant_gcd.total_degree() == 0
    assert sp.factor(resultant_gcd.as_expr()) in (1, -1)
    resultant_in_q = sp.Poly(
        resultant, q, domain=sp.QQ.frac_field(p)
    )
    q6_in_q = sp.Poly(q6, q, domain=sp.QQ.frac_field(p))
    _resultant_quotient, resultant_remainder = sp.div(
        resultant_in_q, q6_in_q
    )
    # Keep the SymPy remainder's native expression tree for the pinned
    # compatibility digest; the exact nonzero test is representation-free.
    resultant_remainder_expr = resultant_remainder.as_expr()
    resultant_remainder_digest = hashlib.sha256(
        sp.srepr(resultant_remainder_expr).encode()
    ).hexdigest()
    assert (
        resultant_remainder_digest
        == EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256
    )
    assert not resultant_remainder.is_zero

    # The family is genuinely in the leaf-determinant open away from its
    # declared factor; no new denominator or affine zero-block is silently
    # removed here.  The factor is retained as an explicit GLD88 residual.
    leaf_determinant = sp.factor(sp.cancel(leaf.det()))
    expected_leaf_determinant = sp.factor(
        -(
            (p - q)
            * omega_leaf_factor
            * l1
            * l2
        )
        / (d0 * pnorm * e)
    )
    assert sp.cancel(leaf_determinant - expected_leaf_determinant) == 0

    return {
        "status": "exact_scoped_H4_Q6_dense_minor_exclusion",
        "gld_identifier": "GLD92",
        "field": "Q_characteristic_zero_then_C",
        "global_conjecture": "UNRESOLVED",
        "syndrome_shape": list(syndrome.shape),
        "pivot_columns": list(PIVOT_COLUMNS),
        "minor_rows": {key: list(value) for key, value in MINOR_ROWS.items()},
        "common_block_kernel_identity_count": block_kernel_identity_count,
        "rank_at_most_six_on_GLD88_family": True,
        "q6": {
            "total_degree": 6,
            "irreducible_over_Q": True,
            "factor_degrees": [
                sp.Poly(factor, p, q).total_degree()
                for factor, _exponent in q6_factors
            ],
            "factor_exponents": [
                exponent for _factor, exponent in q6_factors
            ],
            "Delta_factor_gcds_are_one": True,
        },
        "delta": str(delta),
        "leaf_determinant": str(leaf_determinant),
        "minor_data": {
            key: {
                field: value
                for field, value in data.items()
                if field not in {"numerator", "q6_remainder"}
            }
            for key, data in minor_data.items()
        },
        "stripped_minor_degrees": {
            "F28_total_degree": sp.Poly(f28, p, q, a).total_degree(),
            "F28_degree_a": sp.Poly(f28, a).degree(),
            "F31_total_degree": sp.Poly(f31, p, q, a).total_degree(),
            "F31_degree_a": sp.Poly(f31, a).degree(),
        },
        "vertical_fibre_certificate": {
            "coefficient_equation_count": len(vertical_equations),
            "zero_dimensional_base_ideal": True,
            "q_eliminant": str(vertical_eliminant),
            "delta_product": "(p-q)*(p**2-p+1)",
            "delta_product_power_in_ideal": 6,
            "conclusion": "all vertical common-minor fibres lie outside D(Delta)",
        },
        "resultant": {
            "eliminated_variable": "a",
            "total_degree": resultant_poly.total_degree(),
            "degree_q": resultant_in_q.degree(),
            "srepr_sha256": resultant_digest,
            "gcd_with_Q6": str(resultant_gcd.as_expr()),
            "q6_divides_resultant": False,
            "q6_remainder_degree_q": resultant_remainder.degree(),
            "q6_remainder_srepr_sha256": resultant_remainder_digest,
        },
        "dense_open": "D(F28) union D(F31) inside V(Q6) intersect D(Omega*Delta)",
        "finite_common_locus_residual": (
            "V(Q6,F28,F31) intersect D(Omega*Delta) with denominator and "
            "leaf-determinant factors retained; not enumerated or excluded"
        ),
        "remaining_boundaries": [
            "V(Q6,F28,F31) finite common-minor residual",
            "L1=0",
            "L2=0",
            "e=0",
            "other H4 charts/components/gauges/source branches",
            "GLD83 Fitting pullback and global Krenn-Gu closure",
        ],
        "global_conjecture_resolved": False,
    }


def main() -> None:
    result = check()
    print("GLD92 H4 Q6 dense minor exclusion verifier: PASS")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
