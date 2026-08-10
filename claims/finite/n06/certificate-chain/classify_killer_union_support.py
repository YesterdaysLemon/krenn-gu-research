"""Classify support-feasible selected killer-edge union graphs on six vertices.

The selected union has minimum degree three, so its complement has maximum
degree two.  With 9--12 used edges, the complement is one of the fifteen
disjoint-union-of-paths-and-cycles types listed below.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from global_support_sat import global_support_cnf
from rankone_support_sat import solve_with_cadical


CASES = {
    # 12 used edges, 3 missing.
    "12_used__missing_C3": "01,12,02",
    "12_used__missing_P4": "01,12,23",
    "12_used__missing_P3_K2": "01,12,34",
    "12_used__missing_3K2": "01,23,45",
    # 11 used edges, 4 missing.
    "11_used__missing_C4": "01,12,23,03",
    "11_used__missing_C3_K2": "01,12,02,34",
    "11_used__missing_P5": "01,12,23,34",
    "11_used__missing_P4_K2": "01,12,23,45",
    "11_used__missing_2P3": "01,12,34,45",
    # 10 used edges, 5 missing.
    "10_used__missing_C5": "01,12,23,34,04",
    "10_used__missing_C4_K2": "01,12,23,03,45",
    "10_used__missing_C3_P3": "01,12,02,34,45",
    "10_used__missing_P6": "01,12,23,34,45",
    # 9 used edges, 6 missing.
    "9_used__missing_C6__prism": "01,12,23,34,45,05",
    "9_used__missing_2C3__K33": "01,12,02,34,45,35",
}


def parse_edges(text: str) -> frozenset[tuple[int, int]]:
    return frozenset(
        tuple(sorted((int(token[0]), int(token[1]))))
        for token in text.split(",")
    )


def component_signature(
    edges: frozenset[tuple[int, int]]
) -> tuple[tuple[str, int], ...]:
    adjacency = [set() for _ in range(6)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    unseen = set(range(6))
    components: list[tuple[str, int]] = []
    while unseen:
        root = min(unseen)
        stack = [root]
        vertices: set[int] = set()
        while stack:
            vertex = stack.pop()
            if vertex in vertices:
                continue
            vertices.add(vertex)
            stack.extend(adjacency[vertex] - vertices)
        unseen -= vertices
        edge_count = sum(len(adjacency[v]) for v in vertices) // 2
        kind = "C" if edge_count == len(vertices) else "P"
        components.append((kind, len(vertices)))
    return tuple(sorted(components))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--tmp", type=Path, default=Path("tmp"))
    args = parser.parse_args()
    args.tmp.mkdir(parents=True, exist_ok=True)

    def solve_case(item: tuple[str, str]) -> tuple[str, str]:
        name, edge_text = item
        cnf = global_support_cnf(
            False, missing_edges=parse_edges(edge_text)
        )
        status = solve_with_cadical(cnf, args.tmp / f"{name}.cnf")
        return name, status

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        results = dict(executor.map(solve_case, CASES.items()))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
