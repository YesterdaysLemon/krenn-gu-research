"""Primary exact replay for the common projective joint-response theorem.

The operator-space and determinant arguments in the theorem are load-bearing.
This script checks their bounded arbitrary-h algebraic identity, effective-
scalar split, and sharpness controls with exact SymPy arithmetic.
"""

from fractions import Fraction
from itertools import combinations, product

import sympy as sp

PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def verify_arbitrary_h_identity() -> None:
    delta, eta, h = sp.symbols("delta eta h")
    effective = delta + h * eta
    direct = {edge: sp.symbols(f"B{edge[0]}{edge[1]}") for edge in EDGES}
    channel = {edge: sp.symbols(f"K{edge[0]}{edge[1]}") for edge in EDGES}
    residual_present = {edge: h * direct[edge] + channel[edge] for edge in EDGES}
    selected = {
        edge: delta * direct[edge] + eta * residual_present[edge] for edge in EDGES
    }

    compound_direct = sum(direct[e] * direct[f] for e, f in MATCHINGS)
    compound_channel = sum(channel[e] * channel[f] for e, f in MATCHINGS)
    compound_selected = sum(selected[e] * selected[f] for e, f in MATCHINGS)
    cross = sum(direct[e] * channel[f] + channel[e] * direct[f] for e, f in MATCHINGS)
    residual_present_four = h * compound_direct + cross
    selected_four = delta * compound_direct + eta * residual_present_four
    assert (
        sp.expand(
            effective * selected_four - compound_selected + eta**2 * compound_channel
        )
        == 0
    )

    # No pure axis or effective-scalar divisor requires division.
    pure_m = sp.expand(
        (effective * selected_four - compound_selected).subs({delta: 1, eta: 0})
    )
    pure_z = sp.expand(
        (
            effective * selected_four - compound_selected + eta**2 * compound_channel
        ).subs({delta: 0, eta: 1})
    )
    effective_zero = sp.expand(
        (
            effective * selected_four - compound_selected + eta**2 * compound_channel
        ).subs({delta: -h, eta: 1})
    )
    assert pure_m == 0
    assert pure_z == 0
    assert effective_zero == 0


def verify_effective_scalar_detector_split() -> None:
    effective = sp.symbols("a")
    g = sp.symbols("g0:3", nonzero=True)
    mixed = sp.Matrix(3, 3, lambda row, column: sp.symbols(f"G{row}{column}"))
    detector = sp.diag(*g) - effective * mixed
    assert sp.expand(detector.det().subs(effective, 0)) == sp.prod(g)
    assert sp.expand(detector.det().subs({entry: 0 for entry in mixed})) == sp.prod(g)


def intersection_dimension(spaces: tuple[str, ...]) -> int:
    constraints = {
        "zero": sp.eye(2),
        "line_11": sp.Matrix([[1, -1]]),
        "line_12": sp.Matrix([[2, -1]]),
        "plane": sp.zeros(0, 2),
    }
    rows = [row for name in spaces for row in constraints[name].tolist()]
    return 2 - sp.Matrix(rows).rank() if rows else 2


def predicted_intersection_dimension(spaces: tuple[str, ...]) -> int:
    if "zero" in spaces:
        return 0
    lines = {name for name in spaces if name.startswith("line_")}
    if len(lines) > 1:
        return 0
    if len(lines) == 1:
        return 1
    return 2


def verify_common_subspace_trichotomy() -> None:
    names = ("zero", "line_11", "line_12", "plane")
    checked = 0
    for spaces in product(names, repeat=7):
        observed = intersection_dimension(spaces)
        expected = predicted_intersection_dimension(spaces)
        assert observed == expected
        checked += 1
    assert checked == 4**7
    assert intersection_dimension(("line_11",) * 6 + ("line_12",)) == 0
    assert intersection_dimension(("plane",) * 7) == 2


def zero_matrix() -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix.zeros(3, 3)


def diagonal_matrix(values: tuple[Fraction | int, Fraction | int, Fraction | int]):
    return sp.ImmutableMatrix.diag(*map(sp.Rational, values))


def outer(left: tuple[int, int, int], right: tuple[int, int, int]):
    return sp.ImmutableMatrix(left) * sp.ImmutableMatrix([right])


def corrected_blocks(
    first: tuple[tuple[int, int, int], ...],
    second: tuple[tuple[int, int, int], ...],
) -> dict[tuple[int, int], sp.ImmutableMatrix]:
    return {
        edge: sp.ImmutableMatrix(
            outer(first[edge[0]], second[edge[1]])
            + outer(second[edge[0]], first[edge[1]])
        )
        for edge in EDGES
    }


