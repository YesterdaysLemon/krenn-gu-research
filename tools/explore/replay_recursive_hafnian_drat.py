"""Replay the experimental recursive-hafnian DRAT manifest.

Run this script under Linux or WSL with an independently supplied drat-trim
binary.  It verifies exact input identities before invoking the checker and
writes a durable receipt.  Passing this replay checks only the listed CNF/DRAT
pairs; the mathematical bridge and symmetry cover remain separate obligations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


def identity(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            size += len(chunk)
            digest.update(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_identity(
    path: Path,
    expected: dict[str, object],
    label: str,
) -> dict[str, object]:
    actual = identity(path)
    expected_identity = {
        "bytes": expected["bytes"],
        "sha256": expected["sha256"],
    }
    require(actual == expected_identity, f"{label}: byte identity differs")
    return actual


def invoke(
    checker: Path,
    cnf: Path,
    proof: Path,
    log: Path,
    timeout_seconds: float,
    *,
    binary: bool,
) -> dict[str, object]:
    command = [str(checker), str(cnf), str(proof)]
    if binary:
        command.append("-i")
    started = time.monotonic()
    timed_out = False
    with log.open("wb") as handle:
        try:
            completed = subprocess.run(
                command,
                stdout=handle,
                stderr=subprocess.STDOUT,
                timeout=timeout_seconds,
                check=False,
            )
            exit_code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            exit_code = None
    raw_log = log.read_bytes()
    lines = raw_log.decode("utf-8", errors="replace").splitlines()
    exact_verified = "s VERIFIED" in lines
    exact_rejected = "s NOT VERIFIED" in lines
    return {
        "command": command,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "seconds": round(time.monotonic() - started, 6),
        "exact_verified_line": exact_verified,
        "exact_not_verified_line": exact_rejected,
        "accepted": (
            not timed_out
            and exit_code == 0
            and exact_verified
            and not exact_rejected
        ),
        "log": str(log),
        "log_identity": identity(log),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--case-timeout-seconds", type=float, default=300.0)
    args = parser.parse_args()

    require(os.name == "posix", "run the replay under Linux or WSL")
    require(
        0 < args.case_timeout_seconds <= 900,
        "case timeout must be in (0, 900] seconds",
    )
    manifest_path = args.manifest.resolve()
    artifact_dir = args.artifact_dir.resolve()
    checker = args.checker.resolve()
    output_dir = args.output_dir.resolve()
    require(not output_dir.exists(), "output directory must be new")
    require(artifact_dir.is_dir(), "artifact directory does not exist")
    require(checker.is_file(), "checker does not exist")
    output_dir.mkdir(parents=True)

    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    require(
        manifest.get("schema") == "recursive-hafnian-rzp-drat-v1",
        "unexpected manifest schema",
    )
    require(manifest.get("proof_format") == "binary DRAT", "wrong format")
    expected_checker = manifest["checker"]["sha256"]
    checker_identity = identity(checker)
    require(
        checker_identity["sha256"] == expected_checker,
        "checker binary hash differs",
    )

    case_specs = manifest["cases"]
    case_ids = [case["id"] for case in case_specs]
    require(len(case_ids) == len(set(case_ids)), "duplicate case id")
    require(len(case_ids) == 13, "the n=10 cover must have 13 proof cases")

    receipt_path = output_dir / "replay.json"
    receipt: dict[str, object] = {
        "schema": "recursive-hafnian-rzp-drat-replay-v1",
        "status": "HOLD",
        "scope": manifest["scope"],
        "started": time.time(),
        "driver_identity": identity(Path(__file__).resolve()),
        "manifest": {
            "path": str(manifest_path),
            "identity": {
                "bytes": len(manifest_raw),
                "sha256": hashlib.sha256(manifest_raw).hexdigest(),
            },
        },
        "checker": {"path": str(checker), "identity": checker_identity},
        "controls": [],
        "cases": [],
    }

    def save() -> None:
        receipt_path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    try:
        save()
        controls = [
            (
                "valid-proof",
                "p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n",
                "1 0\n0\n",
                True,
            ),
            (
                "invalid-empty-step",
                "p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n",
                "0\n",
                False,
            ),
            (
                "satisfiable-false-proof",
                "p cnf 2 2\n1 2 0\n-1 2 0\n",
                "0\n",
                False,
            ),
        ]
        with tempfile.TemporaryDirectory(
            prefix="controls-",
            dir=output_dir,
        ) as temporary_name:
            temporary = Path(temporary_name)
            for control_id, cnf_text, proof_text, expected in controls:
                cnf = temporary / f"{control_id}.cnf"
                proof = temporary / f"{control_id}.drat"
                cnf.write_text(cnf_text, encoding="ascii")
                proof.write_text(proof_text, encoding="ascii")
                result = invoke(
                    checker,
                    cnf,
                    proof,
                    output_dir / f"control-{control_id}.log",
                    args.case_timeout_seconds,
                    binary=False,
                )
                passed = (
                    not result["timed_out"]
                    and result["accepted"] == expected
                    and (expected or result["exit_code"] != 0)
                )
                result.update(
                    id=control_id,
                    expected_acceptance=expected,
                    status="PASS" if passed else "FAIL",
                )
                receipt["controls"].append(result)
                save()
            require(
                all(row["status"] == "PASS" for row in receipt["controls"]),
                "checker controls failed",
            )

        for spec in case_specs:
            case_id = spec["id"]
            cnf = (artifact_dir / spec["cnf"]["file"]).resolve()
            proof = (artifact_dir / spec["proof"]["file"]).resolve()
            require(cnf.parent == artifact_dir, f"{case_id}: CNF leaves root")
            require(
                proof.parent == artifact_dir,
                f"{case_id}: proof leaves artifact root",
            )
            row: dict[str, object] = {
                "id": case_id,
                "cover_role": spec["cover_role"],
                "status": "RUNNING",
                "cnf": {
                    "path": str(cnf),
                    "identity": check_identity(cnf, spec["cnf"], case_id),
                },
                "proof": {
                    "path": str(proof),
                    "identity": check_identity(
                        proof,
                        spec["proof"],
                        case_id,
                    ),
                },
            }
            receipt["cases"].append(row)
            save()
            result = invoke(
                checker,
                cnf,
                proof,
                output_dir / f"case-{case_id}.log",
                args.case_timeout_seconds,
                binary=True,
            )
            stable = (
                identity(cnf) == row["cnf"]["identity"]
                and identity(proof) == row["proof"]["identity"]
            )
            row.update(
                result=result,
                input_bytes_stable=stable,
                status="PASS" if result["accepted"] and stable else "FAIL",
            )
            save()
            print(
                json.dumps({"id": case_id, "status": row["status"]}),
                flush=True,
            )
            require(row["status"] == "PASS", f"{case_id}: replay failed")

        receipt.update(
            status="PASS",
            verified_count=len(case_specs),
            finished=time.time(),
        )
        save()
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "verified_count": len(case_specs),
                    "receipt": str(receipt_path),
                    "receipt_identity": identity(receipt_path),
                }
            ),
            flush=True,
        )
    except BaseException as error:
        receipt.update(status="HOLD", error=repr(error), finished=time.time())
        save()
        raise


if __name__ == "__main__":
    main()
