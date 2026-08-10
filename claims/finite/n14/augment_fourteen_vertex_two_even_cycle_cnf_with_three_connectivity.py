"""Add an exact vertex-connectivity >= 3 or >= 4 condition.

Chandran, Gajjala, and Illickan prove the Krenn--Gu conjecture for
edge-coloured weighted multigraph skeletons of vertex connectivity at most
two (arXiv:2407.00303, Theorem 2.1).  Therefore every counterexample
encoded by an all-even-cycle equality architecture must remain connected
after deleting any set of at most two vertices.  The optional
connectivity-four mode addresses the 4-connected branch of the
vertex-minimal-counterexample reduction and also considers three deletions.

For each pinned first-factor representative and each deleted vertex set,
the fixed full factor plus the first singleton factor has a component
partition.  Connectivity of the completed support is exactly the family of
quotient-cut clauses saying that roles 1 or 2 cross every nontrivial union
of those components.
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
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    edge_variable,
    parse_factor,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges

Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def components(
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
        component = {root}
        frontier = [root]
        unseen.remove(root)
        while frontier:
            vertex = frontier.pop()
            for neighbour in adjacency[vertex] & unseen:
                unseen.remove(neighbour)
                component.add(neighbour)
                frontier.append(neighbour)
        output.append(frozenset(component))
    return sorted(output, key=lambda row: (min(row), len(row), tuple(row)))


def connectivity_clauses(
    selector: int,
    representative: Factor,
    full_edges: set[Edge],
    eligible_edges: tuple[Edge, ...],
    minimum_connectivity: int,
) -> set[tuple[int, ...]]:
    fixed_edges = full_edges | set(representative)
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    output: set[tuple[int, ...]] = set()
    for size in range(minimum_connectivity):
        for raw_deleted in itertools.combinations(range(N), size):
            deleted = frozenset(raw_deleted)
            rows = components(fixed_edges, deleted)
            if len(rows) <= 1:
                continue
            # A cut and its complement are identical.  Keep the side
            # containing the canonical first component.
            for tail_mask in range((1 << (len(rows) - 1)) - 1):
                side = set(rows[0])
                for component_id in range(1, len(rows)):
                    if tail_mask & (1 << (component_id - 1)):
                        side.update(rows[component_id])
                clause = [-selector]
                clause.extend(
                    edge_variable(role, edge_id[item], len(eligible_edges))
                    for role in (1, 2)
                    for item in eligible_edges
                    if item not in representative
                    and item[0] not in deleted
                    and item[1] not in deleted
                    and ((item[0] in side) != (item[1] in side))
                )
                normalized = tuple(
                    sorted(
                        set(clause),
                        key=lambda literal: (abs(literal), literal),
                    )
                )
                if len(normalized) == 1:
                    raise AssertionError(
                        "fixed quotient cut cannot be crossed"
                    )
                output.add(normalized)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument(
        "--minimum-connectivity",
        type=int,
        choices=(3, 4),
        default=3,
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    compiled = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, compiled["partition"]))
    if (
        len(lengths) < 2
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
        or tuple(map(int, census["partition"])) != lengths
    ):
        raise AssertionError("all-even-cycle partition changed")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item
        for cycle in cycles
        for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    edge_variables = 3 * len(eligible_edges)
    selectors = tuple(
        edge_variables + 1 + index
        for index in range(len(representatives))
    )
    cnf = CNF(from_file=str(args.base_cnf))
    known = {
        tuple(
            sorted(
                set(clause),
                key=lambda literal: (abs(literal), literal),
            )
        )
        for clause in cnf.clauses
    }
    generated: set[tuple[int, ...]] = set()
    per_selector = []
    for orbit, (selector, representative) in enumerate(
        zip(selectors, representatives, strict=True)
    ):
        clauses = connectivity_clauses(
            selector,
            representative,
            full_edges,
            eligible_edges,
            args.minimum_connectivity,
        )
        fresh = clauses - known
        generated.update(fresh)
        per_selector.append(
            {
                "orbit": orbit,
                "selector": selector,
                "quotient_cut_clauses": len(clauses),
                "new_quotient_cut_clauses": len(fresh),
            }
        )
    for clause in sorted(generated):
        cnf.append(list(clause))
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.output_cnf))
    status = (
        "three_vertex_connectivity_condition_augmented"
        if args.minimum_connectivity == 3
        else "four_vertex_connectivity_condition_augmented"
    )
    theorem_scope = (
        "Krenn-Gu holds for skeleton vertex connectivity at most 2"
        if args.minimum_connectivity == 3
        else (
            "the 4-connected branch of the vertex-minimal-"
            "counterexample reduction"
        )
    )
    payload = {
        "status": status,
        "theorem_source": "https://arxiv.org/abs/2407.00303",
        "theorem_scope": theorem_scope,
        "minimum_vertex_connectivity": args.minimum_connectivity,
        "partition": list(lengths),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "compiled_result": str(args.compiled_result),
        "compiled_result_sha256": sha256(args.compiled_result),
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "first_factor_orbits": len(representatives),
        "selector_rows": per_selector,
        "new_quotient_cut_clauses": len(generated),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_cnf_variables": cnf.nv,
        "output_cnf_clauses": len(cnf.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_reconstructed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
