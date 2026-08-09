"""Independent replay of the complete C3+C3+C4+C4 equality family.

The verifier independently rebuilds the singleton factors, one-term
matching catalogues, full-factor automorphisms, prefix filters, direct
transport rules, and every compact stable-C4 fork witness.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

N = 14
EQUATIONS = 3**N
CYCLES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8, 9),
    (10, 11, 12, 13),
)
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
ALL_VERTICES = (1 << N) - 1


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)
ELIGIBLE_EDGES = tuple(
    item
    for item in itertools.combinations(range(N), 2)
    if item not in FULL_EDGES
)
EDGE_ID = {
    item: position for position, item in enumerate(ELIGIBLE_EDGES)
}
EDGE_VERTEX_MASK = tuple(
    (1 << first) | (1 << second)
    for first, second in ELIGIBLE_EDGES
)
ALL_GRAPH_EDGES = tuple(itertools.combinations(range(N), 2))
ALL_GRAPH_EDGE_ID = {
    item: position for position, item in enumerate(ALL_GRAPH_EDGES)
}
FULL_ADJACENCY = [0] * N
for _first, _second in FULL_EDGES:
    FULL_ADJACENCY[_first] |= 1 << _second
    FULL_ADJACENCY[_second] |= 1 << _first


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@functools.lru_cache(maxsize=None)
def full_completion(remaining: int) -> int:
    if remaining == 0:
        return 1
    first_bit = remaining & -remaining
    first = first_bit.bit_length() - 1
    candidates = FULL_ADJACENCY[first] & remaining
    total = 0
    while candidates:
        second_bit = candidates & -candidates
        candidates ^= second_bit
        total += full_completion(remaining ^ first_bit ^ second_bit)
    return total


COMPLETION_BY_DELETED = tuple(
    full_completion(ALL_VERTICES ^ deleted)
    for deleted in range(1 << N)
)


def enumerate_matchings(
    allowed: Iterable[Edge],
    vertices: int = ALL_VERTICES,
) -> list[Factor]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first

    @functools.lru_cache(maxsize=None)
    def visit(remaining: int) -> tuple[Factor, ...]:
        if remaining == 0:
            return ((),)
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        output = []
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            for suffix in visit(remaining ^ first_bit ^ second_bit):
                output.append(((first, second),) + suffix)
        return tuple(output)

    return sorted(visit(vertices))


@functools.lru_cache(maxsize=None)
def support_count(item_ids: tuple[int, ...]) -> int:
    total = 0
    for selector in range(1 << len(item_ids)):
        deleted = 0
        for position, item_id in enumerate(item_ids):
            if selector & (1 << position):
                deleted |= EDGE_VERTEX_MASK[item_id]
        total += COMPLETION_BY_DELETED[deleted]
    return total


def factor_mask(factor: Sequence[Edge]) -> int:
    return sum(1 << EDGE_ID[item] for item in factor)


def decode_mask(mask: int) -> tuple[int, ...]:
    return tuple(
        position
        for position in range(len(ELIGIBLE_EDGES))
        if mask & (1 << position)
    )


def matching_id_sets(size: int):
    chosen: list[int] = []

    def visit(start: int, used: int):
        if len(chosen) == size:
            yield tuple(chosen)
            return
        for item_id in range(start, len(ELIGIBLE_EDGES)):
            item_mask = EDGE_VERTEX_MASK[item_id]
            if item_mask & used:
                continue
            chosen.append(item_id)
            yield from visit(item_id + 1, used | item_mask)
            chosen.pop()

    yield from visit(0, 0)


def factor_safe(factor: Factor) -> bool:
    item_ids = tuple(EDGE_ID[item] for item in factor)
    exact = [0] * (1 << len(item_ids))
    for selector in range(1 << len(item_ids)):
        deleted = 0
        for position, item_id in enumerate(item_ids):
            if selector & (1 << position):
                deleted |= EDGE_VERTEX_MASK[item_id]
        exact[selector] = COMPLETION_BY_DELETED[deleted]
    totals = exact[:]
    for bit in range(len(item_ids)):
        for selector in range(1 << len(item_ids)):
            if selector & (1 << bit):
                totals[selector] += totals[selector ^ (1 << bit)]
    return not any(
        totals[selector] == 1
        for selector in range(1, (1 << len(item_ids)) - 1)
    )


def full_automorphisms() -> list[dict[int, int]]:
    component_swaps = [
        {0: first, 1: second, 2: third, 3: fourth}
        for first, second in ((0, 1), (1, 0))
        for third, fourth in ((2, 3), (3, 2))
    ]
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
    actions = []
    for component_map in component_swaps:
        for choices in local_choices:
            action = {}
            for source, cycle in enumerate(CYCLES):
                target = CYCLES[component_map[source]]
                direction, rotation = choices[source]
                for position, vertex in enumerate(cycle):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            actions.append(action)
    return actions


def transform_factor(
    factor: Sequence[Edge], action: dict[int, int]
) -> Factor:
    return tuple(
        sorted(
            edge(action[first], action[second])
            for first, second in factor
        )
    )


def factor_orbits(
    factors: Iterable[Factor], actions: Sequence[dict[int, int]]
) -> list[tuple[Factor, int]]:
    factor_set = set(factors)
    unseen = set(factor_set)
    output = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform_factor(representative, action)
            for action in actions
        } & factor_set
        output.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    return output


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


def active_singleton_mask(
    factor: Factor, colour: int, colouring: Sequence[int]
) -> int:
    return sum(
        1 << EDGE_ID[item]
        for item in factor
        if colouring[item[0]] == colouring[item[1]] == colour
    )


def relation_signature(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
    def variables(matching: Sequence[Edge]) -> list[int]:
        output = []
        for item in matching:
            if item in FULL_EDGES:
                first_colour = int(colouring[item[0]])
                second_colour = int(colouring[item[1]])
            else:
                first_colour = second_colour = labels[item]
            output.append(
                9 * ALL_GRAPH_EDGE_ID[item]
                + 3 * first_colour
                + second_colour
            )
        return output

    vector = Counter(variables(first))
    vector.subtract(variables(second))
    direct = tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in vector.items()
            if coefficient
        )
    )
    negative = tuple(
        (entry, -coefficient) for entry, coefficient in direct
    )
    return min(direct, negative)


def active_support_matchings(
    factors: Sequence[Factor], colouring: Sequence[int]
) -> list[Factor]:
    active_edges = set(FULL_EDGES)
    for colour, factor in enumerate(factors):
        active_edges.update(
            item
            for item in factor
            if colouring[item[0]] == colouring[item[1]] == colour
        )
    return enumerate_matchings(active_edges)


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*map(int, item)) for item in raw))


def validate_direct_transport(
    factors: Sequence[Factor],
    origin_index: int,
    target_index: int,
) -> None:
    origin = indexed_colouring(origin_index)
    target = indexed_colouring(target_index)
    if len(set(origin)) == 1 or len(set(target)) == 1:
        raise AssertionError("direct transport uses a required equation")
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    origin_matchings = active_support_matchings(factors, origin)
    target_matchings = active_support_matchings(factors, target)
    if len(origin_matchings) != 2 or len(target_matchings) != 3:
        raise AssertionError("direct transport activity changed")
    origin_signature = relation_signature(
        origin_matchings[0],
        origin_matchings[1],
        origin,
        labels,
    )
    target_signatures = [
        relation_signature(first, second, target, labels)
        for first, second in itertools.combinations(target_matchings, 2)
    ]
    if origin_signature not in target_signatures:
        raise AssertionError("direct relation does not transport")


def component_connected(factors: Sequence[Factor]) -> bool:
    adjacency = [set() for _vertex in range(N)]
    for first, second in itertools.chain(
        FULL_EDGES, *factors
    ):
        adjacency[first].add(second)
        adjacency[second].add(first)
    reached = {0}
    pending = [0]
    while pending:
        first = pending.pop()
        for second in adjacency[first]:
            if second not in reached:
                reached.add(second)
                pending.append(second)
    return len(reached) == N


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--census",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_3_4_4_factor_orbit_census.json"
        ),
    )
    parser.add_argument(
        "--one-term-catalogue",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_3_4_4_larger_one_term_catalogue.json"
        ),
    )
    parser.add_argument(
        "--pair-filter",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_3_4_4_larger_one_term_pair_filter.json"
        ),
    )
    parser.add_argument(
        "--stable-fork-catalogue",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_3_4_4_two_to_three_forks.json"
        ),
    )
    parser.add_argument(
        "--certificate-shard-pattern",
        default=(
            "tmp/fourteen_vertex_c3_3_4_4_"
            "stable_fork_certificate_shard{shard}.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c3_c4_c4_family_verified.json"
        ),
    )
    args = parser.parse_args()

    census = json.loads(args.census.read_text(encoding="utf-8"))
    one_term_payload = json.loads(
        args.one_term_catalogue.read_text(encoding="utf-8")
    )
    pair_payload = json.loads(
        args.pair_filter.read_text(encoding="utf-8")
    )
    stable_payload = json.loads(
        args.stable_fork_catalogue.read_text(encoding="utf-8")
    )
    if census.get("partition") != [3, 3, 4, 4]:
        raise AssertionError("census partition changed")
    if one_term_payload.get("partition") != [3, 3, 4, 4]:
        raise AssertionError("one-term partition changed")
    if stable_payload.get("partition") != [3, 3, 4, 4]:
        raise AssertionError("stable-fork partition changed")
    for payload in (one_term_payload, stable_payload):
        if tuple(
            edge(*map(int, item)) for item in payload["eligible_edges"]
        ) != ELIGIBLE_EDGES:
            raise AssertionError("eligible-edge ordering changed")

    factors_all = enumerate_matchings(ELIGIBLE_EDGES)
    factors = [factor for factor in factors_all if factor_safe(factor)]
    factor_id = {
        factor: position for position, factor in enumerate(factors)
    }
    if len(factors_all) != 44_262 or len(factors) != 7_974:
        raise AssertionError("singleton-factor census changed")
    actions = full_automorphisms()
    orbits = factor_orbits(factors, actions)
    if len(actions) != 9_216 or len(orbits) != 14:
        raise AssertionError("factor orbit census changed")
    reported_orbits = [
        (
            parse_factor(row["representative"]),
            int(row["orbit_size"]),
        )
        for row in census["factor_orbits"]
    ]
    if orbits != reported_orbits:
        raise AssertionError("reported factor orbits do not replay")

    one_terms: dict[int, set[int]] = {}
    one_term_scan_counts = {}
    for size in range(3, 7):
        rows = set()
        scanned = 0
        for item_ids in matching_id_sets(size):
            scanned += 1
            if support_count(item_ids) == 1:
                rows.add(sum(1 << item_id for item_id in item_ids))
        one_terms[size] = rows
        one_term_scan_counts[size] = scanned
        reported = set(
            map(
                int,
                one_term_payload["one_term_masks_by_size"][
                    str(size)
                ],
            )
        )
        if rows != reported:
            raise AssertionError(
                f"size-{size} one-term catalogue mismatch"
            )
    if {size: len(rows) for size, rows in one_terms.items()} != {
        3: 1_152,
        4: 14_400,
        5: 19_008,
        6: 0,
    }:
        raise AssertionError("one-term counts changed")

    # Lemma: every matching of singleton edges can be activated exactly.
    # Precolour its endpoints by their labels; on the remaining vertices,
    # S1 union S2 is a union of paths/even cycles and is properly
    # 2-colourable.  This makes every catalogued one-term mask a sound
    # contradiction independent of how its edges split among S0,S1,S2.
    if any(
        any(
            EDGE_VERTEX_MASK[first] & EDGE_VERTEX_MASK[second]
            for first, second in itertools.combinations(
                decode_mask(mask), 2
            )
        )
        for rows in one_terms.values()
        for mask in rows
    ):
        raise AssertionError("one-term catalogue contains a nonmatching")

    factor_masks = [factor_mask(factor) for factor in factors]
    size_three = one_terms[3]
    pair_completions: dict[tuple[int, int], int] = {}
    for target in size_three:
        item_ids = decode_mask(target)
        for first, second in itertools.combinations(item_ids, 2):
            third = next(
                item
                for item in item_ids
                if item not in {first, second}
            )
            pair_completions[(first, second)] = (
                pair_completions.get((first, second), 0)
                | (1 << third)
            )

    def completion(selected: int) -> int:
        item_ids = decode_mask(selected)
        output = 0
        for first, second in itertools.combinations(item_ids, 2):
            output |= pair_completions.get((first, second), 0)
        return output

    factor_completions = [
        completion(selected) for selected in factor_masks
    ]
    larger_masks = one_terms[4] | one_terms[5]

    def contains_larger(selected: int) -> bool:
        item_ids = decode_mask(selected)
        for size in (4, 5):
            for subset in itertools.combinations(item_ids, size):
                if (
                    sum(1 << item_id for item_id in subset)
                    in one_terms[size]
                ):
                    return True
        return False

    pair_rows: list[tuple[int, int, int]] = []
    size3_compatible_seconds = 0
    for orbit_id, (first, _orbit_size) in enumerate(orbits):
        first_id = factor_id[first]
        first_mask = factor_masks[first_id]
        first_completion = factor_completions[first_id]
        for second_id, second_mask in enumerate(factor_masks):
            if first_mask & second_mask:
                continue
            if first_completion & second_mask:
                continue
            if factor_completions[second_id] & first_mask:
                continue
            size3_compatible_seconds += 1
            if contains_larger(first_mask | second_mask):
                continue
            pair_rows.append((orbit_id, first_id, second_id))
    if (
        size3_compatible_seconds != 15_922
        or len(pair_rows) != 12_172
    ):
        raise AssertionError("pair filtering counts changed")
    reported_pairs = [
        (
            int(row["orbit_id"]),
            factor_id[parse_factor(row["first"])],
            factor_id[parse_factor(row["second"])],
        )
        for row in pair_payload["pair_survivors"]
    ]
    if pair_rows != reported_pairs:
        raise AssertionError("pair survivor ordering changed")

    # Rebuild and semantically replay the direct transport rule pool.
    motif_batches = [
        (
            Path(
                "tmp/fourteen_vertex_c3_3_4_4_"
                "larger_one_term_full_filter.json"
            ),
            "connected_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "seed0_{index}_all_direct_motifs.json"
            ),
            12,
        ),
        (
            Path("tmp/fourteen_vertex_c3_3_4_4_motif12_filter.json"),
            "motif_residual_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "seed1_{index}_all_direct_motifs.json"
            ),
            10,
        ),
        (
            Path("tmp/fourteen_vertex_c3_3_4_4_motif22_filter.json"),
            "motif_residual_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "cegar2_{index}_all_direct_motifs.json"
            ),
            10,
        ),
        (
            Path("tmp/fourteen_vertex_c3_3_4_4_motif615_filter.json"),
            "motif_residual_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "cegar3_{index}_all_direct_motifs.json"
            ),
            9,
        ),
        (
            Path("tmp/fourteen_vertex_c3_3_4_4_motif1071_filter.json"),
            "motif_residual_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "cegar4_{index}_all_direct_motifs.json"
            ),
            8,
        ),
        (
            Path("tmp/fourteen_vertex_c3_3_4_4_motif1468_filter.json"),
            "motif_residual_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "cegar5_{index}_all_direct_motifs.json"
            ),
            7,
        ),
        (
            Path(
                "tmp/fourteen_vertex_c3_3_4_4_"
                "motif1872_res5_filter.json"
            ),
            "motif_residual_survivors",
            (
                "tmp/fourteen_vertex_c3_3_4_4_"
                "cegar6_{index}_all_direct_motifs.json"
            ),
            35,
        ),
    ]
    motif_rules: list[tuple[int, int, int]] = []
    direct_certificates = 0
    motif_artifacts: list[Path] = []
    for manifest_path, support_key, pattern, count in motif_batches:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        supports = manifest[support_key]
        for index in range(count):
            support = supports[index]
            source_factors = tuple(
                parse_factor(support[key])
                for key in ("first", "second", "third")
            )
            analysis_path = Path(pattern.format(index=index))
            motif_artifacts.append(analysis_path)
            analysis = json.loads(
                analysis_path.read_text(encoding="utf-8")
            )
            certificates = analysis.get("certificates") or [
                analysis["certificate"]
            ]
            for certificate in certificates:
                origin_index = int(
                    certificate["origin_equation_index"]
                )
                target_index = int(
                    certificate["target_equation_index"]
                )
                validate_direct_transport(
                    source_factors, origin_index, target_index
                )
                origin = indexed_colouring(origin_index)
                target = indexed_colouring(target_index)
                allowed_by_role = []
                for colour, source_factor in enumerate(source_factors):
                    required_origin = active_singleton_mask(
                        source_factor, colour, origin
                    )
                    required_target = active_singleton_mask(
                        source_factor, colour, target
                    )
                    allowed = 0
                    for factor_position, factor in enumerate(factors):
                        if (
                            active_singleton_mask(
                                factor, colour, origin
                            )
                            == required_origin
                            and active_singleton_mask(
                                factor, colour, target
                            )
                            == required_target
                        ):
                            allowed |= 1 << factor_position
                    allowed_by_role.append(allowed)
                for permutation in itertools.permutations(range(3)):
                    motif_rules.append(
                        tuple(
                            allowed_by_role[role]
                            for role in permutation
                        )
                    )
                direct_certificates += 1
    motif_rules = list(dict.fromkeys(motif_rules))
    if (
        direct_certificates != 5_039
        or len(motif_rules) != 21_837
    ):
        raise AssertionError("direct motif pool changed")

    # Independently validate every stable fork row.
    stable_rows = []
    stable_semantics: dict[int, tuple[Factor, Factor, Factor]] = {}
    for fork_id, row in enumerate(stable_payload["fork_rows"]):
        sparse_mask = int(row["sparse_mask"])
        rich_mask = int(row["rich_mask"])
        component = int(row["alternating_c4_component"])
        sparse_ids = decode_mask(sparse_mask)
        rich_ids = decode_mask(rich_mask)
        if (
            support_count(sparse_ids) != 2
            or support_count(rich_ids) != 3
            or not set(sparse_ids) < set(rich_ids)
        ):
            raise AssertionError("stable fork matching count changed")
        stable_rows.append(
            (sparse_mask, rich_mask, component)
        )
    if len(stable_rows) != 395_784:
        raise AssertionError("stable fork catalogue count changed")

    certificate_by_ordinal: dict[int, list[int]] = {}
    shard_paths = []
    shard_counts = []
    for shard in range(4):
        path = Path(
            args.certificate_shard_pattern.format(shard=shard)
        )
        shard_paths.append(path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = [
            list(map(int, row))
            for row in payload["stable_fork_certificates"]
        ]
        expected = int(payload["stable_fork_scanned_thirds"])
        if (
            int(payload["stable_fork_closed_thirds"]) != expected
            or int(payload["stable_fork_free_thirds"]) != 0
            or len(rows) != expected
        ):
            raise AssertionError("certificate shard is incomplete")
        for row in rows:
            ordinal = row[0]
            if ordinal % 4 != shard:
                raise AssertionError("certificate is in the wrong shard")
            if ordinal in certificate_by_ordinal:
                raise AssertionError("duplicate stable certificate")
            certificate_by_ordinal[ordinal] = row
        shard_counts.append(expected)

    # Bitset indexes for the complete triple replay.
    factor_bits_by_edge = [0] * len(ELIGIBLE_EDGES)
    completion_bits_by_edge = [0] * len(ELIGIBLE_EDGES)
    for position, (selected, completed) in enumerate(
        zip(factor_masks, factor_completions, strict=True)
    ):
        factor_bit = 1 << position
        for item_id in range(len(ELIGIBLE_EDGES)):
            edge_bit = 1 << item_id
            if selected & edge_bit:
                factor_bits_by_edge[item_id] |= factor_bit
            if completed & edge_bit:
                completion_bits_by_edge[item_id] |= factor_bit

    larger_rows = []
    relevant_remainders = set()
    for target in larger_masks:
        bits = [1 << item_id for item_id in decode_mask(target)]
        for selector in range(1, (1 << len(bits)) - 1):
            base = sum(
                bits[position]
                for position in range(len(bits))
                if selector & (1 << position)
            )
            remainder = target ^ base
            larger_rows.append((base, remainder))
            relevant_remainders.add(remainder)
    factor_superset_bits: dict[int, int] = {}
    for position, selected in enumerate(factor_masks):
        bits = [1 << item_id for item_id in decode_mask(selected)]
        for size in range(1, 5):
            for subset in itertools.combinations(bits, size):
                remainder = sum(subset)
                if remainder in relevant_remainders:
                    factor_superset_bits[remainder] = (
                        factor_superset_bits.get(remainder, 0)
                        | (1 << position)
                    )
    base_forbidden_factor_bits: dict[int, int] = {}
    for base, remainder in larger_rows:
        forbidden = factor_superset_bits.get(remainder, 0)
        if forbidden:
            base_forbidden_factor_bits[base] = (
                base_forbidden_factor_bits.get(base, 0)
                | forbidden
            )

    component_id = {
        vertex: component
        for component, cycle in enumerate(CYCLES)
        for vertex in cycle
    }
    component_pairs = tuple(itertools.combinations(range(4), 2))
    component_pair_id = {
        pair: position for position, pair in enumerate(component_pairs)
    }

    def component_pattern(factor: Factor) -> int:
        output = 0
        for first, second in factor:
            pair = tuple(
                sorted((component_id[first], component_id[second]))
            )
            if pair[0] != pair[1]:
                output |= 1 << component_pair_id[pair]
        return output

    def connected_pattern(pattern: int) -> bool:
        reached = {0}
        changed = True
        while changed:
            changed = False
            for position, (first, second) in enumerate(component_pairs):
                if not pattern & (1 << position):
                    continue
                if first in reached and second not in reached:
                    reached.add(second)
                    changed = True
                elif second in reached and first not in reached:
                    reached.add(first)
                    changed = True
        return len(reached) == 4

    factor_patterns = [component_pattern(factor) for factor in factors]
    factor_bits_by_pattern: dict[int, int] = {}
    for position, pattern in enumerate(factor_patterns):
        factor_bits_by_pattern[pattern] = (
            factor_bits_by_pattern.get(pattern, 0)
            | (1 << position)
        )
    connected_bits = {
        pair_pattern: sum(
            bits
            for pattern, bits in factor_bits_by_pattern.items()
            if connected_pattern(pair_pattern | pattern)
        )
        for pair_pattern in range(1 << len(component_pairs))
    }

    all_factor_bits = (1 << len(factors)) - 1
    counts = Counter()
    candidate_ordinal = 0
    used_fork_ids = set()
    for orbit_id, first_id, second_id in pair_rows:
        selected = factor_masks[first_id] | factor_masks[second_id]
        completed = completion(selected)
        conflict = 0
        selected_ids = decode_mask(selected)
        for item_id in selected_ids:
            conflict |= factor_bits_by_edge[item_id]
            conflict |= completion_bits_by_edge[item_id]
        for item_id in decode_mask(completed):
            conflict |= factor_bits_by_edge[item_id]
        size3_candidates = all_factor_bits & ~conflict
        counts["size3"] += size3_candidates.bit_count()

        larger_conflict = 0
        selected_bits = [1 << item_id for item_id in selected_ids]
        for size in range(1, 5):
            for subset in itertools.combinations(selected_bits, size):
                larger_conflict |= base_forbidden_factor_bits.get(
                    sum(subset), 0
                )
        accepted = size3_candidates & ~larger_conflict
        counts["larger"] += accepted.bit_count()
        connected = accepted & connected_bits[
            factor_patterns[first_id] | factor_patterns[second_id]
        ]
        counts["connected"] += connected.bit_count()
        counts["disconnected"] += (
            accepted.bit_count() - connected.bit_count()
        )

        direct_closed = 0
        first_bit = 1 << first_id
        second_bit = 1 << second_id
        for allowed_first, allowed_second, allowed_third in motif_rules:
            if (
                allowed_first & first_bit
                and allowed_second & second_bit
            ):
                direct_closed |= allowed_third
        residual = connected & ~direct_closed
        counts["direct_residual"] += residual.bit_count()
        while residual:
            third_bit = residual & -residual
            residual ^= third_bit
            third_id = third_bit.bit_length() - 1
            row = certificate_by_ordinal.get(candidate_ordinal)
            if row is None:
                raise AssertionError("missing stable-fork certificate")
            (
                ordinal,
                reported_orbit,
                reported_first,
                reported_second,
                reported_third,
                fork_id,
                c4_code,
                origin_index,
                target_index,
            ) = row
            if (
                ordinal != candidate_ordinal
                or reported_orbit != orbit_id
                or reported_first != first_id
                or reported_second != second_id
                or reported_third != third_id
            ):
                raise AssertionError("stable certificate support mismatch")
            sparse_mask, rich_mask, component = stable_rows[fork_id]
            support_mask = (
                factor_masks[first_id]
                | factor_masks[second_id]
                | factor_masks[third_id]
            )
            if rich_mask & support_mask != rich_mask:
                raise AssertionError("stable fork is not contained")
            support_factors = (
                factors[first_id],
                factors[second_id],
                factors[third_id],
            )
            labels = {
                item: colour
                for colour, factor in enumerate(support_factors)
                for item in factor
            }
            origin = indexed_colouring(origin_index)
            target = indexed_colouring(target_index)
            active_origin = sum(
                1 << EDGE_ID[item]
                for item, colour in labels.items()
                if origin[item[0]] == origin[item[1]] == colour
            )
            active_target = sum(
                1 << EDGE_ID[item]
                for item, colour in labels.items()
                if target[item[0]] == target[item[1]] == colour
            )
            if (
                active_origin != sparse_mask
                or active_target != rich_mask
                or len(set(origin)) == 1
                or len(set(target)) == 1
            ):
                raise AssertionError("stable activation replay failed")
            c4_colours = tuple(
                (c4_code // (3**position)) % 3
                for position in range(4)
            )
            c4_vertices = CYCLES[component]
            if (
                tuple(origin[vertex] for vertex in c4_vertices)
                != c4_colours
                or tuple(target[vertex] for vertex in c4_vertices)
                != c4_colours
            ):
                raise AssertionError("stable C4 colours changed")

            if fork_id not in stable_semantics:
                sparse_edges = {
                    ELIGIBLE_EDGES[item_id]
                    for item_id in decode_mask(sparse_mask)
                }
                rich_edges = {
                    ELIGIBLE_EDGES[item_id]
                    for item_id in decode_mask(rich_mask)
                }
                sparse_matchings = enumerate_matchings(
                    set(FULL_EDGES) | sparse_edges
                )
                rich_matchings = enumerate_matchings(
                    set(FULL_EDGES) | rich_edges
                )
                if (
                    len(sparse_matchings) != 2
                    or len(rich_matchings) != 3
                    or not set(sparse_matchings)
                    < set(rich_matchings)
                    or (
                        set(sparse_matchings[0])
                        ^ set(sparse_matchings[1])
                    )
                    != set(cycle_edges(CYCLES[component]))
                ):
                    raise AssertionError("stable fork semantics changed")
                survivor = next(
                    matching
                    for matching in rich_matchings
                    if matching not in set(sparse_matchings)
                )
                stable_semantics[fork_id] = (
                    sparse_matchings[0],
                    sparse_matchings[1],
                    survivor,
                )
            first_matching, second_matching, _survivor = (
                stable_semantics[fork_id]
            )
            if relation_signature(
                first_matching,
                second_matching,
                origin,
                labels,
            ) != relation_signature(
                first_matching,
                second_matching,
                target,
                labels,
            ):
                raise AssertionError("stable relation does not transport")
            used_fork_ids.add(fork_id)
            candidate_ordinal += 1

    expected_counts = {
        "size3": 2_911_352,
        "larger": 2_863_992,
        "connected": 2_862_996,
        "disconnected": 996,
        "direct_residual": 394_068,
    }
    if dict(counts) != expected_counts:
        raise AssertionError(
            f"triple coverage changed: {dict(counts)}"
        )
    if (
        candidate_ordinal != 394_068
        or len(certificate_by_ordinal) != candidate_ordinal
        or sum(shard_counts) != candidate_ordinal
    ):
        raise AssertionError("stable shard partition is incomplete")

    artifacts = [
        args.census,
        args.one_term_catalogue,
        args.pair_filter,
        args.stable_fork_catalogue,
        *motif_artifacts,
        *shard_paths,
    ]
    artifact_hashes = {
        str(path): sha256(path) for path in artifacts
    }
    payload = {
        "verified": True,
        "status": "all_c3_c3_c4_c4_equality_supports_closed",
        "scope": (
            "no n=14,d=3 equality-architecture witness whose full "
            "factor has cycle type C3+C3+C4+C4"
        ),
        "claim_scope": (
            "complete for C3+C3+C4+C4 equality supports; not the "
            "remaining order-14 factor types or the global conjecture"
        ),
        "full_cycle_type": [3, 3, 4, 4],
        "eligible_singleton_factors": len(factors_all),
        "one_term_free_singleton_factors": len(factors),
        "full_factor_automorphisms": len(actions),
        "safe_factor_orbits": len(orbits),
        "one_term_matching_sets_scanned_by_size": (
            one_term_scan_counts
        ),
        "one_term_matching_counts_by_size": {
            size: len(rows) for size, rows in one_terms.items()
        },
        "exact_activation_lemma": (
            "every singleton-edge matching is exactly activatable by "
            "precolouring its endpoints and properly 2-colouring the "
            "remaining S1-union-S2 paths and even cycles"
        ),
        "pair_survivors": len(pair_rows),
        "size3_compatible_thirds": counts["size3"],
        "larger_one_term_free_thirds": counts["larger"],
        "connected_thirds": counts["connected"],
        "disconnected_factorization_thirds": counts["disconnected"],
        "direct_transport_certificates": direct_certificates,
        "direct_transport_rules": len(motif_rules),
        "stable_fork_candidates": candidate_ordinal,
        "stable_fork_shard_counts": shard_counts,
        "stable_fork_certificates_replayed": candidate_ordinal,
        "distinct_stable_forks_used": len(used_fork_ids),
        "residual_supports": 0,
        "artifact_sha256": artifact_hashes,
    }
    payload["canonical_sha256_without_self"] = canonical_json_sha256(
        payload
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
