"""Primary exact replay for the two-vertex-cover all-depth fibre."""

from fractions import Fraction
from itertools import combinations
from math import factorial


Polynomial = dict[frozenset[int], Fraction]


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
        if not answer[monomial]:
            del answer[monomial]
    return answer


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for first, a in left.items():
        for second, b in right.items():
            if first & second:
                continue
            monomial = first | second
            answer[monomial] = answer.get(monomial, Fraction(0)) + a * b
    return {monomial: value for monomial, value in answer.items() if value}


def scale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return {monomial: scalar * value for monomial, value in polynomial.items()}


def exponential(polynomial: Polynomial, n: int) -> Polynomial:
    answer: Polynomial = {frozenset(): Fraction(1)}
    power: Polynomial = {frozenset(): Fraction(1)}
    for degree in range(1, n // 2 + 1):
        power = multiply(power, polynomial)
        if not power:
            break
        answer = add(answer, scale(power, Fraction(1, factorial(degree))))
    return answer


def pair_polynomial(a, b) -> Polynomial:
    answer = {}
    for i, j in combinations(range(len(a)), 2):
        value = Fraction(a[i] * b[j] + b[i] * a[j])
        if value:
            answer[frozenset((i, j))] = value
    return answer


def response(channel: Polynomial, direct: Polynomial, n: int) -> Polynomial:
    return multiply(exponential(direct, n), channel)


def check_control(a, b, edge: tuple[int, int]) -> None:
    n = len(a)
    channel = pair_polynomial(a, b)
    edge_monomial = frozenset(edge)
    direction = {edge_monomial: Fraction(1)}
    assert multiply(channel, direction) == {}
    baseline = {frozenset((0, 1)): Fraction(2)} if edge != (0, 1) else {}
    expected = response(channel, baseline, n)
    for scalar in (Fraction(-3), Fraction(0), Fraction(5, 2)):
        changed = add(baseline, scale(direction, scalar))
        assert response(channel, changed, n) == expected
    support = tuple(monomial for monomial in channel)
    assert all(set(edge) & set(other) for other in support)


def check_converse() -> None:
    channel = {
        frozenset((0, 1)): Fraction(2),
        frozenset((2, 3)): Fraction(-5),
    }
    edge = {frozenset((0, 1)): Fraction(1)}
    product_value = multiply(channel, edge)
    assert product_value == {frozenset((0, 1, 2, 3)): Fraction(-5)}
    assert response(channel, edge, 4) != response(channel, {}, 4)


def check_multi_edge_kernel() -> None:
    channel = pair_polynomial((1, 1, 1, 0, 0, 0), (0, 0, 0, 1, 1, 1))
    direction = {
        frozenset((0, 2)): Fraction(1),
        frozenset((0, 1)): Fraction(-1),
    }
    assert multiply(channel, direction) == {}
    assert all(any(not edge & residual for residual in channel) for edge in direction)
    baseline = {frozenset((2, 5)): Fraction(3)}
    assert response(channel, add(baseline, direction), 6) == response(
        channel, baseline, 6
    )


def main() -> None:
    check_control((1, 1, 1, 1, 1, 0, 0), (0, 0, 0, 0, 0, 1, 1), (5, 6))
    check_control((0, 1, 1, 1, 1, 1, 1), (1, 0, 0, 0, 0, 0, 0), (0, 1))
    check_converse()
    check_multi_edge_kernel()
    print("full-tensor h-zero Z fibre primary replay: PASS")


if __name__ == "__main__":
    main()
