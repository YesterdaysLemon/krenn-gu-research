"""Independent finite audit of the entire all-full P5 boundary."""

from __future__ import annotations

import argparse
import itertools
import json
import math
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

import audit_p5_all_full_tricolour_obstruction as PROPER
from krenn_gu import p5_pair_catalogue as COVERAGE


ROOT = Path(__file__).resolve().parent
MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PAIRS = tuple(itertools.combinations(SOURCES, 2))
PERMUTATIONS_5 = tuple(itertools.permutations(range(5)))
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))
SHAPES = {
    "c10": ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
    "c4c6": ((0, 1), (0, 1), (2, 3), (3, 4), (2, 4)),
}
EXPECTED_VIABLE = {
    ("c10", 82): 27,
    ("c10", 84): 9,
    ("c10", 89): 3,
    ("c10", 96): 3,
    ("c10", 118): 27,
    ("c10", 119): 27,
    ("c10", 124): 3,
    ("c10", 135): 27,
    ("c10", 146): 243,
    ("c10", 147): 243,
    ("c4c6", 39): 45,
    ("c4c6", 68): 27,
    ("c4c6", 76): 243,
}


def colour_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        ((mask >> colour) & 1) << permutation[colour]
        for colour in COLOURS
    )


def full_edges(shape: str) -> frozenset[tuple[int, int]]:
    return frozenset(
        (mode, source)
        for mode, sources in enumerate(SHAPES[shape])
        for source in sources
    )


