"""Primary checks for the active-word cross response and bridge transport."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product

Edge = tuple[int, int]
Table = dict[Edge, tuple[int, int, int]]
Word = tuple[int, ...]


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate every labelled perfect matching recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def matching_word_weight_cross_count(
    matching: tuple[Edge, ...], table: Table, n: int
) -> tuple[Word, int, int]:
    """Evaluate one matching and count its offdiagonal units."""
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


def offdiagonal_ledger(table: Table, n: int) -> dict[Word, int]:
    """Sum all perfect matchings using at least one offdiagonal unit."""
    ledger: dict[Word, int] = {}
    for matching in perfect_matchings(tuple(range(n))):
        word, weight, cross_count = matching_word_weight_cross_count(
            matching, table, n
        )
        if cross_count:
            ledger[word] = ledger.get(word, 0) + weight
    return ledger


def pure_hafnian(table: Table, mask: int, colour: int) -> int:
    """Compute one principal pure-colour hafnian by exact recursion."""
    @lru_cache(maxsize=None)
    def recurse(remaining: int) -> int:
        if remaining == 0:
            return 1
        if remaining.bit_count() % 2:
            return 0
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        rest = remaining ^ first_bit
        value = 0
        partners = rest
        while partners:
            partner_bit = partners & -partners
            partner = partner_bit.bit_length() - 1
            left_label, right_label, weight = table[(first, partner)]
            if left_label == right_label == colour:
                value += weight * recurse(rest ^ partner_bit)
            partners ^= partner_bit
        return value

    return recurse(mask)


def word_shores(word: Word) -> tuple[int, int, int]:
    """Return the three word-shore bitmasks."""
    shores = [0, 0, 0]
    for vertex, colour in enumerate(word):
        shores[colour] |= 1 << vertex
    return tuple(shores)


def cross_response_terms(
    table: Table, word: Word
) -> dict[tuple[Edge, ...], int]:
    """Evaluate the exact cross-matching expansion independently."""
    shores = word_shores(word)
    cross_edges = [
        (left, right, weight)
        for (left, right), (left_label, right_label, weight) in table.items()
        if left_label == word[left]
        and right_label == word[right]
        and left_label != right_label
    ]
    terms: dict[tuple[Edge, ...], int] = {}

    def recurse(
        index: int,
        used: int,
        weight: int,
        selected: tuple[Edge, ...],
    ) -> None:
        if index == len(cross_edges):
            if not selected:
                return
            value = weight
            for colour, shore in enumerate(shores):
                value *= pure_hafnian(table, shore & ~used, colour)
            terms[selected] = value
            return
        left, right, scalar = cross_edges[index]
        recurse(index + 1, used, weight, selected)
        edge_mask = (1 << left) | (1 << right)
        if used & edge_mask:
            return
        recurse(
            index + 1,
            used | edge_mask,
            weight * scalar,
            selected + ((left, right),),
        )

    recurse(0, 0, 1, ())
    return terms


def deterministic_table(n: int, seed: int) -> Table:
    """Build a bounded complete exact table for response checks."""
    table: Table = {}
    for left, right in combinations(range(n), 2):
        left_label = (left + 2 * right + seed) % 3
        right_label = (2 * left + right + seed + 1) % 3
        magnitude = 1 + ((left + 2) * (right + 1) + seed) % 5
        sign = -1 if (left + right + seed) % 4 == 0 else 1
        table[(left, right)] = (left_label, right_label, sign * magnitude)
    return table


def assert_cross_response() -> dict[int, int]:
    """Check Q_chi against the cross-set partition on bounded word sets."""
    ledger: dict[int, int] = {}
    for n, seed in ((6, 4), (8, 7)):
        table = deterministic_table(n, seed)
        offdiagonal = offdiagonal_ledger(table, n)
        words = list(product(range(3), repeat=n))
        if n == 8:
            selected_words = set(words[::31]) | set(offdiagonal)
        else:
            selected_words = set(words)
        for word in selected_words:
            response = sum(cross_response_terms(table, word).values())
            assert response == offdiagonal.get(word, 0)
        ledger[n] = len(selected_words)
    return ledger


def active_table() -> Table:
    """Return the active ternary-core table from the preceding theorem."""
    return {
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


def cross_type_counts(table: Table, word: Word, edges: tuple[Edge, ...]):
    """Count the three unordered cross types."""
    counts: Counter[tuple[int, int]] = Counter()
    for edge in edges:
        left, right = edge
        colours = tuple(sorted((word[left], word[right])))
        assert colours[0] != colours[1]
        counts[colours] += 1
    return counts


def assert_active_core() -> dict[str, object]:
    """Check the cofactor-active 111 core and normalized equation."""
    table = active_table()
    word = (2, 1, 0, 0, 2, 1)
    shores = word_shores(word)
    denominator = 1
    for colour, shore in enumerate(shores):
        denominator *= pure_hafnian(table, shore, colour)
    assert denominator == 1
    terms = cross_response_terms(table, word)
    nonzero = {edges: value for edges, value in terms.items() if value}
    assert len(nonzero) == 1
    edges, value = next(iter(nonzero.items()))
    assert value == -1
    counts = cross_type_counts(table, word, edges)
    assert counts == Counter({(0, 1): 1, (0, 2): 1, (1, 2): 1})
    assert value / denominator == -1
    return {
        "denominator": denominator,
        "active_term": value,
        "cross_counts": dict(sorted(counts.items())),
    }


Endpoint = tuple[str, int]


def normalize_cross_counts(
    counts: tuple[int, int, int]
) -> tuple[list[tuple[Endpoint, Endpoint, int]], dict[Endpoint, int]]:
    """Apply the square/hexagon convention to abstract disjoint endpoints."""
    types = ((0, 1), (0, 2), (1, 2))
    buckets: dict[tuple[int, int], list[tuple[Endpoint, Endpoint]]] = {}
    original_colours: dict[Endpoint, int] = {}
    for edge_type, count in zip(types, counts, strict=True):
        edges = []
        for index in range(count):
            left = (f"{edge_type[0]}{edge_type[1]}_{index}_L", edge_type[0])
            right = (f"{edge_type[0]}{edge_type[1]}_{index}_R", edge_type[1])
            original_colours[left] = edge_type[0]
            original_colours[right] = edge_type[1]
            edges.append((left, right))
        buckets[edge_type] = edges

    bridges: list[tuple[Endpoint, Endpoint, int]] = []
    if counts[0] % 2:
        edge_01 = buckets[(0, 1)].pop()
        edge_02 = buckets[(0, 2)].pop()
        edge_12 = buckets[(1, 2)].pop()
        bridges.extend(
            [
                (edge_01[1], edge_02[1], 0),
                (edge_01[0], edge_12[1], 1),
                (edge_02[0], edge_12[0], 2),
            ]
        )

    for (left_colour, right_colour), edges in buckets.items():
        assert len(edges) % 2 == 0
        for first, second in zip(edges[::2], edges[1::2], strict=True):
            bridges.append((first[0], second[0], right_colour))
            bridges.append((first[1], second[1], left_colour))
    return bridges, original_colours


def assert_bridge_normalization() -> dict[str, int]:
    """Exhaust small parity-valid cross-count triples."""
    cases = 0
    hexagons = 0
    squares = 0
    for counts in product(range(6), repeat=3):
        if counts == (0, 0, 0) or len({count % 2 for count in counts}) != 1:
            continue
        bridges, original = normalize_cross_counts(counts)
        endpoints = [endpoint for edge in bridges for endpoint in edge[:2]]
        assert len(endpoints) == sum(counts) * 2
        assert len(set(endpoints)) == len(endpoints)
        new_colours = {
            endpoint: colour
            for left, right, colour in bridges
            for endpoint in (left, right)
        }
        assert set(new_colours) == set(original)
        assert all(new_colours[endpoint] != colour for endpoint, colour in original.items())
        assert Counter(new_colours.values()) == Counter(original.values())
        cases += 1
        hexagons += counts[0] % 2
        squares += (sum(counts) - 3 * (counts[0] % 2)) // 2
    return {"cases": cases, "hexagons": hexagons, "squares": squares}


def hafnian_four(weights: dict[Edge, int]) -> int:
    """Evaluate a four-vertex pure shore."""
    return (
        weights.get((0, 1), 0) * weights.get((2, 3), 0)
        + weights.get((0, 2), 0) * weights.get((1, 3), 0)
        + weights.get((0, 3), 0) * weights.get((1, 2), 0)
    )


def assert_transport_or_pure_cancellation() -> dict[str, int]:
    """Check exact nonzero-transport and zero-sum pure-shore exits."""
    transported = {(0, 1): 2, (2, 3): 3}
    assert hafnian_four(transported) == 6

    cancelling = {
        (0, 1): 1,
        (2, 3): 1,
        (0, 2): 1,
        (1, 3): -1,
    }
    assert hafnian_four(cancelling) == 0
    matching_terms = [
        cancelling[(0, 1)] * cancelling[(2, 3)],
        cancelling[(0, 2)] * cancelling[(1, 3)],
    ]
    assert matching_terms == [1, -1]
    return {
        "transported_hafnian": hafnian_four(transported),
        "cancelled_hafnian": hafnian_four(cancelling),
        "cancel_terms": len(matching_terms),
    }


def main() -> None:
    response = assert_cross_response()
    active = assert_active_core()
    normalization = assert_bridge_normalization()
    exits = assert_transport_or_pure_cancellation()
    print("matrix-unit active-word cross-response primary checks: PASS")
    print(f"  response word counts: {response}")
    print(f"  cofactor-active ternary core: {active}")
    print(f"  square/hex normalization ledger: {normalization}")
    print(f"  transport/pure-cancellation exits: {exits}")


if __name__ == "__main__":
    main()
