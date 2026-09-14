"""Exact replay of the reviewed eight-vertex 25-literal physical cut.

The checker expands hafnians as sparse integer polynomials indexed by physical
entry ids.  It does not use the recursive-support SAT abstraction, a quotient
certificate, SymPy, or division.  The separate review implementation used a
recursive symbolic expansion, so this matching-enumeration representation is
an independent implementation route.
"""

from __future__ import annotations

import itertools
from functools import lru_cache
from typing import Iterable


Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]
Edge = tuple[int, int]

SCHEMA = "eight-vertex-physical-hafnian-identity-v1"
TARGET_WORDS = ("00000010", "00000110", "00100000", "00100100")
ZERO_ENTRY_IDS = (
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
    227,
    229,
    230,
    235,
    238,
)
NONZERO_ENTRY_IDS = (38, 55, 82, 118, 121, 226, 247)
REMOVED_NONZERO_ENTRY_IDS = (172, 244)
PHYSICAL_CUT = (
    19,
    -38,
    -55,
    73,
    -82,
    92,
    109,
    -118,
    -121,
    163,
    181,
    182,
    190,
    199,
    200,
    208,
    209,
    217,
    -226,
    227,
    229,
    230,
    235,
    238,
    -247,
)
ENTRY_KEYS = tuple(
    (*edge, *colours)
    for edge in itertools.combinations(range(8), 2)
    for colours in itertools.product(range(3), repeat=2)
)
ENTRY_ID_OF = {key: index for index, key in enumerate(ENTRY_KEYS, start=1)}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _typed_integer_list(payload: object, name: str) -> tuple[int, ...]:
    _require(isinstance(payload, list), f"{name} must be a list")
    values = tuple(payload)
    _require(
        all(type(value) is int and value > 0 for value in values),
        f"{name} must contain positive integers (not booleans)",
    )
    _require(len(values) == len(set(values)), f"{name} contains duplicates")
    return values


def validate_pattern(payload: object) -> None:
    """Reject any pattern that is not the exact reviewed certificate input."""

    _require(isinstance(payload, dict), "pattern must be a JSON object")
    _require(payload.get("schema") == SCHEMA, "unexpected pattern schema")
    _require(type(payload.get("n")) is int and payload["n"] == 8, "order must be 8")

    words = payload.get("target_words")
    _require(
        isinstance(words, list)
        and all(type(word) is str for word in words)
        and tuple(words) == TARGET_WORDS,
        "target words differ from the checked identity",
    )
    zero_ids = _typed_integer_list(payload.get("zero_entry_ids"), "zero_entry_ids")
    nonzero_ids = _typed_integer_list(
        payload.get("nonzero_entry_ids"), "nonzero_entry_ids"
    )
    removed_ids = _typed_integer_list(
        payload.get("removed_nonzero_entry_ids"), "removed_nonzero_entry_ids"
    )
    cut = payload.get("physical_cut")
    _require(isinstance(cut, list), "physical_cut must be a list")
    _require(
        all(type(literal) is int and literal != 0 for literal in cut),
        "physical_cut must contain nonzero integers (not booleans)",
    )
    _require(len(cut) == len({abs(literal) for literal in cut}), "physical_cut repeats an entry")
    _require(zero_ids == ZERO_ENTRY_IDS, "zero-entry set differs")
    _require(nonzero_ids == NONZERO_ENTRY_IDS, "nonzero-entry set differs")
    _require(removed_ids == REMOVED_NONZERO_ENTRY_IDS, "removed-entry record differs")
    _require(tuple(cut) == PHYSICAL_CUT, "physical cut differs")
    _require(set(zero_ids).isdisjoint(nonzero_ids), "zero/nonzero assumptions overlap")
    _require(payload.get("all_unspecified_entries_arbitrary") is True, "scope flag differs")
    _require(payload.get("proof_uses_division") is False, "division flag differs")


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    """Enumerate each perfect matching once with canonical edge orientation."""

    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            result.append((((first, second)), *tail))
    return tuple(result)


