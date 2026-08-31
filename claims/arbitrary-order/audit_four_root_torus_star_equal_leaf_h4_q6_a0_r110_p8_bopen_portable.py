#!/usr/bin/env python3
"""No-import direct-matrix audit of the portable GLD101 R110 P8 B-open leaf.

The audit imports only the pinned GLD71 sparse relations.  It locally
transcribes the a=0 equal-leaf H4 chart, rebuilds the full 37 by 9 syndrome,
computes all nine actual seven-minors with direct SymPy determinants, and only
then compares their Q6-reduced coefficient tables with the tracked portable
certificate.  It independently derives the R110 factor and gates and renders
the same canonical Singular standard-basis source.

This is intentionally scoped to the eight-minor B-open P8 leaf.  The C-open
replay is corroborative, the compact P6 route remains inconclusive, and the
global Krenn--Gu conjecture remains UNRESOLVED.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Sequence

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "certificates" / (
    "GLD101_A0_R110_P8_BOPEN_PORTABLE_CERTIFICATE.json"
)

EXPECTED_GLD71_LF_SHA256 = (
    "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e"
)
EXPECTED_CERTIFICATE_LF_SHA256 = (
    "bdf84e09be8e4d7f76a0d05b050957acd2ef9b95d1e55a6fafe3f9d465c1c32b"
)
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
EXPECTED_Q6_SREPR_SHA256 = (
    "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"
)
EXPECTED_DIRECT_GENERATOR_DIGEST = (
    "8ce1f9037e428291f123237df7782968b07ee230f4e39856b25e889c0a06359b"
)
EXPECTED_R110_SHA256 = (
    "1ae5a3e502f686d484b757db27d6f70b3ff535792edb65ceb40c2bd455410016"
)
EXPECTED_RESULTANT_TEXT_SHA256 = (
    "1192e8cfe113b732e6b1dfa67f06c45ed6317437f14ccc520f5c3db5335f2790"
)
EXPECTED_LINEAR_C0_SHA256 = (
    "7592da3baafec83829e532a52fdb18500902134a77c8e07b1c57e62a1557c52f"
)
EXPECTED_LINEAR_C1_SHA256 = (
    "eccd307c79046e6b55bba6852feee2b24515c34c38c3fc591e1624ba22acd2ff"
)
EXPECTED_SINGULAR_SOURCE_SHA256 = (
    "a8b84e4d8cf2cd7768ab4d945a403ac80200adef0019de6a793bb565756b3bd5"
)

p, q, B, C = sp.symbols("p q B C")
Kp = QQ.frac_field(p)
Kpq = QQ.frac_field(p, q)
ALL_ROWS = tuple(range(37))
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
RSTAR = (0, 1, 17, 28, 31, 32, 33)
GENERATOR_ORDER = ("T0", "T1", "T2", "T3", "D0", "D2", "Y0", "Y1", "X3")
EIGHT_NAMES = ("T0", "T1", "T2", "T3", "D0", "Y0", "Y1", "X3")
SIX_NAMES = ("T0", "T1", "T2", "T3", "Y1", "X3")
SIX_COLUMNS = ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))
NAMED = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}
EXTRA = {
    "Y0": (0, 1, 2, 3, 4, 5, 6),
    "Y1": (0, 1, 3, 4, 5, 6, 7),
    "X3": (0, 1, 2, 3, 4, 6, 7),
}


class PortableAuditError(RuntimeError):
    """Fail-closed independent arithmetic, source, or certificate mismatch."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def load_gld71() -> Any:
    if lf_sha256(GLD71) != EXPECTED_GLD71_LF_SHA256:
        raise PortableAuditError("pinned GLD71 source drift")
    spec = importlib.util.spec_from_file_location(
        "gld71_for_r110_p8_portable_direct_audit", GLD71
    )
    if spec is None or spec.loader is None:
        raise PortableAuditError(f"cannot import {GLD71}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def q6_expression() -> sp.Expr:
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


def h4_a0_family() -> dict[str, sp.Expr]:
    h4_denominator = p + q - 1
    rank_denominator = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    b_numerator = (
        p**3 * q**2
        - p**3
        + p**2 * q**3
        - 3 * p**2 * q**2
        + p**2
        - 2 * p * q**3
        + 3 * p * q**2
        - 2 * p
        + q**2
        - 3 * q
        + 2
    )
    c_numerator = (
        p**2 * q**2
        - 2 * p**2 * q
        - 3 * p * q**2
        + p * q
        + p
        - q**2
        + 3 * q
        - 2
    )
    return {
        "s": sp.cancel((p + q - p * q) / h4_denominator),
        "b": sp.cancel(-b_numerator / ((p**2 - p + 1) * rank_denominator)),
        "c": sp.cancel(-c_numerator / (h4_denominator * rank_denominator)),
        "rank_denominator": rank_denominator,
    }


def build_syndrome(gld71: Any) -> tuple[sp.Matrix, dict[str, sp.Expr], str]:
    support_payload = [
        [
            index,
            [
                [list(indices), coefficient]
                for indices, coefficient in gld71.SPARSE_RELATIONS[index]
            ],
        ]
        for index in SUPPORT_ROWS
    ]
    digest = sha256_bytes(
        json.dumps(support_payload, separators=(",", ":")).encode("ascii")
    )
    if digest != EXPECTED_SUPPORT_DIGEST:
        raise PortableAuditError(f"tracked support digest mismatch: {digest}")
    family = h4_a0_family()
    leaves = [
        (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
        (p, q, family["s"]),
        (sp.Integer(0), 1 + family["b"] + B, 1 + family["c"] + C),
    ]
    matrix_rows = []
    for row in ALL_ROWS:
        entries = []
        for root in range(3):
            for component in range(3):
                value = sp.Integer(0)
                for indices, coefficient in gld71.SPARSE_RELATIONS[row]:
                    if indices[0] != root:
                        continue
                    value += sp.Integer(coefficient) * (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                entries.append(sp.cancel(value))
        matrix_rows.append(entries)
    return sp.Matrix(matrix_rows), family, digest


def direct_minors(syndrome: sp.Matrix) -> dict[str, sp.Expr]:
    result = {}
    for name in GENERATOR_ORDER:
        rows, columns = NAMED[name] if name in NAMED else (RSTAR, EXTRA[name])
        print(f"[R110 P8 direct audit] actual minor {name}", file=sys.stderr, flush=True)
        value = syndrome.extract(list(rows), list(columns)).det(method="domain-ge")
        result[name] = sp.cancel(value)
        polynomial = sp.Poly(result[name], B, C, domain=Kpq)
        if polynomial.coeff_monomial(1) != 0:
            raise PortableAuditError(f"{name} has a constant offset term")
    if result["D2"] != 0:
        raise PortableAuditError("D2 is not identically zero on a=0")
    return result


def quotient_reduce_rational(expression: sp.Expr, q6: sp.Expr) -> sp.Expr:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    modulus = sp.Poly(q6, q, domain=Kp)
    numerator_poly = sp.Poly(numerator, q, domain=Kp).rem(modulus)
    denominator_poly = sp.Poly(denominator, q, domain=Kp).rem(modulus)
    if denominator_poly.is_zero:
        raise PortableAuditError("coefficient denominator is zero modulo Q6")
    inverse = sp.invert(denominator_poly, modulus)
    return sp.cancel(sp.expand((numerator_poly * inverse).rem(modulus).as_expr()))


def direct_coefficient_tables(
    minors: dict[str, sp.Expr], q6: sp.Expr
) -> dict[str, dict[str, list[str]]]:
    tables: dict[str, dict[str, list[str]]] = {}
    for name in GENERATOR_ORDER:
        polynomial = sp.Poly(minors[name], B, C, domain=Kpq)
        table = {}
        if not polynomial.is_zero:
            for exponent in sorted(polynomial.monoms()):
                if exponent == (0, 0):
                    continue
                coefficient = sp.cancel(
                    polynomial.coeff_monomial(B ** exponent[0] * C ** exponent[1])
                )
                reduced = quotient_reduce_rational(coefficient, q6)
                reduced_poly = sp.Poly(reduced, q, domain=Kp)
                table[f"{exponent[0]},{exponent[1]}"] = [
                    str(sp.cancel(reduced_poly.nth(index))) for index in range(4)
                ]
        tables[name] = table
    return tables


def table_digest(tables: dict[str, dict[str, list[str]]]) -> str:
    payload: list[Any] = []
    for name in GENERATOR_ORDER:
        terms = []
        for key, slots in sorted(
            tables[name].items(), key=lambda item: tuple(map(int, item[0].split(",")))
        ):
            exponent = [int(value) for value in key.split(",")]
            numerator_denominator = []
            for text in slots:
                numerator, denominator = sp.cancel(
                    sp.sympify(text, locals={"p": p}, rational=True)
                ).as_numer_denom()
                numerator_denominator.append([str(numerator), str(denominator)])
            terms.append([exponent, numerator_denominator])
        payload.append([name, terms])
    return sha256_bytes(
        json.dumps(payload, separators=(",", ":")).encode("ascii")
    )


def table_expression(slots: list[str]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.sympify(text, locals={"p": p}, rational=True) * q**index
            for index, text in enumerate(slots)
        )
    )


def six_selector_from_tables(
    tables: dict[str, dict[str, list[str]]], q6: sp.Expr
) -> tuple[list[sp.Expr], sp.Expr]:
    matrix = sp.Matrix(
        [
            [
                table_expression(
                    tables[name].get(
                        f"{exponent[0]},{exponent[1]}", ["0", "0", "0", "0"]
                    )
                )
                for name in SIX_NAMES
            ]
            for exponent in SIX_COLUMNS
        ]
    )
    print("[R110 P8 direct audit] six-selector determinant", file=sys.stderr, flush=True)
    selector = sp.cancel(matrix.det(method="domain-ge"))
    reduced = quotient_reduce_rational(selector, q6)
    reduced_poly = sp.Poly(reduced, q, domain=Kp)
    slots = [sp.cancel(reduced_poly.nth(index)) for index in range(4)]
    numerator = sp.expand(
        sum(
            item.as_numer_denom()[0] * q**index
            for index, item in enumerate(slots)
        )
    )
    return slots, numerator


def p_polynomial(expression: object) -> sp.Poly:
    return sp.Poly(sp.sympify(expression), p, domain=QQ)


def primitive_integer_polynomial(expression: object) -> sp.Poly:
    polynomial = p_polynomial(expression)
    denominators = [sp.denom(coefficient) for coefficient in polynomial.all_coeffs()]
    scale = sp.ilcm(*[int(value) for value in denominators])
    integer = sp.Poly(sp.expand(scale * polynomial.as_expr()), p, domain=sp.ZZ)
    _content, primitive = integer.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return sp.Poly(primitive.as_expr(), p, domain=QQ)


def derive_r110(resultant: sp.Poly) -> tuple[sp.Poly, int]:
    _content, factors = sp.factor_list(resultant.as_expr(), p)
    candidates = [
        (primitive_integer_polynomial(factor), int(exponent))
        for factor, exponent in factors
        if sp.degree(factor, p) == 110
    ]
    if len(candidates) != 1:
        raise PortableAuditError(f"expected one degree-110 factor, found {len(candidates)}")
    factor, multiplicity = candidates[0]
    digest = sha256_bytes(str(sp.expand(factor.as_expr())).encode("ascii"))
    if digest != EXPECTED_R110_SHA256 or multiplicity != 1:
        raise PortableAuditError(
            f"R110 factor drift: digest={digest}, multiplicity={multiplicity}"
        )
    return factor, multiplicity


def reduce_q_polynomial(expression: sp.Expr, factor: sp.Poly) -> sp.Expr:
    result = sp.Integer(0)
    polynomial = sp.Poly(expression, q, domain=Kp)
    for (q_degree,), coefficient in polynomial.terms():
        result += p_polynomial(str(coefficient)).rem(factor).as_expr() * q**q_degree
    return sp.expand(result)


def field_multiply(left: sp.Poly, right: sp.Poly, factor: sp.Poly) -> sp.Poly:
    return (left * right).rem(factor)


def field_power(value: sp.Poly, exponent: int, factor: sp.Poly) -> sp.Poly:
    result = sp.Poly(1, p, domain=QQ)
    base = value.rem(factor)
    power = exponent
    while power:
        if power & 1:
            result = field_multiply(result, base, factor)
        power >>= 1
        if power:
            base = field_multiply(base, base, factor)
    return result


def homogeneous_root_evaluation(
    expression: sp.Expr, c0: sp.Poly, c1: sp.Poly, factor: sp.Poly
) -> sp.Poly:
    polynomial = sp.Poly(expression, q, domain=Kp)
    degree = int(polynomial.degree())
    total = sp.Poly(0, p, domain=QQ)
    for (q_degree,), coefficient in polynomial.terms():
        term = field_multiply(
            p_polynomial(str(coefficient)).rem(factor),
            field_power(-c0, q_degree, factor),
            factor,
        )
        term = field_multiply(
            term,
            field_power(c1, degree - q_degree, factor),
            factor,
        )
        total = (total + term).rem(factor)
    return total


def singular_term(coefficient: Any, exponents: tuple[int, int, int, int]) -> str:
    numerator, denominator = sp.fraction(sp.Rational(coefficient))
    piece = f"({numerator}/{denominator})"
    for variable, exponent in zip(("p", "q", "B", "C"), exponents):
        if exponent:
            piece += "*" + variable
            if exponent != 1:
                piece += f"^{int(exponent)}"
    return piece


def singular_pq(expression: sp.Expr) -> str:
    terms = []
    for (p_degree, q_degree), coefficient in sp.Poly(
        sp.expand(expression), p, q, domain=QQ
    ).terms():
        terms.append(singular_term(coefficient, (p_degree, q_degree, 0, 0)))
    return " + ".join(terms) if terms else "0"


def hard_generator_texts(
    tables: dict[str, dict[str, list[str]]], factor: sp.Poly
) -> tuple[dict[str, str], dict[str, int]]:
    texts = {}
    gcd_degrees = {}
    for name in EIGHT_NAMES:
        expressions = [
            sp.cancel(sp.sympify(text, locals={"p": p}, rational=True))
            for slots in tables[name].values()
            for text in slots
        ]
        denominator_product = sp.Poly(1, p, domain=QQ)
        for expression in expressions:
            _numerator, denominator = expression.as_numer_denom()
            denominator_product *= p_polynomial(denominator)
        gcd_degrees[name] = int(sp.gcd(denominator_product, factor).degree())
        terms = []
        for key, slots in sorted(
            tables[name].items(), key=lambda item: tuple(map(int, item[0].split(",")))
        ):
            b_degree, c_degree = (int(value) for value in key.split(","))
            value = sp.Integer(0)
            for q_degree, text in enumerate(slots):
                expression = sp.cancel(
                    sp.sympify(text, locals={"p": p}, rational=True)
                )
                numerator, denominator = expression.as_numer_denom()
                quotient, remainder = sp.div(
                    denominator_product, p_polynomial(denominator)
                )
                if not remainder.is_zero:
                    raise PortableAuditError(f"{name} denominator clearing failed")
                value += (p_polynomial(numerator) * quotient).as_expr() * q**q_degree
            polynomial = sp.Poly(value, q, domain=Kp)
            for (q_degree,), coefficient in polynomial.terms():
                reduced = p_polynomial(str(coefficient)).rem(factor)
                for (p_degree,), p_coefficient in reduced.terms():
                    terms.append(
                        singular_term(
                            p_coefficient,
                            (p_degree, q_degree, b_degree, c_degree),
                        )
                    )
        texts[name] = " + ".join(terms) if terms else "0"
    if any(degree != 0 for degree in gcd_degrees.values()):
        raise PortableAuditError("an actual-minor denominator meets R110")
    return texts, gcd_degrees


def build_singular_source(
    factor: sp.Poly,
    q6_reduced: sp.Expr,
    six_reduced: sp.Expr,
    relation: sp.Expr,
    generator_texts: dict[str, str],
) -> str:
    r110_text = str(sp.expand(factor.as_expr())).replace("**", "^")
    mathematical_generators = [
        singular_pq(q6_reduced),
        singular_pq(six_reduced),
        singular_pq(relation),
        *[generator_texts[name] for name in EIGHT_NAMES],
    ]
    lines = [
        'LIB "elim.lib";',
        "ring rg=0,(p),dp;",
        f"poly R110={r110_text};",
        "poly R110Gate=p*(p-1)*(p^2-p+1)*(2*p^2-2*p+1);",
        "poly R110GateGcd=gcd(R110,R110Gate);",
        'print("QSUB_R110_GATE_GCD_DEGREE="+string(deg(R110GateGcd)));',
        'if (deg(R110GateGcd)!=0) { print("QSUB_FATAL_R110_GATE_GCD"); exit; }',
        (
            'print("QSUB_RESULTANT_IDENTITY_SHA256='
            f'{EXPECTED_RESULTANT_TEXT_SHA256}");'
        ),
        'print("QSUB_DELTA_UNIT_BY_RESULTANT=1");',
        "ring r=(0,p),(q,z,B,C),dp;",
        f"minpoly={r110_text};",
        "option(redSB);",
        "ideal I=",
        *[f"  {text}," for text in mathematical_generators],
        "  z*B-1;",
        "poly relation=I[3];",
        "poly common_gcd=gcd(I[1],I[2]);",
        "ideal relation_basis=std(ideal(relation));",
        "poly c0poly=subst(relation,q,0);",
        'if (deg(relation)!=1) { print("QSUB_FATAL_RELATION_DEGREE"); exit; }',
        'if (deg(common_gcd)!=1) { print("QSUB_FATAL_GCD_DEGREE"); exit; }',
        "number c0=leadcoef(c0poly);",
        "number c1=leadcoef(relation);",
        'if (c1==0) { print("QSUB_FATAL_C1_ZERO"); exit; }',
        "number qroot=-c0/c1;",
        "poly q6_at_root=subst(I[1],q,qroot);",
        "poly six_at_root=subst(I[2],q,qroot);",
        "poly relation_at_root=subst(I[3],q,qroot);",
        'print("QSUB_GCD_DEGREE="+string(deg(common_gcd)));',
        'print("QSUB_RELATION_DIVIDES_Q6="+string(reduce(I[1],relation_basis)==0));',
        'print("QSUB_RELATION_DIVIDES_SIX="+string(reduce(I[2],relation_basis)==0));',
        'print("QSUB_C1_NONZERO="+string(c1!=0));',
        'print("QSUB_Q6_ZERO="+string(q6_at_root==0));',
        'print("QSUB_SIX_ZERO="+string(six_at_root==0));',
        'print("QSUB_RELATION_ZERO="+string(relation_at_root==0));',
        'print("QSUB_ROOTCHECK_OK=1");',
        (
            "ideal J=subst(I[4],q,qroot),subst(I[5],q,qroot),"
            "subst(I[6],q,qroot),subst(I[7],q,qroot),"
            "subst(I[8],q,qroot),subst(I[9],q,qroot),"
            "subst(I[10],q,qroot),subst(I[11],q,qroot),I[12];"
        ),
        'print("QSUB_J_SIZE="+string(size(J)));',
        "ideal G=std(J);",
        'print("QSUB_G_SIZE="+string(size(G)));',
        'if (reduce(1,G)==0) { print("QSUB_UNIT=1"); } else { print("QSUB_UNIT=0"); }',
        "exit;",
    ]
    source = "\n".join(lines) + "\n"
    if len(lines) != 52:
        raise PortableAuditError(f"Singular source line count drift: {len(lines)}")
    digest = sha256_bytes(source.encode("utf-8"))
    if digest != EXPECTED_SINGULAR_SOURCE_SHA256:
        raise PortableAuditError(f"Singular source mismatch: {digest}")
    return source


def load_certificate() -> dict[str, Any]:
    if lf_sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_LF_SHA256:
        raise PortableAuditError("tracked portable certificate signature mismatch")
    try:
        payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PortableAuditError("tracked certificate is not strict UTF-8 JSON") from exc
    if payload.get("certificate_id") != (
        "GLD101-A0-R110-P8-B-open-portable-unit-leaf"
    ):
        raise PortableAuditError("portable certificate id mismatch")
    if payload.get("global_conjecture") != "UNRESOLVED":
        raise PortableAuditError("portable certificate global status drift")
    return payload


def check() -> tuple[dict[str, Any], str]:
    gld71 = load_gld71()
    syndrome, family, support_digest = build_syndrome(gld71)
    if syndrome.shape != (37, 9):
        raise PortableAuditError(f"authoritative syndrome shape drift: {syndrome.shape}")
    q6 = sp.expand(q6_expression())
    q6_digest = sha256_bytes(sp.srepr(q6).encode("ascii"))
    if q6_digest != EXPECTED_Q6_SREPR_SHA256:
        raise PortableAuditError(f"Q6 signature mismatch: {q6_digest}")
    minors = direct_minors(syndrome)
    tables = direct_coefficient_tables(minors, q6)
    generator_digest = table_digest(tables)
    if generator_digest != EXPECTED_DIRECT_GENERATOR_DIGEST:
        raise PortableAuditError(f"direct generator digest mismatch: {generator_digest}")

    six_slots, six_numerator = six_selector_from_tables(tables, q6)
    resultant = sp.Poly(sp.resultant(q6, six_numerator, q), p, domain=QQ)
    factor_raw, multiplicity = derive_r110(resultant)
    factor = factor_raw.monic()
    if not sp.Poly(factor_raw.as_expr(), p, modulus=41).is_irreducible:
        raise PortableAuditError("R110 mod-41 irreducibility witness failed")
    excluded_gate = sp.Poly(
        p * (p - 1) * (p**2 - p + 1) * (2 * p**2 - 2 * p + 1),
        p,
        domain=QQ,
    )
    if sp.gcd(factor_raw, excluded_gate).degree() != 0:
        raise PortableAuditError("R110 meets an excluded coefficient or Delta gate")

    subresultants = sp.subresultants(q6, six_numerator, q)
    linear = next(item for item in subresultants if sp.Poly(item, q).degree() == 1)
    linear_poly = sp.Poly(linear, q, domain=Kp)
    c0 = p_polynomial(str(linear_poly.coeff_monomial(1))).rem(factor)
    c1 = p_polynomial(str(linear_poly.coeff_monomial(q))).rem(factor)
    c0_hash = sha256_bytes(str(c0.as_expr()).encode("ascii"))
    c1_hash = sha256_bytes(str(c1.as_expr()).encode("ascii"))
    if c0_hash != EXPECTED_LINEAR_C0_SHA256:
        raise PortableAuditError(f"linear c0 signature mismatch: {c0_hash}")
    if c1_hash != EXPECTED_LINEAR_C1_SHA256 or c1.is_zero:
        raise PortableAuditError(f"linear c1 signature mismatch: {c1_hash}")
    q6_reduced = reduce_q_polynomial(q6, factor)
    six_reduced = reduce_q_polynomial(six_numerator, factor)
    relation = sp.expand(c0.as_expr() + c1.as_expr() * q)
    root_checks = {
        "q6": homogeneous_root_evaluation(q6_reduced, c0, c1, factor).is_zero,
        "six_selector": homogeneous_root_evaluation(
            six_reduced, c0, c1, factor
        ).is_zero,
        "linear_relation": homogeneous_root_evaluation(
            relation, c0, c1, factor
        ).is_zero,
    }
    if not all(root_checks.values()):
        raise PortableAuditError(f"independent linear-root gate failed: {root_checks}")

    delta = sp.expand(
        (p - q)
        * (p + q - 1)
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * family["rank_denominator"]
    )
    expected_delta_resultant = sp.expand(
        27648
        * p**6
        * (p - 1) ** 6
        * (p**2 - p + 1) ** 19
        * (2 * p**2 - 2 * p + 1)
    )
    if sp.expand(sp.resultant(q6, delta, q) - expected_delta_resultant) != 0:
        raise PortableAuditError("independent Q6/Delta resultant identity failed")
    resultant_text = "27648*p^6*(p-1)^6*(p^2-p+1)^19*(2*p^2-2*p+1)"
    if sha256_bytes(resultant_text.encode("ascii")) != EXPECTED_RESULTANT_TEXT_SHA256:
        raise PortableAuditError("Q6/Delta resultant text signature mismatch")

    generator_texts, denominator_gcd_degrees = hard_generator_texts(tables, factor)
    source = build_singular_source(
        factor_raw, q6_reduced, six_reduced, relation, generator_texts
    )

    certificate = load_certificate()
    if certificate["actual_minors"]["coefficient_tables"] != tables:
        raise PortableAuditError("direct coefficient tables differ from certificate")
    if certificate["actual_minors"]["direct_generator_digest"] != generator_digest:
        raise PortableAuditError("certificate direct-generator digest mismatch")
    if certificate["r110"]["polynomial"] != str(sp.expand(factor_raw.as_expr())):
        raise PortableAuditError("certificate R110 polynomial mismatch")
    if certificate["r110"]["linear_relation"]["c0"] != str(c0.as_expr()):
        raise PortableAuditError("certificate linear c0 polynomial mismatch")
    if certificate["r110"]["linear_relation"]["c1"] != str(c1.as_expr()):
        raise PortableAuditError("certificate linear c1 polynomial mismatch")
    if (
        certificate["r110"]["actual_minor_denominator_gcd_degrees"]
        != denominator_gcd_degrees
    ):
        raise PortableAuditError("certificate denominator-unit receipts mismatch")
    if certificate["singular_standard_basis"]["source_sha256"] != (
        EXPECTED_SINGULAR_SOURCE_SHA256
    ):
        raise PortableAuditError("certificate Singular source signature mismatch")

    result = {
        "status": "exact_independent_direct_matrix_audit_GLD101_R110_P8_B_open",
        "global_conjecture": "UNRESOLVED",
        "certificate_lf_sha256": EXPECTED_CERTIFICATE_LF_SHA256,
        "syndrome_shape": list(syndrome.shape),
        "support_digest": support_digest,
        "direct_generator_digest": generator_digest,
        "actual_minor_names": list(EIGHT_NAMES),
        "d2_zero_control": True,
        "six_q_slot_sha256": [
            sha256_bytes(str(item).encode("ascii")) for item in six_slots
        ],
        "r110": {
            "sha256": EXPECTED_R110_SHA256,
            "multiplicity": multiplicity,
            "mod41_irreducible": True,
            "excluded_gate_gcd_degree": 0,
            "delta_unit": True,
            "root_checks": root_checks,
            "denominator_gcd_degrees": denominator_gcd_degrees,
        },
        "singular_source_sha256": EXPECTED_SINGULAR_SOURCE_SHA256,
        "scope": "P8 B-open unit-ideal leaf only",
        "nonclaims": [
            "This audit imports neither the portable primary verifier nor its quotient implementation.",
            "The C-open replay is corroborative and not load-bearing here.",
            "The compact six-minor P6 route remains inconclusive.",
            "No theorem, frontier, full-E31, or global claim is promoted.",
        ],
    }
    return result, source


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-source", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result, source = check()
    if args.emit_source:
        args.emit_source.parent.mkdir(parents=True, exist_ok=True)
        args.emit_source.write_text(source, encoding="utf-8", newline="\n")
    text = canonical_json(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print("GLD101 R110 P8 B-open direct-matrix audit: PASS")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
