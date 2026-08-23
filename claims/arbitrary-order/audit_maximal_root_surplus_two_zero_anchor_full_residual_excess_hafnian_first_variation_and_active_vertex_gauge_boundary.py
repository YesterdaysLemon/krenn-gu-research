"""Independent no-import audit for GLS42.

This script uses only the Python standard library.  It does not import the
primary verifier or any repository module.  Its derivation uses explicit
perfect-matching lists, coefficient arrays, fractional row reduction, and
sparse labelled-coordinate tensors.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


def matchings(vertices: tuple[str, ...]) -> list[tuple[tuple[str, str], ...]]:
    if not vertices:
        return [()]
    first = vertices[0]
    result: list[tuple[tuple[str, str], ...]] = []
    for index, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(remainder):
            result.append((((first, partner)), *tail))
    return result


def key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def scalar_hafnian(
    vertices: tuple[str, ...], weights: dict[tuple[str, str], Fraction]
) -> Fraction:
    return sum(
        (
            product_value(
                weights.get(key(left, right), Fraction(0))
                for left, right in matching
            )
            for matching in matchings(vertices)
        ),
        Fraction(0),
    )


def product_value(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def multiply_polynomials(
    left: list[Fraction], right: list[Fraction]
) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def coefficient_one_hafnian(
    vertices: tuple[str, ...],
    weights: dict[tuple[str, str], Fraction],
    theta: dict[tuple[str, str], Fraction],
) -> Fraction:
    total = Fraction(0)
    for matching in matchings(vertices):
        polynomial = [Fraction(1)]
        for left, right in matching:
            edge = key(left, right)
            polynomial = multiply_polynomials(
                polynomial,
                [weights.get(edge, Fraction(0)), theta.get(edge, Fraction(0))],
            )
        if len(polynomial) > 1:
            total += polynomial[1]
    return total


def pointed_sum(
    vertices: tuple[str, ...],
    weights: dict[tuple[str, str], Fraction],
    theta: dict[tuple[str, str], Fraction],
) -> Fraction:
    total = Fraction(0)
    for matching in matchings(vertices):
        for pointed in range(len(matching)):
            term = Fraction(1)
            for index, (left, right) in enumerate(matching):
                edge = key(left, right)
                term *= (
                    theta.get(edge, Fraction(0))
                    if index == pointed
                    else weights.get(edge, Fraction(0))
                )
            total += term
    return total


def verify_independent_matching_identities() -> None:
    vertices = tuple(f"v{index}" for index in range(8))
    edges = list(combinations(vertices, 2))
    weights = {
        key(left, right): Fraction((index % 7) - 3, (index % 5) + 1)
        for index, (left, right) in enumerate(edges)
    }
    theta = {
        key(left, right): Fraction((2 * index % 9) - 4, (index % 4) + 1)
        for index, (left, right) in enumerate(edges)
    }
    coefficient = coefficient_one_hafnian(vertices, weights, theta)
    direct = pointed_sum(vertices, weights, theta)
    assert coefficient == direct

    pivot = vertices[0]
    recurrence = Fraction(0)
    for partner in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (pivot, partner)
        )
        edge = key(pivot, partner)
        recurrence += theta[edge] * scalar_hafnian(remainder, weights)
        recurrence += weights[edge] * pointed_sum(remainder, weights, theta)
    assert recurrence == direct

    gauges = dict(
        zip(vertices, (2, -1, 3, -4, 5, -2, 1, -4), strict=True)
    )
    gauge_theta = {
        key(left, right): Fraction(gauges[left] + gauges[right])
        * weights[key(left, right)]
        for left, right in edges
    }
    gauge_first = pointed_sum(vertices, weights, gauge_theta)
    assert gauge_first == sum(gauges.values()) * scalar_hafnian(vertices, weights)
    assert sum(gauges.values()) == 0
    assert gauge_first == 0


Matrix = tuple[tuple[Fraction, ...], ...]


def diagonal(first: int, second: int, third: int) -> Matrix:
    return (
        (Fraction(first), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(second), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(third)),
    )


def column(matrix: Matrix, index: int) -> tuple[Fraction, ...]:
    return tuple(matrix[row][index] for row in range(3))


def pair_matrix(
    left: Matrix, right: Matrix, left_index: int, right_index: int
) -> Matrix:
    left_vector = column(left, left_index)
    right_vector = column(right, right_index)
    return tuple(
        tuple(
            left_vector[row] * right_vector[col]
            + right_vector[row] * left_vector[col]
            for col in range(3)
        )
        for row in range(3)
    )


def flatten(matrix: Matrix) -> tuple[Fraction, ...]:
    return tuple(value for row in matrix for value in row)


def rank_columns(columns: list[tuple[Fraction, ...]]) -> int:
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for pivot_column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][pivot_column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][pivot_column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            multiplier = rows[row][pivot_column]
            if multiplier:
                rows[row] = [
                    value - multiplier * pivot_value
                    for value, pivot_value in zip(
                        rows[row], rows[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


Tensor = dict[tuple[int, ...], Fraction]
EdgeTensor = dict[tuple[int, int], Fraction]


def add_term(target: Tensor, word: tuple[int, ...], coefficient: Fraction) -> None:
    if coefficient:
        target[word] = target.get(word, Fraction(0)) + coefficient
        if target[word] == 0:
            del target[word]


def oriented_edge_tensor(
    left: str,
    right: str,
    label_index: dict[str, int],
    tensors: dict[tuple[str, str], EdgeTensor],
) -> EdgeTensor:
    edge = key(left, right)
    tensor = tensors.get(edge, {})
    if label_index[left] < label_index[right]:
        return tensor
    return {(right_coord, left_coord): value for (left_coord, right_coord), value in tensor.items()}


def tensor_hafnian(
    vertices: tuple[str, ...],
    label_index: dict[str, int],
    tensors: dict[tuple[str, str], EdgeTensor],
) -> Tensor:
    result: Tensor = {}
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    for matching in matchings(vertices):
        edge_options = [
            list(oriented_edge_tensor(left, right, label_index, tensors).items())
            for left, right in matching
        ]
        if any(not options for options in edge_options):
            continue
        for choices in product(*edge_options):
            word = [-1] * len(vertices)
            coefficient = Fraction(1)
            for ((left, right), ((left_coord, right_coord), value)) in zip(
                matching, choices, strict=True
            ):
                word[positions[left]] = left_coord
                word[positions[right]] = right_coord
                coefficient *= value
            add_term(result, tuple(word), coefficient)
    return result


def tensor_first_variation(
    vertices: tuple[str, ...],
    label_index: dict[str, int],
    weights: dict[tuple[str, str], EdgeTensor],
    theta: dict[tuple[str, str], EdgeTensor],
) -> Tensor:
    result: Tensor = {}
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    for left, right in combinations(vertices, 2):
        theta_terms = oriented_edge_tensor(left, right, label_index, theta)
        remainder = tuple(vertex for vertex in vertices if vertex not in (left, right))
        deck = tensor_hafnian(remainder, label_index, weights)
        for (left_coord, right_coord), theta_value in theta_terms.items():
            for deck_word, deck_value in deck.items():
                full_word = [-1] * len(vertices)
                full_word[positions[left]] = left_coord
                full_word[positions[right]] = right_coord
                for vertex, coordinate in zip(remainder, deck_word, strict=True):
                    full_word[positions[vertex]] = coordinate
                add_term(result, tuple(full_word), theta_value * deck_value)
    return result


def verify_independent_physical_control() -> None:
    labels = ("q0", "u0", "q1", "u1", "u2", "u3")
    label_index = {label: index for index, label in enumerate(labels)}
    p0 = diagonal(1, 0, 0)
    p1 = diagonal(0, 1, 0)
    p2 = diagonal(0, 0, 1)
    maps = {
        "q0": p0,
        "u0": diagonal(1, -1, 0),
        "q1": p1,
        "u1": p1,
        "u2": p2,
        "u3": p2,
    }

    incidence: list[tuple[Fraction, ...]] = []
    for left, right in combinations(labels, 2):
        if key(left, right) == key("q0", "q1"):
            continue
        for left_coordinate in range(3):
            for right_coordinate in range(3):
                incidence.append(
                    flatten(
                        pair_matrix(
                            maps[left], maps[right], left_coordinate, right_coordinate
                        )
                    )
                )
    assert rank_columns(incidence) == 6

    q_matrix: Matrix = (
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    source_columns = [flatten(p0), flatten(p1), flatten(p2), flatten(q_matrix)]
    assert rank_columns(source_columns) == 4
    assert rank_columns([*incidence, *source_columns]) == 6

    colours = {"q0": 0, "u0": 0, "q1": 1, "u1": 1, "u2": 2, "u3": 2}
    scalar_weights = {
        key("q0", "u2"): Fraction(1),
        key("q0", "u3"): Fraction(-1, 3),
        key("u0", "u2"): Fraction(1, 3),
        key("u0", "u3"): Fraction(-1),
        key("q1", "u1"): Fraction(1),
        key("u0", "u1"): Fraction(1),
        key("u2", "u3"): Fraction(1),
        key("q0", "q1"): Fraction(1),
    }
    weight_tensors: dict[tuple[str, str], EdgeTensor] = {}
    for left, right in combinations(labels, 2):
        edge = key(left, right)
        if edge in scalar_weights:
            weight_tensors[edge] = {
                (colours[edge[0]], colours[edge[1]]): scalar_weights[edge]
            }
        else:
            weight_tensors[edge] = {}

    def theta_tensor(root_row: int, root_column: int) -> dict[tuple[str, str], EdgeTensor]:
        result: dict[tuple[str, str], EdgeTensor] = {}
        for left, right in combinations(labels, 2):
            edge = key(left, right)
            entries: EdgeTensor = {}
            for left_coordinate in range(3):
                for right_coordinate in range(3):
                    value = pair_matrix(
                        maps[left], maps[right], left_coordinate, right_coordinate
                    )[root_row][root_column]
                    if value:
                        if label_index[left] < label_index[right]:
                            entries[left_coordinate, right_coordinate] = value
                        else:
                            entries[right_coordinate, left_coordinate] = value
            result[edge] = entries
        return result

    theta_02 = theta_tensor(0, 2)
    theta_01 = theta_tensor(0, 1)
    gauges = dict(zip(labels, (-1, 1, 1, -1, 2, -2), strict=True))
    for left, right in combinations(labels, 2):
        edge = key(left, right)
        expected = {
            coordinates: Fraction(gauges[left] + gauges[right]) * value
            for coordinates, value in weight_tensors[edge].items()
            if (gauges[left] + gauges[right]) * value
        }
        assert theta_02[edge] == expected
    assert sum(gauges.values()) == 0

    common_word = (0, 0, 1, 1, 2, 2)
    assert tensor_hafnian(labels, label_index, weight_tensors) == {
        common_word: Fraction(-1, 9)
    }
    assert tensor_first_variation(labels, label_index, weight_tensors, theta_02) == {}
    assert tensor_first_variation(labels, label_index, weight_tensors, theta_01) == {
        common_word: Fraction(2),
        (0, 1, 1, 1, 2, 2): Fraction(-1),
    }

    expected_deletions = {
        key("u0", "u3"): Fraction(1),
        key("u0", "u2"): Fraction(-1, 3),
        key("q0", "u3"): Fraction(1, 3),
        key("q0", "u2"): Fraction(-1),
    }
    for deleted, expected in expected_deletions.items():
        remainder = tuple(vertex for vertex in labels if vertex not in deleted)
        deck = tensor_hafnian(remainder, label_index, weight_tensors)
        assert len(deck) == 1
        assert next(iter(deck.values())) == expected
        assert expected != 0

    assert scalar_hafnian(("q0", "q1"), scalar_weights) == 1
    assert scalar_hafnian(("u0", "u1", "u2", "u3"), scalar_weights) == 1
    assert sum(flatten(q_matrix)) == 2
    assert sum(flatten(maps["u0"])) == 0
    pi_q = Fraction(2) * (
        scalar_weights[key("u0", "u3")]
        + scalar_weights[key("u0", "u2")]
        + scalar_weights[key("u0", "u1")]
    )
    assert pi_q == Fraction(2, 3)


def main() -> None:
    verify_independent_matching_identities()
    verify_independent_physical_control()
    print("GLS42 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
