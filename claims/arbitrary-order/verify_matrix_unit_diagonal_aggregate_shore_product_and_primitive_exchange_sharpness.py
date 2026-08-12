"""Primary exact checks for diagonal aggregate shore-product sharpness."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from math import gcd

import sympy as sp

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Table = dict[Edge, tuple[int, int, sp.Expr]]

ORDER = 12
T = sp.symbols("t")
X = -(1 + T)


def canonical_matching(*edges: Edge) -> Matching:
    """Return a consistently ordered matching."""
    return tuple(sorted((min(left, right), max(left, right)) for left, right in edges))


def complete_table() -> Table:
    """Return the complete twelve-vertex matrix-unit table."""
    old_raw: dict[Edge, tuple[int, int, sp.Expr | int]] = {
        (0, 1): (0, 0, 1),
        (0, 2): (0, 0, 1),
        (0, 3): (0, 0, 1),
        (0, 4): (0, 0, 1),
        (0, 5): (1, 2, 1),
        (0, 6): (1, 1, 1),
        (0, 7): (2, 2, 1),
        (1, 2): (0, 1, -1),
        (1, 3): (0, 0, 1),
        (1, 4): (1, 0, -1),
        (1, 5): (1, 1, 1),
        (1, 6): (2, 2, 1),
        (1, 7): (0, 0, 1),
        (2, 3): (1, 1, 1),
        (2, 4): (0, 1, X),
        (2, 5): (2, 2, 1),
        (2, 6): (0, 0, 1),
        (2, 7): (2, 0, 1),
        (3, 4): (2, 2, 1),
        (3, 5): (0, 1, 1),
        (3, 6): (1, 0, 1),
        (3, 7): (1, 1, 1),
        (4, 5): (0, 0, 1),
        (4, 6): (1, 1, 1),
        (4, 7): (1, 1, 1),
        (5, 6): (0, 1, 1),
        (5, 7): (1, 1, 1),
        (6, 7): (1, 1, 1),
    }
    table: Table = {
        edge: (left_label, right_label, sp.sympify(weight))
        for edge, (left_label, right_label, weight) in old_raw.items()
    }

    new_new: dict[Edge, tuple[int, int, sp.Expr | int]] = {
        (8, 9): (0, 0, 1),
        (8, 10): (0, 0, 1),
        (8, 11): (1, 1, 1),
        (9, 10): (1, 1, 1),
        (9, 11): (0, 0, 1),
        (10, 11): (1, 1, 1),
    }
    table.update(
        {
            edge: (left_label, right_label, sp.sympify(weight))
            for edge, (left_label, right_label, weight) in new_new.items()
        }
    )

    for old in range(8):
        for new in range(8, 12):
            if new in (8, 9):
                table[(old, new)] = (0, 1, sp.Integer(1))
            else:
                table[(old, new)] = (1, 0, sp.Integer(1))

    overrides: dict[Edge, tuple[int, int, sp.Expr | int]] = {
        (0, 8): (2, 2, 1),
        (1, 9): (2, 2, 1),
        (2, 8): (0, 0, T),
        (3, 9): (0, 0, 1),
        (6, 10): (2, 2, 1),
        (7, 11): (2, 2, 1),
        (1, 11): (1, 0, 2),
    }
    table.update(
        {
            edge: (left_label, right_label, sp.sympify(weight))
            for edge, (left_label, right_label, weight) in overrides.items()
        }
    )
    return table


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate perfect matchings by pairing the first remaining vertex."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        residue = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(residue):
            yield ((first, partner),) + tail


def matching_record(
    matching: Matching,
    table: Table,
) -> tuple[Word, sp.Expr, bool]:
    """Return the induced word, exact weight, and diagonal flag."""
    word = [-1] * ORDER
    weight: sp.Expr = sp.Integer(1)
    diagonal = True
    for left, right in matching:
        left_label, right_label, scalar = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        weight *= scalar
        diagonal = diagonal and left_label == right_label
    return tuple(word), sp.expand(weight), diagonal


def fibre_ledgers(table: Table):
    """Enumerate every physical matching and group it by its full word."""
    terms: dict[Word, list[tuple[Matching, sp.Expr, bool]]] = defaultdict(list)
    for matching in perfect_matchings(tuple(range(ORDER))):
        word, weight, diagonal = matching_record(matching, table)
        terms[word].append((matching, weight, diagonal))
    return terms


def polynomial_sum(values: list[sp.Expr]) -> sp.Expr:
    """Add and normalize exact univariate polynomials."""
    return sp.expand(sum(values, sp.Integer(0)))


def word(text: str) -> Word:
    """Parse a ternary word."""
    return tuple(map(int, text))


def matching_map(
    records: list[tuple[Matching, sp.Expr, bool]],
) -> dict[Matching, tuple[sp.Expr, bool]]:
    """Index a complete fibre by matching."""
    return {
        canonical_matching(*matching): (sp.expand(weight), diagonal)
        for matching, weight, diagonal in records
    }


def shore_matchings(
    vertices: tuple[int, ...],
    colour: int,
    table: Table,
) -> list[Matching]:
    """Enumerate compatible pure-colour matchings on one shore."""
    output = []
    for matching in perfect_matchings(vertices):
        if all(table[edge][0] == table[edge][1] == colour for edge in matching):
            output.append(canonical_matching(*matching))
    return output


def matching_weight(matching: Matching, table: Table) -> sp.Expr:
    """Multiply exact edge weights."""
    return sp.expand(sp.prod(table[edge][2] for edge in matching))


def incidence_difference(
    positive: Matching,
    negative: Matching,
    edges: tuple[Edge, ...],
) -> list[int]:
    """Return one matching-incidence difference in the ambient edge basis."""
    positive_set = set(positive)
    negative_set = set(negative)
    return [
        int(edge in positive_set) - int(edge in negative_set)
        for edge in edges
    ]


def support(vector: list[int], edges: tuple[Edge, ...]) -> set[Edge]:
    """Return the nonzero edge support of an incidence vector."""
    return {edge for edge, coefficient in zip(edges, vector, strict=True) if coefficient}


def check_no_cancelling_subshore(
    vertices: tuple[int, ...],
    colour: int,
    table: Table,
) -> None:
    """Check that every supported even subshore has nonzero exact hafnian."""
    for size in range(2, len(vertices) + 1, 2):
        for subset in combinations(vertices, size):
            matchings = shore_matchings(subset, colour, table)
            if not matchings:
                continue
            value = polynomial_sum(
                [matching_weight(matching, table) for matching in matchings]
            )
            assert value != 0


def main() -> None:
    """Run the exact symbolic verification."""
    table = complete_table()
    all_edges = tuple(combinations(range(ORDER), 2))
    assert set(table) == set(all_edges)
    assert len(table) == 66
    assert all(weight != 0 for _, _, weight in table.values())

    endpoint_labels = [set() for _ in range(ORDER)]
    for (left, right), (left_label, right_label, _) in table.items():
        endpoint_labels[left].add(left_label)
        endpoint_labels[right].add(right_label)
    assert endpoint_labels == [{0, 1, 2} for _ in range(ORDER)]

    terms = fibre_ledgers(table)
    assert sum(map(len, terms.values())) == 10395
    assert len(terms) == 5128
    assert sum(len(records) == 1 for records in terms.values()) == 2979

    chi_0 = word("000011110011")
    chi_1 = word("001100110011")
    chi_2 = word("010101010011")

    f_0 = canonical_matching(
        (0, 1), (2, 4), (3, 5), (6, 7), (8, 9), (10, 11)
    )
    extra = canonical_matching(
        (0, 1), (2, 8), (3, 9), (4, 6), (5, 7), (10, 11)
    )
    g_2 = canonical_matching(
        (0, 2), (1, 3), (4, 6), (5, 7), (8, 9), (10, 11)
    )
    g_0 = canonical_matching(
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)
    )
    f_1 = canonical_matching(
        (0, 4), (1, 2), (3, 7), (5, 6), (8, 9), (10, 11)
    )
    f_2 = canonical_matching(
        (0, 2), (1, 4), (3, 6), (5, 7), (8, 9), (10, 11)
    )
    g_1 = canonical_matching(
        (0, 4), (1, 5), (2, 6), (3, 7), (8, 9), (10, 11)
    )

    expected_fibres = {
        chi_0: {
            f_0: (X, False),
            extra: (T, True),
            g_2: (sp.Integer(1), True),
        },
        chi_1: {
            g_0: (sp.Integer(1), True),
            f_1: (sp.Integer(-1), False),
        },
        chi_2: {
            f_2: (sp.Integer(-1), False),
            g_1: (sp.Integer(1), True),
        },
    }
    for target_word, expected in expected_fibres.items():
        assert matching_map(terms[target_word]) == expected
        assert polynomial_sum([weight for _, weight, _ in terms[target_word]]) == 0

    pure_matchings = {
        (0,) * ORDER: canonical_matching(
            (0, 3), (1, 7), (2, 6), (4, 5), (8, 10), (9, 11)
        ),
        (1,) * ORDER: canonical_matching(
            (0, 6), (1, 5), (2, 3), (4, 7), (8, 11), (9, 10)
        ),
        (2,) * ORDER: canonical_matching(
            (0, 8), (1, 9), (2, 5), (3, 4), (6, 10), (7, 11)
        ),
    }
    for pure_word, pure_matching in pure_matchings.items():
        assert matching_map(terms[pure_word]) == {
            pure_matching: (sp.Integer(1), True)
        }

    total_coefficients = {
        target_word: polynomial_sum([weight for _, weight, _ in records])
        for target_word, records in terms.items()
    }
    offdiagonal_coefficients = {
        target_word: polynomial_sum(
            [weight for _, weight, diagonal in records if not diagonal]
        )
        for target_word, records in terms.items()
    }
    active_words = {
        target_word
        for target_word in terms
        if total_coefficients[target_word] == 0
        and offdiagonal_coefficients[target_word] != 0
    }
    assert active_words == {chi_0, chi_1, chi_2}

    bridges = (
        (
            canonical_matching((2, 4), (3, 5)),
            canonical_matching((2, 3), (4, 5)),
            canonical_matching((0, 1), (6, 7), (8, 9), (10, 11)),
            f_0,
            g_0,
            chi_0,
            chi_1,
        ),
        (
            canonical_matching((1, 2), (5, 6)),
            canonical_matching((1, 5), (2, 6)),
            canonical_matching((0, 4), (3, 7), (8, 9), (10, 11)),
            f_1,
            g_1,
            chi_1,
            chi_2,
        ),
        (
            canonical_matching((1, 4), (3, 6)),
            canonical_matching((1, 3), (4, 6)),
            canonical_matching((0, 2), (5, 7), (8, 9), (10, 11)),
            f_2,
            g_2,
            chi_2,
            chi_0,
        ),
    )
    for cross, bridge, residue, outgoing, successor, source_word, next_word in bridges:
        assert canonical_matching(*(cross + residue)) == outgoing
        assert canonical_matching(*(bridge + residue)) == successor
        assert matching_record(outgoing, table)[0] == source_word
        successor_record = matching_record(successor, table)
        assert successor_record[0] == next_word
        assert successor_record[2]

    zero_vertices = (0, 1, 2, 3, 8, 9)
    one_vertices = (4, 5, 6, 7, 10, 11)
    zero_shore = shore_matchings(zero_vertices, 0, table)
    one_shore = shore_matchings(one_vertices, 1, table)
    empty_shore = shore_matchings((), 2, table)
    p_zero = canonical_matching((0, 2), (1, 3), (8, 9))
    m_zero = canonical_matching((0, 1), (2, 8), (3, 9))
    p_one = canonical_matching((4, 6), (5, 7), (10, 11))
    assert set(zero_shore) == {p_zero, m_zero}
    assert one_shore == [p_one]
    assert empty_shore == [()]
    assert polynomial_sum([matching_weight(item, table) for item in zero_shore]) == 1 + T
    assert matching_weight(p_one, table) == 1
    assert len(zero_shore) * len(one_shore) * len(empty_shore) == 2

    symmetric_difference = set(p_zero) ^ set(m_zero)
    assert symmetric_difference == {
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 8),
        (3, 9),
        (8, 9),
    }
    degrees = defaultdict(int)
    adjacency: dict[int, set[int]] = defaultdict(set)
    for left, right in symmetric_difference:
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    assert set(degrees.values()) == {2}
    seen = set()
    stack = [0]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    assert seen == set(degrees)

    u_0 = incidence_difference(f_0, g_2, all_edges)
    u_1 = incidence_difference(f_1, g_0, all_edges)
    u_2 = incidence_difference(f_2, g_1, all_edges)
    delta = incidence_difference(extra, g_2, all_edges)
    assert gcd(*[abs(value) for value in delta]) == 1

    rows = sp.Matrix([u_0, u_1, u_2, delta])
    assert rows.rank() == 4
    minor_edges = ((0, 1), (0, 2), (1, 2), (2, 4))
    minor_columns = [all_edges.index(edge) for edge in minor_edges]
    minor = rows[:, minor_columns]
    assert minor == sp.Matrix(
        [
            [1, -1, 0, 1],
            [-1, 0, 1, 0],
            [0, 1, 0, 0],
            [1, -1, 0, 0],
        ]
    )
    assert minor.det() == 1

    cycle_support = support(u_0, all_edges) | support(u_1, all_edges) | support(
        u_2, all_edges
    )
    assert support(delta, all_edges) & cycle_support == {
        (0, 1),
        (0, 2),
        (1, 3),
    }

    check_no_cancelling_subshore(zero_vertices, 0, table)
    check_no_cancelling_subshore(one_vertices, 1, table)

    a, b, c, q, h = sp.symbols("a b c q H")
    basis = sp.groebner(
        [1 + a + q, 1 + b, 1 + c, h * a * b * c - 1],
        a,
        b,
        c,
        q,
        h,
        order="lex",
    )
    h_only = [
        polynomial.as_expr()
        for polynomial in basis.polys
        if polynomial.as_expr().free_symbols <= {h}
    ]
    assert h_only == []
    substitution = {
        q: T,
        a: -(1 + T),
        b: -1,
        c: -1,
        h: -1 / (1 + T),
    }
    assert all(
        sp.cancel(polynomial.as_expr().subs(substitution)) == 0
        for polynomial in basis.polys
    )

    selected_holonomy = sp.cancel(
        matching_weight(g_0, table)
        * matching_weight(g_1, table)
        * matching_weight(g_2, table)
        / (
            matching_weight(f_0, table)
            * matching_weight(f_1, table)
            * matching_weight(f_2, table)
        )
    )
    assert selected_holonomy == -1 / (1 + T)

    eta = word("000001000011")
    eta_matching = canonical_matching(
        (0, 4), (1, 7), (2, 6), (3, 5), (8, 9), (10, 11)
    )
    assert matching_map(terms[eta]) == {
        eta_matching: (sp.Integer(1), False)
    }

    print("PASS complete 12-vertex table: 66 edges, local labels {0,1,2}")
    print("PASS complete matching census: 10395 matchings, 5128 nonempty fibres")
    print("PASS only active words form the selected shortest 3-cycle")
    print("PASS complete cycle fibres 3/2/2 with one diagonal extra")
    print("PASS pure targets are singleton coefficients 1")
    print("PASS diagonal fibre is a 2x1x1 shore product")
    print("PASS diagonal extra is one primitive alternating 6-cycle")
    print("PASS selected fibre lattices are direct and saturated of rank 4")
    print("PASS physical overlap occurs without lattice dependency")
    print("PASS selected-plus-pure holonomy elimination is zero")
    print("PASS outside singleton gives a complete-target Laurent unit")
    print("PASS global Krenn-Gu status remains UNRESOLVED")


if __name__ == "__main__":
    main()
