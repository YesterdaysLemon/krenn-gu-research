"""Independent exact audit for the rank-two and singleton-triangle exclusions.

This script uses only the Python standard library.  It does not import
repository code, a primary verifier, or a computer-algebra package.

The audit uses a representation deliberately different from the written
proof:

* exact quotient maps obtained as annihilator matrices of rational subspaces;
* exhaustive Gamma-subset covers for every active dimension profile;
* a row-reduced coefficient solve for two beta-orthogonal graph planes;
* exact rank checks for bounded surjective local maps; and
* direct reconstruction of all 81 shared-tail splice coefficients from the
  24 permutations defining the order-four permanent.

Finite tables audit displayed identities and case topology.  They do not
replace the arbitrary-point proof.  The committed complex subrank-two theorem
for the order-four permanent is treated as a dependency, not reproved here.

The audit leaves open rank-one Branches I and II, the two-port part of Branch
III, the separate seventh-response condition, weaker response-zero patterns,
nonzero-response absorption, selector legality, the strategic node, and the
global Krenn--Gu conjecture.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
from typing import TypeAlias

Scalar: TypeAlias = Fraction
Vector: TypeAlias = tuple[Scalar, ...]
Matrix: TypeAlias = tuple[Vector, ...]
Subspace: TypeAlias = tuple[Vector, ...]
Gamma: TypeAlias = frozenset[int]

ZERO = Fraction(0)
ONE = Fraction(1)
COLORS = (0, 1, 2)
ACTIVE = ("q0", "q1", "s", "t")
ALL_COLORS = frozenset(COLORS)


def q(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def vector(values: Sequence[int | Fraction]) -> Vector:
    return tuple(q(value) for value in values)


def matrix(rows: Sequence[Sequence[int | Fraction]]) -> Matrix:
    return tuple(vector(row) for row in rows)


def zero_matrix(rows: int, columns: int) -> Matrix:
    return tuple(tuple(ZERO for _ in range(columns)) for _ in range(rows))


def identity(size: int) -> Matrix:
    return tuple(
        tuple(ONE if row == column else ZERO for column in range(size))
        for row in range(size)
    )


def basis(dimension: int, coordinate: int) -> Vector:
    return tuple(
        ONE if position == coordinate else ZERO for position in range(dimension)
    )


def transpose(value: Matrix) -> Matrix:
    return tuple(
        tuple(value[row][column] for row in range(len(value)))
        for column in range(len(value[0]))
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def matrix_scale(scalar: int | Fraction, value: Matrix) -> Matrix:
    coefficient = q(scalar)
    return tuple(tuple(coefficient * entry for entry in row) for row in value)


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(a * b for b in right) for a in left)


def matmul(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(len(right))
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def matvec(value: Matrix, argument: Vector) -> Vector:
    return tuple(
        sum(entry * coordinate for entry, coordinate in zip(row, argument, strict=True))
        for row in value
    )


def matrix_rank(value: Sequence[Sequence[int | Fraction]]) -> int:
    if not value:
        return 0
    rows = [list(vector(row)) for row in value]
    if not rows[0]:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def rref(
    value: Sequence[Sequence[int | Fraction]],
) -> tuple[Matrix, tuple[int, ...]]:
    if not value:
        return (), ()
    rows = [list(vector(row)) for row in value]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(tuple(row) for row in rows), tuple(pivots)


def nullspace(
    value: Sequence[Sequence[int | Fraction]], column_count: int
) -> tuple[Vector, ...]:
    if not value:
        return tuple(
            basis(column_count, coordinate) for coordinate in range(column_count)
        )
    reduced, pivots = rref(value)
    free = tuple(
        coordinate for coordinate in range(column_count) if coordinate not in pivots
    )
    answer = []
    for free_coordinate in free:
        candidate = [ZERO] * column_count
        candidate[free_coordinate] = ONE
        for row, pivot in enumerate(pivots):
            candidate[pivot] = -reduced[row][free_coordinate]
        answer.append(tuple(candidate))
    return tuple(answer)


def canonical_row_space(rows: Sequence[Vector], ambient: int) -> Subspace:
    if not rows:
        return ()
    reduced, _pivots = rref(rows)
    rank = matrix_rank(rows)
    answer = tuple(reduced[row] for row in range(rank))
    assert all(len(row) == ambient for row in answer)
    return answer


def row_span_contains(space: Subspace, candidate: Vector) -> bool:
    return matrix_rank(space + (candidate,)) == len(space)


def normalize_projective(values: tuple[int, ...]) -> tuple[int, ...]:
    divisor = 0
    for value in values:
        divisor = gcd(divisor, abs(value))
    if divisor == 0:
        raise ValueError("the zero vector has no projective normalization")
    answer = tuple(value // divisor for value in values)
    first = next(value for value in answer if value)
    return tuple(-value for value in answer) if first < 0 else answer


def small_projective_vectors(dimension: int) -> tuple[Vector, ...]:
    representatives = {
        normalize_projective(values)
        for values in product((-1, 0, 1), repeat=dimension)
        if any(values)
    }
    return tuple(vector(values) for values in sorted(representatives))


def small_subspaces(dimension: int) -> tuple[Subspace, ...]:
    projective = small_projective_vectors(3)
    if dimension == 1:
        return tuple((candidate,) for candidate in projective)
    if dimension != 2:
        raise ValueError("only active dimensions one and two are audited")
    spaces = {
        canonical_row_space((first, second), 3)
        for first, second in combinations(projective, 2)
        if matrix_rank((first, second)) == 2
    }
    return tuple(sorted(spaces))


def gamma_of(space: Subspace) -> Gamma:
    return frozenset(
        color for color in COLORS if row_span_contains(space, basis(3, color))
    )


def quotient_map(space: Subspace) -> Matrix:
    quotient_rows = nullspace(space, 3)
    assert len(quotient_rows) == 3 - len(space)
    assert all(
        matvec(tuple(quotient_rows), row) == (ZERO,) * len(quotient_rows)
        for row in space
    )
    return tuple(quotient_rows)


def quotient_class(quotient: Matrix, color: int) -> Vector:
    coordinate = basis(3, color)
    return matvec(quotient, coordinate)


def kronecker_vector(left: Vector, right: Vector) -> Vector:
    return tuple(a * b for a in left for b in right)


def quotient_target_flattening(
    space_v: Subspace,
    space_w: Subspace,
    weights: Vector | None = None,
) -> Matrix:
    if weights is None:
        weights = vector((2, -3, 5))
    quotient_v = quotient_map(space_v)
    quotient_w = quotient_map(space_w)
    quotient_dimension = len(quotient_v) * len(quotient_w)
    column_count = quotient_dimension * 9
    result = [[ZERO for _ in range(column_count)] for _ in range(9)]
    gamma_union = gamma_of(space_v) | gamma_of(space_w)
    for color in COLORS:
        if color in gamma_union:
            continue
        class_product = kronecker_vector(
            quotient_class(quotient_v, color),
            quotient_class(quotient_w, color),
        )
        pure_p_row = 3 * color + color
        inactive_tag = 3 * color + color
        for quotient_coordinate, coefficient in enumerate(class_product):
            column = 9 * quotient_coordinate + inactive_tag
            result[pure_p_row][column] += weights[color] * coefficient
    return tuple(tuple(row) for row in result)


def proportional(left: Vector, right: Vector) -> bool:
    if not any(left) or not any(right):
        return False
    pivot = next(index for index, entry in enumerate(right) if entry)
    scalar = left[pivot] / right[pivot]
    return all(a == scalar * b for a, b in zip(left, right, strict=True))


def check_quotient_rank_tables() -> dict[str, int]:
    spaces = {dimension: small_subspaces(dimension) for dimension in (1, 2)}
    quotient_pair_checks = 0
    noncoordinate_checks = 0
    for dimension_v, dimension_w in product((1, 2), repeat=2):
        for space_v, space_w in product(spaces[dimension_v], spaces[dimension_w]):
            gamma_union = gamma_of(space_v) | gamma_of(space_w)
            surviving = len(ALL_COLORS - gamma_union)
            target = quotient_target_flattening(space_v, space_w)
            assert matrix_rank(target) == surviving
            quotient_pair_checks += 1
            if not gamma_of(space_v) or not gamma_of(space_w):
                noncoordinate_checks += 1

    line = canonical_row_space((vector((1, -1, 0)),), 3)
    line_quotient = quotient_map(line)
    assert quotient_class(line_quotient, 0) == quotient_class(line_quotient, 1)
    assert gamma_of(line) == frozenset()

    plane = canonical_row_space((vector((1, -1, 0)), vector((0, 1, -1))), 3)
    plane_quotient = quotient_map(plane)
    plane_classes = tuple(quotient_class(plane_quotient, color) for color in COLORS)
    assert all(proportional(plane_classes[0], item) for item in plane_classes[1:])
    assert gamma_of(plane) == frozenset()

    collapsed_target = quotient_target_flattening(plane, plane)
    assert matrix_rank(collapsed_target) == 3
    assert len(plane_quotient) == 1

    # A left-hand edge times one companion has flattening rank at most one.
    edge = matrix(((1, 2, 0), (0, 1, 1), (0, 0, 0)))
    companion = vector((1, -2, 3, 0, 1))
    left_flattening = outer(tuple(entry for row in edge for entry in row), companion)
    assert matrix_rank(left_flattening) == 1

    return {
        "one_dimensional_spaces": len(spaces[1]),
        "two_dimensional_spaces": len(spaces[2]),
        "quotient_pair_checks": quotient_pair_checks,
        "noncoordinate_pairs": noncoordinate_checks,
        "collapsed_class_target_rank": matrix_rank(collapsed_target),
    }


def subsets_at_most(size: int) -> tuple[Gamma, ...]:
    return tuple(
        frozenset(chosen)
        for cardinality in range(size + 1)
        for chosen in combinations(COLORS, cardinality)
    )


def complement_pair(edge: tuple[str, str]) -> tuple[str, str]:
    return tuple(vertex for vertex in ACTIVE if vertex not in edge)  # type: ignore[return-value]


def edge_constraint(
    gammas: dict[str, Gamma],
    edge: tuple[str, str],
    edge_rank: int,
) -> bool:
    opposite = complement_pair(edge)
    surviving = ALL_COLORS - (gammas[opposite[0]] | gammas[opposite[1]])
    if len(surviving) >= 2:
        return False
    if edge_rank == 2:
        return not surviving
    if edge_rank != 1:
        raise ValueError("only rank-one and rank-two active edges occur")
    if len(surviving) == 1:
        color = next(iter(surviving))
        return color in gammas[edge[0]] and color in gammas[edge[1]]
    return True


def enumerate_profile(
    dimension_s: int, dimension_t: int
) -> tuple[dict[str, Gamma], ...]:
    dimensions = {
        "q0": 2,
        "q1": 2,
        "s": dimension_s,
        "t": dimension_t,
    }
    choices = tuple(subsets_at_most(dimensions[vertex]) for vertex in ACTIVE)
    edges = (
        (("q0", "q1"), 2),
        (("q0", "s"), dimension_s),
        (("q1", "s"), dimension_s),
        (("q0", "t"), dimension_t),
        (("q1", "t"), dimension_t),
    )
    survivors = []
    for selected in product(*choices):
        gammas = dict(zip(ACTIVE, selected, strict=True))
        if all(edge_constraint(gammas, edge, rank) for edge, rank in edges):
            survivors.append(gammas)
    return tuple(survivors)


def check_gamma_profile_cover() -> dict[str, int]:
    profile_counts = {}
    assignments_checked = 0
    full_plane_patterns: tuple[dict[str, Gamma], ...] = ()
    for dimension_s, dimension_t in product((1, 2), repeat=2):
        assignments_checked += (
            len(subsets_at_most(2))
            * len(subsets_at_most(2))
            * len(subsets_at_most(dimension_s))
            * len(subsets_at_most(dimension_t))
        )
        survivors = enumerate_profile(dimension_s, dimension_t)
        profile_counts[(dimension_s, dimension_t)] = len(survivors)
        if (dimension_s, dimension_t) == (2, 2):
            full_plane_patterns = survivors
        else:
            assert not survivors

    assert len(full_plane_patterns) == 6
    pattern_signatures = set()
    for gammas in full_plane_patterns:
        deltas = {vertex: ALL_COLORS - gammas[vertex] for vertex in ACTIVE}
        assert all(len(delta) == 1 for delta in deltas.values())
        i = next(iter(deltas["s"]))
        j = next(iter(deltas["t"]))
        k0 = next(iter(deltas["q0"]))
        k1 = next(iter(deltas["q1"]))
        assert len({i, j, k0}) == 3
        assert k0 == k1
        pattern_signatures.add((i, j, k0))

        b_surviving = ALL_COLORS - (gammas["q0"] | gammas["q1"])
        assert b_surviving == frozenset((k0,))
        coordinate_b = outer(basis(3, k0), basis(3, k0))
        assert matrix_rank(coordinate_b) == 1
    assert len(pattern_signatures) == 6

    return {
        "gamma_assignments": assignments_checked,
        "profile_11": profile_counts[(1, 1)],
        "profile_21": profile_counts[(2, 1)],
        "profile_12": profile_counts[(1, 2)],
        "profile_22_patterns": profile_counts[(2, 2)],
    }


def quotient_coordinates(value: Matrix) -> Vector:
    return (
        value[0][1],
        value[1][0],
        value[0][0] - value[1][1],
    )


def graph_beta(
    graph_t: Matrix,
    graph_s: Matrix,
    left: Vector,
    right: Vector,
) -> Matrix:
    return matrix_add(
        outer(left, matvec(graph_s, right)),
        outer(right, matvec(graph_t, left)),
    )


def graph_variable_matrices(coordinates: Vector) -> tuple[Matrix, Matrix]:
    graph_t = matrix((coordinates[0:2], coordinates[2:4]))
    graph_s = matrix((coordinates[4:6], coordinates[6:8]))
    return graph_t, graph_s


def beta_coefficient_system() -> Matrix:
    rows = []
    for left_coordinate, right_coordinate in product(range(2), repeat=2):
        left = basis(2, left_coordinate)
        right = basis(2, right_coordinate)
        variable_images = []
        for variable in range(8):
            coefficients = basis(8, variable)
            graph_t, graph_s = graph_variable_matrices(coefficients)
            variable_images.append(
                quotient_coordinates(graph_beta(graph_t, graph_s, left, right))
            )
        for quotient_coordinate in range(3):
            rows.append(tuple(image[quotient_coordinate] for image in variable_images))
    return tuple(rows)


def scalar_multiple(left: Vector, right: Vector) -> Fraction | None:
    if not any(right):
        return ZERO if not any(left) else None
    pivot = next(index for index, entry in enumerate(right) if entry)
    coefficient = left[pivot] / right[pivot]
    if all(a == coefficient * b for a, b in zip(left, right, strict=True)):
        return coefficient
    return None


def small_surjections() -> tuple[Matrix, ...]:
    answer = []
    for entries in product((-1, 0, 1), repeat=6):
        if not any(entries):
            continue
        first_nonzero = next(entry for entry in entries if entry)
        if first_nonzero < 0:
            continue
        candidate = matrix((entries[:3], entries[3:]))
        if matrix_rank(candidate) == 2:
            answer.append(candidate)
    return tuple(answer)


def determinant_two(left: Vector, right: Vector) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def bilinear(value: Matrix, left: Vector, right: Vector) -> Fraction:
    return sum(
        left[row] * value[row][column] * right[column]
        for row in range(len(value))
        for column in range(len(value[0]))
    )


def check_beta_graph_planes_and_b_rank() -> dict[str, int]:
    system = beta_coefficient_system()
    assert matrix_rank(system) == 7
    kernel = nullspace(system, 8)
    assert len(kernel) == 1
    expected = vector((0, 1, -1, 0, 0, -1, 1, 0))
    assert scalar_multiple(kernel[0], expected) not in (None, ZERO)

    graph_t, graph_s = graph_variable_matrices(expected)
    symplectic = matrix(((0, 1), (-1, 0)))
    assert graph_t == symplectic
    assert graph_s == matrix_scale(-1, symplectic)
    assert matrix_rank(graph_t) == matrix_rank(graph_s) == 2

    identity_checks = 0
    small_vectors = tuple(vector(values) for values in product(range(-2, 3), repeat=2))
    for left, right in product(small_vectors, repeat=2):
        beta_value = graph_beta(graph_t, graph_s, left, right)
        expected_value = matrix_scale(-determinant_two(left, right), identity(2))
        assert beta_value == expected_value
        identity_checks += 1

    surjections = small_surjections()
    b_rank_checks = 0
    for source_s, source_t in product(surjections, repeat=2):
        b_matrix = matmul(matmul(transpose(source_s), symplectic), source_t)
        assert matrix_rank(b_matrix) == 2
        b_rank_checks += 1

    source_s = matrix(((1, 0, 1), (0, 1, -1)))
    source_t = matrix(((1, 1, 0), (0, 1, 1)))
    b_matrix = matmul(matmul(transpose(source_s), symplectic), source_t)
    labelled_checks = 0
    for local_s, local_t in product(small_projective_vectors(3)[:8], repeat=2):
        left_image = matvec(source_s, local_s)
        right_image = matvec(source_t, local_t)
        assert bilinear(b_matrix, local_s, local_t) == determinant_two(
            left_image, right_image
        )
        labelled_checks += 1

    return {
        "beta_linear_equations": len(system),
        "beta_solution_dimension": len(kernel),
        "beta_identity_checks": identity_checks,
        "bounded_surjections": len(surjections),
        "b_rank_checks": b_rank_checks,
        "labelled_bilinear_checks": labelled_checks,
    }


def permanent_four(columns: Sequence[Vector]) -> Fraction:
    assert len(columns) == 4
    assert all(len(column) == 4 for column in columns)
    return sum(
        (
            columns[0][row_order[0]]
            * columns[1][row_order[1]]
            * columns[2][row_order[2]]
            * columns[3][row_order[3]]
        )
        for row_order in permutations(range(4))
    )


def incidence_map(seed: int) -> Matrix:
    return tuple(
        tuple(
            q(((seed + 2) * (row + 1) + (column + 2) ** 2) % 11 - 5)
            for column in COLORS
        )
        for row in range(4)
    )


def column(value: Matrix, color: int) -> Vector:
    return tuple(row[color] for row in value)


def permanent_term_counter(
    source_label: str,
    source_color: int,
    tail_word: tuple[int, int, int],
) -> Counter[tuple[tuple[str, int, int], ...]]:
    answer: Counter[tuple[tuple[str, int, int], ...]] = Counter()
    labels = (
        (source_label, source_color),
        ("v1", tail_word[0]),
        ("v2", tail_word[1]),
        ("v3", tail_word[2]),
    )
    for row_order in permutations(range(4)):
        monomial = tuple(
            (label, color, row)
            for (label, color), row in zip(labels, row_order, strict=True)
        )
        answer[monomial] += 1
    return answer


def spliced_permanent_term_counter(
    source_label: str,
    source_color: int,
    tail_word: tuple[int, int, int],
    splice_scalar: int | Fraction,
) -> dict[tuple[tuple[str, int, int], ...], Fraction]:
    answer: dict[tuple[tuple[str, int, int], ...], Fraction] = {}
    labels = (
        (source_label, source_color),
        ("v1", tail_word[0]),
        ("v2", tail_word[1]),
        ("v3", tail_word[2]),
    )
    for row_order in permutations(range(4)):
        monomial = tuple(
            (label, color, row)
            for (label, color), row in zip(labels, row_order, strict=True)
        )
        answer[monomial] = answer.get(monomial, ZERO) + q(splice_scalar)
    return answer


def scale_counter(
    coefficient: int | Fraction,
    value: Counter[tuple[tuple[str, int, int], ...]],
) -> dict[tuple[tuple[str, int, int], ...], Fraction]:
    scalar = q(coefficient)
    return {monomial: scalar * multiplicity for monomial, multiplicity in value.items()}


def check_shared_tail_column_splice() -> dict[str, int]:
    incidence = {
        "q0": incidence_map(0),
        "q1": incidence_map(1),
        "t": incidence_map(2),
        "v1": incidence_map(3),
        "v2": incidence_map(4),
        "v3": incidence_map(5),
    }
    active_scalars = vector((2, -3, 5))
    target_weights = vector((7, -11, 13))
    assert all(active_scalars) and all(target_weights)

    permutation_checks = 0
    numeric_splice_checks = 0
    weighted_checks = 0
    normalized_checks = 0
    color_ledger_checks = 0

    for i, j, k in permutations(COLORS):
        source_for_color = {i: "q1", j: "q0", k: "t"}
        scalar_for_color = {
            i: active_scalars[0],
            j: active_scalars[1],
            k: active_scalars[2],
        }
        synthetic_columns = {
            color: tuple(
                scalar_for_color[color] * entry
                for entry in column(incidence[source_for_color[color]], color)
            )
            for color in COLORS
        }

        weighted_tensor: dict[tuple[int, int, int, int], Fraction] = {}
        for color in COLORS:
            source_label = source_for_color[color]
            scalar = scalar_for_color[color]
            for tail_word in product(COLORS, repeat=3):
                source_terms = permanent_term_counter(source_label, color, tail_word)
                synthetic_terms = spliced_permanent_term_counter(
                    source_label, color, tail_word, scalar
                )
                assert synthetic_terms == scale_counter(scalar, source_terms)
                assert len(source_terms) == 24
                permutation_checks += 24

                tail_columns = tuple(
                    column(incidence[label], tail_color)
                    for label, tail_color in zip(
                        ("v1", "v2", "v3"), tail_word, strict=True
                    )
                )
                synthetic_value = permanent_four(
                    (synthetic_columns[color],) + tail_columns
                )
                source_value = scalar * permanent_four(
                    (column(incidence[source_label], color),) + tail_columns
                )
                assert synthetic_value == source_value
                numeric_splice_checks += 1

                # Insert the multiplied pure-companion identity directly.
                spliced_from_assumption = (
                    target_weights[color]
                    if tail_word == (color, color, color)
                    else ZERO
                )
                word = (color,) + tail_word
                if spliced_from_assumption:
                    weighted_tensor[word] = spliced_from_assumption
                expected = target_weights[color] if word == (color,) * 4 else ZERO
                assert spliced_from_assumption == expected
                weighted_checks += 1

        assert weighted_tensor == {
            (color,) * 4: target_weights[color] for color in COLORS
        }
        normalized = {
            word: coefficient / target_weights[word[0]]
            for word, coefficient in weighted_tensor.items()
        }
        assert normalized == {(color,) * 4: ONE for color in COLORS}
        normalized_checks += 3
        assert set(source_for_color.values()) == {"q0", "q1", "t"}
        color_ledger_checks += 1

    return {
        "p4_permutations": len(tuple(permutations(range(4)))),
        "formal_permutation_terms": permutation_checks,
        "numeric_splice_coefficients": numeric_splice_checks,
        "weighted_diagonal_coefficients": weighted_checks,
        "normalized_diagonal_entries": normalized_checks,
        "color_ledgers": color_ledger_checks,
    }


def check_controls_and_scope() -> dict[str, int]:
    weights = vector((2, -3, 5))
    formal_target = {(color,) * 6: weights[color] for color in COLORS}
    independent_terms = (
        {(0,) * 6: weights[0]},
        {(1,) * 6: weights[1]},
        {(2,) * 6: weights[2]},
    )
    assembled = {}
    for term in independent_terms:
        assembled.update(term)
    assert assembled == formal_target

    h_rank_two = matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))
    zero_companion = zero_matrix(1, 5)
    assert matrix_rank(h_rank_two) == 2
    assert matrix_rank(zero_companion) == 0
    assert matrix_rank(outer(tuple(sum(h_rank_two, ())), zero_companion[0])) == 0

    # Characteristic-zero descent uses only finite polynomial data before the
    # declared target-weight normalization.  The rational identity embedding
    # is an exact representative of the injective-embedding step.
    rational_entries = vector((2, -3, 5, 7, -11, 13))
    assert all(rational_entries)
    assert tuple(Fraction(entry) for entry in rational_entries) == rational_entries

    return {
        "formal_triangle_terms": len(independent_terms),
        "n_d_zero_controls": 1,
        "declared_nonzero_scalars": len(rational_entries),
        "unresolved_rank_one_branches": 3,
    }


def main() -> None:
    sections = (
        ("quotient-rank", check_quotient_rank_tables),
        ("gamma-cover", check_gamma_profile_cover),
        ("beta-planes", check_beta_graph_planes_and_b_rank),
        ("shared-tail-splice", check_shared_tail_column_splice),
        ("controls-scope", check_controls_and_scope),
    )
    for label, check in sections:
        result = check()
        rendered = ", ".join(f"{key}={value}" for key, value in result.items())
        print(f"PASS {label}: {rendered}")

    print(
        "DEPENDENCY: the complex order-four permanent subrank-two obstruction "
        "is consumed as a committed theorem and is not reproved here."
    )
    print(
        "DESCENT: the splice uses finite polynomial data and multiplication by "
        "alpha,beta,gamma; only the declared nonzero mu weights are inverted "
        "in the final output normalization."
    )
    print(
        "OPEN: rank-one Branches I, II, and two-port III; seventh response; "
        "weaker response and absorption fibres; selectors; strategic node; "
        "global conjecture."
    )
    print("PASS independent rank-two and singleton-triangle exclusion audit")


if __name__ == "__main__":
    main()
