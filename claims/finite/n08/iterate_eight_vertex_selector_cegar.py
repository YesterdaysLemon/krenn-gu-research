"""Iterate catalogue-selector SAT models through exact Laurent CEGAR."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])


import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from eight_vertex_native_kissat_laurent_batch import run_kissat


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def checked_run(arguments: list[str], stdout: Path, stderr: Path) -> None:
    with stdout.open("wb") as output, stderr.open("wb") as errors:
        result = subprocess.run(
            [sys.executable, *arguments],
            check=False,
            stdout=output,
            stderr=errors,
        )
    if result.returncode:
        raise RuntimeError(
            f"{arguments[0]} returned {result.returncode}; "
            f"see {stdout} and {stderr}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--target-edges", type=int, required=True)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        required=True,
    )
    parser.add_argument("--expected-roles", type=int, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument(
        "--configuration",
        choices=("default", "sat", "unsat"),
        default="sat",
    )
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument(
        "--prefer-transport",
        action="store_true",
        help="try elementary transport certificates before Laurent reduction",
    )
    parser.add_argument("--start-round", type=int, default=1)
    parser.add_argument("--max-rounds", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    current_base = args.base_cnf
    rows: list[dict[str, object]] = []
    payload: dict[str, object] = {
        "status": "running",
        "target_edges": args.target_edges,
        "center_degree": args.center_degree,
        "expected_roles": args.expected_roles,
        "graph6": str(args.graph6),
        "graph6_sha256": sha256(args.graph6),
        "initial_base_cnf": str(args.base_cnf),
        "initial_base_cnf_sha256": sha256(args.base_cnf),
        "prefer_transport": args.prefer_transport,
        "rounds": rows,
    }
    checkpoint(args.output, payload)

    for round_index in range(
        args.start_round,
        args.start_round + args.max_rounds,
    ):
        stem = Path(f"{args.prefix}_round{round_index:02d}")
        selector = stem.with_name(stem.name + "_selector.cnf")
        selector_manifest = stem.with_name(
            stem.name + "_selector.json"
        )
        build_stdout = stem.with_name(
            stem.name + "_selector_build.stdout.log"
        )
        build_stderr = stem.with_name(
            stem.name + "_selector_build.stderr.log"
        )
        checked_run(
            [
                str(HERE / "eight_vertex_16edge_catalogue_cnf.py"),
                "--graph6",
                str(args.graph6),
                "--target-edges",
                str(args.target_edges),
                "--center-degree",
                str(args.center_degree),
                "--expected-roles",
                str(args.expected_roles),
                "--base-cnf",
                str(current_base),
                "--output",
                str(selector),
                "--manifest",
                str(selector_manifest),
            ],
            build_stdout,
            build_stderr,
        )

        solver_log = stem.with_name(
            stem.name + "_kissat.log"
        )
        solver_stderr = stem.with_name(
            stem.name + "_kissat.stderr.log"
        )
        status, solve_seconds = run_kissat(
            args.kissat,
            selector,
            solver_log,
            solver_stderr,
            args.configuration,
        )
        row: dict[str, object] = {
            "round": round_index,
            "input_base_cnf": str(current_base),
            "input_base_cnf_sha256": sha256(current_base),
            "selector_manifest": str(selector_manifest),
            "selector_manifest_sha256": sha256(selector_manifest),
            "selector_cnf": str(selector),
            "selector_cnf_sha256": sha256(selector),
            "solver_log": str(solver_log),
            "solver_log_sha256": sha256(solver_log),
            "solver_stderr": str(solver_stderr),
            "solver_stderr_sha256": sha256(solver_stderr),
            "solve_seconds": solve_seconds,
            "solver_status": status,
        }
        rows.append(row)
        if status == "UNSAT":
            payload.update(
                {
                    "status": "complete",
                    "final_base_cnf": str(current_base),
                    "final_base_cnf_sha256": sha256(current_base),
                    "final_selector_cnf": str(selector),
                    "final_selector_cnf_sha256": sha256(selector),
                    "rounds": rows,
                }
            )
            checkpoint(args.output, payload)
            print(
                f"round={round_index} selector=UNSAT complete",
                flush=True,
            )
            return

        next_base = stem.with_name(stem.name + "_learned.cnf")
        conflict_manifest = stem.with_name(
            stem.name + "_laurent.json"
        )
        learn_stdout = stem.with_name(
            stem.name + "_laurent.stdout.log"
        )
        learn_stderr = stem.with_name(
            stem.name + "_laurent.stderr.log"
        )
        checked_run(
            [
                str(REPO_ROOT / "src/krenn_gu/eight_vertex_degree4_cegar.py"),
                "--model",
                str(solver_log),
                "--center-degree",
                str(args.center_degree),
                "--base-cnf",
                str(current_base),
                "--output-cnf",
                str(next_base),
                "--manifest",
                str(conflict_manifest),
                *(
                    ["--prefer-transport"]
                    if args.prefer_transport
                    else []
                ),
            ],
            learn_stdout,
            learn_stderr,
        )
        row.update(
            {
                "laurent_manifest": str(conflict_manifest),
                "laurent_manifest_sha256": sha256(
                    conflict_manifest
                ),
                "output_base_cnf": str(next_base),
                "output_base_cnf_sha256": sha256(next_base),
            }
        )
        current_base = next_base
        payload.update(
            {
                "status": "running",
                "final_base_cnf": str(current_base),
                "final_base_cnf_sha256": sha256(current_base),
                "rounds": rows,
            }
        )
        checkpoint(args.output, payload)
        print(
            f"round={round_index} selector=SAT learned=1",
            flush=True,
        )

    payload.update(
        {
            "status": "max_rounds_reached",
            "final_base_cnf": str(current_base),
            "final_base_cnf_sha256": sha256(current_base),
            "rounds": rows,
        }
    )
    checkpoint(args.output, payload)
    raise RuntimeError("selector CEGAR reached --max-rounds")


if __name__ == "__main__":
    main()
