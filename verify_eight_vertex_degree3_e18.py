"""One-command audit of the exact n=8 degree-three, 18-edge chain."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


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
        "--rerun-singular-wsl", action="store_true"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_degree3_e18_final_audit.json"
        ),
    )
    args = parser.parse_args()

    graph6 = Path("tmp/n8_mindeg3_e12_28.g6")
    transfer = Path(
        "tmp/eight_vertex_local_degree3_flag_checkpoint_max18.json"
    )
    laurent_manifests = [
        Path("tmp/eight_vertex_local_degree3_flag_laurent_e18.json"),
        Path(
            "tmp/eight_vertex_local_degree3_flag_exact_e18_closed.json"
        ),
        Path(
            "tmp/eight_vertex_local_degree3_flag_exact_e18_round2_learned.json"
        ),
        Path(
            "tmp/eight_vertex_local_degree3_flag_exact_e18_round3_learned.json"
        ),
        Path(
            "tmp/eight_vertex_local_degree3_flag_exact_e18_round4_learned.json"
        ),
    ]
    singular_pairs = [
        (
            Path(
                "tmp/degree3_e18_fallback_laurent_singular.json"
            ),
            Path(
                "tmp/eight_vertex_local_degree3_flag_exact_e18.json"
            ),
        ),
        (
            Path(
                "tmp/degree3_e18_closed_fallback_laurent_singular.json"
            ),
            Path(
                "tmp/eight_vertex_local_degree3_flag_exact_e18_round2.json"
            ),
        ),
        (
            Path(
                "tmp/degree3_e18_round2_fallback_laurent_singular.json"
            ),
            Path(
                "tmp/eight_vertex_local_degree3_flag_exact_e18_round3.json"
            ),
        ),
        (
            Path(
                "tmp/degree3_e18_round3_fallback_laurent_singular.json"
            ),
            Path(
                "tmp/eight_vertex_local_degree3_flag_exact_e18_round4.json"
            ),
        ),
    ]
    final_batch = Path(
        "tmp/eight_vertex_skeleton_laurent_degree3_e18_round4.json"
    )

    run(
        [
            "verify_laurent_batch_manifest.py",
            "--manifest",
            str(transfer),
        ]
    )
    for manifest in laurent_manifests:
        run(
            [
                "verify_laurent_batch_manifest.py",
                "--manifest",
                str(manifest),
            ]
        )
    for fallback, learned in singular_pairs:
        command = [
            "verify_singular_fallback_manifest.py",
            "--fallback-manifest",
            str(fallback),
            "--learned-manifest",
            str(learned),
        ]
        if args.rerun_singular_wsl:
            command.append("--rerun-singular-wsl")
        run(command)
    run(
        [
            "verify_skeleton_laurent_batch.py",
            "--batch",
            str(final_batch),
            "--manifest",
            str(laurent_manifests[-1]),
            "--graph6",
            str(graph6),
        ]
    )

    ordered_chain = [
        transfer,
        laurent_manifests[0],
        singular_pairs[0][1],
        laurent_manifests[1],
        singular_pairs[1][1],
        laurent_manifests[2],
        singular_pairs[2][1],
        laurent_manifests[3],
        singular_pairs[3][1],
        laurent_manifests[4],
    ]
    parsed = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in ordered_chain
    ]
    for previous_path, previous, next_path, following in zip(
        ordered_chain[:-1],
        parsed[:-1],
        ordered_chain[1:],
        parsed[1:],
        strict=True,
    ):
        if output_hash(previous) != following["base_cnf_sha256"]:
            raise AssertionError(
                f"CNF hash discontinuity between {previous_path} "
                f"and {next_path}"
            )

    final = json.loads(final_batch.read_text(encoding="utf-8"))
    if (
        final["status"] != "complete"
        or int(final["target_edges"]) != 18
        or int(final["center_degree"]) != 3
        or int(final["processed"]) != 466
        or int(final["unsat_count"]) != 466
        or int(final["fallback_count"]) != 0
    ):
        raise AssertionError("final batch coverage changed")
    if (
        final["learned_cnf_sha256"]
        != output_hash(parsed[-1])
    ):
        raise AssertionError("final batch learned CNF hash changed")

    payload = {
        "verified": True,
        "scope": (
            "n=8, d=3, exactly 18 nonzero blocks, "
            "with a degree-three vertex"
        ),
        "unlabeled_matching_covered_graphs": int(
            final["unlabeled_matching_covered_graphs"]
        ),
        "canonical_roles": int(
            final["canonical_role_skeletons"]
        ),
        "laurent_conflicts": sum(
            int(
                json.loads(
                    path.read_text(encoding="utf-8")
                )["laurent_conflicts"]
            )
            for path in laurent_manifests
        ),
        "singular_unit_ideals": sum(
            int(
                json.loads(
                    fallback.read_text(encoding="utf-8")
                )["fallbacks"]
            )
            for fallback, _ in singular_pairs
        ),
        "singular_rerun": args.rerun_singular_wsl,
        "graph6_sha256": sha256(graph6),
        "initial_support_cnf_sha256": parsed[0][
            "base_cnf_sha256"
        ],
        "final_learned_cnf_sha256": final[
            "learned_cnf_sha256"
        ],
        "chain_manifests": [
            {
                "path": str(path),
                "sha256": sha256(path),
            }
            for path in ordered_chain
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
