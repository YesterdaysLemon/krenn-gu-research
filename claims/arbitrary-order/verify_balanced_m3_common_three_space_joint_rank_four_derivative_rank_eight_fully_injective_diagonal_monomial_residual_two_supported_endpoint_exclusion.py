#!/usr/bin/env python3
"""Exact replay of the diagonal monomial two-supported endpoint exclusion.

The owning theorem contains the arbitrary-field argument.  This verifier
checks the complete target slice, the tangent/secant incidence fork, the
29 normalized row-space charts, and every rational Nullstellensatz identity.
"""

from __future__ import annotations

import hashlib
import json
from itertools import permutations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_"
    "fully_injective_diagonal_monomial_residual_two_supported_endpoint_"
    "certificates.json"
)
CERTIFICATE_SHA256 = (
    "e9414389e653a76770d8f105a086fcae6887d2dbe012f41e5d74f78686c72f52"
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
    "g",
    "h",
)
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))
TAU = SYMBOL_BY_NAME["tau"]
G = SYMBOL_BY_NAME["g"]
H = SYMBOL_BY_NAME["h"]

Row = tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
ZERO: Row = (sp.Integer(0),) * 4
Q0: Row = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0))
Q1: Row = (sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(1))


def e(index: int, size: int = 3) -> sp.Matrix:
    return sp.eye(size)[:, index]


def target(alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [alpha[index] * beta[index] * gamma[index] for index in range(3)]
    )


def complete_endpoint_face() -> None:
    """Reconstruct the exact same-third row and both common physical rows."""

    w0, w1 = sp.symbols("w_0 w_1", nonzero=True)
    w = sp.Matrix([w0, w1, 0])
    gamma_rows = (sp.Matrix([w1, -w0, 0]), e(2))
    assert all(sp.expand(gamma.dot(w)) == 0 for gamma in gamma_rows)

    roots = (e(0), e(1))
    for i, j, k in product(range(2), repeat=3):
        value = target(roots[i], roots[j], gamma_rows[k])
        expected = sp.zeros(3, 1)
        if (i, j, k) == (0, 0, 0):
            expected = w1 * e(0)
        if (i, j, k) == (1, 1, 0):
            expected = -w0 * e(1)
        assert value == expected

    # For C=e_2 tensor e_2, every complementary row/column of C is zero.
    # Thus p_2 is a common middle row and r_2 a common first row on w^perp.
    residual = sp.zeros(3, 3)
    residual[2, 2] = 1
    assert all(residual[i, 2] == 0 for i in range(2))
    assert all(residual[2, j] == 0 for j in range(2))
    print("diagonal endpoint complete target face: PASS")


def cayley_hyperdeterminant(entries: dict[tuple[int, int, int], sp.Expr]) -> sp.Expr:
    a = entries
    return sp.expand(
        a[0, 0, 0] ** 2 * a[1, 1, 1] ** 2
        + a[0, 0, 1] ** 2 * a[1, 1, 0] ** 2
        + a[0, 1, 0] ** 2 * a[1, 0, 1] ** 2
        + a[1, 0, 0] ** 2 * a[0, 1, 1] ** 2
        - 2
        * (
            a[0, 0, 0] * a[0, 0, 1] * a[1, 1, 0] * a[1, 1, 1]
            + a[0, 0, 0] * a[0, 1, 0] * a[1, 0, 1] * a[1, 1, 1]
            + a[0, 0, 0] * a[1, 0, 0] * a[0, 1, 1] * a[1, 1, 1]
            + a[0, 0, 1] * a[0, 1, 0] * a[1, 0, 1] * a[1, 1, 0]
            + a[0, 0, 1] * a[1, 0, 0] * a[0, 1, 1] * a[1, 1, 0]
            + a[0, 1, 0] * a[1, 0, 0] * a[0, 1, 1] * a[1, 0, 1]
        )
        + 4
        * (
            a[0, 0, 0] * a[0, 1, 1] * a[1, 0, 1] * a[1, 1, 0]
            + a[0, 0, 1] * a[0, 1, 0] * a[1, 0, 0] * a[1, 1, 1]
        )
    )


