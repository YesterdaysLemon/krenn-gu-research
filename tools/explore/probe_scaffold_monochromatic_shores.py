#!/usr/bin/env python3
"""Exact restricted k=2 probe for the monochromatic-shore parent MS.

Each four-vertex shore carries the three unit-weight perfect matchings M_c.
Every cross-colour block X_cd, c != d, is i times one of the eight permutation
matrices carrying M_d on the right to M_c on the left; X_cc is zero.  The same
six choices are used in all fixed-left and fixed-right equations.

The calculation uses Gaussian integer pairs throughout.  Failure of this
finite permutation-phase family is experimental and is not a proof of MS.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


N = 8
COLOURS = tuple(range(3))
LEFT = tuple(range(4))
RIGHT = tuple(range(4, 8))
LOCAL_VERTICES = tuple(range(4))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
CROSS_VARIABLES = tuple(
    (left_colour, right_colour)
    for left_colour in COLOURS
    for right_colour in COLOURS
    if left_colour != right_colour
)
VARIABLE_INDEX = {variable: index for index, variable in enumerate(CROSS_VARIABLES)}
Gaussian = tuple[int, int]
Permutation = tuple[int, int, int, int]


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


PERFECT_MATCHINGS = perfect_matchings(tuple(range(N)))


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gaussian_multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def matching_set(colour: int) -> set[tuple[int, int]]:
    return {tuple(sorted(edge)) for edge in MATCHINGS[colour]}


def maps_matching(permutation: Permutation, source: int, target: int) -> bool:
    image = {
        tuple(sorted((permutation[u], permutation[v])))
        for u, v in MATCHINGS[source]
    }
    return image == matching_set(target)


def permutation_domains() -> dict[tuple[int, int], tuple[Permutation, ...]]:
    domains = {}
    for left_colour, right_colour in CROSS_VARIABLES:
        domain = tuple(
            permutation
            for permutation in itertools.permutations(LOCAL_VERTICES)
            if maps_matching(permutation, right_colour, left_colour)
        )
        if len(domain) != 8:
            raise AssertionError(
                f"X_{left_colour}{right_colour} has {len(domain)} mappings, expected 8"
            )
        domains[(left_colour, right_colour)] = domain
    return domains


def internal_weight(u: int, v: int, a: int, b: int) -> Gaussian:
    if a != b:
        return 0, 0
    local_u = u if u in LEFT else u - 4
    local_v = v if v in LEFT else v - 4
    return ((1, 0) if tuple(sorted((local_u, local_v))) in matching_set(a) else (0, 0))


def edge_weight(
    u: int,
    v: int,
    a: int,
    b: int,
    choices: tuple[int, ...],
    domains: dict[tuple[int, int], tuple[Permutation, ...]],
) -> Gaussian:
    if (u in LEFT) == (v in LEFT):
        return internal_weight(u, v, a, b)
    if u in RIGHT:
        u, v, a, b = v, u, b, a
    if a == b:
        return 0, 0
    variable = (a, b)
    permutation = domains[variable][choices[VARIABLE_INDEX[variable]]]
    return ((0, 1) if permutation[v - 4] == u else (0, 0))


def amplitude(
    word: tuple[int, ...],
    choices: tuple[int, ...],
    domains: dict[tuple[int, int], tuple[Permutation, ...]],
) -> Gaussian:
    total = (0, 0)
    for matching in PERFECT_MATCHINGS:
        product = (1, 0)
        for u, v in matching:
            product = gaussian_multiply(
                product, edge_weight(u, v, word[u], word[v], choices, domains)
            )
            if product == (0, 0):
                break
        total = gaussian_add(total, product)
    return total


def amplitude_by_crossing_count(
    word: tuple[int, ...],
    choices: tuple[int, ...],
    domains: dict[tuple[int, int], tuple[Permutation, ...]],
) -> dict[int, Gaussian]:
    """Split an amplitude into its zero-, two-, and four-crossing sums."""

    output = {0: (0, 0), 2: (0, 0), 4: (0, 0)}
    for matching in PERFECT_MATCHINGS:
        product = (1, 0)
        for u, v in matching:
            product = gaussian_multiply(
                product, edge_weight(u, v, word[u], word[v], choices, domains)
            )
        crossing_count = sum(u in LEFT and v in RIGHT for u, v in matching)
        if crossing_count not in output:
            raise AssertionError("a perfect matching has an odd shore-crossing count")
        output[crossing_count] = gaussian_add(output[crossing_count], product)
    return output


def target(word: tuple[int, ...]) -> Gaussian:
    return ((1, 0) if len(set(word)) == 1 else (0, 0))


def local_choices(
    side: str,
    fixed_colour: int,
    first: int,
    second: int,
) -> tuple[int, ...]:
    choices = [0] * len(CROSS_VARIABLES)
    if side == "left":
        others = tuple(colour for colour in COLOURS if colour != fixed_colour)
        choices[VARIABLE_INDEX[(fixed_colour, others[0])]] = first
        choices[VARIABLE_INDEX[(fixed_colour, others[1])]] = second
    else:
        others = tuple(colour for colour in COLOURS if colour != fixed_colour)
        choices[VARIABLE_INDEX[(others[0], fixed_colour)]] = first
        choices[VARIABLE_INDEX[(others[1], fixed_colour)]] = second
    return tuple(choices)


def shore_word(side: str, fixed_colour: int, varying: tuple[int, ...]) -> tuple[int, ...]:
    if side == "left":
        return (fixed_colour,) * 4 + varying
    return varying + (fixed_colour,) * 4


def local_pair_passes(
    side: str,
    fixed_colour: int,
    pair: tuple[int, int],
    domains: dict[tuple[int, int], tuple[Permutation, ...]],
    stage: str,
) -> bool:
    choices = local_choices(side, fixed_colour, *pair)
    for varying in itertools.product(COLOURS, repeat=4):
        if stage == "quadratic":
            if fixed_colour not in varying or all(value == fixed_colour for value in varying):
                continue
        elif stage != "full":
            raise ValueError(f"unsupported stage {stage}")
        word = shore_word(side, fixed_colour, varying)
        if amplitude(word, choices, domains) != target(word):
            return False
    return True


def allowed_pairs(domains, stage: str):
    output = {}
    for side in ("left", "right"):
        for colour in COLOURS:
            output[(side, colour)] = {
                pair
                for pair in itertools.product(range(8), repeat=2)
                if local_pair_passes(side, colour, pair, domains, stage)
            }
    return output


def quartic_obstructions_after_quadratic(domains, quadratic_constraints):
    """Record the first exact no-fixed-colour failure for each Gram-compatible pair."""

    output = {}
    for (side, colour), pairs in quadratic_constraints.items():
        histogram = {}
        for pair in sorted(pairs):
            choices = local_choices(side, colour, *pair)
            for varying in itertools.product(COLOURS, repeat=4):
                if colour in varying:
                    continue
                word = shore_word(side, colour, varying)
                value = amplitude(word, choices, domains)
                wanted = target(word)
                residual = (value[0] - wanted[0], value[1] - wanted[1])
                if residual == (0, 0):
                    continue
                components = amplitude_by_crossing_count(word, choices, domains)
                key = (
                    "".join(map(str, varying)),
                    residual,
                    tuple((count, components[count]) for count in (0, 2, 4)),
                )
                histogram[key] = histogram.get(key, 0) + 1
                break
        output[f"{side}_{colour}"] = [
            {
                "varying_shore_word": varying_word,
                "full_word": "".join(
                    map(
                        str,
                        shore_word(side, colour, tuple(map(int, varying_word))),
                    )
                ),
                "residual": list(residual),
                "amplitude_by_crossing_count": {
                    str(crossing_count): list(value)
                    for crossing_count, value in components
                },
                "gram_compatible_permutation_pairs_failed": count,
            }
            for (varying_word, residual, components), count in sorted(histogram.items())
        ]
    return output


def assignment_satisfies(
    choices: tuple[int, ...],
    constraints: dict[tuple[str, int], set[tuple[int, int]]],
) -> bool:
    for colour in COLOURS:
        outgoing = tuple(
            choices[VARIABLE_INDEX[(colour, other)]]
            for other in COLOURS
            if other != colour
        )
        if outgoing not in constraints[("left", colour)]:
            return False
        incoming = tuple(
            choices[VARIABLE_INDEX[(other, colour)]]
            for other in COLOURS
            if other != colour
        )
        if incoming not in constraints[("right", colour)]:
            return False
    return True


def explicit_weights(choices, domains):
    entries = []
    # Internal unit entries on both shores.
    for shore_offset in (0, 4):
        for colour, matching in enumerate(MATCHINGS):
            for u, v in matching:
                entries.append(
                    {
                        "vertices": [u + shore_offset, v + shore_offset],
                        "colours": [colour, colour],
                        "value": [1, 0],
                    }
                )
    # Cross entries i*P for all six ordered colour pairs.
    for variable in CROSS_VARIABLES:
        permutation = domains[variable][choices[VARIABLE_INDEX[variable]]]
        for right_vertex, left_vertex in enumerate(permutation):
            entries.append(
                {
                    "vertices": [left_vertex, right_vertex + 4],
                    "colours": list(variable),
                    "value": [0, 1],
                }
            )
    return sorted(entries, key=lambda item: (item["vertices"], item["colours"]))


def residual_hash(residuals) -> str:
    canonical = json.dumps(residuals, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(canonical).hexdigest()


def run_probe() -> dict[str, object]:
    started = time.monotonic()
    domains = permutation_domains()

    controls = []
    for left_colour in COLOURS:
        for right_colour in COLOURS:
            if left_colour == right_colour:
                continue
            variable = (left_colour, right_colour)
            for choice in range(8):
                choices = [0] * len(CROSS_VARIABLES)
                choices[VARIABLE_INDEX[variable]] = choice
                word = (left_colour,) * 4 + (right_colour,) * 4
                value = amplitude(word, tuple(choices), domains)
                if value != (0, 0):
                    raise AssertionError("a pure pair cancellation control failed")
            controls.append(
                {
                    "left_colour": left_colour,
                    "right_colour": right_colour,
                    "permutations_checked": 8,
                    "expected_factor": "(1+i^2)^2=0",
                }
            )

    quadratic_constraints = allowed_pairs(domains, "quadratic")
    full_constraints = allowed_pairs(domains, "full")
    quartic_obstructions = quartic_obstructions_after_quadratic(
        domains, quadratic_constraints
    )
    all_assignments = itertools.product(range(8), repeat=len(CROSS_VARIABLES))
    quadratic_survivors = [
        choices
        for choices in all_assignments
        if assignment_satisfies(choices, quadratic_constraints)
    ]
    shore_survivors = [
        choices
        for choices in quadratic_survivors
        if assignment_satisfies(choices, full_constraints)
    ]

    candidate = None
    apparent_full_target = False
    if shore_survivors:
        choices = shore_survivors[0]
        shore_failures = []
        for word in itertools.product(COLOURS, repeat=N):
            if len(set(word[:4])) != 1 and len(set(word[4:])) != 1:
                continue
            value = amplitude(word, choices, domains)
            if value != target(word):
                shore_failures.append(
                    {"word": "".join(map(str, word)), "value": list(value)}
                )
        if shore_failures:
            raise AssertionError("CSP survivor failed direct monochromatic-shore replay")

        residuals = []
        for word in itertools.product(COLOURS, repeat=N):
            value = amplitude(word, choices, domains)
            wanted = target(word)
            residual = (value[0] - wanted[0], value[1] - wanted[1])
            if residual != (0, 0):
                residuals.append(
                    {"word": "".join(map(str, word)), "residual": list(residual)}
                )
        apparent_full_target = not residuals
        candidate = {
            "choice_indices": {
                f"X_{left}{right}": choices[VARIABLE_INDEX[(left, right)]]
                for left, right in CROSS_VARIABLES
            },
            "permutations_right_to_left": {
                f"X_{left}{right}": list(
                    domains[(left, right)][choices[VARIABLE_INDEX[(left, right)]]]
                )
                for left, right in CROSS_VARIABLES
            },
            "explicit_nonzero_W_entries": explicit_weights(choices, domains),
            "monochromatic_shore_words_checked": 477,
            "full_target_words_checked": 3**N,
            "full_target_nonzero_residual_count": len(residuals),
            "full_target_nonzero_residuals_sha256": residual_hash(residuals),
            "full_target_nonzero_residuals": residuals,
        }

    if apparent_full_target:
        outcome = "APPARENT_EXACT_FULL_TARGET_SOLUTION_REQUIRES_DEDICATED_VALIDATION"
    elif shore_survivors:
        outcome = "EXACT_RESTRICTED_COUNTERMODEL_TO_MS_AT_K2"
    else:
        outcome = "NO_MS_COUNTERMODEL_IN_RESTRICTED_PERMUTATION_PHASE_FAMILY"

    return {
        "schema": "n8-scaffold-monochromatic-shore-permutation-phase-probe-v1",
        "status": "PASS",
        "outcome": outcome,
        "scope": {
            "n": N,
            "shores": [list(LEFT), list(RIGHT)],
            "internal_blocks": "unit matrix entries on M_c inside each K4 shore",
            "cross_blocks": "X_cd=i*P_cd for c!=d and X_cc=0",
            "permutation_condition": "P_cd maps right matching M_d to left matching M_c",
            "coefficient_ring": "Gaussian integers Z[i]",
            "restricted_search_only": True,
        },
        "matchings": {str(colour): [list(edge) for edge in matching] for colour, matching in enumerate(MATCHINGS)},
        "cross_variable_order": [f"X_{left}{right}" for left, right in CROSS_VARIABLES],
        "permutation_domains": {
            f"X_{left}{right}": [list(permutation) for permutation in domains[(left, right)]]
            for left, right in CROSS_VARIABLES
        },
        "pure_pair_controls": controls,
        "constraint_counts": {
            "single_fixed_shore_gram_compatible_pairs": {
                f"{side}_{colour}": len(pairs)
                for (side, colour), pairs in quadratic_constraints.items()
            },
            "full_shore_local_allowed_pairs": {
                f"{side}_{colour}": len(pairs)
                for (side, colour), pairs in full_constraints.items()
            },
            "total_cross_assignments": 8 ** len(CROSS_VARIABLES),
            "quadratic_cycle_survivors": len(quadratic_survivors),
            "all_monochromatic_shore_survivors": len(shore_survivors),
        },
        "quartic_obstructions_after_gram_constraints": quartic_obstructions,
        "candidate": candidate,
        "interpretation": (
            "A survivor is an exact countermodel only to MS at k=2 in this "
            "restricted permutation-phase family. No-solution in this family "
            "would be experimental and would not prove MS."
        ),
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_probe()
    payload = json.dumps(result, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 2 if result["outcome"].startswith("APPARENT_EXACT_FULL_TARGET") else 0


if __name__ == "__main__":
    raise SystemExit(main())
