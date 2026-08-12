"""Independent no-import audit of the normalized full-row S2M controls.

This script imports neither SymPy nor repository code.  It reconstructs the
eight controls in a small exact Laurent-polynomial algebra over Q and checks
all 27 target rows, Cramer determinants, multidegrees, retained derivatives,
and the exceptional replacement determinant.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

Exponent = tuple[int, ...]
ZERO_EXPONENT: Exponent = (0,) * 9
WORDS = tuple(product(range(3), repeat=3))
ROW = {word: index for index, word in enumerate(WORDS)}
EXPECTED_DEGREES = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))
SOLUTION_DEGREES = ((1, 1, 0), (1, 0, 1), (0, 1, 1), (0, 0, 0))


@dataclass
class Laurent:
    """A sparse exact Laurent polynomial in nine variables."""

    terms: dict[Exponent, Fraction]

    def __post_init__(self) -> None:
        self.terms = {
            exponent: coefficient
            for exponent, coefficient in self.terms.items()
            if coefficient
        }

    @staticmethod
    def zero() -> Laurent:
        return Laurent({})

    @staticmethod
    def one() -> Laurent:
        return Laurent({ZERO_EXPONENT: Fraction(1)})

    @staticmethod
    def variable(index: int, power: int = 1) -> Laurent:
        exponent = list(ZERO_EXPONENT)
        exponent[index] = power
        return Laurent({tuple(exponent): Fraction(1)})

    def __add__(self, other: Laurent) -> Laurent:
        answer = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            answer[exponent] = answer.get(exponent, Fraction()) + coefficient
        return Laurent(answer)

    def __sub__(self, other: Laurent) -> Laurent:
        return self + (-other)

    def __neg__(self) -> Laurent:
        return Laurent(
            {exponent: -coefficient for exponent, coefficient in self.terms.items()}
        )

    def __mul__(self, other: Laurent) -> Laurent:
        answer: dict[Exponent, Fraction] = {}
        for left_exp, left_coefficient in self.terms.items():
            for right_exp, right_coefficient in other.terms.items():
                exponent = tuple(
                    left + right
                    for left, right in zip(left_exp, right_exp, strict=True)
                )
                answer[exponent] = (
                    answer.get(exponent, Fraction())
                    + left_coefficient * right_coefficient
                )
        return Laurent(answer)

    def derivative(self, variable: int) -> Laurent:
        answer: dict[Exponent, Fraction] = {}
        for exponent, coefficient in self.terms.items():
            power = exponent[variable]
            if power == 0:
                continue
            derived = list(exponent)
            derived[variable] -= 1
            key = tuple(derived)
            answer[key] = answer.get(key, Fraction()) + coefficient * power
        return Laurent(answer)

    def is_zero(self) -> bool:
        return not self.terms

    def group_degrees(self) -> set[tuple[int, int, int]]:
        return {
            (
                sum(exponent[:3]),
                sum(exponent[3:6]),
                sum(exponent[6:]),
            )
            for exponent in self.terms
        }

    def __str__(self) -> str:
        if not self.terms:
            return "0"
        pieces = []
        for exponent, coefficient in sorted(self.terms.items()):
            pieces.append(f"{coefficient}*{exponent}")
        return " + ".join(pieces)


ZERO = Laurent.zero()
ONE = Laurent.one()


def x(index: int, power: int = 1) -> Laurent:
    return Laurent.variable(index, power)


def y(index: int, power: int = 1) -> Laurent:
    return Laurent.variable(3 + index, power)


def r(index: int, power: int = 1) -> Laurent:
    return Laurent.variable(6 + index, power)


def target() -> list[Laurent]:
    answer = [ZERO for _ in WORDS]
    for colour in range(3):
        answer[ROW[(colour, colour, colour)]] = x(colour) * y(colour) * r(colour)
    return answer


J = target()


def zero_matrix(rows: int, columns: int) -> list[list[Laurent]]:
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def base_matrix() -> list[list[Laurent]]:
    gamma = zero_matrix(27, 4)
    for colour in range(3):
        gamma[ROW[(colour, colour, colour)]][3] = J[
            ROW[(colour, colour, colour)]
        ]
    return gamma


def dot(row: list[Laurent], vector: list[Laurent]) -> Laurent:
    answer = ZERO
    for coefficient, value in zip(row, vector, strict=True):
        answer = answer + coefficient * value
    return answer


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[Laurent]]) -> Laurent:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    answer = ZERO
    for permutation in permutations(range(size)):
        term = ONE
        for row, column in enumerate(permutation):
            term = term * matrix[row][column]
        answer = answer + term if permutation_sign(permutation) == 1 else answer - term
    return answer


def replace_column(
    matrix: list[list[Laurent]],
    column: int,
    replacement: list[Laurent],
) -> list[list[Laurent]]:
    answer = [row.copy() for row in matrix]
    for row, value in enumerate(replacement):
        answer[row][column] = value
    return answer


def differentiate_matrix(
    matrix: list[list[Laurent]], variable: int
) -> list[list[Laurent]]:
    return [
        [entry.derivative(variable) for entry in row]
        for row in matrix
    ]


def matrix_vector(
    matrix: list[list[Laurent]], vector: list[Laurent]
) -> list[Laurent]:
    return [dot(row, vector) for row in matrix]


@dataclass(frozen=True)
class Control:
    name: str
    gamma: list[list[Laurent]]
    solution: list[Laurent]
    selected: tuple[tuple[int, int, int], ...]
    exceptional: tuple[str, int, int]


def outside_control(index: int) -> Control:
    gamma = base_matrix()
    diagonal = (index, index, index)
    gamma[ROW[diagonal]] = [r(0), ZERO, ZERO, ZERO]
    gamma[ROW[(0, 0, 1)]] = [
        -r(0),
        ZERO,
        ZERO,
        x(index) * y(index) * r(index),
    ]
    gamma[ROW[(0, 1, 0)]][1] = y(0)
    gamma[ROW[(1, 0, 0)]][2] = x(0)
    solution = [
        r(index) * r(0, -1) * x(index) * y(index),
        ZERO,
        ZERO,
        ONE,
    ]
    return Control(
        f"outside-r{index}",
        gamma,
        solution,
        (diagonal, (0, 0, 1), (0, 1, 0), (1, 0, 0)),
        ("r", index, index),
    )


def x_control(left: int, right: int) -> Control:
    gamma = base_matrix()
    diagonal = (left, left, left)
    gamma[ROW[(0, 0, 1)]] = [r(left), ZERO, -x(right), ZERO]
    gamma[ROW[diagonal]] = [ZERO, ZERO, x(0), ZERO]
    gamma[ROW[(0, 1, 0)]][1] = y(0)
    solution = [
        x(left) * x(right) * x(0, -1) * y(left),
        ZERO,
        x(left) * x(0, -1) * y(left) * r(left),
        ONE,
    ]
    return Control(
        f"endpoint-x{left}{right}",
        gamma,
        solution,
        ((0, 0, 1), diagonal, (0, 0, 0), (0, 1, 0)),
        ("x", left, right),
    )


def y_control(left: int, right: int) -> Control:
    gamma = base_matrix()
    diagonal = (left, left, left)
    gamma[ROW[(0, 0, 1)]] = [r(left), -y(right), ZERO, ZERO]
    gamma[ROW[diagonal]] = [ZERO, y(0), ZERO, ZERO]
    gamma[ROW[(0, 1, 0)]][2] = x(0)
    solution = [
        x(left) * y(left) * y(right) * y(0, -1),
        x(left) * y(left) * y(0, -1) * r(left),
        ZERO,
        ONE,
    ]
    return Control(
        f"endpoint-y{left}{right}",
        gamma,
        solution,
        ((0, 0, 1), diagonal, (0, 0, 0), (0, 1, 0)),
        ("y", left, right),
    )


def all_controls() -> tuple[Control, ...]:
    controls = [outside_control(index) for index in (1, 2)]
    controls.extend(
        x_control(left, right)
        for left in (1, 2)
        for right in range(left, 3)
    )
    controls.extend(
        y_control(left, right)
        for left in (1, 2)
        for right in range(left, 3)
    )
    return tuple(controls)


def retained_derivatives(pair: Laurent) -> dict[tuple[str, int, int], Laurent]:
    answer = {
        ("r", index, index): pair.derivative(6 + index)
        for index in (1, 2)
    }
    for name, offset in (("x", 0), ("y", 3)):
        for left in (1, 2):
            for right in range(left, 3):
                answer[(name, left, right)] = pair.derivative(
                    offset + left
                ).derivative(offset + right)
    return answer


def subtract_vectors(
    left: list[Laurent], right: list[Laurent]
) -> list[Laurent]:
    return [a - b for a, b in zip(left, right, strict=True)]


def scale_vector(scalar: Laurent, vector: list[Laurent]) -> list[Laurent]:
    return [scalar * value for value in vector]


def first_residual(
    matrix: list[list[Laurent]],
    selected_target: list[Laurent],
    numerator: list[Laurent],
    beta: Laurent,
    variable: int,
) -> list[Laurent]:
    derivative_target = [value.derivative(variable) for value in selected_target]
    derivative_matrix = differentiate_matrix(matrix, variable)
    return subtract_vectors(
        scale_vector(beta, derivative_target),
        matrix_vector(derivative_matrix, numerator),
    )


def hessian_residual(
    matrix: list[list[Laurent]],
    selected_target: list[Laurent],
    numerator: list[Laurent],
    solution: list[Laurent],
    beta: Laurent,
    first: int,
    second: int,
) -> list[Laurent]:
    target_hessian = [
        value.derivative(first).derivative(second)
        for value in selected_target
    ]
    matrix_first = differentiate_matrix(matrix, first)
    matrix_second = differentiate_matrix(matrix, second)
    matrix_hessian = differentiate_matrix(matrix_first, second)
    stress_first = [beta * beta * value.derivative(first) for value in solution]
    stress_second = [beta * beta * value.derivative(second) for value in solution]
    answer = scale_vector(beta * beta, target_hessian)
    answer = subtract_vectors(
        answer,
        scale_vector(beta, matrix_vector(matrix_hessian, numerator)),
    )
    answer = subtract_vectors(answer, matrix_vector(matrix_first, stress_second))
    return subtract_vectors(answer, matrix_vector(matrix_second, stress_first))


def verify(control: Control) -> tuple[Laurent, Laurent]:
    assert control.solution[3] == ONE
    assert matrix_vector(control.gamma, control.solution) == J

    for component, expected in zip(
        control.solution, SOLUTION_DEGREES, strict=True
    ):
        if not component.is_zero():
            assert component.group_degrees() == {expected}

    for column, expected in enumerate(EXPECTED_DEGREES):
        for row in control.gamma:
            entry = row[column]
            if not entry.is_zero():
                assert entry.group_degrees() == {expected}

    selected_indices = [ROW[word] for word in control.selected]
    matrix = [control.gamma[index].copy() for index in selected_indices]
    selected_target = [J[index] for index in selected_indices]
    beta = determinant(matrix)
    assert not beta.is_zero()
    assert matrix_vector(matrix, control.solution) == selected_target

    numerator = [
        determinant(replace_column(matrix, column, selected_target))
        for column in range(4)
    ]
    assert numerator == scale_vector(beta, control.solution)
    assert matrix_vector(control.gamma, numerator) == scale_vector(beta, J)
    assert numerator[3] == beta

    derivatives = retained_derivatives(control.solution[0])
    nonzero = {key for key, value in derivatives.items() if not value.is_zero()}
    assert nonzero == {control.exceptional}

    exceptional_replacement = ZERO
    for coordinate, derivative in derivatives.items():
        name, left, right = coordinate
        if name == "r":
            variable = 6 + left
            residual = first_residual(
                matrix, selected_target, numerator, beta, variable
            )
            expected = beta * beta * derivative
        else:
            offset = 0 if name == "x" else 3
            first = offset + left
            second = offset + right
            residual = hessian_residual(
                matrix,
                selected_target,
                numerator,
                control.solution,
                beta,
                first,
                second,
            )
            expected = beta * beta * beta * derivative
        replacement = determinant(replace_column(matrix, 0, residual))
        assert replacement == expected
        assert (not replacement.is_zero()) == (coordinate == control.exceptional)
        if coordinate == control.exceptional:
            exceptional_replacement = replacement

    assert not exceptional_replacement.is_zero()
    return beta, exceptional_replacement


def main() -> None:
    controls = all_controls()
    assert len(controls) == 8
    for control in controls:
        beta, replacement = verify(control)
        print(
            f"{control.name}: AUDIT PASS; "
            f"beta terms={len(beta.terms)}; replacement terms={len(replacement.terms)}"
        )

    print("independent normalized full-row audit: PASS (8/8)")
    print("implementation: standard-library sparse Laurent algebra over Q")
    print("matching-sum balanced-sensor realization: NOT CLAIMED")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
