"""No-import bitmask audit of active word-shore synchronization."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product

Edge = tuple[int, int]
Table = dict[Edge, tuple[int, int, int]]
Word = tuple[int, ...]


@lru_cache(maxsize=None)
def matching_edge_sets(mask: int) -> tuple[tuple[Edge, ...], ...]:
    """Enumerate perfect matchings by least-set-bit removal."""
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
        residue = rest ^ partner_bit
        for tail in matching_edge_sets(residue):
            output.append(((first, partner),) + tail)
        partners ^= partner_bit
    return tuple(output)


def term(table: Table, matching: tuple[Edge, ...], n: int):
    """Evaluate one matching with the audit's direct endpoint convention."""
    labels = [-1] * n
    scalar = 1
    pure = True
    for left, right in matching:
        left_label, right_label, weight = table[(left, right)]
        labels[left] = left_label
        labels[right] = right_label
        scalar *= weight
        pure = pure and left_label == right_label
    return tuple(labels), scalar, pure


def ledgers(table: Table, n: int):
    """Return separate total, pure-edge, cross-edge, and term ledgers."""
    total: dict[Word, int] = {}
    pure: dict[Word, int] = {}
    cross: dict[Word, int] = {}
    details: dict[Word, list[tuple[tuple[Edge, ...], int, bool]]] = {}
    for matching in matching_edge_sets((1 << n) - 1):
        word, scalar, is_pure = term(table, matching, n)
        total[word] = total.get(word, 0) + scalar
        bucket = pure if is_pure else cross
        bucket[word] = bucket.get(word, 0) + scalar
        details.setdefault(word, []).append((matching, scalar, is_pure))
    return total, pure, cross, details


def pure_hafnian(table: Table, mask: int, colour: int) -> int:
    """Compute a principal pure-colour hafnian with a separate bitmask DP."""
    @lru_cache(maxsize=None)
    def recurse(remaining: int) -> int:
        if remaining == 0:
            return 1
        if remaining.bit_count() % 2:
            return 0
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        others = remaining ^ first_bit
        value = 0
        partners = others
        while partners:
            partner_bit = partners & -partners
            partner = partner_bit.bit_length() - 1
            labels = table[(first, partner)]
            if labels[0] == labels[1] == colour:
                value += labels[2] * recurse(others ^ partner_bit)
            partners ^= partner_bit
        return value

    return recurse(mask)


def shore_masks(word: Word) -> tuple[int, int, int]:
    """Encode the three word shores."""
    masks = [0, 0, 0]
    for vertex, colour in enumerate(word):
        masks[colour] |= 1 << vertex
    return tuple(masks)


def shore_hafnian_product(table: Table, word: Word) -> int:
    """Multiply the three principal pure hafnians."""
    value = 1
    for colour, mask in enumerate(shore_masks(word)):
        value *= pure_hafnian(table, mask, colour)
    return value


def alternate_table(n: int) -> Table:
    """Build audit-only complete tables distinct from the primary family."""
    table: Table = {}
    for left, right in combinations(range(n), 2):
        left_label = (2 * left + right + 2) % 3
        right_label = (left + 2 * right) % 3
        magnitude = 2 + (3 * left + 5 * right) % 7
        sign = -1 if (left * right + right) % 4 == 0 else 1
        table[(left, right)] = (left_label, right_label, sign * magnitude)
    return table


def audit_factorization() -> dict[int, int]:
    """Audit all words at three bounded orders with independent arithmetic."""
    output: dict[int, int] = {}
    for n in (4, 6, 8):
        table = alternate_table(n)
        _, pure, _, _ = ledgers(table, n)
        count = 0
        for word in product(range(3), repeat=n):
            assert pure.get(word, 0) == shore_hafnian_product(table, word)
            count += 1
        output[n] = count
    return output


def factorization_table() -> Table:
    """Reconstruct the active example from a one-factorization of K6."""
    factors = (
        ((0, 5), (1, 4), (2, 3)),
        ((1, 5), (0, 2), (3, 4)),
        ((2, 5), (1, 3), (0, 4)),
        ((3, 5), (2, 4), (0, 1)),
        ((4, 5), (0, 3), (1, 2)),
    )
    table: Table = {}
    for colour, factor in enumerate(factors[:3]):
        for raw_edge in factor:
            edge = tuple(sorted(raw_edge))
            table[edge] = (colour, colour, 1)

    selected = (2, 1, 0, 0, 2, 1)
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
    assert len(table) == 15
    return table


