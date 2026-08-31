#!/usr/bin/env python3
"""Verify the generic symbolic-a GLD103 all-zero coefficient branch.

This is a tracked, exact verifier for the following *necessary* implication on
the normalized GLD88/F88 H4--Q6 chart.  Over characteristic zero, with
``rank(M(G)) <= 6``, ``B*H2*Delta != 0``, and

    G_T0 = G_T1 = G_T2 = G_Y1 = G_X3 = 0,

the branch is empty.  The calculation reconstructs the 37-by-9 syndrome from
the committed GLD70/GLD71 support and GLD88 symbolic chart, computes the five
actual seven-minors, and derives the six quadratic coefficient rows.  Exact
python-flint resultants give the p-cover; exact local fibre ledgers close its
remaining factors.  The rank-to-minor implication is one-way.  No E31
equation is imposed or inverted, and the global Krenn--Gu conjecture remains
UNRESOLVED.

``--manifest-only`` performs only cheap source/contract checks.  The
``--bridge-only`` mode reconstructs the actual minors and coefficient rows.
``--targeted-p2-minus`` and ``--targeted-f40`` replay one local leaf into a
temporary certificate, without touching the durable certificate unless the
caller explicitly selects that output path.  The default full mode additionally
runs the exact p-cover and the recorded local fibre checks; it needs
python-flint 0.9.0 and can take several minutes.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / "GLD103_ALL_ZERO_COEFFICIENT_BRANCH_CERTIFICATE.json"
GLD70 = BASE / "verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
EXPLORE = BASE / "explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py"
GLD102 = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py"

p, a, q, B, C, z = sp.symbols("p a q B C z")
K = QQ.frac_field(p, a)

P = sp.expand(p**2 - p + 1)
H2 = sp.expand(2 * p**2 - 2 * p + 1)
RANK_DENOMINATOR = sp.expand(
    2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
)
DELTA = sp.expand(
    (p - q)
    * (p + q - 1)
    * P
    * (p**2 + 2 * p * q - 2 * p - q)
    * (2 * p * q - p + q**2 - 2 * q)
    * RANK_DENOMINATOR
)


def _monic_factor(expression: object, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=QQ)
    if polynomial.is_zero:
        raise AssertionError("zero denominator factor")
    return sp.expand(polynomial.monic().as_expr())


def _supported_denominator(
    denominator: object,
    variables: tuple[sp.Symbol, ...],
    allowed: tuple[sp.Expr, ...],
    label: str,
) -> dict[str, Any]:
    """Factor a denominator and prove every nonconstant factor is allowed."""
    denominator = sp.factor(sp.sympify(denominator))
    if denominator == 0:
        raise AssertionError((label, "zero denominator"))
    unsupported_symbols = denominator.free_symbols.difference(variables)
    if unsupported_symbols:
        raise AssertionError((label, "denominator has unsupported symbols", unsupported_symbols))
    allowed_keys = {_monic_factor(value, variables) for value in allowed}
    _content, factors = sp.factor_list(denominator, *variables)
    records = []
    for factor, exponent in factors:
        key = _monic_factor(factor, variables)
        if key not in allowed_keys:
            raise AssertionError((label, "unsupported denominator factor", factor, denominator))
        records.append({"factor": str(key), "exponent": int(exponent)})
    return {
        "denominator": str(denominator),
        "factorization": records,
        "supported": True,
        "support_basis": label,
    }


def _chart_denominator_provenance(denominator: object) -> dict[str, Any]:
    # Every q-dependent chart factor is a factor of Delta; P is included as
    # the explicit Delta factor and H2 is the Q6 leading coefficient.
    result = _supported_denominator(
        denominator,
        (p, q),
        (
            p - q,
            p + q - 1,
            P,
            p**2 + 2 * p * q - 2 * p - q,
            2 * p * q - p + q**2 - 2 * q,
            RANK_DENOMINATOR,
            H2,
        ),
        "Delta factors plus Q6 leading H2",
    )
    delta_keys = {
        str(_monic_factor(value, (p, q)))
        for value in (
            p - q,
            p + q - 1,
            P,
            p**2 + 2 * p * q - 2 * p - q,
            2 * p * q - p + q**2 - 2 * q,
            RANK_DENOMINATOR,
        )
    }
    h2_key = str(_monic_factor(H2, (p, q)))
    for factor_record in result["factorization"]:
        if factor_record["factor"] not in delta_keys and factor_record["factor"] != h2_key:
            raise AssertionError(("chart denominator is not supported by Delta/H2", factor_record))
    result["delta_factor_support_checked"] = True
    result["q6_leading_H2_support_checked"] = True
    result["P_divides_Delta_checked"] = sp.cancel(DELTA / P).is_polynomial(p, q)
    if not result["P_divides_Delta_checked"]:
        raise AssertionError("P is not a factor of Delta")
    return result


def _quotient_denominator_provenance(denominator: object) -> dict[str, Any]:
    # Once the Q6 quotient has been reduced, all remaining p-only
    # denominators must come from P or the Q6 leading coefficient H2.
    result = _supported_denominator(
        denominator,
        (p,),
        (P, H2),
        "p-only quotient factors P/H2 (P divides Delta)",
    )
    result["P_divides_Delta_checked"] = sp.cancel(DELTA / P).is_polynomial(p, q)
    if not result["P_divides_Delta_checked"]:
        raise AssertionError("P is not a factor of Delta")
    return result

MINOR_ORDER = ("T0", "T1", "T2", "Y1", "X3")
MINOR_DATA = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}
SELECTED_TRIPLES = {
    "D012": (0, 1, 2),
    "D013": (0, 1, 3),
    "D023": (0, 2, 3),
    "D123": (1, 2, 3),
    "D014": (0, 1, 4),
    "D015": (0, 1, 5),
}
FIBRE_TRIPLES = {
    "D134": (1, 3, 4),
    "D145": (1, 4, 5),
}
SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
EXPECTED_SUPPORT_DIGEST = "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
EXPECTED_ALL_SUPPORT_DIGEST = "22898fcc93f415be5488d22ecf2e74febb74cbd7997ef3c8d9dc2efc3545e324"
EXPECTED_Q6_SREPR_SHA256 = "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"

# These are the exact rational scalars that clear the GLD88 chart
# denominators for the five selected seven-minors.  They are applied to the
# actual reconstructed minors, not read from a generated polynomial panel.
CLEARING_SCALARS = {
    "T0": 4 * P**3 * H2**5,
    "T1": 16 * P**5 * H2**5,
    "T2": 16 * P**5 * H2**5,
    "Y1": 4 * P**5 * H2**5,
    "X3": 4 * P**5 * H2**5,
}
# The common denominator gate used by the raw determinant presentation.  It
# is recorded and checked, but is redundant on the declared D(B*H2*Delta)
# open because P divides Delta and H2 is already explicit there.
CLEARING_GATE = sp.expand(P**23 * H2**45)

# Descending coefficients of the degree-40 residual p factor.  Keeping the
# factor in this verifier makes the f40 route reproducible without any
# generated input.
F40_DESC = (
    7424, -161536, 1836800, -14454272, 88040000, -439964928,
    1867353392, -6884518384, 22398599716, -65072430404,
    170375836211, -405009960715, 879376810077, -1752467492937,
    3218063082751, -5462157661436, 8590438351195, -12541353394198,
    17018386499813, -21483026442413, 25236982384561, -27587608118151,
    28047919243155, -26495326489138, 23220609127349, -18842006278252,
    14118028970848, -9735354310506, 6152381134918, -3545007905402,
    1850774728870, -868862487040, 363420905896, -133926993072,
    42888299184, -11728177920, 2675395584, -492086016, 69030144,
    -6635520, 331776,
)

SOURCE_PINS = {
    "GLD70": {
        "path": GLD70,
        "sha256": "a53433329023223f1f24e960a8b23c7c57baf87b9767c4b2acabc819b982918e",
        "lf_sha256": "1a967f71bc4a08995a9187557eccd0ce39ab0f65544652f99c538049c49251f2",
    },
    "GLD71": {
        "path": GLD71,
        "sha256": "3342809b22cc1e5ffe960e14068f81303a3bc0b597e21e2d29c05c10c605dc7d",
        "lf_sha256": "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    },
    "GLD88": {
        "path": GLD88,
        "sha256": "70c46728c397d7a18fd999c27ca3d10232f9e3169ad508be7071c109be322752",
        "lf_sha256": "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    },
    "GLD102": {
        "path": GLD102,
        "sha256": "742aaccfb1e4b7cab194d8d20add3d5e7b5448a367180d01b398be306317eea",
        "lf_sha256": "c78130ad8ed5a639ffc7683ef21ae2b578312d6c7475820689a996dbc13bbd8e",
    },
}
OPTIONAL_SOURCE_PINS = {
    "GLD96_explore_q6": {
        "path": EXPLORE,
        "sha256": "00417d6dd6b27b1bc6cc51ccdf8d8536061abaa8fa9291befca06cb5bfd55cf1",
        "lf_sha256": "bd4e57c6cb4fb71a8a5c2b503980faacfd1f96994cc583d2d630780e3934ca25",
    },
}
FACTOR_MATRIX_INVERSE_ENV = "GLD103_FACTOR_MATRIX_INVERSE"
FACTOR_NO_FINAL_INVERSE_ENV = "GLD103_FACTOR_NO_FINAL_INVERSE"

# A comparison-only replay against the separately implemented tracked audit
# was run after the Q6-reduced D145 representation was corrected.  This is
# durable provenance for review, not a primary input and not an acceptance
# condition: the primary below recomputes D145 and all F40 identities itself.
# In particular, no historical term count is treated as an equality claim.
D145_CROSS_IMPLEMENTATION_COMPARISON = {
    "status": "verified_comparison_only_replay",
    "audit_verifier_path": (
        "claims/arbitrary-order/"
        "audit_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion.py"
    ),
    "audit_verifier_sha256": "7fa82c67b4322dcc75a59b17cb41d24851b417593962d15070a75130dc2fe79d",
    "comparison_run_id": "gld103-primary-audit-physical-compare-20260831-v4",
    "comparison_run_json_sha256": "c83a785fc98d3e3d5bc85ea5fea7ac448817fb49cfb7e98a28a7cb7108efe2f0",
    "comparison_run_log_sha256": "d647ef5a1964b6f8fd8f71d74f639990ec61bcc0e6c4a025eaf88eeeaf2b8a82",
    "scope": "current Q6-reduced D145 expression only",
    "primary_q6_srepr_sha256": EXPECTED_Q6_SREPR_SHA256,
    "audit_q6_srepr_sha256": EXPECTED_Q6_SREPR_SHA256,
    "expression_equal": True,
    "ratio": "1",
    "raw_term_maps_equal": True,
    "primary_term_count": 1565,
    "audit_term_count": 1565,
    "primary_terms_sha256": "8c27545c0499b89126745aa258b1dc576653ec2587625e30f9e0c8ae3068c084",
    "audit_terms_sha256": "8c27545c0499b89126745aa258b1dc576653ec2587625e30f9e0c8ae3068c084",
    "primary_rational_content": 23887872,
    "audit_rational_content": 23887872,
    "primary_denominator": "(2*p**2 - 2*p + 1)**3",
    "audit_denominator": (
        "8*p**6 - 24*p**5 + 36*p**4 - 32*p**3 + 18*p**2 - 6*p + 1"
    ),
    "used_for_primary_acceptance": False,
    "runtime_dependency": False,
}

# The corrected whole-P_i specialization was also compared with the tracked
# independent audit at both affine factors.  These pins are retained as
# comparison-only provenance.  Primary acceptance still comes only from the
# exact primary reconstruction and replay below; the audit is not imported at
# runtime.  Internal row hashes are included for review, while the canonical
# generator hashes after the displayed K-unit rescalings establish the actual
# coefficient comparison.
PHYSICAL_CROSS_IMPLEMENTATION_COMPARISON = {
    "status": "verified_comparison_only_replay",
    "audit_verifier_path": (
        "claims/arbitrary-order/"
        "audit_four_root_torus_star_equal_leaf_h4_q6_all_zero_coefficient_branch_exclusion.py"
    ),
    "audit_verifier_sha256": "7fa82c67b4322dcc75a59b17cb41d24851b417593962d15070a75130dc2fe79d",
    "comparison_run_id": "gld103-primary-audit-physical-compare-20260831-v4",
    "comparison_run_json_sha256": "c83a785fc98d3e3d5bc85ea5fea7ac448817fb49cfb7e98a28a7cb7108efe2f0",
    "comparison_run_log_sha256": "d647ef5a1964b6f8fd8f71d74f639990ec61bcc0e6c4a025eaf88eeeaf2b8a82",
    "comparison_helper_path": "claims/arbitrary-order/_gld103_all_zero_exact.py",
    "comparison_helper_sha256": "06ca97b8b38136659b8a57279b66959a28130f1eff75ff0dd5bc367ce990f2f23",
    "superseded_invalid_attempts": [
        {
            "run_id": "gld103-primary-audit-physical-compare-20260831-v1",
            "status": "aborted_invalid_helper",
            "original_run_record_status": "stale_running_record",
            "reason": (
                "the first helper mapped p-coefficients as q powers; its partial "
                "output is not comparison evidence"
            ),
            "evidence_accepted": False,
        }
    ],
    "scope": "six whole-P_i generators and exact z*B*Delta-1 localizer at F4 and p^2-2p+2",
    "q_basis": ["1", "q", "q^2", "q^3"],
    "q_shift_count": 4,
    "factors": {
        "F4": {
            "scalar_primary_over_audit_in_K": ["1/3", "1/3", "1/3", "1/3", "1/9", "1/9"],
            "scalar_nonzero_on_factor": [True, True, True, True, True, True],
            "canonical_generator_hashes_after_rescaling": [
                "91bb880a7c806a9530508b46f970201c993a5d2e55d94f5ccb0b865b220af50f",
                "3be9729fc30124e21413163461db4631dfb566ba26fa5f07a4d4c336f51bb935",
                "1d86ba5ab6d22429018ddd4e1da85d6da531ce40a703ec86a6eefc70fdd3d5e9",
                "61bf787484bd67d7c7df6cf31335c531a51f264c61e12efe92bc09f659efd1d0",
                "67e95f6e77b879db49ae016f8c0d308e08e6594375a30d9250c51207704397cc",
                "979ac31e56859489840f194dbaea3e27eb4c5ae48af3b16f48d90c8c2587d080",
            ],
            "primary_generator_hashes": [
                "3821d7f4e75f9786c7c3eb2fc28b72b582a522d4dd0b8fe28820f9a0619b8fd9",
                "bcf4118f34bb0704703b054dbcec4ce835dcd03c42b69ceb1a197dcda0f2561d",
                "e0da33b9554293fe6e19bdc4b1b8f0df7f01c5c5a59cb428b1fe17d5001dd30a",
                "38749993723394bce14ce0fa23b67645842f6670fe851abebc010021d8a2128a",
                "2b0270a242bf1c704c4af0be6308d853a4ba969d10327d7e8b7f9dcb51393b29",
                "376300723f963ef39ed8bda2a345a8ffde133011779cfeed4084cec404b367dd",
            ],
            "audit_generator_hashes": [
                "03ffc744233ae5f3733fdcdade4336128a2ddf2b54d3bf91c0ddcddea83c2c7f",
                "76fcab5b758216061402ba7d3ed484782a27f0a12843306d94732a171457383b",
                "d7b89ad2f8ca91dbf9cb30bc4c9dae05f4f2150b260f1b1d1e007c07fff014ea",
                "7543a61b7e3d611c2a992e925e30c9b14bad3ad2ea4e3f0adafe52930f770459",
                "c684c7bf703060024be08ff5dffd1fd779ef87c23b9ec298a24057c79af4c15a",
                "df31cc63ff6c57885cf2e2f2c382602895b7efd659e61b7d885d9de56df8a85f",
            ],
            "canonical_generator_equality_after_rescaling": True,
            "localizer": {
                "exact_equal": True,
                "scalar_primary_over_audit_in_K": "1",
                "canonical_hash": "35bf7cb2dfa9dcdd168f35e370dd9c09c7b9be0ad36b8adde146297d64bb90b68",
            },
            "row_space": {
                "primary": {
                    "rank": 68, "rank_with_target": 68, "target_in_span": True,
                    "row_count": 88, "columns": 80,
                    "input_matrix_sha256": "639cde33ae4867787bdc40aa9e7a0f457a3b842252b576c738a39032d9acd41b",
                    "rref_matrix_sha256": "f3ed48348abb2ec530e6926d15051cb632ba62b8da118e2744f6992356748f78",
                    "target_residual_sha256": "a8eddbe4f43b8592ca210a10320c3f5f74549f80f5930096d559bde63fc5c2d7",
                },
                "audit": {
                    "rank": 68, "rank_with_target": 68, "target_in_span": True,
                    "row_count": 88, "columns": 80,
                    "row_matrix_sha256": "971db2dbc64e60e3e1a6937dd24496d5100935bc19c565299ba5447641719676e",
                },
                "same_rank_and_membership": True,
                "equal_by_nonzero_generator_units": True,
            },
        },
        "p2_minus_2p_plus_2": {
            "scalar_primary_over_audit_in_K": ["1/3", "1/3", "1/3", "1/3", "1/9", "1/9"],
            "scalar_nonzero_on_factor": [True, True, True, True, True, True],
            "canonical_generator_hashes_after_rescaling": [
                "c8936f3651ed5ce795df21419823376ac0717803c82cb3be9abfbf89da8f9702",
                "ce9ae98f752eeaaba33ce08d48cce02d27dcaf71f75ff5dc2ec9b7b0c3c13aee",
                "0cc9323aeb930db5cc9207e166b97649dbe55d55e2101dc548fa0ebccb479ae1",
                "1a2186d5865cd01844b2135e3e70d9e08cbd879a5237b7b1441fed5b4c77adb5",
                "a1dfced9f549aa414ea6f430128afe85f38a2a00e624c6342111e27104a7a88e",
                "89c0857abb2913e6aecdd627071ac6cd31287e9833b660928ac7f93e05316fad",
            ],
            "primary_generator_hashes": [
                "234838069b225e7c516cf5570e4f98735078197df1848ac8457139e36ff7992d",
                "6e511cf67b235983f11d5af449a22e83148817160338d1ad4ceff7914be7a8cb",
                "6a579bd095893c190112bc97e9bd442d99796d49b97c37bdef43e8379ae95d1a",
                "dcadb087fc3d72b43c93fd2d17265ae2bce30bc3163bc2f6f1b2329cf89308bb",
                "eb4e765c62ce6ead9588ede416b8787aa8d49360b3c9ebfdf9b53bd287bf4abc",
                "3f503dd495a6900642485a218987048f5640b965de6b18e2deec4902129e0005",
            ],
            "audit_generator_hashes": [
                "1ae98ea89cc268bd7850f2d79dbc089360fe15bbb9e55d6df7ca71450983de98",
                "8289f5af7d515d2a48aaad6ca6dd2b019a44f14212daf1d67ea07ab1cf50820a",
                "592bbc041457ee625a26a854772dd831c1c3f4c19f5a8b9d509025fa844a8650",
                "f334ee8187bb1e0ac6d445a3a2e5fe092f0ff4432be52372597378660ef410a1",
                "4650c8d51594fb38c466984675a43ee1bbdd4fc5996359ea6e37f2dd48015e41",
                "9d1ffab1ac750a49f8ec52b41a92853333eebf6806f7796214404b6d84d70a58",
            ],
            "canonical_generator_equality_after_rescaling": True,
            "localizer": {
                "exact_equal": True,
                "scalar_primary_over_audit_in_K": "1",
                "canonical_hash": "7b576e525fbfc6edbc3164a191afaecd91c91eeb5aabcedb31b17c5a837cd5a8",
            },
            "row_space": {
                "primary": {
                    "rank": 66, "rank_with_target": 66, "target_in_span": True,
                    "row_count": 88, "columns": 80,
                    "input_matrix_sha256": "3008cbc453780c56a70b422620807e6809b17ec845a57e4aae4f29ea1f2b473b",
                    "rref_matrix_sha256": "cd44467e2baccc1a91e76193ab465fbf9324d5da550b948a8ab8d7f274ecce0a",
                    "target_residual_sha256": "a8eddbe4f43b8592ca210a10320c3f5f74549f80f5930096d559bde63fc5c2d7",
                },
                "audit": {
                    "rank": 66, "rank_with_target": 66, "target_in_span": True,
                    "row_count": 88, "columns": 80,
                    "row_matrix_sha256": "42d54b81ed26df0fa0d447d3dec9a216be22b091ee58af43c477248f5360359a",
                },
                "same_rank_and_membership": True,
                "equal_by_nonzero_generator_units": True,
            },
        },
    },
    "all_generators_unit_related": True,
    "all_localizers_exact": True,
    "used_for_primary_acceptance": False,
    "runtime_dependency": False,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def source_manifest() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for name, pin in SOURCE_PINS.items():
        path = pin["path"]
        if not path.is_file():
            raise AssertionError(f"missing pinned source: {path}")
        raw = sha256_file(path)
        normalized = lf_sha256(path)
        if raw != pin["sha256"] and normalized != pin["lf_sha256"]:
            raise AssertionError(f"{name} source hash mismatch")
        if normalized != pin["lf_sha256"]:
            raise AssertionError(f"{name} LF-normalized hash mismatch")
        result[name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": raw,
            "lf_sha256": normalized,
        }
    return result


def optional_source_manifest() -> dict[str, dict[str, str]]:
    """Record the exploratory Q6 script without making it an input dependency."""
    result: dict[str, dict[str, str]] = {}
    for name, pin in OPTIONAL_SOURCE_PINS.items():
        path = pin["path"]
        if not path.is_file():
            result[name] = {"available": False, "used_for_exact_replay": False}
            continue
        raw = sha256_file(path)
        normalized = lf_sha256(path)
        if raw != pin["sha256"] and normalized != pin["lf_sha256"]:
            raise AssertionError(f"{name} optional source hash mismatch")
        if normalized != pin["lf_sha256"]:
            raise AssertionError(f"{name} optional LF-normalized hash mismatch")
        result[name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": raw,
            "lf_sha256": normalized,
            "available": True,
            "used_for_exact_replay": False,
        }
    return result


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load tracked source {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def optional_q6_crosscheck(q6: sp.Expr) -> dict[str, Any]:
    """Compare the literal Q6 with GLD96 only as a non-authoritative check."""
    if not EXPLORE.is_file():
        return {"available": False, "used_for_exact_replay": False}
    explore = load_module(EXPLORE, "gld96_explore_for_gld103_primary_optional")
    if sp.expand(q6 - explore.q6_polynomial(p, q)) != 0:
        raise AssertionError("optional GLD96 Q6 crosscheck mismatch")
    return {
        "available": True,
        "used_for_exact_replay": False,
        "match_checked": True,
        "source": EXPLORE.relative_to(ROOT).as_posix(),
        "source_sha256": sha256_file(EXPLORE),
    }


def _implementation_flag(primary_name: str) -> tuple[bool, str]:
    """Read a neutral arithmetic-only implementation switch."""
    if primary_name in os.environ:
        raw = os.environ[primary_name]
        source = primary_name
    else:
        raw = "1"
        source = "default"
    if raw not in {"0", "1"}:
        raise ValueError(f"{primary_name} must be 0 or 1")
    return raw == "1", source


def q6_expression(p_value=p, q_value=q):
    return sp.expand(
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


def clearing_gate_check() -> dict[str, Any]:
    scalar_product = sp.factor(sp.prod(CLEARING_SCALARS.values()))
    # The five tracked 7-minor clearing scalars contribute the literal
    # constant 4*16*16*4*4 = 2**14.  Keep this equality live: a smaller
    # constant would silently accept a normalization drift in the chart.
    expected_scalar_product = sp.factor(16384 * P**23 * H2**25)
    if sp.expand(scalar_product - expected_scalar_product) != 0:
        raise AssertionError("selected minor clearing scalar product drift")
    declared = sp.factor(P**23 * H2**45)
    if sp.expand(CLEARING_GATE - declared) != 0:
        raise AssertionError("ClearingGate expression drift")
    if not sp.cancel(DELTA / P).is_polynomial(p, q):
        raise AssertionError("P is not a factor of Delta")
    return {
        "declared_expression": str(CLEARING_GATE),
        "declared_equality_checked": True,
        "selected_scalar_product": str(scalar_product),
        "selected_scalar_product_equality_checked": True,
        "gate_is_redundant_on_declared_open": True,
        "gate_not_added_to_scope": True,
        "P_divides_Delta_checked": True,
    }


class Algebra:
    """Exact arithmetic in QQ(p,a)[q]/(Q6), low q coefficient first."""

    def __init__(self, q6: sp.Expr) -> None:
        self.q6_expr = sp.expand(q6)
        self.q6 = sp.Poly(self.q6_expr, q, domain=K)
        if self.q6.degree() != 4:
            raise AssertionError("Q6 q-degree drift")
        if sp.expand(self.q6.LC() - H2) != 0:
            raise AssertionError("Q6 leading H2 coefficient drift")
        self.zero = (K.zero, K.zero, K.zero, K.zero)
        self.one = (K.one, K.zero, K.zero, K.zero)
        lead = K.convert(self.q6.LC())
        self.relation = tuple(-K.convert(self.q6.nth(i)) / lead for i in range(4))
        self.inverses: dict[tuple[Any, ...], tuple[Any, ...]] = {}
        self._denominator_cache: dict[str, dict[str, Any]] = {}
        self._denominator_observations: dict[str, dict[str, Any]] = {}
        self._denominator_calls = 0

    def from_expr(self, expression: object):
        numerator, denominator = sp.cancel(sp.sympify(expression)).as_numer_denom()
        denominator = sp.factor(denominator)
        key = sp.srepr(denominator)
        provenance = self._denominator_cache.get(key)
        if provenance is None:
            provenance = _chart_denominator_provenance(denominator)
            self._denominator_cache[key] = provenance
        self._denominator_calls += 1
        observation = self._denominator_observations.setdefault(
            key,
            {
                **provenance,
                "canonical_sha256": sha256_bytes(key.encode()),
                "count": 0,
            },
        )
        observation["count"] += 1
        n = sp.Poly(numerator, q, domain=K).rem(self.q6)
        d = sp.Poly(denominator, q, domain=K).rem(self.q6)
        if d.is_zero:
            raise AssertionError(("zero denominator modulo Q6", expression))
        key = tuple(K.convert(d.nth(i)) for i in range(4))
        inverse = self.inverses.get(key)
        if inverse is None:
            inverse_poly = sp.invert(d, self.q6)
            inverse = tuple(K.convert(inverse_poly.nth(i)) for i in range(4))
            self.inverses[key] = inverse
        raw = tuple(K.convert(n.nth(i)) for i in range(4))
        return self.mul(raw, inverse)

    def add(self, left, right):
        return tuple(left[i] + right[i] for i in range(4))

    def neg(self, value):
        return tuple(-value[i] for i in range(4))

    def sub(self, left, right):
        return self.add(left, self.neg(right))

    def mul(self, left, right):
        raw = [K.zero] * 7
        for i, x in enumerate(left):
            if x == K.zero:
                continue
            for j, y in enumerate(right):
                if y != K.zero:
                    raw[i + j] += x * y
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high == K.zero:
                continue
            for i, coefficient in enumerate(self.relation):
                raw[degree - 4 + i] += high * coefficient
        return tuple(raw[:4])

    def is_zero(self, value) -> bool:
        return all(item == K.zero for item in value)

    def as_expr(self, value) -> sp.Expr:
        return sp.expand(sum(sp.sympify(value[i].as_expr()) * q**i for i in range(4)))

    def denominator_provenance(self) -> dict[str, Any]:
        return {
            "all_supported": True,
            "calls_checked": self._denominator_calls,
            "unique_denominators": len(self._denominator_observations),
            "observations": sorted(
                self._denominator_observations.values(),
                key=lambda item: item["canonical_sha256"],
            ),
            "delta_expression": str(DELTA),
            "P_divides_Delta": sp.cancel(DELTA / P).is_polynomial(p, q),
            "H2_is_q6_leading_coefficient": True,
        }


class BC:
    """Sparse exact polynomial in B,C with Algebra coefficients."""

    def __init__(self, algebra: Algebra, terms: dict[tuple[int, int], Any] | None = None):
        self.A = algebra
        self.terms: dict[tuple[int, int], Any] = {}
        for exponent, value in (terms or {}).items():
            value = tuple(value)
            if not algebra.is_zero(value):
                self.terms[tuple(exponent)] = value

    @classmethod
    def const(cls, algebra: Algebra, value: object):
        return cls(algebra, {(0, 0): value if isinstance(value, tuple) else algebra.from_expr(value)})

    @classmethod
    def variable(cls, algebra: Algebra, exponent: tuple[int, int]):
        return cls(algebra, {tuple(exponent): algebra.one})

    def __add__(self, other):
        out = dict(self.terms)
        for exponent, value in other.terms.items():
            updated = self.A.add(out.get(exponent, self.A.zero), value)
            if self.A.is_zero(updated):
                out.pop(exponent, None)
            else:
                out[exponent] = updated
        return BC(self.A, out)

    def __neg__(self):
        return BC(self.A, {exponent: self.A.neg(value) for exponent, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        out: dict[tuple[int, int], Any] = {}
        for (lb, lc), left in self.terms.items():
            for (rb, rc), right in other.terms.items():
                exponent = (lb + rb, lc + rc)
                updated = self.A.add(out.get(exponent, self.A.zero), self.A.mul(left, right))
                if self.A.is_zero(updated):
                    out.pop(exponent, None)
                else:
                    out[exponent] = updated
        return BC(self.A, out)


def shift_b(value: BC, amount: int = 1) -> BC:
    return BC(value.A, {(b + amount, c): coefficient for (b, c), coefficient in value.terms.items()})


def divide_by_b(value: BC, label: str) -> BC:
    terms = {}
    for (b, c), coefficient in value.terms.items():
        if b == 0:
            raise AssertionError(f"{label} is not divisible by B")
        terms[(b - 1, c)] = coefficient
    quotient = BC(value.A, terms)
    if shift_b(quotient).terms != value.terms:
        raise AssertionError(f"{label} B-division failed")
    return quotient


def det_bc(matrix: list[list[BC]], label: str) -> BC:
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise AssertionError(f"{label} is not square")
    algebra = matrix[0][0].A
    states: dict[int, BC] = {0: BC.const(algebra, 1)}
    size = len(matrix)
    for row_index, row in enumerate(matrix):
        next_states: dict[int, BC] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                inversions = sum(1 for previous in range(column + 1, size) if mask & (1 << previous))
                term = value * entry
                if inversions & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = term if new_mask not in next_states else next_states[new_mask] + term
        states = next_states
        print(f"[GLD103 primary] {label} row={row_index + 1}/{size} states={len(states)}", file=sys.stderr, flush=True)
    return states.get((1 << size) - 1, BC.const(algebra, 0))


def det3_expansion(algebra: Algebra, rows: list[list[Any]]):
    a0, b0, c0 = rows[0]
    a1, b1, c1 = rows[1]
    a2, b2, c2 = rows[2]
    first = algebra.mul(a0, algebra.sub(algebra.mul(b1, c2), algebra.mul(c1, b2)))
    second = algebra.mul(b0, algebra.sub(algebra.mul(a1, c2), algebra.mul(c1, a2)))
    third = algebra.mul(c0, algebra.sub(algebra.mul(a1, b2), algebra.mul(b1, a2)))
    return algebra.add(algebra.sub(first, second), third)


def det3_permutation(algebra: Algebra, rows: list[list[Any]]):
    result = algebra.zero
    for permutation in itertools.permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        term = algebra.one
        for row, column in enumerate(permutation):
            term = algebra.mul(term, rows[row][column])
        result = algebra.add(result, algebra.neg(term) if inversions & 1 else term)
    return result


def expression_to_bc(algebra: Algebra, expression: object, label: str) -> BC:
    try:
        polynomial = sp.Poly(sp.expand(expression), B, C)
    except sp.PolynomialError as exc:
        raise AssertionError(f"{label} is not polynomial in B,C") from exc
    return BC(
        algebra,
        {
            (int(b_degree), int(c_degree)): algebra.from_expr(coefficient)
            for (b_degree, c_degree), coefficient in polynomial.terms()
        },
    )


def support_digests(gld71: Any) -> dict[str, str]:
    def digest(rows):
        payload = [
            [row, [[list(indices), coefficient] for indices, coefficient in gld71.SPARSE_RELATIONS[row]]]
            for row in rows
        ]
        return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())

    all_digest = digest(range(len(gld71.SPARSE_RELATIONS)))
    selected_digest = digest(SUPPORT_ROWS)
    if all_digest != EXPECTED_ALL_SUPPORT_DIGEST or selected_digest != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError(f"support digest drift: all={all_digest}, selected={selected_digest}")
    return {"all_rows": all_digest, "selected_rows": selected_digest}


def load_authoritative(gld71: Any) -> dict[str, int]:
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    if len(relations) != 37 or any(len(row) != 81 for row in relations):
        raise AssertionError("full relation shape drift")
    relation_rank = int(sp.Matrix(relations).rank())
    if relation_rank != 37:
        raise AssertionError("full relation rank drift")
    columns, basis, punctured = gld71.check_punctured_code(parent, relations)
    if (len(columns), len(basis), len(punctured)) != (79, 44, 60):
        raise AssertionError("GLD70/71 dimension drift")
    return {
        "relation_count": len(relations),
        "relation_width": len(relations[0]),
        "relation_matrix_rank": relation_rank,
        "all_column_count": len(columns),
        "annihilator_basis_count": len(basis),
        "punctured_row_count": len(punctured),
    }


def reconstruct_rows(gld71: Any, gld88: Any, algebra: Algebra):
    support = gld71.SPARSE_RELATIONS
    digests = support_digests(gld71)
    chart = gld88.h4_family(p, q, a)
    leaves = [
        [BC.const(algebra, 1), BC.const(algebra, 1), BC.const(algebra, 1)],
        [BC.const(algebra, p), BC.const(algebra, q), BC.const(algebra, chart["s"])],
        [
            BC.const(algebra, a),
            BC.const(algebra, 1 + chart["b"]) + BC.variable(algebra, (1, 0)),
            BC.const(algebra, 1 + chart["c"]) + BC.variable(algebra, (0, 1)),
        ],
    ]
    rows: dict[int, list[BC]] = {}
    for row_index, row_support in enumerate(support):
        entries = []
        for root in range(3):
            for component in range(3):
                total = BC.const(algebra, 0)
                for indices, coefficient in row_support:
                    if indices[0] != root:
                        continue
                    term = leaves[indices[1]][component] * leaves[indices[2]][component] * leaves[indices[3]][component]
                    total = total + BC.const(algebra, coefficient) * term
                entries.append(total)
        rows[row_index] = entries
    if len(rows) != 37 or any(len(row) != 9 for row in rows.values()):
        raise AssertionError("M(G) shape drift")

    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    native_leaf = sp.Matrix(
        [[1, 1, 1], [p, q, chart["s"]], [a, 1 + chart["b"] + B, 1 + chart["c"] + C]]
    )
    native_matrix = gld71.coefficient_matrix(parent, relations, (native_leaf, native_leaf, native_leaf))
    if native_matrix.shape != (37, 9):
        raise AssertionError("native coefficient_matrix shape drift")
    for i in range(37):
        for j in range(9):
            expected = expression_to_bc(algebra, native_matrix[i, j], f"M[{i},{j}]")
            if expected.terms != rows[i][j].terms:
                raise AssertionError(f"native coefficient_matrix mismatch at [{i},{j}]")
    return rows, chart, {
        "support_digest": digests,
        "matrix_shape": [37, 9],
        "native_coefficient_matrix_crosscheck": True,
        "chart": "GLD88 h4_family(p,q,a) with symbolic a",
        "chart_denominators": {
            "s": str(chart["h4_denominator"]),
            "b": str(chart["b"].as_numer_denom()[1]),
            "c": str(chart["c"].as_numer_denom()[1]),
            "rank": str(chart["rank_denominator"]),
        },
    }


def canonical_algebra(value: Any) -> list[Any]:
    """Encode a quotient element without relying on Python/SymPy reprs."""
    encoded = []
    for q_degree, coefficient in enumerate(value):
        if coefficient == K.zero:
            continue
        numerator, denominator = sp.cancel(coefficient.as_expr()).as_numer_denom()
        n = sp.Poly(numerator, p, a, domain=QQ)
        d = sp.Poly(denominator, p, a, domain=QQ)
        if d.LC() < 0:
            n = n.mul_ground(-1)
            d = d.mul_ground(-1)

        def poly_terms(poly):
            return [
                [int(m[0]), int(m[1]), int(coeff.p), int(coeff.q)]
                for m, coeff in poly.terms()
            ]

        encoded.append(
            {
                "q_degree": q_degree,
                "numerator": poly_terms(n),
                "denominator": poly_terms(d),
            }
        )
    return encoded


def canonical_bc(value: BC) -> list[Any]:
    return [
        {
            "B_degree": b,
            "C_degree": c,
            "coefficient": canonical_algebra(coefficient),
        }
        for (b, c), coefficient in sorted(value.terms.items())
    ]


def digest_payload(payload: object) -> str:
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())


def bc_record(value: BC) -> dict[str, Any]:
    canonical = canonical_bc(value)
    return {
        "term_count": len(value.terms),
        "B_degree": max((item["B_degree"] for item in canonical), default=-1),
        "C_degree": max((item["C_degree"] for item in canonical), default=-1),
        "canonical_sha256": digest_payload(canonical),
    }


def partition_affine(value: BC, label: str) -> tuple[BC, BC]:
    f_terms, g_terms = {}, {}
    for (b, c), coefficient in value.terms.items():
        if c == 0:
            f_terms[(b, 0)] = coefficient
        elif c == 1:
            g_terms[(b, 0)] = coefficient
        else:
            raise AssertionError(f"{label} has C-degree >1")
    f, g = BC(value.A, f_terms), BC(value.A, g_terms)
    if any(b == 0 for b, _ in f.terms):
        raise AssertionError(f"{label} F(B=0) is nonzero")
    if (f + BC.variable(value.A, (0, 1)) * g).terms != value.terms:
        raise AssertionError(f"{label} affine-C recomposition failed")
    return f, g


def coefficient_rows(algebra: Algebra, values: list[BC]) -> list[list[Any]]:
    result = []
    for index, value in enumerate(values):
        if any(c for _, c in value.terms):
            raise AssertionError(f"P{index} is not C-free")
        if any(b > 2 for b, _ in value.terms):
            raise AssertionError(f"P{index} has B-degree >2")
        row = [value.terms.get((degree, 0), algebra.zero) for degree in range(3)]
        rebuilt = BC(
            algebra,
            {
                (degree, 0): coefficient
                for degree, coefficient in enumerate(row)
                if not algebra.is_zero(coefficient)
            },
        )
        if rebuilt.terms != value.terms:
            raise AssertionError(f"P{index} coefficient extraction failed")
        result.append(row)
    return result


def evaluate_algebra(algebra: Algebra, value: Any, substitutions: dict[sp.Symbol, object]):
    return sp.expand(algebra.as_expr(value).subs(substitutions))


def evaluate_bc(value: BC, substitutions: dict[sp.Symbol, object]):
    return sp.expand(
        sum(
            evaluate_algebra(value.A, coefficient, substitutions)
            * substitutions[B] ** b
            * substitutions[C] ** c
            for (b, c), coefficient in value.terms.items()
        )
    )


def numeric_crosscheck(rows: dict[int, list[BC]], scaled_raw: dict[str, BC]):
    """Check each scaled actual determinant against a direct numeric det."""
    substitutions = {
        p: sp.Integer(1),
        a: sp.Integer(2),
        q: sp.I,
        B: sp.Integer(2),
        C: sp.Integer(3),
    }
    if sp.simplify(q6_expression(substitutions[p], substitutions[q])) != 0:
        raise AssertionError("generic numeric point is not on Q6")
    gates = {
        "H2": H2,
        "h4_denominator": p + q - 1,
        "b_denominator_factor": P,
        "rank_denominator": RANK_DENOMINATOR,
        "Delta": DELTA,
    }
    values = {name: sp.simplify(expr.subs(substitutions)) for name, expr in gates.items()}
    if any(value == 0 for value in values.values()):
        raise AssertionError(f"generic numeric point hits chart gate: {values}")
    determinants = {}
    for name in MINOR_ORDER:
        row_set, columns = MINOR_DATA[name]
        numeric_matrix = [
            [evaluate_bc(rows[row][column], substitutions) for column in columns]
            for row in row_set
        ]
        direct = sp.expand(sp.Matrix(numeric_matrix).det(method="domain-ge"))
        expected = sp.expand(CLEARING_SCALARS[name].subs(substitutions) * direct)
        actual = evaluate_bc(scaled_raw[name], substitutions)
        if sp.simplify(actual - expected) != 0:
            raise AssertionError(f"{name} generic determinant mismatch at numeric point")
        if sp.simplify(actual) == 0:
            raise AssertionError(f"{name} unexpectedly zero at generic numeric point")
        determinants[name] = str(actual)
    return {
        "point": {"p": "1", "a": "2", "q": "I", "B": "2", "C": "3"},
        "Q6_zero": True,
        "nonzero_chart_gates": {name: str(value) for name, value in values.items()},
        "all_match": True,
        "determinants": determinants,
    }


def build_bridge(manifest: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Rebuild the GLD103 bridge from tracked source, returning certificate data."""
    gld71 = load_module(GLD71, "gld71_for_gld103_primary")
    gld88 = load_module(GLD88, "gld88_for_gld103_primary")
    relation_data = load_authoritative(gld71)
    q6 = sp.expand(q6_expression(p, q))
    q6_hash = sha256_bytes(sp.srepr(q6).encode())
    if q6_hash != EXPECTED_Q6_SREPR_SHA256:
        raise AssertionError(f"Q6 hash drift: {q6_hash}")
    algebra = Algebra(q6)
    rows, chart, reconstruction = reconstruct_rows(gld71, gld88, algebra)

    native_raw: dict[str, BC] = {}
    native_f: dict[str, BC] = {}
    native_g: dict[str, BC] = {}
    scaled_raw: dict[str, BC] = {}
    scaled_f: dict[str, BC] = {}
    scaled_g: dict[str, BC] = {}
    comparison: dict[str, Any] = {}
    for name in MINOR_ORDER:
        row_set, columns = MINOR_DATA[name]
        native_raw[name] = det_bc(
            [[rows[row][column] for column in columns] for row in row_set], name
        )
        native_f[name], native_g[name] = partition_affine(native_raw[name], name)
        scalar = BC.const(algebra, CLEARING_SCALARS[name])
        scaled_raw[name] = scalar * native_raw[name]
        scaled_f[name] = scalar * native_f[name]
        scaled_g[name] = scalar * native_g[name]
        shifted_g = BC(
            algebra,
            {(b, c + 1): coefficient for (b, c), coefficient in scaled_g[name].terms.items()},
        )
        if scaled_raw[name].terms != (scaled_f[name] + shifted_g).terms:
            raise AssertionError(f"{name} scaled affine decomposition failed")
        comparison[name] = {
            "clearing_scalar": str(CLEARING_SCALARS[name]),
            "native_A_scaled": bc_record(scaled_raw[name]),
            "native_F_scaled": bc_record(scaled_f[name]),
            "native_G_scaled": bc_record(scaled_g[name]),
            "raw_term_count": len(native_raw[name].terms),
            "entrywise_reconstructed": True,
        }

    p_values = [divide_by_b(scaled_f["T0"], "F_T0")]
    p_values.extend(scaled_g[name] for name in MINOR_ORDER)
    if shift_b(p_values[0]).terms != scaled_f["T0"].terms:
        raise AssertionError("F_T0=B*P0 failed")
    coeff_rows = coefficient_rows(algebra, p_values)

    determinant_records = {}
    determinants: dict[str, Any] = {}
    all_triples = {**SELECTED_TRIPLES, **FIBRE_TRIPLES}
    for label, triple in all_triples.items():
        selected = [coeff_rows[index] for index in triple]
        first = det3_expansion(algebra, selected)
        second = det3_permutation(algebra, selected)
        if first != second or algebra.is_zero(first):
            raise AssertionError(f"selected determinant {label} failed exact cross-check")
        determinant = BC(algebra, {(0, 0): first})
        determinants[label] = first
        determinant_records[label] = {
            **bc_record(determinant),
            "row_triple": list(all_triples[label]),
            "two_route_exact_match": True,
        }

    numeric = numeric_crosscheck(rows, scaled_raw)
    p_records = {f"P{i}": bc_record(value) for i, value in enumerate(p_values)}
    result = {
        # This is bridge metadata, not the CLI replay mode.  Keeping it under
        # a distinct key prevents result.update(bridge) from erasing a
        # targeted/full mode selected by main().
        "bridge_reconstruction_mode": "exact",
        "clearing_gate": clearing_gate_check(),
        "native_reconstruction": {
            **relation_data,
            **reconstruction,
            "source_basis": "tracked GLD70 -> GLD71 sparse annihilator -> GLD88 symbolic-a chart",
            "external_input_dependency": False,
        },
        "q6": {
            "expression": str(q6),
            "q_degree": int(algebra.q6.degree()),
            "leading_coefficient": str(algebra.q6.LC()),
            "srepr_sha256": q6_hash,
            "exploratory_crosscheck": optional_q6_crosscheck(q6),
        },
        "chart_denominator_provenance": algebra.denominator_provenance(),
        "selected_minors": {
            name: {"rows": list(MINOR_DATA[name][0]), "columns": list(MINOR_DATA[name][1])}
            for name in MINOR_ORDER
        },
        "minor_reconstruction": comparison,
        "selected_minor_numeric_crosscheck": numeric,
        "affine_C_checks": {
            name: {
                "identity": "A_i=F_i+C*G_i",
                "identity_checked": True,
                "F_at_B0": True,
            }
            for name in MINOR_ORDER
        },
        "P_checks": {
            "definitions": [
                "P0=F_T0/B",
                "P1=G_T0",
                "P2=G_T1",
                "P3=G_T2",
                "P4=G_Y1",
                "P5=G_X3",
            ],
            "F_T0_equals_B_times_P0": True,
            "quadratic_B_coefficient_rows": 6,
            "coefficient_vector": ["1", "B", "B^2"],
            "records": p_records,
        },
        "selected_coefficient_determinants": {
            "row_triples": {label: list(triple) for label, triple in SELECTED_TRIPLES.items()},
            "count": len(SELECTED_TRIPLES),
            "all_two_route_exact_matches": True,
            "records": determinant_records,
            "fibre_row_triples": {label: list(triple) for label, triple in FIBRE_TRIPLES.items()},
            "fibre_records": {
                label: determinant_records[label] for label in FIBRE_TRIPLES
            },
        },
        "implication": {
            "direction": "one-way",
            "converse_used": False,
            "premises": [
                "Q6=0",
                "symbolic-a GLD88 chart point",
                "rank(M(G))<=6",
                "G_T0=G_T1=G_T2=G_Y1=G_X3=0",
                "B!=0",
            ],
            "steps": [
                "rank(M(G))<=6 implies every selected actual 7x7 minor A_i vanishes",
                "all G_i=0 makes A_T0=F_T0",
                "F_T0=B*P0 and B!=0 imply P0=0",
                "P0=P1=...=P5=0 gives K*(1,B,B^2)^T=0",
                "the first coordinate is 1, so the kernel vector is nonzero",
                "each selected 3x3 coefficient determinant vanishes",
            ],
            "rank_to_minor_is_not_reversed": True,
        },
    }
    result["_determinants"] = determinants
    result["_algebra"] = algebra
    result["_p_values"] = p_values
    return result


