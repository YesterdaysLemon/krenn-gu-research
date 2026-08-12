"""Exact SymPy replay for the normalized full-row S2M controls.

The owning note gives the proof for the displayed families.  This verifier
builds all 27 target rows for every one of the eight retained coordinates and
checks the Cramer, degree, target, normalization, and jet claims exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import sympy as sp

X = sp.symbols("x0:3")
Y = sp.symbols("y0:3")
R = sp.symbols("r0:3")
VARIABLES = X + Y + R
WORDS = tuple(product(range(3), repeat=3))
ROW = {word: index for index, word in enumerate(WORDS)}
COLUMN_DEGREES = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))
OFF_ONE = (0, 0, 1)
OFF_TWO = (0, 1, 0)
OFF_THREE = (1, 0, 0)


@dataclass(frozen=True)
class Control:
    """One exact full-row control and its selected Cramer rows."""

    name: str
    gamma: sp.Matrix
    solution: sp.Matrix
    selected: tuple[tuple[int, int, int], ...]
    exceptional: tuple[str, int, int]


def ghz_target() -> sp.Matrix:
    """Return the exact 27-row contracted ternary GHZ target."""
    target = sp.zeros(27, 1)
    for colour in range(3):
        target[ROW[(colour, colour, colour)], 0] = (
            X[colour] * Y[colour] * R[colour]
        )
    return target


J = ghz_target()


def base_matrix() -> sp.Matrix:
    """Start with the normalized empty column on all diagonal target rows."""
    gamma = sp.zeros(27, 4)
    for colour in range(3):
        gamma[ROW[(colour, colour, colour)], 3] = J[
            ROW[(colour, colour, colour)], 0
        ]
    return gamma


def outside_control(index: int) -> Control:
    """Build the control for the nonpivot r_index first derivative."""
    gamma = base_matrix()
    diagonal = (index, index, index)
    gamma[ROW[diagonal], :] = sp.Matrix([[R[0], 0, 0, 0]])
    gamma[ROW[OFF_ONE], :] = sp.Matrix(
        [[-R[0], 0, 0, X[index] * Y[index] * R[index]]]
    )
    gamma[ROW[OFF_TWO], 1] = Y[0]
    gamma[ROW[OFF_THREE], 2] = X[0]
    solution = sp.Matrix(
        [R[index] * X[index] * Y[index] / R[0], 0, 0, 1]
    )
    return Control(
        name=f"outside-r{index}",
        gamma=gamma,
        solution=solution,
        selected=(diagonal, OFF_ONE, OFF_TWO, OFF_THREE),
        exceptional=("r", index, index),
    )


def x_endpoint_control(left: int, right: int) -> Control:
    """Build one nonpivot x-Hessian control."""
    gamma = base_matrix()
    diagonal = (left, left, left)
    gamma[ROW[OFF_ONE], :] = sp.Matrix([[R[left], 0, -X[right], 0]])
    gamma[ROW[diagonal], :] = sp.Matrix([[0, 0, X[0], 0]])
    gamma[ROW[OFF_TWO], 1] = Y[0]
    solution = sp.Matrix(
        [
            X[left] * X[right] * Y[left] / X[0],
            0,
            X[left] * Y[left] * R[left] / X[0],
            1,
        ]
    )
    return Control(
        name=f"endpoint-x{left}{right}",
        gamma=gamma,
        solution=solution,
        selected=(OFF_ONE, diagonal, (0, 0, 0), OFF_TWO),
        exceptional=("x", left, right),
    )


def y_endpoint_control(left: int, right: int) -> Control:
    """Build one nonpivot y-Hessian control."""
    gamma = base_matrix()
    diagonal = (left, left, left)
    gamma[ROW[OFF_ONE], :] = sp.Matrix([[R[left], -Y[right], 0, 0]])
    gamma[ROW[diagonal], :] = sp.Matrix([[0, Y[0], 0, 0]])
    gamma[ROW[OFF_TWO], 2] = X[0]
    solution = sp.Matrix(
        [
            X[left] * Y[left] * Y[right] / Y[0],
            X[left] * Y[left] * R[left] / Y[0],
            0,
            1,
        ]
    )
    return Control(
        name=f"endpoint-y{left}{right}",
        gamma=gamma,
        solution=solution,
        selected=(OFF_ONE, diagonal, (0, 0, 0), OFF_TWO),
        exceptional=("y", left, right),
    )


def controls() -> tuple[Control, ...]:
    """Return the two outside and six endpoint controls."""
    answer = [outside_control(index) for index in (1, 2)]
    answer.extend(
        x_endpoint_control(left, right)
        for left in (1, 2)
        for right in range(left, 3)
    )
    answer.extend(
        y_endpoint_control(left, right)
        for left in (1, 2)
        for right in range(left, 3)
    )
    return tuple(answer)


def group_degrees(expression: sp.Expr) -> set[tuple[int, int, int]]:
    """Return the group-degree triples of all nonzero monomials."""
    polynomial = sp.Poly(expression, *VARIABLES)
    return {
        (
            sum(monomial[:3]),
            sum(monomial[3:6]),
            sum(monomial[6:]),
        )
        for monomial, coefficient in polynomial.terms()
        if coefficient
    }


def retained_derivatives(pair_component: sp.Expr) -> dict[tuple[str, int, int], sp.Expr]:
    """Compute the eight retained affine-projective derivatives."""
    answer: dict[tuple[str, int, int], sp.Expr] = {
        ("r", index, index): sp.factor(sp.diff(pair_component, R[index]))
        for index in (1, 2)
    }
    for group_name, group in (("x", X), ("y", Y)):
        for left in (1, 2):
            for right in range(left, 3):
                answer[(group_name, left, right)] = sp.factor(
                    sp.diff(pair_component, group[left], group[right])
                )
    return answer


def first_residual(
    matrix: sp.Matrix,
    target: sp.Matrix,
    beta: sp.Expr,
    numerator: sp.Matrix,
    variable: sp.Symbol,
) -> sp.Matrix:
    """Compute q_D=beta Dj-(DA)v on the selected rows."""
    return beta * target.diff(variable) - matrix.diff(variable) * numerator


def hessian_residual(
    matrix: sp.Matrix,
    target: sp.Matrix,
    beta: sp.Expr,
    numerator: sp.Matrix,
    solution: sp.Matrix,
    first: sp.Symbol,
    second: sp.Symbol,
) -> sp.Matrix:
    """Compute the exact selected-row q_DE from the predecessor theorem."""
    stress_first = (solution.diff(first) * beta**2).applyfunc(sp.factor)
    stress_second = (solution.diff(second) * beta**2).applyfunc(sp.factor)
    return (
        beta**2 * target.diff(first).diff(second)
        - beta * matrix.diff(first).diff(second) * numerator
        - matrix.diff(first) * stress_second
        - matrix.diff(second) * stress_first
    ).applyfunc(sp.factor)


def replacement_determinant(matrix: sp.Matrix, replacement: sp.Matrix) -> sp.Expr:
    """Replace the xy column and return the exact determinant."""
    replaced = matrix.copy()
    replaced[:, 0] = replacement
    return sp.factor(replaced.det())


def verify_control(control: Control) -> tuple[sp.Expr, sp.Expr]:
    """Check every theorem claim for one control."""
    assert control.gamma * control.solution == J
    assert control.solution[3] == 1

    for column, expected in enumerate(COLUMN_DEGREES):
        for entry in control.gamma[:, column]:
            if entry != 0:
                assert group_degrees(entry) == {expected}

    selected_rows = [ROW[word] for word in control.selected]
    matrix = control.gamma.extract(selected_rows, range(4))
    target = J.extract(selected_rows, [0])
    beta = sp.factor(matrix.det())
    assert beta != 0
    assert all(
        sp.cancel(value) == 0
        for value in matrix * control.solution - target
    )

    numerator = matrix.adjugate() * target
    assert all(
        sp.cancel(numerator[index] - beta * control.solution[index]) == 0
        for index in range(4)
    )
    assert all(
        sp.cancel(value) == 0
        for value in control.gamma * numerator - beta * J
    )
    assert sp.factor(numerator[3] - beta) == 0

    derivatives = retained_derivatives(control.solution[0])
    nonzero = {
        coordinate: value
        for coordinate, value in derivatives.items()
        if value != 0
    }
    assert set(nonzero) == {control.exceptional}

    group_name, left, right = control.exceptional
    if group_name == "r":
        variable = R[left]
        residual = first_residual(matrix, target, beta, numerator, variable)
        replacement = replacement_determinant(matrix, residual)
        expected_replacement = sp.factor(
            beta**2 * sp.diff(control.solution[0], variable)
        )
    else:
        group = X if group_name == "x" else Y
        residual = hessian_residual(
            matrix,
            target,
            beta,
            numerator,
            control.solution,
            group[left],
            group[right],
        )
        replacement = replacement_determinant(matrix, residual)
        expected_replacement = sp.factor(
            beta**3
            * sp.diff(control.solution[0], group[left], group[right])
        )
    assert sp.factor(replacement - expected_replacement) == 0
    assert replacement != 0
    return beta, replacement


def main() -> None:
    """Replay all exact controls and print immutable scope markers."""
    all_controls = controls()
    assert len(all_controls) == 8
    for control in all_controls:
        beta, replacement = verify_control(control)
        print(
            f"{control.name}: PASS; beta={beta}; "
            f"exceptional replacement={replacement}"
        )

    print("normalized full-row compatibility controls: PASS (8/8)")
    print("matching-sum balanced-sensor realization: NOT CLAIMED")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
