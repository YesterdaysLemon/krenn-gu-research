"""Independently replay the exact support-toric census certificates."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import hashlib
import json
from pathlib import Path

from eight_vertex_skeleton_laurent_batch import (
    local_positive_to_flat,
)
from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from krenn_gu.search_witness import EquationSystem
from support_toric_degeneration import (
    verify_balanced_certificate,
    verify_degeneration_certificate,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manifest",
        type=Path,
        nargs="?",
        default=Path(
            "tmp/eight_vertex_support_toric_census.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_support_toric_census_verified.json"
        ),
    )
    args = parser.parse_args()

    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    source = Path(payload["source_manifest"])
    if sha256(source) != payload["source_manifest_sha256"]:
        raise AssertionError("source-manifest hash changed")
    system = EquationSystem(8, 3)
    modes = {
        "support_degeneration": 0,
        "balanced_support": 0,
    }
    seen_hashes: set[str] = set()
    for row in payload["models"]:
        log = Path(row["log"])
        log_hash = sha256(log)
        if log_hash != row["log_sha256"]:
            raise AssertionError(f"source log hash changed: {log}")
        if log_hash in seen_hashes:
            raise AssertionError(f"duplicate source log: {log}")
        seen_hashes.add(log_hash)
        selected = sorted(
            local_positive_to_flat(
                system,
                sorted(positive_model_literals(log)),
                center_degree=1,
            )
        )
        if len(selected) != int(row["selected_entries"]):
            raise AssertionError(f"entry count changed: {log}")
        certificate = row["certificate"]
        mode = certificate["mode"]
        if mode == "support_degeneration":
            verify_degeneration_certificate(
                system, selected, certificate
            )
        elif mode == "balanced_support":
            verify_balanced_certificate(
                system, selected, certificate
            )
        else:
            raise AssertionError(f"unknown certificate mode: {mode}")
        modes[mode] += 1

    if len(payload["models"]) != int(payload["support_models"]):
        raise AssertionError("support-model count is inconsistent")
    if modes["support_degeneration"] != int(
        payload["degenerable_supports"]
    ):
        raise AssertionError("degeneration count is inconsistent")
    if modes["balanced_support"] != int(
        payload["balanced_supports"]
    ):
        raise AssertionError("balanced count is inconsistent")
    result = {
        "verified": True,
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "support_models": len(payload["models"]),
        "degenerable_supports": modes["support_degeneration"],
        "balanced_supports": modes["balanced_support"],
    }
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
