"""Independent Q(sqrt(21)) audit of the aligned-core affine completion.

This file imports neither SymPy nor the primary verifier.  It checks the one
fixed 20x12 system, its six-parameter solution, and one degree-one extension.
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
ALPHA = Q21(5, Fraction(2, 21))
BETA = Q21(1, Fraction(16, 21))
CAPITAL_C = Q21(230, Fraction(104, 7))
DELTA = Q21(6, Fraction(1, 21))
P = tuple("12345ab")
GROUP_TWO = (0, 2, 3)
GROUP_ZERO = (1, 4, 5, 6)
CROSS_PAIRS = tuple((left, right) for left in GROUP_TWO for right in GROUP_ZERO)
CROSS_INDEX = {pair: index for index, pair in enumerate(CROSS_PAIRS)}
FACES = tuple("".join(face) for face in combinations(P, 5) if "".join(face) != "12345")
FREE_PAIRS = ((2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6))
FREE_INDEX = {pair: index for index, pair in enumerate(FREE_PAIRS)}


@dataclass(frozen=True)
class Affine6:
    constant: Q21
    coefficients: tuple[Q21, ...]

    @staticmethod
    def scalar(value=0) -> Affine6:
        return Affine6(Q21.coerce(value), (ZERO,) * 6)

    @staticmethod
    def variable(pair: tuple[int, int]) -> Affine6:
        coefficients = [ZERO] * 6
        coefficients[FREE_INDEX[pair]] = ONE
        return Affine6(ZERO, tuple(coefficients))

    def __add__(self, other) -> Affine6:
        if not isinstance(other, Affine6):
            other = Affine6.scalar(other)
        return Affine6(
            self.constant + other.constant,
            tuple(left + right for left, right in zip(self.coefficients, other.coefficients, strict=True)),
        )

    __radd__ = __add__

    def __neg__(self) -> Affine6:
        return Affine6(-self.constant, tuple(-value for value in self.coefficients))

    def __sub__(self, other) -> Affine6:
        return self + (-other)

    def scale(self, scalar) -> Affine6:
        scalar = Q21.coerce(scalar)
        return Affine6(
            scalar * self.constant,
            tuple(scalar * value for value in self.coefficients),
        )

    def evaluate(self, values: dict[tuple[int, int], Q21]) -> Q21:
        return self.constant + sum(
            coefficient * values[pair]
            for pair, coefficient in zip(FREE_PAIRS, self.coefficients, strict=True)
        )


def incidence_matrix() -> tuple[tuple[Q21, ...], ...]:
    matrix = [[ZERO for _ in range(7)] for _ in range(7)]

    def put(row: int, terminal: str, value=1) -> None:
        matrix[row][P.index(terminal)] = Q21.coerce(value)

    put(0, "5", Fraction(1, 7))
    put(1, "2")
    put(2, "1")
    put(2, "3")
    put(3, "2")
    put(3, "4")
    put(4, "4")
    put(4, "b", -ALPHA)
    put(5, "5")
    put(5, "b", CAPITAL_C)
    put(6, "a")
    put(6, "b", BETA)
    return tuple(tuple(row) for row in matrix)


FIXED_EDGES = {
    (2, 3): ONE,
    (4, 5): Q21(-6, Fraction(-1, 21)),
    (4, 6): Q21(0, Fraction(1, 21)),
    (5, 6): Q21(1, Fraction(22, 21)),
}


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


def affine_system(permanent):
    coefficient_rows: list[list[Q21]] = []
    constants: list[Q21] = []
    for face in FACES:
        columns = tuple(P.index(terminal) for terminal in face)
        row = [ZERO] * 12
        constant = ZERO
        for left in range(7):
            for right in range(left + 1, 7):
                remaining = tuple(index for index in range(7) if index not in (left, right))
                multiplier = permanent(remaining, columns)
                pair = (left, right)
                oriented = pair if pair in CROSS_INDEX else (right, left)
                if oriented in CROSS_INDEX:
                    row[CROSS_INDEX[oriented]] += multiplier
                else:
                    constant += FIXED_EDGES.get(pair, ZERO) * multiplier
        coefficient_rows.append(row)
        constants.append(constant)
    return coefficient_rows, constants


def matrix_rank(rows: list[list[Q21]]) -> int:
    matrix = [row[:] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count) if matrix[row][column] != ZERO), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(row_count):
            if row != pivot_row and matrix[row][column] != ZERO:
                multiplier = matrix[row][column]
                matrix[row] = [
                    value - multiplier * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def parametrized_edges() -> dict[tuple[int, int], Affine6]:
    free = {pair: Affine6.variable(pair) for pair in FREE_PAIRS}
    x24, x25, _x26, x34, x35, x36 = (free[pair] for pair in FREE_PAIRS)
    edges = dict(free)
    edges[0, 1] = x34.scale(CAPITAL_C / (7 * ALPHA)) - x35.scale(Fraction(1, 7))
    edges[0, 4] = Affine6.scalar(DELTA / 7) - x34.scale(CAPITAL_C / (7 * ALPHA))
    edges[0, 5] = (Affine6.scalar(DELTA) - x35).scale(CAPITAL_C / (7 * ALPHA))
    edges[0, 6] = x36.scale(CAPITAL_C / (7 * ALPHA)) + Affine6.scalar(
        (BETA * DELTA + 1 + RHO) / (7 * ALPHA)
    )
    edges[2, 1] = Affine6.scalar(-1) - x24 + x25.scale(ALPHA / CAPITAL_C)
    edges[3, 1] = x34 - x35.scale(ALPHA / CAPITAL_C)
    return edges


def check_parametrization(
    coefficient_rows: list[list[Q21]],
    constants: list[Q21],
    edges: dict[tuple[int, int], Affine6],
) -> None:
    ordered = [edges[pair] for pair in CROSS_PAIRS]
    for row, constant in zip(coefficient_rows, constants, strict=True):
        response = Affine6.scalar(constant)
        for coefficient, edge in zip(row, ordered, strict=True):
            response += edge.scale(coefficient)
        assert response == Affine6.scalar()


def degree_one_response(
    terminal: str,
    incidence: tuple[tuple[Q21, ...], ...],
    edges: dict[tuple[int, int], Q21],
) -> Q21:
    @cache
    def hafnian(vertices: tuple[int, ...]) -> Q21:
        if not vertices:
            return ONE
        first = vertices[0]
        total = ZERO
        for position, second in enumerate(vertices[1:], 1):
            pair = (min(first, second), max(first, second))
            total += edges.get(pair, ZERO) * hafnian(
                vertices[1:position] + vertices[position + 1 :]
            )
        return total

    column = P.index(terminal)
    return sum(
        incidence[row][column] * hafnian(tuple(index for index in range(7) if index != row))
        for row in range(7)
    )


def main() -> None:
    assert RHO * RHO == Q21(21)
    assert len(FACES) == 20 and len(CROSS_PAIRS) == 12
    incidence = incidence_matrix()
    permanent = permanent_evaluator(incidence)
    coefficients, constants = affine_system(permanent)
    assert matrix_rank(coefficients) == 6
    augmented = [row + [-constant] for row, constant in zip(coefficients, constants, strict=True)]
    assert matrix_rank(augmented) == 6

    parametrization = parametrized_edges()
    check_parametrization(coefficients, constants, parametrization)

    free_point = {
        (2, 4): Q21(Fraction(337, 506778), Fraction(-41206, 1773723)),
        (2, 5): Q21(Fraction(23005, 521), Fraction(11638, 10941)),
        (2, 6): ZERO,
        (3, 4): ZERO,
        (3, 5): ZERO,
        (3, 6): ONE,
    }
    numeric_edges = {pair: expression.evaluate(free_point) for pair, expression in parametrization.items()}
    numeric_edges.update(FIXED_EDGES)
    for terminal in P:
        assert degree_one_response(terminal, incidence, numeric_edges) == ZERO

    print("independent Q21 aligned-core affine audit: PASS")
    print("degree5_rank=6 augmented_rank=6 free_parameters=6")
    print("degree1_exact_extension=PASS")
    print("alignment_searches=0")


if __name__ == "__main__":
    main()
