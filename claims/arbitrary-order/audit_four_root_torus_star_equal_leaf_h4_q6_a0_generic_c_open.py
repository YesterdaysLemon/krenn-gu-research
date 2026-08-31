#!/usr/bin/env python3
"""No-repository-import audit of the GLD101 generic C-open leaf.

The audit parses the literal GLD71 syndrome table without importing or
executing a repository module and transcribes the hash-pinned normalized
a=0 GLD88 chart locally.  It uses C-dual arithmetic in QQ(p)[q]/(Q6), rather
than the primary checker's full sparse B,C determinant representation, to
rebuild the six disclosed C coefficients.  It then parses the tracked
Singular source with a restricted polynomial parser and independently
recomputes the 6-by-4 rank cover with explicit 4-by-4 Leibniz determinants.

Only the selected necessary minors are covered.  There is no selector
converse, P8 theorem, full-E31 closure, physical-incidence statement, or
global Krenn--Gu resolution.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATES = BASE / "certificates"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD101_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md"
)
GLD101_CANONICAL = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py"
)
SOURCE = CERTIFICATES / "GLD101_A0_GENERIC_COPEN_UNIT_SCREEN.singular.txt"
CERTIFICATE = CERTIFICATES / "GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json"

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "1f84c1d30c1c8403be477b5def91144f687cc08a4ed5406dffb3866cf6996afb"
)
EXPECTED_LF_SHA256 = {
    GLD71: "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    GLD88: "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    GLD101_OWNER: "fe9e705f2fa9cde61c71daeb19abea241545a6c45611c15e6dd03b62ea6d3f45",
    GLD101_CANONICAL: "c36d618651b92621627961d3004128f39cb43e522a76256c74b1141baf9d1a3c",
    SOURCE: "c514d842532f99cde4488cca048c551f39e43ed5cdf2c5ce6a54dcd7aa704850",
}
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
PINNED_SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
SELECTORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTOR_ORDER = tuple(SELECTORS)
USED_ROWS = tuple(sorted({row for rows, _columns in SELECTORS.values() for row in rows}))
DECLARATIONS = (
    "Q6",
    "H2",
    "Delta",
    "H_T0",
    "H_T1",
    "H_T2",
    "H_T3",
    "H_Y1",
    "H_X3",
)

p, q, z = sp.symbols("p q z")
K = QQ.frac_field(p)
VARIABLES = (q, p, z)
DECLARATION_RE = re.compile(r"^poly ([A-Za-z][A-Za-z0-9_]*)=(.*);$")
FACTOR_RE = re.compile(r"([qpz])(?:\^(\d+))?$")


class AuditError(RuntimeError):
    """Fail-closed independent-audit mismatch."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(lf_bytes(path)).hexdigest()


def validate_hashes() -> None:
    for path, expected in EXPECTED_LF_SHA256.items():
        require(path.is_file(), f"missing pinned source {path}")
        observed = lf_sha256(path)
        require(observed == expected, f"LF hash mismatch for {path}: {observed}")
    require(CERTIFICATE.is_file(), f"missing certificate {CERTIFICATE}")
    require(
        lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256,
        "certificate LF hash mismatch",
    )


def q6_expression() -> sp.Expr:
    return sp.expand(
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


def h4_a0_chart() -> dict[str, sp.Expr]:
    d0 = p + q - 1
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
        "s": sp.cancel((p + q - p * q) / d0),
        "b": sp.cancel(-b_numerator / ((p**2 - p + 1) * rank_denominator)),
        "c": sp.cancel(-c_numerator / (d0 * rank_denominator)),
        "rank_denominator": rank_denominator,
    }


def delta_expression(chart: dict[str, sp.Expr]) -> sp.Expr:
    return sp.expand(
        (p - q)
        * (p + q - 1)
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * chart["rank_denominator"]
    )