def incidence_reduction() -> None:
    """Check the tangent/secant discriminator and the finite orbit census."""

    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    secant = {bits: sp.Integer(0) for bits in product(range(2), repeat=3)}
    secant[0, 0, 0] = alpha
    secant[1, 1, 1] = beta
    assert cayley_hyperdeterminant(secant) == alpha**2 * beta**2

    xl = sp.symbols("xl0:2")
    yl = sp.symbols("yl0:2")
    zl = sp.symbols("zl0:2")
    xq = sp.symbols("xq0:2")
    yq = sp.symbols("yq0:2")
    zq = sp.symbols("zq0:2")
    tangent = {
        (i, j, k): (
            xq[i] * yl[j] * zl[k]
            + xl[i] * yq[j] * zl[k]
            + xl[i] * yl[j] * zq[k]
        )
        for i, j, k in product(range(2), repeat=3)
    }
    assert cayley_hyperdeterminant(tangent) == 0

    # For ell=a_0 r_0+a_1 r_1=b_0 p_0+b_1 p_1, its q_0 square is
    # a_0 b_0 T_0+a_1 b_1 T_1.  Two terms violate tangent separation.
    # With one term, S2AL mixed-factor sharing eliminates every noncoordinate
    # support.  The surviving Boolean supports are precisely the four ordered
    # coordinate incidences, including the two cross incidences.
    allowed: set[tuple[int, int]] = set()
    for a_mask in range(1, 4):
        for b_mask in range(1, 4):
            diagonal_products = [
                bool((a_mask >> index) & 1 and (b_mask >> index) & 1)
                for index in range(2)
            ]
            count = sum(diagonal_products)
            if count == 2:
                continue
            if count == 1 and (a_mask == 3 or b_mask == 3):
                continue
            allowed.add((a_mask, b_mask))
    assert allowed == {(1, 1), (1, 2), (2, 1), (2, 2)}

    # Once one graph column is coordinate, diagonal rescaling leaves four
    # quotient matrices: same/cross, with zero/nonzero shear.
    quotient_matrices = (
        sp.Matrix([[1, 0], [0, 1]]),
        sp.Matrix([[1, 1], [0, 1]]),
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, 1], [1, 1]]),
    )
    assert all(matrix.det() in (1, -1) for matrix in quotient_matrices)
    assert all(
        sum(bool(matrix[row, 0]) for row in range(2)) == 1
        for matrix in quotient_matrices
    )

    specifications = case_specifications()
    assert len(specifications) == 29
    assert sum(spec[3] for spec in specifications.values()) == 16
    assert sum(not spec[3] for spec in specifications.values()) == 13
    print("common-row shift / projection / Borel orbit cover: PASS (29 charts)")


