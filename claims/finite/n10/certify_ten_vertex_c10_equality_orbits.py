"""Find a direct binomial/trinomial contradiction in every C10 orbit."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import numpy as np

from explore_random_even_cycle_forks import colouring_table, perfect_matchings

Edge = tuple[int, int]
ALL_EDGES = tuple(itertools.combinations(range(10), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}
DISCOVERED_PATTERNS: list[tuple[int, tuple[int, int, int]]] = []


def monomial_entries(
    matching: list[Edge] | tuple[Edge, ...],
    colouring: np.ndarray,
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> list[int]:
    result: list[int] = []
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        result.append(
            9 * EDGE_INDEX[item] + 3 * first_colour + second_colour
        )
    return result


def relation_signature(
    first: list[Edge] | tuple[Edge, ...],
    second: list[Edge] | tuple[Edge, ...],
    colouring: np.ndarray,
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
    vector: Counter[int] = Counter(
        monomial_entries(first, colouring, full_edges, labels)
    )
    vector.subtract(
        monomial_entries(second, colouring, full_edges, labels)
    )
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


def oriented_signature(
    first: list[Edge] | tuple[Edge, ...],
    second: list[Edge] | tuple[Edge, ...],
    colouring: np.ndarray,
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
    vector: Counter[int] = Counter(
        monomial_entries(first, colouring, full_edges, labels)
    )
    vector.subtract(
        monomial_entries(second, colouring, full_edges, labels)
    )
    return tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in vector.items()
            if coefficient
        )
    )


def negate_signature(
    vector: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    return tuple((entry, -coefficient) for entry, coefficient in vector)


def subtract_signatures(
    target: tuple[tuple[int, int], ...],
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    result: Counter[int] = Counter(dict(target))
    result.subtract(dict(first))
    result.subtract(dict(second))
    return tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in result.items()
            if coefficient
        )
    )


def add_signatures(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    result: Counter[int] = Counter(dict(first))
    result.update(dict(second))
    return tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in result.items()
            if coefficient
        )
    )


def direct_certificate(
    full_edges: set[Edge],
    singleton_matchings: list[list[Edge]],
    colourings: np.ndarray,
    transport_prefix: int,
) -> dict[str, object]:
    colourings = colourings[:transport_prefix]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    skeleton = full_edges | set(labels)
    matchings = perfect_matchings(10, skeleton)
    fixed_target = 10
    fixed_origins = (254, 281, 37)

    def activity_for(colouring: np.ndarray) -> tuple[int, ...]:
        return tuple(
            matching_id
            for matching_id, matching in enumerate(matchings)
            if all(
                item in full_edges
                or (
                    colouring[item[0]]
                    == colouring[item[1]]
                    == labels[item]
                )
                for item in matching
            )
        )

    if (
        fixed_target < len(colourings)
        and all(origin < len(colourings) for origin in fixed_origins)
    ):
        target_activity_fixed = activity_for(
            colourings[fixed_target]
        )
        origin_activities_fixed = [
            activity_for(colourings[origin])
            for origin in fixed_origins
        ]
        if (
            len(target_activity_fixed) == 3
            and all(
                len(activity) == 2
                for activity in origin_activities_fixed
            )
            and len(set(origin_activities_fixed)) == 1
        ):
            first, second = origin_activities_fixed[0]
            if (
                first in target_activity_fixed
                and second in target_activity_fixed
            ):
                target_signature_fixed = oriented_signature(
                    matchings[first],
                    matchings[second],
                    colourings[fixed_target],
                    full_edges,
                    labels,
                )
                origin_signatures_fixed = [
                    oriented_signature(
                        matchings[first],
                        matchings[second],
                        colourings[origin],
                        full_edges,
                        labels,
                    )
                    for origin in fixed_origins
                ]
                transported_fixed = add_signatures(
                    subtract_signatures(
                        origin_signatures_fixed[0],
                        origin_signatures_fixed[1],
                        (),
                    ),
                    origin_signatures_fixed[2],
                )
                if transported_fixed == target_signature_fixed:
                    survivor_fixed = next(
                        matching
                        for matching in target_activity_fixed
                        if matching not in {first, second}
                    )
                    return {
                        "certificate_mode": (
                            "fixed_three_binomial_transport_pairs_"
                            "trinomial"
                        ),
                        "skeleton_perfect_matchings": len(matchings),
                        "binomial_forbidden_colourings": 3,
                        "trinomial_forbidden_colourings": 1,
                        "transport_prefix": transport_prefix,
                        "transport_binomial_equation_indices": list(
                            fixed_origins
                        ),
                        "transport_relation_signs": [1, -1, 1],
                        "transport_binomial_activities": [
                            list(activity)
                            for activity in origin_activities_fixed
                        ],
                        "transport_binomial_colourings": [
                            list(map(int, colourings[origin]))
                            for origin in fixed_origins
                        ],
                        "target_equation_index": fixed_target,
                        "target_colouring": list(
                            map(int, colourings[fixed_target])
                        ),
                        "target_activity": list(target_activity_fixed),
                        "paired_matching_indices": [first, second],
                        "surviving_matching_index": survivor_fixed,
                        "target_relation_signature": [
                            [entry, coefficient]
                            for entry, coefficient
                            in target_signature_fixed
                        ],
                    }

    def additional_fixed_pattern(
        target: int,
        origins: tuple[int, int, int],
    ) -> dict[str, object] | None:
        if target >= len(colourings) or any(
            origin >= len(colourings) for origin in origins
        ):
            return None
        target_activity = activity_for(colourings[target])
        origin_activities = [
            activity_for(colourings[origin]) for origin in origins
        ]
        if (
            len(target_activity) != 3
            or any(len(activity) != 2 for activity in origin_activities)
            or len(set(origin_activities)) != 1
        ):
            return None
        first, second = origin_activities[0]
        if first not in target_activity or second not in target_activity:
            return None
        target_signature = oriented_signature(
            matchings[first],
            matchings[second],
            colourings[target],
            full_edges,
            labels,
        )
        origin_signatures = [
            oriented_signature(
                matchings[first],
                matchings[second],
                colourings[origin],
                full_edges,
                labels,
            )
            for origin in origins
        ]
        transported = add_signatures(
            subtract_signatures(
                origin_signatures[0], origin_signatures[1], ()
            ),
            origin_signatures[2],
        )
        if transported != target_signature:
            return None
        survivor = next(
            matching
            for matching in target_activity
            if matching not in {first, second}
        )
        return {
            "certificate_mode": (
                "fixed_three_binomial_transport_pairs_trinomial"
            ),
            "skeleton_perfect_matchings": len(matchings),
            "binomial_forbidden_colourings": 3,
            "trinomial_forbidden_colourings": 1,
            "transport_prefix": transport_prefix,
            "transport_binomial_equation_indices": list(origins),
            "transport_relation_signs": [1, -1, 1],
            "transport_binomial_activities": [
                list(activity) for activity in origin_activities
            ],
            "transport_binomial_colourings": [
                list(map(int, colourings[origin])) for origin in origins
            ],
            "target_equation_index": target,
            "target_colouring": list(map(int, colourings[target])),
            "target_activity": list(target_activity),
            "paired_matching_indices": [first, second],
            "surviving_matching_index": survivor,
            "target_relation_signature": [
                [entry, coefficient]
                for entry, coefficient in target_signature
            ],
        }

    for target, origins in (
        (19, (262, 289, 46)),
        (10, (253, 281, 38)),
        (1, (244, 272, 29)),
        (22, (265, 292, 49)),
        (13, (257, 284, 40)),
        (13, (259, 286, 40)),
        (13, (256, 284, 41)),
        (22, (265, 293, 50)),
        (14, (260, 287, 41)),
        (30, (246, 244, 28)),
        (33, (276, 244, 1)),
        (9, (90, 93, 12)),
        (9, (117, 120, 12)),
        (9, (171, 174, 12)),
        (39, (264, 265, 40)),
        (42, (285, 259, 16)),
        *DISCOVERED_PATTERNS,
    ):
        fixed = additional_fixed_pattern(target, origins)
        if fixed is not None:
            return fixed
    counts = np.zeros(len(colourings), dtype=np.int16)
    first_id = np.full(len(colourings), -1, dtype=np.int16)
    second_id = np.full(len(colourings), -1, dtype=np.int16)
    third_id = np.full(len(colourings), -1, dtype=np.int16)
    for matching_id, matching in enumerate(matchings):
        requirements: dict[int, int] = {}
        viable = True
        for item in matching:
            if item not in labels:
                continue
            colour = labels[item]
            for vertex in item:
                if (
                    vertex in requirements
                    and requirements[vertex] != colour
                ):
                    viable = False
                    break
                requirements[vertex] = colour
            if not viable:
                break
        if not viable:
            continue
        mask = np.ones(len(colourings), dtype=bool)
        for vertex, colour in requirements.items():
            mask &= colourings[:, vertex] == colour
        first_id[mask & (counts == 0)] = matching_id
        second_id[mask & (counts == 1)] = matching_id
        third_id[mask & (counts == 2)] = matching_id
        counts += mask
    monochromatic = np.all(
        colourings == colourings[:, :1], axis=1
    )
    binomial = (counts == 2) & ~monochromatic
    trinomials = np.flatnonzero((counts == 3) & ~monochromatic)
    if (
        fixed_target < len(colourings)
        and all(origin < len(colourings) for origin in fixed_origins)
        and counts[fixed_target] == 3
        and all(counts[origin] == 2 for origin in fixed_origins)
    ):
        origin_pairs = [
            (
                int(first_id[origin]),
                int(second_id[origin]),
            )
            for origin in fixed_origins
        ]
        if len(set(origin_pairs)) == 1:
            first, second = origin_pairs[0]
            target_ids = [
                int(first_id[fixed_target]),
                int(second_id[fixed_target]),
                int(third_id[fixed_target]),
            ]
            if first in target_ids and second in target_ids:
                target_signature = oriented_signature(
                    matchings[first],
                    matchings[second],
                    colourings[fixed_target],
                    full_edges,
                    labels,
                )
                origin_signatures = [
                    oriented_signature(
                        matchings[first],
                        matchings[second],
                        colourings[origin],
                        full_edges,
                        labels,
                    )
                    for origin in fixed_origins
                ]
                transported = add_signatures(
                    subtract_signatures(
                        origin_signatures[0],
                        origin_signatures[1],
                        (),
                    ),
                    origin_signatures[2],
                )
                if transported == target_signature:
                    survivor = next(
                        matching
                        for matching in target_ids
                        if matching not in {first, second}
                    )
                    return {
                        "certificate_mode": (
                            "fixed_three_binomial_transport_pairs_"
                            "trinomial"
                        ),
                        "skeleton_perfect_matchings": len(matchings),
                        "binomial_forbidden_colourings": int(
                            np.count_nonzero(binomial)
                        ),
                        "trinomial_forbidden_colourings": len(
                            trinomials
                        ),
                        "transport_prefix": len(colourings),
                        "transport_binomial_equation_indices": list(
                            fixed_origins
                        ),
                        "transport_relation_signs": [1, -1, 1],
                        "transport_binomial_activities": [
                            list(pair) for pair in origin_pairs
                        ],
                        "transport_binomial_colourings": [
                            list(map(int, colourings[origin]))
                            for origin in fixed_origins
                        ],
                        "target_equation_index": fixed_target,
                        "target_colouring": list(
                            map(int, colourings[fixed_target])
                        ),
                        "target_activity": target_ids,
                        "paired_matching_indices": [first, second],
                        "surviving_matching_index": survivor,
                        "target_relation_signature": [
                            [entry, coefficient]
                            for entry, coefficient in target_signature
                        ],
                    }
    prefix_limit = len(colourings)
    grouped: dict[
        tuple[int, int],
        dict[tuple[tuple[int, int], ...], int],
    ] = {}
    for origin in np.flatnonzero(
        binomial
    ):
        first = int(first_id[origin])
        second = int(second_id[origin])
        signature = oriented_signature(
            matchings[first],
            matchings[second],
            colourings[origin],
            full_edges,
            labels,
        )
        grouped.setdefault((first, second), {}).setdefault(
            signature, int(origin)
        )
    signed_cache: dict[
        tuple[int, int],
        dict[tuple[tuple[int, int], ...], tuple[int, int]],
    ] = {}
    pair_sum_cache: dict[
        tuple[int, int],
        dict[
            tuple[tuple[int, int], ...],
            tuple[
                tuple[tuple[int, int], ...],
                tuple[int, int],
                tuple[tuple[int, int], ...],
                tuple[int, int],
            ],
        ],
    ] = {}
    for target in trinomials:
        if target >= prefix_limit:
            break
        target_ids = [
            int(first_id[target]),
            int(second_id[target]),
            int(third_id[target]),
        ]
        for first, second in itertools.combinations(target_ids, 2):
            relations = grouped.get((first, second))
            if not relations:
                continue
            pair_key = (first, second)
            if pair_key not in signed_cache:
                signed_cache[pair_key] = {}
                for signature, origin in relations.items():
                    signed_cache[pair_key].setdefault(
                        signature, (origin, 1)
                    )
                    signed_cache[pair_key].setdefault(
                        negate_signature(signature), (origin, -1)
                    )
            signed = signed_cache[pair_key]
            if pair_key not in pair_sum_cache:
                sums: dict[
                    tuple[tuple[int, int], ...],
                    tuple[
                        tuple[tuple[int, int], ...],
                        tuple[int, int],
                        tuple[tuple[int, int], ...],
                        tuple[int, int],
                    ],
                ] = {}
                signed_items_for_sums = list(signed.items())
                for first_signature, first_origin in (
                    signed_items_for_sums
                ):
                    for second_signature, second_origin in (
                        signed_items_for_sums
                    ):
                        sums.setdefault(
                            add_signatures(
                                first_signature, second_signature
                            ),
                            (
                                first_signature,
                                first_origin,
                                second_signature,
                                second_origin,
                            ),
                        )
                pair_sum_cache[pair_key] = sums
            pair_sums = pair_sum_cache[pair_key]
            target_signature = oriented_signature(
                matchings[first],
                matchings[second],
                colourings[target],
                full_edges,
                labels,
            )
            found: tuple[
                tuple[tuple[int, int], ...],
                tuple[int, int],
                tuple[tuple[int, int], ...],
                tuple[int, int],
                tuple[tuple[int, int], ...],
                tuple[int, int],
            ] | None = None
            for third_signature, third_origin in signed.items():
                needed_sum = subtract_signatures(
                    target_signature,
                    third_signature,
                    (),
                )
                if needed_sum in pair_sums:
                    (
                        first_signature,
                        first_origin,
                        second_signature,
                        second_origin,
                    ) = pair_sums[needed_sum]
                    found = (
                        first_signature,
                        first_origin,
                        second_signature,
                        second_origin,
                        third_signature,
                        third_origin,
                    )
                    break
            if found is None:
                continue
            survivor = next(
                matching
                for matching in target_ids
                if matching not in {first, second}
            )
            origins = [found[1], found[3], found[5]]
            return {
                "certificate_mode": (
                    "three_binomial_transport_relations_pair_trinomial"
                ),
                "skeleton_perfect_matchings": len(matchings),
                "binomial_forbidden_colourings": int(
                    np.count_nonzero(binomial)
                ),
                "trinomial_forbidden_colourings": len(trinomials),
                "transport_prefix": prefix_limit,
                "transport_binomial_equation_indices": [
                    int(origin[0]) for origin in origins
                ],
                "transport_relation_signs": [
                    int(origin[1]) for origin in origins
                ],
                "transport_binomial_activities": [
                    [
                        int(first_id[origin[0]]),
                        int(second_id[origin[0]]),
                    ]
                    for origin in origins
                ],
                "transport_binomial_colourings": [
                    list(map(int, colourings[origin[0]]))
                    for origin in origins
                ],
                "target_equation_index": int(target),
                "target_colouring": list(
                    map(int, colourings[target])
                ),
                "target_activity": target_ids,
                "paired_matching_indices": [first, second],
                "surviving_matching_index": survivor,
                "target_relation_signature": [
                    [entry, coefficient]
                    for entry, coefficient in target_signature
                ],
            }
    relation_origins: dict[tuple[tuple[int, int], ...], int] = {}
    for origin in np.flatnonzero(binomial):
        first = int(first_id[origin])
        second = int(second_id[origin])
        signature = relation_signature(
            matchings[first],
            matchings[second],
            colourings[origin],
            full_edges,
            labels,
        )
        relation_origins.setdefault(signature, int(origin))
    for target in trinomials:
        target_ids = [
            int(first_id[target]),
            int(second_id[target]),
            int(third_id[target]),
        ]
        for pair_positions in ((0, 1), (0, 2), (1, 2)):
            first = target_ids[pair_positions[0]]
            second = target_ids[pair_positions[1]]
            signature = relation_signature(
                matchings[first],
                matchings[second],
                colourings[target],
                full_edges,
                labels,
            )
            if signature not in relation_origins:
                continue
            origin = relation_origins[signature]
            origin_pair = [
                int(first_id[origin]),
                int(second_id[origin]),
            ]
            survivor = next(
                matching
                for matching in target_ids
                if matching not in {first, second}
            )
            return {
                "skeleton_perfect_matchings": len(matchings),
                "binomial_forbidden_colourings": int(
                    np.count_nonzero(binomial)
                ),
                "trinomial_forbidden_colourings": len(trinomials),
                "binomial_equation_index": origin,
                "binomial_colouring": list(
                    map(int, colourings[origin])
                ),
                "binomial_activity": origin_pair,
                "target_equation_index": int(target),
                "target_colouring": list(
                    map(int, colourings[target])
                ),
                "target_activity": target_ids,
                "paired_matching_indices": [first, second],
                "surviving_matching_index": survivor,
                "relation_signature": [
                    [entry, coefficient]
                    for entry, coefficient in signature
                ],
            }
    raise AssertionError(
        "support has no direct binomial/trinomial contradiction"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbits",
        type=Path,
        default=Path("tmp/ten_vertex_c10_equality_support_orbits.json"),
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="first orbit index for exploratory slices",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="exploratory prefix limit; zero means all orbits",
    )
    parser.add_argument(
        "--transport-prefix",
        type=int,
        default=729,
        help="search transport relations in this colouring prefix",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c10_equality_support_binomial_trinomial.json"
        ),
    )
    args = parser.parse_args()
    source = json.loads(args.orbits.read_text(encoding="utf-8"))
    if source.get("status") != "complete":
        raise AssertionError("orbit catalogue is incomplete")
    if source["full_cycle_type"] != [10]:
        raise AssertionError("orbit catalogue is not C10")
    full_edges = {
        tuple(map(int, item)) for item in source["full_edges"]
    }
    stop = (
        args.start + args.limit
        if args.limit
        else len(source["rows"])
    )
    selected_rows = source["rows"][args.start : stop]
    colourings = colouring_table(10)
    rows: list[dict[str, object]] = []
    started = time.perf_counter()
    for offset, orbit in enumerate(selected_rows):
        index = args.start + offset
        singleton_matchings = [
            [tuple(map(int, item)) for item in matching]
            for matching in orbit["singleton_matchings"]
        ]
        try:
            certificate = direct_certificate(
                full_edges,
                singleton_matchings,
                colourings,
                args.transport_prefix,
            )
        except AssertionError as error:
            raise AssertionError(f"orbit {index}: {error}") from error
        if certificate["certificate_mode"] == (
            "three_binomial_transport_relations_pair_trinomial"
        ):
            signs = list(
                map(int, certificate["transport_relation_signs"])
            )
            if signs.count(1) == 2 and signs.count(-1) == 1:
                positive = [
                    position
                    for position, sign in enumerate(signs)
                    if sign == 1
                ]
                negative = signs.index(-1)
                order = [positive[0], negative, positive[1]]
                for key in (
                    "transport_binomial_equation_indices",
                    "transport_binomial_activities",
                    "transport_binomial_colourings",
                ):
                    values = certificate[key]
                    certificate[key] = [
                        values[position] for position in order
                    ]
                certificate["transport_relation_signs"] = [1, -1, 1]
        if certificate["certificate_mode"] == (
            "three_binomial_transport_relations_pair_trinomial"
        ) and list(
            map(int, certificate["transport_relation_signs"])
        ) == [1, -1, 1]:
            pattern = (
                int(certificate["target_equation_index"]),
                tuple(
                    map(
                        int,
                        certificate[
                            "transport_binomial_equation_indices"
                        ],
                    )
                ),
            )
            if pattern not in DISCOVERED_PATTERNS:
                DISCOVERED_PATTERNS.append(pattern)
                print(
                    f"discovered transport pattern target={pattern[0]} "
                    f"origins={pattern[1]}",
                    flush=True,
                )
        rows.append(
            {
                "orbit_index": index,
                "orbit_size_uncoloured": int(
                    orbit["orbit_size_uncoloured"]
                ),
                "singleton_matchings": orbit["singleton_matchings"],
                **certificate,
            }
        )
        if (offset + 1) % 25 == 0 or offset + 1 == len(selected_rows):
            print(
                f"orbit={index + 1} processed={offset + 1}/"
                f"{len(selected_rows)} "
                f"binomials={certificate['binomial_forbidden_colourings']} "
                f"trinomials={certificate['trinomial_forbidden_colourings']}",
                flush=True,
            )
    complete = args.start == 0 and len(selected_rows) == len(source["rows"])
    payload = {
        "status": "all_direct" if complete else "limit",
        "scope": (
            "n=10,d=3 C10 equality supports with direct mandatory "
            "binomial/trinomial contradictions"
        ),
        "necessary_conditions_only": not complete,
        "orbit_catalogue": str(args.orbits),
        "raw_uncoloured_factorizations": int(
            source["raw_uncoloured_factorizations"]
        ),
        "support_orbits": len(source["rows"]),
        "processed_orbits": len(rows),
        "certified_orbits": len(rows),
        "discovered_transport_patterns": [
            {
                "target_equation_index": target,
                "origin_equation_indices": list(origins),
            }
            for target, origins in DISCOVERED_PATTERNS
        ],
        "rows": rows,
        "solve_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
