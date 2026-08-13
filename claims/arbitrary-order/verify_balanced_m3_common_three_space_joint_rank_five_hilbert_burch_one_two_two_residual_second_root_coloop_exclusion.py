#!/usr/bin/env python3
"""Exact replay for exclusion of both residual second-root coloops.

The owning theorem proves the arbitrary-field reduction.  This verifier
checks the terminal determinant table, the exact 15-family coloop cover, the
equal-plane symmetry contradiction, and every pinned rational unit identity.
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
    "one_two_two_residual_second_root_coloop_terminal_same_pair_certificates.json"
)
CERTIFICATE_SHA256 = (
    "bc63359ece10e7d12237ab5821f64227de8391b5a9422091d9b5c0591484a7a0"
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

Vector = tuple[sp.Expr, ...]


def e(index: int, size: int = 4) -> Vector:
    return tuple(sp.Integer(position == index) for position in range(size))


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def terminal_face_and_coloop_geometry() -> None:
    # Normalize (s,u,t)=(0,1,2), y=w=e_u, z_s=0, z_t!=0.
    h, kappa, mu, y_u, z_u, z_t = sp.symbols(
        "h kappa mu y_u z_u z_t", nonzero=True
    )
    beta_star = sp.Matrix([0, h * mu, kappa * y_u])
    normal_p = sp.Matrix([0, kappa * y_u, -h * mu])
    assert sp.expand(beta_star.dot(normal_p)) == 0

    # Q_delta has normal kappa*z-h*w in e_s^perp.  One explicit annihilator
    # line has both active coordinates away from two projective directions.
    normal_q = sp.Matrix([0, kappa * z_u - h, kappa * z_t])
    gamma_star = sp.Matrix([0, kappa * z_t, h - kappa * z_u])
    assert sp.expand(gamma_star.dot(normal_q)) == 0

    table = {}
    beta_rows = (beta_star, sp.Matrix([1, 0, 0]))
    gamma_rows = (gamma_star, sp.Matrix([1, 0, 0]))
    for i, j, k in product(range(2), repeat=3):
        target_index = (1, 2)[i]
        coefficient = sp.expand(
            beta_rows[j][target_index] * gamma_rows[k][target_index]
        )
        table[(i, j, k)] = coefficient
    assert {
        cell for cell, value in table.items() if value != 0
    } == {(0, 0, 0), (1, 0, 0)}
    assert table[(0, 0, 0)] == h * kappa * mu * z_t
    assert sp.expand(
        table[(1, 0, 0)] - kappa * y_u * (h - kappa * z_u)
    ) == 0

    # The two residual orientations select different lines of P_delta.
    # If j=s, beta_star lies in beta_j=0 and its opposite Q row cancels it
    # modulo R.  If j=u, P_delta intersect beta_j=0 is exactly e_s and has
    # zero evaluation pair, so p_s lies in R.
    assert beta_star[0] == 0
    b_u, b_t = sp.symbols("b_u b_t")
    intersection = sp.solve(
        (kappa * y_u * b_u - h * mu * b_t, b_u),
        (b_u, b_t),
        dict=True,
    )
    assert intersection == [{b_t: 0, b_u: 0}]
    print("terminal determinant face / residual-coloop fork: PASS")


def q_intersection(qtype: int) -> Vector:
    if qtype == 0:
        return e(0)
    if qtype == 1:
        return e(1)
    assert qtype == 2
    return add(e(0), e(1))


def normal_form_rows(
    qtype: int, branch: int, patch: int
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector], tuple[Vector, Vector]]:
    r_rows = (e(0), e(1))
    q_rows = (e(2), q_intersection(qtype))
    if branch == 0:
        # j=s: p0+q0 is in R.  The three patches cover a nonzero first
        # R-coordinate, the remaining endpoint, and the zero sum.
        if patch == 0:
            p_zero = (sp.Integer(1), TAU, sp.Integer(-1), sp.Integer(0))
        elif patch == 1:
            p_zero = (sp.Integer(0), sp.Integer(1), sp.Integer(-1), sp.Integer(0))
        else:
            assert patch == 2
            p_zero = e(2)
        p_rows = (p_zero, e(3))
    else:
        assert branch == 1
        # j=u: the inactive row p1 is a nonzero line of R.
        if patch == 0:
            p_one = (sp.Integer(1), TAU, sp.Integer(0), sp.Integer(0))
        else:
            assert patch == 1
            p_one = e(1)
        p_rows = (e(3), p_one)
    return r_rows, p_rows, q_rows


def exact_case_cover() -> None:
    expected = {
        (qtype, 0, patch)
        for qtype in range(3)
        for patch in range(3)
    } | {
        (qtype, 1, patch)
        for qtype in range(3)
        for patch in range(2)
    }
    assert len(expected) == 15
    for qtype, branch, patch in expected:
        r_rows, p_rows, q_rows = normal_form_rows(qtype, branch, patch)
        assert q_rows[1] in (e(0), e(1), add(e(0), e(1)))
        if branch == 0:
            if patch < 2:
                assert add(p_rows[0], q_rows[0])[2] == 0
            else:
                assert p_rows[0] == q_rows[0]
        else:
            assert p_rows[1][2:] == (0, 0)
            assert p_rows[1] != (0, 0, 0, 0)
        assert r_rows == (e(0), e(1))
    print("actual residual-coloop same-pair cover: PASS (9 + 6 = 15 cases)")


def equal_plane_symmetry() -> None:
    # If Q=R, write H=F*M where H is the symmetric permanent matrix and
    # M=(L^T)^(-1).  T0 contributes E00*M and T1 contributes E10*M.
    m00, m01, m10, m11 = sp.symbols("m00 m01 m10 m11")
    m = sp.Matrix([[m00, m01], [m10, m11]])
    e00 = sp.Matrix([[1, 0], [0, 0]])
    e10 = sp.Matrix([[0, 0], [1, 0]])
    h0 = e00 * m
    h1 = e10 * m
    conditions = [
        sp.expand(h0[0, 1] - h0[1, 0]),
        sp.expand(h1[0, 1] - h1[1, 0]),
    ]
    assert conditions == [m01, -m00]
    singular = m.subs({m00: 0, m01: 0})
    assert sp.expand(singular.det()) == 0
    print("equal first/third-plane symmetry obstruction: PASS")


def form(root: str, bit: int) -> tuple[sp.Symbol, ...]:
    return tuple(
        SYMBOL_BY_NAME[f"{root}{bit}{coordinate}"] for coordinate in range(4)
    )


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


def generators(qtype: int, branch: int, patch: int) -> list[sp.Poly]:
    r_rows, p_rows, q_rows = normal_form_rows(qtype, branch, patch)
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
            if source_bits == (1, 1, 1) and row_bits == (1, 0, 0):
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
        f"{qtype}-0-{patch}" for qtype in range(3) for patch in range(3)
    } | {f"{qtype}-1-{patch}" for qtype in range(3) for patch in range(2)}
    assert set(data["cases"]) == expected

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for key in sorted(expected):
        qtype, branch, patch = (int(value) for value in key.split("-"))
        system = generators(qtype, branch, patch)
        multipliers = data["cases"][key]
        assert len(system) == len(multipliers) == 64
        total = zero
        for generator, encoded in zip(system, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, key
    assert term_count == 32871
    print(
        "terminal same-pair Nullstellensatz certificates: PASS "
        f"(15 cases / {term_count} multiplier terms)"
    )


def main() -> None:
    terminal_face_and_coloop_geometry()
    exact_case_cover()
    equal_plane_symmetry()
    certificate_replay()
    print("both residual second-root coordinate coloops: IMPOSSIBLE")


if __name__ == "__main__":
    main()
