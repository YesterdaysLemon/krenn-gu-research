"""Independent packed-array audit of an exact-three-partial P5 catalogue."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import audit_p5_all_full_boundary_obstruction as ALL_FULL
import audit_p5_exact_two_partial_boundary as TWO
import verify_p5_pair_signature_catalogue_coverage as COVERAGE


PARTIAL_MASKS = (3, 5, 6)
EXPECTED_LABELLED = 25_194_240


def labelled_valid_supports(
    shape: str,
    valid_local_supports: set[tuple[int, ...]],
    min_available_percent: float,
) -> set[int]:
    edges = tuple(sorted(ALL_FULL.full_edges(shape)))
    positions_by_source = tuple(
        tuple(
            mode
            for mode in TWO.MODES
            if (mode, source) not in edges
        )
        for source in TWO.SOURCES
    )
    valid: set[int] = set()
    generated = 0
    for assignments in itertools.product(
        ALL_FULL.PERMUTATIONS_3, repeat=5
    ):
        base = [
            7 if (mode, source) in edges else 0
            for mode in TWO.MODES
            for source in TWO.SOURCES
        ]
        for source, colours in enumerate(assignments):
            for mode, colour in zip(
                positions_by_source[source], colours, strict=True
            ):
                base[5 * mode + source] = 1 << colour
        base_packed = TWO.pack(base)
        base_rows = tuple(
            tuple(base[5 * mode : 5 * mode + 5])
            for mode in TWO.MODES
        )
        for selected_edges in itertools.combinations(edges, 3):
            positions = tuple(
                5 * mode + source for mode, source in selected_edges
            )
            cleared = base_packed
            for position in positions:
                cleared &= ~(
                    TWO.POSITION_MASK << (TWO.MASK_BITS * position)
                )
            for masks in itertools.product(PARTIAL_MASKS, repeat=3):
                candidate = cleared
                for position, mask in zip(
                    positions, masks, strict=True
                ):
                    candidate |= mask << (
                        TWO.MASK_BITS * position
                    )

                affected_modes = {
                    mode for mode, _source in selected_edges
                }
                locally_valid = True
                for mode in TWO.MODES:
                    if mode not in affected_modes:
                        row = base_rows[mode]
                    else:
                        row_list = list(base_rows[mode])
                        for (
                            selected_mode,
                            selected_source,
                        ), mask in zip(
                            selected_edges, masks, strict=True
                        ):
                            if selected_mode == mode:
                                row_list[selected_source] = mask
                        row = tuple(row_list)
                    if row not in valid_local_supports:
                        locally_valid = False
                        break
                if locally_valid:
                    if candidate in valid:
                        raise AssertionError(
                            "labelled support was generated twice"
                        )
                    valid.add(candidate)
                generated += 1
                if generated % 100_000 == 0:
                    available = TWO.available_memory_percent()
                    print(
                        json.dumps(
                            {
                                "phase": "labelled_generation",
                                "shape": shape,
                                "generated": generated,
                                "valid_unique": len(valid),
                                "available_percent": round(
                                    available, 3
                                ),
                            }
                        ),
                        flush=True,
                    )
                    if available < min_available_percent:
                        raise MemoryError(
                            "available memory crossed configured floor"
                        )
    if generated != EXPECTED_LABELLED:
        raise AssertionError(
            f"labelled exact-three count changed: {generated}"
        )
    return valid


def canonical_support(
    support: int,
    actions: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> int:
    return min(
        TWO.transform(support, positions, masks)
        for positions, masks in actions
    )


def expected_catalogue_supports(
    path: Path,
    shape: str,
    actions: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> set[int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if (
        payload.get("status") != "COMPLETE"
        or payload.get("shape") != shape
        or payload.get("partial_cells") != 3
        or payload.get("support_orbits") != len(payload.get("cases", []))
    ):
        raise ValueError("SAT catalogue metadata is incomplete")
    output = set()
    for case in payload["cases"]:
        if case.get("shape", shape) != shape:
            raise ValueError("SAT catalogue shape changed")
        flat = [
            mask
            for row in case["supports"]
            for mask in row
        ]
        packed = TWO.pack(flat)
        canonical = canonical_support(packed, actions)
        if canonical in output:
            raise ValueError("SAT catalogue repeats a support orbit")
        output.add(canonical)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=ALL_FULL.SHAPES, required=True)
    parser.add_argument("--catalogue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if not 15 <= args.min_available_percent < 100:
        raise ValueError("memory floor must be at least 15 and below 100")

    catalogue = COVERAGE.finite_field_local_signatures()
    by_support: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, signature in enumerate(catalogue):
        by_support[signature[0]].append(index)
    valid_local_supports = set(by_support)
    actions = TWO.transformed_actions(args.shape)

    valid = labelled_valid_supports(
        args.shape,
        valid_local_supports,
        args.min_available_percent,
    )
    print(
        json.dumps(
            {
                "phase": "orbit_partition",
                "shape": args.shape,
                "valid_labelled": len(valid),
                "actions": len(actions),
                "available_percent": round(
                    TWO.available_memory_percent(), 3
                ),
            }
        ),
        flush=True,
    )
    valid_orbits = TWO.orbit_partition(valid, actions)
    del valid

    viable_cases = []
    pair_viable_cases = 0
    viable_tuples = 0
    support_exclusions = Counter()
    orbit_histogram = Counter()
    for orbit_index, (representative, orbit_size) in enumerate(valid_orbits):
        support_rows = TWO.rows(representative)
        viable = ALL_FULL.viable_tuples(
            support_rows, catalogue, by_support
        )
        orbit_histogram[orbit_size] += 1
        if not viable:
            continue
        pair_viable_cases += 1
        viable_tuples += len(viable)
        pure = TWO.has_pure_permanent(support_rows)
        mixed = TWO.avoids_unique_mixed_permanent(support_rows)
        if not pure:
            support_exclusions["missing_pure_permanent"] += 1
        if not mixed:
            support_exclusions["unique_mixed_permanent"] += 1
        if not (pure and mixed):
            continue
        viable_cases.append(
            {
                "shape": args.shape,
                "audit_orbit_index": orbit_index,
                "orbit_size": orbit_size,
                "supports": support_rows,
                "viable_signature_tuples": len(viable),
                "witness_signature_indices": viable[0],
            }
        )

    observed = {
        TWO.pack(
            [
                mask
                for row in case["supports"]
                for mask in row
            ]
        )
        for case in viable_cases
    }
    expected = expected_catalogue_supports(
        args.catalogue, args.shape, actions
    )
    if observed != expected:
        raise AssertionError(
            "independent packed audit disagrees with SAT catalogue: "
            f"missing={len(expected - observed)}, "
            f"extra={len(observed - expected)}"
        )

    result = {
        "verified": True,
        "scope": "exactly three partial noncoordinate cells",
        "shape": args.shape,
        "catalogue_pair_signatures": len(catalogue),
        "labelled_supports": EXPECTED_LABELLED,
        "locally_valid_support_orbits": len(valid_orbits),
        "valid_orbit_size_histogram": dict(
            sorted(orbit_histogram.items())
        ),
        "pair_quota_viable_support_orbits": pair_viable_cases,
        "pair_quota_viable_signature_tuples": viable_tuples,
        "support_semantic_exclusion_histogram": dict(
            sorted(support_exclusions.items())
        ),
        "support_semantic_viable_support_orbits": len(viable_cases),
        "sat_catalogue_support_orbits": len(expected),
        "catalogue_exact_match": True,
        "cases": viable_cases,
    }
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key != "cases"
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
