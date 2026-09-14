"""Bounded exact probe on the tracked 134-entry n=8 physical support.

This script is intentionally self-contained.  It reconstructs physical entry
numbering, perfect matchings, and the four source equations without importing
the repository cancellation encoders or the accompanying review archive.

The experiment applies every allowed vertex/common-colour image of the
division-free boundary consequence whose 17 zero and six nonzero premises are
satisfied by the fixed support.  It then transports those physical binomials
through every complete mixed full-word hafnian, including fibres with three or
more matching monomials.  A contradiction is reported only if a boundary
relation equates a live monomial with zero, or a complete mixed fibre becomes
a nonzero singleton Laurent class over characteristic zero.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path


N = 8
D = 3
SOURCE_COMMIT = "049cc885b825c2de13e6d6f00d1a9422b49f7ef3"
VERTICES = tuple(range(N))
ENTRY_KEYS = tuple(
    (u, v, a, b)
    for u, v in itertools.combinations(VERTICES, 2)
    for a, b in itertools.product(range(D), repeat=2)
)
ENTRY_ID = {key: index for index, key in enumerate(ENTRY_KEYS, start=1)}

ORIGINAL_WORDS = ("00000010", "00000110", "00100000", "00100100")
ORIGINAL_ZEROS = (
    19,
    73,
    92,
    109,
    163,
    181,
    182,
    190,
    199,
    200,
    208,
    209,
    217,
    229,
    230,
    235,
    238,
)
ORIGINAL_REQUIRED_NONZEROS = (38, 55, 82, 118, 121, 247)
RELATION_LEFT = (226, 247)
RELATION_RIGHT = (227, 244)
REVIEWED_VERTEX_MAP = (0, 6, 2, 3, 7, 5, 1, 4)
REVIEWED_COLOUR_MAP = (0, 2, 1)

Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(*polys: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def scale(coefficient: int, poly: Polynomial) -> Polynomial:
    return clean({monomial: coefficient * value for monomial, value in poly.items()})


def multiply(*polys: Polynomial) -> Polynomial:
    result: Polynomial = {(): 1}
    for poly in polys:
        product: Polynomial = {}
        for left, left_coefficient in result.items():
            for right, right_coefficient in poly.items():
                monomial = tuple(sorted((*left, *right)))
                product[monomial] = product.get(monomial, 0) + left_coefficient * right_coefficient
        result = clean(product)
    return result


def variable(identifier: int) -> Polynomial:
    return {(identifier,): 1}


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


def decode(identifier: int) -> dict[str, object]:
    u, v, a, b = ENTRY_KEYS[identifier - 1]
    return {"id": identifier, "entry": f"W{u}{v}[{a},{b}]", "key": [u, v, a, b]}


def hafnian(vertices: tuple[int, ...], word: tuple[int, ...], zeros: set[int]) -> Polynomial:
    colours = dict(zip(vertices, word, strict=True))
    output: Polynomial = {}
    for matching in perfect_matchings(vertices):
        monomial = tuple(sorted(entry_id(u, v, colours[u], colours[v]) for u, v in matching))
        if any(identifier in zeros for identifier in monomial):
            continue
        output[monomial] = output.get(monomial, 0) + 1
    return output


def mapped_id(identifier: int, vertex_map: tuple[int, ...], colour_map: tuple[int, ...]) -> int:
    u, v, a, b = ENTRY_KEYS[identifier - 1]
    return entry_id(vertex_map[u], vertex_map[v], colour_map[a], colour_map[b])


def mapped_word(word: str, vertex_map: tuple[int, ...], colour_map: tuple[int, ...]) -> str:
    output = [-1] * N
    for vertex, colour in enumerate(map(int, word)):
        output[vertex_map[vertex]] = colour_map[colour]
    return "".join(map(str, output))


def subtract_row(target: dict[int, int], multiplier: int, source: dict[int, int]) -> None:
    for variable_id, coefficient in source.items():
        target[variable_id] = target.get(variable_id, 0) - multiplier * coefficient
        if target[variable_id] == 0:
            del target[variable_id]


def canonical_row(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    row = Counter(left)
    row.subtract(right)
    row = Counter({identifier: coefficient for identifier, coefficient in row.items() if coefficient})
    first = min(row)
    if row[first] < 0:
        row = Counter({identifier: -coefficient for identifier, coefficient in row.items()})
    return tuple(sorted(row.items()))


def build_unit_lattice(rows: list[dict[int, int]]) -> tuple[list[tuple[int, dict[int, int]]], list[dict[int, int]]]:
    """Build the exact sublattice reachable using only unit pivots.

    If the residual list is empty, the basis spans every supplied relation over
    the integers.  Otherwise it remains a sound, possibly incomplete sublattice.
    """

    pivots: list[tuple[int, dict[int, int]]] = []
    pending = [dict(row) for row in rows]
    while pending:
        added = False
        residual = []
        for row in pending:
            for pivot, pivot_row in pivots:
                if pivot in row:
                    subtract_row(row, row[pivot], pivot_row)
            units = [identifier for identifier, coefficient in row.items() if abs(coefficient) == 1]
            if not units:
                if row:
                    residual.append(row)
                continue
            pivot = min(units)
            if row[pivot] < 0:
                row = {identifier: -coefficient for identifier, coefficient in row.items()}
            pivots.append((pivot, row))
            added = True
        if not added:
            return pivots, residual
        pending = residual
    return pivots, []


def lattice_normal_form(monomial: Monomial, pivots: list[tuple[int, dict[int, int]]]) -> tuple[tuple[int, int], ...]:
    row = dict(Counter(monomial))
    for pivot, pivot_row in pivots:
        if pivot in row:
            subtract_row(row, row[pivot], pivot_row)
    return tuple(sorted(row.items()))


def reconstruct_boundary_identity() -> dict[str, object]:
    zeros = set(ORIGINAL_ZEROS)
    full = [hafnian(VERTICES, tuple(map(int, word)), zeros) for word in ORIGINAL_WORDS]
    h = hafnian((0, 1, 4, 5), (0, 0, 0, 0), zeros)
    k0 = hafnian((0, 1, 2, 4, 6, 7), (0, 0, 0, 0, 1, 0), zeros)
    k1 = hafnian((0, 1, 2, 4, 6, 7), (0, 0, 1, 0, 0, 0), zeros)

    a, b, c, d = map(variable, (118, 121, 172, 173))
    x, y, z0, z1, s, t, e = map(variable, (38, 82, 244, 247, 226, 55, 227))
    expected = (
        add(multiply(a, z1, h), multiply(c, k0), multiply(a, e, t, y)),
        add(multiply(a, x, y, z1), multiply(d, k0)),
        add(multiply(b, add(multiply(s, t, y), multiply(z0, h))), multiply(c, k1)),
        add(multiply(b, x, y, z0), multiply(d, k1)),
    )
    expansion_checks = [actual == wanted for actual, wanted in zip(full, expected, strict=True)]
    if not all(expansion_checks):
        raise AssertionError("a reconstructed full source expansion differs")

    boundary = add(multiply(s, z1), scale(-1, multiply(e, z0)))
    n_poly = multiply(a, b, t, y, boundary)
    f1, f2, f3, f4 = full
    r_poly = add(
        multiply(a, z1, add(multiply(d, f3), scale(-1, multiply(c, f4)))),
        scale(-1, multiply(b, z0, add(multiply(d, f1), scale(-1, multiply(c, f2))))),
    )
    rhs = multiply(a, a, b, t, x, y, y, z1, boundary)
    if r_poly != multiply(d, n_poly):
        raise AssertionError("R=d*N identity failed")
    if add(multiply(n_poly, f2), scale(-1, multiply(k0, r_poly))) != rhs:
        raise AssertionError("denominator-free boundary certificate failed")

    mapped_zeros = sorted(mapped_id(i, REVIEWED_VERTEX_MAP, REVIEWED_COLOUR_MAP) for i in ORIGINAL_ZEROS)
    mapped_nonzeros = sorted(
        mapped_id(i, REVIEWED_VERTEX_MAP, REVIEWED_COLOUR_MAP)
        for i in ORIGINAL_REQUIRED_NONZEROS
    )
    mapped_left = tuple(mapped_id(i, REVIEWED_VERTEX_MAP, REVIEWED_COLOUR_MAP) for i in RELATION_LEFT)
    mapped_right = tuple(mapped_id(i, REVIEWED_VERTEX_MAP, REVIEWED_COLOUR_MAP) for i in RELATION_RIGHT)
    return {
        "entry_count": len(ENTRY_KEYS),
        "full_word_monomial_counts": [len(poly) for poly in full],
        "expansion_checks": expansion_checks,
        "integer_polynomial_certificate_checked": True,
        "division_used": False,
        "proper_cofactor_nonzero_assumptions": [],
        "zero_entry_ids": list(ORIGINAL_ZEROS),
        "required_nonzero_entry_ids": list(ORIGINAL_REQUIRED_NONZEROS),
        "required_nonzero_entries": [decode(i) for i in ORIGINAL_REQUIRED_NONZEROS],
        "boundary_relation": {
            "left": list(RELATION_LEFT),
            "right": list(RELATION_RIGHT),
            "entry_decoding": [decode(i) for i in (*RELATION_LEFT, *RELATION_RIGHT)],
        },
        "mapped_reviewed_placement": {
            "vertex_map": list(REVIEWED_VERTEX_MAP),
            "colour_map": list(REVIEWED_COLOUR_MAP),
            "zero_entry_ids": mapped_zeros,
            "required_nonzero_entry_ids": mapped_nonzeros,
            "full_target_words": [
                mapped_word(word, REVIEWED_VERTEX_MAP, REVIEWED_COLOUR_MAP)
                for word in ORIGINAL_WORDS
            ],
            "relation_left": list(mapped_left),
            "relation_right": list(mapped_right),
        },
    }


def run_probe(fixture_path: Path) -> dict[str, object]:
    raw_fixture = fixture_path.read_bytes()
    fixture = json.loads(raw_fixture)
    support_list = fixture["nonzero_entry_ids"]
    if len(support_list) != 134 or len(set(support_list)) != 134:
        raise ValueError("fixture does not contain 134 distinct live physical entries")
    support = set(support_list)

    premise = reconstruct_boundary_identity()
    mapped_review = premise["mapped_reviewed_placement"]
    mapped_review["fixture_satisfies_zero_premises"] = not (
        set(mapped_review["zero_entry_ids"]) & support
    )
    mapped_review["fixture_satisfies_nonzero_premises"] = set(
        mapped_review["required_nonzero_entry_ids"]
    ) <= support
    mapped_review["all_four_relation_entries_live"] = set(
        (*mapped_review["relation_left"], *mapped_review["relation_right"])
    ) <= support

    placements = 0
    applicable = 0
    both_live = 0
    both_zero = 0
    both_zero_records = []
    one_live = []
    relation_records: dict[tuple[tuple[int, int], ...], dict[str, object]] = {}
    for vertex_map in itertools.permutations(VERTICES):
        for colour_map in itertools.permutations(range(D)):
            placements += 1
            mapped_zeros = tuple(mapped_id(i, vertex_map, colour_map) for i in ORIGINAL_ZEROS)
            if any(identifier in support for identifier in mapped_zeros):
                continue
            mapped_nonzeros = tuple(
                mapped_id(i, vertex_map, colour_map) for i in ORIGINAL_REQUIRED_NONZEROS
            )
            if any(identifier not in support for identifier in mapped_nonzeros):
                continue
            applicable += 1
            left = tuple(mapped_id(i, vertex_map, colour_map) for i in RELATION_LEFT)
            right = tuple(mapped_id(i, vertex_map, colour_map) for i in RELATION_RIGHT)
            left_live = all(identifier in support for identifier in left)
            right_live = all(identifier in support for identifier in right)
            if left_live != right_live:
                one_live.append(
                    {
                        "vertex_map": list(vertex_map),
                        "colour_map": list(colour_map),
                        "left": list(left),
                        "right": list(right),
                        "left_live": left_live,
                        "right_live": right_live,
                    }
                )
            elif left_live:
                both_live += 1
                key = canonical_row(left, right)
                relation_records.setdefault(
                    key,
                    {
                        "row": [list(pair) for pair in key],
                        "left": list(left),
                        "right": list(right),
                        "vertex_map": list(vertex_map),
                        "colour_map": list(colour_map),
                        "full_target_words": [
                            mapped_word(word, vertex_map, colour_map) for word in ORIGINAL_WORDS
                        ],
                    },
                )
            else:
                both_zero += 1
                both_zero_records.append(
                    {
                        "vertex_map": list(vertex_map),
                        "colour_map": list(colour_map),
                        "left": list(left),
                        "right": list(right),
                        "left_live_factors": [identifier in support for identifier in left],
                        "right_live_factors": [identifier in support for identifier in right],
                        "full_target_words": [
                            mapped_word(word, vertex_map, colour_map) for word in ORIGINAL_WORDS
                        ],
                    }
                )

    rows = [dict(key) for key in relation_records]
    pivots, residual_rows = build_unit_lattice(rows)

    mixed_size_histogram: Counter[int] = Counter()
    quotient_class_histogram: Counter[int] = Counter()
    pure_sizes: dict[str, int] = {}
    small_mixed = []
    singleton_quotients = []
    closest_quotient = None
    for word_tuple in itertools.product(range(D), repeat=N):
        word = "".join(map(str, word_tuple))
        poly = hafnian(VERTICES, word_tuple, set(range(1, 253)) - support)
        terms = list(poly)
        if len(set(word_tuple)) == 1:
            pure_sizes[word] = len(terms)
            continue
        mixed_size_histogram[len(terms)] += 1
        if len(terms) <= 2:
            small_mixed.append({"word": word, "terms": [list(term) for term in terms]})
        classes: dict[tuple[tuple[int, int], ...], list[Monomial]] = {}
        for term in terms:
            classes.setdefault(lattice_normal_form(term, pivots), []).append(term)
        quotient_class_histogram[len(classes)] += 1
        candidate = {
            "word": word,
            "matching_terms": len(terms),
            "laurent_classes": len(classes),
            "class_sizes": sorted((len(group) for group in classes.values()), reverse=True),
        }
        if closest_quotient is None or (
            candidate["laurent_classes"],
            -candidate["class_sizes"][0],
            candidate["matching_terms"],
            candidate["word"],
        ) < (
            closest_quotient["laurent_classes"],
            -closest_quotient["class_sizes"][0],
            closest_quotient["matching_terms"],
            closest_quotient["word"],
        ):
            closest_quotient = candidate
        if len(classes) == 1:
            singleton_quotients.append(candidate)

    exact_exclusion = bool(one_live or singleton_quotients)
    if one_live:
        outcome = "EXACT_SUPPORT_EXCLUSION_BY_BOUNDARY_LIVE_ZERO_MISMATCH"
    elif singleton_quotients:
        outcome = "EXACT_SUPPORT_EXCLUSION_BY_SINGLE_LAURENT_CLASS"
    else:
        outcome = "NO_EXCLUSION_BY_THIS_BOUNDARY_QUOTIENT_MECHANISM"

    repository_root = Path(__file__).resolve().parents[2]
    try:
        fixture_display_path = fixture_path.resolve().relative_to(repository_root).as_posix()
    except ValueError:
        fixture_display_path = fixture_path.as_posix()

    return {
        "schema": "n8-physical-boundary-quotient-probe-v1",
        "status": "PASS",
        "source_commit": SOURCE_COMMIT,
        "outcome": outcome,
        "exact_support_exclusion": exact_exclusion,
        "fixture": {
            "path": fixture_display_path,
            "raw_sha256": hashlib.sha256(raw_fixture).hexdigest(),
            "declared_scope": fixture.get("scope"),
            "live_entry_count": len(support),
        },
        "premise_reconstruction": premise,
        "boundary_orbit": {
            "placements_checked": placements,
            "applicable_placements": applicable,
            "both_sides_live_placements": both_live,
            "both_sides_zero_placements": both_zero,
            "both_sides_zero_records": both_zero_records,
            "one_side_live_contradictions": one_live,
            "distinct_live_binomial_relations": len(relation_records),
            "each_relation_side_reuses_one_physical_vertex": True,
            "therefore_no_relation_side_is_a_perfect_matching_submonomial": True,
            "relations": list(relation_records.values()),
        },
        "integer_lattice_transport": {
            "unit_pivot_rank": len(pivots),
            "nonunit_residual_rows": [sorted(row.items()) for row in residual_rows],
            "complete_for_supplied_relation_lattice": not residual_rows,
        },
        "full_word_census": {
            "mixed_fibre_count": sum(mixed_size_histogram.values()),
            "live_matching_monomials": sum(
                size * count for size, count in mixed_size_histogram.items()
            ),
            "mixed_fibre_size_histogram": dict(sorted(mixed_size_histogram.items())),
            "pure_fibre_sizes": pure_sizes,
            "mixed_fibres_with_at_most_two_terms": small_mixed,
        },
        "larger_fibre_quotient": {
            "laurent_class_count_histogram": dict(sorted(quotient_class_histogram.items())),
            "relation_changes_no_fibre_classes": quotient_class_histogram == mixed_size_histogram,
            "singleton_quotients": singleton_quotients,
            "closest_quotient": closest_quotient,
        },
        "interpretation": (
            "An exclusion is claimed only for a one-live-side boundary relation or a complete "
            "mixed target fibre reduced to one nonzero Laurent class. Otherwise this run only "
            "limits the orbit of the reconstructed boundary relation on the fixed support."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--expected",
        type=Path,
        help="optionally require exact equality with a frozen result JSON",
    )
    args = parser.parse_args()
    result = json.loads(json.dumps(run_probe(args.fixture)))
    if args.expected is not None:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        if result != expected:
            raise ValueError("computed result differs from the frozen result")
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
