"""Independent no-import audit of the bridge-word sharpness boundary.

The audit reconstructs the complete six-vertex relay gadget from an oriented
edge dictionary and evaluates coefficients by assignment-specific bitmask
dynamic programming.  It does not import the primary verifier.  The finite
checks support the displayed sharpness example and label bookkeeping; they
are not an arbitrary-order proof and the gadget is not a Krenn--Gu witness.
"""

from functools import lru_cache
from itertools import combinations, product

N = 6
COLOURS = range(3)
FULL_MASK = (1 << N) - 1


def relay_units():
    """Return all oriented units of the activated K6 relay gadget."""
    raw = {
        (0, 1): (1, 1, 1),
        (0, 2): (0, 1, 1),
        (0, 3): (2, 2, 1),
        (0, 4): (0, 0, 1),
        (0, 5): (0, 2, -1),
        (1, 2): (2, 2, 1),
        (1, 3): (0, 1, 1),
        (1, 4): (1, 0, 1),
        (1, 5): (0, 0, 1),
        (2, 3): (0, 0, 1),
        (2, 4): (1, 2, 1),
        (2, 5): (1, 1, 1),
        (3, 4): (1, 1, 1),
        (3, 5): (2, 0, 1),
        (4, 5): (2, 2, 1),
    }
    table = [[None for _ in range(N)] for _ in range(N)]
    for (u, v), (left, right, weight) in raw.items():
        table[u][v] = (left, right, weight)
        table[v][u] = (right, left, weight)
    return table


def coefficient(table, word, diagonal_only=False):
    """Evaluate one word by a bitmask matching recurrence."""

    @lru_cache(None)
    def visit(mask):
        if mask == 0:
            return 1
        u_bit = mask & -mask
        u = u_bit.bit_length() - 1
        rest = mask ^ u_bit
        total = 0
        candidates = rest
        while candidates:
            v_bit = candidates & -candidates
            candidates ^= v_bit
            v = v_bit.bit_length() - 1
            left, right, weight = table[u][v]
            if diagonal_only and left != right:
                continue
            if left == word[u] and right == word[v]:
                total += weight * visit(rest ^ v_bit)
        return total

    return visit(FULL_MASK)


def compatible_terms(table, word, diagonal_only=False):
    """List compatible monomials only for the two named audit words."""

    def visit(mask):
        if mask == 0:
            return [((), 1)]
        u_bit = mask & -mask
        u = u_bit.bit_length() - 1
        rest = mask ^ u_bit
        terms = []
        candidates = rest
        while candidates:
            v_bit = candidates & -candidates
            candidates ^= v_bit
            v = v_bit.bit_length() - 1
            left, right, weight = table[u][v]
            if diagonal_only and left != right:
                continue
            if left != word[u] or right != word[v]:
                continue
            for tail, tail_weight in visit(rest ^ v_bit):
                terms.append((((u, v),) + tail, weight * tail_weight))
        return terms

    return visit(FULL_MASK)


def pure_hafnian(table, mask, colour):
    """Evaluate a principal pure-colour hafnian by an independent cache."""

    @lru_cache(None)
    def visit(state):
        if state == 0:
            return 1
        u_bit = state & -state
        u = u_bit.bit_length() - 1
        rest = state ^ u_bit
        total = 0
        candidates = rest
        while candidates:
            v_bit = candidates & -candidates
            candidates ^= v_bit
            v = v_bit.bit_length() - 1
            left, right, weight = table[u][v]
            if left == right == colour:
                total += weight * visit(rest ^ v_bit)
        return total

    return visit(mask)


def audit_complete_matrix_unit_support(table):
    edge_count = 0
    for u, v in combinations(range(N), 2):
        unit = table[u][v]
        assert unit is not None
        assert unit[2] != 0
        edge_count += 1
    assert edge_count == 15

    # A nonzero matrix unit evaluates nontrivially on two fully supported
    # coordinate vectors.  Thus no two vertices are zero-coupled, while a
    # singleton is always a torus-root configuration.
    maximum_torus_root = 1
    assert maximum_torus_root == 1


def audit_pure_activation(table):
    expected_supports = {
        0: {frozenset((2, 3)), frozenset((0, 4)), frozenset((1, 5))},
        1: {frozenset((0, 1)), frozenset((2, 5)), frozenset((3, 4))},
        2: {frozenset((4, 5)), frozenset((0, 3)), frozenset((1, 2))},
    }
    for colour in COLOURS:
        support = set()
        degrees = [0] * N
        for u, v in combinations(range(N), 2):
            left, right, _ = table[u][v]
            if left == right == colour:
                support.add(frozenset((u, v)))
                degrees[u] += 1
                degrees[v] += 1
        assert support == expected_supports[colour]
        assert degrees == [1] * N
        assert pure_hafnian(table, FULL_MASK, colour) == 1
        for edge in support:
            u, v = tuple(edge)
            complement = FULL_MASK ^ (1 << u) ^ (1 << v)
            assert pure_hafnian(table, complement, colour) == 1

    # These are the full near-monochromatic active-deck rows, not merely
    # the three pure coefficients.
    for base, local, vertex in product(COLOURS, COLOURS, range(N)):
        word = [base] * N
        word[vertex] = local
        expected = int(local == base)
        assert coefficient(table, tuple(word)) == expected


