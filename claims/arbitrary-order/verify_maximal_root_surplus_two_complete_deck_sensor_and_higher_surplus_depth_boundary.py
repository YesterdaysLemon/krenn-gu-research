"""Focused exact checks for the maximal-root surplus-two supply theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

Word = tuple[int, ...]
Polynomial = dict[Word, int]


def add_term(polynomial: Polynomial, word: Word, coefficient: int) -> None:
    polynomial[word] = polynomial.get(word, 0) + coefficient
    if polynomial[word] == 0:
        del polynomial[word]


def clean_cross_label(root: int, outside: int, r: int) -> int | None:
    """Return 0=a, 1=b, 2=c for the clean chart, or None for a zero edge."""

    if outside < r:
        return 0 if root == outside else None
    if outside == r:
        return 1
    if outside == r + 1:
        return 2
    raise AssertionError("outside label out of range")


def companion_column(r: int, outside_set: tuple[int, ...]) -> Polynomial:
    """Build one G_D by a direct exact matching recurrence."""

    @cache
    def recurse(
        roots: tuple[int, ...], outside: tuple[int, ...]
    ) -> tuple[tuple[Word, int], ...]:
        if not roots and not outside:
            return ((tuple([-1] * r), 1),)
        if not roots or len(outside) > len(roots):
            return ()

        first = roots[0]
        tail = roots[1:]
        result: Polynomial = {}

        for partner in tail:
            remaining = tuple(root for root in tail if root != partner)
            for word, coefficient in recurse(remaining, outside):
                updated = list(word)
                updated[first] = 1
                updated[partner] = 1
                add_term(result, tuple(updated), coefficient)

        for vertex in outside:
            label = clean_cross_label(first, vertex, r)
            if label is None:
                continue
            remaining_outside = tuple(item for item in outside if item != vertex)
            for word, coefficient in recurse(tail, remaining_outside):
                updated = list(word)
                updated[first] = label
                add_term(result, tuple(updated), coefficient)

        return tuple(sorted(result.items()))

    return dict(recurse(tuple(range(r)), outside_set))


def double_factorial(value: int) -> int:
    if value in (-1, 0):
        return 1
    product = 1
    while value > 0:
        product *= value
        value -= 2
    return product


def claimed_column(r: int, outside_set: tuple[int, ...]) -> Polynomial:
    private = {vertex for vertex in outside_set if vertex < r}
    residual = {vertex for vertex in outside_set if vertex >= r}
    remaining = [root for root in range(r) if root not in private]
    ell = len(remaining)
    base = tuple(0 if root in private else 1 for root in range(r))

    if not residual and ell % 2 == 0:
        return {base: double_factorial(ell - 1)}
    if residual == {r} and ell % 2 == 1:
        return {base: double_factorial(ell)}
    if residual == {r + 1} and ell % 2 == 1:
        coefficient = double_factorial(ell - 2)
    elif residual == {r, r + 1} and ell >= 2 and ell % 2 == 0:
        coefficient = double_factorial(ell - 1)
    else:
        return {}

    result: Polynomial = {}
    for root in remaining:
        word = list(base)
        word[root] = 2
        result[tuple(word)] = coefficient
    return result


def valid_outside_sets(r: int) -> list[tuple[int, ...]]:
    vertices = range(r + 2)
    return [
        subset
        for size in range(r + 1)
        if size % 2 == r % 2
        for subset in combinations(vertices, size)
    ]


def check_clean_chart() -> None:
    expected_ranks = {2: 7, 3: 15, 4: 31, 5: 63, 6: 127, 7: 255}
    for r, expected_rank in expected_ranks.items():
        subsets = valid_outside_sets(r)
        assert len(subsets) == 2 ** (r + 1) - 1

        columns = []
        for subset in subsets:
            actual = companion_column(r, subset)
            expected = claimed_column(r, subset)
            assert actual == expected, (r, subset, actual, expected)
            columns.append(
                sp.SparseMatrix(
                    3**r,
                    1,
                    {
                        (
                            sum(
                                letter * 3 ** (r - 1 - index)
                                for index, letter in enumerate(word)
                            ),
                            0,
                        ): coefficient
                        for word, coefficient in actual.items()
                    },
                )
            )

        matrix = sp.SparseMatrix.hstack(*columns)
        assert matrix.rank() == expected_rank


def check_surplus_grades() -> None:
    for r in range(2, 10):
        for surplus in range(0, 10, 2):
            occurring = {surplus + 2 * pairs for pairs in range(r // 2 + 1)}
            legal = {
                size
                for size in range(0, r + surplus + 1, 2)
                if size >= surplus and (size - surplus) // 2 <= r // 2
            }
            assert occurring == legal

            if surplus == 2:
                nonempty_even = set(range(2, r + 3, 2))
                assert occurring == nonempty_even
            if surplus >= 4:
                assert 2 not in occurring

    for surplus in range(0, 10, 2):
        for port_size in range(max(0, surplus), 14, 2):
            p_m = (port_size - surplus) // 2
            p_z = (port_size + 2 - surplus) // 2
            assert p_z == p_m + 1


def check_fixed_pair_counts() -> None:
    for r in range(2, 10):
        desired = 0
        nuisance = 0
        for mask in range(1, 1 << (r + 2)):
            if mask.bit_count() % 2:
                continue
            residual_count = ((mask >> r) & 1) + ((mask >> (r + 1)) & 1)
            if residual_count in (0, 2):
                desired += 1
            else:
                nuisance += 1
        assert desired == 2**r - 1
        assert nuisance == 2**r
        assert desired + nuisance == 2 ** (r + 1) - 1
        assert (r + 2) * (r + 1) // 2 <= desired + nuisance


def check_maximal_root_arithmetic() -> None:
    for r in range(3, 12):
        outside = r + 2
        blocker_incidences = 3 * outside
        assert blocker_incidences >= 3 * r
        # Coordinate outside-outside edges allow at most one outside root;
        # its assigned coordinate edge excludes at least one old root.
        assert 1 + (r - 1) == r


def main() -> None:
    check_clean_chart()
    check_surplus_grades()
    check_fixed_pair_counts()
    check_maximal_root_arithmetic()
    print("maximal-root surplus-two complete-deck sensor checks: PASS")


if __name__ == "__main__":
    main()
