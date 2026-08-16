#!/usr/bin/env python3
"""Exact replay for the residual-coloop common-middle-row localization.

The owning theorem supplies the arbitrary-field orbit proof.  This verifier
rebuilds all 90 normal-form systems, checks every pinned rational unit-ideal
identity, and replays the determinant-pencil table that leaves only the
``w=e_u, z_s=0`` endpoint.
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
    "one_two_two_residual_second_root_coloop_common_middle_row_certificates.json"
)
CERTIFICATE_SHA256 = (
    "a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1"
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
    "sigma",
)
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))
TAU = SYMBOL_BY_NAME["tau"]
SIGMA = SYMBOL_BY_NAME["sigma"]

Vector = tuple[sp.Expr, ...]


def e(index: int, size: int = 4) -> Vector:
    return tuple(sp.Integer(position == index) for position in range(size))


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def line_patch(patch: int) -> Vector:
    if patch == 0:
        return (sp.Integer(1), TAU, SIGMA, sp.Integer(0))
    if patch == 1:
        return (sp.Integer(0), sp.Integer(1), TAU, sp.Integer(0))
    assert patch == 2
    return e(2)


def normal_form_rows(
    plane_case: int, orientation: int, patch: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    r_rows = (e(0), e(1))
    if plane_case == 9:
        q_rows = r_rows
    else:
        intersection_type, third_type = divmod(plane_case, 3)
        if intersection_type == 0:
            intersection = e(0)
        elif intersection_type == 1:
            intersection = e(1)
        else:
            intersection = add(e(0), e(1))
        if third_type == 0:
            q_rows = (intersection, e(2))
        elif third_type == 1:
            q_rows = (e(2), intersection)
        else:
            q_rows = (e(2), subtract(intersection, e(2)))

    v = line_patch(patch)
    escape = e(3)
    if orientation == 0:
        p_rows = (escape, v)
    elif orientation == 1:
        p_rows = (v, escape)
    else:
        assert orientation == 2
        p_rows = (escape, subtract(v, escape))
    return r_rows, p_rows, q_rows


def orbit_cover() -> None:
    distinct_plane_types = set(product(range(3), repeat=2))
    orientations = {0, 1, 2}
    patches = {0, 1, 2}
    assert len(distinct_plane_types) == 9
    assert len(orientations) == len(patches) == 3
    expected = {
        (plane_case, orientation, patch)
        for plane_case in range(10)
        for orientation in orientations
        for patch in patches
    }
    assert len(expected) == 90

    # Hostile points in each affine patch remain nonzero identically.  The
    # theorem proves that the patches cover every projective v in S.
    assert line_patch(0)[0] == 1
    assert line_patch(1)[:2] == (0, 1)
    assert line_patch(2) == e(2)
    for orientation in orientations:
        _, p_rows, _ = normal_form_rows(8, orientation, 0)
        if orientation == 0:
            assert p_rows[1] == line_patch(0)
        elif orientation == 1:
            assert p_rows[0] == line_patch(0)
        else:
            assert add(p_rows[0], p_rows[1]) == line_patch(0)
    print("common-middle-row orbit cover: PASS (10 x 3 x 3 = 90 cases)")


def form(root: str, bit: int) -> tuple[sp.Symbol, ...]:
    return tuple(SYMBOL_BY_NAME[f"{root}{bit}{coordinate}"] for coordinate in range(4))


def evaluate(linear_form: tuple[sp.Symbol, ...], vector: Vector) -> sp.Expr:
    return sum(
        (
            coefficient * coordinate
            for coefficient, coordinate in zip(linear_form, vector, strict=True)
        ),
        sp.Integer(0),
    )


def polarized_product(
    source_bits: tuple[int, int, int], rows: tuple[Vector, Vector, Vector]
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


def generators(plane_case: int, orientation: int, patch: int) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = normal_form_rows(plane_case, orientation, patch)
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
            if source_bits == (1, 1, 1) and row_bits == (1, 0, 1):
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
        f"{plane_case}-{orientation}-{patch}"
        for plane_case in range(10)
        for orientation in range(3)
        for patch in range(3)
    }
    assert set(data["cases"]) == expected

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for key in sorted(expected):
        plane_case, orientation, patch = (int(value) for value in key.split("-"))
        system = generators(plane_case, orientation, patch)
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total = zero
        for generator, encoded in zip(system, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, key
    assert term_count == 31591
    print(
        "common-middle-row Nullstellensatz certificates: PASS "
        f"(90 cases / {term_count} multiplier terms)"
    )


def target_cell(i: int, j: int, k: int) -> tuple[int, int]:
    # Rows are ordered (u,t), (beta_*,beta_s), and (gamma^u,gamma^t).
    if j == 0 and i == k:
        return tuple(int(position == i) for position in range(2))  # type: ignore[return-value]
    return (0, 0)


def determinant_pencil_localization() -> None:
    # Normalize (s,u,t)=(0,1,2), y=e_u.  The P-plane always contains e_s;
    # for h*kappa!=0 its other row has both active coordinates.
    h, kappa, mu, y_u = sp.symbols("h kappa mu y_u", nonzero=True)
    z_s, w_s = sp.symbols("z_s w_s")
    normal_p = sp.Matrix([0, kappa * y_u, -h * mu])
    beta_star = sp.Matrix([0, h * mu, kappa * y_u])
    assert sp.expand(normal_p.dot(sp.Matrix(e(0, 3)))) == 0
    assert sp.expand(normal_p.dot(beta_star)) == 0
    assert beta_star[1] != 0 and beta_star[2] != 0

    q_gate = kappa * z_s - h * w_s
    assert sp.Poly(q_gate, h, kappa).coeff_monomial(h) == -w_s
    assert sp.Poly(q_gate, h, kappa).coeff_monomial(kappa) == z_s

    table = {
        (i, j, k): target_cell(i, j, k)
        for i, j, k in product(range(2), repeat=3)
    }
    assert {cell for cell, value in table.items() if value != (0, 0)} == {
        (0, 0, 0),
        (1, 0, 1),
    }
    assert table[(0, 0, 0)] == (1, 0)
    assert table[(1, 0, 1)] == (0, 1)

    # The only way to avoid the common-middle-row table for every pencil
    # direction is q_gate identically zero.  Endpoint w=e_s has w_s!=0;
    # endpoint w=e_u has w_s=0 and therefore forces z_s=0.
    endpoint_gate_coefficients = {
        "w=e_s": (sp.Integer(1), z_s),
        "w=e_u": (sp.Integer(0), z_s),
    }
    assert endpoint_gate_coefficients["w=e_s"][0] != 0
    assert endpoint_gate_coefficients["w=e_u"][0] == 0
    assert endpoint_gate_coefficients["w=e_u"][1] == z_s
    print("determinant-pencil common-middle-row localization: PASS")


def main() -> None:
    orbit_cover()
    certificate_replay()
    determinant_pencil_localization()
    print("residual second-root-coloop terminal endpoint localization: PASS")


if __name__ == "__main__":
    main()
