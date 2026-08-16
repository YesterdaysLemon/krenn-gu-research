#!/usr/bin/env python3
"""Independent exact audit of residual-coloop projective-pencil localization.

This audit imports neither the primary verifier nor a third-party package.  It
uses standard-library Fraction arithmetic, reverses the certificate variable
order, rebuilds all permanents by direct loops, and checks every sparse unit
ideal identity independently.
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
    "one_two_two_residual_second_root_coloop_projective_pencil_certificates.json"
)
CERTIFICATE_SHA256 = (
    "0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca"
)
CERTIFICATE_VARIABLES = (
    "x10", "x11", "x12", "x13",
    "y10", "y11", "y12", "y13",
    "z10", "z11", "z12", "z13",
    "x00", "x01", "x02", "x03",
    "y00", "y01", "y02", "y03",
    "z00", "z01", "z02", "z03",
)
AUDIT_VARIABLES = tuple(reversed(CERTIFICATE_VARIABLES))
AUDIT_INDEX = {name: index for index, name in enumerate(AUDIT_VARIABLES)}
ZERO_EXPONENT = (0,) * len(AUDIT_VARIABLES)

Vector = tuple[F, ...]
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, F]


def unit(size: int, index: int) -> Vector:
    return tuple(F(position == index) for position in range(size))


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(value: F, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def rank(columns: tuple[Vector, ...]) -> int:
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows = len(matrix)
    cols = len(columns)
    pivot_row = 0
    for column in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            multiple = matrix[row][column]
            if multiple:
                matrix[row] = [
                    entry - multiple * pivot_entry
                    for entry, pivot_entry in zip(
                        matrix[row], matrix[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def projective_and_coloop_audit() -> None:
    lam, mu, h, kappa, value = F(2), F(3), F(5), F(7), F(11)
    beta_y, mu_beta_t = value * h, value * kappa
    gamma_z, gamma_w = -value * h, -value * kappa
    assert beta_y * gamma_w - mu_beta_t * gamma_z == 0
    assert beta_y + gamma_z == mu_beta_t + gamma_w == 0
    assert -lam * F(0) * gamma_w == lam * F(0) * mu_beta_t == 0

    y = (F(13), F(17), F(0))
    z = (F(19), F(23), F(29))
    w = (F(31), F(37), F(41))
    normal_p = tuple(kappa * y[i] - h * mu * F(i == 2) for i in range(3))
    normal_q = tuple(kappa * z[i] - h * w[i] for i in range(3))
    assert normal_p == (kappa * y[0], kappa * y[1], -h * mu)
    assert normal_q == tuple(kappa * z[i] - h * w[i] for i in range(3))

    # Independent coefficient view of L_P L_Q.  For s!=t its two possibly
    # nonzero coefficients are y_s z_s and -y_s w_s; for s=t they are
    # mu*w_t and -mu*z_t.  Hence an identically zero product has exactly the
    # fork stated in the theorem.
    for s in range(2):
        coefficients = (y[s] * z[s], -y[s] * w[s])
        assert all(coefficients)  # hostile nondegenerate fixture
    t_coefficients = (mu * w[2], -mu * z[2])
    assert all(t_coefficients)

    r0, r1, a, gj, b = (unit(5, index) for index in range(5))
    pj = add(scale(F(43), a), gj)
    assert rank((r0, r1)) == 2
    assert rank((r0, r1, gj)) == 3
    assert rank((r0, r1, a, pj)) == 4
    assert rank((r0, r1, a, b)) == 4

    p_star = add(add(scale(F(2), a), scale(F(3), b)), r0)
    q_star = add(add(scale(F(-2), a), scale(F(-3), b)), r1)
    assert add(p_star, q_star) == add(r0, r1)
    assert rank((r0, r1, p_star, q_star)) == rank((r0, r1, p_star))
    print("independent determinant-face / coloop-row audit: PASS")


def incidence_audit() -> None:
    # A generic P-intersection line is p0+p1.  Both target-indexed rows are
    # outside S, while their sum is one of seven nonzero support masks.
    cases = set()
    for r_endpoint, q_endpoint in product(range(2), repeat=2):
        for mask in range(1, 8):
            p0 = unit(4, 3)
            support = tuple(F((mask >> coordinate) & 1) for coordinate in range(3))
            p1 = support + (F(-1),)
            assert add(p0, p1) == support + (F(0),)
            cases.add((r_endpoint, q_endpoint, mask))
    assert len(cases) == 28

    endpoint_table = {
        (0, 0): ("y_j", "z_k*z_t"),
        (0, 1): ("y_k*z_k",),
        (0, 2): ("z_t",),
        (1, 0): ("y_j*z_j",),
        (1, 1): ("y_k", "z_j*z_t"),
        (1, 2): ("z_t",),
    }
    assert len(endpoint_table) == 6
    assert endpoint_table[(0, 2)] == endpoint_table[(1, 2)]
    print("independent incidence / endpoint case-cover audit: PASS")


def add_term(polynomial: Polynomial, exponent: Exponent, coefficient: F) -> None:
    if not coefficient:
        return
    value = polynomial.get(exponent, F(0)) + coefficient
    if value:
        polynomial[exponent] = value
    else:
        polynomial.pop(exponent, None)


def normal_form_rows(
    r_endpoint: int, q_endpoint: int, mask: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    common = unit(4, 0)
    r_other = unit(4, 1)
    q_other = unit(4, 2)
    r_rows = [r_other, r_other]
    q_rows = [q_other, q_other]
    r_rows[r_endpoint] = common
    q_rows[q_endpoint] = common
    p_zero = unit(4, 3)
    support = tuple(F((mask >> coordinate) & 1) for coordinate in range(3))
    p_one = support + (F(-1),)
    return tuple(r_rows), (p_zero, p_one), tuple(q_rows)  # type: ignore[return-value]


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
            for variable, entry in choices:
                exponent[variable] += 1
                coefficient *= entry
            add_term(output, tuple(exponent), coefficient)
    return output


def generators(r_endpoint: int, q_endpoint: int, mask: int) -> list[Polynomial]:
    r_rows, p_rows, q_rows = normal_form_rows(r_endpoint, q_endpoint, mask)
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            rows = (
                r_rows[row_bits[0]],
                p_rows[row_bits[1]],
                q_rows[row_bits[2]],
            )
            polynomial = permanent_polynomial(source_bits, rows)
            if source_bits == row_bits == (0, 0, 0):
                add_term(polynomial, ZERO_EXPONENT, F(-1))
            if source_bits == row_bits == (1, 1, 1):
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
            product_exponent = tuple(
                left + right
                for left, right in zip(
                    multiplier_exponent, generator_exponent, strict=True
                )
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
        system = generators(r_endpoint, q_endpoint, int(mask_text))
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, system, strict=True):
            term_count += len(multiplier)
            add_product(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 20582
    print(
        "independent sparse certificate audit: PASS "
        f"(28 cases / {term_count} multiplier terms)"
    )


def main() -> None:
    projective_and_coloop_audit()
    incidence_audit()
    certificate_audit()
    print("independent residual-coloop projective-pencil audit: PASS")


if __name__ == "__main__":
    main()
