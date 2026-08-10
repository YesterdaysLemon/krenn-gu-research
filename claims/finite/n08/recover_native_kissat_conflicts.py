"""Recover exact support conflicts from completed native-Kissat SAT logs.

The native batch driver historically checkpoints only after a catalogue
role becomes UNSAT.  This utility makes an in-progress role recoverable:
each completed SAT model is reparsed, given a fresh elementary-or-Laurent
certificate, expanded under the canonical stabilizer, and written as one
independently auditable learned-CNF manifest.
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
import re
from pathlib import Path

from krenn_gu.eight_vertex_degree4_cegar import (
    full_equations,
    laurent_conflict,
    symmetry_clauses,
    write_augmented_cnf,
)
from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from krenn_gu.search_witness import EquationSystem


LOG_PATTERN = re.compile(r"role_(\d{4})_run_(\d{3})\.log")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--learned-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        required=True,
    )
    parser.add_argument(
        "--extra-log",
        action="append",
        type=Path,
        default=[],
        help=(
            "additional completed SAT model log outside the work "
            "directory; may be repeated"
        ),
    )
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    equations, names, name_to_flat = full_equations(system)
    learned: set[tuple[int, ...]] = set()
    conflicts: list[dict[str, object]] = []
    source_logs: list[dict[str, object]] = []
    subsumed_logs: list[dict[str, object]] = []

    indexed_logs: list[tuple[int, int, Path]] = []
    for path in args.work_dir.glob("role_*_run_*.log"):
        if path.name.endswith(".stderr.log"):
            continue
        match = LOG_PATTERN.fullmatch(path.name)
        if match is None:
            continue
        text = path.read_text(encoding="ascii")
        if "s SATISFIABLE" not in text:
            if "s UNSATISFIABLE" in text:
                continue
            raise RuntimeError(f"{path} has no valid solver terminal")
        indexed_logs.append(
            (int(match.group(1)), int(match.group(2)), path)
        )
    for extra_index, path in enumerate(args.extra_log):
        text = path.read_text(encoding="ascii")
        if "s SATISFIABLE" not in text:
            raise RuntimeError(f"{path} has no SAT solver terminal")
        indexed_logs.append((0, 1_000_000 + extra_index, path))

    for role_index, run_index, log in sorted(indexed_logs):
        model = sorted(positive_model_literals(log))
        selected = local_positive_to_flat(
            system,
            model,
            args.center_degree,
        )
        positive, negative, metadata = laurent_conflict(
            system,
            equations,
            names,
            name_to_flat,
            selected,
            center_degree=args.center_degree,
            prefer_transport=True,
        )
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
            subsumed_logs.append(
                {
                    "role_index": role_index,
                    "run_index": run_index,
                    "path": str(log),
                    "sha256": sha256(log),
                    "certificate_kind": metadata[
                        "certificate_kind"
                    ],
                    "reason": (
                        "all stabilizer images were already learned "
                        "from earlier recovered models"
                    ),
                }
            )
            continue
        conflict_index = len(conflicts)
        conflicts.append(
            {
                "conflict_index": conflict_index,
                "role_index": role_index,
                "run_index": run_index,
                **metadata,
                "positive_entries": sorted(positive),
                "negative_entries": sorted(negative),
                "cube_size": len(positive) + len(negative),
                "symmetry_images": len(images),
                "new_clauses": len(new_clauses),
                "source_log": str(log),
                "source_log_sha256": sha256(log),
            }
        )
        learned.update(new_clauses)
        source_logs.append(
            {
                "role_index": role_index,
                "run_index": run_index,
                "path": str(log),
                "sha256": sha256(log),
            }
        )

    ordered_learned = sorted(learned)
    write_augmented_cnf(
        args.base_cnf,
        args.learned_cnf,
        ordered_learned,
    )
    payload = {
        "scope": (
            "recovered exact support no-goods from completed "
            "native-Kissat SAT logs"
        ),
        "center_degree": args.center_degree,
        "prefer_transport": True,
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "learned_cnf": str(args.learned_cnf),
        "learned_cnf_sha256": sha256(args.learned_cnf),
        "support_models": len(indexed_logs),
        "subsumed_support_models": len(subsumed_logs),
        "laurent_conflicts": len(conflicts),
        "transport_conflicts": sum(
            conflict["certificate_kind"] == "cancellation_transport"
            for conflict in conflicts
        ),
        "rectangle_conflicts": sum(
            conflict["certificate_kind"] == "two_monomial_rectangle"
            for conflict in conflicts
        ),
        "odd_triangle_conflicts": sum(
            conflict["certificate_kind"] == "odd_binomial_triangle"
            for conflict in conflicts
        ),
        "signed_lattice_conflicts": sum(
            conflict["certificate_kind"] == "signed_binomial_lattice"
            for conflict in conflicts
        ),
        "algebraic_laurent_conflicts": sum(
            conflict["certificate_kind"] == "laurent"
            for conflict in conflicts
        ),
        "learned_clauses": [
            list(clause) for clause in ordered_learned
        ],
        "conflicts": conflicts,
        "source_logs": source_logs,
        "subsumed_logs": subsumed_logs,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "support_models",
                    "subsumed_support_models",
                    "transport_conflicts",
                    "rectangle_conflicts",
                    "odd_triangle_conflicts",
                    "signed_lattice_conflicts",
                    "algebraic_laurent_conflicts",
                    "learned_cnf_sha256",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
