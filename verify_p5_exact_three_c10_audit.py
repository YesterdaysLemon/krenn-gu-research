"""Verify the packaged exact-three-partial C10 census checkpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import audit_p5_exact_three_partial_boundary as AUDIT
import audit_p5_exact_two_partial_boundary as TWO


ROOT = Path(__file__).resolve().parent
PACKAGE = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c10_audit"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def packed(rows: list[list[int]]) -> int:
    return TWO.pack([mask for row in rows for mask in row])


def main() -> None:
    manifest = json.loads(
        (PACKAGE / "manifest.json").read_text(encoding="utf-8")
    )
    catalogue_path = PACKAGE / "sat_catalogue_c10.json"
    audit_path = PACKAGE / "audit_c10.json"
    for path in (catalogue_path, audit_path):
        expected = manifest["files"][path.name]
        if path.stat().st_size != expected["bytes"]:
            raise AssertionError(f"byte count changed: {path.name}")
        if sha256(path) != expected["sha256"]:
            raise AssertionError(f"SHA-256 changed: {path.name}")

    catalogue = json.loads(catalogue_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "EXACT_FINITE_CENSUS"
        or manifest.get("algebraic_exclusion_complete") is not False
        or manifest.get("global_conjecture_resolved") is not False
        or catalogue.get("status") != "COMPLETE"
        or catalogue.get("shape") != "c10"
        or catalogue.get("partial_cells") != 3
        or catalogue.get("support_orbits") != 11_751
        or audit.get("verified") is not True
        or audit.get("shape") != "c10"
        or audit.get("labelled_supports") != 25_194_240
        or audit.get("locally_valid_support_orbits") != 281_896
        or audit.get("pair_quota_viable_support_orbits") != 23_112
        or audit.get("pair_quota_viable_signature_tuples") != 137_405
        or audit.get("support_semantic_viable_support_orbits") != 11_751
        or audit.get("sat_catalogue_support_orbits") != 11_751
        or audit.get("catalogue_exact_match") is not True
    ):
        raise AssertionError("packaged census metadata changed")

    actions = TWO.transformed_actions("c10")
    catalogue_supports = set()
    for case in catalogue["cases"]:
        support = packed(case["supports"])
        canonical = AUDIT.canonical_support(support, actions)
        if canonical in catalogue_supports:
            raise AssertionError("duplicate SAT support orbit")
        catalogue_supports.add(canonical)

    audit_supports = set()
    for case in audit["cases"]:
        support = packed(case["supports"])
        if AUDIT.canonical_support(support, actions) != support:
            raise AssertionError("audit representative is not canonical")
        if case.get("orbit_size") != 60:
            raise AssertionError("unexpected C10 orbit size")
        if case.get("viable_signature_tuples", 0) < 1:
            raise AssertionError("audit case lacks a signature witness")
        if support in audit_supports:
            raise AssertionError("duplicate audit support orbit")
        audit_supports.add(support)

    if len(catalogue_supports) != 11_751:
        raise AssertionError("SAT catalogue support count changed")
    if audit_supports != catalogue_supports:
        raise AssertionError("SAT catalogue and packed audit disagree")

    print(
        json.dumps(
            {
                "verified": True,
                "scope": manifest["scope"],
                "labelled_supports_independently_audited": 25_194_240,
                "support_orbits": len(audit_supports),
                "catalogue_exact_match": True,
                "algebraic_exclusion_complete": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