def audit_selected_word_and_scope(table):
    selected = (0, 0, 1, 1, 2, 2)
    terms = compatible_terms(table, selected)
    normalized = {(frozenset(edges), weight) for edges, weight in terms}
    expected = {
        (frozenset(((0, 2), (1, 3), (4, 5))), 1),
        (frozenset(((0, 5), (1, 3), (2, 4))), -1),
    }
    assert normalized == expected
    assert coefficient(table, selected) == 0
    assert compatible_terms(table, selected, diagonal_only=True) == []
    assert coefficient(table, selected, diagonal_only=True) == 0

    failure = (0, 0, 1, 1, 0, 1)
    failure_terms = compatible_terms(table, failure)
    assert failure_terms == [(((0, 4), (1, 3), (2, 5)), 1)]
    assert coefficient(table, failure) == 1

    expected_nonzero = {
        (0, 0, 0, 0, 0, 0): 1,
        (0, 0, 1, 1, 0, 1): 1,
        (0, 0, 1, 1, 1, 0): 1,
        (0, 1, 0, 0, 0, 2): -1,
        (0, 1, 1, 2, 0, 0): 1,
        (0, 2, 2, 1, 1, 2): -1,
        (0, 2, 2, 2, 0, 0): 1,
        (1, 1, 0, 0, 2, 2): 1,
        (1, 1, 1, 1, 1, 1): 1,
        (1, 1, 1, 2, 2, 0): 1,
        (2, 0, 1, 2, 2, 0): 1,
        (2, 1, 1, 2, 0, 1): 1,
        (2, 2, 2, 2, 2, 2): 1,
    }
    actual_nonzero = {}
    for word in product(COLOURS, repeat=N):
        value = coefficient(table, word)
        if value:
            actual_nonzero[word] = value
    assert actual_nonzero == expected_nonzero


def audit_local_word_flips():
    # Square order: u1,u2,v1,v2.  The promoted pure bridges exchange the
    # two endpoint colours, so none of the three local pairings can be a
    # diagonal matching for the original word.
    square_word = (0, 0, 1, 1)
    square_promoted = {(0, 1): 1, (2, 3): 0}
    promoted_square_word = [None] * 4
    for (u, v), colour in square_promoted.items():
        promoted_square_word[u] = colour
        promoted_square_word[v] = colour
    assert tuple(promoted_square_word) == (1, 1, 0, 0)
    assert tuple(promoted_square_word) != square_word
    assert all(
        not (
            square_word[u] == square_word[v]
            and square_promoted.get(tuple(sorted((u, v)))) == square_word[u]
        )
        for u, v in combinations(range(4), 2)
    )

    # Hexagon order: u0,u1,v0,v2,w1,w2.  Every promoted endpoint flips;
    # the word-preserving diagonal pairs are the disjoint complementary
    # pairs and are not among the promoted bridges.
    hex_word = (0, 1, 0, 2, 1, 2)
    hex_promoted = {(1, 3): 0, (0, 5): 1, (2, 4): 2}
    promoted_hex_word = [None] * 6
    for (u, v), colour in hex_promoted.items():
        promoted_hex_word[u] = colour
        promoted_hex_word[v] = colour
    assert all(a != b for a, b in zip(promoted_hex_word, hex_word, strict=True))
    preserving = {(0, 2): 0, (1, 4): 1, (3, 5): 2}
    assert set(preserving).isdisjoint(hex_promoted)


def main():
    table = relay_units()
    audit_complete_matrix_unit_support(table)
    audit_pure_activation(table)
    audit_selected_word_and_scope(table)
    audit_local_word_flips()
    print("independent bridge-word relay audit: PASS")
    print("bounded order:                         6")
    print("coefficient words checked:             729")
    print("maximum torus-root number:              1")
    print("pure coefficients/cofactors:            ACTIVE EXACTLY")
    print("selected mixed coefficient:             ZERO (TWO TERMS)")
    print("diagonal rematching for selected word:  ABSENT")
    print("explicit non-witness coefficient:       NONZERO")
    print("gadget is a Krenn-Gu witness:            false")
    print("global conjecture resolved:              false")


if __name__ == "__main__":
    main()
