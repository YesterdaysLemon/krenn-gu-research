#!/usr/bin/env python3
"""Audit the packaged exact-three-partial C10 P5 obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import shutil
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/frontier")

import audit_p5_exact_three_partial_boundary as AUDIT
import audit_p5_exact_two_partial_boundary as TWO
import generate_p5_exact_three_partial_support_system as GENERATOR
import verify_p5_pair_signature_catalogue_coverage as COVERAGE


ROOT = Path(__file__).resolve().parent
PACKAGE = (
    REPO_ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c10_boundary"
)
EXPECTED_MANIFEST_SHA256 = (
    "e153f83293214116d7e86c35a8876f3633f7c5a119745730f518cd781df61320"
)
EXPECTED_CATALOGUE_SHA256 = (
    "0c000ecb4b5ed7a1fee30d804b1a37f281861f6cf01e60c132b729f2a31377e1"
)
EXPECTED_AUDIT_SHA256 = (
    "5ffc569491d20c4689fc63f477a361fafe1b35955a1415f30d269bcbc271dc8f"
)
EXPECTED = {
    "labelled_supports": 25_194_240,
    "locally_valid_support_orbits": 281_896,
    "pair_quota_viable_support_orbits": 23_112,
    "pair_quota_viable_signature_tuples": 137_405,
    "support_semantic_viable_support_orbits": 11_751,
    "singular_direct_unit_ideals": 11_751,
    "singular_split_unit_ideals": 0,
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
        return ["wsl.exe", "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError(
        "Singular was not found; pass --singular-command explicitly"
    )


def regenerate_source(
    task: tuple[int, list[list[int]], list[int]],
) -> dict:
    position, support_rows, signature_indices = task
    supports = tuple(tuple(row) for row in support_rows)
    indices = tuple(signature_indices)
    program, metadata = GENERATOR.generate(supports, indices)
    data = program.encode("utf-8")
    return {
        "position": position,
        "source_sha256": sha256_bytes(data),
        "source_bytes": len(data),
        "metadata": metadata,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rerun-singular",
        action="store_true",
        help="Freshly rerun selected exact CAS cases (slow for all).",
    )
    parser.add_argument("--singular-command")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--jobs",
        type=int,
        default=4,
        help="Parallel source-regeneration workers for the full audit.",
    )
    args = parser.parse_args()
    if args.start < 0 or args.step < 1 or args.jobs < 1:
        raise ValueError(
            "start must be nonnegative; step and jobs must be positive"
        )

    manifest_path = PACKAGE / "manifest.json"
    if (
        sha256_bytes(manifest_path.read_bytes())
        != EXPECTED_MANIFEST_SHA256
    ):
        raise AssertionError("packaged manifest hash changed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "EXACT_FINITE_BOUNDARY_THEOREM"
        or manifest.get("shape") != "c10"
        or manifest.get("global_conjecture_resolved") is not False
    ):
        raise AssertionError("manifest status changed")
    for key, value in EXPECTED.items():
        if manifest.get(key) != value:
            raise AssertionError(f"manifest count changed: {key}")

    catalogue_path = (PACKAGE / manifest["catalogue"]["path"]).resolve()
    audit_path = (PACKAGE / manifest["audit"]["path"]).resolve()
    catalogue_hash = sha256_bytes(catalogue_path.read_bytes())
    audit_hash = sha256_bytes(audit_path.read_bytes())
    if (
        catalogue_hash != EXPECTED_CATALOGUE_SHA256
        or catalogue_hash != manifest["catalogue"]["sha256"]
        or audit_hash != EXPECTED_AUDIT_SHA256
        or audit_hash != manifest["audit"]["sha256"]
    ):
        raise AssertionError("packaged census hash changed")
    catalogue_payload = json.loads(
        catalogue_path.read_text(encoding="utf-8")
    )
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if (
        catalogue_payload.get("support_orbits") != 11_751
        or audit.get("verified") is not True
        or audit.get("catalogue_exact_match") is not True
        or audit.get("support_semantic_viable_support_orbits")
        != 11_751
    ):
        raise AssertionError("independent census is incomplete")

    actions = TWO.transformed_actions("c10")
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
    pool = None
    regenerated = None
    if not args.rerun_singular:
        pool = ProcessPoolExecutor(max_workers=args.jobs)
        regenerated = iter(
            pool.map(
                regenerate_source,
                (
                    (
                        position,
                        record["solver_supports"],
                        record["signature_indices"],
                    )
                    for position, record in enumerate(manifest["cases"])
                ),
                chunksize=8,
            )
        )
    for position, record in enumerate(manifest["cases"]):
        if record["algebra_orbit_index"] != position:
            raise AssertionError("algebra orbit ordering changed")
        catalogue_case = catalogue_payload["cases"][position]
        if (
            catalogue_case["orbit_index"] != position
            or catalogue_case["supports"] != record["solver_supports"]
            or catalogue_case["witness_signature_indices"]
            != record["signature_indices"]
        ):
            raise AssertionError("catalogue/algebra mapping changed")

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

        selected_rerun = (
            args.rerun_singular
            and position >= args.start
            and (position - args.start) % args.step == 0
        )
        if args.rerun_singular and not selected_rerun:
            continue
        if args.rerun_singular:
            program, metadata = GENERATOR.generate(supports, indices)
            data = program.encode("utf-8")
            source_sha256 = sha256_bytes(data)
            source_bytes_for_case = len(data)
        else:
            source = next(regenerated)
            if source["position"] != position:
                raise AssertionError("source regeneration ordering changed")
            metadata = source["metadata"]
            source_sha256 = source["source_sha256"]
            source_bytes_for_case = source["source_bytes"]
        if (
            source_sha256 != record["source_sha256"]
            or source_bytes_for_case != record["source_bytes"]
            or metadata["nonzero_entries"] != 42
            or metadata["gauge_free_variables"] != 23
            or metadata["laurent_parameters"] != 23
            or metadata["pure_coefficients"] != 3
            or metadata["mixed_equations"] != record["mixed_equations"]
            or record["status"] != "UNIT_IDEAL"
            or record["output_sha256"] != output_hash
        ):
            raise AssertionError("source reconstruction or result changed")
        source_bytes += source_bytes_for_case
        mixed_histogram[metadata["mixed_equations"]] += 1
        if selected_rerun:
            generated_programs.append((position, program))
            if (
                args.limit is not None
                and len(generated_programs) >= args.limit
            ):
                break
        elif (position + 1) % 1000 == 0:
            print(
                json.dumps(
                    {
                        "regenerated_sources": position + 1,
                        "total": len(manifest["cases"]),
                    }
                ),
                flush=True,
            )
    if pool is not None:
        pool.shutdown()

    if not args.rerun_singular and seen != set(audit_by_key):
        raise AssertionError("manifest does not cover the independent audit")
    if not args.rerun_singular:
        observed_histogram = {
            str(key): value
            for key, value in sorted(mixed_histogram.items())
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
                "recorded_direct_unit_ideals": manifest[
                    "singular_direct_unit_ideals"
                ],
                "recorded_split_unit_ideals": manifest[
                    "singular_split_unit_ideals"
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
