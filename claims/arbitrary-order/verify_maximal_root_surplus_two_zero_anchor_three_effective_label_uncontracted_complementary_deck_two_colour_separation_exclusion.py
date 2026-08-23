"""Focused exact checks for the GLS52 uncontracted-deck exclusion."""

from itertools import combinations, product

import sympy as sp


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def pure_word(color: int, length: int) -> sp.Matrix:
    result = sp.zeros(3**length, 1)
    index = 0
    for _ in range(length):
        index = 3 * index + color
    result[index, 0] = 1
    return result


def test_complete_raw_label_support() -> None:
    labels = ("q0", "q1", "u", "v", "x", "y")
    effective = {"q0", "u", "v"}
    surviving = {
        pair
        for pair in combinations(labels, 2)
        if pair[0] in effective and pair[1] in effective
    }
    assert surviving == {("q0", "u"), ("q0", "v"), ("u", "v")}
    assert ("q0", "q1") not in surviving


def test_common_star_projection() -> None:
    a_scalar, b_scalar = sp.symbols("a b", nonzero=True)
    a = sp.Matrix([a_scalar, 0, 0])
    b = sp.Matrix([b_scalar, 0, 0])
    for prefix in ("u", "v"):
        x = sp.Matrix(sp.symbols(f"x{prefix}0:3"))
        y = sp.Matrix(sp.symbols(f"y{prefix}0:3"))
        value = outer(a, y) + outer(x, b)
        assert value[1, 1] == 0
        assert value[2, 2] == 0


def test_two_colour_deck_separation() -> None:
    gamma, alpha_i, alpha_j = sp.symbols(
        "gamma alpha_i alpha_j", nonzero=True
    )
    for inactive_count in range(1, 7):
        tau_i = pure_word(1, inactive_count)
        tau_j = pure_word(2, inactive_count)
        assert tau_i.dot(tau_j) == 0
        forced_i = gamma * tau_i
        forced_j = gamma * tau_j
        assert forced_i != forced_j

        # Contracting every inactive port at (1,1,1) sends both pure words
        # to one and therefore hides the contradiction.
        all_ones = sp.ones(3**inactive_count, 1)
        assert (all_ones.T * forced_i)[0] == gamma
        assert (all_ones.T * forced_j)[0] == gamma

        # The full and contracted coefficient equations are compatible
        # separately in either colour, but not with one shared deck.
        a_i = alpha_i / gamma
        a_j = alpha_j / gamma
        assert sp.simplify(gamma * a_i - alpha_i) == 0
        assert sp.simplify(gamma * a_j - alpha_j) == 0
        assert sp.simplify(a_i * forced_i - alpha_i * tau_i) == sp.zeros(
            3**inactive_count, 1
        )
        assert sp.simplify(a_j * forced_j - alpha_j * tau_j) == sp.zeros(
            3**inactive_count, 1
        )


def test_gls51_control_projections() -> None:
    half = sp.Rational(1, 2)
    e = [sp.eye(3).col(index) for index in range(3)]
    xu = [-e[0], sp.zeros(3, 1), e[2]]
    yu = [half * e[0], e[1], sp.zeros(3, 1)]
    xv = [-e[0], e[1], sp.zeros(3, 1)]
    yv = [half * e[0], sp.zeros(3, 1), e[2]]
    muv = [
        [outer(xu[left], yv[right]) + outer(xv[right], yu[left]) for right in range(3)]
        for left in range(3)
    ]
    for color in (1, 2):
        for left, right in product(range(3), repeat=2):
            expected = int(left == right == color)
            assert muv[left][right][color, color] == expected

    tau_1 = pure_word(1, 2)
    tau_2 = pure_word(2, 2)
    assert tau_1 != tau_2


def main() -> None:
    test_complete_raw_label_support()
    test_common_star_projection()
    test_two_colour_deck_separation()
    test_gls51_control_projections()
    print("GLS52 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
