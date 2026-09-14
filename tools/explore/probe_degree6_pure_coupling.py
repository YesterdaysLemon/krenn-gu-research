#!/usr/bin/env python3
"""Exact cross-grade coupling probe for pure-attached degree-six rows.

For every live quadratic monomial q and every target word whose endpoint-
colour grade coincides with q times at least one pure word, this probe includes
the actual expanded row q*(T_word-delta_word).  The degree-six terms split by
endpoint-colour grade, while pure rows have shared degree-two tails -q.

Within each high-grade block we eliminate degree-six columns first.  Every
high-kernel residual is therefore an exact quadratic relation.  We reduce all
such relations globally, quotient every surviving high basis tail by that
global low space, and then test the resulting exact row spaces for a singleton
coordinate.  No boundary relation, localization, cofactor abstraction, or
division by a physical entry is used.

The scope is the complete pure-attached degree-six family just described.  It
does not include mixed-only high grades that meet no pure target grade.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
from tools.explore.probe_physical_boundary_quotient_134 import (  # noqa: E402
    ENTRY_KEYS,
    VERTICES,
    hafnian,
)


Monomial = tuple[int, ...]
Word = tuple[int, ...]
SourceLabel = tuple[Word, Monomial]
Row = dict[Monomial, Fraction]
Provenance = dict[SourceLabel, Fraction]


def subtract(target: dict, coefficient: Fraction, source: dict) -> None:
    for key, value in source.items():
        updated = target.get(key, Fraction(0)) - coefficient * value
        if updated:
            target[key] = updated
        else:
            target.pop(key, None)


def add_scaled(target: dict, coefficient: Fraction, source: dict) -> None:
    for key, value in source.items():
        updated = target.get(key, Fraction(0)) + coefficient * value
        if updated:
            target[key] = updated
        else:
            target.pop(key, None)


def normalize(row: Row, provenance: dict, pivot: Monomial) -> tuple[Row, dict]:
    coefficient = row[pivot]
    return (
        {key: value / coefficient for key, value in row.items()},
        {key: value / coefficient for key, value in provenance.items()},
    )


def monomial_order(monomial: Monomial) -> tuple[int, Monomial]:
    return len(monomial), monomial


def exact_rref(rows: list[Row]) -> list[tuple[Monomial, Row, dict[int, Fraction]]]:
    """Return canonical sparse RREF with input-row provenance."""

    basis: list[tuple[Monomial, Row, dict[int, Fraction]]] = []
    for index, source in enumerate(rows):
        row = dict(source)
        provenance = {index: Fraction(1)}
        for pivot, pivot_row, pivot_provenance in basis:
            coefficient = row.get(pivot)
            if coefficient is None:
                continue
            subtract(row, coefficient, pivot_row)
            subtract(provenance, coefficient, pivot_provenance)
        if not row:
            continue
        pivot = max(row, key=monomial_order)
        row, provenance = normalize(row, provenance, pivot)
        updated_basis = []
        for old_pivot, old_row, old_provenance in basis:
            coefficient = old_row.get(pivot)
            if coefficient is not None:
                subtract(old_row, coefficient, row)
                subtract(old_provenance, coefficient, provenance)
            updated_basis.append((old_pivot, old_row, old_provenance))
        updated_basis.append((pivot, row, provenance))
        basis = sorted(updated_basis, key=lambda item: monomial_order(item[0]), reverse=True)
    return basis


def degree(monomial: Monomial) -> tuple[tuple[int, ...], ...]:
    values = [[] for _ in VERTICES]
    for identifier in monomial:
        u, v, a, b = ENTRY_KEYS[identifier - 1]
        values[u].append(a)
        values[v].append(b)
    return tuple(tuple(sorted(value)) for value in values)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def high_echelon(
    labelled_rows: list[tuple[SourceLabel, Row]],
) -> tuple[
    list[tuple[Monomial, Row, Row, Provenance]],
    list[tuple[Row, Provenance]],
    int,
]:
    """Eliminate high columns, retaining exact low tails and provenance."""

    basis: dict[Monomial, tuple[Row, Row, Provenance]] = {}
    low_relations: list[tuple[Row, Provenance]] = []
    zero_relations = 0
    for label, full_row in labelled_rows:
        high = {key: value for key, value in full_row.items() if len(key) == 6}
        low = {key: value for key, value in full_row.items() if len(key) == 2}
        if len(high) + len(low) != len(full_row):
            raise AssertionError("a source row has a degree other than two or six")
        provenance: Provenance = {label: Fraction(1)}
        while high:
            pivot = max(high, key=monomial_order)
            if pivot not in basis:
                coefficient = high[pivot]
                high = {key: value / coefficient for key, value in high.items()}
                low = {key: value / coefficient for key, value in low.items()}
                provenance = {
                    key: value / coefficient for key, value in provenance.items()
                }
                basis[pivot] = (high, low, provenance)
                break
            pivot_high, pivot_low, pivot_provenance = basis[pivot]
            coefficient = high[pivot]
            subtract(high, coefficient, pivot_high)
            subtract(low, coefficient, pivot_low)
            subtract(provenance, coefficient, pivot_provenance)
        else:
            if low:
                low_relations.append((low, provenance))
            elif provenance:
                zero_relations += 1
    return [
        (pivot, high, low, provenance)
        for pivot, (high, low, provenance) in sorted(
            basis.items(), key=lambda item: monomial_order(item[0]), reverse=True
        )
    ], low_relations, zero_relations


def build_problem(live: set[int]):
    zeros = set(range(1, len(ENTRY_KEYS) + 1)) - live

    @lru_cache(maxsize=None)
    def full(word: Word) -> dict[Monomial, int]:
        polynomial = hafnian(VERTICES, word, zeros)
        if len(set(word)) == 1:
            polynomial[()] = polynomial.get((), 0) - 1
        return polynomial

    multiplier_by_physical: dict[
        tuple[int, ...], list[tuple[Monomial, tuple[tuple[int, ...], ...]]]
    ] = defaultdict(list)
    target_grades = set()
    for multiplier in itertools.combinations_with_replacement(sorted(live), 2):
        multiplier_degree = degree(multiplier)
        physical = tuple(map(len, multiplier_degree))
        multiplier_by_physical[physical].append((multiplier, multiplier_degree))
        for colour in range(3):
            target_grades.add(
                tuple(tuple(sorted((*value, colour))) for value in multiplier_degree)
            )

    def rows_for_grade(grade):
        physical = tuple(len(value) - 1 for value in grade)
        rows = []
        for multiplier, multiplier_degree in multiplier_by_physical[physical]:
            remainder = [list(value) for value in grade]
            valid = True
            for vertex, colours in enumerate(multiplier_degree):
                for colour in colours:
                    if colour not in remainder[vertex]:
                        valid = False
                        break
                    remainder[vertex].remove(colour)
                if not valid:
                    break
            if not valid:
                continue
            if any(len(value) != 1 for value in remainder):
                raise AssertionError("grade subtraction did not leave one target colour")
            word = tuple(value[0] for value in remainder)
            polynomial: dict[Monomial, int] = defaultdict(int)
            for term, coefficient in full(word).items():
                polynomial[tuple(sorted((*multiplier, *term)))] += coefficient
            row = {
                term: Fraction(coefficient)
                for term, coefficient in polynomial.items()
                if coefficient
            }
            rows.append(((word, multiplier), row))
        return rows

    return sorted(target_grades), rows_for_grade


def reduce_low(
    low: Row,
    low_basis: list[tuple[Monomial, Row, dict[int, Fraction]]],
) -> tuple[Row, dict[int, Fraction]]:
    remainder = dict(low)
    used: dict[int, Fraction] = {}
    for basis_index, (pivot, row, _) in enumerate(low_basis):
        coefficient = remainder.get(pivot)
        if coefficient is None:
            continue
        subtract(remainder, coefficient, row)
        used[basis_index] = coefficient
    return remainder, used


def expand_low_provenance(
    relation_combination: dict[int, Fraction],
    low_relations: list[tuple[Row, Provenance]],
) -> Provenance:
    output: Provenance = {}
    for relation_index, coefficient in relation_combination.items():
        add_scaled(output, coefficient, low_relations[relation_index][1])
    return output


def certificate_payload(
    monomial: Monomial,
    provenance: Provenance,
    live: set[int],
) -> dict[str, object]:
    zeros = set(range(1, len(ENTRY_KEYS) + 1)) - live
    residual: dict[Monomial, Fraction] = defaultdict(Fraction)
    sources = []
    for (word, multiplier), coefficient in sorted(provenance.items()):
        polynomial = hafnian(VERTICES, word, zeros)
        if len(set(word)) == 1:
            polynomial[()] = polynomial.get((), 0) - 1
        for term, value in polynomial.items():
            residual[tuple(sorted((*multiplier, *term)))] += coefficient * value
        sources.append(
            {
                "word": "".join(map(str, word)),
                "multiplier": list(multiplier),
                "coefficient": fraction_text(coefficient),
            }
        )
    residual = {key: value for key, value in residual.items() if value}
    expected = {monomial: Fraction(1)}
    if residual != expected:
        raise AssertionError("reconstructed singleton certificate has nonzero residual")
    return {"target_monomial": list(monomial), "sources": sources}


def run_probe(support_path: Path) -> dict[str, object]:
    started = time.monotonic()
    raw_support = support_path.read_bytes()
    support_payload = json.loads(raw_support)
    support_list = support_payload["nonzero_entry_ids"]
    if len(support_list) != len(set(support_list)):
        raise ValueError("support contains duplicate live entry ids")
    live = set(support_list)
    target_grades, rows_for_grade = build_problem(live)

    block_row_histogram: Counter[int] = Counter()
    row_count = 0
    high_rank_sum = 0
    low_relations: list[tuple[Row, Provenance]] = []
    zero_high_dependencies = 0
    for grade in target_grades:
        rows = rows_for_grade(grade)
        block_row_histogram[len(rows)] += 1
        row_count += len(rows)
        high_basis, relations, zero_relations = high_echelon(rows)
        high_rank_sum += len(high_basis)
        low_relations.extend(relations)
        zero_high_dependencies += zero_relations

    low_rows = [row for row, _ in low_relations]
    low_basis = exact_rref(low_rows)
    low_singletons = [item for item in low_basis if len(item[1]) == 1]
    if low_singletons:
        _, row, relation_combination = low_singletons[0]
        monomial, coefficient = next(iter(row.items()))
        provenance = expand_low_provenance(relation_combination, low_relations)
        provenance = {key: value / coefficient for key, value in provenance.items()}
        certificate = certificate_payload(monomial, provenance, live)
        outcome = "EXACT_LOW_MONOMIAL_IN_CROSS_GRADE_ROW_SPACE"
        high_blocks_checked = 0
    else:
        certificate = None
        outcome = "EXACT_ABSENCE_OF_MONOMIAL_IN_COMPLETE_PURE_ATTACHED_ROW_SPACE"
        high_blocks_checked = 0
        for grade in target_grades:
            rows = rows_for_grade(grade)
            high_basis, _, _ = high_echelon(rows)
            augmented_rows = []
            local_metadata = []
            for _, high, low, provenance in high_basis:
                low_remainder, used_low_basis = reduce_low(low, low_basis)
                augmented = dict(high)
                add_scaled(augmented, Fraction(1), low_remainder)
                augmented_rows.append(augmented)
                local_metadata.append((provenance, used_low_basis))
            block_rref = exact_rref(augmented_rows)
            singletons = [item for item in block_rref if len(item[1]) == 1]
            high_blocks_checked += 1
            if not singletons:
                continue
            _, singleton_row, block_combination = singletons[0]
            monomial, coefficient = next(iter(singleton_row.items()))
            provenance: Provenance = {}
            for local_index, local_coefficient in block_combination.items():
                local_provenance, used_low_basis = local_metadata[local_index]
                add_scaled(provenance, local_coefficient, local_provenance)
                for low_basis_index, reduction_coefficient in used_low_basis.items():
                    low_relation_combination = low_basis[low_basis_index][2]
                    expanded = expand_low_provenance(
                        low_relation_combination, low_relations
                    )
                    add_scaled(
                        provenance,
                        -local_coefficient * reduction_coefficient,
                        expanded,
                    )
            provenance = {key: value / coefficient for key, value in provenance.items()}
            certificate = certificate_payload(monomial, provenance, live)
            outcome = "EXACT_HIGH_MONOMIAL_IN_CROSS_GRADE_ROW_SPACE"
            break

    try:
        display_path = support_path.resolve().relative_to(
            ROOT
        ).as_posix()
    except ValueError:
        display_path = support_path.as_posix()
    return {
        "schema": "n8-degree6-pure-attached-cross-grade-coupling-v1",
        "status": "PASS",
        "outcome": outcome,
        "support": {
            "path": display_path,
            "raw_sha256": hashlib.sha256(raw_support).hexdigest(),
            "lf_sha256": hashlib.sha256(raw_support.replace(b"\r\n", b"\n")).hexdigest(),
            "declared_status": support_payload.get("status"),
            "declared_scope": support_payload.get("scope"),
            "live_entry_count": len(live),
        },
        "declared_space": {
            "coefficient_field": "Q",
            "quadratic_multipliers": len(live) * (len(live) + 1) // 2,
            "target_grade_rule": (
                "all endpoint-colour grades equal to a live quadratic multiplier "
                "times at least one pure target word"
            ),
            "mixed_only_unattached_grades_included": False,
            "rho_used": False,
            "division_used": False,
            "cofactor_abstraction_used": False,
        },
        "exact_elimination": {
            "high_grade_blocks": len(target_grades),
            "source_rows": row_count,
            "high_rank_sum": high_rank_sum,
            "high_kernel_dimension": row_count - high_rank_sum,
            "nonzero_low_relations": len(low_relations),
            "zero_full_dependencies_after_high_elimination": zero_high_dependencies,
            "global_low_rank": len(low_basis),
            "global_low_singletons": len(low_singletons),
            "high_blocks_checked_mod_global_low_space": high_blocks_checked,
            "block_row_count_histogram": dict(sorted(block_row_histogram.items())),
        },
        "certificate": certificate,
        "interpretation": (
            "The conclusion concerns every q*P_word row in a high grade that can "
            "meet a pure word for the supplied support. It does not claim absence "
            "from mixed-only degree-six grades or from the full target ideal."
        ),
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("support", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_probe(args.support)
    payload = json.dumps(result, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
