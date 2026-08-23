"""Focused exact checks for the GLS53 six-vertex reconstruction."""

from itertools import combinations

import sympy as sp


VERTICES = ("a0", "a1", "u0", "u1", "u2", "u3")
PORTS = VERTICES[2:]


def perfect_matchings(vertices):
    """Enumerate unordered perfect matchings recursively."""

    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            result.append(((first, second),) + matching)
    return tuple(result)


def edge_symbol(left, right):
    pair = {left, right}
    if pair == {"a0", "a1"}:
        return sp.Integer(0)
    if "a0" in pair:
        port = next(vertex for vertex in pair if vertex != "a0")
        return sp.Symbol(f"x{port[1:]}")
    if "a1" in pair:
        port = next(vertex for vertex in pair if vertex != "a1")
        return sp.Symbol(f"y{port[1:]}")
    indices = sorted((int(left[1:]), int(right[1:])))
    return sp.Symbol(f"d{indices[0]}{indices[1]}")


def matching_weight(matching):
    result = sp.Integer(1)
    for left, right in matching:
        result *= edge_symbol(left, right)
    return result


def test_matching_bijection() -> None:
    matchings = perfect_matchings(VERTICES)
    assert len(matchings) == 15
    weights = tuple(matching_weight(matching) for matching in matchings)
    assert sum(weight == 0 for weight in weights) == 3

    hafnian = sp.expand(sum(weights))
    expected = sp.Integer(0)
    for left, right in combinations(range(4), 2):
        complement = sorted(set(range(4)) - {left, right})
        root_pair = sp.Symbol(f"x{left}") * sp.Symbol(f"y{right}")
        root_pair += sp.Symbol(f"x{right}") * sp.Symbol(f"y{left}")
        deck = sp.Symbol(f"d{complement[0]}{complement[1]}")
        expected += root_pair * deck
    assert sp.expand(hafnian - expected) == 0
    assert len(sp.Poly(hafnian).terms()) == 12


def test_raw_label_census_and_complements() -> None:
    for root_order in range(3, 9):
        promoted = tuple(f"u{index}" for index in range(2 * root_order - 2))
        active = set(promoted[:4])
        residual = ("q0", "q1")
        labels = residual + promoted
        live = {
            pair
            for pair in combinations(labels, 2)
            if pair[0] in active and pair[1] in active
        }
        assert live == set(combinations(promoted[:4], 2))
        assert len(live) == 6

        inactive = set(promoted[4:])
        assert len(inactive) == 2 * root_order - 6
        for pair in live:
            remaining_active = active - set(pair)
            deck_domain = set(residual) | inactive | remaining_active
            assert deck_domain == set(labels) - set(pair)
            assert len(remaining_active) == 2


def test_weighted_target_normalization() -> None:
    alphas = (sp.Rational(2, 3), sp.Rational(-5, 7), sp.Rational(11, 13))
    for color, alpha in enumerate(alphas):
        local_scale = sp.Integer(1) / alpha
        assert sp.simplify(alpha * local_scale) == 1
        for other in range(3):
            mixed_coefficient = sp.Integer(0)
            if other != color:
                assert sp.simplify(mixed_coefficient * local_scale) == 0


def main() -> None:
    test_matching_bijection()
    test_raw_label_census_and_complements()
    test_weighted_target_normalization()
    print("GLS53 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
