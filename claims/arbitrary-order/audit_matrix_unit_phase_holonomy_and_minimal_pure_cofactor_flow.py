"""Independent no-import audit of phase holonomy and pure-cofactor flow."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache

Edge = tuple[int, int]
CodeTable = dict[Edge, tuple[int, Fraction]]


def decode(code: int) -> tuple[int, int]:
    """Decode an ordered endpoint-label pair."""
    return divmod(code, 10)


def audit_table() -> CodeTable:
    """Encode the sparse three-cycle independently with decimal labels."""
    raw = {
        (0, 1): (0, 1),
        (0, 2): (0, 1),
        (0, 4): (0, 1),
        (1, 2): (1, -1),
        (1, 3): (0, 1),
        (1, 4): (10, -1),
        (1, 5): (11, 1),
        (2, 3): (11, 1),
        (2, 4): (1, -1),
        (2, 6): (0, 1),
        (3, 5): (1, 1),
        (3, 6): (10, 1),
        (3, 7): (11, 1),
        (4, 5): (0, 1),
        (4, 6): (11, 1),
        (5, 6): (1, 1),
        (5, 7): (11, 1),
        (6, 7): (11, 1),
    }
    return {edge: (code, Fraction(weight)) for edge, (code, weight) in raw.items()}


def compatible_bitmask(table: CodeTable, word: tuple[int, ...]):
    """Return the complete compatible fibre by least-set-bit recursion."""
    full_mask = (1 << len(word)) - 1

    @lru_cache(maxsize=None)
    def recurse(mask: int):
        if mask == 0:
            return (((), Fraction(1), True),)
        first_bit = mask & -mask
        left = first_bit.bit_length() - 1
        residue = mask ^ first_bit
        records = []
        choices = residue
        while choices:
            partner_bit = choices & -choices
            right = partner_bit.bit_length() - 1
            choices ^= partner_bit
            edge = (left, right)
            if edge not in table:
                continue
            code, scalar = table[edge]
            left_label, right_label = decode(code)
            if (left_label, right_label) != (word[left], word[right]):
                continue
            for tail, tail_weight, tail_diagonal in recurse(residue ^ partner_bit):
                records.append(
                    (
                        (edge,) + tail,
                        scalar * tail_weight,
                        tail_diagonal and left_label == right_label,
                    )
                )
        return tuple(records)

    return recurse(full_mask)


def audit_holonomy() -> dict[str, object]:
    """Audit the binomial fibres and the nonzero invariant circulation."""
    table = audit_table()
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
    bridge = (
        ((2, 3), (4, 5)),
        ((1, 5), (2, 6)),
        ((4, 6), (1, 3)),
    )
    for word in words:
        records = compatible_bitmask(table, word)
        assert len(records) == 2
        assert sorted((weight, diagonal) for _, weight, diagonal in records) == [
            (Fraction(-1), False),
            (Fraction(1), True),
        ]
        assert sum(weight for _, weight, _ in records) == 0

    circulation = Counter()
    for matching in bridge:
        circulation.update(matching)
    for matching in cross:
        circulation.subtract(matching)
    assert len(circulation) == 12
    assert set(circulation.values()) == {-1, 1}

    character = Counter()
    numerator = Fraction(1)
    denominator = Fraction(1)
    for edge, exponent in circulation.items():
        code, weight = table[edge]
        left_label, right_label = decode(code)
        character[(edge[0], left_label)] += exponent
        character[(edge[1], right_label)] += exponent
        if exponent > 0:
            numerator *= weight**exponent
            assert left_label == right_label
        else:
            denominator *= weight ** (-exponent)
            assert left_label != right_label
    assert all(value == 0 for value in character.values())
    assert numerator / denominator == -1
    return {
        "fibre_counts": (2, 2, 2),
        "circulation_edges": len(circulation),
        "endpoint_character_zero": True,
        "odd_holonomy": numerator / denominator,
    }


def hafnian_mask(weights: dict[Edge, int], order: int, mask: int | None = None) -> int:
    """Evaluate a scalar hafnian by a cached bitmask recurrence."""
    if mask is None:
        mask = (1 << order) - 1

    @lru_cache(maxsize=None)
    def recurse(active: int) -> int:
        if active == 0:
            return 1
        first_bit = active & -active
        left = first_bit.bit_length() - 1
        residue = active ^ first_bit
        total = 0
        choices = residue
        while choices:
            partner_bit = choices & -choices
            right = partner_bit.bit_length() - 1
            choices ^= partner_bit
            total += weights.get((left, right), 0) * recurse(residue ^ partner_bit)
        return total

    return recurse(mask)


def direct_flow(weights: dict[Edge, int], order: int) -> dict[Edge, int]:
    """Compute edge times the complementary hafnian from bit masks."""
    full_mask = (1 << order) - 1
    result = {}
    for edge, weight in weights.items():
        residue = full_mask ^ (1 << edge[0]) ^ (1 << edge[1])
        value = weight * hafnian_mask(weights, order, residue)
        if value:
            result[edge] = value
    return result


def audit_cofactor_flows() -> dict[str, object]:
    """Audit an alternating cycle and a three-term branching polygon."""
    cycle = {(0, 1): 5, (0, 2): 7, (1, 3): -5, (2, 3): 7}
    assert hafnian_mask(cycle, 4) == 0
    cycle_flow = direct_flow(cycle, 4)
    assert cycle_flow == {(0, 1): 35, (0, 2): -35, (1, 3): -35, (2, 3): 35}

    branch = {
        (0, 1): 2,
        (2, 3): 3,
        (0, 2): 1,
        (1, 3): 5,
        (0, 3): 1,
        (1, 2): -11,
    }
    assert hafnian_mask(branch, 4) == 2 * 3 + 1 * 5 - 11 == 0
    branch_flow = direct_flow(branch, 4)

    summaries = []
    for flow, expected_degree in ((cycle_flow, 2), (branch_flow, 3)):
        row_sum = [0] * 4
        degree = [0] * 4
        for (left, right), value in flow.items():
            row_sum[left] += value
            row_sum[right] += value
            degree[left] += 1
            degree[right] += 1
        assert row_sum == [0] * 4
        assert degree == [expected_degree] * 4
        summaries.append((tuple(row_sum), tuple(degree)))

    # Every supported two-vertex residual has its single nonzero edge as hafnian.
    for weights in (cycle, branch):
        for edge, value in weights.items():
            assert value
            assert hafnian_mask(weights, 4, (1 << edge[0]) | (1 << edge[1])) == value
    return {
        "cycle_flow": tuple(sorted(cycle_flow.items())),
        "branch_flow": tuple(sorted(branch_flow.items())),
        "row_and_degree_summaries": tuple(summaries),
    }


def main() -> None:
    holonomy = audit_holonomy()
    cofactors = audit_cofactor_flows()
    print("matrix-unit phase holonomy and pure-cofactor flow independent audit: PASS")
    print(f"  decimal-code bitmask holonomy: {holonomy}")
    print(f"  alternate exact cofactor flows: {cofactors}")


if __name__ == "__main__":
    main()
