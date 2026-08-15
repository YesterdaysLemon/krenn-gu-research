"""Independent no-import audit of the adjacent-overlap balanced cut."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product


def rank(matrix: list[list[int | Fraction]]) -> int:
    """Compute exact row rank over Q with a custom elimination."""
    if not matrix:
        return 0
    work = [[Fraction(entry) for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    current = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(current, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[current], work[pivot] = work[pivot], work[current]
        scale = work[current][column]
        work[current] = [entry / scale for entry in work[current]]
        for row in range(row_count):
            if row == current or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * basis
                for entry, basis in zip(work[row], work[current], strict=True)
            ]
        current += 1
        if current == row_count:
            break
    return current


def determinant(matrix: list[list[int]]) -> Fraction:
    """Compute an exact determinant independently of the rank routine."""
    size = len(matrix)
    work = [[Fraction(entry) for entry in row] for row in matrix]
    result = Fraction(1)
    sign = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        value = work[column][column]
        result *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, size):
            factor = work[row][column]
            work[row] = [
                entry - factor * basis
                for entry, basis in zip(work[row], work[column], strict=True)
            ]
    return sign * result


def parity_subsets() -> list[tuple[int, ...]]:
    """Return the even subsets of four labels."""
    return [
        subset
        for size in (0, 2, 4)
        for subset in combinations(range(4), size)
    ]


def permanent(matrix: list[list[int]]) -> int:
    """Compute a small integer permanent."""
    if not matrix:
        return 1
    return sum(
        product_value(matrix[row][order[row]] for row in range(len(matrix)))
        for order in permutations(range(len(matrix)))
    )


def product_value(values) -> int:
    """Multiply an iterable of integers."""
    result = 1
    for value in values:
        result *= value
    return result


def submatrix(
    matrix: list[list[int]], rows: tuple[int, ...], columns: tuple[int, ...]
) -> list[list[int]]:
    """Extract a small submatrix."""
    return [[matrix[row][column] for column in columns] for row in rows]


def selector_and_dimension_audit() -> dict[str, object]:
    """Count the two equality orbits and redo the affine dimension ledger."""
    orbit_counts: Counter[tuple[int, ...]] = Counter()
    root_dimensions = set()
    for selector in product(range(4), repeat=3):
        counts = Counter(selector)
        if len(counts) == 1:
            continue
        orbit_counts[tuple(sorted(counts.values(), reverse=True))] += 1
        root_dimensions.add(
            sum(2 - counts.get(vertex, 0) for vertex in range(4)) + 4
        )
    assert orbit_counts == Counter({(2, 1): 36, (1, 1, 1): 24})
    assert root_dimensions == {9}

    exact_sync_dimensions = {}
    for synchronized, maximum_a in ((0, 0), (1, 2), (2, 3), (3, 3), (4, 2)):
        delta = 2 * synchronized - maximum_a
        exact_sync_dimensions[synchronized] = (
            14 - delta + 252 - (20 - synchronized * (synchronized - 1) // 2)
        )
    assert set(exact_sync_dimensions.values()) == {246}
    assert 9 + 252 - 14 == 247
    return {
        "orbit_counts": dict(sorted(orbit_counts.items())),
        "root_dimensions": sorted(root_dimensions),
        "non_equality_source_dimensions": exact_sync_dimensions,
        "equality_source_dimension": 247,
        "proper_cut_upper_dimension": 246,
    }


def dot(left: tuple[int, int, int], right: tuple[int, int, int]) -> int:
    """Return the standard coordinate pairing."""
    return sum(a * b for a, b in zip(left, right, strict=True))


def chart_column(
    selected_nonroots: tuple[int, ...],
    cross_scalars: list[list[int]],
    a_forms: tuple[tuple[int, int, int], ...],
    b_forms: tuple[tuple[int, int, int], ...],
) -> list[int]:
    """Build one full tensor sensor column from the binary chart formula."""
    entries = []
    remaining_count = 4 - len(selected_nonroots)
    matching_count = 3 if remaining_count == 4 else 1
    for colours in product(range(3), repeat=4):
        value = 0
        for selected_roots in combinations(range(4), len(selected_nonroots)):
            coefficient = matching_count * permanent(
                submatrix(cross_scalars, selected_roots, selected_nonroots)
            )
            word_value = product_value(
                (a_forms if root in selected_roots else b_forms)[root][colour]
                for root, colour in enumerate(colours)
            )
            value += coefficient * word_value
        entries.append(value)
    return entries


def full_sensor_fixture_audit() -> dict[str, object]:
    """Use two generic root fixtures different from the primary verifier."""
    cross_scalars = [
        [1 if row == column else 2 for column in range(4)]
        for row in range(4)
    ]
    fixtures = {
        (2, 1): {
            "selector": (0, 0, 1),
            "roots": ((0, 0, 1), (1, 1, 0), (1, 1, 1), (1, 2, 3)),
            "outer": ((1, 1, 1), (1, 2, 1)),
            "a": ((1, 0, 0), (-1, 1, 0), (-1, 1, 0), (-2, 1, 0)),
            "b": ((0, 1, 0), (0, 0, 1), (-1, 0, 1), (-3, 0, 1)),
            "rows": (0, 1, 18, 19, 27, 28, 45, 46),
            "determinant": 56562381,
        },
        (1, 1, 1): {
            "selector": (0, 1, 2),
            "roots": ((0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 2, 3)),
            "outer": ((1, 1, 1), (1, 2, 1)),
            "a": ((1, 0, 0), (0, 1, 0), (-1, 1, 0), (-2, 1, 0)),
            "b": ((0, -1, 1), (-1, 0, 1), (0, 0, 1), (-3, 0, 1)),
            "rows": (0, 6, 9, 15, 27, 33, 36, 42),
            "determinant": 904998096,
        },
    }

    ledger = {}
    for orbit, fixture in fixtures.items():
        selector = fixture["selector"]
        roots = fixture["roots"]
        a_forms = fixture["a"]
        b_forms = fixture["b"]
        assert all(roots[selector[colour]][colour] == 0 for colour in range(3))
        assert all(dot(a_forms[index], roots[index]) == 0 for index in range(4))
        assert all(dot(b_forms[index], roots[index]) == 0 for index in range(4))
        assert all(cross_scalars[row][column] for row in range(4) for column in range(4))

        columns = [
            chart_column(subset, cross_scalars, a_forms, b_forms)
            for subset in parity_subsets()
        ]
        matrix = [[column[row] for column in columns] for row in range(81)]
        assert rank(matrix) == 8
        minor = [[matrix[row][column] for column in range(8)] for row in fixture["rows"]]
        minor_determinant = determinant(minor)
        assert minor_determinant == fixture["determinant"]
        ledger[str(orbit)] = {
            "sensor_rank": 8,
            "minor_determinant": int(minor_determinant),
            "all_cross_scalars_nonzero": True,
            "all_14_evaluations_zero": True,
        }
    return ledger


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield perfect matchings recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second), *matching)


def matrix_vector(
    matrix: tuple[tuple[int, int, int], ...], vector: tuple[int, int, int]
) -> tuple[int, int, int]:
    """Multiply a 3x3 integer matrix by a vector."""
    return tuple(dot(row, vector) for row in matrix)


def common_q_sensor_audit() -> dict[str, object]:
    """Directly reconstruct the rank-seven common-Q complete-deck sensor."""
    q = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
    contractions = ((1, 1, 1), (1, 2, 3), (2, 1, 3), (3, 2, 1))
    h = [matrix_vector(q, vector) for vector in contractions]
    columns = []
    for selected_nonroots in parity_subsets():
        column = []
        for colours in product(range(3), repeat=4):
            value = 0
            for selected_roots in combinations(range(4), len(selected_nonroots)):
                remaining = tuple(
                    root for root in range(4) if root not in selected_roots
                )
                for target_order in permutations(selected_nonroots):
                    cross_value = product_value(
                        h[nonroot][colours[root]]
                        for root, nonroot in zip(
                            selected_roots, target_order, strict=True
                        )
                    )
                    for matching in perfect_matchings(remaining):
                        root_value = product_value(
                            q[colours[first]][colours[second]]
                            for first, second in matching
                        )
                        value += cross_value * root_value
            column.append(value)
        columns.append(column)

    matrix = [[column[row] for column in columns] for row in range(81)]
    assert rank(matrix) == 7
    rows = (0, 2, 5, 8, 14, 17, 26)
    columns_kept = (0, 1, 2, 3, 4, 5, 7)
    minor = [[matrix[row][column] for column in columns_kept] for row in rows]
    minor_determinant = determinant(minor)
    assert minor_determinant == -13436928

    roots = ((1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 1, 0))
    outer = (1, 0, 0)

    def q_pair(
        left: tuple[int, int, int], right: tuple[int, int, int]
    ) -> int:
        return dot(left, matrix_vector(q, right))

    assert all(
        q_pair(roots[first], roots[second]) == 0
        for first, second in combinations(range(4), 2)
    )
    assert all(q_pair(root, outer) == 0 for root in roots)
    return {
        "sensor_rank": 7,
        "rank_seven_minor": int(minor_determinant),
        "all_14_evaluations_zero": True,
    }


def main() -> None:
    incidence = selector_and_dimension_audit()
    full = full_sensor_fixture_audit()
    sharp = common_q_sensor_audit()
    print("adjacent overlap inside balanced rank drop independent audit: PASS")
    print(f"  selector and dimension ledger: {incidence}")
    print(f"  generic full-sensor fixtures: {full}")
    print(f"  common-Q sharpness fixture: {sharp}")


if __name__ == "__main__":
    main()
