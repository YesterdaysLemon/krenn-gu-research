"""Independent no-import audit for the resonant mixed-jet parity theorem."""

from __future__ import annotations

import json
from itertools import permutations, product

Row = tuple[int, int, int]


def pointwise(words: tuple[Row, ...]) -> Row:
    return tuple(product_entry(words, coordinate) for coordinate in range(3))  # type: ignore[return-value]


def product_entry(words: tuple[Row, ...], coordinate: int) -> int:
    answer = 1
    for word in words:
        answer *= word[coordinate]
    return answer


def quotient_rank(columns: list[Row]) -> int:
    projected = [(column[1] - column[0], column[2] - column[0]) for column in columns]
    nonzero = [column for column in projected if column != (0, 0)]
    if not nonzero:
        return 0
    anchor = nonzero[0]
    if all(anchor[0] * column[1] == anchor[1] * column[0] for column in nonzero[1:]):
        return 1
    return 2


def tensor_columns(bases: tuple[tuple[Row, Row], ...]) -> list[Row]:
    return [pointwise(tuple(choice)) for choice in product(*bases)]


def permute(row: Row, permutation: tuple[int, int, int]) -> Row:
    return tuple(row[index] for index in permutation)  # type: ignore[return-value]


def main() -> None:
    base_uniform = ((1, -1, 0), (0, 0, 1))
    uniform_checks = 0
    for permutation in permutations((0, 1, 2)):
        basis = tuple(permute(row, permutation) for row in base_uniform)
        for order in range(1, 16):
            actual = quotient_rank(tensor_columns((basis,) * order))
            expected = 2 if order % 2 else 1
            if actual != expected:
                raise AssertionError((permutation, order, actual, expected))
            uniform_checks += 1

    base_axes = (
        ((0, 1, 0), (0, 0, 1)),
        ((1, 0, 0), (0, 0, 1)),
        ((1, 0, 0), (0, 1, 0)),
    )
    axis_permutation_checks = 0
    for permutation in permutations((0, 1, 2)):
        bases = tuple(tuple(permute(row, permutation) for row in basis) for basis in base_axes)
        for left in range(3):
            for right in range(left + 1, 3):
                if quotient_rank(tensor_columns((bases[left], bases[right]))) != 1:
                    raise AssertionError((permutation, left, right))
        if any(column != (0, 0, 0) for column in tensor_columns(bases)):
            raise AssertionError(permutation)
        axis_permutation_checks += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integer tensor products; no sympy or repository imports",
                "uniform_orders_checked": list(range(1, 16)),
                "uniform_coordinate_permutation_checks": uniform_checks,
                "axis_pattern_permutation_checks": axis_permutation_checks,
                "uniform_odd_rank": 2,
                "uniform_even_rank": 1,
                "axis_pair_rank": 1,
                "axis_triple_product_zero": True,
                "bounded_checks_are_theorem_evidence": False,
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
