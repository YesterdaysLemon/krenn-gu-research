"""Primary exact checks for matrix-unit GHZ endpoint balance."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Unit = tuple[int, int, Fraction]
Table = dict[Edge, Unit]


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate labelled perfect matchings recursively."""
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
    order: int,
) -> tuple[Word, Fraction, bool]:
    """Return the word, scalar weight, and diagonal flag of a matching."""
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


def coefficient_ledgers(
    table: Table,
    order: int,
) -> tuple[
    dict[Word, Fraction],
    dict[Word, Fraction],
    dict[Word, Fraction],
    dict[Word, list[tuple[Matching, Fraction, bool]]],
]:
    """Enumerate total, diagonal, offdiagonal, and term ledgers."""
    total: dict[Word, Fraction] = {}
    diagonal: dict[Word, Fraction] = {}
    offdiagonal: dict[Word, Fraction] = {}
    terms: dict[Word, list[tuple[Matching, Fraction, bool]]] = {}
    for matching in perfect_matchings(tuple(range(order))):
        word, weight, is_diagonal = matching_record(matching, table, order)
        total[word] = total.get(word, Fraction(0)) + weight
        target = diagonal if is_diagonal else offdiagonal
        target[word] = target.get(word, Fraction(0)) + weight
        terms.setdefault(word, []).append((matching, weight, is_diagonal))
    return total, diagonal, offdiagonal, terms


def endpoint_loads(
    table: Table,
    multiplicities: dict[Edge, int],
    order: int,
) -> tuple[tuple[int, int, int], ...]:
    """Count auxiliary labelled half-edge multiplicities at each vertex."""
    loads = [[0, 0, 0] for _ in range(order)]
    for (left, right), (left_label, right_label, _) in table.items():
        multiplicity = multiplicities[(left, right)]
        loads[left][left_label] += multiplicity
        loads[right][right_label] += multiplicity
    return tuple(tuple(row) for row in loads)


def colour_sums(beta: dict[tuple[int, int], int], order: int):
    """Return the three GHZ character sums of an exponent assignment."""
    return tuple(sum(beta.get((vertex, colour), 0) for vertex in range(order)) for colour in range(3))


def edge_exponents(
    table: Table,
    beta: dict[tuple[int, int], int],
) -> dict[Edge, int]:
    """Return endpoint-summed Laurent exponents on every physical edge."""
    result: dict[Edge, int] = {}
    for edge, (left_label, right_label, _) in table.items():
        left, right = edge
        result[edge] = beta.get((left, left_label), 0) + beta.get(
            (right, right_label), 0
        )
    return result


def assert_dual_pairing_identity(
    table: Table,
    multiplicities: dict[Edge, int],
    common_loads: tuple[int, int, int],
    order: int,
) -> int:
    """Check sum m_e r_e(beta)=sum q_c sigma_c(beta) exactly."""
    probes: list[dict[tuple[int, int], int]] = []
    for seed in range(1, 8):
        beta: dict[tuple[int, int], int] = {}
        for colour in range(3):
            subtotal = 0
            for vertex in range(order - 1):
                value = ((vertex + 2) * (colour + seed + 1)) % 7 - 3
                beta[(vertex, colour)] = value
                subtotal += value
            beta[(order - 1, colour)] = -subtotal
        probes.append(beta)

    for beta in probes:
        exponents = edge_exponents(table, beta)
        left = sum(multiplicities[edge] * value for edge, value in exponents.items())
        sigmas = colour_sums(beta, order)
        right = sum(common_loads[colour] * sigmas[colour] for colour in range(3))
        assert sigmas == (0, 0, 0)
        assert left == right == 0
    return len(probes)


def earlier_active_table() -> Table:
    """Return the earlier six-vertex active-fibre sharpness support."""
    raw = {
        (0, 1): (2, 1, 1),
        (0, 2): (1, 1, 1),
        (0, 3): (0, 1, 1),
        (0, 4): (2, 2, 1),
        (0, 5): (0, 0, 1),
        (1, 2): (2, 1, 1),
        (1, 3): (2, 2, 1),
        (1, 4): (0, 0, 1),
        (1, 5): (1, 1, 1),
        (2, 3): (0, 0, 1),
        (2, 4): (0, 2, 1),
        (2, 5): (2, 2, 1),
        (3, 4): (1, 1, 1),
        (3, 5): (0, 1, -1),
        (4, 5): (0, 2, 1),
    }
    return {
        edge: (left_label, right_label, Fraction(weight))
        for edge, (left_label, right_label, weight) in raw.items()
    }


def assert_explicit_erasing_direction() -> dict[str, object]:
    """Check a strict support-erasing direction on the earlier table."""
    table = earlier_active_table()
    beta = {(1, 0): -1, (4, 0): 1}
    assert colour_sums(beta, 6) == (0, 0, 0)
    exponents = edge_exponents(table, beta)
    assert min(exponents.values()) == 0
    positive = {edge: value for edge, value in exponents.items() if value > 0}
    assert positive == {(4, 5): 1}
    return {"beta": beta, "positive_edge_exponents": positive}


