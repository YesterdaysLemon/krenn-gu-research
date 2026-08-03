"""Independent audit of the four-face binary GHZ physical countermodel.

The audit uses only the standard library and exact arithmetic in
Q[rho]/(rho^2-21).  It imports neither SymPy nor the primary verifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


@dataclass(frozen=True)
class Quad:
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

    def __bool__(self) -> bool:
        return self.a != 0 or self.b != 0


ZERO = Quad()
ONE = Quad(Fraction(1))
RHO = Quad(Fraction(0), Fraction(1))
C_VALUE = RHO - 2
T_VALUE = (ONE + RHO) * Fraction(1, 7)
KAPPA = ONE + RHO * Fraction(22, 21)

P = ("1", "2", "3", "4", "5", "a", "b")
Q = frozenset(("a", "b"))
FACES = ("125ab", "145ab", "235ab", "345ab")


def formal_ledger() -> dict[int, dict[frozenset[str], Quad]]:
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(P, size)
        if not (size == 2 and frozenset(deletion) == Q)
    ]
    ledger = {
        colour: {deletion: ZERO for deletion in prescribed} for colour in range(3)
    }

    def assign(deletion: str, colour: int, value: object = 1) -> None:
        ledger[colour][frozenset(deletion)] = Quad.coerce(value)

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
    for pair, colour, with_q in (
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
        if with_q:
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


def terminal_block() -> dict[frozenset[str], Quad]:
    weights = {
        "12": -KAPPA,
        "14": -KAPPA,
        "23": -KAPPA,
        "34": -KAPPA,
        "13": 7,
        "24": 7,
        "1a": 7,
        "3a": 7,
        "2b": 7,
        "4b": 7,
        "1b": -RHO,
        "2a": -RHO,
        "3b": -RHO,
        "4a": -RHO,
        "ab": ONE - RHO,
    }
    return {frozenset(pair): Quad.coerce(value) for pair, value in weights.items()}


LEDGER = formal_ledger()
M = terminal_block()


def full_cofactor(colour: int, surviving: set[str]) -> Quad:
    return LEDGER[colour][frozenset(set(P) - surviving)]


def wick_degree_five(colour: int, surviving: str) -> Quad:
    face = tuple(surviving)
    total = full_cofactor(colour, set(face))
    for pair in combinations(face, 2):
        total -= M.get(frozenset(pair), ZERO) * full_cofactor(
            colour, set(face) - set(pair)
        )
    for four_set in combinations(face, 4):
        i, j, k, ell = four_set
        for first, second in (
            ((i, j), (k, ell)),
            ((i, k), (j, ell)),
            ((i, ell), (j, k)),
        ):
            total += (
                M.get(frozenset(first), ZERO)
                * M.get(frozenset(second), ZERO)
                * full_cofactor(colour, set(face) - set(four_set))
            )
    return total


INCIDENCE: dict[tuple[int, str], dict[int, Quad]] = {
    (2, "1"): {0: ONE},
    (3, "2"): {0: ONE},
    (4, "5"): {0: ONE},
    (5, "a"): {0: ONE},
    (6, "b"): {0: ONE},
    (0, "a"): {1: ONE},
    (1, "b"): {1: ONE},
    (4, "3"): {1: -ONE},
    (5, "4"): {1: -ONE},
    (6, "5"): {1: ONE},
}

CORE_EDGES = {
    (0, 1): (0, 0, C_VALUE),
    (2, 3): (1, 1, C_VALUE),
}


def physical_face_response(face: str) -> dict[tuple[int, ...], Quad]:
    terminals = tuple(face)
    response: dict[tuple[int, ...], Quad] = {}

    def accumulate_edge(
        left: int,
        right: int,
        left_colour: int,
        right_colour: int,
        edge_weight: Quad,
    ) -> None:
        remaining_cores = tuple(i for i in range(7) if i not in (left, right))
        colours: list[int | None] = [None] * 7
        colours[left] = left_colour
        colours[right] = right_colour

        def assign(position: int, used_mask: int, coefficient: Quad) -> None:
            if position == len(remaining_cores):
                if used_mask == (1 << len(terminals)) - 1:
                    word = tuple(int(colour) for colour in colours)
                    response[word] = response.get(word, ZERO) + edge_weight * coefficient
                return
            core = remaining_cores[position]
            for terminal_index, terminal in enumerate(terminals):
                if used_mask & (1 << terminal_index):
                    continue
                for colour, weight in INCIDENCE.get((core, terminal), {}).items():
                    colours[core] = colour
                    assign(
                        position + 1,
                        used_mask | (1 << terminal_index),
                        coefficient * weight,
                    )
                    colours[core] = None

        assign(0, 0, ONE)

    for (left, right), (left_colour, right_colour, edge_weight) in CORE_EDGES.items():
        accumulate_edge(left, right, left_colour, right_colour, edge_weight)
    return {word: value for word, value in response.items() if value}


def add_tensor(
    left: dict[tuple[int, ...], Quad],
    right: dict[tuple[int, ...], Quad],
    scale: int,
) -> dict[tuple[int, ...], Quad]:
    result = dict(left)
    for word, value in right.items():
        result[word] = result.get(word, ZERO) + scale * value
    return {word: value for word, value in result.items() if value}


def main() -> None:
    expected_formal = {
        0: (C_VALUE, ZERO, ZERO, ZERO),
        1: (ZERO, ZERO, ZERO, C_VALUE),
        2: (T_VALUE, T_VALUE, T_VALUE, T_VALUE),
    }
    formal_values: dict[int, tuple[Quad, ...]] = {}
    for colour in range(3):
        values = tuple(wick_degree_five(colour, face) for face in FACES)
        assert values == expected_formal[colour]
        formal_values[colour] = values

    signs = (1, -1, -1, 1)
    formal_circuit = {
        (colour,) * 7: sum(
            (sign * formal_values[colour][index] for index, sign in enumerate(signs)),
            ZERO,
        )
        for colour in range(3)
    }
    formal_circuit = {word: value for word, value in formal_circuit.items() if value}
    assert formal_circuit == {(0,) * 7: C_VALUE, (1,) * 7: C_VALUE}

    physical_values = tuple(physical_face_response(face) for face in FACES)
    assert physical_values == (
        {(0,) * 7: C_VALUE},
        {},
        {},
        {(1,) * 7: C_VALUE},
    )
    physical_circuit: dict[tuple[int, ...], Quad] = {}
    for value, sign in zip(physical_values, signs, strict=True):
        physical_circuit = add_tensor(physical_circuit, value, sign)
    assert physical_circuit == formal_circuit

    print("AUDIT PASS")
    print("formal Wick table and physical sparse response agree")
    print("binary GHZ contraction is an exact physical image point")
    print("no local-colour-word or support search used")


if __name__ == "__main__":
    main()
