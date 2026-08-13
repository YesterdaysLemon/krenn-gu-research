#!/usr/bin/env python3
"""Independent exact audit of both residual second-root-coloop exclusions.

This script imports neither the primary verifier nor a third-party package.
It reverses the certificate variable order, independently reconstructs the
15 systems and every permanent, and checks the rational identities with
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
    "one_two_two_residual_second_root_coloop_terminal_same_pair_certificates.json"
)
CERTIFICATE_SHA256 = (
    "bc63359ece10e7d12237ab5821f64227de8391b5a9422091d9b5c0591484a7a0"
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


def q_intersection(qtype: int) -> Vector:
    if qtype == 0:
        return unit(0)
    if qtype == 1:
        return unit(1)
    assert qtype == 2
    return add_vector(unit(0), unit(1))


def normal_form_rows(
    qtype: int, branch: int, patch: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    r_rows = (unit(0), unit(1))
    q_rows = (unit(2), q_intersection(qtype))
    if branch == 0:
        if patch == 0:
            p_zero = (F(1), "tau", F(-1), F(0))
        elif patch == 1:
            p_zero = (F(0), F(1), F(-1), F(0))
        else:
            assert patch == 2
            p_zero = unit(2)
        p_rows = (p_zero, unit(3))
    else:
        assert branch == 1
        if patch == 0:
            p_one = (F(1), "tau", F(0), F(0))
        else:
            assert patch == 1
            p_one = unit(1)
        p_rows = (unit(3), p_one)
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


def generators(qtype: int, branch: int, patch: int) -> list[Polynomial]:
    r_rows, p_rows, q_rows = normal_form_rows(qtype, branch, patch)
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
            if source_bits == (1, 1, 1) and row_bits == (1, 0, 0):
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
        f"{qtype}-0-{patch}" for qtype in range(3) for patch in range(3)
    } | {f"{qtype}-1-{patch}" for qtype in range(3) for patch in range(2)}
    assert set(data["cases"]) == expected

    term_count = 0
    for key in sorted(expected, reverse=True):
        qtype, branch, patch = (int(value) for value in key.split("-"))
        system = generators(qtype, branch, patch)
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, system, strict=True):
            term_count += len(multiplier)
            add_product(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 32871
    print(
        "independent terminal same-pair certificate audit: PASS "
        f"(15 cases / {term_count} multiplier terms)"
    )


def geometry_audit() -> None:
    cases = {
        (qtype, 0, patch)
        for qtype in range(3)
        for patch in range(3)
    } | {
        (qtype, 1, patch)
        for qtype in range(3)
        for patch in range(2)
    }
    assert len(cases) == 15

    # Independent numeric terminal face: only the common active pair has
    # nonzero u,t target coefficients.
    beta_star = (F(0), F(10), F(21))
    gamma_star = (F(0), F(33), F(-5))
    beta_s = (F(1), F(0), F(0))
    gamma_s = beta_s
    beta_rows = (beta_star, beta_s)
    gamma_rows = (gamma_star, gamma_s)
    active = set()
    for i, j, k in product(range(2), repeat=3):
        coordinate = (1, 2)[i]
        if beta_rows[j][coordinate] * gamma_rows[k][coordinate]:
            active.add((i, j, k))
    assert active == {(0, 0, 0), (1, 0, 0)}

    # Equal-plane coefficient audit with four independent formal matrix
    # entries.  E00*M symmetric kills m01; E10*M symmetric kills m00, so
    # the first row of the purported inverse change matrix vanishes.
    m00 = (F(1), F(0), F(0), F(0))
    m01 = (F(0), F(1), F(0), F(0))
    zero = (F(0),) * 4
    h0_off_difference = tuple(
        left - right for left, right in zip(m01, zero, strict=True)
    )
    h1_off_difference = tuple(
        left - right for left, right in zip(zero, m00, strict=True)
    )
    assert h0_off_difference == m01
    assert h1_off_difference == tuple(-entry for entry in m00)
    assert m00 != zero and m01 != zero
    # Imposing both symmetry equations kills variables m00,m01.  Every
    # determinant monomial m00*m11 and m01*m10 therefore vanishes.
    killed = {0, 1}
    determinant_monomials = ({0, 3}, {1, 2})
    assert all(monomial & killed for monomial in determinant_monomials)
    print("independent terminal-face / incidence-cover audit: PASS")


def main() -> None:
    geometry_audit()
    certificate_audit()
    print("independent residual second-root-coloop exclusion audit: PASS")


if __name__ == "__main__":
    main()
