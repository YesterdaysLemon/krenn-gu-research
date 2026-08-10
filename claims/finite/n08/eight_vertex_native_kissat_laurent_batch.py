"""Native Kissat plus exact Laurent CEGAR over an n=8 role catalogue.

Kissat deliberately has no incremental assumptions interface.  This driver
materializes one canonical skeleton at a time, invokes the native solver,
and learns exact Laurent support no-goods globally.  It is a portfolio
alternative for instances on which the incremental CaDiCaL backend spends a
long time before finding its first support.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

from krenn_gu.eight_vertex_degree4_cegar import (
    full_equations,
    laurent_conflict,
    symmetry_clauses,
    write_augmented_cnf,
)
from eight_vertex_skeleton_batch import (
    canonical_degree_three_role_skeletons,
    canonical_minimum_five_skeletons,
    canonical_normalized_killer_skeletons,
    canonical_role_skeletons,
    ordered_role_skeletons,
)
from eight_vertex_skeleton_laurent_batch import (
    local_positive_to_flat,
)
from krenn_gu.eight_vertex_sparse_exact import (
    local_allowed_edges,
    positive_model_literals,
)
from krenn_gu.search_witness import EquationSystem


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


def wsl_path(path: Path) -> str:
    resolved = str(path.resolve())
    if len(resolved) < 3 or resolved[1:3] != ":\\":
        raise ValueError(f"cannot map path into WSL: {resolved}")
    drive = resolved[0].lower()
    tail = resolved[3:].replace("\\", "/")
    return f"/mnt/{drive}/{tail}"


def run_kissat(
    binary: Path,
    cnf: Path,
    log: Path,
    stderr: Path,
    configuration: str,
) -> tuple[str, float]:
    command = (
        f"'{wsl_path(binary)}' --{configuration} "
        f"'{wsl_path(cnf)}'"
    )
    started = time.perf_counter()
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
    elapsed = time.perf_counter() - started
    log.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    text = result.stdout.decode("ascii", errors="strict")
    if result.returncode == 10 and "s SATISFIABLE" in text:
        return "SAT", elapsed
    if result.returncode == 20 and "s UNSATISFIABLE" in text:
        return "UNSAT", elapsed
    raise RuntimeError(
        f"Kissat returned {result.returncode} without a valid terminal; "
        f"see {log} and {stderr}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--target-edges", type=int)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        required=True,
    )
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument(
        "--configuration",
        choices=("default", "sat", "unsat"),
        default="default",
    )
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--learned-cnf", type=Path, required=True)
    parser.add_argument("--learned-manifest", type=Path, required=True)
    parser.add_argument(
        "--prefer-transport",
        action="store_true",
        help=(
            "try elementary transport/rectangle certificates "
            "before Laurent reduction"
        ),
    )
    args = parser.parse_args()

    builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[args.center_degree]
    catalogue_started = time.perf_counter()
    roles, catalogue = builder(
        args.graph6, target_edges=args.target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    catalogue_seconds = time.perf_counter() - catalogue_started

    args.work_dir.mkdir(parents=True, exist_ok=True)
    work_cnf = args.work_dir / "current_role.cnf"
    allowed = local_allowed_edges(args.center_degree)
    first_block_variable = 1 + 9 * len(allowed)
    system = EquationSystem(8, 3)
    equations, names, name_to_flat = full_equations(system)

    learned: set[tuple[int, ...]] = set()
    conflicts: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    support_models = 0
    fallback_count = 0
    solve_started = time.perf_counter()
    binary_hash = sha256(args.kissat)
    print(
        f"catalogue roles={len(ordered_roles)} "
        f"first_edges={len(ordered_roles[0]) if ordered_roles else 0} "
        f"last_edges={len(ordered_roles[-1]) if ordered_roles else 0}",
        flush=True,
    )

    for role_index, skeleton in enumerate(ordered_roles):
        present = set(skeleton)
        units = [
            (
                first_block_variable + edge_index
                if edge in present
                else -(first_block_variable + edge_index)
            ,)
            for edge_index, edge in enumerate(allowed)
        ]
        role_started = time.perf_counter()
        role_models = 0
        role_conflicts: list[int] = []
        solver_runs: list[dict[str, object]] = []
        status = "UNSAT"
        fallback: dict[str, object] | None = None

        while True:
            write_augmented_cnf(
                args.base_cnf,
                work_cnf,
                [*sorted(learned), *units],
            )
            run_index = len(solver_runs)
            log = args.work_dir / (
                f"role_{role_index:04d}_run_{run_index:03d}.log"
            )
            stderr = log.with_suffix(".stderr.log")
            solver_status, elapsed = run_kissat(
                args.kissat,
                work_cnf,
                log,
                stderr,
                args.configuration,
            )
            solver_runs.append(
                {
                    "run_index": run_index,
                    "status": solver_status,
                    "cnf_sha256": sha256(work_cnf),
                    "log": str(log),
                    "log_sha256": sha256(log),
                    "stderr": str(stderr),
                    "stderr_sha256": sha256(stderr),
                    "solve_seconds": elapsed,
                }
            )
            if solver_status == "UNSAT":
                break

            model = sorted(positive_model_literals(log))
            selected = local_positive_to_flat(
                system, model, args.center_degree
            )
            support_models += 1
            role_models += 1
            try:
                positive, negative, metadata = laurent_conflict(
                    system,
                    equations,
                    names,
                    name_to_flat,
                    selected,
                    center_degree=args.center_degree,
                    prefer_transport=args.prefer_transport,
                )
            except (RuntimeError, ValueError) as error:
                status = "EXACT_FALLBACK"
                fallback_count += 1
                fallback = {
                    "reason": str(error),
                    "selected_entries": len(selected),
                    "selected_flat_indices": sorted(selected),
                    "positive_entry_variables": [
                        literal
                        for literal in model
                        if 0 < literal <= 9 * len(allowed)
                    ],
                }
                break

            images = symmetry_clauses(
                system,
                positive,
                negative,
                center_degree=args.center_degree,
            )
            new_clauses = [
                clause for clause in images if clause not in learned
            ]
            if not new_clauses:
                raise AssertionError(
                    "SAT model yielded no new Laurent conflict"
                )
            conflict_index = len(conflicts)
            role_conflicts.append(conflict_index)
            conflicts.append(
                {
                    "conflict_index": conflict_index,
                    "role_index": role_index,
                    **metadata,
                    "positive_entries": sorted(positive),
                    "negative_entries": sorted(negative),
                    "cube_size": len(positive) + len(negative),
                    "symmetry_images": len(images),
                    "new_clauses": len(new_clauses),
                }
            )
            learned.update(new_clauses)
            print(
                f"role={role_index + 1}/{len(ordered_roles)} "
                f"model={role_models} conflict={len(conflicts)} "
                f"clauses={len(learned)}",
                flush=True,
            )

        row: dict[str, object] = {
            "role_index": role_index,
            "skeleton_edges": [list(edge) for edge in skeleton],
            "status": status,
            "support_models": role_models,
            "conflict_indices": role_conflicts,
            "solver_runs": solver_runs,
            "solve_seconds": time.perf_counter() - role_started,
        }
        if fallback is not None:
            row["fallback"] = fallback
        rows.append(row)
        print(
            f"processed={role_index + 1}/{len(ordered_roles)} "
            f"status={status} models={support_models} "
            f"conflicts={len(conflicts)} fallbacks={fallback_count}",
            flush=True,
        )
        checkpoint(
            args.output,
            {
                "status": "running",
                **catalogue,
                "target_edges": args.target_edges,
                "center_degree": args.center_degree,
                "catalogue_seconds": catalogue_seconds,
                "solver": "native_kissat",
                "kissat": str(args.kissat),
                "kissat_sha256": binary_hash,
                "configuration": args.configuration,
                "prefer_transport": args.prefer_transport,
                "cnf": str(args.base_cnf),
                "processed": len(rows),
                "support_models": support_models,
                "laurent_conflicts": len(conflicts),
                "transport_conflicts": sum(
                    conflict.get("certificate_kind")
                    == "cancellation_transport"
                    for conflict in conflicts
                ),
                "learned_clauses": len(learned),
                "fallback_count": fallback_count,
                "rows": rows,
                "conflicts": conflicts,
            },
        )

    ordered_learned = sorted(learned)
    write_augmented_cnf(
        args.base_cnf, args.learned_cnf, ordered_learned
    )
    learned_payload = {
        "scope": (
            "exact Laurent support no-goods learned by native "
            "Kissat over the n=8 role catalogue"
        ),
        "center_degree": args.center_degree,
        "prefer_transport": args.prefer_transport,
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "learned_cnf": str(args.learned_cnf),
        "learned_cnf_sha256": sha256(args.learned_cnf),
        "support_models": support_models,
        "laurent_conflicts": len(conflicts),
        "transport_conflicts": sum(
            conflict.get("certificate_kind") == "cancellation_transport"
            for conflict in conflicts
        ),
        "learned_clauses": [
            list(clause) for clause in ordered_learned
        ],
        "conflicts": conflicts,
    }
    checkpoint(args.learned_manifest, learned_payload)

    payload = {
        "status": (
            "complete"
            if fallback_count == 0
            else "exact_fallback_required"
        ),
        **catalogue,
        "target_edges": args.target_edges,
        "center_degree": args.center_degree,
        "catalogue_seconds": catalogue_seconds,
        "solver": "native_kissat",
        "kissat": str(args.kissat),
        "kissat_sha256": binary_hash,
        "configuration": args.configuration,
        "prefer_transport": args.prefer_transport,
        "cnf": str(args.base_cnf),
        "processed": len(rows),
        "support_models": support_models,
        "laurent_conflicts": len(conflicts),
        "transport_conflicts": sum(
            conflict.get("certificate_kind") == "cancellation_transport"
            for conflict in conflicts
        ),
        "learned_clauses": len(learned),
        "fallback_count": fallback_count,
        "unsat_count": sum(
            row["status"] == "UNSAT" for row in rows
        ),
        "solve_seconds": time.perf_counter() - solve_started,
        "rows": rows,
        "conflicts": conflicts,
        "learned_cnf": str(args.learned_cnf),
        "learned_cnf_sha256": sha256(args.learned_cnf),
    }
    checkpoint(args.output, payload)
    print(
        f"{payload['status']} roles={len(rows)} "
        f"models={support_models} conflicts={len(conflicts)} "
        f"fallbacks={fallback_count}",
        flush=True,
    )


if __name__ == "__main__":
    main()
