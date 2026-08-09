"""Independent no-import audit of the physical P6 six-face hafnian section."""

from fractions import Fraction
from functools import cache
from itertools import combinations

CORE = (0, 1, 2, 3)
WINDOW = (4, 5, 6, 7)
VERTICES = CORE + WINDOW
WINDOW_PAIRS = tuple(combinations(WINDOW, 2))
VARIABLE_COUNT = 7
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]


def edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if not coefficient else {(0,) * VARIABLE_COUNT: coefficient}


def variable(index: int) -> Polynomial:
    exponents = [0] * VARIABLE_COUNT
    exponents[index] = 1
    return {tuple(exponents): Fraction(1)}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def scale(poly: Polynomial, value: int | Fraction) -> Polynomial:
    factor = Fraction(value)
    return clean({monomial: factor * coefficient for monomial, coefficient in poly.items()})


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_monomial[index] + right_monomial[index]
                for index in range(VARIABLE_COUNT)
            )
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
    return clean(result)


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(left, scale(right, -1))


def polynomial_hafnian(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], Polynomial]
) -> Polynomial:
    @cache
    def rec(remaining: tuple[int, ...]) -> tuple[tuple[Monomial, Fraction], ...]:
        if not remaining:
            return tuple(constant(1).items())
        first = remaining[0]
        total: Polynomial = {}
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            subhafnian = dict(rec(rest))
            total = add(total, multiply(weights[edge(first, partner)], subhafnian))
        return tuple(sorted(clean(total).items()))

    return dict(rec(vertices))


def symbolic_section() -> tuple[
    dict[tuple[int, int], Polynomial],
    dict[tuple[int, int], Polynomial],
    Polynomial,
]:
    faces = {
        pair: variable(index) for index, pair in enumerate(WINDOW_PAIRS)
    }
    tau = variable(6)
    tau_squared = multiply(tau, tau)
    weights: dict[tuple[int, int], Polynomial] = {}
    for pair in combinations(CORE, 2):
        weights[pair] = constant(1)
    for core_vertex in CORE:
        for port in WINDOW:
            weights[(core_vertex, port)] = tau
    for pair in WINDOW_PAIRS:
        weights[pair] = scale(subtract(faces[pair], scale(tau_squared, 12)), Fraction(1, 3))
    return faces, weights, tau


def symbolic_complete_deck_audit() -> None:
    faces, weights, tau = symbolic_section()
    tau_squared = multiply(tau, tau)
    assert polynomial_hafnian(CORE, weights) == constant(3)

    for pair in WINDOW_PAIRS:
        remaining = tuple(sorted(CORE + pair))
        assert polynomial_hafnian(remaining, weights) == faces[pair]

    deck_count = 0
    for remaining in combinations(VERTICES, 4):
        actual = polynomial_hafnian(remaining, weights)
        ports = tuple(vertex for vertex in remaining if vertex in WINDOW)
        if len(ports) == 0:
            expected = constant(3)
        elif len(ports) == 1:
            expected = scale(tau, 3)
        elif len(ports) == 2:
            expected = scale(
                subtract(faces[edge(*ports)], scale(tau_squared, 6)),
                Fraction(1, 3),
            )
        elif len(ports) == 3:
            face_sum: Polynomial = {}
            for pair in combinations(ports, 2):
                face_sum = add(face_sum, faces[pair])
            expected = scale(
                multiply(tau, subtract(face_sum, scale(tau_squared, 36))),
                Fraction(1, 3),
            )
        else:
            b = {pair: weights[pair] for pair in WINDOW_PAIRS}
            expected = add(
                multiply(b[(4, 5)], b[(6, 7)]),
                add(
                    multiply(b[(4, 6)], b[(5, 7)]),
                    multiply(b[(4, 7)], b[(5, 6)]),
                ),
            )
        assert actual == expected
        deck_count += 1
    assert deck_count == 70

    stress_count = 0
    for pair in WINDOW_PAIRS:
        remaining = tuple(sorted(CORE + pair))
        for pivot in remaining:
            total: Polynomial = {}
            for partner in remaining:
                if partner == pivot:
                    continue
                four_set = tuple(
                    vertex for vertex in remaining if vertex not in (pivot, partner)
                )
                term = multiply(
                    weights[edge(pivot, partner)],
                    polynomial_hafnian(four_set, weights),
                )
                total = add(total, term)
            assert total == faces[pair]
            stress_count += 1
    assert stress_count == 36
    print("independent symbolic section, full H4 deck, and nested stresses: PASS")


