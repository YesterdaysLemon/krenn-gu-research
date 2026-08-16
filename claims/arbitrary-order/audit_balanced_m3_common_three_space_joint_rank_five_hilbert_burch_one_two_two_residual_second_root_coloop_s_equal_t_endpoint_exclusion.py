#!/usr/bin/env python3
"""Independent exact audit of residual-coloop ``s=t`` endpoint exclusion.

This file imports neither the primary verifier nor a third-party package.  It
reverses the variable order and rebuilds every row, permanent, generator, and
rational identity with standard-library ``Fraction`` sparse maps.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_"
    "residual_second_root_coloop_s_equal_t_endpoint_certificates.json"
)
CERTIFICATE_SHA256 = (
    "ceb0c69b151523c43219d294806d50a1e1b2905bc7237c6a3709451fc868b9a0"
)
CERTIFICATE_VARIABLES = (
    "x10", "x11", "x12", "x13",
    "y10", "y11", "y12", "y13",
    "z10", "z11", "z12", "z13",
    "x00", "x01", "x02", "x03",
    "y00", "y01", "y02", "y03",
    "z00", "z01", "z02", "z03",
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


def unit(size: int, index: int) -> tuple[F, ...]:
    return tuple(F(position == index) for position in range(size))


def face_and_incidence_audit() -> None:
    # Normalize s=t=2 and audit both coordinate endpoints with an exact
    # projective direction whose active third row has both I-coordinates.
    mu, h, kappa = F(2), F(3), F(5)
    y = (F(13), F(17), F(0))
    normal_p = tuple(kappa * y[i] - h * mu * F(i == 2) for i in range(3))
    beta_lifts = tuple(
        tuple(
            F(i == a) + F(i == 2) * kappa * y[a] / (h * mu)
            for i in range(3)
        )
        for a in range(2)
    )
    assert normal_p[2] == -h * mu
    assert all(
        sum(a * b for a, b in zip(beta, normal_p, strict=True)) == 0
        for beta in beta_lifts
    )
    for endpoint in range(2):
        other = 1 - endpoint
        z = [F(0), F(0), F(0)]
        w = [F(0), F(0), F(0)]
        z[endpoint], z[other], w[endpoint] = F(7), F(11), F(1)
        normal = tuple(kappa * z[i] - h * w[i] for i in range(3))
        assert normal[2] == 0
        gamma_active = (normal[1], -normal[0], F(0))
        assert gamma_active[0] * gamma_active[1]
        assert sum(a * b for a, b in zip(gamma_active, normal, strict=True)) == 0
        roots = (unit(3, 0), unit(3, 1))
        third = (gamma_active, unit(3, 2))
        for a, b, c in product(range(2), repeat=3):
            value = tuple(
                roots[a][i] * beta_lifts[b][i] * third[c][i]
                for i in range(3)
            )
            expected = (F(0),) * 3
            if a == b and c == 0:
                expected = tuple(gamma_active[a] * entry for entry in unit(3, a))
            assert value == expected

    def cell(a: int, middle: int, c: int) -> tuple[F, F]:
        return unit(2, a) if c == 0 and a == middle else (F(0), F(0))

    def expanded(
        left: tuple[F, F], middle: int, right: tuple[F, F]
    ) -> tuple[F, F]:
        return tuple(
            sum(
                (
                    left[a] * right[c] * cell(a, middle, c)[target]
                    for a, c in product(range(2), repeat=2)
                ),
                F(0),
            )
            for target in range(2)
        )  # type: ignore[return-value]

    assert expanded((F(2), F(3)), 0, (F(5), F(7))) == (F(10), F(0))
    assert expanded((F(2), F(3)), 1, (F(5), F(7))) == (F(0), F(15))
    assert len(expected_case_keys()) == 21
    print("independent s=t face / generalized incidence audit: PASS")


def expected_case_keys() -> set[str]:
    cases = {
        f"endpoint-{endpoint}-{mask}"
        for endpoint in range(2)
        for mask in range(1, 8)
    }
    cases.update(f"generic-fixed-{mask}" for mask in (1, 2, 4, 5, 6))
    cases.update(f"generic-parameter-{mask}" for mask in (3, 7))
    return cases


def scalar_row(values: tuple[int, int, int, int]) -> Row:
    return tuple(constant(value) for value in values)


def mask_intersection(mask: int) -> tuple[Polynomial, Polynomial, Polynomial]:
    return tuple(
        constant((mask >> coordinate) & 1) for coordinate in range(3)
    )  # type: ignore[return-value]


def case_rows(key: str) -> tuple[tuple[Row, Row], tuple[Row, Row], tuple[Row, Row]]:
    r_rows = (scalar_row((1, 0, 0, 0)), scalar_row((0, 1, 0, 0)))
    p_zero = scalar_row((0, 0, 0, 1))
    q_zero = scalar_row((0, 0, 1, 0))
    fields = key.split("-")
    if fields[0] == "endpoint":
        endpoint, mask = int(fields[1]), int(fields[2])
        q_one = r_rows[endpoint]
        intersection = mask_intersection(mask)
    elif fields[:2] == ["generic", "fixed"]:
        mask = int(fields[2])
        q_one = scalar_row((1, 1, 0, 0))
        intersection = mask_intersection(mask)
    elif fields[:2] == ["generic", "parameter"]:
        mask = int(fields[2])
        assert mask in (3, 7)
        q_one = scalar_row((1, 1, 0, 0))
        intersection = (constant(1), variable("tau"), constant(mask == 7))
    else:
        raise AssertionError(key)
    p_one = intersection + (constant(-1),)
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
    for ordered_rows in permutations(rows):
        evaluations = [
            evaluate_form(root, bit, row)
            for root, bit, row in zip(
                ("x", "y", "z"), source_bits, ordered_rows, strict=True
            )
        ]
        output = add(
            output,
            multiply(multiply(evaluations[0], evaluations[1]), evaluations[2]),
        )
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


def decode_term(raw_term: list[object]) -> tuple[F, Exponent]:
    raw_coefficient, raw_sparse_exponent = raw_term
    coefficient = F(str(raw_coefficient))
    exponent = [0] * len(AUDIT_VARIABLES)
    previous = -1
    for raw_index, raw_power in raw_sparse_exponent:  # type: ignore[misc]
        certificate_index, power = int(raw_index), int(raw_power)
        assert previous < certificate_index < len(CERTIFICATE_VARIABLES)
        assert power > 0
        exponent[AUDIT_INDEX[CERTIFICATE_VARIABLES[certificate_index]]] = power
        previous = certificate_index
    assert coefficient
    return coefficient, tuple(exponent)


def add_multiplier_product(
    total: Polynomial,
    encoded_multiplier: list[list[object]],
    generator: Polynomial,
) -> None:
    seen: set[Exponent] = set()
    for raw_term in encoded_multiplier:
        coefficient, multiplier_exponent = decode_term(raw_term)
        assert multiplier_exponent not in seen
        seen.add(multiplier_exponent)
        for generator_exponent, generator_coefficient in generator.items():
            exponent = tuple(
                left + right
                for left, right in zip(
                    multiplier_exponent, generator_exponent, strict=True
                )
            )
            add_term(total, exponent, coefficient * generator_coefficient)


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
        assert len(generators) == len(multipliers) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, generators, strict=True):
            term_count += len(multiplier)
            add_multiplier_product(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 44806
    print(
        "independent s=t endpoint certificate audit: PASS "
        f"(21 families / {term_count} multiplier terms)"
    )


def main() -> None:
    face_and_incidence_audit()
    certificate_audit()
    print("independent residual-coloop s=t endpoint audit: PASS")


if __name__ == "__main__":
    main()
