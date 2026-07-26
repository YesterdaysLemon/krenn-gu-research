"""Generalize simple C4+C4+C6 forks by exact matching activity.

The separable transport rules preserve every active singleton edge.  This
stronger scout preserves only what the proof actually needs: the base
equation has no non-full perfect matching, and each cycle target has one
specified non-full survivor.  These conditions become exact relational
constraints on the three singleton factors.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    CYCLES,
    ELIGIBLE_EDGES,
    ELIGIBLE_EDGE_ID,
    FULL_EDGES,
    Factor,
    parse_factor,
    perfect_matchings,
    validate_simple_certificate,
)

N = 14


def factor_mask(factor: Factor) -> int:
    return sum(1 << ELIGIBLE_EDGE_ID[item] for item in factor)


def requirements(
    matching: Factor,
    colouring: Sequence[int],
) -> tuple[int, int, int]:
    output = [0, 0, 0]
    for item in matching:
        if item in FULL_EDGES:
            continue
        first_colour = int(colouring[item[0]])
        second_colour = int(colouring[item[1]])
        if first_colour != second_colour:
            raise AssertionError(
                "a compatible singleton edge is bichromatic"
            )
        output[first_colour] |= 1 << ELIGIBLE_EDGE_ID[item]
    return tuple(output)


def submasks(mask: int):
    selected = mask
    while True:
        yield selected
        if selected == 0:
            break
        selected = (selected - 1) & mask


def minimal_prohibitions(
    rows: set[tuple[int, int, int]],
) -> tuple[tuple[int, int, int], ...]:
    """Drop a prohibition when a componentwise subset already forbids it."""
    output = []
    for row in sorted(
        rows,
        key=lambda item: (
            sum(mask.bit_count() for mask in item),
            item,
        ),
    ):
        dominated = False
        for first in submasks(row[0]):
            if dominated:
                break
            for second in submasks(row[1]):
                if dominated:
                    break
                for third in submasks(row[2]):
                    candidate = (first, second, third)
                    if candidate != row and candidate in rows:
                        dominated = True
                        break
        if not dominated:
            output.append(row)
    return tuple(output)


@functools.lru_cache(maxsize=None)
def compatible_requirement_counts(
    colouring: Sequence[int],
) -> tuple[tuple[tuple[int, int, int], int], ...]:
    allowed = set(FULL_EDGES)
    for item in ELIGIBLE_EDGES:
        if colouring[item[0]] == colouring[item[1]]:
            allowed.add(item)
    counts = Counter(
        requirements(matching, colouring)
        for matching in perfect_matchings(allowed)
    )
    return tuple(
        sorted((row, int(count)) for row, count in counts.items())
    )


def transformed_details(
    analysis: dict[str, object],
    colour_permutation: Sequence[int],
) -> tuple[
    tuple[int, int, int],
    tuple[tuple[int, int, int], ...],
]:
    factors, colourings = validate_simple_certificate(analysis)
    skeleton_matchings = perfect_matchings(
        set(FULL_EDGES) | set().union(*map(set, factors))
    )
    certificate = analysis["certificate"]
    desired = [None]
    for row in certificate["alternatives"]:
        desired.append(
            skeleton_matchings[int(row["surviving_matching"])]
        )
    def permute_row(
        row: tuple[int, int, int],
    ) -> tuple[int, int, int]:
        output = [0, 0, 0]
        for old_role, value in enumerate(row):
            output[colour_permutation[old_role]] = value
        return tuple(output)

    required = [0, 0, 0]
    prohibitions: set[tuple[int, int, int]] = set()
    for colouring, survivor in zip(
        colourings,
        desired,
        strict=True,
    ):
        wanted = None
        if survivor is not None:
            wanted = permute_row(
                requirements(survivor, colouring)
            )
            for role in range(3):
                required[role] |= wanted[role]
        found_wanted = survivor is None
        for original_row, multiplicity in (
            compatible_requirement_counts(colouring)
        ):
            row = permute_row(original_row)
            if row == (0, 0, 0):
                continue
            if survivor is not None and row == wanted:
                if multiplicity != 1:
                    raise AssertionError(
                        "survivor requirement is not unique"
                    )
                found_wanted = True
                continue
            prohibitions.add(row)
        if not found_wanted:
            raise AssertionError(
                "reported survivor is not colouring-compatible"
            )
    rule = (
        tuple(required),
        minimal_prohibitions(prohibitions),
    )
    factor_masks = tuple(map(factor_mask, factors))
    moved_masks = [0, 0, 0]
    for old_role, selected in enumerate(factor_masks):
        moved_masks[colour_permutation[old_role]] = selected
    if any(
        moved_masks[role] & required[role] != required[role]
        for role in range(3)
    ):
        raise AssertionError("source misses a required survivor edge")
    if any(
        all(
            moved_masks[role] & row[role] == row[role]
            for role in range(3)
        )
        for row in prohibitions
    ):
        raise AssertionError(
            "source activates a prohibited non-full matching"
        )
    return rule


def permute_rule(
    rule: tuple[
        tuple[int, int, int],
        tuple[tuple[int, int, int], ...],
    ],
    permutation: Sequence[int],
) -> tuple[
    tuple[int, int, int],
    tuple[tuple[int, int, int], ...],
]:
    def move(row: tuple[int, int, int]) -> tuple[int, int, int]:
        output = [0, 0, 0]
        for old_role, value in enumerate(row):
            output[permutation[old_role]] = value
        return tuple(output)

    return (
        move(rule[0]),
        tuple(sorted(move(row) for row in rule[1])),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_support_samples93.json"
        ),
    )
    parser.add_argument(
        "--analysis-pattern",
        default=(
            "tmp/fourteen_vertex_c4_4_6_"
            "sample93_{index}_factor_fork.json"
        ),
    )
    parser.add_argument(
        "--extra-samples",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--extra-analysis-pattern",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_relational_rule_coverage.json"
        ),
    )
    args = parser.parse_args()
    if len(args.extra_samples) != len(args.extra_analysis_pattern):
        raise ValueError("extra source arguments must be paired")
    primary = json.loads(args.samples.read_text(encoding="utf-8"))
    manifests = [
        ("primary", primary, args.analysis_pattern)
    ]
    for extra_id, (path, pattern) in enumerate(
        zip(
            args.extra_samples,
            args.extra_analysis_pattern,
            strict=True,
        )
    ):
        manifests.append(
            (
                f"extra{extra_id}",
                json.loads(path.read_text(encoding="utf-8")),
                pattern,
            )
        )
    if any(
        manifest.get("partition") != [4, 4, 6]
        for _name, manifest, _pattern in manifests
    ):
        raise AssertionError("source partition changed")
    factors = perfect_matchings(ELIGIBLE_EDGES)
    factor_id = {
        factor: position for position, factor in enumerate(factors)
    }
    masks = list(map(factor_mask, factors))
    started = time.perf_counter()
    colour_permutations = list(itertools.permutations(range(3)))
    rules: set[
        tuple[
            tuple[int, int, int],
            tuple[tuple[int, int, int], ...],
        ]
    ] = set()
    source_statuses = {}
    sources = 0
    for name, manifest, pattern in manifests:
        statuses = {}
        for index in range(len(manifest["survivors"])):
            analysis = json.loads(
                Path(pattern.format(index=index)).read_text(
                    encoding="utf-8"
                )
            )
            status = str(analysis["status"])
            statuses[status] = statuses.get(status, 0) + 1
            if status != "even_cycle_factor_fork":
                continue
            sources += 1
            base_rule = transformed_details(
                analysis, (0, 1, 2)
            )
            for permutation in colour_permutations:
                rules.add(permute_rule(base_rule, permutation))
        source_statuses[name] = statuses

    closed_primary = []
    disconnected_primary = []
    for index, row in enumerate(primary["survivors"]):
        triple = tuple(
            masks[factor_id[parse_factor(row[key])]]
            for key in ("first", "second", "third")
        )
        analysis = json.loads(
            Path(
                args.analysis_pattern.format(index=index)
            ).read_text(encoding="utf-8")
        )
        if analysis["status"] == (
            "disconnected_factorization_contradiction"
        ):
            disconnected_primary.append(index)
            continue
        for required, prohibitions in rules:
            if any(
                triple[role] & required[role] != required[role]
                for role in range(3)
            ):
                continue
            if any(
                all(
                    triple[role] & forbidden[role]
                    == forbidden[role]
                    for role in range(3)
                )
                for forbidden in prohibitions
            ):
                continue
            closed_primary.append(index)
            break
    residual_primary = sorted(
        set(range(len(primary["survivors"])))
        - set(disconnected_primary)
        - set(closed_primary)
    )
    prohibition_histogram: dict[int, int] = {}
    for _required, prohibited in rules:
        prohibition_histogram[len(prohibited)] = (
            prohibition_histogram.get(len(prohibited), 0) + 1
        )
    payload = {
        "status": "relational_simple_factor_fork_rule_coverage",
        "necessary_conditions_only": True,
        "partition": [4, 4, 6],
        "eligible_factors": len(factors),
        "source_certificates_replayed": sources,
        "source_statuses": source_statuses,
        "colour_permutations": len(colour_permutations),
        "deduplicated_relational_rules": len(rules),
        "prohibition_count_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                prohibition_histogram.items()
            )
        },
        "primary_disconnected": disconnected_primary,
        "primary_rule_closed": closed_primary,
        "primary_residuals": residual_primary,
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
