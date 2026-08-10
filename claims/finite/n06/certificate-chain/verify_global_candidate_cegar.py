"""Independently replay support-local certificates from global CEGAR."""

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
from collections import Counter
from pathlib import Path

from candidate_killer_cover_sat import candidate_cover_cnf
from global_candidate_laurent_cegar import (
    candidate_variable_map,
    exact_torus_program,
    required_candidate_arcs,
    symmetry_blocking_clauses,
    symmetry_transforms,
)
from killer_union_stratum import union_orbit_equations_with_colourings
from krenn_gu.prism_laurent_reduction import primitive_binomial_reduction
from krenn_gu.prism_orbit_screen import clean_polynomial
from krenn_gu.search_witness import EquationSystem
from verify_prism_certificates import is_exact_unit_log


def stable_restriction(
    equations: list[Counter],
    positive_names: set[str],
    negative_names: set[str],
) -> tuple[list[Counter], list[int], list[int]]:
    """Keep equations whose every term is fixed on or off by the cube."""
    restricted: list[Counter] = []
    restricted_sources: list[int] = []
    unstable_sources: list[int] = []
    for equation_index, equation in enumerate(equations):
        surviving: Counter = Counter()
        unstable = False
        for monomial, coefficient in equation.items():
            if not coefficient:
                continue
            if all(variable in positive_names for variable in monomial):
                surviving[monomial] += coefficient
            elif any(variable in negative_names for variable in monomial):
                continue
            else:
                unstable = True
                break
        if unstable:
            unstable_sources.append(equation_index)
            continue
        surviving = clean_polynomial(surviving)
        if surviving:
            restricted.append(surviving)
            restricted_sources.append(equation_index)
    return restricted, restricted_sources, unstable_sources


def fallback_artifacts(
    roots: list[Path],
    iteration: int,
    expected_program: str,
) -> tuple[Path, Path] | None:
    name = f"fallback_{iteration}_q.sing"
    matches = [
        (root / name, root / f"fallback_{iteration}_q.log")
        for root in roots
        if (root / name).is_file()
    ]
    if not matches:
        return None
    for singular_path, log_path in matches:
        if (
            log_path.is_file()
            and singular_path.read_text(encoding="utf-8")
            == expected_program
        ):
            return singular_path, log_path
    for singular_path, log_path in matches:
        if log_path.is_file():
            return singular_path, log_path
    return matches[0]


