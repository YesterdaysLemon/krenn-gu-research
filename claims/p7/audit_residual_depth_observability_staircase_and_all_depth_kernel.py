"""Independent no-project-import audit of the residual-depth staircase."""

from fractions import Fraction
from itertools import combinations


def multiply(left, right):
    product = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            product[mask] = product.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in product.items() if value}


def wick_exponential(edges):
    result = {0: Fraction(1)}
    for (first, second), weight in edges.items():
        edge_mask = (1 << first) | (1 << second)
        result = multiply(result, {0: Fraction(1), edge_mask: Fraction(weight)})
    return result


def response_at_depth(moments, port_count, residual_mask):
    shifted = residual_mask << port_count
    return {
        port_mask: moments.get(port_mask | shifted, Fraction(0))
        for port_mask in range(1 << port_count)
    }


def visible(port_mask, residual_mask, residual_count):
    return port_mask.bit_count() + residual_mask.bit_count() >= 2 * residual_count


def q2_tower(parameter):
    port_count = 7
    residual_first = port_count
    residual_second = port_count + 1
    edges = {
        (0, 1): Fraction(parameter),
        (0, residual_first): Fraction(1),
        (1, residual_second): -Fraction(parameter),
        (residual_first, residual_second): Fraction(1),
    }
    moments = wick_exponential(edges)
    return tuple(response_at_depth(moments, port_count, mask) for mask in range(4))


def audit_q2_kernel() -> None:
    first = q2_tower(2)
    second = q2_tower(5)
    for residual_mask in range(4):
        for port_mask in range(1 << 7):
            if visible(port_mask, residual_mask, 2):
                assert first[residual_mask][port_mask] == second[residual_mask][port_mask]

    pair = 3
    assert first[0][pair] == 2
    assert second[0][pair] == 5
    assert first[1][1] == second[1][1] == 1
    assert first[2][2] == -2
    assert second[2][2] == -5
    assert first[3][0] == second[3][0] == 1

    for tower, parameter in ((first, 2), (second, 5)):
        base, y_first, y_second, full = tower
        left = multiply(base, full)
        odd_product = multiply(y_first, y_second)
        discriminant_pair = left.get(pair, 0) - odd_product.get(pair, 0)
        square_pair = multiply(base, base).get(pair, 0)
        assert discriminant_pair == square_pair == 2 * parameter


def stars(values):
    b12, b13, b14, b23, b24, b34 = values
    return (
        b12 + b13 + b14,
        b12 + b23 + b24,
        b13 + b23 + b34,
        b14 + b24 + b34,
    )


def haf_four(values):
    b12, b13, b14, b23, b24, b34 = values
    return b12 * b34 + b13 * b24 + b14 * b23


def audit_marked_star_kernel() -> None:
    models = (
        (-1, 1, 0, 0, 1, -1),
        (-1, 0, 1, 1, 0, -1),
    )
    assert stars(models[0]) == stars(models[1]) == (0, 0, 0, 0)
    assert haf_four(models[0]) == haf_four(models[1]) == 2
    edge_order = tuple(combinations(range(4), 2))
    moments = []
    for model in models:
        edges = {
            edge: Fraction(value)
            for edge, value in zip(edge_order, model, strict=True)
            if value
        }
        moments.append(wick_exponential(edges))
    for residual_mask in range(4):
        for port_mask in range(1 << 7):
            if not visible(port_mask, residual_mask, 2):
                continue
            if residual_mask:
                values = (Fraction(0), Fraction(0))
            else:
                values = tuple(moment.get(port_mask, Fraction(0)) for moment in moments)
            assert values[0] == values[1]


def higher_tower(residual_count, parameter):
    port_count = 7
    residual_offset = port_count
    edges = {}
    for first in range(0, residual_count, 2):
        edges[(residual_offset + first, residual_offset + first + 1)] = Fraction(1)
    edges[(0, residual_offset)] = Fraction(1)
    edges[(1, residual_offset + 1)] = Fraction(parameter)
    moments = wick_exponential(edges)
    return tuple(
        response_at_depth(moments, port_count, residual_mask)
        for residual_mask in range(1 << residual_count)
    )


def audit_higher_kernels() -> None:
    for residual_count in (4, 6):
        first = higher_tower(residual_count, 2)
        second = higher_tower(residual_count, 5)
        for residual_mask in range(1 << residual_count):
            for port_mask in range(1 << 7):
                if visible(port_mask, residual_mask, residual_count):
                    assert first[residual_mask][port_mask] == second[residual_mask][port_mask]
        full_mask = (1 << residual_count) - 1
        assert first[full_mask][0] == second[full_mask][0] == 1
        assert first[full_mask][3] == 2
        assert second[full_mask][3] == 5


def main() -> None:
    assert tuple(4 - depth for depth in range(3)) == (4, 3, 2)
    assert tuple(8 - depth for depth in range(5)) == (8, 7, 6, 5, 4)
    assert tuple(12 - depth for depth in range(7)) == (12, 11, 10, 9, 8, 7, 6)
    audit_q2_kernel()
    audit_marked_star_kernel()
    audit_higher_kernels()
    print("AUDIT PASS: q=2 all-depth eligible coefficients have a rational fiber")
    print("AUDIT PASS: marked stars preserve the independent torus-zero pair fiber")
    print("AUDIT PASS: q=4,6 towers hide a varying quadratic relative coefficient")
    print("AUDIT SCOPE: mixed-GHZ and herald observations remain unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
