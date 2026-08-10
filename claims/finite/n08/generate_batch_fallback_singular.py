"""Generate exact saturated Singular programs for batch fallback strata."""

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

from krenn_gu.eight_vertex_degree4_cegar import full_equations
from krenn_gu.eight_vertex_sparse_exact import (
    exact_equations,
    singular_program,
)
from krenn_gu.prism_laurent_reduction import primitive_binomial_reduction
from krenn_gu.search_witness import EquationSystem


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument(
        "--fallback-index",
        type=int,
        action="append",
        help=(
            "generate only this zero-based flattened fallback; repeat for "
            "a targeted exact run"
        ),
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="skip the exact unimodular Laurent preprocessing",
    )
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    system = EquationSystem(8, 3)
    full, flat_names, _ = full_equations(system)
    rows: list[tuple[dict[str, object], dict[str, object]]] = []
    for row in batch["rows"]:
        if "fallback" in row:
            rows.append((row, row["fallback"]))
        for fallback in row.get("fallbacks", []):
            rows.append((row, fallback))
    if args.fallback_index:
        selected_indices = sorted(set(args.fallback_index))
        if (
            selected_indices[0] < 0
            or selected_indices[-1] >= len(rows)
        ):
            raise ValueError("--fallback-index is outside the batch")
        indexed_rows = [(index, rows[index]) for index in selected_indices]
    else:
        indexed_rows = list(enumerate(rows))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, object]] = []
    for fallback_index, (row, fallback) in indexed_rows:
        selected = tuple(
            map(int, fallback["selected_flat_indices"])
        )
        if selected != tuple(sorted(set(selected))):
            raise AssertionError(
                "fallback selected indices are not canonical"
            )
        input_names = [
            flat_names[index] for index in selected
        ]
        if args.raw:
            names = [
                f"x{index}" for index in range(len(selected))
            ]
            variable_names = dict(
                zip(selected, names, strict=True)
            )
            equations = exact_equations(system, variable_names)
            reduction_metadata: dict[str, object] = {
                "mode": "raw",
                "restricted_equations": len(equations),
                "binomial_equations": None,
                "binomial_rank": None,
            }
        else:
            nonzero_names = set(input_names)
            restricted = []
            restricted_sources: list[int] = []
            for full_index, polynomial in enumerate(full):
                surviving = type(polynomial)(
                    {
                        monomial: coefficient
                        for monomial, coefficient in polynomial.items()
                        if all(
                            variable in nonzero_names
                            for variable in monomial
                        )
                    }
                )
                if surviving:
                    restricted.append(surviving)
                    restricted_sources.append(full_index)
            names, equations, metadata = (
                primitive_binomial_reduction(
                    restricted, input_names
                )
            )
            if metadata["unit_equation_indices"] or metadata[
                "linear_monomial_unit_relations"
            ]:
                raise AssertionError(
                    "batch labelled a Laurent-unit stratum as fallback"
                )
            reduction_metadata = {
                "mode": "unimodular_laurent",
                "restricted_equations": len(restricted),
                "binomial_equations": metadata[
                    "binomial_equations"
                ],
                "binomial_rank": metadata["binomial_rank"],
                "unimodular_determinant": metadata[
                    "unimodular_determinant"
                ],
                "free_laurent_variables": metadata[
                    "free_laurent_variables"
                ],
                "active_polynomial_variables": metadata[
                    "active_polynomial_variables"
                ],
                "active_free_variables": metadata[
                    "active_free_variables"
                ],
                "identically_eliminated_equations": metadata[
                    "identically_eliminated_equations"
                ],
                "basis_restricted_equation_indices": metadata[
                    "basis_equation_indices"
                ],
                "basis_full_equation_indices": [
                    restricted_sources[index]
                    for index in metadata["basis_equation_indices"]
                ],
                "output_restricted_equation_sources": metadata[
                    "output_equation_sources"
                ],
                "output_full_equation_sources": [
                    restricted_sources[index]
                    for index in metadata["output_equation_sources"]
                ],
            }
        program = singular_program(
            names, equations, args.characteristic
        )
        path = args.output_dir / (
            f"fallback_{fallback_index:03d}.sing"
        )
        path.write_text(program, encoding="utf-8")
        outputs.append(
            {
                "fallback_index": fallback_index,
                "role_index": int(row["role_index"]),
                "skeleton_edges": row["skeleton_edges"],
                "selected_entries": len(selected),
                "selected_flat_indices": list(selected),
                **reduction_metadata,
                "output_variables": len(names),
                "output_equations": len(equations),
                "program": str(path),
                "program_sha256": sha256(path),
            }
        )

    payload = {
        "scope": "exact torus ideals for Laurent batch fallbacks",
        "batch": str(args.batch),
        "batch_sha256": sha256(args.batch),
        "center_degree": int(batch.get("center_degree", 4)),
        "target_edges": batch.get("target_edges"),
        "characteristic": args.characteristic,
        "fallbacks": len(outputs),
        "programs": outputs,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
