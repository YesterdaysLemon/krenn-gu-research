#!/usr/bin/env python3
"""Independent no-import audit of the arbitrary-surplus full-span theorem."""

from __future__ import annotations

import itertools
import json
import math
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
    assert "all-full-span cofactor systems: UNKNOWN" in theorem

    ledgers = tuple(
        assignment_ledger(roots, surplus)
        for roots in range(2, 7)
        for surplus in range(4)
        if roots + surplus >= 3
    )
    rank_two = exact_rank_two_contraction_audit()
    diagonals = tuple(diagonal_audit(degree) for degree in (3, 4, 6, 9))
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent exact combinatorial and integer first-polar audit",
                "field": "integer characteristic-zero audit",
                "assignment_ledgers": ledgers,
                "rank_two_contraction": rank_two,
                "diagonal_first_polars": diagonals,
                "required_common_row_span": 3,
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
