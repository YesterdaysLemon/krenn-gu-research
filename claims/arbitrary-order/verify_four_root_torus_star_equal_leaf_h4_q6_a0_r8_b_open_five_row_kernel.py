#!/usr/bin/env python3
"""Verify the portable GLD101 R8 B-open five-row kernel certificate.

This checker consumes only the tracked compact matrix payload.  Arithmetic is
exact in

    A = (QQ[p]/(R8))[q]/(Q6).

It recomputes all six signed maximal cofactors, verifies ``M*K=0``, proves
that ``K6`` is a unit at every Q6 point, and checks the shared linear gcd for
``K2`` and ``K3*K2-K1*K4``.  Together with the fixed monomial coordinates
``(t,1,B*t,B,B^2*t,B^2)``, these identities give the scoped selected-minor
obstruction recorded in the certificate.

This is not a converse from selected minors to syndrome rank and has no
endpoint, physical-incidence, P6, full-E31, or global conclusion.  The global
Krenn--Gu conjecture remains UNRESOLVED.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from pathlib import Path

import sympy as sp
from sympy import QQ


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE / "certificates" / "GLD101_R8_B_OPEN_FIVE_ROW_KERNEL_CERTIFICATE.json"
)
EXPECTED_CERTIFICATE_LF_SHA256 = (
    "df96337e0de80cd1236fde1f366490afa7a06f28845475b03cc5c31eeba8af7c"
)
EXPECTED_SELECTORS = ("T1", "T2", "T3", "Y1", "X3")
EXPECTED_COLUMNS = ("t", "1", "B*t", "B", "B^2*t", "B^2")
EXPECTED_LINEAR_SHA256 = (
    "51d02ef3020d0d8c7d41de6fc266f6a5ba937d192658b0b7c786b66a398eb02f"
)

p, q, alpha, B, t = sp.symbols("p q alpha B t")
SAFE_POLYNOMIAL = re.compile(r"[0-9pq+\-*/^() ]+")


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_polynomial(text: str) -> sp.Expr:
    require(bool(text) and SAFE_POLYNOMIAL.fullmatch(text) is not None, "unsafe polynomial text")
    return sp.expand(
        sp.sympify(text.replace("^", "**"), locals={"p": p, "q": q})
    )


def load_certificate() -> dict[str, object]:
    require(CERTIFICATE.is_file(), f"missing certificate: {CERTIFICATE}")
    actual = lf_sha256(CERTIFICATE)
    require(
        actual == EXPECTED_CERTIFICATE_LF_SHA256,
        f"certificate LF hash drift: {actual}",
    )
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(payload.get("schema_version") == 1, "certificate schema")
    require(
        payload.get("certificate_id") == "GLD101-R8-B-open-five-row-kernel",
        "certificate id",
    )
    require(
        payload.get("status") == "scoped_exact_selected_minor_leaf_certificate",
        "certificate status",
    )
    require(payload.get("global_conjecture") == "UNRESOLVED", "global status")
    scope = payload.get("mathematical_scope", {})
    require(scope.get("factor") == "R8=0", "R8 scope")
    require("D(B*H2*Delta)" in scope.get("open", ""), "open-set scope")
    require(
        tuple(scope.get("selected_necessary_minors", ())) == EXPECTED_SELECTORS,
        "selector scope",
    )
    require(
        "rank(M)<=6" in scope.get("bridge", "")
        and "cancel the common B factor" in scope.get("bridge", ""),
        "one-way rank/B-open bridge",
    )
    nonclaims = " ".join(scope.get("nonclaims", ()))
    for phrase in ("no converse", "no claim on B=0", "no claim for P6", "no global"):
        require(phrase in nonclaims, f"missing nonclaim: {phrase}")
    return payload


def field_element(expression: sp.Expr, field, minpoly: sp.Poly):
    polynomial = sp.Poly(expression, p, domain=QQ).rem(minpoly)
    value = field.zero
    for (degree_p,), coefficient in polynomial.terms():
        value += field.convert(coefficient) * field.unit**degree_p
    return value


def q_polynomial(expression: sp.Expr, field, minpoly: sp.Poly) -> sp.Poly:
    polynomial = sp.Poly(expression, p, q, domain=QQ)
    coefficients: dict[int, object] = {}
    for (degree_p, degree_q), coefficient in polynomial.terms():
        term = field.convert(coefficient) * field.unit**degree_p
        coefficients[degree_q] = coefficients.get(degree_q, field.zero) + term
    return sp.Poly.from_dict(
        {(degree,): value for degree, value in coefficients.items() if value},
        (q,),
        domain=field,
    )


def determinant(matrix: list[list[sp.Poly]], modulus: sp.Poly) -> sp.Poly:
    """Division-free subset determinant, reducing modulo Q6 after every op."""

    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix), "square matrix")
    zero = sp.Poly(0, q, domain=modulus.domain)
    one = sp.Poly(1, q, domain=modulus.domain)
    states: dict[int, sp.Poly] = {0: one}
    for row in matrix:
        next_states: dict[int, sp.Poly] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                product = (value * entry).rem(modulus)
                before = sum(
                    1 for index in range(column) if not mask & (1 << index)
                )
                if before % 2:
                    product = -product
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    next_states.get(new_mask, zero) + product
                ).rem(modulus)
        states = next_states
    return states[(1 << size) - 1].rem(modulus)


def monic_gcd(left: sp.Poly, right: sp.Poly) -> sp.Poly:
    gcd = left.gcd(right)
    require(not gcd.is_zero, "zero gcd")
    return gcd.monic()


def check() -> dict[str, object]:
    payload = load_certificate()
    algebra = payload["algebra"]
    require(tuple(algebra["columns"]) == EXPECTED_COLUMNS, "column order")

    r8_expression = parse_polynomial(algebra["minpoly_R8"])
    r8 = sp.Poly(r8_expression, p, domain=QQ).monic()
    require(r8.degree() == 8 and r8.is_irreducible, "R8 irreducibility")
    r8_signature = hashlib.sha256(str(sp.expand(r8_expression)).encode()).hexdigest()
    require(r8_signature == algebra["R8_signature_sha256"], "R8 signature")

    field = QQ.algebraic_field((r8, alpha))
    q6_expression = parse_polynomial(algebra["Q6"])
    q6_srepr = hashlib.sha256(sp.srepr(q6_expression).encode()).hexdigest()
    require(q6_srepr == algebra["Q6_srepr_sha256"], "Q6 srepr pin")
    q6 = q_polynomial(q6_expression, field, r8)
    require(q6.degree() == 4, "Q6 degree")
    require(monic_gcd(q6, q6.diff()).degree() == 0, "Q6 squarefree")

    h2 = field_element(2 * p**2 - 2 * p + 1, field, r8)
    require(h2 != field.zero, "H2 vanishes in the R8 coefficient field")

    raw_matrix = algebra["matrix"]
    require(tuple(raw_matrix) == EXPECTED_SELECTORS, "matrix row order")
    matrix: list[list[sp.Poly]] = []
    for selector in EXPECTED_SELECTORS:
        row = raw_matrix[selector]
        require(len(row) == 6, f"matrix width: {selector}")
        matrix.append(
            [
                q_polynomial(parse_polynomial(entry), field, r8).rem(q6)
                for entry in row
            ]
        )

    cofactors: list[sp.Poly] = []
    for omitted in range(6):
        submatrix = [row[:omitted] + row[omitted + 1 :] for row in matrix]
        cofactor = determinant(submatrix, q6)
        if omitted % 2:
            cofactor = -cofactor
        cofactors.append(cofactor.rem(q6))

    zero = sp.Poly(0, q, domain=field)
    for row_index, row in enumerate(matrix, start=1):
        value = zero
        for entry, cofactor in zip(row, cofactors, strict=True):
            value = (value + entry * cofactor).rem(q6)
        require(value.is_zero, f"M*K row {row_index}")

    k6_gcd = monic_gcd(q6, cofactors[5])
    require(k6_gcd.degree() == 0, "K6 is not a unit on V(Q6)")

    relation_one = (
        cofactors[2] * cofactors[1] - cofactors[0] * cofactors[3]
    ).rem(q6)
    k2_gcd = monic_gcd(q6, cofactors[1])
    relation_gcd = monic_gcd(q6, relation_one)
    expected_linear_text = algebra["expected_common_linear"]
    expected_linear = q_polynomial(
        parse_polynomial(expected_linear_text), field, r8
    ).monic()
    require(
        hashlib.sha256(
            "63*q+(192p7-672p6+1388p5-1790p4+1814p3-1267p2+340p-34)".encode()
        ).hexdigest()
        == EXPECTED_LINEAR_SHA256,
        "common residual display pin",
    )
    require(k2_gcd.degree() == 1 and k2_gcd == expected_linear, "K2 gcd")
    require(
        relation_gcd.degree() == 1 and relation_gcd == expected_linear,
        "monomial-relation gcd",
    )

    monomial_vector = [t, sp.Integer(1), B * t, B, B**2 * t, B**2]
    require(
        sp.expand(monomial_vector[2] * monomial_vector[1]
                  - monomial_vector[0] * monomial_vector[3]) == 0,
        "monomial-vector relation",
    )
    require(monomial_vector[1] == 1, "monomial-vector second coordinate")

    quarantine = payload.get("quarantined_non_evidence", [])
    require(
        len(quarantine) == 1
        and quarantine[0].get("disposition") == "invalid_non_evidence"
        and "individually invertible" in quarantine[0].get("reason", ""),
        "v1 invalid-probe quarantine",
    )

    return {
        "status": "exact_scoped_r8_five_row_kernel_certificate_verified",
        "global_conjecture": "UNRESOLVED",
        "scope": "GLD101 a=0,R8,V(Q6),D(B*H2*Delta), selected necessary minors T1,T2,T3,Y1,X3 only",
        "matrix_shape": [5, 6],
        "kernel_rows_zero": 5,
        "rank_witness": "gcd(Q6,K6)=1",
        "common_residual_degree": 1,
        "common_residual_sha256": EXPECTED_LINEAR_SHA256,
        "monomial_relation": "x3*x2-x1*x4=0 with x2=1",
        "certificate_lf_sha256": EXPECTED_CERTIFICATE_LF_SHA256,
        "nonclaims": payload["mathematical_scope"]["nonclaims"],
    }


def main() -> None:
    print(json.dumps(check(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
