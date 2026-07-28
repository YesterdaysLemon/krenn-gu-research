"""Independent symmetry and transport audit for fixed P5 cycle branches."""

from __future__ import annotations

import argparse
import collections
import importlib.util
import itertools
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCAL_PROBE = ROOT / "tmp" / "probe_p5_tricolour_support_sat.py"
FIXED_PROBE = ROOT / "tmp" / "probe_p5_max3_coordinate_support.py"

LOCAL_SPEC = importlib.util.spec_from_file_location(
    "p5_local_symmetry_audit", LOCAL_PROBE
)
P5 = importlib.util.module_from_spec(LOCAL_SPEC)
assert LOCAL_SPEC.loader is not None
LOCAL_SPEC.loader.exec_module(P5)

FIXED_SPEC = importlib.util.spec_from_file_location(
    "p5_fixed_symmetry_under_test", FIXED_PROBE
)
FIXED = importlib.util.module_from_spec(FIXED_SPEC)
assert FIXED_SPEC.loader is not None
FIXED_SPEC.loader.exec_module(FIXED)

SHAPES = {
    "c10": ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
    "c4c6": ((0, 1), (0, 1), (2, 3), (3, 4), (2, 4)),
}


def shape_edges(shape: str) -> frozenset[tuple[int, int]]:
    return frozenset(
        (mode, source)
        for mode, sources in enumerate(SHAPES[shape])
        for source in sources
    )


