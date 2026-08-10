"""Compile two-even-cycle factor-fork transports into an exact SAT model.

The supported order-14 full factors have cycle type ``C4+C10`` or
``C6+C8``.  Three edge-disjoint singleton perfect matchings are selected,
the first is pinned to one representative of the full-factor automorphism
orbits, and the combined support is required to connect the two cycles.
Every independently replayed two-cycle factor-fork certificate is
transported under the stabilizer of its pinned first factor and becomes a
CNF no-good.

A SAT model is therefore a connected support not covered by the supplied
certificates.  UNSAT is meaningful only after independent reconstruction of
the compiler and proof replay, just as for the C4+C4+C6 rule SAT model.
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

from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
)
from krenn_gu.explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)

Factor = tuple[Edge, ...]


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*item) for item in raw))


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def edge_variable(colour: int, edge_id: int, edge_count: int) -> int:
    return 1 + colour * edge_count + edge_id


def exactly_one_pairwise(cnf: CNF, variables: Sequence[int]) -> None:
    cnf.append(list(variables))
    for first, second in itertools.combinations(variables, 2):
        cnf.append([-first, -second])


def transform_factor(
    factor: Factor, action: dict[int, int]
) -> Factor:
    return tuple(
        sorted(edge(action[first], action[second]) for first, second in factor)
    )


def transform_colouring(
    colouring: Sequence[int],
    action: dict[int, int],
    colour_permutation: Sequence[int],
) -> tuple[int, ...]:
    output = [0] * N
    for old_vertex, old_colour in enumerate(colouring):
        output[action[old_vertex]] = colour_permutation[int(old_colour)]
    return tuple(output)


def active_matching_ids(
    matchings: Sequence[Factor],
    full_edges: set[Edge],
    factors: Sequence[Factor],
    colouring: Sequence[int],
) -> tuple[int, ...]:
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    active_edges = set(full_edges)
    active_edges.update(
        item
        for item, colour in labels.items()
        if colouring[item[0]] == colouring[item[1]] == colour
    )
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in active_edges for item in matching)
    )


def validate_simple_certificate(
    analysis: dict[str, object],
    survivor: dict[str, object],
    cycles: Sequence[Sequence[int]],
    full_edges: set[Edge],
) -> tuple[
    tuple[Factor, Factor, Factor],
    tuple[tuple[int, ...], ...],
]:
    """Rebuild and validate a two-even-cycle factor-fork certificate."""

    if analysis.get("status") != "two_even_cycle_factor_fork":
        raise AssertionError("analysis is not a simple two-cycle fork")
    if tuple(map(int, analysis["full_cycle_type"])) != tuple(
        map(len, cycles)
    ):
        raise AssertionError("certificate full-cycle type changed")
    factors = tuple(
        parse_factor(survivor[key])
        for key in ("first", "second", "third")
    )
    if any(len(factor) != N // 2 for factor in factors):
        raise AssertionError("source singleton factor is not perfect")
    if len(set().union(*map(set, factors))) != 3 * (N // 2):
        raise AssertionError("source singleton factors overlap")
    if set().union(*map(set, factors)) & full_edges:
        raise AssertionError("source singleton factor uses a full edge")
    matchings = perfect_matchings(
        N, full_edges | set().union(*map(set, factors))
    )
    full_only = tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    if len(full_only) != 4:
        raise AssertionError("two even cycles need four full matchings")
    certificate = analysis["certificate"]
    base_index = int(certificate["base_equation_index"])
    base = indexed_colouring(base_index)
    if tuple(map(int, certificate["base_colouring"])) != base:
        raise AssertionError("stored base colouring changed")
    base_activity = active_matching_ids(
        matchings, full_edges, factors, base
    )
    if (
        base_activity
        != tuple(map(int, certificate["base_activity"]))
        or base_activity != full_only
        or len(set(base)) == 1
    ):
        raise AssertionError("simple fork base activity changed")
    alternatives = certificate["alternatives"]
    if {
        tuple(map(int, row["cycle"])) for row in alternatives
    } != {tuple(map(int, cycle)) for cycle in cycles}:
        raise AssertionError("simple fork misses a cycle alternative")
    colourings = [base]
    for row in alternatives:
        cycle = tuple(map(int, row["cycle"]))
        target_index = int(row["target_equation_index"])
        target = indexed_colouring(target_index)
        if tuple(map(int, row["target_colouring"])) != target:
            raise AssertionError("stored target colouring changed")
        if any(target[vertex] != base[vertex] for vertex in cycle):
            raise AssertionError("cycle colours do not transport")
        activity = active_matching_ids(
            matchings, full_edges, factors, target
        )
        surviving = int(row["surviving_matching"])
        if (
            activity != tuple(map(int, row["target_activity"]))
            or len(activity) != 5
            or set(full_only) - set(activity)
            or surviving not in activity
            or surviving in full_only
            or len(set(target)) == 1
        ):
            raise AssertionError("simple fork target activity changed")
        colourings.append(target)
    return factors, tuple(colourings)


def activation_literals(
    role: int,
    factor: Factor,
    colourings: Iterable[Sequence[int]],
    eligible_edges: Sequence[Edge],
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
        for edge_id, item in enumerate(eligible_edges):
            if item[0] not in vertices or item[1] not in vertices:
                continue
            variable = edge_variable(role, edge_id, len(eligible_edges))
            value = item in factor_edges
            previous = output.get(variable)
            if previous is not None and previous != value:
                raise AssertionError(
                    "source factor contradicts its activation pattern"
                )
            output[variable] = value
    return output


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=Path,
        default=Path("tmp/fourteen_vertex_c4_10_support_samples425.json"),
    )
    parser.add_argument(
        "--analysis-pattern",
        default="tmp/fourteen_vertex_c4_10_sample425_{index}_fork.json",
    )
    parser.add_argument(
        "--extra-samples", type=Path, action="append", default=[]
    )
    parser.add_argument(
        "--extra-analysis-pattern", action="append", default=[]
    )
    parser.add_argument(
        "--census",
        type=Path,
        default=Path("tmp/fourteen_vertex_c4_10_factor_orbit_census.json"),
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
            "tmp/fourteen_vertex_two_even_cycle_simple_rule_residual.cnf"
        ),
    )
    parser.add_argument(
        "--sample-output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_even_cycle_simple_rule_sat_sample.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_even_cycle_simple_rule_sat.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    if (
        len(lengths) != 2
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("census is not a two-even-cycle partition")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    eligible_edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    actions = full_automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("full-factor automorphism count changed")

    edge_variables = 3 * len(eligible_edges)
    selector_variables = tuple(
        edge_variables + 1 + index
        for index in range(len(representatives))
    )
    cnf = CNF()

    for colour in range(3):
        for vertex in range(N):
            incident = [
                edge_variable(colour, edge_id, len(eligible_edges))
                for edge_id, item in enumerate(eligible_edges)
                if vertex in item
            ]
            exactly_one_pairwise(cnf, incident)

    for edge_id in range(len(eligible_edges)):
        for first, second in itertools.combinations(range(3), 2):
            cnf.append(
                [
                    -edge_variable(first, edge_id, len(eligible_edges)),
                    -edge_variable(second, edge_id, len(eligible_edges)),
                ]
            )

    exactly_one_pairwise(cnf, selector_variables)
    for selector, factor in zip(
        selector_variables, representatives, strict=True
    ):
        for item in factor:
            cnf.append(
                [
                    -selector,
                    edge_variable(
                        0, eligible_edge_id[item], len(eligible_edges)
                    ),
                ]
            )

    first_component = set(cycles[0])
    crossing = [
        edge_variable(colour, edge_id, len(eligible_edges))
        for colour in range(3)
        for edge_id, item in enumerate(eligible_edges)
        if (item[0] in first_component)
        != (item[1] in first_component)
    ]
    cnf.append(crossing)

    base_clause_count = len(cnf.clauses)
    colour_permutations = ((0, 1, 2), (0, 2, 1))
    rule_clauses: set[tuple[int, ...]] = set()
    simple_sources = 0
    source_statuses: dict[str, dict[str, int]] = {}

    specs = source_specs(
        args.samples,
        args.analysis_pattern,
        args.extra_samples,
        args.extra_analysis_pattern,
    )
    for source_name, manifest_path, pattern in specs:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if tuple(map(int, manifest["partition"])) != lengths:
            raise AssertionError(
                f"source manifest partition changed: {manifest_path}"
            )
        statuses: dict[str, int] = {}
        for index, survivor in enumerate(manifest["survivors"]):
            path = Path(pattern.format(index=index))
            analysis = json.loads(path.read_text(encoding="utf-8"))
            if int(analysis["survivor_index"]) != index:
                raise AssertionError("analysis survivor index changed")
            status = str(analysis["status"])
            statuses[status] = statuses.get(status, 0) + 1
            if status != "two_even_cycle_factor_fork":
                if status != "factor_fork_absent":
                    raise AssertionError(
                        f"unexpected source status {status}: {path}"
                    )
                continue
            factors, colourings = validate_simple_certificate(
                analysis, survivor, cycles, full_edges
            )
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
                            eligible_edges,
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
                        sorted(
                            set(clause), key=lambda item: (abs(item), item)
                        )
                    )
                    if any(
                        -literal in normalized for literal in normalized
                    ):
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
                for edge_id, item in enumerate(eligible_edges)
                if edge_variable(
                    colour, edge_id, len(eligible_edges)
                )
                in positive
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
            "status": "two_even_cycle_rule_sat_residual_sample",
            "partition": list(lengths),
            "source_census": str(args.census),
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
        "partition": list(lengths),
        "eligible_edges": len(eligible_edges),
        "first_factor_orbits": len(representatives),
        "simple_sources_replayed": simple_sources,
        "source_sets": [
            {
                "name": name,
                "manifest": str(manifest),
                "analysis_pattern": pattern,
            }
            for name, manifest, pattern in specs
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
