"""Bounded support-to-exact-cancellation loop for the full ternary model.

Use the repository process runner to impose wall-clock and memory limits.
No UNSAT status from this exploratory driver is an independently checked proof.
"""

from __future__ import annotations

import argparse
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

from pysat.solvers import Cadical195  # noqa: E402
from krenn_gu.full_tensor_cancellation import FullTensorCancellation  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from tools.explore.probe_recursive_tensor_support import sha256  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--max-relations", type=int, default=768)
    parser.add_argument("--output-dir", type=_BootstrapPath, required=True)
    args = parser.parse_args()
    if args.iterations <= 0 or args.max_relations <= 0:
        parser.error("iteration and relation bounds must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    if summary_path.exists():
        raise RuntimeError("use a fresh output directory; existing evidence is not overwritten")
    started = time.monotonic()
    instance = build_recursive_tensor_support_cnf(args.n)
    audit = FullTensorCancellation(instance)
    cnf_path = args.output_dir / "base.cnf"
    instance.cnf.to_file(str(cnf_path))
    payload = {"n": args.n, "scope": "full_pair_source_necessary_condition",
               "variables": instance.cnf.nv, "base_clauses": len(instance.cnf.clauses),
               "base_sha256": sha256(cnf_path), "iteration_limit": args.iterations,
               "max_relations": args.max_relations, "iterations": [], "result": "RUNNING"}
    print(json.dumps({"stage": "built", "n": args.n, "seconds": time.monotonic() - started}), flush=True)

    def save():
        summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    save()
    learned = []
    with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
        for iteration in range(args.iterations):
            begin = time.monotonic()
            if not solver.solve():
                payload["result"] = "UNSAT_SOLVER_STATUS_NO_CHECKED_PROOF"
                break
            model = solver.get_model()
            positive = {literal for literal in model if literal > 0}
            if not all(any((literal > 0) == (abs(literal) in positive) for literal in clause)
                       for clause in itertools_chain(instance.cnf.clauses, learned)):
                raise AssertionError("SAT assignment failed clause replay")
            support = [variable if variable in positive else -variable
                       for variable in instance.entries.values()]
            prefix = args.output_dir / f"iteration-{iteration:03d}"
            prefix.with_suffix(".support.json").write_text(json.dumps(support) + "\n", encoding="utf-8")
            record = {"iteration": iteration, "nonzero_entries": sum(v > 0 for v in support),
                      "solver_stats": solver.accum_stats(), "assignment_checked": True}
            try:
                certificate = audit.find_obstruction(support, max_relations=args.max_relations)
            except ValueError as error:
                if "explicit Smith bounds" not in str(error):
                    raise
                record.update(result="SMITH_BOUND", detail=str(error))
                payload["iterations"].append(record)
                payload["result"] = "BOUNDED_QUOTIENT_CHECK_INCOMPLETE"
                save()
                print(json.dumps(record), flush=True)
                break
            if certificate is None:
                record["result"] = "NO_QUOTIENT_OBSTRUCTION_FOUND"
                payload["iterations"].append(record)
                payload["result"] = "SURVIVING_QUOTIENT_RELAXATION_NOT_WEIGHTS"
                save()
                print(json.dumps(record), flush=True)
                break
            certificate_path = prefix.with_suffix(".certificate.json")
            certificate_path.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
            # Replay serialized data, independently of the discovery lattice.
            if not audit.verify_certificate(support, json.loads(certificate_path.read_text(encoding="utf-8"))):
                raise AssertionError("serialized certificate replay failed")
            cut = list(certificate["cut"])
            if cut in learned:
                raise AssertionError("a prior cut failed to exclude the candidate")
            solver.add_clause(cut)
            learned.append(cut)
            record.update(result=certificate["kind"], relations=len(certificate["relations"]),
                          cut_literals=len(cut), seconds=time.monotonic() - begin,
                          certificate_sha256=sha256(certificate_path))
            payload["iterations"].append(record)
            save()
            print(json.dumps(record), flush=True)
        else:
            payload["result"] = "ITERATION_LIMIT"
    payload["learned_cuts"] = len(learned)
    payload["seconds"] = time.monotonic() - started
    save()
    print(json.dumps({key: value for key, value in payload.items() if key != "iterations"}), flush=True)


def itertools_chain(*iterables):
    for iterable in iterables:
        yield from iterable


if __name__ == "__main__":
    main()
