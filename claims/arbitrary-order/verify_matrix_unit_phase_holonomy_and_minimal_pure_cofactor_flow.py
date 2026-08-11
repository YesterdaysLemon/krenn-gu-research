"""Primary exact checks for matrix-unit phase holonomy and cofactor flow."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Table = dict[Edge, tuple[int, int, Fraction]]


def perfect_matchings(vertices: tuple[int, ...], allowed: set[Edge] | None = None):
    """Generate perfect matchings, optionally inside a prescribed support."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        edge = (first, partner)
        if allowed is not None and edge not in allowed:
            continue
        residue = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(residue, allowed):
            yield (edge,) + tail


def matching_record(matching: Matching, table: Table, order: int):
    """Return induced word, exact scalar, and diagonal flag."""
    word = [-1] * order
    weight = Fraction(1)
    diagonal = True
    for left, right in matching:
        left_label, right_label, scalar = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        weight *= scalar
        diagonal = diagonal and left_label == right_label
    return tuple(word), weight, diagonal


def compatible_terms(table: Table, word: Word):
    """Enumerate the complete supported matching fibre of one word."""
    records = []
    for matching in perfect_matchings(tuple(range(len(word))), set(table)):
        induced, weight, diagonal = matching_record(matching, table, len(word))
        if induced == word:
            records.append((matching, weight, diagonal))
    return records


def transition_data():
    """Return a three-step binary bridge cycle on eight vertices."""
    words = (
        (0, 0, 0, 0, 1, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 0, 1),
    )
    cross = (
        ((2, 4), (3, 5)),
        ((1, 2), (5, 6)),
        ((1, 4), (3, 6)),
    )
    bridges = (
        ((2, 3), (4, 5)),
        ((1, 5), (2, 6)),
        ((4, 6), (1, 3)),
    )
    residual = (
        ((0, 1), (6, 7)),
        ((0, 4), (3, 7)),
        ((0, 2), (5, 7)),
    )
    return words, cross, bridges, residual


def sparse_holonomy_table() -> Table:
    """Build the exact sparse table realizing the three binomial fibres."""
    words, cross, bridges, residual = transition_data()
    table: Table = {}
    for index, old_word in enumerate(words):
        new_word = words[(index + 1) % len(words)]
        for position, edge in enumerate(cross[index]):
            left, right = edge
            labels = old_word[left], old_word[right]
            weight = Fraction(-1 if position == 0 else 1)
            assert labels[0] != labels[1]
            assert edge not in table
            table[edge] = *labels, weight
        for edge in bridges[index]:
            left, right = edge
            labels = new_word[left], new_word[right]
            assert labels[0] == labels[1]
            assert edge not in table
            table[edge] = *labels, Fraction(1)
        for edge in residual[index]:
            left, right = edge
            labels = old_word[left], old_word[right]
            assert labels[0] == labels[1]
            assert edge not in table
            table[edge] = *labels, Fraction(1)
    assert len(table) == 18
    return table


def matching_weight(matching: Matching, table: Table) -> Fraction:
    """Multiply the physical scalars on a matching."""
    result = Fraction(1)
    for edge in matching:
        result *= table[edge][2]
    return result


def power_of_two(exponent: int) -> Fraction:
    """Return an exact integral power of two."""
    if exponent >= 0:
        return Fraction(2**exponent)
    return Fraction(1, 2 ** (-exponent))


def word_character(word: Word, beta: dict[tuple[int, int], int]) -> Fraction:
    """Evaluate the positive diagonal character of a word."""
    exponent = sum(beta.get((vertex, colour), 0) for vertex, colour in enumerate(word))
    return power_of_two(exponent)


def scaled_table(table: Table, beta: dict[tuple[int, int], int]) -> Table:
    """Apply an exact positive diagonal coordinate scaling."""
    result = {}
    for (left, right), (left_label, right_label, weight) in table.items():
        exponent = beta.get((left, left_label), 0) + beta.get(
            (right, right_label), 0
        )
        result[(left, right)] = (
            left_label,
            right_label,
            weight * power_of_two(exponent),
        )
    return result


def laurent_value(exponents: Counter[Edge], table: Table) -> Fraction:
    """Evaluate a Laurent edge monomial exactly."""
    result = Fraction(1)
    for edge, exponent in exponents.items():
        result *= table[edge][2] ** exponent
    return result


