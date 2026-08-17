"""Independent no-import audit of the two-vertex-cover all-depth fibre."""

from fractions import Fraction
from itertools import combinations


def product(left: dict[int, Fraction], right: dict[int, Fraction]):
    answer = {}
    for first, a in left.items():
        for second, b in right.items():
            if first & second:
                continue
            mask = first | second
            answer[mask] = answer.get(mask, Fraction(0)) + a * b
    return {mask: value for mask, value in answer.items() if value}


def sum_poly(left, right):
    answer = dict(left)
    for mask, value in right.items():
        answer[mask] = answer.get(mask, Fraction(0)) + value
        if not answer[mask]:
            del answer[mask]
    return answer


def channel(a, b):
    return {
        (1 << i) | (1 << j): Fraction(a[i] * b[j] + b[i] * a[j])
        for i, j in combinations(range(len(a)), 2)
        if a[i] * b[j] + b[i] * a[j]
    }


def exp_times_channel(direct, residual, n):
    answer = dict(residual)
    power = {0: Fraction(1)}
    factorial = 1
    for degree in range(1, n // 2 + 1):
        power = product(power, direct)
        if not power:
            break
        factorial *= degree
        answer = sum_poly(
            answer,
            {
                mask: value / factorial
                for mask, value in product(power, residual).items()
            },
        )
    return answer


def audit_case(a, b, endpoints):
    residual = channel(a, b)
    edge_mask = (1 << endpoints[0]) | (1 << endpoints[1])
    direction = {edge_mask: Fraction(1)}
    assert product(residual, direction) == {}
    zero = exp_times_channel({}, residual, len(a))
    for scalar in (Fraction(1), Fraction(-7, 3)):
        changed = {edge_mask: scalar}
        assert exp_times_channel(changed, residual, len(a)) == zero
    assert all(mask & edge_mask for mask in residual)


def audit_failure() -> None:
    residual = {0b0011: Fraction(1), 0b1100: Fraction(4)}
    direction = {0b0011: Fraction(1)}
    assert product(residual, direction) == {0b1111: Fraction(4)}
    assert exp_times_channel(direction, residual, 4) != residual


def audit_multi_edge_kernel() -> None:
    residual = channel((1, 1, 1, 0, 0, 0), (0, 0, 0, 1, 1, 1))
    direction = {
        0b000101: Fraction(1),
        0b000011: Fraction(-1),
    }
    assert product(residual, direction) == {}
    assert all(any(not edge & support for support in residual) for edge in direction)
    baseline = {0b100100: Fraction(3)}
    changed = sum_poly(baseline, direction)
    assert exp_times_channel(changed, residual, 6) == exp_times_channel(
        baseline, residual, 6
    )


def main() -> None:
    audit_case((1, 1, 1, 1, 1, 0, 0), (0, 0, 0, 0, 0, 1, 1), (5, 6))
    audit_case((0, 1, 1, 1, 1, 1, 1), (1, 0, 0, 0, 0, 0, 0), (0, 1))
    audit_failure()
    audit_multi_edge_kernel()
    print("full-tensor h-zero Z fibre independent audit: PASS")


if __name__ == "__main__":
    main()
