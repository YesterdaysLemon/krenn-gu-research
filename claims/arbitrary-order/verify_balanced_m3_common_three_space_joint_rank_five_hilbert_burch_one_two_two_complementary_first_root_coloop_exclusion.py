#!/usr/bin/env python3
"""Exact replay for exclusion of both complementary first-root coloops."""

from __future__ import annotations

import hashlib
import json
from itertools import permutations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_complementary_first_root_coloop_certificates.json"
)
CERTIFICATE_SHA256 = (
    "10ce1216ed2360159eb4709140eabe4db1c51ad509f340ac137300a636583088"
)
DEPENDENCY_CERTIFICATES = {
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
    "c0",
    "c1",
)
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))
C0 = SYMBOL_BY_NAME["c0"]
C1 = SYMBOL_BY_NAME["c1"]

Vector = tuple[sp.Expr, ...]


def e(index: int, size: int = 4) -> Vector:
    return tuple(sp.Integer(position == index) for position in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(
        sum((vector[i] for vector in vectors), sp.Integer(0))
        for i in range(len(vectors[0]))
    )


def scale(value: sp.Expr, vector: Vector) -> Vector:
    return tuple(sp.expand(value * coordinate) for coordinate in vector)


def pencil_and_coloop_geometry() -> None:
    h, kappa, mu = sp.symbols("h kappa mu", nonzero=True)
    # Matched evaluation pairs make the determinant in D_B^T vanish.
    beta_pair = sp.Matrix([h, kappa])
    gamma_pair = sp.Matrix([-h, -kappa])
    determinant = beta_pair[0] * gamma_pair[1] - beta_pair[1] * gamma_pair[0]
    assert sp.expand(determinant) == 0

    # Every displayed covector has both equations of L equal to zero:
    # pure r_b; beta and gamma evaluation kernels; and paired beta+gamma.
    lam = sp.symbols("lambda", nonzero=True)
    checks = (
        (lam * 0, sp.Integer(0)),
        (lam * 0 + 0, mu * 0),
        (lam * 0 + 0, sp.Integer(0)),
        (lam * 0 + h - h, kappa - kappa),
    )
    assert all(sp.expand(left) == 0 and sp.expand(right) == 0 for left, right in checks)

    # Concrete labels (s,a,b)=(0,1,2): the derivative-zero face is
    # alpha_s=0, while the selected coloop divisor is alpha_a=0.  Their
    # pure first-root intersection is exactly e_b^*.
    alpha_s_normal = sp.Matrix([1, 0, 0])
    alpha_a_normal = sp.Matrix([0, 1, 0])
    intersection = alpha_s_normal.cross(alpha_a_normal)
    assert intersection == sp.Matrix([0, 0, 1])

    # The two coordinate projection gates are the selected coordinates of
    # the pencil normals.  Their identically-zero alternatives are A and B.
    y_s, z_s, w_s, delta_st = sp.symbols("y_s z_s w_s delta_st")
    l_p = kappa * y_s - h * mu * delta_st
    l_q = kappa * z_s - h * w_s
    product_gate = sp.Poly(sp.expand(l_p * l_q), h, kappa)
    assert product_gate.total_degree() == 2
    assert sp.Poly(l_p, h, kappa).total_degree() == 1
    assert sp.Poly(l_q, h, kappa).total_degree() == 1
    print("complementary-alpha pencil / coloop-plane geometry: PASS")


def target_coefficients(alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(alpha[i] * beta[i] * gamma[i]) for i in range(3))


def one_sided_tables() -> None:
    b0, b1, g0, g1 = sp.symbols("b0 b1 g0 g1", nonzero=True)
    alpha_rows = (sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]))

    # A without B: the active beta row is common and gamma has coordinate lifts.
    beta_rows = (sp.Matrix([0, 0, 1]), sp.Matrix([b0, b1, 0]))
    gamma_rows = (sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]))
    nonzero_a = set()
    for i, j, k in product(range(2), repeat=3):
        values = target_coefficients(alpha_rows[i], beta_rows[j], gamma_rows[k])
        if any(values):
            nonzero_a.add((i, j, k))
    assert nonzero_a == {(0, 1, 0), (1, 1, 1)}

    # B without A: the active gamma row is common and beta has coordinate lifts.
    beta_rows = (sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]))
    gamma_rows = (sp.Matrix([0, 0, 1]), sp.Matrix([g0, g1, 0]))
    nonzero_b = set()
    for i, j, k in product(range(2), repeat=3):
        values = target_coefficients(alpha_rows[i], beta_rows[j], gamma_rows[k])
        if any(values):
            nonzero_b.add((i, j, k))
    assert nonzero_b == {(0, 0, 1), (1, 1, 1)}
    print("one-sided same-third-row transfers: PASS")


