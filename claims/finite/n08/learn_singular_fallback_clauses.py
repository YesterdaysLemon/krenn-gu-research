"""Learn full-support no-goods from verified Singular fallback units."""

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
from pathlib import Path

from krenn_gu.eight_vertex_degree4_cegar import (
    symmetry_clauses,
    write_augmented_cnf,
)
from krenn_gu.eight_vertex_sparse_exact import local_allowed_edges
from krenn_gu.search_witness import EquationSystem


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allowed_flat_indices(
    system: EquationSystem,
    center_degree: int,
) -> set[int]:
    return {
        9 * system.edge_index[edge] + 3 * row + column
        for edge in local_allowed_edges(center_degree)
        for row in range(3)
        for column in range(3)
    }


def singular_unit(log: str) -> bool:
    lines = [line.strip() for line in log.splitlines()]
    return (
        "GB_SIZE" in lines
        and "REDUCE_ONE" in lines
        and any(
            lines[index : index + 2] == ["GB_SIZE", "1"]
            for index in range(len(lines) - 1)
        )
        and any(
            lines[index : index + 2] == ["REDUCE_ONE", "0"]
            for index in range(len(lines) - 1)
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fallback-manifest", type=Path, required=True
    )
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    fallback = json.loads(
        args.fallback_manifest.read_text(encoding="utf-8")
    )
    center_degree = int(fallback["center_degree"])
    system = EquationSystem(8, 3)
    allowed = allowed_flat_indices(system, center_degree)
    clauses: set[tuple[int, ...]] = set()
    certificates: list[dict[str, object]] = []
    for program in fallback["programs"]:
        program_path = Path(str(program["program"]))
        log_path = program_path.with_suffix(".log")
        stderr_path = program_path.with_suffix(".stderr.log")
        log = log_path.read_text(encoding="utf-8")
        stderr = stderr_path.read_text(encoding="utf-8")
        if stderr.strip():
            raise AssertionError(
                f"Singular wrote errors for {program_path}"
            )
        if not singular_unit(log):
            raise AssertionError(
                f"Singular unit terminal missing for {program_path}"
            )
        positive = set(
            map(int, program["selected_flat_indices"])
        )
        if not positive <= allowed:
            raise AssertionError("fallback selects a structural zero")
        images = symmetry_clauses(
            system,
            positive,
            allowed - positive,
            center_degree=center_degree,
        )
        clauses.update(images)
        certificates.append(
            {
                "fallback_index": int(
                    program["fallback_index"]
                ),
                "role_index": int(program["role_index"]),
                "program": str(program_path),
                "program_sha256": sha256(program_path),
                "log": str(log_path),
                "log_sha256": sha256(log_path),
                "stderr": str(stderr_path),
                "stderr_sha256": sha256(stderr_path),
                "selected_entries": len(positive),
                "zero_entries": len(allowed - positive),
                "symmetry_images": len(images),
            }
        )

    ordered_clauses = sorted(clauses)
    write_augmented_cnf(
        args.base_cnf, args.output_cnf, ordered_clauses
    )
    payload = {
        "scope": (
            "full-support no-goods from exact saturated "
            "Singular unit ideals"
        ),
        "fallback_manifest": str(args.fallback_manifest),
        "fallback_manifest_sha256": sha256(
            args.fallback_manifest
        ),
        "center_degree": center_degree,
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "certificates": certificates,
        "distinct_learned_clauses": len(ordered_clauses),
        "learned_clauses": [
            list(clause) for clause in ordered_clauses
        ],
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
