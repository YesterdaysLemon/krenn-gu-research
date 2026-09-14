"""Bounded discovery probe for necessary protected-scaffold support models.

SAT supplies Boolean supports, not weights. Accepted UNSAT evidence is the
separately audited portable RUP fixture, not this solver's return value.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
from krenn_gu.scaffold_source import VARIABLES, build  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("pair", "binary", "binary-shores", "binary-shores-minority", "four-minority", "full"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--generate-only", action="store_true",
                        help="write canonical CNF for a standalone solver; no python-sat required")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    cnf, words, histogram, polynomial_hash, products = build(args.mode)
    cnf_path = args.output_dir / "instance.cnf"
    cnf_path.write_bytes(cnf.dimacs())
    if args.generate_only:
        result = {"status": "GENERATED_NOT_SOLVED", "mode": args.mode,
                  "word_count": len(words), "variables": cnf.nv, "clauses": len(cnf.clauses),
                  "equation_sha256": polynomial_hash,
                  "cnf_sha256": hashlib.sha256(cnf.dimacs()).hexdigest()}
        (args.output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return
    # The native Windows proof bindings have returned truncated proof data.
    # Treat output as discovery only; prefer --generate-only plus a checked
    # standalone solver when this occurs. Never accept the return value alone.
    from pysat.solvers import Glucose4

    with Glucose4(bootstrap_with=cnf.clauses, with_proof=True) as solver:
        sat = solver.solve()
        if sat:
            model = solver.get_model()
            values = set(model)
            assert all(any(lit in values for lit in clause) for clause in cnf.clauses)
            proof = None
        else:
            model = None
            proof = solver.get_proof()
    result = {
        "status": "SAT_SUPPORT_NOT_WEIGHTS" if sat else "UNSAT_SOLVER_PENDING_AUDIT",
        "solver": "Glucose4",
        "mode": args.mode, "word_count": len(words), "crossing_variables": len(VARIABLES),
        "variables": cnf.nv, "clauses": len(cnf.clauses), "monomial_variables": products,
        "row_term_histogram": dict(sorted(histogram.items())),
        "equation_sha256": polynomial_hash,
        "cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
        "elapsed_seconds": time.monotonic() - start,
    }
    if sat:
        result["nonzero_crossing_entries"] = [VARIABLES[v - 1] for v in range(1, 97) if v in values]
        (args.output_dir / "assignment.json").write_text(json.dumps(model) + "\n", encoding="utf-8")
    else:
        data = ("\n".join(proof) + "\n").encode()
        (args.output_dir / "proof.drat").write_bytes(data)
        result["proof_sha256"] = hashlib.sha256(data).hexdigest()
    (args.output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
