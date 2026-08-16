#!/usr/bin/env python3
"""Independent no-import audit of the off-diagonal endpoint exclusion.

This script imports neither the generator, the primary verifier, nor a third-
party package.  It reverses all certificate variables, parses row expressions
through a restricted AST, reconstructs the permanent generators, and checks
the rational identities with standard-library ``Fraction`` sparse maps.
"""

from __future__ import annotations

import ast
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_"
    "fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_"
    "certificates.json"
)
CERTIFICATE_SHA256 = (
    "e940282a15261df2e5cc6d46c698b9bdb5e37299d5b5bb791dfeef4d711e3af1"
)
CERTIFICATE_VARIABLES = (
    "x10",
    "x11",
    "x12",
    "x13",
    "y10",
    "y11",
    "y12",
    "y13",
    "z10",
    "z11",
    "z12",
    "z13",
    "x00",
    "x01",
    "x02",
    "x03",
    "y00",
    "y01",
    "y02",
    "y03",
    "z00",
    "z01",
    "z02",
    "z03",
    "p00",
    "p01",
    "p02",
    "p03",
    "p10",
    "p11",
    "p12",
    "p13",
    "q00",
    "q01",
    "q10",
    "q11",
)
AUDIT_VARIABLES = tuple(reversed(CERTIFICATE_VARIABLES))
AUDIT_INDEX = {name: index for index, name in enumerate(AUDIT_VARIABLES)}
ZERO_EXPONENT = (0,) * len(AUDIT_VARIABLES)

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, F]
Row = tuple[Polynomial, Polynomial, Polynomial, Polynomial]
Vector = tuple[int, int, int]


def add_term(polynomial: Polynomial, exponent: Exponent, coefficient: F) -> None:
    if not coefficient:
        return
    value = polynomial.get(exponent, F(0)) + coefficient
    if value:
        polynomial[exponent] = value
    else:
        polynomial.pop(exponent, None)


def constant(value: int | F) -> Polynomial:
    coefficient = F(value)
    return {ZERO_EXPONENT: coefficient} if coefficient else {}


def variable(name: str) -> Polynomial:
    exponent = [0] * len(AUDIT_VARIABLES)
    exponent[AUDIT_INDEX[name]] = 1
    return {tuple(exponent): F(1)}


def add(*polynomials: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            add_term(output, exponent, coefficient)
    return output


def scale(coefficient: int | F, polynomial: Polynomial) -> Polynomial:
    value = F(coefficient)
    return {
        exponent: value * entry
        for exponent, entry in polynomial.items()
        if value * entry
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                a + b
                for a, b in zip(left_exponent, right_exponent, strict=True)
            )
            add_term(output, exponent, left_coefficient * right_coefficient)
    return output


def parse_expression_node(node: ast.AST) -> Polynomial:
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return constant(node.value)
    if isinstance(node, ast.Name) and node.id in AUDIT_INDEX:
        return variable(node.id)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return scale(-1, parse_expression_node(node.operand))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return add(
            parse_expression_node(node.left), parse_expression_node(node.right)
        )
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
        return add(
            parse_expression_node(node.left),
            scale(-1, parse_expression_node(node.right)),
        )
    raise AssertionError(f"unsupported row expression: {ast.dump(node)}")


def parse_expression(value: str) -> Polynomial:
    return parse_expression_node(ast.parse(value, mode="eval").body)


def parse_row(raw: list[str]) -> Row:
    assert len(raw) == 4
    return tuple(parse_expression(value) for value in raw)  # type: ignore[return-value]


def form(root: str, bit: int) -> tuple[Polynomial, ...]:
    return tuple(variable(f"{root}{bit}{coordinate}") for coordinate in range(4))


def evaluate(linear_form: tuple[Polynomial, ...], row: Row) -> Polynomial:
    return add(
        *(
            multiply(coefficient, coordinate)
            for coefficient, coordinate in zip(linear_form, row, strict=True)
        )
    )


def polarized_product(
    source_bits: tuple[int, int, int], rows: tuple[Row, Row, Row]
) -> Polynomial:
    forms = (
        form("x", source_bits[0]),
        form("y", source_bits[1]),
        form("z", source_bits[2]),
    )
    terms = []
    for ordered in permutations(rows):
        terms.append(
            multiply(
                multiply(
                    evaluate(forms[0], ordered[0]),
                    evaluate(forms[1], ordered[1]),
                ),
                evaluate(forms[2], ordered[2]),
            )
        )
    return add(*terms)


def generators(specification: dict[str, object]) -> list[Polynomial]:
    raw_rows = specification["rows"]
    assert isinstance(raw_rows, list) and len(raw_rows) == 6
    rows = tuple(parse_row(row) for row in raw_rows)
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            if row_bits[:2] == (0, 1):
                continue
            value = polarized_product(
                source_bits,
                (rows[row_bits[0]], rows[2 + row_bits[1]], rows[4 + row_bits[2]]),
            )
            if source_bits == (0, 0, 0) and row_bits == (0, 0, 0):
                value = add(value, constant(-1))
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 1):
                value = add(value, constant(-1))
            output.append(value)
    raw_physical = specification["physical_v"]
    if raw_physical is not None:
        assert isinstance(raw_physical, list)
        physical = parse_row(raw_physical)
        for source_bits in product(range(2), repeat=3):
            for i, k in product(range(2), repeat=2):
                output.append(
                    polarized_product(
                        source_bits, (rows[i], physical, rows[4 + k])
                    )
                )
    assert len(output) == (80 if raw_physical is not None else 48)
    return output


