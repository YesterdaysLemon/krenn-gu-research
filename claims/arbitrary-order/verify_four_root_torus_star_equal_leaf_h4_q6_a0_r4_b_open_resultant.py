#!/usr/bin/env python3
"""Verify the scoped GLD101 R4 B-open T3/Y1/X3 resultant leaf.

The checker reconstructs the three actual seven-by-seven syndrome minors
from hash-pinned GLD71 and GLD88 parents over QQ(p,q)[B,C].  On B != 0 it
substitutes C=B*t, cancels the common B factor, checks that every cleared
denominator is supported on Delta, and specializes to the irreducible R4
factor.

Each resulting equation is linear in t and quadratic in B.  A common zero
would force the T3-X3 and Y1-X3 pairwise t-resultants to share a B-root.  The
Sylvester B-resultant of those two quartics is a unit in the 16-dimensional
QQ-algebra QQ[p,q]/(R4,Q6), as certified by the nonzero determinant of its
multiplication map.  This is a selected-necessary-minor proof leaf only; it
does not prove a selector converse, P8, full E31, physical incidence, or the
global Krenn--Gu conjecture.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
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
EXPECTED_SOURCE_PINS = {
    "GLD71": (
        GLD71,
        "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    ),
    "GLD88": (
        GLD88,
        "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    ),
    "GLD101_owner": (
        GLD101_OWNER,
        "fe9e705f2fa9cde61c71daeb19abea241545a6c45611c15e6dd03b62ea6d3f45",
    ),
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

p, q, B, C, t = sp.symbols("p q B C t")
Kpq = QQ.frac_field(p, q)
VARIABLES = (p, q, B, t)
R4 = 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5
H2 = 2 * p**2 - 2 * p + 1
SELECTORS = {
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTOR_ORDER = tuple(SELECTORS)
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)


class VerificationError(RuntimeError):
    """Fail-closed source, reconstruction, or exact-proof mismatch."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def lf_sha256(path: Path) -> str:
    return sha256_bytes(lf_bytes(path))


def validate_source_pins() -> dict[str, dict[str, str]]:
    records = {}
    for name, (path, expected) in EXPECTED_SOURCE_PINS.items():
        require(path.is_file(), f"missing pinned source {name}: {path}")
        observed = lf_sha256(path)
        require(observed == expected, f"{name} LF hash mismatch: {observed}")
        records[name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "lf_sha256": observed,
        }
    return records


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise VerificationError(f"cannot import pinned source {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def delta_expression(chart: dict[str, sp.Expr]) -> sp.Expr:
    return sp.expand(
        (p - q)
        * (p + q - 1)
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * chart["rank_denominator"]
    )


class OffsetPolynomial:
    """Sparse B,C polynomial with coefficients in QQ(p,q)."""

    def __init__(self, terms: dict[tuple[int, int], Any] | None = None) -> None:
        self.terms = {
            tuple(exponents): coefficient
            for exponents, coefficient in (terms or {}).items()
            if coefficient != Kpq.zero
        }

    @classmethod
    def const(cls, value: object) -> "OffsetPolynomial":
        converted = value if type(value) is type(Kpq.one) else Kpq.convert(value)
        return cls({(0, 0): converted}) if converted != Kpq.zero else cls()

    @classmethod
    def var(cls, exponents: tuple[int, int]) -> "OffsetPolynomial":
        return cls({tuple(exponents): Kpq.one})

    def __add__(self, other: "OffsetPolynomial") -> "OffsetPolynomial":
        result = dict(self.terms)
        for exponents, coefficient in other.terms.items():
            updated = result.get(exponents, Kpq.zero) + coefficient
            if updated == Kpq.zero:
                result.pop(exponents, None)
            else:
                result[exponents] = updated
        return OffsetPolynomial(result)

    def __neg__(self) -> "OffsetPolynomial":
        return OffsetPolynomial(
            {exponents: -coefficient for exponents, coefficient in self.terms.items()}
        )

    def __sub__(self, other: "OffsetPolynomial") -> "OffsetPolynomial":
        return self + (-other)

    def __mul__(self, other: "OffsetPolynomial") -> "OffsetPolynomial":
        result: dict[tuple[int, int], Any] = {}
        for (left_b, left_c), left in self.terms.items():
            for (right_b, right_c), right in other.terms.items():
                exponents = (left_b + right_b, left_c + right_c)
                updated = result.get(exponents, Kpq.zero) + left * right
                if updated == Kpq.zero:
                    result.pop(exponents, None)
                else:
                    result[exponents] = updated
        return OffsetPolynomial(result)


def determinant_offset(matrix: list[list[OffsetPolynomial]], label: str) -> OffsetPolynomial:
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix), "square determinant")
    states = {0: OffsetPolynomial.const(1)}
    for row_index, row in enumerate(matrix):
        next_states: dict[int, OffsetPolynomial] = {}
        for mask, partial in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
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
        print(
            f"[R4 primary] {label} row={row_index + 1}/{size} states={len(states)}",
            file=sys.stderr,
            flush=True,
        )
    return states.get((1 << size) - 1, OffsetPolynomial.const(0))


