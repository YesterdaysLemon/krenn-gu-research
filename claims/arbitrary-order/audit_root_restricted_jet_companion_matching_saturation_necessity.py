"""Independent no-import audit of restricted-jet matching saturation."""

from __future__ import annotations

import json
from functools import cache
from itertools import product
from math import gcd

Row = tuple[int, int, int]


@cache
def matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    anchor = vertices[-1]
    answer = []
    for index, partner in enumerate(vertices[:-1]):
        remaining = vertices[:index] + vertices[index + 1 : -1]
        for partial in matchings(remaining):
            answer.append(partial + ((partner, anchor),))
    return tuple(answer)


def primitive(row: Row) -> Row:
    common = 0
    for value in row:
        common = gcd(common, abs(value))
    answer = tuple(value // common for value in row)
    leading = next(value for value in answer if value)
    if leading < 0:
        answer = tuple(-value for value in answer)
    return answer  # type: ignore[return-value]


def null_rows(row: Row) -> tuple[Row, Row]:
    pivot = max(range(3), key=lambda index: abs(row[index]))
    answer = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [0, 0, 0]
        vector[free] = row[pivot]
        vector[pivot] = -row[free]
        answer.append(tuple(vector))
    return answer[0], answer[1]  # type: ignore[return-value]


def pointwise_zero(rows: tuple[Row, ...]) -> bool:
    bases = tuple(null_rows(row) for row in rows)
    for choice in product(*bases):
        values = []
        for coordinate in range(3):
            value = 1
            for vector in choice:
                value *= vector[coordinate]
            values.append(value)
        if values != [0, 0, 0]:
            return False
    return True


def axis(row: Row) -> int | None:
    support = [index for index, value in enumerate(row) if value]
    return support[0] if len(support) == 1 else None


def main() -> None:
    rows = sorted(
        {
            primitive(row)
            for row in product(range(-3, 4), repeat=3)
            if row != (0, 0, 0) and sum(row) != 0
        }
    )
    axes = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    zero_checks = 0
    for row in rows:
        for sample in ((axes[0], axes[1], row), (axes[0], axes[2], row), (row,)):
            predicted = {axis(item) for item in sample} >= {0, 1, 2}
            if pointwise_zero(sample) != predicted:
                raise AssertionError(sample)
            zero_checks += 1

    matching_count = 0
    saturation_checks = 0
    for order in range(2, 13, 2):
        for matching in matchings(tuple(range(order))):
            for varied_size in range(1, min(order, 7)):
                varied = set(range(varied_size))
                incident = [edge for edge in matching if edge[0] in varied or edge[1] in varied]
                covered = {vertex for edge in incident for vertex in edge}
                if not varied <= covered:
                    raise AssertionError((matching, varied, incident))
                saturation_checks += 1
            matching_count += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integer kernels and anchored matching recursion; no sympy or repository imports",
                "projective_covectors": len(rows),
                "zero_product_checks": zero_checks,
                "perfect_matchings": matching_count,
                "saturation_checks": saturation_checks,
                "maximum_vertices": 12,
                "bounded_checks_are_theorem_evidence": False,
                "saturating_matching_sufficient": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
