"""Independent exact audit of the order-eight two-edge surplus-shore identity.

This verifier uses only the Python standard library.  It reconstructs physical
entry numbering, all 105 perfect matchings, the four complete hafnian source
polynomials, and their degree-six identity.  It does not import either source
probe or the primary verifier.

The identity is checked with every physical entry outside the generated
15-entry zero guard left as an independent indeterminate.  The fixed 134-entry
support is then checked only as a specialization of that stronger statement.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE = (
    REPO_ROOT / "tests/fixtures/eight_vertex_two_edge_surplus_shore.json"
)
DEFAULT_SUPPORT = (
    REPO_ROOT
    / "tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json"
)
VERTICES = tuple(range(8))
SHORE = (3, 4, 5, 6, 7)
OUTSIDE = (0, 1, 2)
BASE_COLOUR = 0
MOVING_VERTICES = (5, 7)
EXPECTED_SUPPORT_SHA256 = (
    "75cef4c3c16323a01b115d59bdbf19ddfe2b8e46a3a330333631837a6c9941fe"
)

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Monomial = tuple[int, ...]
Polynomial = Counter[Monomial]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def pair_index(u: int, v: int) -> int:
    require(0 <= u < v < 8, "physical pair must satisfy 0 <= u < v < 8")
    return u * (15 - u) // 2 + v - u - 1


def physical_id(u: int, v: int, a: int, b: int) -> int:
    require(0 <= u < 8 and 0 <= v < 8 and u != v, "bad physical edge")
    require(0 <= a < 3 and 0 <= b < 3, "bad physical colour")
    if u > v:
        u, v, a, b = v, u, b, a
    return 9 * pair_index(u, v) + 3 * a + b + 1


def decode_physical_id(identifier: int) -> tuple[int, int, int, int]:
    require(1 <= identifier <= 252, "physical id outside 1..252")
    edge_offset, colour_offset = divmod(identifier - 1, 9)
    edges = tuple(itertools.combinations(VERTICES, 2))
    u, v = edges[edge_offset]
    a, b = divmod(colour_offset, 3)
    return u, v, a, b


@lru_cache(maxsize=None)
def bitmask_matchings(mask: int) -> tuple[Matching, ...]:
    """Pair the least set bit with each other bit, independently of probes."""
    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    result = []
    choices = rest
    while choices:
        second_bit = choices & -choices
        choices ^= second_bit
        second = second_bit.bit_length() - 1
        for tail in bitmask_matchings(rest ^ second_bit):
            result.append(((first, second),) + tail)
    return tuple(result)


def permutation_matchings() -> frozenset[Matching]:
    """Collapse all 8! ordered listings into unordered pair partitions."""
    result = set()
    for permutation in itertools.permutations(VERTICES):
        pairs = [tuple(sorted(permutation[i : i + 2])) for i in range(0, 8, 2)]
        result.add(tuple(sorted(pairs)))
    return frozenset(result)


def normalized(poly: Iterable[tuple[Monomial, int]]) -> Polynomial:
    result: Polynomial = Counter()
    for monomial, coefficient in poly:
        if coefficient:
            key = tuple(sorted(monomial))
            result[key] += coefficient
            if result[key] == 0:
                del result[key]
    return result


def add_scaled(
    target: Polynomial,
    source: Polynomial,
    coefficient: int,
    multiplier: Monomial = (),
) -> None:
    for monomial, value in source.items():
        key = tuple(sorted(multiplier + monomial))
        target[key] += coefficient * value
        if target[key] == 0:
            del target[key]


def polynomial_summary(poly: Polynomial) -> dict[str, object]:
    ordered = sorted(poly.items())
    return {
        "distinct_monomials": len(poly),
        "coefficient_l1": sum(abs(value) for value in poly.values()),
        "first_monomial": list(ordered[0][0]) if ordered else None,
        "first_coefficient": ordered[0][1] if ordered else None,
    }


@dataclass(frozen=True)
class Source:
    word: str
    multiplier: Monomial
    coefficient: int  # coefficient on multiplier * P_word on the RHS


@dataclass(frozen=True)
class Pattern:
    name: str
    covering_edges: tuple[Edge, Edge]
    alternate_colours: tuple[int, int]
    zero_entry_ids: tuple[int, ...]
    nonzero_entry_ids: tuple[int, int]
    target_monomial: Monomial
    sources: tuple[Source, Source, Source, Source]


def word_with_face(first_colour: int, second_colour: int) -> str:
    word = [BASE_COLOUR] * 8
    word[MOVING_VERTICES[0]] = first_colour
    word[MOVING_VERTICES[1]] = second_colour
    return "".join(map(str, word))


def edge_entry_for_leaf(edge: Edge, leaf: int, leaf_colour: int) -> int:
    u, v = edge
    require(leaf in edge, "selected edge does not contain its moving leaf")
    colours = {
        u: leaf_colour if u == leaf else BASE_COLOUR,
        v: leaf_colour if v == leaf else BASE_COLOUR,
    }
    return physical_id(u, v, colours[u], colours[v])


def generate_pattern(
    arrangement: str,
    alternate_colours: tuple[int, int],
) -> Pattern:
    require(arrangement in {"disjoint", "adjacent"}, "unknown edge arrangement")
    require(
        alternate_colours in {(2, 1), (1, 1)},
        "audit covers the two declared alternate-colour types",
    )
    first_edge = (3, 5)
    second_edge = (6, 7) if arrangement == "disjoint" else (3, 7)
    covering_edges = (first_edge, second_edge)

    face_words = [
        word_with_face(first, second)
        for first in (BASE_COLOUR, alternate_colours[0])
        for second in (BASE_COLOUR, alternate_colours[1])
    ]
    zero_ids = set()
    for u, v in itertools.combinations(SHORE, 2):
        if (u, v) in covering_edges:
            continue
        for word in face_words:
            zero_ids.add(physical_id(u, v, int(word[u]), int(word[v])))

    x0 = edge_entry_for_leaf(first_edge, MOVING_VERTICES[0], BASE_COLOUR)
    x1 = edge_entry_for_leaf(
        first_edge, MOVING_VERTICES[0], alternate_colours[0]
    )
    y0 = edge_entry_for_leaf(second_edge, MOVING_VERTICES[1], BASE_COLOUR)
    y1 = edge_entry_for_leaf(
        second_edge, MOVING_VERTICES[1], alternate_colours[1]
    )
    sources = (
        Source(word_with_face(*alternate_colours), tuple(sorted((x0, y0))), -1),
        Source(
            word_with_face(alternate_colours[0], BASE_COLOUR),
            tuple(sorted((x0, y1))),
            +1,
        ),
        Source(
            word_with_face(BASE_COLOUR, alternate_colours[1]),
            tuple(sorted((x1, y0))),
            +1,
        ),
        Source(
            word_with_face(BASE_COLOUR, BASE_COLOUR),
            tuple(sorted((x1, y1))),
            -1,
        ),
    )
    return Pattern(
        name=f"{arrangement}_alt_{alternate_colours[0]}_{alternate_colours[1]}",
        covering_edges=covering_edges,
        alternate_colours=alternate_colours,
        zero_entry_ids=tuple(sorted(zero_ids)),
        nonzero_entry_ids=(x1, y1),
        target_monomial=tuple(sorted((x1, y1))),
        sources=sources,
    )


def matching_monomial(matching: Matching, word: str) -> Monomial:
    return tuple(
        sorted(physical_id(u, v, int(word[u]), int(word[v])) for u, v in matching)
    )


def hafnian_polynomial(
    word: str,
    zero_entry_ids: frozenset[int],
    matchings: tuple[Matching, ...],
) -> Polynomial:
    terms = []
    for matching in matchings:
        monomial = matching_monomial(matching, word)
        if zero_entry_ids.isdisjoint(monomial):
            terms.append((monomial, 1))
    return normalized(terms)


def source_polynomial(
    word: str,
    zero_entry_ids: frozenset[int],
    matchings: tuple[Matching, ...],
    include_pure_target: bool = True,
) -> Polynomial:
    result = hafnian_polynomial(word, zero_entry_ids, matchings)
    if include_pure_target and len(set(word)) == 1:
        add_scaled(result, Counter({(): 1}), -1)
    return result


def identity_residual(
    pattern: Pattern,
    matchings: tuple[Matching, ...],
    *,
    zero_guard: frozenset[int] | None = None,
    forced_zeros: frozenset[int] = frozenset(),
    source_coefficients: tuple[int, int, int, int] | None = None,
    omitted_source: int | None = None,
    include_pure_target: bool = True,
) -> Polynomial:
    guard = frozenset(pattern.zero_entry_ids) if zero_guard is None else zero_guard
    all_zeros = guard | forced_zeros
    result: Polynomial = Counter()
    if forced_zeros.isdisjoint(pattern.target_monomial):
        result[pattern.target_monomial] = 1
    coefficients = source_coefficients or tuple(s.coefficient for s in pattern.sources)
    for index, (source, coefficient) in enumerate(zip(pattern.sources, coefficients)):
        if index == omitted_source or not forced_zeros.isdisjoint(source.multiplier):
            continue
        poly = source_polynomial(
            source.word,
            all_zeros,
            matchings,
            include_pure_target=include_pure_target,
        )
        # residual = target - sum(coefficient * multiplier * P_word)
        add_scaled(result, poly, -coefficient, source.multiplier)
    return result


def validate_numbering() -> dict[str, object]:
    seen = {}
    for u, v in itertools.combinations(VERTICES, 2):
        for a in range(3):
            for b in range(3):
                identifier = physical_id(u, v, a, b)
                require(identifier not in seen, "physical numbering collision")
                seen[identifier] = (u, v, a, b)
                require(
                    decode_physical_id(identifier) == (u, v, a, b),
                    "physical id decode mismatch",
                )
                require(
                    physical_id(v, u, b, a) == identifier,
                    "edge-reversal colour convention mismatch",
                )
    require(set(seen) == set(range(1, 253)), "physical ids do not cover 1..252")
    anchors = {
        172: (3, 5, 0, 0),
        174: (3, 5, 0, 2),
        244: (6, 7, 0, 0),
        245: (6, 7, 0, 1),
    }
    require(
        all(decode_physical_id(identifier) == value for identifier, value in anchors.items()),
        "degree-six identity anchor numbering mismatch",
    )
    return {"entries": len(seen), "anchor_decodings": anchors}


def validate_matching_cover() -> tuple[tuple[Matching, ...], dict[str, int]]:
    recursive = bitmask_matchings((1 << 8) - 1)
    recursive_set = frozenset(tuple(sorted(matching)) for matching in recursive)
    permutation_set = permutation_matchings()
    require(len(recursive) == 105, "bitmask recursion did not produce 7!!=105")
    require(len(recursive_set) == len(recursive), "bitmask recursion duplicated a matching")
    require(permutation_set == recursive_set, "independent matching enumerations differ")
    for matching in recursive:
        flattened = [vertex for edge in matching for vertex in edge]
        require(sorted(flattened) == list(VERTICES), "invalid perfect matching")
    return recursive, {
        "bitmask_recursive": len(recursive),
        "permutation_quotient": len(permutation_set),
        "expected_seven_double_factorial": 105,
    }


def validate_fixture(payload: dict[str, object], expected: Pattern) -> None:
    require(payload.get("schema") == "eight-vertex-two-edge-surplus-shore-v1", "bad fixture schema")
    require(payload.get("n") == 8, "fixture order differs")
    require(payload.get("field") == "any field", "fixture field scope differs")
    require(tuple(payload.get("shore", ())) == SHORE, "fixture shore differs")
    require(
        tuple(map(tuple, payload.get("covering_edges", ()))) == expected.covering_edges,
        "fixture covering edges differ",
    )
    require(payload.get("base_colour") == BASE_COLOUR, "fixture base colour differs")
    require(
        tuple(payload.get("moving_vertices", ())) == MOVING_VERTICES,
        "fixture moving vertices differ",
    )
    require(
        tuple(payload.get("alternate_colours", ())) == expected.alternate_colours,
        "fixture alternate colours differ",
    )
    require(
        tuple(payload.get("zero_entry_ids", ())) == expected.zero_entry_ids,
        "fixture zero guard differs from independent face construction",
    )
    require(
        tuple(payload.get("nonzero_entry_ids", ())) == expected.nonzero_entry_ids,
        "fixture nonzero guard differs from alternate selected-edge entries",
    )
    require(
        tuple(payload.get("target_monomial", ())) == expected.target_monomial,
        "fixture target monomial differs",
    )
    actual_sources = tuple(
        Source(
            str(row["word"]),
            tuple(row["multiplier"]),
            int(row["coefficient"]),
        )
        for row in payload.get("sources", ())
    )
    require(actual_sources == expected.sources, "fixture source certificate differs")
    require(
        payload.get("equation_convention")
        == "P_word=T_W(word)-1 for pure words, T_W(word) otherwise",
        "fixture source/target convention differs",
    )
    require(payload.get("uses_boundary_relation") is False, "unexpected rho dependence")
    require(
        payload.get("requires_nonzero_proper_cofactor") is False,
        "unexpected proper-cofactor nonzero premise",
    )


def audit_pattern(pattern: Pattern, matchings: tuple[Matching, ...]) -> dict[str, object]:
    guard = frozenset(pattern.zero_entry_ids)
    require(len(guard) == 15, f"{pattern.name}: zero guard is not 15 entries")
    require(
        guard.isdisjoint(pattern.nonzero_entry_ids),
        f"{pattern.name}: zero/nonzero guards overlap",
    )
    require(
        pattern.target_monomial == tuple(sorted(pattern.nonzero_entry_ids)),
        f"{pattern.name}: nonzero guards do not certify the target monomial",
    )

    term_counts = {}
    contribution_groups: dict[Monomial, list[int]] = {}
    for source in pattern.sources:
        hafnian = hafnian_polynomial(source.word, guard, matchings)
        term_counts[source.word] = len(hafnian)
        for matching in matchings:
            monomial = matching_monomial(matching, source.word)
            if not guard.isdisjoint(monomial):
                continue
            require(
                any(edge in matching for edge in pattern.covering_edges),
                f"{pattern.name}: a surviving matching avoids both covering edges",
            )
            degree_six = tuple(sorted(source.multiplier + monomial))
            contribution_groups.setdefault(degree_six, []).append(-source.coefficient)

    expected_terms = (
        15
        if set(pattern.covering_edges[0]).isdisjoint(pattern.covering_edges[1])
        else 12
    )
    require(
        set(term_counts.values()) == {expected_terms},
        f"{pattern.name}: complete source term count differs",
    )
    require(
        all(sum(coefficients) == 0 for coefficients in contribution_groups.values()),
        f"{pattern.name}: termwise degree-six cancellation failed",
    )

    exact_residual = identity_residual(pattern, matchings)
    require(not exact_residual, f"{pattern.name}: exact polynomial identity failed")

    wrong_signs = list(source.coefficient for source in pattern.sources)
    wrong_signs[0] *= -1
    wrong_sign_residual = identity_residual(
        pattern,
        matchings,
        source_coefficients=tuple(wrong_signs),
    )
    require(wrong_sign_residual, f"{pattern.name}: wrong-sign mutation escaped")

    omitted_residual = identity_residual(pattern, matchings, omitted_source=0)
    require(omitted_residual, f"{pattern.name}: omitted-source mutation escaped")

    dropped_target_residual = identity_residual(
        pattern,
        matchings,
        include_pure_target=False,
    )
    require(
        dropped_target_residual == Counter({pattern.target_monomial: 1}),
        f"{pattern.name}: dropped pure target did not expose the target monomial",
    )

    relaxed_guards = {}
    for identifier in pattern.zero_entry_ids:
        residual = identity_residual(
            pattern,
            matchings,
            zero_guard=guard - {identifier},
        )
        require(residual, f"{pattern.name}: guard {identifier} was not necessary")
        relaxed_guards[str(identifier)] = polynomial_summary(residual)

    base_entries = tuple(
        sorted(
            set(pattern.sources[0].multiplier)
        )
    )
    require(
        base_entries == pattern.sources[0].multiplier,
        f"{pattern.name}: base multiplier malformed",
    )
    base_specializations = {}
    for label, forced in (
        ("first_base_zero", frozenset((base_entries[0],))),
        ("second_base_zero", frozenset((base_entries[1],))),
        ("both_base_zero", frozenset(base_entries)),
    ):
        residual = identity_residual(pattern, matchings, forced_zeros=forced)
        require(not residual, f"{pattern.name}: base-entry boundary failed")
        base_specializations[label] = sorted(forced)

    nonzero_premise_controls = {}
    for identifier in pattern.nonzero_entry_ids:
        specialized = identity_residual(
            pattern,
            matchings,
            forced_zeros=frozenset((identifier,)),
        )
        require(not specialized, f"{pattern.name}: alternate-zero identity failed")
        target_after_specialization = normalized(
            [] if identifier in pattern.target_monomial else [(pattern.target_monomial, 1)]
        )
        require(
            not target_after_specialization,
            f"{pattern.name}: removed nonzero premise still leaves target nonzero",
        )
        nonzero_premise_controls[str(identifier)] = {
            "identity_residual": polynomial_summary(specialized),
            "target_monomial_after_specialization": polynomial_summary(
                target_after_specialization
            ),
        }

    group_size_histogram = Counter(len(values) for values in contribution_groups.values())
    return {
        "name": pattern.name,
        "covering_edges": pattern.covering_edges,
        "alternate_colours": pattern.alternate_colours,
        "zero_entry_ids": pattern.zero_entry_ids,
        "nonzero_entry_ids": pattern.nonzero_entry_ids,
        "base_entry_ids": base_entries,
        "source_term_counts": term_counts,
        "degree_six_contributions": sum(map(len, contribution_groups.values())),
        "degree_six_monomial_groups": len(contribution_groups),
        "cancellation_group_size_histogram": dict(sorted(group_size_histogram.items())),
        "every_surviving_matching_uses_a_covering_edge": True,
        "zero_guard_inclusion_minimal_with_other_entries_free": True,
        "exact_residual": polynomial_summary(exact_residual),
        "rho_reduction_used": False,
        "mutations": {
            "wrong_first_source_sign": polynomial_summary(wrong_sign_residual),
            "omitted_first_source": polynomial_summary(omitted_residual),
            "dropped_pure_target": polynomial_summary(dropped_target_residual),
            "each_deleted_zero_guard": relaxed_guards,
            "removed_nonzero_premises": nonzero_premise_controls,
        },
        "admitted_base_entry_boundaries": base_specializations,
    }


def audit_fixed_support(
    payload: dict[str, object],
    seed: Pattern,
    matchings: tuple[Matching, ...],
) -> dict[str, object]:
    require(payload.get("schema") == "recursive-physical-parent-survivor-v1", "bad support schema")
    require(payload.get("n") == 8, "support order differs")
    live = frozenset(map(int, payload.get("nonzero_entry_ids", ())))
    require(len(live) == 134, "fixed support does not contain 134 live ids")
    require(
        frozenset(seed.zero_entry_ids).isdisjoint(live),
        "fixed support violates a seed zero guard",
    )
    require(
        set(seed.nonzero_entry_ids) <= live,
        "fixed support lacks a seed nonzero guard",
    )
    support_zeros = frozenset(range(1, 253)) - live
    residual = identity_residual(seed, matchings, zero_guard=support_zeros)
    require(not residual, "identity failed after specialization to fixed support")
    term_counts = {
        source.word: len(hafnian_polynomial(source.word, support_zeros, matchings))
        for source in seed.sources
    }
    require(
        tuple(term_counts.values()) == (4, 4, 5, 5),
        "fixed-support source term counts differ from independent reconstruction",
    )
    return {
        "live_entry_ids": len(live),
        "source_term_counts": term_counts,
        "identity_residual": polynomial_summary(residual),
        "nonzero_target_factors_live": sorted(seed.nonzero_entry_ids),
        "physical_support_excluded_by_source_equations": True,
        "weight_realization_claimed": False,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return f"<external>/{resolved.name}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--support", type=Path, default=DEFAULT_SUPPORT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    fixture_payload = json.loads(args.fixture.read_text(encoding="utf-8"))
    support_payload = json.loads(args.support.read_text(encoding="utf-8"))
    seed = generate_pattern("disjoint", (2, 1))
    validate_fixture(fixture_payload, seed)
    require(
        sha256(args.support) == EXPECTED_SUPPORT_SHA256,
        "fixed support bytes differ from the pinned 134-entry fixture",
    )

    numbering = validate_numbering()
    matchings, matching_counts = validate_matching_cover()
    patterns = tuple(
        generate_pattern(arrangement, colours)
        for arrangement in ("disjoint", "adjacent")
        for colours in ((2, 1), (1, 1))
    )
    pattern_results = [audit_pattern(pattern, matchings) for pattern in patterns]
    fixed_support = audit_fixed_support(support_payload, seed, matchings)

    result = {
        "schema": "eight-vertex-degree6-source-independent-audit-v1",
        "status": "PASS",
        "scope": (
            "four exact order-eight two-edge surplus-shore pattern types; "
            "not a global theorem"
        ),
        "fixture": portable_path(args.fixture),
        "fixture_sha256": sha256(args.fixture),
        "support_fixture": portable_path(args.support),
        "support_sha256": sha256(args.support),
        "physical_numbering": numbering,
        "perfect_matchings": matching_counts,
        "patterns": pattern_results,
        "fixed_134_support": fixed_support,
        "mathematical_conclusion": (
            "For each pattern, vanishing of the four P_word sources forces the "
            "product of the two alternate selected-edge entries to vanish. "
            "Their declared nonzero premises therefore exclude the fixed support "
            "for the seed pattern."
        ),
        "proof_route": (
            "A perfect matching of five shore vertices and three outside vertices "
            "uses a shore edge. The zero guard leaves only the two selected shore "
            "edges. A matching containing either selected edge cancels with the "
            "same matching in the opposite face source after cross multiplication."
        ),
        "global_krenn_gu_status": "UNRESOLVED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(
        json.dumps(
            {
                "schema": "eight-vertex-degree6-source-independent-audit-v1",
                "status": "PASS",
                "patterns": len(pattern_results),
                "perfect_matchings": matching_counts["bitmask_recursive"],
                "fixed_134_support_excluded": fixed_support[
                    "physical_support_excluded_by_source_equations"
                ],
                "rho_reduction_used": False,
                "global_krenn_gu_status": "UNRESOLVED",
                "full_result": portable_path(args.output) if args.output else None,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
