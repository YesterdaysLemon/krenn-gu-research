"""Audit a role-pinned static no-binomial CNF with an entry bound."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.card import CardEnc, EncType

from eight_vertex_skeleton_batch import (
    canonical_normalized_killer_skeletons,
    ordered_role_skeletons,
)
from search_witness import EquationSystem


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        fields = handle.readline().split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise AssertionError(f"{path} is not a DIMACS CNF")
    return int(fields[2]), int(fields[3])


def expected_tail(
    manifest: dict[str, object],
    system: EquationSystem,
    old_variables: int,
) -> tuple[bytes, int, int, int]:
    skeleton = {
        tuple(map(int, edge)) for edge in manifest["skeleton_edges"]
    }
    graph_first = system.variable_count + 1
    rows = [
        (
            f"{graph_first + edge_index} 0\n"
            if edge in skeleton
            else f"-{graph_first + edge_index} 0\n"
        ).encode("ascii")
        for edge_index, edge in enumerate(system.edges)
    ]
    cardinality = CardEnc.atmost(
        lits=list(range(1, system.variable_count + 1)),
        bound=int(manifest["max_entries"]),
        top_id=old_variables,
        encoding=EncType.seqcounter,
    )
    rows.extend(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in cardinality.clauses
    )
    return (
        b"".join(rows),
        int(cardinality.nv),
        len(cardinality.clauses),
        int(cardinality.nv) - old_variables,
    )


def compare_prefix_and_tail(
    base_cnf: Path,
    output_cnf: Path,
    expected: bytes,
) -> None:
    with base_cnf.open("rb") as base, output_cnf.open("rb") as output:
        base.readline()
        output.readline()
        while True:
            chunk = base.read(8 * 1024 * 1024)
            if not chunk:
                break
            if output.read(len(chunk)) != chunk:
                raise AssertionError("output changed a base-CNF body byte")
        if output.read() != expected:
            raise AssertionError(
                "role/cardinality tail differs from reconstruction"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    base_manifest_path = Path(manifest["base_manifest"])
    base_manifest = json.loads(
        base_manifest_path.read_text(encoding="utf-8")
    )
    base_cnf = Path(manifest["base_cnf"])
    output_cnf = Path(manifest["output_cnf"])
    graph6 = Path(manifest["graph6"])

    if sha256(base_manifest_path) != manifest["base_manifest_sha256"]:
        raise AssertionError("base manifest hash changed")
    if sha256(graph6) != manifest["graph6_sha256"]:
        raise AssertionError("graph6 catalogue hash changed")
    observed_base_hash = sha256(base_cnf)
    if observed_base_hash != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash changed")
    if observed_base_hash != base_manifest["output_cnf_sha256"]:
        raise AssertionError("base manifest does not bind the base CNF")
    observed_output_hash = sha256(output_cnf)
    if observed_output_hash != manifest["output_cnf_sha256"]:
        raise AssertionError("output CNF hash changed")

    old_variables, old_clauses = header(base_cnf)
    new_variables, new_clauses = header(output_cnf)
    if (old_variables, old_clauses) != (
        int(manifest["old_variables"]),
        int(manifest["old_clauses"]),
    ):
        raise AssertionError("base header differs from manifest")

    roles, catalogue = canonical_normalized_killer_skeletons(
        graph6,
        target_edges=int(manifest["target_edges"]),
    )
    ordered = ordered_role_skeletons(roles)
    role_index = int(manifest["role_index"])
    expected_skeleton = set(ordered[role_index])
    observed_skeleton = {
        tuple(map(int, edge)) for edge in manifest["skeleton_edges"]
    }
    if expected_skeleton != observed_skeleton:
        raise AssertionError("role skeleton differs from catalogue")
    for key, value in catalogue.items():
        if manifest[key] != value:
            raise AssertionError(f"catalogue field {key} changed")

    system = EquationSystem(8, 3)
    tail, expected_variables, cardinality_clauses, auxiliary = (
        expected_tail(manifest, system, old_variables)
    )
    if expected_variables != new_variables:
        raise AssertionError("new variable count changed")
    if cardinality_clauses != int(
        manifest["cardinality_clauses"]
    ):
        raise AssertionError("cardinality clause count changed")
    if auxiliary != int(manifest["cardinality_auxiliary_variables"]):
        raise AssertionError("cardinality auxiliary count changed")
    expected_clauses = (
        old_clauses + len(system.edges) + cardinality_clauses
    )
    if expected_clauses != new_clauses:
        raise AssertionError("new clause count changed")
    if (new_variables, new_clauses) != (
        int(manifest["new_variables"]),
        int(manifest["new_clauses"]),
    ):
        raise AssertionError("output header differs from manifest")
    compare_prefix_and_tail(base_cnf, output_cnf, tail)

    payload = {
        "verified": True,
        "scope": manifest["scope"],
        "necessary_conditions_only": bool(
            manifest["necessary_conditions_only"]
        ),
        "stronger_than_prize_hypothesis": bool(
            manifest["stronger_than_prize_hypothesis"]
        ),
        "role_index": role_index,
        "skeleton_edges": [
            list(edge) for edge in sorted(observed_skeleton)
        ],
        "max_entries": int(manifest["max_entries"]),
        "variables": new_variables,
        "clauses": new_clauses,
        "role_unit_clauses": len(system.edges),
        "cardinality_encoding": "sequential_counter",
        "cardinality_auxiliary_variables": auxiliary,
        "cardinality_clauses": cardinality_clauses,
        "base_cnf_sha256": observed_base_hash,
        "output_cnf_sha256": observed_output_hash,
        "output_cnf_prefix_and_tail_reconstructed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
