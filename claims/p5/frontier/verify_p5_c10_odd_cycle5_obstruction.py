#!/usr/bin/env python3
"""Verify 74 new five-edge odd-cycle obstructions in the C10 catalogue."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from functools import lru_cache

import sympy as sp

import generate_p5_exact_three_partial_support_system as GENERATOR
import verify_p5_c10_binary_fork_obstruction as FORK
import verify_p5_c10_triangle_obstruction as TRIANGLE


EXPECTED_PRIOR_UNION = 1_441
EXPECTED_NEW_ODD_CYCLES = 74
EXPECTED_UNION = 1_515
EXPECTED_NEW_HIT_SHA256 = (
    "cb27bbb5b2d3d4c4bbf77b3eeb4041eae51777761a1a0597c4fb06d959625a0b"
)
Polynomial = FORK.Polynomial


def subtract(
    minuend: Polynomial, subtrahend: Polynomial
) -> Polynomial | None:
    values = dict(minuend)
    for monomial, coefficient in subtrahend:
        remaining = values.get(monomial, 0) - coefficient
        if remaining < 0:
            return None
        if remaining:
            values[monomial] = remaining
        else:
            values.pop(monomial, None)
    return tuple(sorted(values.items()))


def odd_cycle5(polynomials: list[Polynomial]) -> dict | None:
    """Find E_i=A_i+A_(i+1) around a simple five-cycle."""
    locations = {
        polynomial: index for index, polynomial in enumerate(polynomials)
    }

    @lru_cache(maxsize=None)
    def neighbors(
        component: Polynomial,
    ) -> tuple[tuple[int, Polynomial], ...]:
        result = []
        for index, polynomial in enumerate(polynomials):
            remainder = subtract(polynomial, component)
            if remainder is not None:
                result.append((index, remainder))
        return tuple(result)

    for constant_index, polynomial in enumerate(polynomials):
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
        common = next(iter(nonconstant))
        for monomial in nonconstant:
            common &= monomial
        multiplier = common
        while True:
            start = tuple(
                sorted(
                    (monomial & ~multiplier, coefficient)
                    for monomial, coefficient in nonconstant.items()
                )
            )
            stack = [(start, (), (start,))]
            while stack:
                component, edge_path, component_path = stack.pop()
                if len(edge_path) == 4:
                    closing = locations.get(
                        FORK.add(component, start)
                    )
                    if (
                        closing is not None
                        and closing not in edge_path
                        and len(set((*edge_path, closing))) == 5
                    ):
                        return {
                            "constant": constant_index,
                            "cycle_edges": [*edge_path, closing],
                            "multiplier_mask": multiplier,
                            "certificate": (
                                "2*constant - multiplier*"
                                "(e0-e1+e2-e3+e4) = 2"
                            ),
                        }
                    continue
                for edge, next_component in neighbors(component):
                    if (
                        edge in edge_path
                        or next_component in component_path
                    ):
                        continue
                    stack.append(
                        (
                            next_component,
                            (*edge_path, edge),
                            (*component_path, next_component),
                        )
                    )
            if multiplier == 0:
                break
            multiplier = (multiplier - 1) & common
    return None


def main() -> None:
    payload = json.loads(FORK.CATALOGUE.read_text(encoding="utf-8"))
    if (
        payload.get("status") != "COMPLETE"
        or payload.get("shape") != "c10"
        or payload.get("partial_cells") != 3
        or payload.get("support_orbits") != 11_751
    ):
        raise AssertionError("C10 catalogue metadata changed")

    prior_union = 0
    new_hits = []
    fast_systems = {}
    for position, case in enumerate(payload["cases"]):
        supports = tuple(tuple(row) for row in case["supports"])
        polynomials = FORK.mixed_polynomials(supports)
        if (
            FORK.binary_fork(polynomials) is not None
            or TRIANGLE.triangle(polynomials) is not None
        ):
            prior_union += 1
            continue
        certificate = odd_cycle5(polynomials)
        if certificate is None:
            continue
        if case.get("orbit_index") != position:
            raise AssertionError("catalogue orbit ordering changed")
        hit = {
            "orbit_index": case["orbit_index"],
            "catalogue_position": position,
            **certificate,
        }
        new_hits.append(hit)
        fast_systems[position] = polynomials

    new_hit_data = json.dumps(
        new_hits, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    new_hit_hash = hashlib.sha256(new_hit_data).hexdigest()
    if (
        prior_union != EXPECTED_PRIOR_UNION
        or len(new_hits) != EXPECTED_NEW_ODD_CYCLES
        or prior_union + len(new_hits) != EXPECTED_UNION
        or new_hit_hash != EXPECTED_NEW_HIT_SHA256
    ):
        raise AssertionError("five-cycle census changed")

    variables = sp.symbols("u0:23")
    local = {
        f"u{index}": symbol
        for index, symbol in enumerate(variables)
    }
    for hit in new_hits:
        case = payload["cases"][hit["catalogue_position"]]
        supports = tuple(tuple(row) for row in case["supports"])
        signatures = tuple(case["witness_signature_indices"])
        program, metadata = GENERATOR.generate(supports, signatures)
        match = FORK.IDEAL.search(program)
        if match is None:
            raise AssertionError("full generator output is unrecognized")
        equations = match.group("equations").split(",\n")[:-1]
        if (
            len(equations) != metadata["mixed_equations"]
            or len(equations) != len(fast_systems[hit["catalogue_position"]])
        ):
            raise AssertionError("mixed-equation count changed")
        indices = (hit["constant"], *hit["cycle_edges"])
        expressions = [
            sp.sympify(equations[index], locals=local)
            for index in indices
        ]
        for index, expression in zip(indices, expressions, strict=True):
            if (
                FORK.sympy_polynomial(expression, variables)
                != fast_systems[hit["catalogue_position"]][index]
            ):
                raise AssertionError("independent generators disagree")
        multiplier = sp.prod(
            variables[index]
            for index in range(len(variables))
            if hit["multiplier_mask"] & (1 << index)
        )
        alternating_cycle = sum(
            (-1) ** index * expression
            for index, expression in enumerate(expressions[1:])
        )
        if sp.expand(
            2 * expressions[0]
            - multiplier * alternating_cycle
            - 2
        ) != 0:
            raise AssertionError("five-cycle identity failed")

    multiplier_histogram = Counter(
        hit["multiplier_mask"] for hit in new_hits
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
                "prior_sparse_union": prior_union,
                "new_odd_cycle5_obstructions": len(new_hits),
                "union_obstructions": prior_union + len(new_hits),
                "remaining_after_union": (
                    len(payload["cases"]) - prior_union - len(new_hits)
                ),
                "certificate_identity": (
                    "2P - m*(E0-E1+E2-E3+E4) = 2"
                ),
                "new_hit_sha256": new_hit_hash,
                "new_multiplier_histogram": {
                    str(mask): count
                    for mask, count in sorted(
                        multiplier_histogram.items()
                    )
                },
                "full_generator_identities_replayed": len(new_hits),
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