def assert_binomial_holonomy_cycle() -> dict[str, object]:
    """Check the physical three-cycle, its circulation, and gauge invariance."""
    table = sparse_holonomy_table()
    words, cross, bridges, residual = transition_data()
    full_cross = tuple(tuple(sorted(cross[i] + residual[i])) for i in range(3))
    full_bridge = tuple(tuple(sorted(bridges[i] + residual[i])) for i in range(3))

    for index, word in enumerate(words):
        incoming = full_bridge[(index - 1) % 3]
        outgoing = full_cross[index]
        terms = compatible_terms(table, word)
        assert {record[0] for record in terms} == {incoming, outgoing}
        assert sorted((weight, diagonal) for _, weight, diagonal in terms) == [
            (Fraction(-1), False),
            (Fraction(1), True),
        ]
        assert sum(weight for _, weight, _ in terms) == 0

        next_word = words[(index + 1) % 3]
        assert matching_record(full_cross[index], table, 8)[0] == word
        assert matching_record(full_bridge[index], table, 8)[0] == next_word
        for edge in cross[index]:
            assert table[edge][0] != table[edge][1]
        for edge in bridges[index]:
            assert table[edge][0] == table[edge][1]

    circulation: Counter[Edge] = Counter(
        {
            edge: sum(edge in matching for matching in bridges)
            - sum(edge in matching for matching in cross)
            for edge in table
        }
    )
    circulation = Counter({edge: value for edge, value in circulation.items() if value})
    assert len(circulation) == 12
    assert set(circulation.values()) == {-1, 1}

    endpoint_character: Counter[tuple[int, int]] = Counter()
    for (left, right), exponent in circulation.items():
        left_label, right_label, _ = table[(left, right)]
        endpoint_character[(left, left_label)] += exponent
        endpoint_character[(right, right_label)] += exponent
    assert all(value == 0 for value in endpoint_character.values())

    holonomy = laurent_value(circulation, table)
    assert holonomy == -1 == (-1) ** len(words)
    assert all(
        matching_weight(full_cross[index], table)
        == -matching_weight(full_bridge[(index - 1) % 3], table)
        for index in range(3)
    )

    beta_rows = (
        (1, 0, 0),
        (-1, 1, 0),
        (2, -1, 0),
        (-2, 2, 0),
        (0, -2, 0),
        (0, 1, 0),
        (1, -1, 0),
        (-1, 0, 0),
    )
    assert tuple(sum(row[colour] for row in beta_rows) for colour in range(3)) == (
        0,
        0,
        0,
    )
    beta = {
        (vertex, colour): beta_rows[vertex][colour]
        for vertex in range(8)
        for colour in range(3)
    }
    gauged = scaled_table(table, beta)
    assert laurent_value(circulation, gauged) == holonomy
    for word in words:
        original = compatible_terms(table, word)
        transformed = compatible_terms(gauged, word)
        factor = word_character(word, beta)
        assert [record[0] for record in transformed] == [record[0] for record in original]
        assert [record[1] for record in transformed] == [
            factor * record[1] for record in original
        ]
        assert sum(record[1] for record in transformed) == 0

    return {
        "cycle_length": 3,
        "physical_edges": len(table),
        "terms_per_fibre": 2,
        "circulation_support": len(circulation),
        "holonomy": holonomy,
        "gauge_invariant": True,
    }


def hafnian(vertices: tuple[int, ...], weights: dict[Edge, Fraction]) -> Fraction:
    """Evaluate a scalar hafnian recursively."""
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    result = Fraction(0)
    for index in range(1, len(vertices)):
        partner = vertices[index]
        edge = tuple(sorted((first, partner)))
        residue = vertices[1:index] + vertices[index + 1 :]
        result += weights.get(edge, Fraction(0)) * hafnian(residue, weights)
    return result


def support_has_matching(vertices: tuple[int, ...], weights: dict[Edge, Fraction]) -> bool:
    """Decide whether the nonzero support on a vertex set has a perfect matching."""
    allowed = {edge for edge, value in weights.items() if value}
    return any(perfect_matchings(vertices, allowed))


def minimal_supported_cancellation(
    vertices: tuple[int, ...],
    weights: dict[Edge, Fraction],
) -> tuple[int, ...]:
    """Select a least-cardinality zero hafnian with a supported matching."""
    for size in range(2, len(vertices) + 1, 2):
        for subset in combinations(vertices, size):
            if support_has_matching(subset, weights) and hafnian(subset, weights) == 0:
                return subset
    raise AssertionError("no supported cancellation")


