"""Incrementally decide all exposed matching chains in the hard n=12 profile.

The base CNF fixes an exposed identity matching in tree 0 and its first
complement.  Expanding tree 1 at row 0 either selects the same identity
edge (an immediate two-colour partition) or, by residual S_5 symmetry,
selects column 1.  Recursively expanding at rows 1,...,5 yields one of
5! complete partner permutations.  This script tests those 120 chains
as assumptions in one incremental CaDiCaL instance.
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
FULL = (1 << N) - 1
LEFT = (1 << (N // 2)) - 1


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
        == (mask >> (N // 2)).bit_count()
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


def chain_assumptions(variable, permutation):
    remainder = FULL
    assumptions = []
    pairs = []
    suffixes = []
    for row, column in enumerate(permutation):
        pair = (1 << row) | (1 << (column + N // 2))
        if not pair & remainder == pair:
            raise AssertionError("matching chain reused a vertex")
        pairs.append(pair)
        assumptions.append(variable[1, pair])
        remainder ^= pair
        if remainder:
            suffixes.append(remainder)
            assumptions.append(variable[1, remainder])
    if remainder:
        raise AssertionError("matching chain did not cover the profile")
    return assumptions, pairs, suffixes


def main() -> None:
    cnf_path = Path(
        "tmp",
        "twelve_vertex_complement_set_trees_symmetry_broken.cnf",
    )
    cnf = CNF(from_file=str(cnf_path))
    variable = membership_variables()
    rows = []
    started = time.perf_counter()
    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        for index, tail in enumerate(
            itertools.permutations((0, 2, 3, 4, 5))
        ):
            permutation = (1,) + tail
            assumptions, pairs, suffixes = chain_assumptions(
                variable, permutation
            )
            branch_started = time.perf_counter()
            satisfiable = solver.solve(assumptions=assumptions)
            elapsed = time.perf_counter() - branch_started
            row = {
                "chain_index": index,
                "partner_permutation": list(permutation),
                "pair_masks": pairs,
                "suffix_masks": suffixes,
                "status": "SAT" if satisfiable else "UNSAT",
                "solve_seconds": elapsed,
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "chain": index,
                        "permutation": permutation,
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
    payload = {
        "status": (
            "complete_chain_exhaustion"
            if len(rows) == 120 and sat == 0
            else "chain_model_found"
            if sat
            else "incomplete_chain_exhaustion"
        ),
        "verified": len(rows) == 120 and sat == 0,
        "profile": [6, 0, 0, 0, 0, 0, 0, 6],
        "base_cnf": str(cnf_path),
        "base_cnf_sha256": sha256(cnf_path),
        "base_variables": cnf.nv,
        "base_clauses": len(cnf.clauses),
        "first_tree_identity_matching_fixed": True,
        "second_tree_first_partner_fixed_to_column_1": True,
        "chains_expected": 120,
        "chains_decided": len(rows),
        "unsat_chains": unsat,
        "sat_chains": sat,
        "elapsed_seconds": time.perf_counter() - started,
        "chains": rows,
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "twelve_vertex_complement_matching_chains_explored.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: payload[key] for key in (
        "status",
        "verified",
        "chains_decided",
        "unsat_chains",
        "sat_chains",
        "elapsed_seconds",
    )}, indent=2))


if __name__ == "__main__":
    main()
