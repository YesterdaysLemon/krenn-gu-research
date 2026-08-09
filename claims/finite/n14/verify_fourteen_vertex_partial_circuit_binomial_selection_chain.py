"""Independently replay a binomial relation-selection CEGAR chain."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from pysat.solvers import Solver

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chain", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    chain = json.loads(args.chain.read_text(encoding="utf-8"))
    partial_path = Path(chain["partial_analysis"])
    if sha256(partial_path) != chain["partial_analysis_sha256"]:
        raise AssertionError("partial-analysis hash changed")
    clauses = [
        tuple(map(int, clause)) for clause in chain["relation_clauses"]
    ]
    relation_count = int(chain["relation_count"])
    dimacs = [
        tuple(relation_id + 1 for relation_id in clause)
        for clause in clauses
    ]
    fresh_branch_replays = 0
    minimal_selections_checked = 0
    records_checked = 0
    selection_sizes: Counter[int] = Counter()
    contradiction_modes: Counter[str] = Counter()
    terminal_activities: Counter[int] = Counter()
    terminal_colourings: Counter[tuple[int, ...]] = Counter()
    derived_relation_counts: Counter[int] = Counter()
    with Solver(name="cadical195", bootstrap_with=dimacs) as solver:
        with tempfile.TemporaryDirectory(
            prefix="binomial-selection-chain-audit-"
        ) as raw_directory:
            directory = Path(raw_directory)
            for expected_branch, record in enumerate(
                chain["records"], start=1
            ):
                if int(record["branch"]) != expected_branch:
                    raise AssertionError("branch numbering changed")
                selected = set(
                    map(int, record["selected_relation_ids"])
                )
                if any(not set(clause) & selected for clause in clauses):
                    raise AssertionError(
                        "recorded selection violates a relation clause"
                    )
                if any(
                    all(
                        set(clause) & (selected - {relation_id})
                        for clause in clauses
                    )
                    for relation_id in selected
                ):
                    raise AssertionError(
                        "recorded relation selection is not minimal"
                    )
                assumptions = [
                    relation_id + 1
                    if relation_id in selected
                    else -(relation_id + 1)
                    for relation_id in range(relation_count)
                ]
                if not solver.solve(assumptions=assumptions):
                    raise AssertionError(
                        "selection was already excluded before its branch"
                    )
                minimal_selections_checked += 1
                selection_sizes[len(selected)] += 1
                if (
                    record["status"]
                    != "verified_relation_selection_excluded"
                ):
                    if expected_branch != len(chain["records"]):
                        raise AssertionError(
                            "survivor record is not terminal"
                        )
                    records_checked += 1
                    continue
                analysis_path = Path(record["analysis"])
                verified_path = Path(record["verified"])
                if sha256(analysis_path) != record["analysis_sha256"]:
                    raise AssertionError("branch analysis hash changed")
                if sha256(verified_path) != record["verified_sha256"]:
                    raise AssertionError("branch verifier hash changed")
                analysis = json.loads(
                    analysis_path.read_text(encoding="utf-8")
                )
                contradiction = analysis.get("contradiction") or {}
                contradiction_modes[str(contradiction.get("mode"))] += 1
                if "target_matching_ids" in contradiction:
                    terminal_activities[
                        len(contradiction["target_matching_ids"])
                    ] += 1
                if "target_colouring" in contradiction:
                    terminal_colourings[
                        tuple(map(int, contradiction["target_colouring"]))
                    ] += 1
                derived_relation_counts[
                    sum(
                        int(round_record["new_relations"])
                        for round_record in analysis["rounds"]
                    )
                ] += 1
                if set(
                    map(
                        int,
                        analysis["selected_initial_relation_ids"],
                    )
                ) != selected:
                    raise AssertionError(
                        "branch analysis selection changed"
                    )
                stored_verified = json.loads(
                    verified_path.read_text(encoding="utf-8")
                )
                if not stored_verified.get("verified"):
                    raise AssertionError("stored branch verifier failed")
                replay_path = (
                    directory / f"branch-{expected_branch:04d}.json"
                )
                result = subprocess.run(
                    [
                        sys.executable,
                        str(HERE / "verify_fourteen_vertex_partial_circuit_binomial_branch.py"),
                        str(analysis_path),
                        "--output",
                        str(replay_path),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if result.returncode:
                    raise AssertionError(
                        "fresh branch replay failed: "
                        + (result.stderr or result.stdout)
                    )
                fresh_verified = json.loads(
                    replay_path.read_text(encoding="utf-8")
                )
                stored_without_time = dict(stored_verified)
                fresh_without_time = dict(fresh_verified)
                stored_without_time.pop("elapsed_seconds", None)
                fresh_without_time.pop("elapsed_seconds", None)
                if stored_without_time != fresh_without_time:
                    raise AssertionError(
                        "fresh branch replay summary changed"
                    )
                fresh_branch_replays += 1
                block = tuple(
                    -(relation_id + 1)
                    for relation_id in sorted(selected)
                )
                if list(block) != list(record["blocking_clause"]):
                    raise AssertionError("branch blocking clause changed")
                solver.add_clause(block)
                records_checked += 1
            terminal_sat = solver.solve()

    if chain["status"] == "support_closed":
        if terminal_sat:
            raise AssertionError("claimed support closure is SAT")
    elif chain["status"] in {
        "in_progress",
        "branch_limit",
        "stalled_surviving_relation_selection",
    }:
        if not terminal_sat:
            raise AssertionError(
                "nonterminal branch chain unexpectedly closed support"
            )
    else:
        raise AssertionError("unsupported chain status")

    payload = {
        "verified": True,
        "status": "partial_circuit_binomial_selection_chain_verified",
        "scope": (
            "relation clauses, inclusion-minimal selections, prior-model "
            "checks, fresh independent branch replays, exact blocking "
            "clauses, and the terminal relation-selection SAT decision"
        ),
        "chain": str(args.chain),
        "chain_sha256": sha256(args.chain),
        "chain_status": chain["status"],
        "relation_count": relation_count,
        "relation_clauses": len(clauses),
        "records_checked": records_checked,
        "minimal_selections_checked": minimal_selections_checked,
        "fresh_branch_replays": fresh_branch_replays,
        "selection_size_histogram": {
            str(key): selection_sizes[key]
            for key in sorted(selection_sizes)
        },
        "contradiction_mode_histogram": {
            key: contradiction_modes[key]
            for key in sorted(contradiction_modes)
        },
        "terminal_activity_histogram": {
            str(key): terminal_activities[key]
            for key in sorted(terminal_activities)
        },
        "terminal_colouring_histogram": {
            ",".join(map(str, key)): terminal_colourings[key]
            for key in sorted(terminal_colourings)
        },
        "derived_relation_count_histogram": {
            str(key): derived_relation_counts[key]
            for key in sorted(derived_relation_counts)
        },
        "terminal_relation_selection_sat": terminal_sat,
        "support_closed": not terminal_sat,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
