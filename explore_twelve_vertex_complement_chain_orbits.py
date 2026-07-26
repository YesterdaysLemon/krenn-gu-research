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
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Cadical195

N = 12
SIDE = N // 2
FULL = (1 << N) - 1
LEFT = (1 << SIDE) - 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def balanced(mask: int) -> bool:
    return (
        mask != 0
        and mask.bit_count() % 2 == 0
        and (mask & LEFT).bit_count()
        == (mask >> SIDE).bit_count()
    )


def membership_variables():
    variable = {}
    next_variable = 1
    for colour in range(3):
        for mask in range(1, FULL + 1):
            if balanced(mask):
                variable[colour, mask] = next_variable
                next_variable += 1
    return variable


def partner_orbits(values, group):
    remaining = set(values)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = sorted(
            {permutation[representative] for permutation in group}
        )
        if not set(orbit) <= remaining:
            raise AssertionError(
                "stabilizer did not preserve remaining columns"
            )
        orbits.append(orbit)
        remaining.difference_update(orbit)
    return orbits


def canonical_leaves():
    # The hard first pair fixes indices 0 and 1 under the diagonal
    # stabilizer.  The remaining four indices may still be permuted.
    initial_group = [
        permutation
        for permutation in itertools.permutations(range(SIDE))
        if permutation[0] == 0 and permutation[1] == 1
    ]
    leaves = []

    def recurse(
        pairs,
        used_rows,
        used_columns,
        group,
        orbit_weight,
    ):
        if len(pairs) == SIDE:
            leaves.append(
                {
                    "pairs": tuple(pairs),
                    "partner_permutation": tuple(
                        column for _row, column in pairs
                    ),
                    "orbit_weight": orbit_weight,
                }
            )
            return

        row = min(set(range(SIDE)) - set(used_rows))
        row_stabilizer = [
            permutation
            for permutation in group
            if permutation[row] == row
        ]
        available_columns = sorted(
            set(range(SIDE)) - set(used_columns)
        )
        for orbit in partner_orbits(
            available_columns, row_stabilizer
        ):
            column = orbit[0]
            next_group = [
                permutation
                for permutation in row_stabilizer
                if permutation[column] == column
            ]
            recurse(
                pairs + [(row, column)],
                used_rows + [row],
                used_columns + [column],
                next_group,
                orbit_weight * len(orbit),
            )

    recurse([(0, 1)], [0], [1], initial_group, 1)
    if len(leaves) != 16:
        raise AssertionError(f"expected 16 leaves, got {len(leaves)}")
    if sum(leaf["orbit_weight"] for leaf in leaves) != 120:
        raise AssertionError(
            "canonical leaves do not cover all 5! chains"
        )
    if len(
        {leaf["partner_permutation"] for leaf in leaves}
    ) != len(leaves):
        raise AssertionError("duplicate canonical leaves")
    return leaves


def chain_assumptions(variable, pairs):
    remainder = FULL
    assumptions = []
    pair_masks = []
    suffix_masks = []
    for row, column in pairs:
        pair = (1 << row) | (1 << (column + SIDE))
        if pair & remainder != pair:
            raise AssertionError("matching chain reused a vertex")
        pair_masks.append(pair)
        assumptions.append(variable[1, pair])
        remainder ^= pair
        if remainder:
            suffix_masks.append(remainder)
            assumptions.append(variable[1, remainder])
    if remainder:
        raise AssertionError("matching chain did not cover the profile")
    return assumptions, pair_masks, suffix_masks


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
