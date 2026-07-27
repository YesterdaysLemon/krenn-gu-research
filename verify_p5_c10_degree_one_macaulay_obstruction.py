#!/usr/bin/env python3
"""Verify 1,960 new degree-one Macaulay C10 obstructions."""

from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp

import generate_p5_exact_three_partial_support_system as GENERATOR
import verify_p5_c10_binary_fork_obstruction as FORK
import verify_p5_c10_odd_cycle5_obstruction as ODD5
import verify_p5_c10_scalar_span_obstruction as SCALAR
import verify_p5_c10_triangle_obstruction as TRIANGLE


ROOT = Path(__file__).resolve().parent
MANIFEST = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c10_audit"
    / "degree_one_macaulay_certificates.json"
)
EXPECTED_PRIOR_UNION = 1_690
EXPECTED_NEW_HITS = 1_960
EXPECTED_UNION = 3_650
EXPECTED_REMAINING = 8_101
EXPECTED_CERTIFICATE_SHA256 = (
    "ec7413fa10dfd4acaba533e2f6ff1e2c645fcaeea877d1362826955bb9ca47bd"
)
EXPECTED_DENOMINATORS = {1: 2, 2: 1_842, 4: 109, 6: 2, 8: 5}


def prior_certificate(polynomials: list[FORK.Polynomial]) -> bool:
    return (
        FORK.binary_fork(polynomials) is not None
        or TRIANGLE.triangle(polynomials) is not None
        or ODD5.odd_cycle5(polynomials) is not None
        or SCALAR.constant_certificate_mod(polynomials) is not None
    )


def rational_coefficients(
    record: dict,
) -> dict[tuple[int, int], Fraction]:
    output = {}
    for label, (numerator, denominator) in record[
        "rational_coefficients"
    ].items():
        equation, variable = map(int, label.split(":"))
        output[(equation, variable)] = Fraction(
            numerator,
            denominator,
        )
    return output


