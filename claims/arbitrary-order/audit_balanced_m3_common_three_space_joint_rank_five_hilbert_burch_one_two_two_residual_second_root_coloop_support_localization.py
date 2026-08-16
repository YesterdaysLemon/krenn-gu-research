#!/usr/bin/env python3
"""Independent exact audit of the residual second-root-coloop localization.

This file imports neither the primary verifier nor a third-party package.  It
uses standard-library ``Fraction`` arithmetic, reverses the certificate's
variable order internally, expands permanents directly by coordinate loops,
and accumulates every Nullstellensatz identity as a sparse polynomial.
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
    "one_two_two_residual_second_root_coloop_certificates.json"
)
CERTIFICATE_SHA256 = (
    "3ea2f9470d210d85f2b45dce6fd23126888701a37634f07a32dd6750b71e96d5"
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
)
AUDIT_VARIABLES = tuple(reversed(CERTIFICATE_VARIABLES))
AUDIT_INDEX = {name: index for index, name in enumerate(AUDIT_VARIABLES)}
ZERO_EXPONENT = (0,) * len(AUDIT_VARIABLES)

Vector = tuple[F, ...]
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, F]


def unit(size: int, index: int) -> Vector:
    return tuple(F(position == index) for position in range(size))


def add_term(polynomial: Polynomial, exponent: Exponent, coefficient: F) -> None:
    if not coefficient:
        return
    value = polynomial.get(exponent, F(0)) + coefficient
    if value:
        polynomial[exponent] = value
    else:
        polynomial.pop(exponent, None)


def derivative_and_table_audit() -> None:
    # An exact rational fixture independently checks the two annihilator
    # equations for g_k and all h_m in the chart t=2,j=0,k=1.
    lam, mu = F(2), F(3)
    y = (F(5), F(7), F(0))
    z = (F(11), F(13), F(17))
    w = (F(19), F(23), F(29))

    alpha = (-y[1] / lam, F(0), F(0))
    beta = unit(3, 1)
    gamma = (F(0), F(0), F(0))
    assert lam * alpha[0] + sum(b * v for b, v in zip(beta, y, strict=True)) == 0
    assert mu * beta[2] + sum(g * v for g, v in zip(gamma, w, strict=True)) == 0
    assert beta[0] == 0

    for index in range(3):
        alpha = (-z[index] / lam, F(0), F(0))
        beta = (F(0), F(0), -w[index] / mu)
        gamma = unit(3, index)
        first = (
            lam * alpha[0]
            + sum(b * v for b, v in zip(beta, y, strict=True))
            + sum(g * v for g, v in zip(gamma, z, strict=True))
        )
        second = mu * beta[2] + sum(
            g * v for g, v in zip(gamma, w, strict=True)
        )
        assert first == second == 0
        assert beta[0] == 0

    # Direct target coefficients for w_t != 0.  The lifts have prescribed
    # j,k coordinates and annihilate w exactly.
    gamma_lifts = (
        (F(1), F(0), -w[0] / w[2]),
        (F(0), F(1), -w[1] / w[2]),
    )
    assert all(sum(g * v for g, v in zip(row, w, strict=True)) == 0 for row in gamma_lifts)
    for a, b, c in product(range(2), repeat=3):
        value = tuple(
            unit(3, a)[index] * unit(3, b)[index] * gamma_lifts[c][index]
            for index in range(3)
        )
        assert value == (unit(3, c) if a == b == c else (F(0),) * 3)
    print("independent face / coloop-row / binary-table audit: PASS")


def binary_cell(a: int, b: int, c: int) -> Vector:
    return unit(2, a) if a == b == c else (F(0), F(0))


def expanded_cell(left: Vector, middle: int, right: Vector) -> Vector:
    return tuple(
        sum(
            (
                left[a] * right[c] * binary_cell(a, middle, c)[target]
                for a, c in product(range(2), repeat=2)
            ),
            F(0),
        )
        for target in range(2)
    )


def incidence_audit() -> None:
    left = (F(2), F(3))
    right = (F(5), F(7))
    assert expanded_cell(left, 0, right) == (F(10), F(0))
    assert expanded_cell(left, 1, right) == (F(0), F(21))

    generic = (F(1), F(1))
    for endpoint in range(2):
        endpoint_row = unit(2, endpoint)
        other_row = unit(2, 1 - endpoint)
        square = [expanded_cell(endpoint_row, middle, generic) for middle in range(2)]
        mixed = [expanded_cell(other_row, middle, generic) for middle in range(2)]
        assert square[endpoint] == unit(2, endpoint)
        assert square[1 - endpoint] == (F(0), F(0))
        assert mixed[endpoint] == (F(0), F(0))
        assert mixed[1 - endpoint] == unit(2, 1 - endpoint)

    assert sum(1 for _ in product(range(2), range(2), range(1, 8))) == 28
    print("independent incidence case-cover audit: PASS")


def endpoint_rows(
    r_endpoint: int, q_endpoint: int, mask: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    common = unit(4, 0)
    r_other = unit(4, 1)
    q_other = unit(4, 2)
    p_zero = unit(4, 3)
    p_one = tuple(F((mask >> coordinate) & 1) for coordinate in range(3)) + (F(0),)

    r_rows = [r_other, r_other]
    q_rows = [q_other, q_other]
    r_rows[r_endpoint] = common
    q_rows[q_endpoint] = common
    return (tuple(r_rows), (p_zero, p_one), tuple(q_rows))  # type: ignore[return-value]


def evaluation_terms(root: str, bit: int, row: Vector) -> list[tuple[int, F]]:
    return [
        (AUDIT_INDEX[f"{root}{bit}{coordinate}"], coefficient)
        for coordinate, coefficient in enumerate(row)
        if coefficient
    ]


def permanent_polynomial(
    source_bits: tuple[int, int, int], rows: tuple[Vector, Vector, Vector]
) -> Polynomial:
    output: Polynomial = {}
    roots = ("x", "y", "z")
    for ordered_rows in permutations(rows):
        evaluations = [
            evaluation_terms(root, bit, row)
            for root, bit, row in zip(roots, source_bits, ordered_rows, strict=True)
        ]
        for choices in product(*evaluations):
            exponent = [0] * len(AUDIT_VARIABLES)
            coefficient = F(1)
            for variable, value in choices:
                exponent[variable] += 1
                coefficient *= value
            add_term(output, tuple(exponent), coefficient)
    return output


def endpoint_generators(r_endpoint: int, q_endpoint: int, mask: int) -> list[Polynomial]:
    r_rows, p_rows, q_rows = endpoint_rows(r_endpoint, q_endpoint, mask)
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
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 1):
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
        multiplier_coefficient, multiplier_exponent = decoded_term(raw_term)
        assert multiplier_exponent not in seen
        seen.add(multiplier_exponent)
        for generator_exponent, generator_coefficient in generator.items():
            product_exponent = tuple(
                left + right
                for left, right in zip(multiplier_exponent, generator_exponent, strict=True)
            )
            add_term(
                total,
                product_exponent,
                multiplier_coefficient * generator_coefficient,
            )


def certificate_audit() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-v1"
    assert tuple(data["variable_order"]) == CERTIFICATE_VARIABLES
    assert data["generator_order"] == "source_bits_then_row_bits_lexicographic"

    expected = {
        f"{r_endpoint}{q_endpoint}-{mask}"
        for r_endpoint, q_endpoint in product(range(2), repeat=2)
        for mask in range(1, 8)
    }
    assert set(data["cases"]) == expected

    term_count = 0
    for key in sorted(expected, reverse=True):
        endpoint_text, mask_text = key.split("-")
        r_endpoint, q_endpoint = (int(value) for value in endpoint_text)
        generators = endpoint_generators(r_endpoint, q_endpoint, int(mask_text))
        multipliers = data["cases"][key]
        assert len(multipliers) == len(generators) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, generators, strict=True):
            term_count += len(multiplier)
            add_multiplier_times_generator(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key

    assert term_count == 2310
    print(
        "independent sparse certificate audit: PASS "
        f"(28 cases / {term_count} multiplier terms)"
    )


def main() -> None:
    derivative_and_table_audit()
    incidence_audit()
    certificate_audit()
    print("independent residual second-root-coloop support audit: PASS")


if __name__ == "__main__":
    main()
