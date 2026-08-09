"""Run one WSL Kissat decision with a raw binary DRAT proof."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

from eight_vertex_native_kissat_laurent_batch import sha256, wsl_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--configuration",
        choices=("default", "sat", "unsat"),
        default="sat",
    )
    args = parser.parse_args()

    for path in (
        args.proof,
        args.stdout,
        args.stderr,
        args.output,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
    command = (
        f"'{wsl_path(args.kissat)}' --{args.configuration} --force "
        f"'{wsl_path(args.cnf)}' '{wsl_path(args.proof)}'"
    )
    started = time.perf_counter()
    with args.stdout.open("wb") as stdout, args.stderr.open(
        "wb"
    ) as stderr:
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
    log_text = args.stdout.read_text(encoding="ascii")
    if result.returncode == 20 and "s UNSATISFIABLE" in log_text:
        status = "UNSAT"
    elif result.returncode == 10 and "s SATISFIABLE" in log_text:
        status = "SAT"
    else:
        status = "ERROR"
    payload: dict[str, object] = {
        "status": status,
        "returncode": result.returncode,
        "configuration": args.configuration,
        "kissat": str(args.kissat),
        "kissat_sha256": sha256(args.kissat),
        "cnf": str(args.cnf),
        "cnf_sha256": sha256(args.cnf),
        "proof": str(args.proof),
        "stdout": str(args.stdout),
        "stdout_sha256": sha256(args.stdout),
        "stderr": str(args.stderr),
        "stderr_sha256": sha256(args.stderr),
        "solve_seconds": elapsed,
    }
    if args.proof.exists():
        payload["proof_bytes"] = args.proof.stat().st_size
        payload["proof_sha256"] = sha256(args.proof)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))
    if status == "ERROR":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