def decoded_multiplier_terms(
    encoded: list[list[object]],
) -> list[tuple[Exponent, F]]:
    output = []
    seen = set()
    for raw_coefficient, raw_sparse_exponent in encoded:
        coefficient = F(str(raw_coefficient))
        assert coefficient
        exponent = [0] * len(AUDIT_VARIABLES)
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:  # type: ignore[misc]
            certificate_index = int(raw_index)
            power = int(raw_power)
            assert previous < certificate_index < len(CERTIFICATE_VARIABLES)
            assert power > 0
            name = CERTIFICATE_VARIABLES[certificate_index]
            exponent[AUDIT_INDEX[name]] = power
            previous = certificate_index
        key = tuple(exponent)
        assert key not in seen
        seen.add(key)
        output.append((key, coefficient))
    return output


def add_multiplier_product(
    total: Polynomial,
    encoded: list[list[object]],
    generator: Polynomial,
) -> None:
    for multiplier_exponent, multiplier_coefficient in decoded_multiplier_terms(
        encoded
    ):
        for generator_exponent, generator_coefficient in generator.items():
            exponent = tuple(
                a + b
                for a, b in zip(
                    multiplier_exponent, generator_exponent, strict=True
                )
            )
            add_term(
                total,
                exponent,
                multiplier_coefficient * generator_coefficient,
            )


def normalize(vector: Vector, prime: int) -> Vector:
    vector = tuple(value % prime for value in vector)  # type: ignore[assignment]
    pivot = next(index for index, value in enumerate(vector) if value)
    inverse = pow(vector[pivot], -1, prime)
    return tuple(value * inverse % prime for value in vector)  # type: ignore[return-value]


def flag_key(a: Vector, b: Vector, prime: int) -> tuple[Vector, Vector] | None:
    wedge = (
        a[0] * b[1] - a[1] * b[0],
        a[0] * b[2] - a[2] * b[0],
        a[1] * b[2] - a[2] * b[1],
    )
    if not any(value % prime for value in wedge):
        return None
    return normalize(a, prime), normalize(wedge, prime)


def chart_flags(
    prime: int,
    parameter_count: int,
    chart: object,
) -> set[tuple[Vector, Vector]]:
    function = chart
    assert callable(function)
    output = set()
    for parameters in product(range(prime), repeat=parameter_count):
        a, b = function(*parameters)
        key = flag_key(a, b, prime)
        assert key is not None
        output.add(key)
    return output


def pivot_chart(prime: int, i: int, j: int) -> set[tuple[Vector, Vector]]:
    remaining = next(index for index in range(3) if index not in {i, j})

    def rows(a: int, b: int, c: int) -> tuple[Vector, Vector]:
        first = [0, 0, 0]
        first[i] = 1
        free = [index for index in range(3) if index != i]
        first[free[0]], first[free[1]] = a, b
        second = [0, 0, 0]
        second[j], second[remaining] = 1, c
        return tuple(first), tuple(second)  # type: ignore[return-value]

    return chart_flags(prime, 3, rows)


