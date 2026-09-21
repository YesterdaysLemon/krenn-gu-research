"""Independent exact audit of the common-star full-source exclusion.

This portable checker uses only the Python standard library.  It constructs the
literal 4k-vertex protected scaffold, evaluates its hafnian by a physical
perfect-matching recurrence, and compares it with the proposed A/B projection.
It is a finite replay of small controls, not the arbitrary-order proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import prod


Color = int
Word = tuple[Color, ...]


@dataclass(frozen=True)
class Gadget:
    u: int
    v: int
    color_u: Color
    color_v: Color
    center_weight: Fraction
    leaf_weight: Fraction


Edge = tuple[int, int, Color, Color, Fraction, str]


def physical_vertex(component: int, local_vertex: int) -> int:
    return 4 * component + local_vertex


def protected_edges(k: int) -> list[Edge]:
    matchings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    edges: list[Edge] = []
    for component in range(k):
        for color, matching in enumerate(matchings):
            for left, right in matching:
                edges.append(
                    (
                        physical_vertex(component, left),
                        physical_vertex(component, right),
                        color,
                        color,
                        Fraction(1),
                        "internal",
                    )
                )
    return edges


def literal_edges(k: int, gadgets: tuple[Gadget, ...]) -> list[Edge]:
    edges = protected_edges(k)
    for gadget in gadgets:
        edges.append(
            (
                physical_vertex(gadget.u, 0),
                physical_vertex(gadget.v, 0),
                gadget.color_u,
                gadget.color_v,
                gadget.center_weight,
                "A",
            )
        )
        edges.append(
            (
                physical_vertex(gadget.u, gadget.color_u + 1),
                physical_vertex(gadget.v, gadget.color_v + 1),
                gadget.color_u,
                gadget.color_v,
                gadget.leaf_weight,
                "B",
            )
        )
    return edges


def eligible_adjacency(
    word: Word, edges: list[Edge]
) -> list[list[tuple[int, Fraction, str]]]:
    adjacency: list[list[tuple[int, Fraction, str]]] = [
        [] for _ in range(len(word))
    ]
    for left, right, color_left, color_right, weight, kind in edges:
        if word[left] == color_left and word[right] == color_right:
            adjacency[left].append((right, weight, kind))
            adjacency[right].append((left, weight, kind))
    return adjacency


def literal_hafnian(word: Word, edges: list[Edge]) -> Fraction:
    adjacency = eligible_adjacency(word, edges)
    memo: dict[int, Fraction] = {0: Fraction(1)}

    def recurrence(mask: int) -> Fraction:
        if mask in memo:
            return memo[mask]
        left_bit = mask & -mask
        left = left_bit.bit_length() - 1
        remainder = mask ^ left_bit
        total = Fraction(0)
        for right, weight, _kind in adjacency[left]:
            right_bit = 1 << right
            if remainder & right_bit:
                total += weight * recurrence(remainder ^ right_bit)
        memo[mask] = total
        return total

    return recurrence((1 << len(word)) - 1)


def enumerate_literal_matchings(word: Word, edges: list[Edge]) -> list[tuple[Edge, ...]]:
    adjacency: list[list[tuple[int, Edge]]] = [[] for _ in range(len(word))]
    for edge in edges:
        left, right, color_left, color_right, _weight, _kind = edge
        if word[left] == color_left and word[right] == color_right:
            adjacency[left].append((right, edge))
            adjacency[right].append((left, edge))

    def recurrence(mask: int) -> list[tuple[Edge, ...]]:
        if mask == 0:
            return [()]
        left_bit = mask & -mask
        left = left_bit.bit_length() - 1
        remainder = mask ^ left_bit
        answer: list[tuple[Edge, ...]] = []
        for right, edge in adjacency[left]:
            right_bit = 1 << right
            if remainder & right_bit:
                for tail in recurrence(remainder ^ right_bit):
                    answer.append((edge, *tail))
        return answer

    return recurrence((1 << len(word)) - 1)


def uniform_leaf_word(x: Word, y: Word) -> Word:
    assert len(x) == len(y)
    return tuple(color for pair in zip(x, y) for color in (pair[0], pair[1], pair[1], pair[1]))


def small_hafnian(vertices: tuple[int, ...], weights: dict[tuple[int, int], Fraction]) -> Fraction:
    if not vertices:
        return Fraction(1)
    left = vertices[0]
    total = Fraction(0)
    for index in range(1, len(vertices)):
        right = vertices[index]
        pair = (min(left, right), max(left, right))
        weight = weights.get(pair, Fraction(0))
        if weight:
            remainder = vertices[1:index] + vertices[index + 1 :]
            total += weight * small_hafnian(remainder, weights)
    return total


def projected_source(x: Word, y: Word, gadgets: tuple[Gadget, ...]) -> Fraction:
    k = len(x)
    center: dict[tuple[int, int], Fraction] = {}
    leaf: dict[tuple[int, int], Fraction] = {}
    for gadget in gadgets:
        if x[gadget.u] == gadget.color_u and x[gadget.v] == gadget.color_v:
            center[(gadget.u, gadget.v)] = gadget.center_weight
        if y[gadget.u] == gadget.color_u and y[gadget.v] == gadget.color_v:
            leaf[(gadget.u, gadget.v)] = gadget.leaf_weight

    total = Fraction(0)
    for mask in range(1 << k):
        vertices = tuple(index for index in range(k) if mask & (1 << index))
        if len(vertices) % 2:
            continue
        if any(x[index] != y[index] for index in range(k) if not mask & (1 << index)):
            continue
        total += small_hafnian(vertices, center) * small_hafnian(vertices, leaf)
    return total


def assert_only_ab_crossings(k: int, gadgets: tuple[Gadget, ...]) -> None:
    edges = literal_edges(k, gadgets)
    colors = tuple(product(range(3), repeat=k))
    for x in colors:
        for y in colors:
            word = uniform_leaf_word(x, y)
            for matching in enumerate_literal_matchings(word, edges):
                crossing_kinds: list[list[str]] = [[] for _ in range(k)]
                for left, right, _cl, _cr, _weight, kind in matching:
                    if kind == "internal":
                        continue
                    crossing_kinds[left // 4].append(kind)
                    crossing_kinds[right // 4].append(kind)
                for kinds in crossing_kinds:
                    assert sorted(kinds) in ([], ["A", "B"]), (x, y, kinds)


def assert_projection(k: int, gadgets: tuple[Gadget, ...]) -> int:
    edges = literal_edges(k, gadgets)
    colors = tuple(product(range(3), repeat=k))
    cases = 0
    for x in colors:
        for y in colors:
            literal = literal_hafnian(uniform_leaf_word(x, y), edges)
            projected = projected_source(x, y, gadgets)
            assert literal == projected, (k, x, y, literal, projected)
            cases += 1
    return cases


def full_source_table(k: int, gadgets: tuple[Gadget, ...]) -> dict[tuple[Word, Word], Fraction]:
    colors = tuple(product(range(3), repeat=k))
    return {(x, y): projected_source(x, y, gadgets) for x in colors for y in colors}


def dot(left: Word, right: Word) -> int:
    return sum(a * b for a, b in zip(left, right))


def product_entry(vectors: tuple[Word, ...], coloring: Word) -> int:
    answer = 1
    for vector, color in zip(vectors, coloring):
        answer *= vector[color]
    return answer


def contract(
    table: dict[tuple[Word, Word], Fraction],
    row_vectors: tuple[Word, ...],
    column_vectors: tuple[Word, ...],
) -> Fraction:
    assert all(dot(row, column) == 0 for row, column in zip(row_vectors, column_vectors))
    return sum(
        product_entry(row_vectors, x) * value * product_entry(column_vectors, y)
        for (x, y), value in table.items()
    )


def target_contract(row_vectors: tuple[Word, ...], column_vectors: tuple[Word, ...]) -> int:
    return sum(
        product_entry(row_vectors, (color,) * len(row_vectors))
        * product_entry(column_vectors, (color,) * len(column_vectors))
        for color in range(3)
    )


def assert_odd_diagonal_trace(k: int, gadgets: tuple[Gadget, ...]) -> None:
    assert k % 2 == 1 and k >= 3
    t = (1, 1, -2)
    colors = tuple(product(range(3), repeat=k))
    source = sum(
        prod(t[color] for color in x) * projected_source(x, x, gadgets)
        for x in colors
    )
    target = sum(entry**k for entry in t)
    assert source == 0
    assert target == 2 + (-2) ** k != 0


def assert_even_rank_test(k: int, gadgets: tuple[Gadget, ...]) -> None:
    assert k % 2 == 0 and k >= 2
    table = full_source_table(k, gadgets)
    one = (1, 1, 1)
    t = (1, 1, -2)
    variants = ((1, -1, 0), (1, 0, -1))
    rows = tuple((variant,) + (one,) * (k - 1) for variant in variants)
    columns = tuple((one, variant) + (t,) * (k - 2) for variant in variants)
    source = tuple(
        tuple(contract(table, row, column) for column in columns) for row in rows
    )
    target = tuple(
        tuple(target_contract(row, column) for column in columns) for row in rows
    )
    source_det = source[0][0] * source[1][1] - source[0][1] * source[1][0]
    target_det = target[0][0] * target[1][1] - target[0][1] * target[1][0]
    assert source_det == 0, source
    assert target == ((2, 1), (1, 1 + 2 ** (k - 2)))
    assert target_det == 1 + 2 ** (k - 1) != 0


def assert_k1_full_ghz_control() -> None:
    edges = literal_edges(1, ())
    for word in product(range(3), repeat=4):
        expected = Fraction(int(len(set(word)) == 1))
        assert literal_hafnian(word, edges) == expected, word


def fixtures() -> tuple[tuple[int, tuple[Gadget, ...]], ...]:
    return (
        (2, (Gadget(0, 1, 0, 1, Fraction(2), Fraction(3)),)),
        (
            3,
            (
                Gadget(0, 1, 0, 1, Fraction(2), Fraction(-3)),
                Gadget(1, 2, 2, 0, Fraction(5), Fraction(7)),
                Gadget(0, 2, 1, 2, Fraction(-11), Fraction(13)),
            ),
        ),
        (
            4,
            (
                Gadget(0, 1, 0, 1, Fraction(2), Fraction(3)),
                Gadget(1, 2, 2, 0, Fraction(-5), Fraction(7)),
                Gadget(2, 3, 1, 2, Fraction(11), Fraction(-13)),
                Gadget(0, 3, 2, 1, Fraction(17), Fraction(19)),
                Gadget(0, 2, 1, 0, Fraction(-23), Fraction(29)),
            ),
        ),
    )


def main() -> None:
    assert_k1_full_ghz_control()
    checked = 0
    for k, gadgets in fixtures():
        checked += assert_projection(k, gadgets)
        if k <= 3:
            assert_only_ab_crossings(k, gadgets)
        if k % 2:
            assert_odd_diagonal_trace(k, gadgets)
        else:
            assert_even_rank_test(k, gadgets)
    print("independent literal AB-projection audit: PASS")
    print(f"  literal projected-word equalities: {checked}")
    print("  k=1 protected K4 realizes the full one-component GHZ target")
    print("  no BB or degree-four crossing occurs in enumerated special-word matchings")
    print("  odd diagonal component-target trace and even full-source rank tests pass")


if __name__ == "__main__":
    main()
