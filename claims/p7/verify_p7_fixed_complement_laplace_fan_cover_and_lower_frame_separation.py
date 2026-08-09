"""Verify the P7 fixed-complement fan cover and lower-frame separation."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

ROOTS = tuple(range(5))
LOCAL_COLUMNS = tuple(range(5))
UNMARKED = tuple(range(1, 5))
RANK_TWO_PAIRS = {(0, 1), (2, 3)}


def permanent_dp(matrix: sp.Matrix) -> sp.Expr:
    rows, columns = matrix.shape
    assert rows == columns
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in range(rows):
        nxt: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for column in range(columns):
                if mask & (1 << column) == 0:
                    new_mask = mask | (1 << column)
                    nxt[new_mask] = nxt.get(new_mask, 0) + value * matrix[row, column]
        states = nxt
    return sp.expand(states[(1 << columns) - 1])


def submatrix(
    matrix: sp.Matrix, rows: tuple[int, ...], columns: tuple[int, ...]
) -> sp.Matrix:
    return sp.Matrix([[matrix[row, column] for column in columns] for row in rows])


def complement(universe: tuple[int, ...], chosen: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(item for item in universe if item not in chosen)


def laplace_term(
    matrix: sp.Matrix, root_pair: tuple[int, int], retained: tuple[int, int]
) -> sp.Expr:
    return sp.expand(
        permanent_dp(submatrix(matrix, root_pair, retained))
        * permanent_dp(
            submatrix(
                matrix,
                complement(ROOTS, root_pair),
                complement(LOCAL_COLUMNS, retained),
            )
        )
    )


def check_generic_fixed_complement_laplace() -> None:
    entries = sp.symbols("h0:25")
    matrix = sp.Matrix(5, 5, entries)
    full = permanent_dp(matrix)
    for retained in combinations(UNMARKED, 2):
        expansion = sum(
            (laplace_term(matrix, root_pair, retained) for root_pair in combinations(ROOTS, 2)),
            sp.Integer(0),
        )
        assert sp.Poly(sp.expand(expansion - full), *entries).is_zero


def canonical_matrices() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix(
            [
                [-1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [-1, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 0, 1, 0],
            ]
        ),
        sp.Matrix(
            [
                [0, 1, 0, 0, 0],
                [-1, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [-1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
            ]
        ),
        sp.Matrix(
            [
                [-1, 1, 0, 0, 0],
                [-1, 0, 1, 0, 0],
                [-1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 0],
            ]
        ),
    )


def check_six_window_cover_and_separation() -> None:
    axis_labels = (0, 0, 1, 1, 2)
    assert {
        pair
        for pair in combinations(ROOTS, 2)
        if 3 - len({axis_labels[root] for root in pair}) == 2
    } == RANK_TWO_PAIRS

    expected_witnesses = (
        {
            (1, 2): ((1, 4), -1),
            (1, 3): ((0, 2), 1),
            (1, 4): ((3, 4), -1),
            (2, 3): ((1, 4), -1),
            (2, 4): ((1, 3), -1),
            (3, 4): ((3, 4), -1),
        },
        {
            (1, 2): ((0, 4), -1),
            (1, 3): ((0, 2), -1),
            (1, 4): ((0, 4), -1),
            (2, 3): ((2, 4), -1),
            (2, 4): ((1, 3), 1),
            (3, 4): ((2, 4), -1),
        },
        {
            (1, 2): ((1, 4), -1),
            (1, 3): ((0, 2), 1),
            (1, 4): ((3, 4), -1),
            (2, 3): ((1, 4), -1),
            (2, 4): ((1, 3), -1),
            (3, 4): ((3, 4), -1),
        },
    )

    for matrix, witnesses in zip(canonical_matrices(), expected_witnesses, strict=True):
        full = permanent_dp(matrix)
        assert full == -1
        for retained in combinations(UNMARKED, 2):
            terms = {
                root_pair: laplace_term(matrix, root_pair, retained)
                for root_pair in combinations(ROOTS, 2)
            }
            assert sum(terms.values(), sp.Integer(0)) == full
            assert all(terms[root_pair] == 0 for root_pair in RANK_TWO_PAIRS)
            witness_pair, witness_value = witnesses[retained]
            assert terms[witness_pair] == witness_value
            assert witness_pair not in RANK_TWO_PAIRS


def assembled_blocker_rows() -> dict[str, sp.Matrix]:
    h0, h1, h2 = canonical_matrices()
    raw: dict[str, list[list[sp.Expr]]] = {
        "t": [[h0[i, 0], h1[i, 0], h2[i, 0]] for i in ROOTS],
        "u01": [[h0[i, 1], h1[i, 3], 0] for i in ROOTS],
        "v01": [[h0[i, 2], h1[i, 4], 0] for i in ROOTS],
        "u02": [[h0[i, 3], 0, h2[i, 1]] for i in ROOTS],
        "v02": [[h0[i, 4], 0, h2[i, 2]] for i in ROOTS],
        "u12": [[0, h1[i, 1], h2[i, 3]] for i in ROOTS],
        "v12": [[0, h1[i, 2], h2[i, 4]] for i in ROOTS],
    }
    return {name: sp.Matrix(rows) for name, rows in raw.items()}


def check_common_physical_system() -> None:
    rows = assembled_blocker_rows()
    assert rows["t"].rank() == 3
    null_directions = {
        "u01": sp.Matrix([0, 0, 1]),
        "v01": sp.Matrix([0, 0, 1]),
        "u02": sp.Matrix([0, 1, 0]),
        "v02": sp.Matrix([0, 1, 0]),
        "u12": sp.Matrix([1, 0, 0]),
        "v12": sp.Matrix([1, 0, 0]),
    }
    for name, direction in null_directions.items():
        assert rows[name].rank() == 2
        assert rows[name] * direction == sp.zeros(5, 1)


def check_forced_fan() -> None:
    missing_pairs = {
        0: frozenset({5, 6}),
        1: frozenset({1, 2}),
        2: frozenset({3, 4}),
    }
    all_ports = frozenset(range(1, 7))
    colour_windows: dict[int, set[frozenset[int]]] = {}
    for colour, missing_pair in missing_pairs.items():
        available = sorted(all_ports - missing_pair)
        colour_windows[colour] = {
            missing_pair | frozenset(retained)
            for retained in combinations(available, 2)
        }
        assert len(colour_windows[colour]) == 6

    fan = {
        frozenset({1, 2, 3, 4}),
        frozenset({1, 2, 5, 6}),
        frozenset({1, 3, 5, 6}),
        frozenset({1, 4, 5, 6}),
    }
    assert frozenset({1, 2, 3, 4}) in colour_windows[1]
    assert fan - {frozenset({1, 2, 3, 4})} <= colour_windows[0]
    assert len({(colour, window) for colour, windows in colour_windows.items() for window in windows}) == 18


def main() -> None:
    check_generic_fixed_complement_laplace()
    check_six_window_cover_and_separation()
    check_common_physical_system()
    check_forced_fan()
    print("PASS: six generic fixed-complement Laplace identities")
    print("PASS: all 18 colour-tagged graph-side windows and forced tetrahedral fan")
    print("PASS: common canonical system and global double-blocker null directions")
    print("PASS: zero rho>=2 shore co-occurrence in the exact rational model")
    print("SCOPE: distinguished companion rank remains UNKNOWN")
    print("SCOPE: legal marked-star fan and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
