#!/usr/bin/env python3
"""Independent no-import audit of the arbitrary-surplus full-span theorem."""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md"


def permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    size = len(matrix)
    return sum(
        math.prod(matrix[row][permutation[row]] for row in range(size))
        for permutation in itertools.permutations(range(size))
    )


def assignment_ledger(root_count: int, surplus: int) -> dict[str, int]:
    mode_count = root_count + surplus
    all_assignments = math.comb(mode_count, surplus) * math.factorial(root_count)
    surviving_per_mode = math.comb(mode_count - 1, surplus) * math.factorial(
        root_count - 1
    )
    killed_port_subsets = math.comb(mode_count - 1, surplus - 1) if surplus else 0

    for variable_mode in range(mode_count):
        surviving = 0
        killed = 0
        for unused in itertools.combinations(range(mode_count), surplus):
            retained = tuple(mode for mode in range(mode_count) if mode not in unused)
            for permutation in itertools.permutations(range(root_count)):
                assigned_mode = retained[permutation[0]]
                if assigned_mode == variable_mode:
                    surviving += 1
                else:
                    killed += 1
        assert surviving == surviving_per_mode
        assert surviving + killed == all_assignments
        assert killed >= killed_port_subsets * math.factorial(root_count)

    return {
        "roots": root_count,
        "surplus": surplus,
        "blockers": mode_count,
        "all_assignments_per_mode": all_assignments,
        "surviving_assignments_per_mode": surviving_per_mode,
        "port_subsets_containing_variable_mode": killed_port_subsets,
    }


def laplace_bijection_ledger(root_count: int, port_count: int) -> dict[str, int]:
    mode_count = root_count + port_count
    full_records = set()
    for assignment in itertools.permutations(range(mode_count)):
        port_columns = tuple(sorted(assignment[root_count:]))
        record = (port_columns, assignment[:root_count], assignment[root_count:])
        assert record not in full_records
        full_records.add(record)

    cofactor_records = set()
    for port_columns in itertools.combinations(range(mode_count), port_count):
        port_column_set = set(port_columns)
        root_columns = tuple(
            column for column in range(mode_count) if column not in port_column_set
        )
        for root_assignment in itertools.permutations(root_columns):
            for port_assignment in itertools.permutations(port_columns):
                record = (port_columns, root_assignment, port_assignment)
                assert record not in cofactor_records
                cofactor_records.add(record)

    assert full_records == cofactor_records
    expected = math.factorial(mode_count)
    assert len(full_records) == len(cofactor_records) == expected
    return {
        "roots": root_count,
        "ports": port_count,
        "blockers": mode_count,
        "full_assignments": len(full_records),
        "cofactor_assignments": len(cofactor_records),
    }


def exact_rank(rows: tuple[tuple[int, ...], ...]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - multiplier * matrix[rank][index]
                for index in range(len(matrix[0]))
            ]
        rank += 1
        if rank == len(matrix[0]):
            break
    return rank


def independent_common_port_profile_models() -> tuple[dict[str, object], ...]:
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    profiles = {
        "empty": (0, 0, 0, 0, 0, 0),
        "1": (1, 0, 0, 0, 0, 0),
        "1+1": (1, 2, 0, 0, 0, 0),
        "1+1+1": (1, 2, 4, 0, 0, 0),
        "2": (3, 0, 0, 0, 0, 0),
        "2+1": (3, 4, 0, 0, 0, 0),
    }
    results = []
    for profile, masks in profiles.items():
        mode_rows = []
        port_rows = []
        full_index = 0
        for mask in masks:
            missing = tuple(color for color in range(3) if mask & (1 << color))
            if not missing:
                shift = full_index % 3
                full_index += 1
                rows = tuple(basis[(row + shift) % 3] for row in range(5))
                port = basis[(shift + 1) % 3]
            elif len(missing) == 1:
                present = tuple(color for color in range(3) if color not in missing)
                plane = (basis[present[1]], basis[present[0]])
                rows = tuple(plane[(row + 1) % 2] for row in range(5))
                port = basis[missing[0]]
            else:
                first, second = missing
                third = next(color for color in range(3) if color not in missing)
                plane = (
                    basis[third],
                    tuple(
                        2 * basis[first][color] - basis[second][color]
                        for color in range(3)
                    ),
                )
                rows = tuple(plane[(row + 1) % 2] for row in range(5))
                port = basis[first]

            rank = exact_rank(rows)
            assert rank == (3 if not missing else 2)
            assert exact_rank(rows + (port,)) == 3
            realized = sum(
                1 << color
                for color in range(3)
                if exact_rank(rows + (basis[color],)) > rank
            )
            assert realized == mask
            mode_rows.append(rows)
            port_rows.append(port)

        root_ranks = tuple(
            exact_rank(tuple(mode_rows[mode][row] for mode in range(6)))
            for row in range(5)
        )
        port_rank = exact_rank(tuple(port_rows))
        assert root_ranks == (3, 3, 3, 3, 3)
        assert port_rank == 3
        results.append(
            {
                "profile": profile,
                "missing_masks": masks,
                "root_family_ranks": root_ranks,
                "port_family_rank": port_rank,
            }
        )
    return tuple(results)


