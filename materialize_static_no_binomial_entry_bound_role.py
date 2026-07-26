"""Pin one normalized role and bound support entries in a static CNF."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from pysat.card import CardEnc, EncType

from augment_no_binomial_amplitudes import header, sha256
from eight_vertex_skeleton_batch import (
    canonical_normalized_killer_skeletons,
    ordered_role_skeletons,
)
from search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-manifest", type=Path, required=True)
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--target-edges", type=int, default=20)
    parser.add_argument("--role-index", type=int, required=True)
    parser.add_argument("--max-entries", type=int, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()

    base_manifest = json.loads(
        args.base_manifest.read_text(encoding="utf-8")
    )
    base_cnf = Path(base_manifest["output_cnf"])
    if sha256(base_cnf) != base_manifest["output_cnf_sha256"]:
        raise AssertionError("static no-binomial CNF changed")
    old_variables, old_clauses = header(base_cnf)

    roles, catalogue = canonical_normalized_killer_skeletons(
        args.graph6,
        target_edges=args.target_edges,
    )
    ordered = ordered_role_skeletons(roles)
    if not 0 <= args.role_index < len(ordered):
        raise ValueError("role index is outside the normalized catalogue")
    skeleton = set(ordered[args.role_index])

    system = EquationSystem(8, 3)
    if system.variable_count != 252:
        raise AssertionError("unexpected entry-variable layout")
    graph_first = system.variable_count + 1
    role_units = [
        (
            graph_first + edge_index
            if edge in skeleton
            else -(graph_first + edge_index)
        )
        for edge_index, edge in enumerate(system.edges)
    ]
    cardinality = CardEnc.atmost(
        lits=list(range(1, system.variable_count + 1)),
        bound=args.max_entries,
        top_id=old_variables,
        encoding=EncType.seqcounter,
    )
    cardinality_clauses = [
        tuple(map(int, clause)) for clause in cardinality.clauses
    ]
    new_variables = int(cardinality.nv)
    new_clauses = (
        old_clauses + len(role_units) + len(cardinality_clauses)
    )

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with base_cnf.open("rb") as reader, args.output_cnf.open(
        "wb"
    ) as writer:
        reader.readline()
        writer.write(
            f"p cnf {new_variables} {new_clauses}\n".encode("ascii")
        )
        shutil.copyfileobj(reader, writer, length=8 * 1024 * 1024)
        for literal in role_units:
            writer.write(f"{literal} 0\n".encode("ascii"))
        for clause in cardinality_clauses:
            writer.write(
                (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            )
    if header(args.output_cnf) != (new_variables, new_clauses):
        raise AssertionError("materialized CNF header changed")

    payload = {
        "scope": (
            "one normalized n=8 exact-20 role with no two-term "
            "forbidden amplitude and bounded entry support"
        ),
        "necessary_conditions_only": True,
        "stronger_than_prize_hypothesis": True,
        **catalogue,
        "base_manifest": str(args.base_manifest),
        "base_manifest_sha256": sha256(args.base_manifest),
        "base_cnf": str(base_cnf),
        "base_cnf_sha256": sha256(base_cnf),
        "graph6": str(args.graph6),
        "graph6_sha256": sha256(args.graph6),
        "target_edges": args.target_edges,
        "role_index": args.role_index,
        "skeleton_edges": [list(edge) for edge in sorted(skeleton)],
        "entry_first_variable": 1,
        "entry_last_variable": system.variable_count,
        "max_entries": args.max_entries,
        "old_variables": old_variables,
        "old_clauses": old_clauses,
        "role_unit_clauses": len(role_units),
        "cardinality_encoding": "sequential_counter",
        "cardinality_auxiliary_variables": (
            new_variables - old_variables
        ),
        "cardinality_clauses": len(cardinality_clauses),
        "new_variables": new_variables,
        "new_clauses": new_clauses,
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
