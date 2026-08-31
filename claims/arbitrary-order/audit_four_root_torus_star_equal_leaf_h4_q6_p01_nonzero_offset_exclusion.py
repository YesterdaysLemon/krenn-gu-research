#!/usr/bin/env python3
"""Independent exact audit of the GLD102 p=0,1 offset implication.

This audit imports no project verifier or chart builder.  It copies only the
immutable GLD71 sparse supports used by the six named seven-minors, locally
transcribes the GLD88/F88 H4 chart, specializes each of the two offset charts
before taking direct exact matrix determinants, and recomputes the ideals.

The accepted conclusion is only that, in characteristic zero on the written
normalized H4/Q6 chart and D(Delta), p in {0,1} and rank(M)<=6 imply B=C=0.
The endpoint, physical incidence, arbitrary p, other charts, and the global
Krenn--Gu conjecture remain outside scope.  The global status is UNRESOLVED.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time

import sympy as sp
from sympy import QQ


a, q, B, C, t, z = sp.symbols("a q B C t z")

# Immutable GLD71 sparse relation supports used by the displayed minors.
# Each entry is ((root, leaf_1, leaf_2, leaf_3), coefficient).
PINNED_RELATIONS = {
    0: (((1, 1, 1, 1), 1),),
    1: (((0, 0, 0, 0), 1),),
    2: (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    17: (
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 0), -1),
        ((1, 0, 0, 0), -1),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
    ),
    25: (
        ((1, 1, 0, 0), 1),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 2, 0, 0), -1),
        ((1, 2, 0, 1), 1),
        ((1, 2, 1, 0), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 1), 1),
        ((2, 1, 1, 0), 1),
        ((2, 2, 0, 0), 1),
        ((2, 2, 0, 1), -1),
        ((2, 2, 1, 0), -1),
    ),
    28: (
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 2), -1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 2), -1),
        ((0, 1, 1, 0), -1),
        ((0, 1, 1, 2), 1),
        ((2, 0, 1, 0), -1),
        ((2, 0, 1, 2), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 2), 1),
        ((2, 1, 1, 0), 1),
        ((2, 1, 1, 2), -1),
    ),
    31: (
        ((1, 0, 0, 0), 8),
        ((1, 0, 0, 1), -4),
        ((1, 0, 1, 0), -4),
        ((1, 0, 1, 1), 2),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 1, 1, 2), 3),
        ((1, 1, 2, 1), 3),
        ((1, 2, 0, 0), -12),
        ((1, 2, 0, 1), 6),
        ((1, 2, 1, 0), 6),
        ((2, 1, 1, 1), 6),
    ),
    32: (
        ((0, 0, 0, 1), 1),
        ((0, 0, 0, 2), -3),
        ((0, 0, 1, 0), -2),
        ((0, 0, 1, 1), 4),
        ((0, 0, 2, 1), -6),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 1), -2),
        ((0, 1, 1, 0), 4),
        ((0, 1, 1, 1), -8),
        ((0, 1, 2, 0), -6),
        ((0, 1, 2, 1), 12),
        ((0, 2, 0, 0), -3),
        ((2, 0, 0, 0), -6),
    ),
    33: (
        ((1, 0, 0, 0), 4),
        ((1, 0, 0, 1), -8),
        ((1, 0, 1, 0), -2),
        ((1, 0, 1, 1), 1),
        ((1, 0, 1, 2), 6),
        ((1, 1, 0, 0), -2),
        ((1, 1, 0, 1), 13),
        ((1, 1, 0, 2), -6),
        ((1, 1, 1, 0), -2),
        ((1, 1, 1, 2), -6),
        ((1, 1, 2, 1), 3),
        ((1, 2, 1, 1), 3),
        ((2, 0, 0, 1), 12),
        ((2, 1, 0, 1), -12),
    ),
}
SUPPORT_ROWS = tuple(sorted(PINNED_RELATIONS))

SELECTORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
BASE_SELECTOR_NAMES = ("T0", "T1", "T2", "Y1", "X3")

EXPECTED_SUPPORT_DIGEST = (
    "f2670c9393287eae16dce1bc8aa41e4b0c421645833ad29619a6d7b6fd94ac07"
)
EXPECTED_HASHES = {
    0: {
        "B": {
            "T0": "6698570ba9b983a03eb59e9bf33516dacd34806ebee1b49affb8cf10bd791bad",
            "T1": "c946ddf2793058f6c374230b7a11b997c34a5f930980f38e99f64eb3989b9f47",
            "T2": "eb247f55987cf51ac3056eb3b6b592155f5d7f38e42638f26ed864b644d36d0b",
            "T3": "50ea1f5f1f99449f97d083171a1c19379d610c7028fd6aec509504a6b725126f",
            "Y1": "f58c27e889af1743689fbac7508212ce232d5ea9f627625fc5cd08d09d947cc8",
            "X3": "bec33400e8a096f815fc2313bf8c79730192b6b0aa07be6863247f6d0748436f",
        },
        "C": {
            "T0": "6f5db0d7e894c8dccee64b38e57ca831cbe36abdfbcd9dbf3e1949d4678db44a",
            "T1": "ee90b3a38619597c81ef424da576efb196d4370e5cc6bc5d6df6e7117549147d",
            "T2": "21ccb7e208b186ad567b01d474d544cf5188787b25505ae2ee9a18b2d6d0a88a",
            "T3": "1f12748b26196289948f9fdcade5f1378085294db2b646159f7174dfc5d70054",
            "Y1": "1c4ca6991ea9cf416bc16aac62ed24d209161a4694d5618b43bc0e9b48ccd2e9",
            "X3": "1c866717a84aa6efa9eb1a0c8e445e980ca6f26148f24c4be27e6e18c2a81831",
        },
    },
    1: {
        "B": {
            "T0": "0ef9b6e45dfe83211b11257929815cdef76de590e58171e698ed876c6abdd75a",
            "T1": "3c78c42206d3649f2b6206a4745dad2ad2284c3241a7e76ab25148d0a02d6f67",
            "T2": "f749ac6c9baf18f561550a0c11c8ce491aee07a38dfa4b4d211b11e3427688f4",
            "T3": "d52b7380f8724c57c9628e26340bb30235970d599bcd2669cdedd08624bb8893",
            "Y1": "635d8d441511e8685ec961569f55021521d1489da199c53a795490936ddaf481",
            "X3": "71c0db85421a3ec2e5243fbdfb60b4b35059704b70a663a6e98060c425abfc05",
        },
        "C": {
            "T0": "c80794afcf47d3c2531ad978736f07abaee4170dc48cd12a88ab3d1028de3e2b",
            "T1": "c4aea8a643fcba39845ffb2d0604de0ad84c7c5f8ddd956fb07e1f4b83750876",
            "T2": "900cafb2918de28db8c5188d0935251c662f88d3c46122543464167af232d74c",
            "T3": "dae01bb49c4ea2b669ab9a331c578aa4084ac0e83b530887ceb095bdda0cef4d",
            "Y1": "f3d6843358ed572dbddeaba098cd7061fc270c1138a113d020d83da1bd1ce65a",
            "X3": "e563ef704fbedbacdaa08ba0e94797604d3446519bcc428c07284f36372c2425",
        },
    },
}
EXPECTED_BASES = {
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


def canonical_support_digest() -> str:
    payload = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in PINNED_RELATIONS[row]],
        ]
        for row in SUPPORT_ROWS
    ]
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()


def h4_family(p_value, q_value, a_value):
    d0 = p_value + q_value - 1
    e = (
        2 * p_value * q_value**2
        - 2 * p_value * q_value
        - p_value
        - q_value**2
        - 2 * q_value
        + 2
    )
    nb = (
        -2 * a_value * p_value**2 * q_value**3
        + 3 * a_value * p_value**2 * q_value**2
        - 3 * a_value * p_value**2 * q_value
        + a_value * p_value**2
        + 2 * a_value * p_value * q_value**3
        + 2 * a_value * p_value
        + a_value * q_value**3
        - 3 * a_value * q_value**2
        + 3 * a_value * q_value
        - 2 * a_value
        + p_value**3 * q_value**2
        - p_value**3
        + p_value**2 * q_value**3
        - 3 * p_value**2 * q_value**2
        + p_value**2
        - 2 * p_value * q_value**3
        + 3 * p_value * q_value**2
        - 2 * p_value
        + q_value**2
        - 3 * q_value
        + 2
    )
    nc = (
        2 * a_value * p_value * q_value**3
        - 3 * a_value * p_value * q_value**2
        + 3 * a_value * p_value * q_value
        - a_value * p_value
        - a_value * q_value**3
        + 3 * a_value * q_value**2
        - 3 * a_value * q_value
        + 2 * a_value
        + p_value**2 * q_value**2
        - 2 * p_value**2 * q_value
        - 3 * p_value * q_value**2
        + p_value * q_value
        + p_value
        - q_value**2
        + 3 * q_value
        - 2
    )
    return {
        "s": sp.cancel((p_value + q_value - p_value * q_value) / d0),
        "b": sp.cancel(-nb / ((p_value**2 - p_value + 1) * e)),
        "c": sp.cancel(-nc / (d0 * e)),
    }


def q6(p_value, q_value):
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


def delta(p_value, q_value):
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


def direct_rows(leaf, rows=SUPPORT_ROWS):
    return {
        row: [
            sp.expand(
                sum(
                    coefficient
                    * leaf[indices[1]][component]
                    * leaf[indices[2]][component]
                    * leaf[indices[3]][component]
                    for indices, coefficient in PINNED_RELATIONS[row]
                    if indices[0] == root
                )
            )
            for root in range(3)
            for component in range(3)
        ]
        for row in rows
    }


def primitive_numerator(expression, variables, delta_value):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    denominator_poly = sp.Poly(denominator, *variables, domain=QQ)
    delta_poly = sp.Poly(delta_value, *variables, domain=QQ)
    for factor, multiplicity in sp.factor_list(denominator_poly.as_expr())[1]:
        factor_poly = sp.Poly(factor, *variables, domain=QQ)
        if sp.gcd(delta_poly, factor_poly).monic() != factor_poly.monic():
            raise AssertionError((factor, multiplicity, "outside Delta"))
    polynomial = sp.Poly(sp.expand(numerator), *variables, domain=QQ)
    _content, primitive = polynomial.primitive()
    primitive = primitive.clear_denoms(convert=True)[1]
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive.as_expr()


def polynomial_hash(expression, variables):
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=QQ)
    encoded = [
        [list(monomial), int(coefficient.p), int(coefficient.q)]
        for monomial, coefficient in polynomial.terms()
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def chart_equations(p_value, chart):
    family = h4_family(sp.Integer(p_value), q, a)
    if chart == "B":
        third = [a, 1 + family["b"] + B, 1 + family["c"] + B * t]
        variables = (a, q, B, t)
        divisor = B
    elif chart == "C":
        third = [a, 1 + family["b"], 1 + family["c"] + C]
        variables = (a, q)
        divisor = C
    else:
        raise ValueError(chart)
    leaf = [[1, 1, 1], [sp.Integer(p_value), q, family["s"]], third]
    rows = direct_rows(leaf)
    delta_value = sp.factor(delta(p_value, q))
    equations = {}
    metadata = {}
    for name, (rowset, columns) in SELECTORS.items():
        print(f"[GLD102 audit] p={p_value} chart={chart} determinant {name}", flush=True)
        matrix = sp.Matrix([[rows[row][column] for column in columns] for row in rowset])
        determinant = sp.cancel(matrix.det(method="domain-ge"))
        divided = sp.cancel(determinant / divisor)
        if sp.cancel(determinant - divisor * divided) != 0:
            raise AssertionError((p_value, chart, name, "division failed"))
        equation = primitive_numerator(divided, variables, delta_value)
        digest = polynomial_hash(equation, variables)
        if digest != EXPECTED_HASHES[p_value][chart][name]:
            raise AssertionError((p_value, chart, name, digest))
        equations[name] = equation
        metadata[name] = {
            "sha256": digest,
            "terms": len(sp.Poly(equation, *variables, domain=QQ).terms()),
        }
    return equations, delta_value


def normalized_basis(basis):
    return tuple(sp.expand(polynomial.monic().as_expr()) for polynomial in basis.polys)


def rank_witness(p_value, epsilon):
    if p_value != 0:
        raise ValueError(p_value)
    q_value = 1 + epsilon * sp.I
    b_offset = (1 - epsilon * sp.I) / 2
    ratio = (8 - 15 * epsilon * sp.I) / 17
    c_offset = sp.simplify(b_offset * ratio)
    family = h4_family(0, q_value, 1)
    leaf = [
        [1, 1, 1],
        [0, q_value, family["s"]],
        [1, 1 + family["b"] + b_offset, 1 + family["c"] + c_offset],
    ]
    rows = direct_rows(leaf)
    for name, (rowset, columns) in SELECTORS.items():
        determinant = sp.simplify(
            sp.Matrix([[rows[row][column] for column in columns] for row in rowset]).det()
        )
        if determinant != 0:
            raise AssertionError((epsilon, name, determinant))
    witness_rows = (0, 1, 2, 17, 25, 28, 32)
    witness_columns = (0, 1, 2, 3, 4, 5, 6)
    witness = sp.simplify(
        sp.Matrix(
            [[rows[row][column] for column in witness_columns] for row in witness_rows]
        ).det()
    )
    expected = sp.Rational(-29952, 289) + epsilon * sp.Rational(28416, 289) * sp.I
    if sp.simplify(witness - expected) != 0 or witness == 0:
        raise AssertionError((epsilon, witness, expected))
    return {
        "epsilon": epsilon,
        "q": str(q_value),
        "B": str(b_offset),
        "C": str(c_offset),
        "rank_at_least_seven_determinant": str(witness),
    }


def check():
    started = time.monotonic()
    if canonical_support_digest() != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError("pinned support digest changed")
    cases = {}
    for p_value in (0, 1):
        b_equations, delta_value = chart_equations(p_value, "B")
        c_equations, c_delta = chart_equations(p_value, "C")
        if sp.expand(delta_value - c_delta) != 0:
            raise AssertionError((p_value, "Delta mismatch"))
        q6_value = sp.Poly(q6(p_value, q), q, domain=QQ).monic().as_expr()

        b_basis = sp.groebner(
            [
                q6_value,
                *(b_equations[name] for name in BASE_SELECTOR_NAMES),
                z * B * delta_value - 1,
            ],
            a,
            q,
            B,
            t,
            z,
            order="grevlex",
            domain=QQ,
        )
        actual = normalized_basis(b_basis)
        expected = tuple(
            sp.expand(sp.Poly(value, a, q, B, t, z, domain=QQ).monic().as_expr())
            for value in EXPECTED_BASES[p_value]
        )
        if actual != expected:
            raise AssertionError((p_value, actual, expected))
        t3_remainder = sp.expand(b_basis.reduce(b_equations["T3"])[1])
        if p_value == 0:
            if t3_remainder != 0:
                raise AssertionError((p_value, t3_remainder))
            survivors = [rank_witness(0, epsilon) for epsilon in (-1, 1)]
            b_conclusion = "two selected-zero points independently excluded by rank-seven witnesses"
        else:
            expected_remainder = -sp.Rational(2048, 13) * z - sp.Rational(384, 13)
            if sp.expand(t3_remainder - expected_remainder) != 0:
                raise AssertionError((p_value, t3_remainder))
            if sp.gcd(
                sp.Poly(actual[0], z, domain=QQ),
                sp.Poly(t3_remainder, z, domain=QQ),
            ).degree() != 0:
                raise AssertionError("p=1 residual meets T3")
            survivors = []
            b_conclusion = "empty after T3"

        c_basis = sp.groebner(
            [q6_value, *c_equations.values(), z * delta_value - 1],
            a,
            q,
            z,
            order="grevlex",
            domain=QQ,
        )
        if len(c_basis.polys) != 1 or c_basis.polys[0].monic().as_expr() != 1:
            raise AssertionError((p_value, "C-open", c_basis))
        cases[f"p{p_value}"] = {
            "B_open_basis": [str(value) for value in actual],
            "T3_remainder": str(t3_remainder),
            "B_open_conclusion": b_conclusion,
            "survivor_checks": survivors,
            "B0_C_open_unit": True,
            "equation_hashes": EXPECTED_HASHES[p_value],
        }

    return {
        "status": "independent_exact_GLD102_audit",
        "global_conjecture": "UNRESOLVED",
        "scope": (
            "normalized GLD88 H4/Q6 chart, characteristic zero, p in {0,1}, "
            "arbitrary a, D(Delta); rank(M)<=6 implies B=C=0"
        ),
        "imports_project_verifiers": False,
        "construction": (
            "copied immutable sparse supports, local H4/F88 transcription, "
            "chart-first direct exact matrix determinants"
        ),
        "rank_to_selector_direction_only": True,
        "support_digest_sha256": EXPECTED_SUPPORT_DIGEST,
        "cases": cases,
        "nonclaims": [
            "B=C=0 endpoint exclusion",
            "physical incidence emptiness",
            "arbitrary p or full E31 wall closure",
            "other charts, Fitting, source integrability, or global gluing",
            "resolution of the global Krenn-Gu conjecture",
        ],
        "runtime_environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main():
    result = check()
    print("independent GLD102 p=0,1 nonzero-offset audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
