"""Transport colour-symmetric factor-fork proofs to new pinned roles.

The rule CNFs pin the first singleton matching to an orbit representative.
Older minimum-activity certificates only exploited colour permutations
that kept that role fixed.  This utility independently re-minimizes the
same verified factor-fork proof with source role 1 or 2 pinned first and
then verifies the resulting certificate.
"""

from __future__ import annotations

import argparse
import glob
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


def paths_for(patterns: list[str]) -> list[Path]:
    paths: dict[Path, Path] = {}
    for pattern in patterns:
        for raw in glob.glob(pattern):
            path = Path(raw)
            paths.setdefault(path.resolve(), path)
    return sorted(paths.values(), key=lambda path: str(path))


def existing_verified(
    certificate: Path, audit: Path, role: int
) -> bool:
    if not certificate.exists() or not audit.exists():
        return False
    try:
        data = json.loads(certificate.read_text(encoding="utf-8"))
        replay = json.loads(audit.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    transform = data.get("source_transform") or {}
    return (
        int(transform.get("pinned_source_role", -1)) == role
        and replay.get("verified") is True
        and replay.get("certificate_sha256") == sha256(certificate)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate-glob", action="append", required=True
    )
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument(
        "--role",
        type=int,
        choices=(1, 2),
        action="append",
        default=[],
    )
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    roles = sorted(set(args.role or [1, 2]))
    sources = paths_for(args.certificate_glob)
    if not sources:
        raise ValueError("no source certificates matched")

    started = time.perf_counter()
    rows = []
    skipped = []
    for source in sources:
        source_data = json.loads(source.read_text(encoding="utf-8"))
        if source_data.get("source_transform") is not None:
            skipped.append(
                {
                    "certificate": str(source),
                    "reason": "already_reoriented",
                }
            )
            continue
        samples = Path(source_data["samples"])
        analysis = Path(source_data["analysis"])
        survivor_index = int(source_data["survivor_index"])
        for role in roles:
            certificate = Path(
                f"{args.output_prefix}_{source.stem}_"
                f"pinrole{role}_minimum_activity.json"
            )
            audit = certificate.with_name(
                f"{certificate.stem}_verified{certificate.suffix}"
            )
            reused = existing_verified(certificate, audit, role)
            if not reused:
                subprocess.run(
                    [
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
                        str(survivor_index),
                        "--structural-feasibility",
                        "--pin-source-role",
                        str(role),
                        "--census",
                        str(args.census),
                        "--output",
                        str(certificate),
                    ],
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
            data = json.loads(certificate.read_text(encoding="utf-8"))
            replay = json.loads(audit.read_text(encoding="utf-8"))
            if replay.get("verified") is not True:
                raise AssertionError(
                    f"re-oriented certificate did not verify: {certificate}"
                )
            rows.append(
                {
                    "source_certificate": str(source),
                    "source_certificate_sha256": sha256(source),
                    "pinned_source_role": role,
                    "certificate": str(certificate),
                    "certificate_sha256": sha256(certificate),
                    "audit": str(audit),
                    "audit_sha256": sha256(audit),
                    "activation_constraint_score": int(
                        data["activation_constraint_score"]
                    ),
                    "reused": reused,
                }
            )
            if len(rows) % 25 == 0:
                print(
                    json.dumps(
                        {
                            "reoriented_certificates_verified": len(rows),
                            "sources": len(sources),
                        }
                    ),
                    flush=True,
                )

    payload = {
        "status": "colour_reoriented_minimum_certificates_verified",
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "source_certificates": len(sources),
        "roles": roles,
        "certificates": rows,
        "reoriented_certificates_verified": len(rows),
        "skipped": skipped,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
