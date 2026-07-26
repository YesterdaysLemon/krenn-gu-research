"""Build transferable simple factor-fork rules for the C4+C4+C6 family.

Each exact sample certificate uses a full-only eight-term product equation.
One of its three even-cycle binomials must vanish.  For each alternative,
a second colouring keeps that cycle's local colours fixed and has precisely
the same eight full-only terms plus one supported monomial.  The latter
cannot vanish.

The argument depends only on which singleton edges activate in the few
certificate colourings.  This script converts every validated sample fork
into bitset replacement rules, optionally applies automorphisms of the
fixed full factor, and measures their coverage over either the 93
deterministic samples or the complete ordered factor-prefix census.
"""

from __future__ import annotations

import argparse
import itertools
import json
import pickle
import time
from pathlib import Path
from typing import Iterable, Sequence

N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
CYCLES = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11, 12, 13),
)


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[position], cycle[(position + 1) % len(cycle)])
        for position in range(len(cycle))
    )


FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)
ELIGIBLE_EDGES = tuple(
    item
    for item in itertools.combinations(range(N), 2)
    if item not in FULL_EDGES
)
ELIGIBLE_EDGE_ID = {
    item: position for position, item in enumerate(ELIGIBLE_EDGES)
}


def perfect_matchings(allowed: Iterable[Edge]) -> list[Factor]:
    allowed_set = set(allowed)
    adjacency = [0] * N
    for first, second in allowed_set:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output: list[Factor] = []

    def visit(remaining: int, chosen: Factor) -> None:
        if remaining == 0:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << N) - 1, ())
    return sorted(output)


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*map(int, item)) for item in raw))


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


def colouring_index(colouring: Sequence[int]) -> int:
    return sum(
        int(colour) * (3**vertex)
        for vertex, colour in enumerate(colouring)
    )


def active_mask(
    factor: Factor,
    colour: int,
    colouring: Sequence[int],
) -> int:
    return sum(
        1 << ELIGIBLE_EDGE_ID[item]
        for item in factor
        if colouring[item[0]] == colouring[item[1]] == colour
    )


def factor_mask(factor: Factor) -> int:
    return sum(1 << ELIGIBLE_EDGE_ID[item] for item in factor)


def full_automorphisms() -> list[tuple[int, ...]]:
    component_maps = (
        (0, 1, 2),
        (1, 0, 2),
    )
    local_choices = list(
        itertools.product(
            *[
                [
                    (direction, rotation)
                    for direction in (1, -1)
                    for rotation in range(len(cycle))
                ]
                for cycle in CYCLES
            ]
        )
    )
    output = []
    for component_map in component_maps:
        for choices in local_choices:
            action = [0] * N
            for source_id, source in enumerate(CYCLES):
                target = CYCLES[component_map[source_id]]
                direction, rotation = choices[source_id]
                for position, vertex in enumerate(source):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            output.append(tuple(action))
    return output


def transform_factor(
    factor: Factor, action: Sequence[int]
) -> Factor:
    return tuple(
        sorted(
            edge(action[first], action[second])
            for first, second in factor
        )
    )


def transform_colouring(
    colouring: Sequence[int],
    action: Sequence[int],
    colour_permutation: Sequence[int],
) -> tuple[int, ...]:
    output = [0] * N
    for old_vertex, old_colour in enumerate(colouring):
        output[action[old_vertex]] = colour_permutation[old_colour]
    return tuple(output)


def active_matching_ids(
    matchings: Sequence[Factor],
    factors: Sequence[Factor],
    colouring: Sequence[int],
) -> tuple[int, ...]:
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    active_edges = set(FULL_EDGES)
    active_edges.update(
        item
        for item, colour in labels.items()
        if colouring[item[0]] == colouring[item[1]] == colour
    )
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in active_edges for item in matching)
    )