def load_literal_relations() -> tuple:
    tree = ast.parse(GLD71.read_text(encoding="utf-8"), filename=str(GLD71))
    matches = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(
            isinstance(target, ast.Name) and target.id == "SPARSE_RELATIONS"
            for target in targets
        ):
            matches.append(ast.literal_eval(node.value))
    require(len(matches) == 1, "expected one literal SPARSE_RELATIONS assignment")
    relations = matches[0]
    require(isinstance(relations, tuple) and len(relations) == 37, "relation table shape")
    payload = [
        [
            index,
            [[list(indices), coefficient] for indices, coefficient in relations[index]],
        ]
        for index in PINNED_SUPPORT_ROWS
    ]
    observed = hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    require(observed == EXPECTED_SUPPORT_DIGEST, f"support digest mismatch: {observed}")
    return relations


class QuotientAlgebra:
    """Exact arithmetic in QQ(p)[q]/(Q6), implemented locally."""

    def __init__(self) -> None:
        self.modulus = sp.Poly(q6_expression(), q, domain=K)
        require(self.modulus.degree() == 4, "Q6 q-degree")
        self.zero = (K.zero, K.zero, K.zero, K.zero)
        self.one = (K.one, K.zero, K.zero, K.zero)
        self.inverse_cache: dict[tuple[Any, ...], tuple[Any, ...]] = {}
        lead = K.convert(self.modulus.LC())
        self.relation = tuple(
            -K.convert(self.modulus.nth(index)) / lead for index in range(4)
        )

    def add(self, left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[Any, ...]:
        return tuple(left[index] + right[index] for index in range(4))

    def negate(self, value: tuple[Any, ...]) -> tuple[Any, ...]:
        return tuple(-coefficient for coefficient in value)

    def multiply(
        self, left: tuple[Any, ...], right: tuple[Any, ...]
    ) -> tuple[Any, ...]:
        raw = [K.zero] * 7
        for left_index, left_coefficient in enumerate(left):
            if left_coefficient == K.zero:
                continue
            for right_index, right_coefficient in enumerate(right):
                if right_coefficient != K.zero:
                    raw[left_index + right_index] += left_coefficient * right_coefficient
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high == K.zero:
                continue
            for index, coefficient in enumerate(self.relation):
                raw[degree - 4 + index] += high * coefficient
        return tuple(raw[:4])

    def from_expr(self, expression: object) -> tuple[Any, ...]:
        numerator, denominator = sp.cancel(sp.sympify(expression)).as_numer_denom()
        numerator_poly = sp.Poly(numerator, q, domain=K).rem(self.modulus)
        denominator_poly = sp.Poly(denominator, q, domain=K).rem(self.modulus)
        require(not denominator_poly.is_zero, "zero chart denominator modulo Q6")
        key = tuple(K.convert(denominator_poly.nth(index)) for index in range(4))
        inverse = self.inverse_cache.get(key)
        if inverse is None:
            try:
                inverse_poly = sp.invert(denominator_poly, self.modulus)
            except sp.NotInvertible as error:
                raise AuditError("chart denominator not invertible modulo Q6") from error
            inverse = tuple(K.convert(inverse_poly.nth(index)) for index in range(4))
            self.inverse_cache[key] = inverse
        converted = tuple(K.convert(numerator_poly.nth(index)) for index in range(4))
        return self.multiply(converted, inverse)

    def to_expr(self, value: tuple[Any, ...]) -> sp.Expr:
        return sp.expand(
            sum(sp.sympify(value[index].as_expr()) * q**index for index in range(4))
        )

    def is_zero(self, value: tuple[Any, ...]) -> bool:
        return all(coefficient == K.zero for coefficient in value)


class CDual:
    """Exact constant-plus-linear-C arithmetic over the quotient algebra."""

    def __init__(
        self,
        algebra: QuotientAlgebra,
        constant: tuple[Any, ...] | None = None,
        linear: tuple[Any, ...] | None = None,
    ) -> None:
        self.algebra = algebra
        self.constant = algebra.zero if constant is None else tuple(constant)
        self.linear = algebra.zero if linear is None else tuple(linear)

    @classmethod
    def const(cls, algebra: QuotientAlgebra, expression: object) -> "CDual":
        return cls(algebra, algebra.from_expr(expression), algebra.zero)

    @classmethod
    def variable(cls, algebra: QuotientAlgebra) -> "CDual":
        return cls(algebra, algebra.zero, algebra.one)

    def __add__(self, other: "CDual") -> "CDual":
        return CDual(
            self.algebra,
            self.algebra.add(self.constant, other.constant),
            self.algebra.add(self.linear, other.linear),
        )

    def __neg__(self) -> "CDual":
        return CDual(
            self.algebra,
            self.algebra.negate(self.constant),
            self.algebra.negate(self.linear),
        )

    def __sub__(self, other: "CDual") -> "CDual":
        return self + (-other)

    def __mul__(self, other: "CDual") -> "CDual":
        return CDual(
            self.algebra,
            self.algebra.multiply(self.constant, other.constant),
            self.algebra.add(
                self.algebra.multiply(self.constant, other.linear),
                self.algebra.multiply(self.linear, other.constant),
            ),
        )

    def is_zero(self) -> bool:
        return self.algebra.is_zero(self.constant) and self.algebra.is_zero(self.linear)


def determinant_dual(matrix: list[list[CDual]]) -> CDual:
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix), "square determinant")
    algebra = matrix[0][0].algebra
    states: dict[int, CDual] = {0: CDual.const(algebra, 1)}
    for row in matrix:
        next_states: dict[int, CDual] = {}
        for mask, partial in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or entry.is_zero():
                    continue
                unused_before = sum(
                    1 for index in range(column) if not (mask & (1 << index))
                )
                term = partial * entry
                if unused_before & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    term
                    if new_mask not in next_states
                    else next_states[new_mask] + term
                )
        states = next_states
    return states.get((1 << size) - 1, CDual.const(algebra, 0))