def add_blocks(
    left: dict[tuple[int, int], sp.ImmutableMatrix],
    right: dict[tuple[int, int], sp.ImmutableMatrix],
    right_scale: Fraction | int = 1,
) -> dict[tuple[int, int], sp.ImmutableMatrix]:
    scalar = sp.Rational(right_scale)
    return {
        edge: sp.ImmutableMatrix(left[edge] + scalar * right[edge]) for edge in EDGES
    }


def compound_word(
    blocks: dict[tuple[int, int], sp.ImmutableMatrix],
    word: tuple[int, int, int, int],
):
    return sp.expand(
        sum(
            blocks[e][word[e[0]], word[e[1]]] * blocks[f][word[f[0]], word[f[1]]]
            for e, f in MATCHINGS
        )
    )


def cross_word(
    left: dict[tuple[int, int], sp.ImmutableMatrix],
    right: dict[tuple[int, int], sp.ImmutableMatrix],
    word: tuple[int, int, int, int],
):
    return sp.expand(
        sum(
            left[e][word[e[0]], word[e[1]]] * right[f][word[f[0]], word[f[1]]]
            + right[e][word[e[0]], word[e[1]]] * left[f][word[f[0]], word[f[1]]]
            for e, f in MATCHINGS
        )
    )


def tensor_from_compound_and_cross(
    direct: dict[tuple[int, int], sp.ImmutableMatrix],
    channel: dict[tuple[int, int], sp.ImmutableMatrix],
) -> dict[tuple[int, int, int, int], sp.Expr]:
    return {
        word: compound_word(direct, word) + cross_word(direct, channel, word)
        for word in product(COLORS, repeat=4)
    }


def active_colors(
    pairs: dict[tuple[int, int], sp.ImmutableMatrix], fixed_port: int
) -> set[int]:
    active: set[int] = set()
    for color in COLORS:
        for partner in PORTS:
            if partner == fixed_port:
                continue
            edge = tuple(sorted((fixed_port, partner)))
            complement = tuple(port for port in PORTS if port not in edge)
            other = tuple(sorted(complement))
            if any(
                pairs[edge][color, color] * pairs[other][delta, delta]
                for delta in COLORS
                if delta != color
            ):
                active.add(color)
    return active


def verify_unequal_slope_control() -> None:
    e00 = diagonal_matrix((1, 0, 0))
    channel = {edge: sp.ImmutableMatrix(2 * e00) for edge in EDGES}
    color_one = {(0, 1), (1, 2), (2, 3)}
    color_two = {(0, 2), (1, 3)}
    selected_pairs = {
        edge: diagonal_matrix((2, int(edge in color_one), int(edge in color_two)))
        for edge in EDGES
    }
    direct = add_blocks(selected_pairs, channel, -2)

    # Pair slope [1:2].
    assert add_blocks(direct, channel, 2) == selected_pairs
    # Four-port slope [1:1].
    response = tensor_from_compound_and_cross(direct, channel)
    assert tuple(response[(color,) * 4] for color in COLORS) == (-12, 1, 1)
    assert all(value == 0 for word, value in response.items() if len(set(word)) > 1)
    assert active_colors(selected_pairs, 0) == {0, 1, 2}
    assert selected_pairs[(0, 3)][0, 0] * selected_pairs[(1, 2)][1, 1] == 2
    assert selected_pairs[(0, 1)][1, 1] * selected_pairs[(2, 3)][0, 0] == 2
    assert selected_pairs[(0, 2)][2, 2] * selected_pairs[(1, 3)][0, 0] == 2
    assert sp.Matrix([[1, 2], [1, 1]]).rank() == 2


def camouflage_pairs() -> dict[tuple[int, int], sp.ImmutableMatrix]:
    values = {
        (0, 1): (0, 0, 1),
        (2, 3): (0, 0, 1),
        (0, 2): (1, 1, 0),
        (1, 3): (2, 2, 0),
        (0, 3): (1, Fraction(2, 3), 0),
        (1, 2): (3, 2, 0),
    }
    return {edge: diagonal_matrix(value) for edge, value in values.items()}


def verify_common_line_camouflage() -> None:
    first = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0))
    second = ((0, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0))
    channel = corrected_blocks(first, second)
    selected_pairs = camouflage_pairs()
    direct = add_blocks(selected_pairs, channel, -1)
    response = tensor_from_compound_and_cross(direct, channel)
    expected_pure = (3, sp.Rational(4, 3), 1)
    assert tuple(response[(color,) * 4] for color in COLORS) == expected_pure
    assert all(value == 0 for word, value in response.items() if len(set(word)) > 1)
    for port in PORTS:
        assert active_colors(selected_pairs, port) == {0, 1}


def main() -> None:
    verify_arbitrary_h_identity()
    verify_effective_scalar_detector_split()
    verify_common_subspace_trichotomy()
    verify_unequal_slope_control()
    verify_common_line_camouflage()
    print("common projective joint-response primary replay: PASS")


if __name__ == "__main__":
    main()
