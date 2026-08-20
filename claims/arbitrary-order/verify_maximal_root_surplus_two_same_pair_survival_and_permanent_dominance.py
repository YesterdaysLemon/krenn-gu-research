"""Focused exact replay for same-pair survival and permanent dominance.

The arbitrary-r arguments in the owning theorem are the proofs.  This script
uses exact symbolic arithmetic only to replay the matching-grade, rank-one
triangle, and complementary-permanent Jacobian identities at bounded ranks.
"""

from __future__ import annotations

import sys
from functools import cache
from itertools import combinations, product
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from krenn_gu.bootstrap import bootstrap

REPO_ROOT, HERE = bootstrap(__file__)


@cache
def permanent(entries: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Return the permanent by exact cofactor expansion."""

    if not entries:
        return sp.Integer(1)
    width = len(entries[0])
    assert len(entries) == width
    tail = entries[1:]
    answer = sp.Integer(0)
    for column, value in enumerate(entries[0]):
        if value == 0:
            continue
        minor = tuple(row[:column] + row[column + 1 :] for row in tail)
        answer += value * permanent(minor)
    return sp.expand(answer)


def matrix_permanent(matrix: sp.MatrixBase) -> sp.Expr:
    """Convert a SymPy matrix to the immutable input used by ``permanent``."""

    rows, columns = matrix.shape
    assert rows == columns
    entries = tuple(
        tuple(matrix[row, column] for column in range(columns)) for row in range(rows)
    )
    return permanent(entries)


def root_partial_matchings(
    root_count: int, edge_count: int
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate matchings of a prescribed size in the root set."""

    edges = tuple(combinations(range(root_count), 2))
    answer = []
    for selected in combinations(edges, edge_count):
        endpoints = tuple(vertex for edge in selected for vertex in edge)
        if len(set(endpoints)) == 2 * edge_count:
            answer.append(selected)
    return tuple(answer)


def companion_reading(
    incidence: sp.MatrixBase,
    outside_label: tuple[int, ...],
    root_edges: dict[tuple[int, int], sp.Symbol],
) -> sp.Expr:
    """Scalar root-contracted companion of one even outside label."""

    root_count, outside_count = incidence.shape
    grade_numerator = len(outside_label) - 2
    assert grade_numerator >= 0 and grade_numerator % 2 == 0
    grade = grade_numerator // 2
    outside_remainder = tuple(
        outside for outside in range(outside_count) if outside not in outside_label
    )
    assert len(outside_remainder) == root_count - 2 * grade

    answer = sp.Integer(0)
    for matching in root_partial_matchings(root_count, grade):
        used_roots = {root for edge in matching for root in edge}
        remaining_roots = tuple(
            root for root in range(root_count) if root not in used_roots
        )
        cross = incidence.extract(remaining_roots, outside_remainder)
        root_factor = sp.prod(root_edges[edge] for edge in matching)
        answer += root_factor * matrix_permanent(cross)
    return sp.expand(answer)


def identity_ones_incidence(root_count: int) -> sp.Matrix:
    """The point A_0=[I_r | 1 | 1] from equation (22)."""

    return sp.eye(root_count).row_join(sp.ones(root_count, 2))


def expected_a0_reading(root_count: int, label: tuple[int, int]) -> int:
    """Equation (23), indexed by the two deleted columns."""

    final_columns = {root_count, root_count + 1}
    final_count = len(set(label) & final_columns)
    return (2, 1, 1)[final_count]


def check_matching_grades(root_count: int) -> tuple[int, int]:
    """Replay the grade-zero reading and root-edge annihilation in Lemma 1."""

    outside_count = root_count + 2
    incidence = sp.Matrix(
        root_count,
        outside_count,
        lambda row, column: sp.Symbol(f"x{root_count}_{row}_{column}"),
    )
    root_edges = {
        edge: sp.Symbol(f"rho{root_count}_{edge[0]}_{edge[1]}")
        for edge in combinations(range(root_count), 2)
    }
    root_symbols = tuple(root_edges.values())
    zero_root_edges = {symbol: 0 for symbol in root_symbols}
    a0_substitution = {
        incidence[row, column]: identity_ones_incidence(root_count)[row, column]
        for row in range(root_count)
        for column in range(outside_count)
    }

    pair_count = 0
    higher_count = 0
    for label_size in range(2, outside_count + 1, 2):
        grade = (label_size - 2) // 2
        for label in combinations(range(outside_count), label_size):
            reading = companion_reading(incidence, label, root_edges)
            root_polynomial = sp.Poly(reading, *root_symbols)
            assert root_polynomial.monoms()
            assert {sum(monomial) for monomial in root_polynomial.monoms()} == {grade}
            if grade == 0:
                pair_count += 1
                assert sp.expand(reading.subs(zero_root_edges) - reading) == 0
                a0_value = reading.subs(a0_substitution)
                assert a0_value == expected_a0_reading(root_count, label)
            else:
                higher_count += 1
                assert reading.subs(zero_root_edges) == 0

    assert pair_count == sp.binomial(outside_count, 2)
    assert higher_count == sum(
        sp.binomial(outside_count, size) for size in range(4, outside_count + 1, 2)
    )
    return int(pair_count), int(higher_count)


def high_cofactor_map(
    root_count: int,
) -> tuple[tuple[tuple[int, ...], ...], sp.Matrix, tuple[sp.Matrix, ...]]:
    """Build the common cofactor map Psi in equation (19)."""

    high_count = root_count - 1
    high_maps = tuple(
        sp.Matrix(
            root_count,
            3,
            lambda row, colour, high=high: sp.Symbol(
                f"h{root_count}_{high}_{row}_{colour}"
            ),
        )
        for high in range(high_count)
    )
    high_words = tuple(product(range(3), repeat=high_count))
    cofactor_columns = []
    for omitted_root in range(root_count):
        entries = []
        retained_roots = tuple(
            root for root in range(root_count) if root != omitted_root
        )
        for word in high_words:
            high_matrix = sp.Matrix(
                [
                    [high_maps[high][root, word[high]] for high in range(high_count)]
                    for root in retained_roots
                ]
            )
            entries.append(matrix_permanent(high_matrix))
        cofactor_columns.append(sp.Matrix(entries))
    return high_words, sp.Matrix.hstack(*cofactor_columns), high_maps


def check_common_cofactor_expansion(root_count: int) -> sp.Matrix:
    """Replay equations (16) and (19) for the three rank-one low modes."""

    high_words, psi, high_maps = high_cofactor_map(root_count)
    for low_mode in range(3):
        alpha = sp.Matrix(
            [
                sp.Symbol(f"alpha{root_count}_{low_mode}_{root}")
                for root in range(root_count)
            ]
        )
        expected_high_tensor = psi * alpha
        for low_colour in range(3):
            low_column = alpha if low_colour == low_mode else sp.zeros(root_count, 1)
            for word_number, word in enumerate(high_words):
                columns = [low_column]
                columns.extend(
                    high_maps[high][:, word[high]] for high in range(root_count - 1)
                )
                direct = matrix_permanent(sp.Matrix.hstack(*columns))
                expected = (
                    expected_high_tensor[word_number]
                    if low_colour == low_mode
                    else sp.Integer(0)
                )
                assert sp.expand(direct - expected) == 0
    return psi


def pure_tensor(side_size: int, colour: int) -> sp.Matrix:
    """Coordinate vector of the constant-colour word on one tensor shore."""

    words = tuple(product(range(3), repeat=side_size))
    vector = sp.zeros(len(words), 1)
    vector[words.index((colour,) * side_size)] = 1
    return vector


def symmetric_product_matrix(vector: sp.MatrixBase) -> sp.Matrix:
    """Matrix for the equations defining S_b in (10)."""

    root_count = vector.rows
    rows = []
    for left, right in combinations(range(root_count), 2):
        row = [sp.Integer(0)] * root_count
        row[left] = vector[right]
        row[right] = vector[left]
        rows.append(row)
    return sp.Matrix(rows)


def check_symmetric_kernel_and_triangle(root_count: int, psi: sp.Matrix) -> int:
    """Replay (17)--(20) and the rank-one triangle contradiction."""

    # If only two rank-one modes occur, equation (6) has rank one on the
    # left of their cut, while the three nonzero pure target words have rank 3.
    low_pure = tuple(pure_tensor(2, colour) for colour in range(3))
    high_pure = tuple(pure_tensor(root_count, colour) for colour in range(3))
    weights = tuple(
        sp.Symbol(f"mu{root_count}_{colour}", nonzero=True) for colour in range(3)
    )
    target_flattening = sum(
        (
            weights[colour] * low_pure[colour] * high_pure[colour].T
            for colour in range(3)
        ),
        sp.zeros(3**2, 3**root_count),
    )
    assert target_flattening.rank() == 3

    # The quotient argument before (17) assigns one distinct target coordinate
    # line to each of the three low modes.  Its only covers are permutations.
    quotient_covers = tuple(
        choices
        for choices in product((0, 1, 2, None), repeat=3)
        if all(colour in choices for colour in range(3))
    )
    assert len(quotient_covers) == 6
    assert all(sorted(choices) == [0, 1, 2] for choices in quotient_covers)

    # After the relabelling (17), the 000,111,222 low words isolate the
    # bc,ac,ab summands respectively, exactly as in (18).
    low_isolation = sp.Matrix(
        [[int(low_mode == colour) for colour in range(3)] for low_mode in range(3)]
    )
    assert low_isolation == sp.eye(3)
    anchored_high = sp.Matrix.hstack(
        *(weights[colour] * pure_tensor(root_count - 1, colour) for colour in range(3))
    )
    assert anchored_high.rank() == 3
    assert anchored_high[:, 1:].rank() == 2

    chart_count = 0
    for support_size in range(1, root_count + 1):
        for support in combinations(range(root_count), support_size):
            chart_count += 1
            vector = sp.zeros(root_count, 1)
            for coordinate in support:
                vector[coordinate] = sp.Symbol(
                    f"v{root_count}_{support_size}_{coordinate}", nonzero=True
                )
            kernel_matrix = symmetric_product_matrix(vector)
            expected_rank = root_count - 1 if support_size <= 2 else root_count
            assert kernel_matrix.rank() == expected_rank

            if support_size >= 3:
                # Then S_b=0, so a nonzero active endpoint already contradicts
                # the assumed raw failure.
                continue

            kernel_generator = sp.zeros(root_count, 1)
            if support_size == 1:
                kernel_generator[support[0]] = 1
            else:
                left, right = support
                kernel_generator[left] = vector[left]
                kernel_generator[right] = -vector[right]
            assert kernel_matrix * kernel_generator == sp.zeros(kernel_matrix.rows, 1)

            beta = sp.Symbol(f"beta{root_count}_{support_size}", nonzero=True)
            gamma = sp.Symbol(f"gamma{root_count}_{support_size}", nonzero=True)
            alpha_b = beta * kernel_generator
            alpha_c = gamma * kernel_generator
            k_b = psi * alpha_b
            k_c = psi * alpha_c
            assert sp.expand(gamma * k_b - beta * k_c) == sp.zeros(psi.rows, 1)

    assert chart_count == 2**root_count - 1
    return chart_count


def phi_value(matrix: sp.MatrixBase, deleted: tuple[int, int]) -> sp.Expr:
    """One coordinate of the complementary-permanent map (21)."""

    retained = tuple(column for column in range(matrix.cols) if column not in deleted)
    return matrix_permanent(matrix[:, retained])


def phi_jacobian_at_a0(
    root_count: int, output_labels: tuple[tuple[int, int], ...]
) -> sp.Matrix:
    """Compute the exact Jacobian of Phi_r at A_0 by permanent cofactors."""

    a0 = identity_ones_incidence(root_count)
    variable_count = root_count * (root_count + 2)
    jacobian = sp.zeros(len(output_labels), variable_count)
    for output_number, deleted in enumerate(output_labels):
        retained = tuple(
            column for column in range(root_count + 2) if column not in deleted
        )
        for row in range(root_count):
            for column in retained:
                remaining_rows = tuple(
                    candidate for candidate in range(root_count) if candidate != row
                )
                remaining_columns = tuple(
                    candidate for candidate in retained if candidate != column
                )
                cofactor = a0.extract(remaining_rows, remaining_columns)
                variable = row * (root_count + 2) + column
                jacobian[output_number, variable] = matrix_permanent(cofactor)
    return jacobian


def tangent_direction(
    root_count: int, entries: dict[tuple[int, int], int]
) -> sp.Matrix:
    """A coordinate tangent vector in Mat_{r x (r+2)}."""

    direction = sp.zeros(root_count * (root_count + 2), 1)
    for (row, column), value in entries.items():
        direction[row * (root_count + 2) + column] = value
    return direction


def check_permanent_dominance(root_count: int) -> tuple[int, int, int]:
    """Replay equations (21)--(27) by an exact SymPy Jacobian calculation."""

    a_column = root_count
    b_column = root_count + 1
    root_pairs = tuple(combinations(range(root_count), 2))
    output_labels = (
        root_pairs
        + tuple((root, b_column) for root in range(root_count))
        + tuple((root, a_column) for root in range(root_count))
        + ((a_column, b_column),)
    )
    output_count = sp.binomial(root_count + 2, 2)
    assert len(output_labels) == output_count

    a0 = identity_ones_incidence(root_count)
    readings = {label: phi_value(a0, label) for label in output_labels}
    assert all(
        readings[label] == expected_a0_reading(root_count, label)
        for label in output_labels
    )

    jacobian = phi_jacobian_at_a0(root_count, output_labels)
    assert jacobian.rank() == output_count

    exchange_directions = tuple(
        tangent_direction(
            root_count,
            {
                (left, right): 1,
                (left, a_column): -1,
                (left, b_column): -1,
            },
        )
        for left, right in root_pairs
    )
    a_directions = tuple(
        tangent_direction(root_count, {(row, a_column): 1}) for row in range(root_count)
    )
    b_directions = tuple(
        tangent_direction(root_count, {(row, b_column): 1}) for row in range(root_count)
    )
    diagonal_direction = tangent_direction(root_count, {(0, 0): 1})
    directions = (
        exchange_directions + a_directions + b_directions + (diagonal_direction,)
    )
    assert len(directions) == output_count

    directional_jacobian = jacobian * sp.Matrix.hstack(*directions)
    for direction_number, pair in enumerate(root_pairs):
        expected = sp.zeros(output_count, 1)
        expected[output_labels.index(pair)] = -2
        assert directional_jacobian[:, direction_number] == expected

    determinant = int(directional_jacobian.det(method="domain-ge"))
    expected_absolute = 2 ** int(sp.binomial(root_count, 2))
    assert abs(determinant) == expected_absolute
    return int(output_count), int(jacobian.rank()), determinant


def main() -> None:
    """Run every bounded exact replay."""

    grade_results = {
        root_count: check_matching_grades(root_count) for root_count in (3, 4)
    }
    triangle_results = {}
    for root_count in (3, 4):
        psi = check_common_cofactor_expansion(root_count)
        triangle_results[root_count] = check_symmetric_kernel_and_triangle(
            root_count, psi
        )

    jacobian_results = {
        root_count: check_permanent_dominance(root_count) for root_count in range(2, 7)
    }

    print(
        "matching-grade/root-contraction replay: PASS "
        + ", ".join(
            f"r={root_count} ({pairs} pair, {higher} higher)"
            for root_count, (pairs, higher) in grade_results.items()
        )
    )
    print(
        "same-pair rank-one triangle replay: PASS "
        + ", ".join(
            f"r={root_count} ({charts} nonzero support charts)"
            for root_count, charts in triangle_results.items()
        )
    )
    print(
        "complementary-permanent Jacobians: PASS "
        + ", ".join(
            f"r={root_count} (rank {rank}/{outputs}, det {determinant})"
            for root_count, (outputs, rank, determinant) in jacobian_results.items()
        )
    )
    print(
        "scope: bounded exact replays; the arbitrary-r written arguments are the proofs"
    )
    print("global conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
