"""Replay a generated P5 ideal with a workspace-local msolve binary."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONVERTER = ROOT / "tmp" / "convert_p5_singular_to_msolve.py"
MSOLVE_ROOT = ROOT / "tmp" / "msolve_local"
MSOLVE = MSOLVE_ROOT / "usr" / "bin" / "msolve"
MSOLVE_LIB = MSOLVE_ROOT / "usr" / "lib" / "x86_64-linux-gnu"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wsl_path(path: pathlib.Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    if not drive:
        raise ValueError(f"path has no Windows drive: {resolved}")
    return (
        f"/mnt/{drive}/"
        + str(resolved)[len(resolved.drive) :]
        .lstrip("\\/")
        .replace("\\", "/")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=pathlib.Path)
    parser.add_argument("--artifact-dir", type=pathlib.Path, required=True)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    if args.threads <= 0 or args.timeout <= 0:
        raise ValueError("threads and timeout must be positive")
    if not args.source.is_file():
        raise FileNotFoundError(args.source)
    if not MSOLVE.is_file() or not MSOLVE_LIB.is_dir():
        raise FileNotFoundError(
            "workspace-local msolve is missing; extract msolve and "
            "libmsolve packages under tmp/msolve_local"
        )

    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    stem = args.source.stem
    msolve_input = args.artifact_dir / f"{stem}.ms"
    msolve_output = args.artifact_dir / f"{stem}.msolve.out"
    converted = subprocess.run(
        [
            sys.executable,
            str(CONVERTER),
            str(args.source),
            str(msolve_input),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=args.timeout,
        check=False,
    )
    if converted.returncode:
        raise RuntimeError(f"converter failed: {converted.stderr}")

    command = [
        "wsl.exe",
        "--exec",
        "/usr/bin/env",
        f"LD_LIBRARY_PATH={wsl_path(MSOLVE_LIB)}",
        wsl_path(MSOLVE),
        "-f",
        wsl_path(msolve_input),
        "-o",
        wsl_path(msolve_output),
        "-t",
        str(args.threads),
        "-v",
        "1",
    ]
    try:
        solved = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        print(
            json.dumps(
                {
                    "status": "INCONCLUSIVE_TIMEOUT",
                    "source": str(args.source),
                    "timeout_seconds": error.timeout,
                },
                indent=2,
            )
        )
        raise SystemExit(2)

    result = (
        msolve_output.read_text(encoding="utf-8").strip()
        if msolve_output.is_file()
        else None
    )
    status = (
        "UNIT_IDEAL"
        if solved.returncode == 0 and result == "[-1]:"
        else "INCONCLUSIVE_OR_NONUNIT"
    )
    payload = {
        "status": status,
        "source": str(args.source),
        "source_sha256": sha256(args.source),
        "msolve_input": str(msolve_input),
        "msolve_input_sha256": sha256(msolve_input),
        "msolve_output": str(msolve_output),
        "msolve_output_sha256": (
            sha256(msolve_output) if msolve_output.is_file() else None
        ),
        "result": result,
        "returncode": solved.returncode,
        "stdout": solved.stdout,
        "stderr": solved.stderr,
        "threads": args.threads,
    }
    print(json.dumps(payload, indent=2))
    if status != "UNIT_IDEAL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
