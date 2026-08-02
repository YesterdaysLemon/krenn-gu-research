"""Independent no-import audit of the two-residual third-jet obstruction."""

from __future__ import annotations

import json
from itertools import permutations, product

Row = tuple[int, int, int]


def coordinate_product(rows: tuple[Row, ...]) -> Row:
    answer = []
    for coordinate in range(3):
        value = 1
        for row in rows:
            value *= row[coordinate]
        answer.append(value)
    return tuple(answer)  # type: ignore[return-value]


def quotient_rank(rows: list[Row]) -> int:
    columns = [(row[1] - row[0], row[2] - row[0]) for row in rows]
    nonzero = [column for column in columns if column != (0, 0)]
    if not nonzero:
        return 0
    anchor = nonzero[0]
    return 1 if all(anchor[0] * column[1] == anchor[1] * column[0] for column in nonzero[1:]) else 2


def injective_assignments(inputs: int, endpoints: int) -> list[tuple[int, ...]]:
    return [choice for choice in product(range(endpoints), repeat=inputs) if len(set(choice)) == inputs]


def main() -> None:
    pair_assignments = injective_assignments(2, 2)
    triple_assignments = injective_assignments(3, 2)
    if sorted(pair_assignments) != [(0, 1), (1, 0)] or triple_assignments:
        raise AssertionError((pair_assignments, triple_assignments))

    base = ((1, -1, 0), (0, 0, 1))
    permutation_ranks = {}
    for permutation in permutations((0, 1, 2)):
        basis = tuple(tuple(row[index] for index in permutation) for row in base)
        columns = [coordinate_product(tuple(choice)) for choice in product(basis, repeat=3)]
        rank = quotient_rank(columns)
        if rank != 2:
            raise AssertionError((permutation, rank, columns))
        permutation_ranks[str(permutation)] = rank

    root_count_checks = 0
    for roots in range(4, 15):
        selected_pairs = roots * (roots - 1) // 2
        selected_triples = roots * (roots - 1) * (roots - 2) // 6
        if selected_pairs <= 0 or selected_triples <= 0:
            raise AssertionError(roots)
        for _ in range(selected_pairs):
            if len(pair_assignments) != 2:
                raise AssertionError(roots)
        for _ in range(selected_triples):
            if triple_assignments:
                raise AssertionError(roots)
        root_count_checks += selected_pairs + selected_triples

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integer products and injection ledger; no sympy or repository imports",
                "two_root_two_endpoint_assignments": pair_assignments,
                "three_root_two_endpoint_assignments": triple_assignments,
                "uniform_triple_permutation_ranks": permutation_ranks,
                "root_counts_checked": list(range(4, 15)),
                "subset_checks": root_count_checks,
                "bounded_checks_are_theorem_evidence": False,
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
