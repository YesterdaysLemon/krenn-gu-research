"""Discover a bounded row-space candidate after exact Laurent transport.

This is discovery only.  The output deliberately omits original integer
transport witnesses; ``pack_recursive_row_space.py`` must attach them and the
small exact replayer must accept the resulting certificate before use.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
import json
from math import gcd
from pathlib import Path
import sys as _bootstrap_sys
import time

for _bootstrap_parent in Path(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.recursive_tensor_binomials import TensorLaplaceOrigin  # noqa: E402
from krenn_gu.recursive_tensor_quotient import (  # noqa: E402
    RecursiveTensorQuotient,
    UnitSignedQuotient,
    _origin_data,
)

parser = argparse.ArgumentParser()
parser.add_argument('--n', type=int, required=True)
parser.add_argument('--model', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
if args.output.exists():
    raise ValueError("output path must be new")
args.output.parent.mkdir(parents=True, exist_ok=True)
started = time.monotonic()
instance = build_recursive_tensor_support_cnf(args.n, column_killers=False, fix_root_killers=False)
algebra = RecursiveTensorQuotient(instance)
model = json.loads(args.model.read_text())
assigned, positive = algebra.binomials.support(model)
_expanded, raw, substitutions = algebra.binomials.extract(model)
origins = set(raw)
origins.update(origin for origin, dependencies in substitutions.values())
origins = sorted(origins, key=lambda o: (o.vertices, o.word, o.vertex, o.orientation))
rows = [algebra.binomials.raw_relation(origin, positive) for origin in origins]
quotient = UnitSignedQuotient(rows)
assert quotient.kernel is None, 'earlier binomial kernel already excludes this assignment'
print('quotient', len(rows), len(quotient.pivots), time.monotonic()-started, flush=True)
nodes, basis = [], {}
contradiction = None
insertions = 0

def record(kind, **fields):
    if len(nodes) >= 200000:
        raise RuntimeError('DAG_BOUND')
    nodes.append({'kind': kind, **fields})
    return len(nodes)-1

def order(monomial):
    return sum(p for v, p in monomial), monomial

def normalize(poly, node):
    if not poly:
        return poly, node
    support = set(v for monomial in poly for v, p in monomial)
    dictionaries = [dict(monomial) for monomial in poly]
    common = {v: min(term.get(v, 0) for term in dictionaries) for v in support}
    common = {v: p for v, p in common.items() if p}
    scalar = reduce(gcd, map(abs, poly.values()))
    if poly[max(poly, key=order)] < 0:
        scalar = -scalar
    if common or scalar != 1:
        updated = {}
        for monomial, coefficient in poly.items():
            term = dict(monomial)
            for v, p in common.items():
                term[v] = term.get(v, 0)-p
            updated[tuple(sorted((v, p) for v, p in term.items() if p))] = coefficient//scalar
        poly = updated
        node = record('divide', parent=node, monomial=sorted(common.items()), scalar=scalar)
    return poly, node

def insert(poly, node):
    global insertions, contradiction
    insertions += 1
    while poly:
        poly, node = normalize(poly, node)
        if len(poly) == 1:
            contradiction = node
            return
        pivot = max(poly, key=order)
        if pivot not in basis:
            basis[pivot] = poly, node
            return
        previous, parent = basis[pivot]
        a, b = poly[pivot], previous[pivot]
        factor = gcd(abs(a), abs(b))
        a //= factor
        b //= factor
        updated = {m: b*c for m, c in poly.items()}
        for m, c in previous.items():
            updated[m] = updated.get(m, 0)-a*c
        poly = {m: c for m, c in updated.items() if c}
        node = record('combine', left=node, right=parent, left_scalar=b, right_scalar=-a)
        if len(poly) > 2048 or max((abs(c).bit_length() for c in poly.values()), default=0) > 1024:
            raise RuntimeError('ROW_SIZE_BOUND')

status = 'RUNNING'
try:
    for state in instance.coefficients:
        for vertex in state[0]:
            origin = TensorLaplaceOrigin(*state, vertex)
            polynomial = Counter()
            for term, coefficient in algebra.terms(origin, positive):
                monomial, sign = quotient.signature(term)
                polynomial[monomial] += coefficient*sign
            polynomial = {m: c for m, c in polynomial.items() if c}
            if not polynomial:
                continue
            node = record('source', origin=_origin_data(origin))
            insert(polynomial, node)
            if contradiction is not None:
                break
        if contradiction is not None:
            break
        if insertions and insertions % 1000 == 0:
            print('rows', insertions, 'basis', len(basis), 'nodes', len(nodes), time.monotonic()-started, flush=True)
    status = 'MONOMIAL_CONTRADICTION_CANDIDATE' if contradiction is not None else 'NO_ROW_SPACE_OBSTRUCTION_NOT_WEIGHTS'
except RuntimeError as error:
    status = str(error)
report = {'n': args.n, 'model': str(args.model), 'status': status, 'unit_rows': len(rows),
          'unit_rank': len(quotient.pivots), 'nonunit_residual': len(quotient.residual),
          'insertions': insertions, 'basis': len(basis), 'nodes': len(nodes), 'seconds': time.monotonic()-started}
if contradiction is not None:
    used = set()
    def visit(index):
        if index in used:
            return
        used.add(index)
        node = nodes[index]
        if node['kind'] == 'divide':
            visit(node['parent'])
        elif node['kind'] == 'combine':
            visit(node['left'])
            visit(node['right'])
    visit(contradiction)
    report['dag'] = [{'id': index, **nodes[index]} for index in sorted(used)]
    report['contradiction_node'] = contradiction
    report['dag_status'] = 'unreplayed_discovery; source signatures require exact transport replay'
args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({**report, 'dag': len(report.get('dag', []))}), flush=True)
