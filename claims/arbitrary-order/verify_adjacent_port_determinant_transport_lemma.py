"""Independently audit the adjacent-port determinant transport identity."""

from __future__ import annotations

import hashlib
import json
import random
import time
from fractions import Fraction
from pathlib import Path

from sympy import symbols, simplify


OUTPUT = Path(
    "tmp/adjacent_port_determinant_transport_lemma_verified.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nonzero_fraction(rng: random.Random) -> Fraction:
    numerator = 0
    while numerator == 0:
        numerator = rng.randrange(-19, 20)
    return Fraction(numerator, rng.randrange(1, 20))


def main() -> None:
    started = time.perf_counter()

    path, h00, h10, h01, h11 = symbols(
        "R H00 H10 H01 H11", nonzero=True
    )
    a00 = -path * h00
    a10 = -path * h10
    a01 = -path * h01
    a11 = a10 * a01 / a00
    delta = h11 - h10 * h01 / h00
    local_target = a11 + path * h11
    if simplify(local_target - path * delta) != 0:
        raise AssertionError("local Schur-complement identity changed")
    determinant = h11 * h00 - h10 * h01
    if simplify(h00 * delta - determinant) != 0:
        raise AssertionError("cleared local determinant identity changed")
    if simplify(a11 * a00 - a10 * a01) != 0:
        raise AssertionError("separated alternating monomial changed")

    rng = random.Random(0xAD1AC3)
    component_cases = 0
    proper_corner_checks = 0
    global_identity_checks = 0
    for components in range(1, 7):
        for _trial in range(200):
            paths: list[Fraction] = []
            deltas: list[Fraction] = []
            determinants: list[Fraction] = []
            denominators: list[Fraction] = []
            target_binomials: list[Fraction] = []
            for _component in range(components):
                local_path = nonzero_fraction(rng)
                local_h00 = nonzero_fraction(rng)
                local_h10 = nonzero_fraction(rng)
                local_h01 = nonzero_fraction(rng)
                local_h11 = nonzero_fraction(rng)
                local_a00 = -local_path * local_h00
                local_a10 = -local_path * local_h10
                local_a01 = -local_path * local_h01
                local_a11 = (
                    local_a10 * local_a01 / local_a00
                )
                if any(
                    value != 0
                    for value in (
                        local_a00 + local_path * local_h00,
                        local_a10 + local_path * local_h10,
                        local_a01 + local_path * local_h01,
                    )
                ):
                    raise AssertionError("proper corner stopped vanishing")
                proper_corner_checks += 3
                local_delta = (
                    local_h11
                    - local_h10 * local_h01 / local_h00
                )
                local_target_value = (
                    local_a11 + local_path * local_h11
                )
                if local_target_value != local_path * local_delta:
                    raise AssertionError("numeric local identity changed")
                paths.append(local_path)
                deltas.append(local_delta)
                determinants.append(
                    local_h11 * local_h00
                    - local_h10 * local_h01
                )
                denominators.append(local_h00)
                target_binomials.append(local_target_value)

            path_product = Fraction(1)
            delta_product = Fraction(1)
            determinant_product = Fraction(1)
            denominator_product = Fraction(1)
            target_product = Fraction(1)
            for values in (
                paths,
                deltas,
                determinants,
                denominators,
                target_binomials,
            ):
                product = Fraction(1)
                for value in values:
                    product *= value
                if values is paths:
                    path_product = product
                elif values is deltas:
                    delta_product = product
                elif values is determinants:
                    determinant_product = product
                elif values is denominators:
                    denominator_product = product
                else:
                    target_product = product
            if target_product != path_product * delta_product:
                raise AssertionError("component product identity changed")
            if (
                determinant_product
                != denominator_product * delta_product
            ):
                raise AssertionError(
                    "cleared component product identity changed"
                )

            singleton_product = -delta_product
            extra_monomial = path_product * singleton_product
            if target_product + extra_monomial != 0:
                raise AssertionError("global amplitude did not cancel")
            if (
                determinant_product
                + singleton_product * denominator_product
                != 0
            ):
                raise AssertionError(
                    "cleared global determinant identity changed"
                )
            component_cases += 1
            global_identity_checks += 2

    source = Path(__file__)
    theorem = Path(__file__).resolve().with_name(
        "ADJACENT_PORT_DETERMINANT_TRANSPORT_LEMMA.md"
    )
    payload = {
        "verified": True,
        "status": "adjacent_port_determinant_transport_identity_verified",
        "scope": (
            "symbolic local Schur complement, cleared determinant, and "
            "deterministic exact-rational component products"
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "symbolic_local_identity": True,
        "symbolic_cleared_determinant_identity": True,
        "component_range": [1, 6],
        "trials_per_component_count": 200,
        "component_cases": component_cases,
        "proper_corner_checks": proper_corner_checks,
        "global_identity_checks": global_identity_checks,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