def support_digest(relations: tuple) -> str:
    payload = [
        [
            index,
            [[list(indices), coefficient] for indices, coefficient in relations[index]],
        ]
        for index in SUPPORT_ROWS
    ]
    return sha256_bytes(json.dumps(payload, separators=(",", ":")).encode("ascii"))


def build_rows(relations: tuple, chart: dict[str, sp.Expr]) -> dict[int, list[OffsetPolynomial]]:
    leaves = (
        (
            OffsetPolynomial.const(1),
            OffsetPolynomial.const(1),
            OffsetPolynomial.const(1),
        ),
        (
            OffsetPolynomial.const(p),
            OffsetPolynomial.const(q),
            OffsetPolynomial.const(chart["s"]),
        ),
        (
            OffsetPolynomial.const(0),
            OffsetPolynomial.const(1 + chart["b"]) + OffsetPolynomial.var((1, 0)),
            OffsetPolynomial.const(1 + chart["c"]) + OffsetPolynomial.var((0, 1)),
        ),
    )
    rows: dict[int, list[OffsetPolynomial]] = {}
    for row_index in SUPPORT_ROWS:
        entries: list[OffsetPolynomial] = []
        for root in range(3):
            for component in range(3):
                value = OffsetPolynomial.const(0)
                for indices, coefficient in relations[row_index]:
                    if indices[0] != root:
                        continue
                    value = value + OffsetPolynomial.const(coefficient) * (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                entries.append(value)
        rows[row_index] = entries
    return rows


def primitive_polynomial(expression: sp.Expr) -> sp.Poly:
    polynomial = sp.Poly(sp.expand(expression), *VARIABLES, domain=QQ)
    require(not polynomial.is_zero, "unexpected zero polynomial")
    _content, primitive = polynomial.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def reduce_r4(expression: sp.Expr) -> sp.Poly:
    coefficient_domain = QQ.poly_ring(q, B, t)
    polynomial = sp.Poly(sp.expand(expression), p, domain=coefficient_domain)
    modulus = sp.Poly(R4, p, domain=coefficient_domain)
    remainder = polynomial.rem(modulus)
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


def clear_declared_denominators(
    expression: sp.Expr, delta: sp.Expr
) -> tuple[sp.Poly, list[dict[str, Any]]]:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    denominator_poly = sp.Poly(denominator, *VARIABLES, domain=QQ)
    delta_poly = sp.Poly(delta, *VARIABLES, domain=QQ)
    _constant, factors = sp.factor_list(denominator_poly.as_expr())
    records = []
    for factor, exponent in factors:
        require(factor.free_symbols <= {p, q}, f"offset in denominator {factor}")
        factor_poly = sp.Poly(factor, *VARIABLES, domain=QQ)
        common = sp.gcd(delta_poly, factor_poly).monic()
        require(common == factor_poly.monic(), f"denominator outside Delta: {factor}")
        records.append({"factor": sp.sstr(factor), "exponent": int(exponent)})
    records.sort(key=lambda item: (item["factor"], item["exponent"]))
    return primitive_polynomial(numerator), records


def reconstruct_equations() -> tuple[dict[str, sp.Poly], dict[str, Any], sp.Poly]:
    gld71 = load_module(GLD71, "gld71_for_r4_resultant_primary")
    gld88 = load_module(GLD88, "gld88_for_r4_resultant_primary")
    relations = gld71.SPARSE_RELATIONS
    observed_support = support_digest(relations)
    require(observed_support == EXPECTED_SUPPORT_DIGEST, "support digest mismatch")
    chart = gld88.h4_family(p, q, sp.Integer(0))
    delta = delta_expression(chart)
    rows = build_rows(relations, chart)

    equations: dict[str, sp.Poly] = {}
    metadata: dict[str, Any] = {}
    for name, (row_indices, columns) in SELECTORS.items():
        matrix = [[rows[row][column] for column in columns] for row in row_indices]
        determinant = determinant_offset(matrix, name)
        require(bool(determinant.terms), f"{name} determinant vanished")
        require(
            all(c_exponent in (0, 1) for _b_exponent, c_exponent in determinant.terms),
            f"{name} unexpected C degree",
        )
        require(
            all(b_exponent + c_exponent >= 1 for b_exponent, c_exponent in determinant.terms),
            f"{name} lacks common B factor after C=B*t",
        )
        ratio = sp.cancel(
            sum(
                sp.sympify(coefficient.as_expr())
                * B ** (b_exponent + c_exponent - 1)
                * t**c_exponent
                for (b_exponent, c_exponent), coefficient in determinant.terms.items()
            )
        )
        cleared, denominator_factors = clear_declared_denominators(ratio, delta)
        reduced = reduce_r4(cleared.as_expr())
        record = polynomial_record(reduced)
        require(
            record["sha256"] == EXPECTED_EQUATION_HASHES[name],
            f"{name} accepted equation hash mismatch: {record['sha256']}",
        )
        require(reduced.degree(t) == 1 and reduced.degree(B) <= 2, f"{name} shape")
        equations[name] = reduced
        metadata[name] = {
            "rows": list(row_indices),
            "columns": list(columns),
            "raw_offset_exponents": [list(item) for item in sorted(determinant.terms)],
            "common_B_factor_after_C_equals_Bt": True,
            "denominator_factors": denominator_factors,
            "equation": record,
        }

    q6 = reduce_r4(q6_expression())
    q6_record = polynomial_record(q6)
    require(q6_record["sha256"] == EXPECTED_EQUATION_HASHES["Q6"], "Q6 hash")
    return equations, metadata, q6


class Fp:
    """The exact number field QQ[p]/(R4), represented in basis 1,p,p^2,p^3."""

    zero = (QQ.zero, QQ.zero, QQ.zero, QQ.zero)
    one = (QQ.one, QQ.zero, QQ.zero, QQ.zero)
    relation = (QQ(-1), QQ(16, 5), QQ(-6), QQ(16, 5))

    @classmethod
    def add(cls, left, right):
        return tuple(left[index] + right[index] for index in range(4))

    @classmethod
    def negate(cls, value):
        return tuple(-coefficient for coefficient in value)

    @classmethod
    def multiply(cls, left, right):
        raw = [QQ.zero] * 7
        for left_index, left_coefficient in enumerate(left):
            if left_coefficient == QQ.zero:
                continue
            for right_index, right_coefficient in enumerate(right):
                if right_coefficient != QQ.zero:
                    raw[left_index + right_index] += left_coefficient * right_coefficient
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high == QQ.zero:
                continue
            for index, coefficient in enumerate(cls.relation):
                raw[degree - 4 + index] += high * coefficient
        return tuple(raw[:4])

    @classmethod
    def from_expr(cls, expression: sp.Expr):
        polynomial = sp.Poly(sp.expand(expression), p, domain=QQ)
        remainder = polynomial.rem(sp.Poly(R4, p, domain=QQ))
        return tuple(QQ.convert(remainder.nth(index)) for index in range(4))

    @classmethod
    def as_expr(cls, value) -> sp.Expr:
        return sp.expand(sum(value[index] * p**index for index in range(4)))

    @classmethod
    def inverse(cls, value):
        polynomial = sp.Poly(cls.as_expr(value), p, domain=QQ)
        try:
            inverse = sp.invert(polynomial, sp.Poly(R4, p, domain=QQ))
        except sp.NotInvertible as error:
            raise VerificationError("nonunit leading Q6 coefficient on R4") from error
        return cls.from_expr(inverse.as_expr())


class FibreAlgebra:
    """The 16-dimensional QQ-algebra QQ[p,q]/(R4,Q6)."""

    def __init__(self, q6: sp.Poly) -> None:
        self.zero = (Fp.zero, Fp.zero, Fp.zero, Fp.zero)
        self.one = (Fp.one, Fp.zero, Fp.zero, Fp.zero)
        q_polynomial = sp.Poly(q6.as_expr(), q, domain=QQ.poly_ring(p))
        require(q_polynomial.degree() == 4, "Q6 q-degree")
        coefficients = [
            Fp.from_expr(q_polynomial.nth(index).as_expr()) for index in range(5)
        ]
        leading_inverse = Fp.inverse(coefficients[4])
        self.q_relation = tuple(
            Fp.negate(Fp.multiply(coefficients[index], leading_inverse))
            for index in range(4)
        )
        self.q_leading_coefficient = coefficients[4]
        self.q_leading_inverse = leading_inverse

    @staticmethod
    def add(left, right):
        return tuple(Fp.add(left[index], right[index]) for index in range(4))

    @staticmethod
    def negate(value):
        return tuple(Fp.negate(coefficient) for coefficient in value)

    def multiply(self, left, right):
        raw = [Fp.zero] * 7
        for left_index, left_coefficient in enumerate(left):
            if left_coefficient == Fp.zero:
                continue
            for right_index, right_coefficient in enumerate(right):
                if right_coefficient != Fp.zero:
                    raw[left_index + right_index] = Fp.add(
                        raw[left_index + right_index],
                        Fp.multiply(left_coefficient, right_coefficient),
                    )
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high == Fp.zero:
                continue
            for index, coefficient in enumerate(self.q_relation):
                raw[degree - 4 + index] = Fp.add(
                    raw[degree - 4 + index], Fp.multiply(high, coefficient)
                )
        return tuple(raw[:4])

    def from_expr(self, expression: sp.Expr):
        polynomial = sp.Poly(sp.expand(expression), q, domain=QQ.poly_ring(p))
        result = self.zero
        q_power = self.one
        q_element = (Fp.zero, Fp.one, Fp.zero, Fp.zero)
        for degree in range(polynomial.degree() + 1):
            coefficient = Fp.from_expr(polynomial.nth(degree).as_expr())
            term = tuple(Fp.multiply(part, coefficient) for part in q_power)
            result = self.add(result, term)
            q_power = self.multiply(q_power, q_element)
        return result

    @staticmethod
    def flatten(value) -> tuple[Any, ...]:
        return tuple(coefficient for q_part in value for coefficient in q_part)

    def basis(self) -> list[Any]:
        result = []
        for q_degree in range(4):
            for p_degree in range(4):
                q_parts = [Fp.zero] * 4
                p_parts = [QQ.zero] * 4
                p_parts[p_degree] = QQ.one
                q_parts[q_degree] = tuple(p_parts)
                result.append(tuple(q_parts))
        return result


def rational_pair(value: Any) -> list[int]:
    return [int(value.p), int(value.q)]


def element_table(element, algebra: FibreAlgebra) -> list[list[int]]:
    return [rational_pair(value) for value in algebra.flatten(element)]


def element_record(element, algebra: FibreAlgebra, *, include_coordinates: bool = False) -> dict[str, Any]:
    table = element_table(element, algebra)
    record: dict[str, Any] = {
        "sha256": sha256_bytes(
            json.dumps(table, separators=(",", ":")).encode("ascii")
        ),
        "nonzero_coordinates": sum(pair != [0, 1] for pair in table),
    }
    if include_coordinates:
        record["coordinates_q_major_p_minor"] = table
    return record


def equation_bt(polynomial: sp.Poly, algebra: FibreAlgebra) -> dict[tuple[int, int], Any]:
    result: dict[tuple[int, int], Any] = {}
    for monomial, coefficient in polynomial.terms():
        p_degree, q_degree, b_degree, t_degree = monomial
        element = algebra.from_expr(
            QQ.convert(coefficient) * p**p_degree * q**q_degree
        )
        key = (b_degree, t_degree)
        result[key] = algebra.add(result.get(key, algebra.zero), element)
    return {key: value for key, value in result.items() if value != algebra.zero}


def bt_record(polynomial: dict[tuple[int, int], Any], algebra: FibreAlgebra) -> dict[str, Any]:
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


def split_t(polynomial: dict[tuple[int, int], Any]) -> tuple[dict[int, Any], dict[int, Any]]:
    require(all(t_degree in (0, 1) for _b_degree, t_degree in polynomial), "t degree")
    linear: dict[int, Any] = {}
    constant: dict[int, Any] = {}
    for (b_degree, t_degree), coefficient in polynomial.items():
        (linear if t_degree else constant)[b_degree] = coefficient
    return linear, constant


def poly_b_add(left: dict[int, Any], right: dict[int, Any], algebra: FibreAlgebra):
    result = dict(left)
    for degree, coefficient in right.items():
        result[degree] = algebra.add(result.get(degree, algebra.zero), coefficient)
        if result[degree] == algebra.zero:
            result.pop(degree)
    return result


def poly_b_negate(polynomial: dict[int, Any], algebra: FibreAlgebra):
    return {degree: algebra.negate(value) for degree, value in polynomial.items()}


def poly_b_multiply(left: dict[int, Any], right: dict[int, Any], algebra: FibreAlgebra):
    result: dict[int, Any] = {}
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            degree = left_degree + right_degree
            result[degree] = algebra.add(
                result.get(degree, algebra.zero),
                algebra.multiply(left_coefficient, right_coefficient),
            )
    return {degree: value for degree, value in result.items() if value != algebra.zero}


def t_resultant(left, right, algebra: FibreAlgebra):
    left_linear, left_constant = split_t(left)
    right_linear, right_constant = split_t(right)
    return poly_b_add(
        poly_b_multiply(left_linear, right_constant, algebra),
        poly_b_negate(
            poly_b_multiply(right_linear, left_constant, algebra), algebra
        ),
        algebra,
    )


def poly_b_record(polynomial: dict[int, Any], algebra: FibreAlgebra) -> dict[str, Any]:
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


def sylvester_resultant(
    left: dict[int, Any], right: dict[int, Any], algebra: FibreAlgebra
):
    left_degree = max(left)
    right_degree = max(right)
    left_descending = [
        left.get(degree, algebra.zero) for degree in range(left_degree, -1, -1)
    ]
    right_descending = [
        right.get(degree, algebra.zero) for degree in range(right_degree, -1, -1)
    ]
    size = left_degree + right_degree
    matrix = [[algebra.zero for _ in range(size)] for _ in range(size)]
    for row in range(right_degree):
        for index, coefficient in enumerate(left_descending):
            matrix[row][row + index] = coefficient
    for row in range(left_degree):
        for index, coefficient in enumerate(right_descending):
            matrix[right_degree + row][row + index] = coefficient

    states = {0: algebra.one}
    for row in matrix:
        next_states = {}
        for mask, partial in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or entry == algebra.zero:
                    continue
                term = algebra.multiply(partial, entry)
                unused_before = sum(
                    1 for index in range(column) if not (mask & (1 << index))
                )
                if unused_before & 1:
                    term = algebra.negate(term)
                new_mask = mask | (1 << column)
                next_states[new_mask] = algebra.add(
                    next_states.get(new_mask, algebra.zero), term
                )
        states = next_states
    return states.get((1 << size) - 1, algebra.zero), size


def multiplication_matrix(element, algebra: FibreAlgebra) -> sp.Matrix:
    columns = [
        algebra.flatten(algebra.multiply(element, basis_element))
        for basis_element in algebra.basis()
    ]
    return sp.Matrix(16, 16, lambda row, column: columns[column][row])


def build_certificate() -> dict[str, Any]:
    source_pins = validate_source_pins()
    equations, selector_metadata, q6 = reconstruct_equations()
    require(sp.Poly(R4, p, domain=QQ).is_irreducible, "R4 is not irreducible")
    h2_resultant = sp.resultant(R4, H2, p)
    require(h2_resultant == 145, f"unexpected R4/H2 resultant {h2_resultant}")

    algebra = FibreAlgebra(q6)
    specialized = {
        name: equation_bt(equations[name], algebra) for name in SELECTOR_ORDER
    }
    t_resultants = {
        "T3_X3": t_resultant(specialized["T3"], specialized["X3"], algebra),
        "Y1_X3": t_resultant(specialized["Y1"], specialized["X3"], algebra),
    }
    require(all(max(value) == 4 for value in t_resultants.values()), "quartic t-resultants")
    b_resultant, sylvester_size = sylvester_resultant(
        t_resultants["T3_X3"], t_resultants["Y1_X3"], algebra
    )
    require(b_resultant != algebra.zero, "zero B-resultant")
    matrix = multiplication_matrix(b_resultant, algebra)
    determinant = sp.cancel(matrix.det(method="domain-ge"))
    require(determinant != 0, "B-resultant is not a unit in the fibre algebra")
    numerator, denominator = determinant.as_numer_denom()

    return {
        "schema_version": 1,
        "certificate_id": "GLD101-a0-R4-B-open-T3-Y1-X3-resultant-unit",
        "status": "scoped_exact_selected_necessary_minor_leaf_certificate",
        "global_conjecture": "UNRESOLVED",
        "mathematical_scope": {
            "branch": "normalized a=0 equal-leaf H4 chart with R4=0 and Q6=0",
            "R4": str(R4),
            "open": "D(B*H2*Delta), including the GLD88 chart gates",
            "substitution": "C=B*t followed by cancellation of the common B factor",
            "selected_necessary_minors": list(SELECTOR_ORDER),
            "bridge": (
                "rank(M)<=6 makes T3,Y1,X3 vanish; on B!=0 the substitution "
                "C=B*t and common-B cancellation gives the three reconstructed "
                "equations, whose cleared denominators are units on D(Delta)"
            ),
            "conclusion": (
                "the three selected-minor equations have no common (q,B,t) point "
                "on R4=Q6=0 and D(B*H2*Delta)"
            ),
            "base_change": (
                "the exact QQ multiplication determinant is nonzero, so the B-resultant "
                "is a unit simultaneously on every characteristic-zero R4,Q6 fibre"
            ),
            "nonclaims": [
                "no converse from T3,Y1,X3 to syndrome rank",
                "no claim on B=0, the generic C-open branch, endpoints, or physical incidence",
                "no claim for another residual factor, arbitrary a, P6, P8, or full E31",
                "no live-frontier or global Krenn-Gu promotion",
            ],
        },
        "source_pins": source_pins,
        "support_digest": EXPECTED_SUPPORT_DIGEST,
        "factor_checks": {
            "R4_irreducible_over_QQ": True,
            "resultant_R4_H2": str(h2_resultant),
            "H2_unit_on_R4": True,
            "fibre_algebra_basis": [
                "1",
                "p",
                "p^2",
                "p^3",
                "q",
                "p*q",
                "p^2*q",
                "p^3*q",
                "q^2",
                "p*q^2",
                "p^2*q^2",
                "p^3*q^2",
                "q^3",
                "p*q^3",
                "p^2*q^3",
                "p^3*q^3",
            ],
            "Q6_q_leading_coefficient": element_record(
                (algebra.q_leading_coefficient, Fp.zero, Fp.zero, Fp.zero),
                algebra,
            ),
            "Q6_q_leading_inverse": element_record(
                (algebra.q_leading_inverse, Fp.zero, Fp.zero, Fp.zero),
                algebra,
            ),
        },
        "Q6": polynomial_record(q6),
        "selectors": selector_metadata,
        "specialized_equations": {
            name: bt_record(specialized[name], algebra) for name in SELECTOR_ORDER
        },
        "resultant_proof": {
            "logic": (
                "a common T3=Y1=X3=0 point forces Res_t(T3,X3)=0 and "
                "Res_t(Y1,X3)=0; a unit B-resultant excludes their common B-root"
            ),
            "t_resultants": {
                name: poly_b_record(value, algebra)
                for name, value in t_resultants.items()
            },
            "B_sylvester_matrix_shape": [sylvester_size, sylvester_size],
            "B_resultant": element_record(
                b_resultant, algebra, include_coordinates=True
            ),
            "multiplication_matrix_shape": [16, 16],
            "multiplication_matrix_sha256": sha256_bytes(
                json.dumps(
                    [[rational_pair(value) for value in row] for row in matrix.tolist()],
                    separators=(",", ":"),
                ).encode("ascii")
            ),
            "multiplication_determinant": str(determinant),
            "multiplication_determinant_sha256": sha256_bytes(
                str(determinant).encode("ascii")
            ),
            "determinant_numerator_digits": len(str(abs(int(numerator)))),
            "determinant_denominator_digits": len(str(abs(int(denominator)))),
            "B_resultant_is_unit": True,
        },
        "provenance": {
            "accepted_equation_hash_lineage": (
                "the Q6,T3,Y1,X3 hashes agree with the historical exact R4 Singular "
                "source and its accepted independent direct-minor regeneration"
            ),
            "historical_source_sha256": (
                "fad9adaa23e2f94093b7b6db7875981ed0c7961791d2d01a4ab7a908fcab6cc1"
            ),
            "historical_cross_audit_sha256": (
                "6a00d6cc8023290a21d6133dbd19dfe4ff7a61acebc81de15dae23ba4f4c0068"
            ),
            "historical_transcript_role": (
                "accepted lineage only; the 50 MB Singular transcript and its giant "
                "multipliers are not inputs to this portable resultant proof"
            ),
            "load_bearing_evidence": (
                "tracked-parent determinant reconstruction, Delta-supported denominator "
                "clearing, exact R4/Q6 fibre arithmetic, the two t-resultants, their "
                "B-resultant, and its invertible 16x16 multiplication map"
            ),
        },
        "reproducible_commands": [
            "python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py",
            "python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py",
            "python -m unittest -v tests.test_gld101_r4_b_open_resultant_portable_leaf",
        ],
    }


def canonical_json(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def check(write_certificate: bool = False) -> dict[str, Any]:
    payload = build_certificate()
    encoded = canonical_json(payload)
    digest = sha256_bytes(encoded)
    if write_certificate:
        CERTIFICATE.write_bytes(encoded)
    else:
        require(CERTIFICATE.is_file(), f"missing certificate {CERTIFICATE}")
        require(lf_bytes(CERTIFICATE) == encoded, "certificate regeneration mismatch")
        require(
            digest == EXPECTED_CERTIFICATE_LF_SHA256,
            f"certificate pin mismatch: {digest}",
        )
    proof = payload["resultant_proof"]
    return {
        "status": "exact_scoped_R4_B_open_resultant_unit_verified",
        "global_conjecture": "UNRESOLVED",
        "certificate_lf_sha256": digest,
        "selectors": list(SELECTOR_ORDER),
        "B_sylvester_matrix_shape": proof["B_sylvester_matrix_shape"],
        "multiplication_matrix_shape": proof["multiplication_matrix_shape"],
        "multiplication_determinant_sha256": proof[
            "multiplication_determinant_sha256"
        ],
        "B_resultant_is_unit": proof["B_resultant_is_unit"],
        "certificate_written": write_certificate,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(json.dumps(check(write_certificate=args.write_certificate), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
