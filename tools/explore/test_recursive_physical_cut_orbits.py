"""Test a bounded n=8 parent with full orbits of checked physical cuts.

Every packet is independently replayed before its physical cut is admitted.
Only vertex permutations and one common global colour permutation are used;
independent local colour permutations are not target symmetries.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys as _bootstrap_sys
import time
from pathlib import Path

for _bootstrap_parent in Path(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from pysat.solvers import Cadical195  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.recursive_tensor_ratio_cuts import add_tensor_ratio_consistency  # noqa: E402
from krenn_gu.source_quotient_core import replay_source_quotient_core  # noqa: E402

started = time.monotonic()
parser = argparse.ArgumentParser()
parser.add_argument('--packet', action='append', type=Path, required=True)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
output = args.output_dir
if output.exists():
    raise ValueError("output directory must be new")
output.mkdir(exist_ok=False)
packets = args.packet
unaugmented = build_recursive_tensor_support_cnf(8, column_killers=False, fix_root_killers=False)
checked = [
    replay_source_quotient_core(
        unaugmented,
        json.loads(path.read_text(encoding="utf-8")),
    )
    for path in packets
]
del unaugmented
instance = build_recursive_tensor_support_cnf(8)
ratio = add_tensor_ratio_consistency(instance, component_closure=True)
keys = {value: key for key,value in instance.entries.items()}
orbit_counts = []
for result in checked:
    source = [
        (keys[abs(literal)], 1 if literal > 0 else -1)
        for literal in result['physical_cut']
    ]
    count = 0
    for vertex_map in itertools.permutations(range(8)):
        for colour_map in itertools.permutations(range(3)):
            cut = [
                sign
                * instance.entry(
                    vertex_map[u],
                    vertex_map[v],
                    colour_map[a],
                    colour_map[b],
                )
                for (u, v, a, b), sign in source
            ]
            instance.cnf.append(cut)
            count += 1
    assert count == 241920
    orbit_counts.append(count)
    print('orbit', len(orbit_counts), 'cuts', count, 'source_literals', len(source),
          'seconds', time.monotonic()-started, flush=True)
summary = {'n': 8, 'scope': 'full-source necessary model; no weight realization inference',
           'verified_source_cuts': [len(result['physical_cut']) for result in checked],
           'orbit_counts_including_possible_duplicates': orbit_counts,
           'symmetries': 'all physical vertex permutations and one common colour permutation',
           'ratio_counts': ratio, 'variables': instance.cnf.nv,
           'clauses': len(instance.cnf.clauses), 'result': 'RUNNING'}
(output / 'summary.json').write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
instance.cnf.to_file(str(output / 'instance.cnf'))
print('built', summary['clauses'], 'seconds', time.monotonic()-started, flush=True)
with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
    if solver.solve():
        model = solver.get_model()
        positive = {v for v in model if v > 0}
        assert all(any((v > 0) == (abs(v) in positive) for v in clause) for clause in instance.cnf.clauses)
        (output / 'model.json').write_text(json.dumps(model) + "\n", encoding="utf-8")
        summary.update(result='SAT_ABSTRACTION_NOT_WEIGHTS', assignment_checked=True,
                       nonzero_entry_ids=[v for v in instance.entries.values() if v in positive])
    else:
        summary['result'] = 'UNSAT_STATUS_NO_NATIVE_PROOF_YET'
    summary['solver_stats'] = solver.accum_stats()
summary['seconds'] = time.monotonic()-started
(output / 'summary.json').write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary), flush=True)
