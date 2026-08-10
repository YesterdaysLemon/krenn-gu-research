"""Iterate exact Singular support blockers until a role batch closes.

Each input batch must have completed with ``exact_fallback_required``.
Every fallback torus is rebuilt, reduced, and sent to Singular.  Only when
all reduced ideals have the verified unit terminal are their full-support
symmetry no-goods appended.  The complete catalogue is then rerun.  The
loop stops on zero fallbacks or fails closed on any command or certificate
error.
"""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


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


def wsl_path(path: Path) -> str:
    resolved = str(path.resolve())
    if len(resolved) < 3 or resolved[1:3] != ":\\":
        raise ValueError(f"cannot map path into WSL: {resolved}")
    return (
        f"/mnt/{resolved[0].lower()}/"
        + resolved[3:].replace("\\", "/")
    )


def run_python(
    arguments: list[str], stdout: Path, stderr: Path
) -> None:
    with stdout.open("wb") as output, stderr.open("wb") as errors:
        result = subprocess.run(
            [sys.executable, *arguments],
            check=False,
            stdout=output,
            stderr=errors,
        )
    if result.returncode:
        raise RuntimeError(
            f"{arguments[0]} failed with code {result.returncode}; "
            f"see {stdout} and {stderr}"
        )


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument(
        "--prefix",
        type=Path,
        required=True,
        help="artifact prefix; round numbers are appended",
    )
    parser.add_argument("--start-round", type=int, default=1)
    parser.add_argument("--max-rounds", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--role-index",
        type=int,
        action="append",
        help=(
            "forward a zero-based canonical role to targeted catalogue "
            "passes; repeat as needed"
        ),
    )
    parser.add_argument(
        "--fallback-limit",
        type=int,
        default=1,
        help=(
            "forward the per-role fallback enumeration limit to each "
            "catalogue rerun"
        ),
    )
    args = parser.parse_args()
    if args.fallback_limit < 1:
        raise ValueError("--fallback-limit must be positive")

    current_batch_path = args.batch
    rounds: list[dict[str, object]] = []
    args.prefix.parent.mkdir(parents=True, exist_ok=True)

    for offset in range(args.max_rounds):
        round_number = args.start_round + offset
        current_batch = json.loads(
            current_batch_path.read_text(encoding="utf-8")
        )
        if current_batch["status"] in ("complete", "subset_complete"):
            break
        if current_batch["status"] != "exact_fallback_required":
            raise AssertionError(
                "input batch is neither complete nor an exact fallback"
            )
        fallback_count = int(current_batch["fallback_count"])
        if fallback_count <= 0:
            raise AssertionError(
                "fallback batch has no recorded fallbacks"
            )
        center_degree = int(current_batch["center_degree"])
        target_edges = current_batch.get("target_edges")
        fixed_assumptions = tuple(
            map(int, current_batch.get("fixed_assumptions", []))
        )
        learned_base = Path(str(current_batch["learned_cnf"]))
        if sha256(learned_base) != current_batch[
            "learned_cnf_sha256"
        ]:
            raise AssertionError("input batch learned CNF hash changed")

        stem = Path(f"{args.prefix}_round{round_number:02d}")
        fallback_dir = Path(f"{stem}_singular")
        fallback_manifest = Path(f"{stem}_singular.json")
        generate_stdout = Path(f"{stem}_generate.stdout.log")
        generate_stderr = Path(f"{stem}_generate.stderr.log")
        run_python(
            [
                str(HERE / "generate_batch_fallback_singular.py"),
                "--batch",
                str(current_batch_path),
                "--output-dir",
                str(fallback_dir),
                "--manifest",
                str(fallback_manifest),
            ],
            generate_stdout,
            generate_stderr,
        )
        generated = json.loads(
            fallback_manifest.read_text(encoding="utf-8")
        )
        if int(generated["fallbacks"]) != fallback_count:
            raise AssertionError(
                "fallback generator changed the fallback count"
            )

        for program in generated["programs"]:
            program_path = Path(str(program["program"]))
            command = f"Singular -q '{wsl_path(program_path)}'"
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
                capture_output=True,
            )
            log = program_path.with_suffix(".log")
            stderr = program_path.with_suffix(".stderr.log")
            log.write_bytes(result.stdout)
            stderr.write_bytes(result.stderr)
            if result.returncode:
                raise RuntimeError(
                    f"Singular failed for {program_path} with "
                    f"code {result.returncode}"
                )

        exact_cnf = Path(f"{stem}.cnf")
        exact_manifest = Path(f"{stem}.json")
        learn_stdout = Path(f"{stem}_learn.stdout.log")
        learn_stderr = Path(f"{stem}_learn.stderr.log")
        run_python(
            [
                str(HERE / "learn_singular_fallback_clauses.py"),
                "--fallback-manifest",
                str(fallback_manifest),
                "--base-cnf",
                str(learned_base),
                "--output-cnf",
                str(exact_cnf),
                "--manifest",
                str(exact_manifest),
            ],
            learn_stdout,
            learn_stderr,
        )

        next_batch = Path(f"{stem}_batch.json")
        next_learned_cnf = Path(f"{stem}_laurent.cnf")
        next_learned_manifest = Path(f"{stem}_laurent.json")
        batch_stdout = Path(f"{stem}_batch.stdout.log")
        batch_stderr = Path(f"{stem}_batch.stderr.log")
        batch_arguments = [
            str(HERE / "eight_vertex_skeleton_laurent_batch.py"),
            "--graph6",
            str(args.graph6),
            "--center-degree",
            str(center_degree),
            "--cnf",
            str(exact_cnf),
            "--output",
            str(next_batch),
            "--learned-cnf",
            str(next_learned_cnf),
            "--learned-manifest",
            str(next_learned_manifest),
        ]
        if target_edges is not None:
            batch_arguments.extend(
                ["--target-edges", str(int(target_edges))]
            )
        for role_index in args.role_index or []:
            batch_arguments.extend(
                ["--role-index", str(role_index)]
            )
        for literal in fixed_assumptions:
            batch_arguments.extend(
                ["--assumption", str(literal)]
            )
        if args.fallback_limit != 1:
            batch_arguments.extend(
                ["--fallback-limit", str(args.fallback_limit)]
            )
        run_python(
            batch_arguments, batch_stdout, batch_stderr
        )
        next_payload = json.loads(
            next_batch.read_text(encoding="utf-8")
        )
        round_payload = {
            "round": round_number,
            "input_batch": str(current_batch_path),
            "input_batch_sha256": sha256(current_batch_path),
            "fallbacks": fallback_count,
            "fallback_manifest": str(fallback_manifest),
            "fallback_manifest_sha256": sha256(
                fallback_manifest
            ),
            "exact_manifest": str(exact_manifest),
            "exact_manifest_sha256": sha256(exact_manifest),
            "output_batch": str(next_batch),
            "output_batch_sha256": sha256(next_batch),
            "output_status": next_payload["status"],
            "output_support_models": int(
                next_payload["support_models"]
            ),
            "output_laurent_conflicts": int(
                next_payload["laurent_conflicts"]
            ),
            "output_fallbacks": int(
                next_payload["fallback_count"]
            ),
            "fixed_assumptions": list(fixed_assumptions),
        }
        rounds.append(round_payload)
        current_batch_path = next_batch
        checkpoint(
            args.output,
            {
                "status": (
                    "complete"
                    if next_payload["status"]
                    in ("complete", "subset_complete")
                    else "running"
                ),
                "center_degree": center_degree,
                "target_edges": target_edges,
                "fixed_assumptions": list(fixed_assumptions),
                "rounds": rounds,
                "final_batch": str(current_batch_path),
                "final_batch_sha256": sha256(
                    current_batch_path
                ),
            },
        )
        print(
            f"round={round_number} input_fallbacks={fallback_count} "
            f"output={next_payload['status']} "
            f"models={next_payload['support_models']} "
            f"conflicts={next_payload['laurent_conflicts']} "
            f"fallbacks={next_payload['fallback_count']}",
            flush=True,
        )
        if next_payload["status"] in (
            "complete",
            "subset_complete",
        ):
            break
    else:
        raise RuntimeError(
            f"did not close after {args.max_rounds} exact rounds"
        )

    final = json.loads(
        current_batch_path.read_text(encoding="utf-8")
    )
    if final["status"] not in ("complete", "subset_complete"):
        raise RuntimeError("exact CEGAR loop stopped without closure")
    checkpoint(
        args.output,
        {
            "status": final["status"],
            "center_degree": int(final["center_degree"]),
            "target_edges": final.get("target_edges"),
            "fixed_assumptions": final.get(
                "fixed_assumptions", []
            ),
            "selected_role_indices": final.get(
                "selected_role_indices"
            ),
            "rounds": rounds,
            "final_batch": str(current_batch_path),
            "final_batch_sha256": sha256(current_batch_path),
            "final_learned_cnf": final["learned_cnf"],
            "final_learned_cnf_sha256": final[
                "learned_cnf_sha256"
            ],
        },
    )
    print(
        f"complete final_batch={current_batch_path} "
        f"rounds={len(rounds)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