def entry_id(u: int, v: int, a: int, b: int) -> int:
    """Return the one-based n=8 physical-entry id used by the SAT model."""

    _require(0 <= u < 8 and 0 <= v < 8 and u != v, "invalid vertices")
    _require(a in range(3) and b in range(3), "invalid colours")
    if u > v:
        u, v, a, b = v, u, b, a
    return ENTRY_ID_OF[(u, v, a, b)]


def _clean(polynomial: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return _clean(result)


def scale(coefficient: int, polynomial: Polynomial) -> Polynomial:
    return _clean({monomial: coefficient * value for monomial, value in polynomial.items()})


def multiply(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {(): 1}
    for polynomial in polynomials:
        product: Polynomial = {}
        for left, left_coefficient in result.items():
            for right, right_coefficient in polynomial.items():
                monomial = tuple(sorted((*left, *right)))
                product[monomial] = product.get(monomial, 0) + left_coefficient * right_coefficient
        result = _clean(product)
    return result


def variable(identifier: int) -> Polynomial:
    return {(identifier,): 1}


def hafnian_polynomial(
    vertices: Iterable[int],
    word: Iterable[int],
    zero_entry_ids: Iterable[int],
) -> Polynomial:
    """Expand one physical hafnian by explicit perfect-matching enumeration."""

    vertices_tuple = tuple(vertices)
    word_tuple = tuple(word)
    _require(len(vertices_tuple) == len(word_tuple), "word length differs from vertex count")
    _require(len(vertices_tuple) % 2 == 0, "hafnian order must be even")
    _require(len(set(vertices_tuple)) == len(vertices_tuple), "vertices repeat")
    _require(all(colour in range(3) for colour in word_tuple), "word has an invalid colour")
    colours = dict(zip(vertices_tuple, word_tuple, strict=True))
    zero_ids = set(zero_entry_ids)
    result: Polynomial = {}
    for matching in perfect_matchings(vertices_tuple):
        identifiers = tuple(
            sorted(entry_id(u, v, colours[u], colours[v]) for u, v in matching)
        )
        if any(identifier in zero_ids for identifier in identifiers):
            continue
        result[identifiers] = result.get(identifiers, 0) + 1
    return result


def replay_eight_vertex_physical_hafnian_identity(payload: object) -> dict[str, object]:
    """Replay the full expansions and the division-free polynomial certificate."""

    validate_pattern(payload)
    zero_ids = set(ZERO_ENTRY_IDS)
    full_vertices = tuple(range(8))
    full = [
        hafnian_polynomial(full_vertices, map(int, word), zero_ids)
        for word in TARGET_WORDS
    ]
    h = hafnian_polynomial((0, 1, 4, 5), (0, 0, 0, 0), zero_ids)
    k0 = hafnian_polynomial((0, 1, 2, 4, 6, 7), (0, 0, 0, 0, 1, 0), zero_ids)
    k1 = hafnian_polynomial((0, 1, 2, 4, 6, 7), (0, 0, 1, 0, 0, 0), zero_ids)

    a, b, c, d = map(variable, (118, 121, 172, 173))
    x, y, z0, z1, s, t = map(variable, (38, 82, 244, 247, 226, 55))
    expected_full = [
        add(multiply(a, z1, h), multiply(c, k0)),
        add(multiply(a, x, y, z1), multiply(d, k0)),
        add(multiply(b, add(multiply(s, t, y), multiply(z0, h))), multiply(c, k1)),
        add(multiply(b, x, y, z0), multiply(d, k1)),
    ]
    _require(full == expected_full, "one of the four full-hafnian expansions differs")

    f1, f2, f3, f4 = full
    r = add(
        multiply(a, z1, add(multiply(d, f3), scale(-1, multiply(c, f4)))),
        scale(-1, multiply(b, z0, add(multiply(d, f1), scale(-1, multiply(c, f2))))),
    )
    n_polynomial = multiply(a, b, s, t, y, z1)
    _require(r == multiply(n_polynomial, d), "intermediate identity R = N*d failed")
    rhs = multiply(a, a, b, s, t, x, y, y, z1, z1)
    _require(
        add(multiply(n_polynomial, f2), scale(-1, multiply(k0, r))) == rhs,
        "elimination identity N*F2-K0*R failed",
    )
    coefficients = (
        multiply(k0, b, z0, d),
        add(n_polynomial, scale(-1, multiply(k0, b, z0, c))),
        scale(-1, multiply(k0, a, z1, d)),
        multiply(k0, a, z1, c),
    )
    _require(
        add(*(multiply(coefficient, value) for coefficient, value in zip(coefficients, full, strict=True)))
        == rhs,
        "four-generator source certificate failed",
    )
    _require(rhs == {(38, 55, 82, 82, 118, 118, 121, 226, 247, 247): 1}, "RHS differs")

    return {
        "schema": "eight-vertex-physical-hafnian-identity-replay-v1",
        "status": "PASS",
        "scope": "exact division-free polynomial identity over Z; conditional physical cut only",
        "field_scope": "all fields",
        "full_words": list(TARGET_WORDS),
        "full_word_matching_counts_before_zeros": [105, 105, 105, 105],
        "full_word_monomial_counts_after_zeros": [len(polynomial) for polynomial in full],
        "zero_entry_ids": list(ZERO_ENTRY_IDS),
        "required_nonzero_entry_ids": list(NONZERO_ENTRY_IDS),
        "arbitrary_reviewed_entries": list(REMOVED_NONZERO_ENTRY_IDS),
        "physical_cut": list(PHYSICAL_CUT),
        "rhs_monomial_entry_ids": [38, 55, 82, 82, 118, 118, 121, 226, 247, 247],
        "rhs_coefficient": 1,
        "proof_uses_division": False,
        "all_unspecified_entries_arbitrary": True,
        "parent_coverage_claimed": False,
    }


def analyze_pattern_orbit(
    payload: object,
    nonzero_entry_ids: object,
) -> dict[str, object]:
    """Measure how one physical support avoids every allowed pattern image."""

    validate_pattern(payload)
    support_values = _typed_integer_list(nonzero_entry_ids, "nonzero_entry_ids")
    _require(all(identifier <= len(ENTRY_KEYS) for identifier in support_values), "support id is out of range")
    support = set(support_values)
    source = [
        (*ENTRY_KEYS[abs(literal) - 1], 1 if literal > 0 else -1)
        for literal in PHYSICAL_CUT
    ]
    histogram: dict[int, int] = {}
    minimum = len(PHYSICAL_CUT) + 1
    closest: list[dict[str, object]] = []
    for vertex_map in itertools.permutations(range(8)):
        for colour_map in itertools.permutations(range(3)):
            failures = []
            for u, v, a, b, sign in source:
                identifier = entry_id(
                    vertex_map[u],
                    vertex_map[v],
                    colour_map[a],
                    colour_map[b],
                )
                literal_is_true = identifier in support if sign > 0 else identifier not in support
                if literal_is_true:
                    failures.append(sign * identifier)
            distance = len(failures)
            histogram[distance] = histogram.get(distance, 0) + 1
            if distance < minimum:
                minimum = distance
                closest = []
            if distance == minimum:
                closest.append(
                    {
                        "vertex_map": list(vertex_map),
                        "colour_map": list(colour_map),
                        "failed_literals": failures,
                    }
                )
    return {
        "status": "PASS",
        "images_including_duplicates": sum(histogram.values()),
        "minimum_guard_failures": minimum,
        "distance_histogram": {str(key): histogram[key] for key in sorted(histogram)},
        "closest_images": closest,
    }
