"""Independent exact audit of the arbitrary-alignment row-type lemma.

No SymPy and no project verifier are imported.  Arithmetic is performed in
Q[rho]/(rho^2-21), and permanents use subset dynamic programming.  The audit
does not enumerate core alignments, mixed words, or face rectangles.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations


@dataclass(frozen=True)
class Quad:
    """Element a+b*rho with rho^2=21."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    @staticmethod
    def coerce(value: object) -> Quad:
        if isinstance(value, Quad):
            return value
        return Quad(Fraction(value))  # type: ignore[arg-type]

    def __add__(self, other: object) -> Quad:
        rhs = self.coerce(other)
        return Quad(self.a + rhs.a, self.b + rhs.b)

    __radd__ = __add__

    def __neg__(self) -> Quad:
        return Quad(-self.a, -self.b)

    def __sub__(self, other: object) -> Quad:
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> Quad:
        return self.coerce(other) - self

    def __mul__(self, other: object) -> Quad:
        rhs = self.coerce(other)
        return Quad(
            self.a * rhs.a + 21 * self.b * rhs.b,
            self.a * rhs.b + self.b * rhs.a,
        )

    __rmul__ = __mul__

    def norm(self) -> Fraction:
        return self.a * self.a - 21 * self.b * self.b

    def __bool__(self) -> bool:
        return self.a != 0 or self.b != 0


ZERO = Quad()
ONE = Quad(Fraction(1))
RHO = Quad(Fraction(0), Fraction(1))
TAU = Quad(Fraction(-5), Fraction(-2, 21))
C_VALUE = Quad(Fraction(230), Fraction(104, 7))
BETA = Quad(Fraction(1), Fraction(16, 21))

FEATURES = ("A", "B", "5", "a", "b")
H = ("f1", "ell", "h3", "h5", "ha")
Y = ("f2", "h4")

ROWS = {
    "f1": (ONE, ZERO, ZERO, ZERO, ZERO),
    "f2": (ZERO, ONE, ZERO, ZERO, ZERO),
    "ell": (-ONE, ZERO, ONE, ONE, ZERO),
    "h3": (-ONE, ZERO, ZERO, ZERO, -RHO),
    "h4": (ZERO, -ONE, ZERO, ZERO, TAU),
    "h5": (ZERO, ZERO, ONE, ZERO, C_VALUE),
    "ha": (ZERO, ZERO, ZERO, ONE, BETA),
}


def permanent(matrix: list[list[Quad]]) -> Quad:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    states = {0: ONE}
    for row in matrix:
        next_states: dict[int, Quad] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry:
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = next_states.get(new_mask, ZERO) + value * entry
        states = next_states
    return states.get((1 << size) - 1, ZERO)


def row_minor(row_names: tuple[str, ...], columns: tuple[str, ...]) -> Quad:
    return permanent(
        [
            [ROWS[name][FEATURES.index(column)] for column in columns]
            for name in row_names
        ]
    )


def anchored_minor(
    pair: tuple[str, str],
    roles: dict[str, str],
    selected: frozenset[str],
) -> Quad:
    row_names = pair + tuple(
        roles[role] for role in ("5", "a", "b") if role not in selected
    )
    columns = tuple(column for column in FEATURES if column not in selected)
    return row_minor(row_names, columns)


def main() -> None:
    assert TAU.norm() == Fraction(521, 21)

    expected_one_y = {
        "f1": Quad(Fraction(-231), Fraction(-307, 21)),
        "ell": -RHO,
        "h3": Quad(Fraction(231), Fraction(328, 21)),
        "h5": -RHO,
        "ha": -RHO,
    }
    expected_norms = {
        "f1": Fraction(1026332, 21),
        "ell": Fraction(-21),
        "h3": Fraction(1012997, 21),
        "h5": Fraction(-21),
        "ha": Fraction(-21),
    }
    for omitted, expected in expected_one_y.items():
        four_h = tuple(row for row in H if row != omitted)
        value = row_minor(four_h, ("A", "5", "a", "b"))
        assert value == expected
        assert value.norm() == expected_norms[omitted]
        assert row_minor(("f2",) + four_h, FEATURES) == value
        assert row_minor(("h4",) + four_h, FEATURES) == -value

    zero_triples: set[frozenset[str]] = set()
    for triple in combinations(H, 3):
        value = row_minor(Y + triple, FEATURES)
        if not value:
            zero_triples.add(frozenset(triple))
        else:
            assert value == TAU or value == -TAU
    assert zero_triples == {
        frozenset(("f1", "h3", "ell")),
        frozenset(("f1", "h3", "h5")),
        frozenset(("f1", "h3", "ha")),
    }

    for q in ("ell", "h5", "ha"):
        exceptional_rows = ("f1", "h3", q)
        for role_order in permutations(exceptional_rows):
            roles = dict(zip(("5", "a", "b"), role_order, strict=True))
            row_b = roles["b"]
            a_coordinate = ROWS[row_b][FEATURES.index("A")]
            if a_coordinate:
                value = anchored_minor(Y, roles, frozenset(("5", "a")))
                assert value == TAU * a_coordinate
            elif row_b == "h5":
                row_5 = roles["5"]
                assert row_5 in ("f1", "h3")
                value = anchored_minor(Y, roles, frozenset(("a",)))
                assert value == TAU * ROWS[row_5][0]
            else:
                assert row_b == "ha"
                row_a = roles["a"]
                assert row_a in ("f1", "h3")
                value = anchored_minor(Y, roles, frozenset(("5",)))
                assert value == TAU * ROWS[row_a][0]
            assert value

    print("AUDIT PASS")
    print("quadratic-pair row table and permanent calculations agree")
    print("full-minor case split and exceptional anchored identities agree")
    print("no alignment, mixed-word, or rectangle enumeration used")


if __name__ == "__main__":
    main()
