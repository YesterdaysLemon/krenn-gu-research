"""Learn global symmetry no-goods from a partial-support unit ideal."""

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
from pathlib import Path

from krenn_gu.eight_vertex_degree4_cegar import symmetry_clauses
from krenn_gu.eight_vertex_sparse_exact import local_allowed_edges
from learn_singular_fallback_clauses import singular_unit
from krenn_gu.search_witness import EquationSystem

from verify_laurent_batch_manifest import audit_cnf


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partial-manifest", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    partial = json.loads(
        args.partial_manifest.read_text(encoding="utf-8")
    )
    program = Path(str(partial["program"]))
    log = program.with_suffix(".log")
    stderr = program.with_suffix(".stderr.log")
    if sha256(program) != partial["program_sha256"]:
        raise AssertionError("partial Singular source hash mismatch")
    if stderr.read_text(encoding="utf-8").strip():
        raise AssertionError("partial Singular stderr is nonempty")
    if not singular_unit(log.read_text(encoding="utf-8")):
        raise AssertionError("partial support ideal is not the unit ideal")

    positive = set(map(int, partial["positive_flat_indices"]))
    negative = set(map(int, partial["negative_flat_indices"]))
    if partial.get("pure_tensors") and not partial.get(
        "all_pure_tensors_derived_from_forced_stars"
    ):
        raise AssertionError(
            "derived equations lack a forced-singleton-star justification"
        )
    system = EquationSystem(8, 3)
    center_degree = int(partial["center_degree"])
    allowed_edges = set(local_allowed_edges(center_degree))
    for star in partial.get("forced_singleton_stars", []):
        center = int(star["center"])
        neighbours = tuple(map(int, star["colour_neighbours"]))
        if (
            not 0 <= center < 8
            or len(neighbours) != 3
            or center in neighbours
            or len(set(neighbours)) != 3
        ):
            raise AssertionError("malformed forced singleton star")
        for colour, neighbour in enumerate(neighbours):
            edge = tuple(sorted((center, neighbour)))
            block = {
                9 * system.edge_index[edge] + 3 * row + column
                for row in range(3)
                for column in range(3)
            }
            diagonal = (
                9 * system.edge_index[edge] + 3 * colour + colour
            )
            if diagonal not in positive or not (
                block - {diagonal}
            ) <= negative:
                raise AssertionError(
                    "partial cube does not force its declared singleton"
                )
        for other in range(8):
            if other == center or other in neighbours:
                continue
            edge = tuple(sorted((center, other)))
            if edge not in allowed_edges:
                continue
            block = {
                9 * system.edge_index[edge] + 3 * row + column
                for row in range(3)
                for column in range(3)
            }
            if not block <= negative:
                raise AssertionError(
                    "partial cube does not force star degree three"
                )
    clauses = sorted(
        symmetry_clauses(
            system,
            positive,
            negative,
            center_degree=center_degree,
        )
    )
    from krenn_gu.eight_vertex_degree4_cegar import write_augmented_cnf

    write_augmented_cnf(args.base_cnf, args.output_cnf, clauses)
    audit_cnf(args.base_cnf, args.output_cnf, clauses)
    payload = {
        "scope": (
            "global symmetry no-goods from an exact partial-support "
            "Singular unit ideal"
        ),
        "partial_manifest": str(args.partial_manifest),
        "partial_manifest_sha256": sha256(args.partial_manifest),
        "program_sha256": sha256(program),
        "log_sha256": sha256(log),
        "stderr_sha256": sha256(stderr),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "center_degree": int(partial["center_degree"]),
        "positive_entries": len(positive),
        "negative_entries": len(negative),
        "free_entries": len(partial["free_flat_indices"]),
        "forced_singleton_stars": partial.get(
            "forced_singleton_stars", []
        ),
        "derived_pure_vanishing_equations": int(
            partial.get("derived_pure_vanishing_equations", 0)
        ),
        "symmetry_clauses": len(clauses),
        "learned_clauses": [list(row) for row in clauses],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
