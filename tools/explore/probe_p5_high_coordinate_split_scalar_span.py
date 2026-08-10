#!/usr/bin/env python3
"""Probe high-coordinate closures for split-system scalar identities."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu import p5_support_system as GENERATOR
from krenn_gu import p5_high_coordinate as HIGH


PRIME = 1_000_003
Polynomial = tuple[tuple[int, int], ...]


def split_polynomials(
    supports: tuple[tuple[int, ...], ...],
    gauge_forest: tuple[tuple[int, int, int], ...] = (),
) -> tuple[tuple[Polynomial, ...], dict]:
    """Regenerate the three inverse-pure and all mixed equations.

    This is the polynomial system emitted by the split-saturation
    converter when only the three pure coefficients are saturated.
    Monomials are represented by arbitrary-width Python bitmasks.
    """
    edges = tuple(
        (mode, source, colour)
        for mode in GENERATOR.MODES
        for source in GENERATOR.SOURCES
        for colour in GENERATOR.COLOURS
        if supports[mode][source] & (1 << colour)
    )
    if (
        len(set(gauge_forest)) != len(gauge_forest)
        or any(edge not in edges for edge in gauge_forest)
    ):
        raise ValueError("invalid gauge forest")
    tree_edges = set(gauge_forest)
    free_edges = tuple(edge for edge in edges if edge not in tree_edges)
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }

    nodes = tuple(
        ("r", source) for source in GENERATOR.SOURCES
    ) + tuple(
        ("c", mode, colour)
        for mode in GENERATOR.MODES
        for colour in GENERATOR.COLOURS
    )
    union_find = GENERATOR.UnionFind(nodes)
    for mode, source, colour in gauge_forest:
        if not union_find.union(
            ("r", source), ("c", mode, colour)
        ):
            raise ValueError("gauge forest contains a cycle")

    def entry(mode: int, source: int, colour: int) -> int | None:
        edge = (mode, source, colour)
        if edge in tree_edges:
            return 0
        position = free_position.get(edge)
        return None if position is None else 1 << position

    mixed: list[Polynomial] = []
    mixed_seen: set[Polynomial] = set()
    pure: list[Polynomial] = []
    for colours in GENERATOR.ALL_COLOURINGS:
        terms: Counter[int] = Counter()
        for permutation in GENERATOR.PERMUTATIONS:
            monomial = 0
            for mode, source in enumerate(permutation):
                factor = entry(mode, source, colours[mode])
                if factor is None:
                    break
                monomial |= factor
            else:
                terms[monomial] += 1
        polynomial = tuple(sorted(terms.items()))
        if len(set(colours)) == 1:
            pure.append(polynomial)
        elif polynomial and polynomial not in mixed_seen:
            mixed_seen.add(polynomial)
            mixed.append(polynomial)
    if len(pure) != 3:
        raise AssertionError("pure coefficient count changed")

    inverse_pure = []
    for index, polynomial in enumerate(pure):
        inverse_bit = 1 << (len(free_edges) + index)
        terms = Counter({0: -1})
        for monomial, coefficient in polynomial:
            terms[monomial | inverse_bit] += coefficient
        inverse_pure.append(
            tuple(
                sorted(
                    (monomial, coefficient)
                    for monomial, coefficient in terms.items()
                    if coefficient
                )
            )
        )
    equations = tuple(inverse_pure + mixed)
    return equations, {
        "supported_entries": len(edges),
        "gauge_forest_edges": len(gauge_forest),
        "free_variables": len(free_edges),
        "inverse_pure_equations": len(inverse_pure),
        "mixed_equations": len(mixed),
        "monomials": len(
            {
                monomial
                for polynomial in equations
                for monomial, _coefficient in polynomial
            }
        ),
    }


def axpy(
    target: dict[int, int],
    factor: int,
    source: dict[int, int],
) -> None:
    for key, coefficient in source.items():
        value = (
            target.get(key, 0) + factor * coefficient
        ) % PRIME
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def modular_constant_certificate(
    polynomials: tuple[Polynomial, ...],
) -> dict[int, int] | None:
    """Express the constant monomial in the scalar span over F_p."""
    return modular_span_certificate(polynomials, ((0, 1),))


def modular_span_certificate(
    polynomials: tuple[Polynomial, ...],
    target: Polynomial,
) -> dict[int, int] | None:
    """Express one polynomial in a coefficient span over F_p."""
    basis: dict[
        int, tuple[dict[int, int], dict[int, int]]
    ] = {}
    for equation_index, polynomial in enumerate(polynomials):
        vector = {
            monomial: coefficient % PRIME
            for monomial, coefficient in polynomial
            if coefficient % PRIME
        }
        combination = {equation_index: 1}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = pow(vector[pivot], -1, PRIME)
                vector = {
                    key: value * inverse % PRIME
                    for key, value in vector.items()
                    if value * inverse % PRIME
                }
                combination = {
                    key: value * inverse % PRIME
                    for key, value in combination.items()
                    if value * inverse % PRIME
                }
                basis[pivot] = (vector, combination)
                break
            factor = -vector[pivot]
            basis_vector, basis_combination = basis[pivot]
            axpy(vector, factor, basis_vector)
            axpy(combination, factor, basis_combination)

    vector = {
        monomial: coefficient % PRIME
        for monomial, coefficient in target
        if coefficient % PRIME
    }
    combination: dict[int, int] = {}
    while vector:
        pivot = min(vector)
        if pivot not in basis:
            return None
        factor = -vector[pivot]
        basis_vector, basis_combination = basis[pivot]
        axpy(vector, factor, basis_vector)
        axpy(combination, factor, basis_combination)
    return {
        index: (-coefficient) % PRIME
        for index, coefficient in combination.items()
        if coefficient
    }


def rational_reconstruction(value: int) -> Fraction | None:
    residue = value % PRIME
    r0, s0 = PRIME, 0
    r1, s1 = residue, 1
    bound = math.sqrt(PRIME / 2)
    while r1 >= bound:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        s0, s1 = s1, s0 - quotient * s1
    if s1 == 0 or abs(s1) >= bound:
        return None
    if s1 < 0:
        numerator, denominator = -r1, -s1
    else:
        numerator, denominator = r1, s1
    if (numerator - residue * denominator) % PRIME:
        return None
    return Fraction(numerator, denominator)


def exact_residual(
    polynomials: tuple[Polynomial, ...],
    coefficients: dict[int, Fraction],
    target: Polynomial = ((0, 1),),
) -> dict[int, Fraction]:
    residual = {
        monomial: -Fraction(coefficient)
        for monomial, coefficient in target
        if coefficient
    }
    for index, coefficient in coefficients.items():
        for monomial, value in polynomials[index]:
            updated = (
                residual.get(monomial, Fraction())
                + coefficient * value
            )
            if updated:
                residual[monomial] = updated
            else:
                residual.pop(monomial, None)
    return residual


def exact_constant_certificate(
    polynomials: tuple[Polynomial, ...],
) -> dict[int, Fraction] | None:
    modular = modular_constant_certificate(polynomials)
    if modular is None:
        return None
    rational = {}
    for index, value in modular.items():
        reconstructed = rational_reconstruction(value)
        if reconstructed is None:
            return None
        rational[index] = reconstructed
    if exact_residual(polynomials, rational):
        return None
    return rational


def pure_in_mixed_span_certificate(
    split: tuple[Polynomial, ...],
    free_variables: int,
) -> tuple[int, dict[int, Fraction]] | None:
    """Find a required pure coefficient in the mixed-coefficient span."""
    mixed = split[3:]
    for colour, inverse_equation in enumerate(split[:3]):
        inverse_bit = 1 << (free_variables + colour)
        pure = tuple(
            sorted(
                (monomial ^ inverse_bit, coefficient)
                for monomial, coefficient in inverse_equation
                if monomial
                and monomial & inverse_bit
            )
        )
        if (
            len(pure) + 1 != len(inverse_equation)
            or dict(inverse_equation).get(0) != -1
        ):
            raise AssertionError("inverse-pure equation changed")
        modular = modular_span_certificate(mixed, pure)
        if modular is None:
            continue
        rational = {}
        for index, value in modular.items():
            reconstructed = rational_reconstruction(value)
            if reconstructed is None:
                break
            rational[index] = reconstructed
        else:
            if not exact_residual(mixed, rational, pure):
                return colour, rational
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument(
        "--branch",
        choices=tuple(HIGH.BRANCH_BACKBONES),
        required=True,
    )
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    parser.add_argument(
        "--small-certificate-size",
        type=int,
        default=5,
    )
    args = parser.parse_args()
    if (
        args.offset < 0
        or (args.limit is not None and args.limit <= 0)
        or args.small_certificate_size <= 0
        or not 15 <= args.min_available_percent < 100
    ):
        raise ValueError("invalid probe arguments")

    state = json.loads(args.state.read_bytes())
    if state.get("branch") != args.branch:
        raise ValueError("state branch changed")
    records = state.get("records", [])
    stop = (
        len(records)
        if args.limit is None
        else min(len(records), args.offset + args.limit)
    )
    selected = records[args.offset:stop]

    exact_hits = []
    stored_zero = 0
    overlap = 0
    nonzero_forest_hits = 0
    modular_only = 0
    support_histogram: Counter[int] = Counter()
    denominator_histogram: Counter[int] = Counter()
    small = []
    for position, record in enumerate(
        selected, start=args.offset
    ):
        if (
            HIGH.available_memory_percent()
            < args.min_available_percent
        ):
            raise MemoryError(
                "available host memory fell below the requested floor"
            )
        closure = tuple(
            tuple(map(int, row))
            for row in record["closure_supports"]
        )
        polynomials, metadata = split_polynomials(closure)
        pure_span = pure_in_mixed_span_certificate(
            polynomials, metadata["free_variables"]
        )
        if pure_span is None:
            rational = None
            pure_colour = None
        else:
            pure_colour, rational = pure_span

        is_stored_zero = len(record.get("gauge_tree", ())) == 0
        stored_zero += is_stored_zero
        if rational is None:
            continue
        exact_hits.append(position)
        overlap += is_stored_zero
        nonzero_forest_hits += not is_stored_zero
        support_histogram[len(rational)] += 1
        denominator_histogram[
            max(value.denominator for value in rational.values())
        ] += 1
        if len(rational) <= args.small_certificate_size:
            small.append(
                {
                    "record_index": position,
                    "stored_zero_forest": is_stored_zero,
                    "coordinate_profile": record[
                        "coordinate_profile"
                    ],
                    "pure_colour": pure_colour,
                    "coefficients": {
                        str(index): [
                            value.numerator,
                            value.denominator,
                        ]
                        for index, value in sorted(rational.items())
                    },
                    "metadata": metadata,
                }
            )

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "required pure coefficient in rational mixed "
                    "coefficient span"
                ),
                "state": args.state.as_posix(),
                "branch": args.branch,
                "offset": args.offset,
                "records_scanned": len(selected),
                "stored_zero_forests": stored_zero,
                "exact_pure_span_certificates": len(exact_hits),
                "overlap_with_stored_zero_forests": overlap,
                "new_zero_forest_candidates": nonzero_forest_hits,
                "stored_zero_forests_not_scalar_certified": (
                    stored_zero - overlap
                ),
                "modular_hits_not_reconstructed_exactly": modular_only,
                "certificate_support_histogram": {
                    str(key): value
                    for key, value in sorted(
                        support_histogram.items()
                    )
                },
                "maximum_denominator_histogram": {
                    str(key): value
                    for key, value in sorted(
                        denominator_histogram.items()
                    )
                },
                "small_certificates": small,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