def odd_component_count(table: Table, mask: int, colour: int) -> int:
    """Count odd components in one induced pure support graph."""
    unseen = mask
    odd = 0
    while unseen:
        start_bit = unseen & -unseen
        frontier = start_bit
        component = 0
        unseen ^= start_bit
        while frontier:
            vertex_bit = frontier & -frontier
            frontier ^= vertex_bit
            vertex = vertex_bit.bit_length() - 1
            component |= vertex_bit
            candidates = unseen
            while candidates:
                other_bit = candidates & -candidates
                candidates ^= other_bit
                other = other_bit.bit_length() - 1
                edge = tuple(sorted((vertex, other)))
                left_label, right_label, _ = table[edge]
                if left_label == right_label == colour:
                    unseen ^= other_bit
                    frontier |= other_bit
        odd += component.bit_count() % 2
    return odd


def satisfies_tutte(table: Table, mask: int, colour: int) -> bool:
    """Check every Tutte separator in one bounded shore."""
    subset = mask
    while True:
        residue = mask ^ subset
        if odd_component_count(table, residue, colour) > subset.bit_count():
            return False
        if subset == 0:
            return True
        subset = (subset - 1) & mask


def audit_active_fibre() -> dict[str, object]:
    """Audit D=-Q, nonzero shores, and Tutte on the active word."""
    table = factorization_table()
    total, pure, cross, details = ledgers(table, 6)
    word = (2, 1, 0, 0, 2, 1)
    masks = shore_masks(word)
    shore_values = [pure_hafnian(table, mask, colour) for colour, mask in enumerate(masks)]
    assert shore_values == [1, 1, 1]
    assert all(satisfies_tutte(table, mask, colour) for colour, mask in enumerate(masks))
    assert pure[word] == shore_hafnian_product(table, word) == 1
    assert cross[word] == -1
    assert total[word] == 0
    assert len(details[word]) == 2
    exposed = (0, 0, 2, 1, 0, 2)
    assert total[exposed] == 1 and len(details[exposed]) == 1
    return {
        "D": pure[word],
        "Q": cross[word],
        "shore_values": shore_values,
        "tutte": True,
        "nonwitness_word": exposed,
    }


def zero_fibre_table() -> Table:
    """Construct the unsynchronized binary-square table independently."""
    table: Table = {
        (2, 3): (0, 0, 1),
        (0, 1): (1, 1, 1),
        (4, 5): (1, 1, 1),
        (0, 4): (1, 1, 1),
        (1, 5): (1, 1, -1),
        (0, 5): (0, 0, 1),
        (1, 4): (0, 0, -1),
    }
    weights = (
        ((0, 2), 1),
        ((1, 2), -1),
        ((4, 2), 1),
        ((5, 2), 1),
        ((0, 3), 1),
        ((1, 3), 1),
        ((4, 3), -1),
        ((5, 3), 1),
    )
    for (tail, head), weight in weights:
        edge = tuple(sorted((tail, head)))
        if edge[0] == tail:
            table[edge] = (0, 1, weight)
        else:
            table[edge] = (1, 0, weight)
    assert len(table) == 15
    return table


def audit_zero_fibre() -> dict[str, object]:
    """Audit a Tutte failure confined to an internally zero Q fibre."""
    table = zero_fibre_table()
    total, pure, cross, details = ledgers(table, 6)
    word = (0, 0, 1, 1, 1, 1)
    masks = shore_masks(word)
    assert pure.get(word, 0) == shore_hafnian_product(table, word) == 0
    assert cross[word] == total[word] == 0
    assert len(details[word]) == 2
    assert sorted(value for _, value, _ in details[word]) == [-1, 1]
    assert not satisfies_tutte(table, masks[0], 0)
    assert odd_component_count(table, masks[0], 0) == 2
    return {
        "D": pure.get(word, 0),
        "Q": cross[word],
        "compatible_terms": len(details[word]),
        "empty_separator_odd_components": 2,
        "tutte": False,
    }


def main() -> None:
    factorization = audit_factorization()
    active = audit_active_fibre()
    zero = audit_zero_fibre()
    print("matrix-unit active word-shore independent audit: PASS")
    print(f"  independent all-word factorization counts: {factorization}")
    print(f"  active fibre ledger: {active}")
    print(f"  zero-fibre Tutte failure ledger: {zero}")


if __name__ == "__main__":
    main()
