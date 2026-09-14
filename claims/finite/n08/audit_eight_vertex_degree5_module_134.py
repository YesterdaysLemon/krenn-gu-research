"""Independent exact column-matroid audit of the complete degree-five module.

No primary probe is imported. Bitmask matching expansion supplies columns;
incidence multiplicities and exact column ranks test for coloops. A coordinate
unit belongs to a matrix row space iff deleting its column decreases rank.
Repeated equal columns cannot be coloops. Pure-minus-one tails are retained.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import itertools
import json
from math import gcd
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)


@lru_cache(maxsize=None)
def matchings(mask):
    if not mask:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    result = []
    candidates = rest
    while candidates:
        other_bit = candidates & -candidates
        other = other_bit.bit_length() - 1
        result.extend((((first, other),) + tail)
                      for tail in matchings(rest ^ other_bit))
        candidates ^= other_bit
    return tuple(result)


def rank(columns, size):
    """Exact Q rank by integer elimination, avoiding rational denominators."""
    basis = {}
    for column in columns:
        row = [int(bool(column & (1 << i))) for i in range(size)]
        for pivot, old in basis.items():
            if row[pivot]:
                left, right = old[pivot], row[pivot]
                row = [left * x - right * y for x, y in zip(row, old)]
                divisor = 0
                for value in row:
                    divisor = gcd(divisor, value)
                if divisor > 1:
                    row = [x // divisor for x in row]
        pivot = next((i for i, value in enumerate(row) if value), None)
        if pivot is not None:
            basis[pivot] = row
            basis = dict(sorted(basis.items()))
    return len(basis)


def analyze_patterns(patterns, size):
    """Return rank and singleton-column coloops, using column multiplicities."""
    columns = list(patterns)
    whole_rank = rank(columns, size)
    coloops = [column for column, count in patterns.items()
               if count == 1 and rank([c for c in columns if c != column], size)
               < whole_rank]
    return whole_rank, coloops


def audit(fixture):
    start = time.monotonic()
    raw = fixture.read_bytes()
    live = set(json.loads(raw)["nonzero_entry_ids"])
    keys = list(itertools.product(range(3), repeat=2))
    edges = list(itertools.combinations(range(8), 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}

    def variable(u, v, a, b):
        return 1 + 9 * edge_index[u, v] + 3 * a + b

    assert len(live) == 134 and {82, 88, 91, 97} <= live
    words = list(itertools.product(range(3), repeat=8))
    pure = [index for index, word in enumerate(words) if len(set(word)) == 1]
    full = []
    for word in words:
        terms = []
        for matching in matchings(255):
            term = tuple(sorted(variable(u, v, word[u], word[v])
                                for u, v in matching))
            if all(v in live for v in term):
                terms.append(term)
        assert len(terms) == len(set(terms)) and len(terms) >= 3
        # rho's two factors share physical vertex 1, absent in a matching.
        assert all(not (82 in term and 97 in term) for term in terms)
        full.append(terms)

    # Every quartic matching monomial determines its complete color word.
    # Consequently each constant-multiplier row has >=3 private quartic
    # columns; pure constant tails cannot create a unit or a kernel.
    seen = set()
    for terms in full:
        for term in terms:
            assert term not in seen
            seen.add(term)
    del seen

    # Control the coloop test itself, including a kernel and an odd cycle.
    assert analyze_patterns(Counter({1: 2}), 1) == (1, [])
    assert analyze_patterns(Counter({1: 1}), 1) == (1, [1])
    assert analyze_patterns(Counter({3: 2}), 2) == (1, [])
    assert analyze_patterns(Counter({3: 1, 5: 1, 6: 1}), 3)[0] == 3
    assert len(analyze_patterns(Counter({3: 1, 5: 1, 6: 1}), 3)[1]) == 3

    total_rank = 0
    total_rows = 0
    rho_changes = 0
    pure_tails = 0
    component_histogram = Counter()
    source_incidence_histogram = Counter()
    candidate_columns = 0
    blocks = []
    for edge_number, edge in enumerate(edges):
        multipliers = [1 + 9 * edge_number + 3 * a + b for a, b in keys
                       if 1 + 9 * edge_number + 3 * a + b in live]
        row_count = len(multipliers) * len(words)
        parent = list(range(row_count))

        def find(row):
            while parent[row] != row:
                parent[row] = parent[parent[row]]
                row = parent[row]
            return row

        def join(left, right):
            left, right = find(left), find(right)
            if left != right:
                parent[right] = left

        columns = {}
        for index, multiplier in enumerate(multipliers):
            for word_index, terms in enumerate(full):
                row = index * len(words) + word_index
                for term in terms:
                    factors = (*term, multiplier)
                    # Reverse of the primary orientation: AD -> BC.
                    if 82 in factors and 97 in factors:
                        factors = list(factors)
                        factors.remove(82)
                        factors.remove(97)
                        factors.extend((88, 91))
                        rho_changes += 1
                    monomial = tuple(sorted(factors))
                    if monomial in columns:
                        old = columns[monomial]
                        assert isinstance(old, int) and old != row
                        columns[monomial] = (old, row)
                        join(old, row)
                    else:
                        columns[monomial] = row

        incidence = Counter()
        for rows in columns.values():
            rows = (rows,) if isinstance(rows, int) else tuple(sorted(rows))
            source_incidence_histogram[len(rows)] += 1
            incidence[rows] += 1
        del columns
        for index in range(len(multipliers)):
            rows = tuple(index * len(words) + word for word in pure)
            # All three coefficients of this lower linear column are -1;
            # scaling the column by -1 preserves rank and coloop status.
            incidence[rows] += 1
            pure_tails += len(rows)
            for row in rows[1:]:
                join(rows[0], row)

        members = defaultdict(list)
        for row in range(row_count):
            members[find(row)].append(row)
        positions = {row: index for group in members.values()
                     for index, row in enumerate(group)}
        component_patterns = defaultdict(Counter)
        for rows, count in incidence.items():
            roots = {find(row) for row in rows}
            assert len(roots) == 1
            mask = sum(1 << positions[row] for row in rows)
            component_patterns[next(iter(roots))][mask] += count
        block_rank = 0
        for root, group in members.items():
            patterns = component_patterns[root]
            component_histogram[len(group)] += 1
            candidate_columns += sum(count == 1 for count in patterns.values())
            component_rank, coloops = analyze_patterns(patterns, len(group))
            assert not coloops, (edge, group, patterns, coloops)
            block_rank += component_rank
        blocks.append({"physical_edge": edge, "rows": row_count,
                       "rank": block_rank, "components": len(members)})
        total_rank += block_rank
        total_rows += row_count
        print(f"edge={edge} rows={row_count} rank={block_rank}", flush=True)

    assert total_rows == 134 * 6561 and pure_tails == 134 * 3
    return {
        "status": "PASS",
        "outcome": "EXACT_NO_MONOMIAL_IN_COMPLETE_DEGREE_FIVE_MODULE_MOD_RHO",
        "method": "independent bitmask expansion; reverse rho; column-matroid coloop test over Q",
        "fixture_sha256": sha256(raw).hexdigest(),
        "constant_multiplier_rows": 6561,
        "constant_multiplier_rank": 6561,
        "linear_multiplier_rows": total_rows,
        "linear_multiplier_rank": total_rank,
        "pure_lower_tail_incidences": pure_tails,
        "rho_reductions": rho_changes,
        "source_column_incidence_histogram": dict(source_incidence_histogram),
        "component_size_histogram": dict(sorted(component_histogram.items())),
        "single_columns_tested_for_coloops": candidate_columns,
        "coloop_count": 0,
        "blocks": blocks,
        "scope": "Q row span of all P_a and all live g_s P_a plus all rho multiples through degree 5; no localization",
        "elapsed_seconds": time.monotonic() - start,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=ROOT / "tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.fixture)
    serialized = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
