"""Independent matching audit of the residual-depth cumulant theorem.

This file deliberately imports neither SymPy nor the primary verifier.  It
starts from direct hafnian recursion on induced vertex sets, performs the
square-zero normalization arithmetically, and then reconstructs the response
tower with a separately written loop-hafnian recursion.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

PORT_COUNT = 5
RESIDUAL_COUNT = 4
PORT_MASK = (1 << PORT_COUNT) - 1

Poly = dict[int, int]


def add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for mask, value in right.items():
        result[mask] = result.get(mask, 0) + value
        if result[mask] == 0:
            del result[mask]
    return result


def scale(poly: Poly, scalar: int) -> Poly:
    return {mask: scalar * value for mask, value in poly.items() if scalar * value}


def multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, 0) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def inverse_unit(poly: Poly) -> Poly:
    assert poly.get(0) == 1
    nilpotent = add(poly, {0: -1})
    result: Poly = {0: 1}
    power: Poly = {0: 1}
    for degree in range(1, PORT_COUNT + 1):
        power = multiply(power, nilpotent)
        result = add(result, scale(power, (-1) ** degree))
    assert multiply(poly, result) == {0: 1}
    return result


def port_edge(left: int, right: int) -> int:
    return 2 + left + 3 * right


def residual_edge(left: int, right: int) -> int:
    return 7 + 2 * left + 5 * right


def incidence(residual: int, port: int) -> int:
    return 3 + 4 * residual + 2 * port + residual * port


def edge_weight(left: int, right: int) -> int:
    if left > right:
        left, right = right, left
    if right < PORT_COUNT:
        return port_edge(left, right)
    if left >= PORT_COUNT:
        return residual_edge(left - PORT_COUNT, right - PORT_COUNT)
    return incidence(right - PORT_COUNT, left)


@cache
def hafnian(vertex_mask: int) -> int:
    if vertex_mask == 0:
        return 1
    if vertex_mask.bit_count() % 2:
        return 0
    first_bit = vertex_mask & -vertex_mask
    first = first_bit.bit_length() - 1
    remainder = vertex_mask ^ first_bit
    total = 0
    cursor = remainder
    while cursor:
        second_bit = cursor & -cursor
        second = second_bit.bit_length() - 1
        total += edge_weight(first, second) * hafnian(remainder ^ second_bit)
        cursor ^= second_bit
    return total


def response(residual_mask: int) -> Poly:
    lifted_residual_mask = residual_mask << PORT_COUNT
    result: Poly = {}
    for port_mask in range(PORT_MASK + 1):
        value = hafnian(lifted_residual_mask | port_mask)
        if value:
            result[port_mask] = value
    return result


def main() -> None:
    responses = {
        residual_mask: response(residual_mask)
        for residual_mask in range(1 << RESIDUAL_COUNT)
    }
    moment = responses[0]
    inverse_moment = inverse_unit(moment)
    normalized = {
        mask: multiply(inverse_moment, value)
        for mask, value in responses.items()
    }

    singletons = {vertex: normalized[1 << vertex] for vertex in range(RESIDUAL_COUNT)}
    for vertex, singleton in singletons.items():
        expected = {
            1 << port: incidence(vertex, port)
            for port in range(PORT_COUNT)
        }
        assert singleton == expected

    recovered_edges: dict[tuple[int, int], int] = {}
    for left, right in combinations(range(RESIDUAL_COUNT), 2):
        pair_mask = (1 << left) | (1 << right)
        correction = add(
            normalized[pair_mask],
            scale(multiply(singletons[left], singletons[right]), -1),
        )
        expected = residual_edge(left, right)
        assert correction == {0: expected}
        recovered_edges[left, right] = expected

    @cache
    def loop_hafnian(residual_mask: int) -> Poly:
        if residual_mask == 0:
            return {0: 1}
        first_bit = residual_mask & -residual_mask
        first = first_bit.bit_length() - 1
        remainder = residual_mask ^ first_bit
        total = multiply(singletons[first], loop_hafnian(remainder))
        cursor = remainder
        while cursor:
            second_bit = cursor & -cursor
            second = second_bit.bit_length() - 1
            pair = (min(first, second), max(first, second))
            total = add(
                total,
                scale(
                    loop_hafnian(remainder ^ second_bit),
                    recovered_edges[pair],
                ),
            )
            cursor ^= second_bit
        return total

    for residual_mask, value in normalized.items():
        assert value == loop_hafnian(residual_mask)

    for left, middle, right in combinations(range(RESIDUAL_COUNT), 3):
        triple_mask = (1 << left) | (1 << middle) | (1 << right)
        cumulant = normalized[triple_mask]
        cumulant = add(
            cumulant,
            scale(multiply(normalized[(1 << left) | (1 << middle)], singletons[right]), -1),
        )
        cumulant = add(
            cumulant,
            scale(multiply(normalized[(1 << left) | (1 << right)], singletons[middle]), -1),
        )
        cumulant = add(
            cumulant,
            scale(multiply(normalized[(1 << middle) | (1 << right)], singletons[left]), -1),
        )
        cubic = multiply(multiply(singletons[left], singletons[middle]), singletons[right])
        cumulant = add(cumulant, scale(cubic, 2))
        assert cumulant == {}

    h = residual_edge(0, 1)
    discriminant = add(
        multiply(moment, responses[3]),
        scale(multiply(responses[1], responses[2]), -1),
    )
    assert discriminant == scale(multiply(moment, moment), h)

    moment_squared = multiply(moment, moment)
    for port_mask in range(PORT_MASK + 1):
        size = port_mask.bit_count()
        if size % 2:
            assert moment_squared.get(port_mask, 0) == 0
        else:
            expected = (2 ** (size // 2)) * moment.get(port_mask, 0)
            assert moment_squared.get(port_mask, 0) == expected

    print("PASS: direct matching tower normalizes to four loop-hafnian depths")
    print("PASS: independently recovered singleton incidences and residual edges")
    print("PASS: every third residual cumulant vanishes")
    print("PASS: division-free two-residual discriminant and coefficient law")
    print("SCOPE: fixed integer audit only; arbitrary order is established in the note")
    print("searches=0")


if __name__ == "__main__":
    main()
