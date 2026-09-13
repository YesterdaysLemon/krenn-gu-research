"""Run a bounded algebraic-refinement loop on one fixed physical support.

Proper-cofactor supports remain solver variables.  Each learned clause is
replayed from complete source fibres before it is admitted.  The scorecard is
therefore about one physical support, not the number of Boolean assignments
visited.  A final UNSAT status still needs a checked source-core or proof trace
before it is promoted as a physical-support exclusion.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys as _bootstrap_sys
import time
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from pysat.solvers import Cadical195  # noqa: E402

from krenn_gu.recursive_tensor_binomials import RecursiveTensorBinomials  # noqa: E402
from krenn_gu.recursive_tensor_quotient import RecursiveTensorQuotient  # noqa: E402
from krenn_gu.recursive_tensor_ratio_cuts import (  # noqa: E402
    add_tensor_ratio_consistency,
)
from krenn_gu.recursive_tensor_support import (  # noqa: E402
    build_recursive_tensor_support_cnf,
)
from krenn_gu.source_quotient_core import (  # noqa: E402
    replay_guarded_algebraic_clause,
)


def _clause_value(clause, positive):
    return any((literal > 0) == (abs(literal) in positive) for literal in clause)


def _load_support(path, n, entry_ids):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("n") != n:
        raise ValueError("support fixture has the wrong order")
    values = payload.get("nonzero_entry_ids")
    if (
        not isinstance(values, list)
        or any(type(value) is not int or value <= 0 for value in values)
        or len(values) != len(set(values))
    ):
        raise ValueError("support fixture needs distinct positive entry ids")
    positive = set(values)
    if not positive <= entry_ids:
        raise ValueError("support fixture contains a non-entry variable")
    return payload, positive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--support", type=_BootstrapPath, required=True)
    parser.add_argument("--output-dir", type=_BootstrapPath, required=True)
    parser.add_argument("--iterations", type=int, default=8)
    parser.add_argument(
        "--ratio-closure",
        action="store_true",
        help="add the independently tested ratio-component necessary clauses",
    )
    args = parser.parse_args()
    if not 0 < args.iterations <= 100:
        raise ValueError("iterations must be in [1, 100]")
    if args.output_dir.exists():
        raise ValueError("output directory must be new")
    args.output_dir.mkdir(parents=True)

    started = time.monotonic()
    instance = build_recursive_tensor_support_cnf(
        args.n,
        column_killers=False,
        fix_root_killers=False,
    )
    support_payload, positive_entries = _load_support(
        args.support,
        args.n,
        set(instance.entries.values()),
    )
    ratio_counts = None
    if args.ratio_closure:
        ratio_counts = add_tensor_ratio_consistency(instance, component_closure=True)
    entry_units = [
        variable if variable in positive_entries else -variable
        for variable in instance.entries.values()
    ]
    instance.cnf.extend((literal,) for literal in entry_units)
    recursive = RecursiveTensorBinomials(instance)
    quotient = RecursiveTensorQuotient(instance)
    learned = []
    records = []
    summary = {
        "schema": "recursive-physical-support-refinement-v1",
        "n": args.n,
        "scope": "one fixed physical support; proper-cofactor supports free; not weights",
        "support": support_payload,
        "distinct_physical_supports": 1,
        "ratio_closure": args.ratio_closure,
        "ratio_counts": ratio_counts,
        "base_variables": instance.cnf.nv,
        "base_clauses": len(instance.cnf.clauses),
        "iterations": records,
        "result": "RUNNING",
    }

    def save():
        summary["elapsed_seconds"] = round(time.monotonic() - started, 6)
        (args.output_dir / "summary.json").write_text(
            json.dumps(summary, indent=2) + "\n",
            encoding="utf-8",
        )

    save()
    with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
        for iteration in range(args.iterations):
            begin = time.monotonic()
            if not solver.solve():
                summary["result"] = "UNSAT_REPLAYED_CLAUSES_NEEDS_CHECKED_CORE_OR_TRACE"
                break
            model = solver.get_model()
            positive = {literal for literal in model if literal > 0}
            if not all(
                _clause_value(clause, positive)
                for clause in itertools.chain(instance.cnf.clauses, learned)
            ):
                raise AssertionError("solver assignment failed a recorded clause")

            certificate, recursive_diagnostic = recursive.find_obstruction(model)
            stage = "binomial_kernel"
            if certificate is not None:
                certificate = {"kind": "binomial_kernel", **certificate}
            else:
                certificate, quotient_diagnostic = quotient.find_obstruction(model)
                recursive_diagnostic["quotient"] = quotient_diagnostic
                stage = certificate["kind"] if certificate else "none"
            record = {
                "iteration": iteration,
                "stage": stage,
                "assignment_checked": True,
                "nonzero_entries": len(positive_entries),
                "recursive_diagnostic": recursive_diagnostic,
                "solver_stats": solver.accum_stats(),
                "seconds": round(time.monotonic() - begin, 6),
            }
            (args.output_dir / f"iteration-{iteration:03d}.model.json").write_text(
                json.dumps(model) + "\n",
                encoding="utf-8",
            )
            if certificate is None:
                record["result"] = "NO_IMPLEMENTED_ALGEBRAIC_CLAUSE_NOT_WEIGHTS"
                records.append(record)
                summary["result"] = record["result"]
                save()
                break

            replay = replay_guarded_algebraic_clause(instance, model, certificate)
            cut = list(replay["clause"])
            if _clause_value(cut, positive):
                raise AssertionError("checked clause does not reject its source template")
            if cut in learned:
                raise AssertionError("duplicate learned clause")
            (args.output_dir / f"iteration-{iteration:03d}.certificate.json").write_text(
                json.dumps(certificate, indent=2) + "\n",
                encoding="utf-8",
            )
            solver.add_clause(cut)
            instance.cnf.append(cut)
            learned.append(cut)
            record.update(
                result="REPLAYED_ALGEBRAIC_ASSIGNMENT_CLAUSE",
                algebra_replay=replay["status"],
                cut_literals=len(cut),
            )
            records.append(record)
            save()
        else:
            summary["result"] = "ITERATION_LIMIT"

    summary["assignment_clauses"] = len(learned)
    summary["physical_support_excluded"] = False
    summary["promotion_gate"] = (
        "replay a checked source-core or proof trace before setting this true"
    )
    save()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