def exact_residual(
    polynomials: list[FORK.Polynomial],
    coefficients: dict[tuple[int, int], Fraction],
) -> dict[tuple[int, int], Fraction]:
    residual = {(0, 0): Fraction(-1)}
    for (equation, variable), coefficient in coefficients.items():
        for monomial, value in polynomials[equation]:
            if variable < 0:
                key = (monomial, 0)
            else:
                bit = 1 << variable
                key = (
                    monomial | bit,
                    bit if monomial & bit else 0,
                )
            updated = (
                residual.get(key, Fraction())
                + coefficient * value
            )
            if updated:
                residual[key] = updated
            else:
                residual.pop(key, None)
    return residual


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    catalogue = json.loads(
        FORK.CATALOGUE.read_text(encoding="utf-8")
    )
    records = manifest["certificates"]
    certificate_data = json.dumps(
        records,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    certificate_hash = hashlib.sha256(certificate_data).hexdigest()
    orbits = [record["orbit_index"] for record in records]
    orbit_set = set(orbits)
    if (
        manifest.get("verified") is not True
        or manifest.get("previously_uncovered_orbits_scanned") != 10_061
        or manifest.get("degree_one_modular_hits") != EXPECTED_NEW_HITS
        or manifest.get("exact_rational_degree_one_hits")
        != EXPECTED_NEW_HITS
        or manifest.get("all_modular_hits_reconstructed_exactly")
        is not True
        or manifest.get("prior_certified_union")
        != EXPECTED_PRIOR_UNION
        or manifest.get("new_certified_union") != EXPECTED_UNION
        or manifest.get("not_certified_after_union")
        != EXPECTED_REMAINING
        or manifest.get("certificate_sha256")
        != EXPECTED_CERTIFICATE_SHA256
        or certificate_hash != EXPECTED_CERTIFICATE_SHA256
        or len(records) != EXPECTED_NEW_HITS
        or orbits != sorted(set(orbits))
    ):
        raise AssertionError("degree-one manifest metadata changed")

    prior_orbits = set()
    fast_by_orbit = {}
    for case in catalogue["cases"]:
        supports = tuple(tuple(row) for row in case["supports"])
        polynomials = FORK.mixed_polynomials(supports)
        if prior_certificate(polynomials):
            prior_orbits.add(case["orbit_index"])
        if case["orbit_index"] in orbit_set:
            fast_by_orbit[case["orbit_index"]] = polynomials
    if (
        len(prior_orbits) != EXPECTED_PRIOR_UNION
        or prior_orbits.intersection(orbits)
        or len(fast_by_orbit) != EXPECTED_NEW_HITS
    ):
        raise AssertionError("prior/new certificate partition changed")

    denominator_histogram: Counter[int] = Counter()
    support_histogram: Counter[int] = Counter()
    for record in records:
        coefficients = rational_coefficients(record)
        if exact_residual(
            fast_by_orbit[record["orbit_index"]],
            coefficients,
        ):
            raise AssertionError("fast degree-one identity failed")
        support_histogram[len(coefficients)] += 1
        denominator_histogram[
            max(value.denominator for value in coefficients.values())
        ] += 1
    if dict(denominator_histogram) != EXPECTED_DENOMINATORS:
        raise AssertionError("certificate denominators changed")

    variables = sp.symbols("u0:23")
    local = {
        f"u{index}": symbol
        for index, symbol in enumerate(variables)
    }
    started = time.monotonic()
    for position, record in enumerate(records, start=1):
        orbit = record["orbit_index"]
        case = catalogue["cases"][orbit]
        if case["orbit_index"] != orbit:
            raise AssertionError("catalogue orbit ordering changed")
        supports = tuple(tuple(row) for row in case["supports"])
        signatures = tuple(case["witness_signature_indices"])
        program, metadata = GENERATOR.generate(supports, signatures)
        match = FORK.IDEAL.search(program)
        if match is None:
            raise AssertionError("full generator output is unrecognized")
        equations = match.group("equations").split(",\n")[:-1]
        fast_polynomials = fast_by_orbit[orbit]
        if (
            len(equations) != metadata["mixed_equations"]
            or len(equations) != len(fast_polynomials)
        ):
            raise AssertionError("mixed-equation count changed")

        identity = sp.Integer(-1)
        expressions = {}
        for (equation, variable), coefficient in (
            rational_coefficients(record).items()
        ):
            expression = expressions.get(equation)
            if expression is None:
                expression = sp.sympify(
                    equations[equation],
                    locals=local,
                )
                if (
                    FORK.sympy_polynomial(expression, variables)
                    != fast_polynomials[equation]
                ):
                    raise AssertionError(
                        "independent generators disagree"
                    )
                expressions[equation] = expression
            multiplier = (
                sp.Integer(1)
                if variable < 0
                else variables[variable]
            )
            identity += (
                sp.Rational(
                    coefficient.numerator,
                    coefficient.denominator,
                )
                * multiplier
                * expression
            )
        if sp.expand(identity) != 0:
            raise AssertionError(
                "full-generator degree-one identity failed"
            )
        if position % 100 == 0:
            print(
                json.dumps(
                    {
                        "replay_position": position,
                        "replay_total": len(records),
                        "seconds": round(
                            time.monotonic() - started,
                            1,
                        ),
                    }
                ),
                flush=True,
            )

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "exact-three-partial C10 support-semantic "
                    "survivor catalogue"
                ),
                "support_orbits": len(catalogue["cases"]),
                "prior_certified_union": len(prior_orbits),
                "new_degree_one_rational_certificates": len(records),
                "certified_union": len(prior_orbits) + len(records),
                "not_certified_after_union": (
                    len(catalogue["cases"])
                    - len(prior_orbits)
                    - len(records)
                ),
                "certificate_identity": (
                    "sum((a_i + sum(b_ij*u_j))*F_i) = 1"
                ),
                "certificate_sha256": certificate_hash,
                "certificate_support_range": [
                    min(support_histogram),
                    max(support_histogram),
                ],
                "maximum_denominator_histogram": {
                    str(key): value
                    for key, value in sorted(
                        denominator_histogram.items()
                    )
                },
                "full_generator_identities_replayed": len(records),
                "uses_saturation_equation": False,
                "uses_pure_nonzero_assumptions": False,
                "modular_misses_prove_rational_nonmembership": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