def validate_simple_certificate(
    analysis: dict[str, object],
) -> tuple[
    tuple[Factor, Factor, Factor],
    tuple[tuple[int, ...], ...],
]:
    if analysis.get("status") != "even_cycle_factor_fork":
        raise AssertionError("analysis is not a simple factor fork")
    factors = tuple(
        parse_factor(analysis["singleton_matchings"][key])
        for key in ("first", "second", "third")
    )
    if len(set().union(*map(set, factors))) != 3 * (N // 2):
        raise AssertionError("source singleton factors overlap")
    matchings = perfect_matchings(
        set(FULL_EDGES) | set().union(*map(set, factors))
    )
    full_only = tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in FULL_EDGES for item in matching)
    )
    if len(full_only) != 8:
        raise AssertionError("source full-factor product changed")
    certificate = analysis["certificate"]
    base = indexed_colouring(
        int(certificate["base_equation_index"])
    )
    base_activity = active_matching_ids(matchings, factors, base)
    if (
        base_activity
        != tuple(map(int, certificate["base_activity"]))
        or base_activity != full_only
        or len(set(base)) == 1
    ):
        raise AssertionError("simple fork base activity changed")
    alternatives = certificate["alternatives"]
    if {
        tuple(map(int, row["cycle"])) for row in alternatives
    } != set(CYCLES):
        raise AssertionError("simple fork misses a cycle alternative")
    colourings = [base]
    for row in alternatives:
        cycle = tuple(map(int, row["cycle"]))
        target = indexed_colouring(
            int(row["target_equation_index"])
        )
        if any(target[vertex] != base[vertex] for vertex in cycle):
            raise AssertionError("cycle colours do not transport")
        activity = active_matching_ids(matchings, factors, target)
        if (
            activity != tuple(map(int, row["target_activity"]))
            or len(activity) != 9
            or set(full_only) - set(activity)
            or int(row["surviving_matching"]) not in activity
            or int(row["surviving_matching"]) in full_only
            or len(set(target)) == 1
        ):
            raise AssertionError("simple fork target activity changed")
        colourings.append(target)
    return factors, tuple(colourings)


def certificate_equations(item: object) -> set[int]:
    output: set[int] = set()
    if isinstance(item, dict):
        for key, value in item.items():
            if key.endswith("equation_index") and isinstance(
                value, int
            ):
                output.add(int(value))
            else:
                output.update(certificate_equations(value))
    elif isinstance(item, list):
        for value in item:
            output.update(certificate_equations(value))
    return output


def component_pattern(factor: Factor) -> int:
    component = {
        vertex: component_id
        for component_id, cycle in enumerate(CYCLES)
        for vertex in cycle
    }
    pairs = ((0, 1), (0, 2), (1, 2))
    pair_id = {pair: position for position, pair in enumerate(pairs)}
    output = 0
    for first, second in factor:
        pair = tuple(sorted((component[first], component[second])))
        if pair[0] != pair[1]:
            output |= 1 << pair_id[pair]
    return output


def connected_pattern(pattern: int) -> bool:
    reached = {0}
    pairs = ((0, 1), (0, 2), (1, 2))
    changed = True
    while changed:
        changed = False
        for position, (first, second) in enumerate(pairs):
            if not pattern & (1 << position):
                continue
            if first in reached and second not in reached:
                reached.add(second)
                changed = True
            elif second in reached and first not in reached:
                reached.add(first)
                changed = True
    return len(reached) == 3


