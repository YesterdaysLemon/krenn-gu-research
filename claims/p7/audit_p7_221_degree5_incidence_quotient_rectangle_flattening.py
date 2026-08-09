"""Independent exact audit of the incidence-quotient rectangle theorem.

No SymPy or project verifier is imported.  Q(sqrt(21)) arithmetic reconstructs
the Wick rectangle, a tiny polynomial ring checks the universal rank-one
minor, and a recursive permanent checks the sharp sparse failure model.
"""

from __future__ import annotations

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
    def coerce(value) -> Q21:
        return value if isinstance(value, Q21) else Q21(value)

    def __add__(self, other) -> Q21:
        other = self.coerce(other)
        return Q21(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self) -> Q21:
        return Q21(-self.rational, -self.radical)

    def __sub__(self, other) -> Q21:
        return self + (-self.coerce(other))

    def __rsub__(self, other) -> Q21:
        return self.coerce(other) - self

    def __mul__(self, other) -> Q21:
        other = self.coerce(other)
        return Q21(
            self.rational * other.rational + 21 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def __truediv__(self, other) -> Q21:
        other = self.coerce(other)
        norm = other.rational**2 - 21 * other.radical**2
        assert norm != 0
        return self * Q21(other.rational / norm, -other.radical / norm)


ZERO = Q21()
ONE = Q21(1)
RHO = Q21(0, 1)
KAPPA = ONE + Q21(22) / RHO
P = tuple("12345ab")
P_SET = frozenset(P)
RECTANGLE = {
    frozenset("125ab"): ONE,
    frozenset("145ab"): Q21(-1),
    frozenset("235ab"): Q21(-1),
    frozenset("345ab"): ONE,
}


def formal_ledger() -> dict[int, dict[frozenset[str], Q21]]:
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(P, size)
        if not (size == 2 and frozenset(deletion) == frozenset("ab"))
    ]
    ledger = {colour: {deletion: ZERO for deletion in prescribed} for colour in range(3)}

    def assign(deletion: str, colour: int, value=ONE) -> None:
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


def minus_terminal_block() -> dict[frozenset[str], Q21]:
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


def hafnian_evaluator(matrix: dict[frozenset[str], Q21]):
    @cache
    def hafnian(vertices: tuple[str, ...]) -> Q21:
        if not vertices:
            return ONE
        if len(vertices) % 2:
            return ZERO
        first = vertices[0]
        total = ZERO
        for position, second in enumerate(vertices[1:], 1):
            total += matrix.get(frozenset((first, second)), ZERO) * hafnian(
                vertices[1:position] + vertices[position + 1 :]
            )
        return total

    return lambda vertices: hafnian(tuple(sorted(vertices)))


def formal_wick_values() -> dict[frozenset[str], tuple[Q21, ...]]:
    ledger = formal_ledger()
    hafnian = hafnian_evaluator(minus_terminal_block())
    values = {}
    for face in RECTANGLE:
        colours = []
        ordered_face = tuple(terminal for terminal in P if terminal in face)
        for colour in range(3):
            total = ZERO
            for even_size in (0, 2, 4):
                for edge_tuple in combinations(ordered_face, even_size):
                    edge_set = frozenset(edge_tuple)
                    surviving = face - edge_set
                    total += hafnian(edge_set) * ledger[colour][P_SET - surviving]
            colours.append(total)
        values[face] = tuple(colours)
    return values


@dataclass(frozen=True)
class Polynomial:
    terms: tuple[tuple[tuple[int, ...], Q21], ...]

    @staticmethod
    def from_dict(terms: dict[tuple[int, ...], Q21]) -> Polynomial:
        cleaned = tuple(sorted((monomial, coefficient) for monomial, coefficient in terms.items() if coefficient != ZERO))
        return Polynomial(cleaned)

    @staticmethod
    def variable(index: int) -> Polynomial:
        exponent = [0] * 4
        exponent[index] = 1
        return Polynomial.from_dict({tuple(exponent): ONE})

    def __add__(self, other) -> Polynomial:
        collected = dict(self.terms)
        for monomial, coefficient in other.terms:
            collected[monomial] = collected.get(monomial, ZERO) + coefficient
        return Polynomial.from_dict(collected)

    def __neg__(self) -> Polynomial:
        return Polynomial.from_dict({monomial: -coefficient for monomial, coefficient in self.terms})

    def __sub__(self, other) -> Polynomial:
        return self + (-other)

    def __mul__(self, other) -> Polynomial:
        collected: dict[tuple[int, ...], Q21] = {}
        for left_monomial, left_coefficient in self.terms:
            for right_monomial, right_coefficient in other.terms:
                monomial = tuple(left + right for left, right in zip(left_monomial, right_monomial, strict=True))
                collected[monomial] = collected.get(monomial, ZERO) + left_coefficient * right_coefficient
        return Polynomial.from_dict(collected)


