#!/usr/bin/env python3
"""Durable comparison-only GLD103 physical-generator checker.

The primary verifier does not import this helper.  It compares the primary
Q6-reduced D145 representation and whole-P_i normalization with the
independently implemented tracked audit at F4 and p^2-2p+2, checking one
nonzero K-unit per P_i, an exact localizer, and matching exact Macaulay
rank/membership.  It is provenance/review evidence, not a theorem
certificate or an acceptance dependency.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
PRIMARY = ROOT / "claims" / "arbitrary-order" / "verify_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion.py"
AUDIT = ROOT / "claims" / "arbitrary-order" / "audit_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def primary_k_expr(value, module) -> sp.Expr:
    text = str(value).replace("^", "**").replace("x", "p")
    return sp.expand(sp.sympify(text, locals={"p": module.p}))


def audit_k_expr(value, module) -> sp.Expr:
    return sp.expand(sp.sympify(str(value.poly.as_expr()), locals={"p": module.p}))


def reduce_k(value: object, factor: sp.Expr, module) -> sp.Expr:
    numerator, denominator = sp.cancel(sp.sympify(value)).as_numer_denom()
    modulus = sp.Poly(factor, module.p, domain=QQ)
    n = sp.Poly(numerator, module.p, domain=QQ).rem(modulus)
    d = sp.Poly(denominator, module.p, domain=QQ).rem(modulus)
    if d.is_zero:
        raise AssertionError(("scalar denominator vanishes on factor", value, factor))
    return (n * sp.invert(d, modulus)).rem(modulus).as_expr()


def primary_map(poly, module):
    return {
        tuple(monomial): [primary_k_expr(value, module) for value in coefficients]
        for monomial, coefficients in poly.items()
    }


def audit_map(poly, module):
    return {
        tuple(monomial): [audit_k_expr(value, module) for value in coefficients]
        for monomial, coefficients in poly.items()
    }


def maps_equal(left, right, factor: sp.Expr, module) -> bool:
    for monomial in sorted(set(left) | set(right)):
        left_values = left.get(monomial, [sp.Integer(0)] * 4)
        right_values = right.get(monomial, [sp.Integer(0)] * 4)
        for left_value, right_value in zip(left_values, right_values):
            if reduce_k(left_value - right_value, factor, module) != 0:
                return False
    return True


def canonical_hash(poly, factor: sp.Expr, module) -> str:
    payload = []
    for monomial in sorted(poly):
        payload.append(
            [
                list(monomial),
                [sp.srepr(reduce_k(value, factor, module)) for value in poly[monomial]],
            ]
        )
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()


def unit_relation(primary_poly, audit_poly, factor: sp.Expr, module):
    for monomial in sorted(set(primary_poly) | set(audit_poly)):
        left_values = primary_poly.get(monomial, [sp.Integer(0)] * 4)
        right_values = audit_poly.get(monomial, [sp.Integer(0)] * 4)
        for left_value, right_value in zip(left_values, right_values):
            left_value = reduce_k(left_value, factor, module)
            right_value = reduce_k(right_value, factor, module)
            if left_value == 0 and right_value == 0:
                continue
            if left_value == 0 or right_value == 0:
                raise AssertionError(("generator support mismatch", monomial))
            scalar = reduce_k(left_value / right_value, factor, module)
            if scalar == 0:
                raise AssertionError(("zero generator scalar", monomial))
            scaled = {
                term: [scalar * value for value in values]
                for term, values in audit_poly.items()
            }
            if not maps_equal(primary_poly, scaled, factor, module):
                raise AssertionError(("generator is not a K-unit multiple", monomial))
            return scalar, scaled
    raise AssertionError("zero physical generator")


def matrix_record(primary_matrix, audit_membership, audit_columns, audit_metadata):
    primary = {
        key: primary_matrix[key]
        for key in (
            "bound", "monomial_count", "columns", "row_count",
            "q_basis_multiplier_count", "rank", "rank_with_target",
            "target_in_span", "input_matrix_sha256", "rref_matrix_sha256",
            "target_residual_sha256",
        )
    }
    audit = {
        "columns": audit_columns,
        "row_count": audit_metadata["row_count"],
        "q_shift_count": audit_metadata["q_shift_count"],
        "rank": audit_membership["rank"],
        "rank_with_target": audit_membership["rank_with_target"],
        "target_in_span": audit_membership["target_in_span"],
        "row_matrix_sha256": audit_metadata["row_matrix_sha256"],
    }
    return {
        "primary": primary,
        "audit": audit,
        "same_rank_and_membership": (
            primary["rank"] == audit["rank"]
            and primary["rank_with_target"] == audit["rank_with_target"]
            and primary["target_in_span"] == audit["target_in_span"]
            and primary["columns"] == audit["columns"]
            and primary["row_count"] == audit["row_count"]
        ),
        "row_space_equal_by_nonzero_generator_units": True,
        "internal_hashes_are_implementation_specific": True,
    }


def compare_factor(primary, audit, primary_bridge, audit_bridge, factor_name: str):
    factor, field, quotient = primary._factor_quotient(factor_name, True)
    primary_p, primary_metadata = primary._p_values_to_multivariate(
        primary_bridge["_p_values"], primary_bridge["_algebra"], factor_name, field, quotient
    )
    primary_delta, _delta_metadata = primary._delta_specialization(factor_name, field, quotient)
    primary_localizer = {
        (0, 1, 1): primary_delta,
        (0, 0, 0): quotient.neg(quotient.one),
    }

    pfield = audit.ResidueField(audit._factor_expression(factor_name))
    qfield = audit.QuotientResidueField(pfield, audit.q6_expression(audit.p, audit.q))
    audit_generators = audit._physical_generators(audit_bridge["p_values"], qfield)
    audit_p = audit_generators[:-1]
    audit_localizer = audit_generators[-1]
    factor_expr = sp.sympify(str(factor.as_expr()), locals={"p": primary.p})

    generators = []
    for index, (primary_generator, audit_generator) in enumerate(zip(primary_p, audit_p)):
        pmap = primary_map(primary_generator, primary)
        amap = audit_map(audit_generator, primary)
        scalar, scaled_audit = unit_relation(pmap, amap, factor_expr, primary)
        generators.append(
            {
                "P_index": index,
                "scalar_primary_over_audit_in_K": str(scalar),
                "scalar_nonzero_on_factor": scalar != 0,
                "equal_after_one_K_unit_rescaling": maps_equal(
                    pmap, scaled_audit, factor_expr, primary
                ),
                "primary_generator_hash": primary._hash_multivariate_poly(primary_generator),
                "audit_generator_hash": audit._a_generator_hash(audit_generator),
                "canonical_hash_after_rescaling": canonical_hash(pmap, factor_expr, primary),
                "canonical_audit_hash_after_rescaling": canonical_hash(
                    scaled_audit, factor_expr, primary
                ),
                "primary_normalization": primary_metadata[index],
            }
        )

    primary_localizer_map = primary_map(primary_localizer, primary)
    audit_localizer_map = audit_map(audit_localizer, primary)
    localizer_equal = maps_equal(
        primary_localizer_map, audit_localizer_map, factor_expr, primary
    )
    localizer_scalar, _scaled_localizer = unit_relation(
        primary_localizer_map, audit_localizer_map, factor_expr, primary
    )
    primary_matrix = primary._multivariate_macaulay(
        [*primary_p, primary_localizer], 3, quotient
    )
    audit_membership, audit_columns, audit_metadata = audit._physical_rank(
        audit_bridge["p_values"], factor_name, 3
    )
    return {
        "factor": factor_name,
        "generators": generators,
        "all_generators_unit_related": all(
            item["scalar_nonzero_on_factor"]
            and item["equal_after_one_K_unit_rescaling"]
            and item["canonical_hash_after_rescaling"]
            == item["canonical_audit_hash_after_rescaling"]
            for item in generators
        ),
        "localizer": {
            "exact_equal": localizer_equal,
            "scalar_primary_over_audit_in_K": str(localizer_scalar),
            "primary_canonical_hash": canonical_hash(
                primary_localizer_map, factor_expr, primary
            ),
            "audit_canonical_hash": canonical_hash(
                audit_localizer_map, factor_expr, primary
            ),
            "primary_hash": primary._hash_multivariate_poly(primary_localizer),
            "audit_hash": audit._a_generator_hash(audit_localizer),
        },
        "row_space_reconciliation": matrix_record(
            primary_matrix, audit_membership, audit_columns, audit_metadata
        ),
    }


def compare_d145(primary, audit, primary_bridge, audit_bridge):
    primary_algebra = primary_bridge["_algebra"]
    audit_algebra = audit_bridge["algebra"]
    primary_expression = primary_algebra.as_expr(primary_bridge["_determinants"]["D145"])
    audit_expression = audit_algebra.as_expr(audit_bridge["determinants"]["D145"])
    primary_terms, primary_metadata = primary._integer_sparse_polynomial(primary_expression)
    audit_terms, audit_metadata = audit._integer_sparse(audit_expression)
    difference = sp.expand(primary_expression - audit_expression)
    ratio = sp.cancel(primary_expression / audit_expression)
    return {
        "scope": "current Q6-reduced D145 expression",
        "expression_equal": difference == 0,
        "expression_difference": str(difference),
        "ratio": str(ratio),
        "raw_term_maps_equal": primary_terms == audit_terms,
        "primary_q6_srepr_sha256": primary.EXPECTED_Q6_SREPR_SHA256,
        "audit_q6_srepr_sha256": audit.EXPECTED_Q6_SREPR_SHA256,
        "primary_terms_sha256": primary_metadata["terms_sha256"],
        "audit_terms_sha256": audit_metadata["terms_sha256"],
        "primary_term_count": primary_metadata["term_count"],
        "audit_term_count": audit_metadata["term_count"],
        "primary_rational_content": primary_metadata["rational_content"],
        "audit_rational_content": audit_metadata["rational_content"],
        "primary_denominator": primary_metadata["denominator"],
        "audit_denominator": audit_metadata["denominator"],
    }


def main() -> int:
    primary = load(PRIMARY, "gld103_primary_physical_compare")
    audit = load(AUDIT, "gld103_audit_physical_compare")
    primary_algebra = primary.Algebra(primary.q6_expression())
    primary_bridge = primary.build_bridge(primary.source_manifest())
    audit_algebra = audit.QuotientAlgebra(audit.q6_expression())
    audit_bridge = audit.bridge(audit.canonical_support(), audit_algebra, verbose=False)
    d145 = compare_d145(primary, audit, primary_bridge, audit_bridge)
    factors = {
        name: compare_factor(primary, audit, primary_bridge, audit_bridge, name)
        for name in ("F4", "p2_minus_2p_plus_2")
    }
    if not d145["expression_equal"] or not d145["raw_term_maps_equal"]:
        raise AssertionError("D145 comparison did not close")
    if not all(
        item["all_generators_unit_related"]
        and item["localizer"]["exact_equal"]
        and item["row_space_reconciliation"]["same_rank_and_membership"]
        for item in factors.values()
    ):
        raise AssertionError("physical generator comparison did not close")
    print(json.dumps({
        "D145": d145,
        "scope": "current D145 plus six physical P_i and exact z*B*Delta-1 localizer",
        "factors": factors,
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
