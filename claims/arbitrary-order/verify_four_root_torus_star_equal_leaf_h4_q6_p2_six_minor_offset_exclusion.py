#!/usr/bin/env python3
"""Verify the focused p=2 symbolic-a Q6 offset closure.

This is a primary, exact replay of a deliberately small consequence of the
GLD96 chart.  It uses only the committed GLD71 syndrome constructor and the
committed GLD88 H4/F88 family constructor.  Put ``p=2`` in the normalized
equal-leaf chart, retain symbolic ``a``, write the two remaining leaf
coordinates as the GLD88 values plus offsets ``B,C``, and impose

    Q2(q) = Q6(2,q) = 5*q**4 - 4*q**3 + 12*q**2 - 16*q + 8.

The four ``T`` polynomials are the exact adjugate/Schur residuals for the
official six-row pivot.  ``D0`` and ``D2`` are direct seven-by-seven
determinants.  After exact reduction in ``Q[B,C,q,a]/(Q2)``, the six
representatives are checked against pinned raw/reduced hashes and the exact
grevlex ideal basis ``[Q2/5, B, C]``.

The conclusion is scoped to this normalized offset chart and is not a global
Krenn--Gu proof.  In particular, no ``R31`` generator is included here, no
``E31`` or ``g0`` localization is asserted, and the global conjecture remains
UNRESOLVED.  Run this verifier under the repository's bounded runner when a
wall-clock cap is required, for example ``tools/research/run_bounded.py``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
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

B, C, q, a = sp.symbols("B C q a")

PIVOT_ROWS = (0, 1, 2, 17, 25, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
TARGETS = ((28, 8), (32, 2), (32, 5), (33, 8))

# The two extra direct detectors are intentionally not R31.  Keeping their
# row/column tuples in this file makes the exact ideal input auditable.
MINORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}

EXPECTED_SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)

# These hashes pin the exact determinant and quotient representatives.  They
# are checked after recomputation from the committed constructors below; no
# exploratory script or generated output is imported.
EXPECTED_RAW_DENOMINATORS = {
    "T0": "q*(q + 1)**3",
    "T1": "q**2*(q + 1)**2",
    "T2": "q**2*(q + 1)**3",
    "T3": "q*(q + 1)**2",
    "D0": "(q + 1)**6",
    "D2": "(q + 1)**6",
}
EXPECTED_REDUCED_HASHES = {
    "T0": "e726ee5fd5406059d95043969ad5860eda1463540696d7e4e8cf5420543508d3",
    "T1": "2fd8891db047195270f87c09c7024b5dbde4f8ed27014648ee487b27031e6ca6",
    "T2": "f84a890c3d52c92f0af7a7f753310d59c3cc9bb11ea32433c83a7d3e9bb9764e",
    "T3": "fbe10197fe9898c98389e97e4e58584d9ccf9b61bc2cbc51e959082ccfb11186",
    "D0": "652f5a57dbe12daf26a3336e8924cab9c84f607ca60f330aa2f6c54ec99a19a1",
    "D2": "2cc8f30090e21531f595608185becbb6449ee90f8f8d7b6c36e51c9b4cfc40b2",
}
EXPECTED_RAW_NUMERATOR_HASHES = {
    "T0": "e065890f74336acac357c58ac4f33d1d35b1dc200c6a27ec433efa95d07aa460",
    "T1": "dc608a637397dba5b8354e378c9b142d600693568b52210b9eb32fbebf345311",
    "T2": "959792e9c197492801071ba19dc840b0ccd88a68b39d52e1aaa34f2f66971b0b",
    "T3": "0136e071b62bcb2210310cedf5081a56b234184819711fe7f94b6f476a472cc3",
    "D0": "41338d3c103bebd24dd3862168672b108f38392fbf81a4ce01246acd3e05cb4f",
    "D2": "e9d6455fc3500387b2a40d63663d58fc531ef94b33fb016b4897f12dc8d76124",
}
EXPECTED_GREVLEX_BASIS_SREPR_SHA256 = (
    "da8b07d04dfb0dbc9935345320722fb21f9e711bb9166f82db9fb23b0f7f585f"
)


def load_module(path: Path, name: str):
    """Load one committed constructor without importing a verifier package."""

    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def q6_polynomial(p: sp.Expr, q_value: sp.Expr) -> sp.Expr:
    """The committed GLD96 Q6 formula, transcribed at this leaf."""

    return (
        2 * p**4 * q_value**2
        - 2 * p**4 * q_value
        + p**4
        + 2 * p**3 * q_value**3
        - 7 * p**3 * q_value**2
        + 5 * p**3 * q_value
        - 2 * p**3
        + 2 * p**2 * q_value**4
        - 7 * p**2 * q_value**3
        + 12 * p**2 * q_value**2
        - 7 * p**2 * q_value
        + 2 * p**2
        - 2 * p * q_value**4
        + 5 * p * q_value**3
        - 7 * p * q_value**2
        + 2 * p * q_value
        + q_value**4
        - 2 * q_value**3
        + 2 * q_value**2
    )


def support_digest(gld71) -> str:
    """Hash only the committed supports used by the six displayed minors."""

    supports = tuple(gld71.SPARSE_RELATIONS[index] for index in EXPECTED_SUPPORT_ROWS)
    encoded = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in support],
        ]
        for row, support in zip(EXPECTED_SUPPORT_ROWS, supports, strict=True)
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()


def q2_reduce(expression: sp.Expr, q2: sp.Poly) -> tuple[sp.Expr, str]:
    """Reduce a rational expression modulo Q2 and retain its raw denominator."""

    numerator, denominator = sp.cancel(expression).as_numer_denom()
    if denominator.has(B, C, a):
        raise AssertionError(("displayed-variable denominator", sp.factor(denominator)))
    denominator_poly = sp.Poly(denominator, q, domain=QQ)
    q2_base = sp.Poly(q2.as_expr(), q, domain=QQ)
    denominator_gcd = sp.gcd(denominator_poly, q2_base)
    if denominator_gcd.degree() != 0:
        raise AssertionError(("determinant denominator meets Q2", sp.factor(denominator_gcd.as_expr())))

    coefficient_domain = QQ.frac_field(B, C, a)
    q2_field = sp.Poly(q2.as_expr(), q, domain=coefficient_domain)
    numerator_poly = sp.Poly(numerator, q, domain=coefficient_domain)
    denominator_field = sp.Poly(denominator, q, domain=coefficient_domain)
    inverse = sp.invert(denominator_field, q2_field)
    reduced = (numerator_poly.rem(q2_field) * inverse).rem(q2_field).as_expr()
    reduced = sp.cancel(reduced)
    if sp.denom(reduced).has(B, C, q, a):
        raise AssertionError(("Q2 reduction introduced a displayed-variable denominator", sp.denom(reduced)))
    polynomial = sp.Poly(sp.expand(reduced), B, C, q, a, domain=QQ)
    _content, primitive = polynomial.primitive()
    if primitive.total_degree() == 0:
        primitive = primitive.monic()
    reduced = sp.expand(primitive.as_expr())
    if sp.Poly(reduced, B, C, q, a, domain=QQ).LC() < 0:
        reduced = -reduced
    return sp.expand(reduced), str(sp.factor(denominator))


def gate_ledger(q2: sp.Poly) -> dict[str, object]:
    """Check chart and determinant factors before using quotient identities."""

    p = sp.Integer(2)
    d0 = q + 1
    P = p**2 - p + 1
    L1 = p**2 + 2 * p * q - 2 * p - q
    L2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    delta = sp.expand((p - q) * d0 * P * L1 * L2 * e)
    h2 = 2 * p**2 - 2 * p + 1
    q2_poly = sp.Poly(q2.as_expr(), q, domain=QQ)
    factors = {
        "p_minus_q": p - q,
        "d0": d0,
        "P": P,
        "L1": L1,
        "L2": L2,
        "e": e,
        "Delta": delta,
        "h2_leading_coefficient": h2,
    }
    gcds = {
        name: str(sp.factor(sp.gcd(sp.Poly(value, q, domain=QQ), q2_poly).as_expr()))
        for name, value in factors.items()
    }
    assert all(value == "1" for value in gcds.values()), gcds
    det_g = sp.cancel((1 - a) * L2 / d0)
    return {
        "p": 2,
        "d0": str(d0),
        "P": str(P),
        "L1": str(L1),
        "L2": str(L2),
        "e": str(e),
        "Delta_factorization": str(sp.factor(delta)),
        "h2_leading_coefficient": str(h2),
        "detG_at_p2_F88_origin": str(det_g),
        "chart_denominators": {
            "s": str(d0),
            "b88": str(sp.factor(P * e)),
            "c88": str(sp.factor(d0 * e)),
            "kernel_u_v": str(sp.factor((p - q) * d0**3)),
        },
        "Q2_gate_gcds": gcds,
        "all_q_gates_coprime_to_Q2": True,
        "detG_gate": "a != 1 and L2 != 0 on the displayed GLD88 chart",
    }


def build_data():
    """Construct the exact GLD71 syndrome using only committed builders."""

    gld71 = load_module(GLD71, "gld71_for_p2_offset_primary")
    gld88 = load_module(GLD88, "gld88_for_p2_offset_primary")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37
    assert support_digest(gld71) == EXPECTED_SUPPORT_DIGEST
    p, q_value, a_value, b_value, c_value = sp.symbols("p q a b c")
    family = gld88.h4_family(p, q_value, a_value)
    leaf = sp.Matrix(
        [
            [1, 1, 1],
            [p, q_value, family["s"]],
            [a_value, 1 + b_value, 1 + c_value],
        ]
    )
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    assert syndrome.shape == (37, 9)
    return gld71, gld88, syndrome, (p, q_value, a_value, b_value, c_value)


def check_f88_kernel(syndrome, gld88, variables) -> dict[str, object]:
    """Verify every entry of the 37-by-3 block kernel product (111 checks)."""

    p, q_value, a_value, b_value, c_value = variables
    family = gld88.h4_family(p, q_value, a_value)
    kernel = sp.Matrix([family["u"], family["v"], 1])
    f88_syndrome = syndrome.subs(
        {b_value: family["b"], c_value: family["c"]}
    ).applyfunc(sp.cancel)
    count = 0
    for block in range(3):
        for value in f88_syndrome[:, 3 * block : 3 * block + 3] * kernel:
            assert sp.cancel(value) == 0
            count += 1
    assert count == 111
    return {
        "identity_count": count,
        "kernel": [str(family["u"]), str(family["v"]), "1"],
        "verified": True,
    }


def raw_metadata(name: str, raw: sp.Expr, variables) -> dict[str, object]:
    numerator, denominator = sp.cancel(raw).as_numer_denom()
    polynomial = sp.Poly(numerator, *variables, domain=QQ)
    metadata = {
        "rows": list(MINORS[name][0]),
        "columns": list(MINORS[name][1]),
        "raw_denominator": str(sp.factor(denominator)),
        "raw_numerator_terms": len(polynomial.terms()),
        "raw_numerator_srepr_sha256": hashlib.sha256(
            sp.srepr(numerator).encode()
        ).hexdigest(),
    }
    assert metadata["raw_denominator"] == EXPECTED_RAW_DENOMINATORS[name]
    assert metadata["raw_numerator_srepr_sha256"] == EXPECTED_RAW_NUMERATOR_HASHES[name]
    return metadata


def reduced_metadata(name: str, reduced: sp.Expr) -> dict[str, object]:
    polynomial = sp.Poly(reduced, B, C, q, a, domain=QQ)
    metadata = {
        "terms": len(polynomial.terms()),
        "total_degree": polynomial.total_degree(),
        "degrees": {
            str(variable): polynomial.degree(variable)
            for variable in (B, C, q, a)
        },
        "srepr_sha256": hashlib.sha256(sp.srepr(reduced).encode()).hexdigest(),
        "reduced_polynomial": str(reduced),
    }
    assert metadata["srepr_sha256"] == EXPECTED_REDUCED_HASHES[name]
    return metadata


def canonical_basis(expressions: list[sp.Expr]) -> list[str]:
    return sorted(
        str(
            sp.Poly(sp.expand(expression), B, C, q, a, domain=QQ)
            .monic()
            .as_expr()
        )
        for expression in expressions
    )


def exact_basis_check(q2: sp.Poly, reduced_minors: dict[str, sp.Expr]) -> dict[str, object]:
    """Compute and compare the exact grevlex basis over QQ."""

    q2_monic = sp.expand(q2.as_expr() / 5)
    generators = [q2_monic, *reduced_minors.values()]
    basis = sp.groebner(generators, B, C, q, a, order="grevlex", domain=QQ)
    actual = canonical_basis([poly.as_expr() for poly in basis.polys])
    expected = canonical_basis([q2_monic, B, C])
    assert actual == expected, {"actual": actual, "expected": expected}
    assert basis.reduce(B)[1] == 0
    assert basis.reduce(C)[1] == 0
    serialized = "\n".join(
        sp.srepr(sp.expand(poly.as_expr())) for poly in basis.polys
    )
    basis_hash = hashlib.sha256(serialized.encode()).hexdigest()
    assert basis_hash == EXPECTED_GREVLEX_BASIS_SREPR_SHA256
    return {
        "generator_order": ["Q2/5", *MINORS],
        "grevlex_variables": ["B", "C", "q", "a"],
        "basis": actual,
        "expected_basis": expected,
        "basis_size": len(basis.polys),
        "basis_srepr_sha256": basis_hash,
        "exact_BC_membership": True,
    }


def check() -> dict[str, object]:
    started = time.monotonic()
    gld71, gld88, syndrome, variables = build_data()
    p, q_value, a_value, b_value, c_value = variables
    p2 = sp.Integer(2)
    family = gld88.h4_family(p, q_value, a_value)
    specialized_family = {
        name: sp.cancel(value.subs({p: p2}))
        for name, value in family.items()
    }
    assert sp.cancel(
        p2 * q_value
        + p2 * specialized_family["s"]
        + q_value * specialized_family["s"]
        - p2
        - q_value
        - specialized_family["s"]
    ) == 0
    f88_leaf = sp.Matrix(
        [
            [1, 1, 1],
            [p2, q_value, specialized_family["s"]],
            [a_value, 1 + specialized_family["b"], 1 + specialized_family["c"]],
        ]
    )
    expected_f88_det = sp.cancel(
        (1 - a_value) * (q_value**2 + 2 * q_value - 2) / (q_value + 1)
    )
    assert sp.cancel(f88_leaf.det() - expected_f88_det) == 0
    specialized = syndrome.subs(
        {
            p: p2,
            b_value: specialized_family["b"] + B,
            c_value: specialized_family["c"] + C,
        }
    ).applyfunc(sp.cancel)
    q2 = sp.Poly(q6_polynomial(p2, q_value), q_value, domain=QQ)
    expected_q2 = 5 * q_value**4 - 4 * q_value**3 + 12 * q_value**2 - 16 * q_value + 8
    assert q2.as_expr() == expected_q2
    gates = gate_ledger(q2)
    kernel = check_f88_kernel(syndrome, gld88, variables)

    pivot = specialized.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    pivot_determinant = sp.cancel(pivot.det(method="domain-ge"))
    pivot_adjugate = pivot.adjugate(method="domain-ge")
    reduced_minors: dict[str, sp.Expr] = {}
    raw_records: dict[str, object] = {}
    reduced_records: dict[str, object] = {}

    for name, (rows, columns) in MINORS.items():
        if name.startswith("T"):
            target_row, target_column = TARGETS[int(name[1:])]
            assert rows == (*PIVOT_ROWS, target_row)
            assert columns == (*PIVOT_COLUMNS, target_column)
            schur = sp.cancel(
                pivot_determinant * specialized[target_row, target_column]
                - sum(
                    specialized[target_row, PIVOT_COLUMNS[i]]
                    * pivot_adjugate[i, j]
                    * specialized[PIVOT_ROWS[j], target_column]
                    for i in range(6)
                    for j in range(6)
                )
            )
            raw = schur
        else:
            raw = sp.cancel(
                specialized.extract(rows, columns).det(method="domain-ge")
            )
        raw_records[name] = raw_metadata(name, raw, (B, C, q, a))
        reduced, denominator_text = q2_reduce(raw, q2)
        reduced_minors[name] = reduced
        raw_records[name]["denominator_used_for_Q2_reduction"] = denominator_text
        reduced_records[name] = reduced_metadata(name, reduced)

        denominator = sp.cancel(raw).as_numer_denom()[1]
        denominator_gcd = sp.gcd(
            sp.Poly(denominator, q, domain=QQ),
            sp.Poly(q2.as_expr(), q, domain=QQ),
        )
        assert denominator_gcd.degree() == 0
        delta_2 = -27 * q**2 * (q - 2) ** 2 * (q + 1) * (q**2 + 2 * q - 2)
        for factor, _multiplicity in sp.factor_list(denominator, q)[1]:
            assert sp.rem(
                sp.Poly(delta_2, q, domain=QQ),
                sp.Poly(factor, q, domain=QQ),
            ) == 0
        raw_records[name]["gcd_with_Q2"] = str(sp.factor(denominator_gcd.as_expr()))

    basis = exact_basis_check(q2, reduced_minors)
    return {
        "status": "exact_scoped_p2_symbolic_a_q6_six_minor_offset_exclusion",
        "gld_identifier": "GLD97",
        "field": "Q_characteristic_zero",
        "global_conjecture": "UNRESOLVED",
        "runtime_environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "scope": (
            "normalized equal-leaf H4 GLD88/F88 offset chart at p=2, symbolic a, "
            "on Q2=0; rank-at-most-six implication only"
        ),
        "constructors": {
            "GLD71": GLD71.relative_to(ROOT).as_posix(),
            "GLD88": GLD88.relative_to(ROOT).as_posix(),
            "imports_exploratory_files": False,
            "syndrome_shape": list(syndrome.shape),
            "support_rows": list(EXPECTED_SUPPORT_ROWS),
            "support_digest_sha256": EXPECTED_SUPPORT_DIGEST,
        },
        "specialization": {
            "p": 2,
            "a": "symbolic",
            "offsets": ["B", "C"],
            "Q2": str(q2.as_expr()),
        },
        "gates": gates,
        "GLD88_F88_kernel": kernel,
        "minors": {
            "pivot_rows": list(PIVOT_ROWS),
            "pivot_columns": list(PIVOT_COLUMNS),
            "targets": [list(target) for target in TARGETS],
            "T_construction": "exact pivot determinant plus adjugate/Schur residual",
            "D_construction": "direct 7-by-7 determinant",
            "raw": raw_records,
            "reduced": reduced_records,
            "reduced_hashes": {
                name: reduced_records[name]["srepr_sha256"] for name in MINORS
            },
        },
        "ideal": {
            "generators": ["Q2/5", *MINORS],
            **basis,
            "R31_generator_included": False,
        },
        "localization_fences": {
            "R31": "not included or inverted; p=2 points with R31=0 remain in scope",
            "E31": "not used or inverted",
            "g0": "not used or inverted",
            "H2": gates["h2_leading_coefficient"],
            "Delta": gates["Delta_factorization"],
            "detG_F88_origin": gates["detG_at_p2_F88_origin"],
        },
        "implication": (
            "If all six displayed seven-minors vanish on this chart and Q2=0, "
            "the exact ideal basis forces B=C=0; GLD95 is a separate downstream "
            "dependency, while all other charts remain outside this replay."
        ),
        "scope_fences": [
            "No arbitrary-p R31/double-pivot theorem is claimed; R31 is not inverted at p=2",
            "No E31 or g0 localization is asserted",
            "GLD95 incidence exclusion is not replayed here",
            "Other H4 charts, exceptional fibres, Fitting, and the global conjecture remain open",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("focused p=2 symbolic-a Q6 six-minor offset verifier: PASS")
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
