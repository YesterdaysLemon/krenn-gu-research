"""Independent audit of the order-eight two-slice transfer identities.

The audit generates the four canonical (z,t) in {0,1}^2 patterns from the
mathematical face data.  It uses the separate standard-library polynomial and
matching implementation in ``audit_eight_vertex_degree6_source_134.py`` and
does not import the primary certificate generator or verifier.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE = REPO_ROOT / "tests/fixtures/eight_vertex_two_slice_transfer.json"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_eight_vertex_degree6_source_134 import (  # noqa: E402
    Matching,
    Monomial,
    Polynomial,
    add_scaled,
    hafnian_polynomial,
    physical_id,
    polynomial_summary,
    portable_path,
    require,
    sha256,
    source_polynomial,
    validate_matching_cover,
)


BASE_COLOUR = 2
MOVING_COLOUR = 0
BULK = (1, 2, 3, 4)


@dataclass(frozen=True)
class Source:
    word: str
    multiplier: Monomial
    coefficient: int  # coefficient in target = sum coefficient*multiplier*P


@dataclass(frozen=True)
class TransferPattern:
    name: str
    z: int
    t: int
    zero_entry_ids: tuple[int, ...]
    nonzero_entry_ids: tuple[int, int]
    target_monomial: Monomial
    sources: tuple[Source, ...]


def word(a: int, slice_colour: int, d: int) -> str:
    values = [BASE_COLOUR] * 8
    values[0] = a
    values[6] = slice_colour
    values[7] = d
    return "".join(map(str, values))


def make_pattern(z: int, t: int) -> TransferPattern:
    require(z in {0, 1} and t in {0, 1}, "z and t must be nonbase colours")

    zero_ids = set()
    for vertex in BULK:
        zero_ids.add(physical_id(vertex, 5, 2, 2))
        zero_ids.add(physical_id(vertex, 6, 2, t))
        zero_ids.add(physical_id(vertex, 7, 2, z))
        zero_ids.add(physical_id(vertex, 7, 2, 2))
    zero_ids.add(physical_id(5, 6, 2, t))
    zero_ids.add(physical_id(5, 6, 2, 2))

    a_x = physical_id(0, 5, MOVING_COLOUR, 2)
    a_2 = physical_id(0, 5, 2, 2)
    b_x = physical_id(0, 6, MOVING_COLOUR, t)
    b_2 = physical_id(0, 6, 2, t)
    c_z = physical_id(5, 7, 2, z)
    c_2 = physical_id(5, 7, 2, 2)
    d_z = physical_id(6, 7, 2, z)
    d_2 = physical_id(6, 7, 2, 2)

    sources = (
        Source(word(2, t, 2), tuple(sorted((a_x, d_z))), +1),
        Source(word(2, t, z), tuple(sorted((a_x, d_2))), -1),
        Source(word(MOVING_COLOUR, t, 2), tuple(sorted((a_2, d_z))), -1),
        Source(word(MOVING_COLOUR, t, z), tuple(sorted((a_2, d_2))), +1),
        Source(word(2, 2, 2), tuple(sorted((b_x, c_z))), -1),
        Source(word(2, 2, z), tuple(sorted((b_x, c_2))), +1),
        Source(word(MOVING_COLOUR, 2, 2), tuple(sorted((b_2, c_z))), +1),
        Source(word(MOVING_COLOUR, 2, z), tuple(sorted((b_2, c_2))), -1),
    )
    target = tuple(sorted((b_x, c_z)))
    return TransferPattern(
        name=f"two_slice_z{z}_t{t}",
        z=z,
        t=t,
        zero_entry_ids=tuple(sorted(zero_ids)),
        nonzero_entry_ids=(b_x, c_z),
        target_monomial=target,
        sources=sources,
    )


def matching_monomial(matching: Matching, source_word: str) -> Monomial:
    return tuple(
        sorted(
            physical_id(u, v, int(source_word[u]), int(source_word[v]))
            for u, v in matching
        )
    )


def identity_residual(
    pattern: TransferPattern,
    matchings: tuple[Matching, ...],
    *,
    guard: frozenset[int] | None = None,
    forced_zeros: frozenset[int] = frozenset(),
    source_coefficients: tuple[int, ...] | None = None,
    omitted_source: int | None = None,
    include_pure_target: bool = True,
) -> Polynomial:
    zero_ids = (
        frozenset(pattern.zero_entry_ids) if guard is None else guard
    ) | forced_zeros
    result: Polynomial = Counter()
    if forced_zeros.isdisjoint(pattern.target_monomial):
        result[pattern.target_monomial] = -1
    coefficients = source_coefficients or tuple(
        source.coefficient for source in pattern.sources
    )
    for index, (source, coefficient) in enumerate(
        zip(pattern.sources, coefficients)
    ):
        if index == omitted_source or not forced_zeros.isdisjoint(source.multiplier):
            continue
        polynomial = source_polynomial(
            source.word,
            zero_ids,
            matchings,
            include_pure_target=include_pure_target,
        )
        add_scaled(result, polynomial, coefficient, source.multiplier)
    return result


def validate_fixture(payload: dict[str, object], expected: TransferPattern) -> None:
    require(
        payload.get("schema") == "eight-vertex-physical-degree6-identity-v1",
        "bad two-slice fixture schema",
    )
    require(payload.get("n") == 8, "two-slice fixture order differs")
    require(payload.get("field") == "any field", "two-slice field scope differs")
    require(
        payload.get("family") == "two-slice-shared-cofactor-transfer",
        "two-slice family label differs",
    )
    expected_parameters = {
        "base_colour": BASE_COLOUR,
        "x_colour": MOVING_COLOUR,
        "z_colour": expected.z,
        "first_slice_colour": expected.t,
        "boundary_vertices": [0, 5, 6, 7],
        "bulk_vertices": list(BULK),
    }
    require(
        payload.get("parameters") == expected_parameters,
        "two-slice fixture parameters differ",
    )
    require(
        tuple(payload.get("zero_entry_ids", ())) == expected.zero_entry_ids,
        "fixture zero guard differs from independent construction",
    )
    require(
        tuple(payload.get("nonzero_entry_ids", ())) == expected.nonzero_entry_ids,
        "fixture nonzero premises differ from independent construction",
    )
    require(
        tuple(payload.get("target_monomial", ())) == expected.target_monomial,
        "fixture target differs from independent construction",
    )
    actual_sources = tuple(
        Source(
            word=str(row["word"]),
            multiplier=tuple(row["multiplier"]),
            coefficient=int(row["coefficient"]),
        )
        for row in payload.get("sources", ())
    )
    require(actual_sources == expected.sources, "fixture sources differ")
    a_entries = {
        str(a): physical_id(0, 5, a, BASE_COLOUR)
        for a in (MOVING_COLOUR, BASE_COLOUR)
    }
    b_entries = {
        str(a): physical_id(0, 6, a, expected.t)
        for a in (MOVING_COLOUR, BASE_COLOUR)
    }
    c_entries = {
        str(d): physical_id(5, 7, BASE_COLOUR, d)
        for d in (expected.z, BASE_COLOUR)
    }
    d_entries = {
        str(d): physical_id(6, 7, BASE_COLOUR, d)
        for d in (expected.z, BASE_COLOUR)
    }
    expected_families = {
        "A_a": "W05[a,2]",
        "B_a": f"W06[a,{expected.t}]",
        "C_d": "W57[2,d]",
        "D_d": "W67[2,d]",
        "A": a_entries,
        "B": b_entries,
        "C": c_entries,
        "D": d_entries,
    }
    require(
        payload.get("entry_families") == expected_families,
        "fixture entry-family numbering differs",
    )
    require(
        payload.get("equation_convention")
        == "P_word=T_W(word)-1 for pure words, T_W(word) otherwise",
        "fixture equation convention differs",
    )
    require(
        payload.get("identity")
        == "sum(source.coefficient * source.multiplier * P_word) = B_x*C_z",
        "fixture identity text differs",
    )
    require(payload.get("uses_boundary_relation") is False, "unexpected rho use")
    require(
        payload.get("requires_nonzero_proper_cofactor") is False,
        "unexpected proper-cofactor premise",
    )
    require(payload.get("cofactor_divisions") == 0, "unexpected cofactor division")


def audit_pattern(
    pattern: TransferPattern,
    matchings: tuple[Matching, ...],
) -> dict[str, object]:
    guard = frozenset(pattern.zero_entry_ids)
    require(len(guard) == 18, f"{pattern.name}: guard must have 18 entries")
    require(
        guard.isdisjoint(pattern.nonzero_entry_ids),
        f"{pattern.name}: zero/nonzero overlap",
    )
    require(
        pattern.target_monomial == tuple(sorted(pattern.nonzero_entry_ids)),
        f"{pattern.name}: target not certified nonzero",
    )

    term_counts = {}
    contribution_groups: dict[Monomial, list[tuple[int, int, Matching]]] = {}
    for source_index, source in enumerate(pattern.sources):
        hafnian = hafnian_polynomial(source.word, guard, matchings)
        term_counts[source.word] = len(hafnian)
        for matching in matchings:
            monomial = matching_monomial(matching, source.word)
            if not guard.isdisjoint(monomial):
                continue
            degree_six = tuple(sorted(source.multiplier + monomial))
            contribution_groups.setdefault(degree_six, []).append(
                (source_index, source.coefficient, matching)
            )
    require(
        tuple(term_counts.values()) == (6, 6, 6, 6, 18, 18, 18, 18),
        f"{pattern.name}: complete source term counts differ",
    )
    require(
        all(
            len(contributions) == 2
            and sum(item[1] for item in contributions) == 0
            for contributions in contribution_groups.values()
        ),
        f"{pattern.name}: degree-six term pairing failed",
    )

    residual = identity_residual(pattern, matchings)
    require(not residual, f"{pattern.name}: exact direct identity failed")

    wrong_signs = [source.coefficient for source in pattern.sources]
    wrong_signs[0] *= -1
    wrong_sign = identity_residual(
        pattern,
        matchings,
        source_coefficients=tuple(wrong_signs),
    )
    omitted = identity_residual(pattern, matchings, omitted_source=0)
    dropped_pure = identity_residual(
        pattern,
        matchings,
        include_pure_target=False,
    )
    require(wrong_sign, f"{pattern.name}: wrong sign was not detected")
    require(omitted, f"{pattern.name}: omitted source was not detected")
    require(
        dropped_pure == Counter({pattern.target_monomial: -1}),
        f"{pattern.name}: pure-target deletion control differs",
    )

    deleted_guards = {}
    for identifier in pattern.zero_entry_ids:
        changed = identity_residual(
            pattern,
            matchings,
            guard=guard - {identifier},
        )
        require(changed, f"{pattern.name}: guard {identifier} is redundant")
        deleted_guards[str(identifier)] = polynomial_summary(changed)

    removed_nonzeros = {}
    for identifier in pattern.nonzero_entry_ids:
        specialized = identity_residual(
            pattern,
            matchings,
            forced_zeros=frozenset((identifier,)),
        )
        require(not specialized, f"{pattern.name}: nonzero specialization failed")
        removed_nonzeros[str(identifier)] = {
            "identity_residual": polynomial_summary(specialized),
            "target_product_is_zero": True,
        }

    source_pair_histogram = Counter(
        tuple(item[0] for item in contributions)
        for contributions in contribution_groups.values()
    )
    return {
        "name": pattern.name,
        "z": pattern.z,
        "t": pattern.t,
        "zero_entry_ids": pattern.zero_entry_ids,
        "nonzero_entry_ids": pattern.nonzero_entry_ids,
        "target_monomial": pattern.target_monomial,
        "source_term_counts": term_counts,
        "degree_six_contributions": sum(map(len, contribution_groups.values())),
        "degree_six_monomial_pairs": len(contribution_groups),
        "source_pair_histogram": {
            ",".join(map(str, pair)): count
            for pair, count in sorted(source_pair_histogram.items())
        },
        "exact_residual": polynomial_summary(residual),
        "rho_reduction_used": False,
        "all_other_entries_are_free_indeterminates": True,
        "zero_guard_inclusion_minimal_with_other_entries_free": True,
        "mutations": {
            "wrong_first_source_sign": polynomial_summary(wrong_sign),
            "omitted_first_source": polynomial_summary(omitted),
            "dropped_pure_target": polynomial_summary(dropped_pure),
            "each_deleted_zero_guard": deleted_guards,
            "removed_nonzero_premises": removed_nonzeros,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    matchings, matching_counts = validate_matching_cover()
    patterns = tuple(make_pattern(z, t) for z in (0, 1) for t in (0, 1))
    fixture_path = args.fixture
    if fixture_path is None and DEFAULT_FIXTURE.is_file():
        fixture_path = DEFAULT_FIXTURE
    if fixture_path is not None:
        fixture_payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        parameters = fixture_payload.get("parameters", {})
        require(isinstance(parameters, dict), "fixture parameters must be an object")
        fixture_z = int(parameters.get("z_colour", 0))
        fixture_t = int(parameters.get("first_slice_colour", 1))
        expected = next(
            pattern
            for pattern in patterns
            if pattern.z == fixture_z and pattern.t == fixture_t
        )
        validate_fixture(fixture_payload, expected)

    pattern_results = [audit_pattern(pattern, matchings) for pattern in patterns]
    result = {
        "schema": "eight-vertex-two-slice-transfer-independent-audit-v1",
        "status": "PASS",
        "scope": "four exact order-eight (z,t) two-slice transfer types",
        "fixture": portable_path(fixture_path) if fixture_path else None,
        "fixture_sha256": sha256(fixture_path) if fixture_path else None,
        "perfect_matchings": matching_counts,
        "patterns": pattern_results,
        "proof_structure": (
            "The 18 guards isolate the transfer between the first slice at "
            "vertex 6 colour t and the base slice at colour 2. Exact monomial "
            "pairing cancels all 96 degree-six contributions. The pure base row "
            "leaves the target product B_x*C_z, whose two factors are declared "
            "nonzero."
        ),
        "global_krenn_gu_status": "UNRESOLVED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(
        json.dumps(
            {
                "schema": result["schema"],
                "status": "PASS",
                "patterns": len(pattern_results),
                "perfect_matchings": matching_counts["bitmask_recursive"],
                "guard_size": 18,
                "rho_reduction_used": False,
                "full_result": portable_path(args.output) if args.output else None,
                "global_krenn_gu_status": "UNRESOLVED",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
