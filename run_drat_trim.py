"""Replay one DRAT proof with the independent WSL drat-trim checker."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wsl_path(path: Path) -> str:
    absolute = path.resolve()
    drive = absolute.drive.rstrip(":").lower()
    suffix = absolute.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{suffix}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--forward",
        action="store_true",
        help="pass -f for forward UNSAT proof checking",
    )
    args = parser.parse_args()
    for path in (args.stdout, args.stderr, args.output):
        path.parent.mkdir(parents=True, exist_ok=True)
    command = (
        f"'{wsl_path(args.drat_trim)}' "
        f"'{wsl_path(args.cnf)}' '{wsl_path(args.proof)}' "
        f"{'-f ' if args.forward else ''}-w"
    )
    started = time.perf_counter()
    with args.stdout.open("wb") as stdout, args.stderr.open("wb") as stderr:
        result = subprocess.run(
            [
                "wsl.exe",
                "-d",
                "Ubuntu",
                "--",
                "bash",
                "--noprofile",
                "--norc",
                "-lc",
                command,
            ],
            check=False,
            stdout=stdout,
            stderr=stderr,
        )
    elapsed = time.perf_counter() - started
    text = args.stdout.read_text(encoding="utf-8", errors="replace")
    verified = result.returncode == 0 and "s VERIFIED" in text
    payload = {
        "verified": verified,
        "returncode": result.returncode,
        "forward": args.forward,
        "drat_trim": str(args.drat_trim),
        "drat_trim_sha256": sha256(args.drat_trim),
        "cnf": str(args.cnf),
        "cnf_sha256": sha256(args.cnf),
        "proof": str(args.proof),
        "proof_bytes": args.proof.stat().st_size,
        "proof_sha256": sha256(args.proof),
        "stdout": str(args.stdout),
        "stdout_sha256": sha256(args.stdout),
        "stderr": str(args.stderr),
        "stderr_sha256": sha256(args.stderr),
        "verify_seconds": elapsed,
    }
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))
    if not verified:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
