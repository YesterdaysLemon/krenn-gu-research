"""Package the independently audited exact-three-partial C10 catalogue."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



ROOT = Path(__file__).resolve().parent
TMP = REPO_ROOT / 'tmp'
DESTINATION = (
    REPO_ROOT / 'research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c10_audit'
)
CATALOGUE_SOURCE = TMP / "p5_c10_exact_three_partial_supports.json"
AUDIT_SOURCE = TMP / "p5_c10_exact_three_packed_audit.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    catalogue = json.loads(CATALOGUE_SOURCE.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_SOURCE.read_text(encoding="utf-8"))
    if (
        catalogue.get("status") != "COMPLETE"
        or catalogue.get("shape") != "c10"
        or catalogue.get("partial_cells") != 3
        or catalogue.get("support_orbits") != 11_751
        or len(catalogue.get("cases", [])) != 11_751
    ):
        raise AssertionError("SAT catalogue is incomplete")
    if (
        audit.get("verified") is not True
        or audit.get("shape") != "c10"
        or audit.get("labelled_supports") != 25_194_240
        or audit.get("support_semantic_viable_support_orbits") != 11_751
        or audit.get("sat_catalogue_support_orbits") != 11_751
        or audit.get("catalogue_exact_match") is not True
        or len(audit.get("cases", [])) != 11_751
    ):
        raise AssertionError("independent packed audit is incomplete")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    catalogue_path = DESTINATION / "sat_catalogue_c10.json"
    audit_path = DESTINATION / "audit_c10.json"
    shutil.copyfile(CATALOGUE_SOURCE, catalogue_path)
    shutil.copyfile(AUDIT_SOURCE, audit_path)

    manifest = {
        "schema": 1,
        "status": "EXACT_FINITE_CENSUS",
        "scope": (
            "exactly-three-partial C10 part of the "
            "exact-three-coordinate P5 boundary"
        ),
        "global_conjecture_resolved": False,
        "algebraic_exclusion_complete": False,
        "shape": "c10",
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
        "support_semantic_viable_support_orbits": audit[
            "support_semantic_viable_support_orbits"
        ],
        "catalogue_exact_match": True,
        "files": {
            "sat_catalogue_c10.json": {
                "bytes": catalogue_path.stat().st_size,
                "sha256": sha256(catalogue_path),
            },
            "audit_c10.json": {
                "bytes": audit_path.stat().st_size,
                "sha256": sha256(audit_path),
            },
        },
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
                "support_orbits": 11_751,
                "manifest_sha256": sha256(manifest_path),
                "catalogue_sha256": manifest["files"][
                    "sat_catalogue_c10.json"
                ]["sha256"],
                "audit_sha256": manifest["files"]["audit_c10.json"][
                    "sha256"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
