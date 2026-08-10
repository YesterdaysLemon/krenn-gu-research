"""Audit the exact-one-partial-cell P5 boundary up to symmetry."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/frontier")

import audit_p5_all_full_boundary_obstruction as ALL_FULL
import verify_p5_pair_signature_catalogue_coverage as COVERAGE


MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PARTIAL_MASKS = (3, 5, 6)


def transform(
    support: tuple[int, ...],
    mode_permutation: tuple[int, ...],
    source_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    image = [0] * 25
    for mode in MODES:
        for source in SOURCES:
            image[
                5 * mode_permutation[mode] + source_permutation[source]
            ] = ALL_FULL.colour_mask(
                support[5 * mode + source], colour_permutation
            )
    return tuple(image)


def labelled_supports(
    shape: str,
    valid_local_supports: set[tuple[int, ...]] | None,
) -> set[tuple[int, ...]]:
    edges = ALL_FULL.full_edges(shape)
    positions_by_source = tuple(
        tuple(
            mode
            for mode in MODES
            if (mode, source) not in edges
        )
        for source in SOURCES
    )
    output = set()
    for assignments in itertools.product(
        ALL_FULL.PERMUTATIONS_3, repeat=5
    ):
        base = [7 if (mode, source) in edges else 0
                for mode in MODES for source in SOURCES]
        for source, colours in enumerate(assignments):
            for mode, colour in zip(
                positions_by_source[source], colours, strict=True
            ):
                base[5 * mode + source] = 1 << colour
        for mode, source in edges:
            position = 5 * mode + source
            for mask in PARTIAL_MASKS:
                candidate = list(base)
                candidate[position] = mask
                local = tuple(candidate[5 * mode : 5 * mode + 5])
                if (
                    valid_local_supports is None
                    or local in valid_local_supports
                ):
                    output.add(tuple(candidate))
    return output


def orbit_partition(
    supports: set[tuple[int, ...]],
    group: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> list[tuple[tuple[int, ...], int]]:
    remaining = set(supports)
    output = []
    while remaining:
        representative = min(remaining)
        orbit = {
            transform(
                representative,
                mode_permutation,
                source_permutation,
                colour_permutation,
            )
            for mode_permutation, source_permutation in group
            for colour_permutation in ALL_FULL.PERMUTATIONS_3
        }
        if not orbit.issubset(supports):
            raise AssertionError("boundary set is not symmetry invariant")
        output.append((min(orbit), len(orbit)))
        remaining.difference_update(orbit)
    return sorted(output)


def rows(support: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        support[5 * mode : 5 * mode + 5] for mode in MODES
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            Path(__file__).resolve().parent
            / "tmp"
            / "p5_one_partial_boundary_audit.json"
        ),
    )
    args = parser.parse_args()

    catalogue = COVERAGE.finite_field_local_signatures()
    by_support: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, signature in enumerate(catalogue):
        by_support[signature[0]].append(index)
    valid_local_supports = set(by_support)

    result = {
        "verified": True,
        "scope": "exactly one partial noncoordinate cell",
        "catalogue_pair_signatures": len(catalogue),
    }
    cases = []
    for shape in ALL_FULL.SHAPES:
        group = ALL_FULL.automorphisms(ALL_FULL.full_edges(shape))
        labelled_all = labelled_supports(shape, None)
        labelled = labelled_supports(shape, valid_local_supports)
        all_orbits = orbit_partition(labelled_all, group)
        orbits = orbit_partition(labelled, group)
        viable_orbits = 0
        viable_tuples = 0
        histogram = Counter()
        candidate_histogram = Counter()
        for orbit_index, (representative, orbit_size) in enumerate(orbits):
            support_rows = rows(representative)
            candidate_product = 1
            for row in support_rows:
                candidate_product *= len(by_support[row])
            viable = ALL_FULL.viable_tuples(
                support_rows, catalogue, by_support
            )
            histogram[orbit_size] += 1
            candidate_histogram[candidate_product] += 1
            if viable:
                viable_orbits += 1
                viable_tuples += len(viable)
                cases.append(
                    {
                        "shape": shape,
                        "orbit_index": orbit_index,
                        "orbit_size": orbit_size,
                        "supports": support_rows,
                        "viable_signature_tuples": len(viable),
                        "witness_signature_indices": viable[0],
                    }
                )
        result[shape] = {
            "labelled_supports": len(labelled_all),
            "labelled_valid_supports": len(labelled),
            "support_orbits": len(all_orbits),
            "locally_invalid_support_orbits": (
                len(all_orbits) - len(orbits)
            ),
            "locally_valid_support_orbits": len(orbits),
            "valid_orbit_size_histogram": dict(
                sorted(histogram.items())
            ),
            "candidate_product_histogram": dict(
                sorted(candidate_histogram.items())
            ),
            "pair_quota_viable_support_orbits": viable_orbits,
            "pair_quota_viable_signature_tuples": viable_tuples,
        }
    result["support_orbits"] = sum(
        result[shape]["support_orbits"] for shape in ALL_FULL.SHAPES
    )
    result["locally_invalid_support_orbits"] = sum(
        result[shape]["locally_invalid_support_orbits"]
        for shape in ALL_FULL.SHAPES
    )
    result["locally_valid_support_orbits"] = sum(
        result[shape]["locally_valid_support_orbits"]
        for shape in ALL_FULL.SHAPES
    )
    result["pair_quota_excluded_support_orbits"] = sum(
        result[shape]["locally_valid_support_orbits"]
        - result[shape]["pair_quota_viable_support_orbits"]
        for shape in ALL_FULL.SHAPES
    )
    result["pair_quota_viable_support_orbits"] = len(cases)
    result["pair_quota_viable_signature_tuples"] = sum(
        result[shape]["pair_quota_viable_signature_tuples"]
        for shape in ALL_FULL.SHAPES
    )
    observed = (
        result["support_orbits"],
        result["locally_invalid_support_orbits"],
        result["locally_valid_support_orbits"],
        result["pair_quota_excluded_support_orbits"],
        result["pair_quota_viable_support_orbits"],
        result["pair_quota_viable_signature_tuples"],
        result["c10"]["support_orbits"],
        result["c10"]["locally_invalid_support_orbits"],
        result["c10"]["pair_quota_viable_support_orbits"],
        result["c4c6"]["support_orbits"],
        result["c4c6"]["locally_invalid_support_orbits"],
        result["c4c6"]["pair_quota_viable_support_orbits"],
    )
    expected = (
        5676,
        224,
        5452,
        5133,
        319,
        6575,
        3888,
        144,
        236,
        1788,
        80,
        83,
    )
    if observed != expected:
        raise AssertionError(
            f"one-partial census changed: {observed} != {expected}"
        )
    result["cases"] = cases
    args.output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in result.items() if key != "cases"},
            indent=2,
        )
    )
    print(f"support cases: {len(cases)}")


if __name__ == "__main__":
    main()
