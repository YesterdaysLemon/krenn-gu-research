#!/usr/bin/env python3
"""Verify the five-equation Laurent core on one exact-two P5 support."""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu import p5_exact_two_support_system as GENERATOR


VARIABLES = tuple(f"u{index}" for index in range(24))
ZERO_EXPONENT = (0,) * len(VARIABLES)
IDEAL = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)
EXPECTED_WORDS = {
    180: (2, 2, 0, 0, 1),
    181: (2, 2, 0, 0, 2),
    197: (2, 2, 2, 0, 0),
    198: (2, 2, 2, 0, 1),
    199: (2, 2, 2, 0, 2),
}
EXPECTED_POLYNOMIALS = {
    180: (
        "u22+u15+u15*u20+u3*u8*u15+u3*u6*u22+u3*u6*u15*u20"
        "+u0*u8*u15+u0*u6*u22+u0*u6*u15*u20"
    ),
    181: (
        "u23+u15*u19+u8*u15+u6*u15+u3*u8*u15*u19"
        "+u3*u6*u23+u0*u8*u15*u19+u0*u6*u23"
    ),
    197: (
        "u3*u21+u3*u11+u3*u11*u18+u3*u10*u15"
        "+u3*u10*u15*u18+u0*u21+u0*u15+u0*u11*u18"
        "+u0*u10*u15*u18"
    ),
    198: (
        "u3*u22+u3*u15*u20+u3*u11+u3*u10*u15+u0*u22"
        "+u0*u15*u20+u0*u11+u0*u10*u15"
    ),
    199: (
        "u15+u11+u10*u15+u3*u23+u3*u11*u19"
        "+u3*u10*u15*u19+u0*u23+u0*u11*u19"
        "+u0*u10*u15*u19"
    ),
}


@dataclass(frozen=True)
class Polynomial:
    terms: tuple[tuple[tuple[int, ...], int], ...]

    @staticmethod
    def make(terms: dict[tuple[int, ...], int]) -> "Polynomial":
        return Polynomial(
            tuple(
                sorted(
                    (exponent, coefficient)
                    for exponent, coefficient in terms.items()
                    if coefficient
                )
            )
        )

    @staticmethod
    def constant(value: int) -> "Polynomial":
        return Polynomial.make({ZERO_EXPONENT: value})

    @staticmethod
    def variable(index: int) -> "Polynomial":
        exponent = [0] * len(VARIABLES)
        exponent[index] = 1
        return Polynomial.make({tuple(exponent): 1})

    def as_dict(self) -> dict[tuple[int, ...], int]:
        return dict(self.terms)

    def __add__(self, other: "Polynomial") -> "Polynomial":
        output = self.as_dict()
        for exponent, coefficient in other.terms:
            output[exponent] = output.get(exponent, 0) + coefficient
        return Polynomial.make(output)

    def __neg__(self) -> "Polynomial":
        return Polynomial.make(
            {
                exponent: -coefficient
                for exponent, coefficient in self.terms
            }
        )

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        return self + (-other)

    def __mul__(self, other: "Polynomial") -> "Polynomial":
        output: dict[tuple[int, ...], int] = {}
        for left_exponent, left_coefficient in self.terms:
            for right_exponent, right_coefficient in other.terms:
                exponent = tuple(
                    left + right
                    for left, right in zip(
                        left_exponent,
                        right_exponent,
                        strict=True,
                    )
                )
                output[exponent] = (
                    output.get(exponent, 0)
                    + left_coefficient * right_coefficient
                )
        return Polynomial.make(output)

    def __rmul__(self, value: int) -> "Polynomial":
        return Polynomial.constant(value) * self


U = tuple(Polynomial.variable(index) for index in range(len(VARIABLES)))
ONE = Polynomial.constant(1)
ZERO = Polynomial.constant(0)


