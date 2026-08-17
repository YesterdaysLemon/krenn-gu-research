"""Focused exact checks for surplus-two nonzero-companion sharpness."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

ROOTS = ("r0", "r1", "r2")
OUTSIDE = ("u0", "u1", "u2", "u3", "u4")
VERTICES = ROOTS + OUTSIDE

CROSS_COLOUR = {
    ("r0", "u0"): 1,
    ("r0", "u1"): 0,
    ("r0", "u2"): 2,
    ("r1", "u0"): 2,
    ("r1", "u1"): 1,
    ("r1", "u2"): 0,
    ("r2", "u2"): 1,
    ("r2", "u3"): 0,
    ("r2", "u4"): 2,
}


def pair_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


OUTSIDE_COLOUR = {
    pair_key(left, right): (
        1
        if {left, right} == {"u3", "u4"}
        else 2
        if {left, right} == {"u1", "u3"}
        else 0
    )
    for left, right in combinations(OUTSIDE, 2)
}


def injection_column(outside_triple: tuple[str, ...]) -> dict[str, int]:
    """Directly enumerate root-to-outside injections and their root words."""

    column: dict[str, int] = {}
    for assigned in permutations(outside_triple):
        colours: list[int] = []
        for root, outside in zip(ROOTS, assigned, strict=True):
            colour = CROSS_COLOUR.get((root, outside))
            if colour is None:
                break
            colours.append(colour)
        else:
            word = "".join(map(str, colours))
            column[word] = column.get(word, 0) + 1
    return column


def check_sensor() -> None:
    pair_labels = tuple(combinations(range(5), 2))
    order_four_labels = tuple(combinations(range(5), 4))
    deck_labels = pair_labels + order_four_labels
    rows = tuple("".join(map(str, word)) for word in product(range(3), repeat=3))

    columns: dict[tuple[int, ...], dict[str, int]] = {}
    for pair in pair_labels:
        triple = tuple(OUTSIDE[index] for index in range(5) if index not in pair)
        columns[pair] = injection_column(triple)
    for label in order_four_labels:
        columns[label] = {}  # all p>=1 columns vanish when root-root blocks vanish

    expected = {
        (0, 1, 2): {"111": 1, "021": 1},
        (0, 1, 3): {"110": 1, "020": 1},
        (0, 1, 4): {"112": 1, "022": 1},
        (0, 2, 3): {"100": 1, "220": 1},
        (0, 2, 4): {"102": 1, "222": 1},
        (1, 2, 3): {"000": 1, "210": 1},
        (1, 2, 4): {"002": 1, "212": 1},
    }
    for triple, support in expected.items():
        pair = tuple(index for index in range(5) if index not in triple)
        assert columns[pair] == support

    invisible = {(0, 1), (0, 2), (1, 2)}
    assert {label for label in pair_labels if not columns[label]} == invisible
    matrix = sp.Matrix(
        [[columns[label].get(row, 0) for label in deck_labels] for row in rows]
    )
    assert matrix.rank() == 7

    for residual_pair in pair_labels:
        desired = {
            label
            for label in deck_labels
            if len(set(label) & set(residual_pair)) in (0, 2)
        }
        assert desired & invisible


def matching_list(vertices: tuple[str, ...]) -> list[tuple[tuple[str, str], ...]]:
    if not vertices:
        return [()]
    first = vertices[0]
    result: list[tuple[tuple[str, str], ...]] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matching_list(rest):
            result.append(((first, partner),) + tail)
    return result


def edge_term(left: str, right: str) -> tuple[int, sp.Expr] | None:
    if left in ROOTS and right in ROOTS:
        return None
    if right in ROOTS:
        left, right = right, left
    if left in ROOTS:
        colour = CROSS_COLOUR.get((left, right))
        if colour is None:
            return None
        return colour, sp.Symbol(f"a_{left[1]}{right[1]}")
    colour = OUTSIDE_COLOUR[pair_key(left, right)]
    return colour, sp.Symbol(f"b_{left[1]}{right[1]}")


def full_state() -> tuple[
    dict[str, sp.Expr], dict[str, list[frozenset[tuple[str, str]]]]
]:
    coefficients: dict[str, sp.Expr] = {}
    supports: dict[str, list[frozenset[tuple[str, str]]]] = {}
    for matching in matching_list(VERTICES):
        word = [-1] * len(VERTICES)
        coefficient: sp.Expr = sp.Integer(1)
        used_edges: set[tuple[str, str]] = set()
        for left, right in matching:
            term = edge_term(left, right)
            if term is None:
                break
            colour, weight = term
            word[VERTICES.index(left)] = colour
            word[VERTICES.index(right)] = colour
            coefficient *= weight
            used_edges.add(pair_key(left, right))
        else:
            key = "".join(map(str, word))
            coefficients[key] = sp.expand(coefficients.get(key, 0) + coefficient)
            supports.setdefault(key, []).append(frozenset(used_edges))
    return coefficients, supports


def check_graph_family() -> None:
    row_colours = {
        outside: {
            colour
            for (root, candidate), colour in CROSS_COLOUR.items()
            if candidate == outside
        }
        for outside in OUTSIDE
    }
    assert tuple(len(row_colours[outside]) for outside in OUTSIDE) == (2, 2, 3, 1, 1)
    assert sum(3 - len(row_colours[outside]) for outside in OUTSIDE) == 6
    blockers = {
        colour: {
            outside for outside, colours in row_colours.items() if colour in colours
        }
        for colour in range(3)
    }
    assert blockers == {
        0: {"u1", "u2", "u3"},
        1: {"u0", "u1", "u2"},
        2: {"u0", "u2", "u4"},
    }

    incident = {vertex: set() for vertex in VERTICES}
    for (root, outside), colour in CROSS_COLOUR.items():
        incident[root].add(colour)
        incident[outside].add(colour)
    for (left, right), colour in OUTSIDE_COLOUR.items():
        incident[left].add(colour)
        incident[right].add(colour)
    assert all(colours == {0, 1, 2} for colours in incident.values())

    coefficients, supports = full_state()
    pure_expected = {
        "00000000": sp.Symbol("a_01")
        * sp.Symbol("a_12")
        * sp.Symbol("a_23")
        * sp.Symbol("b_04"),
        "11111111": sp.Symbol("a_00")
        * sp.Symbol("a_11")
        * sp.Symbol("a_22")
        * sp.Symbol("b_34"),
        "22222222": sp.Symbol("a_02")
        * sp.Symbol("a_10")
        * sp.Symbol("a_24")
        * sp.Symbol("b_13"),
    }
    for word, expected in pure_expected.items():
        assert sp.expand(coefficients.get(word, 0) - expected) == 0
        assert len(supports[word]) == 1

    for colour in range(3):
        pure = [colour] * len(VERTICES)
        for vertex in range(len(VERTICES)):
            for replacement in range(3):
                if replacement == colour:
                    continue
                word = pure.copy()
                word[vertex] = replacement
                assert coefficients.get("".join(map(str, word)), 0) == 0

    for vertex in range(len(VERTICES)):
        flattening_minor = sp.Matrix(
            [
                [
                    coefficients.get(
                        "".join(
                            map(
                                str,
                                [
                                    row_colour if index == vertex else column_colour
                                    for index in range(len(VERTICES))
                                ],
                            )
                        ),
                        0,
                    )
                    for column_colour in range(3)
                ]
                for row_colour in range(3)
            ]
        )
        assert sp.expand(flattening_minor.det()) != 0

    mixed = "02120111"
    expected_mixed = (
        sp.Symbol("a_01") * sp.Symbol("a_10") * sp.Symbol("a_22") * sp.Symbol("b_34")
    )
    assert sp.expand(coefficients[mixed] - expected_mixed) == 0
    assert len(supports[mixed]) == 1

    invisible_edges = {
        pair_key("u0", "u1"),
        pair_key("u0", "u2"),
        pair_key("u1", "u2"),
    }
    assert all(
        matching_edges.isdisjoint(invisible_edges)
        for word_supports in supports.values()
        for matching_edges in word_supports
    )


def check_symmetric_product_lemma() -> None:
    for r in range(3, 9):
        for support_size in (1, 2, 3, r):
            support_size = min(support_size, r)
            b = [sp.Integer(index < support_size) for index in range(r)]
            matrix = sp.Matrix(
                [
                    [
                        (b[j] if column == i else 0) + (b[i] if column == j else 0)
                        for column in range(r)
                    ]
                    for i, j in combinations(range(r), 2)
                ]
            )
            assert r - matrix.rank() <= 1


def main() -> None:
    check_sensor()
    check_graph_family()
    check_symmetric_product_lemma()
    print("surplus-two nonzero-companion and physical rank-drop verifier: PASS")


if __name__ == "__main__":
    main()
