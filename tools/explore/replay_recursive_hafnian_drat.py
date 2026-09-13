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
import sys as _bootstrap_sys
import tempfile
import time
from pathlib import Path

for _bootstrap_parent in Path(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import pysat  # noqa: E402

from krenn_gu.recursive_hafnian_support import (  # noqa: E402
    build_recursive_hafnian_support_cnf,
)

CYCLE_TYPES = (
    (5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1),
    (2, 1, 1, 1), (1, 1, 1, 1, 1),
)


def expected_cover() -> dict[str, dict[str, object]]:
    """The six nonshared branches and seven shared-branch refinements."""

    result = {}
    for cycle in CYCLE_TYPES[:-1]:
        label = "p".join(map(str, cycle))
        result[f"top-{label}"] = {
            "n": 10,
            "matching_cycle_type": list(cycle),
            "third_matching_cycle_type": None,
            "two_part_only": False,
            "no_singleton_cancellation": False,
        }
    for cycle in CYCLE_TYPES:
        label = "shared" if cycle == CYCLE_TYPES[-1] else "p".join(map(str, cycle))
        result[f"shared-third-{label}"] = {
            "n": 10,
            "matching_cycle_type": list(CYCLE_TYPES[-1]),
            "third_matching_cycle_type": list(cycle),
            "two_part_only": False,
            "no_singleton_cancellation": False,
        }
    return result


def validate_cover(case_specs: list[dict[str, object]]) -> None:
    expected = expected_cover()
    ids = [spec["id"] for spec in case_specs]
    require(len(ids) == len(set(ids)), "duplicate case id")
    require(set(ids) == set(expected), "not the exhaustive 13-case cover")
    for spec in case_specs:
        # JSON text comparison also distinguishes false from 0 and true from 1.
        require(
            json.dumps(spec["parameters"], sort_keys=True)
            == json.dumps(expected[spec["id"]], sort_keys=True),
            f"{spec['id']}: parameters do not implement its cover branch",
        )


def normalized_source_identity(path: Path) -> dict[str, object]:
    """Pin source text independently of Git checkout LF/CRLF conversion."""

    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def regenerate_cnf(parameters: dict[str, object], output: Path) -> dict[str, object]:
    """Reproduce the original Windows DIMACS bytes explicitly on any OS."""

    third = parameters["third_matching_cycle_type"]
    instance = build_recursive_hafnian_support_cnf(
        parameters["n"],
        matching_cycle_type=tuple(parameters["matching_cycle_type"]),
        third_matching_cycle_type=tuple(third) if third is not None else None,
        two_part_only=parameters["two_part_only"],
        no_singleton_cancellation=parameters["no_singleton_cancellation"],
    )
    text = instance.cnf.to_dimacs() + "\n"
    output.write_bytes(text.replace("\n", "\r\n").encode("ascii"))
    return {
        "variables": instance.cnf.nv,
        "clauses": len(instance.cnf.clauses),
        "identity": identity(output),
    }


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
        "semantic_conflict_rejection": any(
            "conflict claimed, but not detected" in line for line in lines
        ),
        "binary_parser_failure": any("wrong binary prefix" in line for line in lines),
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
        manifest.get("schema") == "recursive-hafnian-rzp-drat-v2",
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
    validate_cover(case_specs)
    generator = manifest["generator"]
    require(pysat.__version__ == generator["python_sat_version"], "python-sat version differs")
    require(generator["dimacs_serialization"] == "ASCII, CRLF, final CRLF", "unknown serialization")
    source = (REPO_ROOT / generator["source"]["file"]).resolve()
    require(source == REPO_ROOT / "src/krenn_gu/recursive_hafnian_support.py", "wrong builder path")
    source_identity = normalized_source_identity(source)
    require(
        source_identity == {key: generator["source"][key] for key in ("bytes", "sha256")},
        "builder source hash differs",
    )

    receipt_path = output_dir / "replay.json"
    receipt: dict[str, object] = {
        "schema": "recursive-hafnian-rzp-drat-replay-v2",
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
        "generator": {
            "source": str(source),
            "normalized_source_identity": source_identity,
            "python_sat_version": pysat.__version__,
            "dimacs_serialization": generator["dimacs_serialization"],
        },
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
                b"a\x02\x00a\x00",
                True,
            ),
            (
                "invalid-empty-step",
                "p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n",
                b"a\x00",
                False,
            ),
            (
                "satisfiable-false-proof",
                "p cnf 2 2\n1 2 0\n-1 2 0\n",
                b"a\x00",
                False,
            ),
        ]
        with tempfile.TemporaryDirectory(
            prefix="controls-",
            dir=output_dir,
        ) as temporary_name:
            temporary = Path(temporary_name)
            for control_id, cnf_text, proof_bytes, expected in controls:
                cnf = temporary / f"{control_id}.cnf"
                proof = temporary / f"{control_id}.drat"
                cnf.write_text(cnf_text, encoding="ascii")
                proof.write_bytes(proof_bytes)
                result = invoke(
                    checker,
                    cnf,
                    proof,
                    output_dir / f"control-{control_id}.log",
                    args.case_timeout_seconds,
                    binary=True,
                )
                passed = (
                    not result["timed_out"]
                    and result["accepted"] == expected
                    and (expected or result["exit_code"] != 0)
                    and not result["binary_parser_failure"]
                    and (expected or (
                        result["exact_not_verified_line"]
                        and result["semantic_conflict_rejection"]
                    ))
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
            rebuilt = output_dir / f"regenerated-{case_id}.cnf"
            regeneration = regenerate_cnf(spec["parameters"], rebuilt)
            check_identity(rebuilt, spec["cnf"], f"{case_id}: regeneration")
            row: dict[str, object] = {
                "id": case_id,
                "cover_role": spec["cover_role"],
                "parameters": spec["parameters"],
                "regeneration": regeneration,
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

        require(identity(checker) == checker_identity, "checker changed during replay")
        require(manifest_path.read_bytes() == manifest_raw, "manifest changed during replay")
        require(normalized_source_identity(source) == source_identity, "builder changed during replay")
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
