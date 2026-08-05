"""Verify the exact mixed-jet parity classification on resonant root cliques."""

from __future__ import annotations

import json
from itertools import product

import sympy as sp

Vector = tuple[sp.Expr, sp.Expr, sp.Expr]


def hadamard(vectors: tuple[Vector, ...]) -> Vector:
    return tuple(sp.prod(vector[index] for vector in vectors) for index in range(3))  # type: ignore[return-value]


def quotient_column(vector: Vector) -> tuple[sp.Expr, sp.Expr]:
    return sp.expand(vector[0] - vector[2]), sp.expand(vector[1] - vector[2])


def image_rank(bases: tuple[tuple[Vector, Vector], ...]) -> int:
    columns = [quotient_column(hadamard(tuple(choice))) for choice in product(*bases)]
    return sp.Matrix(2, len(columns), lambda row, column: columns[column][row]).rank()


def uniform_basis(missing: int) -> tuple[Vector, Vector]:
    occupied = [index for index in range(3) if index != missing]
    anti = [sp.Integer(0)] * 3
    anti[occupied[0]] = 1
    anti[occupied[1]] = -1
    axis = [sp.Integer(0)] * 3
    axis[missing] = 1
    return tuple(anti), tuple(axis)  # type: ignore[return-value]


def axis_kernel(axis: int) -> tuple[Vector, Vector]:
    free = [index for index in range(3) if index != axis]
    first = [sp.Integer(0)] * 3
    second = [sp.Integer(0)] * 3
    first[free[0]] = 1
    second[free[1]] = 1
    return tuple(first), tuple(second)  # type: ignore[return-value]


def symbolic_formula() -> dict[str, str]:
    x, z, w = sp.symbols("x z w")
    even = (x, x, z)
    odd = (x, -x, z)
    constant = (w, w, w)
    even_relation = tuple(sp.expand(even[index] - ((x - z) * (1, 1, 0)[index] + z)) for index in range(3))
    if even_relation != (0, 0, 0):
        raise AssertionError(even_relation)
    odd_matrix = sp.Matrix([[1, 0, -1], [-1, 0, -1], [0, 1, -1]])
    if odd_matrix.det() != 2:
        raise AssertionError(odd_matrix.det())
    return {
        "even_product": str(even),
        "odd_product": str(odd),
        "odd_classes_plus_constant_determinant": str(odd_matrix.det()),
        "characteristic_zero_independence": str(constant),
    }


def uniform_checks() -> dict[str, object]:
    ranks: dict[str, list[int]] = {}
    for missing in range(3):
        basis = uniform_basis(missing)
        values = []
        for order in range(1, 11):
            rank = image_rank((basis,) * order)
            expected = 2 if order % 2 else 1
            if rank != expected:
                raise AssertionError((missing, order, rank, expected))
            values.append(rank)
        ranks[str(missing)] = values
    return {"orders": list(range(1, 11)), "ranks_by_common_zero": ranks}


def axis_checks() -> dict[str, object]:
    bases = tuple(axis_kernel(axis) for axis in range(3))
    pair_ranks = {}
    for left in range(3):
        for right in range(left + 1, 3):
            rank = image_rank((bases[left], bases[right]))
            if rank != 1:
                raise AssertionError((left, right, rank))
            pair_ranks[f"{left}{right}"] = rank
    triple_products = [hadamard(tuple(choice)) for choice in product(*bases)]
    if any(vector != (0, 0, 0) for vector in triple_products):
        raise AssertionError(triple_products)
    return {"pair_ranks": pair_ranks, "triple_product_zero": True}


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "symbolic_formula": symbolic_formula(),
                "uniform_balanced": uniform_checks(),
                "three_axes": axis_checks(),
                "third_jet_graph_realizability_proved": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
