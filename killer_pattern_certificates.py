"""Combinatorial certificates against forced killer-edge patterns.

For a killer pattern, an arc v -> u labelled c means that the block on
{v,u} can be nonzero only when vertex u has colour c.  Consequently:

* a monochromatic colour-c perfect matching may use only edges carrying no
  arcs or arcs all labelled c;
* if one nonzero monochromatic matching is selected for each colour, every
  edge in those matchings has a nonzero diagonal entry;
* recombining those known-nonzero entries can produce a mixed matching.

If that mixed matching is the only structurally allowed perfect matching for
its induced non-monochromatic colouring, its nonzero product cannot cancel.
That pattern/triple is therefore impossible over any field.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np

from search_killer_patterns import Pattern, random_pattern
from search_witness import EquationSystem

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Arc = tuple[int, int, int]


def pattern_arcs(pattern: Pattern) -> dict[Edge, list[Arc]]:
    arcs: dict[Edge, list[Arc]] = {}
    for centre, targets in enumerate(pattern):
        for colour, leaf in enumerate(targets):
            edge = tuple(sorted((centre, leaf)))
            arcs.setdefault(edge, []).append((centre, leaf, colour))
    return arcs


def edge_allows_colouring(
    arcs: dict[Edge, list[Arc]],
    edge: Edge,
    colouring: tuple[int, ...],
) -> bool:
    return all(
        colouring[leaf] == colour
        for _, leaf, colour in arcs.get(edge, ())
    )


def matching_allows_colouring(
    arcs: dict[Edge, list[Arc]],
    matching: Matching,
    colouring: tuple[int, ...],
) -> bool:
    return all(
        edge_allows_colouring(arcs, edge, colouring)
        for edge in matching
    )


def monochromatic_matchings(
    system: EquationSystem,
    arcs: dict[Edge, list[Arc]],
    colour: int,
) -> list[Matching]:
    result: list[Matching] = []
    for matching in system.matchings:
        if all(
            all(arc_colour == colour for _, _, arc_colour in arcs.get(edge, ()))
            for edge in matching
        ):
            result.append(matching)
    return result


def certificate_for_matching_triple(
    system: EquationSystem,
    pattern: Pattern,
    selected: tuple[Matching, Matching, Matching],
) -> dict[str, object] | None:
    """Find one known-nonzero mixed matching with no cancellation partner."""

    arcs = pattern_arcs(pattern)
    edge_colours: dict[Edge, list[int]] = {}
    for colour, matching in enumerate(selected):
        for edge in matching:
            edge_colours.setdefault(edge, []).append(colour)

    for mixed_matching in system.matchings:
        if not all(edge in edge_colours for edge in mixed_matching):
            continue
        choices = [edge_colours[edge] for edge in mixed_matching]
        for matching_colours in itertools.product(*choices):
            colouring = [0] * system.n
            for edge, colour in zip(mixed_matching, matching_colours):
                colouring[edge[0]] = colour
                colouring[edge[1]] = colour
            colouring_tuple = tuple(colouring)
            if len(set(colouring_tuple)) == 1:
                continue
            allowed = [
                matching
                for matching in system.matchings
                if matching_allows_colouring(
                    arcs, matching, colouring_tuple
                )
            ]
            if allowed == [mixed_matching]:
                return {
                    "mixed_matching": mixed_matching,
                    "matching_edge_colours": matching_colours,
                    "induced_colouring": colouring_tuple,
                }
    return None


def audit_pattern(
    system: EquationSystem, pattern: Pattern
) -> dict[str, object]:
    """Check feasibility and whether every possible nonzero triple certifies."""

    arcs = pattern_arcs(pattern)
    choices = tuple(
        monochromatic_matchings(system, arcs, colour)
        for colour in range(3)
    )
    counts = [len(matchings) for matchings in choices]
    if any(count == 0 for count in counts):
        return {
            "status": "monochromatically_infeasible",
            "monochromatic_matching_counts": counts,
        }

    uncertified: list[tuple[Matching, Matching, Matching]] = []
    first_certificate: dict[str, object] | None = None
    triple_count = 0
    for selected in itertools.product(*choices):
        triple_count += 1
        certificate = certificate_for_matching_triple(
            system, pattern, selected
        )
        if certificate is None:
            uncertified.append(selected)
        elif first_certificate is None:
            first_certificate = {
                "selected_monochromatic_matchings": selected,
                **certificate,
            }

    return {
        "status": (
            "combinatorially_eliminated"
            if not uncertified
            else "requires_algebraic_analysis"
        ),
        "monochromatic_matching_counts": counts,
        "matching_triples": triple_count,
        "uncertified_triples": len(uncertified),
        "first_uncertified_triple": (
            uncertified[0] if uncertified else None
        ),
        "first_certificate": first_certificate,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", type=Path)
    parser.add_argument("--samples", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    if args.pattern is None and args.samples <= 0:
        parser.error("provide --pattern or a positive --samples")
    system = EquationSystem(6, 3)
    if args.pattern is not None:
        payload = json.loads(args.pattern.read_text(encoding="utf-8"))
        pattern = payload.get("pattern", payload)
        print(json.dumps(audit_pattern(system, pattern), indent=2))

    if args.samples > 0:
        rng = np.random.default_rng(args.seed)
        counts: dict[str, int] = {}
        for _ in range(args.samples):
            result = audit_pattern(system, random_pattern(6, rng))
            status = str(result["status"])
            counts[status] = counts.get(status, 0) + 1
        print(json.dumps({"samples": args.samples, "counts": counts}, indent=2))


if __name__ == "__main__":
    main()
