#!/usr/bin/env python3
"""Verify the exact certificate package for the entire all-full P5 boundary."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import generate_p5_all_full_signature_system as GENERATOR


ROOT = Path(__file__).resolve().parent
BOUNDARY = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "all_full_boundary"
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


def expected_msolve_input(source_text: str) -> str:
    ring = RING.search(source_text)
    ideal = IDEAL.search(source_text)
    if ring is None or ideal is None:
        raise AssertionError("unrecognized packaged Singular source")
    variables = ring.group("variables").split(",")
    equations = ideal.group("equations").split(",\n")
    if not equations:
        raise AssertionError("empty packaged Singular ideal")
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
    return (
        ",".join(converted_variables)
        + "\n0\n"
        + ",\n".join(converted_equations)
        + "\n"
    )


def expected_split_singular(source_text: str) -> str:
    converted = expected_msolve_input(source_text).splitlines()
    if len(converted) < 3 or converted[1] != "0":
        raise AssertionError("bad internal split-saturation conversion")
    variables = converted[0]
    equations = "\n".join(converted[2:])
    return "\n".join(
        [
            "// exact split-saturation conversion",
            f"ring r=0,({variables}),dp;",
            "option(redSB);",
            f"ideal I={equations};",
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
        "global_conjecture_resolved": False,
        "support_orbits": 226,
        "pair_quota_excluded_support_orbits": 213,
        "proper_support_orbits_covered_by_prior_theorem": 3,
        "nonproper_viable_support_orbits": 10,
        "nonproper_viable_signature_tuples": 198,
        "certified_cases": 198,
        "singular_direct_unit_ideals": 186,
        "singular_split_unit_ideals": 15,
        "singular_certified_union": 198,
        "msolve_unit_ideals": 111,
        "mixed_equation_histogram": {
            "216": 9,
            "220": 18,
            "230": 45,
            "240": 126,
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
        audit.get("pair_quota_excluded_support_orbits"),
        audit.get("proper_viable_support_orbits"),
        audit.get("nonproper_viable_support_orbits"),
        audit.get("nonproper_viable_signature_tuples"),
    )
    if audit_summary != (True, 6495, 226, 213, 3, 10, 198):
        raise AssertionError(f"packaged audit summary changed: {audit_summary}")
    expected_cases = {
        (
            case["shape"],
            case["orbit_index"],
            tuple(case["signature_indices"]),
        ): case
        for case in audit["cases"]
    }
    if len(expected_cases) != 198:
        raise AssertionError("packaged audit case set is not exhaustive")

    seen = set()
    singular_direct_units = 0
    singular_split_units = 0
    singular_union = 0
    msolve_units = 0
    for record in manifest["cases"]:
        key = (
            record["shape"],
            record["support_orbit"],
            tuple(record["signature_indices"]),
        )
        if key in seen or key not in expected_cases:
            raise AssertionError(f"duplicate or unexpected case: {key}")
        seen.add(key)
        expected_case = expected_cases[key]
        if record["supports"] != expected_case["supports"]:
            raise AssertionError(f"support mismatch: {key}")

        source = verified_path(
            record["source"], record["source_sha256"]
        )
        source_text = source.read_text(encoding="utf-8")
        regenerated, metadata = GENERATOR.generate(key[2])
        if source_text != regenerated:
            raise AssertionError(
                f"semantic source regeneration mismatch: {key}"
            )
        if metadata["mixed_equations"] != record["mixed_equations"]:
            raise AssertionError(f"mixed-equation count mismatch: {key}")

        singular_direct = record["singular_direct"]
        if singular_direct["status"] == "UNIT_IDEAL":
            output = verified_path(
                singular_direct["output"],
                singular_direct["output_sha256"],
            )
            if output.read_text(encoding="utf-8").strip() != "UNIT_IDEAL":
                raise AssertionError(
                    f"bad direct Singular certificate: {key}"
                )
            singular_direct_units += 1

        singular_split = record["singular_split"]
        if singular_split["status"] == "UNIT_IDEAL":
            split_source = verified_path(
                singular_split["source"],
                singular_split["source_sha256"],
            )
            split_output = verified_path(
                singular_split["output"],
                singular_split["output_sha256"],
            )
            if split_source.read_text(
                encoding="utf-8"
            ) != expected_split_singular(source_text):
                raise AssertionError(
                    f"split-saturation Singular mismatch: {key}"
                )
            if split_output.read_text(
                encoding="utf-8"
            ).strip() != "UNIT_IDEAL":
                raise AssertionError(
                    f"bad split Singular certificate: {key}"
                )
            singular_split_units += 1
        if (
            singular_direct["status"] == "UNIT_IDEAL"
            or singular_split["status"] == "UNIT_IDEAL"
        ):
            singular_union += 1

        msolve = record["msolve"]
        if msolve["status"] == "UNIT_IDEAL":
            msolve_input = verified_path(
                msolve["input"], msolve["input_sha256"]
            )
            msolve_output = verified_path(
                msolve["output"], msolve["output_sha256"]
            )
            if msolve_input.read_text(
                encoding="utf-8"
            ) != expected_msolve_input(source_text):
                raise AssertionError(
                    f"msolve split-saturation conversion mismatch: {key}"
                )
            if msolve_output.read_text(
                encoding="utf-8"
            ).strip() != "[-1]:":
                raise AssertionError(f"bad msolve certificate: {key}")
            msolve_units += 1
        if (
            singular_direct["status"] != "UNIT_IDEAL"
            and singular_split["status"] != "UNIT_IDEAL"
            and msolve["status"] != "UNIT_IDEAL"
        ):
            raise AssertionError(f"case lacks a unit-ideal certificate: {key}")

    if seen != set(expected_cases):
        raise AssertionError("manifest does not cover the audited case set")
    if (
        singular_direct_units
        != manifest["singular_direct_unit_ideals"]
    ):
        raise AssertionError("direct Singular unit count changed")
    if singular_split_units != manifest["singular_split_unit_ideals"]:
        raise AssertionError("split Singular unit count changed")
    if singular_union != manifest["singular_certified_union"]:
        raise AssertionError("Singular certified union changed")
    if msolve_units != manifest["msolve_unit_ideals"]:
        raise AssertionError("msolve unit count changed")
    print(
        json.dumps(
            {
                "verified": True,
                "scope": manifest["scope"],
                "support_orbits": 226,
                "pair_quota_excluded_support_orbits": 213,
                "proper_support_orbits_from_prior_theorem": 3,
                "nonproper_signature_cases": len(seen),
                "singular_direct_unit_ideals": singular_direct_units,
                "singular_split_unit_ideals": singular_split_units,
                "singular_certified_union": singular_union,
                "msolve_unit_ideals": msolve_units,
                "certified_union": len(seen),
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
