"""Focused exact checks for maximal-root saturation and coordinate absorption.

The written theorem is arbitrary-order.  These bounded checks audit the
fixed-surplus matching ledger, incidence signs, and promotion linear algebra;
they do not enumerate graph or support families.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations

Label = tuple[str, int, int]
Monomial = tuple[Label, ...]


def polynomial_matchings(
    vertices: tuple[int, ...],
    edge_label,
) -> Counter[Monomial]:
    if not vertices:
        return Counter({(): 1})
    first = vertices[0]
    answer: Counter[Monomial] = Counter()
    for position in range(1, len(vertices)):
        second = vertices[position]
        label = edge_label(first, second)
        if label is None:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for monomial, coefficient in polynomial_matchings(rest, edge_label).items():
            answer[tuple(sorted((label, *monomial)))] += coefficient
    return answer


def direct_survivor_polynomial(r: int, surplus: int) -> Counter[Monomial]:
    outside_count = r + surplus
    vertices = tuple(range(r + outside_count))

    def edge_label(left: int, right: int):
        if left > right:
            left, right = right, left
        if right < r:
            return None
        if left < r:
            return ("h", left, right - r)
        return ("w", left - r, right - r)

    return polynomial_matchings(vertices, edge_label)


def factored_survivor_polynomial(r: int, surplus: int) -> Counter[Monomial]:
    outside = tuple(range(r + surplus))
    answer: Counter[Monomial] = Counter()
    for unused in combinations(outside, surplus):
        unused_set = set(unused)
        used = tuple(vertex for vertex in outside if vertex not in unused_set)

        def outside_edge(left: int, right: int) -> Label:
            if left > right:
                left, right = right, left
            return ("w", left, right)

        residual = polynomial_matchings(unused, outside_edge)
        for assignment in permutations(used):
            root_edges = tuple(sorted(("h", root, target) for root, target in enumerate(assignment)))
            for residual_edges, coefficient in residual.items():
                answer[tuple(sorted((*root_edges, *residual_edges)))] += coefficient
    return answer


def check_matching_ledger() -> None:
    cases = ((1, 0), (1, 2), (2, 0), (2, 2), (2, 4), (3, 0), (3, 2), (3, 4))
    for r, surplus in cases:
        direct = direct_survivor_polynomial(r, surplus)
        factored = factored_survivor_polynomial(r, surplus)
        assert direct == factored, (r, surplus)
        assert set(direct.values()) == {1}


def check_incidence_bounds() -> None:
    for r in range(2, 9):
        for surplus in range(0, 7, 2):
            outside = r + surplus
            for t1 in range(outside + 1):
                for t2 in range(outside - t1 + 1):
                    t3 = outside - t1 - t2
                    incidence = t1 + 2 * t2 + 3 * t3
                    if incidence < 3 * r:
                        continue
                    assert 2 * t1 + t2 <= 3 * surplus
                    assert t3 - t1 >= r - 2 * surplus
                    worst_corank = 2 * t1 + t2
                    assert worst_corank <= 3 * surplus


def rank(rows: list[list[Fraction]], columns: int = 3) -> int:
    work = [row[:] for row in rows]
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
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def coordinate(index: int) -> list[Fraction]:
    return [Fraction(int(position == index)) for position in range(3)]


def check_coordinate_promotion() -> None:
    annihilators = {
        1: [
            [Fraction(1), Fraction(-1), Fraction(0)],
            [Fraction(1), Fraction(0), Fraction(-1)],
        ],
        2: [[Fraction(1), Fraction(1), Fraction(1)]],
        3: [],
    }
    for kernel_dimension, old_rows in annihilators.items():
        old_rank = rank(old_rows)
        assert old_rank == 3 - kernel_dimension
        for endpoint_colour in range(3):
            axis = coordinate(endpoint_colour)
            for promoted_colour in range(3):
                scalar = Fraction(promoted_colour + 2)
                old_part = old_rows[0] if old_rows else [Fraction(0)] * 3
                g = [old_part[index] + scalar * axis[index] for index in range(3)]
                new_rows = [*old_rows, g]
                assert rank(new_rows) == old_rank + 1
                assert rank([*new_rows, axis]) == old_rank + 1
                difference = [g[index] - scalar * axis[index] for index in range(3)]
                assert rank([*old_rows, difference]) == old_rank
                assert 3 - rank(new_rows) == kernel_dimension - 1


def main() -> None:
    check_matching_ledger()
    check_incidence_bounds()
    check_coordinate_promotion()
    print("maximal torus-root focused verification: PASS")
    print("fixed-surplus matching ledger checked through ten vertices")
    print("coordinate promotion checked with exact rational row reduction")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