POLY_ZERO = Polynomial.from_dict({})


def matrix_rank(rows: list[list[Q21]]) -> int:
    matrix = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column] != ZERO), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column] != ZERO:
                multiplier = matrix[row][column]
                matrix[row] = [
                    value - multiplier * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivot_row += 1
    return pivot_row


def permanent_evaluator(matrix: tuple[tuple[Q21, ...], ...]):
    @cache
    def permanent(rows: tuple[int, ...], columns: tuple[int, ...]) -> Q21:
        if not rows:
            return ONE
        first = rows[0]
        total = ZERO
        for position, column in enumerate(columns):
            total += matrix[first][column] * permanent(
                rows[1:], columns[:position] + columns[position + 1 :]
            )
        return total

    return permanent


def main() -> None:
    assert RHO * RHO == Q21(21)
    values = formal_wick_values()
    expected = {
        frozenset("125ab"): (RHO - 2, ZERO, (ONE + RHO) / 7),
        frozenset("145ab"): (ZERO, ZERO, (ONE + RHO) / 7),
        frozenset("235ab"): (ZERO, ZERO, (ONE + RHO) / 7),
        frozenset("345ab"): (ZERO, RHO - 2, (ONE + RHO) / 7),
    }
    assert values == expected
    rectangle = tuple(
        sum(RECTANGLE[face] * values[face][colour] for face in RECTANGLE)
        for colour in range(3)
    )
    assert rectangle == (RHO - 2, RHO - 2, ZERO)

    # Nondegenerate formal flattening is diagonal and has rank two.
    formal = [[RHO - 2, ZERO], [ZERO, RHO - 2]]
    assert matrix_rank(formal) == 2

    # A generic physical quotient is an outer product.  The determinant
    # vanishes as a polynomial in four independent variables.
    x0, x1, y0, y1 = (Polynomial.variable(index) for index in range(4))
    physical_minor = (x0 * y0) * (x1 * y1) - (x0 * y1) * (x1 * y0)
    assert physical_minor == POLY_ZERO

    # Quotient killing e0 retains just one formal column.
    counter_a0 = [ZERO] * 6
    counter_a1 = [ZERO, ZERO, ZERO, ONE, ZERO, ZERO]
    counter_flattening = [
        [(RHO - 2) * counter_a0[row], (RHO - 2) * counter_a1[row]] for row in range(6)
    ]
    assert matrix_rank(counter_flattening) == 1

    incidence = [[ZERO for _ in range(7)] for _ in range(5)]
    for row, terminal, value in (
        (0, "1", RHO - 2),
        (1, "2", ONE),
        (2, "5", ONE),
        (3, "a", ONE),
        (4, "b", ONE),
    ):
        incidence[row][P.index(terminal)] = value
    permanent = permanent_evaluator(tuple(tuple(row) for row in incidence))
    permanents = {
        face: permanent(tuple(range(5)), tuple(P.index(terminal) for terminal in P if terminal in face))
        for face in RECTANGLE
    }
    assert permanents == {
        frozenset("125ab"): RHO - 2,
        frozenset("145ab"): ZERO,
        frozenset("235ab"): ZERO,
        frozenset("345ab"): ZERO,
    }
    assert sum(RECTANGLE[face] * permanents[face] for face in RECTANGLE) == RHO - 2

    print("independent Q21 incidence-quotient rectangle audit: PASS")
    print("formal_rectangle=(rho-2)(D0+D1)")
    print("generic_physical_outer_product_minor=0")
    print("formal_rank_if_independent=2")
    print("degenerate_countermodel_rank=1 selector_permanents=PASS")
    print("searches=0")


if __name__ == "__main__":
    main()
