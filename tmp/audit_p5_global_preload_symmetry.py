"""Independent audit of global P5 preload symmetry transport.

The discovery code imports old learned clauses under
C5(mode) x C5(source) x S3(colour).  This script reconstructs that action
without calling the discovery transformers, checks group closure, verifies
each transformed clause against the correspondingly transformed model, and
then compares both each orbit and the aggregate imported clause set.
"""

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
    "p5_local_global_symmetry_audit", LOCAL_PROBE
)
P5 = importlib.util.module_from_spec(LOCAL_SPEC)
assert LOCAL_SPEC.loader is not None
LOCAL_SPEC.loader.exec_module(P5)

FIXED_SPEC = importlib.util.spec_from_file_location(
    "p5_global_preload_under_test", FIXED_PROBE
)
FIXED = importlib.util.module_from_spec(FIXED_SPEC)
assert FIXED_SPEC.loader is not None
FIXED_SPEC.loader.exec_module(FIXED)


def compose_permutations(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def symmetry_group() -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    elements = tuple(
        (mode_shift, source_shift, colours)
        for mode_shift in range(5)
        for source_shift in range(5)
        for colours in itertools.permutations(range(3))
    )
    element_set = set(elements)
    identity = (0, 0, tuple(range(3)))
    if len(elements) != 150 or identity not in element_set:
        raise AssertionError("global symmetry group has the wrong size")
    for left_mode, left_source, left_colours in elements:
        for right_mode, right_source, right_colours in elements:
            product = (
                (left_mode + right_mode) % 5,
                (left_source + right_source) % 5,
                compose_permutations(left_colours, right_colours),
            )
            if product not in element_set:
                raise AssertionError("global symmetry action is not closed")
    return elements


def independent_transformer(pool: Any, allowed: tuple[tuple, ...]):
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
    signature_cache: dict[tuple, int] = {}

    def transform_mask(mask: int, colours: tuple[int, ...]) -> int:
        output = 0
        for old_colour in range(3):
            if mask & (1 << old_colour):
                output |= 1 << colours[old_colour]
        return output

    def transform_signature(
        pattern_index: int,
        source_shift: int,
        colours: tuple[int, ...],
    ) -> int:
        key = (pattern_index, source_shift, colours)
        if key in signature_cache:
            return signature_cache[key]
        support, incidence = allowed[pattern_index]
        new_support = [0] * 5
        for old_source in range(5):
            new_support[(old_source + source_shift) % 5] = transform_mask(
                support[old_source], colours
            )
        new_incidence = [0] * len(source_subsets)
        for old_index, old_subset in enumerate(source_subsets):
            new_subset = tuple(
                sorted((source + source_shift) % 5 for source in old_subset)
            )
            new_incidence[subset_index[new_subset]] = transform_mask(
                incidence[old_index], colours
            )
        transformed = (tuple(new_support), tuple(new_incidence))
        signature_cache[key] = signature_index[transformed]
        return signature_cache[key]

    def transform_support(
        supports: tuple[tuple[int, ...], ...],
        mode_shift: int,
        source_shift: int,
        colours: tuple[int, ...],
    ) -> tuple[tuple[int, ...], ...]:
        output = [[0] * 5 for _ in range(5)]
        for old_mode in range(5):
            for old_source in range(5):
                output[(old_mode + mode_shift) % 5][
                    (old_source + source_shift) % 5
                ] = transform_mask(
                    supports[old_mode][old_source], colours
                )
        return tuple(tuple(row) for row in output)

    def transform_clause(
        clause: list[int],
        mode_shift: int,
        source_shift: int,
        colours: tuple[int, ...],
    ) -> tuple[int, ...]:
        output = []
        for literal in clause:
            variable = pool.obj(abs(literal))
            if variable is None:
                raise AssertionError("learned clause uses an unknown variable")
            if variable[0] == "x":
                _, mode, source, colour = variable
                new_key = (
                    "x",
                    (mode + mode_shift) % 5,
                    (source + source_shift) % 5,
                    colours[colour],
                )
            elif variable[0] == "local_pattern":
                _, mode, pattern_index = variable
                new_key = (
                    "local_pattern",
                    (mode + mode_shift) % 5,
                    transform_signature(
                        pattern_index, source_shift, colours
                    ),
                )
            else:
                raise AssertionError(
                    f"unsupported learned key {variable[0]!r}"
                )
            new_variable = pool.id(new_key)
            output.append(
                new_variable if literal > 0 else -new_variable
            )
        if len(set(output)) != len(output):
            raise AssertionError("symmetry transform repeated a literal")
        if any(-literal in output for literal in output):
            raise AssertionError("symmetry transform produced a tautology")
        return tuple(sorted(output))

    return transform_clause, transform_support, transform_signature


def assert_false_on_transformed_model(
    pool: Any,
    allowed: tuple[tuple, ...],
    clause: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> None:
    selected_patterns: dict[int, int] = {}
    for literal in clause:
        key = pool.obj(abs(literal))
        if key[0] == "local_pattern":
            if literal >= 0:
                raise AssertionError("signature cube has a positive literal")
            _, mode, pattern_index = key
            if mode in selected_patterns:
                raise AssertionError("signature cube repeats a mode")
            selected_patterns[mode] = pattern_index
            value = tuple(allowed[pattern_index][0]) == supports[mode]
        elif key[0] == "x":
            _, mode, source, colour = key
            value = bool(supports[mode][source] & (1 << colour))
        else:
            raise AssertionError(f"unsupported clause key {key[0]!r}")
        literal_value = value if literal > 0 else not value
        if literal_value:
            raise AssertionError(
                "transformed clause is true on its transformed model"
            )
    if selected_patterns and set(selected_patterns) != set(range(5)):
        raise AssertionError("signature cube does not select all five modes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=pathlib.Path, nargs="+")
    args = parser.parse_args()

    allowed = P5.finite_field_local_signatures()
    _cnf, pool = P5.build_cnf(
        allowed, double_lex=True, pair_hierarchy=True
    )
    transform_clause, transform_support, _ = independent_transformer(
        pool, allowed
    )
    group = symmetry_group()

    summaries = []
    for state_path in args.state:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("shape") is not None:
            raise AssertionError("global preload unexpectedly fixes a shape")
        records = list(state.get("learned_records", []))
        if not records:
            raise AssertionError("global preload has no learned records")

        aggregate: set[tuple[int, ...]] = set()
        orbit_sizes: collections.Counter[int] = collections.Counter()
        key_kinds: collections.Counter[str] = collections.Counter()
        for index, record in enumerate(records):
            clause = [int(literal) for literal in record["clause"]]
            supports = tuple(
                tuple(int(mask) for mask in row)
                for row in record["supports"]
            )
            independent = set()
            for mode_shift, source_shift, colours in group:
                transformed_clause = transform_clause(
                    clause, mode_shift, source_shift, colours
                )
                transformed_support = transform_support(
                    supports, mode_shift, source_shift, colours
                )
                assert_false_on_transformed_model(
                    pool,
                    allowed,
                    transformed_clause,
                    transformed_support,
                )
                independent.add(transformed_clause)

            kinds = {
                pool.obj(abs(literal))[0] for literal in clause
            }
            if len(kinds) != 1:
                raise AssertionError(
                    f"record {index} mixes learned variable kinds"
                )
            kind = next(iter(kinds))
            if kind == "x":
                discovery = {
                    tuple(item)
                    for item in P5.symmetry_clause_orbit(pool, clause)
                }
            elif kind == "local_pattern":
                discovery = {
                    tuple(item)
                    for item in P5.local_pattern_clause_orbit(
                        pool, clause, allowed
                    )
                }
            else:
                raise AssertionError(
                    f"record {index} has unsupported key kind {kind!r}"
                )
            if independent != discovery:
                raise AssertionError(
                    f"record {index} has a wrong discovery orbit"
                )
            aggregate.update(independent)
            orbit_sizes[len(independent)] += 1
            key_kinds[kind] += 1

        discovery_clauses, discovery_summary = (
            FIXED.global_local_signature_preload(
                pool, allowed, state_path
            )
        )
        if aggregate != {
            tuple(clause) for clause in discovery_clauses
        }:
            raise AssertionError(
                "aggregate independent preload differs from discovery"
            )
        summaries.append(
            {
                "path": str(state_path),
                "records": len(records),
                "key_kinds": dict(sorted(key_kinds.items())),
                "orbit_sizes": {
                    str(size): count
                    for size, count in sorted(orbit_sizes.items())
                },
                "aggregate_orbit_clauses": len(aggregate),
                "discovery_summary": discovery_summary,
            }
        )

    print(
        json.dumps(
            {
                "status": "AUDIT_PASS",
                "group_order": len(group),
                "states": summaries,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
