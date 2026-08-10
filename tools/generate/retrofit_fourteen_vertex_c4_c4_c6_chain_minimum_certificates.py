"""Retrofit old C4+C4+C6 incremental chains with minimum certificates.

Early incremental searches stored independently checkable factor-fork
analyses, but learned their full-activity clauses directly.  This utility
replays every simple factor-fork analysis in one or more chain manifests,
minimizes its activation premises, and independently verifies the resulting
minimum-activity certificate.  Non-simple fallback rows are reported and
left untouched.
"""

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


def verified_existing(
    certificate: Path,
    audit: Path,
    *,
    structural: bool,
) -> bool:
    if not certificate.exists() or not audit.exists():
        return False
    try:
        certificate_data = json.loads(
            certificate.read_text(encoding="utf-8")
        )
        audit_data = json.loads(audit.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    expected_scope = (
        "perfect_matching_edge_disjoint"
        if structural
        else "unconditional_edge_assignment"
    )
    return (
        certificate_data.get("activity_scope") == expected_scope
        and audit_data.get("verified") is True
        and audit_data.get("certificate_sha256") == sha256(certificate)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chain", type=Path, action="append", required=True
    )
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--structural", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    for chain_path in args.chain:
        chain = json.loads(chain_path.read_text(encoding="utf-8"))
        chain_stem = chain_path.stem
        if not chain_stem.endswith("_chain"):
            raise ValueError(
                f"chain filename lacks _chain suffix: {chain_path}"
            )
        run_prefix = chain_path.with_name(chain_stem.removesuffix("_chain"))
        samples = Path(f"{run_prefix}_samples.json")
        survivors = json.loads(
            samples.read_text(encoding="utf-8")
        )["survivors"]
        for row in chain["iterations"]:
            iteration = int(row["iteration"])
            if row.get("analysis_status") != "even_cycle_factor_fork":
                skipped.append(
                    {
                        "chain": str(chain_path),
                        "iteration": iteration,
                        "analysis_status": row.get("analysis_status"),
                        "certificate_mode": row.get("certificate_mode"),
                    }
                )
                continue
            if iteration >= len(survivors):
                raise AssertionError(
                    "chain iteration exceeds stored survivor manifest"
                )
            analysis = Path(f"{run_prefix}_{iteration}_factor_fork.json")
            tag = run_prefix.name
            certificate = Path(
                f"{args.output_prefix}_{tag}_{iteration}"
                "_minimum_activity.json"
            )
            audit = certificate.with_name(
                f"{certificate.stem}_verified{certificate.suffix}"
            )
            reused = verified_existing(
                certificate,
                audit,
                structural=args.structural,
            )
            if not reused:
                command = [
                    sys.executable,
                    str(
                        REPO_ROOT
                        / "claims/finite/n14/"
                        "minimize_fourteen_vertex_two_even_cycle_"
                        "certificate_activation.py"
                    ),
                    str(samples),
                    str(analysis),
                    "--survivor-index",
                    str(iteration),
                    "--output",
                    str(certificate),
                ]
                if args.structural:
                    command.append("--structural-feasibility")
                subprocess.run(
                    command,
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                subprocess.run(
                    [
                        sys.executable,
                        str(
                            REPO_ROOT
                            / "claims/finite/n14/"
                            "verify_fourteen_vertex_two_even_cycle_"
                            "minimum_activity_certificate.py"
                        ),
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
                raise AssertionError(
                    f"minimum certificate did not verify: {certificate}"
                )
            rows.append(
                {
                    "chain": str(chain_path),
                    "iteration": iteration,
                    "analysis": str(analysis),
                    "analysis_sha256": sha256(analysis),
                    "certificate": str(certificate),
                    "certificate_sha256": sha256(certificate),
                    "audit": str(audit),
                    "audit_sha256": sha256(audit),
                    "activity_scope": certificate_data[
                        "activity_scope"
                    ],
                    "activation_constraint_score": int(
                        certificate_data[
                            "activation_constraint_score"
                        ]
                    ),
                    "reused": reused,
                }
            )
            if len(rows) % 25 == 0:
                print(
                    json.dumps(
                        {
                            "certificates_verified": len(rows),
                            "fallback_rows_skipped": len(skipped),
                        }
                    ),
                    flush=True,
                )

    payload = {
        "status": "c4_c4_c6_chain_minimum_certificates_verified",
        "chains": [str(path) for path in args.chain],
        "structural": args.structural,
        "certificates": rows,
        "certificates_verified": len(rows),
        "fallback_rows": skipped,
        "fallback_rows_skipped": len(skipped),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
