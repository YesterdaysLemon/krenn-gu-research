#!/usr/bin/env python3
"""No-primary-import audit of the portable GLD101 R8 five-row leaf.

The audit parses the literal ``SPARSE_RELATIONS`` tuple from the hash-pinned
tracked GLD71 source without importing or executing any repository module.  A
local transcription of the normalized a=0 GLD88 chart then rebuilds the five
actual seven-minors T1,T2,T3,Y1,X3.  After ``C=B*t`` and cancellation of B on
the B-open chart, every denominator is checked to be supported on Delta.

For each row, the independently rebuilt six coefficients and the tracked
certificate row are compared in

    A = (QQ[p]/(R8))[q]/(Q6)

by the corrected ring-theoretic criterion: both rows are unimodular and all
15 pairwise cross-products vanish.  Thus they differ by a unit in A.  This
audit never imports the primary checker or any repository Python module.

The scope is selected-minor evidence only.  There is no selector converse,
endpoint/physical conclusion, P6 theorem, full-E31 result, or global result.
The global Krenn--Gu conjecture remains UNRESOLVED.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GLD71 = HERE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = HERE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
GLD101_OWNER = HERE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md"
CERTIFICATE = HERE / "certificates" / "GLD101_R8_B_OPEN_FIVE_ROW_KERNEL_CERTIFICATE.json"

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "df96337e0de80cd1236fde1f366490afa7a06f28845475b03cc5c31eeba8af7c"
)
EXPECTED_LF_SHA256 = {
    GLD71: "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    GLD88: "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    GLD101_OWNER: "fe9e705f2fa9cde61c71daeb19abea241545a6c45611c15e6dd03b62ea6d3f45",
}
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
SELECTORS = {
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTOR_ORDER = tuple(SELECTORS)
SUPPORT_ROWS = tuple(
    sorted({row for rows, _columns in SELECTORS.values() for row in rows})
)
PINNED_GLD101_SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
EXPECTED_OFFSET_SUPPORT = {(0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)}
MONOMIAL_EXPONENTS = ((0, 1), (0, 0), (1, 1), (1, 0), (2, 1), (2, 0))

p, q, B, C, t, alpha = sp.symbols("p q B C t alpha")
Kpq = QQ.frac_field(p, q)
SAFE_POLYNOMIAL = re.compile(r"[0-9pq+\-*/^() ]+")


R8_EXPRESSION = (
    64 * p**8 - 256 * p**7 + 580 * p**6 - 844 * p**5 + 946 * p**4
    - 784 * p**3 + 388 * p**2 - 94 * p + 13
)
Q6_EXPRESSION = (
    2 * p**4 * q**2 - 2 * p**4 * q + p**4
    + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
    + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
    - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
    - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def parse_polynomial(text: str) -> sp.Expr:
    require(bool(text) and SAFE_POLYNOMIAL.fullmatch(text) is not None, "unsafe polynomial text")
    return sp.expand(
        sp.sympify(text.replace("^", "**"), locals={"p": p, "q": q})
    )


def load_literal_relations() -> tuple:
    """Read the GLD71 data assignment without importing its module."""

    tree = ast.parse(GLD71.read_text(encoding="utf-8"), filename=str(GLD71))
    matches = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == "SPARSE_RELATIONS" for target in targets):
            matches.append(ast.literal_eval(node.value))
    require(len(matches) == 1, "literal SPARSE_RELATIONS assignment")
    relations = matches[0]
    require(isinstance(relations, tuple) and len(relations) == 37, "relation table shape")
    return relations


class BC:
    """Sparse polynomial in B,C with coefficients in QQ(p,q)."""

    def __init__(self, terms=None):
        self.terms = {
            tuple(exponents): value
            for exponents, value in (terms or {}).items()
            if value
        }

    @classmethod
    def const(cls, value) -> "BC":
        converted = value if type(value) is type(Kpq.one) else Kpq.convert(value)
        return cls({(0, 0): converted}) if converted else cls()

    @classmethod
    def var(cls, exponents: tuple[int, int]) -> "BC":
        return cls({exponents: Kpq.one})

    def __add__(self, other: "BC") -> "BC":
        result = dict(self.terms)
        for exponents, value in other.terms.items():
            updated = result.get(exponents, Kpq.zero) + value
            if updated:
                result[exponents] = updated
            else:
                result.pop(exponents, None)
        return BC(result)

    def __neg__(self) -> "BC":
        return BC({exponents: -value for exponents, value in self.terms.items()})

    def __sub__(self, other: "BC") -> "BC":
        return self + (-other)

    def __mul__(self, other: "BC") -> "BC":
        result = {}
        for (left_b, left_c), left in self.terms.items():
            for (right_b, right_c), right in other.terms.items():
                exponents = (left_b + right_b, left_c + right_c)
                updated = result.get(exponents, Kpq.zero) + left * right
                if updated:
                    result[exponents] = updated
                else:
                    result.pop(exponents, None)
        return BC(result)


def determinant_bc(matrix: list[list[BC]]) -> BC:
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix), "square BC matrix")
    states = {0: BC.const(1)}
    for row in matrix:
        next_states = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                term = value * entry
                before = sum(
                    1 for index in range(column) if not mask & (1 << index)
                )
                if before % 2:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    term if new_mask not in next_states
                    else next_states[new_mask] + term
                )
        states = next_states
    return states.get((1 << size) - 1, BC.const(0))


def h4_a0_family():
    d0 = p + q - 1
    rank_denominator = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    b_numerator = (
        p**3 * q**2 - p**3 + p**2 * q**3 - 3 * p**2 * q**2 + p**2
        - 2 * p * q**3 + 3 * p * q**2 - 2 * p + q**2 - 3 * q + 2
    )
    c_numerator = (
        p**2 * q**2 - 2 * p**2 * q - 3 * p * q**2 + p * q + p
        - q**2 + 3 * q - 2
    )
    return {
        "s": Kpq.convert(sp.cancel((p + q - p * q) / d0)),
        "b": Kpq.convert(sp.cancel(-b_numerator / ((p**2 - p + 1) * rank_denominator))),
        "c": Kpq.convert(sp.cancel(-c_numerator / (d0 * rank_denominator))),
    }


def build_rows(relations: tuple) -> dict[int, list[BC]]:
    support_payload = [
        [index, [[list(indices), coefficient] for indices, coefficient in relations[index]]]
        for index in PINNED_GLD101_SUPPORT_ROWS
    ]
    digest = hashlib.sha256(
        json.dumps(support_payload, separators=(",", ":")).encode()
    ).hexdigest()
    require(digest == EXPECTED_SUPPORT_DIGEST, f"support digest: {digest}")

    family = h4_a0_family()
    leaves = [
        [BC.const(1), BC.const(1), BC.const(1)],
        [BC.const(p), BC.const(q), BC.const(family["s"])],
        [
            BC.const(0),
            BC.const(1 + family["b"]) + BC.var((1, 0)),
            BC.const(1 + family["c"]) + BC.var((0, 1)),
        ],
    ]
    rows = {}
    for row_index in SUPPORT_ROWS:
        entries = []
        for root in range(3):
            for component in range(3):
                value = BC.const(0)
                for indices, coefficient in relations[row_index]:
                    if indices[0] != root:
                        continue
                    value = value + BC.const(coefficient) * (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                entries.append(value)
        rows[row_index] = entries
    return rows


def delta_expression() -> sp.Expr:
    d0 = p + q - 1
    P = p**2 - p + 1
    L1 = p**2 + 2 * p * q - 2 * p - q
    L2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    return sp.expand((p - q) * d0 * P * L1 * L2 * e)


def clear_open_denominator(minor: BC, selector: str) -> sp.Poly:
    require((0, 0) not in minor.terms, f"{selector} constant offset")
    require(set(minor.terms) <= EXPECTED_OFFSET_SUPPORT, f"{selector} offset support")
    ratio = sp.cancel(
        sum(
            coefficient.as_expr() * B ** (degree_b + degree_c - 1) * t**degree_c
            for (degree_b, degree_c), coefficient in minor.terms.items()
        )
    )
    numerator, denominator = ratio.as_numer_denom()
    denominator_poly = sp.Poly(denominator, p, q, B, t, domain=QQ)
    require(not denominator_poly.is_zero, f"{selector} zero denominator")
    require(
        not (denominator_poly.as_expr().free_symbols & {B, t}),
        f"{selector} offset denominator",
    )
    delta_poly = sp.Poly(delta_expression(), p, q, domain=QQ)
    _content, factors = sp.factor_list(denominator_poly.as_expr())
    require(bool(factors), f"{selector} missing declared denominator")
    for factor, _exponent in factors:
        factor_poly = sp.Poly(factor, p, q, domain=QQ)
        common = sp.gcd(delta_poly, factor_poly).monic()
        require(common == factor_poly.monic(), f"{selector} denominator outside Delta")

    polynomial = sp.Poly(sp.expand(numerator), p, q, B, t, domain=QQ)
    _content, primitive = polynomial.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def reduce_p(polynomial: sp.Poly, r8: sp.Poly) -> sp.Poly:
    coefficient_domain = QQ.poly_ring(q, B, t)
    source = sp.Poly(polynomial.as_expr(), p, domain=coefficient_domain)
    modulus = sp.Poly(r8.as_expr(), p, domain=coefficient_domain)
    remainder = source.rem(modulus)
    reduced = sp.Poly(remainder.as_expr(), p, q, B, t, domain=QQ)
    _content, primitive = reduced.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def coefficient_row(polynomial: sp.Poly) -> list[sp.Expr]:
    grouped = {exponents: sp.Integer(0) for exponents in MONOMIAL_EXPONENTS}
    for (degree_p, degree_q, degree_b, degree_t), coefficient in polynomial.terms():
        exponents = (degree_b, degree_t)
        require(exponents in grouped, f"unexpected B,t support: {exponents}")
        grouped[exponents] += coefficient * p**degree_p * q**degree_q
    return [sp.expand(grouped[exponents]) for exponents in MONOMIAL_EXPONENTS]


def field_element(expression: sp.Expr, field, minpoly: sp.Poly):
    polynomial = sp.Poly(expression, p, domain=QQ).rem(minpoly)
    value = field.zero
    for (degree_p,), coefficient in polynomial.terms():
        value += field.convert(coefficient) * field.unit**degree_p
    return value


def q_polynomial(expression: sp.Expr, field, minpoly: sp.Poly) -> sp.Poly:
    polynomial = sp.Poly(expression, p, q, domain=QQ)
    coefficients = {}
    for (degree_p, degree_q), coefficient in polynomial.terms():
        term = field.convert(coefficient) * field.unit**degree_p
        coefficients[degree_q] = coefficients.get(degree_q, field.zero) + term
    return sp.Poly.from_dict(
        {(degree,): value for degree, value in coefficients.items() if value},
        (q,),
        domain=field,
    )


def row_gcd(q6: sp.Poly, row: list[sp.Poly]) -> sp.Poly:
    value = q6
    for entry in row:
        value = value.gcd(entry)
    return value.monic()


def check() -> dict[str, object]:
    require(
        lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256,
        "certificate LF hash",
    )
    for path, expected in EXPECTED_LF_SHA256.items():
        actual = lf_sha256(path)
        require(actual == expected, f"source pin {path.name}: {actual}")

    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(payload.get("global_conjecture") == "UNRESOLVED", "global status")
    require(tuple(payload["algebra"]["matrix"]) == SELECTOR_ORDER, "matrix order")
    expected_definitions = {
        name: {"rows": list(rows), "columns": list(columns)}
        for name, (rows, columns) in SELECTORS.items()
    }
    require(payload["selector_definitions"] == expected_definitions, "selector definitions")
    pins = payload["source_pins"]
    require(pins["GLD71_lf_sha256"] == EXPECTED_LF_SHA256[GLD71], "GLD71 payload pin")
    require(pins["GLD88_lf_sha256"] == EXPECTED_LF_SHA256[GLD88], "GLD88 payload pin")
    require(pins["GLD101_owner_lf_sha256"] == EXPECTED_LF_SHA256[GLD101_OWNER], "owner payload pin")
    require(pins["GLD101_support_digest"] == EXPECTED_SUPPORT_DIGEST, "support payload pin")

    certificate_r8 = parse_polynomial(payload["algebra"]["minpoly_R8"])
    certificate_q6 = parse_polynomial(payload["algebra"]["Q6"])
    require(sp.expand(certificate_r8 - R8_EXPRESSION) == 0, "independent R8 transcription")
    require(sp.expand(certificate_q6 - Q6_EXPRESSION) == 0, "independent Q6 transcription")
    r8 = sp.Poly(R8_EXPRESSION, p, domain=QQ).monic()
    require(r8.is_irreducible, "R8 irreducibility")
    field = QQ.algebraic_field((r8, alpha))
    q6 = q_polynomial(Q6_EXPRESSION, field, r8)
    require(q6.degree() == 4 and q6.gcd(q6.diff()).degree() == 0, "Q6 squarefree")

    relations = load_literal_relations()
    rows = build_rows(relations)
    certificate_matrix = payload["algebra"]["matrix"]
    audit_rows = []
    total_cross_products = 0
    for selector in SELECTOR_ORDER:
        row_indices, columns = SELECTORS[selector]
        matrix = [[rows[row][column] for column in columns] for row in row_indices]
        minor = determinant_bc(matrix)
        cleared = clear_open_denominator(minor, selector)
        reduced = reduce_p(cleared, r8)
        direct_row = [
            q_polynomial(entry, field, r8).rem(q6)
            for entry in coefficient_row(reduced)
        ]
        tracked_row = [
            q_polynomial(parse_polynomial(entry), field, r8).rem(q6)
            for entry in certificate_matrix[selector]
        ]
        require(row_gcd(q6, direct_row).degree() == 0, f"{selector} audit row unimodular")
        require(row_gcd(q6, tracked_row).degree() == 0, f"{selector} certificate row unimodular")
        cross_count = 0
        for left, right in itertools.combinations(range(6), 2):
            cross = (
                direct_row[left] * tracked_row[right]
                - direct_row[right] * tracked_row[left]
            ).rem(q6)
            require(cross.is_zero, f"{selector} cross product {left + 1},{right + 1}")
            cross_count += 1
        require(cross_count == 15, f"{selector} cross-product count")
        total_cross_products += cross_count
        audit_rows.append(selector)
        print(f"[R8 no-import audit] {selector}: unit-equivalent", file=sys.stderr, flush=True)

    audit_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_modules = set()
    for node in ast.walk(audit_tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module.split(".")[0])
    require(
        imported_modules
        <= {"__future__", "ast", "hashlib", "itertools", "json", "re", "sys", "pathlib", "sympy"},
        f"unexpected audit imports: {sorted(imported_modules)}",
    )

    return {
        "status": "independent_direct_matrix_r8_five_row_audit_passed",
        "global_conjecture": "UNRESOLVED",
        "scope": "GLD101 a=0,R8,V(Q6),D(B*H2*Delta), selected necessary minors T1,T2,T3,Y1,X3 only",
        "repository_modules_imported": 0,
        "literal_GLD71_relation_rows": len(relations),
        "selectors_rebuilt": audit_rows,
        "unimodular_row_pairs": len(audit_rows),
        "zero_cross_products": total_cross_products,
        "certificate_lf_sha256": EXPECTED_CERTIFICATE_LF_SHA256,
        "nonclaims": payload["mathematical_scope"]["nonclaims"],
    }


def main() -> None:
    print(json.dumps(check(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