def expected_factor_plan() -> dict[str, Any]:
    """Describe the eleven exact p-cover factors and their fibre routes."""
    return {
        "cover_degree_p": 624,
        "raw_source_cover_degree_p": 624,
        "normalized_open_cover_degree_p": 620,
        "degree_note": (
            "The tracked native resultant/gcd cover has degree 624; exact division by H2^2, "
            "already invertible/outside D(B*H2*Delta), reports a degree-620 open-chart "
            "representative but is not used as the authoritative cover degree."
        ),
        "factor_count": 11,
        "factors": {
            "R8": "64p^8-256p^7+580p^6-844p^5+946p^4-784p^3+388p^2-94p+13",
            "p2_plus_1": "p^2+1",
            "R4": "5p^4-16p^3+30p^2-16p+5",
            "F4": "5p^4-4p^3+12p^2-16p+8",
            "C4": "8p^4-16p^3+12p^2-4p+5",
            "F40": "degree-40 primitive factor pinned by descending coefficient tuple in verifier",
            "p2_minus_2p_plus_2": "p^2-2p+2",
            "p_minus_1": "p-1",
            "H2": "2p^2-2p+1",
            "p": "p",
            "P": "p^2-p+1",
        },
        "selected_cover_determinants": {
            label: list(triple) for label, triple in SELECTED_TRIPLES.items()
        },
        "fibre_only_determinants": {
            label: list(triple) for label, triple in FIBRE_TRIPLES.items()
        },
    }


