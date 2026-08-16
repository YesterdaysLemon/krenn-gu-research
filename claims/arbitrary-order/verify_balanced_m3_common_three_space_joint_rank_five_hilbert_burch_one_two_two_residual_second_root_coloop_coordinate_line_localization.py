#!/usr/bin/env python3
"""Exact replay for residual second-root-coloop coordinate-line localization.

The owning Markdown file contains the arbitrary-field argument.  This script
checks the complete same-third-row table, the plane-incidence reduction, the
21 normal-form families, and their rational Nullstellensatz certificates.
"""

from __future__ import annotations

import hashlib
import json
from itertools import permutations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_same_third_row_certificates.json"
)
CERTIFICATE_SHA256 = (
    "e822cb443173acbab3604d6e3e28afaf7fd99a3e306731e21c7c7bc5023ac5fc"
)
VARIABLES = (
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
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))
TAU = SYMBOL_BY_NAME["tau"]


def e(index: int, size: int = 3) -> sp.Matrix:
    return sp.eye(size)[:, index]


def target(alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [alpha[index] * beta[index] * gamma[index] for index in range(3)]
    )


def same_third_row_face() -> None:
    """Replay the table for w_t=0 and w_j w_k nonzero."""

    wj, wk = sp.symbols("w_j w_k", nonzero=True)
    w = sp.Matrix([wj, wk, 0])
    annihilator_rows = [sp.Matrix([wk, -wj, 0]), e(2)]
    assert all(sp.expand(row.dot(w)) == 0 for row in annihilator_rows)

    root_rows = [e(0), e(1)]
    for a, b, c in product(range(2), repeat=3):
        value = target(root_rows[a], root_rows[b], annihilator_rows[c])
        expected = sp.zeros(3, 1)
        if a == b == 0 and c == 0:
            expected = wk * e(0)
        if a == b == 1 and c == 0:
            expected = -wj * e(1)
        assert value == expected
    print("w_t=0 complementary-support same-third-row table: PASS")


def table_cell(a: int, b: int, c: int) -> sp.Matrix:
    if c == 0 and a == b:
        return e(a, 2)
    return sp.zeros(2, 1)


def bilinear_cell(
    left: tuple[sp.Expr, sp.Expr],
    middle: int,
    right: tuple[sp.Expr, sp.Expr],
) -> sp.Matrix:
    return sum(
        (
            left[a] * right[c] * table_cell(a, middle, c)
            for a, c in product(range(2), repeat=2)
        ),
        sp.zeros(2, 1),
    )


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


def incidence_reduction() -> None:
    """Replay the reduction to q_1=R intersect Q and 21 families."""

    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    left = (a0, a1)
    right = (b0, b1)
    assert bilinear_cell(left, 0, right) == sp.Matrix([a0 * b0, 0])
    assert bilinear_cell(left, 1, right) == sp.Matrix([0, a1 * b0])

    # If the intersection is coordinate in R while retaining a q0
    # component, its square and its mixed map have transverse rank-one
    # images.  S2AL mixed-factor sharing excludes both endpoint choices.
    q_generic = (sp.Integer(1), sp.Integer(1))
    for endpoint in range(2):
        r_endpoint = tuple(sp.Integer(i == endpoint) for i in range(2))
        r_other = tuple(sp.Integer(i != endpoint) for i in range(2))
        square = [
            bilinear_cell(r_endpoint, middle, q_generic)
            for middle in range(2)
        ]
        mixed = [
            bilinear_cell(r_other, middle, q_generic)
            for middle in range(2)
        ]
        assert square[endpoint] == e(endpoint, 2)
        assert square[1 - endpoint] == sp.zeros(2, 1)
        assert mixed[endpoint] == sp.zeros(2, 1)
        assert mixed[1 - endpoint] == e(1 - endpoint, 2)

    cases = expected_case_keys()
    assert len(cases) == 21
    assert len([key for key in cases if key.startswith("endpoint-")]) == 14
    assert len([key for key in cases if key.startswith("generic-fixed-")]) == 5
    assert len(
        [key for key in cases if key.startswith("generic-parameter-")]
    ) == 2
    print("plane incidence / support-orbit reduction: PASS (21 families)")


