"""Decide canonical exposed-chain orbits in the hard n=12 profile.

The base CNF fixes a tree-0 identity matching and the complement of its
first edge.  For tree 1, choosing the same first edge immediately gives
a forbidden two-colour partition.  The residual S_5 action normalizes
every other first edge to row 0--column 1.

At each later step the set-tree axiom may be expanded at a fixed
remaining row.  The stabilizer of the earlier chain partitions the
possible partners into orbits, so it suffices to test one representative
per orbit and then continue with the representative's stabilizer.  The
result is 16 canonical leaves covering all 5! = 120 partner chains.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Cadical195

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n12")

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
    cnf_path = Path(
        "tmp",
        "twelve_vertex_complement_set_trees_symmetry_broken.cnf",
    )
    cnf = CNF(from_file=str(cnf_path))
    variable = membership_variables()
    leaves = canonical_leaves()
    rows = []
    started = time.perf_counter()

    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        for index, leaf in enumerate(leaves):
            assumptions, pair_masks, suffix_masks = chain_assumptions(
                variable, leaf["pairs"]
            )
            branch_started = time.perf_counter()
            satisfiable = solver.solve(assumptions=assumptions)
            elapsed = time.perf_counter() - branch_started
            row = {
                "leaf_index": index,
                "partner_permutation": list(
                    leaf["partner_permutation"]
                ),
                "pair_masks": pair_masks,
                "suffix_masks": suffix_masks,
                "orbit_weight": leaf["orbit_weight"],
                "status": "SAT" if satisfiable else "UNSAT",
                "solve_seconds": elapsed,
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "leaf": index,
                        "permutation": row[
                            "partner_permutation"
                        ],
                        "orbit_weight": row["orbit_weight"],
                        "status": row["status"],
                        "seconds": round(elapsed, 3),
                    }
                ),
                flush=True,
            )
            if satisfiable:
                model = solver.get_model()
                row["positive_model_literals"] = [
                    literal for literal in model if literal > 0
                ]
                break

    unsat = sum(row["status"] == "UNSAT" for row in rows)
    sat = sum(row["status"] == "SAT" for row in rows)
    covered_chains = sum(
        row["orbit_weight"]
        for row in rows
        if row["status"] == "UNSAT"
    )
    payload = {
        "status": (
            "complete_orbit_exhaustion"
            if len(rows) == len(leaves) and sat == 0
            else "orbit_model_found"
            if sat
            else "incomplete_orbit_exhaustion"
        ),
        "verified": len(rows) == len(leaves) and sat == 0,
        "profile": [6, 0, 0, 0, 0, 0, 0, 6],
        "base_cnf": str(cnf_path),
        "base_cnf_sha256": sha256(cnf_path),
        "base_variables": cnf.nv,
        "base_clauses": len(cnf.clauses),
        "first_tree_identity_matching_fixed": True,
        "same_first_partner_immediately_unsat": True,
        "second_tree_first_partner_fixed_to_column_1": True,
        "canonical_leaves_expected": 16,
        "canonical_leaves_decided": len(rows),
        "full_partner_chains_covered": covered_chains,
        "full_partner_chains_expected": 120,
        "unsat_leaves": unsat,
        "sat_leaves": sat,
        "elapsed_seconds": time.perf_counter() - started,
        "leaves": rows,
        "external_unsat_certificate": False,
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "twelve_vertex_complement_chain_orbits_explored.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "status",
                    "verified",
                    "canonical_leaves_decided",
                    "full_partner_chains_covered",
                    "unsat_leaves",
                    "sat_leaves",
                    "elapsed_seconds",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
