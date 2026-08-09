"""Independent Q(sqrt(21)) audit of the aligned degree-three obstruction.

This file imports neither SymPy nor a project verifier.  It uses a six-variable
polynomial dictionary over exact quadratic-field pairs and checks the explicit
three-face unit-ideal certificate.
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
        norm = other.norm()
        assert norm != 0
        return self * Q21(other.rational / norm, -other.radical / norm)

    def norm(self) -> Fraction:
        return self.rational**2 - 21 * self.radical**2


ZERO = Q21()
ONE = Q21(1)
RHO = Q21(0, 1)
ALPHA = Q21(5, Fraction(2, 21))
BETA = Q21(1, Fraction(16, 21))
CAPITAL_C = Q21(230, Fraction(104, 7))
DELTA = Q21(6, Fraction(1, 21))
P = tuple("12345ab")
PARAMETER_NAMES = ("u", "v", "w", "p", "q", "t")
ZERO_MONOMIAL = (0,) * 6


@dataclass(frozen=True)
class Polynomial:
    terms: tuple[tuple[tuple[int, ...], Q21], ...]

    @staticmethod
    def from_dict(terms: dict[tuple[int, ...], Q21]) -> Polynomial:
        cleaned = tuple(sorted((monomial, value) for monomial, value in terms.items() if value != ZERO))
        return Polynomial(cleaned)

    @staticmethod
    def scalar(value=0) -> Polynomial:
        value = Q21.coerce(value)
        return Polynomial.from_dict({ZERO_MONOMIAL: value})

    @staticmethod
    def variable(index: int) -> Polynomial:
        monomial = [0] * 6
        monomial[index] = 1
        return Polynomial.from_dict({tuple(monomial): ONE})

    def as_dict(self) -> dict[tuple[int, ...], Q21]:
        return dict(self.terms)

    def __add__(self, other) -> Polynomial:
        if not isinstance(other, Polynomial):
            other = Polynomial.scalar(other)
        result = self.as_dict()
        for monomial, value in other.terms:
            result[monomial] = result.get(monomial, ZERO) + value
        return Polynomial.from_dict(result)

    __radd__ = __add__

    def __neg__(self) -> Polynomial:
        return Polynomial.from_dict({monomial: -value for monomial, value in self.terms})

    def __sub__(self, other) -> Polynomial:
        return self + (-other)

    def __mul__(self, other) -> Polynomial:
        if not isinstance(other, Polynomial):
            return self.scale(other)
        result: dict[tuple[int, ...], Q21] = {}
        for left_monomial, left_value in self.terms:
            for right_monomial, right_value in other.terms:
                monomial = tuple(
                    left + right for left, right in zip(left_monomial, right_monomial, strict=True)
                )
                result[monomial] = result.get(monomial, ZERO) + left_value * right_value
        return Polynomial.from_dict(result)

    __rmul__ = __mul__

    def scale(self, scalar) -> Polynomial:
        scalar = Q21.coerce(scalar)
        return Polynomial.from_dict({monomial: scalar * value for monomial, value in self.terms})

    def coefficient(self, exponents: tuple[int, ...]) -> Q21:
        return self.as_dict().get(exponents, ZERO)

    def degree(self) -> int:
        return max((sum(monomial) for monomial, _ in self.terms), default=-1)


U, V, W, X_P, X_Q, T = (Polynomial.variable(index) for index in range(6))


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


def parametrized_edges() -> dict[tuple[int, int], Polynomial]:
    edges = {
        (2, 4): U,
        (2, 5): V,
        (2, 6): W,
        (3, 4): X_P,
        (3, 5): X_Q,
        (3, 6): T,
        (0, 1): X_P.scale(CAPITAL_C / (7 * ALPHA)) - X_Q.scale(Fraction(1, 7)),
        (0, 4): Polynomial.scalar(DELTA / 7) - X_P.scale(CAPITAL_C / (7 * ALPHA)),
        (0, 5): (Polynomial.scalar(DELTA) - X_Q).scale(CAPITAL_C / (7 * ALPHA)),
        (0, 6): T.scale(CAPITAL_C / (7 * ALPHA))
        + Polynomial.scalar((BETA * DELTA + 1 + RHO) / (7 * ALPHA)),
        (1, 2): Polynomial.scalar(-1) - U + V.scale(ALPHA / CAPITAL_C),
        (1, 3): X_P - X_Q.scale(ALPHA / CAPITAL_C),
        (2, 3): Polynomial.scalar(1),
        (4, 5): Polynomial.scalar(Q21(-6, Fraction(-1, 21))),
        (4, 6): Polynomial.scalar(Q21(0, Fraction(1, 21))),
        (5, 6): Polynomial.scalar(Q21(1, Fraction(22, 21))),
    }
    for left in range(7):
        for right in range(left + 1, 7):
            edges.setdefault((left, right), Polynomial.scalar())
    return edges


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


def four_core_hafnian(vertices: tuple[int, int, int, int], edges) -> Polynomial:
    first, second, third, fourth = vertices

    def edge(left: int, right: int) -> Polynomial:
        return edges[min(left, right), max(left, right)]

    return (
        edge(first, second) * edge(third, fourth)
        + edge(first, third) * edge(second, fourth)
        + edge(first, fourth) * edge(second, third)
    )


def degree_three_response(face: str, matrix, edges, permanent) -> Polynomial:
    columns = tuple(P.index(terminal) for terminal in face)
    total = Polynomial.scalar()
    for used_rows in combinations(range(7), 3):
        remaining = tuple(index for index in range(7) if index not in used_rows)
        total += four_core_hafnian(remaining, edges).scale(permanent(used_rows, columns))
    return total


def main() -> None:
    assert RHO * RHO == Q21(21)
    assert DELTA.norm() == Fraction(755, 21)
    assert ALPHA.norm() == Fraction(521, 21)
    assert CAPITAL_C.norm() == Fraction(2364964, 49)

    matrix = incidence_matrix()
    edges = parametrized_edges()
    permanent = permanent_evaluator(matrix)
    faces = tuple("".join(face) for face in combinations(P, 3))
    responses = {face: degree_three_response(face, matrix, edges, permanent) for face in faces}
    assert len(responses) == 35
    assert sum(response != Polynomial.scalar() for response in responses.values()) == 24
    assert all(response.degree() <= 2 for response in responses.values())

    p_monomial = (0, 0, 0, 1, 0, 0)
    q_monomial = (0, 0, 0, 0, 1, 0)
    pq_monomial = (0, 0, 0, 1, 1, 0)
    f124 = responses["124"].scale(ONE / responses["124"].coefficient(q_monomial))
    f125 = responses["125"].scale(ONE / responses["125"].coefficient(p_monomial))
    f12a = responses["12a"].scale(ONE / responses["12a"].coefficient(pq_monomial))

    kappa = DELTA * ALPHA / CAPITAL_C
    assert f124 == X_Q - DELTA
    assert f125 == X_P
    assert f12a == X_Q * (X_P - kappa)

    certificate = X_Q * f125 - f12a - f124.scale(kappa)
    assert certificate == Polynomial.scalar(DELTA * kappa)
    unit = certificate.scale(CAPITAL_C / (DELTA * DELTA * ALPHA))
    assert unit == Polynomial.scalar(1)

    assert {face: "".join(terminal for terminal in P if terminal not in face) for face in f124_faces()} == {
        "124": "35ab",
        "125": "34ab",
        "12a": "345b",
    }

    print("independent Q21 aligned degree-three audit: PASS")
    print("degree3_faces=35 nonzero=24")
    print("three_face_unit_certificate=1")
    print("algebraic_closure_solutions=0")
    print("parameter_searches=0")


def f124_faces() -> tuple[str, str, str]:
    return ("124", "125", "12a")


if __name__ == "__main__":
    main()
