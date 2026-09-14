"""Independent exact audit of the frozen pure-attached degree-six family.

Scientific code from the primary probe is not imported. Compatible words are
enumerated inside each grade, then quadratic factors are looked up by base-four
endpoint-color signatures. Bitmask matchings supply full physical polynomials.
Exact column dependencies certify high rank and absence of augmented coloops.

Scope: only quadratic q*P_a rows whose high grade meets some quadratic times a
pure target. No rho, localization, mixed-only grades, or full-ideal assertion.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
FROZEN_LF_SHA256 = "d89d7a498c1a65a177f943aae774543985eef106c5067405648336b97c73b9d6"


@lru_cache(maxsize=None)
def matchings(mask):
    if not mask:
        return ((),)
    bit = mask & -mask
    first = bit.bit_length() - 1
    rest = mask ^ bit
    choices = rest
    result = []
    while choices:
        other_bit = choices & -choices
        other = other_bit.bit_length() - 1
        result.extend((((first, other),) + tail)
                      for tail in matchings(rest ^ other_bit))
        choices ^= other_bit
    return tuple(result)


def add_scaled(target, source, coefficient):
    for index, value in source.items():
        updated = target.get(index, 0) + coefficient * value
        if updated:
            target[index] = updated
        else:
            target.pop(index, None)


class ColumnDependencies:
    """Track an exact column basis and which basis elements are not coloops.