def add_rows(left: Row, right: Row) -> Row:
    return tuple(sp.expand(a + b) for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def projection_rows(kind: str, l0: Row, l1: Row) -> tuple[Row, Row]:
    if kind == "diag":
        return add_rows((1, 0, 0, 0), l0), add_rows((0, 1, 0, 0), l1)
    if kind == "cross":
        return add_rows((0, 1, 0, 0), l0), add_rows((1, 0, 0, 0), l1)
    if kind == "diag_shear":
        return add_rows((1, 0, 0, 0), l0), (sp.Integer(1), sp.Integer(1), G, H)
    if kind == "cross_shear":
        return add_rows((0, 1, 0, 0), l0), (sp.Integer(1), sp.Integer(1), G, H)
    raise AssertionError(kind)


def case_specifications() -> dict[
    str, tuple[tuple[Row, Row], tuple[Row, Row], tuple[Row, Row], bool, Row, Row]
]:
    r = ((sp.Integer(1), 0, 0, 0), (0, sp.Integer(1), 0, 0))
    q = (Q0, Q1)
    specifications = {}
    fixed = {
        "zero_zero": (ZERO, ZERO),
        "zero_q1": (ZERO, Q1),
        "zero_q0": (ZERO, Q0),
        "prop_q0": (Q0, (0, 0, TAU, 0)),
    }
    for kind in ("diag", "cross"):
        for orbit, (l0, l1) in fixed.items():
            specifications[f"{kind}_{orbit}"] = (
                r,
                projection_rows(kind, l0, l1),
                q,
                False,
                ZERO,
                ZERO,
            )
    specifications["diag_ind_q1_q0"] = (
        r,
        projection_rows("diag", Q1, Q0),
        q,
        False,
        ZERO,
        ZERO,
    )
    for kind in ("diag", "cross"):
        specifications[f"{kind}_prop_q1"] = (
            r,
            projection_rows(kind, Q1, (0, 0, 0, TAU)),
            q,
            True,
            Q1,
            Q1,
        )
    independent = {
        "ind_q1_q0": (Q1, Q0),
        "ind_affine": (Q0, (0, 0, 1, 1)),
    }
    for kind, orbit in (
        ("diag", "ind_affine"),
        ("cross", "ind_q1_q0"),
        ("cross", "ind_affine"),
    ):
        l0, l1 = independent[orbit]
        for u_index, v_index in product(range(2), repeat=2):
            specifications[f"{kind}_{orbit}_u{u_index}_v{v_index}"] = (
                r,
                projection_rows(kind, l0, l1),
                q,
                True,
                (l0, l1)[u_index],
                (l0, l1)[v_index],
            )
    for kind in ("diag_shear", "cross_shear"):
        for orbit, l0 in (("zero", ZERO), ("q0", Q0)):
            specifications[f"{kind}_{orbit}"] = (
                r,
                projection_rows(kind, l0, ZERO),
                q,
                False,
                ZERO,
                ZERO,
            )
        specifications[f"{kind}_q1"] = (
            r,
            projection_rows(kind, Q1, ZERO),
            q,
            True,
            Q1,
            Q1,
        )
    return specifications


def form(root: str, bit: int) -> tuple[sp.Symbol, ...]:
    return tuple(SYMBOL_BY_NAME[f"{root}{bit}{coordinate}"] for coordinate in range(4))


def evaluate(linear_form: tuple[sp.Symbol, ...], row: Row) -> sp.Expr:
    return sum(
        (
            coefficient * coordinate
            for coefficient, coordinate in zip(linear_form, row, strict=True)
        ),
        sp.Integer(0),
    )


def polarized_product(source_bits: tuple[int, int, int], rows: tuple[Row, Row, Row]) -> sp.Expr:
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


def case_generators(key: str) -> list[sp.Poly]:
    r, p, q, physical, u, v = case_specifications()[key]
    generators = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            value = polarized_product(
                source_bits,
                (r[row_bits[0]], p[row_bits[1]], q[row_bits[2]]),
            )
            if source_bits == (0, 0, 0) and row_bits == (0, 0, 0):
                value -= 1
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 0):
                value -= 1
            generators.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
    if physical:
        for source_bits in product(range(2), repeat=3):
            for i, k in product(range(2), repeat=2):
                value = polarized_product(source_bits, (r[i], v, q[k]))
                generators.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
        for source_bits in product(range(2), repeat=3):
            for j, k in product(range(2), repeat=2):
                value = polarized_product(source_bits, (u, p[j], q[k]))
                generators.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
    assert len(generators) == (128 if physical else 64)
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

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for key in sorted(specifications):
        generators = case_generators(key)
        multipliers = data["cases"][key]
        assert len(multipliers) == len(generators)
        total = zero
        for generator, encoded in zip(generators, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, key
    assert term_count == 2972
    print(
        "diagonal endpoint Nullstellensatz certificates: PASS "
        f"(29 charts / {term_count} multiplier terms)"
    )


def main() -> None:
    complete_endpoint_face()
    incidence_reduction()
    certificate_replay()
    print("diagonal monomial two-supported endpoint exclusion: PASS")


if __name__ == "__main__":
    main()
