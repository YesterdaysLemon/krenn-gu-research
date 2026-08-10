#!/usr/bin/env python3
"""Verify the exact certificate package for the one-partial P5 boundary."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu import p5_support_system as GENERATOR


ROOT = Path(__file__).resolve().parent
BOUNDARY = (
    REPO_ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "one_partial_boundary"
)
MANIFEST = BOUNDARY / "manifest.json"
RING = re.compile(
    r"^ring r=0,\((?P<variables>[A-Za-z0-9_,]+)\),dp;$",
    re.MULTILINE,
)
IDEAL = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified_path(relative: str, expected_hash: str) -> Path:
    path = (BOUNDARY / relative).resolve()
    if BOUNDARY.resolve() not in path.parents:
        raise AssertionError(f"artifact escapes package: {relative}")
    if not path.is_file():
        raise AssertionError(f"missing artifact: {relative}")
    if sha256(path) != expected_hash:
        raise AssertionError(f"hash mismatch: {relative}")
    return path


def split_top_level_product(expression: str) -> list[str]:
    factors = []
    depth = 0
    start = 0
    for index, character in enumerate(expression):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth < 0:
                raise AssertionError("unbalanced saturation parentheses")
        elif character == "*" and depth == 0:
            factors.append(expression[start:index])
            start = index + 1
    if depth:
        raise AssertionError("unbalanced saturation parentheses")
    factors.append(expression[start:])
    if any(not factor for factor in factors):
        raise AssertionError("empty saturation factor")
    return factors


def expected_split_singular(source_text: str) -> str:
    ring = RING.search(source_text)
    ideal = IDEAL.search(source_text)
    if ring is None or ideal is None:
        raise AssertionError("unrecognized packaged Singular source")
    variables = ring.group("variables").split(",")
    equations = ideal.group("equations").split(",\n")
    parameters = variables[:-1]
    rabinowitsch = variables[-1]
    saturation = equations[-1]
    prefix = f"{rabinowitsch}*("
    if not saturation.startswith(prefix) or not saturation.endswith(")-1"):
        raise AssertionError("unrecognized Rabinowitsch equation")
    factors = split_top_level_product(
        saturation[len(prefix) : -3]
    )
    if factors[: len(parameters)] != parameters:
        raise AssertionError("saturation omits a Laurent parameter")
    if len(factors) != len(parameters) + 3:
        raise AssertionError("saturation does not contain three pure factors")

    safe_parameters = [
        f"v{index:02d}" for index in range(len(parameters))
    ]
    safe_name = dict(zip(parameters, safe_parameters, strict=True))

    def rename(expression: str) -> str:
        unknown = set(IDENTIFIER.findall(expression)).difference(
            safe_name
        )
        if unknown:
            raise AssertionError(
                f"unknown identifiers in converted expression: {unknown}"
            )
        return IDENTIFIER.sub(
            lambda match: safe_name[match.group(0)], expression
        )

    safe_mixed = [rename(equation) for equation in equations[:-1]]
    safe_factors = [rename(factor) for factor in factors]
    inverse_variables = [
        f"w{index:02d}" for index in range(len(safe_factors))
    ]
    inverse_equations = [
        f"{inverse}*({factor})-1"
        for inverse, factor in zip(
            inverse_variables, safe_factors, strict=True
        )
    ]
    converted_variables = safe_parameters + inverse_variables
    converted_equations = inverse_equations + safe_mixed
    equation_text = ",\n".join(converted_equations)
    return "\n".join(
        [
            "// exact split-saturation conversion",
            f"ring r=0,({','.join(converted_variables)}),dp;",
            "option(redSB);",
            f"ideal I={equation_text};",
            "ideal G=slimgb(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_summary = {
        "schema": 1,
        "status": "EXACT_FINITE_BOUNDARY_THEOREM",
        "scope": (
            "exactly-one-partial exact-three-coordinate P5 boundary"
        ),
        "global_conjecture_resolved": False,
        "support_orbits": 5676,
        "locally_invalid_support_orbits": 224,
        "locally_valid_support_orbits": 5452,
        "pair_quota_excluded_support_orbits": 5133,
        "pair_quota_viable_support_orbits": 319,
        "pair_quota_viable_signature_tuples": 6575,
        "certified_support_orbits": 319,
        "singular_direct_unit_ideals": 307,
        "singular_split_unit_ideals": 12,
        "singular_certified_union": 319,
        "mixed_equation_histogram": {
            "216": 20,
            "218": 15,
            "219": 6,
            "220": 21,
            "222": 47,
            "223": 83,
            "224": 127,
        },
    }
    for key, value in expected_summary.items():
        if manifest.get(key) != value:
            raise AssertionError(
                f"manifest {key} changed: {manifest.get(key)!r}"
            )

    audit_path = verified_path(
        manifest["audit"], manifest["audit_sha256"]
    )
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit_summary = (
        audit.get("verified"),
        audit.get("catalogue_pair_signatures"),
        audit.get("support_orbits"),
        audit.get("locally_invalid_support_orbits"),
        audit.get("locally_valid_support_orbits"),
        audit.get("pair_quota_excluded_support_orbits"),
        audit.get("pair_quota_viable_support_orbits"),
        audit.get("pair_quota_viable_signature_tuples"),
        audit.get("c10", {}).get("support_orbits"),
        audit.get("c10", {}).get("locally_invalid_support_orbits"),
        audit.get("c10", {}).get(
            "pair_quota_viable_support_orbits"
        ),
        audit.get("c4c6", {}).get("support_orbits"),
        audit.get("c4c6", {}).get(
            "locally_invalid_support_orbits"
        ),
        audit.get("c4c6", {}).get(
            "pair_quota_viable_support_orbits"
        ),
    )
    if audit_summary != (
        True,
        6495,
        5676,
        224,
        5452,
        5133,
        319,
        6575,
        3888,
        144,
        236,
        1788,
        80,
        83,
    ):
        raise AssertionError(f"packaged audit summary changed: {audit_summary}")

    expected_cases = {
        (case["shape"], case["orbit_index"]): case
        for case in audit["cases"]
    }
    if len(expected_cases) != 319:
        raise AssertionError("packaged audit case set is not exhaustive")

    seen = set()
    direct_units = 0
    split_units = 0
    certified_union = 0
    mixed_histogram: Counter[int] = Counter()
    for record in manifest["cases"]:
        key = (record["shape"], record["support_orbit"])
        if key in seen or key not in expected_cases:
            raise AssertionError(f"duplicate or unexpected case: {key}")
        seen.add(key)
        expected_case = expected_cases[key]
        if (
            record["supports"] != expected_case["supports"]
            or record["orbit_size"] != expected_case["orbit_size"]
            or record["viable_signature_tuples"]
            != expected_case["viable_signature_tuples"]
            or record["witness_signature_indices"]
            != expected_case["witness_signature_indices"]
        ):
            raise AssertionError(f"audit/manifest mismatch: {key}")

        source = verified_path(
            record["source"], record["source_sha256"]
        )
        source_text = source.read_text(encoding="utf-8")
        supports = tuple(
            tuple(row) for row in expected_case["supports"]
        )
        signature_indices = tuple(
            expected_case["witness_signature_indices"]
        )
        regenerated, metadata = GENERATOR.generate(
            supports, signature_indices
        )
        if source_text != regenerated:
            raise AssertionError(
                f"semantic source regeneration mismatch: {key}"
            )
        expected_metadata = {
            "nonzero_entries": 44,
            "gauge_free_variables": 25,
            "laurent_parameters": 25,
            "mixed_equations": record["mixed_equations"],
            "pure_coefficients": 3,
        }
        if metadata != expected_metadata:
            raise AssertionError(f"system metadata mismatch: {key}")
        mixed_histogram[metadata["mixed_equations"]] += 1

        direct = record["singular_direct"]
        if direct["status"] == "UNIT_IDEAL":
            direct_output = verified_path(
                direct["output"], direct["output_sha256"]
            )
            if (
                direct_output.read_text(encoding="utf-8").strip()
                != "UNIT_IDEAL"
            ):
                raise AssertionError(
                    f"bad direct Singular certificate: {key}"
                )
            direct_units += 1

        split = record["singular_split"]
        if split["status"] == "UNIT_IDEAL":
            split_source = verified_path(
                split["source"], split["source_sha256"]
            )
            split_output = verified_path(
                split["output"], split["output_sha256"]
            )
            if (
                split_source.read_text(encoding="utf-8")
                != expected_split_singular(source_text)
            ):
                raise AssertionError(
                    f"split-saturation source mismatch: {key}"
                )
            if (
                split_output.read_text(encoding="utf-8").strip()
                != "UNIT_IDEAL"
            ):
                raise AssertionError(
                    f"bad split Singular certificate: {key}"
                )
            split_units += 1

        if (
            direct["status"] == "UNIT_IDEAL"
            or split["status"] == "UNIT_IDEAL"
        ):
            certified_union += 1
        else:
            raise AssertionError(f"case lacks a unit ideal: {key}")

    if seen != set(expected_cases):
        raise AssertionError("manifest does not cover the audited case set")
    observed_histogram = {
        str(key): value for key, value in sorted(mixed_histogram.items())
    }
    if observed_histogram != manifest["mixed_equation_histogram"]:
        raise AssertionError("mixed-equation histogram changed")
    if direct_units != manifest["singular_direct_unit_ideals"]:
        raise AssertionError("direct Singular unit count changed")
    if split_units != manifest["singular_split_unit_ideals"]:
        raise AssertionError("split Singular unit count changed")
    if certified_union != manifest["singular_certified_union"]:
        raise AssertionError("Singular certified union changed")

    print(
        json.dumps(
            {
                "verified": True,
                "scope": manifest["scope"],
                "support_orbits": manifest["support_orbits"],
                "locally_invalid_support_orbits": manifest[
                    "locally_invalid_support_orbits"
                ],
                "pair_quota_excluded_support_orbits": manifest[
                    "pair_quota_excluded_support_orbits"
                ],
                "certified_support_orbits": len(seen),
                "singular_direct_unit_ideals": direct_units,
                "singular_split_unit_ideals": split_units,
                "singular_certified_union": certified_union,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
