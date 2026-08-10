#!/usr/bin/env python3
"""Verify scalar-span obstructions in 1,523 exact-three C10 orbits."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

import generate_p5_exact_three_partial_support_system as GENERATOR
import verify_p5_c10_binary_fork_obstruction as FORK
import verify_p5_c10_odd_cycle5_obstruction as ODD5
import verify_p5_c10_triangle_obstruction as TRIANGLE


PRIME = 1_000_003
EXPECTED_SCALAR_HITS = 1_523
EXPECTED_PRIOR_UNION = 1_515
EXPECTED_OVERLAP = 1_348
EXPECTED_NEW_HITS = 175
EXPECTED_UNION = 1_690
EXPECTED_CERTIFICATE_SHA256 = (
    "a2fdf4bc3478df94d5b09d68b4df195ebcc400164e47c5ed1b3db3aad12016ee"
)
EXPECTED_NEW_CERTIFICATE_SHA256 = (
    "4d6ff9fdfb3808a4b692201a205722965ca74f0470c85d325266cf7e72227d10"
)
Polynomial = FORK.Polynomial


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


def constant_certificate_mod(
    polynomials: list[Polynomial],
) -> dict[int, int] | None:
    """Express the constant monomial in the coefficient span over F_p."""
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

    vector = {0: 1}
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
    """Wang rational reconstruction with the standard sqrt(p/2) bound."""
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
    polynomials: list[Polynomial],
    coefficients: dict[int, Fraction],
) -> dict[int, Fraction]:
    residual = {0: Fraction(-1)}
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


def certificate_record(
    orbit_index: int,
    coefficients: dict[int, Fraction],
) -> dict:
    return {
        "orbit_index": orbit_index,
        "rational_coefficients": {
            str(index): [
                value.numerator,
                value.denominator,
            ]
            for index, value in sorted(coefficients.items())
        },
    }


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
    scalar_records = []
    new_records = []
    support_histogram: Counter[int] = Counter()
    denominator_histogram: Counter[int] = Counter()
    for position, case in enumerate(payload["cases"]):
        supports = tuple(tuple(row) for row in case["supports"])
        polynomials = FORK.mixed_polynomials(supports)
        prior = (
            FORK.binary_fork(polynomials) is not None
            or TRIANGLE.triangle(polynomials) is not None
            or ODD5.odd_cycle5(polynomials) is not None
        )
        if prior:
            prior_union += 1

        modular = constant_certificate_mod(polynomials)
        if modular is None:
            continue
        rational = {}
        for index, value in modular.items():
            reconstructed = rational_reconstruction(value)
            if reconstructed is None:
                raise AssertionError("rational reconstruction failed")
            rational[index] = reconstructed
        if exact_residual(polynomials, rational):
            raise AssertionError("reconstructed scalar identity failed")
        record = certificate_record(case["orbit_index"], rational)
        scalar_records.append(record)
        support_histogram[len(rational)] += 1
        denominator_histogram[
            max(value.denominator for value in rational.values())
        ] += 1
        if not prior:
            if case.get("orbit_index") != position:
                raise AssertionError("catalogue orbit ordering changed")
            new_records.append(record)

    certificate_data = json.dumps(
        scalar_records, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    certificate_hash = hashlib.sha256(certificate_data).hexdigest()
    new_certificate_data = json.dumps(
        new_records, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    new_certificate_hash = hashlib.sha256(
        new_certificate_data
    ).hexdigest()
    overlap = len(scalar_records) - len(new_records)
    if (
        len(scalar_records) != EXPECTED_SCALAR_HITS
        or prior_union != EXPECTED_PRIOR_UNION
        or overlap != EXPECTED_OVERLAP
        or len(new_records) != EXPECTED_NEW_HITS
        or prior_union + len(new_records) != EXPECTED_UNION
        or certificate_hash != EXPECTED_CERTIFICATE_SHA256
        or new_certificate_hash != EXPECTED_NEW_CERTIFICATE_SHA256
    ):
        raise AssertionError("scalar-span census changed")

    variables = sp.symbols("u0:23")
    local = {
        f"u{index}": symbol
        for index, symbol in enumerate(variables)
    }
    for record in new_records:
        orbit = record["orbit_index"]
        case = payload["cases"][orbit]
        supports = tuple(tuple(row) for row in case["supports"])
        fast_polynomials = FORK.mixed_polynomials(supports)
        signatures = tuple(case["witness_signature_indices"])
        program, metadata = GENERATOR.generate(supports, signatures)
        match = FORK.IDEAL.search(program)
        if match is None:
            raise AssertionError("full generator output is unrecognized")
        equations = match.group("equations").split(",\n")[:-1]
        if (
            len(equations) != metadata["mixed_equations"]
            or len(equations) != len(fast_polynomials)
        ):
            raise AssertionError("mixed-equation count changed")
        identity = sp.Integer(-1)
        for index_text, fraction in record[
            "rational_coefficients"
        ].items():
            index = int(index_text)
            expression = sp.sympify(equations[index], locals=local)
            if (
                FORK.sympy_polynomial(expression, variables)
                != fast_polynomials[index]
            ):
                raise AssertionError("independent generators disagree")
            identity += (
                sp.Rational(fraction[0], fraction[1]) * expression
            )
        if sp.expand(identity) != 0:
            raise AssertionError("full-generator scalar identity failed")

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "exact-three-partial C10 support-semantic "
                    "survivor catalogue"
                ),
                "support_orbits_scanned": len(payload["cases"]),
                "certified_rational_scalar_span_obstructions": len(
                    scalar_records
                ),
                "prior_sparse_union": prior_union,
                "scalar_overlap_with_prior": overlap,
                "new_scalar_span_obstructions": len(new_records),
                "union_obstructions": prior_union + len(new_records),
                "not_certified_after_union": (
                    len(payload["cases"])
                    - prior_union
                    - len(new_records)
                ),
                "certificate_identity": "sum(q_i*F_i) = 1",
                "certificate_sha256": certificate_hash,
                "new_certificate_sha256": new_certificate_hash,
                "certificate_support_histogram": {
                    str(size): count
                    for size, count in sorted(
                        support_histogram.items()
                    )
                },
                "maximum_denominator_histogram": {
                    str(denominator): count
                    for denominator, count in sorted(
                        denominator_histogram.items()
                    )
                },
                "new_full_generator_identities_replayed": len(
                    new_records
                ),
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