def cofactor_flow(
    vertices: tuple[int, ...],
    weights: dict[Edge, Fraction],
) -> dict[Edge, Fraction]:
    """Return C_ij=z_ij haf(Z[R-{i,j}]) on all nonzero active edges."""
    flow = {}
    for edge in combinations(vertices, 2):
        residue = tuple(vertex for vertex in vertices if vertex not in edge)
        value = weights.get(edge, Fraction(0)) * hafnian(residue, weights)
        if value:
            flow[edge] = value
    return flow


def row_sums(vertices: tuple[int, ...], flow: dict[Edge, Fraction]):
    """Return Euler cofactor-flow sums at every vertex."""
    result = {vertex: Fraction(0) for vertex in vertices}
    for (left, right), value in flow.items():
        result[left] += value
        result[right] += value
    return result


def degrees(vertices: tuple[int, ...], flow: dict[Edge, Fraction]):
    """Return active-flow degrees."""
    result = {vertex: 0 for vertex in vertices}
    for left, right in flow:
        result[left] += 1
        result[right] += 1
    return result


def scaled_weights(
    weights: dict[Edge, Fraction],
    vertex_scales: dict[int, Fraction],
) -> dict[Edge, Fraction]:
    """Apply z_ij -> t_i t_j z_ij."""
    return {
        edge: value * vertex_scales[edge[0]] * vertex_scales[edge[1]]
        for edge, value in weights.items()
    }


def assert_minimal_cofactor_flows() -> dict[str, object]:
    """Check the exact cycle and branching boundaries, including covariance."""
    vertices = (0, 1, 2, 3)
    cycle_weights = {
        (0, 1): Fraction(2),
        (0, 2): Fraction(3),
        (1, 3): Fraction(-2),
        (2, 3): Fraction(3),
    }
    assert hafnian(vertices, cycle_weights) == 0
    assert minimal_supported_cancellation(vertices, cycle_weights) == vertices
    cycle_flow = cofactor_flow(vertices, cycle_weights)
    assert cycle_flow == {
        (0, 1): Fraction(6),
        (0, 2): Fraction(-6),
        (1, 3): Fraction(-6),
        (2, 3): Fraction(6),
    }
    assert row_sums(vertices, cycle_flow) == {vertex: 0 for vertex in vertices}
    assert degrees(vertices, cycle_flow) == {vertex: 2 for vertex in vertices}

    scales = {0: Fraction(2), 1: Fraction(3), 2: Fraction(5), 3: Fraction(7)}
    gauged_cycle = scaled_weights(cycle_weights, scales)
    assert hafnian(vertices, gauged_cycle) == 0
    gauged_flow = cofactor_flow(vertices, gauged_cycle)
    common_factor = Fraction(2 * 3 * 5 * 7)
    assert gauged_flow == {
        edge: common_factor * value for edge, value in cycle_flow.items()
    }

    branch_weights = {
        (0, 1): Fraction(1),
        (2, 3): Fraction(1),
        (0, 2): Fraction(1),
        (1, 3): Fraction(1),
        (0, 3): Fraction(1),
        (1, 2): Fraction(-2),
    }
    assert hafnian(vertices, branch_weights) == 0
    assert minimal_supported_cancellation(vertices, branch_weights) == vertices
    branch_flow = cofactor_flow(vertices, branch_weights)
    assert row_sums(vertices, branch_flow) == {vertex: 0 for vertex in vertices}
    assert degrees(vertices, branch_flow) == {vertex: 3 for vertex in vertices}

    # A larger cancellation contains one of the same minimal four-shores.
    double_cycle = dict(cycle_weights)
    double_cycle.update(
        {
            (4, 5): Fraction(2),
            (4, 6): Fraction(3),
            (5, 7): Fraction(-2),
            (6, 7): Fraction(3),
        }
    )
    selected = minimal_supported_cancellation(tuple(range(8)), double_cycle)
    assert selected in {(0, 1, 2, 3), (4, 5, 6, 7)}

    return {
        "cycle_flow": tuple(sorted(cycle_flow.items())),
        "cycle_degrees": tuple(degrees(vertices, cycle_flow).values()),
        "branch_degrees": tuple(degrees(vertices, branch_flow).values()),
        "gauge_common_factor": common_factor,
        "larger_minimal_residual_size": len(selected),
    }


def main() -> None:
    holonomy = assert_binomial_holonomy_cycle()
    cofactor = assert_minimal_cofactor_flows()
    print("matrix-unit phase holonomy and pure-cofactor flow primary checks: PASS")
    print(f"  binomial active-word cycle: {holonomy}")
    print(f"  minimal supported cancellations: {cofactor}")


if __name__ == "__main__":
    main()
