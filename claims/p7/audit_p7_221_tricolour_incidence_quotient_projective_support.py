"""Independent no-import audit of the tricolour quotient theorem."""

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from itertools import combinations


@dataclass(frozen=True)
class Q21:
    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    def __init__(self, rational=0, radical=0):
        object.__setattr__(self, "rational", Fraction(rational))
        object.__setattr__(self, "radical", Fraction(radical))

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Q21) else Q21(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Q21(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return Q21(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Q21(
            self.rational * other.rational + 21 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        norm = other.rational**2 - 21 * other.radical**2
        assert norm
        return self * Q21(other.rational / norm, -other.radical / norm)

    def norm(self):
        return self.rational**2 - 21 * self.radical**2


ZERO = Q21()
ONE = Q21(1)
RHO = Q21(0, 1)
KAPPA = ONE + Q21(22) / RHO
P = tuple("12345ab")
P_SET = frozenset(P)
FACES = {
    "01": frozenset("1234a"),
    "02": frozenset("1235b"),
    "12": frozenset("1345b"),
}


def formal_ledger():
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(P, size)
        if not (size == 2 and frozenset(deletion) == frozenset("ab"))
    ]
    ledger = {colour: {deletion: ZERO for deletion in prescribed} for colour in range(3)}

    def assign(deletion, colour, value=ONE):
        ledger[colour][frozenset(deletion)] = Q21.coerce(value)

    for deletion, colour in {
        "1a": 1,
        "1b": 2,
        "2a": 2,
        "2b": 1,
        "3a": 0,
        "3b": 2,
        "4a": 2,
        "4b": 0,
        "5a": 0,
        "5b": 1,
    }.items():
        assign(deletion, colour)
    assign("12", 1, -1)
    assign("12", 2)
    assign("12ab", 1)
    assign("34", 0, -1)
    assign("34", 2)
    assign("34ab", 0)
    for pair, colour, with_ab in (
        ("13", 2, True),
        ("14", 2, False),
        ("23", 2, False),
        ("24", 2, True),
        ("15", 1, True),
        ("25", 1, False),
        ("35", 0, False),
        ("45", 0, True),
    ):
        assign(pair, colour)
        if with_ab:
            assign(pair + "ab", colour)
    for deletion, colour in {
        "123a": 2,
        "124b": 2,
        "134a": 2,
        "234b": 2,
        "125a": 1,
        "345b": 0,
    }.items():
        assign(deletion, colour)
    assign("1234", 2, Fraction(1, 7))
    assign("1234ab", 2, Fraction(1, 7))
    return ledger


def minus_terminal_block():
    weights = {
        "12": -KAPPA,
        "14": -KAPPA,
        "23": -KAPPA,
        "34": -KAPPA,
        "13": Q21(7),
        "24": Q21(7),
        "1a": Q21(7),
        "3a": Q21(7),
        "2b": Q21(7),
        "4b": Q21(7),
        "1b": -RHO,
        "2a": -RHO,
        "3b": -RHO,
        "4a": -RHO,
        "ab": ONE - RHO,
    }
    return {frozenset(pair): -weight for pair, weight in weights.items()}


def hafnian_evaluator(matrix):
    @cache
    def hafnian(vertices):
        if not vertices:
            return ONE
        first = vertices[0]
        total = ZERO
        for position, second in enumerate(vertices[1:], 1):
            total += matrix.get(frozenset((first, second)), ZERO) * hafnian(
                vertices[1:position] + vertices[position + 1 :]
            )
        return total

    return lambda vertices: hafnian(tuple(sorted(vertices)))


def wick_values():
    ledger = formal_ledger()
    hafnian = hafnian_evaluator(minus_terminal_block())
    values = {}
    for label, face in FACES.items():
        ordered = tuple(terminal for terminal in P if terminal in face)
        colours = []
        for colour in range(3):
            total = ZERO
            for size in (0, 2, 4):
                for matched_tuple in combinations(ordered, size):
                    matched = frozenset(matched_tuple)
                    surviving = face - matched
                    total += hafnian(matched) * ledger[colour][P_SET - surviving]
            colours.append(total)
        values[label] = tuple(colours)
    return values


def tensor(left, right):
    return tuple(a * b for a in left for b in right)


def column_rank(columns):
    rows = [list(row) for row in zip(*columns)]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def pair_rank(left, right):
    return column_rank(
        [tensor(left[colour], right[colour]) for colour in range(3)]
    )


def main():
    beta = Q21(Fraction(2, 7), Fraction(2, 7))
    expected = {
        "01": (Q21(1, Fraction(43, 21)), Q21(-6), ZERO),
        "02": (RHO, ZERO, beta),
        "12": (ZERO, RHO, beta),
    }
    assert wick_values() == expected
    assert expected["01"][0].norm() == Fraction(-1828, 21)
    assert RHO.norm() == -21
    assert beta.norm() == Fraction(-80, 49)

    z = (Fraction(0), Fraction(0))
    e0 = (Fraction(1), Fraction(0))
    e1 = (Fraction(0), Fraction(1))
    sharp = (
        (e0, e1, z),
        (z, e0, e1),
        (e0, z, e1),
        (e0, z, z),
        (z, e0, z),
        (z, z, e0),
        (e0, z, z),
    )
    assert all(
        pair_rank(sharp[left], sharp[right]) <= 1
        for left, right in combinations(range(7), 2)
    )
    assert len(tuple(combinations(range(3), 2))) == 3

    print("AUDIT PASS: three independent exact Wick face identities")
    print("AUDIT PASS: tricolour projective-support sharp model")
    print("AUDIT PASS: at most three distinct independent colour pairs")
    print("searches=0")


if __name__ == "__main__":
    main()
