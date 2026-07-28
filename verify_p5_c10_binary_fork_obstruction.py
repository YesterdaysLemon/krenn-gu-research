#!/usr/bin/env python3
"""Verify binary-fork affine obstructions in 1,328 exact-three C10 orbits."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp

import generate_p5_exact_three_partial_support_system as GENERATOR
import generate_p5_one_partial_support_system as BASE


ROOT = Path(__file__).resolve().parent
CATALOGUE = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c10_audit"
    / "sat_catalogue_c10.json"
)
EXPECTED_HITS = 1_328
EXPECTED_HIT_SHA256 = (
    "05436f68e3c7377ca4ee05245cc93923e849b9ef86c92d64e2de180c2f6363b8"
)
IDEAL = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)
Polynomial = tuple[tuple[int, int], ...]


def mixed_polynomials(
    supports: tuple[tuple[int, ...], ...],
) -> list[Polynomial]:
    """Regenerate normalized mixed coefficients with integer bitmasks."""
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
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    if len(tree_edges) != 19:
        raise AssertionError("gauge dimensions changed")

    entries: dict[tuple[int, int, int], int | None] = {}
    for mode in BASE.MODES:
        for source in BASE.SOURCES:
            for colour in BASE.COLOURS:
                edge = (mode, source, colour)
                if edge in tree_edges:
                    entries[edge] = 0
                elif edge in free_position:
                    entries[edge] = 1 << free_position[edge]
                else:
                    entries[edge] = None

    output = []
    seen = set()
    for colours in BASE.ALL_COLOURINGS:
        if len(set(colours)) == 1:
            continue
        terms: Counter[int] = Counter()
        for permutation in BASE.PERMUTATIONS:
            monomial = 0
            for mode, source in enumerate(permutation):
                factor = entries[(mode, source, colours[mode])]
                if factor is None:
                    break
                monomial |= factor
            else:
                terms[monomial] += 1
        if not terms:
            continue
        common = next(iter(terms))
        for monomial in terms:
            common &= monomial
        polynomial = tuple(
            sorted(
                (monomial & ~common, coefficient)
                for monomial, coefficient in terms.items()
            )
        )
        if polynomial not in seen:
            seen.add(polynomial)
            output.append(polynomial)
    return output


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    total: Counter[int] = Counter(dict(left))
    total.update(dict(right))
    return tuple(sorted(total.items()))


def binary_fork(polynomials: list[Polynomial]) -> dict | None:
    """Find P=1+mA, Q=1+mB, R=A+B."""
    locations = {
        polynomial: index for index, polynomial in enumerate(polynomials)
    }
    candidates: defaultdict[
        int, list[tuple[int, Polynomial]]
    ] = defaultdict(list)
    for index, polynomial in enumerate(polynomials):
        terms = dict(polynomial)
        if terms.get(0) != 1:
            continue
        nonconstant = {
            monomial: coefficient
            for monomial, coefficient in terms.items()
            if monomial
        }
        if not nonconstant:
            continue
        multiplier = next(iter(nonconstant))
        for monomial in nonconstant:
            multiplier &= monomial
        common = multiplier
        while True:
            reduced = tuple(
                sorted(
                    (monomial & ~multiplier, coefficient)
                    for monomial, coefficient in nonconstant.items()
                )
            )
            candidates[multiplier].append((index, reduced))
            if multiplier == 0:
                break
            multiplier = (multiplier - 1) & common

    for multiplier in sorted(candidates):
        group = candidates[multiplier]
        for (left_index, left), (
            right_index,
            right,
        ) in itertools.combinations(group, 2):
            joined = add(left, right)
            if joined in locations:
                return {
                    "left": left_index,
                    "right": right_index,
                    "sum": locations[joined],
                    "multiplier_mask": multiplier,
                    "certificate": (
                        "left + right - multiplier*sum = 2"
                    ),
                }
    return None


def sympy_polynomial(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> Polynomial:
    polynomial = sp.Poly(expression, *variables)
    terms = []
    for exponents, coefficient in polynomial.terms():
        if coefficient.q != 1 or any(
            value not in (0, 1) for value in exponents
        ):
            raise AssertionError("coefficient is not squarefree integral")
        mask = sum(
            1 << index
            for index, value in enumerate(exponents)
            if value
        )
        terms.append((mask, int(coefficient)))
    return tuple(sorted(terms))


def main() -> None:
    payload = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    if (
        payload.get("status") != "COMPLETE"
        or payload.get("shape") != "c10"
        or payload.get("partial_cells") != 3
        or payload.get("support_orbits") != 11_751
    ):
        raise AssertionError("C10 catalogue metadata changed")

    hits = []
    fast_systems = {}
    for position, case in enumerate(payload["cases"]):
        supports = tuple(tuple(row) for row in case["supports"])
        polynomials = mixed_polynomials(supports)
        certificate = binary_fork(polynomials)
        if certificate is None:
            continue
        if case.get("orbit_index") != position:
            raise AssertionError("catalogue orbit ordering changed")
        hit = {
            "orbit_index": case["orbit_index"],
            "catalogue_position": position,
            **certificate,
        }
        hits.append(hit)
        fast_systems[position] = polynomials

    hit_data = json.dumps(
        hits, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    hit_hash = hashlib.sha256(hit_data).hexdigest()
    if len(hits) != EXPECTED_HITS or hit_hash != EXPECTED_HIT_SHA256:
        raise AssertionError("binary-fork census changed")

    variables = sp.symbols("u0:23")
    local = {
        f"u{index}": symbol
        for index, symbol in enumerate(variables)
    }
    for hit in hits:
        case = payload["cases"][hit["catalogue_position"]]
        supports = tuple(tuple(row) for row in case["supports"])
        signatures = tuple(case["witness_signature_indices"])
        program, metadata = GENERATOR.generate(supports, signatures)
        match = IDEAL.search(program)
        if match is None:
            raise AssertionError("full generator output is unrecognized")
        equations = match.group("equations").split(",\n")[:-1]
        if (
            len(equations) != metadata["mixed_equations"]
            or len(equations) != len(fast_systems[hit["catalogue_position"]])
        ):
            raise AssertionError("mixed-equation count changed")
        indices = (hit["left"], hit["right"], hit["sum"])
        expressions = [
            sp.sympify(equations[index], locals=local)
            for index in indices
        ]
        for index, expression in zip(indices, expressions, strict=True):
            if (
                sympy_polynomial(expression, variables)
                != fast_systems[hit["catalogue_position"]][index]
            ):
                raise AssertionError("independent generators disagree")
        multiplier = sp.prod(
            variables[index]
            for index in range(len(variables))
            if hit["multiplier_mask"] & (1 << index)
        )
        if sp.expand(
            expressions[0]
            + expressions[1]
            - multiplier * expressions[2]
            - 2
        ) != 0:
            raise AssertionError("binary-fork identity failed")

    multiplier_histogram = Counter(
        hit["multiplier_mask"] for hit in hits
    )
    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "exact-three-partial C10 support-semantic "
                    "survivor catalogue"
                ),
                "support_orbits_scanned": len(payload["cases"]),
                "binary_fork_affine_obstructions": len(hits),
                "remaining_after_this_rule": len(payload["cases"]) - len(hits),
                "certificate_identity": "P + Q - m*R = 2",
                "hit_sha256": hit_hash,
                "multiplier_histogram": {
                    str(mask): count
                    for mask, count in sorted(
                        multiplier_histogram.items()
                    )
                },
                "full_generator_identities_replayed": len(hits),
                "uses_saturation_equation": False,
                "uses_pure_nonzero_assumptions": False,
                "excluded_characteristic": 2,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
