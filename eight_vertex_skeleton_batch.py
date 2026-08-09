"""Incrementally screen canonical fixed-edge-count degree-four skeleton roles.

The catalogue starts from connected unlabeled eight-vertex graphs with
minimum degree three and a selected edge count.  It retains matching-covered graphs with
a degree-four vertex, then labels:

* that vertex as 0;
* the guaranteed singleton neighbour as 1;
* the two selected nonzero-colour killers as 2 and 3;
* the spare neighbour as 4.

The remaining symmetry is ``S3`` on vertices 5,6,7 together with the joint
swap ``(2 3)`` and colours ``(1 2)``.  Canonicalization under this
12-element stabilizer leaves 10,241 role skeletons.

One PySAT solver is reused with the 25 block indicators supplied as
assumptions.  Every UNSAT result is valid for that whole fixed skeleton;
SAT rows retain only the 225 entry-support bits needed by the exact CEGAR
stage.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.eight_vertex_degree4_support import decode_graph6
from eight_vertex_sparse_exact import local_allowed_edges
from search_witness import perfect_matchings

Edge = tuple[int, int]
Skeleton = tuple[Edge, ...]


def ordered_role_skeletons(
    roles: set[Skeleton],
) -> list[Skeleton]:
    return sorted(roles, key=lambda skeleton: (len(skeleton), skeleton))


def transform_edges(
    edges: set[Edge] | Skeleton,
    permutation: tuple[int, ...],
) -> Skeleton:
    return tuple(
        sorted(
            tuple(
                sorted(
                    (permutation[first], permutation[second])
                )
            )
            for first, second in edges
        )
    )


def vertex_stabilizer() -> tuple[tuple[int, ...], ...]:
    result: list[tuple[int, ...]] = []
    for tail in itertools.permutations((5, 6, 7)):
        for swap in (False, True):
            permutation = list(range(8))
            permutation[5], permutation[6], permutation[7] = tail
            if swap:
                permutation[2], permutation[3] = 3, 2
            result.append(tuple(permutation))
    return tuple(result)


def canonical_role(edges: Skeleton) -> Skeleton:
    return min(
        transform_edges(edges, permutation)
        for permutation in vertex_stabilizer()
    )


def degree_three_vertex_stabilizer() -> tuple[
    tuple[int, ...], ...
]:
    result: list[tuple[int, ...]] = []
    for neighbours in itertools.permutations((1, 2, 3)):
        for tail in itertools.permutations((4, 5, 6, 7)):
            permutation = list(range(8))
            (
                permutation[1],
                permutation[2],
                permutation[3],
            ) = neighbours
            (
                permutation[4],
                permutation[5],
                permutation[6],
                permutation[7],
            ) = tail
            result.append(tuple(permutation))
    return tuple(result)


def canonical_degree_three_role(edges: Skeleton) -> Skeleton:
    return min(
        transform_edges(edges, permutation)
        for permutation in degree_three_vertex_stabilizer()
    )


def matching_covered(edges: set[Edge]) -> bool:
    matchings = [
        matching
        for matching in perfect_matchings(tuple(range(8)))
        if all(edge in edges for edge in matching)
    ]
    if not matchings:
        return False
    used = {
        edge
        for matching in matchings
        for edge in matching
    }
    return used == edges


def canonical_role_skeletons(
    graph6_path: Path,
    target_edges: int | None = 16,
) -> tuple[set[Skeleton], dict[str, int]]:
    roles: set[Skeleton] = set()
    unlabeled = 0
    for row in graph6_path.read_text(encoding="ascii").splitlines():
        if not row.strip():
            continue
        edges = set(decode_graph6(row))
        if (
            target_edges is not None
            and len(edges) != target_edges
        ):
            continue
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(8)
        ]
        if 4 not in degrees or not matching_covered(edges):
            continue
        unlabeled += 1
        for centre in (
            vertex for vertex in range(8) if degrees[vertex] == 4
        ):
            neighbours = sorted(
                other
                for edge in edges
                if centre in edge
                for other in edge
                if other != centre
            )
            remaining = sorted(
                set(range(8)) - {centre, *neighbours}
            )
            for ordered_neighbours in itertools.permutations(neighbours):
                for ordered_remaining in itertools.permutations(remaining):
                    permutation = [-1] * 8
                    permutation[centre] = 0
                    for old, new in zip(
                        ordered_neighbours,
                        (1, 2, 3, 4),
                        strict=True,
                    ):
                        permutation[old] = new
                    for old, new in zip(
                        ordered_remaining,
                        (5, 6, 7),
                        strict=True,
                    ):
                        permutation[old] = new
                    roles.add(
                        canonical_role(
                            transform_edges(
                                edges, tuple(permutation)
                            )
                        )
                    )
    return roles, {
        "unlabeled_matching_covered_graphs": unlabeled,
        "canonical_role_skeletons": len(roles),
    }


def canonical_degree_three_role_skeletons(
    graph6_path: Path,
    target_edges: int | None = None,
) -> tuple[set[Skeleton], dict[str, int]]:
    roles: set[Skeleton] = set()
    unlabeled_graphs: set[str] = set()
    for row in graph6_path.read_text(encoding="ascii").splitlines():
        if not row.strip():
            continue
        edges = set(decode_graph6(row))
        if target_edges is not None and len(edges) != target_edges:
            continue
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(8)
        ]
        if 3 not in degrees or not matching_covered(edges):
            continue
        unlabeled_graphs.add(row)
        for centre in (
            vertex for vertex in range(8) if degrees[vertex] == 3
        ):
            neighbours = sorted(
                other
                for edge in edges
                if centre in edge
                for other in edge
                if other != centre
            )
            remaining = sorted(
                set(range(8)) - {centre, *neighbours}
            )
            permutation = [-1] * 8
            permutation[centre] = 0
            for old, new in zip(
                neighbours, (1, 2, 3), strict=True
            ):
                permutation[old] = new
            for old, new in zip(
                remaining, (4, 5, 6, 7), strict=True
            ):
                permutation[old] = new
            roles.add(
                canonical_degree_three_role(
                    transform_edges(edges, tuple(permutation))
                )
            )
    return roles, {
        "unlabeled_matching_covered_graphs": len(
            unlabeled_graphs
        ),
        "canonical_role_skeletons": len(roles),
    }


def canonical_minimum_five_skeletons(
    graph6_path: Path,
    target_edges: int | None = None,
) -> tuple[set[Skeleton], dict[str, int]]:
    roles: set[Skeleton] = set()
    for row in graph6_path.read_text(encoding="ascii").splitlines():
        if not row.strip():
            continue
        edges = set(decode_graph6(row))
        if target_edges is not None and len(edges) != target_edges:
            continue
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(8)
        ]
        if min(degrees) < 5 or not matching_covered(edges):
            continue
        # ``geng`` emits one canonical graph6 representative per
        # isomorphism class.  The global support CNF has full vertex
        # symmetry, so one supplied labelling is sufficient.
        roles.add(tuple(sorted(edges)))
    return roles, {
        "unlabeled_matching_covered_graphs": len(roles),
        "canonical_role_skeletons": len(roles),
    }


def canonical_normalized_killer_skeletons(
    graph6_path: Path,
    target_edges: int | None = None,
) -> tuple[set[Skeleton], dict[str, int]]:
    roles: set[Skeleton] = set()
    unlabeled_graphs: set[str] = set()
    for row in graph6_path.read_text(encoding="ascii").splitlines():
        if not row.strip():
            continue
        edges = set(decode_graph6(row))
        if target_edges is not None and len(edges) != target_edges:
            continue
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(8)
        ]
        if min(degrees) < 5 or not matching_covered(edges):
            continue
        unlabeled_graphs.add(row)
        for centre in range(8):
            neighbours = sorted(
                other
                for edge in edges
                if centre in edge
                for other in edge
                if other != centre
            )
            for killer_neighbours in itertools.combinations(
                neighbours, 3
            ):
                remaining = sorted(
                    set(range(8))
                    - {centre, *killer_neighbours}
                )
                permutation = [-1] * 8
                permutation[centre] = 0
                for old, new in zip(
                    killer_neighbours, (1, 2, 3), strict=True
                ):
                    permutation[old] = new
                for old, new in zip(
                    remaining, (4, 5, 6, 7), strict=True
                ):
                    permutation[old] = new
                roles.add(
                    canonical_degree_three_role(
                        transform_edges(
                            edges, tuple(permutation)
                        )
                    )
                )
    return roles, {
        "unlabeled_matching_covered_graphs": len(
            unlabeled_graphs
        ),
        "canonical_role_skeletons": len(roles),
    }


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6",
        type=Path,
        default=Path("tmp/n8_mindeg3_e12_16.g6"),
    )
    parser.add_argument(
        "--cnf",
        type=Path,
        default=Path(
            "tmp/eight_vertex_local_degree4_cegar1_max16.cnf"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/eight_vertex_skeleton_batch.json"),
    )
    parser.add_argument("--target-edges", type=int, default=16)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=4,
    )
    args = parser.parse_args()

    from pysat.formula import CNF
    from pysat.solvers import Solver

    started = time.perf_counter()
    catalogue_builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[args.center_degree]
    roles, catalogue = catalogue_builder(
        args.graph6, target_edges=args.target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    catalogue_seconds = time.perf_counter() - started

    formula = CNF(from_file=str(args.cnf))
    allowed = local_allowed_edges(args.center_degree)
    allowed_index = {
        edge: index for index, edge in enumerate(allowed)
    }
    first_block_variable = 1 + 9 * len(allowed)
    rows: list[dict[str, object]] = []
    sat_count = 0
    solve_started = time.perf_counter()
    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        for index, skeleton in enumerate(ordered_roles):
            present = set(skeleton)
            assumptions = [
                (
                    first_block_variable + edge_index
                    if edge in present
                    else -(first_block_variable + edge_index)
                )
                for edge, edge_index in allowed_index.items()
            ]
            case_started = time.perf_counter()
            sat = solver.solve(assumptions=assumptions)
            elapsed = time.perf_counter() - case_started
            row: dict[str, object] = {
                "role_index": index,
                "skeleton_edges": [list(edge) for edge in skeleton],
                "status": "SAT" if sat else "UNSAT",
                "solve_seconds": elapsed,
            }
            if sat:
                sat_count += 1
                positive = {
                    literal
                    for literal in solver.get_model() or []
                    if literal > 0
                }
                row["positive_entry_variables"] = [
                    variable
                    for variable in range(1, 1 + 9 * len(allowed))
                    if variable in positive
                ]
            rows.append(row)
            if (index + 1) % 250 == 0:
                print(
                    f"{index + 1}/{len(ordered_roles)} "
                    f"SAT={sat_count}",
                    flush=True,
                )
                checkpoint(
                    args.output,
                    {
                        "status": "running",
                        **catalogue,
                        "catalogue_seconds": catalogue_seconds,
                        "processed": len(rows),
                        "sat_count": sat_count,
                        "rows": rows,
                    },
                )

    payload = {
        "status": "complete",
        **catalogue,
        "catalogue_seconds": catalogue_seconds,
        "solver": "cadical195",
        "cnf": str(args.cnf),
        "processed": len(rows),
        "sat_count": sat_count,
        "unsat_count": len(rows) - sat_count,
        "solve_seconds": time.perf_counter() - solve_started,
        "rows": rows,
    }
    checkpoint(args.output, payload)
    print(
        f"complete roles={len(rows)} SAT={sat_count} "
        f"UNSAT={len(rows) - sat_count}",
        flush=True,
    )


if __name__ == "__main__":
    main()
