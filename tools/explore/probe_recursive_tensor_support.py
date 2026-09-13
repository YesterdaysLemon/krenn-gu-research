"""Bounded full-model support diagnostic; a SAT assignment is not a witness."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys as _bootstrap_sys
import time
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from pysat.solvers import Cadical195, Glucose4  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--output", type=_BootstrapPath, required=True)
    parser.add_argument("--solver", choices=("cadical195", "glucose4"), default="cadical195")
    parser.add_argument("--no-killers", action="store_true")
    parser.add_argument("--no-root-symmetry", action="store_true")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    instance = build_recursive_tensor_support_cnf(
        args.n, column_killers=not args.no_killers,
        fix_root_killers=not args.no_root_symmetry and not args.no_killers,
    )
    built = time.monotonic() - started
    print(json.dumps({"stage": "built", "seconds": built, "n": args.n,
                      "variables": instance.cnf.nv, "clauses": len(instance.cnf.clauses)}), flush=True)
    dimacs = args.output.with_suffix(".cnf")
    instance.cnf.to_file(str(dimacs))
    payload = {
        "model": "full_pair_source_recursive_coefficient_support",
        "scope": "necessary_condition_not_weight_realization",
        "n": args.n, "column_killers": not args.no_killers,
        "root_symmetry": not args.no_root_symmetry and not args.no_killers,
        "variables": instance.cnf.nv, "clauses": len(instance.cnf.clauses),
        "clause_counts": instance.clause_counts, "build_seconds": built,
        "dimacs": str(dimacs.resolve()), "dimacs_sha256": sha256(dimacs),
        "solver": args.solver, "result": "NOT_FINISHED",
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"stage": "solving", "dimacs_sha256": payload["dimacs_sha256"]}), flush=True)
    started = time.monotonic()
    solver_type = {"cadical195": Cadical195, "glucose4": Glucose4}[args.solver]
    with solver_type(bootstrap_with=instance.cnf.clauses) as solver:
        sat = solver.solve()
        payload.update(result="SAT" if sat else "UNSAT", solve_seconds=time.monotonic() - started,
                       stats=solver.accum_stats())
        if sat:
            model = solver.get_model()
            positive = {literal for literal in model if literal > 0}
            if not all(any((literal > 0) == (abs(literal) in positive) for literal in clause)
                       for clause in instance.cnf.clauses):
                raise RuntimeError("returned assignment fails generated CNF")
            model_path = args.output.with_suffix(".model.json")
            model_path.write_text(json.dumps(model) + "\n", encoding="utf-8")
            payload.update(model_path=str(model_path.resolve()), model_sha256=sha256(model_path),
                           nonzero_entries=[key for key, variable in instance.entries.items()
                                            if variable in positive], assignment_checked=True)
    payload["evidence"] = "checked_boolean_assignment" if sat else "solver_status_no_checked_proof"
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
