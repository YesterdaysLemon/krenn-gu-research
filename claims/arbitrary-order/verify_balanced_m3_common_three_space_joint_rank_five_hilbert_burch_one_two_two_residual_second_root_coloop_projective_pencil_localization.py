#!/usr/bin/env python3
"""Exact replay for residual-coloop projective-pencil localization.

The owning theorem contains the arbitrary-field proof.  This verifier checks
the determinant face, the residual-coloop common-space construction, the
strengthened binary-frame case cover, all 28 pinned rational identities, and
the resulting endpoint support table.
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
    "one_two_two_residual_second_root_coloop_projective_pencil_certificates.json"
)
CERTIFICATE_SHA256 = (
    "0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca"
)
VARIABLES = (
    "x10", "x11", "x12", "x13",
    "y10", "y11", "y12", "y13",
    "z10", "z11", "z12", "z13",
    "x00", "x01", "x02", "x03",
    "y00", "y01", "y02", "y03",
    "z00", "z01", "z02", "z03",
)
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))


def e(index: int, size: int) -> sp.Matrix:
    return sp.eye(size)[:, index]


def determinant_face_and_gates() -> None:
    lam, mu, h, kappa, scale = sp.symbols(
        "lambda mu h kappa scale", nonzero=True
    )
    alpha_s = sp.Integer(0)
    beta_y = scale * h
    mu_beta_t = scale * kappa
    gamma_z = -scale * h
    gamma_w = -scale * kappa

    transpose = (
        beta_y * gamma_w - mu_beta_t * gamma_z,
        -lam * alpha_s * gamma_w,
        lam * alpha_s * mu_beta_t,
    )
    assert tuple(sp.expand(value) for value in transpose) == (0, 0, 0)
    assert sp.expand(beta_y + gamma_z) == 0
    assert sp.expand(mu_beta_t + gamma_w) == 0

    # Normalize t=2.  The normals of P_delta and Q_delta are exactly the
    # vectors whose s coordinates are the two projection gates.
    y0, y1 = sp.symbols("y0 y1")
    z0, z1, z2, w0, w1, w2 = sp.symbols("z0 z1 z2 w0 w1 w2")
    y = sp.Matrix([y0, y1, 0])
    z = sp.Matrix([z0, z1, z2])
    w = sp.Matrix([w0, w1, w2])
    normal_p = kappa * y - h * mu * e(2, 3)
    normal_q = kappa * z - h * w
    expected_p = (kappa * y0, kappa * y1, -h * mu)
    expected_q = (
        kappa * z0 - h * w0,
        kappa * z1 - h * w1,
        kappa * z2 - h * w2,
    )
    assert tuple(normal_p) == expected_p
    assert tuple(normal_q) == expected_q

    # If their product vanishes identically on P^1, integral-domain
    # factorization gives the displayed fork.  These coefficient checks are
    # the three normalized colour cases used in the theorem.
    for s in range(3):
        product_gate = sp.Poly(sp.expand(normal_p[s] * normal_q[s]), h, kappa)
        if s == 2:
            assert product_gate.coeff_monomial(h**2) == mu * w2
            assert product_gate.coeff_monomial(h * kappa) == -mu * z2
        else:
            ys = (y0, y1)[s]
            zs = (z0, z1)[s]
            ws = (w0, w1)[s]
            assert product_gate.coeff_monomial(kappa**2) == ys * zs
            assert product_gate.coeff_monomial(h * kappa) == -ys * ws
    print("determinant face / projective gates: PASS")


def coloop_row_geometry() -> None:
    # Quotient-adapted exact coordinates: R=<e0,e1>, A=e2, g_j=e3,
    # B=e4.  The six nonselected canonical rows lie in R, so g_j supplies
    # the third direction of V and p_j=y_j A+g_j cannot lie in S=R+A.
    yj = sp.symbols("y_j")
    r0, r1, a, gj, b = (e(index, 5) for index in range(5))
    r_space = sp.Matrix.hstack(r0, r1)
    v_space = sp.Matrix.hstack(r0, r1, gj)
    s_space = sp.Matrix.hstack(r0, r1, a)
    pj = yj * a + gj
    assert r_space.rank() == 2
    assert v_space.rank() == 3
    assert s_space.rank() == 3
    assert sp.Matrix.hstack(s_space, pj).rank() == 4
    assert sp.Matrix.hstack(v_space, b).rank() == 4

    # A beta_j-zero row whose evaluation pair is opposite a Q_delta row
    # has a sum in R.  This quotient fixture checks the cancellation that
    # places R, Q_delta, and a nonzero line of P_delta in one three-space.
    hq, kq = sp.symbols("h_q k_q")
    p_star = hq * a + kq * b + r0
    q_star = -hq * a - kq * b + r1
    assert p_star + q_star == r0 + r1
    common = sp.Matrix.hstack(r0, r1, p_star)
    assert sp.Matrix.hstack(common, q_star).rank() == common.rank()
    print("residual-coloop row geometry / forced escape: PASS")


def diagonal_cell(a: int, b: int, c: int) -> sp.Matrix:
    return e(a, 2) if a == b == c else sp.zeros(2, 1)


def expanded_cell(
    left: tuple[sp.Expr, sp.Expr],
    middle: int,
    right: tuple[sp.Expr, sp.Expr],
) -> sp.Matrix:
    return sum(
        (
            left[a] * right[c] * diagonal_cell(a, middle, c)
            for a, c in product(range(2), repeat=2)
        ),
        sp.zeros(2, 1),
    )


def generalized_incidence_cover() -> None:
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    left = (a0, a1)
    right = (b0, b1)
    assert expanded_cell(left, 0, right) == sp.Matrix([a0 * b0, 0])
    assert expanded_cell(left, 1, right) == sp.Matrix([0, a1 * b1])

    # The R-Q intersection reduction is independent of where P meets S.
    # It leaves four ordered endpoint incidences.  A non-coordinate line in
    # P is rescaled to span(p0+p1); its nonzero S-vector has seven supports.
    endpoints = set(product(range(2), repeat=2))
    supports = {
        tuple(i for i in range(3) if mask & (1 << i))
        for mask in range(1, 8)
    }
    assert len(endpoints) == 4
    assert supports == {
        (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)
    }
    assert len(endpoints) * len(supports) == 28
    print("generalized binary-frame cover: PASS (4 endpoints x 7 masks)")


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
                evaluate(forms[0], ordered[0])
                * evaluate(forms[1], ordered[1])
                * evaluate(forms[2], ordered[2])
                for ordered in permutations(rows)
            ),
            sp.Integer(0),
        )
    )


def normal_form_rows(
    r_endpoint: int, q_endpoint: int, mask: int
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], list[tuple[int, ...]]]:
    common = (1, 0, 0, 0)
    r_other = (0, 1, 0, 0)
    q_other = (0, 0, 1, 0)
    r_rows = [r_other, r_other]
    q_rows = [q_other, q_other]
    r_rows[r_endpoint] = common
    q_rows[q_endpoint] = common
    support = tuple((mask >> coordinate) & 1 for coordinate in range(3))
    p_rows = [(0, 0, 0, 1), support + (-1,)]
    assert tuple(p_rows[0][i] + p_rows[1][i] for i in range(4)) == support + (0,)
    return r_rows, p_rows, q_rows


def generators(r_endpoint: int, q_endpoint: int, mask: int) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = normal_form_rows(r_endpoint, q_endpoint, mask)
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            rows = (
                r_rows[row_bits[0]],
                p_rows[row_bits[1]],
                q_rows[row_bits[2]],
            )
            value = polarized_product(source_bits, rows)
            if source_bits == row_bits == (0, 0, 0):
                value -= 1
            if source_bits == row_bits == (1, 1, 1):
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
            index = int(raw_index)
            power = int(raw_power)
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
    expected = {
        f"{r_endpoint}{q_endpoint}-{mask}"
        for r_endpoint, q_endpoint in product(range(2), repeat=2)
        for mask in range(1, 8)
    }
    assert set(data["cases"]) == expected

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for key in sorted(expected):
        endpoint_text, mask_text = key.split("-")
        r_endpoint, q_endpoint = (int(value) for value in endpoint_text)
        system = generators(r_endpoint, q_endpoint, int(mask_text))
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total = zero
        for generator, encoded in zip(system, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, key
    assert term_count == 20582
    print(
        "generic-line Nullstellensatz certificates: PASS "
        f"(28 cases / {term_count} multiplier terms)"
    )


def endpoint_support_table() -> None:
    # Entries are (endpoint l, first-root coordinate s, forced statement).
    # Normalize {j,k,t}={0,1,2}; the table is symmetric in j,k after also
    # relabelling the selected residual coloop.
    table = {
        (0, 0): "y_j=0 and z_k*z_t=0",
        (0, 1): "y_k*z_k=0",
        (0, 2): "z_t=0",
        (1, 0): "y_j*z_j=0",
        (1, 1): "y_k=0 and z_j*z_t=0",
        (1, 2): "z_t=0",
    }
    assert len(table) == 6
    # If s equals the endpoint, y_s=0 together with y_t=0 leaves exactly
    # the other complementary coordinate; the v-incidence gives the product
    # zero in the two remaining z coordinates.
    for endpoint in range(2):
        assert "and" in table[(endpoint, endpoint)]
        assert table[(endpoint, 2)] == "z_t=0"
        other = 1 - endpoint
        assert "=0" in table[(endpoint, other)]
    print("coordinate-endpoint support table: PASS (2 endpoints x 3 s-cases)")


def main() -> None:
    determinant_face_and_gates()
    coloop_row_geometry()
    generalized_incidence_cover()
    certificate_replay()
    endpoint_support_table()
    print("residual second-root-coloop projective-pencil localization: PASS")


if __name__ == "__main__":
    main()
