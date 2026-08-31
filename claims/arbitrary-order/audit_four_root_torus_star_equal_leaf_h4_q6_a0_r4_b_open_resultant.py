#!/usr/bin/env python3
"""No-repository-import audit of the GLD101 R4 B-open resultant leaf.

The audit parses the literal GLD71 syndrome table without importing or
executing repository Python and transcribes the hash-pinned GLD88 a=0 chart
locally.  It substitutes C=B*t before taking the three determinants, checks
and cancels their common B factor, independently clears only Delta-supported
denominators, and reproduces the exact R4 equations.

It then rebuilds the two t-resultants, computes their B-resultant by recursive
Laplace expansion of the Sylvester matrix, and checks the 16-dimensional
multiplication determinant in a reversed basis with Bareiss elimination.
No primary checker or repository module is imported.  The scope remains only
the selected necessary minors T3,Y1,X3 on the stated R4 B-open chart.
"""

from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD101_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md"
)
CERTIFICATE = BASE / "certificates" / "GLD101_A0_R4_B_OPEN_RESULTANT_CERTIFICATE.json"

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "1961eed09059a7434002c610f89eb4e0ebc195398fbd026b0a4a7ddf778cc36e"
)
EXPECTED_LF_SHA256 = {
    GLD71: "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    GLD88: "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    GLD101_OWNER: "fe9e705f2fa9cde61c71daeb19abea241545a6c45611c15e6dd03b62ea6d3f45",
}
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
EXPECTED_EQUATION_HASHES = {
    "Q6": "4a8933c3fa3f3195d2cc65835e88dee9afa77b9348d2115cadb7a9bea6269d9a",
    "T3": "26e97ac75a6ab5d9b99e75b1b1821a2a57a08db29f77a2f63f6cc6c62f93549a",
    "Y1": "fb7921836c64fc06cbce60126ffd1c95b339cccdda0ccde9ad3e3d4dbbc4ec73",
    "X3": "442b967240ac7034927719f5eaf1fecde86647cbc6c599238018ab72b337c5c3",
}
SELECTORS = {
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTOR_ORDER = tuple(SELECTORS)
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
EXPECTED_RAW_OFFSETS = {
    "T3": ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1)),
    "Y1": ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)),
    "X3": ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)),
}

p, q, B, t = sp.symbols("p q B t")
Kpq = QQ.frac_field(p, q)
VARIABLES = (p, q, B, t)
R4 = 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5
H2 = 2 * p**2 - 2 * p + 1


