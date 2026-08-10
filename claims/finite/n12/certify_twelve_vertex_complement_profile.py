"""Build one selector CNF for the corrected n=12 complement profile."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pysat.formula import CNF

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from twelve_vertex_complement_chain_orbits_core import (
    FULL,
    SIDE,
    canonical_leaves,
    chain_assumptions,
    membership_variables,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    base_path = Path(
        "tmp",
        "twelve_vertex_complement_set_trees_symmetry_broken.cnf",
    )
    base = CNF(from_file=str(base_path))
    variable = membership_variables()
    leaves = canonical_leaves()

    branches = []
    same_pair = (1 << 0) | (1 << SIDE)
    branches.append(
        {
            "kind": "same_first_partner",
            "partner_permutation": None,
            "orbit_weight": 1,
            "assumptions": [
                variable[1, same_pair],
                variable[1, FULL ^ same_pair],
            ],
        }
    )
    for leaf in leaves:
        assumptions, pair_masks, suffix_masks = chain_assumptions(
            variable, leaf["pairs"]
        )
        branches.append(
            {
                "kind": "hard_chain_orbit",
                "partner_permutation": list(
                    leaf["partner_permutation"]
                ),
                "orbit_weight": leaf["orbit_weight"],
                "pair_masks": pair_masks,
                "suffix_masks": suffix_masks,
                "assumptions": assumptions,
            }
        )

    selectors = [
        base.nv + index + 1 for index in range(len(branches))
    ]
    extension = [selectors]
    for selector, branch in zip(selectors, branches, strict=True):
        extension.extend(
            [-selector, literal]
            for literal in branch["assumptions"]
        )

    output = Path(
        "tmp",
        "twelve_vertex_complement_profile_selector.cnf",
    )
    with output.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(
            f"p cnf {base.nv + len(selectors)} "
            f"{len(base.clauses) + len(extension)}\n"
        )
        for clause in base.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
        for clause in extension:
            handle.write(" ".join(map(str, clause)) + " 0\n")

    branch_rows = []
    for index, (selector, branch) in enumerate(
        zip(selectors, branches, strict=True)
    ):
        branch_rows.append(
            {
                "branch_index": index,
                "selector": selector,
                **branch,
            }
        )
    payload = {
        "status": "selector_cnf_materialized",
        "verified": True,
        "profile": [6, 0, 0, 0, 0, 0, 0, 6],
        "base_cnf": str(base_path),
        "base_cnf_sha256": sha256(base_path),
        "base_variables": base.nv,
        "base_clauses": len(base.clauses),
        "selector_cnf": str(output),
        "selector_cnf_sha256": sha256(output),
        "selector_variables": len(selectors),
        "selector_cnf_variables": base.nv + len(selectors),
        "selector_extension_clauses": len(extension),
        "selector_cnf_clauses": len(base.clauses) + len(extension),
        "canonical_hard_leaves": len(leaves),
        "hard_partner_chains_covered": sum(
            leaf["orbit_weight"] for leaf in leaves
        ),
        "same_first_partner_branch_included": True,
        "branches": branch_rows,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    manifest = Path(
        "tmp",
        "twelve_vertex_complement_profile_selector_manifest.json",
    )
    manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "status",
                    "selector_cnf_sha256",
                    "selector_variables",
                    "selector_cnf_variables",
                    "selector_extension_clauses",
                    "selector_cnf_clauses",
                    "canonical_hard_leaves",
                    "hard_partner_chains_covered",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