def independent_automorphisms(
    shape: str,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    edges = shape_edges(shape)
    result = []
    for mode_permutation in itertools.permutations(range(5)):
        for source_permutation in itertools.permutations(range(5)):
            image = frozenset(
                (
                    mode_permutation[mode],
                    source_permutation[source],
                )
                for mode, source in edges
            )
            if image == edges:
                result.append((mode_permutation, source_permutation))
    return tuple(result)


def compose_permutations(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def assert_group(
    automorphisms: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> None:
    elements = set(automorphisms)
    identity = tuple(range(5))
    if (identity, identity) not in elements:
        raise AssertionError("shape automorphisms omit the identity")
    for left_modes, left_sources in elements:
        for right_modes, right_sources in elements:
            composition = (
                compose_permutations(left_modes, right_modes),
                compose_permutations(left_sources, right_sources),
            )
            if composition not in elements:
                raise AssertionError("shape automorphisms are not closed")


def independent_clause_transformer(
    pool: Any, allowed: tuple[tuple, ...]
):
    signature_index = {
        signature: index for index, signature in enumerate(allowed)
    }
    source_subsets = tuple(
        subset
        for size in (2, 3, 4)
        for subset in itertools.combinations(range(5), size)
    )
    subset_index = {
        subset: index for index, subset in enumerate(source_subsets)
    }
    cache: dict[tuple, int] = {}

    def transform_mask(mask: int, colours: tuple[int, ...]) -> int:
        result = 0
        for old_colour in range(3):
            if mask & (1 << old_colour):
                result |= 1 << colours[old_colour]
        return result

    def transform_signature(
        pattern_index: int,
        sources: tuple[int, ...],
        colours: tuple[int, ...],
    ) -> int:
        key = (pattern_index, sources, colours)
        if key in cache:
            return cache[key]
        support, incidence = allowed[pattern_index]
        new_support = [0] * 5
        for old_source in range(5):
            new_support[sources[old_source]] = transform_mask(
                support[old_source], colours
            )
        new_incidence = [0] * len(source_subsets)
        for old_index, old_subset in enumerate(source_subsets):
            image_subset = tuple(
                sorted(sources[source] for source in old_subset)
            )
            new_incidence[subset_index[image_subset]] = transform_mask(
                incidence[old_index], colours
            )
        transformed = (tuple(new_support), tuple(new_incidence))
        cache[key] = signature_index[transformed]
        return cache[key]

    def transform(
        clause: list[int],
        modes: tuple[int, ...],
        sources: tuple[int, ...],
        colours: tuple[int, ...],
    ) -> tuple[int, ...]:
        output = []
        for literal in clause:
            key = pool.obj(abs(literal))
            if key[0] == "x":
                _, mode, source, colour = key
                new_key = (
                    "x",
                    modes[mode],
                    sources[source],
                    colours[colour],
                )
            elif key[0] == "local_pattern":
                _, mode, pattern_index = key
                new_key = (
                    "local_pattern",
                    modes[mode],
                    transform_signature(
                        pattern_index, sources, colours
                    ),
                )
            else:
                raise AssertionError(
                    f"unsupported learned key {key[0]!r}"
                )
            new_variable = pool.id(new_key)
            output.append(
                new_variable if literal > 0 else -new_variable
            )
        return tuple(sorted(output))

    return transform


def support_edges(record: dict) -> frozenset[tuple[int, int]]:
    return frozenset(
        (mode, source)
        for mode, row in enumerate(record["supports"])
        for source, mask in enumerate(row)
        if int(mask) not in (1, 2, 4)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=tuple(SHAPES), required=True)
    parser.add_argument("--state", type=pathlib.Path, required=True)
    parser.add_argument("--general-state", type=pathlib.Path, required=True)
    args = parser.parse_args()

    allowed = P5.finite_field_local_signatures()
    _cnf, pool = P5.build_cnf(
        allowed, double_lex=False, pair_hierarchy=True
    )
    transform = independent_clause_transformer(pool, allowed)
    automorphisms = independent_automorphisms(args.shape)
    expected_size = {"c10": 10, "c4c6": 24}[args.shape]
    if len(automorphisms) != expected_size:
        raise AssertionError("independent automorphism count is wrong")
    assert_group(automorphisms)
    if set(automorphisms) != set(
        FIXED.shape_automorphisms(args.shape)
    ):
        raise AssertionError("discovery automorphism set differs")

    colour_permutations = tuple(itertools.permutations(range(3)))

    def independent_orbit(clause: list[int]) -> set[tuple[int, ...]]:
        return {
            transform(clause, modes, sources, colours)
            for modes, sources in automorphisms
            for colours in colour_permutations
        }

    state = json.loads(args.state.read_text(encoding="utf-8"))
    if state.get("shape") != args.shape:
        raise AssertionError("fixed state has the wrong shape")
    fixed_records = list(state["learned_records"])
    fixed_orbit_sizes: collections.Counter[int] = collections.Counter()
    target_edges = shape_edges(args.shape)
    for index, record in enumerate(fixed_records):
        if support_edges(record) != target_edges:
            raise AssertionError(
                f"fixed record {index} has the wrong support skeleton"
            )
        independent = independent_orbit(record["clause"])
        discovery = {
            tuple(clause)
            for clause in FIXED.shape_clause_orbit(
                pool, record["clause"], allowed, automorphisms
            )
        }
        if independent != discovery:
            raise AssertionError(
                f"fixed record {index} has a wrong computed orbit"
            )
        fixed_orbit_sizes[len(independent)] += 1

    general = json.loads(
        args.general_state.read_text(encoding="utf-8")
    )
    if general.get("shape") is not None:
        raise AssertionError("general state unexpectedly fixes a shape")
    selected = []
    transported_orbits: set[tuple[int, ...]] = set()
    for record in general["learned_records"]:
        old_edges = support_edges(record)
        transports = []
        for modes in itertools.permutations(range(5)):
            for sources in itertools.permutations(range(5)):
                image = frozenset(
                    (modes[mode], sources[source])
                    for mode, source in old_edges
                )
                if image == target_edges:
                    transports.append((modes, sources))
        if not transports:
            continue
        selected.append(record)
        representative_orbits = []
        for modes, sources in transports:
            transported = transform(
                record["clause"],
                modes,
                sources,
                tuple(range(3)),
            )
            representative_orbits.append(
                independent_orbit(list(transported))
            )
        first = representative_orbits[0]
        if any(orbit != first for orbit in representative_orbits[1:]):
            raise AssertionError(
                "different graph transports give different target orbits"
            )
        transported_orbits.update(first)

    expected_selected = {"c10": 388, "c4c6": 572}[args.shape]
    if len(selected) != expected_selected:
        raise AssertionError("wrong number of general records selected")
    discovery_clauses, discovery_summary = (
        FIXED.transported_general_preload(
            pool,
            allowed,
            args.shape,
            automorphisms,
            args.general_state,
        )
    )
    if transported_orbits != {
        tuple(clause) for clause in discovery_clauses
    }:
        raise AssertionError(
            "independent transported preload differs from discovery"
        )

    payload = {
        "status": "AUDIT_PASS",
        "shape": args.shape,
        "automorphisms": len(automorphisms),
        "colour_permutations": len(colour_permutations),
        "group_order": len(automorphisms) * len(colour_permutations),
        "fixed_records": len(fixed_records),
        "fixed_orbit_sizes": {
            str(size): count
            for size, count in sorted(fixed_orbit_sizes.items())
        },
        "general_records_selected": len(selected),
        "transported_general_clauses": len(transported_orbits),
        "discovery_general_summary": discovery_summary,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
