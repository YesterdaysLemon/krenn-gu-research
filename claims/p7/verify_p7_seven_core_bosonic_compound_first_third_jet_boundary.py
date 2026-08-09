"""Verify the seven-core bosonic first/third-jet boundary.

This checks one fixed Jacobian certificate and the fixed formal ledger.  It
does not search graph supports, response words, parameter values, or minors.
"""

from itertools import combinations, permutations

import sympy as sp

CORE = tuple(range(7))
TERMINALS = ("1", "2", "3", "4", "5", "a", "b")
EDGES = tuple(combinations(CORE, 2))
TRIPLES = tuple(combinations(CORE, 3))
JACOBIAN_COLUMNS = tuple(range(34)) + (35, 36, 37, 38, 39, 40, 42, 43)


def permanent(matrix: list[list[int]], modulus: int) -> int:
    return sum(
        product(
            (matrix[row][column] for row, column in enumerate(order)), modulus
        )
        for order in permutations(range(len(matrix)))
    ) % modulus


def product(values, modulus: int) -> int:
    result = 1
    for value in values:
        result = result * value % modulus
    return result


def hafnian_deleted(
    edge_values: dict[tuple[int, int], int],
    deleted: frozenset[int],
    modulus: int,
) -> int:
    remaining = tuple(vertex for vertex in CORE if vertex not in deleted)

    def recurse(vertices: tuple[int, ...]) -> int:
        if not vertices:
            return 1
        first = vertices[0]
        total = 0
        for position in range(1, len(vertices)):
            second = vertices[position]
            edge = (min(first, second), max(first, second))
            rest = vertices[1:position] + vertices[position + 1 :]
            total += edge_values[edge] * recurse(rest)
        return total % modulus

    return recurse(remaining)


def response_jacobian(modulus: int) -> list[list[int]]:
    def point_value(index: int) -> int:
        return (((index * index + 3 * index + 7) % 11) - 5) % modulus

    edge_values = {
        edge: point_value(index) for index, edge in enumerate(EDGES)
    }
    terminal_matrix = [
        [point_value(21 + 7 * row + column) for column in CORE]
        for row in CORE
    ]
    hafnians = {
        frozenset(deleted): hafnian_deleted(
            edge_values, frozenset(deleted), modulus
        )
        for size in (1, 3, 5)
        for deleted in combinations(CORE, size)
    }

    def subpermanent(rows: tuple[int, ...], columns: tuple[int, ...]) -> int:
        matrix = [
            [terminal_matrix[row][column] for column in columns]
            for row in rows
        ]
        return permanent(matrix, modulus)

    jacobian: list[list[int]] = []
    for terminal in CORE:
        row = [
            sum(
                hafnians[frozenset((core, left, right))]
                * terminal_matrix[core][terminal]
                for core in CORE
                if core not in (left, right)
            )
            % modulus
            for left, right in EDGES
        ]
        row.extend(
            hafnians[frozenset((core,))] if terminal == column else 0
            for core in CORE
            for column in CORE
        )
        jacobian.append(row)

    for terminal_triple in TRIPLES:
        row = []
        for left, right in EDGES:
            derivative = sum(
                hafnians[frozenset(core_triple + (left, right))]
                * subpermanent(core_triple, terminal_triple)
                for core_triple in TRIPLES
                if left not in core_triple and right not in core_triple
            )
            row.append(derivative % modulus)
        for core in CORE:
            for terminal in CORE:
                derivative = 0
                if terminal in terminal_triple:
                    other_terminals = tuple(
                        value for value in terminal_triple if value != terminal
                    )
                    derivative = sum(
                        hafnians[frozenset(core_triple)]
                        * subpermanent(
                            tuple(value for value in core_triple if value != core),
                            other_terminals,
                        )
                        for core_triple in TRIPLES
                        if core in core_triple
                    )
                row.append(derivative % modulus)
        jacobian.append(row)
    assert len(jacobian) == 42
    assert all(len(row) == 70 for row in jacobian)
    return jacobian


def determinant_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[value % modulus for value in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column] != 0
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % modulus
        inverse = pow(pivot_value, modulus - 2, modulus)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * inverse % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[column])
                ]
    return determinant % modulus


