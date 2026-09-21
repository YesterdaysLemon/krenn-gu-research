"""Independent exact checks for the bounded continuation review.

This standard-library script reconstructs the two n=8 Laurent controls from
their durable fixture.  It does not import the exploratory projected-source
script or either committed scientific checker.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/eight_vertex_scaffold_subsystem_controls.json"

PROTECTED_MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
INTERNAL_COLOR = {
    tuple(sorted(edge)): color
    for color, matching in enumerate(PROTECTED_MATCHINGS)
    for edge in matching
}
PROBES = ((1, -1, 0), (1, 0, -1))

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, int]
Matching = tuple[tuple[int, int], ...]


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[Matching] = []
    for position, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            answer.append(((first, second), *tail))
    return tuple(answer)


MATCHINGS = perfect_matchings(tuple(range(8)))


def add_term(polynomial: Polynomial, exponent: Exponent, coefficient: int) -> None:
    if not coefficient:
        return
    polynomial[exponent] = polynomial.get(exponent, 0) + coefficient
    if polynomial[exponent] == 0:
        del polynomial[exponent]


def support_map(fixture: dict, family: dict) -> dict[tuple[int, int], tuple[tuple[int, int], ...]]:
    return {
        tuple(pair): tuple(tuple(position) for position in positions)
        for pair, positions in zip(
            fixture["parameter_order"], family["supports"], strict=True
        )
    }


def matching_term(
    word: tuple[int, ...],
    matching: Matching,
    supports: dict[tuple[int, int], tuple[tuple[int, int], ...]],
    parameter_order: tuple[tuple[int, int], ...],
) -> tuple[int, Exponent] | None:
    coefficient = 1
    exponent = [0] * len(parameter_order)
    for first, second in matching:
        same_component = (first < 4) == (second < 4)
        if same_component:
            offset = 0 if first < 4 else 4
            local_edge = tuple(sorted((first - offset, second - offset)))
            color = INTERNAL_COLOR[local_edge]
            if word[first] != color or word[second] != color:
                return None
            continue

        left, right = (first, second) if first < 4 else (second, first)
        colors = (word[left], word[right])
        if colors[0] == colors[1] or colors not in supports:
            return None
        position = (left, right - 4)
        choices = supports[colors]
        if position not in choices:
            return None
        choice = choices.index(position)
        parameter = parameter_order.index(colors)
        exponent[parameter] += 1 if choice == 0 else -1
        if choice == 1:
            coefficient *= -1
    return coefficient, tuple(exponent)


def amplitude(
    word: tuple[int, ...],
    supports: dict[tuple[int, int], tuple[tuple[int, int], ...]],
    parameter_order: tuple[tuple[int, int], ...],
) -> tuple[Polynomial, list[tuple[Matching, int, Exponent]]]:
    polynomial: Polynomial = {}
    records = []
    for matching in MATCHINGS:
        term = matching_term(word, matching, supports, parameter_order)
        if term is None:
            continue
        coefficient, exponent = term
        add_term(polynomial, exponent, coefficient)
        records.append((matching, coefficient, exponent))
    return polynomial, records


def target(word: tuple[int, ...], width: int) -> Polynomial:
    return {(0,) * width: 1} if len(set(word)) == 1 else {}


def ab_word(center_left: int, leaves_left: int, center_right: int, leaves_right: int):
    return (
        center_left,
        leaves_left,
        leaves_left,
        leaves_left,
        center_right,
        leaves_right,
        leaves_right,
        leaves_right,
    )


def matching_class(matching: Matching) -> str:
    crossing = tuple(edge for edge in matching if (edge[0] < 4) != (edge[1] < 4))
    if not crossing:
        return "internal_component"
    if len(crossing) == 4:
        return "degree4"
    left_vertices = {vertex for edge in crossing for vertex in edge if vertex < 4}
    right_vertices = {vertex - 4 for edge in crossing for vertex in edge if vertex >= 4}
    left_type = "AB" if 0 in left_vertices else "BB"
    right_type = "AB" if 0 in right_vertices else "BB"
    if (left_type, right_type) != ("AB", "AB"):
        return f"degree2_{left_type}_{right_type}"
    if all((left == 0) == (right == 4) for left, right in crossing):
        return "separated_AB"
    return "mixed_center_leaf_AB"


def evaluate_at_one(polynomial: Polynomial) -> int:
    return sum(polynomial.values())


def projected_matrix_at_one(
    supports: dict[tuple[int, int], tuple[tuple[int, int], ...]],
    parameter_order: tuple[tuple[int, int], ...],
):
    by_class = defaultdict(lambda: [[0, 0], [0, 0]])
    total = [[0, 0], [0, 0]]
    for x0, y0, x1, y1 in product(range(3), repeat=4):
        word = ab_word(x0, y0, x1, y1)
        _polynomial, records = amplitude(word, supports, parameter_order)
        for matching, coefficient, _exponent in records:
            kind = matching_class(matching)
            for row in range(2):
                for column in range(2):
                    contribution = coefficient * PROBES[row][x0] * PROBES[column][y1]
                    by_class[kind][row][column] += contribution
                    total[row][column] += contribution
    return dict(by_class), total


def assert_ab_family(
    fixture: dict,
    family: dict,
    split_failures: dict[tuple[int, ...], tuple[int, Exponent, Matching]],
) -> None:
    parameter_order = tuple(tuple(pair) for pair in fixture["parameter_order"])
    supports = support_map(fixture, family)
    checked = 0
    for x0, y0, x1, y1 in product(range(3), repeat=4):
        word = ab_word(x0, y0, x1, y1)
        polynomial, _records = amplitude(word, supports, parameter_order)
        assert polynomial == target(word, len(parameter_order)), (family["name"], word)
        checked += 1
    assert checked == 81

    for word, (coefficient, exponent, expected_matching) in split_failures.items():
        polynomial, records = amplitude(word, supports, parameter_order)
        assert polynomial == {exponent: coefficient}, (family["name"], word, polynomial)
        assert records == [(expected_matching, coefficient, exponent)], records

    _by_class, projected = projected_matrix_at_one(supports, parameter_order)
    assert projected == [[2, 1], [1, 2]]


def assert_v2_class_table(fixture: dict, family: dict) -> None:
    parameter_order = tuple(tuple(pair) for pair in fixture["parameter_order"])
    by_class, _projected = projected_matrix_at_one(
        support_map(fixture, family), parameter_order
    )
    expected = {
        "internal_component": [[0, 0], [0, 0]],
        "separated_AB": [[0, 0], [-1, 0]],
        "degree2_BB_AB": [[0, 0], [1, 1]],
        "degree2_BB_BB": [[2, 1], [1, 0]],
        "mixed_center_leaf_AB": [[0, 1], [0, 1]],
        "degree2_AB_BB": [[0, -1], [0, 0]],
        "degree4": [[0, 0], [0, 0]],
    }
    zero = [[0, 0], [0, 0]]
    assert set(by_class) <= set(expected), by_class
    assert all(by_class.get(kind, zero) == matrix for kind, matrix in expected.items()), by_class


def assert_separator_combinatorics() -> None:
    # Any two uncut protected color matchings force a K4 onto one shore.
    for shore_bits in product(range(2), repeat=4):
        uncut = [
            matching
            for matching in PROTECTED_MATCHINGS
            if all(shore_bits[u] == shore_bits[v] for u, v in matching)
        ]
        if len(uncut) >= 2:
            assert len(set(shore_bits)) == 1

    # The note's explicit free hollow block is invertible.
    hollow = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
    determinant = (
        hollow[0][0] * (hollow[1][1] * hollow[2][2] - hollow[1][2] * hollow[2][1])
        - hollow[0][1] * (hollow[1][0] * hollow[2][2] - hollow[1][2] * hollow[2][0])
        + hollow[0][2] * (hollow[1][0] * hollow[2][1] - hollow[1][1] * hollow[2][0])
    )
    assert determinant == 2


def assert_frozen_cover(fixture: dict, family: dict) -> None:
    """Reconstruct the actual matching cover, without the primary classifier."""
    parameter_order = tuple(tuple(pair) for pair in fixture["parameter_order"])
    supports = support_map(fixture, family)
    covered = set()
    for a, b in parameter_order:
        word = (a,) * 4 + (b,) * 4
        polynomial, records = amplitude(word, supports, parameter_order)
        assert not polynomial
        assert len(records) == 2
        assert sorted(coefficient for _, coefficient, _ in records) == [-1, 1]
        assert all(exponent == (0,) * 6 for _, _, exponent in records)
        for matching, _, _ in records:
            for left, right in matching:
                if left < 4 <= right:
                    covered.add((a, b, left, right - 4))
    actual = {(a, b, u, v) for (a, b), positions in supports.items()
              for u, v in positions}
    assert len(actual) == 12 and covered == actual


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    families = {family["name"]: family for family in fixture["families"]}
    v2 = families["binary_and_monochromatic_shores_v2"]
    v3 = families["independent_minorities_and_component_constants_v3"]

    assert len(MATCHINGS) == 105
    assert_ab_family(
        fixture,
        v2,
        {
            (0, 0, 0, 2, 0, 0, 1, 1): (
                -1,
                (1, 0, 0, 0, 0, -1),
                ((0, 1), (2, 7), (3, 6), (4, 5)),
            ),
            (0, 1, 0, 0, 0, 0, 0, 2): (
                1,
                (0, 1, 1, 0, 0, 0),
                ((0, 7), (1, 6), (2, 3), (4, 5)),
            ),
        },
    )
    assert_v2_class_table(fixture, v2)
    assert_ab_family(
        fixture,
        v3,
        {
            (0, 0, 0, 1, 0, 2, 2, 1): (
                -1,
                (1, 0, -1, 0, 0, 0),
                ((0, 1), (2, 7), (3, 4), (5, 6)),
            )
        },
    )
    assert_separator_combinatorics()
    assert_frozen_cover(fixture, v2)
    assert_frozen_cover(fixture, v3)

    print("independent continuation audit: PASS")
    print("  105 physical perfect matchings reconstructed")
    print("  v2 and v3: all 81 AB words equal the Laurent GHZ target")
    print("  three cited split-leaf words have their unique Laurent monomials")
    print("  v2 matching-class probe table and rank-two target reproduced")
    print("  protected-K4 cut combinatorics and invertible hollow control pass")
    print("  both controls have all 12 entries frozen by actual component matchings")


if __name__ == "__main__":
    main()