def scalar_hafnian(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], Fraction]
) -> Fraction:
    @cache
    def rec(remaining: tuple[int, ...]) -> Fraction:
        if not remaining:
            return Fraction(1)
        first = remaining[0]
        total = Fraction(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += weights[edge(first, partner)] * rec(rest)
        return total

    return rec(vertices)


def scalar_section(face_column: tuple[int, ...]) -> dict[tuple[int, int], Fraction]:
    faces = dict(zip(WINDOW_PAIRS, map(Fraction, face_column), strict=True))
    weights: dict[tuple[int, int], Fraction] = {}
    for pair in combinations(CORE, 2):
        weights[pair] = Fraction(1)
    for core_vertex in CORE:
        for port in WINDOW:
            weights[(core_vertex, port)] = Fraction(1)
    for pair in WINDOW_PAIRS:
        weights[pair] = (faces[pair] - 12) / 3
    return weights


def integer_fan() -> list[list[int]]:
    parameters = (1, 2, 3, 4)
    columns: list[list[int]] = []
    for left, right in combinations(parameters, 2):
        columns.append(
            [
                2,
                left**2 + right**2,
                left**3 + right**3,
                left + right,
                left * right**2 + right * left**2,
                left * right**3 + right * left**3,
            ]
        )
    return [[columns[column][row] for column in range(6)] for row in range(6)]


def matrix_vector(matrix: list[list[int]], vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(entry * value for entry, value in zip(row, vector, strict=True))
        for row in matrix
    )


def fixed_three_colour_audit() -> None:
    face_columns = (
        (14, -24, 20, 15, -29, 9),
        (10, -33, 36, 30, -58, 18),
        (2, 38, -45, -30, 73, -23),
    )
    left_factors = ((1, 1), (1, 1), (1, 2))
    right_factors = ((1, 1, 1), (1, 2, 3), (1, 4, 9))
    scales = (10, 6, 30)
    fan = integer_fan()
    graphs = [scalar_section(column) for column in face_columns]

    for column, left, right, factor, graph in zip(
        face_columns,
        left_factors,
        right_factors,
        scales,
        graphs,
        strict=True,
    ):
        assert all(graph.values())
        for pair, value in zip(WINDOW_PAIRS, column, strict=True):
            assert scalar_hafnian(tuple(sorted(CORE + pair)), graph) == value
        observed = matrix_vector(fan, column)
        expected = tuple(
            factor * left_value * right_value
            for left_value in left
            for right_value in right
        )
        assert observed == expected
        for first, second in combinations(range(3), 2):
            assert (
                observed[first] * observed[3 + second]
                - observed[second] * observed[3 + first]
                == 0
            )

    window_diagonals = [tuple(graph[pair] for graph in graphs) for pair in WINDOW_PAIRS]
    assert all(value for diagonal in window_diagonals for value in diagonal)
    assert window_diagonals[0] == (Fraction(2, 3), Fraction(-2, 3), Fraction(-10, 3))
    mixed_word = graphs[0][(0, 1)] * graphs[1][(2, 3)] * graphs[2][(4, 5)]
    assert mixed_word == Fraction(-10, 3)
    print("independent three-colour physical sections and mixed-word boundary: PASS")


def main() -> None:
    symbolic_complete_deck_audit()
    fixed_three_colour_audit()
    print("P6 physical six-face/four-deck section independent audit: PASS")


if __name__ == "__main__":
    main()
