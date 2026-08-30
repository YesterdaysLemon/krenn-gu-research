#!/usr/bin/env python3
"""Exact primary certificate for the scoped GLD100 g0-gate removal.

The computation is deliberately split along the proof topology.  GLD96's
proved E31-open cross-resultant step first forces the leaf offset B to vanish.
This verifier then reconstructs the four B=0 C-coefficients from the canonical
GLD71 syndrome and GLD88 family, proves an exhaustive necessary p-cover, and
closes every retained fibre by exact quotient arithmetic or one of the direct
GLD97/GLD99-style seven-minors D0,D2.  GLD99 supplies H2=0 separately.

This proves only the normalized offset-chart implication documented by the
owning theorem.  It is not a global Krenn--Gu resolution.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
GLD96 = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py"
GLD95_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_"
    "EXCLUSION_THEOREM.md"
)
GLD95_VERIFIER = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_"
    "exclusion.py"
)
GLD96_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_"
    "EXCLUSION_THEOREM.md"
)
GLD99_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_"
    "SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md"
)
GLD99_VERIFIER = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_"
    "six_minor_offset_exclusion.py"
)

p, q, a, b, c, C = sp.symbols("p q a b c C")

PIVOT_ROWS = (0, 1, 2, 17, 25, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
TARGETS = ((28, 8), (32, 2), (32, 5), (33, 8))
MINORS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
EXPECTED_GLD99_OWNER_SHA256_16 = "f5fd49a6ff039f12"
EXPECTED_SOURCE_MANIFEST = {
    "GLD71_verifier": "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    "GLD88_verifier": "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    "GLD95_owner": "1c7074a3a6c6e740832f58c37757be8231f104fa8661c05476a516302e79e1c8",
    "GLD95_verifier": "2eef9d94f251dce77b36f8d4dde479928d43087828583c3d59e52dae58c280a1",
    "GLD96_owner": "2d989620d82554197ce7f85d603269122d58dfe07c36a9ab46121a2261aabcff",
    "GLD96_verifier": "05299523e510011f25ca1dcc59cb121b4ab3c8163576788ce7bba575835ce255",
    "GLD99_owner": "f5fd49a6ff039f128f83b89bc3a7019c201001c54ba33223b2ac71e3e2289708",
    "GLD99_verifier": "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
}

EXPECTED_Q6_SHA256 = (
    "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"
)
EXPECTED_GAMMAS = {
    "gamma0": {
        "sha256": "ecc04ca65bf325abe133e0d9dabe709f16d01cc8cb2ff4711d07c683cfc76531",
        "sparse_sha256": "a8730bca93a78aeebdfd6923d4c343d44b8968d4489cbfe8bb4426fd94f3d7f8",
        "terms": 308,
        "degrees": {"p": 27, "q": 3, "a": 2},
        "scale": "4*(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
        "raw_denominator": (
            "(p + q - 1)**2*(p**2 - p + 1)**2*"
            "(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)"
        ),
        "primitive_content": "3",
        "quotient_witness": {
            "numerator_remainder_sha256": "2c32e81d80dca6bd9d541e739ae2c25499f5d7364d747be7224e40cfd202a53d",
            "denominator_remainder_sha256": "577c742b24749fcbbf5ed1e7ff9eb05e7c4ea37f386345736d1adde06f9d783d",
            "inverse_sha256": "f8926c9d494160215b5771ac9070a841ac8b443a43c87e0f4c4dfb020a3a13d0",
            "reduced_sha256": "11eb76112dcdbe89ddcce8acc355c05acf20c9ba5ef0ba535e0880c406e99931",
            "relation_sha256": "23530d959f75d98a6920695b9878ab02e7e60304c6f88cfbc2911fddb0df1c03",
        },
    },
    "gamma1": {
        "sha256": "4db77cd0ce9882b9e2f2e7694805153b9e819a8da2e425a853ba427853c65d31",
        "sparse_sha256": "9e37dd630d8d74a363c4302067ca877070b96b0bf8ae05f6d324eda561a6e6a2",
        "terms": 484,
        "degrees": {"p": 32, "q": 3, "a": 3},
        "scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
        "raw_denominator": (
            "(p + q - 1)*(p**2 - p + 1)**2*"
            "(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2"
        ),
        "primitive_content": "3",
        "quotient_witness": {
            "numerator_remainder_sha256": "5a5df22117a69d752fbd927cebf370e69405f135f6aec1b9c976d752a73aa59c",
            "denominator_remainder_sha256": "087e2b33b2ca64bf4782041848bad66550da030b8cbc64e55b236fb52eb91529",
            "inverse_sha256": "c4f130c9d290435366facbbbe48fc9d1eaaaa4625ce89363dc47ca3a6a0fbffd",
            "reduced_sha256": "453e1b9a5d9d671ea1d8ab4e9ba1c8b78f4272dcab9e2a0b7c7edd671ad21b2f",
            "relation_sha256": "d9f1fdc4b8c6daa8bddd09e4b6413c2b7ae62ae966efa48a2e3a4461601105b7",
        },
    },
    "gamma2": {
        "sha256": "b1afa68aee1f50bf708082d6a9d2f2d6552dd222e6f69a6a5473747d11291232",
        "sparse_sha256": "88ecfc18dcc511a0c61dda5da0d4bdb208102bc0e6164d9019c19a05dc8bb3c8",
        "terms": 437,
        "degrees": {"p": 29, "q": 3, "a": 3},
        "scale": "16*(p**2 - p + 1)**5*(2*p**2 - 2*p + 1)**5",
        "raw_denominator": (
            "(p + q - 1)**2*(p**2 - p + 1)**2*"
            "(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)**2"
        ),
        "primitive_content": "3",
        "quotient_witness": {
            "numerator_remainder_sha256": "cccec3fd93ec6eee4f561f45ab345f8b7997170e14f0e2fbe9cfa170f22ac657",
            "denominator_remainder_sha256": "dbd173898d855e25030194eb94546c21bbaa1fddfeb92c248d50ba7c84dcddff",
            "inverse_sha256": "9189cb88297138a87f4cb6f7feb229467dea80431c3d8acf726e3064c7c91fdb",
            "reduced_sha256": "b419baf541c76083f1a598ddebded301f8540a5ea5e24c099988929cebb4f080",
            "relation_sha256": "b9e43cd1dfe9a4890d958a4647648fd335bfe819f303089b59f295f9d81e599c",
        },
    },
    "gamma3": {
        "sha256": "c171b5d7205afb6d719fe5b3464fa6347968f41e84b0a829c0a81dddfb4bdb2b",
        "sparse_sha256": "6103df0e6a9e7c1279fe00b58eb48974c792f1b80801f768b99d4146bf5fdc3c",
        "terms": 308,
        "degrees": {"p": 27, "q": 3, "a": 2},
        "scale": "(p**2 - p + 1)**3*(2*p**2 - 2*p + 1)**5",
        "raw_denominator": (
            "(p + q - 1)*(p**2 - p + 1)**2*"
            "(2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2)"
        ),
        "primitive_content": "3",
        "quotient_witness": {
            "numerator_remainder_sha256": "f9a906613efcece22b822a773f0bd0be5c680e19f2a3e596a3db1e37c1bebba6",
            "denominator_remainder_sha256": "279c88cab10a6b6c8e3cdbe342ba8f3b8fd75ceef4c5014738ac8fec8a416e6a",
            "inverse_sha256": "e58a7083918e517c01cecf470aeec91481aa4b292244988e828a4547ba1ef2c8",
            "reduced_sha256": "d769ee0cc8efb4ae7c62ee48a4e8104215384d3130ff52d5f487243518ed1cde",
            "relation_sha256": "5a6daf00b0bd95af7075876756f0e8a214cab166aab1b106496a3d3a04365baa",
        },
    },
}
EXPECTED_PAIRS = {
    "01": {
        "resultant_a_sha256": "f01526b8ade89e9474e3a9425f7a87220aa8599b694f2339a64ff1c2681f94e5",
        "remainder_sha256": "0c0abdc92c1b9479a265aa492060965cb046fcd8d13eb2d6c32b6d77fe4149a3",
        "remainder_terms": 576,
        "content": "p**3*(p**2 - p + 1)**10",
        "scale": "(2*p**2 - 2*p + 1)**12",
        "eliminant_degree": 544,
        "eliminant_sha256": "8f1666c2cc18c3c96b2eb2502533593ded9ef2870261c04be057b5a7d32ee32b",
        "primitive_clearing_sha256": "286f00a9f4bf1e3e54eaed31a96150ed95a9ccc1c2cff6ef08a15272f1118cb8",
    },
    "02": {
        "resultant_a_sha256": "a2db7ada8d86e3529cc58a617449c154f016b0b0fbaa209ae29860cd4d92a6fe",
        "remainder_sha256": "53e8eff8d4196bba8a65afa522da5410ca5f6193c99d41fb17efbb04406fe7f4",
        "remainder_terms": 580,
        "content": "(p**2 - p + 1)**10",
        "scale": "(2*p**2 - 2*p + 1)**12",
        "eliminant_degree": 552,
        "eliminant_sha256": "13f408ae39f9df64130f4ade389f3b1835ba6863278b303d0808fdeaf54f6ef7",
        "primitive_clearing_sha256": "d90854308021e1c939082fe69cd29891c2bbc5a790509f78af9aac8296f0f141",
    },
    "03": {
        "resultant_a_sha256": "b3bcbbddba13d6434a764aa7ff579fbfc075e10c523c65ae575e4b288e8d39c2",
        "remainder_sha256": "c3b126f686bd1e437710354e1134fd795ba14193df56a50ebd0eddd4c1a591c3",
        "remainder_terms": 418,
        "content": "p*(p**2 - p + 1)**8",
        "scale": "(2*p**2 - 2*p + 1)**9",
        "eliminant_degree": 406,
        "eliminant_sha256": "24ea888f45f850c676c4c89e01bfa01af72ead3abe01cd2103bab9d98f47767e",
        "primitive_clearing_sha256": "36d30092aa02c2bfa87d747c550eb92f894e890d94f285a7d51d6d597f9ab8b2",
    },
}
EXPECTED_FULL_GCD = {
    "degree": 374,
    "sha256": "f8bfaa97e9d980852df37e1c98bc82769aba0ab3a762452b55bb0696697d42d2",
    "radical_degree": 18,
    "radical_sha256": "dd930e75eaf842e522b08b661739c53693bb5a7de45414851651e36f291d4361",
    "factors": [
        ("p - 1", 44),
        ("p", 84),
        ("p**2 + 1", 1),
        ("p**2 - 2*p + 2", 3),
        ("p**2 - p + 1", 31),
        ("2*p**2 - 2*p + 1", 84),
        ("5*p**4 - 16*p**3 + 30*p**2 - 16*p + 5", 1),
        ("8*p**4 - 16*p**3 + 12*p**2 - 4*p + 5", 1),
    ],
}

# Frozen from the first complete canonical replay with serialized Bezout,
# quotient-unit, q-relation, direct-minor, and handoff records.  The comparison
# in ``check_fibres`` is deliberately unconditional.
EXPECTED_FIBRE_CERTIFICATE_HASHES: dict[str, dict[str, str]] = {
    "p_zero": {
        "q_certificate_sha256": "117cd8a1d34c049d7eccff67c109218dc04598bced324d70516d94b1a893c05c",
        "record_sha256": "ac040719033aadfe063a8d7e0476cbe4ea6346c481eca59e8cfd795e08aec28d",
    },
    "p_one": {
        "q_certificate_sha256": "33a09af34c9cbbbfa23bb121ec65b37c8f62b3dee5b18296e31bb39b37d3ef46",
        "record_sha256": "e7435826b6f83e266b0c7f33913b3f751a7beb34f82611a14e836f14a9246c19",
    },
    "p2_minus_2p_plus_2": {
        "q_certificate_sha256": "ff7800aa3c73d25cf6c32ec126aa5dcdc170ad77d897fdae611076173d31ac26",
        "gamma_certificate_sha256": "a621ea79ac02345a4791cc77758c00aaa40e54c54dc931c8251872a8dd79765b",
        "record_sha256": "9e09bba21de584cbdef71b87adea3434a061ba7a736bad2ed1fa2e2d560431c1",
    },
    "p2_plus_1": {
        "q_certificate_sha256": "f6c68d1dac6f1f3476608ab44b782f3e750b7479bc624a89ba5fe6109566ace0",
        "gamma_certificate_sha256": "09d20e32246d806291968abb6e75a159c171c64f59fe95e78b01245b79b79539",
        "record_sha256": "735e214db73cce1c3dab30796ceaf282a0488fc7635af70e4ed5aa5df129e43e",
    },
    "quartic_A": {
        "q_certificate_sha256": "91df50fd7f698a0f258dd0459345e63bec3e821a8b3b307477f3f70281da420a",
        "gamma_certificate_sha256": "6c7cb7ce998bfc2b3167ff026fa6c8f5888694649e771f06473a19864446767b",
        "record_sha256": "adcaae32f5078caa889a9371c63ef8d64c8f8b1978be1f6d6910f93ee5986a99",
    },
    "quartic_C": {
        "q_certificate_sha256": "9c1b9105f89f59817bb715a602191584ea565e674643c2818fc3311371fb59b1",
        "gamma_certificate_sha256": "90e35d6f039377616d5ffbe267f76689632d2db1d33b029f22936f27f33cab8b",
        "record_sha256": "44b7e8196324d80f376ec1665e30b727671fac95614261c87ddaa9dfda350676",
    },
    "P": {
        "Delta_quotient_sha256": "f1ca4fe15481291de51d3384a71ce629b75b1cd7b9ee288c04bd12f4af2e15a2",
        "record_sha256": "8b37f7b9ddacb578bbdde4c89509e551b3d59019da57635cbbce3868eaf800d0",
    },
    "H2": {
        "record_sha256": "164ff1a0d7fdbb93e68c34cbf6eafb8e669cac5205df888a9c337dd8a65494e2",
    },
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def digest(expression: sp.Expr) -> str:
    return hashlib.sha256(sp.srepr(sp.expand(expression)).encode()).hexdigest()


def digest_payload(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def rational_pair(value: object) -> list[int]:
    """Canonical exact serialization of one rational coefficient."""

    rational = QQ.convert(value)
    return [int(rational.numerator), int(rational.denominator)]


def domain_certificate(domain) -> dict[str, object]:
    """Describe the coefficient field and its fixed power basis."""

    if domain == QQ:
        return {"kind": "QQ", "degree": 1, "basis": ["1"]}
    degree = int(domain.mod.degree())
    return {
        "kind": "QQ_algebraic",
        "degree": degree,
        "alias": str(domain.ext),
        "basis_high_to_low": [
            f"{domain.ext}^{power}" if power > 1 else str(domain.ext) if power == 1 else "1"
            for power in range(degree - 1, -1, -1)
        ],
        "minimal_polynomial_coefficients_high_to_low": [
            rational_pair(coefficient)
            for coefficient in domain.ext.minpoly.all_coeffs()
        ],
    }


def field_element_certificate(value: object, domain) -> dict[str, object]:
    """Serialize a field element in the domain's declared power basis."""

    if domain == QQ:
        return {"coefficients_high_to_low": [rational_pair(QQ.from_sympy(sp.sympify(value)))]}
    element = domain.from_sympy(sp.sympify(value))
    degree = int(domain.mod.degree())
    coefficients = list(element.to_list())
    if len(coefficients) > degree:
        raise AssertionError(("field element exceeds power basis", element, degree))
    coefficients = [QQ.zero] * (degree - len(coefficients)) + coefficients
    return {
        "coefficients_high_to_low": [rational_pair(coefficient) for coefficient in coefficients]
    }


