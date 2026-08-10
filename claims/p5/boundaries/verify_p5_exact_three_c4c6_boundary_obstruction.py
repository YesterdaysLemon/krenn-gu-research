"""Audit the packaged exact-three-partial C4+C6 P5 obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])
expose_claim_package(REPO_ROOT, "claims/p5/frontier")

import audit_p5_exact_three_partial_boundary as AUDIT
import audit_p5_exact_two_partial_boundary as TWO
from krenn_gu import p5_exact_three_support_system as GENERATOR
from krenn_gu import p5_pair_catalogue as COVERAGE


ROOT = Path(__file__).resolve().parent
PACKAGE = (
    REPO_ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c4c6_boundary"
)
EXPECTED_MANIFEST_SHA256 = (
    "c4d707b9720c435a77eaeb5ec6cf6f2541c5478371fb43f12f10bf692df5a139"
)
EXPECTED_AUDIT_SHA256 = (
    "d0f006172e935ed5dbb44ab6aef6c630c2855eafcdd6badfd55f751fe5488d78"
)
EXPECTED = {
    "labelled_supports": 25_194_240,
    "locally_valid_support_orbits": 119_966,
    "pair_quota_viable_support_orbits": 10_216,
    "pair_quota_viable_signature_tuples": 58_664,
    "support_semantic_viable_support_orbits": 5_993,
    "singular_direct_unit_ideals": 5_993,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def packed_support(rows: list[list[int]]) -> int:
    return TWO.pack([mask for row in rows for mask in row])


def singular_command(explicit: str | None) -> list[str]:
    if explicit:
        return shlex.split(explicit)
    if shutil.which("Singular"):
        return ["Singular", "-q"]
    if shutil.which("wsl.exe"):
        return ["wsl.exe", "--exec", "Singular", "-q"]
    raise RuntimeError(
        "Singular was not found; pass --singular-command explicitly"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rerun-singular",
        action="store_true",
        help="Freshly rerun selected exact CAS cases (slow for all 5,993).",
    )
    parser.add_argument("--singular-command")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()
    if args.start < 0 or args.step < 1:
        raise ValueError("start must be nonnegative and step must be positive")

    manifest_path = PACKAGE / "manifest.json"
    if (
        sha256_bytes(manifest_path.read_bytes())
        != EXPECTED_MANIFEST_SHA256
    ):
        raise AssertionError("packaged manifest hash changed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "EXACT_FINITE_BOUNDARY_THEOREM"
        or manifest.get("shape") != "c4c6"
        or manifest.get("global_conjecture_resolved") is not False
    ):
        raise AssertionError("manifest status changed")
    for key, value in EXPECTED.items():
        if manifest.get(key) != value:
            raise AssertionError(f"manifest count changed: {key}")

    audit_path = PACKAGE / manifest["audit"]["path"]
    audit_hash = sha256_bytes(audit_path.read_bytes())
    if (
        audit_hash != EXPECTED_AUDIT_SHA256
        or audit_hash != manifest["audit"]["sha256"]
    ):
        raise AssertionError("packaged independent audit hash changed")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if (
        audit.get("verified") is not True
        or audit.get("catalogue_exact_match") is not True
        or audit.get("support_semantic_viable_support_orbits") != 5_993
    ):
        raise AssertionError("independent audit is incomplete")

    actions = TWO.transformed_actions("c4c6")
    audit_by_key = {}
    for case in audit["cases"]:
        key = packed_support(case["supports"])
        if AUDIT.canonical_support(key, actions) != key:
            raise AssertionError("audit support is not canonical")
        if key in audit_by_key:
            raise AssertionError("duplicate audit support")
        audit_by_key[key] = case

    catalogue = COVERAGE.finite_field_local_signatures()
    seen = set()
    source_bytes = 0
    mixed_histogram: Counter[int] = Counter()
    generated_programs: list[tuple[int, str]] = []
    output_hash = sha256_bytes(b"UNIT_IDEAL\n")
    for position, record in enumerate(manifest["cases"]):
        key = record["canonical_support"]
        if key in seen or key not in audit_by_key:
            raise AssertionError("duplicate or unaudited algebra case")
        seen.add(key)
        audit_case = audit_by_key[key]
        if record["audit_orbit_index"] != audit_case["audit_orbit_index"]:
            raise AssertionError("audit/algebra orbit mapping changed")

        supports = tuple(tuple(row) for row in record["solver_supports"])
        packed = packed_support(record["solver_supports"])
        if AUDIT.canonical_support(packed, actions) != key:
            raise AssertionError("solver support changed orbit")
        indices = tuple(record["signature_indices"])
        if len(indices) != 5:
            raise AssertionError("bad signature witness")
        signatures = tuple(catalogue[index] for index in indices)
        if tuple(signature[0] for signature in signatures) != supports:
            raise AssertionError("signature/support mismatch")
        if not all(
            sum(
                bool(signatures[mode][1][pair] & (1 << colour))
                for mode in range(5)
            )
            >= 2
            for pair in range(10)
            for colour in range(3)
        ):
            raise AssertionError("signature witness misses a pair quota")

        program, metadata = GENERATOR.generate(supports, indices)
        data = program.encode("utf-8")
        if (
            sha256_bytes(data) != record["source_sha256"]
            or len(data) != record["source_bytes"]
            or metadata["nonzero_entries"] != 42
            or metadata["gauge_free_variables"] != 23
            or metadata["laurent_parameters"] != 23
            or metadata["pure_coefficients"] != 3
            or metadata["mixed_equations"] != record["mixed_equations"]
            or record["status"] != "UNIT_IDEAL"
            or record["output_sha256"] != output_hash
        ):
            raise AssertionError("source reconstruction or result changed")
        source_bytes += len(data)
        mixed_histogram[metadata["mixed_equations"]] += 1
        if (
            args.rerun_singular
            and position >= args.start
            and (position - args.start) % args.step == 0
        ):
            generated_programs.append((position, program))
            if (
                args.limit is not None
                and len(generated_programs) >= args.limit
            ):
                break

    if not args.rerun_singular and seen != set(audit_by_key):
        raise AssertionError("manifest does not cover the independent audit")
    if not args.rerun_singular:
        observed_histogram = {
            str(key): value for key, value in sorted(mixed_histogram.items())
        }
        if (
            source_bytes != manifest["regenerated_source_bytes"]
            or observed_histogram != manifest["mixed_equation_histogram"]
        ):
            raise AssertionError("aggregate source metadata changed")

    rerun = 0
    command = None
    if args.rerun_singular:
        command = singular_command(args.singular_command)
        for position, program in generated_programs:
            result = subprocess.run(
                command,
                input=program,
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
            if (
                result.returncode != 0
                or result.stderr.strip()
                or result.stdout.strip() != "UNIT_IDEAL"
            ):
                raise AssertionError(
                    f"fresh Singular rerun failed at case {position}: "
                    f"{result.stdout!r} {result.stderr!r}"
                )
            rerun += 1

    print(
        json.dumps(
            {
                "verified": True,
                "scope": manifest["scope"],
                "independent_audit_cases": len(audit_by_key),
                "regenerated_algebra_sources": (
                    len(seen)
                    if not args.rerun_singular
                    else len(generated_programs)
                ),
                "recorded_unit_ideals": manifest[
                    "singular_direct_unit_ideals"
                ],
                "fresh_singular_reruns": rerun,
                "singular_command": command,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
