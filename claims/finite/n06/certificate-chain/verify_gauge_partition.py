"""Audit normalized/unnormalized orbit partitions and certificate coverage."""

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

from killer_union_stratum import mutual_gauge_rank
from krenn_gu.search_witness import EquationSystem


ACCEPTED = {
    "certified",
    "certified_with_exact_fallback",
    "unconditional_laurent_contradiction",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certified_indices(payload: dict[str, object]) -> set[int]:
    return {
        int(row["orbit"])
        for row in payload["rows"]
        if row["status"] in ACCEPTED
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--normalized-manifest", type=Path, required=True)
    parser.add_argument("--unnormalized-manifest", type=Path, required=True)
    parser.add_argument("--unnormalized-replay", type=Path, required=True)
    parser.add_argument("--normalized-replay", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    patterns = json.loads(
        args.orbits.read_text(encoding="utf-8")
    )["representatives"]
    normalized = json.loads(
        args.normalized_manifest.read_text(encoding="utf-8")
    )
    unnormalized = json.loads(
        args.unnormalized_manifest.read_text(encoding="utf-8")
    )
    unnormalized_replay = json.loads(
        args.unnormalized_replay.read_text(encoding="utf-8")
    )
    normalized_replay = (
        json.loads(args.normalized_replay.read_text(encoding="utf-8"))
        if args.normalized_replay
        else None
    )

    system = EquationSystem(6, 3)
    full_rank: set[int] = set()
    deficient: set[int] = set()
    deficiencies: dict[int, int] = {}
    for orbit, pattern in enumerate(patterns):
        mutual_edges, rank = mutual_gauge_rank(system, pattern)
        deficiencies[orbit] = mutual_edges - rank
        (full_rank if mutual_edges == rank else deficient).add(orbit)

    normalized_covered = certified_indices(normalized)
    unnormalized_covered = certified_indices(unnormalized)
    if not full_rank <= normalized_covered:
        raise AssertionError("normalized manifest misses full-rank orbits")
    if unnormalized_covered != deficient:
        raise AssertionError(
            "unnormalized manifest is not exactly the deficient partition"
        )
    if not unnormalized_replay.get("verified"):
        raise AssertionError("unnormalized replay is not verified")
    if int(unnormalized_replay["pattern_orbits"]) != len(deficient):
        raise AssertionError("unnormalized replay orbit count mismatch")
    if normalized_replay is not None:
        if not normalized_replay.get("verified"):
            raise AssertionError("normalized replay is not verified")
        if int(normalized_replay["pattern_orbits"]) != len(full_rank):
            raise AssertionError("normalized replay orbit count mismatch")

    result = {
        "verified": True,
        "orbits": len(patterns),
        "gauge_full": len(full_rank),
        "gauge_deficient": len(deficient),
        "maximum_deficiency": max(deficiencies.values(), default=0),
        "normalized_certified": len(full_rank & normalized_covered),
        "unnormalized_certified": len(unnormalized_covered),
        "normalized_manifest": str(args.normalized_manifest),
        "normalized_manifest_sha256": sha256(args.normalized_manifest),
        "unnormalized_manifest": str(args.unnormalized_manifest),
        "unnormalized_manifest_sha256": sha256(
            args.unnormalized_manifest
        ),
        "normalized_replay": (
            str(args.normalized_replay)
            if args.normalized_replay
            else None
        ),
        "unnormalized_replay": str(args.unnormalized_replay),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: full={len(full_rank)} "
        f"deficient={len(deficient)} verified=True"
    )


if __name__ == "__main__":
    main()
