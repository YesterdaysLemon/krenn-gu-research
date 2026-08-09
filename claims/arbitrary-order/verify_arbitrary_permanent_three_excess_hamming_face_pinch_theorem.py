"""Primary symbolic checks for the Hamming-face pinch theorem."""

from __future__ import annotations

from itertools import combinations, permutations

import sympy as sp


def permanent(matrix: sp.Matrix) -> sp.Expr:
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            sp.prod(matrix[row, permutation[row]] for row in range(matrix.rows))
            for permutation in permutations(range(matrix.cols))
        )
    )


def complementary(matrix: sp.Matrix, selected: set[int]) -> sp.Matrix:
    retained = [index for index in range(matrix.rows) if index not in selected]
    return matrix.extract(retained, retained)


def main() -> None:
    symbols = sp.symbols("x11:14 x21:24 x31:34")
    generic = sp.Matrix(3, 3, symbols)
    z = sp.symbols("z0:3", nonzero=True)
    for size in range(4):
        for subset_tuple in combinations(range(3), size):
            subset = set(subset_tuple)
            replaced = generic.copy()
            for row in subset:
                for column in range(3):
                    replaced[row, column] = z[row] if row == column else 0
            expected = sp.prod(z[row] for row in subset) * permanent(
                complementary(generic, subset)
            )
            assert sp.expand(permanent(replaced) - expected) == 0

    root_two = sp.sqrt(2)
    bypass = sp.Matrix(
        [
            [1, 1, 1 - root_two],
            [-1, 1, 1],
            [1 + root_two, -1, 1],
        ]
    )
    assert permanent(bypass) == 0
    assert all(permanent(complementary(bypass, {index})) == 0 for index in range(3))
    for pair in combinations(range(3), 2):
        remaining = ({0, 1, 2} - set(pair)).pop()
        coefficient = sp.prod(z[index] for index in pair) * permanent(
            complementary(bypass, set(pair))
        )
        expected = sp.prod(z[index] for index in pair) * bypass[remaining, remaining]
        assert sp.simplify(coefficient - expected) == 0
        assert bypass[remaining, remaining] != 0

    t = sp.symbols("t0:3")
    pinched = bypass + sp.diag(*[z[index] * t[index] for index in range(3)])
    expected_polynomial = (
        z[0] * z[1] * t[0] * t[1]
        + z[0] * z[2] * t[0] * t[2]
        + z[1] * z[2] * t[1] * t[2]
        + z[0] * z[1] * z[2] * t[0] * t[1] * t[2]
    )
    assert sp.expand(permanent(pinched) - expected_polynomial) == 0

    phase_u, phase_v = sp.symbols("phase_u phase_v")
    solutions = sp.solve(
        [phase_u + phase_v - 2, phase_u * phase_v + 1],
        [phase_u, phase_v],
        dict=True,
    )
    expected_solutions = {
        (1 - root_two, 1 + root_two),
        (1 + root_two, 1 - root_two),
    }
    assert {
        (sp.simplify(solution[phase_u]), sp.simplify(solution[phase_v]))
        for solution in solutions
    } == expected_solutions

    # e_alpha, e_beta, and an excess vector have full rank exactly when the
    # excess has a nonzero component in the third colour.
    e_alpha = sp.Matrix([[1, 0, 0]])
    e_beta = sp.Matrix([[0, 1, 0]])
    u, v, gamma = sp.symbols("u v gamma")
    local = sp.Matrix.vstack(e_alpha, e_beta, sp.Matrix([[u, v, gamma]]))
    assert sp.det(local) == gamma

    print("arbitrary permanent Hamming-face pinch theorem: PASS")
    print("symbolic face identity only; no input-word or support-family census was performed")


if __name__ == "__main__":
    main()
