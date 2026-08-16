#!/usr/bin/env python3
"""Independent exact audit of the diagonal two-supported endpoint exclusion.

This script imports neither the primary verifier nor a third-party package.
It reverses the certificate variable order and reconstructs the target face,
tangent identity, normalized charts, permanents, and certificate products with
standard-library ``Fraction`` sparse polynomials.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_"
    "fully_injective_diagonal_monomial_residual_two_supported_endpoint_"
    "certificates.json"
)
CERTIFICATE_SHA256 = (
    "e9414389e653a76770d8f105a086fcae6887d2dbe012f41e5d74f78686c72f52"
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
    "g",
    "h",
)
AUDIT_VARIABLES = tuple(reversed(CERTIFICATE_VARIABLES))
AUDIT_INDEX = {name: index for index, name in enumerate(AUDIT_VARIABLES)}
ZERO_EXPONENT = (0,) * len(AUDIT_VARIABLES)

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, F]
Row = tuple[Polynomial, Polynomial, Polynomial, Polynomial]


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


def scale(value: int | F, polynomial: Polynomial) -> Polynomial:
    coefficient = F(value)
    return {
        exponent: coefficient * entry
        for exponent, entry in polynomial.items()
        if coefficient * entry
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


def square(polynomial: Polynomial) -> Polynomial:
    return multiply(polynomial, polynomial)


def row_from_scalars(values: tuple[int, int, int, int]) -> Row:
    return tuple(constant(value) for value in values)  # type: ignore[return-value]


ZERO = row_from_scalars((0, 0, 0, 0))
Q0 = row_from_scalars((0, 0, 1, 0))
Q1 = row_from_scalars((0, 0, 0, 1))


def hyperdeterminant(a: dict[tuple[int, int, int], Polynomial]) -> Polynomial:
    positive_squares = add(
        multiply(square(a[0, 0, 0]), square(a[1, 1, 1])),
        multiply(square(a[0, 0, 1]), square(a[1, 1, 0])),
        multiply(square(a[0, 1, 0]), square(a[1, 0, 1])),
        multiply(square(a[1, 0, 0]), square(a[0, 1, 1])),
    )
    negative_pairs = add(
        multiply(multiply(a[0, 0, 0], a[0, 0, 1]), multiply(a[1, 1, 0], a[1, 1, 1])),
        multiply(multiply(a[0, 0, 0], a[0, 1, 0]), multiply(a[1, 0, 1], a[1, 1, 1])),
        multiply(multiply(a[0, 0, 0], a[1, 0, 0]), multiply(a[0, 1, 1], a[1, 1, 1])),
        multiply(multiply(a[0, 0, 1], a[0, 1, 0]), multiply(a[1, 0, 1], a[1, 1, 0])),
        multiply(multiply(a[0, 0, 1], a[1, 0, 0]), multiply(a[0, 1, 1], a[1, 1, 0])),
        multiply(multiply(a[0, 1, 0], a[1, 0, 0]), multiply(a[0, 1, 1], a[1, 0, 1])),
    )
    positive_pairs = add(
        multiply(multiply(a[0, 0, 0], a[0, 1, 1]), multiply(a[1, 0, 1], a[1, 1, 0])),
        multiply(multiply(a[0, 0, 1], a[0, 1, 0]), multiply(a[1, 0, 0], a[1, 1, 1])),
    )
    return add(positive_squares, scale(-2, negative_pairs), scale(4, positive_pairs))


def face_and_incidence_audit() -> None:
    w = (F(2), F(3), F(0))
    gamma_rows = ((F(3), F(-2), F(0)), (F(0), F(0), F(1)))
    assert all(sum((a * b for a, b in zip(row, w, strict=True)), F(0)) == 0 for row in gamma_rows)
    roots = ((F(1), F(0), F(0)), (F(0), F(1), F(0)))
    for i, j, k in product(range(2), repeat=3):
        value = tuple(
            roots[i][index] * roots[j][index] * gamma_rows[k][index]
            for index in range(3)
        )
        expected = (F(0), F(0), F(0))
        if (i, j, k) == (0, 0, 0):
            expected = (F(3), F(0), F(0))
        if (i, j, k) == (1, 1, 0):
            expected = (F(0), F(-2), F(0))
        assert value == expected

    zero = {}
    secant = {bits: zero for bits in product(range(2), repeat=3)}
    secant[0, 0, 0] = variable("g")
    secant[1, 1, 1] = variable("h")
    assert hyperdeterminant(secant) == multiply(square(variable("g")), square(variable("h")))

    xl = (variable("x00"), variable("x01"))
    yl = (variable("y00"), variable("y01"))
    zl = (variable("z00"), variable("z01"))
    xq = (variable("x10"), variable("x11"))
    yq = (variable("y10"), variable("y11"))
    zq = (variable("z10"), variable("z11"))
    tangent = {
        (i, j, k): add(
            multiply(multiply(xq[i], yl[j]), zl[k]),
            multiply(multiply(xl[i], yq[j]), zl[k]),
            multiply(multiply(xl[i], yl[j]), zq[k]),
        )
        for i, j, k in product(range(2), repeat=3)
    }
    assert hyperdeterminant(tangent) == {}

    survivors = set()
    for left_mask in range(1, 4):
        for middle_mask in range(1, 4):
            common = left_mask & middle_mask
            if common == 3:
                continue
            if common in (1, 2) and (left_mask == 3 or middle_mask == 3):
                continue
            survivors.add((left_mask, middle_mask))
    assert survivors == {(1, 1), (1, 2), (2, 1), (2, 2)}
    specs = case_specifications()
    assert len(specs) == 29
    assert sum(spec[3] for spec in specs.values()) == 16
    print("independent face / tangent / orbit audit: PASS (29 charts)")


def add_rows(left: Row, right: Row) -> Row:
    return tuple(add(a, b) for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def projection_rows(kind: str, l0: Row, l1: Row) -> tuple[Row, Row]:
    if kind == "diag":
        return add_rows(row_from_scalars((1, 0, 0, 0)), l0), add_rows(
            row_from_scalars((0, 1, 0, 0)), l1
        )
    if kind == "cross":
        return add_rows(row_from_scalars((0, 1, 0, 0)), l0), add_rows(
            row_from_scalars((1, 0, 0, 0)), l1
        )
    tail = (constant(1), constant(1), variable("g"), variable("h"))
    if kind == "diag_shear":
        return add_rows(row_from_scalars((1, 0, 0, 0)), l0), tail
    if kind == "cross_shear":
        return add_rows(row_from_scalars((0, 1, 0, 0)), l0), tail
    raise AssertionError(kind)


def case_specifications() -> dict[
    str, tuple[tuple[Row, Row], tuple[Row, Row], tuple[Row, Row], bool, Row, Row]
]:
    r = (row_from_scalars((1, 0, 0, 0)), row_from_scalars((0, 1, 0, 0)))
    q = (Q0, Q1)
    tau_q0 = (constant(0), constant(0), variable("tau"), constant(0))
    tau_q1 = (constant(0), constant(0), constant(0), variable("tau"))
    affine = row_from_scalars((0, 0, 1, 1))
    specs = {}
    fixed = {
        "zero_zero": (ZERO, ZERO),
        "zero_q1": (ZERO, Q1),
        "zero_q0": (ZERO, Q0),
        "prop_q0": (Q0, tau_q0),
    }
    for kind in ("diag", "cross"):
        for orbit, (l0, l1) in fixed.items():
            specs[f"{kind}_{orbit}"] = (
                r,
                projection_rows(kind, l0, l1),
                q,
                False,
                ZERO,
                ZERO,
            )
    specs["diag_ind_q1_q0"] = (
        r,
        projection_rows("diag", Q1, Q0),
        q,
        False,
        ZERO,
        ZERO,
    )
    for kind in ("diag", "cross"):
        specs[f"{kind}_prop_q1"] = (
            r,
            projection_rows(kind, Q1, tau_q1),
            q,
            True,
            Q1,
            Q1,
        )
    independent = {"ind_q1_q0": (Q1, Q0), "ind_affine": (Q0, affine)}
    for kind, orbit in (
        ("diag", "ind_affine"),
        ("cross", "ind_q1_q0"),
        ("cross", "ind_affine"),
    ):
        l0, l1 = independent[orbit]
        for u_index, v_index in product(range(2), repeat=2):
            specs[f"{kind}_{orbit}_u{u_index}_v{v_index}"] = (
                r,
                projection_rows(kind, l0, l1),
                q,
                True,
                (l0, l1)[u_index],
                (l0, l1)[v_index],
            )
    for kind in ("diag_shear", "cross_shear"):
        for orbit, l0 in (("zero", ZERO), ("q0", Q0)):
            specs[f"{kind}_{orbit}"] = (
                r,
                projection_rows(kind, l0, ZERO),
                q,
                False,
                ZERO,
                ZERO,
            )
        specs[f"{kind}_q1"] = (
            r,
            projection_rows(kind, Q1, ZERO),
            q,
            True,
            Q1,
            Q1,
        )
    return specs


def evaluate_form(root: str, bit: int, row: Row) -> Polynomial:
    return add(
        *(
            multiply(variable(f"{root}{bit}{coordinate}"), row[coordinate])
            for coordinate in range(4)
        )
    )


def permanent_polynomial(source_bits: tuple[int, int, int], rows: tuple[Row, Row, Row]) -> Polynomial:
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
    r, p, q, physical, u, v = case_specifications()[key]
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            polynomial = permanent_polynomial(
                source_bits,
                (r[row_bits[0]], p[row_bits[1]], q[row_bits[2]]),
            )
            if source_bits == (0, 0, 0) and row_bits == (0, 0, 0):
                add_term(polynomial, ZERO_EXPONENT, F(-1))
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 0):
                add_term(polynomial, ZERO_EXPONENT, F(-1))
            output.append(polynomial)
    if physical:
        for source_bits in product(range(2), repeat=3):
            for i, k in product(range(2), repeat=2):
                output.append(permanent_polynomial(source_bits, (r[i], v, q[k])))
        for source_bits in product(range(2), repeat=3):
            for j, k in product(range(2), repeat=2):
                output.append(permanent_polynomial(source_bits, (u, p[j], q[k])))
    assert len(output) == (128 if physical else 64)
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
        for product_exponent, product_coefficient in multiply(
            {exponent: coefficient}, generator
        ).items():
            add_term(total, product_exponent, product_coefficient)


def certificate_audit() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-v1"
    assert tuple(data["variable_order"]) == CERTIFICATE_VARIABLES
    assert data["generator_order"] == (
        "RPQ_source_bits_then_row_bits; physical_tail_RvQ_then_uPQ_"
        "each_source_bits_then_two_row_bits; all_lexicographic"
    )
    specifications = case_specifications()
    assert set(data["cases"]) == set(specifications)
    assert data["case_kinds"] == {
        key: ("physical_128" if specification[3] else "table_64")
        for key, specification in specifications.items()
    }

    term_count = 0
    for key in sorted(specifications, reverse=True):
        generators = case_generators(key)
        multipliers = data["cases"][key]
        assert len(multipliers) == len(generators)
        total: Polynomial = {}
        for multiplier, generator in zip(multipliers, generators, strict=True):
            term_count += len(multiplier)
            add_multiplier_times_generator(total, multiplier, generator)
        assert total == {ZERO_EXPONENT: F(1)}, key
    assert term_count == 2972
    print(
        "independent sparse endpoint certificates: PASS "
        f"(29 charts / {term_count} multiplier terms)"
    )


def main() -> None:
    face_and_incidence_audit()
    certificate_audit()
    print("independent diagonal monomial two-supported endpoint audit: PASS")


if __name__ == "__main__":
    main()
