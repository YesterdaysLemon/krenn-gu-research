"""Exact certificates for support-minimal toric degenerations.

Let ``S`` be the nonzero entry support of a putative three-colour GHZ
witness.  Give every local vertex-colour coordinate ``(v,c)`` an integer
potential ``h[v,c]``.  Scaling

    W_uv[a,b] -> t**(h[u,a] + h[v,b]) W_uv[a,b]

multiplies every matching monomial in a fixed vertex colouring by the same
power of ``t``.  Consequently all forbidden zero amplitudes remain zero.
The three required monochromatic amplitudes remain unchanged when

    sum_v h[v,c] = 0                         for every colour c.

If every supported entry has nonnegative exponent and at least one has
positive exponent, the limit ``t -> 0`` is a new exact witness with
strictly smaller support.

The Gordan--Stiemke alternative gives the exact dual normal form.  If no
such degeneration exists, there are strictly positive weights ``y_e`` on
all supported lifted edges such that the weighted degree of every lifted
vertex ``(v,c)`` is a number ``mu[c]`` independent of ``v``.  We call this
a balanced support.

This module contains only exact integer replay.  Numerical LP discovery is
kept in ``analyze_support_toric_census.py``.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence

from search_witness import EquationSystem


def entry_endpoints(
    system: EquationSystem,
    flat_index: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    edge_index, position = divmod(int(flat_index), system.d**2)
    row, column = divmod(position, system.d)
    first, second = system.edges[edge_index]
    return (first, row), (second, column)


def supported_exponents(
    system: EquationSystem,
    selected: Iterable[int],
    potentials: Sequence[Sequence[int]],
) -> dict[int, int]:
    if len(potentials) != system.n or any(
        len(row) != system.d for row in potentials
    ):
        raise ValueError("potential array has the wrong dimensions")
    result: dict[int, int] = {}
    for flat_index in sorted(map(int, selected)):
        first, second = entry_endpoints(system, flat_index)
        result[flat_index] = (
            int(potentials[first[0]][first[1]])
            + int(potentials[second[0]][second[1]])
        )
    return result


def verify_degeneration_certificate(
    system: EquationSystem,
    selected: Iterable[int],
    certificate: dict[str, object],
) -> dict[str, object]:
    if certificate.get("mode") != "support_degeneration":
        raise AssertionError("wrong degeneration-certificate mode")
    potentials = [
        list(map(int, row))
        for row in certificate["potentials"]  # type: ignore[index]
    ]
    colour_sums = [
        sum(potentials[vertex][colour] for vertex in range(system.n))
        for colour in range(system.d)
    ]
    if any(colour_sums):
        raise AssertionError(
            f"monochromatic exponents are not zero: {colour_sums}"
        )
    exponents = supported_exponents(system, selected, potentials)
    if not exponents or min(exponents.values()) < 0:
        raise AssertionError("a supported entry has negative exponent")
    deleted = sorted(
        flat_index
        for flat_index, exponent in exponents.items()
        if exponent > 0
    )
    if not deleted:
        raise AssertionError("degeneration does not shrink the support")
    if sorted(map(int, certificate["deleted_entries"])) != deleted:
        raise AssertionError("recorded deleted-entry set is incorrect")
    return {
        "verified": True,
        "mode": "support_degeneration",
        "colour_sums": colour_sums,
        "deleted_entries": len(deleted),
        "surviving_entries": len(exponents) - len(deleted),
        "maximum_exponent": max(exponents.values()),
    }


def verify_balanced_certificate(
    system: EquationSystem,
    selected: Iterable[int],
    certificate: dict[str, object],
) -> dict[str, object]:
    if certificate.get("mode") != "balanced_support":
        raise AssertionError("wrong balanced-certificate mode")
    ordered = sorted(map(int, selected))
    weights = list(map(int, certificate["entry_weights"]))  # type: ignore[index]
    colour_degrees = list(
        map(int, certificate["colour_degrees"])  # type: ignore[index]
    )
    if len(weights) != len(ordered):
        raise AssertionError("balanced weight count is incorrect")
    if len(colour_degrees) != system.d:
        raise AssertionError("balanced colour-degree count is incorrect")
    if not weights or min(weights) <= 0:
        raise AssertionError("balanced weights are not strictly positive")
    if min(colour_degrees) <= 0:
        raise AssertionError("balanced colour degrees are not positive")

    degrees = [
        [0 for _ in range(system.d)]
        for _ in range(system.n)
    ]
    for flat_index, weight in zip(ordered, weights, strict=True):
        first, second = entry_endpoints(system, flat_index)
        degrees[first[0]][first[1]] += weight
        degrees[second[0]][second[1]] += weight
    expected = [
        colour_degrees[colour]
        for _vertex in range(system.n)
        for colour in range(system.d)
    ]
    observed = [
        degrees[vertex][colour]
        for vertex in range(system.n)
        for colour in range(system.d)
    ]
    if observed != expected:
        raise AssertionError("lifted weighted degrees do not balance")
    if "uniform_lifted_degree" in certificate:
        uniform = int(certificate["uniform_lifted_degree"])
        if colour_degrees != [uniform] * system.d:
            raise AssertionError("recorded lifted degree is not uniform")
    return {
        "verified": True,
        "mode": "balanced_support",
        "entries": len(ordered),
        "minimum_weight": min(weights),
        "maximum_weight": max(weights),
        "colour_degrees": colour_degrees,
    }


def primitive_integer_vector(values: Sequence[object]) -> list[int]:
    """Rationalize numerical LP output and return a primitive integer vector."""

    from fractions import Fraction

    fractions = [
        value
        if isinstance(value, Fraction)
        else Fraction(float(value)).limit_denominator(1_000_000)
        for value in values
    ]
    denominator = 1
    for value in fractions:
        denominator = math.lcm(denominator, value.denominator)
    integers = [
        int(value.numerator * (denominator // value.denominator))
        for value in fractions
    ]
    divisor = 0
    for value in integers:
        divisor = math.gcd(divisor, abs(value))
    if divisor:
        integers = [value // divisor for value in integers]
    return integers
