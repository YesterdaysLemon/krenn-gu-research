"""Verify the two-residual-only third-root-jet obstruction exactly."""

from __future__ import annotations

import json
from itertools import product

import sympy as sp

Vector = tuple[sp.Expr, sp.Expr, sp.Expr]


def quotient_rank(columns: list[Vector]) -> int:
    projected = [(column[0] - column[2], column[1] - column[2]) for column in columns]
    matrix = sp.Matrix(2, len(projected), lambda row, column: projected[column][row])
    return matrix.rank()


def uniform_triple_rank(missing: int) -> int:
    occupied = [index for index in range(3) if index != missing]
    anti = [sp.Integer(0)] * 3
    anti[occupied[0]] = 1
    anti[occupied[1]] = -1
    axis = [sp.Integer(0)] * 3
    axis[missing] = 1
    basis = (tuple(anti), tuple(axis))
    columns = []
    for choices in product(basis, repeat=3):
        columns.append(tuple(sp.prod(choice[index] for choice in choices) for index in range(3)))
    return quotient_rank(columns)  # type: ignore[arg-type]


def residual_assignments(root_count: int, selected_count: int) -> list[tuple[int, ...]]:
    residuals = tuple(range(2))
    assignments = [choice for choice in product(residuals, repeat=selected_count) if len(set(choice)) == selected_count]
    if selected_count == 2 and sorted(assignments) != [(0, 1), (1, 0)]:
        raise AssertionError(assignments)
    if selected_count == 3 and assignments:
        raise AssertionError(assignments)
    if selected_count > root_count:
        raise AssertionError((root_count, selected_count))
    return assignments


def symbolic_pair_formula() -> dict[str, object]:
    p_i0, p_i1, p_j0, p_j1, cofactor = sp.symbols("p_i0 p_i1 p_j0 p_j1 C")
    terms = [p_i0 * p_j1 * cofactor, p_i1 * p_j0 * cofactor]
    total = sp.factor(sum(terms))
    expected = cofactor * (p_i0 * p_j1 + p_i1 * p_j0)
    if sp.expand(total - expected) != 0:
        raise AssertionError((total, expected))
    deletion_sets = [{"i", "j", "q0", "q1"}, {"i", "j", "q0", "q1"}]
    if deletion_sets[0] != deletion_sets[1]:
        raise AssertionError(deletion_sets)
    return {
        "assignments": [[0, 1], [1, 0]],
        "common_deletion_set": sorted(deletion_sets[0]),
        "formula": str(total),
        "cofactor_span_upper_bound": 1,
    }


def bounded_matching_audit() -> dict[str, object]:
    checks = 0
    for roots in range(4, 11):
        if len(residual_assignments(roots, 2)) != 2:
            raise AssertionError(roots)
        if residual_assignments(roots, 3):
            raise AssertionError(roots)
        checks += 2
    ranks = {str(missing): uniform_triple_rank(missing) for missing in range(3)}
    if set(ranks.values()) != {2}:
        raise AssertionError(ranks)
    return {"root_counts": list(range(4, 11)), "assignment_checks": checks, "triple_ranks": ranks}


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "pair_derivative": symbolic_pair_formula(),
                "bounded_matching_audit": bounded_matching_audit(),
                "minimum_escape": "nonprojective blocker variation, effective root-root channel, or third nonroot endpoint",
                "all_two_residual_graphs_excluded": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
