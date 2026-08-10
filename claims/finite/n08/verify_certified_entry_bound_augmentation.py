"""Independently reconstruct a certified entry-bound CNF augmentation."""

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


def compare(
    base_cnf: Path,
    output_cnf: Path,
    expected_tail: bytes,
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
        if output.read() != expected_tail:
            raise AssertionError("cardinality tail differs from reconstruction")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    base_cnf = Path(manifest["base_cnf"])
    output_cnf = Path(manifest["output_cnf"])
    graph6 = Path(manifest["graph6"])
    entry_audit_path = Path(manifest["entry_bound_audit"])
    family_audit_path = Path(manifest["family_audit"])
    entry_audit = json.loads(
        entry_audit_path.read_text(encoding="utf-8")
    )
    family_audit = json.loads(
        family_audit_path.read_text(encoding="utf-8")
    )

    bindings = [
        (base_cnf, "base_cnf_sha256"),
        (output_cnf, "output_cnf_sha256"),
        (graph6, "graph6_sha256"),
        (entry_audit_path, "entry_bound_audit_sha256"),
        (family_audit_path, "family_audit_sha256"),
    ]
    for path, key in bindings:
        if sha256(path) != manifest[key]:
            raise AssertionError(f"{path} hash changed")
    if entry_audit.get("verified") is not True:
        raise AssertionError("entry-bound audit is not verified")
    if family_audit.get("verified") is not True:
        raise AssertionError("family audit is not verified")
    if int(entry_audit["maximum_entries"]) != (
        int(manifest["max_entries"]) + 1
    ):
        raise AssertionError("entry-bound theorem no longer justifies cap")
    if (
        int(family_audit["labelled_supports"]) != 7938
        or int(family_audit["support_orbits"]) != 86
    ):
        raise AssertionError("equality-family audit coverage changed")

    roles, catalogue = canonical_normalized_killer_skeletons(
        graph6,
        target_edges=int(manifest["target_edges"]),
    )
    ordered = ordered_role_skeletons(roles)
    for key, value in catalogue.items():
        if manifest[key] != value:
            raise AssertionError(f"catalogue field {key} changed")
    if any(
        any(
            sum(vertex in edge for edge in skeleton) != 5
            for vertex in range(8)
        )
        for skeleton in ordered
    ):
        raise AssertionError("an exact-20 role is not 5-regular")

    old_variables, old_clauses = header(base_cnf)
    new_variables, new_clauses = header(output_cnf)
    if (old_variables, old_clauses) != (
        int(manifest["old_variables"]),
        int(manifest["old_clauses"]),
    ):
        raise AssertionError("base header changed")
    system = EquationSystem(8, 3)
    cardinality = CardEnc.atmost(
        lits=list(range(1, system.variable_count + 1)),
        bound=int(manifest["max_entries"]),
        top_id=old_variables,
        encoding=EncType.seqcounter,
    )
    tail = b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in cardinality.clauses
    )
    expected_variables = int(cardinality.nv)
    expected_clauses = old_clauses + len(cardinality.clauses)
    if (new_variables, new_clauses) != (
        expected_variables,
        expected_clauses,
    ):
        raise AssertionError("output header changed")
    if (
        expected_variables - old_variables
        != int(manifest["cardinality_auxiliary_variables"])
        or len(cardinality.clauses)
        != int(manifest["cardinality_clauses"])
    ):
        raise AssertionError("cardinality metadata changed")
    compare(base_cnf, output_cnf, tail)

    payload = {
        "verified": True,
        "scope": manifest["scope"],
        "prize_search_sound": bool(manifest["prize_search_sound"]),
        "all_roles_5_regular": True,
        "canonical_role_skeletons": len(ordered),
        "max_entries": int(manifest["max_entries"]),
        "variables": new_variables,
        "clauses": new_clauses,
        "cardinality_auxiliary_variables": (
            expected_variables - old_variables
        ),
        "cardinality_clauses": len(cardinality.clauses),
        "base_cnf_sha256": manifest["base_cnf_sha256"],
        "output_cnf_sha256": manifest["output_cnf_sha256"],
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
