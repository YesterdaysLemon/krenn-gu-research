"""Independent Q(rho) audit of the fixed-chart four-face mixed circuit.

No SymPy or project verifier is imported.  Twelve symbolic core-edge
variables are represented by an exact affine coefficient vector.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache


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


ZERO = Q21()
ONE = Q21(1)
RHO = Q21(0, 1)
INV_RHO = Q21(0, Fraction(1, 21))
KAPPA = Q21(1, Fraction(22, 21))
P = ("1", "2", "3", "4", "5", "a", "b")
CROSS_PAIRS = tuple((left, right) for left in range(3) for right in range(3, 7))
CROSS_INDEX = {pair: index for index, pair in enumerate(CROSS_PAIRS)}


@dataclass(frozen=True)
class Affine:
    constant: Q21
    coefficients: tuple[Q21, ...]

    @staticmethod
    def scalar(value=0) -> Affine:
        return Affine(Q21.coerce(value), (ZERO,) * len(CROSS_PAIRS))

    @staticmethod
    def variable(pair: tuple[int, int]) -> Affine:
        coefficients = [ZERO] * len(CROSS_PAIRS)
        coefficients[CROSS_INDEX[pair]] = ONE
        return Affine(ZERO, tuple(coefficients))

    def __add__(self, other) -> Affine:
        if not isinstance(other, Affine):
            other = Affine.scalar(other)
        return Affine(
            self.constant + other.constant,
            tuple(left + right for left, right in zip(self.coefficients, other.coefficients, strict=True)),
        )

    __radd__ = __add__

    def __neg__(self) -> Affine:
        return Affine(-self.constant, tuple(-value for value in self.coefficients))

    def __sub__(self, other) -> Affine:
        return self + (-other)

    def scale(self, scalar) -> Affine:
        scalar = Q21.coerce(scalar)
        return Affine(
            scalar * self.constant,
            tuple(scalar * value for value in self.coefficients),
        )


def incidence_matrix() -> tuple[tuple[Q21, ...], ...]:
    matrix = [[ZERO for _ in range(7)] for _ in range(7)]

    def put(row: int, terminal: str, value=1) -> None:
        matrix[row][P.index(terminal)] = Q21.coerce(value)

    put(0, "5", Fraction(1, 7))
    put(1, "1")
    put(1, "3")
    put(2, "2")
    put(2, "4")
    put(3, "3")
    put(3, "b", -RHO)
    put(4, "4")
    put(4, "b", Q21(-5, Fraction(-2, 21)))
    put(5, "5")
    put(5, "b", Q21(230, Fraction(104, 7)))
    put(6, "a")
    put(6, "b", Q21(1, Fraction(16, 21)))
    return tuple(tuple(row) for row in matrix)


def core_edges() -> dict[tuple[int, int], Affine]:
    fixed = {
        (1, 2): ONE,
        (3, 5): RHO,
        (4, 5): -6 - INV_RHO,
        (4, 6): INV_RHO,
        (5, 6): KAPPA,
    }
    result: dict[tuple[int, int], Affine] = {}
    for left in range(7):
        for right in range(left + 1, 7):
            pair = (left, right)
            if pair in CROSS_INDEX:
                result[pair] = Affine.variable(pair)
            else:
                result[pair] = Affine.scalar(fixed.get(pair, ZERO))
    return result


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


def response(
    survivor_face: str,
    edges: dict[tuple[int, int], Affine],
    permanent,
) -> Affine:
    columns = tuple(P.index(terminal) for terminal in survivor_face)
    total = Affine.scalar()
    for left in range(7):
        for right in range(left + 1, 7):
            rows = tuple(index for index in range(7) if index not in (left, right))
            total += edges[left, right].scale(permanent(rows, columns))
    return total


def main() -> None:
    assert RHO * RHO == Q21(21)
    assert INV_RHO * RHO == ONE
    permanent = permanent_evaluator(incidence_matrix())
    edges = core_edges()
    faces = {name: response(name, edges, permanent) for name in ("125ab", "145ab", "235ab", "345ab")}

    circuit = faces["125ab"] - faces["145ab"] - faces["235ab"] + faces["345ab"]
    assert all(coefficient == ZERO for coefficient in circuit.coefficients)
    target = Q21(Fraction(230, 7), Fraction(104, 49))
    assert circuit.constant == target
    assert target == Q21.coerce(Fraction(2, 49)) * Q21(805, 52)
    norm = 805**2 - 21 * 52**2
    assert norm == 591241
    assert norm > 0

    assert {face: "".join(p for p in P if p not in face) for face in faces} == {
        "125ab": "34",
        "145ab": "23",
        "235ab": "14",
        "345ab": "12",
    }

    print("independent Q21 four-face mixed-circuit audit: PASS")
    print("symbolic_cross_colour_variables=12 all_cancel")
    print("constant=230/7+(104/49)*rho != 0")
    print("candidate_searches=0")


if __name__ == "__main__":
    main()
