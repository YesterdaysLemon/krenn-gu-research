#!/usr/bin/env python3
"""Independent exact audit of the strengthened GLD96 R31-free witness.

This audit intentionally does not import the GLD96 primary or GLD88.  It reads
only the pinned sparse relation supports from GLD71, rebuilds each syndrome
entry by a direct support loop, and obtains the four residuals as bordered
determinants (the primary uses an adjugate/Schur computation).  The Q6
reduction, resultant, and norm checks are then replayed independently.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)

ROWS = (0, 1, 2, 17, 25, 31)
COLUMNS = (0, 1, 3, 4, 6, 7)
TARGETS = ((28, 8), (32, 2), (32, 5), (33, 8))
EXPECTED_RESULTANT_COEFFICIENTS = (
    -905501121543829653519134583029125628170363723798877745648523367180968018033574358187,
    -581967626061819630034063550351650331374757486676325140922444735277204122667234925864,
    1965327315048008656313355784299314970407615267446169045708659903094610123987480161652,
    -1135825891000896384111550023303077198001706298129393658672106278421500353284383698011,
)
EXPECTED_RESULTANT_TUPLE_SHA256 = (
    "f0b2368dda1ea6a89d31ccf98242f48ed5d3540a14d412393b7870719780a05b"
)
EXPECTED_RESULTANT_NORM_FACTORS = {
    3: 6,
    5: 282,
    31: 2,
    173: 2,
    269: 1,
    1709: 1,
    20357: 2,
    270217: 2,
    52321: 1,
    475485394682070314208533: 1,
}
EXPECTED_G0 = (
    -sp.Integer(152501184) * sp.Symbol("q") ** 3
    + sp.Integer(255629952) * sp.Symbol("q") ** 2
    - sp.Integer(158823936) * sp.Symbol("q")
    + sp.Integer(30786048)
) / 3125
EXPECTED_G0_NORM_FACTORS = {2: 33, 3: 16, 5: 14, 110281: 1}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def family(p: sp.Expr, q: sp.Expr, a: sp.Expr) -> dict[str, sp.Expr]:
    """Local transcription of the written F88 formula (no GLD88 import)."""

    d0 = p + q - 1
    P = p**2 - p + 1
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    nb = (
        -2 * a * p**2 * q**3
        + 3 * a * p**2 * q**2
        - 3 * a * p**2 * q
        + a * p**2
        + 2 * a * p * q**3
        + 2 * a * p
        + a * q**3
        - 3 * a * q**2
        + 3 * a * q
        - 2 * a
        + p**3 * q**2
        - p**3
        + p**2 * q**3
        - 3 * p**2 * q**2
        + p**2
        - 2 * p * q**3
        + 3 * p * q**2
        - 2 * p
        + q**2
        - 3 * q
        + 2
    )
    nc = (
        2 * a * p * q**3
        - 3 * a * p * q**2
        + 3 * a * p * q
        - a * p
        - a * q**3
        + 3 * a * q**2
        - 3 * a * q
        + 2 * a
        + p**2 * q**2
        - 2 * p**2 * q
        - 3 * p * q**2
        + p * q
        + p
        - q**2
        + 3 * q
        - 2
    )
    return {
        "s": (p + q - p * q) / d0,
        "b": -nb / (P * e),
        "c": -nc / (d0 * e),
    }


def q6_polynomial(p: sp.Expr, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


def q_reduce(value: sp.Expr, q: sp.Symbol, modulus: sp.Poly) -> sp.Expr:
    numerator, denominator = sp.cancel(value).as_numer_denom()
    numerator_poly = sp.Poly(numerator, q, domain=QQ).rem(modulus)
    denominator_poly = sp.Poly(denominator, q, domain=QQ).rem(modulus)
    assert not denominator_poly.is_zero
    return sp.cancel(
        (numerator_poly * sp.invert(denominator_poly, modulus)).rem(modulus).as_expr()
    )


def polynomial_determinant(matrix: sp.Matrix, B: sp.Symbol, C: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    """Bareiss determinant in Q(q)[B,C], keeping B,C out of denominators."""

    domain = QQ.frac_field(q)
    work = [
        [sp.Poly(sp.cancel(matrix[row, column]), B, C, domain=domain)
         for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]
    previous = sp.Poly(1, B, C, domain=domain)
    sign = 1
    size = len(work)
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size) if not work[row][pivot_index].is_zero),
            None,
        )
        assert pivot_row is not None, "zero determinant encountered in audit pivot"
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            left = work[row][pivot_index]
            for column in range(pivot_index + 1, size):
                value = work[row][column] * pivot - left * work[pivot_index][column]
                work[row][column] = value.exquo(previous)
            work[row][pivot_index] = sp.Poly(0, B, C, domain=domain)
        previous = pivot
    result = work[-1][-1]
    if sign < 0:
        result = -result
    return result.as_expr()


def direct_matrix(gld71, parent, supports, leaves):
    """Build M by direct sparse support accumulation, not coefficient_matrix."""

    support_maps = [dict(support) for support in supports]
    matrix_rows = []
    for support in support_maps:
        row = []
        for root in range(3):
            for component in range(3):
                total = 0
                for (support_root, i, j, k), coefficient in support.items():
                    if support_root == root:
                        total += (
                            coefficient
                            * leaves[0][i, component]
                            * leaves[1][j, component]
                            * leaves[2][k, component]
                        )
                row.append(sp.expand(total))
        matrix_rows.append(row)
    return sp.Matrix(matrix_rows)


def check() -> dict[str, object]:
    started = time.monotonic()
    gld71 = load_module(GLD71, "gld71_for_gld96_audit")
    parent = gld71.load_parent()
    supports = gld71.SPARSE_RELATIONS
    assert len(supports) == 37
    p, q, a, B, C = sp.symbols("p q a B C")
    f88 = family(sp.Integer(2), q, sp.Integer(3))
    leaf = sp.Matrix(
        [[1, 1, 1], [2, q, f88["s"]], [3, 1 + f88["b"] + B, 1 + f88["c"] + C]]
    )
    syndrome = direct_matrix(gld71, parent, supports, (leaf, leaf, leaf)).applyfunc(
        sp.cancel
    )
    assert syndrome.shape == (37, 9)
    q6 = sp.Poly(q6_polynomial(sp.Integer(2), q), q, domain=QQ)
    parsed = []
    metadata = []
    for row, column in TARGETS:
        bordered = syndrome.extract((*ROWS, row), (*COLUMNS, column))
        # The audit's primary object is the bordered determinant itself.  The
        # polynomial adjugate identity identifies it with the usual Schur
        # numerator globally; no inverse of R31 is used or needed.
        residual = sp.cancel(polynomial_determinant(bordered, B, C, q))
        numerator, denominator = residual.as_numer_denom()
        if denominator.has(B, C):
            print("unexpected denominator", (row, column), sp.factor(denominator), flush=True)
            raise AssertionError("bordered determinant denominator retained B/C")
        polynomial = sp.Poly(numerator, B, C, domain=QQ.frac_field(q))
        coefficients = {}
        for monomial, coefficient in polynomial.terms():
            reduced = q_reduce(coefficient / denominator, q, q6)
            if reduced != 0:
                coefficients[monomial] = reduced
        assert all(c_exp in (0, 1) for _b_exp, c_exp in coefficients)
        assert all(b_exp >= 1 for b_exp, c_exp in coefficients if c_exp == 0)
        f = sp.Add(
            *(coefficient * B**b_exp for (b_exp, c_exp), coefficient in coefficients.items() if c_exp == 0)
        )
        g = sp.Add(
            *(coefficient * B**b_exp for (b_exp, c_exp), coefficient in coefficients.items() if c_exp == 1)
        )
        assert sp.Poly(f, B).monoms() in (
            [(2,), (1,)],
            [(3,), (2,), (1,)],
        )
        assert tuple(sorted(sp.Poly(g, B).monoms())) == ((0,), (1,), (2,))
        parsed.append((sp.cancel(f), sp.cancel(g)))
        metadata.append({"target": [row, column], "monomial_count": len(coefficients)})

    cross = []
    for index in (1, 2):
        f0, g0 = parsed[0]
        fi, gi = parsed[index]
        polynomial = sp.Poly(sp.expand(f0 * gi - fi * g0), B, domain=QQ.frac_field(q))
        assert q_reduce(polynomial.nth(0), q, q6) == 0
        cross.append(
            sp.cancel(
                sp.Add(
                    *(
                        q_reduce(polynomial.nth(power + 1), q, q6) * B**power
                        for power in range(polynomial.degree())
                    )
                )
            )
        )
    reduced_resultant = q_reduce(sp.resultant(cross[0], cross[1], B), q, q6)
    primitive = sp.Poly(reduced_resultant, q, domain=QQ).primitive()[1]
    coefficients = tuple(int(value) for value in primitive.all_coeffs())
    assert coefficients == EXPECTED_RESULTANT_COEFFICIENTS
    assert hashlib.sha256(repr(coefficients).encode()).hexdigest() == EXPECTED_RESULTANT_TUPLE_SHA256
    norm = int(sp.resultant(q6.as_expr(), primitive.as_expr(), q))
    assert sp.factorint(abs(norm)) == EXPECTED_RESULTANT_NORM_FACTORS
    first_g0 = sp.cancel(q_reduce(parsed[0][1].subs(B, 0), q, q6))
    expected_g0 = EXPECTED_G0.subs({sp.Symbol("q"): q})
    assert first_g0 == expected_g0
    g0_numerator = first_g0.as_numer_denom()[0]
    g0_norm = int(sp.resultant(q6.as_expr(), g0_numerator, q))
    assert sp.factorint(abs(g0_norm)) == EXPECTED_G0_NORM_FACTORS
    return {
        "status": "independent_exact_GLD96_R31_free_witness_audit",
        "gld_identifier": "GLD96",
        "matrix_shape": list(syndrome.shape),
        "construction": "direct sparse-support accumulation",
        "determinant_route": "bordered 7x7 Bareiss determinants in Q(q)[B,C]",
        "R31_gate_used": False,
        "bordered_identity_scope": "global polynomial identity, including R31=0",
        "global_conjecture": "UNRESOLVED",
        "residuals": metadata,
        "resultant_primitive_tuple_sha256": EXPECTED_RESULTANT_TUPLE_SHA256,
        "Q6_norm_factorization": EXPECTED_RESULTANT_NORM_FACTORS,
        "g0_norm_factorization": EXPECTED_G0_NORM_FACTORS,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    print("GLD96 R31-free generic independent audit: PASS")
    print(json.dumps(check(), indent=2, default=str))


if __name__ == "__main__":
    main()