def polynomial_certificate(polynomial: sp.Poly) -> dict[str, object]:
    """Canonical sparse exact serialization over QQ or a declared number field."""

    domain = polynomial.domain
    return {
        "generators": [str(generator) for generator in polynomial.gens],
        "domain": domain_certificate(domain),
        "terms": [
            {
                "monomial": [int(exponent) for exponent in monomial],
                "coefficient": field_element_certificate(coefficient, domain),
            }
            for monomial, coefficient in polynomial.terms()
        ],
    }


def quotient_unit_certificate(
    expression: sp.Expr,
    factor: sp.Expr,
    *,
    label: str,
) -> dict[str, object]:
    """Give an exact inverse witness for ``expression`` in QQ[p]/(factor)."""

    modulus = sp.Poly(factor, p, domain=QQ).monic()
    value = sp.Poly(sp.cancel(expression), p, domain=QQ).rem(modulus)
    if value.is_zero:
        raise AssertionError((label, "zero modulo factor", factor))
    inverse = sp.invert(value, modulus)
    identity = (value * inverse).rem(modulus)
    one = sp.Poly(1, p, domain=QQ)
    if identity != one:
        raise AssertionError((label, "invalid quotient-field inverse", identity))
    payload = {
        "schema": "gld100-quotient-unit-v1",
        "label": label,
        "modulus": polynomial_certificate(modulus),
        "value_remainder": polynomial_certificate(value),
        "inverse_remainder": polynomial_certificate(inverse),
        "identity_remainder": polynomial_certificate(identity),
        "identity_verified": True,
    }
    return {**payload, "sha256": digest_payload(payload)}


