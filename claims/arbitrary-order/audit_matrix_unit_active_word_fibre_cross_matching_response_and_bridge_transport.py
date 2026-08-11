"""No-import audit of the active-word cross response and transport boundary."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product

Edge = tuple[int, int]
Table = dict[Edge, tuple[int, int, int]]
Word = tuple[int, ...]


@lru_cache(maxsize=None)
def full_matchings(mask: int) -> tuple[tuple[Edge, ...], ...]:
    """Enumerate perfect matchings by least-vertex removal."""
    if mask == 0:
        return ((),)
    if mask.bit_count() % 2:
        return ()
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    output: list[tuple[Edge, ...]] = []
    partners = rest
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        for tail in full_matchings(rest ^ partner_bit):
            output.append(((first, partner),) + tail)
        partners ^= partner_bit
    return tuple(output)


def term(table: Table, matching: tuple[Edge, ...], n: int):
    """Return word, weight, and exact cross-edge count."""
    word = [-1] * n
    weight = 1
    cross_count = 0
    for left, right in matching:
        left_label, right_label, scalar = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        weight *= scalar
        cross_count += left_label != right_label
    return tuple(word), weight, cross_count


def cross_ledger(table: Table, n: int) -> dict[Word, int]:
    """Sum the offdiagonal sector using complete matching enumeration."""
    output: dict[Word, int] = {}
    for matching in full_matchings((1 << n) - 1):
        word, weight, cross_count = term(table, matching, n)
        if cross_count:
            output[word] = output.get(word, 0) + weight
    return output


def pure_hafnian(table: Table, colour: int, mask: int) -> int:
    """Audit principal pure hafnians by explicit matching sums."""
    if mask.bit_count() % 2:
        return 0
    value = 0
    for matching in full_matchings(mask):
        scalar = 1
        for edge in matching:
            left_label, right_label, weight = table[edge]
            if left_label != colour or right_label != colour:
                scalar = 0
                break
            scalar *= weight
        value += scalar
    return value


def shores(word: Word) -> tuple[int, int, int]:
    """Encode colour shores as masks."""
    output = [0, 0, 0]
    for vertex, colour in enumerate(word):
        output[colour] |= 1 << vertex
    return tuple(output)


def partial_cross_matchings(
    cross_neighbors: tuple[tuple[tuple[int, int], ...], ...],
    mask: int,
):
    """Yield cross matchings by deciding whether each vertex stays residual."""
    if mask == 0:
        yield ()
        return
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    for tail in partial_cross_matchings(cross_neighbors, rest):
        yield tail
    for partner, _ in cross_neighbors[first]:
        partner_bit = 1 << partner
        if not rest & partner_bit:
            continue
        for tail in partial_cross_matchings(
            cross_neighbors, rest ^ partner_bit
        ):
            yield ((first, partner),) + tail


def response(table: Table, word: Word) -> tuple[int, list[tuple[tuple[Edge, ...], int]]]:
    """Reconstruct the cross response with a residual-vertex recursion."""
    n = len(word)
    neighbor_lists: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for (left, right), (left_label, right_label, weight) in table.items():
        if (
            left_label == word[left]
            and right_label == word[right]
            and left_label != right_label
        ):
            neighbor_lists[left].append((right, weight))
            neighbor_lists[right].append((left, weight))
    neighbors = tuple(tuple(row) for row in neighbor_lists)
    shore_masks = shores(word)
    terms: list[tuple[tuple[Edge, ...], int]] = []
    for matching in partial_cross_matchings(neighbors, (1 << n) - 1):
        if not matching:
            continue
        used = 0
        scalar = 1
        canonical = []
        for raw_left, raw_right in matching:
            edge = tuple(sorted((raw_left, raw_right)))
            used |= (1 << edge[0]) | (1 << edge[1])
            scalar *= table[edge][2]
            canonical.append(edge)
        value = scalar
        for colour, shore in enumerate(shore_masks):
            value *= pure_hafnian(table, colour, shore & ~used)
        terms.append((tuple(sorted(canonical)), value))
    if len({matching for matching, _ in terms}) != len(terms):
        raise AssertionError("partial cross matching counted twice")
    return sum(value for _, value in terms), terms


def alternate_table(n: int) -> Table:
    """Build a complete audit table distinct from the primary instances."""
    output: Table = {}
    for left, right in combinations(range(n), 2):
        left_label = (2 * left + right + 1) % 3
        right_label = (left + 2 * right + 2) % 3
        magnitude = 2 + (5 * left + 3 * right) % 7
        sign = -1 if (left + 2 * right) % 5 == 0 else 1
        output[(left, right)] = (left_label, right_label, sign * magnitude)
    return output


def audit_response_partition() -> dict[int, int]:
    """Compare independent partitions on bounded exact word sets."""
    output: dict[int, int] = {}
    for n in (4, 6, 8):
        table = alternate_table(n)
        ledger = cross_ledger(table, n)
        all_words = list(product(range(3), repeat=n))
        words = all_words if n < 8 else list(set(all_words[::37]) | set(ledger))
        for word in words:
            value, _ = response(table, word)
            assert value == ledger.get(word, 0)
        output[n] = len(words)
    return output


def active_table_from_factors() -> Table:
    """Rebuild the 111 active core from five one-factors."""
    factors = (
        ((0, 5), (1, 4), (2, 3)),
        ((1, 5), (0, 2), (3, 4)),
        ((2, 5), (1, 3), (0, 4)),
        ((3, 5), (2, 4), (0, 1)),
        ((4, 5), (0, 3), (1, 2)),
    )
    selected = (2, 1, 0, 0, 2, 1)
    table: Table = {}
    for colour, factor in enumerate(factors[:3]):
        for raw_edge in factor:
            table[tuple(sorted(raw_edge))] = (colour, colour, 1)
    for index, raw_edge in enumerate(factors[3]):
        left, right = sorted(raw_edge)
        table[(left, right)] = (
            selected[left],
            selected[right],
            -1 if index == 0 else 1,
        )
    for raw_edge in factors[4]:
        left, right = sorted(raw_edge)
        table[(left, right)] = (
            (selected[left] + 1) % 3,
            (selected[right] + 1) % 3,
            1,
        )
    return table


def audit_active_core() -> dict[str, object]:
    """Audit the normalized response and common-parity core."""
    table = active_table_from_factors()
    word = (2, 1, 0, 0, 2, 1)
    value, terms = response(table, word)
    nonzero = [(matching, term_value) for matching, term_value in terms if term_value]
    assert value == -1 and len(nonzero) == 1
    matching, term_value = nonzero[0]
    counts: Counter[tuple[int, int]] = Counter()
    for left, right in matching:
        counts[tuple(sorted((word[left], word[right])))] += 1
    assert [counts[(0, 1)], counts[(0, 2)], counts[(1, 2)]] == [1, 1, 1]
    denominator = 1
    for colour, shore in enumerate(shores(word)):
        denominator *= pure_hafnian(table, colour, shore)
    assert denominator == 1 and term_value / denominator == -1
    return {
        "response": value,
        "denominator": denominator,
        "nonzero_cores": len(nonzero),
        "counts": dict(sorted(counts.items())),
    }


def normalize_population(counts: tuple[int, int, int]) -> tuple[Counter[int], int, int]:
    """Audit colour populations under abstract square/hex replacements."""
    original: Counter[int] = Counter()
    for (left, right), count in zip(((0, 1), (0, 2), (1, 2)), counts, strict=True):
        original[left] += count
        original[right] += count
    odd = counts[0] % 2
    new: Counter[int] = Counter()
    if odd:
        new.update({0: 2, 1: 2, 2: 2})
    remaining = tuple(count - odd for count in counts)
    new[1] += remaining[0]
    new[0] += remaining[0]
    new[2] += remaining[1]
    new[0] += remaining[1]
    new[2] += remaining[2]
    new[1] += remaining[2]
    squares = sum(remaining) // 2
    return new, odd, squares


def audit_bridge_population() -> dict[str, int]:
    """Check parity, multiplicity preservation, and nontrivial transport."""
    cases = 0
    total_hex = 0
    total_squares = 0
    for counts in product(range(7), repeat=3):
        if counts == (0, 0, 0) or len({count % 2 for count in counts}) != 1:
            continue
        original: Counter[int] = Counter()
        for edge_type, count in zip(((0, 1), (0, 2), (1, 2)), counts, strict=True):
            original[edge_type[0]] += count
            original[edge_type[1]] += count
        new, hexagons, squares = normalize_population(counts)
        assert new == original
        assert 3 * hexagons + 2 * squares == sum(counts)
        cases += 1
        total_hex += hexagons
        total_squares += squares
    return {"cases": cases, "hexagons": total_hex, "squares": total_squares}


def hafnian_four(weights: tuple[int, int, int, int, int, int]) -> int:
    """Use edge order 01,02,03,12,13,23."""
    edge_01, edge_02, edge_03, edge_12, edge_13, edge_23 = weights
    return edge_01 * edge_23 + edge_02 * edge_13 + edge_03 * edge_12


def audit_pure_cancellation_and_cycle() -> dict[str, object]:
    """Check a supported zero hafnian and finite no-self-loop iteration."""
    weights = (2, 3, 0, 0, -2, 3)
    terms = (weights[0] * weights[5], weights[1] * weights[4])
    assert terms == (6, -6)
    assert hafnian_four(weights) == 0

    transition = {
        "001122": "010212",
        "010212": "102021",
        "102021": "001122",
    }
    current = "001122"
    seen: dict[str, int] = {}
    order = []
    while current not in seen:
        seen[current] = len(order)
        order.append(current)
        following = transition[current]
        assert following != current
        assert Counter(following) == Counter(current)
        current = following
    cycle = order[seen[current] :]
    assert len(cycle) == 3
    return {
        "pure_terms": terms,
        "pure_hafnian": hafnian_four(weights),
        "cycle_length": len(cycle),
    }


def main() -> None:
    partitions = audit_response_partition()
    active = audit_active_core()
    bridges = audit_bridge_population()
    exits = audit_pure_cancellation_and_cycle()
    print("matrix-unit active-word cross-response independent audit: PASS")
    print(f"  response partition word counts: {partitions}")
    print(f"  active ternary core: {active}")
    print(f"  bridge population ledger: {bridges}")
    print(f"  pure-cancellation/finite-cycle ledger: {exits}")


if __name__ == "__main__":
    main()
