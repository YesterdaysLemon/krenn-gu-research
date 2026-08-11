"""Primary checks for active matrix-unit word-shore synchronization."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product

Edge = tuple[int, int]
EdgeData = dict[Edge, tuple[int, int, int]]
Matching = tuple[Edge, ...]
Word = tuple[int, ...]


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate labelled perfect matchings recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def matching_record(
    matching: Matching,
    table: EdgeData,
    n: int,
) -> tuple[Word, int, bool]:
    """Return the induced word, weight, and diagonal-sector flag."""
    word = [-1] * n
    weight = 1
    diagonal = True
    for left, right in matching:
        edge = tuple(sorted((left, right)))
        first_label, second_label, scalar = table[edge]
        if left > right:
            first_label, second_label = second_label, first_label
        word[left] = first_label
        word[right] = second_label
        weight *= scalar
        diagonal = diagonal and first_label == second_label
    return tuple(word), weight, diagonal


def coefficient_ledgers(
    table: EdgeData,
    n: int,
) -> tuple[dict[Word, int], dict[Word, int], dict[Word, int], dict[Word, list[tuple[Matching, int, bool]]]]:
    """Split every coefficient into diagonal and offdiagonal sectors."""
    total: dict[Word, int] = {}
    diagonal: dict[Word, int] = {}
    offdiagonal: dict[Word, int] = {}
    terms: dict[Word, list[tuple[Matching, int, bool]]] = {}
    for matching in perfect_matchings(tuple(range(n))):
        word, weight, is_diagonal = matching_record(matching, table, n)
        total[word] = total.get(word, 0) + weight
        target = diagonal if is_diagonal else offdiagonal
        target[word] = target.get(word, 0) + weight
        terms.setdefault(word, []).append((matching, weight, is_diagonal))
    return total, diagonal, offdiagonal, terms


def pure_hafnian(table: EdgeData, vertices: tuple[int, ...], colour: int) -> int:
    """Compute one exact principal pure-colour hafnian."""
    @lru_cache(maxsize=None)
    def recurse(remaining: tuple[int, ...]) -> int:
        if not remaining:
            return 1
        if len(remaining) % 2:
            return 0
        first = remaining[0]
        value = 0
        for index in range(1, len(remaining)):
            partner = remaining[index]
            edge = tuple(sorted((first, partner)))
            first_label, second_label, scalar = table[edge]
            if first > partner:
                first_label, second_label = second_label, first_label
            if first_label != colour or second_label != colour:
                continue
            residue = remaining[1:index] + remaining[index + 1 :]
            value += scalar * recurse(residue)
        return value

    return recurse(tuple(sorted(vertices)))


def shore_product(table: EdgeData, word: Word) -> int:
    """Return the product of the three word-shore hafnians."""
    return_value = 1
    for colour in range(3):
        shore = tuple(index for index, label in enumerate(word) if label == colour)
        return_value *= pure_hafnian(table, shore, colour)
    return return_value


def deterministic_table(n: int, seed: int) -> EdgeData:
    """Build a complete exact table unrelated to either sharpness gadget."""
    table: EdgeData = {}
    for left, right in combinations(range(n), 2):
        first_label = (left + 2 * right + seed) % 3
        second_label = (2 * left + right + seed + 1) % 3
        magnitude = 1 + ((left + 1) * (right + 2) + seed) % 5
        sign = -1 if (left + right + seed) % 3 == 0 else 1
        table[(left, right)] = (first_label, second_label, sign * magnitude)
    return table


def assert_diagonal_factorization() -> dict[int, int]:
    """Check every coordinate word for deterministic orders six and eight."""
    ledger: dict[int, int] = {}
    for n, seed in ((6, 2), (8, 5)):
        table = deterministic_table(n, seed)
        _, diagonal, _, _ = coefficient_ledgers(table, n)
        checked = 0
        for word in product(range(3), repeat=n):
            assert diagonal.get(word, 0) == shore_product(table, word)
            checked += 1
        ledger[n] = checked
    return ledger


def active_synchronized_table() -> EdgeData:
    """Return the complete six-vertex active-fibre table from the theorem."""
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


def assert_active_synchronized_fibre() -> dict[str, object]:
    """Replay a nonzero D=-Q fibre with exact word-shore matchings."""
    table = active_synchronized_table()
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table, 6)
    word = (2, 1, 0, 0, 2, 1)
    assert total[word] == 0
    assert diagonal[word] == shore_product(table, word) == 1
    assert offdiagonal[word] == -1
    assert len(terms[word]) == 2
    assert sorted((weight, is_diagonal) for _, weight, is_diagonal in terms[word]) == [
        (-1, False),
        (1, True),
    ]

    pure_values = [total[(colour,) * 6] for colour in range(3)]
    assert pure_values == [1, 1, 1]
    shore_values = {
        colour: pure_hafnian(
            table,
            tuple(index for index, label in enumerate(word) if label == colour),
            colour,
        )
        for colour in range(3)
    }
    assert shore_values == {0: 1, 1: 1, 2: 1}

    exposed = (0, 0, 2, 1, 0, 2)
    assert total[exposed] == 1
    assert len(terms[exposed]) == 1
    return {
        "word": word,
        "D": diagonal[word],
        "Q": offdiagonal[word],
        "shore_hafnians": shore_values,
        "pure_coefficients": pure_values,
        "explicit_nonwitness_word": exposed,
    }


def unsynchronized_zero_fibre_table() -> EdgeData:
    """Return the complete binary-square zero-fibre sharpness gadget."""
    table: EdgeData = {}
    cross_weights = {
        (0, 2): 1,
        (1, 2): -1,
        (2, 4): 1,
        (2, 5): 1,
        (0, 3): 1,
        (1, 3): 1,
        (3, 4): -1,
        (3, 5): 1,
    }
    for edge, weight in cross_weights.items():
        left, right = edge
        if left in (2, 3):
            table[tuple(sorted(edge))] = (1, 0, weight)
        else:
            table[tuple(sorted(edge))] = (0, 1, weight)
    table.update(
        {
            (2, 3): (0, 0, 1),
            (0, 1): (1, 1, 1),
            (4, 5): (1, 1, 1),
            (0, 4): (1, 1, 1),
            (1, 5): (1, 1, -1),
            (0, 5): (0, 0, 1),
            (1, 4): (0, 0, -1),
        }
    )
    assert len(table) == 15
    return table


def assert_unsynchronized_zero_fibre() -> dict[str, object]:
    """Replay internal Q cancellation with a failed word shore."""
    table = unsynchronized_zero_fibre_table()
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table, 6)
    word = (0, 0, 1, 1, 1, 1)
    assert total[word] == diagonal.get(word, 0) == offdiagonal[word] == 0
    assert shore_product(table, word) == 0
    assert len(terms[word]) == 2
    assert all(not is_diagonal for _, _, is_diagonal in terms[word])
    assert sorted(weight for _, weight, _ in terms[word]) == [-1, 1]

    nonzero_coefficients = {key: value for key, value in total.items() if value}
    assert nonzero_coefficients == {(0,) * 6: -1}
    return {
        "word": word,
        "D": diagonal.get(word, 0),
        "Q": offdiagonal[word],
        "offdiagonal_term_weights": [-1, 1],
        "shore_product": shore_product(table, word),
        "full_tensor_support": nonzero_coefficients,
    }


def main() -> None:
    factorization = assert_diagonal_factorization()
    active = assert_active_synchronized_fibre()
    zero = assert_unsynchronized_zero_fibre()
    print("matrix-unit active word-shore primary checks: PASS")
    print(f"  every-word factorization counts: {factorization}")
    print(f"  active synchronized fibre: {active}")
    print(f"  unsynchronized zero fibre: {zero}")


if __name__ == "__main__":
    main()
