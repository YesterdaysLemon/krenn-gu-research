"""Append one complete entry-support assignment to a DIMACS CNF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from augment_no_binomial_amplitudes import header, sha256
from eight_vertex_degree4_cegar import write_augmented_cnf
from search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--support-manifest", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(
        args.support_manifest.read_text(encoding="utf-8")
    )
    support_row = source.get("witness", source)
    selected = set(map(int, support_row["selected_flat_indices"]))
    system = EquationSystem(8, 3)
    if any(
        flat < 0 or flat >= system.variable_count
        for flat in selected
    ):
        raise ValueError("support contains an out-of-range entry")
    units = [
        (variable if variable - 1 in selected else -variable,)
        for variable in range(1, system.variable_count + 1)
    ]

    old_variables, old_clauses = header(args.base_cnf)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    write_augmented_cnf(args.base_cnf, args.output_cnf, units)
    new_variables, new_clauses = header(args.output_cnf)
    if (new_variables, new_clauses) != (
        old_variables,
        old_clauses + len(units),
    ):
        raise AssertionError("exact-support extension header changed")

    payload = {
        "scope": "one exact 252-variable entry-support assignment",
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "support_manifest": str(args.support_manifest),
        "support_manifest_sha256": sha256(args.support_manifest),
        "selected_entries": len(selected),
        "selected_flat_indices": sorted(selected),
        "unit_clauses": len(units),
        "variables": new_variables,
        "clauses": new_clauses,
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
    }
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