def build_rows(relations: tuple, algebra: QuotientAlgebra) -> dict[int, list[CDual]]:
    chart = h4_a0_chart()
    c_variable = CDual.variable(algebra)
    leaves = (
        (CDual.const(algebra, 1), CDual.const(algebra, 1), CDual.const(algebra, 1)),
        (CDual.const(algebra, p), CDual.const(algebra, q), CDual.const(algebra, chart["s"])),
        (
            CDual.const(algebra, 0),
            CDual.const(algebra, 1 + chart["b"]),
            CDual.const(algebra, 1 + chart["c"]) + c_variable,
        ),
    )
    rows: dict[int, list[CDual]] = {}
    for row_index in USED_ROWS:
        entries: list[CDual] = []
        for root in range(3):
            for component in range(3):
                value = CDual.const(algebra, 0)
                for indices, coefficient in relations[row_index]:
                    if indices[0] != root:
                        continue
                    value = value + CDual.const(algebra, coefficient) * (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                entries.append(value)
        rows[row_index] = entries
    return rows


def canonical_primitive(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=QQ)
    if polynomial.is_zero:
        return polynomial
    _denominator, integral = polynomial.clear_denoms(convert=True)
    _content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def term_table(polynomial: sp.Poly) -> list[list[Any]]:
    return [
        [list(monomial), [int(coefficient.p), int(coefficient.q)]]
        for monomial, coefficient in polynomial.terms()
    ]


def polynomial_record(polynomial: sp.Poly, *, include_expression: bool = False) -> dict[str, Any]:
    table = term_table(polynomial)
    record: dict[str, Any] = {
        "sha256": hashlib.sha256(
            json.dumps(table, separators=(",", ":")).encode("ascii")
        ).hexdigest(),
        "term_count": len(table),
        "total_degree": int(polynomial.total_degree()) if table else -1,
    }
    if include_expression:
        record["expression"] = str(polynomial.as_expr())
    return record


def denominator_record(expression: sp.Expr) -> dict[str, Any]:
    polynomial = sp.Poly(sp.expand(expression), p, domain=QQ)
    require(
        sp.Poly(sp.expand(expression), p, q, domain=QQ).degree(q) == 0,
        "coefficient denominator depends on q",
    )
    _content, factors = sp.factor_list(polynomial.as_expr(), p)
    allowed = {
        sp.Poly(p**2 - p + 1, p, domain=QQ).monic().as_expr(): "P",
        sp.Poly(2 * p**2 - 2 * p + 1, p, domain=QQ).monic().as_expr(): "H2",
    }
    records = []
    for factor, exponent in factors:
        monic = sp.Poly(factor, p, domain=QQ).monic().as_expr()
        require(monic in allowed, f"denominator factor outside P*H2: {factor}")
        records.append(
            {"name": allowed[monic], "factor": str(monic), "exponent": int(exponent)}
        )
    records.sort(key=lambda item: item["name"])
    return {
        "expression": str(sp.factor(polynomial.as_expr())),
        "factors": records,
        "unit_on_D(H2*Delta)": True,
    }


def reconstruct(relations: tuple) -> tuple[dict[str, sp.Poly], dict[str, Any]]:
    algebra = QuotientAlgebra()
    rows = build_rows(relations, algebra)
    equations: dict[str, sp.Poly] = {}
    selectors: dict[str, Any] = {}
    for name, (row_indices, columns) in SELECTORS.items():
        # Only component columns 2,5,8 carry C, and each selected minor has
        # exactly one of them.  Therefore the dual coefficient is the entire
        # nonconstant B=0 determinant, not a truncation of a higher C power.
        require(
            len(set(columns).intersection({2, 5, 8})) == 1,
            f"{name} does not have exactly one C-bearing column",
        )
        matrix = [[rows[row][column] for column in columns] for row in row_indices]
        determinant = determinant_dual(matrix)
        require(algebra.is_zero(determinant.constant), f"{name} C-constant term")
        require(not algebra.is_zero(determinant.linear), f"{name} zero C coefficient")
        coefficient = sp.cancel(algebra.to_expr(determinant.linear))
        numerator, denominator = coefficient.as_numer_denom()
        primitive = canonical_primitive(numerator, (q, p))
        require(not primitive.is_zero and primitive.degree(q) <= 3, f"{name} numerator")
        equations[name] = primitive
        selectors[name] = {
            "rows": list(row_indices),
            "columns": list(columns),
            "B_zero_offset_terms": [[0, 1]],
            "C_coefficient_numerator": polynomial_record(primitive),
            "C_coefficient_denominator": denominator_record(denominator),
        }
    return equations, selectors


def parse_source_polynomial(expression: str) -> sp.Poly:
    require(
        not any(character.isspace() and character != " " for character in expression),
        "forbidden source whitespace",
    )
    expression = expression.replace(" ", "")
    require(bool(expression), "empty source expression")
    terms: dict[tuple[int, int, int], sp.Rational] = {}
    position = 0
    while position < len(expression):
        sign = 1
        if expression[position] == "+":
            position += 1
        elif expression[position] == "-":
            sign = -1
            position += 1
        end = position
        while end < len(expression) and expression[end] not in "+-":
            end += 1
        body = expression[position:end]
        position = end
        require(bool(body), "empty source term")
        coefficient = sp.Rational(sign)
        exponents = [0, 0, 0]
        seen: set[str] = set()
        for factor in body.split("*"):
            if re.fullmatch(r"\d+(?:/\d+)?", factor):
                coefficient *= sp.Rational(factor)
                continue
            match = FACTOR_RE.fullmatch(factor)
            require(match is not None, f"forbidden source factor {factor!r}")
            variable, exponent_text = match.groups()
            require(variable not in seen, "duplicate variable in source monomial")
            seen.add(variable)
            exponent = int(exponent_text or "1")
            require(exponent > 0, "nonpositive source exponent")
            exponents["qpz".index(variable)] = exponent
        monomial = tuple(exponents)
        require(monomial not in terms, f"duplicate source monomial {monomial}")
        terms[monomial] = coefficient
    return sp.Poly.from_dict(terms, VARIABLES, domain=QQ)


def parse_source() -> dict[str, sp.Poly]:
    text = SOURCE.read_text(encoding="utf-8")
    required = (
        "ring r=0,(q,p,z),dp;",
        "ideal I=Q6,H_T0,H_T1,H_T2,H_T3,H_Y1,H_X3,z*H2*Delta-1;",
        "ideal G=std(I);",
        "int is_unit=(size(G)==1)&&(G[1]==1);",
    )
    require(all(fragment in text for fragment in required), "Singular source structure")
    declarations: dict[str, sp.Poly] = {}
    for line in text.splitlines():
        match = DECLARATION_RE.fullmatch(line)
        if match is None:
            continue
        name, expression = match.groups()
        if name not in DECLARATIONS:
            continue
        require(name not in declarations, f"duplicate source declaration {name}")
        declarations[name] = parse_source_polynomial(expression)
    require(tuple(declarations) == DECLARATIONS, "source declaration set or order")
    return declarations


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        1
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
        if permutation[left] > permutation[right]
    )
    return -1 if inversions & 1 else 1


