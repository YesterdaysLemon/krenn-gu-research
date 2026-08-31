#!/usr/bin/env python3
"""Verify the scoped p=0,1 nonzero-offset exclusion (GLD102).

The verifier reconstructs six actual seven-minors of the committed GLD71
37-by-9 syndrome on the normalized GLD88/F88 H4 offset chart.  It keeps the
parameter ``a`` symbolic and treats the two exhaustive nonzero-offset charts

    D(B),                 with C = B*t,
    V(B) intersect D(C).

For p=0 the B-open selected-minor ideal has exactly two conjugate points;
an exact direct seven-minor of the complete syndrome is nonzero at both, so
neither has rank at most six.  For p=1 the sixth selector excludes the two
points left by the other five.  Both C-open ideals are unit.  Consequently a
rank-at-most-six point with p in {0,1} on D(Delta) has B=C=0.

This is a one-way rank-to-selected-minor argument on one normalized chart.
It does not exclude the endpoint B=C=0, prove physical incidence emptiness,
close the E31 wall, or resolve Krenn--Gu.  The global conjecture remains
UNRESOLVED.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"

p, q, a, B, C, t, z = sp.symbols("p q a B C t z")
K = QQ.frac_field(p, q, a)
FIELD_ELEMENT_TYPE = type(K.one)

SELECTORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTOR_NAMES = tuple(SELECTORS)
BASE_SELECTOR_NAMES = ("T0", "T1", "T2", "Y1", "X3")
SUPPORT_ROWS = tuple(
    sorted({row for rows, _columns in SELECTORS.values() for row in rows})
)
EXPECTED_OFFSET_SUPPORT = {
    (0, 1),
    (1, 0),
    (1, 1),
    (2, 0),
    (2, 1),
    (3, 0),
}

EXPECTED_SOURCE_LF_SHA256 = {
    GLD71: "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    GLD88: "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
}
EXPECTED_SUPPORT_DIGEST = (
    "f2670c9393287eae16dce1bc8aa41e4b0c421645833ad29619a6d7b6fd94ac07"
)

# Hashes encode primitive polynomials as ordered monomial/coefficient lists.
# They pin the exact equations independently regenerated from the two tracked
# parents below; no ignored research-run file is consumed.
EXPECTED_B_OPEN_HASHES = {
    0: {
        "T0": "6698570ba9b983a03eb59e9bf33516dacd34806ebee1b49affb8cf10bd791bad",
        "T1": "c946ddf2793058f6c374230b7a11b997c34a5f930980f38e99f64eb3989b9f47",
        "T2": "eb247f55987cf51ac3056eb3b6b592155f5d7f38e42638f26ed864b644d36d0b",
        "T3": "50ea1f5f1f99449f97d083171a1c19379d610c7028fd6aec509504a6b725126f",
        "Y1": "f58c27e889af1743689fbac7508212ce232d5ea9f627625fc5cd08d09d947cc8",
        "X3": "bec33400e8a096f815fc2313bf8c79730192b6b0aa07be6863247f6d0748436f",
    },
    1: {
        "T0": "0ef9b6e45dfe83211b11257929815cdef76de590e58171e698ed876c6abdd75a",
        "T1": "3c78c42206d3649f2b6206a4745dad2ad2284c3241a7e76ab25148d0a02d6f67",
        "T2": "f749ac6c9baf18f561550a0c11c8ce491aee07a38dfa4b4d211b11e3427688f4",
        "T3": "d52b7380f8724c57c9628e26340bb30235970d599bcd2669cdedd08624bb8893",
        "Y1": "635d8d441511e8685ec961569f55021521d1489da199c53a795490936ddaf481",
        "X3": "71c0db85421a3ec2e5243fbdfb60b4b35059704b70a663a6e98060c425abfc05",
    },
}
EXPECTED_C_OPEN_HASHES = {
    0: {
        "T0": "6f5db0d7e894c8dccee64b38e57ca831cbe36abdfbcd9dbf3e1949d4678db44a",
        "T1": "ee90b3a38619597c81ef424da576efb196d4370e5cc6bc5d6df6e7117549147d",
        "T2": "21ccb7e208b186ad567b01d474d544cf5188787b25505ae2ee9a18b2d6d0a88a",
        "T3": "1f12748b26196289948f9fdcade5f1378085294db2b646159f7174dfc5d70054",
        "Y1": "1c4ca6991ea9cf416bc16aac62ed24d209161a4694d5618b43bc0e9b48ccd2e9",
        "X3": "1c866717a84aa6efa9eb1a0c8e445e980ca6f26148f24c4be27e6e18c2a81831",
    },
    1: {
        "T0": "c80794afcf47d3c2531ad978736f07abaee4170dc48cd12a88ab3d1028de3e2b",
        "T1": "c4aea8a643fcba39845ffb2d0604de0ad84c7c5f8ddd956fb07e1f4b83750876",
        "T2": "900cafb2918de28db8c5188d0935251c662f88d3c46122543464167af232d74c",
        "T3": "dae01bb49c4ea2b669ab9a331c578aa4084ac0e83b530887ceb095bdda0cef4d",
        "Y1": "f3d6843358ed572dbddeaba098cd7061fc270c1138a113d020d83da1bd1ce65a",
        "X3": "e563ef704fbedbacdaa08ba0e94797604d3446519bcc428c07284f36372c2425",
    },
}

EXPECTED_B_OPEN_BASES = {
    0: (
        z**2 + z / 8 + sp.Rational(1, 128),
        a - 1,
        q - 16 * z - 2,
        B + 8 * z,
        t + sp.Rational(240, 17) * z + sp.Rational(7, 17),
    ),
    1: (
        z**2 + sp.Rational(1, 64),
        a + 8 * z - 1,
        q + 8 * z,
        B + sp.Rational(1, 2),
        t - sp.Rational(40, 13) * z + sp.Rational(12, 13),
    ),
}
EXPECTED_P1_T3_REMAINDER = -sp.Rational(2048, 13) * z - sp.Rational(384, 13)
P0_RANK_WITNESS_ROWS = (0, 1, 2, 17, 25, 28, 32)
P0_RANK_WITNESS_COLUMNS = (0, 1, 2, 3, 4, 5, 6)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def q6_expression(p_value=p, q_value=q):
    return (
        2 * p_value**4 * q_value**2 - 2 * p_value**4 * q_value + p_value**4
        + 2 * p_value**3 * q_value**3 - 7 * p_value**3 * q_value**2
        + 5 * p_value**3 * q_value - 2 * p_value**3
        + 2 * p_value**2 * q_value**4 - 7 * p_value**2 * q_value**3
        + 12 * p_value**2 * q_value**2 - 7 * p_value**2 * q_value
        + 2 * p_value**2 - 2 * p_value * q_value**4
        + 5 * p_value * q_value**3 - 7 * p_value * q_value**2
        + 2 * p_value * q_value + q_value**4 - 2 * q_value**3
        + 2 * q_value**2
    )


def delta_expression(p_value=p, q_value=q):
    return sp.expand(
        (p_value - q_value)
        * (p_value + q_value - 1)
        * (p_value**2 - p_value + 1)
        * (p_value**2 + 2 * p_value * q_value - 2 * p_value - q_value)
        * (2 * p_value * q_value - p_value + q_value**2 - 2 * q_value)
        * (
            2 * p_value * q_value**2
            - 2 * p_value * q_value
            - p_value
            - q_value**2
            - 2 * q_value
            + 2
        )
    )


class BC:
    """Sparse polynomial in B,C with coefficients in QQ(p,q,a)."""

    def __init__(self, terms=None):
        self.terms = {
            tuple(exponent): value
            for exponent, value in (terms or {}).items()
            if value != K.zero
        }

    @classmethod
    def const(cls, value):
        if not isinstance(value, FIELD_ELEMENT_TYPE):
            value = K.from_sympy(sp.cancel(sp.sympify(value)))
        return cls({(0, 0): value})

    @classmethod
    def var(cls, exponent):
        return cls({tuple(exponent): K.one})

    def __add__(self, other):
        output = dict(self.terms)
        for exponent, value in other.terms.items():
            updated = output.get(exponent, K.zero) + value
            if updated == K.zero:
                output.pop(exponent, None)
            else:
                output[exponent] = updated
        return BC(output)

    def __neg__(self):
        return BC({exponent: -value for exponent, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        output = {}
        for (bi, ci), left in self.terms.items():
            for (bj, cj), right in other.terms.items():
                exponent = (bi + bj, ci + cj)
                updated = output.get(exponent, K.zero) + left * right
                if updated == K.zero:
                    output.pop(exponent, None)
                else:
                    output[exponent] = updated
        return BC(output)


def sparse_determinant(matrix: list[list[BC]], label: str) -> BC:
    states = {0: BC.const(1)}
    size = len(matrix)
    for row_index, row in enumerate(matrix):
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                term = value * entry
                inversions = sum(
                    1 for prior in range(column) if not mask & (1 << prior)
                )
                if inversions & 1:
                    term = -term
                new_mask = mask | (1 << column)
                following[new_mask] = (
                    term
                    if new_mask not in following
                    else following[new_mask] + term
                )
        states = following
        print(
            f"[GLD102 primary] {label} row={row_index + 1}/{size} states={len(states)}",
            file=sys.stderr,
            flush=True,
        )
    return states.get((1 << size) - 1, BC.const(0))


def support_digest(gld71) -> str:
    payload = [
        [
            row,
            [
                [list(indices), coefficient]
                for indices, coefficient in gld71.SPARSE_RELATIONS[row]
            ],
        ]
        for row in SUPPORT_ROWS
    ]
    return sha256_bytes(json.dumps(payload, separators=(",", ":")).encode())


def build_raw_minors(gld71, gld88) -> dict[str, BC]:
    family = gld88.h4_family(p, q, a)
    leaves = [
        [BC.const(1), BC.const(1), BC.const(1)],
        [BC.const(p), BC.const(q), BC.const(family["s"])],
        [
            BC.const(a),
            BC.const(1 + family["b"]) + BC.var((1, 0)),
            BC.const(1 + family["c"]) + BC.var((0, 1)),
        ],
    ]
    rows = {}
    for row in SUPPORT_ROWS:
        entries = []
        for root in range(3):
            for component in range(3):
                value = BC.const(0)
                for indices, coefficient in gld71.SPARSE_RELATIONS[row]:
                    if indices[0] != root:
                        continue
                    term = (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                    value = value + BC.const(coefficient) * term
                entries.append(value)
        rows[row] = entries

    minors = {}
    for name, (rowset, columns) in SELECTORS.items():
        matrix = [[rows[row][column] for column in columns] for row in rowset]
        minor = sparse_determinant(matrix, name)
        if (0, 0) in minor.terms:
            raise AssertionError(f"{name} has a nonzero offset constant")
        if not set(minor.terms).issubset(EXPECTED_OFFSET_SUPPORT):
            raise AssertionError((name, sorted(minor.terms)))
        minors[name] = minor
    return minors


def primitive_numerator(expression, variables, delta_value):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    denominator_poly = sp.Poly(denominator, *variables, domain=QQ)
    delta_poly = sp.Poly(delta_value, *variables, domain=QQ)
    factors = []
    _content, factorization = sp.factor_list(denominator_poly.as_expr())
    for factor, multiplicity in factorization:
        factor_poly = sp.Poly(factor, *variables, domain=QQ)
        common = sp.gcd(delta_poly, factor_poly)
        if common.monic() != factor_poly.monic():
            raise AssertionError(
                ("denominator factor outside Delta", factor, multiplicity)
            )
        factors.append((str(factor), int(multiplicity)))
    polynomial = sp.Poly(sp.expand(numerator), *variables, domain=QQ)
    _rational_content, primitive = polynomial.primitive()
    primitive = primitive.clear_denoms(convert=True)[1]
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive.as_expr(), factors


def canonical_polynomial_hash(expression, variables) -> str:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=QQ)
    encoded = [
        [list(monomial), int(coefficient.p), int(coefficient.q)]
        for monomial, coefficient in polynomial.terms()
    ]
    return sha256_bytes(json.dumps(encoded, separators=(",", ":")).encode("ascii"))


def case_equations(minors: dict[str, BC], p_value: int):
    delta_value = sp.factor(delta_expression(sp.Integer(p_value), q))
    b_open = {}
    c_open = {}
    metadata = {"B_open": {}, "C_open": {}}
    for name, minor in minors.items():
        b_terms = []
        for (b_exponent, c_exponent), coefficient in minor.terms.items():
            specialized = sp.cancel(
                sp.sympify(coefficient.as_expr()).subs(p, p_value)
            )
            if specialized.has(sp.zoo, sp.nan):
                raise AssertionError((p_value, name, "undefined specialization"))
            total_offset_degree = b_exponent + c_exponent
            if total_offset_degree < 1 or c_exponent not in (0, 1):
                raise AssertionError((name, b_exponent, c_exponent))
            b_terms.append(
                specialized
                * B ** (total_offset_degree - 1)
                * t**c_exponent
            )
        b_expression, b_factors = primitive_numerator(
            sum(b_terms, sp.Integer(0)),
            (a, q, B, t),
            delta_value,
        )
        b_hash = canonical_polynomial_hash(b_expression, (a, q, B, t))
        if b_hash != EXPECTED_B_OPEN_HASHES[p_value][name]:
            raise AssertionError((p_value, "B", name, b_hash))
        b_open[name] = b_expression
        metadata["B_open"][name] = {
            "sha256": b_hash,
            "terms": len(sp.Poly(b_expression, a, q, B, t, domain=QQ).terms()),
            "denominator_factors": b_factors,
        }

        coefficient = minor.terms.get((0, 1), K.zero)
        c_expression, c_factors = primitive_numerator(
            sp.sympify(coefficient.as_expr()).subs(p, p_value),
            (a, q),
            delta_value,
        )
        c_hash = canonical_polynomial_hash(c_expression, (a, q))
        if c_hash != EXPECTED_C_OPEN_HASHES[p_value][name]:
            raise AssertionError((p_value, "C", name, c_hash))
        c_open[name] = c_expression
        metadata["C_open"][name] = {
            "sha256": c_hash,
            "terms": len(sp.Poly(c_expression, a, q, domain=QQ).terms()),
            "denominator_factors": c_factors,
        }
    return b_open, c_open, metadata, delta_value


def normalized_basis(basis) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(polynomial.monic().as_expr()) for polynomial in basis.polys)


def basis_digest(expressions) -> str:
    return sha256_bytes(
        "\n".join(sp.srepr(sp.expand(expression)) for expression in expressions).encode()
    )


def build_full_syndrome(gld71, gld88, substitution):
    p_value = substitution[p]
    q_value = substitution[q]
    a_value = substitution[a]
    b_offset = substitution[B]
    c_offset = substitution[C]
    family = gld88.h4_family(p_value, q_value, a_value)
    leaf = [
        [sp.Integer(1), sp.Integer(1), sp.Integer(1)],
        [p_value, q_value, sp.cancel(family["s"])],
        [
            a_value,
            sp.cancel(1 + family["b"] + b_offset),
            sp.cancel(1 + family["c"] + c_offset),
        ],
    ]
    rows = []
    for relation in gld71.SPARSE_RELATIONS:
        entries = []
        for root in range(3):
            for component in range(3):
                total = sp.Integer(0)
                for indices, coefficient in relation:
                    if indices[0] == root:
                        total += (
                            coefficient
                            * leaf[indices[1]][component]
                            * leaf[indices[2]][component]
                            * leaf[indices[3]][component]
                        )
                entries.append(sp.simplify(total))
        rows.append(entries)
    return sp.Matrix(rows)


def p0_survivor_checks(gld71, gld88, delta_value):
    reports = []
    for epsilon in (-1, 1):
        i_value = sp.I
        z_value = (-1 + epsilon * i_value) / 16
        q_value = 1 + epsilon * i_value
        b_offset = (1 - epsilon * i_value) / 2
        ratio = (8 - 15 * epsilon * i_value) / 17
        c_offset = sp.simplify(b_offset * ratio)
        substitution = {
            p: sp.Integer(0),
            q: q_value,
            a: sp.Integer(1),
            B: b_offset,
            C: c_offset,
            t: ratio,
            z: z_value,
        }
        if sp.simplify(q6_expression(0, q_value)) != 0:
            raise AssertionError((epsilon, "Q6"))
        delta_at_point = sp.simplify(delta_value.subs(q, q_value))
        if delta_at_point == 0:
            raise AssertionError((epsilon, "Delta"))
        syndrome = build_full_syndrome(gld71, gld88, substitution)
        selected = {}
        for name, (rows, columns) in SELECTORS.items():
            determinant = sp.simplify(syndrome.extract(rows, columns).det())
            if determinant != 0:
                raise AssertionError((epsilon, name, determinant))
            selected[name] = str(determinant)
        witness = sp.simplify(
            syndrome.extract(P0_RANK_WITNESS_ROWS, P0_RANK_WITNESS_COLUMNS).det()
        )
        expected = sp.Rational(-29952, 289) + epsilon * sp.Rational(28416, 289) * sp.I
        if sp.simplify(witness - expected) != 0 or witness == 0:
            raise AssertionError((epsilon, witness, expected))
        reports.append(
            {
                "epsilon": epsilon,
                "point": {
                    "a": str(substitution[a]),
                    "q": str(q_value),
                    "B": str(b_offset),
                    "C": str(c_offset),
                    "t": str(ratio),
                    "z": str(z_value),
                },
                "Delta": str(delta_at_point),
                "selected_minors": selected,
                "rank_at_least_seven_witness": {
                    "rows": list(P0_RANK_WITNESS_ROWS),
                    "columns": list(P0_RANK_WITNESS_COLUMNS),
                    "determinant": str(witness),
                },
            }
        )
    return reports


def check() -> dict[str, object]:
    started = time.monotonic()
    for path, expected in EXPECTED_SOURCE_LF_SHA256.items():
        observed = lf_sha256(path)
        if observed != expected:
            raise AssertionError((path, observed, expected))
    gld71 = load_module(GLD71, "gld71_for_gld102_primary")
    gld88 = load_module(GLD88, "gld88_for_gld102_primary")
    if support_digest(gld71) != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError("GLD71 support digest changed")

    raw_minors = build_raw_minors(gld71, gld88)
    cases = {}
    for p_value in (0, 1):
        print(f"[GLD102 primary] specializing p={p_value}", flush=True)
        b_open, c_open, metadata, delta_value = case_equations(
            raw_minors, p_value
        )
        q6_value = sp.Poly(q6_expression(p_value, q), q, domain=QQ).monic().as_expr()
        b_generators = [
            q6_value,
            *(b_open[name] for name in BASE_SELECTOR_NAMES),
            z * B * delta_value - 1,
        ]
        b_basis = sp.groebner(
            b_generators,
            a,
            q,
            B,
            t,
            z,
            order="grevlex",
            domain=QQ,
        )
        actual_basis = normalized_basis(b_basis)
        expected_basis = tuple(
            sp.expand(sp.Poly(value, a, q, B, t, z, domain=QQ).monic().as_expr())
            for value in EXPECTED_B_OPEN_BASES[p_value]
        )
        if actual_basis != expected_basis:
            raise AssertionError(
                {"p": p_value, "actual": actual_basis, "expected": expected_basis}
            )
        t3_remainder = sp.expand(b_basis.reduce(b_open["T3"])[1])
        if p_value == 0:
            if t3_remainder != 0:
                raise AssertionError((p_value, "T3 remainder", t3_remainder))
            survivor_report = p0_survivor_checks(gld71, gld88, delta_value)
            b_open_conclusion = "two selected-zero points, both rank at least seven"
        else:
            if sp.expand(t3_remainder - EXPECTED_P1_T3_REMAINDER) != 0:
                raise AssertionError((p_value, "T3 remainder", t3_remainder))
            quadratic = sp.Poly(actual_basis[0], z, domain=QQ)
            remainder_polynomial = sp.Poly(t3_remainder, z, domain=QQ)
            if sp.gcd(quadratic, remainder_polynomial).degree() != 0:
                raise AssertionError("p=1 T3 remainder meets the residual quadratic")
            survivor_report = []
            b_open_conclusion = "empty after the sixth selected minor"

        c_generators = [
            q6_value,
            *(c_open[name] for name in SELECTOR_NAMES),
            z * delta_value - 1,
        ]
        c_basis = sp.groebner(
            c_generators,
            a,
            q,
            z,
            order="grevlex",
            domain=QQ,
        )
        if len(c_basis.polys) != 1 or c_basis.polys[0].monic().as_expr() != 1:
            raise AssertionError((p_value, "C-open basis", c_basis))

        cases[f"p{p_value}"] = {
            "Q6": str(q6_value),
            "Delta": str(delta_value),
            "H2": str(2 * p_value**2 - 2 * p_value + 1),
            "equations": metadata,
            "B_open": {
                "five_selector_basis": [str(value) for value in actual_basis],
                "basis_srepr_sha256": basis_digest(actual_basis),
                "T3_remainder": str(t3_remainder),
                "conclusion": b_open_conclusion,
                "survivor_checks": survivor_report,
            },
            "B0_C_open": {
                "basis": ["1"],
                "unit": True,
                "division": (
                    "each selected minor is C times the recorded coefficient; "
                    "C is nonzero on this chart"
                ),
            },
        }

    return {
        "status": "proved_exact_scoped_p01_nonzero_offset_exclusion",
        "claim_id": "GLD102",
        "global_conjecture": "UNRESOLVED",
        "scope": (
            "characteristic zero, normalized GLD88 H4/Q6 offset chart, "
            "p in {0,1}, arbitrary a, D(Delta); rank(M)<=6 implies B=C=0"
        ),
        "rank_to_selector_direction_only": True,
        "nonclaims": [
            "the endpoint B=C=0 is not excluded",
            "no physical incidence or D(Omega) conclusion is asserted",
            "arbitrary p, the full E31 wall, other charts, Fitting, and global gluing remain open",
            "the global Krenn-Gu conjecture remains UNRESOLVED",
        ],
        "runtime_environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "source_lf_sha256": {
            str(path.relative_to(ROOT)): expected
            for path, expected in EXPECTED_SOURCE_LF_SHA256.items()
        },
        "support_digest_sha256": EXPECTED_SUPPORT_DIGEST,
        "selectors": {
            name: {"rows": list(rows), "columns": list(columns)}
            for name, (rows, columns) in SELECTORS.items()
        },
        "offset_cover": ["D(B)", "V(B) intersect D(C)"],
        "cases": cases,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("GLD102 p=0,1 nonzero-offset exclusion verifier: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