def automorphisms(
    edges: frozenset[tuple[int, int]],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    output = []
    for mode_permutation in PERMUTATIONS_5:
        for source_permutation in PERMUTATIONS_5:
            image = frozenset(
                (
                    mode_permutation[mode],
                    source_permutation[source],
                )
                for mode, source in edges
            )
            if image == edges:
                output.append((mode_permutation, source_permutation))
    return tuple(output)


def enumerate_source_proper(
    edges: frozenset[tuple[int, int]],
) -> tuple[tuple[int, ...], ...]:
    positions_by_source = tuple(
        tuple(
            mode
            for mode in MODES
            if (mode, source) not in edges
        )
        for source in SOURCES
    )
    if any(len(positions) != 3 for positions in positions_by_source):
        raise AssertionError("full graph is not two-regular")
    patterns = []
    for assignments in itertools.product(PERMUTATIONS_3, repeat=5):
        pattern = [-1] * 25
        for source, colours in enumerate(assignments):
            for mode, colour in zip(
                positions_by_source[source], colours, strict=True
            ):
                pattern[5 * mode + source] = colour
        patterns.append(tuple(pattern))
    return tuple(patterns)


def transform(
    pattern: tuple[int, ...],
    mode_permutation: tuple[int, ...],
    source_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    image = [-1] * 25
    for mode in MODES:
        for source in SOURCES:
            value = pattern[5 * mode + source]
            image[
                5 * mode_permutation[mode]
                + source_permutation[source]
            ] = -1 if value < 0 else colour_permutation[value]
    return tuple(image)


def canonical(
    pattern: tuple[int, ...],
    group: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> tuple[int, ...]:
    return min(
        transform(
            pattern,
            mode_permutation,
            source_permutation,
            colour_permutation,
        )
        for mode_permutation, source_permutation in group
        for colour_permutation in PERMUTATIONS_3
    )


def supports(pattern: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            7
            if pattern[5 * mode + source] < 0
            else 1 << pattern[5 * mode + source]
            for source in SOURCES
        )
        for mode in MODES
    )


def support_pattern(
    support_rows: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    return tuple(
        -1
        if support_rows[mode][source] == 7
        else support_rows[mode][source].bit_length() - 1
        for mode in MODES
        for source in SOURCES
    )


def row_proper(pattern: tuple[int, ...]) -> bool:
    return all(
        sorted(
            pattern[5 * mode + source]
            for source in SOURCES
            if pattern[5 * mode + source] >= 0
        )
        == [0, 1, 2]
        for mode in MODES
    )


def viable_tuples(
    support_rows: tuple[tuple[int, ...], ...],
    catalogue: tuple[tuple, ...],
    by_support: dict[tuple[int, ...], list[int]],
) -> tuple[tuple[int, ...], ...]:
    output = []
    for indices in itertools.product(
        *(by_support[support_rows[mode]] for mode in MODES)
    ):
        signatures = tuple(catalogue[index] for index in indices)
        if all(
            sum(
                bool(
                    signatures[mode][1][pair_index]
                    & (1 << colour)
                )
                for mode in MODES
            )
            >= 2
            for pair_index in range(len(PAIRS))
            for colour in COLOURS
        ):
            output.append(indices)
    return tuple(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tmp" / "p5_all_full_boundary_audit.json",
    )
    args = parser.parse_args()
    catalogue = COVERAGE.finite_field_local_signatures()
    if len(catalogue) != 6495:
        raise AssertionError("pair-signature catalogue size changed")
    pair_signatures = {
        (signature[0], signature[1][: len(PAIRS)])
        for signature in catalogue
    }
    if len(pair_signatures) != 6495:
        raise AssertionError("catalogue repeats a pair signature")
    by_support: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, signature in enumerate(catalogue):
        by_support[signature[0]].append(index)

    descriptors = []
    shape_results = {}
    proper_canonical = set()
    cases = []
    for shape in SHAPES:
        edges = full_edges(shape)
        group = automorphisms(edges)
        patterns = enumerate_source_proper(edges)
        orbit_counts = Counter(
            canonical(pattern, group) for pattern in patterns
        )
        for orbit_index, (representative, orbit_size) in enumerate(
            sorted(orbit_counts.items())
        ):
            support_rows = supports(representative)
            viable = viable_tuples(
                support_rows, catalogue, by_support
            )
            is_proper = row_proper(representative)
            item = {
                "shape": shape,
                "orbit_index": orbit_index,
                "orbit_size": orbit_size,
                "row_proper": is_proper,
                "supports": support_rows,
                "candidate_product": (
                    math.prod(
                        len(by_support[row]) for row in support_rows
                    )
                ),
                "viable_signature_tuples": len(viable),
            }
            descriptors.append(item)
            if viable:
                expected = EXPECTED_VIABLE.get((shape, orbit_index))
                if expected != len(viable):
                    raise AssertionError(
                        f"viability count changed for {shape} "
                        f"orbit {orbit_index}: {len(viable)} != {expected}"
                    )
                if is_proper:
                    proper_canonical.add(
                        canonical(representative, group)
                    )
                else:
                    for indices in viable:
                        cases.append(
                            {
                                "shape": shape,
                                "orbit_index": orbit_index,
                                "supports": support_rows,
                                "signature_indices": indices,
                            }
                        )
        shape_results[shape] = {
            "automorphisms": len(group),
            "labelled_source_proper_colourings": len(patterns),
            "orbits": len(orbit_counts),
            "orbit_size_histogram": dict(
                sorted(Counter(orbit_counts.values()).items())
            ),
            "proper_row_orbits": sum(
                row_proper(representative)
                for representative in orbit_counts
            ),
        }

    previous_proper = set()
    for name, support_rows in PROPER.SUPPORTS.items():
        shape = "c10" if name.startswith("c10") else "c4c6"
        previous_proper.add(
            canonical(
                support_pattern(support_rows),
                automorphisms(full_edges(shape)),
            )
        )
    if proper_canonical != previous_proper or len(proper_canonical) != 3:
        raise AssertionError("prior proper theorem does not cover proper set")

    viable_descriptors = [
        descriptor
        for descriptor in descriptors
        if descriptor["viable_signature_tuples"]
    ]
    result = {
        "verified": True,
        "scope": (
            "all-full exact-three-coordinate supports with source-column "
            "singleton colours 0,1,2"
        ),
        "catalogue_pair_signatures": len(pair_signatures),
        "shapes": shape_results,
        "support_orbits": len(descriptors),
        "nonproper_support_orbits": sum(
            not descriptor["row_proper"]
            for descriptor in descriptors
        ),
        "pair_quota_excluded_support_orbits": sum(
            not descriptor["viable_signature_tuples"]
            for descriptor in descriptors
        ),
        "pair_quota_viable_support_orbits": len(viable_descriptors),
        "proper_viable_support_orbits": sum(
            descriptor["row_proper"]
            for descriptor in viable_descriptors
        ),
        "nonproper_viable_support_orbits": sum(
            not descriptor["row_proper"]
            for descriptor in viable_descriptors
        ),
        "nonproper_viable_signature_tuples": len(cases),
        "proper_boundary_covered_by_prior_theorem": True,
        "viable_support_counts": {
            f"{shape}_{orbit}": count
            for (shape, orbit), count in sorted(EXPECTED_VIABLE.items())
        },
        "cases": cases,
    }
    expected_summary = (226, 223, 213, 13, 3, 10, 198)
    observed_summary = (
        result["support_orbits"],
        result["nonproper_support_orbits"],
        result["pair_quota_excluded_support_orbits"],
        result["pair_quota_viable_support_orbits"],
        result["proper_viable_support_orbits"],
        result["nonproper_viable_support_orbits"],
        result["nonproper_viable_signature_tuples"],
    )
    if observed_summary != expected_summary:
        raise AssertionError(
            f"all-full census changed: {observed_summary}"
        )
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    summary = {key: value for key, value in result.items() if key != "cases"}
    print(json.dumps(summary, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