def static_certificate(
    mode: str,
    manifest: dict[str, dict[str, str]],
    optional_manifest: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the manifest-only certificate without loading any source module."""
    return {
        "schema_version": 1,
        "status": (
            "exact_scoped_theorem_certificate"
            if mode == "full"
            else "incomplete_replay_manifest"
        ),
        "manifest_status": "exact scoped theorem certificate",
        "mathematical_status": "scoped_necessary_condition_only",
        "global_conjecture": "UNRESOLVED",
        "claim_id": "GLD103",
        "branch": "all-zero selected coefficient branch, generic symbolic a",
        "scope": {
            "characteristic": 0,
            "chart": "normalized GLD88/F88 H4 Q6 chart",
            "rank_condition": "rank(M(G))<=6",
            "open": "D(B*H2*Delta)",
            "coefficient_equations": [
                "G_T0=0", "G_T1=0", "G_T2=0", "G_Y1=0", "G_X3=0"
            ],
            "parameter_a": "symbolic/arbitrary",
        },
        "evidence_boundary": {
            "rank_to_minor_direction": "one-way necessary implication only",
            "arithmetic_independence": "not claimed",
            "E31_equation_imposed": False,
            "E31_inverted": False,
            "physical_incidence_emptiness": False,
            "global_resolution": False,
            "implementation_switch_boundary": (
                "factor-field matrix inversion and no-final-inverse flags are arithmetic "
                "implementation controls only; they do not impose or invert any separate equation or locus"
            ),
        },
        "comparison_provenance": {
            "D145_current_representation": D145_CROSS_IMPLEMENTATION_COMPARISON,
            "physical_generators": PHYSICAL_CROSS_IMPLEMENTATION_COMPARISON,
            "used_for_primary_acceptance": False,
            "runtime_dependency": False,
        },
        "runtime_mode": mode,
        "replay_complete": False,
        "source_manifest": manifest,
        "optional_source_manifest": optional_manifest or {},
        "source_basis": "tracked GLD70, GLD71, GLD88, literal Q6, and GLD102",
        "q6": {
            "expression": str(q6_expression(p, q)),
            "srepr_sha256": EXPECTED_Q6_SREPR_SHA256,
            "q_degree": 4,
        },
        "selected_minors": {
            name: {"rows": list(rows), "columns": list(columns)}
            for name, (rows, columns) in MINOR_DATA.items()
        },
        "exact_arithmetic_plan": expected_factor_plan(),
        "clearing_gate": clearing_gate_check(),
        "local_fibre_plan": {
            "p0_p1": "call tracked GLD102 check()",
            "C4": "1 in <Q6,D134,D012>",
            "R8": "K-linear Macaulay bound 7, rank 32/32, <D134,D012,D013>",
            "p2_plus_1": "K-linear Macaulay bound 5, rank 24/24, <D134,D012,D145>",
            "R4": "K-linear Macaulay bound 5, rank 24/24, <D134,D012,D145>",
            "F4": "sparse total-degree Macaulay bound 3 in A[a,B,z], rank 68/80",
            "p2_minus_2p_plus_2": "sparse total-degree Macaulay bound 3 in A[a,B,z], rank 66/80",
            "F40": "quotient-Euclid D134,D145; unnormalised c; nonzero 4x4 multiplication norm",
        },
        "gates": {
            "B": "B!=0",
            "H2": "H2!=0 and Q6 q-leading coefficient",
            "Delta": "Delta!=0",
            "P": "P divides Delta and is outside the open",
        },
    }


def _json_safe(value: Any) -> Any:
    """Drop transient quotient objects before serializing a certificate."""
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def write_certificate(payload: dict[str, Any], output: Path) -> dict[str, Any]:
    payload = _json_safe(payload)
    payload["verifier_path"] = Path(__file__).resolve().relative_to(ROOT).as_posix()
    payload["verifier_sha256"] = lf_sha256(Path(__file__).resolve())
    payload["verifier_raw_sha256"] = sha256_file(Path(__file__).resolve())
    payload["verifier_hash_semantics"] = (
        "verifier_sha256 is the LF-normalized tracked-source digest; "
        "verifier_raw_sha256 records checkout bytes"
    )
    payload["runtime_environment"] = {
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "platform": platform.platform(),
        "executable": sys.executable,
        "implementation_flags": {
            name: {
                "effective_value": int(_implementation_flag(name)[0]),
                "source": _implementation_flag(name)[1],
            }
            for name in (FACTOR_MATRIX_INVERSE_ENV, FACTOR_NO_FINAL_INVERSE_ENV)
        },
    }
    payload["certificate_payload_definition"] = (
        "sha256 of canonical JSON payload before certificate_payload_sha256 is added"
    )
    canonical = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload["certificate_payload_sha256"] = sha256_bytes(canonical.encode())
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    try:
        certificate_path = output.relative_to(ROOT).as_posix()
    except ValueError:
        certificate_path = "<outside-repository>"
    return {
        "status": payload["status"],
        "claim_id": payload["claim_id"],
        "global_conjecture": payload["global_conjecture"],
        "runtime_mode": payload["runtime_mode"],
        "certificate_path": certificate_path,
        "certificate_file_sha256": sha256_file(output),
        "certificate_payload_sha256": payload["certificate_payload_sha256"],
        "verifier_path": payload["verifier_path"],
        "verifier_sha256": payload["verifier_sha256"],
        "verifier_raw_sha256": payload["verifier_raw_sha256"],
    }


def main(argv=None) -> int:
    started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-only", action="store_true", help="check source pins and write a fast manifest")
    parser.add_argument("--bridge-only", action="store_true", help="rebuild the exact syndrome/minor bridge only")
    parser.add_argument(
        "--targeted-fibres",
        action="store_true",
        help="replay only the R8, p^2+1, R4, and F4 local fibre leaves",
    )
    parser.add_argument(
        "--targeted-p2-minus",
        action="store_true",
        help="replay only the p^2-2p+2 affine local fibre leaf",
    )
    parser.add_argument(
        "--targeted-f40",
        action="store_true",
        help="replay only the F40 quotient-Euclid local fibre leaf",
    )
    parser.add_argument(
        "--certificate-out",
        type=Path,
        default=None,
        help=(
            "certificate output path; required for manifest/partial modes so "
            "they cannot overwrite the durable full-replay certificate"
        ),
    )
    args = parser.parse_args(argv)
    replay_modes = sum(
        bool(value)
        for value in (
            args.bridge_only,
            args.targeted_fibres,
            args.targeted_p2_minus,
            args.targeted_f40,
        )
    )
    if args.manifest_only and replay_modes:
        parser.error("--manifest-only cannot be combined with another replay mode")
    if replay_modes > 1:
        parser.error("replay modes are mutually exclusive")
    if args.certificate_out is None:
        if args.manifest_only or replay_modes:
            parser.error(
                "--certificate-out is required for manifest-only, bridge-only, "
                "and targeted replay modes"
            )
        args.certificate_out = CERTIFICATE

    manifest = source_manifest()
    optional_manifest = optional_source_manifest()
    if args.manifest_only:
        result = static_certificate("manifest-only", manifest, optional_manifest)
        result["elapsed_seconds"] = round(time.perf_counter() - started, 3)
        print(json.dumps(write_certificate(result, args.certificate_out), indent=2, sort_keys=True))
        return 0

    bridge = build_bridge(manifest)
    algebra = bridge.pop("_algebra")
    determinants = bridge.pop("_determinants")
    p_values = bridge.pop("_p_values")
    runtime_mode = (
        "targeted-fibres"
        if args.targeted_fibres
        else (
            "targeted-p2-minus"
            if args.targeted_p2_minus
            else (
                "targeted-f40"
                if args.targeted_f40
                else ("bridge-only" if args.bridge_only else "full")
            )
        )
    )
    result = static_certificate(
        runtime_mode, manifest, optional_manifest
    )
    result.update(bridge)
    result["replay_complete"] = False
    if args.bridge_only:
        result["exact_arithmetic"] = {"status": "not_run_in_bridge_only_mode"}
        result["local_fibre_closures"] = {"status": "not_run_in_bridge_only_mode"}
    elif args.targeted_fibres:
        # This diagnostic deliberately avoids the expensive p-cover and the
        # tracked GLD102 call.  It exercises the four corrected Macaulay
        # leaves against freshly reconstructed determinant inputs.
        result["exact_arithmetic"] = {"status": "not_run_in_targeted_fibre_mode"}
        result["p0_p1_gld102"] = {"status": "not_run_in_targeted_fibre_mode"}
        result["local_fibre_closures"] = local_fibre_ledger(
            determinants,
            p_values,
            algebra,
            selected=("R8", "p2_plus_1", "R4", "F4"),
        )
    elif args.targeted_p2_minus:
        result["exact_arithmetic"] = {"status": "not_run_in_targeted_fibre_mode"}
        result["p0_p1_gld102"] = {"status": "not_run_in_targeted_fibre_mode"}
        result["local_fibre_closures"] = local_fibre_ledger(
            determinants,
            p_values,
            algebra,
            selected=("p2_minus_2p_plus_2",),
        )
    elif args.targeted_f40:
        result["exact_arithmetic"] = {"status": "not_run_in_targeted_fibre_mode"}
        result["p0_p1_gld102"] = {"status": "not_run_in_targeted_fibre_mode"}
        result["local_fibre_closures"] = local_fibre_ledger(
            determinants,
            p_values,
            algebra,
            selected=("F40",),
        )
    else:
        result["exact_arithmetic"] = exact_p_cover(
            {name: determinants[name] for name in SELECTED_TRIPLES}, algebra
        )
        result["p0_p1_gld102"] = run_gld102_check()
        result["local_fibre_closures"] = local_fibre_ledger(determinants, p_values, algebra)
        result["replay_complete"] = True
    result["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    print(json.dumps(write_certificate(result, args.certificate_out), indent=2, sort_keys=True))
    return 0


def _integer_sparse_polynomial_in_variables(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> tuple[dict[tuple[int, ...], int], dict[str, Any]]:
    """Clear one common rational content from an exact sparse polynomial.

    The quotient representation can leave a denominator in p (normally a
    power of H2).  It is allowed only when it is independent of every other
    variable; the declared H2/Delta open then makes this localization
    legitimate.  Keeping this operation on the *whole* polynomial is
    important for the affine P_i rows: independently primitive-normalizing
    their B-coefficients changes the ideal by changing their relative scales.
    """
    numerator, denominator = sp.cancel(sp.sympify(expression)).as_numer_denom()
    variables = tuple(variables)
    denominator = sp.factor(denominator)
    denominator_poly = sp.Poly(denominator, *variables, domain=QQ)
    non_p_variables = [variable for variable in variables if variable != p]
    if any(denominator_poly.degree(variable) > 0 for variable in non_p_variables):
        raise AssertionError(("non-p-only quotient denominator", expression, denominator))
    polynomial = sp.Poly(sp.expand(numerator), *variables, domain=QQ)
    rational_content, primitive = polynomial.primitive()
    integer_denominator, integer_poly = primitive.clear_denoms(convert=True)
    integer_content = int(rational_content) if rational_content.is_Integer else str(rational_content)
    terms: dict[tuple[int, ...], int] = {}
    for monomial, coefficient in integer_poly.terms():
        if not coefficient.is_Integer:
            raise AssertionError(("nonintegral resultant input", monomial, coefficient))
        value = int(coefficient)
        if value:
            terms[tuple(int(index) for index in monomial)] = value
    if not terms:
        raise AssertionError("zero polynomial entered into resultant")
    quotient_denominator = _quotient_denominator_provenance(denominator)
    terms_payload = [
        [list(monomial), coefficient]
        for monomial, coefficient in sorted(terms.items())
    ]
    return terms, {
        "variables": [str(variable) for variable in variables],
        "denominator": str(denominator),
        "integer_denominator": int(integer_denominator),
        "rational_content": integer_content,
        "term_count": len(terms),
        "quotient_denominator_provenance": quotient_denominator,
        "terms_sha256": sha256_bytes(
            json.dumps(terms_payload, separators=(",", ":")).encode()
        ),
    }


def _integer_sparse_polynomial(
    expression: sp.Expr, variables=(p, a, q)
) -> tuple[dict[tuple[int, ...], int], dict[str, Any]]:
    """Clear one common content from a Q6-reduced ``(p,a,q)`` polynomial."""
    variables = tuple(variables)
    if variables != (p, a, q):
        raise AssertionError("unexpected sparse-polynomial variable basis")
    return _integer_sparse_polynomial_in_variables(expression, variables)


def _flint_canonical_hash(poly) -> str:
    payload = [
        [list(tuple(int(value) for value in exponent)), int(coefficient)]
        for exponent, coefficient in poly.terms()
    ]
    return sha256_bytes(json.dumps(payload, separators=(",", ":")).encode())


def _flint_degree(poly, variable: int = 0) -> int:
    degrees = poly.degrees()
    return int(degrees[variable]) if degrees else -1


def _flint_normalize_sign(poly):
    return -poly if int(poly.leading_coefficient()) < 0 else poly


def _flint_from_terms(ctx, terms: dict[tuple[int, ...], int]):
    return ctx.from_dict({tuple(int(v) for v in exponent): int(coefficient) for exponent, coefficient in terms.items()})


def _flint_p_only(poly) -> bool:
    return all(exponent[1] == 0 and exponent[2] == 0 for exponent, _ in poly.terms())


def _expected_flint_factors(ctx):
    p_var, _a_var, _q_var = ctx.gens()
    f40 = ctx.from_dict({
        (40 - index, 0, 0): int(coefficient)
        for index, coefficient in enumerate(F40_DESC)
        if coefficient
    })
    return [
        64 * p_var**8 - 256 * p_var**7 + 580 * p_var**6 - 844 * p_var**5 + 946 * p_var**4 - 784 * p_var**3 + 388 * p_var**2 - 94 * p_var + 13,
        p_var**2 + 1,
        5 * p_var**4 - 16 * p_var**3 + 30 * p_var**2 - 16 * p_var + 5,
        5 * p_var**4 - 4 * p_var**3 + 12 * p_var**2 - 16 * p_var + 8,
        8 * p_var**4 - 16 * p_var**3 + 12 * p_var**2 - 4 * p_var + 5,
        f40,
        p_var**2 - 2 * p_var + 2,
        p_var - 1,
        2 * p_var**2 - 2 * p_var + 1,
        p_var,
        p_var**2 - p_var + 1,
    ]


EXPECTED_FACTOR_NAMES = (
    "R8",
    "p2_plus_1",
    "R4",
    "F4",
    "C4",
    "F40",
    "p2_minus_2p_plus_2",
    "p_minus_1",
    "H2",
    "p",
    "P",
)


def exact_p_cover(determinants: dict[str, Any], algebra: Algebra) -> dict[str, Any]:
    """Compute the six-row p-cover with python-flint only.

    ``D012`` is paired with each of the other five selected coefficient
    determinants.  A q-resultant removes Q6, the p-only gcd is stripped, and
    an a-resultant produces a p-only pair cover.  Their gcd is then factored
    and compared with the pinned eleven-factor support.  All inputs are
    regenerated from the tracked bridge in this process.
    """
    try:
        import flint
        from flint import fmpz_mpoly_ctx
    except ImportError as exc:
        raise RuntimeError("GLD103_FLINT_REQUIRED: install python-flint 0.9.0") from exc
    version = str(getattr(flint, "__version__", ""))
    if version != "0.9.0":
        raise RuntimeError(f"GLD103_FLINT_VERSION_REQUIRED=0.9.0 observed={version!r}")
    ctx = fmpz_mpoly_ctx.get(("p", "a", "q"), ordering="lex")
    q6_terms, q6_meta = _integer_sparse_polynomial(algebra.q6_expr)
    q6_poly = _flint_from_terms(ctx, q6_terms)
    determinant_polys = {}
    input_meta = {"Q6": q6_meta}
    for name, value in determinants.items():
        expression = algebra.as_expr(value)
        terms, metadata = _integer_sparse_polynomial(expression)
        determinant_polys[name] = _flint_from_terms(ctx, terms)
        input_meta[name] = metadata

    resultants: dict[str, Any] = {}
    resultant_meta: dict[str, Any] = {}
    for name in SELECTED_TRIPLES:
        value = q6_poly.resultant(determinant_polys[name], 2)
        if value == 0:
            raise AssertionError(f"zero q-resultant for {name}")
        resultants[name] = value
        resultant_meta[name] = {
            "degree_p": _flint_degree(value),
            "degree_a": _flint_degree(value, 1),
            "term_count": len(list(value.terms())),
            "canonical_sha256": _flint_canonical_hash(value),
        }

    covers = []
    pair_meta = {}
    base = resultants["D012"]
    # The p-cover uses exactly the six selected determinants.  D134 and D145
    # are fibre-only leaves and are intentionally not mixed into this cover.
    for name in ("D013", "D023", "D123", "D014", "D015"):
        other = resultants[name]
        common = base.gcd(other)
        if not _flint_p_only(common):
            raise AssertionError(f"non-p-only q-resultant gcd for {name}")
        left, rem_left = divmod(base, common)
        right, rem_right = divmod(other, common)
        if rem_left != 0 or rem_right != 0:
            raise AssertionError(f"inexact q-resultant gcd division for {name}")
        a_resultant = left.resultant(right, 1)
        if a_resultant == 0 or not _flint_p_only(a_resultant):
            raise AssertionError(f"bad a-resultant for {name}")
        cover = common * a_resultant
        covers.append(cover)
        pair_meta[name] = {
            "q_gcd_degree_p": _flint_degree(common),
            "a_resultant_degree_p": _flint_degree(a_resultant),
            "cover_degree_p": _flint_degree(cover),
            "cover_canonical_sha256": _flint_canonical_hash(cover),
        }

    final = covers[0]
    for cover in covers[1:]:
        final = final.gcd(cover)
    if not _flint_p_only(final):
        raise AssertionError("final all-zero cover is not p-only")
    raw_final_degree = _flint_degree(final)
    raw_final_hash = _flint_canonical_hash(final)
    raw_final = final
    _raw_unit, raw_factorization = raw_final.factor()
    raw_factors = []
    for factor, exponent in raw_factorization:
        factor = _flint_normalize_sign(factor)
        raw_factors.append(
            {
                "degree_p": _flint_degree(factor),
                "exponent": int(exponent),
                "canonical_sha256": _flint_canonical_hash(factor),
            }
        )
    # The tracked native determinant presentation is authoritative here.  Its
    # exact gcd has degree 624.  Since the Q6 quotient is H2-localized, we
    # additionally compute (but do not depend on) the degree-620 open-chart
    # representative by two exact H2 divisions below.
    h2_poly = 2 * ctx.gens()[0] ** 2 - 2 * ctx.gens()[0] + 1
    removed_h2 = 0
    for _ in range(2):
        quotient_final, remainder_final = divmod(final, h2_poly)
        if remainder_final != 0:
            raise AssertionError(("missing H2 localization multiplicity", removed_h2))
        final = quotient_final
        removed_h2 += 1
    # The normalized/open-chart cover intentionally retains the genuine H2^47
    # factor.  Further H2 divisions are therefore expected; the exact
    # normalized factorization and the raw-vs-normalized exponent difference
    # below distinguish those genuine copies from the two localization copies.
    if final * (h2_poly**removed_h2) != raw_final:
        raise AssertionError("H2 localization division does not reconstruct the raw cover")
    normalized_final_degree = _flint_degree(final)
    normalized_final_hash = _flint_canonical_hash(final)
    if normalized_final_degree != raw_final_degree - removed_h2 * _flint_degree(h2_poly):
        raise AssertionError(("normalized p-cover degree drift", normalized_final_degree, raw_final_degree))
    unit, factorization = final.factor()
    raw_actual = {
        _flint_canonical_hash(_flint_normalize_sign(factor))
        for factor, _exponent in raw_factorization
    }
    actual = {
        _flint_canonical_hash(_flint_normalize_sign(factor))
        for factor, _exponent in factorization
    }
    expected_factors = _expected_flint_factors(ctx)
    if len(expected_factors) != len(EXPECTED_FACTOR_NAMES):
        raise AssertionError("expected factor-name table drift")
    expected = {
        _flint_canonical_hash(_flint_normalize_sign(factor))
        for factor in expected_factors
    }
    expected_by_hash = {
        _flint_canonical_hash(_flint_normalize_sign(factor)): name
        for name, factor in zip(EXPECTED_FACTOR_NAMES, expected_factors)
    }
    if raw_actual != expected or actual != raw_actual:
        raise AssertionError(
            f"exact p-cover support mismatch raw={sorted(raw_actual)} normalized={sorted(actual)} expected={sorted(expected)}"
        )
    factors = []
    for factor, exponent in factorization:
        factor = _flint_normalize_sign(factor)
        factors.append(
            {
                "degree_p": _flint_degree(factor),
                "exponent": int(exponent),
                "canonical_sha256": _flint_canonical_hash(factor),
            }
        )
    for factor_record in [*raw_factors, *factors]:
        factor_name = expected_by_hash.get(factor_record["canonical_sha256"])
        if factor_name is None:
            raise AssertionError(("unbound p-cover factor hash", factor_record))
        factor_record["name"] = factor_name
    raw_names = {item["name"] for item in raw_factors}
    normalized_names = {item["name"] for item in factors}
    if raw_names != set(EXPECTED_FACTOR_NAMES) or normalized_names != set(EXPECTED_FACTOR_NAMES):
        raise AssertionError(("p-cover factor-name support drift", raw_names, normalized_names))
    final_degree = _flint_degree(raw_final)
    if final_degree != 624 or len(raw_factorization) != 11 or len(factorization) != 11:
        raise AssertionError(
            (
                "p-cover degree/factor count drift",
                final_degree,
                len(raw_factorization),
                len(factorization),
                [(int(factor.degrees()[0]), int(exponent), _flint_canonical_hash(_flint_normalize_sign(factor))) for factor, exponent in raw_factorization],
            )
        )
    expected_raw_exponents = sorted((1, 2, 2, 2, 2, 2, 10, 46, 49, 96, 124))
    actual_raw_exponents = sorted(int(exponent) for _factor, exponent in raw_factorization)
    if actual_raw_exponents != expected_raw_exponents:
        raise AssertionError(("native p-cover multiplicity drift", actual_raw_exponents, expected_raw_exponents))
    expected_normalized_exponents = sorted((1, 2, 2, 2, 2, 2, 10, 46, 47, 96, 124))
    actual_exponents = sorted(int(exponent) for _factor, exponent in factorization)
    if actual_exponents != expected_normalized_exponents:
        raise AssertionError(("normalized p-cover multiplicity drift", actual_exponents, expected_normalized_exponents))
    expected_raw_by_name = {
        "R8": 1,
        "p2_plus_1": 2,
        "R4": 2,
        "F4": 2,
        "C4": 2,
        "F40": 2,
        "p2_minus_2p_plus_2": 10,
        "p_minus_1": 46,
        "H2": 49,
        "p": 96,
        "P": 124,
    }
    expected_normalized_by_name = {**expected_raw_by_name, "H2": 47}
    raw_exponents_by_name = {item["name"]: item["exponent"] for item in raw_factors}
    normalized_exponents_by_name = {item["name"]: item["exponent"] for item in factors}
    if raw_exponents_by_name != expected_raw_by_name:
        raise AssertionError(("native p-cover named multiplicity drift", raw_exponents_by_name, expected_raw_by_name))
    if normalized_exponents_by_name != expected_normalized_by_name:
        raise AssertionError(("normalized p-cover named multiplicity drift", normalized_exponents_by_name, expected_normalized_by_name))
    raw_support = {item["canonical_sha256"] for item in raw_factors}
    normalized_support = {item["canonical_sha256"] for item in factors}
    if raw_support != normalized_support:
        raise AssertionError("H2 localization changed squarefree factor support")
    h2_hash = _flint_canonical_hash(_flint_normalize_sign(h2_poly))
    raw_h2_exponent = next(
        (item["exponent"] for item in raw_factors if item["canonical_sha256"] == h2_hash),
        0,
    )
    normalized_h2_exponent = next(
        (item["exponent"] for item in factors if item["canonical_sha256"] == h2_hash),
        0,
    )
    if raw_h2_exponent != normalized_h2_exponent + removed_h2:
        raise AssertionError(("H2 localization exponent drift", raw_h2_exponent, normalized_h2_exponent))
    if raw_final_degree != normalized_final_degree + removed_h2 * _flint_degree(h2_poly):
        raise AssertionError(("H2 localization degree drift", raw_final_degree, normalized_final_degree))
    squarefree_support_degree = sum(_flint_degree(_flint_normalize_sign(factor)) for factor, _ in factorization)
    return {
        "status": "verified_exact_necessary_p_cover",
        "arithmetic": "python-flint fmpz_mpoly exact resultants/gcd/factorization",
        "python_flint_version": version,
        "ring": "Z[p,a,q] lex; q-resultant variable index 2, a-resultant variable index 1",
        "q6": {"term_count": len(list(q6_poly.terms())), "canonical_sha256": _flint_canonical_hash(q6_poly)},
        "inputs": input_meta,
        "q_resultants": resultant_meta,
        "pair_covers": pair_meta,
        "authoritative_representation": "tracked_native_resultant_gcd",
        "final_degree_p": final_degree,
        "final_canonical_sha256": raw_final_hash,
        "raw_final_degree_p": raw_final_degree,
        "raw_final_canonical_sha256": raw_final_hash,
        "raw_factor_count": len(raw_factorization),
        "raw_factors": sorted(raw_factors, key=lambda item: (item["degree_p"], item["canonical_sha256"])),
        "raw_squarefree_support_degree_p": sum(item["degree_p"] for item in raw_factors),
        "raw_h2_exponent": raw_h2_exponent,
        "normalized_h2_exponent": normalized_h2_exponent,
        "raw_exponents_by_factor": dict(sorted(raw_exponents_by_name.items())),
        "normalized_exponents_by_factor": dict(sorted(normalized_exponents_by_name.items())),
        "normalized_open_cover_degree_p": normalized_final_degree,
        "normalized_open_cover_canonical_sha256": normalized_final_hash,
        "localization_normalization": {
            "factor": "H2",
            "removed_exponent": removed_h2,
            "exact_division_checked": True,
            "raw_reconstruction_checked": True,
            "reason": "q-quotient relation denominators; H2 is already outside the declared open",
        },
        "factor_count": len(raw_factorization),
        "factors": sorted(raw_factors, key=lambda item: (item["degree_p"], item["canonical_sha256"])),
        "normalized_open_cover_factors": sorted(
            factors, key=lambda item: (item["degree_p"], item["canonical_sha256"])
        ),
        "factor_support_match": True,
        "support_only_comparison": True,
        "squarefree_support_match": True,
        "squarefree_support_degree_p": squarefree_support_degree,
        "multiplicity_degree_p": final_degree,
        "normalized_multiplicity_degree_p": normalized_final_degree,
        "support_factor_degrees": sorted(item["degree_p"] for item in raw_factors),
        "raw_cover_localization_equivalent": True,
        "open_invariance": {
            "declared_open": "D(B*H2*Delta)",
            "removed_factor": "H2^2",
            "reason": "H2 is inverted by the normalized Q6 chart and already excluded by the declared open",
            "squarefree_support_preserved": True,
        },
    }


def _factor_expression(name: str) -> sp.Expr:
    factors = {
        "R8": 64 * p**8 - 256 * p**7 + 580 * p**6 - 844 * p**5 + 946 * p**4 - 784 * p**3 + 388 * p**2 - 94 * p + 13,
        "p2_plus_1": p**2 + 1,
        "R4": 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
        "F4": 5 * p**4 - 4 * p**3 + 12 * p**2 - 16 * p + 8,
        "C4": 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
        "F40": sum(value * p ** (40 - index) for index, value in enumerate(F40_DESC)),
        "p2_minus_2p_plus_2": p**2 - 2 * p + 2,
        "p_minus_1": p - 1,
        "H2": H2,
        "p": p,
        "P": P,
    }
    try:
        return sp.expand(factors[name])
    except KeyError as exc:
        raise AssertionError(f"unknown GLD103 factor {name}") from exc


class _FactorField:
    """Exact K=QQ[p]/(f), backed by python-flint rational polynomials."""

    def __init__(self, descending_coefficients: tuple[int, ...], matrix_inverse: bool):
        from flint import fmpq, fmpq_mat, fmpq_poly

        self._fmpq = fmpq
        self._fmpq_mat = fmpq_mat
        self._fmpq_poly = fmpq_poly
        self.modulus = fmpq_poly([int(c) for c in reversed(descending_coefficients)])
        self.zero = fmpq_poly([0])
        self.one = fmpq_poly([1])
        self.degree = int(self.modulus.degree())
        self.matrix_inverse = bool(matrix_inverse)
        self._powers = [self.one]

    def normalize(self, value):
        value = self._fmpq_poly(value)
        if value.is_zero() or value.degree() < self.degree:
            return value
        return value % self.modulus

    def integer(self, value: int):
        return self._fmpq_poly([int(value)])

    def power(self, exponent: int):
        while len(self._powers) <= exponent:
            self._powers.append(self.normalize(self._powers[-1] * self._fmpq_poly([0, 1])))
        return self._powers[exponent]

    def add(self, left, right):
        return self.normalize(left + right)

    def neg(self, value):
        return self.normalize(-value)

    def sub(self, left, right):
        return self.normalize(left - right)

    def mul(self, left, right):
        return self.normalize(left * right)

    def scale(self, left, coefficient):
        return self.normalize(left * coefficient)

    def inv(self, value):
        value = self.normalize(value)
        if value.is_zero():
            raise ZeroDivisionError("zero in factor field")
        if self.matrix_inverse:
            rows = []
            for row_index in range(self.degree):
                row = []
                for column in range(self.degree):
                    product = self.normalize(value * self._fmpq_poly([0] * column + [1]))
                    coefficients = product.coeffs()
                    row.append(coefficients[row_index] if row_index < len(coefficients) else 0)
                rows.append(row)
            matrix = self._fmpq_mat(rows)
            rhs = self._fmpq_mat([[1]] + [[0]] * (self.degree - 1))
            solution = matrix.solve(rhs)
            return self.normalize(self._fmpq_poly([solution[index, 0] for index in range(self.degree)]))
        from flint import fmpz_poly

        denominator = int(value.denom())
        numerator = fmpz_poly([int(coefficient * denominator) for coefficient in value.coeffs()])
        modulus_integer = fmpz_poly([int(coefficient) for coefficient in self.modulus.coeffs()])
        gcd, multiplier, _other = self._fmpq_poly(numerator).xgcd(self._fmpq_poly(modulus_integer))
        if gcd.degree() != 0 or gcd[0] == 0:
            raise ZeroDivisionError("nonunit in factor field")
        return self.normalize(multiplier * (self._fmpq(denominator) / gcd[0]))


class _QAlgebra:
    """A=K[q]/(Q6), with four K coefficients low-q first."""

    def __init__(self, field: _FactorField, q6_terms: dict[tuple[int, ...], int]):
        self.K = field
        self.q6_terms = {
            tuple(int(index) for index in monomial): int(coefficient)
            for monomial, coefficient in q6_terms.items()
        }
        self.q6_input_sha256 = sha256_bytes(
            json.dumps(
                [
                    [list(monomial), coefficient]
                    for monomial, coefficient in sorted(self.q6_terms.items())
                ],
                separators=(",", ":"),
            ).encode()
        )
        q6 = [field.zero for _ in range(5)]
        for (p_degree, a_degree, q_degree), coefficient in self.q6_terms.items():
            if a_degree or q_degree > 4:
                raise AssertionError("unexpected Q6 support in factor field")
            q6[q_degree] = field.add(q6[q_degree], field.scale(field.power(p_degree), coefficient))
        lead_inverse = field.inv(q6[4])
        self.q6_full = tuple(q6)
        self.relation = tuple(field.neg(field.mul(q6[index], lead_inverse)) for index in range(4))
        self.zero = (field.zero, field.zero, field.zero, field.zero)
        self.one = (field.one, field.zero, field.zero, field.zero)

    def is_zero(self, value):
        return all(item.is_zero() for item in value)

    def add(self, left, right):
        return tuple(self.K.add(x, y) for x, y in zip(left, right))

    def neg(self, value):
        return tuple(self.K.neg(item) for item in value)

    def sub(self, left, right):
        return self.add(left, self.neg(right))

    def reduce(self, values):
        values = list(values)
        while len(values) > 4:
            degree = len(values) - 1
            coefficient = values.pop()
            if coefficient.is_zero():
                continue
            for index, relation_coefficient in enumerate(self.relation):
                location = degree - 4 + index
                values[location] = self.K.add(
                    values[location], self.K.mul(coefficient, relation_coefficient)
                )
        values.extend([self.K.zero] * (4 - len(values)))
        return tuple(values[:4])

    def mul(self, left, right):
        values = [self.K.zero for _ in range(7)]
        for left_degree, left_value in enumerate(left):
            if left_value.is_zero():
                continue
            for right_degree, right_value in enumerate(right):
                if not right_value.is_zero():
                    values[left_degree + right_degree] = self.K.add(
                        values[left_degree + right_degree],
                        self.K.mul(left_value, right_value),
                    )
        return self.reduce(values)

    def from_raw_q(self, raw: dict[int, Any]):
        values = [self.K.zero for _ in range(max(raw.keys(), default=0) + 1)]
        for degree, value in raw.items():
            values[int(degree)] = self.K.add(values[int(degree)], value)
        return self.reduce(values)


def _hash_k_values(values: list[Any] | tuple[Any, ...]) -> str:
    return sha256_bytes(
        json.dumps([str(value) for value in values], separators=(",", ":")).encode()
    )


def _hash_k_matrix(matrix: list[list[Any]]) -> str:
    return sha256_bytes(
        json.dumps(
            [[str(value) for value in row] for row in matrix],
            separators=(",", ":"),
        ).encode()
    )


def _hash_a_poly(poly: list[Any]) -> str:
    return _hash_k_values(tuple(poly))


def _hash_multivariate_poly(poly: dict[tuple[int, ...], Any]) -> str:
    payload = [
        [list(monomial), [str(value) for value in coefficient]]
        for monomial, coefficient in sorted(poly.items())
    ]
    return sha256_bytes(json.dumps(payload, separators=(",", ":")).encode())


def _quotient_input_metadata(quotient: _QAlgebra) -> dict[str, Any]:
    """Pin the exact local Q6 relation and quotient basis used by a leaf."""
    return {
        "q6_term_count": len(quotient.q6_terms),
        "q6_terms_sha256": quotient.q6_input_sha256,
        "q6_reduced_coefficients_sha256": _hash_k_values(quotient.q6_full),
        "q6_relation_sha256": _hash_k_values(quotient.relation),
        "q_basis_dimension": 4,
        "factor_modulus_sha256": _hash_k_values((quotient.K.modulus,)),
    }


def _trim_a(poly: list[Any], algebra: _QAlgebra) -> list[Any]:
    poly = list(poly)
    while poly and algebra.is_zero(poly[-1]):
        poly.pop()
    return poly


def _a_add(left: list[Any], right: list[Any], algebra: _QAlgebra) -> list[Any]:
    output = []
    for index in range(max(len(left), len(right))):
        output.append(
            algebra.add(
                left[index] if index < len(left) else algebra.zero,
                right[index] if index < len(right) else algebra.zero,
            )
        )
    return _trim_a(output, algebra)


def _a_neg(value: list[Any], algebra: _QAlgebra) -> list[Any]:
    return _trim_a([algebra.neg(item) for item in value], algebra)


def _a_sub(left: list[Any], right: list[Any], algebra: _QAlgebra) -> list[Any]:
    return _a_add(left, _a_neg(right, algebra), algebra)


def _a_mul(left: list[Any], right: list[Any], algebra: _QAlgebra) -> list[Any]:
    if not left or not right:
        return []
    output = [algebra.zero for _ in range(len(left) + len(right) - 1)]
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            output[left_degree + right_degree] = algebra.add(
                output[left_degree + right_degree], algebra.mul(left_value, right_value)
            )
    return _trim_a(output, algebra)


def _a_scale(left: list[Any], coefficient: Any, algebra: _QAlgebra) -> list[Any]:
    return _trim_a([algebra.mul(item, coefficient) for item in left], algebra)


def _raw_to_a_poly(raw: dict[tuple[int, ...], int], field: _FactorField, algebra: _QAlgebra) -> list[Any]:
    rows: list[dict[int, Any]] = []
    for (p_degree, a_degree, q_degree), coefficient in raw.items():
        while len(rows) <= a_degree:
            rows.append({})
        rows[a_degree][q_degree] = field.add(
            rows[a_degree].get(q_degree, field.zero),
            field.scale(field.power(p_degree), coefficient),
        )
    return _trim_a([algebra.from_raw_q(row) for row in rows], algebra)


def _k_rank(rows: list[list[Any]], field: _FactorField) -> int:
    """Exact Gaussian rank over the exact factor field."""
    _rref, pivots = _k_rref(rows, field)
    return len(pivots)


def _k_rref(rows: list[list[Any]], field: _FactorField):
    """Return exact row RREF and pivot columns over the factor field."""
    if not rows:
        return [], []
    matrix = [list(row) for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    pivots = []
    for column in range(column_count):
        pivot = next((index for index in range(rank, row_count) if not matrix[index][column].is_zero()), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = field.inv(matrix[rank][column])
        matrix[rank] = [field.mul(value, inverse) for value in matrix[rank]]
        for row in range(row_count):
            if row == rank or matrix[row][column].is_zero():
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                field.sub(left, field.mul(multiplier, right))
                for left, right in zip(matrix[row], matrix[rank])
            ]
        pivots.append(column)
        rank += 1
        if rank == row_count:
            break
    return matrix, pivots


def _k_reduce_against_rref(
    vector: list[Any], rref: list[list[Any]], pivots: list[int], field: _FactorField
) -> list[Any]:
    residual = list(vector)
    for pivot, row in zip(pivots, rref):
        multiplier = residual[pivot]
        if multiplier.is_zero():
            continue
        residual = [
            field.sub(left, field.mul(multiplier, right))
            for left, right in zip(residual, row)
        ]
    return residual


def _a_vector(poly: list[Any], bound: int, quotient: _QAlgebra) -> list[Any]:
    values = []
    for a_degree in range(bound + 1):
        value = poly[a_degree] if a_degree < len(poly) else quotient.zero
        values.extend(value)
    return values


def _a_macaulay_membership(generators: list[list[Any]], bound: int, quotient: _QAlgebra) -> dict[str, Any]:
    rows: list[list[Any]] = []
    q_basis = [
        quotient.from_raw_q({q_degree: quotient.K.one})
        for q_degree in range(4)
    ]
    for generator in generators:
        for q_multiplier in q_basis:
            q_generator = [quotient.mul(value, q_multiplier) for value in generator]
            degree = len(q_generator) - 1
            if degree > bound:
                continue
            for shift in range(bound - degree + 1):
                rows.append(_a_vector([quotient.zero] * shift + q_generator, bound, quotient))
    target = _a_vector([quotient.one], bound, quotient)
    rref, pivots = _k_rref(rows, quotient.K)
    residual = _k_reduce_against_rref(target, rref, pivots, quotient.K)
    before = len(pivots)
    after = _k_rank(rows + [target], quotient.K)
    target_in_span = all(value.is_zero() for value in residual)
    return {
        "bound": bound,
        "row_count": len(rows),
        "q_basis_multiplier_count": len(q_basis),
        "q_basis_multiplier_sha256": [_hash_k_values(multiplier) for multiplier in q_basis],
        "columns": len(target),
        "rank": before,
        "rank_with_target": after,
        "target_in_span": target_in_span,
        "rref_pivots": pivots,
        "input_matrix_sha256": _hash_k_matrix(rows),
        "rref_matrix_sha256": _hash_k_matrix(rref),
        "target_sha256": _hash_k_values(target),
        "target_residual_sha256": _hash_k_values(residual),
        "target_residual_zero": target_in_span,
        "generator_sha256": [_hash_a_poly(generator) for generator in generators],
        "quotient_input": _quotient_input_metadata(quotient),
    }


def _monomials_total_degree(variable_count: int, bound: int):
    output = []
    for exponents in itertools.product(range(bound + 1), repeat=variable_count):
        if sum(exponents) <= bound:
            output.append(tuple(exponents))
    return sorted(output, key=lambda item: (sum(item), item))


def _mv_add(left: dict[tuple[int, ...], Any], right: dict[tuple[int, ...], Any], quotient: _QAlgebra):
    output = dict(left)
    for monomial, coefficient in right.items():
        updated = quotient.add(output.get(monomial, quotient.zero), coefficient)
        if quotient.is_zero(updated):
            output.pop(monomial, None)
        else:
            output[monomial] = updated
    return output


def _mv_mul(left: dict[tuple[int, ...], Any], right: dict[tuple[int, ...], Any], quotient: _QAlgebra):
    output: dict[tuple[int, ...], Any] = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(x + y for x, y in zip(left_monomial, right_monomial))
            product = quotient.mul(left_value, right_value)
            output[monomial] = quotient.add(output.get(monomial, quotient.zero), product)
    return {monomial: value for monomial, value in output.items() if not quotient.is_zero(value)}


def _mv_vector(poly: dict[tuple[int, ...], Any], monomials: list[tuple[int, ...]], quotient: _QAlgebra):
    values = []
    for monomial in monomials:
        values.extend(poly.get(monomial, quotient.zero))
    return values


def _multivariate_macaulay(generators: list[dict[tuple[int, ...], Any]], bound: int, quotient: _QAlgebra) -> dict[str, Any]:
    monomials = _monomials_total_degree(3, bound)
    rows = []
    q_basis = [
        quotient.from_raw_q({q_degree: quotient.K.one})
        for q_degree in range(4)
    ]
    for generator in generators:
        for q_multiplier in q_basis:
            q_generator = {
                monomial: quotient.mul(coefficient, q_multiplier)
                for monomial, coefficient in generator.items()
            }
            generator_degree = max((sum(monomial) for monomial in q_generator), default=0)
            if generator_degree > bound:
                continue
            for multiplier in _monomials_total_degree(3, bound - generator_degree):
                multiplier_poly = {multiplier: quotient.one}
                product = _mv_mul(q_generator, multiplier_poly, quotient)
                rows.append(_mv_vector(product, monomials, quotient))
    target = _mv_vector({(0, 0, 0): quotient.one}, monomials, quotient)
    rref, pivots = _k_rref(rows, quotient.K)
    residual = _k_reduce_against_rref(target, rref, pivots, quotient.K)
    before = len(pivots)
    after = _k_rank(rows + [target], quotient.K)
    target_in_span = all(value.is_zero() for value in residual)
    return {
        "bound": bound,
        "monomial_count": len(monomials),
        "columns": len(target),
        "row_count": len(rows),
        "q_basis_multiplier_count": len(q_basis),
        "q_basis_multiplier_sha256": [_hash_k_values(multiplier) for multiplier in q_basis],
        "rank": before,
        "rank_with_target": after,
        "target_in_span": target_in_span,
        "rref_pivots": pivots,
        "input_matrix_sha256": _hash_k_matrix(rows),
        "rref_matrix_sha256": _hash_k_matrix(rref),
        "target_sha256": _hash_k_values(target),
        "target_residual_sha256": _hash_k_values(residual),
        "target_residual_zero": target_in_span,
        "generator_sha256": [_hash_multivariate_poly(generator) for generator in generators],
        "quotient_input": _quotient_input_metadata(quotient),
    }


def _a_pseudo_divrem(left: list[Any], right: list[Any], quotient: _QAlgebra):
    """Fraction-free pseudo-division in A[a], tracking no inverse in A."""
    left = _trim_a(left, quotient)
    right = _trim_a(right, quotient)
    if not right:
        raise ZeroDivisionError("zero polynomial in quotient Euclid")
    if not left or len(left) < len(right):
        return left, [quotient.one], []
    remainder = list(left)
    first_multiplier = [quotient.one]
    second_multiplier: list[Any] = []
    leading = right[-1]
    for _ in range(len(left) - len(right) + 1):
        if not remainder:
            break
        coefficient = remainder[-1]
        remainder = _a_scale(remainder, leading, quotient)
        first_multiplier = _a_scale(first_multiplier, leading, quotient)
        second_multiplier = _a_scale(second_multiplier, leading, quotient)
        degree = len(remainder) - len(right)
        for index, value in enumerate(right):
            remainder[degree + index] = quotient.sub(
                remainder[degree + index], quotient.mul(coefficient, value)
            )
        while len(second_multiplier) <= degree:
            second_multiplier.append(quotient.zero)
        second_multiplier[degree] = quotient.sub(
            second_multiplier[degree], coefficient
        )
        remainder = _trim_a(remainder, quotient)
        first_multiplier = _trim_a(first_multiplier, quotient)
        second_multiplier = _trim_a(second_multiplier, quotient)
    return remainder, first_multiplier, second_multiplier


def _a_gcdex(left: list[Any], right: list[Any], quotient: _QAlgebra):
    """Extended fraction-free Euclid; normalization is intentionally omitted."""
    r0, r1 = _trim_a(left, quotient), _trim_a(right, quotient)
    s0, s1 = [quotient.one], []
    t0, t1 = [], [quotient.one]
    steps = 0
    while r1:
        remainder, s, t = _a_pseudo_divrem(r0, r1, quotient)
        sr = _a_add(_a_mul(s, s0, quotient), _a_mul(t, s1, quotient), quotient)
        tr = _a_add(_a_mul(s, t0, quotient), _a_mul(t, t1, quotient), quotient)
        r0, r1 = r1, remainder
        s0, s1 = s1, sr
        t0, t1 = t1, tr
        steps += 1
    return r0, s0, t0, steps


def _k_det(matrix: list[list[Any]], field: _FactorField):
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    result = field.zero
    for column in range(size):
        minor = [
            [matrix[row][other] for other in range(size) if other != column]
            for row in range(1, size)
        ]
        term = field.mul(matrix[0][column], _k_det(minor, field))
        result = field.add(result, term if column % 2 == 0 else field.neg(term))
    return result


def _a_norm(value: Any, quotient: _QAlgebra):
    """Determinant of multiplication by value on the K-basis 1,q,q^2,q^3."""
    basis = [
        tuple(quotient.K.one if row == column else quotient.K.zero for row in range(4))
        for column in range(4)
    ]
    columns = [quotient.mul(value, vector) for vector in basis]
    matrix = [[columns[column][row] for column in range(4)] for row in range(4)]
    return _k_det(matrix, quotient.K)


def f40_quotient_euclid_replay(
    determinants: dict[str, Any], source_algebra: Algebra, matrix_inverse: bool
) -> dict[str, Any]:
    """Replay the exact f40 D134/D145 quotient-gcd leaf.

    The Euclidean multipliers are transient.  With the no-final-inverse
    implementation semantics, the returned nonzero constant and its 4-by-4
    multiplication norm are the certificate, so no inverse of that constant
    is materialized.  The switches below are neutral implementation controls;
    neither one imposes or inverts an equation in the theorem variables.
    """
    _factor, field, quotient = _factor_quotient("F40", matrix_inverse)
    d134, d134_metadata = _specialized_a_poly(
        determinants["D134"], source_algebra, "F40", field, quotient
    )
    d145, d145_metadata = _specialized_a_poly(
        determinants["D145"], source_algebra, "F40", field, quotient
    )
    # The current tracked bridge has already reduced the determinant in q
    # modulo Q6 before this sparse integerization.  The 3444/3944 counts are
    # retained only as unverified historical metadata; no representation
    # relation or equality with either count is asserted here.  Keep the exact
    # current denominator/content/term hash in the certificate; the
    # quotient-gcd identity below is the load-bearing F40 check.
    d145_representation = {
        "kind": "Q6-reduced Algebra.as_expr(D145), then cancel/primitive integerization",
        "authoritative": True,
        "term_count": d145_metadata.get("term_count"),
        "terms_sha256": d145_metadata.get("terms_sha256"),
        "denominator": d145_metadata.get("denominator"),
        "integer_denominator": d145_metadata.get("integer_denominator"),
        "rational_content": d145_metadata.get("rational_content"),
        "historical_reference_term_count": 3444,
        "historical_stale_D012_diagnostic_term_count": 3944,
        "historical_counts_status": "unverified historical metadata only",
        "historical_counts_used_as_authoritative_pin": False,
        "exact_expression_equality_to_historical_reference": "not_checked",
        "comparison_reason": (
            "the historical counts are recorded for lineage only; this verifier "
            "does not import or compare either historical representation"
        ),
        "independent_current_comparison": D145_CROSS_IMPLEMENTATION_COMPARISON,
    }
    gcd, u134, u145, steps = _a_gcdex(d134, d145, quotient)
    if len(gcd) != 1 or quotient.is_zero(gcd[0]):
        raise AssertionError(("F40 quotient gcd is not a nonzero constant", len(gcd)))
    relation = _a_sub(
        _a_add(_a_mul(u134, d134, quotient), _a_mul(u145, d145, quotient), quotient),
        gcd,
        quotient,
    )
    if relation:
        raise AssertionError("F40 unnormalised Bezout relation has a residual")
    if not matrix_inverse:
        raise RuntimeError(f"GLD103_F40_REQUIRES_{FACTOR_MATRIX_INVERSE_ENV}=1")
    norm = _a_norm(gcd[0], quotient)
    if norm.is_zero():
        raise AssertionError("F40 constant multiplication norm is zero")
    factor_poly = sp.Poly(_factor_expression("F40"), p, domain=QQ)
    h2_poly = sp.Poly(H2, p, domain=QQ)
    if factor_poly.primitive()[1] != factor_poly:
        raise AssertionError("F40 primitive normalization drift")
    if not factor_poly.is_irreducible:
        raise AssertionError("F40 irreducibility drift")
    if factor_poly.gcd(h2_poly).degree() != 0:
        raise AssertionError("F40 and H2 are not coprime")
    constant = gcd[0]
    c_q_degree = max(
        (index for index, coefficient in enumerate(constant) if not coefficient.is_zero()),
        default=-1,
    )
    if c_q_degree > 3:
        raise AssertionError(("F40 constant q-degree drift", c_q_degree))
    no_final_inverse, no_final_inverse_source = _implementation_flag(FACTOR_NO_FINAL_INVERSE_ENV)
    if not no_final_inverse:
        raise RuntimeError(f"GLD103_F40_REQUIRES_{FACTOR_NO_FINAL_INVERSE_ENV}=1")
    return {
        "factor": str(_factor_expression("F40")),
        "route": "exact quotient-Euclid gcd of D134,D145",
        "factor_field_matrix_inverse": int(bool(matrix_inverse)),
        "factor_no_final_inverse": int(no_final_inverse),
        "implementation_switch_sources": {
            "matrix_inverse": "caller-derived",
            "no_final_inverse": no_final_inverse_source,
        },
        "a_gcd_degree": 0,
        "a_degree_of_c": 0,
        "q_degree_of_c": c_q_degree,
        "euclidean_steps": steps,
        "relation_checked": True,
        "relation_residual_sha256": _hash_a_poly(relation),
        "c_sha256": _hash_k_values(constant),
        "u134_sha256": _hash_a_poly(u134),
        "u145_sha256": _hash_a_poly(u145),
        "unnormalized_constant_c": True,
        "norm_degree_p": int(norm.degree()),
        "norm_nonzero": True,
        "four_by_four_multiplication_norm": True,
        "factor_primitive_checked": True,
        "factor_irreducible_checked": True,
        "gcd_factor_H2_checked": True,
        "u134_terms": sum(not quotient.is_zero(value) for value in u134),
        "u145_terms": sum(not quotient.is_zero(value) for value in u145),
        "transient_multipliers_stored": False,
        "input_metadata": {
            "D134": d134_metadata,
            "D145": d145_metadata,
            "D145_representation_reconciliation": d145_representation,
            "quotient": _quotient_input_metadata(quotient),
        },
        "identity": "u134*D134 + u145*D145 = c; Norm_A/K(c) != 0",
    }


def _factor_quotient(name: str, matrix_inverse: bool = True):
    factor_poly = sp.Poly(_factor_expression(name), p, domain=QQ)
    content, primitive = factor_poly.primitive()
    if int(content) < 0:
        primitive = -primitive
        content = -content
    if int(content) != 1:
        raise AssertionError(f"{name} factor is not primitive")
    if not primitive.is_irreducible:
        raise AssertionError(f"{name} factor is not irreducible over QQ")
    coefficients = tuple(int(value) for value in primitive.all_coeffs())
    field = _FactorField(coefficients, matrix_inverse)
    q6_raw, _q6_meta = _integer_sparse_polynomial(q6_expression())
    quotient = _QAlgebra(field, q6_raw)
    return primitive, field, quotient


def _specialized_a_poly(value: Any, source_algebra: Algebra, factor_name: str, field: _FactorField, quotient: _QAlgebra):
    raw, metadata = _integer_sparse_polynomial(source_algebra.as_expr(value))
    denominator_poly = sp.Poly(sp.sympify(metadata["denominator"]), p, domain=QQ)
    factor_poly = sp.Poly(_factor_expression(factor_name), p, domain=QQ)
    if sp.gcd(denominator_poly, factor_poly).degree() != 0:
        raise AssertionError(("quotient denominator vanishes on factor", factor_name, metadata["denominator"]))
    return _raw_to_a_poly(raw, field, quotient), metadata


def _p_values_to_multivariate(p_values: list[BC], source_algebra: Algebra, factor_name: str, field: _FactorField, quotient: _QAlgebra):
    output = []
    metadata = []
    for p_index, value in enumerate(p_values):
        for (_b_degree, c_degree), _coefficient in value.terms.items():
            if c_degree:
                raise AssertionError("P row unexpectedly contains C")
        # Clear the denominator/content once for the complete P_i(B), then
        # map its integer support into the factor-field Q6 quotient.  Doing
        # this per B coefficient would rescale different powers of B by
        # unrelated nonzero factors and would not preserve the P_i ideal.
        expression = sp.expand(
            sum(
                source_algebra.as_expr(coefficient) * B**b_degree
                for (b_degree, _c_degree), coefficient in value.terms.items()
            )
        )
        raw, item_metadata = _integer_sparse_polynomial_in_variables(
            expression, (p, a, q, B)
        )
        item_metadata.update(
            {
                "P_index": p_index,
                "factor": factor_name,
                "normalization_scope": "whole P_i(B)",
                "source_expression_srepr_sha256": sha256_bytes(
                    sp.srepr(expression).encode()
                ),
            }
        )
        denominator_poly = sp.Poly(
            sp.sympify(item_metadata["denominator"]), p, domain=QQ
        )
        factor_poly = sp.Poly(_factor_expression(factor_name), p, domain=QQ)
        if sp.gcd(denominator_poly, factor_poly).degree() != 0:
            raise AssertionError(
                (
                    "whole-P_i quotient denominator vanishes on factor",
                    p_index,
                    factor_name,
                    item_metadata["denominator"],
                )
            )
        item_metadata["quotient_denominator_nonzero_on_factor"] = True
        metadata.append(item_metadata)
        polynomial: dict[tuple[int, int, int], Any] = {}
        for (p_degree, a_degree, q_degree, b_degree), coefficient in raw.items():
            q_coefficient = field.scale(field.power(p_degree), coefficient)
            q_value = quotient.from_raw_q({q_degree: q_coefficient})
            monomial = (a_degree, b_degree, 0)
            polynomial[monomial] = quotient.add(
                polynomial.get(monomial, quotient.zero), q_value
            )
        output.append(
            {
                monomial: value
                for monomial, value in polynomial.items()
                if not quotient.is_zero(value)
            }
        )
    return output, metadata


def _delta_specialization(factor_name: str, field: _FactorField, quotient: _QAlgebra):
    raw, metadata = _integer_sparse_polynomial(DELTA)
    factor_poly = sp.Poly(_factor_expression(factor_name), p, domain=QQ)
    denominator_poly = sp.Poly(sp.sympify(metadata["denominator"]), p, domain=QQ)
    if sp.gcd(denominator_poly, factor_poly).degree() != 0:
        raise AssertionError(("Delta denominator vanishes on factor", factor_name))
    a_poly = _raw_to_a_poly(raw, field, quotient)
    if len(a_poly) > 1:
        raise AssertionError("Delta acquired an a variable")
    return a_poly[0] if a_poly else quotient.zero, metadata


def local_fibre_ledger(
    determinants: dict[str, Any],
    p_values: list[BC],
    source_algebra: Algebra,
    selected: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Replay every non-(p=0,1) factor leaf with exact quotient arithmetic."""
    all_closures = (
        "C4",
        "R8",
        "p2_plus_1",
        "R4",
        "F4",
        "p2_minus_2p_plus_2",
        "F40",
    )
    requested = set(all_closures if selected is None else selected)
    if not requested.issubset(set(all_closures)) or not requested:
        raise AssertionError(("unknown/empty local-fibre selection", requested))
    for name in FIBRE_TRIPLES:
        if name not in determinants or source_algebra.is_zero(determinants[name]):
            raise AssertionError(f"missing/nonzero fibre determinant {name}")
    matrix_inverse, matrix_inverse_source = _implementation_flag(FACTOR_MATRIX_INVERSE_ENV)
    exact: dict[str, Any] = {}

    if "C4" in requested:
        # C4 is closed by an exact pair quotient-Euclid replay, not by a rank
        # label or a precomputed unit claim.
        factor, field, quotient = _factor_quotient("C4", matrix_inverse)
        c4_d134, c4_d134_meta = _specialized_a_poly(
            determinants["D134"], source_algebra, "C4", field, quotient
        )
        c4_d012, c4_d012_meta = _specialized_a_poly(
            determinants["D012"], source_algebra, "C4", field, quotient
        )
        c4_gcd, c4_u134, c4_u012, c4_steps = _a_gcdex(c4_d134, c4_d012, quotient)
        if len(c4_gcd) != 1 or quotient.is_zero(c4_gcd[0]):
            raise AssertionError(("C4 quotient gcd is not a nonzero constant", len(c4_gcd)))
        c4_relation = _a_sub(
            _a_add(
                _a_mul(c4_u134, c4_d134, quotient),
                _a_mul(c4_u012, c4_d012, quotient),
                quotient,
            ),
            c4_gcd,
            quotient,
        )
        if c4_relation:
            raise AssertionError("C4 unnormalised Bezout relation has a residual")
        if not matrix_inverse:
            raise RuntimeError("GLD103_C4_REQUIRES_FACTOR_MATRIX_INVERSE=1")
        c4_norm = _a_norm(c4_gcd[0], quotient)
        if c4_norm.is_zero():
            raise AssertionError("C4 constant multiplication norm is zero")
        c4_constant = c4_gcd[0]
        c4_q_degree = max(
            (index for index, coefficient in enumerate(c4_constant) if not coefficient.is_zero()),
            default=-1,
        )
        if c4_q_degree > 3:
            raise AssertionError(("C4 constant q-degree drift", c4_q_degree))
        exact["C4"] = {
            "factor": str(factor.as_expr()),
            "ideal": "<Q6,D134,D012>",
            "method": "exact quotient-Euclid pair gcd in A[a]",
            "generators": ["D134", "D012"],
            "unit": not c4_relation and not c4_norm.is_zero(),
            "a_gcd_degree": 0,
            "a_degree_of_c": 0,
            "q_degree_of_c": c4_q_degree,
            "euclidean_steps": c4_steps,
            "relation_checked": True,
            "relation_residual_sha256": _hash_a_poly(c4_relation),
            "c_sha256": _hash_k_values(c4_constant),
            "u134_sha256": _hash_a_poly(c4_u134),
            "u012_sha256": _hash_a_poly(c4_u012),
            "unnormalized_constant_c": True,
            "norm_degree_p": int(c4_norm.degree()),
            "norm_nonzero": True,
            "four_by_four_multiplication_norm": True,
            "input_metadata": {"D134": c4_d134_meta, "D012": c4_d012_meta},
            "quotient_input": _quotient_input_metadata(quotient),
        }

    def k_fibre(name: str, bound: int, generators: tuple[str, ...], expected_rank: int):
        factor, local_field, local_quotient = _factor_quotient(name, matrix_inverse)
        local_generators = []
        input_metadata = {}
        for generator_name in generators:
            local_value, item_metadata = _specialized_a_poly(
                determinants[generator_name], source_algebra, name, local_field, local_quotient
            )
            local_generators.append(local_value)
            input_metadata[generator_name] = item_metadata
        matrix = _a_macaulay_membership(local_generators, bound, local_quotient)
        if not matrix["target_in_span"] or matrix["rank"] != expected_rank or matrix["columns"] != expected_rank:
            raise AssertionError((name, "K-linear Macaulay rank drift", matrix, expected_rank))
        return {
            "factor": str(factor.as_expr()),
            "ideal": "<Q6," + ",".join(generators) + ">",
            "method": "exact K-linear Macaulay membership in A[a]",
            "generators": list(generators),
            "matrix": matrix,
            "unit": bool(matrix["target_residual_zero"]),
            "input_metadata": input_metadata,
        }

    if "R8" in requested:
        exact["R8"] = k_fibre("R8", 7, ("D134", "D012", "D013"), 32)
    if "p2_plus_1" in requested:
        exact["p2_plus_1"] = k_fibre("p2_plus_1", 5, ("D134", "D012", "D145"), 24)
    if "R4" in requested:
        exact["R4"] = k_fibre("R4", 5, ("D134", "D012", "D145"), 24)

    def affine_fibre(name: str, expected_rank: int):
        factor, local_field, local_quotient = _factor_quotient(name, matrix_inverse)
        local_p, input_metadata = _p_values_to_multivariate(
            p_values, source_algebra, name, local_field, local_quotient
        )
        delta, delta_metadata = _delta_specialization(name, local_field, local_quotient)
        localizer = {
            (0, 1, 1): delta,
            (0, 0, 0): local_quotient.neg(local_quotient.one),
        }
        matrix = _multivariate_macaulay([*local_p, localizer], 3, local_quotient)
        if not matrix["target_in_span"] or matrix["rank"] != expected_rank or matrix["columns"] != 80:
            raise AssertionError((name, "sparse total-degree Macaulay rank drift", matrix, expected_rank))
        return {
            "factor": str(factor.as_expr()),
            "ideal": "<P0,P1,P2,P3,P4,P5,z*B*Delta-1>",
            "method": "exact sparse total-degree Macaulay over A[a,B,z]",
            "bound": 3,
            "generators": ["P0", "P1", "P2", "P3", "P4", "P5", "z*B*Delta-1"],
            "matrix": matrix,
            "unit": bool(matrix["target_residual_zero"]),
            "input_metadata": {
                "P": input_metadata,
                "Delta": delta_metadata,
                "localizer": {
                    "monomials": [[0, 0, 0], [0, 1, 1]],
                    "delta_sha256": _hash_k_values((delta,)),
                    "polynomial_sha256": _hash_multivariate_poly(localizer),
                    "constant_term_checked": True,
                    "zBDelta_term_checked": True,
                },
            },
        }

    if "F4" in requested:
        exact["F4"] = affine_fibre("F4", 68)
    if "p2_minus_2p_plus_2" in requested:
        exact["p2_minus_2p_plus_2"] = affine_fibre("p2_minus_2p_plus_2", 66)
    if "F40" in requested:
        exact["F40"] = f40_quotient_euclid_replay(determinants, source_algebra, matrix_inverse)
    return {
        "status": (
            "verified_exact_local_fibre_closures"
            if selected is None
            else "verified_exact_selected_local_fibre_closures"
        ),
        "coefficient_ring": "characteristic-zero exact quotient A[a,B,z]",
        "localizer": "z*B*Delta-1",
        "closures": exact,
        "requested_closures": sorted(requested),
        "p0_p1": {
            "method": "call tracked GLD102 check()",
            "tracked_source": "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py",
            "scope": "arbitrary a, p in {0,1}, D(Delta); rank<=6 implies B=C=0",
            "B_nonzero_contradiction": True,
        },
        "outside_declared_open": {
            "P": "P divides Delta and is therefore outside D(B*H2*Delta)",
            "H2": "H2 is explicitly inverted by the Q6 q-leading coefficient and is outside the declared open",
        },
        "matrix_inverse_mode": matrix_inverse,
        "implementation_switch_sources": {"matrix_inverse": matrix_inverse_source},
    }


def run_gld102_check() -> dict[str, Any]:
    """Invoke the committed GLD102 checker for the p=0,1 leaves."""
    module = load_module(GLD102, "gld102_for_gld103_primary")
    result = module.check()
    if result.get("claim_id") != "GLD102":
        raise AssertionError("tracked GLD102 check returned an unexpected claim")
    if result.get("status") != "proved_exact_scoped_p01_nonzero_offset_exclusion":
        raise AssertionError(("tracked GLD102 status drift", result.get("status")))
    if result.get("global_conjecture") != "UNRESOLVED":
        raise AssertionError("GLD102 global status drift")
    if result.get("rank_to_selector_direction_only") is not True:
        raise AssertionError("GLD102 dependency is not the required rank-to-selector one-way bridge")
    if not result.get("source_lf_sha256"):
        raise AssertionError("GLD102 dependency is not pinned to its tracked source")
    return {
        "called_tracked_check": True,
        "claim_id": result.get("claim_id"),
        "status": result.get("status"),
        "global_conjecture": result.get("global_conjecture"),
        "elapsed_seconds": result.get("elapsed_seconds"),
    }


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, RuntimeError, ValueError, ZeroDivisionError, sp.PolynomialError) as exc:
        print(f"GLD103_PRIMARY_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(2)