def balanced_transport_table() -> Table:
    """Return the complete eight-vertex balanced active-transport table."""
    raw: dict[Edge, tuple[int, int, int | Fraction]] = {
        (0, 1): (0, 0, 1),
        (0, 2): (2, 0, 1),
        (0, 3): (0, 0, 1),
        (0, 4): (0, 1, -1),
        (0, 5): (1, 1, 1),
        (0, 6): (2, 2, 1),
        (0, 7): (1, 0, Fraction(-1, 2)),
        (1, 2): (0, 0, 1),
        (1, 3): (2, 2, 1),
        (1, 4): (1, 1, 1),
        (1, 5): (1, 2, 1),
        (1, 6): (0, 2, 1),
        (1, 7): (2, 1, 1),
        (2, 3): (2, 0, 1),
        (2, 4): (0, 0, 1),
        (2, 5): (2, 2, 1),
        (2, 6): (1, 1, 1),
        (2, 7): (1, 2, 1),
        (3, 4): (1, 0, 1),
        (3, 5): (0, 0, 1),
        (3, 6): (2, 1, 1),
        (3, 7): (1, 1, 1),
        (4, 5): (0, 0, 1),
        (4, 6): (2, 0, 1),
        (4, 7): (2, 2, 1),
        (5, 6): (1, 0, 1),
        (5, 7): (0, 0, 1),
        (6, 7): (0, 0, Fraction(1, 2)),
    }
    return {
        edge: (left_label, right_label, Fraction(weight))
        for edge, (left_label, right_label, weight) in raw.items()
    }


def term_signature(
    records: list[tuple[Matching, Fraction, bool]],
) -> set[tuple[Matching, Fraction, bool]]:
    """Return an order-insensitive exact term signature."""
    return set(records)


def assert_balanced_transport_sharpness() -> dict[str, object]:
    """Replay balance, pure targets, transport, and explicit nonwitness."""
    table = balanced_transport_table()
    order = 8
    assert set(table) == set(combinations(range(order), 2))
    assert all(weight for _, _, weight in table.values())

    multiplicities = {edge: 1 for edge in table}
    loads = endpoint_loads(table, multiplicities, order)
    assert loads == ((3, 2, 2),) * order
    dual_probes = assert_dual_pairing_identity(
        table, multiplicities, (3, 2, 2), order
    )

    total, diagonal, offdiagonal, terms = coefficient_ledgers(table, order)
    assert sum(len(records) for records in terms.values()) == 105
    pure_values = tuple(total[(colour,) * order] for colour in range(3))
    assert pure_values == (Fraction(1), Fraction(1), Fraction(1))

    chi_0 = (0, 1, 2, 0, 1, 2, 0, 0)
    chi_1 = (1, 2, 0, 2, 0, 1, 0, 0)
    p_matching = ((0, 3), (1, 4), (2, 5), (6, 7))
    f_matching = ((0, 4), (1, 5), (2, 3), (6, 7))
    b_matching = ((0, 5), (1, 3), (2, 4), (6, 7))
    f_prime = ((0, 7), (1, 3), (2, 4), (5, 6))

    assert total[chi_0] == 0
    assert diagonal[chi_0] == Fraction(1, 2)
    assert offdiagonal[chi_0] == Fraction(-1, 2)
    assert term_signature(terms[chi_0]) == {
        (p_matching, Fraction(1, 2), True),
        (f_matching, Fraction(-1, 2), False),
    }

    assert total[chi_1] == 0
    assert diagonal[chi_1] == Fraction(1, 2)
    assert offdiagonal[chi_1] == Fraction(-1, 2)
    assert term_signature(terms[chi_1]) == {
        (b_matching, Fraction(1, 2), True),
        (f_prime, Fraction(-1, 2), False),
    }

    # One edge of each cross type, and the exact forced ternary bridges.
    assert table[(0, 4)][:2] == (0, 1)
    assert table[(1, 5)][:2] == (1, 2)
    assert table[(2, 3)][:2] == (2, 0)
    assert table[(2, 4)][:2] == (0, 0)
    assert table[(0, 5)][:2] == (1, 1)
    assert table[(1, 3)][:2] == (2, 2)

    # The next binary core enters the deeper alternative.
    assert table[(0, 7)][:2] == (1, 0)
    assert table[(5, 6)][:2] == (1, 0)
    assert table[(0, 5)][:2] == (1, 1)  # would need (0,0)
    assert table[(6, 7)][:2] == (0, 0)  # would need (1,1)

    exposed = (0, 0, 0, 0, 0, 0, 2, 0)
    exposed_matching = ((0, 3), (1, 6), (2, 4), (5, 7))
    assert total[exposed] == 1
    assert terms[exposed] == [(exposed_matching, Fraction(1), False)]

    return {
        "endpoint_loads": loads[0],
        "dual_identity_probes": dual_probes,
        "pure_coefficients": pure_values,
        "active_fibres": {
            chi_0: (diagonal[chi_0], offdiagonal[chi_0]),
            chi_1: (diagonal[chi_1], offdiagonal[chi_1]),
        },
        "exposed_mixed_word": exposed,
        "perfect_matchings": 105,
    }


def main() -> None:
    erasing = assert_explicit_erasing_direction()
    sharpness = assert_balanced_transport_sharpness()
    print("matrix-unit GHZ diagonal-torus balance primary checks: PASS")
    print(f"  earlier active-support erasing direction: {erasing}")
    print(f"  balanced active-transport sharpness: {sharpness}")


if __name__ == "__main__":
    main()
