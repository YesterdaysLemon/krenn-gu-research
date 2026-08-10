"""Inspect a SAT support model for a generic rank-one prism branch."""

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
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n06/certificate-chain")

import argparse
import json

import numpy as np

from krenn_gu.enumerate_cubic_rankone import graph_edges, nested_pattern
from prism_orbit_batch import complement_edge_blocks
from krenn_gu.prism_orbit_screen import prism_orbit_representatives
from krenn_gu.rankone_support_sat import support_cnf
from krenn_gu.search_killer_patterns import active_mask_for_pattern
from krenn_gu.search_prism_stratum import PRISM_MATCHINGS
from krenn_gu.search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=1)
    args = parser.parse_args()

    from pysat.solvers import Minisat22

    system = EquationSystem(6, 3)
    pattern = prism_orbit_representatives()[args.orbit]
    nested = nested_pattern(pattern)
    active = active_mask_for_pattern(system, nested)
    active_indices = [
        int(flat_index) for flat_index in np.flatnonzero(active)
    ]
    cnf = support_cnf(
        system,
        nested,
        set(graph_edges(PRISM_MATCHINGS)),
        rectangular_support_edges=set(complement_edge_blocks()[0]),
    )
    with Minisat22(bootstrap_with=cnf.clauses) as solver:
        if not solver.solve():
            raise ValueError("generic support CNF is UNSAT")
        model = set(solver.get_model() or ())
        forced_nonzero_entries = []
        for edge in complement_edge_blocks()[0]:
            edge_index = system.edge_index[edge]
            for row in range(3):
                for column in range(3):
                    flat_index = edge_index * 9 + 3 * row + column
                    variable = active_indices.index(flat_index) + 1
                    if not solver.solve(assumptions=[-variable]):
                        forced_nonzero_entries.append(
                            {
                                "edge": list(edge),
                                "entry": [row, column],
                            }
                        )
    blocks = []
    for edge in system.edges:
        edge_index = system.edge_index[edge]
        support = []
        for row in range(3):
            for column in range(3):
                flat_index = edge_index * 9 + 3 * row + column
                if flat_index not in active_indices:
                    continue
                variable = active_indices.index(flat_index) + 1
                if variable in model:
                    support.append([row, column])
        if support:
            blocks.append({"edge": list(edge), "support": support})
    print(
        json.dumps(
            {
                "orbit": args.orbit,
                "pattern": nested,
                "nonzero_blocks": blocks,
                "forced_nonzero_free_entries": forced_nonzero_entries,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
