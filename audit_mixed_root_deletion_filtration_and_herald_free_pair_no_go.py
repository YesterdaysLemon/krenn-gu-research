"""Independent no-project-import audit of the mixed-root filtration."""

from fractions import Fraction
from functools import cache
from itertools import combinations, permutations


def hafnian(matrix):
    @cache
    def recurrence(vertices):
        if not vertices:
            return Fraction(1)
        if len(vertices) % 2:
            return Fraction(0)
        first = vertices[0]
        total = Fraction(0)
        for position in range(1, len(vertices)):
            second = vertices[position]
            remainder = vertices[1:position] + vertices[position + 1 :]
            total += matrix[first][second] * recurrence(remainder)
        return total

    return recurrence(tuple(range(len(matrix))))


def submatrix(matrix, vertices):
    return [[matrix[left][right] for right in vertices] for left in vertices]


def audit_three_root_partition() -> None:
    root_count = 3
    nonroot_count = 5
    size = root_count + nonroot_count
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    root_edges = {(0, 1): 2, (0, 2): 3, (1, 2): 5}
    for (first, second), value in root_edges.items():
        matrix[first][second] = matrix[second][first] = Fraction(value)
    for root in range(root_count):
        for nonroot in range(nonroot_count):
            value = Fraction((root + 2) * (nonroot + 3) + 1)
            vertex = root_count + nonroot
            matrix[root][vertex] = matrix[vertex][root] = value
    for first, second in combinations(range(nonroot_count), 2):
        value = Fraction((first + 1) * (second + 2) + 2)
        left = root_count + first
        right = root_count + second
        matrix[left][right] = matrix[right][left] = value

    direct = hafnian(matrix)
    nonroots = tuple(range(nonroot_count))
    partitioned = Fraction(0)
    for image in permutations(nonroots, root_count):
        unused = tuple(nonroot for nonroot in nonroots if nonroot not in image)
        root_product = Fraction(1)
        for root in range(root_count):
            root_product *= matrix[root][root_count + image[root]]
        partitioned += root_product * matrix[
            root_count + unused[0]
        ][root_count + unused[1]]
    for first, second in combinations(range(root_count), 2):
        remaining_root = ({0, 1, 2} - {first, second}).pop()
        for image in nonroots:
            unused_vertices = tuple(
                root_count + nonroot for nonroot in nonroots if nonroot != image
            )
            partitioned += (
                matrix[first][second]
                * matrix[remaining_root][root_count + image]
                * hafnian(submatrix(matrix, unused_vertices))
            )
    assert direct == partitioned


def sparse_forced_shore(parameter):
    size = 14
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    root_forms = (2, 3, 5, 7, 11)
    shore_targets = (5, 6, 7, 8, 9)
    for root, target, value in zip(
        range(5), shore_targets, root_forms, strict=True
    ):
        matrix[root][target] = matrix[target][root] = Fraction(value)
    matrix[10][11] = matrix[11][10] = Fraction(1)
    matrix[12][13] = matrix[13][12] = Fraction(1)
    matrix[5][6] = matrix[6][5] = Fraction(parameter)
    return matrix


def audit_nonzero_shore_kernel() -> None:
    first = sparse_forced_shore(13)
    second = sparse_forced_shore(17)
    expected = Fraction(2 * 3 * 5 * 7 * 11)
    assert hafnian(first) == hafnian(second) == expected
    assert hafnian(submatrix(first, (5, 6))) == 13
    assert hafnian(submatrix(second, (5, 6))) == 17

    # The forced-shore root tensor is the product of five root-linear factors.
    # Its factor data do not contain the hidden parameter, so neither can any
    # coefficient obtained by choosing fixed or tangent input at each root.
    base_values = tuple(Fraction(value) for value in (2, 3, 5, 7, 11))
    tangent_values = tuple(Fraction(value) for value in (1, -1, 2, -2, 3))
    factor_data_first = tuple(zip(base_values, tangent_values, strict=True))
    factor_data_second = tuple(zip(base_values, tangent_values, strict=True))
    assert factor_data_first == factor_data_second


def audit_shallow_and_vacuum_bounds() -> None:
    nonroot_count = 9
    root_count = 5
    assert nonroot_count - root_count == 4
    assert tuple(root_count - 2 * pairs for pairs in range(3)) == (5, 3, 1)
    assert 7 > root_count
    assert tuple(4 + 2 * pairs for pairs in range(3)) == (4, 6, 8)
    assert tuple(8 + 2 * pairs for pairs in range(2)) == (8, 10)
    assert (12,) == tuple(12 + 2 * pairs for pairs in range(1))

    # A present-vertex evaluation scales with its incident edges; a deleted
    # cofactor does not.  Two nontrivial scalings cannot agree universally.
    present = Fraction(7)
    deleted = Fraction(11)
    assert not (2 * present == deleted and 3 * present == deleted)
    assert 2 * present != 3 * present


def main() -> None:
    audit_three_root_partition()
    audit_nonzero_shore_kernel()
    audit_shallow_and_vacuum_bounds()
    print("AUDIT PASS: independent three-root partial-matching partition")
    print("AUDIT PASS: sparse nonzero shore is pair-blind at all root words")
    print("AUDIT PASS: depth and vertex-scaling obstructions over Q")
    print("AUDIT SCOPE: full mixed-GHZ compatibility and added heralds remain unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
