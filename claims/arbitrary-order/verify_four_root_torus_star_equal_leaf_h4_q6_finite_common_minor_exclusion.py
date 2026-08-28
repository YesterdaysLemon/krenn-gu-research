#!/usr/bin/env python3
"""Verify the exact GLD95 finite common-minor exclusion.

The calculation is over Q and then C.  It reconstructs the fixed GLD71
syndrome on the rational GLD88 H4 formula family, computes the GLD92
six-minors and their Q6 resultant, and exhausts every exact residual
component.  The ordinary open components are checked in nested exact
quotient fields.  The old Q6-leading-coefficient fibre is checked directly,
without the invalid generic division by H2.  Resultant-content fibres at
p=0,1,-1,1/2 are checked separately, including the old P6=0 boundary.

This proves only the finite common-minor residual on the written rational
family over D(Delta).  It does not force arbitrary H4/Q6 points into that
family and does not resolve the global Krenn--Gu conjecture.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ
from sympy.polys.agca.extensions import FiniteExtension


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_P6_ROWS = (0, 1, 2, 17, 19, 32)

EXPECTED_RESULTANT_SREPR_SHA256 = (
    "fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d"
)
EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256 = (
    "0057c78ceea5241553d856ce437f0fb4fd77571c8205eaa96c7c13dce54cec42"
)
EXPECTED_SQUAREFREE_SHA256 = (
    "86eca671802beaf8cb2cb1f3755494b24ece747f3bc3efb8129cf2263f8c6743"
)

EXPECTED_GENERIC_MINOR_SHA256 = {
    (0, 0): "45c2969b26a7e7efa2585489eadb4ef554af37fa646ebdc875458e9ae2afd0f5",
    (0, 1): "fadd23534644e09f245d18c70267beeab53fb4d4a1812352ae4a216b0c61a5e3",
    (1, 0): "e18c9af590ffbe7cf4d646dbcef7b34d9beab4f8142761984469a7e7415f01ba",
    (1, 1): "93724e3a9341a39e0bbc79796dab798b334e066085be3f467d6ccc9dcb8b72d1",
    (3, 0): "0d95bb74a934f840aeffa143c0e8b0444439af55deee0c4f2b6df228f9daec9a",
    (3, 1): "11ecb64cd0892907ff9739bb964cf3cda41cf32fb02087adc428ad48177cacce",
    (4, 0): "89086752d46f7145bd76162679eac0b3391d510b1f05bf23116dfeafd3924e70",
    (4, 1): "d69bbdd0832021bc2e46a421eb7b946318abe7509e84be895d99a56aa53acece",
    (5, 0): "10fb6b29e65080f23b3bb094dd448fac188d8f81b50fcfcf102c76f94d57cc37",
    (6, 0): "0b4623755a43cd5e6ba7a8e15641d264f49d852533900d4a5ddc1827a1a1d36b",
}
EXPECTED_GENERIC_ROWS = {
    (0, 0): (1, 17, 0, 28, 4, 32),
    (0, 1): (1, 17, 0, 28, 4, 32),
    (1, 0): (1, 17, 0, 25, 28, 31),
    (1, 1): (1, 17, 0, 25, 28, 31),
    (3, 0): (1, 17, 0, 25, 28, 31),
    (3, 1): (1, 17, 0, 25, 28, 31),
    (4, 0): (1, 17, 0, 28, 4, 31),
    (4, 1): (1, 17, 0, 28, 4, 31),
    (5, 0): (1, 17, 0, 25, 4, 32),
    (6, 0): (1, 17, 0, 25, 4, 32),
}

EXPECTED_CONTENT_MINOR_SHA256 = {
    "p0_qquad_a0": "943867f4bce314d869a83ccfb7349f34c5f97ca7ddca19f47056da39010780df",
    "p0_qquad_a53": "ce2109fbaa3262e1bad3f7a6377c17be85b0f81e30b59faf3ee7ef7da687a48c",
    "p1_qq_a2": "4576a54cb064bf296164af03c67fd6c3f489917e0825bd6c5d8c304ae4fddc22",
    "pm1": "7cfe9dcb1cea749581b85f9a9ebab5f42be99ebc8dfa5d7786eddf30692e094a",
    "phalf": "191ad4b8b2de39cd364569d75be13e12d332f4cb766eea0d0dc5150da9243d23",
}
EXPECTED_CONTENT_ROWS = {
    "p0_qquad_a0": (1, 17, 28, 0, 32, 3),
    "p0_qquad_a53": (1, 17, 25, 0, 4, 32),
    "p1_qq_a2": (1, 17, 0, 25, 28, 31),
    "pm1": (1, 17, 0, 25, 28, 31),
    "phalf": (1, 17, 0, 28, 4, 31),
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def patch_division(extension: FiniteExtension) -> None:
    # SymPy's FiniteExtension polynomial quotient path uses exact division
    # against a representation that is not normalized.  All coefficient
    # arithmetic here is in the quotient field, so the inverse form is the
    # sound replacement used by the research replay.
    extension.exquo = lambda left, right: left * (right**-1)
    extension.quo = lambda left, right: left * (right**-1)


def q6_polynomial(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


def h_factors(p: sp.Symbol) -> list[sp.Expr]:
    return [
        p**2 - 2 * p + 2,
        p**2 + 1,
        2 * p**2 - 2 * p + 1,
        5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
        8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
        p**6 - 6 * p**5 + 12 * p**4 - 16 * p**3 + 18 * p**2 - 12 * p + 4,
        5 * p**12 - 36 * p**11 + 126 * p**10 - 316 * p**9 + 624 * p**8
        - 984 * p**7 + 1272 * p**6 - 1344 * p**5 + 1146 * p**4
        - 760 * p**3 + 372 * p**2 - 120 * p + 20,
    ]


def generic_branches(p: sp.Symbol, q: sp.Symbol, a: sp.Symbol) -> dict[int, list[tuple[sp.Expr, sp.Expr]]]:
    a0 = a**2 + a * (-11 * p / 12 - sp.Rational(1, 6)) + 7 * p / 12 - sp.Rational(1, 2)
    a5 = a + p**5 / 6 - 2 * p**4 / 3 + 2 * p**3 / 3 - 4 * p**2 / 3 + p / 3 - sp.Rational(1, 3)
    a6 = (
        a - p**11 / 24 + 22 * p**10 / 15 - 959 * p**9 / 120 + 227 * p**8 / 10
        - 50 * p**7 + 347 * p**6 / 4 - 2341 * p**5 / 20 + 2611 * p**4 / 20
        - 113 * p**3 + 1118 * p**2 / 15 - 100 * p / 3 + sp.Rational(47, 6)
    )
    return {
        0: [(q, a0), (q + p - 2, a0)],
        1: [(q - 1, a), (q + p, a)],
        3: [
            (q + 1, a),
            (q - (sp.Rational(2, 3) - 6 * p / 5 - p**3 / 3 + 2 * p**2 / 5), a),
        ],
        4: [
            (q - sp.Rational(1, 2), a - p),
            (q - (sp.Rational(2, 3) - 4 * p**3 / 3 - p + 2 * p**2), a - p),
        ],
        5: [
            (
                q**2 + q * (-p**5 / 2 + 2 * p**4 - p**3 + p**2 - 4)
                - p**5 / 2 + 3 * p**4 - 6 * p**3 + 8 * p**2 - 9 * p + 6,
                a5,
            )
        ],
        6: [
            (
                q**2
                + q * (
                    57 * p**11 / 5 - 3909 * p**10 / 50 + 2569 * p**9 / 10
                    - 15291 * p**8 / 25 + 28872 * p**7 / 25 - 42993 * p**6 / 25
                    + 10449 * p**5 / 5 - 51354 * p**4 / 25 + 39558 * p**3 / 25
                    - 912 * p**2 + 1766 * p / 5 - 74
                )
                - 15 * p**11 / 2 + 239 * p**10 / 5 - 7403 * p**9 / 50
                + 1719 * p**8 / 5 - 15777 * p**7 / 25 + 22734 * p**6 / 25
                - 26991 * p**5 / 25 + 5118 * p**4 / 5 - 19038 * p**3 / 25
                + 10426 * p**2 / 25 - 763 * p / 5 + sp.Rational(142, 5),
                a6,
            )
        ],
    }


def trim(values, zero):
    result = list(values)
    while result and result[-1] == zero:
        result.pop()
    return result


def coefficients(poly: sp.Poly, extension: FiniteExtension):
    if poly.is_zero:
        return []
    return trim(
        [extension.convert(poly.nth(i)) for i in range(poly.degree() + 1)],
        extension.zero,
    )


def divmod_extension(left, right, extension: FiniteExtension):
    numerator = trim(left, extension.zero)
    denominator = trim(right, extension.zero)
    if not denominator:
        raise ZeroDivisionError("polynomial division by zero")
    if len(numerator) < len(denominator):
        return [], numerator
    quotient = [extension.zero] * (len(numerator) - len(denominator) + 1)
    inverse_lead = denominator[-1] ** -1
    while numerator and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        factor = numerator[-1] * inverse_lead
        quotient[shift] += factor
        for index, value in enumerate(denominator):
            numerator[index + shift] -= factor * value
        numerator = trim(numerator, extension.zero)
    return trim(quotient, extension.zero), numerator


def gcd_extension(left: sp.Poly, right: sp.Poly, extension: FiniteExtension):
    left_coefficients = coefficients(left, extension)
    right_coefficients = coefficients(right, extension)
    if not left_coefficients and not right_coefficients:
        raise ValueError("both specialized polynomials vanish identically")
    if not left_coefficients:
        left_coefficients, right_coefficients = right_coefficients, []
    while right_coefficients:
        _quotient, remainder = divmod_extension(
            left_coefficients, right_coefficients, extension
        )
        left_coefficients, right_coefficients = right_coefficients, remainder
    inverse_lead = left_coefficients[-1] ** -1
    return [value * inverse_lead for value in left_coefficients]


def coefficients_as_expr(values, extension: FiniteExtension, variable):
    return sp.Add(
        *(extension.to_sympy(value) * variable**index for index, value in enumerate(values))
    )


def determinant(matrix, zero, one):
    total = zero
    size = len(matrix)
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = one
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total = total - term if inversions % 2 else total + term
    return total


def unit_pivots(matrix, extension):
    work = [list(row) for row in matrix]
    original_rows = list(range(len(work)))
    pivot_rows = []
    pivot_columns = []
    position = 0
    for column in range(len(work[0])):
        chosen = None
        inverse = None
        for row in range(position, len(work)):
            if work[row][column] == extension.zero:
                continue
            try:
                candidate_inverse = work[row][column] ** -1
            except Exception:
                continue
            chosen, inverse = row, candidate_inverse
            break
        if chosen is None:
            continue
        work[position], work[chosen] = work[chosen], work[position]
        original_rows[position], original_rows[chosen] = (
            original_rows[chosen],
            original_rows[position],
        )
        work[position] = [value * inverse for value in work[position]]
        for row in range(position + 1, len(work)):
            multiplier = work[row][column]
            if multiplier == extension.zero:
                continue
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[position], strict=True)
            ]
        pivot_rows.append(original_rows[position])
        pivot_columns.append(column)
        position += 1
        if position == 6:
            break
    return pivot_rows, pivot_columns


def specialize(expression, substitutions, extension):
    numerator, denominator = sp.cancel(expression.subs(substitutions)).as_numer_denom()
    return extension.convert(numerator) / extension.convert(denominator)


def normalized_coefficients(values, extension):
    values = trim(values, extension.zero)
    inverse = values[-1] ** -1
    return [value * inverse for value in values]


def ext_poly_coefficients(poly: sp.Poly, extension: FiniteExtension):
    return [extension.convert(poly.nth(i)) for i in range(poly.degree() + 1)]


def ext_polynomial_equal(left: sp.Poly, right: sp.Poly, extension: FiniteExtension):
    return normalized_coefficients(ext_poly_coefficients(left, extension), extension) == normalized_coefficients(
        ext_poly_coefficients(right, extension), extension
    )


def build_symbolic_data():
    gld71 = load_module(GLD71, "gld71_for_gld95_primary")
    gld88 = load_module(GLD88, "gld88_for_gld95_primary")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37
    p, q, a = sp.symbols("p q a")
    family = gld88.h4_family(p, q, a)
    leaf = sp.Matrix(
        [[1, 1, 1], [p, q, family["s"]], [a, 1 + family["b"], 1 + family["c"]]]
    )
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    assert syndrome.shape == (37, 9)
    rows28 = (0, 1, 2, 17, 25, 28)
    rows31 = (0, 1, 2, 17, 25, 31)
    n28 = sp.cancel(syndrome.extract(rows28, PIVOT_COLUMNS).det(method="domain-ge")).as_numer_denom()[0]
    n31 = sp.cancel(syndrome.extract(rows31, PIVOT_COLUMNS).det(method="domain-ge")).as_numer_denom()[0]
    f28 = sp.expand(sp.cancel(n28 / (p - q) ** 3))
    f31 = sp.expand(sp.cancel(n31 / ((p + q - 1) * (p - q) ** 3)))
    assert f28.as_numer_denom()[1] == 1
    assert f31.as_numer_denom()[1] == 1
    return parent, syndrome, family, leaf, p, q, a, n28, n31, f28, f31


def exact_decomposition(p, q, a, f28, f31):
    started = time.monotonic()
    q6 = q6_polynomial(p, q)
    resultant = sp.resultant(f28, f31, a)
    resultant_poly = sp.Poly(resultant, p, q, domain=QQ)
    assert resultant_poly.total_degree() == 99
    assert resultant_poly.degree(p) == 56
    assert resultant_poly.degree(q) == 53
    resultant_hash = hashlib.sha256(sp.srepr(resultant).encode()).hexdigest()
    assert resultant_hash == EXPECTED_RESULTANT_SREPR_SHA256
    fraction_field = QQ.frac_field(p)
    result_in_q = sp.Poly(resultant, q, domain=fraction_field)
    q6_in_q = sp.Poly(q6, q, domain=fraction_field)
    _quotient, remainder = sp.div(result_in_q, q6_in_q)
    remainder_cancelled = sp.cancel(remainder.as_expr())
    remainder_num, remainder_den = remainder_cancelled.as_numer_denom()
    h2 = 2 * p**2 - 2 * p + 1
    assert sp.factor(remainder_den) == h2**47
    remainder_hash = hashlib.sha256(sp.srepr(remainder.as_expr()).encode()).hexdigest()
    assert remainder_hash == EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256
    remainder_over_p = sp.Poly(remainder_num, q, domain=QQ.poly_ring(p))
    remainder_content, remainder_primitive = remainder_over_p.primitive()
    assert remainder_primitive.degree(q) == 3
    content_factorization = sp.factor_list(remainder_content)
    expected_content = [
        (p - 1, 1),
        (p + 1, 1),
        (2 * p - 1, 1),
        (p, 4),
        (p**2 - p + 1, 9),
    ]
    assert sp.factor(content_factorization[0]) == sp.Rational(1, 2)
    assert [(sp.expand(factor), exponent) for factor, exponent in content_factorization[1]] == [
        (sp.expand(factor), exponent) for factor, exponent in expected_content
    ]
    coefficient_ring = QQ.poly_ring(p)
    q6_over_p = sp.Poly(q6, q, domain=coefficient_ring)
    elimination_expr = sp.resultant(q6_over_p, remainder_primitive, q)
    elimination = sp.Poly(elimination_expr, p, domain=QQ).primitive()[1]
    squarefree = elimination.sqf_part().monic()
    squarefree_hash = hashlib.sha256(sp.srepr(squarefree.as_expr()).encode()).hexdigest()
    assert squarefree_hash == EXPECTED_SQUAREFREE_SHA256
    factors = sp.factor_list(squarefree.as_expr())[1]
    expected_factors = [
        p - 1,
        p,
        p**2 - 2 * p + 2,
        p**2 - p + 1,
        p**2 + 1,
        h2,
        5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
        8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
        p**6 - 6 * p**5 + 12 * p**4 - 16 * p**3 + 18 * p**2 - 12 * p + 4,
        5 * p**12 - 36 * p**11 + 126 * p**10 - 316 * p**9 + 624 * p**8
        - 984 * p**7 + 1272 * p**6 - 1344 * p**5 + 1146 * p**4
        - 760 * p**3 + 372 * p**2 - 120 * p + 20,
    ]
    actual_factors = [sp.Poly(factor, p, domain=QQ).monic().as_expr() for factor, exponent in factors for _ in range(exponent)]
    assert actual_factors == [sp.Poly(factor, p, domain=QQ).monic().as_expr() for factor in expected_factors]
    return {
        "q6": q6,
        "resultant": resultant,
        "resultant_poly": resultant_poly,
        "remainder_primitive": remainder_primitive,
        "content_factorization": content_factorization,
        "h_factors": expected_factors[2:3] + expected_factors[4:5] + expected_factors[5:]
        + [],
        "squarefree": squarefree,
        "factorization": factors,
        "resultant_hash": resultant_hash,
        "resultant_remainder_hash": remainder_hash,
        "squarefree_hash": squarefree_hash,
        "division_denominator": sp.factor(remainder_den),
        "seconds": round(time.monotonic() - started, 3),
    }


def check_generic_components(p, q, a, syndrome, f28, f31, decomposition):
    factors = h_factors(p)
    branches = generic_branches(p, q, a)
    remainder_primitive = decomposition["remainder_primitive"]
    q6 = decomposition["q6"]
    results = []
    for factor_index in sorted(branches):
        h = factors[factor_index]
        p_extension = FiniteExtension(sp.Poly(h, p, domain=QQ))
        patch_division(p_extension)
        q6_extension = sp.Poly(q6, q, domain=p_extension)
        remainder_extension = sp.Poly(remainder_primitive.as_expr(), q, domain=p_extension)
        q_gcd = gcd_extension(q6_extension, remainder_extension, p_extension)
        q_gcd_expr = coefficients_as_expr(q_gcd, p_extension, q)
        expected_product = sp.prod(qmod for qmod, _amod in branches[factor_index])
        expected_q_poly = sp.Poly(expected_product, q, domain=p_extension)
        actual_q_poly = sp.Poly(q_gcd_expr, q, domain=p_extension)
        assert ext_polynomial_equal(actual_q_poly, expected_q_poly, p_extension)
        for branch_index, (q_modulus, a_modulus) in enumerate(branches[factor_index]):
            branch_started = time.monotonic()
            q_extension = FiniteExtension(sp.Poly(q_modulus, q, domain=p_extension))
            patch_division(q_extension)
            f28_a = sp.Poly(f28, a, domain=q_extension)
            f31_a = sp.Poly(f31, a, domain=q_extension)
            a_gcd = gcd_extension(f28_a, f31_a, q_extension)
            actual_a_modulus = coefficients_as_expr(a_gcd, q_extension, a)
            expected_a_poly = sp.Poly(a_modulus, a, domain=q_extension)
            actual_a_poly = sp.Poly(actual_a_modulus, a, domain=q_extension)
            assert ext_polynomial_equal(actual_a_poly, expected_a_poly, q_extension)
            a_degree = len(a_gcd) - 1
            if a_degree == 0:
                assert a_gcd == [q_extension.one]
                results.append(
                    {
                        "factor_index": factor_index,
                        "branch_index": branch_index,
                        "p_degree": p_extension.rank,
                        "q_degree": q_extension.rank,
                        "a_degree": 0,
                        "q_modulus": str(q_modulus),
                        "a_modulus": str(actual_a_modulus),
                        "empty_branch": True,
                        "seconds": round(time.monotonic() - branch_started, 3),
                    }
                )
                continue
            a_extension = FiniteExtension(sp.Poly(actual_a_modulus, a, domain=q_extension))
            patch_division(a_extension)

            def specialize_full(expression):
                numerator, denominator = sp.cancel(expression).as_numer_denom()
                return a_extension.convert(numerator) / a_extension.convert(denominator)

            specialized = [
                [specialize_full(syndrome[row, column]) for column in range(9)]
                for row in range(syndrome.rows)
            ]
            rows, columns = unit_pivots(specialized, a_extension)
            assert len(rows) == 6
            assert tuple(columns) == PIVOT_COLUMNS
            assert tuple(rows) == EXPECTED_GENERIC_ROWS[(factor_index, branch_index)]
            minor = determinant(
                [[specialized[row][column] for column in columns] for row in rows],
                a_extension.zero,
                a_extension.one,
            )
            inverse = minor**-1
            assert minor * inverse == a_extension.one
            minor_expr = sp.cancel(a_extension.to_sympy(minor))
            minor_hash = hashlib.sha256(str(minor_expr).encode()).hexdigest()
            assert minor_hash == EXPECTED_GENERIC_MINOR_SHA256[(factor_index, branch_index)], (
                factor_index,
                branch_index,
                minor_hash,
                EXPECTED_GENERIC_MINOR_SHA256[(factor_index, branch_index)],
                str(minor_expr),
            )
            results.append(
                {
                    "factor_index": factor_index,
                    "branch_index": branch_index,
                    "p_degree": p_extension.rank,
                    "q_degree": q_extension.rank,
                    "a_degree": a_degree,
                    "q_modulus": str(q_modulus),
                    "a_modulus": str(actual_a_modulus),
                    "rows": list(rows),
                    "columns": list(columns),
                    "minor": str(minor_expr),
                    "minor_sha256": minor_hash,
                    "inverse_sha256": hashlib.sha256(
                        str(sp.cancel(a_extension.to_sympy(inverse))).encode()
                    ).hexdigest(),
                    "unit_check": True,
                    "seconds": round(time.monotonic() - branch_started, 3),
                }
            )
    return results


def content_basis(p, q, a, f28, f31, q6, value):
    q6_special = sp.Poly(q6.subs(p, value), q, domain=QQ)
    f28_special = sp.Poly(f28.subs(p, value), q, a, domain=QQ)
    f31_special = sp.Poly(f31.subs(p, value), q, a, domain=QQ)
    basis = sp.groebner(
        [q6_special.as_expr(), f28_special.as_expr(), f31_special.as_expr()],
        a,
        q,
        order="lex",
        domain=QQ,
    )
    return [sp.expand(value) for value in basis]


def check_content_components(p, q, a, syndrome, f28, f31, q6):
    expected_bases = {
        0: [a**2 * q**2 - sp.Rational(5, 3) * a * q**2, q**4 - 2 * q**3 + 2 * q**2],
        1: [
            a**3 - sp.Rational(8, 3) * a**2 + sp.Rational(4, 3) * a,
            a * q**2 - 2 * a * q + a - 2 * q**2 + 4 * q - 2,
            q**4 - 2 * q**3 + 2 * q**2 - 2 * q + 1,
        ],
        -1: [
            a + sp.Rational(5, 9) * q**3 - sp.Rational(2, 3) * q**2 + q / 3 + sp.Rational(14, 9),
            q**4 - sp.Rational(16, 5) * q**3 + 6 * q**2 - sp.Rational(16, 5) * q + 1,
        ],
        sp.Rational(1, 2): [
            a + sp.Rational(8, 9) * q**3 - sp.Rational(4, 3) * q**2 - sp.Rational(5, 18),
            q**4 - 2 * q**3 + sp.Rational(3, 2) * q**2 - q / 2 + sp.Rational(5, 8),
        ],
    }
    for value, expected in expected_bases.items():
        actual = content_basis(p, q, a, f28, f31, q6, value)
        assert actual == [sp.expand(item) for item in expected]

    cases = {
        "p0_qquad_a0": (0, q**2 - 2 * q + 2, 0, (1, 17, 28, 0, 32, 3)),
        "p0_qquad_a53": (0, q**2 - 2 * q + 2, sp.Rational(5, 3), (1, 17, 25, 0, 4, 32)),
        "p1_qq_a2": (1, q**2 + 1, 2, (1, 17, 0, 25, 28, 31)),
        "pm1": (
            -1,
            q**4 - sp.Rational(16, 5) * q**3 + 6 * q**2 - sp.Rational(16, 5) * q + 1,
            -sp.Rational(5, 9) * q**3 + sp.Rational(2, 3) * q**2 - q / 3 - sp.Rational(14, 9),
            (1, 17, 0, 25, 28, 31),
        ),
        "phalf": (
            sp.Rational(1, 2),
            q**4 - 2 * q**3 + sp.Rational(3, 2) * q**2 - q / 2 + sp.Rational(5, 8),
            -sp.Rational(8, 9) * q**3 + sp.Rational(4, 3) * q**2 + sp.Rational(5, 18),
            (1, 17, 0, 28, 4, 31),
        ),
    }
    delta = {
        "p-q": p - q,
        "d0": p + q - 1,
        "P": p**2 - p + 1,
        "L1": p**2 + 2 * p * q - 2 * p - q,
        "L2": 2 * p * q - p + q**2 - 2 * q,
        "e": 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2,
    }
    results = []
    for label, (pvalue, qmodulus, avalue, expected_rows) in cases.items():
        extension = FiniteExtension(sp.Poly(qmodulus, q, domain=QQ).monic())
        q6_remainder = sp.Poly(q6.subs(p, pvalue), q, domain=QQ).rem(
            sp.Poly(qmodulus, q, domain=QQ).monic()
        )
        assert q6_remainder.is_zero
        substitutions = {p: pvalue, a: avalue}
        specialized = [
            [specialize(syndrome[row, column], substitutions, extension) for column in range(9)]
            for row in range(syndrome.rows)
        ]
        rows, columns = unit_pivots(specialized, extension)
        assert tuple(rows) == expected_rows
        assert tuple(columns) == PIVOT_COLUMNS
        minor = determinant(
            [[specialized[row][column] for column in columns] for row in rows],
            extension.zero,
            extension.one,
        )
        inverse = minor**-1
        assert minor * inverse == extension.one
        minor_expr = sp.cancel(extension.to_sympy(minor))
        assert hashlib.sha256(str(minor_expr).encode()).hexdigest() == EXPECTED_CONTENT_MINOR_SHA256[label]
        old_p6 = determinant(
            [[specialized[row][column] for column in PIVOT_COLUMNS] for row in OLD_P6_ROWS],
            extension.zero,
            extension.one,
        )
        assert old_p6 == extension.zero
        delta_units = {
            name: specialize(value, substitutions, extension) != extension.zero
            for name, value in delta.items()
        }
        assert all(delta_units.values())
        leaf_det = specialize(
            -((p - q) * (-3 * a + p + 1) * (p**2 + 2 * p * q - 2 * p - q)
              * (2 * p * q - p + q**2 - 2 * q))
            / ((p + q - 1) * (p**2 - p + 1)
               * (2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2)),
            substitutions,
            extension,
        )
        assert leaf_det != extension.zero
        results.append(
            {
                "label": label,
                "p": str(pvalue),
                "q_modulus": str(sp.Poly(qmodulus, q, domain=QQ).monic().as_expr()),
                "a_modulus": str(a - avalue),
                "rows": list(rows),
                "columns": list(columns),
                "minor": str(minor_expr),
                "minor_sha256": hashlib.sha256(str(minor_expr).encode()).hexdigest(),
                "inverse_sha256": hashlib.sha256(
                    str(sp.cancel(extension.to_sympy(inverse))).encode()
                ).hexdigest(),
                "unit_check": True,
                "old_P6_zero": True,
                "delta_units": delta_units,
                "leaf_determinant_unit": True,
            }
        )
    return results


def check() -> dict[str, object]:
    started = time.monotonic()
    parent, syndrome, family, leaf, p, q, a, n28, n31, f28, f31 = build_symbolic_data()
    q6 = q6_polynomial(p, q)
    d0 = p + q - 1
    pnorm = p**2 - p + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    delta = (p - q) * d0 * pnorm * l1 * l2 * e
    kernel = sp.Matrix([family["u"], family["v"], 1])
    block_kernel_identity_count = 0
    for block in range(3):
        for value in syndrome[:, 3 * block : 3 * block + 3] * kernel:
            assert sp.cancel(value) == 0
            block_kernel_identity_count += 1
    assert block_kernel_identity_count == 111
    assert sp.cancel(leaf.det() + (p - q) * (-3 * a + p + 1) * l1 * l2 / (d0 * pnorm * e)) == 0
    decomposition = exact_decomposition(p, q, a, f28, f31)
    # Q6 is irreducible and none of the declared Delta factors vanish
    # identically on its divisor.
    q6_factors = sp.factor_list(q6, p, q)[1]
    assert len(q6_factors) == 1 and q6_factors[0][1] == 1
    q6_poly = sp.Poly(q6, p, q, domain=QQ)
    for factor in (p - q, d0, pnorm, l1, l2, e):
        assert sp.gcd(q6_poly, sp.Poly(factor, p, q, domain=QQ)).total_degree() == 0
    # Preserve GLD92's no-vertical-line certificate as part of the exact
    # finite-residual bridge.
    vertical_equations = [q6]
    for expression in (f28, f31):
        vertical_equations.extend(sp.Poly(expression, a).all_coeffs())
    vertical_basis = sp.groebner(vertical_equations, p, q, order="lex")
    vertical_eliminant = sp.factor(vertical_basis.polys[-1].as_expr())
    assert vertical_basis.is_zero_dimensional
    assert vertical_eliminant == q**6 * (q**2 - q + 1) ** 4
    assert vertical_basis.reduce(((p - q) * pnorm) ** 6)[1] == 0
    generic = check_generic_components(
        p, q, a, syndrome, f28, f31, decomposition
    )
    # Directly specialize H2.  Generic Q6 division has denominator H2^47,
    # so its apparent quadratic branch is not admissible evidence there.
    h2 = 2 * p**2 - 2 * p + 1
    h2_extension = FiniteExtension(sp.Poly(h2, p, domain=QQ))
    patch_division(h2_extension)
    q6_h2 = sp.Poly(q6, q, domain=h2_extension)
    resultant_h2 = sp.Poly(decomposition["resultant"], q, domain=h2_extension)
    direct_h2_gcd = gcd_extension(q6_h2, resultant_h2, h2_extension)
    direct_h2_expr = coefficients_as_expr(direct_h2_gcd, h2_extension, q)
    assert len(direct_h2_gcd) - 1 == 1
    assert ext_polynomial_equal(
        sp.Poly(direct_h2_expr, q, domain=h2_extension),
        sp.Poly(d0, q, domain=h2_extension),
        h2_extension,
    )
    generic_h2_q6 = sp.Poly(q6, q, domain=h2_extension)
    generic_h2_remainder = sp.Poly(
        decomposition["remainder_primitive"].as_expr(), q, domain=h2_extension
    )
    generic_h2_gcd = gcd_extension(generic_h2_q6, generic_h2_remainder, h2_extension)
    assert len(generic_h2_gcd) - 1 == 3
    content = check_content_components(p, q, a, syndrome, f28, f31, q6)
    return {
        "status": "exact_scoped_H4_Q6_finite_common_minor_exclusion",
        "gld_identifier": "GLD95",
        "field": "Q_characteristic_zero_then_C",
        "global_conjecture": "UNRESOLVED",
        "scope": (
            "written rational GLD88 F88 formula family over D(Delta), including "
            "the old P6=0 resultant-content fibres"
        ),
        "syndrome_shape": list(syndrome.shape),
        "pivot_columns": list(PIVOT_COLUMNS),
        "minor_rows": {
            "M28": [0, 1, 2, 17, 25, 28],
            "M31": [0, 1, 2, 17, 25, 31],
        },
        "common_block_kernel_identity_count": block_kernel_identity_count,
        "rank_at_most_six_on_formula_family": True,
        "delta": str(delta),
        "q6": {
            "total_degree": 6,
            "irreducible_over_Q": True,
            "Delta_factor_gcds_are_one": True,
        },
        "resultant": {
            "total_degree": decomposition["resultant_poly"].total_degree(),
            "degree_p": decomposition["resultant_poly"].degree(p),
            "degree_q": decomposition["resultant_poly"].degree(q),
            "srepr_sha256": decomposition["resultant_hash"],
            "q6_remainder_srepr_sha256": decomposition["resultant_remainder_hash"],
            "generic_q_division_denominator": str(decomposition["division_denominator"]),
            "content_factorization": str(decomposition["content_factorization"]),
            "squarefree_sha256": decomposition["squarefree_hash"],
        },
        "generic_components": generic,
        "H2_direct_fibre": {
            "H2": str(h2),
            "generic_division_denominator": "H2**47",
            "generic_q_gcd_degree": len(generic_h2_gcd) - 1,
            "direct_q6_degree": q6_h2.degree(),
            "direct_resultant_degree": resultant_h2.degree(),
            "direct_q_gcd_degree": len(direct_h2_gcd) - 1,
            "direct_q_gcd": str(direct_h2_expr),
            "direct_common_locus": "d0=p+q-1, excluded by D(Delta)",
            "quadratic_branch_is_division_artifact": True,
        },
        "content_components": content,
        "vertical_fibre_certificate": {
            "zero_dimensional_base_ideal": True,
            "q_eliminant": str(vertical_eliminant),
            "delta_product_power_in_ideal": 6,
        },
        "old_P6_content_extension": {
            "all_content_components_have_P6_zero": True,
            "covered_by_new_unit_minors": True,
        },
        "scope_fences": [
            "arbitrary H4 intersect V(Q6) points outside the written F88 formula family are not covered",
            "the GLD83 pulled-back Fitting ideal is not computed",
            "other charts, components, gauges, source branches, and orders remain open",
            "global Krenn-Gu remains UNRESOLVED",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("GLD95 H4 Q6 finite common-minor exclusion verifier: PASS")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