def determinant_4x4(matrix: list[list[sp.Expr]]) -> sp.Expr:
    require(len(matrix) == 4 and all(len(row) == 4 for row in matrix), "4x4 matrix")
    terms = []
    for permutation in itertools.permutations(range(4)):
        product = sp.Integer(permutation_sign(permutation))
        for row, column in enumerate(permutation):
            product *= matrix[row][column]
        terms.append(product)
    return sp.expand(sum(terms))


def primitive_univariate(polynomial: sp.Poly) -> sp.Poly:
    if polynomial.is_zero:
        return polynomial
    _denominator, integral = polynomial.clear_denoms(convert=True)
    _content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def rank_cover(
    declarations: dict[str, sp.Poly], equations: dict[str, sp.Poly]
) -> dict[str, Any]:
    matrix = [
        [sp.Poly(equations[name].as_expr(), q).nth(degree) for degree in (3, 2, 1, 0)]
        for name in SELECTOR_ORDER
    ]
    subset_order = list(itertools.combinations(range(6), 4))
    by_subset: dict[tuple[int, ...], sp.Poly] = {}
    for subset in reversed(subset_order):
        determinant = determinant_4x4([matrix[index] for index in subset])
        polynomial = primitive_univariate(sp.Poly(determinant, p, domain=QQ))
        require(not polynomial.is_zero, f"zero maximal minor {subset}")
        by_subset[subset] = polynomial

    common: sp.Poly | None = None
    for subset in reversed(subset_order):
        polynomial = by_subset[subset]
        common = (
            polynomial
            if common is None
            else primitive_univariate(sp.gcd(common, polynomial))
        )
    assert common is not None
    expected = sp.Poly(
        p**15
        * (p - 1) ** 6
        * (p + 1) ** 2
        * (p**2 - p + 1) ** 11
        * (2 * p**2 - 2 * p + 1) ** 14,
        p,
        domain=QQ,
    )
    require(common.monic() == expected.monic(), "maximal-minor gcd factorization")

    minors = [
        {
            "selectors": [SELECTOR_ORDER[index] for index in subset],
            **polynomial_record(by_subset[subset]),
        }
        for subset in subset_order
    ]
    combined = hashlib.sha256(
        json.dumps(minors, separators=(",", ":"), sort_keys=True).encode("ascii")
    ).hexdigest()

    special: dict[str, Any] = {}
    expected_common = {
        -1: sp.Poly(1, q, domain=QQ),
        0: sp.Poly(q**2, q, domain=QQ),
        1: sp.Poly((q - 1) ** 2, q, domain=QQ),
    }
    for p_value in (-1, 0, 1):
        q6 = sp.Poly(declarations["Q6"].as_expr().subs(p, p_value), q, domain=QQ)
        common_q = q6
        for name in reversed(SELECTOR_ORDER):
            common_q = sp.gcd(
                common_q,
                sp.Poly(equations[name].as_expr().subs(p, p_value), q, domain=QQ),
            )
        common_q = common_q.monic()
        require(common_q == expected_common[p_value].monic(), f"p={p_value} common gcd")
        delta = sp.Poly(
            declarations["Delta"].as_expr().subs(p, p_value), q, domain=QQ
        )
        q6_delta = sp.gcd(q6, delta).monic()
        if p_value in (0, 1):
            require(q6_delta == common_q, f"p={p_value} Delta closure")
        else:
            require(common_q.degree() == 0, "p=-1 common root")
        special[str(p_value)] = {
            "common_q_gcd": polynomial_record(common_q, include_expression=True),
            "gcd_Q6_Delta": polynomial_record(q6_delta, include_expression=True),
            "disposition": (
                "no common q root"
                if p_value == -1
                else "every common Q6 root lies in Delta=0"
            ),
        }
    return {
        "coefficient_matrix_shape": [6, 4],
        "coefficient_order": ["q^3", "q^2", "q", "1"],
        "maximal_minors": minors,
        "maximal_minors_combined_sha256": combined,
        "maximal_minor_gcd": {
            **polynomial_record(primitive_univariate(common), include_expression=True),
            "factorization": (
                "p^15*(p-1)^6*(p+1)^2*(p^2-p+1)^11*"
                "(2*p^2-2*p+1)^14"
            ),
        },
        "localization_exclusions": {
            "p^2-p+1": "P is a factor of Delta",
            "2*p^2-2*p+1": "this is H2",
        },
        "special_fibres": special,
        "no_common_zero_on_D(H2*Delta)": True,
    }