def q_relation_certificate(
    reduced: sp.Expr,
    numerator: sp.Expr,
    denominator: sp.Expr,
    factor: sp.Expr,
    *,
    label: str,
) -> dict[str, object]:
    """Certify a rational q-relation and its denominator on one p-fibre."""

    modulus = sp.Poly(factor, p, domain=QQ).monic()
    relation = sp.Poly(
        sp.expand(denominator * reduced - numerator), p, domain=QQ
    ).rem(modulus)
    if not relation.is_zero:
        raise AssertionError((label, "q relation mismatch", relation))
    denominator_unit = quotient_unit_certificate(
        denominator, factor, label=f"{label}_denominator"
    )
    payload = {
        "schema": "gld100-q-relation-v1",
        "label": label,
        "reduced_representative": polynomial_certificate(
            sp.Poly(reduced, p, domain=QQ).rem(modulus)
        ),
        "rational_numerator": polynomial_certificate(
            sp.Poly(numerator, p, domain=QQ).rem(modulus)
        ),
        "rational_denominator": polynomial_certificate(
            sp.Poly(denominator, p, domain=QQ).rem(modulus)
        ),
        "cross_multiplication_remainder": polynomial_certificate(relation),
        "cross_multiplication_verified": True,
        "denominator_unit": denominator_unit,
    }
    return {**payload, "sha256": digest_payload(payload)}


def lf_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def source_manifest() -> dict[str, str]:
    paths = {
        "GLD71_verifier": GLD71,
        "GLD88_verifier": GLD88,
        "GLD95_owner": GLD95_OWNER,
        "GLD95_verifier": GLD95_VERIFIER,
        "GLD96_owner": GLD96_OWNER,
        "GLD96_verifier": GLD96,
        "GLD99_owner": GLD99_OWNER,
        "GLD99_verifier": GLD99_VERIFIER,
    }
    actual = {name: lf_sha256(path) for name, path in paths.items()}
    if actual != EXPECTED_SOURCE_MANIFEST:
        raise AssertionError(("source manifest drift", actual, EXPECTED_SOURCE_MANIFEST))
    return actual


def q6_polynomial() -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


def delta_polynomial() -> sp.Expr:
    d0 = p + q - 1
    return (
        (p - q)
        * d0
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * (2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2)
    )


def support_digest(gld71) -> str:
    encoded = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in gld71.SPARSE_RELATIONS[row]],
        ]
        for row in SUPPORT_ROWS
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()


