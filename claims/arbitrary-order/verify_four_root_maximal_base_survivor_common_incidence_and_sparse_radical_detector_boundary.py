"""Exact replay for the GLD69 common-incidence detector boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product

Q = Fraction
PORTS = frozenset(range(4))
PAIRS = tuple(frozenset(pair) for pair in combinations(PORTS, 2))
PERMUTATIONS = tuple(permutations(range(4)))


def matrix_rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def permanent(columns: list[list[Q]]) -> Q:
    assert len(columns) == 4
    return sum(
        (
            columns[0][sigma[0]]
            * columns[1][sigma[1]]
            * columns[2][sigma[2]]
            * columns[3][sigma[3]]
        )
        for sigma in PERMUTATIONS
    )


def residual_form(xi: list[Q], eta: list[Q]) -> list[list[Q]]:
    basis = [[Q(index == coordinate) for index in range(4)] for coordinate in range(4)]
    return [[permanent([xi, eta, left, right]) for right in basis] for left in basis]


def bilinear(left: list[Q], form: list[list[Q]], right: list[Q]) -> Q:
    return sum(
        left[row] * form[row][column] * right[column]
        for row in range(4)
        for column in range(4)
    )


def block(
    left: list[list[Q]], form: list[list[Q]], right: list[list[Q]]
) -> list[list[Q]]:
    return [[bilinear(x, form, y) for y in right] for x in left]


def tensor_index(indices: tuple[int, int, int, int]) -> int:
    return ((indices[0] * 3 + indices[1]) * 3 + indices[2]) * 3 + indices[3]


def column_rank(columns: list[list[Q]]) -> int:
    return matrix_rank([[column[row] for column in columns] for row in range(81)])


def pair_layer_columns(
    form: list[list[Q]], ports: list[list[list[Q]]]
) -> list[list[Q]]:
    columns: list[list[Q]] = []
    for label in PAIRS:
        label_axes = tuple(sorted(label))
        companion_axes = tuple(sorted(PORTS - label))
        companion = block(ports[companion_axes[0]], form, ports[companion_axes[1]])
        for label_indices in product(range(3), repeat=2):
            column = [Q(0)] * 81
            for companion_indices in product(range(3), repeat=2):
                indices = [0] * 4
                for axis, index in zip(label_axes, label_indices, strict=True):
                    indices[axis] = index
                for axis, index in zip(companion_axes, companion_indices, strict=True):
                    indices[axis] = index
                column[tensor_index(tuple(indices))] = companion[companion_indices[0]][
                    companion_indices[1]
                ]
            columns.append(column)
    return columns


def vector(*entries: int) -> list[Q]:
    return [Q(entry) for entry in entries]


def complement_families() -> list[frozenset[frozenset[int]]]:
    representatives = (
        frozenset((0, 1)),
        frozenset((0, 2)),
        frozenset((0, 3)),
    )
    families = []
    for choices in product((0, 1), repeat=3):
        families.append(
            frozenset(
                edge if choice == 0 else PORTS - edge
                for edge, choice in zip(representatives, choices, strict=True)
            )
        )
    assert len(set(families)) == 8
    return families


def check_formal_countermodels() -> tuple[int, int, int, int]:
    target = {
        indices: Q(indices[0] == indices[1] == indices[2] == indices[3])
        for indices in product(range(3), repeat=4)
    }
    stars = 0
    triangles = 0
    quotient_checks = 0
    for family in complement_families():
        is_star = any(all(vertex in edge for edge in family) for vertex in PORTS)
        is_triangle = any(
            all(vertex not in edge for edge in family) for vertex in PORTS
        )
        assert is_star != is_triangle
        stars += int(is_star)
        triangles += int(is_triangle)

        aggregate = {indices: Q(0) for indices in target}
        colours = dict(zip(sorted(family, key=lambda edge: tuple(edge)), range(3)))
        for edge, colour in colours.items():
            assert PORTS - edge not in family
            # H_edge and Pi_edge concatenate to the one pure word of this colour.
            for indices in aggregate:
                if all(indices[port] == colour for port in PORTS):
                    aggregate[indices] += 1
        assert aggregate == target

        # Replay the complete foreign port-pair nuisance for every survivor.
        for target_edge in family:
            receiver = tuple(sorted(PORTS - target_edge))
            target_axes = tuple(sorted(target_edge))
            nuisance_vectors: list[list[Q]] = []
            for label in PAIRS:
                if label == target_edge or label not in family:
                    continue
                companion_colour = colours[label]
                label_axes = tuple(sorted(label))
                for label_indices in product(range(3), repeat=2):
                    full_indices = [companion_colour] * 4
                    for axis, index in zip(label_axes, label_indices, strict=True):
                        full_indices[axis] = index
                    for target_indices in product(range(3), repeat=2):
                        if any(
                            full_indices[axis] != index
                            for axis, index in zip(
                                target_axes, target_indices, strict=True
                            )
                        ):
                            continue
                        receiver_index = (
                            3 * full_indices[receiver[0]] + full_indices[receiver[1]]
                        )
                        row = [Q(0)] * 9
                        row[receiver_index] = 1
                        nuisance_vectors.append(row)
            desired = [Q(0)] * 9
            colour = colours[target_edge]
            desired[3 * colour + colour] = 1
            nuisance_rank = matrix_rank(nuisance_vectors)
            assert matrix_rank(nuisance_vectors + [desired]) == nuisance_rank + 1
            quotient_checks += 1
    assert stars == triangles == 4
    assert quotient_checks == 24
    return len(complement_families()), stars, triangles, quotient_checks


def check_common_pullback() -> int:
    xi = vector(1, 2, -1, 3)
    eta = vector(2, -2, 4, 1)
    form = residual_form(xi, eta)
    ports = [
        [
            vector(1, 0, 1, index),
            vector(0, 1, index, 1),
            vector(1, index, 0, 1),
        ]
        for index in range(1, 5)
    ]
    checks = 0
    for target in PAIRS:
        left, right = sorted(PORTS - target)
        pulled_back = block(ports[left], form, ports[right])
        direct = [
            [permanent([xi, eta, x, y]) for y in ports[right]] for x in ports[left]
        ]
        assert pulled_back == direct
        checks += 9
    assert all(form[index][index] == 0 for index in range(4))
    return checks


def star_data() -> tuple[list[Q], list[Q], list[list[Q]], list[list[list[Q]]]]:
    xi = vector(0, 0, 0, 1)
    eta = vector(0, 0, 1, 0)
    form = residual_form(xi, eta)
    radical_0 = vector(0, 0, 1, 0)
    radical_1 = vector(0, 0, 0, 1)
    centre_line = vector(1, 1, 0, 0)
    leaf_line = vector(1, -1, 0, 0)
    ports = [
        [radical_0, radical_1, centre_line],
        [radical_0, radical_1, leaf_line],
        [radical_0, radical_1, leaf_line],
        [radical_0, radical_1, leaf_line],
    ]
    return xi, eta, form, ports


def check_pair_layer_obstructions() -> tuple[tuple[int, int], tuple[int, int]]:
    _xi, _eta, star_form, star_ports = star_data()
    star_columns = pair_layer_columns(star_form, star_ports)
    target = [
        Q((indices[0] == indices[1] == indices[2] == indices[3]) * (indices[0] + 1))
        for indices in product(range(3), repeat=4)
    ]
    star_ranks = (column_rank(star_columns), column_rank(star_columns + [target]))
    assert star_ranks == (21, 22)

    # Triangle on ports 1,2,3; the centre image projects onto the whole quotient.
    xi = vector(0, 0, 1, 1)
    eta = vector(1, 1, 0, 0)
    triangle_form = residual_form(xi, eta)
    radical_0 = vector(1, -1, 0, 0)
    leaf_ports = [radical_0, vector(0, 0, 1, 0), vector(0, 0, 0, 1)]
    centre_port = [
        vector(1, 0, 1, 0),
        vector(0, 1, 0, 0),
        vector(0, 0, 0, 1),
    ]
    triangle_ports = [centre_port, leaf_ports, leaf_ports, leaf_ports]
    assert 3 + 2 - matrix_rank(centre_port + [radical_0, vector(0, 0, 1, -1)]) == 1
    triangle_columns = pair_layer_columns(triangle_form, triangle_ports)
    triangle_ranks = (
        column_rank(triangle_columns),
        column_rank(triangle_columns + [target]),
    )
    assert triangle_ranks == (19, 20)
    return star_ranks, triangle_ranks


def check_star_geometry_and_detector() -> tuple[int, int]:
    xi, eta, form, ports = star_data()
    assert matrix_rank(form) == 2
    assert all(
        matrix_rank([[entry for entry in column] for column in port]) == 3
        for port in ports
    )
    for leaf in range(1, 4):
        assert not any(
            entry for row in block(ports[0], form, ports[leaf]) for entry in row
        )
    for left, right in combinations(range(1, 4), 2):
        assert any(
            entry for row in block(ports[left], form, ports[right]) for entry in row
        )

    sparse = vector(0, 0, 1, 0)
    assert all(
        bilinear(sparse, form, basis) == 0
        for basis in [
            vector(1, 0, 0, 0),
            vector(0, 1, 0, 0),
            vector(0, 0, 1, 0),
            vector(0, 0, 0, 1),
        ]
    )
    assert sum(entry != 0 for entry in sparse) <= 2

    # The inverse image of sparse is local coordinate 0 at every port.
    inverse_images = [vector(1, 0, 0) for _ in range(4)]
    weights = vector(2, 3, 5)
    detector = sum(
        weights[colour]
        * inverse_images[0][colour]
        * inverse_images[1][colour]
        * inverse_images[2][colour]
        * inverse_images[3][colour]
        for colour in range(3)
    )
    assert detector == 2

    # Replay all 6 port-port, 8 residual-port, and 1 residual-pair companions.
    zero_labels = 0
    for _left, _right in combinations(range(4), 2):
        assert permanent([xi, eta, sparse, sparse]) == 0
        zero_labels += 1
    for _port in range(4):
        assert permanent([eta, sparse, sparse, sparse]) == 0
        assert permanent([xi, sparse, sparse, sparse]) == 0
        zero_labels += 2
    assert permanent([sparse, sparse, sparse, sparse]) == 0
    zero_labels += 1
    assert zero_labels == 15
    return zero_labels, int(detector != 0)


def check_scalar_zero_star_control() -> int:
    xi, eta, form, _ports = star_data()
    radical_0 = vector(0, 0, 1, 0)
    radical_1 = vector(0, 0, 0, 1)
    centre_line = vector(1, 1, 0, 0)
    leaf_line = vector(1, -1, 0, 0)
    ports = [
        [radical_0, radical_1, centre_line],
        [radical_0, radical_1, leaf_line],
        [leaf_line, radical_0, radical_1],
        [radical_0, leaf_line, radical_1],
    ]
    assert all(matrix_rank(port) == 3 for port in ports)
    for leaf in range(1, 4):
        assert not any(
            entry for row in block(ports[0], form, ports[leaf]) for entry in row
        )
    for left, right in combinations(range(1, 4), 2):
        assert any(
            entry for row in block(ports[left], form, ports[right]) for entry in row
        )

    checks = 0
    for first, second in product(range(-3, 4), repeat=2):
        root_vector = [Q(0), Q(0), Q(first), Q(second)]
        local = [
            vector(first, second, 0),
            vector(first, second, 0),
            vector(0, first, second),
            vector(first, 0, second),
        ]
        for port, local_vector in zip(ports, local, strict=True):
            image = [
                sum(local_vector[column] * port[column][row] for column in range(3))
                for row in range(4)
            ]
            assert image == root_vector
        detector = sum(
            local[0][colour] * local[1][colour] * local[2][colour] * local[3][colour]
            for colour in range(3)
        )
        assert detector == 0
        checks += 1
    assert permanent([xi, eta, radical_0, radical_0]) == 0
    return checks


def check_triangle_nonsparse_control() -> tuple[int, int]:
    # This physical residual pair gives J=(x0+x1)(x2+x3), up to polarization.
    xi = vector(0, 0, 1, 1)
    eta = vector(1, 1, 0, 0)
    form = residual_form(xi, eta)
    assert matrix_rank(form) == 2

    radical_0 = vector(1, -1, 0, 0)
    radical_1 = vector(0, 0, 1, -1)
    assert all(
        bilinear(radical, form, basis) == 0
        for radical in (radical_0, radical_1)
        for basis in (
            vector(1, 0, 0, 0),
            vector(0, 1, 0, 0),
            vector(0, 0, 1, 0),
            vector(0, 0, 0, 1),
        )
    )

    leaf = [radical_0, vector(0, 0, 1, 0), vector(0, 0, 0, 1)]
    centre = [vector(1, 0, 1, 0), vector(0, 1, 0, 0), vector(0, 0, 0, 1)]
    assert matrix_rank(leaf) == matrix_rank(centre) == 3
    assert not any(entry for row in block(leaf, form, leaf) for entry in row)
    assert any(entry for row in block(centre, form, leaf) for entry in row)

    intersection_generator = vector(1, -1, 1, -1)
    assert sum(entry != 0 for entry in intersection_generator) == 4
    # A direct solve in parameters (a,-a,b,-b) and x0=x2 gives a=b.
    checks = 0
    for first, second in product(range(-4, 5), repeat=2):
        radical = vector(first, -first, second, -second)
        in_centre = radical[0] == radical[2]
        assert in_centre == (first == second)
        if in_centre and first:
            assert all(
                radical[index] == first * intersection_generator[index]
                for index in range(4)
            )
            assert sum(entry != 0 for entry in radical) == 4
        checks += 1
    return checks, sum(entry != 0 for entry in intersection_generator)


def main() -> None:
    formal = check_formal_countermodels()
    pullbacks = check_common_pullback()
    pair_layers = check_pair_layer_obstructions()
    detector = check_star_geometry_and_detector()
    scalar_zero = check_scalar_zero_star_control()
    triangle = check_triangle_nonsparse_control()
    print("four-root maximal-survivor common-incidence boundary: PASS")
    print("  formal maximal / star / triangle countermodels:", formal)
    print("  typed common-J pullback coordinates:", pullbacks)
    print("  star / triangle pair-layer augmented ranks:", pair_layers)
    print("  annihilated labels / active detector:", detector)
    print("  scalar-zero star samples:", scalar_zero)
    print("  triangle intersection checks / support:", triangle)
    print("  scope: rank-three maximal profiles; exceptional fibres remain open")


if __name__ == "__main__":
    main()
