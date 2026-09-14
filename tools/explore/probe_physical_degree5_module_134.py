#!/usr/bin/env python3
"""Exact degree-five target-module probe on the fixed 134-entry support.

The declared vector space is

    span_Q({P_a : a in {0,1,2}^8} U {g_s P_a : s live, a in {0,1,2}^8})
    + <rho>_{degree <= 5},

where P_a is the fully expanded physical hafnian T_a-delta_a after every
absent fixture entry is set to zero, and

    rho = g88*g91 - g82*g97.

No cofactor symbols, divisions, or nonzero specializations are used.  The
single binomial rho is a Groebner basis for its principal ideal.  Reducing by
g88*g91 -> g82*g97 is therefore exact; because rho is homogeneous and the two
terms have the same endpoint-colour multigrade, it includes precisely all rho
multiples needed for equalities through degree five without mixing blocks.

After normal form, rows are separated by endpoint-colour multigrade.  The
constant terms of the three pure P_a rows and the linear terms of the 402
pure g_s P_a rows are retained, so their actual connected components are
reduced together.  A monomial belongs to a row space exactly when its reduced
row echelon form contains a singleton row.

This is a bounded-degree linear-span computation, not an ideal-membership
calculation for arbitrary polynomial multiples of the target equations.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterable


N = 8
D = 3
VERTICES = tuple(range(N))
PURE_WORD_IDS = (0, (3**N - 1) // 2, 3**N - 1)
RHO_LEFT = (88, 91)
RHO_RIGHT = (82, 97)

ENTRY_KEYS = tuple(
    (u, v, a, b)
    for u, v in itertools.combinations(VERTICES, 2)
    for a, b in itertools.product(range(D), repeat=2)
)
ENTRY_ID = {key: index for index, key in enumerate(ENTRY_KEYS, start=1)}
Monomial = tuple[int, ...]
IntegerPolynomial = dict[Monomial, int]
RationalRow = dict[Monomial, Fraction]
RowLabel = tuple[int, int | None]


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


def entry_id(u: int, v: int, a: int, b: int) -> int:
    if u > v:
        u, v, a, b = v, u, b, a
    return ENTRY_ID[(u, v, a, b)]


def decode_entry(identifier: int) -> dict[str, object]:
    u, v, a, b = ENTRY_KEYS[identifier - 1]
    return {"id": identifier, "entry": f"W{u}{v}[{a},{b}]", "key": [u, v, a, b]}


def word_tuple(word_id: int) -> tuple[int, ...]:
    digits = [0] * N
    value = word_id
    for position in range(N - 1, -1, -1):
        digits[position] = value % D
        value //= D
    return tuple(digits)


def word_text(word_id: int) -> str:
    return "".join(map(str, word_tuple(word_id)))


def word_id(word: Iterable[int]) -> int:
    value = 0
    for digit in word:
        value = D * value + digit
    return value


def expanded_target(word: tuple[int, ...], live: set[int]) -> IntegerPolynomial:
    """Return the actual induced hafnian, with coincident terms collected."""

    output: IntegerPolynomial = {}
    for matching in perfect_matchings(VERTICES):
        monomial = tuple(
            sorted(entry_id(u, v, word[u], word[v]) for u, v in matching)
        )
        if not all(identifier in live for identifier in monomial):
            continue
        output[monomial] = output.get(monomial, 0) + 1
    return output


def target_equation(target: IntegerPolynomial, target_word_id: int) -> IntegerPolynomial:
    equation = dict(target)
    if target_word_id in PURE_WORD_IDS:
        equation[()] = equation.get((), 0) - 1
        if equation[()] == 0:
            del equation[()]
    return equation


def rho_normal_monomial(monomial: Monomial) -> Monomial:
    """Normal form for LT(rho)=g88*g91 under a compatible term order."""

    counts = Counter(monomial)
    replacements = min(counts[RHO_LEFT[0]], counts[RHO_LEFT[1]])
    if not replacements:
        return monomial
    counts[RHO_LEFT[0]] -= replacements
    counts[RHO_LEFT[1]] -= replacements
    counts[RHO_RIGHT[0]] += replacements
    counts[RHO_RIGHT[1]] += replacements
    return tuple(
        identifier
        for identifier in sorted(counts)
        for _ in range(counts[identifier])
    )


def rho_normal_polynomial(poly: IntegerPolynomial) -> tuple[IntegerPolynomial, int]:
    output: IntegerPolynomial = {}
    changed = 0
    for monomial, coefficient in poly.items():
        normal = rho_normal_monomial(monomial)
        changed += normal != monomial
        output[normal] = output.get(normal, 0) + coefficient
    return ({monomial: coefficient for monomial, coefficient in output.items() if coefficient}, changed)


def multiplied_row(
    target: IntegerPolynomial,
    target_word_id: int,
    multiplier: int,
) -> tuple[IntegerPolynomial, int]:
    product = {
        tuple(sorted((*monomial, multiplier))): coefficient
        for monomial, coefficient in target.items()
    }
    if target_word_id in PURE_WORD_IDS:
        product[(multiplier,)] = product.get((multiplier,), 0) - 1
    return rho_normal_polynomial(product)


def fraction_json(value: Fraction) -> int | str:
    if value.denominator == 1:
        return value.numerator
    return f"{value.numerator}/{value.denominator}"


def rref(
    labelled_rows: list[tuple[RowLabel, IntegerPolynomial]],
    *,
    track_combinations: bool = False,
) -> tuple[list[tuple[Monomial, RationalRow, dict[RowLabel, Fraction]]], int]:
    """Compute exact sparse RREF, returning pivot rows and input row rank."""

    basis: list[tuple[Monomial, RationalRow, dict[RowLabel, Fraction]]] = []
    for label, integer_row in labelled_rows:
        row: RationalRow = {
            monomial: Fraction(coefficient) for monomial, coefficient in integer_row.items()
        }
        combination = {label: Fraction(1)} if track_combinations else {}
        for pivot, pivot_row, pivot_combination in basis:
            coefficient = row.get(pivot)
            if coefficient is None:
                continue
            for monomial, value in pivot_row.items():
                updated = row.get(monomial, Fraction(0)) - coefficient * value
                if updated:
                    row[monomial] = updated
                else:
                    row.pop(monomial, None)
            if track_combinations:
                for source_label, value in pivot_combination.items():
                    updated = combination.get(source_label, Fraction(0)) - coefficient * value
                    if updated:
                        combination[source_label] = updated
                    else:
                        combination.pop(source_label, None)
        if not row:
            continue
        pivot = min(row, key=lambda monomial: (len(monomial), monomial))
        pivot_coefficient = row[pivot]
        row = {monomial: value / pivot_coefficient for monomial, value in row.items()}
        if track_combinations:
            combination = {
                source_label: value / pivot_coefficient
                for source_label, value in combination.items()
            }

        updated_basis = []
        for old_pivot, old_row, old_combination in basis:
            coefficient = old_row.get(pivot)
            if coefficient is not None:
                for monomial, value in row.items():
                    updated = old_row.get(monomial, Fraction(0)) - coefficient * value
                    if updated:
                        old_row[monomial] = updated
                    else:
                        old_row.pop(monomial, None)
                if track_combinations:
                    for source_label, value in combination.items():
                        updated = old_combination.get(source_label, Fraction(0)) - coefficient * value
                        if updated:
                            old_combination[source_label] = updated
                        else:
                            old_combination.pop(source_label, None)
            updated_basis.append((old_pivot, old_row, old_combination))
        updated_basis.append((pivot, row, combination))
        basis = sorted(updated_basis, key=lambda item: (len(item[0]), item[0]))
    return basis, len(basis)


def row_space_singletons(
    labelled_rows: list[tuple[RowLabel, IntegerPolynomial]],
) -> tuple[int, list[tuple[Monomial, dict[RowLabel, Fraction]]]]:
    basis, rank = rref(labelled_rows, track_combinations=True)
    singletons = []
    for _, row, combination in basis:
        if len(row) == 1:
            monomial, coefficient = next(iter(row.items()))
            adjusted = {
                label: value / coefficient for label, value in combination.items()
            }
            singletons.append((monomial, adjusted))
    return rank, singletons


def endpoint_multigrade(monomial: Monomial) -> tuple[tuple[int, int, int], ...]:
    grade = [[0, 0, 0] for _ in VERTICES]
    for identifier in monomial:
        u, v, a, b = ENTRY_KEYS[identifier - 1]
        grade[u][a] += 1
        grade[v][b] += 1
    return tuple(tuple(row) for row in grade)


def polynomial_json(poly: IntegerPolynomial) -> list[dict[str, object]]:
    return [
        {"coefficient": coefficient, "entry_ids": list(monomial)}
        for monomial, coefficient in sorted(poly.items(), key=lambda item: (len(item[0]), item[0]))
    ]


def canonical_targets_hash(targets: list[IntegerPolynomial]) -> str:
    digest = hashlib.sha256()
    for target_word_id, target in enumerate(targets):
        digest.update(target_word_id.to_bytes(2, "big"))
        for monomial, coefficient in sorted(target.items()):
            digest.update(bytes(monomial))
            digest.update(b":")
            digest.update(str(coefficient).encode("ascii"))
            digest.update(b";")
        digest.update(b"\n")
    return digest.hexdigest()


def decomposition_options(colour_multiset: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    first, second = colour_multiset
    if first == second:
        return ((first, second),)
    return ((first, second), (second, first))


def certificate_json(
    monomial: Monomial,
    combination: dict[RowLabel, Fraction],
) -> dict[str, object]:
    return {
        "normal_form_monomial": list(monomial),
        "target_row_combination": [
            {
                "coefficient": fraction_json(coefficient),
                "target_word": word_text(label[0]),
                "multiplier_entry_id": label[1],
            }
            for label, coefficient in sorted(combination.items())
        ],
        "note": (
            "This compact combination is in rho normal form. Re-expanding the listed "
            "physical rows and polynomial-dividing their combination by rho reconstructs "
            "the degree-at-most-three rho coefficient without division by an entry."
        ),
    }


def run_probe(fixture_path: Path) -> dict[str, object]:
    raw_fixture = fixture_path.read_bytes()
    fixture = json.loads(raw_fixture)
    support_list = fixture["nonzero_entry_ids"]
    if len(support_list) != 134 or len(set(support_list)) != 134:
        raise ValueError("fixture does not contain 134 distinct live entries")
    live = set(support_list)
    if not set((*RHO_LEFT, *RHO_RIGHT)) <= live:
        raise ValueError("rho contains an entry absent from the declared support")

    rho_left_grade = endpoint_multigrade(RHO_LEFT)
    rho_right_grade = endpoint_multigrade(RHO_RIGHT)
    if rho_left_grade != rho_right_grade:
        raise AssertionError("rho is not endpoint-colour homogeneous")

    targets = [expanded_target(word_tuple(identifier), live) for identifier in range(D**N)]
    equations = [target_equation(target, identifier) for identifier, target in enumerate(targets)]
    target_term_histogram = Counter(len(target) for target in targets)
    target_nonzero = sum(bool(target) for target in targets)

    singleton_certificates: list[dict[str, object]] = []
    component_count_degree4 = 0
    rank_degree4 = 0

    # Every mixed equation has its own endpoint grade.  The three pure rows
    # share the constant column and must be reduced together.
    for identifier, equation in enumerate(equations):
        if identifier in PURE_WORD_IDS:
            continue
        normal, _ = rho_normal_polynomial(equation)
        component_count_degree4 += 1
        rank, singletons = row_space_singletons([((identifier, None), normal)])
        rank_degree4 += rank
        singleton_certificates.extend(
            certificate_json(monomial, combination) for monomial, combination in singletons
        )
    pure_degree4_rows = []
    for identifier in PURE_WORD_IDS:
        normal, _ = rho_normal_polynomial(equations[identifier])
        pure_degree4_rows.append(((identifier, None), normal))
    component_count_degree4 += 1
    rank, singletons = row_space_singletons(pure_degree4_rows)
    rank_degree4 += rank
    singleton_certificates.extend(
        certificate_json(monomial, combination) for monomial, combination in singletons
    )

    degree5_rows_generated = 0
    degree5_nonempty_blocks = 0
    degree5_empty_grades = 0
    degree5_rank = 0
    degree5_component_count = 0
    degree5_changed_terms = 0
    max_block_rows = 0
    max_block_columns = 0
    row_size_histogram: Counter[int] = Counter()
    block_row_histogram: Counter[int] = Counter()
    private_column_blocks = 0
    pure_blocks_by_multiplier: dict[int, list[list[tuple[RowLabel, IntegerPolynomial]]]] = {
        identifier: [] for identifier in support_list
    }
    # One byte per possible (target word, physical entry) pair makes coverage
    # independently checkable without retaining 879,174 row objects.
    product_coverage = bytearray(D**N * (len(ENTRY_KEYS) + 1))

    colour_multisets = tuple(itertools.combinations_with_replacement(range(D), 2))
    for u, v in itertools.combinations(VERTICES, 2):
        other_vertices = tuple(vertex for vertex in VERTICES if vertex not in (u, v))
        for u_multiset in colour_multisets:
            u_options = decomposition_options(u_multiset)
            for v_multiset in colour_multisets:
                v_options = decomposition_options(v_multiset)
                for other_colours in itertools.product(range(D), repeat=N - 2):
                    base_word = [-1] * N
                    for vertex, colour in zip(other_vertices, other_colours, strict=True):
                        base_word[vertex] = colour
                    labelled_rows: list[tuple[RowLabel, IntegerPolynomial]] = []
                    pure_multiplier: int | None = None
                    for target_u, multiplier_u in u_options:
                        base_word[u] = target_u
                        for target_v, multiplier_v in v_options:
                            base_word[v] = target_v
                            multiplier = entry_id(u, v, multiplier_u, multiplier_v)
                            if multiplier not in live:
                                continue
                            target_identifier = word_id(base_word)
                            coverage_offset = (
                                target_identifier * (len(ENTRY_KEYS) + 1) + multiplier
                            )
                            if product_coverage[coverage_offset]:
                                raise AssertionError(
                                    f"duplicate product row ({target_identifier}, {multiplier})"
                                )
                            product_coverage[coverage_offset] = 1
                            row, changed = multiplied_row(
                                targets[target_identifier], target_identifier, multiplier
                            )
                            degree5_changed_terms += changed
                            degree5_rows_generated += 1
                            row_size_histogram[len(row)] += 1
                            labelled_rows.append(((target_identifier, multiplier), row))
                            if target_identifier in PURE_WORD_IDS:
                                if pure_multiplier is not None:
                                    raise AssertionError("a grade block contains two pure rows")
                                pure_multiplier = multiplier

                    if not labelled_rows:
                        degree5_empty_grades += 1
                        continue
                    degree5_nonempty_blocks += 1
                    block_row_histogram[len(labelled_rows)] += 1
                    max_block_rows = max(max_block_rows, len(labelled_rows))
                    columns = set().union(*(set(row) for _, row in labelled_rows))
                    max_block_columns = max(max_block_columns, len(columns))
                    incidence = Counter(
                        monomial for _, row in labelled_rows for monomial in row
                    )
                    if any(count == 1 for count in incidence.values()):
                        private_column_blocks += 1
                    if pure_multiplier is not None:
                        pure_blocks_by_multiplier[pure_multiplier].append(labelled_rows)
                        continue
                    degree5_component_count += 1
                    rank, singletons = row_space_singletons(labelled_rows)
                    degree5_rank += rank
                    singleton_certificates.extend(
                        certificate_json(monomial, combination)
                        for monomial, combination in singletons
                    )

    expected_products = len(support_list) * D**N
    if degree5_rows_generated != expected_products:
        raise AssertionError(
            f"generated {degree5_rows_generated} products, expected {expected_products}"
        )
    for target_identifier in range(D**N):
        base_offset = target_identifier * (len(ENTRY_KEYS) + 1)
        for multiplier in support_list:
            if not product_coverage[base_offset + multiplier]:
                raise AssertionError(
                    f"missing product row ({target_identifier}, {multiplier})"
                )
    for multiplier, blocks in pure_blocks_by_multiplier.items():
        if len(blocks) != D:
            raise AssertionError(
                f"live multiplier {multiplier} belongs to {len(blocks)} pure blocks, expected 3"
            )
        component = [labelled_row for block in blocks for labelled_row in block]
        degree5_component_count += 1
        rank, singletons = row_space_singletons(component)
        degree5_rank += rank
        singleton_certificates.extend(
            certificate_json(monomial, combination) for monomial, combination in singletons
        )

    positive_degree_singletons = [
        certificate
        for certificate in singleton_certificates
        if certificate["normal_form_monomial"]
    ]
    if positive_degree_singletons:
        outcome = "NONZERO_LIVE_MONOMIAL_IN_DECLARED_ROW_SPACE_MOD_RHO"
    elif singleton_certificates:
        outcome = "UNIT_IN_DECLARED_ROW_SPACE_MOD_RHO"
    else:
        outcome = "EXACT_ABSENCE_OF_MONOMIAL_IN_DECLARED_ROW_SPACE_MOD_RHO"

    repository_root = Path(__file__).resolve().parents[2]
    try:
        fixture_display = fixture_path.resolve().relative_to(repository_root).as_posix()
    except ValueError:
        fixture_display = fixture_path.as_posix()

    return {
        "schema": "n8-physical-degree5-module-134-probe-v1",
        "status": "PASS",
        "outcome": outcome,
        "exact_arithmetic": "Q via fractions.Fraction; integer expansion and rho reduction",
        "fixture": {
            "path": fixture_display,
            "raw_sha256": hashlib.sha256(raw_fixture).hexdigest(),
            "declared_scope": fixture.get("scope"),
            "live_entry_count": len(live),
        },
        "declared_space": {
            "coefficient_field": "Q",
            "absent_entries_substituted_zero": True,
            "target_equations": D**N,
            "linear_multipliers_per_target": len(live),
            "linear_target_products": expected_products,
            "rho": {
                "left": list(RHO_LEFT),
                "right": list(RHO_RIGHT),
                "decoded_entries": [
                    decode_entry(identifier)
                    for identifier in (*RHO_LEFT, *RHO_RIGHT)
                ],
                "endpoint_colour_multigrade_checked_equal": True,
                "normal_form_rule": "g88*g91 -> g82*g97",
                "term_order": "lexicographic with g88 first; remaining variables arbitrary",
                "groebner_basis_reason": "one polynomial is a Groebner basis for its principal ideal",
                "all_consequences_through_degree_five_included": True,
                "maximum_rho_coefficient_degree_needed": 3,
            },
            "division_used": False,
            "localization_used": False,
            "cofactor_abstraction_used": False,
            "limitation": (
                "Only constant and live-entry-linear multiples of P_a are included; "
                "higher-degree polynomial multiples of P_a are outside this row space."
            ),
        },
        "expanded_targets": {
            "target_polynomial_count": len(targets),
            "nonzero_target_polynomials": target_nonzero,
            "term_count_histogram": dict(sorted(target_term_histogram.items())),
            "canonical_sha256": canonical_targets_hash(targets),
            "pure_equations": [
                {
                    "word": word_text(identifier),
                    "T_expanded": polynomial_json(targets[identifier]),
                    "P_expanded": polynomial_json(equations[identifier]),
                }
                for identifier in PURE_WORD_IDS
            ],
            "shared_cofactors_retained_as_matching_monomials": True,
        },
        "exact_row_reduction": {
            "degree_zero_four": {
                "components": component_count_degree4,
                "rank_sum": rank_degree4,
            },
            "degree_one_five": {
                "rows_generated": degree5_rows_generated,
                "product_labels_complete_and_unique": True,
                "product_coverage_bitmap_sha256": hashlib.sha256(product_coverage).hexdigest(),
                "nonempty_multigrade_blocks": degree5_nonempty_blocks,
                "empty_multigrade_grades": degree5_empty_grades,
                "connected_components_after_pure_lower_columns": degree5_component_count,
                "rank_sum": degree5_rank,
                "row_size_histogram": dict(sorted(row_size_histogram.items())),
                "block_row_count_histogram": dict(sorted(block_row_histogram.items())),
                "maximum_block_rows_before_pure_join": max_block_rows,
                "maximum_block_columns_before_pure_join": max_block_columns,
                "blocks_with_a_private_column": private_column_blocks,
                "terms_changed_by_rho_normal_form": degree5_changed_terms,
                "pure_blocks_joined_per_live_multiplier": D,
            },
            "singleton_rref_rows": len(singleton_certificates),
        },
        "certificates": singleton_certificates,
        "interpretation": (
            "A singleton RREF row is exactly a scalar multiple of a monomial in the "
            "declared quotient row space. Absence is exact for the stated bounded space "
            "over Q, but does not exclude the support using quadratic-or-higher target "
            "multipliers and does not establish P8 or the global conjecture."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--expected",
        type=Path,
        help="optionally require exact equality with a frozen deterministic result JSON",
    )
    args = parser.parse_args()
    # Normalize integer Counter keys exactly as JSON does before frozen replay.
    result = json.loads(json.dumps(run_probe(args.fixture)))
    if args.expected is not None:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        if result != expected:
            raise ValueError("computed result differs from the frozen result")
    payload = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