Every dependent input column is expressed in the selected original columns.
Its nonzero basis coordinates each certify a dependence containing that basis
column. A duplicated column is immediately protected. Nonbasis columns cannot
be coloops. Thus any unprotected selected column is exactly a coloop.
"""

    def __init__(self):
        self.basis = {}
        self.protected = []
        self.dependencies = 0

    def add(self, mask, multiplicity=1):
        values = {}
        cursor = mask
        while cursor:
            bit = cursor & -cursor
            values[bit.bit_length() - 1] = Fraction(1)
            cursor ^= bit
        combination = {}
        while values:
            pivot = min(values)
            coefficient = values[pivot]
            if pivot not in self.basis:
                selected = len(self.protected)
                normalized = {i: x / coefficient for i, x in values.items()}
                representation = {selected: Fraction(1, 1) / coefficient}
                add_scaled(representation, combination, -1 / coefficient)
                self.basis[pivot] = normalized, representation
                self.protected.append(multiplicity > 1)
                return
            old, representation = self.basis[pivot]
            add_scaled(values, old, -coefficient)
            add_scaled(combination, representation, coefficient)
        for selected, coefficient in combination.items():
            if coefficient:
                self.protected[selected] = True
        self.dependencies += 1


def controls():
    one = ColumnDependencies()
    one.add(1)
    assert one.protected == [False]
    repeated = ColumnDependencies()
    repeated.add(1, 2)
    assert repeated.protected == [True]
    triangle = ColumnDependencies()
    for mask in (1, 2, 3):
        triangle.add(mask)
    assert len(triangle.basis) == 2 and all(triangle.protected)
    # Exact Q rank differs from characteristic two here.
    odd = ColumnDependencies()
    for mask in (3, 5, 6):
        odd.add(mask)
    assert len(odd.basis) == 3 and not any(odd.protected)
    odd.add(7)
    assert all(odd.protected)


def audit(fixture):
    started = time.monotonic()
    raw = fixture.read_bytes()
    # Pin committed LF bytes while allowing Git's Windows CRLF checkout.
    assert sha256(raw.replace(b"\r\n", b"\n")).hexdigest() == FROZEN_LF_SHA256, "frozen support identity changed"
    support = json.loads(raw)
    live = sorted(support["nonzero_entry_ids"])
    assert len(live) == len(set(live)) == 129
    live_set = set(live)
    controls()
    pairs = list(itertools.combinations(range(8), 2))
    pair_number = {pair: index for index, pair in enumerate(pairs)}

    def entry(u, v, a, b):
        return 9 * pair_number[u, v] + 3 * a + b + 1

    # Base four has enough room: q contributes <=2 and a target contributes1
    # to any endpoint-color digit. Addition therefore causes no carry.
    units = [[1 << (2 * (3 * vertex + color)) for color in range(3)]
             for vertex in range(8)]
    entry_signature = {}
    for (u, v), index in pair_number.items():
        for a, b in itertools.product(range(3), repeat=2):
            entry_signature[9 * index + 3 * a + b + 1] = units[u][a] + units[v][b]
    pure_signatures = [sum(units[v][c] for v in range(8)) for c in range(3)]
    quadratic_by_signature = defaultdict(list)
    all_quadratics = list(itertools.combinations_with_replacement(live, 2))
    assert len(all_quadratics) == 8385
    grades = set()
    for q in all_quadratics:
        signature = sum(entry_signature[v] for v in q)
        quadratic_by_signature[signature].append(q)
        grades.update(signature + pure for pure in pure_signatures)

    @lru_cache(maxsize=None)
    def expanded(word):
        output = []
        for matching in matchings(255):
            monomial = tuple(sorted(entry(u, v, word[u], word[v])
                                    for u, v in matching))
            if all(variable in live_set for variable in monomial):
                output.append(monomial)
        assert len(output) == len(set(output))
        return tuple(output)

    rank_sum = 0
    row_total = 0
    row_histogram = Counter()
    column_incidence_histogram = Counter()
    pure_tails = Counter()
    labels_seen = set()
    label_digest = sha256()
    selected_columns = 0
    dependency_certificates = 0
    high_columns = 0
    for grade_number, grade in enumerate(sorted(grades), 1):
        allowed = [tuple(c for c in range(3)
                         if (grade >> (2 * (3 * v + c))) & 3)
                   for v in range(8)]
        rows = []
        for word in itertools.product(*allowed):
            word_signature = sum(units[v][word[v]] for v in range(8))
            for q in quadratic_by_signature.get(grade - word_signature, ()):
                label = word, q
                assert label not in labels_seen, "duplicate source row"
                labels_seen.add(label)
                label_digest.update(bytes((*word, *q)))
                rows.append(label)
        assert rows, "a grade generated by a pure row must be nonempty"
        columns = {}
        low_columns = Counter()
        for row_number, (word, q) in enumerate(rows):
            row_bit = 1 << row_number
            for term in expanded(word):
                monomial = tuple(sorted((*term, *q)))
                assert sum(entry_signature[v] for v in monomial) == grade
                old = columns.get(monomial, 0)
                assert not old & row_bit, "unexpected coefficient multiplicity"
                columns[monomial] = old | row_bit
            if len(set(word)) == 1:
                low_columns[row_bit] += 1
                pure_tails[q] += 1

        patterns = Counter(columns.values())
        high_columns += len(columns)
        for mask in columns.values():
            column_incidence_histogram[mask.bit_count()] += 1
        del columns
        linear = ColumnDependencies()
        # Sparse columns first gives transparent short dependency certificates.
        for mask, multiplicity in sorted(patterns.items(), key=lambda x: (x[0].bit_count(), x[0])):
            linear.add(mask, multiplicity)
        assert len(linear.basis) == len(rows), ("high kernel", grade, rows)
        high_rank = len(linear.basis)
        for mask, multiplicity in low_columns.items():
            # Each lower coefficient is -1. Scaling an entire column by -1
            # leaves rank, dependencies, and coloop status unchanged.
            linear.add(mask, multiplicity)
        assert len(linear.basis) == high_rank
        assert all(linear.protected), ("augmented coloop", grade, rows)
        selected_columns += len(linear.protected)
        dependency_certificates += linear.dependencies
        rank_sum += high_rank
        row_total += len(rows)
        row_histogram[len(rows)] += 1
        if grade_number % 2000 == 0:
            print(f"grades={grade_number}/{len(grades)} rows={row_total} exact_high_rank={rank_sum}", flush=True)

    assert len(grades) == 20280 and row_total == 142328
    assert set(pure_tails) == set(all_quadratics)
    assert set(pure_tails.values()) == {3}
    assert len(labels_seen) == row_total == rank_sum
    return {
        "status": "PASS",
        "outcome": "EXACT_NO_MONOMIAL_IN_COMPLETE_PURE_ATTACHED_DEGREE_SIX_ROW_SPACE",
        "fixture_raw_sha256": sha256(raw).hexdigest(),
        "fixture_lf_sha256": FROZEN_LF_SHA256,
        "method": "independent word-first grade completion, bitmask hafnians, exact Q column dependencies",
        "quadratic_multipliers": len(all_quadratics),
        "pure_attached_grades": len(grades),
        "source_rows": row_total,
        "unique_source_labels": len(labels_seen),
        "source_label_order_sha256": label_digest.hexdigest(),
        "high_rank": rank_sum,
        "high_kernel_dimension": 0,
        "pure_quadratic_tail_incidences": sum(pure_tails.values()),
        "shared_tail_multiplicity": 3,
        "augmented_coloops": 0,
        "high_monomial_columns": high_columns,
        "selected_basis_columns_protected": selected_columns,
        "dependent_column_certificates": dependency_certificates,
        "row_count_histogram": dict(sorted(row_histogram.items())),
        "high_column_incidence_histogram": dict(sorted(column_incidence_histogram.items())),
        "global_tail_argument": "Disjoint high grades and full high row rank force every other block coefficient to zero; shared quadratic tails cannot create additional cancellation.",
        "scope": "Q span of all q*P_word in grades met by some live quadratic times a pure word; no rho, no localization, no unattached grades",
        "elapsed_seconds": time.monotonic() - started,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=ROOT / "tests/fixtures/eight_vertex_two_slice_parent_survivor.json")
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
