#!/usr/bin/env python3
"""Verify the exact certificate package for the two-partial P5 boundary."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])
expose_claim_package(REPO_ROOT, "claims/p5/boundaries")
expose_claim_package(REPO_ROOT, "claims/p5/frontier")

import audit_p5_exact_two_partial_boundary as AUDIT
from krenn_gu import p5_exact_two_support_system as GENERATOR
import verify_p5_one_partial_boundary_obstruction as ONE_PARTIAL
from krenn_gu import p5_pair_catalogue as COVERAGE


ROOT = Path(__file__).resolve().parent
BOUNDARY = (
    REPO_ROOT / 'research_snapshots/2026-07-27-p5-coordinate-cegar/two_partial_boundary'
)
MANIFEST = BOUNDARY / "manifest.json"


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


def canonical(
    shape: str,
    supports: list[list[int]] | tuple[tuple[int, ...], ...],
    actions: dict[str, tuple],
) -> int:
    packed = AUDIT.pack(
        tuple(mask for row in supports for mask in row)
    )
    return min(
        AUDIT.transform(packed, positions, masks)
        for positions, masks in actions[shape]
    )


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_summary = {
        "schema": 1,
        "status": "EXACT_FINITE_BOUNDARY_THEOREM",
        "scope": (
            "exactly-two-partial exact-three-coordinate P5 boundary"
        ),
        "global_conjecture_resolved": False,
        "labelled_supports": 6_298_560,
        "support_orbits": 76_098,
        "locally_invalid_support_orbits": 11_614,
        "locally_valid_support_orbits": 64_484,
        "pair_quota_excluded_support_orbits": 59_911,
        "pair_quota_viable_support_orbits": 4_573,
        "pair_quota_viable_signature_tuples": 50_109,
        "support_semantic_excluded_support_orbits": 1_265,
        "support_semantic_viable_support_orbits": 3_308,
        "certified_support_orbits": 3_308,
        "singular_certified_union": 3_308,
    }
    for key, value in expected_summary.items():
        if manifest.get(key) != value:
            raise AssertionError(
                f"manifest {key} changed: {manifest.get(key)!r}"
            )

    expected_shape_summaries = {
        "c10": (
            52_758,
            7_884,
            44_874,
            41_655,
            3_219,
            35_165,
            2_205,
        ),
        "c4c6": (
            23_340,
            3_730,
            19_610,
            18_256,
            1_354,
            14_944,
            1_103,
        ),
    }
    audits = {}
    actions = {}
    audit_cases = {}
    for shape, expected in expected_shape_summaries.items():
        audit_record = manifest["audits"][shape]
        audit_path = verified_path(
            audit_record["path"], audit_record["sha256"]
        )
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        observed = (
            audit.get("support_orbits"),
            audit.get("locally_invalid_support_orbits"),
            audit.get("locally_valid_support_orbits"),
            audit.get("pair_quota_excluded_support_orbits"),
            audit.get("pair_quota_viable_support_orbits"),
            audit.get("pair_quota_viable_signature_tuples"),
            audit.get("support_semantic_viable_support_orbits"),
        )
        if audit.get("verified") is not True or observed != expected:
            raise AssertionError(
                f"packaged {shape} audit changed: {observed}"
            )
        audits[shape] = audit
        actions[shape] = AUDIT.transformed_actions(shape)
        for case in audit["cases"]:
            key = (shape, case["orbit_index"])
            if key in audit_cases:
                raise AssertionError(f"duplicate audit case: {key}")
            audit_cases[key] = case
    if len(audit_cases) != 3_308:
        raise AssertionError("packaged audit case set is not exhaustive")

    catalogue = COVERAGE.finite_field_local_signatures()
    seen = set()
    canonical_seen = set()
    direct_units = 0
    split_units = 0
    certified_union = 0
    mixed_histogram: Counter[int] = Counter()
    for record in manifest["cases"]:
        key = (record["shape"], record["support_orbit"])
        if key in seen or key not in audit_cases:
            raise AssertionError(f"duplicate or unexpected case: {key}")
        seen.add(key)
        expected_case = audit_cases[key]
        shape = record["shape"]
        support_key = canonical(shape, record["supports"], actions)
        expected_support_key = canonical(
            shape, expected_case["supports"], actions
        )
        canonical_key = (shape, support_key)
        if (
            support_key != expected_support_key
            or canonical_key in canonical_seen
        ):
            raise AssertionError(f"support-orbit mismatch: {key}")
        canonical_seen.add(canonical_key)
        if (
            record["orbit_size"] != expected_case["orbit_size"]
            or record["viable_signature_tuples"]
            != expected_case["viable_signature_tuples"]
        ):
            raise AssertionError(f"audit/manifest mismatch: {key}")

        supports = tuple(tuple(row) for row in record["supports"])
        indices = tuple(record["witness_signature_indices"])
        if len(indices) != 5:
            raise AssertionError(f"bad signature witness: {key}")
        signatures = tuple(catalogue[index] for index in indices)
        if tuple(signature[0] for signature in signatures) != supports:
            raise AssertionError(f"signature/support mismatch: {key}")
        if not all(
            sum(
                bool(
                    signatures[mode][1][pair_index]
                    & (1 << colour)
                )
                for mode in AUDIT.MODES
            )
            >= 2
            for pair_index in range(10)
            for colour in AUDIT.COLOURS
        ):
            raise AssertionError(f"signature witness misses a quota: {key}")

        source = verified_path(
            record["source"], record["source_sha256"]
        )
        source_text = source.read_text(encoding="utf-8")
        regenerated, metadata = GENERATOR.generate(supports, indices)
        if source_text != regenerated:
            raise AssertionError(
                f"semantic source regeneration mismatch: {key}"
            )
        expected_metadata = {
            "nonzero_entries": 43,
            "gauge_free_variables": 24,
            "laurent_parameters": 24,
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
                != ONE_PARTIAL.expected_split_singular(source_text)
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

    if seen != set(audit_cases):
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
                "support_semantic_excluded_support_orbits": manifest[
                    "support_semantic_excluded_support_orbits"
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