def verify_row(
    system: EquationSystem,
    row: dict[str, object],
    fallback_roots: list[Path],
) -> list[str]:
    iteration = int(row["iteration"])
    failures: list[str] = []
    pattern = [
        [int(neighbour) for neighbour in pattern_row]
        for pattern_row in row["pattern"]
    ]
    names, equations, variable_names, equation_colourings = (
        union_orbit_equations_with_colourings(system, pattern)
    )
    valid_flat_indices = set(variable_names)
    positive = {int(index) for index in row["positive_entries"]}
    negative = {int(index) for index in row["negative_entries"]}
    if positive & negative:
        failures.append("positive and negative entry cubes overlap")
    invalid_entries = (positive | negative) - valid_flat_indices
    if invalid_entries:
        failures.append(
            f"cube contains non-variable entries: {sorted(invalid_entries)}"
        )
    positive_names = {
        variable_names[index] for index in positive if index in variable_names
    }
    negative_names = {
        variable_names[index] for index in negative if index in variable_names
    }
    restricted, restricted_sources, unstable_sources = stable_restriction(
        equations,
        positive_names,
        negative_names,
    )
    active_names = [name for name in names if name in positive_names]
    try:
        reduced_names, reduced, metadata = primitive_binomial_reduction(
            restricted,
            active_names,
        )
    except Exception as error:  # pragma: no cover - diagnostic boundary
        failures.append(f"Laurent replay raised {error!r}")
        return failures

    stored_arcs = {
        tuple(int(value) for value in arc)
        for arc in row["candidate_arcs"]
    }
    pattern_arcs = {
        (vertex, colour, neighbour)
        for vertex, pattern_row in enumerate(pattern)
        for colour, neighbour in enumerate(pattern_row)
    }
    if not stored_arcs <= pattern_arcs:
        failures.append("stored candidate arc is absent from the pattern")

    if bool(row["used_grobner_fallback"]):
        if unstable_sources:
            failures.append(
                "fallback cube does not determine every original equation"
            )
        expected_program = exact_torus_program(reduced_names, reduced)
        artifacts = fallback_artifacts(
            fallback_roots,
            iteration,
            expected_program,
        )
        if artifacts is None:
            failures.append("missing fallback Singular source")
            return failures
        singular_path, log_path = artifacts
        if not log_path.is_file():
            failures.append(f"missing fallback log: {log_path}")
            return failures
        actual_program = singular_path.read_text(encoding="utf-8")
        if actual_program != expected_program:
            failures.append(
                f"fallback source does not match replay: {singular_path}"
            )
        log_text = log_path.read_text(encoding="utf-8")
        if not is_exact_unit_log(log_text):
            failures.append(f"fallback log is not an exact unit: {log_path}")
        used_equations = set(range(len(equations)))
    else:
        unit_indices = metadata["unit_equation_indices"]
        if not unit_indices:
            failures.append("stable Laurent replay has no unit equation")
            return failures
        unit_index = int(unit_indices[0])
        basis_indices = metadata["unit_basis_equation_indices"][
            str(unit_index)
        ]
        used_equations = {
            restricted_sources[index]
            for index in [*basis_indices, unit_index]
        }

    replay_arcs = required_candidate_arcs(
        system,
        pattern,
        equation_colourings,
        used_equations,
    )
    if not replay_arcs <= stored_arcs:
        failures.append(
            "stored arc cube omits replay-required arcs: "
            f"{sorted(replay_arcs - stored_arcs)}"
        )
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--fallback-directory",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument("--skip-sat-replay", action="store_true")
    args = parser.parse_args()
    fallback_roots = list(args.fallback_directory)
    if not fallback_roots:
        fallback_roots = sorted(
            path
            for path in Path("tmp").glob(
                "global_candidate_fallback_signed_*"
            )
            if path.is_dir()
        )

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    rows = manifest["rows"]
    failures: list[dict[str, object]] = []
    expected_iterations = list(range(len(rows)))
    actual_iterations = [int(row["iteration"]) for row in rows]
    if actual_iterations != expected_iterations:
        failures.append(
            {
                "iteration": None,
                "errors": ["row iteration sequence is not contiguous"],
            }
        )

    system = EquationSystem(6, 3)
    for row in rows:
        row_failures = verify_row(system, row, fallback_roots)
        if row_failures:
            failures.append(
                {
                    "iteration": int(row["iteration"]),
                    "errors": row_failures,
                }
            )

    symmetry_mode = str(manifest.get("symmetry_images", "none"))
    residual_support_sat: bool | None = None
    replayed_clauses = 0
    if not failures and not args.skip_sat_replay:
        from pysat.solvers import Cadical195

        cnf = candidate_cover_cnf(10)
        candidates = candidate_variable_map()
        transforms = symmetry_transforms(symmetry_mode)
        with Cadical195(bootstrap_with=cnf.clauses) as solver:
            for row in rows:
                clauses = symmetry_blocking_clauses(
                    system,
                    candidates,
                    {
                        tuple(int(value) for value in arc)
                        for arc in row["candidate_arcs"]
                    },
                    {
                        int(index)
                        for index in row["positive_entries"]
                    },
                    {
                        int(index)
                        for index in row["negative_entries"]
                    },
                    transforms,
                )
                expected_count = int(
                    row.get("symmetry_clause_count", len(clauses))
                )
                if len(clauses) != expected_count:
                    failures.append(
                        {
                            "iteration": int(row["iteration"]),
                            "errors": [
                                "symmetry clause count does not replay"
                            ],
                        }
                    )
                    break
                for clause in clauses:
                    solver.add_clause(clause)
                replayed_clauses += len(clauses)
            if not failures:
                residual_support_sat = bool(solver.solve())
                certified = manifest["status"] == "certified"
                if certified == residual_support_sat:
                    failures.append(
                        {
                            "iteration": None,
                            "errors": [
                                "manifest status disagrees with SAT replay"
                            ],
                        }
                    )

    result = {
        "manifest": str(args.manifest),
        "status": manifest["status"],
        "rows": len(rows),
        "direct_laurent_rows": sum(
            not bool(row["used_grobner_fallback"]) for row in rows
        ),
        "exact_fallback_rows": sum(
            bool(row["used_grobner_fallback"]) for row in rows
        ),
        "symmetry_images": symmetry_mode,
        "replayed_blocking_clauses": replayed_clauses,
        "residual_support_sat": residual_support_sat,
        "fallback_directories": [
            str(path) for path in fallback_roots
        ],
        "failures": failures,
        "verified": not failures,
    }
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
