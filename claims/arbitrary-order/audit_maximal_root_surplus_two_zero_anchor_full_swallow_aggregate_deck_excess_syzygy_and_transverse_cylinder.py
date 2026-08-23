"""Independent no-import audit for the GLS40 aggregate-deck/cylinder result."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


Vector = tuple[Fraction, ...]


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale(scalar: Fraction, vector: Vector) -> Vector:
    return tuple(scalar * entry for entry in vector)


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def tensor(left: Vector, right: Vector) -> Vector:
    return tuple(a * b for a in left for b in right)


def standard(index: int, size: int) -> Vector:
    return tuple(Fraction(int(position == index)) for position in range(size))


def rank_rows(rows: list[Vector]) -> int:
    work = [list(row) for row in rows if any(row)]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for index, row in enumerate(work):
            if index == rank or not row[column]:
                continue
            multiple = row[column]
            work[index] = [
                left - multiple * right
                for left, right in zip(row, work[rank], strict=True)
            ]
        rank += 1
    return rank


def rank_columns(columns: list[Vector]) -> int:
    if not columns:
        return 0
    return rank_rows([tuple(entries) for entries in zip(*columns, strict=True)])


def nullspace(rows: list[Vector]) -> list[Vector]:
    if not rows:
        return []
    work = [list(row) for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for index, row in enumerate(work):
            if index == pivot_row or not row[column]:
                continue
            multiple = row[column]
            work[index] = [
                left - multiple * right
                for left, right in zip(row, work[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    free_columns = [
        column for column in range(len(work[0])) if column not in pivot_columns
    ]
    basis = []
    for free in free_columns:
        vector = [Fraction(0)] * len(work[0])
        vector[free] = Fraction(1)
        for row_index, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[row_index][free]
        basis.append(tuple(vector))
    return basis


def determinant(rows: list[Vector]) -> Fraction:
    work = [list(row) for row in rows]
    result = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next(
            (index for index in range(column, len(work)) if work[index][column]),
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
        for index in range(column + 1, len(work)):
            multiple = work[index][column]
            work[index] = [
                left - multiple * right
                for left, right in zip(work[index], work[column], strict=True)
            ]
    return sign * result


def pair_state(x_left: Vector, y_left: Vector, x_right: Vector, y_right: Vector) -> Vector:
    return add(tensor(x_left, y_right), tensor(x_right, y_left))


def canonical_excess_and_cylinders() -> dict[str, tuple[int, ...]]:
    e = [standard(index, 9) for index in range(9)]
    diagonal = [e[index] for index in (0, 4, 8)]
    q_outside = add(e[1], e[3])
    q_inside = e[0]
    extensions = [e[index] for index in (2, 5, 6, 7, 1, 3)]
    epsilon = tuple(Fraction(1) for _ in range(9))

    def project(q: Vector, vector: Vector) -> Vector:
        p = dot(epsilon, q)
        return add(scale(p, vector), scale(-dot(epsilon, vector), q))

    outside_excess = []
    inside_excess = []
    cylinders = []
    pullback_ranks = []
    for k in range(4, 10):
        outside_b = diagonal + [q_outside] + extensions[: k - 4]
        outside_s = diagonal + [q_outside]
        assert rank_columns(outside_b) == k
        projected = [project(q_outside, vector) for vector in outside_b]
        assert rank_columns(projected) == k - 1
        assert rank_columns([project(q_outside, vector) for vector in diagonal]) == 3
        annihilator_s = nullspace(outside_s)
        pullbacks = [tuple(dot(row, column) for column in outside_b) for row in annihilator_s]
        assert rank_rows(pullbacks) == k - 4
        outside_excess.append(k - 4)
        pullback_ranks.append(rank_rows(pullbacks))
        cylinders.append(9 * rank_columns(projected))

        inside_b = diagonal + extensions[: k - 3]
        assert rank_columns(inside_b) == k
        projected = [project(q_inside, vector) for vector in inside_b]
        assert rank_columns(projected) == k - 1
        assert rank_columns([project(q_inside, vector) for vector in diagonal]) == 2
        annihilator_s = nullspace(diagonal)
        pullbacks = [tuple(dot(row, column) for column in inside_b) for row in annihilator_s]
        assert rank_rows(pullbacks) == k - 3
        inside_excess.append(k - 3)

    assert tuple(cylinders) == (27, 36, 45, 54, 63, 72)
    return {
        "q_outside_excess": tuple(outside_excess),
        "q_inside_excess": tuple(inside_excess),
        "cylinders": tuple(cylinders),
        "pullback_ranks": tuple(pullback_ranks),
    }


def rank_six_sparse_word_audit() -> dict[str, int]:
    e = [standard(index, 3) for index in range(3)]

    def residual_state(colour: int) -> list[tuple[Vector, Vector]]:
        return [(e[colour], e[colour])]

    def port_states(colour: int) -> list[tuple[Vector, Vector]]:
        return [
            (e[colour], e[colour]) if index == colour else (scale(0, e[0]), scale(0, e[0]))
            for index in range(3)
        ]

    labels = {
        "q0": residual_state(0),
        "q1": residual_state(1),
        "u0": port_states(0),
        "u1": port_states(1),
        "u2": port_states(2),
        "u3": port_states(2),
    }
    sigma_columns = []
    for left, right in combinations(labels, 2):
        if (left, right) == ("q0", "q1"):
            continue
        for x_left, y_left in labels[left]:
            for x_right, y_right in labels[right]:
                sigma_columns.append(pair_state(x_left, y_left, x_right, y_right))

    q = pair_state(*labels["q0"][0], *labels["q1"][0])
    diagonal = [tensor(vector, vector) for vector in e]
    assert rank_columns(sigma_columns) == 6
    assert rank_columns(sigma_columns + [q] + diagonal) == 6
    assert rank_columns(diagonal + [q]) == 4

    aggregate_columns = []
    checked = 0
    for word in product(range(3), repeat=4):
        aggregate = tuple(Fraction(0) for _ in range(9))
        h_value = Fraction(int(word == (0, 1, 0, 0)))
        if word[2:] == (0, 0):
            aggregate = add(
                aggregate,
                scale(
                    Fraction(-1),
                    pair_state(*labels["u0"][word[0]], *labels["u1"][word[1]]),
                ),
            )
        if word[1:] == (0, 0, 0):
            aggregate = add(
                aggregate,
                scale(
                    Fraction(1, 2),
                    pair_state(*labels["q0"][0], *labels["u0"][word[0]]),
                ),
            )
        if (word[0], word[2], word[3]) == (1, 1, 1):
            aggregate = add(
                aggregate,
                scale(
                    Fraction(1, 2),
                    pair_state(*labels["q1"][0], *labels["u1"][word[1]]),
                ),
            )
        if word[:2] == (2, 2):
            aggregate = add(
                aggregate,
                scale(
                    Fraction(1, 2),
                    pair_state(*labels["u2"][word[2]], *labels["u3"][word[3]]),
                ),
            )
        target = (
            diagonal[word[0]]
            if len(set(word)) == 1
            else tuple(Fraction(0) for _ in range(9))
        )
        assert add(scale(h_value, q), aggregate) == target
        aggregate_columns.append(aggregate)
        checked += 1
    assert checked == 81
    assert rank_columns(aggregate_columns) == 4

    epsilon = tuple(Fraction(1) for _ in range(9))
    p = dot(epsilon, q)
    projected = [add(scale(p, column), scale(-dot(epsilon, column), q)) for column in sigma_columns]
    assert p == 2
    assert rank_columns(projected) == 5
    return {
        "sigma_rank": rank_columns(sigma_columns),
        "aggregate_rank": rank_columns(aggregate_columns),
        "port_words": checked,
        "excess_dimension": 2,
        "transverse_rank": rank_columns(projected),
    }


def rank_five_boundary_audit() -> dict[str, int]:
    x_u = ((0, 0, 0), (1, 1, 0), (-1, 0, 1))
    y_u = ((-1, 0, 1), (0, 0, 0), (0, 0, 0))
    x_v = ((1, 1, 0), (0, 0, 0), (0, -1, 1))
    y_v = ((0, 0, -1), (0, 1, 0), (0, 0, 1))

    def column(matrix: tuple[tuple[int, ...], ...], index: int) -> Vector:
        return tuple(Fraction(row[index]) for row in matrix)

    pair_columns = [
        pair_state(column(x_u, i), column(y_u, i), column(x_v, j), column(y_v, j))
        for i in range(3)
        for j in range(3)
    ]
    e9 = [standard(index, 9) for index in range(9)]
    diagonal = [e9[index] for index in (0, 4, 8)]
    assert rank_columns(pair_columns) == 5
    assert rank_columns(pair_columns + diagonal) == 5
    assert pair_columns[0] == scale(Fraction(-1), e9[0])
    assert pair_columns[4] == e9[4]
    assert pair_columns[8] == e9[8]

    annihilator = [e9[1], e9[2], add(e9[3], e9[5]), add(e9[6], e9[7])]
    assert all(dot(row, output) == 0 for row in annihilator for output in pair_columns)
    assert rank_rows(annihilator) == 4

    compatibility_rows: list[Vector] = []
    for matrices in ((x_u, y_u), (x_v, y_v)):
        x_other, y_other = matrices
        for index in range(3):
            other_x = column(x_other, index)
            other_y = column(y_other, index)
            for relation in annihilator:
                coefficients = []
                for variable in range(6):
                    x_z = standard(variable, 3) if variable < 3 else scale(0, e9[0][:3])
                    y_z = standard(variable - 3, 3) if variable >= 3 else scale(0, e9[0][:3])
                    coefficients.append(dot(relation, pair_state(x_z, y_z, other_x, other_y)))
                compatibility_rows.append(tuple(coefficients))
    assert len(compatibility_rows) == 24
    assert rank_rows(compatibility_rows) == 6

    independent: list[Vector] = []
    for row in compatibility_rows:
        if rank_rows(independent + [row]) > rank_rows(independent):
            independent.append(row)
        if len(independent) == 6:
            break
    independent_determinant = determinant(independent)
    assert abs(independent_determinant) == 1

    raw_left = [Fraction(1), Fraction(2), Fraction(3)]
    raw_right = [Fraction(1), Fraction(-1), Fraction(2)]
    raw_rows = [tuple(left * right for right in raw_right) for left in raw_left]
    ghz_rows = [standard(index, 3) for index in range(3)]
    assert rank_rows(raw_rows) == 1
    assert rank_rows(ghz_rows) == 3
    return {
        "pair_rank": rank_columns(pair_columns),
        "annihilator_rank": rank_rows(annihilator),
        "third_label_equations": len(compatibility_rows),
        "third_label_rank": rank_rows(compatibility_rows),
        "independent_determinant": int(independent_determinant),
        "raw_flattening_rank": rank_rows(raw_rows),
        "ghz_flattening_rank": rank_rows(ghz_rows),
    }


def main() -> None:
    strata = canonical_excess_and_cylinders()
    rank_six = rank_six_sparse_word_audit()
    rank_five = rank_five_boundary_audit()
    print("GLS40 independent no-import aggregate/cylinder audit: PASS")
    print("  canonical excess/cylinders:", strata)
    print("  rank-six sparse-word interface:", rank_six)
    print("  rank-five mixed/pure boundary:", rank_five)


if __name__ == "__main__":
    main()
