"""Independently replay detailed whole-pattern support/Laurent certificates."""

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
from collections import Counter
from pathlib import Path

import numpy as np

from certify_global_pattern_orbits import pattern_union
from global_candidate_laurent_cegar import exact_torus_program
from killer_union_stratum import union_orbit_equations
from krenn_gu.prism_laurent_reduction import primitive_binomial_reduction
from krenn_gu.prism_orbit_screen import clean_polynomial
from krenn_gu.rankone_support_sat import support_cnf
from krenn_gu.search_killer_patterns import active_mask_for_pattern
from krenn_gu.search_witness import EquationSystem
from verify_prism_certificates import is_exact_unit_log


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_laurent_certificate(
    equations: list[Counter],
    names: list[str],
    certificate: dict[str, object],
) -> None:
    positive = set(str(name) for name in certificate["positive_cube"])
    negative = set(str(name) for name in certificate["negative_cube"])
    if positive & negative:
        raise AssertionError("certificate cube has conflicting signs")
    source_indices = [
        *[int(index) for index in certificate["basis_equations"]],
        *(
            []
            if certificate.get("unit_equation") is None
            else [int(certificate["unit_equation"])]
        ),
        *[
            int(index)
            for index in certificate.get("linear_equations", [])
        ],
    ]
    restricted: list[Counter] = []
    for source_index in source_indices:
        polynomial = clean_polynomial(
            Counter(
                {
                    monomial: coefficient
                    for monomial, coefficient in equations[source_index].items()
                    if not any(variable in negative for variable in monomial)
                }
            )
        )
        for monomial in polynomial:
            if not set(monomial) <= positive:
                raise AssertionError(
                    "certificate leaves an unclassified monomial variable"
                )
        if polynomial:
            restricted.append(polynomial)
    active_names = [name for name in names if name in positive]
    _, _, metadata = primitive_binomial_reduction(
        restricted,
        active_names,
    )
    if (
        certificate.get("linear_monomial_unit_relation") is not None
        and not metadata["linear_monomial_unit_relations"]
    ):
        raise AssertionError(
            "recorded linear-monomial relation did not replay"
        )
    if not metadata["unit_equation_indices"] and not metadata[
        "linear_monomial_unit_relations"
    ]:
        raise AssertionError("Laurent replay did not derive a unit equation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--fallback-directory",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--solver",
        choices=("cadical195", "glucose42", "minisat22"),
        default="glucose42",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    from pysat.solvers import Solver

    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    accepted_statuses = {
        "certified",
        "certified_with_exact_fallback",
        "unconditional_laurent_contradiction",
    }
    if payload.get("fully_certified") is False or any(
        row.get("status") not in accepted_statuses
        for row in payload["rows"]
    ):
        raise SystemExit("manifest contains an uncertified pattern")
    system = EquationSystem(6, 3)
    replay_rows = []
    for row in payload["rows"]:
        pattern = [
            [int(neighbour) for neighbour in pattern_row]
            for pattern_row in row["pattern"]
        ]
        normalize_mutual = bool(row.get("normalized", False))
        names, equations, variable_names = union_orbit_equations(
            system,
            pattern,
            normalize_mutual=normalize_mutual,
        )
        structural_indices = [
            int(index)
            for index in np.flatnonzero(
                active_mask_for_pattern(system, pattern)
            )
        ]
        variable_by_flat = {
            flat_index: variable
            for variable, flat_index in enumerate(structural_indices, start=1)
        }
        variable_by_name = {
            name: variable_by_flat[flat_index]
            for flat_index, name in variable_names.items()
        }
        cnf = support_cnf(system, pattern, pattern_union(pattern))
        for certificate in row["certificates"]:
            replay_laurent_certificate(equations, names, certificate)
            positive = {
                str(name) for name in certificate["positive_cube"]
            }
            negative = {
                str(name) for name in certificate["negative_cube"]
            }
            cnf.add(
                *(-variable_by_name[name] for name in sorted(positive)),
                *(variable_by_name[name] for name in sorted(negative)),
            )

        exact_replays = []
        for exact_certificate in row["exact_certificates"]:
            nonzero_names = {
                str(name)
                for name in exact_certificate["nonzero_support"]
            }
            restricted = []
            for equation in equations:
                polynomial = clean_polynomial(
                    Counter(
                        {
                            monomial: coefficient
                            for monomial, coefficient in equation.items()
                            if all(
                                variable in nonzero_names
                                for variable in monomial
                            )
                        }
                    )
                )
                if polynomial:
                    restricted.append(polynomial)
            active_names = [
                name for name in names if name in nonzero_names
            ]
            reduced_names, reduced, _ = primitive_binomial_reduction(
                restricted,
                active_names,
            )
            expected_source = exact_torus_program(
                reduced_names,
                reduced,
            )
            fallback_id = str(exact_certificate["fallback_id"])
            source_path = (
                args.fallback_directory
                / f"fallback_{fallback_id}_q.sing"
            )
            log_path = (
                args.fallback_directory
                / f"fallback_{fallback_id}_q.log"
            )
            if source_path.read_text(encoding="utf-8") != expected_source:
                raise AssertionError("fallback Singular source mismatch")
            log_text = log_path.read_text(encoding="utf-8")
            if not is_exact_unit_log(log_text):
                raise AssertionError("fallback log is not an exact unit proof")
            if not expected_source.startswith("ring r=0,"):
                raise AssertionError("fallback is not characteristic zero")
            exact_replays.append(
                {
                    "fallback_id": fallback_id,
                    "source_sha256": sha256(source_path),
                    "log_sha256": sha256(log_path),
                }
            )

            zero_names = set(variable_by_name) - nonzero_names
            cnf.add(
                *(
                    -variable_by_name[name]
                    for name in sorted(nonzero_names)
                ),
                *(
                    variable_by_name[name]
                    for name in sorted(zero_names)
                ),
            )

        with Solver(
            name=args.solver,
            bootstrap_with=cnf.clauses,
        ) as solver:
            support_exhausted = not solver.solve()
        if not support_exhausted:
            raise AssertionError(
                f"support certificates do not exhaust orbit {row['orbit']}"
            )
        replay_rows.append(
            {
                "orbit": int(row["orbit"]),
                "union_size": int(
                    row.get("union_size", len(pattern_union(pattern)))
                ),
                "normalized": normalize_mutual,
                "laurent_certificates": len(row["certificates"]),
                "exact_fallbacks": len(exact_replays),
                "support_exhausted": support_exhausted,
                "exact_replays": exact_replays,
            }
        )

    result = {
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "solver": args.solver,
        "pattern_orbits": len(replay_rows),
        "laurent_certificates": sum(
            int(row["laurent_certificates"]) for row in replay_rows
        ),
        "exact_fallbacks": sum(
            int(row["exact_fallbacks"]) for row in replay_rows
        ),
        "verified": True,
        "rows": replay_rows,
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(
            f"wrote {args.output}: patterns={len(replay_rows)} "
            f"verified=True"
        )
    else:
        print(text)


if __name__ == "__main__":
    main()
