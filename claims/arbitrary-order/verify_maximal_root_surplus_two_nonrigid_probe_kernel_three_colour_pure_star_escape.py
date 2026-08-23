"""Focused exact checks for GLS56.

The written theorem carries the arbitrary-field and arbitrary-root proof.
This verifier replays the covector, matching, kernel-flag, companion,
GLD3-triangle, and sharp same-graph interfaces with exact rationals.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
from typing import Iterable

Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((x * y for x, y in zip(left, right, strict=True)), Fraction(0))


def is_zero(vector: Vector) -> bool:
    return all(value == 0 for value in vector)


def matrix_rank(rows: Iterable[Iterable[Fraction]]) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[rank], strict=True
                )
            ]
        rank += 1
    return rank


def outer(left: Vector, right: Vector) -> Vector:
    return tuple(x * y for x in left for y in right)


def add(left: Vector, right: Vector) -> Vector:
    return tuple(x + y for x, y in zip(left, right, strict=True))


def scale(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def coordinate_kernel_witness(row: Vector, colour: int) -> Vector | None:
    off_colours = [index for index in range(3) if index != colour]
    if row[colour] and all(row[index] == 0 for index in off_colours):
        return None
    witness = [Fraction(0), Fraction(0), Fraction(0)]
    witness[colour] = 1
    if is_zero(row):
        return tuple(witness)
    pivot = next(index for index in off_colours if row[index])
    witness[pivot] = -row[colour] / row[pivot]
    return tuple(witness)


def audit_coordinate_alternative() -> dict[str, int]:
    cases = 0
    kernel_witnesses = 0
    axis_rows = 0
    values = (Fraction(-1), Fraction(0), Fraction(1))
    for row in product(values, repeat=3):
        for colour in range(3):
            witness = coordinate_kernel_witness(row, colour)
            cases += 1
            if witness is None:
                axis_rows += 1
                assert row[colour]
                assert all(row[index] == 0 for index in range(3) if index != colour)
            else:
                kernel_witnesses += 1
                assert witness[colour] == 1
                assert dot(row, witness) == 0
    assert cases == 81
    return {
        "covector_colour_cases": cases,
        "kernel_witnesses": kernel_witnesses,
        "nonzero_coordinate_axes": axis_rows,
    }


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            result.append(((first, second),) + matching)
    return tuple(result)


def audit_matching_kill() -> dict[str, int]:
    companion_killed = 0
    deck_matchings = 0
    top_matchings = 0
    pair_cases = 0
    for root_order in range(3, 8):
        labels = tuple(range(2 * root_order))
        silent = 0
        for pair in combinations(labels, 2):
            pair_cases += 1
            if silent in pair:
                companion_killed += 1
                continue
            complement = tuple(label for label in labels if label not in pair)
            for matching in perfect_matchings(complement):
                assert any(silent in edge for edge in matching)
                deck_matchings += 1
        for matching in perfect_matchings(labels):
            assert any(silent in edge for edge in matching)
            top_matchings += 1
    return {
        "pair_cases": pair_cases,
        "companion_killed_pairs": companion_killed,
        "deck_matchings_through_silent_label": deck_matchings,
        "top_matchings_through_silent_label": top_matchings,
    }


def proportional_scale(source: Vector, target: Vector) -> Fraction | None:
    if is_zero(source):
        return None
    pivot = next(index for index, value in enumerate(source) if value)
    factor = target[pivot] / source[pivot]
    if all(target[index] == factor * source[index] for index in range(len(source))):
        return factor
    return None


def gamma(pair_s: tuple[Vector, Vector], pair_t: tuple[Vector, Vector]) -> Vector:
    x_s, y_s = pair_s
    x_t, y_t = pair_t
    return add(outer(x_s, y_t), outer(x_t, y_s))


def classified_gamma_zero(
    pair_s: tuple[Vector, Vector], pair_t: tuple[Vector, Vector]
) -> bool:
    x_s, y_s = pair_s
    x_t, y_t = pair_t
    pure_x = is_zero(y_s) and is_zero(y_t)
    pure_y = is_zero(x_s) and is_zero(x_t)
    if pure_x or pure_y:
        return True
    if any(is_zero(vector) for vector in (x_s, y_s, x_t, y_t)):
        return False
    factor = proportional_scale(x_s, x_t)
    return factor is not None and factor != 0 and y_t == scale(-factor, y_s)


def audit_pair_companion_trichotomy() -> dict[str, int]:
    values = (Fraction(-1), Fraction(0), Fraction(1))
    vectors = [tuple(vector) for vector in product(values, repeat=2)]
    visible_pairs = [
        (x_row, y_row)
        for x_row in vectors
        for y_row in vectors
        if not (is_zero(x_row) and is_zero(y_row))
    ]
    pair_cases = 0
    zero_cases = 0
    for pair_s in visible_pairs:
        for pair_t in visible_pairs:
            vanishes = is_zero(gamma(pair_s, pair_t))
            assert vanishes == classified_gamma_zero(pair_s, pair_t)
            pair_cases += 1
            zero_cases += int(vanishes)

    triple_cases = 0
    for indices in combinations(range(len(visible_pairs)), 3):
        triple = [visible_pairs[index] for index in indices]
        if all(is_zero(gamma(triple[i], triple[j])) for i, j in combinations(range(3), 2)):
            all_pure_x = all(is_zero(pair[1]) for pair in triple)
            all_pure_y = all(is_zero(pair[0]) for pair in triple)
            assert all_pure_x or all_pure_y
            triple_cases += 1

    return {
        "visible_row_pairs": len(visible_pairs),
        "ordered_pair_cases": pair_cases,
        "zero_companion_cases": zero_cases,
        "all-pair-zero_triples": triple_cases,
    }


def audit_homogeneous_identity() -> dict[str, int]:
    vectors = [
        (Fraction(1), Fraction(2)),
        (Fraction(-1), Fraction(1)),
        (Fraction(2), Fraction(-3)),
    ]
    scalar_rows = [
        (Fraction(1), Fraction(2), Fraction(-1), Fraction(3)),
        (Fraction(0), Fraction(1), Fraction(2), Fraction(-2)),
        (Fraction(3), Fraction(-1), Fraction(1), Fraction(1)),
    ]
    cases = 0
    assignments = [
        (vectors[0], vectors[1], vectors[1], vectors[2]),
        (vectors[2], vectors[0], vectors[1], vectors[0]),
        (vectors[1], vectors[2], vectors[0], vectors[1]),
    ]
    for x_s, y_s, x_t, y_t in assignments:
        for delta_s, eta_s, delta_t, eta_t in scalar_rows:
            d_s = add(scale(delta_s, x_s), scale(eta_s, y_s))
            d_t = add(scale(delta_t, x_t), scale(eta_t, y_t))
            g_st = add(outer(x_s, y_t), outer(y_s, x_t))
            a_st = add(outer(x_s, y_t), scale(-1, outer(y_s, x_t)))
            left = scale(
                2,
                add(
                    add(
                        outer(d_s, d_t),
                        scale(-delta_s * delta_t, outer(x_s, x_t)),
                    ),
                    scale(-eta_s * eta_t, outer(y_s, y_t)),
                ),
            )
            right = add(
                scale(delta_s * eta_t + eta_s * delta_t, g_st),
                scale(delta_s * eta_t - eta_s * delta_t, a_st),
            )
            assert left == right
            cases += 1
    return {"exact_vector_identities": cases}


def audit_exceptional_flag() -> dict[str, int]:
    checked = 0
    first_stage_failures = 0
    for x_value in range(-4, 5):
        for y_value in range(-4, 5):
            x = Fraction(x_value)
            y = Fraction(y_value)
            if x == 0 or y == 0 or x + y == 0:
                continue
            # K={(x,y,x+y)}.  The first e0-pure shore is (x-y)e0.
            first = (x - y, Fraction(0), Fraction(0))
            successor = (y, x - y, Fraction(0))
            colour_one = (Fraction(0), x, Fraction(0))
            colour_two = (Fraction(0), Fraction(0), y)
            assert colour_one[1] and colour_two[2]
            if first[0]:
                assert first[1:] == (0, 0)
            else:
                first_stage_failures += 1
                assert x == y
                assert successor[0] != 0 and successor[1] == 0
            checked += 1
    assert first_stage_failures > 0
    return {
        "torus_parameter_points": checked,
        "exceptional_divisor_points": first_stage_failures,
        "rank_one_kernel_flag_length": 2,
    }


def audit_gld3_triangle() -> dict[str, int]:
    values = (Fraction(-2), Fraction(-1), Fraction(1), Fraction(2))
    cases = 0
    for lambdas in product(values, repeat=3):
        equations: list[list[Fraction]] = []
        for left, right in combinations(range(3), 2):
            for row in range(3):
                for column in range(3):
                    if row == column:
                        continue
                    equation = [Fraction(0)] * 9
                    if row == left:
                        equation[3 * right + column] += lambdas[left]
                    if column == right:
                        equation[3 * left + row] += lambdas[right]
                    if any(equation):
                        equations.append(equation)
        assert matrix_rank(equations) == 9
        cases += 1

    port_matchings = perfect_matchings((0, 1, 2, 3))
    assert all(any(left < 3 and right < 3 for left, right in matching) for matching in port_matchings)
    return {
        "nonzero_star_scalar_cases": cases,
        "triangle_linear_rank": 9,
        "four_port_matchings": len(port_matchings),
    }


def zero_matrix() -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(3)) for _ in range(3))


def matrix_unit(row: int, column: int, value: int = 1) -> Matrix:
    return tuple(
        tuple(
            Fraction(value if (left, right) == (row, column) else 0)
            for right in range(3)
        )
        for left in range(3)
    )


class ExactGraph:
    def __init__(self, vertices: tuple[str, ...]) -> None:
        self.vertices = vertices
        self.order = {vertex: index for index, vertex in enumerate(vertices)}
        self.edges: dict[tuple[str, str], Matrix] = {}

    def set_edge(self, left: str, right: str, matrix: Matrix) -> None:
        assert left != right
        if self.order[left] < self.order[right]:
            self.edges[(left, right)] = matrix
        else:
            self.edges[(right, left)] = tuple(zip(*matrix, strict=True))

    def matrix(self, left: str, right: str) -> Matrix:
        if self.order[left] < self.order[right]:
            return self.edges.get((left, right), zero_matrix())
        stored = self.edges.get((right, left), zero_matrix())
        return tuple(zip(*stored, strict=True))

    def coefficient(self, colours: dict[str, int], subset: tuple[str, ...] | None = None) -> Fraction:
        active = self.vertices if subset is None else subset
        total = Fraction(0)
        for matching in perfect_matchings(tuple(self.order[vertex] for vertex in active)):
            term = Fraction(1)
            for left_index, right_index in matching:
                left = self.vertices[left_index]
                right = self.vertices[right_index]
                term *= self.matrix(left, right)[colours[left]][colours[right]]
            total += term
        return total


def build_source_adjacent_control() -> ExactGraph:
    vertices = ("a0", "a1", "q0", "q1", "n", "t0", "t1", "t2")
    graph = ExactGraph(vertices)
    graph.set_edge("a0", "q0", matrix_unit(0, 0))
    graph.set_edge("a1", "q1", matrix_unit(0, 0))
    graph.set_edge("a0", "t0", matrix_unit(0, 0))
    graph.set_edge("a1", "t1", matrix_unit(0, 0))
    graph.set_edge("a0", "t2", matrix_unit(0, 0))
    graph.set_edge("q0", "q1", matrix_unit(0, 0))
    graph.set_edge("q0", "n", matrix_unit(0, 0))
    for colour in range(3):
        graph.set_edge("q1", f"t{colour}", matrix_unit(0, colour))
        graph.set_edge("n", f"t{colour}", matrix_unit(0, colour, -1))
    return graph


def evaluated_response(
    graph: ExactGraph, open_vertices: tuple[str, ...]
) -> dict[tuple[int, ...], Fraction]:
    subset = ("q0", "q1") + open_vertices
    result: dict[tuple[int, ...], Fraction] = {}
    for open_colours in product(range(3), repeat=len(open_vertices)):
        value = Fraction(0)
        for q_colours in product(range(3), repeat=2):
            colours = {"q0": q_colours[0], "q1": q_colours[1]}
            colours.update(dict(zip(open_vertices, open_colours, strict=True)))
            value += graph.coefficient(colours, subset)
        result[open_colours] = value
    return result


def companion_pair_scalar(graph: ExactGraph) -> Fraction:
    total = Fraction(0)
    for colours_tuple in product(range(3), repeat=4):
        colours = dict(zip(("a0", "a1", "q0", "q1"), colours_tuple, strict=True))
        first = (
            graph.matrix("a0", "q0")[colours["a0"]][colours["q0"]]
            * graph.matrix("a1", "q1")[colours["a1"]][colours["q1"]]
        )
        second = (
            graph.matrix("a0", "q1")[colours["a0"]][colours["q1"]]
            * graph.matrix("a1", "q0")[colours["a1"]][colours["q0"]]
        )
        total += first + second
    return total


def complementary_permanent_coefficient(graph: ExactGraph) -> Fraction:
    roots = ("a0", "a1", "n")
    ports = ("t0", "t1", "t2")
    port_colours = {"t0": 0, "t1": 0, "t2": 2}
    total = Fraction(0)
    for assigned_ports in permutations(ports):
        for root_colours in product(range(3), repeat=3):
            term = Fraction(1)
            for root, port, colour in zip(roots, assigned_ports, root_colours, strict=True):
                term *= graph.matrix(root, port)[colour][port_colours[port]]
            total += term
    return total


def audit_source_adjacent_control() -> dict[str, object]:
    graph = build_source_adjacent_control()
    auxiliaries = ("q0", "q1", "n", "t0", "t1", "t2")
    ranks = {}
    for label in auxiliaries:
        x_rows = graph.matrix("a0", label)
        y_rows = graph.matrix("a1", label)
        ranks[label] = matrix_rank((*x_rows, *y_rows))
    assert ranks == {"q0": 1, "q1": 1, "n": 0, "t0": 1, "t1": 1, "t2": 1}

    all_ones = (Fraction(1), Fraction(1), Fraction(1))
    for colour in range(3):
        star_matrix = graph.matrix("n", f"t{colour}")
        star_row = tuple(
            sum((all_ones[index] * star_matrix[index][column] for index in range(3)), Fraction(0))
            for column in range(3)
        )
        expected = tuple(Fraction(-1 if index == colour else 0) for index in range(3))
        assert star_row == expected

    assert evaluated_response(graph, ()) == {(): Fraction(1)}
    promoted = ("n", "t0", "t1", "t2")
    pair_responses = [evaluated_response(graph, pair) for pair in combinations(promoted, 2)]
    assert all(all(value == 0 for value in response.values()) for response in pair_responses)
    top_response = evaluated_response(graph, promoted)
    assert all(value == 0 for value in top_response.values())

    assert companion_pair_scalar(graph) == 1
    permanent = complementary_permanent_coefficient(graph)
    assert permanent == -1

    root_vector = {"a0": 0, "a1": 0, "n": 0}
    assert all(
        graph.matrix(left, right)[root_vector[left]][root_vector[right]] == 0
        for left, right in combinations(root_vector, 2)
    )

    nonzero: dict[tuple[int, ...], Fraction] = {}
    for colours_tuple in product(range(3), repeat=8):
        colours = dict(zip(graph.vertices, colours_tuple, strict=True))
        value = graph.coefficient(colours)
        if value:
            nonzero[colours_tuple] = value
    expected_word = (0, 0, 0, 0, 0, 0, 0, 2)
    assert nonzero == {expected_word: Fraction(-2)}
    assert all(tuple([colour] * 8) not in nonzero for colour in range(3))
    return {
        "joint_ranks": ranks,
        "pair_responses_zero": len(pair_responses),
        "top_response_rows_zero": len(top_response),
        "raw_pair_companion": companion_pair_scalar(graph),
        "complementary_permanent_coefficient": permanent,
        "nonzero_full_coefficients": len(nonzero),
    }


def audit_rigid_controls() -> dict[str, int]:
    rank_one_labels = [(colour, sign) for colour in range(3) for sign in (-1, 1)]
    diagonal_coefficients = 0
    surviving_off_diagonal = 0
    for left, right in combinations(rank_one_labels, 2):
        left_colour, left_sign = left
        right_colour, right_sign = right
        coefficient = left_sign + right_sign
        if left_colour == right_colour:
            assert coefficient == 0
            diagonal_coefficients += int(coefficient != 0)
        elif coefficient:
            surviving_off_diagonal += 1
    assert diagonal_coefficients == 0
    assert surviving_off_diagonal > 0

    # Full-rank control: X sees colours 0,1 and Y sees colour 2.
    x_rows = ((Fraction(1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(1), Fraction(0)))
    y_rows = ((Fraction(0), Fraction(0), Fraction(1)),)
    assert matrix_rank((*x_rows, *y_rows)) == 3
    full_rank_diagonal = 0
    full_rank_off_diagonal = 0
    for left_colour in range(3):
        for right_colour in range(3):
            first = int(left_colour in (0, 1) and right_colour == 2)
            second = int(left_colour == 2 and right_colour in (0, 1))
            coefficient = first + second
            if left_colour == right_colour:
                full_rank_diagonal += int(coefficient != 0)
            else:
                full_rank_off_diagonal += int(coefficient != 0)
    assert full_rank_diagonal == 0
    assert full_rank_off_diagonal == 4
    return {
        "rank_one_rigid_labels": len(rank_one_labels),
        "rank_one_surviving_off_diagonal_pairs": surviving_off_diagonal,
        "full_rank_joint_rank": 3,
        "full_rank_off_diagonal_cells": full_rank_off_diagonal,
    }


def main() -> None:
    report = {
        "coordinate_alternative": audit_coordinate_alternative(),
        "matching_kill": audit_matching_kill(),
        "pair_companion_trichotomy": audit_pair_companion_trichotomy(),
        "homogeneous_identity": audit_homogeneous_identity(),
        "exceptional_flag": audit_exceptional_flag(),
        "gld3_triangle": audit_gld3_triangle(),
        "source_adjacent_control": audit_source_adjacent_control(),
        "rigid_controls": audit_rigid_controls(),
    }
    print("GLS56 focused exact verifier: PASS")
    for key, value in report.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
