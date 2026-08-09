"""Independent stdlib audit of the P7 leaf apolar-Hilbert theorem.

The audit deliberately imports neither SymPy nor the primary verifier.  All
ranks are computed over Q with fractions, and generic adjointness is checked
by equality of edge labels rather than by evaluation.
"""

from fractions import Fraction
from itertools import combinations

N = 7
VERTICES = tuple(range(N))


def subsets(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(combinations(VERTICES, size))


def rational_rank(matrix: list[list[object]]) -> int:
    """Exact Gaussian rank over Q."""
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_entry
                for value, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def matrix_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    right_transpose = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in right_transpose]
        for row in left
    ]


def inclusion_matrix(source_size: int, target_size: int) -> list[list[int]]:
    source = subsets(source_size)
    return [
        [int(set(column) <= set(row)) for column in source]
        for row in subsets(target_size)
    ]


def k6_pair_sum_matrix() -> list[list[int]]:
    vertices = tuple(range(6))
    return [
        [int(vertex in edge) for vertex in vertices]
        for edge in combinations(vertices, 2)
    ]


def multiplication_matrix(
    degree: int, edge_weight: dict[tuple[int, int], int]
) -> list[list[int]]:
    domain = subsets(degree)
    rows: list[list[int]] = []
    for target in subsets(degree + 2):
        target_set = set(target)
        row: list[int] = []
        for source in domain:
            if set(source) <= target_set:
                missing = tuple(sorted(target_set - set(source)))
                row.append(edge_weight[missing])
            else:
                row.append(0)
        rows.append(row)
    return rows


def complement(subset: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(vertex for vertex in VERTICES if vertex not in subset)


def multiplication_label(
    source: tuple[int, ...], target: tuple[int, ...]
) -> tuple[int, int] | None:
    """Return the edge label of a nonzero generic multiplication entry."""
    if not set(source) <= set(target):
        return None
    missing = tuple(sorted(set(target) - set(source)))
    assert len(missing) == 2
    return missing


def audit_generic_adjointness() -> None:
    """Check complemented-transpose labels without a coefficient model."""
    for degree in range(6):
        for source in subsets(degree):
            for target in subsets(degree + 2):
                left = multiplication_label(source, target)
                right = multiplication_label(complement(target), complement(source))
                assert left == right


def hilbert_vector(edge_weight: dict[tuple[int, int], int]) -> tuple[int, ...]:
    return tuple(
        rational_rank(multiplication_matrix(degree, edge_weight))
        for degree in range(6)
    )


def main() -> None:
    pair_to_triple = inclusion_matrix(2, 3)
    pair_gram = matrix_product(transpose(pair_to_triple), pair_to_triple)
    edges = subsets(2)
    expected_pair_gram = [
        [
            5 if row == column else int(bool(set(row) & set(column)))
            for column in edges
        ]
        for row in edges
    ]
    assert pair_gram == expected_pair_gram
    assert rational_rank(pair_to_triple) == 21

    # The 1+6+14 Boolean decomposition gives Gram eigenvalues 15, 8, and 3.
    all_ones = [1] * 21
    assert [sum(row) for row in pair_gram] == [15 * value for value in all_ones]
    stars = [[int(vertex in edge) for edge in edges] for vertex in VERTICES]
    for vertex in range(6):
        difference = [a - b for a, b in zip(stars[vertex], stars[6], strict=True)]
        image = [sum(entry * value for entry, value in zip(row, difference, strict=True)) for row in pair_gram]
        assert image == [8 * value for value in difference]
    vertex_edge = transpose(stars)
    assert rational_rank(vertex_edge) == 7
    assert 21 - rational_rank(vertex_edge) == 14
    # On ker(vertex-edge transpose), H^T H=0 and Gram=3I; this identity audits
    # the eigenvalue without choosing or enumerating a kernel basis.
    vertex_edge_gram = matrix_product(vertex_edge, transpose(vertex_edge))
    assert all(
        pair_gram[row][column]
        == 3 * int(row == column) + vertex_edge_gram[row][column]
        for row in range(21)
        for column in range(21)
    )

    k6_incidence = k6_pair_sum_matrix()
    k6_gram = matrix_product(transpose(k6_incidence), k6_incidence)
    assert k6_gram == [
        [5 if row == column else 1 for column in range(6)]
        for row in range(6)
    ]
    assert rational_rank(k6_incidence) == 6
    audit_generic_adjointness()

    uniform = {edge: 1 for edge in edges}
    boundary_star = {edge: int(0 in edge) for edge in edges}
    assert hilbert_vector(uniform) == (1, 7, 21, 21, 7, 1)
    assert hilbert_vector(boundary_star) == (1, 6, 15, 15, 6, 1)

    assert rational_rank(multiplication_matrix(1, uniform)) == 7
    assert 15 - rational_rank(multiplication_matrix(1, uniform)) == 8

    table = []
    for rho in range(21):
        d2 = 21 - rho
        ann3 = 35 - rho
        lower_bound = max(0, ann3 - 7 * d2)
        assert lower_bound == max(0, 6 * rho - 112)
        table.append(lower_bound)
    assert table[20] == 8
    assert table[19] == 2
    assert table[:19] == [0] * 19

    print("PASS: independent Gram decompositions reproduce the 15,8,3 and 10,4 spectra.")
    print("PASS: generic multiplication labels reproduce every complementary adjoint.")
    print("PASS: independent Boolean ranks reproduce both Hilbert controls.")
    print("PASS: the rank-20/rank-19/rank<=18 essential-cubic split is exact.")
    print("SCOPE: stdlib-only audit; no import from the verifier or project code.")


if __name__ == "__main__":
    main()
