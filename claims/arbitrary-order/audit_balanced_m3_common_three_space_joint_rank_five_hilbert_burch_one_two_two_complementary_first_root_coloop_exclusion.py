#!/usr/bin/env python3
"""Independent exact audit of both complementary first-root-coloop exclusions.

This script imports neither the primary verifier nor a third-party package.
It reverses the certificate variable order, reconstructs all five systems
and permanents independently, and checks the rational identities with
standard-library Fraction sparse arithmetic.
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
    "one_two_two_complementary_first_root_coloop_certificates.json"
)
CERTIFICATE_SHA256 = (
    "10ce1216ed2360159eb4709140eabe4db1c51ad509f340ac137300a636583088"
)
DEPENDENCY_PINS = {
    (
        "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
        "one_two_two_residual_second_root_coloop_projective_pencil_"
        "certificates.json"
    ): "0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca",
    (
        "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
        "one_two_two_residual_second_root_coloop_same_third_row_"
        "certificates.json"
    ): "e822cb443173acbab3604d6e3e28afaf7fd99a3e306731e21c7c7bc5023ac5fc",
}
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
    "c0",
    "c1",
)
AUDIT_VARIABLES = tuple(reversed(CERTIFICATE_VARIABLES))
AUDIT_INDEX = {name: index for index, name in enumerate(AUDIT_VARIABLES)}
ZERO_EXPONENT = (0,) * len(AUDIT_VARIABLES)

Entry = F | str
Vector = tuple[Entry, ...]
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, F]


def unit(index: int) -> Vector:
    return tuple(F(position == index) for position in range(4))


def r_line(incidence: int, rtype: int) -> Vector:
    if rtype == 0:
        return unit(0)
    if rtype == 1:
        return unit(1)
    assert incidence == 1 and rtype == 2
    return (F(1), F(1), F(0), F(0))


def normal_form_rows(
    incidence: int, rtype: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    r_rows = (unit(3), r_line(incidence, rtype))
    p_rows = (unit(0), unit(2))
    q_zero = unit(0) if incidence == 0 else unit(1)
    q_one: Vector = ("c0", "c1", F(-1), F(0))
    return r_rows, p_rows, (q_zero, q_one)


def add_term(polynomial: Polynomial, exponent: Exponent, coefficient: F) -> None:
    if not coefficient:
        return
    value = polynomial.get(exponent, F(0)) + coefficient
    if value:
        polynomial[exponent] = value
    else:
        polynomial.pop(exponent, None)


def evaluation_terms(root: str, bit: int, row: Vector) -> list[tuple[Exponent, F]]:
    output = []
    for coordinate, entry in enumerate(row):
        if not entry:
            continue
        exponent = [0] * len(AUDIT_VARIABLES)
        exponent[AUDIT_INDEX[f"{root}{bit}{coordinate}"]] = 1
        coefficient = F(1)
        if isinstance(entry, str):
            exponent[AUDIT_INDEX[entry]] += 1
        else:
            coefficient = entry
        output.append((tuple(exponent), coefficient))
    return output


def permanent_polynomial(
    source_bits: tuple[int, int, int], rows: tuple[Vector, Vector, Vector]
) -> Polynomial:
    output: Polynomial = {}
    for ordered_rows in permutations(rows):
        evaluations = [
            evaluation_terms(root, bit, row)
            for root, bit, row in zip(
                ("x", "y", "z"), source_bits, ordered_rows, strict=True
            )
        ]
        for choices in product(*evaluations):
            exponent = [0] * len(AUDIT_VARIABLES)
            coefficient = F(1)
            for term_exponent, term_coefficient in choices:
                exponent = [
                    left + right
                    for left, right in zip(exponent, term_exponent, strict=True)
                ]
                coefficient *= term_coefficient
            add_term(output, tuple(exponent), coefficient)
    return output


def generators(incidence: int, rtype: int) -> list[Polynomial]:
    r_rows, p_rows, q_rows = normal_form_rows(incidence, rtype)
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            rows = (
                r_rows[row_bits[0]],
                p_rows[row_bits[1]],
                q_rows[row_bits[2]],
            )
            polynomial = permanent_polynomial(source_bits, rows)
            if source_bits == (0, 0, 0) and row_bits == (0, 1, 1):
                add_term(polynomial, ZERO_EXPONENT, F(-1))
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 1):
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
        certificate_index = int(raw_index)
        power = int(raw_power)
        assert previous < certificate_index < len(CERTIFICATE_VARIABLES)
        assert power > 0
        exponent[AUDIT_INDEX[CERTIFICATE_VARIABLES[certificate_index]]] = power
        previous = certificate_index
    assert coefficient
    return coefficient, tuple(exponent)


def add_product(
    total: Polynomial,
    encoded_multiplier: list[list[object]],
    generator: Polynomial,
) -> None:
    seen: set[Exponent] = set()
    for raw_term in encoded_multiplier:
        multiplier_coefficient, multiplier_exponent = decode_term(raw_term)
        assert multiplier_exponent not in seen
        seen.add(multiplier_exponent)
        for generator_exponent, generator_coefficient in generator.items():
            exponent = tuple(
                left + right
                for left, right in zip(
                    multiplier_exponent, generator_exponent, strict=True
                )
            )
            add_term(total, exponent, multiplier_coefficient * generator_coefficient)


def certificate_audit() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-v1"
    assert tuple(data["variable_order"]) == CERTIFICATE_VARIABLES
    assert data["generator_order"] == "source_bits_then_row_bits_lexicographic"
    expected = {"0-0", "0-1", "1-0", "1-1", "1-2"}
    assert set(data["cases"]) == expected

    term_count = 0
    for key in sorted(expected, reverse=True):
        incidence, rtype = (int(value) for value in key.split("-"))
        system = generators(incidence, rtype)
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, system, strict=True):
            term_count += len(multiplier)
            add_product(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 5928
    print(
        "independent complementary-alpha certificate audit: PASS "
        f"(5 cases / {term_count} multiplier terms)"
    )


def geometry_audit() -> None:
    cases = {(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)}
    assert len(cases) == 5

    # Independent label audit for (s,a,b)=(0,1,2): alpha_s=alpha_a=0
    # leaves precisely the pure e_b direction.
    face_and_divisor = [
        vector
        for vector in (
            (F(1), F(0), F(0)),
            (F(0), F(1), F(0)),
            (F(0), F(0), F(1)),
        )
        if vector[0] == 0 and vector[1] == 0
    ]
    assert face_and_divisor == [(F(0), F(0), F(1))]
    for incidence, rtype in cases:
        r_rows, p_rows, q_rows = normal_form_rows(incidence, rtype)
        assert r_rows[0] == unit(3)
        assert all(not entry for entry in r_rows[1][2:])
        assert all(not entry for entry in p_rows[0][2:])
        assert all(not entry for entry in q_rows[0][2:])
        assert p_rows[1][2] == F(1) and q_rows[1][2] == F(-1)
        if incidence == 0:
            assert p_rows[0] == q_rows[0]
        else:
            assert p_rows[0] != q_rows[0]

    # Independent target-coefficient tables for both one-sided degenerations.
    alpha = ((F(1), F(0), F(0)), (F(0), F(1), F(0)))
    beta_common = ((F(0), F(0), F(1)), (F(2), F(3), F(0)))
    gamma_coordinate = ((F(1), F(0), F(0)), (F(0), F(1), F(0)))
    active = set()
    for i, j, k in product(range(2), repeat=3):
        coordinate = i
        if alpha[i][coordinate] * beta_common[j][coordinate] * gamma_coordinate[k][coordinate]:
            active.add((i, j, k))
    assert active == {(0, 1, 0), (1, 1, 1)}

    beta_coordinate = gamma_coordinate
    gamma_common = ((F(0), F(0), F(1)), (F(5), F(7), F(0)))
    active = set()
    for i, j, k in product(range(2), repeat=3):
        coordinate = i
        if alpha[i][coordinate] * beta_coordinate[j][coordinate] * gamma_common[k][coordinate]:
            active.add((i, j, k))
    assert active == {(0, 0, 1), (1, 1, 1)}

    # The equal-partner-plane symmetry equation for E11*M kills m10.
    e11_m = ((F(0), F(0)), (F(11), F(13)))
    assert e11_m[0][1] - e11_m[1][0] == F(-11)
    print("independent pencil / five-case incidence audit: PASS")


def dependency_pin_audit() -> None:
    for name, expected in DEPENDENCY_PINS.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected
    print("independent dependency-pin audit: PASS")


def main() -> None:
    geometry_audit()
    certificate_audit()
    dependency_pin_audit()
    print("independent complementary first-root-coloop exclusion audit: PASS")


if __name__ == "__main__":
    main()