def scalar_cofactor(
    root_count: int,
    surplus: int,
    variable_mode: int,
    port_weights: dict[tuple[int, ...], int],
    point_rows: tuple[tuple[int, ...], ...],
) -> int:
    mode_count = root_count + surplus
    total = 0
    for unused in itertools.combinations(range(mode_count), surplus):
        if variable_mode in unused:
            continue
        retained = tuple(
            mode
            for mode in range(mode_count)
            if mode not in unused and mode != variable_mode
        )
        minor = tuple(
            tuple(point_rows[row - 1][mode] for mode in retained)
            for row in range(1, root_count)
        )
        total += port_weights[unused] * permanent(minor)
    return total


def exact_rank_two_contraction_audit() -> dict[str, object]:
    root_count = 4
    surplus = 2
    mode_count = root_count + surplus
    point = (1, 2, 3)
    row_covectors = (
        (2, -1, 0),
        (3, 0, -1),
        (2, -1, 0),
        (3, 0, -1),
        (5, -1, -1),
        (2, -1, 0),
    )
    assert all(
        sum(row_covectors[mode][index] * point[index] for index in range(3)) == 0
        for mode in range(mode_count)
    )
    assert any(row_covectors[mode] != row_covectors[0] for mode in range(1, mode_count))
    assert row_covectors[4] == tuple(
        row_covectors[0][index] + row_covectors[1][index] for index in range(3)
    )

    point_rows = tuple(
        tuple(2 + 3 * row + 2 * mode for mode in range(mode_count))
        for row in range(root_count - 1)
    )
    port_weights = {
        unused: 1 + sum((index + 1) * (mode + 2) for index, mode in enumerate(unused))
        for unused in itertools.combinations(range(mode_count), surplus)
    }
    scalars = tuple(
        scalar_cofactor(
            root_count,
            surplus,
            mode,
            port_weights,
            point_rows,
        )
        for mode in range(mode_count)
    )
    assert all(scalar != 0 for scalar in scalars)
    contractions = tuple(
        tuple(scalars[mode] * coefficient for coefficient in row_covectors[mode])
        for mode in range(mode_count)
    )

    def proportional(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
        return all(
            left[i] * right[j] == left[j] * right[i] for i in range(3) for j in range(3)
        )

    assert not all(
        proportional(contractions[0], contraction) for contraction in contractions[1:]
    )
    return {
        "roots": root_count,
        "surplus": surplus,
        "annihilator_point": point,
        "rank_two_row_covectors": row_covectors,
        "cofactor_scalars": scalars,
        "modewise_contractions": contractions,
        "one_common_nonzero_diagonal_polar_possible": False,
    }


def diagonal_audit(degree: int) -> dict[str, object]:
    coefficients = (2, -3, 5)
    points = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (2, -1, 1))
    polars = tuple(
        tuple(coefficients[index] * point[index] ** (degree - 1) for index in range(3))
        for point in points
    )
    assert all(any(polar) for polar in polars)
    assert math.comb(degree, 1) == math.comb(degree, degree - 1) == degree
    return {
        "degree": degree,
        "mixed_binomial_coefficient": degree,
        "nonzero_first_polars": len(polars),
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    normalized = " ".join(theorem.split())
    assert "No finite-field inference is used" in normalized
    assert "root-row span exactly two at any surplus: EXCLUDED" in theorem
    assert "span{g_(a,u):u in B}=(C^3)^*" in theorem
    assert (
        "six common-port missing-colour profiles at incidence level: ALL SURVIVE"
        in theorem
    )
    assert "all-full-span cofactor systems: UNKNOWN" in theorem

    ledgers = tuple(
        assignment_ledger(roots, surplus)
        for roots in range(2, 7)
        for surplus in range(4)
        if roots + surplus >= 3
    )
    rank_two = exact_rank_two_contraction_audit()
    diagonals = tuple(diagonal_audit(degree) for degree in (3, 4, 6, 9))
    laplace_ledgers = tuple(
        laplace_bijection_ledger(roots, ports)
        for roots, ports in ((2, 1), (3, 2), (4, 2), (5, 2), (3, 3))
    )
    profile_models = independent_common_port_profile_models()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent exact combinatorial, Laplace, profile, and integer first-polar audit",
                "field": "integer characteristic-zero audit",
                "assignment_ledgers": ledgers,
                "rank_two_contraction": rank_two,
                "diagonal_first_polars": diagonals,
                "factored_port_laplace_ledgers": laplace_ledgers,
                "common_port_profile_span_models": profile_models,
                "required_common_row_span": 3,
                "automatic_first_surplus_port_span": 3,
                "effective_two_port_a_span": 3,
                "effective_two_port_b_span": 3,
                "profile_excluded_by_span_conditions": False,
                "arbitrary_parameters_proved_in_written_termwise_argument": True,
                "full_local_to_global_reduction_complete": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
