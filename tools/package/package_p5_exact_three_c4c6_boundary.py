"""Package the completed exact-three-partial C4+C6 calculation."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/boundaries")

import audit_p5_exact_three_partial_boundary as AUDIT
import audit_p5_exact_two_partial_boundary as TWO


ROOT = Path(__file__).resolve().parent
TMP = REPO_ROOT / 'tmp'
DESTINATION = (
    REPO_ROOT / 'research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c4c6_boundary'
)
AUDIT_SOURCE = TMP / "p5_c4c6_exact_three_packed_audit.json"
SHARDS = (
    TMP / "p5_c4c6_exact_three_shard0.json",
    TMP / "p5_c4c6_exact_three_shard1.json",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def packed_support(rows: list[list[int]]) -> int:
    return TWO.pack([mask for row in rows for mask in row])


def main() -> None:
    audit = json.loads(AUDIT_SOURCE.read_text(encoding="utf-8"))
    if (
        audit.get("verified") is not True
        or audit.get("shape") != "c4c6"
        or audit.get("support_semantic_viable_support_orbits") != 5_993
        or audit.get("catalogue_exact_match") is not True
    ):
        raise AssertionError("independent exact-three audit is incomplete")

    actions = TWO.transformed_actions("c4c6")
    audit_by_key = {}
    for case in audit["cases"]:
        packed = packed_support(case["supports"])
        if AUDIT.canonical_support(packed, actions) != packed:
            raise AssertionError("audit case is not the canonical representative")
        if packed in audit_by_key:
            raise AssertionError("duplicate audit support")
        audit_by_key[packed] = case

    algebra_records = []
    for expected_start, path in enumerate(SHARDS):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if (
            payload.get("status") != "COMPLETE"
            or payload.get("start") != expected_start
            or payload.get("step") != 2
            or payload.get("counts")
            != {"UNIT_IDEAL": payload.get("selected_support_orbits")}
        ):
            raise AssertionError(f"incomplete algebra shard: {path}")
        algebra_records.extend(payload["results"])

    if len(algebra_records) != 5_993:
        raise AssertionError("algebra shards do not contain 5,993 cases")
    algebra_records.sort(key=lambda record: record["orbit_index"])
    if [record["orbit_index"] for record in algebra_records] != list(
        range(5_993)
    ):
        raise AssertionError("algebra orbit indices are not exhaustive")

    seen = set()
    packaged_cases = []
    mixed_histogram: Counter[int] = Counter()
    source_bytes = 0
    solver_seconds = 0.0
    for record in algebra_records:
        solver_support = packed_support(record["supports"])
        canonical = AUDIT.canonical_support(solver_support, actions)
        if canonical in seen or canonical not in audit_by_key:
            raise AssertionError("algebra/audit support mismatch")
        seen.add(canonical)
        audit_case = audit_by_key[canonical]

        if (
            record.get("status") != "UNIT_IDEAL"
            or record.get("split_cas") is not None
        ):
            raise AssertionError("case lacks a direct unit-ideal result")
        cas = record["cas"]
        if (
            cas.get("returncode") != 0
            or cas.get("stdout") != "UNIT_IDEAL"
            or cas.get("stderr") != ""
            or cas.get("order") != "dp"
            or cas.get("algorithm") != "slimgb"
            or cas.get("support_only") is not True
            or cas.get("unit_ideal") is not True
        ):
            raise AssertionError("unexpected CAS result")

        source = REPO_ROOT / cas["source"]
        output = REPO_ROOT / cas["log"]
        source_text = source.read_text(encoding="utf-8")
        source_data = source_text.encode("utf-8")
        output_data = output.read_bytes()
        if output_data.decode("utf-8").strip() != "UNIT_IDEAL":
            raise AssertionError("CAS output changed")
        expected_headers = (
            "// coefficient stratum: exact support only",
            "// nonzero entries: 42",
            "// gauge-free variables: 23",
            "// Laurent parameters: 23",
        )
        if not all(header in source_text for header in expected_headers):
            raise AssertionError("Singular source metadata changed")
        match = re.search(
            r"^// distinct mixed equations: ([0-9]+)$",
            source_text,
            flags=re.MULTILINE,
        )
        if match is None:
            raise AssertionError("Singular mixed-equation count is absent")
        mixed_equations = int(match.group(1))

        mixed_histogram[mixed_equations] += 1
        source_bytes += len(source_data)
        solver_seconds += record["seconds"]
        packaged_cases.append(
            {
                "algebra_orbit_index": record["orbit_index"],
                "audit_orbit_index": audit_case["audit_orbit_index"],
                "canonical_support": canonical,
                "solver_supports": record["supports"],
                "signature_indices": record["signature_indices"],
                "mixed_equations": mixed_equations,
                "source_bytes": len(source_data),
                "source_sha256": sha256_bytes(source_data),
                "status": "UNIT_IDEAL",
                "solver_seconds": record["seconds"],
                "output_sha256": sha256_bytes(b"UNIT_IDEAL\n"),
            }
        )

    if seen != set(audit_by_key):
        raise AssertionError("algebra does not cover the audited catalogue")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    packaged_audit = DESTINATION / "audit_c4c6.json"
    shutil.copyfile(AUDIT_SOURCE, packaged_audit)
    manifest = {
        "schema": 1,
        "status": "EXACT_FINITE_BOUNDARY_THEOREM",
        "scope": (
            "exactly-three-partial C4+C6 part of the "
            "exact-three-coordinate P5 boundary"
        ),
        "global_conjecture_resolved": False,
        "shape": "c4c6",
        "labelled_supports": audit["labelled_supports"],
        "locally_valid_support_orbits": audit[
            "locally_valid_support_orbits"
        ],
        "pair_quota_viable_support_orbits": audit[
            "pair_quota_viable_support_orbits"
        ],
        "pair_quota_viable_signature_tuples": audit[
            "pair_quota_viable_signature_tuples"
        ],
        "support_semantic_exclusion_histogram": audit[
            "support_semantic_exclusion_histogram"
        ],
        "support_semantic_viable_support_orbits": len(packaged_cases),
        "singular_direct_unit_ideals": len(packaged_cases),
        "singular_version": "4.3.2",
        "singular_order": "dp",
        "singular_algorithm": "slimgb",
        "solver_seconds": round(solver_seconds, 3),
        "regenerated_source_bytes": source_bytes,
        "mixed_equation_histogram": {
            str(key): value for key, value in sorted(mixed_histogram.items())
        },
        "audit": {
            "path": "audit_c4c6.json",
            "sha256": sha256_bytes(packaged_audit.read_bytes()),
        },
        "cases": packaged_cases,
    }
    manifest_path = DESTINATION / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "packaged": True,
                "destination": str(DESTINATION.relative_to(REPO_ROOT)),
                "cases": len(packaged_cases),
                "manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
                "audit_sha256": manifest["audit"]["sha256"],
                "source_bytes": source_bytes,
                "solver_seconds": round(solver_seconds, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
