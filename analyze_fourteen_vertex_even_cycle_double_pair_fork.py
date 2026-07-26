"""Find an 8 -> (10, 10) -> 13 all-even factor-choice fork.

For a full factor with three even cycles, the eight full-only monomials
factor as three binomials.  A full-only forbidden equation therefore makes
at least one cycle binomial vanish.  Two ten-term equations preserving that
cycle colouring can then force two further binomial relations.  If a
thirteen-term equation contains those two pairs plus one extra monomial,
the extra survives, giving a contradiction.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_even_cycle_factor_fork import local_codes
from explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles


def pair_cover_with_survivor(
    extras: tuple[int, ...],
    available: list[tuple],
) -> tuple[tuple, ...] | None:
    """Cover all but one extra matching by available disjoint pairs."""
    row_by_pair = {
        frozenset((row[0], row[1])): row for row in available
    }
    adjacency = {
        matching_id: {
            other
            for pair in row_by_pair
            if matching_id in pair
            for other in pair
            if other != matching_id
        }
        for matching_id in extras
    }

    def cover(remaining: frozenset[int]):
        if not remaining:
            return ()
        first = min(
            remaining,
            key=lambda item: len(adjacency[item] & remaining),
        )
        for second in sorted(adjacency[first] & remaining):
            suffix = cover(remaining - {first, second})
            if suffix is not None:
                return (
                    row_by_pair[frozenset((first, second))],
                    *suffix,
                )
        return None

    for survivor in extras:
        selected = cover(frozenset(extras) - {survivor})
        if selected is not None:
            return selected
    return None


def activity_arrays(
    matchings: list[tuple[tuple[int, int], ...]],
    labels: dict[tuple[int, int], int],
    capacity: int,
) -> tuple[np.ndarray, list[np.ndarray], int]:
    counts = np.zeros(engine.EQUATIONS, dtype=np.int16)
    slots = [
        np.full(engine.EQUATIONS, -1, dtype=np.int16)
        for _ in range(capacity)
    ]
    offset_cache: dict[tuple[int, ...], np.ndarray] = {}
    total_extensions = 0
    for matching_id, matching in enumerate(matchings):
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        base = sum(
            colour * (3**vertex)
            for vertex, colour in requirements.items()
        )
        free = tuple(
            vertex
            for vertex in range(engine.N)
            if vertex not in requirements
        )
        indices = base + engine.extension_offsets(free, offset_cache)
        old = counts[indices].copy()
        for position in range(capacity):
            slots[position][indices[old == position]] = matching_id
        counts[indices] = old + 1
        total_extensions += len(indices)
    return counts, slots, total_extensions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--survivor-key", default="survivors")
    parser.add_argument(
        "--triple-pair-cycle",
        type=int,
        help=(
            "also try an 8 -> three 10 -> 15 fork for this "
            "zero-based cycle index"
        ),
    )
    parser.add_argument(
        "--extended-pair-count",
        type=int,
        default=3,
        help=(
            "number of transported pairs in the extended rich target "
            "(default: 3, giving an 8+7=15 term target)"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_even_cycle_double_pair_fork.json"
        ),
    )
    args = parser.parse_args()

    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration[args.survivor_key][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    if len(lengths) != 3 or any(length % 2 for length in lengths):
        raise ValueError("this fork requires exactly three even cycles")
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = full_edges
    singleton_matchings = [
        tuple(engine.edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = engine.perfect_matchings(set(full_edges) | set(labels))
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    baseline = 1 << len(cycles)
    if len(full_only) != baseline:
        raise AssertionError("full-only matching count changed")
    pair_size = baseline + 2
    rich_size = baseline + 5
    if args.extended_pair_count < 2:
        raise ValueError("--extended-pair-count must be at least two")
    triple_rich_size = baseline + 2 * args.extended_pair_count + 1
    capacity = (
        triple_rich_size
        if args.triple_pair_cycle is not None
        else rich_size
    )
    if args.triple_pair_cycle is not None and not (
        0 <= args.triple_pair_cycle < len(cycles)
    ):
        raise ValueError("invalid --triple-pair-cycle")

    started = time.perf_counter()
    counts, slots, total_extensions = activity_arrays(
        matchings, labels, capacity
    )
    monochromatic = np.array(
        [
            sum(
                colour * (3**vertex)
                for vertex in range(engine.N)
            )
            for colour in range(3)
        ],
        dtype=np.int64,
    )
    counts[monochromatic] = -1

    def ids_at(equation: int, size: int) -> tuple[int, ...]:
        return tuple(int(slots[position][equation]) for position in range(size))

    def containing_full(size: int) -> np.ndarray:
        indices = np.flatnonzero(counts == size)
        keep = np.zeros(len(indices), dtype=bool)
        for position, equation in enumerate(indices):
            keep[position] = full_only <= set(
                ids_at(int(equation), size)
            )
        return indices[keep]

    base_indices = containing_full(baseline)
    pair_indices = containing_full(pair_size)
    rich_indices = containing_full(rich_size)
    triple_rich_indices = (
        containing_full(triple_rich_size)
        if args.triple_pair_cycle is not None
        else np.array([], dtype=np.int64)
    )

    # Only signatures which occur as pairs inside a rich target can matter.
    candidate_keys: list[
        set[tuple[int, tuple[tuple[int, int], ...]]]
    ] = [set() for _cycle in cycles]
    rich_rows = []
    for equation_value in rich_indices:
        equation = int(equation_value)
        colouring = engine.indexed_colouring(equation)
        extras = tuple(
            matching_id
            for matching_id in ids_at(equation, rich_size)
            if matching_id not in full_only
        )
        if len(extras) != 5:
            raise AssertionError("rich extra count changed")
        codes = [
            int(
                local_codes(
                    np.array([equation], dtype=np.int64), cycle
                )[0]
            )
            for cycle in cycles
        ]
        pair_rows = []
        for first, second in itertools.combinations(extras, 2):
            signature = engine.relation_signature(
                matchings[first],
                matchings[second],
                colouring,
                labels,
            )
            pair_rows.append((first, second, signature))
            for cycle_id, code in enumerate(codes):
                candidate_keys[cycle_id].add((code, signature))
        rich_rows.append((equation, extras, codes, pair_rows))

    origin_by_key: list[
        dict[
            tuple[int, tuple[tuple[int, int], ...]],
            tuple[int, int, int],
        ]
    ] = [dict() for _cycle in cycles]
    triple_origin_by_key: dict[
        tuple[int, tuple[tuple[int, int], ...]],
        tuple[int, int, int],
    ] = {}
    for equation_value in pair_indices:
        equation = int(equation_value)
        activity = ids_at(equation, pair_size)
        extras = tuple(
            matching_id
            for matching_id in activity
            if matching_id not in full_only
        )
        if len(extras) != 2:
            raise AssertionError("pair extra count changed")
        colouring = engine.indexed_colouring(equation)
        signature = engine.relation_signature(
            matchings[extras[0]],
            matchings[extras[1]],
            colouring,
            labels,
        )
        for cycle_id, cycle in enumerate(cycles):
            code = int(
                local_codes(
                    np.array([equation], dtype=np.int64), cycle
                )[0]
            )
            key = (code, signature)
            if key in candidate_keys[cycle_id]:
                origin_by_key[cycle_id].setdefault(
                    key,
                    (equation, extras[0], extras[1]),
                )
            if cycle_id == args.triple_pair_cycle:
                triple_origin_by_key.setdefault(
                    key,
                    (equation, extras[0], extras[1]),
                )

    fork_by_cycle_code: list[dict[int, dict[str, object]]] = [
        {} for _cycle in cycles
    ]
    for equation, extras, codes, pair_rows in rich_rows:
        for cycle_id, code in enumerate(codes):
            available = []
            for first, second, signature in pair_rows:
                origin = origin_by_key[cycle_id].get((code, signature))
                if origin is not None:
                    available.append(
                        (
                            first,
                            second,
                            signature,
                            origin[0],
                            origin[1],
                            origin[2],
                        )
                    )
            for left, right in itertools.combinations(available, 2):
                left_ids = {left[0], left[1]}
                right_ids = {right[0], right[1]}
                if left_ids & right_ids:
                    continue
                survivor_id = next(
                    matching_id
                    for matching_id in extras
                    if matching_id not in left_ids | right_ids
                )
                fork_by_cycle_code[cycle_id].setdefault(
                    code,
                    {
                        "cycle": list(cycles[cycle_id]),
                        "cycle_local_code": code,
                        "first_pair_equation_index": left[3],
                        "first_pair_matchings": [left[4], left[5]],
                        "first_pair_relation_signature": [
                            list(item) for item in left[2]
                        ],
                        "second_pair_equation_index": right[3],
                        "second_pair_matchings": [right[4], right[5]],
                        "second_pair_relation_signature": [
                            list(item) for item in right[2]
                        ],
                        "rich_equation_index": equation,
                        "rich_activity": list(
                            ids_at(equation, rich_size)
                        ),
                        "rich_paired_matchings": [
                            [left[0], left[1]],
                            [right[0], right[1]],
                        ],
                        "rich_surviving_matching": survivor_id,
                    },
                )
                break

    # A second branch can be stronger than preserving one local code.
    # If conditional forks make the other cycle factors nonzero on a
    # full Cartesian slice of base equations, the remaining cycle
    # binomial is forced to vanish at every one of its local colourings.
    # Then every ten-term equation forces its extra matching pair, with
    # no local-code restriction, and one thirteen-term equation may
    # contain two transported pairs plus a survivor.
    base_code_arrays = [
        local_codes(base_indices, cycle) for cycle in cycles
    ]
    global_forced_cycle_certificate = None
    forced_local_code_coverage_by_cycle: list[int] = []
    forced_local_codes_by_cycle: list[list[int]] = []
    global_rich_pair_fork_by_cycle: list[bool] = []
    for forced_cycle_id, forced_cycle in enumerate(cycles):
        forcing_mask = np.ones(len(base_indices), dtype=bool)
        for other_cycle_id in range(len(cycles)):
            if other_cycle_id == forced_cycle_id:
                continue
            bad_codes = np.array(
                sorted(fork_by_cycle_code[other_cycle_id]),
                dtype=np.int64,
            )
            if len(bad_codes) == 0:
                forcing_mask[:] = False
            else:
                forcing_mask &= np.isin(
                    base_code_arrays[other_cycle_id],
                    bad_codes,
                )
        forcing_positions = np.flatnonzero(forcing_mask)
        forcing_by_code: dict[int, int] = {}
        for position_value in forcing_positions:
            position = int(position_value)
            code = int(base_code_arrays[forced_cycle_id][position])
            forcing_by_code.setdefault(
                code, int(base_indices[position])
            )
        forced_local_code_coverage_by_cycle.append(
            len(forcing_by_code)
        )
        forced_local_codes_by_cycle.append(
            sorted(forcing_by_code)
        )
        if not forcing_by_code:
            global_rich_pair_fork_by_cycle.append(False)
            continue

        forced_codes = set(forcing_by_code)
        forced_origin_by_signature: dict[
            tuple[tuple[int, int], ...],
            tuple[int, int, int, int],
        ] = {}
        pair_codes = local_codes(pair_indices, forced_cycle)
        for position_value in np.flatnonzero(
            np.isin(
                pair_codes,
                np.array(sorted(forced_codes), dtype=np.int64),
            )
        ):
            position = int(position_value)
            equation = int(pair_indices[position])
            activity = ids_at(equation, pair_size)
            extras = tuple(
                matching_id
                for matching_id in activity
                if matching_id not in full_only
            )
            colouring = engine.indexed_colouring(equation)
            signature = engine.relation_signature(
                matchings[extras[0]],
                matchings[extras[1]],
                colouring,
                labels,
            )
            forced_origin_by_signature.setdefault(
                signature,
                (
                    equation,
                    int(pair_codes[position]),
                    extras[0],
                    extras[1],
                ),
            )

        rich_choice: (
            tuple[
                int,
                tuple[
                    tuple[
                        int,
                        int,
                        tuple[tuple[int, int], ...],
                        int,
                        int,
                    ],
                    ...,
                ],
                int,
                int,
                int,
            ]
            | None
        ) = None
        for equation, extras, codes, pair_rows in rich_rows:
            if codes[forced_cycle_id] not in forced_codes:
                continue
            available = [
                (
                    first,
                    second,
                    signature,
                    forced_origin_by_signature[signature][0],
                    forced_origin_by_signature[signature][1],
                    forced_origin_by_signature[signature][2],
                    forced_origin_by_signature[signature][3],
                )
                for first, second, signature in pair_rows
                if signature in forced_origin_by_signature
            ]
            selected_pairs = pair_cover_with_survivor(
                extras, available
            )
            if selected_pairs is not None:
                used = {
                    matching_id
                    for row in selected_pairs
                    for matching_id in row[:2]
                }
                survivor_id = next(
                    matching_id
                    for matching_id in extras
                    if matching_id not in used
                )
                rich_choice = (
                    equation,
                    selected_pairs,
                    survivor_id,
                    codes[forced_cycle_id],
                    rich_size,
                )
            if rich_choice is not None:
                break
        if (
            rich_choice is None
            and args.triple_pair_cycle == forced_cycle_id
        ):
            triple_codes = local_codes(
                triple_rich_indices, forced_cycle
            )
            for position_value in np.flatnonzero(
                np.isin(
                    triple_codes,
                    np.array(
                        sorted(forced_codes), dtype=np.int64
                    ),
                )
            ):
                position = int(position_value)
                equation = int(triple_rich_indices[position])
                colouring = engine.indexed_colouring(equation)
                extras = tuple(
                    matching_id
                    for matching_id in ids_at(
                        equation, triple_rich_size
                    )
                    if matching_id not in full_only
                )
                available = []
                for first, second in itertools.combinations(extras, 2):
                    signature = engine.relation_signature(
                        matchings[first],
                        matchings[second],
                        colouring,
                        labels,
                    )
                    origin = forced_origin_by_signature.get(signature)
                    if origin is not None:
                        available.append(
                        (
                            first,
                            second,
                            signature,
                            origin[0],
                            origin[1],
                            origin[2],
                            origin[3],
                        )
                        )
                selected_pairs = pair_cover_with_survivor(
                    extras, available
                )
                if selected_pairs is None:
                    continue
                used = {
                    matching_id
                    for row in selected_pairs
                    for matching_id in row[:2]
                }
                survivor_id = next(
                    matching_id
                    for matching_id in extras
                    if matching_id not in used
                )
                rich_choice = (
                    equation,
                    selected_pairs,
                    survivor_id,
                    int(triple_codes[position]),
                    triple_rich_size,
                )
                break
        if rich_choice is None:
            global_rich_pair_fork_by_cycle.append(False)
            continue
        global_rich_pair_fork_by_cycle.append(True)

        (
            equation,
            selected_pairs,
            survivor_id,
            rich_forced_code,
            selected_rich_size,
        ) = rich_choice
        required_forced_codes = {
            int(rich_forced_code),
            *(int(row[4]) for row in selected_pairs),
        }
        forcing_rows = []
        used_conditional_codes = [
            set() for _cycle in cycles
        ]
        for code in sorted(required_forced_codes):
            base_equation = forcing_by_code[code]
            local_codes_at_base = [
                int(
                    local_codes(
                        np.array([base_equation], dtype=np.int64),
                        cycle,
                    )[0]
                )
                for cycle in cycles
            ]
            for other_cycle_id, other_code in enumerate(
                local_codes_at_base
            ):
                if other_cycle_id != forced_cycle_id:
                    used_conditional_codes[other_cycle_id].add(
                        other_code
                    )
            forcing_rows.append(
                {
                    "forced_local_code": code,
                    "base_equation_index": base_equation,
                    "base_cycle_local_codes": local_codes_at_base,
                }
            )
        conditional_certificates = []
        for other_cycle_id, codes in enumerate(
            used_conditional_codes
        ):
            if other_cycle_id == forced_cycle_id:
                continue
            conditional_certificates.append(
                {
                    "cycle": list(cycles[other_cycle_id]),
                    "certificates_by_local_code": {
                        str(code): fork_by_cycle_code[
                            other_cycle_id
                        ][code]
                        for code in sorted(codes)
                    },
                }
            )
        global_forced_cycle_certificate = {
            "certificate_mode": (
                "forced_cycle_slice_pair_survivor_fork"
            ),
            "logical_chain": (
                "conditional forks rule out the other cycle factors; "
                "a full Cartesian set of base equations therefore "
                "forces the stated cycle binomial at every local "
                "colouring slice; the selected ten-term equations "
                "then force their extra matching pairs, and the rich "
                "equation leaves one nonzero survivor"
            ),
            "forced_cycle": list(forced_cycle),
            "forcing_base_equations_by_local_code": forcing_rows,
            "conditional_cycle_certificates": (
                conditional_certificates
            ),
            "pair_equations": [
                {
                    "equation_index": row[3],
                    "forced_cycle_local_code": row[4],
                    "matchings": [row[5], row[6]],
                    "rich_matchings": [row[0], row[1]],
                    "relation_signature": [
                        list(item) for item in row[2]
                    ],
                }
                for row in selected_pairs
            ],
            "rich_equation_index": equation,
            "rich_forced_cycle_local_code": rich_forced_code,
            "rich_activity": list(
                ids_at(equation, selected_rich_size)
            ),
            "rich_paired_matchings": [
                [row[0], row[1]] for row in selected_pairs
            ],
            "rich_surviving_matching": survivor_id,
        }
        break

    triple_needed_codes: set[int] = set()
    triple_forks_found = 0
    if (
        args.triple_pair_cycle is not None
        and global_forced_cycle_certificate is None
    ):
        triple_cycle_id = args.triple_pair_cycle
        other_mask = np.ones(len(base_indices), dtype=bool)
        base_code_arrays = [
            local_codes(base_indices, cycle) for cycle in cycles
        ]
        for cycle_id in range(len(cycles)):
            if cycle_id == triple_cycle_id:
                continue
            good_codes = np.array(
                sorted(fork_by_cycle_code[cycle_id]),
                dtype=np.int64,
            )
            if len(good_codes) == 0:
                other_mask[:] = False
            else:
                other_mask &= np.isin(
                    base_code_arrays[cycle_id], good_codes
                )
        triple_needed_codes = set(
            map(
                int,
                np.unique(
                    base_code_arrays[triple_cycle_id][other_mask]
                ),
            )
        )

        for equation_value in triple_rich_indices:
            if (
                triple_needed_codes
                <= set(fork_by_cycle_code[triple_cycle_id])
            ):
                break
            equation = int(equation_value)
            colouring = engine.indexed_colouring(equation)
            code = int(
                local_codes(
                    np.array([equation], dtype=np.int64),
                    cycles[triple_cycle_id],
                )[0]
            )
            if (
                code not in triple_needed_codes
                or code in fork_by_cycle_code[triple_cycle_id]
            ):
                continue
            extras = tuple(
                matching_id
                for matching_id in ids_at(
                    equation, triple_rich_size
                )
                if matching_id not in full_only
            )
            if len(extras) != 2 * args.extended_pair_count + 1:
                raise AssertionError("extended-rich extra count changed")
            available = []
            for first, second in itertools.combinations(extras, 2):
                signature = engine.relation_signature(
                    matchings[first],
                    matchings[second],
                    colouring,
                    labels,
                )
                origin = triple_origin_by_key.get((code, signature))
                if origin is not None:
                    available.append(
                        (
                            first,
                            second,
                            signature,
                            origin[0],
                            code,
                            origin[1],
                            origin[2],
                        )
                    )
            chosen = pair_cover_with_survivor(extras, available)
            if chosen is None:
                continue
            used = {
                matching_id
                for row in chosen
                for matching_id in row[:2]
            }
            survivor_id = next(
                matching_id
                for matching_id in extras
                if matching_id not in used
            )
            fork_by_cycle_code[triple_cycle_id][code] = {
                "cycle": list(cycles[triple_cycle_id]),
                "cycle_local_code": code,
                "pair_count": args.extended_pair_count,
                "pair_equations": [
                    {
                        "equation_index": row[3],
                        "matchings": [row[5], row[6]],
                        "rich_matchings": [row[0], row[1]],
                        "relation_signature": [
                            list(item) for item in row[2]
                        ],
                    }
                    for row in chosen
                ],
                "rich_equation_index": equation,
                "rich_activity": list(
                    ids_at(equation, triple_rich_size)
                ),
                "rich_paired_matchings": [
                    [row[0], row[1]] for row in chosen
                ],
                "rich_surviving_matching": survivor_id,
            }
            triple_forks_found += 1

    base_mask = np.ones(len(base_indices), dtype=bool)
    base_codes = []
    for cycle_id, cycle in enumerate(cycles):
        codes = local_codes(base_indices, cycle)
        base_codes.append(codes)
        good_codes = np.array(
            sorted(fork_by_cycle_code[cycle_id]), dtype=np.int64
        )
        if len(good_codes) == 0:
            base_mask[:] = False
        else:
            base_mask &= np.isin(codes, good_codes)
    good_positions = np.flatnonzero(base_mask)
    certificate = global_forced_cycle_certificate
    if certificate is None and len(good_positions):
        position = int(good_positions[0])
        base_equation = int(base_indices[position])
        alternatives = [
            fork_by_cycle_code[cycle_id][
                int(base_codes[cycle_id][position])
            ]
            for cycle_id in range(len(cycles))
        ]
        certificate = {
            "certificate_mode": (
                "even_cycle_factor_two_pair_survivor_fork"
            ),
            "logical_chain": (
                "the base full-factor product chooses a vanishing "
                "cycle binomial; the two pair equations force two "
                "matching-pair cancellations; the rich equation "
                "then has one nonzero surviving monomial"
            ),
            "base_equation_index": base_equation,
            "base_colouring": list(
                engine.indexed_colouring(base_equation)
            ),
            "base_activity": list(
                ids_at(base_equation, baseline)
            ),
            "alternatives": alternatives,
        }

    payload = {
        "status": (
            "even_cycle_double_pair_fork"
            if certificate is not None
            else "even_cycle_double_pair_fork_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": baseline,
        "full_only_base_colourings": len(base_indices),
        "two_extra_target_colourings": len(pair_indices),
        "five_extra_target_colourings": len(rich_indices),
        "seven_extra_target_colourings": len(triple_rich_indices),
        "extended_pair_count": args.extended_pair_count,
        "extended_extra_target_size": (
            2 * args.extended_pair_count + 1
        ),
        "extended_target_colourings": len(triple_rich_indices),
        "candidate_rich_relation_keys_by_cycle": [
            len(rows) for rows in candidate_keys
        ],
        "matched_pair_relation_keys_by_cycle": [
            len(rows) for rows in origin_by_key
        ],
        "rich_fork_local_codes_by_cycle": [
            len(rows) for rows in fork_by_cycle_code
        ],
        "triple_pair_cycle": args.triple_pair_cycle,
        "triple_pair_needed_local_codes": len(
            triple_needed_codes
        ),
        "triple_pair_forks_found": triple_forks_found,
        "global_forced_cycle_certificate_found": (
            global_forced_cycle_certificate is not None
        ),
        "forced_local_code_coverage_by_cycle": (
            forced_local_code_coverage_by_cycle
        ),
        "forced_local_codes_by_cycle": (
            forced_local_codes_by_cycle
        ),
        "conditional_fork_local_codes_by_cycle": [
            sorted(rows) for rows in fork_by_cycle_code
        ],
        "conditional_fork_certificates_by_cycle": [
            {
                str(code): row
                for code, row in sorted(rows.items())
            }
            for rows in fork_by_cycle_code
        ],
        "global_rich_pair_fork_by_cycle": (
            global_rich_pair_fork_by_cycle
        ),
        "matching_extensions_accumulated": total_extensions,
        "elapsed_seconds": time.perf_counter() - started,
        "certificate": certificate,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