def quotient_reduce(expression: sp.Expr, modulus: sp.Poly, field):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    numerator_poly = sp.Poly(numerator, q, domain=field).rem(modulus)
    denominator_poly = sp.Poly(denominator, q, domain=field).rem(modulus)
    if denominator_poly.is_zero:
        raise AssertionError("denominator vanished modulo Q6")
    inverse = sp.invert(denominator_poly, modulus)
    if (denominator_poly * inverse).rem(modulus) != sp.Poly(1, q, domain=field):
        raise AssertionError("invalid exact denominator inverse")
    reduced_poly = (numerator_poly * inverse).rem(modulus)
    if (denominator_poly * reduced_poly - numerator_poly).rem(modulus) != 0:
        raise AssertionError("invalid exact quotient reduction")
    witness = {
        "numerator_remainder_sha256": digest(numerator_poly.as_expr()),
        "denominator_remainder_sha256": digest(denominator_poly.as_expr()),
        "inverse_sha256": digest(inverse.as_expr()),
        "reduced_sha256": digest(reduced_poly.as_expr()),
        "relation_sha256": digest_payload(
            [
                sp.srepr(numerator_poly.as_expr()),
                sp.srepr(denominator_poly.as_expr()),
                sp.srepr(inverse.as_expr()),
                sp.srepr(reduced_poly.as_expr()),
            ]
        ),
    }
    return sp.cancel(reduced_poly.as_expr()), witness


