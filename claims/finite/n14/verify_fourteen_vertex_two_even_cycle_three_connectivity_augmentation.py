"""Independently replay an all-even-cycle connectivity augmentation."""

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

from pysat.formula import CNF
from pysat.solvers import Solver

N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def parse_factor(raw: list[list[int]]) -> Factor:
    return tuple(sorted(edge(*item) for item in raw))


def edge_variable(role: int, item_id: int, edge_count: int) -> int:
    return 1 + role * edge_count + item_id


def full_factor_edges(lengths: tuple[int, ...]) -> set[Edge]:
    output = set()
    start = 0
    for length in lengths:
        cycle = tuple(range(start, start + length))
        output.update(
            edge(cycle[index], cycle[(index + 1) % length])
            for index in range(length)
        )
        start += length
    if start != N:
        raise AssertionError("partition changed")
    return output


def fixed_components(
    fixed_edges: set[Edge], deleted: frozenset[int]
) -> list[frozenset[int]]:
    adjacency = {
        vertex: set()
        for vertex in range(N)
        if vertex not in deleted
    }
    for first, second in fixed_edges:
        if first in deleted or second in deleted:
            continue
        adjacency[first].add(second)
        adjacency[second].add(first)
    output = []
    unseen = set(adjacency)
    while unseen:
        root = min(unseen)
        seen = {root}
        frontier = [root]
        unseen.remove(root)
        while frontier:
            vertex = frontier.pop()
            for neighbour in adjacency[vertex] & unseen:
                unseen.remove(neighbour)
                seen.add(neighbour)
                frontier.append(neighbour)
        output.append(frozenset(seen))
    return sorted(output, key=lambda row: (min(row), len(row), tuple(row)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    status = manifest.get("status")
    if status == "three_vertex_connectivity_condition_augmented":
        minimum_connectivity = 3
    elif status == "four_vertex_connectivity_condition_augmented":
        minimum_connectivity = 4
    else:
        raise AssertionError("augmentation status changed")
    if int(
        manifest.get(
            "minimum_vertex_connectivity",
            minimum_connectivity,
        )
    ) != minimum_connectivity:
        raise AssertionError("minimum connectivity changed")
    base_path = Path(manifest["base_cnf"])
    compiled_path = Path(manifest["compiled_result"])
    census_path = Path(manifest["census"])
    output_path = Path(manifest["output_cnf"])
    for path, expected in (
        (base_path, manifest["base_cnf_sha256"]),
        (compiled_path, manifest["compiled_result_sha256"]),
        (census_path, manifest["census_sha256"]),
        (output_path, manifest["output_cnf_sha256"]),
    ):
        if sha256(path) != expected:
            raise AssertionError(f"source hash changed: {path}")

    compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
    census = json.loads(census_path.read_text(encoding="utf-8"))
    lengths = tuple(map(int, compiled["partition"]))
    if (
        len(lengths) < 2
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
        or tuple(map(int, census["partition"])) != lengths
        or list(lengths) != list(manifest["partition"])
    ):
        raise AssertionError("partition changed")
    full_edges = full_factor_edges(lengths)
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    eligible_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    selectors = tuple(
        3 * len(eligible_edges) + 1 + orbit
        for orbit in range(len(representatives))
    )
    generated: set[tuple[int, ...]] = set()
    reconstructed_rows = []
    for orbit, (selector, representative) in enumerate(
        zip(selectors, representatives, strict=True)
    ):
        local: set[tuple[int, ...]] = set()
        fixed_edges = full_edges | set(representative)
        for size in range(minimum_connectivity):
            for raw_deleted in itertools.combinations(range(N), size):
                deleted = frozenset(raw_deleted)
                rows = fixed_components(fixed_edges, deleted)
                for mask in range((1 << (len(rows) - 1)) - 1):
                    side = set(rows[0])
                    for component_id in range(1, len(rows)):
                        if mask & (1 << (component_id - 1)):
                            side.update(rows[component_id])
                    literals = {-selector}
                    for role in (1, 2):
                        for item in eligible_edges:
                            if (
                                item not in representative
                                and item[0] not in deleted
                                and item[1] not in deleted
                                and (
                                    (item[0] in side)
                                    != (item[1] in side)
                                )
                            ):
                                literals.add(
                                    edge_variable(
                                        role,
                                        eligible_id[item],
                                        len(eligible_edges),
                                    )
                                )
                    if literals == {-selector}:
                        raise AssertionError(
                            "reconstructed quotient cut is unbridgeable"
                        )
                    local.add(
                        tuple(
                            sorted(
                                literals,
                                key=lambda literal: (
                                    abs(literal),
                                    literal,
                                ),
                            )
                        )
                    )
        generated.update(local)
        reconstructed_rows.append(
            {
                "orbit": orbit,
                "selector": selector,
                "quotient_cut_clauses": len(local),
            }
        )

    stored_rows = manifest["selector_rows"]
    if len(stored_rows) != len(reconstructed_rows):
        raise AssertionError("selector row count changed")
    for stored, rebuilt in zip(
        stored_rows, reconstructed_rows, strict=True
    ):
        if (
            int(stored["orbit"]) != rebuilt["orbit"]
            or int(stored["selector"]) != rebuilt["selector"]
            or int(stored["quotient_cut_clauses"])
            != rebuilt["quotient_cut_clauses"]
        ):
            raise AssertionError("selector cut census changed")

    base_formula = CNF(from_file=str(base_path))
    base_normalized = {
        tuple(
            sorted(
                set(clause),
                key=lambda literal: (abs(literal), literal),
            )
        )
        for clause in base_formula.clauses
    }
    fresh = generated - base_normalized
    if len(fresh) != int(manifest["new_quotient_cut_clauses"]):
        raise AssertionError("new quotient-cut count changed")
    output_formula = CNF(from_file=str(output_path))
    expected_clauses = [
        *base_formula.clauses,
        *map(list, sorted(fresh)),
    ]
    if output_formula.clauses != expected_clauses:
        raise AssertionError("output CNF clause sequence changed")
    with Solver(
        name="cadical195", bootstrap_with=output_formula.clauses
    ) as solver:
        sat = solver.solve()

    reconstructed_status = (
        "three_vertex_connectivity_augmentation_reconstructed"
        if minimum_connectivity == 3
        else "four_vertex_connectivity_augmentation_reconstructed"
    )
    payload = {
        "verified": True,
        "status": reconstructed_status,
        "scope": (
            "source hashes, every deleted-set fixed component quotient, "
            "all canonical cut clauses, exact clause sequence, and an "
            "independent SAT solve"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "partition": list(lengths),
        "minimum_vertex_connectivity": minimum_connectivity,
        "first_factor_orbits": len(representatives),
        "deleted_vertex_sets_per_orbit": sum(
            1
            for size in range(minimum_connectivity)
            for _ in itertools.combinations(range(N), size)
        ),
        "new_quotient_cut_clauses": len(fresh),
        "output_cnf_variables": output_formula.nv,
        "output_cnf_clauses": len(output_formula.clauses),
        "independent_solver": "cadical195",
        "sat": bool(sat),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
