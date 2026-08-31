#!/usr/bin/env python3
"""Independent direct-matrix audit of the portable GLD101 d2 B-open leaf.

The audit imports no repository module and no primary checker.  It AST-parses
the literal GLD71 ``SPARSE_RELATIONS`` table from a hash-pinned tracked file,
locally transcribes the hash-pinned GLD88 a=0 H4 chart, specializes p=i,
rebuilds all six actual seven-by-seven minors, substitutes C=B*t, cancels the
reversible common B factor, checks every cleared denominator against Delta,
and reduces the resulting numerators modulo Q6.  The six primitive Gaussian
equations and the deterministic compact Singular source are then compared
with the tracked certificate.

The p=-i branch follows coefficientwise by conjugation of the rational parent
equations; that symmetry is checked explicitly for the chart, Q6, and Delta.
This is selected-necessary-minor evidence only.  There is no selector converse,
B=0/C-open or endpoint coverage, P6/P8 theorem, arbitrary-a/full-E31 claim, or
global Krenn--Gu resolution.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from typing import Any, Sequence

import sympy as sp
from sympy import QQ_I


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
GLD101 = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py"
GLD102_AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py"
CERTIFICATE = BASE / "certificates" / (
    "GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_CERTIFICATE.json"
)

EXPECTED_SOURCE_LF_SHA256 = {
    GLD71: "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    GLD88: "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    GLD101: "c36d618651b92621627961d3004128f39cb43e522a76256c74b1141baf9d1a3c",
    GLD102_AUDIT: "3d976c4e9470a4c5acece6052acd275b96dc257b82cc197183375825ec6082ec",
}
EXPECTED_CERTIFICATE_LF_SHA256 = (
    "e4d0c5a07a930d8c4305a897e613b73185d48df885f9907f0e67a41fc593338c"
)
EXPECTED_SUPPORT_DIGEST = (
    "f2670c9393287eae16dce1bc8aa41e4b0c421645833ad29619a6d7b6fd94ac07"
)
EXPECTED_SINGULAR_SOURCE_SHA256 = (
    "58530b32e87ff5a4198478c375755ed0452a4c6351ee234872796155c2dd4199"
)

q, B, t = sp.symbols("q B t")
SELECTORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTOR_NAMES = tuple(SELECTORS)
SUPPORT_ROWS = tuple(sorted({row for rows, _columns in SELECTORS.values() for row in rows}))


class PortableD2AuditError(RuntimeError):
    """Fail-closed independent-source, arithmetic, or certificate mismatch."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def extract_literal_assignment(path: Path, name: str) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
        ):
            return ast.literal_eval(node.value)
    raise PortableD2AuditError(f"literal assignment {name} not found in {path.name}")


def load_relations() -> tuple[Any, ...]:
    for path, expected in EXPECTED_SOURCE_LF_SHA256.items():
        actual = lf_sha256(path)
        if actual != expected:
            raise PortableD2AuditError(
                f"pinned parent source drift: {path.name}: {actual}"
            )
    relations = extract_literal_assignment(GLD71, "SPARSE_RELATIONS")
    if not isinstance(relations, tuple) or len(relations) != 37:
        raise PortableD2AuditError("GLD71 relation table is not the literal 37-row tuple")
    payload = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in relations[row]],
        ]
        for row in SUPPORT_ROWS
    ]
    digest = sha256_bytes(json.dumps(payload, separators=(",", ":")).encode())
    if digest != EXPECTED_SUPPORT_DIGEST:
        raise PortableD2AuditError(f"selected GLD71 support digest mismatch: {digest}")
    return relations


