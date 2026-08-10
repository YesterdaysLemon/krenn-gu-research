"""Batch-produce and independently replay minimum-activity certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--analysis-pattern", required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--structural", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.count < 1:
        raise ValueError("--count must be positive")
    started = time.perf_counter()
    rows = []
    for index in range(args.count):
        analysis = Path(args.analysis_pattern.format(index=index))
        certificate = Path(
            f"{args.output_prefix}_{index}_minimum_activity.json"
        )
        audit = Path(
            f"{args.output_prefix}_{index}_"
            "minimum_activity_verified.json"
        )
        command = [
            sys.executable,
            "minimize_fourteen_vertex_two_even_cycle_"
            "certificate_activation.py",
            str(args.samples),
            str(analysis),
            "--survivor-index",
            str(index),
            "--output",
            str(certificate),
        ]
        if args.structural:
            command.append("--structural-feasibility")
        subprocess.run(
            command, check=True, stdout=subprocess.DEVNULL
        )
        subprocess.run(
            [
                sys.executable,
                "verify_fourteen_vertex_two_even_cycle_"
                "minimum_activity_certificate.py",
                str(certificate),
                "--output",
                str(audit),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        certificate_data = json.loads(
            certificate.read_text(encoding="utf-8")
        )
        audit_data = json.loads(audit.read_text(encoding="utf-8"))
        if audit_data.get("verified") is not True:
            raise AssertionError("minimum certificate did not verify")
        rows.append(
            {
                "index": index,
                "analysis": str(analysis),
                "analysis_sha256": sha256(analysis),
                "certificate": str(certificate),
                "certificate_sha256": sha256(certificate),
                "audit": str(audit),
                "audit_sha256": sha256(audit),
                "activity_scope": certificate_data.get(
                    "activity_scope",
                    "unconditional_edge_assignment",
                ),
                "activation_constraint_score": int(
                    certificate_data["activation_constraint_score"]
                ),
            }
        )
        if (index + 1) % 10 == 0:
            print(
                json.dumps(
                    {
                        "completed": index + 1,
                        "total": args.count,
                    }
                ),
                flush=True,
            )
    payload = {
        "status": "minimum_activity_batch_verified",
        "samples": str(args.samples),
        "samples_sha256": sha256(args.samples),
        "analysis_pattern": args.analysis_pattern,
        "structural": args.structural,
        "certificates": rows,
        "certificates_verified": len(rows),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
