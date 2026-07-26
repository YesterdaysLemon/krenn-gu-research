"""Produce and replay compact DRAT proofs for all 23 unary factor CNFs."""

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


def run(
    command: str,
    stdout_path: Path,
    stderr_path: Path,
) -> tuple[int, float]:
    started = time.perf_counter()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
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
    return result.returncode, time.perf_counter() - started


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--producer",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family.json"
        ),
    )
    parser.add_argument(
        "--semantic",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family_verified.json"
        ),
    )
    parser.add_argument(
        "--kissat",
        type=Path,
        default=Path("tmp/kissat_wsl_lf/build/kissat"),
    )
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=Path("tmp/drat-trim/drat-trim"),
    )
    parser.add_argument(
        "--proof-dir",
        type=Path,
        default=Path("tmp/eight_vertex_unary_cycle_relation_proofs"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family_proofs_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    semantic = json.loads(args.semantic.read_text(encoding="utf-8"))
    if producer.get("status") != "UNSAT":
        raise AssertionError("producer family is not UNSAT")
    if semantic.get("verified") is not True:
        raise AssertionError("semantic family replay is not verified")
    if semantic["producer_sha256"] != sha256(args.producer):
        raise AssertionError("semantic replay binds another producer")
    if len(producer["rows"]) != 23 or semantic["orbits"] != 23:
        raise AssertionError("family does not contain 23 orbits")
    args.proof_dir.mkdir(parents=True, exist_ok=True)

    checks: list[dict[str, object]] = []
    for index, row in enumerate(producer["rows"]):
        cnf = Path(row["final_cnf"])
        semantic_row = semantic["checks"][index]
        if Path(semantic_row["final_cnf"]) != cnf:
            raise AssertionError("semantic CNF path mismatch")
        cnf_hash = sha256(cnf)
        if cnf_hash != row["final_cnf_sha256"]:
            raise AssertionError("producer CNF hash mismatch")
        if cnf_hash != semantic_row["final_cnf_sha256"]:
            raise AssertionError("semantic CNF hash mismatch")

        prefix = args.proof_dir / f"orbit_{index:02d}"
        proof = prefix.with_suffix(".drat")
        kissat_stdout = prefix.with_suffix(".kissat.stdout.log")
        kissat_stderr = prefix.with_suffix(".kissat.stderr.log")
        trim_stdout = prefix.with_suffix(".drat_trim.stdout.log")
        trim_stderr = prefix.with_suffix(".drat_trim.stderr.log")
        kissat_command = (
            f"'{wsl_path(args.kissat)}' --sat --force "
            f"'{wsl_path(cnf)}' '{wsl_path(proof)}'"
        )
        kissat_code, solve_seconds = run(
            kissat_command, kissat_stdout, kissat_stderr
        )
        kissat_text = kissat_stdout.read_text(
            encoding="utf-8", errors="replace"
        )
        if kissat_code != 20 or "s UNSATISFIABLE" not in kissat_text:
            raise AssertionError(f"Kissat failed on orbit {index}")
        trim_command = (
            f"'{wsl_path(args.drat_trim)}' "
            f"'{wsl_path(cnf)}' '{wsl_path(proof)}' -f -w"
        )
        trim_code, verify_seconds = run(
            trim_command, trim_stdout, trim_stderr
        )
        trim_text = trim_stdout.read_text(
            encoding="utf-8", errors="replace"
        )
        if trim_code != 0 or "s VERIFIED" not in trim_text:
            raise AssertionError(f"drat-trim failed on orbit {index}")
        checks.append(
            {
                "orbit_index": index,
                "cnf": str(cnf),
                "cnf_sha256": cnf_hash,
                "proof": str(proof),
                "proof_bytes": proof.stat().st_size,
                "proof_sha256": sha256(proof),
                "kissat_stdout": str(kissat_stdout),
                "kissat_stdout_sha256": sha256(kissat_stdout),
                "drat_trim_stdout": str(trim_stdout),
                "drat_trim_stdout_sha256": sha256(trim_stdout),
                "solve_seconds": solve_seconds,
                "verify_seconds": verify_seconds,
                "verified": True,
            }
        )
        print(
            f"orbit={index + 1}/23 proof={proof.stat().st_size} "
            f"verified",
            flush=True,
        )

    payload = {
        "verified": True,
        "scope": (
            "proof-producing SAT decisions and independent DRAT replay "
            "for all 23 unary cycle-relation factor CNFs"
        ),
        "producer": str(args.producer),
        "producer_sha256": sha256(args.producer),
        "semantic": str(args.semantic),
        "semantic_sha256": sha256(args.semantic),
        "kissat": str(args.kissat),
        "kissat_sha256": sha256(args.kissat),
        "drat_trim": str(args.drat_trim),
        "drat_trim_sha256": sha256(args.drat_trim),
        "orbits": len(checks),
        "proof_bytes": sum(int(row["proof_bytes"]) for row in checks),
        "checks": checks,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "checks"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