def check() -> dict[str, Any]:
    validate_hashes()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate["schema_version"] == 1, "certificate schema")
    require(
        certificate["certificate_id"]
        == "GLD101-a0-generic-C-open-selected-minor-rank-cover",
        "certificate id",
    )
    require(certificate["global_conjecture"] == "UNRESOLVED", "global status")
    scope = certificate["mathematical_scope"]
    require(scope["locus"] == "B=0 and C!=0", "scope locus")
    require("D(H2*Delta)" in scope["open"], "scope localization")
    require(tuple(scope["selected_necessary_minors"]) == SELECTOR_ORDER, "scope selectors")
    nonclaims = " ".join(scope["nonclaims"])
    for phrase in ("no converse", "no P8 parent theorem", "no global"):
        require(phrase in nonclaims, f"missing nonclaim: {phrase}")

    expected_paths = {
        "GLD71": GLD71,
        "GLD88": GLD88,
        "GLD101_owner": GLD101_OWNER,
        "GLD101_canonical_verifier": GLD101_CANONICAL,
        "generic_C_open_Singular_source": SOURCE,
    }
    for name, path in expected_paths.items():
        source_pin = certificate["source_pins"][name]
        require(source_pin["path"] == path.relative_to(ROOT).as_posix(), f"{name} path")
        require(source_pin["lf_sha256"] == EXPECTED_LF_SHA256[path], f"{name} pin")
    require(certificate["support_digest"] == EXPECTED_SUPPORT_DIGEST, "certificate support")

    relations = load_literal_relations()
    equations, selector_records = reconstruct(relations)
    declarations = parse_source()
    chart = h4_a0_chart()
    references = {
        "Q6": q6_expression(),
        "H2": 2 * p**2 - 2 * p + 1,
        "Delta": delta_expression(chart),
    }
    for name, expression in references.items():
        expected = sp.Poly(expression, *VARIABLES, domain=QQ)
        require(declarations[name] == expected, f"source {name} regeneration")
    for name in SELECTOR_ORDER:
        expected = sp.Poly(equations[name].as_expr(), *VARIABLES, domain=QQ)
        require(declarations[f"H_{name}"] == expected, f"source H_{name} regeneration")

    equation_records = {name: polynomial_record(equations[name]) for name in SELECTOR_ORDER}
    require(certificate["selector_definitions"] == selector_records, "selector records")
    require(certificate["equations"] == equation_records, "equation records")

    cover = rank_cover(declarations, equations)
    tracked_cover = certificate["rank_cover"]
    for key in (
        "coefficient_matrix_shape",
        "coefficient_order",
        "maximal_minors",
        "maximal_minors_combined_sha256",
        "maximal_minor_gcd",
        "localization_exclusions",
        "special_fibres",
        "no_common_zero_on_D(H2*Delta)",
    ):
        require(tracked_cover[key] == cover[key], f"rank-cover field {key}")

    return {
        "status": "independent_no_repository_import_generic_C_open_audit_passed",
        "global_conjecture": "UNRESOLVED",
        "certificate_lf_sha256": EXPECTED_CERTIFICATE_LF_SHA256,
        "literal_GLD71_table_parsed": True,
        "GLD88_chart_transcribed_locally": True,
        "repository_modules_imported": 0,
        "selectors_reconstructed": list(SELECTOR_ORDER),
        "maximal_minors_recomputed_by_explicit_Leibniz": 15,
        "special_fibres_recomputed": ["-1", "0", "1"],
        "no_common_zero_on_D(H2*Delta)": True,
    }


def main() -> int:
    print(json.dumps(check(), indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as error:
        print(f"AUDIT FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