def parse_polynomial(text: str) -> Polynomial:
    tree = ast.parse(text, mode="eval")

    def visit(node: ast.AST) -> Polynomial:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Name):
            if node.id not in VARIABLES:
                raise AssertionError(f"unknown variable: {node.id}")
            return U[VARIABLES.index(node.id)]
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return Polynomial.constant(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            left = visit(node.left)
            right = visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
        raise AssertionError(f"unsupported polynomial syntax: {ast.dump(node)}")

    return visit(tree)


def require_zero(polynomial: Polynomial, label: str) -> None:
    if polynomial != ZERO:
        raise AssertionError(f"polynomial identity failed: {label}")


def main() -> None:
    supports = (
        (6, 6, 4, 1, 1),
        (7, 7, 1, 4, 2),
        (2, 1, 7, 7, 4),
        (4, 2, 2, 7, 7),
        (1, 4, 7, 2, 7),
    )
    indices = (4799, 6049, 1565, 3279, 779)
    program, metadata = GENERATOR.generate(supports, indices)
    ideal = IDEAL.search(program)
    if ideal is None:
        raise AssertionError("regenerated source has no recognizable ideal")
    equations = ideal.group("equations").split(",\n")
    mixed = equations[:-1]
    if metadata != {
        "nonzero_entries": 43,
        "gauge_free_variables": 24,
        "laurent_parameters": 24,
        "mixed_equations": 205,
        "pure_coefficients": 3,
    }:
        raise AssertionError(f"system metadata changed: {metadata}")
    for index, expected in EXPECTED_POLYNOMIALS.items():
        if mixed[index] != expected:
            raise AssertionError(f"mixed equation {index} changed")

    a, b, p = U[3], U[0], U[15]
    h, k, ell = U[8], U[6], U[19]
    q, r = U[10], U[11]
    s, t = U[18], U[20]
    v, x, y = U[23], U[21], U[22]
    capital_a = a + b
    capital_b = ONE + capital_a * k
    capital_c = ONE + capital_a * h
    capital_r = r + q * p

    factors = {
        180: capital_b * (y + p * t) + p * capital_c,
        181: capital_b * v + p * (k + h + ell * capital_c),
        197: (
            capital_a * (x + s * capital_r)
            + a * capital_r
            + b * p
        ),
        198: capital_a * (y + p * t + capital_r),
        199: p + capital_r + capital_a * (v + ell * capital_r),
    }
    for index, factored in factors.items():
        require_zero(
            parse_polynomial(EXPECTED_POLYNOMIALS[index]) - factored,
            f"coefficient factorization {index}",
        )

    f1, f2, f3, f4, f5 = (
        factors[index] for index in EXPECTED_WORDS
    )
    capital_d = p * capital_c - capital_b * capital_r
    capital_h = (
        capital_a * p * (k + h)
        - capital_b * (p + capital_r)
    )
    require_zero(
        capital_a * f1 - capital_b * f4 - capital_a * capital_d,
        "A F1 - B F4 = A D",
    )
    require_zero(
        capital_a * f2
        - capital_b * f5
        - capital_h
        - ell * capital_a * capital_d,
        "A F2 - B F5 = H + l A D",
    )
    require_zero(capital_d - capital_h - 2 * p, "D - H = 2p")
    require_zero(
        a * f5
        - f3
        - 2 * a * p
        - capital_a * (a * (v + ell * capital_r) - x - s * capital_r - p),
        "a F5 - F3 branch identity",
    )

    print(
        json.dumps(
            {
                "verified": True,
                "scope": "one exact-two-partial C4+C6 P5 support",
                "full_mixed_equations": len(mixed),
                "core_mixed_equations": len(factors),
                "core_colour_words": [
                    "".join(map(str, EXPECTED_WORDS[index]))
                    for index in EXPECTED_WORDS
                ],
                "required_nonzero_variables": ["u0", "u3", "u15"],
                "characteristic_excluded": 2,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
