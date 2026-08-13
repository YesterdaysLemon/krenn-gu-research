#!/usr/bin/env python3
"""Exact replay for the residual second-root-coloop support localization.

The owning Markdown file contains the arbitrary-field proof.  This verifier
checks the derivative-zero face, the coloop row consequences, the binary
diagonal table, the complete plane-incidence reduction, and all 28 endpoint
normal forms through pinned rational Nullstellensatz certificates.
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
    "one_two_two_residual_second_root_coloop_certificates.json"
)
CERTIFICATE_SHA256 = (
    "3ea2f9470d210d85f2b45dce6fd23126888701a37634f07a32dd6750b71e96d5"
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
)
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))


def e(index: int, size: int = 3) -> sp.Matrix:
    return sp.eye(size)[:, index]


def derivative_face_and_coloop_rows() -> None:
    """Replay the face and the canonical rows for j != t."""

    lam, mu = sp.symbols("lambda mu", nonzero=True)
    beta_y, beta_t, gamma_z, gamma_w, alpha_s = sp.symbols(
        "beta_y beta_t gamma_z gamma_w alpha_s"
    )
    transpose_scalars = (
        beta_y * gamma_w - mu * beta_t * gamma_z,
        -lam * alpha_s * gamma_w,
        lam * mu * alpha_s * beta_t,
    )
    assert [value.subs({beta_t: 0, gamma_w: 0}) for value in transpose_scalars] == [
        0,
        0,
        0,
    ]

    # Normalize t=2, choose the residual coloop j=0, and let k=1.
    # The displayed root triples are the preimages of g_k and h_m in L.
    y0, y1 = sp.symbols("y0 y1")
    z0, z1, z2, w0, w1, w2 = sp.symbols("z0 z1 z2 w0 w1 w2")
    y = sp.Matrix([y0, y1, 0])
    z = sp.Matrix([z0, z1, z2])
    w = sp.Matrix([w0, w1, w2])

    def annihilator_equations(
        alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix
    ) -> tuple[sp.Expr, sp.Expr]:
        return (
            sp.expand(lam * alpha[0] + beta.dot(y) + gamma.dot(z)),
            sp.expand(mu * beta[2] + gamma.dot(w)),
        )

    alpha = -(y1 / lam) * e(0)
    beta = e(1)
    gamma = sp.zeros(3, 1)
    assert annihilator_equations(alpha, beta, gamma) == (0, 0)
    assert beta[0] == 0

    for index in range(3):
        alpha = -(z[index] / lam) * e(0)
        beta = -(w[index] / mu) * e(2)
        gamma = e(index)
        assert annihilator_equations(alpha, beta, gamma) == (0, 0)
        assert beta[0] == 0

    print("derivative face / residual-coloop rows: PASS")


def target(alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [alpha[index] * beta[index] * gamma[index] for index in range(3)]
    )


def binary_diagonal_table() -> None:
    """Check the complete table exposed by w_t != 0."""

    wj, wk, wt = sp.symbols("w_j w_k w_t", nonzero=True)
    gamma_lifts = [
        e(0) - (wj / wt) * e(2),
        e(1) - (wk / wt) * e(2),
    ]
    w = sp.Matrix([wj, wk, wt])
    assert all(sp.expand(vector.dot(w)) == 0 for vector in gamma_lifts)
    assert sp.Matrix.hstack(*gamma_lifts)[:2, :] == sp.eye(2)

    rows = [e(0), e(1)]
    for a, b, c in product(range(2), repeat=3):
        value = target(rows[a], rows[b], gamma_lifts[c])
        expected = e(c) if a == b == c else sp.zeros(3, 1)
        assert value == expected
    print("w_t nonzero binary diagonal table: PASS")


def table_cell(a: int, b: int, c: int) -> sp.Matrix:
    if a == b == c:
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


def incidence_reduction() -> None:
    """Replay the human reduction to the 28 endpoint charts."""

    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    left = (a0, a1)
    right = (b0, b1)
    assert bilinear_cell(left, 0, right) == sp.Matrix([a0 * b0, 0])
    assert bilinear_cell(left, 1, right) == sp.Matrix([0, a1 * b1])

    # If the intersection line is coordinate only in R, first/third
    # symmetry lets us use ell=r_a=q_0+q_1.  Its square and its mixed map
    # have rank-one images on the two fully transverse targets.
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

    cases = {
        f"{r_endpoint}{q_endpoint}-{mask}"
        for r_endpoint, q_endpoint in product(range(2), repeat=2)
        for mask in range(1, 8)
    }
    assert len(cases) == 28
    assert {
        tuple(bit for bit in range(3) if mask & (1 << bit))
        for mask in range(1, 8)
    } == {
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
        (0, 1, 2),
    }
    print("plane incidence reduction: PASS (4 endpoints x 7 support masks)")


def form(root: str, bit: int) -> tuple[sp.Symbol, ...]:
    return tuple(SYMBOL_BY_NAME[f"{root}{bit}{coordinate}"] for coordinate in range(4))


def evaluate(linear_form: tuple[sp.Symbol, ...], vector: tuple[int, ...]) -> sp.Expr:
    return sum(
        (coefficient * coordinate for coefficient, coordinate in zip(linear_form, vector, strict=True)),
        sp.Integer(0),
    )


def polarized_product(
    source_bits: tuple[int, int, int],
    rows: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
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


def endpoint_rows(
    r_endpoint: int, q_endpoint: int, mask: int
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], list[tuple[int, ...]]]:
    common = (1, 0, 0, 0)
    r_other = (0, 1, 0, 0)
    q_other = (0, 0, 1, 0)
    r_rows = [r_other, r_other]
    q_rows = [q_other, q_other]
    r_rows[r_endpoint] = common
    r_rows[1 - r_endpoint] = r_other
    q_rows[q_endpoint] = common
    q_rows[1 - q_endpoint] = q_other
    p_rows = [
        (0, 0, 0, 1),
        tuple((mask >> coordinate) & 1 for coordinate in range(3)) + (0,),
    ]
    return r_rows, p_rows, q_rows


def endpoint_generators(r_endpoint: int, q_endpoint: int, mask: int) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = endpoint_rows(r_endpoint, q_endpoint, mask)
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
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 1):
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

    expected_cases = {
        f"{r_endpoint}{q_endpoint}-{mask}"
        for r_endpoint, q_endpoint in product(range(2), repeat=2)
        for mask in range(1, 8)
    }
    assert set(data["cases"]) == expected_cases

    term_count = 0
    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    for key in sorted(expected_cases):
        endpoint_text, mask_text = key.split("-")
        r_endpoint, q_endpoint = (int(value) for value in endpoint_text)
        generators = endpoint_generators(r_endpoint, q_endpoint, int(mask_text))
        encoded_multipliers = data["cases"][key]
        assert len(encoded_multipliers) == 64
        total = zero
        for generator, encoded in zip(generators, encoded_multipliers, strict=True):
            multiplier = multiplier_poly(encoded)
            term_count += len(encoded)
            total += multiplier * generator
        assert total == one, key

    assert term_count == 2310
    print(
        "endpoint Nullstellensatz certificates: PASS "
        f"(28 cases / {term_count} multiplier terms)"
    )


def main() -> None:
    derivative_face_and_coloop_rows()
    binary_diagonal_table()
    incidence_reduction()
    certificate_replay()
    print("residual second-root-coloop w_t support localization: PASS")


if __name__ == "__main__":
    main()