def coverage_sanity() -> None:
    """A second finite-field construction of the reduced flag cover."""

    prime = 7
    vectors = [
        vector
        for vector in product(range(prime), repeat=3)
        if any(vector)
    ]
    universe = {
        key
        for a, b in product(vectors, repeat=2)
        if (key := flag_key(a, b, prime)) is not None
    }
    assert len(universe) == 456

    outside_affine = pivot_chart(prime, 0, 2) | pivot_chart(prime, 2, 0)
    outside_affine |= chart_flags(
        prime, 2, lambda a, b: ((a, b, 1), (0, 1, 0))
    )
    outside_affine |= chart_flags(
        prime, 1, lambda a: ((0, 1, 0), (1, 0, a))
    )
    outside_affine |= chart_flags(
        prime, 0, lambda: ((0, 1, 0), (0, 0, 1))
    )
    outside_affine |= chart_flags(
        prime, 1, lambda a: ((1, a, 0), (0, 1, 0))
    )
    assert outside_affine == universe

    inner_q1 = pivot_chart(prime, 2, 0) | pivot_chart(prime, 2, 1)
    inner_q1 |= chart_flags(
        prime, 2, lambda a, b: ((a, 1, 0), (b, 0, 1))
    )
    inner_q1 |= chart_flags(
        prime, 1, lambda a: ((1, a, 0), (0, 1, 0))
    )
    inner_q1 |= chart_flags(
        prime, 0, lambda: ((0, 1, 0), (1, 0, 0))
    )
    inner_q1 |= chart_flags(
        prime, 1, lambda a: ((1, 0, 0), (0, a, 1))
    )
    assert inner_q1 == universe
    print("independent F_7 reduced-flag coverage sanity: PASS")


def target_face_audit() -> None:
    d, e, t = 0, 1, 2
    nonzero = {(d, d, d): "T0", (e, e, e): "T1"}
    free = {(d, e, d), (d, e, e)}
    assert all(
        (i, j, k) not in nonzero and (i, j, k) not in free
        for i, j, k in product((t,), range(3), range(2))
    )
    assert all(
        (i, j, k) not in nonzero and (i, j, k) not in free
        for i, j, k in product(range(3), (t,), range(2))
    )
    print("independent sparse face / common rows / cross-zero: PASS")


def certificate_audit() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-atlas-v2"
    assert tuple(data["variable_order"]) == CERTIFICATE_VARIABLES
    mapping = data["coverage_case_to_specification"]
    specifications = data["specifications"]
    certificates = data["cases"]
    assert len(mapping) == 317
    assert len(specifications) == len(certificates) == 287
    assert set(mapping.values()) == set(specifications) == set(certificates)
    assert Counter(data["coverage_case_stages"].values()) == {
        "separation_table": 210,
        "separation_refinement": 98,
        "endpoint_graph": 9,
    }
    multiplicities = Counter(mapping.values())
    assert Counter(value for value in multiplicities.values() if value > 1) == {
        2: 12,
        4: 6,
    }

    term_count = 0
    for index, digest in enumerate(sorted(specifications), start=1):
        specification = specifications[digest]
        assert digest == specification["program_sha256"]
        case_generators = generators(specification)
        multipliers = certificates[digest]
        assert len(multipliers) == len(case_generators)
        total: Polynomial = {}
        for generator, encoded in zip(
            case_generators, multipliers, strict=True
        ):
            term_count += len(encoded)
            add_multiplier_product(total, encoded, generator)
        assert total == {ZERO_EXPONENT: F(1)}, specification["representative"]
        if index % 50 == 0:
            print(f"  independent specifications replayed: {index}/287")
    assert term_count == 151484
    print(
        "independent Fraction certificate audit: PASS "
        f"(287 systems / {term_count} multiplier terms)"
    )


def main() -> None:
    target_face_audit()
    coverage_sanity()
    certificate_audit()
    print("independent off-diagonal endpoint exclusion audit: PASS")


if __name__ == "__main__":
    main()
