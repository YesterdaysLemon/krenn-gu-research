"""Exhaust cubic forced-rank-one half-edge colourings up to symmetry."""

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
import itertools
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from krenn_gu.killer_pattern_certificates import (
    audit_pattern,
    monochromatic_matchings,
    pattern_arcs,
)
from krenn_gu.rankone_support_sat import solve_with_minisat, support_cnf
from krenn_gu.search_prism_stratum import K33_MATCHINGS, PRISM_MATCHINGS
from krenn_gu.search_witness import EquationSystem

Edge = tuple[int, int]
PatternTuple = tuple[int, ...]


def graph_edges(
    matchings: tuple[tuple[Edge, ...], ...]
) -> frozenset[Edge]:
    return frozenset(edge for matching in matchings for edge in matching)


def graph_automorphisms(edges: frozenset[Edge]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for permutation in itertools.permutations(range(6)):
        image = frozenset(
            tuple(sorted((permutation[u], permutation[v])))
            for u, v in edges
        )
        if image == edges:
            result.append(permutation)
    return result


def transform_pattern(
    pattern: PatternTuple,
    vertex_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> PatternTuple:
    result = [[-1] * 3 for _ in range(6)]
    for vertex in range(6):
        for colour in range(3):
            result[vertex_permutation[vertex]][colour_permutation[colour]] = (
                vertex_permutation[pattern[3 * vertex + colour]]
            )
    return tuple(value for row in result for value in row)


def canonical_pattern(
    pattern: PatternTuple,
    automorphisms: list[tuple[int, ...]],
) -> PatternTuple:
    colour_permutations = tuple(itertools.permutations(range(3)))
    return min(
        transform_pattern(pattern, vertex_permutation, colour_permutation)
        for vertex_permutation in automorphisms
        for colour_permutation in colour_permutations
    )


def nested_pattern(pattern: PatternTuple) -> list[list[int]]:
    return [list(pattern[start : start + 3]) for start in range(0, 18, 3)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stratum", choices=("k33", "prism"), default="k33")
    parser.add_argument("--support-sat", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument(
        "--feasibility-only",
        action="store_true",
        help="skip the slower unique-mixed-matching certificate",
    )
    parser.add_argument("--tmp", type=Path, default=Path("tmp"))
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    matchings = K33_MATCHINGS if args.stratum == "k33" else PRISM_MATCHINGS
    edges = graph_edges(matchings)
    automorphisms = graph_automorphisms(edges)
    neighbours = [
        tuple(
            sorted(
                other
                for edge in edges
                if vertex in edge
                for other in edge
                if other != vertex
            )
        )
        for vertex in range(6)
    ]
    choices = [tuple(itertools.permutations(row)) for row in neighbours]

    status_counts: Counter[str] = Counter()
    representatives: Counter[PatternTuple] = Counter()
    for rows in itertools.product(*choices):
        pattern = [list(row) for row in rows]
        if args.feasibility_only:
            arcs = pattern_arcs(pattern)
            feasible = all(
                monochromatic_matchings(system, arcs, colour)
                for colour in range(3)
            )
            status = (
                "requires_algebraic_analysis"
                if feasible
                else "monochromatically_infeasible"
            )
        else:
            audit = audit_pattern(system, pattern)
            status = str(audit["status"])
        status_counts[status] += 1
        if status == "requires_algebraic_analysis":
            flat = tuple(value for row in rows for value in row)
            representatives[canonical_pattern(flat, automorphisms)] += 1

    args.tmp.mkdir(parents=True, exist_ok=True)
    representative_items = list(enumerate(sorted(representatives.items())))

    def analyze_representative(
        item: tuple[int, tuple[PatternTuple, int]]
    ) -> dict[str, object]:
        index, (pattern, orbit_size) = item
        row: dict[str, object] = {
            "orbit_size": orbit_size,
            "pattern": nested_pattern(pattern),
        }
        if args.support_sat:
            cnf = support_cnf(system, row["pattern"], set(edges))
            support_status = solve_with_minisat(
                cnf, args.tmp / f"{args.stratum}_orbit_{index}.cnf"
            )
            row.update(
                {
                    "support_status": support_status,
                    "cnf_variables": cnf.variable_count,
                    "cnf_clauses": len(cnf.clauses),
                }
            )
        return row

    if args.jobs > 1 and args.support_sat:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            representative_rows = list(
                executor.map(analyze_representative, representative_items)
            )
    else:
        representative_rows = [
            analyze_representative(item) for item in representative_items
        ]
    support_counts = Counter(
        str(row["support_status"])
        for row in representative_rows
        if "support_status" in row
    )

    print(
        json.dumps(
            {
                "stratum": args.stratum,
                "labelings": 6**6,
                "graph_automorphisms": len(automorphisms),
                "status_counts": dict(status_counts),
                "survivor_orbits": len(representatives),
                "support_counts": dict(support_counts),
                "representatives": representative_rows,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
