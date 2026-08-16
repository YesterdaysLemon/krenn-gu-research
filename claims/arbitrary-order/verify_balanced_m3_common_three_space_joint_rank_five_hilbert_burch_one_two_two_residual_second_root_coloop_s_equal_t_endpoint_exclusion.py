#!/usr/bin/env python3
"""Exact replay for residual-coloop ``s=t`` endpoint exclusion.

The owning theorem contains the arbitrary-field proof.  This verifier checks
the endpoint pencil table, the generalized same-third-row incidence cover,
and all 21 pinned rational Nullstellensatz identities.
"""

from __future__ import annotations

import hashlib
import json
from itertools import permutations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_"
    "residual_second_root_coloop_s_equal_t_endpoint_certificates.json"
)
CERTIFICATE_SHA256 = (
    "ceb0c69b151523c43219d294806d50a1e1b2905bc7237c6a3709451fc868b9a0"
)
VARIABLES = (
    "x10", "x11", "x12", "x13",
    "y10", "y11", "y12", "y13",
    "z10", "z11", "z12", "z13",
    "x00", "x01", "x02", "x03",
    "y00", "y01", "y02", "y03",
    "z00", "z01", "z02", "z03",
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


def endpoint_pencil_face() -> None:
    """Replay one generic s=t pencil member for either endpoint."""

    mu, h, kappa = sp.symbols("mu h kappa", nonzero=True)
    y0, y1 = sp.symbols("y0 y1")
    y = sp.Matrix([y0, y1, 0])
    normal_p = kappa * y - h * mu * e(2)
    for endpoint in range(2):
        other = 1 - endpoint
        z_endpoint, z_other = sp.symbols("z_endpoint z_other", nonzero=True)
        w = e(endpoint)
        z = z_endpoint * e(endpoint) + z_other * e(other)
        assert z[2] == w[2] == 0
        assert sp.Matrix.hstack(z, w).rank() == 2

        normal_q = kappa * z - h * w
        assert normal_q[2] == 0
        gamma_active = sp.Matrix([normal_q[1], -normal_q[0], 0])
        assert sp.expand(gamma_active.dot(normal_q)) == 0
        assert e(2).dot(normal_q) == 0

        # The first projective gate is -h*mu because s=t and y_t=0.
        assert normal_p[2] == -h * mu
        beta_lifts = [
            e(a) + (kappa * y[a] / (h * mu)) * e(2) for a in range(2)
        ]
        assert all(sp.expand(beta.dot(normal_p)) == 0 for beta in beta_lifts)
        assert sp.Matrix.hstack(*beta_lifts)[:2, :] == sp.eye(2)
        root_rows = [e(0), e(1)]
        third_rows = [gamma_active, e(2)]
        for a, b, c in product(range(2), repeat=3):
            value = target(root_rows[a], beta_lifts[b], third_rows[c])
            expected = sp.zeros(3, 1)
            if a == b and c == 0:
                expected = gamma_active[a] * e(a)
            assert value == expected
    print("s=t endpoint determinant-pencil table: PASS")


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
        f"endpoint-{endpoint}-{mask}"
        for endpoint in range(2)
        for mask in range(1, 8)
    }
    cases.update(f"generic-fixed-{mask}" for mask in (1, 2, 4, 5, 6))
    cases.update(f"generic-parameter-{mask}" for mask in (3, 7))
    return cases


def generalized_incidence_cover() -> None:
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    assert bilinear_cell((a0, a1), 0, (b0, b1)) == sp.Matrix([a0 * b0, 0])
    assert bilinear_cell((a0, a1), 1, (b0, b1)) == sp.Matrix([0, a1 * b0])

    # The R-Q intersection reduction is independent of the positions of the
    # two P rows.  The generic P-intersection line is P0+P1.
    generic_q = (sp.Integer(1), sp.Integer(1))
    for endpoint in range(2):
        r_endpoint = tuple(sp.Integer(i == endpoint) for i in range(2))
        r_other = tuple(sp.Integer(i != endpoint) for i in range(2))
        square = [bilinear_cell(r_endpoint, m, generic_q) for m in range(2)]
        mixed = [bilinear_cell(r_other, m, generic_q) for m in range(2)]
        assert square[endpoint] == e(endpoint, 2)
        assert square[1 - endpoint] == sp.zeros(2, 1)
        assert mixed[endpoint] == sp.zeros(2, 1)
        assert mixed[1 - endpoint] == e(1 - endpoint, 2)

    cases = expected_case_keys()
    assert len(cases) == 21
    assert len([key for key in cases if key.startswith("endpoint-")]) == 14
    assert len([key for key in cases if key.startswith("generic-fixed-")]) == 5
    assert len([key for key in cases if key.startswith("generic-parameter-")]) == 2
    print("generalized same-third-row orbit cover: PASS (21 families)")


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
                evaluate(forms[0], ordered[0])
                * evaluate(forms[1], ordered[1])
                * evaluate(forms[2], ordered[2])
                for ordered in permutations(rows)
            ),
            sp.Integer(0),
        )
    )


def mask_row(mask: int) -> tuple[sp.Expr, ...]:
    return tuple(sp.Integer((mask >> coordinate) & 1) for coordinate in range(3))


def case_rows(
    key: str,
) -> tuple[
    list[tuple[sp.Expr, ...]],
    list[tuple[sp.Expr, ...]],
    list[tuple[sp.Expr, ...]],
]:
    zero, one = sp.Integer(0), sp.Integer(1)
    r_rows = [(one, zero, zero, zero), (zero, one, zero, zero)]
    p_zero = (zero, zero, zero, one)
    q_zero = (zero, zero, one, zero)
    fields = key.split("-")
    if fields[0] == "endpoint":
        endpoint, mask = int(fields[1]), int(fields[2])
        q_one = r_rows[endpoint]
        intersection = mask_row(mask)
    elif fields[:2] == ["generic", "fixed"]:
        mask = int(fields[2])
        q_one = (one, one, zero, zero)
        intersection = mask_row(mask)
    elif fields[:2] == ["generic", "parameter"]:
        mask = int(fields[2])
        assert mask in (3, 7)
        q_one = (one, one, zero, zero)
        intersection = (one, TAU, sp.Integer(mask == 7))
    else:
        raise AssertionError(key)
    p_one = intersection + (sp.Integer(-1),)
    assert tuple(p_zero[i] + p_one[i] for i in range(4)) == intersection + (zero,)
    return r_rows, [p_zero, p_one], [q_zero, q_one]


def case_generators(key: str) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = case_rows(key)
    output = []
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
            output.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
    assert len(output) == 64
    return output


def multiplier_poly(encoded: list[list[object]]) -> sp.Poly:
    terms: dict[tuple[int, ...], sp.Rational] = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        coefficient = sp.Rational(str(raw_coefficient))
        exponent = [0] * len(VARIABLES)
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:  # type: ignore[misc]
            index, power = int(raw_index), int(raw_power)
            assert previous < index < len(VARIABLES) and power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        assert coefficient and key not in terms
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
        multipliers = data["cases"][key]
        assert len(generators) == len(multipliers) == 64
        total = zero
        for generator, encoded in zip(generators, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, key
    assert term_count == 44806
    print(
        "s=t endpoint Nullstellensatz certificates: PASS "
        f"(21 families / {term_count} multiplier terms)"
    )


def main() -> None:
    endpoint_pencil_face()
    generalized_incidence_cover()
    certificate_replay()
    print("residual second-root-coloop s=t endpoint exclusion: PASS")


if __name__ == "__main__":
    main()