class AuditError(RuntimeError):
    """Fail-closed independent-audit mismatch."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def lf_sha256(path: Path) -> str:
    return sha256_bytes(lf_bytes(path))


def validate_hashes() -> None:
    for path, expected in EXPECTED_LF_SHA256.items():
        require(path.is_file(), f"missing pinned source {path}")
        require(lf_sha256(path) == expected, f"LF hash mismatch for {path}")
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
    require(len(matches) == 1, "one literal SPARSE_RELATIONS assignment")
    relations = matches[0]
    require(isinstance(relations, tuple) and len(relations) == 37, "relation shape")
    payload = [
        [
            index,
            [[list(indices), coefficient] for indices, coefficient in relations[index]],
        ]
        for index in SUPPORT_ROWS
    ]
    digest = sha256_bytes(json.dumps(payload, separators=(",", ":")).encode("ascii"))
    require(digest == EXPECTED_SUPPORT_DIGEST, f"support digest mismatch: {digest}")
    return relations


class BTPolynomial:
    """Sparse B,t polynomial over QQ(p,q), after substituting C=B*t."""

    def __init__(self, terms: dict[tuple[int, int], Any] | None = None) -> None:
        self.terms = {
            tuple(exponents): coefficient
            for exponents, coefficient in (terms or {}).items()
            if coefficient != Kpq.zero
        }

    @classmethod
    def const(cls, value: object) -> "BTPolynomial":
        converted = value if type(value) is type(Kpq.one) else Kpq.convert(value)
        return cls({(0, 0): converted}) if converted != Kpq.zero else cls()

    @classmethod
    def var(cls, exponents: tuple[int, int]) -> "BTPolynomial":
        return cls({tuple(exponents): Kpq.one})

    def __add__(self, other: "BTPolynomial") -> "BTPolynomial":
        result = dict(self.terms)
        for exponents, coefficient in other.terms.items():
            value = result.get(exponents, Kpq.zero) + coefficient
            if value == Kpq.zero:
                result.pop(exponents, None)
            else:
                result[exponents] = value
        return BTPolynomial(result)

    def __neg__(self) -> "BTPolynomial":
        return BTPolynomial(
            {exponents: -coefficient for exponents, coefficient in self.terms.items()}
        )

    def __sub__(self, other: "BTPolynomial") -> "BTPolynomial":
        return self + (-other)

    def __mul__(self, other: "BTPolynomial") -> "BTPolynomial":
        result: dict[tuple[int, int], Any] = {}
        for (left_b, left_t), left in self.terms.items():
            for (right_b, right_t), right in other.terms.items():
                exponents = (left_b + right_b, left_t + right_t)
                value = result.get(exponents, Kpq.zero) + left * right
                if value == Kpq.zero:
                    result.pop(exponents, None)
                else:
                    result[exponents] = value
        return BTPolynomial(result)


def determinant_bt(matrix: list[list[BTPolynomial]]) -> BTPolynomial:
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix), "square determinant")
    states = {0: BTPolynomial.const(1)}
    for row in matrix:
        next_states: dict[int, BTPolynomial] = {}
        for mask, partial in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                term = partial * entry
                unused_before = sum(
                    1 for index in range(column) if not (mask & (1 << index))
                )
                if unused_before & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    term
                    if new_mask not in next_states
                    else next_states[new_mask] + term
                )
        states = next_states
    return states.get((1 << size) - 1, BTPolynomial.const(0))


def build_rows(relations: tuple, chart: dict[str, sp.Expr]) -> dict[int, list[BTPolynomial]]:
    leaves = (
        (BTPolynomial.const(1), BTPolynomial.const(1), BTPolynomial.const(1)),
        (
            BTPolynomial.const(p),
            BTPolynomial.const(q),
            BTPolynomial.const(chart["s"]),
        ),
        (
            BTPolynomial.const(0),
            BTPolynomial.const(1 + chart["b"]) + BTPolynomial.var((1, 0)),
            BTPolynomial.const(1 + chart["c"]) + BTPolynomial.var((1, 1)),
        ),
    )
    rows: dict[int, list[BTPolynomial]] = {}
    for row_index in SUPPORT_ROWS:
        entries: list[BTPolynomial] = []
        for root in range(3):
            for component in range(3):
                value = BTPolynomial.const(0)
                for indices, coefficient in relations[row_index]:
                    if indices[0] != root:
                        continue
                    value = value + BTPolynomial.const(coefficient) * (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                entries.append(value)
        rows[row_index] = entries
    return rows


def primitive_polynomial(expression: sp.Expr) -> sp.Poly:
    polynomial = sp.Poly(sp.expand(expression), *VARIABLES, domain=QQ)
    require(not polynomial.is_zero, "zero primitive polynomial")
    _content, primitive = polynomial.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def reduce_r4(expression: sp.Expr) -> sp.Poly:
    domain = QQ.poly_ring(q, B, t)
    polynomial = sp.Poly(sp.expand(expression), p, domain=domain)
    remainder = polynomial.rem(sp.Poly(R4, p, domain=domain))
    return primitive_polynomial(remainder.as_expr())


def rational_term_table(polynomial: sp.Poly) -> list[list[Any]]:
    return [
        [list(monomial), [int(coefficient.p), int(coefficient.q)]]
        for monomial, coefficient in polynomial.terms()
    ]


def polynomial_record(polynomial: sp.Poly) -> dict[str, Any]:
    table = rational_term_table(polynomial)
    return {
        "sha256": sha256_bytes(
            json.dumps(table, separators=(",", ":")).encode("ascii")
        ),
        "term_count": len(table),
        "total_degree": int(polynomial.total_degree()),
        "degrees": {
            "p": int(polynomial.degree(p)),
            "q": int(polynomial.degree(q)),
            "B": int(polynomial.degree(B)),
            "t": int(polynomial.degree(t)),
        },
    }


def clear_denominators(expression: sp.Expr, delta: sp.Expr):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    denominator_poly = sp.Poly(denominator, *VARIABLES, domain=QQ)
    delta_poly = sp.Poly(delta, *VARIABLES, domain=QQ)
    _constant, factors = sp.factor_list(denominator_poly.as_expr())
    records = []
    for factor, exponent in factors:
        require(factor.free_symbols <= {p, q}, f"offset denominator factor {factor}")
        factor_poly = sp.Poly(factor, *VARIABLES, domain=QQ)
        require(
            sp.gcd(delta_poly, factor_poly).monic() == factor_poly.monic(),
            f"denominator factor outside Delta: {factor}",
        )
        records.append({"factor": sp.sstr(factor), "exponent": int(exponent)})
    records.sort(key=lambda item: (item["factor"], item["exponent"]))
    return primitive_polynomial(numerator), records


def reconstruct_equations(relations: tuple):
    chart = h4_a0_chart()
    delta = delta_expression(chart)
    rows = build_rows(relations, chart)
    equations = {}
    metadata = {}
    expected_divided_support = {
        "T3": {(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)},
        "Y1": {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)},
        "X3": {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)},
    }
    for name, (row_indices, columns) in SELECTORS.items():
        determinant = determinant_bt(
            [[rows[row][column] for column in columns] for row in row_indices]
        )
        require(bool(determinant.terms), f"{name} determinant vanished")
        require(all(b_degree >= 1 for b_degree, _t_degree in determinant.terms), f"{name} B")
        divided = {
            (b_degree - 1, t_degree): coefficient
            for (b_degree, t_degree), coefficient in determinant.terms.items()
        }
        require(set(divided) == expected_divided_support[name], f"{name} B,t support")
        ratio = sp.cancel(
            sum(
                sp.sympify(coefficient.as_expr()) * B**b_degree * t**t_degree
                for (b_degree, t_degree), coefficient in divided.items()
            )
        )
        cleared, factors = clear_denominators(ratio, delta)
        reduced = reduce_r4(cleared.as_expr())
        record = polynomial_record(reduced)
        require(record["sha256"] == EXPECTED_EQUATION_HASHES[name], f"{name} hash")
        equations[name] = reduced
        metadata[name] = {
            "rows": list(row_indices),
            "columns": list(columns),
            "raw_offset_exponents": [list(value) for value in EXPECTED_RAW_OFFSETS[name]],
            "common_B_factor_after_C_equals_Bt": True,
            "denominator_factors": factors,
            "equation": record,
        }
    q6 = reduce_r4(q6_expression())
    require(polynomial_record(q6)["sha256"] == EXPECTED_EQUATION_HASHES["Q6"], "Q6")
    return equations, metadata, q6


class PField:
    zero = (QQ.zero, QQ.zero, QQ.zero, QQ.zero)
    one = (QQ.one, QQ.zero, QQ.zero, QQ.zero)
    reduction = (QQ(-1), QQ(16, 5), QQ(-6), QQ(16, 5))

    @classmethod
    def plus(cls, left, right):
        return tuple(left[index] + right[index] for index in range(4))

    @classmethod
    def minus(cls, value):
        return tuple(-coefficient for coefficient in value)

    @classmethod
    def times(cls, left, right):
        product = [QQ.zero] * 7
        for left_degree, left_coefficient in enumerate(left):
            for right_degree, right_coefficient in enumerate(right):
                product[left_degree + right_degree] += left_coefficient * right_coefficient
        for degree in range(6, 3, -1):
            high = product[degree]
            for index, coefficient in enumerate(cls.reduction):
                product[degree - 4 + index] += high * coefficient
        return tuple(product[:4])

    @classmethod
    def convert(cls, expression: sp.Expr):
        remainder = sp.Poly(expression, p, domain=QQ).rem(sp.Poly(R4, p, domain=QQ))
        return tuple(QQ.convert(remainder.nth(index)) for index in range(4))

    @classmethod
    def expression(cls, value):
        return sum(value[index] * p**index for index in range(4))

    @classmethod
    def reciprocal(cls, value):
        try:
            inverse = sp.invert(
                sp.Poly(cls.expression(value), p, domain=QQ),
                sp.Poly(R4, p, domain=QQ),
            )
        except sp.NotInvertible as error:
            raise AuditError("Q6 leading coefficient is not a unit") from error
        return cls.convert(inverse.as_expr())


class PQAlgebra:
    def __init__(self, q6: sp.Poly) -> None:
        self.zero = (PField.zero,) * 4
        self.one = (PField.one, PField.zero, PField.zero, PField.zero)
        polynomial = sp.Poly(q6.as_expr(), q, domain=QQ.poly_ring(p))
        require(polynomial.degree() == 4, "Q6 degree")
        coefficients = [
            PField.convert(polynomial.nth(index).as_expr()) for index in range(5)
        ]
        self.leading = coefficients[4]
        self.leading_inverse = PField.reciprocal(self.leading)
        self.reduction = tuple(
            PField.minus(PField.times(coefficients[index], self.leading_inverse))
            for index in range(4)
        )

    @staticmethod
    def plus(left, right):
        return tuple(PField.plus(left[index], right[index]) for index in range(4))

    @staticmethod
    def minus(value):
        return tuple(PField.minus(coefficient) for coefficient in value)

    def times(self, left, right):
        product = [PField.zero] * 7
        for left_degree, left_coefficient in enumerate(left):
            for right_degree, right_coefficient in enumerate(right):
                product[left_degree + right_degree] = PField.plus(
                    product[left_degree + right_degree],
                    PField.times(left_coefficient, right_coefficient),
                )
        for degree in range(6, 3, -1):
            high = product[degree]
            for index, coefficient in enumerate(self.reduction):
                product[degree - 4 + index] = PField.plus(
                    product[degree - 4 + index], PField.times(high, coefficient)
                )
        return tuple(product[:4])

    def convert(self, expression: sp.Expr):
        polynomial = sp.Poly(expression, q, domain=QQ.poly_ring(p))
        result = self.zero
        q_element = (PField.zero, PField.one, PField.zero, PField.zero)
        power = self.one
        for degree in range(polynomial.degree() + 1):
            coefficient = PField.convert(polynomial.nth(degree).as_expr())
            result = self.plus(
                result, tuple(PField.times(value, coefficient) for value in power)
            )
            power = self.times(power, q_element)
        return result

    @staticmethod
    def flatten(value):
        return tuple(coefficient for q_part in value for coefficient in q_part)

    def standard_basis(self):
        result = []
        for q_degree in range(4):
            for p_degree in range(4):
                q_parts = [PField.zero] * 4
                p_parts = [QQ.zero] * 4
                p_parts[p_degree] = QQ.one
                q_parts[q_degree] = tuple(p_parts)
                result.append(tuple(q_parts))
        return result


def rational_pair(value: Any) -> list[int]:
    return [int(value.p), int(value.q)]


def element_table(element, algebra: PQAlgebra):
    return [rational_pair(value) for value in algebra.flatten(element)]


def element_record(element, algebra: PQAlgebra, include_coordinates: bool = False):
    table = element_table(element, algebra)
    record = {
        "sha256": sha256_bytes(
            json.dumps(table, separators=(",", ":")).encode("ascii")
        ),
        "nonzero_coordinates": sum(pair != [0, 1] for pair in table),
    }
    if include_coordinates:
        record["coordinates_q_major_p_minor"] = table
    return record


def equation_bt(polynomial: sp.Poly, algebra: PQAlgebra):
    result = {}
    for monomial, coefficient in polynomial.terms():
        p_degree, q_degree, b_degree, t_degree = monomial
        item = algebra.convert(QQ.convert(coefficient) * p**p_degree * q**q_degree)
        key = (b_degree, t_degree)
        result[key] = algebra.plus(result.get(key, algebra.zero), item)
    return {key: value for key, value in result.items() if value != algebra.zero}


def bt_record(polynomial, algebra: PQAlgebra):
    records = [
        {
            "B_degree": key[0],
            "t_degree": key[1],
            **element_record(value, algebra),
        }
        for key, value in sorted(polynomial.items())
    ]
    return {
        "support": [[item["B_degree"], item["t_degree"]] for item in records],
        "coefficients": records,
        "combined_sha256": sha256_bytes(
            json.dumps(records, separators=(",", ":"), sort_keys=True).encode("ascii")
        ),
    }


def split_t(polynomial):
    require(all(t_degree in (0, 1) for _b_degree, t_degree in polynomial), "t degree")
    linear = {}
    constant = {}
    for (b_degree, t_degree), coefficient in polynomial.items():
        (linear if t_degree else constant)[b_degree] = coefficient
    return linear, constant


def poly_plus(left, right, algebra: PQAlgebra):
    result = dict(left)
    for degree, coefficient in right.items():
        result[degree] = algebra.plus(result.get(degree, algebra.zero), coefficient)
        if result[degree] == algebra.zero:
            result.pop(degree)
    return result


def poly_minus(polynomial, algebra: PQAlgebra):
    return {degree: algebra.minus(value) for degree, value in polynomial.items()}


def poly_times(left, right, algebra: PQAlgebra):
    result = {}
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            degree = left_degree + right_degree
            result[degree] = algebra.plus(
                result.get(degree, algebra.zero),
                algebra.times(left_coefficient, right_coefficient),
            )
    return {degree: value for degree, value in result.items() if value != algebra.zero}


def t_resultant(left, right, algebra: PQAlgebra):
    left_linear, left_constant = split_t(left)
    right_linear, right_constant = split_t(right)
    return poly_plus(
        poly_times(left_linear, right_constant, algebra),
        poly_minus(poly_times(right_linear, left_constant, algebra), algebra),
        algebra,
    )


def poly_record(polynomial, algebra: PQAlgebra):
    records = [
        {"B_degree": degree, **element_record(value, algebra)}
        for degree, value in sorted(polynomial.items())
    ]
    return {
        "degree": max(polynomial),
        "coefficients": records,
        "combined_sha256": sha256_bytes(
            json.dumps(records, separators=(",", ":"), sort_keys=True).encode("ascii")
        ),
    }


def sylvester_matrix(left, right, algebra: PQAlgebra):
    left_degree = max(left)
    right_degree = max(right)
    left_values = [left.get(degree, algebra.zero) for degree in range(left_degree, -1, -1)]
    right_values = [right.get(degree, algebra.zero) for degree in range(right_degree, -1, -1)]
    size = left_degree + right_degree
    matrix = [[algebra.zero for _ in range(size)] for _ in range(size)]
    for row in range(right_degree):
        for offset, coefficient in enumerate(left_values):
            matrix[row][row + offset] = coefficient
    for row in range(left_degree):
        for offset, coefficient in enumerate(right_values):
            matrix[right_degree + row][row + offset] = coefficient
    return matrix


def determinant_laplace(matrix, algebra: PQAlgebra):
    size = len(matrix)

    @lru_cache(maxsize=None)
    def recurse(row: int, columns: tuple[int, ...]):
        if row == size:
            return algebra.one
        total = algebra.zero
        for position, column in enumerate(columns):
            entry = matrix[row][column]
            if entry == algebra.zero:
                continue
            remaining = columns[:position] + columns[position + 1 :]
            term = algebra.times(entry, recurse(row + 1, remaining))
            if position & 1:
                term = algebra.minus(term)
            total = algebra.plus(total, term)
        return total

    return recurse(0, tuple(range(size)))


def multiplication_matrix(element, algebra: PQAlgebra):
    columns = [
        algebra.flatten(algebra.times(element, basis))
        for basis in algebra.standard_basis()
    ]
    return sp.Matrix(16, 16, lambda row, column: columns[column][row])


def check() -> dict[str, Any]:
    validate_hashes()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate["schema_version"] == 1, "schema")
    require(
        certificate["certificate_id"]
        == "GLD101-a0-R4-B-open-T3-Y1-X3-resultant-unit",
        "certificate id",
    )
    require(certificate["global_conjecture"] == "UNRESOLVED", "global status")
    scope = certificate["mathematical_scope"]
    require("R4=0 and Q6=0" in scope["branch"], "R4/Q6 scope")
    require("D(B*H2*Delta)" in scope["open"], "open scope")
    require(tuple(scope["selected_necessary_minors"]) == SELECTOR_ORDER, "selectors")
    nonclaims = " ".join(scope["nonclaims"])
    for phrase in ("no converse", "no claim on B=0", "no claim for another", "no live-frontier"):
        require(phrase in nonclaims, f"missing nonclaim {phrase}")

    source_paths = {"GLD71": GLD71, "GLD88": GLD88, "GLD101_owner": GLD101_OWNER}
    for name, path in source_paths.items():
        record = certificate["source_pins"][name]
        require(record["path"] == path.relative_to(ROOT).as_posix(), f"{name} path")
        require(record["lf_sha256"] == EXPECTED_LF_SHA256[path], f"{name} hash")
    require(certificate["support_digest"] == EXPECTED_SUPPORT_DIGEST, "support")

    relations = load_literal_relations()
    equations, selector_metadata, q6 = reconstruct_equations(relations)
    require(certificate["selectors"] == selector_metadata, "selector reconstruction")
    require(certificate["Q6"] == polynomial_record(q6), "Q6 record")
    require(sp.Poly(R4, p, domain=QQ).is_irreducible, "R4 irreducibility")
    require(sp.resultant(R4, H2, p) == 145, "H2 resultant")

    algebra = PQAlgebra(q6)
    specialized = {name: equation_bt(equations[name], algebra) for name in SELECTOR_ORDER}
    specialized_records = {name: bt_record(value, algebra) for name, value in specialized.items()}
    require(
        certificate["specialized_equations"] == specialized_records,
        "specialized equations",
    )
    expected_factor_checks = certificate["factor_checks"]
    require(expected_factor_checks["R4_irreducible_over_QQ"], "certificate R4")
    require(expected_factor_checks["resultant_R4_H2"] == "145", "certificate H2")
    require(
        expected_factor_checks["Q6_q_leading_coefficient"]
        == element_record((algebra.leading, PField.zero, PField.zero, PField.zero), algebra),
        "Q6 leading coefficient",
    )
    require(
        expected_factor_checks["Q6_q_leading_inverse"]
        == element_record(
            (algebra.leading_inverse, PField.zero, PField.zero, PField.zero), algebra
        ),
        "Q6 leading inverse",
    )

    t_resultants = {
        "T3_X3": t_resultant(specialized["T3"], specialized["X3"], algebra),
        "Y1_X3": t_resultant(specialized["Y1"], specialized["X3"], algebra),
    }
    proof = certificate["resultant_proof"]
    require(
        proof["t_resultants"]
        == {name: poly_record(value, algebra) for name, value in t_resultants.items()},
        "t-resultants",
    )
    sylvester = sylvester_matrix(t_resultants["T3_X3"], t_resultants["Y1_X3"], algebra)
    require(len(sylvester) == 8, "Sylvester size")
    b_resultant = determinant_laplace(sylvester, algebra)
    require(
        proof["B_resultant"]
        == element_record(b_resultant, algebra, include_coordinates=True),
        "B-resultant",
    )
    matrix = multiplication_matrix(b_resultant, algebra)
    matrix_hash = sha256_bytes(
        json.dumps(
            [[rational_pair(value) for value in row] for row in matrix.tolist()],
            separators=(",", ":"),
        ).encode("ascii")
    )
    require(matrix_hash == proof["multiplication_matrix_sha256"], "matrix hash")
    reverse = list(reversed(range(16)))
    reversed_basis_matrix = matrix.extract(reverse, reverse)
    determinant = sp.cancel(reversed_basis_matrix.det(method="bareiss"))
    require(determinant != 0, "multiplication determinant zero")
    require(str(determinant) == proof["multiplication_determinant"], "determinant value")
    require(
        sha256_bytes(str(determinant).encode("ascii"))
        == proof["multiplication_determinant_sha256"],
        "determinant hash",
    )
    require(proof["B_resultant_is_unit"], "unit conclusion")

    return {
        "status": "independent_no_repository_import_R4_B_open_resultant_audit_passed",
        "global_conjecture": "UNRESOLVED",
        "certificate_lf_sha256": EXPECTED_CERTIFICATE_LF_SHA256,
        "literal_GLD71_table_parsed": True,
        "GLD88_chart_transcribed_locally": True,
        "repository_modules_imported": 0,
        "selectors_reconstructed": list(SELECTOR_ORDER),
        "B_resultant_recomputed_by_recursive_Laplace": True,
        "multiplication_determinant_recomputed_in_reversed_basis": True,
        "multiplication_determinant_sha256": proof[
            "multiplication_determinant_sha256"
        ],
        "B_resultant_is_unit": True,
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
