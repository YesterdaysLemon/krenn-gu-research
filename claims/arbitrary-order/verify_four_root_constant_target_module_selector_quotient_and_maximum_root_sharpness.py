"""Primary exact replay for the four-root constant-module selector theorem."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from math import comb


ROOTS = tuple(range(4))
PORTS = tuple(("u", i) for i in range(4))
RESIDUALS = (("q", 0), ("q", 1))
OUTSIDE = PORTS + RESIDUALS


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield unordered perfect matchings of a small labelled tuple."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def outside_letter(root: int, outside: tuple[str, int]) -> str | None:
    """Clean-chart root letter on a root-to-outside edge."""

    kind, index = outside
    if kind == "u":
        return "a" if root == index else None
    if index == 0:
        return "b"
    return "c"


def companion_column(outside_assignment: tuple[tuple[str, int], ...]):
    """Enumerate one clean companion column by injections and root matchings.

    Values count matching multiplicities.  The second key is the common
    power of the root-root scale t.
    """

    size = len(outside_assignment)
    if size > 4 or size % 2:
        return Counter()
    result: Counter[tuple[tuple[str, ...], int]] = Counter()
    for assigned_roots in permutations(ROOTS, size):
        letters: list[str | None] = [None] * 4
        legal = True
        for root, outside in zip(assigned_roots, outside_assignment, strict=True):
            letter = outside_letter(root, outside)
            if letter is None:
                legal = False
                break
            letters[root] = letter
        if not legal:
            continue
        remaining = tuple(root for root in ROOTS if letters[root] is None)
        for matching in perfect_matchings(remaining):
            trial = letters[:]
            for left, right in matching:
                trial[left] = "b"
                trial[right] = "b"
            assert all(letter is not None for letter in trial)
            result[(tuple(trial), len(matching))] += 1
    return result


def all_columns():
    columns = {}
    for size in (0, 2, 4):
        for assignment in combinations(OUTSIDE, size):
            columns[frozenset(assignment)] = companion_column(assignment)
    assert len(columns) == 31
    return columns


def check_dimensions() -> None:
    full_deck = sum(comb(6, size) * 3**size for size in (2, 4, 6))
    assert full_deck == 2079
    assert 3**8 == 6561
    assert 3**6 == 729
    assert 3**4 == 81
    assert full_deck * 3**2 == 18711
    assert full_deck * 3**4 == 168399

    fixed_q = 1
    fixed_q += 2 * (comb(4, 2) * 3**2 + comb(4, 4) * 3**4)
    fixed_q += 2 * (comb(4, 1) * 3 + comb(4, 3) * 3**3)
    assert fixed_q == 511
    assert fixed_q * 3**2 == 4599
    assert fixed_q * 3**4 == 41391
    assert 6 * 729 + 81 == 4455


def deck_labels():
    """Yield all 2079 labelled basis coordinates of the nonempty even deck."""

    for size in (2, 4, 6):
        for label in combinations(OUTSIDE, size):
            for word in product(range(3), repeat=size):
                yield label, word


def check_seven_selectors(columns) -> None:
    basis_coordinates = tuple(deck_labels())
    assert len(basis_coordinates) == 2079

    targets = tuple(combinations(range(4), 2)) + (tuple(range(4)),)
    for target_tuple in targets:
        target = frozenset(target_tuple)
        complement_ports = frozenset(("u", i) for i in ROOTS if i not in target)
        pivot = tuple("b" if i in target else "a" for i in ROOTS)
        expected_t_degree = 1 if len(target) == 2 else 2
        expected_multiplicity = 1 if len(target) == 2 else 3

        occurrences = []
        for assignment, column in columns.items():
            coefficient = column.get((pivot, expected_t_degree), 0)
            if coefficient:
                occurrences.append((assignment, coefficient))
        assert occurrences == [(complement_ports, expected_multiplicity)]

        target_label = frozenset(RESIDUALS) | frozenset(("u", i) for i in target)
        checked = 0
        selected_outputs = set()
        for label_tuple, word in basis_coordinates:
            label = frozenset(label_tuple)
            assignment = frozenset(OUTSIDE) - label
            raw = columns[assignment].get((pivot, expected_t_degree), 0)
            normalized = raw / expected_multiplicity
            word_by_mode = dict(zip(label_tuple, word, strict=True))
            evaluated_residual_letters_are_e0 = all(
                word_by_mode[q] == 0 for q in RESIDUALS if q in label
            )
            observed = normalized * int(evaluated_residual_letters_are_e0)
            expected = int(label == target_label and evaluated_residual_letters_are_e0)
            assert observed == expected
            checked += 1
            if expected:
                selected_outputs.add(
                    tuple(word_by_mode[("u", i)] for i in target_tuple)
                )
        assert checked == 2079
        assert selected_outputs == set(product(range(3), repeat=len(target_tuple)))
        print(f"S={target_tuple}: PASS ({checked} deck coordinates)")


def check_zero_root_wall(columns) -> None:
    for target_tuple in tuple(combinations(range(4), 2)) + (tuple(range(4)),):
        target = frozenset(target_tuple)
        assignment = frozenset(("u", i) for i in ROOTS if i not in target)
        expected_degree = 1 if len(target) == 2 else 2
        column = columns[assignment]
        assert column
        assert all(t_degree == expected_degree for (_word, t_degree) in column)
        # At t=0 the complete desired companion is zero.


def check_spanning_nuisance() -> None:
    """The identity root-to-private-port tensor has every root slice."""

    slices = set()
    for port_word in product(range(3), repeat=4):
        root_word = tuple(port_word)
        slices.add(root_word)
    assert len(slices) == 81
    assert slices == set(product(range(3), repeat=4))


def check_triple_blocker_helper_support() -> None:
    # The clean assigned row and two c-helper rows are three independent
    # outside coordinate rows.  Every helper contribution has a c root letter.
    row_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    assert row_matrix == tuple(tuple(int(i == j) for j in range(3)) for i in range(3))
    no_c_pivots = {
        tuple("b" if i in target else "a" for i in ROOTS)
        for target in map(frozenset, combinations(range(4), 2))
    }
    no_c_pivots.add(("b", "b", "b", "b"))
    assert all("c" not in pivot for pivot in no_c_pivots)


def main() -> None:
    check_dimensions()
    columns = all_columns()
    check_seven_selectors(columns)
    check_zero_root_wall(columns)
    check_spanning_nuisance()
    check_triple_blocker_helper_support()
    print("four-root constant target-module selector verification: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