def bit_positions(bits: int):
    while bits:
        item = bits & -bits
        bits ^= item
        yield item.bit_length() - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_support_samples93.json"
        ),
    )
    parser.add_argument(
        "--census",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_factor_orbit_census.json"
        ),
    )
    parser.add_argument(
        "--analysis-pattern",
        default=(
            "tmp/fourteen_vertex_c4_4_6_"
            "sample93_{index}_factor_fork.json"
        ),
    )
    parser.add_argument(
        "--extra-samples",
        type=Path,
        action="append",
        default=[],
        help="optional second support manifest contributing source forks",
    )
    parser.add_argument(
        "--extra-analysis-pattern",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--rich-analysis",
        type=Path,
        action="append",
        default=[],
        help=(
            "verified richer factor-fork analysis contributing an "
            "exact-active-mask transport rule"
        ),
    )
    parser.add_argument(
        "--factor-cegar-analysis",
        type=Path,
        action="append",
        default=[],
        help=(
            "verified forced-slice factor-CEGAR certificate "
            "contributing an exact-active-mask transport rule"
        ),
    )
    parser.add_argument(
        "--probe-samples",
        type=Path,
        action="append",
        default=[],
        help=(
            "optional support manifests tested against the compiled "
            "rules without contributing source certificates"
        ),
    )
    parser.add_argument(
        "--automorphisms",
        action="store_true",
        help="close the rules under all 1,536 full-factor automorphisms",
    )
    parser.add_argument(
        "--stabilizer-only",
        action="store_true",
        help=(
            "with --automorphisms, use only actions stabilizing the "
            "source first factor and colour permutations fixing role 0"
        ),
    )
    parser.add_argument(
        "--full-scan",
        action="store_true",
        help="scan every ordered factor prefix for all 93 first orbits",
    )
    parser.add_argument(
        "--residual-examples-per-orbit",
        type=int,
        default=1,
        help=(
            "retain up to this many residual examples per first-factor "
            "orbit, choosing distinct second factors when possible"
        ),
    )
    parser.add_argument(
        "--compatibility-cache",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_factor_compatibility.pkl"
        ),
        help="reusable exact factor-disjointness bitset cache",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_transport_rule_coverage.json"
        ),
    )
    args = parser.parse_args()
    if args.residual_examples_per_orbit < 1:
        raise ValueError(
            "--residual-examples-per-orbit must be positive"
        )
    samples = json.loads(args.samples.read_text(encoding="utf-8"))
    census = json.loads(args.census.read_text(encoding="utf-8"))
    if (
        samples.get("partition") != [4, 4, 6]
        or census.get("partition") != [4, 4, 6]
    ):
        raise AssertionError("factor partition changed")
    started = time.perf_counter()
    factors = perfect_matchings(ELIGIBLE_EDGES)
    if len(factors) != 44_196:
        raise AssertionError("eligible factor census changed")
    factor_id = {
        factor: position for position, factor in enumerate(factors)
    }
    factor_masks = [factor_mask(factor) for factor in factors]
    all_factor_bits = (1 << len(factors)) - 1
    factor_bits_by_edge = [0] * len(ELIGIBLE_EDGES)
    for position, selected in enumerate(factor_masks):
        factor_bit = 1 << position
        for edge_id in bit_positions(selected):
            factor_bits_by_edge[edge_id] |= factor_bit
    orbit_first_ids = [
        factor_id[parse_factor(row["representative"])]
        for row in census["factor_orbits"]
    ]
    orbit_first_bits = sum(
        1 << first_id for first_id in orbit_first_ids
    )

    source_rows = []
    disconnected_samples = []
    absent_samples = []
    source_statuses: dict[str, dict[str, int]] = {}
    source_sets = [
        ("primary", samples, args.analysis_pattern)
    ]
    if len(args.extra_samples) != len(args.extra_analysis_pattern):
        raise ValueError(
            "each --extra-samples needs one "
            "--extra-analysis-pattern"
        )
    for extra_id, (extra_path, extra_pattern) in enumerate(
        zip(
            args.extra_samples,
            args.extra_analysis_pattern,
            strict=True,
        )
    ):
        extra_samples = json.loads(
            extra_path.read_text(encoding="utf-8")
        )
        if extra_samples.get("partition") != [4, 4, 6]:
            raise AssertionError("extra source partition changed")
        source_sets.append(
            (
                f"extra{extra_id}",
                extra_samples,
                extra_pattern,
            )
        )
    for source_name, manifest, pattern in source_sets:
        statuses: dict[str, int] = {}
        for index in range(len(manifest["survivors"])):
            path = Path(pattern.format(index=index))
            analysis = json.loads(path.read_text(encoding="utf-8"))
            status = str(analysis["status"])
            statuses[status] = statuses.get(status, 0) + 1
            if status == "even_cycle_factor_fork":
                source_factors, source_colourings = (
                    validate_simple_certificate(analysis)
                )
                source_rows.append(
                    (
                        f"{source_name}:{index}",
                        source_factors,
                        source_colourings,
                    )
                )
            elif status == (
                "disconnected_factorization_contradiction"
            ):
                if source_name == "primary":
                    disconnected_samples.append(index)
            elif status == "factor_fork_absent":
                if source_name == "primary":
                    absent_samples.append(index)
            else:
                raise AssertionError(
                    f"unexpected {source_name} status at {index}: "
                    f"{status}"
                )
        source_statuses[source_name] = statuses
    rich_statuses: dict[str, int] = {}
    for rich_id, path in enumerate(args.rich_analysis):
        analysis = json.loads(path.read_text(encoding="utf-8"))
        status = str(analysis["status"])
        rich_statuses[status] = rich_statuses.get(status, 0) + 1
        if status != "even_cycle_double_pair_fork":
            raise AssertionError(
                f"rich analysis is not closed: {path}"
            )
        rich_factors = tuple(
            parse_factor(analysis["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        equations = sorted(
            certificate_equations(analysis["certificate"])
        )
        if not equations:
            raise AssertionError("rich certificate has no equations")
        source_rows.append(
            (
                f"rich:{rich_id}",
                rich_factors,
                tuple(
                    indexed_colouring(equation)
                    for equation in equations
                ),
            )
        )
    factor_cegar_statuses: dict[str, int] = {}
    for cegar_id, path in enumerate(args.factor_cegar_analysis):
        analysis = json.loads(path.read_text(encoding="utf-8"))
        status = str(analysis["status"])
        factor_cegar_statuses[status] = (
            factor_cegar_statuses.get(status, 0) + 1
        )
        if status != "UNSAT":
            raise AssertionError(
                f"factor CEGAR analysis is not closed: {path}"
            )
        cegar_factors = tuple(
            parse_factor(analysis["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        equations = {
            int(value)
            for value in analysis[
                "forcing_base_equations_by_local_code"
            ].values()
        }
        equations.update(
            int(row["equation_index"])
            for row in analysis["factor_clause_origins"]
        )
        equations.update(
            int(row["certificate"]["target_equation_index"])
            for row in analysis["branches"]
            if row["certificate"]["certificate_mode"]
            == "isolated_factor_lattice_class"
        )
        forced_path = Path(analysis["forced_cycle_analysis"])
        forced_analysis = json.loads(
            forced_path.read_text(encoding="utf-8")
        )
        equations.update(
            certificate_equations(
                forced_analysis[
                    "conditional_fork_certificates_by_cycle"
                ]
            )
        )
        source_rows.append(
            (
                f"factor-cegar:{cegar_id}",
                cegar_factors,
                tuple(
                    indexed_colouring(equation)
                    for equation in sorted(
                        equations,
                        key=lambda value: (
                            value * 2_654_435_761
                        )
                        & 0xFFFFFFFF,
                    )
                ),
            )
        )

    actions = (
        full_automorphisms()
        if args.automorphisms
        else [tuple(range(N))]
    )
    colour_permutations = list(itertools.permutations(range(3)))
    active_constraint_cache: dict[tuple[int, int], int] = {}

    def active_factor_bits(
        equation: int, colour: int, expected: int
    ) -> int:
        colouring = indexed_colouring(equation)
        vertex_mask = sum(
            1 << vertex
            for vertex, value in enumerate(colouring)
            if value == colour
        )
        key = (vertex_mask, expected)
        if key in active_constraint_cache:
            return active_constraint_cache[key]
        allowed = all_factor_bits
        for edge_id in bit_positions(expected):
            allowed &= factor_bits_by_edge[edge_id]
        forbidden = 0
        for edge_id, (first, second) in enumerate(ELIGIBLE_EDGES):
            if (
                vertex_mask & (1 << first)
                and vertex_mask & (1 << second)
                and not expected & (1 << edge_id)
            ):
                forbidden |= factor_bits_by_edge[edge_id]
        allowed &= ~forbidden
        active_constraint_cache[key] = allowed
        return allowed

    rules: dict[
        tuple[int, int, int], tuple[str, int, tuple[int, ...]]
    ] = {}
    for source_index, source_factors, source_colourings in source_rows:
        for action_id, action in enumerate(actions):
            if args.stabilizer_only and transform_factor(
                source_factors[0], action
            ) != source_factors[0]:
                continue
            moved_factors = tuple(
                transform_factor(factor, action)
                for factor in source_factors
            )
            moved_colourings = tuple(
                tuple(
                    colouring[
                        next(
                            old
                            for old, new in enumerate(action)
                            if new == vertex
                        )
                    ]
                    for vertex in range(N)
                )
                for colouring in source_colourings
            )
            for colour_permutation in colour_permutations:
                if (
                    args.stabilizer_only
                    and colour_permutation[0] != 0
                ):
                    continue
                transformed_colourings = tuple(
                    transform_colouring(
                        colouring,
                        tuple(range(N)),
                        colour_permutation,
                    )
                    for colouring in moved_colourings
                )
                equations = tuple(
                    colouring_index(colouring)
                    for colouring in transformed_colourings
                )
                allowed_by_new_role = [0, 0, 0]
                viable = True
                for old_role in sorted(
                    range(3),
                    key=lambda role: colour_permutation[role],
                ):
                    new_role = colour_permutation[old_role]
                    allowed = (1 << len(factors)) - 1
                    source_bit = (
                        1 << factor_id[moved_factors[old_role]]
                    )
                    for equation, colouring in zip(
                        equations,
                        transformed_colourings,
                        strict=True,
                    ):
                        expected = active_mask(
                            moved_factors[old_role],
                            new_role,
                            colouring,
                        )
                        allowed &= active_factor_bits(
                            equation, new_role, expected
                        )
                        if allowed == source_bit:
                            break
                    allowed_by_new_role[new_role] = allowed
                    if new_role == 0 and not (
                        allowed & orbit_first_bits
                    ):
                        viable = False
                        break
                if not viable:
                    continue
                for first_id in bit_positions(
                    allowed_by_new_role[0] & orbit_first_bits
                ):
                    rules.setdefault(
                        (
                            first_id,
                            allowed_by_new_role[1],
                            allowed_by_new_role[2],
                        ),
                        (source_index, action_id, equations),
                    )

    sample_rule_closed = []
    for index, row in enumerate(samples["survivors"]):
        ids = tuple(
            factor_id[parse_factor(row[key])]
            for key in ("first", "second", "third")
        )
        if any(
            first_id == ids[0]
            and allowed_second & (1 << ids[1])
            and allowed_third & (1 << ids[2])
            for first_id, allowed_second, allowed_third in rules
        ):
            sample_rule_closed.append(index)
    sample_residuals = sorted(
        set(range(len(samples["survivors"])))
        - set(disconnected_samples)
        - set(sample_rule_closed)
    )
    probe_results = []
    for path in args.probe_samples:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("partition") != [4, 4, 6]:
            raise AssertionError("probe source partition changed")
        closed = []
        for index, row in enumerate(manifest["survivors"]):
            ids = tuple(
                factor_id[parse_factor(row[key])]
                for key in ("first", "second", "third")
            )
            if any(
                first_id == ids[0]
                and allowed_second & (1 << ids[1])
                and allowed_third & (1 << ids[2])
                for first_id, allowed_second, allowed_third in rules
            ):
                closed.append(index)
        probe_results.append(
            {
                "manifest": str(path),
                "samples": len(manifest["survivors"]),
                "rule_closed": closed,
                "residual": sorted(
                    set(range(len(manifest["survivors"])))
                    - set(closed)
                ),
            }
        )

    full_scan_counts = None
    if args.full_scan:
        if args.compatibility_cache.exists():
            with args.compatibility_cache.open("rb") as handle:
                compatibility = pickle.load(handle)
            if (
                not isinstance(compatibility, list)
                or len(compatibility) != len(factors)
                or any(not isinstance(bits, int) for bits in compatibility)
            ):
                raise AssertionError(
                    "factor compatibility cache changed"
                )
        else:
            compatibility = []
            for selected in factor_masks:
                conflict = 0
                for edge_id in bit_positions(selected):
                    conflict |= factor_bits_by_edge[edge_id]
                compatibility.append(all_factor_bits & ~conflict)
            args.compatibility_cache.parent.mkdir(
                parents=True, exist_ok=True
            )
            with args.compatibility_cache.open("wb") as handle:
                pickle.dump(
                    compatibility,
                    handle,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
        patterns = [component_pattern(factor) for factor in factors]
        bits_by_pattern: dict[int, int] = {}
        for position, pattern in enumerate(patterns):
            bits_by_pattern[pattern] = (
                bits_by_pattern.get(pattern, 0)
                | (1 << position)
            )
        connected_bits = {
            prefix: sum(
                bits
                for pattern, bits in bits_by_pattern.items()
                if connected_pattern(prefix | pattern)
            )
            for prefix in range(8)
        }
        totals = {
            "ordered_prefixes": 0,
            "ordered_thirds": 0,
            "disconnected_thirds": 0,
            "simple_rule_closed_connected_thirds": 0,
            "residual_connected_thirds": 0,
        }
        per_orbit = []
        for orbit_id, first_id in enumerate(orbit_first_ids):
            grouped_relevant: dict[int, int] = {}
            for rule_first, second_bits, third_bits in rules:
                if rule_first != first_id:
                    continue
                grouped_relevant[second_bits] = (
                    grouped_relevant.get(second_bits, 0)
                    | third_bits
                )
            closed_by_second: dict[int, int] = {}
            for second_bits, third_bits in grouped_relevant.items():
                for second_id in bit_positions(
                    second_bits & compatibility[first_id]
                ):
                    closed_by_second[second_id] = (
                        closed_by_second.get(second_id, 0)
                        | third_bits
                    )
            orbit_counts = {
                "orbit_id": orbit_id,
                "ordered_prefixes": 0,
                "ordered_thirds": 0,
                "disconnected_thirds": 0,
                "simple_rule_closed_connected_thirds": 0,
                "residual_connected_thirds": 0,
                "residual_example": None,
                "residual_examples": [],
                "specialized_rule_rectangles": len(
                    grouped_relevant
                ),
            }
            for second_id in bit_positions(
                compatibility[first_id]
            ):
                thirds = (
                    compatibility[first_id]
                    & compatibility[second_id]
                )
                connected = thirds & connected_bits[
                    patterns[first_id] | patterns[second_id]
                ]
                disconnected = (
                    thirds.bit_count() - connected.bit_count()
                )
                closed = connected & closed_by_second.get(
                    second_id, 0
                )
                residual = connected & ~closed
                if (
                    residual
                    and len(orbit_counts["residual_examples"])
                    < args.residual_examples_per_orbit
                ):
                    third_id = (
                        residual & -residual
                    ).bit_length() - 1
                    example = {
                        "first": [
                            list(item) for item in factors[first_id]
                        ],
                        "second": [
                            list(item) for item in factors[second_id]
                        ],
                        "third": [
                            list(item) for item in factors[third_id]
                        ],
                    }
                    orbit_counts["residual_examples"].append(example)
                    if orbit_counts["residual_example"] is None:
                        orbit_counts["residual_example"] = example
                orbit_counts["ordered_prefixes"] += 1
                orbit_counts["ordered_thirds"] += thirds.bit_count()
                orbit_counts["disconnected_thirds"] += disconnected
                orbit_counts[
                    "simple_rule_closed_connected_thirds"
                ] += closed.bit_count()
                orbit_counts[
                    "residual_connected_thirds"
                ] += residual.bit_count()
            per_orbit.append(orbit_counts)
            for key in totals:
                totals[key] += orbit_counts[key]
            print(
                f"orbit={orbit_id + 1}/{len(orbit_first_ids)} "
                f"residual="
                f"{orbit_counts['residual_connected_thirds']}",
                flush=True,
            )
        full_scan_counts = {
            **totals,
            "per_orbit": per_orbit,
        }

    payload = {
        "status": "simple_factor_fork_transport_rule_coverage",
        "necessary_conditions_only": True,
        "partition": [4, 4, 6],
        "eligible_factors": len(factors),
        "first_factor_orbits": len(census["factor_orbits"]),
        "simple_source_certificates_replayed": len(source_rows),
        "source_statuses": source_statuses,
        "rich_source_statuses": rich_statuses,
        "factor_cegar_source_statuses": factor_cegar_statuses,
        "disconnected_source_samples": disconnected_samples,
        "factor_fork_absent_source_samples": absent_samples,
        "full_factor_automorphisms_used": len(actions),
        "colour_permutations_used": len(colour_permutations),
        "stabilizer_only": args.stabilizer_only,
        "deduplicated_first_specialized_transport_rules": len(rules),
        "sample_rule_closed": sample_rule_closed,
        "sample_residuals": sample_residuals,
        "probe_results": probe_results,
        "full_scan": full_scan_counts,
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
