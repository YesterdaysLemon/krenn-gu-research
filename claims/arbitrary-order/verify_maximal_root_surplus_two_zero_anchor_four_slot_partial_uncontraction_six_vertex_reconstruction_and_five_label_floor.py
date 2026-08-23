"""Focused exact checks for the GLS54 partial-uncontraction floor."""

from itertools import combinations

import sympy as sp


ROOTS = ("a0", "a1")
OPEN = ("t0", "t1", "t2", "t3")
VERTICES = ROOTS + OPEN


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def edge_symbol(left, right):
    pair = {left, right}
    if pair == set(ROOTS):
        return sp.Integer(0)
    if "a0" in pair:
        target = next(vertex for vertex in pair if vertex != "a0")
        return sp.Symbol(f"x{target[1:]}")
    if "a1" in pair:
        target = next(vertex for vertex in pair if vertex != "a1")
        return sp.Symbol(f"y{target[1:]}")
    indices = sorted((int(left[1:]), int(right[1:])))
    return sp.Symbol(f"e{indices[0]}{indices[1]}")


def matching_weight(matching):
    result = sp.Integer(1)
    for left, right in matching:
        result *= edge_symbol(left, right)
    return result


def test_activity_padding_and_complements() -> None:
    for root_order in range(3, 10):
        residual = ("q0", "q1")
        promoted = tuple(f"u{index}" for index in range(2 * root_order - 2))
        bhat = residual + promoted
        for active_residual_count in range(3):
            for active_promoted_count in range(5 - active_residual_count):
                activity_size = active_residual_count + active_promoted_count
                active = set(residual[:active_residual_count]) | set(
                    promoted[:active_promoted_count]
                )
                padding_count = 4 - activity_size
                inactive_promoted = [label for label in promoted if label not in active]
                assert len(inactive_promoted) >= padding_count
                padding = set(inactive_promoted[:padding_count])
                open_set = active | padding
                contracted = set(bhat) - open_set
                assert len(open_set) == 4
                assert padding <= set(promoted)
                assert not (padding & set(residual))

                for pair in combinations(bhat, 2):
                    pair_set = set(pair)
                    if not pair_set <= open_set:
                        inactive_endpoint = pair_set & contracted
                        assert inactive_endpoint
                        assert inactive_endpoint <= set(bhat) - active
                    else:
                        complement = set(bhat) - pair_set
                        assert complement == contracted | (open_set - pair_set)
                        assert len(open_set - pair_set) == 2


def test_inactive_residual_must_stay_contracted() -> None:
    z = sp.Matrix([1, 1, 1])
    transverse = sp.Matrix([1, 0, 0])
    root_zero = sp.Matrix(
        [
            [1, -1, 0],
            [0, 1, -1],
            [1, 0, -1],
        ]
    )
    root_one = sp.Matrix(
        [
            [2, -2, 0],
            [0, 3, -3],
            [5, 0, -5],
        ]
    )
    shore_zero = root_zero * z
    shore_one = root_one * z
    assert shore_zero == sp.zeros(3, 1)
    assert shore_one == sp.zeros(3, 1)
    assert root_zero * transverse != sp.zeros(3, 1)
    assert root_one * transverse != sp.zeros(3, 1)

    active_x = sp.Matrix(sp.symbols("x0:3"))
    active_y = sp.Matrix(sp.symbols("y0:3"))
    companion = shore_zero * active_y.T + active_x * shore_one.T
    assert companion == sp.zeros(3, 3)


def test_six_vertex_matching_identity() -> None:
    matchings = perfect_matchings(VERTICES)
    assert len(matchings) == 15
    weights = tuple(matching_weight(matching) for matching in matchings)
    assert sum(weight == 0 for weight in weights) == 3
    actual = sp.expand(sum(weights))

    expected = sp.Integer(0)
    for left, right in combinations(range(4), 2):
        complement = sorted(set(range(4)) - {left, right})
        mu = sp.Symbol(f"x{left}") * sp.Symbol(f"y{right}")
        mu += sp.Symbol(f"x{right}") * sp.Symbol(f"y{left}")
        expected += mu * sp.Symbol(f"e{complement[0]}{complement[1]}")
    assert sp.expand(actual - expected) == 0
    assert len(sp.Poly(actual).terms()) == 12


def test_target_weights_and_normalization() -> None:
    residual_vectors = {
        "q0": (sp.Rational(2), sp.Rational(3), sp.Rational(5)),
        "q1": (sp.Rational(7), sp.Rational(11), sp.Rational(13)),
    }
    residual = ("q0", "q1")
    for active_residual_count in range(3):
        active_residual = set(residual[:active_residual_count])
        contracted_residual = set(residual) - active_residual
        for color in range(3):
            beta = sp.Integer(1)
            for label in contracted_residual:
                beta *= residual_vectors[label][color]
            assert beta != 0
            assert sp.simplify(beta * (sp.Integer(1) / beta)) == 1


def main() -> None:
    test_activity_padding_and_complements()
    test_inactive_residual_must_stay_contracted()
    test_six_vertex_matching_identity()
    test_target_weights_and_normalization()
    print("GLS54 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
