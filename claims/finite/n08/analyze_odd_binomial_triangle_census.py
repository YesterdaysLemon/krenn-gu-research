"""Exploratory census of exact odd-binomial triangles in SAT supports."""

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

from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from krenn_gu.eight_vertex_sparse_exact import (
    local_allowed_edges,
    positive_model_literals,
)
from krenn_gu.odd_binomial_cycle import support_odd_binomial_triangle_conflict
from krenn_gu.search_witness import EquationSystem
from krenn_gu.signed_binomial_lattice import (
    support_signed_binomial_lattice_conflict,
)


LOG_PATTERN = re.compile(r"role_(\d{4})_run_(\d{3})\.log")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def completed_logs(work_dir: Path) -> list[Path]:
    indexed: list[tuple[int, int, Path]] = []
    for path in work_dir.glob("role_*_run_*.log"):
        match = LOG_PATTERN.fullmatch(path.name)
        if match is None:
            continue
        if "s SATISFIABLE" not in path.read_text(encoding="ascii"):
            continue
        indexed.append(
            (int(match.group(1)), int(match.group(2)), path)
        )
    return [path for _role, _run, path in sorted(indexed)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--work-dir",
        action="append",
        type=Path,
        default=[],
    )
    parser.add_argument(
        "--extra-log",
        action="append",
        type=Path,
        default=[],
    )
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=1,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    allowed = set(local_allowed_edges(args.center_degree))
    structural_zero = {
        9 * system.edge_index[edge] + 3 * row + column
        for edge in system.edges
        if edge not in allowed
        for row in range(3)
        for column in range(3)
    }
    sources: list[tuple[str, Path]] = []
    for work_dir in args.work_dir:
        sources.extend(
            (str(work_dir), path)
            for path in completed_logs(work_dir)
        )
    sources.extend(("extra", path) for path in args.extra_log)

    seen_hashes: set[str] = set()
    rows: list[dict[str, object]] = []
    for source, log in sources:
        log_hash = sha256(log)
        if log_hash in seen_hashes:
            continue
        seen_hashes.add(log_hash)
        model = sorted(positive_model_literals(log))
        selected = local_positive_to_flat(
            system,
            model,
            args.center_degree,
        )
        result = support_odd_binomial_triangle_conflict(
            system,
            selected,
            structural_zero,
        )
        lattice = support_signed_binomial_lattice_conflict(
            system,
            selected,
            structural_zero,
        )
        lattice_summary = (
            None
            if lattice is None
            else {
                "mode": lattice[2]["certificate_mode"],
                "basis_relations": len(
                    lattice[2]["basis_relations"]
                ),
                "cube_size": len(lattice[0]) + len(lattice[1]),
            }
        )
        if result is None:
            rows.append(
                {
                    "source": source,
                    "log": str(log),
                    "log_sha256": log_hash,
                    "selected_entries": len(selected),
                    "has_odd_binomial_triangle": False,
                    "signed_lattice_certificate": lattice_summary,
                }
            )
            continue
        positive, negative, certificate = result
        rows.append(
            {
                "source": source,
                "log": str(log),
                "log_sha256": log_hash,
                "selected_entries": len(selected),
                "has_odd_binomial_triangle": True,
                "cube_size": len(positive) + len(negative),
                "certificate": certificate,
                "signed_lattice_certificate": lattice_summary,
            }
        )

    payload = {
        "verified": True,
        "scope": (
            "finite exploratory census of one exact odd-binomial "
            "triangle per completed SAT support"
        ),
        "claim_scope": "no arbitrary-order theorem is claimed",
        "center_degree": args.center_degree,
        "support_models": len(rows),
        "models_with_odd_binomial_triangle": sum(
            bool(row["has_odd_binomial_triangle"]) for row in rows
        ),
        "models_without_odd_binomial_triangle": sum(
            not bool(row["has_odd_binomial_triangle"]) for row in rows
        ),
        "models_with_signed_lattice_certificate": sum(
            row["signed_lattice_certificate"] is not None for row in rows
        ),
        "models_without_signed_lattice_certificate": sum(
            row["signed_lattice_certificate"] is None for row in rows
        ),
        "models": rows,
    }
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "support_models",
                    "models_with_odd_binomial_triangle",
                    "models_without_odd_binomial_triangle",
                    "models_with_signed_lattice_certificate",
                    "models_without_signed_lattice_certificate",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