def primitive_clear(expression: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    polynomial = sp.Poly(sp.cancel(expression), q, domain=QQ.frac_field(p, a))
    denominators = [sp.cancel(value).as_numer_denom()[1] for value in polynomial.all_coeffs()]
    scale = sp.lcm(denominators)
    cleared = sp.Poly(sp.cancel(scale * polynomial.as_expr()), p, q, a, domain=QQ)
    content, primitive = cleared.primitive()
    primitive_expression = sp.expand(primitive.as_expr())
    if sp.cancel(scale * expression - content * primitive_expression) != 0:
        raise AssertionError("invalid primitive-clearing identity")
    return primitive_expression, sp.factor(scale), content


def sparse_payload(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> dict[str, object]:
    """Canonical exact sparse encoding, independent of SymPy's printer tree."""

    polynomial = sp.Poly(expression, *variables, domain=QQ)
    terms = []
    for monomial, coefficient in polynomial.terms():
        rational = sp.Rational(coefficient)
        terms.append([list(monomial), int(rational.p), int(rational.q)])
    return {
        "variables": [str(variable) for variable in variables],
        "domain": "QQ",
        "terms": terms,
    }


def metadata(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> dict[str, object]:
    polynomial = sp.Poly(expression, *variables, domain=QQ)
    sparse = sparse_payload(polynomial.as_expr(), variables)
    return {
        "sha256": digest(polynomial.as_expr()),
        "sparse_sha256": digest_payload(sparse),
        "terms": len(polynomial.terms()),
        "degrees": {str(variable): polynomial.degree(variable) for variable in variables},
    }


def reconstruct_gammas(gld71, gld88, gld96):
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    if len(relations) != 37 or support_digest(gld71) != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError("canonical GLD71 support drift")
    leaf = sp.Matrix(
        [[1, 1, 1], [p, q, (p + q - p * q) / (p + q - 1)], [a, 1 + b, 1 + c]]
    )
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    if syndrome.shape != (37, 9):
        raise AssertionError(syndrome.shape)
    # Recompute the 111 GLD88 common-kernel identities.  They imply rank at
    # most six at B=C=0, hence the constant term of every bordered seven-minor
    # below vanishes without an expensive second determinant expansion.
    kernel_record = gld96.check_f88_kernel(syndrome, gld88, (p, q, a, b, c))
    if kernel_record.get("identity_count") != 111:
        raise AssertionError(("F88 kernel drift", kernel_record))
    family = gld88.h4_family(p, q, a)
    q6_expression = sp.expand(q6_polynomial())
    if sp.expand(q6_expression - gld96.q6_polynomial(p, q)) != 0:
        raise AssertionError("canonical GLD96 Q6 drift")
    if digest(q6_expression) != EXPECTED_Q6_SHA256:
        raise AssertionError("Q6 hash drift")
    field = QQ.frac_field(p, a)
    q6 = sp.Poly(q6_expression, q, domain=field).monic()

    records: dict[str, object] = {}
    gammas: list[sp.Expr] = []
    for index, (row, column) in enumerate(TARGETS):
        name = f"gamma{index}"
        print(f"[gld100] reconstruct {name}", file=sys.stderr, flush=True)
        determinant = sp.cancel(
            syndrome.extract((*PIVOT_ROWS, row), (*PIVOT_COLUMNS, column)).det(
                method="domain-ge"
            )
        )
        numerator, denominator = determinant.as_numer_denom()
        if denominator.has(c):
            raise AssertionError((name, "raw c-dependent denominator"))
        raw_c = sp.Poly(numerator, c, domain=QQ.poly_ring(p, q, a, b))
        if raw_c.degree() != 1:
            raise AssertionError((name, "raw c degree"))
        affine_reconstruction = sp.Poly(
            raw_c.nth(0) + c * raw_c.nth(1),
            c,
            domain=QQ.poly_ring(p, q, a, b),
        )
        if raw_c != affine_reconstruction:
            raise AssertionError((name, "raw affine reconstruction"))
        derivative = sp.cancel((raw_c.nth(1) / denominator).subs(b, family["b"]))
        raw_denominator = str(sp.factor(derivative.as_numer_denom()[1]))
        reduced, quotient_witness = quotient_reduce(derivative, q6, field)
        primitive, scale, content = primitive_clear(reduced)
        actual = {
            **metadata(primitive, (p, q, a)),
            "scale": str(scale),
            "raw_denominator": raw_denominator,
            "primitive_content": str(content),
            "quotient_witness": quotient_witness,
            "raw_c_affine": True,
        }
        pinned_actual = {
            key: actual[key] for key in EXPECTED_GAMMAS[name]
        }
        if pinned_actual != EXPECTED_GAMMAS[name]:
            raise AssertionError((name, actual, EXPECTED_GAMMAS[name]))
        gammas.append(primitive)
        records[name] = actual
    return family, gammas, q6_expression, records, kernel_record


def pair_projection(left: sp.Expr, right: sp.Expr, q6_expression: sp.Expr):
    resultant_a = sp.expand(sp.resultant(left, right, a))
    field = QQ.frac_field(p)
    modulus = sp.Poly(q6_expression, q, domain=field).monic()
    remainder = sp.Poly(resultant_a, q, domain=field).rem(modulus).as_expr()
    if sp.Poly(resultant_a - remainder, q, domain=field).rem(modulus) != 0:
        raise AssertionError("pair q-remainder identity failed")
    coefficients = sp.Poly(remainder, q, domain=field).all_coeffs()
    scale = sp.lcm([sp.cancel(value).as_numer_denom()[1] for value in coefficients])
    cleared = sp.Poly(sp.cancel(scale * remainder), q, domain=QQ.poly_ring(p))
    p_content, primitive_q = cleared.primitive()
    primitive_expression = sp.expand(primitive_q.as_expr())
    if sp.cancel(
        scale * remainder - p_content.as_expr() * primitive_expression
    ) != 0:
        raise AssertionError("pair primitive-clearing identity failed")
    eliminant = sp.Poly(
        sp.resultant(q6_expression, primitive_expression, q), p, domain=QQ
    )
    _rational_content, eliminant = eliminant.primitive()
    return {
        "resultant_a": resultant_a,
        "primitive_q_remainder": primitive_expression,
        "p_content": sp.Poly(p_content.as_expr(), p, domain=QQ),
        "scale": sp.factor(scale),
        "eliminant": eliminant,
        "remainder_identity": True,
        "primitive_clearing_identity": True,
        "primitive_clearing_sha256": digest_payload(
            [
                sp.srepr(scale),
                sp.srepr(remainder),
                sp.srepr(p_content.as_expr()),
                sp.srepr(primitive_expression),
            ]
        ),
    }


def factor_records(polynomial: sp.Poly) -> list[tuple[str, int]]:
    _unit, factors = sp.factor_list(polynomial.as_expr(), p)
    return [(str(factor), int(multiplicity)) for factor, multiplicity in factors]


def projection_cover(gammas: list[sp.Expr], q6_expression: sp.Expr):
    P = p**2 - p + 1
    H2 = 2 * p**2 - 2 * p + 1
    A4 = 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5
    C4 = 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5
    q6_over_qqp = sp.Poly(q6_expression, q, domain=QQ.poly_ring(p))
    if sp.expand(q6_over_qqp.LC() - H2) != 0:
        raise AssertionError("H2 is not LC_q(Q6)")
    pairs: dict[str, object] = {}
    for right_index in (3, 1, 2):
        name = f"0{right_index}"
        print(f"[gld100] pair projection {name}", file=sys.stderr, flush=True)
        record = pair_projection(gammas[0], gammas[right_index], q6_expression)
        expected = EXPECTED_PAIRS[name]
        actual = {
            "resultant_a_sha256": digest(record["resultant_a"]),
            "remainder_sha256": digest(record["primitive_q_remainder"]),
            "remainder_terms": len(sp.Poly(record["primitive_q_remainder"], p, q).terms()),
            "content": str(sp.factor(record["p_content"].as_expr())),
            "scale": str(record["scale"]),
            "eliminant_degree": record["eliminant"].degree(),
            "eliminant_sha256": digest(record["eliminant"].as_expr()),
            "primitive_clearing_sha256": record["primitive_clearing_sha256"],
        }
        pinned_actual = {key: actual[key] for key in expected}
        if pinned_actual != expected:
            raise AssertionError((name, actual, expected))
        pairs[name] = {**record, "metadata": actual}

    conditions = {
        name: (record["eliminant"] * record["p_content"].sqf_part()).monic()
        for name, record in pairs.items()
    }
    full_gcd = sp.gcd(sp.gcd(conditions["03"], conditions["01"]), conditions["02"]).monic()
    radical = full_gcd.sqf_part().monic()
    expected_radical = sp.Poly(
        p
        * (p - 1)
        * P
        * H2
        * (p**2 + 1)
        * (p**2 - 2 * p + 2)
        * A4
        * C4,
        p,
        domain=QQ,
    ).monic()
    if radical != expected_radical:
        raise AssertionError(("exact radical support identity", radical, expected_radical))
    delta = sp.Poly(delta_polynomial(), p, domain=QQ.poly_ring(q))
    if delta.rem(sp.Poly(P, p, domain=QQ.poly_ring(q))) != 0:
        raise AssertionError("P is not a displayed Delta factor")
    actual = {
        "degree": full_gcd.degree(),
        "sha256": digest(full_gcd.as_expr()),
        "radical_degree": radical.degree(),
        "radical_sha256": digest(radical.as_expr()),
        "factors": factor_records(full_gcd),
    }
    if actual != EXPECTED_FULL_GCD:
        raise AssertionError(("full necessary p cover", actual, EXPECTED_FULL_GCD))
    return pairs, full_gcd, radical, actual


def reduce_p(expression: sp.Expr, factor: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    domain = QQ.poly_ring(*variables)
    return sp.Poly(expression, p, domain=domain).rem(
        sp.Poly(factor, p, domain=domain)
    ).as_expr()


def number_field(factor: sp.Expr):
    factor_poly = sp.Poly(factor, p, domain=QQ)
    if not factor_poly.is_irreducible:
        raise AssertionError(("reducible candidate factor", factor))
    if factor_poly.degree() == 1:
        return QQ, sp.solve(factor, p)[0]
    domain = QQ.alg_field_from_poly(factor_poly, alias="r")
    return domain, domain.ext


def specialize(
    expression: sp.Expr,
    factor: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    domain,
    root,
) -> sp.Poly:
    reduced = reduce_p(expression, factor, variables)
    return sp.Poly(reduced.subs(p, root), *variables, domain=domain)


def bezout_gcd(
    polynomials: Iterable[sp.Poly],
) -> tuple[sp.Poly, list[sp.Poly], dict[str, object]]:
    values = list(polynomials)
    if not values:
        raise AssertionError("empty gcd family")
    variable = values[0].gens[0]
    domain = values[0].domain
    gcd_value = values[0]
    coefficients = [sp.Poly(1, variable, domain=domain)]
    for value in values[1:]:
        if value.is_zero:
            coefficients.append(sp.Poly(0, variable, domain=domain))
            continue
        left, right, next_gcd = sp.gcdex(gcd_value, value)
        coefficients = [coefficient * left for coefficient in coefficients]
        coefficients.append(right)
        gcd_value = next_gcd
    gcd_value = gcd_value.monic()
    total = sp.Poly(0, variable, domain=domain)
    for coefficient, value in zip(coefficients, values, strict=True):
        total += coefficient * value
    if total != gcd_value:
        raise AssertionError(("Bezout residual", total, gcd_value))
    payload = {
        "schema": "gld100-bezout-v1",
        "variable": str(variable),
        "domain": domain_certificate(domain),
        "sources": [polynomial_certificate(value) for value in values],
        "source_sha256": [
            digest_payload(polynomial_certificate(value)) for value in values
        ],
        "coefficients": [
            polynomial_certificate(coefficient) for coefficient in coefficients
        ],
        "gcd": polynomial_certificate(gcd_value),
        "identity": polynomial_certificate(total),
        "identity_verified": True,
    }
    return gcd_value, coefficients, {**payload, "sha256": digest_payload(payload)}


def q_fibre(
    name: str,
    factor: sp.Expr,
    q6_expression: sp.Expr,
    pairs: dict[str, object],
    gammas: list[sp.Expr],
    *,
    use_raw_resultants: bool = False,
):
    domain, root = number_field(factor)
    q6_specialized = specialize(q6_expression, factor, (q,), domain, root).monic()
    sources = []
    specialization_units: dict[str, object] = {}
    for pair_name in ("03", "01", "02"):
        expression = (
            pairs[pair_name]["resultant_a"]
            if use_raw_resultants
            else pairs[pair_name]["primitive_q_remainder"]
        )
        if not use_raw_resultants:
            specialization_units[pair_name] = {
                "p_content": quotient_unit_certificate(
                    pairs[pair_name]["p_content"].as_expr(),
                    factor,
                    label=f"{name}_{pair_name}_p_content",
                ),
                "clearing_scale": quotient_unit_certificate(
                    pairs[pair_name]["scale"],
                    factor,
                    label=f"{name}_{pair_name}_clearing_scale",
                ),
            }
        sources.append(specialize(expression, factor, (q,), domain, root))
    q_gcd, _coefficients, certificate = bezout_gcd([q6_specialized, *sources])
    return {
        "name": name,
        "factor": factor,
        "domain": domain,
        "root": root,
        "q_gcd": q_gcd,
        "q_certificate": certificate,
        "q_certificate_sha256": certificate["sha256"],
        "specialization_units": (
            specialization_units
            if not use_raw_resultants
            else {"mode": "raw_resultants_no_content_or_scale_removed"}
        ),
        "gammas": [specialize(gamma, factor, (a, q), domain, root) for gamma in gammas],
    }


def gamma_a_fibre(record: dict[str, object], q_root: sp.Expr):
    domain = record["domain"]
    gamma_a = [
        sp.Poly(gamma.as_expr().subs(q, q_root), a, domain=domain)
        for gamma in record["gammas"]
    ]
    gcd_value, _coefficients, certificate = bezout_gcd(gamma_a)
    return gcd_value, certificate, gamma_a


def direct_determinant(matrix: list[list[sp.Poly]], variable: sp.Symbol, domain) -> sp.Poly:
    zero = sp.Poly(0, variable, domain=domain)
    one = sp.Poly(1, variable, domain=domain)
    states: dict[int, sp.Poly] = {0: one}
    for row in matrix:
        next_states: dict[int, sp.Poly] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                available_before = sum(
                    1 for previous in range(column) if not (mask & (1 << previous))
                )
                term = value * entry
                if available_before & 1:
                    term = -term
                next_mask = mask | (1 << column)
                next_states[next_mask] = next_states.get(next_mask, zero) + term
        states = next_states
    return states[(1 << len(matrix)) - 1]


def direct_minor_fibre(
    gld71,
    family: dict[str, sp.Expr],
    factor: sp.Expr,
    q_expression: sp.Expr,
    a_expression: sp.Expr,
):
    print("[gld100-direct] construct number field", file=sys.stderr, flush=True)
    domain, root = number_field(factor)
    q_value = sp.cancel(q_expression.subs(p, root))
    a_value = sp.cancel(a_expression.subs(p, root))
    substitution = {p: root, q: q_value, a: a_value}
    print("[gld100-direct] check Q6/Delta and F88 coordinates", file=sys.stderr, flush=True)
    q6_value = sp.cancel(q6_polynomial().subs(substitution))
    if sp.Poly(q6_value, C, domain=domain).as_expr() != 0:
        raise AssertionError("candidate q relation is not on Q6")
    delta_value = sp.Poly(
        sp.cancel(delta_polynomial().subs(substitution)), C, domain=domain
    )
    if delta_value.is_zero:
        raise AssertionError("direct-minor candidate lies on Delta")
    family_values = {
        key: sp.cancel(value.subs(substitution)) for key, value in family.items()
    }
    leaf_expressions = [
        [1, 1, 1],
        [root, q_value, family_values["s"]],
        [a_value, 1 + family_values["b"], 1 + family_values["c"] + C],
    ]
    leaf = [
        [sp.Poly(entry, C, domain=domain) for entry in row]
        for row in leaf_expressions
    ]
    print("[gld100-direct] build sparse syndrome rows", file=sys.stderr, flush=True)
    needed_rows = sorted({row for rows, _columns in MINORS.values() for row in rows})
    syndrome: dict[int, list[sp.Poly]] = {}
    zero = sp.Poly(0, C, domain=domain)
    for relation_row in needed_rows:
        entries: list[sp.Poly] = []
        for root_index in range(3):
            for component in range(3):
                total = zero
                for indices, coefficient in gld71.SPARSE_RELATIONS[relation_row]:
                    if indices[0] != root_index:
                        continue
                    total += (
                        coefficient
                        * leaf[indices[1]][component]
                        * leaf[indices[2]][component]
                        * leaf[indices[3]][component]
                    )
                entries.append(total)
        syndrome[relation_row] = entries
    minors: dict[str, sp.Poly] = {}
    for name, (rows, columns) in MINORS.items():
        print(f"[gld100-direct] determinant {name}", file=sys.stderr, flush=True)
        matrix = [[syndrome[row][column] for column in columns] for row in rows]
        minors[name] = direct_determinant(matrix, C, domain)
    return domain, root, q_value, a_value, delta_value, minors


def direct_case_definitions() -> dict[str, dict[str, sp.Expr | str]]:
    A4 = 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5
    C4 = 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5
    return {
        "p2_plus_1": {
            "factor": p**2 + 1,
            "q_relation": -p,
            "q_numerator": -p,
            "q_denominator": sp.Integer(1),
            "a_relation": sp.Integer(0),
            "expected_gamma": a,
            "minor": "D0",
            "lambda": 192 * (1 - p),
        },
        "quartic_A": {
            "factor": A4,
            # Canonical representative of (2p-1)/(p-2) modulo A4.
            "q_relation": (
                sp.Rational(2, 3)
                - sp.Rational(6, 5) * p
                + sp.Rational(2, 5) * p**2
                - sp.Rational(1, 3) * p**3
            ),
            "q_numerator": 2 * p - 1,
            "q_denominator": p - 2,
            "a_relation": sp.Integer(0),
            "expected_gamma": a,
            "minor": "D0",
            "lambda": -sp.Rational(7776, 3125)
            * (p + 1)
            * (8171 * p**2 - 5068 * p + 1965),
        },
        "quartic_C": {
            "factor": C4,
            # Canonical representative of (p+1)/(2p-1) modulo C4.
            "q_relation": (
                sp.Rational(2, 3)
                - p
                + 2 * p**2
                - sp.Rational(4, 3) * p**3
            ),
            "q_numerator": p + 1,
            "q_denominator": 2 * p - 1,
            "a_relation": p,
            "expected_gamma": a - p,
            "minor": "D2",
            "lambda": sp.Rational(243, 128)
            * (p - 1)
            * (52 * p**2 + 2 * p + 25),
        },
    }


def direct_fibre_certificate(name: str) -> dict[str, object]:
    """Fresh-process direct determinant certificate for one residual fibre."""

    if name not in direct_case_definitions():
        raise AssertionError(("unknown direct fibre", name))
    print(f"[gld100-direct] start {name}", file=sys.stderr, flush=True)
    source_manifest()
    gld71 = load(GLD71, f"gld71_for_gld100_direct_{name}")
    if support_digest(gld71) != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError("canonical GLD71 support drift in direct fibre")
    gld88 = load(GLD88, f"gld88_for_gld100_direct_{name}")
    family = gld88.h4_family(p, q, a)
    case = direct_case_definitions()[name]
    domain, root, q_value, a_value, delta_value, minors = direct_minor_fibre(
        gld71,
        family,
        case["factor"],
        case["q_relation"],
        case["a_relation"],
    )
    print(f"[gld100-direct] validate {name}", file=sys.stderr, flush=True)
    for t_name in ("T0", "T1", "T2", "T3"):
        if not minors[t_name].is_zero:
            raise AssertionError((name, t_name, minors[t_name]))
    expected_lambda = sp.Poly(
        case["lambda"].subs(p, root) * C**2, C, domain=domain
    )
    selected = str(case["minor"])
    if minors[selected] != expected_lambda:
        raise AssertionError((name, selected, minors[selected], expected_lambda))
    if expected_lambda.nth(2) == 0:
        raise AssertionError((name, "nonunit direct coefficient"))
    q_relation = q_relation_certificate(
        case["q_relation"],
        case["q_numerator"],
        case["q_denominator"],
        case["factor"],
        label=f"{name}_q",
    )
    delta_unit = quotient_unit_certificate(
        delta_polynomial().subs(q, case["q_relation"]),
        case["factor"],
        label=f"{name}_Delta",
    )
    lambda_unit = quotient_unit_certificate(
        case["lambda"], case["factor"], label=f"{name}_{selected}_lambda"
    )
    minor_records = {
        minor_name: {
            "degree_C": None if minor.is_zero else int(minor.degree()),
            "terms": len(minor.terms()),
            "expression": str(minor.as_expr()),
            "sha256": digest(minor.as_expr()),
            "canonical": polynomial_certificate(minor),
        }
        for minor_name, minor in minors.items()
    }
    return {
        "name": name,
        "factor": str(case["factor"]),
        "field": str(domain),
        "q": str(q_value),
        "a": str(a_value),
        "Delta": str(delta_value.as_expr()),
        "Delta_nonzero": True,
        "Delta_unit": delta_unit,
        "q_relation_certificate": q_relation,
        "selected_minor": selected,
        "selected_identity": str(expected_lambda.as_expr()),
        "selected_identity_canonical": polynomial_certificate(expected_lambda),
        "selected_sha256": digest(expected_lambda.as_expr()),
        "selected_coefficient_unit": lambda_unit,
        "all_T_zero": True,
        "minors": minor_records,
    }


def direct_fibre_subprocess(name: str) -> dict[str, object]:
    """Isolate direct determinants from the large resultant process state."""

    completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--direct-fibre", name],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=900,
    )
    return json.loads(completed.stdout)


def expected_q_gcd(record: dict[str, object], expression: sp.Expr) -> None:
    domain = record["domain"]
    root = record["root"]
    expected = sp.Poly(expression.subs(p, root), q, domain=domain).monic()
    if record["q_gcd"] != expected:
        raise AssertionError((record["name"], record["q_gcd"], expected))


def check_fibres(gld71, family, gammas, q6_expression, pairs):
    P = p**2 - p + 1
    H2 = 2 * p**2 - 2 * p + 1
    A4 = 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5
    C4 = 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5
    records: dict[str, object] = {}

    # p=0 has removed p-content, so replay the raw pair resultants directly.
    print("[gld100] fibre p=0", file=sys.stderr, flush=True)
    p0 = q_fibre("p_zero", p, q6_expression, pairs, gammas, use_raw_resultants=True)
    expected_q_gcd(p0, q**2)
    delta0 = sp.Poly(delta_polynomial().subs(p, 0), q, domain=QQ)
    delta0_quotient, delta0_remainder = sp.div(delta0, p0["q_gcd"])
    if not delta0_remainder.is_zero:
        raise AssertionError("p=0 survivor is not contained in Delta")
    records["p_zero"] = {
        "q_gcd": str(p0["q_gcd"].as_expr()),
        "q_certificate": p0["q_certificate"],
        "q_certificate_sha256": p0["q_certificate_sha256"],
        "pair_specialization_units": p0["specialization_units"],
        "contained_in_Delta": True,
        "Delta_quotient": polynomial_certificate(delta0_quotient),
    }

    print("[gld100] fibre p=1", file=sys.stderr, flush=True)
    p1 = q_fibre("p_one", p - 1, q6_expression, pairs, gammas)
    expected_q_gcd(p1, (q - 1) ** 2)
    delta1 = sp.Poly(delta_polynomial().subs(p, 1), q, domain=QQ)
    delta1_quotient, delta1_remainder = sp.div(delta1, p1["q_gcd"])
    if not delta1_remainder.is_zero:
        raise AssertionError("p=1 survivor is not contained in Delta")
    records["p_one"] = {
        "q_gcd": str(p1["q_gcd"].as_expr()),
        "q_certificate": p1["q_certificate"],
        "q_certificate_sha256": p1["q_certificate_sha256"],
        "pair_specialization_units": p1["specialization_units"],
        "contained_in_Delta": True,
        "Delta_quotient": polynomial_certificate(delta1_quotient),
    }

    print("[gld100] fibre p^2-2p+2", file=sys.stderr, flush=True)
    quadratic_unit = q_fibre(
        "p2_minus_2p_plus_2", p**2 - 2 * p + 2, q6_expression, pairs, gammas
    )
    expected_q_gcd(quadratic_unit, q + p - 2)
    q_root = 2 - quadratic_unit["root"]
    gamma_gcd, gamma_certificate, _gamma_a = gamma_a_fibre(quadratic_unit, q_root)
    if gamma_gcd.degree() != 0:
        raise AssertionError(("quadratic unit gamma gcd", gamma_gcd))
    quadratic_q_relation = q_relation_certificate(
        2 - p,
        2 - p,
        sp.Integer(1),
        p**2 - 2 * p + 2,
        label="p2_minus_2p_plus_2_q",
    )
    quadratic_delta_unit = quotient_unit_certificate(
        delta_polynomial().subs(q, 2 - p),
        p**2 - 2 * p + 2,
        label="p2_minus_2p_plus_2_Delta",
    )
    records["p2_minus_2p_plus_2"] = {
        "q_gcd": str(quadratic_unit["q_gcd"].as_expr()),
        "q_certificate": quadratic_unit["q_certificate"],
        "q_certificate_sha256": quadratic_unit["q_certificate_sha256"],
        "pair_specialization_units": quadratic_unit["specialization_units"],
        "gamma_gcd": "1",
        "gamma_certificate": gamma_certificate,
        "gamma_certificate_sha256": gamma_certificate["sha256"],
        "q_relation_certificate": quadratic_q_relation,
        "Delta_unit": quadratic_delta_unit,
    }

    direct_cases = direct_case_definitions()
    for name, case in direct_cases.items():
        print(f"[gld100] fibre {name} q/gamma", file=sys.stderr, flush=True)
        factor = case["factor"]
        fibre = q_fibre(name, factor, q6_expression, pairs, gammas)
        relation_certificate = q_relation_certificate(
            case["q_relation"],
            case["q_numerator"],
            case["q_denominator"],
            factor,
            label=f"{name}_q",
        )
        expected_q_gcd(
            fibre,
            sp.together(q - case["q_relation"]).as_numer_denom()[0],
        )
        q_root = sp.cancel(case["q_relation"].subs(p, fibre["root"]))
        gamma_gcd, gamma_certificate, _gamma_a = gamma_a_fibre(fibre, q_root)
        expected_gamma = sp.Poly(
            case["expected_gamma"].subs(p, fibre["root"]),
            a,
            domain=fibre["domain"],
        ).monic()
        if gamma_gcd != expected_gamma:
            raise AssertionError((name, "gamma gcd", gamma_gcd, expected_gamma))
        print(f"[gld100] fibre {name} direct minors", file=sys.stderr, flush=True)
        direct_payload = direct_fibre_subprocess(name)
        records[name] = {
            "q_gcd": str(fibre["q_gcd"].as_expr()),
            "q_certificate": fibre["q_certificate"],
            "q_certificate_sha256": fibre["q_certificate_sha256"],
            "pair_specialization_units": fibre["specialization_units"],
            "gamma_gcd": str(gamma_gcd.as_expr()),
            "gamma_certificate": gamma_certificate,
            "gamma_certificate_sha256": gamma_certificate["sha256"],
            "q_relation_certificate": relation_certificate,
            "direct": direct_payload,
        }

    delta_in_p = sp.Poly(delta_polynomial(), p, domain=QQ.poly_ring(q))
    P_poly = sp.Poly(P, p, domain=QQ.poly_ring(q))
    P_quotient, P_remainder = sp.div(delta_in_p, P_poly)
    if not P_remainder.is_zero:
        raise AssertionError("P is not an exact Delta factor")
    records["P"] = {
        "factor": str(P),
        "excluded_by_Delta": True,
        "Delta_quotient": str(sp.factor(P_quotient.as_expr())),
        "Delta_quotient_canonical": sparse_payload(P_quotient.as_expr(), (p, q)),
        "Delta_quotient_sha256": digest(P_quotient.as_expr()),
    }
    records["H2"] = {
        "factor": str(H2),
        "supplied_by": "GLD99",
        "owner_sha256_16": lf_sha256(GLD99_OWNER)[:16],
    }
    if records["H2"]["owner_sha256_16"] != EXPECTED_GLD99_OWNER_SHA256_16:
        raise AssertionError(("GLD99 owner drift", records["H2"]))

    for record in records.values():
        if not isinstance(record, dict):
            raise AssertionError(("non-dictionary fibre record", record))
        record["record_sha256"] = digest_payload(record)

    actual_hashes = {
        name: {
            key: value
            for key, value in record.items()
            if key.endswith("sha256")
        }
        for name, record in records.items()
        if isinstance(record, dict)
    }
    if actual_hashes != EXPECTED_FIBRE_CERTIFICATE_HASHES:
        raise AssertionError(
            ("fibre certificate hash drift", actual_hashes, EXPECTED_FIBRE_CERTIFICATE_HASHES)
        )
    return records, actual_hashes


def check() -> dict[str, object]:
    started = time.monotonic()
    manifest = source_manifest()
    gld71 = load(GLD71, "gld71_for_gld100_primary")
    gld88 = load(GLD88, "gld88_for_gld100_primary")
    gld96 = load(GLD96, "gld96_for_gld100_primary")
    if not GLD99_OWNER.is_file():
        raise AssertionError(GLD99_OWNER)
    family, gammas, q6_expression, gamma_records, kernel_record = reconstruct_gammas(
        gld71, gld88, gld96
    )
    pairs, full_gcd, radical, cover_record = projection_cover(gammas, q6_expression)
    fibres, fibre_hashes = check_fibres(
        gld71, family, gammas, q6_expression, pairs
    )
    return {
        "status": "exact_scoped_g0_gate_removal_certificate",
        "gld_identifier": "GLD100",
        "field": "Q_characteristic_zero_then_C",
        "schema": "gld100-g0-primary-v1",
        "sympy_version": sp.__version__,
        "source_manifest": manifest,
        "global_conjecture": "UNRESOLVED",
        "scope": (
            "normalized GLD96/GLD88 F88-offset H4 Q6 chart; the primary "
            "generic implication is on D(E31*H2*Delta), while GLD99 supplies "
            "H2=0 and yields the combined normalized implication on "
            "D(E31*Delta); physical incidence additionally retains D(Omega)"
        ),
        "support_digest": EXPECTED_SUPPORT_DIGEST,
        "q6_sha256": EXPECTED_Q6_SHA256,
        "f88_kernel": kernel_record,
        "gammas": gamma_records,
        "pair_projections": {
            name: record["metadata"] for name, record in pairs.items()
        },
        "necessary_p_cover": {
            **cover_record,
            "full_gcd_expression_omitted_from_stdout": True,
            "radical_expression": str(sp.factor(radical.as_expr())),
            "logical_role": (
                "necessary projection cover only; every listed fibre is "
                "closed separately below"
            ),
        },
        "fibres": fibres,
        "fibre_certificate_hashes": fibre_hashes,
        "upstream": {
            "GLD96": "E31-open B=0 cross-resultant step",
            "GLD99": "H2=0 six-minor offset closure",
            "GLD95": "F88 endpoint after B=C=0",
        },
        "conclusion": (
            "On the normalized chart, rank at most six plus Q6 and "
            "D(E31*Delta) forces B=C=0 after the GLD99 H2 handoff; the "
            "corresponding physical incidence is empty only after D(Omega) "
            "and the GLD95 endpoint."
        ),
        "retained_frontier": [
            "E31=0",
            "Delta=0",
            "Omega=0 for the physical incidence conclusion",
            "arbitrary H4 Q6 points outside the written F88-offset chart",
            "GLD83 pulled-back Fitting ideal",
            "other charts, components, gauges, source branches, roots, and orders",
            "global Krenn-Gu resolution",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--direct-fibre":
        print(json.dumps(direct_fibre_certificate(sys.argv[2]), sort_keys=True))
        return 0
    if len(sys.argv) != 1:
        raise SystemExit("usage: verifier.py [--direct-fibre NAME]")
    result = check()
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    print("GLD100 g0 gate-removal exact certificate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
