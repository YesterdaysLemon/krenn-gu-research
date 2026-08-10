"""Direct exact-two-partial P5 support audit using packed support arrays."""

from __future__ import annotations

import argparse
import ctypes
import itertools
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/boundaries")
expose_claim_package(REPO_ROOT, "claims/p5/frontier")

import audit_p5_all_full_boundary_obstruction as ALL_FULL
import verify_p5_pair_signature_catalogue_coverage as COVERAGE

MODES = tuple(range(5))
SOURCES = tuple(range(5))
PARTIAL_MASKS = (3, 5, 6)
MASK_BITS = 3
POSITION_MASK = 7
COLOURS = tuple(range(3))
COLOURINGS = tuple(itertools.product(COLOURS, repeat=5))
EXPECTED_SUMMARIES = {
    "c10": {
        "labelled_supports": 3_149_280,
        "support_orbits": 52_758,
        "locally_invalid_support_orbits": 7_884,
        "locally_valid_support_orbits": 44_874,
        "valid_orbit_size_histogram": {30: 452, 60: 44_422},
        "pair_quota_excluded_support_orbits": 41_655,
        "pair_quota_viable_support_orbits": 3_219,
        "pair_quota_viable_signature_tuples": 35_165,
        "support_semantic_exclusion_histogram": {
            "missing_pure_permanent": 8,
            "unique_mixed_permanent": 1_006,
        },
        "support_semantic_viable_support_orbits": 2_205,
    },
    "c4c6": {
        "labelled_supports": 3_149_280,
        "support_orbits": 23_340,
        "locally_invalid_support_orbits": 3_730,
        "locally_valid_support_orbits": 19_610,
        "valid_orbit_size_histogram": {
            36: 44,
            72: 1_946,
            144: 17_620,
        },
        "pair_quota_excluded_support_orbits": 18_256,
        "pair_quota_viable_support_orbits": 1_354,
        "pair_quota_viable_signature_tuples": 14_944,
        "support_semantic_exclusion_histogram": {
            "missing_pure_permanent": 6,
            "unique_mixed_permanent": 245,
        },
        "support_semantic_viable_support_orbits": 1_103,
    },
}


def available_memory_percent() -> float:
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_ulong),
                ("memory_load", ctypes.c_ulong),
                ("total_physical", ctypes.c_ulonglong),
                ("available_physical", ctypes.c_ulonglong),
                ("total_page_file", ctypes.c_ulonglong),
                ("available_page_file", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong),
                ("available_virtual", ctypes.c_ulonglong),
                ("available_extended_virtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(
            ctypes.byref(status)
        ):
            raise OSError("GlobalMemoryStatusEx failed")
        return (
            100.0
            * status.available_physical
            / status.total_physical
        )

    meminfo = {}
    for line in Path("/proc/meminfo").read_text(
        encoding="utf-8"
    ).splitlines():
        key, value = line.split(":", 1)
        meminfo[key] = int(value.strip().split()[0])
    return 100.0 * meminfo["MemAvailable"] / meminfo["MemTotal"]


def pack(support: list[int] | tuple[int, ...]) -> int:
    return sum(
        mask << (MASK_BITS * position)
        for position, mask in enumerate(support)
    )


def unpack(value: int) -> tuple[int, ...]:
    return tuple(
        (value >> (MASK_BITS * position)) & POSITION_MASK
        for position in range(25)
    )


