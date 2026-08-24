"""Independent no-import audit of the GLD69 common-incidence boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

PRIME = 5


def finite_rank(rows: tuple[tuple[int, ...], ...]) -> int:
    matrix = [[entry % PRIME for entry in row] for row in rows]
    pivot_row = 0
    for column in reversed(range(len(matrix[0]))):
        pivot = next(
            (
                row
                for row in reversed(range(pivot_row, len(matrix)))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], PRIME - 2, PRIME)
        matrix[pivot_row] = [entry * inverse % PRIME for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (entry - scale * pivot_entry) % PRIME
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
    return pivot_row


def finite_product(
    left: tuple[int, ...],
    matrix: tuple[tuple[int, ...], ...],
    right: tuple[int, ...],
) -> int:
    return (
        sum(
            left[row] * matrix[row][column] * right[column]
            for row in range(4)
            for column in range(4)
        )
        % PRIME
    )


def zero_diagonal_matrix(entries: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    matrix = [[0] * 4 for _ in range(4)]
    cursor = 0
    for left in range(4):
        for right in range(left + 1, 4):
            matrix[left][right] = matrix[right][left] = entries[cursor]
            cursor += 1
    return tuple(tuple(row) for row in matrix)


def audit_sparse_radicals() -> tuple[int, int, int]:
    sparse_vectors = tuple(
        vector
        for vector in product(range(PRIME), repeat=4)
        if any(vector) and sum(entry != 0 for entry in vector) <= 2
    )
    rank_counts = [0] * 5
    rank_two_with_sparse_radical = 0
    for entries in product(range(PRIME), repeat=6):
        matrix = zero_diagonal_matrix(entries)
        rank = finite_rank(matrix)
        rank_counts[rank] += 1
        assert rank != 1
        if rank != 2:
            continue
        sparse = next(
            (
                vector
                for vector in reversed(sparse_vectors)
                if all(
                    sum(matrix[row][column] * vector[column] for column in range(4))
                    % PRIME
                    == 0
                    for row in range(4)
                )
            ),
            None,
        )
        assert sparse is not None
        assert finite_product(sparse, matrix, sparse) == 0
        rank_two_with_sparse_radical += 1
    assert sum(rank_counts) == PRIME**6
    assert rank_two_with_sparse_radical == rank_counts[2]
    return rank_counts[0], rank_counts[2], rank_counts[4]


def audit_survivor_models() -> tuple[int, int, int, int]:
    vertices = frozenset("dcba")
    matchings = (
        (frozenset("ab"), frozenset("cd")),
        (frozenset("ac"), frozenset("bd")),
        (frozenset("ad"), frozenset("bc")),
    )
    families = []
    for choices in reversed(tuple(product((0, 1), repeat=3))):
        family = frozenset(
            matching[choice]
            for matching, choice in zip(reversed(matchings), choices, strict=True)
        )
        assert len(family) == 3
        assert all(vertices - edge not in family for edge in family)
        families.append(family)
    assert len(set(families)) == 8

    stars = 0
    triangles = 0
    quotient_checks = 0
    for family in families:
        star = any(all(vertex in edge for edge in family) for vertex in vertices)
        triangle = any(
            all(vertex not in edge for edge in family) for vertex in vertices
        )
        assert star != triangle
        stars += int(star)
        triangles += int(triangle)

        colours = dict(
            zip(sorted(family, key=sorted, reverse=True), range(3), strict=True)
        )
        aggregate: dict[tuple[int, int, int, int], Fraction] = {}
        ordered_vertices = tuple(sorted(vertices))
        for word in product(range(3), repeat=4):
            value = Fraction(0)
            for edge, colour in colours.items():
                label_value = all(
                    word[ordered_vertices.index(vertex)] == colour for vertex in edge
                )
                companion_value = all(
                    word[ordered_vertices.index(vertex)] == colour
                    for vertex in vertices - edge
                )
                value += int(label_value and companion_value)
            aggregate[word] = value
            assert value == int(len(set(word)) == 1)
        assert sum(aggregate.values()) == 3
        for target_edge in family:
            receiver = tuple(sorted(vertices - target_edge))
            desired_colour = colours[target_edge]
            nuisance_receiver_words: set[tuple[int, int]] = set()
            for label in family - {target_edge}:
                label_colour = colours[label]
                for label_word in product(reversed(range(3)), repeat=2):
                    full_word = {vertex: label_colour for vertex in vertices}
                    for vertex, colour in zip(
                        sorted(label, reverse=True), label_word, strict=True
                    ):
                        full_word[vertex] = colour
                    nuisance_receiver_words.add(
                        (full_word[receiver[0]], full_word[receiver[1]])
                    )
            assert (desired_colour, desired_colour) not in nuisance_receiver_words
            quotient_checks += 1
    assert stars == triangles == 4
    assert quotient_checks == 24
    return len(families), stars, triangles, quotient_checks


def tensor_column(factors: tuple[tuple[int, ...], ...]) -> list[int]:
    return [
        factors[0][indices[0]]
        * factors[1][indices[1]]
        * factors[2][indices[2]]
        * factors[3][indices[3]]
        % PRIME
        for indices in product(range(3), repeat=4)
    ]


def finite_column_rank(columns: list[list[int]]) -> int:
    return finite_rank(
        tuple(tuple(column[row] for column in columns) for row in range(81))
    )


def audit_pair_layer_formulas() -> tuple[tuple[int, int], tuple[int, int]]:
    basis = tuple(
        tuple(int(index == coordinate) for index in range(3)) for coordinate in range(3)
    )
    c0 = (1, 1, 2)
    c1 = (1, 2, 3)
    c2 = (2, 1, 4)
    c3 = (3, 4, 1)

    star_columns = []
    for centre in reversed(basis):
        for varying in reversed(basis):
            star_columns.append(tensor_column((centre, varying, c2, c3)))
            star_columns.append(tensor_column((centre, c1, varying, c3)))
            star_columns.append(tensor_column((centre, c1, c2, varying)))

    triangle_columns = []
    for first in reversed(basis):
        for second in reversed(basis):
            triangle_columns.append(tensor_column((first, second, c2, c3)))
            triangle_columns.append(tensor_column((first, c1, second, c3)))
            triangle_columns.append(tensor_column((c0, first, second, c3)))

    target = [
        (indices[0] + 1) % PRIME
        if indices[0] == indices[1] == indices[2] == indices[3]
        else 0
        for indices in product(range(3), repeat=4)
    ]
    star = (
        finite_column_rank(star_columns),
        finite_column_rank(star_columns + [target]),
    )
    triangle = (
        finite_column_rank(triangle_columns),
        finite_column_rank(triangle_columns + [target]),
    )
    assert star == (21, 22)
    assert triangle == (19, 20)
    return star, triangle


def permanent_by_deletion(columns: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    if len(columns) == 1:
        return columns[0][0]
    total = Fraction(0)
    first = columns[0]
    for row in reversed(range(len(columns))):
        reduced = tuple(
            tuple(entry for index, entry in enumerate(column) if index != row)
            for column in columns[1:]
        )
        total += first[row] * permanent_by_deletion(reduced)
    return total


def audit_fifteen_label_detector() -> tuple[int, Fraction]:
    xi = (Fraction(0), Fraction(0), Fraction(0), Fraction(2))
    eta = (Fraction(0), Fraction(0), Fraction(3), Fraction(0))
    sparse = (Fraction(0), Fraction(0), Fraction(7), Fraction(0))
    assert sum(entry != 0 for entry in sparse) == 1

    labels = 0
    for _pair in reversed(tuple(combinations(range(4), 2))):
        assert permanent_by_deletion((xi, eta, sparse, sparse)) == 0
        labels += 1
    for _port in reversed(range(4)):
        assert permanent_by_deletion((eta, sparse, sparse, sparse)) == 0
        assert permanent_by_deletion((xi, sparse, sparse, sparse)) == 0
        labels += 2
    assert permanent_by_deletion((sparse, sparse, sparse, sparse)) == 0
    labels += 1
    assert labels == 15

    inverse_images = (
        (Fraction(2), Fraction(0), Fraction(0)),
        (Fraction(3), Fraction(0), Fraction(0)),
        (Fraction(5), Fraction(0), Fraction(0)),
        (Fraction(7), Fraction(0), Fraction(0)),
    )
    weights = (Fraction(11), Fraction(13), Fraction(17))
    detector = sum(
        weights[colour]
        * inverse_images[0][colour]
        * inverse_images[1][colour]
        * inverse_images[2][colour]
        * inverse_images[3][colour]
        for colour in reversed(range(3))
    )
    assert detector == 11 * 2 * 3 * 5 * 7
    return labels, detector


def audit_sharp_boundaries() -> tuple[int, int]:
    scalar_zero_checks = 0
    for first, second in reversed(tuple(product(range(-5, 6), repeat=2))):
        local_vectors = (
            (first, second, 0),
            (first, second, 0),
            (0, first, second),
            (first, 0, second),
        )
        detector = sum(
            local_vectors[0][colour]
            * local_vectors[1][colour]
            * local_vectors[2][colour]
            * local_vectors[3][colour]
            for colour in reversed(range(3))
        )
        assert detector == 0
        scalar_zero_checks += 1

    nonsparse_checks = 0
    for first, second in reversed(tuple(product(range(-5, 6), repeat=2))):
        radical = (first, -first, second, -second)
        lies_in_centre = radical[0] - radical[2] == 0
        assert lies_in_centre == (first == second)
        if lies_in_centre and first:
            assert sum(entry != 0 for entry in radical) == 4
        nonsparse_checks += 1
    return scalar_zero_checks, nonsparse_checks


def main() -> None:
    finite_census = audit_sparse_radicals()
    survivor_models = audit_survivor_models()
    pair_layers = audit_pair_layer_formulas()
    detector = audit_fifteen_label_detector()
    boundaries = audit_sharp_boundaries()
    print("independent GLD69 common-incidence boundary audit: PASS")
    print("  F5 zero / rank-two / rank-four forms:", finite_census)
    print("  formal maximal / star / triangle models:", survivor_models)
    print("  star / triangle pair-layer augmented ranks:", pair_layers)
    print("  annihilated labels / nonzero target value:", detector)
    print("  scalar-zero / nonsparse-centre checks:", boundaries)
    print("  scope: finite-field formula audit; characteristic-zero proof is analytic")


if __name__ == "__main__":
    main()
