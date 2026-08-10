"""Independently reconstruct a C4+C4+C6 rule SAT DIMACS file.

This verifier deliberately does not import the rule compiler, transport
scanner, incremental driver, or CNF augmenter.  It independently:

* enumerates all 44,196 eligible singleton perfect matchings;
* reconstructs their 93 orbits under the fixed C4+C4+C6 factor;
* rebuilds the perfect-matching, edge-disjointness, selector, and
  connectivity clauses;
* replays every simple factor-fork certificate semantically;
* replays transported no-goods from separately audited rich proofs; and
* compares every reconstructed clause with the stated DIMACS files.

The source result must contain the ``source_sets`` field emitted by the
current rule compiler.  Augmentation manifests are supplied in the order
they were applied.
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
from pathlib import Path
from typing import Iterable, Sequence

from pysat.formula import CNF


N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
CYCLES = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11, 12, 13),
)


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)
ELIGIBLE_EDGES = tuple(
    item
    for item in itertools.combinations(range(N), 2)
    if item not in FULL_EDGES
)
ELIGIBLE_EDGE_ID = {
    item: index for index, item in enumerate(ELIGIBLE_EDGES)
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*map(int, item)) for item in raw))


def perfect_matchings(allowed: Iterable[Edge]) -> list[Factor]:
    adjacency = [0] * N
    for first, second in set(allowed):
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output: list[Factor] = []

    def visit(remaining: int, chosen: Factor) -> None:
        if not remaining:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << N) - 1, ())
    return sorted(output)


def full_automorphisms() -> list[tuple[int, ...]]:
    output = []
    for component_map in ((0, 1, 2), (1, 0, 2)):
        local_choices = itertools.product(
            *[
                [
                    (direction, rotation)
                    for direction in (1, -1)
                    for rotation in range(len(cycle))
                ]
                for cycle in CYCLES
            ]
        )
        for choices in local_choices:
            action = [0] * N
            for source_id, source in enumerate(CYCLES):
                target = CYCLES[component_map[source_id]]
                direction, rotation = choices[source_id]
                for position, vertex in enumerate(source):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            output.append(tuple(action))
    if len(output) != len(set(output)):
        raise AssertionError("full-factor automorphisms duplicated")
    return output


def transform_factor(
    factor: Factor, action: Sequence[int]
) -> Factor:
    return tuple(
        sorted(
            edge(action[first], action[second])
            for first, second in factor
        )
    )


def transform_colouring(
    colouring: Sequence[int],
    action: Sequence[int],
    colour_permutation: Sequence[int],
) -> tuple[int, ...]:
    output = [0] * N
    for old_vertex, old_colour in enumerate(colouring):
        output[action[old_vertex]] = colour_permutation[old_colour]
    return tuple(output)


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


def certificate_equations(item: object) -> set[int]:
    output: set[int] = set()
    if isinstance(item, dict):
        for key, value in item.items():
            if key.endswith("equation_index") and isinstance(
                value, int
            ):
                output.add(int(value))
            else:
                output.update(certificate_equations(value))
    elif isinstance(item, list):
        for value in item:
            output.update(certificate_equations(value))
    return output


def active_matching_ids(
    matchings: Sequence[Factor],
    factors: Sequence[Factor],
    colouring: Sequence[int],
) -> tuple[int, ...]:
    labels = {
        item: role
        for role, factor in enumerate(factors)
        for item in factor
    }
    active = set(FULL_EDGES)
    active.update(
        item
        for item, role in labels.items()
        if colouring[item[0]] == colouring[item[1]] == role
    )
    return tuple(
        index
        for index, matching in enumerate(matchings)
        if all(item in active for item in matching)
    )


def validate_simple_certificate(
    analysis: dict[str, object],
) -> tuple[
    tuple[Factor, Factor, Factor],
    tuple[tuple[int, ...], ...],
]:
    if analysis.get("status") != "even_cycle_factor_fork":
        raise AssertionError("analysis is not a simple factor fork")
    factors = tuple(
        parse_factor(analysis["singleton_matchings"][key])
        for key in ("first", "second", "third")
    )
    singleton_edges = set().union(*map(set, factors))
    if len(singleton_edges) != 3 * (N // 2):
        raise AssertionError("simple source factors overlap")
    matchings = perfect_matchings(set(FULL_EDGES) | singleton_edges)
    full_only = tuple(
        index
        for index, matching in enumerate(matchings)
        if all(item in FULL_EDGES for item in matching)
    )
    if len(full_only) != 8:
        raise AssertionError("full-factor product changed")
    certificate = analysis["certificate"]
    base = indexed_colouring(
        int(certificate["base_equation_index"])
    )
    base_activity = active_matching_ids(
        matchings, factors, base
    )
    if (
        base_activity
        != tuple(map(int, certificate["base_activity"]))
        or base_activity != full_only
        or len(set(base)) == 1
    ):
        raise AssertionError("simple base equation changed")
    alternatives = certificate["alternatives"]
    if {
        tuple(map(int, row["cycle"])) for row in alternatives
    } != set(CYCLES):
        raise AssertionError("simple fork alternatives changed")
    colourings = [base]
    for row in alternatives:
        cycle = tuple(map(int, row["cycle"]))
        target = indexed_colouring(
            int(row["target_equation_index"])
        )
        if any(target[vertex] != base[vertex] for vertex in cycle):
            raise AssertionError("cycle colors do not transport")
        activity = active_matching_ids(matchings, factors, target)
        surviving = int(row["surviving_matching"])
        if (
            activity != tuple(map(int, row["target_activity"]))
            or len(activity) != 9
            or set(full_only) - set(activity)
            or surviving not in activity
            or surviving in full_only
            or len(set(target)) == 1
        ):
            raise AssertionError("simple target equation changed")
        colourings.append(target)
    return factors, tuple(colourings)


def edge_variable(role: int, edge_id: int) -> int:
    return 1 + role * len(ELIGIBLE_EDGES) + edge_id


def activation_literals(
    role: int,
    factor: Factor,
    colourings: Iterable[Sequence[int]],
) -> dict[int, bool]:
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
                raise AssertionError("activation conditions conflict")
            output[variable] = value
    return output


def normalize(clause: Iterable[int]) -> tuple[int, ...]:
    output = tuple(
        sorted(set(map(int, clause)), key=lambda item: (abs(item), item))
    )
    if any(-literal in output for literal in output):
        raise AssertionError("transport clause became tautological")
    return output


def certificate_no_goods(
    factors: Sequence[Factor],
    colourings: Sequence[Sequence[int]],
    representative_id: dict[Factor, int],
    selector_variables: Sequence[int],
    actions: Sequence[Sequence[int]],
) -> set[tuple[int, ...]]:
    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError("first factor is not pinned")
    selector = selector_variables[first_orbit]
    output = set()
    for action in actions:
        if transform_factor(factors[0], action) != factors[0]:
            continue
        moved_factors = tuple(
            transform_factor(factor, action) for factor in factors
        )
        for permutation in ((0, 1, 2), (0, 2, 1)):
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
                    if previous is not None and previous != value:
                        raise AssertionError(
                            "transport activation conflict"
                        )
                    conditions[variable] = value
            clause = [-selector]
            clause.extend(
                -variable if value else variable
                for variable, value in conditions.items()
            )
            output.add(normalize(clause))
    return output


def exactly_one_pairwise(
    clauses: list[list[int]], variables: Sequence[int]
) -> None:
    clauses.append(list(variables))
    for first, second in itertools.combinations(variables, 2):
        clauses.append([-first, -second])


def base_clauses(
    representatives: Sequence[Factor],
) -> tuple[list[list[int]], tuple[int, ...]]:
    edge_variables = 3 * len(ELIGIBLE_EDGES)
    selectors = tuple(
        edge_variables + 1 + index
        for index in range(len(representatives))
    )
    clauses: list[list[int]] = []
    for role in range(3):
        for vertex in range(N):
            incident = [
                edge_variable(role, edge_id)
                for edge_id, item in enumerate(ELIGIBLE_EDGES)
                if vertex in item
            ]
            exactly_one_pairwise(clauses, incident)
    for edge_id in range(len(ELIGIBLE_EDGES)):
        for first, second in itertools.combinations(range(3), 2):
            clauses.append(
                [
                    -edge_variable(first, edge_id),
                    -edge_variable(second, edge_id),
                ]
            )
    exactly_one_pairwise(clauses, selectors)
    for selector, factor in zip(
        selectors, representatives, strict=True
    ):
        for item in factor:
            clauses.append(
                [-selector, edge_variable(0, ELIGIBLE_EDGE_ID[item])]
            )
    for component in CYCLES:
        inside = set(component)
        crossing = [
            edge_variable(role, edge_id)
            for role in range(3)
            for edge_id, item in enumerate(ELIGIBLE_EDGES)
            if (item[0] in inside) != (item[1] in inside)
        ]
        clauses.append(crossing)
    return clauses, selectors


def independently_verify_factor_orbits(
    census: dict[str, object],
    actions: Sequence[Sequence[int]],
) -> tuple[Factor, ...]:
    factors = perfect_matchings(ELIGIBLE_EDGES)
    if len(factors) != 44_196:
        raise AssertionError("eligible factor count changed")
    remaining = set(factors)
    independent_rows = []
    while remaining:
        seed = min(remaining)
        orbit = {
            transform_factor(seed, action) for action in actions
        }
        if not orbit <= remaining | (set(factors) - remaining):
            raise AssertionError("factor orbit escaped the census")
        representative = min(orbit)
        independent_rows.append((representative, len(orbit)))
        remaining.difference_update(orbit)
    independent_rows.sort()
    stated_rows = [
        (
            parse_factor(row["representative"]),
            int(row["orbit_size"]),
        )
        for row in census["factor_orbits"]
    ]
    if stated_rows != independent_rows:
        raise AssertionError(
            "factor orbit representatives or sizes changed"
        )
    return tuple(row[0] for row in stated_rows)


def compare_clauses(
    expected: Sequence[Sequence[int]], path: Path
) -> None:
    actual = CNF(from_file=str(path))
    if len(actual.clauses) != len(expected):
        raise AssertionError(
            f"clause count mismatch for {path}: "
            f"{len(actual.clauses)} != {len(expected)}"
        )
    for index, (left, right) in enumerate(
        zip(expected, actual.clauses, strict=True)
    ):
        if list(map(int, left)) != list(map(int, right)):
            raise AssertionError(
                f"clause {index} differs in {path}"
            )


def verified_audit(record: dict[str, object]) -> None:
    certificate = Path(record["certificate"])
    audit_path = Path(record["audit"])
    if (
        sha256(certificate) != record["certificate_sha256"]
        or sha256(audit_path) != record["audit_sha256"]
    ):
        raise AssertionError("rich certificate or audit hash changed")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("verified") is not True:
        raise AssertionError("rich certificate audit is not verified")


def rich_certificate_data(
    record: dict[str, object],
) -> tuple[
    tuple[Factor, Factor, Factor],
    tuple[tuple[int, ...], ...],
]:
    verified_audit(record)
    path = Path(record["certificate"])
    proof = json.loads(path.read_text(encoding="utf-8"))
    mode = record["mode"]
    if mode == "verified_double_pair":
        if proof.get("status") != "even_cycle_double_pair_fork":
            raise AssertionError("double-pair proof changed")
        equations = sorted(
            certificate_equations(proof["certificate"])
        )
    elif mode == "verified_forced_slice_factor_cegar":
        if proof.get("status") != "UNSAT":
            raise AssertionError("factor-CEGAR proof changed")
        equations = {
            int(value)
            for value in proof[
                "forcing_base_equations_by_local_code"
            ].values()
        }
        equations.update(
            int(row["equation_index"])
            for row in proof["factor_clause_origins"]
        )
        equations.update(
            int(row["certificate"]["target_equation_index"])
            for row in proof["branches"]
            if row["certificate"]["certificate_mode"]
            == "isolated_factor_lattice_class"
        )
        forced = json.loads(
            Path(proof["forced_cycle_analysis"]).read_text(
                encoding="utf-8"
            )
        )
        equations.update(
            certificate_equations(
                forced["conditional_fork_certificates_by_cycle"]
            )
        )
        equations = sorted(
            equations,
            key=lambda item: (
                item * 2_654_435_761
            )
            & 0xFFFFFFFF,
        )
    elif mode == (
        "verified_forced_slice_factor_cegar_transport_core"
    ):
        if (
            proof.get("status")
            != "UNSAT_irredundant_factor_cegar_transport_core"
        ):
            raise AssertionError("factor-CEGAR core changed")
        equations = list(map(int, proof["activation_equations"]))
    else:
        raise AssertionError(f"unknown rich certificate mode: {mode}")
    factors = tuple(
        parse_factor(proof["singleton_matchings"][key])
        for key in ("first", "second", "third")
    )
    return (
        factors,
        tuple(indexed_colouring(value) for value in equations),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument(
        "--augmentation",
        type=Path,
        action="append",
        default=[],
        help="augmentation manifests in application order",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    result = json.loads(args.result.read_text(encoding="utf-8"))
    if result.get("partition") != [4, 4, 6]:
        raise AssertionError("rule result partition changed")
    if "source_sets" not in result:
        raise AssertionError(
            "rule result predates source-set provenance"
        )
    census_path = Path(
        "tmp/fourteen_vertex_c4_4_6_factor_orbit_census.json"
    )
    census = json.loads(census_path.read_text(encoding="utf-8"))
    actions = full_automorphisms()
    if len(actions) != 1_536:
        raise AssertionError("full automorphism count changed")
    representatives = independently_verify_factor_orbits(
        census, actions
    )
    if len(representatives) != 93:
        raise AssertionError("factor orbit count changed")
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    clauses, selectors = base_clauses(representatives)
    if len(clauses) != int(result["base_clauses"]):
        raise AssertionError("base clause count changed")

    simple_rule_clauses: set[tuple[int, ...]] = set()
    simple_sources = 0
    source_counts = []
    for source in result["source_sets"]:
        manifest_path = Path(source["manifest"])
        pattern = str(source["analysis_pattern"])
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if manifest.get("partition") != [4, 4, 6]:
            raise AssertionError("source manifest partition changed")
        statuses: dict[str, int] = {}
        for index in range(len(manifest["survivors"])):
            analysis_path = Path(pattern.format(index=index))
            analysis = json.loads(
                analysis_path.read_text(encoding="utf-8")
            )
            status = str(analysis["status"])
            statuses[status] = statuses.get(status, 0) + 1
            if status != "even_cycle_factor_fork":
                if status not in {
                    "factor_fork_absent",
                    "disconnected_factorization_contradiction",
                }:
                    raise AssertionError(
                        f"unexpected source status: {status}"
                    )
                continue
            factors, colourings = validate_simple_certificate(
                analysis
            )
            simple_sources += 1
            simple_rule_clauses.update(
                certificate_no_goods(
                    factors,
                    colourings,
                    representative_id,
                    selectors,
                    actions,
                )
            )
        source_counts.append(
            {
                "name": source["name"],
                "survivors": len(manifest["survivors"]),
                "statuses": statuses,
            }
        )
    if simple_sources != int(result["simple_sources_replayed"]):
        raise AssertionError("simple source count changed")
    if len(simple_rule_clauses) != int(
        result["deduplicated_transport_no_goods"]
    ):
        raise AssertionError("simple transport no-good count changed")
    clauses.extend(list(clause) for clause in sorted(simple_rule_clauses))
    simple_cnf = Path(result["cnf"])
    compare_clauses(clauses, simple_cnf)
    current_path = simple_cnf

    augmentation_rows = []
    for manifest_path in args.augmentation:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if (
            Path(manifest["base_cnf"]) != current_path
            or sha256(current_path) != manifest["base_cnf_sha256"]
            or len(clauses) != int(manifest["base_clauses"])
        ):
            raise AssertionError("augmentation base provenance changed")
        known = {normalize(clause) for clause in clauses}
        added: set[tuple[int, ...]] = set()
        record_rows = []
        for record in manifest["certificate_records"]:
            factors, colourings = rich_certificate_data(record)
            transported = certificate_no_goods(
                factors,
                colourings,
                representative_id,
                selectors,
                actions,
            )
            new = transported - known - added
            if len(new) != int(record["new_no_goods"]):
                raise AssertionError(
                    "rich certificate no-good count changed"
                )
            added.update(new)
            record_rows.append(
                {
                    "mode": record["mode"],
                    "new_no_goods": len(new),
                }
            )
        if len(added) != int(manifest["new_no_goods"]):
            raise AssertionError("augmentation no-good count changed")
        clauses.extend(list(clause) for clause in sorted(added))
        output_path = Path(manifest["output_cnf"])
        if (
            len(clauses) != int(manifest["output_clauses"])
            or sha256(output_path) != manifest["output_cnf_sha256"]
        ):
            raise AssertionError("augmentation output provenance changed")
        compare_clauses(clauses, output_path)
        augmentation_rows.append(
            {
                "manifest": str(manifest_path),
                "records": record_rows,
                "new_no_goods": len(added),
                "output_cnf": str(output_path),
                "output_cnf_sha256": sha256(output_path),
            }
        )
        current_path = output_path

    payload = {
        "verified": True,
        "status": "rule_cnf_independently_reconstructed",
        "scope": (
            "the stated C4+C4+C6 rule CNF and supplied audited "
            "augmentation chain"
        ),
        "result": str(args.result),
        "result_sha256": sha256(args.result),
        "census": str(census_path),
        "census_sha256": sha256(census_path),
        "eligible_edges": len(ELIGIBLE_EDGES),
        "eligible_factors": 44_196,
        "first_factor_orbits": len(representatives),
        "full_factor_automorphisms": len(actions),
        "base_clauses": int(result["base_clauses"]),
        "simple_sources_replayed": simple_sources,
        "simple_transport_no_goods": len(simple_rule_clauses),
        "source_sets": source_counts,
        "augmentations": augmentation_rows,
        "final_cnf": str(current_path),
        "final_cnf_sha256": sha256(current_path),
        "final_clauses": len(clauses),
        "clause_by_clause_match": True,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
