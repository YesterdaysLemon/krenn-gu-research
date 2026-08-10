"""Add the certified exact-20 entry bound to a reusable base CNF.

The bound ``entries <= 83`` is sound on the 5-regular ``n=8,d=3`` exact-20
catalogue only after combining two separately audited results:

* the generic-killer count and equality-diagonal theorem bounds entries by
  84 and puts equality in the full-2-factor/diagonal-singleton family;
* the complete 7,938-support factor-lattice certificate excludes that
  equality family.
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
import json
import shutil
from pathlib import Path

from pysat.card import CardEnc, EncType

from eight_vertex_skeleton_batch import (
    canonical_normalized_killer_skeletons,
    ordered_role_skeletons,
)
from krenn_gu.search_witness import EquationSystem


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


def read_verified(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("verified") is not True:
        raise AssertionError(f"{path} is not a verified audit")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--target-edges", type=int, default=20)
    parser.add_argument("--max-entries", type=int, default=83)
    parser.add_argument("--entry-bound-audit", type=Path, required=True)
    parser.add_argument("--family-audit", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()

    entry_audit = read_verified(args.entry_bound_audit)
    family_audit = read_verified(args.family_audit)
    if int(entry_audit["maximum_entries"]) != args.max_entries + 1:
        raise AssertionError("entry-bound audit does not justify the cap")
    if int(family_audit["labelled_supports"]) != 7938:
        raise AssertionError("family audit does not cover 7,938 supports")
    if int(family_audit["support_orbits"]) != 86:
        raise AssertionError("family audit does not cover all 86 orbits")

    roles, catalogue = canonical_normalized_killer_skeletons(
        args.graph6,
        target_edges=args.target_edges,
    )
    ordered = ordered_role_skeletons(roles)
    for skeleton in ordered:
        degrees = [
            sum(vertex in edge for edge in skeleton)
            for vertex in range(8)
        ]
        if degrees != [5] * 8:
            raise AssertionError("the exact-20 role catalogue is not 5-regular")

    system = EquationSystem(8, 3)
    old_variables, old_clauses = header(args.base_cnf)
    cardinality = CardEnc.atmost(
        lits=list(range(1, system.variable_count + 1)),
        bound=args.max_entries,
        top_id=old_variables,
        encoding=EncType.seqcounter,
    )
    rows = [tuple(map(int, clause)) for clause in cardinality.clauses]
    new_variables = int(cardinality.nv)
    new_clauses = old_clauses + len(rows)

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("rb") as reader, args.output_cnf.open(
        "wb"
    ) as writer:
        reader.readline()
        writer.write(
            f"p cnf {new_variables} {new_clauses}\n".encode("ascii")
        )
        shutil.copyfileobj(reader, writer, length=8 * 1024 * 1024)
        for clause in rows:
            writer.write(
                (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            )
    if header(args.output_cnf) != (new_variables, new_clauses):
        raise AssertionError("output CNF header changed")

    payload = {
        "scope": (
            "certified exact-20 5-regular n=8,d=3 support search "
            "with the closed 84-entry equality boundary removed"
        ),
        "necessary_conditions_only": True,
        "prize_search_sound": True,
        **catalogue,
        "all_roles_5_regular": True,
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "graph6": str(args.graph6),
        "graph6_sha256": sha256(args.graph6),
        "target_edges": args.target_edges,
        "entry_bound_audit": str(args.entry_bound_audit),
        "entry_bound_audit_sha256": sha256(args.entry_bound_audit),
        "family_audit": str(args.family_audit),
        "family_audit_sha256": sha256(args.family_audit),
        "entry_first_variable": 1,
        "entry_last_variable": system.variable_count,
        "max_entries": args.max_entries,
        "old_variables": old_variables,
        "old_clauses": old_clauses,
        "cardinality_encoding": "sequential_counter",
        "cardinality_auxiliary_variables": (
            new_variables - old_variables
        ),
        "cardinality_clauses": len(rows),
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
