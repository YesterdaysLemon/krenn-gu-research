"""One-command audit of the exact n=8 degree-three, 19-edge proof."""

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
    if not isinstance(value, str):
        raise AssertionError("manifest has no output CNF hash")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_degree3_e19_final_audit.json"
        ),
    )
    args = parser.parse_args()

    graph6 = Path("tmp/n8_mindeg3_e12_28.g6")
    checkpoint = Path(
        "tmp/eight_vertex_local_degree3_flag_checkpoint_max19.json"
    )
    learned = Path("tmp/degree3_e19_clean_linear_laurent.json")
    batch = Path("tmp/degree3_e19_clean_linear_batch.json")
    selector = Path("tmp/degree3_e19_clean_linear_selector.json")
    proof = Path(
        "tmp/degree3_e19_clean_linear_selector_cadical195.drat"
    )
    cadical_log = Path(
        "tmp/degree3_e19_clean_linear_selector_cadical195.log"
    )
    drat_log = Path(
        "tmp/degree3_e19_clean_linear_selector_drat_trim.log"
    )
    selector_audit = Path(
        "tmp/degree3_e19_clean_linear_selector_final_audit.json"
    )
    transport_audit = Path(
        "tmp/degree3_e19_clean_linear_transport_audit.json"
    )
    rectangle_audit = Path(
        "tmp/degree3_e19_clean_linear_rectangle_audit.json"
    )

    run(
        [
            str(REPO_ROOT / "src" / "krenn_gu" / "verify_laurent_batch_manifest.py"),
            "--manifest",
            str(checkpoint),
        ]
    )
    run(
        [
            str(REPO_ROOT / "src" / "krenn_gu" / "verify_laurent_batch_manifest.py"),
            "--manifest",
            str(learned),
        ]
    )
    run(
        [
            str(HERE / "verify_skeleton_laurent_batch.py"),
            "--batch",
            str(batch),
            "--manifest",
            str(learned),
            "--graph6",
            str(graph6),
        ]
    )
    run(
        [
            str(HERE / "verify_cancellation_transport_manifest.py"),
            "--manifest",
            str(batch),
            "--output",
            str(transport_audit),
        ]
    )
    run(
        [
            str(HERE / "verify_matching_rectangle_manifest.py"),
            "--manifest",
            str(batch),
            "--output",
            str(rectangle_audit),
        ]
    )
    run(
        [
            str(HERE / "verify_catalogue_selector.py"),
            "--manifest",
            str(selector),
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

    checkpoint_data = json.loads(
        checkpoint.read_text(encoding="utf-8")
    )
    learned_data = json.loads(learned.read_text(encoding="utf-8"))
    batch_data = json.loads(batch.read_text(encoding="utf-8"))
    selector_data = json.loads(selector.read_text(encoding="utf-8"))
    transport_data = json.loads(
        transport_audit.read_text(encoding="utf-8")
    )
    rectangle_data = json.loads(
        rectangle_audit.read_text(encoding="utf-8")
    )

    if (
        output_hash(checkpoint_data)
        != learned_data["base_cnf_sha256"]
    ):
        raise AssertionError(
            "checkpoint-to-linear CNF hash chain is discontinuous"
        )
    if output_hash(learned_data) != batch_data["learned_cnf_sha256"]:
        raise AssertionError("batch does not report the audited learned CNF")
    if output_hash(learned_data) != selector_data["base_cnf_sha256"]:
        raise AssertionError("selector is not based on the audited CNF")

    expected_roles = list(range(235))
    if (
        batch_data["status"] != "complete"
        or not bool(batch_data["catalogue_complete"])
        or int(batch_data["target_edges"]) != 19
        or int(batch_data["center_degree"]) != 3
        or int(batch_data["processed"]) != 235
        or int(batch_data["unsat_count"]) != 235
        or int(batch_data["fallback_count"]) != 0
        or list(batch_data["selected_role_indices"]) != expected_roles
    ):
        raise AssertionError("catalogue coverage changed")
    if (
        int(batch_data["support_models"]) != 252
        or int(batch_data["laurent_conflicts"]) != 252
        or int(batch_data["learned_clauses"]) != 35_496
    ):
        raise AssertionError("clean linear-Laurent census changed")
    if (
        int(checkpoint_data["conflicts"]) != 112
        or int(checkpoint_data["distinct_learned_clauses"]) != 15_912
    ):
        raise AssertionError("theorem-level checkpoint census changed")
    if (
        not bool(transport_data["verified"])
        or int(transport_data["conflicts_checked"]) != 252
        or int(
            transport_data["conflicts_with_transport_certificate"]
        )
        != 12
        or list(transport_data["certified_conflict_indices"])
        != [1, 3, 4, 5, 77, 84, 142, 156, 202, 228, 229, 230]
    ):
        raise AssertionError("cancellation-transport audit changed")
    if (
        not bool(rectangle_data["verified"])
        or int(rectangle_data["conflicts_checked"]) != 252
        or int(
            rectangle_data[
                "conflicts_with_rectangle_certificate"
            ]
        )
        != 35
        or list(rectangle_data["certified_conflict_indices"])
        != [
            0,
            2,
            9,
            14,
            15,
            17,
            18,
            34,
            68,
            72,
            73,
            74,
            91,
            106,
            111,
            114,
            115,
            127,
            129,
            130,
            132,
            133,
            134,
            135,
            147,
            161,
            162,
            165,
            166,
            234,
            235,
            236,
            237,
            239,
            241,
        ]
    ):
        raise AssertionError("matching-rectangle audit changed")

    payload = {
        "verified": True,
        "scope": (
            "n=8, d=3, exactly 19 nonzero blocks, "
            "with a degree-three vertex"
        ),
        "unlabeled_matching_covered_graphs": int(
            batch_data["unlabeled_matching_covered_graphs"]
        ),
        "canonical_roles": int(
            batch_data["canonical_role_skeletons"]
        ),
        "checkpoint_laurent_conflicts": int(
            checkpoint_data["conflicts"]
        ),
        "catalogue_laurent_conflicts": int(
            batch_data["laurent_conflicts"]
        ),
        "total_laurent_conflicts": (
            int(checkpoint_data["conflicts"])
            + int(batch_data["laurent_conflicts"])
        ),
        "elementary_transport_conflicts": int(
            transport_data["conflicts_with_transport_certificate"]
        ),
        "elementary_rectangle_conflicts": int(
            rectangle_data[
                "conflicts_with_rectangle_certificate"
            ]
        ),
        "singular_fallbacks": int(batch_data["fallback_count"]),
        "graph6_sha256": sha256(graph6),
        "initial_support_cnf_sha256": checkpoint_data[
            "base_cnf_sha256"
        ],
        "final_learned_cnf_sha256": output_hash(learned_data),
        "selector_cnf_sha256": selector_data["output_sha256"],
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": sha256(proof),
        "cadical_log_sha256": sha256(cadical_log),
        "drat_log_sha256": sha256(drat_log),
        "selector_audit_sha256": sha256(selector_audit),
        "transport_audit_sha256": sha256(transport_audit),
        "rectangle_audit_sha256": sha256(rectangle_audit),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
