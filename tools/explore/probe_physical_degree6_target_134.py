"""Discover exact physical certificates in degree-six blocks touching pure rows.

Every cofactor is expanded. This probe uses the original equations only,
without a boundary relation or inversion of any physical variable.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
import itertools
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap

ROOT, _ = bootstrap(__file__)
from tools.explore.probe_physical_boundary_quotient_134 import (  # noqa: E402
    ENTRY_KEYS, VERTICES, hafnian,
)


def subtract(row, scale, other):
    for key, value in other.items():
        new = row.get(key, 0) - scale * value
        if new:
            row[key] = new
        else:
            row.pop(key, None)


def combine_provenance(target, scale, source):
    subtract(target, scale, source)


def echelon(rows):
    basis = {}
    for index, source in enumerate(rows):
        row = {m: Fraction(c) for m, c in source.items() if c}
        provenance = {index: Fraction(1)}
        while row:
            pivot = max(row, key=lambda m: (len(m), m))
            if pivot not in basis:
                value = row[pivot]
                row = {m: c / value for m, c in row.items()}
                provenance = {m: c / value for m, c in provenance.items()}
                basis[pivot] = (row, provenance)
                break
            other, other_prov = basis[pivot]
            value = row[pivot]
            subtract(row, value, other)
            combine_provenance(provenance, value, other_prov)
    # Back elimination identifies every coordinate vector in this row space.
    for pivot in sorted(basis, key=lambda m: (len(m), m)):
        row, provenance = basis[pivot]
        for previous in sorted(basis, key=lambda m: (len(m), m)):
            if (len(previous), previous) <= (len(pivot), pivot):
                continue
            other, other_prov = basis[previous]
            if pivot in other:
                value = other[pivot]
                subtract(other, value, row)
                combine_provenance(other_prov, value, provenance)
    singles = [(row, prov) for row, prov in basis.values() if len(row) == 1]
    return singles, len(basis)


def degree(monomial):
    values = [[] for _ in VERTICES]
    for entry in monomial:
        u, v, a, b = ENTRY_KEYS[entry - 1]
        values[u].append(a)
        values[v].append(b)
    return tuple(tuple(sorted(v)) for v in values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-blocks", type=int, default=0)
    parser.add_argument("--include-overlaps", action="store_true")
    parser.add_argument("--support", type=Path,
                        default=ROOT / "tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json")
    args = parser.parse_args()
    start = time.monotonic()
    fixture = args.support
    live = set(json.loads(fixture.read_text())["nonzero_entry_ids"])
    zeros = set(range(1, 253)) - live

    @lru_cache(maxsize=None)
    def full(word):
        poly = hafnian(VERTICES, word, zeros)
        if len(set(word)) == 1:
            poly[()] = -1
        return poly

    multiplier_by_physical = defaultdict(list)
    target_grades = set()
    for m in itertools.combinations_with_replacement(sorted(live), 2):
        dg = degree(m)
        physical = tuple(map(len, dg))
        if not args.include_overlaps and max(physical) != 1:
            continue
        multiplier_by_physical[physical].append((m, dg))
        for colour in range(3):
            target_grades.add(tuple(tuple(sorted((*v, colour))) for v in dg))
    print(f"pure-attached grades={len(target_grades)}", flush=True)
    counts = defaultdict(int)
    histogram = defaultdict(int)
    for grade in sorted(target_grades):
        if args.max_blocks and counts["blocks"] >= args.max_blocks:
            break
        physical = tuple(len(v) - 1 for v in grade)
        rows, sources = [], []
        for m, md in multiplier_by_physical[physical]:
            remainder = [list(v) for v in grade]
            valid = True
            for vertex, colours in enumerate(md):
                for colour in colours:
                    if colour not in remainder[vertex]:
                        valid = False
                        break
                    remainder[vertex].remove(colour)
                if not valid:
                    break
            if not valid:
                continue
            word = tuple(v[0] for v in remainder)
            poly = defaultdict(int)
            for term, coefficient in full(word).items():
                poly[tuple(sorted((*m, *term)))] += coefficient
            rows.append({term: c for term, c in poly.items() if c})
            sources.append({"word": "".join(map(str, word)), "multiplier": list(m)})
        singles, rank = echelon(rows)
        counts["blocks"] += 1
        counts["rows"] += len(rows)
        counts["ranks"] += rank
        histogram[len(rows)] += 1
        if singles:
            row, prov = singles[0]
            monomial, value = next(iter(row.items()))
            certificate = []
            for index, coefficient in sorted(prov.items()):
                source = dict(sources[index])
                source["coefficient"] = str(coefficient / value)
                certificate.append(source)
            result = {"status": "candidate_exact_polynomial_certificate",
                      "scope": "fixed_support_degree6_pure_attached_blocks",
                      "support_file": fixture.name, "uses_rho": False,
                      "grade": grade, "target_monomial": monomial,
                      "sources": certificate, "counts": dict(counts),
                      "elapsed_seconds": time.monotonic() - start}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result), flush=True)
            return 0
        if counts["blocks"] % 1000 == 0:
            print(f"blocks={counts['blocks']} rows={counts['rows']} elapsed={time.monotonic()-start:.1f}", flush=True)
    result = {"status": "no_singleton_in_tested_blocks",
              "scope": "individual_pure_attached_degree6_blocks_only",
              "cross_block_pure_target_coupling_checked": False,
              "include_overlaps": args.include_overlaps,
              "total_grades": len(target_grades), "counts": dict(counts),
              "row_count_histogram": dict(histogram),
              "elapsed_seconds": time.monotonic() - start}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
