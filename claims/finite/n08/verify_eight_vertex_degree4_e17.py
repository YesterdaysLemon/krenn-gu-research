"""One-command audit of the exact n=8 degree-four, 17-edge proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(arguments: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(
            f"{arguments[0]} failed:\n"
            f"{result.stdout}\n{result.stderr}"
        )


def output_hash(manifest: dict[str, object]) -> str:
    value = manifest.get("learned_cnf_sha256")
    if value is None:
        value = manifest.get("output_cnf_sha256")
    if isinstance(value, str):
        return value
    path = manifest.get("learned_cnf")
    if path is None:
        path = manifest.get("output_cnf")
    if not isinstance(path, str):
        raise AssertionError("manifest has no output CNF path")
    return sha256(Path(path))


def input_hash(manifest: dict[str, object]) -> str:
    value = manifest.get("base_cnf_sha256")
    if isinstance(value, str):
        return value
    path = manifest.get("base_cnf")
    if not isinstance(path, str):
        raise AssertionError("manifest has no base CNF path")
    return sha256(Path(path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_degree4_e17_final_audit.json"
        ),
    )
    args = parser.parse_args()

    graph6 = Path("tmp/n8_mindeg3_e17.g6")
    replay = Path(
        "tmp/eight_vertex_local_degree4_flag_cegar3_"
        "max17_replay.json"
    )
    original_replay_cnf = Path(
        "tmp/eight_vertex_local_degree4_flag_cegar3_max17.cnf"
    )
    replay_cnf = Path(
        "tmp/eight_vertex_local_degree4_flag_cegar3_"
        "max17_replay.cnf"
    )
    local_manifests = [
        replay,
        Path(
            "tmp/eight_vertex_local_degree4_flag_cegar4_max17.json"
        ),
        Path(
            "tmp/eight_vertex_local_degree4_flag_laurent_e17.json"
        ),
    ]
    batch = Path(
        "tmp/eight_vertex_skeleton_laurent_flag_batch_e17.json"
    )
    selector_manifest = Path(
        "tmp/eight_vertex_17edge_catalogue_flag_laurent.json"
    )
    proof = Path(
        "tmp/eight_vertex_17edge_catalogue_flag_"
        "laurent_cadical195.drat"
    )
    cadical_log = Path(
        "tmp/eight_vertex_17edge_catalogue_flag_"
        "laurent_cadical195.log"
    )
    drat_log = Path(
        "tmp/eight_vertex_17edge_catalogue_flag_"
        "laurent_drat_trim.log"
    )
    selector_audit = Path(
        "tmp/eight_vertex_17edge_selector_final_audit.json"
    )

    for manifest in local_manifests:
        run(
            [
                str(HERE / "verify_laurent_batch_manifest.py"),
                "--manifest",
                str(manifest),
            ]
        )
    if sha256(original_replay_cnf) != sha256(replay_cnf):
        raise AssertionError(
            "replayed three-conflict prefix differs from the "
            "historical proof prefix"
        )
    run(
        [
            str(HERE / "verify_skeleton_laurent_batch.py"),
            "--batch",
            str(batch),
            "--manifest",
            str(local_manifests[-1]),
            "--graph6",
            str(graph6),
        ]
    )
    run(
        [
            str(HERE / "verify_catalogue_selector.py"),
            "--manifest",
            str(selector_manifest),
            "--proof",
            str(proof),
            "--cadical-log",
            str(cadical_log),
            "--drat-log",
            str(drat_log),
            "--output",
            str(selector_audit),
        ]
    )

    parsed = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in local_manifests
    ]
    for previous, following in zip(
        parsed[:-1], parsed[1:], strict=True
    ):
        if output_hash(previous) != input_hash(following):
            raise AssertionError("local CNF hash chain is discontinuous")
    selector = json.loads(
        selector_manifest.read_text(encoding="utf-8")
    )
    if selector["base_cnf_sha256"] != output_hash(parsed[-1]):
        raise AssertionError("selector is not based on the audited CNF")
    coverage = json.loads(batch.read_text(encoding="utf-8"))
    if (
        coverage["status"] != "complete"
        or int(coverage["target_edges"]) != 17
        or int(coverage["processed"]) != 11051
        or int(coverage["unsat_count"]) != 11051
        or int(coverage["fallback_count"]) != 0
    ):
        raise AssertionError("catalogue coverage changed")

    payload = {
        "verified": True,
        "scope": (
            "n=8, d=3, exactly 17 nonzero blocks, "
            "with a degree-four vertex"
        ),
        "unlabeled_matching_covered_graphs": int(
            coverage["unlabeled_matching_covered_graphs"]
        ),
        "canonical_roles": int(
            coverage["canonical_role_skeletons"]
        ),
        "laurent_conflicts": (
            int(parsed[0]["conflicts"])
            + 1
            + int(parsed[2]["laurent_conflicts"])
        ),
        "learned_clauses": (
            int(parsed[0]["distinct_learned_clauses"])
            + int(parsed[1]["distinct_learned_clauses"])
            + len(parsed[2]["learned_clauses"])
        ),
        "graph6_sha256": sha256(graph6),
        "selector_cnf_sha256": selector["output_sha256"],
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": sha256(proof),
        "cadical_log_sha256": sha256(cadical_log),
        "drat_log_sha256": sha256(drat_log),
        "selector_audit_sha256": sha256(selector_audit),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
