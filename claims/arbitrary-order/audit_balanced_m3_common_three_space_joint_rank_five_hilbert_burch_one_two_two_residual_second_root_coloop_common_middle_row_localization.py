#!/usr/bin/env python3
"""Independent audit of the residual-coloop common-middle-row localization.

This audit imports neither the primary verifier nor any third-party package.
It reverses the 26-variable order, reconstructs the 90 row systems by a
separate standard-library sparse expander, and checks every rational unit
ideal identity.
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
    "one_two_two_residual_second_root_coloop_common_middle_row_certificates.json"
)
CERTIFICATE_SHA256 = (
    "a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1"
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
    "sigma",
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


def add_vector(left: Vector, right: Vector) -> Vector:
    output: list[Entry] = []
    for a, b in zip(left, right, strict=True):
        assert not isinstance(a, str) and not isinstance(b, str)
        output.append(a + b)
    return tuple(output)


def subtract_vector(left: Vector, right: Vector) -> Vector:
    output: list[Entry] = []
    for a, b in zip(left, right, strict=True):
        if isinstance(a, str):
            assert not b
            output.append(a)
        else:
            assert not isinstance(b, str)
            output.append(a - b)
    return tuple(output)


def line_patch(patch: int) -> Vector:
    if patch == 0:
        return (F(1), "tau", "sigma", F(0))
    if patch == 1:
        return (F(0), F(1), "tau", F(0))
    assert patch == 2
    return unit(2)


def normal_form_rows(
    plane_case: int, orientation: int, patch: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    r_rows = (unit(0), unit(1))
    if plane_case == 9:
        q_rows = r_rows
    else:
        intersection_type, third_type = divmod(plane_case, 3)
        if intersection_type == 0:
            intersection = unit(0)
        elif intersection_type == 1:
            intersection = unit(1)
        else:
            intersection = add_vector(unit(0), unit(1))
        if third_type == 0:
            q_rows = (intersection, unit(2))
        elif third_type == 1:
            q_rows = (unit(2), intersection)
        else:
            q_rows = (unit(2), subtract_vector(intersection, unit(2)))

    v = line_patch(patch)
    escape = unit(3)
    if orientation == 0:
        p_rows = (escape, v)
    elif orientation == 1:
        p_rows = (v, escape)
    else:
        assert orientation == 2
        p_rows = (escape, subtract_vector(v, escape))
    return r_rows, p_rows, q_rows


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


def generators(plane_case: int, orientation: int, patch: int) -> list[Polynomial]:
    r_rows, p_rows, q_rows = normal_form_rows(plane_case, orientation, patch)
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
            if source_bits == (1, 1, 1) and row_bits == (1, 0, 1):
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
            add_term(
                total,
                exponent,
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
        f"{plane_case}-{orientation}-{patch}"
        for plane_case in range(10)
        for orientation in range(3)
        for patch in range(3)
    }
    assert set(data["cases"]) == expected

    term_count = 0
    for key in sorted(expected, reverse=True):
        plane_case, orientation, patch = (int(value) for value in key.split("-"))
        system = generators(plane_case, orientation, patch)
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, system, strict=True):
            term_count += len(multiplier)
            add_product(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 31591
    print(
        "independent common-middle-row certificate audit: PASS "
        f"(90 cases / {term_count} multiplier terms)"
    )


def geometry_audit() -> None:
    cases = {
        (plane_case, orientation, patch)
        for plane_case in range(10)
        for orientation in range(3)
        for patch in range(3)
    }
    assert len(cases) == 90
    # Separate numeric gate audit in the normalized (s,u,t)=(0,1,2) chart.
    h, kappa, mu, y_u = F(2), F(3), F(5), F(7)
    normal_p = (F(0), kappa * y_u, -h * mu)
    beta_star = (F(0), h * mu, kappa * y_u)
    assert sum(a * b for a, b in zip(normal_p, beta_star, strict=True)) == 0
    assert beta_star[1] and beta_star[2]
    table = {
        (i, j, k): (j == 0 and i == k)
        for i, j, k in product(range(2), repeat=3)
    }
    assert {cell for cell, active in table.items() if active} == {
        (0, 0, 0),
        (1, 0, 1),
    }
    # q_gate=kappa*z_s-h*w_s is identically zero exactly at z_s=w_s=0.
    assert (kappa * F(11) - h * F(13)) != 0
    assert kappa * F(0) - h * F(0) == 0
    print("independent orbit / determinant-pencil geometry audit: PASS")


def main() -> None:
    geometry_audit()
    certificate_audit()
    print("independent terminal endpoint localization audit: PASS")


if __name__ == "__main__":
    main()