def transformed_actions(
    shape: str,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    actions = []
    group = ALL_FULL.automorphisms(ALL_FULL.full_edges(shape))
    for mode_permutation, source_permutation in group:
        positions = tuple(
            5 * mode_permutation[mode] + source_permutation[source]
            for mode in MODES
            for source in SOURCES
        )
        for colour_permutation in ALL_FULL.PERMUTATIONS_3:
            masks = tuple(
                ALL_FULL.colour_mask(mask, colour_permutation)
                for mask in range(8)
            )
            actions.append((positions, masks))
    return tuple(actions)


def transform(
    support: int,
    positions: tuple[int, ...],
    masks: tuple[int, ...],
) -> int:
    image = 0
    for old_position, new_position in enumerate(positions):
        mask = (
            support >> (MASK_BITS * old_position)
        ) & POSITION_MASK
        image |= masks[mask] << (MASK_BITS * new_position)
    return image


def orbit_partition(
    supports: set[int],
    actions: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> list[tuple[int, int]]:
    remaining = set(supports)
    output = []
    for representative in sorted(supports):
        if representative not in remaining:
            continue
        orbit = {
            transform(representative, positions, masks)
            for positions, masks in actions
        }
        if not orbit.issubset(supports):
            raise AssertionError("support set is not symmetry invariant")
        output.append((representative, len(orbit)))
        remaining.difference_update(orbit)
    if remaining:
        raise AssertionError("orbit partition left unvisited supports")
    return output


def labelled_supports(
    shape: str,
    valid_local_supports: set[tuple[int, ...]],
    min_available_percent: float,
) -> tuple[set[int], set[int]]:
    edges = tuple(sorted(ALL_FULL.full_edges(shape)))
    positions_by_source = tuple(
        tuple(
            mode
            for mode in MODES
            if (mode, source) not in edges
        )
        for source in SOURCES
    )
    raw = set()
    valid = set()
    generated = 0
    for assignments in itertools.product(
        ALL_FULL.PERMUTATIONS_3, repeat=5
    ):
        base = [
            7 if (mode, source) in edges else 0
            for mode in MODES
            for source in SOURCES
        ]
        for source, colours in enumerate(assignments):
            for mode, colour in zip(
                positions_by_source[source], colours, strict=True
            ):
                base[5 * mode + source] = 1 << colour
        base_packed = pack(base)
        base_rows = tuple(
            tuple(base[5 * mode : 5 * mode + 5])
            for mode in MODES
        )
        for (mode_a, source_a), (mode_b, source_b) in (
            itertools.combinations(edges, 2)
        ):
            position_a = 5 * mode_a + source_a
            position_b = 5 * mode_b + source_b
            cleared = (
                base_packed
                & ~(POSITION_MASK << (MASK_BITS * position_a))
                & ~(POSITION_MASK << (MASK_BITS * position_b))
            )
            for mask_a, mask_b in itertools.product(
                PARTIAL_MASKS, repeat=2
            ):
                candidate = (
                    cleared
                    | (mask_a << (MASK_BITS * position_a))
                    | (mask_b << (MASK_BITS * position_b))
                )
                raw.add(candidate)

                affected_modes = {mode_a, mode_b}
                locally_valid = True
                for mode in MODES:
                    if mode not in affected_modes:
                        row = base_rows[mode]
                    else:
                        row_list = list(base_rows[mode])
                        if mode == mode_a:
                            row_list[source_a] = mask_a
                        if mode == mode_b:
                            row_list[source_b] = mask_b
                        row = tuple(row_list)
                    if row not in valid_local_supports:
                        locally_valid = False
                        break
                if locally_valid:
                    valid.add(candidate)
                generated += 1
                if generated % 100_000 == 0:
                    available = available_memory_percent()
                    print(
                        json.dumps(
                            {
                                "shape": shape,
                                "generated": generated,
                                "raw_unique": len(raw),
                                "valid_unique": len(valid),
                                "available_percent": round(available, 3),
                            }
                        ),
                        flush=True,
                    )
                    if available < min_available_percent:
                        raise MemoryError(
                            "available memory crossed the configured floor"
                        )
    if generated != 3_149_280 or len(raw) != generated:
        raise AssertionError(
            f"labelled exact-two count changed: {generated}, {len(raw)}"
        )
    return raw, valid


def rows(support: int) -> tuple[tuple[int, ...], ...]:
    flat = unpack(support)
    return tuple(
        flat[5 * mode : 5 * mode + 5] for mode in MODES
    )


def has_pure_permanent(
    support_rows: tuple[tuple[int, ...], ...],
) -> bool:
    return all(
        any(
            all(
                support_rows[mode][permutation[mode]]
                & (1 << colour)
                for mode in MODES
            )
            for permutation in ALL_FULL.PERMUTATIONS_5
        )
        for colour in COLOURS
    )


def avoids_unique_mixed_permanent(
    support_rows: tuple[tuple[int, ...], ...],
) -> bool:
    return all(
        sum(
            all(
                support_rows[mode][permutation[mode]]
                & (1 << colouring[mode])
                for mode in MODES
            )
            for permutation in ALL_FULL.PERMUTATIONS_5
        )
        != 1
        for colouring in COLOURINGS
        if len(set(colouring)) > 1
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=ALL_FULL.SHAPES, required=True)
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

    actions = transformed_actions(args.shape)
    raw, valid = labelled_supports(
        args.shape,
        valid_local_supports,
        args.min_available_percent,
    )
    print(
        json.dumps(
            {
                "phase": "orbit_partition",
                "shape": args.shape,
                "raw_labelled": len(raw),
                "valid_labelled": len(valid),
                "actions": len(actions),
                "available_percent": round(
                    available_memory_percent(), 3
                ),
            }
        ),
        flush=True,
    )
    raw_orbits = orbit_partition(raw, actions)
    del raw
    valid_orbits = orbit_partition(valid, actions)
    del valid

    viable_cases = []
    pair_viable_cases = 0
    viable_tuples = 0
    support_exclusions = Counter()
    orbit_histogram = Counter()
    for orbit_index, (representative, orbit_size) in enumerate(valid_orbits):
        support_rows = rows(representative)
        viable = ALL_FULL.viable_tuples(
            support_rows, catalogue, by_support
        )
        orbit_histogram[orbit_size] += 1
        if viable:
            pair_viable_cases += 1
            viable_tuples += len(viable)
            pure = has_pure_permanent(support_rows)
            mixed = avoids_unique_mixed_permanent(support_rows)
            if not pure:
                support_exclusions["missing_pure_permanent"] += 1
            if not mixed:
                support_exclusions["unique_mixed_permanent"] += 1
            if not (pure and mixed):
                continue
            viable_cases.append(
                {
                    "shape": args.shape,
                    "orbit_index": orbit_index,
                    "orbit_size": orbit_size,
                    "supports": support_rows,
                    "viable_signature_tuples": len(viable),
                    "witness_signature_indices": viable[0],
                }
            )
    result = {
        "verified": True,
        "scope": "exactly two partial noncoordinate cells",
        "shape": args.shape,
        "catalogue_pair_signatures": len(catalogue),
        "labelled_supports": 3_149_280,
        "support_orbits": len(raw_orbits),
        "locally_invalid_support_orbits": (
            len(raw_orbits) - len(valid_orbits)
        ),
        "locally_valid_support_orbits": len(valid_orbits),
        "valid_orbit_size_histogram": dict(
            sorted(orbit_histogram.items())
        ),
        "pair_quota_excluded_support_orbits": (
            len(valid_orbits) - pair_viable_cases
        ),
        "pair_quota_viable_support_orbits": pair_viable_cases,
        "pair_quota_viable_signature_tuples": viable_tuples,
        "support_semantic_exclusion_histogram": dict(
            sorted(support_exclusions.items())
        ),
        "support_semantic_viable_support_orbits": len(viable_cases),
        "cases": viable_cases,
    }
    expected = EXPECTED_SUMMARIES[args.shape]
    observed = {
        key: result.get(key)
        for key in expected
    }
    if observed != expected:
        raise AssertionError(
            f"exact-two census changed: {observed} != {expected}"
        )
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {key: value for key, value in result.items() if key != "cases"},
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
