#!/usr/bin/env python3
"""Verify 113 new four-equation triangle obstructions in the C10 catalogue."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter

import sympy as sp

import generate_p5_exact_three_partial_support_system as GENERATOR
import verify_p5_c10_binary_fork_obstruction as FORK


EXPECTED_TRIANGLES = 604
EXPECTED_NEW_TRIANGLES = 113
EXPECTED_UNION = 1_441
EXPECTED_NEW_HIT_SHA256 = (
    "28feb91d7eaaacafa9bf16967af37d1f1f3a402738d42c37c27777e33b7c3bb3"
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


def triangle(polynomials: list[Polynomial]) -> dict | None:
    """Find P=1+mA, X=A+B, Y=A+C, Z=B+C."""
    locations = {
        polynomial: index for index, polynomial in enumerate(polynomials)
    }
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
            a = tuple(
                sorted(
                    (monomial & ~multiplier, coefficient)
                    for monomial, coefficient in nonconstant.items()
                )
            )
            extensions = []
            for index, candidate in enumerate(polynomials):
                if index == constant_index:
                    continue
                remainder = subtract(candidate, a)
                if remainder is not None:
                    extensions.append((index, remainder))
            for (left_index, b), (
                right_index,
                c,
            ) in itertools.combinations(extensions, 2):
                opposite = FORK.add(b, c)
                opposite_index = locations.get(opposite)
                if (
                    opposite_index is not None
                    and opposite_index
                    not in (
                        constant_index,
                        left_index,
                        right_index,
                    )
                ):
                    return {
                        "constant": constant_index,
                        "left": left_index,
                        "right": right_index,
                        "opposite": opposite_index,
                        "multiplier_mask": multiplier,
                        "certificate": (
                            "2*constant - multiplier*left "
                            "- multiplier*right "
                            "+ multiplier*opposite = 2"
                        ),
                    }
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

    fork_count = 0
    triangle_count = 0
    new_hits = []
    fast_systems = {}
    for position, case in enumerate(payload["cases"]):
        supports = tuple(tuple(row) for row in case["supports"])
        polynomials = FORK.mixed_polynomials(supports)
        fork = FORK.binary_fork(polynomials)
        certificate = triangle(polynomials)
        if fork is not None:
            fork_count += 1
        if certificate is None:
            continue
        triangle_count += 1
        if fork is not None:
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
        fork_count != FORK.EXPECTED_HITS
        or triangle_count != EXPECTED_TRIANGLES
        or len(new_hits) != EXPECTED_NEW_TRIANGLES
        or fork_count + len(new_hits) != EXPECTED_UNION
        or new_hit_hash != EXPECTED_NEW_HIT_SHA256
    ):
        raise AssertionError("triangle census changed")

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
        indices = (
            hit["constant"],
            hit["left"],
            hit["right"],
            hit["opposite"],
        )
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
        if sp.expand(
            2 * expressions[0]
            - multiplier * expressions[1]
            - multiplier * expressions[2]
            + multiplier * expressions[3]
            - 2
        ) != 0:
            raise AssertionError("triangle identity failed")

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
                "binary_fork_obstructions": fork_count,
                "triangle_obstructions": triangle_count,
                "new_triangle_obstructions": len(new_hits),
                "union_obstructions": fork_count + len(new_hits),
                "remaining_after_union": (
                    len(payload["cases"]) - fork_count - len(new_hits)
                ),
                "certificate_identity": "2P - mX - mY + mZ = 2",
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
