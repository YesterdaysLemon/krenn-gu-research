"""Exact symbolic checks for the arbitrary-alignment degree-five selector.

This verifies the two row-type lemmas used by the proof.  It does not loop
over core alignments, mixed words, or terminal rectangles.
"""

from __future__ import annotations

from itertools import combinations, permutations

import sympy as sp

RHO = sp.Symbol("rho")
MINPOLY = sp.Poly(RHO**2 - 21, RHO)
FEATURES = ("A", "B", "5", "a", "b")
H = ("f1", "ell", "h3", "h5", "ha")
Y = ("f2", "h4")


def reduce_qrho(value: sp.Expr) -> sp.Expr:
    """Return the canonical linear representative modulo rho^2-21."""

    numerator, denominator = sp.fraction(sp.cancel(value))
    denominator = sp.rem(sp.Poly(denominator, RHO), MINPOLY).as_expr()
    numerator = sp.rem(sp.Poly(numerator, RHO), MINPOLY).as_expr()
    inverse = sp.invert(sp.Poly(denominator, RHO), MINPOLY).as_expr()
    return sp.rem(sp.Poly(sp.expand(numerator * inverse), RHO), MINPOLY).as_expr()


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Permanent by subset dynamic programming, with exact field reduction."""

    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in matrix:
        next_states: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or entry == 0:
                    continue
                new_mask = mask | (1 << column)
                old = next_states.get(new_mask, sp.Integer(0))
                next_states[new_mask] = reduce_qrho(old + value * entry)
        states = next_states
    return reduce_qrho(states.get((1 << size) - 1, sp.Integer(0)))


def feature_row(terminal_row: dict[str, sp.Expr]) -> list[sp.Expr]:
    return [
        terminal_row.get("1", 0) - terminal_row.get("3", 0),
        terminal_row.get("2", 0) - terminal_row.get("4", 0),
        terminal_row.get("5", 0),
        terminal_row.get("a", 0),
        terminal_row.get("b", 0),
    ]


TAU = -5 - 2 * RHO / 21
C_VALUE = 230 + 104 * RHO / 7
BETA = 1 + 16 * RHO / 21

COLOUR_ZERO_TERMINAL_ROWS = {
    "f1": {"1": 1},
    "f2": {"2": 1},
    "ell": {"3": 1, "5": 1, "a": 1},
    "h3": {"3": 1, "b": -RHO},
    "h4": {"4": 1, "b": TAU},
    "h5": {"5": 1, "b": C_VALUE},
    "ha": {"a": 1, "b": BETA},
}

COLOUR_TWO_TERMINAL_ROWS = {
    "z_*": {"5": sp.Rational(1, 7)},
    "z_1": {"1": 1, "3": 1},
    "z_2": {"2": 1, "4": 1},
    "z_3": {"1": 1, "3": 1, "a": 1},
    "z_4": {"2": 1, "4": 1, "b": 1},
    "z_5": {"1": 1, "3": 1},
    "z_6": {"2": 1, "4": 1},
}

L0 = {name: feature_row(row) for name, row in COLOUR_ZERO_TERMINAL_ROWS.items()}
L2 = {name: feature_row(row) for name, row in COLOUR_TWO_TERMINAL_ROWS.items()}


EXPECTED_L0 = {
    "f1": [1, 0, 0, 0, 0],
    "f2": [0, 1, 0, 0, 0],
    "ell": [-1, 0, 1, 1, 0],
    "h3": [-1, 0, 0, 0, -RHO],
    "h4": [0, -1, 0, 0, TAU],
    "h5": [0, 0, 1, 0, C_VALUE],
    "ha": [0, 0, 0, 1, BETA],
}

EXPECTED_L2 = {
    "z_*": [0, 0, sp.Rational(1, 7), 0, 0],
    "z_1": [0, 0, 0, 0, 0],
    "z_2": [0, 0, 0, 0, 0],
    "z_3": [0, 0, 0, 1, 0],
    "z_4": [0, 0, 0, 0, 1],
    "z_5": [0, 0, 0, 0, 0],
    "z_6": [0, 0, 0, 0, 0],
}


def row_minor(row_names: tuple[str, ...], columns: tuple[str, ...]) -> sp.Expr:
    matrix = [
        [L0[name][FEATURES.index(column)] for column in columns]
        for name in row_names
    ]
    return permanent(matrix)


def anchored_minor(
    pair: tuple[str, str],
    roles: dict[str, str],
    selected: frozenset[str],
) -> sp.Expr:
    rows = pair + tuple(roles[role] for role in ("5", "a", "b") if role not in selected)
    columns = tuple(column for column in FEATURES if column not in selected)
    return row_minor(rows, columns)


def norm_linear(value: sp.Expr) -> sp.Rational:
    reduced = sp.Poly(reduce_qrho(value), RHO)
    a = reduced.nth(0)
    b = reduced.nth(1)
    return sp.factor(a**2 - 21 * b**2)


def main() -> None:
    assert L0 == EXPECTED_L0
    assert L2 == EXPECTED_L2
    assert norm_linear(TAU) == sp.Rational(521, 21)

    # Exactly one B-support row: expand through that unique B entry.  The
    # four-column values depend only on the omitted H row.
    expected_one_y = {
        "f1": -231 - 307 * RHO / 21,
        "ell": -RHO,
        "h3": 231 + 328 * RHO / 21,
        "h5": -RHO,
        "ha": -RHO,
    }
    for omitted, expected in expected_one_y.items():
        four_h = tuple(row for row in H if row != omitted)
        base = row_minor(four_h, ("A", "5", "a", "b"))
        assert reduce_qrho(base - expected) == 0
        assert norm_linear(base) != 0
        assert reduce_qrho(row_minor(("f2",) + four_h, FEATURES) - base) == 0
        assert reduce_qrho(row_minor(("h4",) + four_h, FEATURES) + base) == 0

    # Both B-support rows: the full minor vanishes exactly for H-triples
    # containing f1,h3; every other value is +/-tau.
    zero_triples: set[frozenset[str]] = set()
    for triple in combinations(H, 3):
        value = row_minor(Y + triple, FEATURES)
        if value == 0:
            zero_triples.add(frozenset(triple))
        else:
            assert reduce_qrho(value - TAU) == 0 or reduce_qrho(value + TAU) == 0
    expected_zero_triples = {
        frozenset(("f1", "h3", "ell")),
        frozenset(("f1", "h3", "h5")),
        frozenset(("f1", "h3", "ha")),
    }
    assert zero_triples == expected_zero_triples

    # The only exceptional local configuration is R={f1,h3,q}.  Check the
    # role-sensitive identities used in the non-enumerative case proof.
    for q in ("ell", "h5", "ha"):
        exceptional_rows = ("f1", "h3", q)
        for role_order in permutations(exceptional_rows):
            roles = dict(zip(("5", "a", "b"), role_order, strict=True))
            row_b = roles["b"]
            a_coordinate = L0[row_b][FEATURES.index("A")]
            if a_coordinate != 0:
                value = anchored_minor(Y, roles, frozenset(("5", "a")))
                assert reduce_qrho(value - TAU * a_coordinate) == 0
            elif row_b == "h5":
                row_5 = roles["5"]
                assert row_5 in ("f1", "h3")
                value = anchored_minor(Y, roles, frozenset(("a",)))
                assert reduce_qrho(value - TAU * L0[row_5][0]) == 0
            else:
                assert row_b == "ha"
                row_a = roles["a"]
                assert row_a in ("f1", "h3")
                value = anchored_minor(Y, roles, frozenset(("5",)))
                assert reduce_qrho(value - TAU * L0[row_a][0]) == 0
            assert value != 0

    print("transformed colour-0 and colour-2 row structures: exact")
    print("one-Y full-minor table: exact and nonzero")
    print("two-Y full-minor zero criterion: exactly {f1,h3} subset J")
    print("exceptional anchored identities: exact and nonzero")
    print("alignment/word/rectangle enumeration: not used")
    print("arbitrary-alignment fixed c0/c2 completion: EXCLUDED")


if __name__ == "__main__":
    main()
