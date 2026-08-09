"""Verify the physical countermodel for the four-face binary GHZ tensor.

The calculation is exact.  It reconstructs the four pure formal Wick
responses and evaluates one fixed sparse tensor-valued physical graph.  It
does not search supports, parameters, or local-colour words.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp

P = ("1", "2", "3", "4", "5", "a", "b")
Q = frozenset(("a", "b"))
FACES = ("125ab", "145ab", "235ab", "345ab")
RHO = sp.sqrt(21)
KAPPA = 1 + 22 / RHO
C_VALUE = RHO - 2
T_VALUE = (RHO + 1) / 7


def formal_ledger() -> dict[int, dict[frozenset[str], sp.Expr]]:
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(P, size)
        if not (size == 2 and frozenset(deletion) == Q)
    ]
    ledger = {
        colour: {deletion: sp.Integer(0) for deletion in prescribed}
        for colour in range(3)
    }

    def assign(deletion: str, colour: int, value: sp.Expr | int = 1) -> None:
        ledger[colour][frozenset(deletion)] = sp.sympify(value)

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
    assign("1234", 2, sp.Rational(1, 7))
    assign("1234ab", 2, sp.Rational(1, 7))
    return ledger


def terminal_block() -> dict[frozenset[str], sp.Expr]:
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
        "ab": 1 - RHO,
    }
    return {frozenset(pair): sp.sympify(value) for pair, value in weights.items()}


LEDGER = formal_ledger()
M = terminal_block()


def full_cofactor(colour: int, surviving: set[str]) -> sp.Expr:
    deletion = frozenset(set(P) - surviving)
    return LEDGER[colour][deletion]


def wick_degree_five(colour: int, surviving: str) -> sp.Expr:
    """Coefficient of E_(-M)F on one fixed five-set."""

    face = tuple(surviving)
    total = full_cofactor(colour, set(face))
    for pair in combinations(face, 2):
        total -= M.get(frozenset(pair), 0) * full_cofactor(
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
                M.get(frozenset(first), 0)
                * M.get(frozenset(second), 0)
                * full_cofactor(colour, set(face) - set(four_set))
            )
    return sp.simplify(total)


# Physical graph.  Incidence values are sparse local vectors represented by
# colour -> scalar dictionaries.
INCIDENCE: dict[tuple[int, str], dict[int, sp.Expr]] = {
    (2, "1"): {0: sp.Integer(1)},
    (3, "2"): {0: sp.Integer(1)},
    (4, "5"): {0: sp.Integer(1)},
    (5, "a"): {0: sp.Integer(1)},
    (6, "b"): {0: sp.Integer(1)},
    (0, "a"): {1: sp.Integer(1)},
    (1, "b"): {1: sp.Integer(1)},
    (4, "3"): {1: sp.Integer(-1)},
    (5, "4"): {1: sp.Integer(-1)},
    (6, "5"): {1: sp.Integer(1)},
}

# endpoint pair -> (left colour, right colour, scalar)
CORE_EDGES = {
    (0, 1): (0, 0, C_VALUE),
    (2, 3): (1, 1, C_VALUE),
}


def physical_face_response(face: str) -> dict[tuple[int, ...], sp.Expr]:
    """Sparse tensor response on a five-terminal face."""

    terminals = tuple(face)
    response: dict[tuple[int, ...], sp.Expr] = {}

    def accumulate_edge(
        left: int,
        right: int,
        left_colour: int,
        right_colour: int,
        edge_weight: sp.Expr,
    ) -> None:
        remaining_cores = tuple(i for i in range(7) if i not in (left, right))
        colours: list[int | None] = [None] * 7
        colours[left] = left_colour
        colours[right] = right_colour

        def assign(position: int, used_mask: int, coefficient: sp.Expr) -> None:
            if position == len(remaining_cores):
                if used_mask != (1 << len(terminals)) - 1:
                    return
                word = tuple(int(colour) for colour in colours)
                response[word] = sp.simplify(
                    response.get(word, sp.Integer(0)) + edge_weight * coefficient
                )
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

        assign(0, 0, sp.Integer(1))

    for (left, right), (left_colour, right_colour, edge_weight) in CORE_EDGES.items():
        accumulate_edge(left, right, left_colour, right_colour, edge_weight)
    return {word: value for word, value in response.items() if sp.simplify(value) != 0}


def add_tensor(
    left: dict[tuple[int, ...], sp.Expr],
    right: dict[tuple[int, ...], sp.Expr],
    scale: sp.Expr,
) -> dict[tuple[int, ...], sp.Expr]:
    result = dict(left)
    for word, value in right.items():
        result[word] = sp.simplify(result.get(word, 0) + scale * value)
    return {word: value for word, value in result.items() if value != 0}


def main() -> None:
    expected_formal = {
        0: (C_VALUE, 0, 0, 0),
        1: (0, 0, 0, C_VALUE),
        2: (T_VALUE, T_VALUE, T_VALUE, T_VALUE),
    }
    formal_values: dict[int, tuple[sp.Expr, ...]] = {}
    for colour in range(3):
        values = tuple(wick_degree_five(colour, face) for face in FACES)
        formal_values[colour] = values
        assert all(
            sp.simplify(value - expected) == 0
            for value, expected in zip(values, expected_formal[colour], strict=True)
        )

    signs = (1, -1, -1, 1)
    formal_circuit = {
        (colour,) * 7: sp.simplify(
            sum(sign * formal_values[colour][index] for index, sign in enumerate(signs))
        )
        for colour in range(3)
    }
    formal_circuit = {word: value for word, value in formal_circuit.items() if value != 0}
    assert formal_circuit == {(0,) * 7: C_VALUE, (1,) * 7: C_VALUE}

    physical_values = tuple(physical_face_response(face) for face in FACES)
    assert physical_values == (
        {(0,) * 7: C_VALUE},
        {},
        {},
        {(1,) * 7: C_VALUE},
    )
    physical_circuit: dict[tuple[int, ...], sp.Expr] = {}
    for value, sign in zip(physical_values, signs, strict=True):
        physical_circuit = add_tensor(physical_circuit, value, sign)
    assert physical_circuit == formal_circuit

    print("formal Wick four-face table: exact")
    print("formal contraction: (rho-2)(D0+D1)")
    print("physical non-D2 tuple: ((rho-2)D0,0,0,(rho-2)D1)")
    print("mixed local-colour support in physical tuple: empty")
    print("contracted degree-five separator: REFUTED BY PHYSICAL IMAGE POINT")


if __name__ == "__main__":
    main()
