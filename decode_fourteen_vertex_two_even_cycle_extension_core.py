"""Decode an exploratory C6+C8/C4+C10 DIMACS extension core as edge rules."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import contiguous_cycles
from explore_random_even_cycle_forks import cycle_edges


ROLE_NAMES = ("first", "second", "third")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument(
        "--partition", type=int, nargs=2, required=True, metavar=("A", "B")
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if sum(args.partition) != 14 or any(n % 2 for n in args.partition):
        raise ValueError("partition must be two even parts summing to 14")
    core = json.loads(args.core.read_text(encoding="utf-8"))
    assumption = int(core["assumption"])
    cycles = contiguous_cycles(tuple(args.partition))
    full_edges = {
        edge for cycle in cycles for edge in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        edge
        for edge in itertools.combinations(range(14), 2)
        if edge not in full_edges
    )
    edge_count = len(eligible_edges)
    edge_variable_limit = 3 * edge_count

    decoded_clauses: list[dict[str, object]] = []
    unit_forbidden: list[dict[str, object]] = []
    for source_index, clause in zip(
        core["clause_indices"], core["clauses"], strict=True
    ):
        nonselector = [
            int(literal)
            for literal in clause
            if abs(int(literal)) != abs(assumption)
        ]
        if len(nonselector) + 1 != len(clause):
            raise AssertionError("core clause lacks the target selector literal")
        forbidden: list[dict[str, object]] = []
        for literal in nonselector:
            variable = abs(literal)
            if not 1 <= variable <= edge_variable_limit:
                raise AssertionError(
                    f"unexpected non-edge variable {variable} in core"
                )
            zero_based = variable - 1
            role, edge_id = divmod(zero_based, edge_count)
            item = {
                "variable": variable,
                "role": role,
                "role_name": ROLE_NAMES[role],
                "edge": list(eligible_edges[edge_id]),
                "value": literal < 0,
            }
            forbidden.append(item)
        row = {
            "source_extension_clause_index": int(source_index),
            "reduced_width": len(nonselector),
            "forbidden_assignment": forbidden,
        }
        decoded_clauses.append(row)
        if len(forbidden) == 1:
            unit_forbidden.append(forbidden[0])

    payload = {
        "status": "decoded_two_even_cycle_extension_core",
        "core": str(args.core),
        "partition": args.partition,
        "cycles": [list(cycle) for cycle in cycles],
        "eligible_edges": edge_count,
        "assumption_selector": assumption,
        "meaning": (
            "Each row is a partial edge-role assignment forbidden when the "
            "target first-factor selector is active."
        ),
        "decoded_clauses": decoded_clauses,
        "unit_forbidden_assignments": unit_forbidden,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