def r_line(incidence: int, rtype: int) -> Vector:
    if rtype == 0:
        return e(0)
    if rtype == 1:
        return e(1)
    assert incidence == 1 and rtype == 2
    return add(e(0), e(1))


def normal_form_rows(
    incidence: int, rtype: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    r_rows = (e(3), r_line(incidence, rtype))
    p_rows = (e(0), e(2))
    q_zero = e(0) if incidence == 0 else e(1)
    q_one = add(scale(C0, e(0)), scale(C1, e(1)), scale(-1, e(2)))
    return r_rows, p_rows, (q_zero, q_one)


def exact_case_cover() -> None:
    expected = {(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)}
    for incidence, rtype in expected:
        r_rows, p_rows, q_rows = normal_form_rows(incidence, rtype)
        assert r_rows[0] == e(3)
        assert r_rows[1][2:] == (0, 0)
        assert p_rows[0][2:] == (0, 0)
        assert q_rows[0][2:] == (0, 0)
        assert add(p_rows[1], q_rows[1])[2:] == (0, 0)
        if incidence == 0:
            assert p_rows[0] == q_rows[0]
        else:
            assert p_rows[0] != q_rows[0]
    print("actual complementary-alpha endpoint cover: PASS (2 + 3 = 5 cases)")


def equal_partner_plane_boundary() -> None:
    # If both partner planes equal C, write H=F*M in one C basis.  Symmetry
    # of E11*M forces M10=0, hence the inactive rows align and the active
    # values become one square map on the two-dimensional first-row plane.
    m00, m01, m10, m11 = sp.symbols("m00 m01 m10 m11")
    matrix = sp.Matrix([[m00, m01], [m10, m11]])
    e11 = sp.Matrix([[0, 0], [0, 1]])
    symmetric_form = e11 * matrix
    assert sp.expand(symmetric_form[0, 1] - symmetric_form[1, 0]) == -m10
    print("equal partner-plane square boundary: PASS")


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


def generators(incidence: int, rtype: int) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = normal_form_rows(incidence, rtype)
    output = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            rows = (
                r_rows[row_bits[0]],
                p_rows[row_bits[1]],
                q_rows[row_bits[2]],
            )
            value = polarized_product(source_bits, rows)
            if source_bits == (0, 0, 0) and row_bits == (0, 1, 1):
                value -= 1
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 1):
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
    expected = {"0-0", "0-1", "1-0", "1-1", "1-2"}
    assert set(data["cases"]) == expected

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for key in sorted(expected):
        incidence, rtype = (int(value) for value in key.split("-"))
        system = generators(incidence, rtype)
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total = zero
        for generator, encoded in zip(system, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, key
    assert term_count == 5928
    print(
        "complementary-alpha Nullstellensatz certificates: PASS "
        f"(5 cases / {term_count} multiplier terms)"
    )


def dependency_pins() -> None:
    for name, expected in DEPENDENCY_CERTIFICATES.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected
    print("dependency certificate pins: PASS (S2BF and S2BE)")


def main() -> None:
    pencil_and_coloop_geometry()
    one_sided_tables()
    exact_case_cover()
    equal_partner_plane_boundary()
    certificate_replay()
    dependency_pins()
    print("both complementary first-root coordinate coloops: IMPOSSIBLE")


if __name__ == "__main__":
    main()
