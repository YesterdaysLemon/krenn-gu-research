#!/usr/bin/env python3
"""Verify the scoped GLD96 generic-R31 resultant localization.

The replay is exact over ``Q``.  It reconstructs the fixed GLD71 syndrome,
checks the raw R31 pivot and four selected seven-minors, and then specializes
the GLD88 F88 chart at ``(p,a)=(2,3)``.  On that exact Q6 fibre it computes the
four bordered Schur residuals in the two offsets ``B,C``, forms the first two
cross-resultants, and verifies a nonzero Q6 norm.  This specialization proves
that the corresponding generic resultant polynomial E31 is not identically
zero; the theorem localizes at E31 and does not silently claim that the
exceptional E31=0 locus is closed.

The GLD88-to-GLD95 consequence is recorded as an upstream dependency: after
the generic R31 residuals force ``B=C=0``, GLD95 excludes the resulting F88
point on its declared D(Delta) open.  This verifier does not re-run GLD95's
all-factor decomposition.  The R31=0/double-pivot branch, the exceptional
E31/H2/g0 strata, arbitrary H4 points outside F88, and the global conjecture
remain open.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD95_DOC = ROOT / "claims" / "arbitrary-order" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_EXCLUSION_THEOREM.md"
)

PIVOT_ROWS = (0, 1, 2, 17, 25, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
TARGETS = ((28, 8), (32, 2), (32, 5), (33, 8))

EXPECTED_RAW = {
    "pivot": {
        "denominator": "1",
        "terms": 289,
        "degrees": {"p": 8, "q": 8, "a": 2, "b": 2, "c": 0},
        "srepr_sha256": "48534ee25c536cbc4bfa36b126360a0479857cb3855d87ac9fd13b1e5e51cd32",
    },
    "28,8": {
        "denominator": "(p + q - 1)**3",
        "terms": 1268,
        "degrees": {"p": 11, "q": 11, "a": 2, "b": 2, "c": 1},
        "srepr_sha256": "ec46caa68329938274aca4330cdaddf562303eb6f220b6ff1f56cccf395a84b9",
    },
    "32,2": {
        "denominator": "(p + q - 1)**2",
        "terms": 1435,
        "degrees": {"p": 10, "q": 10, "a": 3, "b": 3, "c": 1},
        "srepr_sha256": "1a3a7ed2d5a75403be1f474c8d3d5355d5f3171f62ffe6c1d813caff75e83012",
    },
    "32,5": {
        "denominator": "(p + q - 1)**3",
        "terms": 2134,
        "degrees": {"p": 12, "q": 12, "a": 3, "b": 3, "c": 1},
        "srepr_sha256": "b21e118aaedaed1bb832f248f5cdae44498a28e5ef5ca40166d425f5e0f0512a",
    },
    "33,8": {
        "denominator": "(p + q - 1)**2",
        "terms": 850,
        "degrees": {"p": 10, "q": 10, "a": 2, "b": 2, "c": 1},
        "srepr_sha256": "726316fc7b1c76acb254793b271e9d77e655fda5333cef4643b4fe5c18fe14fb",
    },
}

EXPECTED_SUPPORT = ((1, 2), (1, 2, 3), (1, 2, 3), (1, 2))
EXPECTED_G_SUPPORT = (0, 1, 2)
EXPECTED_RESULTANT_COEFFICIENTS = (
    -905501121543829653519134583029125628170363723798877745648523367180968018033574358187,
    -581967626061819630034063550351650331374757486676325140922444735277204122667234925864,
    1965327315048008656313355784299314970407615267446169045708659903094610123987480161652,
    -1135825891000896384111550023303077198001706298129393658672106278421500353284383698011,
)
EXPECTED_RESULTANT_TUPLE_SHA256 = (
    "f0b2368dda1ea6a89d31ccf98242f48ed5d3540a14d412393b7870719780a05b"
)
EXPECTED_RESULTANT_NORM_FACTORS = {
    3: 6,
    5: 282,
    31: 2,
    173: 2,
    269: 1,
    1709: 1,
    20357: 2,
    270217: 2,
    52321: 1,
    475485394682070314208533: 1,
}
EXPECTED_G0 = (
    -sp.Integer(152501184) * sp.Symbol("q") ** 3
    + sp.Integer(255629952) * sp.Symbol("q") ** 2
    - sp.Integer(158823936) * sp.Symbol("q")
    + sp.Integer(30786048)
) / 3125
EXPECTED_G0_NORM_FACTORS = {2: 33, 3: 16, 5: 14, 110281: 1}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def q6_polynomial(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


def q_reduce(value: sp.Expr, variable: sp.Symbol, modulus: sp.Poly) -> sp.Expr:
    """Reduce a rational Q(variable)-expression in Q[variable]/(modulus)."""

    numerator, denominator = sp.cancel(value).as_numer_denom()
    numerator_poly = sp.Poly(numerator, variable, domain=QQ).rem(modulus)
    denominator_poly = sp.Poly(denominator, variable, domain=QQ).rem(modulus)
    assert not denominator_poly.is_zero, "a cleared denominator vanished mod Q6"
    inverse = sp.invert(denominator_poly, modulus)
    return sp.cancel((numerator_poly * inverse).rem(modulus).as_expr())


def raw_digest(
    expression: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    key: str,
) -> dict[str, object]:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    polynomial = sp.Poly(numerator, *variables, domain=QQ)
    metadata = {
        "denominator": str(sp.factor(denominator)),
        "terms": len(polynomial.terms()),
        "degrees": {
            str(variable): polynomial.degree(variable) for variable in variables
        },
        "srepr_sha256": hashlib.sha256(sp.srepr(numerator).encode()).hexdigest(),
    }
    assert metadata == EXPECTED_RAW[key], (key, metadata, EXPECTED_RAW[key])
    return metadata


def build_data():
    gld71 = load_module(GLD71, "gld71_for_gld96_primary")
    gld88 = load_module(GLD88, "gld88_for_gld96_primary")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37
    p, q, a, b, c = sp.symbols("p q a b c")
    leaf = sp.Matrix(
        [
            [1, 1, 1],
            [p, q, (p + q - p * q) / (p + q - 1)],
            [a, 1 + b, 1 + c],
        ]
    )
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    assert syndrome.shape == (37, 9)
    return gld88, syndrome, (p, q, a, b, c)


def check_raw_chart(syndrome, variables):
    p, q, a, b, c = variables
    all_variables = (p, q, a, b, c)
    pivot = syndrome.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    pivot_determinant = sp.cancel(pivot.det(method="domain-ge"))
    raw = {"pivot": raw_digest(pivot_determinant, all_variables, "pivot")}
    pivot_numerator = pivot_determinant.as_numer_denom()[0]
    d0 = p + q - 1
    assert sp.cancel(pivot_numerator / (2 * (p - q) * d0)).is_polynomial(
        p, q, a, b, c
    )
    assert sp.cancel(pivot_numerator / (2 * (p - q) * d0)) != 0
    for row, column in TARGETS:
        key = f"{row},{column}"
        determinant = sp.cancel(
            syndrome.extract((*PIVOT_ROWS, row), (*PIVOT_COLUMNS, column)).det(
                method="domain-ge"
            )
        )
        raw[key] = raw_digest(determinant, all_variables, key)
    return raw


def check_f88_kernel(syndrome, gld88, variables):
    """Check the exact GLD88 common block kernel used for B-divisibility."""

    p, q, a, b, c = variables
    family = gld88.h4_family(p, q, a)
    kernel = sp.Matrix([family["u"], family["v"], 1])
    f88_syndrome = syndrome.subs({b: family["b"], c: family["c"]}).applyfunc(
        sp.cancel
    )
    count = 0
    for block in range(3):
        for value in f88_syndrome[:, 3 * block : 3 * block + 3] * kernel:
            assert sp.cancel(value) == 0
            count += 1
    assert count == 111
    return {
        "identity_count": count,
        "kernel": [str(family["u"]), str(family["v"]), "1"],
    }


def residual_data(syndrome, gld88, variables):
    p, q, a, b, c = variables
    B, C = sp.symbols("B C")
    family = gld88.h4_family(p, q, a)
    specialized_family = {
        name: sp.cancel(value.subs({p: 2, a: 3}))
        for name, value in family.items()
    }
    specialized = syndrome.subs(
        {
            p: 2,
            a: 3,
            b: specialized_family["b"] + B,
            c: specialized_family["c"] + C,
        }
    ).applyfunc(sp.cancel)
    pivot = specialized.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    pivot_determinant = sp.cancel(pivot.det(method="domain-ge"))
    adjugate = pivot.adjugate(method="domain-ge")
    q = variables[1]
    q6 = sp.Poly(q6_polynomial(sp.Integer(2), q), q, domain=QQ)

    parsed: list[tuple[sp.Expr, sp.Expr]] = []
    residual_metadata = []
    for row, column in TARGETS:
        schur = sp.cancel(
            pivot_determinant * specialized[row, column]
            - sum(
                specialized[row, PIVOT_COLUMNS[i]]
                * adjugate[i, j]
                * specialized[PIVOT_ROWS[j], column]
                for i in range(6)
                for j in range(6)
            )
        )
        numerator, denominator = schur.as_numer_denom()
        assert not denominator.has(B, C)
        polynomial = sp.Poly(numerator, B, C, domain=QQ.frac_field(q))
        coefficients: dict[tuple[int, int], sp.Expr] = {}
        for monomial, coefficient in polynomial.terms():
            reduced = q_reduce(coefficient / denominator, q, q6)
            if reduced != 0:
                coefficients[monomial] = reduced
        assert all(c_exp in (0, 1) for _b_exp, c_exp in coefficients)
        assert all(
            b_exp >= 1 for (b_exp, c_exp) in coefficients if c_exp == 0
        )
        f = sp.Add(
            *(coefficient * B**b_exp for (b_exp, c_exp), coefficient in coefficients.items() if c_exp == 0)
        )
        g = sp.Add(
            *(coefficient * B**b_exp for (b_exp, c_exp), coefficient in coefficients.items() if c_exp == 1)
        )
        expected_f_support = EXPECTED_SUPPORT[len(parsed)]
        assert tuple(sorted(sp.Poly(f, B).monoms(), reverse=False)) == tuple(
            (exponent,) for exponent in expected_f_support
        )
        assert tuple(sorted(sp.Poly(g, B).monoms(), reverse=False)) == tuple(
            (exponent,) for exponent in EXPECTED_G_SUPPORT
        )
        assert len(coefficients) == len(expected_f_support) + len(EXPECTED_G_SUPPORT)
        parsed.append((sp.cancel(f), sp.cancel(g)))
        residual_metadata.append(
            {
                "target": [row, column],
                "support_B_only": list(expected_f_support),
                "support_C": list(EXPECTED_G_SUPPORT),
                "term_count": len(coefficients),
            }
        )

    # Cross-multiplication removes C and is divisible by B because every f_i
    # is.  The quotient is formed after Q6 reduction, so this is an identity
    # in the exact finite Q6 algebra, not a floating-point specialization.
    cross_residuals = []
    for index in (1, 2):
        f0, g0 = parsed[0]
        fi, gi = parsed[index]
        cross = sp.Poly(
            sp.expand(f0 * gi - fi * g0), B, domain=QQ.frac_field(q)
        )
        assert q_reduce(cross.nth(0), q, q6) == 0
        quotient = sp.Add(
            *(
                q_reduce(cross.nth(power + 1), q, q6) * B**power
                for power in range(cross.degree())
            )
        )
        quotient = sp.cancel(quotient)
        assert sp.Poly(quotient, B, domain=QQ.frac_field(q)).degree() == 4
        cross_residuals.append(quotient)

    resultant = sp.resultant(cross_residuals[0], cross_residuals[1], B)
    reduced_resultant = q_reduce(resultant, q, q6)
    primitive = sp.Poly(reduced_resultant, q, domain=QQ).primitive()[1]
    coefficients = tuple(int(value) for value in primitive.all_coeffs())
    assert coefficients == EXPECTED_RESULTANT_COEFFICIENTS
    assert hashlib.sha256(repr(coefficients).encode()).hexdigest() == EXPECTED_RESULTANT_TUPLE_SHA256
    norm = int(sp.resultant(q6.as_expr(), primitive.as_expr(), q))
    assert norm != 0
    assert sp.factorint(abs(norm)) == EXPECTED_RESULTANT_NORM_FACTORS

    first_g0 = sp.cancel(q_reduce(parsed[0][1].subs(B, 0), q, q6))
    expected_g0 = EXPECTED_G0.subs({sp.Symbol("q"): q})
    assert first_g0 == expected_g0
    g0_num, g0_den = first_g0.as_numer_denom()
    g0_norm = int(sp.resultant(q6.as_expr(), g0_num, q))
    assert g0_norm != 0
    assert sp.factorint(abs(g0_norm)) == EXPECTED_G0_NORM_FACTORS

    return {
        "specialization": {"p": 2, "a": 3, "q6": str(q6.as_expr())},
        "residuals": residual_metadata,
        "cross_resultants": {
            "pairs": [[0, 1], [0, 2]],
            "B_degrees": [4, 4],
            "reduced_Q6_primitive_coefficients": list(coefficients),
            "primitive_tuple_sha256": EXPECTED_RESULTANT_TUPLE_SHA256,
            "Q6_norm_factorization": EXPECTED_RESULTANT_NORM_FACTORS,
        },
        "g0": {
            "reduced_value": str(first_g0),
            "numerator_norm_factorization": EXPECTED_G0_NORM_FACTORS,
            "denominator": str(g0_den),
        },
    }


def check() -> dict[str, object]:
    started = time.monotonic()
    gld88, syndrome, variables = build_data()
    raw = check_raw_chart(syndrome, variables)
    kernel = check_f88_kernel(syndrome, gld88, variables)
    specialization = residual_data(syndrome, gld88, variables)
    p, q, _a, _b, _c = variables
    d0 = p + q - 1
    delta = (
        (p - q)
        * d0
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * (2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2)
    )
    h2 = 2 * p**2 - 2 * p + 1
    assert GLD95_DOC.is_file()
    assert "GLD95" in GLD95_DOC.read_text(encoding="utf-8")
    return {
        "status": "exact_scoped_generic_R31_resultant_localization",
        "gld_identifier": "GLD96",
        "field": "Q_characteristic_zero_then_C",
        "global_conjecture": "UNRESOLVED",
        "scope": (
            "normalized equal-leaf H4 Q6 chart on the R31 pivot open, after "
            "localization at E31, H2, g0, and Delta; the conclusion is the "
            "GLD88 F88 reduction followed by the GLD95 exclusion"
        ),
        "syndrome_shape": list(syndrome.shape),
        "R31": {
            "rows": list(PIVOT_ROWS),
            "columns": list(PIVOT_COLUMNS),
            "raw_replay": raw,
            "raw_factor_contains": "2*(p-q)*(p+q-1)",
        },
        "GLD88_F88_kernel": kernel,
        "localization": {
            "open": "D(R31*E31*H2*g0*Delta)",
            "Delta": str(delta),
            "H2": str(h2),
            "E31_definition": (
                "cleared q-norm/resultant of Res_B(H01,H02), where "
                "H_ij=(f_i*g_j-f_j*g_i)/B in Q(p,a)[q]/(Q6)"
            ),
            "g0_definition": (
                "cleared q-norm of the C-coefficient g_0(B=0) of the first "
                "R31 Schur residual"
            ),
        },
        "specialized_nonzero_witness": specialization,
        "implication": (
            "On D(R31*E31*H2*g0*Delta), rank-at-most-six plus Q6 forces "
            "B=C=0, hence the written F88 family; GLD95 then excludes the "
            "F88 incidence on D(Omega*Delta)."
        ),
        "exceptional_strata": [
            "R31=0, including the unresolved double-pivot branch",
            "E31=0 or g0=0, where this residual localization is silent",
            "H2=2*p^2-2*p+1=0, where q-leading-coefficient division is invalid",
            "Delta=0 (p-q, d0, P, L1, L2, or e), handled only by the separately scoped GLD87/89/93/94 results where applicable",
            "arbitrary H4 intersect V(Q6) points outside the GLD88 F88 family",
            "the GLD83 pulled-back Fitting ideal, other charts/components/source branches, and global resolution",
        ],
        "upstream": {
            "GLD88": "forces F88 on its own declared principal open",
            "GLD95": "excludes V(Q6) common minors on F88 intersect D(Delta), including old P6=0 content fibres",
            "GLD95_replayed_here": False,
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("GLD96 generic R31 resultant localization verifier: PASS")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
