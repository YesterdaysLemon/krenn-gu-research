"""Create a resumable manifest from completed SAT logs in live CEGAR dirs.

The main no-binomial search checkpoints only after finishing a skeleton
role.  Long role-zero searches can nevertheless contain many immutable,
completed SAT logs.  This utility validates and snapshots those logs into
the small subset of the manifest schema consumed by ``--resume-manifest``.
It ignores the solver's current incomplete log.
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
import json
from pathlib import Path

from eight_vertex_no_binomial_cegar import (
    indicator_layout,
    sha256,
    violated_no_binomial_clauses,
)
from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from krenn_gu.search_witness import EquationSystem


def complete_sat_log(path: Path) -> bool:
    text = path.read_text(encoding="ascii", errors="replace")
    return (
        ("s SATISFIABLE" in text or "\nSAT\n" in f"\n{text}")
        and any(line.rstrip().endswith(" 0") for line in text.splitlines())
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-manifest",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    reference = json.loads(
        args.reference_manifest.read_text(encoding="utf-8")
    )
    system = EquationSystem(8, 3)
    indicator_last = int(reference["indicator_last_variable"])
    indicator_first, _ = indicator_layout(system, indicator_last)
    if indicator_first != int(reference["indicator_first_variable"]):
        raise AssertionError("reference indicator layout changed")

    seen_paths: set[Path] = set()
    learned: set[tuple[int, ...]] = set()
    rows: list[dict[str, object]] = []
    for work_dir in args.work_dir:
        runs: list[dict[str, object]] = []
        for path in sorted(work_dir.glob("role_*_run_*.log")):
            resolved = path.resolve()
            if resolved in seen_paths or not complete_sat_log(path):
                continue
            before = sha256(path)
            positive = positive_model_literals(path)
            after = sha256(path)
            if before != after:
                continue
            clauses, _records = violated_no_binomial_clauses(
                system,
                positive,
                indicator_first,
            )
            if not clauses:
                # A true no-binomial survivor belongs in a support audit,
                # not in a learned-clause resume snapshot.
                continue
            learned.update(clauses)
            seen_paths.add(resolved)
            runs.append(
                {
                    "status": "SAT",
                    "log": str(path),
                    "log_sha256": before,
                    "violated_two_term_amplitudes": len(clauses),
                }
            )
        rows.append(
            {
                "work_dir": str(work_dir),
                "solver_runs": runs,
            }
        )

    payload = {
        "status": "snapshot",
        "scope": "completed live no-binomial CEGAR SAT logs",
        "reference_manifest": str(args.reference_manifest),
        "reference_manifest_sha256": sha256(args.reference_manifest),
        "indicator_first_variable": indicator_first,
        "indicator_last_variable": indicator_last,
        "completed_sat_logs": len(seen_paths),
        "distinct_no_binomial_clauses": len(learned),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
