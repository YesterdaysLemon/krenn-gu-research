"""Bitset filter of support triples by larger one-term matching sets."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import itertools
import json
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    completion_tables,
    contiguous_cycles,
    factor_safe,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges, perfect_matchings
from find_fourteen_vertex_two_to_three_fork import solve_colouring

Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument("one_term_catalogue", type=Path)
    parser.add_argument("pair_filter", type=Path)
    parser.add_argument("--survivor-limit", type=int, default=20)
    parser.add_argument("--residuals-per-orbit", type=int, default=1)
    parser.add_argument(
        "--motif-supports",
        type=Path,
        help=(
            "support manifest whose connected_survivors correspond to "
            "the direct-motif analyses"
        ),
    )
    parser.add_argument(
        "--motif-analysis-pattern",
        default=(
            "tmp/fourteen_vertex_c3_3_4_4_connected_filtered_"
            "{index}_direct_motifs.json"
        ),
    )
    parser.add_argument("--motif-count", type=int, default=0)
    parser.add_argument(
        "--motif-batch",
        action="append",
        default=[],
        help=(
            "repeatable SUPPORT_PATH|SUPPORT_KEY|ANALYSIS_PATTERN|COUNT "
            "batch; ANALYSIS_PATTERN must contain {index}"
        ),
    )
    parser.add_argument(
        "--stable-fork-catalogue",
        type=Path,
        help=(
            "optional stable-C4 two-to-three fork catalogue to scan "
            "against every direct-motif residual"
        ),
    )
    parser.add_argument(
        "--stable-fork-scan-limit",
        type=int,
        default=0,
        help="maximum residual supports to scan; use 0 for all",
    )
    parser.add_argument(
        "--stable-fork-shard-count", type=int, default=1
    )
    parser.add_argument(
        "--stable-fork-shard-index", type=int, default=0
    )
    parser.add_argument(
        "--save-stable-fork-certificates",
        action="store_true",
        help=(
            "save a compact exact witness for every support closed by "
            "the stable-fork scan"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_larger_one_term_full_filter.json"
        ),
    )
    args = parser.parse_args()
    if (
        args.stable_fork_shard_count < 1
        or not 0
        <= args.stable_fork_shard_index
        < args.stable_fork_shard_count
    ):
        raise ValueError("invalid stable-fork shard")
    census = json.loads(args.census.read_text(encoding="utf-8"))
    catalogue = json.loads(
        args.one_term_catalogue.read_text(encoding="utf-8")
    )
    pairs = json.loads(args.pair_filter.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    if tuple(
        tuple(map(int, item)) for item in catalogue["eligible_edges"]
    ) != eligible_edges:
        raise ValueError("catalogue edge order mismatch")
    edge_id = {
        item: position for position, item in enumerate(eligible_edges)
    }
    vertex_component = {
        vertex: component
        for component, cycle in enumerate(cycles)
        for vertex in cycle
    }
    tables = completion_tables(cycles)
    all_factors = perfect_matchings(N, set(eligible_edges))
    factors = [
        factor
        for factor in all_factors
        if factor_safe(
            factor, cycles, vertex_component, tables
        )
    ]

    def mask(items: Factor | set[Edge]) -> int:
        return sum(1 << edge_id[item] for item in items)

    factor_masks = [mask(factor) for factor in factors]
    factor_id = {
        factor: position for position, factor in enumerate(factors)
    }
    vertex_component = {
        vertex: component
        for component, cycle in enumerate(cycles)
        for vertex in cycle
    }
    component_pairs = tuple(
        itertools.combinations(range(len(cycles)), 2)
    )
    component_pair_id = {
        pair: position for position, pair in enumerate(component_pairs)
    }

    def component_pattern(factor: Factor) -> int:
        output = 0
        for first, second in factor:
            pair = tuple(
                sorted(
                    (
                        vertex_component[first],
                        vertex_component[second],
                    )
                )
            )
            if pair[0] != pair[1]:
                output |= 1 << component_pair_id[pair]
        return output

    def component_connected(pattern: int) -> bool:
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
        return len(reached) == len(cycles)

    factor_component_patterns = [
        component_pattern(factor) for factor in factors
    ]
    factor_bits_by_component_pattern: dict[int, int] = {}
    for position, pattern in enumerate(factor_component_patterns):
        factor_bits_by_component_pattern[pattern] = (
            factor_bits_by_component_pattern.get(pattern, 0)
            | (1 << position)
        )
    connected_factor_bits = {
        pair_pattern: sum(
            bits
            for factor_pattern, bits
            in factor_bits_by_component_pattern.items()
            if component_connected(pair_pattern | factor_pattern)
        )
        for pair_pattern in range(1 << len(component_pairs))
    }

    motif_rules: list[tuple[int, int, int]] = []
    motif_rows = []
    motif_batches: list[tuple[Path, str, str, int]] = []
    if args.motif_count:
        if args.motif_supports is None:
            raise ValueError("--motif-count requires --motif-supports")
        motif_batches.append(
            (
                args.motif_supports,
                "connected_survivors",
                args.motif_analysis_pattern,
                args.motif_count,
            )
        )
    for raw_batch in args.motif_batch:
        parts = raw_batch.split("|")
        if len(parts) != 4:
            raise ValueError("invalid --motif-batch specification")
        motif_batches.append(
            (
                Path(parts[0]),
                parts[1],
                parts[2],
                int(parts[3]),
            )
        )

    def decode_colouring(index: int) -> tuple[int, ...]:
        return tuple(
            (index // (3**vertex)) % 3
            for vertex in range(N)
        )

    motif_id = 0
    for (
        motif_support_path,
        motif_support_key,
        motif_analysis_pattern,
        motif_count,
    ) in motif_batches:
        motif_support_payload = json.loads(
            motif_support_path.read_text(encoding="utf-8")
        )
        motif_supports = motif_support_payload[motif_support_key]
        for batch_index in range(motif_count):
            support = motif_supports[batch_index]
            analysis_path = Path(
                motif_analysis_pattern.format(index=batch_index)
            )
            analysis = json.loads(
                analysis_path.read_text(encoding="utf-8")
            )
            if analysis.get("status") != "direct_contradiction":
                raise AssertionError("motif analysis is not a contradiction")
            if analysis.get("one_term_forbidden_colourings") != 0:
                raise AssertionError("motif unexpectedly uses one-term mode")
            support_factors = [
                tuple(
                    tuple(map(int, item)) for item in support[key]
                )
                for key in ("first", "second", "third")
            ]
            reported_factors = [
                tuple(
                    tuple(map(int, item))
                    for item in analysis["singleton_matchings"][key]
                )
                for key in ("first", "second", "third")
            ]
            if support_factors != reported_factors:
                raise AssertionError("motif support/analysis mismatch")
            certificates = analysis.get("certificates") or [
                analysis["certificate"]
            ]
            for certificate_index, certificate in enumerate(certificates):
                if not certificate or certificate.get("certificate_mode"):
                    raise AssertionError(
                        "motif is not a direct "
                        "binomial-trinomial transport"
                    )
                origin = decode_colouring(
                    int(certificate["origin_equation_index"])
                )
                target = decode_colouring(
                    int(certificate["target_equation_index"])
                )
                allowed_by_role = []
                allowed_counts = []
                for colour, sample_factor in enumerate(support_factors):
                    required_origin = {
                        item
                        for item in sample_factor
                        if origin[item[0]]
                        == origin[item[1]]
                        == colour
                    }
                    required_target = {
                        item
                        for item in sample_factor
                        if target[item[0]]
                        == target[item[1]]
                        == colour
                    }
                    allowed = 0
                    for position, factor in enumerate(factors):
                        active_origin = {
                            item
                            for item in factor
                            if origin[item[0]]
                            == origin[item[1]]
                            == colour
                        }
                        if active_origin != required_origin:
                            continue
                        active_target = {
                            item
                            for item in factor
                            if target[item[0]]
                            == target[item[1]]
                            == colour
                        }
                        if active_target == required_target:
                            allowed |= 1 << position
                    if not allowed & (1 << factor_id[sample_factor]):
                        raise AssertionError(
                            "motif does not cover its source"
                        )
                    allowed_by_role.append(allowed)
                    allowed_counts.append(allowed.bit_count())
                for role_for_position in itertools.permutations(range(3)):
                    motif_rules.append(
                        tuple(
                            allowed_by_role[role]
                            for role in role_for_position
                        )
                    )
                motif_rows.append(
                    {
                        "motif_id": motif_id,
                        "batch_index": batch_index,
                        "certificate_index": certificate_index,
                        "support_manifest": str(motif_support_path),
                        "support_key": motif_support_key,
                        "analysis": str(analysis_path),
                        "source_orbit": int(support["orbit_id"]),
                        "allowed_factor_counts_by_role": allowed_counts,
                    }
                )
                motif_id += 1
    raw_motif_rule_count = len(motif_rules)
    motif_rules = list(dict.fromkeys(motif_rules))
    stable_fork_rows: list[
        tuple[int, int, int, tuple[int, ...]]
    ] = []
    if args.stable_fork_catalogue is not None:
        stable_payload = json.loads(
            args.stable_fork_catalogue.read_text(encoding="utf-8")
        )
        if tuple(map(int, stable_payload["partition"])) != lengths:
            raise ValueError("stable-fork catalogue partition mismatch")
        if tuple(
            tuple(map(int, item))
            for item in stable_payload["eligible_edges"]
        ) != eligible_edges:
            raise ValueError("stable-fork catalogue edge-order mismatch")
        stable_fork_rows = [
            (
                row_id,
                int(row["sparse_mask"]),
                int(row["rich_mask"]),
                tuple(cycles[int(row["alternating_c4_component"])]),
            )
            for row_id, row in enumerate(stable_payload["fork_rows"])
        ]

    def decode_edge_mask(selected: int) -> set[Edge]:
        return {
            eligible_edges[item_id]
            for item_id in range(len(eligible_edges))
            if selected & (1 << item_id)
        }

    def has_colour_feasible_stable_fork(
        support_factor_ids: tuple[int, int, int],
    ) -> (
        tuple[int, int, tuple[int, ...], tuple[int, ...]]
        | None
    ):
        support_factors = [
            factors[position] for position in support_factor_ids
        ]
        labelled_edges = {
            item: colour
            for colour, factor in enumerate(support_factors)
            for item in factor
        }
        support_edge_mask = (
            factor_masks[support_factor_ids[0]]
            | factor_masks[support_factor_ids[1]]
            | factor_masks[support_factor_ids[2]]
        )
        for (
            fork_id,
            sparse_mask,
            rich_mask,
            c4_vertices,
        ) in stable_fork_rows:
            if rich_mask & support_edge_mask != rich_mask:
                continue
            sparse_edges = decode_edge_mask(sparse_mask)
            rich_edges = decode_edge_mask(rich_mask)
            for c4_colours in itertools.product(range(3), repeat=4):
                fixed = dict(zip(c4_vertices, c4_colours))
                origin = solve_colouring(
                    labelled_edges, sparse_edges, fixed
                )
                if origin is None:
                    continue
                target = solve_colouring(
                    labelled_edges, rich_edges, fixed
                )
                if target is not None:
                    c4_code = sum(
                        colour * (3**position)
                        for position, colour in enumerate(c4_colours)
                    )
                    return fork_id, c4_code, origin, target
        return None
    one_terms = {
        int(size): set(map(int, masks))
        for size, masks in catalogue["one_term_masks_by_size"].items()
    }
    size_three = one_terms.get(3, set())
    pair_completions: dict[tuple[int, int], int] = {}
    for target_mask in size_three:
        item_ids = tuple(
            position
            for position in range(len(eligible_edges))
            if target_mask & (1 << position)
        )
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

    def completion(selected_edges: int) -> int:
        item_ids = [
            position
            for position in range(len(eligible_edges))
            if selected_edges & (1 << position)
        ]
        output = 0
        for first, second in itertools.combinations(item_ids, 2):
            output |= pair_completions.get((first, second), 0)
        return output

    factor_completions = [completion(value) for value in factor_masks]
    factor_bits_by_edge = [0] * len(eligible_edges)
    completion_bits_by_edge = [0] * len(eligible_edges)
    for position, (selected, completed) in enumerate(
        zip(factor_masks, factor_completions, strict=True)
    ):
        factor_bit = 1 << position
        for item_id in range(len(eligible_edges)):
            edge_bit = 1 << item_id
            if selected & edge_bit:
                factor_bits_by_edge[item_id] |= factor_bit
            if completed & edge_bit:
                completion_bits_by_edge[item_id] |= factor_bit

    larger_masks = tuple(
        mask_value
        for size in sorted(one_terms)
        if size >= 4
        for mask_value in one_terms[size]
    )
    split_rows = []
    relevant_remainders = set()
    for target in larger_masks:
        bits = [
            1 << item_id
            for item_id in range(len(eligible_edges))
            if target & (1 << item_id)
        ]
        for selector in range(1, (1 << len(bits)) - 1):
            base = sum(
                bits[position]
                for position in range(len(bits))
                if selector & (1 << position)
            )
            remainder = target ^ base
            split_rows.append((base, remainder))
            relevant_remainders.add(remainder)

    factor_superset_bits: dict[int, int] = {}
    for position, selected in enumerate(factor_masks):
        bits = [
            1 << item_id
            for item_id in range(len(eligible_edges))
            if selected & (1 << item_id)
        ]
        for size in range(1, 5):
            for subset in itertools.combinations(bits, size):
                remainder = sum(subset)
                if remainder not in relevant_remainders:
                    continue
                factor_superset_bits[remainder] = (
                    factor_superset_bits.get(remainder, 0)
                    | (1 << position)
                )

    base_forbidden_factor_bits: dict[int, int] = {}
    for base, remainder in split_rows:
        forbidden = factor_superset_bits.get(remainder, 0)
        if forbidden:
            base_forbidden_factor_bits[base] = (
                base_forbidden_factor_bits.get(base, 0)
                | forbidden
            )

    all_factor_bits = (1 << len(factors)) - 1
    orbit_rows = {
        orbit_id: {
            "orbit_id": orbit_id,
            "pair_survivors": 0,
            "size3_compatible_thirds": 0,
            "larger_one_term_free_thirds": 0,
            "connected_larger_one_term_free_thirds": 0,
            "direct_motif_free_connected_thirds": 0,
            "stable_fork_scanned_thirds": 0,
            "stable_fork_free_thirds": 0,
        }
        for orbit_id in range(len(census["factor_orbits"]))
    }
    survivors = []
    connected_survivors: dict[int, dict[str, object]] = {}
    motif_residual_survivors: dict[
        int, list[dict[str, object]]
    ] = {}
    stable_fork_residual_survivors: dict[
        int, list[dict[str, object]]
    ] = {}
    stable_fork_scanned_total = 0
    stable_fork_closed_total = 0
    stable_fork_candidate_total = 0
    stable_fork_certificates: list[list[int]] = []
    for pair in pairs["pair_survivors"]:
        orbit_id = int(pair["orbit_id"])
        first = tuple(
            tuple(map(int, item)) for item in pair["first"]
        )
        second = tuple(
            tuple(map(int, item)) for item in pair["second"]
        )
        first_id = factor_id[first]
        second_id = factor_id[second]
        selected = factor_masks[first_id] | factor_masks[second_id]
        completed = completion(selected)

        conflict_factors = 0
        selected_ids = [
            item_id
            for item_id in range(len(eligible_edges))
            if selected & (1 << item_id)
        ]
        for item_id in selected_ids:
            conflict_factors |= factor_bits_by_edge[item_id]
            conflict_factors |= completion_bits_by_edge[item_id]
        for item_id in range(len(eligible_edges)):
            if completed & (1 << item_id):
                conflict_factors |= factor_bits_by_edge[item_id]
        size3_candidates = all_factor_bits & ~conflict_factors

        larger_conflicts = 0
        selected_bits = [1 << item_id for item_id in selected_ids]
        for size in range(1, 5):
            for subset in itertools.combinations(selected_bits, size):
                larger_conflicts |= base_forbidden_factor_bits.get(
                    sum(subset), 0
                )
        accepted = size3_candidates & ~larger_conflicts
        pair_component_pattern = (
            factor_component_patterns[first_id]
            | factor_component_patterns[second_id]
        )
        connected_accepted = (
            accepted & connected_factor_bits[pair_component_pattern]
        )
        direct_closed = 0
        if motif_rules:
            first_bit = 1 << first_id
            second_bit = 1 << second_id
            for allowed_first, allowed_second, allowed_third in motif_rules:
                if (
                    allowed_first & first_bit
                    and allowed_second & second_bit
                ):
                    direct_closed |= allowed_third
        direct_residual = connected_accepted & ~direct_closed
        size3_count = size3_candidates.bit_count()
        accepted_count = accepted.bit_count()
        connected_count = connected_accepted.bit_count()
        direct_residual_count = direct_residual.bit_count()
        row = orbit_rows[orbit_id]
        row["pair_survivors"] += 1
        row["size3_compatible_thirds"] += size3_count
        row["larger_one_term_free_thirds"] += accepted_count
        row["connected_larger_one_term_free_thirds"] += connected_count
        row["direct_motif_free_connected_thirds"] += (
            direct_residual_count
        )

        stable_fork_residual = 0
        pending_stable = direct_residual
        while pending_stable and stable_fork_rows:
            if (
                args.stable_fork_scan_limit
                and stable_fork_scanned_total
                >= args.stable_fork_scan_limit
            ):
                break
            third_bit = pending_stable & -pending_stable
            pending_stable ^= third_bit
            third_id = third_bit.bit_length() - 1
            candidate_ordinal = stable_fork_candidate_total
            stable_fork_candidate_total += 1
            if (
                candidate_ordinal
                % args.stable_fork_shard_count
                != args.stable_fork_shard_index
            ):
                continue
            stable_fork_scanned_total += 1
            row["stable_fork_scanned_thirds"] += 1
            stable_certificate = has_colour_feasible_stable_fork(
                (first_id, second_id, third_id)
            )
            if stable_certificate is not None:
                stable_fork_closed_total += 1
                if args.save_stable_fork_certificates:
                    (
                        fork_id,
                        c4_code,
                        origin,
                        target,
                    ) = stable_certificate
                    stable_fork_certificates.append(
                        [
                            candidate_ordinal,
                            orbit_id,
                            first_id,
                            second_id,
                            third_id,
                            fork_id,
                            c4_code,
                            sum(
                                colour * (3**vertex)
                                for vertex, colour in enumerate(origin)
                            ),
                            sum(
                                colour * (3**vertex)
                                for vertex, colour in enumerate(target)
                            ),
                        ]
                    )
            else:
                stable_fork_residual |= third_bit
                row["stable_fork_free_thirds"] += 1
            if stable_fork_scanned_total % 10_000 == 0:
                print(
                    "stable_fork_scanned="
                    f"{stable_fork_scanned_total} "
                    f"closed={stable_fork_closed_total}",
                    flush=True,
                )
        if not stable_fork_rows:
            stable_fork_residual = direct_residual

        if connected_accepted and orbit_id not in connected_survivors:
            third_bit = connected_accepted & -connected_accepted
            third_id = third_bit.bit_length() - 1
            connected_survivors[orbit_id] = {
                "orbit_id": orbit_id,
                "first": [list(item) for item in first],
                "second": [list(item) for item in second],
                "third": [
                    list(item) for item in factors[third_id]
                ],
            }
        saved_residuals = motif_residual_survivors.setdefault(
            orbit_id, []
        )
        if (
            direct_residual
            and len(saved_residuals) < args.residuals_per_orbit
        ):
            third_bit = direct_residual & -direct_residual
            third_id = third_bit.bit_length() - 1
            saved_residuals.append(
                {
                    "orbit_id": orbit_id,
                    "first": [list(item) for item in first],
                    "second": [list(item) for item in second],
                    "third": [
                        list(item) for item in factors[third_id]
                    ],
                }
            )
        saved_stable_residuals = (
            stable_fork_residual_survivors.setdefault(orbit_id, [])
        )
        if (
            stable_fork_residual
            and len(saved_stable_residuals) < args.residuals_per_orbit
        ):
            third_bit = (
                stable_fork_residual & -stable_fork_residual
            )
            third_id = third_bit.bit_length() - 1
            saved_stable_residuals.append(
                {
                    "orbit_id": orbit_id,
                    "first": [list(item) for item in first],
                    "second": [list(item) for item in second],
                    "third": [
                        list(item) for item in factors[third_id]
                    ],
                }
            )

        while accepted and (
            args.survivor_limit == 0
            or len(survivors) < args.survivor_limit
        ):
            third_bit = accepted & -accepted
            accepted ^= third_bit
            third_id = third_bit.bit_length() - 1
            survivors.append(
                {
                    "orbit_id": orbit_id,
                    "first": [list(item) for item in first],
                    "second": [list(item) for item in second],
                    "third": [
                        list(item) for item in factors[third_id]
                    ],
                }
            )
            if (
                args.survivor_limit
                and len(survivors) == args.survivor_limit
            ):
                break

    rows = [orbit_rows[index] for index in sorted(orbit_rows)]
    payload = {
        "status": (
            "zero_supports_after_uncoloured_one_term_filter"
            if not sum(
                row["larger_one_term_free_thirds"] for row in rows
            )
            else "uncoloured_one_term_filter_survivors"
        ),
        "necessary_conditions_only": True,
        "partition": list(lengths),
        "safe_factors": len(factors),
        "larger_one_term_masks": len(larger_masks),
        "relevant_remainder_masks": len(relevant_remainders),
        "indexed_remainder_masks": len(factor_superset_bits),
        "indexed_base_masks": len(base_forbidden_factor_bits),
        "pair_survivors": len(pairs["pair_survivors"]),
        "size3_compatible_thirds": sum(
            row["size3_compatible_thirds"] for row in rows
        ),
        "larger_one_term_free_thirds": sum(
            row["larger_one_term_free_thirds"] for row in rows
        ),
        "connected_larger_one_term_free_thirds": sum(
            row["connected_larger_one_term_free_thirds"]
            for row in rows
        ),
        "disconnected_larger_one_term_free_thirds": sum(
            row["larger_one_term_free_thirds"]
            - row["connected_larger_one_term_free_thirds"]
            for row in rows
        ),
        "direct_motifs": len(motif_rows),
        "raw_direct_motif_colour_rules": raw_motif_rule_count,
        "direct_motif_colour_rules": len(motif_rules),
        "direct_motif_free_connected_thirds": sum(
            row["direct_motif_free_connected_thirds"] for row in rows
        ),
        "stable_fork_catalogue": (
            str(args.stable_fork_catalogue)
            if args.stable_fork_catalogue is not None
            else None
        ),
        "stable_fork_catalogued_patterns": len(stable_fork_rows),
        "stable_fork_candidate_thirds": stable_fork_candidate_total,
        "stable_fork_shard_count": args.stable_fork_shard_count,
        "stable_fork_shard_index": args.stable_fork_shard_index,
        "stable_fork_scanned_thirds": stable_fork_scanned_total,
        "stable_fork_closed_thirds": stable_fork_closed_total,
        "stable_fork_free_thirds": sum(
            row["stable_fork_free_thirds"] for row in rows
        ),
        "stable_fork_certificates_saved": len(
            stable_fork_certificates
        ),
        "survivor_save_limit": args.survivor_limit,
        "residuals_per_orbit": args.residuals_per_orbit,
        "survivors": survivors,
        "connected_survivors": [
            connected_survivors[index]
            for index in sorted(connected_survivors)
        ],
        "motif_residual_survivors": [
            survivor
            for index in sorted(motif_residual_survivors)
            for survivor in motif_residual_survivors[index]
        ],
        "stable_fork_residual_survivors": [
            survivor
            for index in sorted(stable_fork_residual_survivors)
            for survivor in stable_fork_residual_survivors[index]
        ],
        "motif_rows": motif_rows,
        "stable_fork_certificates": stable_fork_certificates,
        "orbit_rows": rows,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key not in {
                    "survivors",
                    "connected_survivors",
                    "motif_residual_survivors",
                    "stable_fork_residual_survivors",
                    "motif_rows",
                    "stable_fork_certificates",
                    "orbit_rows",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