def formal_ledger() -> dict[int, dict[frozenset[str], sp.Expr]]:
    all_terminals = frozenset(TERMINALS)
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(TERMINALS, size)
        if not (size == 2 and frozenset(deletion) == frozenset(("a", "b")))
    ]
    ledger = {
        color: {deletion: sp.Integer(0) for deletion in prescribed}
        for color in range(3)
    }

    def assign(deletion: str, color: int, value=1) -> None:
        ledger[color][frozenset(deletion)] = sp.sympify(value)

    for deletion, color in {
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
        assign(deletion, color)
    assign("12", 1, -1)
    assign("12", 2)
    assign("12ab", 1)
    assign("34", 0, -1)
    assign("34", 2)
    assign("34ab", 0)
    for pair, color, with_q in (
        ("13", 2, True),
        ("14", 2, False),
        ("23", 2, False),
        ("24", 2, True),
        ("15", 1, True),
        ("25", 1, False),
        ("35", 0, False),
        ("45", 0, True),
    ):
        assign(pair, color)
        if with_q:
            assign(pair + "ab", color)
    for deletion, color in {
        "123a": 2,
        "124b": 2,
        "134a": 2,
        "234b": 2,
        "125a": 1,
        "345b": 0,
    }.items():
        assign(deletion, color)
    assign("1234", 2, sp.Rational(1, 7))
    assign("1234ab", 2, sp.Rational(1, 7))
    assert all_terminals == frozenset(TERMINALS)
    return ledger


def check_wick_deconvolution() -> None:
    ledger = formal_ledger()
    all_terminals = frozenset(TERMINALS)
    rho = sp.sqrt(21)
    kappa = 1 + 22 / rho
    weights = {
        "12": -kappa,
        "14": -kappa,
        "23": -kappa,
        "34": -kappa,
        "13": 7,
        "24": 7,
        "1a": 7,
        "3a": 7,
        "2b": 7,
        "4b": 7,
        "1b": -rho,
        "2a": -rho,
        "3b": -rho,
        "4a": -rho,
        "ab": 1 - rho,
    }
    terminal_block = {
        frozenset(pair): sp.sympify(value) for pair, value in weights.items()
    }
    phi_one = {
        frozenset((terminal,)): tuple(
            ledger[color][all_terminals - frozenset((terminal,))]
            for color in range(3)
        )
        for terminal in TERMINALS
    }
    assert phi_one[frozenset(("5",))] == (0, 0, sp.Rational(1, 7))
    assert all(
        value == (0, 0, 0)
        for terminal, value in phi_one.items()
        if terminal != frozenset(("5",))
    )

    phi_three = {}
    for triple in combinations(TERMINALS, 3):
        terminal_set = frozenset(triple)
        deletion = all_terminals - terminal_set
        value = [ledger[color][deletion] for color in range(3)]
        for pair in combinations(triple, 2):
            singleton = terminal_set - frozenset(pair)
            weight = terminal_block.get(frozenset(pair), 0)
            for color in range(3):
                value[color] -= weight * phi_one[singleton][color]
        phi_three["".join(triple)] = tuple(map(sp.simplify, value))
    expected = {
        "123": (1, 0, 0),
        "125": (1, 0, kappa / 7),
        "12a": (1, 0, 0),
        "145": (0, 0, kappa / 7),
        "15b": (0, 0, rho / 7),
        "234": (0, 1, 0),
        "235": (0, 0, kappa / 7),
        "25a": (0, 0, rho / 7),
        "345": (0, 1, kappa / 7),
        "34b": (0, 1, 0),
        "35b": (0, 0, rho / 7),
        "45a": (0, 0, rho / 7),
        "5ab": (0, 0, rho / 7),
    }
    assert {
        key: value for key, value in phi_three.items() if value != (0, 0, 0)
    } == expected


def check_local_derivative_identity() -> None:
    entries = sp.symbols("l00:03 l10:13 l20:23")
    matrix = sp.Matrix(3, 3, entries)
    anchored_sum = sum(
        matrix[anchor, 0]
        * (
            matrix[(anchor + 1) % 3, 1] * matrix[(anchor + 2) % 3, 2]
            + matrix[(anchor + 1) % 3, 2] * matrix[(anchor + 2) % 3, 1]
        )
        for anchor in range(3)
    )
    assert sp.expand(anchored_sum - sp.per(matrix)) == 0


def main() -> None:
    check_wick_deconvolution()
    check_local_derivative_identity()
    jacobian = response_jacobian(101)
    minor = [[row[column] for column in JACOBIAN_COLUMNS] for row in jacobian]
    assert len(JACOBIAN_COLUMNS) == 42
    assert determinant_mod(minor, 101) == 81
    print("PASS: corrected degree-one and degree-three Wick ledger")
    print("PASS: bosonic insertion derivative identity")
    print("PASS: fixed 42x42 Jacobian minor is 81 mod 101")
    print("SCOPE: scalar low-jet dominance; physical tensor synchronization open")


if __name__ == "__main__":
    main()
