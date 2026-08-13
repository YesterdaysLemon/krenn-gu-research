#!/usr/bin/env python3
"""Independent exact audit of residual beta-coloop line localization.

This file imports neither the primary verifier nor a third-party package.  It
reverses the certificate variable order and rebuilds every source evaluation,
permanent, generator, and rational identity with sparse ``Fraction`` maps.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_same_third_row_certificates.json"
)
CERTIFICATE_SHA256 = (
    "e822cb443173acbab3604d6e3e28afaf7fd99a3e306731e21c7c7bc5023ac5fc"
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
    "tau",
)
AUDIT_VARIABLES = tuple(reversed(CERTIFICATE_VARIABLES))
AUDIT_INDEX = {name: index for index, name in enumerate(AUDIT_VARIABLES)}
ZERO_EXPONENT = (0,) * len(AUDIT_VARIABLES)

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, F]
Row = tuple[Polynomial, ...]


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


def scale(value: int | F, polynomial: Polynomial) -> Polynomial:
    coefficient = F(value)
    return {
        exponent: coefficient * entry
        for exponent, entry in polynomial.items()
        if coefficient * entry
    }


def unit_row(size: int, index: int) -> tuple[F, ...]:
    return tuple(F(position == index) for position in range(size))


def face_and_incidence_audit() -> None:
    wj, wk = F(2), F(3)
    w = (wj, wk, F(0))
    third_rows = ((wk, -wj, F(0)), unit_row(3, 2))
    assert all(
        sum((left * right for left, right in zip(row, w, strict=True)), F(0))
        == 0
        for row in third_rows
    )
    roots = (unit_row(3, 0), unit_row(3, 1))
    for a, b, c in product(range(2), repeat=3):
        value = tuple(
            roots[a][index] * roots[b][index] * third_rows[c][index]
            for index in range(3)
        )
        expected = (F(0),) * 3
        if a == b == 0 and c == 0:
            expected = (wk, F(0), F(0))
        if a == b == 1 and c == 0:
            expected = (F(0), -wj, F(0))
        assert value == expected

    # ell=a0*r0+a1*r1=b0*q0+b1*q1.  The two square values are
    # a0*b0*T0 and a1*b0*T1.  A coordinate ell in R with b0 nonzero
    # has a square on one target and a mixed map on the other.
    left = (F(2), F(3))
    right = (F(5), F(7))

    def cell(a: int, middle: int, c: int) -> tuple[F, F]:
        if c == 0 and a == middle:
            return unit_row(2, a)  # type: ignore[return-value]
        return (F(0), F(0))

    def expanded(left_row: tuple[F, F], middle: int, right_row: tuple[F, F]) -> tuple[F, F]:
        return tuple(
            sum(
                (
                    left_row[a] * right_row[c] * cell(a, middle, c)[target]
                    for a, c in product(range(2), repeat=2)
                ),
                F(0),
            )
            for target in range(2)
        )  # type: ignore[return-value]

    assert expanded(left, 0, right) == (F(10), F(0))
    assert expanded(left, 1, right) == (F(0), F(15))
    for endpoint in range(2):
        endpoint_row = unit_row(2, endpoint)
        other_row = unit_row(2, 1 - endpoint)
        generic_q = (F(1), F(1))
        square = [expanded(endpoint_row, middle, generic_q) for middle in range(2)]
        mixed = [expanded(other_row, middle, generic_q) for middle in range(2)]
        assert square[endpoint] == unit_row(2, endpoint)
        assert square[1 - endpoint] == (F(0), F(0))
        assert mixed[endpoint] == (F(0), F(0))
        assert mixed[1 - endpoint] == unit_row(2, 1 - endpoint)
    print("independent same-third-row face / incidence audit: PASS")


def expected_case_keys() -> set[str]:
    cases = {
        f"endpoint-{endpoint}-{support_mask}"
        for endpoint in range(2)
        for support_mask in range(1, 8)
    }
    cases.update(
        f"generic-fixed-{support_mask}"
        for support_mask in (1, 2, 4, 5, 6)
    )
    cases.update(
        f"generic-parameter-{support_mask}" for support_mask in (3, 7)
    )
    return cases


def row_from_scalars(values: tuple[int, int, int, int]) -> Row:
    return tuple(constant(value) for value in values)


def mask_row(support_mask: int) -> Row:
    return row_from_scalars(
        tuple((support_mask >> coordinate) & 1 for coordinate in range(3))
        + (0,)
    )


def case_rows(key: str) -> tuple[tuple[Row, Row], tuple[Row, Row], tuple[Row, Row]]:
    r_rows = (row_from_scalars((1, 0, 0, 0)), row_from_scalars((0, 1, 0, 0)))
    p_zero = row_from_scalars((0, 0, 0, 1))
    q_zero = row_from_scalars((0, 0, 1, 0))
    fields = key.split("-")
    if fields[0] == "endpoint":
        endpoint = int(fields[1])
        support_mask = int(fields[2])
        q_one = r_rows[endpoint]
        p_one = mask_row(support_mask)
    elif fields[:2] == ["generic", "fixed"]:
        support_mask = int(fields[2])
        q_one = row_from_scalars((1, 1, 0, 0))
        p_one = mask_row(support_mask)
    elif fields[:2] == ["generic", "parameter"]:
        support_mask = int(fields[2])
        assert support_mask in (3, 7)
        q_one = row_from_scalars((1, 1, 0, 0))
        p_one = (
            constant(1),
            variable("tau"),
            constant(support_mask == 7),
            constant(0),
        )
    else:
        raise AssertionError(key)
    return r_rows, (p_zero, p_one), (q_zero, q_one)


def evaluate_form(root: str, bit: int, row: Row) -> Polynomial:
    return add(
        *(
            multiply(variable(f"{root}{bit}{coordinate}"), row[coordinate])
            for coordinate in range(4)
        )
    )


def permanent_polynomial(
    source_bits: tuple[int, int, int], rows: tuple[Row, Row, Row]
) -> Polynomial:
    output: Polynomial = {}
    roots = ("x", "y", "z")
    for ordered_rows in permutations(rows):
        evaluations = [
            evaluate_form(root, bit, row)
            for root, bit, row in zip(roots, source_bits, ordered_rows, strict=True)
        ]
        output = add(output, multiply(multiply(evaluations[0], evaluations[1]), evaluations[2]))
    return output


def case_generators(key: str) -> list[Polynomial]:
    r_rows, p_rows, q_rows = case_rows(key)
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            rows = (
                r_rows[row_bits[0]],
                p_rows[row_bits[1]],
                q_rows[row_bits[2]],
            )
            polynomial = permanent_polynomial(source_bits, rows)
            if source_bits == (0, 0, 0) and row_bits == (0, 0, 0):
                add_term(polynomial, ZERO_EXPONENT, F(-1))
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 0):
                add_term(polynomial, ZERO_EXPONENT, F(-1))
            output.append(polynomial)
    assert len(output) == 64
    return output


def decoded_term(raw_term: list[object]) -> tuple[F, Exponent]:
    raw_coefficient, raw_sparse_exponent = raw_term
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
    return coefficient, tuple(exponent)


def add_multiplier_times_generator(
    total: Polynomial,
    encoded_multiplier: list[list[object]],
    generator: Polynomial,
) -> None:
    seen: set[Exponent] = set()
    for raw_term in encoded_multiplier:
        coefficient, exponent = decoded_term(raw_term)
        assert exponent not in seen
        seen.add(exponent)
        multiplier = {exponent: coefficient}
        product_polynomial = multiply(multiplier, generator)
        for product_exponent, product_coefficient in product_polynomial.items():
            add_term(total, product_exponent, product_coefficient)


def certificate_audit() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-v1"
    assert tuple(data["variable_order"]) == CERTIFICATE_VARIABLES
    assert data["generator_order"] == "source_bits_then_row_bits_lexicographic"
    expected = expected_case_keys()
    assert set(data["cases"]) == expected

    term_count = 0
    for key in sorted(expected, reverse=True):
        generators = case_generators(key)
        multipliers = data["cases"][key]
        assert len(multipliers) == len(generators) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, generators, strict=True):
            term_count += len(multiplier)
            add_multiplier_times_generator(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 9256
    print(
        "independent sparse same-third-row certificates: PASS "
        f"(21 families / {term_count} multiplier terms)"
    )


def main() -> None:
    face_and_incidence_audit()
    certificate_audit()
    print("independent residual beta-coloop coordinate-line audit: PASS")


if __name__ == "__main__":
    main()
