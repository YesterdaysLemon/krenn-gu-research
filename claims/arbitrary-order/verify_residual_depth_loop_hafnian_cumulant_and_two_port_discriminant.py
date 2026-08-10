"""Verify the residual-depth loop-hafnian and discriminant theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

PORT_COUNT = 4
RESIDUAL_COUNT = 4


class SquareZeroPoly:
    """Sparse polynomial in separate square-zero port and residual variables."""

    def __init__(self, terms=None):
        self.terms = {}
        for key, value in (terms or {}).items():
            coefficient = sp.expand(value)
            if coefficient != 0:
                self.terms[key] = coefficient

    @classmethod
    def scalar(cls, value):
        return cls({(0, 0): sp.sympify(value)})

    def __add__(self, other):
        other = coerce(other)
        result = dict(self.terms)
        for key, value in other.terms.items():
            result[key] = sp.expand(result.get(key, 0) + value)
            if result[key] == 0:
                del result[key]
        return SquareZeroPoly(result)

    __radd__ = __add__

    def __neg__(self):
        return SquareZeroPoly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-coerce(other))

    def __rsub__(self, other):
        return coerce(other) - self

    def __mul__(self, other):
        other = coerce(other)
        result = {}
        for (x_left, y_left), left_value in self.terms.items():
            for (x_right, y_right), right_value in other.terms.items():
                if x_left & x_right or y_left & y_right:
                    continue
                key = (x_left | x_right, y_left | y_right)
                result[key] = sp.expand(
                    result.get(key, 0) + left_value * right_value
                )
        return SquareZeroPoly(result)

    __rmul__ = __mul__

    def scale(self, value):
        return SquareZeroPoly(
            {key: sp.sympify(value) * coefficient for key, coefficient in self.terms.items()}
        )

    def coefficient(self, x_mask: int, y_mask: int = 0):
        return self.terms.get((x_mask, y_mask), sp.Integer(0))

    def residual_coefficient(self, y_mask: int):
        return SquareZeroPoly(
            {
                (x_mask, 0): coefficient
                for (x_mask, present_y), coefficient in self.terms.items()
                if present_y == y_mask
            }
        )

    def with_residual_mask(self, y_mask: int):
        return SquareZeroPoly(
            {
                (x_mask, y_mask): coefficient
                for (x_mask, present_y), coefficient in self.terms.items()
                if present_y == 0
            }
        )

    def is_zero(self):
        return not self.terms


def coerce(value):
    if isinstance(value, SquareZeroPoly):
        return value
    return SquareZeroPoly.scalar(value)


def sq_exp(value: SquareZeroPoly, maximum_degree: int):
    result = SquareZeroPoly.scalar(1)
    term = SquareZeroPoly.scalar(1)
    for degree in range(1, maximum_degree + 1):
        term = (term * value).scale(sp.Rational(1, degree))
        result += term
    return result


def sq_log(value: SquareZeroPoly, maximum_degree: int):
    nilpotent = value - 1
    result = SquareZeroPoly.scalar(0)
    power = SquareZeroPoly.scalar(1)
    for degree in range(1, maximum_degree + 1):
        power = power * nilpotent
        result += power.scale(sp.Rational((-1) ** (degree - 1), degree))
    return result


def port_variable(port: int):
    return SquareZeroPoly({(1 << port, 0): sp.Integer(1)})


def residual_variable(residual: int):
    return SquareZeroPoly({(0, 1 << residual): sp.Integer(1)})


def main() -> None:
    x = tuple(port_variable(port) for port in range(PORT_COUNT))
    y = tuple(residual_variable(vertex) for vertex in range(RESIDUAL_COUNT))

    port_weights = {
        pair: sp.Symbol(f"b{pair[0]}{pair[1]}")
        for pair in combinations(range(PORT_COUNT), 2)
    }
    residual_weights = {
        pair: sp.Symbol(f"a{pair[0]}{pair[1]}")
        for pair in combinations(range(RESIDUAL_COUNT), 2)
    }
    incidence = {
        (vertex, port): sp.Symbol(f"r{vertex}{port}")
        for vertex in range(RESIDUAL_COUNT)
        for port in range(PORT_COUNT)
    }

    q_port = sum(
        port_weights[left, right] * x[left] * x[right]
        for left, right in combinations(range(PORT_COUNT), 2)
    )
    q_residual = sum(
        residual_weights[left, right] * y[left] * y[right]
        for left, right in combinations(range(RESIDUAL_COUNT), 2)
    )
    q_incidence = sum(
        incidence[vertex, port] * y[vertex] * x[port]
        for vertex in range(RESIDUAL_COUNT)
        for port in range(PORT_COUNT)
    )

    total = sq_exp(q_port + q_residual + q_incidence, 4)
    moment = sq_exp(q_port, 2)
    inverse_moment = sq_exp(-q_port, 2)
    assert (moment * inverse_moment - 1).is_zero()

    normalized = SquareZeroPoly.scalar(0)
    normalized_depths = {}
    for residual_mask in range(1 << RESIDUAL_COUNT):
        response = total.residual_coefficient(residual_mask)
        normalized_depths[residual_mask] = inverse_moment * response
        normalized += normalized_depths[residual_mask].with_residual_mask(
            residual_mask
        )

    expected_normalized = sq_exp(q_residual + q_incidence, 4)
    assert (normalized - expected_normalized).is_zero()
    assert (sq_log(normalized, 8) - q_residual - q_incidence).is_zero()

    singleton = {
        vertex: normalized_depths[1 << vertex]
        for vertex in range(RESIDUAL_COUNT)
    }
    recovered_edges = {}
    for left, right in combinations(range(RESIDUAL_COUNT), 2):
        pair_mask = (1 << left) | (1 << right)
        recovered = (
            normalized_depths[pair_mask] - singleton[left] * singleton[right]
        )
        assert recovered.terms == {
            (0, 0): residual_weights[left, right]
        }
        recovered_edges[left, right] = residual_weights[left, right]

    @cache
    def loop_hafnian(mask: int):
        if mask == 0:
            return SquareZeroPoly.scalar(1)
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        result = singleton[first] * loop_hafnian(remainder)
        cursor = remainder
        while cursor:
            second_bit = cursor & -cursor
            second = second_bit.bit_length() - 1
            pair = tuple(sorted((first, second)))
            result += recovered_edges[pair] * loop_hafnian(remainder ^ second_bit)
            cursor ^= second_bit
        return result

    for residual_mask in range(1 << RESIDUAL_COUNT):
        assert (
            normalized_depths[residual_mask] - loop_hafnian(residual_mask)
        ).is_zero()

    response_empty = total.residual_coefficient(0)
    response_left = total.residual_coefficient(1)
    response_right = total.residual_coefficient(2)
    response_pair = total.residual_coefficient(3)
    h = residual_weights[0, 1]
    discriminant = (
        response_empty * response_pair
        - response_left * response_right
        - h * response_empty * response_empty
    )
    assert discriminant.is_zero()

    moment_squared = response_empty * response_empty
    for port_mask in range(1 << PORT_COUNT):
        size = port_mask.bit_count()
        if size % 2:
            assert moment_squared.coefficient(port_mask) == 0
            continue
        expected = 2 ** (size // 2) * response_empty.coefficient(port_mask)
        assert sp.expand(moment_squared.coefficient(port_mask) - expected) == 0

    print("PASS: normalized residual-depth exponential and logarithm")
    print("PASS: all sixteen residual subsets reconstruct as loop hafnians")
    print("PASS: two-residual response discriminant")
    print("PASS: coefficient law [x_S]M^2=2^(|S|/2)m_S")
    print("SCOPE: legal P5/P6/P7 exposure of the required depths remains UNKNOWN")
    print("searches=0")


if __name__ == "__main__":
    main()
