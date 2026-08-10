"""Find a C4+C4+C6 support outside known factor-fork transports.

The full family has more than 25 billion ordered connected factor triples.
The bitset coverage scanner can count them exactly, but it retains only a
small number of residual examples.  This script compiles the same
certificate semantics into SAT:

* three edge-disjoint singleton perfect matchings are selected;
* the first factor is symmetry-broken to one of the 93 pinned orbit
  representatives;
* the full-factor/singleton skeleton is connected; and
* every validated simple factor-fork transport becomes one no-good clause.

A SAT model is therefore a support not covered by the supplied simple
certificates.  UNSAT would close the whole C4+C4+C6 family by those
certificates, subject to independent CNF reconstruction and proof replay.
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
import itertools
import json
import time
from pathlib import Path
from typing import Iterable, Sequence

from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    CYCLES,
    ELIGIBLE_EDGE_ID,
    ELIGIBLE_EDGES,
    Factor,
    full_automorphisms,
    parse_factor,
    transform_colouring,
    transform_factor,
    validate_simple_certificate,
)

N = 14


def edge_variable(colour: int, edge_id: int) -> int:
    return 1 + colour * len(ELIGIBLE_EDGES) + edge_id


def exactly_one_pairwise(cnf: CNF, variables: Sequence[int]) -> None:
    cnf.append(list(variables))
    for first, second in itertools.combinations(variables, 2):
        cnf.append([-first, -second])


def source_specs(
    primary_samples: Path,
    primary_pattern: str,
    extra_samples: Sequence[Path],
    extra_patterns: Sequence[str],
) -> list[tuple[str, Path, str]]:
    if len(extra_samples) != len(extra_patterns):
        raise ValueError(
            "each --extra-samples needs one --extra-analysis-pattern"
        )
    output = [("primary", primary_samples, primary_pattern)]
    output.extend(
        (f"extra{index}", samples, pattern)
        for index, (samples, pattern) in enumerate(
            zip(extra_samples, extra_patterns, strict=True)
        )
    )
    return output


def activation_literals(
    role: int,
    factor: Factor,
    colourings: Iterable[Sequence[int]],
) -> dict[int, bool]:
    """Return edge-variable values fixing every observed active mask."""

    factor_edges = set(factor)
    output: dict[int, bool] = {}
    for colouring in colourings:
        vertices = {
            vertex
            for vertex, colour in enumerate(colouring)
            if colour == role
        }
        for edge_id, item in enumerate(ELIGIBLE_EDGES):
            if item[0] not in vertices or item[1] not in vertices:
                continue
            variable = edge_variable(role, edge_id)
            value = item in factor_edges
            previous = output.get(variable)
            if previous is not None and previous != value:
                raise AssertionError(
                    "source factor contradicts its activation pattern"
                )
            output[variable] = value
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_support_samples93.json"
        ),
    )
    parser.add_argument(
        "--analysis-pattern",
        default=(
            "tmp/fourteen_vertex_c4_4_6_"
            "sample93_{index}_factor_fork.json"
        ),
    )
    parser.add_argument(
        "--extra-samples",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--extra-analysis-pattern",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--census",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_factor_orbit_census.json"
        ),
    )
    parser.add_argument(
        "--solver",
        default="cadical195",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument(
        "--cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_simple_rule_residual.cnf"
        ),
    )
    parser.add_argument(
        "--sample-output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_simple_rule_sat_sample.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_simple_rule_sat.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    census = json.loads(args.census.read_text(encoding="utf-8"))
    if census.get("partition") != [4, 4, 6]:
        raise AssertionError("factor census partition changed")
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    if len(representatives) != 93:
        raise AssertionError("first-factor orbit count changed")
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }

    edge_variables = 3 * len(ELIGIBLE_EDGES)
    selector_variables = tuple(
        edge_variables + 1 + index
        for index in range(len(representatives))
    )
    cnf = CNF()

    # Each singleton colour class is a perfect matching.
    for colour in range(3):
        for vertex in range(N):
            incident = [
                edge_variable(colour, edge_id)
                for edge_id, item in enumerate(ELIGIBLE_EDGES)
                if vertex in item
            ]
            exactly_one_pairwise(cnf, incident)

    # An edge belongs to at most one singleton colour class.
    for edge_id in range(len(ELIGIBLE_EDGES)):
        for first, second in itertools.combinations(range(3), 2):
            cnf.append(
                [
                    -edge_variable(first, edge_id),
                    -edge_variable(second, edge_id),
                ]
            )

    # Symmetry break the first factor to one pinned representative.
    exactly_one_pairwise(cnf, selector_variables)
    for selector, factor in zip(
        selector_variables, representatives, strict=True
    ):
        for item in factor:
            cnf.append(
                [-selector, edge_variable(0, ELIGIBLE_EDGE_ID[item])]
            )

    # Connectivity of the quotient on the three full-factor components.
    # For three vertices, requiring every vertex to meet the rest is
    # equivalent to connectedness.
    for component in CYCLES:
        inside = set(component)
        crossing = [
            edge_variable(colour, edge_id)
            for colour in range(3)
            for edge_id, item in enumerate(ELIGIBLE_EDGES)
            if (item[0] in inside) != (item[1] in inside)
        ]
        cnf.append(crossing)

    base_clause_count = len(cnf.clauses)
    actions = full_automorphisms()
    colour_permutations = ((0, 1, 2), (0, 2, 1))
    rule_clauses: set[tuple[int, ...]] = set()
    simple_sources = 0
    source_statuses: dict[str, dict[str, int]] = {}

    for source_name, manifest_path, pattern in source_specs(
        args.samples,
        args.analysis_pattern,
        args.extra_samples,
        args.extra_analysis_pattern,
    ):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("partition") != [4, 4, 6]:
            raise AssertionError(
                f"source manifest partition changed: {manifest_path}"
            )
        statuses: dict[str, int] = {}
        for index in range(len(manifest["survivors"])):
            path = Path(pattern.format(index=index))
            analysis = json.loads(path.read_text(encoding="utf-8"))
            status = str(analysis["status"])
            statuses[status] = statuses.get(status, 0) + 1
            if status != "even_cycle_factor_fork":
                if status not in {
                    "factor_fork_absent",
                    "disconnected_factorization_contradiction",
                }:
                    raise AssertionError(
                        f"unexpected source status {status}: {path}"
                    )
                continue
            factors, colourings = validate_simple_certificate(analysis)
            first_orbit = representative_id.get(factors[0])
            if first_orbit is None:
                raise AssertionError(
                    "source first factor is not its pinned representative"
                )
            simple_sources += 1
            selector = selector_variables[first_orbit]
            for action in actions:
                if transform_factor(factors[0], action) != factors[0]:
                    continue
                moved_factors = tuple(
                    transform_factor(factor, action)
                    for factor in factors
                )
                for permutation in colour_permutations:
                    moved_colourings = tuple(
                        transform_colouring(
                            colouring, action, permutation
                        )
                        for colouring in colourings
                    )
                    conditions: dict[int, bool] = {}
                    for old_role in (1, 2):
                        new_role = permutation[old_role]
                        for variable, value in activation_literals(
                            new_role,
                            moved_factors[old_role],
                            moved_colourings,
                        ).items():
                            previous = conditions.get(variable)
                            if (
                                previous is not None
                                and previous != value
                            ):
                                raise AssertionError(
                                    "transport conditions conflict"
                                )
                            conditions[variable] = value
                    clause = [-selector]
                    clause.extend(
                        -variable if value else variable
                        for variable, value in conditions.items()
                    )
                    normalized = tuple(
                        sorted(set(clause), key=lambda item: (abs(item), item))
                    )
                    if any(-literal in normalized for literal in normalized):
                        raise AssertionError(
                            "transport no-good became tautological"
                        )
                    rule_clauses.add(normalized)
        source_statuses[source_name] = statuses

    for clause in sorted(rule_clauses):
        cnf.append(list(clause))
    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.cnf))

    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None

    residual = None
    if model is not None:
        positive = {literal for literal in model if literal > 0}
        factors = []
        for colour in range(3):
            factor = tuple(
                item
                for edge_id, item in enumerate(ELIGIBLE_EDGES)
                if edge_variable(colour, edge_id) in positive
            )
            if len(factor) != N // 2:
                raise AssertionError("SAT model is not a perfect matching")
            factors.append(factor)
        selected_orbits = [
            index
            for index, selector in enumerate(selector_variables)
            if selector in positive
        ]
        if len(selected_orbits) != 1:
            raise AssertionError("SAT model has no unique orbit selector")
        residual = {
            "orbit_id": selected_orbits[0],
            "first": [list(item) for item in factors[0]],
            "second": [list(item) for item in factors[1]],
            "third": [list(item) for item in factors[2]],
        }
        sample_payload = {
            "status": "simple_rule_sat_residual_sample",
            "partition": [4, 4, 6],
            "source_cnf": str(args.cnf),
            "survivors": [residual],
            "exploratory_only": True,
        }
        args.sample_output.parent.mkdir(parents=True, exist_ok=True)
        args.sample_output.write_text(
            json.dumps(sample_payload, indent=2) + "\n",
            encoding="utf-8",
        )

    payload = {
        "status": (
            "SAT_simple_rule_residual"
            if sat
            else "UNSAT_all_connected_supports_rule_closed"
        ),
        "necessary_conditions_only": sat,
        "partition": [4, 4, 6],
        "eligible_edges": len(ELIGIBLE_EDGES),
        "first_factor_orbits": len(representatives),
        "simple_sources_replayed": simple_sources,
        "source_sets": [
            {
                "name": name,
                "manifest": str(manifest),
                "analysis_pattern": pattern,
            }
            for name, manifest, pattern in source_specs(
                args.samples,
                args.analysis_pattern,
                args.extra_samples,
                args.extra_analysis_pattern,
            )
        ],
        "source_statuses": source_statuses,
        "full_factor_automorphisms": len(actions),
        "colour_permutations_fixing_first_role": len(
            colour_permutations
        ),
        "edge_variables": edge_variables,
        "selector_variables": len(selector_variables),
        "cnf_variables": cnf.nv,
        "base_clauses": base_clause_count,
        "deduplicated_transport_no_goods": len(rule_clauses),
        "cnf_clauses": len(cnf.clauses),
        "solver": args.solver,
        "sat": sat,
        "residual_support": residual,
        "cnf": str(args.cnf),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": sat,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
