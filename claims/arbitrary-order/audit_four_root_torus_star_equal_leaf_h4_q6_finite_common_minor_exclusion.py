#!/usr/bin/env python3
"""Independently audit the exact GLD95 finite common-minor closure.

This audit does not import the primary verifier, the GLD71 relation builder,
or the GLD88 family builder.  It directly evaluates the immutable sparse
relation supports used by the displayed minors and unit witnesses.  It then
repeats the resultant/content decomposition, the direct H2 fibre check, and
the quotient-field unit tests.  The QQ[q] content-minor checks use numerator
and denominator gcds instead of a FiniteExtension inverse, providing a
separate arithmetic route for the old P6=0 fibres.

The upstream GLD75/GLD86 bridge and the GLD88 kernel implication remain
mathematical dependencies; this is an independent determinant/evaluation
audit, not an independent proof of those bridges.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time

import sympy as sp
from sympy import QQ
from sympy.polys.agca.extensions import FiniteExtension


PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_P6_ROWS = (0, 1, 2, 17, 19, 32)
MINOR_ROWS = {
    "M28": (0, 1, 2, 17, 25, 28),
    "M31": (0, 1, 2, 17, 25, 31),
}
EXPECTED_RESULTANT_SREPR_SHA256 = (
    "fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d"
)
EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256 = (
    "0057c78ceea5241553d856ce437f0fb4fd77571c8205eaa96c7c13dce54cec42"
)
EXPECTED_SQUAREFREE_SHA256 = (
    "86eca671802beaf8cb2cb1f3755494b24ece747f3bc3efb8129cf2263f8c6743"
)
EXPECTED_SUPPORT_DIGEST_SHA256 = (
    "24cdba204347947370076c621b167f5aac617b9731d30cd22e25504630cf87d3"
)

# These are immutable GLD71 sparse relation supports, copied rather than
# imported.  Rows 3,4,19,32 are needed by the new unit witnesses; rows 0,1,2,
# 17,25,28,31 are the GLD92 displayed-minor supports.
AUDIT_RELATIONS = {
    0: (((1, 1, 1, 1), 1),),
    1: (((0, 0, 0, 0), 1),),
    2: (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    3: (((2, 0, 2, 0), 1), ((2, 1, 2, 1), -1)),
    4: (((2, 0, 0, 2), 1), ((2, 1, 1, 2), -1)),
    17: (
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 0), -1),
        ((1, 0, 0, 0), -1),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
    ),
    19: (
        ((0, 0, 1, 0), 1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 1, 0), -2),
        ((0, 1, 1, 1), 1),
        ((1, 0, 0, 1), -1),
        ((1, 1, 1, 0), 1),
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
}

EXPECTED_GENERIC = {
    (0, 0): ((1, 17, 0, 28, 4, 32), "45c2969b26a7e7efa2585489eadb4ef554af37fa646ebdc875458e9ae2afd0f5"),
    (0, 1): ((1, 17, 0, 28, 4, 32), "fadd23534644e09f245d18c70267beeab53fb4d4a1812352ae4a216b0c61a5e3"),
    (1, 0): ((1, 17, 0, 25, 28, 31), "e18c9af590ffbe7cf4d646dbcef7b34d9beab4f8142761984469a7e7415f01ba"),
    (1, 1): ((1, 17, 0, 25, 28, 31), "93724e3a9341a39e0bbc79796dab798b334e066085be3f467d6ccc9dcb8b72d1"),
    (3, 0): ((1, 17, 0, 25, 28, 31), "0d95bb74a934f840aeffa143c0e8b0444439af55deee0c4f2b6df228f9daec9a"),
    (3, 1): ((1, 17, 0, 25, 28, 31), "11ecb64cd0892907ff9739bb964cf3cda41cf32fb02087adc428ad48177cacce"),
    (4, 0): ((1, 17, 0, 28, 4, 31), "89086752d46f7145bd76162679eac0b3391d510b1f05bf23116dfeafd3924e70"),
    (4, 1): ((1, 17, 0, 28, 4, 31), "d69bbdd0832021bc2e46a421eb7b946318abe7509e84be895d99a56aa53acece"),
    (5, 0): ((1, 17, 0, 25, 4, 32), "10fb6b29e65080f23b3bb094dd448fac188d8f81b50fcfcf102c76f94d57cc37"),
    (6, 0): ((1, 17, 0, 25, 4, 32), "0b4623755a43cd5e6ba7a8e15641d264f49d852533900d4a5ddc1827a1a1d36b"),
}
EXPECTED_CONTENT = {
    "p0_qquad_a0": ((1, 17, 28, 0, 32, 3), "943867f4bce314d869a83ccfb7349f34c5f97ca7ddca19f47056da39010780df"),
    "p0_qquad_a53": ((1, 17, 25, 0, 4, 32), "ce2109fbaa3262e1bad3f7a6377c17be85b0f81e30b59faf3ee7ef7da687a48c"),
    "p1_qq_a2": ((1, 17, 0, 25, 28, 31), "4576a54cb064bf296164af03c67fd6c3f489917e0825bd6c5d8c304ae4fddc22"),
    "pm1": ((1, 17, 0, 25, 28, 31), "7cfe9dcb1cea749581b85f9a9ebab5f42be99ebc8dfa5d7786eddf30692e094a"),
    "phalf": ((1, 17, 0, 28, 4, 31), "191ad4b8b2de39cd364569d75be13e12d332f4cb766eea0d0dc5150da9243d23"),
}


def q6(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4 + 2 * p**3 * q**3
        - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3 + 2 * p**2 * q**4
        - 7 * p**2 * q**3 + 12 * p**2 * q**2 - 7 * p**2 * q + 2 * p**2
        - 2 * p * q**4 + 5 * p * q**3 - 7 * p * q**2 + 2 * p * q
        + q**4 - 2 * q**3 + 2 * q**2
    )


def h4_family(p: sp.Symbol, q: sp.Symbol, a: sp.Symbol) -> dict[str, sp.Expr]:
    d0 = p + q - 1
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    nb = (
        -2 * a * p**2 * q**3 + 3 * a * p**2 * q**2 - 3 * a * p**2 * q + a * p**2
        + 2 * a * p * q**3 + 2 * a * p + a * q**3 - 3 * a * q**2 + 3 * a * q - 2 * a
        + p**3 * q**2 - p**3 + p**2 * q**3 - 3 * p**2 * q**2 + p**2
        - 2 * p * q**3 + 3 * p * q**2 - 2 * p + q**2 - 3 * q + 2
    )
    nc = (
        2 * a * p * q**3 - 3 * a * p * q**2 + 3 * a * p * q - a * p
        - a * q**3 + 3 * a * q**2 - 3 * a * q + 2 * a + p**2 * q**2
        - 2 * p**2 * q - 3 * p * q**2 + p * q + p - q**2 + 3 * q - 2
    )
    dk = (p - q) * d0**3
    return {
        "s": (p + q - p * q) / d0,
        "b": -nb / ((p**2 - p + 1) * e),
        "c": -nc / (d0 * e),
        "u": (q**2 - q + 1) * (2 * p * q - p + q**2 - 2 * q) / dk,
        "v": -(p**2 - p + 1) * (p**2 + 2 * p * q - 2 * p - q) / dk,
    }


def direct_rows(leaf: sp.Matrix, rows: tuple[int, ...]) -> sp.Matrix:
    return sp.Matrix(
        [
            [
                sp.expand(
                    sum(
                        coefficient
                        * leaf[indices[1], component]
                        * leaf[indices[2], component]
                        * leaf[indices[3], component]
                        for indices, coefficient in AUDIT_RELATIONS[row]
                        if indices[0] == root
                    )
                )
                for root in range(3)
                for component in range(3)
            ]
            for row in rows
        ]
    )


def patch_division(extension: FiniteExtension) -> None:
    extension.exquo = lambda left, right: left * (right**-1)
    extension.quo = lambda left, right: left * (right**-1)


def trim(values, zero):
    result = list(values)
    while result and result[-1] == zero:
        result.pop()
    return result


def poly_coefficients(poly: sp.Poly, extension: FiniteExtension):
    return trim(
        [extension.convert(poly.nth(i)) for i in range(poly.degree() + 1)],
        extension.zero,
    ) if not poly.is_zero else []


def divmod_extension(left, right, extension: FiniteExtension):
    numerator = trim(left, extension.zero)
    denominator = trim(right, extension.zero)
    if len(numerator) < len(denominator):
        return [], numerator
    quotient = [extension.zero] * (len(numerator) - len(denominator) + 1)
    inverse = denominator[-1] ** -1
    while numerator and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] * inverse
        quotient[shift] += coefficient
        for index, value in enumerate(denominator):
            numerator[index + shift] -= coefficient * value
        numerator = trim(numerator, extension.zero)
    return trim(quotient, extension.zero), numerator


def gcd_extension(left: sp.Poly, right: sp.Poly, extension: FiniteExtension):
    a = poly_coefficients(left, extension)
    b = poly_coefficients(right, extension)
    if not a and not b:
        raise ValueError("both polynomials vanish")
    if not a:
        a, b = b, []
    while b:
        _, remainder = divmod_extension(a, b, extension)
        a, b = b, remainder
    inverse = a[-1] ** -1
    return [value * inverse for value in a]


def coeff_expr(values, extension: FiniteExtension, variable):
    return sp.Add(*(extension.to_sympy(value) * variable**i for i, value in enumerate(values)))


def determinant(matrix, zero, one):
    total = zero
    for permutation in itertools.permutations(range(len(matrix))):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(len(matrix))
            for j in range(i + 1, len(matrix))
        )
        term = one
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total = total - term if inversions % 2 else total + term
    return total


def specialize(expression, substitutions, extension):
    numerator, denominator = sp.cancel(expression.subs(substitutions)).as_numer_denom()
    return extension.convert(numerator) / extension.convert(denominator)


def ext_poly_equal(left: sp.Poly, right: sp.Poly, extension: FiniteExtension):
    def normalize(values):
        values = trim(values, extension.zero)
        inverse = values[-1] ** -1
        return [value * inverse for value in values]
    return normalize(poly_coefficients(left, extension)) == normalize(poly_coefficients(right, extension))


def generic_branches(p, q, a):
    a0 = a**2 + a * (-11 * p / 12 - sp.Rational(1, 6)) + 7 * p / 12 - sp.Rational(1, 2)
    a5 = a + p**5 / 6 - 2 * p**4 / 3 + 2 * p**3 / 3 - 4 * p**2 / 3 + p / 3 - sp.Rational(1, 3)
    a6 = a - p**11 / 24 + 22 * p**10 / 15 - 959 * p**9 / 120 + 227 * p**8 / 10 - 50 * p**7 + 347 * p**6 / 4 - 2341 * p**5 / 20 + 2611 * p**4 / 20 - 113 * p**3 + 1118 * p**2 / 15 - 100 * p / 3 + sp.Rational(47, 6)
    return {
        0: [(q, a0), (q + p - 2, a0)],
        1: [(q - 1, a), (q + p, a)],
        3: [(q + 1, a), (q - (sp.Rational(2, 3) - 6 * p / 5 - p**3 / 3 + 2 * p**2 / 5), a)],
        4: [(q - sp.Rational(1, 2), a - p), (q - (sp.Rational(2, 3) - 4 * p**3 / 3 - p + 2 * p**2), a - p)],
        5: [(q**2 + q * (-p**5 / 2 + 2 * p**4 - p**3 + p**2 - 4) - p**5 / 2 + 3 * p**4 - 6 * p**3 + 8 * p**2 - 9 * p + 6, a5)],
        6: [(q**2 + q * (57 * p**11 / 5 - 3909 * p**10 / 50 + 2569 * p**9 / 10 - 15291 * p**8 / 25 + 28872 * p**7 / 25 - 42993 * p**6 / 25 + 10449 * p**5 / 5 - 51354 * p**4 / 25 + 39558 * p**3 / 25 - 912 * p**2 + 1766 * p / 5 - 74) - 15 * p**11 / 2 + 239 * p**10 / 5 - 7403 * p**9 / 50 + 1719 * p**8 / 5 - 15777 * p**7 / 25 + 22734 * p**6 / 25 - 26991 * p**5 / 25 + 5118 * p**4 / 5 - 19038 * p**3 / 25 + 10426 * p**2 / 25 - 763 * p / 5 + sp.Rational(142, 5), a6)],
    }


def h_factors(p):
    return [
        p**2 - 2 * p + 2,
        p**2 + 1,
        2 * p**2 - 2 * p + 1,
        5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
        8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
        p**6 - 6 * p**5 + 12 * p**4 - 16 * p**3 + 18 * p**2 - 12 * p + 4,
        5 * p**12 - 36 * p**11 + 126 * p**10 - 316 * p**9 + 624 * p**8 - 984 * p**7 + 1272 * p**6 - 1344 * p**5 + 1146 * p**4 - 760 * p**3 + 372 * p**2 - 120 * p + 20,
    ]


def support_digest():
    encoded = [
        [row, [[list(indices), coefficient] for indices, coefficient in support]]
        for row, support in sorted(AUDIT_RELATIONS.items())
    ]
    return hashlib.sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def main():
    started = time.monotonic()
    assert set(AUDIT_RELATIONS) == {0, 1, 2, 3, 4, 17, 19, 25, 28, 31, 32}
    assert support_digest() == EXPECTED_SUPPORT_DIGEST_SHA256
    p, q, a = sp.symbols("p q a")
    family = h4_family(p, q, a)
    leaf = sp.Matrix([[1, 1, 1], [p, q, family["s"]], [a, 1 + family["b"], 1 + family["c"]]])
    q6_poly = q6(p, q)
    minor_data = {}
    numerators = []
    for name, rows in MINOR_ROWS.items():
        matrix = direct_rows(leaf, rows)
        determinant_expr = sp.cancel(matrix[:, PIVOT_COLUMNS].det(method="domain-ge"))
        numerator, denominator = determinant_expr.as_numer_denom()
        numerator = sp.expand(numerator)
        assert sp.cancel(
            denominator
            - (p**2 - p + 1) ** 2
            * (2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2) ** 2
        ) == 0
        numerators.append(numerator)
        remainder = sp.div(
            sp.Poly(numerator, q, domain=QQ.frac_field(p, a)),
            sp.Poly(q6_poly, q, domain=QQ.frac_field(p, a)),
        )[1]
        remainder_expr = sp.expand(remainder.as_expr())
        minor_data[name] = {
            "rows": list(rows),
            "numerator_sha256": hashlib.sha256(sp.srepr(numerator).encode()).hexdigest(),
            "q6_remainder_sha256": hashlib.sha256(sp.srepr(remainder_expr).encode()).hexdigest(),
            "q6_remainder_nonzero": not remainder.is_zero,
        }
    assert minor_data["M28"]["numerator_sha256"] == "55bfba7b569752acb072ad0922d273e55d70651782e93394a14f9c23098727b8"
    assert minor_data["M31"]["numerator_sha256"] == "352948a2c113f32f10b90520592cb266cb455853297a664964478fdd7369b18f"
    assert minor_data["M28"]["q6_remainder_sha256"] == "8efab099320d2e498167c86999ac90adfeb85f2d80d3bd1f4b4e7539577298ef"
    assert minor_data["M31"]["q6_remainder_sha256"] == "b05d58c3177d7d0c8ea1b54cf7931f0a8e73b314518c748031f9be847d331912"
    f28 = sp.cancel(numerators[0] / (p - q) ** 3)
    f31 = sp.cancel(numerators[1] / ((p + q - 1) * (p - q) ** 3))
    assert sp.factor_list(f28)[1][0][1] == 1 and sp.factor_list(f31)[1][0][1] == 1

    resultant = sp.resultant(f28, f31, a)
    resultant_hash = hashlib.sha256(sp.srepr(resultant).encode()).hexdigest()
    assert resultant_hash == EXPECTED_RESULTANT_SREPR_SHA256
    resultant_poly = sp.Poly(resultant, p, q, domain=QQ)
    fraction_field = QQ.frac_field(p)
    result_in_q = sp.Poly(resultant, q, domain=fraction_field)
    q6_in_q = sp.Poly(q6_poly, q, domain=fraction_field)
    _quotient, remainder = sp.div(result_in_q, q6_in_q)
    remainder_num, remainder_den = sp.cancel(remainder.as_expr()).as_numer_denom()
    assert sp.factor(remainder_den) == (2 * p**2 - 2 * p + 1) ** 47
    remainder_hash = hashlib.sha256(sp.srepr(remainder.as_expr()).encode()).hexdigest()
    assert remainder_hash == EXPECTED_RESULTANT_Q6_REMAINDER_SREPR_SHA256
    remainder_over_p = sp.Poly(remainder_num, q, domain=QQ.poly_ring(p))
    content, primitive = remainder_over_p.primitive()
    assert sp.factor_list(content)[1] == [
        (p - 1, 1), (p + 1, 1), (2 * p - 1, 1), (p, 4), (p**2 - p + 1, 9)
    ]
    elimination = sp.Poly(sp.resultant(sp.Poly(q6_poly, q, domain=QQ.poly_ring(p)), primitive, q), p, domain=QQ).primitive()[1]
    squarefree = elimination.sqf_part().monic()
    assert hashlib.sha256(sp.srepr(squarefree.as_expr()).encode()).hexdigest() == EXPECTED_SQUAREFREE_SHA256

    factors = h_factors(p)
    branches = generic_branches(p, q, a)
    generic_results = []
    for index in sorted(branches):
        p_ext = FiniteExtension(sp.Poly(factors[index], p, domain=QQ))
        patch_division(p_ext)
        q6_ext = sp.Poly(q6_poly, q, domain=p_ext)
        prim_ext = sp.Poly(primitive.as_expr(), q, domain=p_ext)
        qg = gcd_extension(q6_ext, prim_ext, p_ext)
        assert ext_poly_equal(
            sp.Poly(coeff_expr(qg, p_ext, q), q, domain=p_ext),
            sp.Poly(sp.prod(qmod for qmod, _ in branches[index]), q, domain=p_ext),
            p_ext,
        )
        for branch_index, (qmod, amod) in enumerate(branches[index]):
            q_ext = FiniteExtension(sp.Poly(qmod, q, domain=p_ext))
            patch_division(q_ext)
            f28_ext = sp.Poly(f28, a, domain=q_ext)
            f31_ext = sp.Poly(f31, a, domain=q_ext)
            ag = gcd_extension(f28_ext, f31_ext, q_ext)
            assert ext_poly_equal(
                sp.Poly(coeff_expr(ag, q_ext, a), a, domain=q_ext),
                sp.Poly(amod, a, domain=q_ext),
                q_ext,
            )
            if len(ag) == 1:
                assert ag == [q_ext.one]
                continue
            a_ext = FiniteExtension(sp.Poly(coeff_expr(ag, q_ext, a), a, domain=q_ext))
            patch_division(a_ext)
            rows, expected_hash = EXPECTED_GENERIC[(index, branch_index)]
            matrix = direct_rows(leaf, rows)
            specialized = [
                [specialize(matrix[row, column], {}, a_ext) for column in range(9)]
                for row in range(6)
            ]
            minor = determinant(
                [[specialized[row][column] for column in PIVOT_COLUMNS] for row in range(6)],
                a_ext.zero,
                a_ext.one,
            )
            assert minor * (minor**-1) == a_ext.one
            minor_expr = sp.cancel(a_ext.to_sympy(minor))
            assert hashlib.sha256(str(minor_expr).encode()).hexdigest() == expected_hash
            generic_results.append({"factor": index, "branch": branch_index, "rows": list(rows), "unit": True})

    content_cases = {
        "p0_qquad_a0": (0, q**2 - 2 * q + 2, 0),
        "p0_qquad_a53": (0, q**2 - 2 * q + 2, sp.Rational(5, 3)),
        "p1_qq_a2": (1, q**2 + 1, 2),
        "pm1": (-1, q**4 - sp.Rational(16, 5) * q**3 + 6 * q**2 - sp.Rational(16, 5) * q + 1, -sp.Rational(5, 9) * q**3 + sp.Rational(2, 3) * q**2 - q / 3 - sp.Rational(14, 9)),
        "phalf": (sp.Rational(1, 2), q**4 - 2 * q**3 + sp.Rational(3, 2) * q**2 - q / 2 + sp.Rational(5, 8), -sp.Rational(8, 9) * q**3 + sp.Rational(4, 3) * q**2 + sp.Rational(5, 18)),
    }
    expected_bases = {
        0: [a**2 * q**2 - sp.Rational(5, 3) * a * q**2, q**4 - 2 * q**3 + 2 * q**2],
        1: [a**3 - sp.Rational(8, 3) * a**2 + sp.Rational(4, 3) * a, a * q**2 - 2 * a * q + a - 2 * q**2 + 4 * q - 2, q**4 - 2 * q**3 + 2 * q**2 - 2 * q + 1],
        -1: [a + sp.Rational(5, 9) * q**3 - sp.Rational(2, 3) * q**2 + q / 3 + sp.Rational(14, 9), q**4 - sp.Rational(16, 5) * q**3 + 6 * q**2 - sp.Rational(16, 5) * q + 1],
        sp.Rational(1, 2): [a + sp.Rational(8, 9) * q**3 - sp.Rational(4, 3) * q**2 - sp.Rational(5, 18), q**4 - 2 * q**3 + sp.Rational(3, 2) * q**2 - q / 2 + sp.Rational(5, 8)],
    }
    content_results = []
    for value, expected in expected_bases.items():
        actual = list(sp.groebner([q6_poly.subs(p, value), f28.subs(p, value), f31.subs(p, value)], a, q, order="lex", domain=QQ))
        assert actual == [sp.expand(expr) for expr in expected]
    delta = {
        "p-q": p - q,
        "d0": p + q - 1,
        "P": p**2 - p + 1,
        "L1": p**2 + 2 * p * q - 2 * p - q,
        "L2": 2 * p * q - p + q**2 - 2 * q,
        "e": 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2,
    }
    for label, (pvalue, qmod, avalue) in content_cases.items():
        ext = FiniteExtension(sp.Poly(qmod, q, domain=QQ).monic())
        patch_division(ext)
        rows, expected_hash = EXPECTED_CONTENT[label]
        matrix = direct_rows(leaf, rows)
        substitutions = {p: pvalue, a: avalue}
        specialized = [
            [specialize(matrix[row, column], substitutions, ext) for column in range(9)]
            for row in range(6)
        ]
        minor = determinant(
            [[specialized[row][column] for column in PIVOT_COLUMNS] for row in range(6)],
            ext.zero,
            ext.one,
        )
        assert minor * (minor**-1) == ext.one
        minor_expr = sp.cancel(ext.to_sympy(minor))
        assert hashlib.sha256(str(minor_expr).encode()).hexdigest() == expected_hash
        p6_matrix = direct_rows(leaf, OLD_P6_ROWS)
        p6_specialized = [
            [specialize(p6_matrix[row, column], substitutions, ext) for column in PIVOT_COLUMNS]
            for row in range(6)
        ]
        assert determinant(p6_specialized, ext.zero, ext.one) == ext.zero
        assert all(specialize(expr, substitutions, ext) != ext.zero for expr in delta.values())
        content_results.append({"label": label, "rows": list(rows), "unit": True, "old_P6_zero": True})

    # Independent QQ[q] gcd route for the same content witnesses.
    content_gcd_results = []
    for label, (pvalue, qmod, avalue) in content_cases.items():
        rows, _ = EXPECTED_CONTENT[label]
        determinant_expr = sp.cancel(
            direct_rows(leaf, rows)
            .extract(range(6), PIVOT_COLUMNS)
            .det(method="domain-ge")
            .subs({p: pvalue, a: avalue})
        )
        numerator, denominator = determinant_expr.as_numer_denom()
        modulus = sp.Poly(qmod, q, domain=QQ).monic()
        numerator_poly = sp.Poly(numerator, q, domain=QQ)
        denominator_poly = sp.Poly(denominator, q, domain=QQ)
        assert sp.gcd(numerator_poly, modulus).degree() == 0
        assert sp.gcd(denominator_poly, modulus).degree() == 0
        content_gcd_results.append(label)

    # Direct H2 correction, independent of generic Q6 division.
    h2 = 2 * p**2 - 2 * p + 1
    h2_ext = FiniteExtension(sp.Poly(h2, p, domain=QQ))
    patch_division(h2_ext)
    direct_h2 = gcd_extension(
        sp.Poly(q6_poly, q, domain=h2_ext),
        sp.Poly(resultant, q, domain=h2_ext),
        h2_ext,
    )
    assert len(direct_h2) == 2
    assert ext_poly_equal(
        sp.Poly(coeff_expr(direct_h2, h2_ext, q), q, domain=h2_ext),
        sp.Poly(p + q - 1, q, domain=h2_ext),
        h2_ext,
    )
    print("GLD95 independent sparse-support finite-residual audit: PASS")
    print(json.dumps({
        "status": "independent_exact_sparse_support_audit",
        "gld_identifier": "GLD95",
        "global_conjecture": "UNRESOLVED",
        "imports_primary": False,
        "imports_GLD71_builder": False,
        "imports_GLD88_builder": False,
        "support_rows": sorted(AUDIT_RELATIONS),
        "support_digest_sha256": support_digest(),
        "resultant": {
            "total_degree": resultant_poly.total_degree(),
            "degree_p": resultant_poly.degree(p),
            "degree_q": resultant_poly.degree(q),
            "srepr_sha256": resultant_hash,
            "q6_remainder_srepr_sha256": remainder_hash,
            "generic_division_denominator": str(sp.factor(remainder_den)),
        },
        "generic_unit_witnesses": generic_results,
        "content_unit_witnesses": content_results,
        "content_QQ_gcd_witnesses": content_gcd_results,
        "H2_direct_gcd": {"degree": 1, "gcd": "p+q-1", "generic_division_artifact": True},
        "scope_fences": [
            "written rational F88 formula family over D(Delta) only",
            "arbitrary H4 Q6 points outside F88 are not covered",
            "GLD75/GLD86 bridge and GLD88 kernel implication are upstream dependencies",
            "GLD83 Fitting pullback and global Krenn-Gu remain open",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }, indent=2))


if __name__ == "__main__":
    main()
