#!/usr/bin/env python3
"""Classify five-equation P5 templates by monomial-hypergraph structure."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import generate_p5_one_partial_support_system as BASE
import verify_p5_five_equation_laurent_core as CORE


ROOT = Path(__file__).resolve().parent
SHAPES = ("c10", "c4c6")
PACKAGE = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "two_partial_boundary"
)
TEMPLATE_COUNTS = (9, 8, 9, 8, 9)


def word_index(word: tuple[int, ...]) -> int:
    value = 0
    for colour in word:
        value = 3 * value + colour
    return value


def coefficient_support_counts(
    supports: tuple[tuple[int, ...], ...],
) -> list[int]:
    counts = [0] * (3**5)
    for permutation in BASE.PERMUTATIONS:
        choices = tuple(
            tuple(
                colour
                for colour in BASE.COLOURS
                if supports[mode][permutation[mode]]
                & (1 << colour)
            )
            for mode in BASE.MODES
        )
        for word in itertools.product(*choices):
            counts[word_index(word)] += 1
    return counts


def rectangle_equation_words() -> tuple[
    tuple[tuple[int, ...], ...], ...
]:
    output = []
    for fixed_pair in itertools.combinations(BASE.MODES, 2):
        remaining = tuple(
            mode for mode in BASE.MODES if mode not in fixed_pair
        )
        for toggle in remaining:
            tail = tuple(
                mode for mode in remaining if mode != toggle
            )
            for fixed_beta, varying in (
                tail,
                tuple(reversed(tail)),
            ):
                for alpha, beta in itertools.permutations(
                    BASE.COLOURS, 2
                ):
                    gamma = next(
                        colour
                        for colour in BASE.COLOURS
                        if colour not in (alpha, beta)
                    )

                    def word(
                        toggle_colour: int,
                        varying_colour: int,
                    ) -> tuple[int, ...]:
                        result = [0] * 5
                        for mode in fixed_pair:
                            result[mode] = alpha
                        result[toggle] = toggle_colour
                        result[fixed_beta] = beta
                        result[varying] = varying_colour
                        return tuple(result)

                    output.append(
                        tuple(
                            word(
                                toggle_colour,
                                varying_colour,
                            )
                            for toggle_colour in (beta, alpha)
                            for varying_colour in (
                                beta,
                                gamma,
                                alpha,
                            )
                            if (
                                toggle_colour,
                                varying_colour,
                            )
                            != (beta, beta)
                        )
                    )
    if len(output) != 360:
        raise AssertionError("rectangle pattern count changed")
    return tuple(output)


RECTANGLE_EQUATION_WORDS = rectangle_equation_words()


def gauge_data(
    supports: tuple[tuple[int, ...], ...],
) -> tuple[
    set[tuple[int, int, int]],
    dict[tuple[int, int, int], int],
]:
    edges = tuple(
        (mode, source, colour)
        for mode in BASE.MODES
        for source in BASE.SOURCES
        for colour in BASE.COLOURS
        if supports[mode][source] & (1 << colour)
    )
    nodes = tuple(("r", source) for source in BASE.SOURCES) + tuple(
        ("c", mode, colour)
        for mode in BASE.MODES
        for colour in BASE.COLOURS
    )
    union_find = BASE.UnionFind(nodes)
    tree_edges = set()
    for edge in edges:
        mode, source, colour = edge
        if union_find.union(
            ("r", source), ("c", mode, colour)
        ):
            tree_edges.add(edge)
    free_edges = tuple(edge for edge in edges if edge not in tree_edges)
    if len(tree_edges) != 19 or len(free_edges) != 24:
        raise AssertionError("exact-two gauge dimensions changed")
    return tree_edges, {
        edge: index for index, edge in enumerate(free_edges)
    }


def coefficient_polynomial(
    supports: tuple[tuple[int, ...], ...],
    colours: tuple[int, ...],
    tree_edges: set[tuple[int, int, int]],
    free_position: dict[tuple[int, int, int], int],
) -> CORE.Polynomial:
    one: BASE.Expression = (
        Fraction(1),
        (0,) * len(free_position),
    )

    def entry(
        mode: int, source: int, colour: int
    ) -> BASE.Expression | None:
        edge = (mode, source, colour)
        if edge in tree_edges:
            return one
        if edge not in free_position:
            return None
        exponent = [0] * len(free_position)
        exponent[free_position[edge]] = 1
        return Fraction(1), tuple(exponent)

    terms: dict[tuple[int, ...], int] = {}
    for permutation in BASE.PERMUTATIONS:
        value = one
        for mode, source in enumerate(permutation):
            factor = entry(mode, source, colours[mode])
            if factor is None:
                break
            value = BASE.multiply(value, factor)
        else:
            if value[0].denominator != 1:
                raise AssertionError("nonintegral support coefficient")
            terms[value[1]] = (
                terms.get(value[1], 0) + value[0].numerator
            )
    return CORE.Polynomial.make(terms)


def used_variables(
    equations: tuple[CORE.Polynomial, ...],
) -> tuple[int, ...]:
    return tuple(
        index
        for index in range(len(CORE.VARIABLES))
        if any(
            exponent[index]
            for polynomial in equations
            for exponent, _coefficient in polynomial.terms
        )
    )


def variable_colours(
    equations: tuple[CORE.Polynomial, ...],
    rounds: int = 12,
) -> dict[int, str]:
    variables = used_variables(equations)
    colours = {variable: "v" for variable in variables}
    for _round in range(rounds):
        descriptors = {}
        for variable in variables:
            equation_descriptors = []
            for equation_index, polynomial in enumerate(equations):
                terms = []
                for exponent, coefficient in polynomial.terms:
                    if not exponent[variable]:
                        continue
                    neighbourhood = []
                    for neighbour in variables:
                        multiplicity = exponent[neighbour]
                        if neighbour == variable:
                            multiplicity -= 1
                        neighbourhood.extend(
                            [colours[neighbour]] * multiplicity
                        )
                    terms.append(
                        (
                            coefficient,
                            exponent[variable],
                            tuple(sorted(neighbourhood)),
                        )
                    )
                equation_descriptors.append(
                    (equation_index, tuple(sorted(terms)))
                )
            descriptors[variable] = tuple(equation_descriptors)
        next_colours = {
            variable: hashlib.sha256(
                json.dumps(
                    descriptor,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            for variable, descriptor in descriptors.items()
        }
        if next_colours == colours:
            break
        colours = next_colours
    return colours


def polynomial_terms(
    polynomial: CORE.Polynomial,
    mapping: dict[int, int] | None = None,
) -> Counter[tuple[int, tuple[tuple[int, int], ...]]]:
    output = Counter()
    for exponent, coefficient in polynomial.terms:
        variables = []
        for index, power in enumerate(exponent):
            if not power:
                continue
            target = mapping[index] if mapping is not None else index
            variables.append((target, power))
        output[(coefficient, tuple(sorted(variables)))] += 1
    return output


def partial_mapping_consistent(
    source: tuple[CORE.Polynomial, ...],
    target: tuple[CORE.Polynomial, ...],
    mapping: dict[int, int],
) -> bool:
    mapped_source_variables = set(mapping)
    for source_polynomial, target_polynomial in zip(
        source, target, strict=True
    ):
        target_terms = polynomial_terms(target_polynomial)
        for exponent, coefficient in source_polynomial.terms:
            active = {
                index
                for index, power in enumerate(exponent)
                if power
            }
            if not active.issubset(mapped_source_variables):
                continue
            variables = tuple(
                sorted(
                    (mapping[index], power)
                    for index, power in enumerate(exponent)
                    if power
                )
            )
            if target_terms[(coefficient, variables)] == 0:
                return False
    return True


def variable_isomorphism(
    source: tuple[CORE.Polynomial, ...],
    target: tuple[CORE.Polynomial, ...],
) -> dict[int, int] | None:
    source_colours = variable_colours(source)
    target_colours = variable_colours(target)
    source_groups: dict[str, list[int]] = defaultdict(list)
    target_groups: dict[str, list[int]] = defaultdict(list)
    for variable, colour in source_colours.items():
        source_groups[colour].append(variable)
    for variable, colour in target_colours.items():
        target_groups[colour].append(variable)
    if {
        colour: len(group) for colour, group in source_groups.items()
    } != {
        colour: len(group) for colour, group in target_groups.items()
    }:
        return None

    groups = sorted(
        source_groups,
        key=lambda colour: (
            len(source_groups[colour]),
            colour,
        ),
    )

    def visit(
        position: int,
        mapping: dict[int, int],
    ) -> dict[int, int] | None:
        if position == len(groups):
            if all(
                polynomial_terms(source_polynomial, mapping)
                == polynomial_terms(target_polynomial)
                for source_polynomial, target_polynomial in zip(
                    source, target, strict=True
                )
            ):
                return dict(mapping)
            return None
        colour = groups[position]
        source_variables = sorted(source_groups[colour])
        for image in itertools.permutations(
            sorted(target_groups[colour])
        ):
            for left, right in zip(
                source_variables, image, strict=True
            ):
                mapping[left] = right
            if partial_mapping_consistent(source, target, mapping):
                result = visit(position + 1, mapping)
                if result is not None:
                    return result
            for left in source_variables:
                del mapping[left]
        return None

    return visit(0, {})


def system_signature(
    equations: tuple[CORE.Polynomial, ...],
) -> tuple:
    colours = variable_colours(equations)
    equation_shapes = tuple(
        tuple(
            sorted(
                (
                    coefficient,
                    sum(exponent),
                    sum(bool(power) for power in exponent),
                )
                for exponent, coefficient in polynomial.terms
            )
        )
        for polynomial in equations
    )
    return (
        tuple(sorted(Counter(colours.values()).items())),
        equation_shapes,
    )


def load_candidates(shape: str) -> list[dict]:
    manifest = json.loads(
        (PACKAGE / "manifest.json").read_text(encoding="utf-8")
    )
    cases = tuple(
        case for case in manifest["cases"] if case["shape"] == shape
    )
    output = []
    for catalogue_index, case in enumerate(cases):
        supports = tuple(tuple(row) for row in case["supports"])
        counts = coefficient_support_counts(supports)
        words = next(
            (
                equation_words
                for equation_words in RECTANGLE_EQUATION_WORDS
                if tuple(
                    counts[word_index(word)]
                    for word in equation_words
                )
                == TEMPLATE_COUNTS
            ),
            None,
        )
        if words is None:
            continue
        tree_edges, free_position = gauge_data(supports)
        equations = tuple(
            coefficient_polynomial(
                supports,
                word,
                tree_edges,
                free_position,
            )
            for word in words
        )
        output.append(
            {
                "case_id": case["case_id"],
                "shape": shape,
                "catalogue_index": catalogue_index,
                "source_orbit_index": case["support_orbit"],
                "supports": supports,
                "words": words,
                "equations": equations,
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    candidates = [
        candidate
        for shape in SHAPES
        for candidate in load_candidates(shape)
    ]
    core = next(
        candidate
        for candidate in candidates
        if candidate["case_id"] == "c4c6_orbit_18445"
    )
    core_signature = system_signature(core["equations"])
    signature_histogram = Counter(
        system_signature(candidate["equations"])
        for candidate in candidates
    )
    signature_matches = [
        candidate
        for candidate in candidates
        if system_signature(candidate["equations"]) == core_signature
    ]
    exact_matches = []
    for candidate in signature_matches:
        mapping = variable_isomorphism(
            core["equations"], candidate["equations"]
        )
        if mapping is not None:
            exact_matches.append(
                {
                    "case_id": candidate["case_id"],
                    "shape": candidate["shape"],
                    "catalogue_index": (
                        candidate["catalogue_index"]
                    ),
                    "source_orbit_index": (
                        candidate["source_orbit_index"]
                    ),
                    "words": [
                        "".join(map(str, word))
                        for word in candidate["words"]
                    ],
                    "variable_mapping": {
                        f"u{left}": f"u{right}"
                        for left, right in sorted(mapping.items())
                    },
                }
            )

    payload = {
        "status": "EXPLORATORY_MONOMIAL_HYPERGRAPH_CLASSIFICATION",
        "template_support_orbits": len(candidates),
        "refined_signature_classes": len(signature_histogram),
        "core_shape": core["shape"],
        "core_case_id": core["case_id"],
        "core_catalogue_index": core["catalogue_index"],
        "core_source_orbit_index": core["source_orbit_index"],
        "core_used_variables": len(used_variables(core["equations"])),
        "core_signature_support_orbits": len(signature_matches),
        "exact_variable_isomorphic_support_orbits": len(exact_matches),
        "exact_matches": exact_matches,
        "global_conjecture_resolved": False,
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
