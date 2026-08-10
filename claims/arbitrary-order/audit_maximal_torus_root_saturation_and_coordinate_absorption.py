"""Independent no-import audit for the maximal torus-root theorem.

This implementation uses labelled matching sets and a separate nullspace
calculation.  It audits bounded conventions only; the owning note contains
the arbitrary-order proof.
"""

from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(tuple(sorted((edge(first, second), *tail))))
    return tuple(answer)


def audit_labelled_bijection() -> None:
    for root_count, surplus in ((4, 2), (3, 4)):
        outside_count = root_count + surplus
        roots = set(range(root_count))
        outside = set(range(root_count, root_count + outside_count))
        signatures = {}
        for matching in matchings(tuple(range(2 * root_count + surplus))):
            if any(left in roots and right in roots for left, right in matching):
                continue
            injection = {}
            residual = []
            for left, right in matching:
                if left in roots:
                    injection[left] = right
                elif right in roots:
                    injection[right] = left
                else:
                    residual.append((left - root_count, right - root_count))
            assert set(injection) == roots
            image = set(injection.values())
            unused = tuple(sorted(vertex - root_count for vertex in outside - image))
            signature = (
                unused,
                tuple(injection[root] - root_count for root in range(root_count)),
                tuple(sorted(residual)),
            )
            assert signature not in signatures
            signatures[signature] = matching

        expected = 0
        for unused in combinations(range(outside_count), surplus):
            expected += factorial(root_count) * len(matchings(tuple(unused)))
        assert len(signatures) == expected


def factorial(value: int) -> int:
    answer = 1
    for factor in range(2, value + 1):
        answer *= factor
    return answer


def audit_incidence_optimization() -> None:
    for root_count in range(2, 9):
        for surplus in range(0, 7, 2):
            outside = root_count + surplus
            feasible = []
            for triple_count in range(outside + 1):
                for double_count in range(outside - triple_count + 1):
                    single_count = outside - triple_count - double_count
                    total_incidence = single_count + 2 * double_count + 3 * triple_count
                    if total_incidence >= 3 * root_count:
                        feasible.append((single_count, double_count, triple_count))
            for single_count, double_count, triple_count in feasible:
                missing_incidence = 2 * single_count + double_count
                assert missing_incidence <= 3 * surplus
                assert triple_count - single_count >= root_count - 2 * surplus


def rref(rows: list[list[Fraction]], columns: int = 3):
    work = [row[:] for row in rows]
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
    return work[:pivot_row], pivots


def nullspace(rows: list[list[Fraction]], columns: int = 3) -> list[list[Fraction]]:
    reduced, pivots = rref(rows, columns)
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * columns
        vector[free_column] = Fraction(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        basis.append(vector)
    return basis


def rank(rows: list[list[Fraction]]) -> int:
    return len(rref(rows)[1])


def same_span(left: list[list[Fraction]], right: list[list[Fraction]]) -> bool:
    common_rank = rank(left)
    return common_rank == rank(right) == rank([*left, *right])


def audit_coordinate_kernels() -> None:
    charts = {
        1: {
            "kernel": [[Fraction(1), Fraction(1), Fraction(1)]],
            "annihilator": [
                [Fraction(1), Fraction(-1), Fraction(0)],
                [Fraction(1), Fraction(0), Fraction(-1)],
            ],
        },
        2: {
            "kernel": [
                [Fraction(1), Fraction(-1), Fraction(0)],
                [Fraction(1), Fraction(0), Fraction(-1)],
            ],
            "annihilator": [[Fraction(1), Fraction(1), Fraction(1)]],
        },
        3: {
            "kernel": [
                [Fraction(1), Fraction(0), Fraction(0)],
                [Fraction(0), Fraction(1), Fraction(0)],
                [Fraction(0), Fraction(0), Fraction(1)],
            ],
            "annihilator": [],
        },
    }
    for kernel_dimension, chart in charts.items():
        old_kernel = chart["kernel"]
        old_rows = chart["annihilator"]
        assert same_span(nullspace(old_rows), old_kernel)
        for side in range(2):
            for coordinate_index in range(3):
                axis = [Fraction(int(index == coordinate_index)) for index in range(3)]
                scalar = Fraction(2 + side)
                old_part = old_rows[-1] if old_rows else [Fraction(0)] * 3
                promoted_row = [
                    old_part[index] + scalar * axis[index] for index in range(3)
                ]
                promoted_rows = [*old_rows, promoted_row]
                expected_rows = [*old_rows, axis]
                assert same_span(promoted_rows, expected_rows)
                promoted_kernel = nullspace(promoted_rows)
                expected_kernel = nullspace(expected_rows)
                assert same_span(promoted_kernel, expected_kernel)
                assert len(promoted_kernel) == kernel_dimension - 1


def main() -> None:
    audit_labelled_bijection()
    audit_incidence_optimization()
    audit_coordinate_kernels()
    print("independent maximal torus-root audit: PASS")
    print("labelled matching bijection checked on two ten-vertex ledgers")
    print("no import from primary verifier; exact Fraction nullspaces")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