def form(root: str, bit: int) -> tuple[sp.Symbol, ...]:
    return tuple(SYMBOL_BY_NAME[f"{root}{bit}{coordinate}"] for coordinate in range(4))


def evaluate(
    linear_form: tuple[sp.Symbol, ...], vector: tuple[sp.Expr, ...]
) -> sp.Expr:
    return sum(
        (
            coefficient * coordinate
            for coefficient, coordinate in zip(linear_form, vector, strict=True)
        ),
        sp.Integer(0),
    )


def polarized_product(
    source_bits: tuple[int, int, int],
    rows: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
) -> sp.Expr:
    forms = (
        form("x", source_bits[0]),
        form("y", source_bits[1]),
        form("z", source_bits[2]),
    )
    return sp.expand(
        sum(
            (
                evaluate(forms[0], ordered_rows[0])
                * evaluate(forms[1], ordered_rows[1])
                * evaluate(forms[2], ordered_rows[2])
                for ordered_rows in permutations(rows)
            ),
            sp.Integer(0),
        )
    )


def mask_row(support_mask: int) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.Integer((support_mask >> coordinate) & 1) for coordinate in range(3)
    ) + (sp.Integer(0),)


def case_rows(
    key: str,
) -> tuple[
    list[tuple[sp.Expr, ...]],
    list[tuple[sp.Expr, ...]],
    list[tuple[sp.Expr, ...]],
]:
    zero = sp.Integer(0)
    one = sp.Integer(1)
    r_rows = [(one, zero, zero, zero), (zero, one, zero, zero)]
    p_zero = (zero, zero, zero, one)
    q_zero = (zero, zero, one, zero)

    fields = key.split("-")
    if fields[0] == "endpoint":
        endpoint = int(fields[1])
        support_mask = int(fields[2])
        q_one = r_rows[endpoint]
        p_one = mask_row(support_mask)
    elif fields[:2] == ["generic", "fixed"]:
        support_mask = int(fields[2])
        q_one = (one, one, zero, zero)
        p_one = mask_row(support_mask)
    elif fields[:2] == ["generic", "parameter"]:
        support_mask = int(fields[2])
        assert support_mask in (3, 7)
        q_one = (one, one, zero, zero)
        p_one = (one, TAU, sp.Integer(support_mask == 7), zero)
    else:
        raise AssertionError(key)
    return r_rows, [p_zero, p_one], [q_zero, q_one]


def case_generators(key: str) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = case_rows(key)
    generators = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            rows = (
                r_rows[row_bits[0]],
                p_rows[row_bits[1]],
                q_rows[row_bits[2]],
            )
            value = polarized_product(source_bits, rows)
            if source_bits == (0, 0, 0) and row_bits == (0, 0, 0):
                value -= 1
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 0):
                value -= 1
            generators.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
    assert len(generators) == 64
    return generators


def multiplier_poly(encoded: list[list[object]]) -> sp.Poly:
    terms: dict[tuple[int, ...], sp.Rational] = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        coefficient = sp.Rational(str(raw_coefficient))
        assert coefficient
        exponent = [0] * len(VARIABLES)
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:  # type: ignore[misc]
            index = int(raw_index)
            power = int(raw_power)
            assert previous < index < len(VARIABLES)
            assert power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        assert key not in terms
        terms[key] = coefficient
    return sp.Poly.from_dict(terms, *SYMBOLS, domain=sp.QQ)


def certificate_replay() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-v1"
    assert tuple(data["variable_order"]) == VARIABLES
    assert data["generator_order"] == "source_bits_then_row_bits_lexicographic"

    expected = expected_case_keys()
    assert set(data["cases"]) == expected
    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for key in sorted(expected):
        generators = case_generators(key)
        encoded_multipliers = data["cases"][key]
        assert len(encoded_multipliers) == 64
        total = zero
        for generator, encoded in zip(generators, encoded_multipliers, strict=True):
            multiplier = multiplier_poly(encoded)
            term_count += len(encoded)
            total += multiplier * generator
        assert total == one, key

    assert term_count == 9256
    print(
        "same-third-row Nullstellensatz certificates: PASS "
        f"(21 families / {term_count} multiplier terms)"
    )


def main() -> None:
    same_third_row_face()
    incidence_reduction()
    certificate_replay()
    print("residual second-root-coloop coordinate-line localization: PASS")


if __name__ == "__main__":
    main()
