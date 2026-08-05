"""Exact Jacobian certificate for dominance of the three-port boundary jet."""

from __future__ import annotations

from itertools import combinations, permutations

import sympy as sp


EXPECTED_DETERMINANT = 10622643353619573315207168
PIVOT_COLUMNS = tuple(range(17)) + (18, 19, 20)


def permanent(matrix: sp.Matrix) -> sp.Expr:
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            sp.prod(matrix[row, permutation[row]] for row in range(matrix.rows))
            for permutation in permutations(range(matrix.rows))
        )
    )


def response_coordinates(
    y: sp.Matrix,
    z: sp.Matrix,
    w: sp.Matrix,
) -> list[sp.Expr]:
    coordinates: list[sp.Expr] = []
    universe = tuple(range(3))
    for degree in range(4):
        subsets = tuple(combinations(universe, degree))
        for core_modes in subsets:
            for core_sources in subsets:
                response = sp.Integer(0)
                for exterior_rows in subsets:
                    remaining_rows = tuple(
                        index for index in universe if index not in exterior_rows
                    )
                    for exterior_columns in subsets:
                        remaining_columns = tuple(
                            index for index in universe if index not in exterior_columns
                        )
                        response += (
                            permanent(y.extract(core_modes, exterior_columns))
                            * permanent(z.extract(exterior_rows, core_sources))
                            * permanent(w.extract(remaining_rows, remaining_columns))
                        )
                coordinates.append(sp.expand(response))
    return coordinates


def main() -> None:
    y_parameters = sp.symbols("y00:09")
    z_parameters = sp.symbols("z00:09")
    w_parameters = sp.symbols("w00:09")
    parameters = y_parameters + z_parameters + w_parameters
    y = sp.Matrix(3, 3, y_parameters)
    z = sp.Matrix(3, 3, z_parameters)
    w = sp.Matrix(3, 3, w_parameters)

    coordinates = response_coordinates(y, z, w)
    assert len(coordinates) == 20
    jacobian = sp.Matrix(coordinates).jacobian(parameters)

    point_values = (
        1, 2, 0,
        0, 1, 3,
        2, 0, 1,
        1, 0, 2,
        3, 1, 0,
        0, 2, 1,
        2, 1, 0,
        1, 3, 2,
        0, 1, 4,
    )
    point = dict(zip(parameters, point_values, strict=True))
    evaluated = jacobian.subs(point)
    certificate_minor = evaluated[:, list(PIVOT_COLUMNS)]
    determinant = int(certificate_minor.det(method="domain-ge"))

    assert determinant == EXPECTED_DETERMINANT
    assert sp.factorint(determinant) == {
        2: 31,
        3: 5,
        7: 2,
        11: 4,
        13: 2,
        379: 1,
        443: 1,
    }
    assert evaluated.rank() == 20

    print("three-port boundary-jet dominance certificate: PASS")
    print(f"exact 20x20 Jacobian determinant = {determinant}")
    print("characteristic-zero symbolic rank only; no response-family census")


if __name__ == "__main__":
    main()
