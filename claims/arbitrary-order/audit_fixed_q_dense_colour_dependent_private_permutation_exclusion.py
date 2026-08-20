"""Independent no-import audit of the GLD23 private-permutation exclusion.

Unlike the primary 945-matching expansion, this standard-library audit
derives the affine system from the only three nonzero matching types in the
dense chart.  It does no symmetry reduction: all 24^2 ordered active-colour
permutation pairs are eliminated separately over Fraction.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product


ROOTS = tuple(range(4))
COLOURS = tuple(range(3))
DEAD = 2
PERMS = tuple(permutations(ROOTS))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}

P0_BASE = 0
P1_BASE = 12
W_BASE = 24
ALPHA_BASE = 78
NVARIABLES = 81


def p_index(which: int, root: int, colour: int) -> int:
    return (P0_BASE if which == 0 else P1_BASE) + 3 * root + colour


def w_index(left: int, right: int, lc: int, rc: int) -> int:
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return W_BASE + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def add(row: dict[int, int], index: int, value: int) -> None:
    if not value:
        return
    updated = row.get(index, 0) + value
    if updated:
        row[index] = updated
    else:
        row.pop(index, None)


def private_assignment(
    port_word: tuple[int, ...],
    colour_perms: tuple[tuple[int, ...], ...],
    retained_ports: tuple[int, ...],
) -> tuple[dict[int, int], bool]:
    assignment: dict[int, int] = {}
    for port in retained_ports:
        colour = port_word[port]
        root = colour_perms[colour][port]
        if root in assignment:
            return {}, False
        assignment[root] = colour
    return assignment, True


def closed_form_system(
    first_perm: tuple[int, ...], second_perm: tuple[int, ...]
) -> list[tuple[dict[int, int], int]]:
    """Use QQ+4RU, QR+QU+3RU, and 2QU+2RU+RR matching types."""

    colour_perms = (first_perm, second_perm, ROOTS)
    x = (1, 1, 0)
    y = (1, -1, 0)
    rows: list[tuple[dict[int, int], int]] = []

    for port_word in product(COLOURS, repeat=4):
        equations: dict[tuple[int, ...], list[object]] = {}

        def equation(root_word: tuple[int, ...]) -> list[object]:
            return equations.setdefault(root_word, [{}, 0])

        # The residual endpoints pair together; all four ports meet roots.
        full, valid = private_assignment(port_word, colour_perms, ROOTS)
        if valid:
            root_word = tuple(full[root] for root in ROOTS)
            equation(root_word)[1] -= 1

        # One residual endpoint meets a root and the other the omitted port.
        for omitted_port in ROOTS:
            retained = tuple(port for port in ROOTS if port != omitted_port)
            partial, valid = private_assignment(port_word, colour_perms, retained)
            if not valid:
                continue
            missing_root = next(root for root in ROOTS if root not in partial)
            port_colour = port_word[omitted_port]
            for free_colour in COLOURS:
                values = dict(partial)
                values[missing_root] = free_colour
                root_word = tuple(values[root] for root in ROOTS)
                row = equation(root_word)[0]
                assert isinstance(row, dict)
                add(
                    row,
                    p_index(0, missing_root, free_colour),
                    y[port_colour],
                )
                add(
                    row,
                    p_index(1, missing_root, free_colour),
                    x[port_colour],
                )

        # Both residual endpoints meet ports; the two unused roots pair.
        for omitted_pair in EDGES:
            left_port, right_port = omitted_pair
            left_colour = port_word[left_port]
            right_colour = port_word[right_port]
            corrected_pair = (
                x[left_colour] * y[right_colour] + y[left_colour] * x[right_colour]
            )
            if not corrected_pair:
                continue
            retained = tuple(port for port in ROOTS if port not in omitted_pair)
            partial, valid = private_assignment(port_word, colour_perms, retained)
            if not valid:
                continue
            missing_roots = tuple(root for root in ROOTS if root not in partial)
            for left_colour_free in COLOURS:
                for right_colour_free in COLOURS:
                    values = dict(partial)
                    values[missing_roots[0]] = left_colour_free
                    values[missing_roots[1]] = right_colour_free
                    root_word = tuple(values[root] for root in ROOTS)
                    row = equation(root_word)[0]
                    assert isinstance(row, dict)
                    add(
                        row,
                        w_index(
                            missing_roots[0],
                            missing_roots[1],
                            left_colour_free,
                            right_colour_free,
                        ),
                        corrected_pair,
                    )

        # Allow arbitrary coefficients even on the three pure target words.
        if len(set(port_word)) == 1:
            colour = port_word[0]
            row = equation(port_word)[0]
            assert isinstance(row, dict)
            add(row, ALPHA_BASE + colour, -1)

        for raw_row, raw_rhs in equations.values():
            assert isinstance(raw_row, dict)
            assert isinstance(raw_rhs, int)
            if raw_row or raw_rhs:
                rows.append((raw_row, raw_rhs))

    return rows


def exact_consistency(
    integer_rows: list[tuple[dict[int, int], int]],
) -> tuple[bool, int]:
    """Independent sparse Fraction elimination without a stored certificate."""

    pivots: dict[int, tuple[dict[int, Fraction], Fraction]] = {}
    for integer_row, integer_rhs in integer_rows:
        row = {key: Fraction(value) for key, value in integer_row.items()}
        rhs = Fraction(integer_rhs)
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse_pivot = 1 / row[pivot]
                row = {key: value * inverse_pivot for key, value in row.items()}
                rhs *= inverse_pivot
                pivots[pivot] = (row, rhs)
                break
            basis, basis_rhs = pivots[pivot]
            factor = row[pivot]
            for key, value in basis.items():
                updated = row.get(key, Fraction(0)) - factor * value
                if updated:
                    row[key] = updated
                else:
                    row.pop(key, None)
            rhs -= factor * basis_rhs
        else:
            if rhs:
                return False, len(pivots)
    return True, len(pivots)


EXPECTED_INCONSISTENT_RANKS = {
    75: 2,
    76: 56,
    78: 63,
    79: 305,
    80: 150,
}


def main() -> None:
    outcomes: Counter[int] = Counter()
    for first_perm, second_perm in product(PERMS, repeat=2):
        rows = closed_form_system(first_perm, second_perm)
        assert all(0 <= variable < NVARIABLES for row, _ in rows for variable in row)
        consistent, rank = exact_consistency(rows)
        assert not consistent
        outcomes[rank] += 1

    assert dict(outcomes) == EXPECTED_INCONSISTENT_RANKS
    assert sum(outcomes.values()) == 24**2 == 576
    print(
        "PASS: independent three-type Fraction audit excludes all 576 "
        "ordered active private-permutation pairs without symmetry reduction"
    )


if __name__ == "__main__":
    main()