def load_certificate() -> dict[str, Any]:
    digest = lf_sha256(CERTIFICATE)
    if digest != EXPECTED_CERTIFICATE_LF_SHA256:
        raise PortableD2AuditError(f"certificate LF hash mismatch: {digest}")
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    payload = json.loads(raw.decode("utf-8"))
    if raw != (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode():
        raise PortableD2AuditError("certificate is not canonical sorted JSON")
    if payload.get("global_conjecture") != "UNRESOLVED":
        raise PortableD2AuditError("global status must remain UNRESOLVED")
    if set(payload["selected_minor_equations"]) != set(SELECTOR_NAMES):
        raise PortableD2AuditError("certificate selector ordering drift")
    if tuple(payload["mathematical_scope"]["compact_unit_core"]) != (
        "T3",
        "Y1",
        "X3",
    ):
        raise PortableD2AuditError("certificate compact core drift")
    for name, (rows, columns) in SELECTORS.items():
        definition = payload["selector_definitions"][name]
        if tuple(definition["rows"]) != rows or tuple(definition["columns"]) != columns:
            raise PortableD2AuditError(f"{name} selector definition drift")
    return payload


def h4_family(p_value: sp.Expr, q_value: sp.Expr, a_value: sp.Expr) -> dict[str, sp.Expr]:
    """Literal GLD88 F88 chart transcription, pinned above but not imported."""
    d0 = p_value + q_value - 1
    e = (
        2 * p_value * q_value**2
        - 2 * p_value * q_value
        - p_value
        - q_value**2
        - 2 * q_value
        + 2
    )
    nb = (
        -2 * a_value * p_value**2 * q_value**3
        + 3 * a_value * p_value**2 * q_value**2
        - 3 * a_value * p_value**2 * q_value
        + a_value * p_value**2
        + 2 * a_value * p_value * q_value**3
        + 2 * a_value * p_value
        + a_value * q_value**3
        - 3 * a_value * q_value**2
        + 3 * a_value * q_value
        - 2 * a_value
        + p_value**3 * q_value**2
        - p_value**3
        + p_value**2 * q_value**3
        - 3 * p_value**2 * q_value**2
        + p_value**2
        - 2 * p_value * q_value**3
        + 3 * p_value * q_value**2
        - 2 * p_value
        + q_value**2
        - 3 * q_value
        + 2
    )
    nc = (
        2 * a_value * p_value * q_value**3
        - 3 * a_value * p_value * q_value**2
        + 3 * a_value * p_value * q_value
        - a_value * p_value
        - a_value * q_value**3
        + 3 * a_value * q_value**2
        - 3 * a_value * q_value
        + 2 * a_value
        + p_value**2 * q_value**2
        - 2 * p_value**2 * q_value
        - 3 * p_value * q_value**2
        + p_value * q_value
        + p_value
        - q_value**2
        + 3 * q_value
        - 2
    )
    return {
        "s": sp.cancel((p_value + q_value - p_value * q_value) / d0),
        "b": sp.cancel(-nb / ((p_value**2 - p_value + 1) * e)),
        "c": sp.cancel(-nc / (d0 * e)),
    }


def q6_expression(p_value: sp.Expr, q_value: sp.Expr) -> sp.Expr:
    return (
        2 * p_value**4 * q_value**2
        - 2 * p_value**4 * q_value
        + p_value**4
        + 2 * p_value**3 * q_value**3
        - 7 * p_value**3 * q_value**2
        + 5 * p_value**3 * q_value
        - 2 * p_value**3
        + 2 * p_value**2 * q_value**4
        - 7 * p_value**2 * q_value**3
        + 12 * p_value**2 * q_value**2
        - 7 * p_value**2 * q_value
        + 2 * p_value**2
        - 2 * p_value * q_value**4
        + 5 * p_value * q_value**3
        - 7 * p_value * q_value**2
        + 2 * p_value * q_value
        + q_value**4
        - 2 * q_value**3
        + 2 * q_value**2
    )


def delta_expression(p_value: sp.Expr, q_value: sp.Expr) -> sp.Expr:
    return sp.expand(
        (p_value - q_value)
        * (p_value + q_value - 1)
        * (p_value**2 - p_value + 1)
        * (p_value**2 + 2 * p_value * q_value - 2 * p_value - q_value)
        * (2 * p_value * q_value - p_value + q_value**2 - 2 * q_value)
        * (
            2 * p_value * q_value**2
            - 2 * p_value * q_value
            - p_value
            - q_value**2
            - 2 * q_value
            + 2
        )
    )


def coefficientwise_conjugate(expression: sp.Expr) -> sp.Expr:
    return sp.expand(expression.xreplace({sp.I: -sp.I}))


def check_conjugation() -> None:
    plus = h4_family(sp.I, q, sp.Integer(0))
    minus = h4_family(-sp.I, q, sp.Integer(0))
    for coordinate in ("s", "b", "c"):
        if sp.cancel(minus[coordinate] - coefficientwise_conjugate(plus[coordinate])) != 0:
            raise PortableD2AuditError(f"H4 {coordinate} conjugation mismatch")
    if sp.expand(q6_expression(-sp.I, q)) != coefficientwise_conjugate(
        sp.expand(q6_expression(sp.I, q))
    ):
        raise PortableD2AuditError("Q6 conjugation mismatch")
    if delta_expression(-sp.I, q) != coefficientwise_conjugate(
        delta_expression(sp.I, q)
    ):
        raise PortableD2AuditError("Delta conjugation mismatch")


def direct_rows(relations: tuple[Any, ...], leaf: list[list[sp.Expr]]) -> dict[int, list[sp.Expr]]:
    return {
        row: [
            sp.expand(
                sum(
                    coefficient
                    * leaf[indices[1]][component]
                    * leaf[indices[2]][component]
                    * leaf[indices[3]][component]
                    for indices, coefficient in relations[row]
                    if indices[0] == root
                )
            )
            for root in range(3)
            for component in range(3)
        ]
        for row in SUPPORT_ROWS
    }


def gaussian_poly(expression: sp.Expr, *variables: sp.Symbol) -> sp.Poly:
    return sp.Poly(sp.expand(expression), *variables, extension=sp.I)


def integral_gaussian_poly(polynomial: sp.Poly) -> sp.Poly:
    denominator_lcm = 1
    components: list[tuple[sp.Rational, sp.Rational]] = []
    for coefficient in polynomial.coeffs():
        real, imaginary = sp.expand(coefficient).as_real_imag()
        pair = (sp.Rational(real), sp.Rational(imaginary))
        components.append(pair)
        denominator_lcm = sp.ilcm(
            denominator_lcm, int(pair[0].q), int(pair[1].q)
        )
    common = 0
    for value in (
        abs(int(component * denominator_lcm))
        for pair in components
        for component in pair
        if component != 0
    ):
        common = sp.igcd(common, value)
    if common == 0:
        raise PortableD2AuditError("cannot normalize a zero Gaussian polynomial")
    scaled = sp.expand(polynomial.as_expr() * sp.Rational(denominator_lcm, common))
    return gaussian_poly(scaled, *polynomial.gens)


def clear_declared_denominators(
    expression: sp.Expr, delta: sp.Expr
) -> tuple[sp.Expr, list[list[Any]]]:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    if denominator.free_symbols - {q}:
        raise PortableD2AuditError(f"offset variable entered denominator: {denominator}")
    denominator_poly = sp.Poly(denominator, q, extension=sp.I)
    delta_poly = sp.Poly(delta, q, extension=sp.I)
    factors: list[list[Any]] = []
    for factor, exponent in sp.factor_list(
        denominator_poly.as_expr(), extension=sp.I
    )[1]:
        factor_poly = sp.Poly(factor, q, extension=sp.I)
        if sp.gcd(delta_poly, factor_poly).monic() != factor_poly.monic():
            raise PortableD2AuditError(
                f"minor denominator factor lies outside Delta: {factor}"
            )
        factors.append([sp.sstr(factor), int(exponent)])
    polynomial = gaussian_poly(numerator, q, B, t)
    _denominator, integral = polynomial.clear_denoms(convert=True)
    return integral.as_expr(), factors


def reduce_q6(expression: sp.Expr, q6: sp.Expr) -> sp.Poly:
    coefficient_domain = QQ_I.poly_ring(B, t)
    polynomial = sp.Poly(sp.expand(expression), q, domain=coefficient_domain)
    modulus = sp.Poly(sp.expand(q6), q, domain=coefficient_domain)
    remainder = polynomial.rem(modulus)
    return integral_gaussian_poly(gaussian_poly(remainder.as_expr(), q, B, t))


def gaussian_polynomial_digest(polynomial: sp.Poly) -> str:
    encoded = []
    for monomial, coefficient in polynomial.terms():
        real, imaginary = sp.expand(coefficient).as_real_imag()
        real = sp.Rational(real)
        imaginary = sp.Rational(imaginary)
        encoded.append(
            [
                list(monomial),
                int(real.p),
                int(real.q),
                int(imaginary.p),
                int(imaginary.q),
            ]
        )
    return sha256_bytes(json.dumps(encoded, separators=(",", ":")).encode("ascii"))


def singular(expression: sp.Expr) -> str:
    return sp.sstr(sp.expand(expression)).replace("**", "^").replace("I", "i")


def parse_singular_polynomial(text: str) -> sp.Poly:
    python_text = re.sub(r"\bi\b", "I", text.replace("^", "**"))
    expression = sp.sympify(
        python_text, locals={"I": sp.I, "q": q, "B": B, "t": t}
    )
    return gaussian_poly(expression, q, B, t)


SOURCE_SUFFIX = (
    "// Exact minimum-cardinality core found by the sealed selector scout.",
    "// Rank<=6 implies T3=Y1=X3=0; no selector converse is used.",
    "ideal I=Q6,H_T3,H_Y1,H_X3,z*B*Delta-1;",
    "timer=1;",
    "matrix T;",
    "ideal L=liftstd(I,T);",
    'print("LIFT_SECONDS");',
    "timer;",
    'print("BASIS_SIZE");',
    "size(L);",
    'print("BASIS_BEGIN");',
    "L;",
    'print("BASIS_END");',
    "int unit_column=0;",
    "int column;",
    "for (column=1;column<=size(L);column++)",
    "{",
    "  if ((L[column]!=0)&&(deg(L[column])==0)) { unit_column=column; }",
    "}",
    'print("UNIT_COLUMN");',
    "unit_column;",
    'if (unit_column==0) { print("ERROR_NO_UNIT_COLUMN"); quit; }',
    "poly unit_value=L[unit_column];",
    'print("UNIT_VALUE");',
    "unit_value;",
    'print("LIFT_MATRIX_CHECK_BEGIN");',
    "matrix(I)*T-matrix(L);",
    'print("LIFT_MATRIX_CHECK_END");',
    "poly identity=0;",
    "poly multiplier;",
    "int row;",
    "int nonzero_multipliers=0;",
    'print("NORMALIZED_MULTIPLIERS_BEGIN");',
    "for (row=1;row<=nrows(T);row++)",
    "{",
    "  multiplier=T[row,unit_column]/unit_value;",
    "  identity=identity+I[row]*multiplier;",
    "  if (multiplier!=0) { nonzero_multipliers=nonzero_multipliers+1; }",
    '  print("MULTIPLIER_ROW"); row;',
    '  print("MULTIPLIER_DEGREE_TERMS");',
    "  if (multiplier==0) { -1; } else { deg(multiplier); }",
    "  size(multiplier);",
    '  print("MULTIPLIER_POLYNOMIAL"); multiplier;',
    "}",
    'print("NORMALIZED_MULTIPLIERS_END");',
    'print("NONZERO_MULTIPLIERS");',
    "nonzero_multipliers;",
    'print("IDENTITY_SUM_MINUS_ONE");',
    "simplify(identity-1,2);",
    'print("CERTIFICATE_EXACT 1");',
    'print("RUN_COMPLETE 1");',
    "quit;",
)


def render_source(
    q6: sp.Poly, delta: sp.Poly, equations: dict[str, sp.Poly]
) -> str:
    lines = [
        "// Juniper independent direct-matrix GLD101 d2 B-open audit v1",
        "// p=i; p=-i is coefficientwise conjugate.",
        "// Selected-minor ideal only; no rank converse or global claim.",
        "ring r=(0,i),(q,B,t,z),dp;",
        "minpoly=i^2+1;",
        "option(redSB);",
        f"poly Q6={singular(q6.as_expr())};",
        f"poly Delta={singular(delta.as_expr())};",
    ]
    lines.extend(
        f"poly H_{name}={singular(equations[name].as_expr())};"
        for name in SELECTOR_NAMES
    )
    lines.extend(SOURCE_SUFFIX)
    return "\n".join(lines) + "\n"


def audit() -> dict[str, Any]:
    started = time.monotonic()
    payload = load_certificate()
    relations = load_relations()
    check_conjugation()

    family = h4_family(sp.I, q, sp.Integer(0))
    leaf = [
        [sp.Integer(1), sp.Integer(1), sp.Integer(1)],
        [sp.I, q, family["s"]],
        [sp.Integer(0), 1 + family["b"] + B, 1 + family["c"] + B * t],
    ]
    rows = direct_rows(relations, leaf)
    q6_raw = sp.expand(q6_expression(sp.I, q))
    delta_raw = sp.expand(delta_expression(sp.I, q))
    q6_poly = sp.Poly(q6_raw, q, extension=sp.I)
    if q6_poly.degree() != 4 or sp.gcd(q6_poly, q6_poly.diff()).degree() != 0:
        raise PortableD2AuditError("p=i Q6 is not a squarefree quartic")
    if sp.gcd(q6_poly, sp.Poly(delta_raw, q, extension=sp.I)).degree() != 0:
        raise PortableD2AuditError("p=i Q6 meets Delta")
    h2_at_i = sp.expand(2 * sp.I**2 - 2 * sp.I + 1)
    h2_real, h2_imaginary = h2_at_i.as_real_imag()
    if h2_at_i != -1 - 2 * sp.I or h2_real**2 + h2_imaginary**2 != 5:
        raise PortableD2AuditError("H2(i) Gaussian norm gate failed")

    equations: dict[str, sp.Poly] = {}
    denominator_factors: dict[str, list[list[Any]]] = {}
    for name, (rowset, columns) in SELECTORS.items():
        print(f"[d2 portable audit] actual minor {name}", file=sys.stderr, flush=True)
        matrix = sp.Matrix([[rows[row][column] for column in columns] for row in rowset])
        determinant = sp.cancel(matrix.det(method="domain-ge"))
        divided = sp.cancel(determinant / B)
        if sp.cancel(determinant - B * divided) != 0:
            raise PortableD2AuditError(f"{name} common B cancellation failed")
        numerator, factors = clear_declared_denominators(divided, delta_raw)
        equation = reduce_q6(numerator, q6_raw)
        if equation.is_zero:
            raise PortableD2AuditError(f"{name} vanished modulo Q6")
        equations[name] = equation
        denominator_factors[name] = factors

        record = payload["selected_minor_equations"][name]
        tracked = parse_singular_polynomial(record["singular_polynomial"])
        if tracked != equation:
            raise PortableD2AuditError(f"{name} reconstructed equation mismatch")
        digest = gaussian_polynomial_digest(equation)
        if digest != record["scaled_sha256"]:
            raise PortableD2AuditError(f"{name} reconstructed digest mismatch")
        if len(equation.terms()) != record["terms"]:
            raise PortableD2AuditError(f"{name} reconstructed term-count mismatch")
        if factors != record["cleared_denominator_factors"]:
            raise PortableD2AuditError(f"{name} denominator-factor lineage mismatch")

    q6_integral = integral_gaussian_poly(q6_poly)
    delta_integral = integral_gaussian_poly(
        sp.Poly(delta_raw, q, extension=sp.I).rem(q6_poly)
    )
    source = render_source(q6_integral, delta_integral, equations)
    source_digest = sha256_bytes(source.encode("utf-8"))
    if source_digest != EXPECTED_SINGULAR_SOURCE_SHA256:
        raise PortableD2AuditError(
            f"independently regenerated Singular source mismatch: {source_digest}"
        )
    if source_digest != payload["singular_unit_lift"]["source_sha256"]:
        raise PortableD2AuditError("certificate Singular source pin mismatch")
    if len(source.splitlines()) != payload["singular_unit_lift"]["source_line_count"]:
        raise PortableD2AuditError("Singular source line count drift")

    return {
        "status": "independent_direct_matrix_d2_bopen_portable_audit_passed",
        "global_conjecture": "UNRESOLVED",
        "scope": "a=0,p^2+1=0,V(Q6),D(B*H2*Delta),selected necessary minors only",
        "repository_modules_imported": 0,
        "gld71_literal_rows_parsed": len(relations),
        "actual_minors_rebuilt": list(SELECTOR_NAMES),
        "common_B_factor_cancelled": list(SELECTOR_NAMES),
        "denominator_factors_checked_inside_Delta": denominator_factors,
        "compact_unit_core": ["T3", "Y1", "X3"],
        "p_minus_i_conjugation_checked": True,
        "singular_source_sha256": source_digest,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "nonclaims_preserved": True,
    }


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise PortableD2AuditError("this audit accepts no arguments")
    print(json.dumps(audit(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
