"""CEGAR over partial-circuit relation selections using binomial closure."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

from analyze_fourteen_vertex_partial_circuit_factor_cegar import (
    partial_relation_clauses,
)
from analyze_fourteen_vertex_portal_determinant_lattice import (
    contiguous_cycles,
    edge,
)


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode:
        raise RuntimeError(
            f"subprocess failed with code {result.returncode}: {command}"
        )


def proof_colourings(analysis: dict[str, object]) -> set[tuple[int, ...]]:
    """Return the exact colouring equations used by one branch proof."""

    output = {
        tuple(map(int, source["target_colouring"]))
        for source in analysis["relation_sources"]
        if str(source["mode"]).startswith("derived_")
    }
    contradiction = analysis.get("contradiction")
    if isinstance(contradiction, dict) and "target_colouring" in contradiction:
        output.add(
            tuple(map(int, contradiction["target_colouring"]))
        )
    return output


def write_chain(
    output: Path,
    *,
    status: str,
    partial_analysis: Path,
    radius: int,
    relation_clauses: list[tuple[int, ...]],
    relation_count: int,
    records: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "status": status,
        "scope": (
            "all exact partial-circuit relation clauses of one support, "
            "with every learned relation-selection block backed by an "
            "independently replayed iterative binomial-closure conflict"
        ),
        "partial_analysis": str(partial_analysis),
        "partial_analysis_sha256": sha256(partial_analysis),
        "radius": radius,
        "relation_count": relation_count,
        "relation_clauses": [list(clause) for clause in relation_clauses],
        "verified_branch_conflicts": sum(
            record["status"]
            == "verified_relation_selection_excluded"
            for record in records
        ),
        "records": records,
        "support_closed": status == "support_closed",
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial_analysis", type=Path)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--max-branches", type=int, default=20)
    parser.add_argument("--max-closure-rounds", type=int, default=20)
    parser.add_argument(
        "--max-derived-per-round", type=int, default=500
    )
    parser.add_argument(
        "--adaptive-candidate-pool",
        action="store_true",
        help=(
            "try colourings used by prior verified branches first, then "
            "fall back to the full Hamming census on any survivor"
        ),
    )
    parser.add_argument("--previous-chain", type=Path)
    parser.add_argument("--artifact-prefix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    partial = json.loads(
        args.partial_analysis.read_text(encoding="utf-8")
    )
    partition = tuple(map(int, partial["partition"]))
    cycles = contiguous_cycles(partition)
    factors = tuple(
        tuple(edge(*map(int, item)) for item in factor)
        for factor in partial["singleton_factors"]
    )
    clauses, relations, _origins = partial_relation_clauses(
        factors, cycles
    )
    dimacs = [
        tuple(relation_id + 1 for relation_id in clause)
        for clause in clauses
    ]
    records: list[dict[str, object]] = []
    if args.previous_chain is not None:
        previous = json.loads(
            args.previous_chain.read_text(encoding="utf-8")
        )
        if (
            Path(previous["partial_analysis"]) != args.partial_analysis
            or previous["partial_analysis_sha256"]
            != sha256(args.partial_analysis)
            or int(previous["radius"]) != args.radius
            or int(previous["relation_count"]) != len(relations)
            or previous["relation_clauses"]
            != [list(clause) for clause in clauses]
        ):
            raise ValueError("previous chain is bound to another problem")
        if any(
            record["status"]
            != "verified_relation_selection_excluded"
            for record in previous["records"]
        ):
            raise ValueError(
                "previous chain contains a non-exclusion terminal record"
            )
        records = list(previous["records"])
    candidate_pool: set[tuple[int, ...]] = set()
    if args.adaptive_candidate_pool:
        for record in records:
            if (
                record["status"]
                == "verified_relation_selection_excluded"
            ):
                prior_analysis = json.loads(
                    Path(record["analysis"]).read_text(encoding="utf-8")
                )
                candidate_pool.update(
                    proof_colourings(prior_analysis)
                )
    with Solver(name="cadical195", bootstrap_with=dimacs) as solver:
        for record in records:
            solver.add_clause(list(map(int, record["blocking_clause"])))
        for branch_id in range(
            len(records) + 1, args.max_branches + 1
        ):
            if not solver.solve():
                write_chain(
                    args.output,
                    status="support_closed",
                    partial_analysis=args.partial_analysis,
                    radius=args.radius,
                    relation_clauses=clauses,
                    relation_count=len(relations),
                    records=records,
                    started=started,
                )
                print(
                    json.dumps(
                        {
                            "status": "support_closed",
                            "verified_branch_conflicts": len(records),
                        },
                        indent=2,
                    ),
                    flush=True,
                )
                return
            model = solver.get_model() or []
            selected = sorted(
                literal - 1
                for literal in model
                if 1 <= literal <= len(relations)
            )
            selected_set = set(selected)
            for relation_id in sorted(selected, reverse=True):
                candidate = selected_set - {relation_id}
                if all(set(clause) & candidate for clause in clauses):
                    selected_set = candidate
            selected = sorted(selected_set)
            if any(not set(clause) & selected_set for clause in clauses):
                raise AssertionError(
                    "minimized selection stopped satisfying clauses"
                )
            if any(
                all(
                    set(clause) & (selected_set - {relation_id})
                    for clause in clauses
                )
                for relation_id in selected
            ):
                raise AssertionError("relation selection is not minimal")
            stem = Path(
                f"{args.artifact_prefix}_branch{branch_id:04d}"
            )
            analysis_path = stem.with_name(
                stem.name + "_closure.json"
            )
            restricted_path = stem.with_name(
                stem.name + "_restricted_closure.json"
            )
            candidate_pool_path = stem.with_name(
                stem.name + "_candidate_pool.json"
            )
            verified_path = stem.with_name(
                stem.name + "_verified.json"
            )
            closure_command = [
                sys.executable,
                "analyze_fourteen_vertex_partial_circuit_binomial_closure.py",
                str(args.partial_analysis),
                "--selected-relation-ids",
                ",".join(map(str, selected)),
                "--radius",
                str(args.radius),
                "--max-rounds",
                str(args.max_closure_rounds),
                "--max-derived-per-round",
                str(args.max_derived_per_round),
            ]
            used_restricted_pool = bool(
                args.adaptive_candidate_pool and candidate_pool
            )
            chosen_analysis_path = analysis_path
            if used_restricted_pool:
                candidate_pool_path.parent.mkdir(
                    parents=True, exist_ok=True
                )
                candidate_pool_path.write_text(
                    json.dumps(
                        {
                            "scope": (
                                "colouring equations used by prior "
                                "independently verified branch proofs"
                            ),
                            "colourings": [
                                list(colouring)
                                for colouring in sorted(candidate_pool)
                            ],
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                run(
                    closure_command
                    + [
                        "--candidate-colourings-file",
                        str(candidate_pool_path),
                        "--output",
                        str(restricted_path),
                    ]
                )
                restricted = json.loads(
                    restricted_path.read_text(encoding="utf-8")
                )
                if (
                    restricted.get("status")
                    == "relation_selection_branch_contradiction"
                ):
                    chosen_analysis_path = restricted_path
                    analysis = restricted
                else:
                    run(
                        closure_command
                        + ["--output", str(analysis_path)]
                    )
                    analysis = json.loads(
                        analysis_path.read_text(encoding="utf-8")
                    )
            else:
                run(
                    closure_command
                    + ["--output", str(analysis_path)]
                )
                analysis = json.loads(
                    analysis_path.read_text(encoding="utf-8")
                )
            analysis_path = chosen_analysis_path
            if (
                analysis.get("status")
                != "relation_selection_branch_contradiction"
            ):
                records.append(
                    {
                        "branch": branch_id,
                        "status": "surviving_relation_selection",
                        "selected_relation_ids": selected,
                        "analysis": str(analysis_path),
                        "analysis_sha256": sha256(analysis_path),
                        "analysis_status": analysis.get("status"),
                    }
                )
                write_chain(
                    args.output,
                    status="stalled_surviving_relation_selection",
                    partial_analysis=args.partial_analysis,
                    radius=args.radius,
                    relation_clauses=clauses,
                    relation_count=len(relations),
                    records=records,
                    started=started,
                )
                print(
                    json.dumps(records[-1], indent=2), flush=True
                )
                return
            if args.adaptive_candidate_pool:
                candidate_pool.update(proof_colourings(analysis))
            run(
                [
                    sys.executable,
                    str(REPO_ROOT / "claims" / "finite" / "n14" / "verify_fourteen_vertex_partial_circuit_binomial_branch.py"),
                    str(analysis_path),
                    "--output",
                    str(verified_path),
                ]
            )
            verified = json.loads(
                verified_path.read_text(encoding="utf-8")
            )
            if not verified.get("verified"):
                raise AssertionError("branch verifier did not pass")
            block = tuple(
                -(relation_id + 1) for relation_id in selected
            )
            solver.add_clause(block)
            record = {
                "branch": branch_id,
                "status": "verified_relation_selection_excluded",
                "selected_relation_ids": selected,
                "analysis": str(analysis_path),
                "analysis_sha256": sha256(analysis_path),
                "verified": str(verified_path),
                "verified_sha256": sha256(verified_path),
                "blocking_clause": list(block),
            }
            records.append(record)
            write_chain(
                args.output,
                status="in_progress",
                partial_analysis=args.partial_analysis,
                radius=args.radius,
                relation_clauses=clauses,
                relation_count=len(relations),
                records=records,
                started=started,
            )
            print(
                json.dumps(
                    {
                        "branch": branch_id,
                        "selected_relations": len(selected),
                        "verified_branch_conflicts": len(records),
                    },
                    indent=2,
                ),
                flush=True,
            )
        terminal_status = (
            "branch_limit" if solver.solve() else "support_closed"
        )
    write_chain(
        args.output,
        status=terminal_status,
        partial_analysis=args.partial_analysis,
        radius=args.radius,
        relation_clauses=clauses,
        relation_count=len(relations),
        records=records,
        started=started,
    )


if __name__ == "__main__":
    main()
