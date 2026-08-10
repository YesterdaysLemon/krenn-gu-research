"""Independently reconstruct a two-even-cycle rule SAT certificate.

This verifier intentionally does not import the compiler, incremental
driver, factor-census generator, or certificate-search scripts.  It
re-enumerates the eligible perfect matchings and their automorphism orbits,
rebuilds every base clause, replays every simple certificate semantically,
and compares the resulting DIMACS clause sequence exactly.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import hashlib
import itertools
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Sequence

from pysat.solvers import Solver

N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def cycles_for(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + int(length))))
        start += int(length)
    if start != N:
        raise AssertionError("cycle partition does not sum to 14")
    return tuple(output)


def cycle_edge_set(cycles: Sequence[Sequence[int]]) -> set[Edge]:
    return {
        edge(cycle[position], cycle[(position + 1) % len(cycle)])
        for cycle in cycles
        for position in range(len(cycle))
    }


def enumerate_matchings(allowed: Sequence[Edge]) -> list[Factor]:
    adjacency = [0] * N
    allowed_set = set(allowed)
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output: list[Factor] = []

    def visit(remaining: int, chosen: Factor) -> None:
        if not remaining:
            output.append(tuple(sorted(chosen)))
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            item = edge(first, second)
            if item not in allowed_set:
                raise AssertionError("matching enumerator left allowed set")
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, item),
            )

    visit((1 << N) - 1, ())
    return sorted(set(output))


def automorphisms(
    cycles: Sequence[Sequence[int]],
) -> list[dict[int, int]]:
    groups: dict[int, list[int]] = defaultdict(list)
    for component, cycle in enumerate(cycles):
        groups[len(cycle)].append(component)
    component_maps: list[dict[int, int]] = [{}]
    for indices in groups.values():
        next_rows = []
        for permutation in itertools.permutations(indices):
            mapping = dict(zip(indices, permutation, strict=True))
            for row in component_maps:
                next_rows.append({**row, **mapping})
        component_maps = next_rows
    local_choices = itertools.product(
        *[
            [
                (direction, rotation)
                for direction in (1, -1)
                for rotation in range(len(cycle))
            ]
            for cycle in cycles
        ]
    )
    choices = list(local_choices)
    output = []
    for component_map in component_maps:
        for local in choices:
            action: dict[int, int] = {}
            for source_id, source in enumerate(cycles):
                target = cycles[component_map[source_id]]
                direction, rotation = local[source_id]
                for position, vertex in enumerate(source):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            output.append(action)
    return output


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*item) for item in raw))


def transform_factor(
    factor: Factor, action: dict[int, int]
) -> Factor:
    return tuple(
        sorted(edge(action[first], action[second]) for first, second in factor)
    )


def factor_orbits(
    factors: Sequence[Factor],
    actions: Sequence[dict[int, int]],
) -> list[tuple[Factor, int]]:
    factor_set = set(factors)
    unseen = set(factors)
    output = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform_factor(representative, action)
            for action in actions
        }
        if not orbit <= factor_set:
            raise AssertionError("automorphism leaves eligible factors")
        output.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    return output


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def transform_colouring(
    colouring: Sequence[int],
    action: dict[int, int],
    colour_permutation: Sequence[int],
) -> tuple[int, ...]:
    output = [0] * N
    for old_vertex, old_colour in enumerate(colouring):
        output[action[old_vertex]] = colour_permutation[int(old_colour)]
    return tuple(output)


def support_matchings(
    allowed: set[Edge],
) -> list[Factor]:
    return enumerate_matchings(sorted(allowed))


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
    active = set(full_edges)
    active.update(
        item
        for item, colour in labels.items()
        if colouring[item[0]] == colouring[item[1]] == colour
    )
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in active for item in matching)
    )


def validate_certificate(
    analysis: dict[str, object],
    survivor: dict[str, object],
    cycles: Sequence[Sequence[int]],
    full_edges: set[Edge],
) -> tuple[
    tuple[Factor, Factor, Factor],
    tuple[tuple[int, ...], ...],
]:
    if analysis.get("status") != "two_even_cycle_factor_fork":
        raise AssertionError("analysis is not a simple factor fork")
    if tuple(map(int, analysis["full_cycle_type"])) != tuple(
        map(len, cycles)
    ):
        raise AssertionError("certificate cycle type changed")
    factors = tuple(
        parse_factor(survivor[key])
        for key in ("first", "second", "third")
    )
    if any(len(factor) != N // 2 for factor in factors):
        raise AssertionError("source factor is not perfect")
    union = set().union(*map(set, factors))
    if len(union) != 3 * (N // 2) or union & full_edges:
        raise AssertionError("source singleton factors are invalid")
    matchings = support_matchings(full_edges | union)
    full_only = tuple(
        index
        for index, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    if len(full_only) != 4:
        raise AssertionError("full-only matching count changed")
    certificate = analysis["certificate"]
    base = indexed_colouring(int(certificate["base_equation_index"]))
    if tuple(map(int, certificate["base_colouring"])) != base:
        raise AssertionError("stored base colouring changed")
    if (
        active_matching_ids(
            matchings, full_edges, factors, base
        )
        != full_only
        or tuple(map(int, certificate["base_activity"])) != full_only
        or len(set(base)) == 1
    ):
        raise AssertionError("base activity changed")
    alternatives = certificate["alternatives"]
    if {
        tuple(map(int, row["cycle"])) for row in alternatives
    } != {tuple(map(int, cycle)) for cycle in cycles}:
        raise AssertionError("certificate alternatives changed")
    colourings = [base]
    for row in alternatives:
        cycle = tuple(map(int, row["cycle"]))
        target = indexed_colouring(
            int(row["target_equation_index"])
        )
        if tuple(map(int, row["target_colouring"])) != target:
            raise AssertionError("stored target colouring changed")
        if any(target[vertex] != base[vertex] for vertex in cycle):
            raise AssertionError("target does not preserve cycle code")
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
            raise AssertionError("target activity changed")
        colourings.append(target)
    return factors, tuple(colourings)


def edge_variable(colour: int, edge_id: int, edge_count: int) -> int:
    return 1 + colour * edge_count + edge_id


def activation_literals(
    role: int,
    factor: Factor,
    colourings: Iterable[Sequence[int]],
    eligible_edges: Sequence[Edge],
) -> dict[int, bool]:
    factor_set = set(factor)
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
            value = item in factor_set
            previous = output.get(variable)
            if previous is not None and previous != value:
                raise AssertionError("activation conditions conflict")
            output[variable] = value
    return output


def normalize(clause: Iterable[int]) -> tuple[int, ...]:
    output = tuple(
        sorted(set(map(int, clause)), key=lambda item: (abs(item), item))
    )
    if any(-literal in output for literal in output):
        raise AssertionError("clause is tautological")
    return output


def certificate_no_goods(
    factors: Sequence[Factor],
    colourings: Sequence[Sequence[int]],
    representative_id: dict[Factor, int],
    selectors: Sequence[int],
    actions: Sequence[dict[int, int]],
    eligible_edges: Sequence[Edge],
) -> set[tuple[int, ...]]:
    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError("first factor is not a pinned representative")
    selector = selectors[first_orbit]
    output = set()
    for action in actions:
        if transform_factor(factors[0], action) != factors[0]:
            continue
        moved_factors = tuple(
            transform_factor(factor, action) for factor in factors
        )
        for permutation in ((0, 1, 2), (0, 2, 1)):
            moved_colourings = tuple(
                transform_colouring(colouring, action, permutation)
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
                    if previous is not None and previous != value:
                        raise AssertionError(
                            "transport conditions conflict"
                        )
                    conditions[variable] = value
            output.add(
                normalize(
                    [
                        -selector,
                        *[
                            -variable if value else variable
                            for variable, value in conditions.items()
                        ],
                    ]
                )
            )
    return output


def exactly_one(clauses: list[list[int]], variables: Sequence[int]) -> None:
    clauses.append(list(variables))
    for first, second in itertools.combinations(variables, 2):
        clauses.append([-first, -second])


def base_clauses(
    cycles: Sequence[Sequence[int]],
    eligible_edges: Sequence[Edge],
    representatives: Sequence[Factor],
) -> tuple[list[list[int]], tuple[int, ...]]:
    clauses: list[list[int]] = []
    for colour in range(3):
        for vertex in range(N):
            exactly_one(
                clauses,
                [
                    edge_variable(colour, edge_id, len(eligible_edges))
                    for edge_id, item in enumerate(eligible_edges)
                    if vertex in item
                ],
            )
    for edge_id in range(len(eligible_edges)):
        for first, second in itertools.combinations(range(3), 2):
            clauses.append(
                [
                    -edge_variable(first, edge_id, len(eligible_edges)),
                    -edge_variable(second, edge_id, len(eligible_edges)),
                ]
            )
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    edge_variables = 3 * len(eligible_edges)
    selectors = tuple(
        edge_variables + 1 + index
        for index in range(len(representatives))
    )
    exactly_one(clauses, selectors)
    for selector, factor in zip(selectors, representatives, strict=True):
        for item in factor:
            clauses.append(
                [
                    -selector,
                    edge_variable(
                        0, edge_id[item], len(eligible_edges)
                    ),
                ]
            )
    first_component = set(cycles[0])
    clauses.append(
        [
            edge_variable(colour, item_id, len(eligible_edges))
            for colour in range(3)
            for item_id, item in enumerate(eligible_edges)
            if (item[0] in first_component)
            != (item[1] in first_component)
        ]
    )
    return clauses, selectors


def read_dimacs(path: Path) -> tuple[int, list[list[int]]]:
    variables = None
    declared_clauses = None
    clauses = []
    pending: list[int] = []
    with path.open("r", encoding="ascii") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                _, kind, raw_variables, raw_clauses = line.split()
                if kind != "cnf":
                    raise AssertionError("DIMACS is not CNF")
                variables = int(raw_variables)
                declared_clauses = int(raw_clauses)
                continue
            for value in map(int, line.split()):
                if value == 0:
                    clauses.append(pending)
                    pending = []
                else:
                    pending.append(value)
    if pending:
        raise AssertionError("unterminated DIMACS clause")
    if (
        variables is None
        or declared_clauses is None
        or declared_clauses != len(clauses)
    ):
        raise AssertionError("DIMACS header changed")
    return variables, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    lengths = tuple(map(int, result["partition"]))
    if (
        len(lengths) != 2
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("result is not a two-even-cycle family")
    cycles = cycles_for(lengths)
    full_edges = cycle_edge_set(cycles)
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    actions = automorphisms(cycles)
    if len(actions) != int(result["full_factor_automorphisms"]):
        raise AssertionError("automorphism count changed")
    factors = enumerate_matchings(eligible_edges)
    census_path = Path(result["source_sets"][0]["manifest"])
    first_manifest = json.loads(
        census_path.read_text(encoding="utf-8")
    )
    actual_census_path = Path(first_manifest["source_census"])
    census = json.loads(
        actual_census_path.read_text(encoding="utf-8")
    )
    if tuple(map(int, census["partition"])) != lengths:
        raise AssertionError("census partition changed")
    if len(factors) != int(census["eligible_singleton_factors"]):
        raise AssertionError("eligible factor count changed")
    orbit_rows = factor_orbits(factors, actions)
    stored_rows = census["factor_orbits"]
    if len(orbit_rows) != len(stored_rows):
        raise AssertionError("factor orbit count changed")
    for (representative, size), stored in zip(
        orbit_rows, stored_rows, strict=True
    ):
        if (
            parse_factor(stored["representative"]) != representative
            or int(stored["orbit_size"]) != size
        ):
            raise AssertionError("factor orbit census changed")
    representatives = tuple(row[0] for row in orbit_rows)
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    clauses, selectors = base_clauses(
        cycles, eligible_edges, representatives
    )
    if len(clauses) != int(result["base_clauses"]):
        raise AssertionError("base clause count changed")

    rule_clauses: set[tuple[int, ...]] = set()
    simple_sources = 0
    source_rows = []
    for source in result["source_sets"]:
        manifest_path = Path(source["manifest"])
        pattern = str(source["analysis_pattern"])
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if tuple(map(int, manifest["partition"])) != lengths:
            raise AssertionError("source manifest partition changed")
        statuses: dict[str, int] = {}
        for index, survivor in enumerate(manifest["survivors"]):
            analysis = json.loads(
                Path(pattern.format(index=index)).read_text(
                    encoding="utf-8"
                )
            )
            status = str(analysis["status"])
            statuses[status] = statuses.get(status, 0) + 1
            if status != "two_even_cycle_factor_fork":
                if status != "factor_fork_absent":
                    raise AssertionError(
                        f"unexpected source status: {status}"
                    )
                continue
            factors_row, colourings = validate_certificate(
                analysis, survivor, cycles, full_edges
            )
            rule_clauses.update(
                certificate_no_goods(
                    factors_row,
                    colourings,
                    representative_id,
                    selectors,
                    actions,
                    eligible_edges,
                )
            )
            simple_sources += 1
        source_rows.append(
            {
                "manifest": str(manifest_path),
                "survivors": len(manifest["survivors"]),
                "statuses": statuses,
            }
        )
    if simple_sources != int(result["simple_sources_replayed"]):
        raise AssertionError("simple source count changed")
    if len(rule_clauses) != int(
        result["deduplicated_transport_no_goods"]
    ):
        raise AssertionError("transport no-good count changed")
    clauses.extend(list(clause) for clause in sorted(rule_clauses))
    cnf_path = Path(result["cnf"])
    variables, stored_clauses = read_dimacs(cnf_path)
    if clauses != stored_clauses:
        for index, (expected, actual) in enumerate(
            itertools.zip_longest(clauses, stored_clauses)
        ):
            if expected != actual:
                raise AssertionError(
                    f"CNF clause {index} changed: "
                    f"expected={expected}, actual={actual}"
                )
        raise AssertionError("CNF changed")
    if variables != int(result["cnf_variables"]):
        raise AssertionError("CNF variable count changed")
    with Solver(
        name="glucose4", bootstrap_with=stored_clauses
    ) as solver:
        independently_sat = solver.solve()
    if independently_sat is not bool(result["sat"]):
        raise AssertionError("independent SAT decision changed")
    payload = {
        "verified": True,
        "status": "two_even_cycle_rule_cnf_independently_reconstructed",
        "scope": (
            "the stated two-even-cycle factor census, simple transport "
            "sources, exact CNF, and independent SAT decision"
        ),
        "partition": list(lengths),
        "result": str(args.result),
        "result_sha256": sha256(args.result),
        "census": str(actual_census_path),
        "census_sha256": sha256(actual_census_path),
        "eligible_edges": len(eligible_edges),
        "eligible_factors": len(factors),
        "first_factor_orbits": len(representatives),
        "full_factor_automorphisms": len(actions),
        "base_clauses": int(result["base_clauses"]),
        "simple_sources_replayed": simple_sources,
        "transport_no_goods": len(rule_clauses),
        "cnf_variables": variables,
        "cnf_clauses": len(stored_clauses),
        "cnf": str(cnf_path),
        "cnf_sha256": sha256(cnf_path),
        "source_sets": source_rows,
        "independent_solver": "glucose4",
        "sat": independently_sat,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
