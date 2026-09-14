"""Bounded P8 occurrence test for the complete two-edge shore pattern family.

SAT is a checked Boolean countermodel to occurrence, never a weighted witness.
UNSAT without a separately checked proof is reported only as solver status.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
from pysat.solvers import Cadical195  # noqa: E402
from krenn_gu.eight_vertex_physical_hafnian_identity import (  # noqa: E402
    replay_eight_vertex_physical_hafnian_identity,
)
from krenn_gu.recursive_tensor_ratio_cuts import add_tensor_ratio_consistency  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.source_quotient_core import replay_source_quotient_core  # noqa: E402
from krenn_gu.two_edge_surplus_shore import four_patterns, replay  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replay-assignment", type=Path,
                        help="regenerate clauses and check a frozen bitset, without solving")
    parser.add_argument("--include-two-slice", action="store_true")
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    fixtures = ROOT / "tests/fixtures"
    raw = build_recursive_tensor_support_cnf(8, column_killers=False, fix_root_killers=False)
    checked = []
    for name in ("recursive_source_quotient_n8_core.json",
                 "recursive_source_quotient_n8_second_core.json",
                 "recursive_source_quotient_n8_third_core.json"):
        checked.append(replay_source_quotient_core(raw, json.loads((fixtures / name).read_text())))
    del raw
    checked.append(replay_eight_vertex_physical_hafnian_identity(json.loads(
        (fixtures / "eight_vertex_physical_hafnian_identity_25_literal.json").read_text())))
    checked.extend(replay(pattern) for pattern in four_patterns())
    if args.include_two_slice:
        from krenn_gu.two_slice_transfer import four_patterns as transfer_patterns
        checked.extend(replay(pattern) for pattern in transfer_patterns())
    instance = build_recursive_tensor_support_cnf(8)
    ratio = add_tensor_ratio_consistency(instance, component_closure=True)
    key_by_id = {v: key for key, v in instance.entries.items()}
    orbit_counts = []
    for result in checked:
        source = [(key_by_id[abs(lit)], 1 if lit > 0 else -1) for lit in result["physical_cut"]]
        orbit = set()
        for vm in itertools.permutations(range(8)):
            for cm in itertools.permutations(range(3)):
                cut = tuple(sorted((sign * instance.entry(vm[u], vm[v], cm[a], cm[b])
                                    for (u, v, a, b), sign in source), key=abs))
                orbit.add(cut)
        instance.cnf.extend(sorted(orbit))
        orbit_counts.append(len(orbit))
        print(f"orbit={len(orbit_counts)} unique={len(orbit)} seconds={time.monotonic()-start:.1f}", flush=True)
    header = f"p cnf {instance.cnf.nv} {len(instance.cnf.clauses)}\n".encode()
    digest = hashlib.sha256(header)
    for clause in instance.cnf.clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    summary = {"n": 8, "status": "RUNNING", "variables": instance.cnf.nv,
               "clauses": len(instance.cnf.clauses), "unique_orbit_counts": orbit_counts,
               "canonical_dimacs_sha256": digest.hexdigest(), "ratio_counts": ratio,
               "scope": "Boolean necessary model, not weights",
               "old_pattern_count": 4, "new_pattern_count": len(checked) - 4,
               "includes_two_slice_transfer": args.include_two_slice}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"solve clauses={summary['clauses']} elapsed={time.monotonic()-start:.1f}", flush=True)
    if args.replay_assignment:
        packet = json.loads(args.replay_assignment.read_text())
        if packet["canonical_dimacs_sha256"] != digest.hexdigest():
            raise ValueError("regenerated CNF hash differs from packet")
        bits = gzip.decompress(base64.b64decode(packet["assignment_bitset_gzip_base64"], validate=True))
        if len(bits) != (instance.cnf.nv + 7) // 8 or hashlib.sha256(bits).hexdigest() != packet["assignment_bitset_sha256"]:
            raise ValueError("assignment bitset identity differs")
        def truth(lit):
            pos = abs(lit) - 1
            return bool(bits[pos // 8] & (1 << (pos % 8))) == (lit > 0)
        if not all(any(truth(lit) for lit in clause) for clause in instance.cnf.clauses):
            raise ValueError("assignment does not satisfy regenerated clauses")
        actual_live = [v for v in instance.entries.values() if truth(v)]
        if actual_live != packet["nonzero_entry_ids"]:
            raise ValueError("physical projection differs")
        summary.update(status="PASS_FROZEN_BOOLEAN_ASSIGNMENT", assignment_checked=True,
                       elapsed_seconds=time.monotonic() - start)
        (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary), flush=True)
        return
    with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
        if solver.solve():
            model = solver.get_model()
            positive = {v for v in model if v > 0}
            if not all(any((v > 0) == (abs(v) in positive) for v in clause) for clause in instance.cnf.clauses):
                raise AssertionError("solver assignment failed clause replay")
            payload = json.dumps(model, separators=(",", ":")).encode()
            packed = gzip.compress(payload, mtime=0)
            (out / "model.json.gz").write_bytes(packed)
            summary.update(status="SAT_ABSTRACTION_NOT_WEIGHTS", assignment_checked=True,
                           assignment_gzip_sha256=hashlib.sha256(packed).hexdigest(),
                           assignment_json_sha256=hashlib.sha256(payload).hexdigest(),
                           nonzero_entry_ids=[v for v in instance.entries.values() if v in positive])
        else:
            summary["status"] = "UNSAT_SOLVER_STATUS_NO_CHECKED_PROOF"
        summary["solver_stats"] = solver.accum_stats()
    summary["elapsed_seconds"] = time.monotonic() - start
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
