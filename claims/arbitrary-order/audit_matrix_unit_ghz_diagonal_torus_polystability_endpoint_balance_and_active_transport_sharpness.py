"""Independent no-import audit of matrix-unit GHZ endpoint balance."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations

Edge = tuple[int, int]
CodeTable = dict[Edge, tuple[int, Fraction]]


def decode(code: int) -> tuple[int, int]:
    """Decode the two endpoint labels stored as one decimal digit pair."""
    return divmod(code, 10)


def sharp_table() -> CodeTable:
    """Build the audit table without importing the primary checker."""
    labels = {
        (0, 1): 0,
        (0, 2): 20,
        (0, 3): 0,
        (0, 4): 1,
        (0, 5): 11,
        (0, 6): 22,
        (0, 7): 10,
        (1, 2): 0,
        (1, 3): 22,
        (1, 4): 11,
        (1, 5): 12,
        (1, 6): 2,
        (1, 7): 21,
        (2, 3): 20,
        (2, 4): 0,
        (2, 5): 22,
        (2, 6): 11,
        (2, 7): 12,
        (3, 4): 10,
        (3, 5): 0,
        (3, 6): 21,
        (3, 7): 11,
        (4, 5): 0,
        (4, 6): 20,
        (4, 7): 22,
        (5, 6): 10,
        (5, 7): 0,
        (6, 7): 0,
    }
    weights = {edge: Fraction(1) for edge in labels}
    weights[(0, 4)] = Fraction(-1)
    weights[(0, 7)] = Fraction(-1, 2)
    weights[(6, 7)] = Fraction(1, 2)
    return {edge: (labels[edge], weights[edge]) for edge in labels}


def half_edge_census(table: CodeTable, order: int):
    """Count labels directly from the decimal code representation."""
    census = [[0, 0, 0] for _ in range(order)]
    for (left, right), (code, _) in table.items():
        left_label, right_label = decode(code)
        census[left][left_label] += 1
        census[right][right_label] += 1
    return tuple(tuple(row) for row in census)


def compatible_recursion(table: CodeTable, word: tuple[int, ...]):
    """Return exact diagonal/offdiagonal sums and counts by bitmask DP."""
    full_mask = (1 << len(word)) - 1

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[Fraction, Fraction, int, int]:
        if mask == 0:
            return Fraction(1), Fraction(0), 1, 0
        lowest = mask & -mask
        left = lowest.bit_length() - 1
        residue = mask ^ lowest
        diagonal_sum = Fraction(0)
        offdiagonal_sum = Fraction(0)
        diagonal_count = 0
        offdiagonal_count = 0
        choices = residue
        while choices:
            partner_bit = choices & -choices
            right = partner_bit.bit_length() - 1
            choices ^= partner_bit
            code, scalar = table[(left, right)]
            left_label, right_label = decode(code)
            if (left_label, right_label) != (word[left], word[right]):
                continue
            d_sum, o_sum, d_count, o_count = recurse(residue ^ partner_bit)
            if left_label == right_label:
                diagonal_sum += scalar * d_sum
                offdiagonal_sum += scalar * o_sum
                diagonal_count += d_count
                offdiagonal_count += o_count
            else:
                offdiagonal_sum += scalar * (d_sum + o_sum)
                offdiagonal_count += d_count + o_count
        return diagonal_sum, offdiagonal_sum, diagonal_count, offdiagonal_count

    return recurse(full_mask)


def total_perfect_matchings(order: int) -> int:
    """Return (order-1)!! without using the primary recursion."""
    result = 1
    for odd in range(1, order, 2):
        result *= odd
    return result


def edge_exponent(
    edge: Edge,
    code: int,
    beta: dict[tuple[int, int], int],
) -> int:
    """Evaluate one Laurent edge exponent."""
    left, right = edge
    left_label, right_label = decode(code)
    return beta.get((left, left_label), 0) + beta.get((right, right_label), 0)


def audit_laurent_duality(table: CodeTable) -> dict[str, object]:
    """Audit the balance pairing and a separate unstable support."""
    census = half_edge_census(table, 8)
    assert census == ((3, 2, 2),) * 8

    pairing_checks = 0
    for seed in range(9):
        beta: dict[tuple[int, int], int] = {}
        for colour in range(3):
            running = 0
            for vertex in range(7):
                value = ((seed + 2) * (vertex + 1) + colour) % 11 - 5
                beta[(vertex, colour)] = value
                running += value
            beta[(7, colour)] = -running
        sigmas = tuple(
            sum(beta[(vertex, colour)] for vertex in range(8))
            for colour in range(3)
        )
        assert sigmas == (0, 0, 0)
        edge_sum = sum(
            edge_exponent(edge, code, beta)
            for edge, (code, _) in table.items()
        )
        colour_sum = sum(load * sigma for load, sigma in zip((3, 2, 2), sigmas))
        assert edge_sum == colour_sum == 0
        pairing_checks += 1

    # Independent encoding of the earlier active-fibre support.
    old_codes = {
        (0, 1): 21,
        (0, 2): 11,
        (0, 3): 1,
        (0, 4): 22,
        (0, 5): 0,
        (1, 2): 21,
        (1, 3): 22,
        (1, 4): 0,
        (1, 5): 11,
        (2, 3): 0,
        (2, 4): 2,
        (2, 5): 22,
        (3, 4): 11,
        (3, 5): 1,
        (4, 5): 2,
    }
    erasing_beta = {(1, 0): -1, (4, 0): 1}
    sigmas = tuple(
        sum(erasing_beta.get((vertex, colour), 0) for vertex in range(6))
        for colour in range(3)
    )
    assert sigmas == (0, 0, 0)
    exponents = {
        edge: edge_exponent(edge, code, erasing_beta)
        for edge, code in old_codes.items()
    }
    assert all(value >= 0 for value in exponents.values())
    assert {edge: value for edge, value in exponents.items() if value} == {
        (4, 5): 1
    }
    return {
        "census": census[0],
        "pairing_checks": pairing_checks,
        "old_support_erased_edge": (4, 5),
    }


def audit_active_transport(table: CodeTable) -> dict[str, object]:
    """Audit pure targets, two active fibres, bridge labels, and failure."""
    pure = []
    for colour in range(3):
        diagonal, offdiagonal, diagonal_count, offdiagonal_count = compatible_recursion(
            table, (colour,) * 8
        )
        assert offdiagonal == 0
        assert offdiagonal_count == 0
        pure.append((diagonal, diagonal_count))
    assert pure == [(Fraction(1), 2), (Fraction(1), 1), (Fraction(1), 1)]

    chi_0 = (0, 1, 2, 0, 1, 2, 0, 0)
    chi_1 = (1, 2, 0, 2, 0, 1, 0, 0)
    records = {}
    for word in (chi_0, chi_1):
        diagonal, offdiagonal, diagonal_count, offdiagonal_count = compatible_recursion(
            table, word
        )
        assert (diagonal, offdiagonal) == (Fraction(1, 2), Fraction(-1, 2))
        assert (diagonal_count, offdiagonal_count) == (1, 1)
        records[word] = (diagonal, offdiagonal)

    expected_bridge_labels = {
        (0, 4): (0, 1),
        (1, 5): (1, 2),
        (2, 3): (2, 0),
        (2, 4): (0, 0),
        (0, 5): (1, 1),
        (1, 3): (2, 2),
    }
    for edge, labels in expected_bridge_labels.items():
        assert decode(table[edge][0]) == labels

    assert decode(table[(0, 7)][0]) == (1, 0)
    assert decode(table[(5, 6)][0]) == (1, 0)
    assert decode(table[(0, 5)][0]) != (0, 0)
    assert decode(table[(6, 7)][0]) != (1, 1)

    exposed = (0, 0, 0, 0, 0, 0, 2, 0)
    diagonal, offdiagonal, diagonal_count, offdiagonal_count = compatible_recursion(
        table, exposed
    )
    assert diagonal == 0
    assert offdiagonal == 1
    assert (diagonal_count, offdiagonal_count) == (0, 1)
    return {
        "pure_values_and_counts": pure,
        "active_fibres": records,
        "exposed_word": exposed,
        "perfect_matchings": total_perfect_matchings(8),
    }


def main() -> None:
    table = sharp_table()
    assert set(table) == set(combinations(range(8), 2))
    assert all(weight for _, weight in table.values())
    duality = audit_laurent_duality(table)
    transport = audit_active_transport(table)
    print("matrix-unit GHZ diagonal-torus balance independent audit: PASS")
    print(f"  Laurent incidence duality: {duality}")
    print(f"  bitmask active-transport audit: {transport}")


if __name__ == "__main__":
    main()
