"""Condition a DIMACS formula on membership in a selector set.

The input encoding is expected to impose its own selector semantics.  This
utility only appends the positive clause saying that at least one of the
listed selector variables is true and records exact hashes for replay.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from pysat.formula import CNF


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument(
        "--selector", type=int, action="append", required=True
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    selectors = sorted(set(args.selector))
    if any(variable < 1 for variable in selectors):
        raise ValueError("selectors must be positive DIMACS variables")

    formula = CNF(from_file=str(args.cnf))
    if selectors[-1] > formula.nv:
        raise ValueError("selector exceeds the input variable count")
    input_clauses = len(formula.clauses)
    formula.append(selectors)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    formula.to_file(str(args.output_cnf))
    payload = {
        "status": "DIMACS_conditioned_on_selector_set",
        "input_cnf": str(args.cnf),
        "input_cnf_sha256": sha256(args.cnf),
        "input_cnf_variables": formula.nv,
        "input_cnf_clauses": input_clauses,
        "selector_clause": selectors,
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_cnf_variables": formula.nv,
        "output_cnf_clauses": len(formula.clauses),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
